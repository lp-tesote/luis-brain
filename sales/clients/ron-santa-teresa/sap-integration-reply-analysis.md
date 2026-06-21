---
title: Santa Teresa — SAP integration reply, analysis
tags: [sales, client, ron-santa-teresa, sap, scoping]
updated: 2026-05-06
status: draft
---

# Santa Teresa — SAP integration reply, analysis

What they sent back to our 5-question email, and what it means for the proposal.

Source material:
- Their reply text (5 paragraphs, one per question).
- Sample bank statement: `MERCANTIL BS CARST 7215902.xlsx` — 7-column custom Excel, 117 rows.
- Bot manual: `1.- BPD - Extractos bancarios UV Firmado.pdf` (signed BPD).
- Flujograma del proceso estándar (PNG): user → email → BTP bot → FF.67 in SAP.

---

## TL;DR

The deal is movable. Scope just got **simpler, not harder**. We can send a proposal.

- The format is **not** MT940 / BAI2 / CAMT. It's a custom Excel they already process. We produce that Excel — done.
- They explicitly want minimum disruption to their existing bot. We oblige; v1 is "Tesote sends the email instead of the user." That's the whole inbound integration.
- They want **no Z-developments**. That matches our preference.
- They have BTP and a real SAP partner ecosystem (Abside + Integratec) — they have the technical muscle on their side.

**Critical framing for the Abside meeting:** what we're proposing here is **v1**, not the destination. If we just produce the Excel they consume today, they're getting bank-statement plumbing — not the actual Tesote value. None of our enrichment (categorization, counterparty resolution, RIF matching, GL pre-mapping) reaches SAP. The roadmap conversation has to start at the meeting, not after we ship.

**Important consequence:** in pure v1 (email-with-Excel) **there is no actual integration with SAP**. We don't read from it, we don't write to it, we don't connect to it. We send an email. That means the entire integration-architecture conversation in their reply (OData on BTP, SCC vs VPN, no-Z preference) is **irrelevant to v1** — those are v1.5 / v2 questions. We need to be honest about that internally and in the meeting, otherwise we'll over-scope and over-quote v1 against questions it doesn't have to answer.

---

## Their answers, decoded

### 1. Partner SAP / Basis

- **Abside** = SAP partner (functional/implementation).
- **Integratec** = Basis support contract.
- Hosting: **GCP, hosted directly by SAP**.

→ Almost certainly **RISE with SAP** (private cloud), even though the brief says ECC 6.0 EHP 7 on HANA. Worth one confirmation in our reply. Doesn't change our work, but if they're already on S/4HANA Cloud Private Edition, the Fiori-equivalent of FF.67 becomes the relevant transaction.

### 2. Carga del extracto hoy

- Transaction used: **FF.67** (manual bank statement entry).
- Automation: **Bot on SAP BTP** that reformats Excel and posts the statement.
- Channel: triggered by **email-with-attachment**.

→ They are **not running EBS / FEBAN / BCM**. The bot is doing screen-scrape-style entry against FF.67. Brittle but working. Not our problem to fix in v1.

→ The Excel sample (`MERCANTIL BS CARST 7215902.xlsx`) shows the schema:

| Column | Meaning |
|---|---|
| `Op.` | Transaction-type code (MND/MNC/MPE = Mov. Nacional Débito / Crédito / Pagos Electrónicos) |
| `Fe.valor` | Value date, `DD.MM.YYYY` |
| `Importe` | Signed amount (negative = debit), `,` decimal separator |
| `Asignacion` | Reference (numeric, ~11 digits) |
| `Texto position` | Description, 40-char truncated, uppercase |
| `Saldo final` | Closing balance — only on row 1 |

We can produce that exact layout from any of our supported banks. No SAP-side dev needed for the inbound leg.

### 3. Datos maestros

- Available via BTP: **OData**, **RFC-BAPI**, **HANA read**.
- Strong preference: **"lo ideal es no crear desarrollos Z."**

→ Our recommendation: **OData exposed via BTP**. Native to their stack, no Z-code, async-friendly, easy to scope/version. RFC/BAPI as fallback for the few BAPIs that don't have an OData equivalent. Avoid direct HANA — tighter network and auth surface for marginal latency gains we don't need.

### 4. Canal de entrega

- Their explicit ask: **don't redesign the bot — Tesote sends the email instead of the user.**

→ v1 channel: **SMTP** to their bot inbox, with the Excel attached. Same UX as today, just no human downloading from the bank portal.

→ Future cleanup (not v1): replace email-trigger with SFTP / BTP storage drop. Park this.

### 5. Acceso de red

- Open to **VPN** or **SAP Cloud Connector**.

→ Our recommendation: **SAP Cloud Connector**. Canonical pattern for SAP-hosted environments, cleanest path to expose OData services from BTP to us, and Integratec already knows it. VPN works but heavier and requires more admin on their side.

---

## Coverage check vs the 6 must-haves

The long-form questionnaire flagged six minimum points to close the proposal: A1, A2, C10, C11, C12, D18.

| # | Question | Status |
|---|---|---|
| A1 | Hospedaje | ✅ GCP, hosted by SAP |
| A2 | Partner Basis | ✅ Abside + Integratec |
| C10 | Proceso actual de carga | ✅ FF.67 via BTP bot |
| C11 | Formato + sample file | ✅ Excel custom, sample sent |
| C12 | EBS configurado | ⚠️ Not directly answered. FF.67 implies no EBS. Worth one line of confirmation. |
| D18 | Destino de entrega | ✅ Email to bot inbox |

5 of 6 cleanly answered. C12 is a soft gap — we can either ask in our reply, or just proceed assuming "no EBS, we deliver Excel" since that's what the evidence shows.

---

## What each version actually needs

| | **v1 — email plumbing** | **v1.5 — enriched delivery** | **v2 — direct integration** |
|---|---|---|---|
| What Tesote does | Sends email + Excel to their bot inbox | Same, but the Excel includes Tesote-side enrichment (categories, counterparty, RIF, GL hint) | Posts directly into SAP FI; FF.67 retired |
| SAP-side change | None. Bot stays as-is. | Bot may need light tweaks to use the extra columns (or ignore them) | EBS configured, BAPI/OData consumers built; bot replaced |
| Reads from SAP? | **No** | **Yes** — master data (GL plan, customer/vendor with RIF, house bank IDs) | Yes — same as v1.5 plus posting feedback |
| Writes to SAP? | No (the bot writes via FF.67) | No (still via the bot) | **Yes** — direct FI postings |
| Network needs | SMTP destination | SAP Cloud Connector or equivalent for OData read | SCC for read + write |
| OData / BAPI / no-Z conversation | **Not relevant** | **Relevant — read side** | **Relevant — read + write side** |
| Their effort | Configure email rule | Light: confirm OData scopes, provision SCC | Heavier: configure EBS, define posting rules, retire bot |
| What Tesote demonstrates | "We replaced one human step." | "Your bank statements arrive already categorized and RIF-matched." | "Bank → ledger, no humans, no FF.67." |

The honest truth: **v1 alone is thin.** It saves them a download-and-forward step. It doesn't put any Tesote value into SAP. The interesting integration work — and the conversations in their reply — start at v1.5.

## Recommended response stack (what we send back)

| Topic | v1 only | v1.5+ |
|---|---|---|
| Inbound bank statement channel | Tesote → SMTP → bot inbox. Same Excel schema as today. No bot rework. | Same channel, enriched payload (extra columns: category, counterparty, RIF, suggested GL). |
| Master data | Not needed for v1. | OData on BTP. RFC/BAPI as fallback. No Z-code. |
| Network | SMTP only. | SAP Cloud Connector. |
| Posting | Stays via FF.67 + bot. | Stays via FF.67 + bot until v2. |
| Confirmation needed | File-naming convention; bot inbox address; exact column spec. | + Exact SAP edition (RISE / S4HCP vs ECC 6.0 EHP 7), EBS status, BTP service ownership (Abside or Integratec). |
| Roadmap framing | Explicit "this is v1" — surface enrichment gap as the v1.5 conversation. | Explicit "this is the value step" — categorization/counterparty/RIF/GL hint reaching SAP. |
| Next step | 30-min joint call with **Abside** before signing. Abside's blessing accelerates everything; we use the meeting to scope v1.5 and v2 explicitly. |

---

## Strategic notes

1. **Inheriting brittleness, not buying it.** Their email→bot→FF.67 stack is fragile, but it's working and they've protected it. We should not be the team that breaks it. v1 is conservative on purpose.
2. **v1 is plumbing — the value pitch is v2.** If we only produce today's Excel, every Tesote-side automation stays stuck on our side: transaction categorization, counterparty resolution, RIF matching, GL account pre-mapping, supplier/customer reconciliation. The bot will keep typing raw rows into FF.67 and SAP will keep needing humans to fix categorization downstream. The expansion conversation is: enrich what we deliver (counterparty + GL on every row), then graduate from FF.67-via-Excel to direct FI postings via BAPI/OData. **Plant this flag at the Abside meeting**, not after go-live.
3. **Architecture v2 has two axes, not one.**
   - **Channel axis:** email → SFTP/BTP storage → direct API into SAP.
   - **Enrichment axis:** raw rows → categorized rows → fully mapped FI postings.
   The channel cleanup is housekeeping. The enrichment is the actual upsell — that's where Tesote becomes irreplaceable, not just a cheaper bank-portal scraper.
4. **Abside is leverage.** They built the bot, they know the gaps, they'll tell the client whether our proposal is sane. Get them on a call before sending anything formal — and they're also the right audience for the v2 vision (they'd be the implementation partner on the SAP side).
5. **Format flexibility is our edge here.** They were probably bracing to hear "you need to switch to MT940." We say "we'll match what you have today." That's a small commercial win — and it's also the trojan horse: once we're delivering files reliably, the conversation shifts to what *else* we put in the file.

---

## Open questions to confirm before / during the technical call

- Exact SAP edition (ECC vs S/4HANA Cloud Private Edition).
- EBS configured or not — even if FF.67 implies not.
- Number of house banks in scope and which company codes.
- Cadence expected (real-time, intra-day batches, end-of-day).
- File-naming convention the bot expects in the email subject / attachment name.
- Master data scope: which company codes, vendor/customer master with RIF, GL accounts of interest.
- Who provisions the BTP OData services and the SCC tunnel — Abside or Integratec.
