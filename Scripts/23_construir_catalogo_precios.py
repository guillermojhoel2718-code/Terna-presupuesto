"""Construcción y validación del catálogo de conceptos y precios unitarios (T-204 y T-205).

Agente: AG-2 (Precios) · Equipo: PC-B
Salidas atómicas (.tmp -> os.replace):
- _harness/intermedios/precios/catalogo_v01.json
- Catalogo de precios/catalogo_v01.json
- Catalogo de precios/resumen_catalogo_v01.md
- Catalogo de precios/Catalogo_precios_v01.xlsx (si openpyxl está disponible)
- _harness/intermedios/pdf/tabulador_cdmx_indice.json (si no existe aún)
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "Scripts" / "schemas"
for _p in (str(SCHEMAS_DIR), str(ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from common import FuenteTipo, Unidad, normalizar_unidad
from precios import (
    CatalogoPrecios,
    Concepto,
    InsumoAPU,
    MapeoRevit,
    ResumenCatalogo,
)


def _cargar_modulo(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {ruta}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def escribir_json_atomico(ruta: Path, datos: dict) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta.with_suffix(ruta.suffix + f".{os.getpid()}.tmp")
    tmp.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, ruta)


def escribir_texto_atomico(ruta: Path, texto: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta.with_suffix(ruta.suffix + f".{os.getpid()}.tmp")
    tmp.write_text(texto, encoding="utf-8")
    os.replace(tmp, ruta)


def asegurar_indice_tabulador() -> None:
    ruta_indice = ROOT / "_harness" / "intermedios" / "pdf" / "tabulador_cdmx_indice.json"
    if ruta_indice.exists():
        return
    mod20 = _cargar_modulo("proc20", ROOT / "Scripts" / "20_procesar_fuentes_precios.py")
    mod20.procesar_tabulador_cdmx()


def _inferir_tipo_insumo(codigo: str, unidad: str, descripcion: str) -> str:
    cod = codigo.upper()
    u = unidad.lower()
    desc = descripcion.upper()
    if cod.startswith("%") or "HERRAMIENTA" in desc:
        return "herramienta"
    if cod.startswith("MO") or u == "jor" or "CUADRILLA" in desc:
        return "mano_obra"
    if cod.startswith("EQ") or u in {"hr", "hor"}:
        return "equipo"
    if cod.startswith(("10401-", "14202-", "10301-", "14301-", "BA00")):
        return "basico"
    return "material"


# Mapa de conceptos con coincidencia directa en Tabulador CDMX Septiembre 2026 (D-003, D-011: P.U. = Costo Directo sin conversión)
TABULADOR_CDMX_2026_MATCHES: dict[str, dict] = {
    "ED-01-01-001": {"clave_tab": "BC12BB", "pagina": 9, "pu": 12.46, "desc_tab": "Desyerbe y limpia del terreno realizada a mano, incluye: acarreo libre a 20 m."},
    "ED-01-01-002": {"clave_tab": "BE12BB", "pagina": 11, "pu": 273.94, "desc_tab": "Despalme de material por medios manuales, todas las zonas."},
    "ED-01-02-001": {"clave_tab": "AF13DB", "pagina": 9, "pu": 10.10, "desc_tab": "Trazo y nivelación para desplante de estructura para edificación, con equipo de topografía."},
    "ED-02-01-001": {"clave_tab": "BF16DB", "pagina": 12, "pu": 479.39, "desc_tab": "Excavación a mano, material clase II-A, de 0.00 a 2.00 m de profundidad."},
    "ED-02-01-002": {"clave_tab": "GG13BB", "pagina": 77, "pu": 202.72, "desc_tab": "Plantilla de concreto hidráulico resistencia normal f'c=100 kg/cm2, de 5 cm de espesor."},
    "ED-02-02-001": {"clave_tab": "FG12CB", "pagina": 50, "pu": 4241.93, "desc_tab": "Suministro y colocación de concreto hidráulico f'c=250 kg/cm2 clase 1 bombeable en cimentación."},
    "ED-02-02-002": {"clave_tab": "CB12BD", "pagina": 31, "pu": 347.97, "desc_tab": "Cimbra acabado común y descimbra en cimentación (zapatas, contratrabes, dados)."},
    "ED-02-03-001": {"clave_tab": "BP12DC", "pagina": 30, "pu": 756.39, "desc_tab": "Relleno de excavación para estructuras, con tepetate, compactado al 90% con rodillo vibratorio."},
    "ED-02-03-002": {"clave_tab": "BN15BB", "pagina": 25, "pu": 188.03, "desc_tab": "Carga manual, acarreo en camión al primer kilómetro y descarga, de material fino o granular, medido en banco."},
    "ED-03-01-001": {"clave_tab": "FJ18BC", "pagina": 53, "pu": 4254.17, "desc_tab": "Suministro y colocación de concreto hidráulico estructural clase 1 f'c=250 kg/cm2 bombeable en superestructura (columnas, trabes, losas)."},
    "ED-03-01-002": {"clave_tab": "CC14BG", "pagina": 32, "pu": 454.76, "desc_tab": "Cimbra de madera acabado aparente y descimbra en columnas y trabes hasta 4.00 m de altura."},
    "ED-03-02-001": {"clave_tab": "FJ18BC", "pagina": 53, "pu": 4254.17, "desc_tab": "Suministro y colocación de concreto hidráulico estructural clase 1 f'c=250 kg/cm2 bombeable en superestructura (trabes y cadenas)."},
    "ED-03-03-001": {"clave_tab": "GL14BH", "pagina": 84, "pu": 819.18, "desc_tab": "Losa con vigueta pretensada P-13 y bovedilla de concreto con capa de compresión y malla electrosoldada 66-10-10."},
    "ED-04-01-001": {"clave_tab": "EB12BB", "pagina": 40, "pu": 74.11, "desc_tab": "Suministro, fabricación, transporte y montaje de estructura metálica formada con perfiles laminados."},
    "ED-04-01-002": {"clave_tab": "EB12CB", "pagina": 40, "pu": 72.10, "desc_tab": "Suministro, fabricación, transporte y montaje de estructura metálica formada con placas de acero A-36."},
    "ED-04-01-003": {"clave_tab": "EB14BD", "pagina": 40, "pu": 404.88, "desc_tab": "Suministro y colocación de ancla de acero rolado en frío de 25.4 mm (1\") de diámetro."},
    "ED-05-01-001": {"clave_tab": "GC22DC", "pagina": 64, "pu": 720.65, "desc_tab": "Muro de tabique de barro extruido aparente Novaceramic junteado con mortero cemento-arena 1:4."},
    "ED-05-01-002": {"clave_tab": "GC16BB", "pagina": 60, "pu": 707.07, "desc_tab": "Muro de tabique rojo recocido de 14 cm de espesor asentado con mortero cemento-arena 1:5."},
    "ED-05-02-001": {"clave_tab": "GH12BE", "pagina": 78, "pu": 350.35, "desc_tab": "Firme de concreto hidráulico resistencia normal f'c=150 kg/cm2 de 10 cm de espesor."},
    "ED-06-01-002": {"clave_tab": "GH16GB", "pagina": 80, "pu": 492.96, "desc_tab": "Piso de loseta cerámica de 30 x 30 cm asentada con pasta adhesiva pegazulejo y lechadeado."},
    "ED-06-01-003": {"clave_tab": "GH14BC", "pagina": 79, "pu": 442.10, "desc_tab": "Piso de concreto hidráulico f'c=150 kg/cm2 acabado escobillado reforzado con malla electrosoldada 66-1010."},
    "ED-06-02-001": {"clave_tab": "LG12CB", "pagina": 228, "pu": 87.10, "desc_tab": "Suministro y aplicación de pintura vinil acrílica en muros y plafones, previa preparación de superficie con sellador."},
    "ED-06-03-001": {"clave_tab": "GE12HJ", "pagina": 73, "pu": 639.70, "desc_tab": "Suministro e instalación de plafón modular registrable acústico de 0.61 x 0.61 m con suspensión visible."},
    "ED-06-04-001": {"clave_tab": "GS15BB", "pagina": 96, "pu": 558.36, "desc_tab": "Suministro y colocación de sistema de impermeabilización prefabricada con Festermip APP PS 4.0 mm gravilla roja e Hidroprimer."},
    "ED-07-01-001": {"clave_tab": "EH12BM", "pagina": 45, "pu": 5077.77, "desc_tab": "Suministro, habilitado y colocación de puerta de 1.00 x 2.10 m abatible en aluminio anodizado natural."},
    "ED-07-02-001": {"clave_tab": "EH12BJ", "pagina": 44, "pu": 3428.81, "desc_tab": "Suministro, habilitado y colocación de ventana de 1.80 x 1.20 m en aluminio anodizado natural de 3\"."},
    "ED-08-01-003": {"clave_tab": "IG13BF", "pagina": 151, "pu": 64.41, "desc_tab": "Codo de PVC tipo hidráulico unión cementar de 90° x 25 mm de diámetro."},
    "ED-08-01-004": {"clave_tab": "IC12CC", "pagina": 135, "pu": 817.34, "desc_tab": "Válvula de compuerta de bronce, extremos roscados."},
    "ED-09-01-001": {"clave_tab": "HB12BC", "pagina": 97, "pu": 64.12, "desc_tab": "Suministro, instalación y pruebas de tubo de PVC tipo sanitario unión cementar, extremos lisos de 51 mm."},
    "ED-09-01-002": {"clave_tab": "HB12BE", "pagina": 97, "pu": 113.21, "desc_tab": "Suministro, instalación y pruebas de tubo de PVC tipo sanitario unión cementar, extremos lisos de 102 mm."},
    "ED-09-01-003": {"clave_tab": "HB12EE", "pagina": 98, "pu": 109.51, "desc_tab": "Suministro, instalación y pruebas de codo de PVC tipo sanitario unión cementar de 90° x 102 mm."},
    "ED-09-02-001": {"clave_tab": "HI13BO", "pagina": 114, "pu": 5254.43, "desc_tab": "Suministro, instalación y pruebas de inodoro ecológico WC Drakar16 de 4.80 L por descarga, marca Helvex."},
    "ED-09-03-001": {"clave_tab": "HE12CC", "pagina": 112, "pu": 3162.50, "desc_tab": "Registro sanitario de 0.40 x 0.60 y 1.00 m de profundidad, medidas interiores, muros de tabique rojo recocido."},
    "ED-10-02-001": {"clave_tab": "KM13BB", "pagina": 211, "pu": 1934.64, "desc_tab": "Suministro, colocación y pruebas de luminario tipo LED panel de 30 x 122 cm, 40 W, modelo PANLED3-40-E3-DIMT-NW."},
    "ED-10-02-002": {"clave_tab": "KM13BG", "pagina": 211, "pu": 675.50, "desc_tab": "Suministro, colocación y pruebas de luminario tipo plafón circular LED de 18 W modelo SUX-18-LED-E3-NW."},
    "ED-10-04-001": {"clave_tab": "KN14BC", "pagina": 218, "pu": 7336.72, "desc_tab": "Suministro y colocación de tablero de alumbrado y distribución NQOD203L11, 20 polos, 100 amperes."},
}


def construir_conceptos(incluir_v02: bool = False) -> list[Concepto]:
    mod_01_06 = _cargar_modulo("cap01_06", ROOT / "Scripts" / "21_catalogo_cap01_06.py")
    mod_07_14 = _cargar_modulo("cap07_14", ROOT / "Scripts" / "22_catalogo_cap07_14.py")
    crudos: list[dict] = [dict(x) for x in list(mod_01_06.CAPITULOS_01_06) + list(mod_07_14.CAPITULOS_07_14)]

    if incluir_v02:
        mod_v02 = _cargar_modulo("cap_v02", ROOT / "Scripts" / "24_conceptos_adicionales_v02.py")
        overrides = getattr(mod_v02, "OVERRIDES_MAPEO_V02", {})
        for it in crudos:
            if it["clave"] in overrides:
                it["mapeo_revit"] = overrides[it["clave"]]
        crudos.extend(dict(x) for x in mod_v02.CONCEPTOS_ADICIONALES_V02)
        crudos.sort(key=lambda item: tuple(int(p) for p in item["clave"].split("-")[1:]))

    conceptos: list[Concepto] = []
    for item in crudos:
        apu_items: list[InsumoAPU] = []
        for ins in item.get("apu", []):
            cant = round(float(ins["cantidad"]), 6)
            pu = round(float(ins.get("precio", ins.get("precio_unitario", 0.0))), 4)
            imp = round(cant * pu, 2)
            u_norm = normalizar_unidad(str(ins["unidad"]))
            u_str = str(u_norm) if u_norm is not None else str(ins["unidad"]).lower()
            tipo_ins = ins.get("tipo") or _inferir_tipo_insumo(str(ins["codigo"]), u_str, str(ins["descripcion"]))
            apu_items.append(
                InsumoAPU(
                    codigo=str(ins["codigo"]),
                    descripcion=str(ins["descripcion"]),
                    tipo=tipo_ins,
                    unidad=u_str,
                    cantidad=cant,
                    precio=pu,
                    importe=imp,
                    fuente=str(ins["fuente"]),
                )
            )

        clave_c = item["clave"]
        if clave_c in TABULADOR_CDMX_2026_MATCHES:
            m_tab = TABULADOR_CDMX_2026_MATCHES[clave_c]
            ft = FuenteTipo.TABULADOR_CDMX
            pu_concepto = round(float(m_tab["pu"]), 2)
            fuente_ref = f"Tabulador CDMX Septiembre 2026 clave {m_tab['clave_tab']} (pág. {m_tab['pagina']})"
            pu_apu_ref = round(sum(i.importe for i in apu_items), 2) if apu_items else pu_concepto
            justificacion = (
                f"Tabulador CDMX Septiembre 2026 clave {m_tab['clave_tab']} (pág. {m_tab['pagina']}): "
                f"'{m_tab['desc_tab']}' — P.U. = ${pu_concepto:,.2f} (tomado directo como costo directo conforme a D-011). "
                f"Referencia cruzada APU Neodata/Xalapa: ${pu_apu_ref:,.2f}."
            )
        else:
            ft = FuenteTipo(item["fuente_tipo"])
            if ft == FuenteTipo.APU:
                pu_concepto = round(sum(i.importe for i in apu_items), 2)
            else:
                pu_concepto = round(float(item["precio_unitario"]), 2)
            fuente_ref = item["fuente_ref"]
            justificacion = item.get("justificacion")

        mapeos = [
            MapeoRevit(
                modelo=m.get("modelo"),
                categoria=m["categoria"],
                filtro_tipo=m.get("filtro_tipo"),
                campo_cantidad=m["campo_cantidad"],
                factor=float(m.get("factor", 1.0)),
            )
            for m in item.get("mapeo_revit", [])
        ]

        u_concepto = normalizar_unidad(str(item["unidad"]))
        if u_concepto is None:
            raise ValueError(f"Unidad inválida en {item['clave']}: {item['unidad']}")

        conceptos.append(
            Concepto(
                clave=item["clave"],
                capitulo=item["capitulo"],
                subcapitulo=item["subcapitulo"],
                concepto=item["concepto"],
                unidad=u_concepto,
                precio_unitario=pu_concepto,
                fuente_tipo=ft,
                fuente_ref=fuente_ref,
                fecha_fuente=item["fecha_fuente"],
                justificacion=justificacion,
                sin_cantidad_revit=bool(item.get("sin_cantidad_revit", False)),
                mapeo_revit=mapeos,
                apu=apu_items,
            )
        )
    return conceptos


def generar_resumen_md(cat: CatalogoPrecios) -> str:
    lineas = [
        "# Resumen del Catálogo de Conceptos y Precios Unitarios (`catalogo_v01`)",
        "",
        f"- **Alcance:** {cat.alcance}",
        f"- **Versión:** `{cat.version}` · **Fecha:** `{cat.fecha}` · **Agente:** `AG-2`",
        f"- **Total de conceptos:** **{cat.resumen.total_conceptos}**",
        f"- **Conceptos con precio (Costo Directo MXN):** **{cat.resumen.con_precio}**",
        f"- **Conceptos sin precio (`sin_precio`):** **{len(cat.resumen.sin_precio)}** ({', '.join(cat.resumen.sin_precio) if cat.resumen.sin_precio else 'ninguno'})",
        f"- **Conceptos marcados como `SUPUESTO`:** **{len(cat.resumen.supuestos)}** ({', '.join(cat.resumen.supuestos) if cat.resumen.supuestos else 'ninguno'})",
        "- **Capítulos 11 y 12:** 0 conceptos (`D-016`).",
        "- **Capítulo 05 (Albañilería):** mapeado a `TT-ED-EDU-ARQ-MOB` (`D-017`).",
        "",
        "## 1. Claves sin precio (`sin_precio`)",
        "",
    ]
    if not cat.resumen.sin_precio:
        lineas.append("- *(Ninguna — el 100% de las claves cuenta con Costo Directo validado)*")
    else:
        for cl in cat.resumen.sin_precio:
            lineas.append(f"- `{cl}`")

    lineas.extend([
        "",
        "## 2. Claves marcadas como `SUPUESTO`",
        "",
        "| Clave | Unidad | P.U. (CD MXN) | Justificación |",
        "|---|---|---:|---|",
    ])
    for c in cat.conceptos:
        u_txt = c.unidad.value if hasattr(c.unidad, "value") else str(c.unidad)
        if c.fuente_tipo == FuenteTipo.SUPUESTO:
            lineas.append(f"| `{c.clave}` | `{u_txt}` | ${c.precio_unitario:,.2f} | {c.justificacion} |")

    lineas.extend([
        "",
        "## 3. Catálogo completo por capítulo",
        "",
        "| Clave | Cap. | Unidad | P.U. (CD MXN) | Fuente tipo | Rev. Revit | Concepto (resumen) |",
        "|---|---:|---|---:|---|---|---|",
    ])
    for c in cat.conceptos:
        u_txt = c.unidad.value if hasattr(c.unidad, "value") else str(c.unidad)
        rev = "Sin cant. Revit" if c.sin_cantidad_revit else ", ".join(f"{m.categoria}:{m.campo_cantidad}" for m in c.mapeo_revit)
        desc_corta = c.concepto[:110] + ("..." if len(c.concepto) > 110 else "")
        lineas.append(
            f"| `{c.clave}` | `{c.capitulo}` | `{u_txt}` | ${c.precio_unitario:,.2f} | `{c.fuente_tipo.value}` | `{rev}` | {desc_corta} |"
        )
    return "\n".join(lineas) + "\n"


def exportar_excel(cat: CatalogoPrecios, ruta_xlsx: Path) -> bool:
    try:
        import openpyxl
        from openpyxl.styles import Alignment, Font, PatternFill
    except ImportError:
        return False

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Catalogo_v01"

    headers = [
        "Clave",
        "Capítulo",
        "Subcapítulo",
        "Concepto",
        "Unidad",
        "Costo Directo (MXN)",
        "Moneda",
        "Fuente Tipo",
        "Fuente Referencia",
        "Fecha Fuente",
        "Sin Cantidad Revit",
        "Mapeo Revit",
        "Justificación",
    ]
    ws.append(headers)
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for c in cat.conceptos:
        mapeo_str = "; ".join(
            f"{m.modelo or '*'}/{m.categoria}[{m.filtro_tipo}]->{m.campo_cantidad}"
            for m in c.mapeo_revit
        )
        ws.append([
            c.clave,
            c.capitulo,
            c.subcapitulo,
            c.concepto,
            c.unidad.value if hasattr(c.unidad, "value") else str(c.unidad),
            c.precio_unitario,
            "MXN",
            c.fuente_tipo.value if c.fuente_tipo else "",
            c.fuente_ref or "",
            c.fecha_fuente or "",
            "SÍ" if c.sin_cantidad_revit else "NO",
            mapeo_str,
            c.justificacion or "",
        ])

    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 12
    ws.column_dimensions["D"].width = 65
    ws.column_dimensions["E"].width = 10
    ws.column_dimensions["F"].width = 18
    ws.column_dimensions["H"].width = 16
    ws.column_dimensions["I"].width = 35
    ws.column_dimensions["L"].width = 40
    ws.column_dimensions["M"].width = 50

    ws_apu = wb.create_sheet(title="Matrices_APU")
    ws_apu.append(["Clave Concepto", "Código Insumo", "Descripción Insumo", "Tipo", "Unidad", "Cantidad", "P.U. (MXN)", "Importe (MXN)", "Fuente"])
    for col_idx in range(1, 10):
        cell = ws_apu.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font

    for c in cat.conceptos:
        for ins in c.apu:
            ws_apu.append([
                c.clave,
                ins.codigo,
                ins.descripcion,
                ins.tipo,
                ins.unidad,
                ins.cantidad,
                ins.precio,
                ins.importe,
                ins.fuente,
            ])

    ruta_xlsx.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta_xlsx.with_suffix(f".{os.getpid()}.tmp.xlsx")
    wb.save(tmp)
    os.replace(tmp, ruta_xlsx)
    return True


def _armar_catalogo(version: str, incluir_v02: bool) -> CatalogoPrecios:
    conceptos = construir_conceptos(incluir_v02=incluir_v02)
    cap_11_12 = [c.clave for c in conceptos if c.capitulo in {"11", "12"}]
    if cap_11_12:
        raise ValueError(f"Violación D-016: conceptos en capítulos 11 o 12: {cap_11_12}")
    sin_precio = [c.clave for c in conceptos if c.precio_unitario is None or c.precio_unitario <= 0]
    supuestos = [c.clave for c in conceptos if c.fuente_tipo == FuenteTipo.SUPUESTO]
    resumen = ResumenCatalogo(
        total_conceptos=len(conceptos),
        con_precio=len(conceptos) - len(sin_precio),
        sin_precio=sin_precio,
        supuestos=supuestos,
    )
    return CatalogoPrecios(
        version=version,
        fecha="23-11-2026",
        alcance="Edificio de educación (vínculos del modelo federado)",
        resumen=resumen,
        conceptos=conceptos,
    )


def main() -> int:
    asegurar_indice_tabulador()

    # 1. Construir y guardar catalogo_v01 (65 conceptos base con mapeo_revit D-019 / P-011)
    catalogo_v01 = _armar_catalogo("v01", incluir_v02=False)
    payload_v01 = catalogo_v01.model_dump(mode="json")
    escribir_json_atomico(ROOT / "_harness" / "intermedios" / "precios" / "catalogo_v01.json", payload_v01)
    escribir_json_atomico(ROOT / "Catalogo de precios" / "catalogo_v01.json", payload_v01)
    escribir_texto_atomico(ROOT / "Catalogo de precios" / "resumen_catalogo_v01.md", generar_resumen_md(catalogo_v01))
    exportar_excel(catalogo_v01, ROOT / "Catalogo de precios" / "Catalogo_precios_v01.xlsx")

    # 2. Construir y guardar catalogo_v02 (catálogo ampliado con todas las partidas del edificio ~2,500 m2)
    catalogo_v02 = _armar_catalogo("v02", incluir_v02=True)
    payload_v02 = catalogo_v02.model_dump(mode="json")
    escribir_json_atomico(ROOT / "_harness" / "intermedios" / "precios" / "catalogo_v02.json", payload_v02)
    escribir_json_atomico(ROOT / "Catalogo de precios" / "catalogo_v02.json", payload_v02)
    escribir_texto_atomico(ROOT / "Catalogo de precios" / "resumen_catalogo_v02.md", generar_resumen_md(catalogo_v02))

    mod25 = _cargar_modulo("excel25", ROOT / "Scripts" / "25_generar_catalogo_v02_excel_neodata.py")
    mod25.generar_plantilla_completada_xlsm(
        catalogo_v02,
        ROOT / "Catalogo de precios" / "Catalogo_precios_v02.xlsm",
        ROOT / "Catalogo de precios" / "Catalogo_precios_v02.xlsx",
    )

    # Sincronizar Scripts 20..25 al worktree local si existe
    worktree_scripts = Path(r"C:\Users\kukle\deska\workspaces\Presupuestos taller terminal\trabajo-en-paralelo-memo\Scripts")
    if worktree_scripts.exists():
        for sname in (
            "20_procesar_fuentes_precios.py",
            "21_catalogo_cap01_06.py",
            "22_catalogo_cap07_14.py",
            "23_construir_catalogo_precios.py",
            "24_conceptos_adicionales_v02.py",
            "25_generar_catalogo_v02_excel_neodata.py",
        ):
            src = ROOT / "Scripts" / sname
            dst = worktree_scripts / sname
            if src.exists() and dst.resolve() != src.resolve():
                shutil.copy2(src, dst)

    for cat in (catalogo_v01, catalogo_v02):
        r = cat.resumen
        por_ft = {}
        for c in cat.conceptos:
            k = c.fuente_tipo.value if c.fuente_tipo else "SIN"
            por_ft[k] = por_ft.get(k, 0) + 1
        print(
            f"OK [catalogo_{cat.version}]: total={r.total_conceptos}, con_precio={r.con_precio}, "
            f"sin_precio={len(r.sin_precio)}, fuentes={por_ft}, supuestos={r.supuestos}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
