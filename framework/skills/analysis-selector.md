<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 8. -->

# analysis-selector.md

**Purpose:** Read `assets/analyses/registry.md`, present the MVP-status methodologies to the consultant, accept multi-pick selections.

**Inputs:** `assets/analyses/registry.md`.

**Outputs:** consultant's selected methodologies (one or many).

**Used by:** `framework/orchestrators/analyse-orch.md` — step 2.

**Used how:** Called after the state-check passes. The recommendation skill (`recommend-next-option.md`) surfaces a specific analysis with rationale when the consultant arrived from a completeness-report side-action recommendation; otherwise presents all MVP rows neutrally.

> Content TBD per `plan/v7b-Brief.md > §/analyse > step 2` + §Analyses > Registry & selection.
