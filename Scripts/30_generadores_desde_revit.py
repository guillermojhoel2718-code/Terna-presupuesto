"""
30_generadores_desde_revit.py — Generadores por partida a partir del catálogo (AG-2) y la extracción Revit (AG-1).

Entrada :
  --catalogo   _harness/intermedios/precios/catalogo_vNN.json        (schema precios.CatalogoPrecios)
  --revit-dir  _harness/intermedios/revit/                           (*.json, schema revit.ExtraccionRevit)
  --manual     _harness/intermedios/generadores/manual.json          (opcional; partidas sin Revit, ver abajo)
  --version    vNN
Salida  :
  _harness/intermedios/generadores/generadores_vNN.json  (schema generadores.Generadores, validado)
  _harness/intermedios/generadores/reporte_vNN.md        (claves sin cantidad, elementos sin asignar, duplicados, unidades)
  Generadores/Generadores_vNN.xlsx                        (una hoja por capítulo, bloque por clave, hoja REF_REVIT; Carta horizontal)
Dependencias: py -m pip install -r Scripts/requirements.txt  (pydantic, openpyxl)
Fecha  : 23-11-2026 · Dueño: CL-1 (rol AG-3) · Specs: SPEC_02, SPEC_03 §3, SPEC_07, SPEC_08 §3

Reglas:
- La cantidad de cada clave = Σ de los elementos Revit que cumplen su `mapeo_revit`
  (categoría + regex sobre familia/tipo/material + campo de cantidad × factor). Sin desperdicio.
- Renglones agrupados por (modelo, nivel, tipo); los IDs completos van en el JSON y en REF_REVIT.
- Claves `sin_cantidad_revit` o sin elementos: toman sus renglones de `manual.json` (con fuente
  MEMORIA:p.NN / SUPUESTO:<motivo>); si no hay, quedan en `claves_sin_cantidad`. Nunca se inventan.
- parcial = (largo·ancho·alto·piezas, solo si hay alguna dimensión) + adicion − deduccion.
  La misma fórmula se escribe en Excel para que el usuario pueda editar.
- Idempotente. No sobrescribe salidas existentes sin --force. Escribe a .tmp y renombra (OneDrive).

manual.json:
  {"generadores": [ {Generador completo según schemas/generadores.py}, ... ]}

Uso:
  py Scripts/30_generadores_desde_revit.py --catalogo _harness/intermedios/precios/catalogo_v01.json --version v01
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "Scripts" / "schemas"))

from generadores import Generador, Generadores, RenglonGenerador  # noqa: E402
from precios import CatalogoPrecios  # noqa: E402
from revit import ExtraccionRevit  # noqa: E402

PROYECTO = 'Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"'  # D-010
UBICACION = "Lib. Sur 285, 37904 Misión de Chichimecas, San Luis de la Paz, Gto."
ZONA = "Edificio de educación"  # D-001
CAPITULOS = {  # SPEC_02 §2
    "01": "PRELIMINARES", "02": "CIMENTACIÓN", "03": "ESTRUCTURA DE CONCRETO Y MAMPOSTERÍA",
    "04": "ESTRUCTURA METÁLICA Y CUBIERTA", "05": "ALBAÑILERÍA", "06": "ACABADOS",
    "07": "HERRERÍA Y CANCELERÍA", "08": "INSTALACIÓN HIDRÁULICA Y PLUVIAL", "09": "INSTALACIÓN SANITARIA",
    "10": "INSTALACIÓN ELÉCTRICA Y FOTOVOLTAICA", "11": "VOZ Y DATOS", "12": "CCTV Y SEGURIDAD",
    "13": "MOBILIARIO Y EQUIPAMIENTO FIJO", "14": "LIMPIEZA Y ENTREGA",
}
CAMPO_UNIDAD = {"area_m2": {"m2"}, "volumen_m3": {"m3"}, "longitud_m": {"m"}, "conteo": {"pza", "jgo", "salida"},
                "peso_kg": {"kg", "ton"}}


# ----------------------------------------------------------------------------- utilidades
def hoy() -> str:
    return date.today().strftime("%d-%m-%Y")


def norm_cat(s: str) -> str:
    s = re.sub(r"[^a-z0-9]", "", (s or "").lower())
    s = s[3:] if s.startswith("ost") else s
    return s[:-1] if s.endswith("s") else s


def rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def parcial(r: dict) -> float:
    dims = [r.get(k) for k in ("largo", "ancho", "alto")]
    base = 0.0
    if any(d is not None for d in dims):
        base = 1.0
        for d in dims:
            if d is not None:
                base *= d
        base *= r.get("piezas", 1) or 0
    return base + (r.get("adicion") or 0) - (r.get("deduccion") or 0)


def escribir_atomico(path: Path, data: bytes | str):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    if isinstance(data, str):
        tmp.write_text(data, encoding="utf-8")
    else:
        tmp.write_bytes(data)
    os.replace(tmp, path)


# ----------------------------------------------------------------------------- cálculo
def cargar_revit(revit_dir: Path):
    extracciones = []
    for f in sorted(revit_dir.glob("*.json")):
        if f.name == "indice.json":
            continue
        ex = ExtraccionRevit.model_validate(json.loads(f.read_text(encoding="utf-8")))
        extracciones.append((f, ex))
    return extracciones


def calcular(catalogo: CatalogoPrecios, extracciones, manual: dict[str, Generador]):
    generadores, sin_cantidad, avisos = [], [], []
    asignados: dict[tuple, list[str]] = defaultdict(list)  # (modelo, id, campo) -> claves

    for c in catalogo.conceptos:
        if c.capitulo in ("11", "12"):  # D-016 fuera de alcance
            continue
        grupos: dict[tuple, dict] = {}
        for m in c.mapeo_revit:
            unidades_ok = CAMPO_UNIDAD.get(m.campo_cantidad, set())
            if c.unidad.value not in unidades_ok:
                avisos.append(f"{c.clave}: unidad '{c.unidad.value}' con campo '{m.campo_cantidad}' (revisar factor)")
            rx = re.compile(m.filtro_tipo, re.I) if m.filtro_tipo else None
            for f, ex in extracciones:
                if norm_cat(ex.categoria) != norm_cat(m.categoria):
                    continue
                if m.modelo and m.modelo.lower() not in ex.modelo.lower():
                    continue
                for e in ex.elementos:
                    texto = " | ".join(x for x in (e.familia, e.tipo, e.material_principal) if x)
                    if rx and not rx.search(texto):
                        continue
                    valor = getattr(e.cantidades, m.campo_cantidad)
                    if valor is None:
                        avisos.append(f"{c.clave}: elemento {e.modelo_origen}#{e.element_id} sin {m.campo_cantidad}")
                        continue
                    asignados[(e.modelo_origen, e.element_id, m.campo_cantidad)].append(c.clave)
                    k = (e.modelo_origen, e.nivel or "-", e.tipo or e.familia or "-")
                    g = grupos.setdefault(k, {"adicion": 0.0, "ids": [], "archivo": rel(f)})
                    g["adicion"] += valor * m.factor
                    g["ids"].append(e.element_id)

        if grupos:
            renglones = []
            for (modelo, nivel, tipo), g in sorted(grupos.items()):
                r = {"localizacion": nivel, "descripcion": tipo, "piezas": len(g["ids"]), "adicion": g["adicion"],
                     "deduccion": 0, "modelo_origen": modelo, "element_ids": sorted(g["ids"]),
                     "archivo_intermedio": g["archivo"]}
                # piezas es informativo cuando no hay dimensiones: parcial = adicion
                r["parcial"] = parcial(r)
                renglones.append(RenglonGenerador(**r))
            campos = sorted({m.campo_cantidad for m in c.mapeo_revit})
            generadores.append(Generador(
                clave=c.clave, concepto=c.concepto, unidad=c.unidad,
                formula=f"Σ {', '.join(campos)} de elementos Revit (mapeo_revit)" +
                        ("" if all(m.factor == 1 for m in c.mapeo_revit) else " × factor"),
                renglones=renglones, cantidad_total=sum(r.parcial for r in renglones),
                fuente="REVIT:" + ", ".join(sorted({r.archivo_intermedio for r in renglones}))))
        elif c.clave in manual:
            generadores.append(manual[c.clave])
        else:
            sin_cantidad.append(c.clave)

    duplicados = {k: v for k, v in asignados.items() if len(v) > 1}
    no_asignados = defaultdict(int)
    for f, ex in extracciones:
        for e in ex.elementos:
            if not any((e.modelo_origen, e.element_id, campo) in asignados for campo in CAMPO_UNIDAD):
                no_asignados[(ex.modelo, ex.categoria)] += 1
    return generadores, sin_cantidad, avisos, duplicados, no_asignados


# ----------------------------------------------------------------------------- Excel
def escribir_excel(gens: Generadores, path: Path, catalogo: CatalogoPrecios):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.pagebreak import Break

    cap_de = {c.clave: c.capitulo for c in catalogo.conceptos}
    fino = Side(style="thin", color="808080")
    borde = Border(left=fino, right=fino, top=fino, bottom=fino)
    guinda = PatternFill("solid", fgColor="990033")
    gris = PatternFill("solid", fgColor="E7E6E6")
    blanco_b = Font(bold=True, color="FFFFFF", size=12)
    neg = Font(bold=True)
    centro = Alignment(horizontal="center", vertical="center", wrap_text=True)
    izq = Alignment(horizontal="left", vertical="center", wrap_text=True)
    num = "#,##0.00"
    # A loc | B descripción | C largo | D ancho | E alto | F pzas | G (+) | H (-) | I parcial | J total | K ref revit
    anchos = [16, 34, 9, 9, 9, 8, 12, 10, 12, 13, 34]

    wb = Workbook()
    wb.remove(wb.active)
    por_cap = defaultdict(list)
    for g in gens.generadores:
        por_cap[cap_de.get(g.clave, g.clave[3:5])].append(g)

    for cap in sorted(por_cap):
        ws = wb.create_sheet(f"{cap} {CAPITULOS.get(cap, '')}"[:31])
        for i, w in enumerate(anchos, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
        # Encabezado de hoja (se repite al imprimir)
        ws.merge_cells("A1:K1"); ws["A1"] = "INSTITUTO POLITÉCNICO NACIONAL · ESIA Unidad Tecamachalco"
        ws.merge_cells("A2:K2"); ws["A2"] = PROYECTO
        ws.merge_cells("A3:F3"); ws["A3"] = f"UBICACIÓN: {UBICACION}"
        ws.merge_cells("G3:K3"); ws["G3"] = f"ZONA DE TRABAJO: {ZONA}"
        ws.merge_cells("A4:F4"); ws["A4"] = f"CAPÍTULO {cap}: {CAPITULOS.get(cap, '')}"
        ws.merge_cells("G4:K4"); ws["G4"] = f"FECHA: {gens.fecha} · VERSIÓN: {gens.version} · RESPONSABLE: CL-1"
        for c in ("A1", "A2"):
            ws[c].font = Font(bold=True, size=12); ws[c].alignment = centro
        for c in ("A3", "G3", "A4", "G4"):
            ws[c].font = neg; ws[c].alignment = izq
        fila = 6
        for g in por_cap[cap]:
            inicio = fila
            ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=11)
            ws.cell(fila, 1, "HOJA DE CUANTIFICACIÓN").font = blanco_b
            ws.cell(fila, 1).fill = guinda; ws.cell(fila, 1).alignment = centro
            fila += 1
            ws.cell(fila, 1, "PARTIDA:").font = neg
            ws.merge_cells(start_row=fila, start_column=2, end_row=fila, end_column=5)
            ws.cell(fila, 2, CAPITULOS.get(cap, ""))
            ws.cell(fila, 6, "CLAVE:").font = neg
            ws.merge_cells(start_row=fila, start_column=7, end_row=fila, end_column=8)
            ws.cell(fila, 7, g.clave).font = Font(bold=True, size=12)
            ws.cell(fila, 9, "UNIDAD:").font = neg
            ws.cell(fila, 10, g.unidad.value).font = Font(bold=True, size=12)
            fila += 1
            ws.cell(fila, 1, "CONCEPTO:").font = neg
            ws.cell(fila, 1).alignment = Alignment(vertical="center")
            ws.merge_cells(start_row=fila, start_column=2, end_row=fila, end_column=11)
            ws.cell(fila, 2, g.concepto).alignment = izq
            ws.row_dimensions[fila].height = max(30, 15 * (len(g.concepto) // 110 + 1))
            fila += 1
            heads = ["LOCALIZACIÓN", "DESCRIPCIÓN / TIPO", "LARGO", "ANCHO", "ALTO", "NO. PZAS",
                     "( + ) ÁREA/VOL.", "( - )", "PARCIAL", "TOTAL", "REFERENCIA (modelo · elementos)"]
            for j, h in enumerate(heads, start=1):
                cl = ws.cell(fila, j, h); cl.font = neg; cl.fill = gris; cl.alignment = centro; cl.border = borde
            ws.row_dimensions[fila].height = 28
            fila += 1
            primera = fila
            for r in g.renglones:
                vals = [r.localizacion, r.descripcion, r.largo, r.ancho, r.alto, r.piezas, r.adicion, r.deduccion]
                for j, v in enumerate(vals, start=1):
                    cl = ws.cell(fila, j, v); cl.border = borde
                    cl.alignment = izq if j <= 2 else centro
                    if 3 <= j <= 8:
                        cl.number_format = "#,##0" if j == 6 else num
                f = (f"=IF(COUNT(C{fila}:E{fila})=0,0,PRODUCT(C{fila}:E{fila})*F{fila})+G{fila}-H{fila}")
                for j, v in ((9, f), (10, f"=I{fila}")):
                    cl = ws.cell(fila, j, v)
                    cl.number_format = num
                    cl.alignment = Alignment(horizontal="right", vertical="center")
                ids = r.element_ids
                ref = r.modelo_origen or ""
                if ids:
                    muestra = ", ".join(map(str, ids[:4])) + (" …" if len(ids) > 4 else "")
                    ref = f"{ref} · {len(ids)} elem. · IDs {muestra}"
                ws.cell(fila, 11, ref or g.fuente).alignment = izq
                for j in (9, 10, 11):
                    ws.cell(fila, j).border = borde
                fila += 1
            ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=8)
            ws.cell(fila, 1, f"TOTAL {g.clave} ({g.unidad.value})").font = neg
            ws.cell(fila, 1).alignment = Alignment(horizontal="right")
            ws.cell(fila, 10, f"=SUM(J{primera}:J{fila-1})").number_format = num
            ws.cell(fila, 10).font = neg; ws.cell(fila, 10).border = borde
            ws.cell(fila, 11, f"Fórmula: {g.formula}").alignment = izq
            fila += 1
            ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=11)
            ws.cell(fila, 1, f"Fuente: {g.fuente}").font = Font(italic=True, size=8)
            fila += 1
            for j, t in ((1, "ELABORÓ: CL-1"), (5, "REVISÓ:"), (9, "RECIBE:")):
                ws.cell(fila, j, t).font = Font(size=9)
            fila += 2
            if fila - inicio > 40:  # bloque largo: empezar el siguiente en página nueva
                ws.row_breaks.append(Break(id=fila - 1))

        configurar_impresion(ws, fila - 1, "K", gens.version, gens.fecha)

    # Hoja de trazabilidad completa
    ws = wb.create_sheet("REF_REVIT")
    cab = ["clave", "modelo_origen", "element_id", "localización", "tipo", "archivo_intermedio"]
    ws.append(cab)
    for c in ws[1]:
        c.font = neg; c.fill = gris
    for g in gens.generadores:
        for r in g.renglones:
            for i in r.element_ids:
                ws.append([g.clave, r.modelo_origen, i, r.localizacion, r.descripcion, r.archivo_intermedio])
    for col, w in zip("ABCDEF", (16, 40, 12, 16, 40, 50)):
        ws.column_dimensions[col].width = w
    configurar_impresion(ws, ws.max_row, "F", gens.version, gens.fecha)

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp.xlsx")
    wb.save(tmp)
    os.replace(tmp, path)


def configurar_impresion(ws, ultima_fila: int, ultima_col: str, version: str, fecha: str):
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER  # D-006
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = f"A1:{ultima_col}{max(ultima_fila, 1)}"
    if ws.title != "REF_REVIT":
        ws.print_title_rows = "1:4"
    else:
        ws.print_title_rows = "1:1"
    ws.page_margins.left = ws.page_margins.right = 0.4
    ws.page_margins.top = 0.75
    ws.page_margins.bottom = 0.6
    ws.page_margins.header = 0.25
    ws.page_margins.footer = 0.25
    # Proyecto, fecha, versión y responsable ya van en las filas 1-4 (títulos repetidos);
    # el encabezado de página solo lleva la referencia corta para no encimarse.
    ws.oddHeader.right.text = f"Generadores {version} · {fecha}"
    ws.oddFooter.left.text = f"{PROYECTO} · Responsable: CL-1"
    ws.oddFooter.right.text = "Página &P de &N"


# ----------------------------------------------------------------------------- reporte
def reporte(version, catalogo_path, sin_cantidad, avisos, duplicados, no_asignados, gens) -> str:
    l = [f"# Reporte de generadores {version} · {hoy()}", "",
         f"Catálogo: `{catalogo_path}` · Generadores: {len(gens.generadores)} · Sin cantidad: {len(sin_cantidad)}", ""]
    l += ["## Claves sin cantidad (ni Revit ni manual.json)", ""] + ([f"- {c}" for c in sin_cantidad] or ["- ninguna"])
    l += ["", "## Elementos asignados a más de una clave con el mismo campo (posible doble conteo)", ""]
    l += [f"- {m}#{i} ({campo}) → {', '.join(cl)}" for (m, i, campo), cl in list(duplicados.items())[:200]] or ["- ninguno"]
    l += ["", "## Elementos Revit sin asignar a ninguna clave", "", "| Modelo | Categoría | Elementos |", "|---|---|---|"]
    l += [f"| {m} | {c} | {n} |" for (m, c), n in sorted(no_asignados.items())] or ["| — | — | 0 |"]
    l += ["", "## Avisos", ""] + ([f"- {a}" for a in avisos[:300]] or ["- ninguno"])
    return "\n".join(l) + "\n"


# ----------------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--catalogo", required=True)
    ap.add_argument("--revit-dir", default=str(ROOT / "_harness/intermedios/revit"))
    ap.add_argument("--manual", default=str(ROOT / "_harness/intermedios/generadores/manual.json"))
    ap.add_argument("--version", required=True)
    ap.add_argument("--out-dir", default=str(ROOT / "_harness/intermedios/generadores"))
    ap.add_argument("--xlsx-dir", default=str(ROOT / "Generadores"))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    if not re.fullmatch(r"v\d{2}", a.version):
        ap.error("--version debe ser vNN")

    cat_path = Path(a.catalogo)
    catalogo = CatalogoPrecios.model_validate(json.loads(cat_path.read_text(encoding="utf-8")))
    extracciones = cargar_revit(Path(a.revit_dir)) if Path(a.revit_dir).exists() else []
    manual = {}
    if Path(a.manual).exists():
        for g in json.loads(Path(a.manual).read_text(encoding="utf-8")).get("generadores", []):
            gm = Generador.model_validate(g)
            manual[gm.clave] = gm

    out_json = Path(a.out_dir) / f"generadores_{a.version}.json"
    out_md = Path(a.out_dir) / f"reporte_{a.version}.md"
    out_xlsx = Path(a.xlsx_dir) / f"Generadores_{a.version}.xlsx"
    for p in (out_json, out_xlsx):
        if p.exists() and not a.force:
            print(f"Ya existe {p}. Usa --force para regenerarlo (nunca sobre una versión aprobada).", file=sys.stderr)
            return 1

    gens_l, sin_cantidad, avisos, duplicados, no_asignados = calcular(catalogo, extracciones, manual)
    gens = Generadores(version=a.version, fecha=hoy(), catalogo_usado=rel(cat_path),
                       generadores=gens_l, claves_sin_cantidad=sin_cantidad)
    Generadores.model_validate(json.loads(gens.model_dump_json()))  # validación de ida y vuelta

    escribir_atomico(out_json, gens.model_dump_json(indent=2))
    escribir_atomico(out_md, reporte(a.version, rel(cat_path), sin_cantidad, avisos, duplicados, no_asignados, gens))
    escribir_excel(gens, out_xlsx, catalogo)
    print(f"OK {len(gens_l)} generadores · {len(sin_cantidad)} sin cantidad · {len(duplicados)} duplicados")
    print(f"   {rel(out_json)}\n   {rel(out_md)}\n   {rel(out_xlsx)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
