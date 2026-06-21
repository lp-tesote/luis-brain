# The Untrainable — visual essay

Scroll-driven HTML visual essay rendering the "The Untrainable" essay (mid-2026, Substack — where AI value survives the model: private correctness, walled environments, who writes the benchmark).

## Files

- `the-untrainable-v1.html` — the essay, single self-contained file (only external dep: Google Fonts)
- `site/index.html` — deploy copy, renamed for clean URLs. Drag the `site/` folder onto https://app.netlify.com/drop to publish.

## Status

- v1 built and reviewed 2026-06-11. Luis: "this is incredible."
- Sharing path: Netlify Drop (no CLI on this machine; Shopify's "Quick" is internal-only, not an option).
- The **format is now a reusable template** — spec lives at [`learnings/visual-essay-html-format.md`](../../learnings/visual-essay-html-format.md). Read that before building the next one; this file is the reference implementation.

## Iterating

Per the versioning workflow: changes go in a new sibling (`the-untrainable-v2.html`), never edit v1 in place. Re-copy to `site/index.html` before re-deploying.
