# Brand Style Extraction — Prompt Template

**Purpose:** This is a reusable instruction block for extracting brand colours, font families, typography scale, weights, line-heights, shadows, and motion tokens from CSS content via LLM analysis. The design-system-styler workflow loads this file after successfully fetching CSS content (step-04) and applies its instructions to produce structured brand extraction results.

**Usage:** Read this file using the Read tool. Apply the instructions to `{{primary_css_content}}` (the CSS text obtained from the two-pass site fetching step).

Ported from v3 b3-style-extractor and extended for the v7b-test token scope (status colours, typography scale, line-heights, shadows, motion). Border-radius and spacing extraction are explicitly out of scope for v1.

---

## Data File References

The extraction logic is organized into focused data files. Step-05 reads them **in one batched message**; the application order below is what's preserved (the insufficient-data gate first, so it can short-circuit before any extraction reasoning):

| Order | Data File | Content |
|-------|-----------|---------|
| 1 | `prompt-templates/brand-extraction.md` (this file) | Extraction overview + the Section 7 output format. |
| 2 | `data/insufficient-data-handling.md` | Minimum 3-color threshold check (Section 8). Applied first; if threshold fails, all extraction is skipped and every token is routed to step-05b. |
| 3 | `data/color-extraction-rules.md` | CSS analysis strategy, colour extraction and normalization, colour-to-token mapping heuristics for the 7 brand tokens (Sections 1-3). Status colours are explicitly NOT extracted here — they always fall through to step-05b. |
| 4 | `data/font-rules.md` | Font family extraction (Section 4). Border-radius extraction has been removed from this rules file. |
| 5 | `data/typography-scale-rules.md` | Font-size scale, font-weight, line-height extraction (Sections A–C). |
| 6 | `data/shadow-motion-rules.md` | `box-shadow` elevation tokens, `transition-duration`, `transition-timing-function` (Sections E–F). |
| — | `data/contrast-validation.md` | WCAG AA contrast ratio validation and adjustment strategy (Section 6). **Read by step-05b, not step-05** — it validates the final token set (extracted *and* domain-inferred), so it runs after the domain-inference fill. |

**Note:** The six step-05 files are read in one batch; the application order in the table above is what's preserved. The insufficient-data gate is applied before colour extraction so it can short-circuit before any extraction reasoning when the CSS lacks sufficient data. Contrast validation (`contrast-validation.md`) is a step-05b concern, applied last so it can validate against any token (extracted *or* domain-inferred).

---

## 7. Output Format

After completing extraction and validation, produce this structured result. Tokens left unset by extraction (i.e. not found in the CSS) are written as `null` here and filled by step-05b before artefact generation.

```yaml
extraction_status: "success"  # or "no_url" | "fetch_failed" | "no_css" | "css_fetch_failed" | "insufficient_data"

extracted_colors:
  primary:     { hex: "#RRGGBB" | null, source: "{css_selector_or_property}" | null }
  secondary:   { hex: "#RRGGBB" | null, source: "{source_context}" | null }
  accent:      { hex: "#RRGGBB" | null, source: "{source_context}" | null }
  background:  { hex: "#RRGGBB" | null, source: "{source_context}" | null }
  surface:     { hex: "#RRGGBB" | null, source: "{source_context}" | null }
  text:        { hex: "#RRGGBB" | null, source: "{source_context}" | null }
  text-muted:  { hex: "#RRGGBB" | null, source: "{source_context}" | null }
  # Status colours (success/warning/error/info) are NOT extracted here.
  # They are always populated by step-05b via per-run domain inference.

extracted_typography:
  heading_family:  { value: "Font Name" | null, source: "{source_context}" | null }
  heading_weight:  { value: 600 | null,         source: "{source_context}" | null }
  body_family:     { value: "Font Name" | null, source: "{source_context}" | null }
  body_weight:     { value: 400 | null,         source: "{source_context}" | null }
  size_xs:         { value: "0.75rem" | null,   source: "{source_context}" | null }
  size_sm:         { value: "0.875rem" | null,  source: "{source_context}" | null }
  size_base:       { value: "1rem" | null,      source: "{source_context}" | null }
  size_lg:         { value: "1.125rem" | null,  source: "{source_context}" | null }
  size_xl:         { value: "1.25rem" | null,   source: "{source_context}" | null }
  size_2xl:        { value: "1.5rem" | null,    source: "{source_context}" | null }
  size_3xl:        { value: "1.875rem" | null,  source: "{source_context}" | null }
  size_4xl:        { value: "2.25rem" | null,   source: "{source_context}" | null }
  lh_tight:        { value: 1.25 | null,        source: "{source_context}" | null }
  lh_base:         { value: 1.5 | null,         source: "{source_context}" | null }
  lh_loose:        { value: 1.75 | null,        source: "{source_context}" | null }

extracted_effects:
  shadow_sm:       { value: "0 1px 2px ..." | null, source: "{source_context}" | null }
  shadow_md:       { value: "0 4px 6px ..." | null, source: "{source_context}" | null }
  shadow_lg:       { value: "0 10px 15px ..." | null, source: "{source_context}" | null }
  dur_fast:        { value: "150ms" | null,         source: "{source_context}" | null }
  dur_base:        { value: "200ms" | null,         source: "{source_context}" | null }
  dur_slow:        { value: "300ms" | null,         source: "{source_context}" | null }
  easing_standard: { value: "cubic-bezier(...)" | null, source: "{source_context}" | null }

contrast_validation:
  text_on_background:        { ratio: 7.2, pass: true }
  text_on_surface:           { ratio: 6.8, pass: true }
  text_muted_on_background:  { ratio: 4.6, pass: true }
  text_muted_on_surface:     { ratio: 4.5, pass: true }
  adjustments_made:
    - { token: "text-muted", original: "#9CA3AF", adjusted: "#6B7280", reason: "text-muted on surface ratio was 3.8:1, needed 4.5:1" }
```

**Diagnostic summary** (append to step-07 handback report):

```
STYLER BRAND EXTRACTION
───────────────────────
Colours extracted: {extracted_count}/7 brand tokens (status colours always inferred-from-domain)
  primary: {hex_or_null} (from: {source_or_null})
  ... (one line per token)
Typography extracted: {extracted_typo_count}/15 tokens
  heading: {family_or_null} {weight_or_null}
  body: {family_or_null} {weight_or_null}
  scale tokens found: {size_count}/8
  line-heights found: {lh_count}/3
Effects extracted: {extracted_effects_count}/7 tokens
  shadows found: {shadow_count}/3
  motion found: {motion_count}/4
Contrast validation: {pass_count}/4 passed ({adjustment_count} adjustments made)
Extraction status: {extraction_status}
```
