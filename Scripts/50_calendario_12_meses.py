"""Calendario de obra 2027 (CX-2).
Entrada: catalogo_v01.json (claves/conceptos), indice Revit (contexto de niveles).
Salida: calendario_v01.json y Calendario_v01.xlsx; hoja Pendientes con cantidades/rendimientos faltantes.
Dependencias: pydantic, openpyxl. Ejecutar con Python absoluto del equipo.
Fecha: 23-11-2026. Idempotente: reconstruye desde entradas fuente.
"""
from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "_harness/intermedios/precios/catalogo_v01.json"
INDEX = ROOT / "_harness/intermedios/revit/indice.json"
JSON_OUT = ROOT / "_harness/intermedios/calendario/calendario_v01.json"
XLSX_OUT = ROOT / "Calendario/Calendario_v01.xlsx"
PROJECT = 'Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"'
PYTHON_NOTE = "Duración SUPUESTO; recalcular como cantidad / (rendimiento de cuadrilla × cuadrillas × jornadas/mes) cuando se apruebe generador."
FRONTS = {"01":"F1","02":"F1","03":"F1","05":"F1","04":"F2","08":"F3","09":"F3","10":"F3","06":"F4","07":"F4","13":"F5","14":"F5"}
# Ventanas preliminares; total del proyecto enero-diciembre = 12 meses.
# Las partidas dentro de cada capítulo comparten una ventana hasta disponer de generadores por clave.
CHAPTER_WINDOWS = {
    "01": (1, 1), "02": (2, 3), "03": (4, 6), "05": (5, 8),
    "04": (7, 8), "06": (9, 10), "07": (9, 10), "13": (11, 11), "14": (12, 12),
}
# Conceptos de montaje terminal/equipamiento se coordinan con acabados (F3 con F4).
LATE_INSTALL_SUBCHAPTERS = {"08": {"02","03"}, "09": {"02"}, "10": {"02","03","04","05"}}
EARLY_INSTALL_SUBCHAPTERS = {"08": {"01"}, "09": {"01","03"}, "10": {"01"}}
INSTALL_WINDOWS = {"early": (5, 7), "late": (9, 10)}


def month_window(chapter: str, subchapter: str) -> tuple[int, int]:
    if chapter in EARLY_INSTALL_SUBCHAPTERS and subchapter in EARLY_INSTALL_SUBCHAPTERS[chapter]:
        return INSTALL_WINDOWS["early"]
    if chapter in LATE_INSTALL_SUBCHAPTERS and subchapter in LATE_INSTALL_SUBCHAPTERS[chapter]:
        return INSTALL_WINDOWS["late"]
    return CHAPTER_WINDOWS[chapter]


def activity_relation(pred: dict, succ: dict) -> tuple[str, int]:
    pc, sc, ss = pred["capitulo"], succ["capitulo"], succ["subcapitulo"]
    if pc == "03" and sc == "05": return "SS", 1  # albañilería escalonada por niveles
    if pc == "05" and sc in {"08","09","10"} and ss in EARLY_INSTALL_SUBCHAPTERS[sc]: return "SS", 0
    if pc == "06" and sc in {"08","09","10"} and ss in LATE_INSTALL_SUBCHAPTERS[sc]: return "SS", 0
    return "FS", 0


def chapter_predecessor_chapters(a: dict) -> list[str]:
    ch, sub = a["capitulo"], a["subcapitulo"]
    if ch == "01": return []
    if ch == "02": return ["01"]
    if ch == "03": return ["02"]
    if ch in {"04","05"}: return ["03"]
    if ch in {"08","09","10"}:
        return ["05"] if sub in EARLY_INSTALL_SUBCHAPTERS[ch] else ["06"]
    if ch == "06": return ["04","08-rough","09-rough","10-rough"]
    if ch == "07": return ["04"]
    if ch == "13": return ["06","07"]
    if ch == "14": return ["13"]
    raise ValueError(f"Capítulo fuera de alcance: {ch}")


def build_activities(catalog: dict, levels_count: int) -> list[dict]:
    concepts = catalog["conceptos"]
    keys = [c["clave"] for c in concepts]
    if len(keys) != len(set(keys)):
        raise ValueError("El catálogo contiene claves duplicadas")
    if any(c["capitulo"] not in FRONTS for c in concepts):
        raise ValueError("El catálogo contiene un capítulo sin frente definido")
    rows = []
    for c in concepts:
        ch, sub = c["capitulo"], c["subcapitulo"]
        start, end = month_window(ch, sub)
        pct = [0.0] * 12
        for m in range(start, end + 1): pct[m-1] = 100.0 / (end-start+1)
        if ch == "03": reason = f"SUPUESTO: estructura de concreto distribuida en {levels_count} niveles principales; ventana de 3 meses (validar con cantidades y rendimiento de cuadrilla)."
        elif ch == "05": reason = f"SUPUESTO: albañilería por niveles, solapada con estructura; ventana de 4 meses para {levels_count} niveles (validar con cantidades y rendimiento)."
        elif ch in {"08","09","10"} and sub in EARLY_INSTALL_SUBCHAPTERS[ch]: reason = "SUPUESTO: ranurado/ductos/ramales iniciales en paralelo con albañilería; 3 meses. Recalcular con cantidad/rendimiento."
        elif ch in {"08","09","10"}: reason = "SUPUESTO: muebles, equipos y conexiones finales coordinados con acabados; 2 meses. Recalcular con cantidad/rendimiento."
        elif ch == "04": reason = "SUPUESTO: montaje de estructura metálica/cubierta tras cierre de estructura de concreto; 2 meses. Recalcular con cantidad/rendimiento."
        elif ch == "02": reason = "SUPUESTO: excavaciones, plantilla, cimentación y rellenos; 2 meses. Recalcular con cantidades y rendimientos de cuadrilla."
        elif ch == "01": reason = "SUPUESTO: habilitación, limpieza y trazo inicial; 1 mes. Recalcular con cantidad/rendimiento."
        elif ch in {"06","07"}: reason = "SUPUESTO: acabados/cancelería después de cubierta; 2 meses. Recalcular con cantidad/rendimiento."
        elif ch == "13": reason = "SUPUESTO: mobiliario/equipamiento en penúltimo mes (F5); 1 mes. Recalcular con cantidad/rendimiento."
        else: reason = "SUPUESTO: limpieza y entrega en diciembre (F5); 1 mes. Recalcular con cantidad/rendimiento."
        rows.append({"clave":c["clave"],"concepto":c["concepto"],"capitulo":ch,"subcapitulo":sub,
                     "frente":FRONTS[ch],"mes_inicio":start,"mes_fin":end,"duracion_meses":end-start+1,
                     "justificacion":reason,"avance_mensual_pct":pct,"predecesoras":[],"ruta_critica":False,"importe":None})
    by_ch = defaultdict(list)
    for a in rows: by_ch[a["capitulo"]].append(a)
    rough = [a for a in rows if a["capitulo"] in {"08","09","10"} and a["subcapitulo"] in EARLY_INSTALL_SUBCHAPTERS[a["capitulo"]]]
    for a in rows:
        groups = chapter_predecessor_chapters(a)
        preds=[]
        for group in groups:
            if group.endswith("-rough"):
                source=group[:2]
                preds.extend(p["clave"] for p in rough if p["capitulo"] == source)
            else:
                preds.extend(p["clave"] for p in by_ch[group])
        a["predecesoras"] = sorted(set(preds))
    return rows


def compute_cpm(rows: list[dict]) -> dict[str, int]:
    by_key={a["clave"]:a for a in rows}
    successors=defaultdict(list); indegree={a["clave"]:0 for a in rows}; rel={}
    for a in rows:
        for pk in a["predecesoras"]:
            p=by_key[pk]; kind,lag=activity_relation(p,a)
            rel[(pk,a["clave"])]=(kind,lag)
            successors[pk].append(a["clave"]); indegree[a["clave"]]+=1
    queue=deque(k for k,v in indegree.items() if v==0); order=[]
    while queue:
        k=queue.popleft(); order.append(k)
        for s in successors[k]:
            indegree[s]-=1
            if indegree[s]==0: queue.append(s)
    if len(order)!=len(rows): raise ValueError("Ciclo en las predecesoras del calendario")
    es={}; ef={}
    for k in order:
        a=by_key[k]; starts=[0]
        for p in a["predecesoras"]:
            pk=p; kind,lag=rel[(pk,k)]
            starts.append(es[pk]+(by_key[pk]["duracion_meses"] if kind=="FS" else 0)+lag)
        es[k]=max(starts); ef[k]=es[k]+a["duracion_meses"]
    project_end=max(ef.values())
    if project_end!=12: raise ValueError(f"Red de dependencias produce {project_end} meses, se requieren 12 exactos")
    ls={}
    for k in reversed(order):
        a=by_key[k]
        limits=[project_end-a["duracion_meses"]]
        for s in successors[k]:
            kind,lag=rel[(k,s)]
            limits.append(ls[s]-lag-(a["duracion_meses"] if kind=="FS" else 0))
        ls[k]=min(limits)
        total_float=ls[k]-es[k]
        if total_float<0: raise ValueError(f"Calendario inviable: holgura negativa en {k}: {total_float}")
        a["ruta_critica"]=(total_float==0)
        a["_holgura_meses"]=total_float
        planned=a["mes_inicio"]-1
        if es[k]!=planned:
            raise ValueError(f"Mes propuesto {a['mes_inicio']} no coincide con CPM temprano {es[k]+1} para {k}")
    return {k:v for k,v in ls.items()}


def build_workbook(rows: list[dict], levels_count: int) -> None:
    wb=Workbook(); ws=wb.active; ws.title="Programa"
    ws.append([PROJECT]); ws.append(["Fecha: 23-11-2026","Versión: v01","Responsable: CX-2 (PC-B)"])
    ws.append([f"SUPUESTOS de duración para ~2,500 m² / {levels_count} niveles principales; usar cantidad / rendimiento de cuadrilla al recibir generadores."])
    headers=["Clave","Concepto","Capítulo","Subcapítulo","Frente","Importe"]+[f"Mes {i} %" for i in range(1,13)]+["Inicio","Fin","Duración (meses)","Holgura (meses)","Justificación de duración","Predecesoras","Vínculo CPM"]
    ws.append(headers); headerrow=4
    for a in rows:
        rel_text=[]
        for pk in a["predecesoras"]:
            p=next(x for x in rows if x["clave"]==pk); kind,lag=activity_relation(p,a)
            rel_text.append(f"{pk} {kind}{lag:+d}m" if kind=="SS" and lag else f"{pk} {kind}")
        ws.append([a["clave"],a["concepto"],a["capitulo"],a["subcapitulo"],a["frente"],None,
                   *[x/100 for x in a["avance_mensual_pct"]],a["mes_inicio"],a["mes_fin"],a["duracion_meses"],a["_holgura_meses"],a["justificacion"],"; ".join(a["predecesoras"]),"; ".join(rel_text)])
        rr=ws.max_row
        ws.cell(rr,6).number_format='$#,##0.00'
        for col in range(7,19):
            ws.cell(rr,col).number_format='0.00%'
            if ws.cell(rr,col).value:
                color="F4B183" if a["ruta_critica"] else "9DC3E6"
                ws.cell(rr,col).fill=PatternFill("solid",fgColor=color)
        ws.cell(rr,22).number_format='0.00'
        ws.cell(rr,23).alignment=Alignment(wrap_text=True,vertical='top')
    n=len(rows); first=headerrow+1; last=headerrow+n
    ws.freeze_panes="G5"; ws.sheet_view.showGridLines=False
    ws.merge_cells(start_row=1,start_column=1,end_row=1,end_column=25)
    ws.merge_cells(start_row=3,start_column=1,end_row=3,end_column=25)
    ws["A1"].font=Font(size=14,bold=True,color="FFFFFF"); ws["A1"].fill=PatternFill("solid",fgColor="1F4E78")
    ws["A3"].font=Font(italic=True,color="9C0006"); ws["A3"].alignment=Alignment(wrap_text=True)
    for cell in ws[headerrow]:
        cell.font=Font(bold=True,color="FFFFFF"); cell.fill=PatternFill("solid",fgColor="4472C4"); cell.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
    widths=[17,55,10,12,10,15]+[9]*12+[9,9,13,14,58,34,42]
    for col,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(col)].width=w
    for row in ws.iter_rows(min_row=first,max_row=last):
        for cell in row:
            cell.border=Border(bottom=Side(style="hair",color="B4C6E7"))
            if cell.column in (2,23,24,25): cell.alignment=Alignment(wrap_text=True,vertical="top")
    # Hoja de seguimiento de datos a incorporar cuando existan los generadores aprobados.
    pend=wb.create_sheet("Pendientes")
    pend.append([PROJECT]); pend.append(["Fecha: 23-11-2026","Versión: v01","Responsable: CX-2 (PC-B)"])
    pend.append(["Duraciones actuales = SUPUESTO por capítulo; el calendario reserva enero-diciembre 2027 (12 meses)."])
    pend.append(["Pendiente","Entrada requerida","Cálculo/acción","Estado"])
    tasks=[
      ["Cantidades por clave","generadores_v01.json aprobado","Q total por clave y unidad; conservar fuente Revit/element IDs","Pendiente: T-302/T-303"],
      ["Rendimiento de cuadrilla","APU/recursos de catalogo_v01.json y criterio de cuadrilla","Duración (meses)=Q/(rendimiento de cuadrilla × cuadrillas × jornadas laborales/mes); verificar unidad","SUPUESTO hasta generadores"],
      ["Distribución por niveles","Índice Revit: niveles principales y cantidades por nivel","Calcular avance por nivel/frente y revisar solapes F1-F3","Aprox. 2,500 m²; 4 niveles principales reportados"],
      ["Actualizar duraciones y CPM","Cantidades + rendimientos revisados","Reprogramar en 12 meses; CPM hacia adelante/atrás; holgura=LS-ES; crítica sólo holgura cero","Posterior a generadores"],
      ["Claves definitivas","catalogo_v01.json aprobado","Mantener una actividad por clave; no usar claves 99","Catálogo publicado; pendiente revisión CL-1"],
      ["Importes y flujo financiero","presupuesto_v01.json aprobado y cola T-403 aprobada","Importe por clave; flujo mensual=importe×avance; suma calendario=subtotal presupuesto","No iniciar antes de T-403 aprobado"],
      ["Cierre QA","validar.py calendario + comparación de subtotal","Validar 100% por actividad, 12 meses y total igual a subtotal","Pendiente"],
    ]
    for row in tasks: pend.append(row)
    for cell in pend[4]: cell.font=Font(bold=True,color="FFFFFF"); cell.fill=PatternFill("solid",fgColor="4472C4")
    for col,w in enumerate([34,48,86,38],1): pend.column_dimensions[get_column_letter(col)].width=w
    pend.freeze_panes="A5"; pend.sheet_view.showGridLines=False
    pend.merge_cells("A1:D1"); pend.merge_cells("A3:D3"); pend["A1"].font=Font(size=14,bold=True,color="FFFFFF"); pend["A1"].fill=PatternFill("solid",fgColor="1F4E78"); pend["A3"].alignment=Alignment(wrap_text=True); pend["A3"].font=Font(italic=True,color="9C0006")
    for row in pend.iter_rows(min_row=5):
        for cell in row: cell.alignment=Alignment(wrap_text=True,vertical="top"); cell.border=Border(bottom=Side(style="hair",color="B4C6E7"))
    for sh,area,repeat in ((ws,f"A1:Y{last}","1:4"),(pend,f"A1:D{pend.max_row}","1:4")):
        sh.page_setup.paperSize=sh.PAPERSIZE_LETTER; sh.page_setup.orientation="landscape"; sh.page_setup.fitToWidth=1; sh.page_setup.fitToHeight=0; sh.sheet_properties.pageSetUpPr.fitToPage=True
        sh.print_area=area; sh.print_title_rows=repeat; sh.page_margins.left=sh.page_margins.right=0.35; sh.page_margins.top=sh.page_margins.bottom=0.5
        sh.oddHeader.center.text=PROJECT; sh.oddHeader.right.text="Versión v01 · &D"; sh.oddFooter.left.text="Responsable: CX-2 (PC-B)"; sh.oddFooter.right.text="Página &P de &N"
    XLSX_OUT.parent.mkdir(parents=True,exist_ok=True); tmp=XLSX_OUT.with_name(XLSX_OUT.name+".tmp.xlsx"); wb.save(tmp); wb.close(); tmp.replace(XLSX_OUT)


def main() -> None:
    if not CATALOG.exists(): raise SystemExit(f"Falta catálogo AG-2: {CATALOG}")
    if not INDEX.exists(): raise SystemExit(f"Falta índice Revit: {INDEX}")
    catalog=json.loads(CATALOG.read_text(encoding="utf-8")); idx=json.loads(INDEX.read_text(encoding="utf-8"))
    structure=next((x for x in idx["vinculos"] if x.get("modelo")=="Edificio de educacion"),None)
    if not structure: raise SystemExit("No está vínculo Edificio de educacion en indice.json")
    # Cuatro bandas funcionales del vínculo estructural: +5.30, +8.80, +12.30 y cubierta (+13.80/+14.80 agrupadas); excluir dalas auxiliares.
    level_elevations=[round(float(x["elevacion_m"]),2) for x in structure["niveles"] if "auxiliar" not in x["nombre"].lower()]
    floor_bands=sum(any(abs(e-target)<=0.05 for e in level_elevations) for target in (5.30,8.80,12.30))
    roof_band=any(any(abs(e-target)<=0.05 for e in level_elevations) for target in (13.80,14.80))
    levels_count=floor_bands+int(roof_band)
    if levels_count!=4: raise SystemExit(f"Índice Revit no confirma 4 bandas principales; detectadas {levels_count}: {level_elevations}")
    rows=build_activities(catalog,levels_count)
    compute_cpm(rows)
    for a in rows: a.pop("_holgura_meses",None); a.pop("capitulo"); a.pop("subcapitulo"); a.pop("duracion_meses"); a.pop("justificacion")
    data={"version":"v01","fecha":"23-11-2026","fecha_inicio_obra":"04-01-2027","duracion_meses":12,
          "presupuesto_usado":None,"actividades":rows,"total_importe":None}
    JSON_OUT.parent.mkdir(parents=True,exist_ok=True); jt=JSON_OUT.with_name(JSON_OUT.name+".tmp"); jt.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); jt.replace(JSON_OUT)
    # Build workbook again from full metadata after writing schema-only JSON.
    workbook_rows=build_activities(catalog,levels_count); compute_cpm(workbook_rows); build_workbook(workbook_rows,levels_count)
    print(f"Generadas {len(rows)} actividades; CPM={max(a['mes_fin'] for a in rows)} meses; críticas={sum(a['ruta_critica'] for a in rows)}")

if __name__ == "__main__": main()