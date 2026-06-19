# Refusal Registry

Catalogue of refusal predicates used by pre-ingestion and pipeline agents. Each predicate has a stable ID `RF-NN`, a trigger condition, a surface mechanism (how the agent communicates the refusal to the consultant), and a recovery path. Agents reference predicates by ID in their workflow; the registry is the single source of truth for what each ID means.

Add new predicates by appending; never renumber.

**Severity:**
- `pause` — recoverable. The agent halts work but the consultant can resolve the condition (install a tool, drop a supported file, run `/clear`) and continue without restarting the pipeline.
- `hard` — unrecoverable. The agent halts, fails its handback, and the orchestrator does not advance. The consultant must resolve and re-invoke the pipeline.

**Surface mechanisms:**
- `AskUserQuestion` with a bounded choice set — used for `pause` predicates so the consultant's intent is explicit and machine-readable.
- Plain-text halt — used for `hard` predicates where the only response is to abort and protect prior work.

## RF-01 — dependency_missing

**Severity:** pause.

**Trigger:** A required external dependency — an **MCP-backed tool** or a **CLI binary** — is not available at preflight time. Two MVP cases: (a) `mcp__markitdown__convert_to_markdown` (probed via `framework/skills/preflight-mcp.md`) is required when at least one input file's tier is `Supported-via-MCP`; (b) a vector renderer (probed via `framework/skills/preflight-cli.md`) is required when at least one input file's tier is `Vector-renderable`. The predicate is dependency-agnostic; the surfacing caller supplies the `advice_path` of the specific dependency.

**Surface:** `AskUserQuestion` with the choice set `{ continue-skip, continue-later }` plus an "Other" override.
- `continue-skip` — the agent proceeds with the missing dependency absent; every file that needed it reclassifies to `Unsupported` for this run and is recorded in the manifest with `conversions_applied: "skipped — RF-01"`.
- `continue-later` — the agent writes `status: setup-pending` and `pending_setup: { predicate: "RF-01", advice_path: "<the probed dependency's advice_path>", since: <ISO-8601 UTC> }` to `framework/state/.progress.json` and exits cleanly. The consultant installs the dependency and re-invokes the pipeline. (The `advice_path` is `framework/shared/setup-instructions/markitdown.md` for the markitdown case, `framework/shared/setup-instructions/visual-render.md` for the vector-renderer case.)

**Recovery:** Read the `advice_path` surfaced in the question text — `framework/shared/setup-instructions/markitdown.md` (markitdown) or `framework/shared/setup-instructions/visual-render.md` (vector renderer).

**Refusal-registry schema field:** `setup_instructions_path` — the absolute repo-relative path to the install copy. Used only by `RF-01` for now; reserved for future predicates that point at out-of-band setup steps.

## RF-02 — input_format_unsupported

**Severity:** pause.

**Trigger:** One or more files in `input/` have an extension that the tier rubric in `framework/skills/classify-input-tier.md` maps to `Unsupported`, AND at least one file in `input/` is non-Unsupported (so the run is not blocked by RF-03).

**Surface:** No prompt — the agent records the unsupported files in the manifest with `tier: "Unsupported", kind: "primary", conversions_applied: "none"` and proceeds with the supported files. The drafter skips Unsupported rows per its workflow. The unsupported files remain on disk for forensic record.

**Recovery:** None required for the run to proceed. The consultant may convert the file out-of-band and re-drop it as a supported format, then re-run.

## RF-03 — input_no_supported_files

**Severity:** pause.

**Trigger:** Every file in `input/` classifies to `Unsupported` (or `input/` is empty after the one-message wait completed). The drafter has no readable inputs.

**Surface:** `AskUserQuestion` with the choice set `{ retry-after-fix, abort }`.
- `retry-after-fix` — the consultant drops a supported file into `input/`; the input-handler re-enumerates and re-classifies, then continues from preflight.
- `abort` — the agent halts with a failed handback; the orchestrator does not write a `completed` event.

**Recovery:** `retry-after-fix` is the standard path; `abort` exits cleanly.

## RF-04 — artifact_write_unverified

**Severity:** hard.

**Trigger:** `framework/skills/verify-artifact-write.md` reports a mismatch between the in-memory render and the on-disk file after one silent retry. Any artefact-producing step (input-handler manifest, drafter draft, resolver answers, merger requirements) can fire this predicate.

**Surface:** Plain-text halt. The agent emits exactly one line — *"Aborting to protect your work — write verification failed for `<path>` after one retry."* — and fails its handback. No `AskUserQuestion`; the consultant cannot meaningfully choose between options when the filesystem is in an unknown state.

**Recovery:** The consultant inspects the failure (disk full, read-only filesystem, hook interference) and re-invokes the pipeline. The orchestrator's rerun detection picks up the partial state.

## RF-05 — prior_stage_context_bloated  [RETIRED 2026-06-15]

**Status:** Retired. The context-bloat preflight feature — the `framework/skills/check-context-bloat.md` skill, this predicate, and the `context-bloated` progress-status value — was removed on 2026-06-15. The heuristic summed on-disk artefact bytes as a proxy for *conversation* context, but the two are decoupled: the bytes are identical across a `/clear`, so the gate false-fired on every run of any mature project (where `requirements/` routinely exceeds the old 500 KB ceiling). It is replaced by non-blocking `/clear` suggestions emitted at each pipeline's success terminal — see `framework/shared/context-hygiene.md`.

This ID is retained — never renumbered or deleted — per the append-only stable-ID invariant. **No orchestrator surfaces it.** Do not reuse `RF-05` for a new predicate; append a new `RF-NN` instead.

## RF-06 — style_extraction_dependency_missing

**Severity:** pause.

**Trigger:** The design-system-styler's preflight in `step-04-site-fetching.md` does not find `mcp__playwright__browser_navigate` in the available tool list, AND the consultant supplied a non-null `{{reference_url}}` in step-02. Distinct from `RF-01` because the styler has a degraded-fidelity fallback path (WebFetch) that the input-handler does not, so the choice set is three-way rather than two-way.

**Surface:** `AskUserQuestion` with the choice set `{ install-and-retry, use-webfetch-fallback, drop-url }` plus an "Other" override. The question text must include the install instructions path (`advice_path`) and the verbatim fidelity warning for the WebFetch option.

- `install-and-retry` — the agent halts step-04, writes `status: setup-pending` and `pending_setup: { predicate: "RF-06", advice_path: "framework/shared/setup-instructions/playwright.md", since: <ISO-8601 UTC> }` semantics into the styler's own state (the styler does not write `framework/state/.progress.json` per the stand-alone constraint — it surfaces the install path in the handback message and exits cleanly so the consultant installs Playwright and re-runs `/design-system`). Highest-fidelity outcome.
- `use-webfetch-fallback` — the agent proceeds via the legacy WebFetch two-pass path. Sets `extraction_method = "webfetch-fallback"` in `metadata.json`, does not write `computed-tokens.json`. The consultant's choice is the contract — the agent does not re-warn during the run. Lower-fidelity outcome; many tokens may end up `inferred-from-domain` instead of `extracted-from-url`.
- `drop-url` — the agent sets `{{reference_url}} = null`, records `extraction_status = playwright_unavailable`, and skips to `step-05b-domain-inference.md`. Most predictable outcome; tokens uniformly `inferred-from-domain`.

**Recovery:** `install-and-retry` exits cleanly so the consultant installs Playwright per `framework/shared/setup-instructions/playwright.md` and re-invokes `/design-system`. `use-webfetch-fallback` and `drop-url` continue the run.

**Refusal-registry schema field:** `setup_instructions_path` — same field as RF-01, pointing here at `framework/shared/setup-instructions/playwright.md`.

## RF-07 — mermaid_render_dependency_missing

**Severity:** pause.

**Trigger:** Gate 9 of an MVP analyser whose methodology emits Mermaid source requires `mmdc` (Mermaid CLI) on PATH to validate the emitted Mermaid `mindmap` or `flowchart TD` source via `framework/skills/mermaid-validator.md`. `mmdc` not found on PATH. Distinct from `RF-01` because the methodology-level rendering dependency is independent of the input-handler's markitdown MCP dependency, and distinct from the validator skill's own internal `not-installed` halt because the analyser exposes a three-way choice rather than a hard halt.

> **No active caller as of the analyse-inputs inline-SVG conversion.** `affinity-mapping` was the original surfacer (its Step 10 Gate 9); it — and `swim-lane-process-mapping` — now **pre-render their diagrams as inline `<svg>`** and no longer validate Mermaid, so this predicate currently has no surfacing analyser. It remains defined (stable IDs are append-only — never renumber/delete) for any future Mermaid-render-dependent methodology that chooses to surface it.

**Surface:** `AskUserQuestion` with the choice set `{ install-and-retry, skip-mermaid-validation-with-warning, abort }` plus an "Other" override. The question text must include the install instructions path (`advice_path`) and the verbatim warning for the skip option.

- `install-and-retry` — the agent halts Gate 9, surfaces the install advice path in the handback message, and exits cleanly so the consultant installs `mmdc` per `framework/shared/setup-instructions/mmdc.md` and re-invokes the pipeline. The analyser does **not** write `framework/state/.progress.json` — the `/analyse-inputs` pipeline is bound by a no-write-outside-`analyse-inputs/` invariant (with the input-handler's documented manifest exception), and Step 10 has not yet written the artefact. Highest-fidelity outcome.
- `skip-mermaid-validation-with-warning` — the agent proceeds without running Gate 9's mermaid-validator invocation. The artefact still writes with the Mermaid source verbatim inside `<pre class="mermaid-source">` (consultants render out-of-band via [mermaid.live](https://mermaid.live)). The diagnostics block records a warning entry naming the skipped validation; Gate 9's status in the quality-gates list is `warn` with the explanation *"`mmdc` not on PATH; pre-write validation skipped per consultant choice — render out-of-band to confirm syntax"*. Lower-fidelity outcome; Mermaid syntax errors are caught only by the consultant's out-of-band render.
- `abort` — the agent halts Step 10 and fails its handback. The orchestrator does not write a `completed` event. No artefact write.

**Recovery:** `install-and-retry` exits cleanly so the consultant installs `mmdc` per `framework/shared/setup-instructions/mmdc.md` and re-invokes the pipeline. `skip-mermaid-validation-with-warning` continues the run with the diagnostics warning. `abort` exits cleanly with a failed handback.

**Refusal-registry schema field:** `setup_instructions_path` — same field as RF-01 and RF-06, pointing here at `framework/shared/setup-instructions/mmdc.md`.

## RF-08 — stale_analysis_sidecar

**Severity:** hard.

**Trigger:** The blueprint-architect's step-02 block 2.6 read a `<METHOD>.sidecar.json` whose `source_sha256` field does not match a freshly-computed sha256 of `source_path` on disk. This indicates the consultant hand-edited the prose artefact after the analyser wrote the sidecar — the sidecar's `architect_projection` is potentially stale and the architect cannot trust it.

**Surface:** Plain-text halt. The agent emits exactly one line — *"Aborting to protect downstream wireframes — sidecar `<METHOD>.sidecar.json` is stale relative to `<source_path>` (sha256 mismatch). Re-run `/analyse-requirement <method>` to regenerate the sidecar, then re-invoke `/wireframe`."* — and fails its handback. No `AskUserQuestion`; there is no meaningful in-thread choice when the analyser's structured projection has diverged from the prose the consultant edited.

**Recovery:** The consultant re-runs `/analyse-requirement <method>` to regenerate both the prose artefact and the sidecar from current `requirements/requirements.md`. The wireframe pipeline is then re-invoked; rerun detection at `step-0d` picks up the prior `analyses-inputs.json` and reuses the same selection.

**Refusal-registry schema field:** none specific. Distinct from `RF-04` because the data-integrity failure is between two artefacts on disk (sidecar vs prose), not between an in-memory render and disk; distinct from `RF-09` because the sidecar exists but is stale, not absent.

## RF-09 — legacy_analysis_too_large

**Severity:** pause.

**Trigger:** The blueprint-architect's step-02 block 2.6 encountered a `selections[i]` whose sidecar is absent on disk (`sidecar_present == false` or the file is missing) AND whose prose `output_path` is larger than 60 KB on disk. Loading the prose whole would impose unacceptable architect-side context cost; the consultant is asked to regenerate the analyser so a structured sidecar is available. The 60 KB threshold is set per `framework/assets/analyses/sidecar-schema.md > Section 3.3` and reflects the largest acceptable single-analysis context contribution to the architect's read budget.

**Surface:** `AskUserQuestion` with the choice set `{ regenerate-and-retry, proceed-with-bounded-read, cancel }` plus an "Other" override.

- `regenerate-and-retry` — the architect halts step-02 and surfaces the regeneration advice in the handback message: *"Re-run `/analyse-requirement <method>` to regenerate the prose artefact and its sidecar, then re-invoke `/wireframe`."*. The wireframe pipeline does **not** write to `framework/state/.progress.json` (consistent with the wireframe-orch no-write-outside-`wireframes/`-and-`blueprints/` invariant); the architect simply exits cleanly and prior on-disk state (including the consultant's Stage-1b `analyses-inputs.json`) is reused on the next `/wireframe` invocation via the prior-set detection at step 0d. Highest-fidelity outcome.
- `proceed-with-bounded-read` — the architect proceeds with a deferred full-Read of `output_path` at the step that consumes it, drops the cached prose from in-memory state at step boundary, and records `[ANALYSIS-FALLBACK: <selections[i].name>] (>60 KB; consultant-accepted)` in the blueprint's Architect notes. Lower-fidelity outcome; downstream context-bloat risk is real and the architect's `cached_projections[<role>][<source-name>]` for this selection is best-effort prose extraction rather than structured payload.
- `cancel` — the architect halts step-02 and fails handback cleanly. No further work.

**Recovery:** `regenerate-and-retry` exits cleanly so the consultant re-runs `/analyse-requirement <method>` (which under the per-method follow-up rollout will emit the sidecar). `proceed-with-bounded-read` continues the run with the documented degraded-fidelity caveat. `cancel` exits cleanly.

**Refusal-registry schema field:** none specific. Distinct from `RF-08` because the sidecar is absent (one-cycle-deprecation legacy path), not stale (sha256 mismatch). The measurement is per-selection at architect-read time, not aggregated bytes at an orchestrator preflight.

## RF-10 — node_toolchain_missing

**Severity:** pause.

**Trigger:** The `prototype-app-scaffolder`'s preflight (or `framework/skills/scaffold-prototype-app.md`) finds Node.js / npm absent from PATH, or the Node major version is below what the prototype app requires (the template targets Next 16 / React 19 → Node ≥ 20). Fires only at scaffold time (Step F1 of `prototype-orch.md`), before `npm install`.

**Surface:** `AskUserQuestion` with the choice set `{ install-and-retry, abort }` plus an "Other" override.
- `install-and-retry` — the orchestrator writes `status: "setup-pending"` and `pending_setup: { predicate: "RF-10", advice_path: "framework/shared/setup-instructions/node-toolchain.md", since: <ISO-8601 UTC> }` to `framework/state/.prototype-progress.json` and exits cleanly. The consultant installs Node and re-invokes `/prototype`; resumption picks up at scaffold.
- `abort` — the scaffolder fails its handback; the orchestrator does not advance and does not write `.scaffold.json`.

**Recovery:** Read `framework/shared/setup-instructions/node-toolchain.md`. The `advice_path` is also surfaced in the question text.

**Refusal-registry schema field:** `setup_instructions_path` — `framework/shared/setup-instructions/node-toolchain.md`.

## RF-11 — playwright_browsers_missing

**Severity:** pause.

**Trigger:** `framework/skills/verify-prototype-build.md`'s smoke phase cannot launch a browser. The app's `playwright.config.ts` auto-detects an installed Chrome/Edge (and honours `PLAYWRIGHT_CHROME_PATH`/`PLAYWRIGHT_CHANNEL`), falling back to Playwright's bundled Chromium — and *none* of these resolves to a launchable binary (no system Chrome/Edge present and `npx playwright install` was never run; the launch errors with an "Executable doesn't exist" class message). Distinct from `RF-10` because the toolchain is present and lint/typecheck already passed; only the runtime browser is missing, and a degraded path (skip the smoke) exists.

**Surface:** `AskUserQuestion` with the choice set `{ install-and-retry, skip-smoke-with-warning, abort }` plus an "Other" override. The question text must include the install instructions path (`advice_path`) and the verbatim fidelity warning for the skip option.
- `install-and-retry` — the verify skill surfaces the advice path in its return; the orchestrator writes `status: "setup-pending"` + `pending_setup: { predicate: "RF-11", advice_path: "framework/shared/setup-instructions/playwright-browsers.md", since: <ISO-8601 UTC> }` to `framework/state/.prototype-progress.json` and exits cleanly. The generated route + spec remain on disk; re-invoke resumes at verify. Highest-assurance outcome.
- `skip-smoke-with-warning` — the verify gate degrades to `lint` + `tsc --noEmit` only; the runtime smoke is skipped. The verify skill returns `pass-with-warning`; the landing-updater records `smoke_skipped: true` for that prototype. Lower assurance — runtime render/click is not proven.
- `abort` — the verify skill returns a structured fail; the orchestrator does not advance to the landing update.

**Recovery:** `install-and-retry` exits cleanly so the consultant installs browsers per `framework/shared/setup-instructions/playwright-browsers.md` and re-invokes. `skip-smoke-with-warning` continues; `abort` halts.

**Refusal-registry schema field:** `setup_instructions_path` — `framework/shared/setup-instructions/playwright-browsers.md`.

## RF-12 — prototype_build_failed_after_retries

**Severity:** hard.

**Trigger:** `framework/skills/verify-prototype-build.md` reports a failing phase (`lint`, `tsc --noEmit`, or Playwright smoke) and the `prototype-generator`'s bounded retry budget (N = 2 regenerations of the offending surface) is exhausted with the failure persisting. Distinct from `RF-04` (single-artefact write-verification) — this is a failure of the **assembled app** to compile/lint/render.

**Surface:** Plain-text halt. The agent emits exactly one line — *"Aborting to protect your work — the prototype `<name-slug>` failed `<phase>` after 2 regeneration attempts: `<last error summary>`. Inspect the spec / shared components and re-invoke `/prototype`."* — and fails its handback. The generated (broken) route + spec remain on disk for inspection; the landing is **not** updated to list a broken prototype.

**Recovery:** The consultant inspects the build/test error, corrects the design spec or a shared component, and re-invokes `/prototype`; resumption picks up at generate/verify for that `<name-slug>`.

**Refusal-registry schema field:** none specific.

## RF-13 — prototype_app_scaffold_failed

**Severity:** hard.

**Trigger:** The `prototype-app-scaffolder` failed irrecoverably — the copy failed, `npm install` failed, or the empty-app build smoke (`scaffolding-instructions.md §6`) failed after one retry; OR a partial `prototypes/` tree — real scaffold files without a valid `.scaffold.json` — was detected (`scaffolding-instructions.md §1`). A `prototypes/` holding only the committed `.gitkeep` never-run marker is **not** partial and does **not** trigger this (it is treated as absent → scaffold proceeds).

**Surface:** Plain-text halt. The agent emits exactly one line — *"Aborting — scaffolding `prototypes/` failed at `<step>`: `<error>`. `.scaffold.json` was not written; remove any partial `prototypes/` tree and re-invoke `/prototype` to retry clean."* — and fails its handback. Because `.scaffold.json` is **not** written, the next run's idempotency gate treats the app as un-scaffolded.

**Recovery:** The consultant inspects (disk space, npm registry reachability, Node version), removes any partial `prototypes/` tree if instructed, and re-invokes.

**Refusal-registry schema field:** none specific.

## Anti-Patterns

- Do not invent a predicate ID. If no `RF-NN` covers the condition, append a new entry rather than overload an existing one.
- Do not surface a `pause` predicate via plain-text halt. The choice set is the contract — without it, the consultant cannot machine-readably resume.
- Do not surface a `hard` predicate via `AskUserQuestion`. There is no meaningful choice when prior work is at risk; halting cleanly is the only safe response.
- Do not write `status: setup-pending` for any predicate other than `RF-01`, `RF-10`, `RF-11`. The `pending_setup` block is reserved for those setup-required pauses: `RF-01` writes it to `framework/state/.progress.json`; `RF-10` / `RF-11` write it to `framework/state/.prototype-progress.json` (the prototype-orch's own progress file). A future predicate must explicitly register here before writing `pending_setup`. RF-06 deliberately does **not** write to `framework/state/.progress.json`; its `install-and-retry` path surfaces the advice in the handback message instead. RF-09 deliberately does **not** write either — the wireframe pipeline is bound by a no-write-outside-`wireframes/`-and-`blueprints/` invariant, and the consultant's Stage-1b `analyses-inputs.json` is reused on re-invocation via the wireframe-orch's prior-set detection.
- Do not silently downgrade a `hard` predicate to `pause`. `RF-04` halts; conflating it with a pausable refusal hides write failures.
