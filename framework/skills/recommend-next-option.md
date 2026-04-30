<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 3 or 5. -->

# recommend-next-option.md

**Purpose:** Reusable recommendation skill called by every orchestrator before surfacing a multi-option menu. Produces the Unicorn's recommended option together with a rationale grounded in the current state — never silent, never neutral. Includes inline offers for `/analyse` and `/research` as side actions when warranted.

**Inputs:** current stage + state, latest completeness-report findings (counts × severity), the menu's option set, `assets/persona-llm.md`, the current character file.

**Outputs:** recommended option ID + rationale string in the Unicorn's voice, calibrated to the consultant audience (calibration baked in by the author at design time per `plan/audience-profile-consultant.md`; never runtime-loaded). When a side action is warranted, the rationale string includes the offer inline.

**Used by:**
- `framework/orchestrators/requirements-orch.md` — step 5 options menu, detect-rerun two-option prompt.
- `framework/orchestrators/design-orch.md` — step 4 options menu, detect-rerun two-option prompt.
- `framework/orchestrators/analyse-orch.md` — analysis-selector, per-analysis menu.
- `framework/orchestrators/research-orch.md` — scope prompt, per-finding menu.

**Used how:** Single source of truth for recommendation logic. Forward-compat stubs from day 1: (a) analyses-registry expansion beyond the 4 MVP methodologies; (b) research scope guidance.

> Content TBD per `plan/v7b-Brief.md > §Recommendation rule`.
