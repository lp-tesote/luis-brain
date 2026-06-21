---
title: marketing.tesote.com — full HTML snapshot
tags: [marketing, website]
updated: 2026-06-06
status: draft
---

# marketing.tesote.com snapshot — 2026-06-06

Full HTML pull of the Rails staging site (repo `tesote/tesote.com`; prod is still WordPress at tesote.com).

**Caveat:** this is the UNapproved eng output. [[designer-brief-marketing-site-html]] — tesote.cloud is the approved design direction. Use this snapshot as a **page/content inventory and editing base**, not a design reference.

## Contents

- `es/` — 29 pages, base Spanish locale (default site)
- `en/` — 28 pages, English locale
- `assets/` — `application-*.css` (site styles), `admin-*.css`, fontawesome, `application-*.js`
- `es-urls.txt` / `en-urls.txt` — sitemap URL lists

Regional variants (`/ve`, `/mx`, `/do` + EN equivalents) were checked and **skipped** — identical copy to base, only link prefixes and the country selector differ.

## Page map (ES slugs; EN mirrors 1:1, minus `/blog/cuanto-tiempo-pierde-tu-equipo`)

- Core: `index`, `caracteristicas`, `como-funciona`, `integraciones`, `api`, `precios`, `sobre-tesote`, `socios`, `contacto`, `downloads`
- Soluciones (4): `tesoreria`, `conciliacion`, `cierre`, `ap`
- Industrias (4): `retail`, `salud`, `manufactura`, `servicios-financieros`
- Casos de éxito (3 + index): `munchy-escalando-sin-contratar`, `cines-unidos-multi-pais`, `grupo-mimesa-cierre-contable`
- Blog (4 + index)
- Legal: `privacidad`, `terminos`

File naming: URL path with `/` → `__` (e.g. `casos-de-exito__munchy-escalando-sin-contratar.html`).
