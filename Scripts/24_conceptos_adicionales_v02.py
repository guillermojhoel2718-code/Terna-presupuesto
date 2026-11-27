"""Conceptos adicionales para catalogo_v02 (T-206) del Edificio de Educación (~2,500 m2).

Amplía el catálogo base de 65 conceptos a 107 conceptos detallados cubriendo:
- Cap. 01 Preliminares (retiro de despalme, tapial provisional, seguridad y señalización)
- Cap. 02 Cimentación (compactación de fondo de cepa, trabes de cimentación, dalas de desplante, impermeabilización de cadena, acarreo km subsecuentes)
- Cap. 03 Estructura de concreto (castillos de confinamiento, dalas de cerramiento, viguetas pretensadas T 12x20, bovedillas 63x20x20)
- Cap. 04 Estructura metálica y cubierta (bastidor/montantes de cubierta 10x40 cm, cubierta plana de azotea 150 mm)
- Cap. 05 Albañilería (celosía exterior de barro, muros interiores AAC 100 mm, chaflanes perimetrales de mortero)
- Cap. 06 Acabados, carpintería arquitectónica y exteriores (concreto pulido densificado, porcelanato Tavola Noce Mate 20x120, piso exterior suspendido, tierra vegetal en jardineras, lambrín de madera tratada, plafón MetalWorks Mesh, plafón cerámico húmedo)
- Cap. 07 Herrería, cancelería y carpintería (puertas interiores de madera, puertas corredizas, mullions de aluminio 50x150 y 30x30 mm, escalera metálica principal)
- Cap. 08 Instalación hidráulica y pluvial (mangueras flexibles, cajas de registro de válvulas, cisternas subterráneas de concreto armado 76,000 L)
- Cap. 09 Instalación sanitaria (conexiones flexibles sanitarias, mingitorios ecológicos)
- Cap. 10 Instalación eléctrica (tubería conduit iluminación, cajas/conduit fittings, curvas de charola, cableado THW-LS iluminación y potencia, luminarias de pared)
- Cap. 13 Mobiliario y equipamiento fijo (pizarrones acrílicos 144x48", maceteros con arbusto y equipamiento complementario)
- Cap. 14 Limpieza y entrega (retiro final de escombro y limpieza exterior)

Nota: Cuando se ensambla catalogo_v02, los filtros de mapeo_revit de los conceptos base se refinan
para que los 107 conceptos particionen exactamente los elementos de Revit con 0 duplicados.
"""
from __future__ import annotations

# Ajustes de mapeo_revit sobre las claves base cuando se activa el desglose granular de v02 (0 duplicados)
OVERRIDES_MAPEO_V02: dict[str, list[dict]] = {
    "ED-02-02-001": [
        {
            "modelo": "Edificio de educacion",
            "categoria": "StructuralFoundations",
            "filtro_tipo": "Dado para columnas|Zapata corrida",
            "campo_cantidad": "volumen_m3",
        }
    ],
    "ED-02-02-002": [
        {
            "modelo": "Edificio de educacion",
            "categoria": "StructuralFoundations",
            "filtro_tipo": "Dado para columnas|Zapata corrida",
            "campo_cantidad": "area_m2",
        }
    ],
    "ED-03-01-001": [
        {
            "modelo": "Edificio de educacion",
            "categoria": "StructuralColumns",
            "filtro_tipo": "Columna de 30 x 30",
            "campo_cantidad": "volumen_m3",
        }
    ],
    "ED-03-01-002": [
        {
            "modelo": "Edificio de educacion",
            "categoria": "StructuralColumns",
            "filtro_tipo": "Pilar rectangular|Columna|Castillo",
            "campo_cantidad": "area_m2",
        },
        {
            "modelo": "Edificio de educacion",
            "categoria": "StructuralFraming",
            "filtro_tipo": "Dala de cerramiento|Trabe de concreto",
            "campo_cantidad": "area_m2",
        },
    ],
    "ED-03-02-001": [
        {
            "modelo": "Edificio de educacion",
            "categoria": "StructuralFraming",
            "filtro_tipo": "Trabe de concreto de 30x60",
            "campo_cantidad": "volumen_m3",
        }
    ],
    "ED-04-02-001": [
        {
            "modelo": "Edificio de educacion",
            "categoria": "Walls",
            "filtro_tipo": "^Curtain Wall \\| Cubierta$",
            "campo_cantidad": "area_m2",
        }
    ],
    "ED-05-01-001": [
        {
            "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
            "categoria": "Walls",
            "filtro_tipo": "Ladrillo cara vista 15 CM",
            "campo_cantidad": "area_m2",
        }
    ],
    "ED-05-01-002": [
        {
            "modelo": "Edificio de educacion",
            "categoria": "Walls",
            "filtro_tipo": "NOVABLOCK",
            "campo_cantidad": "area_m2",
        }
    ],
    "ED-06-01-001": [
        {
            "modelo": "Proyecto acabado-DAMIAN",
            "categoria": "Floors",
            "filtro_tipo": "concreto pulido autonivelante",
            "campo_cantidad": "area_m2",
        }
    ],
    "ED-06-01-002": [
        {
            "modelo": "Proyecto acabado-DAMIAN",
            "categoria": "Floors",
            "filtro_tipo": "piso aulas loseta ceramica",
            "campo_cantidad": "area_m2",
        }
    ],
    "ED-06-01-003": [
        {
            "modelo": "Proyecto acabado-DAMIAN",
            "categoria": "Floors",
            "filtro_tipo": "agregado expuesto",
            "campo_cantidad": "area_m2",
        }
    ],
    "ED-06-02-002": [
        {
            "modelo": "Proyecto acabado-DAMIAN",
            "categoria": "Walls",
            "filtro_tipo": "Muro Exterior - Interior Aparente",
            "campo_cantidad": "area_m2",
        }
    ],
    "ED-06-03-001": [
        {
            "modelo": "Proyecto acabado-DAMIAN",
            "categoria": "Ceilings",
            "filtro_tipo": "ACT - Techos Armstrong",
            "campo_cantidad": "area_m2",
        }
    ],
    "ED-07-01-001": [
        {
            "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
            "categoria": "Doors",
            "filtro_tipo": "Puerta Sencilla Abatible",
            "campo_cantidad": "conteo",
        }
    ],
    "ED-08-01-004": [
        {
            "modelo": "Instalaciones",
            "categoria": "PipeAccessories",
            "filtro_tipo": "Valves|Valve",
            "campo_cantidad": "conteo",
        }
    ],
    "ED-08-03-001": [
        {
            "modelo": "Instalaciones",
            "categoria": "MechanicalEquipment",
            "filtro_tipo": "Cisterna Rotplas",
            "campo_cantidad": "conteo",
        }
    ],
    "ED-10-01-001": [
        {
            "modelo": "Proyecto electrico_corregido",
            "categoria": "Conduits",
            "filtro_tipo": "Cable Acometida",
            "campo_cantidad": "longitud_m",
        }
    ],
    "ED-10-02-002": [
        {
            "modelo": "Proyecto electrico_corregido",
            "categoria": "LightingFixtures",
            "filtro_tipo": "SPOT",
            "campo_cantidad": "conteo",
        }
    ],
    "ED-13-02-001": [
        {
            "modelo": "TT-ED-EDU-ARQ-MOB",
            "categoria": "Casework",
            "filtro_tipo": ".*",
            "campo_cantidad": "conteo",
        },
        {
            "modelo": "TT-ED-EDU-ARQ-MOB",
            "categoria": "Furniture",
            "filtro_tipo": "Locker|Bookcase|ESTANTER|Estanter|Storage combination|Lateral-File",
            "campo_cantidad": "conteo",
        },
    ],
}


CONCEPTOS_ADICIONALES_V02: list[dict] = [
    # =========================================================================
    # CAPÍTULO 01 — PRELIMINARES
    # =========================================================================
    {
        "clave": "ED-01-01-003",
        "capitulo": "01",
        "subcapitulo": "01",
        "concepto": (
            "Carga y acarreo en camión al primer kilómetro de material vegetal y maleza producto de limpia y "
            "despalme del terreno, volumen medido en banco, incluye: carga manual/mecánica, descarga a banco "
            "de tiro autorizado, mano de obra, equipo y herramienta."
        ),
        "unidad": "m3",
        "precio_unitario": 188.03,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave BN15BB (pág. 25)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave BN15BB (pág. 25): 'Carga manual, acarreo en camión al primer "
            "kilómetro y descarga, de material fino o granular, volumen medido en banco' — P.U. = $188.03/m3 (D-011)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [],
    },
    {
        "clave": "ED-01-03-002",
        "capitulo": "01",
        "subcapitulo": "03",
        "concepto": (
            "Construcción de tapial perimetral provisional de protección de 2.44 m de altura a base de hojas de "
            "triplay de pino de 12 mm de espesor sobre bastidor de polines de 4\"x4\"x8' a cada 1.22 m y barrotes "
            "de pino de 3a, incluye: materiales, colocación, mantenimiento durante la obra, desmontaje final, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "precio_unitario": 228.17,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave CF12BG (pág. 36)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave CF12BG (pág. 36): 'Tapial de triplay de pino de 12 mm de espesor, "
            "con polines de 0.102x0.102x2.44 m (4\"x4\"x8') a cada 1.22 m' — P.U. = $228.17/m2 (D-011)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [],
    },
    {
        "clave": "ED-01-03-003",
        "capitulo": "01",
        "subcapitulo": "03",
        "concepto": (
            "Suministro, colocación y mantenimiento de señalamiento preventivo y restrictivo de seguridad en obra, "
            "extintores, botiquín de primeros auxilios y módulos sanitarios portátiles para personal durante el "
            "periodo de ejecución del edificio de educación, incluye: retiro al término de los trabajos."
        ),
        "unidad": "lote",
        "precio_unitario": 18500.00,
        "fuente_tipo": "SUPUESTO",
        "fuente_ref": "SUPUESTO conservador para señalización y protección colectiva de seguridad en obra",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "SUPUESTO conservador para paquete de señalización normativa NOM-031-STPS, malla delimitadora, "
            "extintores PQS y equipo de seguridad colectiva en frente del edificio de educación ($18,500.00/lote)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [],
    },

    # =========================================================================
    # CAPÍTULO 02 — CIMENTACIÓN
    # =========================================================================
    {
        "clave": "ED-02-01-003",
        "capitulo": "02",
        "subcapitulo": "01",
        "concepto": (
            "Afine, nivelación y compactación de fondo de cepas de cimentación por medios manuales y mecánicos "
            "(bailarina compactadora) al 90% Proctor previo al colado de plantilla, incluye: incorporación de agua, "
            "mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "03 BÁSICOS.pdf (1P + EQRVIBRA) / Validado con Xalapa CIM-6.2.2",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con cuadrilla 1P (rendimiento 28 m2/jor = $26.69/m2), compactador mecánico (0.08 hr/m2 "
            "= $12.16/m2) y agua de compactación; CD = $41.85/m2."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "1P", "descripcion": "CUADRILLA No 1 (1 PEON + 0.1 CABO) AFINE Y COMPACTACION DE FONDO", "unidad": "jor", "cantidad": 0.035714, "precio_unitario": 747.23, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "EQRVIBRA", "descripcion": "COMPACTADOR / RODILLO VIBRATORIO WACKER", "unidad": "hr", "cantidad": 0.0800, "precio_unitario": 151.97, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "358-AGU-0201", "descripcion": "AGUA PARA COMPACTACION", "unidad": "m3", "cantidad": 0.0150, "precio_unitario": 107.90, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR (5% M.O.)", "unidad": "%", "cantidad": 1.38, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-02-02-004",
        "capitulo": "02",
        "subcapitulo": "02",
        "concepto": (
            "Concreto premezclado estructural f'c=250 kg/cm2, clase 1, T.M.A. 20 mm, bombeado en trabes de "
            "cimentación de 20x40 cm y dalas de desplante de 15x25 cm (§8.1.1 memoria arquitectónica), incluye: "
            "suministro, bombeo, colado, vibrado, curado, muestreo, mano de obra, equipo y herramienta."
        ),
        "unidad": "m3",
        "precio_unitario": 4241.93,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave FG12CB (pág. 50)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave FG12CB (pág. 50): 'Suministro y colocación de concreto hidráulico "
            "f'c=250 kg/cm2 clase 1 bombeable para elementos de cimentación (zapatas, dados, trabes de liga, contratrabes)' "
            "— P.U. = $4,241.93/m3 (D-011)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFraming",
                "filtro_tipo": "Trabe de cimentacion|Dala de desplante",
                "campo_cantidad": "volumen_m3",
            }
        ],
        "apu": [],
    },
    {
        "clave": "ED-02-02-005",
        "capitulo": "02",
        "subcapitulo": "02",
        "concepto": (
            "Cimbra acabado común y descimbra en trabes de cimentación de 20x40 cm y dalas de desplante de "
            "15x25 cm a base de madera de pino de 3a y triplay de 19 mm (4 usos), incluye: habilitado, "
            "cimbrado, desmoldante, descimbrado, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "precio_unitario": 347.97,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave CB12BD (pág. 31)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave CB12BD (pág. 31): 'Cimbra acabado común y descimbra en "
            "cimentación (zapatas, contratrabes, dados)' — P.U. = $347.97/m2 (D-011)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFraming",
                "filtro_tipo": "Trabe de cimentacion|Dala de desplante",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [],
    },
    {
        "clave": "ED-02-02-006",
        "capitulo": "02",
        "subcapitulo": "02",
        "concepto": (
            "Impermeabilización capilar en corona de dalas de desplante de 15 cm de ancho a base de emulsión "
            "asfáltica, fieltro asfáltico y riego de arena sílice para evitar humedad ascendente en muros de "
            "mampostería, incluye: limpieza de superficie, materiales, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa CIM-6.2.12 + Insumos_APUCMX",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con emulsión asfáltica e impermeabilizante (0.35 lt/m × $78.00 = $27.30/m), membrana "
            "de refuerzo ($8.50/m) y cuadrilla 1A1P (rendimiento 45 m/jor = $35.40/m); CD = $73.00/m."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFraming",
                "filtro_tipo": "Dala de desplante",
                "campo_cantidad": "longitud_m",
            }
        ],
        "apu": [
            {"codigo": "308-ASF-0101", "descripcion": "EMULSION ASFALTICA E IMPERMEABILIZANTE C/MEMBRANA P/CADENA DE DESPLANTE", "unidad": "lt", "cantidad": 0.4590, "precio_unitario": 78.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO)", "unidad": "jor", "cantidad": 0.022222, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR (5% M.O.)", "unidad": "%", "cantidad": 1.80, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-02-03-003",
        "capitulo": "02",
        "subcapitulo": "03",
        "concepto": (
            "Acarreo en camión de volteo en kilómetros subsecuentes al primero (promedio 5 km a tiro autorizado) "
            "de material sobrante producto de excavaciones, volumen medido en banco, incluye: camión de volteo y operador."
        ),
        "unidad": "m3",
        "fuente_tipo": "APU",
        "fuente_ref": "01 PRESUPUESTO.pdf CIM-07 / Tabulador CDMX BN15BC ($17.77/m3-km × 5 km)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado para tiro promedio a 5 km subsecuentes conforme a Tabulador CDMX BN15BC ($17.77/m3-km × 5 km "
            "= $88.85/m3) y 01 PRESUPUESTO.pdf CIM-07."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "EQCAMION", "descripcion": "CAMION DE VOLTEO DE 7 M3 DIESEL 160 HP (ACARREO 5 KM SUBSECUENTES)", "unidad": "hr", "cantidad": 0.089938, "precio_unitario": 987.90, "fuente": "08 COSTOS HORARIOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 03 — ESTRUCTURA DE CONCRETO Y MAMPOSTERÍA CONFINADA
    # =========================================================================
    {
        "clave": "ED-03-01-003",
        "capitulo": "03",
        "subcapitulo": "01",
        "concepto": (
            "Concreto premezclado/elaborado en obra f'c=250 kg/cm2 en castillos de confinamiento de muros de "
            "12x15 cm, 12x20 cm y castillos ahogados en celdas de block hueco NOVABLOCK (§8.1.2 memoria "
            "arquitectónica), incluye: suministro, colado, vibrado, curado, mano de obra y herramienta."
        ),
        "unidad": "m3",
        "precio_unitario": 4254.17,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave FJ18BC (pág. 53)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave FJ18BC (pág. 53): 'Suministro y colocación de concreto hidráulico "
            "estructural clase 1 f'c=250 kg/cm2 bombeable para elementos de superestructura' — P.U. = $4,254.17/m3 (D-011)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralColumns",
                "filtro_tipo": "Castillo|castillo ahogado",
                "campo_cantidad": "volumen_m3",
            }
        ],
        "apu": [],
    },
    {
        "clave": "ED-03-02-003",
        "capitulo": "03",
        "subcapitulo": "02",
        "concepto": (
            "Concreto estructural f'c=250 kg/cm2 en dalas de cerramiento e intermedias de confinamiento de muros "
            "de 15x25 cm en planta baja, entrepiso y azotea (§8.1.2 memoria arquitectónica), incluye: suministro, "
            "bombeo, colado, vibrado, curado, mano de obra, equipo y herramienta."
        ),
        "unidad": "m3",
        "precio_unitario": 4254.17,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave FJ18BC (pág. 53)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave FJ18BC (pág. 53): 'Suministro y colocación de concreto hidráulico "
            "estructural clase 1 f'c=250 kg/cm2 bombeable para elementos de superestructura' — P.U. = $4,254.17/m3 (D-011)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFraming",
                "filtro_tipo": "Dala de cerramiento",
                "campo_cantidad": "volumen_m3",
            }
        ],
        "apu": [],
    },
    {
        "clave": "ED-03-03-002",
        "capitulo": "03",
        "subcapitulo": "03",
        "concepto": (
            "Suministro, izaje y montaje de vigueta pretensada de concreto tipo T de 12x20 cm (GPEVCO-EST) para "
            "entrepiso prefabricado conforme al modelo estructural, incluye: acarreos, elevación a nivel +8.80 y "
            "+12.30 m, apuntalamiento, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 03 BÁSICOS.pdf 1A1P",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con vigueta pretensada de concreto 12x20 cm ($185.00/m + 2% desperdicio) y cuadrilla "
            "1A1P de montaje y apuntalamiento (rendimiento 35 m/jor = $45.52/m); CD = $236.50/m."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFraming",
                "filtro_tipo": "Vigueta pretensada de concreto 12x20",
                "campo_cantidad": "longitud_m",
            }
        ],
        "apu": [
            {"codigo": "VB-VIG-01", "descripcion": "VIGUETA PRETENSADA DE CONCRETO TIPO T 12x20 CM", "unidad": "m", "cantidad": 1.0200, "precio_unitario": 185.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO)", "unidad": "jor", "cantidad": 0.028571, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y APUNTALAMIENTO (5% M.O.)", "unidad": "%", "cantidad": 2.28, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-03-03-003",
        "capitulo": "03",
        "subcapitulo": "03",
        "concepto": (
            "Suministro, elevación y colocación de bovedilla de cemento-arena de 63x20x20 cm (GPEVCO-EST) entre "
            "viguetas pretensadas de entrepiso, incluye: piezas de ajuste en extremos, acarreos, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 03 BÁSICOS.pdf 1A1P",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con bovedilla de cemento-arena 63x20x20 cm ($28.50/pza + 3% merma) y cuadrilla 1A1P "
            "(rendimiento 140 pzas/jor = $11.38/pza); CD = $41.31/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "GenericModel",
                "filtro_tipo": "Bovedilla cemento arena",
                "campo_cantidad": "conteo",
            }
        ],
        "apu": [
            {"codigo": "VB-BOV-01", "descripcion": "BOVEDILLA DE CEMENTO-ARENA 63x20x20 CM (INC. 3% MERMA)", "unidad": "pza", "cantidad": 1.0300, "precio_unitario": 28.50, "fuente": "Insumos_APUCMX"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO)", "unidad": "jor", "cantidad": 0.007143, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR (5% M.O.)", "unidad": "%", "cantidad": 0.57, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 04 — ESTRUCTURA METÁLICA Y CUBIERTA
    # =========================================================================
    {
        "clave": "ED-04-01-005",
        "capitulo": "04",
        "subcapitulo": "01",
        "concepto": (
            "Suministro, habilitado y montaje de bastidor y largueros metálicos de soporte para cubierta inclinada "
            "en nivel +12.30 m (sección rectangular de 10x40 cm conforme a modelo estructural), incluye: cortes, "
            "soldadura E-7018, primario anticorrosivo, izaje, mano de obra, equipo y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf EST-04 (Básico 10502-059) por metro lineal de perfil",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado a partir de la matriz Neodata 02 PRECIOS UNITARIOS.pdf EST-04 ($42.76/kg × 14.5 kg/m de "
            "larguero tubular/montén reforzado para cubierta = $620.02/m). Alimentado por los 587 CurtainWallMullions "
            "de cubierta de Edificio de educacion (883.52 m)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "CurtainWallMullions",
                "filtro_tipo": "Montante rectangular - 10 x 40 cm",
                "campo_cantidad": "longitud_m",
            }
        ],
        "apu": [
            {"codigo": "313-HSS-0124", "descripcion": "PERFIL TUBULAR / LARGUERO ESTRUCTURAL PARA BASTIDOR DE CUBIERTA (14.5 KG/M)", "unidad": "ton", "cantidad": 0.014935, "precio_unitario": 18096.54, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "313-SOL-0101", "descripcion": "SOLDADURA ELECTRODO 7018 DE 5/32\" Y PRIMARIO GALVADUR", "unidad": "kg", "cantidad": 0.4500, "precio_unitario": 195.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1S2E", "descripcion": "CUADRILLA No 18 (1 OFICIAL SOLDADOR + 2 AYUDANTES ESPECIALIZADOS)", "unidad": "jor", "cantidad": 0.0850, "precio_unitario": 2572.48, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "EQGRUA", "descripcion": "GRUA DE PATIO DE 20 TON Y PLANTA DE SOLDAR", "unidad": "hr", "cantidad": 0.0220, "precio_unitario": 1854.76, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD", "unidad": "%", "cantidad": 2.55, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-04-02-003",
        "capitulo": "04",
        "subcapitulo": "02",
        "concepto": (
            "Sistema de losa de cubierta plana de azotea de 15 cm de espesor con relleno ligero de tezontle para "
            "dar pendiente pluvial del 2% y entortado de mortero cemento-arena 1:5 de 3 cm para recibir "
            "impermeabilizante en nivel de azotea (+12.30 m), incluye: materiales, elevación, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa IMP-6.5.1 (Entortado y relleno en azotea) + Tabulador CDMX GL14BH",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado para las 4 losas de azotea 'Generic 150mm' en Nivel - Azotea de TT_ED_EDUCACIÓN_CANCELERIA_2027 "
            "(1,113.73 m2): losa/entortado y relleno ligero de pendiente validado con Xalapa IMP-6.5.1 ($925.40/m2 CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Floors",
                "filtro_tipo": "Generic 150mm",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [
            {"codigo": "307-CON-0101", "descripcion": "CONCRETO Y MORTERO P/CUBIERTA DE AZOTEA E=15 CM C/RELLENO DE PENDIENTE", "unidad": "m3", "cantidad": 0.1650, "precio_unitario": 2335.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "d6c4fd62", "descripcion": "MALLA ELECTROSOLDADA 6X6-10/10 Y ACERO DE TEMPERATURA", "unidad": "m2", "cantidad": 1.0800, "precio_unitario": 115.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1A5P", "descripcion": "CUADRILLA No 22 (1 OFICIAL ALBAÑIL + 5 PEONES + 0.6 CABO)", "unidad": "jor", "cantidad": 0.0880, "precio_unitario": 4582.12, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ELEVACION (3% M.O.)", "unidad": "%", "cantidad": 12.70, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 05 — ALBAÑILERÍA
    # =========================================================================
    {
        "clave": "ED-05-01-003",
        "capitulo": "05",
        "subcapitulo": "01",
        "concepto": (
            "Muro de celosía exterior de barro extruido aparente en fachadas para control solar y ventilación "
            "cruzada natural (§6.2 y §7.3 memoria arquitectónica), asentado con mortero cemento-arena 1:4 y "
            "refuerzo horizontal con escalerilla, incluye: materiales, cortes, plomeo, andamios, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 03 BÁSICOS.pdf 1A1P",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para los 4 muros anfitriones 'Curtain Wall | Celosia Exterior' de Edificio de educacion "
            "(46.48 m2, D-019/P-011): pieza de celosía de barro extruido ($485.00/m2), mortero 1:4 ($58.40/m2) y "
            "cuadrilla 1A1P (rendimiento 7.0 m2/jor = $227.60/m2); CD = $782.40/m2."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "Walls",
                "filtro_tipo": "Celosia Exterior",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [
            {"codigo": "310-CEL-0150", "descripcion": "PIEZA DE CELOSIA DE BARRO EXTRUIDO APARENTE (INC. 5% DESPERDICIO)", "unidad": "m2", "cantidad": 1.0500, "precio_unitario": 461.90, "fuente": "Insumos_APUCMX"},
            {"codigo": "10401-544", "descripcion": "MORTERO CEMENTO-ARENA PROPORCION 1:4 HECHO EN OBRA", "unidad": "m3", "cantidad": 0.0250, "precio_unitario": 2336.00, "fuente": "Xalapa Básico 10401-544"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO)", "unidad": "jor", "cantidad": 0.142857, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (5% M.O.)", "unidad": "%", "cantidad": 11.40, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-05-01-004",
        "capitulo": "05",
        "subcapitulo": "01",
        "concepto": (
            "Muro divisorio interior ligero de block de concreto celular autoclavado (AAC) de 100 mm de espesor "
            "en mamparas y divisiones interiores, asentado con mortero adhesivo para block celular, incluye: "
            "materiales, cortes, nivelación, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "precio_unitario": 484.06,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave GC23CI (pág. 65)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave GC23CI (pág. 65): 'Muro de block hueco de concreto de 12 cm de "
            "espesor acabado común' — P.U. = $484.06/m2 (D-011). Mapeado a los 4 muros 'Muro 100 mm AAC COM' en "
            "TT_ED_EDUCACIÓN_CANCELERIA_2027 (7.22 m2, D-019)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Walls",
                "filtro_tipo": "Muro 100 mm AAC COM",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [],
    },
    {
        "clave": "ED-05-02-003",
        "capitulo": "05",
        "subcapitulo": "02",
        "concepto": (
            "Chaflán perimetral triangular de 10 x 10 cm de sección a base de mortero cemento-arena proporción "
            "1:4 en unión de losa de azotea con pretiles y muros para recibir sistema impermeabilizante, "
            "incluye: materiales, elevación, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa IMP-6.5.3 (Chaflán de mortero 10x10 cm, CD=$76.42/m)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz validada con Xalapa IMP-6.5.3 (Chaflán de mortero cemento-arena 1:4 de 10x10 cm en azoteas, "
            "Costo Directo = $76.42/m); alimentado por el perímetro de las losas de azotea 'Generic 150mm' (441.51 m)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Floors",
                "filtro_tipo": "Generic 150mm",
                "campo_cantidad": "longitud_m",
            }
        ],
        "apu": [
            {"codigo": "10401-544", "descripcion": "MORTERO CEMENTO-ARENA PROPORCION 1:4 HECHO EN OBRA", "unidad": "m3", "cantidad": 0.0065, "precio_unitario": 2336.00, "fuente": "Xalapa Básico 10401-544"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO) REND 28 M/JOR", "unidad": "jor", "cantidad": 0.0365, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR (5% M.O.)", "unidad": "%", "cantidad": 3.09, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 06 — ACABADOS, CARPINTERÍA ARQUITECTÓNICA Y EXTERIORES
    # =========================================================================
    {
        "clave": "ED-06-01-004",
        "capitulo": "06",
        "subcapitulo": "01",
        "concepto": (
            "Piso de concreto pulido densificado de alta resistencia a la abrasión con aplicación de densificador "
            "químico de silicato de litio y pulido mecánico con discos diamantados en talleres de oficios y "
            "laboratorios (§8.2.1 memoria arquitectónica), incluye: preparación, materiales, equipo y mano de obra."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 03 BÁSICOS.pdf 1A1P",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para el tipo 'Floor | Piso de concreto pulido densificado e= 0.002' de Proyecto "
            "acabado-DAMIAN (295.95 m2): densificador de silicato ($82.00/m2), consumibles de diamantado ($45.00/m2) "
            "y cuadrilla 1A1P (CD = $275.40/m2)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Floors",
                "filtro_tipo": "concreto pulido densificado",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [
            {"codigo": "308-DEN-0102", "descripcion": "DENSIFICADOR DE SILICATO DE LITIO Y SELLADOR P/CONCRETO PULIDO", "unidad": "lt", "cantidad": 0.3500, "precio_unitario": 362.86, "fuente": "Insumos_APUCMX"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO)", "unidad": "jor", "cantidad": 0.0880, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "PULIDORA DIAMANTADA Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 8.20, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-06-01-005",
        "capitulo": "06",
        "subcapitulo": "01",
        "concepto": (
            "Piso de porcelanato esmaltado rectificado tipo madera modelo Tavola Noce Mate de 20 x 120 cm en "
            "biblioteca, centro digital, administración y salas de lectura, asentado con adhesivo porcelánico "
            "de alta adherencia y boquilla epóxica/antimanchas, incluye: materiales, cortes, desperdicios, "
            "niveladores, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 02 PRECIOS UNITARIOS.pdf 1CO1A / Validado con Xalapa ACAB-6.13.9",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para el tipo 'Floor | Acabado - Porcelanato Esmaltado Tavola Noce Mate - 20x120' en "
            "TT_ED_EDUCACIÓN_CANCELERIA_2027 (596.50 m2): porcelanato 20x120 cm ($365.00/m2 + 6% desperdicio), "
            "adhesivo porcelánico ($54.00/m2) y cuadrilla 1CO1A (rendimiento 8.5 m2/jor = $204.47/m2); CD = $658.40/m2."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Floors",
                "filtro_tipo": "Porcelanato Esmaltado Tavola Noce Mate",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [
            {"codigo": "325-POR-2012", "descripcion": "PORCELANATO ESMALTADO RECTIFICADO TAVOLA NOCE MATE 20x120 CM (INC. 6% DESP.)", "unidad": "m2", "cantidad": 1.0600, "precio_unitario": 365.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "302-ADH-0102", "descripcion": "ADHESIVO PORCELANICO Y BOQUILLA SELLADA (SACO 20 KG)", "unidad": "pza", "cantidad": 0.3500, "precio_unitario": 154.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.117647, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y CORTADORA DE DISCO DIAMANTE", "unidad": "%", "cantidad": 13.13, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-06-01-006",
        "capitulo": "06",
        "subcapitulo": "01",
        "concepto": (
            "Sistema de piso exterior elevado/suspendido con base drenante, aislamiento y carpeta de concreto "
            "arquitectónico de 6.5 cm en pórticos de acceso, rampas y áreas exteriores cubiertas del edificio "
            "de educación (§8.2.1 memoria arquitectónica), incluye: materiales, juntas, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa OBR-EXT-11 ($484.40/m2) + 03 BÁSICOS.pdf",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado para los 3 elementos 'Floor | Floor-Grnd-Susp_65Scr-80Ins-100Blk-75PC' en "
            "TT_ED_EDUCACIÓN_CANCELERIA_2027 (233.31 m2), validado contra Xalapa OBR-EXT-11 ($545.20/m2 CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Floors",
                "filtro_tipo": "Floor-Grnd-Susp",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [
            {"codigo": "10401-292", "descripcion": "CONCRETO Y BASE DRENANTE P/PISO EXTERIOR EN PORTICOS Y ACCESOS", "unidad": "m3", "cantidad": 0.1250, "precio_unitario": 2660.76, "fuente": "Xalapa Básico 10401-292"},
            {"codigo": "d6c4fd62", "descripcion": "MALLA ELECTROSOLDADA 6X6-10/10 Y JUNTA DE DILATACION", "unidad": "m2", "cantidad": 1.0500, "precio_unitario": 52.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1A5P", "descripcion": "CUADRILLA No 22 (1 OFICIAL ALBAÑIL + 5 PEONES + 0.6 CABO)", "unidad": "jor", "cantidad": 0.0325, "precio_unitario": 4582.12, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR", "unidad": "%", "cantidad": 9.09, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-06-01-007",
        "capitulo": "06",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y tendido de sustrato de tierra vegetal preparada y gravilla/cubresuelos de 5 a 10 cm "
            "de espesor en jardineras interiores y áreas ajardinadas perimetrales del edificio de educación, "
            "incluye: nivelación, riego inicial, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "precio_unitario": 61.45,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave VB12BB (pág. 329)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave VB12BB (pág. 329): 'Suministro y tendido de gravilla/sustrato "
            "en áreas jardinadas' — P.U. = $61.45/m2 (D-011). Mapeado a 'Floor | Tierra 30mm' en "
            "TT_ED_EDUCACIÓN_CANCELERIA_2027 (6.43 m2)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Floors",
                "filtro_tipo": "Tierra 30mm",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [],
    },
    {
        "clave": "ED-06-02-003",
        "capitulo": "06",
        "subcapitulo": "02",
        "concepto": (
            "Suministro y colocación de lambrín y mampara divisoria de carpintería arquitectónica en madera "
            "natural/triplay enchapado de encino de 19 mm sobre bastidor tratado con acabado en barniz de "
            "poliuretano mate en aulas y biblioteca, incluye: herrajes de fijación, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa CARP-6.16.1 + Insumos_APUCMX",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para los 4 elementos 'Basic Wall | Madera' en TT_ED_EDUCACIÓN_CANCELERIA_2027 (20.88 m2): "
            "tablero y bastidor de madera tratada con barniz de poliuretano ($640.00/m2) más cuadrilla de carpintería "
            "(CD = $965.50/m2)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Walls",
                "filtro_tipo": "Basic Wall \\| Madera",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [
            {"codigo": "305-MAD-0119", "descripcion": "TABLERO Y BASTIDOR DE MADERA TRATADA C/BARNIZ DE POLIURETANO MATE", "unidad": "m2", "cantidad": 1.0500, "precio_unitario": 610.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1C1A", "descripcion": "CUADRILLA No 7 (1 OFICIAL CARPINTERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.166667, "precio_unitario": 1825.24, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y HERRAJES DE FIJACION", "unidad": "%", "cantidad": 20.79, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-06-03-002",
        "capitulo": "06",
        "subcapitulo": "03",
        "concepto": (
            "Suministro e instalación de falso plafón metálico microperforado arquitectónico marca Armstrong "
            "modelo MetalWorks Mesh Torsion Spring (Woven Square Weave, color Tech Black, módulos de 24\"x48\" "
            "y 14\"x24\") con suspensión de 15/16\" en vestíbulos, biblioteca y pasillos (§7.3 y §8.2.3 memoria "
            "arquitectónica), incluye: colganteo, nivelación láser, cortes, mano de obra, andamios y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa ACAB-6.13.2 ($634.42/m2) + 02 PRECIOS UNITARIOS.pdf 1CO1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para los 12 plafones 'PF_Plafon ACT - Armstrong Ceilings - METALWORKS Mesh Torsion Spring' "
            "modelados en categoría Floors de Proyecto acabado-DAMIAN (1,023.22 m2); CD = $748.50/m2."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Floors",
                "filtro_tipo": "PF_Plafon ACT - Armstrong",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [
            {"codigo": "321-PLA-0613", "descripcion": "PLAFON METALICO ARMSTRONG METALWORKS MESH TORSION SPRING TECH BLACK C/SUSPENSION 15/16\"", "unidad": "m2", "cantidad": 1.0500, "precio_unitario": 570.00, "fuente": "Insumos_APUCMX / Ref. Xalapa ACAB-6.13.2"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.0800, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (7.9% M.O.)", "unidad": "%", "cantidad": 10.96, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-06-03-003",
        "capitulo": "06",
        "subcapitulo": "03",
        "concepto": (
            "Plafón corrido resistente a la humedad con acabado cerámico / placa de cemento de 2 cm de espesor "
            "en núcleos sanitarios y áreas húmedas, incluye: bastidor galvanizado, colganteo, tratamiento de "
            "juntas, acabado, mano de obra, andamios y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Tabulador CDMX GE12JB ($947.88/m2) / Xalapa ACAB-6.13.1 ($548.20/m2)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para el elemento 'Floor | PF_Plafon de loseta ceramica de 2cm de espesor' de Proyecto "
            "acabado-DAMIAN (27.23 m2); CD = $584.20/m2."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Floors",
                "filtro_tipo": "PF_Plafon de loseta ceramica",
                "campo_cantidad": "area_m2",
            }
        ],
        "apu": [
            {"codigo": "321-PLA-0614", "descripcion": "PLACA Y RECUBRIMIENTO P/PLAFON EN ZONA HUMEDA C/BASTIDOR GALVANIZADO CAL. 22", "unidad": "m2", "cantidad": 1.0500, "precio_unitario": 410.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.083333, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS", "unidad": "%", "cantidad": 8.87, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 07 — HERRERÍA, CANCELERÍA Y CARPINTERÍA DE PUERTAS
    # =========================================================================
    {
        "clave": "ED-07-01-003",
        "capitulo": "07",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y colocación de puerta interior de carpintería de madera de 0.85 a 0.90 x 2.10 m con "
            "bastidor de pino estufado, vistas de triplay/MDF enchapado en melamina o encino barnizado y marco "
            "de madera/aluminio en oficinas, cubículos y servicios (§8.2.4 memoria arquitectónica), incluye: "
            "3 bisagras de libro, cerradura de intercomunicación, topes, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa CARP-6.16.1 + 02 PRECIOS UNITARIOS.pdf 1C1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para las 12 puertas 'puerta simple | puerta simple' de TT_ED_EDUCACIÓN_CANCELERIA_2027: "
            "hoja y marco de carpintería institucional ($3,850.00/pza), cerradura y bisagras ($680.00/pza) y "
            "cuadrilla 1C1A (0.35 jor = $638.83/pza); CD = $5,200.75/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Doors",
                "filtro_tipo": "puerta simple",
                "campo_cantidad": "conteo",
            }
        ],
        "apu": [
            {"codigo": "315-CAR-0821", "descripcion": "PUERTA DE CARPINTERIA DE MADERA / MELAMINA 0.85x2.10 M C/MARCO Y CHAMBRANA", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 3850.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "315-HER-0101", "descripcion": "JUEGO DE 3 BISAGRAS DE LIBRO 3 1/2\" Y CERRADURA DE PALANCA INSTITUCIONAL", "unidad": "jgo", "cantidad": 1.0000, "precio_unitario": 680.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1C1A", "descripcion": "CUADRILLA No 7 (1 OFICIAL CARPINTERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.3500, "precio_unitario": 1825.24, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR (5% M.O.)", "unidad": "%", "cantidad": 31.92, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-07-01-004",
        "capitulo": "07",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y colocación de puerta corrediza colgada de aluminio anodizado y cristal templado claro "
            "de 9.5 mm con riel superior de acero inoxidable sin perfil inferior en salas de estudio y talleres "
            "(§8.2.4 memoria arquitectónica), incluye: carretillas de uso pesado, jaladera H de acero inoxidable, "
            "mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 02 PRECIOS UNITARIOS.pdf 1H1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para las 6 puertas 'Puerta corrediza sin perfil.0001' de TT_ED_EDUCACIÓN_CANCELERIA_2027: "
            "hoja de cristal templado 9.5 mm con riel corredizo aéreo y herrajes ($5,420.00/pza) más cuadrilla 1H1A "
            "(0.50 jor = $818.81/pza); CD = $6,280.00/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Doors",
                "filtro_tipo": "Puerta corrediza",
                "campo_cantidad": "conteo",
            }
        ],
        "apu": [
            {"codigo": "315-COR-0921", "descripcion": "PUERTA CORREDIZA DE CRISTAL TEMPLADO 9.5 MM C/RIEL AEREO Y JALADERA INOX", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 5420.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1H1A", "descripcion": "CUADRILLA No 9 (1 OFICIAL CANCELERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.5000, "precio_unitario": 1637.61, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y SELLADOR (5% M.O.)", "unidad": "%", "cantidad": 41.19, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-07-02-003",
        "capitulo": "07",
        "subcapitulo": "02",
        "concepto": (
            "Suministro, habilitado y colocación de perfilería de montantes y travesaños (mullions) de aluminio "
            "anodizado estructural de 50x150 mm y 30x30 mm para fachada de muro cortina y celosías de cancelería, "
            "incluye: anclajes, neoprenos, tornillería inoxidable, sellado, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 02 PRECIOS UNITARIOS.pdf 1H1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para los 640 montantes de aluminio ('Rectangular Mullion | 50 x 150mm' y 'Cuadrado 30 mm') "
            "en TT_ED_EDUCACIÓN_CANCELERIA_2027__CurtainWallMullions.json (776.07 m); CD = $445.60/m."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "CurtainWallMullions",
                "filtro_tipo": ".*",
                "campo_cantidad": "longitud_m",
            }
        ],
        "apu": [
            {"codigo": "316-MUL-5015", "descripcion": "PERFIL MONTANTE DE ALUMINIO ANODIZADO 50x150 / 30x30 MM C/EMPAQUES Y ANCLAJES", "unidad": "m", "cantidad": 1.0500, "precio_unitario": 335.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1H1A", "descripcion": "CUADRILLA No 9 (1 OFICIAL CANCELERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0550, "precio_unitario": 1637.61, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS", "unidad": "%", "cantidad": 3.78, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-07-03-002",
        "capitulo": "07",
        "subcapitulo": "03",
        "concepto": (
            "Suministro, fabricación y montaje de escalera metálica principal de intercomunicación de planta "
            "baja (+5.30 m) a primer piso (+8.80 m) con alfardas de perfil estructural C/IPR, 20 escalones con "
            "huella de placa antiderrapante cal. 12 (H=28 cm, C=17.5 cm, ancho 1.40 m) y descanso intermedio, "
            "acabado con primario anticorrosivo y esmalte poliuretano, incluye: placas de anclaje, soldadura "
            "E-7018, montaje, mano de obra, equipo y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf EST-03 + Tabulador CDMX EC12CB ($65.13/kg × 920 kg)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para el elemento 'Assembled Stair | Escalera Metalica - C=17.5 H=28 cm' de "
            "TT_ED_EDUCACIÓN_CANCELERIA_2027__Stairs.json (1 pza): 920 kg de acero estructural en alfardas, "
            "descanso y huellas antiderrapantes + soldadura, primario y montaje con cuadrilla 1S2E (CD = $54,820.00/pza)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Stairs",
                "filtro_tipo": "Escalera Metalica",
                "campo_cantidad": "conteo",
            }
        ],
        "apu": [
            {"codigo": "313-HSS-0124", "descripcion": "ACERO ESTRUCTURAL EN ALFARDAS, DESCANSO Y HUELLAS ANTIDERRAPANTES (920 KG)", "unidad": "ton", "cantidad": 0.9476, "precio_unitario": 28500.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "313-SOL-0101", "descripcion": "SOLDADURA 7018, PRIMARIO GALVADUR Y ESMALTE POLIURETANO", "unidad": "kg", "cantidad": 35.0000, "precio_unitario": 195.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1S2E", "descripcion": "CUADRILLA No 18 (1 OFICIAL SOLDADOR + 2 AYUDANTES ESPECIALIZADOS)", "unidad": "jor", "cantidad": 7.5000, "precio_unitario": 2572.48, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "EQPLAN", "descripcion": "PLANTA DE SOLDAR MILLER Y EQUIPO DE CORTE", "unidad": "hr", "cantidad": 45.0000, "precio_unitario": 16.40, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y MANIOBRAS DE IZAJE", "unidad": "%", "cantidad": 956.10, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 08 — INSTALACIÓN HIDRÁULICA Y PLUVIAL
    # =========================================================================
    {
        "clave": "ED-08-01-005",
        "capitulo": "08",
        "subcapitulo": "01",
        "concepto": (
            "Suministro e instalación de manguera flexible alimentadora trenzada de acero inoxidable con "
            "interior de EPDM de 9.53 a 12.7 mm para conexión de muebles sanitarios, incluye: empaques, "
            "pruebas de presión, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 05 SALARIOS.pdf 1PL1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para los 5 elementos 'Flex Pipe Round | Domestic_Cold_Water · 9.53 mmø' en "
            "Instalaciones__FlexPipes.json (1.58 m); CD = $148.50/m."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "FlexPipes",
                "filtro_tipo": "Domestic_Cold_Water",
                "campo_cantidad": "longitud_m",
            }
        ],
        "apu": [
            {"codigo": "331-MAN-0101", "descripcion": "MANGUERA FLEXIBLE TRENZADA DE ACERO INOXIDABLE P/ALIMENTACION HIDRAULICA", "unidad": "m", "cantidad": 1.0000, "precio_unitario": 94.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1PL1A", "descripcion": "CUADRILLA PLOMERIA (1 OFICIAL PLOMERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0300, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR", "unidad": "%", "cantidad": 2.36, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-08-01-006",
        "capitulo": "08",
        "subcapitulo": "01",
        "concepto": (
            "Construcción de caja de registro para cuadro de válvulas de control de instalaciones hidráulicas "
            "en muro/piso de 0.30 x 0.60 m de sección con tabique rojo recocido, aplanado interior y tapa "
            "metálica registrable, incluye: materiales, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "precio_unitario": 367.05,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave GC27EB (pág. 65)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave GC27EB (pág. 65): 'Registro para cuadro de válvula de control "
            "de instalaciones en muro de tabique de 0.30 x 0.60 m de sección' — P.U. = $367.05/pza (D-011). "
            "Mapeado a las 26 instancias de 'Caja Registro DE VALVULAS' en Instalaciones__PipeAccessories.json."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "PipeAccessories",
                "filtro_tipo": "Caja Registro DE VALVULAS",
                "campo_cantidad": "conteo",
            }
        ],
        "apu": [],
    },
    {
        "clave": "ED-08-03-002",
        "capitulo": "08",
        "subcapitulo": "03",
        "concepto": (
            "Construcción de módulo de cisterna de almacenamiento subterráneo de concreto armado f'c=250 kg/cm2 "
            "con aditivo impermeabilizante integral (sistema bicompartimental para agua potable 20,000 L y agua "
            "pluvial 56,000 L conforme a modelo de Instalaciones y §9.1 memoria arquitectónica), incluye: "
            "excavación, plantilla, losa de fondo, muros y losa tapa de concreto armado, acabado interior "
            "pulido con mortero impermeabilizado, tapa registro hermética, escalera marina, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "precio_unitario": 64800.00,
        "fuente_tipo": "SUPUESTO",
        "fuente_ref": "SUPUESTO conservador desglosado con concreto FG12CB, acero DB12CC y cimbra CB12BD por módulo de cisterna",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "SUPUESTO conservador para cada uno de los 4 módulos de 'CISTERNA | Cisterna de almacenamiento "
            "subterráneo de concreto armado (76,000 L total = 19,000 L/módulo, 20.49 m3 de volumen geométrico por "
            "módulo)' en Instalaciones__MechanicalEquipment.json: concreto f'c=250 kg/cm2 impermeable ($34,800), "
            "acero de refuerzo ($13,500), cimbra y aplanado pulido impermeable ($11,200), excavación y accesorios ($5,300) "
            "= $64,800.00/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "MechanicalEquipment",
                "filtro_tipo": "^CISTERNA \\|",
                "campo_cantidad": "conteo",
            }
        ],
        "apu": [],
    },

    # =========================================================================
    # CAPÍTULO 09 — INSTALACIÓN SANITARIA
    # =========================================================================
    {
        "clave": "ED-09-01-004",
        "capitulo": "09",
        "subcapitulo": "01",
        "concepto": (
            "Suministro, instalación y pruebas de conexión flexible sanitaria / céspol de PVC de 50 mm (2\") "
            "para descarga de lavabos y muebles húmedos, incluye: adaptadores, empaques, mano de obra y herramienta."
        ),
        "unidad": "m",
        "precio_unitario": 140.50,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave HB19BB (pág. 100)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave HB19BB (pág. 100): 'Suministro, instalación y pruebas de céspol "
            "/ conexión de PVC para lavabo' — P.U. = $140.50 (D-011). Mapeado a los 3 elementos 'Flex Pipe Round "
            "| Sanitary · 50.80 mmø' en Instalaciones__FlexPipes.json (1.24 m)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "FlexPipes",
                "filtro_tipo": "Sanitary",
                "campo_cantidad": "longitud_m",
            }
        ],
        "apu": [],
    },
    {
        "clave": "ED-09-02-003",
        "capitulo": "09",
        "subcapitulo": "02",
        "concepto": (
            "Suministro, instalación y pruebas de mingitorio ecológico de cerámica vitrificada color blanco "
            "de bajo consumo (0.5 L por descarga o seco con trampa integrada) para núcleos sanitarios de "
            "hombres (§9.1 y §9.2 memoria arquitectónica), incluye: fijación a muro, brida, sellado con "
            "silicón antimicótico, pruebas, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "precio_unitario": 5403.81,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave HI13CP (pág. 114)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave HI13CP (pág. 114): 'Suministro, instalación y pruebas de "
            "Mingitorio modelo Niágara II marca American Standard o similar' — P.U. = $5,403.81/pza (D-011); "
            "validado contra Xalapa ACC-SAN-6.17.3 ($5,812.40/pza)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [],
    },

    # =========================================================================
    # CAPÍTULO 10 — INSTALACIÓN ELÉCTRICA Y FOTOVOLTAICA
    # =========================================================================
    {
        "clave": "ED-10-01-003",
        "capitulo": "10",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y tendido de tubería conduit metálica galvanizada pared delgada (EMT) de 13 a 19 mm "
            "de diámetro para circuitos derivados de iluminación en plafón y muros (§9.3 memoria arquitectónica), "
            "incluye: coples, conectores, abrazaderas tipo uña/omega, cortes, doblado, mano de obra, andamios y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + Xalapa INS-ELE-6.10.7 + 05 SALARIOS.pdf 1EL1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para los 440 tramos 'Conduit with Fittings | TUBO ILUMINACION -EMT- · 13 y 19 mmø' en "
            "Proyecto electrico_corregido__Conduits.json (526.29 m): tubo conduit EMT 13-19 mm con coples y "
            "abrazaderas ($54.00/m) más cuadrilla electricista 1EL1A (rendimiento 35 m/jor = $49.66/m); CD = $109.20/m."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "Conduits",
                "filtro_tipo": "TUBO ILUMINACION",
                "campo_cantidad": "longitud_m",
            }
        ],
        "apu": [
            {"codigo": "340-CON-0190", "descripcion": "TUBO CONDUIT GALVANIZADO PARED DELGADA (EMT) 13-19 MM C/ABRAZADERAS Y CONECTORES", "unidad": "m", "cantidad": 1.0500, "precio_unitario": 54.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1EL1A", "descripcion": "CUADRILLA ELECTRICISTA (1 OFICIAL ELECTRICISTA + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.028571, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (5.7% M.O.)", "unidad": "%", "cantidad": 2.84, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-10-01-004",
        "capitulo": "10",
        "subcapitulo": "01",
        "concepto": (
            "Suministro e instalación de accesorios y cajas de conexión para canalización conduit (cajas de "
            "registro tipo cruce, cajas octagonales, codos conduit, coples y reducciones de 13 a 25 mm de "
            "diámetro), incluye: fijación, tapa, conectores, mano de obra, andamios y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa INS-ELE-6.10.8 ($112.40/pza) e INS-ELE-6.10.9 ($136.96/pza)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU promedio ponderado para los 498 elementos de Proyecto electrico_corregido__ConduitFittings.json "
            "(247 cajas conduit cruce, 222 codos conduit, 25 reducciones, 2 cajas octagonales, 2 coples); "
            "validado contra Xalapa INS-ELE-6.10.8..9; CD = $78.60/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "ConduitFittings",
                "filtro_tipo": ".*",
                "campo_cantidad": "conteo",
            }
        ],
        "apu": [
            {"codigo": "340-FIT-0190", "descripcion": "CAJA DE CONEXION CONDUIT / CODO / REDUCCION 13-25 MM C/TAPA Y FIJACION", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 42.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1EL1A", "descripcion": "CUADRILLA ELECTRICISTA (1 OFICIAL ELECTRICISTA + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0200, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR (5.3% M.O.)", "unidad": "%", "cantidad": 1.84, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-10-01-005",
        "capitulo": "10",
        "subcapitulo": "01",
        "concepto": (
            "Suministro e instalación de curva horizontal/vertical de 90° tipo escalera de acero electrozincado "
            "de 250 x 75 mm para charola portacables principal, incluye: clemas de unión, tornillería, puente "
            "de unión a tierra, soportería, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 05 SALARIOS.pdf 1EL1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para las 4 curvas de charola ('Ladder Horizontal Bend' y 'Ladder Vertical Inside Bend' "
            "250x75 mm) en Proyecto electrico_corregido__CableTrayFittings.json; CD = $685.40/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "CableTrayFittings",
                "filtro_tipo": ".*",
                "campo_cantidad": "conteo",
            }
        ],
        "apu": [
            {"codigo": "340-CHA-0251", "descripcion": "CURVA 90° TIPO ESCALERA P/CHAROLA PORTACABLES 250x75 MM C/CLEMAS Y TORNILLERIA", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 538.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1EL1A", "descripcion": "CUADRILLA ELECTRICISTA (1 OFICIAL ELECTRICISTA + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0800, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS", "unidad": "%", "cantidad": 8.36, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-10-01-006",
        "capitulo": "10",
        "subcapitulo": "01",
        "concepto": (
            "Suministro, guiado y cableado de conductor eléctrico de cobre suave con aislamiento termoplástico "
            "THW-LS/THHW-LS 90°C, 600 V, calibre 12 AWG (línea de circuito de iluminación con fase, neutro y "
            "tierra física), marca Condumex o equivalente, incluye: cintas de identificación, pruebas de "
            "continuidad y aislamiento, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX (ppto_reftab_apuc_norm.csv) + 05 SALARIOS.pdf 1EL1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para los 232 tramos 'Wire Types | CABLE ILUMINACION' en "
            "Proyecto electrico_corregido__Wires.json (561.26 m); CD = $68.40/m."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "Wires",
                "filtro_tipo": "CABLE ILUMINACION",
                "campo_cantidad": "longitud_m",
            }
        ],
        "apu": [
            {"codigo": "341-CAB-0012", "descripcion": "CABLE DE COBRE THW-LS 90°C 600V CAL. 12 AWG CONDUMEX (PAR FASE+NEUTRO+TIERRA)", "unidad": "m", "cantidad": 2.6000, "precio_unitario": 18.20, "fuente": "Insumos_APUCMX"},
            {"codigo": "1EL1A", "descripcion": "CUADRILLA ELECTRICISTA (1 OFICIAL ELECTRICISTA + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0115, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "CINTA AISLANTE Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 1.09, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-10-01-007",
        "capitulo": "10",
        "subcapitulo": "01",
        "concepto": (
            "Suministro, guiado y cableado de conductor eléctrico de cobre suave con aislamiento termoplástico "
            "THW-LS/THHW-LS 90°C, 600 V, calibre 10 AWG para circuitos derivados de fuerza, contactos y "
            "potencia (§9.3 memoria arquitectónica), incluye: fase, neutro y tierra física, pruebas de "
            "aislamiento, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX (ppto_reftab_apuc_norm.csv) + 05 SALARIOS.pdf 1EL1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para los 116 tramos 'Wire Types | CABLE POTENCIA' en "
            "Proyecto electrico_corregido__Wires.json (430.04 m); CD = $96.80/m."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "Wires",
                "filtro_tipo": "CABLE POTENCIA",
                "campo_cantidad": "longitud_m",
            }
        ],
        "apu": [
            {"codigo": "341-CAB-0010", "descripcion": "CABLE DE COBRE THW-LS 90°C 600V CAL. 10 AWG CONDUMEX (CIRCUITO FUERZA)", "unidad": "m", "cantidad": 2.6000, "precio_unitario": 27.50, "fuente": "Insumos_APUCMX"},
            {"codigo": "1EL1A", "descripcion": "CUADRILLA ELECTRICISTA (1 OFICIAL ELECTRICISTA + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0138, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "CONECTORES, CINTA Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 1.32, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-10-02-003",
        "capitulo": "10",
        "subcapitulo": "02",
        "concepto": (
            "Suministro e instalación de luminaria LED tipo arbotante de pared con soporte arquitectónico "
            "de 18 W, 127-277 V, 4,000 K, IP54 para pasillos cubiertos, escaleras y accesos del edificio de "
            "educación (§9.3 memoria arquitectónica), incluye: fijación a muro, conexión, pruebas, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa LUM-ACC-6.11.8 ($948.55/pza) + 05 SALARIOS.pdf 1EL1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para las 18 luminarias 'LUMINARIA PARED Soporte HOME SMART | LAMPARA DE PARED' en "
            "Proyecto electrico_corregido__LightingFixtures.json; validado contra Xalapa LUM-ACC-6.11.8 ($948.55/pza CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "LightingFixtures",
                "filtro_tipo": "PARED",
                "campo_cantidad": "conteo",
            }
        ],
        "apu": [
            {"codigo": "LUM-ACC-6.11.8", "descripcion": "LUMINARIO ARBOTANTE LED DE PARED 18W 127-277V IP54 C/SOPORTE", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 718.00, "fuente": "Xalapa LUM-ACC-6.11.8"},
            {"codigo": "1EL1A", "descripcion": "CUADRILLA ELECTRICISTA (1 OFICIAL ELECTRICISTA + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.1250, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y TAQUETES (6% M.O.)", "unidad": "%", "cantidad": 13.30, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 13 — MOBILIARIO, CARPINTERÍA FIJA Y EQUIPAMIENTO
    # =========================================================================
    {
        "clave": "ED-13-02-003",
        "capitulo": "13",
        "subcapitulo": "02",
        "concepto": (
            "Suministro y colocación de pizarrón blanco acrílico magnético institucional de 3.66 x 1.22 m "
            "(144\" x 48\") con marco perimetral de aluminio anodizado, charola portaborrador y caballete "
            "móvil en aulas teóricas y talleres (§5.1 y §10 memoria arquitectónica), incluye: fijación a muro, "
            "nivelación, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 02 PRECIOS UNITARIOS.pdf 1CO1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para los pizarrones 'Steelcase - Premium Whiteboard 144W x 48H', 'MO. PIZARÓN' y "
            "'MobileEasel' en TT-ED-EDU-ARQ-MOB (13 pzas) y TT_ED_EDUCACIÓN_CANCELERIA_2027 (11 pzas); CD = $3,980.00/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT-ED-EDU-ARQ-MOB",
                "categoria": "Furniture",
                "filtro_tipo": "Whiteboard|PIZAR",
                "campo_cantidad": "conteo",
            },
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Furniture",
                "filtro_tipo": "Whiteboard|PIZAR",
                "campo_cantidad": "conteo",
            },
        ],
        "apu": [
            {"codigo": "350-PIZ-1448", "descripcion": "PIZARRON ACRILICO MAGNETICO INSTITUCIONAL 3.66x1.22 M (144\"x48\") C/MARCO ALUMINIO", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 3615.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.2000, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "TAQUETES Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 17.40, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-13-02-004",
        "capitulo": "13",
        "subcapitulo": "02",
        "concepto": (
            "Suministro y colocación de equipamiento complementario de estaciones de trabajo, mamparas de "
            "privacidad de resina para módulos de estudio, organizadores pasacables, papeleros metálicos y "
            "maceteros arquitectónicos de 40x40x100 cm con planta ornamental en biblioteca y centro digital "
            "(§10 memoria arquitectónica), incluye: armado, fijación, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 02 PRECIOS UNITARIOS.pdf 1CO1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU promedio ponderado para los elementos complementarios de mobiliario modular ('Planter_with_shrub', "
            "'Papelero', 'KO_Priority_Privacy-Screen', 'Cushion-Top', 'End-Support', 'Support-Rail', 'Bracket', "
            "'Wire-Manager', 'Desk - Base') en TT-ED-EDU-ARQ-MOB__Furniture.json; CD = $1,145.00/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT-ED-EDU-ARQ-MOB",
                "categoria": "Furniture",
                "filtro_tipo": "Planter|Papelero|Privacy-Screen|Cushion-Top|End-Support|Support-Rail|Bracket|Wire-Manager-Fillers|Desk - Base|WideScreenMonitor|Powerstrip|WEM61|optimizada|^11 \\||^12 \\||^62 \\|",
                "campo_cantidad": "conteo",
            }
        ],
        "apu": [
            {"codigo": "350-ACC-0101", "descripcion": "ACCESORIO MODULAR DE ESTACION DE TRABAJO / MAMPARA / MACETERO ARQUITECTONICO", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 1054.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0500, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR", "unidad": "%", "cantidad": 4.10, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 14 — LIMPIEZA FINAL Y ENTREGA
    # =========================================================================
    {
        "clave": "ED-14-01-003",
        "capitulo": "14",
        "subcapitulo": "01",
        "concepto": (
            "Limpieza general de áreas exteriores perimetrales, retiro final de escombro y sobrantes de obra "
            "en camión de volteo a tiro autorizado, pruebas integrales de entrega y carpeta de planos As-Built "
            "del edificio de educación (~2,500 m2), incluye: mano de obra, camión, equipo y herramienta."
        ),
        "unidad": "lote",
        "precio_unitario": 24500.00,
        "fuente_tipo": "SUPUESTO",
        "fuente_ref": "SUPUESTO conservador para retiro final de escombro, limpieza exterior y entrega final",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "SUPUESTO conservador integrado por 3 viajes finales de camión de volteo 7 m3 con cuadrilla 1P "
            "($11,500), limpieza de andadores/plazas exteriores ($7,500) e integración de carpeta técnica de "
            "pruebas y planos As-Built ($5,500) = $24,500.00/lote."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [],
    },
]
