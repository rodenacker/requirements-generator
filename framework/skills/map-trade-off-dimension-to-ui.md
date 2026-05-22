<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order (downstream wireframing/prototyping consumption). -->

# map-trade-off-dimension-to-ui.md

**Purpose:** Translate a trade-off dimension matrix (`analyse-requirements/TRADE-OFF-DIMENSIONS/trade-off-matrix.html`) into UI-design guidance entries: per-goal posture cells become bias inputs to downstream wireframing options, and the kept-dimensions list constrains the dimensions design variants are evaluated against.

**Inputs:**

- `analyse-requirements/TRADE-OFF-DIMENSIONS/trade-off-matrix.html` — the artefact written by `framework/agents/analyses/trade-off-dimension-analyser.md`.
- The embedded JSON payload at `<script type="application/json" id="trade-off-scores">` inside that file is the canonical machine-readable contract. HTML parsing is not required — extract the JSON text between the opening and closing script tags and `JSON.parse` it.

**Outputs:** UI design guidance entries for the downstream wireframing / prototyping agents. Two shapes:

1. **Per-goal posture profile** — for each goal, the list of `(dimension_id, score, lean_label, implication)` tuples after the post-pass prune, sorted by `|score|` descending. Downstream agents bias their design options by this profile.
2. **Project-wide dimension constraint set** — the kept-dimensions list (the columns of the matrix). Downstream agents evaluate competing design variants along exactly this axis-set; dimensions dropped in Stage A are not legitimate evaluation criteria for this project.

**JSON payload schema** (canonical — see `framework/agents/analyses/trade-off-dimension-analyser.md > Step 11` for the producer-side contract):

```json
{
  "schema_version": 1,
  "generated_at": "<iso-8601>",
  "requirements_sha256": "<hex>",
  "context": {"domain": "...", "business_goal": "...", "target": "application|prototype", "scope_in_count": N, "scope_out_count": N, "scope_deferred_count": N},
  "kept_dimensions": [{"id": "TD-NN", "name": "...", "pole_a": "...", "pole_b": "...", "raw_score": N, "kept_by": "threshold|cap-top-15|floor-relaxation|consultant-override", "signal_breakdown": [...]}, ...],
  "dropped_dimensions": [...],
  "pruned_dimensions": [...],
  "goals": [{"id": "G-NN", "statement": "...", "quality_signals": "...", "kind": "..."}, ...],
  "cells": [{"goal_id": "G-NN", "dimension_id": "TD-NN", "score": -2..2, "lean_label": "...", "pole_a_hits": [...], "pole_b_hits": [...], "rationale": "...", "cell_kind": "no-signal|balanced|null"}, ...],
  "guidance": {"G-NN": [{"dimension_id": "TD-NN", "lean_label": "...", "implication": "..."}, ...], ...}
}
```

**Used by:** downstream wireframing / prototyping agents that author design-option variants per goal. Called when the trade-off-dimension analysis is present at the canonical `output_path`. Combines with other `map-*-to-ui` skills (OOUX object map, JTBD job map, user journeys) via the accrue-all pattern: each map skill contributes a slice of the design-time evidence pack.

> Content TBD. The full procedure for translating each per-goal posture into concrete wireframe variants and evaluation criteria will be written when the downstream wireframing agent is built. Until then, the schema above is the contract: consumers can read the JSON payload directly and bias their decisions even before this skill's procedural body is filled in.
