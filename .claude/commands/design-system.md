---
description: Run the design-system styler (domain + optional URL → design tokens) end-to-end.
---

Launch the design-system orchestrator at `framework/orchestrators/design-system-orch.md`.

Follow the orchestrator exactly — run the single agent in the prescribed foreground:

1. `framework/agents/design-system-styler.md` — wait for the design-system document to be accepted.

Honour the startup gate (overwrite / keep / cancel) and the handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The agent is stand-alone — it does not read `requirements/`, `framework/state/`, or `framework/shared/`. The final artefact is `design-system/design-system.md`.
