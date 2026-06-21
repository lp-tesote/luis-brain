---
title: Alimentos Génica
tags: [sales, client, genica, sap, venezuela]
updated: 2026-04-15
stage: discovery
---

# Alimentos Génica

## Quick Facts

| Field | Value |
|---|---|
| **Stage** | `Discovery` — post-discovery call completada |
| **AE** | Esteban Suárez (esteban.suarez@tesote.com) |
| **Account Owner** | Carlos Melián (carlos.melian@tesote.com) |
| **Champions** | José Boscán (jose.boscan@genica.com.ve) · Anaura Prieto (anaura.prieto@genica.com.ve) |
| **Technical Gate** | Leodardo Chacín · Juan García |
| **ERP** | SAP — integración estándar vía API (JSON) |
| **Cuentas bancarias** | 25–30 nacionales (+ custodio/electrónicas pendientes de inventario) |
| **Transacciones/mes** | ~5.000 (estimado) |
| **Dossier ID** | TST-2026-005 |

## Discovery Summary (2026-04-10)

Génica tiene el 95% del proceso de carga a SAP automatizado. El eslabón manual es la descarga diaria de extractos bancarios desde múltiples portales bancarios (~1 hora/día). Tesote cierra exactamente esa brecha: descarga automática → envío JSON a SAP vía API. Equipo de 15 personas en la discovery, incluyendo finanzas, tesorería, cobranza e IT. Dos champions sólidos. Economic buyer no identificado — acción urgente antes de presentar propuesta.

**Pain points clave:**
- Descarga manual de extractos (~1 hora/día)
- Fallos en SAP por códigos bancarios nuevos no registrados
- Extractos con datos incompletos (RIF truncados) desde algunos bancos

**Timeline acordado:** ~8 semanas total (4–5 finanzas + 5–7 SAP, en paralelo)

## Files

| File | Location |
|---|---|
| Blueprint Operativo v1.0 | `implementation/playbooks/blueprint-operativo-genica.md` |
| Dossier v1.0 (confidencial) | `sales/clients/genica/genica_dossier_v1.0.md` |
| Follow-up email (2026-04-10) | `sales/clients/genica/genica_followup_2026-04-10.md` |
| Discovery transcript | `.scratch/meetings/genica-discovery-2026-04-10.md` |

## Open Actions

1. **José Boscán** — Inventario completo de cuentas bancarias (bloqueante para propuesta)
2. **Anaura Prieto** — Validar volumen de transacciones
3. **Leodardo / Juan García** — Revisar documentación técnica API + seguridad
4. **Esteban (Tesote)** — Confirmar tiempos de respuesta para alertas de códigos bancarios
5. **Esteban (Tesote)** — Identificar economic buyer antes de presentar propuesta formal

## Engagement Log

| Date | Type | Notes |
|---|---|---|
| 2026-03-27 | Intro Call | Presentación Tesote. Confirmado SAP. Identificado proceso manual. |
| 2026-04-10 | Discovery Call | Casos de uso confirmados. SAP API JSON. 25–30 cuentas. 8 semanas timeline. |
