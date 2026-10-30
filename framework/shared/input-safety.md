# Input Safety

Behavioural invariants governing the framework's treatment of files under the consultant-dropped documentation folder (`documentation_dir`, canonically `documentation/`). Files in `documentation/` are **consultant-owned source material**: the framework reads them, derives from them, and — in exactly three named, consultant-initiated resets — deletes its *own* generated derivatives, but it never destroys what the consultant placed or authored there.

Read by every pipeline that touches `documentation/`. This file is the canonical home of the "never delete consultant inputs" rule; other files (the reset orchestrators, the input-handler, the input-consumers) reference an `IS-NN` ID rather than re-deriving the policy.

Add new invariants by appending; never renumber.

## IS-01 — Consultant input files are never deleted or overwritten by the framework

Files under `documentation/` are consultant-owned source material. No orchestrator, agent, or skill may delete, move, or overwrite any of the following:

- raw dropped source files of any format (`.md`, `.txt`, `.docx`, `.xlsx`, `.pptx`, `.pdf`, images, vectors, …);
- the `*.stadium` pointer file and every path under a dropped Stadium 6 application folder (read-only to the extractor — `framework/agents/stadium-ingestor.md`);
- `/resolve-review` outputs (`documentation/<stem>-<date>.md`, written additively — `framework/agents/resolve-review-drafter.md`);
- any file the consultant hand-edited, including hand-edits to generated Stadium assets (`documentation/<AppName>.stadium-assets/*.md`) or to a `*.converted.md` sibling (a hand-edited re-ingestion extract: see `IS-05`);
- re-ingestion extracts (`documentation/*.analysis.md`) — except the guarded replace in `IS-05`.

These are deleted only by the consultant, manually. This consolidates the guarantees already stated locally at `framework/agents/input-handler.md` (Anti-Patterns), `framework/orchestrators/requirements-orch.md` (reset), and `framework/agents/resolve-review-drafter.md` (Anti-Patterns).

## IS-02 — Excluding or skipping a file is not deleting it

When a pipeline is instructed to **leave a file out**, "leave out" means *do not read it / do not include it in the artefact* — the file stays on disk, untouched. It never means delete or move. This covers every leave-out mechanism:

- an excluded manifest row (`framework/shared/input-exclusions.md`, `IX-01..IX-05`) — the path never becomes a manifest row;
- an `Unsupported`-tier row skipped under the Read-path resolution rule (`framework/skills/build-source-manifest.md`), recorded in the reviewer/analyser's **skipped roster** with a reason;
- an `irrelevant-*` diagnostic in an analysis (a file that was read but yielded nothing in-domain).

A review or analysis records the left-out file in its diagnostics / skipped roster and moves on. It has no mechanism, and no authority, to delete an input file.

## IS-03 — The only permitted `documentation/` deletions are three named generated-derivative resets

Exhaustively, the framework deletes under `documentation/` in exactly three places, all consultant-initiated, all git-checkpointed first, and all removing **only files the framework itself generated**:

- **`/requirements` reset** — deletes `documentation/**/*.converted.md` conversion siblings, at any depth (`framework/orchestrators/requirements-orch.md`). Backed by the `Bash(rm -f documentation/*.converted.md)` and `Bash(rm -f documentation/*.media/*.converted.md)` allow-entries in `.claude/settings.json`; a sibling in a deeper folder asks for permission. A name ending in `.converted.md` is input-handler output by definition (`IX-02`), so this deletion never reaches a client original.
- **`/ingest-stadium` re-ingest** — deletes `documentation/<AppName>.stadium-assets/` (`framework/orchestrators/ingest-stadium-orch.md`), only on the consultant's explicit "Re-ingest" choice at the startup gate.
- **Media-directory reconciliation** — deletes orphaned extracted media from `documentation/*.media/` (`framework/agents/input-handler.md`, Step 0 `Refresh` branch), only on the consultant's explicit "Refresh" choice at the manifest-drift gate, and only inside a directory carrying the `.extracted-by-framework` marker. Governed by `IS-04`.

None touches a consultant-dropped original or a consultant-authored file (IS-01). Any deletion under `documentation/` outside these three is a defect.

## IS-04 — Media-directory reconciliation is marker-gated and consultant-initiated

A **media directory** (`documentation/<full-filename>.media/`) holds the images `framework/skills/extract-ooxml-media.md` unpacked from an OOXML input. Its contents are framework-generated derivatives, not consultant source material — but the directory sits inside consultant-owned space, so its reconciliation is fenced twice:

1. **Marker gate.** The framework may only remove files from a directory containing `.extracted-by-framework`, which the extractor writes into every directory it creates. A directory a consultant hand-created at that path carries no marker and is never touched.
2. **Consultant gate.** The removal happens only in the `Refresh` branch of the input-handler's Step-0 manifest-drift prompt — the same shape as the other two `IS-03` deletions. The extractor itself **never** deletes; it reports an `orphans` list and returns.

Within a marked directory, reconciliation removes exactly the paths the current extraction did not produce — an orphaned `img-<hash>.<ext>` and its `*.converted.md` description. It never wipes-and-rewrites: a surviving image keeps its bytes and its description untouched, so a consultant's hand-edit to a frozen description survives every refresh (the Step-5 idempotency guard's guarantee, extended to extracted media).

**Why deletion is permitted here at all.** Extracted media are enumerated as manifest rows, so a stale image is not inert — it is a *live citable source*. If a consultant ships v2 of a document with a screenshot removed and the extracted copy survives on disk, it is re-enumerated, re-described and mined, and `framework/skills/grounding-verifier.md` builds its allowlist from the manifest, so the resulting claim cites a legal source. The artefact would then carry requirements grounded in material the consultant deliberately retracted, with provenance that passes every check the system has, and no artefact anywhere would reveal it. Retention is therefore not the safe default here; **reconciliation protects citation integrity**, which is why this is the one derived-file class the framework is allowed to remove outside a full reset.

Content-hash filenames are what make this safe rather than destructive: an unchanged image re-extracts to a byte-identical name, so only genuinely-removed images are ever candidates for deletion (`framework/skills/extract-ooxml-media.md > Naming`).

## IS-05 — Re-ingestion extracts are overwritten only under the byte-identity guard

A **re-ingestion extract** (`documentation/<method_name>.analysis.md`) is the Markdown projection of an accepted `/analyse-inputs` artefact. It is framework-generated, but it sits in consultant-owned space and a consultant may hand-edit it before the next `/requirements` run — so its replacement is fenced:

1. **Sole writer.** Only `framework/skills/write-reingestion-extract.md` writes a file of this class, and only on the consultant's `Accept & use` choice at an `/analyse-inputs` handback gate. Each write also leaves a **staged copy** beside the analysis artefact (`<dirname(output_path)>/<method_name>.analysis.md`).
2. **Byte-identity guard.** No existing extract → write. An existing extract byte-identical (SHA-256) to its staged copy → replace silently: it is still exactly what the pipeline last wrote. Anything else — a missing staged copy, or differing bytes — means the file was hand-edited or was not written by this pipeline, and is replaced only if the consultant chooses `Replace` at the skill's `Extract` prompt. `Keep mine` leaves both files untouched.

This is the content-identity + consultant-gate shape of `IS-04`, applied to an overwrite instead of a deletion. The framework never **deletes** an extract: `IS-03`'s list is unchanged, and stale extracts are removed by the consultant, manually.
