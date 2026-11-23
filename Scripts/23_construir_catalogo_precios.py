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


def construir_conceptos() -> list[Concepto]:
    mod_01_06 = _cargar_modulo("cap01_06", ROOT / "Scripts" / "21_catalogo_cap01_06.py")
    mod_07_14 = _cargar_modulo("cap07_14", ROOT / "Scripts" / "22_catalogo_cap07_14.py")
    crudos: list[dict] = list(mod_01_06.CAPITULOS_01_06) + list(mod_07_14.CAPITULOS_07_14)

    conceptos: list[Concepto] = []
    for item in crudos:
        apu_items: list[InsumoAPU] = []
        for ins in item.get("apu", []):
            cant = round(float(ins["cantidad"]), 6)
            pu = round(float(ins["precio_unitario"]), 4)
            imp = round(cant * pu, 2)
            u_norm = normalizar_unidad(str(ins["unidad"]))
            apu_items.append(
                InsumoAPU(
                    codigo=str(ins["codigo"]),
                    descripcion=str(ins["descripcion"]),
                    unidad=u_norm if u_norm is not None else Unidad.PZA,
                    cantidad=cant,
                    precio_unitario=pu,
                    importe=imp,
                    fuente=str(ins["fuente"]),
                )
            )

        ft = FuenteTipo(item["fuente_tipo"])
        if ft == FuenteTipo.APU:
            pu_concepto = round(sum(i.importe for i in apu_items), 2)
        else:
            pu_concepto = round(float(item["precio_unitario"]), 2)

        mapeos = [
            MapeoRevit(
                modelo=m.get("modelo"),
                categoria=m["categoria"],
                filtro_tipo=m["filtro_tipo"],
                campo_cantidad=m["campo_cantidad"],
                nota=m.get("nota"),
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
                moneda="MXN",
                fuente_tipo=ft,
                fuente_ref=item["fuente_ref"],
                fecha_fuente=item["fecha_fuente"],
                justificacion=item.get("justificacion"),
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
        f"- **Proyecto:** {cat.proyecto}",
        f"- **Versión:** `{cat.version}` · **Fecha:** `{cat.fecha}` · **Agente:** `{cat.agente}`",
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
        if c.fuente_tipo == FuenteTipo.SUPUESTO:
            lineas.append(f"| `{c.clave}` | `{c.unidad.value}` | ${c.precio_unitario:,.2f} | {c.justificacion} |")

    lineas.extend([
        "",
        "## 3. Catálogo completo por capítulo",
        "",
        "| Clave | Cap. | Unidad | P.U. (CD MXN) | Fuente tipo | Rev. Revit | Concepto (resumen) |",
        "|---|---:|---|---:|---|---|---|",
    ])
    for c in cat.conceptos:
        rev = "Sin cant. Revit" if c.sin_cantidad_revit else ", ".join(f"{m.categoria}:{m.campo_cantidad}" for m in c.mapeo_revit)
        desc_corta = c.concepto[:110] + ("..." if len(c.concepto) > 110 else "")
        lineas.append(
            f"| `{c.clave}` | `{c.capitulo}` | `{c.unidad.value}` | ${c.precio_unitario:,.2f} | `{c.fuente_tipo.value}` | `{rev}` | {desc_corta} |"
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
            c.unidad.value,
            c.precio_unitario,
            c.moneda,
            c.fuente_tipo.value,
            c.fuente_ref,
            c.fecha_fuente,
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
    ws_apu.append(["Clave Concepto", "Código Insumo", "Descripción Insumo", "Unidad", "Cantidad", "P.U. (MXN)", "Importe (MXN)", "Fuente"])
    for col_idx in range(1, 9):
        cell = ws_apu.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font

    for c in cat.conceptos:
        for ins in c.apu:
            ws_apu.append([
                c.clave,
                ins.codigo,
                ins.descripcion,
                ins.unidad.value,
                ins.cantidad,
                ins.precio_unitario,
                ins.importe,
                ins.fuente,
            ])

    ruta_xlsx.parent.mkdir(parents=True, exist_ok=True)
    tmp = ruta_xlsx.with_suffix(f".{os.getpid()}.tmp.xlsx")
    wb.save(tmp)
    os.replace(tmp, ruta_xlsx)
    return True


def main() -> int:
    asegurar_indice_tabulador()
    conceptos = construir_conceptos()

    # Verificar D-016: capítulos 11 y 12 sin conceptos
    cap_11_12 = [c.clave for c in conceptos if c.capitulo in {"11", "12"}]
    if cap_11_12:
        raise ValueError(f"Violación D-016: conceptos en capítulos 11 o 12: {cap_11_12}")

    sin_precio = [c.clave for c in conceptos if c.precio_unitario <= 0]
    supuestos = [c.clave for c in conceptos if c.fuente_tipo == FuenteTipo.SUPUESTO]
    resumen = ResumenCatalogo(
        total_conceptos=len(conceptos),
        con_precio=len(conceptos) - len(sin_precio),
        sin_precio=sin_precio,
        supuestos=supuestos,
    )

    catalogo = CatalogoPrecios(
        version="v01",
        fecha="23-11-2026",
        agente="AG-2",
        proyecto="Centro Comunitario de Desarrollo Integral 'Casa de los Chichimecas' - Edificio de Educación (ED)",
        resumen=resumen,
        conceptos=conceptos,
    )

    payload = catalogo.model_dump(mode="json")

    ruta_intermedio = ROOT / "_harness" / "intermedios" / "precios" / "catalogo_v01.json"
    ruta_cat_json = ROOT / "Catalogo de precios" / "catalogo_v01.json"
    ruta_cat_md = ROOT / "Catalogo de precios" / "resumen_catalogo_v01.md"
    ruta_cat_xlsx = ROOT / "Catalogo de precios" / "Catalogo_precios_v01.xlsx"

    escribir_json_atomico(ruta_intermedio, payload)
    escribir_json_atomico(ruta_cat_json, payload)
    escribir_texto_atomico(ruta_cat_md, generar_resumen_md(catalogo))
    xlsx_ok = exportar_excel(catalogo, ruta_cat_xlsx)

    # Sincronizar Scripts/22_catalogo_cap07_14.py al worktree local si existe
    worktree_scripts = Path(r"C:\Users\kukle\deska\workspaces\Presupuestos taller terminal\trabajo-en-paralelo-memo\Scripts")
    if worktree_scripts.exists() and (ROOT / "Scripts" / "22_catalogo_cap07_14.py").exists():
        dst = worktree_scripts / "22_catalogo_cap07_14.py"
        if dst.resolve() != (ROOT / "Scripts" / "22_catalogo_cap07_14.py").resolve():
            shutil.copy2(ROOT / "Scripts" / "22_catalogo_cap07_14.py", dst)

    print(
        f"OK [catalogo_v01]: total={resumen.total_conceptos}, con_precio={resumen.con_precio}, "
        f"sin_precio={len(resumen.sin_precio)}, supuestos={len(resumen.supuestos)} ({resumen.supuestos}), "
        f"excel={'SI' if xlsx_ok else 'NO'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
