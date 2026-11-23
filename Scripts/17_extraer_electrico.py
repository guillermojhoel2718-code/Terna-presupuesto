"""
17_extraer_electrico.py — Extracción de elementos del vínculo Instalación Eléctrica (T-107).

Entrada: sesión de Revit 2027 activa con modelo_federado.rvt (vínculo Proyecto electrico_corregido.rvt)
Salida: _harness/intermedios/revit/Proyecto electrico_corregido__<Categoria>.json (25 archivos, schema revit.ExtraccionRevit)
Dependencias: Revit API (Autodesk.Revit.DB), pyrevit agent / pyrevit-mcp (modo query)
Fecha: 23-11-2026 · Dueño: AG-1
Uso:
    pyrevit agent run Scripts/17_extraer_electrico.py --mode=query --engine=cpython --revit=2027
"""
from _revit_extractor_lib import ejecutar_extraccion_vinculo

if __name__ == "__main__" or "__revit__" in dir():
    result = ejecutar_extraccion_vinculo("Proyecto electrico_corregido")
