---
description: Generate parallel low-fi interactive HTML wireframe variants for a scope of requirements.md, with full traceability and a cross-variant trade-off comparison.
---

Launch the wireframe orchestrator at `framework/orchestrators/wireframe-orch.md`.

Follow the orchestrator exactly — run the four stages in the prescribed foreground:

1. `framework/skills/scope-selector.md` — capture which requirement IDs are in scope; write `blueprints/<scope-slug>/scope.json`.
2. `framework/agents/blueprint-architect.md` — produce `blueprints/<scope-slug>/blueprint.md` (screen inventory + flow + scope→screen trace, **no pattern bindings**) and `wireframes/<scope-slug>/variants.json` (persona-bound variant configurations; cardinality default 2, max 3). Fires a conditional gate only when self-validation flags conflicts, AI-SUGGESTED pattern-coverage gaps, or bijection violations.
3. `framework/agents/wireframe-variant-generator.md` — invoked in parallel, one Agent tool call per variant (cap 4), each producing `wireframes/<scope-slug>/<VARIANT>/{wireframes.html, screen-NN-*.html, wireframe-ds.css, manifest.json, variant-position.json}`.
4. `framework/agents/wireframe-comparator.md` — read only the JSON sidecars + `blueprint.md`; write `wireframes/<scope-slug>/comparison.html` and `wireframes/<scope-slug>/index.html`. Drift detection between declared positions and rendered pattern picks.

Honour the prerequisite gate (`requirements/requirements.md` present + non-empty), the startup overwrite gate (per scope slug — shared `blueprints/<slug>/` + private `wireframes/<slug>/`), the step-0b RF-05 context-bloat preflight, the conditional design-brief gate, and the handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator.

The pipeline writes only to `wireframes/<scope-slug>/**`, with one documented cross-pipeline exception inherited from the shared `blueprint-architect.md` agent: writes to `blueprints/<scope-slug>/{scope.json, blueprint.md}`. The cross-pipeline `blueprints/` directory is shared with a future `/prototype` pipeline by design.

The final artefacts are:
- `wireframes/<scope-slug>/index.html` — scope landing (links every variant + comparison).
- `wireframes/<scope-slug>/comparison.html` — dimension × variant trade-off matrix sourced entirely from JSON sidecars.
- `wireframes/<scope-slug>/<VARIANT>/` — per-variant directory of screen HTMLs (each linked to the shared low-fi `wireframe-ds.css`) with every interactive element carrying a `data-src` attribute traceable to a requirement ID.
