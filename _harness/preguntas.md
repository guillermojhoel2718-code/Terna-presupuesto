# Preguntas abiertas

Formato: `P-NNN | [ID] [DD-MM-AAAA] pregunta · impacto · archivo afectado · supuesto mientras tanto`
Todos agregan al final (con lock). Solo CL-1 cierra (mueve a "Cerradas" con la respuesta y, si aplica, crea una decisión en `decisiones.md`).

## Abiertas (para el usuario)

- P-009 | [CL-1] [23-11-2026] El PDF del tabulador CDMX (`Resources/referencias_docs/tabulador-general-...-septiembre-2026.pdf`, 3.8 MB) está en PC-A pero AG-2 no lo ve en PC-B. ¿Revisas el estado de sincronización de OneDrive en PC-A (ícono de la nube) y en PC-B? · Impacto: T-201 y precios por tabulador (D-003) · Supuesto: AG-2 sigue con APU + Xalapa/Neodata y reabre T-201 cuando el archivo llegue.
- P-010 | [CL-1] [23-11-2026] En Instalaciones.rvt (IHS) el sub-vínculo `Bloque de baños_vinculo.rvt` está **Unloaded**: por eso no hay WC, lavabos ni mingitorios (solo 14 cajas de registro y 3 biodigestores). ¿Lo cargas en Revit del PC-B (Manage Links) para que AG-1 vuelva a extraer IHS? · Impacto: cap. 08/09 incompletos (muebles sanitarios) · Supuesto: se cuantifica lo que hay y se marca el faltante.

- P-012 | [CX-1 vía CL-1] [23-11-2026] La plantilla no trae tasa de IVA ni celda de origen (solo la leyenda "MÁS EL I.V.A. CORRESPONDIENTE"). ¿El presupuesto se entrega **sin IVA** con esa leyenda, o con IVA calculado? Si se calcula, ¿16 % (tasa general; San Luis de la Paz no es zona fronteriza)? · Impacto: total de Presupuesto y Calendario · `presupuesto_vNN.json` (iva_tasa) · Supuesto: se presenta subtotal sin IVA y el IVA al 16 % como renglón informativo, marcado SUPUESTO.

## Cerradas

- P-007 | Instalaciones Especiales → no se toman en cuenta (D-016).
- P-008 | Albañilería → modelo ARQ-MOB (D-017).

- P-001 | Eléctrico → ya vinculado; el vigente es el de "Copias de seguridad" (D-008). Especiales y albañilería pasan a P-007 y P-008.
- P-002 | RevitCortex → se instala en ambos equipos (D-009).
- P-003 | Nombre "Centro Comunitario de Desarrollo Integral "Casa de los Chichimecas"", 2,500 m² aprox. (D-010).
- P-004 | Tabulador CDMX = costo directo, sin conversión (D-011).
- P-005 | Inicio enero 2027 (D-012).
- P-006 | Montos de sobrecosto se dejan como vienen (D-013).
- P-011 | Muros desde Estructura + Cancelería, confirmado por el usuario (D-019). Se mantiene como tarea para AG-1: revisar si los 9,931 paneles de muro cortina de Estructura duplican los 101 muros NOVABLOCK antes de cuantificar (T-302).
