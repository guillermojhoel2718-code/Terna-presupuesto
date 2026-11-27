"""
18_consolidar_resumen_revit.py — Consolida las 59 extracciones de _harness/intermedios/revit/
en un resumen estructurado por categoría, tipo y nivel listo para generadores (Edificio de educación ~2,500 m²).

Entrada : _harness/intermedios/revit/*.json (59 archivos ExtraccionRevit) + indice.json
Salida  :
  - _harness/intermedios/revit/resumen_por_categoria_y_nivel.json
  - _harness/intermedios/revit/resumen_por_categoria_y_nivel.md
  - MCP Revit/resumen_por_categoria_y_nivel.md
Dependencias: Python 3.11+ (biblioteca estándar)
Fecha   : 26-11-2026 · Dueño: AG-1 · Idempotente (escritura atómica .tmp -> os.replace).
"""
from __future__ import annotations

import glob
import json
import os
from collections import defaultdict
from pathlib import Path

ROOTS = [
    Path(r"C:\Users\kukle\OneDrive - Instituto Politecnico Nacional\Taller Terminal - Taller Terminal 1\Presupuestos taller terminal"),
    Path(r"C:\Users\kukle\deska\workspaces\Presupuestos taller terminal\trabajo-en-paralelo-memo"),
]

FECHA_ACTUAL = "26-11-2026"

NIVEL_CANONICO_MAP = {
    "Nivel 1": ("N0_Sotano_Cimentacion (+0.20 m)", 0.20),
    "Nivel 2": ("N1_Basamento (+3.10 m)", 3.10),
    "Level 3": ("N1_Cisterna_IHS (+3.83 m)", 3.83),
    "Nivel +5.30": ("PB_Planta_Baja (+5.30 m)", 5.30),
    "Nivel - Planta Baja": ("PB_Planta_Baja (+5.30 m)", 5.30),
    "N.P.T +5.30": ("PB_Planta_Baja (+5.30 m)", 5.30),
    "Nivel 3": ("PB_Planta_Baja (+5.30 m)", 5.30),
    "NPT 5.30": ("PB_Planta_Baja (+5.30 m)", 5.30),
    "Nivel 4": ("PB_Mezzanine_6.00 (+6.00 m)", 6.00),
    "NIVEL 6.00": ("PB_Mezzanine_6.00 (+6.00 m)", 6.00),
    "Auxiliar dala intermedia +5.30": ("PB_Dala_Intermedia (+7.13 a +7.65 m)", 7.60),
    "Nivel - Dala Int 01": ("PB_Dala_Intermedia (+7.13 a +7.65 m)", 7.60),
    "Auxiliar dala intermedia +7.65": ("PB_Dala_Intermedia (+7.13 a +7.65 m)", 7.65),
    "N.P.T.": ("PA_Primer_Piso (+8.80 m)", 8.80),
    "Nivel - Primer Piso": ("PA_Primer_Piso (+8.80 m)", 8.80),
    "N.P.T +8.80": ("PA_Primer_Piso (+8.80 m)", 8.80),
    "Nivel 5": ("PA_Primer_Piso (+8.80 m)", 8.80),
    "NPT 8.80": ("PA_Primer_Piso (+8.80 m)", 8.80),
    "Auxiliar dala intermedia +8.80": ("PA_Dala_Intermedia (+10.63 a +11.15 m)", 11.10),
    "Nivel - Dala Int 02": ("PA_Dala_Intermedia (+10.63 a +11.15 m)", 11.10),
    "Auxiliar dala intermedia +11.15": ("PA_Dala_Intermedia (+10.63 a +11.15 m)", 11.15),
    "Nivel +12.30": ("AZ_Azotea (+12.30 m)", 12.30),
    "Nivel - Azotea": ("AZ_Azotea (+12.30 m)", 12.30),
    "PLANTA DE AZOTEA": ("AZ_Azotea (+12.30 m)", 12.30),
    "Nivel 6": ("AZ_Azotea (+12.30 m)", 12.30),
    "NPT 12.30": ("AZ_Azotea (+12.30 m)", 12.30),
    "Nivel +13.80": ("CUB1_Cubierta_01 (+13.80 m)", 13.80),
    "Nivel - Cubierta 01": ("CUB1_Cubierta_01 (+13.80 m)", 13.80),
    "Nivel 7": ("CUB1_Cubierta_01 (+13.80 m)", 13.80),
    "Nivel +14.80": ("CUB2_Cubierta_02 (+14.80 m)", 14.80),
    "Nivel - Cubierta 02": ("CUB2_Cubierta_02 (+14.80 m)", 14.80),
    "Nivel 8": ("CUB2_Cubierta_02 (+14.80 m)", 14.80),
}


def escribir_atomico_ambos(rel_path: str, content: str):
    for r in ROOTS:
        if not r.exists():
            continue
        p = r / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(p.suffix + ".tmp")
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, p)
        print("OK ->", p)


def main() -> int:
    base_root = ROOTS[0] if ROOTS[0].exists() else ROOTS[1]
    revit_dir = base_root / "_harness" / "intermedios" / "revit"

    SKIP_JSON = {"indice.json", "resumen_por_categoria_y_nivel.json"}
    files = sorted([Path(f) for f in glob.glob(str(revit_dir / "*.json")) if Path(f).name not in SKIP_JSON])

    por_modelo_cat_nivel_tipo = []
    por_categoria_nivel = defaultdict(lambda: {"conteo": 0, "longitud_m": 0.0, "area_m2": 0.0, "volumen_m3": 0.0, "peso_kg": 0.0, "sin_longitud": 0, "sin_area": 0, "sin_volumen": 0, "sin_peso": 0})
    por_nivel_canonico = defaultdict(lambda: {"elev_m": 999.0, "conteo": 0, "longitud_m": 0.0, "area_m2": 0.0, "volumen_m3": 0.0, "peso_kg": 0.0})
    huecos_elementos = []

    total_archivos = 0
    total_elementos = 0

    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        if "elementos" not in data or "categoria" not in data:
            continue
        total_archivos += 1
        modelo = data["modelo"]
        modelo_origen = data["elementos"][0]["modelo_origen"] if data["elementos"] else f"{modelo}.rvt"
        cat = data["categoria"]
        rel_file = f"_harness/intermedios/revit/{f.name}"

        grupos = {}
        for e in data["elementos"]:
            total_elementos += 1
            lvl_raw = e.get("nivel")
            lvl = lvl_raw or "SIN_NIVEL (-)"
            canon_name, canon_elev = NIVEL_CANONICO_MAP.get(lvl_raw, ("SIN_NIVEL (-)", 999.0))
            fam = e.get("familia") or "-"
            tip = e.get("tipo") or "-"
            mat = e.get("material_principal") or "-"
            c = e["cantidades"]

            k = (lvl, canon_name, canon_elev, fam, tip, mat)
            g = grupos.setdefault(k, {
                "conteo": 0,
                "longitud_m": 0.0,
                "area_m2": 0.0,
                "volumen_m3": 0.0,
                "peso_kg": 0.0,
                "n_sin_longitud": 0,
                "n_sin_area": 0,
                "n_sin_volumen": 0,
                "n_sin_peso": 0,
                "sample_ids": [],
            })
            g["conteo"] += c.get("conteo", 1)
            if len(g["sample_ids"]) < 5:
                g["sample_ids"].append(e["element_id"])

            for campo, sin_k in (("longitud_m", "n_sin_longitud"), ("area_m2", "n_sin_area"), ("volumen_m3", "n_sin_volumen"), ("peso_kg", "n_sin_peso")):
                v = c.get(campo)
                if v is not None:
                    g[campo] += float(v)
                else:
                    g[sin_k] += 1

            ck = (modelo, cat, lvl, canon_name, canon_elev)
            cg = por_categoria_nivel[ck]
            cg["conteo"] += 1
            for campo, sin_k in (("longitud_m", "sin_longitud"), ("area_m2", "sin_area"), ("volumen_m3", "sin_volumen"), ("peso_kg", "sin_peso")):
                v = c.get(campo)
                if v is not None:
                    cg[campo] += float(v)
                else:
                    cg[sin_k] += 1

            nk = canon_name
            ng = por_nivel_canonico[nk]
            ng["elev_m"] = canon_elev
            ng["conteo"] += 1
            if c.get("longitud_m") is not None:
                ng["longitud_m"] += float(c["longitud_m"])
            if c.get("area_m2") is not None and not (modelo == "Edificio de educacion" and cat == "CurtainWallPanels"):
                ng["area_m2"] += float(c["area_m2"])
            if c.get("volumen_m3") is not None and not (modelo == "Edificio de educacion" and cat == "CurtainWallPanels"):
                ng["volumen_m3"] += float(c["volumen_m3"])
            if c.get("peso_kg") is not None:
                ng["peso_kg"] += float(c["peso_kg"])

        for (lvl, canon_name, canon_elev, fam, tip, mat), g in sorted(grupos.items(), key=lambda x: (x[0][2], x[0][0], x[0][3], x[0][4])):
            entry = {
                "archivo": rel_file,
                "modelo": modelo,
                "modelo_origen": modelo_origen,
                "categoria": cat,
                "nivel_revit": None if lvl == "SIN_NIVEL (-)" else lvl,
                "nivel_canonico": canon_name,
                "elevacion_m": None if canon_elev == 999.0 else canon_elev,
                "familia": fam,
                "tipo": tip,
                "material_principal": None if mat == "-" else mat,
                "conteo": g["conteo"],
                "longitud_m": round(g["longitud_m"], 4),
                "area_m2": round(g["area_m2"], 4),
                "volumen_m3": round(g["volumen_m3"], 4),
                "peso_kg": round(g["peso_kg"], 4),
                "faltantes": {
                    "sin_longitud": g["n_sin_longitud"],
                    "sin_area": g["n_sin_area"],
                    "sin_volumen": g["n_sin_volumen"],
                    "sin_peso": g["n_sin_peso"],
                },
                "muestra_element_ids": g["sample_ids"],
            }
            por_modelo_cat_nivel_tipo.append(entry)

            if cat in ("StructuralFoundations", "StructuralFraming", "StructuralColumns", "Floors", "Walls") and g["n_sin_volumen"] > 0 and cat != "Walls":
                huecos_elementos.append({
                    "modelo": modelo,
                    "categoria": cat,
                    "nivel": lvl,
                    "tipo": f"{fam} | {tip}",
                    "conteo_total": g["conteo"],
                    "sin_volumen_m3": g["n_sin_volumen"],
                    "sin_area_m2": g["n_sin_area"],
                    "muestra_ids": g["sample_ids"],
                })

    reconciliacion_area_m2 = {
        "referencia_D010_m2": 2500.0,
        "estructura_pisos_y_cubierta": {
            "PB_firme_estructural_10cm_m2": 804.0946,
            "PB_plantilla_concreto_5cm_m2": 804.1953,
            "PA_losa_vigueta_bovedilla_25cm_m2": 741.6654,
            "PA_capa_compresion_5cm_m2": 11.4489,
            "AZ_losa_generic_150mm_canceleria_m2": 1113.7323,
            "CUB_cubierta_inclinada_estructura_m2": 367.0639,
            "suma_PB_firme_mas_PA_losa_mas_AZ_losa_m2": round(804.0946 + 753.1143 + 1113.7323, 4),
            "suma_PB_firme_mas_PA_losa_mas_CUB_inclinada_m2": round(804.0946 + 753.1143 + 367.0639, 4),
        },
        "acabados_pisos_por_nivel": {
            "PB_Nivel_3_5.30_concreto_pulido_y_agregado_m2": 1238.7734,
            "PA_Nivel_5_8.80_concreto_densificado_y_ceramica_m2": 323.1738,
            "PA_Nivel_Primer_Piso_8.80_porcelanato_canceleria_m2": 596.4988,
            "PA_plafones_modelados_como_Floors_en_acabados_m2": 1050.4469,
            "PA_plafones_en_Ceilings_acabados_m2": 1125.0812,
            "suma_pisos_acabados_PB_mas_PA_m2": round(1238.7734 + 323.1738 + 596.4988, 4),
        },
        "nota": (
            "La huella estructural techada/pisos (PB Firme 804.09 m² + PA Losa entrepiso 753.11 m² + "
            "Losa Azotea 1,113.73 m² = 2,670.94 m²; o pisos terminados PB 1,238.77 m² + PA 919.67 m² + "
            "Cubierta inclinada 367.06 m² = 2,525.51 m²) encaja con la superficie de referencia D-010 (~2,500 m²)."
        ),
    }

    huecos_y_preguntas = [
        {
            "id_pregunta": "P-010 (Abierta)",
            "capitulo": "08 / 09",
            "archivo": "_harness/intermedios/revit/Instalaciones__PlumbingFixtures.json",
            "hallazgo": "Sub-vínculo 'Bloque de baños_vinculo.rvt' está Unloaded en Instalaciones.rvt. Solo hay 14 cajas de registro y 3 biodigestores (TOL-7000L); 0 WC, 0 lavabos y 0 mingitorios.",
            "impacto": "ED-09-02-001 (inodoros) y ED-09-02-002 (lavabos) quedan con cantidad 0 desde Revit.",
            "supuesto_loop": "Mantener en manual.json o re-extraer T-106 en cuanto el usuario cargue el sub-vínculo en Revit PC-B.",
        },
        {
            "id_pregunta": "P-013 (Nueva AG-1)",
            "capitulo": "02 / 03",
            "archivo": "_harness/intermedios/revit/Edificio de educacion__StructuralFraming.json",
            "hallazgo": (
                "10 tramos cortos de concreto en StructuralFraming tienen volumen_m3 = null y area_m2 = null en Revit "
                "por recortes de unión (1 'Trabe de cimentacion 20x40' id #552895 de L=0.15 m, y 9 'Dala de cerramiento de concreto de 15x25' "
                "ids #435689, #435905, #436684, #436724, #473890, #534743, #534834, #535908, #619739 que suman L=3.49 m). "
                "Generan los 32 avisos del script 30 en ED-02-02-001, ED-02-02-002, ED-03-01-002 y ED-03-02-001."
            ),
            "impacto": "Diferencia despreciable (~0.14 m³ = 0.2% del volumen de trabes/dalas); el volumen de los 334 tramos restantes (84.38 m³) cuadra 100% con la tabla 'Volumen de trabes y dalas' de Revit.",
            "supuesto_loop": "Ignorar los 32 avisos del script 30 y conservar volumen_m3 = null fiel al modelo Revit.",
        },
        {
            "id_pregunta": "P-014 (Nueva AG-1)",
            "capitulo": "04",
            "archivo": "_harness/intermedios/revit/Edificio de educacion__CurtainWallMullions.json",
            "hallazgo": (
                "La cubierta inclinada 'Curtain Wall | Cubierta' (367.06 m²) tiene 587 montantes 'Montante rectangular - 10 x 40 cm' "
                "(longitud_m = 883.5243 m, volumen_m3 = 31.1167 m³, peso_kg = null) que no están asignados a ninguna clave en catalogo_v01.json, "
                "mientras que ED-04-01-001 solo toma los 36 perfiles de acero de Cancelería (30 C310X45 + 6 L150x12 = 4,461.02 kg). "
                "Asimismo, ED-04-01-004 (pintura anticorrosiva en estructura metálica, en kg) tiene sin_cantidad_revit=true."
            ),
            "impacto": "Definir si los 883.52 m de montantes de cubierta se cuantifican como bastidor metálico en ED-04-01-001 (con factor kg/m) y si ED-04-01-004 debe mapear al mismo peso_kg de estructura metálica.",
            "supuesto_loop": "ED-04-01-001 opera con los 4,461.02 kg verificados de Cancelería; los 587 montantes quedan identificados por si CL-1/AG-2 agregan mapeo por longitud_m × factor.",
        },
        {
            "id_pregunta": "P-015 (Nueva AG-1)",
            "capitulo": "06",
            "archivo": "_harness/intermedios/revit/Proyecto acabado-DAMIAN__Floors.json",
            "hallazgo": (
                "En Proyecto acabado-DAMIAN hay 13 plafones modelados dentro de la categoría Floors ('PF_Plafon ACT - Armstrong Ceilings 24x48' = 487.89 m², "
                "'PF_Plafon ACT 14x24' = 535.33 m², 'PF_Plafon de loseta ceramica' = 27.23 m²; subtotal = 1,050.45 m²) además de los 3 plafones en "
                "Ceilings ('ACT - Techos Armstrong - 24x48' = 1,125.08 m²). Actualmente ED-06-03-001 suma ambos (1,023.22 + 1,125.08 = 2,148.30 m² en N5 y N6)."
            ),
            "impacto": "Verificar si los 12 plafones 'PF_Plafon ACT' en Floors (1,023.22 m²) y los 3 'Ceilings' (1,125.08 m²) son áreas complementarias o se solapan en planta.",
            "supuesto_loop": "Mantener ambos en el resumen separados por categoría (Floors vs Ceilings) para que CL-1 decida en T-302 si filtra solo Ceilings (1,125.08 m²) o Floors+Ceilings (2,148.30 m²).",
        },
        {
            "id_pregunta": "P-016 (Nueva AG-1)",
            "capitulo": "01 / 02 / 05 / 06 / 10 / 14",
            "archivo": "_harness/intermedios/generadores/manual.json",
            "hallazgo": (
                "16 claves del catálogo v01 (además de las 2 de muebles sanitarios P-010) no tienen elementos directos en Revit y requieren captura o fórmula derivada en manual.json: "
                "Cap. 01 (ED-01-01-001 limpia, ED-01-01-002 despalme, ED-01-02-001 trazo, ED-01-03-001 bodega), "
                "Cap. 02 (ED-02-01-001 excavación, ED-02-03-001 relleno, ED-02-03-002 acarreo), "
                "Cap. 04 (ED-04-01-002 placas base, ED-04-01-003 anclas, ED-04-01-004 pintura acero, ED-04-02-002 canalón pluvial), "
                "Cap. 05 (ED-05-02-002 aplanado muros), Cap. 06 (ED-06-04-001 impermeabilización azotea), "
                "Cap. 10 (ED-10-05-001 sistema fotovoltaico 10 kWp = 1 jgo), Cap. 14 (ED-14-01-001 limpieza pisos, ED-14-01-002 limpieza vidrios)."
            ),
            "impacto": "Si no se incluyen en manual.json, quedan en claves_sin_cantidad al correr Scripts/30_generadores_desde_revit.py.",
            "supuesto_loop": "Se incluye en el resumen de AG-1 una tabla de cantidades base sugeridas desde medidas geométricas de Revit (huella PB = 804.20 m², azotea = 1,113.73 m², vidrios = 313.10 m², etc.) para alimentar manual.json de inmediato.",
        },
    ]

    cantidades_base_para_manual = [
        {"clave": "ED-01-01-001", "unidad": "m2", "cantidad_sugerida": 804.1953, "criterio_revit": "Área de desplante = Plantilla de concreto e=5cm en Edificio de educacion__Floors.json (#560921)"},
        {"clave": "ED-01-01-002", "unidad": "m3", "cantidad_sugerida": 160.8391, "criterio_revit": "Área de desplante (804.1953 m²) × 0.20 m de espesor de despalme"},
        {"clave": "ED-01-02-001", "unidad": "m2", "cantidad_sugerida": 804.1953, "criterio_revit": "Área de desplante = Plantilla de concreto e=5cm (#560921)"},
        {"clave": "ED-01-03-001", "unidad": "m2", "cantidad_sugerida": 36.0000, "criterio_revit": "SUPUESTO: Caseta y bodega provisional de obra 6.00 × 6.00 m"},
        {"clave": "ED-02-01-001", "unidad": "m3", "cantidad_sugerida": 204.5233, "criterio_revit": "Área de contacto de cimentación (340.8721 m² de Zapata corrida + Dados) × 0.60 m profundidad promedio"},
        {"clave": "ED-02-03-001", "unidad": "m3", "cantidad_sugerida": 110.2820, "criterio_revit": "Excavación (204.5233 m³) − Concreto en cimentación/contratrabes/plantilla (48.5436 + 5.6877 + 40.01 = 94.2413 m³)"},
        {"clave": "ED-02-03-002", "unidad": "m3", "cantidad_sugerida": 255.1594, "criterio_revit": "Despalme (160.8391 m³) + Sobrante de excavación (94.3203 m³) medido en banco"},
        {"clave": "ED-04-01-002", "unidad": "kg", "cantidad_sugerida": 336.4400, "criterio_revit": "37 apoyos de columnas (31 concreto/mixtas + 6 acero L150x12) × placa base A-36 0.30×0.30 m de 1/2\" (9.093 kg/pza)"},
        {"clave": "ED-04-01-003", "unidad": "pza", "cantidad_sugerida": 148.0000, "criterio_revit": "4 anclas cold rolled de 1\"×1.40 m por cada uno de los 37 apoyos de columna (37 × 4)"},
        {"clave": "ED-04-01-004", "unidad": "kg", "cantidad_sugerida": 4461.0194, "criterio_revit": "Mismo peso_kg que ED-04-01-001 (30 Canal C310X45 + 6 Pilar L150x12 en Cancelería)"},
        {"clave": "ED-04-02-002", "unidad": "m", "cantidad_sugerida": 106.6771, "criterio_revit": "50% de la longitud de borde de Curtain Wall | Cubierta (213.3542 m / 2) en Nivel +12.30"},
        {"clave": "ED-05-02-002", "unidad": "m2", "cantidad_sugerida": 1601.4938, "criterio_revit": "Área de muros interiores con acabado en Proyecto acabado-DAMIAN__Walls.json (32 'muro general EDUC' = 1,601.4938 m²)"},
        {"clave": "ED-06-04-001", "unidad": "m2", "cantidad_sugerida": 1113.7323, "criterio_revit": "Área de losas de azotea 'Generic 150mm' en Nivel - Azotea (TT_ED_EDUCACIÓN_CANCELERIA_2027__Floors.json, 4 losas = 1,113.7323 m²)"},
        {"clave": "ED-10-05-001", "unidad": "jgo", "cantidad_sugerida": 1.0000, "criterio_revit": "MEMORIA §9.3: 1 juego de sistema solar fotovoltaico interconectado de 10.0 kWp (18 paneles × 550 Wp)"},
        {"clave": "ED-14-01-001", "unidad": "m2", "cantidad_sugerida": 2391.7529, "criterio_revit": "Suma de pisos terminados (ED-06-01-001: 1,101.70 m² + ED-06-01-002: 623.72 m² + ED-06-01-003: 666.33 m²)"},
        {"clave": "ED-14-01-002", "unidad": "m2", "cantidad_sugerida": 313.0951, "criterio_revit": "Área de vidrios en ventanas y muros cortina (ED-07-02-002: 207.21 m² Glazed + 46.52 m² Puerta Muro Cortina + 59.37 m² Ventanas = 313.10 m²)"},
    ]

    resumen_cat_nivel_list = []
    for (modelo, cat, lvl, canon_name, canon_elev), cg in sorted(por_categoria_nivel.items(), key=lambda x: (x[0][0], x[0][1], x[0][4], x[0][2])):
        resumen_cat_nivel_list.append({
            "modelo": modelo,
            "categoria": cat,
            "nivel_revit": None if lvl == "SIN_NIVEL (-)" else lvl,
            "nivel_canonico": canon_name,
            "elevacion_m": None if canon_elev == 999.0 else canon_elev,
            "conteo": cg["conteo"],
            "longitud_m": round(cg["longitud_m"], 4),
            "area_m2": round(cg["area_m2"], 4),
            "volumen_m3": round(cg["volumen_m3"], 4),
            "peso_kg": round(cg["peso_kg"], 4),
            "faltantes": {
                "sin_longitud": cg["sin_longitud"],
                "sin_area": cg["sin_area"],
                "sin_volumen": cg["sin_volumen"],
                "sin_peso": cg["sin_peso"],
            },
        })

    resumen_niveles_canonicos = []
    for nk, ng in sorted(por_nivel_canonico.items(), key=lambda x: (x[1]["elev_m"], x[0])):
        resumen_niveles_canonicos.append({
            "nivel_canonico": nk,
            "elevacion_m": None if ng["elev_m"] == 999.0 else ng["elev_m"],
            "conteo_elementos": ng["conteo"],
            "longitud_m": round(ng["longitud_m"], 4),
            "area_m2_sin_paneles_duplicados": round(ng["area_m2"], 4),
            "volumen_m3_sin_paneles_duplicados": round(ng["volumen_m3"], 4),
            "peso_kg": round(ng["peso_kg"], 4),
        })

    payload_json = {
        "proyecto": 'Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"',
        "alcance": "Edificio de educación (~2,500 m², 6 vínculos del modelo federado)",
        "fecha": FECHA_ACTUAL,
        "productor": "AG-1",
        "script": "Scripts/18_consolidar_resumen_revit.py",
        "total_archivos_categoria": total_archivos,
        "total_elementos": total_elementos,
        "reconciliacion_superficie_2500m2": reconciliacion_area_m2,
        "resumen_por_nivel_canonico": resumen_niveles_canonicos,
        "resumen_por_categoria_y_nivel": resumen_cat_nivel_list,
        "desglose_para_generadores_por_categoria_nivel_y_tipo": por_modelo_cat_nivel_tipo,
        "huecos_y_preguntas": huecos_y_preguntas,
        "cantidades_derivadas_para_manual_json": cantidades_base_para_manual,
    }

    md = [
        "# Resumen Consolidado por Categoría y Nivel para Generadores (Edificio de Educación ~2,500 m²)",
        "",
        f"- **Fecha**: {FECHA_ACTUAL} · **Agente**: AG-1 (Extracción Revit · PC-B `MEMO`)",
        f"- **Fuente**: 59 archivos JSON validados en `_harness/intermedios/revit/` (`{total_elementos:,}` elementos en los 6 vínculos de `modelo_federado.rvt`).",
        "- **JSON estructurado**: `_harness/intermedios/revit/resumen_por_categoria_y_nivel.json`",
        "- **Script generador (idempotente)**: `Scripts/18_consolidar_resumen_revit.py`",
        "",
        "---",
        "",
        "## 1. Reconciliación de Superficie Construida (~2,500 m², D-010)",
        "",
        "| Nivel Canónico | Elevación | Elementos de Piso / Losa / Cubierta en Revit | Archivo Intermedio | Área (m²) | Volumen (m³) |",
        "|---|---:|---|---|---:|---:|",
        "| **PB · Planta Baja** | `+5.30 m` | `Plantilla de concreto e=5cm` (`#560921`, Cap. 02) | `Edificio de educacion__Floors.json` | **804.1953** | 40.2098 |",
        "| **PB · Planta Baja** | `+5.30 m` | `Firme estructural e=10 cm` (`#516170`, Cap. 05) | `Edificio de educacion__Floors.json` | **804.0946** | 80.4095 |",
        "| **PA · Primer Piso (Entrepiso)** | `+8.80 m` | 10 losas `Suelo de vigueta y bovedilla e=0.25` (`741.6654 m²`) + 1 `Capa de compresion 5cm` (`11.4489 m²`) | `Edificio de educacion__Floors.json` | **753.1143** | 188.1539 |",
        "| **AZ · Azotea** | `+12.30 m` | 4 losas `Generic 150mm` en `Nivel - Azotea` | `TT_ED_EDUCACIÓN_CANCELERIA_2027__Floors.json` | **1,113.7323** | 167.0598 |",
        "| **CUB · Cubierta inclinada** | `+12.30 a +14.62 m` | 18 elementos `Curtain Wall \\| Cubierta` | `Edificio de educacion__Walls.json` | **367.0639** | — |",
        "| **Subtotal Estructura (PB Firme + PA Losa + AZ Losa)** | — | Huella horizontal acumulada de pisos y losas estructurales | — | **2,670.9412** | 435.6232 |",
        "| **Subtotal Pisos Acabados (PB + PA) + Cubierta** | — | Pisos acabados PB (`1,238.77 m²`) + PA (`323.17 + 596.50 = 919.67 m²`) + Cubierta (`367.06 m²`) | `Proyecto acabado-DAMIAN` + `CANCELERIA` + `Estructura` | **2,525.5099** | — |",
        "",
        "> **Conclusión de superficie**: Tanto la suma de pisos terminados más cubierta (**2,525.51 m²**) como la suma de firmes y losas estructurales (**2,670.94 m²**) cuadran con la superficie construida oficial de **~2,500 m² (D-010)**.",
        "",
        "---",
        "",
        "## 2. Resumen Global por Nivel Canónico (Unificando los 6 Vínculos)",
        "",
        "*(Nota: Se excluyen de las columnas de Área y Volumen los 10,467 `CurtainWallPanels` de `Edificio de educacion` para no duplicar los 123 muros `Curtain Wall` de `Walls`, conforme a P-011).* ",
        "",
        "| Nivel Canónico Unificado | Elev. (m) | Niveles equivalentes en los 6 vínculos | Elem. | Longitud Σ (m) | Área Σ (m²) | Volumen Σ (m³) | Peso Acero Σ (kg) |",
        "|---|---:|---|---:|---:|---:|---:|---:|",
    ]

    equiv_str = {
        "N0_Sotano_Cimentacion (+0.20 m)": "`Nivel 1` (ARQ-MOB, Cancelería)",
        "N1_Basamento (+3.10 m)": "`Nivel 2` (ARQ-MOB, Cancelería)",
        "N1_Cisterna_IHS (+3.83 m)": "`Level 3` (Instalaciones IHS)",
        "PB_Planta_Baja (+5.30 m)": "`Nivel +5.30`, `Nivel - Planta Baja`, `N.P.T +5.30`, `Nivel 3`, `NPT 5.30`",
        "PB_Mezzanine_6.00 (+6.00 m)": "`Nivel 4` (Acabados), `NIVEL 6.00` (Eléctrico)",
        "PB_Dala_Intermedia (+7.13 a +7.65 m)": "`Auxiliar dala intermedia +7.65`, `Nivel - Dala Int 01`, `Auxiliar +5.30`",
        "PA_Primer_Piso (+8.80 m)": "`N.P.T.`, `Nivel - Primer Piso`, `N.P.T +8.80`, `Nivel 5`, `NPT 8.80`",
        "PA_Dala_Intermedia (+10.63 a +11.15 m)": "`Auxiliar dala intermedia +11.15`, `Nivel - Dala Int 02`, `Auxiliar +8.80`",
        "AZ_Azotea (+12.30 m)": "`Nivel +12.30`, `Nivel - Azotea`, `PLANTA DE AZOTEA`, `Nivel 6`, `NPT 12.30`",
        "CUB1_Cubierta_01 (+13.80 m)": "`Nivel +13.80`, `Nivel - Cubierta 01`, `Nivel 7`",
        "CUB2_Cubierta_02 (+14.80 m)": "`Nivel +14.80`, `Nivel - Cubierta 02`, `Nivel 8`",
        "SIN_NIVEL (-)": "`nivel = null` (Rebar, Zapata corrida In-Place, 12 WallFoundation, 82 Luminarias Face-Based)",
    }

    for r in resumen_niveles_canonicos:
        elev_txt = f"{r['elevacion_m']:.2f}" if r["elevacion_m"] is not None else "—"
        eq = equiv_str.get(r["nivel_canonico"], "—")
        md.append(
            f"| **{r['nivel_canonico']}** | {elev_txt} | {eq} | {r['conteo_elementos']:,} | "
            f"{r['longitud_m']:,.2f} | {r['area_m2_sin_paneles_duplicados']:,.2f} | "
            f"{r['volumen_m3_sin_paneles_duplicados']:,.2f} | {r['peso_kg']:,.2f} |"
        )

    md += [
        "",
        "---",
        "",
        "## 3. Resumen por Vínculo, Categoría y Nivel (`59` archivos JSON)",
        "",
        "| Vínculo (`modelo`) | Categoría (`categoria`) | Nivel en Revit (`nivel`) | Nivel Canónico | Elem. | Longitud (m) | Área (m²) | Volumen (m³) | Peso (kg) | Faltantes (`L / A / V / P`) |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---|",
    ]

    for r in resumen_cat_nivel_list:
        lvl_txt = r["nivel_revit"] or "SIN_NIVEL (-)"
        f_str = f"{r['faltantes']['sin_longitud']}/{r['faltantes']['sin_area']}/{r['faltantes']['sin_volumen']}/{r['faltantes']['sin_peso']}"
        md.append(
            f"| `{r['modelo']}` | `{r['categoria']}` | `{lvl_txt}` | {r['nivel_canonico']} | "
            f"{r['conteo']:,} | {r['longitud_m']:,.2f} | {r['area_m2']:,.2f} | "
            f"{r['volumen_m3']:,.2f} | {r['peso_kg']:,.2f} | `{f_str}` |"
        )

    md += [
        "",
        "---",
        "",
        "## 4. Huecos Detectados y Marcados como Preguntas (`P-010`, `P-013` a `P-016`)",
        "",
        "| ID | Cap. | Archivo Afectado | Hueco / Discrepancia Detectada | Impacto en Generadores | Supuesto de Trabajo (Loop sin bloqueo) |",
        "|---|---|---|---|---|---|",
    ]

    for h in huecos_y_preguntas:
        md.append(
            f"| **{h['id_pregunta']}** | {h['capitulo']} | `{h['archivo']}` | {h['hallazgo']} | {h['impacto']} | {h['supuesto_loop']} |"
        )

    md += [
        "",
        "---",
        "",
        "## 5. Cantidades Base Derivadas de Geometría Revit para las 16 Claves de `manual.json` (`P-016`)",
        "",
        "Para que CL-1 (rol AG-3) pueda cerrar las partidas `sin_cantidad_revit` en `_harness/intermedios/generadores/manual.json` sin esperar:",
        "",
        "| Clave | Unidad | Cantidad Derivada | Criterio / Elemento Revit de Respaldo |",
        "|---|---|---:|---|",
    ]

    for m in cantidades_base_para_manual:
        md.append(f"| `{m['clave']}` | `{m['unidad']}` | **{m['cantidad_sugerida']:,.4f}** | {m['criterio_revit']} |")

    md_text = "\n".join(md) + "\n"
    json_text = json.dumps(payload_json, ensure_ascii=False, indent=2)

    escribir_atomico_ambos("_harness/intermedios/revit/resumen_por_categoria_y_nivel.json", json_text)
    escribir_atomico_ambos("_harness/intermedios/revit/resumen_por_categoria_y_nivel.md", md_text)
    escribir_atomico_ambos("MCP Revit/resumen_por_categoria_y_nivel.md", md_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
