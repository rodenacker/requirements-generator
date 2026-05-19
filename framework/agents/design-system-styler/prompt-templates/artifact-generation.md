# Artifact Generation — Prompt Template

**Purpose:** Reusable instruction block for writing the populated design-system doc to `design-system/design-system.html`. The design-system-styler workflow loads this file after extraction (step-05) and domain-inference fill (step-05b), then applies its instructions to serialise the in-memory token set into the structured artefact.

**Usage:** Read this file using the Read tool. Apply the instructions to the in-memory results: `{{extracted_colors}}`, `{{extracted_typography}}`, `{{extracted_effects}}`, `{{contrast_validation}}`, `{{extraction_status}}`, `{{voice}}`, plus the consultant inputs (`{{domain}}`, `{{reference_url}}`).

---

## 1. Output File Structure

The artefact file `design-system/design-system.html` is populated from `framework/assets/template-design-system.html`. It is a self-contained HTML document with two parallel encodings of the same token set:

- **Machine encoding** — a `<script type="application/json" id="design-tokens">` block in the `<body>`. LLMs and downstream tools extract it with one regex and `JSON.parse` it.
- **Human encoding** — visual sections rendered with inline styles using the actual token values, so a consultant opens the file via `file://` in a browser and sees swatches, typography specimens, shadow cards, motion samples, and contrast pairs.

Section order (contractual — do not reorder; matches the template):

```
<head>
  <title>, <meta>, inlined <style>
</head>
<body>
  <script type="application/json" id="design-tokens"> ← JSON token block
  <main>
    <header class="doc-header"> ← H1, attribution blockquote, generated-at
    <section id="colours">      ← 11 swatches
    <section id="typography">   ← 2 family + 8 size + 3 line-height specimens
    <section id="effects">      ← 3 shadow cards + 3 transition rows + 1 easing row
    <section id="contrast">     ← 4 text-on-bg pairs + adjustments line
    {{STANDARDS_BLOCK}}         ← verbatim insertion of design-system-standards.html
  </main>
</body>
```

The JSON block and visual sections intentionally carry the same data. The JSON has machine-precise field names + provenance; the visual sections render the same values for human verification. Both must agree token-for-token; do not skip a token in one without skipping it in the other.

---

## 2. Source the Template

Read `framework/assets/template-design-system.html` and use it as the structural base. Replace every `{{placeholder}}` with the corresponding value or pre-rendered HTML block. Do not insert, remove, or reorder sections. The schema comment block at the top of the template enumerates every placeholder, the JSON shape, and the per-section row schemas — follow them exactly.

---

## 3. Build the JSON Metadata Block

The `{{TOKENS_JSON}}` placeholder receives a JSON-serialised object with five top-level keys. Use 2-space indent.

```json
{
  "meta": {
    "domain": "{{domain}}",
    "reference_url": "{{reference_url_or_null}}",
    "extraction_date": "{{extraction_date}}",
    "extraction_status": "{{extraction_status}}",
    "css_source_type": "{{css_source_type_or_null}}",
    "css_source_url": "{{css_source_url_or_null}}"
  },
  "colours": { ... 11 entries ... },
  "typography": { ... 15 entries ... },
  "effects": { ... 7 entries ... },
  "contrast": { ... 4 pairs + adjustments string ... }
}
```

- `meta.domain`: consultant's typed domain string, lowercased and trimmed in step-02. Drives the Voice synthesis in step-05b.
- `meta.reference_url`: the URL the consultant supplied, or `null` if they skipped the URL prompt.
- `meta.extraction_date`: ISO date (e.g. `2026-05-04`).
- `meta.extraction_status`: one of `success | no_url | fetch_failed | no_css | css_fetch_failed | insufficient_data | workspace_read_failed | playwright_unavailable`. Still write the artefact even on non-success — the doc is complete (every unset token domain-inferred in step-05b); the status records *why* the URL path didn't yield extracted values.
- `meta.css_source_type`, `meta.css_source_url`: present on the Playwright path, `null` otherwise.

Each colour / typography / effects entry has the shape `{"hex" | "value": "...", "prov": "extracted-from-url|inferred-from-domain", "source": "..."}`. The full key list is documented in the template's JSON SHAPE comment block.

Each contrast pair has the shape `{"ratio": 7.2, "status": "Pass"}`. The `adjustments` key is a string (`"none"` or the comma-separated record).

---

## 4. Attribution Paragraph

The styler picks one variant for the `<blockquote class="attribution">` inner HTML, substituted into `{{ATTRIBUTION_PARAGRAPH}}`:

| Condition | Attribution HTML |
| --- | --- |
| `extraction_status = success`, `reference_url` set | `Tokens extracted from <a href="{{reference_url}}">{{reference_url}}</a>. Status colours and any unset tokens are inferred per-run from the <code>{{domain}}</code> string.` |
| `reference_url` is null (consultant skipped) | `Tokens inferred per-run from <code>{{domain}}</code> — no reference URL was provided.` |
| Any other non-success status (fetch_failed, no_css, css_fetch_failed, insufficient_data, workspace_read_failed, playwright_unavailable) | `Tokens inferred per-run from <code>{{domain}}</code>. URL extraction was attempted from <a href="{{reference_url}}">{{reference_url}}</a> but did not complete: {{extraction_status}}.` |

Always end the attribution with the standing reminder: `<br><br>Every token below carries a provenance marker — <code>extracted-from-url</code> if the value was found in the fetched CSS, <code>inferred-from-domain</code> if it was inferred per-run from the <code>{{domain}}</code> string. Review before proceeding.`

---

## 5. Provenance Tagging Rules

For every token in the doc:

- If the in-memory token came from step-05 (CSS extraction), tag it `extracted-from-url`. JSON `source` = the CSS selector or custom-property name the value came from.
- If the in-memory token came from step-05b (domain-inference fill), tag it `inferred-from-domain`. JSON `source` = `domain-inference ({{domain}})`.
- Never leave a `prov` value empty. Never invent a third marker.
- For status colours (success/warning/error/info), `prov` is **always** `inferred-from-domain` — they are not extracted by this agent under any condition.
- Every visual snippet that surfaces a token also carries a matching `<span class="prov prov-{{prov-slug}}">{{prov}}</span>` element. The prov-slug equals the prov value verbatim; it's used directly as a CSS class suffix (the template defines `.prov-extracted-from-url` and `.prov-inferred-from-domain`).

Source-context examples (used in the visual snippets and in the JSON `source` field):

- `--brand-primary in :root` (CSS custom property)
- `.btn background-color` (class declaration)
- `body color` (element selector)
- `derived: primary hue +120°` (extraction derivation; still tag `extracted-from-url` because the seed came from CSS)
- `domain-inference (retail-banking)` (per-run inference)
- `domain-inference (legal services SaaS)` (per-run inference; free-text)

---

## 6. Render the Visual Sections

Each placeholder receives a pre-rendered HTML block. Follow the row schemas documented at the top of the template; the per-row shapes are repeated here for quick reference.

### `{{COLOUR_SWATCHES}}` (11 rows)

One `<li class="swatch-row">` per token (primary / secondary / accent / background / surface / text / text-muted / success / warning / error / info). Hex values in `#RRGGBB` (uppercase hash, 6-digit). Inline style on `.swatch`: `background: {{hex}}`.

### `{{TYPE_FAMILY_SPECIMENS}}` (2 rows)

Heading and body families. Each `<div class="type-specimen">` has a meta column (token name, value, source, prov) and a sample column whose inline style is `font-family: {{family-stack}}; font-weight: {{paired-weight}};`. The pangram `The quick brown fox jumps over the lazy dog 1234567890` renders at the default body font-size — the goal is to demonstrate glyph shapes and the family stack, not size.

### `{{TYPE_SIZE_SPECIMENS}}` (8 rows)

`text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`, `text-4xl`. Each sample inline style: `font-size: {{value}};`. The pangram renders at the literal size.

### `{{TYPE_LH_SPECIMENS}}` (3 rows)

`line-height-tight`, `line-height-base`, `line-height-loose`. Sample text is the pangram repeated twice (two lines) so the line-height is visible. Inline style: `line-height: {{value}};`.

### `{{SHADOW_SPECIMENS}}` (3 cards)

`shadow-sm`, `shadow-md`, `shadow-lg`. Each `<div class="shadow-card">` has inline style `box-shadow: {{value}};`. The card body shows the token name, the literal value (in `<code>`), and a provenance label.

### `{{MOTION_SPECIMENS}}` (4 rows)

`transition-fast`, `transition-base`, `transition-slow`, `easing-standard`. Each `<div class="motion-row">` has the token meta on the left, an animated dot in the middle track, and the source-context on the right. Inline style on `.motion-dot`:

- For `transition-*` rows: `animation-duration: {{value}}; animation-timing-function: {{easing-standard-value}};` (use the brand's easing on all three durations so the consultant compares durations under the same curve).
- For `easing-standard` row: `animation-duration: 2s; animation-timing-function: {{value}};` (use a fixed slow duration so the curve is visible).

### `{{CONTRAST_PAIRS}}` (4 cards)

Four pairs: `text on background`, `text on surface`, `text-muted on background`, `text-muted on surface`. Each `<div class="contrast-card">` has inline style `background: {{bg-hex}}; color: {{fg-hex}};`. The `<p class="sample">` contains the pair label and the pangram. The `<div class="contrast-meta">` row shows `{{ratio}}:1` and a status badge (`<span class="status-pass">Pass</span>` if ratio ≥ 4.5, `<span class="status-fail">Fail</span>` otherwise). Ratios printed to one decimal place.

### `{{CONTRAST_ADJUSTMENTS}}` (single line)

`none` if no adjustments were needed, else the comma-separated record `{token} adjusted from {original_hex} to {adjusted_hex} ({pair} contrast was {original_ratio}:1)`.

---

## 7. Write Discipline

- Output path: `design-system/design-system.html`.
- Create the `design-system/` directory first if it does not exist.
- Compute `sha256` of the rendered byte string (template + substituted standards) before writing — this hash is passed to `framework/skills/verify-artifact-write.md` after the Write call with `expected_min_bytes = 8000`.
- Never write the artefact incrementally. The render is built fully in memory, then written in one atomic Write call.
- Never edit a previously-written `design-system.html` in this step — overwrites are governed by the orchestrator's startup gate, not by step-06.
- HTML escaping is not required for token values: hex codes (`#RRGGBB`), CSS lengths (`16px`, `1.5`), font-family stacks (`"Segoe UI", system-ui, sans-serif`), and shadow declarations contain no HTML-special characters under any extraction status. The attribution paragraph and source-context strings come from a closed set of pre-defined formats that likewise contain no HTML-special characters.
