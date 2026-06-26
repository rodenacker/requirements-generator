<!-- ROLE: asset (cross-pipeline, read-only reference). Canonical source for SYSTEM terminology. -->

# System glossary

**Purpose.** Canonical definitions of the **system's own terminology** — the language the framework uses to describe *itself*, its pipelines, roles, artefacts, and outputs (e.g. *orchestrator*, *blueprint*, *scope-slug*, *UX posture*, *trade-off dimension*, *handback gate*). This is shared vocabulary between the consultant and the LLM so that plans to extend, change, or describe the system reuse one precise set of terms.

**This is NOT a client-application glossary.** The terminology of the *products* a consultant documents with the system (their domain nouns, entities, statuses) is produced by the two **GLOSSARY methodologies** and lives under `analyse-requirements/GLOSSARY/` (extraction) and `analyse-inputs/GLOSSARY/` (convergence). Those methods are forbidden from loading this file; keep the two worlds separate — system terms here, application terms there.

**Out of scope (for now).** Pure domain-modelling / output-description vocabulary the system *uses inside artefacts* — Domain Model, Concept, Aggregate, Ubiquitous Language, object map, ORCA, CCP, and the atomic-UI element ladder (Atom / Molecule / Organism) — is **not** defined here. It belongs to a later output-vocabulary effort; the methodology references (`framework/assets/analyses/*-reference.md`, the OOUX object map) remain its canonical sources until then.

**Canonical-source rule (docs/maintenance.md > Canonical-source rule).** This file is the single defining source for the *system-terminology* vocabulary below. Where a term is also a **schema field** or **stable-ID family** owned by another file, the entry gives a one-line gloss and points to that owner with `Canonical source:` rather than restating its schema.

**How to use (token-efficient path).** Consult the slim lookup table `framework/assets/glossary.index.md` for the canonical term and a one-line gloss; **read the matching `### Term` entry here only on demand** when you need the full definition or a disambiguation. When extending/changing/describing the system, use these terms exactly and do **not** coin synonyms for defined concepts.

**Maintenance.** Add a `### Term` here and a matching row in `glossary.index.md` together; never let them drift. Entries are alphabetised in the index; grouped by concept here for learnability.

---

## 1 · Pipeline structure & roles

### Command
A slash-command entrypoint under `.claude/commands/<verb>.md` — a thin shim that names the orchestrator it launches. The ten commands are listed in CLAUDE.md §1.
Canonical source: `CLAUDE.md §1` · entrypoints in `.claude/commands/`.

### Orchestrator
The control-flow owner of a pipeline (`framework/orchestrators/<verb>-orch.md`). Runs preflight gates, sequences agents in the foreground, owns progress/timing state, handback gates, and reset. Never edits content artefacts.
Canonical source: `docs/maintenance.md > Separation of concerns`.
Not to be confused with: an **agent** (which produces content) — an orchestrator only directs.

### Agent
A persona+workflow `.md` file the LLM reads and *adopts* to produce one content artefact. Cross-pipeline agents carry no pipeline prefix (`input-handler.md`, `blueprint-architect.md`); pipeline-private agents are `<pipeline>-<role>.md`. Writes only within its scoped output paths.
Canonical source: `docs/maintenance.md > Separation of concerns`.

### Skill
A reusable, parameterised unit of agent behaviour (`framework/skills/<verb-noun>.md`). Caller-agnostic; returns a structured result (`pass | RF-NN trigger | row | ok`). No file I/O outside its declared inputs/outputs.
Canonical source: `docs/maintenance.md > Separation of concerns`.

### Asset
Read-only reference content under `framework/assets/` — templates, registries, taxonomies, characters, pattern catalogue, this glossary. Mutated only by appending.
Canonical source: `docs/maintenance.md > Separation of concerns`.

### Shared
Cross-pipeline invariants under `framework/shared/` — general rules, refusals, prototype invariants, scope, setup-instructions. Read-only; mutated only by appending new IDs.
Canonical source: `docs/maintenance.md > Separation of concerns`.

### Character
A persona file under `framework/assets/characters/` defining the stance, voice, and constraints an agent adopts for a stage. Distinct from a *target-user persona* (the product's end user).
Not to be confused with: **persona** (see *target-user*).

### Dispatcher
A role within a multi-agent step that distributes work to parallel sub-agents (e.g. the prototype generator dispatching per-surface generation). The `/start` command is also described as a *dispatcher* in the user sense (it lists and launches commands).
Canonical source: `framework/agents/prototype-generator/` (per-surface dispatch).

### Methodology
A named analytical or critique method applied by an analysis/review pipeline (OOUX, JTBD, DATA-MODEL, ADVERSARIAL, GLOSSARY …). Each ships an analyser/reviewer agent + reference + template + character and is registered in a `registry.md`.
Canonical source: `framework/assets/{analyses,analyses-inputs,reviews,reviews-inputs}/registry.md`.
Not to be confused with: **lens** (informal synonym used in consultant-facing copy, "through a chosen lens"); **analysis/review** (the *output* of applying a methodology).

### Analysis
The artefact produced by applying a methodology to a structured input — `requirements.md` (`/analyse-requirement`, output under `analyse-requirements/<METHOD>/`) or raw `input/` material (`/analyse-inputs`, output under `analyse-inputs/<METHOD>/`).
Not to be confused with: **review** (a *critique* methodology, not a transform — outputs under `review-*`).

### Review
The artefact produced by a *critique* methodology (ADVERSARIAL, COMPLETENESS-REVIEW, GAP-ANALYSIS …) that interrogates rather than transforms its source.
Not to be confused with: **analysis** (a lens-transform that converges on a restructured view).

### Review resolutions document
The consultant-approved input document `/resolve-review` writes as a NEW dated file into `input/` (`<stem>-<date>.md`, never overwriting), turning selected findings of one existing `review-inputs/` artefact into first-class corpus material the next `/requirements` run ingests. Each resolution anchors on the finding's **verbatim quote** (finding IDs are per-run labels that reset when the review re-runs), carries exactly one origin marker — `[CONSULTANT-STATED]` or `[AI-INFERRED, CONSULTANT-CONFIRMED]` (every AI-inferred resolution is confirmed by an explicit consultant affirmative — per finding, or via an explicit accept-all-remaining choice — never silently or by default) — and exactly one Supersedes line naming the corpus statement it replaces (or the explicit net-new sentinel). Canonical skeleton + marker definitions: `framework/assets/resolve-review/template-resolutions.md`; per-methodology semantics: `framework/assets/resolve-review/methodology-map.md`.
Not to be confused with: the **review** itself (the critique artefact under `review-inputs/<METHOD>/`, which stays untouched).

---

## 2 · The draft → resolve → merge triplet

### Drafter
The first agent of a content pipeline: produces the initial artefact with inline provenance markers (`[SRC: …]`, `[AI-SUGGESTED: …]`, etc.) and a claims sidecar. Examples: `requirements-drafter`, `prd-drafter`, `prototype-spec-drafter`.

### Resolver
The second agent: walks the drafter's `[AI-SUGGESTED]` markers and resolves them with the consultant via foreground Q&A; skips deterministic markers (`[STANDARD-RULE]`, `[POSTURE-DEFAULT]`).

### Merger
The third agent: strips resolution markers, applies final validation, and writes the clean final artefact (`requirements.md`, `prd.md`, `design-spec.md`). May mechanically embed canonical content (e.g. `PI-01..08`).

### Handback gate
The orchestrator-owned decision point where a finished agent's artefacts are validated and accepted (or the agent is re-invoked). Conditional gates surface Q&A when a conflict is detected.
Not to be confused with: **preflight gate** (runs *before* agent work).

### Preflight gate
An early orchestrator check before any agent runs — prerequisite presence, prior-progress detection, overwrite/continue choice.

---

## 3 · Cross-pipeline IR & scoping

### Scope
The subset of `requirements/requirements.md` (a set of requirement IDs) a wireframe or prototype run addresses. Captured in `scope.json`.
Canonical source: `framework/skills/scope-selector.md` (+ `blueprints/<scope-slug>/scope.json`).

### Scope-slug
The kebab-case identifier for a scope (e.g. `file-upload-flow`). Names the shared IR root `blueprints/<scope-slug>/` and the wireframe output dir `wireframes/<scope-slug>/`.
Not to be confused with: **name-slug** (the kebab-case identifier of a single *prototype*, naming `prototypes/src/app/<name-slug>/`).

### Blueprint
The shared, cross-pipeline **intermediate representation** of a scope: a logical inventory of surfaces (`LS-NN`) with per-surface allowed/default realizations, logical flow, scope→surface trace, and a per-surface **Properties closed set**. Contains **no pattern bindings and no chosen realization** — those live per-variant in `surface_plan`. One blueprint is reused by `/wireframe` and `/prototype`.
Canonical source: `framework/agents/blueprint-architect.md` (single owner of the blueprint IR).
Not to be confused with: **requirements** (the input doc) and **design-spec** (a prototype's realization plan) — see the disambiguation map.

### Logical surface (LS-NN)
A decomposition-agnostic surface in the blueprint inventory — a coherent unit of UI work (a list, a detail, a capture step) before any decision about *how many physical screens* it becomes. Carries its Properties closed set, allowed realizations, and a default realization.
Canonical source: `framework/agents/blueprint-architect.md`.
Not to be confused with: **physical screen** (the realized output) and **screen file** (a wireframe HTML file).

### Realization (realization strategy)
The closed-enum information-architecture choice for *how* one logical surface becomes physical screen(s): `standalone-screen` (default; `LS-NN ≡ S-NN`), `inline-drawer`, `inline-expand`, `wizard-split`, `modal` (and `combined`, deferred). Realization is the IA divergence axis — same surface inventory, different screen counts/placement.
Canonical source: `framework/assets/wireframes/realization-strategies.md`.
Not to be confused with: **pattern** (the catalogue UI pattern inside a screen) and **component** (its React implementation).

### Physical screen
A concrete screen produced by realizing a logical surface. `standalone-screen` → 1 (`S-NN`); `wizard-split` → N (`S-NNa`, `S-NNb`); folded realizations (drawer/expand/modal) → 0 own screens (rendered as a host-screen state).
Canonical source: `framework/assets/wireframes/realization-strategies.md`.

### surface_plan
The per-variant JSON (in `wireframes/<scope-slug>/variants.json`) that authors, per `LS-NN`: the chosen realization, pattern picks (`primary_pattern`, `primary_pattern_variant`, `base_pattern_owner`, `modifiers`, `secondary_patterns`), `covers_properties` (mirroring the blueprint closed set), `physical_screens[]`, and `states_rendered`. Authored by the architect, rendered by the generator, checked by the comparator.
Canonical source: `framework/agents/blueprint-architect.md` + `framework/assets/wireframes/realization-strategies.md §2`.

### Wireframe variant
One named configuration in `variants.json` — persona-bound, with `dimension_positions`, a `design_philosophy` label, and a `surface_plan`. Cardinality cap 3 per scope. Variants diverge on trade-off dimensions **and** information architecture (realization).
Not to be confused with: a **prototype** (one per run; inter-prototype divergence is via posture + positions, not a "variant"). The word *variant* belongs to wireframes.

### Divergence (divergence profile)
How variants/prototypes for a scope are made to *differ*. The goal-driven `divergence_profile` (axes + persona bindings) is derived **once** by `scope-selector` from §3 personas + §4 goals and persisted to `scope.json`; the blueprint-architect consumes it (never re-derives).
Canonical source: `framework/skills/scope-selector.md` (defines the profile) + `framework/assets/wireframes/divergence-heuristics.md` (the heuristics).

---

## 4 · Prototype layer

### Prototype
One hi-fi, clickable, **client-side-only** React/Next.js realization of a scope, generated by `/prototype`. All prototypes accumulate in **one shared app** under `prototypes/` and share one brand. One prototype per run.
Canonical source: `framework/orchestrators/prototype-orch.md` + `framework/shared/prototype-invariants.md`.

### Build target
The manifest's output-mode field, auto-set to **prototype** (client-stub simulated server, fixture data) by the `/requirements` orchestrator's Step 1b — the consultant choice is retired. **application** remains a legal legacy value, honoured by dormant branches. The application-audience document is produced by `/export-application` from the finished `requirements.md`. Durable in `requirements/source-manifest.json > target`.
Canonical source: `framework/shared/prototype-invariants.md` (PI-06) + `framework/skills/set-build-target.md`.

### Design-spec
A single prototype's realization plan (`prototypes/.specs/<name-slug>/design-spec.md`): chosen UX posture, D1–D5 positions, per-surface realization, workflow design, component inventory, and data bindings. Produced via the draft→resolve→merge triplet.
Canonical source: `framework/assets/prototypes/template-design-spec.md`.
Not to be confused with: **design-system** (brand tokens) and **blueprint** (scope decomposition). See the disambiguation map.

### Design
Bare *Design* in system copy means **UX / interaction / information-architecture design** — the structure of surfaces, workflows, and behaviour. It does **not** mean visual styling (that is the *brand* / *design-system*) and it is not the *design-spec* artefact.
Not to be confused with: **design-system**, **design-spec**, **design philosophy**.

### UX posture
A curated, named **preset** over the active trade-off dimensions plus the structural/realization choices it implies — the system's single notion of "design philosophy". The six: **P1** Efficiency-First / Power-Operator, **P2** Guided / Novice-Safe, **P3** Analytical / Information-Dense, **P4** Error-Averse / High-Stakes, **P5** Calm Focus, **P6** Adaptive / Progressive Pro. Postures vary **layout and workflow only** — never visual brand. Cross-pipeline: in `/prototype` the consultant **manually picks one** posture per run; in `/wireframe` postures are **auto-recommended, one per variant** (the divergence heuristic looks one up per variant binding) and consumed by the architect as a structural/realization + naming overlay that does not change the variant's dimension positions.
Canonical source: `framework/assets/wireframes/design-philosophies.md` (incl. the "Posture selection by persona goal-type" mapping both pipelines reference).
Aliases: **design philosophy** (the consultant-facing label for a posture). Not to be confused with: **position** (a single dimension value) or **brand**.

### Trade-off dimension
One of the six named axes (`D1..D6`) along which a design can be positioned: **D1** speed-accuracy, **D2** power-simplicity, **D3** density-focus, **D4** control-automation, **D5** flexibility-consistency, **D6** memorability-discoverability (D6 currently inactive, pending an upstream rename). Each carries a signed **position** `-2..+2`.
Canonical source: `framework/assets/trade-off-dimensions.md` (canonical vocabulary) + `framework/assets/wireframes/tradeoff-dimensions-registry.md` (operational per-pattern effects, applicability §2, incoherent pairs §4, persona rules §5).

### Position
A signed value `-2..+2` recording a design's stance on one trade-off dimension (e.g. D1 `+2` = "maximally fast"). Plain-English labels for each `(dimension, position)` come from the position vocabulary; signed notation is never shown to the consultant.
Canonical source: `framework/assets/wireframes/position-vocabulary.md`.
Not to be confused with: **posture** (a preset *over* positions). Avoid the word "stance" as a system term — use *position* (numeric) or *posture* (preset).

### Brand
The fixed visual identity — colour, type, radius, elevation, motion — applied **uniformly across all prototypes** via one shared `theme.css` (sourced from `/design-system` → consultant → defaults). Per-prototype styling is forbidden; divergence between prototypes is pure UX.
Canonical source: `framework/assets/prototypes/app-shell-spec.md` + `framework/skills/extract-brand-theme.md`.
Aliases: *brand-lock*, *theme*. Not to be confused with: **design-system** (the *brief/artefact* that defines the brand tokens).

### design-system
The brand-token brief produced by `/design-system` (`design-system/design-system.html`) — colour/type/shadow/motion tokens. The *source* of a prototype's `theme.css`.
Not to be confused with: **Design** (UX), **design-spec** (prototype realization), **design philosophy** (posture).

### Fixture
A static in-memory JSON data file shipped with a prototype (`prototypes/src/data/…`). Per PI-02, prototype data is fixture-sourced and mutations persist in-session only.
Not to be confused with: **store** (the live state) and **seed** (the act of loading fixtures into a store).

### Store
The client-side state container (one per entity) a prototype reads/writes at runtime, initialised from fixtures.
Not to be confused with: **fixture** (the on-disk data) and **seed**.

### Seed
The act of hydrating a store from its fixtures (`seedFromFixtures()`); also the reset-to-initial behaviour behind the chrome's data-reset control.

### Prototype invariant (PI-NN)
A behavioural contract every prototype must satisfy (`PI-01..PI-08`) — e.g. simulated server, fixture-backed data, visual-validation-only. The merger appends the canonical list verbatim into `requirements.md`.
Canonical source: `framework/shared/prototype-invariants.md`.

### App shell
The shared layout/structure wrapping every prototype (nav, regions). The prototype **chrome** (`PrototypeChrome` — role switcher, data-reset, nav) is part of the shell and sits *outside* the app under design (PI-08), so it is never treated as a design surface.
Canonical source: `framework/assets/prototypes/app-shell-spec.md`.

---

## 5 · Provenance, grounding & rules

### Claim
A single asserted fact or design decision in a draft, recorded in an NDJSON sidecar with its source so it can be verified before it reaches a final artefact.

### Citation (`[SRC: …]`)
The inline marker grounding a claim in a source: `[SRC: C-NNN]` (requirements draft + final doc, sidecar-backed by `draft-claims.ndjson`), `[SRC: <filename>]` (analyse/review-inputs, a manifest row), or design-spec refs to requirement IDs / `LS-NN` / wireframe variants. **Retained** in the final `requirements.md` by the merger as inline provenance for downstream LLM consumers — only the resolution markers (`[AI-SUGGESTED]`/`[STANDARD-RULE]`/`[OUT-OF-SCOPE]`) are stripped; the `draft-claims.ndjson` sidecar stays the authoritative store of the verbatim source quotes.
Canonical source: marker legend in `CLAUDE.md > Markers in content`; retention rule in `framework/agents/requirements-merger.md`.

### Grounding
The act of linking a claim to a real source. A grounded claim cites an input (`[SRC]`) or a named provenance marker; an ungrounded fabricated fact is a self-validation failure.

### Traceability
The end-state property that every fact in a final artefact can be followed back to a citation or provenance marker. The system optimises for traceability + auditability over speed.
Canonical source: `CLAUDE.md §1`.

### Orphan (traceability)
A fact or requirement in a final artefact that traces back to no legitimate provenance class — no `[SRC: C-NNN]` citation, no accepted `[AI-SUGGESTED]`, no `[STANDARD-RULE]`, no `[OUT-OF-SCOPE]` default. The headline defect surfaced by the `/review-requirement` REQUIREMENTS-TRACEABILITY lens; reported as "no antecedent found", never "fabricated".
Canonical source: `framework/assets/reviews/requirements-traceability-reference.md`.

### Anti-fabrication
The rule that no data-bound element may invent object properties: every bound element carries a `data-prop` naming a member of the blueprint's **Properties closed set**. Properties outside the set are an `RF-04`-class failure.
Canonical source: `CLAUDE.md §1` (constraints) + `framework/agents/blueprint-architect.md`.

### Properties closed set
The blueprint's canonical, per-surface list of allowed data properties (`Shape.Field` or `F-NN:ParamName`). It bounds what wireframes and prototypes may bind to; anything outside it is fabrication.
Canonical source: `framework/agents/blueprint-architect.md`.

### data-src / data-prop
Audit attributes on generated HTML/components: `data-src` cites the requirement ID(s) a node realizes; `data-prop` names the closed-set property a data-bound node displays. Greppable for traceability checks.
Canonical source: `CLAUDE.md §1` + `framework/assets/prototypes/shared-component-conventions.md`.

### Provenance markers
The closed set of inline tags carrying *why a value is what it is*: `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` (LLM inference needing resolution), `[STANDARD-RULE: GR-NN]` (deterministic, resolver skips), `[OUT-OF-SCOPE: domain-default]` (prototype-only exclusion), `[POSTURE-DEFAULT]` (value fixed by the chosen UX posture, resolver skips, merger strips).
Canonical source: marker legend in `CLAUDE.md > Markers in content`.

### General rule (GR-NN)
A deterministic, reusable design/answer rule (`framework/shared/general-rules.md`) the resolver applies without asking the consultant (surfaced via `[STANDARD-RULE: GR-NN]`). Append-only; never renumber.
Canonical source: `framework/shared/general-rules.md` (slim index `general-rules.index.md`).

### Refusal (RF-NN)
A canonical halt predicate (`framework/shared/refusal-registry.md`): when triggered, the agent pauses or hard-halts with a defined severity. Never paraphrase or redefine refusal predicates.
Canonical source: `framework/shared/refusal-registry.md`.

---

## 6 · State & lifecycle

### Progress file
The per-orchestrator JSON state recording `called`/`completed` per agent so a run can resume. Owned files: `.progress.json` (requirements), `.prd-progress.json` (generate-prd), `.prototype-progress.json` (prototype). Most pipelines are resumable on-disk and own no progress file.
Canonical source: declared in each orchestrator's Tools section.

### Timing event
An append-only NDJSON record in `framework/state/timing.ndjson` (`run_start`, `stage_start/end`, `substep_start/end`, `consultant_prompted/responded`, `run_end`) — the forensic timeline across all runs.

### Checkpoint
A preserved partial state (typically a git commit) taken before a destructive step such as reset/overwrite, so prior work is recoverable.

### Resumability
The property that a `/clear` + re-invoke continues a pipeline at the first incomplete agent, driven by the progress file or on-disk artefact presence.
Canonical source: `CLAUDE.md §1`.

### Definition of done (DoD)
An agent's or orchestrator's explicit completion checklist that gates handback acceptance and final `status: complete`.

### Self-validation
An agent's pre-handback checks of its own output (closed-set conformance, citation integrity, etc.). Every artefact write is followed by `verify-artifact-write` (sha256 + min-bytes); a mismatch is an `RF-04` hard halt.
Canonical source: `framework/skills/verify-artifact-write.md`.

### Source-manifest
The canonical record of consultant inputs (`requirements/source-manifest.json`) — per-file tier, format, conversion status, provenance, and the build `target`. Shared by `/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`; lifecycle owned solely by the input-handler.
Canonical source: `framework/agents/input-handler.md`.

### Sidecar
A compact machine-readable companion to a prose artefact — e.g. a claims `*.ndjson` beside a draft, or an analysis `*.sidecar.json` carrying a role-keyed `architect_projection` so consumers read a small projection instead of full prose. Sidecar-first reading avoids context bloat.
Canonical source: `framework/assets/analyses/sidecar-schema.md`.

### Input tier
The classification of an input file by how it can be ingested — Native, Supported-via-MCP, Unsupported — set by `classify-input-tier` and recorded on the manifest row; governs conversion and `RF-01` pauses.
Canonical source: `framework/skills/classify-input-tier.md`.

---

## 7 · People & roles

### Consultant
The human operating the system in Claude Code — the solo consultant/BA who drops inputs, answers `AskUserQuestion` prompts in-thread, and accepts artefacts. Every interactive surface is foreground for the consultant.
Not to be confused with: **reviewer** or **target-user**.

### Reviewer
Anyone who opens a generated prototype to evaluate the design (uses the role switcher to inspect each persona's view). A consumer of output, not the operator.

### Target-user (persona)
A persona of the *product under design* — the end user whose goals the requirements serve (defined in `requirements.md §3`). Bound to wireframe variants and posture choices.
Not to be confused with: **consultant** (operator), **reviewer** (evaluator), or **character** (an agent's voice file).

---

## 8 · Disambiguation map (the overloaded clusters)

Quick entry-point when several similar terms collide. Each row points to the canonical entries above; it does not redefine them.

| Cluster | Resolution |
|---|---|
| screen / surface / page / view | **logical surface** (`LS-NN`, blueprint) → **physical screen** (`S-NN`, realized) → **screen file** (wireframe HTML). "page"/"view" = avoid as system terms. |
| Design / design-system / design-spec / design philosophy | **Design** = UX/IA design (not styling) · **design-system** = brand-token brief · **design-spec** = a prototype's realization plan · **design philosophy** = label for a **UX posture**. |
| posture / philosophy / position / stance | **UX posture** = named preset · **design philosophy** = its label (alias) · **position** = a numeric `-2..+2` on a dimension · "stance" = avoid. |
| variant (wireframe vs prototype) | **wireframe variant** = a config in `variants.json`; a **prototype** is one-per-run — no "prototype variant"; inter-prototype divergence = posture + positions. |
| requirements / blueprint / design-spec | **requirements** (`requirements.md`, the input spec) → **blueprint** (scope decomposition IR) → **design-spec** (prototype realization). |
| realization / pattern / component | **realization** = IA strategy (how a surface becomes screens) · **pattern** = a catalogue UI pattern *inside* a screen · **component** = its React implementation. |
| fixture / store / seed | **fixture** = on-disk JSON data · **store** = live in-memory state · **seed** = the act of loading fixtures into the store. |
| lens / methodology / analysis / review | **methodology** = the named method · **lens** = its informal consultant-facing synonym · **analysis** = a lens-transform output · **review** = a critique output. |
| claim / citation / grounding / traceability | **claim** (asserted fact) → **citation `[SRC]`** (its source) → **grounding** (the act of linking) → **traceability** (the end-state auditability). |
| scope-slug / name-slug | **scope-slug** identifies a *scope* (`blueprints/`, `wireframes/`); **name-slug** identifies a single *prototype* (`prototypes/src/app/<name-slug>/`). |
| brand / design-system / theme | **brand** = the fixed visual identity (uniform across prototypes) · **design-system** = the brief defining it · **theme** = the shared `theme.css` that applies it. |
| architect_roles / architect_projection / role-keyed | Schema of the analysis sidecar — see `framework/assets/analyses/sidecar-schema.md` (canonical); the glossary does not restate the schema. |
| primary_basis / wireframe_basis | Schema fields marking a chosen wireframe variant as a prototype's design basis — see `framework/agents/prototype-spec-drafter.md` (canonical). |

> **A note on discouraged terms.** *page*, *view*, and *stance* are non-preferred synonyms — prefer *surface*/*screen* and *position*/*posture*. This is guidance, not enforced; a future alignment pass may add a lint.
