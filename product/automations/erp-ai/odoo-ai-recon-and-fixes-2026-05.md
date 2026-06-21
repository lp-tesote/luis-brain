---
title: Odoo AI — Reconciliation Flow + Bug Findings + Fixes
tags: [product, ai, odoo, reconciliation, debugging]
updated: 2026-05-25
status: draft
---

# Odoo AI — Reconciliation Flow + Bug Findings + Fixes

Bundled record of the 2026-05-25 session with [[majo-vero]]'s counterpart Mariel testing Tesote AI on Odoo, the bugs surfaced, Dan's mining + ship response (PR #7154), and the foundational reconciliation walkthrough that should inform every future automation we layer on this surface.

Related: [[odoo-mcp]] (product strategy), [[flagship-workflows]] (Conciliación Relámpago is the workflow this powers), [[winning-vs-horizontal-ai]] (the moat we're building requires getting this layer right).

---

## 1. Session context (2026-05-25)

Mariel + Luis on Zoom, working through live Odoo flows in the Tesote AI chatbot:

- **Goal**: put Tesote AI in a pressure cooker — if someone who knows Odoo well would rather do it in Odoo, we have a problem
- **Tasks attempted**: (a) issue a credit note against Avanti (churning client, won't pay open invoice), (b) create a new invoice for Cenco Zotti at the negotiated paralelo rate
- **Output**: neither completed cleanly; bugs documented below

Recording lives on the call thread.

---

## 2. Bugs found

### 2.1 Bs vs USD: "1 USD = 1 Bs" treatment (Avanti)

When asked to create the credit note, the AI took the **USD line amount** and dropped it into the **Bs total field** — effectively treating 1 USD = 1 Bs. Same bug seen earlier in the week, still recurring.

Mariel's observation: the credit-note flow itself should be trivial — **duplicate the invoice, mark as nota de crédito, post**. The AI was overcomplicating into many steps.

### 2.2 BCV rate truncation + token exhaustion (Cenco Zotti)

Two issues stacked:

- **Rate truncation**: BCV rate displayed in Odoo has **4 decimals** (e.g. `96.9572`). Tesote AI was truncating to **2 decimals** before computing the Bs total, so the proposed total didn't match what Odoo would generate at post-time.
- **Possible buy vs sell rate confusion**: Mariel suspected the AI may have pulled the *compra* rate instead of *venta* — unconfirmed.
- **Out of tokens**: the conversation hit token exhaustion before the AI could land a draft in Odoo. Never completed the flow.

### 2.3 Product ask raised: per-conversation IDs

Today there's no way to point at "this specific conversation" when reporting bugs. Proposed adding a unique conversation ID surfaced in the UI so reports → debugging is one click.

---

## 3. Dan's response — PR #7154 (shipped)

### Shipped

- **Conversation IDs in the UI** — subtle copy-to-clipboard footer below the composer. Every AI tool-call failure also tags Sentry with `ai_conversation_id` + `ai_tool` + `ai_workspace_id`. Customer reports the footer id → Sentry breadcrumb is one click away.
- **`Intl.NumberFormat` across renderers** (per Sebastian's call) — new shared `formatMoney(cents, currency)` helper. VES rows now render with `Bs.` prefix and `.`/`,` grouping; chart tooltips pick up currency per series. Stops the AI from hand-formatting money strings in chat — found in **8 of 8** sampled conversations.
- **Plan doc** at `docs/plans/tesote-ai-odoo-fixes-2026-05/` (treasury repo) — captures the framing pivot + 15 evidence-backed behavioural rules from mining 10 conversations.

### Top 5 mining findings by impact

1. **Field-name guessing loops** — root cause of "ran out of context" sessions. AI burns 8+ tool calls cycling through `x_studio_…` / `concepto_islr_id` / `l10n_ve_islr_concept_id` variants.
2. **Hand-formatted money in prose** — in 8/8 convs. Renderer fix ships now; system-prompt rule follows.
3. **Silent Odoo rate overrides at post-time** — user supplied 550, Odoo silently applied BCV 385.272 at post. AI presented draft as final. (This is the Cenco Zotti class of bug.)
4. **`currency_id` mis-derivation on transfers** — user said "USD 15,000", AI wrote `currency_id: VEF`. **Same class as the Avanti 1 USD = 1 Bs bug.**
5. **Recon matches without amount sanity floor** — AI proposed matching Bs 326,443 BSL to Bs 773 invoice because partner matched.

### Held pending Mariel's writeup

Gated `apply_invoice` / `apply_payment` / `apply_credit_note` actions with explicit `rate` + `rate_source` args. Dan's framing: **"the signature itself is the forcing function"**. Need the collection-flow taxonomy before locking required-arg shapes.

### Coming next (independent of writeup)

- System-prompt edit with the 8 always-applicable rules from the mining
- **Auto-compact at 60%** (Sebastian's suggestion) — addresses token exhaustion which is just Rule 1 downstream
- Working-file routing through `Ai::McpResultSerializer` — coordinate after PR #7142 lands

---

## 4. Open: Mariel's collection-flow taxonomy (UNBLOCKER)

Dan needs from Mariel — for each flow, **which rate applies** and **what the AI should confirm before posting**:

- USD → Bs invoice (USD-denominated invoice paid in Bs)
- Bs → Bs indexed (Bs-denominated invoice with USD indexation)
- Partial payments
- Credit notes vs refunds
- (others Mariel identifies)

Without this, the gated actions can't ship — and gated actions are the structural fix for the entire Bs/USD bug class (#2.1, #2.2, mining findings #3 and #4).

**Luis owes**: nudge Mariel + provide air cover if she needs to deprioritize other work for this.

---

## 5. Foundational reference — current manual reconciliation flow (Mariel's process in Odoo)

The reconciliation cycle has **three artifacts** that need to land before an invoice is fully closed:

1. The **invoice** (already created in Odoo)
2. The **bank statement movement** (arrives via extract upload — Tesote loads this automatically today)
3. The **payment registration** (Odoo's `pago` object, which generates an accounting entry)

### 5.1 Step-by-step (Mango Center example)

1. **Invoice exists** in Odoo (created previously).
2. **Bank movement arrives** in the BNC statement → pulled into Odoo via Tesote.
3. **Register the payment manually**:
   - Clientes → Pagos → Nuevo
   - Action: `Recibir`
   - Customer: Mango Center
   - Importe: **must exactly match** the bank amount
   - Fecha + número de referencia (Mariel always sets the bank reference here)
   - Diario: BNC (the bank that received the money)
   - Save → Odoo generates accounting entry: **Dr. Banco Transitorio / Cr. Cuentas por Cobrar**
4. **Cross the payment with the invoice**:
   - Clientes → Facturas → Mango Center → open the oldest open invoice
   - Scroll down → list of all that customer's payments → select the one just created → cross it
5. **Auto-reconciliation kicks in**:
   - Odoo's "Coincidencia perfecta de facturas" model matches the bank statement against the transitory bank entry by reference number → marks both as conciliated automatically.
6. **Validation**: Tablero → bank account (e.g. 5097 = Banesco) → entry should show green.

### 5.2 Why the "banco transitorio" detour?

Two valid approaches in Odoo:

- **Direct**: cross the bank statement directly against the invoice (some Tesote clients do this — less control).
- **Banco transitorio** (Mariel's preferred): use transitory bank as a buffer. Adds a control layer — you can reconcile *before* you've matched 1-to-1 with invoices. Standard accounting-control pattern.

Mariel pre-built this as a `plantilla` (template) in Odoo so the entry isn't created from scratch each time.

### 5.3 Compressed flow Luis is proposing for Tesote

> Bank movement arrives → **Tesote recognizes movement + invoice + does the cross** → Tesote sends the already-conciliated package to Odoo.

For Tesote to be the centralizador, Mariel said it needs to handle **three inputs**:

1. **Comprobantes de retención** — receive + register + cross with invoice
2. **The payment itself** (the movement)
3. **The categorized bank statement entry**

With those three, Tesote can do a "perfect match" on its side and ship the resolved state to Odoo. This is exactly the [[flagship-workflows]] "Conciliación Relámpago" pattern, just specified.

---

## 6. Edge case: exchange-rate gain/loss (diferencia en cambio)

When a client pays a month after invoice date, the BCV rate has moved → customer pays a slightly different Bs amount than what was invoiced. Generates a **diferencia en cambio realizada** (ganancia o pérdida).

### 6.1 How Mariel handles it today

1. Run the reconciliation as above.
2. Reportes → Libro Mayor → Cuentas por Cobrar → Group by Client → open client (e.g. Doña Emilia).
3. See the residual — the line shows what's left unmatched (e.g. 17,000 Bs over/under).
4. Contabilidad → create a manual **asiento contable** marked "Ajuste por diferencia en cambio realizado" — closes the receivable, posts to ganancia/pérdida en cambio.
5. Select the bank partida + the asiento contable → Conciliar.

### 6.2 What "should" happen (Mariel's note)

The cleaner pattern: issue a **nota de débito** (if client overpaid) or **nota de crédito** (if underpaid) for the difference → cross with the payment under the original invoice. Same result, but proper documentation instead of a raw asiento.

### 6.3 Odoo config the connector should read

Contabilidad → Configuración → Cuentas por defecto exposes:

- Ganancia por diferencia en cambio realizada (account)
- Pérdida por diferencia en cambio realizada (account)
- Diario where these post
- Plus defaults for: anticipos, bancos transitorios, transferencias internas, descuentos, IGTF, gastos/ingresos diferidos

**Mariel flagged**: the Tesote connector should be able to read all of this — meaning Tesote can know per-client which accounts to post diferencia en cambio against, without re-asking each time.

---

## 7. Product implications — what Tesote AI needs to land for full recon automation

1. Ingest comprobantes de retención + bank statements + match to open invoices
2. Auto-suggest the cross — "this bank movement closes invoice X for Y Bs"
3. Compute the residual and propose: nota de débito / nota de crédito / manual asiento
4. Read Odoo's default account config (gain/loss accounts, transitory bank, etc.) via the connector so it posts to the right places without prompting
5. Handle the three-monedas reality (Bs / USD / BCV rate at invoice date vs payment date) — **this is where #2 and Dan's mining #3 and #4 currently break**

The last one is the structural blocker. Solving it = unblocking everything in [[flagship-workflows]] that touches money.

---

## 8. Cross-cutting business issue surfaced (separate from AI bugs)

Mariel's current invoice-creation process for Cenco Zotti and other clients requires juggling **multiple rates** (paralelo, BCV, promedio, euro) outside Odoo in a spreadsheet, then back-calculating the Bs amount that will reproduce the agreed USD figure. This is a pricing/contract-structure problem, not an AI problem:

- Luis's proposal to Roberto + Mariel: **renegotiate all clients to a single rate (BCV)**, raise the USD price 30–35% if needed to absorb the brecha. "If you want to pay in USD via the US entity, $100. If via the VE entity in Bs, $130 — but everything at BCV."
- Mariel concurred: at some point a fiscalización will hit and "I work at paralelo" isn't a defensible answer.
- Status: pending the lawyer conversation Luis has lined up (Roberto knows the contact).

Tracked separately because it doesn't block the AI fixes — but if it lands, it dramatically simplifies the AI's rate-handling logic (single rate per client, sourced from Odoo, no prompting).

---

## 9. Loose threads

- Banking-side conversation (separate thread of the same call): Mariel's pushback on consolidating into BNC. Luis's position — for client-facing flows we optimize for banks that give us *full transaction descriptions* (BNC, Banca Amiga w/ debit card); BanPlus + others for internal treasury moves only. Doesn't affect the AI work directly but informs which bank rails we prioritize for the recon pipeline.
- Tasa source on AI: needs a definitive answer on which rate the AI is pulling and from where. Mariel showed Odoo has compra/venta; AI's output suggested it might be using the wrong one.
- The credit-note flow itself ("just duplicate + mark") should be a one-shot tool call, not a multi-step composition. Worth flagging to Dan as a "simple action" candidate.

---

## 10. Next moves

- [ ] **Mariel**: collection-flow taxonomy writeup (unblocks gated actions)
- [ ] **Dan**: ship system-prompt edit + auto-compact at 60% + working-file routing (independent of Mariel)
- [ ] **Luis**: nudge Mariel on the writeup; surface the brecha-cambiaria renegotiation in the next exec sync
- [ ] **Luis**: lawyer convo on the asesoría-vs-servicio facturación question (Mariel wants to be in that meeting)
- [ ] Verify the AI's rate-source (compra vs venta vs BCV) once we have a conversation ID to point at

When this matures, the recon-flow section (5–7) is promotion-worthy to the team KB — it's the canonical reference for how Conciliación Relámpago has to behave.
