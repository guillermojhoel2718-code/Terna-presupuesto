# CL-1 · Estado
Última actualización: 26-11-2026 23:13 · Equipo: PC-A (worktree Deska `trabajo-en-paralelo-memo`)
Tarea actual: **OLAS 1–4 COMPLETADAS** — Todos los entregables validados, QA cruzado OK y consolidados en `Resultados/`

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-000 | aprobada | specs, schemas, harness | OK |
| T-301..T-304 | aprobada | `generadores_v02.json`, `Generadores/Generadores_v02.xlsx` | OK `validar.py generadores` (65 claves; 14 hojas Carta) |
| T-901 | aprobada | `_harness/cola.md`, `_harness/preguntas.md` | OK (AG-1, AG-2, CX-1, CX-2 aprobados) |
| T-902 | aprobada | `Scripts/90_qa_cruzado.py` | OK (código 0: cantidades, importes, 100% calendario y 20/20 hojas en Carta) |
| T-903 | aprobada | `Resultados/*`, `Resultados/revisiones/26-11-2026/*` | OK |

## Resumen financiero consolidado (v01/v02 · 63 partidas con cantidad)
- **Costo directo:** `$14,682,580.51` MXN
- **Factor de sobrecosto (12 meses, `D25-00_Sobrecosto`):** `1.389012` (`+38.90%`)
- **Subtotal (Precio de venta sin IVA):** `$20,394,278.87` MXN (= `total_importe` de `Calendario_v02.xlsx`)
- **IVA (16%):** `$3,263,084.62` MXN
- **Gran Total:** **`$23,657,363.49` MXN**

## Entregables en `Resultados/` (y `Resultados/revisiones/26-11-2026/`)
- `Generadores_v02.xlsx`
- `Presupuesto_v01.xlsm`
- `Calendario_v02.xlsx`
- `Catalogo_precios_v02.xlsm` y `Catalogo_precios_v02.xlsx`

## Pendientes opcionales para siguiente iteración
- Copiar `Resultados/` y scripts nuevos hacia la carpeta principal de OneDrive (`main`).
- Si se desea ampliar el presupuesto de 63 a las 107 partidas de `catalogo_v02.json`, regenerar `Generadores_v03.xlsx` desde `catalogo_v02.json` y volver a correr CX-1/CX-2.
- `P-010`: 2 partidas de muebles sanitarios (`ED-09-02-001`, `ED-09-02-002`) pendientes de cargar `Bloque de baños_vinculo.rvt` en Revit.
