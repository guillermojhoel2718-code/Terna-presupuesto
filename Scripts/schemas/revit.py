"""
revit.py — Schema de la extracción Revit (AG-1).

Entrada: JSON en _harness/intermedios/revit/<modelo>__<categoria>.json
Salida: validación (ExtraccionRevit)
Dependencias: pydantic>=2, common.py
Fecha: 23-11-2026
Contrato: _harness/specs/SPEC_03_intermedios.md §1 y SPEC_04_revit.md
"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import Field, model_validator

from common import Base, Fecha


class Cantidades(Base):
    longitud_m: Optional[float] = None
    area_m2: Optional[float] = None
    volumen_m3: Optional[float] = None
    conteo: int = 1
    peso_kg: Optional[float] = None


class ElementoRevit(Base):
    modelo_origen: str = Field(description="Nombre del .rvt de donde viene el elemento (vínculo o archivo)")
    vinculo: Optional[str] = Field(None, description="Nombre de la instancia de vínculo en el federado; None si se leyó directo")
    element_id: int
    unique_id: Optional[str] = None
    categoria: str = Field(description="Categoría Revit en inglés (OST_*) o nombre visible")
    familia: Optional[str] = None
    tipo: Optional[str] = None
    nivel: Optional[str] = None
    material_principal: Optional[str] = None
    cantidades: Cantidades
    parametros_tipo: dict[str, Any] = Field(default_factory=dict)
    parametros_instancia: dict[str, Any] = Field(default_factory=dict)


class ExtraccionRevit(Base):
    modelo: str
    ruta_modelo: str
    categoria: str
    fecha: Fecha
    herramienta: str = Field(description="pyrevit-mcp | pyrevit-agent | pyrevit-run | revitcortex")
    script: str = Field(description="Ruta del script en Scripts/ que generó el archivo")
    unidades: str = "SI (m, m2, m3, kg)"
    total_elementos: int
    elementos: list[ElementoRevit]

    @model_validator(mode="after")
    def _total(self):
        if self.total_elementos != len(self.elementos):
            raise ValueError("total_elementos no coincide con len(elementos)")
        return self
