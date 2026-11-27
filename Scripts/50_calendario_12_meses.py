""" 
Calendario de obra de 12 meses (CX-2).
Entrada: catalogo_v01.json si existe; en su ausencia usa estructura temporal por capítulo.
Salida: _harness/intermedios/calendario/calendario_v01.json y Calendario/Calendario_v01.xlsx
Dependencias: openpyxl; schema Scripts/schemas/calendario.py.
Fecha: 23-11-2026. Idempotente: reconstruye los dos entregables desde las entradas.
"""
from __future__ import annotations

import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
INTERMEDIATE = ROOT / "_harness/intermedios/calendario/calendario_v01.json"
EXCEL = ROOT / "Calendario/Calendario_v01.xlsx"
PROJECT = 'Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"'

# Programa preliminar por secuencia de capítulos; reemplazar por partidas del catálogo
# y recalcular duraciones cuando estén disponibles memoria y PROGRAMA DE OBRA.
PLAN = [
    ("01", "Preliminares", "F1", 1, 1, []),
    ("02", "Cimentación", "F1", 1, 2, ["01"]),
    ("03", "Estructura de concreto y mampostería confinada", "F1", 2, 5, ["02"]),
    ("05", "Albañilería", "F1", 3, 6, ["02"]),
    ("04", "Estructura metálica y cubierta", "F2", 5, 6, ["03", "05"]),
    ("08", "Instalación hidráulica y pluvial", "F3", 5, 9, ["05"]),
    ("09", "Instalación sanitaria", "F3", 5, 9, ["05"]),
    ("10", "Instalación eléctrica y fotovoltaica", "F3", 5, 9, ["05"]),
    ("06", "Acabados", "F4", 7, 10, ["04", "08", "09", "10"]),
    ("07", "Herrería y cancelería", "F4", 7, 10, ["04"]),
    ("13", "Mobiliario y equipamiento fijo", "F5", 11, 12, ["06", "07"]),
    ("14", "Limpieza final y entrega", "F5", 12, 12, ["13"]),
]


def main() -> None:
    catalog = ROOT / "_harness/intermedios/precios/catalogo_v01.json"
    if catalog.exists():
        raise SystemExit("Catálogo encontrado: integrar sus claves antes de generar; no sobrescribir estructura temporal.")
    rows = []
    for chapter, title, front, start, end, parents in PLAN:
        pct = [0.0] * 12
        for m in range(start, end + 1):
            pct[m - 1] = 100.0 / (end - start + 1)
        # Claves técnicas temporales (subcapítulo 99); sustituir con claves AG-2.
        key = f"ED-{chapter}-99-001"
        rows.append({"clave": key, "concepto": f"Estructura temporal capítulo {chapter}: {title}",
                     "frente": front, "mes_inicio": start, "mes_fin": end,
                     "avance_mensual_pct": pct,
                     "predecesoras": [f"ED-{p}-99-001" for p in parents],
                     "ruta_critica": False, "importe": None})
    # CPM sobre duraciones de las ventanas programadas. Holgura cero = ruta crítica.
    by_key = {a["clave"]: a for a in rows}
    ef: dict[str, int] = {}
    for a in rows:
        dur = a["mes_fin"] - a["mes_inicio"] + 1
        es = max((ef[p] for p in a["predecesoras"]), default=0)
        ef[a["clave"]] = es + dur
    project_end = max(ef.values())
    ls: dict[str, int] = {}
    for a in reversed(rows):
        successors = [b for b in rows if a["clave"] in b["predecesoras"]]
        dur = a["mes_fin"] - a["mes_inicio"] + 1
        latest_finish = min((ls[b["clave"]] for b in successors), default=project_end)
        ls[a["clave"]] = latest_finish - dur
        earliest_start = max((ef[p] for p in a["predecesoras"]), default=0)
        a["ruta_critica"] = ls[a["clave"]] == earliest_start
    data = {"version": "v01", "fecha": "23-11-2026", "fecha_inicio_obra": "04-01-2027",
            "duracion_meses": 12, "presupuesto_usado": None, "actividades": rows, "total_importe": None}
    INTERMEDIATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = INTERMEDIATE.with_name(INTERMEDIATE.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(INTERMEDIATE)

    wb = Workbook()
    ws = wb.active
    ws.title = "Programa 2027"
    ws.append([PROJECT])
    ws.append(["Fecha: 23-11-2026", "Versión: v01", "Responsable: CX-2 (PC-B)"])
    ws.append(["Calendario estructural provisional · claves por capítulo sujetas a catálogo AG-2"])
    ws.append(["Clave", "Concepto", "Frente", "Importe", *[f"Mes {i}" for i in range(1, 13)], "Inicio", "Fin", "Predecesoras", "Ruta crítica"])
    header = 4
    for a in rows:
        vals = [a["clave"], a["concepto"], a["frente"], None,
                *[p / 100 for p in a["avance_mensual_pct"]], a["mes_inicio"], a["mes_fin"],
                ", ".join(a["predecesoras"]), "Sí" if a["ruta_critica"] else "No"]
        ws.append(vals)
        rr = ws.max_row
        for col in range(5, 17):
            if ws.cell(rr, col).value:
                ws.cell(rr, col).fill = PatternFill("solid", fgColor="F4B183" if a["ruta_critica"] else "9DC3E6")
            ws.cell(rr, col).number_format = "0.00%"
        ws.cell(rr, 4).number_format = '$#,##0.00'
    totalrow = ws.max_row + 1
    ws.cell(totalrow, 1, "Avance financiero mensual")
    ws.cell(totalrow + 1, 1, "Avance financiero acumulado")
    ws.cell(totalrow + 2, 1, "Subtotal del presupuesto")
    for c in range(5, 17):
        letter = get_column_letter(c)
        ws.cell(totalrow + 1, c, f"=SUM({letter}{header+1}:{letter}{totalrow-1})")
        ws.cell(totalrow + 1, c).number_format = "0.00%"
        ws.cell(totalrow + 2, c, f"=SUM($E${totalrow+1}:{letter}${totalrow+1})")
        ws.cell(totalrow + 2, c).number_format = "0.00%"
    ws.cell(totalrow + 3, 1, "Importes pendientes del presupuesto aprobado (T-503)")
    ws.merge_cells(start_row=totalrow+3, start_column=1, end_row=totalrow+3, end_column=20)
    widths = [18, 52, 10, 15] + [11] * 12 + [10, 10, 28, 14]
    for c, width in enumerate(widths, 1): ws.column_dimensions[get_column_letter(c)].width = width
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=20)
    ws.freeze_panes = "E5"
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[1].height = 28
    ws["A1"].font = Font(size=14, bold=True, color="FFFFFF")
    ws["A1"].fill = PatternFill("solid", fgColor="1F4E78")
    ws["A3"].font = Font(italic=True, color="9C0006")
    for cell in ws[header]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="4472C4")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for row in ws.iter_rows(min_row=header+1, max_row=totalrow+2):
        for cell in row:
            cell.border = Border(bottom=Side(style="hair", color="B4C6E7"))
            if cell.column >= 5: cell.alignment = Alignment(horizontal="center")
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = f"A1:T{totalrow+3}"
    ws.print_title_rows = "1:4"
    ws.page_margins.left = ws.page_margins.right = 0.5
    ws.page_margins.top = ws.page_margins.bottom = 0.75
    ws.oddHeader.center.text = PROJECT
    ws.oddHeader.right.text = "Versión v01 · &D"
    ws.oddFooter.left.text = "Responsable: CX-2 (PC-B)"
    ws.oddFooter.right.text = "Página &P de &N"
    EXCEL.parent.mkdir(parents=True, exist_ok=True)
    xtmp = EXCEL.with_name(EXCEL.name + ".tmp.xlsx")
    wb.save(xtmp)
    wb.close()
    xtmp.replace(EXCEL)


if __name__ == "__main__":
    main()
