---
name: step-04-check-pattern-coverage
description: 'Invoke check-pattern-coverage as preflight. Capture verdict and AI-SUGGESTED gaps for the conditional gate. Skipped on non-create modes.'
---

# Step 4: Pattern-coverage preflight

Runs **only** on `mode = "create"`. On `regenerate-variants` and `add-variant`, the blueprint did not change so the prior preflight result is no longer needed for gate decisions; skip this step. **Because this step is skipped on `mode != "create"`, the `pattern_candidates` map it populates (4.2 below) will be empty on those modes — step-05 must therefore derive its own candidate shortlist from the reused inventory + `framework/assets/wireframes/pattern-bindings.md` + `framework/assets/pattern-catalogue/_index.md` when it authors `surface_plan` (see `step-05-compose-variants.md > 5.3.6`'s `regenerate-variants` fallback).**

## 4.0 Drop step-3-only legacy fallback cache

For each entry in `cached_legacy_full_reads[<source-name>]` (populated by `step-02-read-inputs.md > 2.6.2` only on the legacy-fallback branch), check whether the originating selection's `architect_roles` contain any **step-5** role (per the closed-enum partition in `step-02-read-inputs.md > 2.6.1`). If the selection had only step-3 roles, **drop the entry** from `cached_legacy_full_reads` here — step 3 has consumed it; keeping it in memory would bloat steps 4 → 5 for no purpose. If the selection has both step-3 and step-5 roles, keep the entry; step-05's consumers will read it again from the same slot. This eviction is the load-bearing context-cost optimisation for the legacy branch (the sidecar branch incurs no such cost because `cached_projections[<role>][<name>]` is already small).

## 4.1 Call the skill

The blueprint at `<blueprint_output_path>` does not yet exist on disk — step 6 will write it. The pattern-coverage skill, however, reads the **rendered** blueprint to evaluate per-surface viability. To avoid a "skill needs the file before the file is written" deadlock, write the blueprint to disk **before** running the skill:

1. Render the blueprint per the template populated with the in-memory state from step 3.
2. `Write <blueprint_output_path>` with the rendered content.
3. Call `framework/skills/verify-artifact-write.md` with `path = <blueprint_output_path>`, `expected_sha256 = <rendered hash>`, `expected_min_bytes = 256` (a minimal-shape blueprint is comfortably above 256 bytes).
4. On `pass`, call `framework/skills/check-pattern-coverage.md` with `blueprint_path = <blueprint_output_path>`, `mode: "preflight"`.

(This collapses what `framework/agents/blueprint-architect.md`'s workflow description treats as separate "step 3 author" + "step 6 write" actions for the blueprint. The variants.json write remains at step 6.)

## 4.2 Capture the return value

The skill returns `{ verdict, per_screen, ai_suggested_gaps, notes }`. The skill's return keys are unchanged (`per_screen`, `primary_slot.candidate_patterns`); each `per_screen[i].screen_id` is now a **logical surface** ID (`LS-NN`) because the blueprint inventory rows are keyed `LS-NN`. Capture into in-memory state:

- `pattern_coverage.verdict` ∈ `{ ok | borderline | gap }`.
- `pattern_coverage.notes` — the one-or-two-line summary the skill returned (will populate the blueprint's `{{PATTERN_COVERAGE_SUMMARY}}` slot at the re-write below).
- `pattern_coverage.ai_suggested_gaps` — the list of `{ screen_id, requirement_id, description }` gap entries (`screen_id` is an `LS-NN`).
- `pattern_candidates[<LS>]` — for each `per_screen[i]`, capture `per_screen[i].primary_slot.candidate_patterns` into `pattern_candidates[per_screen[i].screen_id]`. This per-surface candidate shortlist is **reused by step-05's `surface_plan` authoring** (`step-05-compose-variants.md > 5.3.6`) so it does not re-run the catalogue match per variant. (On `mode != "create"` this whole step is skipped, leaving `pattern_candidates` empty — step-05 then derives its own shortlist per the fallback noted in the step header and in 5.3.6.)

## 4.3 Re-write the blueprint with the preflight summary slotted in

The first blueprint write at 4.1.2 used a placeholder `{{PATTERN_COVERAGE_SUMMARY}}` ("preflight pending"). With the skill's verdict in hand, replace the placeholder with the actual `pattern_coverage.notes` line and re-write:

1. Re-render the blueprint with the populated `{{PATTERN_COVERAGE_SUMMARY}}`.
2. `Write <blueprint_output_path>` with the re-rendered content.
3. Call `verify-artifact-write` again with the new hash. On `pass`, advance.

This second write is intentional — the alternative (skill writes the blueprint, then we patch it via Edit) introduces a hash-skew risk that the verify skill is specifically designed to catch. Two clean Writes with two verify passes is the safe shape.

## 4.4 Decide gate-firing on verdict

Capture the gate-firing predicate into in-memory state — step 7 owns the actual gate surface.

- `verdict == "ok"` → no gate fires from pattern coverage. Step 7 fires only if bijection or conflicts also flagged.
- `verdict == "borderline"` → no gate fires from pattern coverage alone (per `check-pattern-coverage.md`'s contract). Borderline summaries appear in the blueprint's preflight section for the consultant's awareness but do not interrupt the auto-accept path.
- `verdict == "gap"` → **gate fires** at step 7 regardless of bijection / conflicts. The consultant must accept an `[AI-SUGGESTED]` stub for every gapped surface, narrow scope to remove the gap-causing source, or cancel.

---

**Next:** Read fully and follow `step-05-compose-variants.md`.
