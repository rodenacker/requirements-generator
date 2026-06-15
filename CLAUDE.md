# CLAUDE.md

> Orientation (directory inventory, the runtime data-flow walkthrough, full per-pipeline read/write enumeration, and the `/wireframe` + `/prototype` mechanics) lives in `docs/architecture.md` — reference only, not auto-loaded, may lag (verify against real files). This file is the **contract**: the rules and placement decisions you must follow.

## 4. Collaboration Style & Feedback
- **Role:** You are a senior peer and a strategic thinking partner. Treat me as an equal ally.
- **Pushback:** If you disagree, say so and explain why. If my claim seems incorrect, explain why and support your view.
- **Devil's Advocate:** Play devil's advocate when I propose a solution, identifying 2-3 potential blind spots or assumptions that need testing.
- **Uncertainty:** Do not smooth over uncertainty to sound authoritative. I would rather have an accurate map of what you know and do not know.

## 2. Project purpose & division of labour

**What.** Consultant-driven Claude Code workspace. Twelve slash commands — each a prompt-only pipeline of markdown orchestrators + agents + skills — turn loose client material into structured artefacts, wireframes, and clickable prototypes. Together these build a comprehensive, citation-grounded set of **frontend requirements** for generating internal, enterprise-level **data-management applications**. No runtime code: every "agent" is an `.md` file Claude reads and adopts as persona (the one exception: `/prototype` *generates* a real client-side Next.js app under `prototypes/`).

**Division of labour (what vs how).** Mine **everything** relevant from the inputs — both *what* and *how*. The distinction between them is one of **authority**, not of source:

- **The *what* — authoritative, citation-bound.** What the business and users want to achieve; the tasks users perform; the data each surface must represent (object shapes and their properties); how that data is processed; data-management rules; business rules for data processing; and required interactions / behaviour — i.e. how the frontend must *work*. These are binding requirements: the system must represent them faithfully, they are citation-bound (`[SRC: …]`), and object properties are a closed set that must not be invented.
- **The *how* — mined, but advisory only.** Information architecture and surface decomposition; screen layout; choice of controls; UX posture / design philosophy; visual styling and brand look; and any specific screen designs pictured in visual inputs (screenshots, mockups, decks). Where the inputs express these, mine them — but treat them strictly as **requirement signals: possibilities and desiderata that bias the system's design, never authoritative outcomes.** The system holds design authority over the *how*; the resulting wireframes and prototypes may diverge substantially from anything pictured. A *how*-decision cites its input signal when it honours one, and is marker-backed (`[AI-SUGGESTED]` / `[POSTURE-DEFAULT]` / `[OUT-OF-SCOPE: domain-default]`) when the system generates or diverges from it.
- **Boundary cases.** A *required interaction* ("user must be able to reassign a case") is *what*; its realization (dedicated screen vs inline drawer vs modal, which control, which gesture) is *how*. A *data property* is *what* (must exist, citation-bound); its *presentation* (table column vs status chip vs detail row) is *how*. The visual representations therefore **emerge** from running the system and are a co-equal end alongside the textual artefacts.

**Command catalogue.** (Full mechanics for the heavy two in `docs/architecture.md`; full method lists in the per-pipeline registries.)

| Command | Produces |
|---|---|
| `/start` | Dispatcher — lists the other commands and launches the chosen one. |
| `/requirements` | LLM-audience FE spec (`requirements/requirements.md`). |
| `/generate-prd` | Human-audience PRD (`prd/prd.md`) — strategic framing, success metrics, hypotheses, MVP phasing, risks, stakeholders. Independent of `/requirements`; can run before/after/alongside. |
| `/design-system` | Brand-token brief (`design-system/design-system.html`). |
| `/analyse-requirement` | Lens-transforms `requirements/requirements.md` (17 lens methods; list: `framework/assets/analyses/registry.md`). |
| `/analyse-inputs` | Lens-transforms raw `input/` material (`framework/assets/analyses-inputs/registry.md`). |
| `/review-requirement` | Critiques `requirements/requirements.md` (7 methods; `framework/assets/reviews/registry.md`). |
| `/review-inputs` | Critiques raw `input/` material (`framework/assets/reviews-inputs/registry.md`). |
| `/wireframe` | 2–3 parallel low-fi HTML wireframe variants for a scope of `requirements/requirements.md`; cross-pipeline `blueprint-architect` + `scope-selector` + `design-philosophies.md` reused by `/prototype`. |
| `/prototype` | One hi-fi, clickable, client-side-only Next.js prototype per run, accumulating in one shared app under `prototypes/`, reachable from a single landing page. Brand-locked; divergence is pure UX (posture + D1–D5). |
| `/export-application` | Application-audience export of the finished `requirements.md` (`export-application/requirements-application.md`) — pure re-projection: swaps §6.10 fixtures to backend-contract pointers, relabels §7 sources, strips the PI appendix, stamps provenance (source sha256). Zero generated content. |
| `/resolve-review` | Consultant-approved resolutions document from selected findings of an existing `review-inputs/` **or** `review-requirements/` artefact, written as a NEW dated file into `input/` (never overwriting) for the next `/requirements` run to ingest. On review-requirements-sourced runs (opt-in), additionally inserts a transient `## Amendments (pending re-merge)` section into `requirements/requirements.md` — a cache of the same resolutions for immediate downstream use, deleted by the next `/requirements` re-merge. Per-methodology schemas: `framework/assets/resolve-review/methodology-map.md`; addendum shape: `framework/assets/resolve-review/template-addendum.md`. |

**For.** Solo consultants / BAs running Claude Code locally to produce deterministic, citation-grounded handoff artefacts — specs, PRDs, analyses, reviews, wireframes, and prototypes — from briefs, decks, screenshots, spreadsheets, PDFs.

**Output audience.** `requirements/requirements.md` is LLM-audience; `prd/prd.md` and **all analysis and review outputs are human-audience** (consultant; sometimes client stakeholders). Analyses are *additionally* read by a pipeline-specific downstream consumer — `/analyse-inputs` outputs by `/requirements`, `/analyse-requirement` outputs optionally by `/wireframe`'s `blueprint-architect` (via the per-analysis sidecar). Reviews have **no** downstream consumer. The human-readability standard for analyses + reviews is `framework/shared/output-readability.md` (an "In plain terms" lead, first-use jargon glossing, retained citations; additive — it relaxes no gate, no severity, and no quality check).

**Optimizes for.** Determinism + auditability over speed. Every fact in a final artefact must be traceable to an input citation (`[SRC: C-NNN]`, `[SRC: <filename>]`, `data-src="<F-NN,BR-NN,UI-NN>"`) or a named provenance marker (`[AI-SUGGESTED]`, `[STANDARD-RULE: GR-NN]`, `[OUT-OF-SCOPE]`). Resumability: every pipeline checkpoints to disk so `/clear` + re-invoke continues at the first incomplete agent.

**Constraints.**
- Target domain = **data-management productivity apps** (CRUD-heavy). Prototype defaults assume that, not marketing/content.
- Output target = **prototype** for every pipeline run (client-stub simulated server, fixture data — see `framework/shared/prototype-invariants.md` PI-01..PI-08); `requirements/source-manifest.json > target` is auto-set to `"prototype"` at the orchestrator's Step 1b (the consultant choice is retired; legacy `"application"` manifests are honoured by dormant branches). The application-audience document is an export-time concern (`/export-application`). The pipeline doc carries §1.7 / §6.6.1 / §6.6.2 + the §6.1 Rationale column as scope-noted application-build guidance — never prototype design inputs.
- Every consultant interaction = foreground in-thread via `AskUserQuestion`. **No background/sub/async agents** for interactive surfaces — handback gates depend on same-thread acceptance.
- Every artefact write = `Write` then `framework/skills/verify-artifact-write.md` (sha256 + min-bytes). Mismatch → RF-04 hard halt.
- Refusal predicates are canonical in `framework/shared/refusal-registry.md` — never paraphrase or redefine.
- Inline `[SRC: C-NNN]` refs live in the draft + NDJSON sidecar; the merger **retains** them in the final `requirements.md` as inline provenance for downstream LLM consumers (it strips only the resolution markers `[AI-SUGGESTED]`/`[STANDARD-RULE]`/`[OUT-OF-SCOPE]`). The `draft-claims.ndjson` sidecar stays the authoritative store of the verbatim source quotes (joined on the retained `C-NNN` tags). `[AI-SUGGESTED]` reserved for facts not traceable to inputs and not covered by `GR-NN` — never widen this set.
- **Wireframe pipeline never invents object properties.** Every data-bound element (form input, table column, detail row, status chip) carries a `data-prop` naming a §7 data-shape property (`Shape.Field`) or F-NN-named parameter (`F-NN:ParamName`). The blueprint's per-surface `Properties` column is the canonical closed set (mirrored into each variant's `surface_plan` as per-physical-screen `covers_properties`); properties outside that set are fabrications and a `RF-04`-class self-validation FAIL. The contract survives a fold: a surface realized as an inline drawer/modal still stamps its `data-prop`s on the host screen's drawer/modal sub-tree. UI-only controls (search, sort, pagination, filter chips, save/cancel, dropzones) are exempt. `data-src="F-NN"` alone is insufficient justification — the field's property must be in the blueprint's closed set.

## 3. Roles & write isolation

### Separation of concerns

- **Orchestrator** = control flow only. Reads progress/timing, deletes during reset, writes events. Never edits content artefacts (one exception: drafter handback gate reads `draft-claims-verification.ndjson` summary line).
- **Agent** = content production. Reads inputs, writes its one artefact, owns its self-validation + handback. Never writes outside its scoped output paths.
- **Skill** = reusable procedure. Parameterised by inputs. Returns `pass | <RF-NN> trigger | structured-row | ok`. No file I/O outside its declared inputs/outputs.
- **Asset** = read-only reference. Templates, registries, taxonomies, characters, pattern catalogue.
- **Shared** = cross-pipeline invariants (rules, scope, refusals, invariants, setup-instructions). Read-only; mutated only by appending new IDs.
- **State** = orchestrator/agent runtime scratch. Each owner declared in the orchestrator's Tools section.

### Stand-alone constraints (write isolation)

Each pipeline writes **only to its own output dir**. The four **documented cross-pipeline exceptions** (the first two inherited from shared agents, the third and fourth pipeline-private to `/resolve-review`):

- **`input-handler.md`** (shared by `/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`) writes `requirements/source-manifest.json` and `input/*.converted.md` siblings. Step-0 decides create / refresh / no-op / halt; only create + refresh write. When invoked with `progress_path: null` (i.e. by `/analyse-inputs` or `/review-inputs`), does not touch `framework/state/*`.
- **`blueprint-architect.md` + `scope-selector.md`** (shared by `/wireframe` and `/prototype`) write `blueprints/<scope-slug>/{scope.json, blueprint.md}`.
- **`resolve-review-drafter.md`** (private to `/resolve-review`) writes one NEW `input/<stem>-<date>.md` per accepted run — **additive only**, never overwriting an existing `input/` file (same-day collisions suffix `-2`, `-3`). The draft is staged under `resolve-review/` and never enters `input/` unaccepted.
- **`resolve-review-drafter.md` Step 9b** (review-requirements-sourced runs, consultant opt-in only) inserts/extends the single `## Amendments (pending re-merge)` section in `requirements/requirements.md` — **bounded to that one section** (placed before the PI appendix; no other byte changes), always paired with — and a subset of — the `input/` resolutions doc written first (the pairing invariant). The section is a transient cache: the next `/requirements` re-merge regenerates the doc and folds the same resolutions in from `input/`. Canonical shape: `framework/assets/resolve-review/template-addendum.md`.

Full per-pipeline read/write enumeration: `docs/architecture.md`.

## 4. File and component placement rules

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
- Adjusting the end-of-pipeline `/clear` suggestion → `framework/shared/context-hygiene.md` (the canonical tip wording + placement rule, emitted by each orchestrator at its success terminal). This replaced the retired context-bloat preflight (`RF-05`, tombstoned in `framework/shared/refusal-registry.md`).
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
- **Markers in content.** `[SRC: C-NNN]` (input-cited fact in `/requirements` draft **and final doc**, sidecar-backed by `draft-claims.ndjson`, **retained by the merger** as downstream provenance — not stripped). `[SRC: <filename>]` (filename-cited fact in `/analyse-inputs` and `/review-inputs` artefacts — manifest row's `filename` payload). `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` (drafter inference, resolver Q&A). `[STANDARD-RULE: GR-NN]` (deterministic, resolver skips). `[OUT-OF-SCOPE: domain-default]` (prototype-only, resolver skips). `[POSTURE-DEFAULT]` (`/prototype` design spec — value deterministically from the chosen UX posture; resolver skips, merger strips; `[SRC: …]` in the design spec references requirement IDs / blueprint `LS-NN` / wireframe variants and is retained). `[CONSULTANT-STATED]` / `[AI-INFERRED, CONSULTANT-CONFIRMED]` (`/resolve-review` resolutions-document origin markers — canonical definitions in `framework/assets/resolve-review/template-resolutions.md`; also carried by `AMD-NN` entries in the transient `## Amendments (pending re-merge)` section of `requirements.md` — canonical shape in `framework/assets/resolve-review/template-addendum.md`; deliberately not requirement-ID-shaped). Stable-ID prefixes: `C-` claims, `AI-` suggestions, `PC-` / `PAI-` PRD equivalents, `GR-` general rules, `RF-` refusals, `PI-` prototype invariants, `AMD-` amendments (transient, per-section numbering).
- **Timing events.** `run_start`, `run_end`, `stage_start`, `stage_end`, `substep_start`, `substep_end`, `consultant_prompted`, `consultant_responded` — all NDJSON, append-only via PowerShell `Add-Content`.
- **Progress events.** `called` / `completed` per agent.

