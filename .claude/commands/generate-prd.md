---
description: Run the generate-PRD pipeline (draft → resolve → merge) end-to-end. Produces a human-audience Product Requirements Document at prd/prd.md.
---

Launch the generate-PRD orchestrator at `framework/orchestrators/generate-prd-orch.md`.

Follow the orchestrator exactly — run the four agents in the prescribed order:

1. `framework/agents/input-handler.md` — wait for the source manifest to be accepted.
2. `framework/agents/prd-drafter.md` — wait for the draft to be accepted.
3. `framework/agents/prd-resolver.md` — wait for the last question to be answered (or accept-all-remaining).
4. `framework/agents/prd-merger.md` — wait for the merged PRD to be accepted.

Honour every handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The final artefact is `prd/prd.md`.

This pipeline is fully independent of `requirements/requirements.md` — it reads only the shared input manifest and the files under `input/`. It can run before, after, or alongside `/requirements` without state collision (each pipeline has its own progress file).
