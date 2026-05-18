---
description: Analyse the raw input documents through a chosen lens (e.g. glossary, jtbd, five-whys) and write the result under analyse-inputs/.
---

Launch the analyse-inputs orchestrator at `framework/orchestrators/analyse-inputs-orch.md`.

Follow the orchestrator exactly — run the chosen input-analyser in the prescribed foreground:

1. Methodology selection — `framework/skills/analysis-selector.md` reads `framework/assets/analyses-inputs/registry.md` and presents the `status: mvp` rows. On `empty-registry`, exit cleanly with the "no input analyses available yet" message.
2. Context-bloat preflight (RF-05 analyse-inputs-orch surface variant).
3. Manifest preflight — `requirements/source-manifest.json` must exist; if absent, invoke `framework/agents/input-handler.md` in the foreground to build it. The input-handler is shared with `/requirements`; on this invocation `progress_path` is `null` (this pipeline does not own a progress file).
4. Prior-artefact gate per methodology — Overwrite / Keep / Cancel against `<chosen.output_path>` (under `analyse-inputs/<METHOD>/`).
5. The selected analyser agent (e.g. `framework/agents/analyses-inputs/glossary-analyser.md`) runs in the foreground — wait for the artefact to be accepted.

Honour the per-methodology prior-artefact gate (Overwrite / Keep / Cancel), the context-bloat preflight, and the analyser's handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The pipeline is stand-alone — the orchestrator and analyser write only to `analyse-inputs/<METHOD>/`; the orchestrator's Step 1 input-handler invocation writes to `requirements/source-manifest.json` and `input/*.converted.md` as a documented exception inherited from the input-handler's contract. No writes to `requirements/requirements*.md`, `requirements/consultant-answers.md`, `requirements/requirements-draft.md`, `design-system/`, `framework/state/`, `framework/shared/`, or `analyse-requirements/<METHOD>/` (the requirement-doc analyses' scope).

This pipeline ships its framework first; methodologies are added one at a time in follow-up developments. Until the first methodology row's status is flipped to `mvp` in `framework/assets/analyses-inputs/registry.md`, the orchestrator's selector returns `empty-registry` and the pipeline exits cleanly with a "no input analyses available yet" message.
