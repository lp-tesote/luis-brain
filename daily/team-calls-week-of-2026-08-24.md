---
title: Team calls — week of 2026-08-24
tags: [team-calls, weekly-digest, fireflies, roam]
updated: 2026-08-28
window: 2026-08-24 .. 2026-08-28
---

## Needs Luis's attention

Items where Luis is explicitly assigned (Roam `assignedToMe`) or named in Fireflies `action_items`:

- [ ] Contact Patricia de Su Portuguesa re: APIs and OXXO — from "Tesote: estrategia, producto y conexiones" (2026-08-27)
- [ ] Validate Venezuela fiscal/legal structure with lawyers (agent-de-cobro figure, RIF, payroll) — from "Finanzas, crecimiento y estructura de Tesote" (2026-08-27)
- [ ] Model formalization costs: Venezuelan payroll + benefits (insurance, etc.) — from "Finanzas, crecimiento y estructura de Tesote" (2026-08-27)
- [ ] Research insurance/benefits options for Venezuelan team — from "Finanzas, crecimiento y estructura de Tesote" (2026-08-27)
- [ ] Kick off Reverón→Odoo reconciliation automation with Dan + Mariel — from "Finanzas, crecimiento y estructura de Tesote" (2026-08-27)
- [ ] Prepare USD liquidity projection (billing cycle → collection → availability) — from "Proyección de caja y capital requerido" (2026-08-25)
- [ ] Confirm BT account count for correct pricing tier — from "Revisión de deals, Reverón y pricing" (2026-08-27)
- [ ] Follow up on Yumi deal (confirm house discount) — from "Revisión de deals, Reverón y pricing" (2026-08-27)
- [ ] Confirm Fibertel K requirements and send material to Esteban — from "Revisión de deals, Reverón y pricing" (2026-08-27)
- [ ] Follow up on Zinac/Ramiro situation — from "Inventarios, integraciones y acuerdos comerciales" (2026-08-25)
- [ ] Send roadmap, addendum, and follow-up email to [Avances] client (wait for Fireflies transcript) — from "Avances y propuesta comercial del proyecto" (2026-08-25)
- [ ] Activate both workspaces to start sending emails — from "Avances y propuesta comercial del proyecto" (2026-08-25)
- [ ] Send formal collection notice to Protinal and Maralaca (suspend threat) — from "Cobranza y selección de personal" (2026-08-25)
- [ ] Push Caché to pay two overdue invoices this week — from "Cobranza y selección de personal" (2026-08-25)
- [ ] Send new proposal + roadmap to Fernando (upsell: ~$6,900 with Reverón) — from "Nueva propuesta comercial y estado bancario" (2026-08-24)
- [ ] Email Ana/Daniel/Walter re: large opportunity (no-ERP client) — from "Propuestas comerciales y oportunidades" (2026-08-24)
- [ ] Extract representative HubSpot contract (start with Roam example) for finance audit — from "Finance Automation Audit and Platform Strategy" (2026-08-26)
- [ ] Finish investor-facing company blurb — from "Finance Automation Audit and Platform Strategy" (2026-08-26)
- [ ] Schedule Mariel working session on billing ops (first-of-day billing flow) — from "Internal Finance Product Dogfooding Plan" (2026-08-26)
- [ ] List finance-dept problems + ideal solutions (FX, billing, Stripe) — from "Internal Finance Product Dogfooding Plan" (2026-08-26)
- [ ] Deliver Gerais beta access to Reverón within ~1 week — from "Reverón IA: Tesote // Gerais" (2026-08-27)
- [ ] Send formal Reverón deliverable description to Fivenca; coordinate beta test phase — from "Tesote // Fivenca" (2026-08-26)
- [ ] Send Grupo Abreu meeting minutes + work plan + roadmap (coordinate Bancaribe status with Stephanie) — from "Tesote x Grupo Abreu" (2026-08-24)
- [ ] Write to Víctor (Seven) once he joins the WhatsApp group for Reverón feedback — from "Feedback y seguridad de Reverón" (2026-08-24)
- [ ] Send Suzanne (Farmacias San Ignacio) the case-study interview summary — from "Farmacias San Ignacio JT // Tesote" (2026-08-25)

---

## By workstream

### Product & Engineering — Reverón + Tesoldi

- **Tesoldi UX, Design System, and ICP** — 2026-08-28, Luis + Florin, ~20 min
  Aligned: Tesoldi needs a step up from data-only to workflow-oriented UX. Decision: build shared design system from current repo (standardize buttons, modals, agent/board views). Florin will start before Amalfi Coast vacation (available through Monday). ICP converging on treasury professionals/CFOs with complex, expensive problems. Current customers are reacting well once past raw UI.

- **Internal Finance Product Dogfooding Plan** — 2026-08-26, Luis + Dan
  Decision: use next 2 weeks to dogfood internally, focus on concrete finance problems (FX exposure, Stripe, invoicing). Product surfaces: dashboards, chat, agents. Key gaps: approval-gating bugs, chat regressions, dashboard sharing complexity, FX grouping, manual account permissions. Tentative timeline: internal beta Sep 15, public launch Oct 1. Next step: map Mariel's billing workflow → first-of-day billing via Stripe+Odoo.

- **Finance Automation Audit and Platform Strategy** — 2026-08-26, Luis + Dan
  Deep dive into current state: contracts in HubSpot as attachments (not a contract object), no source of truth across spreadsheets/Odoo/Stripe/HubSpot. Potential revenue leakage identified: FX rate date mismatches, unreconciled Odoo balances, inconsistent prorated implementation fees, suboptimal tax treatment. Decision: build current-state system map first, then quantify losses, then prioritize v1.

### Finance & Fundraising

- **Finanzas, crecimiento y estructura de Tesote** — 2026-08-27, Luis + Mariel
  Performance review conversation: Mariel has taken on too many manual ops tasks, causing burnout. Decision: free her from daily operations → let her focus on analysis/leadership. First internal Reverón project: automate Odoo reconciliation (contracts + billing dates). Comp: Lorena interviews 9 more Finance candidates (Jonathan discarded); Mariel prepares raise proposal. Structural issue flagged: Tesote underpaying vs. Venezuelan market on benefits (insurance). Also: legal/fiscal structure (agent-de-cobro, RIF, payroll) needs revalidation with lawyers.

- **Proyección de caja y capital requerido** — 2026-08-25, Luis + Mariel + (3rd person)
  Fixed model error (was using only BsF balance as base). Conservative position: ~$240K cash + ~$125K AR – ~$30-35K owed to Stripe. Forecast: with ~$5K/month FX exposure provision, Dec cash balance ~$165K ($200-210K with healthy AR). Liquidity problem = USD available in accounts + lag between billing/collection/availability. If ops approach breakeven by Dec, additional operational need could be ~$100K. Before setting round size: identify short-term investments + deferred capex to finance.

### Strategy & Leadership

- **Tesote: estrategia, producto y conexiones** — 2026-08-27, Luis + Estefany
  Luis reflected on intensity of last months (APIs, fundraising, churn, Reverón). Decision: entering a more mature phase — protect risk areas, control costs, delegate operations to leadership team, shift to long-term planning (5-year vision, North Star, team KPIs). Banking connections health ~80-85%. Prioritized banks for API migration: Mercantil, Bancaribe, Banesco, Bancoplaza. Client pipeline reviewed: Joamic, Chin Chin, Ubipagos, Kaizen, Oriant — Estefany owns follow-ups. Luis owns Patricia/Su Portuguesa.

### Sales Pipeline

- **Revisión de deals, Reverón y pricing** — 2026-08-27, Luis + Esteban
  Reverón decision: delay launch until monitoring + bug visibility improves. Fibertel K: free Reverón trial month 1, billing starts October. Key pending proposals: Tijerazo (~15K movimientos, ~$4K MRR, $8-10K impl), automated reconciliation ($2.5-3K MRR, $1-3K impl, two options: flat file or SAP direct). All proposals in USD. Esteban leads price conversations. Upshous→Slack pipeline integration needs Luis's help.

- **Propuesta comercial y requisitos del cliente** — 2026-08-26, Luis + Esteban
  Quick sync on a deal: agreed to raise subscription to $1,500-2,000+. Justification framing: platform cost increase + new features (not support). Esteban sending proposal same day. Meeting with Alfonso Rivas on Thursday; client's non-negotiable: message appearance feature must be available.

- **Inventarios, integraciones y acuerdos comerciales** — 2026-08-25, Luis + Esteban + Roberto
  Reviewed Sana bank inventory (Bancaribe, Banesco, Banesco USA/Panama, Banam Plus, BNC, Mercantil, Provincial, Banco de Venezuela, Venezolana Credit). Droonena: complex due to wholesale ops. Valgreste: starts with 11 accounts (has ~60); Esteban updating proposal in USD w/ copy to Roberto. Zinac: Luis to follow up with Ramiro. Ad partnership negotiation: prioritize cash component (~75/25 split). Technical client with internal ERP: needs discovery call.

- **Avances y propuesta comercial del proyecto** — 2026-08-25, Luis + Nicolás + client
  Project progressing well; live board working fast. Decision: activate both workspaces to start sending emails. Commercial: current payment ~$715/month; considering adjusted proposal given narrower FX gap (upsell package with calls + features). Nicolas to create director user during Smart's vacation → joint meeting after.

- **Cobranza y selección de personal** — 2026-08-25, Luis + Mariel + Roberto
  Total AR ~$125K; ~$87K considered relatively safe. Additional $10-15K potentially recoverable. Caché: 2 overdue invoices ~$9,750 each — reminder this week. Luis León: two options — pay or official suspension. Protinal + Maralaca: formal suspension notice. Roberto follows up BSB, Mi Mesa, Rockenbout, Euromercado, Canaima. Mariel to separate healthy AR from doubtful in Tesote. Hiring: Mariel evaluating candidates; Luis to interview additional Central candidate before deciding on Jonathan.

- **Nueva propuesta comercial y estado bancario** — 2026-08-24, Luis + Esteban + Roberto + Estefany
  New proposal for Fernando: breakdown by bank, includes implementation + roadmap. Proposed: ~$6,900 total ($3,400 subscription + $500 Reverón — needs confirmation). Roberto to coordinate Fernando meeting w/ Luis. Mercantil now in prod; Caribe not yet. Santi on vacation — team to cover bank follow-up.

- **Propuestas comerciales y oportunidades** — 2026-08-24, Luis + Esteban + Roberto
  Large client (no ERP): implementation raised to $5K for bank connection migration + API work. Monthly license updated per account count + volume (new value: categories, counterparties, reports, Reverón). GetSight continuing but international accounts still limited (third-party costs). Grupo Gypsy opportunity identified via Distribuidora de Market. Thursday meeting with Alfonso Ríos (Sage): flat-file solution from banks directly to Sage for reconciliation. Grupo Canaima: prepare for significant price increase — frame it as "tariff held for years despite prior increases."

- **Negociación de pagos y salida en vivo** — 2026-08-24, Luis + Esteban
  Ana proposed phased payment: 25% at Banesco/Provincial/Venezuela test, 25% after validation, 50% impl + license at Dynamus live (Dec/Jan). Luis counter: get some payment pre-live via limited license (~$2K) or November start. Decision: Esteban to prepare email with proposal; may need to escalate to Daniela directly (Ana says Daniela won't pay until live).

### Customer Expansion — New Logos

- **Intro: Hospital de Clínicas Caracas // Tesote** — 2026-08-28, Esteban + Luisana + client (5 pax), 46 min
  Strong intro. Currently: 18 banks loaded manually into Excel, separated by currency. Phase 1 plan: consolidate balances, cross-reference ERP with Tesote, build real availability reports. Pricing range $12K-70K annual + $5K+ implementation. Board reviewing next week. Esteban to send contract model, NDA, tech security docs, client list, and adjusted proposal.

- **Intro: Ovomar // Tesote** — 2026-08-28, Luisana + Nicolás + client (4 pax), 26 min
  Odoo in production month 2. Conciliation still manual. Interested in automated conciliation + Tesote-Odoo integration via API. Nicolás to prepare phased implementation proposal (CONODU project), coordinate with María José (product) and IT/ICE teams.

- **CS Meeting: Netuno // Tesote** — 2026-08-28, Estefany + client (4 pax), 48 min
  Focused on ISM vs SMM file format differences (daily vs grouped). Tecno phone issues blocking SMS code reception. Mercantil API migration pending. Estefany to: fix Tecno SMS permissions, confirm Mercantil API to prod, send Vanesco update.

- **Discovery: Casa Franceschi // Tesote** — 2026-08-28, Estefany + Nicolás + Esteban + client, 31 min
  Agroindustrial group restructuring ops in Venezuela. 50% of exports from Apure/Barinas expansion. Uses USDT. Treasury (Daniela Chepo) manages BsF + USD. Goal: unify accounting processes. Client to send bank account inventory + consult ERP options. Estefany to facilitate Corpureca partner contact; schedule follow-up demo Thu PM.

- **Tesote // Coseimpa** — 2026-08-28, Esteban + Luis + Roberto + client (7 pax), 24 min
  Pricing renegotiated: maintain $1K/month from November despite operating losses. API implementation: $1,500 one-time, no additional costs for new connections. Reverón: free trial. Client reduced active accounts to 53. Roberto to adjust proposal and coordinate API bank testing.

- **Reverón IA: Tesote // Gerais** — 2026-08-27, Luis + Nicolás + Joan + client, 40 min
  Client wants IA for historical analysis, predictive models, automated reports, alerts, custom dashboards, and data warehouse. Gerais confirmed as beta site (formal letter of commitment). Luis committed to beta access within ~1 week. Nicolás to send roadmap + coordinate technical brainstorming with D Link.

- **Tesote x Grupo Rica: Hoja de ruta y más** — 2026-08-27, Luis + Esteban + Estefany + Roberto + client (7 pax), 13 min
  Quick sync: Mercantil authorization letters sent but no response from bank. Glorimar to share Katia Cabezas (Mercantil exec) contact with Estefany. Esteban to check if Álvaro wants to work via email or in a live meeting. Plan: demo Reverón AI when Álvaro is available.

- **Tesote // Fivenca** — 2026-08-26, Luis + Esteban + Estefany + client (8 pax), 26 min
  Account reducing from 187 to ~100. Monthly cost increasing to $2K due to platform fixed cost increase. Reverón: enabling access end of week / early next week for beta + training. Luis to send formal description of Reverón deliverable and scope. Esteban to send adjusted proposal (50 accounts tier) and coordinate in-person Caracas meeting with José Miguel.

- **Tesote // Veconinter** — 2026-08-26, Luis + Esteban + Roberto + client (8 pax), 68 min
  Full demo of Tesote (treasury consolidation, multi-FX, auto-sync, categories). SOC 2 certification in process. Reverón as complement for automated KPI reports. IT team to review security docs. Roberto to send security documentation, roadmap, and coordinate next steps. Client needs time for internal analysis before committing.

- **Discovery: Grupo DUG // Tesote** — 2026-08-27, Luisana + Esteban + client (7 pax), **3 hours**
  Large complex opportunity. Current issue: manual downloads cause 1-2hr availability delays. Goal: automate extracts → feed Quimat/Cuimat directly (eliminating manual downloads). Portal de autocobro in development. API validation depends on bank APIs. Esteban to send commercial proposal + API docs; coordinate follow-up.

- **Farmacias San Ignacio JT // Tesote** — 2026-08-25, Luis + Veronica + Estefany + client (5 pax), 25 min
  Case study session with Suzanne. Tesote automated >80% of transactions; processing time reduced from ~4 hrs to 2 hrs. Team of ~50 benefiting. Areas for improvement flagged: more flexible reports, more frequent updates. Luis to send Suzanne case study interview summary.

- **Tesote x Comercializadora Tiares: Hoja de ruta y más** — 2026-08-25, Luis + Nicolás + Estefany + client, 39 min
  New features presented: ERP API integration, Reverón AI. Client on "Happy" plan — evaluating flexibility/cost adjustment. Nicolás to coordinate with Luis on activating reports (starting with cash-close reports). Luis to send detailed meeting summary + roadmap + activate automatic reports.

- **Discusión Comercial: Chronus Oil // Tesote** — 2026-08-25, Esteban + client (7 pax), 26 min
  Presented automated commission reconciliation + payroll (included at no extra cost; invoice reconciliation coming year-end). Reverón: automated financial reports. Revised commercial proposal with significant discounts. Odoo partner (Indexa) integration confirmed. Client to respond same day after internal review.

- **Discovery: Tesote // Grupo Di Biase** — 2026-08-24, Nicolás + client, 47 min
  Start pilot in Caracas branch before expanding to Barquisimeto/Valencia. Arturo and Robert are decision-makers. SAP integration needed. Nicolás to prepare proposal + case, organize technical session with IT team, and send discovery form.

- **Intro: Paveca // Tesote** — 2026-08-25, Luisana + Esteban + client (4 pax), 52 min
  Multi-company tool with cloud auto-connections, multi-currency, Reverón AI. Implementation 5-6 weeks. Plans: connect treasury core first, then full Odoo integration. Esteban to send docs within 48h; client to coordinate multi-functional team evaluation.

- **Propuesta: Tesote // Biotel** — 2026-08-26, Nicolás + client (3 pax), 37 min
  Proposal: $5,500 implementation + $1,500/month, three-phase rollout. Client interested in projected budget module with AI. Vicente to send hotel budget Excel model; Nicolás to evaluate feasibility with engineering + send formal proposal.

- **Propuesta: Tesote // Inversiones Mad Warapa** — 2026-08-26, Nicolás + client (2 pax), 15 min
  Proposal: $4,000 one-time + $1,000/month. ROI: ~$39K based on other client metrics. Two-phase implementation. Follow-up call Wednesday for client decision.

- **Intro: Hipermercado Garzón // Tesote** — 2026-08-27, Luisana + Esteban + client (3 pax), 20 min
  Interested in automating cash flow reports and reducing manual work. Mercantil integration is low-priority for them. Decision: Esteban to send video + info, recontact in late September. Client to give definitive response Oct 7-11.

- **Propuesta: Tesote // Wynco** — 2026-08-24, Nicolás + client (4 pax), 22 min
  10 accounts, ~3,000 transactions/month, currently all manual. Proposal: $5,000 impl + $1,500/month + Odoo integration. Target: ready before Odoo full integration (November). Nicolás to send formal proposal + contract + sandbox access.

- **Tesote x Grupo Abreu: Hoja de ruta y más** — 2026-08-24, Luis + Esteban + Estefany + Roberto + client, 20 min
  Focus on completing Bancaribe and Mercantil integrations (Mercantil = 70% of their revenue). Technical challenges with Mercantil API. Luis to send meeting minutes + work plan + roadmap; coordinate Bancaribe status with Stephanie.

- **Reunión con Tesote [Andrés Milano / Coloris]** — 2026-08-28, Nicolás + client (2 pax), 19 min
  Client managing accounts in Venezuela, Panama, USA (~200 tx/month). Read-only consultation needs. Wants ERP link for reconciliation and financial management. Security is top priority. Nicolás to send security info, confirm bank sync quality, send contact info, and organize discovery meeting with admin team.

- **Intro: Servicárnicos // Tesote** — 2026-08-24, Carlos.Melian + Esteban + client (4 pax), 26 min
  Multi-business-line group interested in automating financial consolidation. Currently prioritizing ERP implementation first. Follow-up: end of September / early October.

### Customer Success — Active Accounts

- **Tesote // Inquiport** — 2026-08-27, Nicolás + Keyla + Joan + client (5 pax), 30 min
  Two connections pending (BNC, Vanesco BsF) due to credential issues. Charlys to update credentials this week. Google Authenticator migration planned for Bancamiga. Categories directory needs simplification (list of codes + names pending). 76% pilot data validated. Joan to cover during Keyla's absence.

- **Control de Avances: Tu Aliado // Tesote** — 2026-08-26, Keyla + client (3 pax), 92 min
  Implementation at ~100% use but technical pendants remain. Mercantil: needs Android user + SMS automation + phone number update. Panama banks (Vanesco, Mercantil): need invited users + initial token. BDT showing missing account. Categorization automated at 87.5%. UBI/Zain integrations still pending.

- **Control de Avances: Mimesa Alimentos // Tesote** — 2026-08-26, Keyla + client (3 pax), 90 min
  Focus: SAGE integration — replicating categories, counterparties, rules. Evaluating consolidated Excel/CSV vs per-bank files. Keyla to evaluate feasibility of consolidated file with SAGE converter. Night auto-sync for operational close balance being configured.

- **Control de Avances: Agroavicola del Llano // Tesote** — 2026-08-25, Keyla + client (4 pax), 45 min
  Validated BNC and Provincial connections. Bank Digital de Trabajadores has session limitations. Vanesco and Banplus credentials need updating (sync breaking). Odoo integration currently manual — jefe de sistemas to evaluate Tesote connector for automated reconciliation.

- **Implementación: Grupo Santa Teresa // Tesote** — 2026-08-25 + 2026-08-27, Keyla + client
  Aug 25 (56 min): Updated credentials for BNC and Calica (automated). Banco de Venezuela needs 2nd signature + mobile app. International banks (Vanesco USA, Amaranth) queued. Aug 27 (brief): Rescheduled to Monday 11am; Mercantil token pending from Evelin; Carmen's app install postponed to Monday. Joan/Stephanie to cover for Keyla.

- **Customer Success Meeting: Hispana de Seguros // Tesote** — 2026-08-26, Estefany + Keyla + client (4 pax), 112 min
  Partial automation achieved on Redmi devices (Tecno too limited). Keyla introduced as implementation manager. Mercantil migrating to API. Sync schedule: 3x/day. Keyla to create engineering ticket for Bancamiga QR code issue. Follow-up meeting scheduled Sep 8 at 10am.

- **CS Meeting: Netuno // Tesote** — 2026-08-28, Estefany + client (4 pax), 48 min
  ISM vs SMM format clarification. Tecno phone blocking SMS codes — Estefany to investigate permissions. Mercantil API confirmation pending. Ongoing monitoring of sync reliability.

- **Configuración de Conexiones: IOCECA // Tesote** — 2026-08-27, Joan + client (4 pax), 55 min
  Connections active: Vanesco (BsF only, no FX), Provincial, Bancaribe, Venecia. Mercantil + BNC in progress. Bancaribe: manual security questions blocking auto-sync (recommend eliminating). Sync options: every 10 min, max 3 blocks/day. Joan to configure daily auto-syncs and confirm API call capacity.

- **Configuración de Usuarios - Covencaucho** — 2026-08-26, Joan + client (2 pax), 86 min
  Alexandra as admin role, credit-only access (no debit/balances). Excluded FX accounts and inactive accounts. Reports: mobile payments + cache income only (no internal transfers). Saldo display issue in screen (available in exports). RIF counterparty upload pending.

- **Consultoría: Centro Clínico Fenix Salud // Tesote** — 2026-08-24, Joan + client (4 pax), 35 min
  Current process: manual AR review via Excel. Tesote demo: real-time balance view, auto-updates 3x/day, custom filters per role. Next: Joan to provide login credentials; client to decide on Odoo integration or API connector.

- **Configuración de Conexiones: Grupo Rokouka // Tesote** — 2026-08-24, Joan + Keyla + client (9 pax), 122 min
  Issues: unified accounts across entities (need separation by company), Banca Amiga sync instability, Tesote app not syncing (recommend update), Infinix device permission conflicts. Google Authenticator migration proposed. Joan to investigate dynamic SMS message changes, propose auto-rules. Planilla to complete by Monday.

- **Quo Vadis Tesote** — 2026-08-26, Estefany + team (internal), 78 min
  Internal CX team session. Key initiatives: (1) bank API migration (Mercantil, Vanesco, Bancaribe) → real-time sync, (2) Google Authenticator auto-use to eliminate token errors, (3) Reverón for context-aware automated reports, (4) advanced permissions + auto-notifications. Transaction volume growing significantly.

### Banking Connections & CX Operations

- **Feedback y seguridad de Reverón** — 2026-08-24, Luis + Estefany, ~2 pax
  Víctor de Seven has security concerns after connecting Reverón to Tesote (NCP usage, data authorization, destination, public services). Likely a misconfiguration in initial integration auth. Plan: Estefany creates WhatsApp group (Luis + Víctor + Estefany) to coordinate. Luis to write to Víctor when he joins.

- **Rebeca Triana Cannilla <> Jhossua Angulo** — 2026-08-27, Rebeca + client, 22 min
  Auto-code reception failing since Aug 25 — Mercantil connection broken. App active but no codes arriving. Suspected Tesote-Endros incompatibility. Rebeca to review config with Joan and prepare report for Jhossua.

- **Rebeca Triana <> Victum Legal** — 2026-08-25, Rebeca + client, 31 min
  Ban Plus credential reset + sync restored. Rodrigo to provide Mercantil authentication token.

- **Rebeca Triana <> Netuno** — 2026-08-24, Rebeca + Caridad, 12 min
  Auth issue: wrong phone number registered causing SMS codes to fail. Resolved: email auth used as fallback. Follow-up via chat to confirm definitive sync.

- **Tesote // Grupo Di Biase (IT)** — 2026-08-25, Nicolás + MaJo Díaz + client (4 pax), 20 min
  VenIoT integration: use Tesote API to sync financial data → VenIoT builds display interface. Pilot at Boleíta store. Scope: basic financial variable visualization (cash, accumulated sales). Pricing based on account count + volume. Nicolás to send API docs + proposal.

### Marketing

- **Marketing, leads y contenido de Luis** — 2026-08-26, Luis + Veronica + Mavo (3 pax)
  Pricing page decision: consider ranges or WhatsApp CTA instead of forcing a call. Fix broken generic emails on website (info@ or sales@). ManyChat / WhatsApp flow not ready to activate yet — finish qualification flow first, then reactivate Instagram redirect. Luis content plan: natural desk videos (product demos, Tesote, Reverón). Luis available to record Sep 7-11. Mavo to send Instagram account proposal; Veronica to send content guide + updated LinkedIn prompt.

---

## Coverage

**Roam** = Luis's personal meetings only (personal-access token). Returns all calls where Luis was a participant.
**Fireflies** = org-wide admin view. Returns all team members' calls that Fireflies joined.
**Gap**: purely internal Roam syncs between teammates Luis wasn't in are not captured in either source.

- Roam: **16 calls**
- Fireflies: **49 calls** (includes 9 silent/skipped with no summary — listed selectively above)
- Deduped: **1** (Fireflies "Luis/Florin" = Roam "Tesoldi UX, Design System, and ICP" — matched on participants + time within ~2 min; kept Roam record as richer)
- **Total unique calls: 64**
