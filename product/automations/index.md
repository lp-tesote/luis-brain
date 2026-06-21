# Automations

ERP integrations + AI surfaces on top of ERPs. The layer that turns financial system data into operational outputs (journal entries, reports, AI-driven workflows).

## Framing (2026-05-12): the command center

The 2026-05-12 architectural lock-in reframes this whole bucket. **Tesote is the command center; Odoo (and the other ERPs we'll support) is the execution layer.** The user works in Tesote; Odoo runs underneath, invisible.

Cockpit framing (in [[accounting-automation/]]) was directionally right — this bucket graduates into the full command center expression. See [[../business/counterparties/system-of-record]] for the spine + architectural decision.

The three sub-buckets remain valid; they're now the three flavors of how Tesote commands Odoo:

## Sub-buckets

- [[accounting-automation/]] — **Accounting Automation**. The structured workflow product: queues, inboxes, recon engines, mapping config, productized close. Cockpit PRD + the new inbound-inbox surface. **This is the daily operating UI** for the command center.
- [[erp-ai/]] — **ERP AI**. AI chat / agent surfaces in the Tesote UI on top of customer ERPs. Tesote-branded chatbot for Odoo. The conversational lane into the command center.
- [[erp-workspace-ai/]] — **ERP + Workspace AI**. Multi-surface bridges (email, Drive, Slack, WhatsApp) that feed documents and signals INTO the command center's inbound inbox.

## Scope (working definition)

- **ERP integrations** — Odoo, SAP, Dynamics 365, Profit (push journal entries, pull masters, auto-generate workflows)
- **Reports** — scheduled / on-demand outputs to clients
- **AI surfaces** — chat + agent + workspace integrations that sit on top of the ERP
- **Inbound document inbox** — the "first landing place" for anything external with finance metadata (see [[accounting-automation/inbound-inbox]])
- **Reconciliation + writeback** — bank txn → Tesote → Odoo journal
