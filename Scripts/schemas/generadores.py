"""
generadores.py — Schema de generadores por partida (CL-1 en rol AG-3).

Entrada: _harness/intermedios/generadores/generadores_vNN.json
Salida: validación (Generadores)
Dependencias: pydantic>=2, common.py
Fecha: 23-11-2026
Contrato: _harness/specs/SPEC_03_intermedios.md §3
"""
from __future__ import annotations

from typing import Optional

from pydantic import Field, model_validator

from common import Base, Clave, Fecha, Unidad

TOL = 1e-6


class RenglonGenerador(Base):
    localizacion: Optional[str] = Field(None, description="eje / tramo / nivel / local")
    descripcion: Optional[str] = None
    largo: Optional[float] = None
    ancho: Optional[float] = None
    alto: Optional[float] = None
    piezas: float = 1
    adicion: float = 0
    deduccion: float = 0
    parcial: float
    modelo_origen: Optional[str] = None
    element_ids: list[int] = Field(default_factory=list)
    archivo_intermedio: Optional[str] = Field(None, description="JSON de intermedios/revit usado")


class Generador(Base):
    clave: Clave
    concepto: str
    unidad: Unidad
    formula: str = Field(description="ej. 'largo × alto × piezas' o 'Σ area_m2 Revit'")
    renglones: list[RenglonGenerador]
    cantidad_total: float
    fuente: str = Field(description="REVIT:<archivo> | MEMORIA:p.NN | SUPUESTO:<motivo>")

    @model_validator(mode="after")
    def _suma(self):
        s = sum(r.parcial for r in self.renglones)
        if abs(s - self.cantidad_total) > max(TOL, abs(s) * 1e-9):
            raise ValueError(f"{self.clave}: Σparciales {s} ≠ cantidad_total {self.cantidad_total}")
        return self


class Generadores(Base):
    version: str = Field(pattern=r"^v\d{2}$")
    fecha: Fecha
    catalogo_usado: str
    generadores: list[Generador]
    claves_sin_cantidad: list[Clave] = Field(default_factory=list)
