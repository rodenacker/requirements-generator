---
name: step-05-brand-extraction
description: 'Orchestrate brand extraction by loading data files in sequence and applying extraction logic to {{primary_css_content}}.'
# Variables referenced (inherited from agent):
# prompt_brand_extraction: 'framework/agents/design-system-styler/prompt-templates/brand-extraction.md'
# data_color_rules: 'framework/agents/design-system-styler/data/color-extraction-rules.md'
# data_font_rules: 'framework/agents/design-system-styler/data/font-rules.md'
# data_typography_scale_rules: 'framework/agents/design-system-styler/data/typography-scale-rules.md'
# data_shadow_motion_rules: 'framework/agents/design-system-styler/data/shadow-motion-rules.md'
# data_contrast_validation: 'framework/agents/design-system-styler/data/contrast-validation.md'
# data_insufficient_handling: 'framework/agents/design-system-styler/data/insufficient-data-handling.md'
# workspace_path: 'design-system/.workspace'
---

# Step 5: Brand Extraction (URL-driven)

**Skip condition:** if step-04 set a non-success `{{extraction_status}}` (`fetch_failed`, `no_css`, `css_fetch_failed`), or step-02 set `{{extraction_status}} = "no_url"`, skip this step entirely and route to `step-05b-domain-fill.md`. Step 5b will fill every token from the domain defaults.

## Workspace Read

Read CSS content from disk (not from in-memory state of step-04):

1. Read `design-system/.workspace/css-content.txt` → store as `{{primary_css_content}}`.
2. Read `design-system/.workspace/metadata.json` → confirm `css_source_type`, `css_source_url`, `reference_url`.

**If workspace file read fails:**

- Log: "Workspace read failed — css-content.txt not found or unreadable".
- Set `{{extraction_status}} = "workspace_read_failed"`.
- Skip to `step-05b-domain-fill.md`.

## Extraction Orchestration

Load and apply data files in this exact sequence. Each file is read, its instructions applied to `{{primary_css_content}}`, then released before loading the next.

### 1. Load Extraction Overview

Read `framework/agents/design-system-styler/prompt-templates/brand-extraction.md` for:

- Extraction purpose and the data-file load order.
- Section 7 output format — the target structure for in-memory extraction results.

### 2. Insufficient-Data Check

Read `framework/agents/design-system-styler/data/insufficient-data-handling.md` and apply its threshold check:

- Count distinct non-white/non-black hex colors in `{{primary_css_content}}`.
- **If fewer than 3:** Set `{{extraction_status}} = "insufficient_data"`, log the diagnostic, and skip to `step-05b-domain-fill.md`. Do NOT halt.
- **If 3 or more:** Continue.

### 3. Colour Extraction (7 brand tokens)

Read `framework/agents/design-system-styler/data/color-extraction-rules.md` and apply:

- Section 1: CSS Analysis Strategy.
- Section 2: Colour Extraction (collect, normalize to `#RRGGBB`, deduplicate, rank).
- Section 3: Colour-to-Token Mapping for the 7 brand tokens (primary, secondary, accent, background, surface, text, text-muted) using heuristics and derivation fallbacks.

Status colours (`success`, `warning`, `error`, `info`) are NOT extracted here — they are always populated by step-05b.

Store: `{{extracted_colors}}` as the structure defined in `brand-extraction.md` Section 7. Tokens that could not be extracted remain `null`.

### 4. Typography — Families

Read `framework/agents/design-system-styler/data/font-rules.md` and apply Section 4 to extract `heading_family`, `heading_weight`, `body_family`, `body_weight`. Tokens that could not be extracted remain `null`.

### 5. Typography — Scale, Weights, Line-Heights

Read `framework/agents/design-system-styler/data/typography-scale-rules.md` and apply Sections A–C to extract:

- 8 size tokens (`size_xs` … `size_4xl`)
- font weights (already covered by Section 4 — re-confirm against the heading/body-weight heuristics if those weren't found)
- 3 line-height tokens (`lh_tight`, `lh_base`, `lh_loose`)

Apply the coverage threshold from Section A: if fewer than 3 of the 8 size tokens can be confidently extracted, leave **all 8** unset and let step-05b fill the entire size scale.

### 6. Effects — Shadows and Motion

Read `framework/agents/design-system-styler/data/shadow-motion-rules.md` and apply:

- Section E to extract `shadow_sm`, `shadow_md`, `shadow_lg`.
- Section F to extract `dur_fast`, `dur_base`, `dur_slow`, `easing_standard`.

All seven effects tokens are independent — fill what was found, leave the rest `null`.

### 7. Assemble In-Memory Extraction Results

Assemble the structured output per Section 7 format from `brand-extraction.md`:

- `{{extracted_colors}}` — 7 brand tokens (status colours not included)
- `{{extracted_typography}}` — 15 typography tokens
- `{{extracted_effects}}` — 7 effect tokens
- `{{extraction_status}} = "success"` (only if extraction completed without an early skip; otherwise the prior status is preserved)

Contrast validation runs **after** step-05b, not here — it must validate against the final token set, including any domain-default fills.

---

**Next:** Read fully and follow `step-05b-domain-fill.md`.
