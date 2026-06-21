---
title: "Prompt — CAPCA counterparty HTMLs iteration"
tags: [drafts, prompt, capca, tesote-negocios, prototypes]
updated: 2026-04-29
author: Luis Pulgar
status: draft
context: |
  For feeding to a fresh Claude session to iterate on claim-flow-capca.html
  and the canonical claim-flow.html alongside the spec PRD. Generated after
  the 2026-04-24 Rosa Toro call and ahead of the 2026-04-30 Claudia meeting.
---

# Prompt — CAPCA counterparty HTMLs iteration

> Copy from the start of "## Prompt" below. Everything above is meta.

## Decisions baked in (so future-Luis remembers what this prompt encodes)

- **Multi-pay** — promote to v1, cross-client (canonical + CAPCA)
- **Partial pay** — defer to v1.1, do not build yet (capture in spec only)
- **Contraparte 360 from payer side** — promote to v1, cross-client
- **Saldo Disponible para Compra** — v1, **CAPCA-only** (don't leak to canonical)
- **Payment terms display (flavor a — display-only)** — v1, cross-client. Skip flavor b (early-pay discount, v1.1) and flavor c (propose-a-plan, never)

If any of these flips, update the prompt before re-firing.

---

## Prompt

```
You are iterating on the CAPCA-specific counterparty HTMLs and updating the
spec to match. This is Tesote Negocios — the payer-side portal — being
tailored for CAPCA, our highest-priority sales engagement.

# Context you need

- Repo: ~/Programming/tesote/luis-brain
- Canonical (cross-client) prototype: product/tesote-pay/prototypes/pro-112/claim-flow.html
- CAPCA-specific variant (the one you're editing): product/tesote-pay/prototypes/pro-112/claim-flow-capca.html
- Workspace-side CAPCA variant: product/tesote-pay/prototypes/pro-112/workspace-capca.html
- Spec (must update alongside HTML changes): product/tesote-pay/plans/counterparty-portal-prd.md
- Engineering handoff README: product/tesote-pay/prototypes/pro-112/README.md
- CAPCA portal vision (source — Rosa Toro / DigiSalud, 2026-04-24):
  sales/clients/capca/rosa-vision-doc-2026-04-24.md
- Tomorrow's Claudia meeting prep (decisions framing):
  sales/clients/capca/claudia-meeting-prep-2026-04-30.md
- Master CAPCA blueprint: customer-experience/playbooks/blueprint-operativo-capca.md

Read the prep doc and the Rosa vision doc first — they explain the WHY
behind these changes.

# Source-of-truth rule

claim-flow.html is canonical for visual system + flows. claim-flow-capca.html
follows it for everything EXCEPT the CAPCA-specific additions below. Don't
let CAPCA-only features leak into claim-flow.html. If a feature is truly
cross-client, promote it to claim-flow.html and update the spec.

# Visual system invariants (don't drift)

- Mercury pastel pills (lavender/amber/salmon/mint/gray); filled bg, no border, dark text, 5px radius
- Pill + button uniform 96px width, padding 3px 8px, font 11px
- Acción column header label "Acción", content centered
- Date columns nowrap
- Account number 20 digits, phone 11 digits

# Features to add

## 1. Multi-invoice select + consolidated pay (CROSS-CLIENT — promote to canonical)

Promote from v1.1 to v1. Update spec §"v1 scope" table accordingly.

UX:
- Add a checkbox column at the leftmost position of the Pagos table
  (claim-flow.html and claim-flow-capca.html both)
- Header checkbox toggles select-all-visible
- Selecting ≥1 row reveals a sticky bottom action bar:
  - Left: "X facturas seleccionadas · Total Bs. {sum}"
  - Right: "Pagar seleccionadas →" (primary blue, 96px-or-wider as needed for content)
- Sticky bar disappears on deselect-all or after successful pay
- Per-row "Pagar" action stays for single-invoice case (no regression)

Pay flow changes (4-step overlay):
- Step 1: invoice summary block becomes a STACKED list of selected invoices
  (vendor / factura # / monto each), with grand total below in larger weight
- Step 2 (OTP): unchanged
- Step 3 (procesando): unchanged
- Step 4 (éxito): comprobante card now shows N rows of "Factura X — concepto — monto"
  with "Total pagado" footer line. Sub copy: "Pagaste {total} a {vendor}.
  Le notificamos del pago a tu proveedor y te enviamos el comprobante por correo."
- Single BNC debit on the backend; surface as one referencia number in the comprobante

State model:
- One Cobros row in the workspace per invoice (paid individually, even if bundled in pay)
- Group identifier on the Event log so the workspace can show "pago en lote (3 facturas)"
- Update spec §3 entity list — add `payment_batch_id` (nullable) to Cobro
- Update spec state machine notes — multi-pay doesn't add states, just a batch ID

## 2. Contraparte 360 from payer's POV (CROSS-CLIENT — promote to canonical)

Currently a prototype limitation per README ("clicking a proveedor in Contrapartes
doesn't open a detail page"). Build it.

UX:
- Click any row in Contrapartes (sidebar item) → opens a detail page (not side panel —
  full route, mirroring how the workspace handles its Contraparte 360)
- Layout sections, top-to-bottom:
  1. Header — proveedor logo + name + RIF + "En red Tesote" check icon
  2. Resumen card — Total facturado YTD, Total pagado YTD, Deuda actual,
     Plazo promedio (días)
  3. Pago / facturación timeline — line or bar chart, last 12 months
  4. Historial de facturas — full table (incl. paid), filter by año + estado
  5. Acciones — "Descargar estado de cuenta (PDF)" / "Descargar (Excel)"
- Both buttons are stubs that toast: "Generando estado de cuenta…" then
  "Estado de cuenta descargado" (no real PDF in prototype)
- Estado de cuenta concept: cumulative, all invoices + payments + retenciones,
  date-range selectable in production (v1 prototype: just YTD)

Spec updates:
- Add to spec §"v1 scope" table: "Contraparte 360 (read-only) + estado de cuenta
  download (PDF/Excel)"
- Remove from spec "Out of scope (v1)": "Payment history and exports" — that's
  now in scope

## 3. Partial payment — DEFERRED, do not build yet

Luis flagged it in the brainstorm. Decision is to hold for v1.1 unless Claudia
explicitly asks. Capture in the spec under "Out of scope (v1)" with a note:
"Partial payment requires `parcial` state, abono ledger, and partial-clearing
logic in SAP FI — defer to v1.1 unless customer demand surfaces."

Do not add UI elements for it. If you find yourself drafting a "monto a pagar"
input on the invoice row, stop — that's v1.1.

## 4. Saldo Disponible para Compra (CAPCA-ONLY — claim-flow-capca.html only)

Do NOT add to claim-flow.html. This is CAPCA-specific because it depends on
SAP credit-limit data we don't have for other clients yet.

UX:
- New card at the top of the Pagos screen (above the invoice table)
- Card title: "Saldo disponible para compra"
- Big number: Bs. {límite_crédito − vencidas − por_vencer}
- Three breakdown lines below:
  - Límite de crédito SAP: Bs. X
  - Facturas vencidas: − Bs. Y
  - Facturas por vencer: − Bs. Z
- If saldo ≤ 0: card border + number switch to amber (Mercury pastel amber),
  helper text: "Saldo bajo. Paga facturas vencidas para liberar crédito."
- DO NOT block any UI based on this. Display-only. (Blocking is a
  Solicitudes-module feature, out of scope per Claudia prep.)

Mock numbers (use realistic CAPCA-scale figures):
- Límite: Bs. 8,500,000
- Vencidas: Bs. 1,200,000
- Por vencer: Bs. 3,400,000
- Saldo: Bs. 3,900,000

Spec note: add a CAPCA-specific addendum to the PRD ("Client-specific
extensions" section) so we have a place for these one-off requirements.
First entry = Saldo Disponible.

## 5. Payment terms display (CROSS-CLIENT — promote to canonical, scope (a) only)

Doing the display-only flavor. NOT building the early-pay-discount or
propose-a-plan flavors yet.

UX:
- Pagos table: add "Plazo" column between "Vence" and "Estado" — values like
  "30 días", "Contado", "60 días". Width tight; nowrap.
- Side panel (when row clicked): add "Términos de pago" line in the Detalles section
- Contraparte 360 (from feature 2): add "Plazo otorgado: 30 días" + "Plazo
  promedio de pago: 28 días" to the Resumen card
- Inicio dashboard: small line under the greeting card: "Tu plazo de crédito
  con {vendor}: 30 días" (only if there's exactly one vendor; suppress if multi-vendor)

Spec:
- Add `payment_terms_days` (int, nullable) and `payment_terms_label`
  (enum: contado | credito_30 | credito_60 | credito_90 | custom) to the
  Counterparty entity in spec §3.1
- Add `payment_terms_snapshot` (string) to Cobro — captures the term at
  time of issue, immutable per invoice
- Source: ERP-pulled per counterparty in v1; manually editable in workspace
  Contraparte view (out of scope for THIS handoff — workspace-side change)

# Out of scope for this iteration

- Real PDF/Excel generation (stubs only)
- Workspace-side Contraparte editing UI for payment terms
- Partial payments (deferred)
- Early-pay discount UX
- Multi-vendor logic in dashboard payment-terms line (just hide if multi)
- Wrong-OTP / bank-rejection error states (still v1.1 per existing spec)

# Files you'll touch

Required:
- product/tesote-pay/prototypes/pro-112/claim-flow.html (features 1, 2, 5)
- product/tesote-pay/prototypes/pro-112/claim-flow-capca.html (features 1, 2, 4, 5)
- product/tesote-pay/plans/counterparty-portal-prd.md (all spec updates)
- product/tesote-pay/prototypes/pro-112/README.md (update at-a-glance,
  feature list, known limitations table — remove items now built)

Don't touch:
- workspace-shell.html / workspace-capca.html (workspace side, out of this scope)
- claim-flow284.html / workspace-shell284.html (legacy variants)

# Working style

- Walk both HTMLs cold first to understand current structure
- For each feature, read the relevant spec section before touching the HTML
  so your changes match the spec's vocabulary
- After each feature: update the spec, then the HTML, then verify the README
  doesn't lie about it
- Mock data realistically — use Spanish, use Bs. amounts in the millions
  (CAPCA scale), use realistic vendor names (Kaizen Logística, MARCAS PROPIAS,
  PRIMERA FACTURA S.A. are already seeded in the prototype — extend the set)
- Comments in HTML/JS only where the WHY isn't obvious

# Done =

1. All 4 building features visible and interactive in their respective HTMLs
2. Partial payment captured in spec as deferred, no UI
3. Spec PRD reflects new v1 scope additions + new entity fields
4. README at-a-glance + limitations table updated
5. claim-flow.html and claim-flow-capca.html stay visually consistent except
   for the CAPCA-only saldo card
6. No regressions in existing flows (single-invoice pay, auth, comprobante)

Report what you built, what you skipped and why, and any open questions
that surfaced for Luis to decide.
```
