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
Not to be confused with: **persona** (see *target-user*); **Application character** (the product's own copy voice, recorded in `requirements.md` §1.8).

### Application character
The persona/voice of the application-under-specification's **own user-facing copy** — notifications, error messages, validation messages, confirmations, empty states. Recorded in `requirements.md` §1.8: input-stated (`[SRC]`-cited) or drafter-inferred and consultant-resolved via the standard blocking `[AI-SUGGESTED]` workflow (gap-pass A16). Governs tone and phrasing only — never which feedback exists, its structure, placement, or vocabulary. Consumed downstream by `/wireframe` (via the blueprint) and `/prototype` (via design-spec §3) when phrasing generated copy.
Canonical source: `framework/assets/template-requirements.md` §1.8.
Not to be confused with: **Character** (an agent's voice file under `framework/assets/characters/`); a **target-user persona** (§3 — who uses the app, not how it speaks).

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

### Amendment (AMD-NN)
An entry in the transient `## Amendments (pending re-merge)` section of `requirements/requirements.md` that **supersedes** the base text it names, everywhere in the document, until the next `/requirements` run regenerates the document and folds its source into the body with `[SRC: C-NNN]` citations. Written only by `framework/skills/apply-amendments-section.md`, called by `/resolve-review` (Step 9b, consultant opt-in) or `/amend-requirements` (Step 9, unconditional). Numbering is per-section and continuous across runs; entries carry an origin marker and, where candidate-derived, a grounding tag. Downstream consumers apply them as supersessions without re-litigating them — `blueprint-architect` extends or shrinks the **Properties closed set** on their authority, and `/export-application` retains them byte-identical. Canonical shape: `framework/assets/resolve-review/template-addendum.md`.
Not to be confused with: an **amendments document** (the durable `input/` record the section caches — see below). The section is a cache; deleting it loses nothing, because the record survives in `input/`. An amendment that exists *only* in the section is destroyed by the next re-merge.

### Amendments document
The consultant-approved input document `/amend-requirements` writes as a NEW dated file into `input/` (`amendments-<date>.md`, never overwriting), turning changes the consultant states in-thread about a finished `requirements.md` into first-class corpus material the next `/requirements` run ingests. Each entry is anchored on a **verbatim quote of the base text it supersedes** (there is no review finding to anchor to — the document itself is the anchor), carries exactly one origin marker — `[CONSULTANT-STATED]` or `[AI-INFERRED, CONSULTANT-CONFIRMED]` (the latter only from an *individual* candidate selection; this pipeline offers no accept-all path) — exactly one Supersedes line, and exactly one **Impact** line from the closed flag set `closed-set-change` / `scope-change` / `amends-amendment` (computed from the document, never asked). Block IDs are `AM-NN`, document-local and deliberately independent of the host document's `AMD-NN` numbering. Canonical skeleton + `AM-NN` / Amends / Impact definitions: `framework/assets/amend-requirements/template-amendments.md`; origin markers and grounding tags are reused from `framework/assets/resolve-review/template-resolutions.md`.
Not to be confused with: the **review resolutions document** (same durable-record role, but sourced from a review artefact's findings rather than the consultant's own statements), or the **amendment** entries in the host document (its transient cache).

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
Aliases: *brand-lock*, *theme*. Not to be confused with: **design-system** (the *brief/artefact* that defines the brand tokens), or **visual-craft floor** (how well the brand's tokens are *used*, which is uniform too but is a quality bar, not an identity).

### visual-craft floor
The shared, non-negotiable bar for how a generated prototype **looks and feels** — token binding, press response, hover shift, overlay entrances, the elevation ladder, type hierarchy, spacing rhythm, focus, and the responsive contract. It is a *floor*, not a style: it raises quality uniformly and is never a divergence axis, so it coexists with brand-lock rather than competing with it. Complements the **UX baseline** (which governs whether a surface *works*); a posture may emphasise items but never waives either.
Canonical source: `framework/assets/prototypes/visual-craft-standard.md`.
Not to be confused with: **brand** (the identity the floor binds to), **UX posture** (layout/workflow divergence), **UX baseline** (usability/accessibility floor).

### press response
The tactile feedback every clickable element gives when pressed: it scales to **98%** over the fast duration — a firm press, not a collapse. Applied structurally by the template's global press layer in `globals.css` (matching semantic controls plus anything marked `data-pressable`), using the CSS `scale` property so a component-level override cascades instead of compounding. Press is **transform + elevation only, never a colour change**, so it cannot introduce a fill state whose on-colour was never measured. Clickable table rows are the one exception, pressing via the `accent` fill.
Canonical source: `framework/assets/prototypes/visual-craft-standard.md §2`.
Not to be confused with: **hover shift** (pointer-arrival feedback) or the `active` state's role in the six required interactive states.

### elevation ladder
The four meaning-bound elevation rungs — `shadow-xs` hairline, `shadow-sm` resting card, `shadow-md` hovered/raised, `shadow-lg` overlay — registered in `theme.css`'s `@theme` as Tailwind's `--shadow-*` and backed per colour mode by `--elevation-*` (a dark set raises the black alpha over the same geometry). Rungs are never skipped on hover, and elevation is never stacked with a heavy border.
Canonical source: `framework/assets/prototypes/visual-craft-standard.md §5` (values: `framework/skills/extract-brand-theme.md`).

### device target
The set of viewports one prototype must work at, chosen by the consultant per prototype at `prototype-orch.md` Step B(5) and recorded as the design spec's `device_targets` (front-matter key + §4b table): `{ primary, breakpoints, touch }` over the named viewports **mobile** 390×844 (touch), **tablet** 768×1024, **desktop** 1280×800. `primary` names the viewport the full per-route smoke runs at; each additional breakpoint gets one bounded layout-integrity check. Per prototype, not per app — two prototypes in the same shared app may legitimately target different devices, and a shared component reused at a narrower target is **widened**, never forked.
Canonical source: `framework/assets/prototypes/visual-craft-standard.md §11`.
Not to be confused with: **mode (design-system)** (colour scheme, app-level and scaffold-locked) or **posture** (layout/workflow preset).

### design-system
The brand-token brief produced by `/design-system` (`design-system/design-system-light.html` and/or `design-system-dark.html`) — colour/type/shadow/motion tokens. The *source* of a prototype's `theme.css`. One self-contained file per **mode (design-system)**; the unsuffixed `design-system.html` is retired.
Not to be confused with: **Design** (UX), **design-spec** (prototype realization), **design philosophy** (posture).

### mode (design-system)
The colour scheme a design-system artefact renders — `light` or `dark`. One file per mode (`design-system/design-system-<mode>.html`), each a complete single-mode document; there is no in-document switcher and no combined file. The consultant chooses `light-only` / `dark-only` / `both` at step-05b §E — asked *after* extraction, so the question can name the scheme actually found. The mode is marked in the filename, the `<title>`, the H1, and `meta.mode`. Only the 11 colour and 3 shadow tokens differ between modes; the other 19 (typography + motion) are shared verbatim.
Canonical source: `framework/agents/design-system-styler/steps/step-05b-domain-inference.md` + `framework/agents/design-system-styler/data/cross-mode-derivation-rules.md`.
Not to be confused with: **hue source** (which mode is the grounded one), **Design** (UX), **design philosophy** (posture).

### hue source
The colour mode whose palette is **grounded** — the scheme actually extracted from the reference URL, or domain-inferred light when no URL was given. Recorded as `meta.hue_source` (`extracted-light` | `extracted-dark` | `domain-inferred-light`) and carrying `meta.primary: true` in its file. The *other* mode is **derived** from it per `cross-mode-derivation-rules.md`, tagged `inferred-from-domain` with a `derived: <target> variant of <source> <token> (<hex>)` source string, and is never presented as extracted.

Nothing in the pipeline assumes light: a reference URL ships a dark palette as readily as a light one, and when it does, **light is the derived mode**. The hue-source file is always written — it is both the grounded record and the derivation seed — so asking for one mode against a site in the other scheme legitimately produces two files.
Canonical source: `framework/agents/design-system-styler/data/cross-mode-derivation-rules.md`.
Not to be confused with: **mode (design-system)** (which scheme a *file* renders), **provenance marker** (the two-value `prov` set, which derivation does not extend).

### colour-mode strategy
How a prototype's users move between light and dark — one of `toggle` (a control in the application UI, defaulting to the OS/browser setting), `system` (follows `prefers-color-scheme`, no control), `none` (a single mode, no switching), or `custom` (consultant free text, bounded to the default mode / control placement / 2- vs 3-state). Chosen **once per app** at `/prototype` Step B(4b) and locked into `prototypes/.scaffold.json` alongside the brand (D1); later runs ask nothing.

The question is asked **only** when both `design-system/design-system-light.html` and `design-system/design-system-dark.html` exist. Any other state — one mode file, a consultant-supplied brand, template defaults — is a determined outcome: `strategy: none`, reported in one status line, no menu. `/prototype` never derives a missing mode; that is `/design-system`'s contrast-gated job.

Realized by one mechanism regardless of strategy: a `.dark` class on `<html>`, selecting between `theme.css`'s `:root` and `.dark` token blocks. Distinct from **on-colour**, which is about legibility *within* whichever mode is active.
Canonical source: `framework/orchestrators/prototype-orch.md` Step B(4b) + `framework/assets/prototypes/app-shell-spec.md`.
Not to be confused with: **mode (design-system)** (which scheme a design-system *file* renders), **hue source** (which mode is grounded), **design philosophy** (posture).

### on-colour
The label/icon colour that sits on a filled element — `--primary-foreground` on `--primary`, `--success-foreground` on `--success`, and so on. Derived per colour mode by `framework/skills/extract-brand-theme.md` by **measuring** near-white and near-black against the actual fill and taking the higher scorer — never inferred from the mode, which demonstrably fails (a light-mode brand accent of `#00D6FF` scores 1.74:1 for white and 11.37:1 for black).

Validated against every state the fill appears in, not just at rest: the shipped shadcn primitives composite fills at `/90`, `/80`, `/60`, `/50` and `/30` over the mode's background, and a label that passes at rest can fail on hover. When no candidate clears 4.5:1 across all states, the **fill** is nudged in lightness (hue and saturation preserved) and the change is logged — the same operation `contrast-validation.md` performs upstream, applied where `/design-system`'s deliberately-narrow four-pair gate does not reach.
Canonical source: `framework/skills/extract-brand-theme.md` > *Contrast & on-colours*.
Not to be confused with: **colour-mode strategy** (how users switch modes), **mode (design-system)**.

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
The shared layout/structure wrapping every prototype (nav, regions) — in practice **any** component that wraps a surface's content, whether a per-prototype `layout.tsx` or a `templates/*Shell` composed per page; it is never assumed to be a singleton. The prototype **chrome** (`PrototypeChrome` — role switcher, data-reset, *inter*-prototype nav) sits *outside* the app under design (PI-08), so it is never treated as a design surface. The two navs are different things: the chrome's jumps **between** generated prototypes; the application's own nav (from the **Nav table**) moves **within** one.
Canonical source: `framework/assets/prototypes/app-shell-spec.md`.

### Nav table
The generated, per-prototype list of intra-prototype destinations — `{ route, label, surface_id, roles }` per entry — written by the generator driver before sub-agent dispatch and resolved at runtime by route (`NAV_BY_PROTOTYPE[<slug>]`), because app shells are *shared* components and cannot import one prototype's nav. It is the **only** grant table: roles come from `proto-chrome-store.activeRole` (PI-05), per-destination visibility from here. Distinct from the **prototype registry**, which is inter-prototype (one row per prototype, the landing link). Any second derivation — a hand-rolled array, a `navItemsForRole()` helper, a role→pages store method — is a defect.
Canonical source: `framework/assets/prototypes/shared-component-conventions.md` §6a.

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
Contrast **Scope marker** — a different axis, and not a member of this closed set.

### Scope marker (`[PROTO-ONLY]`)
A paired inline span — `[PROTO-ONLY] … [/PROTO-ONLY]` — wrapping content that is true of the prototype and false or meaningless for the application build. Distinct in *axis* from a **Provenance marker**: provenance answers *"where did this value come from?"*, scope answers *"which build target does this apply to?"*. Because the axes are independent, a scope span may co-occur with a `[SRC: C-NNN]` citation and with one provenance marker, and is therefore exempt from the provenance markers' mutual-exclusion rule. The merger **retains** it (as it retains `[SRC:]`); `/export-application` deletes each span whole with a single non-greedy regex, which is what makes that export a mechanical transform rather than a prose-reading heuristic. A span never crosses a markdown block boundary, and never wraps a normative requirement — only a realization note about one.
Canonical source: `framework/shared/prototype-scope.md > Prototype-only content marking`.

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

### Stadium-app (input unit)
A deployed Twenty57 Stadium 6 low-code web app dropped into `input/` — either as a folder (`administration.db` + `App_Data/Updates/*.sapz` + `ClientApp/`) or as a one-line `*.stadium` pointer file naming such a folder — treated as a single input *unit* rather than a per-file tier row. Extracted once by the standalone `/ingest-stadium` command; the input-handler's **Step S** pre-pass separately **excludes** it from manifest enumeration + the freshness check and **nudges** the consultant when it is un-ingested. Only its extracted assets become manifest rows.
Canonical source: `framework/orchestrators/ingest-stadium-orch.md` + `framework/agents/stadium-ingestor.md` + `framework/skills/extract-stadium-app.md` (extraction); `framework/agents/input-handler.md` (Step S exclusion + nudge).
Not to be confused with: **input tier** (a per-file ingest classification) — a Stadium-app is a unit that is extracted into ordinary `Native-text` files, not itself a tier.

### Stadium extractor
The sanctioned runtime-code helper `framework/tools/extract_stadium_app.py` (stdlib-only Python) that shards a Stadium-app into its category assets (deterministic Phase A) — invoked by `extract-stadium-app.md`, whose Phase B adds bounded advisory `[AI-SUGGESTED]` assets. An ingestion runtime-code exception, sibling to the markitdown/inkscape ingestion CLIs.
Canonical source: `framework/skills/extract-stadium-app.md` (wraps the tool).
Not to be confused with: the **observability** tools under `framework/tools/` (e.g. `timing-report.mjs`), which only read state and never produce pipeline inputs.

### Category asset (`.stadium-assets`)
One of the lean, citation-ready requirement files the Stadium extractor writes under `input/<AppName>.stadium-assets/` (`<stem>.stadium.{overview,data-model,…}.md` Tier-1 + the advisory Phase-B assets). Each is an ordinary `Native-text` input the normal pipelines consume; the consultant may hand-edit them (the processed-ledger preserves edits).
Canonical source: `framework/skills/extract-stadium-app.md` + `framework/assets/stadium/asset-schemas.md`.
Not to be confused with: the app-domain **Stadium glossary** (`framework/assets/stadium/glossary.md`) — that is reference knowledge, not an extracted per-app asset.

### Processed-ledger
The runtime ledger `framework/state/.stadium-processed.json`, keyed by `app_id` (the app folder basename, equal to its Stadium `FileGuid`), recording which Stadium-apps have been extracted. An already-ledgered app is skipped by the `stadium-ingestor` (process-once contract), protecting consultant hand-edits to its category assets, unless the consultant re-ingests it via the orchestrator's re-ingest gate (which removes the entry). Read read-only by the input-handler's Step S for the un-ingested nudge.
Canonical source: `framework/agents/stadium-ingestor.md` (writes it) + `framework/orchestrators/ingest-stadium-orch.md` (re-ingest reset removes an entry).

### Stadium ingestion command (`/ingest-stadium`)
The standalone command that turns a **Stadium-app (input unit)** dropped in `input/` into its **category assets** — the sole trigger for Stadium extraction (formerly the input-handler's Step S pre-pass). A thin command shim launches `framework/orchestrators/ingest-stadium-orch.md`, which runs the **Stadium ingestor** agent in the foreground and surfaces the per-app re-ingest gate. Standalone: it never touches `requirements/` state or builds the source manifest — the produced assets are picked up as ordinary `Native-text` inputs by the next input-consuming pipeline run.
Canonical source: `.claude/commands/ingest-stadium.md` + `framework/orchestrators/ingest-stadium-orch.md`.
Not to be confused with: the input-handler's **Step S** — which no longer extracts; it only excludes the raw app folder/pointer and nudges.

### Stadium ingestor
The agent `framework/agents/stadium-ingestor.md` that owns the per-app extraction lifecycle for `/ingest-stadium`: detect Stadium units, skip already-ledgered apps (process-once), preflight Python (`RF-01`), delegate to the **Stadium extractor** via `extract-stadium-app.md`, and write the **processed-ledger**. It is the standalone home of the logic formerly in the input-handler's Step S.
Canonical source: `framework/agents/stadium-ingestor.md`.

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
| amendment / amendments document / review resolutions document · `AMD-NN` / `AM-NN` | **amendment** (`AMD-NN`) = an entry in the *transient* `## Amendments (pending re-merge)` section of `requirements.md` — a **cache**, cleared by the next re-merge · **amendments document** = the durable `input/amendments-<date>.md` `/amend-requirements` writes, whose entries are `AM-NN` (document-local, independent of `AMD-NN`) · **review resolutions document** = the same durable role but sourced from a review's findings (`/resolve-review`). The record is always the `input/` file; the section is only its projection. |
| scope-slug / name-slug | **scope-slug** identifies a *scope* (`blueprints/`, `wireframes/`); **name-slug** identifies a single *prototype* (`prototypes/src/app/<name-slug>/`). |
| brand / design-system / theme | **brand** = the fixed visual identity (uniform across prototypes) · **design-system** = the brief defining it · **theme** = the shared `theme.css` that applies it. |
| architect_roles / architect_projection / role-keyed | Schema of the analysis sidecar — see `framework/assets/analyses/sidecar-schema.md` (canonical); the glossary does not restate the schema. |
| primary_basis / wireframe_basis | Schema fields marking a chosen wireframe variant as a prototype's design basis — see `framework/agents/prototype-spec-drafter.md` (canonical). |

> **A note on discouraged terms.** *page*, *view*, and *stance* are non-preferred synonyms — prefer *surface*/*screen* and *position*/*posture*. This is guidance, not enforced; a future alignment pass may add a lint.
