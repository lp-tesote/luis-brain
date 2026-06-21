---
title: Tesote Connect — KYC Onboarding Collection Spec
tags: [product, onboarding, kyc, tesote-connect]
updated: 2026-04-27
status: draft
---

# Tesote Connect — KYC Onboarding Collection Spec

Customer-facing onboarding flow for collecting the KYC information Tesote needs before activating a **Tesote Connect** customer. Operationalizes the design proposed in [[../legal/kyc-customer-collection-design]].

**Scope: Tesote Connect only.** Connect is a SaaS product — selling and operating it does not trigger regulated KYC obligations. The ask here is right-sized for a B2B SaaS vendor: validate the entity, identify the signatory, screen for sanctions/PEP. Anything beyond that is out of scope for this spec.

Payments-related KYC (BNC KYB discharge, source-of-funds for money movement, Payment Link individuals) is **explicitly out of scope** here and will be specced separately when Payments leaves the gated phase.

Audience: product + design + eng + internal legal (sign-off section at the end).

---

## Default assumption

A standard Tesote Connect customer is a **VE-incorporated B2B entity buying SaaS**. Default risk tier: **Bajo** (per counsel's risk matrix). The flow is calibrated for that case and progressively reveals fields only when triggered (foreign entity, opaque ownership, regulated industry).

---

## Principles

1. **Customer types core entity data; we validate silently** — the customer enters RIF, razón social, domicilio fiscal, activity, cédula, and signatory name themselves. Server-side, we cross-check against SENIAT/SAIME on submit and flag mismatches for manual review without surfacing the lookup to the customer. Auto-pull is reserved for things the customer can't reasonably type (sanctions/PEP screening).
2. **Identity entered once** — name/RIF/cédula collected once, reused everywhere.
3. **Single document upload at sign-up** — only the latest `acta de asamblea`. No print-sign-scan, no notarial Word docs, no bundled PDF packets.
4. **E-sign attestations** — checkboxes + typed signature in the flow itself.
5. **Conditional, not exhaustive** — foreign-entity, regulated-industry, and opaque-structure fields stay hidden until triggered.

---

## The flow — default (Bajo) tier

Target: **6 screens, < 6 minutes, one document upload (acta de asamblea).**

### Screen 1 — Identify the company

Customer types each of:

- RIF
- Razón social
- Domicilio fiscal
- Registered economic activity (free-text, short)

On submit the backend cross-checks all four against SENIAT silently. Mismatches flag the account for manual review but do not block sign-up. Conditional: if RIF format indicates non-VE, expand the flow with country-of-origin fields and route to manual review.

### Screen 2 — Identify the signatory

Customer types each of:

- Cédula
- Full name
- Role in company
- Work email
- Phone

On submit the backend cross-checks cédula → name against SAIME/CNE silently. Mismatches flag for review, do not block.

### Screen 3 — Beneficial owners (UBOs)

Question: **"¿Alguna persona física posee, directa o indirectamente, ≥25% de la empresa?"**

- **No** → continue (covers public companies, very distributed ownership, etc. — flagged for manual sanity-check by ops on submit).
- **Yes** → inline sub-table with one row per UBO, "agregar otro" to add more:
  - Nombre completo
  - Cédula o pasaporte
  - Nacionalidad
  - País de residencia
  - % de participación
  - ¿Es PEP (Persona Expuesta Políticamente)? (sí / no)

Threshold: **25%** (FATF default). All UBOs disclosed feed into the sanctions/PEP screen on submit alongside the signatory.

### Screen 4 — Acta de asamblea (latest)

Single document upload:

- File: most recent `acta de asamblea` (PDF, max ~10 MB).
- Purpose: evidences the current legal representative's authority to sign and the company's most recently registered ownership/governance state.
- Drag-and-drop or browse. Required.
- Backend stores in the expediente. If the upload is missing pages or unreadable, ops requests a re-upload via email (does not block immediate sign-up status — but Connect access stays "pending review" until accepted).

### Screen 5 — Attestations (e-sign)

Single screen, three checkboxes + signature:

- [ ] All information provided is true and complete; I will notify Tesote of material changes.
- [ ] No person listed (signatory or UBOs) is subject to sanctions (OFAC, UN, EU) or is a PEP, except as disclosed.
- [ ] The company is not engaged in activity prohibited by Venezuelan AML/CFT law.
- E-signature: typed name + timestamp + IP, captured for the expediente.

### Screen 6 — Confirm + submit

- Summary of everything entered (empresa, firmante, UBOs, acta filename, declaraciones).
- Submit → backend runs sanctions/PEP screen on the entity, the signatory, and every disclosed UBO.
- Outcome:
  - **Clean + Bajo + acta accepted** → activated, customer routed to Connect.
  - **Hit, anomaly, or acta rejected** → "We're reviewing — we'll be in touch within 1 business day." No tipping-off; manual review queue.

**That is the entire sign-up flow at default tier. One document uploaded (acta de asamblea). No bank or commercial references. No source-of-funds declaration. No utility-bill domicile proof. No ISLR. No financial statements.**

---

## Conditional escalations

Triggered only when warranted; otherwise hidden.

| Trigger                                                                | What gets added                                                                                |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Foreign entity                                                         | Country-of-origin fields, manual review, registro equivalent upload                            |
| Sanctions/PEP near-miss (signatory or any UBO)                         | Manual review by ops + counsel, additional ID verification                                     |
| Registered economic activity is in a regulated/banned list             | Manual review, possible decline                                                                |
| Acta de asamblea unreadable / missing pages                            | Email request for re-upload; account stays in "pending review" until acta accepted             |
| Customer answers "No UBO ≥25%" but company is not obviously diffuse    | Ops sanity-check; may request follow-up evidence                                               |

These are exception paths, not the default flow.

---

## What we collect vs. what we run silently

| Data point                          | Source                                  | Customer-facing?                            |
| ----------------------------------- | --------------------------------------- | ------------------------------------------- |
| RIF                                 | Customer input                          | **Typed**                                   |
| Razón social                        | Customer input                          | **Typed**                                   |
| Domicilio fiscal                    | Customer input                          | **Typed**                                   |
| Economic activity                   | Customer input                          | **Typed**                                   |
| Cédula                              | Customer input                          | **Typed**                                   |
| Signatory full name                 | Customer input                          | **Typed**                                   |
| Signatory role                      | Customer input                          | **Typed**                                   |
| Work email + phone                  | Customer input                          | **Typed**                                   |
| UBOs ≥25% (per UBO row)             | Customer input                          | **Typed** (sub-table, default ask)          |
| Acta de asamblea (latest)           | Customer file upload                    | **Uploaded** (PDF)                          |
| Attestations                        | Checkboxes + typed signature            | **Typed**                                   |
| SENIAT cross-check                  | Server-side (entity data → SENIAT)      | Silent — flags review on mismatch           |
| SAIME cross-check                   | Server-side (cédula → name → SAIME/CNE) | Silent — flags review on mismatch           |
| Sanctions/PEP screen                | Server-side (3rd-party: OFAC/UN/EU)     | Silent — flags review on hit                |

Goal: **1 document at sign-up (acta de asamblea); ~9 typed identity fields + UBO rows; all verification happens silently in the background.**

---

## Backend services this implies

- **SENIAT lookup service** — RIF → entity data
- **SAIME/CNE validation** — cédula → person data
- **Sanctions/PEP screening** — 3rd-party API on submit (OFAC, UN, EU lists)
- **Risk-scoring engine** — implements counsel's matrix server-side, default Bajo for SaaS
- **Expediente service** — stores the customer record + e-signed attestations with retention timer
- **Refresh trigger system** — listens for ownership change, sanctions list update, material entity status change

---

## Refresh cadence

**Event-triggered**, not annual. Triggers:

- Sanctions list update with a new hit on existing data
- Customer-reported ownership or signatory change
- Material entity change detected by silent SENIAT re-check (e.g., entity dissolved or activity changed materially)

When triggered: email + in-app banner → 1-screen diff form (only changed fields + re-attestation).

If internal legal requires a time-based fallback, the fallback is a once-yearly 1-screen "Has anything changed?" reconfirmation — not a re-collection of the full flow.

---

## Sign-off — Internal Legal

This section is the explicit ask: **review and sign off on the scope below before we ship the flow.**

External counsel proposed a comprehensive customer-facing ask (Ficha + Beneficial Owner form + Source-of-Funds declaration + a checklist of uploaded documents). That ask is calibrated for a regulated financial entity. Tesote Connect is not one — it is a B2B SaaS product. The scope below right-sizes the ask for Connect.

### A. What we WILL collect from the customer

| Item                                              | How                          | Required                              |
| ------------------------------------------------- | ---------------------------- | ------------------------------------- |
| RIF                                               | Customer-typed               | Always                                |
| Razón social                                      | Customer-typed               | Always                                |
| Domicilio fiscal                                  | Customer-typed               | Always                                |
| Registered economic activity                      | Customer-typed               | Always                                |
| Signatory cédula                                  | Customer-typed               | Always                                |
| Signatory full name                               | Customer-typed               | Always                                |
| Signatory role in company                         | Customer-typed               | Always                                |
| Signatory work email + phone                      | Customer-typed               | Always                                |
| Attestation: information is true                  | E-sign checkbox              | Always                                |
| Attestation: no sanctions / no PEP (or disclosed) | E-sign checkbox              | Always                                |
| Attestation: no AML/CFT-prohibited activity       | E-sign checkbox              | Always                                |
| SENIAT silent cross-check on entity data          | Server-side                  | Always (Tesote runs, customer doesn't see) |
| SAIME silent cross-check on cédula → name         | Server-side                  | Always (Tesote runs, customer doesn't see) |
| Sanctions + PEP screen results                    | 3rd-party API (server-side)  | Always (Tesote runs on entity, signatory, and every UBO; customer doesn't see) |
| Beneficial owners ≥25%                            | Customer input (sub-table)   | Always — yes/no question, sub-table if yes (FATF 25% threshold) |
| `Acta de asamblea` (most recent)                  | PDF upload at sign-up        | Always                                |
| Foreign-entity / country-of-origin data           | Customer input               | Conditional — only if RIF is non-VE   |

### B. What we will NOT collect (out of scope for Tesote Connect)

External counsel proposed each item below. We are explicitly leaving each out for Tesote Connect, with rationale. Internal legal: please flag any item you believe must be re-included.

| Item counsel proposed                                | Out of scope — rationale                                                                                  |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Top clients table (with each one's RIF + address)    | Invasive, sensitive commercial data; standard B2B SaaS does not ask. Not required by law for SaaS sale.   |
| Top suppliers table                                  | Same reasoning.                                                                                           |
| Two bank references (≤3 months old)                  | Bureaucratic theater for a SaaS subscription. No regulatory basis at Bajo tier.                           |
| Two commercial references                            | Same.                                                                                                     |
| Most recent ISLR declaration                         | Tax data not relevant to risk for a SaaS sale; reading it does not reduce our risk.                       |
| Audited financial statements                         | Only relevant if extending credit. Tesote Connect does not extend credit.                                 |
| Source-of-Funds signed declaration                   | Customer is paying for software, not depositing funds with us. Concept does not apply to SaaS.            |
| Beneficial Owner declaration at 10% threshold        | Replaced with **25% threshold** (FATF global default). Asked by default (yes/no + sub-table).             |
| Beneficial Owner declaration as standalone Word doc  | Replaced with inline sub-table + e-sign attestation in the same flow.                                     |
| Site visit ("visita técnica")                        | Inappropriate for a SaaS vendor; no regulatory basis.                                                     |
| Acta constitutiva / registro mercantil PDF upload    | Replaced with public registro mercantil lookup; PDF only requested if public lookup fails.                |
| Operating-license document                           | Conditional — only if registered activity is in a regulated industry. Hidden by default.                  |
| Domicile proof (utility bill)                        | Replaced with customer-typed domicilio fiscal, cross-checked silently against SENIAT.                     |
| Notarial-format Word-doc declarations                | Replaced with e-sign checkbox attestations.                                                               |
| Annual full-expediente refresh                       | Replaced with event-triggered refresh; 1-screen diff form on change.                                      |
| Operating phone number for company                   | Customer's signatory phone is collected; separate company line is not asked.                              |
| Website (company URL)                                | Optional / not collected. Not material to risk.                                                           |

### C. The substitutions we are making — please confirm acceptable

These are the design choices that depart most from counsel's template. Internal legal sign-off on each:

1. **25% beneficial-owner threshold** (vs. counsel's 10%). Aligned with FATF global default. ☐ OK ☐ Not OK
2. **Public registro mercantil lookup as substitute for PDF upload** at default tier. ☐ OK ☐ Not OK
3. **Customer-typed entity data with silent server-side SENIAT/SAIME validation** (vs. counsel's PDF document uploads). Mismatches flag for manual review without surfacing the lookup to the customer. ☐ OK ☐ Not OK
4. **Customer-typed domicilio fiscal as substitute for utility-bill domicile proof** (typed value cross-checked against SENIAT silently). ☐ OK ☐ Not OK
5. **E-sign checkbox attestations as substitute for notarial-format Word-doc declarations** (sworn statement, no-sanctions, no-AML-prohibited-activity). ☐ OK ☐ Not OK
6. **Event-triggered refresh as substitute for annual full-expediente refresh.** ☐ OK ☐ Not OK
7. **Risk tier defaults to Bajo for VE-domiciled B2B SaaS customers** (per counsel's own matrix) — no Medio/Alto escalation built into the default Connect flow. ☐ OK ☐ Not OK
8. **No source-of-funds declaration for Tesote Connect.** Concept reserved for future Payments / Capital products. ☐ OK ☐ Not OK
9. **Sanctions/PEP screening run by Tesote (3rd-party API), no customer-facing screening question.** ☐ OK ☐ Not OK

### D. What is reserved for future products (not this spec)

Listed for completeness — these will return when the relevant product launches, and will be specced separately:

- Source-of-Funds declaration → returns for **Tesote Capital** (when launched)
- Audited financial statements → returns for **Tesote Capital** (credit-related products)
- Beneficial Owner at 10% threshold → only if a future product or a specific high-risk customer warrants it
- Heavy bank/commercial references → only if a future product requires non-bank-discharged KYC

### E. Sign-off

- Reviewed by: ______________________
- Date: ______________________
- Decision: ☐ Approved as-is ☐ Approved with changes (note below) ☐ Not approved
- Notes / required changes: ______________________

---

## Open dependencies

These shape the flow as designed; tracked alongside the legal sign-off above:

1. Confirmation that e-sign satisfies VE law (Ley sobre Mensajes de Datos y Firmas Electrónicas) for the three attestations
2. Confirmation that public registro mercantil lookup is acceptable as substitute for PDF upload
3. Decision on whether the operating-license question stays at all for Connect (probably no — Connect's customer base does not include regulated industries by default)

---

## Links

- [[../legal/kyc-customer-collection-design]] — regulatory rationale, friction audit, and the broader counsel pushback
- [[tesote-legal-affairs-april-2026]] — counsel-facing master brief
- [[../strategy/product-strategy-execution-plan]] — onboarding speed is on the critical path
