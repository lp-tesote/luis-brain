# ERP AI

AI chat / agent surfaces on top of customer ERPs. The customer talks to AI; AI reads from and writes to their ERP. Tesote-branded chatbot in Tesote's UI.

## Active drafts

- [[odoo-mcp]] — Tesote AI for Odoo (v1 strategy). Chatbot in Tesote UI (only surface), MCP under the hood, zero Tesote-core dependencies, ships fast. Same ICP as the Cockpit, different ergonomic surface.
- [[flagship-workflows]] — 6 agentic workflows that turn the chatbot from Q&A into delegation. The "sell tomorrow" demo stack: Cobranzas Autopilot, Cierre Express, Conciliación Relámpago, Bandeja Mágica, Pre-Auditoría SENIAT, Brief para el CEO.
- [[odoo-ai-recon-and-fixes-2026-05]] — Mariel-session bugs (Avanti + Cenco Zotti), Dan's PR #7154 response w/ mining findings, and the foundational reconciliation walkthrough Conciliación Relámpago has to encode. Blocker on Mariel's collection-flow taxonomy writeup.
- [[collection-flow-taxonomy]] — Scaffold of every collection flow (USD-pure / USD-dual / Bs-indexed × pay-USD / pay-Bs × same-day / deferred, plus partial / overpay / credit note / refund / retentions). For each: rate source, currency_id derivation, AI pre-post confirmations + proposed `apply_invoice` / `apply_payment` / `apply_credit_note` signatures. Awaiting Mariel sign-off to unblock Dan's gated-actions PR.

## Working principles for this bucket

- Tesote UI is the only surface (no external MCP, no Claude desktop dependency) until the market matures
- Zero coupling to Tesote core (Connect/Pagos/Cobros not in critical path)
- Guided experience is part of the product — use-case galleries, suggested prompts, wow-moment curation
- LATAM-native by default (Spanish, VE/LATAM compliance, local tax codes)
- Read-first, write-with-confirmation

## Future

- Same product pattern for SAP, Dynamics 365, Profit, etc. — pick the next ERP after Odoo validation
- Voice / WhatsApp input as additional surfaces (post-v1)
