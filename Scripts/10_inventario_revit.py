"""
10_inventario_revit.py — Inventario de vínculos y conteo de elementos por categoría (T-101).

Entrada: sesión de Revit 2027 activa con modelo_federado.rvt (vía pyrevit agent run --mode=query --engine=cpython)
Salida: JSON en stdout con estado del documento, vínculos, niveles, planificaciones y conteos por categoría
Dependencias: Revit API (Autodesk.Revit.DB)
Fecha: 23-11-2026 · Dueño: AG-1
"""
import json
import os
import Autodesk.Revit.DB as DB

doc = __revit__.ActiveUIDocument.Document

# Categorías de interés para los capítulos 01 a 13 (SPEC_02 §2)
_CAT_NAMES = [
    ("StructuralFoundations", "OST_StructuralFoundation"),
    ("StructuralColumns", "OST_StructuralColumns"),
    ("StructuralFraming", "OST_StructuralFraming"),
    ("StructuralConnections", "OST_StructConnections"),
    ("Rebar", "OST_Rebar"),
    ("Floors", "OST_Floors"),
    ("Walls", "OST_Walls"),
    ("Roofs", "OST_Roofs"),
    ("Ceilings", "OST_Ceilings"),
    ("Gutter", "OST_Gutter"),
    ("Fascia", "OST_Fascia"),
    ("Stairs", "OST_Stairs"),
    ("Ramps", "OST_Ramps"),
    ("Railings", "OST_StairsRailing"),
    ("Doors", "OST_Doors"),
    ("Windows", "OST_Windows"),
    ("CurtainWallPanels", "OST_CurtainWallPanels"),
    ("CurtainWallMullions", "OST_CurtainWallMullions"),
    ("Furniture", "OST_Furniture"),
    ("FurnitureSystems", "OST_FurnitureSystems"),
    ("Casework", "OST_Casework"),
    ("SpecialityEquipment", "OST_SpecialityEquipment"),
    ("GenericModel", "OST_GenericModel"),
    ("Site", "OST_Site"),
    ("Topography", "OST_Topography"),
    ("Toposolid", "OST_Toposolid"),
    ("Parking", "OST_Parking"),
    ("Planting", "OST_Planting"),
    ("PlumbingFixtures", "OST_PlumbingFixtures"),
    ("PipeCurves", "OST_PipeCurves"),
    ("FlexPipeCurves", "OST_FlexPipeCurves"),
    ("PipeFitting", "OST_PipeFitting"),
    ("PipeAccessory", "OST_PipeAccessory"),
    ("MechanicalEquipment", "OST_MechanicalEquipment"),
    ("Sprinklers", "OST_Sprinklers"),
    ("Conduit", "OST_Conduit"),
    ("ConduitFitting", "OST_ConduitFitting"),
    ("CableTray", "OST_CableTray"),
    ("CableTrayFitting", "OST_CableTrayFitting"),
    ("LightingFixtures", "OST_LightingFixtures"),
    ("LightingDevices", "OST_LightingDevices"),
    ("ElectricalFixtures", "OST_ElectricalFixtures"),
    ("ElectricalEquipment", "OST_ElectricalEquipment"),
    ("DataDevices", "OST_DataDevices"),
    ("CommunicationDevices", "OST_CommunicationDevices"),
    ("SecurityDevices", "OST_SecurityDevices"),
    ("FireAlarmDevices", "OST_FireAlarmDevices"),
]
CATEGORIAS_INTERES = [(n, getattr(DB.BuiltInCategory, b, None)) for n, b in _CAT_NAMES]

def inspeccionar_documento(d, vinculo_nombre=None):
    # También escanear TODAS las categorías de elementos físicos (WhereElementIsNotElementType)
    all_elems = DB.FilteredElementCollector(d).WhereElementIsNotElementType().ToElements()
    todas_cats = {}
    for e in all_elems:
        cat = e.Category
        if cat is None:
            continue
        if cat.CategoryType != DB.CategoryType.Model:
            continue
        # Ignorar subcategorías o cámaras/vistas
        cname = cat.Name
        bcat = ""
        try:
            bcat = str(cat.BuiltInCategory)
        except Exception:
            pass
        key = "{} ({})".format(cname, bcat)
        todas_cats[key] = todas_cats.get(key, 0) + 1

    # Conteo por BuiltInCategory explícito
    conteo_explicito = {}
    resumen_tipos = {}
    for nombre_cat, bic in CATEGORIAS_INTERES:
        if bic is None:
            continue
        try:
            col = DB.FilteredElementCollector(d).OfCategory(bic).WhereElementIsNotElementType().ToElements()
            cnt = len(col)
            if cnt > 0:
                conteo_explicito[nombre_cat] = cnt
                tipos_set = {}
                for el in col:
                    tname = ""
                    fname = ""
                    try:
                        tid = el.GetTypeId()
                        if tid and tid != DB.ElementId.InvalidElementId:
                            et = d.GetElement(tid)
                            if et:
                                p_t = et.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME)
                                tname = p_t.AsString() if (p_t and p_t.AsString()) else et.Name
                                p_f = et.get_Parameter(DB.BuiltInParameter.ALL_MODEL_FAMILY_NAME)
                                fname = p_f.AsString() if (p_f and p_f.AsString()) else getattr(et, "FamilyName", "")
                    except Exception:
                        pass
                    ft = "{} | {}".format(fname or "-", tname or "-")
                    tipos_set[ft] = tipos_set.get(ft, 0) + 1
                resumen_tipos[nombre_cat] = tipos_set
        except Exception as ex:
            pass

    # Niveles
    niveles = []
    try:
        for lv in DB.FilteredElementCollector(d).OfClass(DB.Level).ToElements():
            elev_m = DB.UnitUtils.ConvertFromInternalUnits(lv.Elevation, DB.UnitTypeId.Meters)
            niveles.append({"id": int(lv.Id.Value), "nombre": lv.Name, "elevacion_m": round(elev_m, 4)})
    except Exception:
        pass

    # Tablas de planificación (ViewSchedule)
    schedules = []
    try:
        for vs in DB.FilteredElementCollector(d).OfClass(DB.ViewSchedule).ToElements():
            if not vs.IsTitleblockRevisionSchedule and not vs.IsInternalKeynoteSchedule:
                schedules.append({"id": int(vs.Id.Value), "nombre": vs.Name})
    except Exception:
        pass

    return {
        "titulo": d.Title,
        "ruta": d.PathName,
        "vinculo": vinculo_nombre,
        "niveles": sorted(niveles, key=lambda x: x["elevacion_m"]),
        "planificaciones": schedules,
        "conteo_categorias_interes": conteo_explicito,
        "todas_categorias_modelo": todas_cats,
        "tipos_por_categoria": resumen_tipos,
    }

resultado = {
    "federado": inspeccionar_documento(doc, None),
    "vinculos": []
}

link_instances = DB.FilteredElementCollector(doc).OfClass(DB.RevitLinkInstance).ToElements()
for li in link_instances:
    ldoc = li.GetLinkDocument()
    lt = doc.GetElement(li.GetTypeId())
    status = str(lt.GetLinkedFileStatus()) if lt else "Unknown"
    if ldoc:
        info = inspeccionar_documento(ldoc, li.Name)
        info["link_instance_id"] = int(li.Id.Value)
        info["estado"] = status
        resultado["vinculos"].append(info)
    else:
        resultado["vinculos"].append({
            "link_instance_id": int(li.Id.Value),
            "vinculo": li.Name,
            "estado": status,
            "error": "No cargado (GetLinkDocument() == None)"
        })

print(json.dumps(resultado, ensure_ascii=False))
