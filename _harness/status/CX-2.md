# CX-2 · Estado
Última actualización: 23-11-2026 02:48 · Equipo: PC-B
Raíz de trabajo: C:\Users\kukle\OneDrive - Instituto Politecnico Nacional\Taller Terminal - Taller Terminal 1\Presupuestos taller terminal
Tarea actual: T-501/T-502 (estructura provisional lista para revisión)

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-501 | lista para revisión · estructura por capítulo/frente | `_harness/intermedios/calendario/calendario_v01.json` | Schema OK; duraciones propuestas con secuencia constructiva de SPEC_02 y contexto arquitectónico disponible |
| T-502 | lista para revisión · estructura sin importes | `Scripts/50_calendario_12_meses.py`; `Calendario/Calendario_v01.xlsx` | Schema OK; Carta horizontal, 1 página de ancho, A1:T20 |
| T-503 | pendiente | — | Espera T-403 aprobado; cola y archivos del catálogo/presupuesto siguen pendientes/ausentes |

## Preguntas nuevas
- Memoria pp. 4-10 aporta programa espacial, materialidad, varios volúmenes y niveles (incluida planta alta educativa aprox. +8.80 m), pero no especifica duraciones constructivas. Las ventanas por capítulo siguen siendo propuesta preliminar de programación para cumplir D-012; requieren revisión de CL-1.
- `catalogo_v01.json` aún no está publicado (cola: T-204/T-205 pendientes). Claves `ED-CC-99-001` se conservan solo como marcadores temporales, no son claves definitivas.

## Hecho
- Base de trabajo cambiada a la raíz real de OneDrive indicada por el usuario.
- Migrados sin colisión, archivo por archivo con `.tmp` y renombrado: `Scripts/50_calendario_12_meses.py`, `_harness/intermedios/calendario/calendario_v01.json`, `Calendario/Calendario_v01.xlsx`.
- Verificadas legibilidad completa de plantilla, PDF ejemplo y memoria; no se reconstruyeron fuentes.
- T-501 estructura preliminar: F1 (01→02→03/05 por niveles), F2 (04 tras 03), F3 (08-10 coordinadas con 05/06), F4 (06/07 tras cubierta), F5 (13/14 al cierre). Capítulos 11-12 excluidos conforme D-016.
- T-502 generado/validado con Python 3.11.9 absoluto: `C:\Users\kukle\AppData\Local\Programs\Python\Python311\python.exe`. El CPM considera lags derivados de ventanas mensuales para modelar solapes entre frentes/niveles.
- Fuente de programa: PDF de 22 páginas de obra distinta (portones Xochimilco, 90 días). Usado solo como referencia de presentación por concepto/periodo; no se copiaron fechas, duración ni importes.

## Pendiente
Ajustar estructura y sustituir claves cuando AG-2 publique catálogo v01. Incorporar importes y avance financiero únicamente cuando T-403 esté aprobado; no iniciar T-503 antes. Revisar con CL-1 las duraciones, ya que la memoria no ofrece un programa cuantificado.

## Siguiente paso
Esperar publicación de catalogo_v01.json y aprobación de presupuesto_v01.json; entonces actualizar calendario por clave definitiva y completar T-503.

## Archivos tocados en OneDrive
`Scripts/50_calendario_12_meses.py`; `_harness/intermedios/calendario/calendario_v01.json`; `Calendario/Calendario_v01.xlsx`; `_harness/status/CX-2.md`; `_harness/logs/CX-2-23-11-2026.md`.