---
title: Bank Nomenclature Scoring — Purolomo Bank Set
tags: [purolomo, sales, banks, cobranzas, kyc-onboarding]
updated: 2026-04-28
status: draft
notion: https://www.notion.so/3501ee04eee181958c5fdaaf6ab7eca3
---

> **Notion mirror:** [Implementation › Bank Nomenclature Scoring — Purolomo Bank Set](https://www.notion.so/3501ee04eee181958c5fdaaf6ab7eca3) (pushed 2026-04-28). Edit there if changes need to be visible to the team; mirror back here when promoted.

# Bank Nomenclature Scoring — Purolomo Bank Set

**What this is.** The cuadro Luis committed to send Daniela in the 2026-04-22 meeting. For each of Purolomo's 20 banks, what payer-identification fields the bank's transaction descriptions actually carry, split by direction (credit / debit), so Crédito y Cobranza can see at a glance which banks they can reconcile by RIF and which they can't.

**Audience.** Internal first (Luis + product/data), then Daniela once we agree on the framing.

**Replaces** Majo's existing Notion DB (`Playbook - Descripciones de Bancos`), which scored each bank as a single record without splitting by direction. Credit and debit nomenclature are different on most banks; that's the load-bearing distinction this version fixes.

## Methodology

- Source: `tesote_transactions` for all Tesote workspaces, last 90 days, VES only, non-discarded.
- Out-of-scope rows excluded by classifier: card POS settlements, bank fees/comisiones/retenciones, internal own-account transfers, reversals.
- KEEP-only sample = real third-party cobros and outflows.
- Auto-scored fields: `RIF`, `Número de Cuenta` (regex over description).
- Visual-scored fields: `Razón Social`, `Concepto`, `Código de Transacción` (eyeball top patterns from 100-row random sample per bank × direction).
- Buckets: **COMPLETO** (≥90% of rows have it) / **PARCIAL** (30–90% or truncated) / **NO** (<30%).

## Major caveat — initial aggregate scoring was misleading for B2B

The original scoring averaged all Tesote customers (B2B + B2C + individuals) and bucketed by count. Manual validation against a single B2B workspace (VDT, 555 VES rows, 6 banks) shows aggregate scoring **dramatically understated** B2B coverage on credits:

| Bank | Aggregate (old) | VDT B2B (actual) |
|---|---|---|
| BBVA CR | 56% PARCIAL | 73% — pattern COMPLETO across rows |
| Banco Activo CR | 8% NO | **95% — COMPLETO** |
| Banco Plaza CR | 24% NO | **85% — COMPLETO** |
| BDV CR | 73% PARCIAL | **100% — COMPLETO** |
| Banesco CR | 37% PARCIAL | **87% — COMPLETO** |
| BNC CR | 2% NO | COMPLETO (LBTR rail — manually validated) |

Why aggregate failed: B2C/individual workspaces dominate count with Pago Móvil traffic that ships zero payer ID. B2B receivables traffic (`CR.I/REC <bank> <RIF>`, `TRF <bank> <RIF> <name>`, `N/C CRED I<bank><RIF>`, `PAGO RECIBIDO OTROS BANCOS <bank> <RIF>`, `TRF.MB <bank> <RIF> <name>`, etc.) is a smaller fraction of count but carries the actual B2B cobros — and ships full RIF. **Purolomo's mix will look like VDT's, not the aggregate.**

**Practical implication:** the per-bank rows below are now updated for the 6 banks visible in VDT. Banks NOT in that CSV (Mercantil, Bancaribe, BNC, R4, Bancrecer, Banplus, Banco Exterior, BFC, Tesoro, Bangente, Bancamiga, Venezolano de Crédito) still carry the aggregate score and should be re-validated against a B2B sample before being treated as final.

## Other caveats

- **Razón Social often appears in `nombre_contraparte` field even when truncated in description.** Tesote parses counterparty names into a separate field — BBVA 24%, BDV 63%, Banesco 28% have full names there. So Razón Social availability is higher than desc-only scoring shows.
- **Banco del Tesoro classifier leak.** `LQ ELE` (~26% of credits) and `COM/LIQ/ELE` (~14% of debits) are card POS settlements not yet caught by the v3 CARD_LIQ regex. Tesoro's KEEP figures and RIF/Cuenta % are slightly understated. Easy fix.
- **Aggregate by count masks important sub-types** (the methodology issue surfaced by BNC). Q8 in the SQL file gives a sub-type breakdown (count + value + RIF rate) for any bank.
- **Debits not validated.** The VDT CSV is credits-only. Debit scoring still relies on aggregate Q3-K and may be similarly understated for B2B outgoing payments. Re-validate when a B2B debit sample is available.

## Scoring matrix

Direction codes: **CR** = Crédito (cobro entrante) / **DB** = Débito (egreso).

Status legend: **B2B-validated** = checked against VDT B2B workspace data; **needs B2B validation** = still on aggregate score, re-validate before treating as final.

| # | Bank (Purolomo term) | Dir | RIF | Razón Social | Concepto | Cuenta | Cód Tx | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | 100% BANCO | CR | NO³ | NO | NO | NO | NO | low sample |
|   | | DB | NO | NO | NO | NO | NO | needs B2B validation |
| 2 | MI BANCO (R4) | CR | NO | NO | NO | NO | NO | needs B2B validation |
|   | | DB | NO | NO | NO | NO | NO | needs B2B validation |
| 3 | **ACTIVO** | CR | **COMPLETO** | NO⁴ | NO | NO | PARCIAL | **B2B-validated** |
|   | | DB | PARCIAL | NO | NO | NO | PARCIAL | needs B2B validation |
| 4 | BANCARIBE | CR | NO | NO | NO | NO | NO | needs B2B validation |
|   | | DB | NO | NO | NO | NO | NO | needs B2B validation |
| 5 | BANCRECER | CR | NO | NO | NO | NO | NO | needs B2B validation |
|   | | DB | PARCIAL | NO | NO | NO | NO | needs B2B validation |
| 6 | **BANESCO** | CR | **COMPLETO** | **PARCIAL**⁵ | NO | NO | COMPLETO | **B2B-validated** |
|   | | DB | PARCIAL | NO | NO | NO | NO | needs B2B validation |
| 7 | BANPLUS | CR | NO | NO | NO | NO | NO | needs B2B validation |
|   | | DB | NO | NO | NO | NO | NO | needs B2B validation |
| 8 | BICENTENARIO (BDT) | — | — | — | — | — | — | no Tesote data |
| 9 | **BNC** | CR | **COMPLETO**² | **COMPLETO**² | **COMPLETO** | NO | **COMPLETO** | manually validated |
|   | | DB | **PARCIAL (87%)** | PARCIAL | **COMPLETO** | **COMPLETO** | **COMPLETO** | aggregate-validated |
| 10 | EXTERIOR | CR | PARCIAL | NO | NO | NO | COMPLETO | needs B2B validation |
|   | | DB | NO | NO | NO | NO | COMPLETO | needs B2B validation |
| 11 | FONDO COMÚN | CR | PARCIAL | NO | NO | NO | PARCIAL | needs B2B validation |
|   | | DB | NO | NO | NO | NO | NO | needs B2B validation |
| 12 | MERCANTIL | CR | NO | NO | NO | NO | PARCIAL | needs B2B validation |
|   | | DB | NO | NO | NO | NO | PARCIAL | needs B2B validation |
| 13 | **PLAZA** | CR | **COMPLETO** | **PARCIAL**⁵ | NO | NO | COMPLETO | **B2B-validated** |
|   | | DB | PARCIAL | NO | NO | NO | COMPLETO | needs B2B validation |
| 14 | **PROVINCIAL (BBVA)** | CR | **COMPLETO** | **PARCIAL**⁵ | NO | PARCIAL | COMPLETO | **B2B-validated** |
|   | | DB | PARCIAL | NO | NO | NO | COMPLETO | needs B2B validation |
| 15 | SOFITASA | — | — | — | — | — | — | no Tesote data |
| 16 | TESORO | CR | PARCIAL | NO | NO | NO | PARCIAL | needs B2B validation |
|   | | DB | PARCIAL | PARCIAL | NO | NO | PARCIAL | needs B2B validation |
| 17 | **VENEZUELA (BDV)** | CR | **COMPLETO** | **PARCIAL**⁵ | NO | NO | COMPLETO | **B2B-validated** |
|   | | DB | **PARCIAL (71%)** | NO | NO | NO | COMPLETO | needs B2B validation |
| 18 | VENEZOLANO DE CRÉDITO | CR | NO | NO | NO | NO | NO | needs B2B validation |
|   | | DB | NO | NO | NO | NO | NO | needs B2B validation |
| 19 | BANCAMIGA | CR | NO | NO | NO | NO | NO | needs B2B validation |
|   | | DB | NO | NO | NO | NO | NO | needs B2B validation |
| 20 | N58 BANCO DIGITAL | — | — | — | — | — | — | no Tesote data |

² *BNC CREDIT carries full payer info — RIF, razón social, concept, código — on its **inter-bank LBTR rail** (e.g. `TRANSFERENCIA RECIBIDA DE :BANCO PROVINCIAL POR CUENTA DE :J000154937 LABORATORIOS LA SAN E C A REFERENCIA : 22150645 - Abono Via BCV - LBTR LBTRAB - Codigo 262`). High-value B2B transfers. Pago Móvil rows on the same bank carry zero payer ID. Aggregate Q3-K showed 2% RIF because Pago Móvil dominates by count; LBTR carries most of the $ value. Manually validated.*

³ *100% Banco CREDIT: only 4 VES rows in the VDT B2B sample, all "Pago de Intereses". Insufficient sample. Re-score when more data available.*

⁴ *Banco Activo CREDIT: format is `N/C CRED I<bank-code><RIF>` — RIF embedded but no name field. Razón Social must come from `nombre_contraparte` enrichment if Tesote populates it.*

⁵ *Razón Social PARCIAL: name appears in description but truncated to 13–17 chars (e.g. `LABORATORIOS LA S` for "Laboratorios La Sante C.A."). Full name typically available in `nombre_contraparte` enrichment field.*

## Three banks we cannot score from Tesote data

These appear in Purolomo's bank list but have zero rows in our 90-day production window — Tesote either has no live integration or no client uses them in that window.

| Bank | Notes |
|---|---|
| BICENTENARIO (BDT, Banco de los Trabajadores) | No rows. Need samples from Purolomo's BDT extracts directly to score. |
| SOFITASA | Only visible as relayed entries inside `Cuenta Manual` descriptions ("TRANSFERENCIA RECIBIDA DEL BANCO SOFITASA POR ORDEN DE..."). No first-class integration. |
| N58 BANCO DIGITAL | Likely Banco Digital de los Trabajadores. In Majo's existing Notion playbook but zero rows in our 90-day window. |

This is its own line item to bring to Daniela: **Tesote cannot deliver these three to Purolomo today** without integration work or sample data from her side.

## Findings to bring to Daniela

### 1. For the 6 B2B-validated banks, RIF coverage on cobros is high

In the VDT B2B workspace sample, all five banks with meaningful volume ship RIF on the dominant credit pattern:

| Bank | VDT B2B credits, RIF coverage | Pattern |
|---|---:|---|
| BDV | 100% | `PAGO RECIBIDO OTROS BANCOS <bank> <RIF>` / `PAGO RECIBIDO BDV <RIF> <name>` / `PAGO A PROVEEDORES <RIF> <name>` |
| Banco Activo | 95% | `N/C CRED I<bank><RIF>` (RIF only, no name in desc) |
| Banesco | 87% | `TRF.MB <bank> <RIF> <name truncated>` / `TRF CR INM <bank> <RIF> <name>` |
| Banco Plaza | 85% | `TRF <BANK> <RIF> <name truncated>` (PROVIN, BNC, BANESC, VZLA, etc.) |
| BBVA | 73% | `CR.I/REC <bank> <RIF>` / `TRA<RIF>` / `TR/REC-AV <bank> <name>` |
| BNC (manual) | COMPLETO on LBTR | `TRANSFERENCIA RECIBIDA DE :<BANCO X> POR CUENTA DE :<RIF> <name> REFERENCIA : <ref> - Abono Via BCV - LBTR LBTRAB - Codigo <code>` |

This is the opposite of what the aggregate scoring suggested. **The 11 other banks (Mercantil, Bancaribe, R4, Banplus, Bancrecer, Banco Exterior, BFC, Tesoro, Bangente, Bancamiga, Venezolano) still need B2B validation** before any conclusions can be drawn — the aggregate scores I have for them may be similarly understated.

### 2. Razón Social: present, but often truncated to 13–17 chars in the description

Banks like Banesco (`LABORATORIOS LA S`), BDV (`LABORATORIOS LA SA`), BBVA (`IMPORTADORA V`), Banco Plaza (`IMPORTAD`) truncate counterparty names to a short fixed-width field in the description. Full name typically available in Tesote's enriched `nombre_contraparte` field — VDT data shows ~24-63% population on that field. **The TXT format Tesote sends to Purolomo should pull from `nombre_contraparte` when present, not just parse the description.**

### 3. The BNC outlier — gold standard on both directions, just different shape

BNC's debit feed has `TELF.: <phone> CED.: <RIF> CTA.: <20-digit-account> <free-text-concept> - <CIOPPS code>` on every row. 87% RIF + 100% Cuenta + COMPLETO on Concepto and Código de Transacción.

BNC's credit feed carries full payer info on the inter-bank LBTR rail (high-value B2B transfers). Pago Móvil rows on the same bank carry zero payer ID, but those aren't the cobros that matter for Purolomo. See footnote ².

### 4. The structured-code-only banks — partial wins for non-RIF rows

Even on rows where RIF is missing, several banks ship clean transaction codes on every row: Banco Exterior (4-digit prefix), BBVA (TRA/DR OB/CR.I/REC), Banco Plaza (TDY routing codes + Nota de Crédito/Débito), BDV (PAGOMOVIL/PAGO RECIBIDO/PAGO A PROVEEDORES tx-type), BNC (CIPOTR/CIOCCS/P2COTR).

For these banks, the **Código de Transacción** column gives Daniela's team a way to classify by *type* (was this a pago móvil cobro? a transferencia? a pago a proveedores?) even when the payer ID is missing on the minority rows.

## Implications for the TXT format

For the 6 B2B-validated banks, Tesote's TXT can carry RIF on most cobros (75-100% coverage). For the 11 not-yet-validated banks, hold off on conclusions until B2B sample data confirms or rejects the aggregate scores.

## Next moves

- [ ] **Validate the 11 remaining banks against B2B sample data** before sending anything to Daniela. Mercantil and Bancaribe are the most important — they were scored as "blind" on aggregate but might look very different in B2B context.
- [ ] Per-Purolomo-workspace scoring: re-run Q3-K / Q4-K with `AND w.id = '<purolomo_workspace_id>'` to get their specific numbers vs aggregate. This is the cleanest fix.
- [ ] Verify `nombre_contraparte` enrichment behavior — when does Tesote populate it vs leave empty? VDT data shows it varies by bank (24-63%). Worth understanding so the TXT format can lean on it.
- [ ] Decide what to tell Daniela about the 3 unscorable banks (BDT, Sofitasa, N58). Options: ask her to send raw extracts, or scope an integration if any of them is volumetrically meaningful.
- [ ] Fix the Banco del Tesoro classifier leak (`LQ ELE`, `COM/LIQ/ELE`).

## Source

- SQL: `data/purolomo_bank_nomenclature_samples.sql` (Q1–Q7, plus Q2-K, Q3-K, Q4-K filtered to KEEP-only)
- Q2-K sample CSV (v3 classifier, 2026-04-27): in Downloads
- Q3-K + Q4-K result CSVs (2026-04-28): in Downloads
