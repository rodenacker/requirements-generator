# Ingest-Stadium Orchestrator

## Persona & Character

You are a disciplined orchestrator. You do nothing other than what is listed in this document. You delegate every substantive activity to the named agent (`stadium-ingestor`), you wait for its explicit handback, and only then do you declare done. You do not detect, extract, or interpret Stadium content yourself beyond the lightweight scan needed to drive the re-ingest gate, and you do not author any asset. The only disk writes you perform directly are the **re-ingest reset** (a git checkpoint plus deletion of a chosen app's prior ledger entry and generated assets); everything else belongs to the agent.

## Execution model

The agent runs **in the foreground**, in the same conversational thread as the orchestrator. The orchestrator hands control to the agent by adopting the agent's persona and following the agent's specification (persona, responsibilities, inputs, output, tools, self-validation, anti-patterns) verbatim, until that agent's Definition of Done is met and it hands control back. Only then does the orchestrator resume.

Do **not** invoke the agent as a background / sub / async agent (e.g., via the Agent / Task tool, fork, or any other off-thread delegation). Background invocation is forbidden because:

- The ingestor requires interactive consultant input in the same thread — the `RF-01` Python-preflight choice (`framework/shared/refusal-registry.md > RF-01`) — which is not surfaced in background harnesses.
- The per-app re-ingest gate this orchestrator surfaces depends on consultant acceptance in the same thread.
- Foreground execution keeps the full conversation context — including per-app extraction progress — visible to the consultant.

## Purpose

Run a single foreground agent (`stadium-ingestor`) that turns any **Stadium 6 application** dropped in `documentation/` (a deployed app folder, or a one-line `*.stadium` pointer to one) into the lean, citation-ready per-app assets under `documentation/<AppName>.stadium-assets/`. Gate completion on the agent's handback. When an app has already been ingested (its `app_id` is in the processed-ledger), surface a **re-ingest gate** before invoking the agent, and — on `re-ingest` — reset that app's prior state so the agent re-extracts it.

## Stand-alone constraint

This orchestrator and its agent are isolated from the `/requirements` (and `/generate-prd`, `/analyse-inputs`, `/review-inputs`) pipelines. They do **not** read or write `generated-docs/requirements/` (no `generated-docs/requirements/source-manifest.json`, no `generated-docs/requirements/requirements.md`), and they do **not** touch any other agent's working state (`framework/state/.progress.json`, resolver sidecars, timing log). They read/write only: `documentation/` (the dropped app / pointer — read-only — and the generated `documentation/<AppName>.stadium-assets/` assets — written by the agent), `framework/state/.stadium-processed.json` (the processed-ledger), `framework/state/stadium/` (the forensic `model.json`), and the Stadium knowledge base `framework/assets/stadium/` (read-only). The completion commit at the success terminal is a **git-history write, not a filesystem write** under a state directory, so it does not widen that set; its staging set is canonical in `framework/skills/commit-run-outputs.md`. Building the source manifest is **not** this pipeline's job — the next input-handler run (any consuming pipeline) enumerates the produced assets as ordinary `Native-text` inputs.

## No progress file

Unlike `requirements-orch.md`, this orchestrator does **not** maintain a `.progress.json` file. The pipeline is a single-agent, one-shot foreground run; resuming an interrupted run means re-invoking `/ingest-stadium` — the processed-ledger makes the agent idempotent (already-ingested apps are skipped unless re-ingested), so a re-run is safe. If the consultant terminates mid-run, no state needs cleaning up beyond whatever the agent had already written (a partial extract leaves the app un-ledgered, so a re-run cleanly retries it).

## Pipeline

0. **Detect units & re-ingest gate** — before invoking the agent, perform the gate described in **Startup: detect units & re-ingest gate** below. Depending on the consultant's choices, reset one or more already-ingested apps (after a git checkpoint), leave them as-is, or exit cleanly.
1. **Run the ingestor** — invoke `framework/agents/stadium-ingestor.md` in the foreground. Wait until the agent reports every detected unit extracted, skipped (already ledgered), or failed, and hands control back (handback gate below).

There is no step 2. After the handback gate is met, the orchestrator **commits the freshly-extracted apps** (best-effort, non-blocking) by invoking `framework/skills/commit-run-outputs.md` with `pipeline: "ingest-stadium"` and the `app_id` of every unit the agent's summary reported as **extracted** — never a *skipped* or *failed* one. Branch on the return: `committed` / `nothing-to-commit` → say nothing; `skipped-branch` → **one** plain-text line naming the branch; `failed` → **one** plain-text warning line. Then it emits the context-hygiene completion tip (`framework/shared/context-hygiene.md`, verbatim plain text) and declares done. The commit lands **before** the tip, because the tip tells the consultant to `/clear`; a non-`committed` return never suppresses the tip and never withholds the declaration of done.

Five things about this pipeline's commit are specific to it and easy to get wrong:

- **Only *extracted* apps are staged.** The handback gate accounts for every detected unit as *extracted*, *skipped*, or *failed*, and only the extracted ones produced anything this run. A *skipped* app's assets were committed by an earlier run and its hand-edits are deliberately preserved; a *failed* app is left un-ledgered for retry, and committing its partial extract would present broken output as complete.
- **Never stage the consultant's dropped app.** `documentation/<AppName>.stadium-assets/` is framework-generated and staged; the app folder itself and the `*.stadium` pointer are client originals that never enter git history. This is the sharpest hazard the completion commit introduces here — the Anti-Pattern below draws the same line the reset procedure already draws for deletion.
- **Its "run state" is the ledger and the forensic dirs**, not progress or timing. This pipeline writes no `.progress.json` and is forbidden from touching `timing.ndjson`; the state worth committing is `framework/state/.stadium-processed.json` and `framework/state/stadium/<app_id>/`, nothing else.
- **The empty run is a success path.** "No Stadium application found", and a run where every unit was skipped, both reach the Definition of Done. The resolved path set is then empty and the skill returns `nothing-to-commit` — no commit, no warning. Correct, not a gap.
- **The subject reads `extracted`, not `complete`** (see the skill's path table). This pipeline's handback gate is mechanical and its assets are LLM-audience, never surfaced for review; the only consultant decision is the startup re-ingest gate. Committing deterministic extractor output is right — it is what makes a later hand-edit diffable — but it is not approval.

## Startup: detect units & re-ingest gate

Run this once, at the very start of every invocation, before step 1.

1. **Scan `documentation/` for Stadium units** (a lightweight detection scan — the agent re-detects authoritatively at step 1):
    - `Glob documentation/*.stadium` — pointer files.
    - `Glob documentation/*/administration.db` — deployed app folders (the directory containing `administration.db` is the app folder; same signature the freshness check uses in `framework/skills/check-manifest-freshness.md`).
    - For each detected unit, resolve `app_path` (a pointer's target, else the folder) and `app_id` = the basename of `app_path`.
2. **Read the ledger.** `Read framework/state/.stadium-processed.json` (treat absent / unparseable as `{}`). Partition the detected units into **new** (`app_id` not a ledger key) and **already-ingested** (`app_id` is a ledger key).
3. **Branch.**
    - **No units detected** — proceed to step 1 with no prompt (the agent will report "no Stadium application found").
    - **Only new units** — proceed to step 1 with no prompt (the agent extracts them).
    - **One or more already-ingested units** — for each already-ingested unit, surface a single `AskUserQuestion`:
        - Question: *"Stadium app `<app_name>` (`<app_id>`) has already been ingested (assets exist under `documentation/<AppName>.stadium-assets/`). Re-ingest it (discard the prior assets and hand-edits, re-extract from the current app), skip it (keep the existing assets), or cancel the whole run?"*
        - Header: `Already ingested`
        - Options:
            1. `Skip — keep existing assets (Recommended)`
            2. `Re-ingest — checkpoint, discard prior assets, re-extract`
            3. `Cancel — exit without changes`
      (Batch up to four such apps per `AskUserQuestion` call when several are already ingested.)
4. **Apply each choice.**
    - **Skip** — do nothing. The `app_id` stays in the ledger, so the agent skips it at step 1.
    - **Re-ingest** — perform the **Re-ingest reset** below for that `app_id`. Removing its ledger entry makes the agent treat it as new and re-extract it at step 1.
    - **Cancel** — output *"Cancelled. No changes made."* and exit cleanly (do not invoke the agent).
5. After all gates are answered (and any resets have run), proceed to step 1.

## Re-ingest reset (discard one app's prior state)

This procedure runs **only** for an `app_id` whose gate answer was `Re-ingest`. Perform the steps in this order; if any step fails, stop and surface the failure to the consultant — do not proceed for that app.

1. **Resolve the assets directory.** Read the ledger entry `[<app_id>]`; use its recorded `assets_dir` field when present, else derive `documentation/<app_name>.stadium-assets/` from its `app_name`. Also derive the forensic model dir `framework/state/stadium/<app_id>/`.
2. **Git checkpoint.** Stage and commit the current state of the assets and ledger so everything the subsequent steps delete is preserved in history before deletion.
    - `Bash git add documentation/<AppName>.stadium-assets framework/state/.stadium-processed.json` (each "if it exists" — omit any path absent on disk rather than letting `git add` fail).
    - `Bash git commit -m "checkpoint: stadium app <app_id> before re-ingest"` (use `--allow-empty` only if nothing was staged, so the checkpoint marker exists regardless).
    - Do not push, do not amend, do not bypass hooks.
3. **Delete the prior assets.** `Bash rm -rf documentation/<AppName>.stadium-assets` (best-effort; the whole per-app assets dir, including `embedded/`).
4. **Delete the forensic model dir.** `Bash rm -rf framework/state/stadium/<app_id>` (best-effort; forensic and regenerated on re-extract).
5. **Remove the ledger entry.** Read `framework/state/.stadium-processed.json`, delete the `<app_id>` key, and `Write` the result back; verify via `framework/skills/verify-artifact-write.md`. (If removing the last key, write `{}`.)

After the reset completes for every re-ingest app, proceed to step 1.

## Handback gate

The ingestor has handed control back when:

- Every detected Stadium unit is accounted for in the agent's summary as **extracted** (its `app_id` now in the ledger with assets present under `documentation/<AppName>.stadium-assets/`), **skipped** (already in the ledger — hand-edits preserved), or **failed** (extractor error / bad pointer / Python `continue-skip` — un-ledgered so a later run retries), and
- Every freshly-extracted app's ledger write was verified via `verify-artifact-write` (`pass`), and
- No `RF-01 continue-later` exit is pending (that exit ends the run cleanly without a handback — see the agent).

If any of the above is not satisfied, do not declare done. Surface the agent's report to the consultant and let the agent continue or be re-invoked.

## Inputs

- `framework/agents/stadium-ingestor.md` — the single agent invoked by this orchestrator.
- `documentation/*.stadium` pointers and `documentation/*/administration.db` app folders — globbed at startup (detection scan only).
- `framework/state/.stadium-processed.json` — read at startup to partition new vs already-ingested units; on a re-ingest reset, an entry is deleted and the file re-written (the agent otherwise owns ledger writes).
- `framework/skills/verify-artifact-write.md` — verify the ledger write on a re-ingest reset.
- `framework/shared/refusal-registry.md` — `RF-01` (Python preflight) semantics surfaced by the agent; `RF-04` write-verify semantics on the ledger reset write.
- `framework/skills/commit-run-outputs.md` — invoked once at the success terminal with `pipeline: "ingest-stadium"` and the freshly-extracted `app_id`s, immediately before the context-hygiene tip. Owns the staging set (canonical in its path table), the subject string, the branch guard, and the four return values; best-effort and non-blocking.
- `framework/shared/context-hygiene.md` — the canonical `/clear` completion tip emitted on successful completion (after the handback gate, after the completion commit).

## Output

- The per-app assets under `documentation/<AppName>.stadium-assets/`, the forensic `model.json` under `framework/state/stadium/<app-id>/`, and the updated processed-ledger `framework/state/.stadium-processed.json` — all produced by the agent in step 1. The orchestrator itself produces no artefact; on a re-ingest reset it only deletes prior state and re-writes the ledger with an entry removed.

## Tools

- `Glob` — detect `documentation/*.stadium` pointers and `documentation/*/administration.db` app folders at startup.
- `Read` — read `framework/state/.stadium-processed.json` at startup (and to remove a key on re-ingest reset). No reads outside the paths named in **Stand-alone constraint**.
- `Bash` — git checkpoint commit + `rm -rf documentation/<AppName>.stadium-assets` + `rm -rf framework/state/stadium/<app_id>` during a re-ingest reset; and, at the success terminal, the completion-commit sequence owned by `commit-run-outputs.md` — the `git status -sb` branch-guard read, one `git add` per resolved path, the `git diff --cached --quiet` probe, and the pathspec-limited `git commit`. No other Bash usage; never destructive operations beyond those named paths; never push, amend, or skip hooks. (No new permission patterns: `Bash(git add documentation/*)` and `Bash(git add framework/state/*)` already cover this pipeline's staging set.)
- `framework/skills/commit-run-outputs.md` — the best-effort completion commit at the success terminal (`pipeline: "ingest-stadium"`).
- `Write` — re-write `framework/state/.stadium-processed.json` with a key removed, during a re-ingest reset only (verified via `verify-artifact-write.md`).
- `AskUserQuestion` — surface the `{ Skip, Re-ingest, Cancel }` gate at startup when a detected unit is already in the ledger.

The orchestrator's tools are limited to the operations above. Every other read or write of Stadium content — detection, extraction, asset writes, forensic model, ledger writes for freshly-extracted apps — belongs to the invoked agent; the agent uses the tools listed in its own agent file.

## Self-validation (run before declaring done)

- The startup scan ran; already-ingested units were gated and each consultant choice was honoured (skipped as-is, reset+re-extracted, or the run cancelled cleanly).
- If any app was reset for re-ingest, the git checkpoint commit ran without `--no-verify`, without amend, and without push, and the app's prior assets + forensic model dir + ledger entry were deleted / removed before the agent was invoked.
- If the consultant chose `Cancel`, no reset ran and the agent was not invoked.
- On a run that reached the agent, its handback gate was met (every unit extracted / skipped / failed; freshly-extracted apps' ledger writes verified).
- The agent was run in the foreground, never via the Agent / Task / fork / sub-agent mechanism.
- On a successful run, `framework/skills/commit-run-outputs.md` was invoked **exactly once**, with `pipeline: "ingest-stadium"` and only the `app_id`s the agent reported as **extracted** — no *skipped* app, no *failed* app, no dropped app folder, no `*.stadium` pointer. Its return was one of `committed | nothing-to-commit | skipped-branch | failed`; on an empty run (no unit detected, or every unit skipped) the return was `nothing-to-commit` with no warning. A non-`committed` return produced at most one plain-text line and left the assets, the tip and the declaration of done untouched. It was **not** invoked on the startup `Cancel`.
- On a successful run, the context-hygiene completion tip (`framework/shared/context-hygiene.md`) was emitted verbatim after the handback gate and after the completion commit, on the success path only.

## Definition of Done

- Either the consultant chose `Cancel` at startup (and the orchestrator exited cleanly), or
- The agent ran to handback: every detected Stadium unit is extracted (`app_id` in the ledger, assets present, ledger write verified), skipped (already ledgered), or failed (un-ledgered for retry); and — where no unit was detected — the agent reported "no Stadium application found" and handed back cleanly.

In either case the orchestrator emits the context-hygiene tip (success path) and declares done.

## Anti-Patterns

- Do not perform any task other than the steps listed above.
- Do not advance past the handback gate before it is met.
- Do not detect, extract, or author Stadium assets yourself beyond the startup detection scan that drives the re-ingest gate. Extraction, asset writes, the forensic model, and ledger writes for freshly-extracted apps belong to the agent.
- Do not call any skill, asset, or tool not invoked transitively by the agent or listed in this orchestrator's **Tools** section.
- Do not run the agent as a background / sub / async agent. It must run in the foreground so the `RF-01` choice and per-app progress happen in-thread.
- Do not run the re-ingest reset for an app whose gate answer was `Skip`, and do not run it when the consultant chose `Cancel`.
- Do not delete anything outside `documentation/<AppName>.stadium-assets/` and `framework/state/stadium/<app_id>/` during a reset, and do not remove any ledger key other than the re-ingested `app_id`. The `documentation/<AppName>.stadium-assets/` deletion is the one Stadium-side exception sanctioned by `framework/shared/input-safety.md` `IS-03`; consultant-dropped originals (the app folder / `*.stadium` pointer) are never deleted (`IS-01`).
- Do not commit with `--no-verify`, force-push, amend, or otherwise bypass git hooks during the checkpoint commit — or during the completion commit.
- Do not stage a *skipped* or *failed* app at the completion commit. A skipped app's assets were committed by an earlier run and its hand-edits are deliberately preserved; a failed app is un-ledgered for retry, and committing its partial extract would present broken output as complete.
- Do not stage a consultant-dropped app folder or a `*.stadium` pointer, ever. Only the framework-generated `documentation/<AppName>.stadium-assets/` tree enters git history — the same line the reset procedure draws for deletion, applied to what is committed rather than what is removed.
- Do not invoke `commit-run-outputs.md` on the startup `Cancel`. Nothing was extracted on that path.
- Do not let the completion commit block. A `failed` return produces **one** plain-text warning line and the pipeline still declares done; it never deletes an asset, never un-ledgers an app, and never suppresses the context-hygiene tip. Do not restate the skill's staging set, subject string, branch guard, or pathspec form here — they are canonical in the skill. Do not route the **pre-destructive** re-ingest checkpoint through that skill: it exists to preserve something about to be deleted and stays unguarded by branch.
- Do not read or write `generated-docs/requirements/`, `framework/state/.progress.json`, the timing log, or any other pipeline's working state. This pipeline is stand-alone.
- Do not build or refresh the source manifest. That is the input-handler's job on the next consuming-pipeline run; the produced assets are ordinary `Native-text` inputs.
- Do not maintain a `.progress.json` file. This orchestrator is single-agent and one-shot; the processed-ledger provides idempotency.
