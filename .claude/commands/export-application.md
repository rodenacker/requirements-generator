---
description: Export the finished requirements.md as an application-audience document (export-application/requirements-application.md) — pure re-projection, zero generated content.
---

Launch the export-application orchestrator at `framework/orchestrators/export-application-orch.md`.

Follow the orchestrator exactly — run the single agent in the prescribed foreground:

1. `framework/agents/export-application-exporter.md` — wait for the export to be accepted at its accept/edit/reject gate.

Honour the prerequisite gate (`requirements/requirements.md` must exist; already-application sources exit; non-final status is a soft gate), the prior-artefact/freshness gate (Keep / Regenerate / Cancel, sha256-anchored), the RF-05 context-bloat preflight, and the handback gate, all as defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The pipeline is stand-alone and stateless — it writes only to `export-application/` (no progress file, no timing events) and reads `requirements/requirements.md` as its sole content input. The final artefact is `export-application/requirements-application.md`: the finished requirements re-projected to the application audience — §6.10 fixtures swapped to backend-contract pointers, §7 sources relabelled, the prototype-invariants appendix removed, and an embedded provenance block (source sha256 + citation legend) anchoring it to the exact source version. Bundle `requirements/draft-claims.ndjson` with any handoff.
