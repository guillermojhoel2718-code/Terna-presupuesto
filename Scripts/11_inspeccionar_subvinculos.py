"""
11_inspeccionar_subvinculos.py — Inspecciona sub-vínculos dentro de los 6 vínculos del modelo federado.

Entrada: sesión de Revit 2027 activa con modelo_federado.rvt (vía pyrevit agent run --mode=query --engine=cpython)
Salida: JSON en stdout con los RevitLinkType y RevitLinkInstance dentro de cada vínculo
Dependencias: Revit API (Autodesk.Revit.DB)
Fecha: 23-11-2026 · Dueño: AG-1
"""
import json
import Autodesk.Revit.DB as DB

doc = __revit__.ActiveUIDocument.Document

res = []
for li in DB.FilteredElementCollector(doc).OfClass(DB.RevitLinkInstance).ToElements():
    ldoc = li.GetLinkDocument()
    if not ldoc:
        continue
    sub_links = []
    for sli in DB.FilteredElementCollector(ldoc).OfClass(DB.RevitLinkInstance).ToElements():
        sldoc = sli.GetLinkDocument()
        slt = ldoc.GetElement(sli.GetTypeId())
        status = str(slt.GetLinkedFileStatus()) if slt else "Unknown"
        sub_links.append({
            "name": sli.Name,
            "type_name": slt.Name if slt else None,
            "status": status,
            "loaded": sldoc is not None,
            "path": sldoc.PathName if sldoc else None
        })
    res.append({
        "vinculo": li.Name,
        "titulo": ldoc.Title,
        "sub_links": sub_links
    })

print(json.dumps(res, ensure_ascii=False))
