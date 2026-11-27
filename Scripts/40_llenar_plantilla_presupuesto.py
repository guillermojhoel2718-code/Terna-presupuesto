"""CX-1: preparar plantilla y generar presupuesto desde Generadores + AG-2.

Entrada: Resources/plantillas_para_usar/Taller Terminal_Presupuesto.xlsm,
         _harness/intermedios/generadores/generadores_vNN.json,
         _harness/intermedios/precios/catalogo_vNN.json.
Salida: Presupuesto/Presupuesto_vNN.xlsm y
        _harness/intermedios/presupuesto/presupuesto_vNN.json.
Dependencias: openpyxl, pydantic>=2, Excel de escritorio (PowerShell COM).
Fecha: 26-11-2026
Uso: py Scripts/40_llenar_plantilla_presupuesto.py --prepare-template
     py Scripts/40_llenar_plantilla_presupuesto.py --version v01
     py Scripts/40_llenar_plantilla_presupuesto.py --test-only
"""
from __future__ import annotations

import argparse
import json
import math
import posixpath
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.page import PageMargins
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Scripts" / "schemas"))
from generadores import Generadores  # noqa: E402
from precios import CatalogoPrecios  # noqa: E402
from presupuesto import Presupuesto  # noqa: E402

PROJECT = 'Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"'
CHAPTERS = {
    "01": "Preliminares",
    "02": "Cimentación",
    "03": "Estructura de concreto y mampostería confinada",
    "04": "Estructura metálica y cubierta",
    "05": "Albañilería",
    "06": "Acabados",
    "07": "Herrería y cancelería",
    "08": "Instalación hidráulica y pluvial",
    "09": "Instalación sanitaria",
    "10": "Instalación eléctrica y fotovoltaica",
    "11": "Voz y datos — fuera de alcance",
    "12": "CCTV y seguridad — fuera de alcance",
    "13": "Mobiliario y equipamiento fijo",
    "14": "Limpieza final y entrega",
}
SHEETS = {
    "general": "01_Datos Generales",
    "resumen": "D25-00_Resumen",
    "budget": "D25-00_Presupuesto",
    "overhead": "D25-00_Sobrecosto",
    "reference": "02_Ref_Datos",
}


def atomic_save_workbook(workbook, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.stem + ".tmp" + target.suffix)
    workbook.save(temporary)
    temporary.replace(target)


def configure_print(ws, area: str, title_rows: str, orientation: str, version: str = "v00") -> None:
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_setup.orientation = orientation
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = area
    ws.print_title_rows = title_rows
    ws.page_margins = PageMargins(left=0.5, right=0.5, top=0.75, bottom=0.75,
                                  header=0.3, footer=0.3)
    ws.oddHeader.center.text = PROJECT
    ws.oddHeader.right.text = f"Versión {version} · &D"
    ws.oddFooter.left.text = "Responsable: CX-1"
    ws.oddFooter.right.text = "Página &P de &N"


def prepare_template(source: Path, target: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"No existe la plantilla fuente: {source}")
    wb = load_workbook(source, keep_vba=True, data_only=False, keep_links=True)
    for sheet in SHEETS.values():
        if sheet not in wb.sheetnames:
            raise ValueError(f"La plantilla no contiene la hoja {sheet!r}")
    general = wb[SHEETS["general"]]
    general["D9"] = PROJECT
    general["G11"] = "2,500 m² aprox."
    general["G7"] = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    general["G7"].number_format = "DD-MM-YYYY"
    # El cliente puede completarse después; la fórmula del sobrecosto apunta a D15.
    ref = wb[SHEETS["reference"]]
    ref["D9"] = PROJECT
    overhead = wb[SHEETS["overhead"]]
    overhead["Q9"] = "='01_Datos Generales'!D15"
    overhead["AW11"] = 12

    budget = wb[SHEETS["budget"]]
    budget["A13"] = "=B10"
    summary = wb[SHEETS["resumen"]]
    # The source has merged callout bands in rows 25–26; those rows become
    # ordinary chapter lines in the 14-chapter summary.
    for merged in list(summary.merged_cells.ranges):
        if merged.min_row <= 31 and merged.max_row >= 18 and merged.min_col <= 6 and merged.max_col >= 1:
            if merged.min_row >= 25 or merged.max_row >= 25:
                summary.unmerge_cells(str(merged))
    for n in range(1, 15):
        row = 17 + n
        _copy_row_style(summary, row, 18, max_col=7)
        summary.cell(row, 1, n)
        summary.cell(row, 2, CHAPTERS[f"{n:02d}"])
        summary.cell(row, 5, 0)
        summary.cell(row, 6, f"=IFERROR(E{row}/$E$32,0)")
    summary["D32"] = "Subtotal del Presupuesto mostrado sin Impuestos"
    summary["E32"] = "=SUM(E18:E31)"
    summary["D33"] = "IVA"
    summary["E33"] = "=E32*0.16"
    summary["D34"] = "Total"
    summary["E34"] = "=E32+E33"
    summary.print_area = "A1:G34"

    for ws in wb.worksheets:
        orientation = "landscape" if ws.title == SHEETS["overhead"] else "portrait"
        if ws.title == SHEETS["general"]:
            area, titles = "A1:G21", "1:7"
        elif ws.title == SHEETS["resumen"]:
            area, titles = "A1:G34", "1:17"
        elif ws.title == SHEETS["budget"]:
            area, titles = "A1:I27", "1:16"
        elif ws.title == SHEETS["overhead"]:
            area, titles = "A1:BE223", "1:8"
        else:
            area, titles = "A1:G30", "1:7"
        configure_print(ws, area, titles, orientation, "v00")
    atomic_save_workbook(wb, target)
    wb.close()


def newest_json(folder: Path, stem: str) -> Path:
    matches = sorted(folder.glob(f"{stem}_v*.json"))
    if not matches:
        raise FileNotFoundError(f"No se encontró {stem}_vNN.json en {folder}")
    return matches[-1]


def load_models(generators_path: Path, catalog_path: Path):
    generators = Generadores.model_validate_json(generators_path.read_text(encoding="utf-8-sig"))
    catalog = CatalogoPrecios.model_validate_json(catalog_path.read_text(encoding="utf-8-sig"))
    catalog_by_key = {item.clave: item for item in catalog.conceptos}
    items = []
    excluded = set(generators.claves_sin_cantidad)
    for generator in generators.generadores:
        if generator.clave in excluded or generator.cantidad_total <= 0:
            excluded.add(generator.clave)
            continue
        price = catalog_by_key.get(generator.clave)
        if price is None:
            raise ValueError(f"Generadores incluye {generator.clave}, ausente del catálogo AG-2")
        if price.precio_unitario is None:
            raise ValueError(f"{generator.clave}: AG-2 no asignó costo directo")
        if price.unidad != generator.unidad:
            raise ValueError(f"{generator.clave}: unidad distinta en Generadores y AG-2")
        chapter, subchapter, code = generator.clave.split("-")[1:]
        source = (f"Cantidad: {generator.fuente} | Precio: {price.fuente_tipo.value}: "
                  f"{price.fuente_ref}")
        items.append({
            "clave": generator.clave,
            "capitulo": chapter,
            "subcapitulo": subchapter,
            "numero_concepto": code,
            "concepto": price.concepto,
            "unidad": price.unidad.value,
            "cantidad": generator.cantidad_total,
            "precio_unitario_cd": float(price.precio_unitario),
            "fuente": source,
        })
    return generators, catalog, items, sorted(excluded)


def _copy_row_style(ws, target_row: int, source_row: int, max_col: int = 12) -> None:
    from copy import copy
    if target_row == source_row:
        return
    for col in range(1, max_col + 1):
        src, dst = ws.cell(source_row, col), ws.cell(target_row, col)
        if src.has_style:
            dst._style = copy(src._style)
        if src.number_format:
            dst.number_format = src.number_format
        if src.alignment:
            dst.alignment = copy(src.alignment)
        if src.protection:
            dst.protection = copy(src.protection)
    ws.row_dimensions[target_row].height = ws.row_dimensions[source_row].height


def _clear_value_area(ws, start_row: int, end_row: int, max_col: int = 12) -> None:
    for row in range(start_row, end_row + 1):
        for col in range(1, max_col + 1):
            ws.cell(row, col).value = None
            ws.cell(row, col).comment = None


def _iva_rate_from_formula(ws) -> float:
    # La tasa se toma de la fórmula de IVA que trae la plantilla.
    candidates = [ws["E33"].value, ws["G25"].value, ws["G33"].value]
    for formula in candidates:
        if isinstance(formula, str):
            match = re.search(r"\*\s*(0?\.\d+)", formula)
            if match:
                return float(match.group(1))
    raise ValueError("No se pudo leer la tasa de IVA de la fórmula de la plantilla")


def fill_workbook(base: Path, output: Path, items: list[dict[str, Any]], version: str,
                  date_text: str, excluded_keys: list[str] | None = None) -> tuple[float, float]:
    wb = load_workbook(base, keep_vba=True, data_only=False, keep_links=True)
    ws = wb[SHEETS["budget"]]
    summary = wb[SHEETS["resumen"]]
    chapter_groups: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for item in items:
        chapter_groups[item["capitulo"]][item["subcapitulo"]].append(item)
    for group in chapter_groups.values():
        for concepts in group.values():
            concepts.sort(key=lambda x: x["clave"])
    end_clean = max(ws.max_row, 350)
    _clear_value_area(ws, 17, end_clean)
    chapter_rows: dict[str, int] = {}
    current = 17
    item_rows = []
    for chapter in sorted(chapter_groups):
        chapter_name = CHAPTERS.get(chapter, f"Capítulo {chapter}")
        chapter_row = current
        _copy_row_style(ws, chapter_row, 17)
        ws.cell(chapter_row, 1, int(chapter))
        ws.cell(chapter_row, 2, "Total de capítulo")
        ws.cell(chapter_row, 3, chapter_name)
        chapter_rows[chapter] = chapter_row
        current += 1
        subchapter_total_rows = []
        for subchapter in sorted(chapter_groups[chapter]):
            concepts = chapter_groups[chapter][subchapter]
            sub_row = current
            _copy_row_style(ws, sub_row, 18)
            ws.cell(sub_row, 1, f"{int(chapter)}.{int(subchapter)}")
            ws.cell(sub_row, 3, f"{subchapter} Subcapítulo {subchapter}")
            current += 1
            first_item_row = current
            for index, item in enumerate(concepts, start=1):
                row = current
                _copy_row_style(ws, row, 19)
                ws.cell(row, 1, f"{int(chapter)}.{int(subchapter)}.{index}")
                ws.cell(row, 2, item["clave"])
                ws.cell(row, 3, item["concepto"])
                ws.cell(row, 4, item["unidad"])
                ws.cell(row, 5, item["cantidad"])
                ws.cell(row, 6, f"=J{row}*$J$16")
                ws.cell(row, 7, f"=E{row}*F{row}")
                ws.cell(row, 9, item["fuente"])
                ws.cell(row, 10, item["precio_unitario_cd"])
                ws.cell(row, 12, f"=E{row}*J{row}")
                ws.cell(row, 3).alignment = Alignment(vertical="top", wrap_text=True)
                ws.cell(row, 9).alignment = Alignment(vertical="top", wrap_text=True)
                ws.cell(row, 9).font = Font(name=ws.cell(row, 3).font.name or "Arial", size=8)
                ws.cell(row, 5).number_format = "#,##0.00"
                for col in (6, 7, 10, 12):
                    ws.cell(row, col).number_format = '$#,##0.00'
                item_rows.append(row)
                current += 1
            last_item_row = current - 1
            subtotal_row = current
            _copy_row_style(ws, subtotal_row, 20)
            ws.cell(subtotal_row, 1, f"{int(chapter)}.{int(subchapter)}")
            ws.cell(subtotal_row, 2, "Total de:")
            ws.cell(subtotal_row, 3, f"=C{sub_row}")
            ws.cell(subtotal_row, 7, f"=SUM(G{first_item_row}:G{last_item_row})")
            ws.cell(subtotal_row, 12, f"=SUM(L{first_item_row}:L{last_item_row})")
            subchapter_total_rows.append(subtotal_row)
            current += 1
        _copy_row_style(ws, chapter_row, 17)
        ws.cell(chapter_row, 7, "=" + "+".join(f"G{r}" for r in subchapter_total_rows))
        ws.cell(chapter_row, 8, f"=IFERROR(G{chapter_row}/$G${current},0)")
        ws.cell(chapter_row, 12, "=" + "+".join(f"L{r}" for r in subchapter_total_rows))

    subtotal_row, iva_row, total_row, text_row = current, current + 1, current + 2, current + 3
    for row, source in ((subtotal_row, 24), (iva_row, 25), (total_row, 26), (text_row, 27)):
        _copy_row_style(ws, row, source)
    ws.cell(subtotal_row, 2, "SUBTOTAL")
    ws.cell(subtotal_row, 7, "=" + "+".join(f"G{r}" for r in chapter_rows.values()) if chapter_rows else "=0")
    ws.cell(subtotal_row, 12, "=" + "+".join(f"L{r}" for r in chapter_rows.values()) if chapter_rows else "=0")
    ws["L16"] = f"=L{subtotal_row}"
    for row in item_rows:
        ws.cell(row, 8, f"=IFERROR(G{row}/$G${subtotal_row},0)")
    for row in chapter_rows.values():
        ws.cell(row, 8, f"=IFERROR(G{row}/$G${subtotal_row},0)")
    ws.cell(iva_row, 2, "IVA")
    iva_rate = _iva_rate_from_formula(wb[SHEETS["resumen"]])
    ws.cell(iva_row, 7, f"=G{subtotal_row}*{iva_rate}")
    ws.cell(total_row, 2, "TOTAL")
    ws.cell(total_row, 7, f"=G{subtotal_row}+G{iva_row}")
    ws.cell(text_row, 8, "Importes sujetos al IVA correspondiente")
    ws["A13"] = "=B10"
    ws["B10"] = f"='{SHEETS['general']}'!D9"
    general = wb[SHEETS["general"]]
    general["G7"] = datetime.strptime(date_text, "%d-%m-%Y")
    general["G7"].number_format = "DD-MM-YYYY"
    ws["J16"] = 1.0
    ws["I16"] = "Fuente"
    ws.column_dimensions["I"].width = 42
    ws.print_area = f"A1:I{text_row}"
    ws.print_title_rows = "1:16"
    ws.sheet_view.showGridLines = False

    excluded_note = (f" Claves sin cantidad omitidas: {', '.join(excluded_keys)}." if excluded_keys else "")
    summary["A12"] = (f'Presupuesto de obra para {PROJECT}. '
                      f"Versión {version} · {date_text} · Responsable: CX-1.{excluded_note}")
    for n in range(1, 15):
        row = 17 + n
        _copy_row_style(summary, row, 18, max_col=7)
        chapter = f"{n:02d}"
        summary.cell(row, 1, n)
        summary.cell(row, 2, CHAPTERS[chapter])
        summary.cell(row, 5, f"='{SHEETS['budget']}'!G{chapter_rows[chapter]}" if chapter in chapter_rows else 0)
        summary.cell(row, 6, f"=IFERROR(E{row}/$E$32,0)")
    for row, style_source in ((32, 22), (33, 23), (34, 24)):
        _copy_row_style(summary, row, style_source, max_col=7)
    summary["D32"] = "Subtotal del Presupuesto mostrado sin Impuestos"
    summary["E32"] = "=SUM(E18:E31)"
    summary["D33"] = "IVA"
    summary["E33"] = f"=E32*{iva_rate}"
    summary["D34"] = "Total"
    summary["E34"] = "=E32+E33"
    summary.print_area = "A1:G34"
    for sheet in wb.worksheets:
        orientation = "landscape" if sheet.title == SHEETS["overhead"] else "portrait"
        if sheet.title == SHEETS["budget"]:
            area, titles = f"A1:I{text_row}", "1:16"
        elif sheet.title == SHEETS["resumen"]:
            area, titles = "A1:G34", "1:17"
        elif sheet.title == SHEETS["overhead"]:
            area, titles = "A1:BE223", "1:8"
        elif sheet.title == SHEETS["general"]:
            area, titles = "A1:G21", "1:7"
        else:
            area, titles = "A1:G30", "1:7"
        configure_print(sheet, area, titles, orientation, version)
    atomic_save_workbook(wb, output)
    wb.close()
    return iva_rate, float(subtotal_row)


def recalculate_with_excel(path: Path) -> dict[str, Any]:
    helper = ROOT / "Scripts" / "41_recalcular_presupuesto.ps1"
    completed = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(helper),
         "-Workbook", str(path)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if completed.returncode:
        raise RuntimeError(f"Excel COM falló ({completed.returncode}): {completed.stderr.strip()}")
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip().startswith("{")]
    if not lines:
        raise RuntimeError(f"Excel COM no devolvió datos: {completed.stdout} {completed.stderr}")
    return json.loads(lines[-1])


def set_overcost_factor(path: Path, factor: float) -> None:
    wb = load_workbook(path, keep_vba=True, data_only=False, keep_links=True)
    wb[SHEETS["budget"]]["J16"] = factor
    atomic_save_workbook(wb, path)
    wb.close()


def restore_print_setup_after_excel(path: Path) -> None:
    """Excel can serialize default Letter/fit settings as omitted attributes.

    Restore the explicit SPEC_07 OOXML attributes after COM has calculated and
    saved formulas. The ZIP parts and cached formula values otherwise remain
    untouched.
    """
    main_ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    package_rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    setup_re = re.compile(rb"<pageSetup\b([^>]*)/>")
    fit_re = re.compile(rb"<pageSetUpPr\b([^>]*)/>")
    attr_re = re.compile(rb"([A-Za-z_:][\w:.-]*)=(['\"])(.*?)\2")

    with zipfile.ZipFile(path, "r") as source:
        workbook_xml = ET.fromstring(source.read("xl/workbook.xml"))
        rels_xml = ET.fromstring(source.read("xl/_rels/workbook.xml.rels"))
        rels = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels_xml.findall(f"{{{package_rel_ns}}}Relationship")}
        sheet_orientation = {}
        for sheet in workbook_xml.find(f"{{{main_ns}}}sheets"):
            target = rels[sheet.attrib[f"{{{rel_ns}}}id"]]
            sheet_path = (posixpath.normpath(target.lstrip("/")) if target.startswith("/")
                          else posixpath.normpath(posixpath.join("xl", target)))
            sheet_orientation[sheet_path] = "landscape" if sheet.attrib["name"] == SHEETS["overhead"] else "portrait"
        files = [(item, source.read(item.filename)) for item in source.infolist()]

    updated = []
    for info, data in files:
        orientation = sheet_orientation.get(info.filename)
        if orientation:
            def setup_repl(match: re.Match[bytes]) -> bytes:
                attrs = {m.group(1): m.group(3) for m in attr_re.finditer(match.group(1))}
                for key in (b"scale", b"paperSize", b"fitToWidth", b"fitToHeight", b"orientation"):
                    attrs.pop(key, None)
                attrs.update({b"paperSize": b"1", b"fitToWidth": b"1", b"fitToHeight": b"0",
                              b"orientation": orientation.encode("ascii")})
                serialized = b" ".join(k + b"=\"" + v + b"\"" for k, v in attrs.items())
                return b"<pageSetup " + serialized + b"/>"

            def fit_repl(match: re.Match[bytes]) -> bytes:
                attrs = {m.group(1): m.group(3) for m in attr_re.finditer(match.group(1))}
                attrs[b"fitToPage"] = b"1"
                serialized = b" ".join(k + b"=\"" + v + b"\"" for k, v in attrs.items())
                return b"<pageSetUpPr " + serialized + b"/>"

            data = setup_re.sub(setup_repl, data, count=1)
            data = fit_re.sub(fit_repl, data, count=1)
        updated.append((info, data))

    temporary = path.with_name(path.stem + ".print.tmp" + path.suffix)
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as target:
        for info, data in updated:
            target.writestr(info, data)
    temporary.replace(path)


def apply_overcost(path: Path, tolerance: float = 0.0001, max_iterations: int = 20):
    factor = 1.0
    cells = {}
    for iteration in range(1, max_iterations + 1):
        set_overcost_factor(path, factor)
        cells = recalculate_with_excel(path)
        direct = float(cells["AW5"])
        sale = float(cells["AW215"])
        if direct <= 0:
            raise ValueError(f"Costo directo no positivo (AW5={direct}); no se puede obtener factor")
        next_factor = sale / direct
        if not math.isfinite(next_factor) or next_factor <= 0:
            raise ValueError(f"Factor inválido calculado por la hoja: {next_factor}")
        if abs(next_factor - factor) < tolerance:
            factor = next_factor
            set_overcost_factor(path, factor)
            cells = recalculate_with_excel(path)
            restore_print_setup_after_excel(path)
            return factor, cells, iteration
        factor = next_factor
    raise RuntimeError(f"El factor no convergió en {max_iterations} iteraciones; último={factor}")


def export_json(path: Path, output_path: Path, version: str, date_text: str,
                generators_path: Path, catalog_path: Path, items: list[dict[str, Any]],
                factor: float, cells: dict[str, Any], excluded_keys: list[str] | None = None) -> dict[str, Any]:
    partidas = []
    for item in items:
        pu = item["precio_unitario_cd"] * factor
        partidas.append({
            "clave": item["clave"], "capitulo": item["capitulo"],
            "subcapitulo": item["subcapitulo"], "concepto": item["concepto"],
            "unidad": item["unidad"], "cantidad": item["cantidad"],
            "precio_unitario": pu, "precio_unitario_cd": item["precio_unitario_cd"],
            "importe": item["cantidad"] * pu, "fuente": item["fuente"],
        })
    subtotal = sum(p["importe"] for p in partidas)
    iva = float(cells["IVA"])
    total = float(cells["TOTAL"])
    over = {
        "periodo_meses": 12,
        "costo_directo": float(cells["AW5"]),
        "indirectos": float(cells["AD200"]),
        "financiamiento": float(cells["AD209"]),
        "utilidad": float(cells["AD210"]),
        "cargos_adicionales": float(cells["AD211"]),
        "precio_venta_sin_iva": float(cells["AW215"]),
        "factor_sobrecosto": factor,
        "iva_tasa": iva / subtotal if subtotal else 0.0,
        "celdas_origen": {
            "periodo_meses": "D25-00_Sobrecosto!AW11",
            "indirectos": "D25-00_Sobrecosto!AD200",
            "financiamiento": "D25-00_Sobrecosto!AD209",
            "utilidad": "D25-00_Sobrecosto!AD210",
            "cargos_adicionales": "D25-00_Sobrecosto!AD211",
            "precio_venta_sin_iva": "D25-00_Sobrecosto!AW215",
            "costo_directo": "D25-00_Sobrecosto!AW5",
            "factor_financiamiento": "D25-00_Sobrecosto!BE209",
            "factor_utilidad": "D25-00_Sobrecosto!BE210",
            "factor_cargos": "D25-00_Sobrecosto!BE211",
            "factor_sobrecosto": "D25-00_Sobrecosto!AW215 / AW5",
            "iva_tasa": "D25-00_Resumen!E33 / E32 (fórmula de plantilla: E33=E32*0.16)",
        },
    }
    data = {
        "version": version, "fecha": date_text,
        "generadores_usados": (generators_path.relative_to(ROOT).as_posix()
                               + (f" | claves sin cantidad omitidas: {', '.join(excluded_keys)}" if excluded_keys else "")),
        "catalogo_usado": catalog_path.relative_to(ROOT).as_posix(),
        "partidas": partidas, "sobrecosto": over,
        "subtotal": subtotal, "iva": iva, "total": total,
    }
    Presupuesto.model_validate(data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp = output_path.with_suffix(output_path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(output_path)
    return data


def write_test_inputs(test_json: Path, work_dir: Path):
    """Crear modelos de prueba a partir del fixture sintético ya marcado."""
    raw = json.loads(test_json.read_text(encoding="utf-8-sig"))
    if "DATOS SINTÉTICOS MARCADOS" not in raw.get("generadores_usados", ""):
        raise ValueError("El fixture no está identificado como datos sintéticos de T-402")
    gs = {
        "version": "v00", "fecha": raw["fecha"], "catalogo_usado": "DATOS SINTÉTICOS MARCADOS · prueba T-402",
        "generadores": [], "claves_sin_cantidad": [],
    }
    cs = {"version": "v00", "fecha": raw["fecha"], "alcance": "DATOS SINTÉTICOS MARCADOS · prueba T-402",
          "conceptos": [], "resumen": {"total_conceptos": 0, "con_precio": 0, "sin_precio": [], "supuestos": []}}
    for p in raw["partidas"]:
        chapter, subchapter, code = p["clave"].split("-")[1:]
        gs["generadores"].append({
            "clave": p["clave"], "concepto": p["concepto"], "unidad": p["unidad"],
            "formula": "DATOS SINTÉTICOS MARCADOS · solo prueba T-402",
            "renglones": [{"parcial": p["cantidad"], "modelo_origen": "DATOS SINTÉTICOS MARCADOS"}],
            "cantidad_total": p["cantidad"], "fuente": "SUPUESTO:DATOS SINTÉTICOS MARCADOS · prueba T-402",
        })
        cs["conceptos"].append({
            "clave": p["clave"], "capitulo": chapter, "subcapitulo": subchapter,
            "concepto": p["concepto"], "unidad": p["unidad"],
            "precio_unitario": p["precio_unitario_cd"], "fuente_tipo": "SUPUESTO",
            "fuente_ref": "DATOS SINTÉTICOS MARCADOS · prueba T-402",
            "fecha_fuente": raw["fecha"], "justificacion": "Datos sintéticos para probar CX-1; no usar en obra",
            "apu": [], "mapeo_revit": [], "sin_cantidad_revit": False,
        })
    cs["resumen"].update(total_conceptos=len(cs["conceptos"]), con_precio=len(cs["conceptos"]))
    generators = Generadores.model_validate(gs)
    catalog = CatalogoPrecios.model_validate(cs)
    items = []
    catalog_by_key = {c.clave: c for c in catalog.conceptos}
    for g in generators.generadores:
        price = catalog_by_key[g.clave]
        chapter, subchapter, code = g.clave.split("-")[1:]
        items.append({"clave": g.clave, "capitulo": chapter, "subcapitulo": subchapter,
                      "numero_concepto": code, "concepto": price.concepto,
                      "unidad": price.unidad.value, "cantidad": g.cantidad_total,
                      "precio_unitario_cd": price.precio_unitario,
                      "fuente": "Cantidad: SUPUESTO:DATOS SINTÉTICOS MARCADOS | Precio: SUPUESTO: DATOS SINTÉTICOS MARCADOS"})
    return generators, catalog, items, []


def ensure_approved_inputs(root: Path, generators_path: Path, catalog_path: Path) -> None:
    queue = (root / "_harness" / "cola.md").read_text(encoding="utf-8-sig")
    ag2 = (root / "_harness" / "status" / "AG-2.md").read_text(encoding="utf-8-sig")
    cl1 = (root / "_harness" / "status" / "CL-1.md").read_text(encoding="utf-8-sig")
    def queue_state(task_id: str) -> str | None:
        for line in queue.splitlines():
            if re.search(rf"\b{task_id}\b", line):
                match = re.search(r"estado:\s*([^|]+)", line, re.IGNORECASE)
                return match.group(1).strip().lower() if match else None
        return None

    def status_state(status_text: str, task_id: str) -> str | None:
        for line in status_text.splitlines():
            if re.match(rf"^\|\s*{re.escape(task_id)}\s*\|", line):
                cells = [part.strip().lower() for part in line.strip().strip("|").split("|")]
                return cells[1] if len(cells) > 1 else None
        return None

    gen_version = re.search(r"v(\d{2})", generators_path.stem)
    cat_version = re.search(r"v(\d{2})", catalog_path.stem)
    if not gen_version or not cat_version:
        raise RuntimeError("No se pudo identificar la versión de los intermedios")
    gen_tasks = ["T-302", "T-303", "T-304"]
    cat_task = "T-205" if cat_version.group(1) == "01" else "T-206"
    required = gen_tasks + [cat_task]
    pending = [task for task in required if queue_state(task) != "aprobada"]
    if pending:
        raise RuntimeError(f"T-403 bloqueada: cola.md no aprueba las dependencias {', '.join(pending)}")
    for label, state in ((f"AG-2/{cat_task}", status_state(ag2, cat_task)),
                         ("CL-1/T-304", status_state(cl1, "T-304"))):
        if state not in ("lista para revisión", "aprobada"):
            raise RuntimeError(f"T-403 bloqueada: status {label} aún no confirma el intermedio ({state})")
    for path in (generators_path, catalog_path):
        age = datetime.now().timestamp() - path.stat().st_mtime
        if age < 60:
            raise RuntimeError(f"Intermedio cambió hace menos de un minuto: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-template", action="store_true")
    parser.add_argument("--version", default="v01")
    parser.add_argument("--test-only", action="store_true")
    parser.add_argument("--generadores", type=Path)
    parser.add_argument("--catalogo", type=Path)
    parser.add_argument("--plantilla", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    template_copy = ROOT / "Presupuesto" / "_plantilla_trabajo.xlsm"
    base = ROOT / "Presupuesto" / "Presupuesto_v00_base.xlsm"
    if args.prepare_template:
        source = args.plantilla or (ROOT / "Resources" / "plantillas_para_usar" / "Taller Terminal_Presupuesto.xlsm")
        if not source.exists():
            source = template_copy
        prepare_template(source, base)
        print(f"Plantilla corregida: {base.relative_to(ROOT)}")
        return 0
    today = date.today().strftime("%d-%m-%Y")
    if args.test_only:
        test_xlsm = ROOT / "Presupuesto" / "Presupuesto_v00_prueba.xlsm"
        test_json = ROOT / "Presupuesto" / "Presupuesto_v00_prueba.json"
        if not test_xlsm.is_file() or not test_json.is_file():
            raise FileNotFoundError("Faltan Presupuesto_v00_prueba.xlsm/.json")
        if not base.is_file():
            raise FileNotFoundError("Ejecuta primero --prepare-template")
        fixture = load_workbook(test_xlsm, keep_vba=True, data_only=False, keep_links=True)
        fixture_budget = fixture[SHEETS["budget"]]
        fixture_keys = {fixture_budget.cell(row, 2).value for row in range(17, fixture_budget.max_row + 1)}
        fixture_data = json.loads(test_json.read_text(encoding="utf-8-sig"))
        expected_keys = {p["clave"] for p in fixture_data["partidas"]}
        if not expected_keys.issubset(fixture_keys) or fixture[SHEETS["overhead"]]["AW11"].value != 12:
            fixture.close()
            raise ValueError("El libro de prueba no corresponde al fixture T-402 esperado")
        fixture.close()
        generators, catalog, items, excluded_keys = write_test_inputs(test_json, ROOT / "Presupuesto")
        generator_path, catalog_path = test_json, test_json
        version = "v00"
        output = ROOT / "Presupuesto" / "_T402_salida_temporal.xlsm"
        json_output = ROOT / "Presupuesto" / "_T402_intermedio_temporal.json"
    else:
        generators_path = args.generadores or newest_json(ROOT / "_harness" / "intermedios" / "generadores", "generadores")
        catalog_path = args.catalogo or newest_json(ROOT / "_harness" / "intermedios" / "precios", "catalogo")
        generators_path, catalog_path = generators_path.resolve(), catalog_path.resolve()
        ensure_approved_inputs(ROOT, generators_path, catalog_path)
        generators, catalog, items, excluded_keys = load_models(generators_path, catalog_path)
        generator_path, version = generators_path, args.version
        output = args.output or ROOT / "Presupuesto" / f"Presupuesto_{version}.xlsm"
        json_output = ROOT / "_harness" / "intermedios" / "presupuesto" / f"presupuesto_{version}.json"
        if output.exists() or json_output.exists():
            queue = (ROOT / "_harness" / "cola.md").read_text(encoding="utf-8-sig")
            task_line = next((line for line in queue.splitlines() if re.match(r"^\s*- \[[ xX]\] T-403\b", line)), "")
            task_state = re.search(r"estado:\s*([^|]+)", task_line, re.IGNORECASE)
            if task_state and task_state.group(1).strip().lower() == "aprobada":
                raise RuntimeError(f"T-{version} ya está aprobado; no se sobrescribe. Usa la siguiente versión.")
    date_text = today if not args.test_only else "23-11-2026"
    fill_workbook(base, output, items, version, date_text, excluded_keys)
    factor, cells, iterations = apply_overcost(output)
    data = export_json(output, json_output, version, date_text, generator_path, catalog_path,
                       items, factor, cells, excluded_keys)
    if args.test_only:
        # El fixture se conserva; la salida temporal permanece para revisión reproducible.
        print(f"PRUEBA T-402: {len(data['partidas'])} partidas, factor={factor:.8f}, iteraciones={iterations}")
        print(f"Libro temporal de prueba: {output.relative_to(ROOT)}")
        print(f"JSON temporal de prueba: {json_output.relative_to(ROOT)}")
    else:
        print(f"Presupuesto generado: {output.relative_to(ROOT)}")
        print(f"Intermedio generado: {json_output.relative_to(ROOT)}")
        print(f"Factor de sobrecosto={factor:.8f}; iteraciones={iterations}; subtotal={data['subtotal']:.2f}")
        if excluded_keys:
            print(f"Claves omitidas por falta de cantidad: {', '.join(excluded_keys)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, ValueError, RuntimeError, ValidationError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
