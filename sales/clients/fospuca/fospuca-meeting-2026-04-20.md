---
title: Fospuca — Sesión técnica Oficina Virtual
date: 2026-04-20
tags: [sales, client, fospuca, meeting, integration]
duration: 22 min
fireflies: https://app.fireflies.ai/view/01KPE0TFEVPE9QT7J7X6H0R8FF
---

# Fospuca — Sesión técnica OV (2026-04-20)

**Asistentes:** Luis Pulgar, Esteban Suárez (Tesote) · Adriana Sanchez, Carlos Canache, Juan C. Gutiérrez (Fospuca)
**Duración:** 22 min

## Por qué ocurrió

La propuesta original de Tesote se presentó sin haber mapeado que Fospuca opera con una **Oficina Virtual (OV)** propia que es parte central del pipeline de cobranzas. Esta sesión fue para entender cómo funciona realmente el flujo OV → Sage → GP y poder rediseñar la integración.

## Cómo funciona el flujo de pagos hoy

1. **Cliente reporta pago en OV.** Entra al portal, elige municipio, ve sus proformas pendientes, reporta: monto, fecha de pago, banco origen, banco destino, tipo de pago (transferencia, P2P, multipago, punto de venta, etc.), referencia, sube comprobante. Indica cómo distribuir el monto entre proformas (puede dividir).
2. **OV hace validación online vía Megasoft.** Solo contra **BNC** y **Banca Amiga**. Si la transferencia valida, el pago entra a un txt `pagos en línea` → cargado a **GP Direct** (descarga + carga manual).
3. **Lo no validado va a Sage.** Txt separado. Sage corre conciliación automática contra extractos:
   - Tesorería previamente descarga todos los extractos bancarios y los pasa por un **"convertidor" propio** que los estructura al formato que Sage espera (separa gastos bancarios, transferencias, intercompañía, ingresos por concepto de aseo, etc.).
   - Reglas de match en Sage: referencia, fecha, monto, descripción.
   - Lo que Sage no auto-concilia, **Tesorería/Cobros lo hace a mano dentro de Sage** (típicamente cliente puso mal la referencia o el monto, pero el pago sí está en banco).
4. **Sage emite txt de conciliados.** Cargado a GP. GP factura y aplica cobros.
5. **Caja (efectivo) NO va por la interfase.** IGTF complica el formato; se maneja aparte.

**Resultado:** GP recibe **dos streams** — validados-online (vía OV) y conciliados-offline (vía Sage) — con descargas/cargas manuales entre cada etapa.

## Insights clave

- La OV ya hace un **primer filtro de validación bancaria**, no es solo intake.
- **Sage = motor de conciliación**, no ERP. GP es el ERP real.
- Cobertura bancaria de OV es estrecha: solo BNC + Banca Amiga online. El resto va por conciliación contra extracto.
- El **"convertidor" de extractos es propio de Fospuca** y no se discutió en detalle — área de profundización pendiente.
- Mucho trabajo manual: descargas de extractos, cargas a Sage, conciliación a mano, ejecución de interfase a GP.

## Próximos pasos acordados

- **Tesote** se lleva la info para rediseñar la arquitectura internamente.
- **Esteban** retomará con Adriana una vez tengamos la propuesta revisada.
- **Adriana** ofrece traer al dueño técnico de Sage si necesitamos más profundidad.
- **Carlos** ofrece demo con Tesorería/Cobros para mostrar la conciliación manual.

## Preguntas internas a resolver

- ¿Reemplazamos Sage end-to-end o lo complementamos upstream (extractos + auto-match, dejando review manual en Sage)?
- ¿Hemos integrado con Microsoft Dynamics **GP** antes? ¿Qué tan estándar/reusable es?
- ¿Replicamos el "convertidor" o lo reemplazamos con nuestra ingestión nativa de extractos?
- ¿Cómo manejamos IGTF / caja, si es que entra en alcance?

→ Ver [[ask-dan-architecture]] para el ask estructurado al equipo técnico.
