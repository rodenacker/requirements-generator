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

**Trigger:** A required external tool is not in the available tool list at preflight time. MVP scope: `mcp__markitdown__convert_to_markdown` is required when at least one input file's tier is `Supported-via-MCP`.

**Surface:** `AskUserQuestion` with the choice set `{ continue-skip, continue-later }` plus an "Other" override.
- `continue-skip` — the agent proceeds with the missing tool absent; every file that needed the tool reclassifies to `Unsupported` for this run and is recorded in the manifest with `conversions_applied: "skipped — RF-01"`.
- `continue-later` — the agent writes `status: setup-pending` and `pending_setup: { predicate: "RF-01", advice_path: "framework/shared/setup-instructions/markitdown.md", since: <ISO-8601 UTC> }` to `framework/state/.progress.json` and exits cleanly. The consultant installs the dependency and re-invokes the pipeline.

**Recovery:** Read `framework/shared/setup-instructions/markitdown.md`. The `advice_path` is also surfaced in the question text.

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

## RF-05 — prior_stage_context_bloated

**Severity:** pause.

**Trigger:** `framework/skills/check-context-bloat.md` reports the bloat heuristic exceeded. Surfaced by both orchestrators that call the skill, with caller-specific recovery semantics described in **Surface variants** below.

**Surface:** `AskUserQuestion` with the choice set `{ proceed-without-clear, continue-later }`. The `proceed-without-clear` branch always advances; the `continue-later` branch always exits cleanly. What differs between callers is whether `continue-later` writes a `status` field to `framework/state/.progress.json` before exiting.

### Surface variants

- **requirements-orch variant** — fired immediately before each `called` event after the input-handler's `completed` event has been written. Skill is invoked with `artefact_dir = requirements/`, `manifest_path = requirements/source-manifest.json`, `progress_path = framework/state/.progress.json`.
    - `proceed-without-clear` — the orchestrator writes the `called` event and proceeds. The override is recorded by the `called` event itself; no additional sidecar.
    - `continue-later` — the orchestrator writes `status: "context-bloated"` to `framework/state/.progress.json`, does **not** write the `called` event, and exits cleanly. The consultant runs `/clear` and re-invokes `/requirements`; rerun detection resumes at the same step.

- **design-system-orch variant** — fired once at startup in step-0b (after the prior-artefact gate, before the styler is invoked). Skill is invoked with the same three parameter values as the requirements variant — the design-system pipeline uses prior `/requirements` state on disk as a proxy for in-conversation bloat. The design-system pipeline has no progress file of its own and is bound by a no-write-outside-`design-system/` invariant, so this variant deliberately omits the `status` write.
    - `proceed-without-clear` — the orchestrator proceeds to step 1 and invokes the styler.
    - `continue-later` — the orchestrator surfaces a *"run `/clear` and re-invoke `/design-system`"* message and exits cleanly. **No write to `framework/state/.progress.json`.** No `design-system/` side effects. This mirrors the RF-06 `install-and-retry` pattern, which already documents that the design-system pipeline cannot write to `framework/state/.progress.json`.

**Recovery:** The standard path is `/clear` then re-invoke the same orchestrator. `proceed-without-clear` is the override for short cases where the consultant judges the bloat tolerable.

## RF-06 — style_extraction_dependency_missing

**Severity:** pause.

**Trigger:** The design-system-styler's preflight in `step-04-site-fetching.md` does not find `mcp__playwright__browser_navigate` in the available tool list, AND the consultant supplied a non-null `{{reference_url}}` in step-02. Distinct from `RF-01` because the styler has a degraded-fidelity fallback path (WebFetch) that the input-handler does not, so the choice set is three-way rather than two-way.

**Surface:** `AskUserQuestion` with the choice set `{ install-and-retry, use-webfetch-fallback, drop-url }` plus an "Other" override. The question text must include the install instructions path (`advice_path`) and the verbatim fidelity warning for the WebFetch option.

- `install-and-retry` — the agent halts step-04, writes `status: setup-pending` and `pending_setup: { predicate: "RF-06", advice_path: "framework/shared/setup-instructions/playwright.md", since: <ISO-8601 UTC> }` semantics into the styler's own state (the styler does not write `framework/state/.progress.json` per the stand-alone constraint — it surfaces the install path in the handback message and exits cleanly so the consultant installs Playwright and re-runs `/design-system`). Highest-fidelity outcome.
- `use-webfetch-fallback` — the agent proceeds via the legacy WebFetch two-pass path. Sets `extraction_method = "webfetch-fallback"` in `metadata.json`, does not write `computed-tokens.json`. The consultant's choice is the contract — the agent does not re-warn during the run. Lower-fidelity outcome; many tokens may end up `inferred-from-domain` instead of `extracted-from-url`.
- `drop-url` — the agent sets `{{reference_url}} = null`, records `extraction_status = playwright_unavailable`, and skips to `step-05b-domain-inference.md`. Most predictable outcome; tokens uniformly `inferred-from-domain`.

**Recovery:** `install-and-retry` exits cleanly so the consultant installs Playwright per `framework/shared/setup-instructions/playwright.md` and re-invokes `/design-system`. `use-webfetch-fallback` and `drop-url` continue the run.

**Refusal-registry schema field:** `setup_instructions_path` — same field as RF-01, pointing here at `framework/shared/setup-instructions/playwright.md`.

## Anti-Patterns

- Do not invent a predicate ID. If no `RF-NN` covers the condition, append a new entry rather than overload an existing one.
- Do not surface a `pause` predicate via plain-text halt. The choice set is the contract — without it, the consultant cannot machine-readably resume.
- Do not surface a `hard` predicate via `AskUserQuestion`. There is no meaningful choice when prior work is at risk; halting cleanly is the only safe response.
- Do not write `status: setup-pending` or `status: context-bloated` for any predicate other than `RF-01` and `RF-05` respectively. The `pending_setup` block is reserved for `RF-01` until a future predicate explicitly registers as a setup-required pause. `RF-05`'s `status: context-bloated` write is specific to the **requirements-orch surface variant**; the **design-system-orch variant** of `RF-05` deliberately does not write, for the same reason `RF-06` does not — the design-system pipeline is bound by a no-write-outside-`design-system/` invariant. RF-06 deliberately does **not** write to `framework/state/.progress.json` either; its `install-and-retry` path surfaces the advice in the handback message instead.
- Do not silently downgrade a `hard` predicate to `pause`. `RF-04` halts; conflating it with a pausable refusal hides write failures.
