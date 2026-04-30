<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 9. -->

# map-ooux-to-ui.md

**Purpose:** Translate an OOUX object map (`artifacts/requirements/analyses/ooux.html`) into UI inventory entries: objects → screen-taxonomy elements + modifiers; CTAs → behaviour entries on appropriate atoms/molecules; relationships → navigation links between screens.

**Inputs:** `artifacts/requirements/analyses/ooux.html`, `assets/taxonomy-screens.md`.

**Outputs:** UI inventory rows for the design spec.

**Used by:** `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when the OOUX analysis is present. Combines with other map-*-to-ui skills via the accrue-all pattern.

> Content TBD per `plan/v7b-Brief.md > §Analyses > Downstream consumption`.
