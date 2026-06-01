# step-01-activate

**Goal:** Enter the generation stance and load the build instruction.

1. Load `framework/assets/persona-llm.md`, then `framework/assets/characters/prototype-generator.md`.
2. Re-affirm **write isolation**: this agent (driver) and its sub-agents write only under `prototypes/**` (plus orchestrator-owned `framework/state/timing.ndjson` appends). Never write `framework/`, `requirements/`, `blueprints/`, `input/`.
3. Read `prototypes/.specs/<name_slug>/design-spec.md` (the finalised spec) and `blueprints/<scope_slug>/blueprint.md` (logical surfaces + per-surface **Property closed sets** — the anti-fabrication source of truth). Capture `prototype_identity` (name_slug, scope_slug, posture, dimension_positions, primary_persona) from the orchestrator.
4. Confirm the app is scaffolded (`prototypes/.scaffold.json` present). If absent, this agent was mis-sequenced — return `failed {reason: "app not scaffolded"}` (the orchestrator runs Step F1 first).

Proceed to `step-02-read-spec.md`.
