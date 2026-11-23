# SPEC 02 · Claves, capítulos y frentes

Contrato común para que AG-2, CL-1 (Generadores), CX-1 y CX-2 trabajen en paralelo sin esperar a que otro defina la estructura. Implementado en `Scripts/schemas/common.py`.

## 1. Formato de clave (D-007)

```
ED-CC-SS-NNN
│  │  │  └── concepto 001..999 (consecutivo dentro del subcapítulo)
│  │  └───── subcapítulo 01..99 (lo define AG-2 dentro de cada capítulo)
│  └──────── capítulo 01..14 (tabla de abajo, fija)
└─────────── bloque: ED = Edificio de educación (único en alcance, D-001)
```

- Regex: `^(ED|SC|CD|AS)-\d{2}-\d{2}-\d{3}$`. SC/CD/AS quedan reservados.
- La clave nace en AG-2 (`catalogo_vNN.json`). Nadie más crea claves; si falta un concepto, se pide en `preguntas.md`.
- En la plantilla de presupuesto: columna **A "Partida"** = numeración jerárquica (`2`, `2.1`, `2.1.3`), columna **B "Código"** = clave `ED-02-01-003`.

## 2. Capítulos (fijos)

Derivados de la memoria (§4–§10) y de los vínculos del federado.

| CC | Capítulo | Fuente de cantidad principal | Categorías Revit típicas |
|---|---|---|---|
| 01 | Preliminares (limpieza, trazo, nivelación) | Área de desplante del modelo | Floors (nivel 0), Pads |
| 02 | Cimentación (excavación, plantilla, zapatas corridas, dados, dalas de desplante, rellenos) | Estructura_2027 | Structural Foundations, Structural Framing |
| 03 | Estructura de concreto y mampostería confinada (castillos, dalas, cerramientos, losa vigueta-bovedilla, capa de compresión) | Estructura_2027 | Structural Columns, Structural Framing, Floors |
| 04 | Estructura metálica y cubierta (cerchas, correas, arriostres, placas base, panel sándwich, canalones) | Estructura_2027 / Arq | Structural Framing (acero), Roofs, Gutters |
| 05 | Albañilería (muros de mampostería, firmes, chaflanes, pretiles) | Edificio de educacion.rvt y Cancelería (D-019; ARQ-MOB no tiene muros) | Walls |
| 06 | Acabados (pisos, muros, plafones) | Acabados_2027 | Floors (acabado), Walls (acabado), Ceilings |
| 07 | Herrería y cancelería | Herrería y Cancelería_2027 | Windows, Doors, Curtain Panels, Railings |
| 08 | Instalación hidráulica y pluvial | Instalacion IHS_2027 | Pipes, Pipe Fittings, Plumbing Fixtures |
| 09 | Instalación sanitaria | Instalacion IHS_2027 | Pipes, Plumbing Fixtures |
| 10 | Instalación eléctrica y fotovoltaica | Instalacion Electrica_2027 (vinculado, D-008) | Conduits, Cable Trays, Lighting Fixtures, Electrical Equipment/Fixtures |
| 11 | Voz y datos — **fuera de alcance (D-016)**, número reservado sin conceptos | — | — |
| 12 | CCTV y seguridad — **fuera de alcance (D-016)**, número reservado sin conceptos | — | — |
| 13 | Mobiliario y equipamiento fijo | TT-ED-EDU-ARQ-MOB | Furniture, Casework, Specialty Equipment |
| 14 | Limpieza final y entrega | Sin Revit (`sin_cantidad_revit: true`) | — |

## 3. Frentes de trabajo (para CX-2)

| Frente | Capítulos | Lógica de secuencia |
|---|---|---|
| F1 Obra negra | 01, 02, 03, 05 | 01 → 02 → 03 ↔ 05 (por niveles) |
| F2 Estructura metálica y cubierta | 04 | inicia al cerrar 03 del último nivel |
| F3 Instalaciones | 08, 09, 10 | ranurado/ductos con 05; guiado y equipos con 06 |
| F4 Acabados | 06, 07 | tras 04 (edificio cerrado) |
| F5 Equipamiento y entrega | 13, 14 | últimos 2 meses |

## 4. Unidades

Solo las del enum `Unidad` de `common.py`. Los CSV traen `ml`: se normaliza a `m` con `normalizar_unidad()`. `lote` solo para partidas globales, con justificación.
