# CLAUDE.md

## 1. Project Purpose

**What.** Consultant-driven Claude Code workspace. Four slash commands (`/requirements`, `/design-system`, `/analyse`, `/review`) — each a prompt-only pipeline of markdown orchestrators + agents + skills — that turn loose client material into structured artefacts. No runtime code: every "agent" is an `.md` file Claude reads and adopts as persona.

**For.** Solo consultants / BAs running Claude Code locally to produce deterministic, citation-grounded handoff docs (requirements specs, design-token sets, OOUX / JTBD / use-case / data-model / sequence-diag / state-diag / activity-diag / user-journey maps, adversarial reviews) from briefs, decks, screenshots, spreadsheets, PDFs.

**Optimizes for.** Determinism + auditability over speed. Every fact in a final artefact must be traceable to either an input quote (sidecar NDJSON of `[SRC: C-NNN]` claims, verified verbatim) or a named provenance marker (`[AI-SUGGESTED]`, `[STANDARD-RULE: GR-NN]`, `[OUT-OF-SCOPE]`). Resumability: every pipeline checkpoints to disk so `/clear` + re-invoke continues at the first incomplete agent. Stand-alone pipelines: `/analyse`, `/review`, `/design-system` write only to their own dirs.

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
| `.claude/commands/` | Slash-command entrypoints (`start`, `requirements`, `design-system`, `analyse`, `review`). Each is a thin shim that names its orchestrator. |
| `framework/orchestrators/` | One orch per command. Owns control flow, progress/timing state, handback gates, reset procedure. Delegates all content work to agents. |
| `framework/agents/` | Agents = `.md` persona+workflow files. Claude adopts the persona, executes the workflow verbatim, hands back when DoD met. `requirements-{input-handler,drafter,resolver,merger}.md` for `/requirements`; `design-system-styler.md` (+ `design-system-styler/{steps,prompt-templates,data}/`) for `/design-system`; `agents/analyses/<method>-analyser.md` for `/analyse`; `agents/reviews/<method>-reviewer.md` (+ `adversarial-dimension-worker.md`) for `/review`. |
| `framework/skills/` | Reusable units of agent behaviour. Caller-agnostic, parameterised by inputs. Examples: `verify-artifact-write`, `check-context-bloat`, `classify-input-tier`, `convert-input-file`, `build-source-manifest`, `completeness-gap-pass`, `grounding-verifier`, `mermaid-validator`, `analysis-selector`, `review-selector`, `set-build-target`. Plus `map-<method>-to-ui.md` per analysis methodology. |
| `framework/assets/` | Read-only reference content: `template-*.md/html` (skeletons agents populate), `topics-*.md` (bijection invariants for gap-pass), `taxonomy-*.md`, `glossary.md`, `persona-llm.md`, `constraints.md`, `pattern-catalogue/` (auth/collections/feedback/forms/layouts/navigation/surfaces), `characters/*.md` (Unicorn voice per agent), `analyses/registry.md` + per-method reference/template, `reviews/registry.md` + per-method reference/template, `references/`. |
| `framework/shared/` | Cross-pipeline invariants and policy: `general-rules.md` (`GR-NN` deterministic defaults), `prototype-scope.md` + `.index.md` (in/out-scope filter for gap-pass), `prototype-invariants.md` (`PI-01..05` appended to every merged requirements.md), `refusal-registry.md` (`RF-NN`), `setup-instructions/{markitdown,playwright}.md`. |
| `framework/state/` | Runtime state. `.progress.json` (requirements-orch only — append-only event log + status + pending_setup), `timing.ndjson` (append-only observability across all runs, never truncated), `draft-fragments/`, resolver sidecars (`resolver-manifest.ndjson`, `resolver-answers.ndjson`, `resolver-cursor.json`). |
| `framework/dependency-graphs.md` | Mermaid dep graphs per orchestrator. Source of truth for what loads what. |
| `input/` | Consultant drop zone for `/requirements` inputs (briefs, decks, screenshots, PDFs, spreadsheets, .drawio, .yml). Input-handler enumerates here. `.converted.md` siblings produced by markitdown live here too. |
| `requirements/` | `/requirements` outputs only: `source-manifest.json`, `requirements-draft.md`, `draft-claims.ndjson`, `draft-claims-verification.ndjson`, `consultant-answers.md`, `requirements.md`. |
| `design-system/` | `/design-system` output: `design-system.md`. Workspace `.workspace/` is styler-owned. |
| `analyses/<METHOD>/` | `/analyse` outputs, one HTML per methodology (OOUX, JTBD, DATA-MODEL, USE-CASES, SEQUENCE-DIAGRAM, STATE-DIAGRAM, ACTIVITY-DIAGRAM, USER-JOURNEYS). |
| `reviews/<METHOD>/` | `/review` outputs (ADVERSARIAL MVP). |

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

- `/requirements` writes: `requirements/*`, `input/*.converted.md`, `framework/state/*`.
- `/design-system` writes: `design-system/*`. Reads `requirements/`+`framework/state/` only for context-bloat preflight.
- `/analyse` writes: `analyses/<METHOD>/*`. Reads `requirements/requirements.md` + same preflight exception.
- `/review` writes: `reviews/<METHOD>/*`. Same read scope as `/analyse`.

### Where new system elements go

| Adding | Goes in | Also touch |
|---|---|---|
| New slash command | `.claude/commands/<name>.md` (frontmatter `description:` + body that names the orchestrator) | New `framework/orchestrators/<name>-orch.md` |
| New orchestrator | `framework/orchestrators/<name>-orch.md` | New `framework/dependency-graphs.md` entry |
| New agent | `framework/agents/<pipeline>-<role>.md` (or subdir for multi-file agents like `design-system-styler/`) | Reference in orchestrator |
| New analysis methodology | `framework/agents/analyses/<method>-analyser.md` + reference + template + character + map skill | Append row to `framework/assets/analyses/registry.md` (status: `mvp`). Zero orch changes. |
| New review methodology | `framework/agents/reviews/<method>-reviewer.md` + reference + template + character | Append row to `framework/assets/reviews/registry.md` (status: `mvp`). Zero orch changes. |
| New skill | `framework/skills/<verb-noun>.md` | Reference from caller(s) |
| New asset (template, taxonomy, character) | `framework/assets/<kind>/<name>.md` (or `framework/assets/<name>.md`) | Reference from agent/skill |
| New shared rule (`GR-NN`) | Append to `framework/shared/general-rules.md` — never renumber | — |
| New refusal predicate (`RF-NN`) | Append to `framework/shared/refusal-registry.md` — never renumber | Add `setup_instructions_path` under `framework/shared/setup-instructions/` if applicable |
| New prototype invariant (`PI-NN`) | Append to `framework/shared/prototype-invariants.md` — never renumber | Merger auto-appends to `requirements.md` |
| New pipeline state file | `framework/state/<name>` + declare owner in orchestrator Tools section | — |

## 3. File and component placement rules

### Create new file

- New methodology / agent / skill / asset / shared-rule / refusal / invariant — see the matrix above. Always **append** to registries and `NN`-numbered files; never renumber.
- New pipeline output artefact → its pipeline's dedicated dir (`requirements/`, `design-system/`, `analyses/<METHOD>/`, `reviews/<METHOD>/`). **Never** write outside this dir from that pipeline.
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

Otherwise inline. Don't pre-extract for hypothetical future reuse. Counter-examples in this repo: `verify-artifact-write`, `check-context-bloat`, `classify-input-tier`, `convert-input-file`, `analysis-selector`, `review-selector`, `completeness-gap-pass`, `grounding-verifier`, `mermaid-validator` — each used by ≥ 2 callers with clean I/O.

Cross-pipeline policy (rules, scopes, refusals, invariants) goes in `framework/shared/`. Pipeline-specific procedure goes in `framework/skills/`. Pipeline-specific reference content goes in `framework/assets/`.

### Naming patterns

- **Commands.** `.claude/commands/<verb>.md`. Single lowercase verb.
- **Orchestrators.** `framework/orchestrators/<verb>-orch.md`.
- **Agents.** `framework/agents/<pipeline>-<role>.md` for requirements (`requirements-drafter.md`); `framework/agents/<plural-pipeline>/<method>-analyser.md` for analyse / review (`analyses/ooux-analyser.md`, `reviews/adversarial-reviewer.md`); multi-file agent → subdir with `steps/`, `prompt-templates/`, `data/`.
- **Skills.** `framework/skills/<verb-noun>.md` — verb-led, hyphenated, lowercase (`verify-artifact-write.md`, `check-context-bloat.md`, `build-source-manifest.md`, `set-build-target.md`).
- **Assets.**
  - Templates: `template-<thing>.{md,html}`.
  - References: `<method>-reference.md`.
  - Characters: `<persona-or-stage>.md` under `assets/characters/`.
  - Taxonomies: `taxonomy-<dimension>.md`.
  - Topics (bijection lists): `topics-<pipeline>.md`.
  - Registries: `registry.md` inside the pipeline-plural subdir.
- **Shared.** `<noun>.md` / `<noun>-registry.md` / `<noun>-invariants.md`. Stable-ID files use `NN-NN` numbering inside (`GR-NN`, `RF-NN`, `PI-NN`); never renumber.
- **State.** `.progress.json`, `timing.ndjson`, `<agent>-<role>.ndjson|json` under `framework/state/`.
- **Pipeline outputs.** `<artefact>.md`/`.json`/`.ndjson` under the pipeline's own dir. Analyses use UPPERCASE-METHOD subdirs (`analyses/OOUX/`, `analyses/DATA-MODEL/`); reviews same (`reviews/ADVERSARIAL/`).
- **Markers in content.** `[SRC: C-NNN]` (input-cited fact, sidecar-backed), `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` (drafter inference, resolver Q&A), `[STANDARD-RULE: GR-NN]` (deterministic, resolver skips), `[OUT-OF-SCOPE: domain-default]` (prototype-only, resolver skips). Stable-ID prefixes: `C-` (claims), `AI-` (suggestions), `GR-` (general rules), `RF-` (refusals), `PI-` (prototype invariants).
- **Timing events.** `run_start`, `run_end`, `stage_start`, `stage_end`, `substep_start`, `substep_end`, `consultant_prompted`, `consultant_responded` — all NDJSON, append-only via PowerShell `Add-Content`.
- **Progress events.** `called` / `completed` per agent.
