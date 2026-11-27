"""Definición de conceptos y APUs para los capítulos 01 a 06 del Edificio de Educación (ED).

Agente: AG-2 (Precios)
Fuentes:
- Memoria arquitectónica (_harness/intermedios/pdf/memoria_arquitectonica.txt §4-§10)
- Resources/precios_procesados/*.csv (_harness/intermedios/precios/insumos_norm.json)
- Resources/resultado_ejemplo_neodata/ (01..11 PDFs)
- Resources/referencias_docs/PRESUPUESTO CENTRO DE INVESTIGACION XALAPA_MUÑOZ.pdf
"""
from __future__ import annotations

CAPITULOS_01_06: list[dict] = [
    # =========================================================================
    # CAPÍTULO 01 — PRELIMINARES
    # =========================================================================
    {
        "clave": "ED-01-01-001",
        "capitulo": "01",
        "subcapitulo": "01",
        "concepto": (
            "Limpia, desyerbe y desenraice del terreno en área de desplante del edificio de educación, "
            "incluye: acopio de maleza y basura, mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "precio_unitario": 12.46,
        "fuente_tipo": "TABULADOR_CDMX",
        "fuente_ref": "Tabulador CDMX Septiembre 2026 clave BC12BB (pág. 9)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Tabulador CDMX Septiembre 2026 clave BC12BB (pág. 9): 'Desyerbe y limpia del terreno realizada a mano, "
            "incluye: acarreo libre a 20 m', P.U. = $12.46/m2 (usado directo como costo directo conforme a D-011); "
            "validado contra APU Neodata ($16.35/m2) y Xalapa PREGEN-01 ($16.88/m2)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "MO011", "descripcion": "PEON (JORNADA 8 HRS, SALARIO REAL)", "unidad": "jor", "cantidad": 0.0208, "precio_unitario": 615.56, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "MO082", "descripcion": "CABO DE OFICIOS (JORNADA 8 HRS, SALARIO REAL)", "unidad": "jor", "cantidad": 0.0021, "precio_unitario": 1316.68, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 0.78, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-01-01-002",
        "capitulo": "01",
        "subcapitulo": "01",
        "concepto": (
            "Despalme de capa vegetal de 20 cm de espesor por medios manuales y mecánicos en área de desplante, "
            "medido en banco, incluye: acopio para reutilización en áreas verdes, mano de obra, equipo y herramienta."
        ),
        "unidad": "m3",
        "fuente_tipo": "APU",
        "fuente_ref": "Neodata/Xalapa PREGEN-02 (10302-002) + 05 SALARIOS.pdf",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con cuadrilla 1P ($747.23/jor, rendimiento 3.50 m3/jor = 0.2857 jor/m3) "
            "más herramienta menor; validado contra Xalapa PREGEN-02 ($234.46/m3 CD)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "MO011", "descripcion": "PEON (JORNADA 8 HRS, SALARIO REAL)", "unidad": "jor", "cantidad": 0.2857, "precio_unitario": 615.56, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "MO082", "descripcion": "CABO DE OFICIOS (JORNADA 8 HRS, SALARIO REAL)", "unidad": "jor", "cantidad": 0.0286, "precio_unitario": 1316.68, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 10.68, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-01-02-001",
        "capitulo": "01",
        "subcapitulo": "02",
        "concepto": (
            "Trazo y nivelación con equipo topográfico para desplante de estructuras y ejes de referencia del edificio "
            "de educación, estableciendo bancos de nivel, incluye: materiales de señalamiento, cuadrilla de topografía, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf PRE-01 (Básico 10301-002) / Validado con Xalapa PREGEN-09",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta del básico Neodata 10301-002 (02 PRECIOS UNITARIOS.pdf PRE-01, CD = $11.73/m2); "
            "validado contra Xalapa PREGEN-09 ($13.61/m2 CD)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "302-CAL-0102", "descripcion": "CALHIDRA, TONELADA", "unidad": "ton", "cantidad": 0.0002, "precio_unitario": 3034.40, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "305-M3A-0101", "descripcion": "DUELA DE PINO DE 3a DE 3/4x4x8' (0.019x0.10x2.44 m)", "unidad": "pza", "cantidad": 0.0100, "precio_unitario": 65.51, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "304-VAR-0101", "descripcion": "HILO CAÑAMO ROLLO DE 100 M", "unidad": "pza", "cantidad": 0.0010, "precio_unitario": 164.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "303-ARF-0201", "descripcion": "VARILLA R-42 DEL No. 3 (3/8 Ø), 0.557 KG/M", "unidad": "kg", "cantidad": 0.0200, "precio_unitario": 16.98, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "10401-291", "descripcion": "CONCRETO F'c=100 KG/CM2 HECHO EN OBRA P/MOJONERAS", "unidad": "m3", "cantidad": 0.0003, "precio_unitario": 2252.19, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "1T2E", "descripcion": "CUADRILLA No 32 (1 TOPOGRAFO + 2 AYUDANTES ESPECIALIZADOS)", "unidad": "jor", "cantidad": 0.003333, "precio_unitario": 2455.62, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "EQTRAN", "descripcion": "EQUIPO DE TOPOGRAFIA", "unidad": "hr", "cantidad": 0.0400, "precio_unitario": 16.89, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 0.41, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-01-03-001",
        "capitulo": "01",
        "subcapitulo": "03",
        "concepto": (
            "Construcción de bodega y oficina provisional de obra a base de bastidor ligero y lámina acanalada, "
            "con piso firme provisional de concreto pobre, incluye: materiales, montaje, desmontaje al término de la obra, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "SUPUESTO",
        "fuente_ref": "SUPUESTO conservador referenciado a Xalapa PREGEN-11 e insumos 11 RELACIÓN MATERIALES.pdf",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "SUPUESTO conservador para caseta/bodega provisional de obra con materiales recuperables "
            "(lámina Zintro R-101 cal. 22, polines de pino 3a y firme f'c=100 kg/cm2 de 8 cm), sin "
            "sobre-especificación de Xalapa PREGEN-11."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "precio_unitario": 1850.00,
        "apu": [],
    },

    # =========================================================================
    # CAPÍTULO 02 — CIMENTACIÓN (Modelo: Estructura)
    # =========================================================================
    {
        "clave": "ED-02-01-001",
        "capitulo": "02",
        "subcapitulo": "01",
        "concepto": (
            "Excavación en cepas a cielo abierto por medios manuales de 0.00 a -2.00 m de profundidad en material "
            "tipo II-A en seco para zapatas corridas y contratrabes, medido en banco, incluye: afine de taludes y fondo, "
            "traspaleos, acarreo libre a 20 m, mano de obra, equipo y herramienta."
        ),
        "unidad": "m3",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-02 (Básicos 10401-007 + 10401-106) / Validado con Xalapa CIM-6.2.1",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz directa de 02 PRECIOS UNITARIOS.pdf CIM-02 (Costo Directo = $425.93/m3: excavación 10401-007 "
            "$313.84/m3 + acarreo en carretilla 20 m 10401-106 $112.09/m3); validado contra Xalapa CIM-6.2.1 ($552.64/m3)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "10401-007", "descripcion": "EXCAVACION A CIELO ABIERTO MANUAL 0.00 A -2.00 M MAT. TIPO II-A (CUADRILLA 1P REND 2.5 M3/JOR)", "unidad": "m3", "cantidad": 1.00, "precio_unitario": 313.84, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "10401-106", "descripcion": "ACARREO EN CARRETILLA 1a ESTACION 20 M MEDIDO EN BANCO (CUADRILLA 1P REND 7.0 M3/JOR)", "unidad": "m3", "cantidad": 1.00, "precio_unitario": 112.09, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-02-01-002",
        "capitulo": "02",
        "subcapitulo": "01",
        "concepto": (
            "Plantilla de concreto simple hecho en obra f'c=100 kg/cm2 de 5 cm de espesor, T.M.A. 19 mm, para desplante "
            "de zapatas corridas y contratrabes, incluye: preparación y compactación de la superficie, nivelación, "
            "maestreado, colado, curado, mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-08 (Básico 10401-265) / Validado con Xalapa CIM-6.2.5",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz directa del básico Neodata 10401-265 en 02 PRECIOS UNITARIOS.pdf CIM-08 (Costo Directo = $175.70/m2); "
            "validado contra Xalapa CIM-6.2.5 ($203.71/m2 CD) y EST-6.3.13 ($216.60/m2 CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "Floors",
                "filtro_tipo": "Plantilla de concreto",
                "campo_cantidad": "area_m2",
                "nota": "Área de Plantilla de concreto e=5cm en modelo Edificio de educacion (804.20 m2).",
            }
        ],
        "apu": [
            {"codigo": "10401-291", "descripcion": "CONCRETO F'c=100 KG/CM2 HECHO EN OBRA, T.M.A. 19 MM", "unidad": "m3", "cantidad": 0.0505, "precio_unitario": 2252.19, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO)", "unidad": "jor", "cantidad": 0.037037, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 2.95, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-02-02-001",
        "capitulo": "02",
        "subcapitulo": "02",
        "concepto": (
            "Concreto premezclado estructural f'c=250 kg/cm2, clase 1, T.M.A. 20 mm, revenimiento 14 cm, bombeado "
            "en cimentación (zapatas corridas, dados y contratrabes de desplante), incluye: suministro, bombeo, "
            "colado, vibrado, curado, muestreo y pruebas de laboratorio, mano de obra, equipo y herramienta."
        ),
        "unidad": "m3",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-14 (Básico 10401-331) / Validado con Xalapa CIM-6.2.6",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz directa de 02 PRECIOS UNITARIOS.pdf CIM-14 (Costo Directo = $3,476.46/m3); "
            "validado contra Xalapa CIM-6.2.6 ($3,959.78/m3 CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFoundations",
                "filtro_tipo": "Dado para columnas|Zapata corrida",
                "campo_cantidad": "volumen_m3",
                "nota": "Volumen de concreto en zapatas corridas y dados de cimentación en Edificio de educacion.",
            },
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFraming",
                "filtro_tipo": "Trabe de cimentacion",
                "campo_cantidad": "volumen_m3",
                "nota": "Volumen de concreto en trabes de cimentación 20x40 en Edificio de educacion.",
            },
        ],
        "apu": [
            {"codigo": "307-CON-0101", "descripcion": "CONCRETO PREMEZCLADO F'c=250 KG/CM2 CLASE 1 BOMBEADO", "unidad": "m3", "cantidad": 1.0200, "precio_unitario": 2335.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "358-AGU-0101", "descripcion": "AGUA DE TOMA PARA CURADO", "unidad": "m3", "cantidad": 0.1200, "precio_unitario": 35.52, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "ma0000000015", "descripcion": "PRUEBA DE LABORATORIO EN CONCRETO", "unidad": "pza", "cantidad": 0.047619, "precio_unitario": 3000.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1A5P", "descripcion": "CUADRILLA No 22 (1 OFICIAL ALBAÑIL + 5 PEONES + 0.6 CABO)", "unidad": "jor", "cantidad": 0.181818, "precio_unitario": 4582.12, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "EQVIB", "descripcion": "VIBRADOR PARA CONCRETO 4 HP GASOLINA", "unidad": "hr", "cantidad": 0.5000, "precio_unitario": 145.75, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 41.65, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-02-02-002",
        "capitulo": "02",
        "subcapitulo": "02",
        "concepto": (
            "Cimbra común en cimentación (zapatas corridas, dados y contratrabes) a base de triplay de pino de 19 mm "
            "y madera de pino de 3a (4 usos), incluye: habilitado, cimbrado, chaflanes, desmoldante, descimbrado, "
            "acarreos, mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-13 (Básico BA0000000001) / Validado con Xalapa CIM-6.2.8..10",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz directa de 02 PRECIOS UNITARIOS.pdf CIM-13 (Costo Directo = $633.47/m2) con madera de pino "
            "de 3a y triplay 19 mm a 4 usos más cuadrilla 1C1A; validado contra Xalapa CIM-6.2.8 ($391.29/m2 CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFoundations",
                "filtro_tipo": "Dado para columnas|Zapata corrida",
                "campo_cantidad": "area_m2",
                "nota": "Área de contacto/cimbra en dados y zapatas corridas en Edificio de educacion.",
            },
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFraming",
                "filtro_tipo": "Trabe de cimentacion",
                "campo_cantidad": "area_m2",
                "nota": "Área de cimbra en trabes de cimentación 20x40 en Edificio de educacion.",
            },
        ],
        "apu": [
            {"codigo": "BA0000000001", "descripcion": "CIMBRA EN CIMENTACION (ZAPATAS, DADOS, CONTRATRABES) PROPORCION 4 USOS", "unidad": "m2", "cantidad": 0.2500, "precio_unitario": 1141.91, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "1C1A", "descripcion": "CUADRILLA No 7 (1 OFICIAL CARPINTERO O.N. + 1 AYUDANTE + 0.1 CABO) CIMBRADO Y DESCIMBRADO", "unidad": "jor", "cantidad": 0.181579, "precio_unitario": 1825.24, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 16.57, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-02-02-003",
        "capitulo": "02",
        "subcapitulo": "02",
        "concepto": (
            "Acero de refuerzo en cimentación fy=4,200 kg/cm2 con varilla corrugada del No. 3 (3/8\") al No. 6 (3/4\"), "
            "incluye: suministro, acarreos, cortes, habilitado, dobleces, ganchos, traslapes, amarres con alambre "
            "recocido cal. 16, silletas, desperdicios, mano de obra, equipo y herramienta."
        ),
        "unidad": "kg",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-09 y CIM-10 (Básicos 10401-172 y 10401-173) / Validado con Xalapa CIM-6.2.4",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz directa del básico Neodata 10401-172/173 (02 PRECIOS UNITARIOS.pdf CIM-09 CD=$29.04/kg y "
            "CIM-10 CD=$27.79/kg; promedio ponderado $28.39/kg); validado contra Xalapa CIM-6.2.4 ($40.17/kg CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "Rebar",
                "filtro_tipo": "Varilla del #5|Estribos #4",
                "campo_cantidad": "peso_kg",
                "nota": "Peso de acero de refuerzo principal (#5 y estribos #4) modelado en Edificio de educacion.",
            }
        ],
        "apu": [
            {"codigo": "303-ARF-0301", "descripcion": "VARILLA CORRUGADA R-42 FY=4200 KG/CM2 No. 3 A No. 6 (INCLUYE 7% DESPERDICIO Y TRASLAPES)", "unidad": "kg", "cantidad": 1.0700, "precio_unitario": 16.98, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "303-ARF-1101", "descripcion": "ALAMBRE RECOCIDO CAL. 16 (1.59 MM)", "unidad": "kg", "cantidad": 0.0450, "precio_unitario": 25.86, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1F1A", "descripcion": "CUADRILLA No 6 (1 OFICIAL FIERRERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.004724, "precio_unitario": 1825.24, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 0.43, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-02-03-001",
        "capitulo": "02",
        "subcapitulo": "03",
        "concepto": (
            "Relleno en cepas de cimentación y para alcanzar niveles de proyecto con material de banco (tepetate) "
            "compactado con equipo mecánico (rodillo vibratorio/bailarina) al 90% Proctor en capas de 15 cm de espesor, "
            "medido compacto, incluye: suministro de tepetate, incorporación de agua, acarreos internos, mano de obra, equipo y herramienta."
        ),
        "unidad": "m3",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-15 (Básicos 14301-024 + 10401-106)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta de 02 PRECIOS UNITARIOS.pdf CIM-15 (Costo Directo = $939.94/m3: básico 14301-024 "
            "relleno compactado con tepetate $827.85/m3 + básico 10401-106 acarreo libre a 20 m $112.09/m3)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "301-TEP-0103", "descripcion": "TEPETATE PUESTO EN OBRA (FACTOR ABUNDAMIENTO 1.30)", "unidad": "m3", "cantidad": 1.3000, "precio_unitario": 400.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "358-AGU-0201", "descripcion": "AGUA DE PIPA PARA COMPACTACION", "unidad": "m3", "cantidad": 0.1500, "precio_unitario": 107.90, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1P-U", "descripcion": "CUADRILLA No 71 (1 PEON URBANIZACION + MANDO INTERMEDIO)", "unidad": "jor", "cantidad": 0.2500, "precio_unitario": 723.20, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "EQRVIBRA", "descripcion": "RODILLO VIBRATORIO WACKER DE 1/2 TON", "unidad": "hr", "cantidad": 0.6700, "precio_unitario": 151.97, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "10401-106", "descripcion": "ACARREO EN CARRETILLA 1a ESTACION DE 20 M", "unidad": "m3", "cantidad": 1.0000, "precio_unitario": 112.09, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 9.04, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-02-03-002",
        "capitulo": "02",
        "subcapitulo": "03",
        "concepto": (
            "Carga manual y acarreo en camión de volteo a primer kilómetro de material sobrante producto de "
            "excavaciones, volumen medido en banco, incluye: mano de obra, camión de volteo de 7 m3, equipo y herramienta."
        ),
        "unidad": "m3",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-06 (Básico 10401-102) / Validado con Xalapa CIM-6.2.3",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta de 02 PRECIOS UNITARIOS.pdf CIM-06 (Básico 10401-102, Costo Directo = $377.75/m3); "
            "validado contra Xalapa CIM-6.2.3 ($519.33/m3 CD)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "1P", "descripcion": "CUADRILLA No 1 (1 PEON + 0.1 CABO) RENDIMIENTO 6.00 M3/JOR", "unidad": "jor", "cantidad": 0.166667, "precio_unitario": 747.23, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "EQCAMION", "descripcion": "CAMION DE VOLTEO DE 7 M3 DIESEL 160 HP", "unidad": "hr", "cantidad": 0.2500, "precio_unitario": 987.90, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 6.23, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 03 — ESTRUCTURA DE CONCRETO (Modelo: Estructura)
    # =========================================================================
    {
        "clave": "ED-03-01-001",
        "capitulo": "03",
        "subcapitulo": "01",
        "concepto": (
            "Concreto premezclado estructural f'c=250 kg/cm2 en columnas, castillos y elementos verticales, "
            "clase 1, T.M.A. 20 mm, bombeado hasta nivel +8.80 m, incluye: suministro, bombeo, colado, vibrado, "
            "curado, pruebas de laboratorio, mano de obra, equipo y herramienta."
        ),
        "unidad": "m3",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-14 ajustado a columnas + Xalapa EST-6.3.2",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado con concreto premezclado f'c=250 kg/cm2 (307-CON-0101 $2,335/m3 con 3% desperdicio), "
            "cuadrilla 1A5P (rendimiento 4.5 m3/jor en elementos verticales), vibrador y pruebas; "
            "CD = $3,712.56/m3, validado contra Xalapa EST-6.3.2 ($4,063.98/m3 CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralColumns",
                "filtro_tipo": "Pilar rectangular|Columna|Castillo|Zona de castillo",
                "campo_cantidad": "volumen_m3",
                "nota": "Volumen de columnas y castillos de concreto en modelo Edificio de educacion (19.86 m3).",
            }
        ],
        "apu": [
            {"codigo": "307-CON-0101", "descripcion": "CONCRETO PREMEZCLADO F'c=250 KG/CM2 CLASE 1 BOMBEADO", "unidad": "m3", "cantidad": 1.0300, "precio_unitario": 2335.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "358-AGU-0101", "descripcion": "AGUA DE TOMA PARA CURADO", "unidad": "m3", "cantidad": 0.1500, "precio_unitario": 35.52, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "ma0000000015", "descripcion": "PRUEBA DE LABORATORIO EN CONCRETO", "unidad": "pza", "cantidad": 0.047619, "precio_unitario": 3000.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1A5P", "descripcion": "CUADRILLA No 22 (1 OFICIAL ALBAÑIL + 5 PEONES + 0.6 CABO)", "unidad": "jor", "cantidad": 0.222222, "precio_unitario": 4582.12, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "EQVIB", "descripcion": "VIBRADOR PARA CONCRETO 4 HP GASOLINA", "unidad": "hr", "cantidad": 0.6500, "precio_unitario": 145.75, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 50.91, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-03-01-002",
        "capitulo": "03",
        "subcapitulo": "01",
        "concepto": (
            "Cimbra acabado aparente en columnas, castillos, trabes y cerramientos de concreto a base de triplay "
            "de pino de 19 mm y madera de pino de 3a, con chaflanes en esquinas, incluye: obra falsa, habilitado, "
            "cimbrado, desmoldante, descimbrado, elevaciones, mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa EST-6.3.1 ($596.34/m2) y EST-6.3.6 ($570.71/m2) + 02 PRECIOS UNITARIOS.pdf CIM-13",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con básico de madera de cimbra BA0000000001 (4 usos) y cuadrilla 1C1A (02 PRECIOS "
            "UNITARIOS.pdf CIM-13); CD = $588.35/m2, validado contra Xalapa EST-6.3.1 ($596.34/m2 CD) y EST-6.3.6 ($570.71/m2 CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralColumns",
                "filtro_tipo": "Pilar rectangular|Columna|Castillo",
                "campo_cantidad": "area_m2",
                "nota": "Área de cimbra en columnas y castillos de concreto en Edificio de educacion.",
            },
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFraming",
                "filtro_tipo": "Dala de cerramiento|Dala de desplante|Trabe de concreto",
                "campo_cantidad": "area_m2",
                "nota": "Área de cimbra en trabes y dalas de concreto en Edificio de educacion.",
            },
        ],
        "apu": [
            {"codigo": "BA0000000001", "descripcion": "CIMBRA DE MADERA Y TRIPLAY 19 MM (PROPORCION POR USO EN ESTRUCTURA)", "unidad": "m2", "cantidad": 0.2500, "precio_unitario": 1141.91, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "1C1A", "descripcion": "CUADRILLA No 7 (1 OFICIAL CARPINTERO O.N. + 1 AYUDANTE + 0.1 CABO)", "unidad": "jor", "cantidad": 0.1580, "precio_unitario": 1825.24, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 14.48, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-03-02-001",
        "capitulo": "03",
        "subcapitulo": "02",
        "concepto": (
            "Concreto premezclado estructural f'c=250 kg/cm2 en trabes, cadenas de cerramiento y dalas de "
            "confinamiento, clase 1, T.M.A. 20 mm, bombeado, incluye: suministro, bombeo, colado, vibrado, "
            "curado, pruebas de laboratorio, mano de obra, equipo y herramienta."
        ),
        "unidad": "m3",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-14 ajustado a trabes + Xalapa EST-6.3.8",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Misma matriz de concreto estructural f'c=250 kg/cm2 bombeado en superestructura (CD = $3,712.56/m3); "
            "validado contra Xalapa EST-6.3.8 ($4,063.98/m3 CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "StructuralFraming",
                "filtro_tipo": "Dala de cerramiento|Dala de desplante|Trabe de concreto",
                "campo_cantidad": "volumen_m3",
                "nota": "Volumen de trabes, cadenas y dalas de concreto en modelo Edificio de educacion (64.93 m3).",
            }
        ],
        "apu": [
            {"codigo": "307-CON-0101", "descripcion": "CONCRETO PREMEZCLADO F'c=250 KG/CM2 CLASE 1 BOMBEADO", "unidad": "m3", "cantidad": 1.0300, "precio_unitario": 2335.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "358-AGU-0101", "descripcion": "AGUA DE TOMA PARA CURADO", "unidad": "m3", "cantidad": 0.1500, "precio_unitario": 35.52, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "ma0000000015", "descripcion": "PRUEBA DE LABORATORIO EN CONCRETO", "unidad": "pza", "cantidad": 0.047619, "precio_unitario": 3000.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1A5P", "descripcion": "CUADRILLA No 22 (1 OFICIAL ALBAÑIL + 5 PEONES + 0.6 CABO)", "unidad": "jor", "cantidad": 0.222222, "precio_unitario": 4582.12, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "EQVIB", "descripcion": "VIBRADOR PARA CONCRETO 4 HP GASOLINA", "unidad": "hr", "cantidad": 0.6500, "precio_unitario": 145.75, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 50.91, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-03-02-002",
        "capitulo": "03",
        "subcapitulo": "02",
        "concepto": (
            "Acero de refuerzo en superestructura (columnas, castillos, trabes y cadenas) fy=4,200 kg/cm2 con "
            "varilla corrugada del No. 3 (3/8\") al No. 8 (1\"), incluye: suministro, acarreos, elevaciones, "
            "cortes, habilitado, ganchos, traslapes, amarres con alambre recocido cal. 16, desperdicios, mano de obra y herramienta."
        ),
        "unidad": "kg",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-09..11 (Básicos 10401-172..176) / Validado con Xalapa EST-6.3.7",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz de acero de refuerzo en estructura con varilla R-42 y cuadrilla 1F1A (rendimiento 190 kg/jor "
            "incluyendo elevación en PB y PA); CD = $29.85/kg ($29,850/ton), validado contra Xalapa EST-6.3.7 ($32,146.14/ton CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "Rebar",
                "filtro_tipo": "Varilla$|Estribos #3|Varilla #4|Varilla del #2",
                "campo_cantidad": "peso_kg",
                "nota": "Peso de acero de refuerzo en superestructura modelado en Edificio de educacion (3,539.74 kg).",
            }
        ],
        "apu": [
            {"codigo": "303-ARF-0301", "descripcion": "VARILLA CORRUGADA R-42 FY=4200 KG/CM2 (PROMEDIO No. 3 A No. 8, INC. 7% DESPERDICIO)", "unidad": "kg", "cantidad": 1.0700, "precio_unitario": 17.85, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "303-ARF-1101", "descripcion": "ALAMBRE RECOCIDO CAL. 16 (1.59 MM)", "unidad": "kg", "cantidad": 0.0450, "precio_unitario": 25.86, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1F1A", "descripcion": "CUADRILLA No 6 (1 OFICIAL FIERRERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.005263, "precio_unitario": 1825.24, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 0.48, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-03-03-001",
        "capitulo": "03",
        "subcapitulo": "03",
        "concepto": (
            "Losa prefabricada de entrepiso de vigueta pretensada de concreto y bovedilla de cemento-arena de 25 cm "
            "de peralte total, con capa de compresión de 5 cm de concreto premezclado f'c=250 kg/cm2 reforzada con "
            "malla electrosoldada 6x6/10-10, conforme a memoria arquitectónica (§8.1.3), incluye: suministro y montaje "
            "de viguetas y bovedillas, apuntalamiento provisional, frontera perimetral, colado, vibrado, curado, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX (malla 6x6/10-10 + concreto 307-CON-0101 + vigueta y bovedilla) / Validado con Xalapa EST-6.3.11",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para sistema de vigueta pretensada y bovedilla de concreto con capa de compresión de 5 cm "
            "f'c=250 kg/cm2 y malla 6x6/10-10 (§8.1.3 memoria arquitectónica); CD = $1,148.52/m2, validado contra "
            "losa aligerada Xalapa EST-6.3.11 ($1,821.94/m2 CD con casetón y nervaduras en sitio)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "Floors",
                "filtro_tipo": "vigueta y bovedilla|Capa de compresion",
                "campo_cantidad": "area_m2",
                "nota": "Área de losa de vigueta y bovedilla e=0.25 y capa de compresión en Edificio de educacion (753.11 m2).",
            }
        ],
        "apu": [
            {"codigo": "VB-VIG-01", "descripcion": "VIGUETA PRETENSADA DE CONCRETO P/LOSA DE 20+5 CM (A CADA 0.75 M)", "unidad": "m", "cantidad": 1.3800, "precio_unitario": 185.00, "fuente": "Insumos_APUCMX / Mercado regional"},
            {"codigo": "VB-BOV-01", "descripcion": "BOVEDILLA DE CEMENTO-ARENA 15x25x56 CM (8.5 PZAS/M2)", "unidad": "pza", "cantidad": 8.6700, "precio_unitario": 28.50, "fuente": "Insumos_APUCMX / Mercado regional"},
            {"codigo": "d6c4fd62", "descripcion": "MALLA ELECTROSOLDADA 6X6-10/10 (INC. 8% TRASLAPE)", "unidad": "m2", "cantidad": 1.0800, "precio_unitario": 41.05, "fuente": "Insumos_APUCMX / Xalapa EST-6.3.12"},
            {"codigo": "307-CON-0101", "descripcion": "CONCRETO PREMEZCLADO F'c=250 KG/CM2 CLASE 1 P/CAPA DE COMPRESION Y NERVIOS", "unidad": "m3", "cantidad": 0.0680, "precio_unitario": 2335.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "305-M3A-0302", "descripcion": "POLIN DE PINO DE 3a DE 4x4x8' P/APUNTALAMIENTO (4 USOS)", "unidad": "pza", "cantidad": 0.4500, "precio_unitario": 206.89, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1A5P", "descripcion": "CUADRILLA No 22 (1 OFICIAL ALBAÑIL + 5 PEONES + 0.6 CABO)", "unidad": "jor", "cantidad": 0.0720, "precio_unitario": 4582.12, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR, EQUIPO Y VIBRADO (6% M.O.)", "unidad": "%", "cantidad": 19.99, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 04 — ESTRUCTURA METÁLICA Y CUBIERTA (Modelos: Estructura / ARQ)
    # =========================================================================
    {
        "clave": "ED-04-01-001",
        "capitulo": "04",
        "subcapitulo": "01",
        "concepto": (
            "Suministro, fabricación, transporte y montaje de estructura metálica principal y secundaria a base de "
            "perfiles tubulares HSS/OR y perfiles laminados IPR (columnas metálicas, cerchas/armaduras para grandes "
            "claros, correas y arriostramientos), conforme a memoria arquitectónica (§8.1.4), incluye: cortes, "
            "soldadura E-7018, limpieza de superficie, aplicación de primario anticorrosivo a base de inorgánico "
            "de zinc a 2.5 milésimas de espesor, montaje con grúa a cualquier altura, mano de obra, equipo y herramienta."
        ),
        "unidad": "kg",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf EST-03 (Básico 10502-057, CD=$41.88/kg) y EST-04 (Básico 10502-059, CD=$42.76/kg)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz directa del básico Neodata 10502-057 en 02 PRECIOS UNITARIOS.pdf EST-03 (Costo Directo = $41.88/kg "
            "para perfiles HSS/OR, columnas y armaduras con primario anticorrosivo Galvadur y grúa de 20 ton)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "StructuralFraming",
                "filtro_tipo": "Canal C|C310X45",
                "campo_cantidad": "peso_kg",
                "nota": "Peso en kg de vigas y canales metálicos C310X45 en TT_ED_EDUCACIÓN_CANCELERIA_2027 (4,209.06 kg).",
            },
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "StructuralColumns",
                "filtro_tipo": "Pilar L|L150x12",
                "campo_cantidad": "peso_kg",
                "nota": "Peso en kg de columnas metálicas L150x12 en TT_ED_EDUCACIÓN_CANCELERIA_2027 (251.96 kg).",
            },
        ],
        "apu": [
            {"codigo": "313-HSS-0124", "descripcion": "PERFIL ESTRUCTURAL HSS / LAMINADO A-36/A-500 (INC. 3% DESPERDICIO)", "unidad": "ton", "cantidad": 0.001030, "precio_unitario": 18096.54, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "313-SOL-0101", "descripcion": "SOLDADURA ELECTRODO 7018 DE 5/32\" (4 MM)", "unidad": "kg", "cantidad": 0.0200, "precio_unitario": 67.06, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "337-SVT-0302", "descripcion": "THINNER ESTANDAR", "unidad": "lt", "cantidad": 0.0030, "precio_unitario": 43.66, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "ma0000000016", "descripcion": "PRIMARIO GALVADUR A BASE DE ZINC", "unidad": "lt", "cantidad": 0.0080, "precio_unitario": 538.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1S2E", "descripcion": "CUADRILLA No 18 (1 OFICIAL SOLDADOR + 2 AYUDANTES ESPECIALIZADOS + 0.1 SOBRESTANTE)", "unidad": "jor", "cantidad": 0.0050, "precio_unitario": 2572.48, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "EQPLAN", "descripcion": "PLANTA DE SOLDAR MILLER 300 AMP", "unidad": "hr", "cantidad": 0.0150, "precio_unitario": 16.40, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "EQGRUA", "descripcion": "GRUA DE PATIO DE 20 TON DIESEL", "unidad": "hr", "cantidad": 0.0020, "precio_unitario": 1854.76, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 0.65, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-04-01-002",
        "capitulo": "04",
        "subcapitulo": "01",
        "concepto": (
            "Suministro, fabricación y colocación de placas base y cartabones de acero A-36 de 1/2\" (12.7 mm), "
            "incluye: cortes con oxiacetileno, perforaciones, soldadura E-7018, primario anticorrosivo a base de "
            "zinc, nivelación, mano de obra, equipo y herramienta."
        ),
        "unidad": "kg",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf EST-01 (Básico 10502-055)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta de 02 PRECIOS UNITARIOS.pdf EST-01 (Básico 10502-055, Costo Directo = $55.39/kg)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "313-APL-0105", "descripcion": "PLACA DE ACERO A-36 DE 1/2\" (12.7 MM) 99.6 KG/M2 (INC. 3% DESPERDICIO)", "unidad": "ton", "cantidad": 0.001030, "precio_unitario": 28500.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "313-SOL-0101", "descripcion": "SOLDADURA ELECTRODO 7018 DE 5/32\" (4 MM)", "unidad": "kg", "cantidad": 0.0400, "precio_unitario": 67.06, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "337-SVT-0302", "descripcion": "THINNER ESTANDAR", "unidad": "lt", "cantidad": 0.0040, "precio_unitario": 43.66, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "ma0000000016", "descripcion": "PRIMARIO GALVADUR A BASE DE ZINC", "unidad": "lt", "cantidad": 0.0080, "precio_unitario": 538.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1S2E", "descripcion": "CUADRILLA No 18 (1 OFICIAL SOLDADOR + 2 AYUDANTES ESPECIALIZADOS)", "unidad": "jor", "cantidad": 0.0050, "precio_unitario": 2572.48, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "EQECORTE", "descripcion": "EQUIPO DE CORTE OXI-ACETILENO", "unidad": "hr", "cantidad": 0.0018, "precio_unitario": 319.10, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "EQGRUA", "descripcion": "GRUA DE PATIO DE 20 TON", "unidad": "hr", "cantidad": 0.0025, "precio_unitario": 1854.76, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "EQPLAN", "descripcion": "PLANTA DE SOLDAR MILLER", "unidad": "hr", "cantidad": 0.0100, "precio_unitario": 16.40, "fuente": "08 COSTOS HORARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 0.65, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-04-01-003",
        "capitulo": "04",
        "subcapitulo": "01",
        "concepto": (
            "Suministro, fabricación y colocación de anclas de acero cold rolled de 1\" x 1.40 m de desarrollo total "
            "con cuerda de 10 cm, doblez de 30 cm, tuerca y arandela de presión, con relleno de nivelación grout no "
            "metálico bajo placa base, incluye: fijado, plomeado, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf CIM-12 (CD=$511.65/pza) + EST-02 (grout $31.64/kg)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz directa de 02 PRECIOS UNITARIOS.pdf CIM-12 (Costo Directo = $511.65/pza) para ancla cold "
            "rolled de 1\"x1.40 m colocada y plomeada."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "MA0000000001", "descripcion": "ANCLA DE ACERO COLD ROLLED 1\"x1.40 M C/TUERCA Y ARANDELA DE PRESION", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 320.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1F1A", "descripcion": "CUADRILLA No 6 (1 OFICIAL FIERRERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.1000, "precio_unitario": 1825.24, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 9.13, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-04-01-004",
        "capitulo": "04",
        "subcapitulo": "01",
        "concepto": (
            "Pintura de acabado epóxico / poliuretano anticorrosivo tipo Amerlock 400 a 4 milésimas de espesor en "
            "estructura metálica expuesta, aplicada a dos manos, incluye: preparación de la superficie, materiales, "
            "solventes, andamios, mano de obra, equipo y herramienta."
        ),
        "unidad": "kg",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf EST-05 (Básico 10806-008)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta de 02 PRECIOS UNITARIOS.pdf EST-05 (Básico 10806-008, Costo Directo = $18.18/kg)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "337-COM-1102", "descripcion": "PINTURA ACABADO AMERLOCK 400 A 4 MILESIMAS DE ESPESOR", "unidad": "lt", "cantidad": 0.0150, "precio_unitario": 752.89, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "337-SVT-0302", "descripcion": "THINNER (LATA 19 LTS)", "unidad": "lt", "cantidad": 0.0150, "precio_unitario": 43.66, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1P1A", "descripcion": "CUADRILLA No 8 (1 OFICIAL PINTOR + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.003333, "precio_unitario": 1705.11, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR, ANDAMIOS Y EQUIPO DE SEGURIDAD (10% M.O.)", "unidad": "%", "cantidad": 0.56, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-04-02-001",
        "capitulo": "04",
        "subcapitulo": "02",
        "concepto": (
            "Suministro y colocación de cubierta de panel metálico aislado tipo sándwich (doble lámina de acero "
            "galvanizado prepintado cal. 26/26 con núcleo de espuma rígida de poliuretano de 1.5\" de espesor, tipo "
            "Multytecho o equivalente) sobre estructura metálica de cubierta (§7.3 y §8.1.4 memoria arquitectónica), "
            "incluye: caballetes, tapajuntas, tornillería autorroscante con rondana de neopreno, sellador de "
            "poliuretano, izaje, mano de obra, andamios, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "02 PRECIOS UNITARIOS.pdf LAM-01 (Básico 10503-061) actualizado a panel aislado tipo sándwich",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Basado en la matriz de cubierta metálica 02 PRECIOS UNITARIOS.pdf LAM-01 (CD = $809.59/m2 para "
            "lámina Zintro R-101 cal. 22), sustituyendo la lámina simple por panel metálico aislado tipo sándwich "
            "de 1.5\" ($865.00/m2) con los mismos accesorios de fijación, tapajuntas y cuadrilla 1H1A (CD = $1,176.38/m2)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "Walls",
                "filtro_tipo": "^Curtain Wall \\| Cubierta$",
                "campo_cantidad": "area_m2",
                "nota": "Área de cubierta inclinada modelada como Curtain Wall 'Cubierta' en Edificio de educacion (367.06 m2).",
            },
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Floors",
                "filtro_tipo": "Generic 150mm",
                "campo_cantidad": "area_m2",
                "nota": "Área de cubierta en Nivel - Azotea en TT_ED_EDUCACIÓN_CANCELERIA_2027 (1,113.73 m2).",
            },
        ],
        "apu": [
            {"codigo": "314-PAN-0150", "descripcion": "PANEL METALICO AISLADO TIPO SANDWICH CAL. 26/26 NUCLEO POLIURETANO 1.5\" (INC. 8% TRASLAPE/DESP.)", "unidad": "m2", "cantidad": 1.0800, "precio_unitario": 881.20, "fuente": "Insumos_APUCMX / Ref. 11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "314-CBT-0102", "descripcion": "BIRLO / PIJA AUTORROSCANTE P/TECHO C/RONDANA NEOPRENO (CIENTOS)", "unidad": "pza", "cantidad": 0.0400, "precio_unitario": 1034.00, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "314-LAM-0371", "descripcion": "TAPAJUNTAS MASTER FLASH No. 1 DE 1/4 A 2\"", "unidad": "pza", "cantidad": 0.2500, "precio_unitario": 301.11, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "321-PYE-0601", "descripcion": "MOLDURA / REMATE ESQUINERO GALVANIZADO PREPINTADO DE 2.44 M", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 33.19, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1H1A", "descripcion": "CUADRILLA No 9 (1 OFICIAL HERRERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.041667, "precio_unitario": 1637.61, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR, ANDAMIOS Y EQUIPO DE SEGURIDAD (10% M.O.)", "unidad": "%", "cantidad": 6.82, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-04-02-002",
        "capitulo": "04",
        "subcapitulo": "02",
        "concepto": (
            "Suministro y colocación de canalón pluvial de lámina de acero galvanizado prepintado cal. 22 de 60 cm "
            "de desarrollo para captación de agua pluvial en cubierta inclinada (§9.1 memoria arquitectónica), "
            "incluye: soportes de solera a cada 1.00 m, sellado de juntas con poliuretano, boquillas de bajada, "
            "mano de obra, andamios y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "11 RELACIÓN MATERIALES.pdf (314-LAM-0304 + 1H1A)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado con lámina Zintro cal. 22 (314-LAM-0304 $531.55/m2 × 0.65 m2/m desarrollo), soportes y "
            "sellador más cuadrilla 1H1A (rendimiento 18 m/jor); CD = $489.50/m."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [
            {
                "modelo": "TT-ED-EDU-ARQ-MOB",
                "categoria": "Gutters",
                "filtro_tipo": ".*",
                "campo_cantidad": "longitud_m",
                "nota": "Longitud de canalones pluviales en cubierta (no modelados en Revit; se cuantifica desde memoria en AG-3).",
            }
        ],
        "apu": [
            {"codigo": "314-LAM-0304", "descripcion": "LAMINA ZINTRO CAL. 22 (DESARROLLO 0.60 M + TRASLAPE)", "unidad": "m2", "cantidad": 0.6500, "precio_unitario": 531.55, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "321-PYE-0601", "descripcion": "SOPORTE Y FIJACION GALVANIZADA P/CANALON", "unidad": "pza", "cantidad": 1.3300, "precio_unitario": 33.19, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1H1A", "descripcion": "CUADRILLA No 9 (1 OFICIAL HERRERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.0555, "precio_unitario": 1637.61, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR, ANDAMIOS Y EQUIPO DE SEGURIDAD (10% M.O.)", "unidad": "%", "cantidad": 8.98, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 05 — ALBAÑILERÍA (D-019 y P-011: Muros desde Edificio de educacion y Cancelería)
    # =========================================================================
    {
        "clave": "ED-05-01-001",
        "capitulo": "05",
        "subcapitulo": "01",
        "concepto": (
            "Muro de mampostería de ladrillo/tabique de barro extruido aparente cara vista de 15 cm de espesor "
            "y celosía exterior de barro en fachadas y muros perimetrales (§7.3 y §8.1.2 memoria arquitectónica), "
            "asentado con mortero cemento-arena 1:4 con junta aparente boleada, incluye: suministro de materiales, "
            "acarreos, cortes, desperdicios, plomeo, andamios, limpieza, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 03 BÁSICOS.pdf (mortero 1:4 y cuadrilla 1A1P) / Validado con Xalapa",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con ladrillo/block de barro extruido aparente (25 pzas/m2 + 5% desperdicio), mortero "
            "cemento-arena 1:4 (0.025 m3/m2) y cuadrilla 1A1P (rendimiento 8.5 m2/jor por acabado aparente); "
            "mapeado a Walls de TT_ED_EDUCACIÓN_CANCELERIA_2027 (Ladrillo cara vista 15 CM) y Edificio de educacion "
            "(Celosia Exterior) conforme a D-019 y notas_doble_conteo_muros.md (P-011)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Walls",
                "filtro_tipo": "Ladrillo cara vista 15 CM",
                "campo_cantidad": "area_m2",
                "nota": "D-019: 87 muros de Ladrillo cara vista 15 CM (1,040.43 m2) en TT_ED_EDUCACIÓN_CANCELERIA_2027.",
            },
            {
                "modelo": "Edificio de educacion",
                "categoria": "Walls",
                "filtro_tipo": "Celosia Exterior",
                "campo_cantidad": "area_m2",
                "nota": "D-019 / P-011: 4 muros anfitriones Celosía Exterior (46.48 m2) en Edificio de educacion (sin tocar CurtainWallPanels).",
            },
        ],
        "apu": [
            {"codigo": "310-NOV-0150", "descripcion": "BLOCK DE BARRO EXTRUIDO APARENTE TIPO NOVACERAMIC 15x10x20 CM (25 PZAS/M2 + 5% DESP.)", "unidad": "pza", "cantidad": 26.2500, "precio_unitario": 14.80, "fuente": "Insumos_APUCMX / Mercado regional"},
            {"codigo": "10401-544", "descripcion": "MORTERO CEMENTO-ARENA PROPORCION 1:4 HECHO EN OBRA", "unidad": "m3", "cantidad": 0.0250, "precio_unitario": 2336.00, "fuente": "Xalapa Básico 10401-544"},
            {"codigo": "358-AGU-0101", "descripcion": "AGUA DE TOMA", "unidad": "m3", "cantidad": 0.0200, "precio_unitario": 35.52, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO)", "unidad": "jor", "cantidad": 0.117647, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (8% M.O.)", "unidad": "%", "cantidad": 15.00, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-05-01-002",
        "capitulo": "05",
        "subcapitulo": "01",
        "concepto": (
            "Muro de mampostería de block hueco de barro extruido NOVABLOCK (12) H y tabique/block ligero de "
            "10 a 14 cm de espesor en aulas, talleres, administración y servicios sanitarios (§8.1.2 memoria "
            "arquitectónica), asentado con mortero cemento-arena 1:5, incluye: materiales, acarreos, andamios, "
            "mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa matrices 310-TAB-0202 + 10401-544 + 03 BÁSICOS.pdf 1A1P",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con tabique/block de barro (310-TAB-0202 $4,201.30/millar), mortero 1:5 (10401-544) "
            "y cuadrilla 1A1P (rendimiento 11.0 m2/jor); CD = $424.91/m2. Mapeado exclusivamente a la categoría "
            "anfitriona Walls de Edificio de educacion (101 muros NOVABLOCK 12 H = 1,337.95 m2) y Cancelería "
            "(Muro 100 mm AAC COM = 7.22 m2) conforme a D-019 y P-011 (sin mapear CurtainWallPanels)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "Walls",
                "filtro_tipo": "NOVABLOCK",
                "campo_cantidad": "area_m2",
                "nota": "D-019 / P-011: 101 muros anfitriones NOVABLOCK (12) H (1,337.95 m2) en categoría Walls de Edificio de educacion (excluye los 9,931 CurtainWallPanels hijos).",
            },
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Walls",
                "filtro_tipo": "Muro 100 mm AAC COM",
                "campo_cantidad": "area_m2",
                "nota": "D-019: 4 muros divisorios interiores Muro 100 mm AAC COM (7.22 m2) en TT_ED_EDUCACIÓN_CANCELERIA_2027.",
            },
        ],
        "apu": [
            {"codigo": "310-TAB-0202", "descripcion": "TABIQUE ROJO RECOCIDO DE 6x13x26 CM (54 PZAS/M2 INC. DESPERDICIO, POR MILLAR)", "unidad": "pza", "cantidad": 0.0540, "precio_unitario": 4201.30, "fuente": "Xalapa 310-TAB-0202"},
            {"codigo": "10401-544", "descripcion": "MORTERO CEMENTO-ARENA PROPORCION 1:5 HECHO EN OBRA", "unidad": "m3", "cantidad": 0.0180, "precio_unitario": 2336.00, "fuente": "Xalapa Básico 10401-544"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO)", "unidad": "jor", "cantidad": 0.090909, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (7.7% M.O.)", "unidad": "%", "cantidad": 11.15, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-05-02-001",
        "capitulo": "05",
        "subcapitulo": "02",
        "concepto": (
            "Firme de concreto f'c=150 kg/cm2 de 10 cm de espesor promedio acabado común para recibir piso "
            "terminado en planta baja, reforzado con malla electrosoldada 6x6/10-10, incluye: preparación y "
            "compactación de base, cimbrado de fronteras, colado, nivelación, curado, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa OBR-EXT-11 (10606-005, CD=$484.40/m2) + 03 BÁSICOS.pdf",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado con concreto f'c=150 kg/cm2 hecho en obra (10401-292 $2,660.76/m3 × 0.103 m3/m2), "
            "malla 6x6/10-10 ($44.33/m2) y cuadrilla 1A5P (rendimiento 30 m2/jor); CD = $481.28/m2, "
            "validado contra Xalapa OBR-EXT-11 ($484.40/m2 CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Edificio de educacion",
                "categoria": "Floors",
                "filtro_tipo": "Firme estructural e=10 cm",
                "campo_cantidad": "area_m2",
                "nota": "Área de Firme estructural e=10 cm en Edificio de educacion (804.09 m2).",
            }
        ],
        "apu": [
            {"codigo": "10401-292", "descripcion": "CONCRETO F'c=150 KG/CM2 HECHO EN OBRA, T.M.A. 19 MM", "unidad": "m3", "cantidad": 0.1030, "precio_unitario": 2660.76, "fuente": "Xalapa Básico 10401-292"},
            {"codigo": "EST-6.3.12", "descripcion": "MALLA ELECTROSOLDADA 6x6/10-10 COLOCADA", "unidad": "m2", "cantidad": 1.0000, "precio_unitario": 44.33, "fuente": "Xalapa EST-6.3.12"},
            {"codigo": "1A5P", "descripcion": "CUADRILLA No 22 (1 OFICIAL ALBAÑIL + 5 PEONES + 0.6 CABO)", "unidad": "jor", "cantidad": 0.033333, "precio_unitario": 4582.12, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD", "unidad": "%", "cantidad": 10.15, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-05-02-002",
        "capitulo": "05",
        "subcapitulo": "02",
        "concepto": (
            "Aplanado acabado repellado y fino sobre muros interiores y áreas húmedas con mortero cemento-arena "
            "en proporción 1:4 de 2.0 cm de espesor promedio, incluye: preparación de la superficie, materiales, "
            "acarreos, andamios, limpieza, mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa ALB-6.4.3 (10702-001, CD=$269.23/m2) + 03 BÁSICOS.pdf",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz validada contra Xalapa ALB-6.4.3 (Costo Directo = $269.23/m2): mortero cemento-arena 1:4 "
            "(0.024 m3/m2) y cuadrilla 1A1P (rendimiento 8.0 m2/jor) más herramienta y andamios."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "10401-544", "descripcion": "MORTERO CEMENTO-ARENA PROPORCION 1:4 HECHO EN OBRA", "unidad": "m3", "cantidad": 0.0240, "precio_unitario": 2336.00, "fuente": "Xalapa Básico 10401-544"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO)", "unidad": "jor", "cantidad": 0.1250, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (7% M.O.)", "unidad": "%", "cantidad": 14.02, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 06 — ACABADOS (Modelo: Proyecto acabado-DAMIAN)
    # =========================================================================
    {
        "clave": "ED-06-01-001",
        "capitulo": "06",
        "subcapitulo": "01",
        "concepto": (
            "Acabado de piso de concreto pulido y endurecido superficialmente con endurecedor mineral y sellador "
            "acrílico transparente en aulas, talleres, biblioteca, centro digital y circulaciones interiores "
            "(§8.2.1 memoria arquitectónica), incluye: allanado mecánico con helicóptero, cortes de juntas de "
            "control con disco de diamante, sellado de juntas con poliuretano, mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + Xalapa OBR-EXT-06 / OBR-EXT-08",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para el acabado pulido espejo/endurecido sobre firme de concreto (§8.2.1 memoria): "
            "endurecedor superficial ($48.50/m2), sellador acrílico, corte y sellado de juntas ($38.20/m2) y "
            "cuadrilla 1A1P con allanadora mecánica (CD = $248.60/m2); validado contra Xalapa OBR-EXT-06 ($262.18/m2)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Floors",
                "filtro_tipo": "concreto pulido (autonivelante|densificado)",
                "campo_cantidad": "area_m2",
                "nota": "Pisos interiores de concreto pulido autonivelante y densificado en Proyecto acabado-DAMIAN (1,101.70 m2).",
            }
        ],
        "apu": [
            {"codigo": "308-END-0101", "descripcion": "ENDURECEDOR MINERAL Y SELLADOR ACRILICO P/PISO DE CONCRETO PULIDO (4 KG/M2)", "unidad": "kg", "cantidad": 4.0000, "precio_unitario": 18.50, "fuente": "Insumos_APUCMX"},
            {"codigo": "14202-012", "descripcion": "ASERRADO Y SELLADO DE JUNTAS DE CONTROL CON POLIURETANO (PROPORCION 0.50 M/M2)", "unidad": "m", "cantidad": 0.5000, "precio_unitario": 74.47, "fuente": "Xalapa OBR-EXT-08"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA No 5 (1 OFICIAL ALBAÑIL + 1 PEON + 0.1 CABO) PULIDO CON ALLANADORA", "unidad": "jor", "cantidad": 0.0800, "precio_unitario": 1593.21, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "ALLANADORA MECANICA Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 9.91, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-06-01-002",
        "capitulo": "06",
        "subcapitulo": "01",
        "concepto": (
            "Piso de loseta cerámica antiderrapante de 30 x 30 cm tráfico pesado en sanitarios, cocina, clínica "
            "y zonas húmedas (§8.2.1 memoria arquitectónica), asentado con adhesivo pega-azulejo y boquilla "
            "antifúngica con sellador, incluye: suministro de materiales, cortes, desperdicios, nivelación, "
            "mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX (loseta cerámica + adhesivo) + 02 PRECIOS UNITARIOS.pdf 1CO1A / Validado con Xalapa ACAB-6.13.10",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con loseta cerámica antiderrapante 30x30 cm ($215.00/m2 + 5% desperdicio), adhesivo "
            "mortero ($38.50/m2), boquilla y cuadrilla 1CO1A (1 Oficial Colocador + 1 Ayudante $1,738.00/jor, "
            "rendimiento 11 m2/jor = $158.00/m2); CD = $432.15/m2, validado contra Xalapa ACAB-6.13.10 ($423.49/m2)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Floors",
                "filtro_tipo": "piso aulas loseta ceramica",
                "campo_cantidad": "area_m2",
                "nota": "Piso de loseta cerámica e=0.02 en Proyecto acabado-DAMIAN (27.23 m2).",
            },
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Floors",
                "filtro_tipo": "Porcelanato Esmaltado",
                "campo_cantidad": "area_m2",
                "nota": "Piso de porcelanato esmaltado en TT_ED_EDUCACIÓN_CANCELERIA_2027 (596.50 m2).",
            },
        ],
        "apu": [
            {"codigo": "325-CER-0301", "descripcion": "LOSETA CERAMICA ANTIDERRAPANTE 30x30 CM TRAFICO PESADO (INC. 5% DESPERDICIO)", "unidad": "m2", "cantidad": 1.0500, "precio_unitario": 215.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "302-ADH-0101", "descripcion": "ADHESIVO EN POLVO PEGA-LOSETA Y BOQUILLA SELLADA (SACO 20 KG)", "unidad": "pza", "cantidad": 0.2500, "precio_unitario": 154.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.090909, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y CORTADORA (6.2% M.O.)", "unidad": "%", "cantidad": 9.90, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-06-01-003",
        "capitulo": "06",
        "subcapitulo": "01",
        "concepto": (
            "Piso de concreto lavado / escobillado antiderrapante en circulaciones exteriores cubiertas, terrazas "
            "y accesos del edificio de educación (§8.2.1 memoria arquitectónica), incluye: texturizado superficial, "
            "juntas de dilatación, curado, sellador hidrofugante, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa OBR-EXT-06 ($262.18/m2 CD)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU referenciado directamente a Xalapa OBR-EXT-06 (14202-009: Tendido y acabado rayado/escobillado "
            "de piso hidráulico, Costo Directo = $262.18/m2)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Floors",
                "filtro_tipo": "agregado expuesto",
                "campo_cantidad": "area_m2",
                "nota": "Piso de concreto con agregado expuesto en Proyecto acabado-DAMIAN (433.02 m2).",
            },
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Floors",
                "filtro_tipo": "Floor-Grnd-Susp",
                "campo_cantidad": "area_m2",
                "nota": "Pisos exteriores/accesos en TT_ED_EDUCACIÓN_CANCELERIA_2027 (233.31 m2).",
            },
        ],
        "apu": [
            {"codigo": "14202-009", "descripcion": "ACABADO ESCOBILLADO/LAVADO, JUNTAS Y CURADO EN PISO DE CONCRETO", "unidad": "m2", "cantidad": 1.0000, "precio_unitario": 262.18, "fuente": "Xalapa OBR-EXT-06"},
        ],
    },
    {
        "clave": "ED-06-02-001",
        "capitulo": "06",
        "subcapitulo": "02",
        "concepto": (
            "Pintura vinil-acrílica lavable en muros interiores y plafones marca Comex Pro-1000 o equivalente "
            "a dos manos en tonos neutros de alta reflectancia lumínica (§8.2.2 memoria arquitectónica), "
            "incluye: aplicación previa de sellador vinílico 5x1, preparación de la superficie, materiales, "
            "andamios, mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa ACAB-6.13.7 (CD=$122.97/m2) + 02 PRECIOS UNITARIOS.pdf 1P1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta validada contra Xalapa ACAB-6.13.7 (Costo Directo = $122.97/m2): pintura vinílica "
            "Pro-1000, sellador vinílico y cuadrilla 1P1A (1 Oficial Pintor + 1 Ayudante) con andamios."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Walls",
                "filtro_tipo": "muro general EDUC",
                "campo_cantidad": "area_m2",
                "nota": "Acabado de pintura en muros interiores 'muro general EDUC' del modelo Proyecto acabado-DAMIAN (1,601.49 m2).",
            }
        ],
        "apu": [
            {"codigo": "337-VIN-0101", "descripcion": "PINTURA VINIL-ACRILICA COMEX PRO-1000 Y SELLADOR 5x1 (0.28 LT/M2)", "unidad": "lt", "cantidad": 0.2800, "precio_unitario": 175.00, "fuente": "Xalapa ACAB-6.13.7 / Insumos_APUCMX"},
            {"codigo": "1P1A", "descripcion": "CUADRILLA No 8 (1 OFICIAL PINTOR + 1 AYUDANTE GENERAL + 0.1 CABO) REND 25 M2/JOR", "unidad": "jor", "cantidad": 0.0400, "precio_unitario": 1705.11, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR, BROCHAS Y ANDAMIOS (8.5% M.O.)", "unidad": "%", "cantidad": 5.77, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-06-02-002",
        "capitulo": "06",
        "subcapitulo": "02",
        "concepto": (
            "Recubrimiento de azulejo / loseta cerámica rectificada en muros de sanitarios, cocina y áreas "
            "húmedas (§8.2.2 memoria arquitectónica), asentado con adhesivo pega-azulejo y boquilla sellada "
            "antihongos, incluye: suministro de materiales, cortes, desperdicios, remates de aluminio/PVC en "
            "esquinas, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + 02 PRECIOS UNITARIOS.pdf 1CO1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con azulejo cerámico para muro húmedo ($225.00/m2 + 6% desperdicio), adhesivo "
            "pega-azulejo ($42.00/m2) y cuadrilla 1CO1A (rendimiento 9.5 m2/jor en muro); CD = $473.85/m2."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Walls",
                "filtro_tipo": "Muro Exterior - Interior Aparente",
                "campo_cantidad": "area_m2",
                "nota": "Recubrimiento en muros del modelo Proyecto acabado-DAMIAN (67.95 m2).",
            },
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Floors",
                "filtro_tipo": "PF_Plafon de loseta ceramica",
                "campo_cantidad": "area_m2",
                "nota": "Recubrimiento de loseta cerámica de 2 cm en Proyecto acabado-DAMIAN (27.23 m2).",
            },
        ],
        "apu": [
            {"codigo": "325-AZU-0201", "descripcion": "AZULEJO CERAMICO ESMALTADO P/MURO HUMEDO (INC. 6% DESPERDICIO)", "unidad": "m2", "cantidad": 1.0600, "precio_unitario": 225.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "302-ADH-0101", "descripcion": "ADHESIVO PEGA-AZULEJO Y BOQUILLA ANTIHONGOS (SACO 20 KG)", "unidad": "pza", "cantidad": 0.2800, "precio_unitario": 154.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.105263, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (5% M.O.)", "unidad": "%", "cantidad": 9.28, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-06-03-001",
        "capitulo": "06",
        "subcapitulo": "03",
        "concepto": (
            "Falso plafón modular registrable de 0.61 x 1.22 m con suspensión visible de 15/16\" marca Armstrong "
            "(línea acústica / metálica microperforada MetalWorks Mesh y Cortega conforme a §7.3 y §8.2.3 de la "
            "memoria arquitectónica) para control acústico y paso de instalaciones en aulas, biblioteca, centro "
            "digital y administración, incluye: suministro de paneles, tee principal y secundarias, ángulo "
            "perimetral, colganteo con alambre galvanizado cal. 14, nivelación láser, cortes, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa ACAB-6.13.2 (10803-015, CD=$634.42/m2) + 02 PRECIOS UNITARIOS.pdf 1CO1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz validada directamente con Xalapa ACAB-6.13.2 (Falso plafón modular 0.61x1.22 m Armstrong "
            "con suspensión visible 15/16\", Costo Directo = $634.42/m2)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Ceilings",
                "filtro_tipo": "Armstrong",
                "campo_cantidad": "area_m2",
                "nota": "Plafones registrables Armstrong en categoría Ceilings de Proyecto acabado-DAMIAN (1,125.08 m2).",
            },
            {
                "modelo": "Proyecto acabado-DAMIAN",
                "categoria": "Floors",
                "filtro_tipo": "PF_Plafon ACT - Armstrong",
                "campo_cantidad": "area_m2",
                "nota": "Plafones Armstrong MetalWorks Mesh modelados en categoría Floors de Proyecto acabado-DAMIAN (1,023.22 m2).",
            },
        ],
        "apu": [
            {"codigo": "321-PLA-0612", "descripcion": "SISTEMA DE FALSO PLAFON MODULAR ARMSTRONG 0.61x1.22 M C/SUSPENSION VISIBLE 15/16\" Y COLGANTEO", "unidad": "m2", "cantidad": 1.0500, "precio_unitario": 465.00, "fuente": "Xalapa ACAB-6.13.2 / Insumos_APUCMX"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL + 0.1 CABO) REND 12.5 M2/JOR", "unidad": "jor", "cantidad": 0.0800, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (5.1% M.O.)", "unidad": "%", "cantidad": 7.13, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-06-04-001",
        "capitulo": "06",
        "subcapitulo": "04",
        "concepto": (
            "Impermeabilización prefabricada en losas y zonas húmedas a base de primario asfáltico Hidroprimer "
            "y manto prefabricado APP/SBS de 4.0 mm de espesor con refuerzo de poliéster y acabado granular "
            "terracota, aplicada por termofusión, incluye: limpieza y preparación de superficie, sellado de "
            "chaflanes y puntos críticos, traslapes de 10 cm, elevaciones, mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa IMP-6.5.2 (10901-012, CD=$493.84/m2)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz validada directamente contra Xalapa IMP-6.5.2 (Impermeabilización con Hidroprimer y "
            "Festermip 4 mm acabado terracota, Costo Directo = $493.84/m2)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "308-IMP-0400", "descripcion": "MANTO IMPERMEABILIZANTE PREFABRICADO 4 MM POLIESTER + HIDROPRIMER (INC. 12% TRASLAPE)", "unidad": "m2", "cantidad": 1.1200, "precio_unitario": 335.00, "fuente": "Xalapa IMP-6.5.2 / Insumos_APUCMX"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL + 0.1 CABO) REND 15.5 M2/JOR", "unidad": "jor", "cantidad": 0.0645, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "GAS BUTANO, SOPLETE Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 6.54, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
]
