---
name: step-05-write-landing-and-sidecars
description: 'Write wireframes.html (variant landing), manifest.json (per-screen bindings accumulator), variant-position.json (immutable mirror of variants.json own-entry + self-authored strengths/weaknesses/use-when). Verify each.'
---

# Step 5: Write the landing and the two sidecars

## 5.1 Compose `wireframes.html` (variant landing)

Read the variant-landing template:

```
Read tool: framework/assets/wireframes/template-variant-landing.html
```

Token-substitute every slot:

- `{{SCOPE_SLUG}}` → `<scope_slug>`.
- `{{VARIANT_ID}}` → `<variant_id>`.
- `{{PERSONA_BINDING}}` → `own.persona_binding`.
- `{{DESIGN_PHILOSOPHY}}` → `own.design_philosophy`.
- `{{DIMENSION_POSITIONS_TABLE}}` → one `<tr><td>{dimension}</td><td>{position}</td></tr>` per dimension in `own.dimension_positions`.
- `{{SCREEN_LIST}}` → one `<li><a href="screen-NN-<slug>.html">S-NN — Intent</a></li>` per screen in inventory order.
- `{{STATE_MATRIX_TABLE}}` → one `<tr><td>S-NN</td><td>{pipe-separated states_rendered}</td></tr>` per screen, drawing from the in-memory `manifest.screens` accumulator.
- `{{CROSS_VARIANT_NAV}}` → one `<a href="../<OTHER-VARIANT-ID>/wireframes.html">{OTHER-VARIANT-ID}</a>` per other variant in `variants.json` (own-entry excluded). For the current variant, render a `<button aria-pressed="true">Current: {variant_id}</button>`.
- `{{SET_INDEX_HREF}}` → `"../index.html"`.
- `{{COMPARISON_HREF}}` → `"../comparison.html"`.

Compute sha256. Write to `<output_dir>/wireframes.html`. Verify via `framework/skills/verify-artifact-write.md` with `expected_min_bytes = 512`. On `pass`, advance.

## 5.2 Write `manifest.json`

Serialise the in-memory accumulator into the schema documented in `framework/agents/wireframe-variant-generator.md > Output`:

```json
{
  "scope_slug": "<scope_slug>",
  "variant_id": "<variant_id>",
  "authored_at": "<ISO-8601 UTC at this moment>",
  "blueprint_sha256": "<blueprint.sha256 captured at step 2.1>",
  "screens": { ... }
}
```

Compute sha256. Write to `<output_dir>/manifest.json` with two-space indentation. Verify with `expected_min_bytes = 256`.

On `pass`, capture `manifest_written = true` and advance.

## 5.3 Write `variant-position.json`

Compose the artefact per the schema in `framework/agents/wireframe-variant-generator.md > Output`. The `dimension_positions`, `persona_binding`, and `design_philosophy` fields are **immutable mirrors** of `own.*` (verbatim — drift here is a structural bug). The `strengths`, `weaknesses`, `tradeoffs`, `use_when` fields are **self-authored** by this sub-agent based on:

- The chosen pattern picks in `manifest.screens` (e.g. "table.compact" at density-+2 → strength: "18 fields visible without scroll").
- The bound persona's traits from `own.persona_traits` (e.g. daily-Importer → use_when: "Daily users, high volume; persona has used a similar product before").
- The dimension positions at the poles (e.g. power-simplicity: +2 → weakness: "Cognitive load high for first-time users").

Each field's content guidance:

- `strengths` — 3-5 bulleted strings; each names a concrete UX benefit attributable to the pattern picks + positions, not generic praise.
- `weaknesses` — 3-5 bulleted strings; each names a concrete UX cost, mirroring the strengths' tone.
- `tradeoffs` — one-line summary of the directional trade-off (e.g. "Expert-first; low learnability.", "Novice-first; low expert-efficiency.", "Audit-first; low workflow-speed.").
- `use_when` — one-line guidance on which persona / context this variant is the right pick for.

Compute sha256. Write to `<output_dir>/variant-position.json` with two-space indentation. Verify with `expected_min_bytes = 384`.

On `pass`, capture `variant_position_written = true` and advance.

---

**Next:** Read fully and follow `step-06-self-validate-and-handback.md`.
