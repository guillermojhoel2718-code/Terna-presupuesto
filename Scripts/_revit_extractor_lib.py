"""
_revit_extractor_lib.py — Biblioteca común de extracción Revit para AG-1 (T-101 a T-107).

Entrada: llamada desde Scripts/10_*.py a 17_*.py dentro de una sesión de Revit 2027 (pyrevit-mcp / pyrevit agent --mode=query)
Salida: JSON por vínculo y categoría en _harness/intermedios/revit/<modelo>__<categoria>.json e indice.json
Dependencias: Revit API (Autodesk.Revit.DB)
Fecha: 23-11-2026 · Dueño: AG-1 · Idempotente.
"""
import json
import os
import Autodesk.Revit.DB as DB

ONEDRIVE_ROOT = r"C:\Users\kukle\OneDrive - Instituto Politecnico Nacional\Taller Terminal - Taller Terminal 1\Presupuestos taller terminal"
WORKTREE_ROOT = r"C:\Users\kukle\deska\workspaces\Presupuestos taller terminal\trabajo-en-paralelo-memo"
ARCHIVOS_REVIT = r"C:\Users\kukle\OneDrive - Instituto Politecnico Nacional\Taller Terminal - Taller Terminal 1\Archivos revit"
FECHA_HOY = "23-11-2026"

MAPA_VINCULOS = {
    "Edificio de educacion": (
        "Scripts/12_extraer_estructura.py",
        [
            ("StructuralFoundations", "OST_StructuralFoundation"),
            ("StructuralColumns", "OST_StructuralColumns"),
            ("StructuralFraming", "OST_StructuralFraming"),
            ("Floors", "OST_Floors"),
            ("Walls", "OST_Walls"),
            ("CurtainWallPanels", "OST_CurtainWallPanels"),
            ("CurtainWallMullions", "OST_CurtainWallMullions"),
            ("Rebar", "OST_Rebar"),
            ("GenericModel", "OST_GenericModel"),
        ]
    ),
    "TT-ED-EDU-ARQ-MOB": (
        "Scripts/13_extraer_arq_mob.py",
        [
            ("Furniture", "OST_Furniture"),
            ("FurnitureSystems", "OST_FurnitureSystems"),
            ("Casework", "OST_Casework"),
            ("SpecialtyEquipment", "OST_SpecialityEquipment"),
        ]
    ),
    "Proyecto acabado-DAMIAN": (
        "Scripts/14_extraer_acabados.py",
        [
            ("Floors", "OST_Floors"),
            ("Walls", "OST_Walls"),
            ("Ceilings", "OST_Ceilings"),
        ]
    ),
    "TT_ED_EDUCACIÓN_CANCELERIA_2027": (
        "Scripts/15_extraer_canceleria.py",
        [
            ("Doors", "OST_Doors"),
            ("Windows", "OST_Windows"),
            ("CurtainWallPanels", "OST_CurtainWallPanels"),
            ("CurtainWallMullions", "OST_CurtainWallMullions"),
            ("Railings", "OST_StairsRailing"),
            ("Stairs", "OST_Stairs"),
            ("StructuralColumns", "OST_StructuralColumns"),
            ("StructuralFraming", "OST_StructuralFraming"),
            ("Walls", "OST_Walls"),
            ("Floors", "OST_Floors"),
            ("Furniture", "OST_Furniture"),
        ]
    ),
    "Instalaciones": (
        "Scripts/16_extraer_ihs.py",
        [
            ("Pipes", "OST_PipeCurves"),
            ("FlexPipes", "OST_FlexPipeCurves"),
            ("PipeFittings", "OST_PipeFitting"),
            ("PipeAccessories", "OST_PipeAccessory"),
            ("PlumbingFixtures", "OST_PlumbingFixtures"),
            ("MechanicalEquipment", "OST_MechanicalEquipment"),
            ("SpecialtyEquipment", "OST_SpecialityEquipment"),
        ]
    ),
    "Proyecto electrico_corregido": (
        "Scripts/17_extraer_electrico.py",
        [
            ("Conduits", "OST_Conduit"),
            ("ConduitFittings", "OST_ConduitFitting"),
            ("CableTrays", "OST_CableTray"),
            ("CableTrayFittings", "OST_CableTrayFitting"),
            ("LightingFixtures", "OST_LightingFixtures"),
            ("LightingDevices", "OST_LightingDevices"),
            ("ElectricalFixtures", "OST_ElectricalFixtures"),
            ("ElectricalEquipment", "OST_ElectricalEquipment"),
            ("Wires", "OST_Wire"),
            ("DataDevices", "OST_DataDevices"),
            ("CommunicationDevices", "OST_CommunicationDevices"),
            ("SecurityDevices", "OST_SecurityDevices"),
            ("FireAlarmDevices", "OST_FireAlarmDevices"),
            ("SpecialtyEquipment", "OST_SpecialityEquipment"),
            ("MechanicalEquipment", "OST_MechanicalEquipment"),
            ("Walls", "OST_Walls"),
            ("Floors", "OST_Floors"),
            ("Ceilings", "OST_Ceilings"),
            ("Doors", "OST_Doors"),
            ("Windows", "OST_Windows"),
            ("StructuralFraming", "OST_StructuralFraming"),
            ("Pipes", "OST_PipeCurves"),
            ("PipeFittings", "OST_PipeFitting"),
            ("PipeAccessories", "OST_PipeAccessory"),
            ("PlumbingFixtures", "OST_PlumbingFixtures"),
        ]
    ),
}

_LEVEL_BIPS = []
for _n in (
    "INSTANCE_REFERENCE_LEVEL_PARAM",
    "FAMILY_LEVEL_PARAM",
    "FAMILY_BASE_LEVEL_PARAM",
    "SCHEDULE_LEVEL_PARAM",
    "WALL_BASE_CONSTRAINT",
    "STAIRS_BASE_LEVEL_PARAM",
    "RBS_START_LEVEL_PARAM",
):
    _b = getattr(DB.BuiltInParameter, _n, None)
    if _b is not None:
        _LEVEL_BIPS.append(_b)

_LEN_BIPS = []
for _n in (
    "CURVE_ELEM_LENGTH",
    "INSTANCE_LENGTH_PARAM",
    "STRUCTURAL_FRAME_CUT_LENGTH",
    "REBAR_ELEM_TOTAL_LENGTH",
    "HOST_PERIMETER_COMPUTED",
):
    _b = getattr(DB.BuiltInParameter, _n, None)
    if _b is not None:
        _LEN_BIPS.append(_b)

_WIDTH_BIPS = []
for _n in (
    "DOOR_WIDTH",
    "WINDOW_WIDTH",
    "FAMILY_WIDTH_PARAM",
    "GENERIC_WIDTH",
):
    _b = getattr(DB.BuiltInParameter, _n, None)
    if _b is not None:
        _WIDTH_BIPS.append(_b)

_HEIGHT_BIPS = []
for _n in (
    "DOOR_HEIGHT",
    "WINDOW_HEIGHT",
    "FAMILY_HEIGHT_PARAM",
    "GENERIC_HEIGHT",
):
    _b = getattr(DB.BuiltInParameter, _n, None)
    if _b is not None:
        _HEIGHT_BIPS.append(_b)

_VOL_BIPS = []
for _n in (
    "HOST_VOLUME_COMPUTED",
    "REINFORCEMENT_VOLUME",
):
    _b = getattr(DB.BuiltInParameter, _n, None)
    if _b is not None:
        _VOL_BIPS.append(_b)


def ruta_relativa(abs_path):
    if not abs_path:
        return ""
    p = abs_path.replace("\\", "/")
    r1 = ONEDRIVE_ROOT.replace("\\", "/")
    r2 = ARCHIVOS_REVIT.replace("\\", "/")
    if p.lower().startswith(r1.lower() + "/"):
        return p[len(r1) + 1:]
    if p.lower().startswith(r2.lower() + "/"):
        return "../Archivos revit/" + p[len(r2) + 1:]
    return os.path.basename(p)


def escribir_json_ambos(rel_path, obj):
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    for base in (ONEDRIVE_ROOT, WORKTREE_ROOT):
        if not os.path.exists(base):
            continue
        full = os.path.join(base, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        tmp = full + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, full)


def obtener_nivel_rapido(elem, level_map):
    try:
        lid = elem.LevelId
        if lid and lid != DB.ElementId.InvalidElementId:
            lv = level_map.get(int(lid.Value))
            if lv:
                return lv
    except Exception:
        pass
    for bip in _LEVEL_BIPS:
        try:
            p = elem.get_Parameter(bip)
            if p and p.HasValue:
                eid = p.AsElementId()
                if eid and eid != DB.ElementId.InvalidElementId:
                    lv = level_map.get(int(eid.Value))
                    if lv:
                        return lv
        except Exception:
            pass
    try:
        if hasattr(elem, "Host") and elem.Host:
            return obtener_nivel_rapido(elem.Host, level_map)
    except Exception:
        pass
    return None


def info_tipo_cacheada(ldoc, etype, type_cache):
    if etype is None:
        return (None, None, None, {})
    tid = int(etype.Id.Value)
    if tid in type_cache:
        return type_cache[tid]

    tname = etype.Name
    fname = getattr(etype, "FamilyName", None)
    try:
        p_t = etype.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME)
        if p_t and p_t.AsString():
            tname = p_t.AsString()
        p_f = etype.get_Parameter(DB.BuiltInParameter.ALL_MODEL_FAMILY_NAME)
        if p_f and p_f.AsString():
            fname = p_f.AsString()
    except Exception:
        pass

    mat_str = None
    for bip_name in ("STRUCTURAL_MATERIAL_PARAM", "MATERIAL_ID_PARAM"):
        bip = getattr(DB.BuiltInParameter, bip_name, None)
        if bip is None:
            continue
        try:
            p = etype.get_Parameter(bip)
            if p and p.HasValue:
                mid = p.AsElementId()
                if mid and mid != DB.ElementId.InvalidElementId:
                    m = ldoc.GetElement(mid)
                    if m:
                        mat_str = m.Name
                        break
        except Exception:
            pass
    if not mat_str and hasattr(etype, "GetCompoundStructure"):
        try:
            cs = etype.GetCompoundStructure()
            if cs:
                mats = []
                for layer in cs.GetLayers():
                    if layer.MaterialId and layer.MaterialId != DB.ElementId.InvalidElementId:
                        m = ldoc.GetElement(layer.MaterialId)
                        if m and m.Name not in mats:
                            mats.append(m.Name)
                if mats:
                    mat_str = " + ".join(mats[:3])
        except Exception:
            pass

    p_tipo = {}
    SKIP = {"IfcGUID", "Type IfcGUID", "Export to IFC", "Export Type to IFC", "Design Option", "Category", "Family and Type", "Family Name", "Type Name", "Family", "Type", "Type Id"}
    try:
        for p in etype.Parameters:
            name = p.Definition.Name
            if name in SKIP:
                continue
            val = None
            st = p.StorageType
            if st == DB.StorageType.String:
                val = p.AsString()
            elif st == DB.StorageType.Double:
                val = p.AsValueString()
            elif st == DB.StorageType.Integer:
                val = p.AsValueString() or p.AsInteger()
            elif st == DB.StorageType.ElementId:
                val = p.AsValueString()
            if val is not None and str(val).strip() != "" and str(val) != "None":
                p_tipo[name] = val
                if not mat_str and "material" in name.lower() and str(val) != "<By Category>":
                    mat_str = str(val)
    except Exception:
        pass

    res = (fname, tname, mat_str, p_tipo)
    type_cache[tid] = res
    return res


def extraer_cantidades_rapido(ldoc, elem, etype, cat_key):
    longitud_m = None
    area_m2 = None
    volumen_m3 = None
    peso_kg = None

    for bip in _LEN_BIPS:
        try:
            p = elem.get_Parameter(bip)
            if p and p.HasValue and p.StorageType == DB.StorageType.Double:
                v_ft = p.AsDouble()
                if v_ft > 1e-6:
                    longitud_m = round(DB.UnitUtils.ConvertFromInternalUnits(v_ft, DB.UnitTypeId.Meters), 6)
                    break
        except Exception:
            pass
    if longitud_m is None and cat_key in ("StructuralFoundations", "Railings", "Stairs", "StructuralColumns"):
        for pname in ("Length", "System Length"):
            try:
                p = elem.LookupParameter(pname)
                if p and p.HasValue and p.StorageType == DB.StorageType.Double and p.AsDouble() > 1e-6:
                    longitud_m = round(DB.UnitUtils.ConvertFromInternalUnits(p.AsDouble(), DB.UnitTypeId.Meters), 6)
                    break
            except Exception:
                pass
    if longitud_m is None and isinstance(elem, DB.WallFoundation):
        try:
            w = ldoc.GetElement(elem.WallId)
            if w:
                p_wl = w.get_Parameter(DB.BuiltInParameter.CURVE_ELEM_LENGTH)
                if p_wl and p_wl.HasValue and p_wl.AsDouble() > 1e-6:
                    longitud_m = round(DB.UnitUtils.ConvertFromInternalUnits(p_wl.AsDouble(), DB.UnitTypeId.Meters), 6)
        except Exception:
            pass

    try:
        p = elem.get_Parameter(DB.BuiltInParameter.HOST_AREA_COMPUTED)
        if p and p.HasValue and p.StorageType == DB.StorageType.Double and p.AsDouble() > 1e-6:
            area_m2 = round(DB.UnitUtils.ConvertFromInternalUnits(p.AsDouble(), DB.UnitTypeId.SquareMeters), 6)
    except Exception:
        pass
    if area_m2 is None and cat_key in ("Doors", "Windows", "CurtainWallPanels"):
        w_m = None
        h_m = None
        for target in (elem, etype):
            if target is None:
                continue
            for bip_w in _WIDTH_BIPS:
                try:
                    pw = target.get_Parameter(bip_w)
                    if pw and pw.HasValue and pw.StorageType == DB.StorageType.Double and pw.AsDouble() > 1e-6:
                        w_m = DB.UnitUtils.ConvertFromInternalUnits(pw.AsDouble(), DB.UnitTypeId.Meters)
                        break
                except Exception:
                    pass
            for bip_h in _HEIGHT_BIPS:
                try:
                    ph = target.get_Parameter(bip_h)
                    if ph and ph.HasValue and ph.StorageType == DB.StorageType.Double and ph.AsDouble() > 1e-6:
                        h_m = DB.UnitUtils.ConvertFromInternalUnits(ph.AsDouble(), DB.UnitTypeId.Meters)
                        break
                except Exception:
                    pass
        if w_m and h_m:
            area_m2 = round(w_m * h_m, 6)

    for bip in _VOL_BIPS:
        try:
            p = elem.get_Parameter(bip)
            if p and p.HasValue and p.StorageType == DB.StorageType.Double and p.AsDouble() > 1e-8:
                volumen_m3 = round(DB.UnitUtils.ConvertFromInternalUnits(p.AsDouble(), DB.UnitTypeId.CubicMeters), 6)
                break
        except Exception:
            pass

    if cat_key in ("Rebar", "StructuralColumns", "StructuralFraming"):
        for pname in ("Reinforcement Mass", "Exact Weight", "Weight"):
            try:
                p = elem.LookupParameter(pname)
                if p and p.HasValue and p.StorageType == DB.StorageType.Double and p.AsDouble() > 1e-6:
                    val_raw = p.AsDouble()
                    try:
                        val_kg = DB.UnitUtils.ConvertFromInternalUnits(val_raw, DB.UnitTypeId.Kilograms)
                    except Exception:
                        val_kg = val_raw
                    peso_kg = round(val_kg, 6)
                    break
            except Exception:
                pass

    return {
        "longitud_m": longitud_m,
        "area_m2": area_m2,
        "volumen_m3": volumen_m3,
        "conteo": 1,
        "peso_kg": peso_kg,
    }


def ejecutar_extraccion_vinculo(filtro_titulo=None):
    import __main__
    doc = getattr(__main__, "doc", None)
    if doc is None and hasattr(__main__, "__revit__"):
        doc = __main__.__revit__.ActiveUIDocument.Document

    indice_archivos = []
    resumen_modelos = []

    for li in DB.FilteredElementCollector(doc).OfClass(DB.RevitLinkInstance).ToElements():
        ldoc = li.GetLinkDocument()
        if not ldoc:
            continue
        titulo = ldoc.Title
        if titulo not in MAPA_VINCULOS:
            continue
        if filtro_titulo and titulo != filtro_titulo:
            continue
        script_rel, lista_cats = MAPA_VINCULOS[titulo]
        ruta_rel = ruta_relativa(ldoc.PathName)
        modelo_rvt = os.path.basename(ldoc.PathName)
        vinculo_inst = li.Name

        niveles_info = []
        level_map = {}
        for lv in DB.FilteredElementCollector(ldoc).OfClass(DB.Level).ToElements():
            lid = int(lv.Id.Value)
            level_map[lid] = lv.Name
            elev_m = round(DB.UnitUtils.ConvertFromInternalUnits(lv.Elevation, DB.UnitTypeId.Meters), 4)
            niveles_info.append({"id": lid, "nombre": lv.Name, "elevacion_m": elev_m})
        niveles_info.sort(key=lambda x: x["elevacion_m"])

        type_cache = {}
        cats_extraidas = {}

        for cat_key, bic_name in lista_cats:
            bic = getattr(DB.BuiltInCategory, bic_name, None)
            if bic is None:
                continue
            col = DB.FilteredElementCollector(ldoc).OfCategory(bic).WhereElementIsNotElementType().ToElements()
            if not col:
                continue

            elementos_out = []
            tipos_resumen = {}
            is_mep = cat_key in ("Pipes", "FlexPipes", "PipeFittings", "PipeAccessories", "Conduits", "ConduitFittings", "CableTrays", "CableTrayFittings")

            for elem in col:
                eid = int(elem.Id.Value)
                uid = elem.UniqueId
                tid = elem.GetTypeId()
                etype = ldoc.GetElement(tid) if (tid and tid != DB.ElementId.InvalidElementId) else None
                fname, tname, mat_str, p_tipo = info_tipo_cacheada(ldoc, etype, type_cache)
                if not tname:
                    tname = elem.Name

                tname_full = tname
                p_inst = {}
                if is_mep:
                    p_sys = elem.get_Parameter(DB.BuiltInParameter.RBS_SYSTEM_CLASSIFICATION_PARAM)
                    sys_cls = p_sys.AsString() if (p_sys and p_sys.AsString()) else None
                    p_st = elem.get_Parameter(DB.BuiltInParameter.RBS_PIPING_SYSTEM_TYPE_PARAM)
                    sys_type = p_st.AsValueString() if (p_st and p_st.AsValueString()) else None
                    p_sz = elem.get_Parameter(DB.BuiltInParameter.RBS_CALCULATED_SIZE)
                    sz = p_sz.AsString() if (p_sz and p_sz.AsString()) else None
                    partes = [tname or "-"]
                    if sys_type and sys_type != "Undefined":
                        partes.append(sys_type)
                        p_inst["System Type"] = sys_type
                    elif sys_cls:
                        partes.append(sys_cls)
                        p_inst["System Classification"] = sys_cls
                    if sz:
                        partes.append(sz)
                        p_inst["Size"] = sz
                    tname_full = " · ".join(partes)

                try:
                    p_c = elem.get_Parameter(DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
                    if p_c and p_c.AsString():
                        p_inst["Comments"] = p_c.AsString()
                    p_m = elem.get_Parameter(DB.BuiltInParameter.ALL_MODEL_MARK)
                    if p_m and p_m.AsString():
                        p_inst["Mark"] = p_m.AsString()
                except Exception:
                    pass

                nivel_str = obtener_nivel_rapido(elem, level_map)
                cants = extraer_cantidades_rapido(ldoc, elem, etype, cat_key)

                elementos_out.append({
                    "modelo_origen": modelo_rvt,
                    "vinculo": vinculo_inst,
                    "element_id": eid,
                    "unique_id": uid,
                    "categoria": cat_key,
                    "familia": fname,
                    "tipo": tname_full,
                    "nivel": nivel_str,
                    "material_principal": mat_str,
                    "cantidades": cants,
                    "parametros_tipo": p_tipo,
                    "parametros_instancia": p_inst,
                })

                tk = "{} | {}".format(fname or "-", tname_full or "-")
                tr = tipos_resumen.setdefault(tk, {"conteo": 0, "longitud_m": 0.0, "area_m2": 0.0, "volumen_m3": 0.0, "peso_kg": 0.0})
                tr["conteo"] += 1
                if cants["longitud_m"]:
                    tr["longitud_m"] = round(tr["longitud_m"] + cants["longitud_m"], 4)
                if cants["area_m2"]:
                    tr["area_m2"] = round(tr["area_m2"] + cants["area_m2"], 4)
                if cants["volumen_m3"]:
                    tr["volumen_m3"] = round(tr["volumen_m3"] + cants["volumen_m3"], 4)
                if cants["peso_kg"]:
                    tr["peso_kg"] = round(tr["peso_kg"] + cants["peso_kg"], 4)

            elementos_out.sort(key=lambda x: x["element_id"])
            nombre_json = "{}__{}.json".format(titulo, cat_key)
            rel_json = "_harness/intermedios/revit/" + nombre_json

            payload = {
                "modelo": titulo,
                "ruta_modelo": ruta_rel,
                "categoria": cat_key,
                "fecha": FECHA_HOY,
                "herramienta": "pyrevit-mcp",
                "script": script_rel,
                "unidades": "SI (m, m2, m3, kg)",
                "total_elementos": len(elementos_out),
                "elementos": elementos_out,
            }
            escribir_json_ambos(rel_json, payload)

            indice_archivos.append({
                "archivo": rel_json,
                "modelo": titulo,
                "modelo_origen": modelo_rvt,
                "ruta_modelo": ruta_rel,
                "vinculo": vinculo_inst,
                "categoria": cat_key,
                "total_elementos": len(elementos_out),
                "fecha": FECHA_HOY,
                "script": script_rel,
                "tipos": tipos_resumen,
            })
            cats_extraidas[cat_key] = len(elementos_out)

        resumen_modelos.append({
            "modelo": titulo,
            "modelo_origen": modelo_rvt,
            "ruta_modelo": ruta_rel,
            "vinculo": vinculo_inst,
            "link_instance_id": int(li.Id.Value),
            "estado": "Loaded",
            "niveles": niveles_info,
            "categorias_extraidas": cats_extraidas,
        })

    return {"archivos": len(indice_archivos), "vinculos": len(resumen_modelos)}
