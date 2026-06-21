---
title: Tesote AI — feature requests & improvements
tags: [product, ai, chat, ux]
updated: 2026-05-20
status: draft
---

# Tesote AI — feature requests & improvements

Running punch list of UX / capability gaps in the Tesote AI chat surface. Separate from [[tesote-workspace-mcp-feedback]] — that doc tracks **backend MCP / tool gaps**; this one tracks **chat product UX**.

Add new items at the bottom. Promote to a `/tesote-plan` run once a cluster is ready for eng.

## Linear

- [PRO-154](https://linear.app/tesote/issue/PRO-154) — Bug: table mixes Bs + USD without disambiguation (B1)
- [PRO-155](https://linear.app/tesote/issue/PRO-155) — Improvement: composer textarea auto-expand (#1)
- [PRO-156](https://linear.app/tesote/issue/PRO-156) — Feature: OCR fallback for scanned PDFs (#2)

## Open — features

### 1. Auto-expand chat input for long messages
The composer textarea should grow vertically with content (up to ~⅓ viewport) instead of staying fixed and scrolling internally. Editing/reviewing a long paste is painful today.

- **Treasury code:** `app/javascript/components/ai/App.tsx:1599-1652` (composer JSX, `rows={3}`) + `app/javascript/components/ai/styles.css:2701-2717` (`max-height: 120px`, `resize: none`). Source: design dossier exploration 2026-05-20.
- **Why it matters:** common workflow is dumping a chunk of context (email, transcript, table) into chat. Tiny box = friction = users break the message up or skip the tool.
- **Reference behavior:** Claude/ChatGPT/Linear input fields — grow to ~⅓ viewport, then scroll inside.

### 2. OCR for scanned PDFs (and images-of-documents)
**Already shipped:** images go to Claude vision via `app/javascript/components/ai/lib/imageVision.ts` (resize to 1568px, base64, content block). Text-extractable PDFs land via `app/services/ai/upload_extractor.rb:101-108`.
**Gap:** scanned/image-only PDFs return `extract_failed: pdf_no_text_layer` (`upload_extractor.rb:103`). Comment at `upload_extractor.rb:25` explicitly: *"would be the image-OCR fallback path in a later pass."* Note: `Contracts::PdfTextExtractor:59-61` returns `method: :vision` on text failure — vision fallback may be wired at the contract layer but isn't reaching the user-facing path. **Ask Dan to confirm scope** before sizing.

- **Why it matters:** half of the killer Tesote workflows start with a document the user is staring at — invoice photos that come in as scanned PDFs, payment confirmations photographed off a phone, bank screenshots saved as PDF. Without scan-OCR the AI tells the customer "no puedo leer este archivo" on artifacts that are central to the job.

## Open — bugs

### B1. Working-file `table` displays mixed-currency amounts in a single ambiguous column
The AI builds `table` working files with a single `total` (and `pendiente`) column typed as `currency` but **no currency code per row**. When the source data spans Bs and USD, the rows are silently mixed and the numbers become meaningless to read (5,445,475 sitting next to 870 with no way to tell which is which).

- **Surface:** Tesote AI (`/ai`) — right-pane working-file `table` (rendered by `TableRenderer.tsx`).
- **Concrete repro:** working file `facturas-pendientes-mayo2026.json` (server_id `f3e99811-01fe-4a72-bcf7-786885df2381`, updated `2026-05-20T15:28:23-04:00`, 36 rows). Columns emitted: `numero, tipo, cliente_proveedor, fecha, vencimiento, total, pendiente`. No `currency` / `moneda` column. Rows include both `FACTC/2026/00140` at 5,445,475 (clearly Bs) and `FACTC/2026/00135` at 870 (clearly USD) in the same `total` column.
- **Likely root cause:** **not** a code regression — no `/ai` commits today; last touch was 2026-05-19 18:21 UTC (`81366090b`). The system-prompt currency rule (`app/services/ai/system_prompts.rb`) covers *aggregation* ("never mix currencies in a single total") but not **display** — nothing tells the model "if rows can span currencies, the table MUST carry a `currency` column or split into per-currency tables." Same gap shows up in `TableRenderer.tsx` — `type: "currency"` columns have no per-row currency context to format against. The aggregation guard in `mcp_result_serializer.rb:304-316` only fires on `dump_to` + `template: sum/avg`, not on the model emitting a plain `table`.
- **Required behavior:** invoices/transactions in Bs render as Bs; in USD render as USD. Two acceptable shapes — (a) add a `moneda` column to the `table` schema for mixed datasets, or (b) split into two tables (`facturas-pendientes-bs.json`, `facturas-pendientes-usd.json`). Probably (a) for compact, (b) for clarity — Dan to call.
- **Scope tag:** prompt fix (system_prompts.rb) + renderer hardening (TableRenderer.tsx refuses to format `type: currency` rows without a currency anchor) + possibly MCP serializer change to always include `currency` when the source row has one.

## Promoted / shipped

_(empty)_

## Related

- [[tesote-workspace-mcp-feedback]] — backend tool gaps
- [[../automations/erp-ai/odoo-mcp]] — chat surface strategy
- [[pitch-agents-plus-ai]] — customer-facing framing
