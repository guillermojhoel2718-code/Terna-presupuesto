"""
12_extraer_estructura.py — Extracción de elementos del vínculo Estructura (T-102).

Entrada: sesión de Revit 2027 activa con modelo_federado.rvt (vínculo Edificio de educacion.rvt)
Salida: _harness/intermedios/revit/Edificio de educacion__<Categoria>.json (9 archivos, schema revit.ExtraccionRevit)
Dependencias: Revit API (Autodesk.Revit.DB), pyrevit agent / pyrevit-mcp (modo query)
Fecha: 23-11-2026 · Dueño: AG-1
Uso:
    pyrevit agent run Scripts/12_extraer_estructura.py --mode=query --engine=cpython --revit=2027
"""
from _revit_extractor_lib import ejecutar_extraccion_vinculo

if __name__ == "__main__" or "__revit__" in dir():
    result = ejecutar_extraccion_vinculo("Edificio de educacion")
