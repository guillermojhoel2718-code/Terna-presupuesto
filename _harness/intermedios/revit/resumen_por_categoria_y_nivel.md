# Resumen Consolidado por Categoría y Nivel para Generadores (Edificio de Educación ~2,500 m²)

- **Fecha**: 26-11-2026 · **Agente**: AG-1 (Extracción Revit · PC-B `MEMO`)
- **Fuente**: 59 archivos JSON validados en `_harness/intermedios/revit/` (`20,988` elementos en los 6 vínculos de `modelo_federado.rvt`).
- **JSON estructurado**: `_harness/intermedios/revit/resumen_por_categoria_y_nivel.json`
- **Script generador (idempotente)**: `Scripts/18_consolidar_resumen_revit.py`

---

## 1. Reconciliación de Superficie Construida (~2,500 m², D-010)

| Nivel Canónico | Elevación | Elementos de Piso / Losa / Cubierta en Revit | Archivo Intermedio | Área (m²) | Volumen (m³) |
|---|---:|---|---|---:|---:|
| **PB · Planta Baja** | `+5.30 m` | `Plantilla de concreto e=5cm` (`#560921`, Cap. 02) | `Edificio de educacion__Floors.json` | **804.1953** | 40.2098 |
| **PB · Planta Baja** | `+5.30 m` | `Firme estructural e=10 cm` (`#516170`, Cap. 05) | `Edificio de educacion__Floors.json` | **804.0946** | 80.4095 |
| **PA · Primer Piso (Entrepiso)** | `+8.80 m` | 10 losas `Suelo de vigueta y bovedilla e=0.25` (`741.6654 m²`) + 1 `Capa de compresion 5cm` (`11.4489 m²`) | `Edificio de educacion__Floors.json` | **753.1143** | 188.1539 |
| **AZ · Azotea** | `+12.30 m` | 4 losas `Generic 150mm` en `Nivel - Azotea` | `TT_ED_EDUCACIÓN_CANCELERIA_2027__Floors.json` | **1,113.7323** | 167.0598 |
| **CUB · Cubierta inclinada** | `+12.30 a +14.62 m` | 18 elementos `Curtain Wall \| Cubierta` | `Edificio de educacion__Walls.json` | **367.0639** | — |
| **Subtotal Estructura (PB Firme + PA Losa + AZ Losa)** | — | Huella horizontal acumulada de pisos y losas estructurales | — | **2,670.9412** | 435.6232 |
| **Subtotal Pisos Acabados (PB + PA) + Cubierta** | — | Pisos acabados PB (`1,238.77 m²`) + PA (`323.17 + 596.50 = 919.67 m²`) + Cubierta (`367.06 m²`) | `Proyecto acabado-DAMIAN` + `CANCELERIA` + `Estructura` | **2,525.5099** | — |

> **Conclusión de superficie**: Tanto la suma de pisos terminados más cubierta (**2,525.51 m²**) como la suma de firmes y losas estructurales (**2,670.94 m²**) cuadran con la superficie construida oficial de **~2,500 m² (D-010)**.

---

## 2. Resumen Global por Nivel Canónico (Unificando los 6 Vínculos)

*(Nota: Se excluyen de las columnas de Área y Volumen los 10,467 `CurtainWallPanels` de `Edificio de educacion` para no duplicar los 123 muros `Curtain Wall` de `Walls`, conforme a P-011).* 

| Nivel Canónico Unificado | Elev. (m) | Niveles equivalentes en los 6 vínculos | Elem. | Longitud Σ (m) | Área Σ (m²) | Volumen Σ (m³) | Peso Acero Σ (kg) |
|---|---:|---|---:|---:|---:|---:|---:|
| **N1_Cisterna_IHS (+3.83 m)** | 3.83 | `Level 3` (Instalaciones IHS) | 31 | 71.98 | 0.03 | 0.64 | 0.00 |
| **PB_Planta_Baja (+5.30 m)** | 5.30 | `Nivel +5.30`, `Nivel - Planta Baja`, `N.P.T +5.30`, `Nivel 3`, `NPT 5.30` | 6,265 | 5,367.73 | 9,109.57 | 987.51 | 0.00 |
| **PB_Mezzanine_6.00 (+6.00 m)** | 6.00 | `Nivel 4` (Acabados), `NIVEL 6.00` (Eléctrico) | 6 | 1.85 | 0.28 | 0.00 | 0.00 |
| **PB_Dala_Intermedia (+7.13 a +7.65 m)** | 7.60 | `Auxiliar dala intermedia +7.65`, `Nivel - Dala Int 01`, `Auxiliar +5.30` | 1,459 | 688.46 | 463.13 | 34.32 | 0.00 |
| **PA_Primer_Piso (+8.80 m)** | 8.80 | `N.P.T.`, `Nivel - Primer Piso`, `N.P.T +8.80`, `Nivel 5`, `NPT 8.80` | 9,257 | 5,922.33 | 10,776.26 | 833.76 | 0.00 |
| **PA_Dala_Intermedia (+10.63 a +11.15 m)** | 11.10 | `Auxiliar dala intermedia +11.15`, `Nivel - Dala Int 02`, `Auxiliar +8.80` | 2,029 | 581.97 | 429.47 | 27.80 | 0.00 |
| **AZ_Azotea (+12.30 m)** | 12.30 | `Nivel +12.30`, `Nivel - Azotea`, `PLANTA DE AZOTEA`, `Nivel 6`, `NPT 12.30` | 1,577 | 2,675.01 | 2,597.43 | 226.93 | 4,461.02 |
| **SIN_NIVEL (-)** | — | `nivel = null` (Rebar, Zapata corrida In-Place, 12 WallFoundation, 82 Luminarias Face-Based) | 364 | 5,299.14 | 903.92 | 369.72 | 4,166.36 |

---

## 3. Resumen por Vínculo, Categoría y Nivel (`59` archivos JSON)

| Vínculo (`modelo`) | Categoría (`categoria`) | Nivel en Revit (`nivel`) | Nivel Canónico | Elem. | Longitud (m) | Área (m²) | Volumen (m³) | Peso (kg) | Faltantes (`L / A / V / P`) |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| `Edificio de educacion` | `CurtainWallMullions` | `Nivel +12.30` | AZ_Azotea (+12.30 m) | 587 | 883.53 | 460.54 | 34.71 | 0.00 | `0/0/0/587` |
| `Edificio de educacion` | `CurtainWallPanels` | `Nivel +5.30` | PB_Planta_Baja (+5.30 m) | 3,463 | 0.00 | 506.09 | 81.52 | 0.00 | `3463/0/0/3463` |
| `Edificio de educacion` | `CurtainWallPanels` | `Auxiliar dala intermedia +7.65` | PB_Dala_Intermedia (+7.13 a +7.65 m) | 1,332 | 0.00 | 168.71 | 31.99 | 0.00 | `1332/0/0/1332` |
| `Edificio de educacion` | `CurtainWallPanels` | `N.P.T.` | PA_Primer_Piso (+8.80 m) | 3,442 | 0.00 | 504.37 | 80.72 | 0.00 | `3442/0/0/3442` |
| `Edificio de educacion` | `CurtainWallPanels` | `Auxiliar dala intermedia +11.15` | PA_Dala_Intermedia (+10.63 a +11.15 m) | 1,974 | 0.00 | 205.26 | 47.41 | 0.00 | `1974/0/0/1974` |
| `Edificio de educacion` | `CurtainWallPanels` | `Nivel +12.30` | AZ_Azotea (+12.30 m) | 256 | 0.00 | 280.36 | 2.80 | 0.00 | `256/28/28/256` |
| `Edificio de educacion` | `Floors` | `Nivel +5.30` | PB_Planta_Baja (+5.30 m) | 2 | 328.65 | 1,608.29 | 120.62 | 0.00 | `0/0/0/2` |
| `Edificio de educacion` | `Floors` | `N.P.T.` | PA_Primer_Piso (+8.80 m) | 11 | 428.93 | 753.11 | 188.15 | 0.00 | `0/0/0/11` |
| `Edificio de educacion` | `GenericModel` | `N.P.T.` | PA_Primer_Piso (+8.80 m) | 3,712 | 0.00 | 1,985.43 | 50.16 | 0.00 | `3712/0/0/3712` |
| `Edificio de educacion` | `Rebar` | `SIN_NIVEL (-)` | SIN_NIVEL (-) | 247 | 5,184.77 | 0.00 | 0.54 | 4,166.36 | `0/247/0/0` |
| `Edificio de educacion` | `StructuralColumns` | `Nivel +5.30` | PB_Planta_Baja (+5.30 m) | 111 | 388.50 | 118.09 | 10.17 | 0.00 | `0/0/0/111` |
| `Edificio de educacion` | `StructuralColumns` | `N.P.T.` | PA_Primer_Piso (+8.80 m) | 106 | 371.00 | 114.80 | 9.69 | 0.00 | `0/0/0/106` |
| `Edificio de educacion` | `StructuralFoundations` | `Nivel +5.30` | PB_Planta_Baja (+5.30 m) | 17 | 6.80 | 2.72 | 1.63 | 0.00 | `0/0/0/17` |
| `Edificio de educacion` | `StructuralFoundations` | `SIN_NIVEL (-)` | SIN_NIVEL (-) | 13 | 95.62 | 338.15 | 42.19 | 0.00 | `1/12/12/13` |
| `Edificio de educacion` | `StructuralFraming` | `Nivel +5.30` | PB_Planta_Baja (+5.30 m) | 52 | 297.99 | 118.15 | 10.41 | 0.00 | `0/1/1/52` |
| `Edificio de educacion` | `StructuralFraming` | `Auxiliar dala intermedia +7.65` | PB_Dala_Intermedia (+7.13 a +7.65 m) | 19 | 222.53 | 90.31 | 7.59 | 0.00 | `0/1/1/19` |
| `Edificio de educacion` | `StructuralFraming` | `N.P.T.` | PA_Primer_Piso (+8.80 m) | 232 | 1,527.65 | 529.66 | 41.43 | 0.00 | `0/5/5/232` |
| `Edificio de educacion` | `StructuralFraming` | `Auxiliar dala intermedia +11.15` | PA_Dala_Intermedia (+10.63 a +11.15 m) | 19 | 224.65 | 88.55 | 7.45 | 0.00 | `0/2/2/19` |
| `Edificio de educacion` | `StructuralFraming` | `Nivel +12.30` | AZ_Azotea (+12.30 m) | 22 | 296.02 | 142.83 | 17.49 | 0.00 | `0/1/1/22` |
| `Edificio de educacion` | `Walls` | `Nivel +5.30` | PB_Planta_Baja (+5.30 m) | 29 | 236.99 | 506.09 | 0.00 | 0.00 | `0/0/29/29` |
| `Edificio de educacion` | `Walls` | `Auxiliar dala intermedia +7.65` | PB_Dala_Intermedia (+7.13 a +7.65 m) | 28 | 231.11 | 168.71 | 0.00 | 0.00 | `0/0/28/28` |
| `Edificio de educacion` | `Walls` | `N.P.T.` | PA_Primer_Piso (+8.80 m) | 25 | 235.48 | 504.37 | 0.00 | 0.00 | `0/0/25/25` |
| `Edificio de educacion` | `Walls` | `Auxiliar dala intermedia +11.15` | PA_Dala_Intermedia (+10.63 a +11.15 m) | 23 | 228.14 | 205.26 | 0.00 | 0.00 | `0/0/23/23` |
| `Edificio de educacion` | `Walls` | `Nivel +12.30` | AZ_Azotea (+12.30 m) | 18 | 213.35 | 367.06 | 0.00 | 0.00 | `0/0/18/18` |
| `Instalaciones` | `FlexPipes` | `N.P.T +5.30` | PB_Planta_Baja (+5.30 m) | 8 | 2.82 | 0.00 | 0.00 | 0.00 | `0/8/1/8` |
| `Instalaciones` | `MechanicalEquipment` | `N.P.T +5.30` | PB_Planta_Baja (+5.30 m) | 6 | 0.00 | 518.07 | 87.75 | 0.00 | `6/0/0/6` |
| `Instalaciones` | `PipeAccessories` | `Level 3` | N1_Cisterna_IHS (+3.83 m) | 2 | 0.00 | 0.00 | 0.00 | 0.00 | `2/2/0/2` |
| `Instalaciones` | `PipeAccessories` | `N.P.T +5.30` | PB_Planta_Baja (+5.30 m) | 36 | 0.00 | 68.69 | 4.31 | 0.00 | `36/10/0/36` |
| `Instalaciones` | `PipeFittings` | `Level 3` | N1_Cisterna_IHS (+3.83 m) | 16 | 0.00 | 0.03 | 0.01 | 0.00 | `16/11/0/16` |
| `Instalaciones` | `PipeFittings` | `N.P.T +5.30` | PB_Planta_Baja (+5.30 m) | 279 | 0.00 | 1.02 | 0.34 | 0.00 | `279/197/0/279` |
| `Instalaciones` | `PipeFittings` | `PLANTA DE AZOTEA` | AZ_Azotea (+12.30 m) | 17 | 0.00 | 0.03 | 0.06 | 0.00 | `17/16/0/17` |
| `Instalaciones` | `PipeFittings` | `SIN_NIVEL (-)` | SIN_NIVEL (-) | 1 | 0.00 | 0.01 | 0.00 | 0.00 | `1/0/0/1` |
| `Instalaciones` | `Pipes` | `Level 3` | N1_Cisterna_IHS (+3.83 m) | 13 | 71.98 | 0.00 | 0.63 | 0.00 | `0/13/0/13` |
| `Instalaciones` | `Pipes` | `N.P.T +5.30` | PB_Planta_Baja (+5.30 m) | 311 | 744.42 | 0.00 | 3.46 | 0.00 | `0/311/0/311` |
| `Instalaciones` | `Pipes` | `PLANTA DE AZOTEA` | AZ_Azotea (+12.30 m) | 20 | 83.30 | 0.00 | 0.85 | 0.00 | `0/20/0/20` |
| `Instalaciones` | `PlumbingFixtures` | `N.P.T +5.30` | PB_Planta_Baja (+5.30 m) | 17 | 0.00 | 60.67 | 23.96 | 0.00 | `17/0/0/17` |
| `Instalaciones` | `SpecialtyEquipment` | `N.P.T +5.30` | PB_Planta_Baja (+5.30 m) | 1 | 0.00 | 1.13 | 0.04 | 0.00 | `1/0/0/1` |
| `Proyecto acabado-DAMIAN` | `Ceilings` | `Nivel 3` | PB_Planta_Baja (+5.30 m) | 2 | 286.47 | 589.75 | 17.69 | 0.00 | `0/0/0/2` |
| `Proyecto acabado-DAMIAN` | `Ceilings` | `Nivel 5` | PA_Primer_Piso (+8.80 m) | 1 | 239.58 | 535.33 | 16.06 | 0.00 | `0/0/0/1` |
| `Proyecto acabado-DAMIAN` | `Floors` | `Nivel 3` | PB_Planta_Baja (+5.30 m) | 15 | 619.26 | 1,262.19 | 30.50 | 0.00 | `0/0/0/15` |
| `Proyecto acabado-DAMIAN` | `Floors` | `Nivel 5` | PA_Primer_Piso (+8.80 m) | 15 | 691.68 | 1,350.21 | 35.78 | 0.00 | `0/0/0/15` |
| `Proyecto acabado-DAMIAN` | `Walls` | `Nivel 3` | PB_Planta_Baja (+5.30 m) | 20 | 242.58 | 845.40 | 133.90 | 0.00 | `0/0/0/20` |
| `Proyecto acabado-DAMIAN` | `Walls` | `Nivel 5` | PA_Primer_Piso (+8.80 m) | 17 | 236.32 | 824.05 | 131.85 | 0.00 | `0/0/0/17` |
| `Proyecto electrico_corregido` | `CableTrayFittings` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 4 | 0.00 | 0.00 | 0.05 | 0.00 | `4/4/0/4` |
| `Proyecto electrico_corregido` | `CableTrays` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 5 | 32.60 | 0.00 | 0.61 | 0.00 | `0/5/0/5` |
| `Proyecto electrico_corregido` | `Ceilings` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 1 | 249.45 | 515.49 | 15.46 | 0.00 | `0/0/0/1` |
| `Proyecto electrico_corregido` | `Ceilings` | `NPT 8.80` | PA_Primer_Piso (+8.80 m) | 1 | 239.58 | 502.90 | 15.09 | 0.00 | `0/0/0/1` |
| `Proyecto electrico_corregido` | `CommunicationDevices` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 1 | 0.00 | 0.56 | 0.01 | 0.00 | `1/0/0/1` |
| `Proyecto electrico_corregido` | `ConduitFittings` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 297 | 0.00 | 8.05 | 0.22 | 0.00 | `297/178/0/297` |
| `Proyecto electrico_corregido` | `ConduitFittings` | `NIVEL 6.00` | PB_Mezzanine_6.00 (+6.00 m) | 2 | 0.00 | 0.00 | 0.00 | 0.00 | `2/2/0/2` |
| `Proyecto electrico_corregido` | `ConduitFittings` | `NPT 8.80` | PA_Primer_Piso (+8.80 m) | 199 | 0.00 | 10.43 | 0.26 | 0.00 | `199/44/0/199` |
| `Proyecto electrico_corregido` | `Conduits` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 549 | 640.44 | 0.00 | 0.17 | 0.00 | `0/549/0/549` |
| `Proyecto electrico_corregido` | `Conduits` | `NIVEL 6.00` | PB_Mezzanine_6.00 (+6.00 m) | 2 | 1.85 | 0.00 | 0.00 | 0.00 | `0/2/0/2` |
| `Proyecto electrico_corregido` | `Conduits` | `NPT 8.80` | PA_Primer_Piso (+8.80 m) | 341 | 500.81 | 0.00 | 0.14 | 0.00 | `0/341/0/341` |
| `Proyecto electrico_corregido` | `DataDevices` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 11 | 0.00 | 1.14 | 0.03 | 0.00 | `11/0/0/11` |
| `Proyecto electrico_corregido` | `DataDevices` | `SIN_NIVEL (-)` | SIN_NIVEL (-) | 18 | 0.00 | 0.13 | 0.00 | 0.00 | `18/0/0/18` |
| `Proyecto electrico_corregido` | `Doors` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 1 | 0.00 | 3.01 | 0.13 | 0.00 | `1/0/0/1` |
| `Proyecto electrico_corregido` | `ElectricalEquipment` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 4 | 0.00 | 2.82 | 0.03 | 0.00 | `4/0/0/4` |
| `Proyecto electrico_corregido` | `ElectricalFixtures` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 61 | 0.00 | 5.07 | 0.01 | 0.00 | `61/0/0/61` |
| `Proyecto electrico_corregido` | `ElectricalFixtures` | `NPT 8.80` | PA_Primer_Piso (+8.80 m) | 60 | 0.00 | 4.99 | 0.01 | 0.00 | `60/0/0/60` |
| `Proyecto electrico_corregido` | `FireAlarmDevices` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 9 | 0.00 | 0.81 | 0.01 | 0.00 | `9/0/0/9` |
| `Proyecto electrico_corregido` | `Floors` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 1 | 30.94 | 42.43 | 8.49 | 0.00 | `0/0/0/1` |
| `Proyecto electrico_corregido` | `LightingDevices` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 4 | 0.00 | 0.56 | 0.00 | 0.00 | `4/0/0/4` |
| `Proyecto electrico_corregido` | `LightingDevices` | `NIVEL 6.00` | PB_Mezzanine_6.00 (+6.00 m) | 2 | 0.00 | 0.28 | 0.00 | 0.00 | `2/0/0/2` |
| `Proyecto electrico_corregido` | `LightingDevices` | `NPT 8.80` | PA_Primer_Piso (+8.80 m) | 7 | 0.00 | 0.98 | 0.00 | 0.00 | `7/0/0/7` |
| `Proyecto electrico_corregido` | `LightingFixtures` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 60 | 0.00 | 106.98 | 14.77 | 0.00 | `60/0/0/60` |
| `Proyecto electrico_corregido` | `LightingFixtures` | `NPT 8.80` | PA_Primer_Piso (+8.80 m) | 107 | 0.00 | 300.99 | 67.35 | 0.00 | `107/0/0/107` |
| `Proyecto electrico_corregido` | `LightingFixtures` | `SIN_NIVEL (-)` | SIN_NIVEL (-) | 82 | 0.00 | 553.47 | 326.93 | 0.00 | `82/0/0/82` |
| `Proyecto electrico_corregido` | `MechanicalEquipment` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 1 | 0.00 | 0.14 | 0.01 | 0.00 | `1/0/0/1` |
| `Proyecto electrico_corregido` | `PipeAccessories` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 3 | 0.00 | 0.01 | 0.00 | 0.00 | `3/0/0/3` |
| `Proyecto electrico_corregido` | `PipeFittings` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 9 | 0.00 | 0.00 | 0.00 | 0.00 | `9/3/0/9` |
| `Proyecto electrico_corregido` | `Pipes` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 6 | 3.39 | 0.00 | 0.00 | 0.00 | `0/6/0/6` |
| `Proyecto electrico_corregido` | `PlumbingFixtures` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 1 | 0.00 | 0.43 | 0.04 | 0.00 | `1/0/0/1` |
| `Proyecto electrico_corregido` | `SecurityDevices` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 9 | 0.00 | 274.93 | 282.55 | 0.00 | `9/0/0/9` |
| `Proyecto electrico_corregido` | `SpecialtyEquipment` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 6 | 0.00 | 42.41 | 1.10 | 0.00 | `6/0/0/6` |
| `Proyecto electrico_corregido` | `StructuralFraming` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 1 | 0.94 | 0.00 | 0.01 | 0.00 | `0/1/0/1` |
| `Proyecto electrico_corregido` | `Walls` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 24 | 244.00 | 846.22 | 126.81 | 0.00 | `0/0/0/24` |
| `Proyecto electrico_corregido` | `Walls` | `NPT 8.80` | PA_Primer_Piso (+8.80 m) | 17 | 236.10 | 823.45 | 123.50 | 0.00 | `0/0/0/17` |
| `Proyecto electrico_corregido` | `Windows` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 1 | 0.00 | 1.14 | 0.01 | 0.00 | `1/0/0/1` |
| `Proyecto electrico_corregido` | `Wires` | `NPT 5.30` | PB_Planta_Baja (+5.30 m) | 187 | 521.72 | 0.00 | 0.00 | 0.00 | `0/187/187/187` |
| `Proyecto electrico_corregido` | `Wires` | `NPT 8.80` | PA_Primer_Piso (+8.80 m) | 161 | 469.58 | 0.00 | 0.00 | 0.00 | `0/161/161/161` |
| `TT-ED-EDU-ARQ-MOB` | `Casework` | `Nivel - Planta Baja` | PB_Planta_Baja (+5.30 m) | 40 | 0.00 | 87.78 | 2.92 | 0.00 | `40/0/0/40` |
| `TT-ED-EDU-ARQ-MOB` | `Furniture` | `Nivel - Planta Baja` | PB_Planta_Baja (+5.30 m) | 204 | 0.00 | 482.06 | 24.26 | 0.00 | `204/20/20/204` |
| `TT-ED-EDU-ARQ-MOB` | `Furniture` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 326 | 0.00 | 1,078.52 | 33.06 | 0.00 | `326/27/27/326` |
| `TT-ED-EDU-ARQ-MOB` | `FurnitureSystems` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 2 | 0.00 | 20.27 | 0.37 | 0.00 | `2/0/0/2` |
| `TT-ED-EDU-ARQ-MOB` | `SpecialtyEquipment` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 34 | 0.00 | 21.84 | 0.41 | 0.00 | `34/0/0/34` |
| `TT-ED-EDU-ARQ-MOB` | `SpecialtyEquipment` | `SIN_NIVEL (-)` | SIN_NIVEL (-) | 1 | 0.00 | 12.16 | 0.06 | 0.00 | `1/0/0/1` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `CurtainWallMullions` | `Nivel - Planta Baja` | PB_Planta_Baja (+5.30 m) | 84 | 99.59 | 6.05 | 0.09 | 0.00 | `0/0/0/84` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `CurtainWallMullions` | `Nivel - Dala Int 01` | PB_Dala_Intermedia (+7.13 a +7.65 m) | 44 | 43.52 | 9.03 | 0.33 | 0.00 | `0/0/0/44` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `CurtainWallMullions` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 84 | 99.77 | 6.06 | 0.09 | 0.00 | `0/0/0/84` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `CurtainWallMullions` | `Nivel - Azotea` | AZ_Azotea (+12.30 m) | 428 | 533.19 | 109.45 | 3.98 | 0.00 | `0/0/0/428` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `CurtainWallPanels` | `Nivel - Planta Baja` | PB_Planta_Baja (+5.30 m) | 173 | 0.00 | 56.53 | 2.31 | 0.00 | `173/0/0/173` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `CurtainWallPanels` | `Nivel - Dala Int 01` | PB_Dala_Intermedia (+7.13 a +7.65 m) | 10 | 0.00 | 4.95 | 0.05 | 0.00 | `10/0/0/10` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `CurtainWallPanels` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 227 | 0.00 | 64.07 | 2.87 | 0.00 | `227/0/0/227` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `CurtainWallPanels` | `Nivel - Azotea` | AZ_Azotea (+12.30 m) | 182 | 0.00 | 187.55 | 1.88 | 0.00 | `182/12/12/182` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Doors` | `Nivel - Planta Baja` | PB_Planta_Baja (+5.30 m) | 20 | 0.00 | 36.07 | 0.71 | 0.00 | `20/2/2/20` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Doors` | `Nivel - Dala Int 01` | PB_Dala_Intermedia (+7.13 a +7.65 m) | 6 | 0.00 | 3.68 | 0.00 | 0.00 | `6/0/6/6` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Doors` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 11 | 0.00 | 43.96 | 0.90 | 0.00 | `11/2/2/11` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Floors` | `Nivel - Planta Baja` | PB_Planta_Baja (+5.30 m) | 4 | 128.25 | 229.15 | 4.16 | 0.00 | `0/0/0/4` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Floors` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 8 | 298.26 | 607.08 | 59.73 | 0.00 | `0/0/0/8` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Floors` | `Nivel - Azotea` | AZ_Azotea (+12.30 m) | 4 | 441.51 | 1,113.73 | 167.06 | 0.00 | `0/0/0/4` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Furniture` | `Nivel - Planta Baja` | PB_Planta_Baja (+5.30 m) | 13 | 0.00 | 38.32 | 1.56 | 0.00 | `13/0/0/13` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Furniture` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 5 | 0.00 | 25.14 | 0.42 | 0.00 | `5/0/0/5` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Railings` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 4 | 91.08 | 0.00 | 0.00 | 0.00 | `0/4/4/4` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Railings` | `SIN_NIVEL (-)` | SIN_NIVEL (-) | 2 | 18.75 | 0.00 | 0.00 | 0.00 | `0/2/2/2` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Stairs` | `Nivel - Planta Baja` | PB_Planta_Baja (+5.30 m) | 1 | 0.00 | 0.00 | 0.00 | 0.00 | `1/1/1/1` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `StructuralColumns` | `Nivel - Azotea` | AZ_Azotea (+12.30 m) | 6 | 10.92 | 0.00 | 0.03 | 251.96 | `0/6/0/0` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `StructuralFraming` | `Nivel - Azotea` | AZ_Azotea (+12.30 m) | 30 | 89.74 | 0.00 | 0.54 | 4,209.06 | `0/30/0/0` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Walls` | `Nivel - Planta Baja` | PB_Planta_Baja (+5.30 m) | 41 | 261.93 | 449.15 | 55.33 | 0.00 | `0/0/3/41` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Walls` | `Nivel - Dala Int 01` | PB_Dala_Intermedia (+7.13 a +7.65 m) | 20 | 191.31 | 186.45 | 26.35 | 0.00 | `0/0/2/20` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Walls` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 29 | 256.51 | 459.37 | 55.36 | 0.00 | `0/0/4/29` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Walls` | `Nivel - Dala Int 02` | PA_Dala_Intermedia (+10.63 a +11.15 m) | 13 | 129.19 | 135.66 | 20.35 | 0.00 | `0/0/0/13` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Walls` | `Nivel - Azotea` | AZ_Azotea (+12.30 m) | 7 | 123.45 | 216.22 | 0.33 | 0.00 | `0/0/6/7` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Windows` | `Nivel - Planta Baja` | PB_Planta_Baja (+5.30 m) | 60 | 0.00 | 171.99 | 0.87 | 0.00 | `60/0/0/60` |
| `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `Windows` | `Nivel - Primer Piso` | PA_Primer_Piso (+8.80 m) | 73 | 0.00 | 209.25 | 1.05 | 0.00 | `73/0/0/73` |

---

## 4. Huecos Detectados y Marcados como Preguntas (`P-010`, `P-013` a `P-016`)

| ID | Cap. | Archivo Afectado | Hueco / Discrepancia Detectada | Impacto en Generadores | Supuesto de Trabajo (Loop sin bloqueo) |
|---|---|---|---|---|---|
| **P-010 (Abierta)** | 08 / 09 | `_harness/intermedios/revit/Instalaciones__PlumbingFixtures.json` | Sub-vínculo 'Bloque de baños_vinculo.rvt' está Unloaded en Instalaciones.rvt. Solo hay 14 cajas de registro y 3 biodigestores (TOL-7000L); 0 WC, 0 lavabos y 0 mingitorios. | ED-09-02-001 (inodoros) y ED-09-02-002 (lavabos) quedan con cantidad 0 desde Revit. | Mantener en manual.json o re-extraer T-106 en cuanto el usuario cargue el sub-vínculo en Revit PC-B. |
| **P-013 (Nueva AG-1)** | 02 / 03 | `_harness/intermedios/revit/Edificio de educacion__StructuralFraming.json` | 10 tramos cortos de concreto en StructuralFraming tienen volumen_m3 = null y area_m2 = null en Revit por recortes de unión (1 'Trabe de cimentacion 20x40' id #552895 de L=0.15 m, y 9 'Dala de cerramiento de concreto de 15x25' ids #435689, #435905, #436684, #436724, #473890, #534743, #534834, #535908, #619739 que suman L=3.49 m). Generan los 32 avisos del script 30 en ED-02-02-001, ED-02-02-002, ED-03-01-002 y ED-03-02-001. | Diferencia despreciable (~0.14 m³ = 0.2% del volumen de trabes/dalas); el volumen de los 334 tramos restantes (84.38 m³) cuadra 100% con la tabla 'Volumen de trabes y dalas' de Revit. | Ignorar los 32 avisos del script 30 y conservar volumen_m3 = null fiel al modelo Revit. |
| **P-014 (Nueva AG-1)** | 04 | `_harness/intermedios/revit/Edificio de educacion__CurtainWallMullions.json` | La cubierta inclinada 'Curtain Wall | Cubierta' (367.06 m²) tiene 587 montantes 'Montante rectangular - 10 x 40 cm' (longitud_m = 883.5243 m, volumen_m3 = 31.1167 m³, peso_kg = null) que no están asignados a ninguna clave en catalogo_v01.json, mientras que ED-04-01-001 solo toma los 36 perfiles de acero de Cancelería (30 C310X45 + 6 L150x12 = 4,461.02 kg). Asimismo, ED-04-01-004 (pintura anticorrosiva en estructura metálica, en kg) tiene sin_cantidad_revit=true. | Definir si los 883.52 m de montantes de cubierta se cuantifican como bastidor metálico en ED-04-01-001 (con factor kg/m) y si ED-04-01-004 debe mapear al mismo peso_kg de estructura metálica. | ED-04-01-001 opera con los 4,461.02 kg verificados de Cancelería; los 587 montantes quedan identificados por si CL-1/AG-2 agregan mapeo por longitud_m × factor. |
| **P-015 (Nueva AG-1)** | 06 | `_harness/intermedios/revit/Proyecto acabado-DAMIAN__Floors.json` | En Proyecto acabado-DAMIAN hay 13 plafones modelados dentro de la categoría Floors ('PF_Plafon ACT - Armstrong Ceilings 24x48' = 487.89 m², 'PF_Plafon ACT 14x24' = 535.33 m², 'PF_Plafon de loseta ceramica' = 27.23 m²; subtotal = 1,050.45 m²) además de los 3 plafones en Ceilings ('ACT - Techos Armstrong - 24x48' = 1,125.08 m²). Actualmente ED-06-03-001 suma ambos (1,023.22 + 1,125.08 = 2,148.30 m² en N5 y N6). | Verificar si los 12 plafones 'PF_Plafon ACT' en Floors (1,023.22 m²) y los 3 'Ceilings' (1,125.08 m²) son áreas complementarias o se solapan en planta. | Mantener ambos en el resumen separados por categoría (Floors vs Ceilings) para que CL-1 decida en T-302 si filtra solo Ceilings (1,125.08 m²) o Floors+Ceilings (2,148.30 m²). |
| **P-016 (Nueva AG-1)** | 01 / 02 / 05 / 06 / 10 / 14 | `_harness/intermedios/generadores/manual.json` | 16 claves del catálogo v01 (además de las 2 de muebles sanitarios P-010) no tienen elementos directos en Revit y requieren captura o fórmula derivada en manual.json: Cap. 01 (ED-01-01-001 limpia, ED-01-01-002 despalme, ED-01-02-001 trazo, ED-01-03-001 bodega), Cap. 02 (ED-02-01-001 excavación, ED-02-03-001 relleno, ED-02-03-002 acarreo), Cap. 04 (ED-04-01-002 placas base, ED-04-01-003 anclas, ED-04-01-004 pintura acero, ED-04-02-002 canalón pluvial), Cap. 05 (ED-05-02-002 aplanado muros), Cap. 06 (ED-06-04-001 impermeabilización azotea), Cap. 10 (ED-10-05-001 sistema fotovoltaico 10 kWp = 1 jgo), Cap. 14 (ED-14-01-001 limpieza pisos, ED-14-01-002 limpieza vidrios). | Si no se incluyen en manual.json, quedan en claves_sin_cantidad al correr Scripts/30_generadores_desde_revit.py. | Se incluye en el resumen de AG-1 una tabla de cantidades base sugeridas desde medidas geométricas de Revit (huella PB = 804.20 m², azotea = 1,113.73 m², vidrios = 313.10 m², etc.) para alimentar manual.json de inmediato. |

---

## 5. Cantidades Base Derivadas de Geometría Revit para las 16 Claves de `manual.json` (`P-016`)

Para que CL-1 (rol AG-3) pueda cerrar las partidas `sin_cantidad_revit` en `_harness/intermedios/generadores/manual.json` sin esperar:

| Clave | Unidad | Cantidad Derivada | Criterio / Elemento Revit de Respaldo |
|---|---|---:|---|
| `ED-01-01-001` | `m2` | **804.1953** | Área de desplante = Plantilla de concreto e=5cm en Edificio de educacion__Floors.json (#560921) |
| `ED-01-01-002` | `m3` | **160.8391** | Área de desplante (804.1953 m²) × 0.20 m de espesor de despalme |
| `ED-01-02-001` | `m2` | **804.1953** | Área de desplante = Plantilla de concreto e=5cm (#560921) |
| `ED-01-03-001` | `m2` | **36.0000** | SUPUESTO: Caseta y bodega provisional de obra 6.00 × 6.00 m |
| `ED-02-01-001` | `m3` | **204.5233** | Área de contacto de cimentación (340.8721 m² de Zapata corrida + Dados) × 0.60 m profundidad promedio |
| `ED-02-03-001` | `m3` | **110.2820** | Excavación (204.5233 m³) − Concreto en cimentación/contratrabes/plantilla (48.5436 + 5.6877 + 40.01 = 94.2413 m³) |
| `ED-02-03-002` | `m3` | **255.1594** | Despalme (160.8391 m³) + Sobrante de excavación (94.3203 m³) medido en banco |
| `ED-04-01-002` | `kg` | **336.4400** | 37 apoyos de columnas (31 concreto/mixtas + 6 acero L150x12) × placa base A-36 0.30×0.30 m de 1/2" (9.093 kg/pza) |
| `ED-04-01-003` | `pza` | **148.0000** | 4 anclas cold rolled de 1"×1.40 m por cada uno de los 37 apoyos de columna (37 × 4) |
| `ED-04-01-004` | `kg` | **4,461.0194** | Mismo peso_kg que ED-04-01-001 (30 Canal C310X45 + 6 Pilar L150x12 en Cancelería) |
| `ED-04-02-002` | `m` | **106.6771** | 50% de la longitud de borde de Curtain Wall | Cubierta (213.3542 m / 2) en Nivel +12.30 |
| `ED-05-02-002` | `m2` | **1,601.4938** | Área de muros interiores con acabado en Proyecto acabado-DAMIAN__Walls.json (32 'muro general EDUC' = 1,601.4938 m²) |
| `ED-06-04-001` | `m2` | **1,113.7323** | Área de losas de azotea 'Generic 150mm' en Nivel - Azotea (TT_ED_EDUCACIÓN_CANCELERIA_2027__Floors.json, 4 losas = 1,113.7323 m²) |
| `ED-10-05-001` | `jgo` | **1.0000** | MEMORIA §9.3: 1 juego de sistema solar fotovoltaico interconectado de 10.0 kWp (18 paneles × 550 Wp) |
| `ED-14-01-001` | `m2` | **2,391.7529** | Suma de pisos terminados (ED-06-01-001: 1,101.70 m² + ED-06-01-002: 623.72 m² + ED-06-01-003: 666.33 m²) |
| `ED-14-01-002` | `m2` | **313.0951** | Área de vidrios en ventanas y muros cortina (ED-07-02-002: 207.21 m² Glazed + 46.52 m² Puerta Muro Cortina + 59.37 m² Ventanas = 313.10 m²) |
