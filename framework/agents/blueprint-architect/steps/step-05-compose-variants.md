---
name: step-05-compose-variants
description: 'Compose 1-3 variant configurations bound to specific personas and positioned on consultant-chosen trade-off dimensions. On add-variant mode, append one new variant subject to the cap.'
---

# Step 5: Compose variants

Skipped entirely when `variants_output_path == null` (future `/prototype` single-design invocation).

The architect runs three sub-steps in order:

1. Surface dimension-divergence prompt to the consultant (skipped on `add-variant`).
2. Compose variant configurations (`create` / `regenerate-variants`) or surface single-variant prompt (`add-variant`).
3. Self-validate per `tradeoff-dimensions-registry.md`.

## 5.1 (Skipped on `add-variant`) Filter dimensions by applicability

Per `framework/assets/wireframes/tradeoff-dimensions-registry.md > Section 2`, apply the applicability rules using:

- Scope characteristics (collection-heavy? form-heavy? read-only? multi-flow?).
- `scope.personas_available` (mixed-persona scope → D2 applies; uniform persona → D2 may not apply).
- Optional `analyse-requirements/TRADE-OFF-DIMENSIONS/trade-off-matrix.html` per-goal scoring (if the file was read at step 2.6) — goals scoring near the poles on a dimension reinforce applicability.

Compute the **applicable dimensions** list. Filter out the upstream-pending `memorability-discoverability` regardless (the dimension is reserved per Section 1 status).

## 5.2 (Skipped on `add-variant`) Prompt the consultant for divergence dimensions

Surface a single `AskUserQuestion`:

- Question: *"Which trade-off dimensions should the variants diverge on? Up to 3 recommended; more than 3 dilutes the comparison."*
- Header: `Dimensions`
- `multiSelect: true`
- Options: one per applicable dimension, labelled with the dimension's positive-pole / negative-pole names (e.g. `density-focus — sparse Focus … dense Density`). Description lines summarise the dimension's effect in one sentence.

Capture the consultant's selection into `dimensions_diverging_on` (1 to 6 elements; the architect's character file recommends ≤3 but does not hard-cap at this layer — the *variant cardinality* cap of 3 effectively bounds how many dimensions can be meaningfully diverged on anyway).

## 5.3 (Skipped on `add-variant`) Prompt the consultant for cardinality

Surface a single `AskUserQuestion`:

- Question: *"How many variants? Default 2 (recommended for a clean A/B stakeholder choice); 3 is the hard cap."*
- Header: `Variant count`
- `multiSelect: false`
- Options:
    1. `2 — A/B comparison (Recommended)`
    2. `3 — three-way comparison (only when a third dimension adds genuine divergence)`

Capture as `N` (2 or 3).

## 5.4 (Skipped on `add-variant`) Per-variant configuration

For each variant index `i` in `1..N`, surface a sequence of prompts:

### 5.4.1 — Persona binding

Surface a single `AskUserQuestion`:

- Question: *"Variant {{i}} — bind to which persona from `requirements.md > §3`?"*
- Header: `Persona V{{i}}`
- `multiSelect: false`
- Options: one per persona in `scope.personas_available`, label = persona name, description = persona characteristic from step 2.4.

Capture as `variant.persona_binding` and `variant.persona_traits` (the in-memory traits from step 2.4).

### 5.4.2 — Per-dimension position

For each dimension in `dimensions_diverging_on`, the architect proposes an initial position for variant `i` based on:

- Persona traits (per `tradeoff-dimensions-registry.md > Section 5`).
- Distinctness from variants `1..i-1` (variants must diverge structurally, so position values do not duplicate).
- Goal scoring (if `trade-off-matrix.html` was read).

Surface a single `AskUserQuestion` per dimension to confirm or override the architect's proposal:

- Question: *"Variant {{i}} on dimension `{{dimension}}`: position?"*
- Header: `V{{i}} {{dimension}}`
- `multiSelect: false`
- Options: one per legal integer position `-2 -1 0 +1 +2`, label = position + pole name + one-line consequence. The architect's proposal is marked `(Recommended)`.

Capture as `variant.dimension_positions[<dimension>]`.

For dimensions NOT in `dimensions_diverging_on`, set `variant.dimension_positions[<dimension>] = 0` (neutral) automatically. Always set `variant.dimension_positions["memorability-discoverability"] = 0` regardless of consultant input (upstream-pending invariant).

### 5.4.3 — Design philosophy

The architect composes a one-line `design_philosophy` string grounded in the variant's bound persona and dimension positions. Example: *"Inline-edit table optimised for keyboard navigation; minimal confirmation friction for daily-Importer throughput."* No consultant prompt at this sub-step; the architect emits the line and surfaces it at the per-variant compatibility check below.

### 5.4.4 — Per-variant compatibility check (architect-side)

Cross-check the proposed variant `{persona_binding, dimension_positions}` against `tradeoff-dimensions-registry.md`:

- Section 4 (incoherent pairs): if any rejected pair matches, surface a structured rejection plain-text *"Variant {{i}} rejected: incoherent pair `<dim_a>: <pos_a>` × `<dim_b>: <pos_b>` per registry. Re-prompt this variant."* and loop back to 5.4.2.
- Section 5 (persona-position hard rejects): if any hard-reject rule matches, surface a structured rejection plain-text *"Variant {{i}} rejected: persona `<persona>` is incompatible with `<dim>: <pos>` per registry. Re-prompt persona or position."* and loop back to 5.4.1 or 5.4.2 (consultant decides via `AskUserQuestion`).
- Section 5 (soft conflicts): record a warning into in-memory state but do not reject; the warning surfaces in the architect's step-7 summary.

## 5.5 (Only on `add-variant`) Single-variant prompt

Read the existing `variants.json` (from step 2.5). Capture:

- `existing_dimensions_diverging_on` from `existing.dimensions_diverging_on`.
- `existing_variants_count = existing.variants.length`.

If `existing_variants_count == 3`, the cardinality cap is reached. Surface plain-text *"Variant cap reached: 3 of 3 variants already exist for `{{scope_slug}}`. Cannot add. Cancel or remove a variant via `Regenerate variants only` first."* and fail handback cleanly.

Otherwise, surface the same sub-prompts as 5.4 (persona binding, per-dimension position, design philosophy) for the **single** new variant. Run the same compatibility check. Append to `existing.variants` and set the merged list as `variants` for step 6's write.

## 5.6 Distinctness check

After every variant is composed (whether via 5.4 or 5.5), confirm no two variants have identical `dimension_positions` across the full six-dimension key set. A duplicate is a hard structural error — re-prompt the offending variant per the orchestrator's `Variant V<N> dimension positions are identical to V<M>; vary at least one dimension or cancel.` message.

## 5.7 Compose `variants.json` in memory

Assemble the artefact per the schema documented in `framework/agents/blueprint-architect.md > Output`:

```json
{
  "scope_slug": "<scope_slug>",
  "authored_at": "<ISO-8601 UTC at this moment>",
  "blueprint_sha256": "<hash of blueprint.md as written at step 4>",
  "dimensions_diverging_on": [...],
  "cardinality_cap": 3,
  "variants": [...]
}
```

Step 6 writes it.

---

**Next:** Read fully and follow `step-06-write-artefacts.md`.
