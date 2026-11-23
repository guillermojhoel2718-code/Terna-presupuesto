# CX-2 · Estado
Última actualización: 23-11-2026 03:14 · Equipo: PC-B
Raíz de trabajo: C:\Users\kukle\OneDrive - Instituto Politecnico Nacional\Taller Terminal - Taller Terminal 1\Presupuestos taller terminal
Tarea actual: T-501/T-502 · correcciones CL-1

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-501 | lista para revisión · corregida | `_harness/intermedios/calendario/calendario_v01.json` | 65/65 claves catálogo, JSON schema OK, CPM adelante/atrás |
| T-502 | lista para revisión · PDF COM verificado | `Scripts/50_calendario_12_meses.py`; `Calendario/Calendario_v01.xlsx`; `_harness/intermedios/calendario/Calendario_v01_revision.pdf` | Excel COM: PDF revisado, columnas completas |
| T-503 | pendiente | script `Scripts/51_calendario_financiero.py` en preparación | No iniciar hasta que cola marque T-403 aprobado |

## Preguntas nuevas
- Generadores_v01.json aún no está disponible/aprobado; no hay cantidad por clave para calcular duraciones ni rendimiento de cuadrilla por unidad. Se mantienen ventanas temporales SUPUESTO y el criterio Q/(rendimiento × cuadrillas × jornadas/mes) en Excel/Pendientes.
- Catálogo v01 está publicado y valida, pero cola/status AG-2 lo mantienen en revisión; se adoptaron sus 65 claves para la revisión solicitada. Confirmar aprobación de CL-1 antes de etiquetarlas como definitivas.

## Hecho
- Raíz OneDrive actual y fuente de Python absoluta mantenidas; cero escrituras al worktree.
- Punto 1: CPM forward/backward sobre 65 actividades con vínculos FS y SS/lag documentados. Total float en meses añadido a Excel. 40/65 críticas, 25 con holgura positiva; F3 instalaciones tiene float.
- Punto 2: duraciones no presentadas como definitivas; marcadas SUPUESTO por capítulo, criterio calculable y hoja `Pendientes`. Programa abarca enero-diciembre 2027 y 12 meses exactos. Índice estructural confirma 4 bandas funcionales (+5.30,+8.80,+12.30,cubierta +13.80/+14.80 agrupada), excluyendo dalas auxiliares. D-010: ~2,500 m².
- Punto 3: Excel abierto en solo lectura con Excel COM y exportado a PDF de 5 páginas en intermedios; Carta (paper=1), apaisado, FitToWidth=1, fecha DD-MM-AAAA visible, encabezado y columnas hasta Vínculo CPM presentes. Libro y Excel cerrados en finally. PDF revisado, columnas no cortadas. `\_harness/intermedios/calendario/Calendario_v01_revision.pdf`.
Punto 4: sustituidas claves temporales por las 65 claves del catálogo v01 publicado (pendiente aprobación de CL-1).
- JSON de calendario regenerado y validado con schema.

## Pendiente
Preparar script T-503 con prueba sintética de igualdad subtotal y dejar T-503 sin ejecutar.

## Siguiente paso
Cerrar puntos 3 y 5, documentar resultados, esperar T-302/T-303 (generadores) para recalcular Q/rendimiento y aprobación CL-1 del catálogo.

## Archivos tocados
`Scripts/50_calendario_12_meses.py`; `_harness/intermedios/calendario/calendario_v01.json`; `Calendario/Calendario_v01.xlsx`; `_harness/status/CX-2.md`; `_harness/logs/CX-2-23-11-2026.md`.