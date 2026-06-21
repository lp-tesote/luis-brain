# Accounting Automation

The structured workflow product on top of the ERP — the deep finance-operations layer. Where AI plus humans actually run the close, post entries, reconcile banks, and own the operational ledger. Distinguished from [[../erp-ai/]] (chatbot/agent surface) and [[../erp-workspace-ai/]] (multi-surface bridges) by being a **UI-driven productized workflow product**.

## Framing (2026-05-12): command center, not just cockpit

The cockpit framing in [[odoo-prd]] was directionally right and remains the v1 anchor. The 2026-05-12 architectural lock-in expanded it: the cockpit IS the command center, with the inbound document inbox as the new general-purpose surface that subsumes Cap #2 (AP automation) and extends it to contracts, retention vouchers, receipts, expense reports, sales orders.

Spine of the architecture lives in [[../../business/counterparties/system-of-record]].

## Active drafts

- [[odoo-prd]] — Cockpit on Odoo. Ramp-style cockpit, productized 30-day onboarding, four v1 capabilities (AI transaction coding, AP automation, bank recon, counterparty management). Still the foundational PRD; the command center framing builds on it.
- [[inbound-inbox]] — **Inbound document inbox**. The "first landing place" surface for anything external with finance metadata. Generalizes Cap #2 (AP automation) to cover contracts, retention vouchers, receipts. Net-new from 2026-05-12.
- [[prototypes/]] — interactive HTML prototypes covering the Cockpit's onboarding stages and v1 capabilities (preflight, mapping, banks, rules, queue, AP inbox, dashboard, recon).

## Re-bucketing the Cockpit caps under the command center

The four v1 caps in [[odoo-prd]] map cleanly onto the command center loops:

- **Cap #1 — AI transaction coding** → the cobros/pagos side of reconciliation. Inputs from [[../../connect]] bank data.
- **Cap #2 — AP automation** → graduates into [[inbound-inbox]] (broader scope: invoices, contracts, receipts, retentions).
- **Cap #3 — Bank reconciliation** → the reconciliation engine in the outbound loop ([[../../business/cobros/outbound-invoice-routing]]).
- **Cap #5 — Counterparty management** → owned by [[../../business/counterparties/]].

## Working principles for this bucket

- Tesote-native operational ledger (counterparties, categories, comments, audit trail) — Odoo holds the GL, Tesote owns workflow
- Tesote = command center; Odoo = execution layer. End user never opens Odoo.
- Productized 30-day onboarding SLA — CS drives, customer decides, product executes
- Hard dependency on Tesote Connect (clean bank data is the moat)
- AP/AR clerks, controllers, CFOs are the daily users
- Assisted → Automated maturity curve for every capability
- Single-step approval for v1 (multi-step is v2 if needed)

## Future

- Same cockpit/command-center pattern for SAP, Dynamics 365, Profit (post-Odoo v1)
- Post-v1 capabilities: accruals/close, intelligent reporting, multi-step approval workflows
