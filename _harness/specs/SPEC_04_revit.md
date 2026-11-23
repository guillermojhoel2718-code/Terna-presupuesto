# SPEC 04 · Lectura de Revit (AG-1)

Verificado en esta máquina el 23-11-2026.

## 1. Entorno real

| Elemento | Estado |
|---|---|
| Revit 2027 | Instalado, `C:\Program Files\Autodesk\Revit 2027\` (27.0.4) |
| pyRevit | 7.0.0, clon `master`, **adjunto a Revit 2027** |
| pyRevit MCP (`pyrevit mcp`) | **Registrado** en la config de Claude Code como servidor `pyrevit`. Herramientas: `get_context`, `run_query`, `inspect_elements`, `navigate_revit_link`, `get_skill("scheduling")`… |
| pyRevit CLI agent | `pyrevit agent run <script.py> --mode=query --revit=2027 --inputs=<json>` (mismo motor que el MCP, para agentes sin MCP: Antigravity/Codex) |
| RevitCortex v1.0.50 | **MCP preferente** (D-009). Instalar en cada equipo con `MCP Revit/instalar_revitcortex.ps1` (Revit cerrado; usa el ZIP verificado por SHA256 de `MCP Revit/instalador/`). Después, en Revit: pestaña RevitCortex → **Cortex Switch** para encender el servidor. Herramientas útiles: `get_linked_file_instances`, `get_linked_elements`, `get_material_quantities`, `get_schedule_data`, `export_elements_data`. Activar modo solo lectura en Settings. El código fuente en `MCP Revit/RevitCortex/` es solo referencia. |
| Python local | Usar `py` (el comando `python` es el alias de Microsoft Store y falla). Paquetes: `py -m pip install -r Scripts/requirements.txt` |

**Requisito:** el MCP y `pyrevit agent` hablan con una sesión de Revit **abierta**. Por D-014, la sesión de Revit con el federado está en **PC-B**, donde corre AG-1. Comprobar con `pyrevit agent status` o `list_revit_instances`. PC-A no abre el federado (evita dos copias locales del mismo .rvt sincronizándose).

## 2. Modelo federado

- Archivo vigente: `Modelo federado/modelo_federado.rvt`. Los `.0001/.0002/.0003.rvt` son **copias de respaldo de Revit**: ignorarlas.
- Vínculos (TransmissionData, rutas relativas `..\..\Archivos revit\` = `Taller Terminal - Taller Terminal\Archivos revit\`):

| Vínculo | Capítulos |
|---|---|
| `Estructura_2027\00_ Edificio de educacion\Edificio de educacion.rvt` | 02, 03, 04 |
| `Acabados_2027\theriam\Proyecto acabado-DAMIAN.rvt` | 06 |
| `Herrería y Cancelería_2027\TT_ED_EDUCACIÓN_CANCELERIA_2027.rvt` | 07 |
| `Instalacion IHS_2027\Instalaciones.rvt` | 08, 09 |
| `TT-ED-EDU-ARQ-MOB.rvt` | 01, 05, 13 |
| `Instalacion Electrica_2027\Copias de seguridad\Proyecto electrico_corregido.rvt` (vinculado 23-11-2026, D-008) | 10 |

- **Solo se leen los 6 vínculos.** No se abre ningún RVT fuera del federado: Instalaciones Especiales queda fuera de alcance (D-016) y la albañilería sale de ARQ-MOB (D-017).
- Comprobar en cualquier equipo que los vínculos existan localmente: `Scripts/01_preparar_equipo.ps1`.

## 3. Cómo extraer

1. `get_context` → confirmar documento activo = `modelo_federado`.
2. `get_skill("revit-scripting")` y `get_skill("scheduling")` antes del primer script.
3. Para cada vínculo: `navigate_revit_link` o, en script, `FilteredElementCollector(doc, RevitLinkInstance)` → `link.GetLinkDocument()` → colectar por categoría en el documento vinculado. Registrar `vinculo` = nombre de la instancia.
4. Cantidades: parámetros integrados (`HOST_AREA_COMPUTED`, `HOST_VOLUME_COMPUTED`, `CURVE_ELEM_LENGTH`, `STRUCTURAL_*`) convertidos a SI con `UnitUtils.ConvertFromInternalUnits`.
5. Si el modelo tiene **planificaciones** (schedules) útiles, exportarlas también (`get_schedule_data` / `ViewSchedule`) como respaldo; la fuente preferida es el elemento.
6. Escribir el JSON desde el script (la salida del run) a `_harness/intermedios/revit/` y validar.

Scripts en `Scripts/10_*.py … 19_*.py` (rango de AG-1). Encabezado obligatorio: entrada, salida, dependencias, fecha.

## 4. Reglas

- Modo `query` (solo lectura). Nunca `run_modify`, `save_document`, ni sincronizar. No escribir en los vínculos.
- **Solo AG-1 toca Revit.** Si otro agente necesita un dato, lo pide en `preguntas.md`.
- Si un vínculo no carga (ruta rota), anotarlo en `preguntas.md` con la ruta que Revit reporta y seguir con los demás.
- Unidades del proyecto pueden estar en cm/mm: siempre convertir desde unidades internas, nunca desde el texto mostrado.
