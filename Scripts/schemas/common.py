"""
common.py — Tipos compartidos por todos los schemas del proyecto.

Entrada: ninguna (módulo de tipos).
Salida: tipos Pydantic reutilizables (Clave, Unidad, FuenteTipo, ...).
Dependencias: pydantic>=2
Fecha: 23-11-2026
Dueño: CL-1 (otros agentes proponen cambios en _harness/preguntas.md).

Contrato descrito en _harness/specs/SPEC_02_claves_y_partidas.md y SPEC_03_intermedios.md.
"""
from __future__ import annotations

import re
from enum import Enum
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict

# --------------------------------------------------------------------------
# Clave de partida: ED-CC-SS-NNN  (ver SPEC_02)
#   ED  = bloque (Edificio de educación). Reservado para otros bloques: SC, CD, AS.
#   CC  = capítulo 01..99
#   SS  = subcapítulo 01..99
#   NNN = concepto 001..999
# --------------------------------------------------------------------------
CLAVE_RE = re.compile(r"^(ED|SC|CD|AS)-\d{2}-\d{2}-\d{3}$")
CAPITULO_RE = re.compile(r"^\d{2}$")
FECHA_RE = re.compile(r"^\d{2}-\d{2}-\d{4}$")  # DD-MM-AAAA


def _check_clave(v: str) -> str:
    if not CLAVE_RE.match(v):
        raise ValueError(f"clave '{v}' no cumple el formato ED-CC-SS-NNN")
    return v


def _check_fecha(v: str) -> str:
    if not FECHA_RE.match(v):
        raise ValueError(f"fecha '{v}' debe ser DD-MM-AAAA")
    return v


Clave = Annotated[str, AfterValidator(_check_clave)]
Fecha = Annotated[str, AfterValidator(_check_fecha)]


class Unidad(str, Enum):
    m = "m"
    m2 = "m2"
    m3 = "m3"
    pza = "pza"
    kg = "kg"
    ton = "ton"
    lote = "lote"   # solo partidas globales (limpieza, trámites); justificar en fuente
    salida = "salida"  # instalaciones (salida eléctrica/hidráulica)
    jgo = "jgo"
    lt = "lt"
    hr = "hr"
    jor = "jor"


# Normalización de unidades de los CSV de Resources/precios_procesados
UNIDAD_ALIAS = {
    "ml": "m", "m.l.": "m", "mts": "m", "m²": "m2", "m³": "m3",
    "pieza": "pza", "pz": "pza", "pzas": "pza", "lote": "lote", "lot": "lote",
    "kg.": "kg", "tonelada": "ton", "litro": "lt", "l": "lt", "jor.": "jor",
}


def normalizar_unidad(u: str) -> str:
    u2 = (u or "").strip().lower()
    return UNIDAD_ALIAS.get(u2, u2)


class FuenteTipo(str, Enum):
    REVIT = "REVIT"                     # elemento/planificación de Revit
    PRECIOS_PROCESADOS = "PRECIOS_PROCESADOS"
    CATALOGO = "CATALOGO"               # Catalogo de precios/
    TABULADOR_CDMX = "TABULADOR_CDMX"   # referencias_docs/tabulador...2026.pdf
    NEODATA = "NEODATA"                 # resultado_ejemplo_neodata/
    REF_XALAPA = "REF_XALAPA"           # referencias_docs/PRESUPUESTO ... XALAPA
    APU = "APU"                         # análisis armado desde insumos
    MEMORIA = "MEMORIA"                 # Memoria arquitectonica descriptiva.pdf
    SUPUESTO = "SUPUESTO"               # aproximado conservador, requiere justificación


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
