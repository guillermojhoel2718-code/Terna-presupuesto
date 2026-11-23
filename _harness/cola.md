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
- [ ] T-003 | USUARIO | PC-A y PC-B: cerrar Revit, correr `MCP Revit/instalar_revitcortex.ps1`, reabrir Revit y encender Cortex Switch | depende: — | estado: pendiente
- [ ] T-004 | USUARIO | PC-B: correr `Scripts/01_preparar_equipo.ps1` y pegar el prompt de sincronización (`prompts_agentes.md` §0) | depende: — | estado: pendiente

## Ola 1 · Paralelo total
### AG-1 · Revit
- [ ] T-101 | AG-1 | Verificar MCP/`pyrevit agent status`, inventario de vínculos cargados, conteo de elementos por categoría y modelo → `revit/indice.json` | depende: T-001 | estado: pendiente
- [ ] T-102 | AG-1 | Extraer Estructura (cimentación, castillos/columnas, trabes/dalas, losas, acero de cubierta) | depende: T-101 | estado: pendiente
- [ ] T-103 | AG-1 | Extraer TT-ED-EDU-ARQ-MOB (muros, pisos, cubiertas, mobiliario, área de desplante) | depende: T-101 | estado: pendiente
- [ ] T-104 | AG-1 | Extraer Acabados (pisos, muros, plafones) | depende: T-101 | estado: pendiente
- [ ] T-105 | AG-1 | Extraer Cancelería (puertas, ventanas, muros cortina, barandales) | depende: T-101 | estado: pendiente
- [ ] T-106 | AG-1 | Extraer IHS (tuberías por sistema y diámetro, conexiones, muebles) | depende: T-101 | estado: pendiente
- [ ] T-107 | AG-1 | Extraer Eléctrico (vínculo) | depende: T-101 | estado: pendiente
### AG-2 · Precios
- [ ] T-201 | AG-2 | Extraer e indexar tabulador CDMX 2026 → `pdf/tabulador_cdmx_indice.json` | depende: — | estado: pendiente
- [ ] T-202 | AG-2 | Extraer texto de PDFs Neodata (02, 03, 05, 08) y Xalapa a `pdf/` | depende: — | estado: pendiente
- [ ] T-203 | AG-2 | Deduplicar y normalizar insumos (`precios_procesados`) → `precios/insumos_norm.json` | depende: — | estado: pendiente
- [ ] T-204 | AG-2 | Catálogo de conceptos por capítulo (claves, descripciones, unidades, `mapeo_revit`) → `catalogo_v01.json` sin precios | depende: — (usa `revit/indice.json` si ya existe) | estado: pendiente
- [ ] T-205 | AG-2 | Precios: tabulador → catálogo → APU → SUPUESTO; actualizar `catalogo_v01.json` | depende: T-201, T-202, T-203, T-204 | estado: pendiente
### CX-1 · Presupuesto (preparación)
- [ ] T-401 | CX-1 | Copiar plantilla a `Presupuesto/`, corregir defectos (SPEC_06 §3), AW11=12, Carta; verificar método de recálculo (COM/LibreOffice) | depende: — | estado: pendiente
- [ ] T-402 | CX-1 | Script `40_llenar_plantilla_presupuesto.py`: JSON → renglones/jerarquía/resumen, lectura del factor de sobrecosto; probar con datos de prueba | depende: T-401 | estado: pendiente
### CX-2 · Calendario (estructura)
- [ ] T-501 | CX-2 | Estructura de actividades por capítulo/frente (SPEC_02 §3), duraciones y predecesoras; inicio enero 2027 (D-012) | depende: — | estado: pendiente
- [ ] T-502 | CX-2 | Script `50_calendario_12_meses.py` + plantilla Excel horizontal Carta; `calendario_v01.json` estructura (sin importes) | depende: T-501 | estado: pendiente
### CL-1 · Generadores (preparación) y QA
- [ ] T-301 | CL-1 | Limpiar plantilla de generadores y script `30_generadores_desde_revit.py` (aplica `mapeo_revit` a intermedios Revit) | depende: — | estado: pendiente
- [ ] T-901 | CL-1 | Revisar cada entrega de Ola 1 contra schema y fuente; aprobar/rechazar | depende: tareas de Ola 1 | estado: pendiente

## Ola 2 · Cuantificación
- [ ] T-302 | CL-1 | Generadores v01 por capítulo (02–07) | depende: T-102…T-106, T-204 | estado: pendiente
- [ ] T-303 | CL-1 | Generadores v01 de instalaciones (08–10) y sin Revit (01, 14) | depende: T-106, T-107, T-204 | estado: pendiente
- [ ] T-304 | CL-1 | `Generadores/Generadores_v01.xlsx` impresión Carta | depende: T-302, T-303 | estado: pendiente
- [ ] T-206 | AG-2 | Cerrar precios faltantes de las claves con cantidad; `catalogo_v02.json` si v01 ya fue aprobado | depende: T-205, T-302 | estado: pendiente

## Ola 3 · Presupuesto y calendario
- [ ] T-403 | CX-1 | Presupuesto v01: cantidades + CD + sobrecosto → `presupuesto_v01.json` y `Presupuesto/Presupuesto_v01.xlsm` | depende: T-304, T-205, T-402 | estado: pendiente
- [ ] T-503 | CX-2 | Calendario v01 con importes y avance financiero → `Calendario/Calendario_v01.xlsx` | depende: T-403, T-502 | estado: pendiente

## Ola 4 · Integración
- [ ] T-902 | CL-1 | QA cruzado (`90_qa_cruzado.py`): Σ generadores = cantidades del presupuesto; Σ calendario = subtotal; 100 % por actividad | depende: T-403, T-503 | estado: pendiente
- [ ] T-903 | CL-1 | Consolidar `Resultados/*_v01` + copia fechada en `Resultados/revisiones/` | depende: T-902 | estado: pendiente
