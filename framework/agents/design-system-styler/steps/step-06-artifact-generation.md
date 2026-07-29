---
name: step-06-artifact-generation
description: 'Render one single-mode artefact per mode in files_to_write — hue-source mode first: build the JSON token block, render the visual sections, populate the HTML template, append the static standards HTML verbatim, write to design-system/design-system-<mode>.html, then verify each write.'
# Variables referenced (inherited from agent):
# prompt_artifact_generation: 'framework/agents/design-system-styler/prompt-templates/artifact-generation.md'
# template_path: 'framework/assets/template-design-system.html'
# standards_path: 'framework/assets/design-system-standards.html'
# component_catalogue: 'framework/agents/design-system-styler/data/component-catalogue.md'
# output_path_light: 'design-system/design-system-light.html'
# output_path_dark: 'design-system/design-system-dark.html'
---

# Step 6: Generate the Artefact(s)

## 0. Read inputs (batched)

Read all four static render inputs in a **single batched message** (the harness runs the reads concurrently); none depends on another, so there is no reason to serialise the reads:

- `framework/agents/design-system-styler/prompt-templates/artifact-generation.md` — the generation instructions applied below.
- `framework/assets/template-design-system.html` — the structural base (§A).
- `framework/agents/design-system-styler/data/component-catalogue.md` — the Components section source (§A / §B.4).
- `framework/assets/design-system-standards.html` — the static standards appendix (§B-bis).

**If `design-system-standards.html` cannot be read** (absent or unreadable), halt — do not write a partial artefact. (This is the same guard previously stated in §B-bis; it now applies to the batched read.)

With all four in context, apply the artifact-generation prompt's instructions in the order below.

**Read once, render N times.** These four inputs do not vary by mode — do **not** re-read them per mode.

**Inputs (in-memory after step-05b):**

- The **hue-source token set** — 11 colours (status colours always domain-filled), 15 typography, 7 effects — in `{{hue_source_mode}}`'s scheme.
- The **derived token set**, if `{{derived_mode_requested}}` — the same 33 tokens in the opposite mode, its 11 colours + 3 shadows carrying `derived: …` source strings and its 19 shared tokens copied verbatim.
- `{{voice}}` — one-line Voice statement synthesised in step-05b
- **Mode state:** `{{files_to_write}}`, `{{hue_source_mode}}`, `{{mode_choice}}`, `{{hue_source}}`, `{{primary_mode}}`, `{{extracted_scheme}}`
- **Per-mode contrast:** `{{cv_pass_count_light}}` / `{{cv_adjustments_light}}` / `{{cv_adjustment_count_light}}` and the `_dark` twins
- `{{extraction_status}}`, `{{extraction_date}}`, `{{domain}}`, `{{domain_provenance}}`, `{{reference_url}}`, `{{css_source_type}}`, `{{css_source_url}}`

## 0-bis. Render Loop

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
2. **Section 4 — Attribution paragraph.** Pick the variant per `{{extraction_status}}` and `{{reference_url}}` state. The rendered string is inserted **as inner HTML of the `<blockquote class="attribution">`** (already in the template); the styler emits raw text plus any necessary `<a>` anchors for URLs. Substitute into `{{ATTRIBUTION_PARAGRAPH}}`.
3. **Section 5 — Provenance tagging.** Every token in the JSON gets `prov` set to one of `extracted-from-url` or `inferred-from-domain`. Every visual snippet that surfaces a token gets a matching `<span class="prov prov-{{prov-slug}}">{{prov}}</span>` element (`prov-slug` is the prov value verbatim — `extracted-from-url` or `inferred-from-domain`, used directly as a CSS class suffix).
4. **Section 6 — Render visual snippets.** Build the four pre-rendered HTML blocks and substitute them into the template placeholders:
    - `{{COLOUR_SWATCHES}}` — 11 `<li class="swatch-row">` blocks per the COLOUR ROW SCHEMA. Each `<div class="swatch">` carries `style="background:{{hex}}"`; each row also surfaces the hex (in `<code>`), source-context, and provenance.
    - `{{TYPE_FAMILY_SPECIMENS}}` — 2 `<div class="type-specimen">` blocks (heading + body). Inline style on the sample: `font-family: {{family-stack}}; font-weight: {{paired-weight}}`. The token-value shown in the meta column is the literal family stack. **Prepend one rendering note** before the two blocks (see `artifact-generation.md` → `{{TYPE_FAMILY_SPECIMENS}}`): the artefact loads no webfont, so the sample only renders in the named family when that face is installed on the reader's machine. Use existing chrome markup for the note — no new CSS class, no template edit.
    - `{{TYPE_SIZE_SPECIMENS}}` — 8 `<div class="type-specimen">` blocks (text-xs..text-4xl). Inline style on the sample: `font-size: {{value}}`. Sample text is the fixed pangram.
    - `{{TYPE_LH_SPECIMENS}}` — 3 `<div class="type-specimen">` blocks (tight/base/loose). Sample is a two-line span (the pangram repeated, or wrapped) so the line-height is visible. Inline style: `line-height: {{value}}`.
    - `{{SHADOW_SPECIMENS}}` — 3 `<div class="shadow-card">` blocks. Inline style: `box-shadow: {{value}}` on the card; render the token name, the literal value (in `<code>`), and the provenance label.
    - `{{MOTION_SPECIMENS}}` — 4 `<div class="motion-row">` blocks (transition-fast / transition-base / transition-slow / easing-standard) per the MOTION SCHEMA. The animated dot's inline style is `animation-duration: {{value}}; animation-timing-function: {{easing-token-value}};` for transition rows, and `animation-duration: 2s; animation-timing-function: {{value}};` for the easing-standard row.
    - `{{CONTRAST_PAIRS}}` — 4 `<div class="contrast-card">` blocks per the CONTRAST PAIR SCHEMA. Inline style: `background: {{bg-hex}}; color: {{fg-hex}};`. Pair label and ratio printed inside; the status badge uses class `status-pass` (ratio ≥ 4.5) or `status-fail`.
    - `{{CONTRAST_ADJUSTMENTS}}` — the adjustments line (`none`, or the comma-separated `{token} adjusted from {original} to {adjusted} ({pair} contrast was {ratio}:1)` record).
    - `{{COMPONENT_STYLES}}` and `{{COMPONENT_SPECIMENS}}` — sourced from the component catalogue. Procedure:
        1. Parse the catalogue's `## Render order` list. Each numbered bullet is a family slug (`buttons`, `form-inputs`, `alerts`, `badges`, `cards`, `data-table`, `tabs`, `modal`). A bullet whose line starts with `<!--` or `#` is **skipped** — the family is not rendered.
        2. Extract the single fenced `css` block under `## Component CSS`. Its inner content (no fences) is the **component-css buffer**.
        3. For each enabled family slug, in render order, locate the catalogue heading `## {{slug}}`, then extract the two fenced `html` blocks under `### Live demo` and `### States matrix` (in that order). Wrap each family's two snippets in `<div class="cv-family"><h3>{{Title-Case-Slug}}</h3><p class="cv-note">Live demo</p>{{live-demo-html}}<p class="cv-note">States matrix</p>{{states-matrix-html}}</div>`. Append to the **component-specimens buffer**.
        4. **Dark-render neutral swap — only when `{{mode}} == "dark"`.** On the **raw** buffers, before any token substitution, replace every occurrence of `rgba(0,0,0,` with `rgba(255,255,255,`, leaving the alpha and everything else untouched. There are no exemptions. Then assert: **neither buffer still contains the substring `rgba(0,0,0,`** — if one does, the swap was incomplete; halt.

            **This must run before sub-step 5, not after.** The catalogue substitutes `{{effects.shadow_sm|md|lg.value}}` at five sites, and dark shadow tokens are deliberately *black with raised alpha* (dark elevation is carried by the lighter `surface`). Swapping after substitution would flip those shadows to white and destroy the treatment; swapping before means substituted values are untouched by construction. See `component-catalogue.md` → *Dark-render neutral swap*.

            On a light render, skip this sub-step entirely — the catalogue's constants are already authored for a light surface.
        5. **Token-substitute** both buffers in memory: for every reference of the form `{{colours.<name>.hex}}`, `{{typography.<name>.value}}`, or `{{effects.<name>.value}}`, replace with the literal value from **`{{mode}}`'s token set**. This is plain string replacement — no other substitution semantics. After this pass, **no `{{colours.…}}` / `{{typography.…}}` / `{{effects.…}}` references must remain** in either buffer.
        6. Substitute the component-css buffer into the template's `{{COMPONENT_STYLES}}` placeholder (which sits inside the `<style>` block, immediately before `</style>`).
        7. Substitute the component-specimens buffer into the template's `{{COMPONENT_SPECIMENS}}` placeholder (which sits inside `<section id="components">`).
5. **Section 7 — Page-level scalars.** Substitute `{{DOMAIN}}` (the lowercased+trimmed consultant input) and `{{GENERATED_AT}}` (ISO date) into the `<head>` `<title>`, the H1, and the generated-at line. Also substitute the two mode-scoped placeholders:
    - `{{MODE_LABEL}}` — `Light` or `Dark`, title-cased, matching `{{mode}}`. It appears in **both** the `<title>` and the H1.
    - `{{DOC_CHROME_VARS}}` — the fixed literal block for `{{mode}}` from the template's **DOC CHROME** comment section, substituted into the template's `:root`. These are documentation-chrome values: brand-neutral, identical for every run and every domain. Do **not** derive them from brand tokens, and do **not** run them through contrast validation. Copy the block for this mode verbatim; all 15 custom properties **and** the block's leading `color-scheme: {{mode}};` declaration must be present. That declaration is load-bearing, not cosmetic: it is what makes the browser paint UA-drawn control parts (the `<input type="date">` picker indicator, number spinners, native checkbox/radio, `<select>` popup, scrollbars) in the file's own mode. Omit it on a dark render and every date field shows a black calendar glyph on a dark surface — invisible.
6. **Contrast section — this mode's own numbers.** `{{CONTRAST_PAIRS}}` and `{{CONTRAST_ADJUSTMENTS}}` render from `{{mode}}`'s cv variables (`{{cv_pass_count_<mode>}}`, `{{cv_adjustments_<mode>}}`). A derived set was validated independently in step-05b §F and never inherits the hue-source set's ratios.

The artefact is generated even when `{{extraction_status}}` ≠ `"success"`. The doc is always complete (every token domain-inferred if extraction was skipped); the JSON `meta.extraction_status` field records *why* the URL path didn't yield extracted values.

## B-bis. Append the Static Standards Appendix

After the template is fully rendered (all placeholders replaced except `{{STANDARDS_BLOCK}}`) and before the pre-write self-check, substitute the static standards file (`design-system-standards.html`, read in Section 0):

1. Substitute its **full contents verbatim** into the `{{STANDARDS_BLOCK}}` placeholder. The standards file opens with its own HTML comment block and a `<section id="standards" class="standards">` wrapper, so it slots in cleanly after the contrast section.
2. **Do not modify the standards content.** No placeholder substitution, no rewording, no truncation. It is static reference material that ships verbatim with every output. (The read-failure halt is handled in Section 0.)

## C. Pre-Write Self-Check

Runs **per file**, before that file's `Write`:

- Render the full artefact (template body + substituted standards) as one string in memory.
- Confirm: every `{{placeholder}}` has been replaced. No literal `{{...}}` substrings remain. (The standards block contains no placeholders. `{{MODE_LABEL}}` and `{{DOC_CHROME_VARS}}` must both be substituted. The catalogue's token references — `{{colours.…}}`, `{{typography.…}}`, `{{effects.…}}` — must also be fully substituted; any survivor indicates a typo in the catalogue or a missing token in the in-memory set, and is a hard halt.)
- Confirm: the `<script type="application/json" id="design-tokens">` block is present, and its inner content is **valid JSON** — parse it back in memory to verify. If parsing fails, halt and do not Write.
- Confirm: the JSON `meta`, `colours`, `typography`, `effects`, and `contrast` keys are all present.
- Confirm: `meta.domain_provenance` is present and is one of `suggested-from-url-accepted | suggested-from-url-overridden | consultant-typed`.
- Confirm: every `prov` value in the JSON is one of `extracted-from-url` or `inferred-from-domain`. No third marker.
- Confirm: status-colour entries (success/warning/error/info) all carry `prov: "inferred-from-domain"` regardless of the URL outcome.
- Confirm: the document closes with `</body>\n</html>` (the template's literal closing tags are intact and not duplicated).
- Confirm: the rendered string contains the literal substring `<section id="standards"` (from the appended standards file) exactly once.
- Confirm: the rendered string contains the literal substring `<section id="components"` exactly once.
- Confirm: the rendered string contains the literal substring `class="cv-btn` at least once (smoke test that the component CSS / HTML from the catalogue actually landed in the artefact; a buffer-substitution failure would drop it silently).
- Confirm: the rendered string contains the literal substring `class="type-render-note"` exactly once (the family-specimen rendering caveat landed — see `artifact-generation.md` → `{{TYPE_FAMILY_SPECIMENS}}`).

**Brand-family assertions (all files):**

Check the **two in-memory token values** `typography.heading_family.value` and `typography.body_family.value` — **not** the rendered string. Those two values are the sole source of every brand `font-family:` declaration in the artefact (the ~20 component-catalogue substitution sites plus the 2 family specimens), so two checks are exhaustive. A whole-string scan would false-positive on the documentation chrome, which legitimately declares `system-ui` and is exempt (see the `DOC CHROME` comment in `template-design-system.html`).

- Confirm: neither value contains a **non-brand family** from group (a), (b), or (d) of `data/font-rules.md` §1, in any position.
- Confirm: neither value contains a group-(c) position-dependent face (`Roboto`, `Noto Sans`, `Ubuntu`, `Cantarell`, `Oxygen`, `Droid Sans`) in any position **other than first**. First position is a legitimate brand choice.
- Confirm: each value matches the emitted stack shape `'<Family>', <generic>` — exactly one quoted named family, then exactly one generic terminal, nothing more.

Any failure is a **hard halt before the `Write`**. This should never fire: `font-rules.md` §1 stops a non-brand family at extraction and `domain-inference.md` §C.1 stops one at inference, so a violation reaching step-06 means one of those two rules was skipped. It is a fail-closed backstop, not the primary mechanism — do not "repair" the value here and continue, and do not downgrade the halt to a warning. Shipping `Arial` as a client's brand font is the defect this whole rule exists to prevent, and unlike an unreachable contrast ratio it has a free, deterministic correct answer (leave the token unset; step-05b infers a real webfont).

**Mode assertions (all files):**

- Confirm: `meta.mode` is present and is `light` or `dark`, and **matches the filename suffix** this file is about to be written to.
- Confirm: the literal `({{MODE_LABEL}})`-substituted text appears in **both** the `<title>` and the H1 — i.e. `(Light)` or `(Dark)`, agreeing with `meta.mode`.
- Confirm: `meta.mode_choice` is one of `light-only | dark-only | both`.
- Confirm: `meta.hue_source` is one of `extracted-light | extracted-dark | domain-inferred-light`.
- Confirm: `meta.primary` is a JSON **boolean** (not the string `"true"`), and equals `(meta.mode == {{hue_source_mode}})`. Across the whole run, **exactly one** written file has `primary: true`.
- Confirm: the `:root` block contains all 15 documentation-chrome custom properties and no leftover `{{DOC_CHROME_VARS}}`.
- Confirm: the `:root` block contains `color-scheme: light;` on a light render or `color-scheme: dark;` on a dark render — matching `meta.mode`, and appearing exactly once.
- Confirm: the rendered string contains **no** `::-webkit-calendar-picker-indicator` rule that sets `color`, `fill`, or `filter`, and no `cv-input-icon` / `cv-input-wrap` markup. Date/time inputs render bare (`<input type="date" class="cv-input">`) — the UA supplies the picker glyph and `color-scheme` supplies its colour. See `component-catalogue.md` → *Native-control policy*.

**Derived-file assertions (only when `{{mode}} != {{hue_source_mode}}`):**

- Confirm: every one of the 11 colour entries and 3 shadow entries has a `source` beginning `derived: {{mode}} variant of` — a derived file whose colours still claim a CSS selector or a bare `domain-inference (…)` source is a provenance failure and a hard halt.
- Confirm: every `prov` in the file is still one of the two markers (the derived tokens are `inferred-from-domain`; no third marker was introduced).
- Confirm: the attribution paragraph contains the derived-variant clause naming `design-system-{{hue_source_mode}}.html`. A derived file must never present itself as extracted.

**Dark-render assertion:** the `rgba(0,0,0,` check belongs to §B.4 sub-step 4 and is made there, on the raw buffers **before** token substitution. Do **not** re-assert it here on the rendered string — dark shadow token values legitimately contain `rgba(0,0,0,`, so the assertion is only meaningful at the swap point.

- Compute `sha256` of **this file's** rendered byte string (template + standards). Store as `{{expected_sha256_<mode>}}`. Never reuse one mode's hash for the other file.

## D. Write

1. Ensure the `design-system/` directory exists. If not, create it: `Bash mkdir -p design-system` (a no-op on the second render).
2. Write the rendered string to `design-system/design-system-{{mode}}.html` (single atomic Write call).
3. Store `{{artifact_written_{{mode}}}} = true` — i.e. `{{artifact_written_light}}` or `{{artifact_written_dark}}`.

## E. Verify the Write

Invoke `framework/skills/verify-artifact-write.md` with:

- `path = "design-system/design-system-{{mode}}.html"`
- `expected_sha256 = {{expected_sha256_<mode>}}`
- `expected_min_bytes = 14000` (HTML body + inlined CSS + JSON block + visual sections + components section + standards appendix runs well above this; a truncated render that drops the components section or the standards appendix will not. The threshold was raised from 8000 to 14000 when the components section was added. It applies **per file** — both modes render the same structure, so both clear it.)

If the skill returns `pass`:

- If more modes remain in `{{files_to_write}}`, return to §A and render the next one. (The hue-source file is now on disk and verified, which is the precondition for the derived render.)
- If every mode in `{{files_to_write}}` has been written and verified, advance to step-07.

If the skill returns `RF-04 trigger`, halt per the refusal-registry surface — the agent does not write a `completed` event for itself, the orchestrator surfaces the refusal, and the consultant resolves the underlying filesystem issue before re-running. **Halt immediately; do not proceed to the next mode.** A verified hue-source file plus a failed derived write is a partial run, and step-07's handback gate will reject it.

---

**Next:** Read fully and follow `step-07-handback.md`.
