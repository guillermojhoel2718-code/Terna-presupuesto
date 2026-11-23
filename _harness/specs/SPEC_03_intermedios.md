# SPEC 03 · Contratos de intermedios (quién produce qué)

Todo intermedio es JSON UTF-8, se valida antes de marcar la tarea como `lista para revisión`:

```powershell
py Scripts/schemas/validar.py <tipo> <archivo.json>
```

| # | Productor | Archivo | Schema (`Scripts/schemas/`) | Consumidores |
|---|---|---|---|---|
| 1 | AG-1 | `_harness/intermedios/revit/<modelo>__<categoria>.json` (un archivo por modelo y categoría) + `revit/indice.json` | `revit.py · ExtraccionRevit` | CL-1 (Generadores), AG-2 (para conocer tipos/materiales) |
| 2 | AG-2 | `_harness/intermedios/precios/catalogo_vNN.json` | `precios.py · CatalogoPrecios` | CL-1, CX-1, CX-2 |
| 3 | CL-1 (rol AG-3) | `_harness/intermedios/generadores/generadores_vNN.json` | `generadores.py · Generadores` | CX-1 |
| 4 | CX-1 | `_harness/intermedios/presupuesto/presupuesto_vNN.json` | `presupuesto.py · Presupuesto` | CX-2, CL-1 |
| 5 | CX-2 | `_harness/intermedios/calendario/calendario_vNN.json` | `calendario.py · Calendario` | CL-1 |
| — | CL-1 | `_harness/intermedios/pdf/*.txt` (texto extraído de PDFs, por página) | — | todos |

## 1. Revit (AG-1)

- Nombre: `<modelo_sin_extension>__<Categoria>.json`, p. ej. `Edificio de educacion__StructuralFoundation.json`.
- `revit/indice.json`: lista de archivos generados con modelo, categoría, total de elementos, fecha y script. Formato libre pero estable; CL-1 lo usa para saber qué hay.
- Cantidades en SI (m, m², m³, kg). Revit trabaja en pies internamente: convertir con `UnitUtils`.
- `peso_kg` solo para acero cuando el tipo tenga peso/longitud.

## 2. Catálogo de precios (AG-2)

- Un `Concepto` por partida, con `clave`, `unidad`, `precio_unitario` (costo directo), `fuente_tipo`, `fuente_ref`.
- **`mapeo_revit`**: la regla que dice qué elementos Revit alimentan la partida (categoría + regex de tipo + campo de cantidad). Es el puente entre AG-1 y Generadores, y permite que AG-1 y AG-2 trabajen en paralelo.
- `precio_unitario: null` está permitido en versiones intermedias; la clave va en `resumen.sin_precio`.

## 3. Generadores (CL-1)

- Un `Generador` por clave del catálogo. Cada renglón cita `element_ids` y `archivo_intermedio` o, si no hay Revit, `fuente: MEMORIA:p.NN` o `SUPUESTO:<motivo>`.
- Partidas sin Revit (`sin_cantidad_revit`, p. ej. limpieza): renglones capturados por CL-1 en `_harness/intermedios/generadores/manual.json` (`{"generadores": [Generador…]}`), cada uno con fuente `MEMORIA:p.NN` o `SUPUESTO:<motivo>`.
- `reporte_vNN.md` acompaña cada versión: claves sin cantidad, posibles dobles conteos, elementos Revit sin asignar y avisos de unidad.
- `cantidad_total = Σ parcial` (lo valida el schema). Sin factores de desperdicio en la cantidad: el desperdicio va en el APU.

## 4. Presupuesto (CX-1)

- `precio_unitario_cd` de AG-2; `precio_unitario` = CD × `factor_sobrecosto` leído de la hoja (ver SPEC_06).
- `importe = cantidad × precio_unitario` (lo valida el schema). No redondear antes de totalizar.

## 5. Calendario (CX-2)

- Una `Actividad` por clave (o por subcapítulo si CL-1 lo aprueba). 12 valores de avance que suman 100, solo dentro de `[mes_inicio, mes_fin]`.
- Versión de estructura (`importe: null`) permitida desde el día 1; la versión final toma importes de `presupuesto_vNN.json` y `total_importe` debe igualar su `subtotal`.

## 6. Versionado

`vNN` empieza en `v01`. Nunca se sobrescribe un intermedio ya `aprobado`: se crea `vNN+1`. Los JSON en curso pueden reescribirse por su único dueño.
