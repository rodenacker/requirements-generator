---
name: step-05b-domain-inference
description: 'Classify the extracted colour scheme, infer every unset token from the domain, validate contrast, ask which colour mode(s) to ship, and derive the opposite mode when requested. Always runs — both after a successful URL extraction (to fill gaps) and after every URL-failure path (to fill the entire token set).'
# Variables referenced (inherited from agent):
# data_contrast_validation: 'framework/agents/design-system-styler/data/contrast-validation.md'
# data_cross_mode_derivation: 'framework/agents/design-system-styler/data/cross-mode-derivation-rules.md'
# domain_inference: 'framework/agents/design-system-styler/prompt-templates/domain-inference.md'
---

# Step 5b: Scheme Detection, Domain-Inference Fill, Mode Selection + Cross-Mode Derivation

This step always runs. It fills every token still unset after step-05 (or the entire token set, if step-05 was skipped) by inferring values from the consultant's free-text `{{domain}}` string against the canonical token list defined in `framework/assets/template-design-system.html` (the JSON SHAPE comment block at the top of the template enumerates all 33 token names). It then validates contrast, asks the consultant which colour mode(s) to ship, and derives the opposite mode if one is wanted.

**The governing rule for this step:** *the extracted scheme is the hue source; the other mode is derived from it.* Nothing here assumes light — a reference URL ships a dark palette as readily as a light one, and when it does, **light** is the derived mode.

## A. Load the Contracts

Read both in a single batched message — neither depends on the other:

- `framework/agents/design-system-styler/prompt-templates/domain-inference.md` — the inference protocol: voice synthesis from `{{domain}}`, then per-section derivation rules (colours, typography, effects), coherence constraints, and the 33-token output contract. Hold the synthesised Voice in memory — it anchors every value produced in this step.
- `framework/agents/design-system-styler/data/cross-mode-derivation-rules.md` — the bidirectional mode-derivation rules, used per-token in §B and for the whole set in §F.

## A-bis. Detect the Extracted Scheme

Before filling anything, classify what step-05 actually extracted. Apply the **Scheme Detection** rule in `framework/agents/design-system-styler/data/contrast-validation.md` (relative luminance of the `background` token; `>= 0.5` → `light`, `< 0.5` → `dark`). Do not restate the math — cite that subsection.

Set:

- `{{extracted_scheme}}` — `light` or `dark`.
  - If `background` was extracted, classify it as above.
  - If `{{reference_url}}` was null, or `{{extraction_status}}` is anything other than `"success"`, or `background` is unset → `light`. The domain-inference contract is light-anchored by construction, so an all-inferred set is a light set.
- `{{hue_source_mode}}` = `{{extracted_scheme}}`. This is the mode whose palette is grounded; it is the seed for any derivation and it will carry `meta.primary: true`.
- `{{hue_source}}` (the JSON `meta` field) — `extracted-light` | `extracted-dark` | `domain-inferred-light`:
  - `background` came from CSS and classified `light` → `extracted-light`
  - `background` came from CSS and classified `dark` → `extracted-dark`
  - no URL / non-success extraction → `domain-inferred-light`

Output one short Unicorn-voice line so the consultant can see what was found before being asked anything:

- extracted: *"Extracted palette is **`{{extracted_scheme}}`** (background `{{background_hex}}`). That's the hue source for this run."*
- inferred: *"No extracted palette — inferring a light set from `{{domain}}`."*

**Do not "normalise" a dark extraction toward light.** A dark result here is correct, not a defect.

## B. Fill Loop

For every token in the canonical set (11 colours + 15 typography + 7 effects = 33 tokens):

1. If the token is already set in the in-memory extraction results from step-05, leave it alone. Its provenance remains `extracted-from-url` and its Source Context records the CSS selector or property where it was found.
2. If the token is unset (`null`), fill it by applying the inference rules from `domain-inference.md`:
   - Source Context = `domain-inference ({{domain}})`
   - Provenance = `inferred-from-domain`

### B.1 Scheme-aware gap-fill (required when `{{extracted_scheme}} == "dark"`)

`domain-inference.md` produces **light** values by construction — it anchors `background` to `#FFFFFF`. Filling a gap in a **dark** extracted set straight from that contract would drop a near-white neutral into a dark palette, and the result would be incoherent (and would then be dragged around by contrast validation trying to rescue it).

So when `{{extracted_scheme}} == "dark"`, every value produced by step 2 above is passed through the **Light → dark** conversion in `cross-mode-derivation-rules.md` (§3) **one token at a time, before it is stored**:

- Store the converted (dark) value, not the inferred light one.
- Provenance stays `inferred-from-domain` — the token *is* domain-inferred.
- Source Context = `domain-inference ({{domain}}) → dark variant`

This keeps dark neutral targets defined in exactly one file. Do not copy dark neutral rules into the inference contract, and do not hand-pick dark values here.

Tokens that were **extracted** are never converted — they are already in the extracted scheme.

After this loop, every token in the in-memory state has a non-null value in `{{extracted_scheme}}`'s scheme, a non-empty Source Context, and a Provenance marker. This set is the **hue-source set**.

## C. Status Colours (Always Domain-Inferred)

The four status colours (`success`, `warning`, `error`, `info`) are always inferred from the domain — never extracted from the URL. Apply the same fill rules as in §B (per `domain-inference.md` §3.B.3), **including the §B.1 conversion when `{{extracted_scheme}} == "dark"`**; their Provenance is **always** `inferred-from-domain` regardless of the URL outcome.

On a dark set, check the status colours for the amber trap called out in the derivation rules (§3.3): a warning amber that has been darkened or over-desaturated muddies to brown. Status colours must stay legible against **both** the dark `background` and the dark `surface`.

## D. Contrast Validation (hue-source set)

Read `framework/agents/design-system-styler/data/contrast-validation.md` and apply Section 6 to the hue-source token set:

1. Compute the four required contrast ratios (text/background, text/surface, text-muted/background, text-muted/surface).
2. If any ratio falls below 4.5:1, run the adjustment strategy from the rules file **in `{{extracted_scheme}}`'s direction**:
   - `light` set → darken text first; if text is already very dark, lighten background/surface (never darken).
   - `dark` set → lighten text first (clamping at 255); if text is already very light, darken background/surface (never lighten).
3. Re-validate after every adjustment. Stop after 20 adjustment iterations per token; record any unmet pair as `Pass | Fail` accordingly.
4. Append every adjustment to the **hue-source mode's** adjustments variable — `{{cv_adjustments_light}}` if `{{extracted_scheme}} == "light"`, else `{{cv_adjustments_dark}}` — in the format:
    `{token} adjusted from {original_hex} to {adjusted_hex} ({pair} contrast was {original_ratio}:1)`
5. Set that mode's `{{cv_pass_count_<mode>}}` and `{{cv_adjustment_count_<mode>}}`.

Adjusted tokens **retain their original provenance marker** — adjustment is a downstream correction, not a re-source.

The per-mode variable names are keyed by **mode**, not by source/derived role: `_light` always means the light set, whichever mode happened to be extracted.

## E. Choose Output Modes

The hue-source set is now final. Ask the consultant which mode(s) to ship — this is the one place `{{mode_choice}}` is set.

Use `AskUserQuestion`:

- Header: `Modes`
- multiSelect: false
- Question — pick the phrasing that matches the run:
  - **Extraction produced a palette** (`{{hue_source}}` is `extracted-light` or `extracted-dark`): *"`{{reference_url}}`'s palette is **{{extracted_scheme}}**. Which colour mode(s) should the design system ship in? The {{extracted_scheme}} palette is the hue source — the other mode is derived from the same brand hues, not extracted separately."*
  - **No extracted palette** (`{{hue_source}}` is `domain-inferred-light`): *"Every token was inferred from `{{domain}}` as a light palette. Which colour mode(s) should the design system ship in? A dark palette would be derived from the same brand hues."*
- Options — **list the extracted scheme first and mark it Recommended**, since it is the grounded one:
  1. `{{extracted_scheme}} only` *(Recommended)* — ship just the grounded palette.
  2. `{{other_mode}} only` — ship the derived palette. *(Note in the option description that the {{extracted_scheme}} file is still written, as the grounded record.)*
  3. `Both` — ship both; the {{extracted_scheme}} file is primary.

Resolve the answer:

- Consultant picked an option → set `{{mode_choice}}` to `light-only`, `dark-only`, or `both` accordingly. (Option 1 maps to `<extracted_scheme>-only`; option 2 to `<other_mode>-only`.)
- Consultant typed `Other` free-text → coerce it to the nearest of the three (e.g. "just dark" → `dark-only`, "light + dark" → `both`). If it cannot be read as one of the three, re-ask **once**; if still unclear, default to `{{extracted_scheme}}-only` and say so.

Then derive:

- `{{derived_mode_requested}}` — true iff `{{mode_choice}}` names a mode other than `{{hue_source_mode}}` (i.e. `both`, or `<other_mode>-only`).
- `{{primary_mode}}` = `{{hue_source_mode}}`. **Always.** The grounded palette is the primary one regardless of what was asked for.
- `{{files_to_write}}` = the mode(s) named by `{{mode_choice}}` **∪ `{{hue_source_mode}}`**. The hue-source file is always written — it is the record of what was actually extracted, and it is produced anyway as the derivation seed.

**Echo the resolved file list, and be explicit when it exceeds the request:**

- One file: *"Writing `design-system/design-system-{{mode}}.html`."*
- Two files, both asked for: *"Writing both files — `{{hue_source_mode}}` is primary (the extracted palette); `{{other_mode}}` is derived from the same hues."*
- Two files, only one asked for: *"Writing `design-system/design-system-{{requested}}.html` as asked, **plus** `design-system/design-system-{{hue_source_mode}}.html` — the `{{hue_source_mode}}` palette is what the URL actually shipped, so it's kept as the grounded record and marked primary."*

Never let the second file appear unannounced; a consultant who asked for one file and finds two must be told why.

Note for reference: step-07's **Restart** re-enters `step-02-inputs.md`, so extraction runs again and this question is re-asked. The mode choice is not sticky across a restart.

## F. Cross-Mode Derivation

**Runs if and only if `{{derived_mode_requested}}`.** Skip entirely otherwise.

Using `cross-mode-derivation-rules.md` — §3 if deriving dark from light, §4 if deriving light from dark:

1. Derive the derived mode's **11 colours** and **3 shadows** from the *contrast-validated* hue-source set (the output of §D, not the pre-validation values).
2. Copy the **19 shared tokens** verbatim — all 15 typography tokens plus `transition_fast`, `transition_base`, `transition_slow`, `easing_standard`. Same values, same `prov`, same `source`. Do not re-derive or re-round them.
3. Tag every derived colour and shadow: `prov: "inferred-from-domain"`, `source: "derived: <target-mode> variant of <source-mode> <token> (<source-hex>)"`. Two markers only — there is no third.
4. Run contrast validation over the derived set **in the derived mode's direction** (§D's procedure, opposite branch). Write results into that mode's `{{cv_pass_count_<mode>}}` / `{{cv_adjustments_<mode>}}` / `{{cv_adjustment_count_<mode>}}`. The derived set gets its **own** four ratios — it never inherits the hue-source set's numbers.
5. Check the derived status colours for legibility against the derived `background` **and** `surface`, and honour the **fill-legibility constraint** (rules file §5.6): brand and status fills must stay far enough in lightness from the derived `surface` that the catalogue's on-fill label text reads against them. This is derivation guidance, not an additional validation gate — the gate remains the four pairs.

Store the derived set as a separate in-memory token set. Both sets now exist and step-06 renders one file from each.

## G. Bookkeeping for Step-06

Before advancing, set:

- `{{extraction_status}}` to `"success"` if and only if step-05 reached its happy path. Otherwise preserve the prior status (`no_url` / `fetch_failed` / `no_css` / `css_fetch_failed` / `insufficient_data` / `workspace_read_failed`).
- `{{extraction_date}}` to today's date in ISO 8601 (`YYYY-MM-DD`).
- `{{voice}}` to the one-line Voice statement synthesised in §A. Step-07 prints it in the diagnostic summary.
- **Mode state:** `{{extracted_scheme}}`, `{{hue_source_mode}}`, `{{hue_source}}`, `{{mode_choice}}`, `{{derived_mode_requested}}`, `{{primary_mode}}`, `{{files_to_write}}`.
- **Per-mode contrast:** `{{cv_pass_count_light}}` / `{{cv_adjustments_light}}` / `{{cv_adjustment_count_light}}` and the `_dark` twins. Exactly one set is populated when a single file is written; both are populated when two are.

Confirm before advancing:

- Every token in the hue-source set has a non-null value, a Source Context, and one of the two provenance markers.
- If `{{derived_mode_requested}}`, the derived set likewise has all 33 tokens, with its 11 colours + 3 shadows carrying `derived: …` source strings and its 19 shared tokens carrying the hue-source markers.
- `{{files_to_write}}` contains `{{hue_source_mode}}`, and `{{primary_mode}} == {{hue_source_mode}}`.

The artefact is generated even on non-success status. The doc is always complete; the status records *why* the URL path didn't yield extracted values.

---

**Next:** Read fully and follow `step-06-artifact-generation.md`.
