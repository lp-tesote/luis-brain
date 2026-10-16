---
title: Team calls — week of 2026-10-12
tags: [team-calls, weekly-digest, fireflies, roam]
updated: 2026-10-16
window: 2026-10-12 .. 2026-10-16
---

## Needs Luis's attention

No action items were formally assigned to or suggested for Luis in either Roam or Fireflies this week.

**One inbound to watch:** The Roam marketing brief (Oct 13) logged that Roberto Drew-Bear was going to write to Luis about the Startup Summit — organizers haven't responded, and Luis's participation details are still unclear. If Roberto hasn't reached out yet, worth a ping. (`Weekly Marketing Brief`, 2026-10-13)

**Flag — churn:** Binaural canceled their Tesote subscription citing a better financial offer from a competitor. Service/support were praised. No action item assigned to Luis, but worth knowing. (`Binaural + Tesote`, 2026-10-13)

---

## By workstream

### Sales / New Business

- **Intro: Tesote // Credicard** — 2026-10-16, organizer: esteban.suarez@tesote.com, 82 min
  Large prospect. Operations: manual payment ID, daily SAP extract uploads, Excel-based bank availability. Tesote presented centralized saldo/movements (3x/day), filters, pre-reconciliation, read-only. SAP HANA integration to be evaluated. Two-phase implementation, 4–5 weeks estimated. Pricing shown: $5K–$10K impl, $12K–$70K/yr subscription. Next: client sends account inventory; Esteban prepares proposal, references, and executive presentation.

- **Intro: Domosa // Tesote** — 2026-10-16, organizer: luisana.cotoret@tesote.com, 23 min
  Multi-business group (construction, agro, electrical plants, wholesale, retail). Need: real-time bank positions to speed up purchase decisions, reduce Finance manual work. Tesote: consolidated BsD + USD saldos, filters by bank/currency/entity/BU, segregated permissions, ERP API or bulk template. Discovery meeting scheduled Tue Oct 20 at 2pm. Next: client sends bank/account/volume data; Nicolás sends commercial proposal.

- **Reunión con Tesote: MasterGroupVE** — 2026-10-13, organizer: carlos.melian@tesote.com, 37 min
  Holding of 15 restaurants, multiple legal entities. Validated Tesote for automating bank consolidation + Odoo T-2 integration (automate reconciliation, load payroll/commissions/taxes). Next: Emiliano Bond sends account inventory + avg monthly transactions; Esteban prepares proposal and may coordinate an in-person Caracas session.

- **Reunión con Tesote (Dialca / food distributors)** — 2026-10-14, organizer: nicolas.rossini@tesote.com, 49 min
  Group of 4 food distribution companies. ~10 bank accounts, 100–120 daily payments, 4–5 daily manual balance checks + Dynamics conciliation. Tesote presented consolidated view, programmable reports, pre-reconciliation, Dynamics API/template. Next: meeting Mon at 2:30pm with Accounting and Collections; Nicolás prepares business case.

- **Intro: Neovalores // Tesote** — 2026-10-14, organizer: carlos.melian@tesote.com, 25 min
  Investment promoter; multiple accounts in Banco Activo, Plaza, Vanesco, Sofitasa, R — only some active. Wants secure multi-user access without sharing keys. Agreed on a basic read-only proposal at adjusted price, review after 6 months. Next: Nicolás sends proposal.

- **Conversación Comercial: Tesote // POS Venezuela** — 2026-10-14, organizer: nicolas.rossini@tesote.com, 13 min
  Negotiated discount: license $650→$500/mo, implementation $3.5K→$3K (split half at signing). Timeline reduced 8→4 weeks. Prepayment discounts offered (5% semi, 10% annual). Client needs internal sign-off from Rory and Angélica. Next: Nicolás sends updated proposal; follow-up call Friday.

- **Discovery: Tesote // Cartago C.A** — 2026-10-15, organizer: nicolas.rossini@tesote.com, 34 min
  Starting with Cartago workspace, then expanding to other entities (some without ERP). Priority: control debits, supplier payments, counterparties. ~1,100 monthly Cachea movements to track. Tesote AI trial proposed. Next: Nicolás receives complete account info; commercial meeting Wed at 10am.

- **Reunión con Tesote (Odoo / Valery replacement)** — 2026-10-13, organizer: esteban.suarez@tesote.com, 24 min
  5 stores migrating to Odoo, replacing Valery. ~25K invoices/month, potentially 3x in December. Accounts: Vanesco, BNC, BdV + Panama/US international. Tesote for bank consolidation + POS code matching + Odoo pre-reconciliation. Next: discovery meeting Thu at 10am; client sends account inventory.

- **Tesote // Viva Supercentro** — 2026-10-13, organizer: esteban.suarez@tesote.com, 16 min
  1,150+ weekly invoices, 200+ suppliers, manual SAP processes (TXT files, duplicates, multiple steps). Interested in Tesote + SAP API integration; asked about payment execution (Tesote doesn't do that yet). Reverón module (beta) for projections discussed. Priority: BNC (highest outgoing payments). Next: technical meetings to be scheduled; Esteban sends brochure.

---

### CX / Implementation — Banking Connections

- **Purolomo // Tesote** (2 sessions: Oct 16 ~2h, Oct 14 ~1h) — organizer: keyla.hernandez@tesote.com
  Oct 14: Provincial + 2 Banesco users synced; BdV being connected via SMS on Ana's phone; auto-sync 3x/day (6:30am, noon, 4pm). PDF statements not available yet, manual bank download for now. Oct 16: María onboarded (Chrome recommended). Provincial + Banesco automated; BdV on Tecno phone but SMS only arrive when app is open — considering migration to Samsung corporate phone. Sync schedules set: 06:00/09:00/12:00/18:00/23:00. Phase 1 testing limited to Puro Lomo + Daterra (no PDFs). Next meeting: Tue at 2pm, priority: automating BdV.

- **Tesote <> Cines Unidos: Automatización de token** — 2026-10-16, organizer: yorleny.merette@tesote.com, 25 min
  Mercantil QR linked, device named. Sync has been failing for a week — no notification/token arrived, process hung ~3 min then connection error. Mercantil may have ~5K monthly transactions. Next: Yorleny rechecks config; Yimi retries sync in 10 min; if error persists → escalate to engineering via WhatsApp.

- **Mesa de Trabajo: Crixto // Tesote** — 2026-10-16 (presencial), organizer: keyla.hernandez@tesote.com, 88 min
  Stabilizing banking connections: Banco Activo down since Oct 1; Banplus needs new credentials; Caroní may start with manual uploads. Plaza and Bancaribe heading toward API integrations (Santiago = Tesote tech contact). SMS Forwarder tested on Android. Odoo native connector: T-2 close/verify cadence, validates movements vs. final balances. New interface mandatory Oct 31; weekly meetings Thu 3–4pm for 4 weeks. Next: Esteban sends Odoo commercial proposal.

- **Control de Avances: Protinal // Tesote** — 2026-10-15, organizer: keyla.hernandez@tesote.com, 44 min
  Sync interrupted since Oct 7; BdV fixed via credential change + manual sync + reactivation of auto-processes. 179 transactions pending since Oct 1 — status must change to "complete" after new syncs. API running once/day at 8:30am temporarily. Before escalating incidents: validate in Tesote (last sync, credentials, tokens, alerts, account status). Next: María José analyzes cursors + repeated calls + old periods; sends flowchart and API recommendations.

- **Reunión de Kick Off: Industrias Iberia // Tesote** — 2026-10-15, organizer: keyla.hernandez@tesote.com, 63 min
  Phase 1: bank connections + auto-sync. Phase 2: categories/counterparties/auto-classification. Phase 3: consulting + change mgmt. Phase 4: Sage conciliation file. Priority banks: Mercantil, Banesco, BNC, Provincial, BdV Exterior, Banflu. BNC needs corporate form + signature. Goal: eliminate Denisse's manual bank downloads, enable liquidity/cash flow queries, daily Sage consolidated file (prior day close). Next session: Tue at 2pm.

- **Mimesa // Tesote (Sesión Técnica - Archivo Sage XRT)** — 2026-10-15, organizer: keyla.hernandez@tesote.com, 81 min
  Tesote consolidates connected bank data into single daily file for Sage XRT. File format: date, reference, concept, amount, movement type, RIF, bank, account number, currency (+ transaction code when available). Sage calculates balances from movements. Evaluating Excel vs. CSV vs. fixed TXT. Pilot: STF-selected banks for 1–2 weeks, then expand. Yelitze (Tesote) to enable test environment and adapt SAGE converter. Next: Elena defines pilot banks; Tesote sends format and schedule.

- **Reunión de Kick Off: Aduserca // Tesote** — 2026-10-14, organizer: keyla.hernandez@tesote.com, 47 min
  Contract sent via DocuSign; RIF confirmation pending. Phase 1: Provincial, BdV, Mercantil, Banesco, Bancaribe via consultation users; BNC needs per-company forms + signature (5–7 days). Next session Wed at 10am — requires signed contract, processed billing, users created. API docs being sent to Douglas for demo testing; data will feed Quimix and potentially JD Edwards.

- **Configuración de Conexiones Grupo Oseo** — 2026-10-14, organizer: joan.gonzalez@tesote.com, 92 min
  Reviewed bank access config, generic corporate-phone users with limited privileges. New Tesote interface mandatory from Oct 31. Sync: last 10 days, manual or auto 3x/day (7:30am, 11am, 6pm); 24h to apply changes. Vanesco + Provincial: no token. Banca Amiga + Mercantil: SMS codes. Android APK for auto SMS forwarding tested. 20 active accounts limit. Next meeting: Tue at 2pm; Joan sending categories proposal.

- **Configuración de conexiones La Wawa // Tesote** (2 sessions: Oct 13 ~106 min, Oct 14 ~21 min) — organizer: joan.gonzalez@tesote.com
  Oct 13: Alejandro granted Indriani permissions; Vanesco uses SMS tokens; Ban Plus pending 2 of 4 security questions; BNC needs signed corporate form + bank exec contact (Joan investigating). App tested with Vanesco + Bancamiga. Next: categorization/counterparties session. Oct 14 (follow-up): Ban Plus security questions pending; auto-sync scheduled; reminder set for OnePlus sync.

- **Check In Covencaucho // Tesote** — 2026-10-14, organizer: joan.gonzalez@tesote.com, 54 min
  7 banks connected, 48 accounts synced, 8K+ transactions in September, 70.5% auto-classification, 3-schedule syncs. API with Idenpier working; SMS Forwarder on corporate phone. Automation freed half a day for reconciler; 100% auto-classification of bank commissions achieved. Mercantil + Vanesco still have faults requiring manual sync. New interface mandatory Oct 31. Next: bi-weekly afternoon meetings; Joan sends invitation.

- **Revisión de Conexiones Covencaucho** (2 sessions: Oct 13 ~23 min + Oct 13 ~11 min) — organizer: joan.gonzalez@tesote.com
  Oct 13 (longer): Mercantil configured via Entros QR; Vanesco + BdV already active → 3 banks integrated. Counterparties file updated; API working for conciliation including commission assignment. Commission rules adjusted for apostrophes; reject condition being considered. Oct 13 (shorter): Mercantil setup coordination; Vanesco + BdV configured for auto-conciliation; sync timing discussion (noon vs. EOD).

- **CS Meeting: Proalpo (Marsoca) // Tesote** — 2026-10-13, organizer: estefany.gonzalez@tesote.com, 39 min
  Updated + synced bank connections; Ingrid designated as master user. Pending: Provincial, Sofitasa, BDT, Mercantil Panama (missing credentials/users); inventory to be sent for missing accounts. SMS Forwarder to be implemented on Infinix Android 15. Creating rules/categories/counterparties for auto-classification. Possible separation of Proalpo and Marzoca spaces. Next: Tue Oct 20 at 10am for onboarding + automation.

- **Marsoca (Proalpo) // Tesote** — 2026-10-14, organizer: estefany.gonzalez@tesote.com, 23 min
  User permissions defined: Ingrid + Eliana = standard; Roberto + Juan Peña = master only. Both companies in same workspace (also Piemonte); unified categories. Token automation: Android corporate phones needed for SMS. Mercantil Panama + Vanesco Panama + BPO available; Sofitasa Venezuela still in process (last update Oct 9). Odoo integration possible; Confía has no API. Auto cash position report once connections stabilized. Bi-monthly joint meetings agreed. Next: Estefany organizes Proalpo token session; Roberto evaluates Odoo admin implementation.

- **Configuración de Conexiones: Purolomo // Tesote** — 2026-10-14, organizer: keyla.hernandez@tesote.com, 66 min
  Provincial + 2 Banesco users synced (10-day initial recovery). BdV processing multiple company accounts via Ana's credentials + SMS token. José Luis retains admin of connections/security. Auto-sync planned 3x/day: 6:30am, noon, 4pm; 48-hour reviews to detect reference changes and avoid duplicates. BdV auth to change from AMI to SMS. PDF statements not yet available. Next session: Fri at 2pm.

- **Tesote <> Sizuca: Automatización de tokens** — 2026-10-14, organizer: yorleny.merette@tesote.com, 25 min
  Starting automation with BdV (credentials need update first to avoid lockouts). José (master) to grant Angélica permission to change credentials independently. SMS Forwarder installed on Samsung A5 (Play Protect adjusted). Mercantil Panama = only recent sync; BNC = 6h ago; Vanesco = up to 4 months without activity. Incorrect credentials in Banca Amiga, BdV, Vanesco, Mercantil. Dollar accounts not visible; manual accounts not syncing. Next: update credentials, verify; escalate tech discrepancies if they persist.

- **Conexiones Corporación JSL** — 2026-10-13, organizer: joan.gonzalez@tesote.com, 47 min
  Mercantil: credential issue fixed (new user "Luis", uppercase C password); app linked via QR, SMS + camera permissions enabled, auto-sync now active. Ban Plus: 4 security questions registered, bank updated and functioning, 3x/day auto-sync configured. Joan to follow up with Marta.

- **CS meeting: Marcas Propias // Tesote** — 2026-10-13, organizer: estefany.gonzalez@tesote.com, 43 min
  BNC token expired — following up with Team Pagos + Latín Pago. Mercantil + BAN tokens failing on Android (phone change). Sync scheduled from 6:00am, cash position report by 7:00am — Mercantil must be updated manually until automated. Daily report configured with all currencies and companies. Next meeting: Oct 28 to onboard new users and train on SOTE.

- **Rebeca Triana Cannilla <> Laboratorios Kimiceg** — 2026-10-13, organizer: rebeca.triana@tesote.com, 11 min
  Bancaribe connection error: fixed by having Armando delete 40 stored security coordinates, reload only the requested ones. 2 accounts now reading correctly with transactions. Agreed: delete old answers before adding new ones; incremental flow for future incidents. Auto-sync at 8am remains active.

- **Implementación: Grupo Santa Teresa // Tesote** — 2026-10-15, silent meeting, no summary
- **CS meeting: Corporación Inveca // Tesote** — 2026-10-13, silent meeting, no summary

---

### Product / Integrations / Engineering Signals

- **Tesote // Grupo Abreu** — 2026-10-15, organizer: esteban.suarez@tesote.com, 46 min (Luis attended)
  Bank connection status: BdV, Mercantil, Vanesco active; Bancaribe limited to last 15 movements (full API next quarter). Sync proposal: saldos 7:00–7:30am, transactions after 8:00am. Mercantil + Vanesco: ~1 min connection time, front-end may show up to 64 min. **Mobile payment real-time validation (Mercantil + Cachea) flagged as priority.** Banfan: no formal communication yet. Commercial proposal pending approval.
  Action for Roberto Drew-Bear: investigate Mercantil API for mobile payment validation; ensure token automation for Mercantil + BdV.

- **Tesote // Promaker - Conexión Odoo** — 2026-10-15, organizer: nicolas.rossini@tesote.com, 12 min
  Two integration paths: (1) Tesote native connector — T-2 lag, Tesote manages data cleaning + first transfer; (2) partner-maintained API — partner controls query frequency + maintenance. Nicolás recommends API due to Corpureca involvement. Decision still pending with Luis Acosta (Promaker). Production planned: week after Nov 16. API: $350/mo; connector: $550/mo. Luis Acosta to decide by Monday with Nicolás.

- **Tesote <> Promaker: Customer Success Check-In** — 2026-10-13, organizer: yorleny.merette@tesote.com, 46 min
  Token sent to external Odoo integrators for integration testing. Categorization rules for freelancers being evaluated (exclude from "salaries" category). **Transaction order issue in downloaded reports (especially Cachea account) — being investigated.** Connection bug in transactions module for uncategorized counterparties (found by Brian). Monthly check-ins agreed. Action: Yorleny to resolve transaction order issue and fix counterparty connection bug.

---

### Marketing / Brand

- **Weekly Marketing Brief (Roam)** — 2026-10-13, host: Veronica Alvite, 3 participants, 23 min
  Startup Summit: Mavo building content plan from engagement/click data; want higher posting cadence before + during event. Alliance announcements (Corpo Breka approved — Mavo to post on LinkedIn + Instagram). WhatsApp message differentiation per ad for HubSpot lead attribution. Accounting-closure campaign: 4 pieces (chaos without Tesote vs. ordered office with Tesote) — agency to send budget + timeline this week; low December commercial activity noted. Veronica wants LinkedIn strategy with blog article repurposing; Roberto to share SEO report. KPIs proposal in progress (Veronica).
  **Startup Summit escalation:** organizers haven't responded to Veronica; Luis's participation details unclear. Roberto said he'd write to Luis to escalate.

- **Tesote - Nugget** — 2026-10-15, organizer: mavo.vivas@tesote.com, 46 min
  First official Tesote audiovisual campaign: video ads for social + cinema. Format: sober financial satire targeting treasury/accounting/CFO personas. One main video + 4 episodes (20–45 sec), subtitles mandatory, real Tesote UI, original material, no stock animation. Nugget Films as production agency (guión through post). Timeline: proposals received before Oct 20, production in November, launch first half of December. Evaluation criteria: ICP understanding, script quality, budget, production capacity, tone. Veronica reviews proposals; Mavo coordinates.

---

### Churn / CX Risk

- **Binaural + Tesote** — 2026-10-13, organizer: estefany.gonzalez@tesote.com, 28 min
  **Client canceled subscription.** Reason: competitor offered a better financial deal. Helen Bullones praised service and support. Key people (Gustavo, Manuel) were absent — evaluation was partly stalled. Tesote had automated complex BdV reconciliation (3 references), Bancamiga, and Bicentenario rules. Estefany to keep contact via email marketing; Helen will share details on alternative proposal when available. **Tesote needs to learn more about what competitors are offering to avoid future surprise churn.**

---

## Coverage

- **Roam** = Luis's personal calls only (personal token). Returned 1 meeting this week.
- **Fireflies** = org-wide (admin access). Returned 39 meetings this week.
- **Deduplication**: 0 overlaps detected between sources (the Roam marketing brief did not appear in Fireflies).
- **Total unique calls**: 40.
- **Gap**: purely-internal Roam syncs between teammates Luis wasn't in are not captured unless Fireflies recorded them. 2 calls were silent/no-transcript (Grupo Santa Teresa, Corporación Inveca) and counted but not summarized. 1 call (Reunión con Tesote / Dialca Oct 13) was a short silent re-run.
