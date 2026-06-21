---
title: Architecture diagram — vendor-review draft
tags: [security, vendor-review, draft]
updated: 2026-04-27
status: draft
---

# Architecture — vendor-review draft

High-level, conceptual diagram of Tesote's cloud architecture intended as a starting point for **external vendor / security questionnaires** (Nestlé and similar).

## Files

- `architecture.mermaid` — editable source
- `architecture.png` — rendered export

## Scope & non-goals

**This is intentionally generic.** It describes the *shape* of a typical B2B SaaS / fintech architecture, not Tesote's actual stack details. That's deliberate — vendor questionnaires need enough to assess risk, not enough to map our infra.

What it shows:
- Network boundaries (public ↔ edge ↔ private VPC ↔ third parties)
- Component tiers (frontend, API, data, identity, platform)
- Where TLS is applied (every external hop) and where AES-256 at rest applies (data tier, backups)
- Categories of third-party integrations (banking, KYC, email, analytics) — without naming partners

What it deliberately omits:
- Specific cloud provider, regions, account structure
- Specific vendor names (BNC, KYC partner, email provider, etc.)
- Hostnames, IP ranges, internal service names
- Database schemas, table counts, data volumes
- Internal contacts, on-call arrangements

## Before sending to anyone external

- [ ] Confirm the questionnaire actually requires an architecture diagram (some only need a written description).
- [ ] Decide which specifics, if any, are required and safe to add (e.g., cloud provider name is usually fine; partner names usually aren't without an NDA).
- [ ] Have whoever owns infra/security at Tesote sanity-check the labels.
- [ ] Add a "Confidential — for [vendor] security review only" footer.
- [ ] Promote the polished version to the shared KB (`legal/` or a new `security/` folder) and edit there going forward — stop editing this draft.

## Editing

Render after edits:

```
cd drafts/architecture-vendor-review
npx -p @mermaid-js/mermaid-cli mmdc -i architecture.mermaid -o architecture.png -b white -w 1600
```

## Open questions for the real artifact

- Is this for Nestlé specifically, or a recurring vendor-review template? If recurring, this belongs in `legal/` or `security/` in the team KB, not in `drafts/`.
- Does Tesote have an existing security one-pager / SOC-style summary I should align with? If so, this draft should be reconciled against it before reuse.
