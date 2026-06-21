---
title: Tesote US Odoo — Setup Thinking
tags: [finance, odoo, us-entity]
updated: 2026-05-12
status: draft
---

# Tesote US Odoo — Setup Thinking

Initial scoping conversation, 2026-05-12. Captures the fork-in-the-road decisions before a real setup plan.

## Premise

- US entity: TESOTE TECHNOLOGIES INC. (Delaware C-corp). See [[reference_tesote_legal_entities]].
- Already running Odoo for VE + DR
- Building MCPs against Odoo — multi-jurisdiction MCP layer is in scope regardless
- Self-implemented dogfood, no partner
- Architecture context: [[tesote-command-center]] — Tesote = SoR on top of per-jurisdiction Odoo

## Big fork: separate instance vs multi-company

**Picked: separate Odoo instance for US.**

Reasoning:
- Command center already assumes per-jurisdiction Odoo
- US has zero shared vendors/customers/banking with VE
- Multi-company saves setup pain now but forces a painful split later (fundraising DD wants clean US books)
- Matches the SoR/MCP design — each jurisdiction is its own posted-facts store

## Hosting: Odoo.sh vs self-hosted

**Recommendation: Odoo.sh** for the dogfood instance.

- Self-hosted gives more MCP latitude, but US-Inc dogfood is about leverage *now*, not infra projects
- Odoo.sh: books running in days, handles upgrades
- MCPs work fine against Odoo.sh API (XML-RPC/REST exposed — MCP layer doesn't care about underlying host)
- Revisit self-hosted only if we hit a wall on customization the API can't cover

## Load-bearing pieces

| Piece | Notes |
|---|---|
| **CoA + l10n_us module** | Clean Delaware C-corp baseline. No sales tax setup needed unless we have nexus outside DE (probably none). |
| **Bank feed** | Tesote Inc's US bank (Mercury? SVB? — confirm). Odoo has Plaid-based feeds; CSV fallback until MCP wires it. |
| **Stripe → Odoo** | If US-Inc invoices through Stripe, this is the load-bearing revenue integration. |
| **Payroll / contractors** | Heaviest piece if W-2 employees exist. Near-zero if all 1099/Deel. |
| **Migration cutover** | If QuickBooks (or anything) holds current US books, pick a clean date — fiscal-year boundary ideal, month-end otherwise. |

## Open questions before scoping a plan

1. **What's the source of truth for US-Inc books today?** — QuickBooks, spreadsheet, nothing? Determines greenfield vs migration.
2. **W-2 employees on US-Inc, or contractors only?** — Difference between "weekend setup" and "needs a payroll plan."
3. **Cutover date** — depends on #1 + fiscal calendar
4. **Bank confirmation** — which US bank(s) hold Tesote Inc accounts today
5. **Stripe linkage** — is US-Inc the merchant of record on Stripe, or VE?

## Next step when we come back

Answer the 5 open questions → draft a setup runbook (likely lands in `product/automations/` once it becomes execution-ready, mirroring VE/DR Odoo work).
