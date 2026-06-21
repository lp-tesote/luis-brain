---
title: Fospuca
tags: [sales, client, fospuca, gp, sage, venezuela, utilities, multi-municipal]
updated: 2026-04-27
linear: SAL-2
author: Luis Pulgar
stage: proposal-revision
---

# Fospuca

| Campo | Detalle |
|---|---|
| **Stage** | `Proposal Revision` — propuesta inicial enviada antes de mapear OV; rediseñando arquitectura |
| **AE** | Esteban Suárez (esteban.suarez@tesote.com) |
| **Champions Fospuca** | Adriana Sanchez (asanchezb@fospuca.com) · Carlos Canache (ccanache@fospuca.com) · Juan C. Gutiérrez (jcgutierrez@fospuca.com) |
| **Sector** | Recolección / aseo urbano — operador multi-municipal en Venezuela |
| **ERP** | Microsoft Dynamics **GP** (no SAP) |
| **Stack pago/conciliación** | Oficina Virtual (custom) → Megasoft (validación online BNC + Banca Amiga) → **Sage** (motor de conciliación con extractos) → GP |
| **Por qué importa** | Logo grande en utilities. Dos vectores de upsell: Payments (reemplazo del leg de pago de OV) + Portal (reemplazo de OV completo). |

## Contexto

Stack atípico para Tesote. Clientes auto-reportan pagos en una **Oficina Virtual** propia. La OV hace validación online vs. BNC y Banca Amiga vía Megasoft. Lo no validado va a **Sage**, que corre conciliación automática contra extractos y deja el resto para revisión manual de Tesorería/Cobros adentro de Sage. GP recibe dos archivos txt: pagos online-validados (vía OV) y pagos conciliados (vía Sage).

Integración estándar de Tesote (extractos → ERP) no calza directo. Hay que decidir si reemplazamos Sage end-to-end o lo complementamos upstream.

## Archivos

| Archivo | Ubicación |
|---|---|
| Meeting recap 2026-04-20 (sesión técnica OV) | `sales/clients/fospuca/fospuca-meeting-2026-04-20.md` |
| Ask a Dan — arquitectura | `sales/clients/fospuca/ask-dan-architecture.md` |
| Transcript Fireflies | https://app.fireflies.ai/view/01KPE0TFEVPE9QT7J7X6H0R8FF |
| Linear ticket (Dan) | [SAL-2](https://linear.app/tesote/issue/SAL-2/fospuca-architecture-decision-ov-sage-gp) |

## Open Actions

1. **Dan** — Responder en [SAL-2](https://linear.app/tesote/issue/SAL-2/fospuca-architecture-decision-ov-sage-gp) con read sobre opciones de arquitectura, esfuerzo, y reusabilidad (ver `ask-dan-architecture.md`)
2. **Esteban** — Retomar con Adriana una vez tengamos arquitectura revisada para reformular propuesta
3. **Por programar** — Demo con Tesorería/Cobros (ofrecida por Carlos Canache) sobre conciliación manual en Sage
4. **Por programar** — Sesión con dueño técnico de Sage en Fospuca (vía Adriana) si necesitamos profundidad

## Engagement Log

| Fecha | Tipo | Notas |
|---|---|---|
| (anterior) | Propuesta inicial | Enviada sin haber mapeado OV — gap detectado al revisar internamente |
| 2026-04-20 | Sesión técnica OV | Adriana + Carlos demostraron flujo OV → Sage → GP. Estructura de data y proceso de conciliación mapeados. |
