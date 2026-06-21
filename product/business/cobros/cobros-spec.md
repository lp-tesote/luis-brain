---
title: Cobros — Product & Engineering Spec (v1)
tags: [product, tesote-pay, tesote-negocios, cobros, spec, engineering]
updated: 2026-04-23
author: Luis Pulgar
status: Draft for Dan review
audience: Engineering (Dan) + Product (Luis)
related:
  - ../prototypes/pro-112/workspace-shell.html
  - ../prototypes/pro-112/claim-flow.html
  - ../prototypes/pro-112/README.md
---

# Cobros — v1 Product & Engineering Spec

> **⚠️ Status note (2026-04-25).** This spec is **frozen at the 2026-04-23 review point**. The Cobros workstream paused after that handoff so the team could build out the **counterparty pay flow first** — see `../prototypes/pro-112/claim-flow.html` (the counterparty prototype is the spec for that side). Treat this doc as the canonical Cobros (workspace-side) reference, but expect a v1.1 pass once the counterparty side ships and we know what the workspace needs to expose to it (webhook contract, paid-state echo, comprobante metadata). Open questions in §9 still apply.
>
> **Purpose.** This document is the authoritative spec for the **Cobros** surface inside a Tesote workspace for v1 launch. It covers the complete set of states, flows, data contracts, copy, and acceptance criteria needed to build Cobros end-to-end with zero ambiguity. The payer-side experience (what the counterparty sees when they open a payment link) is fully expressed in the prototype `../prototypes/pro-112/claim-flow.html` — this doc treats it as a black box and focuses on the workspace-user side.
>
> **How to read.** §1–§3 frame scope, permissions, and data. §4 is the state machine (ground truth). §5 is the flow catalogue (one sub-section per flow, each with trigger, steps, state transitions, copy, and edge cases). §6 inventories everything that can go wrong. §7 is the authoritative copy deck. §8 is testable acceptance criteria. §9 is open decisions. §10 suggests the Linear ticket breakdown.

---

## 1. Scope

### In scope (v1)

| Capability | Detail |
|---|---|
| Cobros list | Unified view of outstanding outbound invoices (from ERP) + ad-hoc payment links (Directo). |
| Create — ERP flow | Invoices syncing in from **Odoo** arrive as `borrador`. User sends them selectively. |
| Create — Directo flow | Manual creation form for cobros without an invoice in the ERP. |
| Send flow | Includes email-capture modal when recipient email is missing. |
| Counterparty email sourcing | ERP pre-fill → Tesote confirm pattern (locked, see §5.3). |
| Cobro detail | Side-panel showing factura details, timeline, payment link, contact, actions. |
| Reminder | Manual reminder action per cobro. No auto-reminders in v1. |
| Cancel | Cancel any cobro not yet in `procesando` / `pagada`. |
| Payment tracking | Status timeline reflecting counterparty-side progress (via portal webhooks / polls). |
| ERP writeback | On payment success, write payment status back to Odoo invoice. |
| Basic filters & search | Filter by state, origin, date; search by client / factura number / amount. |
| Bulk actions | Select multiple, bulk-send (all with email on file), bulk-remind. |
| Permission model | Single role (workspace member). Every member can do every Cobros action. |

### Out of scope (deferred)

| Deferred to | Item | Why |
|---|---|---|
| v1.1 | Auto-reminders on cadence | Needs reminder engine + workspace preference settings; v1 manual is enough to launch. |
| v1.1 | Partial payments | Billing/reconciliation complexity; require exact-amount in v1. |
| v1.1 | Dispute resolution UI inside Tesote | v1 surfaces the dispute state; resolution happens via support. |
| v1.1 | Refund flow | Rare, off-ramp flow; v1 handles refunds manually via support. |
| v1.1 | ERP-pushed writebacks beyond "pagada" (journal entries, credit notes) | Writeback scope is limited to payment status in v1. |
| v1.1 | Link-creation-from-ERP auto-mode | v1 requires explicit user click to send; no blast-send on ERP sync. |
| v2 | SAP integration | CAPCA runs SAP S/4HANA Cloud but a proper SAP connector is a separate engineering stream. Prototype shows SAP rows for realism; code path treats only Odoo. |
| v2 | Multi-currency (USD, USDT) | v1 is VES-only. |
| v2 | Multi-role workspace permissions (AP clerk / CFO / auditor) | Dan's PRO-112 G.2. Deferred for v1. |
| v2 | Team approval workflows (multi-approver) | Dan's PRO-112 G.3. |
| v2 | API access | Dan's PRO-112 G.10. |
| v2 | Customer-facing invoice PDF generation | v1 reuses ERP's PDF link; Directo cobros have no PDF. |

### Explicit non-goals

- We do **not** auto-create a payment link for every new ERP invoice. User must explicitly click Enviar. This is a deliberate scope choice to avoid surprise-sending links to unconfirmed email addresses during launch.
- We do **not** build a workspace accounts-payable side (Pagos). That's a separate surface covered in its own spec.
- We do **not** try to match payments to invoices automatically if they arrive outside the Tesote payment link. That's Tesote Connect's job (bank sync side) and will link to Cobros in v1.1.

---

## 2. Personas & Permissions

### Workspace users (v1 single role)

| Persona | Typical title | Uses Cobros to… |
|---|---|---|
| Workspace member | Admin, founder, treasury lead, CFO | Do everything — create, send, remind, cancel, view status, export. |

No role-gating in v1. All workspace members can perform all Cobros actions. Multi-role comes in v2.

### System actors (non-human)

| Actor | Role |
|---|---|
| ERP sync worker | Pulls invoices from Odoo at configured cadence. Creates/updates `borrador` cobros. |
| Notification worker | Sends transactional emails (initial send + reminders). |
| Payment-link webhook receiver | Listens to counterparty-portal side events and advances Cobro state. |
| BNC reconciler | On bank transaction match, advances `procesando → pagada`. |
| TTL cron | Moves `enviada → vencida` on due date; moves live links → `link_expirado` at 30-day TTL. |

### Counterparty (payer-side)

Treated as a black-box for this spec. The payer-side design is fully expressed in `../prototypes/pro-112/claim-flow.html` (the prototype is the spec for that side). The only surface where Cobros interacts is via state-transition webhooks.

---

## 3. Data model

### 3.1 Entities

#### `Cobro`

The atomic invoice/payment-request record inside a workspace.

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | PK |
| `workspace_id` | uuid FK | Workspace that owns this cobro. |
| `counterparty_id` | uuid FK | The contraparte being charged. |
| `receiving_account_id` | uuid FK | Which BNC account funds land in. |
| `amount_ves` | numeric(18,2) | VES only in v1. Positive. |
| `currency` | enum | `VES` only in v1. Stored explicitly for v2 migration cleanliness. |
| `concept` | text | User-visible description (e.g., "Servicios abril 2026"). |
| `invoice_number` | string(40) | ERP invoice number (F-2026-0042) or internally-generated for Directo (L-2026-NNNN). |
| `origin` | enum | `odoo` \| `directo`. (`sap` reserved for v2.) |
| `origin_ref_id` | string(80), null | ERP's internal invoice ID. Null for Directo. |
| `origin_ref_url` | string, null | Deep-link back to ERP (e.g., Odoo invoice URL). Null for Directo. |
| `state` | enum | See §4. Default `borrador`. |
| `issued_at` | timestamp | ERP issue date, or creation date for Directo. |
| `due_at` | timestamp | ERP due date, or form-entered for Directo. |
| `sent_at` | timestamp, null | When we first dispatched the email. |
| `seen_at` | timestamp, null | When counterparty first opened `/pay/:token`. |
| `approved_at` | timestamp, null | When counterparty approved (Layer 1). |
| `paid_at` | timestamp, null | When BNC confirmed. |
| `cancelled_at` | timestamp, null | |
| `cancellation_reason` | text, null | |
| `payment_link_token` | string(32), null | Set on first `enviar`. Unique. URL-safe. |
| `payment_link_url` | string, null | Derived / cached. |
| `link_expires_at` | timestamp, null | Set to `sent_at + 30 days`. Refreshed on resend. |
| `created_at` / `updated_at` | timestamp | |

Indexes: `(workspace_id, state)`, `(payment_link_token)` unique, `(counterparty_id)`, `(origin, origin_ref_id)` unique.

#### `Counterparty`

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | PK |
| `workspace_id` | uuid FK | Each workspace has its own counterparty records. Tesote-network resolution (cross-workspace `CounterpartyIdentity`) happens downstream — out of scope for this v1 spec. |
| `legal_name` | string | Display name. |
| `rif` | string(20) | SENIAT RIF. Unique per workspace. |
| `primary_email_id` | uuid FK, null | Points to `EmailRecord`. May be null if no email confirmed yet. |
| `phone` | string, null | |
| `origin` | enum | `odoo` \| `directo` \| `manual`. Where the record first came from. |
| `origin_ref_id` | string, null | ERP's internal customer ID. |
| `tesote_network_status` | enum | `active` (has claimed portal) \| `inactive` (no portal yet). Mirrored from cross-workspace `CounterpartyIdentity`. |
| `notes` | text, null | User-editable workspace-local note. |
| `created_at` / `updated_at` | timestamp | |

Indexes: `(workspace_id, rif)` unique, `(workspace_id, legal_name)`, `(origin, origin_ref_id)`.

#### `EmailRecord`

Counterparties can accumulate multiple email addresses over time. `primary_email_id` points to the one currently used.

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | |
| `counterparty_id` | uuid FK | |
| `email` | string | |
| `source` | enum | `erp_imported` \| `erp_confirmed` \| `user_entered`. |
| `confirmed_at` | timestamp, null | When the workspace user confirmed this email via Tesote. |
| `confirmed_by_user_id` | uuid FK, null | Who confirmed. |
| `last_used_at` | timestamp, null | Last time we dispatched an email to this address. |
| `created_at` | timestamp | |

Note: we store `erp_imported` state to distinguish "came from Odoo but nobody confirmed" from `erp_confirmed` (came from Odoo and a workspace user explicitly confirmed). Only `erp_confirmed` or `user_entered` emails are eligible for silent send. `erp_imported` triggers the email-capture modal on first Enviar.

#### `PaymentLink` (conceptual — may live on `Cobro`)

In v1 we embed `payment_link_token` on the Cobro row. If link rotation / multiple links per cobro is ever needed, split into a separate table. For v1, one link per cobro, stored in-place.

#### `Reminder`

| Field | Type |
|---|---|
| `id` | uuid |
| `cobro_id` | uuid FK |
| `sent_at` | timestamp |
| `sent_by_user_id` | uuid FK |
| `channel` | enum `email` |
| `delivered_at` | timestamp, null |

Append-only audit.

#### `Event`

Append-only audit log for every Cobro state transition. Used to build the side-panel timeline.

| Field | Type |
|---|---|
| `id` | uuid |
| `cobro_id` | uuid FK |
| `event_type` | enum | See §4.2. |
| `occurred_at` | timestamp |
| `actor_type` | enum `user` \| `counterparty` \| `system` \| `erp` \| `bnc` |
| `actor_id` | string, null | User id if `actor_type=user`, else null. |
| `payload` | jsonb | Event-specific context. |

### 3.2 Derived / read-only views

- **Cobros list view** — `workspace_id` + filters, returns paginated `Cobro` rows joined with `Counterparty` and latest `Event`.
- **Contraparte 360** — all Cobros + Pagos for a given `Counterparty`.

---

## 4. State machine

### 4.1 States

| State | Meaning | Can the workspace still act? |
|---|---|---|
| `borrador` | Created locally. Not yet dispatched. | Edit, send, cancel, delete. |
| `enviada` | Email dispatched. Not opened. | Resend, remind, cancel. |
| `vista` | Counterparty opened the link. | Resend, remind, cancel. |
| `aprobada` | Counterparty tapped Aprobar (Layer 1). Waiting for bank auth. | Cancel (heavy — undoes a pending payment commit). |
| `procesando` | Tesote submitted debit to BNC. Awaiting confirmation. | No actions. In-flight. |
| `pagada` | BNC confirmed. | View-only. (v1.1: refund.) |
| `fallida` | BNC rejected, or OTP timed out. | Retry (re-enters `enviada` for resend), cancel. |
| `vencida` | Due date passed without payment. Link may still be live. | Remind, cancel, resend. |
| `link_expirado` | Link TTL hit 30 days. Counterparty cannot pay through this link anymore. | Resend (mints a new link / token), cancel. |
| `cancelada` | Workspace cancelled. Terminal. | None. |
| `disputada` | Counterparty disputed post-payment. | View-only. (v1.1: resolve.) |

> `esperando_otp` is **not** a workspace-visible state in v1. It exists on the counterparty side (payer portal). From the workspace's perspective, anything between `aprobada` and `procesando` is still `aprobada`.

### 4.2 Event types (emit on every transition)

```
cobro.created_from_erp
cobro.created_directo
cobro.edited
cobro.email_confirmed
cobro.sent
cobro.resent
cobro.opened_by_counterparty
cobro.approved_by_counterparty
cobro.submitted_to_bnc
cobro.paid
cobro.failed
cobro.expired_due
cobro.expired_link
cobro.cancelled
cobro.disputed
cobro.erp_writeback_ok
cobro.erp_writeback_failed
cobro.reminder_sent
```

### 4.3 Transitions

```
borrador ──Enviar──> enviada
borrador ──Cancelar──> cancelada
borrador ──(delete)──> (removed; hard delete allowed in borrador only)

enviada ──(counterparty opens)──> vista
enviada ──(due passes)──> vencida
enviada ──(30 days pass)──> link_expirado
enviada ──Cancelar──> cancelada
enviada ──Reenviar──> enviada   (logs a Reminder; state unchanged)

vista  ──(counterparty approves)──> aprobada
vista  ──(same ext exits as enviada)

aprobada ──(BNC ACK submit)──> procesando
aprobada ──Cancelar──> cancelada   (confirmation required — "se cancelará un pago ya aprobado")

procesando ──(BNC ok)──> pagada
procesando ──(BNC rejected / OTP expired)──> fallida

fallida ──Reenviar / Reintentar──> enviada
fallida ──Cancelar──> cancelada

vencida ──(counterparty approves late)──> aprobada
vencida ──Cancelar──> cancelada
vencida ──(30 days post-send)──> link_expirado

link_expirado ──Reenviar (new token)──> enviada
link_expirado ──Cancelar──> cancelada

pagada ──(v1.1: refund)──> reembolsada
pagada ──(counterparty dispute)──> disputada
```

All transitions emit an `Event`. All `Cancelar` actions require confirmation modal with a text reason.

---

## 5. Flows

Each flow is described as: **trigger**, **actors**, **steps with state transitions**, **user-facing copy**, **edge cases specific to this flow**.

### 5.1 Create from ERP (Odoo)

**Trigger.** Odoo ERP sync job detects an invoice eligible for import (see §5.1.1).

**Actors.** ERP sync worker.

**Steps.**
1. Sync job reads invoice from Odoo.
2. Resolve Counterparty:
   - If Odoo customer ID exists in `counterparties.origin_ref_id` → use that.
   - Else if RIF matches existing Counterparty → merge & update.
   - Else create new Counterparty with `origin=odoo`, `tesote_network_status` resolved via cross-workspace lookup.
3. Resolve counterparty email:
   - If Odoo has an email on the customer record → create `EmailRecord` with `source=erp_imported` if new, leave existing `erp_confirmed` untouched.
   - If no email in Odoo → do not create an EmailRecord.
4. Create `Cobro` with `state=borrador`, `origin=odoo`, all invoice fields.
5. Emit `cobro.created_from_erp`.

#### 5.1.1 Eligibility filter (what syncs in)

Only these Odoo invoices sync as Cobros:
- Status: confirmed & open (not draft, not paid, not cancelled in Odoo).
- Residual amount > 0 (still owed).
- Customer has a RIF (we skip "internal" invoices without a proper RIF).
- Not on workspace's ERP-exclusion list (settings, v1.1).

#### 5.1.2 Sync cadence

- Default: every 15 minutes.
- On-demand: user can click "Sincronizar ahora" in Cobros header.
- Webhooks if Odoo supports them (Odoo Enterprise does via `base_automation`).

**Copy.**
- Toast on manual sync complete: `"Sincronización con Odoo completa · 4 facturas nuevas · 1 actualizada"`

**Edge cases.**
- Invoice is deleted in Odoo after syncing → mark Cobro as `cancelada` with reason `"Eliminada en Odoo"` if still in `borrador` / `enviada`. If already `procesando` or later, keep the record and surface a warning.
- Odoo invoice amount changes after syncing → if Cobro is `borrador`, update amount silently. If already `enviada` or later, mark as needing re-send (see §5.7) and show a warning pill.
- Odoo customer email changes → new `EmailRecord` with `source=erp_imported`. Primary email on the Counterparty does NOT auto-flip. User must explicitly confirm the new one.
- Duplicate invoice number within same workspace+origin → reject & alert user (sync log error).

### 5.2 Create Directo

**Trigger.** User clicks `+ Nuevo cobro` button in Cobros header.

**Actors.** Workspace member.

**Steps.**
1. Opens full-screen creation form (slide-in from right or full-page takeover — design TBD).
2. Form fields:
   - Contraparte (search + create-new). Required.
   - Email (pre-filled from counterparty's primary if exists, editable). **Required before save.**
   - Amount in VES. Required.
   - Concept. Required.
   - Due date. Required.
   - Receiving BNC account. Required. Defaults to workspace's primary.
3. Validates:
   - Amount > 0.
   - Due date ≥ today.
   - Valid email format.
4. On save:
   - If Counterparty doesn't exist → create with `origin=directo`.
   - Create or confirm `EmailRecord` with `source=user_entered`, `confirmed_at=now`.
   - Create `Cobro` with `origin=directo`, `invoice_number = L-YYYY-NNNNN` (workspace-scoped sequence), `state=borrador`.
   - Emit `cobro.created_directo`.
5. Redirect to Cobros list, newly-created row highlighted.
6. Directo flow is **ready to send immediately** — unlike ERP, the email is always already confirmed by the save step.

**Copy.**
- Form title: `"Nuevo cobro"`
- Submit button: `"Guardar borrador"` (secondary) · `"Guardar y enviar"` (primary, sends immediately)

**Edge cases.**
- User enters an existing counterparty name but different RIF → warning modal: "Ya existe una contraparte con este nombre. ¿Crear nueva o usar la existente?"
- User leaves the form without saving → confirm discard modal.
- Counterparty already exists in Tesote network → surface `tesote_network_status=active` inline for transparency.

### 5.3 Send

**Trigger.** User clicks `Enviar` on a `borrador` Cobro.

Two sub-paths depending on counterparty email state ("ERP pre-fill, Tesote confirm" pattern — when an invoice is imported from the ERP with a counterparty email, Tesote pre-fills it but requires the workspace user to explicitly confirm or edit before the first send to that counterparty):

#### 5.3.A Email on file (no modal)

Condition: Counterparty's `primary_email_id` points to an `EmailRecord` with `source ∈ {erp_confirmed, user_entered}`.

Steps:
1. Click Enviar.
2. Small inline confirmation: `"Enviando a finanzas@apb.com"` + undo toast for 5s.
3. Generate `payment_link_token`, set `sent_at=now`, `link_expires_at=now+30d`, transition `borrador → enviada`.
4. Notification worker sends email.
5. Row updates: state pill → `Enviada`, action → `Recordar`.

#### 5.3.B Email missing or unconfirmed (email-capture modal)

Condition: no EmailRecord exists, OR `primary_email_id` points to `erp_imported` source (never confirmed).

Steps:
1. Click Enviar.
2. Centered modal opens. Shows cobro summary + email input.
3. If an `erp_imported` email exists, pre-fill the input with it and helper text: `"Detectado en Odoo — confirma o cambia."`. If no email at all, leave input empty.
4. User enters / confirms email, clicks primary `Enviar`.
5. System creates/updates `EmailRecord` with `source=user_entered` (or promotes `erp_imported → erp_confirmed` if the value is unchanged) and `confirmed_at=now`. Sets it as `primary_email_id`.
6. Proceeds as in 5.3.A (generate token, send, state update).

**Copy (modal).**
- Title: `"Enviar factura a {Counterparty.legal_name}"`
- Sub (no email): `"Esta contraparte no tiene un correo registrado. Agrégalo para enviarle el enlace de pago."`
- Sub (erp_imported): `"Detectamos este correo en Odoo. Confírmalo antes de enviar."`
- Input label: `"Correo del destinatario"`
- Helper: `"Le enviaremos el enlace de pago a este correo. Quedará guardado en la contraparte para futuros cobros."`
- Cancel: `"Cancelar"`
- Primary: `"Enviar"`

**Edge cases.**
- Email format invalid → disable send button, no error shown until blur.
- User enters an email that matches another existing EmailRecord on the same counterparty → promote that existing one to primary, don't create duplicate.
- Network error on send → keep modal open, show inline error `"No pudimos enviar el correo. Inténtalo de nuevo."` Leave cobro in `borrador`.

### 5.4 Counterparty pays (happy path)

This flow lives in the counterparty portal. Summarized here for Cobros-side state-transition clarity.

| Step | Counterparty side | Cobro state in workspace |
|---|---|---|
| Email received → clicks link | Lands on `/pay/:token` | no change yet |
| Opens link | Verifies email, sees details | `enviada → vista`, `seen_at` set, event `cobro.opened_by_counterparty` |
| Taps "Aprobar" | Layer 1 approval | `vista → aprobada`, `approved_at` set |
| Completes bank auth (OTP or standing) | — | `aprobada → procesando` on BNC submit |
| BNC confirms | Done | `procesando → pagada`, `paid_at` set; `cobro.paid` event fires; ERP writeback job schedules |

**No user action needed** on the workspace side during this flow. Row auto-updates via real-time events (WebSocket or polling; TBD with Dan).

### 5.5 Reminder

**Trigger.** User clicks `Recordar` on a row in state `enviada`, `vista`, `aprobada`, `fallida`, `vencida`.

**Actors.** Workspace member.

**Steps.**
1. Click Recordar.
2. Small inline confirmation: `"Recordatorio enviado a {email}"`.
3. Create `Reminder` record, emit `cobro.reminder_sent`. State is unchanged.
4. Notification worker sends the reminder email (same link; no new token).

**Rules.**
- Min 1 hour between consecutive reminders to the same cobro (rate limit). If violated → toast `"Ya enviaste un recordatorio hace poco. Inténtalo más tarde."`
- Max 10 reminders per cobro lifetime (safety rail).

### 5.6 Cancel

**Trigger.** User clicks `Cancelar` (available in side-panel footer for any state except `procesando`, `pagada`, `cancelada`, `disputada`).

**Steps.**
1. Confirmation modal.
2. Copy varies by state:
   - From `borrador`: `"¿Descartar este borrador? Se eliminará permanentemente."`
   - From `enviada` / `vista`: `"¿Cancelar este cobro? El enlace dejará de funcionar y la contraparte verá un mensaje."`
   - From `aprobada`: `"Esta contraparte ya aprobó el pago. Si cancelas, se cancelará también el pago pendiente en su banco. ¿Continuar?"`
3. Optional reason text field (not required).
4. On confirm:
   - `state → cancelada`.
   - Invalidate the payment link token (subsequent visits see a "Cobro cancelado" page).
   - Emit `cobro.cancelled` with reason.
   - Notify counterparty by email IF state was beyond `enviada`: `"El cobro F-XXXX fue cancelado por {Workspace}. No se requiere ninguna acción."`

**Edge cases.**
- From `borrador`, no counterparty-side state to clean → hard delete allowed (admin setting). For normal users, soft-delete via `cancelada`.
- From `aprobada` with BNC call already in flight → fail the cancel with error `"No se puede cancelar: el pago ya está en proceso."`. Show loading spinner during that check.

### 5.7 Edit

**Trigger.** User opens side panel → clicks edit icon (or fields editable inline in panel, TBD).

**Pre-send edits (`borrador`):** all fields editable. Saves as a new version of the cobro.

**Post-send edits (`enviada` / `vista`):**
- Only allowed on: concept, due date, email.
- Amount NOT editable post-send — if amount is wrong, cancel and re-create.
- On save: emit `cobro.edited`, and:
  - If email changed → re-dispatch the email to new address; old link token stays valid.
  - If due date changed → update on the counterparty portal's display.
- Do NOT notify the counterparty of the edit (silent change).

**Post-approve / paid:** no edits allowed.

### 5.8 Refund (deferred to v1.1)

Not in v1. Refunds handled via support process. Surface the cobro's `pagada` state with a footer CTA `"Solicitar reembolso (contacta soporte)"`.

### 5.9 Dispute

**Trigger.** Counterparty taps "Disputar" on their side (rare; the counterparty-side flow is stubbed in v1 — see `claim-flow.html`).

**Steps (workspace side).**
1. Incoming webhook from portal.
2. Cobro `state → disputada` (only possible from `pagada`).
3. Side panel shows prominent red banner with dispute reason text from counterparty.
4. Notification to workspace: email + in-app.
5. Workspace can only view. No resolution UI in v1 — direct to support.

**Copy (banner).**
- `"La contraparte disputó este pago el {date}. Razón: {dispute_reason}. Ponte en contacto con soporte."`

### 5.10 Payment failed

**Trigger.** BNC webhook: debit failed OR OTP expired on counterparty side OR retry exhausted.

**Steps.**
1. Cobro `state → fallida`.
2. Store failure reason (`payload` of the event).
3. Show in the side panel with a red banner + reason text.
4. Workspace can: `Reenviar` (which takes it back to `enviada` with a new attempt), `Cancelar`.

**Known failure reasons (from BNC):**
- `insufficient_funds` → copy: `"La cuenta no tenía fondos suficientes."`
- `account_not_authorized` → copy: `"La cuenta no autorizó el débito. Pídele que reintente con otra cuenta o con OTP."`
- `otp_timeout` → copy: `"La contraparte no ingresó el código OTP a tiempo."`
- `bank_unreachable` → copy: `"El banco no respondió. Inténtalo de nuevo en unos minutos."`
- Unknown → copy: `"El pago falló. Contacta soporte si el problema persiste."`

### 5.11 Link expired

**Trigger.** Cron job runs daily. For any cobro with `state ∈ {enviada, vista, fallida, vencida}` and `link_expires_at < now`, transition `→ link_expirado`.

**Steps.**
1. State change.
2. Invalidate the token (counterparty sees "Enlace expirado" page).
3. Send notification to workspace: `"El enlace de {Counterparty} ({invoice_number}) expiró. Reenvíaselo para darle un nuevo plazo."`
4. User can `Reenviar` — generates fresh token, fresh `link_expires_at`.

### 5.12 Resend (explicit, not just reminder)

Distinct from "Recordar" — this mints a new token because the old one expired/failed.

**Trigger.** User clicks `Reenviar` from states: `fallida`, `link_expirado`, or on-demand from `enviada` (to refresh).

**Steps.**
1. Mint new `payment_link_token`, update `link_expires_at`.
2. `state → enviada`, `sent_at = now`.
3. Send email as in 5.3.A.
4. Emit `cobro.resent`.

---

## 6. Error & edge cases (cross-cutting)

### 6.1 ERP integration errors

| Scenario | Handling |
|---|---|
| Odoo auth token expired | Sync pauses. Banner in Cobros: `"La conexión con Odoo expiró. Vuelve a conectar."` with CTA to settings. |
| Odoo unreachable | Silent retry 3× with backoff. On 3rd fail, banner. Previous data still visible. |
| Schema mismatch (Odoo version change) | Sync errors logged, banner: `"Error sincronizando. El equipo de Tesote fue notificado."` + alert to Tesote ops. |
| Invoice import creates duplicate | Block on `(origin, origin_ref_id)` unique constraint. Log error. |
| Very large sync (10k+ invoices first time) | Paginate. Show progress: `"Importando facturas… 2.400 de 8.137"`. |

### 6.2 Email delivery errors

| Scenario | Handling |
|---|---|
| Bounce | EmailRecord flagged `bounced=true`. Cobro state unchanged. Show in side panel: `"El correo rebotó. Verifica la dirección."` |
| Spam / delayed | No signal; treat as delivered optimistically. |
| Same email for many counterparties | Allowed. No uniqueness constraint across counterparties. |

### 6.3 Data integrity

| Scenario | Handling |
|---|---|
| RIF collision (two counterparties, same RIF, same workspace) | Unique constraint blocks. Force merge flow. |
| Counterparty deleted while cobros reference them | Cascade via state `cancelada` for all open cobros; `pagada` cobros keep the counterparty ID pinned (no cascade). |
| Amount mismatch during reconciliation (BNC says X, we expected Y) | v1: flag for manual review, keep `procesando`. v1.1: auto-resolve if within 0.5% tolerance. |

### 6.4 Concurrency

- Two workspace members click Enviar on the same `borrador` simultaneously → first wins, second gets error `"Este cobro ya fue enviado por {user}."`.
- Race between workspace cancelling and counterparty approving → last write wins at state machine level; if cancel lands after `aprobada` we follow 5.6 aprobada-path (reverses the bank call if possible).

### 6.5 Timezone

All timestamps stored UTC. Display in workspace's configured timezone (default Venezuela, UTC-4). "Vence 8 may" means end-of-day in workspace timezone.

### 6.6 Permissions & multi-tenant

- Every query is scoped by `workspace_id`. Enforced at ORM level with a required scope parameter (not trusting the UI).
- No cross-workspace data exposure in Cobros API.

---

## 7. Copy deck (Spanish, authoritative)

All user-facing strings. **Source of truth** — Dan should not improvise copy during build.

### 7.1 Cobros list header

- Page title: `Cobros`
- Subtitle: `Facturas que enviaste a tus clientes. Cobra, reenvía o cancela desde aquí.`
- Primary CTA: `Nuevo cobro`
- Export: `Exportar`
- Sync now: `Sincronizar ahora`

### 7.2 Summary cards

- `Total por cobrar`
- `Vencido`
- `Próximo vencimiento`
- `Cobrado este mes`

### 7.3 State pills

- `Borrador` · grey
- `Enviada` · blue
- `Vista` · blue (same visual; sub-label "abierto hace Xh")
- `Aprobada` · yellow
- `Procesando` · yellow (spinner)
- `Pagada` · green
- `Fallida` · red
- `Vencida` · red
- `Enlace expirado` · grey
- `Cancelada` · grey (muted)
- `Disputada` · red

### 7.4 Action buttons (row)

- `Enviar` · primary blue, paper-plane icon
- `Recordar` · ghost, bell icon
- `Ver` · ghost, no icon (paid/cancelled terminal states)

### 7.5 Tabs

- `Todas` · `Borradores` · `Enviadas` · `Aprobadas` · `Pagadas` · `Vencidas`

### 7.6 Network banner (workspaces with mixed clients)

- `{N} de tus clientes ya están en Tesote. Les cobras en 1 clic — cuando ellos aprueban, el dinero llega al instante. {M} aún no se han activado: envíales un recordatorio para que reclamen su portal.`
- CTA: `Invitar a los {M}`

### 7.7 Side panel

- Section labels: `DETALLES DEL COBRO` · `CONTACTO` · `ENLACE DE PAGO` · `HISTORIAL`
- Footer: `Reenviar notificación` · `Descargar PDF` · `Cancelar cobro`

### 7.8 Empty states

- No cobros yet (new workspace): `"Aún no has enviado ningún cobro. Sincroniza tu ERP o crea tu primer cobro manualmente."` + `Conectar Odoo` secondary / `Nuevo cobro` primary.
- No results on filter: `"No hay cobros que coincidan con este filtro."`

### 7.9 Toasts

- Sync complete: `"Sincronización con Odoo completa — {N} facturas nuevas."`
- Email sent: `"Enviado a {email}."`
- Reminder sent: `"Recordatorio enviado a {email}."`
- Cancelled: `"Cobro cancelado."`
- Link refreshed: `"Nuevo enlace generado y enviado."`
- Generic error: `"Algo salió mal. Inténtalo de nuevo."`

### 7.10 Emails (to counterparty)

See `prototypes/pro-112/claim-flow.html` for the initial send email. Reminder email is a simpler variant with a `"Recordatorio: tienes una factura pendiente"` subject. Full email templates → separate doc once design is signed off.

---

## 8. Acceptance criteria

Each flow has testable outcomes. Dan can turn these into integration tests / Cypress specs.

### 8.1 Create from ERP

- [ ] Connecting Odoo for the first time imports all eligible invoices as `borrador` within 5 minutes.
- [ ] Re-syncing does not create duplicates.
- [ ] Invoice closed in Odoo between syncs → Cobro marked `cancelada`.
- [ ] Invoice amount changed in Odoo → if `borrador`, silently updated; if post-send, warning surfaced.

### 8.2 Create Directo

- [ ] Required fields (contraparte, email, amount, concept, due date, receiving account) enforced client-side and server-side.
- [ ] Duplicate invoice number within same (origin, workspace) rejected.
- [ ] Creating a new counterparty from the form creates the counterparty record with correct defaults.
- [ ] `Guardar y enviar` transitions to `enviada` immediately.

### 8.3 Send

- [ ] Email on file (source ∈ confirmed / user_entered) → no modal, silent send with confirm toast.
- [ ] Email missing / imported-only → modal opens, pre-fills if `erp_imported`, requires valid email.
- [ ] Modal "Enviar" disabled until email passes validation.
- [ ] On successful send, row state changes, audit event recorded.
- [ ] Pressing Enter in email input submits if valid.

### 8.4 Reminder

- [ ] Rate limit enforced (1 per hour per cobro).
- [ ] Count of reminders visible in side-panel timeline.
- [ ] Reminder email uses the same link token as original.

### 8.5 Cancel

- [ ] Confirmation modal before cancel.
- [ ] From `borrador` → state becomes `cancelada` (no notification).
- [ ] From `enviada+` → counterparty notified by email.
- [ ] From `aprobada` → preflight check blocks cancel if bank call already in flight.
- [ ] Link invalidated post-cancel (counterparty sees "Cobro cancelado" page).

### 8.6 Link expired

- [ ] Cron runs daily; cobros exceeding 30d since last send transition to `link_expirado`.
- [ ] `Reenviar` from `link_expirado` mints a new token and returns to `enviada`.

### 8.7 Payment success

- [ ] Webhook from portal transitions state correctly without workspace intervention.
- [ ] ERP writeback fires within 1 minute of `pagada`.
- [ ] Failed writeback retries 3× with backoff; then flags for manual review.

### 8.8 Payment failure

- [ ] State transitions to `fallida` with human-readable reason.
- [ ] `Reenviar` from `fallida` resets state to `enviada` with a fresh attempt.

### 8.9 Permissions

- [ ] No workspace can read/write another workspace's Cobros (automated cross-tenant test).

### 8.10 Performance targets

- [ ] Cobros list with up to 1,000 rows renders in < 1.5s on a warm cache.
- [ ] Side panel opens in < 200ms.
- [ ] Send action completes (including email dispatch enqueue) in < 1s from click.

---

## 9. Open decisions (need product input)

| # | Question | Context | Recommendation |
|---|---|---|---|
| 1 | Soft vs hard delete from `borrador`. | Accidental delete recovery. | Soft-delete (30-day trash) even from borrador. |
| 2 | Link TTL — 30 days or configurable? | 30d may be too short for some AP cycles. | 30d default, configurable per-workspace in v1.1. |
| 3 | Reminder rate limit — 1/hour strict, or exponential backoff? | User may want to hammer for vencidas. | 1/hour first, then 1/day after 3rd reminder. |
| 4 | Multi-email per counterparty — store all, use one. Or just primary + history? | Real counterparties have multiple inboxes (AP + treasury). | Store all in `EmailRecord`, promote one to primary, allow resend-to-all as v1.1. |
| 5 | Bulk send — show "requires email" warning? | If 40 cobros selected and 8 are missing emails, do we send 32 + surface the 8, or block? | Send the 32, surface a modal listing the 8 at the end. |
| 6 | `procesando` visible in list or hidden in sub-state of `aprobada`? | Showing procesando makes a racy UI; hiding simplifies. | Show as distinct state for transparency; small spinner adornment. |
| 7 | Counterparty-side cancellation reason visible to workspace? | Privacy vs transparency. | Show only if user chose to share; blank otherwise. |
| 8 | ERP writeback — just "paid" flag, or journal entries? | Accountants love journal entries. | v1 flag only. v1.1 optional entries per workspace setting. |
| 9 | Workspace can self-serve disable Odoo sync? | Debug / holiday mode. | Yes, toggle in ERP Integrations settings. |
| 10 | Audit log retention? | Compliance + cost. | Forever for `pagada`; 2 years for non-terminal states. |

---

## 10. Suggested Linear ticket breakdown

Rough engineering stream. Sequencing matters — ticket 1 blocks 2, 2 blocks 3, etc.

1. **Data model & migrations** — create `cobros`, `counterparties`, `email_records`, `reminders`, `events` tables with constraints.
2. **Cobros CRUD + state machine** — internal API for create / read / state transitions. No UI yet.
3. **Odoo sync worker** — stand up the sync worker, respect eligibility filters, idempotent on repeat syncs. Integration-test against a staging Odoo.
4. **Cobros list UI** — render the table, filters, tabs, summary cards. Read-only.
5. **Create Directo flow** — form + submit path.
6. **Send flow** — email-on-file silent + modal flow for missing email; notification dispatch.
7. **Side panel** — detail view + timeline from `events`.
8. **Reminder + resend** — rate-limited + audit trail.
9. **Cancel + edit** — with permission checks and copy variants per state.
10. **Payment webhook handlers** — portal → cobros state transitions.
11. **ERP writeback worker** — on `pagada`, push status to Odoo with retry.
12. **Link expiry cron** — daily job, new-token on resend.
13. **Failure handling** — `fallida` path + reason display + retry.
14. **Bulk actions** — multi-select, bulk-send, bulk-remind.
15. **Empty + loading + error states** — polish pass.
16. **Permissions & cross-tenant tests** — hard safety rails.
17. **Perf + scale** — pagination, indexes, tune list query.

Parallelizable after ticket 4:
- Portal-side work (separate spec).
- Copy + design QA.

---

## Appendix A — Glossary

| Term | Meaning |
|---|---|
| **Cobro** | A single outbound invoice / payment request owned by a workspace. |
| **Origen** | Where the Cobro record was born — Odoo (ERP) or Directo (Tesote form). |
| **Borrador** | Cobro created but not yet sent. |
| **Contraparte** | The entity being charged. |
| **Enlace de pago** | Tokenized URL `/p/:token` that the counterparty opens. |
| **Recordar** | Send a reminder email using the same link. |
| **Reenviar** | Mint a new token and send a fresh link (used for expired / failed links). |
| **Directo** | Cobro created directly in Tesote, not synced from an ERP. |
| **Layer 1 / Layer 2** | Tesote approval (L1) vs bank authentication (L2). See `claim-flow.html` for the L2 surface. |

---

## Appendix B — Reference wireframes

| Surface | File |
|---|---|
| Cobros list + dropdowns + state indicators | `../prototypes/pro-112/workspace-shell.html` |
| Cobro side panel (detail view) | Same file, click any Cobro row |
| Send-email modal | Same file, click Enviar on `PRIMERA FACTURA, S.A.` |
| Counterparty claim flow (payer side) | `../prototypes/pro-112/claim-flow.html` |
| Contraparte 360 detail | Same file, click any client name |

Wireframes to be built (see §10 ticket 4 onwards):
- [ ] Create Directo form
- [ ] Empty state (zero cobros)
- [ ] ERP first-connect flow
- [ ] Bulk-send modal
- [ ] Cancel confirmation (3 copy variants)
- [ ] Payment-failed state in side panel
- [ ] Dispute banner state in side panel
- [ ] Link-expired state + resend CTA
- [ ] ERP sync error banner
- [ ] Sync-in-progress states (importing N of M)
- [ ] Loading skeletons for list + panel

---

*End of Cobros v1 spec. Open an issue on PRO-112 with any section that needs clarification before sprinting.*
