---
title: PRO-112 Engineering Handoff Packet — Workspace Cobros + Counterparty Claim Flow
tags: [product, tesote-pay, tesote-negocios, cobros, counterparty-portal, pro-112, handoff]
updated: 2026-04-25
audience: Dan (engineering), Luis (product)
scope:
  - Workspace Cobros (sender side) — full v1 spec
  - Counterparty claim flow (payer side) — full v1 spec, native pay flow built
status: Both streams ready for engineering review
---

# PRO-112 Engineering Handoff Packet

> Two parallel streams: **workspace Cobros** (the sender experience for outbound invoices) and the **counterparty claim flow** (the payer experience for inbound invoices). Both are at engineering-handoff quality as of 2026-04-25.
>
> The counterparty side just gained a full **native 4-step pay flow** (BNC ACH direct debit, per-transaction OTP) that was deferred at the original 2026-04-23 review point.
>
> **Two artifacts per stream, except the counterparty side has no separate written spec — the prototype is the spec.** The workspace side has both because the engineering build is bigger and the data/state model needs prose. For anything counterparty-related, walk `claim-flow.html`; the locked decisions and open questions are summarized in Stream 2 below.

---

## At a glance

| Stream | Prototype | Written spec | Status | Open product Qs |
|---|---|---|---|---|
| **Workspace Cobros** | [`workspace-shell.html`](workspace-shell.html) | [`cobros-spec.md`](../../plans/cobros-spec.md) | Frozen at 2026-04-23 review point | 10 (see spec §9) |
| **Counterparty claim flow** | [`claim-flow.html`](claim-flow.html) | — (prototype is the spec; see Stream 2 below) | Pay flow + auth locked 2026-04-25 | 3 + structural (Stream 2) |

Both prototypes share a visual system (Mercury pastel pills, 96px button width, 5px radius, etc.). When you find drift, **`claim-flow.html` is canonical**; workspace-shell follows.

---

## Read in this order

1. **[`claim-flow.html`](claim-flow.html)** — counterparty prototype. Walk it (see Stream 2 below).
2. **[`cobros-spec.md`](../../plans/cobros-spec.md)** — workspace-side spec. ~810 lines. (Note frozen-status banner at top.)
3. **[`workspace-shell.html`](workspace-shell.html)** — workspace prototype. Walk it (see Stream 1 below).

Doing the counterparty side first means you'll know what the workspace side has to integrate with (paid-state webhook, comprobante metadata) by the time you reach the Cobros spec.

---

## What's in this folder

| File | What it is |
|---|---|
| `README.md` | You are here. |
| `claim-flow.html` | **Canonical** counterparty prototype. Email → login → portal → 4-step pay flow → success. The prototype is the spec for the counterparty side; locked decisions and open questions are summarized in Stream 2 below. |
| `workspace-shell.html` | **Canonical** workspace prototype. Cobros + Inicio + Contrapartes + ERP connect wizard + Nuevo cobro overlay + side panel + cancel/email-capture modals. |

Brand-styled variants exist locally (`claim-flow-brand.html`, `claim-flow-brand-comprobantes.html`, `workspace-shell-brand.html`) but lag the canonical files and aren't part of this engineering handoff.

**Referenced by this packet:**

- `../../plans/cobros-spec.md` — workspace spec.

---

# Stream 1 — Workspace Cobros

The sender-side experience for creating, sending, tracking, and reconciling outbound invoices / payment requests. Authoritative spec is [`cobros-spec.md`](../../plans/cobros-spec.md).

## How to use `workspace-shell.html`

Black **dev strip** at the top with three switchers (dev-only — disappears in production):

- **Rol** — Workspace (default) / Contraparte activa / Contraparte sin activar. Toggles the chassis between three personas. Most of this stream is the Workspace view.
- **Vista** — Inicio / Negocios · Pagos / **Negocios · Cobros** / Crear cobro / Conectar ERP. The prototype is focused on Cobros; the others are scaffolding (Inicio, Pagos) or v1 flows reachable in context (Crear cobro via overlay; Conectar ERP wizard).
- **Estado Cobros** — Normal / Vacío / Sincronizando / Error ERP. Switches the Cobros screen between its four launch-relevant states.

### Recommended walkthrough (5 min)

1. Land on **Cobros** (default). Observe the 9 seeded rows, every state represented at least once (borrador · enviada · vista · aprobada · vencida · pagada).
2. Click **`Kaizen Logística`** row → side panel opens. Scroll through Detalles / Contacto / Enlace / **Recordatorios enviados** / Historial. Notice the panel footer varies by state.
3. Click the bell → row-level **Recordar** → a toast fires and the reminder history increments. Try again → it's blocked ("Ya enviaste un recordatorio hoy") because of the 1-per-day cap.
4. Click **`MARCAS PROPIAS`** row (vencida). See the amber banner, pre-seeded 2 reminders. Click **Reenviar** in panel → fresh token, state flips to `enviada`, toast confirms.
5. Click `+ Nuevo cobro` top right → full-screen overlay. Type a name that doesn't match any existing counterparty → hit `Crear "…" como nueva contraparte` → toggle Empresa / Persona → fill in RIF/Cédula → back to form. Enter a monto with `18450` → watch the Venezuelan formatting auto-apply. Submit → success screen with copyable link → `Ver en Cobros` → new row flashes in at the top.
6. Click the **Enviar** button on `PRIMERA FACTURA, S.A.` row (no email on file) → email-capture modal. Enter an email → submit → state flips, toast fires.
7. Dev strip → **Conectar ERP** → walk through all 4 steps. Step 4 animates a mock import from 0 → 8,137 facturas.
8. Dev strip → **Estado Cobros** → toggle through Vacío / Sincronizando / Error ERP to see launch-critical non-happy states.

### Notable interactions

| Thing | How it fires |
|---|---|
| Open side panel | Click any Cobros row |
| Navigate to a Contraparte 360 | Click any client name in any Cobros / Contrapartes row |
| Send an invoice (with email) | Click `Enviar` on a borrador row → instant send + toast |
| Send an invoice (no email) | Click `Enviar` on a borrador row without email → capture modal |
| Remind | Click `Recordar` on row OR bell icon in panel footer |
| Resend (new link) | `Reenviar` in panel footer (visible on fallida/vencida/link_expirado) |
| Mark paid | Panel footer `Marcar pagada` (demo shortcut — real flow is via BNC webhook) |
| Cancel — 3 variants | Panel footer `Cancelar cobro`. Modal copy adapts to state. Cmd+1/2/3 forces specific variant for demo |
| Exit Nuevo cobro with unsaved data | ESC or X → confirmation modal "¿Salir sin enviar?" |

## What's locked (captured in `cobros-spec.md`)

- v1 ERP integration scope: **Odoo only** (SAP v2)
- Currency: **VES only**
- Permission model: **single workspace-member role**; multi-role is v2
- Email sourcing: **ERP pre-fill, Tesote confirm** (spec §5.3)
- Counterparty tax-id type: **Empresa (RIF) or Persona (Cédula)** via toggle in creation form
- Reminders: **manual only in v1**, rate-limited to **1/day, 10 lifetime**  (prototype). *Note: spec §5.5 currently says 1/hour; see "Known spec-prototype drift" below.*
- Payment link TTL: **30 days** (spec §5.11)
- Out of v1: bulk actions, partial payments, dispute resolution UI, refund flow, auto-create-link from every ERP invoice, multi-currency, team approvals
- The **Cobros origen** column is plain text (`Odoo` / `SAP` / `Directo`), no chip
- Counterparty rows in Cobros: **no avatars**; only a minimal status icon — blue check (en red Tesote) / grey question (sin activar)

## Open — still need product input (`cobros-spec.md` §9)

Ten decisions Dan needs from Luis before sprint kickoff. Summary:

1. Soft vs. hard delete from borrador
2. Link TTL configurable per workspace?
3. Reminder backoff curve (spec says 1/hour; prototype uses 1/day — reconcile)
4. Multi-email per counterparty
5. Bulk-send with missing emails — surface or block?
6. `procesando` visible as its own state or nested under `aprobada`?
7. Counterparty dispute reason privacy
8. ERP writeback scope — paid flag only or journal entries?
9. Workspace can self-pause Odoo sync?
10. Audit log retention

See spec §9 for each with my recommendation.

## Known prototype limitations (not product decisions)

So Dan doesn't mistake scrappy prototype behavior for design intent:

1. **No persistence.** Refresh = reset. Everything lives in memory (`ROW_DATA` in `<script>`).
2. **Contraparte 360 is half data-driven.** Header populates from the clicked client; summary stats (Bs. 45,200 por cobrar, 3,1 días plazo, etc.) and the facturas table below still show Kaizen's numbers regardless. Real data-wiring TBD.
3. **Inicio (home) is static.** Cards don't reflect live state from `ROW_DATA`. The screen is illustrative of the chassis, not a launch-ready dashboard.
4. **Pagos is scaffolding, not spec'd.** A Pagos screen is present in the prototype because the workspace shell needs it, but **`cobros-spec.md` explicitly excludes Pagos from v1 Cobros scope**. Pagos gets its own spec before building.
5. **Filter + Agrupar dropdowns open but don't actually filter.** Illustrative only.
6. **Search input accepts typing but doesn't filter rows.**
7. **Side-panel PDF button** just toasts. Real PDF generation is a real engineering task.
8. **Dispute reason** in the banner ("monto incorrecto en factura") is hardcoded. Real dispute text comes from the counterparty portal.
9. **ERP wizard step 2** shows a credentials form but doesn't actually test the connection. Step 4's import is a mock animation.
10. **Panel mock email** shows "confirmado" regardless of whether the email is actually `erp_confirmed` or `user_entered` in the data. Refinement if it matters.
11. **Cancel from `aprobada`** doesn't pre-flight-check BNC (the spec describes this; prototype just cancels). Handle in real build.
12. **The email-capture modal** is wired for one specific row (`PRIMERA FACTURA, S.A.`) but the logic works for any row without `cpEmail`. New rows created via Nuevo cobro with no email will go through the same flow when Enviar is clicked.
13. **The "Contraparte activa / sin activar" role toggle** in the dev strip shows a thin preview of what a counterparty claimant would see using the same workspace chassis. It's **not** the real payer experience — see Stream 2 below for that.

## Known spec-prototype drift

Tracked here so we can reconcile before Dan starts:

| Item | Spec says | Prototype does | Action |
|---|---|---|---|
| Reminder rate limit | §5.5: 1 per hour, 10 lifetime | 1 per day, 10 lifetime | Luis's latest preference is 1/day. Update spec §5.5 + §7.9 toast copy. |
| Success state after send | §5.3 ends at state transition; doesn't show a success screen | Prototype adds a full success screen with copyable link | Codify in spec §5.2 / §5.3 — it's good UX that's now standard. |
| Counterparty `tax_id_type` | §3.1 `Counterparty` has `rif` field only | Prototype supports RIF (Empresa) and Cédula (Persona) via toggle | Add `tax_id_type` enum to `Counterparty` in spec §3.1; clarify that `rif` field stores either. |
| Exit confirmation for Nuevo cobro | §5.2 doesn't specify | Prototype prompts "¿Salir sin enviar?" when form has data, no Guardar-borrador button | Add to §5.2. |
| Minimum visual state indicator on rows | Spec doesn't mandate | Blue check / grey question icon next to counterparty name | Add to §7.3 / §7.4 — minor copy + visual commitment. |

## Out of scope for Cobros v1

- **Tesote Capital** — deferred, see PRO-112 epic G.7.
- **Tesote IA** — beta teaser in the chassis, no functionality.
- **Retentions engine** — IVA/ISLR handling, SENIAT XML export, comprobantes generation. PRO-112 epic E.
- **Bulk actions, partial payments, refund UI, dispute resolution UI** — all deferred per `cobros-spec.md` §1.
- **Pagos** (workspace AP-side) — scaffolding only; gets its own spec.

## Data model at a glance

Full field lists in `cobros-spec.md` §3. Prototype mirrors these entities in the `ROW_DATA` JS object for demo purposes.

```
Cobro            — id, workspace_id, counterparty_id, amount_ves, concept,
                   invoice_number, origin (odoo/directo), state, timestamps,
                   payment_link_token, receiving_account_id

Counterparty     — id, workspace_id, legal_name, rif, primary_email_id,
                   tesote_network_status, origin (odoo/directo/manual)
                   [+ tax_id_type enum per drift table]

EmailRecord      — id, counterparty_id, email, source (erp_imported /
                   erp_confirmed / user_entered), confirmed_at

Reminder         — id, cobro_id, sent_at, sent_by_user_id, channel

Event            — id, cobro_id, event_type, occurred_at, actor_type,
                   actor_id, payload (jsonb)
```

Every state transition emits an `Event`. The side-panel Historial timeline is the user-visible projection of the event stream.

## State machine (read from `cobros-spec.md` §4)

```
borrador ──Enviar──> enviada ──(counterparty opens)──> vista
                         │                                │
                         │                                └──(counterparty approves)──> aprobada
                         │                                                                   │
                         ├──(due passes)──> vencida                                          │
                         ├──(30 days)──> link_expirado                                       │
                         └──Cancelar──> cancelada                                            │
                                                                                             │
                                            procesando ◄──(BNC ACK)──────┐                  │
                                                │                        │                  │
                                                ├──(BNC ok)──> pagada    └──────────────────┘
                                                └──(rejected)──> fallida
```

All 11 states covered in the prototype side panel with their respective banners, timelines, and footer actions.

## Suggested engineering ticket sequence

From `cobros-spec.md` §10 — 17 tickets, sequenced. TL;DR order:

1. Data model & migrations
2. Cobros CRUD + state machine API
3. Odoo sync worker (integration against staging)
4. Cobros list UI
5. Create Directo flow
6. Send flow (email-on-file silent + modal flow for missing email)
7. Side panel + timeline
8. Reminder + resend (with rate limits)
9. Cancel + edit with state-specific copy
10. Payment webhook handlers
11. ERP writeback worker
12. Link expiry cron
13. Failure handling
14. Bulk actions
15. Empty / loading / error states polish
16. Permissions & cross-tenant tests
17. Perf & scale

Parallelizable after #4: copy & design QA, and Stream 2 build.

---

# Stream 2 — Counterparty Claim Flow

The payer-side experience: how a counterparty receives an invoice, signs in, lands in the portal, and pays. **The prototype `claim-flow.html` is the spec** — walk it to understand the design, and the subsections below summarize what's locked, what's open, and known prototype limitations.

## How to use `claim-flow.html`

Black **dev strip** at the top has three controls:

- **Screen tabs** — `1 · Email` / `2 · Login` / `2b · Verificar correo` / `3 · Phone (first run)` / `4 · Portal app`. Direct jumps for demos.
- **`↺ Reset payer profile`** — wipes saved bank accounts in `PAYER_PROFILE` (in-memory). Useful to re-demo the first-time pay path.
- **Payer state** segment — `First-time` / `Returning`. Toggles which login variant Screen 2 renders.

### Recommended walkthrough (5–7 min)

1. **Tab 1 (Email).** Gmail-rendered invoice email from APB Group. Copy is locked (subline `Revisa los detalles y paga de forma segura desde tu portal de cliente`; footer `Tesote · Venezuela`). Click `Ver factura →`.
2. **Tab 2 (Login) — first-time.** Default state. Email pre-filled to `pagos@kaizen.com.ve`. `Continuar →` lands on phone capture.
3. **Tab 3 (Phone).** WhatsApp number capture. Skippable. `Saltar por ahora` → portal.
4. **Tab 4 (Portal app).** Inicio: `Hola, Kaizen Logística` greeting + Personalizar, two quick actions (`Pagar factura` primary / `Habla con ventas` lock-icon), Facturas-por-pagar card (Bs. 42.890 / 3 facturas, 3 preview rows AP/CA/MP), 2×2 locked teasers (Connect / Auto / Capital / IA).
5. **Sidebar.** `Inicio` (active) · `Pagos ↑ (4)` · `Cobros ↓` (locked) · `Contrapartes` (active). Tesote Connect = `Saldos` + `Transacciones` (both locked). All other pillars locked.
6. **Pay flow (the highlight).** Click any row's `Pagar` button → 4-step overlay:
   - **Step 1.** Aprobar default account; or `+ Usar otra cuenta` → Empresa/Persona toggle, type any 20-digit account number → bank auto-detects from first 4 digits → fill RIF/Cédula/phone/holder (any format) → Aprobar.
   - **Step 2.** Type any 6 digits in the OTP cells → auto-advances → Confirmar pago.
   - **Step 3.** ~1.8s spinner.
   - **Step 4.** Animated thin checkmark draws in (circle then check, ~0.95s total). Sub copy: *"Pagaste {monto} a {vendor}. Le notificamos del pago a tu proveedor y te enviamos el comprobante por correo."* Comprobante card with 6 rows: Referencia / Fecha / Método / Factura / Concepto / Monto. `Volver al portal` → row in Pagos table flips to `Pagada` pill + ghost `Ver comprobante` action.
7. **Returning login flow.** Click `↺ Reset payer profile`. Toggle `Payer: Returning`. Click email link `Ver factura →` → Tab 2 now renders the Tesote sign-in surface (single column, "Inicia sesión en Tesote", `Enviar código →`) → Tab 2b OTP screen → enter any 6 digits → `Verificar →` lands directly in portal (skips phone capture, since returning users already have it on file).
8. **Sales CTA.** Click any of the three `Habla con ventas` buttons (topbar, Inicio quick action, locked Connect card) → toast: *"Recibimos tu interés. Un asesor de ventas te contactará pronto."*
9. **Cancel paths.** Step 1 ESC/X/Cancelar → closes immediately. Step 2 ESC/X/Cancelar → "¿Cancelar el pago?" confirm modal. Steps 3–4 ESC closes silently.

### Notable interactions

| Thing | How it fires |
|---|---|
| Open invoice side panel | Click any Pagos row or Inicio preview row |
| Pay an invoice | Row `Pagar` button OR side-panel `Aprobar y pagar` / `Pagar ahora` |
| Save a new account | First-time pay flow — saved automatically in `PAYER_PROFILE` on success |
| Surface saved accounts | Second pay — radio cards in step 1, with Empresa/Persona chip |
| Demo first-time pay again | `↺ Reset payer profile` button (dev strip) |
| Switch login persona | `Payer: First-time / Returning` segment (dev strip) |
| Talk to sales (BNC) | Topbar `Habla con ventas` / Inicio quick action / locked Connect card |

## What's locked

**Auth model.** First-time = email-only sign-up (no verification — signed URL is the access gate). Returning = email + 6-digit OTP. **No passwords, ever** (payers aren't Tesote customers).

**Pay flow.** 4 steps, BNC ACH direct debit, **per-transaction OTP always** (no standing authorization in v1). Account-type toggle: **Empresa (RIF) → BNC only**, **Persona (Cédula) → any Venezuelan bank**. Bank discovery via **auto-detect** from first 4 digits of account number (no dropdown). Account format **exactly 20 digits**, phone **exactly 11 digits**. RIF/Cédula/phone accept any user format, normalized internally. Method label `Débito Inmediato` (not "Débito ACH"). Aprobar button **always primary blue**, never red.

**Success state.** Animated thin draw-in check (circle then check via stroke-dashoffset). Sub copy mentions vendor was notified. Comprobante shows 6 rows including Concepto + Monto.

**BNC connect.** Sales-led for v1 (`Habla con ventas` toast on all three CTAs). Self-serve "Powered by Tesote" OAuth wizard is **v1.1**. The wizard was scoped, drafted, and scrapped pre-build in favor of shipping the pay flow first; existing saved accounts in `PAYER_PROFILE` will migrate to a real BNC connection on activation, no data loss.

**Sidebar lock state.** Active: Inicio + Pagos + Contrapartes. Locked: Cobros + Saldos + Transacciones + Conexiones bancarias + Contabilidad + Reportes + Capital + IA + the entire Espacio de Trabajo group (Mi equipo, Permisos, Configuración) — admin doesn't apply to payers, but the section mirrors the workspace-side IA so the chassis stays consistent.

**Visual system.** Mercury pastel pills (lavender / amber / salmon / mint / gray; filled bg, no border, dark text, 5px radius). Pill + button uniform 96px width, padding 3px 8px, font 11px. Same as workspace-shell.

## Open — still need product input

Three product decisions:

1. **Brand split** — separate brand `tesotenegocios.com` vs subdomain `portal.tesote.com` vs same app. Prototype mocks separate brand. Decision affects domain, lockup, marketing.
2. **First-login empty state** — just-the-invoice vs SENIAT-resolved historical txns vs cross-workspace outstanding invoices. Recommended: just-the-invoice in v1.
3. **Multi-RIF at Tier 1** — one email tied to multiple RIFs (personal cédula + company J-RIF). Deferred unless it blocks v1.

Plus structural ones for engineering scoping:

4. **Codebase split** — separate service vs. logged-out view of `app.tesote.com`.
5. **Inbox data model** — invoice data lives on sender side vs. dedicated counterparty inbox.
6. **SENIAT lookup SLA** — for company-name pre-fill on the landing page.
7. **Webhook contract** — workspace → portal: paid state echo + comprobante metadata. **Cross-stream — see Shared concerns below.**

## Known prototype limitations (not product decisions)

1. **No persistence.** Refresh = full reset. `PAYER_PROFILE`, invoice state, etc. all in memory.
2. **No real BNC OAuth.** Saved accounts are just `(bank, last4, holder, rif, phone, accountType)` tuples. Production flow requires the v1.1 wizard.
3. **Wrong-OTP / bank-rejection / OTP-timeout** — caught and toasted, but no design for the error states yet (v1.1 scope).
4. **Comprobante PDF download** — toast stub. Real generation is engineering work.
5. **Disputar action** in side-panel footer → toast stub.
6. **Email verification intentionally absent** on first-time (signed URL is the access gate); returning is OTP only.
7. **Invoice detail screen** — not yet drafted. Side panel is the only invoice view in v1.
8. **Comprobantes / retenciones tab** — deferred. SENIAT spike lives in a separate scope.
9. **Counterparty 360 from payer's POV** — clicking a proveedor in Contrapartes doesn't open a detail page.
10. **Notification + settings icons** in topbar are visual only.
11. **Payer-state toggle** is a dev-strip affordance; in production, the server detects first-time vs. returning via the signed-URL token + session cookie / device record.

## Out of scope for v1 (counterparty)

- **Cobros from the counterparty side** (sending invoices back to the workspace) — v1.1.
- **Comprobantes / retenciones tab** — v1.1; SENIAT spike lives separately.
- **Real-time BNC paid-status webhook on the payer side** — v1 trusts the synchronous response; v1.1 reconciles via the sender's BNC feed.
- **Multi-invoice / bulk pay** — v1.1.
- **Refund flow** — v1.1.
- **Standing authorization / "trusted account" opt-out of OTP** — explicitly out of v1 (per-transaction OTP always).

---

# Shared concerns

## Visual system (must stay in sync between both prototypes)

These are the cross-prototype invariants. Drift here is a bug.

| What | Spec |
|---|---|
| **Pills** | Mercury pastel — filled background, no border, dark text, 5px radius. Lavender / amber / salmon / mint / gray. |
| **Pill + button uniform width** | 96px (`min-width` for pills, fixed `width` for buttons), padding 3px 8px, font 11px. |
| **Acción column header** | Labeled `Acción`, content centered in cell. |
| **Date columns** | `white-space: nowrap` for Emitida / Vence. |
| **Account number formatting** | 20 digits, no separators in input. |
| **Phone formatting** | 11 digits, no separators in input. Display as `04XX XXX XXXX` where shown. |
| **Sidebar — Tesote Connect** | Three items in order: `Saldos` + `Transacciones` + `Conexiones bancarias` (all locked on counterparty side, all unlocked on workspace side). Never collapsed. |
| **Sidebar — Tesote Automatizaciones** | Two items in order: `Contabilidad` + `Reportes` (both locked on counterparty side, both unlocked on workspace side). |
| **Sidebar — Tesote Negocios** | `Pagos` with **up arrow** (money outgoing) + `Cobros` with **down arrow** (money incoming). Lock state inverts between streams. |
| **Sidebar — Espacio de Trabajo** | New bottom section after Tesote IA. Three items in order: `Mi equipo` + `Permisos` + `Configuración`. All unlocked on workspace side; entire section locked on counterparty side (admin doesn't apply to payers — section is mirrored only for chassis consistency). |
| **BNC CTA copy** | `Habla con ventas` everywhere in v1. The phrase `Conectar mi banco` is dead. |

`claim-flow.html` is the source of truth for any conflict. Workspace-shell follows.

## Cross-stream contract (workspace → portal)

The two streams communicate via a webhook + state-echo pattern that's referenced from both docs but not yet specced end-to-end. **This is the single biggest cross-stream coordination point and needs a co-spec session.**

Rough shape (provisional):

1. Workspace sends `Cobros.send` event when a `Cobro` enters `enviada`.
2. Portal materializes the invoice into the counterparty's inbox.
3. Counterparty pays in the portal (4-step flow above) → portal triggers BNC debit on the workspace's BNC connection.
4. Portal echoes back `Cobros.paid` with comprobante metadata (referencia, fecha, método, monto).
5. Workspace's Cobros UI updates the row state (`aprobada → procesando → pagada`) and surfaces the comprobante in the side-panel `Comprobante` tab.

Currently referenced in `cobros-spec.md` §3 (Counterparty + Event entities). Action: schedule a co-spec session before any of the payment-webhook tickets (Cobros §10 ticket #10) start.

---

## Where to discuss / file feedback

- **Product / scope questions** → Luis (`luis@tesote.com`), or comment on the Notion mirror of the spec.
- **Engineering / API / data questions** → PRO-112 Linear issue comments.
- **Prototype bugs or missing flows** → tell Luis; small fixes are cheap, bigger gaps we'll scope.

---

*Last updated 2026-05-01. When things change materially (new locked decisions, new flows built, scope adjustments), update this doc and the relevant spec together.*

**2026-05-01 update** — Sidebar IA expanded to preserve features that exist in current production but were missing from the v1 prototype: `Conexiones bancarias` (Tesote Connect), `Reportes` (Tesote Automatizaciones), and a new bottom section `Espacio de Trabajo` with `Mi equipo` / `Permisos` / `Configuración`. Workspace-side fully active; counterparty-side mirrors as locked placeholders per the existing chassis-consistency rule. Files touched: `workspace-shell.html`, `workspace-capca-2.html`, `claim-flow.html`, `claim-flow-capca-2.html`. Legacy `*284.html` variants left untouched.
