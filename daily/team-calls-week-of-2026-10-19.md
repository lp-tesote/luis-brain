---
title: Team calls — week of 2026-10-19
tags: [team-calls, weekly-digest, fireflies, roam]
updated: 2026-10-23
window: 2026-10-19 .. 2026-10-23
---

## Needs Luis's attention

- [ ] Send Airtek meeting summary + pending requirements doc + continuity proposal — from "Tesote // Airtek" (2026-10-20)

---

## By workstream

### CX / Ops (internal)

- **Weekly CX w/Luis** — 2026-10-20, 5 people, ~1h46m (Roam)
  Estefany led. Reviewed implementation KPIs (velocity, at-risk clients, stage health), retention/churn learnings (decision-maker loss, bank-config failures), and support metrics. Key calls: measure implementation hours via Clock for 1 month; pilot per-stage CSAT survey; define weekly case-close criteria; schedule CS sessions for high-volume support accounts; follow up on 19 intermittent-use clients next meeting.

- **Sales Pitch, Diagnostics, and Pricing** — 2026-10-20, 3 people, ~21m (Roam, Luis hosted)
  Internal prep for an Odoo prospect. Agreed: keep pitch simple (customer-specific diagrams); paid diagnostic at ~$2K (with optional credit toward fees); Daniel to draft concise data request; Nicolás to confirm Odoo operational status via Ronald.

### Sales / Business Development

**Monday Oct 20**

- **Intro: Corpocrea // Tesote** — Luisana + Nicolás. Edwin wants reconciliation-first, API integration with Odoo. No full platform needed. Nicolás to send requirements doc + proposal for Friday 11:00 presentation. Estimated 5hrs/week recovered.

- **Propuesta: Tesote // Drovital** — Nicolás. 8 accounts. $2,500 impl + $500/mo (discounts 5%/10%). Board review scheduled Tuesday. Pending demo + contract from Nicolás before board meeting.

- **Tesote // Airtek** — Luis + Nicolás + Daniel + 6 Airtek contacts. Reconciliation automation in Odoo confirmed as complete product. Scope: bank connections, POS batch mapping, payment methods. Diagnostic needed before confirming cost. Implementation 4–5 months. Luis to send requirements doc + summary + continuity proposal. ← **Luis's action item**

- **Propuesta: Tesote // Simbi (pre-call)** — Nicolás + Roberto. Decision-maker hasn't seen a demo yet. Nicolás to prep simple demo + business case. Rescheduled to next day 16:00.

- **Tesote // Grupo Wolf** — Nicolás. 112 accounts, 37 entities, 5 banks. Conciliation currently manual via states of account → Profit. Tesote to standardize, apply rules, generate Profit-compatible files (compatibility still to validate). Proposal to be reviewed Thursday 11:30.

- **Tesote // Hispana de Seguros (presencial)** — Esteban + Estefany. Weekly manual reconciliation, egress conciliation hard due to non-uniform bank references + batch payments. Mercantil T-1, Banesco/Venezuela real-time. AX integration: programmer needs to define how to consume Tesote references. Banco Activo/Banca Amiga/Venezuela need credential updates. 45-day Reverón trial offered. Estefany to send token, tech docs, authorization forms.

- **Sesión de Alineamiento: Tesote // Master Group** — Esteban. Proposal B (no Odoo integration initially). $5,300 impl, $2,300 (Jessica's budget) vs $2,500 (Esteban's floor) monthly. Bimonthly billing, 225 accounts, ~27K tx/mo. Contract 12 months; legal review + counteroffer pending. BNC/Mercantil via API; others via consultation users or PLAT/Netcash. 6–8 weeks impl.

- **Intro: Delcop // Tesote** (Oct 19) — Luisana + Nicolás. ~360 payments/day, 8 accounts, 2–5% retention differences. Odoo 16 native app. Security questions outstanding (ISO 27001, MFA, AWS). Nicolás to send form + security docs; awaiting form completion from client.

**Tuesday Oct 21**

- **Intro: Mango Bajito // Tesote** — Luisana + Esteban + Roberto. Call failed — key leader was pulled by the president. Douglas to validate availability and re-contact Luisana.

- **Propuesta: Tesote // Cartago C.A** — Nicolás. 6 accounts, ~2K tx/mo in Odoo. $4,000 + $750/mo (5%/10% discounts). Odoo integration via API at no extra cost. Partner validates post-implementation. Joseph to review with partners, decision next week.

- **Discovery: Credicard // Tesote** — Esteban. High-complexity strategic prospect. Manual SAP conciliation with no auto-match, open items, missing identifiers. PCI/SUDEBAN restrictions → on-premise architecture required (tech + security + operations + SAP team + Ibicorp partner). Phases: connection → identification → reporting → SAP integration. Proposal with technical alternatives + phases + cost due by Friday. **Client needs info within 15 days to evaluate 2027 budget (or falls to 2028).** Esteban to coordinate with technical partner.

- **Tesote // Farmadon** — Esteban. 20 accounts in Venezuela, 2–3 day lag in manual reconciliation. Priority: reconciliation automation + commission tracking. Banplus needs statement mirror. Phase 1 without Odoo. Esteban to send demo + inventory request.

- **Propuesta: Tesote // Simbi** (Oct 21 evening) — Silent/skipped, no summary.

**Wednesday Oct 22**

- **Discovery: Tesote // Domosa** — Nicolás. 11 companies, ~100 accounts, shared banks across entities. API preferred over manual loads. $15K–22K annual (TBD by accounts/tx/development). Nicolás to share API docs + proposal; client to send company/accounts/volume data.

- **Intro: Multimarcas del Centro // Tesote** — Luisana + Nicolás. 5 national + Panama + US + Binance accounts. ~1,200 receipts/week (4,800–5,000/mo). Migrating Odoo → Nebula; multicompany, multicurrency. Tesote to integrate via API or flat file with Nebula. $9K–25K annual range (TBD). Nicolás to send bank template and coordinate meeting with partners.

- **Nicolás & Jonathan (Aromacom) - Tesote** — Tesote API adjusted since February; can connect to Odoo, other systems, and agents. Tesote as banking hub. Jonathan to share updated proposal with board + CEO. Nicolás to send updated commercial proposal + contract. Approval pending from directiva.

**Thursday Oct 23**

- **Propuesta: Tesote // Grupo Wolf** — Nicolás. 112 accounts, $7K implementation + $3,500/mo (payment mode discounts). Reverón AI included. Profit integration: extracts from Tesote as pre-conciliated files (Profit can't load directly). Nelsi to present to management; Nicolás to send docs + contract.

- **Propuesta: Tesote // Seguros Caroní** — Nicolás. 5 accounts, ~1,700 tx/mo. $4,500 one-time + $800/mo + 3 months Reverón free. 3 phases. Banco Caroní: no direct connection, daily manual extract for now (bank integration to be evaluated). Nicolás to send demo + proposal + contract + blueprint; Rubén to review internally, conversation to resume ~next week.

- **Tesote // Chevere** — Esteban. Replacing manual financial controls pre-expansion. 4 banks (Mercantil VE, BNC, Provincial, Banesco) + Mercantil/Banesco Panama. Brazil via available bank API. Binance connection planned for November (not yet available). Needs operational meeting + commercial materials + client list. Esteban to send.

### Implementation / Customer Success

**Monday Oct 20**

- **Mesa de Trabajo: APB Group // Tesote** — Keyla + Esteban + Estefany + 5 APB contacts. Redmi Note 13 configured for Banca Amiga SMS auto-forward (successful). 5 pending: Venezuela/Banco Activo/Exterior (bad/expired credentials), Mercantil (migrating to SMS), Exterior. API migration for Venezuela + Vanesco bolívares: 48h after bank authorization. Vanesco Panama account 9306 + October duplicate movements under review. FIGO masters pending for categorization rules.

- **Sesión de Alineamiento: Tesote // Master Group** — (listed above in Sales; also an implementation alignment call)

- **Purolomo // Tesote** — Keyla + Estefany. Samsung set up for BDV SMS forwarding (test successful). Sync schedules pending. Daily Excel file for VOG. Induction: Monday 2pm, Tuesday as backup.

- **Consultoría: La Wawa // Tesote** — Joan. Daily flow: balance check → movement download → report + voucher cross. Banca Amiga validated (4 movements confirmed). Vanesco needed additional sync. One account R: 64 vs 65 movements discrepancy — extract to be re-downloaded. BNC form pending signature. Vanesco follow-up + report validation Friday.

- **Corporacion JSL // Odoo (session "jsl")** — Joan (~2h46m). Odoo-Tesote integration: provider/client cross by RIF, variable entity names, BNC "R" issue. Nov production date. Cut-off Oct 15: validated entries auto-pass, pending ones wait. Rules by phases: transfers + commissions first. Manual validation October, go-live November.

**Tuesday Oct 21**

- **CS meeting: Corporación Inveca // Tesote** — Estefany. ~20 Vanesco movements missing on Monday update (report rebuild from bank required). Estefany to investigate + reconcile. Banco Plaza back to scheduled syncs (post 09:00). Isaac to add 4th sync window and new cash position report (post 08:30). Provider base + tax IDs to be shared to improve egress identification.

- **Fivenca // Tesote (Revisión de Reglas)** — Joan + Estefany + Katleya (3h1m). Automated classification rules for commissions, recurring payments, employees, variable cases. Notes/counterparties/categories via text conditions, amounts, names, types. Duplicate rules and records detected and cleaned. Consolidated bank commission rules across companies pending. Estefany: bring rule engine improvements to Dan.

- **Consultoría: Grupo Oseo // Tesote** — Joan (~1h18m). Treasury downloads daily bank extracts and shares with CX/Cobranza. Mercantil API in testing (synced with linked phone, no token, scheduled). BNC for collections, Bancamiga for payroll, Provincial for POS. Groups configured: Gerencia / Contabilidad / Analistas. Next session: categories + counterparties validation + auto reports.

- **Corporacion JSL // Odoo** — Joan. BNC mapping complete. Daily transaction auto-send live from Oct 15. Missing transactions comparison ongoing. Mercantil Electrónica + Vanesco Electrónica still without visible movements. Provincial up to 5 days lag. Production Nov via single cutover. Joan + Wilmar + Sandra to Odoo group.

- **Tesote // Viva Supercentro** — Esteban + Estefany + 2 Viva contacts (~1h12m). Phase 1 confirmed: bank connections, balance queries, categorization, auto reports, email reports, SAP + Power BI integration. Plan of accounts + client/provider base to be loaded for classification rules. Daily payments file development: $1,000 one-time fee, structure to be confirmed. **$1,400/mo license from November** (October at prior rate). Amaranth priority — CEL operations start Nov 1. Estefany to coordinate setup.

- **Conexiones // Consorcio Ragnar** — Joan (~2h39m). Banca Amiga done (QR saved, Google Authenticator set). Vanesco Panama connected. Mercantil Panama partial (5 questions registered, token pending). Venezuela pending (phone signal + app + Justin's codes). Scheduled syncs automated for all except Venezuela/Mercantil (manual). Daily report 4pm configured; Adriana adopting. Engineering to validate open connections.

- **Grupo Parawa // Tesote** — Estefany. Account config by bank/currency/company. Mercantil via API+token in process. Unassigned tasks: OceanBank connection, Banco Ademi manual account, authentication update, category alignment with Contabilidad. Estefany: send bank user guide + API integration details + coordinate in-person meeting.

- **Tesote <> ABODOM: Check-in Octubre** — Yorle. Platform use declined (key person on leave). Dilkenia to resume on return. Client directory to be loaded for auto-counterparty rules. SAP integration on hold — Fernando to resume when team available.

**Wednesday Oct 22**

- **Configuración de Conexiones Bancarias SAVAKE (FerreTotal)** — Joan (~2h35m). Connected: Mercantil VE, Vanesco VE, Provincial, Bancaribe, Tesoro, Banca Amiga, Vanesco Panama, Vanesco USA. Mercantil Panama failing (security questions recurring). BNC planillas need Alberto's physical signature (up to 1-week delay). Venezuela pending (master user). Sync schedules defined; Tuesday 11am follow-up for pending connections + cash flow categories.

- **Crixto // Tesote (Configuración)** — Keyla + Estefany. Banco Activo IBAN Plus updated. Banco Plaza → API integration in progress. Bancaribe pending email confirmation. Daily reports 8am and 4pm agreed. Account inventory + counterparties + permission review next session.

- **Check In Fenix Salud** — Joan + Estefany. 11 banks connected (including Amaranth). 80%+ categorized across Administración/Tesorería/Cobranza. Odoo conector (bidirectional, some latency) vs API (flexible): Yesika to decide. Banco Plaza connection next step. Adjusted manual work from a full morning to 1–2 hours.

- **Tesote <> La Innovacion: Check-in Octubre** — Yorle + Joan. Two calls (pre-call logistics + main). Main: team uses Tesote for balance queries only (no reconciliation/categories yet). Yorle to check with Sofía whether Contabilidad uses it — could enable bank pre-reconciliation. Slowness and outages flagged. Monthly/bimonthly cadence proposed. Next scheduled check-in: Nov 8 at 14:00.

- **Customer Success Meeting: Nueve Once // Tesote** — Estefany + Joan + Yorle. Banco del Tesoro synced. Banesco reconfigured (consultation user). Still pending: OnePlus, Facebank, Banplus (need to clear 4 security answers), Venezuela, Mercantil (Android user + Entros token). Facebank: manual token daily + 2 scheduled afternoon syncs. Daily cash position report at ~08:00-08:15 configured.

- **Configuración de Conexiones: Grupo DUSA // Tesote** — Keyla. Bancaribe connected (3 accounts, 7 days sync). Provincial blocked (soft token config needed). Mercantil: delete old user → new user → Android phone. Vanesco: pending master access. First connection loads 10 days, then 3x/day auto. Next session: Thursday 10:00. BNC planillas pending.

- **Molina Viajes (Soporte) // Tesote** — Estefany + Rebeca. Credentials + permissions restructured (Nelly + Jean Carlos as authorized users). Android Honor XC on v1.4.2. Mercantil + Venezuela synced. Provincial intermittent (engineering ticket). Venezolano de Crédito shows next-day movements + manual transfer confirmation required. New interface migration: Oct 31. Early syncs pre-5am + cash position 8am.

- **Tesote <> Acabados y Pinturas: Check-In** — Yorle. Diego unavailable (in another meeting). Rescheduled to next week, pending date confirmation.

**Thursday Oct 23**

- **Tesote // Alvarigua** — Nicolás + Estefany + 2 Alvarigua contacts (~72min). Focus: daily cash flow control. 56% tx categorized in last 30 days → progressive target 80-85% → 90%. Account inventory audit needed. Sofitasa connection to review. EUR dolarization missing. Venezuela + Mercantil need SMS code automation. Estefany: send minutes + inventory + template. Technical session to validate syncs + saldo reconciliation.

- **Organización El Tunal // Tesote** — Keyla + Estefany + 2 El Tunal contacts (~63min). Sync modes (manual 10min lock, scheduled). Bancaribe/Banplus specific config. Banca Amiga/Venezuela/Mercantil via SMS. AMI/Entrust app codes not capturable. Vanesco + Redmi test failed (connection selection issue) — retry with real treasury users needed. SAP API available but not auto-posting entries yet.

- **Grupo Da Silva // Tesote** — Keyla + Estefany + 2 Da Silva contacts (~76min). Provinet credentials need update. Fondo Común: IP address save pending. Mercantil API migration pending bank authorization. First scheduled email report was empty → review with Product Monday 8am. Cash position report + bank statement schedules configured (morning + afternoon). Keyla to prepare categorization proposal.

### Engineering / Banking Integration

- **Incidencia API Extracto Bancario** — Santiago Pinzon (Tesote) + 4 Bancaribe engineers (Mujica, Camacho, Rojas, Blanco), ~62min. Console/Carbon work, seller request via room view, Paris requests, endpoint transaction fix, customer ID validation confirmed. No action items captured; silent meeting not flagged.

---

## Coverage

Roam = Luis's calls only (personal access token). Fireflies = org-wide (admin).
Gap: purely-internal Roam syncs between teammates Luis wasn't in are not captured. Fireflies returned exactly 50 calls (the query limit) — additional calls from earlier in the week may have been truncated; pagination not checked.

**Counts:** Roam = 2 calls | Fireflies = 50 calls (44 with summaries, 6 silent/skipped) | Deduped = 0 | Total distinct = 52
