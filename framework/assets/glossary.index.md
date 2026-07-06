# System glossary — index

Slim lookup of `framework/assets/glossary.md`. Consult this table for the canonical term + a one-line gloss; **Read the matching `### Term` section in `glossary.md` on demand** when you need the full definition, `Canonical source:`, or `Not to be confused with:` detail. Loading this index instead of the full body keeps the vocabulary out of context for a whole run.

Format: one row per term — `Term | one-line gloss | canonical owner (if another file owns the schema/IDs) or — `.

Add a row here whenever a `### Term` is added to `glossary.md`; keep the two in lockstep (row count == `###` count). Alphabetised here; grouped by concept in the body.

| Term | Gloss | Canonical owner |
|---|---|---|
| Agent | Persona+workflow `.md` the LLM adopts to produce one content artefact. | `docs/maintenance.md > Separation of concerns` |
| Analysis | Output of a lens-transform methodology on requirements/inputs (`analyse-*`). | registries |
| Anti-fabrication | Rule: no data-bound element may invent a property outside the closed set. | `blueprint-architect.md` |
| Application character | The product's own copy voice (notifications/errors/validations/confirmations/empty states), recorded in `requirements.md` §1.8; not an agent Character. | `template-requirements.md` §1.8 |
| App shell | Shared layout wrapping every prototype; the chrome sits outside the app under design (PI-08). | `prototypes/app-shell-spec.md` |
| Asset | Read-only reference content under `framework/assets/`. | `docs/maintenance.md > Separation of concerns` |
| Blueprint | Shared scope IR: logical surfaces + closed sets + allowed realizations; no patterns/realization chosen. | `blueprint-architect.md` |
| Brand | Fixed visual identity applied uniformly across all prototypes (one `theme.css`). | `prototypes/app-shell-spec.md` |
| Build target | Manifest output-mode field, auto-set to prototype (fixtures); application = legacy value / export-time concern (`/export-application`). | `prototype-invariants.md` PI-06 |
| Category asset (`.stadium-assets`) | Lean citation-ready `Native-text` file the Stadium extractor writes under `input/<AppName>.stadium-assets/`; consumed by the normal pipelines. | `skills/extract-stadium-app.md` |
| Character | Persona file giving an agent its stance/voice; not a product persona. | `assets/characters/` |
| Checkpoint | Preserved partial state (often a git commit) before a destructive step. | — |
| Citation (`[SRC: …]`) | Inline marker grounding a claim in an input source; retained in the final `requirements.md` as downstream provenance (only resolution markers are stripped). | `CLAUDE.md > Markers in content` |
| Claim | One asserted fact/decision recorded with its source in an NDJSON sidecar. | — |
| Command | Slash-command shim under `.claude/commands/` that names its orchestrator. | `CLAUDE.md §1` |
| Consultant | The human operating the system; answers prompts in-thread, accepts artefacts. | `CLAUDE.md §1` |
| data-src / data-prop | Audit attributes: requirement citation / closed-set property on generated nodes. | `shared-component-conventions.md` |
| Definition of done (DoD) | An agent/orchestrator completion checklist gating handback + final status. | — |
| Design | UX/IA design (structure, workflow, behaviour) — **not** visual styling. | glossary.md §8 |
| design-system | The brand-token brief (`design-system.html`); source of a prototype's theme. | `/design-system` output |
| Design-spec | One prototype's realization plan (posture + positions + workflow + bindings). | `prototypes/template-design-spec.md` |
| Dispatcher | Role distributing work to parallel sub-agents (e.g. per-surface generation). | `prototype-generator/` |
| Divergence (divergence profile) | How variants/prototypes differ; goal-driven profile derived once into `scope.json`. | `scope-selector.md` |
| Drafter | First triplet agent: emits the artefact with provenance markers + claims sidecar. | — |
| Fixture | Static in-memory JSON data shipped with a prototype (PI-02). | `prototype-invariants.md` |
| General rule (GR-NN) | Deterministic reusable rule the resolver applies without asking. | `shared/general-rules.md` |
| Grounding | The act of linking a claim to a real source; ungrounded facts fail validation. | — |
| Handback gate | Orchestrator checkpoint accepting/re-invoking a finished agent. | orchestrators |
| Input tier | Ingest classification (Native / Supported-via-MCP / Unsupported). | `skills/classify-input-tier.md` |
| Logical surface (LS-NN) | Decomposition-agnostic blueprint surface, pre-screen-count. | `blueprint-architect.md` |
| Merger | Third triplet agent: strips markers, validates, writes the clean final artefact. | — |
| Methodology | A named analysis/critique method (OOUX, ADVERSARIAL, GLOSSARY …); "lens" = its alias. | registries |
| Orchestrator | Pipeline control-flow owner; sequences agents, owns state/gates; no content edits. | `docs/maintenance.md > Separation of concerns` |
| Orphan (traceability) | A final-doc fact/requirement that traces to no provenance class; the headline defect of the REQUIREMENTS-TRACEABILITY review. | `reviews/requirements-traceability-reference.md` |
| Physical screen | A concrete screen produced by realizing a logical surface (`S-NN`). | `realization-strategies.md` |
| Position | Signed `-2..+2` stance on one trade-off dimension; labelled, never shown as notation. | `position-vocabulary.md` |
| Preflight gate | Orchestrator check before any agent runs (prereqs, prior progress). | orchestrators |
| Processed-ledger | Runtime `state/.stadium-processed.json` keyed by `app_id`; skips already-extracted Stadium-apps (process-once). | `agents/stadium-ingestor.md` |
| Progress file | Per-orchestrator JSON tracking `called`/`completed` per agent for resume. | orchestrator Tools |
| Properties closed set | Blueprint's per-surface list of allowed data properties; the anti-fabrication boundary. | `blueprint-architect.md` |
| Prototype | One hi-fi clickable client-side realization of a scope; accrues in one shared app. | `prototype-orch.md` |
| Prototype invariant (PI-NN) | Behavioural contract every prototype satisfies (`PI-01..08`). | `shared/prototype-invariants.md` |
| Provenance markers | Closed tag set: `[AI-SUGGESTED]` `[STANDARD-RULE]` `[OUT-OF-SCOPE]` `[POSTURE-DEFAULT]`. | `CLAUDE.md > Markers in content` |
| Realization (realization strategy) | Closed-enum IA choice turning a surface into screen(s): standalone/drawer/expand/wizard/modal. | `realization-strategies.md` |
| Refusal (RF-NN) | Canonical halt predicate; pause/hard-halt with defined severity. | `shared/refusal-registry.md` |
| Resolver | Second triplet agent: resolves `[AI-SUGGESTED]` markers with the consultant. | — |
| Resumability | A `/clear` + re-invoke continues at the first incomplete agent. | `CLAUDE.md §1` |
| Review | Output of a critique methodology (`review-*`); interrogates rather than transforms. | registries |
| Review resolutions document | Consultant-approved `/resolve-review` output: a NEW dated `input/` file turning selected review findings into corpus material (verbatim-anchored, origin-marked, supersession-explicit). | `assets/resolve-review/template-resolutions.md` |
| Reviewer | Anyone evaluating a generated prototype (uses the role switcher). | — |
| Scope | The requirement-ID subset a wireframe/prototype run addresses; captured in `scope.json`. | `scope-selector.md` |
| Scope-slug | Kebab-case scope id naming `blueprints/`/`wireframes/`; cf. name-slug (a prototype). | `scope-selector.md` |
| Seed | The act of hydrating a store from fixtures (`seedFromFixtures()`). | — |
| Self-validation | An agent's pre-handback checks; each write verified by `verify-artifact-write`. | `skills/verify-artifact-write.md` |
| Shared | Cross-pipeline invariants under `framework/shared/`; append-only. | `docs/maintenance.md > Separation of concerns` |
| Sidecar | Compact machine-readable companion to a prose artefact (claims/projection JSON). | `analyses/sidecar-schema.md` |
| Skill | Reusable parameterised unit of agent behaviour returning a structured result. | `docs/maintenance.md > Separation of concerns` |
| Source-manifest | Canonical input record (`source-manifest.json`); owned solely by the input-handler. | `agents/input-handler.md` |
| Stadium extractor | Runtime-code helper (`tools/extract_stadium_app.py`) that shards a Stadium-app into category assets; an ingestion exception. | `skills/extract-stadium-app.md` |
| Stadium ingestion command (`/ingest-stadium`) | Standalone command that extracts a Stadium-app into its category assets; sole trigger for Stadium extraction. | `orchestrators/ingest-stadium-orch.md` |
| Stadium ingestor | Agent owning per-app Stadium extraction for `/ingest-stadium` (detect, skip-if-ledgered, preflight, extract, write ledger). | `agents/stadium-ingestor.md` |
| Stadium-app (input unit) | A deployed Twenty57 Stadium 6 app dropped into `input/`; extracted once by `/ingest-stadium`; excluded + nudged at the input-handler's Step S. | `agents/stadium-ingestor.md` |
| Store | Client-side state container a prototype reads/writes, initialised from fixtures. | `shared-component-conventions.md` |
| surface_plan | Per-variant JSON authoring realization + pattern picks + screens per `LS-NN`. | `blueprint-architect.md` |
| Target-user (persona) | A persona of the product under design (`requirements.md §3`); not the consultant. | `requirements.md §3` |
| Timing event | Append-only NDJSON record of the run timeline (`timing.ndjson`). | `state/timing.ndjson` |
| Trade-off dimension | One of six axes `D1..D6` a design is positioned on (D6 inactive). | `trade-off-dimensions.md` |
| Traceability | End-state: every final fact follows back to a citation or marker. | `CLAUDE.md §1` |
| UX posture | Named preset over dimensions + structural choices (P1–P6); the "design philosophy". Cross-pipeline: manual single pick in `/prototype`, auto-recommended per variant in `/wireframe`. | `wireframes/design-philosophies.md` |
| Wireframe variant | One persona-bound config in `variants.json`; a prototype is one-per-run, not a variant. | `blueprint-architect.md` |
