# Notas de lectura Revit (AG-1) · 23-11-2026

## 1. Entorno verificado (PC-B · MEMO)
- **Revit 2027** (build `27.3.0.28`, PID `37340`) con `Modelo federado/modelo_federado.rvt` abierto y sin modificar (`is_modified: false`).
- **pyRevit**: `v7.0.0.26278+2233` adjunto a Revit 2027, Agent Host habilitado (`policy: ask`) y servidor MCP (`pyrevit mcp`) operativo.
- **Engine recomendado**: `--engine=cpython` (Python 3.12.3). IronPython 2.7 presenta `UnicodeDecodeError` al serializar caracteres acentuados en los títulos de los vínculos (como `TT_ED_EDUCACIÓN_CANCELERIA_2027.rvt`).
- **Modo**: `query` (solo lectura; `run_query` hace rollback automático y bloquea guardado/sincronización).

## 2. Inventario de los 6 vínculos del modelo federado

| ID Instancia | Vínculo | Ruta relativa | Estado | Archivos JSON | Total elementos |
|---|---|---|---|---|---|
| `374618` | `TT-ED-EDU-ARQ-MOB` | `../Archivos revit/TT-ED-EDU-ARQ-MOB.rvt` | `Loaded` | 4 | 607 |
| `374621` | `Instalaciones` | `../Archivos revit/Instalacion IHS_2027/Instalaciones.rvt` | `Loaded` | 7 | 727 |
| `374624` | `Edificio de educacion` | `../Archivos revit/Estructura_2027/00_ Edificio de educacion/Edificio de educacion.rvt` | `Loaded` | 9 | 15,740 |
| `374627` | `TT_ED_EDUCACIÓN_CANCELERIA_2027` | `../Archivos revit/Herrería y Cancelería_2027/TT_ED_EDUCACIÓN_CANCELERIA_2027.rvt` | `Loaded` | 11 | 1,623 |
| `374630` | `Proyecto acabado-DAMIAN` | `../Archivos revit/Acabados_2027/theriam/Proyecto acabado-DAMIAN.rvt` | `Loaded` | 3 | 70 |
| `374644` | `Proyecto electrico_corregido` | `../Archivos revit/Instalacion Electrica_2027/Copias de seguridad/Proyecto electrico_corregido.rvt` | `Loaded` | 25 | 2,247 |

**Total**: 6 vínculos cargados · 59 archivos JSON en `_harness/intermedios/revit/` + `indice.json` · 21,014 elementos extraídos y validados con `py Scripts/schemas/validar.py revit`.

## 3. Hallazgos clave para AG-2 (Catálogo / `mapeo_revit`) y CL-1 (Generadores)

1. **`TT-ED-EDU-ARQ-MOB.rvt` (Cap. 01, 05, 13)**:
   - Contiene únicamente mobiliario y equipamiento fijo (`Furniture`: 530, `Casework`: 40, `SpecialtyEquipment`: 35, `FurnitureSystems`: 2). No tiene instancias de `Walls`, `Floors` ni `Roofs`.
2. **Albañilería (Cap. 05) y Área de desplante (Cap. 01)**:
   - Los muros están modelados en dos vínculos:
     - `Edificio de educacion.rvt`: 101 muros cortina `NOVABLOCK® (12) H` (`1,337.95 m²`, `918.43 m`, compuestos por 9,931 piezas en `CurtainWallPanels`) y 4 muros `Celosia Exterior` (`46.48 m²`).
     - `TT_ED_EDUCACIÓN_CANCELERIA_2027.rvt`: 87 muros básicos `Ladrillo cara vista 15 CM` (`1,040.43 m²`, `156.07 m³`), 4 muros `Madera` (`20.88 m²`) y 4 muros `Muro 100 mm AAC COM` (`7.22 m²`).
   - El área de desplante y firme de planta baja está en `Edificio de educacion__Floors.json`: `Plantilla de concreto e=5cm` (`element_id: 560921`, `804.1953 m²`, `40.2098 m³`) y `Firme estructural e=10 cm` (`element_id: 516170`, `804.0946 m²`, `80.4095 m³`).
3. **Cimentación y Estructura (Cap. 02, 03, 04)**:
   -En `Edificio de educacion__StructuralFoundations.json`: 1 `Zapata corrida de borde` (`42.1931 m³`, `338.1521 m²`) y 17 `Dado para columnas 0.40x0.40x0.60` (`1.632 m³`, `2.72 m²`). Las 12 instancias de `Wall Foundation` tienen `volumen_m3 = null` porque en Revit su volumen reportado es `0.00 m³` (sus longitudes de muro anfitrión sí quedaron registradas en `longitud_m`: `46.42 m`, `11.88 m` y `37.32 m`).
   - En `Edificio de educacion__StructuralColumns.json`: 31 `Columna de 30 x 30_Para claros largos` (`9.4609 m³`, `108.50 m`), 102 `Castillo de 12x15 cm_confinamiento para muros` (`6.2673 m³`, `357.00 m`), 1 `Castillo de 12x20 cm_confinamiento para muros 2` (`0.0607 m³`, `3.50 m`) y 83 `Zona de varilla interna de muro` (`4.068 m³`, `290.50 m`).
   - En `Edificio de educacion__StructuralFraming.json`: 15 `Trabe de cimentacion 20x40` (`4.7185 m³`, `76.45 m`), 37 `Dala de desplante de 15x25` (`5.6876 m³`, `221.54 m`), 101 `Dala de cerramiento de concreto de  15x25` (`39.0622 m³`, `1,227.84 m`), 13 `Trabe de concreto de 30x60` (`20.1756 m³`, `118.98 m`) y 178 `Vigueta pretensada de concreto 12x20` (`14.7358 m³`, `924.03 m`).
   - En `Edificio de educacion__GenericModel.json`: 3,712 bovedillas de cemento-arena (`GPEVCO-EST-Bovedilla cemento arena 63 x 20 x 20`: 3,684 pzas + 28 pzas de ajuste).
   - En `Edificio de educacion__Rebar.json`: 247 elementos de acero de refuerzo con `peso_kg` total = `4,166.36 kg`.
   - Cubierta y acero estructural (Cap. 04): En `Edificio de educacion` la cubierta está modelada como `Curtain Wall | Cubierta` en `Nivel +12.30` (18 elementos, `367.0639 m²`) con 587 `Montante rectangular - 10 x 40 cm` (`883.52 m`). Adicionalmente, en `TT_ED_EDUCACIÓN_CANCELERIA_2027` hay 30 perfiles de acero `Canal C | C310X45` (`89.74 m`, `4,209.06 kg`), 6 columnas de acero `Pilar L igual | L150x12` (`10.92 m`, `251.96 kg`) y 4 losas `Generic 150mm` en `Nivel - Azotea` (`1,113.7323 m²`).
4. **Acabados (Cap. 06)**:
   - En `Proyecto acabado-DAMIAN__Floors.json`: 8 `Piso de concreto pulido autonivelante y firme de concreto f¨c=200 kg/cm2` (`805.7509 m²`), 4 `Piso de concreto pulido con agregado expuesto e= 0.002` (`433.0225 m²`), 4 `Piso de concreto pulido densificado e= 0.002` (`295.9488 m²`), 1 `piso aulas loseta ceramica e=0.02` (`27.225 m²`), y 13 plafones modelados como `Floors` (`PF_Plafon de loseta ceramica de 2cm de espesor`: `27.225 m²`; 6 `PF_Plafon ACT - Armstrong Ceilings - 24" x 48"`: `487.8944 m²`; 6 `PF_Plafon ACT - Armstrong Ceilings - 14" x 24"`: `535.3275 m²`).
   - En `Proyecto acabado-DAMIAN__Ceilings.json`: 3 plafones `ACT - Techos Armstrong - 24" x 48" -` (`1,125.0812 m²`).
   - En `Proyecto acabado-DAMIAN__Walls.json`: 32 `muro general EDUC` (`1,601.4939 m²`) y 5 `Muro Exterior - Interior Aparente` (`67.9504 m²`).
   - Nota: En `TT_ED_EDUCACIÓN_CANCELERIA_2027__Floors.json` también hay 8 pisos `Acabado - Porcelanato Esmaltado Tavola Noce Mate - 20x120` (`596.4988 m²`).
5. **Instalación Hidráulica y Sanitaria (Cap. 08 y 09)**:
   - En `Instalaciones__Pipes.json` y `PipeFittings.json`, el campo `tipo` incluye el sistema (`Sanitary` / `Domestic_Cold_Water`) y el diámetro (`101.60 mmø`, `50.80 mmø`, `25.40 mmø`, `12.70 mmø`) para que `mapeo_revit` pueda filtrar directamente por regex sobre `tipo`.
   - En `Instalaciones__PlumbingFixtures.json` solo hay 14 cajas de registro y 3 biodigestores (`TOL-7000L`), y en `MechanicalEquipment.json` hay 1 bomba, 1 cisterna Rotoplas 1,100 L y 4 elementos de la cisterna de concreto armado de 76,000 L. Los muebles de baño (WC, lavabos, mingitorios) no están colocados como instancias en `Instalaciones.rvt` (el sub-vínculo `Bloque de baños_vinculo.rvt` dentro de IHS está `Unloaded`).
6. **Instalación Eléctrica (Cap. 10)**:
   - En `Proyecto electrico_corregido__Conduits.json` (892 tramos, `1,143.10 m`), `ConduitFittings.json` (498 pzas), `CableTrays.json` (5 tramos, `32.60 m`), `CableTrayFittings.json` (4 pzas), `Wires.json` (348 tramos, `991.30 m`), `LightingFixtures.json` (249 luminarias: 220 panel LED, 18 pared, 11 spot), `LightingDevices.json` (13 apagadores), `ElectricalFixtures.json` (121 contactos) y `ElectricalEquipment.json` (4 tableros/paneles).
