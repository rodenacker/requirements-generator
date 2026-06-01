---
name: step-02-read-inputs
description: 'Read the blueprint surface inventory, the variants.json own entry (incl. the authored surface_plan), the templates, the catalogue index, and the position-vocabulary. The generator renders the authored surface_plan — it no longer reads the trade-off-dimensions registry or pattern-bindings to derive patterns.'
---

# Step 2: Read inputs

## 2.1 Read the blueprint surface inventory

```
Read tool: <blueprint_path>
```

Compute the sha256 of the bytes read; capture into in-memory `blueprint.sha256` for later cross-validation. Parse:

- The `## Sources` section's comma-separated source list (for cross-reference at self-validation).
- The `## Available personas` bulleted list.
- The `## Surface inventory` table — this is now a **logical surface inventory** keyed by `LS-NN` (decomposition-agnostic), not a physical screen inventory. For every row, capture `{ surface_id: "LS-NN", intent: "<text>", sources: ["<id1>", ...], properties: ["<Shape.Field|F-NN:ParamName>", ...], allowed_realizations: ["standalone-screen", ...], default_realization: "<one member>", host_surface: "LS-NN or —", secondary_intent: "<text or null>" }` into in-memory `surfaces[]` (preserving inventory order). The `properties` array is the comma-split, trimmed Properties cell; if the cell value is the literal `none`, `properties` is the empty array `[]` (pure UI surface, no entity bindings). The variant-generator treats `properties` as the **closed set** of object-properties allowed in `data-prop` attributes wherever this surface is rendered (its own standalone screen, its wizard-split sub-screens, or — for folds — the host screen's drawer/modal sub-tree).
- The `## Logical flow` section's flow notation (over `LS-NN` surfaces; used together with the variant's `physical_flow` for composing cross-screen prev/next nav).

The blueprint no longer dictates how many physical screens a surface becomes — that is the variant's authored `realization` per surface (read at 2.2 / built at 2.6). The blueprint is the **convergence** layer (logical surfaces + per-surface closed property set + the set of *allowed* realizations); the variant's `surface_plan` is the **divergence** layer that this generator renders.

Set `M = surfaces.length`. (`M` is the count of *logical surfaces*, not the count of physical screen files — those are derived at 2.6 and depend on each surface's realization.) Output one short line: *"Variant {{variant_id}} ready. Rendering surface_plan over {{M}} logical surfaces for scope `{{scope_slug}}`."* (matches the placeholder from step 1's announcement.)

## 2.2 Read the variants.json own-entry

```
Read tool: <variants_path>
```

JSON-parse. Locate the entry where `variants[i].variant_id == <variant_id>`. **Read only that own entry for composition; the sibling entries are read at 4.5 for cross-variant nav (metadata only — their `surface_plan` realization map).** Capture into in-memory:

- `own.variant_id`
- `own.persona_binding`
- `own.posture` + `own.posture_label` (the variant's UX posture id `P1`..`P6` + label, or both `null`) — metadata mirrored into `variant-position.json`; the posture's structural influence is already baked into `own.surface_plan` by the architect, so this generator does **not** re-apply it (render-the-plan contract).
- `own.design_philosophy`
- `own.dimension_positions` (all six canonical dimensions)
- `own.surface_plan` — the architect's authored per-surface composition + realization plan, keyed by `LS-NN`. This is the **single source of truth** for this variant's pattern picks and information-architecture realizations. Per-surface shape (`realization`, `host_surface`/`rendered_on`/`host_state`, `physical_screens[]`, `covers_properties`, `primary_pattern`, `primary_pattern_variant`, `base_pattern_owner`, `modifiers[]`, `secondary_patterns[]`, `states_rendered[]`) is defined canonically in `framework/assets/wireframes/realization-strategies.md > Section 2`. Capture verbatim — the generator renders it, it does not re-derive it.
- `own.physical_flow` — the variant's concrete physical screen flow (arrow notation, e.g. `S-01 → S-02 → S-04; S-01 ⟳ drawer(LS-03)`), used at 4.5 for cross-screen prev/next nav alongside the blueprint's logical flow.
- `own.persona_traits` — derived from the persona binding text by the same heuristic used in `framework/agents/blueprint-architect/steps/step-02-read-inputs.md > 2.4` (frequency, expertise, role).

Cross-check `variants.json > blueprint_sha256` against `blueprint.sha256` from step 2.1. Mismatch indicates the blueprint was edited between the architect's run and Stage 3 dispatch — return `failed` with structured plain-text *"Blueprint sha256 drift: variants.json declares <hash1>, blueprint.md is <hash2>. Re-run architect first."*. Do not proceed.

## 2.3 Read the screen template

```
Read tool: framework/assets/templates/template-screen.html
```

Capture into in-memory `template_screen` (reused for every screen render at step 4).

## 2.4 Read the position-vocabulary (for the plain-English tagline)

```
Read tool: framework/assets/wireframes/position-vocabulary.md
```

Capture the `(dimension, position) → short label` map; this is the lookup table for the chrome header's plain-English `{{POSITION_TAGLINE}}` at step 4.5b.

> **Pattern + realization selection moved to the architect.** This generator no longer reads `framework/assets/wireframes/tradeoff-dimensions-registry.md` or `framework/assets/wireframes/pattern-bindings.md`, because it no longer **derives** patterns from dimension positions. The architect authored every pattern pick, every `primary_pattern_variant`, every modifier, and every per-surface realization into `own.surface_plan` (read at 2.2). The generator's job is to **render the authored plan**, not to re-pick from the registry. The only remaining wireframes-asset read is `position-vocabulary.md` (above), needed purely for the consultant-facing tagline.

## 2.5 Read the catalogue index

```
Read tool: framework/assets/pattern-catalogue/_index.md
```

Capture the full list of `{ id, category, tier, file_path }` rows. This is still needed — but now only to (a) **validate** that every pattern ID the architect authored into `own.surface_plan` is a real catalogue ID, and (b) look up the file path for the selective per-pattern reads at step 4. It is **not** used to pick patterns (the architect already picked).

## 2.6 Build the per-physical-screen render plan from the authored `surface_plan`

The generator does **not** derive patterns. It enumerates the physical screens implied by `own.surface_plan` and renders each one against the authored pattern fields. Per `framework/assets/wireframes/realization-strategies.md > Section 1`:

- **`standalone-screen`** — the surface contributes its **1** `physical_screens[]` element (an own file). The pattern fields live on that element.
- **`wizard-split`** — the surface contributes its **N** `physical_screens[]` elements (one own file per sub-step). The pattern fields live on each element; each sub-screen renders its own slice (`covers_properties`) of the surface.
- **`inline-drawer` / `inline-expand` / `modal`** — the surface contributes **0** own files. It is rendered as a `host_state` sub-tree on its `host_surface`'s physical screen. Its pattern fields sit on the surface entry (not on a `physical_screens[]` element, which is empty for folds). Capture `host_surface`, `rendered_on` (the host's physical `screen_id`), and `host_state` for step 4's fold rendering.
- **`combined`** — not emitted in the first wave (the architect must not author it; treat any occurrence as a structural bug → `failed`).

Build the in-memory `render_plan` as a flat list of **physical screen render units** plus a list of **fold render units**:

1. For every surface `LS` in `own.surface_plan`, read `LS.realization`.
2. If `standalone-screen` or `wizard-split`: for each element `ps` in `LS.physical_screens[]`, push a render unit `{ surface_id: LS, realization, screen_id: ps.screen_id, screen_file: ps.screen_file, covers_properties: ps.covers_properties, primary_pattern: ps.primary_pattern, primary_pattern_variant: ps.primary_pattern_variant, base_pattern_owner: ps.base_pattern_owner, modifiers: ps.modifiers, secondary_patterns: ps.secondary_patterns, states_rendered: ps.states_rendered, sub_step: ps.sub_step ?? null, of: ps.of ?? null }`.
3. If `inline-drawer` / `inline-expand` / `modal`: push a **fold render unit** `{ surface_id: LS, realization, host_surface: LS.host_surface, rendered_on: LS.rendered_on, host_state: LS.host_state, covers_properties: LS.covers_properties, primary_pattern: LS.primary_pattern, primary_pattern_variant: LS.primary_pattern_variant, base_pattern_owner: LS.base_pattern_owner, modifiers: LS.modifiers, secondary_patterns: LS.secondary_patterns, states_rendered: LS.states_rendered }`. A fold produces **no own file**; step 4 renders it onto its host screen's HTML.

**Cross-validate each render unit against `_index.md`:** every `primary_pattern` and every entry in `secondary_patterns[]` must be a real catalogue ID. The `primary_pattern_variant` membership in the pattern's `variants:` block is confirmed at step 4.1 when the per-pattern file is read. A pattern ID absent from `_index.md` is an architect bug that should have been caught at author-time — at render time it is a defensive `failed` (no silent substitution).

For each render unit (physical screen and fold), also derive a `screen_slug` from the surface's intent (kebab-case, max ~30 chars). For `standalone-screen` the file is `screen-NN-<slug>.html`; for `wizard-split` sub-steps the file is `screen-NNa-<slug>.html`, `screen-NNb-<slug>.html`, … (the `screen_file` field carries the authored filename — use it verbatim); folds have **no file**.

The `render_plan` (physical units + fold units) is the input to step 4. Each physical unit names the catalogue files step 4 will selectively read (its `primary_pattern` file + each `secondary_patterns` file); each fold unit names the same, to render its `host_state` sub-tree on the host screen.

---

**Next:** Read fully and follow `step-03-extract-ds.md`.
