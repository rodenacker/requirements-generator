---
name: step-02-read-inputs
description: 'Read the scope manifest, the requirements document, and (on non-create modes) the existing blueprint and variants.json.'
---

# Step 2: Read inputs

## 2.1 Read the scope manifest

```
Read tool: <scope_path>
```

JSON-parse the contents. Capture into in-memory state:

- `scope.scope_slug` — must equal the input parameter `scope_slug`. Mismatch is a structural error: surface plain-text *"Scope-slug mismatch: scope.json carries `{{scope.scope_slug}}` but agent was invoked with `{{scope_slug}}`. Cancelling — re-run scope-selector."* and fail handback. The orchestrator does not write a completed event.
- `scope.sources` — the six categorised lists. Empty categories are valid (the consultant chose to skip them at scope-selector); zero non-empty categories is a structural error (re-run scope-selector).
- `scope.personas_available` — the list of §3 persona names from the requirements doc at selection time.
- `scope.freeform_description` — optional prose (free-form branch) or `null` (structural branch). Used in the architect's notes only.
- `scope.requirements_sha256` — propagated into the blueprint's `REQUIREMENTS_SHA256` slot for drift detection by downstream readers.

## 2.2 Read the requirements doc

```
Read tool: requirements/requirements.md
```

Full read; the orchestrator's prerequisite gate guaranteed it exists and is non-empty.

**Amendments supersession:** if the document carries an `## Amendments (pending re-merge)` section (inserted by `/resolve-review`; canonical shape in `framework/assets/resolve-review/template-addendum.md`), apply its `AMD-NN` entries to every extraction this step and step 3 perform — amendments supersede the base text they name, including the §7 / F-NN property extraction the Properties closed set is derived from (additions extend, removals shrink, renames replace). Note the applied amendments in the in-thread announcement.

**Drift check:** compute the sha256 of the bytes just read. If it does not match `scope.requirements_sha256`, the requirements doc has changed since scope-selection. Surface a structured warning in the architect's in-thread announcement (do **not** fail; the consultant may have intentionally edited the doc): *"⚠ `requirements/requirements.md` has changed since scope-selection (new sha256 `{{actual_sha256}}` vs scope.json `{{scope.requirements_sha256}}`). Proceeding with current requirements; any scope sources no longer present will surface as bijection violations in step 3."*

## 2.3 Locate scope-restricted slices

Walk the requirements doc and locate the lines that reference each ID / name in `scope.sources`. Capture the one-line summary text per ID (typically the first content line under the ID's anchor) into in-memory `scope_summaries[<id>] = "<first-line>"`. Truncate each summary to 120 chars.

## 2.4 Extract §3 personas

Walk `## 3. Target users` and locate every `### <Name>` header. For each, capture:

- `personas[<Name>].name` — the verbatim header text.
- `personas[<Name>].characteristic` — the first one-or-two-line description below the header.
- `personas[<Name>].traits` — heuristic-extracted traits used by `tradeoff-dimensions-registry.md > Section 5`:
    - `frequency` ∈ `{daily | weekly | occasional | first-time}` (extract from copy like "daily high-volume", "occasional", "first-time").
    - `expertise` ∈ `{novice | intermediate | expert}` (extract from copy like "expert", "novice", "trained operator").
    - `role` ∈ `{operator | reviewer | approver | auditor | viewer | admin}` (extract from copy or the persona's name).

Cross-check `personas` against `scope.personas_available` — every persona name in `scope.personas_available` should be in `personas`. A mismatch (e.g. requirements doc renamed a persona) is a structural warning, not a hard fail; surface in-thread and use the requirements doc's current names as authoritative.

## 2.4b Extract §1.8 Application character

Walk `## 1.8 Application character` and capture verbatim into in-memory state:

- `application_character.name_and_statement` — the `**Selected character:**` line's value.
- `application_character.tone_attributes` — the `**Tone attributes:**` line's value.
- `application_character.per_surface_guidance` — the five copy-surface rows (Notifications / Errors / Validation / Confirmations / Empty states), each with Guidance + Example.

Purely mechanical — no inference, no widening. When the section is absent (a requirements.md that predates §1.8), set `application_character = null` and surface a one-line in-thread note: *"no §1.8 Application character — wireframe copy will use a neutral professional voice"*. The Amendments-supersession rule in 2.2 applies to this extraction like every other.

## 2.5 (Non-create modes only) Read prior artefacts

On `mode = "regenerate-variants"`:

```
Read tool: <blueprint_output_path>
```

Capture the screen inventory + flow + sources from the existing blueprint. Re-use the in-memory variables that `step-03-author-blueprint.md` would produce, but skip the authoring logic. Note the existing blueprint's sha256 into in-memory state (will be re-verified at step 7 to confirm step 6 did not overwrite it).

On `mode = "add-variant"`:

```
Read tool: <blueprint_output_path>
Read tool: <variants_output_path>
```

Capture both. The variants.json's `variants[]` list is preserved verbatim through step 5; step 5 surfaces a single new-variant prompt and appends one entry only.

## 2.6 Read supporting analyses (when selected)

**Read protocol.** Selected analyses are consumed via per-method **JSON sidecars** (≤ 20 KB each), not by full-reading the prose `output_path`. The sidecar shape is defined canonically in `framework/assets/analyses/sidecar-schema.md`; the architect reads `architect_projection[<role>]` per-role keyed by the closed enum from `framework/skills/select-supporting-analyses.md`. When a sidecar is absent on disk (one-cycle-deprecation legacy artefacts whose analyser has not yet been updated to emit a sidecar), the architect falls back to a **bounded** full-Read of the prose — see block 2.6.3 — capped at 60 KB by `RF-09`.

If the input parameter `analyses_inputs_path` is non-null **and** the file exists on disk:

```
Read tool: <analyses_inputs_path>
```

JSON-parse the contents. Capture into in-memory state:

- `analyses.scope_slug` — must equal the input parameter `scope_slug`. Mismatch is a structural error (a stale selection from a prior scope leaked into this run): surface plain-text *"Analyses-inputs scope-slug mismatch: analyses-inputs.json carries `{{analyses.scope_slug}}` but agent was invoked with `{{scope_slug}}`. Cancelling — re-run /wireframe so Stage 1b re-captures."* and fail handback.
- `analyses.selections[]` — the consultant's selected supporting analyses; may be an empty array on a `selected-none` capture (the architect runs without analyses).

Skip the remainder of 2.6 entirely on empty selections.

### 2.6.1 Partition selections by role consumer

Before reading any sidecar, classify each `selections[i]` by which step file's roles it serves. This lets step-02 read only what step-03 needs and defer step-05-only roles to step-05.

For each `selections[i]`, compute:

- `step3_roles[i] = selections[i].architect_roles ∩ { "screen-inventory", "screen-inventory-entity-bijection", "screen-flow", "screen-properties-cross-check" }`
- `step5_roles[i] = selections[i].architect_roles ∩ { "variant-philosophy", "variant-dimension-applicability", "per-screen-state-chips", "per-screen-async-states", "per-screen-role-visibility", "per-screen-cta-set", "copy-vocabulary", "feature-presence" }`
- `upstream_only[i] = ("upstream-only" ∈ selections[i].architect_roles)`

Selections with `step3_roles` non-empty are read **at step-02** below. Selections whose only roles are in `step5_roles` are deferred to step-05; only their metadata (path + sidecar pointer + roles) is captured in `pending_step5_selections[]` here.

Selections that are `upstream-only` are recorded into `cached_projections["upstream-only"][<name>] = { "selection": <selections[i]> }` and otherwise ignored at this step and downstream (today: `five-whys`).

### 2.6.2 Read sidecars for step-3 roles

For each `selections[i]` with non-empty `step3_roles[i]`:

1. **Source artefact existence check.** If `selections[i].output_path` is absent on disk, surface plain-text *"Selected analysis `{{name}}` was promised at `{{output_path}}` but is absent on disk. Cancelling — re-run /wireframe so Stage 1b re-captures."* and fail handback. (`RF-04`-class data-integrity halt; the skill verified existence at Stage 1b so absence here means the file disappeared between Stage 1b and this step.)

2. **Sidecar branch.** When `selections[i].sidecar_present == true` **and** the file at `selections[i].sidecar_path` exists on disk:

    ```
    Read tool: selections[i].sidecar_path
    ```

    JSON-parse the contents. Verify:

    - `schema_version == "1"` — mismatch is a structural error; halt plain-text *"Sidecar `{{sidecar_path}}` declares unsupported schema_version `{{actual}}`. Expected `1`. Cancelling — re-run /analyse-requirement to regenerate, then re-invoke /wireframe."*.
    - `method == selections[i].name` — mismatch is a structural error; halt plain-text *"Sidecar at `{{sidecar_path}}` declares method `{{actual}}` but selection names `{{selections[i].name}}`. Cancelling — likely a hand-edited sidecar; re-run /analyse-requirement to regenerate."*.

    **Drift detection (RF-08).** Compute the sha256 of `selections[i].output_path` from disk and compare against the sidecar's `source_sha256`. Mismatch fires `RF-08 stale_analysis_sidecar` per `framework/shared/refusal-registry.md > RF-08` (hard halt; plain-text exit message; no `AskUserQuestion` — there is no in-thread choice when the structured projection has diverged from the consultant-edited prose).

    For each role in `step3_roles[i]`, capture `architect_projection[<role>]` into `cached_projections[<role>][<selections[i].name>]`. Skip a role silently when `architect_projection[<role>]` is absent in the sidecar — the method does not expose that role even though the static mapping declares it (the analyser PR for that method has not yet projected that role; non-fatal).

3. **Legacy fallback branch (no sidecar).** When `selections[i].sidecar_present == false` **or** the sidecar file does not exist on disk:

    - Log `[ANALYSIS-FALLBACK: <selections[i].name>]` to in-memory state for inclusion in the blueprint's Architect notes (`step-03-author-blueprint.md > 3.6`).
    - Measure the on-disk byte size of `selections[i].output_path`.
    - If size > **60 KB**, fire `RF-09 legacy_analysis_too_large` per `framework/shared/refusal-registry.md > RF-09`. The architect surfaces the registry's three-way `AskUserQuestion` and branches per the consultant's choice:
        - `regenerate-and-retry` — halt step-02; surface the regeneration advice in handback. The consultant re-runs `/analyse-requirement <method>` and re-invokes `/wireframe`. The wireframe pipeline does not write to `framework/state/.progress.json`.
        - `proceed-with-bounded-read` — append `(>60 KB; consultant-accepted)` to the existing `[ANALYSIS-FALLBACK: ...]` log and fall through to the bounded-read step below as if the size were within the cap.
        - `cancel` — halt step-02 and fail handback cleanly.
    - When size ≤ 60 KB (or the consultant chose `proceed-with-bounded-read` above):

        ```
        Read tool: selections[i].output_path
        ```

        Capture the full prose content into `cached_legacy_full_reads[<selections[i].name>] = { "format": selections[i].format, "content": <bytes>, "roles": step3_roles[i] }`. Step-03's role-keyed lookup falls through to `cached_legacy_full_reads[<source-name>].content` and applies best-effort role-relevant extraction at consumption time (see `step-03-author-blueprint.md > 3.2c`). The entry is dropped from cache at the step-03 boundary by `step-04-check-pattern-coverage.md`'s preamble (cf. step-04's note on cache eviction) so it does not survive into step-05.

### 2.6.3 Defer step-5-only selections

For each `selections[i]` whose `step3_roles[i]` is empty but `step5_roles[i]` is non-empty: capture only `pending_step5_selections[i] = { "name": selections[i].name, "sidecar_path": selections[i].sidecar_path, "sidecar_present": selections[i].sidecar_present, "output_path": selections[i].output_path, "format": selections[i].format, "step5_roles": step5_roles[i] }`. Do **not** read the sidecar or the prose here; `step-05-compose-variants.md` opens this slot at its preamble and reads each entry via the same sidecar-first / bounded-fallback protocol as 2.6.2 above.

A selection that carries both step-3 and step-5 roles is read at step-02 (block 2.6.2 above) for all its roles — both `step3_roles[i]` and `step5_roles[i]` projections are captured in one read pass. Such selections do **not** appear in `pending_step5_selections[]`.

### 2.6.4 Self-validation

Before advancing to 2.7, verify:

- Every `selections[i]` is reflected in exactly one of: `cached_projections[<role>][<name>]` (for ≥ 1 of its step-3 roles), `cached_legacy_full_reads[<name>]` (when a step-3 role was active and no sidecar existed), `pending_step5_selections[]` (when all its roles are step-5-only), `cached_projections["upstream-only"][<name>]` (when `upstream-only` is one of its roles). No selection was silently dropped.
- No sidecar Read crossed the 20 KB cap (the schema's hard cap — anything larger is a malformed sidecar; surface plain-text *"Sidecar `{{sidecar_path}}` exceeds the 20 KB cap (actual: `{{KB}}` KB). Cancelling — likely a malformed sidecar; re-run /analyse-requirement to regenerate."*).
- `cached_legacy_full_reads[<name>].content` is populated only for selections whose `sidecar_present == false`; no double-read happened (sidecar branch and legacy branch are mutually exclusive).

When `analyses_inputs_path` is null, OR the file is absent on disk, skip block 2.6 entirely and continue to 2.7. The architect runs without consuming analyses (pre-Stage-1b behaviour).

## 2.7 (Legacy fallback) Read trade-off matrix

Only when block 2.6 produced no entry for `trade-off-dimension-analysis` in `cached_projections["variant-dimension-applicability"]` AND no entry in `cached_legacy_full_reads` AND no entry in `pending_step5_selections[]` for the same name (because `analyses_inputs_path` was null/absent OR the consultant did not select trade-off-dimensions at Stage 1b): test whether `analyse-requirements/TRADE-OFF-DIMENSIONS/trade-off-matrix.html` exists on disk. If yes, `Read` it (the file is HTML; extract the per-goal × dimension scoring from its `<table>` body). Use the scoring at step 5 to inform the dimension-applicability filter — goals scoring near the poles on a given dimension reinforce that dimension's applicability. Absent → skip silently; the architect falls back to the heuristic rules in `tradeoff-dimensions-registry.md > Section 2`.

When block 2.6 produced a `trade-off-dimension-analysis` selection (in any of the cache slots above), **skip block 2.7 entirely** — the consultant's explicit selection takes precedence over the legacy existence-conditional read.

---

**Next:** On `mode = "create"`, read fully and follow `step-03-author-blueprint.md`. On `mode = "regenerate-variants"` or `mode = "add-variant"`, skip to `step-05-compose-variants.md` (step 3 is skipped because the blueprint is reused; step 4 is also skipped because the blueprint did not change and the prior preflight result is no longer needed — `variants.json` regeneration is purely a re-composition of trade-off positions and personas, not a re-evaluation of pattern coverage).

**In-memory cache shape consumed downstream:**

- `cached_projections[<role>][<selections[i].name>]` — per-role payload from sidecars per `framework/assets/analyses/sidecar-schema.md`. Keyed by role first so steps 3 and 5 can look up by role uniformly across methods. Step 3 reads roles `screen-inventory`, `screen-inventory-entity-bijection`, `screen-flow`, `screen-properties-cross-check`. Step 5 reads roles `variant-philosophy`, `variant-dimension-applicability`, `per-screen-state-chips`, `per-screen-async-states`, `per-screen-role-visibility`, `per-screen-cta-set`, `copy-vocabulary`, `feature-presence`. Role `upstream-only` is recorded but never consumed.
- `cached_legacy_full_reads[<selections[i].name>]` — full prose content for legacy artefacts without sidecars; populated only at step-02 for selections whose step-3 roles fired, and only when the prose is ≤ 60 KB (or the consultant accepted the `proceed-with-bounded-read` branch of `RF-09`). Step 3 falls through to this slot when `cached_projections[<role>][<name>]` is empty for one of its required roles. Dropped from cache by the step-04 preamble so it does not bloat step-05.
- `pending_step5_selections[]` — metadata-only stubs for selections whose roles are step-5-only (no step-3 roles fired at step-02). Step-05's preamble reads sidecars (or falls back to bounded prose Read per the same protocol as 2.6.2 above) for each pending entry at the moment step-05 begins composition. This deferred-read pattern is the load-bearing context-cost optimisation: step-5-only analyses do not consume any tokens during steps 3 + 4.
