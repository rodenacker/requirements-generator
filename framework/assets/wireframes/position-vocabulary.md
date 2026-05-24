# Wireframe position vocabulary (plain-English labels)

**Role:** asset (wireframe-private; cross-pipeline-reusable by a future `/prototype`).

**Purpose:** Provide plain-English labels and short tooltips for every
`(dimension, position)` pair across the active trade-off dimensions. Consumed
by templates and agents to substitute the cryptic `D1+1` notation with
descriptive language wherever consultant-facing HTML is rendered. The notation
remains in JSON sidecars (`variants.json`, `variant-position.json`,
`manifest.json`) as the audit trail.

**Inherits from:** `framework/assets/wireframes/tradeoff-dimensions-registry.md`
(canonical dimension vocabulary). Position semantics are mirrored from there;
this file is the *translation layer* between the registry's `-2 .. +2` scale
and consultant-facing prose.

**D6 deferred.** `D6 memorability-discoverability` is inactive (pending
upstream rename per the registry). This file omits D6 rows until upstream
resolves; downstream readers expecting D6 must treat it as `position: 0`
(neutral) and skip rendering its label.

**Used by:**
- `framework/assets/wireframes/template-set-index.html` — variant column headers
  render position tags using the *short label* below.
- `framework/assets/wireframes/template-comparison.html` — matrix cells render
  the *short label* + the *tooltip* (e.g. `<abbr title="...">…</abbr>`).
- `framework/assets/templates/template-screen.html` — header chrome's
  position-translation tagline uses the *short label* joined with ` · `.
- `framework/agents/wireframe-variant-generator.md` — when authoring the
  position-translation tagline in screen HTML headers.
- `framework/agents/wireframe-comparator.md` — when authoring the matrix and
  the per-variant right-rail copy on `index.html`.

---

## Lookup format

For each `(dimension, position)` pair the table provides:

- **Short label** — 1–2 words for column headers, tags, and one-line taglines.
- **Tooltip** — ≤ 80 chars expanding the label for hover or fallback prose.

Agents substitute the cryptic notation by joining short labels with ` · ` (e.g.
"Dense · Speed-leaning"). When more detail is helpful, the tooltip is rendered
inline or via `<abbr title="…">`.

---

## D1 speed-accuracy

| Position | Short label | Tooltip |
|---|---|---|
| -2 | Maximally accurate | Slow careful pace, mandatory review at every step |
| -1 | Accuracy-leaning | More confirmation, careful pace |
|  0 | Balanced | Standard validation, standard pace |
| +1 | Speed-leaning | Keyboard-first, fewer guardrails, faster throughput |
| +2 | Maximally fast | Auto-commit on blur, minimal confirmation, optimised for throughput |

## D2 power-simplicity

| Position | Short label | Tooltip |
|---|---|---|
| -2 | Maximally simple | Novice-first, wizard-driven, one task per page |
| -1 | Simplicity-leaning | Verbose help, opinionated defaults, hand-holding |
|  0 | Balanced | Standard help density, expected affordances |
| +1 | Power-leaning | Keyboard-first, on-demand help, command palette available |
| +2 | Maximally powerful | Expert-first, minimal copy, assumes prior knowledge |

## D3 density-focus

| Position | Short label | Tooltip |
|---|---|---|
| -2 | Maximally focused | Single record per viewport, one thing at a time |
| -1 | Spacious | Whitespace-led, 1–2 items per row, calm layout |
|  0 | Balanced | Standard density, typical column counts |
| +1 | Dense | 5+ columns visible, compact rows |
| +2 | Maximally dense | 8+ columns, inline-edit enabled, high information per viewport |

## D4 control-automation

| Position | Short label | Tooltip |
|---|---|---|
| -2 | Manual | No autofill, user types every value, validation on-submit only |
| -1 | Control-leaning | User accepts/rejects per suggestion, explicit confirms |
|  0 | Balanced | Standard defaults, field-level validation on-blur |
| +1 | Automation-leaning | Smart-default-fill with preview, user can override |
| +2 | Automated | Aggressive auto-defaults, one-click "fill from previous" |

## D5 flexibility-consistency

| Position | Short label | Tooltip |
|---|---|---|
| -2 | Bespoke | Each screen has a layout tuned to its task |
| -1 | Flexibility-leaning | Two layout shells across the scope |
|  0 | Balanced | One primary shell, one secondary shell |
| +1 | Consistency-leaning | One shell across every screen; section reuse |
| +2 | Rigidly consistent | One shell, identical composition, content-only variation |

---

## How to use

**Single tag.** When rendering a position as a tag (e.g. in a variant column
header on `index.html`), use the short label only. Tooltip becomes the `title`
attribute when the HTML allows.

```html
<span class="wf-tag" title="Many items visible at once, 8+ columns">Maximally dense</span>
```

**Joined taglines.** When the variant carries non-neutral positions on
multiple dimensions, join short labels with ` · ` in dimension-ID order
(`D1` → `D5`):

> "Accuracy-leaning · Spacious" (the default `CAREFUL-DEFAULT` variant)
> "Speed-leaning · Maximally dense" (the default `POWER-DENSE` variant)

Neutral (0) positions are omitted from the joined tagline — they add no
signal to the comparison.

**Matrix cells.** In `comparison.html`, each dimension row's per-variant cell
renders the short label plus the tooltip. Position numbers (e.g. `-1`, `+2`)
are kept as a small subtle annotation for readers who want the underlying
scale, but the short label is the primary content of the cell.

---

## Anti-patterns

- Do not embed dimension IDs (`D1`, `D2`, …) or signed positions (`+2`, `-1`)
  in any HTML rendered with these labels. The whole point is to hide the
  cryptic scale; if a label says "Maximally dense (D3+2)", the abstraction
  is broken.
- Do not embed pattern-catalogue IDs (`table.compact`, `single-form.compact`,
  etc.) in tooltips. The vocabulary is consultant-facing; pattern IDs belong
  in `manifest.json` only.
- Do not edit the labels to be marketing-flavoured. They describe positions,
  not products. "Maximally dense" is honest; "Pro mode" is not.
- Do not add D6 rows until the upstream rename in
  `tradeoff-dimensions-registry.md > Section 1` resolves.
- Do not extend the scale beyond `-2 .. +2`. The canonical scale is
  governed by the registry; this file mirrors it.
