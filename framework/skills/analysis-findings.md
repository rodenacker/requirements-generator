<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 10. -->

# analysis-findings.md

**Purpose:** Synthesise an analysis output back into the requirements-template context — what new information the analysis surfaces, what it confirms, what it contradicts. Presents findings to the consultant for the per-analysis Apply / Dismiss decision.

**Inputs:** an analysis file from `artifacts/requirements/analyse-requirements/<method>.<ext>`, current `requirements.md`, the analysis's reference asset.

**Outputs:** structured findings list with: section in `requirements.md` it relates to, what the analysis says, type (additive / confirmatory / contradictory), suggested resolution.

**Used by:** `framework/orchestrators/analyse-requirement-orch.md` — step 4.

**Used how:** Runs once per analysis after the analyser agent completes. Output drives the per-analysis four-option menu (Apply / Dismiss / Run another / Done).

> Content TBD per `plan/v7b-Brief.md > §/analyse-requirement > step 4`.
