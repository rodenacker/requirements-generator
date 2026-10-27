---
name: step-06-artifact-generation
description: 'Render one single-mode artefact per mode in files_to_write — hue-source mode first: build the JSON token block, render the visual sections, populate the HTML template, append the static standards HTML verbatim, write to generated-docs/design-system/design-system-<mode>.html, then verify each write.'
# Variables referenced (inherited from agent):
# prompt_artifact_generation: 'framework/agents/design-system-styler/prompt-templates/artifact-generation.md'
# template_path: 'framework/assets/template-design-system.html'
# standards_path: 'framework/assets/design-system-standards.html'
# component_catalogue: 'framework/agents/design-system-styler/data/component-catalogue.md'
# output_path_light: 'generated-docs/design-system/design-system-light.html'
# output_path_dark: 'generated-docs/design-system/design-system-dark.html'
---

# Step 6: Generate the Artefact(s)

## 0. Read inputs (batched)

Read all five static render inputs in a **single batched message** (the harness runs the reads concurrently); none depends on another, so there is no reason to serialise the reads:

- `framework/agents/design-system-styler/prompt-templates/artifact-generation.md` — the generation instructions applied below.
- `framework/assets/template-design-system.html` — the structural base (§A).
- `framework/agents/design-system-styler/data/component-catalogue.md` — the Components section source (§A / §B.4).
- `framework/assets/design-system-standards.html` — the static standards appendix (§B-bis).
- `framework/agents/design-system-styler/data/font-availability-rules.md` — §4.1 / §4.2 are the lists §C's availability assertions check against, and §6.3 is the link shape. Re-read here rather than relying on step-05's context: §C is a fail-closed gate and must not depend on an earlier step's read surviving.

**If `design-system-standards.html` cannot be read** (absent or unreadable), halt — do not write a partial artefact. (This is the same guard previously stated in §B-bis; it now applies to the batched read.)

With all five in context, apply the artifact-generation prompt's instructions in the order below.

**Read once, render N times.** These five inputs do not vary by mode — do **not** re-read them per mode.

**Inputs (in-memory after step-05b):**

- The **hue-source token set** — 12 colours (incl. the identity-only `brand`; status colours are the helper's house set), 15 typography, 7 effects — in `{{hue_source_mode}}`'s scheme.
- The **other-mode token set**, if `{{derived_mode_requested}}` — the same 34 tokens in the opposite mode. Derived: its colours other than `brand` and its 3 shadows carry `derived: …` source strings. Extracted (`{{hue_source}} == extracted-both`): its colours carry the alt-scheme selectors. Its 19 shared tokens (and `brand`) are copied verbatim.
- `{{palettes}}` — the helper's per-palette, per-mode `{ colours, on_colours, contrast, fills, adjustments }` (step-05b §G). **Every colour value and every on-colour this step renders comes from `{{palettes}}`** — never recomputed. Palette `default` when `{{palette_options}}` is null; otherwise `neutral` and `site_colour` (rendering both is step-06 §F, a review render).
- `{{palette_option}}` — `null`, or the option the consultant picked in step-07 (`neutral` | `site-colour`); a final render uses only that palette.
- **Mode state:** `{{files_to_write}}`, `{{hue_source_mode}}`, `{{mode_choice}}`, `{{hue_source}}`, `{{primary_mode}}`, `{{extracted_scheme}}`
- **Per-mode contrast:** `{{cv_pass_count_light}}` / `{{cv_adjustments_light}}` / `{{cv_adjustment_count_light}}` and the `_dark` twins
- `{{extraction_status}}`, `{{extraction_date}}`, `{{references}}` (final statuses), `{{lead_url}}`, `{{css_source_type}}`, `{{css_source_url}}`
- `{{brand_fonts}}` — the loadable-font contract assembled in step-05b §G. Mode-invariant: the same object goes into both files.

## 0-bis. Render Loop

**Review render or final render?** If `{{palette_options}}` is non-null **and** `{{palette_option}}` is still `null` (the consultant has not picked yet), this pass is a **review render**: run §A–§C once per mode with **both** palettes, as §F specifies, write each to `generated-docs/design-system/.workspace/review-<mode>.html` (never the real paths), then write `options.json` (§F.3) and advance to step-07, which asks the palette question. Otherwise (one palette, or the pick is made) this pass is a **final render**: the palette is `default`, or the picked one (`neutral` / `site_colour`), and §A–§E run exactly as below. The real output paths are written **only** by a final render, so an abandoned options run never leaves a two-palette file where `/prototype` reads and never overwrites the last accepted design system.

Sections §A–§E below are a **render procedure parameterised by one mode**. Run the whole procedure once per mode in `{{files_to_write}}`, in this order:

1. **`{{hue_source_mode}}` first** — using the hue-source token set.
2. Then the derived mode, if it is in `{{files_to_write}}` — using the derived token set.

**The hue-source file must be fully written (§D) and verified `pass` (§E) before the derived render begins.** Do not interleave the two renders, and do not batch the two Writes.

Throughout §A–§E, `{{mode}}` means the mode currently being rendered, and *the token set* means that mode's set.

## A. Source the Template and the Component Catalogue

Use `template-design-system.html` (read in Section 0) as the structural base. Replace every `{{placeholder}}` with the corresponding in-memory value. Do not insert, remove, or reorder sections.

The component catalogue `component-catalogue.md` (also read in Section 0) owns the **Components** section content (the single `css` block and every family's `Live demo` + `States matrix` HTML snippets). Step-06 substitutes its content into the template's `{{COMPONENT_STYLES}}` and `{{COMPONENT_SPECIMENS}}` placeholders — see Section B.4 below for the substitution procedure.

## B. Apply the Artifact-Generation Prompt

Apply the prompt template's instructions in order:

1. **Section 3 — JSON metadata block.** Build the `tokens` object in memory with `meta`, `colours`, `typography`, `effects`, and `contrast` keys per the JSON SHAPE documented at the top of the template. Serialise with `JSON.stringify`-equivalent 2-space indent. Substitute into `{{TOKENS_JSON}}`.
2. **Section 4 — Attribution paragraph.** Build it from `{{references}}` (the `used` ones, then any not used). The rendered string is inserted **as inner HTML of the `<blockquote class="attribution">`** (already in the template); the styler emits raw text plus any necessary `<a>` anchors for URLs. Substitute into `{{ATTRIBUTION_PARAGRAPH}}`.
3. **Section 5 — Provenance tagging.** Every token in the JSON gets `prov` set to one of `extracted` or `system-derived`. Every visual snippet that surfaces a token gets a matching `<span class="prov prov-{{prov-slug}}">{{prov}}</span>` element (`prov-slug` is the prov value verbatim — `extracted` or `system-derived`, used directly as a CSS class suffix).
4. **Section 6 — Render visual snippets.** Build the four pre-rendered HTML blocks and substitute them into the template placeholders:
    - `{{PALETTE_VARS}}` — the palette custom properties per the template's PALETTE VARS list, from this mode's `{{palettes}}.<palette>.<mode>`: `--c-<token>` = `colours.<token>` (token `_` written as `-`) for all 12 colours, and `--on-<fill>` = `on_colours.<fill>` for the 8 fills. A final render emits **one** block: `    :root { --c-primary: #…; … --on-info: #…; }`, and `{{PALETTE_TABS}}` becomes the empty string. (The two-block review form is §F.)
    - `{{COLOUR_SWATCHES}}` — 12 `<li class="swatch-row">` blocks per the COLOUR ROW SCHEMA (primary / secondary / accent / background / surface / text / text-muted / brand / success / warning / error / info). Each `<div class="swatch">` carries `style="background:var(--c-<token-slug>)"`; each row also surfaces the literal hex (in `<code>`), source-context, and provenance. The `brand` row's source-context ends with ` — identity only (header / logo strip / brand mark / empty state; never a button, link, badge, focus ring or text)`.
    - `{{BRAND_FONT_LINKS}}` — `meta.brand_fonts.links` (the `link`-delivery families only) emitted verbatim, one `<link rel="stylesheet">` per entry, into `<head>` (see `artifact-generation.md` → `{{BRAND_FONT_LINKS}}`). The list is already built and deduped by step-05b §G — do **not** rebuild it from the token stacks, and never merge two families into one request. When `links` is `[]` (every family embedded), substitute the single HTML comment the prompt template specifies so the placeholder is still replaced.
    - `{{TYPE_FAMILY_SPECIMENS}}` — 2 `<div class="type-specimen">` blocks (heading + body). Inline style on the sample: `font-family: {{family-stack}}; font-weight: {{paired-weight}}`. The token-value shown in the meta column is the literal family stack; a `substituted` or `unverified` slot also carries the line naming the face it renders in. **Prepend one rendering note** before the two blocks — pick the variant matching this run's `meta.brand_fonts` per `artifact-generation.md` → `{{TYPE_FAMILY_SPECIMENS}}` (every family embedded / any family linked). Exactly one note is emitted in every case. Use existing chrome markup for the note — no new CSS class, no template edit.
    - **The `brand-font-faces` block** — emit the template's `<style id="brand-font-faces">/* BRAND_FONT_FACES */</style>` verbatim, marker included, as the last child of `<body>`. It is filled after the write (§E), never here; never write font data or base64 into the render.
    - `{{TYPE_SIZE_SPECIMENS}}` — 8 `<div class="type-specimen">` blocks (text-xs..text-4xl). Inline style on the sample: `font-size: {{value}}`. Sample text is the fixed pangram.
    - `{{TYPE_LH_SPECIMENS}}` — 3 `<div class="type-specimen">` blocks (tight/base/loose). Sample is a two-line span (the pangram repeated, or wrapped) so the line-height is visible. Inline style: `line-height: {{value}}`.
    - `{{SHADOW_SPECIMENS}}` — 3 `<div class="shadow-card">` blocks. Inline style: `box-shadow: {{value}}` on the card; render the token name, the literal value (in `<code>`), and the provenance label.
    - `{{MOTION_SPECIMENS}}` — 4 `<div class="motion-row">` blocks (transition-fast / transition-base / transition-slow / easing-standard) per the MOTION SCHEMA. The animated dot's inline style is `animation-duration: {{value}}; animation-timing-function: {{easing-token-value}};` for transition rows, and `animation-duration: 2s; animation-timing-function: {{value}};` for the easing-standard row.
    - `{{CONTRAST_PAIRS}}` — 4 `<div class="contrast-card">` blocks per the CONTRAST PAIR SCHEMA. Inline style: `background: {{bg-hex}}; color: {{fg-hex}};`. Pair label and ratio printed inside; the status badge uses class `status-pass` (ratio ≥ 4.5) or `status-fail`.
    - `{{CONTRAST_ADJUSTMENTS}}` — `none`, or this mode's helper `adjustments` lines joined with `; ` (text adjustments, flips, moved fills, labels below target).
    - `{{COMPONENT_STYLES}}` and `{{COMPONENT_SPECIMENS}}` — sourced from the component catalogue. Procedure:
        1. Parse the catalogue's `## Render order` list. Each numbered bullet is a family slug (`buttons`, `form-inputs`, `alerts`, `badges`, `cards`, `data-table`, `tabs`, `modal`, `brand`). A bullet whose line starts with `<!--` or `#` is **skipped** — the family is not rendered.
        2. Extract the single fenced `css` block under `## Component CSS`. Its inner content (no fences) is the **component-css buffer**.
        3. For each enabled family slug, in render order, locate the catalogue heading `## {{slug}}`, then extract the two fenced `html` blocks under `### Live demo` and `### States matrix` (in that order). Wrap each family's two snippets in `<div class="cv-family"><h3>{{Title-Case-Slug}}</h3><p class="cv-note">Live demo</p>{{live-demo-html}}<p class="cv-note">States matrix</p>{{states-matrix-html}}</div>`. Append to the **component-specimens buffer**.
        4. **Dark-render neutral swap — only when `{{mode}} == "dark"`.** On the **raw** buffers, before any token substitution, replace every occurrence of `rgba(0,0,0,` with `rgba(255,255,255,`, leaving the alpha and everything else untouched. There are no exemptions. Then assert: **neither buffer still contains the substring `rgba(0,0,0,`** — if one does, the swap was incomplete; halt.

            **This must run before sub-step 5, not after.** The catalogue substitutes `{{effects.shadow_sm|md|lg.value}}` at five sites, and dark shadow tokens are deliberately *black with raised alpha* (dark elevation is carried by the lighter `surface`). Swapping after substitution would flip those shadows to white and destroy the treatment; swapping before means substituted values are untouched by construction. See `component-catalogue.md` → *Dark-render neutral swap*.

            On a light render, skip this sub-step entirely — the catalogue's constants are already authored for a light surface.
        5. **Token-substitute** both buffers in memory: for every reference of the form `{{typography.<name>.value}}` or `{{effects.<name>.value}}`, replace with the literal value from **`{{mode}}`'s token set**. This is plain string replacement — no other substitution semantics. Colours are **not** substituted: the catalogue holds only `var(--c-*)` / `var(--on-*)` references, resolved by `{{PALETTE_VARS}}`. After this pass, **no `{{colours.…}}` / `{{typography.…}}` / `{{effects.…}}` references must remain** in either buffer.
        6. Substitute the component-css buffer into the template's `{{COMPONENT_STYLES}}` placeholder (which sits inside the `<style>` block, immediately before `</style>`).
        7. Substitute the component-specimens buffer into the template's `{{COMPONENT_SPECIMENS}}` placeholder (which sits inside `<section id="components">`).
5. **Section 7 — Page-level scalars.** Substitute `{{BRAND_LABEL}}` (the first `used` reference's short name, per the template's placeholder list) and `{{GENERATED_AT}}` (ISO date) into the `<head>` `<title>`, the H1, and the generated-at line. Also substitute the two mode-scoped placeholders:
    - `{{MODE_LABEL}}` — `Light` or `Dark`, title-cased, matching `{{mode}}`. It appears in **both** the `<title>` and the H1.
    - `{{DOC_CHROME_VARS}}` — the fixed literal block for `{{mode}}` from the template's **DOC CHROME** comment section, substituted into the template's `:root`. These are documentation-chrome values: brand-neutral, identical for every run and every brand. Do **not** derive them from brand tokens, and do **not** run them through contrast validation. Copy the block for this mode verbatim; all 15 custom properties **and** the block's leading `color-scheme: {{mode}};` declaration must be present. That declaration is load-bearing, not cosmetic: it is what makes the browser paint UA-drawn control parts (the `<input type="date">` picker indicator, number spinners, native checkbox/radio, `<select>` popup, scrollbars) in the file's own mode. Omit it on a dark render and every date field shows a black calendar glyph on a dark surface — invisible.
6. **Contrast section — this mode's own numbers.** `{{CONTRAST_PAIRS}}` and `{{CONTRAST_ADJUSTMENTS}}` render from this mode's helper output (`{{palettes}}.<palette>.<mode>.contrast` / `.adjustments`, mirrored in `{{cv_*_<mode>}}`). JSON `contrast.<pair>.ratio` = the helper's ratio rounded to 2 decimals; `status` = `Pass` when ≥ 4.5. A derived set was validated independently in step-05b §F and never inherits the hue-source set's ratios.

The artefact is generated even when `{{extraction_status}}` ≠ `"success"` (a PDF reference was used instead). The doc is always complete; the JSON `meta.extraction_status` field records *why* the URL path didn't yield extracted values, and `meta.references` records every reference's status.

## B-bis. Append the Static Standards Appendix

After the template is fully rendered (all placeholders replaced except `{{STANDARDS_BLOCK}}`) and before the pre-write self-check, substitute the static standards file (`design-system-standards.html`, read in Section 0):

1. Substitute its **full contents verbatim** into the `{{STANDARDS_BLOCK}}` placeholder. The standards file opens with its own HTML comment block and a `<section id="standards" class="standards">` wrapper, so it slots in cleanly after the contrast section.
2. **Do not modify the standards content.** No placeholder substitution, no rewording, no truncation. It is static reference material that ships verbatim with every output. (The read-failure halt is handled in Section 0.)

## C. Pre-Write Self-Check

Runs **per file**, before that file's `Write`:

- Render the full artefact (template body + substituted standards) as one string in memory.
- Confirm: every `{{placeholder}}` has been replaced. No literal `{{...}}` substrings remain. (The standards block contains no placeholders. `{{MODE_LABEL}}`, `{{DOC_CHROME_VARS}}` and `{{BRAND_FONT_LINKS}}` must all be substituted — `{{BRAND_FONT_LINKS}}` becomes an HTML comment rather than nothing when every family is embedded, so an empty `links` list is still a substitution. The catalogue's token references — `{{colours.…}}`, `{{typography.…}}`, `{{effects.…}}` — must also be fully substituted; any survivor indicates a typo in the catalogue or a missing token in the in-memory set, and is a hard halt.)
- Confirm: the `<script type="application/json" id="design-tokens">` block is present, and its inner content is **valid JSON** — parse it back in memory to verify. If parsing fails, halt and do not Write.
- Confirm: the JSON `meta`, `colours`, `typography`, `effects`, and `contrast` keys are all present, and `colours` has exactly **12** keys including `brand`.
- Confirm: every `colours.<token>.hex` equals the value in `{{palettes}}.<palette>.<mode>.colours` for the palette being rendered — the helper is the only source of colour values. (That is what guarantees no `primary` / `secondary` / `accent` sits in the reserved zone: the helper never assigns one there.)
- Confirm: `meta.palette_option` is one of `"neutral"`, `"site-colour"`, `null`, and is `null` exactly when `{{palette_options}}` is null (`site_colour` palette → `"site-colour"`). A final file contains no `palette-site-colour` radio and exactly one `--c-primary:` declaration; a collapsed file is structurally identical to a no-options run apart from `meta.palette_option`.
- Confirm: `{{PALETTE_VARS}}` defines every `--c-*` and `--on-*` name that the rendered component CSS and swatches use (scan the rendered string for `var(--c-` / `var(--on-` and check each name is defined), and the rendered component CSS contains no `{{colours.` reference.
- Confirm: `meta.references` is present and non-empty, every entry has `kind` (`url` | `pdf`), `ref` and `status`, and at least one `status` is `used`. `meta` has no `domain` and no `domain_provenance` key.
- Confirm: `meta.brand_fonts` is present, with `families`, `links` and `embedded_bytes` keys.
- Confirm: every `prov` value in the JSON is one of `extracted` or `system-derived`. No third marker. (`meta.brand_fonts.families[].status` is an availability enum, not a `prov` value — it must never appear as one.)
- Confirm: status-colour entries (success/warning/error/info) all carry `prov: "system-derived"` (`source: HOUSE_STATUS`) regardless of the references.
- Confirm: the rendered string begins with `<!doctype html>` — those bytes are the very first bytes of the render (an optional UTF-8 BOM aside): the template's header comment is scaffolding documentation and is never emitted, and no blank line precedes the doctype. `verify-artifact-write` returns `re-render required` on a file that is not doctype-first; treat that as this step's own self-check FAIL — re-render from the doctype, recompute the per-file sha256, re-`Write`, and re-verify.
- Confirm: the document closes with `</body>\n</html>` (the template's literal closing tags are intact and not duplicated).
- Confirm: the rendered string contains the literal substring `<section id="standards"` (from the appended standards file) exactly once.
- Confirm: the rendered string contains `brand-font-faces` exactly once, **after** `<section id="standards"`, as `<style id="brand-font-faces">/* BRAND_FONT_FACES */</style>` — the block holds exactly the marker and nothing else.
- Confirm: the `design-tokens` JSON block contains no `data:` URI. Font data never enters the token block.
- Confirm: the rendered string contains the literal substring `<section id="components"` exactly once.
- Confirm: the rendered string contains the literal substring `class="cv-btn` at least once (smoke test that the component CSS / HTML from the catalogue actually landed in the artefact; a buffer-substitution failure would drop it silently).
- Confirm: the rendered string contains the literal substring `class="type-render-note"` exactly once (the family-specimen rendering caveat landed — see `artifact-generation.md` → `{{TYPE_FAMILY_SPECIMENS}}`).

**Brand-family assertions (all files):**

Check the **two in-memory token values** `typography.heading_family.value` and `typography.body_family.value` — **not** the rendered string. Those two values are the sole source of every brand `font-family:` declaration in the artefact (the ~20 component-catalogue substitution sites plus the 2 family specimens), so two checks are exhaustive. A whole-string scan would false-positive on the documentation chrome, which legitimately declares `system-ui` and is exempt (see the `DOC CHROME` comment in `template-design-system.html`).

- Confirm: neither value contains a **non-brand family** from group (a), (b), or (d) of `data/font-rules.md` §1, in any position. Match on **whole family names**, not substrings — a name is a comma-delimited entry in the stack, so `'Rockwell', 'Zilla Slab', serif` is not a `Slab` match and `Roboto Slab` is not a `Roboto` match.
- Confirm: neither value contains a group-(c) position-dependent face (`Roboto`, `Noto Sans`, `Ubuntu`, `Cantarell`, `Oxygen`, `Droid Sans`) in any position **other than first**. First position is a legitimate brand choice.
- Confirm: each value matches **one** of the two legal emitted stack shapes:
    - `'<Family>', <generic>` — exactly one quoted named family, then exactly one generic terminal, nothing more. This is the shape for every slot whose `meta.brand_fonts` entry is `google-native`.
    - `'<Brand>', '<Loadable>', <generic>` — exactly two quoted named families, then exactly one generic terminal. Legal **only** when that slot's `meta.brand_fonts` entry has `status: "substituted"` or `status: "unverified"`, and only when the two quoted names equal that entry's `brand` and `loadable`, **in that order**. Defined in `data/font-availability-rules.md` §6.1.
  A three-name stack with no matching `substituted` / `unverified` record — or with the two names transposed — is a hard halt: it means either a captured fallback tail leaked into the token (the defect the one-family rule exists to stop) or the brand and its stand-in got swapped, which would ship the substitute as the client's brand font.

**Brand-font availability assertions (all files):**

- Confirm: `meta.brand_fonts.families` has exactly two entries, `role: "heading"` then `role: "body"`.
- Confirm: every `status` is one of `google-native | substituted | unverified`. No other value, and this enum never appears as a `prov` value anywhere in the JSON.
- Confirm: every `param` is **either** a family listed in `data/font-availability-rules.md` §4.1, spelled identically once each `+` is read as a space, **or** an entry whose `evidence` records first-hand verification — a `fonts.googleapis.com` href on the source page (E1) or a successful probe (E3). Those two tiers are *stronger* evidence than the list, not weaker: the list is a cache of past probes, so a family verified this run must not be rejected for being absent from it. Only a `param` with neither backing is a halt — that one has never been shown to exist, and linking it would emit a request that fails silently.
  - A `substituted` or `unverified` entry's `param` is the exception with no exception: a **substitute** must always be in §4.1, because we chose it and had no reason to pick an unverified one. (The one carve-out is a `substituted` entry whose `evidence` begins `site @font-face`: that `loadable` is the face the site itself serves, verified by E1/E3 rather than chosen.)
- Confirm: no `loadable` is a family named in `data/font-availability-rules.md` §4.2 (the group-(b)/(c) faces and the names containing them). Those are Google-hosted but illegal in second position.
- Confirm: on a `google-native` entry, `loadable == brand`. Every entry has a non-null `loadable` and `param`, and `delivery` is `embedded` or `link`.
- Confirm: `meta.brand_fonts.links` has exactly one entry per **distinct** `param` whose `delivery` is `link`, each of the form `https://fonts.googleapis.com/css2?family=<param>:wght@400;500;600;700&display=swap`, and **no** entry carries more than one `family=` segment.
- Confirm: the rendered string contains exactly as many `<link rel="stylesheet" href="https://fonts.googleapis.com` **elements** as there are entries in `links`. Count elements, **not** raw `fonts.googleapis.com` occurrences: the template's own comment block names that host while explaining the exception and ships with the artefact, so a substring count is always one high and would halt every run.
- Confirm: the rendered string contains no `<link`, `<script src`, `<img src`, `url(http`, or `@import` pointing at any host other than `fonts.googleapis.com`. The template comment authorises these font links and only these.
- Confirm: the rendered string still contains `system-ui` in the documentation-chrome `html, body` rule. The chrome must not have picked up the brand family now that a webfont actually loads.

Any failure is a **hard halt before the `Write`**. This should never fire: `font-rules.md` §1 stops a non-brand family at extraction and the only other source is the interim fallback (`house-defaults.md` §4, `Inter`), so a violation reaching step-06 means §1 was skipped. It is a fail-closed backstop, not the primary mechanism — do not "repair" the value here and continue, and do not downgrade the halt to a warning. Shipping `Arial` as a client's brand font is the defect this whole rule exists to prevent, and unlike an unreachable contrast ratio it has a free, deterministic correct answer (leave the token unset; step-05b fills the interim fallback).

The availability assertions are the same kind of backstop for the second axis. **Do not repair here either** — in particular, do not "fix" an unlisted `param` by substituting a family you believe exists, and do not downgrade a `substituted` entry to `unverified` to get past the check. Both hide the real fault, which is upstream in step-05 §4b or step-05b §B.2.

**Mode assertions (all files):**

- Confirm: `meta.mode` is present and is `light` or `dark`, and **matches the filename suffix** this file is about to be written to.
- Confirm: the literal `({{MODE_LABEL}})`-substituted text appears in **both** the `<title>` and the H1 — i.e. `(Light)` or `(Dark)`, agreeing with `meta.mode`.
- Confirm: `meta.mode_choice` is one of `light-only | dark-only | both`.
- Confirm: `meta.hue_source` is one of `extracted-light | extracted-dark | extracted-both | declared-light`.
- Confirm: `meta.primary` is a JSON **boolean** (not the string `"true"`), and equals `(meta.mode == {{hue_source_mode}})`. Across the whole run, **exactly one** written file has `primary: true`.
- Confirm: the `:root` block contains all 15 documentation-chrome custom properties and no leftover `{{DOC_CHROME_VARS}}`.
- Confirm: the `:root` block contains `color-scheme: light;` on a light render or `color-scheme: dark;` on a dark render — matching `meta.mode`, and appearing exactly once.
- Confirm: the rendered string contains **no** `::-webkit-calendar-picker-indicator` rule that sets `color`, `fill`, or `filter`, and no `cv-input-icon` / `cv-input-wrap` markup. Date/time inputs render bare (`<input type="date" class="cv-input">`) — the UA supplies the picker glyph and `color-scheme` supplies its colour. See `component-catalogue.md` → *Native-control policy*.

**Derived-file assertions (only when `{{mode}} != {{hue_source_mode}}` and `meta.hue_source != extracted-both`):**

- Confirm: every one of the 11 per-mode colour entries (all except `brand`) and 3 shadow entries has a `source` beginning `derived: {{mode}} variant of` — a derived file whose colours still claim a reference (a CSS selector or a PDF page) is a provenance failure and a hard halt.
- Confirm: every `prov` in the file is still one of the two markers (the derived tokens are `system-derived`; no third marker was introduced).
- Confirm: the attribution paragraph contains the derived-variant clause naming `design-system-{{hue_source_mode}}.html`. A derived file must never present itself as extracted.
- Confirm: `meta.brand_fonts` and the `{{BRAND_FONT_LINKS}}` block are **byte-identical** to the hue-source file's, and — after §E's inject — so is the filled `brand-font-faces` block. Typography is mode-invariant, so a derived file loading a different face — or loading none — means the shared token set was not actually shared.

**Dark-render assertion:** the `rgba(0,0,0,` check belongs to §B.4 sub-step 4 and is made there, on the raw buffers **before** token substitution. Do **not** re-assert it here on the rendered string — dark shadow token values legitimately contain `rgba(0,0,0,`, so the assertion is only meaningful at the swap point.

- Compute `sha256` of **this file's** rendered byte string (template + standards). Store as `{{expected_sha256_<mode>}}`. Never reuse one mode's hash for the other file.

## D. Write

1. Ensure the `generated-docs/design-system/` directory exists. If not, create it: `Bash mkdir -p generated-docs/design-system` (a no-op on the second render).
2. Write the rendered string to `generated-docs/design-system/design-system-{{mode}}.html` (single atomic Write call).
   **On this run's first final-render Write only:** if a `generated-docs/design-system/design-system-<mode>.html` exists for a mode not in `{{files_to_write}}`, remove it now (`Bash rm -f generated-docs/design-system/design-system-<that mode>.html`). The orchestrator's Reset no longer deletes the accepted files, so this is the one point where the previous design system is retired — after a palette pick, never before.
3. Store `{{artifact_written_{{mode}}}} = true` — i.e. `{{artifact_written_light}}` or `{{artifact_written_dark}}`.

## E. Verify the Write

Invoke `framework/skills/verify-artifact-write.md` with:

- `path = "generated-docs/design-system/design-system-{{mode}}.html"`
- `expected_sha256 = {{expected_sha256_<mode>}}`
- `expected_min_bytes = 14000` (HTML body + inlined CSS + JSON block + visual sections + components section + standards appendix runs well above this; a truncated render that drops the components section or the standards appendix will not. The threshold was raised from 8000 to 14000 when the components section was added. It applies **per file** — both modes render the same structure, so both clear it.)

If the skill returns `pass`, **fill the brand faces** — the file on disk now carries the empty marker block:

```
node framework/tools/font-embed.cjs inject --html generated-docs/design-system/design-system-{{mode}}.html --css generated-docs/design-system/.workspace/font-faces.css
```

- Exit ≠ 0 → halt per `framework/shared/refusal-registry.md > RF-04` (the file on disk is not the artefact this step claims to have written).
- Record the printed `sha256` / `bytes` as this file's **final** values; the pre-inject hash is superseded.
- Post-inject checks (Bash `grep -c` / the printed `bytes`, never a `Read` of the file): the marker `/* BRAND_FONT_FACES */` no longer appears; `bytes` ≥ the written byte count + `meta.brand_fonts.embedded_bytes`. Either failing → `RF-04` halt.
- The preview hook waits for this fill before it opens the file (`framework/shared/artifact-preview.md`), so the consultant's first view already shows the embedded faces.

Then:

- If more modes remain in `{{files_to_write}}`, return to §A and render the next one. (The hue-source file is now on disk and verified, which is the precondition for the derived render.)
- If every mode in `{{files_to_write}}` has been written and verified, advance to step-07.

If the skill returns `RF-04 trigger`, halt per the refusal-registry surface — the agent does not write a `completed` event for itself, the orchestrator surfaces the refusal, and the consultant resolves the underlying filesystem issue before re-running. **Halt immediately; do not proceed to the next mode.** A verified hue-source file plus a failed derived write is a partial run, and step-07's handback gate will reject it.

## F. Review Render (two palettes offered, no pick yet)

Runs instead of §D/§E when §0-bis selects a review render. Render each mode in `{{files_to_write}}` (hue-source first) once, with **both** palettes, by the §A–§C procedure with these differences — everything not listed is identical to a final render, and the component catalogue is still rendered **once** per file:

1. **`{{PALETTE_VARS}}`** — two blocks instead of one: `    :root:has(#palette-neutral:checked) { --c-*: …; --on-*: … }` from `{{palettes}}.neutral.<mode>`, and `    :root:has(#palette-site-colour:checked) { … }` from `{{palettes}}.site_colour.<mode>`; then this tab CSS, verbatim:
   ```css
       .palette-tabs { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 12px; }
       .palette-tabs input { position: absolute; opacity: 0; pointer-events: none; }
       .palette-tabs label { padding: 6px 12px; border: 1px solid var(--border-strong); border-radius: 6px; cursor: pointer; }
       .palette-tabs input:checked + label { background: var(--fg); color: var(--bg); border-color: var(--fg); }
       .palette-tabs input:focus-visible + label { outline: 2px solid var(--fg); outline-offset: 2px; }
       .palette-tabs .palette-note { flex-basis: 100%; margin: 4px 0 0; color: var(--muted); font-size: 12px; }
       :root:has(#palette-neutral:checked) .pal-site-colour, :root:has(#palette-site-colour:checked) .pal-neutral { display: none; }
   ```
2. **`{{PALETTE_TABS}}`** —
   ```html
       <div class="palette-tabs" role="radiogroup" aria-label="Palette option">
         <input type="radio" name="palette" id="palette-neutral" checked><label for="palette-neutral">Option 1 — neutral (primary {{neutral_primary_hex}})</label>
         <input type="radio" name="palette" id="palette-site-colour"><label for="palette-site-colour">Option 2 — site colour (primary {{site_colour_primary_hex}})</label>
         <p class="palette-note">Review file — the two options differ only in primary, secondary and accent. Pick one in the chat; the final file holds only the chosen palette.</p>
       </div>
   ```
   with the two primary hexes substituted from `{{palettes}}.<palette>.<mode>.colours.primary`.
3. **Swatch hex labels** for `primary`, `secondary`, `accent` (the only tokens that differ) carry both values: `<code class="swatch-hex"><span class="pal-neutral">#…</span><span class="pal-site-colour">#…</span></code>`. Every other row is unchanged. `{{CONTRAST_ADJUSTMENTS}}` likewise wraps each option's helper lines in a `pal-neutral` / `pal-site-colour` span when they differ.
4. **JSON block** — the `neutral` palette's token set with `meta.palette_option: null`. (The JSON of a review file is never consumed; the authoritative pair is `options.json`.)
5. **Self-check** — §C applies, except: the file contains exactly two `--c-primary:` declarations, both radio inputs, and a non-empty `{{PALETTE_TABS}}`; and `meta.palette_option` is `null` while `{{palette_options}}` is non-null (no pick yet — this replaces §C's `palette_option` bullet for a review file). The mode / derived-file assertions apply unchanged.
6. **Write + verify + inject** — `generated-docs/design-system/.workspace/review-<mode>.html`, single atomic `Write`, then `framework/skills/verify-artifact-write.md` with that path, its own sha256, `expected_min_bytes = 14000`, then §E's `inject` with `--html` set to the review file. `RF-04` → halt. The preview hook opens each review file once it is filled (allowlisted in `framework/shared/artifact-preview.md`).

### F.3 `options.json` — the resume record

After every review file is written and verified, write `generated-docs/design-system/.workspace/options.json` (single `Write`, then `verify-artifact-write`, `expected_min_bytes = 512`). It holds everything a **final render** needs, so step-07 can collapse — now or after a resume — without re-extracting (the embedded faces stay in `.workspace/font-faces.css` beside it, which a resume reuses as is):

```json
{
  "version": 1,
  "references": [ { "kind": "url", "ref": "…", "status": "used" } ], "files_to_write": ["light", "dark"],
  "hue_source_mode": "light", "hue_source": "extracted-light", "mode_choice": "both",
  "palettes": {
    "neutral":     { "<mode>": { "tokens": { <the full design-tokens object for that file, meta.palette_option = "neutral"> }, "on_colours": { … }, "adjustments": [ … ] } },
    "site_colour": { "<mode>": { "tokens": { … meta.palette_option = "site-colour" … }, "on_colours": { … }, "adjustments": [ … ] } }
  },
  "shared": { "assign_decisions": [ … ], "brand": "#…", "extraction_method": "…",
              "font_rejected_heading": null, "font_rejected_body": null, "brand_fonts": { … },
              "attribution": { "extraction_status": "…", "lead_url": "…" } },
  "review_files": ["generated-docs/design-system/.workspace/review-light.html", "…"]
}
```

`tokens` is exactly the object §B.1 serialises into `{{TOKENS_JSON}}` for that mode and palette, so a final render reads it back verbatim. **A final render after a resume** (step-07 §A-0) takes, for the chosen palette and each mode: `{{TOKENS_JSON}}` = `tokens` verbatim; `--c-<token>` = `tokens.colours.<token>.hex`; `--on-<fill>` = `on_colours.<fill>`; the contrast section from `tokens.contrast`; `{{CONTRAST_ADJUSTMENTS}}` from `adjustments`. That is the `{{palettes}}` view §C checks against. `options.json` is read only by step-07 and the orchestrator's resume gate — never by any other pipeline — and is deleted with the rest of `.workspace/` on accept.

---

**Next:** Read fully and follow `step-07-handback.md`.
