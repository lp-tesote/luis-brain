---
title: Team calls — week of 2026-06-08
tags: [team-calls, weekly-digest, fireflies, roam]
updated: 2026-06-10
window: 2026-06-08 .. 2026-06-10 (mid-week snapshot — full week closes Fri 2026-06-12)
---

> Mid-week test snapshot. The Friday 5pm routine will re-run and overwrite this with the full Mon–Fri week.

## Needs Luis's attention

Action items assigned to or suggested for you (from your Roam calls):

- [ ] **Prepare mass communication to clients re: bank-connection changes** — from "Operational Bottlenecks / Client Strategy" (2026-06-10)
- [ ] **Write to Gustavo to push Broward's implementation fee this month** — from "Actualización comercial y técnica" (2026-06-10)
- [ ] **In-person meeting with Grupo Rica** (upsell + transition pitch) — from "Arranque transición bancaria" (2026-06-10)
- [ ] **Decide the bank-integrations comms channel** (reuse vs new for API integrations) — from "Arranque transición bancaria" (2026-06-10)
- [ ] **Lock a tentative AI launch date** (align Dan / Sebastián / Majo) — from "Lanzamiento y estrategia de Tesote AI" (2026-06-09)
- [ ] **Share the AI-launch planning doc** so each dept identifies its tasks — from "Lanzamiento y estrategia de Tesote AI" (2026-06-09)
- [ ] **Organize the bank-API transition meeting** (define initial client/bank batch) — from "Lanzamiento y estrategia de Tesote AI" (2026-06-09)
- [ ] **Coordinate the all-teams alignment meeting** for launch — from "Lanzamiento AI: Estrategia, Deals y Coordinación" (2026-06-08)
- [ ] **Send the support video for the Conozoil deal** — from "Lanzamiento AI: Estrategia, Deals y Coordinación" (2026-06-08)

---

## By workstream

### AI launch & web/dashboard redesign (internal strategy)

- **Lanzamiento y rediseño de Tesote: estrategia y comunicación** — 2026-06-10, 3 people (Roam). Walked the new dashboard + web/app redesign; AI + new web targeted for **July 1**; pricing/model for new products aimed at high-value clients; defined client-comms plan. Last session with John & Dan to be scheduled after the 15th.
- **Lanzamiento Tesote AI y transición a APIs bancarias** — 2026-06-10, 12 people (Roam). All-hands on launch posture: usage-limited AI to drive sales, marketing/CX/sales prep, dashboard relaunch, bank-API migration framing, contracts (Mercantil/Provincial weight).
- **Lanzamiento y estrategia de Tesote AI** — 2026-06-09, 6 people (Roam; Esteban, Majo, Estefany, Vero, Roberto). AI rebuilt as standalone product; launch = queries over Tesote data + aggressive marketing; usage-based pricing; QA is the gate; technical separation so AI can't affect core.
- **Prioridades de marketing y lanzamiento de nueva web** — 2026-06-09, 2 people (Roam; Vero). Marketing email deliverability/spam → separate domain + warming (Esteban); onboarding PDF reused for sales; Vero to build employee-onboarding doc; data-driven marketing direction.
- **Lanzamiento AI: Estrategia, Deals y Coordinación** — 2026-06-08, 2 people (Roam). Launch strategy, segmentation, upsell; simplify contracts/subscription terms; intrigue campaign + free trials; deal support (Sana, Cructísimo); sales/post-sales staffing gaps.

### Finance & fundraising

- **Planificación financiera y opciones de financiamiento** — 2026-06-10, 2 people (Roam; Mariel). Break-even + financial cycle; **$300–400k cash reserve**, ~$100k more to burn to break-even; financing via credit lines (prefer over dilution), investors willing to add **$150–200k**, ideal raise $200–300k. Mariel correcting cash-flow + P&L projection to year-end. → ties to [[financial-operating-plan-2026-06]].

### Ops, team & client strategy

- **Operational Bottlenecks, Client Strategy & Team Morale** — 2026-06-10, 2 people (Roam; Esteban). Candid: overwhelm from bank-connection issues + big-client complaints; need a dedicated collections person; implementation-as-sales-extension w/ incentives; finance bottlenecks → internal automation project; SAP integration proposal + pricing; morale after recent losses.

### Banking migration & connections

- **Arranque y estrategia de transición bancaria para clientes** — 2026-06-10, 5 people (Roam). Formal kickoff of the bank-API transition project; client prioritization by company×bank (Provincial/Mercantil/Banesco/Bancaribe); most clients OK with T-1 data; automate planilla filling; per-client strategies (Kasea, Kangur, Grupo Rica, Jumpy, Grupo Abreu, Yomi, Leiros).
- **Marcas Propias // Tesote** — 2026-06-10, Keyla. Critical sync breakage: **Banesco killed SMS auth → token-based** (breaks auto-sync); Mercantil UI changes hit the connection. Ongoing eng follow-up; inactivate unlinked accounts.
- **Configuración de Conexiones: Prevaler // Tesote** — 2026-06-10, Keyla/Estefany. Prevaler connected to Exterior + Mercantil; pending BDV, Bancaribe, BNC; Marta handling read-only user creation w/ Estefany support.
- **Consultoría: Besser Solutions // Tesote** — 2026-06-10, Keyla. BNC pending confirmation, Mercantil needs final approval; auto-sync at 8am/1pm/5pm; permissions + daily recon process.
- **CS Meeting: Cencozotti // Tesote (presencial)** — 2026-06-09, Yorleny. Token automation for Mercantil + BDV (Android-only app on key users' phones, background permissions); sync intermittency; Odoo integration to cut IT load ~80%.
- **Tesote // Mimesa (Conexiones Bancarias)** — 2026-06-08, Keyla. Multi-bank user sync; tokenless auto-connect working for Banesco Panamá + Mercantil Panamá; Banesco VE still manual; align categories Tesote↔Sage.
- **Control de Avances: FSI // Tesote** — 2026-06-08, Keyla. Rule optimization 190→96 to cut categorization latency (30–40min); RIF-based counterparties for transfers; auto-cleanup of archived rules; push for API to fix sync intermittency.

### New business — discovery & proposals

- **Intro: Robin Agency // Tesote** — 2026-06-10, Luisana. Auto balance refresh (8am/noon/EOD), accounts + transactions modules, accounting/AI tie-in; next = account inventory + follow-up.
- **Propuesta: Tesote // Brilux** — 2026-06-10, Nicolás. 70+ accounts (Banesco/Mercantil), Dynamics 365 via API; **$7k impl + $3,500/mo**, 3-phase over 8 weeks; ROI framing for board.
- **Marcas Propias** — (see Banking).
- **nicolas.rossini — Untitled** — 2026-06-10, Nicolás. Odoo impl starting the 16th → mid-Oct, aligned w/ Tesote; demo to María Alejandra; **$5k + $2.5k/mo** (budget-flexible).
- **Intro: Esimeca // Tesote** — 2026-06-10, Nicolás. ~150 clients pitch; Sineca (metalworking) already has internal recon; interested in cash-flow-by-project visibility.
- **Discovery: Grupo AG Vicson // Tesote** — 2026-06-10, Esteban. Mercantil/Banesco automation; API up to 3×/day (Mercantil limited); option to integrate without Mercantil; on-site support in Valencia.
- **Tesote // La Oriental de Seguros** — 2026-06-10, Nicolás. Regulated insurer, $10–15k/mo revenue; staged 3–6mo proposal to fit their finances.
- **Discusión Comercial: Consorcio Ragnar // Tesote** — 2026-06-10, Esteban. Impl starts Mon the 15th (Keyla leads, Alexander = tech contact); **$1,750/quarter** indexed to BCV; read-only bank users.
- **Tesote - Proveedor** — 2026-06-09, Esteban. Platform pitch to extended IT + Treasury team; Dynamics 365 integration not yet available — evaluate security/architecture.
- **Reunión de Kick Off: Corporación Inveca // Tesote** — 2026-06-09, Keyla. Phased impl, 5 banks validated, controlled access; contract signed + invoice sent.
- **Propuesta: Tesote // Solinvet** — 2026-06-08, Nicolás. Pain = migration to Profit AU + no Odoo sync; 99.5% data-match pitch + AI reporting agent; internal review w/ Verónica.
- **Intro: Cidata // Tesote** — 2026-06-08, Carlos Melián. Recon automation 300→12-20 unreconciled/day; Odoo flows; ~26k ops/mo (BDV primary); **$15–24k/yr + $5k impl**.

### Customer success & implementation (existing clients)

- **Tesote <> Grupo Landa: CS Meeting** — 2026-06-10, Yorleny. Recon module (beta) demo; multi-company/account filters needed; future ERP API; live sync-support sessions; moved comms off WhatsApp to a formal channel.
- **Fivenca <> Tesote** — 2026-06-10, Estefany. Internal daily FX rates (set 7,562 Bs/USD); balances still show BCV rate — work to reflect internal rate; bulk historical-rate load; automate rate registration.
- **Customer Success Meeting: Viva Super Centro // Tesote (API)** — 2026-06-10, Estefany. Read-only DB access for SAP Business One + Power BI; API docs shared; auto-classification target 70%; native SAP B1 module early-stage.
- **Implementación: Inquiport, S.A // Tesote** — 2026-06-08, Keyla. SAP integration — transactions w/ categories + counterparties; avoid duplicates via unified masters + prefixes; external ID linking accounting accounts.
- **(Presencial) CS Meeting: Hispana de Seguros // Tesote** — 2026-06-08, Estefany. Silent/in-person — no transcript captured.
- **Discovery: Envases CHC // Tesote** — 2026-06-08, Esteban. Silent/in-person — no transcript captured.

---

## Coverage

- **Roam** = Luis's calls only (personal token, no org token) — 10 calls this window (incl. 1 trivial reschedule, omitted above).
- **Fireflies** = org-wide (Luis is admin) — 24 calls this window across the team (Estefany, Keyla, Nicolás, Esteban, Yorleny, Luisana, Carlos).
- **Deduped:** 0 overlaps (Roam = internal strategy; Fireflies = client-facing — disjoint this week).
- **Gap:** purely-internal Roam syncs between teammates Luis wasn't in are not captured (no Roam org token). 2 Fireflies calls were silent in-person sessions with no transcript.
