<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 9. -->

# map-use-cases-to-ui.md

**Purpose:** Translate a Use Cases map (`analyses/USE-CASES/use-cases-map.html`) into UI inventory entries: each main-flow step becomes a screen / state transition; each extension becomes a branch; each precondition becomes a guard on the entry transition; each success guarantee becomes an acceptance assertion on the exit transition; each minimal guarantee becomes a recovery invariant; the trigger becomes the entry condition.

**Inputs:** `analyses/USE-CASES/use-cases-map.html`, `assets/taxonomy-screens.md`.

**Outputs:** UI inventory rows for the design spec — one flow per `user-goal` UC, with branches per extension, guards per precondition, and acceptance entries per success guarantee. `summary` UCs map to multi-flow orchestrations; `subfunction` UCs map to shared partial flows reusable across screens.

**Used by:** `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when the Use Cases analysis is present. Combines with `map-ooux-to-ui.md` (objects → screen-taxonomy) and `map-jtbd-to-ui.md` (jobs → primary-task weighting) via the accrue-all pattern: object inventory from OOUX × actor-task weighting from JTBD × procedural flow from Use Cases.

> Content TBD per `plan/v7b-Brief.md > §Analyses > Downstream consumption`.
