# SPEC 06 · Plantilla de presupuesto y hoja de sobrecosto (CX-1)

Plantilla real: `Resources/plantillas_para_usar/Taller Terminal_Presupuesto.xlsm` (CLAUDE.md la llama "taller_terminal_presupuesto"; es este archivo).

## 1. Hojas

| Hoja | Uso |
|---|---|
| `01_Datos Generales` | Proyecto, número `CDC-TTP-26`, revisión, ubicación, superficie (dice 27,000 m²; corregir a 2,500 m² aprox., D-010), periodo = `Sobrecosto!AW11` |
| `D25-00_Resumen` | Resumen por partida (hoy solo "1 ESTACIONAMIENTO", ejemplo). Área de impresión A1:G113, papel A4 |
| `D25-00_Presupuesto` | Renglones: A Partida, B Código, C Descripción, D Unidad, E Cantidad, F P.U., G Importe, H % Inc. F = `J × $J$16` (J = CD unitario, J16 = factor), L = `E × J` (CD por renglón), L16 = `SUBTOTAL(9, L…)` = costo directo |
| `D25-00_Sobrecosto` | Cálculo completo de indirectos (1.1–1.8), financiamiento (2), utilidad (3), cargos adicionales (4), IMSS (5), seguros y fianzas (6). Resumen en filas 198–215 |
| `02_Ref_Datos` | Datos de contratista y cliente |

## 2. Cómo se obtienen los porcentajes

La hoja **no tiene porcentajes fijos**: calcula montos con base en el costo directo (`AW5 = Presupuesto!L16`) y el periodo (`AW11`). Con CD = 0 hoy da `#DIV/0!`. Por eso:

1. Copiar la plantilla (nunca editar la de `Resources/`) a `Presupuesto/Presupuesto_vNN.xlsm` y trabajar ahí.
2. Escribir `AW11 = 12` (D-005). Es un dato del proyecto, no un porcentaje.
3. Llenar renglones de `D25-00_Presupuesto` con cantidades (CL-1) y CD unitario en columna J (AG-2).
4. Recalcular (Excel/LibreOffice headless) y **leer** de la hoja: `AD200` (C.I.), `AD209` (C.F.), `AD210` (C.U.), `AD211` (C.A.), `AW215` (precio de venta), `BE209:BE211` (factores). El factor de sobrecosto = `AW215 / AW5`.
5. Escribir ese factor en `D25-00_Presupuesto!J16` y guardar en `presupuesto_vNN.json → sobrecosto.celdas_origen` de qué celda salió cada valor.
6. Si la hoja requiere iterar (factor depende de CD con sobrecosto), iterar hasta que el factor cambie < 0.0001.

**Prohibido** teclear porcentajes de indirectos/utilidad en otro lado. Los montos de personal, rentas, etc. **se dejan como vienen** en la plantilla (D-013).

Recálculo: Excel está disponible por COM en ambos equipos; CX-1 corre en PC-B (D-014).

## 3. Defectos de la plantilla a corregir en la copia

| Celda | Problema | Acción |
|---|---|---|
| `Sobrecosto!Q9` | `='D25-00_Presupuesto'!#REF!` | Apuntar a `'01_Datos Generales'!D15` (cliente) |
| `Sobrecosto!AW11` | 3 meses | 12 |
| `Resumen!A18` | Partida "ESTACIONAMIENTO" de ejemplo | Reemplazar por los capítulos de SPEC_02 |
| `Presupuesto!A13` | Texto "Nombre de la Obra" | Usar `B10` |
| Todas | Papel A4 o sin definir | Carta (SPEC_07) |
| `01_Datos Generales!D9` | Nombre con typo "Chicimecas" | `Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"` (D-010) |
| `01_Datos Generales!G11` | 27,000 m² (conjunto) | `2,500 m² aprox.` (D-010) |
| `02_Ref_Datos!D9` | Nombre con otra redacción | Igual que D9 (D-010) |

## 4. Recalcular sin abrir Excel a mano

openpyxl **no calcula fórmulas**. Opciones (verificar cuál existe en la máquina antes de usarla y anotarla en el log):
- Excel por COM (PowerShell `New-Object -ComObject Excel.Application`, abrir, `Calculate()`, guardar, cerrar).
- LibreOffice `soffice --headless --convert-to xlsx` para forzar recálculo.

Conservar el `.xlsm` (macros) con `keep_vba=True` si se edita con openpyxl.

## 5. IVA (D-020)

- Tasa **16 %** (`iva_tasa = 0.16`). Se calcula sobre el subtotal = precio de venta sin IVA (`AW215` de la hoja sobrecosto) y se muestra en renglón aparte: SUBTOTAL, IVA 16 %, TOTAL.
- No se mezcla con el factor de sobrecosto ni con los P.U. del renglón.
- `presupuesto_vNN.json`: `iva = subtotal × iva_tasa`, `total = subtotal + iva` (lo valida el schema).
- La leyenda "MÁS EL I.V.A. CORRESPONDIENTE" de la plantilla se sustituye por el desglose; el total en letra va con IVA incluido.
