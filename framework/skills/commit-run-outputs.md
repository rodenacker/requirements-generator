# commit-run-outputs.md

**Purpose:** Commit a completed, consultant-approved pipeline run's artefacts to git history, automatically and with no extra prompt, at the point where the orchestrator's handback gate has been met and immediately before it emits the context-hygiene tip (`framework/shared/context-hygiene.md`). Generalises the inlined completion commit `/prototype` has carried at its Step-G Accept since the pipeline shipped, so that all thirteen pipelines preserve accepted work rather than preserving it only when the *next* run is about to destroy it (the pre-destructive `checkpoint: …` commits, which this skill does **not** touch).

**Best-effort and non-blocking by design.** Failure here never undoes a `status` write, never suppresses the context-hygiene tip, and never registers an `RF-NN` predicate — the pipeline has already succeeded by the time this skill runs.

**Inputs:**
- `pipeline` — exactly one of the thirteen names keying the path table below. An unknown name returns `failed` (a caller bug, not a refusal).
- Run slugs — a **closed slot set**: `scope_slug`, `name_slug`, `app_id`, `date`, `stem`, `method_name`, `method_dir`, `files_to_write`. Only the slots the chosen row references are required; a slot the row does not reference is ignored. Anything outside this set is rejected — a caller must not be able to smuggle an arbitrary path in through a slot.

`paths` is **not** a caller argument. It is resolved from the table in **The path table** below. Paths that do not exist on disk are **omitted** from both the `git add` and the commit pathspec — never allowed to fail the staging step (the existing house convention, e.g. `design-system-orch.md`'s reset, `ingest-stadium-orch.md`'s reset).

**Outputs:** exactly one of:
- `committed` — a commit was created.
- `nothing-to-commit` — every resolved path was clean (or none resolved); no commit made, **no warning emitted**.
- `skipped-branch` — the branch guard refused. The caller emits **one** plain-text line naming the branch; no prompt, no gate.
- `failed` — not a git repo, a staging error, a rejecting hook, or an unknown `pipeline`. The caller emits **one** plain-text warning line and continues.

**Used by:** all thirteen orchestrators, at their success terminal only.
- **Pattern A — single success terminal (9):** `framework/orchestrators/{requirements,generate-prd,design-system,export-application,wireframe,amend-requirements,resolve-review,ingest-stadium,prototype}-orch.md`.
- **Pattern B — selection loop (4):** `framework/orchestrators/{analyse-requirement,analyse-inputs,review-requirement,review-inputs}-orch.md`, invoked **per accepted methodology** at the `✓ Ran {{chosen.name}}. Back to the menu.` line — not once at session exit.

## Procedure

1. **Branch guard — before any staging.** `Bash git status -sb` and read the first line only (e.g. `## human-readable-outputs...origin/human-readable-outputs`). Return `skipped-branch` when either of:
    - the upstream named after `...` is on the `release` remote (`release/…`);
    - HEAD is detached (the first line reads `## HEAD (no branch)`).

   **No upstream at all → allow.** A local-only branch cannot be a release branch. Evaluating the guard first means a refusal leaves the index untouched.

   **`main` is deliberately *not* refused.** It was, until the guard's `main` clause proved to be the wrong shape: it used the branch name as a proxy for *"this is a framework-development checkout"*, and that proxy is equally true of every consultant who clones the framework and starts working. The pipelines' audience is consultants and BAs who are not expected to know git, so a name-based refusal on `main` meant the completion commit never fired for exactly the user it exists to protect — announced only by one `skipped-branch` line emitted immediately before the `/clear` tip, where it is reliably missed. What the guard now refuses is the outcome that is actually bad: a commit on a branch that tracks the shipped framework repo, or on a detached HEAD where the commit would be unreachable. Refusing `main` bought less than it appeared to in any case — the thirteen pre-destructive `checkpoint: …` commits are unguarded and land on `main` already.
2. **Resolve `paths`** from the table below using the supplied slots. Drop every resolved path that does not exist on disk — **except a path the table marks *deletion-tracked*** (†). For such a path, run `Bash git status --porcelain -- <path>`. Output starting ` D` means git tracks it and the run deleted it: keep it, so steps 3–5 stage and commit the deletion. Any other output, or none, means there is nothing to record: drop it. If nothing remains, return `nothing-to-commit`.
3. **Stage** — one `Bash git add <path>` invocation **per resolved path**. One path per invocation, so each call matches a narrow permission pattern in `.claude/settings.json` rather than requiring a broad grant.
4. **Probe** — `Bash git diff --cached --quiet`. Exit 0 means nothing was staged: return `nothing-to-commit`. (Stage-then-probe, not stderr parsing — which is what makes any non-zero from step 5 unambiguously a real failure.)
5. **Commit** — `Bash git commit -m "<subject>" -- <paths…>`, with the same omission rule applied to the pathspec. Non-zero exit → return `failed`. Otherwise return `committed`.

## The path table

Canonical here. The staging set is a *subset* of each orchestrator's write list — run state yes, scratch sidecars no. Each orchestrator's stand-alone-constraint block points at this table rather than restating its paths.

| `pipeline` | `paths` | `subject` |
|---|---|---|
| `requirements` | `generated-docs/requirements/`, `documentation/*.converted.md`, `framework/state/.progress.json`, `framework/state/timing.ndjson` | `requirements: complete` |
| `generate-prd` | `generated-docs/prd/`, `framework/state/.prd-progress.json`, `framework/state/timing.ndjson` | `prd: complete` |
| `design-system` | each file in `{{files_to_write}}` | `design-system: complete` |
| `export-application` | `generated-docs/export-application/requirements-application.md`, `generated-docs/export-application/fold-report.md` † | `export-application: complete` |
| `wireframe` | `wireframes/<scope_slug>/`, `blueprints/<scope_slug>/` | `wireframe: <scope_slug> complete` |
| `amend-requirements` | `documentation/amendments-<date>[-N].md`, `generated-docs/requirements/requirements.md` | `amend-requirements: <date> complete` |
| `resolve-review` | `documentation/<stem>-<date>[-N].md`; plus `generated-docs/requirements/requirements.md` **only** if the orchestrator's step 9b applied the addendum | `resolve-review: <stem> complete` |
| `ingest-stadium` | per **freshly-extracted** app: `documentation/<AppName>.stadium-assets/` + `framework/state/stadium/<app_id>/`; plus `framework/state/.stadium-processed.json` once | `ingest-stadium: <app_id> extracted` (one app) / `ingest-stadium: <N> apps extracted` (several) |
| `prototype` | `prototypes`, `blueprints/<scope_slug>`, `framework/state/.prototype-progress.json`, `framework/state/timing.ndjson` | `prototype: <name_slug> complete` |
| `analyse-requirement` | `<method_dir>` | `analyse-requirement: <method_name> complete` |
| `analyse-inputs` | `<method_dir>`, `generated-docs/requirements/source-manifest.json`, `documentation/*.converted.md` | `analyse-inputs: <method_name> complete` |
| `review-requirement` | `<method_dir>` | `review-requirement: <method_name> complete` |
| `review-inputs` | `<method_dir>`, `generated-docs/requirements/source-manifest.json`, `documentation/*.converted.md` | `review-inputs: <method_name> complete` |

Notes on individual rows:

- **`prototype`** carries the path set and subject string the pipeline used before this skill existed, byte-identical, so its history stays uniform across the refactor. It does newly acquire the branch guard.
- **`ingest-stadium`** says `extracted`, not `complete`. This pipeline has no consultant approval step — its handback gate is mechanical and its assets are LLM-audience, never surfaced for review. Committing deterministic extractor output is right (it is what makes a later hand-edit diffable) but it is not approval, and `complete` must keep meaning *a human accepted this*. Only apps the run reported as **extracted** are staged: a *skipped* app's assets were committed by an earlier run and its hand-edits are deliberately preserved; a *failed* app is left un-ledgered for retry, and committing its partial extract would present broken output as complete.
- **`export-application`** stages `fold-report.md` alongside the export — it is the record of what the amendment fold changed. It is **deletion-tracked** (†): the orchestrator deletes it on a Regenerate and on a run with no amendments, so an accepted run with no fold must commit that deletion. Otherwise git would keep the report from an earlier source version, and the working tree would show an uncommitted deletion indefinitely. The transient `.folded-source.md` is never staged; the orchestrator deletes it before this skill runs.
- **† deletion-tracked** — a path whose deletion by the run is itself an output. Step 2 keeps it when `git status --porcelain` reports it as a tracked deletion (` D`); `git add <path>` then stages the removal, and the `--` pathspec commits it. Only the paths marked † get this treatment — every other absent path is still dropped.
- **`design-system`** stages exactly the mode files the run actually wrote (`{{files_to_write}}`), never the pair unconditionally.
- **The `[-N]` disambiguator** on the two dated-document rows is resolved by matching `documentation/amendments-<date>*.md` / `documentation/<stem>-<date>*.md` rather than by plumbing the exact suffix through a slot. A same-day file from an earlier run is already committed and therefore clean, so matching it is a no-op; the run's own new file is the only one that lands in the commit. Both patterns stay inside class 3 of the `documentation/` allow-list below.
- **`<method_dir>`** is the **directory** containing the methodology's `output_path` (e.g. `generated-docs/analyse-requirements/<METHOD>/`), so the `<METHOD>.sidecar.json` written alongside is captured. The four loop pipelines stage **no run state** — they persist none (no `.progress.json`, no `timing.ndjson`, and `run_count` is in-memory only).
- **The two `*-inputs` rows** name the manifest and the conversion siblings **unconditionally**, and the caller passes no first-iteration flag. Those paths carry a change only on the loop's first iteration, because the shared input-handler is once-per-session preflight; on every later iteration they are already clean and staging them is a no-op that adds nothing to the commit. Deriving the set from the `pipeline` name alone keeps the slot set closed and the behaviour deterministic.

## Self-validation

- The branch guard ran **before** any `git add`. On `skipped-branch` the index is byte-identical to what it was at entry.
- Every `git add` was a single explicit path from the resolved set — never `-A`, never `.`, never a bare directory the run did not produce.
- An absent path stayed in the resolved set only when the table marks it † **and** `git status --porcelain -- <path>` reported ` D`.
- The commit carried a `--` pathspec listing exactly the resolved paths, so its content does not depend on what the consultant had staged when the run started.
- No path under `documentation/` outside the three allowed classes was staged (see Anti-Patterns).
- Exactly one of the four return values was produced, and the caller's branch on it matched: `committed` → silent, `nothing-to-commit` → silent, `skipped-branch` → one line, `failed` → one warning line.

## Anti-Patterns

- Never `push`, `--amend`, `--no-verify`, or force. Same rule the thirteen pre-destructive `checkpoint:` blocks already carry.
- Never `--allow-empty`. A checkpoint uses it so the marker exists in history regardless of whether anything was staged; a *completion* commit with nothing in it is pure noise. This is a deliberate divergence from the checkpoint blocks, not an oversight.
- Never a bare `git commit` without the `--` pathspec. `git commit` commits the *index*, which in a repo where the consultant is also the framework developer routinely holds in-flight framework edits. The pathspec is what makes the commit's content equal to `paths` rather than dependent on consultant discipline — and what stops a hook-rejected commit leaving residue for the next run's `checkpoint: … --allow-empty` block to sweep into a commit labelled as a pre-destructive checkpoint.
- Never `git add -A`, `git add .`, or a bare directory the run did not produce.
- **Never commit a client original.** This is a **confidentiality and repo-bloat** rule governing what enters git history — *not* an input-safety rule. `IS-01`/`IS-03` (`framework/shared/input-safety.md`) govern **deletion**, and a file can be `IS-01`-protected yet obviously safe to commit. Exactly three classes under `documentation/` may be staged:
  1. `documentation/*.converted.md` — framework-generated conversion siblings;
  2. `documentation/<AppName>.stadium-assets/` — framework-generated extractor output;
  3. framework-authored dated documents — `documentation/amendments-<date>[-N].md` and `documentation/<stem>-<date>[-N].md`.

  Everything else `IS-01` enumerates is a client original and never enters history: raw dropped source files of any format, the `*.stadium` pointer, and every path under a dropped Stadium 6 application folder. Class 3 files *are* named in `IS-01`'s protected list — they are protected from **deletion**, and they are precisely the artefact `/amend-requirements` and `/resolve-review` exist to produce, so committing them is the point.
- Never `git add documentation/` wholesale, and never a bare `documentation/<AppName>/` app folder.
- Never guard the pre-destructive checkpoints. The branch guard applies to the **completion** commit only. A future reader will see `checkpoint:` commits landing on a release-tracking branch or a detached HEAD while completion commits do not; that asymmetry is deliberate — a checkpoint's job is preserving something about to be deleted, on any branch.
- Never invoke this skill on a `Keep`-existing branch, a cancel branch, a prerequisite exit, or a refusal halt. Callers invoke it **only where a fresh artefact was written this iteration**. Invoking on a `Keep` branch would find an artefact left dirty by a previously *cancelled* run and commit it under a subject claiming this iteration produced it.
- Never block. A `failed` return produces one plain-text warning line from the caller and the pipeline continues; it never undoes a `status: "complete"` write and never suppresses the context-hygiene tip. `nothing-to-commit` produces nothing at all.
- Never register a new `RF-NN` for a failure here. Failure is benign by design; a refusal predicate would misclassify it.
- Never refactor the thirteen pre-run `checkpoint: …` blocks into this skill. They are deliberately out of scope — they run on a different trigger (imminent destruction), carry different flags (`--allow-empty`), and are unguarded by branch.
- Do not read the `skipped-branch` guard from `git rev-parse` or `git branch`. `git status -sb` is used specifically because `Bash(git status *)` is already in the shipped allowlist, so the guard adds **zero** new permission patterns.
