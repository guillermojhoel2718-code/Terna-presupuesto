# SPEC 07 · Excel de entrega e impresión

Aplica a Generadores, Presupuesto y Calendario. CL-1 lo verifica antes de copiar a `Resultados/`.

## 1. Configuración obligatoria (openpyxl)

```python
ws.page_setup.paperSize = ws.PAPERSIZE_LETTER      # 1 = Carta (D-006)
ws.page_setup.orientation = "portrait"             # Calendario: "landscape"
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0                      # 0 = las páginas que hagan falta a lo alto
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.print_area = "A1:N<ultima_fila>"
ws.print_title_rows = "1:<fila_encabezado_tabla>"  # repetir encabezado
ws.page_margins.left = ws.page_margins.right = 0.5   # pulgadas
ws.page_margins.top = 0.75; ws.page_margins.bottom = 0.75
ws.oddHeader.center.text = 'Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"'   # D-010
ws.oddHeader.right.text  = "Versión vNN · &D"
ws.oddFooter.left.text   = "Responsable: <agente/usuario>"
ws.oddFooter.right.text  = "Página &P de &N"
```

Encabezado con **proyecto, fecha, versión y responsable** (CLAUDE.md §8). Fechas visibles en DD-MM-AAAA.

## 2. Por entregable

| Entregable | Base | Orientación | Notas |
|---|---|---|---|
| `Generadores_vNN.xlsx` | `plantilla_base_archivo _de_generadores.xlsx` (hojas PRE, CIM, EST con formato "HOJA DE CUANTIFICACIÓN CALCULADORA") | Horizontal | La plantilla trae datos de **otro proyecto** (hospital 34 camas, Tepotzotlán, nombre de alumno): limpiar todo. Una hoja por capítulo, un bloque por clave. Columna de referencia Revit (modelo + IDs) agregada a la derecha dentro del área de impresión. Clave de la plantilla `="URG-"&…` se reemplaza por la clave `ED-CC-SS-NNN` |
| `Presupuesto_vNN.xlsm` | `Taller Terminal_Presupuesto.xlsm` | Vertical | Ver SPEC_06. Si se pide `.xlsx`, guardar también sin macros |
| `Calendario_vNN.xlsx` | Nuevo (referencia visual `12 PROGRAMA DE OBRA.pdf`) | Horizontal | Columnas: clave, concepto, frente, importe, 12 meses (barra con relleno + % y monto mensual), fila de avance financiero mensual y acumulado. Ruta crítica en color distinto |

## 3. Formato numérico

- Cantidades `#,##0.00`; precios e importes `$#,##0.00`; porcentajes `0.00%`.
- Totales con fórmulas (`SUM`) para que el usuario pueda editar; no pegar valores en los totales.
- No redondear con `ROUND` dentro de los cálculos; solo formato de celda.

## 4. OneDrive

- La plantilla de generadores está **solo en la nube** (atributo O). Antes de leerla: "Mantener siempre en este dispositivo" o copiarla.
- La plantilla de presupuesto dio "Permission denied" al abrirla directo (probablemente abierta en Excel). Leerla copiándola primero a un temporal.
- Cerrar el libro (Excel COM) siempre en `finally`, para no dejar locks de OneDrive.
