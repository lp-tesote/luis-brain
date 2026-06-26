---
title: Team calls — week of 2026-06-22
tags: [team-calls, weekly-digest, fireflies, roam]
updated: 2026-06-26
window: 2026-06-22 .. 2026-06-26
---

## Needs Luis's attention

- [ ] Make landing page interactive — from "Operator AI, Product Demo, and Launch Planning" (2026-06-24)
- [ ] Send Reverón pitch deck + visual materials to Roberto for review — from "Avances Reverón, estrategia de pitch y coordinación bancaria" (2026-06-22)

---

## By workstream

### Product / AI & Reverón

- **Operator AI, Product Demo, and Launch Planning** — 2026-06-24, Luis + Daniel Francoeur, ~unrecorded
  Reviewed PRD in Notion; recent production changes unblocked dev. Discussed AI agents for AP/AR/treasury with gated workflows + audit logs for compliance. Covered SSO fixes, local env setup, and demo prep strategy. Bank API integration progressing; AI usability and cron QA in flight. Landing page next, then launch.
  *Key decisions:* Luis makes landing page interactive; Daniel delivers EOD status + finishes cron QA + determines dashboard scope for launch.

- **Avances Reverón, estrategia de pitch y coordinación bancaria** — 2026-06-22, Luis + Roberto Drew-Bear, ~unrecorded
  Luis debriefed on Caracas meetings and VZ corporate market sizing. Discussed Reverón differentiation vs. competitors, external AI model integrations, Tesote architecture. Agreed to minimize bank-connection errors before launch. Planned to review lost deals and train Nicolás on Discovery. Andrés González comp package flagged — Roberto to coordinate with Jennifer for adjustment.
  *Key decisions:* Luis sends Reverón pitch + visuals to Roberto; Roberto coordinates Banco Plaza + BanPlus API meetings (loop in Stefi); Roberto/Jennifer adjust Andrés's comp.

### Banking Migration / Customer Success

- **Client Integration Process and Next Steps** — 2026-06-22, 3 participants (Roberto, Santiago + client), Roam
  Short sync on sharing info for Valles del Turbio and BT app integration. Clients must contact their bank exec to request service and run tests. Santiago escalating API support issue to Dani + André, will update via email. Roberto sent WhatsApp number format instructions via Slack.

- **Grupo Rica // Tesote** — 2026-06-23, Estefany González (organizer), 50m
  Migration + automation of bank connections: Bancaribe and UNESCO migration underway since Aug 2023. Mercantil automation via token + Google Authenticator in progress; API migration planned for next week. AI reporting tools launching in 2–3 weeks; >90% transactions auto-categorized. Issues: duplications in reconciliation, Mercantil data refresh lag. Client needs: Android device for token automation, signed Mercantil planillas, updated Odoo chart of accounts + contacts.

- **Configuración de Conexiones: Consorcio Ragnar // Tesote** — 2026-06-23, Joan González + Estefany González (Tesote), 45m
  Working through bank connection setup: Banco de Venezuela needs Android device + APK for SMS tokens. Some Tesote user accounts not activating due to missing permissions. BNC connection confirmed; BNC planillas being filled. Discussed ERP category normalization for multilevel import. US bank accounts require master user.
  *Follow-ups:* José Pinero to complete all bank user accounts + update shared Google Sheet; send multilevel category list; complete BNC planilla. Estefany/Joan: resolve permission issues, provide category import template.

- **Customer Success Meeting: Grupo Mimesa // Tesote** — 2026-06-22, Estefany + Joan González (Tesote), 46m
  Banco MAR sync issue requires manual unblock. Suggested running Tesote app in background for better SMS token reception. Friday 10am follow-up set with Yeilin + Jaycee. Categories/counterparty proposal from May 29 to be re-sent; Elena excluded from this phase.
  *Follow-ups:* Estefany to send Friday invite, reinvestigate Banco Plaza + BDV sync failures, re-send May 29 categories proposal.

- **Binaural // Tesote (Categorización)** — 2026-06-22, Estefany + Joan González (Tesote), 57m
  Only Banco de Venezuela + Bancamiga operational; Facebank and VOF failed due to limited permissions. Odoo category sync inconsistencies flagged — need automatic rules for better assignment. Counterparty management feature demoed. Reconciliation must cross on RIF + amount due to reference discrepancies. Odoo connector link to be sent.
  *Follow-ups:* Helen Bullones to send counterparty list (name, RIF, email) + validate category/rules proposal. Estefany to build auto-rules proposal, schedule training session, send Odoo connector link.

- **CS Meeting Mensual: Victum Legal // Tesote** — 2026-06-22, Yorleny Merette (organizer), 39m
  Stephanie Murillo onboarding as new platform admin. Currently only Rodrigo + partner use Tesote for balance checks — expanding to reconciliation + automation. Daily auto-sync scheduled for 7–8am. Bulk category/counterparty load planned; automation rules next after Stephanie reviews data.
  *Follow-ups:* Rodrigo: send chart of accounts + client/vendor list. Yorleny: configure Mercantil + BanPlus token auto-sync, send meeting notes.

- **CS Meeting Mensual: CALA // Tesote** — 2026-06-25, Yorleny Merette + Carolina Diaz (LABCALA), 12m
  Silent meeting — Fireflies recorded but no transcript available (summary_status: skipped).

### Sales Pipeline

- **Intro: Iberia // Tesote** — 2026-06-22, Carlos Melian + Esteban Suárez (Tesote) + Martha Fuentes + Edgardo (Iberia), 1h 14m
  Strong intro. Iberia runs 18 banks — currently manual. Tesote pitched: 3× daily auto-refresh, MFA + automated token handling, multi-currency/multi-entity dashboard, SAGE ERP integration. Good reception. Next step: operational deep-dive with treasury + accounting + systems teams to deliver technical proposal + timeline.
  *Follow-ups:* Martha to send treasury/systems contacts + SAGE format template + bank inventory. Esteban to send client list + bank inventory sheet + coordinate ops meeting.

- **Discovery: Ferretotal // Tesote** — 2026-06-23, Esteban Suárez (organizer) + Carlos Melian + Roberto (Tesote), 41m
  Pitched automation of multi-currency, multi-bank balance consolidation (4× daily updates). Covered bank statement normalization, SAP reconciliation automation, and role-based permissions. Strong interest. Next: Esteban to send Excel bank inventory template; Ferretotal (Carolina Jaramillo + Diego Méndez) to fill and return; Esteban to prepare proposal + schedule presentation with Andrés + Erika.

- **Customer Success Meeting: Grupo Mimesa // Tesote** *(see Banking/CX above)*

- **Tesote // Ximple** — 2026-06-22, Nicolás Rossini + Lisbeth Vicente (Ximple), 12m
  Intro/first call. Ximple has 5–10 person team doing daily balance checks across banks + accounting in Citrus via Excel. Pitched Tesote dashboard + pre-reconciliation automation via API. Positive reception. Nicolás to send demo, contract template + formal proposal for Lisbeth to share with leadership. Follow-up meeting set for next day.

- **Propuesta: Tesote // Ximple** — 2026-06-23, Nicolás Rossini + Lisbeth Vicente, 12m
  Follow-up to Jun 22 intro. Silent meeting — no transcript (summary_status: skipped).

- **Propuesta: Tesote // Alivensa** — 2026-06-22, Nicolás Rossini + Karla Rodríguez (Alivensa), 20m
  Proposal presented. Karla flagged economic viability concerns in current context; compared Tesote cost vs. Odoo (Odoo cheaper). Nicolás committed to adjusting proposal. Digital proposal to be sent; Nicolás to follow up Friday.
  *Risk:* price sensitivity — may need tiered or scaled pricing to close.

- **Propuesta: Tesote // Cero Cien Ingeniería** — 2026-06-23, Nicolás Rossini + Berrios (Cero Cien), 11m
  Short call — Vladimir (key decision-maker) absent. Berrios (tech, ex-Toyota clients) engaged and supportive. Meeting needs to be rescheduled with Vladimir included. Nicolás to coordinate.

- **Intro: Alimentos Santoni // Tesote** — 2026-06-22, Carlos Melian + Nicolás Rossini, 18m
  Silent meeting — no transcript available.

- **Rebeca Triana <> KATHERINE OJEDA (PLAN B)** — 2026-06-23, Rebeca Triana, 14m
  Silent meeting — no transcript available.

- **Rebeca Triana <> EDUARDO GONZALEZ (Farmacias San Ignacio)** — 2026-06-22, Rebeca Triana, 13m
  Silent meeting — no transcript available.

---

## Coverage

Roam = Luis's calls only (personal token — no org-wide view). Fireflies = org-wide (admin token, no mine/participants filter).
Gap: internal Roam syncs between teammates that Luis wasn't in are not captured here.

- **Roam:** 3 calls
- **Fireflies:** 15 calls
- **Deduped:** 0 overlaps found
- **Total unique calls:** 18
