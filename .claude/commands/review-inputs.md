---
description: Review the raw input documents through a chosen lens and write the result under review-inputs/.
---

Launch the review-inputs orchestrator at `framework/orchestrators/review-inputs-orch.md`.

Follow the orchestrator exactly — run the chosen input-reviewer in the prescribed foreground:

1. Methodology selection — `framework/skills/analysis-selector.md` reads `framework/assets/reviews-inputs/registry.md` and presents the `status: mvp` rows. On `empty-registry`, exit cleanly with the "no input reviews available yet" message.
2. Context-bloat preflight (RF-05 review-inputs-orch surface variant).
3. Manifest preflight — `requirements/source-manifest.json` must exist; if absent, invoke `framework/agents/input-handler.md` in the foreground to build it. The input-handler is shared with `/requirements` and `/analyse-inputs`; on this invocation `progress_path` is `null` (this pipeline does not own a progress file).
4. Prior-artefact gate per methodology — Overwrite / Keep / Cancel against `<chosen.output_path>` (under `review-inputs/<METHOD>/`).
5. The selected reviewer agent (e.g. `framework/agents/reviews-inputs/<method>-reviewer.md`) runs in the foreground — wait for the artefact to be accepted.

Honour the per-methodology prior-artefact gate (Overwrite / Keep / Cancel), the context-bloat preflight, and the reviewer's handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The pipeline is stand-alone — the orchestrator and reviewer write only to `review-inputs/<METHOD>/`; the orchestrator's Step 1 input-handler invocation writes to `requirements/source-manifest.json` and `input/*.converted.md` as a documented exception inherited from the input-handler's contract. No writes to `requirements/requirements*.md`, `requirements/consultant-answers.md`, `requirements/requirements-draft.md`, `design-system/`, `framework/state/`, `framework/shared/`, `analyse-requirements/<METHOD>/`, `analyse-inputs/<METHOD>/`, or `review-requirements/<METHOD>/` (the requirement-doc reviews' scope).

This pipeline ships its framework first; methodologies are added one at a time in follow-up developments. Until the first methodology row's status is flipped to `mvp` in `framework/assets/reviews-inputs/registry.md`, the orchestrator's selector returns `empty-registry` and the pipeline exits cleanly with a "no input reviews available yet" message.
