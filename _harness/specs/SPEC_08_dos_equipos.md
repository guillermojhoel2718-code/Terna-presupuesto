# SPEC 08 · Dos equipos sobre la misma carpeta de OneDrive (D-014)

## 1. Reparto

| Equipo | Quién | Agentes | Herramientas | Revit |
|---|---|---|---|---|
| **PC-A** (este, `LAPTOP-37IJ4HR0`) | Claude Code | **CL-1** (coordinación, QA, generadores, integración, git) | Claude Code, Excel, Python | No abre el federado |
| **PC-B** | Antigravity + Codex | **AG-1** (Revit), **AG-2** (precios), **CX-1** (presupuesto), **CX-2** (calendario) | Revit 2027 con el federado abierto, pyRevit 7, RevitCortex, Excel, Python | Sí, una sola sesión |

La carpeta raíz puede tener **otra ruta absoluta** en cada equipo (p. ej. `...\Taller Terminal - Taller Terminal\` en PC-A y `...\Taller Terminal - Taller Terminal 1\` en PC-B). Por eso:
- Todos los scripts calculan la raíz desde su propia ubicación; nunca rutas absolutas en código ni en JSON.
- En los JSON, rutas **relativas a la raíz del proyecto** (`Modelo federado/modelo_federado.rvt`, `../Archivos revit/...`).

## 2. Un solo escritor por archivo, también entre equipos

Los locks (`_harness/locks/`) **no son confiables entre equipos**: OneDrive tarda de segundos a minutos en sincronizar, y dos ediciones casi simultáneas generan copias de conflicto (`cola-PC-B.md`). En modo de dos equipos aplica esta regla, que reemplaza la edición compartida de HARNESS.md §2 y SPEC_01:

| Archivo | Escribe | Cómo se comunican los demás |
|---|---|---|
| `_harness/cola.md` | **solo CL-1** (PC-A) | Cada agente declara el estado de sus tareas en la tabla "Tareas" de su `status/<ID>.md`; CL-1 la pasa a `cola.md` |
| `_harness/preguntas.md`, `decisiones.md`, `specs/`, `Scripts/schemas/` | **solo CL-1** | Las preguntas nuevas van en la sección "Preguntas nuevas" de `status/<ID>.md`; CL-1 las numera y las publica |
| `_harness/status/<ID>.md`, `_harness/logs/<ID>-*.md` | el agente `<ID>` | — |
| Intermedios y entregables | su dueño (SPEC_01 §1) | — |

Los locks siguen sirviendo **dentro de PC-B** (4 agentes en la misma máquina), por ejemplo si dos agentes necesitaran el mismo PDF en `intermedios/pdf/`.

### Formato de `status/<ID>.md` en modo dos equipos

```
# AG-1 · Estado
Última actualización: DD-MM-AAAA HH:MM · Equipo: PC-B
Tarea actual: T-102

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-101 | lista para revisión | intermedios/revit/indice.json | OK validar.py |
| T-102 | en curso | — | — |

## Preguntas nuevas
- [23-11-2026] ¿…? · impacto · archivo · supuesto

## Hecho / Pendiente / Siguiente paso / Archivos tocados
...
```

## 3. Escritura segura en OneDrive

1. Escribir JSON/Excel en un temporal en la misma carpeta (`archivo.json.tmp`) y luego renombrar a `archivo.json`. OneDrive sube el archivo completo, nunca a medias.
2. Antes de leer el intermedio de otro agente, verificar que su `status` diga `lista para revisión` o `aprobada` y que el archivo no haya cambiado en el último minuto.
3. Cerrar siempre Excel (COM) en `finally`. Un `.xlsx` abierto bloquea la sincronización.
4. Después de cada bloque, buscar copias de conflicto (`Scripts/01_preparar_equipo.ps1` las reporta). No borrar ninguna sin que CL-1 decida.
5. Marcar el proyecto y `..\Archivos revit` como "Mantener siempre en este dispositivo" (`01_preparar_equipo.ps1 -Pin`).

## 4. Revit

- Solo PC-B tiene abierto `modelo_federado.rvt`. **Nunca guardar** (cada guardado crea respaldos `.000N.rvt` que OneDrive sincroniza y cambia el archivo para el otro equipo).
- PC-A no abre el federado mientras PC-B trabaja.
- AG-1 es el único agente que habla con Revit, aunque CX-1/CX-2/AG-2 estén en la misma máquina.

## 5. Git (D-015)

- Repositorio: `https://github.com/guillermojhoel2718-code/Terna-presupuesto.git`, rama `main`.
- **Solo PC-A hace `git` (CL-1).** La carpeta `.git` también se sincroniza por OneDrive: en PC-B nadie corre `git`.
- Se versiona solo código y documentación (`.gitignore`): md, `Scripts/`, `_harness/` (sin `locks/`, `logs/`, intermedios pesados), `MCP Revit/*.ps1`. No modelos, PDFs, Excel ni el ZIP de RevitCortex.

## 6. Ritmo de sincronización

- Agentes de PC-B: actualizar `status` al cerrar cada tarea **y** al menos cada 30 min de trabajo continuo.
- CL-1: revisar `status/*.md` al final de cada bloque y pasar estados a `cola.md`. Si un `status` no se actualiza en > 2 h, preguntar al usuario.
