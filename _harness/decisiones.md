# Decisiones del proyecto

Registro de decisiones tomadas por el usuario. **Tienen prioridad sobre cualquier interpretación de un agente.** Solo CL-1 agrega entradas, y solo con una respuesta del usuario.

Formato: `D-NNN | fecha | decisión | origen`

| ID | Fecha | Decisión | Origen |
|---|---|---|---|
| D-001 | 23-11-2026 | **Alcance = solo lo vinculado en el modelo federado** (Edificio de educación). Los otros bloques de la memoria (social-cultural, comercial-deportivo, acceso-servicios) quedan fuera. | Usuario, sesión de arranque |
| D-002 | 23-11-2026 | Lectura de Revit **mediante MCP** (ver `specs/SPEC_04_revit.md`). Las especialidades del Edificio de educación que no están vinculadas al federado (eléctrico, especiales, albañilería) se leen con el MCP directamente de su RVT en solo lectura, registrando el archivo de origen. Ver P-001 para confirmar qué archivo es el vigente. **Superada por D-008, D-016 y D-017: solo se leen los 6 vínculos.** | Usuario, sesión de arranque |
| D-003 | 23-11-2026 | **Precios: esquema mixto.** P.U. de concepto del tabulador CDMX 2026 cuando el concepto exista; si no, análisis de P.U. (APU) armado con insumos de `Resources/precios_procesados/` y rendimientos de los PDFs Neodata. Detalle en `specs/SPEC_05_precios.md`. | Usuario, sesión de arranque |
| D-004 | 23-11-2026 | **Equipo de 5 agentes**: AG-1, AG-2, CX-1, CX-2 y CL-1. CL-1 absorbe el rol AG-3 (Generadores), como prevé `AGENTS.md` §1. | Usuario, sesión de arranque |
| D-005 | 23-11-2026 | Periodo de ejecución **12 meses**. Se captura en `D25-00_Sobrecosto!AW11` (hoy dice 3). | CLAUDE.md §1 |
| D-006 | 23-11-2026 | Impresión en **tamaño Carta** (paperSize = 1), aunque las plantillas vengan en A4 o sin tamaño. | CLAUDE.md §1 |
| D-007 | 23-11-2026 | Formato de clave `ED-CC-SS-NNN` (ver `specs/SPEC_02_claves_y_partidas.md`). No se cambia después de aprobado el catálogo v01. | CL-1, CLAUDE.md §7 |
| D-008 | 23-11-2026 | **Eléctrico ya vinculado** al federado: `Instalacion Electrica_2027\Copias de seguridad\Proyecto electrico_corregido.rvt` es el vigente (aunque esté en "Copias de seguridad"). Ahora son 6 vínculos. Especiales: fuera de alcance (D-016). | Usuario (P-001) |
| D-009 | 23-11-2026 | **RevitCortex v1.0.50** se instala en ambos equipos desde `MCP Revit/instalador/RevitCortex-v1.0.50.zip` con `MCP Revit/instalar_revitcortex.ps1`. MCP preferente para AG-1: RevitCortex; respaldo: pyRevit MCP / `pyrevit agent`. | Usuario (P-002) |
| D-010 | 23-11-2026 | Nombre oficial: **Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"**. Superficie construida: **2,500 m² aprox.** | Usuario (P-003) |
| D-011 | 23-11-2026 | Los P.U. del **tabulador CDMX 2026 son costo directo**: se usan sin conversión. | Usuario (P-004) |
| D-012 | 23-11-2026 | Inicio de obra: **enero de 2027** (mes 1 = enero 2027, mes 12 = diciembre 2027). `fecha_inicio_obra` = 04-01-2027 (primer lunes hábil). | Usuario (P-005) |
| D-013 | 23-11-2026 | Montos de la hoja sobrecosto (personal, rentas, etc.) **se dejan como vienen** en la plantilla; solo cambia `AW11 = 12`. | Usuario (P-006) |
| D-014 | 23-11-2026 | **Dos equipos**: PC-A (este, usuario `jcama`) corre solo **CL-1 (Claude)**. PC-B (Revit 2027 + Excel, ya con Revit abierto) corre **AG-1, AG-2, CX-1, CX-2** en paralelo. Sincronizan por la carpeta compartida de OneDrive. Ver `specs/SPEC_08_dos_equipos.md`. | Usuario |
| D-015 | 23-11-2026 | Repositorio de código: `https://github.com/guillermojhoel2718-code/Terna-presupuesto.git` (rama `main`). Solo código y documentación; no modelos, PDFs ni Excel. Solo PC-A hace commits/push. | Usuario |
| D-016 | 23-11-2026 | **Instalaciones Especiales fuera de alcance**: no se lee su RVT. Capítulos 11 (voz y datos) y 12 (CCTV) quedan reservados sin conceptos. | Usuario (P-007) |
| D-017 | 23-11-2026 | **Albañilería (cap. 05) desde el modelo ARQ-MOB** (`TT-ED-EDU-ARQ-MOB.rvt`). El RVT de Novablock no se usa. Con esto todas las cantidades salen de los 6 vínculos del federado. | Usuario (P-008) |
| D-018 | 23-11-2026 | El Excel de generadores **se genera con `Scripts/30_generadores_desde_revit.py`** reproduciendo el formato de bloque de la plantilla (HOJA DE CUANTIFICACIÓN, PARTIDA/CLAVE/UNIDAD, dimensiones, (+)/(−), parcial, total, firmas). No se copia la plantilla: trae datos de otro proyecto e imágenes que openpyxl no conserva. Se agregan columna de referencia Revit y hoja `REF_REVIT`. | CL-1 (T-301) |
| D-019 | 23-11-2026 | **Cap. 05 Albañilería — enmienda a D-017** (supuesto de trabajo, el usuario puede vetarlo): `TT-ED-EDU-ARQ-MOB.rvt` solo contiene mobiliario (530 Furniture, 40 Casework, 35 SpecialtyEquipment, 2 FurnitureSystems) y ningún muro. Los muros salen de `Edificio de educacion.rvt` (101 muros NOVABLOCK 12 H, 1,337.95 m²) y de `TT_ED_EDUCACIÓN_CANCELERIA_2027.rvt` (87 muros ladrillo cara vista, 1,040.43 m²). Hallazgo de AG-1 (`revit/indice.json`, notas). Cap. 13 sí sigue en ARQ-MOB. | CL-1 (T-101 de AG-1) |
