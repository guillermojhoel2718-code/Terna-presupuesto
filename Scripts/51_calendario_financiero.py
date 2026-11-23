"""Integración financiera del calendario (CX-2, T-503).
Entrada real: presupuesto_v01.json aprobado (cola T-403 aprobada) y calendario_v01.json.
Salida real: calendario_v01.json con importes y Calendario_v01.xlsx con flujo mensual.
Modo de prueba: --self-test usa datos sintéticos en memoria, no escribe archivos.
Dependencias: pydantic, openpyxl. Ejecutar con Python absoluto del PC-B.
Fecha: 23-11-2026. Escritura JSON/XLSX atómica mediante .tmp y rename.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
JSON_CAL = ROOT / "_harness/intermedios/calendario/calendario_v01.json"
JSON_BUDGET = ROOT / "_harness/intermedios/presupuesto/presupuesto_v01.json"
QUEUE = ROOT / "_harness/cola.md"
XLSX = ROOT / "Calendario/Calendario_v01.xlsx"


def allocate(calendar: dict, budget: dict) -> tuple[dict, list[list[float]]]:
    subtotal = float(budget["subtotal"])
    partidas = budget["partidas"]
    by_key = {p["clave"]: p for p in partidas}
    if len(by_key) != len(partidas):
        raise ValueError("presupuesto_v01.json contiene claves duplicadas")
    activities = calendar["actividades"]
    cal_keys = {a["clave"] for a in activities}
    budget_keys = set(by_key)
    if cal_keys != budget_keys:
        raise ValueError(f"Claves calendario/presupuesto no coinciden; faltan={sorted(budget_keys-cal_keys)}, sobran={sorted(cal_keys-budget_keys)}")
    budget_sum = sum(float(p["importe"]) for p in partidas)
    if abs(budget_sum - subtotal) > 0.05:
        raise ValueError(f"Σ importes presupuesto {budget_sum} no coincide con subtotal {subtotal}")
    monthly = [[0.0] * 12 for _ in activities]
    for i, activity in enumerate(activities):
        amount = float(by_key[activity["clave"]]["importe"])
        shares = activity["avance_mensual_pct"]
        if len(shares) != 12 or abs(sum(shares) - 100.0) > 1e-6:
            raise ValueError(f"{activity['clave']}: avance no suma 100% en 12 meses")
        activity["importe"] = amount
        monthly[i] = [amount * float(pct) / 100.0 for pct in shares]
    calendar["presupuesto_usado"] = "presupuesto_v01.json"
    calendar["total_importe"] = subtotal
    calendar_sum = sum(float(a["importe"]) for a in activities)
    if abs(calendar_sum - subtotal) > 0.05:
        raise ValueError(f"Σ calendario {calendar_sum} no coincide con subtotal presupuesto {subtotal}")
    if abs(sum(sum(m) for m in monthly) - subtotal) > 0.05:
        raise ValueError("El flujo mensual distribuido no coincide con el subtotal")
    return calendar, monthly


def self_test() -> None:
    cal = {"actividades":[
      {"clave":"ED-01-01-001","avance_mensual_pct":[100.0]+[0.0]*11,"importe":None},
      {"clave":"ED-02-01-001","avance_mensual_pct":[0.0,50.0,50.0]+[0.0]*9,"importe":None},
    ]}
    budget = {"subtotal":500.0,"partidas":[
      {"clave":"ED-01-01-001","importe":300.0},
      {"clave":"ED-02-01-001","importe":200.0},
    ]}
    result, monthly = allocate(cal,budget)
    assert result["total_importe"] == 500.0
    assert sum(a["importe"] for a in result["actividades"]) == budget["subtotal"]
    assert abs(sum(sum(x) for x in monthly)-budget["subtotal"])<0.01
    assert monthly[0][0] == 300.0 and monthly[1][1:3] == [100.0,100.0]
    print("SELF-TEST OK: subtotal presupuesto = calendario = flujo mensual = 500.00")


def require_approval() -> None:
    if not QUEUE.exists(): raise SystemExit(f"Falta cola de control: {QUEUE}")
    text=QUEUE.read_text(encoding="utf-8")
    line=next((x for x in text.splitlines() if re.search(r"\bT-403\b",x)),"")
    if not re.search(r"estado:\s*aprobada\b",line,re.IGNORECASE):
        raise SystemExit("T-503 no se inicia: cola.md aún no marca T-403/presupuesto_v01.json como aprobada.")


def write_json_atomic(path: Path, obj: dict) -> None:
    tmp=path.with_name(path.name+".tmp")
    if tmp.exists(): raise FileExistsError(f"Temporal existente, no se sobrescribe: {tmp}")
    tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    tmp.replace(path)


def write_workbook(calendar: dict, monthly: list[list[float]], budget: dict) -> None:
    wb=load_workbook(XLSX)
    try:
        ws=wb["Programa"]
        by_key={a["clave"]:a for a in calendar["actividades"]}
        key_rows={}
        for row in range(5,ws.max_row+1):
            key=ws.cell(row,1).value
            if key in by_key: key_rows[key]=row
        if set(key_rows)!=set(by_key): raise ValueError("El Excel estructural no contiene todas las claves del calendario")
        month_amount_start=26  # Z; las columnas G:R contienen avance mensual porcentual.
        for m in range(12): ws.cell(4,month_amount_start+m,f"Mes {m+1} $")
        for i,a in enumerate(calendar["actividades"]):
            row=key_rows[a["clave"]]
            ws.cell(row,6,float(a["importe"])).number_format='$#,##0.00'
            for m in range(12):
                pct_col=7+m; amount_col=month_amount_start+m
                ws.cell(row,amount_col,f"=$F{row}*{__import__('openpyxl').utils.get_column_letter(pct_col)}{row}")
                ws.cell(row,amount_col).number_format='$#,##0.00'
        final_row=max(key_rows.values())
        subtotal_row=final_row+2; monthly_pct_row=subtotal_row+1; cumulative_row=subtotal_row+2
        ws.cell(subtotal_row,1,"Subtotal del calendario")
        ws.cell(subtotal_row,6,f"=SUM(F5:F{final_row})").number_format='$#,##0.00'
        for m in range(12):
            col=month_amount_start+m; letter=__import__('openpyxl').utils.get_column_letter(col)
            ws.cell(subtotal_row,col,f"=SUM({letter}5:{letter}{final_row})").number_format='$#,##0.00'
        ws.cell(monthly_pct_row,1,"Avance financiero mensual")
        ws.cell(cumulative_row,1,"Avance financiero acumulado")
        for m in range(12):
            amount_letter=__import__('openpyxl').utils.get_column_letter(month_amount_start+m)
            pct_letter=__import__('openpyxl').utils.get_column_letter(7+m)
            ws.cell(monthly_pct_row,7+m,f"=IF($F${subtotal_row}=0,0,{amount_letter}{subtotal_row}/$F${subtotal_row})").number_format='0.00%'
            prior=__import__('openpyxl').utils.get_column_letter(7+m)
            ws.cell(cumulative_row,7+m,f"=SUM($G${monthly_pct_row}:{prior}${monthly_pct_row})").number_format='0.00%'
        ws.cell(subtotal_row,1).font=ws.cell(monthly_pct_row,1).font=ws.cell(cumulative_row,1).font
        ws.page_setup.paperSize=ws.PAPERSIZE_LETTER; ws.page_setup.orientation='landscape'; ws.page_setup.fitToWidth=1; ws.page_setup.fitToHeight=0; ws.sheet_properties.pageSetUpPr.fitToPage=True
        ws.print_area=f"A1:AK{cumulative_row}"
        for c in range(26,38): ws.column_dimensions[__import__('openpyxl').utils.get_column_letter(c)].width=13
        tmp=XLSX.with_name(XLSX.name+".tmp.xlsx")
        if tmp.exists(): raise FileExistsError(f"Temporal Excel existente, no se sobrescribe: {tmp}")
        wb.save(tmp)
    finally:
        wb.close()
    tmp.replace(XLSX)


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true",help="probar reparto con fixture sintético en memoria; no escribe")
    args=parser.parse_args()
    if args.self_test: self_test(); return
    require_approval()
    if not JSON_CAL.exists() or not JSON_BUDGET.exists(): raise SystemExit("Faltan JSON de calendario o presupuesto v01")
    sys.path.insert(0,str(ROOT/"Scripts/schemas"))
    from calendario import Calendario
    from presupuesto import Presupuesto
    budget=json.loads(JSON_BUDGET.read_text(encoding="utf-8")); Presupuesto.model_validate(budget)
    calendar=json.loads(JSON_CAL.read_text(encoding="utf-8")); Calendario.model_validate(calendar)
    calendar,monthly=allocate(calendar,budget)
    Calendario.model_validate(calendar)
    write_json_atomic(JSON_CAL,calendar)
    write_workbook(calendar,monthly,budget)
    print(f"T-503 listo: total_importe calendario = subtotal presupuesto = {calendar['total_importe']:.2f}")

if __name__ == "__main__": main()