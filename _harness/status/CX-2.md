# CX-2 · Estado
Última actualización: 26-11-2026 · Equipo: PC-B
Tarea actual: T-503 en espera de aprobación del presupuesto

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-501 | lista para revisión | `_harness/intermedios/calendario/calendario_v01.json` | 12 meses, fecha 04-01-2027, frentes y predecesoras según SPEC_02; schema OK |
| T-502 | lista para revisión | `Scripts/50_calendario_12_meses.py`; `Calendario/Calendario_v01.xlsx` | Excel Carta horizontal, 1 página de ancho; schema OK |
| T-503 | lista para revisión | `_harness/intermedios/calendario/calendario_v02.json`; `Calendario/Calendario_v02.xlsx` | OK validar.py; subtotal = presupuesto v01 |

## Preguntas nuevas
- Ninguna. La ausencia del presupuesto y de las fuentes visuales se reporta como dependencia, sin crear partidas ni importes.

## Hecho
- Leídos en el orden pedido CLAUDE.md, AGENTS.md, HARNESS.md, decisiones, SPEC_01, SPEC_02, SPEC_03, SPEC_07, SPEC_08, este status y cola (solo lectura).
- Verificados `calendario_v01.json` y `calendario_v02.json` con el schema calendario: ambos OK. `py` no detecta Python en este equipo; validación realizada con Python 3.11.9 por ruta absoluta.
- v02 permanece provisional por la entrega anterior; no contiene presupuesto ni importes.

## Pendiente
- T-503: esperar que CL-1 marque aprobado el presupuesto v01 en cola.md y verificar status de CX-1 antes de abrir el intermedio. Luego asignar cada clave presupuestal a su ventana constructiva, calcular avance financiero mensual/acumulado y comprobar suma contra subtotal.
- La copia actual no contiene `Resources/resultado_ejemplo_neodata/`, `Resources/referencias_docs/` ni `_harness/intermedios/pdf/memoria_arquitectonica.txt`; duraciones siguen provisionales.

## Observador
- `Scripts/51_calendario_v02.py --watch` está activo con Python 3.11 (sesión de ejecución 29498).
- Requiere simultáneamente `_harness/intermedios/presupuesto/presupuesto_v01.json` y `T-403 | ... | estado: aprobada` en `cola.md`. Solo entonces integra presupuesto, genera v02, ejecuta `validar.py calendario` y actualiza este status.
- El observador se inició sin regenerar el entregable provisional; queda a la escucha de ambas condiciones.

## Siguiente paso
Mantener el observador activo hasta que aparezcan ambas condiciones; revisar la validación y resultado al completar T-503.

## Archivos tocados en esta actualización
`_harness/status/CX-2.md`; `_harness/logs/CX-2-26-11-2026.md`

## T-503 · Cierre automático
- Presupuesto: `_harness/intermedios/presupuesto/presupuesto_v01.json` aprobado por CL-1 en T-403.
- Generada secuencia provisional de 12 meses (enero–diciembre 2027) con importes y avance financiero.
- Intermedio validado con Scripts/schemas/validar.py calendario.
