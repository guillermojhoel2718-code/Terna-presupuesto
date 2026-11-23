# SPEC 05 · Precios (AG-2), esquema mixto (D-003)

## 1. Qué hay en `Resources/precios_procesados/`

| Archivo | Filas | Contenido | Nota |
|---|---|---|---|
| `catalogo_apuc_mvp.csv` / `.json` | ~12 200 | Insumos APUCMX (`tipo_registro`: material ~6 700, mano_obra ~45, …), fecha 2025-05-16 | Son **insumos**, no conceptos |
| `insumos_apuc_norm.csv` | ~12 050 | Misma base de insumos normalizada | Duplica gran parte del anterior: deduplicar por `codigo` |
| `ppto_reftab_apuc_norm.csv` | 148 | Material eléctrico Dyven CDMX 2023-24 | Útil para cap. 10 |
| `machinery_costs_*.csv` | 3 | Costos horarios CMIC (casi vacío) | Completar con `08 COSTOS HORARIOS.pdf` |

Columnas comunes: `codigo, descripcion, unidad, precio_unitario, categoria, subcategoria, fuente, fecha_fuente, unidad_inferida`. Si `unidad_inferida = True`, verificar la unidad antes de usarla.

## 2. Orden de resolución por concepto

1. **Tabulador CDMX 2026** (`referencias_docs/tabulador-general-...-septiembre-2026.pdf`): si existe un concepto equivalente, usar su P.U. → `fuente_tipo: TABULADOR_CDMX`, `fuente_ref: "clave tabulador · página"`.
2. **`Catalogo de precios/`**, si ya contiene el concepto → `CATALOGO`.
3. **APU** con insumos de `precios_procesados` + rendimientos/cuadrillas de `resultado_ejemplo_neodata/02 PRECIOS UNITARIOS.pdf`, `03 BÁSICOS.pdf`, `05 SALARIOS.pdf`, `08 COSTOS HORARIOS.pdf` → `APU`, con lista `apu[]` y `justificacion` (de qué concepto Neodata se tomó el rendimiento).
4. **Validación**: comparar contra `PRESUPUESTO CENTRO DE INVESTIGACION XALAPA_MUÑOZ.pdf` y `01 PRESUPUESTO.pdf`. Desviación > ±30 % → anotarlo en `justificacion`.
5. **SUPUESTO**: aproximado conservador, no mayor a la referencia más baja disponible, con `justificacion`.

Nunca subir un precio "por seguridad". El P.U. del catálogo es **costo directo** (sin indirectos ni utilidad). Los P.U. del tabulador CDMX **ya son costo directo** (D-011): se usan tal cual, sin conversión.

## 3. Extracción de PDFs

- `pdfplumber`, por página, a `_harness/intermedios/pdf/<nombre>.txt` con marcas `=== PAGINA N ===`. Si el `.txt` ya existe, reutilizarlo.
- El tabulador CDMX es grande: dividir por página y crear un índice `pdf/tabulador_cdmx_indice.json` (`clave → página, descripción, unidad, precio`).

## 4. Catálogo de conceptos

AG-2 define los conceptos de cada capítulo de SPEC_02 con descripción estilo Neodata (`…, incluye: materiales, mano de obra, equipo y herramienta`). Para saber qué existe en el modelo, leer `intermedios/revit/indice.json` cuando AG-1 lo publique; mientras tanto, partir de la memoria (§4 sistema estructural, §5 acabados, §6–10 instalaciones).

Cada concepto con cantidad de Revit lleva `mapeo_revit` (categoría, regex de tipo/material, campo de cantidad).
