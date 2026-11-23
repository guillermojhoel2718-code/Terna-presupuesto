# Cola de tareas

Formato: `- [ ] T-NNN | ID | descripción | depende: … | estado: …`
Estados: `pendiente`, `en curso`, `bloqueada`, `lista para revisión`, `aprobada`, `rechazada`.
Cada agente cambia **solo la línea de su tarea** (con lock, ver SPEC_01). Solo CL-1 marca `aprobada`/`rechazada` y agrega tareas.
Olas y criterio de cierre: `_harness/PLAN_IMPLEMENTACION.md`.
Equipos (D-014): **CL-1 → PC-A**; **AG-1, AG-2, CX-1, CX-2 → PC-B**.

## Ola 0 · Preparación (CL-1)
- [x] T-000 | CL-1 | Harness, specs, schemas Pydantic, decisiones D-001…D-007 | depende: — | estado: aprobada
- [x] T-001 | USUARIO | Revit 2027 abierto en PC-B con el federado; eléctrico vinculado (6 vínculos) | depende: — | estado: aprobada
- [x] T-002 | USUARIO | Responder P-001…P-006 | depende: — | estado: aprobada
- [ ] T-003 | USUARIO | PC-A y PC-B: cerrar Revit, correr `MCP Revit/instalar_revitcortex.ps1`, reabrir Revit y encender Cortex Switch | depende: — | estado: en curso
  > 23-11-2026: PC-B ya tiene RevitCortex (setup-MEMO). Falta confirmar PC-A.
- [ ] T-004 | USUARIO | PC-B: correr `Scripts/01_preparar_equipo.ps1` y pegar el prompt de sincronización (`prompts_agentes.md` §0) | depende: — | estado: aprobada
  > 23-11-2026: setup-MEMO OK, LISTO PARA AGENTES: SÍ.

## Ola 1 · Paralelo total
### AG-1 · Revit
- [ ] T-101 | AG-1 | Verificar MCP/`pyrevit agent status`, inventario de vínculos cargados, conteo de elementos por categoría y modelo → `revit/indice.json` | depende: T-001 | estado: aprobada
  > 23-11-2026 CL-1: cifras de AG-1 verificadas contra los JSON (101 muros NOVABLOCK = 1,337.95 m²; cimentación 43.8251 m³; 87 muros ladrillo = 1,040.43 m²).
- [ ] T-102 | AG-1 | Extraer Estructura (cimentación, castillos/columnas, trabes/dalas, losas, acero de cubierta) | depende: T-101 | estado: aprobada
  > 23-11-2026 CL-1: cifras de AG-1 verificadas contra los JSON (101 muros NOVABLOCK = 1,337.95 m²; cimentación 43.8251 m³; 87 muros ladrillo = 1,040.43 m²).
- [ ] T-103 | AG-1 | Extraer TT-ED-EDU-ARQ-MOB (solo mobiliario y equipo; muros y desplante salen de Estructura/Cancelería, D-019) | depende: T-101 | estado: aprobada
  > 23-11-2026 CL-1: 59/59 válidos por schema; hallazgos documentados por AG-1 (notas_doble_conteo_muros.md).
- [ ] T-104 | AG-1 | Extraer Acabados (pisos, muros, plafones) | depende: T-101 | estado: aprobada
  > 23-11-2026 CL-1: 59/59 válidos por schema; hallazgos documentados por AG-1 (notas_doble_conteo_muros.md).
- [ ] T-105 | AG-1 | Extraer Cancelería (puertas, ventanas, muros cortina, barandales) | depende: T-101 | estado: aprobada
  > 23-11-2026 CL-1: cifras de AG-1 verificadas contra los JSON (101 muros NOVABLOCK = 1,337.95 m²; cimentación 43.8251 m³; 87 muros ladrillo = 1,040.43 m²).
- [ ] T-106 | AG-1 | Extraer IHS (tuberías por sistema y diámetro, conexiones, muebles) | depende: T-101 | estado: lista para revisión
  > CL-1: válido por schema; queda pendiente la re-extracción de Instalaciones.rvt cuando el usuario cargue el sub-vínculo 'Bloque de baños' (P-010). Duplicados detectados en mi prueba: 118 elementos cuentan en ED-08-01-003 y ED-09-01-003 a la vez (conexiones hidráulicas y sanitarias): separar por sistema/tipo de tubería en el mapeo.
- [ ] T-107 | AG-1 | Extraer Eléctrico (vínculo) | depende: T-101 | estado: aprobada
  > 23-11-2026 CL-1: 59/59 válidos por schema; hallazgos documentados por AG-1 (notas_doble_conteo_muros.md).
### AG-2 · Precios
- [ ] T-201 | AG-2 | Extraer e indexar tabulador CDMX 2026 → `pdf/tabulador_cdmx_indice.json` | depende: — | estado: lista para revisión
  > CL-1: el PDF llegó al PC-B (tabulador_cdmx_2026.txt, índice con 5,477 conceptos). Los 36 precios citados del catálogo coinciden con el PDF original (clave, página y precio): 36/36.
- [ ] T-202 | AG-2 | Extraer texto de PDFs Neodata (02, 03, 05, 08) y Xalapa a `pdf/` | depende: — | estado: aprobada
  > 23-11-2026 CL-1: textos por página presentes, incluido el tabulador.
- [ ] T-203 | AG-2 | Deduplicar y normalizar insumos (`precios_procesados`) → `precios/insumos_norm.json` | depende: — | estado: aprobada
  > CL-1: 12,200 insumos únicos; cuadra con 12,200 + 12,052 + 148 = 24,400 filas de los 3 CSV.
- [ ] T-204 | AG-2 | Catálogo de conceptos por capítulo (claves, descripciones, unidades, `mapeo_revit`) → `catalogo_v01.json` sin precios | depende: — (usa `revit/indice.json` si ya existe) | estado: rechazada
  > 23-11-2026 CL-1: schema OK y 65 conceptos, pero `mapeo_revit` se armó antes de los datos de AG-1: con `py Scripts/30_generadores_desde_revit.py` solo 23 de 65 conceptos reciben cantidad (42 sin cantidad, incluidos cimentación, estructura, cubierta y muros). El cap. 05 sigue mapeado a ARQ-MOB (D-017, superado por D-019) y ARQ-MOB no tiene muros. Rehacer los mapeos en catalogo_v02.json con revit/indice.json y notas_doble_conteo_muros.md (ver T-206).
- [ ] T-205 | AG-2 | Precios: tabulador → catálogo → APU → SUPUESTO; actualizar `catalogo_v01.json` | depende: T-201, T-202, T-203, T-204 | estado: lista para revisión
  > CL-1: 36 precios TABULADOR_CDMX verificados 36/36 contra el PDF. Pendiente muestreo de los 25 APU y los 4 SUPUESTO (ED-01-03-001, ED-08-03-001, ED-09-03-002, ED-10-05-001). El status de AG-2 dice 61 APU, el catálogo dice 36 tabulador + 25 APU + 4 supuesto: corregir el status.
### CX-1 · Presupuesto (preparación)
- [ ] T-401 | CX-1 | Copiar plantilla a `Presupuesto/`, corregir defectos (SPEC_06 §3), AW11=12, Carta; verificar método de recálculo (COM/LibreOffice) | depende: — | estado: aprobada
  > 23-11-2026 CL-1: Presupuesto_v00_base.xlsm conserva hojas y macros; AW11=12, Q9 sin #REF!, nombre y 2,500 m² (D-010), papel Carta. Antes de T-403: (a) definir área de impresión en D25-00_Sobrecosto y 01_Datos Generales (SPEC_07); (b) quedan #VALUE! en A1 (Resumen), A2 (Presupuesto), BE1 (Sobrecosto), A2 y A9 (Ref_Datos), ya presentes en la plantilla original, probablemente los logos: corregirlos o vaciarlos para que no salgan en el PDF.
- [ ] T-402 | CX-1 | Script `40_llenar_plantilla_presupuesto.py`: JSON → renglones/jerarquía/resumen, lectura del factor de sobrecosto; probar con datos de prueba | depende: T-401 | estado: aprobada
  > 23-11-2026 CL-1: py validar.py presupuesto OK sobre Presupuesto_v00_prueba_resultado.json. Verificado en el libro recalculado: AW5=L16=2,500, AD200=3,075,750, AD210=277,042.5, AD211=33,552.93, AW215=3,419,713.24, J16=AW215/L16=1,367.885 (factor sin tecleo de porcentajes). El factor de la prueba es absurdo solo por CD sintético de 2,500 contra indirectos fijos de 12 meses. IVA resuelto: 16 % (D-020, P-012).
### CX-2 · Calendario (estructura)
- [ ] T-501 | CX-2 | Estructura de actividades por capítulo/frente (SPEC_02 §3), duraciones y predecesoras; inicio enero 2027 (D-012) | depende: — | estado: aprobada
  > 23-11-2026 CL-1: 65 actividades con las mismas claves del catálogo, schema OK, 12 meses, CPM adelante/atrás. Críticas: 40 de 65 (alto pero ya no 12/12). Duraciones siguen siendo SUPUESTO; recalcular con cantidades de generadores_v01.
- [ ] T-502 | CX-2 | Script `50_calendario_12_meses.py` + plantilla Excel horizontal Carta; `calendario_v01.json` estructura (sin importes) | depende: T-501 | estado: aprobada
  > 23-11-2026 CL-1: Calendario_v01.xlsx y PDF de revisión generados con Excel COM por CX-2. Rehacer cuando haya claves/cantidades definitivas.
### CL-1 · Generadores (preparación) y QA
- [ ] T-301 | CL-1 | Limpiar plantilla de generadores y script `30_generadores_desde_revit.py` (aplica `mapeo_revit` a intermedios Revit) | depende: — | estado: aprobada
  > 23-11-2026 CL-1: probado con datos sintéticos (Σ JSON = totales recalculados en Excel, Carta horizontal 1 pág. de ancho, idempotente). Formato generado por script; ver D-018.
- [ ] T-901 | CL-1 | Revisar cada entrega de Ola 1 contra schema y fuente; aprobar/rechazar | depende: tareas de Ola 1 | estado: pendiente

## Ola 2 · Cuantificación
- [ ] T-302 | CL-1 | Generadores v01 por capítulo (02–07) | depende: T-102…T-106, T-204 | estado: bloqueada
  > Espera catalogo_v02.json (T-206). Origen de muros ya confirmado (D-019) y doble conteo resuelto por AG-1 (P-011).
- [ ] T-303 | CL-1 | Generadores v01 de instalaciones (08–10) y sin Revit (01, 14) | depende: T-106, T-107, T-204 | estado: pendiente
- [ ] T-304 | CL-1 | `Generadores/Generadores_v01.xlsx` impresión Carta | depende: T-302, T-303 | estado: pendiente
- [ ] T-206 | AG-2 | Cerrar precios faltantes de las claves con cantidad; `catalogo_v02.json` si v01 ya fue aprobado | depende: T-205, T-302 | estado: pendiente
  > 23-11-2026 CL-1: reactivada y prioritaria. Entregar catalogo_v02.json con `mapeo_revit` real (ver prompt a AG-2). Bloquea T-302.

## Ola 3 · Presupuesto y calendario
- [ ] T-403 | CX-1 | Presupuesto v01: cantidades + CD + sobrecosto → `presupuesto_v01.json` y `Presupuesto/Presupuesto_v01.xlsm` | depende: T-304, T-205, T-402 | estado: pendiente
- [ ] T-503 | CX-2 | Calendario v01 con importes y avance financiero → `Calendario/Calendario_v01.xlsx` | depende: T-403, T-502 | estado: pendiente

## Ola 4 · Integración
- [ ] T-902 | CL-1 | QA cruzado (`90_qa_cruzado.py`): Σ generadores = cantidades del presupuesto; Σ calendario = subtotal; 100 % por actividad | depende: T-403, T-503 | estado: pendiente
- [ ] T-903 | CL-1 | Consolidar `Resultados/*_v01` + copia fechada en `Resultados/revisiones/` | depende: T-902 | estado: pendiente
