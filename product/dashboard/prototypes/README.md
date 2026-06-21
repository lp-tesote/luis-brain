# Dashboard (Inicio) redesign — prototype series

Redesign of the Tesote workspace **dashboard / home (Inicio)**. Third surface in the
2026 redesign sweep after **Saldos v4** and **Movimientos v7** — same locked design
system and app shell.

## Hard constraints

- **Banking data only — no ERP data.** Everything must be derivable from the bank feed:
  balances, transactions, FX/BCV, categories, counterparties, sync status. No invoices,
  no AR aging, no reconciliation-to-invoice, no Bandeja/approvals.
- **Design system = locked Lunour tokens**, identical to Saldos/Movimientos. Cream surfaces,
  `#1661E2` primary, warm grays, 4/8/12 radii, status-pill family, Geist Mono numbers,
  Inter Tight display. No emojis — inline SVG only. Spanish, **tú** (VE dialect).
- Component vocabulary borrowed from marketing landing page **`marketing/landing-page/v41-homepage.html`**
  (hero-panel, IA subcard, stat-grid, chip/bar lists) so product ↔ marketing read as one family.

## Versions (newest learning last)

| File | Direction | Verdict |
|---|---|---|
| `dashboard-v1.html` | Posición-first cockpit: position table by entity w/ per-account flujos/devaluación columns + exceptions + freshness + delivery banner | superseded |
| `dashboard-v2.html` | **Banking command center** — landing-page vocabulary. Position hero (figure + spark + Δ-decomp + Moneda/Entidad/Banco toggle) + weekly AI summary rail + 3 KPIs + categories + top movements | **PREFERRED (Luis, 2026-06-08)** |
| `dashboard-v3.html` | Single-box bento; aggregated USD/Bs balances on top; cash-flow-by-category (direct method) replacing flat category bars | rejected in favor of v2 |
| `posicion-box-v1.html` | The v2 first box (Posición), extracted to an isolated canvas (~740px). | superseded |
| `posicion-box-v2.html` | Posición restructured: USD/VES promoted to always-visible boxes (Bs-first), Desglose opened to banco/entidad/cuenta (no toggle) | superseded |
| `posicion-box-v2-gallery.html` | 10 compositions of the box (3-col, split-bar, rail, unified table, dense, banco-primary, bento, stacked sections…) | exploration |
| `posicion-box-v3.html` | The box at true hero width + **Tesote AI copilot** beside it; Desglose trimmed to banco+entidad; accounts moved out | direction adopted |
| `posicion-box-graph-gallery.html` | 10 graph-forward takes (position as a large chart): area, axes, stacked composition, bars, annotations, overlay, callout, **decomp band (v8)**, baseline, sparse | exploration → **v8 chosen** |
| `posicion-box-v8-final-gallery.html` | 10 refinements of v8 (beginning-balance marker + reordered band); **v1 chosen** (gradient area + start-balance dot, clean band) | selection |
| `dashboard-v4.html` | Full page = v2 base + graph-forward Posición hero (v8/v1) + Tesote AI panel + cash-flow-by-category report + Saldos por cuenta list. Workspace identity (logo + name) in header. | superseded by v5 |
| `dashboard-v5.html` | **CURRENT — SIGNED OFF (Luis, 2026-06-09).** v4 + page-head stripped to logo+name (no date/tagline/En-vivo/Personalizar); Variación neta same size as band, kept blue; Por moneda badges removed; USD sub-line removed; VES `≈ $` enlarged (14px); Saldos box spacing fixed; **entity name (≤15ch, grey) in Saldos meta** between last4 and currency. | **FROZEN** |

## Current state (2026-06-09, session 3 — visual FROZEN)

- **`dashboard-v5.html` is the signed-off, frozen visual.** Luis approved 2026-06-09; box-by-box PRD detail is now written against it ([[../dashboard-prd]]). v4 kept for the diff; v2 stays as the clean baseline.
- **Session-3 changes (v4 → v5):** page head = logo + workspace name only; Variación neta normalized to band size (still blue); currency badge squares removed; USD "2 cuentas · Mercury" sub-line removed; VES dollarized `≈ $` enlarged; Saldos box gets even row spacing; Saldos meta now carries the **entity name (grey, body font, 15-char cap, full name on hover)** between last-4 and currency.

### Prior state (2026-06-08, end of session 2)

- **`dashboard-v4.html` was the working full page.** v2 stays as the preferred clean baseline (per versioning convention — preserve original, iterate in a sibling).
- **Posición hero is now graph-forward:** big consolidated-USD area chart (30 d) with the **beginning balance ($490.550) marked on the curve** + end dot; a **decomposition band** (Entró · Salió · **Variación neta** · Devaluación) that reconciles to the chart (begin + neta − devaluación = today; the `+$31.290 · 30 d` chip); then **Por moneda** (USD; **VES shown in Bs with the dollarized amount below**) and **Desglose** (banco + entidad only — accounts live in their own list at the bottom).
- **Tesote AI** lives in the hero's right column: catchy serif line + a **pre-generated week-to-date report** (insights) + 3 prompt buttons + input. Name is **Tesote AI** (not IA), no "Copiloto" badge. See [[feedback_tesote_ai_naming]].
- **Categorías box → cash-flow report** (direct method: créditos − débitos by category, net headline). **Saldos por cuenta** is now a list at the bottom. KPI cards carry explicit date ranges.
- **Three time windows coexist on the page** (chart/band = 30 d, Entró/salió KPI = week, cash-flow = month) — each labeled; make a deliberate call at PRD time.

### Open / next
- Decide whether to keep the last divider line (chart → band) — currently kept.
- Hero height vs Tesote AI column balance: box is tall; AI stretches to match (input pinned via flex spacer).
- **Terminal move:** `/tesote-plan` in treasury + `redesign-2026-design-system`. The **Δ-decomposition** (flujos vs devaluación vs ε) and **cash-flow-by-category (direct method)** and **recurrence detection** are NOT shipped primitives — the PRD must flag them.

## Luis's content inventory (the 9 data points — all banking-derived)

1. Balances by currency  2. by entity  3. by bank  *(v2 folds these into one Moneda/Entidad/Banco toggle)*
4. Money in/out (week)  5. Categories → **build as a cash-flow-by-category report** (see v3 attempt)
6. Top movements (30d)  7. New counterparties / new transaction types  8. % transactions categorized
9. Weekly AI summary box (liked in v2/v3)

Plus the **Δ decomposition** (Δ ayer / Flujos / Devaluación / Sin explicar) — Luis likes it;
placement still open (hero strip in v2/v3; could be its own box).

## Backend gaps to flag in the eventual PRD

Two of the most differentiated elements are **not shipped primitives** (prototype mocks them):

- **Δ-decomposition** (flujos vs devaluación vs ε residual) — pure math over shipped data, exposed nowhere.
- **Recurrence detection** (próximos débitos recurrentes) — flagged "missing" in `../reports-catalog.md`.

See `../daily-position-pack-prd.md` (the decomposition identity + worked example) and `../reports-catalog.md`.

## Mock-data convention (keep consistent across versions)

- Consolidated position **$521.840,17 USD**.
- USD holdings **$457.109** (Mercury Checking $312.400 + Treasury $144.709).
- Bs holdings **Bs 36.161.741,48 ≈ $64.731** at BCV 558,6436.
- Entities: **Tesote Technologies Inc.** (US, USD) + **TST Servicios y Consultoría** (VE, VES).
- Banks: Mercury (US), BNC / Mercantil / Banesco / Bancamiga (VE).
- BNC row mirrors the `daily-position-pack-prd` worked example (+$8.950 flow, −$271 devaluación).
- All breakdowns reconcile to the $521.840 total.

## Terminal move (per repo CLAUDE.md)

Once the page design settles: write `../dashboard-prd.md` (use `product/_prd-template.md`,
fill the Tesote-Plan Intake block) → file PRO-* ticket → `/tesote-plan` in treasury,
paired with the `redesign-2026-design-system` skill.

## References

- Shell + tokens: `../../connect/movimientos/prototypes/movimientos-v7-retrofit.html`, `../../connect/saldos/prototypes/saldos-v4-retrofit.html`
- Design decisions: `../../design/workspace-design-decisions.md`
- Landing-page component source: `../../../marketing/landing-page/v41-homepage.html`
- Command-center layout reference (ERP-heavy, IA inspo): `../../business/pagos/prototypes/pro-112/workspace-shell-v2-command-center.html`
