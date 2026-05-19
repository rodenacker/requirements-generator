---
name: step-06-artifact-generation
description: 'Build the JSON token block, render the visual sections, populate the HTML template, append the static standards HTML verbatim, write to design-system/design-system.html, then verify the write.'
# Variables referenced (inherited from agent):
# prompt_artifact_generation: 'framework/agents/design-system-styler/prompt-templates/artifact-generation.md'
# template_path: 'framework/assets/template-design-system.html'
# standards_path: 'framework/assets/design-system-standards.html'
# output_path: 'design-system/design-system.html'
---

# Step 6: Generate the Artefact

Read the artifact-generation prompt template:

```
Read tool: framework/agents/design-system-styler/prompt-templates/artifact-generation.md
```

**Inputs (in-memory after step-05b):**

- `{{extracted_colors}}` — 7 brand tokens (status colours always domain-filled)
- `{{status_colors}}` — 4 status tokens (always `inferred-from-domain`)
- `{{extracted_typography}}` — 15 typography tokens
- `{{extracted_effects}}` — 7 effect tokens
- `{{contrast_validation}}` — 4 pair ratios + adjustments line
- `{{voice}}` — one-line Voice statement synthesised in step-05b
- `{{extraction_status}}`, `{{extraction_date}}`, `{{domain}}`, `{{reference_url}}`, `{{css_source_type}}`, `{{css_source_url}}`

## A. Source the Template

Read `framework/assets/template-design-system.html`. Use it as the structural base. Replace every `{{placeholder}}` with the corresponding in-memory value. Do not insert, remove, or reorder sections.

## B. Apply the Artifact-Generation Prompt

Apply the prompt template's instructions in order:

1. **Section 3 — JSON metadata block.** Build the `tokens` object in memory with `meta`, `colours`, `typography`, `effects`, and `contrast` keys per the JSON SHAPE documented at the top of the template. Serialise with `JSON.stringify`-equivalent 2-space indent. Substitute into `{{TOKENS_JSON}}`.
2. **Section 4 — Attribution paragraph.** Pick the variant per `{{extraction_status}}` and `{{reference_url}}` state. The rendered string is inserted **as inner HTML of the `<blockquote class="attribution">`** (already in the template); the styler emits raw text plus any necessary `<a>` anchors for URLs. Substitute into `{{ATTRIBUTION_PARAGRAPH}}`.
3. **Section 5 — Provenance tagging.** Every token in the JSON gets `prov` set to one of `extracted-from-url` or `inferred-from-domain`. Every visual snippet that surfaces a token gets a matching `<span class="prov prov-{{prov-slug}}">{{prov}}</span>` element (`prov-slug` is the prov value verbatim — `extracted-from-url` or `inferred-from-domain`, used directly as a CSS class suffix).
4. **Section 6 — Render visual snippets.** Build the four pre-rendered HTML blocks and substitute them into the template placeholders:
    - `{{COLOUR_SWATCHES}}` — 11 `<li class="swatch-row">` blocks per the COLOUR ROW SCHEMA. Each `<div class="swatch">` carries `style="background:{{hex}}"`; each row also surfaces the hex (in `<code>`), source-context, and provenance.
    - `{{TYPE_FAMILY_SPECIMENS}}` — 2 `<div class="type-specimen">` blocks (heading + body). Inline style on the sample: `font-family: {{family-stack}}; font-weight: {{paired-weight}}`. The token-value shown in the meta column is the literal family stack.
    - `{{TYPE_SIZE_SPECIMENS}}` — 8 `<div class="type-specimen">` blocks (text-xs..text-4xl). Inline style on the sample: `font-size: {{value}}`. Sample text is the fixed pangram.
    - `{{TYPE_LH_SPECIMENS}}` — 3 `<div class="type-specimen">` blocks (tight/base/loose). Sample is a two-line span (the pangram repeated, or wrapped) so the line-height is visible. Inline style: `line-height: {{value}}`.
    - `{{SHADOW_SPECIMENS}}` — 3 `<div class="shadow-card">` blocks. Inline style: `box-shadow: {{value}}` on the card; render the token name, the literal value (in `<code>`), and the provenance label.
    - `{{MOTION_SPECIMENS}}` — 4 `<div class="motion-row">` blocks (transition-fast / transition-base / transition-slow / easing-standard) per the MOTION SCHEMA. The animated dot's inline style is `animation-duration: {{value}}; animation-timing-function: {{easing-token-value}};` for transition rows, and `animation-duration: 2s; animation-timing-function: {{value}};` for the easing-standard row.
    - `{{CONTRAST_PAIRS}}` — 4 `<div class="contrast-card">` blocks per the CONTRAST PAIR SCHEMA. Inline style: `background: {{bg-hex}}; color: {{fg-hex}};`. Pair label and ratio printed inside; the status badge uses class `status-pass` (ratio ≥ 4.5) or `status-fail`.
    - `{{CONTRAST_ADJUSTMENTS}}` — the adjustments line (`none`, or the comma-separated `{token} adjusted from {original} to {adjusted} ({pair} contrast was {ratio}:1)` record).
5. **Section 7 — Page-level scalars.** Substitute `{{DOMAIN}}` (the lowercased+trimmed consultant input) and `{{GENERATED_AT}}` (ISO date) into the `<head>` `<title>`, the H1, and the generated-at line.

The artefact is generated even when `{{extraction_status}}` ≠ `"success"`. The doc is always complete (every token domain-inferred if extraction was skipped); the JSON `meta.extraction_status` field records *why* the URL path didn't yield extracted values.

## B-bis. Append the Static Standards Appendix

After the template is fully rendered (all placeholders replaced except `{{STANDARDS_BLOCK}}`) and before the pre-write self-check, substitute the static standards file:

1. Read `framework/assets/design-system-standards.html`.
2. Substitute its **full contents verbatim** into the `{{STANDARDS_BLOCK}}` placeholder. The standards file opens with its own HTML comment block and a `<section id="standards" class="standards">` wrapper, so it slots in cleanly after the contrast section.
3. **Do not modify the standards content.** No placeholder substitution, no rewording, no truncation. It is static reference material that ships verbatim with every output. If the file cannot be read, halt — do not write a partial artefact.

## C. Pre-Write Self-Check

Before calling `Write`:

- Render the full artefact (template body + substituted standards) as one string in memory.
- Confirm: every `{{placeholder}}` has been replaced. No literal `{{...}}` substrings remain. (The standards block contains no placeholders.)
- Confirm: the `<script type="application/json" id="design-tokens">` block is present, and its inner content is **valid JSON** — parse it back in memory to verify. If parsing fails, halt and do not Write.
- Confirm: the JSON `meta`, `colours`, `typography`, `effects`, and `contrast` keys are all present.
- Confirm: every `prov` value in the JSON is one of `extracted-from-url` or `inferred-from-domain`. No third marker.
- Confirm: status-colour entries (success/warning/error/info) all carry `prov: "inferred-from-domain"` regardless of the URL outcome.
- Confirm: the document closes with `</body>\n</html>` (the template's literal closing tags are intact and not duplicated).
- Confirm: the rendered string contains the literal substring `<section id="standards"` (from the appended standards file) exactly once.
- Compute `sha256` of the rendered byte string (template + standards). Store as `{{expected_sha256}}`.

## D. Write

1. Ensure the `design-system/` directory exists. If not, create it: `Bash mkdir -p design-system`.
2. Write the rendered string to `design-system/design-system.html` (single atomic Write call).
3. Store `{{artifact_path}} = "design-system/design-system.html"` and `{{artifact_written}} = true`.

## E. Verify the Write

Invoke `framework/skills/verify-artifact-write.md` with:

- `path = "design-system/design-system.html"`
- `expected_sha256 = {{expected_sha256}}`
- `expected_min_bytes = 8000` (HTML body + inlined CSS + JSON block + visual sections + standards appendix runs well above this; a truncated render that drops any section will not)

If the skill returns `pass`, advance to step-07.

If the skill returns `RF-04 trigger`, halt per the refusal-registry surface — the agent does not write a `completed` event for itself, the orchestrator surfaces the refusal, and the consultant resolves the underlying filesystem issue before re-running.

---

**Next:** Read fully and follow `step-07-handback.md`.
