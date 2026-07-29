# step-06-verify-build

**Goal:** Prove the prototype lints, typechecks, and clicks — the handback gate.

1. Invoke `framework/skills/verify-prototype-build.md` (pass `device_targets` from the step-02 render plan alongside `routes` — it selects the primary Playwright project and adds one bounded layout-integrity run per extra breakpoint) with `app_dir: "prototypes/"`, `name_slug`, `route: "/<name_slug>"`, `routes`, `attempt: 1` (increment on each re-invocation below). The verify skill emits its own per-phase `stage:"verify"` substeps stamped with `attempt`.
   - **`routes`** = **every** route this prototype authored, primary first: the driver-owned routes from `route_map` (root page, wizard sub-steps; folded surfaces contribute **no** route — they render on their host) plus each sub-agent manifest's `route_written`. Both are already in hand — `route_map` from step-02, the manifests from step-04 — so nothing new is derived here. Deduplicate, and keep `"/<name_slug>"` at index 0.
   - Passing the full list is what makes the gate see secondary routes at all. A run that passes only `route` reverts the gate to primary-route-only coverage, which is how a hydration mismatch and three toggle-less shells previously shipped.
2. Branch on the verdict:
   - **`pass`** / **`pass-with-warning`** → proceed to `step-07-handback.md` (carry the warning flag, e.g. `smoke_skipped`, for the landing-updater).
   - **`structured-fail {phase, summary}`** → **bounded retry** (budget N=2, tracked in memory):
     - Diagnose which surface/component the failure implicates (from the error summary + file paths).
     - **Timing:** wrap the regeneration in a `substep_start`/`substep_end` pair (`stage:"generator"`, `substep:"retry-surface"`, `surface:"<LS-NN>"`, `attempt:<N>`), per `prototype-generator.md > Timing log (sub-steps)`.
     - Regenerate only that surface: re-run its sub-agent (step-04 for one surface — which re-authors its components **and**, for a standalone secondary, its own route page) and/or re-compose a driver-owned route (step-05), or fix the driver-owned data layer if the error is there.
     - Re-invoke `verify-prototype-build.md` with the incremented `attempt` and the **same `routes`** (recomputed if the retry re-authored a route file, so a route added or renamed during retry is still covered).
     - If the budget is exhausted with the failure persisting → surface **`RF-12`** (hard, plain-text halt per the registry) and hand back `failed`.
   - **`RF-11 trigger`** (Playwright browsers missing) → return the trigger to the orchestrator, which surfaces `RF-11`. On `skip-smoke-with-warning`, re-invoke the verify skill with the smoke disabled → expect `pass-with-warning`.
3. Never edit generated code just to silence lint/types without fixing the underlying issue; never weaken the smoke.

Proceed to `step-07-handback.md` on a passing verdict.
