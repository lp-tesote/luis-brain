---
title: Counterparty Portal — PRD (v1, ready for engineering)
tags: [product, tesote-pay, tesote-negocios, counterparty-portal, prd]
updated: 2026-04-25
author: Luis Pulgar
status: Ready for Dan review — pay flow + auth locked, 3 product Qs open
---

# Counterparty Portal — PRD

> **Purpose.** Lock the v1 scope, information architecture, and visual direction of the counterparty-facing portal (domain: `tesotenegocios.com` — subject to change). This PRD reconciles three threads that currently diverge:
>
> 1. `prototypes/future.html` — the existing "portal" view Luis built (guest checkout + dashboard sketch for payment links).
> 2. `prototypes/pro-112/claim-flow.html` — the Tier 0→1 claim flow matching Dan's A.1–A.4 (no email verification in v0, WhatsApp-based notifications).
> 3. [PRO-112](pro-112-dan-super-app.md) — Dan's broader 3-tier super-app framing (invoice-first, retentions, capital, graduation).
>
> Goal of this doc: decide what the first-login counterparty portal *is*, so we can design and build it without re-relitigating the scope on every screen.

---

## Product positioning

**Working name:** Tesote Negocios (separate brand from "Tesote Pay") — to be confirmed.

**Elevator line:**
> La red donde las empresas se conectan, se facturan y se pagan entre sí. Ve todas las facturas de tus proveedores y clientes en un solo lugar.

**Who is this for?**
The **counterparty** — an empresa that receives invoices and/or payment requests from one or more Tesote workspaces. They do not have (and do not need) a full Tesote workspace.

**Acquisition wedge:**
A Tier 2 workspace sends them an invoice. Email CTA: *"Ver factura →"* — no mention of claims, sign-up, or portal in the outbound email. The portal is the payoff, not the ask.

---

## v1 scope — what's in, what's out

### In scope (v1)

| Area | What |
|---|---|
| **Auth** | Two flows: first-time = email-only sign-up (no verification); returning = email + 6-digit OTP. No passwords ever — payers aren't Tesote customers. (See "Auth — first-time vs returning" below; locked 2026-04-25.) |
| **First-run onboarding** | Optional WhatsApp number capture. Skippable. |
| **Inbox** | List of invoices received across *all* Tesote senders (unified). |
| **Invoice detail** | Read-only: line items, IVA, net due, sender info, PDF download. |
| **Payment** | **Native 4-step pay flow** (Revisar → OTP del banco → Procesando → Éxito), BNC ACH direct debit. Saved-account on second pay. Per-transaction OTP, always. No standing authorization in v1. (See "Pay flow" below; locked 2026-04-25.) |
| **Multi-invoice pay** | Checkbox column on Pagos table; sticky bottom bar with `Pagar seleccionadas →`; bundled into a single BNC debit. Per-row `Pagar` still works for single-invoice case. One Cobro row per invoice on the workspace side; group identified by a shared `payment_batch_id`. (See "Multi-pay" below; locked 2026-04-29.) |
| **Contraparte 360 (read-only)** | Click any Contrapartes row → detail page (full route, not side panel) with header, resumen card, 12-month pago/facturación chart, full historial de facturas, and Estado de cuenta download (PDF/Excel stubs in prototype). |
| **Payment terms display** | Read-only display of agreed payment terms across surfaces — Pagos table `Plazo` column; side-panel Detalles `Términos de pago` line; Contraparte 360 Resumen card `Plazo otorgado` + `Plazo promedio de pago`. Display-only; no early-pay discount or propose-a-plan UX in v1. |
| **BNC upgrade nudge** | "Habla con ventas" CTA — sales-led activation. The full self-serve "Powered by Tesote" OAuth wizard is **v1.1**. (See "BNC connect — sales-led for v1" below.) |
| **Profile** | Minimal — email, phone, company name (pre-filled from SENIAT if available). |

### Out of scope (v1)

- Retentions engine (epic E of PRO-112) — no auto-calc, no comprobantes issued from the portal.
- Multi-entity / multi-RIF profile switching.
- Tesote Capital, ERP integrations, team roles, API — all Tier 2 gates.
- Self-serve "Powered by Tesote" BNC connect wizard — v1.1 (sales-led only in v1).
- Search, filters, sorting.
- Wrong-OTP / bank-rejection / OTP-timeout error paths (caught and toasted in v1; specced fully in v1.1).
- Refund flow.
- **Partial payment** — deferred to v1.1. Requires a `parcial` invoice state, an abono ledger, and partial-clearing logic in SAP FI. Holding until customer demand surfaces; if Claudia or another v1 customer asks explicitly we revisit. Do not add a "monto a pagar" input on the invoice row.
- Early-pay-discount and propose-a-plan flavors of payment terms (display-only flavor is in v1).

### Explicitly deferred decisions

See "Open decisions" section.

---

## Information architecture

### Sidebar (locked 2026-04-25 — see `claim-flow.html`)

The counterparty chassis mirrors the workspace shell, but most products are locked. Active items in v1:

```
INICIO ─────────────────────────  active (default landing)

TESOTE NEGOCIOS
  Pagos  ↑ (4)         active     ← outstanding invoices to pay
  Cobros ↓             locked     ← v1.1; payers don't send invoices yet
  Contrapartes         active     ← payee directory

TESOTE CONNECT (locked)
  Saldos               locked     ← unlocks via BNC connect (sales-led, v1)
  Transacciones        locked

TESOTE AUTOMATIZACIONES (locked)
TESOTE CAPITAL          (locked)
TESOTE IA               (locked beta)
```

Arrow direction is meaningful: **Pagos = up** (money outgoing), **Cobros = down** (money incoming). The "Tesote Connect" item splits into **Saldos** + **Transacciones** as two separate locked entries (matches the unlocked workspace pattern).

### Inicio (default landing)

1. **Hero greeting** — `Hola, {company-name}` + Personalizar button.
2. **Two quick actions** — `Pagar factura` (primary blue, routes to Pagos) + `Habla con ventas` (lock icon, opens sales toast — see BNC-connect section).
3. **Facturas por pagar card** — total Bs. + count + 3 preview rows (avatar-prefixed) + `Ver todo →` to Pagos.
4. **2×2 locked teasers** — Tesote Connect, Automatizaciones, Capital, IA. Each has a `Habla con ventas` CTA (Connect) or `Ver qué incluye` / `Pronto` / `Unirme a la beta` (others).

### Pagos screen

Outstanding invoices table — sender, concepto, monto, vence, estado, acción. Per-row pay action opens the 4-step pay flow overlay. State pills use Mercury pastel (lavender / amber / salmon / mint / gray); pill + button uniform 96px width. Acción column header label is `Acción`, content centered. Date columns are `nowrap`.

### Contrapartes screen

Directory of proveedores + clientes the counterparty has transacted with through Tesote. Same row-density pattern as Pagos. Clicking a row opens the Contraparte 360 detail (see "Contraparte 360" section below).

### Deliberate omissions vs. `future.html`

`future.html` includes bulk pay, CSV export, reconciliation banner. These are **deferred to v1.1**, after we validate the email → portal → pay → repeat loop actually drives activation.

---

## Open decisions (lock before build)

### 1. Can the counterparty *pay* from the portal in v1?

**Resolved 2026-04-25 — option (c), native pay flow.** The 4-step BNC ACH overlay is built and replaces the earlier "(b) reuse the sender's payment-link" recommendation. Rationale: the payment-link flow assumes a fresh URL per invoice and a one-shot guest checkout; the portal model breaks that — payers see *all* their invoices in one place, expect saved bank accounts on the second pay, and need a unified UX. Reusing the legacy flow would have forced a re-auth + re-collect-bank-info loop on every invoice. See "Pay flow" section below for locked decisions.

### 2. Email verification — really not in v0?

**Resolved 2026-04-25** — see "Auth — first-time vs returning" below. Verification is split by session type:
- **First-time:** no verification at the acquisition moment (preserves the 2026-04-23 decision; URL is long and signed, friction stays off the funnel).
- **Returning:** email-OTP required on every re-auth (because the URL is no longer the access gate — the payer comes back via the regular sign-in surface).

### 3. Is "Tesote Negocios" a real brand split from "Tesote Pay"?

Options:
- **(a)** Separate brand, separate domain (`tesotenegocios.com`), separate visual lockup. Clean counterparty identity, insulates Tesote's main brand from any counterparty support issues. Marketing overhead.
- **(b)** Same brand, subdomain (`portal.tesote.com`). Simpler.
- **(c)** Same app entirely — counterparty is just "logged out view" of `app.tesote.com`. Conflicts with tier separation.

Dan's PRO-112 recommends (a) or (b). `claim-flow.html` currently mocks (a).

### 4. What's the primary "empty state" for a first-login counterparty?

Most counterparties hit the portal because they got one invoice. What do they see as state #2 onward?
- Only the one invoice? Can feel sparse.
- That invoice + any historical BNC txs we can match to their RIF via SENIAT lookup? Richer, but may surface payments they don't expect Tesote to know about.
- That invoice + outstanding invoices from *other* Tesote workspaces they already transact with (the network-already-exists play from PRO-112's data memo)? Powerful but requires cross-workspace resolution at login.

**Recommendation:** just the invoice they came for, in v1. Layer on cross-workspace surfacing in v1.1 once we see how people respond to the basic portal.

### 5. Multi-RIF at Tier 1 (from PRO-112)

A single person may have a personal cédula RIF and a company J-RIF. One login, switch profiles? Two logins? Deferring — unlikely to block v1 if we assume one email → one RIF.

---

## Auth — first-time vs returning (locked 2026-04-25)

The counterparty portal has **two distinct auth flows**, gated by whether the visitor is a known payer:

### First-time flow (sign-up at acquisition)

Trigger: payer arrives via a signed invoice URL (`tesotenegocios.com/i/<token>`) and we don't recognize them.

Steps:
1. **Landing card** — aside teaser ("Tienes una factura nueva") + email input pre-filled from the workspace-confirmed counterparty record. No password field. Copy: *"Ingresa para ver tu factura · Usa tu correo de empresa. Sin contraseñas."*
2. **Continuar →** creates the payer record and drops them into the (skippable) WhatsApp capture screen, then the portal.
3. **No email verification.** The signed URL is the acquisition gate — adding a code here kills funnel without buying real security at the moment of first contact.

### Returning flow (re-auth on subsequent visits)

Trigger: payer comes back to the portal *not* through a freshly-signed invoice URL — e.g. they bookmarked it, typed `tesotenegocios.com`, or clicked a "view portal" link in a notification email.

Steps:
1. **Sign-in card** — single-column, framed like the standard Tesote sign-in surface. Copy: *"Inicia sesión en Tesote · Te enviaremos un código de 6 dígitos a tu correo. Sin contraseñas — los pagadores no necesitan crear una cuenta de Tesote."* Email field only.
2. **Enviar código →** generates a 6-digit OTP and emails it to the address on file.
3. **OTP screen** — same `auth-card` chassis, 6-cell input, `Reenviar código` / `Cambiar correo` helpers. Code expires in 10 minutes.
4. **Verificar →** lands directly in the portal (skip phone capture — returning user already has it on file or skipped it).

### Why no password (ever)

Payers aren't Tesote customers. Asking them to set and remember a password for an app they may visit twice a year is wrong-shaped friction; it also implies an account-management surface (reset, change, etc.) that we don't want to build or support for non-paying users. Email-OTP gives us a re-auth signal that matches the use cadence and reuses an inbox we already know they read.

### Why verification only on returning

The signed invoice URL is *itself* the verification on first contact — possession of the URL is the proof. Once the payer's session ends and the URL is no longer the entry point, we lose that proof and need a fresh one. Email-OTP is the cheapest replacement.

### Detection (how the portal decides which flow to show)

In v1 the prototype gates on a body data-attribute (`data-payer="first-time"|"returning"`) toggled from the dev strip. In production:
- **First-time** = arrival via `/i/<token>` with no matching session cookie / device record for that email.
- **Returning** = arrival via `/login`, OR arrival via `/i/<token>` where we already have a recent authenticated session for that email.

### Out of scope for v1

- Multi-device session management (one active session per email; signing in elsewhere silently invalidates).
- Trusted-device opt-in to skip OTP for N days.
- SSO / Google sign-in.
- Password fallback. None — no passwords, ever.

### Reference implementation

`prototypes/pro-112/claim-flow.html` — screens 2 (Login, dual-state) and 2b (Verificar correo).

---

## Pay flow (locked 2026-04-25)

The native 4-step pay overlay opens from any unpaid invoice action button (table row, side panel, Inicio preview).

### Steps

| # | Step | What's on screen |
|---|---|---|
| 1 | **Revisar y elegir cuenta** | Invoice summary block (vendor / big amount / factura # / concepto / vence). Account-type toggle (`Empresa (RIF)` / `Persona (Cédula)`) at top. Single inline form — no bank dropdown; bank auto-detected from first 4 digits of account number. Pre-filled holder name + RIF/Cédula for known counterparty. Trust strip explaining BNC debit. Returning payers see saved-account radio cards + `+ Usar otra cuenta` instead. |
| 2 | **Código de tu banco (OTP)** | 6-digit OTP, auto-advance, Enter submits. Copy: *"Tu banco te envió un código de 6 dígitos al teléfono registrado en la cuenta."* Helpers: `Reenviar código` · `Cambiar cuenta`. |
| 3 | **Procesando** | Transient ~1.8s spinner. No buttons. |
| 4 | **Éxito** | Animated thin draw-in check (circle + check via stroke-dashoffset). Sub: *"Pagaste {monto} a {vendor}. Le notificamos del pago a tu proveedor y te enviamos el comprobante por correo."* Comprobante card with 6 rows: Referencia · Fecha · Método · Factura · Concepto · Monto. Buttons: `Descargar comprobante` (stub) / `Volver al portal`. |

### Locked decisions

| What | Decision |
|---|---|
| Account-type gating | Empresa (RIF) → **BNC only**. Persona (Cédula) → **any Venezuelan bank**. |
| Bank discovery | **Auto-detect** from first 4 digits of account number. 20-bank prefix table covers BNC, BdV, Mercantil, Provincial, Banesco, etc. **No dropdown.** |
| Identifiers | RIF / Cédula / phone all accept any user format; normalized internally (alphanumeric uppercase / digits-only). |
| Account number length | **Exactly 20 digits** (Venezuelan standard). |
| Phone number length | **Exactly 11 digits** (04XX XXX XXXX). |
| OTP | **Per-transaction, always.** No standing authorization in v1. Even saved accounts go through OTP. |
| Method label | `Débito Inmediato` (not `Débito ACH`). |
| Aprobar button color | **Always primary blue.** Never red, regardless of invoice state (e.g., `vencida`). |
| Trust strip copy | "Débito seguro vía BNC. Tu banco recibe la orden de débito — Tesote nunca almacena tu contraseña. Solo los últimos 4 dígitos de tu cuenta bancaria para reconocerla en próximos pagos." |
| Saved accounts | Stored in `PAYER_PROFILE.accounts` per (bank, last4, accountType). Idempotent. Surfaces as radio cards on subsequent pays. |
| Cancel behavior | Step 1 cancels immediately (nothing committed). Step 2 confirms first ("¿Cancelar el pago?"). Steps 3–4 close without confirm. |
| Visual system | **Mercury pastel pills** (filled bg, no border, dark text, 5px radius — lavender / amber / salmon / mint / gray). Pill + button uniform 96px width, padding 3px 8px, font 11px. Same as workspace shell. |

### Out of scope for v1 (deferred error paths)

- Wrong-OTP / bank-rejection / OTP-timeout error paths (caught + toasted in v1; full UX in v1.1).
- Refund flow.
- Standing authorization / "trusted account" opt-out of OTP.
- Real-time BNC status webhook integration on the payer side (we trust the synchronous response in v1; v1.1 reconciles via the sender's BNC feed).

### Reference implementation

`prototypes/pro-112/claim-flow.html` — overlay opens from `Pagar` row action / side-panel `Aprobar y pagar` / Inicio preview.

---

## Multi-invoice pay (locked 2026-04-29)

Promoted to v1 from v1.1 after the 2026-04-24 Rosa call: paying one invoice at a time at CAPCA scale (4–6 weekly invoices per supplier) is friction. The promotion is cross-client; not CAPCA-specific.

### UX

- **Checkbox column** at the leftmost position of the Pagos table. Header checkbox toggles select-all-visible. Selecting ≥1 row reveals a sticky bottom action bar.
- **Sticky bar**: left = `X facturas seleccionadas · Total Bs. {sum}`; right = `Pagar seleccionadas →` (primary blue). Disappears on deselect-all or after successful pay.
- **Per-row `Pagar` still works** for single-invoice case — no regression. Multi-pay does not block or replace it.
- Paid rows do not render a checkbox.

### Pay flow changes (4-step overlay)

- **Step 1.** Invoice summary block becomes a STACKED list of selected invoices (factura # / concepto / monto each), with grand total below in larger weight. Single-invoice mode unchanged.
- **Steps 2–3** unchanged.
- **Step 4 (éxito).** Comprobante card shows N rows of `Factura X — concepto — monto` with `Total pagado` footer. Sub copy unchanged: *"Pagaste {total} a {vendor}. Le notificamos del pago a tu proveedor y te enviamos el comprobante por correo."*

### Backend / state model

- **Single BNC debit** on the backend; surface as one `referencia` number (the batch ref) in the comprobante.
- **One Cobros row per invoice** on the workspace side — invoices are paid individually even when bundled in the pay flow. No new state added to the state machine; the batch is metadata, not a state transition.
- **Group identifier on the Event log** so the workspace can render `pago en lote (N facturas)` in the timeline.
- **No partial pay.** Selecting an invoice = paying the full amount. (See partial-pay note in Out-of-scope.)

### Reference implementation

`prototypes/pro-112/claim-flow.html` — checkboxes wired on the Pagos table; sticky bar implemented with `cp-multipay-bar` / `cp-multipay-cta`. Multi-mode hero card uses `cp-multi-list` inside the existing `cp-inv-summary`.

---

## Data model additions (2026-04-29)

These additions land in the engineering data model alongside the existing entities defined in [`cobros-spec.md`](cobros-spec.md) §3. Captured here because the counterparty portal surfaces them; the workspace-side spec is authoritative on storage details.

### `Counterparty`

| Field | Type | Notes |
|---|---|---|
| `payment_terms_days` | int, nullable | Days of credit granted by this counterparty for invoices issued under v1's display-only flavor. Nullable — not every counterparty has terms on file. |
| `payment_terms_label` | enum, nullable | One of: `contado` / `credito_30` / `credito_60` / `credito_90` / `custom`. The `custom` value pairs with a free-form day count surfaced in `payment_terms_days`. |

Source: ERP-pulled per counterparty in v1; manually editable in workspace Contraparte view (out of scope for the PRO-112 handoff — workspace-side change, separate ticket).

### `Cobro`

| Field | Type | Notes |
|---|---|---|
| `payment_batch_id` | uuid, nullable | Set on every Cobro that was paid as part of a multi-invoice batch. Same value on every Cobro in the batch. Null for single-pay. Drives the `pago en lote (N facturas)` rendering on Event-log timelines. Doesn't add states to the state machine — multi-pay still flows `aprobada → procesando → pagada` per row. |
| `payment_terms_snapshot` | string, nullable | Captures the term label at time of issue (e.g. `30 días`), immutable per invoice. Decouples invoice-level terms from later changes to the counterparty's standing terms. |

### State machine impact

None. Multi-invoice pay does not introduce new states. Each Cobro in a batch transitions `aprobada → procesando → pagada` independently; the batch is metadata only (`payment_batch_id` + Event-log group).

---

## Contraparte 360 — payer-side detail (locked 2026-04-29)

Counterparty rows in the Contrapartes screen open a **full-page detail** (not a side panel — full route, mirroring the workspace-side Contraparte 360). Read-only in v1.

### Layout (top to bottom)

1. **Header** — proveedor logo + name + RIF + "En red Tesote" check icon.
2. **Resumen card** — Total facturado YTD · Total pagado YTD · Deuda actual · Plazo otorgado · Plazo promedio de pago · Facturas activas.
3. **Pago / facturación timeline** — bar chart, last 12 months, two series (Facturado lavender / Pagado dark).
4. **Historial de facturas** — full table including paid; filterable by año + estado.
5. **Acciones — Estado de cuenta** — `Descargar PDF` + `Descargar Excel`. Both are stubs in the v1 prototype: toast `Generando estado de cuenta…` then `Estado de cuenta descargado`. Real PDF/Excel generation is engineering work.

### Estado de cuenta concept

Cumulative ledger: all invoices + payments + retenciones for that counterparty. Date-range selectable in production; v1 prototype is YTD only.

### Reference implementation

`prototypes/pro-112/claim-flow.html` — `data-cp-screen="contraparte-detail"`, opened via `[data-cp-nav="contraparte-detail"]` on each Contrapartes row.

---

## Client-specific extensions

Some counterparty-portal features are unlocked per-client based on what we can pull from their ERP / data partners. The canonical PRD scope above is cross-client; this section catalogs the per-client overlays.

- **CAPCA — Saldo disponible para compra.** Top-of-Pagos credit card showing límite SAP minus vencidas minus por vencer. Display-only; does not block any UI. Depends on SAP credit-limit data we have only for CAPCA in v1. See `prototypes/pro-112/claim-flow-capca-2.html` for reference. Other clients get this once their credit-limit feed is wired.

---

## BNC connect — sales-led for v1 (locked 2026-04-25)

The self-serve "Powered by Tesote" BNC OAuth wizard was scoped, drafted, and **scrapped pre-build** in favor of shipping the pay flow first. For v1, every BNC-related CTA in the portal routes to a **sales conversation** instead.

### CTA locations

All three fire the same toast (`Recibimos tu interés. Un asesor de ventas te contactará pronto.`):

1. **Topbar primary button** — `Habla con ventas` (phone icon).
2. **Inicio quick action** — `Habla con ventas` (phone icon), replaces the earlier `Conecta tu banco` quick action.
3. **Locked Tesote Connect teaser card** — `Habla con ventas →`.

### Why sales-led, not self-serve

- BNC OAuth needs production credentials we don't have yet (per `project_bnc_ach_status.md`).
- Most counterparties hitting v1 will be Tesote Negocios users with one inbound invoice; full BNC connect is overkill before activation is proven.
- A sales touchpoint at this CTA gives the team a real lead and keeps activation friction off the pay flow itself (which uses BNC under the hood via the workspace's connection, not the payer's).

### v1.1 plan

When the wizard ships, it replaces the toast (CTA wording stays as a sales pitch but routes to the OAuth flow). Existing saved accounts in `PAYER_PROFILE` migrate to a real BNC connection on activation — no data loss.

---

## Cobros — data model decisions (decided 2026-04-23)

The Cobros surface inside a workspace must unify two sources of truth:

1. **Invoices pulled from the ERP** (Odoo, SAP, etc.) — the system of record for most workspaces' receivables. Outstanding invoices flow into Tesote as rows labelled `Origen: ERP · Odoo` (or SAP).
2. **Ad-hoc payment links created directly in Tesote** — for workspaces without an ERP, or for off-ERP transactions. Rows labelled `Origen: Tesote · directo`.

**Out of scope (v1):** auto-creating a payment link for every new ERP invoice. For v1, the workspace user explicitly chooses which invoices to "cobrar por Tesote." This is a deliberate scope cut to avoid mass-sending unwanted payment links while the product is new.

### Counterparty email sourcing (locked 2026-04-23)

**Decision: ERP-pre-fill, Tesote-confirm.** When an invoice is imported from the ERP with a counterparty email, Tesote pre-fills the email but requires the workspace user to explicitly confirm (or edit) it before the first payment request is sent to that counterparty. Subsequent requests to the same counterparty trust the confirmed email.

**Why not pure ERP pull:** Counterparty emails in accounting systems rot — AP contacts leave, old placeholder addresses get set once and never fixed. The counterparty email is the identity key for Tesote Negocios; a wrong email = failed activation, wrong-party exposure, and a broken network effect.

**Why not pure prompt:** Adds friction on every counterparty; ERP data, when correct, is the fastest path.

**UX:** On first-send to a counterparty, surface a confirm step: *"Email detectado en Odoo: `compras@apb.com`. Confirmar o cambiar."* After confirmation, stored on the Tesote-side counterparty record with `source: erp_confirmed`. Subsequent sends are silent unless the email changes in the ERP.

**Edge cases:**
- ERP has no email → prompt is required
- ERP email doesn't match SENIAT-resolved RIF domain → soft warning on confirm
- Email is for a generic domain (gmail.com) → soft warning but allow

### Counterparty visual identifiers (deferred 2026-04-23)

**Avatars removed.** Squares-with-initials were noise at table density. When we have real brand logos (SENIAT lookup, logo-fetch service, or workspace upload), bring back a circular mark — never initials as the default.

**"En red Tesote" / "Sin activar" badge — kept, but iconified.** A small inline icon next to the company name, no text chip:
- **Blue filled check** → en red Tesote (confirmed counterparty with an active portal)
- **Grey question-mark circle** → no active portal yet (we don't know if they'll claim)
- Label surfaces on hover only (`title` attr). No body text, no pill.

The earlier decision to remove it was reversed 2026-04-23 — the distinction is high-signal enough at glance-time that it's worth 14px in every row. Keep the visual weight tiny so it doesn't compete with the name.

### Origen column (simplified 2026-04-23)

Renders as plain text — `Odoo`, `SAP`, `Directo`. No chips, no icons. The origin still drives logic under the hood (which sync happens, whether we can round-trip payment status back to the ERP) but the UI presentation is minimal.

### Two flows for creating a Cobro, one shared button (locked 2026-04-23)

A Cobro row enters the workspace in one of two ways, each with its own place to capture the counterparty email:

1. **ERP flow.** Invoice syncs from Odoo/SAP. Row appears in the Cobros table as `Borrador`. The workspace user clicks **`Enviar`**. If the counterparty email is not yet on file, clicking Enviar opens a small confirmation (side-panel or centered modal — TBD in design) asking the user to enter / confirm the recipient's email. Only after that is the link sent.
2. **Directo flow.** Invoice is created directly in Tesote (no ERP round-trip). The creation form itself requires the recipient email before the row can be saved — so by the time the row shows up in Cobros, the email is already on file.

**Implication for the UI.** The Cobros action column only needs two button states, not three:
- **`Enviar`** (paper-plane icon) — for any pre-send row (`Borrador`). Click either sends immediately (email on file) or opens the small email-capture step first (email missing). The state difference is handled in the click flow, not surfaced as a separate button.
- **`Recordar`** (bell icon) — for any already-sent row (`Enviada`, `Vista`, `Aprobada`, `Vencida`).
- Paid rows still show `Ver` (terminal state, no action to take).

This removes the earlier `Agregar email` button state from the table. The email-missing case is not a distinct row-level action; it's a lazy prompt inside the Enviar flow.

---

## What the designer needs to produce

Most of the v1 surface is drafted in `claim-flow.html`. Remaining design work, priority order:

1. **Invoice detail screen** — not yet drafted. Read-only for v1. Needs: sender block, line items, IVA, net due, PDF download, prominent `Pagar →` button (routes to the existing 4-step pay overlay).
2. **Profile / settings screen** — minimal. Email (read-only), phone (editable), sign out. No RIF management in v1. Currently absent from the prototype.
3. **Portal home polish** — Inicio is drafted; needs a finished pass on the locked-teaser cards once visual identity for each pillar (Connect, Automatizaciones, Capital, IA) is locked.
4. **Empty states** — first-login when only one invoice is present; post-pay when no outstanding invoices remain. Currently the prototype assumes 4 unpaid invoices.
5. **Pay-flow error states** — wrong OTP, bank rejection, OTP timeout, account auto-detect failure. Toasted in v1; design for v1.1.
6. **BNC connect wizard (v1.1)** — full Powered-by-Tesote OAuth flow. Out of v1.

---

## What needs decided before engineering scoping

1. Decisions 3, 4, 5 above (decision 1 resolved 2026-04-25; decision 2 resolved 2026-04-25).
2. Whether the portal shares a codebase/database with `app.tesote.com` or is a separate service.
3. Whether invoice data lives on the sending workspace's side or gets a dedicated "inbox" model for the counterparty.
4. SENIAT lookup SLA — if the landing page is supposed to pre-fill the company name, how fresh does that lookup need to be?
5. Webhook contract from workspace Cobros → counterparty portal (paid state echo, comprobante metadata). Cobros spec §3 references this; needs to be co-specced by both streams.

---

## Related

- [PRO-112 — Dan's super-app spec](pro-112-dan-super-app.md) — parent framing
- [user-stories.md](user-stories.md) — Luis's original Tesote Pay v1/v2 plan (payment-link-centric, different framing)
- [cobros-spec.md](cobros-spec.md) — workspace-side companion spec (paused 2026-04-23, see status note)
- [`claim-flow.html`](../prototypes/pro-112/claim-flow.html) — canonical counterparty prototype
- [`workspace-shell.html`](../prototypes/pro-112/workspace-shell.html) — workspace-side companion prototype
