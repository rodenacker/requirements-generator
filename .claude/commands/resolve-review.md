---
description: Turn selected findings from an existing input-review artefact into a new consultant-approved input document under input/.
---

Launch the resolve-review orchestrator at `framework/orchestrators/resolve-review-orch.md`.

Follow the orchestrator exactly — single-shot, single foreground agent:

1. Artefact picker — printed numbered list of `review-inputs/*/*.html` (friendly exit when none exist; `0` = cancel), then the methodology-map gate against `framework/assets/resolve-review/methodology-map.md`.
2. Stale-draft gate on `resolve-review/resolutions-draft.md` (Discard / Cancel).
3. `framework/agents/resolve-review-drafter.md` runs in the foreground, parameterised by the chosen artefact + methodology key (per-methodology parse anchors and resolution semantics live in the methodology map): parse findings, consultant multi-pick, per-finding resolution with **per-item confirmation of every AI-inferred resolution**, staged draft + accept/revise/restart, then finalise to a NEW dated file under `input/` — never overwriting an existing `input/` file (same-day collisions suffix `-2`, `-3`, …).

Honour the stale-draft gate and the drafter's handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The pipeline is stand-alone — it writes only `resolve-review/resolutions-draft.md` (transient staging) plus the single new `input/<stem>-<date>.md` (the documented cross-pipeline write exception, additive only). No progress file, no timing events, no input-handler invocation; the new file is picked up by the next source-manifest create/refresh.
