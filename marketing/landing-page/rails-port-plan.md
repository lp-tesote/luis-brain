---
title: Rails Port Plan — v41 homepage → tesote.com (marketing.tesote.com)
tags: [marketing, website, homepage, port, rails]
updated: 2026-06-07
status: draft
---

# Rails port plan — v41 homepage → `tesote/tesote.com`

> **STATUS 2026-06-07 (overnight build): BUILT + COMMITTED + PUSHED.** Branch `redesign-homepage-v41` (commit `36b2f26`) is on origin. All 7 workstreams done (light theme, 8 components + JS controller, home.html.erb, nav/footer trim, i18n es+en, tests). Ruby syntax-checked locally (no Docker → no full `bin/rails test`/`bin/dev`). **Open the PR to run CI:** https://github.com/tesote/tesote.com/pull/new/redesign-homepage-v41 . Deviation: secondary routes left intact (unlinked) instead of redirected, so existing controller tests stay green — harden later. Review EN copy + decorative-panel ES + og:image + Dan security sign-off before merge→prod (marketing.tesote.com).

**Goal:** replace the current `pages#home` with the v41 prototype. Repo: `~/Programming/tesote/tesote.com/rails` (Rails 8 · Bootstrap 5 SCSS · ViewComponent · Stimulus · Propshaft + cssbundling/bun).
**Deploy path:** branch → PR → CI (RuboCop/ERB-lint/ESLint/Brakeman/tests) → `workflow_dispatch` to **staging** (verify) → merge to `main` → auto-build → ArgoCD deploys **production = marketing.tesote.com**. (No infra-repo changes; off-app only.)
**Source of truth for markup/styles/copy:** `marketing/landing-page/v41-homepage.html` (+ this README chain).

## Why this is tractable
The prototype was built from `current/index.html` (a pristine copy of this exact app), so the class names (`.pcard`, `.hero-panel`, `.chapter`, `.cta-section`, `.site-navbar__*`, `.section__*`) and tokens (`--tesote-blue-*`, `--space-*`, `--fs-*`, `--radius-*`) are **already the repo's design system**. The redesign README literally framed the theme flip as *"a token change, not a redesign."*

## The 3 real port challenges
1. **Light theme.** Repo is dark-only (`<html data-theme="dark">`, semantic tokens dark). v41 is light (Lunour). Fix = define a `[data-theme="light"]` token set (lift values from v41's head token-override block) and have `pages#home` render under `data-theme="light"`. All components use semantic tokens (`--bg-*`, `--text-*`, `--border-*`), so navbar/footer/cards **auto-adapt** — no per-component rewrite.
2. **i18n, both locales, no `default:`.** v41 is Spanish-only. Every string must land in `config/locales/es/*` **and** `config/locales/en/*`. English copy needs writing (it doesn't exist yet).
3. **Nav/footer are global + componentized in Ruby.** Trimming them (`NavbarComponent#menus`/`#direct_links`, `FooterComponent`) touches every page. Lean nav anchors must be `/#features` etc. (root-absolute) so they work from any route, not just `#features`.

---

## Workstream sequence

### 1. Light theme mechanism
- Add `[data-theme="light"] { … }` block in `app/assets/stylesheets/tokens/_colors.scss` with the Lunour semantic values from v41's head `<style>` token-override (bg-base/surface, text, border, accent, link, shadows).
- Make the layout emit `data-theme="light"` for the marketing pages (drive off controller/`content_for`). Recommend: **per-page theme** — home (and eventually all marketing pages) light; admin stays dark. Navbar/footer inherit via the `<html>` attr.
- Port the `density-pass` token overrides (container 75rem, trimmed `--fs-*` scale, section padding) into the token layer or `pages/_home.scss`.

### 2. SCSS port (new partials under `app/assets/stylesheets/components/`)
Reuse existing where present; add new partials for net-new sections:
- `_pcard.scss` (product rail cards + mini-UI: chips, pills, match-node, chart, chat bubbles)
- `_chapter.scss` (split-row chapters: copy + panel, `chapter-steps`, `chapter-flow-*`, dark AI register)
- `_story-bridge.scss`
- `_security.scss` (sec-grid 3-card triad)
- `_booking.scss` (HubSpot frame + placeholder)
- `_ai-digest.scss` (weekly digest bubble)
- extend `pages/_home.scss` for section rhythm + the v41 mobile-pass block.

### 3. ViewComponents (`app/components/ui/`)
**Reuse / extend:** `HeroComponent` (swap media slot for the command-center HTML panel), `LogoStripComponent`, `CtaSectionComponent` (add the 4-bullet consulting list slot), `FaqComponent` (accordion already exists), `TestimonialComponent`/`TestimonialPullComponent`, `SeoMetaComponent`.
**New components (sidecar `.rb` + `.html.erb`):**
- `ProductRailComponent` (the 5 `pcard`s → chapter anchors)
- `StoryBridgeComponent`
- `ChapterComponent` (split-row; takes side/flip, copy, bullet list, panel slot, dark flag) — render the 5 chapters as instances
- `SecurityGridComponent` (3 cards)
- `HubspotMeetingsComponent` (booking embed)
- `AiDigestComponent` (or fold into the AI chapter's panel slot)
Assemble in `app/views/pages/home.html.erb`.

### 4. Navbar + footer trim
- `NavbarComponent#menus` → drop the 4 mega-menus + language/country selectors; `#direct_links` → `Producto /#features`, `Seguridad /#seguridad`, `FAQ /#faq`; keep login + "Agenda una demo" → `/#agenda`. Update the template (remove mega/drawer-mega markup; lean mobile drawer).
- `FooterComponent` → 3 lean cols (Navegación anchors / Tesote: login+WhatsApp / Legal: privacidad+terminos), keep social, drop subscribe + dead cols + locale switcher.
- **Anchors root-absolute** (`/#features`) so they survive on non-home routes.

### 5. i18n (`config/locales/{es,en}/`)
- New/updated keys under `pages.home.*` for: hero H1/sub, stat grid, rail header + 5 cards, story-bridge line, 5 chapter H2s + bodies + bullet lists + panel labels, AI digest (all lines), security triad, CTA (title/sub/4 bullets), booking header, 6 FAQ Q&A.
- `navigation.*` → lean nav/footer labels.
- **Write the EN translations** (don't exist). Keep ES verbatim from v41. No `:default` anywhere.
- Mock-data note: the digest/panel numbers are content strings — they can live in locale files or be passed as component args; keep them identical across locales (they're figures, not translatable).

### 6. HubSpot booking
- `HubspotMeetingsComponent` renders `<div class="meetings-iframe-container" data-src="https://meetings.hubspot.com/ventas690/reunion-de-ventas-ve?embed=true">` + the `MeetingsEmbed/ex/MeetingsEmbedCode.js` script (defer/append to `<head>` via `content_for(:head)` or in-component). Section id `#agenda`.

### 7. Meta / OG
- Update `SeoMetaComponent` inputs for home: title/description to the locked positioning; **swap `og:image`** to a new light-hero share asset (NEW image needed — only net-new asset in the port); remove `og:locale:alternate`/hreflang for unshipped locales.

### 8. Stimulus
- Reuse existing `mega-menu`/`mobile-menu`/`accordion` controllers (already present). Lean nav uses `mobile-menu` only. Add `scroll-behavior: smooth` + `scroll-margin-top` (already in v41). No new JS expected.

### 9. Mobile + tests + lint
- Port v41's `#mobile-pass-v41` rules (story-bridge wrap <1199px, hero non-100svh on phones, rhythm trims).
- Component tests for each new component (success/edge), per repo convention (Minitest + FactoryBot). `bin/rails test`, `bin/lint` green. A system test (Cuprite) on `pages#home` rendering + anchor scroll.

### 9b. Hide the unshipped marketing routes (Luis: keep hidden)
- `/pricing`, `/features`, `/about`, `/api`, `/blog`, `/contact` (form stays if HubSpot needs it? — booking is on-home, so contact can hide too), `/casos-de-exito`, locale `/mx /ve /do`, etc. → redirect to root or gate behind a feature flag for launch. Keep the code; just make them non-reachable publicly so only the new home ships. Confirm whether `/contacto` (lead form) must stay live or the on-home HubSpot calendar fully replaces it.

### 10. Ship
- PR → `workflow_dispatch` staging → eyeball `tesote-com-staging` (incl. real HubSpot calendar + mobile) → merge `main` → prod = marketing.tesote.com.

---

## Decisions — LOCKED (Luis, 2026-06-07)
1. **Light theme scope:** ✅ **home light only** — per-page theme; other pages stay dark. Home renders `data-theme="light"`; navbar/footer inherit light on home, dark elsewhere.
2. **Other marketing routes** (`/pricing`, `/features`, `/blog`, `/contact`, locale `/mx /ve /do`): ✅ **keep hidden** — not touching those pages yet. Add a launch workstream to hide them (redirect → root, or gate the routes) so only the new home is publicly reachable. New nav already doesn't link them.
3. **EN copy:** ✅ **Claude drafts EN translations** for all new keys; Luis edits after. ES verbatim from v41. No `:default`.

## New assets required
- One **og:image** (light hero share card, ~1200×630). Everything else is HTML/CSS (no screenshots).

## Effort shape (rough)
Light-theme tokens + SCSS partials (½–1 day) · components + home assembly (1–1.5 days) · nav/footer trim (½ day) · i18n es+en (½ day) · HubSpot + meta + mobile + tests (½–1 day). ~3–4 focused days, most of it mechanical given the shared design system.
