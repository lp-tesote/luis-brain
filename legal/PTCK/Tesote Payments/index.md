# Tesote Payments — PTCK Working Folder

Materials for PTCK's review of **Tesote Payments** — the cobros + pagos product on top of BNC's API (Crédito Inmediato y Débito Inmediato vía rieles BCV). Highest stakes / most regulatory ambiguity of the three products.

## Contents

- [`flujograma-payments-ptck.md`](flujograma-payments-ptck.md) — first draft of the PTCK-bound flujograma. Covers the three transactional flows: Collect/DI-OTP (live B2C, biz blocked), Collect/Domiciliación (in QA con BNC), Send/CI (API available, not yet productized). Mirrors the structure of the Connect flujograma — Spanish, audience PTCK Fase 1.

## Sister deliverables PTCK still expects

- BNC API documentation / specs (Tesote will request from BNC tech team).
- Eventual partnership agreement Tesote ↔ BNC if/when formalized.
- Términos al Pagador (payer-facing terms) — does not exist yet; flagged as a gap in §5 of the flujograma.
- Updated Anexo III "Tesote Cobros" of the MSA with Payments-specific terms.

## Status

- **2026-05-05**: First draft of the flujograma. Pending internal review with engineering / product before sending to PTCK. Not yet pushed to Notion.

## Notes for the brain author (Luis)

- This flujograma is **less mature than Connect's** because the product itself is less mature: B2C live, B2B blocked, Send not productized. The doc explicitly says so per flow rather than overclaiming. Acceptable for PTCK at this stage — they need accurate scope, not aspirational scope.
- Distinct from Connect: Payments adds **third-party data** (the pagador) to the regulatory analysis. That's a meaningfully new vector PTCK has not yet seen in the Connect docs.
- The "alianza vs partner-tecnológico" question (PTCK's flag in the kickoff) is most acute here — formalizing BNC partnership commercially could pull Tesote into fintech classification.

## Sources

- Kickoff recap: [`../ptck-kickoff-2026-04-29.md`](../ptck-kickoff-2026-04-29.md).
- Master brief: [`../tesote-legal-affairs-april-2026.md`](../tesote-legal-affairs-april-2026.md), section P0.1 (the Payments slice).
- Connect flujograma (sister doc): [`../Tesote Connect/flujograma-connect-ptck.md`](../Tesote%20Connect/flujograma-connect-ptck.md).
- Operational status: [`../../../drafts/bnc-ach-status.md`](../../../drafts/bnc-ach-status.md), [`../../../strategy/product-strategy-execution-plan.md`](../../../strategy/product-strategy-execution-plan.md).
- BNC QA matrix (interbank validation): [`../../../product/tesote-pay/rails/bnc/juridico-interbank-qa-matrix.md`](../../../product/tesote-pay/rails/bnc/juridico-interbank-qa-matrix.md).
