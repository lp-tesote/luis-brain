---
title: "CAPCA — Claudia meeting prep (2026-04-30)"
tags: [capca, sales, claudia, portal, prep]
updated: 2026-04-29
author: Luis Pulgar
status: draft
---

# CAPCA — Claudia meeting prep · 2026-04-30

> **Goal of tomorrow's meeting:** alignment, not pitch. Show Claudia we received Rosa's doc, the visions overlap ~80%, and we're already building the highest-impact piece (Pagos + Conciliación). Park Solicitudes/Logística as a future module — don't kill it, don't commit to it.

> **Tactical posture (locked):**
> - Portal IS the protagonist. CAPCA mental model: SAP does everything; portal is the customer-facing extension of SAP.
> - **Do not push the workspace dashboard.** It exists, but for CAPCA's day-to-day operators (Tesorería, Contabilidad), SAP is the workspace. Tesote workspace surfaces only for monitoring/exceptions.
> - SAP S/4HANA Cloud went live 2026-03-09. Sofos left bank-extraction + BCV in the backlog. **Tesote closes that gap.** Claudia knows this — don't re-pitch.

---

## TL;DR for Luis

1. Open with: *"Rosa nos compartió el documento. La visión está casi 1:1 alineada con donde Tesote ha estado invirtiendo los últimos meses. Lo que ustedes ven como Fase 3 — Pagos + Conciliación — es nuestra Fase 1 contigo. Empezamos donde ustedes querían terminar."*
2. Demo `claim-flow-capca.html` end-to-end: factura por correo → login → dashboard → multi-pago → comprobante → conciliación SAP.
3. Map Rosa's 5 modules to **3 buckets**: in-v1 / promote-to-v1 / future-roadmap.
4. Surface 6 decisions Claudia owns (auth model, multi-pay, estado de cuenta, credit limit, retenciones, procurement module).
5. Close: confirm Fase 1 runway, pilot with N clients, schedule next sync.

---

## How Rosa's vision maps to what we have

### Bucket A — Already in v1 (just needs CAPCA chrome)

| Rosa's ask | Tesote v1 status | Notes |
|---|---|---|
| Dashboard con facturas pendientes / deuda / histórico | ✅ Inicio + Pagos screens built | Re-skin to Fiori-feel; same data |
| Línea de tiempo de deuda (cronológico) | ✅ Pagos table sorts by `vence` | Add aging buckets visually |
| Selección de banco + monto + referencia | ✅ 4-step pay flow built (BNC débito inmediato) | Better than what Rosa described — direct debit, no manual ref |
| Trazabilidad de Terceros (RIF mismatch) | ✅ Already in master blueprint #9 (Fase 1) | Workspace-side flag, surface in portal too |
| Retenciones | 🟡 Luis pitched in Rosa call → Rosa loved it. Spec'd in [seniat-retenciones] | v1 = comprobante shows línea de retención; full SENIAT XML = v1.1 |
| Notificación de pago dinámica | ✅ Comprobante card on success (Step 4) | 6-row card already built |
| Conciliación automática SAP FI clearing | 🟡 Master plan Fase 2 (#15) — "objetivo no negociable de Claudia" | The pay flow triggers it; FI-AR matching is the engineering work |

### Bucket B — Promote to v1 for CAPCA (currently deferred in master spec)

| Rosa's ask | Current spec | Recommend |
|---|---|---|
| **Multi-invoice select + consolidated pay** | Out of v1 (per `counterparty-portal-prd.md`) | **Promote to v1.** Sugar buyers pay multiple facturas at once. Killer omission otherwise. |
| **Estado de Cuenta PDF/Excel** | Out of v1 ("payment history and exports" deferred) | **Promote to v1.** It's a download endpoint, not architectural. Easy win. |
| **Calculadora BCV widget** | Not in spec | **Add to v1.** Cheap — we already inject BCV into SAP in Fase 1. Reuse the source. |
| **Aging buckets (0-30 / 31-60 / 60+)** | Not in spec | **Add to v1.** UI-only, derived from `vence` date. |
| **Saldo Disponible para Compra (credit limit display)** | Not in spec | **Show as info in v1, do NOT block.** Blocking ties portal to SAP credit-limit field + Solicitudes module. Show the number; defer the gating logic. |
| **SAP customer code + password login** | Spec is email + OTP, no passwords | **Decision needed — see §Auth below.** |

### Bucket C — Future roadmap (out of scope, capture and park)

| Rosa's ask | Why deferred | What to call it |
|---|---|---|
| Solicitudes de pedido (módulo SD) | Not payments. Procurement / order management. | **"Tesote Procurement" / "Tesote Compras"** — future module |
| Precios dinámicos consultados a SAP | Pricing engine, depends on Solicitudes | Same module |
| Forma de pago (Contado/Crédito) routing a Ventas | Solicitudes-coupled | Same module |
| Timeline DHL-style (cita, QR, chofer, placa) | Fulfillment tracking, depends on Solicitudes | Same module — "Tesote Logística" or sub-module of Procurement |
| AWS internacional, CEDCA arbitraje | Infra/legal — addressable but not portal feature | Contracts/security review (Mariel + legal) |

---

## The phasing flip

**Rosa's roadmap:**
1. Dashboard + autogestión
2. Solicitudes + logística
3. Pagos + conciliación

**Tesote's natural fit (frame to Claudia):**
1. **Pagos + Conciliación** — Rosa's Fase 3, Tesote's Fase 1
2. **Dashboard + autogestión** — bundled in (because the pay flow needs the inbox + dashboard around it)
3. **Solicitudes + logística** — future module, separate scoping

**Why this works:**
- Rosa's ROI argument to Claudia ("ahorro horas-hombre cobranzas") lives in Pagos+Conciliación. We deliver the high-ROI piece first.
- Solicitudes is real engineering — SAP SD integration, pricing, dispatch. Doing it last means CAPCA gets value first; doing it first means months before they see anything.
- Aligns with our master blueprint: Fase 1 (bancario+SAP+BCV) → Fase 2 (FI-AR matching) → Fase 3 (portal). The portal IS the trigger that makes Fase 2 close itself.

---

## Decisions Claudia owns (surface tomorrow)

### 1. Auth model: SAP customer code vs email

**Rosa's doc:** "Login con código de cliente SAP y contraseña"
**Our spec:** email + OTP, no passwords

| Option | Pro | Con |
|---|---|---|
| (a) SAP customer code + password | Matches CAPCA's mental model (SAP-first) | Adds password infra we don't want; identity tied to SAP not portable |
| (b) Email + OTP, RIF as secondary identifier | Our tested model; portable across multiple sellers (network play) | Requires CAPCA to confirm/maintain customer email in SAP master |
| (c) Hybrid: email + OTP for auth, SAP customer code shown as identifier in dashboard | Best of both | Slight onboarding lift |

**Recommend:** (c). Auth = email+OTP; dashboard headers show the SAP customer code so CAPCA's customers see their familiar identifier.

### 2. Multi-invoice consolidated pay in v1?

**Recommend YES.** Sugar buyers don't pay one factura at a time. Promote from v1.1 to v1.

### 3. Estado de Cuenta export (PDF/Excel) in v1?

**Recommend YES.** Cheap; high-perceived-value; closes "missing feature" objection on day 1.

### 4. Saldo Disponible para Compra — show or block?

**Recommend show, don't block.** Blocking couples portal to SAP credit-limit field + Solicitudes module. Show the number prominently; let CAPCA's Ventas team enforce in their own flow.

### 5. Retenciones in v1?

**Recommend partial.** Comprobante already shows monto pagado; add a "monto retenido" line item to the PDF. Full SENIAT XML export + comprobante issuance = v1.1, lives in [seniat-retenciones-process-mariel-review.md].

### 6. Procurement / Solicitudes module — when?

**Recommend: capture, don't commit.** Frame it as "Tesote Procurement / Tesote Compras" — separate engagement post-Fase 1 Go-Live. Don't kill Rosa's vision, but don't put it on this contract's critical path.

---

## What to demo (in order)

`claim-flow-capca.html` — happy path, ~5 min:

1. **Email** — factura llega de CAPCA al cliente
2. **Login** — email + OTP (mention the SAP-code-as-identifier overlay we'll add)
3. **Inicio** — facturas por pagar, total Bs., BCV widget, aging snapshot
4. **Pago multi-factura** — select 3, pago consolidado, BCV-exact en Bs.
5. **OTP del banco** (BNC débito inmediato)
6. **Comprobante** — animado, 6 filas, mención de retención
7. **Vuelta al portal** — facturas marcadas como pagadas, conciliación SAP en backend

`workspace-capca.html` — **2 min only**, framed as: "Esto es lo que ven Yolimar, Leandro y los equipos de Tesorería para monitoreo y excepciones — no para operación diaria. La operación diaria sigue en SAP."

---

## What NOT to do tomorrow

- ❌ Don't push workspace dashboard as the main thing
- ❌ Don't commit to Solicitudes / Pedidos / Logística timeline in Fase 1 or Fase 2
- ❌ Don't promise Saldo-bloquea-pedido — it's a Solicitudes feature
- ❌ Don't agree to "SAP customer code + password" without the email layer
- ❌ Don't volunteer scope for AWS regional storage / CEDCA — defer to legal review

---

## Open questions to ask Claudia

1. ¿Cuántos clientes activos tiene CAPCA hoy? (dimensiona piloto)
2. ¿Cuántos pagan facturas múltiples en un solo movimiento bancario? (valida Multi-pay v1)
3. ¿El equipo de Ventas tiene appetite para un módulo separado de Solicitudes/Logística post-Fase 1, o es nice-to-have?
4. ¿La integración SAP_COM_0316 ya quedó habilitada por Sofos? (estado depende de Arnaldo Parra)
5. ¿Pilot scope — 5 clientes? 10? ¿Quiénes?

---

## After the meeting

- If Claudia greenlights v1 scope expansion (multi-pay + estado de cuenta + BCV widget + aging) → update `counterparty-portal-prd.md` "v1 scope" table the same day
- Capture Procurement module commitment (or non-commitment) → add to CAPCA blueprint Fase 4 placeholder
- If retenciones move into v1 → coordinate with Mariel on SENIAT spike
- Update `sales/clients/capca.md` engagement log

---

## Cross-ref

- Source: `rosa-vision-doc-2026-04-24.md`
- Master CAPCA blueprint: `customer-experience/playbooks/blueprint-operativo-capca.md`
- Tesote portal spec: `product/tesote-pay/plans/counterparty-portal-prd.md`
- HTMLs being rebuilt: `product/tesote-pay/prototypes/pro-112/{claim-flow-capca,workspace-capca}.html`
- Retenciones thread: `product/seniat-retenciones-process-mariel-review.md`
- Fireflies (Rosa, 2026-04-24): <https://app.fireflies.ai/view/01KPTRCQGMVGZQNSZ70WW391AC>
- Caracas trip context: `strategy/caracas-trip-2026-04-26.md`
