"""
presupuesto.py — Schema del presupuesto (CX-1).

Entrada: _harness/intermedios/presupuesto/presupuesto_vNN.json
Salida: validación (Presupuesto)
Dependencias: pydantic>=2, common.py
Fecha: 23-11-2026
Contrato: _harness/specs/SPEC_03_intermedios.md §4 y SPEC_06_sobrecosto.md
"""
from __future__ import annotations

from pydantic import Field, model_validator

from common import Base, Clave, Fecha, Unidad


class Partida(Base):
    clave: Clave
    capitulo: str
    subcapitulo: str
    concepto: str
    unidad: Unidad
    cantidad: float
    precio_unitario: float = Field(description="P.U. de venta = CD unitario × factor_sobrecosto")
    precio_unitario_cd: float = Field(description="Costo directo unitario de AG-2")
    importe: float
    fuente: str = Field(description="cantidad: <generador> | precio: <fuente AG-2>")

    @model_validator(mode="after")
    def _importe(self):
        esperado = self.cantidad * self.precio_unitario
        if abs(esperado - self.importe) > max(0.01, abs(esperado) * 1e-9):
            raise ValueError(f"{self.clave}: importe {self.importe} ≠ cantidad×PU {esperado}")
        return self


class Sobrecosto(Base):
    """Valores LEÍDOS de la hoja D25-00_Sobrecosto (nunca escritos a mano)."""
    periodo_meses: int = 12
    costo_directo: float
    indirectos: float
    financiamiento: float
    utilidad: float
    cargos_adicionales: float
    precio_venta_sin_iva: float
    factor_sobrecosto: float = Field(description="precio_venta_sin_iva / costo_directo")
    iva_tasa: float
    celdas_origen: dict[str, str] = Field(description="concepto → celda de la hoja sobrecosto")


class Presupuesto(Base):
    version: str = Field(pattern=r"^v\d{2}$")
    fecha: Fecha
    generadores_usados: str
    catalogo_usado: str
    partidas: list[Partida]
    sobrecosto: Sobrecosto
    subtotal: float
    iva: float
    total: float

    @model_validator(mode="after")
    def _totales(self):
        s = sum(p.importe for p in self.partidas)
        if abs(s - self.subtotal) > 0.05:
            raise ValueError(f"subtotal {self.subtotal} ≠ Σimportes {s}")
        if abs(self.subtotal + self.iva - self.total) > 0.05:
            raise ValueError("total ≠ subtotal + iva")
        return self
