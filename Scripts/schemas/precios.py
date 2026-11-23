"""
precios.py — Schema del catálogo de conceptos y precios (AG-2).

Entrada: _harness/intermedios/precios/catalogo_vNN.json
Salida: validación (CatalogoPrecios)
Dependencias: pydantic>=2, common.py
Fecha: 23-11-2026
Contrato: _harness/specs/SPEC_02_claves_y_partidas.md y SPEC_05_precios.md
"""
from __future__ import annotations

from typing import Optional

from pydantic import Field, model_validator

from common import Base, Clave, Fecha, FuenteTipo, Unidad


class InsumoAPU(Base):
    codigo: str = Field(description="codigo del CSV de precios_procesados o del PDF")
    descripcion: str
    tipo: str = Field(description="material | mano_obra | equipo | herramienta | basico")
    unidad: str
    cantidad: float = Field(description="rendimiento / consumo por unidad de concepto")
    precio: float
    importe: float
    fuente: str


class MapeoRevit(Base):
    """Regla para que CL-1/AG-3 sepa qué elementos Revit alimentan el concepto."""
    categoria: str = Field(description="Categoría Revit (ej. Walls, Floors, Structural Foundation)")
    filtro_tipo: Optional[str] = Field(None, description="regex sobre familia/tipo/material")
    campo_cantidad: str = Field(description="longitud_m | area_m2 | volumen_m3 | conteo | peso_kg")
    factor: float = Field(1.0, description="factor de conversión (ej. kg/m de perfil, desperdicio NO)")
    modelo: Optional[str] = None


class Concepto(Base):
    clave: Clave
    capitulo: str
    subcapitulo: str
    concepto: str = Field(description="Descripción completa, estilo Neodata: '..., incluye: ...'")
    unidad: Unidad
    precio_unitario: Optional[float] = Field(None, description="Costo directo unitario, MXN, sin sobrecosto")
    fuente_tipo: Optional[FuenteTipo] = None
    fuente_ref: Optional[str] = Field(None, description="código/página/archivo exacto de la fuente")
    fecha_fuente: Optional[str] = None
    justificacion: Optional[str] = Field(None, description="Obligatoria si SUPUESTO o APU")
    apu: list[InsumoAPU] = Field(default_factory=list)
    mapeo_revit: list[MapeoRevit] = Field(default_factory=list)
    sin_cantidad_revit: bool = Field(False, description="True si la cantidad no sale de Revit (ej. limpieza, trazo)")

    @model_validator(mode="after")
    def _reglas(self):
        if self.precio_unitario is not None:
            if self.precio_unitario < 0:
                raise ValueError(f"{self.clave}: precio negativo")
            if self.fuente_tipo is None or not self.fuente_ref:
                raise ValueError(f"{self.clave}: precio sin fuente_tipo/fuente_ref")
        if self.fuente_tipo in (FuenteTipo.SUPUESTO, FuenteTipo.APU) and not self.justificacion:
            raise ValueError(f"{self.clave}: SUPUESTO/APU requiere justificacion")
        if self.fuente_tipo == FuenteTipo.APU and not self.apu:
            raise ValueError(f"{self.clave}: fuente APU sin insumos")
        return self


class ResumenCatalogo(Base):
    total_conceptos: int
    con_precio: int
    sin_precio: list[Clave]
    supuestos: list[Clave]


class CatalogoPrecios(Base):
    version: str = Field(pattern=r"^v\d{2}$")
    fecha: Fecha
    alcance: str = "Edificio de educación (vínculos del modelo federado)"
    conceptos: list[Concepto]
    resumen: ResumenCatalogo

    @model_validator(mode="after")
    def _unicos(self):
        claves = [c.clave for c in self.conceptos]
        dup = {c for c in claves if claves.count(c) > 1}
        if dup:
            raise ValueError(f"claves duplicadas: {sorted(dup)}")
        if self.resumen.total_conceptos != len(self.conceptos):
            raise ValueError("resumen.total_conceptos no cuadra")
        return self
