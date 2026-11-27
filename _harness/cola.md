# Cola de tareas

Formato: `- [ ] T-NNN | ID | descripción | depende: … | estado: …`
Estados: `pendiente`, `en curso`, `bloqueada`, `lista para revisión`, `aprobada`, `rechazada`.
Cada agente cambia **solo la línea de su tarea** (en modo dos equipos D-014 / SPEC_08 §2, solo CL-1 escribe `cola.md` desde `status/<ID>.md`). Solo CL-1 marca `aprobada`/`rechazada` y agrega tareas.
Olas y criterio de cierre: `_harness/PLAN_IMPLEMENTACION.md`.
Equipos (D-014): **CL-1 → PC-A**; **AG-1, AG-2, CX-1, CX-2 → PC-B**.

## Ola 0 · Preparación (CL-1)
- [x] T-000 | CL-1 | Harness, specs, schemas Pydantic, decisiones D-001…D-007 | depende: — | estado: aprobada
- [x] T-001 | USUARIO | Revit 2027 abierto en PC-B con el federado; eléctrico vinculado (6 vínculos) | depende: — | estado: aprobada
- [x] T-002 | USUARIO | Responder P-001…P-006 | depende: — | estado: aprobada
- [ ] T-003 | USUARIO | PC-A y PC-B: cerrar Revit, correr `MCP Revit/instalar_revitcortex.ps1`, reabrir Revit y encender Cortex Switch | depende: — | estado: pendiente
  - Nota CL-1 (26-11-2026): `setup-MEMO-23-11-2026.md` confirma RevitCortex instalado; AG-1 operó vía pyRevit sin bloqueo.
- [x] T-004 | USUARIO | PC-B: correr `Scripts/01_preparar_equipo.ps1` y pegar el prompt de sincronización (`prompts_agentes.md` §0) | depende: — | estado: aprobada
  - Verificado en `_harness/logs/setup-MEMO-23-11-2026.md` (`LISTO PARA AGENTES: SÍ`, 6/6 vínculos cargados).

## Ola 1 · Paralelo total
### AG-1 · Revit
- [x] T-101 | AG-1 | Verificar MCP/`pyrevit agent status`, inventario de vínculos cargados, conteo de elementos por categoría y modelo → `revit/indice.json` | depende: T-001 | estado: aprobada
  - Incluye `notas_doble_conteo_muros.md` y `resumen_por_categoria_y_nivel.{json,md}` (26-11-2026).
- [x] T-102 | AG-1 | Extraer Estructura (cimentación, castillos/columnas, trabes/dalas, losas, acero de cubierta) | depende: T-101 | estado: aprobada
- [x] T-103 | AG-1 | Extraer TT-ED-EDU-ARQ-MOB (muros, pisos, cubiertas, mobiliario, área de desplante) | depende: T-101 | estado: aprobada
- [x] T-104 | AG-1 | Extraer Acabados (pisos, muros, plafones) | depende: T-101 | estado: aprobada
- [x] T-105 | AG-1 | Extraer Cancelería (puertas, ventanas, muros cortina, barandales) | depende: T-101 | estado: aprobada
- [x] T-106 | AG-1 | Extraer IHS (tuberías por sistema y diámetro, conexiones, muebles) | depende: T-101 | estado: aprobada
  - QA CL-1 (26-11-2026): 7/7 `Instalaciones__*.json` validados OK con `validar.py revit`. Abierta P-010 por sub-vínculo `Bloque de baños_vinculo.rvt` (Unloaded); se aprueba con lo existente para no bloquear Ola 2.
- [x] T-107 | AG-1 | Extraer Eléctrico (vínculo) | depende: T-101 | estado: aprobada
### AG-2 · Precios
- [x] T-201 | AG-2 | Extraer e indexar tabulador CDMX 2026 → `pdf/tabulador_cdmx_indice.json` | depende: — | estado: aprobada
  - QA CL-1 (26-11-2026): 5,477 conceptos indexados; referencias verificadas en `catalogo_v01.json` y `catalogo_v02.json`.
- [x] T-202 | AG-2 | Extraer texto de PDFs Neodata (02, 03, 05, 08) y Xalapa a `pdf/` | depende: — | estado: aprobada
- [x] T-203 | AG-2 | Deduplicar y normalizar insumos (`precios_procesados`) → `precios/insumos_norm.json` | depende: — | estado: aprobada
- [x] T-204 | AG-2 | Catálogo de conceptos por capítulo (claves, descripciones, unidades, `mapeo_revit`) → `catalogo_v01.json` sin precios | depende: — (usa `revit/indice.json` si ya existe) | estado: aprobada
  - QA CL-1 (26-11-2026): `validar.py precios _harness/intermedios/precios/catalogo_v01.json` → OK (65 conceptos, 0 `sin_precio`).
- [x] T-205 | AG-2 | Precios: tabulador → catálogo → APU → SUPUESTO; actualizar `catalogo_v01.json` | depende: T-201, T-202, T-203, T-204 | estado: aprobada
  - QA CL-1 (26-11-2026): 65/65 con costo directo MXN (36 TABULADOR_CDMX + 25 APU + 4 SUPUESTO).
### CX-1 · Presupuesto (preparación)
- [x] T-401 | CX-1 | Copiar plantilla a `Presupuesto/`, corregir defectos (SPEC_06 §3), AW11=12, Carta; verificar método de recálculo (COM/LibreOffice) | depende: — | estado: aprobada
  - QA CL-1 (26-11-2026): `Presupuesto/Presupuesto_v00_base.xlsm` con macros conservadas, defectos SPEC_06 §3 corregidos, `AW11=12`, Carta y recálculo Excel COM verificado.
- [x] T-402 | CX-1 | Script `40_llenar_plantilla_presupuesto.py`: JSON → renglones/jerarquía/resumen, lectura del factor de sobrecosto; probar con datos de prueba | depende: T-401 | estado: aprobada
  - QA CL-1 (26-11-2026): `Scripts/40_llenar_plantilla_presupuesto.py` + `41_recalcular_presupuesto.ps1` probados con libro sintético y recálculo COM.
### CX-2 · Calendario (estructura)
- [x] T-501 | CX-2 | Estructura de actividades por capítulo/frente (SPEC_02 §3), duraciones y predecesoras; inicio enero 2027 (D-012) | depende: — | estado: aprobada
  - QA CL-1 (26-11-2026): estructura provisional de 12 capítulos/frentes aprobada para desbloquear Ola 3 (ver P-018 sobre fuentes de duración).
- [x] T-502 | CX-2 | Script `50_calendario_12_meses.py` + plantilla Excel horizontal Carta; `calendario_v01.json` estructura (sin importes) | depende: T-501 | estado: aprobada
  - QA CL-1 (26-11-2026): `calendario_v01.json` y `calendario_v02.json` validados OK con `validar.py calendario`; `Calendario_v01.xlsx` y `Calendario_v02.xlsx` presentes.
### CL-1 · Generadores (preparación) y QA
- [x] T-301 | CL-1 | Limpiar plantilla de generadores y script `30_generadores_desde_revit.py` (aplica `mapeo_revit` a intermedios Revit) | depende: — | estado: aprobada
  - `Scripts/30_generadores_desde_revit.py` alineado al catálogo de 65 claves (`Scripts/21+22`) + 16 cantidades derivadas de `resumen_por_categoria_y_nivel.json`.
- [x] T-901 | CL-1 | Revisar cada entrega de Ola 1 contra schema y fuente; aprobar/rechazar | depende: tareas de Ola 1 | estado: aprobada
  - Todas las entregas de Ola 1 (AG-1, AG-2, CX-1, CX-2, CL-1) validadas y aprobadas.

## Ola 2 · Cuantificación
- [x] T-302 | CL-1 | Generadores v01 por capítulo (02–07) | depende: T-102…T-106, T-204 | estado: aprobada
  - Entregado en `_harness/intermedios/generadores/generadores_v02.json` (validado OK con `validar.py generadores`; 65 claves: 47 directas de Revit + 16 derivadas + 2 pendientes P-010).
- [x] T-303 | CL-1 | Generadores v01 de instalaciones (08–10) y sin Revit (01, 14) | depende: T-106, T-107, T-204 | estado: aprobada
  - Integrado en `_harness/intermedios/generadores/generadores_v02.json` (capítulos 01, 08, 09, 10, 13 y 14 completos; `ED-09-02-001` y `ED-09-02-002` en `claves_sin_cantidad` por P-010).
- [x] T-304 | CL-1 | `Generadores/Generadores_v01.xlsx` impresión Carta | depende: T-302, T-303 | estado: aprobada
  - Generado `Generadores/Generadores_v02.xlsx` (14 hojas: `RESUMEN`, `01 PRE`..`14 LIM`, `REF_REVIT`, Carta horizontal, 1 pág. de ancho, SPEC_07).
- [x] T-206 | AG-2 | Cerrar precios faltantes de las claves con cantidad; `catalogo_v02.json` si v01 ya fue aprobado | depende: T-205, T-302 | estado: aprobada
  - QA CL-1 (26-11-2026): `validar.py precios _harness/intermedios/precios/catalogo_v02.json` → OK (107 conceptos: 47 TABULADOR_CDMX + 53 APU + 7 SUPUESTO, 0 `sin_precio`; incluye `Catalogo_precios_v02.xlsm`/`.xlsx`).

## Ola 3 · Presupuesto y calendario
- [x] T-403 | CX-1 | Presupuesto v01: cantidades + CD + sobrecosto → `presupuesto_v01.json` y `Presupuesto/Presupuesto_v01.xlsm` | depende: T-304, T-205, T-402 | estado: aprobada
  - QA CL-1 (26-11-2026): `validar.py presupuesto` → OK; 63 partidas (CD $14,682,580.51; factor sobrecosto 1.389012; subtotal $20,394,278.87; IVA $3,263,084.62; total $23,657,363.49); Carta y macros conservadas.
- [x] T-503 | CX-2 | Calendario v01 con importes y avance financiero → `Calendario/Calendario_v01.xlsx` | depende: T-403, T-502 | estado: aprobada
  - QA CL-1 (26-11-2026): `Calendario/Calendario_v02.xlsx` y `calendario_v02.json` generados automáticamente con 63 partidas e importes reales; `validar.py calendario` → OK; subtotal = `$20,394,278.87` = Presupuesto v01; 100% por actividad.

## Ola 4 · Integración
- [x] T-902 | CL-1 | QA cruzado (`90_qa_cruzado.py`): Σ generadores = cantidades del presupuesto; Σ calendario = subtotal; 100 % por actividad | depende: T-403, T-503 | estado: aprobada
  - `python Scripts/90_qa_cruzado.py --gen v02 --pto v01 --cal v02` → `QA CRUZADO OK` (código 0; 20/20 hojas en Carta, `fitToWidth=1`).
- [x] T-903 | CL-1 | Consolidar `Resultados/*_v01` + copia fechada en `Resultados/revisiones/` | depende: T-902 | estado: aprobada
  - Consolidados en `Resultados/` y `Resultados/revisiones/26-11-2026/`: `Generadores_v02.xlsx`, `Presupuesto_v01.xlsm`, `Calendario_v02.xlsx`, `Catalogo_precios_v02.xlsm` y `Catalogo_precios_v02.xlsx`.
