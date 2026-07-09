# Input Safety

Behavioural invariants governing the framework's treatment of files under the consultant-dropped input folder (`input_dir`, canonically `input/`). Files in `input/` are **consultant-owned source material**: the framework reads them, derives from them, and — in exactly two named, consultant-initiated resets — deletes its *own* generated derivatives, but it never destroys what the consultant placed or authored there.

Read by every pipeline that touches `input/`. This file is the canonical home of the "never delete consultant inputs" rule; other files (the reset orchestrators, the input-handler, the input-consumers) reference an `IS-NN` ID rather than re-deriving the policy.

Add new invariants by appending; never renumber.

## IS-01 — Consultant input files are never deleted or overwritten by the framework

Files under `input/` are consultant-owned source material. No orchestrator, agent, or skill may delete, move, or overwrite any of the following:

- raw dropped source files of any format (`.md`, `.txt`, `.docx`, `.xlsx`, `.pptx`, `.pdf`, images, vectors, …);
- the `*.stadium` pointer file and every path under a dropped Stadium 6 application folder (read-only to the extractor — `framework/agents/stadium-ingestor.md`);
- `/resolve-review` outputs (`input/<stem>-<date>.md`, written additively — `framework/agents/resolve-review-drafter.md`);
- any file the consultant hand-edited, including hand-edits to generated Stadium assets (`input/<AppName>.stadium-assets/*.md`) or to a `*.converted.md` sibling.

These are deleted only by the consultant, manually. This consolidates the guarantees already stated locally at `framework/agents/input-handler.md` (Anti-Patterns), `framework/orchestrators/requirements-orch.md` (reset), and `framework/agents/resolve-review-drafter.md` (Anti-Patterns).

## IS-02 — Excluding or skipping a file is not deleting it

When a pipeline is instructed to **leave a file out**, "leave out" means *do not read it / do not include it in the artefact* — the file stays on disk, untouched. It never means delete or move. This covers every leave-out mechanism:

- an excluded manifest row (`framework/shared/input-exclusions.md`, `IX-01..IX-04`) — the path never becomes a manifest row;
- an `Unsupported`-tier row skipped under the Read-path resolution rule (`framework/skills/build-source-manifest.md`), recorded in the reviewer/analyser's **skipped roster** with a reason;
- an `irrelevant-*` diagnostic in an analysis (a file that was read but yielded nothing in-domain).

A review or analysis records the left-out file in its diagnostics / skipped roster and moves on. It has no mechanism, and no authority, to delete an input file.

## IS-03 — The only permitted `input/` deletions are two named generated-derivative resets

Exhaustively, the framework deletes under `input/` in exactly two places, both consultant-initiated, both git-checkpointed first, and both removing **only files the framework itself generated**:

- **`/requirements` reset** — deletes `input/*.converted.md` conversion siblings (`framework/orchestrators/requirements-orch.md`). Backed by the `Bash(rm -f input/*.converted.md)` allow-entry in `.claude/settings.json`.
- **`/ingest-stadium` re-ingest** — deletes `input/<AppName>.stadium-assets/` (`framework/orchestrators/ingest-stadium-orch.md`), only on the consultant's explicit "Re-ingest" choice at the startup gate.

Neither touches a consultant-dropped original or a consultant-authored file (IS-01). Any deletion under `input/` outside these two is a defect.
