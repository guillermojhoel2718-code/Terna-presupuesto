# AG-2 · Estado
Última actualización: 26-11-2026 22:50 · Equipo: PC-B
Tarea actual: T-201 a T-206 completadas (`lista para revisión`)

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-201 | lista para revisión | `_harness/intermedios/pdf/tabulador_cdmx_2026.txt`, `_harness/intermedios/pdf/tabulador_cdmx_indice.json` | OK (358 páginas extraídas e indexados **5,477 conceptos** del Tabulador CDMX Septiembre 2026; 36/36 precios verificados por CL-1) |
| T-202 | aprobada | `_harness/intermedios/pdf/01 PRESUPUESTO.txt`, `02 PRECIOS UNITARIOS.txt`, `03 BÁSICOS.txt`, `05 SALARIOS.txt`, `08 COSTOS HORARIOS.txt`, `PRESUPUESTO CENTRO DE INVESTIGACION XALAPA_MUÑOZ.txt` | OK (Aprobada por CL-1 en `cola.md`) |
| T-203 | aprobada | `_harness/intermedios/precios/insumos_norm.json` | OK (12,200 insumos únicos deduplicados de 24,400 filas CSV; aprobada por CL-1 en `cola.md`) |
| T-204 | lista para revisión | `_harness/intermedios/precios/catalogo_v01.json`, `_harness/intermedios/precios/catalogo_v02.json` | OK (`validar.py precios` -> código 0 en `v01` y `v02`; `mapeo_revit` corregido conforme a `D-019`, `revit/indice.json` y `notas_doble_conteo_muros.md` P-011: Cap. 05 mapeado a `Walls` de `Edificio de educacion` y `TT_ED_EDUCACIÓN_CANCELERIA_2027` sin usar `ARQ-MOB` ni `CurtainWallPanels`; **0 duplicados** en `30_generadores_desde_revit.py`) |
| T-205 | lista para revisión | `_harness/intermedios/precios/catalogo_v01.json`, `Catalogo de precios/Catalogo_precios_v01.xlsx` | OK (`v01`: 65 conceptos = **36 `TABULADOR_CDMX`** + **25 `APU`** + **4 `SUPUESTO`** conservadores justificados; `sin_precio = 0`) |
| T-206 | lista para revisión | `_harness/intermedios/precios/catalogo_v02.json`, `Catalogo de precios/catalogo_v02.json`, `Catalogo de precios/Catalogo_precios_v02.xlsm`, `Catalogo de precios/Catalogo_precios_v02.xlsx`, `Catalogo de precios/resumen_catalogo_v02.md` | OK (`v02`: **107 conceptos** = **47 `TABULADOR_CDMX`** + **53 `APU`** + **7 `SUPUESTO`** conservadores justificados; `sin_precio = 0`; **82 conceptos cuantificados directo desde Revit con 0 elementos duplicados**; plantilla XLSM + hojas estilo Neodata `01 PRESUPUESTO` y `02 PRECIOS UNITARIOS`) |

## Preguntas nuevas
- *(Ninguna — todas las observaciones de CL-1 sobre T-204, T-205 y T-206 quedaron atendidas en `catalogo_v01.json` y `catalogo_v02.json`)*

## Resumen del Catálogo (`catalogo_v01` y `catalogo_v02`)
- **Alcance**: Edificio de educación (~2,500 m², 6 vínculos del modelo federado, `D-001`, `D-010`).
- **Capítulos 11 y 12**: 0 conceptos (`D-016`).
- **Capítulo 05 (Albañilería)**: Mapeado exclusivamente a la categoría anfitriona `Walls` de `Edificio de educacion` (`NOVABLOCK` 1,337.95 m² y `Celosia Exterior` 46.48 m²) y `TT_ED_EDUCACIÓN_CANCELERIA_2027` (`Ladrillo cara vista 15 CM` 1,040.43 m² y `Muro 100 mm AAC COM` 7.22 m²), eliminando el mapeo a `TT-ED-EDU-ARQ-MOB` y excluyendo `CurtainWallPanels` conforme a `D-019` y `notas_doble_conteo_muros.md` (`P-011`).
- **Claves sin precio (`sin_precio`)**: **0** (`[]`) tanto en `catalogo_v01.json` como en `catalogo_v02.json`.
- **Desglose de fuentes en `catalogo_v01.json` (65 conceptos)**:
  - `TABULADOR_CDMX`: **36** conceptos (P.U. tomado directo como Costo Directo sin conversión conforme a `D-011`).
  - `APU`: **25** conceptos (insumos de `insumos_norm.json` + rendimientos Neodata `02`/`03`/`05`/`08`, validados contra Xalapa y `01 PRESUPUESTO.pdf`).
  - `SUPUESTO`: **4** conceptos (`ED-01-03-001`, `ED-08-03-001`, `ED-09-03-002`, `ED-10-05-001`).
  - Cobertura Revit en `30_generadores_desde_revit.py`: **47 generadores con cantidad directa de Revit** (subió de 23 a 47 tras ajustar `mapeo_revit` a `revit/indice.json`), **0 duplicados**.
- **Desglose de fuentes en `catalogo_v02.json` (107 conceptos ampliados para el edificio de ~2,500 m²)**:
  - `TABULADOR_CDMX`: **47** conceptos.
  - `APU`: **53** conceptos.
  - `SUPUESTO`: **7** conceptos conservadores justificados:
    1. `ED-01-03-001` (`$1,850.00/m2`): Bodega y oficina provisional de obra.
    2. `ED-01-03-003` (`$18,500.00/lote`): Señalamiento preventivo, protección colectiva y sanitarios portátiles de obra.
    3. `ED-08-03-001` (`$38,500.00/jgo`): Sistema de captación, filtrado de primeras lluvias y cisterna prefabricada equipada.
    4. `ED-08-03-002` (`$64,800.00/pza`): Módulo de cisterna subterránea de concreto armado f'c=250 kg/cm2 impermeable (capacidad total 76,000 L en 4 módulos).
    5. `ED-09-03-002` (`$28,900.00/pza`): Biodigestor autolimpiable anaerobio prefabricado de 7,000 L (`TOL-7000L`).
    6. `ED-10-05-001` (`$132,000.00/jgo`): Sistema solar fotovoltaico interconectado a red de 10.0 kWp (18 módulos 550 Wp + inversor trifásico 10 kW).
    7. `ED-14-01-003` (`$24,500.00/lote`): Retiro final de escombro en camión, limpieza de áreas exteriores y carpeta As-Built.
  - Cobertura Revit en `30_generadores_desde_revit.py`: **82 generadores con cantidad directa de Revit** y **0 elementos duplicados** (los 25 restantes son partidas preliminares, terracerías, acarreos, muebles sanitarios del vínculo `Bloque de baños` no cargado en P-010, sistema fotovoltaico y limpieza final).

## Hecho
- Atendidas las observaciones de CL-1 en `_harness/cola.md` sobre **T-204, T-205 y T-206**:
  - Corregido el conteo en este status (`v01`: 36 `TABULADOR_CDMX` + 25 `APU` + 4 `SUPUESTO` = 65; `v02`: 47 `TABULADOR_CDMX` + 53 `APU` + 7 `SUPUESTO` = 107).
  - Eliminado el mapeo obsoleto de muros del Cap. 05 a `TT-ED-EDU-ARQ-MOB` (`D-017` superada por `D-019`) y aplicado el filtro exacto de `notas_doble_conteo_muros.md` (`P-011`).
  -Separadas las conexiones hidráulicas (`ED-08-01-003`, filtro `Domestic[_ ]Cold[_ ]Water`) de las sanitarias (`ED-09-01-003`, filtro `· (Sanitary|Undefined) ·`) eliminando al 100% los duplicados en `PipeFittings`.
- Ampliado el catálogo a **`catalogo_v02`** (107 conceptos) agregando partidas de preliminares, cimentación (afine, trabes de cimentación, dalas de desplante, impermeabilización capilar, acarreo subsecuente), estructura (castillos, dalas de cerramiento, vigueta T 12×20, bovedilla 63×20×20), estructura metálica y cubierta (bastidor 10×40 cm de cubierta, losa azotea 150 mm), albañilería (celosía exterior, muros AAC 100 mm, chaflanes), acabados/carpintería/exteriores (concreto pulido densificado, porcelanato Tavola Noce Mate 20×120, piso exterior suspendido, tierra vegetal en jardineras, lambrín de madera, plafón Armstrong MetalWorks Mesh, plafón cerámico húmedo), herrería/cancelería/carpintería (puertas interiores de madera, puertas corredizas, mullions de aluminio, escalera metálica principal), instalaciones IHS/eléctricas (mangueras flexibles, registros de válvulas, cisternas de concreto armado, conduit iluminación, cajas conduit, curvas de charola, cables THW-LS iluminación y potencia, luminarias de pared), mobiliario (pizarrones 144×48", maceteros y accesorios de estación) y limpieza exterior/retiro final.
- Completada la plantilla en `Catalogo de precios/Catalogo_precios_v02.xlsm` (copia de `Resources/plantillas_para_usar/Taller Terminal_Presupuesto.xlsm` con `keep_vba=True` y correcciones `SPEC_06`/`SPEC_07`) y `Catalogo de precios/Catalogo_precios_v02.xlsx`, incluyendo las hojas con formato visual estilo Neodata (`Neodata_01_Catalogo`, `Neodata_02_Matrices_APU` y `Tabulador_y_Supuestos`).

## Pendiente
- En espera de revisión y aprobación de `catalogo_v01.json` y `catalogo_v02.json` por CL-1 para desbloquear T-302/T-303/T-403.

## Siguiente paso
CL-1 corre `Scripts/30_generadores_desde_revit.py` con `catalogo_v02.json` (o `catalogo_v01.json`) para generar `generadores_v01.json` y `Generadores/Generadores_v01.xlsx`.

## Archivos tocados
- `Scripts/20_procesar_fuentes_precios.py`
- `Scripts/21_catalogo_cap01_06.py`
- `Scripts/22_catalogo_cap07_14.py`
- `Scripts/23_construir_catalogo_precios.py`
- `Scripts/24_conceptos_adicionales_v02.py`
- `Scripts/25_generar_catalogo_v02_excel_neodata.py`
- `_harness/intermedios/pdf/tabulador_cdmx_2026.txt`
- `_harness/intermedios/pdf/tabulador_cdmx_indice.json`
- `_harness/intermedios/precios/insumos_norm.json`
- `_harness/intermedios/precios/catalogo_v01.json`
- `_harness/intermedios/precios/catalogo_v02.json`
- `Catalogo de precios/catalogo_v01.json`
- `Catalogo de precios/catalogo_v02.json`
- `Catalogo de precios/resumen_catalogo_v01.md`
- `Catalogo de precios/resumen_catalogo_v02.md`
- `Catalogo de precios/Catalogo_precios_v01.xlsx`
- `Catalogo de precios/Catalogo_precios_v02.xlsx`
- `Catalogo de precios/Catalogo_precios_v02.xlsm`
- `_harness/status/AG-2.md`
- `_harness/logs/AG-2-23-11-2026.md`
- `_harness/logs/AG-2-26-11-2026.md`
