---
title: Tesote AI — Iconography Spec (No Emojis)
tags: [product, ai, design, iconography]
updated: 2026-05-20
status: locked — applies product-wide; called out here because /ai still ships some
companion: [[typography-spec.md]]
---

# Tesote AI — Iconography Spec

The rule, in one line:

> **No emojis in user-facing product UI. No symbol-font glyphs used as icons. All iconography is inline SVG from a defined library.**

This is product-wide (sidebars, filters, indicators, buttons — anything a customer sees) and applies to the `/ai` surface specifically. Brain notes, internal docs, and design mockups are exempt — write with emojis freely there if it helps you think.

---

## Why

1. **Brand integrity.** Emojis render differently on every OS (Apple's 🎨 ≠ Google's 🎨 ≠ Windows's 🎨). The product looks crafted on one machine and amateur on another. Inline SVGs render identically everywhere.
2. **Color discipline.** Apple-style emojis are full-color and ignore your palette. They blow out the Lunour neutral surface every time. SVGs inherit `currentColor` and respect the system.
3. **Weight discipline.** Emojis are pictorial, dense, attention-magnets. Combined with [[typography-spec|the capped 500-weight type system]], emojis become the loudest thing on every screen. SVGs at 1.5px stroke recede.
4. **Accessibility.** Emojis announce inconsistently across screen readers ("paperclip emoji" vs "📎" vs nothing). SVGs with `aria-label` give us deterministic semantic labels.
5. **Dark theme.** Color emojis don't adapt. A pastel paperclip emoji on Lunour gold dark mode looks broken. SVGs swap palette with the theme.

---

## What to use instead

**Library: [Lucide](https://lucide.dev)** (MIT, React bindings, ~1,500 icons, used by shadcn/ui, Vercel, Linear-adjacent stack). Already the right aesthetic for Tesote — clean modernist line work, consistent stroke, designed for variable stroke-width.

```bash
bun add lucide-react
```

```tsx
import { Paperclip, BookOpen, ArrowLeft, Moon, Sun, X, ChevronLeft, ChevronRight } from 'lucide-react';

<Paperclip size={16} strokeWidth={1.5} aria-label="Adjuntar archivo" />
```

**Alternatives if Lucide doesn't have what you need (rare):**
- [Phosphor](https://phosphoricons.com) — more characterful, multiple weights, slightly more "playful"
- [Heroicons](https://heroicons.com) — Tailwind's set, slightly chunkier
- Custom inline SVG — last resort, hand-drawn at 24×24 viewBox, 1.5px stroke

**Never:**
- Emoji literals in JSX (`📎`, `📚`, `🤖`, `☀`, `☾`)
- Symbol-font glyphs used as icons (`›`, `‹`, `×`, `←`) — these are typographic punctuation, not icons. Use `ChevronLeft`/`ChevronRight`/`X`/`ArrowLeft` instead.
- Emoji fonts loaded via `font-family`
- Icon fonts (FontAwesome etc.) — they were great in 2014; we're not in 2014

---

## Implementation contract

Every icon in the `/ai` surface follows these rules:

| Aspect | Rule |
|---|---|
| **Size** | 16px default. 14px for dense rows (file tree, tool pills). 20px for prominent actions (composer attach). Set via `size={16}` prop. |
| **Stroke width** | 1.5px (Lucide's `strokeWidth={1.5}`). 1.75 for very small (≤12px). Never below 1.25. |
| **Color** | `currentColor` — inherits text color from parent. Never set `color` or `fill` directly on the icon. |
| **Accessibility** | `aria-label="..."` if the icon is the only label (icon-only button). `aria-hidden="true"` if it's paired with visible text. Never both. |
| **Container** | Icons go in a fixed-size flex slot so they don't jiggle when neighbors change. `<span class="icon-slot">` with `width/height` matching the icon size. |
| **Animation** | None by default. Spinner allowed on async actions (use Lucide's `Loader2` with CSS `animate-spin`). |

CSS scaffold:

```css
.icon-slot {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  color: inherit;
  flex-shrink: 0;
}
.icon-slot[data-size="sm"] { width: 14px; height: 14px; }
.icon-slot[data-size="lg"] { width: 20px; height: 20px; }
```

---

## Audit — current `/ai` surface

These are the emoji/symbol-as-icon instances in treasury today. All should be replaced.

| Where | Current | Replace with |
|---|---|---|
| Sidenav theme toggle | `☾` / `☀` (Unicode moon/sun) | `<Moon />` / `<Sun />` |
| Sidenav collapse toggle | `›` / `‹` (Unicode chevrons) | `<ChevronLeft />` / `<ChevronRight />` |
| Sidenav back to Classic | `←` (Unicode arrow) | `<ArrowLeft />` |
| Sidenav drawer close (mobile) | `×` (Unicode multiplication sign) | `<X />` |
| Composer attach button | `📎` paperclip (per `PRODUCT.md` reference) | `<Paperclip />` |
| Capability browser trigger | `📚` book (per code comments in `App.tsx`) | `<BookOpen />` or `<Library />` |
| Tool pill check / status | mixed | `<Check />` / `<X />` / `<Loader2 className="animate-spin" />` |
| Empty-state hero chip arrows | none today, but planned | `<ArrowRight size={14} />` inline |
| File-tree folder/file icons | none today (just bullet dots) | Optional: `<Folder />` / `<File />` / `<FileText />` / `<FileSpreadsheet />` per file_type |
| Sidenav new conversation `+` | text plus | `<Plus />` |

The brand mark "T" in the sidenav stays as-is — it's a wordmark, not an icon.

---

## File-type icons (new — recommended addition)

The file tree currently shows colored dots. Worth replacing with file-type icons since Lucide has clean ones that map cleanly to our six `file_type` values:

| `file_type` | Icon |
|---|---|
| `chart` | `<BarChart3 />` |
| `card` | `<LayoutGrid />` |
| `table` | `<Table />` |
| `comparison` | `<Columns2 />` |
| `csv` | `<FileSpreadsheet />` |
| `log` | `<ScrollText />` |
| `upload` (inputs/) | `<Paperclip />` for PDF, `<FileSpreadsheet />` for CSV, `<Image />` for image |

Status indicator dots (`building`, `ready`, `error`) stay as colored dots — they're not icons, they're state markers.

---

## What stays out of scope

- **Inline emoji in chat content** sent by the AI (e.g. the assistant writes `:)` or `🎉` in a response). The system prompt should be updated to discourage this, but it's a runtime concern not a design-system concern. Track separately.
- **User-typed emoji in their messages.** Customer is welcome to type whatever; we don't censor their input.
- **Logos of third parties** (Banesco, BNC, Banco Exterior, etc.) when shown in bank-connection rows. Those are brand marks, not icons — render as their official SVG logos via existing asset pipeline.

---

## Migration plan

Same shape as the typography pass — one PR, behind the `:tesote_ai_demo` flag, included in the same ticket if scope allows.

1. `bun add lucide-react` in treasury
2. Replace the audit table above one-by-one in `App.tsx` and `components/ai/components/*.tsx`
3. Add the `icon-slot` CSS scaffold to `styles.css`
4. Update the system prompt to remove `📚` / `📎` references in capability examples (lives in `app/services/ai/system_prompts.rb`)
5. Optional: add file-type icons to `FileTree.tsx` per the table above — bonus polish if the migration session has time

Total LOC delta: similar to typography (~50–80 lines). The two specs ship together cleanly.

---

## Decision (locked)

- **Library**: Lucide (`lucide-react`)
- **Stroke width**: 1.5px
- **Default size**: 16px
- **Scope**: `/ai` surface for this pass; rule already applies product-wide per [[../../CLAUDE.md|brain CLAUDE.md]] and the underlying [No Emojis in Product UI](https://luis-brain) feedback memory.

Pair this spec with [[typography-spec]] when filing the PRO-* ticket — both are CSS/component-level changes to the same surface.
