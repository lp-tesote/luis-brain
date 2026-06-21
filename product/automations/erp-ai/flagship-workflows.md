---
title: Tesote AI for Odoo — flagship workflows (the "sell tomorrow" pitch)
tags: [product, automations, odoo, ai, mcp, agents, demo, sales]
updated: 2026-05-12
status: draft
---

# Tesote AI for Odoo — Flagship Workflows

> Companion to [[odoo-mcp]]. That doc lays out the chatbot strategy. This one answers: **if we had to sell it tomorrow, what do we show?** Not prompts. **Workflows.** Agentic, multi-step, visibly impressive, useful Monday morning.

## The shift: chatbot → agent

The v1 gallery in [[odoo-mcp]] is mostly **first-order interactions** — one prompt, one tool call, one answer. That's table stakes in 2026. ChatGPT does that. We won't differentiate there.

The "wow" lives one layer up: **the user assigns work, the agent executes a sequence, the user supervises and approves.** Not "ask the books a question" — **"give the books an instruction."**

We're not selling Q&A. We're selling **leverage**:

| Chatbot framing | Agent framing |
|---|---|
| "Cuánto vendí ayer?" | "Cobra esta semana" |
| One tool call | 5–15 tool calls, chained |
| The user drives | The agent drives, the user approves |
| Answer in 3 seconds | Outcome in 60–90 seconds |
| Feels like search | Feels like delegation |
| Demo: "look, it knows" | Demo: "look, it DID it" |

The chat surface stays the same. What changes is **what we curate behind each suggested prompt.** The prompt fires an agent, not a tool.

## What makes a workflow mindblowing

Five tests. A workflow earns "flagship" status only if it hits all five:

1. **Compresses time visibly** — work that takes hours/days, done in under 90 seconds *with the agent's progress visible on screen* (not a black box). The visible tick-tick-tick of "matched 12, matched 13, matched 14" is the magic.
2. **Touches a real pain weekly or monthly** — cierre, cobranzas, conciliación, SENIAT, CEO ad-hoc requests. If it's not a recurring pain, it's a parlor trick.
3. **Produces an artifact** — a sent message, a posted entry, a rendered PDF, a queued action. Not just an answer on screen. **Customers screenshot artifacts; they don't screenshot answers.**
4. **VE-native specificity** — retenciones, RIF/SENIAT, libros, bolívar/USD, BCV rate, LATAM tone. ChatGPT can't fake this. This is our moat in the demo.
5. **Confirmation, not autonomy** — every write step has a "approve / edit / skip" gate. Demo viewers feel control, not fear. The agent doing 14 things autonomously is scary; the agent proposing 14 things and the human one-tapping approve is **delight**.

## The 6 flagship workflows (ranked for demo impact)

Each one below is structured as: **pain → prompt → choreography → wow moment → tool surface → demo-readiness**.

Ranking criteria: emotional resonance with the buyer + visible AI work + demo feasibility within ~weeks.

---

### 1. Cobranzas Autopilot — *"Cobra esta semana"*

**Pain.** AR chasing is the most draining, personal, recurring task in a LATAM finance team. Drafting WhatsApp messages, picking the right tone for each client, tracking who replied, following up. Hours per week. Emotional labor.

**Prompt.** `Cobra esta semana` (or chip: "Generar cobranzas de la semana")

**Choreography (visible on screen, ~60 seconds).**
1. *"Revisando cuentas por cobrar…"* — pulls aged AR from Odoo
2. *"Encontré 23 clientes con saldo vencido. Segmentando…"*
3. Shows a queue grouped by overdue band (1–15 días / 16–45 / 45+) and payment history (friend / regular / problemático)
4. *"Redactando mensajes personalizados…"* — drafts a WhatsApp message *per client* in Spanish, tone-matched (warm for friend-clients, firm for chronic late-payers)
5. Renders the queue: client name, monto vencido, days overdue, the draft message, a button per row: **Enviar / Editar / Saltar / Cambiar tono**
6. User one-taps through 23 approvals (Luis: "this is the moment they gasp")
7. *"Mensajes enviados. Te aviso si responden."*
8. Behind the scenes: schedules 3-day follow-up if no reply

**The wow.** The agent **wrote 23 personalized Spanish WhatsApp messages in your voice in 30 seconds.** Each message references the actual invoice number, the actual due date, and the actual relationship history. The controller looks at message #11 and goes "yes, that's exactly how I'd word it for José."

**Tool surface needed.**
- `get_open_invoices(status=overdue, aging_buckets)` — read
- `get_payment_history(counterparty_id)` — read, for tone calibration
- `get_counterparty_contact(counterparty_id)` — phone, preferred channel
- `draft_collection_message(invoice_ids, tone)` — LLM-generated
- `send_whatsapp_message(phone, body)` — write, needs WhatsApp BSP integration *(or v1: copy-to-clipboard and let user paste — still demos beautifully)*
- `schedule_followup(invoice_id, days)` — write to internal DB

**Demo-readiness.**
- v1 demo this month: AR pull + drafting + queue with **"Copiar mensaje"** button (manual paste into WhatsApp). Still wins the room.
- v2 (Q3): WhatsApp BSP integration → one-tap send + reply tracking.

**Why this is #1.** Universal pain. Emotional resonance. The "AI typed in my voice" moment is unforgettable.

---

### 2. Cierre Express — *"Ciérrame mayo"*

**Pain.** Month-end close is the worst week of every month. Hunting for unposted entries, chasing missing invoices, reconciling stragglers, then producing the close package. 5 days of cumulative pain across the team.

**Prompt.** `Ciérrame mayo` (or chip: "Cerrar el mes")

**Choreography (~90 seconds visible + ~5 min of approvals).**
1. *"Iniciando cierre de mayo. Corriendo 18 verificaciones…"*
2. Progress checklist appears, items tick green/yellow/red in real time:
   - ✓ Todas las transacciones bancarias del mes importadas
   - ⚠ 4 transacciones sin categorizar
   - ⚠ 2 facturas en estado borrador
   - ✓ Retenciones IVA aplicadas
   - ⚠ 1 RIF mal formateado en proveedor "Distribuidora ABC"
   - ⚠ Conciliación bancaria: 6 movimientos sin match
   - ✓ Libro de compras consistente con facturas registradas
   - … (continues)
3. *"Encontré 8 cosas para resolver. Te las paso una por una."*
4. Each yellow/red item has a **proposed fix** + **Aprobar / Editar / Saltar** buttons:
   - "Categorizo la transacción de $1,200 del 18-may como 'Gasolina'?" → tap Aprobar
   - "Cierro la factura #INV-0241, ya fue pagada el 22-may?" → tap Aprobar
4. User flies through approvals in 3 minutes
5. *"Cierre ejecutado. Generando paquete de cierre…"*
6. Produces a **PDF close-package**: P&L del mes, Balance General, flujo de caja, comparativo vs abril, comparativo vs mayo año anterior, comentario ejecutivo
7. Bonus: *"¿Lo envío al CEO?"* — drafts email/WhatsApp + attaches PDF

**The wow.** What used to be 5 days of tribal-knowledge hell becomes 10 minutes of supervised AI execution. The close package itself is **prettier than what the team produces manually**.

**Tool surface needed.**
- A `close_month_diagnostic(period)` agent that orchestrates ~20 reads
- Each individual write tool (categorize_transaction, close_invoice, fix_partner_rif, reconcile, post_entry) wrapped in approval UX
- `generate_close_package(period)` — produces PDF (templated, plus AI-written commentary)

**Demo-readiness.**
- v1 demo: diagnostic + propose-fix UI, execute 2–3 fixes live, render PDF (with placeholders OK). ~3 weeks of build.
- v2: full execution of all fix categories.

**Why this is #2.** Maximum emotional payoff (everyone hates close). Less visceral than cobranzas-in-your-voice, but the relief is profound. Also: **CFOs make the buying decision and this is the most CFO-y workflow.**

---

### 3. Conciliación Relámpago — *"Concílialo todo"*

**Pain.** Bank reconciliation is the most repetitive grind in finance. Match line by line against invoices, journal entries, payments. Hours per bank statement, multiplied by banks (we hold 5+ accounts).

**Prompt.** Drag/upload bank statement PDF or paste lines → `Concílialo todo` (or upload triggers it automatically)

**Choreography (~30 seconds visible).**
1. *"Procesando estado de cuenta de Banesco mayo…"*
2. *"Detecté 84 movimientos."*
3. Progress bar of matches appears, ticking up in real time:
   - "Matched 12 / 84 — invoice payments"
   - "Matched 27 / 84"
   - "Matched 53 / 84"
   - "Matched 78 / 84 — pattern-matched (gasolina, telefonía, alquiler)"
4. *"6 sin match. Necesito tu ayuda con estos."*
5. Renders 6 unmatched txns, each with **3 AI-ranked candidate matches** + a "crear nueva entrada" option, one-tap to pick
6. *"Conciliación completa. Postulando 84 asientos…"*
7. *"Listo. ¿Generar reporte de conciliación?"*

**The wow.** The progress counter is hypnotic. Going from "84 transactions, please match each one" to "84 matched, click confirm" in 30 seconds — viewers literally lean in.

**Tool surface needed.**
- `parse_bank_statement(file)` — already in v1 scope of [[odoo-mcp]]
- `match_transactions_to_entries(txn_list)` — ML-assisted matching
- `pattern_classify(unmatched_txns)` — known-counterparty heuristics
- `reconcile(matches)` — batch write
- `generate_reconciliation_report(period, journal)` — PDF artifact

**Demo-readiness.**
- v1 demo: feasible in 2–3 weeks. We have bank statement parsers already (Connect). The matching agent is the new piece.
- Big asset: **we already have bank rails work in Connect** — reuse the parsers, don't reinvent.

**Why this is #3.** Most viscerally demonstrable (the progress bar). Less emotional than cobranzas/cierre, more obvious as productivity. Great "third slot" in a demo after the wow + the relief.

---

### 4. Bandeja Mágica — *Your inbox closes itself*

**Pain.** Vendor invoices arrive by email. Manual download, manual upload, manual entry. Multiple times a day, often missed, sometimes lost in the inbox until a payment is overdue.

**Setup.** One-time Gmail OAuth connect (5 seconds). Done.

**Daily ritual (passive, but the demo is the **morning open**).**
1. Adriana opens Tesote in the morning. The Asistente tab has a badge: **"8 facturas nuevas en tu bandeja."**
2. Click into it. The agent has already:
   - Detected 8 emails from known/likely vendors with PDF attachments
   - Parsed each PDF
   - Matched to existing vendor records (or proposes creating new)
   - Computed retentions
   - Drafted the vendor bill
3. Each row shows: vendor, monto, vencimiento, RIF, retenciones, link to source email, **Aprobar / Editar / Rechazar**
4. Adriana taps Aprobar 7 times, edits one, rejects a spam-looking one — done in 90 seconds
5. *"7 facturas creadas en Odoo. 1 archivada. Te aviso cuando llegue la próxima."*

**The wow.** The agent **proactively found work you didn't know you had**. This shifts the customer's mental model from "I use Tesote when I need something" to "Tesote works while I sleep." That's the upgrade.

**Tool surface needed.**
- Gmail OAuth + a label-watcher (or polling) — *new infra*
- `parse_invoice_pdf` — already v1
- `match_or_create_vendor(extracted_data)` — new
- `compute_retentions(vendor, line_items)` — VE-specific, valuable, defensible
- `create_vendor_bill(draft)` — v1 write tool, batched

**Demo-readiness.**
- v1 demo: feasible in 3–4 weeks. Gmail OAuth + watcher is the long pole.
- Alt for the **literal "sell tomorrow" demo**: pre-stage one Gmail inbox with 8 invoices, demo live. **Don't fake it — actually wire one inbox.** Costs a day. Pays for itself the first call.

**Why this is #4.** Strategic differentiator (no chatbot does this), but lower viscerality in a one-shot demo than the top 3. Becomes #1 in *second meetings* and trials, because the daily-arrival ritual is what creates the habit.

---

### 5. Pre-Auditoría SENIAT — *"¿Estoy lista para declarar?"*

**Pain.** Tax declaration anxiety. *Did we miss something? Will SENIAT fine us? Did the retentions match the invoices? Are the libros consistent?* The week before declaración IVA is dread.

**Prompt.** `¿Estoy lista para declarar IVA del período?` (chip: "Pre-auditoría SENIAT")

**Choreography (~45 seconds visible).**
1. *"Corriendo 32 verificaciones SENIAT del período abril-mayo…"*
2. Checklist with categorized verdicts:
   - ✓ Libro de compras consistente con facturas (47 facturas, $234,500)
   - ✓ Libro de ventas consistente con notas fiscales emitidas
   - ✓ Retenciones IVA aplicadas a 12 de 12 proveedores especiales
   - ⚠ 1 RIF inválido: "Distribuidora ABC" — RIF `J-12345-X` no pasa validación
   - ⚠ Cruce libros vs declaración: diferencia de $84 en IVA débito (línea 23)
   - ✓ Comprobantes de retención emitidos: 12 / 12
   - … (continues 32 checks)
3. Final verdict banner: **"AMARILLO — 2 problemas para resolver antes de declarar"**
4. Each problem has a **proposed fix** + a **why this matters** explainer
5. User resolves issues one-tap
6. Verdict turns **VERDE — Lista para declarar.**
7. *"Generando libros y borrador de declaración…"*
8. Renders: libro de compras (formato SENIAT), libro de ventas, borrador de planilla, comprobantes de retención

**The wow.** *Anxiety → certainty in 90 seconds*, with audit trail. The CFO/controller emotionally feels the relief. The artifacts are exactly what SENIAT accepts.

**Tool surface needed.**
- `seniat_audit_run(period)` — orchestrator over ~30 internal checks
- `validate_rif(rif)` — local checksum validation (online SENIAT lookup is v2)
- `cross_check_libros_vs_declaracion(period)` — reconciliation engine, VE-specific
- `generate_libro_compras(period, format=seniat)` — already v2 of [[odoo-mcp]]
- `generate_libro_ventas(period)`
- `generate_declaracion_iva_draft(period)`

**Demo-readiness.**
- v1 demo: 4–6 weeks. The 30+ checks are real engineering, not vibes. But the value is so high it's worth it.
- Demo shortcut for **right-now sales**: run the diagnostic with 5 checks instead of 30, show the framework. The auditor logic is the moat anyway.

**Why this is #5.** Lower demo-readiness than top 4, but it's the **single most defensible workflow against ChatGPT/Claude alone.** No general LLM has SENIAT knowledge baked. This is where we earn permanent moat.

---

### 6. Brief para el CEO — *"Hazme un brief de mayo para el CEO"*

**Pain.** The CEO asks "how are we doing?" The controller spends 3 hours pulling numbers, writing a memo, polishing for the audience. Recurring weekly or monthly.

**Prompt.** `Hazme un brief para el CEO de mayo` (chip: "Generar brief ejecutivo")

**Choreography (~30 seconds visible).**
1. *"Recopilando indicadores del mes…"* (P&L, BS, cash, AR, AP)
2. *"Comparando con plan, mes anterior, y mismo mes del año pasado…"*
3. *"Identificando las 3 variaciones más notables…"*
4. *"Redactando…"*
5. Renders a 1-page PDF in clean executive Spanish:
   - **Headline**: "Ventas crecieron 14% vs abril, principalmente por sucursal Las Mercedes"
   - **Cifras clave** (4 numbers, big)
   - **3 highlights con comentario** (not just numbers, actual prose explaining the why)
   - **3 watchpoints** (cosas que el CEO debería preguntar)
   - **Mini-charts** (revenue trend, AR aging, cash trajectory)
6. *"¿Lo envío a Luis?"* — pre-fills email draft

**The wow.** **Actual writing**, not a dashboard. The CEO gets a memo that reads like a Bloomberg analyst wrote it. The controller looks brilliant. The CEO looks at their phone and goes "wait, this is from finance?"

**Tool surface needed.**
- `get_executive_metrics(period)` — composite read
- `compare_periods(period, baseline, prior_year)` — variance engine
- `identify_top_variances(comparison_data, k=3)` — ranks by significance
- `generate_brief_pdf(data, narrative_style)` — LLM writes prose, template renders
- `email_draft(recipient, subject, body, attachment)` — handoff

**Demo-readiness.**
- v1 demo: ~2 weeks. Mostly LLM prompt engineering + a PDF template. Low engineering risk, high demo polish.
- Could literally ship this **next week** as a standalone "AI Brief" feature even before the chat surface is full.

**Why this is #6.** Highest demo-polish-per-engineering-hour. Slot it as a closer — the customer's last impression is **"AI made me look better to my boss."** That's a sticky emotional anchor.

---

## Demo flow for prospect calls

**The "sell tomorrow" demo** is not all 6. Pick 3. Suggested sequence (15 minutes total, in this order):

1. **Cobranzas Autopilot** (5 min) — opens with maximum viscerality. The "in my voice" moment.
2. **Conciliación Relámpago** (3 min) — fast follow-up with maximum work-compression visibility. The progress-bar moment.
3. **Brief para el CEO** (4 min) — closes with the polish moment + the "make me look good" emotional anchor.

Save **Cierre Express** for the *second* meeting (it's a CFO conversation, deeper). Save **Bandeja Mágica** for the trial (it's about *daily ritual*, not first impression). Save **Pre-Auditoría SENIAT** for the procurement/finance-director call (it's the moat-defining one).

**Demo principle: don't show the gallery.** The gallery is for self-serve activation. In a live sales demo, you don't show a buffet — you serve plated dishes. Pick the 3, show them like they're flagship features, not options.

**Demo principle: live data, not test data.** If at all possible, demo against a sample customer's anonymized Odoo (with their permission), not synthetic data. The prospect knows the difference instantly.

**Demo principle: do the WhatsApp/email actually-send if you can.** Don't mock the send button. Wire one demo account. The actual "ping" of the WhatsApp message arriving on the demo phone is worth more than 10 slides.

## Sequencing for engineering

Order to build (assuming we want to be selling within ~6 weeks):

| Week | Build | Demo readiness |
|---|---|---|
| 1–2 | **Chat shell + Brief para el CEO** (prose generation + PDF) | Demo-ready: 1 workflow |
| 2–3 | **Cobranzas Autopilot** (read AR + draft + queue UX + clipboard copy) | Demo-ready: 2 workflows |
| 3–4 | **Conciliación Relámpago** (parser + matcher + reconcile write) | Demo-ready: 3 workflows |
| 4–6 | **Cierre Express** (diagnostic agent + fix-approval UX + close package) | Demo-ready: 4 workflows |
| 6–10 | **Bandeja Mágica** (Gmail integration + inbox watcher) | Habit-forming feature live |
| 10–14 | **Pre-Auditoría SENIAT** (30+ checks + libro generation) | Moat-defining feature live |

Top 3 = 3–4 weeks to demo-ready. **That's the "sell tomorrow" target.** Everything after that is depth.

## What this requires from us (Luis + Dan + product)

**This week:**
1. **Decide: are we actually building this?** Or is this still in the strategy-debate phase? If yes, lock the eng owner and the team shape. Dan's call.
2. **Pick the 3 demo workflows** to commit to (recommend: Cobranzas, Conciliación, Brief). The full 6 is the *roadmap*; the demo-stack is what we charter immediately.
3. **Identify the demo Odoo** — sample customer (Casagri? El Dorado?) or our own Odoo with seeded data. Without a demo target, no demo.
4. **Naming + branding** — are these called "Cobranzas Autopilot" as features? Or just suggested prompts? My take: they become **named features in the Tesote AI surface**, with their own chip/card in the gallery. Naming builds salience.

**Next week:**
5. **Mock the demo flow in Figma** — 3 workflows × ~8 screens each = ~24 screens. Words don't sell this; the screen-by-screen tour does. **This is the single highest-leverage artifact for sales.**
6. **Prototype the Brief workflow end-to-end** (lowest eng risk, highest demo polish) as a proof point we can show next week even before chat is built.
7. **Talk to 3 prospects with the Figma mock** — Casagri, El Dorado, one other. Watch their faces on each workflow. Refine the order.

## Open questions

1. **Naming as features vs. prompts.** Are these "the Cobranzas Autopilot feature" (productized, billable, screenshot-able) or "a smart prompt suggestion"? I lean *feature*: it sells better, it's easier to roadmap, and it creates a SKU hierarchy if we ever want to upsell. Risk: more product surface to maintain.
2. **Pricing tied to flagships vs. flat.** Do flagship workflows have usage caps (e.g., 50 collections per month)? Tiered packages? Or does the entire AI surface get one flat per-Odoo-instance price? Flat is simpler for v1; tiered is more capturing-value at scale. Defer for now.
3. **Confirmation friction tuning.** For Cobranzas, every message needs approval — but 23 approvals is a lot. Should we allow "approve all of tone X" or "approve all overdue 1–15 días"? Test in demos.
4. **The "Mariel test."** Mariel is our dogfood design partner (per [[../../../strategy/product-strategy-execution-plan]] and [[../../business/counterparties/system-of-record]]). Run every flagship workflow past her before locking specs. If she doesn't go "I need this NOW," recalibrate.
5. **Cross-product gravity vs. zero-coupling rule.** [[odoo-mcp]] says zero Tesote-core coupling. But Cobranzas could pull Connect's WhatsApp send. Conciliación could use Connect's parsers. Where's the line? My current take: **the AI chat product stays independent, but flagship workflows can call Connect via API if available, and degrade gracefully if not.** That preserves ship-speed while not duplicating bank-rail work.

---

## Cross-links

- [[odoo-mcp]] — the v1 strategy + gallery this builds on
- [[../../business/counterparties/system-of-record]] — command-center framing this lives inside
- [[../accounting-automation/odoo-prd]] — Cockpit PRD (the sibling product surface)
- [[../../../strategy/product-strategy-execution-plan]] — where this fits in the 2026 plan
- [[../../ai/]] — broader AI-native surface thinking
