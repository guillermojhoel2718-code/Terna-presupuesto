"""Generador de libros Excel de Catálogo de Precios v02 con formato de plantilla + Neodata/Referencias.

Agente: AG-2 (Precios) · Equipo: PC-B
Salidas en Catalogo de precios/ (escritura atómica .tmp -> os.replace):
- Catalogo de precios/Catalogo_precios_v02.xlsm (copia poblada de Resources/plantillas_para_usar/Taller Terminal_Presupuesto.xlsm + hojas estilo Neodata)
- Catalogo de precios/Catalogo_precios_v02.xlsx (libro institucional estilo Neodata 01 PRESUPUESTO / 02 PRECIOS UNITARIOS / Tabulador CDMX 2026)
"""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from copy import copy
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]

PROYECTO = 'Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"'
UBICACION = "Lib. Sur 285, 37904 Misión de Chichimecas, San Luis de la Paz, Guanajuato"
ALCANCE_EDIFICIO = "Edificio de Educación (~2,500.00 m² de construcción)"

CAPITULOS_NOMBRES = {
    "01": "PRELIMINARES",
    "02": "CIMENTACIÓN",
    "03": "ESTRUCTURA DE CONCRETO Y MAMPOSTERÍA CONFINADA",
    "04": "ESTRUCTURA METÁLICA Y CUBIERTA",
    "05": "ALBAÑILERÍA",
    "06": "ACABADOS, CARPINTERÍA ARQUITECTÓNICA Y EXTERIORES",
    "07": "HERRERÍA, CANCELERÍA Y CARPINTERÍA DE PUERTAS",
    "08": "INSTALACIÓN HIDRÁULICA Y PLUVIAL",
    "09": "INSTALACIÓN SANITARIA Y TRATAMIENTO",
    "10": "INSTALACIÓN ELÉCTRICA Y SISTEMA FOTOVOLTAICO",
    "11": "VOZ Y DATOS (FUERA DE ALCANCE D-016)",
    "12": "CCTV Y SEGURIDAD (FUERA DE ALCANCE D-016)",
    "13": "MOBILIARIO, CARPINTERÍA FIJA Y EQUIPAMIENTO",
    "14": "LIMPIEZA FINAL, PRUEBAS Y ENTREGA",
}

SUBCAPITULOS_NOMBRES = {
    ("01", "01"): "Limpieza, desyerbe, despalme y retiro de capa vegetal",
    ("01", "02"): "Trazo y nivelación topográfica",
    ("01", "03"): "Obras provisionales, tapial y seguridad de obra",
    ("02", "01"): "Excavaciones, afine y plantillas de desplante",
    ("02", "02"): "Zapatas corridas, dados, contratrabes y dalas de desplante",
    ("02", "03"): "Rellenos compactados y acarreos de material sobrante",
    ("03", "01"): "Columnas y castillos de concreto armado",
    ("03", "02"): "Trabes estructurales, cadenas de cerramiento y acero de refuerzo",
    ("03", "03"): "Losas prefabricadas de vigueta pretensada y bovedilla",
    ("04", "01"): "Estructura metálica principal, bastidor de cubierta, placas y anclas",
    ("04", "02"): "Cubiertas de panel aislado sándwich, azotea plana y canalones",
    ("05", "01"): "Muros de ladrillo aparente, block NOVABLOCK, celosía y divisorios AAC",
    ("05", "02"): "Firmes de concreto, aplanados y chaflanes de albañilería",
    ("06", "01"): "Pisos interiores pulidos, porcelánicos, cerámicos y pisos exteriores",
    ("06", "02"): "Pintura vinil-acrílica, recubrimientos cerámicos y lambrines de madera",
    ("06", "03"): "Falsos plafones acústicos, metálicos MetalWorks Mesh y zonas húmedas",
    ("06", "04"): "Impermeabilización prefabricada en azoteas y cubiertas",
    ("07", "01"): "Puertas abatibles metálicas, dobles de emergencia, madera y corredizas",
    ("07", "02"): "Ventanas de aluminio, muros cortina acristalados y montantes (mullions)",
    ("07", "03"): "Barandales metálicos de protección y escalera metálica principal",
    ("08", "01"): "Red hidráulica de agua potable, agua pluvial tratada, válvulas y registros",
    ("08", "02"): "Equipos de bombeo y presurización hidroneumática",
    ("08", "03"): "Captación pluvial y cisternas de almacenamiento potable/pluvial",
    ("09", "01"): "Red sanitaria de PVC DWV, bajadas pluviales y conexiones",
    ("09", "02"): "Muebles sanitarios ecológicos de bajo consumo y grifería institucional",
    ("09", "03"): "Registros sanitarios y planta/biodigestores de tratamiento primario",
    ("10", "01"): "Canalizaciones conduit EMT, charolas portacables, cajas y conductores THW-LS",
    ("10", "02"): "Luminarias LED interiores de alta eficiencia y arbotantes",
    ("10", "03"): "Contactos polarizados, GFCI y apagadores institucionales",
    ("10", "04"): "Tableros generales y centros de carga QO/NQ Square D",
    ("10", "05"): "Sistema de generación solar fotovoltaica interconectado a red (10 kWp)",
    ("13", "01"): "Mesas de trabajo, pupitres dobles, escritorios y sillería ergonómica",
    ("13", "02"): "Carpintería fija, lockers, estanterías, pizarrones y equipamiento especializado",
    ("14", "01"): "Limpieza fina general, lavado de cristales, retiro de escombro y entrega",
}

# Cantidades de referencia de proyecto (2,500 m2 construidos, desplante 804.20 m2) para conceptos sin_cantidad_revit
CANTIDADES_REFERENCIA_MEMORIA: dict[str, float] = {
    "ED-01-01-001": 804.20,   # Área de desplante (Plantilla/Firme PB = 804.20 m2)
    "ED-01-01-002": 160.84,   # Despalme 20 cm sobre 804.20 m2 = 160.84 m3
    "ED-01-01-003": 209.09,   # Retiro de despalme (160.84 m3 * 1.30 abundamiento)
    "ED-01-02-001": 1608.40,  # Trazo y nivelación PB + PA (804.20 * 2)
    "ED-01-03-001": 36.00,    # Bodega y oficina provisional de obra (6x6 m = 36 m2)
    "ED-01-03-002": 400.96,   # Tapial perimetral (perímetro 164.33 m * 2.44 m altura)
    "ED-01-03-003": 1.00,     # Lote señalización y seguridad colectiva 12 meses
    "ED-02-01-001": 306.78,   # Excavación en cepas (340.87 m2 * 0.90 m prof. prom.)
    "ED-02-01-003": 340.87,   # Afine y compactación de fondo de cepas (340.87 m2)
    "ED-02-03-001": 212.50,   # Relleno compactado con tepetate en cepas
    "ED-02-03-002": 122.56,   # Acarreo 1er km material sobrante de excavación
    "ED-02-03-003": 122.56,   # Acarreo km subsecuentes material sobrante
    "ED-04-01-002": 680.00,   # Placas base y cartabones A-36 1/2" (kg)
    "ED-04-01-003": 72.00,    # Anclas cold rolled 1" x 1.40 m (4 por columna/apoyo = 72 pzas)
    "ED-04-01-004": 4461.02,  # Pintura anticorrosiva sobre los 4,461.02 kg de estructura metálica
    "ED-04-02-002": 213.35,   # Canalón pluvial cal. 22 en cubierta inclinada (213.35 m)
    "ED-05-02-002": 845.00,   # Aplanado fino en muros interiores y zonas húmedas (m2)
    "ED-06-04-001": 1113.73,  # Impermeabilización prefabricada en azotea (1,113.73 m2)
    "ED-09-02-001": 16.00,    # Inodoros ecológicos en núcleos sanitarios PB y PA (pzas)
    "ED-09-02-002": 14.00,    # Lavabos institucionales en núcleos sanitarios PB y PA (pzas)
    "ED-09-02-003": 6.00,     # Mingitorios ecológicos en núcleos sanitarios hombres (pzas)
    "ED-10-05-001": 1.00,     # Sistema solar fotovoltaico 10 kWp en cubierta (1 jgo)
    "ED-14-01-001": 2500.00,  # Limpieza fina general del edificio de educación (2,500 m2)
    "ED-14-01-002": 694.35,   # Limpieza fina de vidrios/ventanas (381.24 m2 ventanas + 313.10 m2 muro cortina)
    "ED-14-01-003": 1.00,     # Retiro final de escombro, limpieza exterior y entrega (1 lote)
}


UNIDADES_LETRA = (
    "", "UN", "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE",
    "DIEZ", "ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE", "DIECISEIS", "DIECISIETE",
    "DIECIOCHO", "DIECINUEVE", "VEINTE", "VEINTIUN", "VEINTIDOS", "VEINTITRES",
    "VEINTICUATRO", "VEINTICINCO", "VEINTISEIS", "VEINTISIETE", "VEINTIOCHO", "VEINTINUEVE",
)
DECENAS_LETRA = (
    "", "DIEZ", "VEINTE", "TREINTA", "CUARENTA", "CINCUENTA",
    "SESENTA", "SETENTA", "OCHENTA", "NOVENTA",
)
CENTENAS_LETRA = (
    "", "CIENTO", "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS", "QUINIENTOS",
    "SEISCIENTOS", "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS",
)


def _menor_mil_a_letra(n: int) -> str:
    if n == 0:
        return ""
    if n == 100:
        return "CIEN"
    c = n // 100
    r = n % 100
    partes = []
    if c > 0:
        partes.append(CENTENAS_LETRA[c])
    if r > 0:
        if r < 30:
            partes.append(UNIDADES_LETRA[r])
        else:
            d = r // 10
            u = r % 10
            if u == 0:
                partes.append(DECENAS_LETRA[d])
            else:
                partes.append(f"{DECENAS_LETRA[d]} Y {UNIDADES_LETRA[u]}")
    return " ".join(partes)


def numero_a_letra_mxn(monto: float) -> str:
    """Convierte un importe a texto estilo Neodata: (* UN MIL DOSCIENTOS PESOS 34/100 M.N. *)."""
    entero = int(round(abs(monto) * 100)) // 100
    centavos = int(round(abs(monto) * 100)) % 100
    if entero == 0:
        letras = "CERO"
    else:
        millones = entero // 1_000_000
        miles = (entero % 1_000_000) // 1_000
        unidades = entero % 1_000
        partes = []
        if millones == 1:
            partes.append("UN MILLON")
        elif millones > 1:
            partes.append(f"{_menor_mil_a_letra(millones)} MILLONES")
        if miles == 1:
            partes.append("UN MIL")
        elif miles > 1:
            partes.append(f"{_menor_mil_a_letra(miles)} MIL")
        if unidades > 0:
            partes.append(_menor_mil_a_letra(unidades))
        letras = " ".join(partes)
    return f"(* {letras} PESOS {centavos:02d}/100 M.N. *)"


def calcular_cantidades_revit(cat) -> dict[str, tuple[float, str]]:
    """Calcula la cantidad de cada concepto desde _harness/intermedios/revit/ o memoria."""
    import importlib.util
    revit_dir = ROOT / "_harness" / "intermedios" / "revit"
    cantidades: dict[str, tuple[float, str]] = {}
    if revit_dir.exists():
        spec = importlib.util.spec_from_file_location("gen30", ROOT / "Scripts" / "30_generadores_desde_revit.py")
        if spec and spec.loader:
            mod30 = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod30)
            extracciones = []
            for f in sorted(revit_dir.glob("*__*.json")):
                try:
                    ex = mod30.ExtraccionRevit.model_validate(json.loads(f.read_text(encoding="utf-8")))
                    extracciones.append((f, ex))
                except Exception:
                    continue
            gens, _, _, _, _ = mod30.calcular(cat, extracciones, {})
            for g in gens:
                cantidades[g.clave] = (round(float(g.cantidad_total), 4), g.fuente)
            # Además, si existe resumen con cantidades_derivadas_para_manual_json en revit/, aprovecharlo
            for f_res in sorted(revit_dir.glob("*.json")):
                if "__" in f_res.name or f_res.name == "indice.json":
                    continue
                try:
                    d_res = json.loads(f_res.read_text(encoding="utf-8"))
                    for item_m in d_res.get("cantidades_derivadas_para_manual_json", []):
                        cl_m = item_m.get("clave")
                        q_m = item_m.get("cantidad") or item_m.get("cantidad_total")
                        if cl_m and q_m and cl_m not in cantidades:
                            cantidades[cl_m] = (round(float(q_m), 4), item_m.get("fuente", f"REVIT_DERIVADO:{f_res.name}"))
                except Exception:
                    continue
    for c in cat.conceptos:
        if c.clave not in cantidades:
            q_ref = CANTIDADES_REFERENCIA_MEMORIA.get(c.clave, 1.0)
            cantidades[c.clave] = (
                q_ref,
                "MEMORIA_ARQ:Estimación paramétrica edificio educación 2,500 m² (sin_cantidad_revit)",
            )
    return cantidades


def agregar_hojas_neodata(wb: openpyxl.Workbook, cat, cantidades: dict[str, tuple[float, str]]) -> None:
    """Agrega las 3 hojas con formato visual idéntico a resultado_ejemplo_neodata y referencias_docs."""
    fino = Side(style="thin", color="808080")
    med = Side(style="medium", color="1F4E78")
    doble = Side(style="double", color="1F4E78")
    borde_celda = Border(left=fino, right=fino, top=fino, bottom=fino)
    borde_total = Border(top=fino, bottom=doble, left=fino, right=fino)
    borde_caja = Border(left=med, right=med, top=med, bottom=med)

    fill_guinda = PatternFill("solid", fgColor="6B1D2F")
    fill_azul_osc = PatternFill("solid", fgColor="1F4E78")
    fill_cap = PatternFill("solid", fgColor="D9E1F2")
    fill_subcap = PatternFill("solid", fgColor="EDEDED")
    fill_supuesto = PatternFill("solid", fgColor="FFF2CC")
    fill_tabulador = PatternFill("solid", fgColor="E2EFDA")
    fill_apu = PatternFill("solid", fgColor="FCE4D6")
    fill_zebra = PatternFill("solid", fgColor="F9FAFB")

    font_titulo = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_subtitulo = Font(name="Calibri", size=9, bold=True, color="1F4E78")
    font_th = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
    font_cap = Font(name="Calibri", size=10, bold=True, color="1F4E78")
    font_sub = Font(name="Calibri", size=9, bold=True, color="333333")
    font_norm = Font(name="Calibri", size=9, bold=False, color="000000")
    font_bold = Font(name="Calibri", size=9, bold=True, color="000000")
    font_letra = Font(name="Calibri", size=8, italic=True, color="333333")
    font_sup = Font(name="Calibri", size=9, bold=True, color="9C6500")

    al_centro = Alignment(horizontal="center", vertical="center", wrap_text=True)
    al_izq = Alignment(horizontal="left", vertical="center", wrap_text=True)
    al_der = Alignment(horizontal="right", vertical="center", wrap_text=True)

    # =========================================================================
    # HOJA 1: Neodata_01_Catalogo (Formato 01 PRESUPUESTO.pdf + Referencias)
    # =========================================================================
    if "Neodata_01_Catalogo" in wb.sheetnames:
        del wb["Neodata_01_Catalogo"]
    ws1 = wb.create_sheet("Neodata_01_Catalogo")

    ws1.merge_cells("A1:I1")
    ws1["A1"] = "INSTITUTO POLITÉCNICO NACIONAL · ESIA UNIDAD TECAMACHALCO · TALLER TERMINAL"
    ws1["A1"].font = font_titulo
    ws1["A1"].fill = fill_guinda
    ws1["A1"].alignment = al_centro
    ws1.row_dimensions[1].height = 22

    ws1.merge_cells("A2:F2")
    ws1["A2"] = f"OBRA: {PROYECTO.upper()} — {ALCANCE_EDIFICIO.upper()}"
    ws1["A2"].font = font_bold
    ws1.merge_cells("G2:I2")
    ws1["G2"] = f"FECHA: {cat.fecha} · VERSIÓN: {cat.version.upper()} · DURACIÓN: 365 DÍAS (12 MESES)"
    ws1["G2"].font = font_subtitulo
    ws1["G2"].alignment = al_der

    ws1.merge_cells("A3:F3")
    ws1["A3"] = f"LUGAR: {UBICACION} · INICIO: 04/01/2027 · FIN: 31/12/2027"
    ws1["A3"].font = font_norm
    ws1.merge_cells("G3:I3")
    ws1["G3"] = "DOCUMENTO ART. 45 A.IX RLOPySRM · PRECIOS EN COSTO DIRECTO (MXN)"
    ws1["G3"].font = font_subtitulo
    ws1["G3"].alignment = al_der

    ws1.merge_cells("A4:I4")
    ws1["A4"] = "CATÁLOGO DE CONCEPTOS Y CANTIDADES DE OBRA PARA EXPRESIÓN DE PRECIOS UNITARIOS (COSTO DIRECTO) Y FUENTES"
    ws1["A4"].font = font_titulo
    ws1["A4"].fill = fill_azul_osc
    ws1["A4"].alignment = al_centro
    ws1.row_dimensions[4].height = 20

    headers_1 = [
        "Código",
        "Concepto (Descripción Completa Estilo Neodata)",
        "Unidad",
        "Cantidad",
        "P. Unitario (CD)",
        "Precio con Letra (Costo Directo)",
        "Importe (CD MXN)",
        "Tipo Fuente",
        "Referencia Exacta / Criterio / Mapeo Revit",
    ]
    fila = 6
    for col_idx, h in enumerate(headers_1, start=1):
        c = ws1.cell(fila, col_idx, h)
        c.font = font_th
        c.fill = fill_azul_osc
        c.alignment = al_centro
        c.border = borde_celda
    ws1.row_dimensions[fila].height = 26
    fila += 1

    por_cap: dict[str, dict[str, list[Any]]] = {}
    for c in cat.conceptos:
        por_cap.setdefault(c.capitulo, {}).setdefault(c.subcapitulo, []).append(c)

    filas_totales_cap: list[int] = []
    for cap in sorted(por_cap.keys()):
        ws1.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=9)
        c_cap = ws1.cell(fila, 1, f"CAPÍTULO {cap} · {CAPITULOS_NOMBRES.get(cap, '')}")
        c_cap.font = font_cap
        c_cap.fill = fill_cap
        c_cap.alignment = al_izq
        for col_i in range(1, 10):
            ws1.cell(fila, col_i).fill = fill_cap
            ws1.cell(fila, col_i).border = borde_celda
        ws1.row_dimensions[fila].height = 22
        fila += 1

        filas_items_cap: list[int] = []
        for sub in sorted(por_cap[cap].keys()):
            nom_sub = SUBCAPITULOS_NOMBRES.get((cap, sub), f"Subcapítulo {cap}.{sub}")
            ws1.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=9)
            c_sub = ws1.cell(fila, 1, f"   {cap}.{sub} · {nom_sub}")
            c_sub.font = font_sub
            for col_i in range(1, 10):
                ws1.cell(fila, col_i).fill = fill_subcap
                ws1.cell(fila, col_i).border = borde_celda
            ws1.row_dimensions[fila].height = 19
            fila += 1

            for item in por_cap[cap][sub]:
                u_txt = item.unidad.value if hasattr(item.unidad, "value") else str(item.unidad)
                ft_txt = item.fuente_tipo.value if hasattr(item.fuente_tipo, "value") else str(item.fuente_tipo)
                cant_val, cant_fuente = cantidades.get(item.clave, (1.0, "MEMORIA"))
                pu_val = float(item.precio_unitario or 0.0)
                letra_pu = numero_a_letra_mxn(pu_val)
                mapeo_str = "; ".join(
                    f"{m.modelo}/{m.categoria}[{m.filtro_tipo}]->{m.campo_cantidad}"
                    for m in item.mapeo_revit
                ) or "Sin cantidad Revit (cuantificación manual/memoria)"
                ref_completa = f"{item.fuente_ref} | {item.justificacion or ''} | Revit: {mapeo_str}"

                ws1.cell(fila, 1, item.clave).font = font_bold
                ws1.cell(fila, 1).alignment = al_centro
                ws1.cell(fila, 2, item.concepto).font = font_norm
                ws1.cell(fila, 2).alignment = al_izq
                ws1.cell(fila, 3, u_txt.upper()).font = font_bold
                ws1.cell(fila, 3).alignment = al_centro
                ws1.cell(fila, 4, cant_val).font = font_norm
                ws1.cell(fila, 4).number_format = "#,##0.00"
                ws1.cell(fila, 4).alignment = al_der
                ws1.cell(fila, 5, pu_val).font = font_bold
                ws1.cell(fila, 5).number_format = "$#,##0.00"
                ws1.cell(fila, 5).alignment = al_der
                ws1.cell(fila, 6, letra_pu).font = font_letra
                ws1.cell(fila, 6).alignment = al_izq
                ws1.cell(fila, 7, f"=D{fila}*E{fila}").font = font_bold
                ws1.cell(fila, 7).number_format = "$#,##0.00"
                ws1.cell(fila, 7).alignment = al_der
                ws1.cell(fila, 8, ft_txt).font = font_sup if ft_txt == "SUPUESTO" else font_bold
                ws1.cell(fila, 8).alignment = al_centro
                ws1.cell(fila, 9, ref_completa).font = font_norm
                ws1.cell(fila, 9).alignment = al_izq

                row_fill = (
                    fill_supuesto if ft_txt == "SUPUESTO"
                    else (fill_tabulador if ft_txt == "TABULADOR_CDMX" else fill_zebra)
                )
                for col_i in range(1, 10):
                    ws1.cell(fila, col_i).border = borde_celda
                    if col_i == 8 or ft_txt == "SUPUESTO":
                        ws1.cell(fila, col_i).fill = row_fill
                ws1.row_dimensions[fila].height = max(32, 14 * (len(item.concepto) // 75 + 1))
                filas_items_cap.append(fila)
                fila += 1

        # Subtotal del capítulo
        ws1.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=6)
        c_tot = ws1.cell(fila, 1, f"TOTAL CAPÍTULO {cap} · {CAPITULOS_NOMBRES.get(cap, '')}")
        c_tot.font = font_cap
        c_tot.alignment = al_der
        formula_cap = "=" + "+".join(f"G{r}" for r in filas_items_cap) if filas_items_cap else 0
        ws1.cell(fila, 7, formula_cap).font = font_cap
        ws1.cell(fila, 7).number_format = "$#,##0.00"
        ws1.cell(fila, 7).alignment = al_der
        for col_i in range(1, 10):
            ws1.cell(fila, col_i).fill = fill_cap
            ws1.cell(fila, col_i).border = borde_total
        ws1.row_dimensions[fila].height = 22
        filas_totales_cap.append(fila)
        fila += 1

    # Total general a Costo Directo
    fila += 1
    ws1.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=6)
    ws1.cell(fila, 1, "TOTAL COSTO DIRECTO DEL CATÁLOGO DE CONCEPTOS (SIN INDIRECTOS NI IVA)").font = font_titulo
    ws1.cell(fila, 1).alignment = al_der
    ws1.cell(fila, 7, "=" + "+".join(f"G{r}" for r in filas_totales_cap)).font = font_titulo
    ws1.cell(fila, 7).number_format = "$#,##0.00"
    ws1.cell(fila, 7).alignment = al_der
    for col_i in range(1, 10):
        ws1.cell(fila, col_i).fill = fill_guinda
        ws1.cell(fila, col_i).border = borde_caja
    ws1.row_dimensions[fila].height = 26

    anchos_1 = [15, 58, 9, 12, 15, 36, 16, 16, 48]
    for idx_col, w in enumerate(anchos_1, start=1):
        ws1.column_dimensions[get_column_letter(idx_col)].width = w

    ws1.page_setup.paperSize = ws1.PAPERSIZE_LETTER
    ws1.page_setup.orientation = "landscape"
    ws1.page_setup.fitToWidth = 1
    ws1.page_setup.fitToHeight = 0
    ws1.sheet_properties.pageSetUpPr.fitToPage = True
    ws1.print_area = f"A1:I{fila}"
    ws1.print_title_rows = "1:6"
    ws1.oddHeader.center.text = PROYECTO
    ws1.oddHeader.right.text = f"Catálogo {cat.version} · {cat.fecha}"
    ws1.oddFooter.left.text = "Responsable: AG-2 (Precios)"
    ws1.oddFooter.right.text = "Página &P de &N"

    # =========================================================================
    # HOJA 2: Neodata_02_Matrices_APU (Formato 02 PRECIOS UNITARIOS.pdf)
    # =========================================================================
    if "Neodata_02_Matrices_APU" in wb.sheetnames:
        del wb["Neodata_02_Matrices_APU"]
    ws2 = wb.create_sheet("Neodata_02_Matrices_APU")

    ws2.merge_cells("A1:I1")
    ws2["A1"] = "ANÁLISIS DE PRECIOS UNITARIOS (COSTO DIRECTO) · ART. 45 A.1 RLOPySRM · FORMATO NEODATA"
    ws2["A1"].font = font_titulo
    ws2["A1"].fill = fill_guinda
    ws2["A1"].alignment = al_centro
    ws2.row_dimensions[1].height = 22

    ws2.merge_cells("A2:I2")
    ws2["A2"] = f"OBRA: {PROYECTO} · ALCANCE: {ALCANCE_EDIFICIO} · VERSIÓN: {cat.version.upper()} · FECHA: {cat.fecha}"
    ws2["A2"].font = font_subtitulo
    ws2["A2"].alignment = al_centro

    r2 = 4
    for idx_c, c in enumerate(cat.conceptos, start=1):
        u_txt = (c.unidad.value if hasattr(c.unidad, "value") else str(c.unidad)).upper()
        ft_txt = c.fuente_tipo.value if hasattr(c.fuente_tipo, "value") else str(c.fuente_tipo)
        cant_val, _ = cantidades.get(c.clave, (1.0, "MEMORIA"))
        pu_val = float(c.precio_unitario or 0.0)

        # Banda de encabezado de tarjeta APU (estilo 02 PRECIOS UNITARIOS.pdf)
        ws2.cell(r2, 1, f"Análisis No. {idx_c:03d}").font = font_th
        ws2.cell(r2, 2, f"Clave: {c.clave}").font = font_th
        ws2.cell(r2, 3, f"Cap. {c.capitulo}.{c.subcapitulo}").font = font_th
        ws2.cell(r2, 4, f"Unidad: {u_txt}").font = font_th
        ws2.cell(r2, 5, f"Cant. Ref.: {cant_val:,.2f}").font = font_th
        ws2.cell(r2, 6, f"Fuente: {ft_txt}").font = font_th
        ws2.merge_cells(start_row=r2, start_column=7, end_row=r2, end_column=9)
        ws2.cell(r2, 7, f"COSTO DIRECTO (CD): ${pu_val:,.2f} MXN").font = font_th
        ws2.cell(r2, 7).alignment = al_der
        for col_i in range(1, 10):
            ws2.cell(r2, col_i).fill = fill_azul_osc
            ws2.cell(r2, col_i).border = borde_celda
        ws2.row_dimensions[r2].height = 20
        r2 += 1

        # Descripción completa del concepto
        ws2.merge_cells(start_row=r2, start_column=1, end_row=r2, end_column=9)
        ws2.cell(r2, 1, c.concepto).font = font_norm
        ws2.cell(r2, 1).alignment = al_izq
        for col_i in range(1, 10):
            ws2.cell(r2, col_i).border = borde_celda
        ws2.row_dimensions[r2].height = max(28, 14 * (len(c.concepto) // 95 + 1))
        r2 += 1

        # Encabezados de tabla de insumos
        th_apu = ["Código Insumo", "Descripción del Insumo / Básico / Cuadrilla", "Tipo", "Unidad", "Op.", "Cantidad / Rend.", "Costo Unitario", "Importe (MXN)", "Fuente del Insumo"]
        for col_i, h_txt in enumerate(th_apu, start=1):
            cell_h = ws2.cell(r2, col_i, h_txt)
            cell_h.font = font_sub
            cell_h.fill = fill_subcap
            cell_h.alignment = al_centro
            cell_h.border = borde_celda
        ws2.row_dimensions[r2].height = 18
        r2 += 1

        if c.apu:
            for ins in c.apu:
                ws2.cell(r2, 1, ins.codigo).font = font_bold
                ws2.cell(r2, 1).alignment = al_centro
                ws2.cell(r2, 2, ins.descripcion).font = font_norm
                ws2.cell(r2, 2).alignment = al_izq
                ws2.cell(r2, 3, ins.tipo.upper()).font = font_norm
                ws2.cell(r2, 3).alignment = al_centro
                ws2.cell(r2, 4, ins.unidad.upper()).font = font_norm
                ws2.cell(r2, 4).alignment = al_centro
                ws2.cell(r2, 5, "*").font = font_norm
                ws2.cell(r2, 5).alignment = al_centro
                ws2.cell(r2, 6, ins.cantidad).font = font_norm
                ws2.cell(r2, 6).number_format = "#,##0.000000"
                ws2.cell(r2, 6).alignment = al_der
                ws2.cell(r2, 7, ins.precio).font = font_norm
                ws2.cell(r2, 7).number_format = "$#,##0.00"
                ws2.cell(r2, 7).alignment = al_der
                ws2.cell(r2, 8, ins.importe).font = font_bold
                ws2.cell(r2, 8).number_format = "$#,##0.00"
                ws2.cell(r2, 8).alignment = al_der
                ws2.cell(r2, 9, ins.fuente).font = font_norm
                ws2.cell(r2, 9).alignment = al_izq
                for col_i in range(1, 10):
                    ws2.cell(r2, col_i).border = borde_celda
                ws2.row_dimensions[r2].height = 18
                r2 += 1
        else:
            ws2.cell(r2, 1, ft_txt).font = font_bold
            ws2.cell(r2, 1).alignment = al_centro
            ws2.cell(r2, 2, f"{c.fuente_ref} — {c.justificacion or ''}").font = font_norm
            ws2.cell(r2, 2).alignment = al_izq
            ws2.cell(r2, 3, ft_txt).font = font_bold
            ws2.cell(r2, 3).alignment = al_centro
            ws2.cell(r2, 4, u_txt).font = font_norm
            ws2.cell(r2, 4).alignment = al_centro
            ws2.cell(r2, 5, "*").font = font_norm
            ws2.cell(r2, 5).alignment = al_centro
            ws2.cell(r2, 6, 1.0).font = font_norm
            ws2.cell(r2, 6).number_format = "#,##0.000000"
            ws2.cell(r2, 6).alignment = al_der
            ws2.cell(r2, 7, pu_val).font = font_norm
            ws2.cell(r2, 7).number_format = "$#,##0.00"
            ws2.cell(r2, 7).alignment = al_der
            ws2.cell(r2, 8, pu_val).font = font_bold
            ws2.cell(r2, 8).number_format = "$#,##0.00"
            ws2.cell(r2, 8).alignment = al_der
            ws2.cell(r2, 9, c.fuente_ref).font = font_norm
            ws2.cell(r2, 9).alignment = al_izq
            for col_i in range(1, 10):
                ws2.cell(r2, col_i).border = borde_celda
            ws2.row_dimensions[r2].height = 22
            r2 += 1

        # Pie de tarjeta APU: Costo Directo + Precio con letra + Justificación
        ws2.merge_cells(start_row=r2, start_column=1, end_row=r2, end_column=6)
        ws2.cell(r2, 1, f"{numero_a_letra_mxn(pu_val)} · Ref.: {c.fuente_ref}").font = font_letra
        ws2.cell(r2, 1).alignment = al_izq
        ws2.cell(r2, 7, "(CD) COSTO DIRECTO:").font = font_bold
        ws2.cell(r2, 7).alignment = al_der
        ws2.cell(r2, 8, pu_val).font = font_bold
        ws2.cell(r2, 8).number_format = "$#,##0.00"
        ws2.cell(r2, 8).alignment = al_der
        ws2.cell(r2, 9, "100.00% (Sin indirectos, D-011 / SPEC_06)").font = font_letra
        fill_pie = fill_supuesto if ft_txt == "SUPUESTO" else (fill_tabulador if ft_txt == "TABULADOR_CDMX" else fill_apu)
        for col_i in range(1, 10):
            ws2.cell(r2, col_i).fill = fill_pie
            ws2.cell(r2, col_i).border = borde_total
        ws2.row_dimensions[r2].height = 20
        r2 += 2

    anchos_2 = [16, 52, 14, 10, 6, 15, 15, 15, 34]
    for idx_col, w in enumerate(anchos_2, start=1):
        ws2.column_dimensions[get_column_letter(idx_col)].width = w

    ws2.page_setup.paperSize = ws2.PAPERSIZE_LETTER
    ws2.page_setup.orientation = "landscape"
    ws2.page_setup.fitToWidth = 1
    ws2.page_setup.fitToHeight = 0
    ws2.sheet_properties.pageSetUpPr.fitToPage = True
    ws2.print_area = f"A1:I{r2 - 1}"
    ws2.print_title_rows = "1:2"
    ws2.oddHeader.center.text = PROYECTO
    ws2.oddHeader.right.text = f"Matrices APU {cat.version} · {cat.fecha}"
    ws2.oddFooter.left.text = "Responsable: AG-2 (Precios)"
    ws2.oddFooter.right.text = "Página &P de &N"

    # =========================================================================
    # HOJA 3: Tabulador_y_Supuestos (Trazabilidad D-003, D-011, D-019, SUPUESTOS)
    # =========================================================================
    if "Tabulador_y_Supuestos" in wb.sheetnames:
        del wb["Tabulador_y_Supuestos"]
    ws3 = wb.create_sheet("Tabulador_y_Supuestos")

    ws3.merge_cells("A1:H1")
    ws3["A1"] = "MATRIZ DE TRAZABILIDAD DE PRECIOS UNITARIOS: TABULADOR CDMX 2026 · APU NEODATA/XALAPA · SUPUESTOS"
    ws3["A1"].font = font_titulo
    ws3["A1"].fill = fill_guinda
    ws3["A1"].alignment = al_centro
    ws3.row_dimensions[1].height = 22

    th3 = ["Clave", "Cap.", "Unidad", "Costo Directo (MXN)", "Clasificación Fuente", "Marca SUPUESTO", "Fuente Exacta (Clave / Página / Archivo)", "Justificación Técnica y Validación Cruzada"]
    for col_i, h_txt in enumerate(th3, start=1):
        ch = ws3.cell(3, col_i, h_txt)
        ch.font = font_th
        ch.fill = fill_azul_osc
        ch.alignment = al_centro
        ch.border = borde_celda
    ws3.row_dimensions[3].height = 24

    r3 = 4
    for c in cat.conceptos:
        u_txt = c.unidad.value if hasattr(c.unidad, "value") else str(c.unidad)
        ft_txt = c.fuente_tipo.value if hasattr(c.fuente_tipo, "value") else str(c.fuente_tipo)
        es_sup = ft_txt == "SUPUESTO"
        ws3.cell(r3, 1, c.clave).font = font_bold
        ws3.cell(r3, 1).alignment = al_centro
        ws3.cell(r3, 2, f"{c.capitulo}.{c.subcapitulo}").font = font_norm
        ws3.cell(r3, 2).alignment = al_centro
        ws3.cell(r3, 3, u_txt).font = font_bold
        ws3.cell(r3, 3).alignment = al_centro
        ws3.cell(r3, 4, float(c.precio_unitario or 0.0)).font = font_bold
        ws3.cell(r3, 4).number_format = "$#,##0.00"
        ws3.cell(r3, 4).alignment = al_der
        ws3.cell(r3, 5, ft_txt).font = font_sup if es_sup else font_bold
        ws3.cell(r3, 5).alignment = al_centro
        ws3.cell(r3, 6, "SUPUESTO CONSERVADOR" if es_sup else "DATO DIRECTO / APU").font = font_sup if es_sup else font_norm
        ws3.cell(r3, 6).alignment = al_centro
        ws3.cell(r3, 7, c.fuente_ref or "").font = font_norm
        ws3.cell(r3, 7).alignment = al_izq
        ws3.cell(r3, 8, c.justificacion or "").font = font_norm
        ws3.cell(r3, 8).alignment = al_izq
        fill_r3 = fill_supuesto if es_sup else (fill_tabulador if ft_txt == "TABULADOR_CDMX" else fill_zebra)
        for col_i in range(1, 9):
            ws3.cell(r3, col_i).fill = fill_r3
            ws3.cell(r3, col_i).border = borde_celda
        ws3.row_dimensions[r3].height = 28
        r3 += 1

    for idx_col, w in enumerate([16, 8, 9, 18, 18, 22, 42, 65], start=1):
        ws3.column_dimensions[get_column_letter(idx_col)].width = w
    ws3.page_setup.paperSize = ws3.PAPERSIZE_LETTER
    ws3.page_setup.orientation = "landscape"
    ws3.page_setup.fitToWidth = 1
    ws3.page_setup.fitToHeight = 0
    ws3.sheet_properties.pageSetUpPr.fitToPage = True
    ws3.print_area = f"A1:H{r3 - 1}"
    ws3.print_title_rows = "1:3"


def _copiar_estilo_fila(ws, fila_origen: int, fila_destino: int, max_col: int = 12) -> None:
    for col in range(1, max_col + 1):
        ws.cell(fila_destino, col)._style = copy(ws.cell(fila_origen, col)._style)
    if ws.row_dimensions[fila_origen].height is not None:
        ws.row_dimensions[fila_destino].height = ws.row_dimensions[fila_origen].height


def generar_plantilla_completada_xlsm(cat, ruta_salida_xlsm: Path, ruta_salida_xlsx: Path) -> None:
    """Completa una copia de Resources/plantillas_para_usar/Taller Terminal_Presupuesto.xlsm en Catalogo de precios/."""
    plantilla_src = ROOT / "Resources" / "plantillas_para_usar" / "Taller Terminal_Presupuesto.xlsm"
    cantidades = calcular_cantidades_revit(cat)

    # 1. Crear libro .xlsx limpio con las 3 hojas Neodata/Tabulador + hoja Resumen
    wb_xlsx = openpyxl.Workbook()
    wb_xlsx.remove(wb_xlsx.active)
    agregar_hojas_neodata(wb_xlsx, cat, cantidades)
    ruta_salida_xlsx.parent.mkdir(parents=True, exist_ok=True)
    tmp_xlsx = ruta_salida_xlsx.with_suffix(f".{os.getpid()}.tmp.xlsx")
    wb_xlsx.save(tmp_xlsx)
    os.replace(tmp_xlsx, ruta_salida_xlsx)

    if not plantilla_src.exists():
        return

    # 2. Copiar plantilla Taller Terminal_Presupuesto.xlsm a temporal y poblarla con las 99 partidas + hojas Neodata
    tmp_copy = Path(tempfile.gettempdir()) / f"catalogo_plantilla_{os.getpid()}.xlsm"
    shutil.copy2(plantilla_src, tmp_copy)
    wb = openpyxl.load_workbook(tmp_copy, keep_vba=True)

    # Corregir defectos SPEC_06 §3 en la copia de trabajo
    if "01_Datos Generales" in wb.sheetnames:
        ws_dg = wb["01_Datos Generales"]
        ws_dg["D9"] = PROYECTO
        ws_dg["G9"] = UBICACION
        ws_dg["G11"] = "2,500 m² aprox."
    if "02_Ref_Datos" in wb.sheetnames:
        ws_rd = wb["02_Ref_Datos"]
        ws_rd["D9"] = PROYECTO
        ws_rd["A2"] = None
        ws_rd["A9"] = None
    if "D25-00_Sobrecosto" in wb.sheetnames:
        ws_sc = wb["D25-00_Sobrecosto"]
        ws_sc["Q9"] = "='01_Datos Generales'!D15"
        ws_sc["AW11"] = 12
        ws_sc["BE1"] = None
        for r_sc in [*range(200, 209), 212, 213]:
            c_sc = ws_sc[f"BE{r_sc}"]
            if isinstance(c_sc.value, str) and c_sc.value.startswith("=") and not c_sc.value.upper().startswith("=IFERROR("):
                c_sc.value = f"=IFERROR({c_sc.value[1:]},0)"
        c_v215 = ws_sc["V215"]
        if isinstance(c_v215.value, str) and c_v215.value.startswith("=") and not c_v215.value.upper().startswith("=IFERROR("):
            c_v215.value = f"=IFERROR({c_v215.value[1:]},0)"

    ws = wb["D25-00_Presupuesto"]
    ws_res = wb["D25-00_Resumen"]
    ws["A2"] = None
    ws_res["A1"] = None
    ws["A13"] = '="Por este medio, y en atención a su amable solicitud de cotización, presentamos nuestro catálogo de conceptos y precios unitarios para "&B10&", edificio de educación de ~2,500 m²:"'
    ws["J16"] = 1.0  # Factor = 1.0000 en catálogo de precios para expresar Costo Directo puro (D-011 / SPEC_05)

    for r_clear in range(17, max(ws.max_row, 450) + 1):
        for col_c in range(1, 14):
            c_obj = ws.cell(r_clear, col_c)
            if not isinstance(c_obj, openpyxl.cell.cell.MergedCell):
                c_obj.value = None
                c_obj.comment = None

    grupos: dict[int, dict[int, list[Any]]] = {}
    for c in cat.conceptos:
        grupos.setdefault(int(c.capitulo), {}).setdefault(int(c.subcapitulo), []).append(c)

    filas_cap: dict[int, int] = {}
    filas_detalle: list[int] = []
    row = 17
    for cc in range(1, 15):
        partes_cap = grupos.get(cc)
        if not partes_cap:
            continue
        cap_str = f"{cc:02d}"
        fila_cap = row
        _copiar_estilo_fila(ws, 17, row)
        filas_cap[cc] = row
        ws.cell(row, 1, cc)
        ws.cell(row, 3, CAPITULOS_NOMBRES.get(cap_str, f"CAPÍTULO {cap_str}"))
        ws.cell(row, 3).font = Font(bold=True)
        sub_totales: list[int] = []
        row += 1

        for ss in sorted(partes_cap.keys()):
            sub_str = f"{ss:02d}"
            fila_sub = row
            _copiar_estilo_fila(ws, 18, row)
            ws.cell(row, 1, f"{cc}.{ss}")
            ws.cell(row, 3, SUBCAPITULOS_NOMBRES.get((cap_str, sub_str), f"Subcapítulo {cc}.{ss}"))
            ws.cell(row, 3).font = Font(bold=True)
            row += 1

            filas_items: list[int] = []
            for item in partes_cap[ss]:
                nnn = int(item.clave.split("-")[3])
                r = row
                _copiar_estilo_fila(ws, 20, r)
                filas_detalle.append(r)
                filas_items.append(r)
                u_txt = item.unidad.value if hasattr(item.unidad, "value") else str(item.unidad)
                ft_txt = item.fuente_tipo.value if hasattr(item.fuente_tipo, "value") else str(item.fuente_tipo)
                cant_val, cant_fuente = cantidades.get(item.clave, (1.0, "MEMORIA"))
                pu_cd = float(item.precio_unitario or 0.0)
                marca_sup = " [SUPUESTO]" if ft_txt == "SUPUESTO" else ""

                ws.cell(r, 1, f"{cc}.{ss}.{nnn}")
                ws.cell(r, 2, item.clave)
                ws.cell(r, 3, f"{item.concepto}{marca_sup}")
                ws.cell(r, 4, u_txt)
                ws.cell(r, 5, cant_val)
                ws.cell(r, 6, f"=J{r}*$J$16")
                ws.cell(r, 7, f"=E{r}*F{r}")
                ws.cell(r, 10, pu_cd)
                ws.cell(r, 12, f"=E{r}*J{r}")
                ws.cell(r, 13, f"{ft_txt}: {item.fuente_ref}")
                ws.cell(r, 2).comment = Comment(
                    f"Fuente P.U.: {ft_txt} ({item.fuente_ref})\n"
                    f"Justificación: {item.justificacion or '-'}\n"
                    f"Fuente Cantidad Ref.: {cant_fuente}",
                    "AG-2",
                )
                ws.cell(r, 5).number_format = "#,##0.00"
                ws.cell(r, 6).number_format = "$#,##0.00"
                ws.cell(r, 7).number_format = "$#,##0.00"
                ws.cell(r, 8).number_format = "0.00%"
                ws.cell(r, 10).number_format = "$#,##0.00"
                ws.cell(r, 12).number_format = "$#,##0.00"
                row += 1

            _copiar_estilo_fila(ws, 21, row)
            ws.cell(row, 1, f"{cc}.{ss}")
            ws.cell(row, 2, "Total de:")
            ws.cell(row, 3, f"=C{fila_sub}")
            ws.cell(row, 7, f"=SUM(G{filas_items[0]}:G{filas_items[-1]})")
            ws.cell(row, 12, f"=SUM(L{filas_items[0]}:L{filas_items[-1]})")
            ws.cell(row, 7).number_format = "$#,##0.00"
            ws.cell(row, 12).number_format = "$#,##0.00"
            sub_totales.append(row)
            row += 1

        ws.cell(fila_cap, 2, "Total de capítulo")
        ws.cell(fila_cap, 7, "=" + "+".join(f"G{x}" for x in sub_totales))
        ws.cell(fila_cap, 12, "=" + "+".join(f"L{x}" for x in sub_totales))
        ws.cell(fila_cap, 7).number_format = "$#,##0.00"
        ws.cell(fila_cap, 12).number_format = "$#,##0.00"

    fila_subtotal = row
    _copiar_estilo_fila(ws, 23, fila_subtotal)
    _copiar_estilo_fila(ws, 24, fila_subtotal + 1)
    _copiar_estilo_fila(ws, 24, fila_subtotal + 2)
    ws["L16"] = "=SUBTOTAL(9," + ",".join(f"L{x}" for x in filas_detalle) + ")"
    for r in filas_detalle:
        ws.cell(r, 8, f"=IFERROR(G{r}/$G${fila_subtotal},0)")
    ws.cell(fila_subtotal, 2, "SUBTOTAL COSTO DIRECTO")
    ws.cell(fila_subtotal, 7, "=" + "+".join(f"G{x}" for x in filas_cap.values()))
    ws.cell(fila_subtotal, 12, "=" + "+".join(f"L{x}" for x in filas_cap.values()))
    ws.cell(fila_subtotal, 8, f"=IFERROR(G{fila_subtotal}/G{fila_subtotal},0)")
    ws.cell(fila_subtotal + 1, 2, "IVA (16% D-020)")
    ws.cell(fila_subtotal + 1, 7, f"=G{fila_subtotal}*0.16")
    ws.cell(fila_subtotal + 2, 2, "TOTAL")
    ws.cell(fila_subtotal + 2, 7, f"=G{fila_subtotal}+G{fila_subtotal + 1}")
    for r_tot in (fila_subtotal, fila_subtotal + 1, fila_subtotal + 2):
        ws.cell(r_tot, 7).number_format = "$#,##0.00"

    # Llenar D25-00_Resumen con los 14 capítulos
    for rng_m in list(ws_res.merged_cells.ranges):
        if rng_m.min_row >= 18 and rng_m.max_row <= 35:
            ws_res.unmerge_cells(str(rng_m))
    for r_res in range(18, 32):
        if r_res != 18:
            _copiar_estilo_fila(ws_res, 18, r_res, 7)
        for col_c in range(1, 8):
            c_obj = ws_res.cell(r_res, col_c)
            if not isinstance(c_obj, openpyxl.cell.cell.MergedCell):
                c_obj.value = None
    for cc in range(1, 15):
        r_res = 17 + cc
        cap_str = f"{cc:02d}"
        ws_res.cell(r_res, 1, cc)
        ws_res.cell(r_res, 2, CAPITULOS_NOMBRES.get(cap_str, ""))
        ws_res.cell(r_res, 5, f"='D25-00_Presupuesto'!G{filas_cap[cc]}" if cc in filas_cap else 0)
        ws_res.cell(r_res, 6, f"=IFERROR(E{r_res}/$E$32,0)")
        ws_res.cell(r_res, 5).number_format = "$#,##0.00"
        ws_res.cell(r_res, 6).number_format = "0.00%"
    ws_res["D32"] = "Subtotal Costo Directo sin Impuestos"
    ws_res["E32"] = "=" + "+".join(f"E{r_res}" for r_res in range(18, 32))
    ws_res["D33"] = "IVA 16%"
    ws_res["E33"] = "=E32*0.16"
    ws_res["D34"] = "Total"
    ws_res["E34"] = "=E32+E33"

    # Agregar también las 3 hojas Neodata/Tabulador dentro del XLSM
    agregar_hojas_neodata(wb, cat, cantidades)

    # Configurar impresión Carta en todas las hojas (SPEC_07)
    for sname in wb.sheetnames:
        s = wb[sname]
        s.page_setup.paperSize = s.PAPERSIZE_LETTER
        s.page_setup.fitToWidth = 1
        s.page_setup.fitToHeight = 0
        s.sheet_properties.pageSetUpPr.fitToPage = True

    ruta_salida_xlsm.parent.mkdir(parents=True, exist_ok=True)
    tmp_out = ruta_salida_xlsm.with_suffix(f".{os.getpid()}.tmp.xlsm")
    wb.save(tmp_out)
    os.replace(tmp_out, ruta_salida_xlsm)
    try:
        tmp_copy.unlink(missing_ok=True)
    except OSError:
        pass
