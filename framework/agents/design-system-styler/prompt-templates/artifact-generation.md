# Artifact Generation — Prompt Template

**Purpose:** Reusable instruction block for writing the populated design-system doc — **one file per colour mode** — from `framework/assets/template-design-system.html`. The design-system-styler workflow loads this file after extraction (step-05) and the domain-inference fill + mode selection + cross-mode derivation (step-05b), then applies its instructions once per mode in `{{files_to_write}}` to serialise the in-memory token sets into the structured artefacts.

**Usage:** Read this file using the Read tool. Apply the instructions to the in-memory results: `{{extracted_colors}}`, `{{extracted_typography}}`, `{{extracted_effects}}`, the per-mode contrast results, `{{extraction_status}}`, `{{voice}}`, the mode state (`{{mode_choice}}`, `{{extracted_scheme}}`, `{{hue_source_mode}}`, `{{files_to_write}}`, `{{primary_mode}}`), plus the consultant inputs (`{{domain}}`, `{{reference_url}}`).

---

## 1. Output File Structure

Each written mode gets its **own complete, single-mode file**:

- `design-system/design-system-light.html` — `mode = light`
- `design-system/design-system-dark.html` — `mode = dark`

There is no in-document mode switcher, and no combined file. Which files are written is decided in step-05b: **every mode the consultant asked for, plus the hue-source mode always** (`{{files_to_write}}`). The plain `design-system.html` filename is retired.

The **hue source** is the mode whose palette is grounded in the reference URL — whichever scheme that site actually ships, dark as readily as light — or domain-inferred light when no URL was given. The other mode is **derived** from it per `framework/agents/design-system-styler/data/cross-mode-derivation-rules.md` and is **never presented as extracted**.

Each file is populated from `framework/assets/template-design-system.html`. It is a self-contained HTML document with two parallel encodings of the same token set:

- **Machine encoding** — a `<script type="application/json" id="design-tokens">` block in the `<body>`. LLMs and downstream tools extract it with one regex and `JSON.parse` it.
- **Human encoding** — visual sections rendered with inline styles using the actual token values, so a consultant opens the file via `file://` in a browser and sees swatches, typography specimens, shadow cards, motion samples, and contrast pairs.

Section order (contractual — do not reorder; matches the template):

```
<head>
  <title>                              ← carries ({{MODE_LABEL}})
  <meta>, inlined <style>              ← {{DOC_CHROME_VARS}} in :root;
                                         {{COMPONENT_STYLES}} before </style>
</head>
<body>
  <script type="application/json" id="design-tokens"> ← JSON token block
  <main>
    <header class="doc-header"> ← H1, attribution blockquote, generated-at
    <section id="colours">      ← 11 swatches
    <section id="typography">   ← 2 family + 8 size + 3 line-height specimens
    <section id="effects">      ← 3 shadow cards + 3 transition rows + 1 easing row
    <section id="contrast">     ← 4 text-on-bg pairs + adjustments line
    <section id="components">   ← {{COMPONENT_SPECIMENS}}: live demos + state matrices from catalogue
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
    "domain_provenance": "{{domain_provenance}}",
    "reference_url": "{{reference_url_or_null}}",
    "extraction_date": "{{extraction_date}}",
    "extraction_status": "{{extraction_status}}",
    "css_source_type": "{{css_source_type_or_null}}",
    "css_source_url": "{{css_source_url_or_null}}",
    "mode": "{{mode}}",
    "mode_choice": "{{mode_choice}}",
    "hue_source": "{{hue_source}}",
    "primary": {{primary}}
  },
  "colours": { ... 11 entries ... },
  "typography": { ... 15 entries ... },
  "effects": { ... 7 entries ... },
  "contrast": { ... 4 pairs + adjustments string ... }
}
```

- `meta.domain`: the domain string, lowercased and trimmed — set in step-04b (suggested from the fetched page and confirmed, or typed directly when no URL/signals). Drives the Voice synthesis in step-05b.
- `meta.domain_provenance`: how the domain was chosen — one of `suggested-from-url-accepted` (consultant accepted the page-derived suggestion), `suggested-from-url-overridden` (a suggestion was offered but the consultant picked an alternative or typed their own), or `consultant-typed` (no signals; domain entered via the prose prompt).
- `meta.reference_url`: the URL the consultant supplied, or `null` if they skipped the URL prompt.
- `meta.extraction_date`: ISO date (e.g. `2026-05-04`).
- `meta.extraction_status`: one of `success | no_url | fetch_failed | no_css | css_fetch_failed | insufficient_data | workspace_read_failed | playwright_unavailable`. Still write the artefact even on non-success — the doc is complete (every unset token domain-inferred in step-05b); the status records *why* the URL path didn't yield extracted values.
- `meta.css_source_type`, `meta.css_source_url`: present on the Playwright path, `null` otherwise.
- `meta.mode`: the colour mode **this file** renders — `light` or `dark`. Must agree with the filename suffix and with the `({{MODE_LABEL}})` text in the `<title>` and H1.
- `meta.mode_choice`: what the consultant selected at step-05b — one of `light-only | dark-only | both`. The **same value in every written file**, so a reader of one file can tell what was asked for.
- `meta.hue_source`: which palette is grounded, and how — one of `extracted-light` (the URL shipped a light scheme), `extracted-dark` (the URL shipped a dark scheme), or `domain-inferred-light` (no URL, or extraction did not complete; the light set came from domain inference). The **same value in every written file**.
- `meta.primary`: a JSON **boolean** (not a string). `true` in exactly one written file — **the hue-source mode's file**, because that palette is the one grounded in the real brand; the derived mode is `false`. Derive it as `mode == hue_source_mode`. When only one file is written it is necessarily `true`.

Note that `meta.mode` varies per file while `mode_choice` and `hue_source` do not; `primary` is the join between them. The five top-level keys (`meta`, `colours`, `typography`, `effects`, `contrast`) and the 11 / 15 / 7 token counts are **unchanged** — these `meta` fields are purely additive, so existing downstream parsers of the `design-tokens` block keep working.

Each colour / typography / effects entry has the shape `{"hex" | "value": "...", "prov": "extracted-from-url|inferred-from-domain", "source": "..."}`. The full key list is documented in the template's JSON SHAPE comment block.

Each contrast pair has the shape `{"ratio": 7.2, "status": "Pass"}`. The `adjustments` key is a string (`"none"` or the comma-separated record).

---

## 4. Attribution Paragraph

The styler builds the `<blockquote class="attribution">` inner HTML in **two parts**, substituted into `{{ATTRIBUTION_PARAGRAPH}}`: a base sentence describing where the tokens came from, then a mode clause. Truthfulness about extraction-vs-derivation is the whole point of this paragraph — get the branch right.

### 4.1 Base sentence

Pick one variant:

| Condition | Attribution HTML |
| --- | --- |
| `extraction_status = success`, `reference_url` set | `Tokens extracted from <a href="{{reference_url}}">{{reference_url}}</a>. Status colours and any unset tokens are inferred per-run from the <code>{{domain}}</code> string.` |
| `reference_url` is null (consultant skipped) | `Tokens inferred per-run from <code>{{domain}}</code> — no reference URL was provided.` |
| Any other non-success status (fetch_failed, no_css, css_fetch_failed, insufficient_data, workspace_read_failed, playwright_unavailable) | `Tokens inferred per-run from <code>{{domain}}</code>. URL extraction was attempted from <a href="{{reference_url}}">{{reference_url}}</a> but did not complete: {{extraction_status}}.` |

### 4.2 Mode clause

Append one clause, chosen by whether **this file's mode is the hue-source mode**:

| Condition | Appended HTML |
| --- | --- |
| `mode == hue_source_mode` **and** a derived sibling was written | `<br><br>This is the <strong>{{mode}}</strong> variant, and it is the hue source for this run — its palette is the one grounded in the source above. The <a href="design-system-{{derived_mode}}.html">{{derived_mode}} variant</a> is derived from these same brand hues.` |
| `mode == hue_source_mode` **and** no sibling was written | *(nothing — the base sentence already tells the whole story)* |
| `mode != hue_source_mode` (this is the derived file) | `<br><br>This is the derived <strong>{{mode}}</strong> variant — the palette is derived from the same brand hues as the <a href="design-system-{{hue_source_mode}}.html">{{hue_source_mode}} variant</a> (<code>design-system-{{hue_source_mode}}.html</code>), <strong>not separately extracted</strong>. Only the 11 colour and 3 shadow tokens differ between the two files; typography and motion are shared verbatim.` |

The derived file **must never** imply its colours were read from the URL. When `extraction_status = success` and this is the derived file, the base sentence's "Tokens extracted from …" is still accurate for the *run* — the mode clause is what disambiguates this file — so both parts are required. Never drop the mode clause on a derived file.

### 4.3 Standing reminder

Always end the attribution with: `<br><br>Every token below carries a provenance marker — <code>extracted-from-url</code> if the value was found in the fetched CSS, <code>inferred-from-domain</code> if it was inferred per-run from the <code>{{domain}}</code> string or derived from the other mode. Review before proceeding.`

---

## 5. Provenance Tagging Rules

For every token in the doc:

- If the in-memory token came from step-05 (CSS extraction), tag it `extracted-from-url`. JSON `source` = the CSS selector or custom-property name the value came from.
- If the in-memory token came from step-05b (domain-inference fill), tag it `inferred-from-domain`. JSON `source` = `domain-inference ({{domain}})`.
- If the token was **gap-filled on a dark-extracted run** (step-05b §B converted a domain-inferred light value to dark), tag it `inferred-from-domain`. JSON `source` = `domain-inference ({{domain}}) → dark variant`.
- If the token is a **cross-mode derived** colour or shadow in the derived file (step-05b §F), tag it `inferred-from-domain`. JSON `source` = `derived: <target-mode> variant of <source-mode> <token> (<source-hex>)` — e.g. `derived: light variant of dark primary (#7AA2F7)`.
- The derived file's **19 shared tokens** (15 typography + 3 transitions + easing) keep the hue-source file's markers and source strings **verbatim** — they were not re-derived, so their provenance does not change.
- Never leave a `prov` value empty. **Never invent a third marker** — a derived value is `inferred-from-domain`, because it was not read from the URL. There is no `derived-from-mode` marker and no `consultant-specified` marker; the `source` string carries the detail, the marker set stays at two.
- For status colours (success/warning/error/info), `prov` is **always** `inferred-from-domain` — they are not extracted by this agent under any condition.
- Every visual snippet that surfaces a token also carries a matching `<span class="prov prov-{{prov-slug}}">{{prov}}</span>` element. The prov-slug equals the prov value verbatim; it's used directly as a CSS class suffix (the template defines `.prov-extracted-from-url` and `.prov-inferred-from-domain`).

Source-context examples (used in the visual snippets and in the JSON `source` field):

- `--brand-primary in :root` (CSS custom property)
- `.btn background-color` (class declaration)
- `body color` (element selector)
- `derived: primary hue +120°` (extraction derivation; still tag `extracted-from-url` because the seed came from CSS)
- `domain-inference (retail-banking)` (per-run inference)
- `domain-inference (legal services SaaS)` (per-run inference; free-text)
- `domain-inference (retail-banking) → dark variant` (inferred light, converted for a dark-extracted run)
- `derived: dark variant of light background (#FFFFFF)` (cross-mode derivation)
- `derived: light variant of dark shadow_md (0 4px 6px rgba(0,0,0,0.32))` (cross-mode derivation)

---

## 6. Render the Visual Sections

Each placeholder receives a pre-rendered HTML block. Follow the row schemas documented at the top of the template; the per-row shapes are repeated here for quick reference.

### 6.0 Per-mode rendering

**This whole section runs once per mode in `{{files_to_write}}`, hue-source mode first.** The static inputs (this file, the template, the catalogue, the standards appendix) are read **once** in step-06 §0 and re-used for every render — do not re-read them per mode.

Rendering the derived mode is not a different procedure; it is the same procedure over a different token set. Specifically:

- **Same placeholders.** The derived mode's 11 colours and 3 shadows go into `{{COLOUR_SWATCHES}}`, `{{SHADOW_SPECIMENS}}`, `{{CONTRAST_PAIRS}}`, `{{COMPONENT_STYLES}}`, `{{COMPONENT_SPECIMENS}}` exactly as the hue-source mode's values do. No placeholder is added, dropped, or reordered per mode.
- **Shared tokens are copied, not re-rendered from scratch.** The 19 typography + motion tokens are identical across modes, so `{{TYPE_FAMILY_SPECIMENS}}`, `{{TYPE_SIZE_SPECIMENS}}`, `{{TYPE_LH_SPECIMENS}}` and `{{MOTION_SPECIMENS}}` are byte-identical between the two files.
- **`{{MODE_LABEL}}`** — `Light` or `Dark`, matching this render's mode.
- **`{{DOC_CHROME_VARS}}`** — substitute the mode's fixed literal block from the template's DOC CHROME comment. These are documentation-chrome values, brand-neutral and identical for every run; do not derive them from brand tokens and do not run them through contrast validation.
- **Catalogue neutral swap (dark renders only)** — apply the `rgba(0,0,0,` → `rgba(255,255,255,` replacement to the raw component buffers **before** token substitution, per `component-catalogue.md` → *Dark-render neutral swap*. Ordering matters: dark shadow tokens are legitimately black with raised alpha and must not be caught by the swap.
- **Per-mode contrast values.** The contrast section renders **this mode's own** four ratios, statuses, and adjustments line. A derived set is validated independently and never inherits the hue-source set's numbers.

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

### `{{COMPONENT_STYLES}}` and `{{COMPONENT_SPECIMENS}}` (component catalogue)

The component visualisation section is sourced from `framework/agents/design-system-styler/data/component-catalogue.md` — the single source of truth for which components render, in what order, and how. Defer all per-component schema decisions to the catalogue itself; this prompt template only describes the read / extract / substitute mechanic.

**Read order in step-06:** read all four inputs together **once** (this prompt template, the HTML template, the catalogue, and the standards appendix) → then, **for each mode in `{{files_to_write}}`, hue-source mode first**: render JSON + visual snippets in memory → apply the dark neutral swap to the raw component buffers if this is a dark render → render the component buffers (token substitution) → substitute everything (including the verbatim standards appendix) → pre-write self-check → Write → verify. The hue-source file must be written **and verified** before the derived render begins.

**Render order:** parse the catalogue's `## Render order` list. Each numbered bullet is a family slug; render families in list order. A slug whose line starts with `<!--` or `#` is skipped (the family is not rendered). This is the consultant's hook for cheaply toggling families on / off without touching any other file.

**Two snippets per family:** under each `## {{slug}}` heading the catalogue contains two fenced `html` blocks — `### Live demo` and `### States matrix`. Extract both, in that order. Wrap them in a `<div class="cv-family">` with an `<h3>{{Title-Case-Slug}}</h3>`, a `<p class="cv-note">Live demo</p>` lead-in for the demo, a `<p class="cv-note">States matrix</p>` lead-in for the matrix, and append the wrapper to the component-specimens buffer.

**Token-reference substitution convention:** inside the catalogue's CSS block and its HTML snippets, token references take one of three forms — `{{colours.<name>.hex}}`, `{{typography.<name>.value}}`, `{{effects.<name>.value}}` — matching the JSON-shape paths defined in Section 3. The styler does plain string replacement against the in-memory token set built in step-05 / step-05b. No other substitution semantics; no expression evaluation; no fallback. A typo or a missing token leaves a literal `{{…}}` that the pre-write self-check (Section C in step-06) refuses to write.

**Structural-constant policy:** the catalogue's CSS contains hardcoded neutral constants for padding (`8px 16px` for buttons, `8px 12px` for inputs, `16px` for cards, etc.), border-radii (`4px` small, `6px` medium, `8px` large), border colours (`rgba(0,0,0,0.20)` strong, `rgba(0,0,0,0.08)` light), and focus-ring offsets. These are **not tokens** — they are pattern decisions shared across brands, not brand decisions. Adding spacing / radius / border-colour token categories is deliberately out of scope here; if a future requirement is "extract spacing from the brand site too", the constants in the catalogue become the seed values for the new tokens.

The colour constants among them are authored **black-based**, which only reads on a light surface. On a **dark render** step-06 therefore swaps every `rgba(0,0,0,` for `rgba(255,255,255,` at the same alpha — on the **raw buffers, before token substitution**, so the deliberately-black dark shadow tokens are not caught. There are no per-line exemptions. The catalogue owns this rule (*Dark-render neutral swap*); it is restated here only because step-06 executes it.

**Interactivity policy:** the catalogue's CSS pairs every `:hover` / `:focus` / `:active` / `:disabled` / `:checked` rule with a `.cv-force-{state}` sibling so live demos respond to real interaction and the state matrix renders the same visuals statically. Tabs use hidden `<input type="radio">` + `:checked`; the modal uses native `<details>`/`<summary>`. **No `<script>` tags.** The template invariant ("No external `<script>` tags — the JSON block is data, not code") is preserved.

**The catalogue is the contract.** Do not duplicate per-family schemas in this prompt template — the catalogue's HTML and CSS *are* the schema. Edits to which components render, what their HTML looks like, what states are shown, and what CSS applies happen in one file: the catalogue.

---

## 7. Write Discipline

- Output paths: `design-system/design-system-light.html` and/or `design-system/design-system-dark.html`, one per mode in `{{files_to_write}}`. The plain `design-system.html` path is retired.
- Create the `design-system/` directory first if it does not exist.
- **Write and verify one mode at a time, hue-source mode first.** Compute a **per-file** `sha256` of that file's rendered byte string (template + substituted standards) before writing it — each hash is passed to `framework/skills/verify-artifact-write.md` after that file's Write call with `expected_min_bytes = 14000`. Never reuse one mode's hash for the other file.
- Do not begin the derived render until the hue-source file has been written **and** its verify returned `pass`. A derived palette is meaningless without the grounded one on disk, and a half-written pair is worse than a single file.
- Never write an artefact incrementally. Each render is built fully in memory, then written in one atomic Write call.
- Never edit a previously-written `design-system-*.html` in this step — overwrites are governed by the orchestrator's startup gate, not by step-06.
- HTML escaping is not required for token values: hex codes (`#RRGGBB`), CSS lengths (`16px`, `1.5`), font-family stacks (`"Segoe UI", system-ui, sans-serif`), and shadow declarations contain no HTML-special characters under any extraction status. The attribution paragraph and source-context strings come from a closed set of pre-defined formats that likewise contain no HTML-special characters.
