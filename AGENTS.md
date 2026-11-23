# AGENTS.md — Equipo de agentes

Lee primero `CLAUDE.md`. Este archivo define quién hace qué. Si tu rol no está aquí, no trabajes.

## 1. Roles

| ID | Herramienta | Rol | Escribe en | Lee de | Depende de |
|---|---|---|---|---|---|
| **AG-1** | Antigravity | Extracción Revit: cantidades desde `Modelo federado/` vía pyRevit CLI | `_harness/intermedios/revit/`, `MCP Revit/` | `Modelo federado/` | — |
| **AG-2** | Antigravity | Precios: construye la base de precios de las partidas | `_harness/intermedios/precios/`, `Catalogo de precios/` | `Resources/precios_procesados/`, `referencias_docs/`, `resultado_ejemplo_neodata/` | — |
| **AG-3** | Antigravity | Generadores: cuantificación por partida con referencia al plano o elemento | `Generadores/`, `_harness/intermedios/generadores/` | salida de AG-1 y AG-2 | AG-1, AG-2 |
| **CX-1** | Codex | Presupuesto: partidas, precios, sobrecostos según plantilla | `Presupuesto/`, `_harness/intermedios/presupuesto/` | salida de AG-3, AG-2, `Resources/plantillas_para_usar/` (hoja "sobrecosto") | AG-3 |
| **CX-2** | Codex | Calendario: ejecución de 1 año con partidas distribuidas | `Calendario/`, `_harness/intermedios/calendario/` | salida de CX-1 y lista de frentes de la memoria | CX-1 (puede empezar con la estructura de actividades) |
| **CL-1** | Claude | Coordinación, QA e integración: revisa, consolida y genera `Resultados/` | `Resultados/`, `_harness/cola.md`, `_harness/preguntas.md` | todo | todos |

Si el equipo se reduce a 5 agentes, CL-1 también asume el rol de AG-3 en las etapas finales de cuantificación.

**Configuración vigente: 5 agentes (AG-1, AG-2, CX-1, CX-2, CL-1); CL-1 asume AG-3** (`_harness/decisiones.md` D-004). Contratos y reglas detalladas por rol: `_harness/specs/` (empezar por `SPEC_01_indice_y_propiedad.md`). Plan por olas: `_harness/PLAN_IMPLEMENTACION.md`. Prompts de arranque completos: `_harness/prompts_agentes.md`.

Nota: la plantilla "taller_terminal_presupuesto" es el archivo `Resources/plantillas_para_usar/Taller Terminal_Presupuesto.xlsm` (hoja de sobrecosto = `D25-00_Sobrecosto`).

## 2. Flujo

```
AG-1 (Revit) ──┐
               ├──► AG-3 (Generadores) ──► CX-1 (Presupuesto) ──► CX-2 (Calendario)
AG-2 (Precios) ┘                                 ▲
                                                 │
                                    CL-1 valida cada salida y consolida en Resultados/
```

Las etapas 1 (AG-1 y AG-2) corren en paralelo. Ninguna etapa avanza sin que la anterior haya entregado un intermedio validado.

## 3. Reglas por rol

### AG-1 · Extracción Revit
- Verificar comandos de pyRevit con `pyrevit --help` antes de usarlos.
- Extraer planificaciones y parámetros por modelo. Un archivo JSON por modelo y por categoría en `_harness/intermedios/revit/`.
- Cada elemento lleva: modelo de origen, ID, categoría, nivel, cantidades (longitud, área, volumen, conteo) y parámetros de tipo.
- Antes de extraer, revisar `Scripts/` y `MCP Revit/`. Reutilizar scripts existentes.
- Validar el JSON con su schema Pydantic antes de cerrar la tarea.

### AG-2 · Precios
- Resolver precios en el orden de `CLAUDE.md`, sección 4.
- Por cada partida: `precio_unitario`, `unidad`, `fuente`. Si es aproximado, marcar `SUPUESTO` y explicar el criterio.
- Porcentajes de indirectos y sobrecostos: solo de la hoja "sobrecosto". No reescribirlos.
- Entregar `_harness/intermedios/precios/catalogo_v01.json` con todas las claves y un resumen de partidas sin precio o marcadas como SUPUESTO.

### AG-3 · Generadores
- Un generador por partida, con nivel medio: cantidad, unidad, fórmula sencilla (ej. `largo × alto × piezas`) y referencia al plano o al elemento Revit.
- No cuantificar a mano lo que AG-1 ya extrajo. Si no existe en la salida de AG-1, abrir una pregunta en `_harness/preguntas.md`.
- Entregar `Generadores/Generadores_v01.xlsx` configurado para impresión.

### CX-1 · Presupuesto
- Usar la plantilla `taller_terminal_presupuesto` de `Resources/plantillas_para_usar/` como estructura.
- Tomar cantidades de AG-3 y precios de AG-2. Aplicar sobrecostos de la hoja "sobrecosto".
- Mantener la trazabilidad: cada renglón lleva su `fuente`.
- Entregar `Presupuesto/Presupuesto_v01.xlsx` configurado para impresión.

### CX-2 · Calendario
- Distribuir las partidas en 12 meses (1 año de ejecución). Definir frentes de trabajo y predecesoras en el calendario.
- Cada partida debe tener un mes de inicio y fin, y un porcentaje mensual de avance que sume 100%.
- Marcar la ruta crítica. Si una partida depende de otra, el calendario lo refleja.
- Entregar `Calendario/Calendario_v01.xlsx` configurado para impresión.

### CL-1 · Coordinación y QA
- Revisar cada intermedio contra su schema y contra la fuente de origen.
- Verificar que los totales de Presupuesto cuadren con el catálogo y con las cantidades de Generadores.
- Verificar que el calendario sume 100% por partida y que el total de importes coincida con Presupuesto.
- Consolidar en `Resultados/` solo lo que pasó la revisión. Dejar copia fechada en `Resultados/revisiones/`.
- Mantener `_harness/cola.md` y `_harness/preguntas.md` al día.

## 4. Arranque de cada agente

Cada terminal arranca con este prompt, cambiando solo el ID:

```
Eres el agente <ID> del proyecto. Lee CLAUDE.md y AGENTS.md completos.
Tu rol está en la sección 3 de AGENTS.md. Antes de empezar:
1. Lee _harness/cola.md y toma la primera tarea de tu ID que esté en estado "pendiente" y cuyas dependencias estén "lista".
2. Lee _harness/status/<tu-ID>.md si existe y continúa desde ahí.
3. Revisa Scripts/ y _harness/intermedios/ antes de crear algo nuevo.
Escribe solo en tus carpetas asignadas. Actualiza tu status al terminar cada paso.
```

## 5. Dudas y bloqueos

- Duda sobre datos: `_harness/preguntas.md`, con formato `[ID] [fecha] pregunta · impacto · archivo afectado`.
- Bloqueo por dependencia: marcar la tarea como `bloqueada` en `_harness/cola.md` y pasar a otra tarea de tu rol que sí esté disponible.
- Nunca avanzar con datos inventados. Un `SUPUESTO` marcado es válido; un dato sin marca no.
