# Dashboard

The cockpit. Treat as a product surface in its own right — the cross-product workspace experience that ties Connect, Business, Automations, etc. together.

## Live docs

- [[reports-catalog]] — **first-principles catalog** of banking-data reports a pro finance team consumes (daily/weekly/monthly × position/flow/control/projection/evidence). The "what to build" menu, verified against shipped MCP primitives. 2026-06-03.
- [[daily-position-pack-prd]] — **build #1: Posición Diaria.** Daily delivered cash-position brief with the flows-vs-devaluación Δ decomposition (exact identity, ε residual as data-quality signal). v0 = agent-to-Slack dogfood this week, zero product code. 2026-06-03.

## Prototypes

See [[prototypes/README]] for the full series log, constraints, content inventory, and current state.

- **`prototypes/README.md`** — series handoff doc. Read first when resuming.
- `prototypes/dashboard-v2.html` — **PREFERRED direction** (Luis, 2026-06-08). Banking command center built from landing-page (`v41`) component vocabulary. Banking-data only, no ERP.
- `prototypes/posicion-box-v1.html` — **current focus**: the v2 Posición box extracted to an isolated canvas for fast iteration before the full page is rebuilt around it.
- `prototypes/dashboard-v1.html` · `dashboard-v3.html` — earlier directions (cockpit posición-first; single-box bento + cash-flow-by-category). Superseded by v2.
