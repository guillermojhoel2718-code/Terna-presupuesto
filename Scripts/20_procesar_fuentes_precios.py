"""
20_procesar_fuentes_precios.py — Procesa fuentes de precios para AG-2 (T-201, T-202, T-203).

Entrada:
  - Resources/referencias_docs/tabulador-general-*.pdf (si existe localmente)
  - Resources/referencias_docs/PRESUPUESTO CENTRO DE INVESTIGACION XALAPA_*.pdf
  - Resources/resultado_ejemplo_neodata/*.pdf (01, 02, 03, 05, 08, 09, 10, 11)
  - Resources/precios_procesados/*.csv (catalogo_apuc_mvp.csv, insumos_apuc_norm.csv, ppto_reftab_apuc_norm.csv)
Salida:
  - _harness/intermedios/pdf/<nombre>.txt (con marcas === PAGINA N ===)
  - _harness/intermedios/pdf/tabulador_cdmx_indice.json (si existe el PDF del tabulador)
  - _harness/intermedios/precios/insumos_norm.json (insumos deduplicados por codigo y unidades normalizadas)
Dependencias: pdfplumber, Scripts/schemas/common.py
Fecha: 23-11-2026
Dueño: AG-2
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "Scripts" / "schemas"))

from common import normalizar_unidad  # noqa: E402


def _ext_win(p: Path) -> str:
    s = str(p)
    return s if s.startswith("\\\\?\\") else f"\\\\?\\{s}"


def escribir_atomico(path: Path, contenido: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(_ext_win(tmp), "w", encoding="utf-8") as f:
        f.write(contenido)
    os.replace(_ext_win(tmp), _ext_win(path))


def con_lock_pdf(nombre_lock: str, fn):
    lock_dir = ROOT / "_harness" / "locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / f"{nombre_lock}.lock"
    if lock_path.exists():
        # Esperar brevemente si otro agente local está extrayendo el mismo PDF
        for _ in range(10):
            if not lock_path.exists():
                break
            time.sleep(1)
        if lock_path.exists():
            print(f"SKIP lock activo: {lock_path.name}")
            return None
    try:
        lock_path.write_text(f"AG-2 | {datetime.now().isoformat()}\n", encoding="utf-8")
        return fn()
    finally:
        if lock_path.exists():
            try:
                lock_path.unlink()
            except OSError:
                pass


def extraer_pdf_a_txt(pdf_path: Path, txt_path: Path) -> int:
    if txt_path.exists() and txt_path.stat().st_size > 0:
        print(f"REUSE {txt_path.relative_to(ROOT)} ({txt_path.stat().st_size} bytes)")
        return -1

    def _do():
        if txt_path.exists() and txt_path.stat().st_size > 0:
            return -1
        raw_str = str(pdf_path)
        ext_path = raw_str if raw_str.startswith("\\\\?\\") else f"\\\\?\\{raw_str}"
        paginas = []
        with open(ext_path, "rb") as fp:
            with pdfplumber.open(fp) as pdf:
                for idx, page in enumerate(pdf.pages, start=1):
                    texto = page.extract_text() or ""
                    paginas.append(f"=== PAGINA {idx} ===\n{texto.strip()}")
                num_pages = len(pdf.pages)
        escribir_atomico(txt_path, "\n\n".join(paginas) + "\n")
        print(f"OK    {txt_path.relative_to(ROOT)} ({num_pages} páginas)")
        return num_pages

    res = con_lock_pdf(txt_path.stem, _do)
    return res if res is not None else 0


def buscar_pdf_por_patron(carpeta: Path, substring: str) -> Path | None:
    if not carpeta.exists():
        return None
    sub_norm = unicodedata.normalize("NFC", substring).lower()
    for p in sorted(carpeta.iterdir()):
        if p.suffix.lower() == ".pdf":
            name_norm = unicodedata.normalize("NFC", p.name).lower()
            if sub_norm in name_norm:
                return p
    return None


def _existe_win_largo(ruta: Path) -> bool:
    raw = str(ruta)
    ext = raw if raw.startswith("\\\\?\\") else f"\\\\?\\{raw}"
    try:
        os.stat(ext)
        return True
    except OSError:
        return False


def procesar_tabulador_cdmx() -> dict:
    import subprocess
    ref_dir = ROOT / "Resources" / "referencias_docs"
    pdf_dir = ROOT / "_harness" / "intermedios" / "pdf"
    nombre_exacto = (
        "tabulador-general-de-precios-unitarios-del-gobierno-de-la-ciudad-de-mexico-"
        "actualizacion-de-septiembre-2026.pdf"
    )
    ruta_exacta = ref_dir / nombre_exacto
    indice_path = pdf_dir / "tabulador_cdmx_indice.json"

    # Ejecutar attrib con cwd=ref_dir para evitar límite MAX_PATH (261 chars > 260)
    r_file = subprocess.run(
        ["attrib", "+P", "-U", nombre_exacto],
        cwd=str(ref_dir),
        capture_output=True,
        text=True,
    )
    r_list = subprocess.run(
        ["attrib", "*.*"],
        cwd=str(ref_dir),
        capture_output=True,
        text=True,
    )
    print(f"INFO  Longitud ruta completa: {len(str(ruta_exacta))} chars (MAX_PATH=260)")
    print("INFO  attrib +P -U (cwd=referencias_docs):", (r_file.stdout or r_file.stderr).strip())
    print("INFO  attrib *.* (cwd=referencias_docs):\n" + (r_list.stdout or r_list.stderr).strip())

    ext_dir = f"\\\\?\\{ref_dir}"
    entradas_ext = [e.name for e in os.scandir(ext_dir)] if os.path.exists(ext_dir) else []
    print("INFO  scandir(\\\\?\\referencias_docs):", entradas_ext)

    pdf_path: Path | None = None
    if _existe_win_largo(ruta_exacta):
        pdf_path = ruta_exacta
    else:
        for ename in entradas_ext:
            if "tabulador" in ename.lower() and ename.lower().endswith(".pdf"):
                pdf_path = ref_dir / ename
                break

    if pdf_path is None:
        # Esperar hasta 40 s (4 intentos cada 10 s) por si OneDrive está sincronizando el archivo
        for intento in range(1, 5):
            print(f"INFO  Esperando sincronización OneDrive del tabulador CDMX (intento {intento}/4, 10s)...")
            time.sleep(10.0)
            subprocess.run(["attrib", "+P", "-U", nombre_exacto], cwd=str(ref_dir), capture_output=True, text=True)
            entradas_ext = [e.name for e in os.scandir(ext_dir)] if os.path.exists(ext_dir) else []
            if _existe_win_largo(ruta_exacta):
                pdf_path = ruta_exacta
                break
            for ename in entradas_ext:
                if "tabulador" in ename.lower() and ename.lower().endswith(".pdf"):
                    pdf_path = ref_dir / ename
                    break
            if pdf_path is not None:
                break

    txt_existentes = sorted(pdf_dir.glob("*tabulador*.txt")) if pdf_dir.exists() else []

    if pdf_path is None and not txt_existentes:
        err_msg = (
            f"Ruta completa mide {len(str(ruta_exacta))} caracteres (> MAX_PATH=260 en Windows). "
            f"Al ejecutar `attrib +P -U {nombre_exacto}` desde `Resources\\referencias_docs`, "
            f"attrib devolvió: '{(r_file.stdout or r_file.stderr).strip()}'. "
            f"Archivos en `\\\\?\\...\\Resources\\referencias_docs`: {entradas_ext}. "
            f"OneDrive en PC-A o PC-B no ha podido sincronizar el archivo probablemente porque la ruta completa "
            f"en PC-B excede MAX_PATH (261 chars)."
        )
        print(f"WARN  No apareció {nombre_exacto}. {err_msg}")
        payload = {
            "fuente": f"{nombre_exacto} (no sincronizado en PC-B)",
            "disponible": False,
            "error_onedrive": err_msg,
            "fecha_extraccion": "23-11-2026",
            "total_conceptos": 0,
            "conceptos": {},
        }
        escribir_atomico(indice_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return {"disponible": False, "error": err_msg, "conceptos": {}}

    txt_path = txt_existentes[0] if txt_existentes else (pdf_dir / "tabulador_cdmx_2026.txt")
    if pdf_path is not None:
        extraer_pdf_a_txt(pdf_path, txt_path)

    with open(_ext_win(txt_path), "r", encoding="utf-8") as f:
        texto = f.read()
    conceptos = {}
    pagina_actual = 1
    # Patrón general para renglones de tabulador: clave al inicio, unidad y precio al final
    re_pag = re.compile(r"^===\s*PAGINA\s+(\d+)\s*===$")
    re_linea = re.compile(
        r"^([A-Z0-9][A-Z0-9.\-_]{3,24})\s+(.+?)\s+(M2|M3|M|ML|PZA|KG|TON|LOTE|SAL|JGO|LT|HR|JOR|m2|m3|m|ml|pza|kg|ton|lote|jgo|lt|hr|jor)\s+\$?\s*([\d,]+\.\d{2})\b"
    )
    for raw_line in texto.splitlines():
        line = raw_line.strip()
        m_pag = re_pag.match(line)
        if m_pag:
            pagina_actual = int(m_pag.group(1))
            continue
        m_lin = re_linea.match(line)
        if m_lin:
            clave, desc, unidad, precio_s = m_lin.groups()
            try:
                precio = float(precio_s.replace(",", ""))
            except ValueError:
                continue
            conceptos[clave] = {
                "clave": clave,
                "pagina": pagina_actual,
                "descripcion": desc.strip(),
                "unidad": normalizar_unidad(unidad),
                "precio_unitario": precio,
            }

    payload = {
        "fuente": pdf_path.name if pdf_path else txt_path.name,
        "fecha_extraccion": "23-11-2026",
        "total_conceptos": len(conceptos),
        "conceptos": conceptos,
    }
    escribir_atomico(indice_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"OK    {indice_path.relative_to(ROOT)} ({len(conceptos)} conceptos indexados)")
    return {"disponible": True, "total": len(conceptos)}


def procesar_pdfs_neodata_y_xalapa() -> dict[str, int]:
    pdf_dir = ROOT / "_harness" / "intermedios" / "pdf"
    neo_dir = ROOT / "Resources" / "resultado_ejemplo_neodata"
    ref_dir = ROOT / "Resources" / "referencias_docs"

    resultados = {}
    pdfs_neodata = [
        "01 PRESUPUESTO.pdf",
        "02 PRECIOS UNITARIOS.pdf",
        "03 BÁSICOS.pdf",
        "05 SALARIOS.pdf",
        "08 COSTOS HORARIOS.pdf",
        "09 RELACIÓN MAQUINARIA.pdf",
        "10 RELACIÓN MANO DE OBRA.pdf",
        "11 RELACIÓN MATERIALES.pdf",
    ]
    for nombre in pdfs_neodata:
        p = buscar_pdf_por_patron(neo_dir, nombre[:5])
        if p and p.exists():
            stem_norm = unicodedata.normalize("NFC", p.stem)
            out_txt = pdf_dir / f"{stem_norm}.txt"
            resultados[p.name] = extraer_pdf_a_txt(p, out_txt)
        else:
            print(f"WARN  No encontrado: {nombre}")

    xalapa_pdf = buscar_pdf_por_patron(ref_dir, "xalapa")
    if xalapa_pdf and xalapa_pdf.exists():
        stem_norm = unicodedata.normalize("NFC", xalapa_pdf.stem)
        out_txt = pdf_dir / f"{stem_norm}.txt"
        resultados[xalapa_pdf.name] = extraer_pdf_a_txt(xalapa_pdf, out_txt)
        # También guardar copia con alias corto xalapa_presupuesto.txt para fácil consulta
        alias_txt = pdf_dir / "PRESUPUESTO_XALAPA.txt"
        if not alias_txt.exists() and out_txt.exists():
            escribir_atomico(alias_txt, out_txt.read_text(encoding="utf-8"))
    else:
        print("WARN  No encontrado PDF Xalapa en Resources/referencias_docs/")

    return resultados


def procesar_insumos_csv() -> dict:
    proc_dir = ROOT / "Resources" / "precios_procesados"
    out_path = ROOT / "_harness" / "intermedios" / "precios" / "insumos_norm.json"

    archivos = [
        ("catalogo_apuc_mvp.csv", True),
        ("insumos_apuc_norm.csv", False),
        ("ppto_reftab_apuc_norm.csv", False),
    ]

    por_codigo: dict[str, dict] = {}
    filas_leidas = 0
    duplicados = 0
    unidades_corregidas = 0

    for nombre_csv, tiene_tipo in archivos:
        ruta = proc_dir / nombre_csv
        if not ruta.exists():
            print(f"WARN  No existe {ruta}")
            continue
        with ruta.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                filas_leidas += 1
                codigo = (row.get("codigo") or "").strip()
                if not codigo:
                    continue
                try:
                    precio = float((row.get("precio_unitario") or "0").replace(",", "").strip())
                except ValueError:
                    continue
                u_orig = (row.get("unidad") or "").strip()
                u_norm = normalizar_unidad(u_orig)
                desc = (row.get("descripcion") or "").strip()
                cat = (row.get("categoria") or "").strip()
                subcat = (row.get("subcategoria") or "").strip()
                fuente = (row.get("fuente") or nombre_csv).strip()
                fecha_fuente = (row.get("fecha_fuente") or "").strip()
                u_inf = str(row.get("unidad_inferida") or "").strip().lower() == "true"
                tipo_reg = (row.get("tipo_registro") or "").strip() if tiene_tipo else ""

                if not tipo_reg:
                    cat_l = cat.lower()
                    if "mano de obra" in cat_l or u_norm == "jor":
                        tipo_reg = "mano_obra"
                    elif "maquinaria" in cat_l or "equipo" in cat_l or u_norm == "hr":
                        tipo_reg = "equipo"
                    elif "indirecto" in cat_l or u_norm.startswith("%"):
                        tipo_reg = "herramienta"
                    else:
                        tipo_reg = "material"

                # Si unidad_inferida es True y la descripción indica explícitamente otra unidad (TONELADA, M3, KG, LT, ML)
                if u_inf and u_norm == "pza":
                    desc_u = desc.upper()
                    if "TONELADA" in desc_u or desc_u.endswith(", TON"):
                        u_norm = "ton"
                        unidades_corregidas += 1
                    elif any(x in desc_u for x in ("ARENA DE MINA", "GRAVA DE MINA", "AGUA DE PIPA", "AGUA DE TOMA", "TEPETATE", "BOMBEO DE CONCRETO")) or desc_u.endswith(", M3"):
                        u_norm = "m3"
                        unidades_corregidas += 1
                    elif "LITRO" in desc_u or " CUBETA 19 LTS" in desc_u or " LATA 19 LTS" in desc_u:
                        u_norm = "lt"
                        unidades_corregidas += 1

                item = {
                    "codigo": codigo,
                    "descripcion": desc,
                    "unidad": u_norm,
                    "unidad_original": u_orig,
                    "precio_unitario": precio,
                    "categoria": cat,
                    "subcategoria": subcat,
                    "fuente": fuente,
                    "fecha_fuente": fecha_fuente,
                    "unidad_inferida": u_inf,
                    "tipo_registro": tipo_reg,
                    "archivo_origen": nombre_csv,
                }

                if codigo in por_codigo:
                    duplicados += 1
                    existente = por_codigo[codigo]
                    # Conservar tipo_registro si el nuevo archivo no lo traía
                    if not existente.get("tipo_registro") and tipo_reg:
                        existente["tipo_registro"] = tipo_reg
                    # Preferir registro con unidad_inferida == False
                    if existente["unidad_inferida"] and not u_inf:
                        por_codigo[codigo] = item
                else:
                    por_codigo[codigo] = item

    insumos_lista = sorted(por_codigo.values(), key=lambda x: (x["tipo_registro"], x["categoria"], x["codigo"]))
    resumen = {
        "fecha": "23-11-2026",
        "filas_leidas": filas_leidas,
        "total_unicos": len(insumos_lista),
        "duplicados_omitidos": duplicados,
        "unidades_inferidas_corregidas": unidades_corregidas,
    }
    payload = {
        "resumen": resumen,
        "insumos": insumos_lista,
    }
    escribir_atomico(out_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(
        f"OK    {out_path.relative_to(ROOT)} ({len(insumos_lista)} insumos únicos de {filas_leidas} filas; {duplicados} duplicados)"
    )
    return resumen


def main() -> int:
    print(f"Raíz del proyecto: {ROOT}")
    r_tab = procesar_tabulador_cdmx()
    r_pdf = procesar_pdfs_neodata_y_xalapa()
    r_ins = procesar_insumos_csv()
    print("Resumen:", json.dumps({"tabulador": r_tab, "pdfs": r_pdf, "insumos": r_ins}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
