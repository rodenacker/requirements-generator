---
description: Generate parallel low-fi interactive HTML wireframe variants for a scope of requirements.md, with full traceability and a cross-variant trade-off comparison.
---

Launch the wireframe orchestrator at `framework/orchestrators/wireframe-orch.md`.

Follow the orchestrator exactly — run the four stages in the prescribed foreground:

1. `framework/skills/scope-selector.md` — capture which requirement IDs are in scope; write `blueprints/<scope-slug>/scope.json`.
2. `framework/agents/blueprint-architect.md` — produce `blueprints/<scope-slug>/blueprint.md` (screen inventory + flow + scope→screen trace, **no pattern bindings**) and `wireframes/<scope-slug>/variants.json` (persona-bound variant configurations; cardinality default 2, max 3). Fires a conditional gate only when self-validation flags conflicts, AI-SUGGESTED pattern-coverage gaps, or bijection violations.
3. `framework/agents/wireframe-variant-generator.md` — invoked in parallel, one Agent tool call per variant (cap 4), each producing `wireframes/<scope-slug>/<VARIANT>/{screen-NN-*.html, wireframe-ds.css, manifest.json, variant-position.json}` (no per-variant `wireframes.html` is authored).
4. `framework/agents/wireframe-comparator.md` — read only the JSON sidecars + `blueprint.md` + `scope.json`; write `wireframes/<scope-slug>/index.html` (metadata-only landing: TOC + four sections — scope details, side-by-side screen links, side-by-side variant prose cards, trade-off matrix) and `wireframes/<scope-slug>/_drift.json`. Drift detection between declared positions and rendered pattern picks.

Honour the prerequisite gate (`requirements/requirements.md` present + non-empty), the startup overwrite gate (per scope slug — shared `blueprints/<slug>/` + private `wireframes/<slug>/`), the conditional design-brief gate, and the handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator.

The pipeline writes only to `wireframes/<scope-slug>/**`, with one documented cross-pipeline exception inherited from the shared `blueprint-architect.md` agent: writes to `blueprints/<scope-slug>/{scope.json, blueprint.md}`. The cross-pipeline `blueprints/` directory is shared with a future `/prototype` pipeline by design.

The final artefacts are:
- `wireframes/<scope-slug>/index.html` — **single** consultant-facing landing page, metadata-only (no embedded wireframes). TOC + four ordered sections: §1 Scope details, §2 Wireframes (side-by-side variant columns of screen links, every link `target="_blank" rel="noopener"`), §3 Variant metadata (side-by-side prose cards), §4 Trade-off matrix (dimension × variant table with plain-English labels).
- `wireframes/<scope-slug>/_drift.json` — system file with the full drift detail; the index surfaces only a one-line summary.
- `wireframes/<scope-slug>/<VARIANT>/` — per-variant directory of screen HTMLs (each linked to the shared low-fi `wireframe-ds.css`) with every interactive element carrying a `data-src` attribute traceable to a requirement ID. The `data-src` attributes are agent-facing audit metadata — no visible hover-tooltip exposes them on the consultant-facing screens.
