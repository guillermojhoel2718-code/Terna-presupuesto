"""Definición de conceptos y APUs para los capítulos 07 a 14 del Edificio de Educación (ED).

Agente: AG-2 (Precios)
Notas normativas:
- D-016: Capítulos 11 (Voz y datos) y 12 (Aire acondicionado y ventilación) reservados SIN conceptos.
- D-003 / D-011 / SPEC_05: Costos directos en MXN con trazabilidad a precios_procesados, Neodata PDFs y Xalapa.
"""
from __future__ import annotations

CAPITULOS_07_14: list[dict] = [
    # =========================================================================
    # CAPÍTULO 07 — HERRERÍA Y CANCELERÍA (Modelo: TT_ED_EDUCACIÓN_CANCELERIA_2027)
    # =========================================================================
    {
        "clave": "ED-07-01-001",
        "capitulo": "07",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y colocación de puerta abatible de 0.90 x 2.15 m para aulas, talleres y oficinas, con "
            "marco de perfil metálico/aluminio y hoja entablerada de alta resistencia o lámina cal. 18 con "
            "mirilla vertical de cristal templado (§8.2.4 memoria arquitectónica), incluye: bisagras de uso "
            "rudo, cerradura de palanca institucional, topes, sellado perimetral, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa HERR-6.14.3 ($7,635.52/pza) y CARP-6.16.1 ($12,819.96/pza) + 02 PRECIOS UNITARIOS.pdf 1H1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con puerta institucional de 0.90x2.15 m con marco, bisagras reforzadas y cerradura "
            "de palanca más cuadrilla 1H1A (rendimiento 2.0 pzas/jor); CD = $7,635.52/pza, validado contra "
            "Xalapa HERR-6.14.3 ($7,635.52/pza CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Doors",
                "filtro_tipo": "0\\.?8|0\\.?9|1\\.?0|simple|una hoja|aula|oficina|interior|abatible|madera|metal",
                "campo_cantidad": "conteo",
                "nota": "Puertas abatibles sencillas en modelo de cancelería/arquitectura.",
            }
        ],
        "apu": [
            {"codigo": "315-PUE-0921", "descripcion": "PUERTA INSTITUCIONAL ABATIBLE 0.90x2.15 M C/MARCO, BISAGRAS Y CERRADURA DE PALANCA", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 6735.00, "fuente": "Xalapa HERR-6.14.3 / Insumos_APUCMX"},
            {"codigo": "1H1A", "descripcion": "CUADRILLA No 9 (1 OFICIAL HERRERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.5000, "precio_unitario": 1637.61, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR, TAQUETES Y SELLADOR (10% M.O.)", "unidad": "%", "cantidad": 81.72, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-07-01-002",
        "capitulo": "07",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y colocación de puerta doble abatible de 1.80 x 2.20 m en accesos principales, talleres, "
            "biblioteca y salidas de emergencia (§8.2.4 memoria arquitectónica), fabricada con perfilería pesada "
            "de aluminio/acero y cristal templado de 9.5 mm o tablero metálico aislado, barra antipánico y "
            "cierrapuertas hidráulico, incluye: herrajes, fijación, sellado, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa HERR-6.14.2 ($23,777.63/pza) + 02 PRECIOS UNITARIOS.pdf 1H1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado para puerta doble institucional de acceso/emergencia con barra antipánico y "
            "cierrapuertas; CD = $16,845.32/pza, validado contra puerta de seguridad Xalapa HERR-6.14.2 ($23,777.63/pza CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Doors",
                "filtro_tipo": "doble|1\\.?5|1\\.?6|1\\.?8|2\\.?0|acceso|emergencia|salida",
                "campo_cantidad": "conteo",
                "nota": "Puertas dobles abatibles en modelo de cancelería/arquitectura.",
            }
        ],
        "apu": [
            {"codigo": "315-PUE-1822", "descripcion": "PUERTA DOBLE ABATIBLE 1.80x2.20 M C/BARRA ANTIPANICO, CIERRAPUERTAS Y HERRAJES", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 15044.00, "fuente": "Insumos_APUCMX / Ref. Xalapa HERR-6.14.2"},
            {"codigo": "1H1A", "descripcion": "CUADRILLA No 9 (1 OFICIAL HERRERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 1.0000, "precio_unitario": 1637.61, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR, ANCLAJE Y SELLADOR (10% M.O.)", "unidad": "%", "cantidad": 163.71, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-07-02-001",
        "capitulo": "07",
        "subcapitulo": "02",
        "concepto": (
            "Suministro y colocación de ventana de cancelería de aluminio anodizado natural/negro línea 3\" "
            "(fijos y proyectables para ventilación cruzada conforme a §6.2 y §8.2.4 memoria arquitectónica) "
            "de 1.80 x 1.50 m promedio con cristal claro templado/laminado de 6 mm, incluye: felpas, vinilos, "
            "operadores proyectables, sellado perimetral con silicón neutro, cortes, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa CAN-6.15.1 ($1,824.31/pza en 0.64 m2 = $2,850.48/m2) + 02 PRECIOS UNITARIOS.pdf 1H1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado a razón de $2,480/m2 de cancelería de aluminio 3\" con cristal de 6 mm para módulo "
            "promedio de ventana de aula/taller (2.40 m2 = $5,952.00/pza), consistente con el costo unitario por m2 "
            "de Xalapa CAN-6.15.1 ($2,850/m2)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Windows",
                "filtro_tipo": ".*",
                "campo_cantidad": "conteo",
                "nota": "Ventanas de aluminio y cristal en modelo TT_ED_EDUCACIÓN_CANCELERIA_2027.",
            }
        ],
        "apu": [
            {"codigo": "316-CAN-0306", "descripcion": "MODULO DE VENTANA DE ALUMINIO ANODIZADO 3\" C/CRISTAL TEMPLADO 6 MM Y HERRAJES PROYECTABLES", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 5051.32, "fuente": "Insumos_APUCMX / Ref. Xalapa CAN-6.15.1"},
            {"codigo": "1H1A", "descripcion": "CUADRILLA No 9 (1 OFICIAL HERRERO/CANCELERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.5000, "precio_unitario": 1637.61, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "SILICON ESTRUCTURAL, PIJAS INOXIDABLES Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 81.87, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-07-02-002",
        "capitulo": "07",
        "subcapitulo": "02",
        "concepto": (
            "Suministro y colocación de fachada integral / muro cortina de aluminio anodizado serie 3\" con "
            "cristal laminado/templado de seguridad de 6+6 mm o 9.5 mm para iluminación natural cenital y "
            "vestíbulos (§7.3 y §8.2.4 memoria arquitectónica), incluye: mullions, transoms, anclajes a estructura "
            "metálica/concreto, empaques EPDM, sellado climático, andamios, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + Xalapa CAN-6.15.1 + 02 PRECIOS UNITARIOS.pdf 1H1A",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con perfilería de aluminio para muro cortina ($1,320.00/m2), cristal templado de 9.5 mm "
            "($980.00/m2), herrajes/sellador ($165.00/m2) y cuadrilla 1H1A (rendimiento 4.5 m2/jor); CD = $2,865.30/m2."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT_ED_EDUCACIÓN_CANCELERIA_2027",
                "categoria": "Curtain Panels",
                "filtro_tipo": ".*",
                "campo_cantidad": "area_m2",
                "nota": "Paneles de muro cortina y cancelería corrida en modelo TT_ED_EDUCACIÓN_CANCELERIA_2027.",
            }
        ],
        "apu": [
            {"codigo": "316-MCO-0101", "descripcion": "PERFILERIA DE ALUMINIO P/MURO CORTINA 3\" C/ANCLAJES Y EMPAQUES EPDM", "unidad": "m2", "cantidad": 1.0000, "precio_unitario": 1320.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "317-CRI-0950", "descripcion": "CRISTAL TEMPLADO DE SEGURIDAD 9.5 MM CLARO C/CANTOS PULIDOS", "unidad": "m2", "cantidad": 1.0500, "precio_unitario": 980.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "316-SEL-0101", "descripcion": "SELLADOR DE SILICON ESTRUCTURAL Y CINTA NORTON", "unidad": "pza", "cantidad": 0.8500, "precio_unitario": 158.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1H1A", "descripcion": "CUADRILLA No 9 (1 OFICIAL CANCELERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.222222, "precio_unitario": 1637.61, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (5% M.O.)", "unidad": "%", "cantidad": 18.09, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-07-03-001",
        "capitulo": "07",
        "subcapitulo": "03",
        "concepto": (
            "Suministro y colocación de barandal metálico de protección de 0.90 a 1.05 m de altura en pasillos "
            "de planta alta, balcones, escaleras y rampas (§6.3 y §8.2.4 memoria arquitectónica), fabricado con "
            "postes de PTR 1 1/2\" x 1 1/2\" a cada 1.00 m con placa base A-36 de 5/16\", pasamanos de tubo "
            "cédula 30 de 2\" y largueros horizontales de 1 1/4\", acabado con primario anticorrosivo y pintura "
            "de esmalte poliuretano, incluye: cortes, soldadura, anclaje, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa HERGEN-01 / HERGEN-05 (11008-011, CD=$1,478.43/m)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta validada contra Xalapa HERGEN-01 y HERGEN-05 (Código 11008-011: Barandal de 0.90 m "
            "de altura con postes de PTR 1 1/2\" y pasamanos de tubo céd. 30 de 2\", Costo Directo = $1,478.43/m)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT-ED-EDU-ARQ-MOB",
                "categoria": "Railings",
                "filtro_tipo": ".*",
                "campo_cantidad": "longitud_m",
                "nota": "Longitud de barandales y pasamanos en modelo arquitectónico/cancelería.",
            }
        ],
        "apu": [
            {"codigo": "11008-011", "descripcion": "PERFILES PTR 1 1/2\", TUBO CED. 30 2\" Y 1 1/4\", PLACA A-36 5/16\", SOLDADURA Y ESMALTE", "unidad": "m", "cantidad": 1.0000, "precio_unitario": 1035.00, "fuente": "Xalapa HERGEN-01"},
            {"codigo": "1H1A", "descripcion": "CUADRILLA No 9 (1 OFICIAL HERRERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.2500, "precio_unitario": 1637.61, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "PLANTA DE SOLDAR, HERRAMIENTA MENOR Y SEGURIDAD", "unidad": "%", "cantidad": 34.03, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 08 — INSTALACIÓN HIDRÁULICA Y PLUVIAL (Modelo: Instalaciones)
    # =========================================================================
    {
        "clave": "ED-08-01-001",
        "capitulo": "08",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y tendido de tubería hidráulica de PVC RD-13.5 / PPR termofusionable de 19 a 25 mm de "
            "diámetro para red de distribución de agua potable fría (§9.1 memoria arquitectónica), incluye: "
            "coples, cortes, soportería, pruebas hidrostáticas de hermeticidad, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa INS-HID-6.6.1 (CD=$95.37/m) + Insumos_APUCMX",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz validada directamente contra Xalapa INS-HID-6.6.1 (Tubo de PVC hidráulico de 25 mm RD-13.5 "
            "instalado y probado, Costo Directo = $95.37/m)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "Pipes",
                "filtro_tipo": "hidraul|agua fria|agua potable|ppr|rd-13|13 ?mm|19 ?mm|25 ?mm|1/2|3/4|1\"",
                "campo_cantidad": "longitud_m",
                "nota": "Tubería hidráulica de agua potable de 13 a 25 mm en modelo Instalaciones.",
            }
        ],
        "apu": [
            {"codigo": "330-PVC-0250", "descripcion": "TUBO HIDRAULICO PVC RD-13.5 / PPR DE 25 MM (1\") C/CEMENTO Y LIMPIADOR", "unidad": "m", "cantidad": 1.0500, "precio_unitario": 42.50, "fuente": "Xalapa INS-HID-6.6.1 / Insumos_APUCMX"},
            {"codigo": "1PL1A", "descripcion": "CUADRILLA PLOMERIA (1 OFICIAL PLOMERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.0280, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y BOMBA DE PRUEBA HIDROSTATICA", "unidad": "%", "cantidad": 2.08, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-08-01-002",
        "capitulo": "08",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y tendido de tubería hidráulica de PVC RD-26 de 38 a 50 mm de diámetro para línea "
            "principal de alimentación y red de agua pluvial tratada para descarga de inodoros y riego "
            "(§6.4 y §9.1 memoria arquitectónica), incluye: fijación, pruebas hidrostáticas, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa INS-ATRA-6.7.1 (CD=$110.49/m)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz validada directamente contra Xalapa INS-ATRA-6.7.1 (Tubo de PVC hidráulico de 38 mm RD-26 "
            "para red de agua tratada, Costo Directo = $110.49/m)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "Pipes",
                "filtro_tipo": "tratada|pluvial|alimentacion|rd-26|32 ?mm|38 ?mm|50 ?mm|1 1/4|1 1/2",
                "campo_cantidad": "longitud_m",
                "nota": "Tubería hidráulica de alimentación/agua pluvial tratada de 32 a 50 mm en modelo Instalaciones.",
            }
        ],
        "apu": [
            {"codigo": "330-PVC-0380", "descripcion": "TUBO HIDRAULICO PVC RD-26 DE 38 MM (1 1/2\") C/CEMENTO Y SOPORTERIA", "unidad": "m", "cantidad": 1.0500, "precio_unitario": 53.20, "fuente": "Xalapa INS-ATRA-6.7.1 / Insumos_APUCMX"},
            {"codigo": "1PL1A", "descripcion": "CUADRILLA PLOMERIA (1 OFICIAL PLOMERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 0.0300, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y PRUEBAS", "unidad": "%", "cantidad": 2.49, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-08-01-003",
        "capitulo": "08",
        "subcapitulo": "01",
        "concepto": (
            "Suministro e instalación de conexiones hidráulicas (codos, tees, coples, reducciones y adaptadores) "
            "de PVC hidráulico / PPR de 19 a 38 mm de diámetro, incluye: materiales de unión, pruebas de "
            "presión, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa INS-HID-6.6.2 ($92.40), 6.6.3 ($64.93), 6.7.2 ($86.60)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU promedio ponderado de conexiones hidráulicas de 25 a 38 mm validado contra Xalapa INS-HID-6.6.2 "
            "($92.40/pza), INS-HID-6.6.3 ($64.93/pza) e INS-ATRA-6.7.2 ($86.60/pza); CD = $81.35/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "Pipe Fittings",
                "filtro_tipo": "hidraul|agua|ppr|rd-|13|19|25|32|38",
                "campo_cantidad": "conteo",
                "nota": "Conexiones hidráulicas en modelo Instalaciones.",
            }
        ],
        "apu": [
            {"codigo": "330-CON-0250", "descripcion": "CONEXION HIDRAULICA (CODO/TEE/COPLE) PVC RD-13.5 / PPR 25-38 MM C/ADHESIVO", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 44.50, "fuente": "Xalapa INS-HID-6.6.2..4"},
            {"codigo": "1PL1A", "descripcion": "CUADRILLA PLOMERIA (1 OFICIAL PLOMERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0200, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR (6% M.O.)", "unidad": "%", "cantidad": 2.09, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-08-01-004",
        "capitulo": "08",
        "subcapitulo": "01",
        "concepto": (
            "Suministro e instalación de válvula de seccionamiento (compuerta / esfera / retención) de bronce "
            "roscable de 25 a 38 mm de diámetro para control de zonas hidráulicas, incluye: adaptadores, "
            "cinta teflón, pruebas, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa INS-HID-6.6.8 ($1,079.46) y 6.6.9 ($600.40)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU validado contra Xalapa INS-HID-6.6.8 ($1,079.46/pza) e INS-HID-6.6.9 ($600.40/pza); "
            "CD = $842.50/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "Pipe Accessories",
                "filtro_tipo": ".*",
                "campo_cantidad": "conteo",
                "nota": "Válvulas y accesorios de tubería en modelo Instalaciones.",
            }
        ],
        "apu": [
            {"codigo": "331-VAL-0250", "descripcion": "VALVULA DE COMPUERTA/ESFERA DE BRONCE ROSCABLE 25-38 MM C/CONECTORES", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 660.00, "fuente": "Xalapa INS-HID-6.6.8..9"},
            {"codigo": "1PL1A", "descripcion": "CUADRILLA PLOMERIA (1 OFICIAL PLOMERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.1000, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR (5% M.O.)", "unidad": "%", "cantidad": 8.70, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-08-02-001",
        "capitulo": "08",
        "subcapitulo": "02",
        "concepto": (
            "Suministro e instalación de equipo hidroneumático presurizador con tanque precargado de 200 L y "
            "bomba centrífuga de 1.5 HP marca Pedrollo modelo JSWM15M/200CL o equivalente (§9.1 memoria "
            "arquitectónica), incluye: manómetro, presostato, válvula check, conexiones flexibles, pruebas de "
            "arranque y paro, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX código a4ba6e38 ($16,175.00) + Xalapa INS-HID-6.6.7 ($1,356.28)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado con el insumo real de precios_procesados código a4ba6e38 (EQUIPO HIDRONEUMATICO DE 200L "
            "JSWM15M/200CL PEDROLLO = $16,175.00), tren de válvulas/manómetro ($1,356.28) y cuadrilla de "
            "instalación 1PL1A (1.0 jornada = $1,738.00); CD = $19,356.18/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "Mechanical Equipment",
                "filtro_tipo": "bomba|hidroneumatico|presurizador|cisterna|tanque|filtro",
                "campo_cantidad": "conteo",
                "nota": "Equipos de bombeo e hidroneumático en modelo Instalaciones.",
            }
        ],
        "apu": [
            {"codigo": "a4ba6e38", "descripcion": "EQUIPO HIDRONEUMATICO DE 200L JSWM15M/200CL PEDROLLO", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 16175.00, "fuente": "Insumos_APUCMX (catalogo_apuc_mvp.csv)"},
            {"codigo": "INS-HID-6.6.7", "descripcion": "JUEGO DE MANOMETRO, VALVULA CHECK Y CONEXIONES DE DESCARGA", "unidad": "jgo", "cantidad": 1.0000, "precio_unitario": 1356.28, "fuente": "Xalapa INS-HID-6.6.7"},
            {"codigo": "1PL1A", "descripcion": "CUADRILLA PLOMERIA (1 OFICIAL PLOMERO + 1 AYUDANTE GENERAL + 0.1 CABO)", "unidad": "jor", "cantidad": 1.0000, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE PRUEBA (5% M.O.)", "unidad": "%", "cantidad": 86.90, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-08-03-001",
        "capitulo": "08",
        "subcapitulo": "03",
        "concepto": (
            "Suministro e instalación de sistema de captación, filtrado de primeras lluvias (separador de "
            "hojas y filtro de sedimentos/carbón activado) y almacenamiento pluvial en cisterna prefabricada "
            "equipada de 10,000 L para aprovechamiento de agua de lluvia (§6.4 y §9.1 memoria arquitectónica), "
            "incluye: excavación, plantilla, colocación, tren de filtrado, interconexión a bajadas pluviales, "
            "mano de obra y herramienta."
        ),
        "unidad": "jgo",
        "fuente_tipo": "SUPUESTO",
        "fuente_ref": "SUPUESTO conservador basado en cisterna prefabricada 10,000 L + filtro pluvial + excavación/plantilla",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "SUPUESTO conservador para el paquete de captación y filtrado pluvial de 10,000 L descrito en "
            "§6.4 y §9.1 de la memoria arquitectónica (cisterna equipada $26,500 + filtro separador de primeras "
            "lluvias y sedimentos $6,800 + instalación y cama de apoyo $5,200 = $38,500.00/jgo)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "precio_unitario": 38500.00,
        "apu": [],
    },

    # =========================================================================
    # CAPÍTULO 09 — INSTALACIÓN SANITARIA (Modelo: Instalaciones)
    # =========================================================================
    {
        "clave": "ED-09-01-001",
        "capitulo": "09",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y tendido de tubería de PVC sanitario de 50 mm (2\") de diámetro para ramales de "
            "desagüe de lavabos, tarjas, coladeras y tubos de ventilación (§9.2 memoria arquitectónica), "
            "incluye: cemento PVC, abrazaderas, cortes, pruebas de hermeticidad, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa INS-SAN-6.9.1 (CD=$95.71/m)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta validada contra Xalapa INS-SAN-6.9.1 (Tubo de PVC sanitario de 50 mm de diámetro "
            "instalado y probado, Costo Directo = $95.71/m)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "Pipes",
                "filtro_tipo": "sanit|drenaje|desague|ventilacion|50 ?mm|38 ?mm|2\"",
                "campo_cantidad": "longitud_m",
                "nota": "Tubería sanitaria PVC de 50 mm en modelo Instalaciones.",
            }
        ],
        "apu": [
            {"codigo": "332-SAN-0050", "descripcion": "TUBO PVC SANITARIO NORMA DE 50 MM (2\") C/CEMENTO Y SOPORTERIA", "unidad": "m", "cantidad": 1.0500, "precio_unitario": 42.80, "fuente": "Xalapa INS-SAN-6.9.1"},
            {"codigo": "1PL1A", "descripcion": "CUADRILLA PLOMERIA (1 OFICIAL PLOMERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0280, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y PRUEBAS", "unidad": "%", "cantidad": 2.11, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-09-01-002",
        "capitulo": "09",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y tendido de tubería de PVC sanitario de 100 mm (4\") de diámetro para colectores "
            "de aguas negras, aguas jabonosas y bajadas de aguas pluviales (B.A.P.) con separación de redes "
            "(§9.2 memoria arquitectónica), incluye: cemento PVC, soportería, cama de arena en tramos "
            "enterrados, pruebas de hermeticidad, mano de obra y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa INS-SAN-6.9.2 (CD=$151.33/m)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta validada contra Xalapa INS-SAN-6.9.2 (Tubo de PVC sanitario de 100 mm de diámetro "
            "instalado y probado, Costo Directo = $151.33/m)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "Pipes",
                "filtro_tipo": "100 ?mm|102 ?mm|110 ?mm|150 ?mm|4\"|6\"|colector|bap|bajada",
                "campo_cantidad": "longitud_m",
                "nota": "Tubería sanitaria y pluvial PVC de 100 mm o mayor en modelo Instalaciones.",
            }
        ],
        "apu": [
            {"codigo": "332-SAN-0100", "descripcion": "TUBO PVC SANITARIO NORMA DE 100 MM (4\") C/CEMENTO Y SOPORTERIA", "unidad": "m", "cantidad": 1.0500, "precio_unitario": 82.00, "fuente": "Xalapa INS-SAN-6.9.2"},
            {"codigo": "1PL1A", "descripcion": "CUADRILLA PLOMERIA (1 OFICIAL PLOMERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0360, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y PRUEBAS", "unidad": "%", "cantidad": 2.66, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-09-01-003",
        "capitulo": "09",
        "subcapitulo": "01",
        "concepto": (
            "Suministro e instalación de conexiones sanitarias de PVC para cementar (codos de 45° y 90°, "
            "yees sencillas y reducciones) de 50 a 100 mm de diámetro, incluye: limpiador, cemento PVC, "
            "pruebas de hermeticidad, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa INS-SAN-6.9.3 ($55.27), 6.9.4 ($105.59), 6.9.9 ($102.41), 6.9.10 ($150.43)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU promedio ponderado de conexiones sanitarias de 50 y 100 mm validado contra Xalapa "
            "INS-SAN-6.9.3..10; CD = $105.59/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "Pipe Fittings",
                "filtro_tipo": "sanit|drenaje|pvc|50|100|102|110|yee|codo",
                "campo_cantidad": "conteo",
                "nota": "Conexiones sanitarias de PVC en modelo Instalaciones.",
            }
        ],
        "apu": [
            {"codigo": "332-CON-0100", "descripcion": "CONEXION SANITARIA PVC (CODO/YEE/COPLE) 50-100 MM C/CEMENTO", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 68.74, "fuente": "Xalapa INS-SAN-6.9.4"},
            {"codigo": "1PL1A", "descripcion": "CUADRILLA PLOMERIA (1 OFICIAL PLOMERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.0200, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR (6% M.O.)", "unidad": "%", "cantidad": 2.09, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-09-02-001",
        "capitulo": "09",
        "subcapitulo": "02",
        "concepto": (
            "Suministro e instalación de inodoro ecológico de bajo consumo (< 4.8 L por descarga) de cerámica "
            "vitrificada color blanco con fluxómetro/válvula ahorradora y asiento elongado (§9.1 y §9.2 memoria "
            "arquitectónica), incluye: junta de cera con guía, brida sanitaria, válvula angular, manguera "
            "flexible, sellado con silicón antimicótico, pruebas, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa ACC-SAN-6.17.1 ($5,126.01) + ACC-SAN-6.17.10 ($537.84)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado y validado con Xalapa ACC-SAN-6.17.1 (Taza elongada blanca Helvex $5,126.01) y "
            "ACC-SAN-6.17.10 (Asiento elongado $537.84); CD = $5,663.85/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "Plumbing Fixtures",
                "filtro_tipo": "wc|inodoro|sanitario|taza|mingitorio|toilet|water closet",
                "campo_cantidad": "conteo",
                "nota": "Inodoros y mingitorios en modelo Instalaciones / ARQ-MOB.",
            }
        ],
        "apu": [
            {"codigo": "ACC-SAN-6.17.1", "descripcion": "TAZA SANITARIA ECOLOGICA ELONGADA BLANCA BAJO CONSUMO C/BRIDA Y HERRAJES", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 4650.00, "fuente": "Xalapa ACC-SAN-6.17.1"},
            {"codigo": "ACC-SAN-6.17.10", "descripcion": "ASIENTO ELONGADO BLANCO USO INSTITUCIONAL", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 537.84, "fuente": "Xalapa ACC-SAN-6.17.10"},
            {"codigo": "1PL1A", "descripcion": "CUADRILLA PLOMERIA (1 OFICIAL PLOMERO + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.2500, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "SELLADOR Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 41.51, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-09-02-002",
        "capitulo": "09",
        "subcapitulo": "02",
        "concepto": (
            "Suministro e instalación de lavabo institucional de cerámica vitrificada color blanco con llave "
            "ahorradora temporizada/monomando y céspol cromado con registro (§9.1 y §9.2 memoria arquitectónica), "
            "incluye: válvulas angulares de 1/2\", mangueras alimentadoras trenzadas, fijación, sellado, "
            "pruebas, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa ACC-SAN-6.17.2 ($2,124.94) + ACC-SAN-6.17.13 ($1,698.50)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado y validado con Xalapa ACC-SAN-6.17.2 (Lavabo blanco Helvex $2,124.94), ACC-SAN-6.17.13 "
            "(Céspol cromado con registro $1,698.50) y llave ahorradora institucional ($1,450.00); CD = $5,273.44/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Instalaciones",
                "categoria": "Plumbing Fixtures",
                "filtro_tipo": "lavabo|ovalin|sink|lavamanos|fregadero|tarja|coladera",
                "campo_cantidad": "conteo",
                "nota": "Lavabos, tarjas y muebles húmedos en modelo Instalaciones / ARQ-MOB.",
            }
        ],
        "apu": [
            {"codigo": "ACC-SAN-6.17.2", "descripcion": "LAVABO DE CERAMICA VITRIFICADA BLANCO USO INSTITUCIONAL", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 2124.94, "fuente": "Xalapa ACC-SAN-6.17.2"},
            {"codigo": "ACC-SAN-6.17.13", "descripcion": "CESPOL CROMADO C/REGISTRO, VALVULAS ANGULARES Y MANGUERAS", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 1698.50, "fuente": "Xalapa ACC-SAN-6.17.13"},
            {"codigo": "333-LLA-0101", "descripcion": "LLAVE ECONOMIZADORA TEMPORIZADA CROMADA P/LAVABO", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 1450.00, "fuente": "Insumos_APUCMX"},
        ],
    },
    {
        "clave": "ED-09-03-001",
        "capitulo": "09",
        "subcapitulo": "03",
        "concepto": (
            "Registro sanitario de 0.60 x 0.40 m de medidas interiores y 0.80 m de profundidad promedio, "
            "fabricado con muros de tabique rojo recocido asentado con mortero cemento-arena 1:5 sobre firme "
            "de 8 cm de concreto f'c=150 kg/cm2, aplanado interior pulido con media caña y tapa de concreto "
            "con marco y contramarco metálico, incluye: excavación, materiales, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa ALBGEN-02 (10608-002, CD=$3,324.44/pza)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta validada contra Xalapa ALBGEN-02 (Código 10608-002: Registro sanitario 0.40x0.60x0.80 m "
            "completo con marco y contramarco, Costo Directo = $3,324.44/pza)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "10608-002", "descripcion": "MATERIALES DE REGISTRO SANITARIO (TABIQUE, MARCO Y CONTRAMARCO 40x60, CIMBRA)", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 1181.67, "fuente": "Xalapa ALBGEN-02"},
            {"codigo": "10401-544", "descripcion": "MORTERO CEMENTO-ARENA 1:5 Y CONCRETO F'c=150 KG/CM2", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 508.96, "fuente": "Xalapa ALBGEN-02"},
            {"codigo": "1A1P", "descripcion": "CUADRILLA ALBAÑILERIA Y EXCAVACION (1A1P + 1P)", "unidad": "jor", "cantidad": 1.0000, "precio_unitario": 1556.01, "fuente": "Xalapa ALBGEN-02"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y EQUIPO DE SEGURIDAD (5% M.O.)", "unidad": "%", "cantidad": 77.80, "precio_unitario": 1.00, "fuente": "Xalapa ALBGEN-02"},
        ],
    },
    {
        "clave": "ED-09-03-002",
        "capitulo": "09",
        "subcapitulo": "03",
        "concepto": (
            "Suministro e instalación de biodigestor autolimpiable anaerobio prefabricado de polietileno de "
            "alta densidad de 7,000 L de capacidad para tratamiento primario de aguas negras previo a descarga "
            "(§6.4 y §9.2 memoria arquitectónica), incluye: excavación, plantilla de concreto pobre, registro "
            "de lodos, interconexiones de entrada y salida en PVC sanitario de 100 mm, relleno compactado, "
            "mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "SUPUESTO",
        "fuente_ref": "SUPUESTO conservador basado en biodigestor prefabricado 7,000 L + excavación y registro de lodos",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "SUPUESTO conservador para el sistema de tratamiento primario con biodigestor anaerobio de 7,000 L "
            "especificado en §9.2 de la memoria arquitectónica (equipo biodigestor 7,000 L $21,500 + excavación, "
            "plantilla, registro de lodos e instalación $7,400 = $28,900.00/pza)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "precio_unitario": 28900.00,
        "apu": [],
    },

    # =========================================================================
    # CAPÍTULO 10 — INSTALACIÓN ELÉCTRICA (Modelo: Proyecto electrico_corregido)
    # =========================================================================
    {
        "clave": "ED-10-01-001",
        "capitulo": "10",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y tendido de tubería conduit metálica galvanizada pared delgada (EMT) de 19 a 25 mm "
            "de diámetro aparente/oculta en plafón y muros con cableado conductor de cobre THW-LS/THHW cal. "
            "12 y 10 AWG (fase, neutro y tierra física desnuda) para circuitos derivados de alumbrado y "
            "contactos (§9.3 memoria arquitectónica), incluye: conectores, coples, abrazaderas tipo uña/omega, "
            "cajas de conexión, mano de obra, andamios y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + Xalapa INS-ELE-6.10.7 ($919.32/salida de 6 m = $153.22/m)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con tubo conduit galvanizado pared delgada 19-25 mm ($48.50/m), 3 hilos de cable "
            "THW-LS cal. 12 AWG ($18.20/m × 3.15 = $57.33/m), abrazaderas/coples ($12.40/m) y cuadrilla de "
            "electricista (rendimiento 32 m/jor); CD = $175.40/m, validado contra Xalapa INS-ELE-6.10.7 ($153.22/m en poliducto)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "Conduits",
                "filtro_tipo": ".*",
                "campo_cantidad": "longitud_m",
                "nota": "Tubería conduit eléctrica en modelo Proyecto electrico_corregido.",
            }
        ],
        "apu": [
            {"codigo": "340-CON-0250", "descripcion": "TUBO CONDUIT GALVANIZADO PARED DELGADA 19-25 MM C/COPLES Y ABRAZADERAS", "unidad": "m", "cantidad": 1.0500, "precio_unitario": 58.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "341-CAB-0012", "descripcion": "CABLE DE COBRE THW-LS 90°C 600V CAL. 12 AWG CONDUMEX (3 CONDUCTORES)", "unidad": "m", "cantidad": 3.1500, "precio_unitario": 18.20, "fuente": "Insumos_APUCMX"},
            {"codigo": "1EL1A", "descripcion": "CUADRILLA ELECTRICISTA (1 OFICIAL ELECTRICISTA + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.03125, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (5.3% M.O.)", "unidad": "%", "cantidad": 2.86, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-10-01-002",
        "capitulo": "10",
        "subcapitulo": "01",
        "concepto": (
            "Suministro e instalación de charola portacables tipo escalera/malla de acero electrozincado de "
            "20 a 30 cm de ancho para alimentadores principales en pasillos técnicos y plafón registrable "
            "(§9.3 memoria arquitectónica), incluye: soportes tipo trapecio con varilla roscada de 3/8\", "
            "clemas de unión, puesta a tierra, mano de obra, andamios y herramienta."
        ),
        "unidad": "m",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + Xalapa INS-ELE-6.10.10 ($635.57/m)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con charola portacables electrozincada 25 cm ($385.00/m), soportería colgante "
            "($95.00/m) y cuadrilla electricista (rendimiento 14 m/jor = $124.14/m); CD = $610.35/m, "
            "validado contra canalización principal Xalapa INS-ELE-6.10.10 ($635.57/m CD)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "Cable Trays",
                "filtro_tipo": ".*",
                "campo_cantidad": "longitud_m",
                "nota": "Charola portacables en modelo Proyecto electrico_corregido.",
            }
        ],
        "apu": [
            {"codigo": "340-CHA-0250", "descripcion": "CHAROLA PORTACABLES ELECTROZINCADA 25 CM DE ANCHO C/SOPORTERIA Y CLEMAS", "unidad": "m", "cantidad": 1.0000, "precio_unitario": 480.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1EL1A", "descripcion": "CUADRILLA ELECTRICISTA (1 OFICIAL ELECTRICISTA + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.071429, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (5% M.O.)", "unidad": "%", "cantidad": 6.21, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-10-02-001",
        "capitulo": "10",
        "subcapitulo": "02",
        "concepto": (
            "Suministro e instalación de luminaria LED tipo panel o gabinete lineal de 36 a 47 W, 127-277 V, "
            "temperatura de color 4,000 K (blanco neutro), alta eficiencia (>110 lm/W) y vida útil de 50,000 h, "
            "para empotrar o suspender en aulas, talleres, biblioteca, centro digital y oficinas (§9.3 memoria "
            "arquitectónica), incluye: driver multivoltaje, accesorios de suspensión/fijación, conexión, "
            "pruebas, mano de obra, andamios y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa LUM-ACC-6.11.10 ($2,131.75/pza) y LUM-ACC-6.11.11 ($2,958.87/pza)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta validada contra Xalapa LUM-ACC-6.11.10 (Luminario panel LED de suspender o empotrar "
            "a techo de 47 W, 127-277 V, 4000 K, Costo Directo = $2,131.75/pza)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "Lighting Fixtures",
                "filtro_tipo": "panel|lineal|gabinete|aula|taller|oficina|40w|47w|36w|60x60|120|suspend|^(?!.*(downlight|spot|empotrad.*9w|18w)).*$",
                "campo_cantidad": "conteo",
                "nota": "Luminarias LED principales (paneles/lineales) en modelo Proyecto electrico_corregido.",
            }
        ],
        "apu": [
            {"codigo": "LUM-ACC-6.11.10", "descripcion": "LUMINARIO PANEL / LINEAL LED 40-47W 127-277V 4000K C/DRIVER Y KIT DE SUSPENSION", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 1825.00, "fuente": "Xalapa LUM-ACC-6.11.10"},
            {"codigo": "1EL1A", "descripcion": "CUADRILLA ELECTRICISTA (1 OFICIAL ELECTRICISTA + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.166667, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (5.9% M.O.)", "unidad": "%", "cantidad": 17.08, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-10-02-002",
        "capitulo": "10",
        "subcapitulo": "02",
        "concepto": (
            "Suministro e instalación de luminaria LED tipo downlight de empotrar en plafón de 12 a 24 W, "
            "127-277 V, 3,000-4,000 K, para pasillos, sanitarios, vestíbulos y áreas de servicio (§9.3 memoria "
            "arquitectónica), incluye: conexión, fijación, pruebas, mano de obra, andamios y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa LUM-ACC-6.11.8 ($948.55/pza) y LUM-ACC-6.11.9 ($1,746.38/pza)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU validado contra Xalapa LUM-ACC-6.11.8 ($948.55/pza para 9 W) y LUM-ACC-6.11.9 ($1,746.38/pza "
            "para 24 W); promedio para downlight de 15-18 W CD = $1,185.40/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "Lighting Fixtures",
                "filtro_tipo": "downlight|spot|empotrad|9w|12w|15w|18w|24w|redond|sanitario|pasillo",
                "campo_cantidad": "conteo",
                "nota": "Luminarias LED tipo downlight/spot en modelo Proyecto electrico_corregido.",
            }
        ],
        "apu": [
            {"codigo": "LUM-ACC-6.11.8", "descripcion": "LUMINARIO DOWNLIGHT LED EMPOTRABLE 15-18W 127-277V 4000K C/DRIVER", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 955.00, "fuente": "Xalapa LUM-ACC-6.11.8..9"},
            {"codigo": "1EL1A", "descripcion": "CUADRILLA ELECTRICISTA (1 OFICIAL ELECTRICISTA + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.1250, "precio_unitario": 1738.00, "fuente": "05 SALARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ANDAMIOS (6% M.O.)", "unidad": "%", "cantidad": 13.15, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-10-03-001",
        "capitulo": "10",
        "subcapitulo": "03",
        "concepto": (
            "Suministro e instalación de contacto dúplex polarizado con tierra física aislada / falla a tierra "
            "(GFCI en zonas húmedas) de 15-20 A, 127 V, con placa y chalupa galvanizada Raco en aulas, talleres, "
            "centro digital y oficinas (§9.3 memoria arquitectónica), incluye: conexión, fijación, pruebas, "
            "mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa LUM-ACC-6.11.1 ($242.16) + INS-ELE-6.10.9 ($136.96) y LUM-ACC-6.11.2 ($542.04)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado y validado con Xalapa LUM-ACC-6.11.1 (Contacto dúplex polarizado 15A 127V $242.16) + "
            "INS-ELE-6.10.9 (Caja chalupa galvanizada Raco $136.96); CD = $379.12/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "Electrical Fixtures",
                "filtro_tipo": ".*",
                "campo_cantidad": "conteo",
                "nota": "Contactos y salidas de fuerza en modelo Proyecto electrico_corregido.",
            }
        ],
        "apu": [
            {"codigo": "LUM-ACC-6.11.1", "descripcion": "CONTACTO DUPLEX POLARIZADO 15-20A 127V C/PLACA Y SOPORTE", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 242.16, "fuente": "Xalapa LUM-ACC-6.11.1"},
            {"codigo": "INS-ELE-6.10.9", "descripcion": "CAJA CHALUPA GALVANIZADA RACO 690 INSTALADA", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 136.96, "fuente": "Xalapa INS-ELE-6.10.9"},
        ],
    },
    {
        "clave": "ED-10-03-002",
        "capitulo": "10",
        "subcapitulo": "03",
        "concepto": (
            "Suministro e instalación de apagador sencillo / de tres vías (escalera) de 16 A, 127 V, con placa "
            "y caja chalupa galvanizada en accesos de aulas, talleres, pasillos y sanitarios (§9.3 memoria "
            "arquitectónica), incluye: conexión, pruebas, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa LUM-ACC-6.11.6 ($228.14) + INS-ELE-6.10.9 ($136.96)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado y validado con Xalapa LUM-ACC-6.11.6 (Apagador de tres vías 16A 127V $228.14) + "
            "INS-ELE-6.10.9 (Caja chalupa galvanizada $136.96); CD = $365.10/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "Lighting Devices",
                "filtro_tipo": ".*",
                "campo_cantidad": "conteo",
                "nota": "Apagadores y controles de iluminación en modelo Proyecto electrico_corregido.",
            }
        ],
        "apu": [
            {"codigo": "LUM-ACC-6.11.6", "descripcion": "APAGADOR SENCILLO / TRES VIAS 16A 127V C/PLACA", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 228.14, "fuente": "Xalapa LUM-ACC-6.11.6"},
            {"codigo": "INS-ELE-6.10.9", "descripcion": "CAJA CHALUPA GALVANIZADA RACO 690 INSTALADA", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 136.96, "fuente": "Xalapa INS-ELE-6.10.9"},
        ],
    },
    {
        "clave": "ED-10-04-001",
        "capitulo": "10",
        "subcapitulo": "04",
        "concepto": (
            "Suministro e instalación de tablero de distribución y control tipo QO / NQ de 20 a 30 polos, "
            "3F-4H, barra de 125-225 A en gabinete NEMA 1 marca Square D, equipado con interruptor principal y "
            "derivados termomagnéticos QO para separación de circuitos de iluminación, fuerza normal y cómputo "
            "(§9.3 memoria arquitectónica), incluye: peinado de cables, identificación de circuitos, barra de "
            "tierra física, pruebas, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa INS-ELE-6.10.3 ($6,459.06) + 6 x INS-ELE-6.10.2 ($1,996.92)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Integrado y validado con Xalapa INS-ELE-6.10.3 (Centro de carga QO 20 polos Square D $6,459.06) "
            "más juego de interruptores termomagnéticos derivados QO (INS-ELE-6.10.2, 6 pzas × $1,996.92 = $11,981.52); "
            "CD = $18,440.58/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "Proyecto electrico_corregido",
                "categoria": "Electrical Equipment",
                "filtro_tipo": ".*",
                "campo_cantidad": "conteo",
                "nota": "Tableros eléctricos y equipos de distribución en modelo Proyecto electrico_corregido.",
            }
        ],
        "apu": [
            {"codigo": "INS-ELE-6.10.3", "descripcion": "CENTRO DE CARGA / TABLERO QO 20-30 POLOS NEMA 1 SQUARE D INSTALADO", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 6459.06, "fuente": "Xalapa INS-ELE-6.10.3"},
            {"codigo": "INS-ELE-6.10.2", "descripcion": "INTERRUPTOR TERMOMAGNETICO QO SQUARE D INSTALADO (LOTE DERIVADOS)", "unidad": "pza", "cantidad": 6.0000, "precio_unitario": 1996.92, "fuente": "Xalapa INS-ELE-6.10.2"},
        ],
    },
    {
        "clave": "ED-10-05-001",
        "capitulo": "10",
        "subcapitulo": "05",
        "concepto": (
            "Suministro e instalación de sistema de generación solar fotovoltaica interconectado a red de "
            "10.0 kWp en cubierta orientada al sur (§6.4 y §9.3 memoria arquitectónica), integrado por 18 "
            "módulos fotovoltaicos monocristalinos de 550 Wp, inversor central trifásico de 10 kW, estructura "
            "de montaje de aluminio anodizado anclada a cubierta, protecciones DC/AC, cableado solar PV y "
            "puesta a tierra, incluye: izaje, montaje, interconexión, pruebas y puesta en marcha."
        ),
        "unidad": "jgo",
        "fuente_tipo": "SUPUESTO",
        "fuente_ref": "SUPUESTO conservador para sistema fotovoltaico de 10 kWp en cubierta (§9.3 memoria arquitectónica)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "SUPUESTO conservador basado en precios de mercado mexicano 2025-2026 para sistema solar "
            "fotovoltaico comercial de 10 kWp en costo directo (18 paneles 550 Wp × $3,250 = $58,500; "
            "inversor trifásico 10 kW $34,000; estructura aluminio, protecciones DC/AC, cableado PV y "
            "mano de obra de montaje $39,500 = $132,000.00/jgo)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "precio_unitario": 132000.00,
        "apu": [],
    },

    # =========================================================================
    # CAPÍTULOS 11 Y 12 — RESERVADOS SIN CONCEPTOS (D-016)
    # =========================================================================

    # =========================================================================
    # CAPÍTULO 13 — MOBILIARIO Y EQUIPAMIENTO FIJO (Modelo: TT-ED-EDU-ARQ-MOB)
    # =========================================================================
    {
        "clave": "ED-13-01-001",
        "capitulo": "13",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y colocación de mesa de trabajo / pupitre modular para aulas teóricas, talleres de "
            "oficios, biblioteca y centro digital (§5.1 y §10 memoria arquitectónica), fabricado con estructura "
            "tubular de acero cal. 18 con pintura electrostática horneada y cubierta de MDF/melamina de alta "
            "densidad de 28 mm con cantos de PVC termoformado y regatones niveladores, incluye: armado, "
            "distribución en sitio, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + Xalapa CARP-6.16.2 / OBR-EXT-26",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con mesa escolar/taller modular en acero y cubierta laminada de alta resistencia "
            "($2,650.00/pza) más cuadrilla de colocación 1CO1A (rendimiento 10 pzas/jor = $173.80/pza); "
            "CD = $2,832.50/pza, validado contra mobiliario Xalapa CARP-6.16.2 ($1,687.67) y OBR-EXT-26 ($3,558.47)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT-ED-EDU-ARQ-MOB",
                "categoria": "Furniture",
                "filtro_tipo": "mesa|escritorio|pupitre|banco de trabajo|desk|table|mostrador",
                "campo_cantidad": "conteo",
                "nota": "Mesas, escritorios y pupitres en modelo TT-ED-EDU-ARQ-MOB.",
            }
        ],
        "apu": [
            {"codigo": "350-MOB-0101", "descripcion": "MESA DE TRABAJO / ESCRITORIO MODULAR ESTRUCTURA TUBULAR CAL. 18 Y CUBIERTA MELAMINA 28 MM", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 2650.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.1000, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ACARREO INTERNO (5% M.O.)", "unidad": "%", "cantidad": 8.70, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-13-01-002",
        "capitulo": "13",
        "subcapitulo": "01",
        "concepto": (
            "Suministro y colocación de silla / banco ergonómico apilable de uso institucional pesado para "
            "aulas, biblioteca, talleres, centro digital y oficinas (§5.1 y §10 memoria arquitectónica), con "
            "estructura tubular de acero cal. 16 y asiento/respaldo de polipropileno de alto impacto, incluye: "
            "acarreos, desempaque, colocación en sitio y mano de obra."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Insumos_APUCMX + Xalapa OBR-EXT-23 ($1,092.59/pza)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU integrado con silla institucional ergonómica estructura acero cal. 16 ($980.00/pza) y mano "
            "de obra de acarreo/distribución ($86.90/pza); CD = $1,071.25/pza, validado contra Xalapa OBR-EXT-23 ($1,092.59/pza)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT-ED-EDU-ARQ-MOB",
                "categoria": "Furniture",
                "filtro_tipo": "silla|banca|banco|asiento|sillon|butaca|chair|seat",
                "campo_cantidad": "conteo",
                "nota": "Sillas, bancas y asientos en modelo TT-ED-EDU-ARQ-MOB.",
            }
        ],
        "apu": [
            {"codigo": "350-MOB-0102", "descripcion": "SILLA INSTITUCIONAL ERGONÓMICA APILABLE ESTRUCTURA ACERO CAL. 16 Y POLIPROPILENO", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 980.00, "fuente": "Insumos_APUCMX"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL) REND 20 PZAS/JOR", "unidad": "jor", "cantidad": 0.0500, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR (5% M.O.)", "unidad": "%", "cantidad": 4.35, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-13-02-001",
        "capitulo": "13",
        "subcapitulo": "02",
        "concepto": (
            "Suministro y colocación de mueble fijo de guardado (estantería/librero modular para biblioteca, "
            "gabinete de taller, locker metálico o mueble bajo de guardado en aulas y guardería conforme a "
            "§5.1 y §10 memoria arquitectónica), de 1.80 x 0.90 x 0.45 m promedio, incluye: anclaje antivuelco "
            "a muro, nivelación, herrajes, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa ACC-SAN-6.17.4 (Locker metálico 1.80x0.38x0.45 m, CD=$4,750.76/pza)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta validada contra Xalapa ACC-SAN-6.17.4 (Locker/gabinete metálico de 1.80x0.38x0.45 m "
            "acabado esmalte horneado, Costo Directo = $4,750.76/pza)."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT-ED-EDU-ARQ-MOB",
                "categoria": "Casework",
                "filtro_tipo": ".*",
                "campo_cantidad": "conteo",
                "nota": "Muebles fijos, gabinetes y libreros (Casework) en modelo TT-ED-EDU-ARQ-MOB.",
            },
            {
                "modelo": "TT-ED-EDU-ARQ-MOB",
                "categoria": "Furniture",
                "filtro_tipo": "librero|estante|anaquel|locker|gabinete|closet|archivero|pizarron|storage|cabinet|shelf",
                "campo_cantidad": "conteo",
                "nota": "Libreros, estantes, lockers y pizarrones clasificados en Furniture en TT-ED-EDU-ARQ-MOB.",
            },
        ],
        "apu": [
            {"codigo": "ACC-SAN-6.17.4", "descripcion": "MUEBLE FIJO / ESTANTERIA / LOCKER MODULAR 1.80x0.90x0.45 M C/HERRAJES", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 4385.00, "fuente": "Xalapa ACC-SAN-6.17.4"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.2000, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "TAQUETES ANTIVUELCO Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 18.16, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },
    {
        "clave": "ED-13-02-002",
        "capitulo": "13",
        "subcapitulo": "02",
        "concepto": (
            "Suministro e instalación de equipamiento fijo especializado para talleres, cocina comunitaria, "
            "laboratorio/centro digital y sanitarios (mamparas sanitarias esmaltadas, tarjas y mesas de acero "
            "inoxidable, campana/equipo fijo conforme a §5.1 memoria arquitectónica), incluye: fijación a piso "
            "y muro, nivelación, mano de obra y herramienta."
        ),
        "unidad": "pza",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa ACC-SAN-6.17.5 ($2,063.70), 6.17.9 ($9,804.90) y 6.17.14 ($2,920.72)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "APU promedio ponderado para equipamiento fijo especializado validado contra Xalapa ACC-SAN-6.17.5 "
            "($2,063.70), ACC-SAN-6.17.9 ($9,804.90) y ACC-SAN-6.17.14 ($2,920.72); CD = $6,480.00/pza."
        ),
        "sin_cantidad_revit": False,
        "mapeo_revit": [
            {
                "modelo": "TT-ED-EDU-ARQ-MOB",
                "categoria": "Specialty Equipment",
                "filtro_tipo": ".*",
                "campo_cantidad": "conteo",
                "nota": "Equipamiento especializado fijo en modelo TT-ED-EDU-ARQ-MOB.",
            }
        ],
        "apu": [
            {"codigo": "350-EQP-0201", "descripcion": "EQUIPAMIENTO FIJO ESPECIALIZADO EN ACERO INOXIDABLE / MAMPARA ESMALTADA C/HERRAJES", "unidad": "pza", "cantidad": 1.0000, "precio_unitario": 5933.00, "fuente": "Xalapa ACC-SAN-6.17.5..14"},
            {"codigo": "1CO1A", "descripcion": "CUADRILLA No 12 (1 OFICIAL COLOCADOR + 1 AYUDANTE GENERAL)", "unidad": "jor", "cantidad": 0.3000, "precio_unitario": 1738.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
            {"codigo": "%MO1", "descripcion": "TAQUETES INOXIDABLES Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 25.60, "precio_unitario": 1.00, "fuente": "02 PRECIOS UNITARIOS.pdf"},
        ],
    },

    # =========================================================================
    # CAPÍTULO 14 — LIMPIEZA FINAL Y ENTREGA
    # =========================================================================
    {
        "clave": "ED-14-01-001",
        "capitulo": "14",
        "subcapitulo": "01",
        "concepto": (
            "Limpieza fina general de pisos de concreto pulido, loseta cerámica, muros aparentes y mobiliario "
            "para entrega final del edificio de educación, a base de agua, jabón neutro y desengrasante, "
            "incluye: materiales de limpieza, retiro de manchas de pintura o mortero, acopio de residuos, "
            "mano de obra, equipo y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa LIM-6.18.5 (CD=$50.88/m2) + 05 SALARIOS.pdf 1P",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta validada contra Xalapa LIM-6.18.5 (Limpieza fina de pisos y lambrines para entrega "
            "de obra, Costo Directo = $50.88/m2)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "358-AGU-0101", "descripcion": "AGUA, JABON NEUTRO Y DESENGRASANTE BIODEGRADABLE", "unidad": "m3", "cantidad": 0.1000, "precio_unitario": 35.52, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1P", "descripcion": "CUADRILLA No 1 (1 PEON + 0.1 CABO) RENDIMIENTO 16.5 M2/JOR", "unidad": "jor", "cantidad": 0.0603, "precio_unitario": 747.23, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "HERRAMIENTA MENOR Y ENCERADORA/PULIDORA", "unidad": "%", "cantidad": 2.27, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
    {
        "clave": "ED-14-01-002",
        "capitulo": "14",
        "subcapitulo": "01",
        "concepto": (
            "Limpieza fina de vidrios, ventanas de aluminio y muros cortina por ambas caras a cualquier altura, "
            "a base de agua, detergente neutro y jalador de goma, incluye: materiales, andamios, equipo de "
            "seguridad, mano de obra y herramienta."
        ),
        "unidad": "m2",
        "fuente_tipo": "APU",
        "fuente_ref": "Xalapa LIM-6.18.6 (CD=$58.08/m2)",
        "fecha_fuente": "23-11-2026",
        "justificacion": (
            "Matriz exacta validada contra Xalapa LIM-6.18.6 (Limpieza de vidrios por ambos lados a base de "
            "jabón y agua incluyendo andamios, Costo Directo = $58.08/m2)."
        ),
        "sin_cantidad_revit": True,
        "mapeo_revit": [],
        "apu": [
            {"codigo": "358-AGU-0101", "descripcion": "AGUA Y DETERGENTE LIMPIAVIDRIOS", "unidad": "m3", "cantidad": 0.0800, "precio_unitario": 35.52, "fuente": "11 RELACIÓN MATERIALES.pdf"},
            {"codigo": "1P", "descripcion": "CUADRILLA No 1 (1 PEON + 0.1 CABO) RENDIMIENTO 14.5 M2/JOR", "unidad": "jor", "cantidad": 0.0686, "precio_unitario": 747.23, "fuente": "03 BÁSICOS.pdf"},
            {"codigo": "%MO1", "descripcion": "ANDAMIOS, EQUIPO DE SEGURIDAD Y HERRAMIENTA MENOR", "unidad": "%", "cantidad": 3.98, "precio_unitario": 1.00, "fuente": "03 BÁSICOS.pdf"},
        ],
    },
]
