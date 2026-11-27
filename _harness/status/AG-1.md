# AG-1 · Estado
Última actualización: 26-11-2026 22:41 · Equipo: PC-B (`MEMO`)
Tarea actual: **LISTO PARA GENERADORES** — Consolidado por categoría, nivel y tipo publicado en `_harness/intermedios/revit/resumen_por_categoria_y_nivel.json` y `resumen_por_categoria_y_nivel.md` (superficie reconciliada ~2,500 m²); huecos marcados como preguntas `P-013` a `P-016` en `_harness/preguntas.md` (más `P-010` pendiente de sub-vínculo de baños).

## Tareas
| Tarea | Estado | Intermedio | Fecha | Validado |
|---|---|---|---|---|
| T-101 | aprobada | `_harness/intermedios/revit/indice.json` + `notas_doble_conteo_muros.md` + `resumen_por_categoria_y_nivel.{json,md}` | 26-11-2026 | OK (Aprobada por CL-1; 6 vínculos, 59 JSON + resumen consolidado por categoría y nivel para generadores) |
| T-102 | aprobada | `_harness/intermedios/revit/Edificio de educacion__*.json` (9 archivos, 15,740 elem.) | 23-11-2026 | OK (Aprobada por CL-1; `validar.py revit` 9/9 + análisis P-011 y cimentación) |
| T-103 | aprobada | `_harness/intermedios/revit/TT-ED-EDU-ARQ-MOB__*.json` (4 archivos, 607 elem.) | 23-11-2026 | OK (Aprobada por CL-1; `validar.py revit` 4/4; solo mobiliario/equipo, D-019) |
| T-104 | aprobada | `_harness/intermedios/revit/Proyecto acabado-DAMIAN__*.json` (3 archivos, 70 elem.) | 23-11-2026 | OK (Aprobada por CL-1; `validar.py revit` 3/3; pisos, muros y plafones) |
| T-105 | aprobada | `_harness/intermedios/revit/TT_ED_EDUCACIÓN_CANCELERIA_2027__*.json` (11 archivos, 1,623 elem.) | 23-11-2026 | OK (Aprobada por CL-1; `validar.py revit` 11/11; puertas, ventanas, muros cortina, barandales, muros ladrillo y perfiles acero) |
| T-106 | lista para revisión | `_harness/intermedios/revit/Instalaciones__*.json` (7 archivos, 727 elem.) | 23-11-2026 | OK `validar.py revit` (7/7; 0 duplicados en `catalogo_v01.json` actual; pendiente re-extracción solo si el usuario carga `Bloque de baños_vinculo.rvt`, P-010) |
| T-107 | aprobada | `_harness/intermedios/revit/Proyecto electrico_corregido__*.json` (25 archivos, 2,247 elem.) | 23-11-2026 | OK (Aprobada por CL-1; `validar.py revit` 25/25) |

## Consolidación por Categoría y Nivel Lista para Generadores (`~2,500 m²`)
- **Archivos entregados**:
  - `_harness/intermedios/revit/resumen_por_categoria_y_nivel.json`
  - `_harness/intermedios/revit/resumen_por_categoria_y_nivel.md`
  - `MCP Revit/resumen_por_categoria_y_nivel.md`
  - `Scripts/18_consolidar_resumen_revit.py` (idempotente, escritura atómica `.tmp` → `os.replace`).
- **Reconciliación de superficie construida (~2,500 m², D-010)**:
  - **Huella horizontal estructural**: PB Firme estructural 10 cm (`804.09 m²`, plantilla 5 cm = `804.20 m²`) + PA Losa de vigueta y bovedilla 25 cm (`753.11 m²`) + AZ Losa `Generic 150mm` en Cancelería (`1,113.73 m²`) = **`2,670.94 m²`** (o PB Firme + PA Losa + Cubierta inclinada `367.06 m²` = `1,924.27 m²`).
  - **Huella de pisos acabados + cubierta**: Pisos terminados PB (`1,238.77 m²`) + Pisos terminados PA (`323.17 m²` en Acabados + `596.50 m²` Porcelanato en Cancelería = `919.67 m²`) + Cubierta inclinada (`367.06 m²`) = **`2,525.51 m²`** (cuadra con los **~2,500 m²** oficiales de `D-010`).
- **Verificación contra `Scripts/30_generadores_desde_revit.py` y `catalogo_v01.json` actualizado**:
  - **47 de 65 conceptos** ya reciben cantidad directa desde los 59 JSON de Revit con **0 elementos duplicados** (`Duplicados: 0`; incluso la separación de conexiones hidráulicas `ED-08-01-003` = 167 pzas vs sanitarias `ED-09-01-003` = 146 pzas ya da 0 duplicados).
  - Para los **18 conceptos restantes** (2 de muebles sanitarios por `P-010` + 16 conceptos `sin_cantidad_revit: true`), el resumen incluye la tabla `cantidades_derivadas_para_manual_json` con las cantidades base calculadas desde dimensiones de Revit listas para `manual.json`.

## Preguntas nuevas (Huecos detectados y registrados en `_harness/preguntas.md`)
- **P-010** *(se mantiene abierta)*: Sub-vínculo `Bloque de baños_vinculo.rvt` está `Unloaded` en `Instalaciones.rvt` (0 WC, 0 lavabos, 0 mingitorios; solo 14 registros y 3 biodigestores).
- **P-013** | `[AG-1] [26-11-2026]` 10 tramos cortos de concreto en `Edificio de educacion__StructuralFraming.json` (1 `Trabe de cimentacion 20x40` `#552895` de `L=0.15 m` y 9 `Dala de cerramiento 15x25` que suman `L=3.49 m`) tienen `volumen_m3 = null` y `area_m2 = null` en Revit por recortes de unión, generando los 32 avisos en `Scripts/30_generadores_desde_revit.py` · impacto: cap. 02 y 03 (< 0.2% del volumen; los 334 tramos restantes suman `84.38 m³`, idéntico al schedule de Revit) · supuesto: conservar `null` fiel al modelo e ignorar los 32 avisos.
- **P-014** | `[AG-1] [26-11-2026]` 587 montantes `Montante rectangular - 10 x 40 cm` (`883.52 m`, `31.12 m³`, `peso_kg: null`) en `Edificio de educacion__CurtainWallMullions.json` (cubierta `Curtain Wall | Cubierta`) quedan sin asignar en `catalogo_v01.json`, mientras `ED-04-01-001` suma `4,461.02 kg` de los 36 perfiles de acero de Cancelería y `ED-04-01-004` (pintura acero) tiene `sin_cantidad_revit: true` · impacto: cap. 04 · supuesto: `ED-04-01-001` y `ED-04-01-004` operan con `4,461.02 kg` mientras se confirma si los 883.52 m de montantes llevan factor kg/m.
- **P-015** | `[AG-1] [26-11-2026]` En `Proyecto acabado-DAMIAN__Floors.json` hay 13 plafones modelados como `Floors` (`1,050.45 m²`, de los cuales 12 son `PF_Plafon ACT` = `1,023.22 m²`) además de los 3 plafones en `Ceilings.json` (`1,125.08 m²`), sumando `2,148.30 m²` en `ED-06-03-001` · impacto: cap. 06 · supuesto: se reportan desglosados por categoría (`Floors` vs `Ceilings`) y nivel en `resumen_por_categoria_y_nivel.md`.
- **P-016** | `[AG-1] [26-11-2026]` 16 claves `sin_cantidad_revit: true` requieren captura en `_harness/intermedios/generadores/manual.json` · impacto: caps. 01, 02, 04, 05, 06, 10 y 14 · supuesto: publicadas en `resumen_por_categoria_y_nivel.json` (`cantidades_derivadas_para_manual_json`) y `.md` (§5) las 16 cantidades derivadas de la geometría Revit listas para usar en `manual.json`.

## Hecho
- **T-101 a T-105 y T-107 aprobadas por CL-1** (59/59 extracciones válidas por schema + `notas_doble_conteo_muros.md` para P-011).
- **Consolidación Ciclo 3 (`26-11-2026`)**: Creado y ejecutado `Scripts/18_consolidar_resumen_revit.py`, generando `_harness/intermedios/revit/resumen_por_categoria_y_nivel.json` y `_harness/intermedios/revit/resumen_por_categoria_y_nivel.md` con:
  1. Reconciliación de superficie construida (~2,500 m², D-010) por nivel canónico.
  2. Tabla global por nivel canónico unificado (excluyendo paneles duplicados de Estructura, P-011).
  3. Resumen de las 59 extracciones por vínculo, categoría y nivel, más desglose completo por `(modelo, categoría, nivel, familia, tipo, material_principal)` en JSON idéntico al agrupador de `Scripts/30_generadores_desde_revit.py`.
  4. Huecos marcados como preguntas (`P-013` a `P-016` agregadas con lock en `_harness/preguntas.md` y en este status) y tabla de 16 cantidades derivadas para `manual.json`.

## Pendiente
- **P-010 (IHS)**: Re-extraer `Instalaciones.rvt` (T-106) únicamente si el usuario carga el sub-vínculo `Bloque de baños_vinculo.rvt` en Revit del PC-B.

## Siguiente paso
CL-1 ejecuta `Scripts/30_generadores_desde_revit.py` (`T-302`, `T-303`, `T-304`) apoyándose en `_harness/intermedios/revit/resumen_por_categoria_y_nivel.{json,md}` y en las cantidades derivadas para `manual.json`.

## Archivos tocados
- `Scripts/18_consolidar_resumen_revit.py`
- `_harness/intermedios/revit/resumen_por_categoria_y_nivel.json`
- `_harness/intermedios/revit/resumen_por_categoria_y_nivel.md`
- `MCP Revit/resumen_por_categoria_y_nivel.md`
- `_harness/preguntas.md`
- `_harness/status/AG-1.md`
- `_harness/logs/AG-1-23-11-2026.md`
