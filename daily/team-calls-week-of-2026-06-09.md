---
title: Team calls — week of 2026-06-09
tags: [team-calls, weekly-digest, fireflies, roam]
updated: 2026-06-11
window: 2026-06-09 .. 2026-06-13
---

## Needs Luis's attention

- [ ] Prepare mass communication for clients about bank connection changes — from "Operational Bottlenecks, Client Strategy & Team Morale" (2026-06-10)
- [ ] Write Gustavo to close Broward implementation fee this month — from "Actualización comercial y técnica Tesote" (2026-06-10)
- [ ] Schedule in-person meeting with Grupo Rica for upsell + banking migration — from "Arranque y estrategia de transición bancaria" (2026-06-10)
- [ ] Define and set up comms channel for bank API integrations (existing vs new channel) — from "Arranque y estrategia de transición bancaria" (2026-06-10)
- [ ] Confirm Jul 1 launch date for Tesote AI with Dan/Sebastián/Majo — from "Lanzamiento y estrategia de Tesote AI" (2026-06-09)
- [ ] Share launch planning doc so each department maps their tasks — from "Lanzamiento y estrategia de Tesote AI" (2026-06-09)
- [ ] Organize banking API migration batch meeting (may be done — meeting held Jun 10) — from "Lanzamiento y estrategia de Tesote AI" (2026-06-09)
- [ ] Send phased proposal to La Oriental de Seguros (3–6 month ramp, fits their budget) — from "Tesote // La Oriental de Seguros" (2026-06-10)

## By workstream

### Product / AI Launch & Website Redesign

- **Lanzamiento y estrategia de Tesote AI** — 2026-06-09, 6 people (Luis, Esteban, Majo, Estefany, Verónica, Roberto)
  AI rebuilt as standalone product. Launch focus: queries over Tesote data, aggressive marketing, usage-limit pricing model. QA is the gate. Banking migration comms to be decoupled from AI launch. Next: define date, distribute launch planning doc, prep client incident list.

- **Lanzamiento Tesote AI y transición a APIs bancarias** — 2026-06-10, 12 people (full team all-hands)
  Presented new dashboard/web redesign + AI launch strategy to full team. Banking API migration status covered; client communication plan agreed. Mercantil + Provincial are key banks. Physical team presence needed for launch week. Last session with John & Dan to be scheduled after Jun 15.

- **Lanzamiento y rediseño de Tesote: estrategia y comunicación** — 2026-06-10, 3 people (Luis, Estefany, external)
  Deep-dive on new dashboard: balance visualization by bank/account, AI summaries, intercompany transfers, cash flow categorization. Jul 1 launch confirmed. Estefany building power-user list + selecting channels for client communication.

- **Prioridades de marketing y lanzamiento de nueva web** — 2026-06-09, 2 people (Luis, Verónica)
  New website reviewed (benchmark-driven design). Priorities: design, narrative, positioning, case studies. Onboarding PDF repurposed for sales. Verónica to build employee onboarding doc. Esteban to configure marketing email domain + warming.

### Finance / Fundraising

- **Planificación financiera y opciones de financiamiento** — 2026-06-10, 2 people (Luis, Mariel)
  Break-even needs ~$100K more burn; reserve target $300–400K. Prefer credit lines (Mercury, Rogue, Stripe, partner lines) over investor dilution — investors offered $150–200K if needed. 4 pillars for next month: implementation, banking migration, finance, product launch. Need dedicated VZ headcount. Mariel working on cash flow projection + P&L to pin break-even date.

### Banking Migration & CX / Ops

- **Arranque y estrategia de transición bancaria** — 2026-06-10, 5 people (Luis + ops team)
  Kicked off API migration project. Priority clients: Kasea, Kangur, Grupo Rica, JUMPY, Grupo Abreu, Yomi, Leiros. Grupo Rica → in-person meeting needed (upsell + migration). T-1 data confirmed OK for most clients. Automating form-filling agreed; API comms channel to be defined.

- **Operational Bottlenecks, Client Strategy & Team Morale** — 2026-06-10, 2 people (Luis + Esteban)
  Candid debrief. Core issues: bank connection failures → client complaints; finance bottleneck; no dedicated collections person. Plans: mass client communication, economic incentives for implementations, treat implementation as sales extension. SAP proposal to go out (Esteban). Pipeline needs more proposals + refreshed narrative. Morale dip post-client losses — needs active counter.

- **CS Meeting: Cencozotti // Tesote (PRESENCIAL)** — 2026-06-09, 161 min (Yorleny, Estefany + client)
  Long config session on bank token automation (Mercantil, BdV). Android-only app; background permissions complex to set up. Sync intermittency diagnosed live. AI classification + Odoo integration previewed as upcoming value.

- **Reunión de Kick Off: Corporación Inveca // Tesote** — 2026-06-09, 43 min, 6 people
  Implementation kick-off. 5 banks validated for connection. Contract signed + invoice sent. Dennys (Inveca) to validate secondary user permissions + complete BNC form. Roberto to offer demo to new admin.

- **Tesote <> Grupo Landa: CS Meeting** — 2026-06-10, 73 min (Yorleny, Rebeca + client)
  Beta conciliation module demo. Multi-company/account filtering still needed. Bank sync issues acknowledged; live 8am monitoring sessions planned. Formal support channel established (off WhatsApp). Dynamics ERP API integration on roadmap.

- **Marcas Propias // Tesote** — 2026-06-10, Keyla + client
  Vanesco dropped SMS auth → token-only, breaks auto-sync. Mercantil UI changes caused connection issues (transactions syncing OK now). Engineering escalations raised. Inactive accounts to be cleaned up.

- **Configuración de Conexiones: Prevaler // Tesote** — 2026-06-10, 71 min (Keyla, Estefany + client)
  Exterior + Mercantil connected. Pending: BdV, Bancamiga, Vanesco, Bancaribe. Client (Marta) to create read-only users + complete BNC forms. Engineering to review Provincial permissions bug.

- **Consultoría: Besser Solutions // Tesote** — 2026-06-10, 78 min (Keyla + 4 client contacts)
  Config session. BNC pending bank confirmation; Mercantil pending final user authorization. Sync schedule agreed: 8am/1pm/5pm. Client to send counterparts + categories DB.

- **Joan - PTP (MCP training)** — 2026-06-10, 112 min (Majo, Estefany, Keyla + Joan González)
  MCP onboarding session. PowerShell/Cursor install issues resolved. Joan explored demo space, learned category/rule config. Final session with Dan (CTO) scheduled Friday after 16:30.

- **Customer Success Meeting: Viva Super Centro // Tesote (API)** — 2026-06-10, 55 min (Estefany + client)
  Client evaluating API integration with SAP Business One + Power BI. Read-only DB access explained. Native SAP module in early dev. Estefany to send test token + demo credentials. Client to decide: current API path or wait for native module.

- **Fivenca <> Tesote** — 2026-06-10, 18 min (Estefany + client)
  Internal FX rate (7,562 BsD) configured for daily transactions. Rate applies to movements but not yet account balances (engineering WIP). Historical bulk rate upload under evaluation.

### Sales Pipeline

- **Actualización comercial y técnica Tesote** — 2026-06-10, 7 people (Luis + sales team)
  Weekly commercial review. SOC 2 + pentest results positive. New lead: José Ernesto Núñez (FiveX). Open follow-ups: Broward (Luis → write Gustavo), FedEx (last chance), Ragnar (contract closes Mon Jun 15), El Dorado, Grupo Rica, Net 1, Grupo Abreu, Leiros, Kanguro, San Ignacio, Grupo Paraguas (Esteban API follow-up). Yomi + Banesco proposals in motion. Krustísimo + Inveco discount negotiations ongoing.

- **Tesote // La Oriental de Seguros** — 2026-06-10, 42 min (Luis, Nicolás + 2 client contacts)
  Insurance company, $10–15K/month revenue. Interested in centralized treasury + AI. Agreed on phased 3–6 month proposal tied to their growth trajectory. Luis to send escalated proposal.

- **Discusión Comercial: Consorcio Ragnar // Tesote** — 2026-06-10, 14 min (Esteban + client)
  Contract closing: $1,750/quarter BCB-indexed. Implementation kick-off Mon Jun 15 at 11:30. Keyla leads; Alexander is tech contact. Client to provide signatory + RIF.

- **Propuesta: Tesote // Brilux** — 2026-06-10, 39 min (Nicolás + client)
  70+ accounts, Dynamics 365 integration via API. Proposal: $7K implementation + $3,500/month. Board needs ROI blueprint before approving. Nicolás to deliver operational blueprint with ROI scenarios next week.

- **Intro: Robin Agency // Tesote** — 2026-06-10, 30 min (Luisana, Esteban + 2 client contacts)
  Clean intro; treasury automation pitch landed. Andrés (client) to send account inventory. Esteban to prepare commercial proposal.

- **Discovery: Envases CHC // Tesote** — 2026-06-11, 53 min (Esteban, Luisana, Roberto + 2 client contacts)
  SAP + Profit fragmentation → painful manual reconciliation. Pilot to start with Servidane (smaller entity), 3–4 weeks. Rafael visiting Caracas Jun 23 for in-person implementation work.

- **Discovery: Grupo AG Vicson // Tesote** — 2026-06-10, 34 min (Esteban + clients)
  Manual bank statement downloads from Mercantil + Vanesco. API integrations in progress (Mercantil limited). AI for auto-reports pitched. Client to send account inventory; Esteban to follow with proposal + security/API docs.

- **Tesote - Proveedor (KOF / Coca-Cola distributor)** — 2026-06-09, 49 min (Esteban, Roberto + 6 KOF contacts)
  Large enterprise. Tesote + AI presented to IT + Treasury. Dynamics 365 integration not yet available — noted as gap. KOF to review internally before technical sessions. Esteban to send full phased proposal + security documentation.

- **Intro: Esimeca // Tesote** — 2026-06-10, 15 min (Luisana, Nicolás + client)
  Metalmecánica with existing internal reconciliation system. Key ask: project-level cash flow visibility. Vicente to review with admin + IT. Nicolás to coordinate follow-up meeting with both departments.

- **Untitled – Nicolás (Odoo client)** — 2026-06-10, 16 min (Nicolás + client)
  Odoo implementation starting Jun 16, target completion mid-October alongside Tesote integration. Proposal: $5K + $2,500/month. Client (Orlando) to confirm budget in 1–2 days; Nicolás to send full proposal packet.

## Coverage

Roam = Luis's calls only (personal token — no org-wide view). Fireflies = org-wide (admin token, all calls where the bot joined).

Gap: internal Roam syncs between teammates Luis didn't attend are not captured. No Roam↔Fireflies overlap detected — Roam calls are Roam-platform internal meetings; Fireflies calls are Google Meet / Teams external/CS calls.

- Roam: 8 calls
- Fireflies: 18 calls
- Deduped: 0
- Total unique calls: 26
