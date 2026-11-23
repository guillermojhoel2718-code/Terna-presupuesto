"""
15_extraer_canceleria.py — Extracción de elementos del vínculo Herrería y Cancelería (T-105).

Entrada: sesión de Revit 2027 activa con modelo_federado.rvt (vínculo TT_ED_EDUCACIÓN_CANCELERIA_2027.rvt)
Salida: _harness/intermedios/revit/TT_ED_EDUCACIÓN_CANCELERIA_2027__<Categoria>.json (11 archivos, schema revit.ExtraccionRevit)
Dependencias: Revit API (Autodesk.Revit.DB), pyrevit agent / pyrevit-mcp (modo query)
Fecha: 23-11-2026 · Dueño: AG-1
Uso:
    pyrevit agent run Scripts/15_extraer_canceleria.py --mode=query --engine=cpython --revit=2027
"""
from _revit_extractor_lib import ejecutar_extraccion_vinculo

if __name__ == "__main__" or "__revit__" in dir():
    result = ejecutar_extraccion_vinculo("TT_ED_EDUCACIÓN_CANCELERIA_2027")
