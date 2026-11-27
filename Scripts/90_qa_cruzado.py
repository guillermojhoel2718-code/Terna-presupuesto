"""
90_qa_cruzado.py — QA cruzado de Generadores, Presupuesto y Calendario (CL-1, T-902).

Entrada : _harness/intermedios/generadores/generadores_vNN.json
          _harness/intermedios/presupuesto/presupuesto_vNN.json
          _harness/intermedios/calendario/calendario_vNN.json
          Generadores/Generadores_vNN.xlsx
          Presupuesto/Presupuesto_vNN.xlsm
          Calendario/Calendario_vNN.xlsx
Salida  : Código 0 si todas las verificaciones pasan; código 1 con detalle de hallazgos si falla.
Uso     : python Scripts/90_qa_cruzado.py [--gen v02] [--pto v01] [--cal v02]
Depende : openpyxl, pydantic>=2
Fecha   : 26-11-2026
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "Scripts" / "schemas"
if str(SCHEMAS_DIR) not in sys.path:
    sys.path.insert(0, str(SCHEMAS_DIR))

from calendario import Calendario  # noqa: E402
from generadores import Generadores  # noqa: E402
from presupuesto import Presupuesto  # noqa: E402

TOL_CANT = 1e-3
TOL_MNY = 0.05


def cargar_json(ruta: Path, modelo):
    if not ruta.exists():
        return None, f"No existe {ruta}"
    try:
        raw = json.loads(ruta.read_text(encoding="utf-8"))
        return modelo.model_validate(raw), None
    except Exception as exc:
        return None, f"Error de schema en {ruta.name}: {exc}"


def revisar_impresion(ruta: Path) -> list[str]:
    errs: list[str] = []
    if not ruta.exists():
        return [f"No existe libro Excel: {ruta}"]
    wb = openpyxl.load_workbook(ruta, read_only=False, keep_vba=ruta.suffix.lower() == ".xlsm")
    try:
        for ws in wb.worksheets:
            ps = ws.page_setup.paperSize
            if str(ps) != str(ws.PAPERSIZE_LETTER):
                errs.append(f"{ruta.name} [{ws.title}]: paperSize={ps} (esperado 1=Carta)")
            if ws.page_setup.fitToWidth != 1:
                errs.append(f"{ruta.name} [{ws.title}]: fitToWidth={ws.page_setup.fitToWidth} (esperado 1)")
    finally:
        wb.close()
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", default="v02")
    ap.add_argument("--pto", default="v01")
    ap.add_argument("--cal", default="v02")
    args = ap.parse_args()

    p_gen = ROOT / "_harness" / "intermedios" / "generadores" / f"generadores_{args.gen}.json"
    p_pto = ROOT / "_harness" / "intermedios" / "presupuesto" / f"presupuesto_{args.pto}.json"
    p_cal = ROOT / "_harness" / "intermedios" / "calendario" / f"calendario_{args.cal}.json"

    errores: list[str] = []
    gen, e = cargar_json(p_gen, Generadores)
    if e:
        errores.append(e)
    pto, e = cargar_json(p_pto, Presupuesto)
    if e:
        errores.append(e)
    cal, e = cargar_json(p_cal, Calendario)
    if e:
        errores.append(e)

    if gen and pto:
        g_map = {g.clave: g.cantidad_total for g in gen.generadores}
        for r in pto.partidas:
            if not (r.fuente and r.fuente.strip()):
                errores.append(f"Presupuesto {r.clave}: falta fuente")
            if r.clave not in g_map:
                errores.append(f"Presupuesto {r.clave}: no existe en {p_gen.name}")
            elif abs(g_map[r.clave] - r.cantidad) > max(TOL_CANT, abs(r.cantidad) * 1e-6):
                errores.append(f"{r.clave}: cantidad Generadores ({g_map[r.clave]:.4f}) != Presupuesto ({r.cantidad:.4f})")
        suma_pto = sum(r.importe for r in pto.partidas)
        if abs(suma_pto - pto.subtotal) > TOL_MNY:
            errores.append(f"Presupuesto: Σ importes ({suma_pto:,.2f}) != subtotal ({pto.subtotal:,.2f})")

    if pto and cal:
        for act in cal.actividades:
            s_pct = sum(act.avance_mensual_pct)
            if abs(s_pct - 100.0) > 1e-3:
                errores.append(f"Calendario {act.clave}: suma avance {s_pct:.2f}% != 100%")
        if cal.total_importe is None:
            errores.append("Calendario: total_importe es null (aún sin importes de Presupuesto)")
        elif abs(cal.total_importe - pto.subtotal) > TOL_MNY:
            errores.append(f"Calendario total_importe ({cal.total_importe:,.2f}) != Presupuesto subtotal ({pto.subtotal:,.2f})")

    for xlsx in (
        ROOT / "Generadores" / f"Generadores_{args.gen}.xlsx",
        ROOT / "Presupuesto" / f"Presupuesto_{args.pto}.xlsm",
        ROOT / "Calendario" / f"Calendario_{args.cal}.xlsx",
    ):
        errores.extend(revisar_impresion(xlsx))

    if errores:
        print(f"QA CRUZADO: {len(errores)} hallazgo(s):")
        for item in errores:
            print(f"  - {item}")
        return 1

    print("QA CRUZADO OK: Generadores, Presupuesto y Calendario cuadran y cumplen impresión Carta.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
