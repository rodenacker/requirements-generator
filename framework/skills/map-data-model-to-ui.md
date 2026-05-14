<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 9. -->

# map-data-model-to-ui.md

**Purpose:** Translate a Logical Data Model (`analyses/DATA-MODEL/data-model.html`) into UI inventory entries: entities → screen-taxonomy elements (list + detail pairs for `persistent` entities); attributes → form fields and column lists; relationships → cross-screen navigation links; cardinalities → list-vs-detail decisions; business rules → constraints and validation messages; normalisation notes → global decisions (e.g. first-class entity surfaces vs inline summaries).

**Inputs:** `analyses/DATA-MODEL/data-model.html`, `assets/taxonomy-screens.md`.

**Outputs:** UI inventory rows for the design spec.

**Used by:** `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when the data-model analysis is present. Combines with other `map-*-to-ui` skills via the accrue-all pattern. Notation selection in the data-model artefact does not affect the mapping — the mapping consumes the Tier-1 Data Model tables, which are notation-agnostic and always present.

> Content TBD per `plan/v7b-Brief.md > §Analyses > Downstream consumption` and per `framework/assets/analyses/data-model-reference.md > Downstream consumption`.
