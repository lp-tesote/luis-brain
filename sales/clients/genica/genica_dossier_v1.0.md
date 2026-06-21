---
title: "Alimentos Génica — Internal Dossier v1.0"
tags: [dossier, genica, confidential, sap, venezuela]
updated: 2026-04-15
author: Tesote
notion_page_id: 3431ee04-eee1-8170-9a5c-d3690cc0cef5
notion_last_synced: "2026-04-15T20:00:00Z"
---

# Client Dossier
*Tesote Intelligence Record — Confidential*

---

# Part I — Client & Commercial Context
*Sales-owned. Who the client is, how they operate, and what their problems are.*

## 0. Record Metadata

| Field | Value |
|---|---|
| **Dossier ID** | `TST-2026-005` |
| **Account Name** | Alimentos Génica |
| **Dossier Status** | `Active Pursuit` |
| **Sales Rep** | Esteban Suárez |
| **Sales Rep Email** | esteban.suarez@tesote.com |
| **Primary Owner** | Carlos Melián |
| **Date of Intro Call** | 2026-03-27 |
| **Date of Discovery Call** | 2026-04-10 |
| **Estimated Close Date** | 2026-05-10 |
| **Date Initiated** | 2026-03-27 |
| **Last Updated** | 2026-04-15 |
| **Source** | TBD |

---

## 1. Company Overview

### 1.1 Organizational Profile

| Field | Value |
|---|---|
| **Legal Entity Name** | TBD |
| **Trade Name** | Alimentos Génica |
| **Industry / Sector** | Food Manufacturing |
| **Annual Revenue (est.)** | TBD |
| **Ownership Structure** | TBD |
| **Parent Company** | TBD |
| **Subsidiaries / Business Units** | TBD — multiple entities mentioned (custodio accounts suggest holding or trust structure); José Boscán hinted at expanding beyond Génica: *"arranquemos con Génica"* — suggests a broader corporate group |
| **Website** | genica.com.ve |

### 1.2 Strategic Context

Alimentos Génica is a Venezuelan food manufacturer (genica.com.ve) with medium-high financial operations complexity: 25–30 national bank accounts (not counting custodio and electronic accounts that multiply the real total — *"cada banco lo multiplicamos por cuatro"* — José Boscán), international accounts in Panama and the US, and approximately 5,000 transactions per month. They run SAP as their ERP since at least 2018. The finance team, led by Anaura Prieto, has automated 95% of the SAP loading process, but extracting data from bank portals remains manual. José Boscán confirmed they operate with daily payments since 2018: *"tenemos desde el 2018 pagando todos los días, no hay un solo día de pago."* Interest in Tesote is clear, driven by an operations team that already knows exactly what to automate.

---

## 2. Stakeholder Map

### 2.1 Key Contacts

| Name | Title | Department | Role in Process | Contact | Notes |
|---|---|---|---|---|---|
| **José Boscán** | Treasury / Sales Administration | Finance | `Champion` + `End User` | jose.boscan@genica.com.ve | Primary contact. Leads the treasury team. Identifies the pain. Responsible for the account inventory. Present at both meetings. Hinted at expanding scope beyond Génica. |
| **Anaura Prieto** | Finance / Treasury | Finance | `Champion` + `End User` | anaura.prieto@genica.com.ve | Knows the process in detail — confirmed 95% SAP automation. Responsible for validating transaction volume. Proposed creating read-only bank users for Tesote. Manages daily availability: checks balances ~10am in Excel, passes info to the Finance Director to authorize payments. |
| **Leodardo Chacín** | Technology / IT | Technology | `Technical Gatekeeper` | leodardo.chacin@genica.com.ve | Actively participated in discovery. Insisted on immediate alerts for new bank codes. Mentioned his team can respond in 15–20 min (max 1 hour) to register new codes in SAP. Asked about architecture (cloud vs. on-prem) — confirmed Tesote = AWS cloud, no local installation. |
| **Juan García** | Systems / IT | Technology | `Technical Support` | juan.garcia@genica.com.ve | Technical support in both meetings. Complements the technical side of the SAP integration. |
| **Mileidy Hernández** | Collections | Collections | `End User` | mileidy.hernandez@genica.com.ve | Confirmed that segmented view (credits only for her team) would be a significant improvement. Asked about differentiating clients with similar RIF (last digit). |
| **Alexandra Rodríguez** | TBD | TBD | `End User` | alexandra.rodriguez@genica.com.ve | Asked about handling incomplete RIF in statements: *"hay veces que faltan números al final del RIF."* Interested in per-bank parameterization rules. |
| **Dayana Faneitte** | Analyst | Finance | `End User` | dayana.faneitte@genica.com.ve | Shared real-world case of Provincial code 595 (forex auctions loaded as commissions). Asked how Tesote handles errors in automated statements. Direct user of the SAP loading process. |
| **Viviana Parra** | TBD | TBD | `Attendee` | viviana.parra@genica.com.ve | Present at both meetings. Role TBD. |
| **Yulimar Valbuena** | TBD | TBD | `Attendee` | yulimar.valbuena@genica.com.ve | Present at both meetings. Role TBD. |
| **Claudia Rosales** | TBD | TBD | `Attendee` | claudia.rosales@genica.com.ve | Present at discovery. Role TBD. |
| **Iraquil Borges** | TBD | TBD | `Attendee` | iraquil.borges@genica.com.ve | Present at discovery. Role TBD. |
| **Marlene Villasmil** | TBD | TBD | `Attendee` | marlene.villasmil@genica.com.ve | Present at discovery. Role TBD. |
| **Egglys Martínez** | TBD | TBD | `Attendee` | egglys.martinez@genica.com.ve | Present at discovery. Role TBD. |
| **Esteban Suárez** | Account Executive | Tesote | AE | esteban.suarez@tesote.com | Organized both meetings. Led the discovery session. |
| **Carlos Melián** | TBD | Tesote | AE / Account Owner | carlos.melian@tesote.com | Organized the intro call. |

### 2.2 Decision Dynamics

- **Economic buyer:** Not identified. With 15 people from Génica in the discovery, the purchase decision likely involves a management or director-level figure who was not present. Must identify and engage before presenting a formal proposal.
- **Technical gate:** Leodardo Chacín and Juan García — evaluating technical feasibility of SAP integration. Their approval of the API and security documentation unlocks the proposal. Leodardo's team can turn around SAP config changes in 15–60 minutes.
- **Champion:** José Boscán + Anaura Prieto — both understand the pain, comprehend the solution, and are actively committed to moving forward. José hinted at expanding beyond Génica (*"arranquemos con Génica"*), suggesting broader group potential.
- **Political considerations:** The participation of 15 people in the discovery (finance, treasury, collections, IT) suggests Génica is taking the evaluation seriously and that the project has internal visibility. However, the economic buyer has not participated and must be identified before presenting a formal proposal. Previous proposal from July 2025 did not close — need to understand what changed.

---

## 3. Financial Operations Diagnostic

### 3.1 Banking Relationships

| Bank | Country | Account Type | Volume Tier | Notes |
|---|---|---|---|---|
| Banesco | Venezuela | Checking / Savings | `High` | ~10 accounts confirmed by Anaura. Primary bank — ~1,100 transactions/month on one account alone. |
| BBVA Provincial | Venezuela | Checking / Savings | `High` | 3 accounts confirmed by Anaura. RIF truncated on portal. Code 595 issue (forex auctions mixed with commissions). |
| TBD — others | Venezuela | Checking / Savings | `Varies` | 25–30 national accounts total. Custodio and electronic accounts multiply real total (×4 per bank approx). Full inventory pending. |
| TBD | Panama | TBD | TBD | International accounts mentioned. Detail pending from inventory. |
| TBD | US | TBD | TBD | International accounts mentioned. Detail pending from inventory. |

> **Coverage note:** Once the full inventory is received, each bank will be cross-referenced against Tesote's active integration registry. Major Venezuelan banks (BNC, Banesco, Mercantil, BBVA Provincial, Banco de Venezuela, Bancaribe, Bancamiga, etc.) are in the active registry. For international banks in Panama (Banesco Panamá, Mercantil Panamá, Global Bank, Banistmo) and the US (Amerant), Tesote has confirmed coverage. Any bank outside the registry will be escalated to the product team.

### 3.2 Operational Cash Flow Structure

Génica operates with daily payment cycles — José Boscán confirmed: *"tenemos desde el 2018 pagando todos los días, todos los días hacemos desembolsos de pago."* The daily workflow:

1. **~10:00 AM:** Anaura checks bank balances across all paying banks (~4 main banks), logs them in an Excel sheet to determine availability. Passes the information to the Finance Director.
2. **Finance Director** authorizes which payments to execute based on available balance vs. committed payments.
3. **Throughout the day:** If additional payments are needed, Anaura re-checks bank balances against committed amounts and processes if funds are available.
4. **Daily (1+ hour):** One person downloads bank statements from every portal for SAP loading.
5. **Post-download:** 95% of statements load automatically into SAP; 5% require manual intervention (new bank codes, data errors).
6. **Daily:** Collections team (Mileidy) views loaded statements in SAP to confirm client payments.

Additionally, Génica maintains "cajas principales" (petty cash / cash registers) at different locations — these are accounting entries, not bank accounts, and would require manual upload via Excel template in Tesote.

---

## 4. Technology Landscape

### 4.1 ERP & Core Systems

| System | Vendor | Version | Module Scope | Deployment | Maturity |
|---|---|---|---|---|---|
| **ERP** | SAP | TBD | Accounting, Treasury, Bank Reconciliation | TBD (likely On-Premise) | `Mature` — in production since at least 2018 |

### 4.2 Data & Integration Architecture

- **Existing automation:** Génica already has 95% of the SAP loading process automated. The manual piece is extracting data from bank portals. Tesote replaces exactly that piece.
- **Data format for SAP:** JSON — Tesote supports this natively for SAP integration.
- **SAP bank code architecture:** Each bank has its own transaction codes mapped in SAP. When a bank introduces a new code, the automatic load fails until IT registers it. Dayana provided a real example: Provincial code 595 was intended for commissions but the bank started routing forex auctions through the same code.
- **IT ownership model:** Internal technology team (Leodardo Chacín, Juan García) manages SAP integration and automation processes. Leodardo confirmed their internal response time for new code registration: 15–20 min, max 1 hour.
- **Architecture:** Tesote is cloud-based (AWS). Génica will not need any on-premise installation — access is via web platform only. Leodardo confirmed understanding and acceptance of this model.

### 4.3 Known Constraints & Compliance Requirements

- **New bank codes in SAP:** When a bank introduces a new code, SAP load fails until IT registers it. This is the most discussed technical concern — Leodardo insisted on immediate alerts. Tesote resolves with reconciliation module + real-time alerts + two options: (1) client registers code in SAP, or (2) Tesote maps the new code to an existing one via rules.
- **Incomplete data in statements:** Several banks send statements with truncated RIF or erroneous references. Alexandra Rodríguez and Dayana Faneitte both confirmed this pain. Provincial in particular doesn't return the full RIF. Tesote resolves with per-bank parameterization rules during implementation.
- **Custodio and electronic accounts:** No direct bank integration. Will continue manual upload via Excel template in Tesote.
- **Security:** Leodardo and IT team will evaluate API and security documentation before approving the integration. Read-only bank user policy already defined by Anaura Prieto.
- **Provincial code 595:** Specific issue where bank routes different transaction types (commissions vs. forex auctions) through the same code — Tesote can handle via rules engine.

---

## 5. Problem Definition

### 5.1 Stated Pain Points

*Direct language from participants — sourced from discovery call 2026-04-10.*

1. **"Una persona lo gestiona, eso tiene una hora"** — José Boscán, on the daily manual statement download process [discovery, 7:50]
2. **"El 95% los tenemos automatizados para cargarlo a SAP"** — Anaura Prieto, confirming that the manual bottleneck is specifically the bank portal extraction, not the SAP loading [discovery, 7:13]
3. **"Cuando hay un nuevo código de operación bancario [...] dio un error en la carga del extracto"** — Leodardo Chacín, on the failure mode when banks introduce new codes not mapped in SAP [discovery, 57:01]
4. **"Hay veces que faltan números al final del RIF"** — Alexandra Rodríguez, on incomplete client identification in bank statements [discovery, 21:16]
5. **"El extracto que me genera el banco está incorrecto y por supuesto SAP me indica que no lo va a cargar y lo estoy haciendo de manera manual"** — Dayana Faneitte, describing a real incident with Mercantil statements [discovery, 11:45]
6. **"La visualización segmentada sería un avance para mi equipo"** — Mileidy Hernández, on differentiated access for the collections team [intro call]

### 5.2 Latent Pain Points

1. **Single-person dependency:** The manual download process is concentrated in one or few operators. Absences delay the daily close.
2. **Scalability limit:** At 5,000 tx/month the manual process is already a daily burden. Growth will make it unsustainable.
3. **Audit risk:** Manually downloaded and loaded statements lack automated validation before SAP. The reconciliation module adds a validation layer.
4. **Fragmented visibility:** Treasury accesses balances bank by bank — no consolidated real-time view without entering each portal. Anaura described an Excel-based availability process that is inherently manual and point-in-time.
5. **Code maintenance burden:** Every time a bank introduces a new transaction code, the load fails system-wide for that bank until IT intervenes. Dayana's Provincial 595 example shows this is a recurring operational disruption.

### 5.3 Triggering Event

No imminent ERP transformation event (unlike CAPCA's SAP Go Live). The pain is chronic since 2018. The urgency is driven by the maturity of the finance team — they already automated 95% of the process and know exactly what's missing. The opportunity window is the team's willingness and the scale of operations (~5,000 tx/month) that makes the manual bottleneck increasingly costly. Prior proposal from July 2025 did not close; the new evaluation involves more people, more defined use cases, and an engaged IT team.

### 5.4 Cost of Inaction

| Category | Estimate | Basis |
|---|---|---|
| Manual download time | ≥1 hour/day · ~22 business days/month = ≥22 hours/month | José Boscán, discovery 2026-04-10 |
| Estimated annual savings | ~$38,400 USD | Proposal presentation July 2025 (800 hrs/month valued at ~$4/hr) |
| Bank code failure risk | High — SAP load fails until manual resolution | Leodardo Chacín + Dayana Faneitte, discovery 2026-04-10 |
| Portal downtime risk | Medium — delays statement availability for the day | Operational context confirmed (Mercantil downtime mentioned) |
| Manual validation time | Not quantified — Anaura confirmed team validates every bank load individually in SAP | Anaura Prieto, discovery 2026-04-10 |

---

# Part II — Scope & Implementation
*The operational handoff. Implementation starts here.*

## 6. Use Cases by Team

*How Tesote integrates into each team's operation within Génica. Each item maps to a scope capability in section 7.1.*

### Treasury (Anaura Prieto)

- Real-time balances across all accounts without accessing bank portals — consolidated visibility by bank, currency, and entity *(replaces manual portal-by-portal check at ~10am)*
- Automated scheduled syncs (morning, afternoon, end-of-day) + on-demand — eliminates the 1+ hour/day manual statement download
- 2FA token automation for banks that require it
- Manual account upload (Excel template) for petty cash and custodio accounts without bank integration

### Collections (Mileidy Hernández)

- Segmented view: collections team sees only credits (incoming payments) — no access to balances or debits
- Client payment identification via RIF matching and counterparty rules *(per-bank parameterization for incomplete RIF — e.g., Provincial missing last digit)*
- Visibility into bank statement data in Tesote as an alternative to waiting for SAP load

### Finance / Accounting (Dayana Faneitte, Alexandra Rodríguez, analysts)

- Automated bank statement delivery to SAP in JSON format — no manual download or upload
- Reconciliation module validates data integrity before SAP load — alerts on discrepancies, errors, and unregistered bank codes
- Categorized transactions (commissions, payments, collections, transfers) for cash flow reporting
- Per-bank rules to resolve data quality issues (truncated RIF, erroneous references, code mapping)

### IT / Technology (Leodardo Chacín, Juan García)

- Real-time alerts when a bank introduces a new transaction code not registered in SAP — enables the 15–60 min internal registration process without waiting for manual discovery
- API documentation for SAP integration — Tesote sends JSON, IT team connects to SAP
- Two code management options: (1) register new code in SAP, or (2) Tesote remaps via rules engine
- No on-premise installation required — cloud (AWS) with web-based access

---

## 7. Scope Definition

### 7.1 Scope

*All capabilities Tesote will deliver as part of this engagement. This is the master list — every deliverable appears here.*

| # | Capability | Type | Phase | Notes |
|---|---|---|---|---|
| 1 | Bank connectivity — banks per inventory (Venezuela national) | `Native` | 1 | 25–30 accounts confirmed; actual bank list pending inventory from José Boscán |
| 2 | Bank connectivity — international (Panama, US) | `Native` | 1 | Banks to validate against registry post-inventory |
| 3 | Real-time bank balances (refresh ≥1x per day) | `Native` | 1 | Available first thing in the morning without manual portal access |
| 4 | Real-time & T+1 bank transactions (refresh ≥1x per day) | `Native` | 1 | Automated scheduled syncs (3x daily recommended) + on-demand manual syncs |
| 5 | SAP integration via API — JSON format | `Native` | 2 | Standard native integration — Tesote sends validated statements to SAP; T+1 (day-closed) recommended for SAP load |
| 6 | Reconciliation and data validation alerts | `Native` | 1 | Detects discrepancies, incomplete data, and bank code issues before SAP load |
| 7 | New bank code alerts | `Native` | 1 | Real-time notification when a movement contains a code not registered in SAP |
| 8 | Categorization & counterparty rules | `Configuration` | 1 | Per-bank rule config: RIF matching (BNC full, Provincial truncated), transaction type categorization (commissions, payments, collections) |
| 9 | GL account mapping | `Configuration` | 2 | Requires chart of accounts from Génica as prerequisite |
| 10 | Multi-entity support | `Native` | 1 | To dimension based on account inventory |
| 11 | User roles, access controls & team segmentation | `Native` | 1 | Differentiated permissions: treasury (full), collections (credits only), finance (all), IT (admin). User administration delegated to Génica. |
| 12 | 2FA token automation | `Native` | 1 | Applicable to banks with token — to verify per bank in inventory |
| 13 | Scheduled syncs (up to 3x daily) | `Native` | 1 | Morning, afternoon, end-of-day — plus on-demand |
| 14 | Manual account upload for accounts without bank integration | `Configuration` | 1 | Excel template for custodio, electronic, and petty cash accounts |
| 15 | Cash flow classification by category | `Configuration` | 1 | Categorized transactions for reporting: commissions, payments, collections, transfers |

> **Type definitions:**
> - **Native** — Standard platform capability. No additional engineering effort.
> - **Configuration** — Available in the platform but requires client-specific setup (rules, mappings, permissions).
> - **Custom Build** — Requires engineering scoping and development. See 7.2 for detail.

### 7.2 Special Features or Integrations

No `Custom Build` items identified. SAP integration is standard (JSON via API). All scope items are either Native or Configuration.

### 7.3 Out of Scope

| # | Item | Notes |
|---|---|---|
| 1 | Final reconciliation in SAP | Responsibility of Génica's finance team in SAP. Tesote performs pre-reconciliation and sends validated data. |
| 2 | New bank code creation in SAP | Responsibility of Génica's IT team. Tesote alerts; the client acts. |
| 3 | Payment execution or transfers | Tesote is a visualization and reconciliation platform — does not handle funds or execute payments. |
| 4 | Accounts payable module | Anaura asked about an integrated availability/payments workflow — Tesote does not currently have an AP module. Workaround: asset/liability account classification in Tesote. |

### 7.4 Pending Definition

| # | Item | Status | Owner |
|---|---|---|---|
| 1 | Full bank account inventory (bank, type, entity, account count) | `Pending — Client` | José Boscán |
| 2 | Average monthly transaction volume by bank | `Pending — Client` | Anaura Prieto |
| 3 | API and security documentation review for SAP integration | `Pending — Client` | IT team (Leodardo Chacín / Juan García) |
| 4 | Exact SAP version and deployment type | `Pending — Client` | IT team |
| 5 | International bank details (Panama, US) | `Pending — Client` | José Boscán / Anaura Prieto |
| 6 | Number of legal entities in scope | `Pending — Client` | José Boscán |
| 7 | Tesote internal response time for new bank code alerts | `Under Review` | Esteban Suárez (Tesote) |
| 8 | Bank code → GL mapping methodology: understand how Génica currently maps bank operation codes to GL accounts in SAP — whether codes are strictly required or if description-based matching (RIF, counterparty, transaction type) could replace or supplement code-based mapping. Request examples of current mapping rules and failure cases. | `Pending — Tesote` | Esteban Suárez (Tesote) |

---

## 8. Implementation Plan

### 8.1 Scope Indicators

- **Number of legal entities:** TBD — minimum 1 (Génica); potentially more per José Boscán's comment about multiple companies
- **Bank accounts in scope:** 25–30 national + custodio/electronic (multiplied ×4 per bank) + international accounts = estimated 60+ total
- **ERP instances:** TBD — likely 1 SAP instance
- **Target go-live:** ~8 weeks post-start (4–5 weeks Phase 1 finance; 5–7 weeks Phase 2 SAP, in parallel)
- **Phasing:** Phase 1 = bank connectivity + finance users; Phase 2 = SAP integration + code alerts

### 8.2 Phases

| Phase | Scope | Owner (Tesote) | Owner (Client) | Est. Start | Est. Go-Live |
|---|---|---|---|---|---|
| **Phase 1 — Finance & Operations** | Bank connectivity, balance dashboard, availability reports, user roles, categorization rules, manual account upload | Esteban Suárez | José Boscán + Anaura Prieto | Post-signature (est. May 2026) | ~4–5 weeks from start |
| **Phase 2 — SAP Integration** | API connection Tesote → SAP, automated statement delivery (JSON), load validation, bank code alert parameterization, GL mapping | Esteban Suárez | Leodardo Chacín + Juan García | Parallel with Phase 1 | ~5–7 weeks from start (~8 weeks total) |

### 8.3 Client Prerequisites

| Prerequisite | Owner | Deadline |
|---|---|---|
| Full bank account inventory | José Boscán | ASAP |
| Transaction volume validation | Anaura Prieto | ASAP |
| API and security documentation review and approval | IT team (Leodardo / Juan García) | Post-receipt |
| SAP chart of accounts (GL) for mapping | IT team | Before Phase 2 start |
| Designate Tesote Master User at Génica | José Boscán / Anaura Prieto | Before Phase 1 start |
| Create read-only bank users for Tesote | Anaura Prieto | Before Phase 1 start |

---

# Part III — Sales Intelligence
*Sales-only. Deal history, qualification, and commercial terms. Not relevant to implementation.*

## 9. Engagement Log

| Date | Type | Participants | Key Outputs | Next Step |
|---|---|---|---|---|
| 2025-07 | `Proposal Presentation` | Luis Pulgar, Roberto Drew-Bear, Esteban Suárez (Tesote) · Indira Gutierrez, Jhordaly Jordan, Yulimar Valbuena, Juan García, Leodardo Chacín, Alejandro Hernández (Génica) | First proposal. ~5,000 tx/month, ~$38,400 USD savings/year, $22,500 USD/year proposed cost. ROI 1.7x Y1, 2.4x Y3. Implementation fee $3,125 USD. Approval path: direct to presidency based on "feeling". | Proposal did not close — deal went dormant |
| 2026-03-27 | `Intro Call` | Carlos Melián, Esteban Suárez (Tesote) · José Boscán, Anaura Prieto, Leodardo Chacín, Juan García, Mileidy Hernández, Alexandra Rodríguez, Dayana Faneitte, Viviana Parra, Yulimar Valbuena, Claudia Rosales, Iraquil Borges, Marlene Villasmil, Egglys Martínez (Génica) | Tesote presentation. SAP confirmed. Manual process identified. 7 accounts initially shared by client. Discovery call scheduled. | Discovery call |
| 2026-04-10 | `Discovery Call` | Carlos Melián, Esteban Suárez (Tesote) · José Boscán, Anaura Prieto, Leodardo Chacín, Juan García, Mileidy Hernández, Alexandra Rodríguez, Dayana Faneitte, Viviana Parra, Yulimar Valbuena, Claudia Rosales, Iraquil Borges, Marlene Villasmil, Egglys Martínez (Génica) | Use cases confirmed. SAP API JSON integration defined. 25–30 national accounts. 10–15 users. 8-week timeline. Bank code management extensively discussed. Action items agreed. | Account inventory + API docs + commercial proposal |

---

## 10. Qualification Assessment

### 10.1 MEDDIC Scorecard

| Dimension | Rating | Evidence / Notes |
|---|---|---|
| **Metrics** — Can we quantify value? | `Partial` | ≥1 hour/day manual download = ~22 hours/month minimum. Prior estimate: 800 hrs/month savings ($38,400 USD/year vs. $22,500 USD/year cost). ROI 1.7x Y1. Numbers are sufficient for a compelling proposal but savings estimate is from July 2025. |
| **Economic Buyer** — Have we identified and engaged? | `Weak` | Not identified. No director/management-level attended either meeting. The massive participation (15 people in discovery) suggests serious evaluation, but purchase approval is a separate step. Prior proposal went "direct to presidency" based on "feeling" — unclear if same dynamic applies. |
| **Decision Criteria** — Do we know their evaluation framework? | `Partial` | Technical criteria clear: SAP integration, bank code alerts, automated download. Commercial criteria (price, contract) not explored. Prior proposal was $22,500/year + $3,125 implementation — unclear if this anchors or not. |
| **Decision Process** — Do we understand the buying steps? | `Weak` | Not explored. Who approves, whether there's procurement, Legal, etc. — unknown. Prior proposal went to presidency. |
| **Identify Pain** — Is the pain recognized and urgent? | `Strong` | Pain confirmed verbatim by multiple stakeholders across two levels (finance + IT). Team has lived with manual process since 2018 and knows exactly what they need. Dayana provided a specific real-world failure example (Provincial code 595). |
| **Champion** — Is our champion credible and active? | `Strong` | José Boscán + Anaura Prieto: both identified the pain, understood the solution, and committed to next steps. Leodardo Chacín active on the technical side with specific, detailed questions. |

### 10.2 Deal Risk Register

| Risk | Severity | Mitigation |
|---|---|---|
| Economic buyer not identified — proposal may stall at operational level | `High` | Ask José Boscán or Anaura to identify who must be in the proposal presentation meeting. Aim to involve the decision-maker before sending the formal proposal. |
| IT team blocks on security/compliance review process | `Medium` | Send API and security documentation immediately. Leodardo seems collaborative and technically engaged. Commit to clear response times from Tesote. |
| Account inventory takes too long and blocks the commercial proposal | `Medium` | José Boscán committed to sending the inventory. Follow up immediately post-discovery. Proposal cannot close without this data. |
| Custodio/electronic accounts without direct integration create adoption friction | `Low` | Excel manual upload template available in Tesote. Communicate clearly in the proposal as a documented workaround. |
| Prior proposal from July 2025 did not close — risk of long sales cycle | `Medium` | The new evaluation context is different: more people involved, more defined use cases, IT team engaged. Do not assume the pattern will repeat, but maintain active follow-up. Understand what changed since 2025. |
| Multiple entities beyond Génica may increase complexity | `Low` | José Boscán hinted at expanding scope. Start with Génica to prove value; use success as expansion lever. |

### 10.3 Overall Qualification Signal

`Qualified — with immediate action required on economic buyer`

*The pain is real, chronic, and confirmed by multiple stakeholders at two distinct levels (finance and IT). The champions are committed. The solution fits exactly what the client needs. The main process risk is the lack of identification and engagement of the economic buyer — without this, the proposal may stall at the operational level. Secondary risk is the prior failed proposal from July 2025. Priority action: before presenting the formal proposal, confirm who approves the purchase and ensure they are in the room.*

---

## 11. Proposal Parameters

- **Suggested implementation tier:** `Standard` — native SAP integration + multi-account bank connectivity + consolidated dashboard + reconciliation alerts
- **Implementation fee range (est.):** To define post-inventory; prior reference: $3,125 USD (July 2025)
- **Recurring subscription range (est.):** To define — base 25–30 national accounts + international; prior reference: $22,500 USD/year (July 2025)
- **Proposed phasing:** Phase 1: bank connectivity + finance users (~4–5 weeks); Phase 2: SAP integration + code alerts (~5–7 weeks, parallel with Phase 1)
- **Key value anchors for proposal narrative:**
  1. Eliminate the daily manual statement download — the last hour lost every day, eliminated permanently
  2. Validated statements in SAP every morning, automatically, ready to reconcile
  3. Real-time alerts for new bank codes — no SAP load failure without prior warning
  4. 95% of the process already automated in SAP — Tesote closes the 5% gap
  5. Native SAP integration — no custom development, no ERP changes required
  6. Consolidated view of all banks, all accounts, in real time
  7. Per-bank rules engine for RIF resolution, code mapping, and transaction categorization
- **Negotiation boundaries:** To define post-inventory. Prior proposal ($22,500/year) anchors expectations but may need adjustment based on actual account count (potentially 60+).

---

*— End of Dossier —*

*Dossier initiated: 2026-03-27. Last updated: 2026-04-15. Maintained by the Tesote commercial team.*
