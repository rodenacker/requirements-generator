<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 9. -->

# map-sequence-diagram-to-ui.md

**Purpose:** Translate a UML 2.5 sequence-diagram catalogue (`analyse-requirements/SEQUENCE-DIAGRAM/sequence-diagram.html`) into UI inventory entries: scenarios → screen-flow sequences (each `primary` scenario becomes an ordered list of screen transitions); external-system participants → UI integration points (loading states, error banners, retry CTAs, timeout messages); `alt` branches → error-state UI variants (e.g., the `payment failure` branch becomes a dedicated error screen or modal); `opt` fragments → conditional UI sections (e.g., dual-approval CTA appears only when the guard holds); `loop` fragments → list/iterative UI patterns (batch operations, retry indicators); cross-scenario participant matrix → component-reuse hints for the design system (a participant used in 5+ scenarios warrants a first-class component).

**Inputs:** `analyse-requirements/SEQUENCE-DIAGRAM/sequence-diagram.html`, `assets/taxonomy-screens.md`.

**Outputs:** UI inventory rows for the design spec.

**Used by:** `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when the sequence-diagram analysis is present. Combines with other `map-*-to-ui` skills via the accrue-all pattern. Scenario selection in the sequence-diagram artefact does not affect the mapping — the mapping consumes the Tier-1 catalogue tables (Scenarios, Participants, Messages, Combined fragments, Cross-scenario participant matrix), which are always present.

> Content TBD per `plan/v7b-Brief.md > §Analyses > Downstream consumption` and per `framework/assets/analyses/sequence-diagram-reference.md > Downstream consumption`.
