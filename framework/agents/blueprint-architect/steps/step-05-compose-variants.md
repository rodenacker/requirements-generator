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

The architect runs these sub-steps in order:

1. Resolve dimensions + cardinality by **three-tier precedence**: `scope.json > dimension_override` → `scope.json > divergence_profile` → `domain-defaults.md`.
2. Filter dimensions for applicability; substitute via fallback chain if needed.
3. Compose variant configurations deterministically; bind personas (per the in-force tier); pick polar positions; author the per-surface `surface_plan` (pattern picks + realization + `physical_screens[]`) and derive `physical_flow`.
4. Self-validate per `tradeoff-dimensions-registry.md` (incl. realization integrity + `(dimension_position × realization)` coherence).

**Supporting analyses consumed at this step.** When step 2.6 captured analyses (either as role-keyed projections from sidecars in `cached_projections[<role>][<source-name>]` per `framework/assets/analyses/sidecar-schema.md`, as bounded prose in `cached_legacy_full_reads[<source-name>].content`, or as deferred metadata stubs in `pending_step5_selections[]`), this step consumes those whose `architect_roles` include `variant-philosophy`, `variant-dimension-applicability`, `per-screen-state-chips`, `per-screen-async-states`, `per-screen-role-visibility`, `per-screen-cta-set`, `copy-vocabulary`, or `feature-presence`. The analyses **augment** the variant configurations with refining detail (per-screen state chip sets from STATE-DIAGRAM, persona-bound visibility from ACTIVITY-DIAGRAM, async screen variants from SEQUENCE-DIAGRAM, label vocabulary from GLOSSARY) and additional instructions about variant philosophy (USER-JOURNEYS pain-points and JTBD job-outcome mappings inform `design_philosophy` text and per-variant feature emphasis). Trade-off dimension applicability prefers the cached `trade-off-dimension-analysis` selection over the legacy fallback path at step 2.7.

## 5.0 Preamble — open deferred step-5 selections

Before composition begins, walk `pending_step5_selections[]` (populated at `step-02-read-inputs.md > 2.6.3`). For each entry, apply the same sidecar-first / bounded-fallback read protocol that block 2.6.2 used at step-02:

1. **Source artefact existence check.** If `entry.output_path` is absent on disk, halt plain-text per the same data-integrity message as 2.6.2 (a file disappearing between step-02 and step-05 is a `RF-04`-class halt).
2. **Sidecar branch.** When `entry.sidecar_present == true` AND the sidecar file exists: `Read` it; verify `schema_version`, `method`, and `source_sha256` per 2.6.2; fire `RF-08 stale_analysis_sidecar` on drift mismatch; for each role in `entry.step5_roles`, capture `architect_projection[<role>]` into `cached_projections[<role>][<entry.name>]`. Skip absent roles silently.
3. **Legacy fallback branch.** When the sidecar is absent: log `[ANALYSIS-FALLBACK: <entry.name>]` to the variant generator's in-thread summary; measure on-disk size of `entry.output_path`; fire `RF-09 legacy_analysis_too_large` if > 60 KB (same three-way `AskUserQuestion` as 2.6.2); otherwise full-Read into `cached_legacy_full_reads[<entry.name>]` and proceed.

After the preamble, the in-memory cache shape for step-5 consumption is uniform: every role payload the architect needs at this step is in `cached_projections[<role>][<source-name>]` (sidecar branch) or `cached_legacy_full_reads[<source-name>].content` (legacy branch).

`pending_step5_selections[]` is emptied after this preamble completes.

## 5.1 Resolve dimensions and cardinality (three-tier precedence)

Resolve the divergence configuration by **three-tier precedence** (first present tier wins; lower tiers are not consulted once a higher tier is in force):

1. **`scope.json > dimension_override`** (Tier 1 — manual edit, always wins). When non-null, the consultant explicitly overrode the dimension profile at scope-selector's `Edit dimensions` branch. Use it verbatim:
    - `dimensions_diverging_on = scope.json.dimension_override.dimensions`.
    - `cardinality = scope.json.dimension_override.cardinality`.
    - Variant slugs: derived from the dimensions + pole position (sub-step 5.3.1, override branch).
    - Persona binding: per the `domain-defaults.md > Section 4` occasional/daily logic (5.3.2 default branch) — `dimension_override` carries no per-variant persona bindings.
2. **`scope.json > divergence_profile`** (Tier 2 — the goal/persona-driven recommendation persisted by `framework/skills/scope-selector.md`). When `dimension_override == null` AND `divergence_profile` is present, consume it **verbatim** (see the anti-double-inference note below). It carries:
    - `divergence_profile.dimensions` → `dimensions_diverging_on`.
    - `divergence_profile.cardinality` → `cardinality`.
    - `divergence_profile.variant_bindings[]` — one entry per variant, each `{ persona, pole, recommended_posture, posture_label, ... }` where `persona` is a verbatim §3 persona name and `pole ∈ {careful, power, mixed}`. Drives persona binding (5.3.2 profile branch) and polar position mapping (5.3.3 profile branch).
    - `divergence_profile.variant_bindings[i].recommended_posture` (+ `posture_label`) — the UX posture (`P1`..`P6`, or `null`). Consumed **verbatim** as a structural/realization + naming overlay: it names the `design_philosophy` string (5.3.4) and biases pattern picks (5.3.6 A). It does **not** change `dimension_positions` (those stay governed by `pole` + the registry §3 at 5.3.3). When `null`, fall back to today's position-derived `design_philosophy` + pattern picks.
    - `divergence_profile.realization_recommendation` — a persona-goal-type → `{ prefer: [...], avoid: [...] }` map of preferred / avoided realization strategies. Consumed at 5.3.6 when picking each surface's realization.
    - Variant slugs: derived per 5.3.1's profile branch (pole-word vocabulary, like the override branch).
3. **`framework/assets/wireframes/domain-defaults.md`** (Tier 3 — static fallback). When both `dimension_override` and `divergence_profile` are absent (the simplest happy path):
    - `dimensions_diverging_on = ["density-focus", "speed-accuracy"]` (per Section 1).
    - `cardinality = 2` (per Section 2).
    - Variant slugs: `["CAREFUL-DEFAULT", "POWER-DENSE"]` (per Section 3).
    - Persona binding: the occasional/daily logic of `domain-defaults.md > Section 4` (5.3.2 default branch).
    - There is no profile-supplied `realization_recommendation`; every surface uses its blueprint `Default realization` (`standalone-screen` in the first wave) at 5.3.6 — i.e. the baseline.

Record which tier is in force as `divergence_tier ∈ {override, profile, defaults}` in in-memory state (surfaced in step 7's handback summary).

> **Anti-double-inference (load-bearing).** When `divergence_profile` is in force (Tier 2), the architect **consumes it verbatim** and must **never re-run the divergence heuristic** — that heuristic executes exactly once, in `framework/skills/scope-selector.md`, and its output is what `divergence_profile` records. In particular, do **not** apply the `domain-defaults.md > Section 4` occasional/daily persona-binding logic when a profile is in force: bind each variant to `variant_bindings[i].persona` directly. (If a `variant_bindings[i].persona` is absent from `scope.json > personas_available` — requirements drifted between scope selection and now — treat it as a structural warning and fall back to Tier 3 `domain-defaults.md`; do not hard-fail. This mirrors `framework/agents/blueprint-architect.md > Anti-Patterns`.) **Likewise for the posture:** consume `variant_bindings[i].recommended_posture` verbatim and never re-run `divergence-heuristics.md` §4b's lookup — the posture is a structural overlay, not a fresh inference.

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

If one or more dimensions are inapplicable AND `divergence_tier ∈ {defaults, profile}` (the auto-derived tiers — neither was a manual consultant override), apply the **fallback chain** from `domain-defaults.md > Section 5`:

1. Substitute `control-automation` for an inapplicable default iff scope has system-driven decisions.
2. Substitute `power-simplicity` iff `personas_available` spans novice + expert traits.
3. Substitute `flexibility-consistency` iff scope spans multiple object types.

Record the substitution as a non-blocking note in the architect's in-memory state (surfaced in step 7's handback summary). Re-check applicability of the substituted dimension; if still inapplicable, advance to the next fallback rule. (On the `profile` tier, a substitution that drops a profile-recommended dimension is still non-blocking, but record it as a `profile-dimension-substituted` note so the divergence between the scope-selector's recommendation and the rendered set is auditable.)

If after exhausting the fallback chain fewer than two applicable dimensions remain, **do not auto-compose**. Set in-memory flag `cardinality_below_two = true` and let step 7's conditional gate fire (the consultant decides whether to accept a single-dimension comparison, narrow scope, or cancel).

If one or more dimensions are inapplicable AND `divergence_tier == override` (Tier 1 — the consultant explicitly chose those dimensions at scope-selector's `Edit dimensions` branch), do **not** silently substitute. Set in-memory flag `override_inapplicable = true` listing the offending dimensions; step 7's conditional gate fires asking the consultant to confirm, swap, or cancel.

## 5.3 Compose variants deterministically

Compose exactly `cardinality` variants. For each variant `i` in `1..cardinality`:

### 5.3.1 — Variant slug

- **Defaults tier** (`divergence_tier == defaults`, `cardinality == 2`): use the canonical slugs from `domain-defaults.md > Section 3`: variant 1 = `CAREFUL-DEFAULT`, variant 2 = `POWER-DENSE`.
- **Override / profile tier** (`divergence_tier ∈ {override, profile}`): derive the slug from the variant's pole position. For each dimension in `dimensions_diverging_on`, the variant sits at either its "careful pole" (negative position) or "power pole" (positive position) — for the `profile` tier, the variant's pole comes verbatim from `variant_bindings[i].pole`. Compose the slug from the dominant pole words:
    - 2 variants → `<NEGATIVE-POLE-WORDS>-DEFAULT` and `<POSITIVE-POLE-WORDS>-LEAN`. E.g. for dimensions `[power-simplicity, control-automation]`: slugs `SIMPLE-MANUAL-DEFAULT` and `POWER-AUTO-LEAN`.
    - 3 variants → add a third `BALANCED-MIX` with neutral or opposite-pole positions on at least one dimension (or the pole of the third `variant_bindings[2]` entry when on the profile tier).
    - Pole-word vocabulary (per `framework/assets/wireframes/position-vocabulary.md`): `density-focus → SPACIOUS/DENSE`, `speed-accuracy → CAREFUL/SPEED`, `power-simplicity → SIMPLE/POWER`, `control-automation → MANUAL/AUTO`, `flexibility-consistency → BESPOKE/RIGID`.

Slugs must match `^[A-Z][A-Z0-9-]*$` and be unique within the run.

### 5.3.2 — Persona binding

The binding source depends on `divergence_tier`:

- **Profile tier** (`divergence_tier == profile`): bind variant `i` → `divergence_profile.variant_bindings[i].persona` **verbatim** — do **not** re-run the occasional/daily heuristic (anti-double-inference, per 5.1). The scope-selector already decided which persona each pole serves and persisted it in the profile. If `variant_bindings[i].persona` is absent from `scope.json > personas_available` (requirements drifted since scope selection), record a structural warning and fall back to the `domain-defaults.md > Section 4` rules below for that variant (do not hard-fail).
- **Override / defaults tier** (`divergence_tier ∈ {override, defaults}`): apply `domain-defaults.md > Section 4` rules:
    1. If `scope.json.personas_available` contains a persona matching {`occasional`, `first-time`, `infrequent`, `new-user`} AND a persona matching {`daily`, `high-volume`, `power-user`, `expert`}: bind variant 1 (the "careful" / negative-pole variant) → occasional persona; bind variant 2 (the "power" / positive-pole variant) → daily persona. For a third variant, bind to the second-most-relevant persona or the first variant's persona (whichever is closer to "middle" traits).
    2. Else if exactly one persona: bind every variant to it.
    3. Else: bind every variant to the first persona alphabetically; record a non-blocking note in the architect's handback summary.

Capture as `variant.persona_binding` (verbatim persona name from §3) and `variant.persona_traits` (the in-memory traits captured at step 2.4).

### 5.3.3 — Dimension positions (polar pick)

For each variant, pick polar positions on each dimension in `dimensions_diverging_on`. On the **profile tier**, the variant's pole is `divergence_profile.variant_bindings[i].pole ∈ {careful, power, mixed}`; map it to a concrete position per the rules below (`careful → negative-pole rule`, `power → positive-pole rule`, `mixed → variant-3 mixed rule`). On the **override / defaults tiers**, the careful/power assignment is by variant index (variant 1 = careful, variant 2 = power, variant 3 = mixed).

- **Careful pole** (variant 1 on override/defaults; `pole == careful` on profile): pick the negative-pole position per `tradeoff-dimensions-registry.md > Section 3` that produces the most distinct rendering. Default rule: `-1` unless `-2` is the only position that produces visibly different output (rare).
- **Power pole** (variant 2 on override/defaults; `pole == power` on profile): pick the positive-pole position per Section 3. Default rule: `+2` on the lead dimension (the first entry in `dimensions_diverging_on`), `+1` on others.
- **Mixed pole** (variant 3 when `cardinality == 3` on override/defaults; `pole == mixed` on profile): mixed. On the lead dimension, sit at `0`. On the others, alternate `+1`/`-1` to differentiate from the careful and power variants.

For dimensions NOT in `dimensions_diverging_on`, set `variant.dimension_positions[<dimension>] = 0` (neutral) automatically.

Always set `variant.dimension_positions["memorability-discoverability"] = 0` regardless (upstream-pending invariant).

**Defaults-tier concrete values** (`divergence_tier == defaults`):
- `CAREFUL-DEFAULT`: `density-focus: -1, speed-accuracy: -1, all others: 0`.
- `POWER-DENSE`: `density-focus: +2, speed-accuracy: +1, all others: 0`.

These match `domain-defaults.md > Section 3` verbatim.

### 5.3.4 — Design philosophy (posture-derived)

The architect composes a one-line `design_philosophy` string grounded in the variant's bound persona and dimension positions. ≤ 100 chars. **No** dimension notation (`D3+2`), **no** pattern-catalogue IDs (`table.compact`). Plain English only.

**Posture binding.** On the **profile tier**, when `variant_bindings[i].recommended_posture` is non-null, set `variant.posture = recommended_posture` and `variant.posture_label = posture_label` (verbatim from the profile), and **derive the `design_philosophy` string from that posture's essence + the bound persona** — the posture is the named source of the variant's UX character (look up the posture's characterization in `framework/assets/wireframes/design-philosophies.md`, restated in ≤ 100 plain-English chars; never copy its prose wholesale or emit the `P#` id in the string). When `recommended_posture` is `null` (override / defaults tier, or the degrade case), set `variant.posture = null` / `variant.posture_label = null` and compose `design_philosophy` from the bound persona + positions exactly as before. Both `posture` and `posture_label` are carried onto the variant for the artefact (5.6) and `variant-position.json`.

When `cached_projections["variant-philosophy"]["user-journeys"]` or `cached_projections["variant-philosophy"]["jtbd"]` is populated (sidecar branch — preferred; payload shape per `framework/assets/analyses/sidecar-schema.md > 2.9`), iterate `philosophy_inputs[]` and incorporate the relevant `phase_or_job` + `design_implication` (e.g. *"reduces frustration at the `Validating` phase"* per a USER-JOURNEYS pain-point entry) or the job-outcome mapping (e.g. *"prioritises the `submit-and-leave` job"* per a JTBD entry) into the prose. When the sidecar projection is absent for either source but `cached_legacy_full_reads["user-journeys"].content` or `cached_legacy_full_reads["jtbd"].content` is populated (legacy branch — fallback), best-effort-extract the same pain-point / job-outcome facts from the prose. The string remains ≤ 100 chars and plain-English; cite the source only via `augmented_by` in step 6's `variants.json` metadata (see 5.6 below), not inline in `design_philosophy`.

Happy-path examples (no analyses cached):
- `CAREFUL-DEFAULT`: *"Spacious layout with careful confirmation gates; built for occasional or new operators."*
- `POWER-DENSE`: *"Dense table with keyboard-first inline-edit; built for daily high-volume operators."*

Augmented examples (USER-JOURNEYS + JTBD cached):
- `CAREFUL-DEFAULT`: *"Spacious confirmation-gated upload; reduces frustration at the Validating phase for new operators."*
- `POWER-DENSE`: *"Dense keyboard-first table; serves the daily submit-and-leave job for high-volume operators."*

### 5.3.5 — Per-variant compatibility check (architect-side)

Cross-check the composed variant `{persona_binding, dimension_positions}` against `tradeoff-dimensions-registry.md`:

- **Section 4 (incoherent pairs)**: if any rejected pair matches, treat as a hard structural error. On the `defaults` tier this should never fire (the defaults at `domain-defaults.md > Section 3` are pre-validated against incoherent pairs); fire-on-defaults indicates a registry edit broke the defaults — surface a structured halt *"Architect default pair `<dim_a>: <pos_a>` × `<dim_b>: <pos_b>` is now incoherent per registry. Fix `domain-defaults.md` and re-run."* and abort. On the `override` or `profile` tier, surface as a step-7 conditional-gate trigger asking the consultant to swap a dimension or cancel (a `profile`-tier incoherent pair means the scope-selector's recommendation needs revisiting — do not silently rewrite the profile).
- **Section 5 (persona-position hard rejects)**: if any hard-reject rule matches, attempt automatic rebinding to a different persona from `personas_available` (apply Section 4 rules with the offending persona excluded). On the `profile` tier, a hard reject against the profile-bound persona is **not** auto-rebound (the profile's persona binding is authoritative) — surface it as a step-7 conditional-gate trigger instead. If no compatible persona exists, surface as a step-7 conditional-gate trigger.
- **Section 5 (soft conflicts)**: record a warning in the architect's in-memory state; surfaced in step 7's handback summary.

### 5.3.6 — Author the per-surface `surface_plan`

Per variant, after the 5.3.5 compatibility check passes, author a `surface_plan` keyed by **every** `LS-NN` in the blueprint's surface inventory (1:1 — no surface missing, no extra key). This is the single source of truth for the variant's pattern picks **and** its information-architecture realizations; the variant-generator *renders* this plan and never re-derives it. The per-surface shape is defined canonically in `framework/assets/wireframes/realization-strategies.md > Section 2`.

For each surface `LS`:

**A. Pick the primary pattern + variant (per Section 3.0's base-owner rule).**

**Posture bias (profile tier, `variant.posture` non-null).** Before applying the base-owner rule, read the bound posture's **structural recommendations** from `framework/assets/wireframes/design-philosophies.md` (navigation model, primary data display, input philosophy, disclosure, realization preference). Use them to *bias* the shortlist resolution below **only where the base-owner rule leaves a genuine choice** — e.g. a `P2 Guided` variant prefers a `multi-step-wizard` Forms archetype + cards / spacious list; a `P1`/`P3` variant prefers a compact table + inline-edit; a `P4 Error-Averse` variant prefers a modal create/edit. The posture **never** overrides the registry Section 3.0 base-owner rule, the catalogue closed set, or the author-time validation (part D) — it breaks ties within the already-legal candidate set, nothing more. **Low-fi altitude guard:** consume only the *structural* layer of the posture (navigation / data display / disclosure / input philosophy / realization preference). **Ignore** the posture's hi-fi interaction specifics (command palette Cmd-K, optimistic-update + undo toasts, type-to-confirm, sparklines) — those are prototype-only and have no low-fi wireframe rendering. When `variant.posture` is `null`, skip this bias entirely (today's behaviour).

1. **Candidate shortlist.** Use `pattern_candidates[<LS>]` (captured by step-04 at `step-04-check-pattern-coverage.md > 4.2`). **`regenerate-variants` fallback:** when `pattern_candidates` is empty (step-04 was skipped because `mode != "create"`), derive the shortlist directly: re-read the reused blueprint's surface inventory row for `LS` (its `Intent` + `Sources`), shortlist by intent against `framework/assets/wireframes/pattern-bindings.md > Section 1` (the pattern-category bindings) cross-checked against `framework/assets/pattern-catalogue/_index.md` (the closed set of real patterns + tiers). Skip `T3` stubs (they have no authored body to render against).
2. **`primary_pattern`** — pick from the shortlist ∩ `framework/assets/pattern-catalogue/_index.md` (a real, non-`T3` catalogue ID). When the shortlist offers more than one candidate, prefer the one whose pattern-category the base-owner dimension (next bullet) governs.
3. **`primary_pattern_variant`** — read the chosen pattern's catalogue file (`framework/assets/pattern-catalogue/<category>/<pattern>.md`) `variants:` block and pick a variant present in it, applying the registry **Section 3.0 base-owner rule** for this variant's `dimension_positions`:
    - The **base-pattern owner** dimension for the surface's pattern-category selects the base pattern + variant. Per registry Section 3.0: **density-focus owns Collections** (base pattern + `wf-table--spacious` / `wf-table--compact` DS spacing *modifier*, never a non-existent `table.spacious` catalogue variant); **speed-accuracy owns the Forms archetype** (`multi-step-wizard` ↔ `single-form` ↔ `inline-edit`) and density-focus owns the Forms *layout* variant; power-simplicity owns Navigation/surfaces.
    - Record the owner in `base_pattern_owner` (the dimension that chose the base, per Section 3.0).
4. **Modifier dimensions → `modifiers[]` + `secondary_patterns[]`.** Every other diverging dimension contributes only modifiers (DS spacing classes like `wf-table--compact`, combinable catalogue behaviours like `selectable` / `editable`, and plain-text composition adjustments) and any secondary catalogue patterns (`forms/search-and-filter`, `feedback/empty-state`, etc.) — never a competing base pattern. Two diverging dimensions must **not** both name a base for one surface (registry Section 3.0).
5. **`states_rendered[]`** — derive the states this surface renders (`default`, `loading`, `empty`, `error`, host-state for a fold) from the surface intent + any cached `per-screen-state-chips` / `per-screen-async-states` projections.

**B. Pick the surface's realization (per `realization-strategies.md`).**

1. Read the blueprint surface row's `Allowed realizations` set for `LS` (`allowed_realizations[LS]`).
2. **Preferred-set intersection.** On the `profile` tier, intersect `allowed_realizations[LS]` with the bound persona's `divergence_profile.realization_recommendation.prefer` (the persona-goal-type's preferred realizations). Pick the first member of the intersection that is not in `…realization_recommendation.avoid`. When the intersection is empty (or on the `override` / `defaults` tier where no `realization_recommendation` exists), fall back to the surface's `Default realization` (`standalone-screen` in the first wave — i.e. the baseline).
    - The bound posture's own "Realization recommendation" line (in `design-philosophies.md`) **agrees with** `realization_recommendation` by construction — both are keyed to the same persona-goal-type (the heuristic's §4 and §4b draw on the same binding). So the persisted `realization_recommendation` remains the single field consulted here; do not introduce a second, possibly-conflicting realization source from the posture.
3. Record the chosen `realization` on the surface_plan entry.

**C. Derive `physical_screens[]` per `realization-strategies.md > Section 1`.**

- **`standalone-screen`** → exactly **1** `physical_screens[]` element: `{ screen_id: "S-NN", screen_file: "screen-NN-slug.html", covers_properties: <the surface's full Properties closed set>, primary_pattern, primary_pattern_variant, base_pattern_owner, modifiers[], secondary_patterns[], states_rendered[] }`. **Baseline:** when every surface in the variant is `standalone-screen`, the `S-NN` / `screen-NN-slug.html` names reproduce the pre-realization `LS-NN ≡ S-NN` mapping (one physical screen per surface, same numbering and slug convention as the pre-realization pipeline).
- **`wizard-split`** → **N** `physical_screens[]` elements (`screen_id` = `S-NNa`, `S-NNb`, `S-NNc`, …; `screen_file` = `screen-NNa-slug.html`, …; `sub_step` / `of` set). **Partition the surface's Properties closed set across the sub-screens so that `union(physical_screens[*].covers_properties) == ` the surface's full closed set** (no property dropped, none duplicated unless a field legitimately recurs as a review echo). The pattern fields (`primary_pattern: forms/multi-step-wizard`, `secondary_patterns: [navigation/stepper-indicator]`, etc.) live on **each** sub-screen element.
- **`inline-drawer` / `inline-expand` / `modal`** → **0** `physical_screens[]` elements. Set on the surface entry: `host_surface` (the LS-NN this folds onto — from the blueprint's `Host surface` cell), `rendered_on` (the host's physical `screen_id` in *this* variant — resolved from the host surface's own surface_plan entry), `host_state` (the host screen state that renders this surface — e.g. `drawer-detail-open`, `errors-expanded`, `confirm-modal-open`). The pattern fields sit on the surface entry (not on `physical_screens`) and the generator renders them into the host's `host_state` sub-tree. The folded surface still carries its full `covers_properties` (the fold does not drop the property audit trail).

**D. Author-time validation (do NOT silently fall back).** For every pattern + variant the plan names:

- Confirm `primary_pattern` and every `secondary_patterns[]` entry is a valid catalogue ID present in `framework/assets/pattern-catalogue/_index.md` (and is not a `T3` stub).
- Confirm `primary_pattern_variant` is present in that pattern's catalogue `variants:` block.
- On any miss, set in-memory flag `surface_plan_gap = true` and record `{surface_id, variant_id, missing: <pattern-or-variant-id>, reason}`. This flag is a **step-07 conditional-gate trigger** (it joins the bijection / conflict / pattern-coverage-gap predicates step-07 already fires on; step-07's 7.1 predicate list must include `surface_plan_gap == true`, and its 7.2 prompt must surface the recorded `{surface_id, variant_id, missing}` rows). **Never silently substitute a different pattern or let an absent variant fall through to the generator** (that was the old behaviour that produced false-positive drift). This realizes the catalogue-validity routing that `framework/agents/blueprint-architect.md > Self-validation` already declares ("A miss was routed to the step-07 conditional gate — never left to fall through to the generator").

**E. `(dimension_position × realization)` coherence check.** Reject (route to the step-07 gate, recording `surface_plan_gap`) any surface_plan entry whose chosen `realization` is incoherent with the variant's `dimension_positions`, per this minimal set:

- `realization == combined` is **never** valid (first wave) — but `combined` is never picked anyway (it is not in any blueprint `Allowed realizations` set), so this is a defensive guard. In particular, never pair `density-focus -2` × `combined`.
- `wizard-split` × `speed-accuracy +2` — a max-speed variant must not split a capture into a multi-step wizard (the wizard fights speed-+2's premise; same spirit as registry Section 4's D1×D2 incoherence). Prefer `standalone-screen` (or `modal` for a low-field capture) on a `speed-accuracy +2` variant.

(This list is intentionally minimal — it catches the structurally self-contradictory `(position × realization)` combinations only; it is not a second copy of registry Section 4's dimension-pair rules.)

**F. Derive `physical_flow` for the variant.** Expand the blueprint's logical flow (`LS-01 → LS-02; …`) into this variant's concrete `physical_flow` string by substituting each surface's realization:

- A `standalone-screen` surface contributes its `S-NN` node.
- A `wizard-split` surface contributes its sub-screen chain (`S-NNa → S-NNb → S-NNc`).
- A folded surface (`inline-drawer` / `inline-expand` / `modal`) contributes **no** standalone navigation node — instead annotate the host edge (e.g. `S-01 ⟳ drawer(LS-03)`, `S-02 ⟳ modal(LS-04)`).

Also enforce the **no-fold-of-fold** rule here (deferred from step-3's 3.5c): a folded surface's `host_surface` must, in *this* variant, resolve to a surface whose own `realization` produces ≥1 physical screen (`standalone-screen` or `wizard-split`). If a host is itself folded in this variant, the fold has no physical screen to render onto — set `surface_plan_gap` and route to the step-07 gate.

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

Run the compatibility check from 5.3.5 against the new variant, then author its `surface_plan` + `physical_flow` per 5.3.6 (the new variant gets a full surface_plan keyed by every `LS-NN`, same as a `create`-mode variant; on `add-variant` the `pattern_candidates` map is empty — use 5.3.6's `regenerate-variants` fallback to derive the candidate shortlist from the reused inventory + `pattern-bindings.md` + `_index.md`). Append to `existing.variants` and set the merged list as `variants` for step 6's write.

## 5.5 Distinctness check

After every variant is composed (whether via 5.3 or 5.4), confirm no two variants have identical `dimension_positions` across the full six-dimension key set. On happy path with defaults this is guaranteed (CAREFUL-DEFAULT and POWER-DENSE diverge on every default dimension). On override + 3-variant runs, the mixed variant 3 must differ from both poles on at least one dimension — if not, the architect's polar-pick rule produced an aliased variant; re-derive variant 3 with explicit `0` on the lead dimension and opposite-pole values on the others.

## 5.6 Compose `variants.json` in memory

Assemble the artefact per the schema documented in `framework/agents/blueprint-architect.md > Output`. **Each variant entry now includes its `surface_plan`** (keyed by `LS-NN`, authored at 5.3.6; the per-surface shape is canonical in `framework/assets/wireframes/realization-strategies.md > Section 2`) **and its `physical_flow`** string (derived at 5.3.6 F). These are nested inside each `variants[]` entry — **do not add a new top-level field** for them (the comparator's known-schema contract caps the top-level field set; only the optional `augmented_by` may appear above `variants`). **Each variant entry also carries `posture` + `posture_label`** (authored at 5.3.4; both `null` when no posture was bound) — per-variant fields alongside `design_philosophy`, not new top-level fields.

**Baseline note.** When every surface in a variant is realized `standalone-screen`, each `surface_plan` entry has exactly one `physical_screens[]` element reproducing the pre-realization `S-NN` / `screen-NN-slug.html` names, and the variant's `physical_flow` equals the blueprint's logical flow with `LS-NN` rewritten to `S-NN` — i.e. byte-for-byte the pre-realization shape.

When step 2.6 cached one or more analyses with non-`upstream-only` roles, add an `augmented_by` field at the top level listing each consumed analysis as an audit trail (the comparator's index.html § Variant metadata cards surface this; the variant-generator does not consume it):

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
