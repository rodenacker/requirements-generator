<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 6. -->

# detect-rerun.md

**Purpose:** Silent classification of stage state into greenfield / brownfield-partial / brownfield-final, plus detection of input-delta / upstream-delta / uncommitted-mutation signals. No `--rerun` flag — detection is fully silent; the consultant-facing prompt is conversational.

**Inputs:** `.progress.json` for the current stage, `/input/` content hashes vs `source-manifest.md`, upstream main-spec revision markers vs this stage's `last_finalised_at`, current `sha256(spec)` vs `.progress.json > completeness_hash`.

**Outputs:** classification + signals; on brownfield, the two-option prompt body (continue / start fresh).

**Used by:** every stage orchestrator at step 1 (`requirements-orch.md`, `design-orch.md`, `analyse-orch.md`, `research-orch.md`, `style-orch.md`).

**Used how:** First call in every stage. Greenfield → silent proceed to step 1a. Brownfield → two-option prompt routed through `recommend-next-option.md`. Includes the `completeness-hash` check for forcing a fresh completeness report when the spec changed since the last report.

> Content TBD per `plan/v7b-Brief.md > §Rerun detection`.
