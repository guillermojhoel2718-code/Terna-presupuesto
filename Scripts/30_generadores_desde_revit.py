"""
30_generadores_desde_revit.py — Generadores por partida desde Revit + cantidades derivadas (CL-1 en rol AG-3).

Entrada : _harness/intermedios/revit/<modelo>__<categoria>.json  (AG-1)
          _harness/intermedios/revit/resumen_por_categoria_y_nivel.json  (16 cantidades derivadas)
          _harness/intermedios/precios/catalogo_v01.json  (si existe; respaldo: Scripts/21 y 22 de AG-2)
          _harness/intermedios/generadores/manual.json  (opcional; sobreescribe cantidades derivadas)
Salida  : _harness/intermedios/generadores/generadores_<ver>.json  (valida con Scripts/schemas/generadores.py)
          Generadores/Generadores_<ver>.xlsx  (Carta horizontal, 1 pág. de ancho, SPEC_07)
Uso     : python Scripts/30_generadores_desde_revit.py [v02]
Depende : openpyxl, pydantic>=2
Fecha   : 26-11-2026
Notas   : - Idempotente; usa las 65 claves oficiales ED-CC-SS-NNN del catálogo de AG-2.
          - Aplica mapeo_revit (modelo, categoría, regex filtro_tipo, campo_cantidad, factor).
          - Integra las 16 cantidades derivadas de resumen_por_categoria_y_nivel.json para conceptos sin Revit.
          - Sin desperdicios en cantidad (SPEC_03 §3).
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "Scripts" / "schemas"
if str(SCHEMAS_DIR) not in sys.path:
    sys.path.insert(0, str(SCHEMAS_DIR))

from common import normalizar_unidad  # noqa: E402

REVIT = ROOT / "_harness" / "intermedios" / "revit"
RESUMEN_REVIT = REVIT / "resumen_por_categoria_y_nivel.json"
CATALOGO = ROOT / "_harness" / "intermedios" / "precios" / "catalogo_v01.json"
MANUAL = ROOT / "_harness" / "intermedios" / "generadores" / "manual.json"
VER = sys.argv[1] if len(sys.argv) > 1 else "v02"
FECHA = "26-11-2026"
PROYECTO = 'Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"'
UBICACION = "San Luis de la Paz, Guanajuato"
RESP = "CL-1 (rol AG-3)"

CAPITULOS = OrderedDict([
    ("01", ("PRE", "PRELIMINARES")),
    ("02", ("CIM", "CIMENTACIÓN")),
    ("03", ("EST", "ESTRUCTURA DE CONCRETO Y MAMPOSTERÍA CONFINADA")),
    ("04", ("MET", "ESTRUCTURA METÁLICA Y CUBIERTA")),
    ("05", ("ALB", "ALBAÑILERÍA")),
    ("06", ("ACA", "ACABADOS")),
    ("07", ("CAN", "HERRERÍA Y CANCELERÍA")),
    ("08", ("IHP", "INSTALACIÓN HIDRÁULICA Y PLUVIAL")),
    ("09", ("ISA", "INSTALACIÓN SANITARIA")),
    ("10", ("IEL", "INSTALACIÓN ELÉCTRICA Y FOTOVOLTAICA")),
    ("13", ("MOB", "MOBILIARIO Y EQUIPAMIENTO FIJO")),
    ("14", ("LIM", "LIMPIEZA FINAL Y ENTREGA")),
])

CAMPO_TXT = {
    "conteo": "Σ piezas",
    "longitud_m": "Σ longitud_m",
    "area_m2": "Σ area_m2",
    "volumen_m3": "Σ volumen_m3",
    "peso_kg": "Σ peso_kg",
}

CAT_ALIAS = {
    "Cable Trays": "CableTrays",
    "Cable Tray Fittings": "CableTrayFittings",
    "Conduit Fittings": "ConduitFittings",
    "Curtain Wall Mullions": "CurtainWallMullions",
    "Curtain Wall Panels": "CurtainWallPanels",
    "Electrical Equipment": "ElectricalEquipment",
    "Electrical Fixtures": "ElectricalFixtures",
    "Fire Alarm Devices": "FireAlarmDevices",
    "Flex Pipes": "FlexPipes",
    "Furniture Systems": "FurnitureSystems",
    "Generic Models": "GenericModel",
    "Lighting Devices": "LightingDevices",
    "Lighting Fixtures": "LightingFixtures",
    "Mechanical Equipment": "MechanicalEquipment",
    "Pipe Accessories": "PipeAccessories",
    "Pipe Fittings": "PipeFittings",
    "Plumbing Fixtures": "PlumbingFixtures",
    "Security Devices": "SecurityDevices",
    "Specialty Equipment": "SpecialtyEquipment",
    "Structural Columns": "StructuralColumns",
    "Structural Foundations": "StructuralFoundations",
    "Structural Framing": "StructuralFraming",
    "Communication Devices": "CommunicationDevices",
    "Data Devices": "DataDevices",
}

_revit_cache: dict[str, list[dict]] = {}


def _cargar_modulo(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {ruta}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cargar_catalogo() -> tuple[list[dict], str]:
    if CATALOGO.exists():
        d = json.loads(CATALOGO.read_text(encoding="utf-8"))
        return d.get("conceptos", []), "catalogo_v01.json"
    m1 = _cargar_modulo("cap01_06", ROOT / "Scripts" / "21_catalogo_cap01_06.py")
    m2 = _cargar_modulo("cap07_14", ROOT / "Scripts" / "22_catalogo_cap07_14.py")
    return list(m1.CAPITULOS_01_06) + list(m2.CAPITULOS_07_14), "catalogo_v01 (Scripts/21+22 AG-2)"


def cargar_derivadas() -> dict[str, dict]:
    deriv: dict[str, dict] = {}
    if RESUMEN_REVIT.exists():
        d = json.loads(RESUMEN_REVIT.read_text(encoding="utf-8"))
        for item in d.get("cantidades_derivadas_para_manual_json", []):
            deriv[item["clave"]] = item
    if MANUAL.exists():
        m = json.loads(MANUAL.read_text(encoding="utf-8"))
        items = m if isinstance(m, list) else m.get("manual", m.get("conceptos", []))
        for item in items:
            if isinstance(item, dict) and "clave" in item:
                deriv[item["clave"]] = item
    return deriv


def normalizar_categoria(cat: str) -> str:
    return CAT_ALIAS.get(cat, cat.replace(" ", ""))


def cargar_revit_archivos(modelo: str | None, categoria: str) -> list[tuple[str, list[dict]]]:
    cat_norm = normalizar_categoria(categoria)
    if modelo:
        archivos = [REVIT / f"{modelo}__{cat_norm}.json"]
    else:
        archivos = sorted(REVIT.glob(f"*__{cat_norm}.json"))
    res = []
    for p in archivos:
        if not p.exists():
            continue
        fn = p.name
        if fn not in _revit_cache:
            _revit_cache[fn] = json.loads(p.read_text(encoding="utf-8")).get("elementos", [])
        res.append((fn, _revit_cache[fn]))
    return res


def num(v) -> float:
    return float(v) if isinstance(v, (int, float)) else 0.0


def construir():
    conceptos, cat_label = cargar_catalogo()
    derivadas = cargar_derivadas()
    gens = []
    claves_sin_cantidad = []
    asignados: dict[tuple[str, int], list[str]] = {}
    avisos_null = 0

    for c in conceptos:
        clave = c["clave"]
        concepto = c.get("concepto") or c.get("descripcion") or ""
        unidad = normalizar_unidad(str(c["unidad"]))
        mapeos = c.get("mapeo_revit") or []
        grupos: "OrderedDict[tuple, dict]" = OrderedDict()
        campos_usados: list[str] = []
        factores_usados: list[float] = []

        for m in mapeos:
            modelo = m.get("modelo")
            cat = m["categoria"]
            regex_txt = m.get("filtro_tipo") or ".*"
            campo = m["campo_cantidad"]
            factor = float(m.get("factor", 1.0))
            pat = re.compile(regex_txt, re.IGNORECASE)
            campos_usados.append(campo)
            factores_usados.append(factor)

            for fn, elems in cargar_revit_archivos(modelo, cat):
                for e in elems:
                    haystack = f"{e.get('familia') or ''} | {e.get('tipo') or ''} | {e.get('material_principal') or ''}"
                    if not pat.search(haystack):
                        continue
                    cant = e.get("cantidades") or {}
                    val = cant.get(campo)
                    if val is None:
                        if campo == "conteo":
                            val = 1
                        else:
                            avisos_null += 1
                            val = 0.0
                    parcial_e = float(val) * factor
                    eid = int(e["element_id"])
                    asignados.setdefault((fn, eid), []).append(clave)
                    k = (fn, e.get("nivel") or "Sin nivel", f"{e.get('familia') or ''} : {e.get('tipo') or ''}", factor, campo)
                    g = grupos.setdefault(k, {
                        "conteo": 0, "longitud_m": 0.0, "area_m2": 0.0,
                        "volumen_m3": 0.0, "peso_kg": 0.0, "parcial": 0.0,
                        "ids": [], "modelo": e.get("modelo_origen") or (modelo or fn.split("__")[0]),
                    })
                    g["conteo"] += int(cant.get("conteo") or 1)
                    for f in ("longitud_m", "area_m2", "volumen_m3", "peso_kg"):
                        g[f] += num(cant.get(f))
                    g["parcial"] += parcial_e
                    g["ids"].append(eid)

        renglones = []
        nota = ""
        campo_princ = campos_usados[0] if campos_usados else "manual"

        if grupos:
            for (fn, nivel, desc, factor, campo), g in sorted(grupos.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
                renglones.append({
                    "localizacion": nivel,
                    "descripcion": desc,
                    "piezas": g["conteo"],
                    "largo": round(g["longitud_m"], 6) or None,
                    "area": g["area_m2"],
                    "volumen": g["volumen_m3"],
                    "peso": g["peso_kg"],
                    "factor": factor,
                    "campo": campo,
                    "parcial": g["parcial"],
                    "modelo_origen": g["modelo"],
                    "element_ids": g["ids"],
                    "archivo_intermedio": fn,
                })
            archivos_u = sorted({r["archivo_intermedio"] for r in renglones})
            fuente = "REVIT:" + ", ".join(archivos_u)
            f_txt = CAMPO_TXT.get(campo_princ, campo_princ)
            if any(abs(f - 1.0) > 1e-9 for f in factores_usados):
                f_txt += f" × factor ({factores_usados[0]:g})"
            formula = f"{f_txt} ({unidad}) de elementos Revit mapeados"
        elif clave in derivadas:
            dv = derivadas[clave]
            cant_d = float(dv["cantidad_sugerida"])
            crit = dv.get("criterio_revit", "Cantidad derivada de geometría Revit")
            nota = crit
            es_memoria = "MEMORIA" in crit.upper()
            es_supuesto = crit.upper().startswith("SUPUESTO")
            fuente = f"MEMORIA:{crit}" if es_memoria else (f"SUPUESTO:{crit}" if es_supuesto else f"REVIT:resumen_por_categoria_y_nivel.json ({crit})")
            formula = f"Derivado de geometría Revit ({unidad})" if not (es_memoria or es_supuesto) else crit
            renglones.append({
                "localizacion": "Proyecto general",
                "descripcion": crit,
                "piezas": 1,
                "largo": None,
                "area": cant_d if unidad == "m2" else 0.0,
                "volumen": cant_d if unidad == "m3" else 0.0,
                "peso": cant_d if unidad == "kg" else 0.0,
                "factor": 1.0,
                "campo": "manual",
                "parcial": cant_d,
                "modelo_origen": "Derivado Revit (resumen_por_categoria_y_nivel.json)",
                "element_ids": [],
                "archivo_intermedio": "resumen_por_categoria_y_nivel.json",
            })
        else:
            claves_sin_cantidad.append(clave)
            nota = "Pendiente P-010: sub-vínculo 'Bloque de baños_vinculo.rvt' Unloaded en Instalaciones.rvt"
            fuente = "SUPUESTO:P-010 sub-vínculo Bloque de baños_vinculo.rvt Unloaded en Revit"
            formula = "Pendiente de carga de sub-vínculo (P-010)"
            renglones.append({
                "localizacion": "Núcleo de baños (P-010)",
                "descripcion": nota,
                "piezas": 0,
                "largo": None,
                "area": 0.0,
                "volumen": 0.0,
                "peso": 0.0,
                "factor": 1.0,
                "campo": "manual",
                "parcial": 0.0,
                "modelo_origen": "Instalaciones.rvt (sub-vínculo Unloaded)",
                "element_ids": [],
                "archivo_intermedio": "Instalaciones__PlumbingFixtures.json",
            })

        total = sum(r["parcial"] for r in renglones)
        gens.append({
            "clave": clave,
            "concepto": concepto,
            "unidad": unidad,
            "campo": campo_princ,
            "formula": formula,
            "nota": nota,
            "renglones": renglones,
            "cantidad_total": total,
            "fuente": fuente,
        })

    duplicados = {k: v for k, v in asignados.items() if len(set(v)) > 1}
    return gens, claves_sin_cantidad, cat_label, len(duplicados), avisos_null


def guardar_json(gens, claves_sin_cantidad, cat_label):
    out = {
        "version": VER,
        "fecha": FECHA,
        "catalogo_usado": cat_label,
        "generadores": [
            {
                "clave": g["clave"],
                "concepto": g["concepto"],
                "unidad": g["unidad"],
                "formula": g["formula"],
                "cantidad_total": g["cantidad_total"],
                "fuente": g["fuente"],
                "renglones": [
                    {
                        "localizacion": r["localizacion"],
                        "descripcion": r["descripcion"],
                        "piezas": r["piezas"],
                        "largo": r["largo"],
                        "parcial": r["parcial"],
                        "modelo_origen": r["modelo_origen"],
                        "element_ids": r["element_ids"],
                        "archivo_intermedio": r["archivo_intermedio"],
                    }
                    for r in g["renglones"]
                ],
            }
            for g in gens
        ],
        "claves_sin_cantidad": claves_sin_cantidad,
    }
    d = ROOT / "_harness" / "intermedios" / "generadores"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"generadores_{VER}.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


# ----------------------------------------------------------------------------------------------
F = "Arial"
THIN = Side(style="thin", color="808080")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HDR_FILL = PatternFill("solid", fgColor="1F3864")
BLK_FILL = PatternFill("solid", fgColor="D9E1F2")
TOT_FILL = PatternFill("solid", fgColor="F2F2F2")
COLS = [
    ("LOCALIZACIÓN / NIVEL", 18),
    ("DESCRIPCIÓN (FAMILIA : TIPO / CRITERIO)", 46),
    ("UNIDAD", 7),
    ("PZAS", 7),
    ("LARGO (m)", 10),
    ("ÁREA (m²)", 10),
    ("VOLUMEN (m³)", 10),
    ("PESO (kg)", 10),
    ("PARCIAL", 12),
    ("REFERENCIA REVIT / FUENTE", 46),
]
NC = len(COLS)
CAMPO_COL = {"conteo": "D", "longitud_m": "E", "area_m2": "F", "volumen_m3": "G", "peso_kg": "H"}


def config_impresion(ws, ultima, fila_tit, horizontal=True):
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.orientation = "landscape" if horizontal else "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = f"A1:{get_column_letter(ws.max_column)}{ultima}"
    ws.print_title_rows = f"1:{fila_tit}"
    ws.page_margins.left = ws.page_margins.right = 0.4
    ws.page_margins.top = ws.page_margins.bottom = 0.75
    ws.page_margins.header = ws.page_margins.footer = 0.3
    ws.print_options.horizontalCentered = True
    ws.oddHeader.center.text = PROYECTO
    ws.oddHeader.center.size = 8
    ws.oddHeader.right.text = f"Generadores {VER} · {FECHA}"
    ws.oddHeader.right.size = 8
    ws.oddFooter.left.text = f"Responsable: {RESP}"
    ws.oddFooter.left.size = 8
    ws.oddFooter.right.text = "Página &P de &N"
    ws.oddFooter.right.size = 8


def encabezado(ws, subtitulo, ncols):
    last = get_column_letter(ncols)
    filas = [
        ("NÚMEROS GENERADORES", 12, True),
        (f"OBRA: {PROYECTO}", 9, True),
        (f"UBICACIÓN: {UBICACION}", 8, False),
        (subtitulo, 9, True),
        (f"FECHA: {FECHA}    VERSIÓN: {VER}    ELABORÓ: {RESP}    FUENTE: Modelo federado Revit 2027 + resumen_por_categoria_y_nivel.json", 8, False),
    ]
    for i, (txt, sz, b) in enumerate(filas, start=1):
        ws.merge_cells(f"A{i}:{last}{i}")
        c = ws[f"A{i}"]
        c.value = txt
        c.font = Font(name=F, size=sz, bold=b, color="1F3864" if i == 1 else "000000")
        c.alignment = Alignment(horizontal="center" if i in (1, 2) else "left", vertical="center")
    return 6


def fila_cols(ws, r, cols):
    for j, (n, w) in enumerate(cols, start=1):
        c = ws.cell(r, j, n)
        c.font = Font(name=F, size=8, bold=True, color="FFFFFF")
        c.fill = HDR_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BOX
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[r].height = 24


def ref_txt(r):
    ids = r["element_ids"]
    if not ids:
        return f"{r['modelo_origen']} ({r['archivo_intermedio']})"
    s = ", ".join(str(i) for i in ids[:8])
    if len(ids) > 8:
        s += f" … (+{len(ids) - 8}, ver REF_REVIT)"
    return f"{r['modelo_origen']} · {s}"


def escribir_excel(gens):
    wb = Workbook()
    res = wb.active
    res.title = "RESUMEN"
    hojas = {}
    total_cell = {}
    for cc, (abr, nombre) in CAPITULOS.items():
        ws = wb.create_sheet(f"{cc} {abr}")
        hojas[cc] = ws
        encabezado(ws, f"CAPÍTULO {cc} · {nombre}", NC)
        fila_cols(ws, 7, COLS)
        ws.freeze_panes = "A8"
        ws._r = 8

    for g in gens:
        cc = g["clave"][3:5]
        ws = hojas[cc]
        r = ws._r
        ws.cell(r, 1, g["clave"])
        ws.cell(r, 2, g["concepto"])
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=8)
        ws.cell(r, 9, g["unidad"])
        ws.cell(r, 10, f"Fórmula: {g['formula']}")
        for j in range(1, NC + 1):
            c = ws.cell(r, j)
            c.fill = BLK_FILL
            c.font = Font(name=F, size=8, bold=True)
            c.border = BOX
            c.alignment = Alignment(vertical="center", wrap_text=True, horizontal="center" if j == 9 else "left")
        ws.row_dimensions[r].height = 26 if len(g["concepto"]) > 75 else 15
        r += 1
        r0 = r
        for rr in g["renglones"]:
            if rr["campo"] in CAMPO_COL:
                col_ref = f"{CAMPO_COL[rr['campo']]}{r}"
                parcial_expr = f"={col_ref}*{rr['factor']}" if abs(rr["factor"] - 1.0) > 1e-9 else f"={col_ref}"
            else:
                parcial_expr = rr["parcial"]
            vals = [
                rr["localizacion"],
                rr["descripcion"],
                g["unidad"],
                rr["piezas"],
                rr["largo"] or None,
                rr["area"] or None,
                rr["volumen"] or None,
                rr["peso"] or None,
                parcial_expr,
                ref_txt(rr),
            ]
            for j, v in enumerate(vals, start=1):
                c = ws.cell(r, j, v)
                c.font = Font(name=F, size=7 if j in (2, 10) else 8)
                c.border = BOX
                c.alignment = Alignment(vertical="top", wrap_text=j in (1, 2, 10), horizontal="center" if j == 3 else None)
                if j == 4:
                    c.number_format = "#,##0"
                elif 5 <= j <= 9:
                    c.number_format = "#,##0.00"
            r += 1
        ws.cell(r, 2, f"TOTAL {g['clave']}" + (f"   ·   {g['nota']}" if g["nota"] else ""))
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
        ws.cell(r, 8, g["unidad"])
        ws.cell(r, 9, f"=SUM(I{r0}:I{r - 1})")
        ws.cell(r, 10, g["fuente"])
        for j in range(1, NC + 1):
            c = ws.cell(r, j)
            c.fill = TOT_FILL
            c.border = BOX
            c.font = Font(name=F, size=7 if j in (2, 10) else 8, bold=j in (8, 9))
            c.alignment = Alignment(wrap_text=j in (2, 10), vertical="center", horizontal="right" if j == 8 else None)
        ws.cell(r, 9).number_format = "#,##0.00"
        total_cell[g["clave"]] = f"='{ws.title}'!I{r}"
        ws._r = r + 2

    for ws in hojas.values():
        config_impresion(ws, ws._r - 1, 7)

    rcols = [("CLAVE", 14), ("CONCEPTO", 62), ("UNIDAD", 8), ("CANTIDAD", 13), ("HOJA", 9), ("FUENTE", 52)]
    encabezado(res, "RESUMEN DE CANTIDADES POR PARTIDA (65 CONCEPTOS)", len(rcols))
    fila_cols(res, 7, rcols)
    res.freeze_panes = "A8"
    r = 8
    for cc, (abr, nombre) in CAPITULOS.items():
        res.cell(r, 1, cc)
        res.cell(r, 2, nombre)
        for j in range(1, len(rcols) + 1):
            c = res.cell(r, j)
            c.font = Font(name=F, size=8, bold=True)
            c.fill = BLK_FILL
            c.border = BOX
        r += 1
        for g in [x for x in gens if x["clave"][3:5] == cc]:
            vals = [g["clave"], g["concepto"], g["unidad"], total_cell[g["clave"]], f"{cc} {abr}", g["fuente"]]
            for j, v in enumerate(vals, start=1):
                c = res.cell(r, j, v)
                c.font = Font(name=F, size=7 if j in (2, 6) else 8)
                c.border = BOX
                c.alignment = Alignment(wrap_text=j in (2, 6), vertical="top", horizontal="center" if j in (3, 5) else None)
            res.cell(r, 4).number_format = "#,##0.00"
            r += 1
    config_impresion(res, r - 1, 7, horizontal=False)

    ws = wb.create_sheet("REF_REVIT")
    fcols = [("CLAVE", 14), ("ARCHIVO INTERMEDIO", 44), ("MODELO", 32), ("NIVEL", 22), ("FAMILIA : TIPO", 60), ("ELEMENT_ID", 12)]
    encabezado(ws, "REFERENCIA COMPLETA DE ELEMENTOS REVIT POR PARTIDA", len(fcols))
    fila_cols(ws, 7, fcols)
    ws.freeze_panes = "A8"
    r = 8
    for g in gens:
        for rr in g["renglones"]:
            for eid in rr["element_ids"]:
                for j, v in enumerate([g["clave"], rr["archivo_intermedio"], rr["modelo_origen"], rr["localizacion"], rr["descripcion"], eid], start=1):
                    ws.cell(r, j, v).font = Font(name=F, size=7)
                r += 1
    config_impresion(ws, r - 1, 7, horizontal=False)

    out = ROOT / "Generadores" / f"Generadores_{VER}.xlsx"
    out.parent.mkdir(exist_ok=True)
    wb.save(out)
    return out


if __name__ == "__main__":
    gens, sin_cant, cat_label, n_dup, n_null = construir()
    pj = guardar_json(gens, sin_cant, cat_label)
    px = escribir_excel(gens)
    print(f"OK {len(gens)} partidas | catalogo={cat_label} | duplicados={n_dup} | avisos_null={n_null} | sin_cantidad={sin_cant}")
    print(pj)
    print(px)
    for g in gens:
        print(f"  {g['clave']} {g['cantidad_total']:12.2f} {g['unidad']:6s} {len(g['renglones']):3d} renglones")
