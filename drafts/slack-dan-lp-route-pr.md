---
title: Slack to Dan — post-expert follow-up + /lp route PR
tags: [marketing, website]
updated: 2026-06-12
status: sent 2026-06-12 (Slack DM to Dan)
---

Dan — followed up on your post-expert pointer. Skill is great: posts, case studies, and copy edits are fully self-serve, and the root-relative link validator means everything published now survives the cutover. Nice work whoever built that.

One gap though: net-new pages (campaign/landing pages outside /blog and /casos-de-exito) still needed a hand-written line in routes.rb per page. Rather than ticket it, I shipped it: **https://github.com/tesote/tesote.com/pull/41**

What's in it:

- Dynamic `/lp/:slug` route — any template at `pages/static/lp/<slug>.html.erb` is live at that URL, directory-driven like posts. Unknown slugs 404.
- First CI run got flagged by Brakeman (dynamic render path), so the slug now resolves through a filesystem allowlist on `RepoContent::Paths` — the render path never touches params. Sitemap enumerates from the same helper.
- `lp/_skeleton.html.erb` copy-source + a landing-page section in CONTRIBUTING-CONTENT.md, so marketing can run the lane without asking anyone.
- Tests for the 200/404 paths + sitemap inclusion. CI is green.

Two things for you:

1. Review/merge when you can. One call flagged in the PR: prefix is `/lp/` — trivial to rename until the first page publishes under it, so veto now if you'd rather `/info/` or a Spanish slug.
2. For the post-expert pilot I want to run: who should hold the `ADMIN_API_KEY` the upload script uses, and is Kubeez billing set up for marketing?

After merge I'll extend post-expert with a landing-page lane (skill-doc edit — will send it past you) and hand the whole package to Vero's team.
