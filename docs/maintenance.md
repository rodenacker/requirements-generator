# Maintenance & extension rulebook

> The **rules for changing this system** — roles & write-isolation, file/component placement, the canonical-source rule, and naming patterns. **Load on demand** when planning or making system additions/changes; this file is *not* auto-loaded. The map of what already exists is `docs/architecture.md`; the consultant-facing behavioural contract is `CLAUDE.md`. These rules were relocated verbatim from `CLAUDE.md` — cite sections of this file by title (e.g. `docs/maintenance.md > Canonical-source rule`).

## 1. Roles & write isolation

### Separation of concerns

- **Orchestrator** = control flow only. Reads progress/timing, deletes during reset, writes events. Never edits content artefacts (one exception: drafter handback gate reads `draft-claims-verification.ndjson` summary line).
- **Agent** = content production. Reads inputs, writes its one artefact, owns its self-validation + handback. Never writes outside its scoped output paths.
- **Skill** = reusable procedure. Parameterised by inputs. Returns `pass | <RF-NN> trigger | structured-row | ok`. No file I/O outside its declared inputs/outputs.
- **Asset** = read-only reference. Templates, registries, taxonomies, characters, pattern catalogue.
- **Shared** = cross-pipeline invariants (rules, scope, refusals, invariants, setup-instructions). Read-only; mutated only by appending new IDs.
- **State** = orchestrator/agent runtime scratch. Each owner declared in the orchestrator's Tools section.

### Stand-alone constraints (write isolation)

Each pipeline writes **only to its own output dir**. The four **documented cross-pipeline exceptions** (the first two inherited from shared agents, the third and fourth pipeline-private to `/resolve-review`):

- **`input-handler.md`** (shared by `/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`) writes `requirements/source-manifest.json` and `input/*.converted.md` siblings. The `*.converted.md` siblings are of two kinds: markitdown renderings of `Supported-via-MCP` files, and **frozen vision descriptions** of visual inputs (`Native-multimodal` rasters and rendered `Vector-renderable` diagrams — `.svg/.drawio/.vsdx`), produced via `framework/skills/describe-visual-input.md` so each visual is *interpreted once* and every downstream input-consumer reads the same text (the **Read-path resolution** rule, canonical in `framework/skills/build-source-manifest.md`: read `converted_sibling` when non-null, else `original_path`). Visual descriptions are clobber-protected — regenerated only when absent or the original's sha256 changed — so consultant edits persist. Step-0 decides create / refresh / no-op / halt; only create + refresh write. When invoked with `progress_path: null` (i.e. by `/analyse-inputs` or `/review-inputs`), does not touch `framework/state/*`.
- **`blueprint-architect.md` + `scope-selector.md`** (shared by `/wireframe` and `/prototype`) write `blueprints/<scope-slug>/{scope.json, blueprint.md}`.
- **`resolve-review-drafter.md`** (private to `/resolve-review`) writes one NEW `input/<stem>-<date>.md` per accepted run — **additive only**, never overwriting an existing `input/` file (same-day collisions suffix `-2`, `-3`). The draft is staged under `resolve-review/` and never enters `input/` unaccepted.
- **`resolve-review-drafter.md` Step 9b** (review-requirements-sourced runs, consultant opt-in only) inserts/extends the single `## Amendments (pending re-merge)` section in `requirements/requirements.md` — **bounded to that one section** (placed before the PI appendix; no other byte changes), always paired with — and a subset of — the `input/` resolutions doc written first (the pairing invariant). The section is a transient cache: the next `/requirements` re-merge regenerates the doc and folds the same resolutions in from `input/`. Canonical shape: `framework/assets/resolve-review/template-addendum.md`.

Full per-pipeline read/write enumeration: `docs/architecture.md`.

## 2. File and component placement rules

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
- New pipeline output artefact → its pipeline's dedicated dir. **Never** write outside this dir (the input-handler / blueprint-architect exceptions are documented under *Stand-alone constraints (write isolation)* above and bounded to specific paths).
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

### Naming patterns

- **Commands.** `.claude/commands/<verb>.md`. Single lowercase verb.
- **Orchestrators.** `framework/orchestrators/<verb>-orch.md`.
- **Agents.** Pipeline-private: `framework/agents/<pipeline>-<role>.md` (`requirements-drafter.md`). Cross-pipeline: `framework/agents/<role>.md` (no pipeline prefix — `input-handler.md`, `blueprint-architect.md`). Methodology: `framework/agents/<plural-pipeline>/<method>-(analyser|reviewer).md`. Multi-file agent → subdir with `steps/`, `prompt-templates/`, `data/`.
- **Skills.** `framework/skills/<verb-noun>.md` — verb-led, hyphenated, lowercase.
- **Assets.** Templates `template-<thing>.{md,html}`; references `<method>-reference.md`; characters `<persona-or-stage>.md` under `assets/characters/`; taxonomies `taxonomy-<dimension>.md`; topics `topics-<pipeline>.md`; registries `registry.md` inside the pipeline-plural subdir.
- **Shared.** `<noun>.md` / `<noun>-registry.md` / `<noun>-invariants.md`. Stable-ID files use `NN-NN` numbering inside; never renumber.
- **State.** `.progress.json`, `timing.ndjson`, `<agent>-<role>.ndjson|json` under `framework/state/`.
- **Pipeline outputs.** `<artefact>.md/.html/.json/.ndjson` under the pipeline's own dir. Analyses + reviews use UPPERCASE-METHOD subdirs (`analyse-requirements/OOUX/`, `review-inputs/COMPLETENESS-REVIEW/`). `/prototype` is the exception — it generates a Next.js app under `prototypes/` with kebab-case per-prototype route segments (`prototypes/src/app/<name-slug>/`) + non-routed dot-state (`prototypes/.specs/<name-slug>/`, `.registry.json`, `.scaffold.json`).
- **Timing events.** `run_start`, `run_end`, `stage_start`, `stage_end`, `substep_start`, `substep_end`, `consultant_prompted`, `consultant_responded` — all NDJSON, append-only via PowerShell `Add-Content`.
- **Progress events.** `called` / `completed` per agent.
