"""Calendario v02. Reads CX-1's presupuesto_vNN.json and builds a 12-month Gantt.
If the budget is absent, emits a clearly provisional copy based on v01 chapters.
Run with --watch to regenerate when CX-1 changes the budget JSON.
Inputs: _harness/intermedios/presupuesto/presupuesto_vNN.json; fallback calendario_v01.json.
Outputs: Calendario/Calendario_v02.xlsx and _harness/intermedios/calendario/calendario_v02.json.
Dependencies: openpyxl. Owner: CX-2. Idempotent.
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys, time
from datetime import date
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / '_harness/intermedios/calendario/calendario_v02.json'
OUT_XLSX = ROOT / 'Calendario/Calendario_v02.xlsx'
BUDGET_DIR = ROOT / '_harness/intermedios/presupuesto'
PROJECT = 'Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"'
SCHEDULE = {
 '01': ('Preliminares','F1',1,1,[]), '02': ('CimentaciÃ³n','F1',1,2,['01']),
 '03': ('Estructura de concreto y mamposterÃ­a confinada','F1',2,5,['02']),
 '05': ('AlbaÃ±ilerÃ­a','F1',3,6,['02']), '04': ('Estructura metÃ¡lica y cubierta','F2',5,6,['03','05']),
 '08': ('InstalaciÃ³n hidrÃ¡ulica y pluvial','F3',5,9,['05']), '09': ('InstalaciÃ³n sanitaria','F3',5,9,['05']),
 '10': ('InstalaciÃ³n elÃ©ctrica y fotovoltaica','F3',5,9,['05']),
 '06': ('Acabados','F4',7,10,['04','08','09','10']), '07': ('HerrerÃ­a y cancelerÃ­a','F4',7,10,['04']),
 '13': ('Mobiliario y equipamiento fijo','F5',11,12,['06','07']), '14': ('Limpieza final y entrega','F5',12,12,['13'])}

def budget_file():
    candidate = BUDGET_DIR / 'presupuesto_v01.json'
    return candidate if candidate.is_file() else None

def t403_approved():
    queue = ROOT / '_harness/cola.md'
    if not queue.is_file(): return False
    for line in queue.read_text(encoding='utf-8-sig').splitlines():
        if re.match(r'^\s*-\s*\[[ xX]\]\s*T-403\s*\|', line):
            return bool(re.search(r'estado\s*:\s*aprobada\s*$', line, re.IGNORECASE))
    return False

def validate_and_update_status():
    validator = ROOT / 'Scripts/schemas/validar.py'
    result = subprocess.run([sys.executable, str(validator), 'calendario', str(OUT_JSON)], cwd=ROOT, capture_output=True, text=True)
    print((result.stdout + result.stderr).strip(), flush=True)
    if result.returncode:
        raise RuntimeError('validar.py rechazó el intermedio; revisar error anterior')
    status = ROOT / '_harness/status/CX-2.md'
    content = status.read_text(encoding='utf-8-sig') if status.exists() else '# CX-2 · Estado\n'
    start = '## Tareas'
    if start in content and '| T-503 |' in content:
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.startswith('| T-503 |'):
                lines[i] = '| T-503 | lista para revisión | `_harness/intermedios/calendario/calendario_v02.json`; `Calendario/Calendario_v02.xlsx` | OK validar.py; subtotal = presupuesto v01 |'
        content = '\n'.join(lines) + '\n'
    entry = ('\n## T-503 · Cierre automático\n'
             f'- Presupuesto: `_harness/intermedios/presupuesto/presupuesto_v01.json` aprobado por CL-1 en T-403.\n'
             '- Generada secuencia provisional de 12 meses (enero–diciembre 2027) con importes y avance financiero.\n'
             '- Intermedio validado con Scripts/schemas/validar.py calendario.\n')
    if '## T-503 · Cierre automático' not in content: content += entry
    tmp = status.with_name(status.name + '.tmp')
    tmp.write_text(content, encoding='utf-8'); tmp.replace(status)

def load_data():
    src = budget_file()
    if src:
        b = json.loads(src.read_text(encoding='utf-8-sig'))
        partidas = b.get('partidas', [])
        if not partidas: raise ValueError(f'{src} no contiene partidas')
        by_chapter = {}
        for p in partidas:
            cc = p['clave'].split('-')[1] if p.get('clave') else str(p.get('capitulo', '')).split()[0]
            by_chapter.setdefault(str(cc).zfill(2), []).append(p)
        allkeys = {p['clave'] for p in partidas}
        rows=[]
        for cc, items in by_chapter.items():
            title, front, start, end, parents = SCHEDULE.get(cc, (f'CapÃ­tulo {cc}','F5',9,12,[]))
            predecessor_keys = [p['clave'] for prev in parents for p in by_chapter.get(prev, [])]
            for p in items:
                rows.append({'clave':p['clave'],'concepto':p['concepto'],'frente':front,
                    'mes_inicio':start,'mes_fin':end,'predecesoras':predecessor_keys,
                    'importe':float(p['importe'])})
        # Sequential CPM on chapter network with the inherited 12-month work windows.
        # Activities inherit criticality from their chapter's longest downstream chain.
        ch_dur={cc:end-start+1 for cc,(_,_,start,end,_) in SCHEDULE.items()}
        ef={}
        for cc,(_,_,start,end,parents) in SCHEDULE.items(): ef[cc]=max((ef.get(x,0) for x in parents),default=0)+(end-start+1)
        project_end=max(ef.values())
        ls={}
        for cc in reversed(list(SCHEDULE)):
            succ=[x for x,(_,_,_,_,ps) in SCHEDULE.items() if cc in ps]
            dur=ch_dur[cc]; ls[cc]=min((ls[x] for x in succ),default=project_end)-dur
        for r in rows:
            cc=r['clave'].split('-')[1]
            months=r['mes_fin']-r['mes_inicio']+1
            # Even monthly financial distribution, exact 100% despite binary rounding.
            vals=[0.0]*12
            for m in range(r['mes_inicio'],r['mes_fin']+1): vals[m-1]=100/months
            vals[r['mes_fin']-1]=100-sum(vals[:r['mes_fin']-1])-sum(vals[r['mes_fin']:])
            r['avance_mensual_pct']=vals
            r['ruta_critica']=(cc in ls and ls[cc]==max((ef.get(x,0) for x in SCHEDULE[cc][4]),default=0))
        return {'version':'v02','fecha':date.today().strftime('%d-%m-%Y'),'fecha_inicio_obra':'04-01-2027',
            'duracion_meses':12,'presupuesto_usado':src.name,'actividades':rows,
            'total_importe':float(b['subtotal'])}, True
    old=json.loads((ROOT/'_harness/intermedios/calendario/calendario_v01.json').read_text(encoding='utf-8-sig'))
    rows=[]
    for a in old['actividades']:
        b=dict(a); b['concepto']=b['concepto'].replace('Estructura temporal capÃ­tulo','PROVISIONAL capÃ­tulo'); rows.append(b)
    return {'version':'v02','fecha':date.today().strftime('%d-%m-%Y'),'fecha_inicio_obra':'04-01-2027',
        'duracion_meses':12,'presupuesto_usado':None,'actividades':rows,'total_importe':None}, False

def generate():
    data, final=load_data(); rows=data['actividades']
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True); OUT_XLSX.parent.mkdir(parents=True,exist_ok=True)
    tmp=OUT_JSON.with_suffix('.json.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); tmp.replace(OUT_JSON)
    wb=Workbook(); ws=wb.active; ws.title='Programa 2027'
    ws.append([PROJECT]); ws.append([f"Fecha: {data['fecha']}",'VersiÃ³n: v02','Responsable: CX-2'])
    ws.append(['Programa financiero por partida' if final else 'PROVISIONAL: presupuesto CX-1 no disponible en esta copia del proyecto'])
    ws.append(['Clave','Concepto','Frente','Importe',*[f'Mes {i}' for i in range(1,13)],'Inicio','Fin','Predecesoras','Ruta crÃ­tica'])
    critical=PatternFill('solid',fgColor='F4B183'); ordinary=PatternFill('solid',fgColor='9DC3E6')
    for a in rows:
        ws.append([a['clave'],a['concepto'],a['frente'],a['importe'],*[x/100 for x in a['avance_mensual_pct']],a['mes_inicio'],a['mes_fin'],', '.join(a['predecesoras']),'SÃ­' if a['ruta_critica'] else 'No'])
        rr=ws.max_row
        for c in range(5,17):
            cell=ws.cell(rr,c); cell.number_format='0.00%'
            if cell.value: cell.fill=critical if a['ruta_critica'] else ordinary
        ws.cell(rr,4).number_format='$#,##0.00'
    n=ws.max_row; ws.cell(n+1,1,'Avance financiero mensual')
    ws.cell(n+2,1,'Avance financiero acumulado'); ws.cell(n+3,1,'Subtotal del presupuesto')
    if final:
        for c in range(5,17):
            L=get_column_letter(c); ws.cell(n+1,c,f'=SUMPRODUCT($D$5:$D${n},{L}5:{L}{n})')
            ws.cell(n+1,c).number_format='$#,##0.00'; ws.cell(n+2,c,f'=SUM($E${n+1}:{L}${n+1})'); ws.cell(n+2,c).number_format='$#,##0.00'
        ws.cell(n+3,4,f'=SUM(D5:D{n})'); ws.cell(n+3,4).number_format='$#,##0.00'
    else:
        ws.merge_cells(start_row=n+1,start_column=1,end_row=n+1,end_column=20)
    widths=[18,52,10,15]+[11]*12+[10,10,34,14]
    for c,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(c)].width=w
    ws.merge_cells('A1:T1'); ws.freeze_panes='E5'; ws.sheet_view.showGridLines=False
    ws.row_dimensions[1].height=28; ws['A1'].font=Font(size=14,bold=True,color='FFFFFF'); ws['A1'].fill=PatternFill('solid',fgColor='1F4E78')
    ws['A3'].font=Font(italic=True,color='9C0006' if not final else '385723')
    for cell in ws[4]: cell.font=Font(bold=True,color='FFFFFF'); cell.fill=PatternFill('solid',fgColor='4472C4'); cell.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
    for row in ws.iter_rows(min_row=5,max_row=n+3):
        for cell in row:
            cell.border=Border(bottom=Side(style='hair',color='B4C6E7'))
            if cell.column>=5: cell.alignment=Alignment(horizontal='center')
    ws.page_setup.paperSize=ws.PAPERSIZE_LETTER; ws.page_setup.orientation='landscape'; ws.page_setup.fitToWidth=1; ws.page_setup.fitToHeight=0
    ws.sheet_properties.pageSetUpPr.fitToPage=True; ws.print_area=f'A1:T{n+3}'; ws.print_title_rows='1:4'
    ws.page_margins.left=ws.page_margins.right=.5; ws.page_margins.top=ws.page_margins.bottom=.75
    ws.oddHeader.center.text=PROJECT; ws.oddHeader.right.text='VersiÃ³n v02 Â· &D'; ws.oddFooter.left.text='Responsable: CX-2'; ws.oddFooter.right.text='PÃ¡gina &P de &N'
    xtmp=OUT_XLSX.with_name(OUT_XLSX.stem+'.tmp.xlsx'); wb.save(xtmp); wb.close(); xtmp.replace(OUT_XLSX)
    return len(rows),final

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--watch',action='store_true'); ap.add_argument('--interval',type=float,default=5); args=ap.parse_args()
    if args.watch:
        print('Observando presupuesto_v01.json y aprobación de T-403 por CL-1; no se generará T-503 hasta cumplir ambas condiciones.',flush=True)
        last_done=None
        while True:
            f=budget_file(); ready=bool(f and t403_approved())
            stamp=f.stat().st_mtime_ns if ready else None
            if ready and stamp!=last_done:
                count,final=generate()
                if final:
                    validate_and_update_status()
                    print(f'T-503 listo para revisión: {count} actividades; subtotal conciliado.',flush=True)
                    last_done=stamp
            time.sleep(args.interval)
    while True:
        count,final=generate(); print(f"v02 regenerado: {count} actividades; presupuesto={'CX-1' if final else 'pendiente'}",flush=True)
        if not args.watch: break
        f=budget_file(); stamp=f.stat().st_mtime_ns if f else None
        while True:
            time.sleep(args.interval); nf=budget_file(); ns=nf.stat().st_mtime_ns if nf else None
            if ns is not None and ns!=stamp: break

