"""
13_extraer_arq_mob.py — Extracción de elementos del vínculo TT-ED-EDU-ARQ-MOB (T-103).

Entrada: sesión de Revit 2027 activa con modelo_federado.rvt (vínculo TT-ED-EDU-ARQ-MOB.rvt)
Salida: _harness/intermedios/revit/TT-ED-EDU-ARQ-MOB__<Categoria>.json (4 archivos, schema revit.ExtraccionRevit)
Dependencias: Revit API (Autodesk.Revit.DB), pyrevit agent / pyrevit-mcp (modo query)
Fecha: 23-11-2026 · Dueño: AG-1
Uso:
    pyrevit agent run Scripts/13_extraer_arq_mob.py --mode=query --engine=cpython --revit=2027
"""
from _revit_extractor_lib import ejecutar_extraccion_vinculo

if __name__ == "__main__" or "__revit__" in dir():
    result = ejecutar_extraccion_vinculo("TT-ED-EDU-ARQ-MOB")
