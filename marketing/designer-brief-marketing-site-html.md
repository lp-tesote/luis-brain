---
title: Designer Brief — Bringing the tesote.cloud design to the marketing site (HTML handoff)
tags: [marketing, website, designer-onboarding]
updated: 2026-06-05
status: promoted
notion: https://app.notion.com/p/3761ee04eee181e7ba32df864d37e952
---

# Brief for the designer — marketing site in HTML

## What we're asking you to do (the short version)

We love the design direction you set with **tesote.cloud** — that's the foundation. The site currently at **marketing.tesote.com** was an engineering-built attempt based on your work; we have **not** approved its design or its copy, and it shouldn't be treated as a reference for anything. Your job: **continue the tesote.cloud design direction and bring it into plain HTML/CSS** that we can fold into our real site. This is your design, evolved — not a restyling of what's there now.

You don't need access to our code, our servers, or any framework. Plain HTML files + one stylesheet. You work in your own environment (Claude Code if you like), send us files, we review in a browser.

The single most important thing — more important than any individual page — is that we end up with a **defined set of reusable components**. Pages come and go; the component library is what we'll build every future page from.

## Step by step

### 1. Audit what exists (½ day)

- Start from **tesote.cloud** — your design is the reference for look, feel, and voice.
- Skim **marketing.tesote.com** only as an inventory of what pages/sections someone thought the site needed. Nothing there is approved — don't inherit its layout, styling, or copy.
- Make two lists: (a) every page the site actually needs, (b) every distinct visual block from your tesote.cloud design (hero, nav, footer, feature cards, pricing, testimonials, CTA bands, FAQ, forms…), plus any new blocks the page list demands.
- Output: a one-page inventory. We review this together before you build anything.

### 2. Define the component library — the most important step

- From the inventory, name the reusable components. Aim for the smallest set that can build every page (probably 12–20).
- For each component: a name, what content goes in it (title, body, image, button…), and its variants (e.g. hero with/without screenshot; card in 2-col vs 3-col grid).
- Rule of thumb: **if a block appears on two pages, it's a component, and it must be the exact same markup both times** — not two similar copies. This is what lets us reuse them forever on our side.
- Output: the component list, agreed with Luis, before page assembly starts.

### 3. Set the foundation (design tokens)

- One CSS file. At the top, define everything as CSS variables: colors, type scale, spacing steps, radii, shadows, buttons.
- Pull these from the tesote.cloud design — this is the "translation" part.
- No component or page may use a raw hex value or random pixel size; everything references a token. This keeps the whole site consistent and lets us re-theme later by changing one block of variables.

### 4. Build a component showcase page first

- One `components.html` that renders every component and its variants, in isolation, before any real page exists.
- This is our review surface: we approve components here, then pages are just assembly.
- Use clean, consistent class names (`.hero`, `.hero--with-image`, `.card`, `.cta-band`…). Same component = same classes everywhere, always.

### 5. Assemble pages from approved components only

- Start with the **homepage**. Then we prioritize the rest of the page list together.
- A page should be nothing more than components stacked in order. If a page needs something new, it becomes a new component in `components.html` first.

### 6. Copy and styling — together with Luis

- Treat copy as unwritten: the marketing.tesote.com copy is not approved, so don't carry it over. Start from the tesote.cloud voice and use placeholders where needed — Luis and you will write the real copy together, section by section.
- Copy is **Spanish-first** (an English version will exist later, so leave room: buttons and headings shouldn't break with text ~30% longer).
- Styling refinements (spacing, color balance, imagery) happen in review rounds on the showcase page and homepage.

### 7. How you deliver, how we ship

- Send a folder/zip: `index.html`, `components.html`, other pages, `styles.css`, `/assets` (SVG preferred for logos/icons).
- We open it in a browser, give feedback, iterate.
- Once approved, we port it into our site's codebase ourselves — your components become our site's building blocks — and it goes live on marketing.tesote.com. You check the live result and flag anything that drifted from your design.

## Constraints (keep it portable)

- **Plain HTML + one CSS file.** No build tools, no React/Vue, no CSS frameworks. Vanilla is the most portable thing you can hand us.
- Minimal JS — only where essential (mobile nav toggle, FAQ accordion). No libraries.
- Mobile-first responsive; must hold at 375 / 768 / 1440.
- SVG for icons and logos — no emoji as UI elements.
- System-safe font loading (Google Fonts links are fine).

## What success looks like

1. A component library we both point at and say "that's the Tesote design system for the site."
2. A homepage built only from those components, clearly your tesote.cloud design language.
3. A repeatable loop: you design in HTML → we review in browser → we ship → you verify live.
