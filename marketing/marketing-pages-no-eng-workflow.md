---
title: Marketing Pages Without Eng — Defined Workflow
tags: [marketing, ops, website]
updated: 2026-06-12
status: draft
---

# Marketing pages without eng — the defined workflow

Goal: a proven, repeatable way to spin up new pages on **marketing.tesote.com** (and tesote.com post-cutover) with **zero eng work per page**. The tesote.com Rails repo already has 90% of this built (`CONTRIBUTING-CONTENT.md` in that repo is the operator manual). This doc maps what works today, the one gap, and the one-time eng ask that closes it.

## What ships with zero eng TODAY

| Lane | URL | What you create | Eng needed |
|---|---|---|---|
| Blog post | `/blog/<slug>` | 1 ERB view (copy of `_skeleton`) + ES/EN locale files | None — slug auto-discovered from directory |
| Case study | `/casos-de-exito/<slug>` | Same shape, different paths | None — directory-driven via `CaseStudies::Loader` |
| Copy edit on existing page | any static page | Edit the locale file only | None |

Workflow per page: branch → scaffold from skeleton (Claude/Cursor does it from a one-line prompt) → preview on `localhost:3000` → PR → CI green (lint + Brakeman + tests) → merge → **deploy is automatic** (ArgoCD). Staging preview available via `workflow_dispatch` on the branch before merging.

### Execution layer: the `post-expert` skill (added 2026-06-12, via Dan)

The tesote.com repo ships `.claude/skills/post-expert/` — an authoring skill that runs this entire lane end-to-end (works in Claude Code and Cursor sessions inside that repo). Beyond what `CONTRIBUTING-CONTENT.md` documents, it adds:

- **Media pipeline**: `scripts/uploads/upload` pushes user photos or Kubeez AI-generated images to the prod media API → stable `cdn.tesote.com` URL, indexed for SEO. Kubeez bills per generation; skill confirms cost before spending.
- **Cutover-proofing**: internal links must be root-relative (`/contacto`); `Posts::LinkValidator` rejects host-prefixed links. Everything published now survives the tesote.com cutover.
- **Encoded footguns**: kebab-slug symbol syntax, orphan-locale hreflang breakage, SEO char limits, lint+test gates, PR-only (never main).

Operational dependencies to provision before handing to marketing: (1) `ADMIN_API_KEY` for the upload script — decide who holds it; (2) Kubeez billing access.

Safety rails (why this can't break the app):

- Pages are additive views + locale files — structurally can't touch auth, DB, or deploy config (explicitly fenced off in `CONTRIBUTING-CONTENT.md`)
- CI gates every merge; rollback = re-tag a known-good image
- i18n is enforced (ES + EN both required), so SEO/locale structure stays intact

## The one gap: brand-new pages at new URLs

New standalone marketing pages (campaign pages, new solution/industry pages, launch pages) render through `pages#static` — the controller already renders **any** template under `app/views/pages/static/` by slug. But each public URL needs a hand-written line in `routes.rb`:

```ruby
get 'caracteristicas', to: 'pages#static', defaults: { slug: 'features' }, as: :features
```

`routes.rb` is dev territory. So today, a new-URL page costs one eng-touched line per page.

## One-time route change (SHIPPED as PR — 2026-06-12)

> **Status:** Luis shipped this directly — no eng ticket. PR: [tesote/tesote.com#41](https://github.com/tesote/tesote.com/pull/41) (`marketing/lp-dynamic-route`). Dan reviews/merges; merge auto-deploys. Includes the dynamic route, 404 handling, sitemap enumeration, `lp/_skeleton.html.erb` copy-source, tests, and a "Spinning up a landing page" section in `CONTRIBUTING-CONTENT.md`. Prefix `/lp/` — renameable until the first page publishes (flagged in the PR body).

Original ask, for the record:

Add a dynamic landing-page route — same directory-driven pattern blog/case studies already use:

```ruby
# inside the (:locale)(:country) scope in routes.rb
get 'lp/:slug', to: 'pages#static',
    constraints: { slug: /[a-z0-9-]+/ }, as: :landing_page
```

Plus small supporting changes:

1. `PagesController#static` — map the route slug to `pages/static/lp/<slug>`, rescue `ActionView::MissingTemplate` → 404 (today a missing template would 500)
2. Widen `STATIC_SLUG_REGEX` to allow hyphens (currently `[a-z0-9_]` only; our slug convention is kebab-case)
3. Include `lp/*` pages in the sitemap generator
4. One test covering: known slug renders, unknown slug 404s

After this ships: **new page = drop `lp/<slug>.html.erb` + ES/EN locale files into a PR.** No routes, no eng, ever. URL: `marketing.tesote.com/lp/<slug>` (and `tesote.com/lp/<slug>` after cutover — URLs survive the transition since it's the same app).

Prefix note: `/lp/` is the placeholder; `/info/` or bare Spanish slugs are alternatives. Decide once with Dan — changing later breaks URLs.

## Still dev-side (by design — don't route around it)

- New **section types** (ViewComponents) — pages compose from the existing set: `HeroComponent`, `FeatureGridComponent`, `FeatureCardComponent`, `CtaSectionComponent`, `FaqComponent`, `LogoStripComponent`, `PageHeaderComponent`. If a page needs a new block, request it; don't inline-style around it.
- Porting the v54 sitemap prototypes (`page-*.html`) into ViewComponent/i18n form — that's a translation job, batch it through `/tesote-plan` rather than page-by-page.

## What NOT to do

- No separate static host (Vercel/Netlify) on a subdomain — fragments SEO, bypasses i18n/analytics, and ingress is Cloudflare Tunnel so eng owns DNS anyway. The Rails lane is nearly as fast and strictly safer.
- No WordPress edits on current tesote.com — frozen until cutover.

## Next moves

1. **PR #41 merge**: Dan reviews [tesote.com#41](https://github.com/tesote/tesote.com/pull/41) (the `/lp/:slug` route) — veto window on the `/lp/` prefix closes when the first page publishes
2. **Pilot post-expert**: ship one real blog post end-to-end from the tesote.com repo (Luis first, before Vero's team) — validates the chain including `ADMIN_API_KEY` and Kubeez access
3. Once #41 merges, extend post-expert with a "landing page" lane (skill-doc edit, ask Dan to bless)
4. Hand the package (post-expert + `CONTRIBUTING-CONTENT.md`) to marketing; consider a one-line voice-conventions addition to the skill (it says generic LatAm `ustedes`) → then promote this doc to the KB as the team-facing manual
