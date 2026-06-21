---
title: [TITLE]
tags: [product, prd, ...]
updated: YYYY-MM-DD
status: draft | ready-for-tesote-plan | filed-as-ticket | implementing | shipped
audience: Luis (primary), [reviewers]
author: Luis Pulgar (synthesis with Claude)
linear: [URL once filed]
tesote_plan_dir: [path once /tesote-plan run]
---

# [TITLE]

> **One-line purpose.** [What this PRD synthesizes / proposes. One sentence.]

---

## Tesote-Plan Intake

> **Treasury's `/tesote-plan` ingests this block.** Six fields. Keep tight even if the rest of the PRD sprawls. Match the format exactly — `/tesote-plan` reads it mechanically.

### Actor & Problem

As a **[specific actor — Mariel / a Tesote workspace admin / a Tier 1 counterparty / a CS agent / Dan / ...]**, I need to **[specific action]** because **[specific problem today — what's broken / what's the manual workaround / what's the cost of doing nothing]**.

### The Test

This solves **[problem]** for **[actor]** in **[workstream — Cobros / Pagos / Connect / Contabilidad / Contrapartes / IA / Capital / Workspace / ...]**. Without it: **[what specifically happens — Mariel stays in Excel, customer drops at portal, retention voucher gets lost, ...]**.

### V0 — Simplest thing that works

- [ ] [Specific, testable condition — "Mariel can upload a vendor invoice PDF and approve it inside Tesote" not "AP automation"]
- [ ] [Another condition]
- [ ] [Another condition]

### Out of Scope (explicit "Not Doing")

- [Thing that sounds related but isn't V0 — name it explicitly to kill scope creep]
- [Feature creep we're deliberately avoiding]
- [Future-phase stuff that belongs in V1.1+]

### Technical Requirements

- [ ] Feature-flagged (if customer-facing): `flag_name`
- [ ] Permissions (if access-controlled): `permission_name`
- [ ] Spanish copy (if user-facing)
- [ ] Idempotent (if background processing — safe to re-run)
- [ ] Multi-tenant safe (`workspace_id` on all new tables; no cross-workspace leakage)
- [ ] Audit trail (financial data — soft delete only, never hard delete)
- [ ] [Other constraints from `redesign-2026-design-system` if UI work]

### Rollout Plan

1. **Internal** — Tesote Finance (Mariel) dogfoods on real workspace data → verify
2. **Beta** — N named workspaces with hand-holding → validate
3. **GA** — feature flag flipped for all

---

## Context (why now)

[Why this PRD exists. What discovery / Mariel sync / customer signal / bank conversation triggered it. Paste the raw context — Claude will tidy if needed.]

---

## Architecture / Design

[ASCII boxes, schema sketches, flow diagrams, wireframe references. Use as much or as little as needed. Long-form is fine here; the Intake block above is what `/tesote-plan` consumes — this section is for human readers (you, Dan, Majo).]

---

## Surfaces affected

[Which sidebar sections (Connect / Negocios / Automatizaciones / IA / Espacio de Trabajo), which existing components, which new screens. Map to the workspace-shell IA from the Command Center PRD.]

---

## Data model implications

[New tables / fields / relationships. Counterparty schema impact. Multi-entity considerations. Cross-reference [[reference_finance_db_schema]] for canonical schema and [[project_tesote_vs_odoo_split]] for the SoR-vs-execution split (which fields live in Tesote, which in Odoo).]

---

## AI / automation implications

[Where AI shows up — utility under the hood, surface in Tesote IA, or both. Read-first / write-with-confirmation defaults. If pure automation (rules engine, scheduler), say so.]

---

## Open decisions

| # | Decision | Owner | Status |
|---|----------|-------|--------|
| 1 | [decision] | Luis / Dan / Majo / Mariel | Open / Deferred / Resolved [date] |

---

## Path forward

### V1 wedge

[The smallest cut that proves the architecture or unblocks the next step. One paragraph. If V1 is what's in the Intake block above, just say "see Intake — V0 is the wedge."]

### What sequences after v1

```
v1   (QX)  — [description]
v1.1 (QX)  — [description]
v2   (QX)  — [description]
```

### Discipline calls

[What slips to free bandwidth. Be explicit — "Capital surface defers to v3+", "DR/US entities wait for VE proof", etc.]

---

## References

### Internal source docs (this PRD draws from)

- [[...]]

### External

- Linear ticket: [URL once filed]
- Treasury plan dir: [path once `/tesote-plan` run]
- [Other links — Notion, Figma, Slack threads, Fireflies recordings]

### Memory references (load-bearing context)

- [[...]]

---

## Appendix (optional)

[Glossary, edge cases, dropped alternatives with reasons, future-state sketches.]

---

*Template lives at `product/_prd-template.md`. Sourced from the `product-management` skill's Acceptance Criteria + treasury's `/tesote-plan` architecture-review intake. See [[../_workflows/brain-to-treasury]] for the full workflow.*
