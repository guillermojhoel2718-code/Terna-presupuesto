"""
14_extraer_acabados.py — Extracción de elementos del vínculo Acabados (T-104).

Entrada: sesión de Revit 2027 activa con modelo_federado.rvt (vínculo Proyecto acabado-DAMIAN.rvt)
Salida: _harness/intermedios/revit/Proyecto acabado-DAMIAN__<Categoria>.json (3 archivos, schema revit.ExtraccionRevit)
Dependencias: Revit API (Autodesk.Revit.DB), pyrevit agent / pyrevit-mcp (modo query)
Fecha: 23-11-2026 · Dueño: AG-1
Uso:
    pyrevit agent run Scripts/14_extraer_acabados.py --mode=query --engine=cpython --revit=2027
"""
from _revit_extractor_lib import ejecutar_extraccion_vinculo

if __name__ == "__main__" or "__revit__" in dir():
    result = ejecutar_extraccion_vinculo("Proyecto acabado-DAMIAN")
