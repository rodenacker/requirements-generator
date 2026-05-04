# Artifact Generation — Prompt Template

**Purpose:** Reusable instruction block for writing the populated design-system doc to `design-system/design-system.md`. The design-system-styler workflow loads this file after extraction (step-05) and domain-defaults fill (step-05b), then applies its instructions to serialize the in-memory token set into the structured artefact.

**Usage:** Read this file using the Read tool. Apply the instructions to the in-memory results: `{{extracted_colors}}`, `{{extracted_typography}}`, `{{extracted_effects}}`, `{{contrast_validation}}`, `{{extraction_status}}`, plus the domain-defaults fill outputs and the consultant inputs (`{{domain}}`, `{{domain_source}}`, `{{reference_url}}`).

Adapted from v3 b3-style-extractor: the output path moved from `genesis/extracted-brand.md` to `design-system/design-system.md`, all references to a B5 downstream consumer have been removed, and the schema has been extended to cover status colours, typography scale, and effects.

---

## 1. Output File Structure

The artefact file `design-system/design-system.md` is populated from `framework/assets/template-design-system.md`. It has three distinct sections (in this exact order):

1. **YAML frontmatter** — provenance metadata
2. **Extraction Summary** — human-readable tables with Source Context and Provenance columns
3. **Brand sections** — machine-readable token tables for downstream consumption

```
---
(frontmatter metadata)
---

# Design System: {{domain}}
> (attribution paragraph + provenance reminder)

## Extraction Summary
### Colours              ← human-readable, 11 rows, Source Context + Provenance columns
### Typography           ← human-readable, 15 rows, Source Context + Provenance columns
### Effects              ← human-readable, 7 rows, Source Context + Provenance columns
### Contrast Validation  ← human-readable, 4 pairs + adjustments line

## Brand Colours         ← machine-readable, 11 rows, Token | Value
## Brand Typography      ← machine-readable, three sub-tables (Families, Sizes, Line Heights)
## Brand Effects         ← machine-readable, two sub-tables (Shadows, Motion)
```

The Extraction Summary and Brand sections intentionally duplicate the values. The Summary carries Source Context + Provenance for review; the Brand sections carry only the values for clean machine consumption. Do not merge them.

---

## 2. Source the Template

Read `framework/assets/template-design-system.md` and use it as the structural base. Replace every `{{placeholder}}` with the corresponding value from the in-memory extraction + fill results. Do not insert, remove, or reorder sections.

---

## 3. Frontmatter

```yaml
---
reference_url: "{{reference_url_or_null}}"
extraction_date: "{{extraction_date}}"
extraction_status: "{{extraction_status}}"
domain: "{{domain}}"
domain_source: "{{domain_source}}"        # "curated" or "free-text"
css_source_type: "{{css_source_type_or_null}}"
css_source_url: "{{css_source_url_or_null}}"
---
```

- `reference_url`: the URL the consultant supplied, or `null` if they skipped the URL prompt.
- `extraction_date`: ISO date (e.g. `2026-05-04`).
- `extraction_status`: one of `success | no_url | fetch_failed | no_css | css_fetch_failed | insufficient_data | workspace_read_failed`. Still write the artefact even on non-success — the doc is complete (filled from domain defaults), the status records *why* the URL path didn't yield extracted values.
- `domain_source`: `curated` if `{{domain}}` matches a file in `framework/assets/domain-defaults/`, `free-text` otherwise.

---

## 4. Attribution Paragraph

The single blockquote line under the H1. Pick the variant per status:

| Condition | Attribution paragraph |
| --- | --- |
| `extraction_status = success`, `reference_url` set | `Tokens extracted from [{{reference_url}}]({{reference_url}}). Status colours and any unset tokens are filled from `framework/assets/domain-defaults/{{domain}}.md` (or per-run inference if {{domain_source}} is free-text).` |
| `reference_url` is null (consultant skipped) | `Tokens generated from `{{domain}}` defaults — no reference URL was provided.` |
| Any other non-success status (fetch_failed, no_css, css_fetch_failed, insufficient_data, workspace_read_failed) | `Tokens generated from `{{domain}}` defaults. URL extraction was attempted from {{reference_url}} but did not complete: {{extraction_status}}.` |

Always end the blockquote with the standing line from the template: *"Every token below carries a provenance marker — `extracted-from-url` if the value was found in the fetched CSS, `inferred-from-domain` if it came from the `{{domain}}` defaults. Review before proceeding."*

---

## 5. Provenance Tagging Rules

For every token in the doc:

- If the in-memory token came from step-05 (CSS extraction), tag it `extracted-from-url`. Source Context = the CSS selector or custom-property name the value came from.
- If the in-memory token came from step-05b (domain-defaults fill), tag it `inferred-from-domain`. Source Context = `domain-default ({{domain}})` if the domain is curated, `domain-inference ({{domain}})` if it is free-text.
- Never leave a Provenance cell empty. Never invent a third marker.
- For status colours (success/warning/error/info), the marker is **always** `inferred-from-domain` — they are not extracted by this agent under any condition.

---

## 6. Populate the Tables

### Extraction Summary > Colours (11 rows)

Format identical to the template. Hex values in `#RRGGBB` (uppercase hash, 6-digit). Source Context examples:
- `--brand-primary in :root` (CSS custom property)
- `.btn background-color` (class declaration)
- `body color` (element selector)
- `derived: primary hue +120°` (extraction derivation; still tag `extracted-from-url` because the seed came from CSS)
- `domain-default (retail-banking)` (curated fill)
- `domain-inference (legal services SaaS)` (free-text fill)

### Extraction Summary > Typography (15 rows)

One row per token: `heading-family`, `heading-weight`, `body-family`, `body-weight`, `text-xs..text-4xl`, `line-height-tight`, `line-height-base`, `line-height-loose`. Same Source Context conventions.

### Extraction Summary > Effects (7 rows)

One row per token: `shadow-sm`, `shadow-md`, `shadow-lg`, `transition-fast`, `transition-base`, `transition-slow`, `easing-standard`.

### Extraction Summary > Contrast Validation (4 rows + adjustments line)

- Ratios as `7.2:1` (one decimal place).
- Status: `Pass` if ratio ≥ 4.5, else `Fail` (should not happen after step-05's adjustment pass).
- Adjustments line: `none` if no adjustments were needed, else the comma-separated record `{token} adjusted from {original_hex} to {adjusted_hex} ({pair} contrast was {original_ratio}:1)`.

### Brand Colours (11 rows, machine-readable)

2-column table (`Token | Value`). Bare `#RRGGBB` hex, no backticks, no quotes.

### Brand Typography (three sub-tables)

- **Families:** `Heading | {{t_heading_family}} | {{t_heading_weight}}` and `Body | {{t_body_family}} | {{t_body_weight}}`.
- **Sizes:** 8 rows (`text-xs..text-4xl`).
- **Line Heights:** 3 rows.

### Brand Effects (two sub-tables)

- **Shadows:** 3 rows.
- **Motion:** 4 rows (durations + easing).

---

## 7. Write Discipline

- Output path: `design-system/design-system.md`.
- Create the `design-system/` directory first if it does not exist.
- Compute `sha256` of the rendered byte string before writing — this hash is passed to `framework/skills/verify-artifact-write.md` after the Write call.
- Never write the artefact incrementally. The render is built fully in memory, then written in one atomic Write call.
- Never edit a previously-written `design-system.md` in this step — overwrites are governed by the orchestrator's startup gate, not by step-06.
