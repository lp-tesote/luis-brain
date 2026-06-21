# Tesote Connect — PTCK Working Folder

Materials for PTCK's review of **Tesote Connect** (bank-data extraction; the live core product on top of which Automations and Payments are built).

## Contents

- [`flujograma-connect-ptck.md`](flujograma-connect-ptck.md) — **the version sent to PTCK**. Cleaned up, no internal references, all `[VERIFICAR]` markers replaced. Pushed to Notion as a child of "Tesote — Asuntos Legales — Abril 2026" (https://www.notion.so/3571ee04eee181b19d5eff6e552cd5fa).
- [`flujograma-connect.md`](flujograma-connect.md) — the **original / internal master version** with the full self-analysis, regulatory triggers, gaps, and notes-to-self. **Do not send to PTCK.** Useful when revisiting the underlying analysis or when porting structure to the next flujograma (Automations, Payments).
- [`flujograma-connect-verificar.csv`](flujograma-connect-verificar.csv) — tracking sheet of the `[VERIFICAR]` questions and answers (some pending Daniel via Linear LEG-2).
- `msa-template.docx` — MSA template that Tesote signs with all clients. Contracting party: TST SERVICIOS Y CONSULTORIA, C.A. (VE entity). Source for the cláusula references in §5 of the flujograma.

## Status

- **2026-05-05**: PTCK-bound flujograma pushed to Notion. Some technical details (encryption schemes, infra location, RTO/RPO, log retention period) marked as "en confirmación interna" — pending Daniel's response on Linear [LEG-2](https://linear.app/tesote/issue/LEG-2) before re-syncing the Notion version.

## Sister deliverables PTCK still expects

- T&C of the platform (referenced by MSA cláusula 14, kept separately).
- Plaid Developer Agreement.
- Flujogramas for Automations and Payments (siblings to this folder, in preparation).

## Sources

- Kickoff recap that triggered this folder: [`../ptck-kickoff-2026-04-29.md`](../ptck-kickoff-2026-04-29.md).
- Master brief: [`../../tesote-legal-affairs-april-2026.md`](../../tesote-legal-affairs-april-2026.md), section P0.2 (the Connect-relevant slice).
