# HARNESS.md — Operación del equipo en paralelo

Carpeta de apoyo para coordinar varias terminales (Antigravity, Codex, Claude) sobre el mismo proyecto en OneDrive. No cambia la estructura de carpetas del proyecto.

## 1. Estructura de `_harness/`

```
HARNESS.md            Este archivo (vive en la raíz del proyecto)
_harness/
  decisiones.md       Decisiones del usuario (prioridad sobre interpretaciones)
  PLAN_IMPLEMENTACION.md  Olas de trabajo en paralelo
  prompts_agentes.md  Prompts de arranque de los 5 agentes
  specs/              Contratos: SPEC_01 (índice/propiedad) … SPEC_07 (impresión)
  cola.md             Cola de tareas: quién hace qué y en qué estado
  preguntas.md        Dudas abiertas para el usuario
  status/             Un archivo por agente: AG-1.md, AG-2.md, AG-3.md, CX-1.md, CX-2.md, CL-1.md
  locks/              Candados de escritura (un archivo .lock por archivo en edición)
  intermedios/        Salidas JSON/texto validadas por rol
    revit/  precios/  generadores/  presupuesto/  calendario/  pdf/
  logs/               Registro de sesiones por agente
```

## 2. Cola de tareas (`cola.md`)

Formato de cada tarea:

```
- [ ] T-014 | AG-3 | Generadores · muros de block planta baja | depende: T-003, T-007 | estado: pendiente
```

Estados válidos: `pendiente`, `en curso`, `bloqueada`, `lista para revisión`, `aprobada`, `rechazada`.

Reglas:
- Solo el agente con el ID de la tarea la cambia a `en curso`.
- Una tarea pasa a `lista para revisión` cuando su intermedio está en `_harness/intermedios/` y validado por schema.
- CL-1 es el único que pasa una tarea a `aprobada` o `rechazada`.
- Si CL-1 rechaza, escribe el motivo debajo de la tarea. El agente la retoma.

## 3. Estado por agente (`status/<ID>.md`)

Actualizar al terminar cada paso. Es la memoria que permite retomar una sesión:

```
# AG-3 · Estado
Última actualización: 2026-MM-DD HH:MM
Tarea actual: T-014
Hecho: extracción de muros cargada desde intermedios/revit/muros_modelo_A.json
Pendiente: cuantificar muros de fachada (ver preguntas.md P-004)
Siguiente paso: validar generadores contra schema
Archivos tocados: Generadores/Generadores_v01.xlsx
```

## 4. Candados de escritura (`locks/`)

OneDrive sincroniza y puede generar copias de conflicto si dos agentes escriben el mismo archivo. Para evitarlo:

1. Antes de editar un archivo compartido, crear `locks/<nombre-archivo>.lock` con el ID del agente y la hora.
2. Si el lock ya existe y no es tuyo, no escribas. Anótalo en tu status y pasa a otra tarea.
3. Al terminar, borra tu lock.
4. Un lock con más de 2 horas sin actividad se considera abandonado. Avisar en `preguntas.md` antes de borrarlo.

Regla de oro: **cada archivo tiene un solo escritor**. Los locks son respaldo, no la estrategia principal. La estrategia principal es la asignación de `AGENTS.md`.

## 5. OneDrive

- Marcar la carpeta del proyecto como **"Siempre mantener en este dispositivo"** para evitar archivos solo en la nube durante la corrida.
- Pausar la sincronización solo si hay errores repetidos de archivo bloqueado. Reanudar al terminar la sesión.
- Después de cada corrida larga, buscar archivos con "conflicto" o "-PC" en el nombre. Si aparecen, revisar cuál versión es la correcta antes de borrar algo.
- Los JSON intermedios son pequeños; los Excel y PDF pesan más. No generar PDFs en cada paso, solo en revisiones.

## 6. Correr sesiones largas

Para dejar a la IA trabajar varias horas:

1. **Checkpoints**: el agente guarda `status/<ID>.md` y su intermedio al cerrar cada tarea, no al final de la sesión.
2. **Contexto**: cuando una sesión se haga muy larga, cerrarla y abrir una nueva con el prompt de arranque de `AGENTS.md`. La nueva sesión retoma desde `status/`.
3. **Límites**: cada agente trabaja en bloques de tareas (2 a 4 tareas por sesión). Al terminar el bloque, cerrar la sesión.
4. **Logs**: registrar en `logs/<ID>-AAAA-MM-DD.md` qué se hizo, qué comandos se corrieron y qué errores aparecieron.
5. **Errores repetidos**: si un agente falla 3 veces la misma tarea, se detiene, escribe el error en `preguntas.md` y pasa a otra tarea.

## 7. Orden de arranque

1. Abrir CL-1 primero. Revisar que `cola.md` tenga todas las tareas por partida y dependencias.
2. Arrancar AG-1 y AG-2 (independientes, en paralelo).
3. Cuando AG-1 y AG-2 tengan intermedios aprobados, arrancar AG-3.
4. Cuando AG-3 tenga generadores aprobados, arrancar CX-1. CX-2 puede arrancar con la estructura de actividades desde el primer día.
5. CL-1 revisa cada hora o al cerrar cada bloque de tareas, y consolida en `Resultados/` cuando haya avance importante.

Nota para Antigravity: confirmar en tu versión si carga automáticamente `AGENTS.md` o `CLAUDE.md`. Si no lo hace, usar el prompt de arranque de la sección 4 de `AGENTS.md`.

## 8. Revisiones parciales

Cuando el avance sea suficiente para revisar:

1. CL-1 corre la verificación cruzada: totales, cantidades contra Revit, calendario al 100%.
2. Genera `Resultados/Generadores_vNN.xlsx`, `Presupuesto_vNN.xlsx` y `Calendario_vNN.xlsx` con la versión siguiente.
3. Deja copia fechada en `Resultados/revisiones/`.
4. Anota en `preguntas.md` los pendientes que quedan para la siguiente versión.

## 9. Checklist de cierre de corrida

- [ ] Todas las tareas están en `aprobada` o con motivo en `bloqueada`.
- [ ] No quedan locks activos.
- [ ] `preguntas.md` solo tiene dudas que requieren al usuario.
- [ ] Los tres Excel tienen versión nueva en `Resultados/` y están configurados para impresión.
- [ ] Los scripts nuevos están en `Scripts/` con encabezado.
