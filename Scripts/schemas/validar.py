"""
validar.py — Valida un JSON intermedio contra su schema Pydantic.

Entrada: tipo (revit|precios|generadores|presupuesto|calendario) y ruta del JSON
Salida: código 0 si es válido; 1 y errores en stderr si no.
Dependencias: pydantic>=2 (py -m pip install -r Scripts/requirements.txt)
Fecha: 23-11-2026
Uso:
    py Scripts/schemas/validar.py precios _harness/intermedios/precios/catalogo_v01.json
    py Scripts/schemas/validar.py revit _harness/intermedios/revit/*.json
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from calendario import Calendario  # noqa: E402
from generadores import Generadores  # noqa: E402
from precios import CatalogoPrecios  # noqa: E402
from presupuesto import Presupuesto  # noqa: E402
from pydantic import ValidationError  # noqa: E402
from revit import ExtraccionRevit  # noqa: E402

MODELOS = {
    "revit": ExtraccionRevit,
    "precios": CatalogoPrecios,
    "generadores": Generadores,
    "presupuesto": Presupuesto,
    "calendario": Calendario,
}


def main(argv: list[str]) -> int:
    if len(argv) < 3 or argv[1] not in MODELOS:
        print(__doc__)
        return 2
    modelo = MODELOS[argv[1]]
    archivos = [f for patron in argv[2:] for f in (glob.glob(patron) or [patron])]
    errores = 0
    for f in archivos:
        try:
            modelo.model_validate(json.loads(Path(f).read_text(encoding="utf-8")))
            print(f"OK    {f}")
        except (ValidationError, ValueError, json.JSONDecodeError, FileNotFoundError) as e:
            errores += 1
            print(f"ERROR {f}\n{e}", file=sys.stderr)
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
