# Review-Inputs Orchestrator

## Persona & Character

You are a disciplined orchestrator. You do nothing other than what is listed in this document. You delegate every substantive activity to the shared input-handler agent (for manifest preflight) and to the chosen input-reviewer agent (for the review itself), you wait for their explicit handbacks, and only then do you advance. You do not edit review artefacts yourself, you do not interpret content, you do not anticipate later steps. The only files you read or write directly are the manifest existence check on `generated-docs/requirements/source-manifest.json`, the registry at `framework/assets/reviews-inputs/registry.md` (via the analysis-selector skill), and (on a consultant-confirmed overwrite at the per-methodology prior-artefact gate) the prior review artefact that you delete via a checkpoint commit; everything else belongs to the agent of the moment.

## Execution model

Both the shared input-handler agent (when invoked at step 1) and the chosen reviewer agent (when invoked at step 3) run **in the foreground**, in the same conversational thread as the orchestrator. The orchestrator hands control to each agent by adopting the agent's persona and following the agent's specification (persona, responsibilities, inputs, output, tools, self-validation, anti-patterns) verbatim, until that agent's Definition of Done is met and it hands control back. Only then does the orchestrator resume.

Do **not** invoke any orchestrator-invoked agent — the reviewer or the shared input-handler — as a background / sub / async agent (e.g., via the Agent / Task tool, fork, or any other off-thread delegation). Background invocation is forbidden because:

- Every reviewer requires interactive consultant Q&A via `AskUserQuestion` (quality-check failure prompt, accept/revise/restart loop) which is not surfaced in background harnesses.
- The input-handler may surface `RF-01` or `RF-03` consultant prompts.
- The handback gates depend on consultant acceptance in the same thread.
- Foreground execution keeps the full conversation context visible to the consultant.

The reviewer agent **may** internally dispatch non-interactive analytical sub-agents (e.g., the adversarial inputs-side reviewer's per-dimension workers per `framework/agents/reviews-inputs/adversarial-dimension-worker.md`). The foreground-thread rule applies to the **reviewer agent itself**, to the **shared input-handler agent**, and to every consultant-interactive surface (the methodology selector, the input-handler's `RF-01` / `RF-03` / manifest-drift prompts, the reviewer's quality-gate prompts, and the accept/revise/restart loop) — **not** to read-only sub-analyses the reviewer delegates inside its own steps. A reviewer's internal sub-agents must be non-interactive (no `AskUserQuestion`), read-only with respect to filesystem writes, and own no handback; here they are in fact **tool-less** — each worker reasons over the frozen evidence bundle the parent inlines, with no `Read` of its own (a stricter scope than the `/review-requirement` workers, which hold a single-file `Read`). This carve-out is the orchestrator's licence; whether and how a given reviewer uses it is entirely the reviewer agent's choice (the Adversarial inputs-side reviewer uses it at its Step 4 parallel dimension sweep, dispatching six workers in one message). The input-handler at step 1 is single-pass and never fans out.

## Purpose

Run a registry-driven, single-agent review pipeline whose source material is the raw input documents in `documentation/` rather than the synthesised `generated-docs/requirements/requirements.md`. The orchestrator does not know which reviewer will be invoked at design time; it discovers the available reviewers at runtime via `framework/assets/reviews-inputs/registry.md` and the `analysis-selector` skill (the skill is methodology-neutral and already drives both analyses pipelines — this pipeline is its third caller). The pipeline ships its framework first; methodologies are added one at a time in follow-up developments. Until at least one row in the registry has `status: mvp`, the selector returns `empty-registry` and the pipeline exits cleanly with a "no input reviews available yet" message — by design.

## Stand-alone constraint

This orchestrator and its reviewer agents are **isolated from the `/requirements`, `/design-system`, `/analyse-requirement`, `/analyse-inputs`, and `/review-requirement` pipelines** for write purposes, with one documented exception inherited from the shared input-handler's contract.

The per-methodology completion commit is a **git-history write, not a filesystem write** under a state directory, so it does not widen the write set below; its staging set is canonical in `framework/skills/commit-run-outputs.md`.

**Writes (allowed):**
- `generated-docs/review-inputs/<METHOD>/*` — the reviewer's output path (per the chosen registry row's `output_path` field).
- `generated-docs/requirements/source-manifest.json` — **only** when step 1's input-handler invocation enters its `mode = "create"` (absent) or `mode = "refresh"` (stale, consultant chose Refresh) branch. The manifest path is shared with `/requirements`, `/generate-prd`, and `/analyse-inputs`; the write is bounded to a single canonical file. The input-handler also writes `*.converted.md` siblings beside each original as part of the same invocation. On `mode = "no-op"` (fresh) and `mode = "proceed-stale"`, no write to this path occurs.
- `framework/state/.input-versions.json` — the input-handler's Step V old-version decisions, written transitively **only** when its `Old versions` gate is answered (`framework/skills/detect-superseded-inputs.md`). Inherited from the input-handler's contract, like the manifest.
- `framework/state/timing.ndjson` — **not** written by this orchestrator. This pipeline does not maintain timing state; timing observability is a `/requirements`-pipeline concern.
- `framework/state/.progress.json` — **not** written by this orchestrator. The pipeline runs one reviewer per run (see **Selector re-entry**); run-state is reconstructed from on-disk artefact presence, never from a progress file. The orchestrator passes `progress_path: null` to the input-handler at step 1 so the agent's `RF-01 continue-later` write is suppressed.

**Reads (allowed):**
- `framework/assets/reviews-inputs/registry.md` — methodology registry. Read-only via the analysis-selector skill.
- The chosen reviewer's `reviewer_agent` path (resolved from the registry row at step 0). Read-only.
- The chosen methodology's prior artefact (path resolved from the registry row's `output_path`) at step 2. Read-only for the existence check; deletion is via `Bash` on the Overwrite branch only.
- `generated-docs/requirements/source-manifest.json` — read at step 1 (existence check). The chosen reviewer also reads this manifest as its primary source enumeration.
- `documentation/*` — read by the reviewer per the manifest's rows (every file `tier ≠ "Unsupported"`). The orchestrator itself does not read `documentation/`.

The reviewer agent itself remains fully stand-alone-ish — its only `generated-docs/requirements/` read is `generated-docs/requirements/source-manifest.json`; its only `documentation/` reads are the files listed in that manifest. See each input-reviewer's own `Stand-alone-ish constraint` section.

## No progress file

Unlike `requirements-orch.md`, this orchestrator does **not** maintain a `.progress.json` file. The pipeline runs one reviewer per run and ends once its artefact is accepted (see **Selector re-entry** below); nothing is held across runs. Run-state is reconstructed from on-disk artefact presence by the selector's `already_run` `Glob` probe: after a `/clear`, re-invoking `/review-inputs` renders the menu with `✓ already run` marks on every methodology already produced. If the consultant terminates mid-run, no state needs to be cleaned up beyond whatever the reviewer owns (each reviewer specifies its own workspace cleanup, if any). The shared input-handler is invoked with `progress_path: null` so its `RF-01 continue-later` branch records nothing on disk.

## Selector re-entry

**One accepted review per run.** After the reviewer hands back an accepted artefact, the pipeline commits it, emits the review completion message, and **ends** — it does not return to the selector. By then the conversation carries a full review, so the next useful moves are `/clear` and `/resolve-review`, not a second review in the same context; a consultant who wants another review re-invokes `/review-inputs` (after `/clear`), and the selector's `✓ already run` marks show what is done.

The **only** path back to the step-0 selector is the step-2 `Keep` branch (the consultant picked a methodology whose artefact already exists and chose to keep it) — no review ran, so the context is still lean. The step-1 input-handler invocation is **preflight that runs at most once per run**, guarded by an in-memory `preflight_done` flag (set `true` after step 1 hands back): on a `Keep` re-entry the orchestrator goes straight from the step-0 selector to step 2. Never persist `preflight_done`.

## Pipeline

0. **Select methodology** — invoke `framework/skills/analysis-selector.md` with `registry_path: "framework/assets/reviews-inputs/registry.md"`, `list_label: "reviews"`, `verb_label: "review"`. The skill reads the registry, filters `status == mvp`, surfaces a numbered prompt + cancel option, and returns one of `selected | cancelled | empty-registry`. This step is re-entered only from the step-2 `Keep` branch (see **Selector re-entry**); each invocation re-probes disk, so already-run methodologies carry the `✓` mark and the next un-run one carries `★`.
    - `selected` — capture the returned row payload (nine registry fields) into in-memory variables: `chosen.name`, `chosen.reviewer_agent`, `chosen.output_path`, `chosen.reference_asset`, `chosen.template_asset`, `chosen.map_skill`, `chosen.character`. Advance to step 1.
    - `cancelled` — emit *"Cancelled. No review run."* and exit cleanly. (No review can have run in this invocation: an accepted review ends the pipeline at step 3.)
    - `empty-registry` — emit *"No input-review methodologies are available yet. See `plans/` for candidate methodologies and their build checklists."* and exit cleanly. This is a defensive guard; with MVP methodologies registered it should not fire. (Only reachable on the first entry; a `Keep` re-entry implies a registered methodology.)

1. **Input-handle (first entry only)** — performed only when `preflight_done` is `false`; on a `Keep` re-entry skip this step and go straight to step 2. Invoke `framework/agents/input-handler.md` in the foreground with `documentation_dir: "documentation/"`, `manifest_path: "generated-docs/requirements/source-manifest.json"`, and `progress_path: null`. The agent owns the manifest lifecycle: it decides at its step 0 whether to **create** (manifest absent), **refresh** (present-and-stale, with consultant consent at its drift prompt), **no-op** (present-and-fresh, silent), or **halt** (present-but-corrupt). The orchestrator does not branch on manifest state itself; this single invocation is uniform regardless of what is on disk. Wait until the agent hands back per its Definition of Done. If the agent fails its handback via `RF-01 continue-later` (with `progress_path: null` the agent records nothing on disk), `RF-03 abort`, `RF-04 manifest-corruption halt`, or `Cancel` at the step-0 drift prompt, exit cleanly. On successful handback, set `preflight_done = true` and advance to step 2.

2. **Detect prior artefact for the chosen methodology** — `Read chosen.output_path`.
    - **No prior artefact** — proceed directly to step 3.
    - **Prior artefact exists** — surface a single `AskUserQuestion`:
        - Question: *"`{{chosen.output_path}}` already exists. Overwrite it with a fresh run, or keep it and pick another?"*
        - Header: `Prior artefact`
        - Options:
            1. `Overwrite — checkpoint and re-run`
            2. `Keep — back to the menu (Recommended)`
        - Branch:
            - **Overwrite** — perform the per-methodology **Reset procedure** below, then proceed to step 3.
            - **Keep** — output: *"Keeping existing `{{chosen.output_path}}`. Back to the menu."* and return to step 0 (see **Selector re-entry**).

3. **Invoke the reviewer** — invoke `chosen.reviewer_agent` in the foreground. Wait until the agent reports the artefact accepted (handback gate below).

After the handback gate is met, **commit the accepted artefact** (best-effort, non-blocking): invoke `framework/skills/commit-run-outputs.md` with `pipeline: "review-inputs"`, `method_name: chosen.name`, `method_dir: <the directory containing chosen.output_path>` — the directory, not the file, so the methodology's `<METHOD>.sidecar.json` is captured alongside it. Branch on the return: `committed` / `nothing-to-commit` → say nothing; `skipped-branch` → **one** plain-text line naming the branch; `failed` → **one** plain-text warning line. Then emit the **review completion message** (`framework/shared/context-hygiene.md`, verbatim plain text) with `{{method_name}}` = `chosen.name`, `{{output_path}}` = `chosen.output_path`, `{{METHOD_DIR}}` = the directory name directly containing `chosen.output_path`, `{{group}}` = `Input reviews`. Then declare done — the pipeline ends here and does **not** return to the step-0 selector (see **Selector re-entry**). There is **no** commit at the step-0 `cancelled` exit: nothing ran on that path.

## Per-methodology Reset procedure (overwrite an existing artefact)

This procedure runs **only** when the consultant chose `Overwrite` at step 2 and a prior artefact was detected at `chosen.output_path`. Perform the steps in this order; if any step fails, stop and surface the failure to the consultant — do not proceed.

1. **Git checkpoint.** Stage and commit the current state of the artefact so the prior run is preserved in history before deletion.
    - `Bash git add <chosen.output_path>`
    - `Bash git commit -m "checkpoint: prior <chosen.name> input-review before reset"` (use `--allow-empty` only if the file is unstaged, so the checkpoint marker exists in history regardless).
    - Do not push, do not amend, do not bypass hooks.
2. **Delete the prior artefact.**
    - `Bash rm -f <chosen.output_path>`
3. **Best-effort workspace deletion.** If the chosen methodology defines a workspace folder, the orchestrator does **not** delete it here — each reviewer owns its own workspace cleanup at its handback step. This is consistent with `design-system-styler`'s step-07 ownership of `generated-docs/design-system/.workspace/`.

After the reset completes, proceed to step 3.

## Handback gate

The chosen reviewer has handed control back when:

- The artefact at `chosen.output_path` exists.
- The agent's `verify-artifact-write` invocation in its write step returned `pass`.
- The consultant has chosen `Accept` in the agent's accept/revise/restart loop.
- Any agent-specific workspace cleanup (if defined) has been performed.

If any of the above is not satisfied, do not declare done. Surface the agent's report to the consultant and let the agent continue or be re-invoked.

## Inputs

- `framework/assets/reviews-inputs/registry.md` — read via the analysis-selector skill at step 0. Source of truth for the methodology list and per-methodology file paths.
- `framework/skills/analysis-selector.md` — invoked at step 0 with `registry_path: "framework/assets/reviews-inputs/registry.md"`, `list_label: "reviews"`, `verb_label: "review"`. The skill is shared with `/analyse-requirement` and `/analyse-inputs`; `/review-inputs` is its third caller.
- `framework/agents/input-handler.md` — invoked at step 1 with `documentation_dir: "documentation/"`, `manifest_path: "generated-docs/requirements/source-manifest.json"`, `progress_path: null` **on every path**. The agent owns the create / refresh / no-op / halt decision internally; the orchestrator never branches on manifest state. Shared with `/requirements`, `/generate-prd`, `/analyse-inputs`.
- `framework/agents/reviews-inputs/<method>-reviewer.md` — the reviewer agent invoked at step 3, resolved per the chosen registry row's `reviewer_agent` field. No reviewer exists on disk in this PR; the first one ships in the next follow-up development.
- `generated-docs/requirements/source-manifest.json` — read at step 1 by the input-handler (existence check + freshness comparison). Re-built by the input-handler when absent or when the consultant chooses `Refresh` at the input-handler's step-0 drift prompt; otherwise left unchanged.
- `documentation/` — read by the reviewer per-row (originals or converted siblings) per its own workflow; the orchestrator does not read it.
- `framework/shared/refusal-registry.md` — `RF-01`, `RF-03`, `RF-04` semantics surfaced by this orchestrator, by the input-handler at step 1, and by the reviewer at its write step.
- `framework/skills/commit-run-outputs.md` — invoked once, after the accepted artefact at the end of step 3, with `pipeline: "review-inputs"`, `method_name`, `method_dir`. Owns the staging set, the subject string, the branch guard, and the four return values; best-effort and non-blocking.
- `framework/shared/context-hygiene.md` — the canonical review completion message emitted at the end of step 3.

## Output

- `<chosen.output_path>` — produced by the reviewer at its write step. The orchestrator produces no other artefact directly. The step-1 input-handler invocation, when it fires, additionally produces `generated-docs/requirements/source-manifest.json` and `documentation/**/*.converted.md` siblings as documented in the stand-alone constraint exception.

## Tools

- `Read` — check whether `<chosen.output_path>` exists at step 2. No other reads outside the input-handler's and reviewer's input paths are permitted. The step-1 manifest existence-and-freshness check is owned by the input-handler at its step 0, not by the orchestrator.
- `Bash` — git checkpoint commit + `rm -f <chosen.output_path>` during the Reset procedure; and, after the accepted artefact, the completion-commit sequence owned by `commit-run-outputs.md` — the `git status -sb` branch-guard read, one `git add` per resolved path, the `git diff --cached --quiet` probe, and the pathspec-limited `git commit`. No other Bash usage outside what the invoked agents own. Never use destructive operations beyond the explicitly named path. Never push, amend, or skip hooks.
- `framework/skills/commit-run-outputs.md` — the best-effort completion commit after the accepted artefact (`pipeline: "review-inputs"`).
- `AskUserQuestion` — surface the step-2 `{ Overwrite, Keep }` prompt when a prior artefact exists. The step-0 methodology prompt belongs to the analysis-selector skill; the step-1 input-handler's `RF-01` / `RF-03` / `Old versions` / `Manifest drift` prompts belong to that agent; the step-3 accept/revise/restart prompts belong to the reviewer agent — the orchestrator does not surface any of these directly.

The orchestrator's tools are limited to the operations above. Every other read or write of review content belongs to the invoked agent; each agent uses the tools listed in its own agent file.

## Markers in content (reviewer citation namespace)

Input-reviewers under this pipeline cite source-of-fact in their artefacts using `[SRC: <filename>]` markers, where `<filename>` is the manifest row's `filename` field (its path relative to `documentation/`, forward slashes — equal to the basename for a top-level file; `framework/skills/build-source-manifest.md > Field rules`). This matches the `/analyse-inputs` analyser convention and differs from the `/requirements`-pipeline drafter's `[SRC: C-NNN]` markers, which carry stable sidecar-claim IDs. All three forms can coexist in the workspace because:

- The `/review-inputs` pipeline writes only to `generated-docs/review-inputs/<METHOD>/`; the `/requirements` pipeline never reads under that path.
- `framework/skills/grounding-verifier.md` consumes only the `/requirements`-pipeline draft and its sidecar; it never reads under `generated-docs/review-inputs/`.

Each input-reviewer additionally records a source-roster section in its artefact listing every manifest row consumed (with `filename`, `tier`, `sha256` first eight chars) and every manifest row skipped (with reason). See each reviewer's own template for the exact section shape.

## Self-validation (run before declaring done)

- Step 0 ran; on each entry the analysis-selector skill returned exactly one of `selected | cancelled | empty-registry`, and the orchestrator branched accordingly. Step 0 was re-entered only from the step-2 `Keep` branch — never after an accepted artefact. On `empty-registry` (first entry only), the orchestrator exited cleanly with the "no input reviews available yet" message and no further step ran. A `cancelled` exit emitted *"Cancelled. No review run."*
- At most one reviewer ran in this invocation. After its accepted handback the orchestrator emitted the review completion message (`framework/shared/context-hygiene.md`) verbatim with its placeholders filled (`{{group}}` = `Input reviews`), and ended — it did not return to the selector and did not emit the generic context-hygiene tip.
- Step 1 is at-most-once preflight, guarded by `preflight_done`: it ran on the first `selected` entry and was **skipped** on any `Keep` re-entry (the orchestrator went straight from step 0 to step 2). `preflight_done` was set `true` only after step 1's successful handback.
- On the first entry, step 1's input-handler was invoked uniformly with `progress_path: null` and ran to handback per its Definition of Done, decided its own mode (`create` / `refresh` / `no-op` / `proceed-stale`), and produced a manifest at `generated-docs/requirements/source-manifest.json` plus any required `*.converted.md` siblings (on `create` and `refresh` only). If the input-handler exited via `RF-01 continue-later`, `RF-03 abort`, step-0 `RF-04 manifest-corruption halt`, or step-0 `Cancel` at its drift prompt, the orchestrator exited cleanly and no reviewer was invoked.
- If the consultant chose `Keep` at the step-2 prior-artefact gate, no `Bash` was run and the reviewer was not invoked; `Keep` returned control to step 0.
- If the consultant chose `Overwrite` at step 2, the git checkpoint commit ran without `--no-verify`, without amend, and without push, and the prior artefact was deleted before the agent was invoked.
- If the reviewer was invoked, its handback gate was met (artefact exists, verify pass, consultant accepted).
- The reviewer agent and the shared input-handler agent were each run in the foreground, never via the Agent / Task / fork / sub-agent mechanism. The reviewer's own internal per-dimension workers (dispatched at its Step 4) are the sanctioned exception per the **Execution model** carve-out — read-only (in fact tool-less), non-interactive, owning no handback; they are not orchestrator-invoked agents.
- `framework/skills/commit-run-outputs.md` was invoked **exactly once** when a review was accepted, immediately after the handback gate and before the review completion message — never on the `Keep` branch, never on the step-0 `cancelled` / `empty-registry` exits, and never on a step-1 input-handler exit. Its return was one of `committed | nothing-to-commit | skipped-branch | failed`; a non-`committed` return produced at most one plain-text line, left the artefact on disk, and did not suppress the review completion message.
- No file was written outside `generated-docs/review-inputs/<chosen.name>/`, with the documented step-1 exception of `generated-docs/requirements/source-manifest.json` and `documentation/**/*.converted.md` siblings produced by the input-handler. (The per-methodology completion commit is a git-history write, not a filesystem write.)
- `framework/state/.progress.json` was not written by this orchestrator on any branch. `preflight_done` was not persisted to disk.
- `framework/state/timing.ndjson` was not written by this orchestrator on any branch.

## Definition of Done

The pipeline is done when exactly one of:

- The reviewer handed back a consultant-accepted artefact (`<chosen.output_path>` exists with `verify-artifact-write` having returned `pass`), the completion commit was attempted, and the review completion message was emitted — the success terminal, or
- The consultant chose `Cancel` at the step-0 selector (and the orchestrator exited cleanly with *"Cancelled. No review run."*), or
- The selector returned `empty-registry` at step 0 (first entry; and the orchestrator exited cleanly with the "no input reviews available yet" message), or
- The input-handler exited on the first entry via `RF-01 continue-later`, `RF-03 abort`, `RF-04 manifest-corruption halt`, or `Cancel` at the step-0 drift prompt (and the orchestrator exited cleanly).

## Anti-Patterns

- Do not perform any task other than the steps listed above.
- Do not advance past the handback gate before it is met.
- Do not read, write, or edit any review artefact directly. The orchestrator's only direct disk operations are the existence checks (Read), the per-methodology Reset procedure (Bash rm + git checkpoint commit), and the per-methodology completion commit — the last of which is a git-history write, not a filesystem write. Every other read or write belongs to the invoked agent.
- Do not call any skill, asset, or tool not invoked transitively by the input-handler or the reviewer, or listed in this orchestrator's **Tools** section.
- Do not run the reviewer agent or the shared input-handler agent as a background / sub / async agent. Each must run in the foreground in the same thread so consultant Q&A and acceptance happen in-thread. The reviewer's internal read-only (tool-less) per-dimension workers are the sole sanctioned sub-agent dispatch, per the **Execution model** carve-out — they are non-interactive, write nothing, and own no handback; do not extend this licence to any consultant-interactive surface.
- Do not run the per-methodology Reset procedure when no prior artefact was detected, and do not run it when the consultant chose `Keep`.
- Do not delete anything outside `<chosen.output_path>` during a reset. The Reset procedure is scoped to one file per methodology, plus the git checkpoint commit.
- Do not commit with `--no-verify`, force-push, amend, or otherwise bypass git hooks during the checkpoint commit — or during the completion commit.
- Do not invoke `commit-run-outputs.md` on the step-2 `Keep` branch, on the step-0 `cancelled` / `empty-registry` exits, or on a step-1 input-handler exit. Nothing fresh was written on those paths; invoking there would find an artefact left dirty by a previously *cancelled* run and commit it under a subject claiming this run produced it.
- Do not let the completion commit block. A `failed` return produces **one** plain-text warning line and the review completion message still follows; it never deletes the artefact. Do not restate the skill's staging set, subject string, branch guard, or pathspec form here — they are canonical in the skill.
- Do not maintain a `.progress.json` file. This orchestrator runs one reviewer per run (the input-handler invocation at step 1 is at-most-once preflight, not a tracked pipeline stage); on-disk progress tracking is unnecessary and out of scope (the selector reconstructs run-state from artefact presence).
- Do not re-run the step-1 input-handler invocation on a `Keep` re-entry. It is at-most-once preflight, guarded by `preflight_done`; a re-entry goes straight from step 0 to step 2.
- Do not return to the step-0 selector after an accepted artefact, and do not offer another review in the same context. The accepted-review terminal is the review completion message; the consultant runs the next review after `/clear`.
- Do not paraphrase the review completion message or substitute the generic context-hygiene tip for it. Its wording is canonical in `framework/shared/context-hygiene.md`.
- Do not persist `preflight_done` to disk, and do not treat it as resumable across a `/clear`. Cross-session continuity comes from the selector's on-disk `✓ already run` probe and the input-handler's own freshness check on a fresh invocation.
- Do not write to `framework/state/timing.ndjson`. Timing observability is a `/requirements`-pipeline concern; this pipeline does not append to it.
- Do not skip step 1's input-handler invocation on the **first** entry (when `preflight_done` is `false`) once step 0 has returned `selected`. Without it the manifest's freshness goes unchecked and (on first-mover) the manifest is never built; either way, the reviewer has no usable source enumeration. (On a `Keep` re-entry the input-handler is deliberately skipped — that is the `preflight_done` guard, not a violation.)
- Do not branch step 1 on whether the manifest exists on disk. The orchestrator must call the input-handler uniformly; the agent owns the create / refresh / no-op / halt decision. Re-introducing per-orchestrator branching here duplicates instructions the input-handler already owns.
- Do not invoke the input-handler with a non-null `progress_path`. This pipeline does not own a progress file; passing a path would orphan a `setup-pending` state with no orchestrator that watches for it.
- Do not write `framework/state/.progress.json` on the input-handler's `RF-01 continue-later` branch. The review-inputs pipeline is bound by the no-write-outside-`generated-docs/review-inputs/` invariant (with the documented step-1 exceptions).
- Do not read `framework/state/` or `framework/shared/` outside the refusal-registry references documented in **Stand-alone constraint**. This orchestrator and its reviewers remain stand-alone for every other purpose.
- Do not write to `generated-docs/review-requirements/<METHOD>/`. That directory is owned by the `/review-requirement` pipeline; this pipeline writes only under `generated-docs/review-inputs/<METHOD>/`.
- Do not write to `generated-docs/analyse-inputs/<METHOD>/`. That directory is owned by `/analyse-inputs`; review-inputs writes only under `generated-docs/review-inputs/<METHOD>/`.
- Do not invoke `framework/skills/set-build-target.md`. The manifest's `target` field is a `/requirements`-pipeline concern; this pipeline leaves it `null` indefinitely. Setting it from here would originate a `/requirements`-pipeline field from the wrong pipeline (origination belongs to the `/requirements` orchestrator's Step 1b policy).
- Do not surface the step-0 methodology prompt from within this orchestrator. That prompt is the analysis-selector skill's responsibility; surfacing it inline duplicates the registry-read logic and breaks the open/closed extension contract (adding a methodology must require zero orchestrator edits).
- Do not surface the step-3 accept/revise/restart prompt from within this orchestrator. That prompt belongs to the chosen reviewer's handback step.
- Do not hardcode any methodology name in this orchestrator's control flow. Every methodology-specific value is resolved from the chosen registry row's fields. The orchestrator must work unchanged when a new MVP row is added or an existing row is renamed.
- Do not flip the framework-empty exit (step 0 `empty-registry`) into a `RF-04` or other halt predicate. An empty MVP registry on this pipeline is the **expected** state on ship; the friendly exit message is the correct surface.
