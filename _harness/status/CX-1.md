# CX-1 · Estado
Última actualización: 26-11-2026 23:10 · Equipo: PC-B
Tarea actual: T-401..T-403 completadas, listas para revisión de CL-1

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-401 | lista para revisión | `Presupuesto/Presupuesto_v00_base.xlsm` | OK: copia con VBA, defectos SPEC_06 corregidos, Carta explícita y recálculo Excel COM verificado |
| T-402 | lista para revisión | `Scripts/40_llenar_plantilla_presupuesto.py`, `Scripts/41_recalcular_presupuesto.ps1`, `Presupuesto/_T402_salida_temporal.xlsm` | OK: prueba sintética marcada de 2 partidas; intermedio de prueba válido contra schema; iteración de sobrecosto por COM |
| T-403 | lista para revisión | `Presupuesto/Presupuesto_v01.xlsm`, `_harness/intermedios/presupuesto/presupuesto_v01.json` | OK: 63 partidas trazables; schema Pydantic OK; suma CD y venta conciliadas con libro; macros y Carta verificados |

## Hecho
- T-401: plantilla copiada a `Presupuesto/Presupuesto_v00_base.xlsm`, sin modificar la fuente. Corregidos `Q9`, `AW11=12`, nombre y superficie del proyecto, `02_Ref_Datos!D9`, texto de obra y los 14 capítulos; las hojas quedan en Carta.
- T-402: implementado el generador JSON → jerarquía/renglones/resumen y el helper de recálculo/lectura con Excel COM. Probado con `Presupuesto/Presupuesto_v00_prueba.xlsm` y su JSON sintético marcado; validación de salida OK. El factor alto de esa prueba corresponde al CD sintético de $2,500 frente a los montos fijos de la plantilla; el resultado de prueba no es presupuesto de obra.
- El generador rechaza sobrescribir una versión de presupuesto ya aprobada; para nuevos intermedios detecta y valida la última versión de Generadores y catálogo aprobada.
- T-403: tras la aprobación de CL-1 en `cola.md` para T-302/T-303/T-304 y T-205/T-206, se usaron `generadores_v02.json` y `catalogo_v02.json` (la tarea de presupuesto entrega v01). Se excluyeron `ED-09-02-001` y `ED-09-02-002`, marcadas `claves_sin_cantidad` por P-010.
- Presupuesto v01: costo directo $14,682,580.51; factor de sobrecosto 1.3890118871 leído por iteración de la plantilla; subtotal $20,394,278.87; IVA $3,263,084.62; total $23,657,363.49.
- Verificación: `python Scripts/schemas/validar.py presupuesto _harness/intermedios/presupuesto/presupuesto_v01.json` → OK. Se comprobó que cada clave presupuestada coincide con el intermedio, tiene fuente en columna I y cuadra con cantidades, P.U. CD, `J16`, `L16` y el resumen.
- Excel 16.0 COM calculó y guardó los libros; el cierre está en `finally`. Se conservaron macros y se verificaron `paperSize=1`, `fitToWidth=1`, `fitToHeight=0` y orientación.

## Pendiente
- Revisión y aprobación de CL-1; no edité `cola.md` porque SPEC_08 reserva ese archivo a CL-1.
- Las dos partidas sanitarias sin cantidad permanecen pendientes por P-010 y no forman parte del presupuesto v01.

## Siguiente paso
CL-1 revisa los 3 entregables de CX-1 y sincroniza sus estados en `cola.md`. CX-2 puede tomar `presupuesto_v01.json` cuando se apruebe.

## Preguntas nuevas
- Ninguna agregada. P-010 continúa bajo coordinación de CL-1.

## Archivos tocados
- `Scripts/40_llenar_plantilla_presupuesto.py`
- `Scripts/41_recalcular_presupuesto.ps1`
- `Presupuesto/Presupuesto_v00_base.xlsm`
- `Presupuesto/_T402_salida_temporal.xlsm`, `Presupuesto/_T402_intermedio_temporal.json`
- `Presupuesto/Presupuesto_v01.xlsm`
- `_harness/intermedios/presupuesto/presupuesto_v01.json`
- `_harness/status/CX-1.md`
- `_harness/logs/CX-1-26-11-2026.md`
