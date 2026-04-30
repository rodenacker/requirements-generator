<!-- ROLE: asset. STATUS: stub — author during phase-1 build-order step 1. -->

# constraints.md

**Purpose:** Defines what is in scope (any UI the consultant specifies — screens/forms/navigation/states/auth UI/role-gated UI/etc.) and what is out of scope (technical implementations behind the UI — backend APIs, DB schema, session management, server-side validation, security internals, performance optimisation, DevOps, data migration).

**Used by:**
- `framework/agents/requirements-drafter/agent.md` — refuses to capture out-of-scope material as a requirement; flags consultant requests for out-of-scope items.
- `framework/agents/design-spec-drafter/agent.md` — refuses to write tool-specific tokens, pixel values, CSS classes, server-side concerns.
- `framework/skills/completeness-report.md` — `contradictory` finding when in-scope content references out-of-scope items.

**How used:** Loaded by drafters. Acts as a hard fail-fast guard, not just guidance — out-of-scope content does not get written into specs.

> Content TBD per `plan/v7b-Brief.md > §constraints.md`.
