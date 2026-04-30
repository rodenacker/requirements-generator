<!-- ROLE: asset. STATUS: stub — author during phase-1 build-order step 1. -->

# taxonomy-goals.md

**Purpose:** Defines what a User Goal is in v7b — a tuple of `{objective, context {frequency, expertise, stakes / error-cost}, quality dimension}` — plus the quality-signal phrase → trade-off-position mapping table and the goal-kind hierarchy (top-level / sub-level / interaction-level).

**Used by:**
- `framework/agents/requirements-drafter/agent.md` — when populating §User goals.
- `framework/agents/requirements-qa/agent.md` — when probing goal-related ambiguity.
- `framework/skills/rate-against-dimensions.md` — quality-signal mapping.
- `framework/agents/design-spec-drafter/agent.md` — goal-to-screen mapping (top-level → screen, sub-level → view/organism, interaction-level → behaviour on atom/molecule).
- `framework/assets/template-requirements.md` — referenced for §3 User goals shape.
- `framework/assets/references/user-goal-trigger-reference.md` — supplies conceptual seed.

**How used:** Loaded by every agent that touches user goals. The quality-signal mapping is the operational link between consultant-language inputs and trade-off-dimension positions.

> Content TBD per `plan/v7b-Brief.md > §taxonomy-goals.md`.
