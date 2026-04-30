---
description: Run the requirements pipeline (draft → resolve → merge) end-to-end.
---

Launch the requirements orchestrator at `framework/orchestrators/requirements-orch.md`.

Follow the orchestrator exactly — run the three agents in the prescribed order:

1. `framework/agents/requirements-drafter.md` — wait for the draft to be accepted.
2. `framework/agents/requirements-resolver.md` — wait for the last question to be answered (or accept-all-remaining).
3. `framework/agents/requirements-merger.md` — wait for the merged requirements document to be accepted.

Honour every handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The final artefact is `requirements/requirements.md`.
