# CL-1 · Estado
Última actualización: 23-11-2026 · Equipo: PC-A
Tarea actual: T-901 (revisiones) en espera de entregas de PC-B

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-000 | aprobada | specs, schemas, harness | OK |

## Hecho
- T-000: harness, SPEC_01..08, schemas Pydantic + validar.py, decisiones D-001..D-017, preguntas P-001..P-008 cerradas, plan, prompts para dos equipos.
- Scripts/01_preparar_equipo.ps1 (chequeo de equipo) y MCP Revit/instalar_revitcortex.ps1 (instalador con SHA256).
- Repo git: primer commit y push a main (Terna-presupuesto).

## Pendiente
- T-003: el usuario instala RevitCortex (requiere UAC; el agente no tiene permiso de elevar).
- T-301: plantilla y script de generadores.

## Siguiente paso
Esperar reporte del prompt 0 en PC-B (_harness/logs/setup-<PC-B>-*.md) y arrancar T-301.

## Archivos tocados
_harness/*, Scripts/00-09, Scripts/schemas/, MCP Revit/instalar_revitcortex.ps1, AGENTS.md, HARNESS.md
