# Plan de implementación en paralelo

Equipo de 5 agentes (D-004). Las tareas detalladas y su estado viven en `cola.md`; este archivo explica **por qué** el orden es este y qué cierra cada ola.

## Idea central: contratos primero, datos después

Lo que bloqueaba el paralelismo era que nadie había definido la lista de partidas ni el formato de los intermedios. Ya están fijados en `specs/` y `Scripts/schemas/`, así que cada agente puede construir su herramienta **contra el contrato** desde el día 1 y conectarla a datos reales cuando el productor publique.

```
             Ola 1 (todos en paralelo)            Ola 2            Ola 3              Ola 4
AG-1  Revit ───── T-101…T-107 ──────────────┐
                                            ├──► CL-1 T-302…T-304 ──► CX-1 T-403 ──► CX-2 T-503 ──► CL-1 T-902/T-903
AG-2  Precios ─── T-201…T-205 ──────────────┤    (Generadores)        (Presupuesto)   (Calendario)    (QA + Resultados)
                                            │         ▲                    ▲               ▲
CL-1  T-301 plantilla+script generadores ───┘         │                    │               │
CX-1  T-401/T-402 plantilla+script presupuesto ───────┼────────────────────┘               │
CX-2  T-501/T-502 estructura+script calendario ───────┴────────────────────────────────────┘
AG-2  T-206 cierra precios faltantes (Ola 2, en paralelo con Generadores)
```

## Ola 0 · Preparación (hecha, T-000)
- Harness, specs SPEC_01–07, schemas Pydantic con `validar.py`, decisiones D-001–D-017, preguntas P-001–P-008 cerradas, status iniciales.
- **Pendiente del usuario:** instalar RevitCortex en ambos equipos (T-003) y preparar PC-B (T-004). Solo AG-1 depende de esto; si RevitCortex aún no está, AG-1 usa pyRevit MCP.
- Reparto por equipos y reglas de sincronización: `specs/SPEC_08_dos_equipos.md`.

## Ola 1 · Paralelo total (5 agentes a la vez)
| Agente | Produce | Cierra cuando |
|---|---|---|
| AG-1 | `intermedios/revit/*.json` + `indice.json` | Todos los vínculos extraídos y validados con `validar.py revit` |
| AG-2 | `pdf/` índices, `precios/insumos_norm.json`, `catalogo_v01.json` | Catálogo validado; cada clave con precio o en `sin_precio`; `mapeo_revit` en las claves con cantidad Revit |
| CX-1 | `Presupuesto/Presupuesto_v00_prueba.xlsm` + script 40 | Plantilla corregida, Carta, AW11=12; el script llena datos de prueba y lee un factor de sobrecosto sin `#DIV/0!` |
| CX-2 | `calendario_v01.json` (estructura) + script 50 | Actividades por capítulo con predecesoras, 100 % por fila, Excel horizontal Carta de prueba |
| CL-1 | Plantilla limpia de generadores + script 30; revisiones | Script probado con un intermedio Revit real o de prueba; revisión de cada entrega en < 1 bloque |

Riesgo principal: que AG-1 (Revit) tarde. Mitigación: AG-2 arranca el catálogo desde la memoria y ajusta `mapeo_revit` cuando aparezca `indice.json`.

## Ola 2 · Cuantificación
- CL-1 aplica `mapeo_revit` a los intermedios de AG-1 → `generadores_v01.json` → `Generadores_v01.xlsx`.
- En paralelo, AG-2 cierra los precios de las claves que sí tienen cantidad (T-206).
- Claves sin cantidad Revit: `MEMORIA:p.NN` o pregunta; nunca a mano sin fuente.

## Ola 3 · Presupuesto y calendario
- CX-1 corre el script 40 con datos reales, recalcula la hoja sobrecosto, lee el factor, publica `presupuesto_v01.json` y el `.xlsm`.
- CX-2 en cuanto existe `presupuesto_v01.json`: cruza importes, avance financiero mensual y acumulado.

## Ola 4 · Integración (CL-1)
- `Scripts/90_qa_cruzado.py`: cantidades presupuesto = generadores; Σ importes = subtotal; Σ calendario = subtotal; 100 % por actividad; toda partida con `fuente`; impresión Carta en las 3 hojas.
- Copia a `Resultados/Generadores_v01.xlsx`, `Presupuesto_v01.xlsm` (y `.xlsx` si se pide), `Calendario_v01.xlsx` y copia fechada en `Resultados/revisiones/23-11-2026/` (o la fecha real).

## Cadencia
- Bloques de 2–4 tareas por sesión (HARNESS.md §6). Al cerrar un bloque: status + log + intermedio validado.
- CL-1 revisa al final de cada bloque de cualquier agente.
- Si un agente falla 3 veces la misma tarea: pregunta en `preguntas.md` y pasa a otra.

## Orden para abrir las terminales
1. **PC-A**: CL-1 (prompt 5) → confirma cola y specs.
2. **PC-B**: prompt 0 (sincronización) en una terminal; espera su reporte OK.
3. **PC-B**: AG-1 (prompt 1) y AG-2 (prompt 2).
4. **PC-B**: CX-1 (prompt 3) y CX-2 (prompt 4) al mismo tiempo: su Ola 1 no depende de nadie.
