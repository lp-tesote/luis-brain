---
title: Tesote AI for Odoo — chatbot in Tesote UI, MCP under the hood
tags: [product, automations, odoo, ai, mcp, chatbot, 10x]
updated: 2026-05-11
status: draft
---

# Tesote AI for Odoo

> Working draft. Different product from the Cockpit ([[odoo-prd]]). Same ICP. Ships first.

## TL;DR

A Tesote-branded chatbot inside the Tesote web app. Customers talk to it. It reads from and writes to their Odoo. AI does the work.

**Distribution: Tesote UI only.** Not Claude desktop. Not an external MCP. Not a registry listing. The chat lives behind the Tesote login, in our app, with our brand on it. MCP is the internal tool-protocol — it doesn't surface to the customer.

**Zero dependencies on existing Tesote product.** No Connect. No Pagos. No Cobros. No Treasury Rails plumbing in the critical path. Fresh build, fast stack, ship-ship-ship velocity. We're frustrated with clunky/slow internal implementations — this product doesn't inherit any of that.

**The bet**: LATAM mid-market finance teams are not AI-native yet. They don't have Claude desktop. They don't know what MCP is. They might use ChatGPT casually but not for accounting. **There's a window where Tesote can be their first real AI-at-work experience**, before they discover Claude/Gemini/ChatGPT on their own. Own the surface while we can.

## Why "Tesote UI only" is the right call right now

- **Customers aren't there yet** — installing Claude desktop, configuring an MCP endpoint, copy-pasting tokens: that's not the experience a 50-year-old controller in Caracas wants. She wants a tab in Tesote that looks like WhatsApp.
- **Own the surface, own the relationship** — every prompt, every wow moment, every share, every screenshot has Tesote on it. Free brand surface area. We lose that the moment customers go to Claude desktop instead.
- **Avoid support hell** — "my Claude desktop config isn't loading the MCP" is not a support ticket we want to inherit. Browser-based chat in Tesote is a known-quantity support surface.
- **Faster iteration loop** — we control the UI, we control the prompts, we control the model. No vendor blockers, no waiting on Anthropic's UX, no MCP-protocol limitations leaking through.
- **Capture before commoditization** — when AI assistants become commodity in LATAM (12–24 months), customers will know what they want. Until then, the default they meet first wins.

When the market matures and customers explicitly want to use Tesote's tools from inside Claude/Gemini/etc., we can flip the MCP server to be externally addressable. The architecture leaves the door open. The product, for now, does not.

## Why this is a different product from the Cockpit

Same as before — both target LATAM mid-market on Odoo, but different surfaces and different motions.

| | Cockpit | AI Chat |
|---|---|---|
| **Surface** | Tesote web UI: queues, dashboards, inbox | Tesote web UI: a chatbot |
| **Mental model** | "Manage finance work" | "Ask an assistant about my books" |
| **Tesote dependency** | Hard (Connect bank data is the moat) | None (just Odoo creds) |
| **Onboarding** | Productized 30-day flow, CS-driven | Self-serve in minutes |
| **Ergonomics** | Visual / spatial / list-driven | Conversational |
| **Time-to-wow** | Days–weeks (after setup) | Minutes (first useful answer) |
| **Sales motion** | Demo → contract → onboarding → adoption | Trial → habit → upgrade |
| **Pricing** | Per seat / % automated | Flat tier per Odoo instance, likely |

Same buyer can buy both. Or just one. They're separate SKUs.

## Why this ships first

- **Faster build** — chatbot + LLM + Odoo tool layer. No queue UIs, no inbox UIs, no recon engine to spec. Order-of-magnitude smaller v1.
- **Lower onboarding friction** — paste Odoo creds, start chatting. No mapping work, no taxonomy, no CS-driven 30-day flow.
- **AI-momentum tailwind** — the market is conditioned to expect AI. We're handing them what they're already asking for. Cockpit is a bigger sell ("re-platform your finance team").
- **Validates demand before we double down on the Cockpit** — if customers love chatting with their books, we learn what they want from AI before we spec the bigger product.

## Product principles

1. **Tesote chatbot UI is the ONLY surface.** No external MCP exposure in v1.
2. **Zero coupling to Tesote core.** A customer who has never touched anything else in Tesote can sign up, paste Odoo creds, and use this.
3. **Ship-fast / fresh stack.** Not stuck waiting on Treasury or Connect teams. Standalone codebase + standalone deploy. Reusing internal libs only when it speeds us up, never when it slows us down.
4. **Guided experience over open prompt.** Most customers won't know what to do with "ask me anything." First-run shows a use-case gallery; every chat surface has suggested-prompt chips; the empty state is never empty.
5. **Read-first, write-with-confirmation.** Reads return data instantly. Writes show a preview ("I'm about to create this vendor bill — confirm?") that the user clicks/types to approve.
6. **LATAM-native.** Spanish default. VE tax codes, retenciones, RIF/CI handling, bolívar/USD, libro mayor / libro de compras / declaración IVA fluent.
7. **Auditable.** Every write is logged with who, when, what AI suggested, what user confirmed, what got posted. Audit log is a tab in the chat.

## Vision

Adriana, controller at a Caracas distribution business, opens Tesote in her browser. The home tab is the **Asistente** — a clean chat window with the company name at the top, her name at the bottom-right. Below the input, six suggested prompts:

- *"¿Cuánto vendí el mes pasado por sucursal?"*
- *"Muéstrame los proveedores que no me han facturado en 30+ días"*
- *"Crea una factura para Movistar de $450, vence en 15 días"*
- *"¿Por qué subieron mis gastos de combustible este mes?"*
- *"Hazme la declaración de retenciones IVA"*
- *"Sube esta factura y créamela en Odoo"* (with a paperclip)

She clicks the first one. Three seconds later: a clean table, ten branches ranked by sales, total at the bottom, link to drill into any row. She didn't open Odoo. She might not open Odoo today.

She types: *"y la cuarta sucursal, ¿qué le pasó?"* The AI knows what "la cuarta sucursal" refers to (the one ranked #4 in the prior answer), pulls the detail, points at three large refunds that explain the drop. She forwards the conversation to her CEO.

That's the product.

## Starter use-case gallery (the wow moments)

This is the single most important thing besides the chat itself. Users won't discover what's possible on their own — we tell them. Curate ruthlessly. Each prompt below should:

- Work end-to-end in v1 (no half-broken demos)
- Produce a visibly-impressive answer in <10 seconds
- Be useful enough that the customer wants to do it again tomorrow

Organize as **categories** in the UI gallery. Show 4–6 prompts per category. Refresh the suggestions based on what's been used.

### "Dame visibilidad" — instant Q&A (lowest barrier, highest hit rate)
- "Resumen ejecutivo del mes pasado: ventas, gastos, utilidad"
- "Mis 10 clientes con mayor deuda vencida"
- "¿Cuánto le debo a [proveedor] en facturas abiertas?"
- "Compara mis gastos de enero vs febrero por categoría"
- "Saldo actual de todas mis cuentas bancarias"
- "¿Cuáles son mis 5 gastos más grandes este mes?"
- "Dame el flujo de caja proyectado de las próximas 4 semanas"

### "Hazlo por mí" — workflow execution (the wedge)
- "Crea un proveedor llamado [nombre] con RIF [J-XXX]"
- "Crea una factura para [cliente] por [monto], vence el [fecha]"
- "Categoriza la transacción de [monto] del [fecha] como [categoría]"
- "Marca la factura #[N] como pagada"
- "Concilia el depósito de ayer con la factura #[N]"

### "Lee este documento" — OCR / upload (the magic moment)
- Sube una factura PDF → "léela y créamela en Odoo"
- Sube un estado de cuenta bancario → "cárgalo y concilia lo que puedas"
- Sube un Excel de facturas → "créalas todas en lote, te las paso a aprobar"
- Foto de una factura impresa por WhatsApp → "captúrala como gasto"

### "Reportes de compliance" — VE-native, hard-to-do-elsewhere
- "Genera el libro de compras del mes en formato SENIAT"
- "Hazme el libro de ventas del mes"
- "Declaración de retenciones IVA del período actual"
- "Libro mayor de la cuenta [N] para el trimestre"
- "Reporte de retenciones ISLR practicadas el mes pasado"

### "Detecta cosas raras" — anomalies & insights (AI-magic moment)
- "¿Qué gastos del mes pasado son inusuales para mí?"
- "¿Algún cliente cambió su patrón de pago recientemente?"
- "¿Tengo facturas duplicadas en el sistema?"
- "Identifica proveedores con RIF mal formateado"
- "¿Por qué subió [categoría de gasto] este mes?"

### "Optimízame" — proactive savings/leakage
- "¿Qué suscripciones pago que tal vez no estoy usando?"
- "Clientes que pagan tarde consistentemente — ¿debería pedirles depósito?"
- "Gastos recurrentes que aumentaron de precio sin avisar"

**Per-role tailoring** (post-v1, but plan for it):
- Controller sees full gallery
- AP clerk sees Workflow + OCR + Compliance prompts
- CFO sees Visibility + Insights + Optimízame

## Tool surface (internal, MCP-formatted)

The chatbot talks to an LLM. The LLM has access to Odoo via a set of tools defined in MCP format (server-internal, not exposed). MCP-format keeps us future-proofed if we ever want to flip the server to be externally addressable.

### Read tools (auto-callable)
- `query_transactions` — filter by date, account, counterparty, amount, status
- `get_open_invoices` — AR or AP aging, by counterparty or branch
- `get_counterparties` — search `res.partner`
- `get_pnl` — P&L for a period, optionally by analytic
- `get_balance_sheet` — BS at a date
- `get_bank_balances` — balance per `account.journal` (bank type)
- `get_journal_entries` — filter by journal, date, posted/draft
- `get_chart_of_accounts` — CoA
- `get_report` — libro mayor, libro de compras, libro de ventas, declaración IVA, retenciones

### Write tools (require user confirmation in chat)
- `create_vendor_bill`
- `create_customer_invoice`
- `create_counterparty`
- `categorize_transaction`
- `reconcile`
- `post_entry`
- `add_attachment`

### Document tools (drive the OCR wow)
- `parse_invoice_pdf` → extracted fields
- `parse_bank_statement` → list of transactions
- `parse_invoice_image` (WhatsApp photo → fields)

### Per-tool design rules
- **Idempotent writes** — re-issuing the same call doesn't duplicate
- **Return rich context for chaining** — read results carry IDs so the AI can drill in on the next turn
- **Spanish-language tool/parameter descriptions** — guides AI to respond in Spanish naturally
- **Server-side per-tool rate limits** — don't let an AI loop hammer the customer's Odoo

## Architecture (initial)

```
┌──────────────────────────────────────────────────────────────────┐
│  Tesote AI Chat — web UI                                         │
│  - Chat surface                                                  │
│  - Use-case gallery + suggested-prompt chips                     │
│  - File upload (PDF / image / Excel)                             │
│  - Write-confirmation modals                                     │
│  - Audit log tab                                                 │
└─────────────────────────────┬────────────────────────────────────┘
                              │ WebSocket / HTTP streaming
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  AI Chat backend                                                 │
│  - Conversation state                                            │
│  - LLM orchestration (Claude API — see open questions)           │
│  - MCP-format tool layer                                         │
│  - Audit logger                                                  │
│  - Rate limiting + cost guards per customer                      │
│  - Odoo credential vault                                         │
└─────────────────────────────┬────────────────────────────────────┘
                              │ XML-RPC / JSON-RPC over HTTPS
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  Customer's Odoo (SaaS, .sh, or self-hosted)                     │
└──────────────────────────────────────────────────────────────────┘
```

**Stack choices to lock in fast** (open questions below):
- LLM: Claude API (Sonnet 4.6 default, Opus where needed) — likely default
- Backend: new service, modern stack (TBD: Node/TS, Python, or Go — pick what's fastest for the team)
- Frontend: standalone Next.js or similar (NOT bolted onto existing Tesote frontend if that introduces friction)
- DB: new Postgres, separate from Treasury
- Odoo client: rewrite minimal client in chosen stack, or call out to a tiny service that wraps existing odoo_client.rb — whichever ships faster
- Auth: standalone, or thin SSO bridge with existing Tesote login (decide based on speed)

**Explicit "we will not" items** (to keep velocity):
- We will NOT depend on Treasury Rails for the AI chat
- We will NOT depend on Connect for AI chat
- We will NOT block on the existing Tesote frontend codebase
- We will NOT share schema with any existing DB
- We will NOT wait for the Cockpit/Connector eng team's roadmap

## v1 scope

Tighten further. Ship a chat that does a *small* number of things, *brilliantly*.

**v1 = chat + 5 reads + 2 writes + 1 OCR + gallery.**

- Tesote login + Odoo connection flow (paste URL/creds, validate)
- Chat UI with streaming responses, suggested-prompt chips, file upload
- 5 read tools: `get_pnl`, `query_transactions`, `get_open_invoices`, `get_counterparties`, `get_bank_balances`
- 2 write tools (with confirmation): `create_counterparty`, `create_vendor_bill`
- 1 OCR tool: `parse_invoice_pdf` → handoff to `create_vendor_bill`
- Use-case gallery (the 5 categories above, ~5 prompts each)
- Audit log tab
- Spanish-language by default
- Single LLM (Claude API)

**What we deliberately cut from v1:**
- Reconciliation (complex, save for v2)
- Compliance reports (libro mayor / libro de compras — high-value but complex formatting; v2)
- Anomaly detection (needs more data + tuning; v2)
- Multi-user / per-seat audit attribution (v2)
- Custom AI surface tuning per role (v2)
- Voice / WhatsApp input (later)

**Pilot client**: same shortlist as the Cockpit — Casagri or El Dorado. Whoever signs first and has appetite for "give us a week, we'll plug into your Odoo and you'll be chatting with your books."

**Pre-v1 spike (this week)**: end-to-end thinnest-possible slice. One read tool (`get_pnl`), one write tool (`create_counterparty`), in a stub chat UI, against a test Odoo. ~3–5 days. Validates the ergonomics — confirmation UX, response latency, AI behavior with Spanish prompts and VE accounting context — before we commit to v1 scope.

## Open questions

1. **LLM choice** — Claude API default (Sonnet 4.6, Opus 4.7 where needed). Alternatives: OpenAI, Gemini, open-weights via a hosted provider. **Lean Claude unless there's a compelling reason; revisit if cost or latency hurts.**
2. **New codebase vs. bolt-on** — green-field Node/Python repo, or new module inside existing Treasury Rails? Green-field is faster but costs us future integration with the Cockpit. **Lean green-field for v1; design API surfaces so the Cockpit can call them later if useful.**
3. **Where does the chat live in Tesote's app?** — top-level "Asistente" tab, or floating widget on every page, or both? Top-level tab is simpler for v1.
4. **Authentication & credential vault** — store customer Odoo creds securely. New vault, or piggyback on existing Tesote secrets infra? Compliance bar matters.
5. **Cost guards** — AI agents can loop. Per-customer monthly cap on LLM tokens + Odoo API calls; circuit breakers when exceeded. What's the right default tier?
6. **Confirmation UX for writes** — modal in chat? Inline button? Free-text "confirmar"? Affects safety and friction. Need to prototype.
7. **Conversation memory** — does the AI remember prior conversations? Per-session only, or persistent? Persistent is more useful but more complex (privacy, summarization). Probably per-session for v1.
8. **OCR provider** — Claude's native vision, or a dedicated OCR (AWS Textract, Google Doc AI, Mathpix)? Claude vision is probably good enough for typed invoices; specialized OCR for handwritten / photo-quality.
9. **Pricing tier** — flat per-Odoo-instance/month? With usage caps? Trial length?
10. **Free trial design** — 14-day full access, or limited tools? Limits force conversion conversation early, full access shows the value.
11. **Spanish vs. multilingual** — VE/LATAM Spanish is default. Do we ship English on day 1, or strictly Spanish?
12. **Sequencing vs. the Cockpit** — same eng leadership? Are these built in parallel by different sub-teams, or sequenced?

## What we figure out next (this week)

1. **Run the 3–5 day spike** — thinnest end-to-end slice. Validates ergonomics and unblocks v1 scope decisions. Owner TBD.
2. **Lock LLM + stack choices** — Claude API, language for backend, frontend approach. Dan should be in the room.
3. **Talk to 3 pilot candidates** — show them the use-case gallery as a static mock, watch their faces. Casagri, El Dorado, one other. We're optimizing for "I want this now" reactions.
4. **Draft the chat UI in Figma** — 3 screens: empty state with gallery, mid-conversation, write-confirmation. Words don't sell this; the screenshot does.
5. **Decide v1 launch criteria** — what does "ready to charge" look like? Define before we build.
6. **Sequence with Cockpit** — alignment meeting with Dan + product. Both products, one ICP, decide priority.

---

## Cross-links

- [[odoo-prd]] — Cockpit PRD (in `../accounting-automation/`), parallel product targeting same ICP
- [[../../ai/]] — broader AI-native surface thinking (when populated)
- [[../../../strategy/product-strategy-execution-plan]] — where does this fit in 2026 plan?
- Treasury repo: `app/clients/erp_client/odoo_client.rb` — reference for Odoo API patterns, not a dependency
