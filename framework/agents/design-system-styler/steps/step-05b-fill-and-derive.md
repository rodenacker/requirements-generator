---
name: step-05b-fill-and-derive
description: 'Classify the references'' colour scheme, fill the house defaults and the interim font fallback, assign every colour through the helper, validate contrast, ask which colour mode(s) to ship, and derive the opposite mode when requested. Always runs after step-05''s reference gate passes.'
# Variables referenced (inherited from agent):
# data_contrast_validation: 'framework/agents/design-system-styler/data/contrast-validation.md'
# data_cross_mode_derivation: 'framework/agents/design-system-styler/data/cross-mode-derivation-rules.md'
# data_house_defaults: 'framework/agents/design-system-styler/data/house-defaults.md'
---

# Step 5b: Scheme Detection, House-Default Fill, Mode Selection + Cross-Mode Derivation

This step always runs. It completes the canonical token list defined in `framework/assets/template-design-system.html` (the JSON SHAPE comment block at the top of the template enumerates all 34 token names): sizes, line heights, shadows and motion from the fixed house defaults, unextracted fonts from the interim fallback, and every colour from the helper (`framework/tools/colour-tokens.cjs`). Nothing is inferred. It then validates contrast, asks the consultant which colour mode(s) to ship, and derives the opposite mode if one is wanted.

**The governing rule for this step:** *the extracted scheme is the hue source; the other mode is derived from it.* Nothing here assumes light — a reference URL ships a dark palette as readily as a light one, and when it does, **light** is the derived mode.

## A. Load the Contracts

Read both in a single batched message — neither depends on the other:

- `framework/agents/design-system-styler/data/house-defaults.md` — the fixed house values for sizes, line heights, shadows and motion, and the interim font fallback. Used in §B.
- `framework/agents/design-system-styler/data/cross-mode-derivation-rules.md` — the bidirectional mode-derivation rules (dark-shadow treatment in §B, the whole set in §F).

## A-bis. Detect the Extracted Scheme

Before filling anything, classify the merged `background` step-05 §7 wrote into `assign-in.json` → `neutrals.background` (the first PDF that declares a background, else the lead URL's). Apply the **Scheme Detection** rule in `framework/agents/design-system-styler/data/contrast-validation.md` (relative luminance of the `background` token; `>= 0.5` → `light`, `< 0.5` → `dark`). Do not restate the math — cite that subsection.

Set:

- `{{extracted_scheme}}` — `light` or `dark`.
  - If `background` is non-null, classify it as above.
  - If no reference gave a `background` → `light`. This is a default for missing evidence, **not** "light is authoritative": an extracted dark `background` still makes dark the hue source.
- `{{hue_source_mode}}` = `{{extracted_scheme}}`. This is the mode whose palette is grounded; it is the seed for any derivation and it will carry `meta.primary: true`.
- `{{hue_source}}` (the JSON `meta` field) — `extracted-light` | `extracted-dark` | `extracted-both` | `declared-light` (`extracted-both` is set by §A-bis.1 when the site ships its own other scheme):
  - `background` given and classified `light` → `extracted-light`
  - `background` given and classified `dark` → `extracted-dark`
  - no `background` in any reference → `declared-light`

Output one short Unicorn-voice line so the consultant can see what was found before being asked anything:

- extracted: *"Extracted palette is **`{{extracted_scheme}}`** (background `{{background_hex}}`). That's the hue source for this run."*
- declared-light: *"No background colour in the references; the light palette is the hue source."*

**Do not "normalise" a dark extraction toward light.** A dark result here is correct, not a defect.

### A-bis.1 The site's own other scheme

If step-04 captured `{{alt_scheme}}` (non-null, Playwright path only) and its `scheme` is the opposite of `{{extracted_scheme}}`, apply the `color-extraction-rules.md` §0/§1/§3 pick heuristics to `{{alt_scheme}}.customProperties` and `.declarations` to pick that scheme's `background`, `surface`, `text`, `text_muted`, `primary`, `secondary`, `accent`. If **at least `background` and `text`** resolve:

- `{{other_mode_extracted}} = true` and `{{hue_source}} = extracted-both`. The other mode is **extracted, not derived**: its tokens carry `prov: extracted` with the alt-scheme selector / property as Source Context.
- Its picks go through the helper in §C (reserved zones apply in both modes), with `brand` forced to the hue-source `brand`.
- Say so in the scheme line: *"The site also ships its own **{{other_mode}}** palette — extracting it instead of deriving."*

Otherwise `{{other_mode_extracted}} = false` and the other mode, if requested, is derived in §F.

## B. Fill Loop

Fill every non-colour token. Colours (all 12, neutrals included) are §C's: the helper owns them.

1. **Sizes, line heights, shadows, motion** (8 + 3 + 3 + 4 = 18 tokens): **always** from `house-defaults.md` §1–§3, never from extraction. `prov: system-derived`, `source: "house default"`. Shadows take `<text-rgb>` from the hue-source `text` colour, which §C settles: fill the shadows after §C step 4 (on a dark hue-source set, apply `house-defaults.md` §2's dark treatment).
2. **Font families and weights** already set by step-05: leave them alone. Their provenance stays `extracted`, with the selector or page as Source Context.
3. **Font families and weights not extracted:** the interim fallback, `house-defaults.md` §4. `prov: system-derived`, `source: "interim font fallback"`.

### B.2 Availability of a fallback family

A `heading_family` or `body_family` filled from the interim fallback is **`google-native` by construction**: `Inter` is in `font-availability-rules.md` §4.1, the verified Google-hosted list. So:

- Set `{{font_availability_<slot>}}` to the availability record in `house-defaults.md` §4.
- **Do not run the evidence ladder and do not probe.** Never re-probe a fallback family: there is nothing to establish; the value came from the verified list.

An **extracted** family keeps whatever record step-05 §4b already produced, including a `substituted` or `unverified` three-name value. This loop never rewrites it. Every family, fallback or extracted, gets its `delivery` in §G.

## C. Brand Roles and Status Colours (house set) — via the helper

**Ordering (fixed):** step-05 §7 wrote `generated-docs/design-system/.workspace/assign-in.json` with the merged candidates, picks and neutrals (it raised `RF-14` instead when no reference was usable, so the file always exists here); this section runs the helper. Nothing else assigns `primary`, `secondary`, `accent`, `brand` or the status colours.

1. **No `assign-in.json`** → raise `RF-14` (step-05 §7's reference gate was skipped; this is a backstop, not a second path).
2. Read `assign-in.json`, set `mode` to `{{hue_source_mode}}` (§A-bis), and Write it back. Leave `neutrals` as step-05 wrote them: a `null` neutral is filled by the helper from its neutral ladder.
3. Run, via Bash:
   ```
   node framework/tools/colour-tokens.cjs assign --in generated-docs/design-system/.workspace/assign-in.json --out generated-docs/design-system/.workspace/assign-out.json
   ```
   Exit code ≠ 0 → **halt** and show the helper's one-line stderr message. Never fall back to prose colour rules.
4. Read `assign-out.json` and set:
   - `{{brand}}` = `brand`; `{{roles}}` = `roles` (the single palette, or Option 1 when options exist); `{{palette_options}}` = `options` (or `null`); `{{assign_decisions}}` = `decisions`; the four status colours = `status`; and the four neutrals = `neutrals`. A neutral named in `filled` → `prov: system-derived`, `source: "neutral ladder"`; the others keep their extracted provenance.
   - Provenance: `brand`, and every role whose hex is an extracted candidate or pick → `extracted` (Source Context: the reference from step-05 §7's `{{merged_sources}}` — `<url> <selector>`, `<file>.pdf p.N: "<as written>"`, or `<lead url> area-weighted capture` for an area-picked `brand`). A role the helper filled with a **brand-tinted neutral** → `system-derived` (Source Context: `cascade fallback — <the matching decisions line>`), and all four status colours → `system-derived` (Source Context: `HOUSE_STATUS`). Two markers only.

5. **Other mode extracted** (`{{other_mode_extracted}}`): write `assign-in-<other_mode>.json` with the same `candidates`, the §A-bis.1 picks, that scheme's four neutrals (`null` for an unpicked one: the helper's ladder fills it), `"mode": "<other_mode>"`, and `picks.brand` = `{{brand}}`; run `assign` on it (→ `assign-out-<other_mode>.json`). Its `roles` and `status` are the other mode's; its `brand` equals `{{brand}}` by construction. When `{{palette_options}}` is non-null, the other mode's two option sets are this call's `options` if non-null; otherwise each option's other-mode roles come from that option's §F `derive`.

The status colours are the helper's fixed house set (`HOUSE_STATUS` in `framework/tools/colour-tokens.cjs`) — never extracted. On a reserved (red / orange / amber) brand the helper moves `error` away from the brand hue, and on a dark hue-source surface it moves status lightness only as far as the fill contrast target needs. Do not restate or re-tune those numbers here.

## D. Contrast Validation (hue-source set)

The numbers come from the helper; `framework/agents/design-system-styler/data/contrast-validation.md` states what is checked (the four text pairs, fills, labels). Do not compute ratios or adjust colours by hand.

1. For each palette — `default` when `{{palette_options}}` is null, else `neutral` and `site_colour` (the option's `primary` / `secondary` / `accent`; everything else shared) — write `generated-docs/design-system/.workspace/measure-<palette>-<hue_source_mode>-in.json` = `{ "mode": "{{hue_source_mode}}", "colours": { <12 colours incl. brand> } }` and run:
   ```
   node framework/tools/colour-tokens.cjs measure --in generated-docs/design-system/.workspace/measure-<palette>-<hue_source_mode>-in.json --out generated-docs/design-system/.workspace/measure-<palette>-<hue_source_mode>-out.json
   ```
   Exit code ≠ 0 → halt with the stderr line.
2. Take `colours` from the output (the helper adjusts only `text` / `text_muted`, lightness only, in the scheme's direction; extracted fills are reported, never moved) and store the result as `{{palettes}}.<palette>.<hue_source_mode>` = `{ colours, on_colours, contrast, fills, adjustments }`.
3. Set the hue-source mode's `{{on_colours_<mode>}}` (the `default` / `neutral` palette's), `{{cv_adjustments_<mode>}}` = the helper's `adjustments` lines, `{{cv_pass_count_<mode>}}` = how many of the four `contrast` pairs are ≥ 4.5, and `{{cv_adjustment_count_<mode>}}` = how many `adjustments` lines start with `text` / `text_muted` and say "adjusted".
4. **Other mode extracted** (`{{other_mode_extracted}}`): run `measure` the same way over the other mode's extracted set (per palette) and store it under `{{palettes}}.<palette>.<other_mode>`. That set is not derived in §F.

Adjusted tokens **retain their original provenance marker** — adjustment is a downstream correction, not a re-source.

The per-mode variable names are keyed by **mode**, not by source/derived role: `_light` always means the light set, whichever mode happened to be extracted.

## E. Choose Output Modes

The hue-source set is now final. Ask the consultant which mode(s) to ship — this is the one place `{{mode_choice}}` is set.

Use `AskUserQuestion`:

- Header: `Modes`
- multiSelect: false
- Question — pick the phrasing that matches the run:
  - **A reference gave a background** (`{{hue_source}}` is `extracted-light` or `extracted-dark`): *"The references' palette is **{{extracted_scheme}}**. Which colour mode(s) should the design system ship in? The {{extracted_scheme}} palette is the hue source — the other mode is derived from the same brand hues, not extracted separately."* (When `{{hue_source}}` is `extracted-both`, replace that last sentence with: *"The site ships its own {{other_mode}} palette too, so that mode is extracted, not derived."*)
  - **No reference declared a background** (`{{hue_source}}` is `declared-light`): *"No reference declared a background, so the light palette is the hue source. Which colour mode(s) should the design system ship in? A dark palette would be derived from the same brand hues."*
- Options — **list `Both` first and mark it Recommended**. Both is the default because a design system that ships only one mode leaves every downstream consumer (`/prototype`'s scaffold in particular) with no palette for the other mode, and the derived set costs nothing beyond §F. The single-mode options follow, extracted scheme before derived, since the extracted one is the grounded palette:
  1. `Both` *(Recommended)* — ship both files. The {{extracted_scheme}} file is primary (the palette actually extracted); the {{other_mode}} file is derived from the same brand hues.
  2. `{{extracted_scheme}} only` — ship just the grounded palette.
  3. `{{other_mode}} only` — ship the derived palette. *(Note in the option description that the {{extracted_scheme}} file is still written, as the grounded record.)*

Resolve the answer:

- Consultant picked an option → set `{{mode_choice}}` to `both`, `light-only`, or `dark-only` accordingly. (Option 1 maps to `both`; option 2 to `<extracted_scheme>-only`; option 3 to `<other_mode>-only`.)
- Consultant typed `Other` free-text → coerce it to the nearest of the three (e.g. "just dark" → `dark-only`, "light + dark" → `both`). If it cannot be read as one of the three, re-ask **once**; if still unclear, default to `both` — the recommended option — and say so.

Then derive:

- `{{derived_mode_requested}}` — true iff `{{mode_choice}}` names a mode other than `{{hue_source_mode}}` (i.e. `both`, or `<other_mode>-only`).
- `{{primary_mode}}` = `{{hue_source_mode}}`. **Always.** The grounded palette is the primary one regardless of what was asked for.
- `{{files_to_write}}` = the mode(s) named by `{{mode_choice}}` **∪ `{{hue_source_mode}}`**. The hue-source file is always written — it is the record of what was actually extracted, and it is produced anyway as the derivation seed.

**Echo the resolved file list, and be explicit when it exceeds the request:**

- One file: *"Writing `generated-docs/design-system/design-system-{{mode}}.html`."*
- Two files, both asked for: *"Writing both files — `{{hue_source_mode}}` is primary (the extracted palette); `{{other_mode}}` is derived from the same hues."*
- Two files, only one asked for: *"Writing `generated-docs/design-system/design-system-{{requested}}.html` as asked, **plus** `generated-docs/design-system/design-system-{{hue_source_mode}}.html` — the `{{hue_source_mode}}` palette is what the URL actually shipped, so it's kept as the grounded record and marked primary."*

Never let the second file appear unannounced; a consultant who asked for one file and finds two must be told why.

Note for reference: step-07's **Restart** re-enters `step-02-inputs.md`, so extraction runs again and this question is re-asked. The mode choice is not sticky across a restart.

## F. Cross-Mode Derivation

**Runs if and only if `{{derived_mode_requested}}` and not `{{other_mode_extracted}}`** (an extracted other mode was already measured in §D step 4). Skip entirely otherwise.

The policy is `cross-mode-derivation-rules.md` §3–§5; the numbers come from the helper:

1. For each palette in `{{palettes}}` (`default`, or `neutral` and `site_colour`), write `generated-docs/design-system/.workspace/derive-<palette>-in.json` = `{ "source_mode": "{{hue_source_mode}}", "colours": <that palette's contrast-validated hue-source colours from §D> }` and run:
   ```
   node framework/tools/colour-tokens.cjs derive --in generated-docs/design-system/.workspace/derive-<palette>-in.json --out generated-docs/design-system/.workspace/derive-<palette>-out.json
   ```
   Exit code ≠ 0 → halt with the stderr line. Store the output as `{{palettes}}.<palette>.<other_mode>` = `{ colours, on_colours, contrast, fills, adjustments }`. The derived set's **12 colours** are exactly the helper's — do not retune them.
2. Derive the **3 shadows** per `cross-mode-derivation-rules.md` §3.4 / §4.4 (geometry verbatim, alpha scaled).
3. Copy the **19 shared tokens** verbatim — all 15 typography tokens plus `transition_fast`, `transition_base`, `transition_slow`, `easing_standard`. Same values, same `prov`, same `source`. Do not re-derive or re-round them.
4. Tag every derived colour and shadow: `prov: "system-derived"`, `source: "derived: <target-mode> variant of <source-mode> <token> (<source-hex>)"` — except `brand`, which is mode-invariant and copied with its hue-source `prov` / `source`. Two markers only — there is no third.
5. Set the derived mode's `{{on_colours_<mode>}}`, `{{cv_adjustments_<mode>}}` (the helper's `adjustments` lines), `{{cv_pass_count_<mode>}}` (pairs ≥ 4.5) and `{{cv_adjustment_count_<mode>}}` (lines describing a moved or flipped colour) from the `default` / `neutral` palette's output. The derived set gets its **own** numbers — it never inherits the hue-source set's.

Store the derived set as a separate in-memory token set. Both sets now exist and step-06 renders one file from each.

## G. Bookkeeping for Step-06

Before advancing, set:

- `{{extraction_status}}` to `"success"` if and only if step-05 reached its happy path. Otherwise preserve the prior status (`no_url` / `fetch_failed` / `no_css` / `css_fetch_failed` / `insufficient_data` / `workspace_read_failed`).
- `{{extraction_date}}` to today's date in ISO 8601 (`YYYY-MM-DD`).
- **Mode state:** `{{extracted_scheme}}`, `{{hue_source_mode}}`, `{{hue_source}}` (`extracted-light` | `extracted-dark` | `extracted-both` | `declared-light`), `{{other_mode_extracted}}`, `{{mode_choice}}`, `{{derived_mode_requested}}`, `{{primary_mode}}`, `{{files_to_write}}`.
- **Colour state (from the helper):** `{{brand}}`, `{{palette_options}}`, `{{assign_decisions}}`, and `{{palettes}}` — `{ <palette>: { <mode>: { colours, on_colours, contrast, fills, adjustments } } }`, palette `default` (no options) or `neutral` + `site_colour`. Step-06 renders from `{{palettes}}`.
- **Per-mode contrast:** `{{cv_pass_count_light}}` / `{{cv_adjustments_light}}` / `{{cv_adjustment_count_light}}` and the `_dark` twins. Exactly one set is populated when a single file is written; both are populated when two are.
- **Embed the faces** (`font-availability-rules.md` §6.4). Before assembling `{{brand_fonts}}`, run once over the distinct `param`s of the two availability records:

  ```
  node framework/tools/font-embed.cjs embed --params "<distinct params, comma-separated>" --out generated-docs/design-system/.workspace/font-faces.css
  ```

  Keep its report as `{{font_embed_report}}` (`{ embedded, failed, bytes }`). A non-zero exit is not a halt: treat every family as `failed` with reason `network` and continue. The CSS file is what step-06 injects; never open it or copy from it.
- **`{{brand_fonts}}`** — assemble the `meta.brand_fonts` object in the shape `font-availability-rules.md` §6.2 specifies, from `{{font_availability_heading}}` and `{{font_availability_body}}` (set by step-05 §4b for extracted families, by §B.2 above for fallback ones) and `{{font_embed_report}}`:
  - `families` — exactly two entries, `role: "heading"` first then `role: "body"`, even when both resolve to the same face. Each gets `delivery: "embedded"` when its `param` is in the report's `embedded`, else `delivery: "link"`.
  - `links` — one URL per **distinct** `param` whose `delivery` is `"link"`, built per §6.3 (`?family=<param>:wght@400;500;600;700&display=swap`, one family per link, never combined). Deduped when heading and body share a face; `[]` when every family is embedded.
  - `embedded_bytes` — the report's `bytes` (`0` when nothing was embedded).
  - Typography is mode-invariant, so `{{brand_fonts}}` is a single object written **identically into both mode files** — do not derive a per-mode variant.

Confirm before advancing:

- Every token in the hue-source set has a non-null value, a Source Context, and one of the two provenance markers.
- If `{{derived_mode_requested}}`, the other-mode set likewise has all 34 tokens; when it was derived (not `extracted-both`), its colours other than `brand` and its 3 shadows carry `derived: …` source strings and its 19 shared tokens carrying the hue-source markers.
- `{{files_to_write}}` contains `{{hue_source_mode}}`, and `{{primary_mode}} == {{hue_source_mode}}`.
- `{{brand_fonts}}.families` has two entries with `status` in `google-native | substituted | unverified` and `delivery` in `embedded | link`; every `param` is non-null and is in `font-availability-rules.md` §4.1 or was verified this run (E1 / E3, per §4.1's cache note); each `substituted` or `unverified` entry's token value carries `brand` then `loadable` in that order; `links` holds exactly the `link`-delivery params.

The artefact is generated even on non-success status. The doc is always complete; the status records *why* the URL path didn't yield extracted values.

---

**Next:** Read fully and follow `step-06-artifact-generation.md`.
