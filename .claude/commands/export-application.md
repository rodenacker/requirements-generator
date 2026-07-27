---
description: Export the finished requirements.md as an application-audience document (export-application/requirements-application.md) — pure re-projection, zero improvised content.
---

Launch the export-application orchestrator at `framework/orchestrators/export-application-orch.md`.

Follow the orchestrator exactly — run the single agent in the prescribed foreground:

1. `framework/agents/export-application-exporter.md` — wait for the export to be accepted at its accept/reject gate.

Honour the prerequisite gate (`requirements/requirements.md` must exist; already-application sources exit; non-final status is a soft gate), the prior-artefact/freshness gate (Keep / Regenerate / Cancel, sha256-anchored, with `Keep` withheld on a rejected artefact), and the handback gate, all as defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The pipeline is stand-alone and stateless — it writes only to `export-application/` (no progress file, no timing events) and reads `requirements/requirements.md` as its sole content input.

The final artefact is `export-application/requirements-application.md`: the finished requirements re-projected to the application audience — §6.10 fixtures swapped to backend-contract pointers, §7 sources relabelled, §0.1 replaced by a short document-scope note, prototype-scope sentences elided from the five named scope-note blockquotes, the prototype-invariants appendix removed, and an embedded provenance block (source sha256 + citation legend + known residue + gate outcome) anchoring it to the exact source version.

Prototype framing the transforms cannot handle deterministically — including anything frozen by a `[SRC: …]` citation — passes through **verbatim** and is disclosed in place (a section-local residue note, the `Known residue` provenance row, and a gate warning). It is never rewritten: rewriting text under a retained citation would falsify provenance. Residue is a **source** defect — fix it in `requirements/requirements.md` and re-export, which is free. There is no in-gate edit path.

Bundle `requirements/draft-claims.ndjson` with any handoff.
