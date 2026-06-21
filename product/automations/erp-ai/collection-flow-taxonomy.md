---
title: Collection-Flow Taxonomy — Tesote AI for Odoo
tags: [product, ai, odoo, accounting, reconciliation]
updated: 2026-05-25
status: draft
---

# Collection-Flow Taxonomy — Tesote AI for Odoo

**Purpose**: enumerate every collection flow Tesote AI will encounter, the rate that applies, and what the AI must confirm before posting. This is the unblocker for gated `apply_invoice` / `apply_payment` / `apply_credit_note` actions in PR #7154 follow-up. Per Dan: *"the signature itself is the forcing function"* — required args make wrong calls impossible to construct.

**Owner**: Mariel Álvarez (accounting). Luis scaffolds; Mariel validates/completes.
**Consumer**: Daniel Francoeur (eng) — locks tool signatures from this doc.
**Status**: scaffold. Sections marked `[MARIEL]` need her input before locking.

Related: [[odoo-ai-recon-and-fixes-2026-05]] (bug context + PR #7154), [[odoo-mcp]] (product strategy), [[odoo-ai-fixes-arc]] (memory: Dan's design principle).

---

## 1. Framing — the three axes a flow varies on

A collection flow is defined by three independent axes. The taxonomy is the cartesian product of these (filtered down to the combinations that actually occur in our book).

### Axis A — Invoice currency setup

| Code | Setup | Description |
|---|---|---|
| `USD-pure` | Invoice in USD, no Bs side | US entity (Tesote Technologies Inc.) — fully out of VE fiscal scope. |
| `USD-dual` | Invoice in USD with Bs equivalent displayed (Odoo dualidad de monedas) | VE entity (TST Servicios) — fiscal record is USD-denominated, Bs shown at BCV for fiscal reference. |
| `Bs-pure` | Invoice in Bs, no USD reference | Pure Bs commercial deal (rare in our book). |
| `Bs-indexed` | Invoice in Bs, indexed to a USD amount the client agreed to | Commercial agreement at non-BCV rate (paralelo, promedio). Bs amount is computed = USD × negotiated rate. |

### Axis B — Payment currency

| Code | Currency received |
|---|---|
| `pay-USD` | USD (Zelle, Chase, dollar cash, USD bank-to-bank) |
| `pay-Bs` | Bs (any VE bank rail) |

### Axis C — Payment timing vs invoice

| Code | Timing |
|---|---|
| `same-day` | Payment lands on invoice date — no FX delta. |
| `deferred` | Payment lands later than invoice date — FX rate has moved → diferencia en cambio realizada (ganancia o pérdida). |

### Plus four orthogonal modifiers

- **Completeness**: full / partial / overpayment
- **Retentions present**: ISLR / IVA / both / none
- **Document type for corrections**: credit note (nota de crédito — fiscal) / debit note (nota de débito — fiscal) / refund (devolución, no fiscal)
- **Rate source for the conversion**: BCV / paralelo / promedio / euro paralelo

---

## 2. The flows we actually see

Enumerated by frequency in our book. `[MARIEL]` to confirm/correct + add anything missing.

### Flow 1 — `USD-dual` × `pay-Bs` × `deferred` (the dominant case)

**Example**: Cenco Zotti. We invoice in USD (with Bs dual display at BCV at invoice date). Client pays in Bs ~30 days later at a different BCV rate.

- **Rate at invoice creation**: BCV at invoice date (4 decimals — *must not truncate*)
- **Rate at payment posting**: BCV at payment date
- **Diferencia en cambio**: yes, expected. Account: ganancia/pérdida en cambio realizada (read from Odoo config).
- **`currency_id` on invoice**: `USD`
- **`currency_id` on payment**: `VES` (the bank movement is in Bs)
- **AI pre-post confirmations**:
  - [ ] Rate at invoice date matches BCV-at-invoice-date (4 decimals preserved)
  - [ ] Rate at payment date matches BCV-at-payment-date (4 decimals preserved)
  - [ ] Bs total ≡ USD × rate-at-payment-date (within 1 Bs tolerance) — **amount sanity floor**
  - [ ] If Odoo will silently override at post (Dan's mining finding #3), surface this to user *before* post, not after
- **Sanity checks**: if proposed Bs / USD ratio falls outside `[BCV × 0.95, paralelo × 1.05]`, abort and ask user.
- `[MARIEL]` Confirm: when client pays Bs at paralelo rate (i.e. more Bs than BCV-at-payment-date would imply), is the surplus posted as ganancia en cambio realizada, or as a separate "ajuste comercial" account?

### Flow 2 — `Bs-indexed` × `pay-Bs` × `same-day` (subscription invoicing today)

**Example**: Mariel's current process — Cenco Zotti subscription. We compute Bs = USD × paralelo (or whatever rate was negotiated), invoice in Bs, client pays the same Bs amount.

- **Rate at invoice creation**: negotiated rate (paralelo / promedio) — **not** BCV
- **Rate stored on invoice**: BCV at invoice date (for fiscal record), even though commercial amount used paralelo
- **`currency_id` on invoice**: `VES`
- **Indexation tracking**: the USD-equivalent at the negotiated rate is recorded as a memo / studio field (`[MARIEL]` which field?)
- **AI pre-post confirmations**:
  - [ ] Negotiated rate is explicitly captured (`rate_source: paralelo` not `bcv`)
  - [ ] User confirms the negotiated rate value (no defaulting — must come from contract / convo)
  - [ ] Bs total ≡ USD × negotiated rate (within 1 Bs tolerance)
- **Open**: Luis is pushing to **deprecate this flow entirely** by renegotiating all clients to a single BCV-based price. If that lands, this flow collapses into Flow 1. Track separately — see [[odoo-ai-recon-and-fixes-2026-05]] §8.

### Flow 3 — `USD-pure` × `pay-USD` × any timing

**Example**: US-entity subscriptions (Tesote Technologies Inc., Stripe/Chase payments).

- **Rate**: N/A (no Bs side)
- **`currency_id`**: `USD` on both invoice and payment
- **AI pre-post confirmations**:
  - [ ] No rate args supplied (signature must reject `rate` for `USD-pure` flow)
  - [ ] Amount matches invoice exactly (no FX wiggle)
- This is the simplest flow. Use as the regression-test flow.

### Flow 4 — `USD-dual` × `pay-USD` × any timing

**Example**: VE-entity invoice but client pays via dollar account (Zelle to Tesote VE, or USD cash).

- **Rate at invoice creation**: BCV at invoice date (fiscal record)
- **Rate at payment**: N/A for amount (USD = USD), but fiscal record needs BCV-at-payment-date for the Bs equivalent line
- **`currency_id` on invoice**: `USD`
- **`currency_id` on payment**: `USD`
- **AI pre-post confirmations**:
  - [ ] Amount matches invoice exactly in USD
  - [ ] Bs-equivalent line on payment posts at BCV-at-payment-date (Odoo handles automatically if connector reads default account config)
- `[MARIEL]` Confirm: any IGTF implications when receiving USD into VE entity?

### Flow 5 — Partial payment (orthogonal modifier on Flows 1, 2, 4)

- **Logic**: payment amount < invoice amount in matching currency
- **Resolution**: payment cruzado against invoice leaves residual; invoice stays open
- **AI pre-post confirmations**:
  - [ ] User explicitly confirms partial (not a typo) — surface "this leaves Bs X / USD Y open on invoice Z"
  - [ ] No diferencia en cambio asiento yet — wait for final payment
- `[MARIEL]` Confirm: do we post a partial diferencia en cambio at each partial pay, or only at full settlement?

### Flow 6 — Overpayment (orthogonal modifier)

- **Logic**: payment amount > invoice amount
- **Resolution options**:
  - (a) Apply surplus as advance against next invoice (anticipo)
  - (b) Issue nota de débito to absorb surplus into current invoice
  - (c) Refund (devolución)
- **AI pre-post confirmations**:
  - [ ] User picks resolution (a/b/c) — AI never auto-picks
- `[MARIEL]` Which is the default behavior in our book today?

### Flow 7 — Credit note (nota de crédito)

**Example**: Avanti (churning, won't pay). Open invoice → issue credit note to anular.

- **Rate**: inherits from original invoice (same `currency_id`, same rate, same Bs amounts) — **the AI should not recompute rates**
- **Posting behavior**: Mariel's note — "just duplicate the invoice and mark as nota de crédito". One-shot, not multi-step.
- **AI pre-post confirmations**:
  - [ ] Reason captured (churned client / billing error / overcharge / etc.)
  - [ ] Original invoice referenced
  - [ ] Amounts mirror original exactly (no recomputation)
  - [ ] If partial credit note, the residual on original invoice is computed correctly
- **Tool signature implication**: `apply_credit_note` should accept `original_invoice_id` and *not* accept `rate` — the rate is derived from the original. Refusing `rate` in the signature is what prevents the Avanti bug class.

### Flow 8 — Debit note (nota de débito)

**Example**: client paid more in Bs than the original Bs total because BCV moved — issue debit note for the difference.

- **Rate**: derived from the payment date (the rate at which the surplus was generated)
- **`currency_id`**: `VES`
- **AI pre-post confirmations**:
  - [ ] Justification linked to a specific payment (not free-form)
  - [ ] Amount = payment_bs − invoice_bs_at_invoice_date_rate
- `[MARIEL]` Confirm: is the cleaner pattern (your words) really debit note here, or is the manual asiento de diferencia en cambio still standard?

### Flow 9 — Refund (devolución)

**Example**: client paid for a service we're not delivering, we send the money back.

- **Posting**: NOT a fiscal document. Bank-side outflow + reversal of the receivable.
- **`currency_id`**: matches the original payment currency
- **AI pre-post confirmations**:
  - [ ] Linked to the original payment record
  - [ ] User confirms this is a refund (not a credit note) — *fiscal implications differ*
- `[MARIEL]` Confirm: refund vs credit note decision tree?

### Flow 10 — Retentions present (orthogonal modifier on Flows 1, 2, 4)

**Example**: corporate clients (Roburestyres, large enterprises) apply ISLR + IVA retentions at payment time.

- **Logic**: payment amount = invoice amount − ISLR − IVA. AI must reconcile invoice = payment + retention vouchers.
- **AI pre-post confirmations**:
  - [ ] Retention voucher(s) ingested + linked
  - [ ] Sum of payment + retentions ≡ invoice total (within 1 unit tolerance)
  - [ ] ISLR % matches the registered `concepto_islr_id` for the client × service combo
- `[MARIEL]` What's the canonical list of ISLR conceptos we use? (Dan's mining #1 — field-name guessing — comes from the AI not knowing this.)

---

## 3. Proposed tool signatures (for Dan)

Working scaffold. Refine after `[MARIEL]` items above resolve.

### 3.1 `apply_invoice`

```
apply_invoice(
  workspace_id: required,
  partner_id: required,
  flow_code: enum required,           # USD-pure | USD-dual | Bs-pure | Bs-indexed
  amount_usd: conditional,            # required iff flow_code in {USD-pure, USD-dual, Bs-indexed}
  amount_bs: conditional,             # required iff flow_code in {Bs-pure, Bs-indexed}
  rate: conditional,                  # required iff flow_code in {USD-dual, Bs-indexed}
  rate_source: enum conditional,      # required iff rate present; one of {bcv, paralelo, promedio, euro_paralelo}
  rate_date: conditional,             # required iff rate present
  currency_id: derived,               # AI cannot pass — derived from flow_code
  invoice_date: required,
  due_date: optional,
  lines: required,                    # [{description, quantity, unit_price, tax_ids}]
)
```

Forcing-function moves:
- `currency_id` is **derived**, not user-supplied → eliminates Avanti class
- `rate` cannot be supplied without `rate_source` + `rate_date` → eliminates Dan mining #3
- `flow_code` is enum → AI must classify the flow upfront, not freestyle
- 4-decimal rate preserved in the signature schema (use `decimal(18,4)` or higher; reject 2-decimal floats)

### 3.2 `apply_payment`

```
apply_payment(
  workspace_id: required,
  partner_id: required,
  invoice_id: required,
  payment_amount: required,           # in payment currency
  payment_currency: required,         # USD or VES
  payment_date: required,
  payment_rate: conditional,          # required iff payment_currency differs from invoice currency
  payment_rate_source: enum conditional,
  retention_voucher_ids: optional,    # array
  partial: bool default false,
  diff_en_cambio_account_id: derived, # read from Odoo default account config
)
```

Forcing-function moves:
- `payment_rate` required when currencies differ → no silent BCV override
- Retention vouchers are an input, not an inferred state → AI can't post a payment that doesn't add up

### 3.3 `apply_credit_note`

```
apply_credit_note(
  workspace_id: required,
  original_invoice_id: required,
  reason: enum required,              # churn | billing_error | overcharge | service_not_delivered | other
  scope: enum required,               # full | partial
  partial_amount: conditional,        # required iff scope = partial; in original invoice currency
)
```

Forcing-function moves:
- No `rate` arg accepted → AI cannot recompute, must mirror original invoice
- No `currency_id` arg accepted → derived from `original_invoice_id`
- `scope` is enum → no implicit assumption of full

---

## 4. Sanity-floor rules the AI must apply pre-post

Independent of flow, before any `apply_*` call:

1. **Amount floor**: if `|invoice_amount − payment_amount_in_invoice_currency|` > 5% of invoice amount, abort + ask user. (Addresses Dan's mining #5 — recon match without sanity floor.)
2. **Rate sanity**: if `rate` is outside `[BCV × 0.5, paralelo × 1.5]`, abort + ask user.
3. **Decimal precision**: rates must carry ≥4 decimals end-to-end. Any 2-decimal float in the chain triggers abort.
4. **Currency consistency**: derived `currency_id` must not be `VES` when `flow_code` ∈ `{USD-pure, USD-dual}`. If mismatch, abort.

---

## 5. Open questions for Mariel

Compile to one writeup pass:

1. Flow 1 — paralelo surplus account treatment?
2. Flow 2 — which Odoo studio field captures the negotiated USD-equivalent for indexed invoices?
3. Flow 4 — IGTF on USD payments to VE entity?
4. Flow 5 — partial diferencia en cambio at each partial pay, or only at full settlement?
5. Flow 6 — default overpayment resolution (anticipo / nota débito / refund)?
6. Flow 8 — debit note vs manual asiento de diferencia en cambio — which is standard?
7. Flow 9 — refund vs credit note decision tree (fiscal lens)?
8. Flow 10 — canonical ISLR concepto list per service/client type?
9. **Anything missing from this taxonomy?** — e.g. anticipo collection (collecting before invoice exists), prompt-payment discount, IVA-exempt clients, foreign-payer flows.

---

## 6. Next moves

- [ ] **Luis**: walk Mariel through this doc; her job is to (a) answer §5, (b) flag missing flows, (c) sanity-check the §2 defaults
- [ ] **Mariel**: produce filled-in version (edit in place or comment); target turnaround = `[MARIEL: date]`
- [ ] **Luis**: when §5 closes, ping Dan in #feat-ai-workspace to unblock the gated-actions PR
- [ ] **Dan**: lock tool signatures from §3 once §2 + §5 are settled

When this doc closes, it's promotion-worthy to the team KB — it's the spec for how every AI write-action on collections has to behave.
