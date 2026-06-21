---
title: Brain → KB Flow (Operating Manual)
tags: [ops, brain-kb, workflow]
updated: 2026-04-19
status: draft
---

# Brain → KB Flow

How content trickles from a Claude conversation into the right home. Brain is the workshop. KB is the showroom. Nearly everything starts here.

## The flow

```
                    ┌──────────────────────────┐
                    │   CLAUDE CONVERSATION    │
                    │    (any session)         │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                 ╔══════════════════════════════╗
                 ║  Does the output have a      ║
                 ║  clear function home?        ║
                 ╚══════════════════════════════╝
                        │                  │
                    YES │                  │ NO
                        ▼                  ▼
          ┌──────────────────────┐   ┌──────────────────────┐
          │ Writes to matching   │   │ Lands in drafts/     │
          │ function folder      │   │ (or daily/ if it's   │
          │ (sales/, product/,   │   │ time-stamped).       │
          │ customer-experience/ │   │ Raw, unfiltered.     │
          │ etc.) — still a      │   │                      │
          │ brain-side draft.    │   │                      │
          └──────────┬───────────┘   └──────────┬───────────┘
                     │                          │
                     │              ┌───────────┘
                     │              │
                     │              ▼
                     │   ┌────────────────────────────┐
                     │   │ Draft matures → "assigned" │
                     │   │ to a function folder.      │
                     │   └────────────┬───────────────┘
                     │                │
                     ▼                ▼
          ┌──────────────────────────────────────────┐
          │   brain/<function>/<file>.md             │
          │   Polished? → MANUAL COPY to KB          │
          │   (same-named folder, if function        │
          │   mirror exists).                        │
          └────────────────┬─────────────────────────┘
                           │
                           ▼
          ┌──────────────────────────────────────────┐
          │   knowledge-base/<function>/<file>.md    │
          │   (team-shared, pushed to GitHub)        │
          └──────────────────────────────────────────┘
```

## Destinations

| Signal | Destination |
|---|---|
| Skill w/ enforced schema (`/post-intro`, `/post-discovery`, `/workspace-review`, `/proposal`) | Matching brain function folder at v0.1 — still a draft, don't ship yet |
| Thought has no clear audience yet | `brain/drafts/` |
| Topic is clear but still for you only | `brain/<function>/` |
| Team needs it + quality threshold met | Copy brain → KB, same-named folder |
| Time-stamped / process (meeting notes, decisions) | `brain/daily/` or `decisions/`, rarely promoted |
| Raw notes on a person | `brain/people/`, rarely promoted |
| Skill-building / learning | `brain/learnings/`, rarely promoted |

## Function folder mirror

| Brain | KB |
|---|---|
| `sales/` | `sales/` |
| `product/` | `product/` |
| `marketing/` | `marketing/` |
| `customer-experience/` | `implementation/` + `customer-success/` |
| `legal/` | (engineering ADRs if applicable) |
| `finance/` | — |
| `ops/` | `ops/` |
| `strategy/` | — (strategy is brain-only) |

## Trigger points — when Claude should prompt you

### Entry triggers (conversation → file)

**1. Substantive content emerges with no destination.**
Signal: >~100 words of real thinking with nothing on disk.
Prompt: *"This is real content now. Park it in `drafts/`, or does it have a home already?"*

**2. External input lands (transcript, email, Slack thread, doc paste).**
Signal: raw material dropped into the session.
Prompt: *"Skill case (`/post-intro` etc.) or unstructured (→ `daily/` or `drafts/`)?"*

**3. Memory is ballooning with a topic that deserves a file.**
Signal: 3rd or 4th memory on the same subject, or a single memory turning into a mini-doc.
Prompt: *"`project_X` memory is getting long. Promote content to `drafts/X.md` and keep memory as a pointer?"*

### Assignment triggers (drafts → function folder)

**4. A draft has stabilized around one topic.**
Signal: returning to `drafts/X.md` across sessions; audience/function now obvious.
Prompt: *"This draft has settled into a product topic. Move to `product/` with a proper filename?"*

**5. A draft starts touching multiple functions.**
Signal: half sales-objection, half product-spec.
Prompt: *"This straddles sales + product. Primary home, or split?"*

### Promotion triggers (brain → KB)

**6. Brain content reads team-ready.**
Signal: polished prose, absolute dates, no first-person hunches, links to other docs. `status: ready-for-kb` in frontmatter.
Prompt: *"`brain/<function>/X.md` looks team-ready. Copy to `knowledge-base/<function>/X.md`?"*

**7. You reference brain-only content in a team context.**
Signal: about to send, cite, or hand something off that only lives in brain.
Prompt: *"What you're about to share only exists in brain. Promote a clean copy first?"*

**8. A decision was made.**
Signal: concrete call landed (not a hunch — a decision).
Prompt: *"That's a decision. Log in `decisions/YYYY-MM-DD-X.md`? Does the team need to see it in KB?"*

### Anti-triggers — don't prompt

- Skill-driven output (goes to brain function folder directly; no decision to make).
- Edits to files that already have a home.
- Read-only / research sessions.
- Quick one-off asks where we won't revisit.
- When you're clearly in flow — batch flags for end-of-session.

### End-of-session sweep

*"Before we close — N loose threads with no home yet: [X, Y, Z]. Park, assign, or drop?"*

## Frontmatter convention

Use the `status` field to signal lifecycle:

- `status: draft` — default, work in progress
- `status: ready-for-kb` — polish threshold met, awaiting promotion
- `status: promoted` — a copy has been pushed to KB; edit there, not here

## The two flops to avoid

1. **Drafting in KB directly** — defeats the point. KB is downstream.
2. **Auto-syncing brain → KB** — removes the quality gate. Manual `cp` is the feature.
