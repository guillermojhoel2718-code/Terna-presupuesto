"""
calendario.py — Schema del calendario de obra de 12 meses (CX-2).

Entrada: _harness/intermedios/calendario/calendario_vNN.json
Salida: validación (Calendario)
Dependencias: pydantic>=2, common.py
Fecha: 23-11-2026
Contrato: _harness/specs/SPEC_03_intermedios.md §5
"""
from __future__ import annotations

from typing import Optional

from pydantic import Field, model_validator

from common import Base, Clave, Fecha

MESES = 12


class Actividad(Base):
    clave: Clave
    concepto: str
    frente: str = Field(description="Frente de trabajo (ver SPEC_02 §3)")
    mes_inicio: int = Field(ge=1, le=MESES)
    mes_fin: int = Field(ge=1, le=MESES)
    avance_mensual_pct: list[float] = Field(description="12 valores; suma = 100")
    predecesoras: list[Clave] = Field(default_factory=list)
    ruta_critica: bool = False
    importe: Optional[float] = Field(None, description="De presupuesto; None en la versión de estructura")

    @model_validator(mode="after")
    def _reglas(self):
        if self.mes_fin < self.mes_inicio:
            raise ValueError(f"{self.clave}: mes_fin < mes_inicio")
        if len(self.avance_mensual_pct) != MESES:
            raise ValueError(f"{self.clave}: avance_mensual_pct debe tener 12 valores")
        if abs(sum(self.avance_mensual_pct) - 100) > 1e-6:
            raise ValueError(f"{self.clave}: avance suma {sum(self.avance_mensual_pct)} ≠ 100")
        for i, v in enumerate(self.avance_mensual_pct, start=1):
            if v < 0:
                raise ValueError(f"{self.clave}: avance negativo en mes {i}")
            if v > 0 and not (self.mes_inicio <= i <= self.mes_fin):
                raise ValueError(f"{self.clave}: avance en mes {i} fuera de [{self.mes_inicio},{self.mes_fin}]")
        return self


class Calendario(Base):
    version: str = Field(pattern=r"^v\d{2}$")
    fecha: Fecha
    fecha_inicio_obra: Fecha
    duracion_meses: int = MESES
    presupuesto_usado: Optional[str] = None
    actividades: list[Actividad]
    total_importe: Optional[float] = None

    @model_validator(mode="after")
    def _reglas(self):
        claves = {a.clave for a in self.actividades}
        for a in self.actividades:
            for p in a.predecesoras:
                if p not in claves:
                    raise ValueError(f"{a.clave}: predecesora {p} no existe")
        if self.total_importe is not None:
            s = sum(a.importe or 0 for a in self.actividades)
            if abs(s - self.total_importe) > 0.05:
                raise ValueError(f"total_importe {self.total_importe} ≠ Σ {s}")
        return self
