---
description: Export the finished requirements.md as an application-audience document (generated-docs/export-application/requirements-application.md) — pending amendments folded into the body, then a re-projection that improvises nothing.
---

Launch the export-application orchestrator at `framework/orchestrators/export-application-orch.md`.

Follow the orchestrator exactly — run its agents in the prescribed foreground order:

1. `framework/agents/export-application-folder.md` — **only** when `requirements.md` carries a `## Amendments (pending re-merge)` section. It folds every `AMD-NN` entry into a private copy of the body and writes `generated-docs/export-application/fold-report.md`. An amendment whose anchor cannot be found halts the run before any write.
2. `framework/agents/export-application-exporter.md` — wait for the export to be accepted at its accept/reject gate. The gate points to the fold report when a fold ran.

Honour the prerequisite gate (`generated-docs/requirements/requirements.md` must exist; already-application sources exit; non-final status is a soft gate), the prior-artefact/freshness gate (Keep / Regenerate / Cancel, sha256-anchored, with `Keep` withheld on a rejected artefact), and the handback gate, all as defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The pipeline is stand-alone and stateless — it writes only to `generated-docs/export-application/` (no progress file, no timing events) and reads `generated-docs/requirements/requirements.md` as its sole content input. It never changes `requirements.md`.

The final artefact is `generated-docs/export-application/requirements-application.md`: the finished requirements, with any pending amendments folded in (contradictions replaced, refinements inserted, net-new requirements given the next free ID, every folded unit cited `[SRC: <filename>]` against its amendment document), re-projected to the application audience — §6.10 fixtures swapped to backend-contract pointers, §7 sources relabelled, §0.1 replaced by a short document-scope note, every `[PROTO-ONLY] … [/PROTO-ONLY]` scope span deleted whole, the prototype-invariants appendix removed, and an embedded provenance block (source sha256 + citation legend + known residue + gate outcome) anchoring it to the exact source version.

Prototype framing the transforms cannot handle deterministically — including anything frozen by a `[SRC: …]` citation — passes through **verbatim** and is disclosed in place (a section-local residue note, the `Known residue` provenance row, and a gate warning). It is never rewritten: rewriting text under a retained citation would falsify provenance. The exporter improvises nothing; the fold is the one judgement-bearing step, and every edit it makes is listed in the fold report for the consultant to check before accepting. Residue is a **source** defect — fix it in `generated-docs/requirements/requirements.md` and re-export, which is free. There is no in-gate edit path.

Bundle `generated-docs/requirements/draft-claims.ndjson` with any handoff.
