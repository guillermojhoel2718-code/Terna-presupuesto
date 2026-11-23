# CX-1 Â· Estado
Ãšltima actualizaciÃ³n: 23-11-2026 (inicial, creado por CL-1) Â· Equipo: PC-B
Tarea actual: â€”

## Tareas
| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|

## Preguntas nuevas
- (ninguna)

## Hecho
â€”

## Pendiente
Tomar la primera tarea de CX-1 en _harness/cola.md cuyas dependencias estÃ©n listas.

## Siguiente paso
Leer CLAUDE.md, AGENTS.md, HARNESS.md, _harness/decisiones.md y _harness/specs/ (incluida SPEC_08).

## Archivos tocados
â€”

## Nota CX-1 Â· 23-11-2026
Se localizÃ³ la raÃ­z OneDrive correcta: C:\Users\kukle\OneDrive - Instituto Politecnico Nacional\Taller Terminal - Taller Terminal 1\Presupuestos taller terminal. Contiene CLAUDE.md, _harness/specs, Resources/plantillas_para_usar/Taller Terminal_Presupuesto.xlsm y _harness/intermedios/pdf/memoria_arquitectonica.txt. El status ya existÃ­a allÃ­ y no se sobrescribiÃ³. Se trasladÃ³ el log CX-1 de esta fecha porque el destino no existÃ­a. No se trasladaron archivos de calendario; CX-1 no creÃ³ ninguno. A partir de esta sesiÃ³n, trabajar solo en esta raÃ­z.
## Actualización CX-1 · 23-11-2026 03:00 · PC-B
Tarea actual: T-403 bloqueada; T-401 y T-402 listas para revisión de CL-1.

| Tarea | Estado | Intermedio | Validado |
|---|---|---|---|
| T-401 | lista para revisión | Presupuesto/Presupuesto_v00_base.xlsm | OK: copia VBA; defectos SPEC_06 corregidos; Carta en todas las hojas; Excel COM 16.0 disponible y probado |
| T-402 | lista para revisión | Scripts/40_llenar_plantilla_presupuesto.py; Presupuesto/Presupuesto_v00_prueba.xlsm | OK: prueba sintética marcada; COM convergió; resultado de prueba pasó validar.py; macros/Carta/fit-to-width confirmados |
| T-403 | bloqueada | presupuesto_v01.json / Presupuesto_v01.xlsm | No: T-205/catálogo y T-304/generadores siguen pendientes; además no hay celda/fuente de IVA identificable en plantilla |

### Hecho
- Raíz verificada: C:\Users\kukle\OneDrive - Instituto Politecnico Nacional\Taller Terminal - Taller Terminal 1\Presupuestos taller terminal; contiene CLAUDE.md, _harness/specs, plantilla XLSM indicada y _harness/intermedios/pdf/memoria_arquitectonica.txt.
- T-401: copia de plantilla corregida y guardada con keep_vba=True. Q9='01_Datos Generales'!D15, AW11=12, nombre y superficie D-010, capítulo ejemplo reemplazado por la lista SPEC_02, A13 enlazado a B10; impresión Carta.
- T-402: script JSON→jerarquía/renglones/resumen, fuente en comentarios, CD en J, factor leído/iterado desde hoja mediante Excel COM, JSON atómico y validación de schema. El script preserva VBA y restaura Carta/fit-to-width tras el guardado COM.
- Prueba: datos sintéticos identificados como prueba T-402, solamente en Presupuesto_v00_prueba.*. Factor = 1367.8852956756064 para CD sintético 2,500; salida JSON sintética validada. El porcentaje IVA 0.0 del fixture es solo un control de prueba, no un dato de obra.
- La carpeta de trabajo anterior no es la raíz real; no se trabajará allí. No se trasladaron archivos de calendario porque CX-1 no los creó. El status de OneDrive ya existía y no se sustituyó con una copia.

### Pendiente / siguiente paso
- CL-1 debe revisar T-401 y T-402 y reflejar sus estados en cola.md.
- Esperar aprobaciones de generadores_v01 y catalogo_v01 en cola.md y validación del IVA de origen antes de T-403. No se escribe porcentaje supuesto.

### Preguntas nuevas
- [23-11-2026] ¿Cuál celda de la plantilla contiene la tasa de IVA que debe leerse? No se encontró una celda/fórmula para la tasa en el XLSM; el documento solo menciona “más el I.V.A.”. · impacto: iva/total de presupuesto_v01.json y cierre de T-403 · archivo afectado: Resources/plantillas_para_usar/Taller Terminal_Presupuesto.xlsm / _harness/intermedios/presupuesto/presupuesto_v01.json · sin supuesto

### Archivos tocados
Presupuesto/Presupuesto_v00_base.xlsm; Presupuesto/Presupuesto_v00_prueba.xlsm; Presupuesto/Presupuesto_v00_prueba.json; Presupuesto/Presupuesto_v00_prueba_final.xlsm; Presupuesto/Presupuesto_v00_prueba_final.json; Presupuesto/Presupuesto_v00_prueba_integrada.xlsm; Presupuesto/Presupuesto_v00_prueba_integrada.json; Presupuesto/Presupuesto_v00_prueba_resultado.xlsm; Presupuesto/Presupuesto_v00_prueba_resultado.json; Scripts/40_llenar_plantilla_presupuesto.py; _harness/status/CX-1.md; _harness/logs/CX-1-23-11-2026.md
