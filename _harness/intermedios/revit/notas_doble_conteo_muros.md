# Análisis de Doble Conteo de Muros y Paneles de Muro Cortina (P-011) y Notas de Cuantificación

- **Fecha**: 23-11-2026
- **Agente**: AG-1 (Extracción Revit · PC-B `MEMO`)
- **Alcance**: Vínculo `Edificio de educacion.rvt` (Estructura) y cruce con `TT_ED_EDUCACIÓN_CANCELERIA_2027.rvt` (Cancelería) en modo **solo lectura** (`query`).
- **Referencias**: Decisión `D-019`, Pregunta `P-011`, `Scripts/30_generadores_desde_revit.py`.

---

## 1. Diagnóstico de Doble Conteo: `Walls` vs `CurtainWallPanels` en `Edificio de educacion.rvt` (P-011)

En `Edificio de educacion.rvt` existen **123 elementos en `Walls`** (todos de la familia `Curtain Wall`) y **10,467 elementos en `CurtainWallPanels`**. Se verificó mediante la API de Revit (`Wall.CurtainGrid.GetPanelIds()`, `Panel.Host`, nivel de referencia e intersección tridimensional de `BoundingBoxXYZ`) la relación exacta entre ambas categorías:

### (a) ¿Cuántos paneles se solapan con los muros `NOVABLOCK® (12) H` y cuántos m² serían doble conteo?

- **Los 9,931 paneles de block (`9,930` de tipo `NOVABLOCK® (12) H 1 Tercio` + `1` de tipo `NOVABLOCK® (12) H`) son exactamente las piezas hijas alojadas (`CurtainGrid.GetPanelIds()`) dentro de los 101 muros anfitriones `Curtain Wall | NOVABLOCK® (12) H`.**
- El modelador de Estructura creó los muros de mampostería como **Muro Cortina (`Curtain Wall`)** con una retícula del tamaño de cada pieza de block (`12 × 20 × 60 cm`), de modo que Revit genera:
  1. El elemento anfitrión en la categoría `Walls` (101 muros, **1,337.9468 m²**, longitud total **918.4329 m**).
  2. Las 9,931 piezas individuales en la categoría `CurtainWallPanels` (**1,337.9467 m²**, volumen **238.5020 m³**).
- **Comparación por nivel y Bounding Box (3D)**:

| Nivel en `Edificio de educacion.rvt` | Muros `Walls` (`NOVABLOCK® (12) H`) | Área en `Walls` (m²) | Longitud en `Walls` (m) | Paneles hijos en `CurtainWallPanels` | Área en `CurtainWallPanels` (m²) | Paneles con BoundingBox solapado 100% |
|---|---:|---:|---:|---:|---:|---:|
| `Nivel +5.30` | 27 | 485.0531 | 230.9778 | 3,335 (3,334 `1 Tercio` + 1 `H`) | 485.0531 | 3,335 (100%) |
| `Auxiliar dala intermedia +7.65` | 28 | 168.7070 | 231.1053 | 1,332 (`1 Tercio`) | 168.7068 | 1,332 (100%) |
| `N.P.T.` (+8.80) | 23 | 478.9306 | 228.2124 | 3,290 (`1 Tercio`) | 478.9307 | 3,290 (100%) |
| `Auxiliar dala intermedia +11.15` | 23 | 205.2561 | 228.1374 | 1,974 (`1 Tercio`) | 205.2560 | 1,974 (100%) |
| **TOTAL NOVABLOCK** | **101** | **1,337.9468** | **918.4329** | **9,931** | **1,337.9467** | **9,931 (100%)** |

- **Envolvente espacial (`BoundingBoxXYZ` en metros)**:
  - 101 muros `Walls | NOVABLOCK® (12) H`: `Min = (-10.5293, -64.2746, 5.3000)`, `Max = (42.2370, -36.0721, 12.0500)`.
  - 9,931 paneles `CurtainWallPanels | NOVABLOCK®`: `Min = (-10.2019, -63.8781, 5.2900)`, `Max = (41.8228, -36.3779, 12.4000)`.
- **Magnitud del doble conteo**: Si se sumaran `Walls` y `CurtainWallPanels` para muros de block, se duplicarían **9,931 elementos** y **1,337.95 m²** al 100% (diferencia de solo `0.0001 m²` por redondeo de punto flotante).
- Lo mismo ocurre con los otros dos tipos de `Curtain Wall` en `Edificio de educacion__Walls.json`:
  - **`Curtain Wall | Celosia Exterior`**: 4 muros anfitriones en `Walls` (**46.4763 m²**, 13.2788 m) que alojan **280 paneles** en `CurtainWallPanels` (264 `Wall Panel - ornamental` = `46.1987 m²` + 16 `System Panel | Vacio` = `0.2775 m²`, suma exacta = **46.4762 m²**).
  - **`Curtain Wall | Cubierta`**: 18 elementos anfitriones en `Walls` en `Nivel +12.30` (**367.0639 m²**, 213.3542 m) que alojan **256 paneles** en `CurtainWallPanels` (228 `System Panel | Vacio` = `280.3625 m²` + 28 `Solid Pane vaciol` = `0.00 m²`) y **587 montantes** en `CurtainWallMullions` (`Montante rectangular - 10 x 40 cm` = **883.5243 m**).

---

### (b) Desglose completo de los 10,467 `CurtainWallPanels` de `Edificio de educacion.rvt`

| Familia y Tipo en `CurtainWallPanels` | Conteo | Área total (m²) | Volumen total (m³) | Muro anfitrión (`Host` en `Walls`) | Niveles | Función en el modelo |
|---|---:|---:|---:|---|---|---|
| `NOVABLOCK® (12) H 1 Tercio \| NOVABLOCK® (12) H 1 Tercio` | 9,930 | 1,337.8028 | 238.4769 | `Curtain Wall \| NOVABLOCK® (12) H` (101 muros) | `+5.30` (3,334), `+7.65` (1,332), `N.P.T.` (3,290), `+11.15` (1,974) | Piezas individuales de block de los 101 muros Novablock |
| `NOVABLOCK® (12) H \| NOVABLOCK® (12) H` | 1 | 0.1439 | 0.0251 | `Curtain Wall \| NOVABLOCK® (12) H` | `Nivel +5.30` (1) | Pieza de block entero en muro Novablock |
| `Wall Panel - ornamental \| Wall Panel - ornamental` | 264 | 46.1987 | 3.1261 | `Curtain Wall \| Celosia Exterior` (4 muros) | `Nivel +5.30` (120), `N.P.T.` (144) | Piezas de celosía ornamental en los 4 muros de celosía |
| `System Panel \| Vacio` (en Celosía) | 16 | 0.2775 | 0.0028 | `Curtain Wall \| Celosia Exterior` | `Nivel +5.30` (8), `N.P.T.` (8) | Huecos vacíos de ajuste en la retícula de los 4 muros de celosía |
| `System Panel \| Vacio` (en Cubierta) | 228 | 280.3625 | 2.8036 | `Curtain Wall \| Cubierta` (18 muros) | `Nivel +12.30` (228) | Paños vacíos entre la retícula de montantes de la cubierta |
| `Solid Pane vaciol \| Solid Pane vaciol` | 28 | 0.0000 | 0.0000 | `Curtain Wall \| Cubierta` (18 muros) | `Nivel +12.30` (28) | Paneles vacíos sin geometría en la retícula de cubierta |
| **TOTAL `Edificio de educacion__CurtainWallPanels.json`** | **10,467** | **1,664.7853** | **244.4345** | **123 muros `Curtain Wall` en `Walls`** | — | **100% son sub-elementos de los 123 `Walls`** |

---

### (c) Regla y filtro exacto para `mapeo_revit` en Catálogo (AG-2) y Generadores (CL-1 / Script 30)

Para **evitar cualquier doble conteo** en `Scripts/30_generadores_desde_revit.py`:

1. **NO mapear ningún concepto a `categoria: "CurtainWallPanels"` del modelo `"Edificio de educacion"`**. Los 10,467 paneles de `Edificio de educacion__CurtainWallPanels.json` deben quedar sin asignar a partidas de mampostería o cubierta (aparecerán en la sección informativa *"Elementos Revit sin asignar"* de `reporte_v01.md`, lo cual es correcto porque son las piezas anidadas de los `Curtain Wall`).
2. **Cuantificar siempre desde la categoría anfitriona `Walls`** (además de ser mucho más limpio en `Generadores_v01.xlsx` y `REF_REVIT`, pues genera 101 IDs de muros en vez de 9,931 IDs de piezas de block):
   - **Cap. 05 · Muros de block (`ED-05-01-002` o partida de muro Novablock 12 cm)**:
     - `modelo`: `"Edificio de educacion"`
     - `categoria`: `"Walls"`
     - `filtro_tipo`: `"NOVABLOCK"`
     - `campo_cantidad`: `"area_m2"` → **1,337.95 m²** (101 muros).
   - **Cap. 05 · Muros de ladrillo aparente (`ED-05-01-001`)**:
     - `modelo`: `"TT_ED_EDUCACIÓN_CANCELERIA_2027"`
     - `categoria`: `"Walls"`
     - `filtro_tipo`: `"Ladrillo cara vista"` (o `"Ladrillo|Celosia"` si se incluye la celosía exterior de Estructura)
     - `campo_cantidad`: `"area_m2"` → **1,040.43 m²** (87 muros en Cancelería) + opcionalmente **46.48 m²** (4 muros `Celosia Exterior` en `Edificio de educacion__Walls.json`).
   - **Cap. 05 · Muros divisorios interiores adicionales en Cancelería**:
     - En `TT_ED_EDUCACIÓN_CANCELERIA_2027__Walls.json` hay además 4 muros `Muro 100 mm AAC COM` (**7.22 m²**) y 4 muros `Madera` (**20.88 m²**). Nota: los 15 muros `Curtain Wall | Muro cortina` de `TT_ED_EDUCACIÓN_CANCELERIA_2027__Walls.json` tienen `area_m2 = 229.88 m²` y sus paneles acristalados están en `TT_ED_EDUCACIÓN_CANCELERIA_2027__CurtainWallPanels.json` (Cap. 07), por lo que en Cancelería el filtro de `Walls` para Cap. 05 **no debe incluir `"Muro cortina"`**.

---

## 2. Cimentación (Cap. 02): Zapata Corrida, Dados, Trabes/Dalas y Hallazgo de 12 `WallFoundation` con Volumen 0

### 2.1 Cantidades reales verificadas en `Edificio de educacion.rvt`

| Elemento / Concepto de Cimentación | Archivo intermedio | Categoría | Filtro `tipo` sugerido | Pzas | Longitud real (m) | Área (m²) | Volumen real (m³) | Observaciones técnicas |
|---|---|---|---|---:|---:|---:|---:|---|
| **Plantilla de concreto e=5 cm** | `Edificio de educacion__Floors.json` | `Floors` | `Plantilla de concreto` | 1 | 164.3259 *(perímetro)* | **804.1953** | **40.2098** | Modelada en `Floors` (`id: 560921`, `Nivel +5.30`). Alternativamente, el área de contacto de `Zapata corrida de borde` + `Dados` en `StructuralFoundations` es **340.8721 m²** (`338.1521 + 2.7200 m²`). |
| **Firme estructural e=10 cm (PB)** | `Edificio de educacion__Floors.json` | `Floors` | `Firme estructural` | 1 | 164.3259 *(perímetro)* | **804.0946** | **80.4095** | Modelado en `Floors` (`id: 516170`, `Nivel +5.30`) para Cap. 05 (`ED-05-02-001`). |
| **Zapata corrida de borde** | `Edificio de educacion__StructuralFoundations.json` | `StructuralFoundations` | `Zapata corrida de borde` | 1 *(In-Place)* | **~248.62** *(eje de 10 sólidos)* | **338.1521** | **42.1931** | Familia *In-Place* (`id: 514502`, cotas `4.80 a 5.05 m`, espesor `0.25 m`, compuesta por 10 cuerpos sólidos). No expone parámetro `Length` nativo (`longitud_m: null`); su longitud desarrollada medida sobre la geometría de sus 10 sólidos es `~248.62 m` (perímetro superior `993.08 m`). |
| **Dados de cimentación 0.40×0.40×0.60 m** | `Edificio de educacion__StructuralFoundations.json` | `StructuralFoundations` | `Dado para columnas` | 17 | **6.8000** *(17 × 0.40 m)* | **2.7200** | **1.6320** | 17 instancias de `Encepado-Rectangular \| Dado para columnas 0.40x0.40x0.60` en `Nivel +5.30` (cotas `4.70 a 5.30 m`, `0.096 m³` c/u). |
| **Subtotal `StructuralFoundations` con volumen** | `Edificio de educacion__StructuralFoundations.json` | `StructuralFoundations` | `Zapata corrida\|Dado` | **18** | — | **340.8721** | **43.8251** | **Cuadra al 100% con la tabla de planificación `Volumen de cimentacion` de Revit (`42.19 + 1.63 = 43.83 m³`)**. |
| **Trabe de cimentación 20×40 cm** | `Edificio de educacion__StructuralFraming.json` | `StructuralFraming` | `Trabe de cimentacion 20x40` | 15 | **76.4516** | 39.1993 | **4.7185** | 15 tramos en `Nivel +5.30` (1 tramo de ajuste de `0.15 m` tiene `volumen_m3: null` por recorte de unión en Revit; los otros 14 suman `4.7185 m³`). |
| **Dala de desplante 15×25 cm** | `Edificio de educacion__StructuralFraming.json` | `StructuralFraming` | `Dala de desplante de 15x25` | 37 | **221.5386** | 78.9463 | **5.6877** | 37 tramos en `Nivel +5.30`, todos con longitud y volumen completos. |
| **Acero de refuerzo en cimentación (`Rebar`)** | `Edificio de educacion__Rebar.json` | `Rebar` | `.*` *(o por host)* | 247 *(total)* | 4,581.47 *(total)* | — | 0.5307 *(total)* | El modelo tiene 247 elementos `Rebar` (**4,166.36 kg** en total). De ellos, **982.45 kg** están alojados en elementos de cimentación/desplante (`527.74 kg` en Zapata corrida + `164.65 kg` en Dados + `64.35 kg` en Trabe de cimentación + `225.72 kg` en Dala de desplante) y **3,183.91 kg** en superestructura/losas. |

### 2.2 Hallazgo del modelo: 12 instancias de `WallFoundation` con `Volume = 0` (`volumen_m3: null`)

En `Edificio de educacion__StructuralFoundations.json` existen 12 elementos de la clase `DB.WallFoundation` cuyo parámetro nativo `HOST_VOLUME_COMPUTED` en Revit es **`0.00 m³`** (`Area = 0.00 m²`, `Length = 0.00 m`), tal como lo confirma la propia tabla de planificación `Volumen de cimentacion` dentro del archivo `.rvt`:

| Tipo de `WallFoundation` | Conteo | IDs en Revit | Muros anfitriones (`WallId`) | Niveles de los muros anfitriones | Longitud de muros anfitriones (`longitud_m`) | Volumen en Revit (`volumen_m3`) |
|---|---:|---|---|---|---:|---:|
| `Wall Foundation \| Cimentación de muro` (0.91×0.30 m) | 6 | `513031, 513051, 513455, 513474, 540238, 540239` | 2 `Celosia Exterior` + 4 `NOVABLOCK® (12) H` | `Nivel +5.30` (3), `Auxiliar +7.65` (2), `N.P.T.` (1) | **46.4212 m** | `null` (`0.00 m³`) |
| `Wall Foundation \| Zapata - Le0xLi80xS45 cm` (1.11×0.45 m) | 2 | `513433, 540237` | 2 `NOVABLOCK® (12) H` (`366126, 536825`) | `Nivel +5.30` (1), `Auxiliar +7.65` (1) | **11.8800 m** | `null` (`0.00 m³`) |
| `Wall Foundation \| Centrado - La80xS45 cm` (0.80×0.45 m) | 4 | `513498, 513514, 540240, 540241` | 4 `NOVABLOCK® (12) H` (`368012, 366147, 536843, 536830`) | `Nivel +5.30` (2), `Auxiliar +7.65` (2) | **37.3200 m** | `null` (`0.00 m³`) |
| **TOTAL `WallFoundation` sin geometría** | **12** | — | **12 muros `Curtain Wall`** | — | **95.6211 m** | **`null` (`0.00 m³`)** |

- **Causa técnica del defecto en el modelo**: En Revit, un `WallFoundation` requiere un muro básico estructural para generar su sólido de extrusión. En este modelo, esos 12 `WallFoundation` quedaron asociados a muros de tipo **`Curtain Wall`** (`NOVABLOCK® (12) H` y `Celosia Exterior`), e incluso 5 de ellos están asociados a muros en niveles superiores (`Auxiliar dala intermedia +7.65` y `N.P.T. +8.80`). Por ello Revit no genera geometría sólida para esos 12 elementos (`Volume = 0`) y el modelador creó en su lugar la familia In-Place **`Zapata corrida de borde` (`id: 514502`, `42.1931 m³`)** que cubre toda la zapata corrida real del edificio.
- **Acción tomada**: Siguiendo la instrucción de **no corregir defectos del modelo**, se reporta como hallazgo. En `Edificio de educacion__StructuralFoundations.json` esas 12 instancias conservan `volumen_m3: null` y `area_m2: null` (por lo que si `ED-02-02-001` filtra por `Zapata corrida|Dado`, ni siquiera generarán avisos de `volumen_m3` nulo en el script 30).

---

## 3. Cubierta (`Curtain Wall | Cubierta`) y Perfiles de Acero de Cancelería (Cap. 04 y Cap. 07)

En los modelos vinculados no existen elementos en las categorías `Roofs` ni `Gutter`. En su lugar, la estructura metálica y la cubierta se modelaron repartidas entre `Edificio de educacion.rvt` y `TT_ED_EDUCACIÓN_CANCELERIA_2027.rvt`:

| Elemento en Revit | Vínculo (`modelo`) | Categoría JSON | Familia y Tipo (`familia \| tipo`) | Pzas | Cantidad disponible | Concepto del catálogo que debe alimentar |
|---|---|---|---|---:|---|---|
| **Cubierta inclinada (área de envolvente)** | `Edificio de educacion` | `Walls` | `Curtain Wall \| Cubierta` | 18 | **`area_m2 = 367.0639 m²`** (`longitud_m = 213.3542 m`, `Nivel +12.30`) | **`ED-04-02-001`** (Cubierta de panel metálico aislado tipo sándwich, en `m2`). *Nota*: Si además se incluye la losa de azotea del vínculo Cancelería (`TT_ED_EDUCACIÓN_CANCELERIA_2027__Floors.json`, tipo `Generic 150mm` en `Nivel - Azotea`), hay 4 elementos adicionales con `1,113.7323 m²`. |
| **Perfilería/bastidor de cubierta (`10 × 40 cm`)** | `Edificio de educacion` | `CurtainWallMullions` | `Montante rectangular \| Montante rectangular - 10 x 40 cm` | 587 | **`longitud_m = 883.5243 m`** (`volumen_m3 = 31.1167 m³`, `Nivel +12.30`) | **`ED-04-01-001`** (Estructura metálica principal y secundaria, si se aplica factor de peso lineal en `mapeo_revit`, p. ej. perfil tubular/IPR equivalente) o concepto específico de bastidor de cubierta en `m`. |
| **Vigas/canales estructurales de acero en Azotea (`C310X45`)** | `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `StructuralFraming` | `Canal C \| C310X45` | 30 | **`peso_kg = 4,209.0623 kg`** (`longitud_m = 89.7405 m`, `volumen_m3 = 0.5362 m³`, `Nivel - Azotea`) | **`ED-04-01-001`** (Estructura metálica principal y secundaria en `kg`) y **`ED-04-01-004`** (Pintura anticorrosiva en estructura metálica en `kg`). |
| **Columnas/pilares de acero en Azotea (`L150x12`)** | `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `StructuralColumns` | `Pilar L igual \| L150x12` | 6 | **`peso_kg = 251.9628 kg`** (`longitud_m = 10.9200 m`, `volumen_m3 = 0.0321 m³`, `Nivel - Azotea`) | **`ED-04-01-001`** (Estructura metálica en `kg`) y **`ED-04-01-004`** (Pintura en estructura metálica en `kg`). **Suma acero en Cancelería = `4,461.0251 kg`**. |
| **Fachada integral / Muro cortina de aluminio y cristal** | `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `CurtainWallPanels` | `System Panel \| Glazed` (580 pzas = `207.2071 m²`) + `Puerta Muro Cortina` (12 pzas = `46.5194 m²`) | 592 | **`area_m2 = 253.7265 m²`** (acompañados de 640 `CurtainWallMullions` = `719.2994 m`) | **`ED-07-02-002`** (Fachada integral / muro cortina de aluminio serie 3" con cristal templado, en `m2`). |
| **Barandales metálicos** | `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Railings` | `Railing \| Tubo Rectangular` (4 pzas = `14.54 m`) + `900mm Pipe` (2 pzas = `39.1795 m`) | 6 | **`longitud_m = 53.7195 m`** | **`ED-07-03-001`** (Barandal metálico de protección, en `m`). *(En `TT-ED-EDU-ARQ-MOB` no hay `Railings`; están en `TT_ED_EDUCACIÓN_CANCELERIA_2027`).* |
