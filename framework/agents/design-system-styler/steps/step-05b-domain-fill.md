---
name: step-05b-domain-fill
description: 'Fill every unset token from the domain defaults. Always runs — both after a successful URL extraction (to fill gaps) and after every URL-failure path (to fill the entire token set).'
# Variables referenced (inherited from agent):
# data_contrast_validation: 'framework/agents/design-system-styler/data/contrast-validation.md'
---

# Step 5b: Domain-Defaults Fill + Contrast Validation

This step always runs. It fills every token still unset after step-05 (or the entire token set, if step-05 was skipped) using `framework/assets/domain-defaults/{{domain}}.md` (curated path) or per-run inference (free-text path). It then runs contrast validation across the final token set.

## A. Determine the Fill Source

Branch on `{{domain_source}}`:

- **`curated`** — Read `framework/assets/domain-defaults/{{domain}}.md`. This file contains the canonical token set under headings matching the template's machine-readable Brand sections. Parse the three sections (Brand Colours, Brand Typography, Brand Effects) into in-memory lookup tables.
- **`free-text`** — Do not Read any `domain-defaults/*.md` file. Instead, infer a coherent token set per-run, against the same canonical token list defined in `framework/assets/template-design-system.md`. Use the consultant's free-text domain string as guidance. Cross-token coherence (e.g. shadow alpha matched to background lightness, body-weight matched to body-size) matters more than perfect domain accuracy.

## B. Fill Loop

For every token in the canonical set (11 colours + 15 typography + 7 effects = 33 tokens):

1. If the token is already set in the in-memory extraction results from step-05, leave it alone. Its provenance remains `extracted-from-url` and its Source Context records the CSS selector or property where it was found.
2. If the token is unset (`null`), fill it from the lookup table (curated path) or by inference (free-text path):
   - Curated: Source Context = `domain-default ({{domain}})`.
   - Free-text: Source Context = `domain-inference ({{domain}})`.
   - Provenance in either case = `inferred-from-domain`.

After this loop, every token in the in-memory state has a non-null value, a non-empty Source Context, and a Provenance marker.

## C. Status Colours (Always Domain-Filled)

The four status colours (`success`, `warning`, `error`, `info`) are always filled from the domain defaults — never extracted from the URL. Apply the same fill rules as in §B; their Provenance is **always** `inferred-from-domain` regardless of the URL outcome.

## D. Contrast Validation

Read `framework/agents/design-system-styler/data/contrast-validation.md` and apply Section 6 to the final token set:

1. Compute the four required contrast ratios (text/background, text/surface, text-muted/background, text-muted/surface).
2. If any ratio falls below 4.5:1, run the adjustment strategy from the rules file (darken text first; if text is already very dark, lighten background/surface).
3. Re-validate after every adjustment. Stop after 20 adjustment iterations per token; record any unmet pair as `Pass | Fail` accordingly.
4. Append every adjustment to `{{cv_adjustments}}` in the format:
    `{token} adjusted from {original_hex} to {adjusted_hex} ({pair} contrast was {original_ratio}:1)`

Adjusted tokens **retain their original provenance marker** — adjustment is a downstream correction, not a re-source.

## E. Bookkeeping for Step-06

Before advancing, set:

- `{{extraction_status}}` to `"success"` if and only if step-05 reached its happy path. Otherwise preserve the prior status (`no_url` / `fetch_failed` / `no_css` / `css_fetch_failed` / `insufficient_data` / `workspace_read_failed`).
- `{{extraction_date}}` to today's date in ISO 8601 (`YYYY-MM-DD`).
- `{{contrast_validation}}` to the four ratio/pass-fail rows + the adjustments record.

The artefact is generated even on non-success status. The doc is always complete; the status records *why* the URL path didn't yield extracted values.

---

**Next:** Read fully and follow `step-06-artifact-generation.md`.
