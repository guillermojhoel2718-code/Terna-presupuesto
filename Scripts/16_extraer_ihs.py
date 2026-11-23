"""
16_extraer_ihs.py — Extracción de elementos del vínculo Instalación IHS (T-106).

Entrada: sesión de Revit 2027 activa con modelo_federado.rvt (vínculo Instalaciones.rvt)
Salida: _harness/intermedios/revit/Instalaciones__<Categoria>.json (7 archivos, schema revit.ExtraccionRevit)
Dependencias: Revit API (Autodesk.Revit.DB), pyrevit agent / pyrevit-mcp (modo query)
Fecha: 23-11-2026 · Dueño: AG-1
Uso:
    pyrevit agent run Scripts/16_extraer_ihs.py --mode=query --engine=cpython --revit=2027
"""
from _revit_extractor_lib import ejecutar_extraccion_vinculo

if __name__ == "__main__" or "__revit__" in dir():
    result = ejecutar_extraccion_vinculo("Instalaciones")
