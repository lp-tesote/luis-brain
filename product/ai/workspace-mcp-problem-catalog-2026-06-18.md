# Tesote AI — Workspace MCP Problem Catalog

> **Luis's annotated pass — 2026-06-18.** Edited from Dan's draft (`problem-catalog (1).md`) for the round-1 automated QA. Row numbers 1–188 are **unchanged** so the QA harness stays stable; my edits are (a) the round-1 scope header below, (b) per-section gating tags, (c) O+P promoted to cross-cutting assertions that ride on *every* row, (d) three appended sections (Q/R/S) for launch-contract behaviors with zero coverage, (e) a gold-standard answer-template appendix. Cross-checked against [[launch-contract-2026-06-05]] and the day-one scope.

~180 realistic problems a finance user (CFO / owner / accountant / AP-AR analyst) would pose to Tesote AI, each routed through the **tesote-workspace MCP**. Used to (1) QA the MCP for data-model completeness and (2) build the knowledge-base file.

Grounded in Luis's launch PRD (`luis-ideas.md`): three pillars (ask-anything / setup-en-masa / reports), the **scope line**, per-currency + BCV-rate-of-each-transaction-date dollarization, "mayo = May 1–31", "este mes" default, preview-before-mutate.

**Legend:** `→` MCP path that should answer it. **QA status** filled during QA: ✅ works · ⚠️ works-with-caveat · ❌ broken/gap · 🔲 untested.
Target QA workspace: **Tesote Finance** `19234e69-781e-45ce-a429-f2d529575a25` (33 accts, USD/VES/EUR, full access).

---

## Round-1 scope (Luis, 2026-06-18) — read before running

This pass gates the **~June 22 all-users launch** ([[launch-master-plan]]). Not everything in the catalog gates it. Tags per section:

- **`CORE`** — must pass for launch. A failure here is a launch blocker.
- **`OUT`** — excluded from round 1. Don't QA for launch. (Re-add in the wave-2 catalog.)

| Section | Tag | Note |
|---|---|---|
| A Balances | **CORE** | |
| B Cash flow / spend | **CORE** | Pillar 1 — the heart of the demo |
| C Top-N / rankings | **CORE** | |
| D Period comparisons | **CORE** | |
| E Dollarization / FX | **CORE** | The VE doctrine; non-negotiable |
| F Categorization + rules | **CORE** | Pillar 2 |
| G Counterparty | **CORE** | |
| H Reports | **CORE** | Pillar 3 |
| I Transaction search | **CORE** | |
| J Reconciliation-vs-bank | **OUT** | Recon = data-integrity check vs the bank's own truth. MCP likely doesn't expose it yet (rows are mostly "gap check"). Out of round 1; revisit when the surface exists. |
| K Bank connection / sync | **CORE** | Sync health is day-one — a stale bank breaks every other answer |
| L Intercompany transfers | **CORE** | Stays in. Real day-one need. |
| M ERP / Odoo | **OUT** | Wave 2 — connector workspaces only, manual install. Day-one V1 = Tesote workspace MCP only. |
| N Invoices (Tesote-native) / aging | **OUT** | Not in this first pass. |
| O Date semantics | **CORE → cross-cutting** | See below |
| P Scope / currency / robustness | **CORE → cross-cutting** | See below |
| Q Reliability (Behavior 0) | **CORE** | New — appended below |
| R Preview-before-execute (Behavior 5) | **CORE** | New — appended below |
| S Output choreography (Behavior 4) | **CORE** | New — appended below |

**`OUT` sections still get a smoke check:** asking an out-of-scope question must degrade *gracefully* — a clean "eso llega con la conexión Odoo / próximamente" answer, never a crash, a silent empty, or a hallucinated number. That's the only bar for J/M/N this round.

### O + P are not sections — they're assertions on every row

The original catalog lists O (date semantics) and P (scope / currency / robustness) as 13 bottom-of-the-list test cases. They're not cases — they're **invariants**. Every one of the ~150 core rows above must *also* satisfy these, or the answer fails even if the number is right. This is the trust signature from behaviors 1/2/6. Grade every core row against:

- **`SCOPE`** — answer states period + accounts + currency + row count *(P181 / behavior 1)*
- **`NO-BLEND`** — Bs and USD never share a total/column/series *(P182 / behavior 2)*
- **`PARTIAL-FIRST`** — if coverage is partial (>rows, capped), it warns **before** answering, not under cross-examination *(P183 / behavior 1)*
- **`BCV-OF-DATE`** — any dollarized figure converts each txn at the BCV of *its own date*, and names that basis *(E64 / behavior 2)*
- **`EU-FORMAT`** — `1.234.567,89` everywhere incl. prose *(P187 / behavior 6)*
- **`PERMS`** — out-of-permission accounts/fields are dropped, never widened; redaction holds *(P185–186)*
- **`STRONG-FAIL`** — unsupported option errors loudly, never silently ignored *(O178)*
- **`DATE-EXACT`** — "mayo" = May 1–31; no period → "este mes" (mtd); "este año" = Jan 1–today *(O176–180)*

Recommend the QA emit, per row, a `scope_ok / blend_ok / partial_ok / fx_basis_ok / format_ok` boolean vector — not just pass/fail on the number. The KB prompt is graded against these too.

---

## A. Balances & positions (current stock) — `CORE`
1. 🔲 ¿Cuánto tengo en total ahora mismo? (per-currency, never blended) → `account/list` sum, or `report.aggregate balance`
2. 🔲 ¿Cuánto tengo en USD y cuánto en bolívares? → `account/list` group by currency
3. 🔲 Saldo por banco → `account/list` / `report.run balance_changes_by_bank`
4. 🔲 Saldo por entidad legal (VDT, Plazafin…) → `account/list?legal_entity_name`
5. 🔲 Saldo total dolarizado al BCV de hoy → `report.aggregate balance currency_mode:usd`
6. 🔲 ¿Cuál es mi cuenta con mayor saldo? → `account/list` sort
7. 🔲 ¿Qué cuentas tengo en cero / vacías? → `account/list` filter balance=0
8. 🔲 Lista todas mis cuentas con banco y moneda → `account/list`
9. 🔲 ¿Cuántas cuentas tengo y en cuántos bancos? → `account/list` / `workspace/info`
10. 🔲 Saldo disponible vs saldo contable → `account/list` (available_balance)
11. 🔲 Posición total de la entidad X en dólares → `account/list?legal_entity` + FX
12. 🔲 ¿Cuál es mi exposición en bolívares (FX exposure)? → `report.aggregate fx_exposure` (⚠ daily_balance_snapshots empty)
13. 🔲 Evolución de mi saldo en los últimos 90 días → `report.run balance_over_time` (⚠ snapshots empty)
14. 🔲 ¿Cuánto cambió mi saldo este mes por banco? → `report.run balance_changes_by_bank`
15. 🔲 Actualiza el saldo de mi cuenta manual de caja chica → `account/update_balance` (manual only, view_balance) — **`R` preview-gate applies**

> **Doctrine note (12, 13, 71):** `daily_balance_snapshots` is empty — balance-over-time and FX-exposure-over-time will look broken. Decide before QA: is "saldo en el tiempo" a launch promise or a known-gap? If gap, the AI must say "no tengo historia de saldos aún", never return a flat/empty chart silently (`STRONG-FAIL`).

## B. Cash flow / spend totals (flows) — Pillar 1 core — `CORE`
16. 🔲 ¿Cuánto gasté este mes y en qué? (the chip) → `report.aggregate group_by:category period:mtd`
17. 🔲 ¿Cuánto ingresé este mes? → `report.aggregate group_by:none direction via measures`
18. 🔲 Flujo neto de este mes → `cash_flow/statement` / `report.aggregate`
19. 🔲 ¿Cuánto gasté en mayo? (mayo = 1–31) → `report.aggregate period:custom 05-01..05-31`
20. 🔲 ¿Cuánto le pagué a [proveedor] este año? (US-1) → `report.aggregate group_by:counterparty + filter`
21. 🔲 Gasto por categoría este trimestre → `report.aggregate group_by:category period:qtd`
22. 🔲 Ingresos vs egresos del año → `report.aggregate group_by:none period:ytd`
23. 🔲 Flujo de caja mensual del año (serie) → `report.run cash_flow granularity:monthly` / `aggregate group_by:month`
24. 🔲 Flujo diario de la última semana → `report.aggregate group_by:day period:7d`
25. 🔲 ¿En qué se me va la plata? (US-2 breakdown, "sin categorizar" loud) → `report.aggregate group_by:category`
26. 🔲 Gasto por cuenta este mes → `report.aggregate group_by:account`
27. 🔲 Gasto por banco este mes → `report.aggregate group_by:bank`
28. 🔲 Gasto por entidad legal → `report.aggregate group_by:legal_entity`
29. 🔲 ¿Cuánto gasté en nómina este mes? → `report.aggregate group_by:category` + category filter
30. 🔲 ¿Cuánto pagué en comisiones bancarias este año? → category-filtered aggregate
31. 🔲 Total de egresos en USD (solo cuentas dólar) → `aggregate account_ids:USD-set`
32. 🔲 ¿Cuánto moví en total (volumen) este mes? → `aggregate transaction_count`
33. 🔲 Flujo de caja de mayo dolarizado al BCV de cada fecha → `aggregate currency_mode:usd period:custom`
34. 🔲 Egresos por categoría en bolívares vs dólares (per-currency split) → `aggregate group_by:category per_currency`
35. 🔲 ¿Cuánto gasté el mes pasado? (mes calendario anterior completo) → `aggregate period:custom prev month`
36. 🔲 Promedio de gasto mensual del año → derived from `aggregate group_by:month`
37. 🔲 ¿Cuál fue mi mes de mayor gasto? → `aggregate group_by:month` then max
38. 🔲 Egreso total a proveedores USA este año → counterparty/category filter
39. 🔲 ¿Cuánto he gastado hoy? → `aggregate period:custom today..today`
40. 🔲 Neto por moneda del trimestre → `aggregate group_by:currency period:qtd`

> **Doctrine note (25, 81):** "sin categorizar" must surface **loud** — it's ~70% of volume and it's the hook into the rules/setup pitch, not noise to bury. An answer to #16/#25 that hides it fails even if the categorized numbers are correct.

## C. Top-N / rankings — `CORE`
41. 🔲 ¿Quiénes son mis 10 contrapartes más grandes este año? (the chip) → `report.run cash_flow_by_counterparty top_n:10` / `aggregate group_by:counterparty`
42. 🔲 Top 5 categorías de gasto este mes → `aggregate group_by:category` sort
43. 🔲 Top proveedores por egreso (outflow only) → `cash_flow_by_counterparty direction:outflow`
44. 🔲 Top clientes por ingreso (inflow only) → `cash_flow_by_counterparty direction:inflow`
45. 🔲 Mis 20 transacciones más grandes este mes → `transaction/search` sort by amount (⚠ 100-row cap — **Behavior 3 gate; see Q/I131**)
46. 🔲 ¿A quién le pago más en bolívares? → `aggregate group_by:counterparty per_currency`
47. 🔲 Top bancos por volumen de movimientos → `aggregate group_by:bank metric:count`
48. 🔲 Categoría con mayor crecimiento mes a mes → 2× `aggregate group_by:category` + diff
49. 🔲 Contraparte sin RIF con mayor volumen → counterparty + aggregate join
50. 🔲 Top 10 contrapartes dolarizadas al BCV → `aggregate group_by:counterparty currency_mode:usd`

## D. Period comparisons — `CORE`
51. 🔲 Compárame mayo contra abril (US-3, both exact calendar months) → 2× `aggregate period:custom`
52. 🔲 Este mes vs el mes pasado (MoM) → 2× aggregate
53. 🔲 Este año vs el año pasado (YoY) → 2× aggregate period:custom
54. 🔲 Q2 vs Q1 → 2× aggregate
55. 🔲 ¿Creció mi gasto en nómina respecto al mes pasado? → category-filtered MoM
56. 🔲 Variación de ingresos trimestre a trimestre → aggregate group_by:quarter
57. 🔲 Los mayores movers entre mayo y abril (biggest deltas by category) → 2× group_by:category diff
58. 🔲 Compara mi flujo de caja de este trimestre con el anterior → 2× cash_flow
59. 🔲 ¿Gasté más este mes que el promedio del año? → aggregate month vs avg
60. 🔲 Comparación dolarizada mayo vs abril (BCV de cada fecha) → 2× aggregate currency_mode:usd

## E. Dollarization / FX (Venezuela doctrine: BCV-of-each-date) — `CORE`
61. 🔲 ¿Cuál es el BCV de hoy? → `exchange_rate/current USD VES` (NOT workspace_exchange_rate)
62. 🔲 ¿Cuál era el BCV el 15 de marzo? → `exchange_rate/history` filter
63. 🔲 Histórico del BCV último mes → `exchange_rate/history`
64. 🔲 Todo lo anterior "en dólares" (per-transaction BCV-of-date) → `aggregate currency_mode:usd`
65. 🔲 ¿Tengo una tasa paralelo/contractual configurada? → `workspace_exchange_rate/list` / `configurable_status`
66. 🔲 Configura una tasa contractual de 40 Bs/USD efectiva hoy → `workspace_exchange_rate/create` (recalcs txns) — **`R` preview-gate applies (recalcs many txns — must preview impact first)**
67. 🔲 ¿Qué tasa se aplicó a esta transacción? → `transaction/show` (exchange_rate_to_usd, override)
68. 🔲 Fija una tasa manual a esta transacción → `transaction/set_manual_exchange_rate` — **`R` preview-gate**
69. 🔲 Quita la tasa manual de esta transacción → `transaction/clear_manual_exchange_rate` — **`R` preview-gate**
70. 🔲 ¿Cuánto perdí por devaluación este trimestre? → `position_decomposition` (devaluation_usd) — exposed?
71. 🔲 Mi saldo dolarizado a fin de cada mes → daily_balance_snapshots (⚠ empty — see A doctrine note)
72. 🔲 ¿Qué monedas maneja mi workspace? → `account/list` distinct currency
73. 🔲 Lista de pares de cambio disponibles → `exchange_rate/list_currencies`
74. 🔲 Cobertura USD de mis movimientos (cuántos tienen valor en USD) → `aggregate usd_coverage_pct`
75. 🔲 ¿Cuánto vale en USD lo que ingresé en Bs este mes? → `aggregate currency_mode:usd` inflow
76. 🔲 Tasa workspace vs BCV para una fecha → `workspace_exchange_rate/current on_date` (source field)
77. 🔲 Elimina una tasa de workspace y ver impacto → `workspace_exchange_rate/delete` (affected_transactions) — **`R` preview-gate (must show affected_transactions before deleting)**
78. 🔲 ¿La tasa configurable está aplicándose? → `workspace_exchange_rate/configurable_status`
79. 🔲 Dolariza el gasto por categoría del año → `aggregate group_by:category currency_mode:usd period:ytd`
80. 🔲 ¿Cuál es mi exposición neta por moneda? → balances per currency + FX

> **Doctrine note (the core of behavior 2):** every dollarized figure in E (and anywhere in A–D) converts each transaction at the **BCV of its own date**, and the answer names that basis ("al BCV de la fecha de cada transacción"). Applying today's rate to old Bs measures FX drift, not the business — that's an automatic fail (`BCV-OF-DATE`).

## F. Categorization gaps + rule proposals (Pillar 2) — `CORE`
81. 🔲 ¿Cuánto tengo sin categorizar? ("$40k sin categorizar" hook) → `aggregate group_by:category` NULL bucket
82. 🔲 Muéstrame el volumen sin categorizar por monto → category NULL aggregate
83. 🔲 Propón reglas para mis movimientos sin categorizar (the chip, US-6) → list uncategorized + propose `transaction_rule/create` — **`R` preview-gate**
84. 🔲 ¿Qué transacciones tocaría esta regla? (preview) → `transaction/search` matching rule conditions — **this IS the `R` preview surface; must show affected rows w/ per-row exclude**
85. 🔲 Crea una regla: descripción contiene "GUSTO" → categoría Nómina → `transaction_rule/create` — **`R` preview-gate**
86. 🔲 Crea regla por banda de monto (>$1000 → Inversión) → `transaction_rule/create` amount op — **`R` preview-gate**
87. 🔲 Aplica esta categoría a todas las transacciones de [contraparte] → rule with counterparty condition — **`R` preview-gate**
88. 🔲 Lista mis reglas activas → `transaction_rule/list`
89. 🔲 Edita una regla para cambiar la categoría destino → `transaction_rule/update` — **`R` preview-gate**
90. 🔲 Archiva una regla que ya no aplica → `transaction_rule/archive` — **`R` preview-gate**
91. 🔲 ¿Qué reglas asignan contraparte automáticamente? → `transaction_rule/list` filter
92. 🔲 Categoriza esta transacción específica como "Comisión bancaria" → `transaction/categorize add_category_ids` — **`R` preview-gate**
93. 🔲 Quita una categoría mal puesta de una transacción → `transaction/categorize remove_category_ids` — **`R` preview-gate**
94. 🔲 ¿Cuántas categorías tengo y cuál es la jerarquía? → `category/list` (parent_id)
95. 🔲 Crea una subcategoría bajo "Impuestos" → (category create — exposed? gap check)
96. 🔲 Reglas que cubran el 80% del volumen sin categorizar → analysis + multi rule propose — **`R` preview-gate**
97. 🔲 ¿Una transacción puede tener varias categorías? (M:N) → `transaction/show` category_ids
98. 🔲 Muestra transacciones de la categoría "Nómina" este mes → `transaction/search` (category filter?) — gap check
99. 🔲 Regla con condiciones múltiples (match all) → `transaction_rule/create conditions_match_type:all` — **`R` preview-gate**
100. 🔲 Desarchivar una regla → `transaction_rule/unarchive` — **`R` preview-gate**

## G. Counterparty master-data (US-7) — `CORE`
101. 🔲 Lista mis contrapartes → `counterparty/list`
102. 🔲 ¿Qué contrapartes no tienen RIF (external_identifier)? → `counterparty/list` filter
103. 🔲 Busca contrapartes duplicadas → `counterparty/list` + dedup analysis
104. 🔲 Crea una contraparte nueva con RIF → `counterparty/create` — **`R` preview-gate**
105. 🔲 Corrige el email de una contraparte → `counterparty/update` — **`R` preview-gate**
106. 🔲 Archiva una contraparte → `counterparty/archive` (blocks if active rules) — **`R` preview-gate**
107. 🔲 ¿Cuánto le he pagado a esta contraparte en total? → `aggregate group_by:counterparty` filter
108. 🔲 ¿Qué contrapartes fueron creadas automáticamente (auto_seniat/auto_rule)? → `counterparty/list source`
109. 🔲 Vincula esta contraparte a su partner de Odoo → `counterparty/link_external_partner` — **(Odoo-linked — verify it degrades cleanly on non-connector workspaces, per `OUT`/M smoke rule)**
110. 🔲 ¿Esta contraparte ya está vinculada a un partner externo? → `counterparty/list_external_partners`
111. 🔲 Asigna una contraparte a esta transacción → `transaction/assign_counterparty` — **`R` preview-gate**
112. 🔲 Quita la contraparte de una transacción → `transaction/assign_counterparty counterparty_id:null` — **`R` preview-gate**
113. 🔲 Transacciones sin contraparte ("Sin contraparte") este mes → `aggregate group_by:counterparty` NULL

## H. Reports (Pillar 3) — `CORE`
114. 🔲 Córreme el flujo de caja de mayo (the chip, US-9) → `report.run cash_flow period:custom`
115. 🔲 ¿Qué reportes guardados tengo? → `report/list_definitions`
116. 🔲 Guárdame esto como reporte mensual (US-10) → `report/save_definition` — **`R` preview-gate**
117. 🔲 Corre mi reporte guardado de flujo de caja → `report/run definition_id`
118. 🔲 Reporte de cambios de saldo por banco → `report.run balance_changes_by_bank`
119. 🔲 Reporte de flujo por contraparte (top 10) → `report.run cash_flow_by_counterparty`
120. 🔲 Reporte de saldo en el tiempo → `report.run balance_over_time` (⚠ snapshots — see A doctrine note)
121. 🔲 Guarda un reporte compartido para todo el equipo → `save_definition visibility:shared` — **`R` preview-gate**
122. 🔲 Programa un reporte para que llegue cada lunes → `save_definition schedule` (delivery = next release) — **scheduled delivery is post-launch; AI must say so, not fake-confirm (`STRONG-FAIL`)**
123. 🔲 Narra mi flujo de caja de este mes vs el anterior → 2× report.run + narration
124. 🔲 ¿El reporte compartido respeta mis permisos? (viewer scope) → run_saved_definition redaction — **`PERMS` invariant**
125. 🔲 Reporte ad-hoc de flujo diario de la última semana → `report.run cash_flow granularity:daily period:7d`

> **Doctrine note (behavior 4 / W7):** every workspace ships with **seeded default reports** so "córreme el flujo de caja" works in the first session — the library is never empty. The seeded list is ours to pick (Luis is dogfooding the candidates now → [[qa-pre-created-reports-2026-06-03]]). QA should run against a workspace with the seeded set present, not an empty one.

## I. Transaction search / drill-down (US-5) — `CORE`
126. 🔲 Muéstrame las transacciones de esta cuenta este mes → `transaction/search account_id`
127. 🔲 Busca transacciones que digan "transferencia" → `transaction/search description`
128. 🔲 Transacciones entre $1000 y $5000 → `transaction/search min/max_amount`
129. 🔲 Transacciones de una fecha específica → `transaction/search start=end`
130. 🔲 Detalle completo de una transacción → `transaction/show`
131. 🔲 ¿Cuántas transacciones tengo en total este año? (>100, must aggregate not list) → `transaction/aggregate` (has_more redirect) — **Behavior 3 gate: the 100-row cap must not produce a wrong total; `PARTIAL-FIRST` invariant**
132. 🔲 Drill: total → categoría → contraparte → movimientos → aggregate then search
133. 🔲 Crea una transacción manual en mi cuenta de caja → `transaction/create_manual` (manual acct, view_balance) — **`R` preview-gate**
134. 🔲 Archiva una transacción manual errónea → `transaction/archive_manual` — **`R` preview-gate**
135. 🔲 Envía el comprobante de esta transacción por email → `transaction/send_receipt_email` — **`R` preview-gate (outbound side-effect — confirm recipient + content before send)**
136. 🔲 Transacciones grandes sin categorizar este mes → search + category gap
137. 🔲 ¿Esta transacción es parte de una transferencia intercompañía? → `transaction/show` intercompany block
138. 🔲 Movimientos pendientes (status pending) → search (status filter? gap check)
139. 🔲 Última transacción en cada cuenta → per-account latest
140. 🔲 Busca un pago específico por código de referencia → search (reference_code? gap check)

## J. Reconciliation health — `OUT` (round 1) — smoke-test only
> **Excluded from launch QA (Luis, 2026-06-18).** "Recon" = data-integrity check vs the bank's own ledger. The MCP likely doesn't expose recon status yet — these rows are mostly "gap check". Run them ONLY to confirm the AI degrades gracefully ("la conciliación aún no está disponible en el chat"), never crashes or fabricates a recon verdict. Feeds the *expand-the-MCP* backlog, not the launch blocker list. Revisit for wave 2.
141. 🔲 ¿Cuáles de mis cuentas están conciliadas? → reconciliation status — exposed via MCP? (gap check)
142. 🔲 ¿Qué cuentas tienen conciliación fallida? → ReconciliationStat.health — gap check
143. 🔲 ¿Cuántas conciliaciones pendientes tengo? → gap check
144. 🔲 Salud de conciliación del workspace → gap check (no MCP resource)
145. 🔲 ¿Por qué falló la conciliación de esta cuenta? → failure_diagnosis — gap check
146. 🔲 ¿Cuál es la diferencia entre mi saldo y el del banco? → reconciliation balance diff — gap check
147. 🔲 Cuentas con conciliación habilitada → account reconciliation_enabled — gap check
148. 🔲 Última fecha conciliada por cuenta → gap check

## K. Bank connection / sync — `CORE`
149. 🔲 ¿Cómo están mis conexiones bancarias? → `bank_connection/status`
150. 🔲 ¿Qué bancos no se han sincronizado recientemente? → `bank_connection/status` last_synced_at
151. 🔲 ¿Hay conexiones fallidas? → `bank_connection/status` status=failing
152. 🔲 Sincroniza mi conexión de Citibank → `sync/trigger` (api only, rate-limited) — **`R` preview-gate (action with side-effect + rate limit)**
153. 🔲 ¿Por qué no puedo sincronizar mi banco venezolano? → `sync/trigger` decline (webscraper)
154. 🔲 ¿Cuándo fue la última sincronización de cada banco? → `bank_connection/status`
155. 🔲 ¿Cuántas cuentas trae cada conexión? → `bank_connection/status` accounts_count
156. 🔲 ¿Qué conexiones son API vs scraper vs manual? → `bank_connection/status` integration_type

> **Why K stays in (Luis):** a stale/failing bank silently poisons every balance and cash-flow answer above. The AI must be able to say "ojo, [banco] no sincroniza desde [fecha]" so the user trusts (or distrusts) the numbers. Sync transparency is part of the trust signature, not a side feature.

## L. Intercompany transfers — `CORE`
157. 🔲 Muéstrame mis transferencias intercompañía → `intercompany_transfer/list`
158. 🔲 Transferencias entre mis entidades este mes → `intercompany_transfer/list` date filter
159. 🔲 Transferencias con contraparte pendiente (one-sided) → `list only_pending_counterpart`
160. 🔲 ¿Cuánto moví entre cuentas internamente? → intercompany sum
161. 🔲 Transferencias de salida (outflow direction) → `list direction:outflow`
162. 🔲 ¿Esta transferencia es same-entity o cross-entity? → list (kind)

## M. ERP / Odoo — `OUT` (wave 2) — smoke-test only
> **Excluded from round 1.** Day-one V1 = Tesote workspace MCP only; Odoo is wave 2, connector workspaces, manual install. On a non-connector workspace, every M row must answer cleanly ("Disponible con la conexión Odoo"), never crash or hallucinate ERP data. Row 169 IS that smoke test.
163. 🔲 ¿Tengo conexión Odoo? → `erp_console/list_pipelines`
164. 🔲 Muéstrame mis facturas de cliente abiertas en Odoo → `erp_console/invoices`
165. 🔲 ¿Cuánto me deben mis clientes (AR)? → erp_console invoices residual
166. 🔲 Concilia esta línea bancaria con su factura → `erp_console/match_bsl_to_invoice` (dry-run default)
167. 🔲 Genera la factura de suscripción de este pedido → `erp_console/generate_subscription_invoice`
168. 🔲 Aplica tasa BCV a esta factura USD borrador → `erp_console/apply_rate_to_usd_invoice`
169. 🔲 (workspace sin Odoo) → "Disponible con la conexión Odoo" (handler not visible) — **the graceful-degradation smoke test for all `OUT` sections**

## N. Invoices (Tesote-native) / AR-AP aging — `OUT` (round 1)
> **Excluded from this first pass (Luis, 2026-06-18).** Smoke-test only: must degrade gracefully, never fabricate aging buckets or invoice state.
170. 🔲 Lista mis facturas → `invoice/list`
171. 🔲 Facturas sin pagar (payment_state) → `invoice/list payment_state:not_paid`
172. 🔲 Crea una factura de cliente (dry-run preview) → `invoice/create live:false`
173. 🔲 Antigüedad de cuentas por cobrar (aging buckets 0-30/30-60/...) → gap (compute from invoice due_date)
174. 🔲 ¿Cuánto vence esta semana? → invoice/list due_date filter — gap check
175. 🔲 Postea una factura borrador → `invoice/post`

## O. Date semantics & option-honesty — `CORE → cross-cutting` (see top: `DATE-EXACT` / `STRONG-FAIL`)
> Keep these as explicit rows AND grade them on every other core row.
176. 🔲 "mayo" devuelve exactamente 1–31 mayo (not trailing 30d) → resolve_preset custom auto-promote
177. 🔲 Sin periodo especificado → default "este mes" (mtd), named in scope → default preset mtd
178. 🔲 Opción no soportada → error fuerte, nunca ignorar silenciosamente → invalid group_by/currency_mode raises
179. 🔲 "este año" = 1 enero–hoy (ytd) → preset ytd
180. 🔲 Rango custom con start+end exactos honrados → custom window

## P. Scope-line / currency-discipline / robustness — `CORE → cross-cutting` (see top: the invariant vector)
> These are the trust signature. Keep as rows AND grade on every core row.
181. 🔲 Toda respuesta numérica trae scope (periodo, cuentas, moneda, conteo) → scope envelope every aggregate/report — **`SCOPE`**
182. 🔲 Nunca mezclar Bs y USD en un total → per_currency default — **`NO-BLEND`**
183. 🔲 Respuesta parcial (>filas) avisa ANTES → has_more / more_exists / partial flags — **`PARTIAL-FIRST`**
184. 🔲 Una consulta no puede tumbar la plataforma → query timeout 15s guard — **see Q (Behavior 0)**
185. 🔲 Redacción por permisos: usuario sin view_credit → inflow nil → ResolveFieldVisibility — **`PERMS`**
186. 🔲 Scope de cuentas: IDs fuera de permiso se descartan, nunca amplían → PermittedAccounts intersect — **`PERMS`**
187. 🔲 Formato europeo de números (1.234.567,89) → presentation layer (KB note) — **`EU-FORMAT`**
188. 🔲 Workspace sin datos → respuesta vacía limpia, no error → empty_result

---

## Q. Reliability — Behavior 0 (NEW, `CORE`) — "it stays up, and it finishes what it starts"
> Added 2026-06-18. The original catalog had zero coverage of behavior 0 — yet P1 (outage) and P2 (token expiry mid-confirmation) are the hardest launch gates. No analytical behavior matters if the surface is unreliable.
189. 🔲 Una consulta pesada (año completo, 33 cuentas, group_by) no degrada ni tumba la app → worst case = "la IA se disculpa", nunca "Tesote no responde" (P1)
190. 🔲 Una confirmación pendiente sobrevive el límite de conversación → si el chat llega a su límite, la aprobación pendiente NO muere (P2 — the integrity guarantee behind every `R` preview)
191. 🔲 Si la IA no puede terminar, lo dice explícitamente → nunca declara "listo" sin output
192. 🔲 Consulta ambigua o sin datos → respuesta limpia, no excepción cruda al usuario
193. 🔲 Timeout de 15s se respeta y devuelve mensaje claro, no cuelga la sesión (ties to P184)
194. 🔲 Pregunta fuera de alcance (J/M/N) → degrada con gracia, nunca crash ni número inventado (the `OUT` smoke bar, consolidated)

## R. Preview-before-execute — Behavior 5 (NEW, `CORE`) — "propose → inspect → approve → execute"
> Added 2026-06-18. The original catalog tested whether mutations *work*, but not whether they *preview first*. Every mutating row above is tagged `R`. These rows test the pattern itself as a universal invariant.
195. 🔲 Toda mutación (categorizar, crear regla, editar contraparte, tasa, manual txn, enviar email) renderiza un artefacto de preview en el panel derecho ANTES de ejecutar
196. 🔲 El preview muestra las filas afectadas con exclusión por-fila ("inspeccionar 47 matches → Excluir")
197. 🔲 Aprobar ejecuta EXACTAMENTE lo previsualizado → el audit trail registra propuesto-vs-ejecutado
198. 🔲 Una acción masiva (regla que toca cientos de txns, recálculo de tasa #66/#77) muestra el conteo de impacto antes de confirmar
199. 🔲 Ninguna acción del lado-workspace (bulk) se salta el gate → audit which workspace-side mutations currently skip preview
200. 🔲 Cancelar en el preview no deja efectos parciales (atomicidad)

## S. Output choreography — Behavior 4 (NEW, `CORE`) — "reports come out right, in the format the user wants"
> Added 2026-06-18. The table-or-chart-or-both choreography from the contract wasn't tested.
201. 🔲 Al producir un reporte/serie, la IA pregunta o devuelve por defecto AMBOS: tabla + gráfico (ambos renderers ya existen)
202. 🔲 "Muéstramelo como gráfico" / "como tabla" se honra → no ignora la preferencia
203. 🔲 Una serie temporal (flujo mensual, #23) se ofrece como gráfico, no solo tabla cruda
204. 🔲 El gráfico respeta `NO-BLEND` → series por moneda separadas, nunca Bs+USD en un mismo eje

---

## Appendix — Gold-standard answer templates (Luis's voice, for the KB-prompt output)

The QA's second output is the knowledge-base prompt that teaches agents how to answer. Grading answer *quality* needs gold phrasing. These are the doctrine templates — the KB prompt should reproduce this register:

**Scope envelope (every numeric answer ends or opens with this):**
> *"Sobre 1.432 movimientos, ene–may 2026, 3 cuentas USD."*
Period + accounts + currency + count. Non-negotiable.

**Dollarization basis (whenever a Bs figure is shown in USD):**
> *"…al BCV de la fecha de cada transacción."*
Never "al BCV de hoy" applied to history.

**Partial coverage (stated BEFORE the number, not when challenged):**
> *"Ojo: hay más de 100 movimientos en este rango; te doy el total agregado, no el detalle fila por fila."*

**"Sin categorizar" surfaced loud:**
> *"De tus egresos de mayo, $40.231,00 (≈68%) están sin categorizar. ¿Quieres que te proponga reglas para clasificarlos?"*
It's the hook into Pillar 2, never buried.

**Stale-sync warning (behavior K):**
> *"Ojo: Banco Exterior no sincroniza desde el 2026-06-14, así que este saldo puede estar desactualizado."*

**Out-of-scope graceful degrade (J/M/N):**
> *"La conciliación contra el banco aún no está disponible en el chat — te aviso cuando lo habilitemos."* / *"Eso llega con la conexión Odoo."*

**Strong-fail on unsupported option:**
> *"No puedo agrupar por '[x]' — las opciones disponibles son: categoría, contraparte, banco, cuenta, entidad, mes, día. ¿Cuál quieres?"*
Never silently return an ungrouped answer.

> **Number format throughout:** `Bs. 5.445.475,00` / `$1.234,56` — European grouping in prose, tables, charts, tooltips. One formatter, zero hand-formatted money.
