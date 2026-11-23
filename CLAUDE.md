# CLAUDE.md — Centro de Desarrollo Integral, San Luis de la Paz

Este archivo lo leen todos los agentes al iniciar. Junto con `AGENTS.md` (roles) y `_harness/` (estado) define cómo trabajamos.

## 1. Proyecto

Elaborar para un centro de desarrollo integral en San Luis de la Paz, Guanajuato:

1. **Catálogo de generadores**: cuantificación de cada partida, con referencia al plano o elemento de Revit.
2. **Presupuesto**: partidas con precio unitario, sobrecostos y total, siguiendo la plantilla oficial.
3. **Calendario de obra**: ejecución de **1 año**, con las partidas distribuidas en el tiempo.

Entregables: **un archivo Excel por cada uno** (Generadores, Presupuesto, Calendario), configurado para impresión y exportación a PDF. El usuario hará las modificaciones finales y exportará a PDF. Por lo que debe estar configurado en tamaño de impresion en Carta

## 2. Fuentes de verdad

| Prioridad | Fuente | Uso |
|---|---|---|
| 1 | `Memoria arquitectonica descriptiva.pdf` (raíz) | Datos generales del proyecto, programa, integrantes, superficies |
| 1 | `Modelo federado/` (modelos Revit vinculados) | **Única fuente de cantidades.** Se lee con pyRevit CLI |
| 2 | `Resources/` | Apoyo: precios, plantillas, ejemplos. **No es fuente de cantidades** |

Regla: una cantidad que no tenga origen en la fuente 1 o 2 **no se usa**. Si falta un dato, se marca como pendiente en `_harness/preguntas.md`.

## 3. Estructura de carpetas (NO modificar)

La estructura está fijada para encontrar recursos rápido. No renombrar, mover ni crear carpetas de proyecto nuevas fuera de las existentes.

```
Calendario/            Entregable: calendario de obra (1 año)
Catalogo de precios/   Precios unitarios del proyecto
Generadores/           Entregable: generadores por partida
MCP Revit/             Scripts y configuración de lectura Revit (pyRevit CLI)
Modelo federado/       Modelos Revit vinculados (fuente de cantidades)
Presupuesto/           Entregable: presupuesto
Resources/             Recursos de apoyo (no es fuente de cantidades)
  archivos_excel_ejemplos/
  plantillas_para_usar/     Incluye taller_terminal_presupuesto (plantilla y hoja "sobrecosto")
  precios_procesados/       Precios ya procesados (fuente principal de precios)
  referencias_docs/         PDFs de referencia
  resultado_ejemplo_neodata/ PDFs digitales de ejemplo (extraer texto)
Resultados/            Entregables finales y revisiones parciales
Scripts/               Scripts reutilizables (ver sección 6)
CLAUDE.md              Este archivo
AGENTS.md              Roles del equipo de agentes
_harness/              Carpeta de apoyo creada para coordinación (ver HARNESS.md)
```

## 4. Precios

Orden de resolución para cada partida:

1. `Resources/precios_procesados/`: fuente principal.
2. `Catalogo de precios/`: si ya contiene la partida.
3. PDFs de `Resources/referencias_docs/` y `resultado_ejemplo_neodata/`: como referencia para validar o completar.
4. Si nada de lo anterior existe: usar un **aproximado conservador** (que no eleve el precio por encima de la referencia más baja disponible) y marcarlo como `SUPUESTO` con justificación en la columna de fuente.

Nunca inventar precios sin marca. Nunca subir un precio "por seguridad".

**Indirectos, sobrecosto, financiamiento, utilidad e IVA**: tomar los porcentajes de la hoja **"sobrecosto"** del archivo `taller_terminal_presupuesto` en `Resources/plantillas_para_usar/`. No escribir porcentajes a mano en otros lugares.

## 5. Revit (versión 2027)

- Usar **pyRevit CLI** para leer tablas de planificación y parámetros sin abrir la interfaz de Revit cuando sea posible.
- Antes de usar un comando, verificarlo con `pyrevit --help` en la instalación real. No asumir sintaxis. El archivo solo tiene vinculos por lo que se tiene que tener esta consideracion
- Modo por defecto: **solo lectura**. Escribir en Revit únicamente si el usuario lo pide explícitamente por escrito. Si es necesario para tener persistencia si se puede escribir.
- Nunca guardar ni sincronizar modelos de `Modelo federado/`. A menos que sea necesario
- Cada cantidad extraída guarda su origen: archivo `.rvt`, ID del elemento o nombre de la planificación.

## 6. Scripts y reutilización

- Antes de escribir una extracción, revisar `Scripts/`, `MCP Revit/` y `_harness/intermedios/`. Si ya existe, **reutilizarla**. No empezar desde cero.
- Nombre de scripts: `NN_nombre_descriptivo.py` (ej. `01_extraer_planificacion_muros.py`).
- Cada script incluye en su encabezado: entrada, salida, dependencias y fecha.
- Scripts **idempotentes**: correrlos dos veces produce el mismo resultado.
- Modelos de datos con **Pydantic** en `Scripts/schemas/`. Toda salida intermedia (JSON) se valida contra su schema antes de pasar a otro agente.
- Extracción de PDFs: los PDFs son digitales, usar extracción de texto (pdfplumber o PyMuPDF). Dividir en chunks por página o sección cuando el documento sea grande. Guardar el texto extraído en `_harness/intermedios/pdf/` para no volver a extraerlo.

## 7. Convenciones de datos

- Unidades: m, m², m³, pza, kg, ton. Moneda: MXN. Fechas en formato (DD-MM-AAAA).
- Cada partida lleva los campos: `clave`, `concepto`, `unidad`, `cantidad`, `precio_unitario`, `importe`, `fuente` (Revit ID / plano / precio ID / SUPUESTO).
- No redondear antes de totalizar. Redondear solo en presentación.
- Claves de partida: un solo formato en todo el proyecto. Definirlo en el catálogo y no cambiarlo después.

## 8. Entregables

- Un Excel por entregable, en `Resultados/`:
  - `Generadores_vNN.xlsx`
  - `Presupuesto_vNN.xlsx`
  - `Calendario_vNN.xlsx`
- Cada Excel configurado para imprimir: área de impresión definida, ajuste a 1 página de ancho, encabezado con proyecto, fecha, versión y responsable.
- Incrementar `vNN` en cada entrega. No sobrescribir versiones anteriores.
- Revisiones parciales: el integrador deja copias en `Resultados/revisiones/` con fecha.

## 9. Reglas de trabajo

- Cada agente escribe **solo en su carpeta o archivo asignado** (ver `AGENTS.md`).
- Nunca editar un archivo que esté asignado a otro agente.
- No borrar archivos de otros agentes ni de `Resources/`.
- Si algo no está claro, escribir la duda en `_harness/preguntas.md` y continuar con lo que sí está claro. No inventar.
- Al terminar cada paso, actualizar `_harness/status/<agente>.md` (ver `HARNESS.md`).
