# AG-1 · Estado
Última actualización: 23-11-2026 03:12 · Equipo: PC-B (`MEMO`)
Tarea actual: T-101 a T-107 en `lista para revisión`; P-011 resuelto en `_harness/intermedios/revit/notas_doble_conteo_muros.md`; en espera de carga de sub-vínculo `Bloque de baños_vinculo.rvt` (P-010) para re-extraer IHS.

## Tareas
| Tarea | Estado | Intermedio | Fecha | Validado |
|---|---|---|---|---|
| T-101 | lista para revisión | `_harness/intermedios/revit/indice.json` + `notas_doble_conteo_muros.md` | 23-11-2026 | OK (6 vínculos cargados, 59 JSON indexados, 21,014 elementos; validado por CL-1) |
| T-102 | lista para revisión | `_harness/intermedios/revit/Edificio de educacion__*.json` (9 archivos, 15,740 elem.) | 23-11-2026 | OK `validar.py revit` (9/9) + análisis P-011 y cimentación |
| T-103 | lista para revisión | `_harness/intermedios/revit/TT-ED-EDU-ARQ-MOB__*.json` (4 archivos, 607 elem.) | 23-11-2026 | OK `validar.py revit` (4/4; solo mobiliario/equipo, D-019) |
| T-104 | lista para revisión | `_harness/intermedios/revit/Proyecto acabado-DAMIAN__*.json` (3 archivos, 70 elem.) | 23-11-2026 | OK `validar.py revit` (3/3; pisos, muros y plafones) |
| T-105 | lista para revisión | `_harness/intermedios/revit/TT_ED_EDUCACIÓN_CANCELERIA_2027__*.json` (11 archivos, 1,623 elem.) | 23-11-2026 | OK `validar.py revit` (11/11; puertas, ventanas, muros cortina, barandales, muros ladrillo y perfiles acero) |
| T-106 | lista para revisión | `_harness/intermedios/revit/Instalaciones__*.json` (7 archivos, 727 elem.) | 23-11-2026 | OK `validar.py revit` (7/7; pendiente re-extracción cuando usuario cargue `Bloque de baños_vinculo.rvt`, P-010) |
| T-107 | lista para revisión | `_harness/intermedios/revit/Proyecto electrico_corregido__*.json` (25 archivos, 2,247 elem.) | 23-11-2026 | OK `validar.py revit` (25/25; conduits, charolas, cables, luminarias, contactos, tableros) |

## Hallazgos y resolución de P-011 / P-010
1. **P-011 (Doble conteo `Walls` vs `CurtainWallPanels` en `Edificio de educacion.rvt` — RESUELTO)**:
   - Documentado en `_harness/intermedios/revit/notas_doble_conteo_muros.md`.
   - Los **9,931 paneles de block** (`9,930` `NOVABLOCK® (12) H 1 Tercio` + `1` `NOVABLOCK® (12) H`, suma = **1,337.9467 m²**) son el 100% de los paneles hijos (`CurtainGrid.GetPanelIds()`) alojados en los **101 muros `Curtain Wall | NOVABLOCK® (12) H`** (`1,337.9468 m²`, `918.43 m`). Sus `BoundingBoxXYZ` e inventario por nivel (`Nivel +5.30`: 3,335 pzas = 485.05 m²; `Auxiliar +7.65`: 1,332 pzas = 168.71 m²; `N.P.T.`: 3,290 pzas = 478.93 m²; `Auxiliar +11.15`: 1,974 pzas = 205.26 m²) se solapan al 100%.
   - Los otros 536 paneles de `Edificio de educacion__CurtainWallPanels.json` también son hijos de muros cortina de `Walls`: **280 paneles** (`264` `Wall Panel - ornamental` = `46.20 m²` + `16` `System Panel | Vacio` = `0.28 m²`, total `46.48 m²`) pertenecen a los 4 muros `Curtain Wall | Celosia Exterior` (`46.48 m²`); y **256 paneles** (`228` `System Panel | Vacio` = `280.36 m²` + `28` `Solid Pane vaciol` = `0.00 m²`) pertenecen a los 18 elementos `Curtain Wall | Cubierta` (`367.06 m²`).
   - **Regla para el generador (`Scripts/30_generadores_desde_revit.py`)**: **NO mapear ninguna partida a `CurtainWallPanels` de `Edificio de educacion`**. Cuantificar mampostería y cubierta exclusivamente desde `Walls` (`filtro_tipo: "NOVABLOCK"` → `1,337.95 m²`; `filtro_tipo: "Celosia Exterior"` → `46.48 m²`; `filtro_tipo: "Cubierta"` → `367.06 m²`), más los 87 muros `Ladrillo cara vista 15 CM` (`1,040.43 m²`) en `TT_ED_EDUCACIÓN_CANCELERIA_2027__Walls.json` (D-019).
2. **Cimentación (Cap. 02) y defecto de 12 `WallFoundation` con volumen 0**:
   - **Zapata corrida de borde**: 1 familia In-Place (`id: 514502`) en `StructuralFoundations` con **`volumen_m3 = 42.1931 m³`**, **`area_m2 = 338.1521 m²`** y longitud desarrollada en sus 10 sólidos de **`~248.62 m`** (`longitud_m: null` en parámetro nativo).
   - **Dados de columnas `0.40x0.40x0.60`**: 17 piezas en `StructuralFoundations` (`Nivel +5.30`) con **`volumen_m3 = 1.6320 m³`**, **`area_m2 = 2.7200 m²`** y **`longitud_m = 6.8000 m`** (`0.40 m` c/u). Suma `StructuralFoundations` = **`43.8251 m³`** (idéntico a la tabla `Volumen de cimentacion` de Revit = `43.83 m³`).
   - **Trabes de cimentación y dalas de desplante** (`Edificio de educacion__StructuralFraming.json`, `Nivel +5.30`): 15 `Trabe de cimentacion 20x40` (**`longitud_m = 76.4516 m`**, **`volumen_m3 = 4.7185 m³`**) y 37 `Dala de desplante de 15x25` (**`longitud_m = 221.5386 m`**, **`volumen_m3 = 5.6877 m³`**).
   - **12 `WallFoundation` con `Volume = 0` (`volumen_m3: null`)**: Defecto de modelado en origen (no se corrige). Están asociados a 12 muros de tipo `Curtain Wall` (`NOVABLOCK® (12) H` y `Celosia Exterior`, incluso 5 en niveles `+7.65` y `+8.80`), por lo que Revit no genera sólido (`Volume = 0.00 m³` en la propia tabla de planificación del modelo). Su longitud heredada del muro anfitrión es `95.6211 m` (`46.42 m` en 6 `Cimentación de muro`, `11.88 m` en 2 `Zapata - Le0xLi80xS45 cm`, `37.32 m` en 4 `Centrado - La80xS45 cm`). Para `ED-02-02-001` y `ED-02-01-002` se recomienda filtrar `StructuralFoundations` con `filtro_tipo: "Zapata corrida|Dado"`.
3. **Cubierta (`Curtain Wall | Cubierta`) y perfiles de acero en Cancelería (Cap. 04 y Cap. 07)**:
   - `Edificio de educacion__Walls.json` (`tipo: "Cubierta"`, 18 elem., **`367.0639 m²`** en `Nivel +12.30`) → debe alimentar **`ED-04-02-001`** (Cubierta en `m2`).
   - `Edificio de educacion__CurtainWallMullions.json` (`Montante rectangular - 10 x 40 cm`, 587 elem., **`883.5243 m`**, `31.1167 m³` en `Nivel +12.30`) → bastidor/perfilería de cubierta (puede alimentar **`ED-04-01-001`** con factor de peso lineal o partida de estructura de cubierta en `m`).
   - `TT_ED_EDUCACIÓN_CANCELERIA_2027__StructuralFraming.json` (`Canal C | C310X45`, 30 elem., **`89.7405 m`**, **`4,209.0623 kg`**) y `TT_ED_EDUCACIÓN_CANCELERIA_2027__StructuralColumns.json` (`Pilar L igual | L150x12`, 6 elem., **`10.9200 m`**, **`251.9628 kg`**) → suman **`4,461.0251 kg`** de acero estructural con `peso_kg` exacto y deben alimentar **`ED-04-01-001`** (Estructura metálica en `kg`) y **`ED-04-01-004`** (Pintura anticorrosiva en estructura metálica en `kg`).
4. **P-010 (Sub-vínculo `Bloque de baños_vinculo.rvt` en `Instalaciones.rvt`)**:
   - Queda pendiente de re-extracción en cuanto el usuario cargue el sub-vínculo `Bloque de baños_vinculo.rvt` desde *Manage Links* en Revit del PC-B y lo notifique.

## Auditoría de Calidad para Generadores (`Scripts/30_generadores_desde_revit.py`)
- En **los 59 archivos JSON** (`21,014` elementos), **0 elementos** carecen de `familia` (`no_fam = 0`) y **0 elementos** carecen de `tipo` (`no_tip = 0`).
- El script 30 agrupa por `(modelo_origen, nivel or "-", tipo or familia or "-")` y busca el regex `filtro_tipo` en `" | ".join(familia, tipo, material_principal)`. Ningún archivo ya validado requirió reescritura porque `familia` y `tipo` están poblados al 100%.
- A continuación se listan las categorías donde algún elemento tiene `nivel = null`, `material_principal = null`, o (en categorías de acero/estructura) `peso_kg = null` o `longitud_m = null`, con el conteo exacto de elementos afectados:

| Archivo JSON (`modelo__categoria`) | Total elem. | Sin `nivel` | Sin `familia` / `tipo` | Sin `material_principal` | Sin `longitud_m` | Sin `peso_kg` | Causa en Revit / Impacto en Script 30 |
|---|---:|---:|---:|---:|---:|---:|---|
| `Edificio de educacion__Rebar.json` | 247 | **247** | 0 | 0 | 0 | **0** (`4,166.36 kg`) | `DB.Rebar` en Revit no tiene `LevelId` directo (su nivel depende del elemento anfitrión: `982.45 kg` en cimentación `Nivel +5.30` y `3,183.91 kg` en superestructura `Nivel +5.30`/`+7.65`/`N.P.T.`). Traen `material_principal = "Acero"`, `longitud_m` y `peso_kg` al 100%. Script 30 los agrupa con `localizacion = "-"`. |
| `Edificio de educacion__StructuralFoundations.json` | 30 | **13** | 0 | **30** | **1** | 30 *(concreto)* | Sin `nivel`: la `Zapata corrida de borde` In-Place (1) y los 12 `WallFoundation` con volumen 0. Sin `longitud_m`: la `Zapata corrida de borde` (1) se cuantifica por `volumen_m3` (`42.19 m³`) y `area_m2` (`338.15 m²`). Material en tipo = `<By Category>`. |
| `Edificio de educacion__StructuralColumns.json` | 217 | 0 | 0 | **217** | 0 | 217 *(concreto)* | Son 217 columnas/castillos de **concreto** (`19.86 m³`, `759.50 m`); su material en tipo es `<By Category>` y su nombre de tipo indica el elemento (`Columna de 30 x 30`, `Castillo de 12x15`). |
| `Edificio de educacion__StructuralFraming.json` | 344 | 0 | 0 | **166** | 0 | 344 *(concreto)* | Las 178 viguetas sí traen material; las 166 trabes y dalas de concreto tienen `<By Category>` en tipo, pero su nombre de tipo dice explícitamente `concreto` / `Trabe` / `Dala`. *(Nota: 10 tramos cortos tienen `volumen_m3 = null` por recortes de unión en Revit; los 334 restantes suman `84.38 m³`, idéntico al schedule de Revit).* |
| `Edificio de educacion__CurtainWallMullions.json` | 587 | 0 | 0 | **587** | 0 (`883.52 m`) | **587** | Montantes de `Curtain Wall \| Cubierta` (`10 x 40 cm`). En Revit los `Mullion` tienen `Material = <By Category>`, `longitud_m` y `volumen_m3` (`31.12 m³`), pero Revit no calcula parámetro `Weight` (`peso_kg = null`) en familias de sistema `CurtainWallMullion`. |
| `Edificio de educacion__Walls.json` | 123 | 0 | 0 | **123** | 0 | 123 *(muros)* | Los 123 muros son `Curtain Wall` (no tienen `CompoundStructure` de capas); el material/sistema viene en `tipo` (`NOVABLOCK® (12) H`, `Celosia Exterior`, `Cubierta`). |
| `Edificio de educacion__CurtainWallPanels.json` | 10,467 | 0 | 0 | **264** | 10,467 | 10,467 | Solo los 264 `Wall Panel - ornamental` no definen material en tipo; no se usan en generadores para evitar doble conteo con `Walls` (P-011). |
| `Edificio de educacion__Floors.json` | 13 | 0 | 0 | **13** | 0 | 13 *(losas)* | Tienen `Structural Material = <By Category>`, pero el tipo describe el material (`Plantilla de concreto e=5cm`, `Firme estructural e=10 cm`, `Suelo de vigueta y bovedilla e=0.25`, `Capa de compresion f'c= 250 kg/cm²`). |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027__StructuralColumns.json` | 6 | 0 | 0 | **6** | **0** (`10.92 m`) | **0** (`251.96 kg`) | **Acero en Cancelería**: 6 pilares `Pilar L igual \| L150x12`. Traen **`longitud_m` y `peso_kg` al 100%** (`0` faltantes). `material_principal` es `null` porque `Structural Material = <By Category>`. |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027__StructuralFraming.json` | 30 | 0 | 0 | **30** | **0** (`89.74 m`) | **0** (`4,209.06 kg`) | **Acero en Cancelería**: 30 canales `Canal C \| C310X45`. Traen **`longitud_m` y `peso_kg` al 100%** (`0` faltantes). `material_principal` es `null` (`<By Category>`). |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027__CurtainWallMullions.json` | 640 | 0 | 0 | 0 (`Aluminio`) | 0 (`719.30 m`) | **640** | Montantes de aluminio de cancelería (`material_principal = "Aluminio"`, `longitud_m` al 100%); incluidos en el P.U. por `m2` de muro cortina (`ED-07-02-002`). |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027__Railings.json` | 6 | **2** | 0 | **6** | 0 (`53.72 m`) | 6 | 2 barandales (`900mm Pipe`) alojados en rampa/escalera no reportan `Base Level` directo; los 6 tienen `longitud_m` completa (`53.72 m`). |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027__Walls.json` | 110 | 0 | 0 | **15** | 0 | 110 | Los 95 muros básicos (87 `Ladrillo cara vista`, 4 `Madera`, 4 `AAC`) tienen `material_principal` completo; solo los 15 `Curtain Wall \| Muro cortina` tienen `material_principal = null`. |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027__CurtainWallPanels.json` | 592 | 0 | 0 | **336** | 592 | 592 | 336 paneles `System Panel \| Glazed` tienen material por categoría; todos traen `area_m2` (`253.73 m²`). |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027__Windows.json` / `Doors.json` / `Furniture.json` / `Stairs.json` | 133 / 37 / 18 / 1 | 0 | 0 | **133 / 12 / 14 / 1** | — | — | Se cuantifican por `conteo` (`pza`) y su descripción está en `familia` y `tipo`. |
| `TT-ED-EDU-ARQ-MOB__SpecialtyEquipment.json` / `Furniture.json` / `FurnitureSystems.json` | 35 / 530 / 2 | **1** / 0 / 0 | 0 | **34 / 328 / 2** | — | — | 1 `Projection_Screen` sin nivel (`nivel = null`); todos se cuantifican por `conteo` (`pza`) mediante `familia` y `tipo`. |
| `Instalaciones__PipeFittings.json` / `Pipes.json` / `FlexPipes.json` / `PipeAccessories.json` / `PlumbingFixtures.json` / `MechanicalEquipment.json` / `SpecialtyEquipment.json` | 313 / 344 / 8 / 38 / 17 / 6 / 1 | **1** / 0 / 0 / 0 / 0 / 0 / 0 | 0 | **313 / 344 / 8 / 10 / 17 / 4 / 1** | 0 en `Pipes`/`FlexPipes` | — | Solo 1 codo (`id: 970400`) en `PipeFittings` tiene `nivel = null`. En `Pipes` y `PipeFittings` el material, sistema y diámetro vienen codificados en `tipo` (ej. ` Tubería estándar - PVC · Sanitary · 101.60 mmø`). |
| `Proyecto electrico_corregido__LightingFixtures.json` | 249 | **82** | 0 | 0 (`100%` con mat.) | — | — | 82 luminarias basadas en cara/punto (`Face-Based` sobre plafones/muros del vínculo o sin host en `z ≈ 5.20, 6.53, 7.90, 11.46 m`) tienen `Schedule Level = InvalidElementId` en Revit (`nivel = null`). Script 30 las agrupa bajo `localizacion = "-"` sin perder ninguna pieza (`conteo = 249`). |
| `Proyecto electrico_corregido__DataDevices.json` | 29 | **18** | 0 | **20** | — | — | Fuera de alcance (Cap. 11, D-016). |
| `Proyecto electrico_corregido__Conduits.json` / `ConduitFittings.json` / `CableTrays.json` / `CableTrayFittings.json` / `ElectricalFixtures.json` / `LightingDevices.json` / `ElectricalEquipment.json` | 892 / 498 / 5 / 4 / 121 / 13 / 4 | 0 | 0 | **892 / 498 / 5 / 4 / 121 / 13 / 2** | 0 en `Conduits`/`CableTrays` | — | Tienen `nivel`, `familia`, `tipo` (con diámetro en `Conduits`) y cantidades (`longitud_m` o `conteo`) al 100%. |

## Preguntas nuevas
- (Las 3 preguntas originales de AG-1 ya fueron atendidas por CL-1 y el usuario en `D-019`, `P-010` y `P-011`; no se abren preguntas adicionales).

## Hecho
- Leídos `CLAUDE.md`, `AGENTS.md`, `HARNESS.md`, `_harness/decisiones.md` (incluida `D-019`), `_harness/preguntas.md` (`P-010`, `P-011`) y `_harness/cola.md`.
- **T-101 a T-107**: Extraídos y validados los 59 archivos JSON e `indice.json` de los 6 vínculos cargados en `modelo_federado.rvt` (validación `59/59 OK` confirmada por CL-1).
- **P-011 (Prioridad)**: Ejecutado análisis en solo lectura comparando por nivel, `Host`/`CurtainGrid.GetPanelIds()`, `BoundingBoxXYZ` y área los 123 `Walls` contra los 10,467 `CurtainWallPanels` de `Edificio de educacion.rvt`. Entregado `_harness/intermedios/revit/notas_doble_conteo_muros.md`.
- **Auditoría de calidad (Punto 3)** y **Documentación de cimentación, cubierta y perfiles de acero (Punto 4)**: Completadas y registradas en este status y en `_harness/intermedios/revit/notas_doble_conteo_muros.md`.
- **Verificación de RevitCortex (Punto 6)**: Confirmado que en la sesión activa de Revit 2027 (PID 37340) la pestaña `RevitCortex` no está cargada (Revit inició antes de instalarse el `.addin`, por lo que `RevitCortex.Server.exe` no está corriendo) y toda la extracción y análisis se realizó con `pyrevit-mcp` (`run_query`, modo solo lectura).

## Pendiente
- **P-010 (IHS)**: Re-extraer `Instalaciones.rvt` (T-106) tan pronto como el usuario cargue el sub-vínculo `Bloque de baños_vinculo.rvt` en Revit del PC-B y nos avise.

## Siguiente paso
CL-1 y AG-2 aplican las reglas de `_harness/intermedios/revit/notas_doble_conteo_muros.md` en `catalogo_v01.json` y `Scripts/30_generadores_desde_revit.py` (T-204, T-302).

## Archivos tocados
- `_harness/intermedios/revit/indice.json`
- `_harness/intermedios/revit/*.json` (59 archivos por modelo y categoría)
- `_harness/intermedios/revit/notas_doble_conteo_muros.md`
- `MCP Revit/notas_extraccion_revit.md`
- `MCP Revit/notas_doble_conteo_muros.md`
- `Scripts/_revit_extractor_lib.py`
- `Scripts/10_inventario_revit.py` a `Scripts/17_extraer_electrico.py`
- `_harness/status/AG-1.md`
- `_harness/logs/AG-1-23-11-2026.md`
