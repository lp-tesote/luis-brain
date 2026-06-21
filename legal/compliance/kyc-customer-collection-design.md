---
title: KYC — What We Ask Customers, and How (Design)
tags: [legal, compliance, kyc, onboarding, payments, friction]
updated: 2026-04-27
status: draft
---

# KYC — What We Ask Customers, and How

Counsel sent six documents (`~/Downloads/documento_de_compliance_kyc_1/`). This doc separates **what's internal vs customer-facing**, inventories everything we'd ask a customer to provide, audits friction, and proposes a low-friction collection design.

Companion to [[tesote-legal-affairs-april-2026]] — specifically P0.1 (Payments KYB / AML obligation allocation) and P0.4 (Tesote Business / counterparty TOS).

---

## What counsel sent — separated by audience

**Internal (Tesote uses these — never shown to customers):**

- `Politica-Conoce-Tu-Cliente-Rev02.docx` — our KYC policy, defines 4 risk tiers and what diligence each tier triggers
- `Matriz-Evaluacion-Riesgo.xlsx` — risk-scoring spreadsheet (24 variables across client profile + transactional behavior; outputs Muy Bajo / Bajo / Medio / Alto)
- `Modelo-de Acta-Junta-Directiva.docx` — template for a Tesote board acta approving the KYC policy (one-time governance artifact, not per-customer)

**Customer-facing (the customer fills/signs these):**

- `FOR-ADM-001-3 Ficha de Clientes.xlsx` — Customer ID form (the "Ficha")
- `Formulario-Beneficario-Final-3.xlsx` — Beneficial Owner declaration (legal entities only)
- `Modelo-de-Declaración de Origen de Fondos.docx` — Source-of-Funds declaration

**Plus a customer document checklist** baked into the Ficha (RIF, cédulas, registro mercantil, ISLR, bank refs, commercial refs, contract, etc.).

---

## Counsel's full ask — raw inventory

### Information the customer types into forms

**From the Ficha (legal entity case):**

1. Razón social, RIF, place + date of constitution
2. Office address, city, country
3. Object social / economic activity, specific activity, products/services
4. Website, phone
5. If foreign company → country of origin
6. **For each shareholder / legal rep / apoderado**: full name, ID number, fiscal domicile
7. Operating license info (if industry requires one): license number, issue date
8. **Top clients** (each: name/razón social, address, ID/RIF, length of relationship)
9. **Top suppliers** (each: name/razón social, address, ID/RIF, length of relationship)
10. AML/CFT policies — yes/no + describe
11. Sanctions / fines / legal procedures history under VE AML law
12. Sworn statement (info is true; will notify of changes)
13. Signature

**From the Beneficial Owner form (legal entity):**

For every individual with ≥10% ownership or effective control:
- Full name, ID, nationality, country of residence, % participation, type of control, PEP status
- Plus: any intermediate vehicles in the chain (holding cos, trusts, etc.)

**From the Source-of-Funds declaration:**

Sworn statement that funds come from lawful sources (savings, salaries, lawful commercial revenue, inheritance, donations, prior investments, etc.) — signed by legal rep.

### Documents the customer uploads

**Legal entity (full ask, per the Ficha checklist):**

1. RIF (current)
2. Cédula + RIF for each legal rep
3. Certified registro mercantil + amendments (acta constitutiva)
4. Acta de asamblea showing current Junta Directiva (term not expired)
5. Most recent ISLR declaration
6. **Two** bank references (≤3 months old)
7. **Two** commercial references
8. Signed Source-of-Funds declaration
9. Signed Beneficial Owner declaration
10. Signed service contract

**Natural person:**

1. RIF
2. Cédula / passport
3. Proof of domicile (utility bill)
4. One bank reference
5. One commercial reference (≤3 months)
6. Signed Source-of-Funds declaration
7. Signed service contract

### What counsel does behind the scenes

- Sanctions screening: ONU, OFAC, ONCDOFT, ICIJ Offshore Leaks
- PEP screening
- SENIAT / IVSS / public-registry validation
- Site visit ("visita técnica") if domicile looks suspicious
- Risk score → tier → triggers heavier diligence
- Annual refresh (or on triggering event)
- File retention: 10 years post-relationship

---

## The risk-tier escape hatch counsel already gave us

Counsel's own policy says diligence depth scales with risk:

| Tier        | Trigger                              | Customer-facing ask                                                            |
| ----------- | ------------------------------------ | ------------------------------------------------------------------------------ |
| Muy Bajo    | Minimal exposure                     | "Identificación mínima" — basically ID + RIF                                   |
| Bajo        | Standard SaaS customer, VE-domiciled | RIF, cédula of rep, domicile receipt, registro mercantil, 1 bank ref, contract |
| Medio       | Enhanced — flagged variables         | + financial statements, 2 ISLRs, 1 commercial ref, bank statement              |
| Alto        | High-risk variables                  | + audited financials, 2 bank refs, 2 commercial refs, sanctions/PEP deep dive  |

**This is the lever.** The Ficha checklist as written shows the *maximum* ask (Alto). For most Tesote customers we should be operating at Bajo or Muy Bajo and *not* asking for two of everything.

The Ficha form itself, however, is one document with all fields — it doesn't visually scale with risk. That's the UX problem to solve.

---

## Friction audit — what's actively annoying

Ranked from "most likely to kill conversion" downward:

1. **Top clients + top suppliers tables.** This is the worst ask. Sensitive commercial info, customer has to chase RIFs of *their* counterparties, and it's almost never asked of B2B SaaS customers elsewhere. Counsel needs to defend why this is needed for a low-risk customer.
2. **Two bank references + two commercial references.** Old-school VE bureaucracy. Each bank reference takes 1–2 weeks to obtain. Doubles the onboarding time.
3. **Triple identity entry.** Customer types name + RIF + address into the Ficha, then again into the Beneficial Owner form, then again into the Source-of-Funds declaration. Pure dedupe waste.
4. **Notarized-looking declarations as Word docs.** Source-of-funds and Beneficial Owner are formatted like notarial instruments. Customers will treat them as such (read: delay, lawyer, route to admin).
5. **Acta de asamblea with current Junta Directiva.** Often expired in real VE companies — fixing that is a multi-week registro mercantil procedure that has nothing to do with us.
6. **ISLR declaration + financial statements.** Customers don't want to share these casually; many don't have clean ones.
7. **Manual signatures on multiple documents.** Without e-sign, this is print-sign-scan-email × 3.
8. **Operating-license question.** Most SaaS customers don't need one; the field is noise for them. Conditional, not required.

**Total time-to-onboard at full ask, conservatively: 10–20 business days.** That's a deal-killer for the GTM motion in [[../strategy/product-strategy-execution-plan]].

---

## Proposed design — coverage without the clunk

### 1. Risk-first, not form-first

Don't show the customer the Ficha. Show them a single onboarding flow that *internally* maps to the Ficha. Behind the scenes, we score risk first (using public data — RIF lookup, SENIAT, basic profile). Only escalate to enhanced diligence when the score warrants it.

Default tier for an established VE B2B customer using SaaS-only: **Muy Bajo or Bajo**. Coverage = ID + RIF + cédula of rep + domicile + sanctions/PEP screening (we do this, not them).

### 2. One form, dedupe identity

Combine Ficha + Beneficial Owner + Source-of-Funds into a single web form. Identity fields entered once. Beneficial Owner is a sub-table inside the same flow. Source-of-Funds becomes a checkbox attestation, not a separate signed document.

### 3. Pre-fill from public sources

For VE legal entities we can — at minimum — auto-pull:

- RIF data from SENIAT (number, razón social, domicilio fiscal, status)
- Registro mercantil basics from public lookups (where available)
- Cédula validation via SAIME or CNE

This shrinks the typing burden by ~60% for the customer.

### 4. Conditional fields, hidden by default

- Foreign-company fields: only show if entity is non-VE
- License fields: only show if industry flagged as regulated
- Top-clients / top-suppliers: **only at Medio+ tier**, never at default
- Audited statements: **only at Alto tier**

### 5. Replace manual references with electronic signals where defensible

- Instead of "two bank references," use Tesote Connect itself: a customer who has connected their bank accounts gives us 12+ months of statement-level signal. Counsel needs to bless this as a substitute (this is the most important policy ask in this whole doc).
- Commercial references: replace with proof of an existing customer/supplier relationship pulled from their ERP via Tesote Automations, when available.

### 6. E-sign by default

All declarations (sworn statement, source-of-funds, beneficial owner) become checkbox + e-signature in the flow. No notarial-looking Word docs. Counsel to confirm e-signature is sufficient under VE law for these AML attestations.

### 7. Stage the ask

- **Sign-up:** identity + RIF + cédula + sworn checkbox attestations. ~5 minutes.
- **Activation (before first transaction):** registro mercantil + domicile proof. Async, customer can drag & drop.
- **Volume thresholds:** if the customer's transactional behavior crosses a Medio/Alto trigger, *then* request the heavier docs. Justified by their own activity.
- **Annual refresh:** automated email, only re-confirms what's changed.

### 8. Make our internal work invisible

- Risk scoring happens server-side. Customer never sees the matrix.
- Sanctions/PEP screening runs on submit. If clean → onboarded. If hit → manual review without telling the customer (counsel: this is also the "no tipping-off" rule).
- The full Ficha document gets generated *from* the customer's inputs and stored in the expediente — they never fill an Excel.

---

## What this means for the product team

This isn't a "send the customer a Word doc" workflow. It's an onboarding screen + a risk engine + an expediente generator. Roughly:

- Frontend: one progressive form, ~5–8 screens, conditional logic
- Backend: risk-scoring service implementing the matrix, sanctions/PEP screening (3rd party), public-source enrichment (SENIAT, SAIME)
- Document service: generates the Ficha, Beneficial Owner declaration, Source-of-Funds declaration as PDFs (e-signed) for the expediente
- Storage: expediente per customer, retention timer (10 years)
- Annual renewal: email + diff form

This belongs on the Payments roadmap, not as a separate compliance project — it *is* the onboarding for everything we ship.

---

## Open questions for counsel

1. **Bank-account-connection-as-bank-reference substitution.** Can a connected, verified bank-account stream from Tesote Connect substitute for the "two bank references" requirement at Bajo and Medio tiers? This single ruling collapses the biggest friction point.
2. **E-signature sufficiency for AML attestations.** Source-of-Funds, Beneficial Owner, and the sworn statement at the bottom of the Ficha — can these be e-signed under VE law (Ley sobre Mensajes de Datos y Firmas Electrónicas)? If yes, we kill the print-sign-scan loop.
3. **Top-clients / top-suppliers requirement.** Is this Sudeban-mandated for our model, or counsel's belt-and-suspenders default? If the latter, can we drop it at Bajo tier?
4. **Two-of-everything at higher tiers.** Two bank refs + two commercial refs at Alto — Sudeban-mandated or counsel default?
5. **Acta with current Junta Directiva.** Hard requirement, or can we accept the most-recent acta on file even if the term technically lapsed? Many customers will fail this if strict.
6. **Risk-matrix variable for "AML obligation sits with BNC."** Tesote-on-BNC means BNC has the regulatory KYB obligation on the debited account (per [[tesote-legal-affairs-april-2026]] P0.1). Should our matrix down-weight customers when BNC is the rail (since they're already KYB'd by BNC) — and is counsel comfortable with that down-weighting?
7. **Beneficial owner threshold.** 10% is conservative; FATF default is 25%. Can we move to 25% to reduce form length, or is 10% policy-locked?
8. **Annual refresh cadence.** Strict annual, or event-triggered (changes to ownership / volume threshold crossings)? Event-triggered is much cheaper for both sides.

---

## Critical vs. overkill — opinionated take

The previous sections take counsel's ask at face value and design around it. This section pressure-tests the ask itself. **TL;DR: the docs counsel sent are a generic Venezuelan corporate AML/KYC template. They're calibrated for a regulated financial entity. We're not one.** Most of it is overkill for what Tesote is *today*.

### What we actually are, regulatorily

- **Tesote-the-SaaS** sells software (Connect, Automations, Business) to companies. Selling SaaS does not trigger KYC obligations anywhere — at most you sanctions-screen and validate the entity exists for billing/contract purposes.
- **Tesote-the-payments-orchestrator** moves money between two BNC accounts. Tesote never custodies. The regulated KYC obligation sits with **BNC** (they hold the accounts and KYB'd both sides). Confirmed in [[tesote-legal-affairs-april-2026]] P0.1.
- **Tesote-the-future-Capital-marketplace** would be different — but that's 2027 at earliest.

So the docs counsel sent are not really about regulatory compliance for Tesote-today. They're about *defensive corporate posture* — making sure Tesote isn't a vehicle for money laundering through its customer relationships. Useful, but the right calibration for that is "B2B SaaS Stripe-style verification," not "Venezuelan bank's customer onboarding."

### The true minimum that gives us coverage

For a default Tesote SaaS customer (VE-incorporated, paying for software):

1. **Razón social + RIF**, validated against SENIAT (we pull, customer doesn't type)
2. **Signatory cédula + role**, just enough to confirm contract authority
3. **Automated sanctions/PEP screen** on the entity and the signatory (OFAC, UN, EU, ICIJ — third-party API, runs on submit)
4. **Object social sanity check** — registered economic activity is plausible and not in a banned list
5. **Domicile** — pulled from SENIAT/registro mercantil; we don't ask the customer

That's it. Customer-perceived friction: ~3 minutes, no documents to upload, no signatures beyond the master service agreement. Coverage: real entity, authorized signer, not on a list, plausible business. That's what 95% of B2B SaaS in well-regulated markets does.

For Payments customers specifically: add **proof they're an active BNC business-account holder** — which BNC will already have validated as part of the OTP debit setup. So we get bank-grade KYC for free without asking the customer anything more.

### What's legitimately needed at higher tiers (only when triggered)

- **Beneficial Owner declaration** — at FATF's 25% threshold (not 10%), and only when the ownership chain isn't readable from public registro mercantil data, OR the entity is non-VE
- **Acta de asamblea** — only when contract value or signing authority is non-obvious; for a standard SaaS contract this is irrelevant
- **Source-of-Funds declaration** — for *Capital* customers (when we launch it). Not for SaaS subscriptions. Companies don't "deposit funds" with their software vendor.
- **Enhanced screening + manual review** — for PEP hits, sanction-list near-misses, very high transaction volume, foreign opaque structures

### What's overkill for default Tesote customers

- ❌ **Top clients / top suppliers** — invasive, sensitive, never asked by B2B SaaS competitors. Counsel-default belt-and-suspenders.
- ❌ **2 bank references** — bureaucratic theater. Tesote Connect bank stream is strictly better signal at zero customer effort.
- ❌ **2 commercial references** — same.
- ❌ **ISLR declaration** — not our business; reading it doesn't reduce our risk meaningfully.
- ❌ **Audited financial statements** — irrelevant unless we're extending credit (we're not).
- ❌ **Source-of-Funds declaration as a default** — overkill for SaaS. Move to Capital-only.
- ❌ **Beneficial Owner at 10% threshold** — too low for our risk surface; 25% is the global standard.
- ❌ **Site visits** — totally inappropriate for a SaaS vendor.
- ❌ **Annual refresh of the full expediente** — event-triggered (volume crossing, ownership change, sanctions hit) is the right cadence.
- ❌ **Notarial-format declarations** — replace with checkbox attestation in the master service agreement.

### What changes the math

Right-sizing today doesn't lock us in. The ask should expand when *the product expands*:

| Trigger                                                | New requirements unlock                                                                              |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Tesote Capital launches                                | Source-of-Funds, audited financials, beneficial owner at 10%, real underwriting docs                 |
| Tesote gets its own PSP / fintech license              | We become the regulated entity → full Sudeban-style ask becomes legit (and required)                 |
| Multi-bank Payments where partner doesn't carry KYC    | Some of the heavier ask returns for the non-KYC'd flows                                              |
| Specific high-risk customer (large vol, PEP, foreign)  | Escalate that customer to enhanced diligence — but it's exception handling, not the default flow     |
| FATF / Sudeban guidance materially changes for fintech | Re-baseline                                                                                          |

### Pushback to counsel — the actual ask

When counsel circles back, the conversation shouldn't be "tweak the form." It should be:

1. **"This template is calibrated for a regulated entity. We're not one — we're a B2B SaaS with a payments product riding BNC's licenses. Re-baseline the ask for that posture."**
2. **"Confirm in writing that, for Tesote-on-BNC payment flows, BNC's KYB on both ends discharges Tesote's regulatory KYC obligation."** This is already P0.1 in the legal affairs brief — pull it forward.
3. **"Give us the minimum viable customer onboarding ask for Tesote-today, and a separate spec for what gets layered on when Capital launches and/or we hold our own license."** Two specs, not one.
4. **"Bless the substitutions"** — Tesote Connect bank stream as bank-reference substitute, e-signed checkbox attestations as declaration substitute, automated sanctions/PEP screen as the standard.

If counsel pushes back hard on the minimum tier, the right framing is: *we are a software company. The point at which our regulatory exposure goes up is the point at which we get our own license — and at that point, we'll meet the bar that license requires. Until then, asking customers for two bank references to use SaaS is friction we cannot justify.*

---

## Notes & links

- [[tesote-legal-affairs-april-2026]] — counsel-facing master brief; this doc operationalizes the KYC ask under P0.1
- [[../strategy/product-strategy-execution-plan]] — onboarding speed is on the critical path for the Payments + Business launch
- [[../sales/payments-gtm-while-b2b-gated]] — friction here directly affects activation rate during the gated phase
- Source files (do not edit): `~/Downloads/documento_de_compliance_kyc_1/`
