# step-06-verify-build

**Goal:** Prove the prototype lints, typechecks, and clicks — the handback gate.

1. Invoke `framework/skills/verify-prototype-build.md` with `app_dir: "prototypes/"`, `name_slug`, `route: "/<name_slug>"`.
2. Branch on the verdict:
   - **`pass`** / **`pass-with-warning`** → proceed to `step-07-handback.md` (carry the warning flag, e.g. `smoke_skipped`, for the landing-updater).
   - **`structured-fail {phase, summary}`** → **bounded retry** (budget N=2, tracked in memory):
     - Diagnose which surface/component the failure implicates (from the error summary + file paths).
     - Regenerate only that surface: re-run its sub-agent (step-04 for one surface — which re-authors its components **and**, for a standalone secondary, its own route page) and/or re-compose a driver-owned route (step-05), or fix the driver-owned data layer if the error is there.
     - Re-invoke `verify-prototype-build.md`.
     - If the budget is exhausted with the failure persisting → surface **`RF-12`** (hard, plain-text halt per the registry) and hand back `failed`.
   - **`RF-11 trigger`** (Playwright browsers missing) → return the trigger to the orchestrator, which surfaces `RF-11`. On `skip-smoke-with-warning`, re-invoke the verify skill with the smoke disabled → expect `pass-with-warning`.
3. Never edit generated code just to silence lint/types without fixing the underlying issue; never weaken the smoke.

Proceed to `step-07-handback.md` on a passing verdict.
