# SPEC 01 · Índice de specs y propiedad de archivos

Leer en este orden: `CLAUDE.md` → `AGENTS.md` → `HARNESS.md` → `_harness/decisiones.md` → este archivo → la spec de tu rol.

| Spec | Tema | Lo leen |
|---|---|---|
| SPEC_01 | Índice y propiedad de archivos | todos |
| SPEC_02 | Claves, capítulos, frentes, unidades | todos |
| SPEC_03 | Contratos JSON de intermedios | todos |
| SPEC_04 | Lectura de Revit (MCP, vínculos) | AG-1, CL-1 |
| SPEC_05 | Precios, esquema mixto | AG-2, CL-1 |
| SPEC_06 | Plantilla de presupuesto y sobrecosto | CX-1, CL-1 |
| SPEC_07 | Excel de entrega e impresión Carta | CL-1, CX-1, CX-2 |
| SPEC_08 | Dos equipos: reparto, sincronización OneDrive, git | todos |
| `PLAN_IMPLEMENTACION.md` | Olas de trabajo en paralelo | todos |
| `prompts_agentes.md` | Prompts de arranque de los 5 agentes | usuario |

## 1. Propiedad (un solo escritor por archivo)

Configuración de 5 agentes (D-004): CL-1 asume AG-3.

| Ruta | Dueño |
|---|---|
| `_harness/intermedios/revit/`, `MCP Revit/` (solo notas/config, no tocar `RevitCortex/`) | AG-1 |
| `_harness/intermedios/precios/`, `Catalogo de precios/` | AG-2 |
| `_harness/intermedios/generadores/`, `Generadores/` | CL-1 (rol AG-3) |
| `_harness/intermedios/presupuesto/`, `Presupuesto/` | CX-1 |
| `_harness/intermedios/calendario/`, `Calendario/` | CX-2 |
| `_harness/intermedios/pdf/` | Quien extrae primero el PDF; nombre = PDF sin extensión. No se reescribe |
| `Resultados/`, `_harness/cola.md` (estados `aprobada`/`rechazada`, nuevas tareas), `_harness/decisiones.md`, `_harness/specs/`, `Scripts/schemas/` | CL-1 |
| `_harness/preguntas.md` | Todos **agregan** al final; solo CL-1 cierra preguntas |
| `_harness/cola.md` (cambiar a `en curso` / `bloqueada` / `lista para revisión` solo la línea de tu tarea) | El agente de la tarea |
| `_harness/status/<ID>.md`, `_harness/logs/<ID>-*.md` | Cada agente el suyo |

`cola.md` y `preguntas.md` son compartidos: crear `_harness/locks/<archivo>.lock` antes de editarlos, editar una sola línea/bloque, borrar el lock (HARNESS.md §4).

> **Modo dos equipos vigente (D-014, SPEC_08 §2):** `cola.md` y `preguntas.md` los escribe **solo CL-1**. Los demás agentes reportan estado de tareas y preguntas nuevas en su `status/<ID>.md`. Esta regla manda sobre las dos filas de arriba.

## 2. Rangos de scripts en `Scripts/`

| Rango | Dueño | Ejemplo |
|---|---|---|
| `00–09` + `schemas/` | CL-1 | `05_extraer_pdf_texto.py` |
| `10–19` | AG-1 | `10_extraer_cimentacion_estructura.py` |
| `20–29` | AG-2 | `20_indexar_tabulador_cdmx.py` |
| `30–39` | CL-1 (Generadores) | `30_generadores_desde_revit.py` |
| `40–49` | CX-1 | `40_llenar_plantilla_presupuesto.py` |
| `50–59` | CX-2 | `50_calendario_12_meses.py` |
| `90–99` | CL-1 (QA) | `90_qa_cruzado.py` |

Todos los scripts se corren con `py` desde la raíz del proyecto y son idempotentes.
