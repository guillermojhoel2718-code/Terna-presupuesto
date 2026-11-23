# AG-2 · Estado
Última actualización: 23-11-2026 02:25 · Equipo: PC-B
Tarea actual: T-204

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-201 | bloqueada | _harness/intermedios/pdf/tabulador_cdmx_indice.json | Bloqueada: no existe `tabulador-general-...-septiembre-2026.pdf` en `Resources/referencias_docs/` (solo está el PDF de Xalapa). Se generó índice vacío y se avanza con esquema mixto (APU Neodata + insumos `precios_procesados` + validación Xalapa/01 PRESUPUESTO) |
| T-202 | lista para revisión | _harness/intermedios/pdf/01 PRESUPUESTO.txt, 02 PRECIOS UNITARIOS.txt, 03 BÁSICOS.txt, 05 SALARIOS.txt, 08 COSTOS HORARIOS.txt, PRESUPUESTO CENTRO DE INVESTIGACION XALAPA_MUÑOZ.txt | OK (9 PDFs extraídos con marcas `=== PAGINA N ===`) |
| T-203 | lista para revisión | _harness/intermedios/precios/insumos_norm.json | OK (12,200 insumos únicos deduplicados de 24,400 filas CSV; unidades normalizadas con `common.normalizar_unidad`) |
| T-204 | en curso | _harness/intermedios/precios/catalogo_v01.json | En construcción desde memoria arquitectónica (§4–§10) y SPEC_02 |
| T-205 | pendiente | _harness/intermedios/precios/catalogo_v01.json | — |

## Preguntas nuevas
- [23-11-2026] ¿Se agregará el archivo `tabulador-general-...-septiembre-2026.pdf` en `Resources/referencias_docs/` o se autoriza cerrar T-201/T-205 usando exclusivamente APU (`Resources/precios_procesados/` + rendimientos de PDFs Neodata y validación contra `PRESUPUESTO CENTRO DE INVESTIGACION XALAPA_MUÑOZ.pdf` / `01 PRESUPUESTO.pdf`)? · impacto: T-201 y fuente `TABULADOR_CDMX` en T-205 · archivo: `Resources/referencias_docs/` y `_harness/intermedios/precios/catalogo_v01.json` · supuesto: mientras no esté el PDF del tabulador CDMX 2026 en `Resources/referencias_docs/`, todos los conceptos de `catalogo_v01.json` se calculan mediante `APU` (insumos de `insumos_norm.json` + rendimientos Neodata/Xalapa) o `SUPUESTO` conservador justificado conforme a D-003 y SPEC_05 §2.

## Hecho
- Leídos completos: `CLAUDE.md`, `AGENTS.md`, `HARNESS.md`, `_harness/decisiones.md`, `SPEC_01`, `SPEC_02`, `SPEC_03`, `SPEC_05`, `SPEC_08`, `_harness/status/AG-2.md` y `_harness/cola.md`.
- Creado y ejecutado `Scripts/20_procesar_fuentes_precios.py` (idempotente, escritura atómica `.tmp` y locks locales en `_harness/locks/`).
- T-202 completada: extraídos a `_harness/intermedios/pdf/` los textos por página (`=== PAGINA N ===`) de `01 PRESUPUESTO.pdf` (9 págs.), `02 PRECIOS UNITARIOS.pdf` (30 págs.), `03 BÁSICOS.pdf` (36 págs.), `05 SALARIOS.pdf` (1 pág.), `08 COSTOS HORARIOS.pdf` (8 págs.), `09 RELACIÓN MAQUINARIA.pdf` (1 pág.), `10 RELACIÓN MANO DE OBRA.pdf` (1 pág.), `11 RELACIÓN MATERIALES.pdf` (3 págs.) y `PRESUPUESTO CENTRO DE INVESTIGACION XALAPA_MUÑOZ.pdf` (432 págs.).
- T-203 completada: deduplicados por `codigo` los 3 CSV de `Resources/precios_procesados/` (`catalogo_apuc_mvp.csv`, `insumos_apuc_norm.csv`, `ppto_reftab_apuc_norm.csv` con `utf-8-sig`) y normalizadas sus unidades (`ml` → `m`, etc.) con `Scripts/schemas/common.py` → `_harness/intermedios/precios/insumos_norm.json` (12,200 insumos únicos de 24,400 filas).

## Pendiente
- T-204: estructurar catálogo de conceptos `catalogo_v01.json` para los capítulos 01 a 14 (excepto 11 y 12 reservados sin conceptos por D-016; cap. 05 mapeado a `TT-ED-EDU-ARQ-MOB` por D-017).
- T-205: integrar costos directos unitarios (`APU` y `SUPUESTO` conservador justificado) en `catalogo_v01.json`, exportar catálogo en `Catalogo de precios/` y validar con `py Scripts/schemas/validar.py precios _harness/intermedios/precios/catalogo_v01.json`.

## Siguiente paso
Escribir y ejecutar `Scripts/21_construir_catalogo_precios.py` para generar `_harness/intermedios/precios/catalogo_v01.json` (T-204 y T-205) y validarlo contra el schema Pydantic.

## Archivos tocados
- `Scripts/20_procesar_fuentes_precios.py`
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
- `_harness/status/AG-2.md`
- `_harness/logs/AG-2-23-11-2026.md`
