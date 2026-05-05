---
name: step-05b-domain-inference
description: 'Infer every unset token from the consultant-provided domain string. Always runs — both after a successful URL extraction (to fill gaps) and after every URL-failure path (to fill the entire token set).'
# Variables referenced (inherited from agent):
# data_contrast_validation: 'framework/agents/design-system-styler/data/contrast-validation.md'
# domain_inference: 'framework/agents/design-system-styler/prompt-templates/domain-inference.md'
---

# Step 5b: Domain-Inference Fill + Contrast Validation

This step always runs. It fills every token still unset after step-05 (or the entire token set, if step-05 was skipped) by inferring values from the consultant's free-text `{{domain}}` string against the canonical token list defined in `framework/assets/template-design-system.md`. It then runs contrast validation across the final token set.

## A. Load the Inference Contract

Read `framework/agents/design-system-styler/prompt-templates/domain-inference.md`. That file defines the inference protocol: voice synthesis from `{{domain}}`, then per-section derivation rules (colours, typography, effects), coherence constraints, and the 33-token output contract. Hold the synthesised Voice in memory — it anchors every value produced in this step.

## B. Fill Loop

For every token in the canonical set (11 colours + 15 typography + 7 effects = 33 tokens):

1. If the token is already set in the in-memory extraction results from step-05, leave it alone. Its provenance remains `extracted-from-url` and its Source Context records the CSS selector or property where it was found.
2. If the token is unset (`null`), fill it by applying the inference rules from `domain-inference.md`:
   - Source Context = `domain-inference ({{domain}})`
   - Provenance = `inferred-from-domain`

After this loop, every token in the in-memory state has a non-null value, a non-empty Source Context, and a Provenance marker.

## C. Status Colours (Always Domain-Inferred)

The four status colours (`success`, `warning`, `error`, `info`) are always inferred from the domain — never extracted from the URL. Apply the same fill rules as in §B (per `domain-inference.md` §3.B.3); their Provenance is **always** `inferred-from-domain` regardless of the URL outcome.

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
- `{{voice}}` to the one-line Voice statement synthesised in §A. Step-07 prints it in the diagnostic summary.

The artefact is generated even on non-success status. The doc is always complete; the status records *why* the URL path didn't yield extracted values.

---

**Next:** Read fully and follow `step-06-artifact-generation.md`.
