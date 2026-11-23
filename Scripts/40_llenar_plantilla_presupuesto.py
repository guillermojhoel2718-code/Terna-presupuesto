"""Presupuesto desde un intermedio validado, conservando la plantilla XLSM.

Entrada: _harness/intermedios/presupuesto/presupuesto_vNN.json (schema presupuesto).
Salida: Presupuesto/Presupuesto_vNN.xlsm; opcionalmente actualiza el JSON validado.
Dependencias: openpyxl, pydantic>=2, Excel instalado (COM de PowerShell).
Fecha: 23-11-2026
Dueño: CX-1. Las cantidades y costos directos provienen de intermedios aprobados.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import zipfile
import subprocess
import sys
import tempfile
from datetime import datetime
from copy import copy
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from openpyxl.comments import Comment
from openpyxl.styles import Font

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Scripts" / "schemas"))
from presupuesto import Presupuesto  # noqa: E402

CHAPTERS = {
    1: "Preliminares", 2: "Cimentación",
    3: "Estructura de concreto y mampostería confinada",
    4: "Estructura metálica y cubierta", 5: "Albañilería", 6: "Acabados",
    7: "Herrería y cancelería", 8: "Instalación hidráulica y pluvial",
    9: "Instalación sanitaria", 10: "Instalación eléctrica y fotovoltaica",
    11: "Voz y datos — fuera de alcance", 12: "CCTV y seguridad — fuera de alcance",
    13: "Mobiliario y equipamiento fijo", 14: "Limpieza final y entrega",
}


def atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load_model(path: Path) -> tuple[dict[str, Any], Presupuesto]:
    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    return raw, Presupuesto.model_validate(raw)


def item_key(part: dict[str, Any]) -> tuple[int, int, int]:
    prefix, cc, ss, nnn = part["clave"].split("-")
    if prefix != "ED":
        raise ValueError(f"Alcance fuera de ED: {part['clave']}")
    return int(cc), int(ss), int(nnn)


def powershell_calculate(path: Path) -> dict[str, float]:
    """Itera en Excel COM. El libro y Excel siempre se cierran en finally."""
    ps = r'''param([string]$WorkbookPath)
$excel = $null; $book = $null; $sheet = $null
try {
  $excel = New-Object -ComObject Excel.Application
  $excel.Visible = $false; $excel.DisplayAlerts = $false; $excel.EnableEvents = $false
  $book = $excel.Workbooks.Open($WorkbookPath, 0, $false)
  $sheet = $book.Worksheets.Item('D25-00_Presupuesto')
  $over = $book.Worksheets.Item('D25-00_Sobrecosto')
  $sheet.Range('J16').Value2 = 1.0
  $factor = 1.0
  for ($i = 0; $i -lt 30; $i++) {
    $excel.CalculateFullRebuild()
    $cd = [double]$over.Range('AW5').Value2
    $pv = [double]$over.Range('AW215').Value2
    if ($cd -le 0) { throw 'Costo directo cero: no se puede calcular el factor.' }
    $next = $pv / $cd
    if ([Math]::Abs($next - $factor) -lt 0.0001) { $factor = $next; break }
    $factor = $next; $sheet.Range('J16').Value2 = $factor
  }
  $sheet.Range('J16').Value2 = $factor
  $excel.CalculateFullRebuild()
  $out = [ordered]@{ factor=$factor; costo_directo=[double]$over.Range('AW5').Value2;
    indirectos=[double]$over.Range('AD200').Value2; financiamiento=[double]$over.Range('AD209').Value2;
    utilidad=[double]$over.Range('AD210').Value2; cargos_adicionales=[double]$over.Range('AD211').Value2;
    precio_venta=[double]$over.Range('AW215').Value2; factor_financiamiento=[double]$over.Range('BE209').Value2;
    factor_utilidad=[double]$over.Range('BE210').Value2; factor_cargos=[double]$over.Range('BE211').Value2;
    iteraciones=$i+1 }
  $book.Save()
  Write-Output ('CX1_RESULT:' + ($out | ConvertTo-Json -Compress))
}
finally {
  if ($book -ne $null) { $book.Close($true) }
  if ($excel -ne $null) { $excel.Quit() }
  if ($sheet -ne $null) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($sheet) }
  if ($book -ne $null) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($book) }
  if ($excel -ne $null) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($excel) }
  [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}'''
    with tempfile.NamedTemporaryFile("w", suffix=".ps1", encoding="utf-8", delete=False, dir=path.parent) as f:
        f.write(ps)
        ps_path = Path(f.name)
    try:
        proc = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps_path), str(path)],
            text=True, capture_output=True, check=False,
        )
        if proc.returncode:
            raise RuntimeError(f"Excel COM falló ({proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}")
        marker = next((line for line in proc.stdout.splitlines() if line.startswith("CX1_RESULT:")), None)
        if not marker:
            raise RuntimeError(f"Excel COM no devolvió resultados: {proc.stdout} {proc.stderr}")
        result = json.loads(marker.removeprefix("CX1_RESULT:"))
        if result["iteraciones"] >= 30:
            raise RuntimeError("El factor no convergió en 30 iteraciones.")
        return result
    finally:
        ps_path.unlink(missing_ok=True)


def patch_print_settings(path: Path) -> None:
    """Restaura Carta/fit-to-width tras Excel COM sin invalidar cachés de fórmulas."""
    tmp = path.with_name(path.stem + ".print.tmp" + path.suffix)
    with zipfile.ZipFile(path, "r") as src, zipfile.ZipFile(tmp, "w") as dst:
        for info in src.infolist():
            payload = src.read(info.filename)
            if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", info.filename):
                xml = payload.decode("utf-8")
                setup = re.search(r"<pageSetup\b([^>]*)/>", xml)
                if setup:
                    attrs = dict(re.findall(r'([A-Za-z_:][A-Za-z0-9_.:-]*)="([^"]*)"', setup.group(1)))
                    attrs.pop("scale", None)
                    attrs.update({"paperSize": "1", "fitToWidth": "1", "fitToHeight": "0"})
                    rendered = "<pageSetup " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + "/>"
                    xml = xml[:setup.start()] + rendered + xml[setup.end():]
                margins = re.search(r"<pageMargins\b([^>]*)/>", xml)
                if margins:
                    attrs = dict(re.findall(r'([A-Za-z_:][A-Za-z0-9_.:-]*)="([^"]*)"', margins.group(1)))
                    attrs.update({"left": "0.5", "right": "0.5", "top": "0.75", "bottom": "0.75"})
                    rendered = "<pageMargins " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + "/>"
                    xml = xml[:margins.start()] + rendered + xml[margins.end():]
                pspr = re.search(r"<pageSetUpPr\b([^>]*)/>", xml)
                if pspr:
                    attrs = dict(re.findall(r'([A-Za-z_:][A-Za-z0-9_.:-]*)="([^"]*)"', pspr.group(1)))
                    attrs["fitToPage"] = "1"
                    rendered = "<pageSetUpPr " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + "/>"
                    xml = xml[:pspr.start()] + rendered + xml[pspr.end():]
                elif "</sheetPr>" in xml:
                    xml = xml.replace("</sheetPr>", '<pageSetUpPr fitToPage="1"/></sheetPr>', 1)
                else:
                    root = re.search(r"<worksheet\b[^>]*>", xml)
                    if root:
                        xml = xml[:root.end()] + '<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>' + xml[root.end():]
                payload = xml.encode("utf-8")
            dst.writestr(info, payload)
    os.replace(tmp, path)

def copy_row_style(ws: Any, source_row: int, target_row: int, max_col: int = 12) -> None:
    for col in range(1, max_col + 1):
        ws.cell(target_row, col)._style = copy(ws.cell(source_row, col)._style)
        if ws.row_dimensions[source_row].height is not None:
            ws.row_dimensions[target_row].height = ws.row_dimensions[source_row].height

def write_rows(workbook_path: Path, data: dict[str, Any], factor: float) -> None:
    wb = load_workbook(workbook_path, keep_vba=True)
    ws = wb["D25-00_Presupuesto"]
    summary = wb["D25-00_Resumen"]
    ws["J16"] = factor
    # Limpia valores anteriores sin tocar el diseño ni la macro.
    for row in range(17, max(ws.max_row, 1000) + 1):
        for col in range(1, 13):
            ws.cell(row, col).value = None
            ws.cell(row, col).comment = None
    parts = sorted(data["partidas"], key=item_key)
    groups: dict[int, dict[int, list[dict[str, Any]]]] = {}
    for part in parts:
        cc, ss, _ = item_key(part)
        groups.setdefault(cc, {}).setdefault(ss, []).append(part)
    chapter_rows: dict[int, int] = {}
    detail_rows: list[int] = []
    row = 17
    for cc in range(1, 15):
        chapter_parts = groups.get(cc)
        if not chapter_parts:
            continue
        chapter_row = row
        copy_row_style(ws, 17, row)
        chapter_rows[cc] = row
        ws.cell(row, 1).value = cc
        ws.cell(row, 3).value = CHAPTERS[cc]
        ws.cell(row, 3).font = Font(bold=True)
        chapter_subtotals: list[int] = []
        row += 1
        for ss, concepts in sorted(chapter_parts.items()):
            subrow = row
            copy_row_style(ws, 18, row)
            ws.cell(row, 1).value = f"{cc}.{ss}"
            ws.cell(row, 3).value = concepts[0]["subcapitulo"]
            ws.cell(row, 3).font = Font(bold=True)
            row += 1
            item_rows = []
            for part in concepts:
                _, _, nnn = item_key(part)
                r = row
                copy_row_style(ws, 20, r)
                item_rows.append(r)
                detail_rows.append(r)
                ws.cell(r, 1).value = f"{cc}.{ss}.{nnn}"
                ws.cell(r, 2).value = part["clave"]
                ws.cell(r, 3).value = part["concepto"]
                ws.cell(r, 4).value = part["unidad"].value if hasattr(part["unidad"], "value") else part["unidad"]
                ws.cell(r, 5).value = part["cantidad"]
                ws.cell(r, 6).value = f"=J{r}*$J$16"
                ws.cell(r, 7).value = f"=E{r}*F{r}"
                ws.cell(r, 8).value = None
                ws.cell(r, 10).value = part["precio_unitario_cd"]
                ws.cell(r, 12).value = f"=E{r}*J{r}"
                ws.cell(r, 2).comment = Comment(f"Fuente: {part['fuente']}", "CX-1")
                for col in (5, 10, 12):
                    ws.cell(r, col).number_format = '#,##0.00'
                for col in (6, 7):
                    ws.cell(r, col).number_format = '$#,##0.00'
                ws.cell(r, 8).number_format = '0.00%'
                row += 1
            sub_total_row = row
            copy_row_style(ws, 21, row)
            ws.cell(row, 1).value = f"{cc}.{ss}"
            ws.cell(row, 2).value = "Total de:"
            ws.cell(row, 3).value = f"={ws.cell(subrow, 3).coordinate}"
            ws.cell(row, 7).value = f"=SUM(G{item_rows[0]}:G{item_rows[-1]})"
            ws.cell(row, 8).value = f"=IFERROR(G{row}/$G${row},0)"
            chapter_subtotals.append(row)
            row += 1
        ws.cell(chapter_row, 2).value = "Total de capítulo"
        ws.cell(chapter_row, 7).value = "=" + "+".join(f"G{x}" for x in chapter_subtotals)
        ws.cell(chapter_row, 12).value = "=" + "+".join(f"L{x}" for x in chapter_subtotals)
        ws.cell(chapter_row, 3).comment = Comment(
            "Fuentes: " + "; ".join(p["fuente"] for ps in chapter_parts.values() for p in ps), "CX-1")
    subtotal_row = row
    copy_row_style(ws, 23, row)
    copy_row_style(ws, 24, row + 1)
    copy_row_style(ws, 24, row + 2)
    if detail_rows:
        ws["L16"] = "=SUBTOTAL(9," + ",".join(f"L{x}" for x in detail_rows) + ")"
    for r in detail_rows:
        ws.cell(r, 8).value = f"=IFERROR(G{r}/$G${subtotal_row},0)"
    ws.cell(row, 2).value = "SUBTOTAL"
    ws.cell(row, 7).value = "=" + "+".join(f"G{x}" for x in chapter_rows.values())
    ws.cell(row, 12).value = "=" + "+".join(f"L{x}" for x in chapter_rows.values())
    ws.cell(row, 8).value = f"=IFERROR(G{subtotal_row}/G{subtotal_row},0)"
    ws.cell(row + 1, 2).value = "IVA"
    ws.cell(row + 1, 7).value = f"=G{subtotal_row}*{float(data['sobrecosto']['iva_tasa']):.12g}"
    ws.cell(row + 2, 2).value = "TOTAL"
    ws.cell(row + 2, 7).value = f"=G{subtotal_row}+G{row + 1}"
    for r in (subtotal_row, subtotal_row + 1, subtotal_row + 2):
        ws.cell(r, 7).number_format = '$#,##0.00'
    # Resumen por capítulo, con subtotal y participaciones formuladas.
    for r in range(18, 32):
        if r != 18:
            copy_row_style(summary, 18, r, 7)
        for c in range(1, 8):
            summary.cell(r, c).value = None
            summary.cell(r, c).comment = None
    for cc in range(1, 15):
        r = 17 + cc
        summary.cell(r, 1).value = cc
        summary.cell(r, 2).value = CHAPTERS[cc]
        if cc in chapter_rows:
            summary.cell(r, 5).value = f"='{ws.title}'!G{chapter_rows[cc]}"
        else:
            summary.cell(r, 5).value = 0
        summary.cell(r, 6).value = f"=IFERROR(E{r}/$E$32,0)"
        summary.cell(r, 5).number_format = '$#,##0.00'
        summary.cell(r, 6).number_format = '0.00%'
    summary["D32"] = "Subtotal del Presupuesto mostrado sin Impuestos"
    summary["E32"] = "=" + "+".join(f"E{r}" for r in range(18, 32))
    summary["D33"] = "IVA"
    summary["E33"] = f"=E32*{float(data['sobrecosto']['iva_tasa']):.12g}"
    summary["D34"] = "Total"
    summary["E34"] = "=E32+E33"
    summary.print_area = "A1:G113"
    summary.print_title_rows = "1:17"
    ws.print_area = f"A1:H{row + 2}"
    ws.print_title_rows = "1:16"
    project = 'Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"'
    version = data["version"]
    fecha = data["fecha"]
    for sheet in (summary, ws):
        sheet.oddHeader.center.text = project
        sheet.oddHeader.right.text = f"Versión {version} · {fecha}"
        sheet.oddFooter.left.text = "Responsable: CX-1"
        sheet.oddFooter.right.text = "Página &P de &N"
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    wb.save(workbook_path)


def updated_budget(data: dict[str, Any], cells: dict[str, float]) -> dict[str, Any]:
    factor = cells["factor"]
    iva_tasa = float(data["sobrecosto"]["iva_tasa"])
    subtotal = 0.0
    for part in data["partidas"]:
        part["precio_unitario"] = part["precio_unitario_cd"] * factor
        part["importe"] = part["cantidad"] * part["precio_unitario"]
        subtotal += part["importe"]
    iva = subtotal * iva_tasa
    data["subtotal"] = subtotal
    data["iva"] = iva
    data["total"] = subtotal + iva
    data["sobrecosto"] = {
        "periodo_meses": 12, "costo_directo": cells["costo_directo"],
        "indirectos": cells["indirectos"], "financiamiento": cells["financiamiento"],
        "utilidad": cells["utilidad"], "cargos_adicionales": cells["cargos_adicionales"],
        "precio_venta_sin_iva": cells["precio_venta"], "factor_sobrecosto": factor,
        "iva_tasa": iva_tasa,
        "celdas_origen": {
            "indirectos": "D25-00_Sobrecosto!AD200", "financiamiento": "D25-00_Sobrecosto!AD209",
            "utilidad": "D25-00_Sobrecosto!AD210", "cargos_adicionales": "D25-00_Sobrecosto!AD211",
            "precio_venta_sin_iva": "D25-00_Sobrecosto!AW215", "costo_directo": "D25-00_Sobrecosto!AW5",
            "factor_financiamiento": "D25-00_Sobrecosto!BE209", "factor_utilidad": "D25-00_Sobrecosto!BE210",
            "factor_cargos": "D25-00_Sobrecosto!BE211",
            "iva_tasa": data["sobrecosto"]["celdas_origen"]["iva_tasa"],
        },
    }
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, required=True, help="Presupuesto preliminar con partidas/CD y tasa IVA trazada")
    parser.add_argument("--plantilla", type=Path, default=ROOT / "Presupuesto" / "Presupuesto_v00_base.xlsm")
    parser.add_argument("--salida-xlsm", type=Path, required=True)
    parser.add_argument("--salida-json", type=Path, help="Destino atómico del presupuesto calculado; si se omite no cambia el JSON fuente")
    parser.add_argument("--recalcular", action="store_true", default=True, help="Recalcula hoja de sobrecosto con Excel COM (siempre requerido)")
    parser.add_argument("--overwrite", action="store_true", help="Permite reemplazar solo un XLSM de salida de prueba/no aprobado")
    args = parser.parse_args()
    raw, model = load_model(args.json)
    if raw.get("sobrecosto", {}).get("iva_tasa") is None or not raw.get("sobrecosto", {}).get("celdas_origen", {}).get("iva_tasa"):
        raise ValueError("La tasa IVA debe venir con una celda de origen identificada, no de un porcentaje supuesto.")
    data = raw
    target = args.salida_xlsm.resolve()
    if target.exists() and not args.overwrite:
        raise FileExistsError(f"No se sobrescribe entregable existente: {target}; para una salida de prueba indica --overwrite")
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(target.stem + ".tmp" + target.suffix)
    shutil.copy2(args.plantilla, tmp)
    try:
        write_rows(tmp, data, 1.0)
        if args.recalcular:
            cells = powershell_calculate(tmp)
            patch_print_settings(tmp)
            result = updated_budget(data, cells)
            Presupuesto.model_validate(result)
            # Guarda el factor calculado en la hoja después de la iteración COM.
            if args.salida_json:
                if args.salida_json.resolve().exists():
                    raise FileExistsError(f"No se sobrescribe intermedio existente: {args.salida_json.resolve()}")
                atomic_json(args.salida_json.resolve(), result)
        else:
            cells = None
        os.replace(tmp, target)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
    print(json.dumps({"workbook": str(target), "factor": cells["factor"] if cells else None}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())






