---
title: Brain → Treasury — the implementation bridge
tags: [workflow, treasury, tesote-plan, claude-code]
updated: 2026-05-18
status: active
---

# Brain → Treasury — the implementation bridge

When a brain doc matures past prose framing into something that'll become code, the next step is **`/tesote-plan` in the treasury repo**, not a copy to the KB. The skill ingests the brain spec + a Linear ticket and produces a structured implementation plan grounded in the actual treasury codebase. Skip this step and Dan/team manually re-derive schema, services, multi-tenant impact from prose.

Sourced from a session with Dan on 2026-05-17. Memory: [[feedback_tesote_plan_workflow]].

---

## What `/tesote-plan` actually is

A slash command in `~/Programming/tesote/treasury/.claude/commands/tesote-plan.md`. Takes a free-form goal **or a Linear URL** and produces a plan directory at `treasury/.debugging/plans/[name]/` containing:

> **Handoff step (Dan's directive, 2026-06-11):** `.debugging/` is local — don't hand plans from there. After `/tesote-plan`, **copy the plan dir to `docs/plans/[name]/` in a treasury PR**, include the design contract in the same PR when it's UI work (HTML wireframes + design-system doc + recon doc), and **link Dan to the PR**. The PR *is* the handoff.

- `CONTEXT.md` — keyword/file:line map for an LLM to inject (read first)
- `summary.md` — 1–2 sentences
- `TODO.md` — phased, checkboxed, with `file:line` refs
- `DEPENDENCIES.md` — order + parallelizable work
- `index.md` + (complex plans) `plan-database.md`, `plan-services.md`, `plan-api.md`, `plan-client.md`, `plan-testing.md`, `VERIFICATION.md`

Before finalizing, it runs **mandatory architecture-review** checklists:

- **Scale** — rows in 6 months, per-row loops, batch jobs, JSONB-vs-normalized
- **Multi-tenant / privacy** — cross-workspace leakage, names/amounts leaking
- **Concurrency / idempotency** — locks, dedupe, split/duplicate risks
- **Security** — PII, auth, data-export paths
- **Index planning** — every WHERE clause covered, partial/GIN indexes
- **Post-release validation** — PRO-* monitoring ticket with 24h / 1-week checks

And it enforces Treasury's coding standards (SOLID, TDD, model+factory+seed+spec for every new table, no `rescue StandardError`).

The output is **explicitly LLM-optimized** — designed so `/implement` (the sibling command) can pick it up and start coding without re-reading the world.

---

## Why this is the right bridge

The last two weeks of brain output — [[../product/tesote-2026-command-center-prd|Command Center PRD]], business/pagos super-app, AR cockpit, filter primitive, design-system locked decisions, tier convention — are gorgeous as product framing and **invisible to the treasury codebase**.

Today the gap is closed manually: Luis hands prose to Dan, Dan re-derives schema / services / multi-tenant / security / index implications, files Linear tickets, then engineers implement.

`/tesote-plan` is the translation step. Run it once and the output is:

1. A design+tech plan grounded in actual `file:line` references in treasury
2. The architecture-review checklist already filled in
3. A directory `/implement` can consume

Dan gets to review a real plan, not redo the work.

It's also the only command that wires brain work to treasury's other skills — `database-design`, `redesign-2026-design-system`, `product-management`, `using-knowledge-base`, `using-linear`. They're inert until something pulls them in. `/tesote-plan` does.

---

## The workflow

Three repos, three modes — be deliberate about which you're in:

| Mode      | Repo                | Output                                                |
|-----------|---------------------|-------------------------------------------------------|
| Thinking  | `luis-brain/`       | drafts, PRDs, prototypes, raw takes                   |
| Sharing   | `knowledge-base/`   | polished team reference                               |
| Building  | `treasury/`         | `/tesote-plan` → `.debugging/plans/` → `/implement`   |

For each brain doc that crosses the "this is becoming code" threshold:

1. In `luis-brain/`, start the PRD/spec from **[`product/_prd-template.md`](../product/_prd-template.md)**. The "Tesote-Plan Intake" block at the top is the contract — `/tesote-plan` reads it mechanically. Rest of the PRD can sprawl in Luis's natural shape (long-form, ASCII diagrams, open decisions tables).
2. File the Linear PRO-* ticket (from anywhere — Linear MCP is loaded). Paste the Intake block + the relevant PRD sections into the description.
3. `cd ~/Programming/tesote/treasury`, then run `/tesote-plan <Linear URL>`. The skill pulls the ticket, runs Explore over treasury, runs the architecture-review checklists, writes the plan directory.
4. Review `CONTEXT.md` + `TODO.md`. If it's wrong, the brain PRD was wrong — fix at the source, not in the plan files.
5. Hand the plan path to Dan, or run `/implement` if it's a feature shipping in this session.

The rule lives in [`../CLAUDE.md`](../CLAUDE.md) → "Relationship to treasury (implementation bridge)" so Claude enforces it in every brain session.

### For prototypes specifically

Pair `/tesote-plan` with the `redesign-2026-design-system` skill in the same treasury session. That skill catches every Mercury pastel / Tailwind default / wrong radius / wrong font (Inter without "Tight") before it's coded. It will eat the drift in the existing 15 prototype HTMLs.

### Three-terminal-moves rule

Every product-design session ends with one of:

- (a) keep drafting in brain
- (b) promote to KB (team reference)
- (c) `/tesote-plan` in treasury (becoming code)

If none apply, the session isn't done. Schedule the next move; don't close the loop.

---

## Compound moves

1. **Pre-format PRDs against the intake schema.** Use [`product/_prd-template.md`](../product/_prd-template.md) from the start. Then step 3 is mechanical.
2. **Decisions in [`decisions/`](../decisions/), not scattered drafts.** Path A typography, locked pill family, tier numbering, command center architecture (2026-05-12) all belong as discrete decision files with date + why + links to relevant treasury skills. Future-Claude finds them.
3. **Linear MCP from within `luis-brain/`.** No need to leave the brain repo to file the ticket.
4. **Pair with `/schedule` or `/loop` for long-running plays.** Mariel dogfood checkpoints, BNC weekly status, CAPCA milestones — plan-now-and-check-back. Schedule the check-in when the plan is created.
5. **Don't let skills go invisible.** CLAUDE.md should flag `/tesote-plan` proactively when a brain doc has eng/UI implications and name which treasury skills the run will pull in (`database-design`, `redesign-2026-design-system`, `product-management`, `using-linear`, `using-knowledge-base`).

---

## First dry-run (planned 2026-05-18)

Saldos (Cuentas) redesign — the lightest first run. Mostly a visual/styling pass, so architecture-review checklists should mostly come back as "n/a — read-only surface, no new tables." Anything beyond that is signal worth catching.

Sequence: draft `product/connect/saldos/saldos-prd.md` from the template → resolve the "Before I run /tesote-plan" decisions list → file PRO ticket → run `/tesote-plan <URL>` in treasury → review `CONTEXT.md` + `TODO.md` with Dan.

Second target if the loop runs clean: [[../product/tesote-2026-command-center-prd|Command Center PRD]] (already 80% template-shaped; will exercise the architecture-review checklists at full scope).

---

## Related

- [[reference_treasury_repo]] — sibling Rails app, data-model source of truth
- [[project_tesote_command_center]] — second dry-run candidate
- [[project_tesote_vs_odoo_split]] — split rule that should appear in `CONTEXT.md` of any cross-system plan
- [[feedback_tesote_plan_workflow]] — memory entry for Dan's directive
- [[../CLAUDE.md]] → "Relationship to treasury (implementation bridge)" — enforces this workflow in every brain session
- [[../product/_prd-template.md]] — PRD template; the Intake block is the contract `/tesote-plan` ingests
