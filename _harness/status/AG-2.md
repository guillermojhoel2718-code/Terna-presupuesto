# AG-2 · Estado
Última actualización: 23-11-2026 02:57 · Equipo: PC-B
Tarea actual: T-206 (en espera de T-302 / `revit/indice.json` de AG-1)

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-201 | bloqueada | _harness/intermedios/pdf/tabulador_cdmx_indice.json | Bloqueada: no existe `tabulador-general-...-septiembre-2026.pdf` en `Resources/referencias_docs/` (solo está el PDF de Xalapa). Se dejó índice placeholder (`disponible: false`) y se resolvió T-205 con APU Neodata + insumos `precios_procesados` + validación Xalapa/01 PRESUPUESTO |
| T-202 | lista para revisión | _harness/intermedios/pdf/01 PRESUPUESTO.txt, 02 PRECIOS UNITARIOS.txt, 03 BÁSICOS.txt, 05 SALARIOS.txt, 08 COSTOS HORARIOS.txt, PRESUPUESTO CENTRO DE INVESTIGACION XALAPA_MUÑOZ.txt | OK (9 PDFs extraídos con marcas `=== PAGINA N ===`) |
| T-203 | lista para revisión | _harness/intermedios/precios/insumos_norm.json | OK (12,200 insumos únicos deduplicados de 24,400 filas CSV; unidades normalizadas con `common.normalizar_unidad`) |
| T-204 | lista para revisión | _harness/intermedios/precios/catalogo_v01.json | OK (`py Scripts/schemas/validar.py precios _harness/intermedios/precios/catalogo_v01.json` -> código 0; 65 conceptos `ED-CC-SS-NNN` en caps. 01-10, 13 y 14; 0 en 11-12 por D-016; cap. 05 mapeado a `TT-ED-EDU-ARQ-MOB` por D-017) |
| T-205 | lista para revisión | _harness/intermedios/precios/catalogo_v01.json | OK (65/65 conceptos con Costo Directo MXN validado; 61 `APU` + 4 `SUPUESTO` conservadores justificados; 0 `sin_precio`) |
| T-206 | bloqueada | _harness/intermedios/precios/catalogo_v02.json | En espera de T-302 (`generadores_v01.json` de CL-1) y/o `_harness/intermedios/revit/indice.json` de AG-1 para ajuste fino de `mapeo_revit` o claves nuevas |

## Preguntas nuevas
- [23-11-2026] ¿Se agregará el archivo `tabulador-general-...-septiembre-2026.pdf` en `Resources/referencias_docs/` o se aprueba cerrar T-201/T-205 con las 61 matrices `APU` (`Resources/precios_procesados/` + rendimientos Neodata `02`/`03`/`05`/`08` validados contra `PRESUPUESTO CENTRO DE INVESTIGACION XALAPA_MUÑOZ.pdf` y `01 PRESUPUESTO.pdf`) y los 4 `SUPUESTO` conservadores justificados? · impacto: T-201 y fuente `TABULADOR_CDMX` en T-205 · archivo: `Resources/referencias_docs/` y `_harness/intermedios/precios/catalogo_v01.json` · supuesto: se entregó `catalogo_v01.json` 100% costeado a Costo Directo (`con_precio=65`, `sin_precio=[]`, `supuestos=['ED-01-03-001', 'ED-08-03-001', 'ED-09-03-002', 'ED-10-05-001']`).

## Hecho
- Leídos completos: `CLAUDE.md`, `AGENTS.md`, `HARNESS.md`, `_harness/decisiones.md`, `SPEC_01`, `SPEC_02`, `SPEC_03`, `SPEC_05`, `SPEC_08`, `_harness/status/AG-2.md` y `_harness/cola.md`.
- Ejecutado `Scripts/20_procesar_fuentes_precios.py`:
  - **T-202 (`lista para revisión`)**: extraídos 9 PDFs con `pdfplumber` a `_harness/intermedios/pdf/*.txt`.
  - **T-203 (`lista para revisión`)**: deduplicados 24,400 registros CSV en **12,200 insumos únicos** con unidades normalizadas en `_harness/intermedios/precios/insumos_norm.json`.
  - **T-201 (`bloqueada`)**: generado `_harness/intermedios/pdf/tabulador_cdmx_indice.json` (`disponible: false`) por ausencia del PDF del tabulador CDMX 2026 en `Resources/referencias_docs/`.
- Creados y ejecutados `Scripts/21_catalogo_cap01_06.py`, `Scripts/22_catalogo_cap07_14.py` y `Scripts/23_construir_catalogo_precios.py`:
  - **T-204 y T-205 (`lista para revisión`)**: construido `_harness/intermedios/precios/catalogo_v01.json` (65 conceptos en capítulos `01` a `10`, `13` y `14`; capítulos `11` y `12` sin conceptos por `D-016`; muros de albañilería cap. `05` mapeados a `TT-ED-EDU-ARQ-MOB` por `D-017`), además de `Catalogo de precios/catalogo_v01.json`, `Catalogo de precios/resumen_catalogo_v01.md` y `Catalogo de precios/Catalogo_precios_v01.xlsx`.
  - Validado exitosamente con `py Scripts/schemas/validar.py precios _harness/intermedios/precios/catalogo_v01.json` (`OK`).

## Pendiente
- **T-206 (Ola 2)**: cuando AG-1 publique `_harness/intermedios/revit/indice.json` y/o CL-1 ejecute T-302 (`generadores_v01.json`), ajustar `mapeo_revit` a las familias/tipos exactos extraídos de Revit o agregar claves faltantes en `catalogo_v02.json`.

## Siguiente paso
Esperar la publicación de `_harness/intermedios/revit/indice.json` (AG-1) y la revisión de `catalogo_v01.json` / `generadores_v01.json` (CL-1 en T-302) para ejecutar T-206.

## Archivos tocados
- `Scripts/20_procesar_fuentes_precios.py`
- `Scripts/21_catalogo_cap01_06.py`
- `Scripts/22_catalogo_cap07_14.py`
- `Scripts/23_construir_catalogo_precios.py`
- `_harness/intermedios/pdf/tabulador_cdmx_indice.json`
- `_harness/intermedios/pdf/01 PRESUPUESTO.txt`
- `_harness/intermedios/pdf/02 PRECIOS UNITARIOS.txt`
- `_harness/intermedios/pdf/03 BÁSICOS.txt`
- `_harness/intermedios/pdf/05 SALARIOS.txt`
- `_harness/intermedios/pdf/08 COSTOS HORARIOS.txt`
- `_harness/intermedios/pdf/09 RELACIÓN MAQUINARIA.txt`
- `_harness/intermedios/pdf/10 RELACIÓN MANO DE OBRA.txt`
- `_harness/intermedios/pdf/11 RELACIÓN MATERIALES.txt`
- `_harness/intermedios/pdf/PRESUPUESTO CENTRO DE INVESTIGACION XALAPA_MUÑOZ.txt`
- `_harness/intermedios/pdf/PRESUPUESTO_XALAPA.txt`
- `_harness/intermedios/precios/insumos_norm.json`
- `_harness/intermedios/precios/catalogo_v01.json`
- `Catalogo de precios/catalogo_v01.json`
- `Catalogo de precios/resumen_catalogo_v01.md`
- `Catalogo de precios/Catalogo_precios_v01.xlsx`
- `_harness/status/AG-2.md`
- `_harness/logs/AG-2-23-11-2026.md`
