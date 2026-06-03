# CLAUDE.md

## 1. Project Purpose

**What.** Consultant-driven Claude Code workspace. Ten slash commands — each a prompt-only pipeline of markdown orchestrators + agents + skills — turn loose client material into structured artefacts. No runtime code: every "agent" is an `.md` file Claude reads and adopts as persona (the one exception: `/prototype` *generates* a real client-side Next.js app under `prototypes/`).

| Command | Audience / role |
|---|---|
| `/start` | Dispatcher — lists the other commands and launches the chosen one. |
| `/requirements` | LLM-audience FE spec (`requirements/requirements.md`). |
| `/generate-prd` | Human-audience PRD (`prd/prd.md`) — strategic framing, success metrics, hypotheses, MVP phasing, risks, stakeholders. Independent of `/requirements`; can run before/after/alongside. |
| `/design-system` | Brand-token brief (`design-system/design-system.html`). |
| `/analyse-requirement` | Lens-transforms `requirements/requirements.md` (e.g. OOUX, DATA-MODEL, USE-CASES, USER-JOURNEYS, FIVE-WHYS, GLOSSARY, TRADE-OFF-DIMENSIONS). |
| `/analyse-inputs` | Lens-transforms raw `input/` material (e.g. THEMATIC-ANALYSIS, OOUX, JTBD, SWIM-LANE-PROCESS-MAPPING). |
| `/review-requirement` | Critiques `requirements/requirements.md` (ADVERSARIAL, FIRST-PRINCIPLES, TEN-BA / TEN-UX QUESTIONS, USER-STORIES). |
| `/review-inputs` | Critiques raw `input/` material (ADVERSARIAL, COMPLETENESS-REVIEW, AMBIGUITY-REVIEW, GAP-ANALYSIS). |
| `/wireframe` | 2–3 parallel low-fi HTML wireframe variants for a scope of `requirements/requirements.md`. Persona-bound; variants diverge on trade-off dimensions **and** information architecture (per-surface realization: standalone screen / inline drawer / inline-expand / modal / wizard-split); divergence axes + persona bindings are **goal-driven** (extrapolated from §3 personas + §4 goals by `divergence-heuristics.md`, surfaced as a recommended default at the scope-selector confirm gate). Each variant is also **posture-bound**: the divergence heuristic auto-recommends a **UX posture** (`framework/assets/wireframes/design-philosophies.md`, the cross-pipeline registry) per variant, which the architect consumes as a structural/realization + naming overlay (it biases pattern picks but does **not** change the variant's dimension positions, so the comparison stays single-axis). Full requirement-ID traceability via `data-src` + `data-prop`; metadata-only `index.html` landing with side-by-side screen links + a decomposition/structure comparison row. Cross-pipeline `blueprint-architect` agent + `scope-selector` skill + `design-philosophies.md` posture registry reusable by `/prototype`. |
| `/prototype` | One hi-fi, **clickable, client-side-only** React/Next.js prototype per run of a scope of `requirements/requirements.md`, accumulating in **one shared app** (`prototypes/`, scaffolded once from `template/`) reachable from a single landing page. **Look & feel is brand-locked and identical across all prototypes** (one `theme.css` from `/design-system` → consultant → defaults); divergence between prototypes is **pure UX** — a selectable named **UX posture** (`framework/assets/wireframes/design-philosophies.md`, the cross-pipeline registry shared with `/wireframe`) + trade-off positions (D1–D5) reshape layout + workflows. Reuses `scope-selector` (`propose_divergence_axes:false`) + `blueprint-architect` (`variants_output_path:null`, blueprint-only). Pipeline: scope+name → inputs (A requirement / B analyse-requirement / C analyse-inputs / D wireframes / E input docs) → blueprint → purpose+posture+positions → design-spec **draft→resolve→merge** → scaffold-if-needed → **parallel per-surface generation** → verify (lint+typecheck+build+Playwright smoke) → landing update. Anti-fabrication via blueprint Property closed sets (`data-prop`); honours PI-01..PI-08. |

**For.** Solo consultants / BAs running Claude Code locally to produce deterministic, citation-grounded handoff docs from briefs, decks, screenshots, spreadsheets, PDFs.

**Optimizes for.** Determinism + auditability over speed. Every fact in a final artefact must be traceable to an input citation (`[SRC: C-NNN]`, `[SRC: <filename>]`, `data-src="<F-NN,BR-NN,UI-NN>"`) or a named provenance marker (`[AI-SUGGESTED]`, `[STANDARD-RULE: GR-NN]`, `[OUT-OF-SCOPE]`). Resumability: every pipeline checkpoints to disk so `/clear` + re-invoke continues at the first incomplete agent.

**Constraints.**
- Target domain = **data-management productivity apps** (CRUD-heavy). Prototype defaults assume that, not marketing/content.
- Output mode = **prototype** (client-stub simulated server, fixture data — see `framework/shared/prototype-invariants.md` PI-01..PI-08) OR **application** (full backend reqs). Chosen once per manifest; durable in `requirements/source-manifest.json > target`.
- Every consultant interaction = foreground in-thread via `AskUserQuestion`. **No background/sub/async agents** for interactive surfaces — handback gates depend on same-thread acceptance.
- Every artefact write = `Write` then `framework/skills/verify-artifact-write.md` (sha256 + min-bytes). Mismatch → RF-04 hard halt.
- Refusal predicates are canonical in `framework/shared/refusal-registry.md` — never paraphrase or redefine.
- Inline `[SRC: C-NNN]` refs live in the draft + NDJSON sidecar; the merger **retains** them in the final `requirements.md` as inline provenance for downstream LLM consumers (it strips only the resolution markers `[AI-SUGGESTED]`/`[STANDARD-RULE]`/`[OUT-OF-SCOPE]`). The `draft-claims.ndjson` sidecar stays the authoritative store of the verbatim source quotes (joined on the retained `C-NNN` tags). `[AI-SUGGESTED]` reserved for facts not traceable to inputs and not covered by `GR-NN` — never widen this set.
- **Wireframe pipeline never invents object properties.** Every data-bound element (form input, table column, detail row, status chip) carries a `data-prop` naming a §7 data-shape property (`Shape.Field`) or F-NN-named parameter (`F-NN:ParamName`). The blueprint's per-surface `Properties` column is the canonical closed set (mirrored into each variant's `surface_plan` as per-physical-screen `covers_properties`); properties outside that set are fabrications and a `RF-04`-class self-validation FAIL. The contract survives a fold: a surface realized as an inline drawer/modal still stamps its `data-prop`s on the host screen's drawer/modal sub-tree. UI-only controls (search, sort, pagination, filter chips, save/cancel, dropzones) are exempt. `data-src="F-NN"` alone is insufficient justification — the field's property must be in the blueprint's closed set.

## 2. Architecture

### Top-level dirs

| Path | Role |
|---|---|
| `.claude/commands/` | Slash-command entrypoints. Each is a thin shim that names its orchestrator. |
| `framework/orchestrators/` | One orch per command. Owns control flow, progress/timing state, handback gates, reset procedure. Delegates all content work to agents. |
| `framework/agents/` | Agents = `.md` persona+workflow files. Cross-pipeline agents have no pipeline prefix (`input-handler.md` — shared by `/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`; **single owner of the source-manifest lifecycle**; `blueprint-architect.md` + subdir — shared by `/wireframe` and `/prototype`; **single owner of the blueprint IR**, no pattern bindings). Pipeline-private agents use `<pipeline>-<role>.md` (`requirements-{drafter,resolver,merger}`, `prd-{drafter,resolver,merger}`, `design-system-styler/`, `wireframe-variant-generator/`, `wireframe-comparator.md`, `prototype-{spec-drafter,spec-resolver,spec-merger,app-scaffolder,generator/,landing-updater}`). Methodology agents nest under their pipeline: `agents/{analyses,analyses-inputs,reviews,reviews-inputs}/<method>-(analyser\|reviewer).md`. |
| `framework/skills/` | Reusable units of agent behaviour. Caller-agnostic, parameterised. Examples: `verify-artifact-write`, `check-context-bloat`, `check-manifest-freshness`, `classify-input-tier`, `convert-input-file`, `build-source-manifest`, `completeness-gap-pass`, `grounding-verifier`, `mermaid-validator`, `analysis-selector` (drives all four methodology selectors — `/analyse-requirement`, `/analyse-inputs`, `/review-inputs`, and `/review-requirement`; clusters methodologies by lens `group` with a `★ suggested next` flag derived purely from on-disk `output_path` presence — the former pipeline-private `review-selector` was retired), `set-build-target`, `scope-selector` (cross-pipeline — `/wireframe` + `/prototype`), `select-supporting-analyses` (wireframe-private — on-disk-presence filter is load-bearing), `check-pattern-coverage`, `check-wireframe-set-freshness`, `select-prototype-inputs` (prototype-private A–E input selector), `scaffold-prototype-app` + `extract-brand-theme` + `verify-prototype-build` (prototype-private). Plus `map-<method>-to-ui.md` per analysis methodology. |
| `framework/assets/` | Read-only reference content: `template-*.md/html`, `templates/` (cross-pipeline DS-agnostic), `design-systems/` (sibling DS files — currently `wireframe-ds.html`), `wireframes/` (wireframe-private templates + the cross-pipeline trade-off/posture substrate: `tradeoff-dimensions-registry.md`, `pattern-bindings.md`, `domain-defaults.md`, `position-vocabulary.md`, `divergence-heuristics.md`, and the shared UX-posture registry `design-philosophies.md`), `topics-*.md` (bijection invariants), `taxonomy-*.md`, `glossary.md` + `glossary.index.md` (system-terminology glossary + slim lookup index — the framework's own vocabulary; distinct from the application-domain GLOSSARY methods under `analyse-*/GLOSSARY/`), `persona-llm.md`, `constraints.md`, `pattern-catalogue/`, `characters/*.md`, `analyses/registry.md` + per-method reference/template, `analyses-inputs/registry.md` + per-method, `reviews/registry.md` + per-method, `reviews-inputs/registry.md` + per-method, `references/`, `prototypes/` (prototype-private: `ux-baseline-checklist.md`, `template-design-spec.md`, `scaffolding-instructions.md`, `app-shell-spec.md`, `shared-component-conventions.md` — the UX-posture registry `design-philosophies.md` is now the cross-pipeline `wireframes/design-philosophies.md`). |
| `framework/shared/` | Cross-pipeline invariants: `general-rules.md` (`GR-NN`), `prototype-scope.md` + `.index.md`, `prototype-invariants.md` (`PI-NN`), `refusal-registry.md` (`RF-NN`), `setup-instructions/{markitdown,playwright,node-toolchain,playwright-browsers}.md`. |
| `framework/state/` | Runtime state. `.progress.json` (requirements-orch only), `.prd-progress.json` (generate-prd-orch only — same shape), `.prototype-progress.json` (prototype-orch only — same shape), `timing.ndjson` (append-only across all runs), `draft-fragments/`, resolver sidecars per pipeline (`prototype-resolver-*` for `/prototype`). `/analyse-inputs`, `/review-inputs`, `/wireframe`, `/design-system`, `/analyse-requirement`, `/review-requirement` do **not** own a progress file. |
| `framework/dependency-graphs.md` | Mermaid dep graphs per orchestrator. Source of truth for what loads what. |
| `input/` | Consultant drop zone (briefs, decks, screenshots, PDFs, spreadsheets, .drawio, .yml). Read by `/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`. `.converted.md` markitdown siblings live alongside originals. |
| `requirements/` | `/requirements` outputs: `source-manifest.json` (canonical, shared with `/generate-prd`, `/analyse-inputs`, `/review-inputs` via the shared input-handler), `requirements-draft.md`, `draft-claims.ndjson`, `draft-claims-verification.ndjson`, `consultant-answers.md`, `requirements.md`. Only `source-manifest.json` is shared. |
| `prd/` | `/generate-prd` outputs: `prd-draft.md`, `draft-claims.ndjson`, `draft-claims-verification.ndjson`, `consultant-answers.md`, `prd.md`. Citation IDs namespaced `PC-NNN` / `PAI-NNN` to avoid visual collision with `C-NNN` / `AI-NNN`. |
| `design-system/` | `/design-system` output: `design-system.html` (self-contained — embedded `<script type="application/json" id="design-tokens">` block + visual swatch/typography/shadow/motion/contrast sections). Workspace `.workspace/` is styler-owned. |
| `analyse-requirements/<METHOD>/` | `/analyse-requirement` outputs. MVP methods: OOUX, JTBD, DATA-MODEL, USE-CASES, SEQUENCE/STATE/ACTIVITY-DIAGRAM, USER-JOURNEYS, TASK-FLOWS, OPPORTUNITY-SOLUTION-TREES, FIVE-WHYS, GLOSSARY, TRADE-OFF-DIMENSIONS. |
| `analyse-inputs/<METHOD>/` | `/analyse-inputs` outputs. Each methodology ships in its own follow-up PR; see `framework/assets/analyses-inputs/registry.md` for current MVP set. |
| `review-requirements/<METHOD>/` | `/review-requirement` outputs. MVP methods: ADVERSARIAL, FIRST-PRINCIPLES, TEN-BA-QUESTIONS, TEN-UX-QUESTIONS, USER-STORIES. |
| `review-inputs/<METHOD>/` | `/review-inputs` outputs. See `framework/assets/reviews-inputs/registry.md` for current MVP set. |
| `blueprints/<scope-slug>/` | **Shared cross-pipeline IR root**, created by `/wireframe` or `/prototype` (whichever scopes first) and reused by the other without re-authoring. Per-scope: `scope.json` (which requirement IDs are in scope; plus an optional goal-driven `divergence_profile`) + `blueprint.md` (**logical surface inventory** of `LS-NN` surfaces + per-surface allowed/default realizations + logical flow + scope→surface trace + per-surface Properties closed set drawn from §7 data shapes and F-NN parameters; **no pattern bindings, no chosen realization** — both live per-variant in `variants.json > surface_plan`). The all-standalone realization baseline reproduces the legacy 1-screen-per-surface output. |
| `wireframes/<scope-slug>/` | `/wireframe` outputs (wireframe-private): `analyses-inputs.json` (Stage-1b consultant selection of completed-on-disk supporting analyses — schema in `framework/skills/select-supporting-analyses.md`), `variants.json` (architect's variant configs — persona-bound + **posture-bound** (`posture` + `posture_label`, a UX posture consumed verbatim from `scope.json > divergence_profile`), cardinality cap 3; each carries a `surface_plan` authoring per-surface pattern picks + realization, plus `physical_flow`), `index.html` (metadata-only consultant landing, four sections: scope details / side-by-side wireframe columns (grouped by logical surface) / variant metadata cards / trade-off matrix with a decomposition/structure row), `_drift.json` (system file; index surfaces a one-line summary), and per-variant `<VARIANT>/` subdirs (`screen-NN-*.html` with `data-src` + `data-prop` audit attributes, `wireframe-ds.css`, `manifest.json`, `variant-position.json`). |
| `prototypes/` | `/prototype` output: **one shared Next.js app** scaffolded once from `template/` (rule 8: landing + all prototypes in this single folder). `src/app/page.tsx` landing (lists every prototype grouped by scope), `src/app/<name-slug>/**` per-prototype routes, shared `src/components/**` (shadcn primitives + atomic-design HOCs — grow additively across runs), shared `src/styles/theme.css` (one brand, identical for all), shared `src/stores`/`src/data` (fixtures), `src/components/organisms/PrototypeChrome.tsx` (role switcher PI-05 + data-reset + nav). Non-routed dot-state: `.scaffold.json` (idempotency + brand sha), `.registry.json` (durable prototype list), `.specs/<name-slug>/{supporting-inputs.json, design-spec-draft.md, design-spec-claims.ndjson, design-spec-answers.md, design-spec.md}`. `node_modules/` + `.next/` git-ignored. |

### Data flow

1. Consultant types `/start` or a specific slash command → command shim → orchestrator adopts persona.
2. Orchestrator runs **preflight gates** (prerequisite check, context-bloat skill, prior-progress detection, `AskUserQuestion` for start-fresh vs continue / overwrite vs keep).
3. Orchestrator writes `called` event to progress file (where it owns one) + `stage_start` to `timing.ndjson`, then invokes the next agent **in the foreground (same thread)**.
4. Agent reads its inputs per `framework/dependency-graphs.md`, executes its workflow, writes its artefact, calls `verify-artifact-write`, runs self-validation, prompts consultant for accept via `AskUserQuestion`.
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

Each pipeline writes only to its own output dir. The two **documented cross-pipeline exceptions** are inherited from shared agents:

- **`input-handler.md`** (shared by `/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`) writes `requirements/source-manifest.json` and `input/*.converted.md` siblings. Step-0 decides create / refresh / no-op / halt; only create + refresh write. When invoked with `progress_path: null` (i.e. by `/analyse-inputs` or `/review-inputs`), does not touch `framework/state/*`.
- **`blueprint-architect.md` + `scope-selector.md`** (shared by `/wireframe` and `/prototype`) write `blueprints/<scope-slug>/{scope.json, blueprint.md}`.

Per-pipeline writes / reads:

- `/requirements` writes `requirements/*`, `input/*.converted.md`, `framework/state/*` (`.progress.json`, resolver sidecars, `timing.ndjson`).
- `/generate-prd` writes `prd/*`, `framework/state/.prd-progress.json`, `framework/state/prd-resolver-*.{ndjson,json}`, `timing.ndjson`. Reads `requirements/source-manifest.json` + `input/*`. Fully independent of `requirements/requirements.md` — never reads or writes it.
- `/design-system` writes `design-system/*`. Reads `requirements/` + `framework/state/` only for preflight.
- `/analyse-requirement` writes `analyse-requirements/<METHOD>/*`. Reads `requirements/requirements.md`.
- `/analyse-inputs` writes `analyse-inputs/<METHOD>/*`. Reads `requirements/source-manifest.json` + `input/*` (multimodal for `Native-multimodal` tier). Does not write `framework/state/*`.
- `/review-requirement` writes `review-requirements/<METHOD>/*`. Same read scope as `/analyse-requirement`.
- `/review-inputs` writes `review-inputs/<METHOD>/*`. Same read scope as `/analyse-inputs`. Does not write `framework/state/*`.
- `/wireframe` writes `wireframes/<scope-slug>/*`. Reads `requirements/requirements.md` (scoped by `scope.json`) + `framework/assets/analyses/registry.md` + `framework/assets/analyses/sidecar-schema.md` + selected `analyse-requirements/<METHOD>/*` sidecars (sidecar-first per `framework/assets/analyses/sidecar-schema.md`; bounded prose fallback under `RF-09`; drift halts under `RF-08`) + `framework/assets/{pattern-catalogue,wireframes,design-systems,templates}/**`. Does not write `framework/state/*` (resumability is on-disk per scope-slug).
- `/prototype` writes `prototypes/**` + `framework/state/*` (`.prototype-progress.json`, `prototype-resolver-*`, `timing.ndjson`). Via the shared `scope-selector` + `blueprint-architect` it also writes `blueprints/<scope-slug>/{scope.json, blueprint.md}` (the documented cross-pipeline exception). Reads `requirements/requirements.md` (scoped) + the consultant's A–E selections (`analyse-requirements/*`, `analyse-inputs/*`, `wireframes/<scope-slug>/*`, `input/*` via `source-manifest.json`) + `design-system/design-system.html` (brand source a, if present) + `template/**` (scaffold source, once) + `framework/assets/prototypes/**`. One prototype per run; brand look is fixed/shared; divergence is UX-only (posture + D1–D5 positions). Honours PI-01..PI-08; new refusals `RF-10`..`RF-13`.

### Where new system elements go

| Adding | Goes in | Also touch |
|---|---|---|
| New slash command | `.claude/commands/<name>.md` (frontmatter `description:` + body that names the orchestrator) | New `framework/orchestrators/<name>-orch.md` |
| New orchestrator | `framework/orchestrators/<name>-orch.md` | New `framework/dependency-graphs.md` entry |
| New agent | `framework/agents/<pipeline>-<role>.md` (or subdir for multi-file agents) | Reference in orchestrator |
| New `/analyse-requirement` methodology | `framework/agents/analyses/<method>-analyser.md` + reference + template + character + map skill + sidecar emission per `framework/assets/analyses/sidecar-schema.md` | Append row to `framework/assets/analyses/registry.md` (status: `mvp`, assign a lens `group`; see `plans/` for candidate pre-plans); append `architect_roles` row to `framework/skills/select-supporting-analyses.md`. Zero orch changes. Skipping sidecar emission trips `RF-09` legacy-fallback on selection in `/wireframe`. |
| New `/analyse-inputs` methodology | `framework/agents/analyses-inputs/<method>-analyser.md` + `framework/assets/analyses-inputs/<method>-reference.md` + template + character + map skill (or reuse `map-<method>-to-ui.md` if source-agnostic) | Append the row to `framework/assets/analyses-inputs/registry.md` with `status: mvp`, fill all eight fields (+ optional lens `group`; see `plans/` for candidate pre-plans). `output_path` under `analyse-inputs/<METHOD>/`. Zero orch changes. |
| New `/review-requirement` methodology | `framework/agents/reviews/<method>-reviewer.md` + reference + template + character | Append row to `framework/assets/reviews/registry.md` (status: `mvp`, assign a lens `group`; see `plans/` for candidate pre-plans). Zero orch changes. |
| New `/review-inputs` methodology | `framework/agents/reviews-inputs/<method>-reviewer.md` + reference + template + character | Append the row to `framework/assets/reviews-inputs/registry.md` with `status: mvp` (+ optional lens `group`; see `plans/` for candidate pre-plans). `output_path` under `review-inputs/<METHOD>/`. Zero orch changes. |
| New skill | `framework/skills/<verb-noun>.md` | Reference from caller(s) |
| New asset (template, taxonomy, character) | `framework/assets/<kind>/<name>.md` | Reference from agent/skill |
| New shared rule (`GR-NN`) | Append to `framework/shared/general-rules.md` — never renumber | — |
| New refusal predicate (`RF-NN`) | Append to `framework/shared/refusal-registry.md` — never renumber | Add `setup-instructions/<tool>.md` if applicable |
| New prototype invariant (`PI-NN`) | Append to `framework/shared/prototype-invariants.md` — never renumber | Merger auto-appends to `requirements.md` |
| New pipeline state file | `framework/state/<name>` + declare owner in orchestrator Tools section | — |
| New wireframe variant configuration shape (`variants.json > surface_plan`) | Architect **authors** the per-variant `surface_plan` (per-surface pattern picks + realization, validated against the catalogue at author time); generator **renders** it; comparator checks render-vs-plan. Canonical schema in `blueprint-architect.md > Output` + `framework/assets/wireframes/realization-strategies.md > Section 2`. Configuration emerges per run from goals/personas × dimensions × realization. | If the `surface_plan` / `manifest.json` / `variant-position.json` shape evolves, update `blueprint-architect.md`, `wireframe-variant-generator.md`, `wireframe-comparator.md`, and `framework/assets/wireframes/{realization-strategies.md, template-set-index.html}` together — implicit schema contract. |
| New realization strategy (how a surface becomes physical screens) | Append to `framework/assets/wireframes/realization-strategies.md` Section 1 (enum → existing-catalogue-pattern mapping). | Consumed by `blueprint-architect.md` (step-03 derives `allowed_realizations`; step-05 picks + derives `physical_screens`), `wireframe-variant-generator.md` (renders), `wireframe-comparator.md` (decomposition/structure row). Co-edit. Never add a realization that needs a non-existent catalogue pattern. |
| New goal-type / persona-divergence heuristic | Append to `framework/assets/wireframes/divergence-heuristics.md`. Executed **once** by `scope-selector.md` (persisted to `scope.json > divergence_profile`); consumed by `blueprint-architect.md` step-05 (never re-derived in the architect). | `divergence_profile` is *defined* in `scope-selector.md`'s schema (canonical owner); referenced by `blueprint-architect.md`. The heuristic reuses (does not redefine) `tradeoff-dimensions-registry.md` §2/§5 + `position-vocabulary.md`. |
| New cross-pipeline asset (shared by `/wireframe` + `/prototype`) | `framework/assets/templates/` (DS-agnostic) OR `framework/assets/design-systems/` (sibling DS) OR `framework/assets/wireframes/` (wireframe-private) per scope | Reference from consuming agent. Cross-pipeline agents use no pipeline prefix (`input-handler.md`, `blueprint-architect.md`). |
| New UX posture (cross-pipeline design philosophy) | Append to `framework/assets/wireframes/design-philosophies.md` (posture → D1–D5 position preset + structural/realization recommendations + a row in the "Posture selection by persona goal-type" mapping). **References** `tradeoff-dimensions-registry.md` + `position-vocabulary.md`, never redefines; record `D6 = 0` while D6 is inactive; check the preset against §4 incoherent-pairs + §5 persona rules; the new mapping row must be pole-consistent. | Consumed by `prototype-spec-drafter.md` + `prototype-orch.md` Step B (manual pick) **and** `divergence-heuristics.md` §4b + `scope-selector.md` + `blueprint-architect` step-05 (auto-recommended per `/wireframe` variant). Any new posture-derived incoherent pair appends to `tradeoff-dimensions-registry.md` §4 (canonical owner), not the posture file. Zero orch changes. |
| New `/prototype` design-spec section / marker | Edit `framework/assets/prototypes/template-design-spec.md` (the populate-top-to-bottom skeleton + marker legend `[SRC]`/`[POSTURE-DEFAULT]`/`[AI-SUGGESTED]`). | Co-edit `prototype-spec-{drafter,resolver,merger}.md` + `prototype-generator/steps/*` when a section the generator consumes changes — implicit schema contract (mirrors the wireframe `surface_plan` co-edit rule). |
| New trade-off dimension applicability / incoherent-pair / persona-position rule | Append to `framework/assets/wireframes/tradeoff-dimensions-registry.md`; never renumber `D1..D6`. | `blueprint-architect.md` and `wireframe-comparator.md` read transitively — no agent edits needed. |
| New pattern-binding guidance | Append to `framework/assets/wireframes/pattern-bindings.md > Section 1`; never remove rows. | Consumed by `wireframe-variant-generator.md` and `check-pattern-coverage.md`. |
| New default dimension profile (different domain) | Do **not** edit `framework/assets/wireframes/domain-defaults.md` in-place — it is keyed to the project's locked domain. Fork it under a new pipeline-specific defaults asset and parameterise `scope.json > dimension_override`. | Current `domain-defaults.md` is consumed by `blueprint-architect.md` when `dimension_override == null`. |
| New plain-English `(dimension, position)` label | Append to `framework/assets/wireframes/position-vocabulary.md`; never embed dimension notation (`D1+1`) or pattern IDs (`table.compact`) in labels. | Consumed by `template-set-index.html`, `template-screen.html`'s `{{POSITION_TAGLINE}}`, the variant-generator, and the comparator. |

## 3. File and component placement rules

### Create new file

- New methodology / agent / skill / asset / shared-rule / refusal / invariant — see the matrix above. Always **append** to registries and `NN`-numbered files; never renumber.
- New pipeline output artefact → its pipeline's dedicated dir. **Never** write outside this dir (the input-handler / blueprint-architect exceptions are documented in §2 Stand-alone constraints and bounded to specific paths).
- New `setup-instructions/<tool>.md` when an `RF-01`-style pause needs out-of-band install steps.
- New `template-<thing>.md/html` in `framework/assets/` when an agent needs a populate-top-to-bottom skeleton.

### Edit existing file

- Tweaking an agent's workflow, handback gate, timing events → its single `.md`. Keep workflow + Self-validation + DoD + Anti-Patterns sections in sync.
- Adjusting an orchestrator's pipeline steps → its single `<name>-orch.md`. Update **Tools**, **Self-validation**, **Anti-Patterns**, **Inputs/Output** together.
- Adding a `[STANDARD-RULE: GR-NN]` answer → append rule to `framework/shared/general-rules.md`. The drafter's `completeness-gap-pass.md` picks it up automatically when its scope predicate matches.
- Adding a methodology (from a `plans/` candidate or net-new) → append the registry row with `status: mvp`, fill the eight registry fields, and ship the agent + reference + template + character + map skill. Orchestrator unchanged.
- Tuning the context-bloat heuristic → `framework/skills/check-context-bloat.md` (`bytes_total > 250_000` or `row_count > 25`).
- Updating dep graphs after any structural edit → `framework/dependency-graphs.md`.

### Create abstraction (extract a skill or shared file)

Extract only when **all** of:
1. The same procedure is invoked by ≥ 2 agents or orchestrators (or will be on a near-term planned change).
2. The procedure has clean parameter inputs and a single structured return (`pass | RF-NN trigger | row | ok`).
3. Extracting does not require the abstraction to know caller-specific state.

Otherwise inline. Don't pre-extract for hypothetical future reuse.

Cross-pipeline policy (rules, scopes, refusals, invariants) goes in `framework/shared/`. Pipeline-specific procedure goes in `framework/skills/`. Pipeline-specific reference content goes in `framework/assets/`.

### Canonical-source rule (definitions only)

Every field name, NDJSON row schema, vocabulary term, stable-ID (`GR-NN`, `RF-NN`, `PI-NN`, `C-NNN`, `AI-NNN`, `PC-NNN`, `PAI-NNN`), and registry must have exactly **one** file that *defines* it. Every other file that uses it references the canonical file by name or link — never re-defines it.

Scope is **definitions only**, not procedures. Procedural extraction follows the "Create abstraction" criteria above.

Mechanically derived embedding (e.g. the merger appending `PI-01..08` verbatim from the canonical source into every `requirements.md`, or `[SRC: C-NNN]` markers copied from `draft-claims.ndjson` into `requirements-draft.md`) is **not** a violation. Restating constraints in an agent's *Self-validation* section for fail-closed resilience is also not a violation.

**Canonical owners (orientation):**
- Stable-ID registries: `framework/shared/{general-rules,refusal-registry,prototype-invariants}.md`.
- Methodology registries: `framework/assets/{analyses,analyses-inputs,reviews,reviews-inputs}/registry.md`.
- Pipeline loading graph: `framework/dependency-graphs.md`.
- Source manifest: `requirements/source-manifest.json` (owned by `framework/agents/input-handler.md`).
- System terminology: `framework/assets/glossary.md` (slim lookup `framework/assets/glossary.index.md`).

### System terminology (use the glossary)

When extending, changing, or describing this system — writing plans, editing orchestrators/agents/skills/assets, or phrasing consultant-facing prompts — use the system's own terms exactly as defined in `framework/assets/glossary.md`. Consult the slim lookup `framework/assets/glossary.index.md` for the canonical term + one-line gloss, and Read the full `### Term` entry on demand only when you need the definition or a disambiguation. Do **not** coin synonyms for defined concepts (e.g. "page"/"view" for *surface*/*screen*, "styling" for *Design*, "stance" for *position*). The glossary defines **system** vocabulary only — the client application's domain vocabulary is produced separately by the GLOSSARY methodologies (`analyse-requirements/GLOSSARY/`, `analyse-inputs/GLOSSARY/`).

### Naming patterns

- **Commands.** `.claude/commands/<verb>.md`. Single lowercase verb.
- **Orchestrators.** `framework/orchestrators/<verb>-orch.md`.
- **Agents.** Pipeline-private: `framework/agents/<pipeline>-<role>.md` (`requirements-drafter.md`). Cross-pipeline: `framework/agents/<role>.md` (no pipeline prefix — `input-handler.md`, `blueprint-architect.md`). Methodology: `framework/agents/<plural-pipeline>/<method>-(analyser|reviewer).md`. Multi-file agent → subdir with `steps/`, `prompt-templates/`, `data/`.
- **Skills.** `framework/skills/<verb-noun>.md` — verb-led, hyphenated, lowercase.
- **Assets.** Templates `template-<thing>.{md,html}`; references `<method>-reference.md`; characters `<persona-or-stage>.md` under `assets/characters/`; taxonomies `taxonomy-<dimension>.md`; topics `topics-<pipeline>.md`; registries `registry.md` inside the pipeline-plural subdir.
- **Shared.** `<noun>.md` / `<noun>-registry.md` / `<noun>-invariants.md`. Stable-ID files use `NN-NN` numbering inside; never renumber.
- **State.** `.progress.json`, `timing.ndjson`, `<agent>-<role>.ndjson|json` under `framework/state/`.
- **Pipeline outputs.** `<artefact>.md/.html/.json/.ndjson` under the pipeline's own dir. Analyses + reviews use UPPERCASE-METHOD subdirs (`analyse-requirements/OOUX/`, `review-inputs/COMPLETENESS-REVIEW/`). `/prototype` is the exception — it generates a Next.js app under `prototypes/` with kebab-case per-prototype route segments (`prototypes/src/app/<name-slug>/`) + non-routed dot-state (`prototypes/.specs/<name-slug>/`, `.registry.json`, `.scaffold.json`).
- **Markers in content.** `[SRC: C-NNN]` (input-cited fact in `/requirements` draft **and final doc**, sidecar-backed by `draft-claims.ndjson`, **retained by the merger** as downstream provenance — not stripped). `[SRC: <filename>]` (filename-cited fact in `/analyse-inputs` and `/review-inputs` artefacts — manifest row's `filename` payload). `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` (drafter inference, resolver Q&A). `[STANDARD-RULE: GR-NN]` (deterministic, resolver skips). `[OUT-OF-SCOPE: domain-default]` (prototype-only, resolver skips). `[POSTURE-DEFAULT]` (`/prototype` design spec — value deterministically from the chosen UX posture; resolver skips, merger strips; `[SRC: …]` in the design spec references requirement IDs / blueprint `LS-NN` / wireframe variants and is retained). Stable-ID prefixes: `C-` claims, `AI-` suggestions, `PC-` / `PAI-` PRD equivalents, `GR-` general rules, `RF-` refusals, `PI-` prototype invariants.
- **Timing events.** `run_start`, `run_end`, `stage_start`, `stage_end`, `substep_start`, `substep_end`, `consultant_prompted`, `consultant_responded` — all NDJSON, append-only via PowerShell `Add-Content`.
- **Progress events.** `called` / `completed` per agent.

## 4. Collaboration Style & Feedback
- **Role:** You are a senior peer and a strategic thinking partner. Treat me as an equal ally.
- **Pushback:** If you disagree, say so and explain why. If my claim seems incorrect, explain why and support your view.
- **Devil's Advocate:** Play devil's advocate when I propose a solution, identifying 2-3 potential blind spots or assumptions that need testing.
- **Uncertainty:** Do not smooth over uncertainty to sound authoritative. I would rather have an accurate map of what you know and do not know.
