# CLAUDE.md

## 1. Project Purpose

**What.** Consultant-driven Claude Code workspace. Seven slash commands (`/requirements`, `/generate-prd`, `/design-system`, `/analyse-requirement`, `/analyse-inputs`, `/review-requirement`, `/review-inputs`) — each a prompt-only pipeline of markdown orchestrators + agents + skills — that turn loose client material into structured artefacts. No runtime code: every "agent" is an `.md` file Claude reads and adopts as persona. `/requirements` produces the LLM-audience FE spec; `/generate-prd` produces the human-audience PRD (strategic framing, success metrics, hypotheses, MVP phasing, risks, stakeholders) — fully independent of `/requirements`, can run before/after/alongside it. `/analyse-requirement` and `/review-requirement` lens the synthesised `requirements/requirements.md` (transform vs critique respectively); `/analyse-inputs` and `/review-inputs` lens the raw consultant-dropped material in `input/` (parallel registry-driven pipelines that share the input-handler agent with `/requirements` and `/generate-prd` and the `analysis-selector` skill across all three methodology pipelines).

**For.** Solo consultants / BAs running Claude Code locally to produce deterministic, citation-grounded handoff docs (requirements specs, design-token sets, OOUX / JTBD / use-case / data-model / sequence-diag / state-diag / activity-diag / user-journey maps, adversarial reviews) from briefs, decks, screenshots, spreadsheets, PDFs.

**Optimizes for.** Determinism + auditability over speed. Every fact in a final artefact must be traceable to either an input quote (sidecar NDJSON of `[SRC: C-NNN]` claims for `/requirements` drafts, verified verbatim; `[SRC: <filename>]` markers in `/analyse-inputs` and `/review-inputs` artefacts citing manifest rows) or a named provenance marker (`[AI-SUGGESTED]`, `[STANDARD-RULE: GR-NN]`, `[OUT-OF-SCOPE]`). Resumability: every pipeline checkpoints to disk so `/clear` + re-invoke continues at the first incomplete agent. Stand-alone pipelines: `/analyse-requirement`, `/analyse-inputs`, `/review-requirement`, `/review-inputs`, `/design-system` write only to their own dirs (the input-handler agent shared between `/requirements`, `/analyse-inputs`, and `/review-inputs` writes to `requirements/source-manifest.json` and `input/*.converted.md` — a documented cross-pipeline exception).

**Constraints.**
- Target domain = **data-management productivity apps** (CRUD-heavy). Prototype defaults assume that, not marketing/content.
- Output mode = **prototype** (client-stub simulated server, fixture data, visual-only validation — see `framework/shared/prototype-invariants.md` PI-01..PI-05) OR **application** (full backend reqs). Chosen once per manifest; durable in `requirements/source-manifest.json > target`.
- Every consultant interaction = foreground in-thread via `AskUserQuestion`. **No background/sub/async agents** for interactive surfaces — handback gates depend on same-thread acceptance.
- Every artefact write = `Write` then `framework/skills/verify-artifact-write.md` (sha256 + min-bytes). Mismatch → RF-04 hard halt.
- Refusal predicates (`framework/shared/refusal-registry.md`) are canonical: `RF-01` setup-pending, `RF-02` unsupported-file, `RF-03` no-supported-files, `RF-04` write-unverified, `RF-05` context-bloated.
- Inline `[SRC: C-NNN]` refs live in the draft + NDJSON sidecar; merger strips them. Final `requirements.md` is clean. `[AI-SUGGESTED]` reserved for facts not traceable to inputs and not covered by `GR-NN` — never widen this set.

## 2. Architecture

### Top-level dirs

| Path | Role |
|---|---|
| `.claude/commands/` | Slash-command entrypoints (`start`, `requirements`, `generate-prd`, `design-system`, `analyse-requirement`, `analyse-inputs`, `review-requirement`, `review-inputs`). Each is a thin shim that names its orchestrator. |
| `framework/orchestrators/` | One orch per command. Owns control flow, progress/timing state, handback gates, reset procedure. Delegates all content work to agents. |
| `framework/agents/` | Agents = `.md` persona+workflow files. Claude adopts the persona, executes the workflow verbatim, hands back when DoD met. `input-handler.md` (cross-pipeline — shared by `/requirements`, `/generate-prd`, `/analyse-inputs`, and `/review-inputs`; **single owner of the source-manifest lifecycle: create-if-absent, refresh-if-stale (with consultant consent at its step-0 drift prompt), no-op-if-fresh, halt-if-corrupt** — each calling orchestrator's Step 1 invokes it uniformly with `input_dir`, `manifest_path`, and `progress_path`, and the agent decides what the manifest needs); `requirements-{drafter,resolver,merger}.md` for `/requirements`; `prd-{drafter,resolver,merger}.md` for `/generate-prd`; `design-system-styler.md` (+ `design-system-styler/{steps,prompt-templates,data}/`) for `/design-system`; `agents/analyse-requirements/<method>-analyser.md` for `/analyse-requirement`; `agents/analyses-inputs/<method>-analyser.md` for `/analyse-inputs`; `agents/review-requirements/<method>-reviewer.md` (+ `adversarial-dimension-worker.md`) for `/review-requirement`; `agents/reviews-inputs/<method>-reviewer.md` for `/review-inputs` (planned — no agents on disk in framework first-ship). |
| `framework/skills/` | Reusable units of agent behaviour. Caller-agnostic, parameterised by inputs. Examples: `verify-artifact-write`, `check-context-bloat`, `check-manifest-freshness` (manifest-vs-disk drift detection, called by input-handler at its step 0), `classify-input-tier`, `convert-input-file`, `build-source-manifest` (parameterised `manifest_path` + optional `inherited_target` for refresh-path target preservation), `completeness-gap-pass`, `grounding-verifier`, `mermaid-validator`, `analysis-selector` (parameterised `registry_path` + optional `list_label` / `verb_label` — drives both analyses pipelines and `/review-inputs`), `review-selector` (drives `/review-requirement` only), `set-build-target`. Plus `map-<method>-to-ui.md` per analysis methodology. |
| `framework/assets/` | Read-only reference content: `template-*.md/html` (skeletons agents populate), `topics-*.md` (bijection invariants for gap-pass), `taxonomy-*.md`, `glossary.md`, `persona-llm.md`, `constraints.md`, `pattern-catalogue/` (auth/collections/feedback/forms/layouts/navigation/surfaces), `characters/*.md` (Unicorn voice per agent), `analyses/registry.md` + per-method reference/template (for `/analyse-requirement`), `analyses-inputs/registry.md` + per-method reference/template (for `/analyse-inputs`), `reviews/registry.md` + per-method reference/template (for `/review-requirement`), `reviews-inputs/registry.md` + per-method reference/template (for `/review-inputs`), `references/`. |
| `framework/shared/` | Cross-pipeline invariants and policy: `general-rules.md` (`GR-NN` deterministic defaults), `prototype-scope.md` + `.index.md` (in/out-scope filter for gap-pass), `prototype-invariants.md` (`PI-01..05` appended to every merged requirements.md), `refusal-registry.md` (`RF-NN`), `setup-instructions/{markitdown,playwright}.md`. |
| `framework/state/` | Runtime state. `.progress.json` (requirements-orch only — append-only event log + status + pending_setup; not written by `/analyse-inputs` or `/review-inputs` even when they invoke the shared input-handler, because both pass `progress_path: null`), `.prd-progress.json` (generate-prd-orch only — same shape as `.progress.json`; the `/generate-prd` pipeline invokes the input-handler with this path), `timing.ndjson` (append-only observability across all runs, never truncated; not written by `/analyse-inputs` or `/review-inputs`), `draft-fragments/`, resolver sidecars (`resolver-manifest.ndjson`, `resolver-answers.ndjson`, `resolver-cursor.json` for `/requirements`; `prd-resolver-manifest.ndjson`, `prd-resolver-answers.ndjson`, `prd-resolver-cursor.json` for `/generate-prd`). |
| `framework/dependency-graphs.md` | Mermaid dep graphs per orchestrator. Source of truth for what loads what. |
| `input/` | Consultant drop zone for inputs (briefs, decks, screenshots, PDFs, spreadsheets, .drawio, .yml). Read by `/requirements`, `/generate-prd`, `/analyse-inputs`, and `/review-inputs`. Input-handler enumerates here. `.converted.md` siblings produced by markitdown live here too. |
| `requirements/` | `/requirements` outputs: `source-manifest.json` (shared canonical manifest — also produced by `/generate-prd`, `/analyse-inputs`, and `/review-inputs` via their shared input-handler invocation), `requirements-draft.md`, `draft-claims.ndjson`, `draft-claims-verification.ndjson`, `consultant-answers.md`, `requirements.md`. Everything except `source-manifest.json` is `/requirements`-private. |
| `prd/` | `/generate-prd` outputs: `prd-draft.md`, `draft-claims.ndjson`, `draft-claims-verification.ndjson`, `consultant-answers.md`, `prd.md`. Human-audience PRD (problem, success metrics, hypotheses, MVP phasing, risks, stakeholders). Citation IDs are namespaced `PC-NNN` and `PAI-NNN` to avoid visual collision with requirements-pipeline `C-NNN` / `AI-NNN`. All files `/generate-prd`-private; only `requirements/source-manifest.json` is shared upstream. |
| `design-system/` | `/design-system` output: `design-system.html` — self-contained HTML with an embedded `<script type="application/json" id="design-tokens">` block (LLM-readable token set + provenance) and visual sections rendering swatches / typography specimens / shadow / motion / contrast pairs with inline styles (consultant-readable via `file://`). Workspace `.workspace/` is styler-owned. |
| `analyse-requirements/<METHOD>/` | `/analyse-requirement` outputs, one HTML or MD per methodology (OOUX, JTBD, DATA-MODEL, USE-CASES, SEQUENCE-DIAGRAM, STATE-DIAGRAM, ACTIVITY-DIAGRAM, USER-JOURNEYS, TASK-FLOWS, OPPORTUNITY-SOLUTION-TREES, FIVE-WHYS, GLOSSARY). |
| `analyse-inputs/<METHOD>/` | `/analyse-inputs` outputs, one artefact per methodology (each methodology ships in its own follow-up PR; framework first-ship has zero MVP rows). |
| `review-requirements/<METHOD>/` | `/review-requirement` outputs (ADVERSARIAL, FIRST-PRINCIPLES, TEN-BA-QUESTIONS, TEN-UX-QUESTIONS, USER-STORIES MVP). |
| `review-inputs/<METHOD>/` | `/review-inputs` outputs, one artefact per methodology (each methodology ships in its own follow-up PR; framework first-ship has zero MVP rows — selector returns `empty-registry` and the orchestrator exits cleanly). |

### Data flow

1. Consultant types `/start` or a specific slash command → command shim → orchestrator adopts persona.
2. Orchestrator runs **preflight gates** (prerequisite check, context-bloat skill, prior-progress detection, `AskUserQuestion` for start-fresh vs continue / overwrite vs keep).
3. Orchestrator writes `called` event to `.progress.json` + `stage_start` to `timing.ndjson`, then invokes the next agent **in the foreground (same thread)**.
4. Agent reads its inputs (manifest, prior artefacts, assets/templates/characters/shared/skills it transitively depends on per `framework/dependency-graphs.md`), executes its workflow, writes its artefact, calls `verify-artifact-write` (sha256), runs self-validation, prompts consultant for accept via `AskUserQuestion`.
5. Agent hands back. Orchestrator writes `completed` + `stage_end`. Repeats per step until DoD.
6. Final acceptance → `status: complete` + `run_end` event.

### Separation of concerns

- **Orchestrator** = control flow only. Reads progress/timing, deletes during reset, writes events. Never edits content artefacts (one exception: drafter handback gate reads `draft-claims-verification.ndjson` summary line).
- **Agent** = content production. Reads inputs, writes its one artefact, owns its self-validation + handback. Never writes outside its scoped output paths.
- **Skill** = reusable procedure. Parameterised by inputs. Returns `pass | <RF-NN> trigger | structured-row | ok`. No file I/O outside its declared inputs/outputs.
- **Asset** = read-only reference. Templates, registries, taxonomies, characters, pattern catalogue.
- **Shared** = cross-pipeline invariants (rules, scope, refusals, invariants, setup-instructions). Read-only; mutated only by appending new IDs.
- **State** = orchestrator/agent runtime scratch. Each owner declared in the orchestrator's Tools section.

### Stand-alone constraints (write isolation)

- `/requirements` writes: `requirements/*`, `input/*.converted.md`, `framework/state/*` (the input-handler invocation at Step 1 produces `requirements/source-manifest.json` and `input/*.converted.md`).
- `/generate-prd` writes: `prd/*`, `framework/state/.prd-progress.json`, `framework/state/prd-resolver-*.{ndjson,json}`, `framework/state/timing.ndjson` (append only). Reads `requirements/source-manifest.json` (manifest) + `input/*` (per manifest rows) + same preflight exception. Documented cross-pipeline exception (inherited from the shared input-handler's contract): writes `requirements/source-manifest.json` and `input/*.converted.md` siblings when the manifest is absent or stale at orchestrator Step 1 (the input-handler's step 0 decides; create or refresh paths both write). Fully independent of `requirements/requirements.md` — never reads or writes it.
- `/design-system` writes: `design-system/*`. Reads `requirements/`+`framework/state/` only for context-bloat preflight.
- `/analyse-requirement` writes: `analyse-requirements/<METHOD>/*`. Reads `requirements/requirements.md` + same preflight exception.
- `/analyse-inputs` writes: `analyse-inputs/<METHOD>/*`. Reads `requirements/source-manifest.json` (manifest) + `input/*` (per manifest rows, including multimodal vision for `Native-multimodal` tier) + same preflight exception. Documented cross-pipeline exception: when the manifest is absent or stale at orchestrator Step 1, the shared `framework/agents/input-handler.md` agent is invoked and writes `requirements/source-manifest.json` and `input/*.converted.md` siblings (the canonical manifest is shared with `/requirements`, `/generate-prd`, and `/review-inputs`; downstream `/requirements`-private artefacts are never written by `/analyse-inputs`). The input-handler's step 0 decides between create / refresh / no-op / halt; only create and refresh write. Does **not** write `framework/state/*` on any branch (input-handler invoked with `progress_path: null`).
- `/review-requirement` writes: `review-requirements/<METHOD>/*`. Same read scope as `/analyse-requirement`.
- `/review-inputs` writes: `review-inputs/<METHOD>/*`. Reads `requirements/source-manifest.json` (manifest) + `input/*` (per manifest rows, including multimodal vision for `Native-multimodal` tier) + same preflight exception. Documented cross-pipeline exception: when the manifest is absent or stale at orchestrator Step 1, the shared `framework/agents/input-handler.md` agent is invoked and writes `requirements/source-manifest.json` and `input/*.converted.md` siblings (the canonical manifest is shared with `/requirements`, `/generate-prd`, and `/analyse-inputs`; downstream `/requirements`-private artefacts are never written by `/review-inputs`). The input-handler's step 0 decides between create / refresh / no-op / halt; only create and refresh write. Does **not** write `framework/state/*` on any branch (input-handler invoked with `progress_path: null`).

### Where new system elements go

| Adding | Goes in | Also touch |
|---|---|---|
| New slash command | `.claude/commands/<name>.md` (frontmatter `description:` + body that names the orchestrator) | New `framework/orchestrators/<name>-orch.md` |
| New orchestrator | `framework/orchestrators/<name>-orch.md` | New `framework/dependency-graphs.md` entry |
| New agent | `framework/agents/<pipeline>-<role>.md` (or subdir for multi-file agents like `design-system-styler/`) | Reference in orchestrator |
| New analysis methodology (lenses `requirements/requirements.md`) | `framework/agents/analyses/<method>-analyser.md` + reference + template + character + map skill | Append row to `framework/assets/analyses/registry.md` (status: `mvp`). Zero orch changes. |
| New input-analysis methodology (lenses raw `input/` via manifest) | `framework/agents/analyses-inputs/<method>-analyser.md` + `framework/assets/analyses-inputs/<method>-reference.md` + template (under `framework/assets/analyses-inputs/`) + character (under `framework/assets/characters/<method>-inputs-analysis.md`) + map skill (or reuse the existing `map-<method>-to-ui.md` if source-agnostic) | Promote a row in `framework/assets/analyses-inputs/registry.md` from `status: future` to `status: mvp` and fill all eight fields; `output_path` lives under `analyse-inputs/<METHOD>/`. Zero orch changes. |
| New review methodology (critiques `requirements/requirements.md`) | `framework/agents/reviews/<method>-reviewer.md` + reference + template + character | Append row to `framework/assets/reviews/registry.md` (status: `mvp`). Zero orch changes. |
| New input-review methodology (critiques raw `input/` via manifest) | `framework/agents/reviews-inputs/<method>-reviewer.md` + `framework/assets/reviews-inputs/<method>-reference.md` + template (under `framework/assets/reviews-inputs/`) + character (under `framework/assets/characters/<method>-inputs-review.md`) | Promote a row in `framework/assets/reviews-inputs/registry.md` from `status: future` to `status: mvp` and fill all eight remaining fields; `output_path` lives under `review-inputs/<METHOD>/`. Zero orch changes. |
| New skill | `framework/skills/<verb-noun>.md` | Reference from caller(s) |
| New asset (template, taxonomy, character) | `framework/assets/<kind>/<name>.md` (or `framework/assets/<name>.md`) | Reference from agent/skill |
| New shared rule (`GR-NN`) | Append to `framework/shared/general-rules.md` — never renumber | — |
| New refusal predicate (`RF-NN`) | Append to `framework/shared/refusal-registry.md` — never renumber | Add `setup_instructions_path` under `framework/shared/setup-instructions/` if applicable |
| New prototype invariant (`PI-NN`) | Append to `framework/shared/prototype-invariants.md` — never renumber | Merger auto-appends to `requirements.md` |
| New pipeline state file | `framework/state/<name>` + declare owner in orchestrator Tools section | — |

## 3. File and component placement rules

### Create new file

- New methodology / agent / skill / asset / shared-rule / refusal / invariant — see the matrix above. Always **append** to registries and `NN`-numbered files; never renumber.
- New pipeline output artefact → its pipeline's dedicated dir (`requirements/`, `design-system/`, `analyse-requirements/<METHOD>/` for `/analyse-requirement`, `analyse-inputs/<METHOD>/` for `/analyse-inputs`, `review-requirements/<METHOD>/` for `/review-requirement`, `review-inputs/<METHOD>/` for `/review-inputs`). **Never** write outside this dir from that pipeline (the documented `/analyse-inputs` and `/review-inputs` → `requirements/source-manifest.json` + `input/*.converted.md` exception is inherited from the shared input-handler's contract and is bounded to those two paths).
- New `setup-instructions/<tool>.md` when an `RF-01`-style pause needs out-of-band install steps.
- New `template-<thing>.md/html` in `framework/assets/` when an agent needs a populate-top-to-bottom skeleton.

### Edit existing file

- Tweaking an agent's workflow, handback gate, timing events → its single `.md`. Keep workflow + Self-validation + DoD + Anti-Patterns sections in sync.
- Adjusting an orchestrator's pipeline steps → its single `<name>-orch.md`. Update **Tools**, **Self-validation**, **Anti-Patterns**, **Inputs/Output** together.
- Adding a `[STANDARD-RULE: GR-NN]` answer → append rule to `framework/shared/general-rules.md`. The drafter's `completeness-gap-pass.md` picks it up automatically when its scope predicate matches.
- Promoting a registry row from `future` to `mvp` → fill the eight registry fields and ship the agent + reference + template + character + map skill. Orchestrator unchanged.
- Tuning the context-bloat heuristic → `framework/skills/check-context-bloat.md` (`bytes_total > 250_000` or `row_count > 25`).
- Updating dep graphs after any structural edit → `framework/dependency-graphs.md`.

### Create abstraction (extract a skill or shared file)

Extract only when **all** of:
1. The same procedure is invoked by ≥ 2 agents or orchestrators (or will be on a near-term planned change).
2. The procedure has clean parameter inputs and a single structured return (`pass | RF-NN trigger | row | ok`).
3. Extracting does not require the abstraction to know caller-specific state.

Otherwise inline. Don't pre-extract for hypothetical future reuse. Counter-examples in this repo: `verify-artifact-write`, `check-context-bloat`, `check-manifest-freshness`, `classify-input-tier`, `convert-input-file`, `analysis-selector`, `review-selector`, `completeness-gap-pass`, `grounding-verifier`, `mermaid-validator` — each used by ≥ 2 callers with clean I/O.

Cross-pipeline policy (rules, scopes, refusals, invariants) goes in `framework/shared/`. Pipeline-specific procedure goes in `framework/skills/`. Pipeline-specific reference content goes in `framework/assets/`.

### Canonical-source rule (definitions only)

Every field name, NDJSON row schema, vocabulary term, stable-ID (e.g. `GR-NN`, `RF-NN`, `PI-NN`, `C-NNN`, `AI-NNN`, `PC-NNN`, `PAI-NNN`), and registry must have exactly **one** file that *defines* it. Every other file that uses it references the canonical file by name or link — never re-defines it. If two files appear to redefine the same definition, that is a structural bug; pick the canonical owner and replace the other with a reference.

Scope is **definitions only**, not procedures. Procedural extraction continues to follow the "Create abstraction" criteria above (extract only when ≥ 2 callers exist with clean I/O).

**What this rule does *not* forbid.** Mechanically derived embedding — e.g. the merger appending `PI-01..05` verbatim from `framework/shared/prototype-invariants.md` into every `requirements.md`, or `[SRC: C-NNN]` markers being copied from `requirements/draft-claims.ndjson` into `requirements-draft.md` — is *not* a violation, because the embedded copy is produced from the canonical source by a named skill or agent step. Likewise, an agent's *Self-validation* section restating constraints that live canonically in `framework/shared/` is *not* a violation: the restatement is for fail-closed resilience and auditability, and adds no new definitional content.

**Where canonical owners live today (non-exhaustive, for orientation).**
- Stable-ID registries: `framework/shared/general-rules.md` (`GR-NN`), `framework/shared/refusal-registry.md` (`RF-NN`), `framework/shared/prototype-invariants.md` (`PI-NN`).
- Methodology registries: `framework/assets/{analyses,analyses-inputs,reviews,reviews-inputs}/registry.md`.
- Pipeline loading graph: `framework/dependency-graphs.md`.
- Source manifest: `requirements/source-manifest.json` (owned by `framework/agents/input-handler.md`).

When introducing a new definition, decide its canonical home first, place it there, and reference it from anywhere else that uses it.

### Naming patterns

- **Commands.** `.claude/commands/<verb>.md`. Single lowercase verb.
- **Orchestrators.** `framework/orchestrators/<verb>-orch.md`.
- **Agents.** `framework/agents/<pipeline>-<role>.md` for requirements-pipeline-private agents (`requirements-drafter.md`); `framework/agents/<role>.md` (no pipeline prefix) for cross-pipeline shared agents (`input-handler.md` — shared between `/requirements`, `/analyse-inputs`, and `/review-inputs`); `framework/agents/<plural-pipeline>/<method>-(analyser|reviewer).md` for analyse / review (`analyses/ooux-analyser.md`, `analyses-inputs/glossary-analyser.md`, `reviews/adversarial-reviewer.md`, `reviews-inputs/<method>-reviewer.md`); multi-file agent → subdir with `steps/`, `prompt-templates/`, `data/`.
- **Skills.** `framework/skills/<verb-noun>.md` — verb-led, hyphenated, lowercase (`verify-artifact-write.md`, `check-context-bloat.md`, `check-manifest-freshness.md`, `build-source-manifest.md`, `set-build-target.md`).
- **Assets.**
  - Templates: `template-<thing>.{md,html}`.
  - References: `<method>-reference.md`.
  - Characters: `<persona-or-stage>.md` under `assets/characters/`.
  - Taxonomies: `taxonomy-<dimension>.md`.
  - Topics (bijection lists): `topics-<pipeline>.md`.
  - Registries: `registry.md` inside the pipeline-plural subdir.
- **Shared.** `<noun>.md` / `<noun>-registry.md` / `<noun>-invariants.md`. Stable-ID files use `NN-NN` numbering inside (`GR-NN`, `RF-NN`, `PI-NN`); never renumber.
- **State.** `.progress.json`, `timing.ndjson`, `<agent>-<role>.ndjson|json` under `framework/state/`.
- **Pipeline outputs.** `<artefact>.md`/`.html`/`.json`/`.ndjson` under the pipeline's own dir. `/design-system` writes `design-system/design-system.html` (self-contained HTML with embedded JSON token block). Analyses use UPPERCASE-METHOD subdirs (`analyse-requirements/OOUX/`, `analyse-requirements/DATA-MODEL/`); input-analyses use UPPERCASE-METHOD subdirs under `analyse-inputs/` (`analyse-inputs/THEMATIC-ANALYSIS/`, `analyse-inputs/OPPORTUNITY-SOLUTION-TREES/`); requirement-doc reviews same (`review-requirements/ADVERSARIAL/`); input-reviews use UPPERCASE-METHOD subdirs under `review-inputs/` (`review-inputs/COMPLETENESS-REVIEW/`, `review-inputs/AMBIGUITY-REVIEW/`).
- **Markers in content.** `[SRC: C-NNN]` (input-cited fact in the `/requirements` draft, sidecar-backed by `requirements/draft-claims.ndjson` and verified verbatim — used only inside `requirements/requirements-draft.md`; the merger strips them so the final `requirements.md` is clean), `[SRC: <filename>]` (filename-cited fact in `/analyse-inputs` and `/review-inputs` artefacts, payload is the manifest row's `filename` field — never used inside `/requirements` artefacts), `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` (drafter inference, resolver Q&A), `[STANDARD-RULE: GR-NN]` (deterministic, resolver skips), `[OUT-OF-SCOPE: domain-default]` (prototype-only, resolver skips). Stable-ID prefixes: `C-` (claims), `AI-` (suggestions), `GR-` (general rules), `RF-` (refusals), `PI-` (prototype invariants).
- **Timing events.** `run_start`, `run_end`, `stage_start`, `stage_end`, `substep_start`, `substep_end`, `consultant_prompted`, `consultant_responded` — all NDJSON, append-only via PowerShell `Add-Content`.
- **Progress events.** `called` / `completed` per agent.

## 4. Collaboration Style & Feedback
- **Role:** You are a senior peer and a strategic thinking partner. Treat me as an equal ally.
- **Pushback:** If you disagree, say so and explain why. If my claim seems incorrect, explain why and support your view.
- **Devil's Advocate:** Play devil's advocate when I propose a solution, identifying 2-3 potential blind spots or assumptions that need testing.
- **Uncertainty:** Do not smooth over uncertainty to sound authoritative. I would rather have an accurate map of what you know and do not know.
