---
description: Analyse the requirements through a chosen lens (e.g. OOUX) and write the result under analyse-requirements/.
---

Launch the analyse-requirement orchestrator at `framework/orchestrators/analyse-requirement-orch.md`.

Follow the orchestrator exactly — run the chosen analyser in the prescribed foreground:

1. Prerequisite gate — `requirements/requirements.md` must exist and be non-empty. If absent, exit cleanly with the prerequisite message; do not invoke any agent.
2. Methodology selection — `framework/skills/analysis-selector.md` reads `framework/assets/analyses/registry.md` and presents the `status: mvp` rows.
3. Prior-artefact gate per methodology — Overwrite / Keep / Cancel against `<chosen.output_path>`.
4. The selected analyser agent (e.g. `framework/agents/analyses/ooux-analyser.md`) runs in the foreground — wait for the artefact to be accepted.

Honour the prerequisite gate, the context-bloat preflight (RF-05 analyse-requirement-orch surface variant), the per-methodology prior-artefact gate (Overwrite / Keep / Cancel), and the analyser's handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The pipeline is stand-alone — the orchestrator and analyser do not write to `requirements/`, `design-system/`, `framework/state/`, or `framework/shared/`; the analyser reads `requirements/requirements.md` only and writes a single artefact under `analyse-requirements/<METHOD>/`. For the OOUX MVP, the final artefact is `analyse-requirements/OOUX/ooux-object-map.html`.
