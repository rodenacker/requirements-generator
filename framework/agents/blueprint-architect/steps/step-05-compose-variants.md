---
name: step-05-compose-variants
description: 'Compose 1-3 variant configurations deterministically from scope.json + domain-defaults.md. On add-variant mode, prompt the consultant for the one additional variant subject to the cap.'
---

# Step 5: Compose variants

Skipped entirely when `variants_output_path == null` (future `/prototype` single-design invocation).

This step is **deterministic** on the happy path. The consultant has already
expressed their direction at scope-selector's confirmation prompt (`Accept` /
`Edit dimensions`); the architect now applies that direction without asking
the consultant any further routine question. The conditional gate at step 7
is the only escalation path — and it fires only on bijection, conflict, or
pattern-coverage gap, never on routine variant composition.

The architect runs four sub-steps in order:

1. Resolve dimensions + cardinality from scope.json (override) or domain-defaults.md (default).
2. Filter dimensions for applicability; substitute via fallback chain if needed.
3. Compose variant configurations deterministically; bind personas; pick polar positions.
4. Self-validate per `tradeoff-dimensions-registry.md`.

**Supporting analyses consumed at this step.** When step 2.6 captured analyses (either as role-keyed projections from sidecars in `cached_projections[<role>][<source-name>]` per `framework/assets/analyses/sidecar-schema.md`, as bounded prose in `cached_legacy_full_reads[<source-name>].content`, or as deferred metadata stubs in `pending_step5_selections[]`), this step consumes those whose `architect_roles` include `variant-philosophy`, `variant-dimension-applicability`, `per-screen-state-chips`, `per-screen-async-states`, `per-screen-role-visibility`, `per-screen-cta-set`, `copy-vocabulary`, or `feature-presence`. The analyses **augment** the variant configurations with refining detail (per-screen state chip sets from STATE-DIAGRAM, persona-bound visibility from ACTIVITY-DIAGRAM, async screen variants from SEQUENCE-DIAGRAM, label vocabulary from GLOSSARY) and additional instructions about variant philosophy (USER-JOURNEYS pain-points and JTBD job-outcome mappings inform `design_philosophy` text and per-variant feature emphasis). Trade-off dimension applicability prefers the cached `trade-off-dimension-analysis` selection over the legacy fallback path at step 2.7.

## 5.0 Preamble — open deferred step-5 selections

Before composition begins, walk `pending_step5_selections[]` (populated at `step-02-read-inputs.md > 2.6.3`). For each entry, apply the same sidecar-first / bounded-fallback read protocol that block 2.6.2 used at step-02:

1. **Source artefact existence check.** If `entry.output_path` is absent on disk, halt plain-text per the same data-integrity message as 2.6.2 (a file disappearing between step-02 and step-05 is a `RF-04`-class halt).
2. **Sidecar branch.** When `entry.sidecar_present == true` AND the sidecar file exists: `Read` it; verify `schema_version`, `method`, and `source_sha256` per 2.6.2; fire `RF-08 stale_analysis_sidecar` on drift mismatch; for each role in `entry.step5_roles`, capture `architect_projection[<role>]` into `cached_projections[<role>][<entry.name>]`. Skip absent roles silently.
3. **Legacy fallback branch.** When the sidecar is absent: log `[ANALYSIS-FALLBACK: <entry.name>]` to the variant generator's in-thread summary; measure on-disk size of `entry.output_path`; fire `RF-09 legacy_analysis_too_large` if > 60 KB (same three-way `AskUserQuestion` as 2.6.2); otherwise full-Read into `cached_legacy_full_reads[<entry.name>]` and proceed.

After the preamble, the in-memory cache shape for step-5 consumption is uniform: every role payload the architect needs at this step is in `cached_projections[<role>][<source-name>]` (sidecar branch) or `cached_legacy_full_reads[<source-name>].content` (legacy branch).

`pending_step5_selections[]` is emptied after this preamble completes.

## 5.1 Resolve dimensions and cardinality

Read `scope.json > dimension_override`.

- **`dimension_override == null`** (happy path): use the canonical defaults from
  `framework/assets/wireframes/domain-defaults.md`:
    - `dimensions_diverging_on = ["density-focus", "speed-accuracy"]` (per Section 1).
    - `cardinality = 2` (per Section 2).
    - Variant slugs: `["CAREFUL-DEFAULT", "POWER-DENSE"]` (per Section 3).
- **`dimension_override != null`** (consultant overrode at scope-selector): use the override verbatim:
    - `dimensions_diverging_on = scope.json.dimension_override.dimensions`.
    - `cardinality = scope.json.dimension_override.cardinality`.
    - Variant slugs: derived from the dimensions + pole position. See sub-step 5.3.

On `mode = "add-variant"`, skip steps 5.1–5.3 entirely; jump to 5.4.

## 5.2 Filter dimensions for applicability + fallback chain

Read `framework/assets/wireframes/tradeoff-dimensions-registry.md > Section 2`
applicability rules. When `cached_projections["variant-dimension-applicability"]["trade-off-dimension-analysis"]` exists (sidecar branch — preferred; payload shape per `framework/assets/analyses/sidecar-schema.md > 2.10`), iterate its `dimension_scores[]` and use them to refine the applicability decision: a dimension is applicable iff the registry's Section 2 heuristic permits **and** the analysis scores ≥1 in-scope goal at a non-neutral position (`score` ∈ `{-2, -1, +1, +2}`) on the dimension. When that slot is absent but `cached_legacy_full_reads["trade-off-dimension-analysis"].content` is populated (legacy branch — fallback), best-effort-extract the same per-goal × dimension scoring from the prose's `<table>` body. When both are absent, fall back to the step-2.7 legacy read result; when all three are absent, use the registry heuristics alone.

For each dimension in `dimensions_diverging_on`, check applicability against the scope:

- **density-focus** applies iff scope contains ≥1 collection screen (table / data-list / dashboard inferred from the blueprint's screen inventory).
- **speed-accuracy** applies iff scope contains ≥1 input / capture screen (form or wizard inferred from the blueprint).
- **power-simplicity** applies iff `scope.json.personas_available` contains a persona whose §3 description spans both novice and expert traits (or a pair of personas where one is each).
- **control-automation** applies iff scope has system-driven decisions (validation / suggestion / default-fill / approval routing inferred from `BR-NN` rows or screen intents).
- **flexibility-consistency** applies iff scope spans multiple object types or multiple flows (≥2 distinct flows in scope.json's `task_flows` or ≥2 §7 data shapes in `data_shapes`).
- **memorability-discoverability** is **inactive** — reject any inclusion in `dimensions_diverging_on` and surface a structured error.

If every dimension in `dimensions_diverging_on` is applicable, advance to 5.3.

If one or more dimensions are inapplicable AND `dimension_override == null` (happy path), apply the **fallback chain** from `domain-defaults.md > Section 5`:

1. Substitute `control-automation` for an inapplicable default iff scope has system-driven decisions.
2. Substitute `power-simplicity` iff `personas_available` spans novice + expert traits.
3. Substitute `flexibility-consistency` iff scope spans multiple object types.

Record the substitution as a non-blocking note in the architect's in-memory state (surfaced in step 7's handback summary). Re-check applicability of the substituted dimension; if still inapplicable, advance to the next fallback rule.

If after exhausting the fallback chain fewer than two applicable dimensions remain, **do not auto-compose**. Set in-memory flag `cardinality_below_two = true` and let step 7's conditional gate fire (the consultant decides whether to accept a single-dimension comparison, narrow scope, or cancel).

If one or more dimensions are inapplicable AND `dimension_override != null` (override path), the consultant explicitly chose those dimensions. Do **not** silently substitute. Set in-memory flag `override_inapplicable = true` listing the offending dimensions; step 7's conditional gate fires asking the consultant to confirm, swap, or cancel.

## 5.3 Compose variants deterministically

Compose exactly `cardinality` variants. For each variant `i` in `1..cardinality`:

### 5.3.1 — Variant slug

- **Happy path** (`dimension_override == null`, `cardinality == 2`): use the canonical slugs from `domain-defaults.md > Section 3`: variant 1 = `CAREFUL-DEFAULT`, variant 2 = `POWER-DENSE`.
- **Override path** (`dimension_override != null`): derive the slug from the variant's pole position. For each dimension in `dimensions_diverging_on`, the variant sits at either its "careful pole" (negative position) or "power pole" (positive position). Compose the slug from the dominant pole words:
    - 2 variants → `<NEGATIVE-POLE-WORDS>-DEFAULT` and `<POSITIVE-POLE-WORDS>-LEAN`. E.g. for dimensions `[power-simplicity, control-automation]`: slugs `SIMPLE-MANUAL-DEFAULT` and `POWER-AUTO-LEAN`.
    - 3 variants → add a third `BALANCED-MIX` with neutral or opposite-pole positions on at least one dimension.
    - Pole-word vocabulary (per `framework/assets/wireframes/position-vocabulary.md`): `density-focus → SPACIOUS/DENSE`, `speed-accuracy → CAREFUL/SPEED`, `power-simplicity → SIMPLE/POWER`, `control-automation → MANUAL/AUTO`, `flexibility-consistency → BESPOKE/RIGID`.

Slugs must match `^[A-Z][A-Z0-9-]*$` and be unique within the run.

### 5.3.2 — Persona binding

Apply `domain-defaults.md > Section 4` rules:

1. If `scope.json.personas_available` contains a persona matching {`occasional`, `first-time`, `infrequent`, `new-user`} AND a persona matching {`daily`, `high-volume`, `power-user`, `expert`}: bind variant 1 (the "careful" / negative-pole variant) → occasional persona; bind variant 2 (the "power" / positive-pole variant) → daily persona. For a third variant, bind to the second-most-relevant persona or the first variant's persona (whichever is closer to "middle" traits).
2. Else if exactly one persona: bind every variant to it.
3. Else: bind every variant to the first persona alphabetically; record a non-blocking note in the architect's handback summary.

Capture as `variant.persona_binding` (verbatim persona name from §3) and `variant.persona_traits` (the in-memory traits captured at step 2.4).

### 5.3.3 — Dimension positions (polar pick)

For each variant, pick polar positions on each dimension in `dimensions_diverging_on`:

- **Variant 1** (the "careful" / negative-pole variant): pick the negative-pole position per `tradeoff-dimensions-registry.md > Section 3` that produces the most distinct rendering. Default rule: `-1` unless `-2` is the only position that produces visibly different output (rare).
- **Variant 2** (the "power" / positive-pole variant): pick the positive-pole position per Section 3. Default rule: `+2` on the lead dimension (the first entry in `dimensions_diverging_on`), `+1` on others.
- **Variant 3** (only when `cardinality == 3`): mixed. On the lead dimension, sit at `0`. On the others, alternate `+1`/`-1` to differentiate from variants 1 and 2.

For dimensions NOT in `dimensions_diverging_on`, set `variant.dimension_positions[<dimension>] = 0` (neutral) automatically.

Always set `variant.dimension_positions["memorability-discoverability"] = 0` regardless (upstream-pending invariant).

**Happy-path concrete values** (when defaults applied, no override):
- `CAREFUL-DEFAULT`: `density-focus: -1, speed-accuracy: -1, all others: 0`.
- `POWER-DENSE`: `density-focus: +2, speed-accuracy: +1, all others: 0`.

These match `domain-defaults.md > Section 3` verbatim.

### 5.3.4 — Design philosophy

The architect composes a one-line `design_philosophy` string grounded in the variant's bound persona and dimension positions. ≤ 100 chars. **No** dimension notation (`D3+2`), **no** pattern-catalogue IDs (`table.compact`). Plain English only.

When `cached_projections["variant-philosophy"]["user-journeys"]` or `cached_projections["variant-philosophy"]["jtbd"]` is populated (sidecar branch — preferred; payload shape per `framework/assets/analyses/sidecar-schema.md > 2.9`), iterate `philosophy_inputs[]` and incorporate the relevant `phase_or_job` + `design_implication` (e.g. *"reduces frustration at the `Validating` phase"* per a USER-JOURNEYS pain-point entry) or the job-outcome mapping (e.g. *"prioritises the `submit-and-leave` job"* per a JTBD entry) into the prose. When the sidecar projection is absent for either source but `cached_legacy_full_reads["user-journeys"].content` or `cached_legacy_full_reads["jtbd"].content` is populated (legacy branch — fallback), best-effort-extract the same pain-point / job-outcome facts from the prose. The string remains ≤ 100 chars and plain-English; cite the source only via `augmented_by` in step 6's `variants.json` metadata (see 5.6 below), not inline in `design_philosophy`.

Happy-path examples (no analyses cached):
- `CAREFUL-DEFAULT`: *"Spacious layout with careful confirmation gates; built for occasional or new operators."*
- `POWER-DENSE`: *"Dense table with keyboard-first inline-edit; built for daily high-volume operators."*

Augmented examples (USER-JOURNEYS + JTBD cached):
- `CAREFUL-DEFAULT`: *"Spacious confirmation-gated upload; reduces frustration at the Validating phase for new operators."*
- `POWER-DENSE`: *"Dense keyboard-first table; serves the daily submit-and-leave job for high-volume operators."*

### 5.3.5 — Per-variant compatibility check (architect-side)

Cross-check the composed variant `{persona_binding, dimension_positions}` against `tradeoff-dimensions-registry.md`:

- **Section 4 (incoherent pairs)**: if any rejected pair matches, treat as a hard structural error. On happy path (`dimension_override == null`), this should never fire (the defaults at `domain-defaults.md > Section 3` are pre-validated against incoherent pairs); fire-on-happy-path indicates a registry edit broke the defaults — surface a structured halt *"Architect default pair `<dim_a>: <pos_a>` × `<dim_b>: <pos_b>` is now incoherent per registry. Fix `domain-defaults.md` and re-run."* and abort. On override path, surface as a step-7 conditional-gate trigger asking the consultant to swap a dimension or cancel.
- **Section 5 (persona-position hard rejects)**: if any hard-reject rule matches, attempt automatic rebinding to a different persona from `personas_available` (apply Section 4 rules with the offending persona excluded). If no compatible persona exists, surface as a step-7 conditional-gate trigger.
- **Section 5 (soft conflicts)**: record a warning in the architect's in-memory state; surfaced in step 7's handback summary.

## 5.4 (Only on `mode = "add-variant"`) Single-variant consultant prompt

Read the existing `variants.json` (from step 2.5). Capture:

- `existing_dimensions_diverging_on = existing.dimensions_diverging_on`.
- `existing_variants_count = existing.variants.length`.

If `existing_variants_count == 3`, the cardinality cap is reached. Surface plain-text *"Variant cap reached: 3 of 3 variants already exist for `{{scope_slug}}`. Cannot add. Cancel or remove a variant via `Regenerate variants only` first."* and fail handback cleanly.

Otherwise, the architect surfaces **two** consultant prompts (the only AskUserQuestion calls in step 5; intentional because `add-variant` is an opt-in path):

### 5.4.1 — Persona binding for the new variant

Surface a single `AskUserQuestion`:

- Question: *"New variant — bind to which persona from `requirements.md > §3`?"*
- Header: `Persona`
- `multiSelect: false`
- Options: one per persona in `scope.personas_available`; label = persona name; description = persona characteristic from step 2.4.

### 5.4.2 — Polar pole choice

Surface a single `AskUserQuestion`:

- Question: *"New variant — which pole on the diverging dimensions (`{{existing_dimensions_diverging_on}}`)?"*
- Header: `Variant pole`
- `multiSelect: false`
- Options: `Careful / negative pole`, `Power / positive pole`, `Mixed / balanced`, `Cancel`.

The architect then derives the new variant's `dimension_positions` per the same polar rules as 5.3.3 — distinctness from existing variants is enforced (positions cannot duplicate any existing variant).

Run the compatibility check from 5.3.5 against the new variant. Append to `existing.variants` and set the merged list as `variants` for step 6's write.

## 5.5 Distinctness check

After every variant is composed (whether via 5.3 or 5.4), confirm no two variants have identical `dimension_positions` across the full six-dimension key set. On happy path with defaults this is guaranteed (CAREFUL-DEFAULT and POWER-DENSE diverge on every default dimension). On override + 3-variant runs, the mixed variant 3 must differ from both poles on at least one dimension — if not, the architect's polar-pick rule produced an aliased variant; re-derive variant 3 with explicit `0` on the lead dimension and opposite-pole values on the others.

## 5.6 Compose `variants.json` in memory

Assemble the artefact per the schema documented in `framework/agents/blueprint-architect.md > Output`. When step 2.6 cached one or more analyses with non-`upstream-only` roles, add an `augmented_by` field at the top level listing each consumed analysis as an audit trail (the comparator's index.html § Variant metadata cards surface this; the variant-generator does not consume it):

```json
{
  "scope_slug": "<scope_slug>",
  "authored_at": "<ISO-8601 UTC at this moment>",
  "blueprint_sha256": "<hash of blueprint.md as written at step 4>",
  "dimensions_diverging_on": [...],
  "cardinality_cap": 3,
  "augmented_by": [
    { "name": "task-flows", "consumed_at_steps": [3, 5], "consumed_roles": ["screen-inventory", "screen-flow", "per-screen-cta-set"] },
    { "name": "state-diagram", "consumed_at_steps": [3, 5], "consumed_roles": ["screen-inventory", "per-screen-state-chips"] }
  ],
  "variants": [...]
}
```

When no analyses were cached (Stage 1b returned `selected-none` or `analyses_inputs_path` was null), omit the `augmented_by` field entirely (do not write an empty array — the absence of the field signals "no augmentation").

Step 6 writes it.

---

**Next:** Read fully and follow `step-06-write-artefacts.md`.
