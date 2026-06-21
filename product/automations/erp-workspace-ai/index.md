# ERP + Workspace AI

AI that spans the ERP and the customer's workspace tools — email, Drive, Slack, WhatsApp, calendar. Multi-surface workflows where the AI bridges where work *happens* (workspace) with where it *gets recorded* (ERP).

## Why this is its own bucket

The [[../erp-ai/]] bucket is AI that operates *inside* the ERP context — read books, write entries, run reports. That's a self-contained surface.

This bucket is AI that operates *across surfaces* — workspace input → ERP action, or ERP signal → workspace notification. The integration story and the UX story are different.

## Example flows (sketches, not committed)

- **Email → AP entry** — vendor sends an invoice by email; AI reads from Gmail, parses, drafts a vendor bill in Odoo, posts a notification to Slack for approval
- **WhatsApp → expense capture** — employee snaps a receipt photo, sends to a Tesote WhatsApp number; AI OCRs and books it
- **Drive → batch import** — controller drops a folder of PDFs in a Drive folder; AI processes them all into draft entries
- **ERP → calendar** — upcoming AR due dates synced to controller's calendar with collection-call prompts
- **Slack → query** — CFO asks `@tesote what's my cash position?` in a Slack channel; bot responds with the answer pulled from Odoo

## Status

Empty for now. Placeholder for product thinking when the [[../erp-ai/]] base product is shipping and we start expanding surface area.
