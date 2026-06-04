---
role: asset
kind: registry
methodologies:
  # MVP — fully implemented and selectable via /analyse-requirement. Curated order + `group`
  # drive the selector's lens grouping + `★ suggested next` flag (see framework/skills/analysis-selector.md).
  - name: data-model
    status: mvp
    group: Objects, data & lifecycle
    description: Choose this when the requirements imply data but never state the schema and you need an explicit entity model before designing forms, lists, and detail views. It produces an HTML data model of the entities, attributes, and relationships the requirements imply, each traced back to its source requirement. Use it as the schema your screens and field-level UI are designed against, and to spot entities the requirements left undefined.
    output_path: analyse-requirements/DATA-MODEL/data-model.html
    reference_asset: framework/assets/analyses/data-model-reference.md
    template_asset: framework/assets/analyses/template-data-model.html
    map_skill: framework/skills/map-data-model-to-ui.md
    analyser_agent: framework/agents/analyses/data-model-analyser.md
    character: framework/assets/characters/data-model-analysis.md
  - name: jtbd
    status: mvp
    group: Users, goals & value
    description: Choose this when you want design decisions anchored to user motivation rather than to the feature list the requirements already assume. It produces an HTML job map of the jobs users hire the product for and the outcomes they expect from each. Use the jobs and outcomes to sanity-check which features earn their place and to prioritise the ones that serve a real job.
    output_path: analyse-requirements/JTBD/jtbd-job-map.html
    reference_asset: framework/assets/analyses/jtbd-reference.md
    template_asset: framework/assets/analyses/template-jtbd.html
    map_skill: framework/skills/map-jtbd-to-ui.md
    analyser_agent: framework/agents/analyses/jtbd-analyser.md
    character: framework/assets/characters/jtbd-analysis.md
  - name: ooux
    status: mvp
    group: Objects, data & lifecycle
    description: Choose this when you need to structure screens and navigation around the product's core objects before laying out any UI. It produces an HTML object map of the core objects, their attributes, and their call-to-action verbs implied by the requirements. Use the objects to drive your information architecture — what gets its own screen, what nests, and what each object's primary actions are.
    output_path: analyse-requirements/OOUX/ooux-object-map.html
    reference_asset: framework/assets/analyses/ooux-reference.md
    template_asset: framework/assets/analyses/template-ooux.html
    map_skill: framework/skills/map-ooux-to-ui.md
    analyser_agent: framework/agents/analyses/ooux-analyser.md
    character: framework/assets/characters/ooux-analysis.md
  - name: sequence-diagram
    status: mvp
    group: Processes & flows
    description: Choose this when a scenario crosses the user, system components, and external services and you need that interaction clear before specifying APIs or async flows. It produces an HTML sequence diagram of the messages exchanged across one scenario, ordered over time. Use it to pin down API calls, request and response ordering, and the failure points async flows must handle.
    output_path: analyse-requirements/SEQUENCE-DIAGRAM/sequence-diagram.html
    reference_asset: framework/assets/analyses/sequence-diagram-reference.md
    template_asset: framework/assets/analyses/template-sequence-diagram.html
    map_skill: framework/skills/map-sequence-diagram-to-ui.md
    analyser_agent: framework/agents/analyses/sequence-diagram-analyser.md
    character: framework/assets/characters/sequence-diagram-analysis.md
  - name: use-cases
    status: mvp
    group: Processes & flows
    description: Choose this when you want explicit usage paths — actor goals, preconditions, and main and extension flows — before designing the screens and APIs that serve them. It produces an HTML use-case map of each actor's goals with the main flow and its extensions and exceptions. Use the flows as the usage paths your screens and endpoints are designed against, and to catch unhandled exception branches.
    output_path: analyse-requirements/USE-CASES/use-cases-map.html
    reference_asset: framework/assets/analyses/use-cases-reference.md
    template_asset: framework/assets/analyses/template-use-cases.html
    map_skill: framework/skills/map-use-cases-to-ui.md
    analyser_agent: framework/agents/analyses/use-cases-analyser.md
    character: framework/assets/characters/use-cases-analysis.md
  - name: user-journeys
    status: mvp
    group: Users, goals & value
    description: Choose this when you want to target the experience moments that matter most rather than spreading design effort evenly across features. It produces an HTML journey map of the experience phases, pain-points, and opportunities the requirements describe. Use the pain-points and opportunities to prioritise the features that relieve the sharpest friction.
    output_path: analyse-requirements/USER-JOURNEYS/user-journeys-map.html
    reference_asset: framework/assets/analyses/user-journeys-reference.md
    template_asset: framework/assets/analyses/template-user-journeys.html
    map_skill: framework/skills/map-user-journeys-to-ui.md
    analyser_agent: framework/agents/analyses/user-journeys-analyser.md
    character: framework/assets/characters/user-journeys-analysis.md
  - name: opportunity-solution-trees
    status: mvp
    group: Users, goals & value
    description: Choose this when you want to check that the requirements' features actually ladder up to its stated outcomes and surface opportunities it missed. It produces an HTML opportunity-solution tree linking the desired outcome to opportunities, the proposed solutions, and their assumption tests. Use it to cut features that serve no outcome, flag outcomes with no solution, and queue the assumption tests worth running.
    output_path: analyse-requirements/OPPORTUNITY-SOLUTION-TREES/opportunity-solution-tree.html
    reference_asset: framework/assets/analyses/opportunity-solution-trees-reference.md
    template_asset: framework/assets/analyses/template-opportunity-solution-trees.html
    map_skill: framework/skills/map-opportunity-solution-trees-to-ui.md
    analyser_agent: framework/agents/analyses/opportunity-solution-trees-analyser.md
    character: framework/assets/characters/opportunity-solution-trees-analysis.md
  - name: mvp-slicing
    status: mvp
    group: Users, goals & value
    description: Choose this when the requirements carry priorities but no one has drawn the line between what ships first and what waits. It produces an HTML user-story map — a §5 task-flow backbone with F-NN, UI-NN, and §4.2 story cards beneath each activity and a release-slice line proposed from the GR-24 Must set — paired with a MoSCoW board of the §6.1, §6.4, and §4.2 priorities. Use the proposed slice to confirm the MVP scope before wireframing, and the MoSCoW board to see at a glance what each priority bucket holds.
    output_path: analyse-requirements/MVP-SLICING/mvp-slicing.html
    reference_asset: framework/assets/analyses/mvp-slicing-reference.md
    template_asset: framework/assets/analyses/template-mvp-slicing.html
    map_skill: framework/skills/map-mvp-slicing-to-ui.md
    analyser_agent: framework/agents/analyses/mvp-slicing-analyser.md
    character: framework/assets/characters/mvp-slicing-analysis.md
  - name: five-whys
    status: mvp
    group: Users, goals & value
    description: Choose this when you suspect some requirements rest on thin justification and want each one's rationale traced before designing against it. It produces an HTML report — a pre-rendered inline-SVG why-chain diagram per requirement above the textual drill-down — drilling each requirement down to the user goal, business driver, or external mandate behind it. Use the thin-justification chains it flags as an interview list for the consultant before those features are built.
    output_path: analyse-requirements/FIVE-WHYS/five-whys.html
    reference_asset: framework/assets/analyses/five-whys-reference.md
    template_asset: framework/assets/analyses/template-five-whys.html
    map_skill: framework/skills/map-five-whys-to-ui.md
    analyser_agent: framework/agents/analyses/five-whys-analyser.md
    character: framework/assets/characters/five-whys-analysis.md
  - name: glossary
    status: mvp
    group: Objects, data & lifecycle
    description: Choose this before writing copy, labels, status pills, or role surfaces, when terms in the requirements need one agreed meaning. It produces an alphabetical, citation-bound HTML glossary of every domain term the requirements use, with an embedded machine-readable term model. Use it as the single source for UI wording and to catch terms used inconsistently across the document.
    output_path: analyse-requirements/GLOSSARY/glossary.html
    reference_asset: framework/assets/analyses/glossary-reference.md
    template_asset: framework/assets/analyses/template-glossary.html
    map_skill: framework/skills/map-glossary-to-ui.md
    analyser_agent: framework/agents/analyses/glossary-analyser.md
    character: framework/assets/characters/glossary-analysis.md
  - name: activity-diagram
    status: mvp
    group: Processes & flows
    description: Choose this when a multi-actor process with branching or parallel paths needs to be clear before designing the screens that drive it. It produces an HTML activity diagram of the process flow, including decision branches and concurrent paths. Use it to design each step's screen and to make sure no branch or parallel path is left without UI.
    output_path: analyse-requirements/ACTIVITY-DIAGRAM/activity-diagram.html
    reference_asset: framework/assets/analyses/activity-diagram-reference.md
    template_asset: framework/assets/analyses/template-activity-diagram.html
    map_skill: framework/skills/map-activity-diagram-to-ui.md
    analyser_agent: framework/agents/analyses/activity-diagram-analyser.md
    character: framework/assets/characters/activity-diagram-analysis.md
  - name: state-diagram
    status: mvp
    group: Objects, data & lifecycle
    description: Choose this when entities move through statuses and you need their lifecycle explicit before designing status-driven UI. It produces an HTML state diagram of each entity's statuses, the transitions between them, and the guards on each transition. Use it to drive status pills, enabled and disabled actions, and the transition rules your screens must enforce.
    output_path: analyse-requirements/STATE-DIAGRAM/state-diagram.html
    reference_asset: framework/assets/analyses/state-diagram-reference.md
    template_asset: framework/assets/analyses/template-state-diagram.html
    map_skill: framework/skills/map-state-diagram-to-ui.md
    analyser_agent: framework/agents/analyses/state-diagram-analyser.md
    character: framework/assets/characters/state-diagram-analysis.md
  - name: crud-coverage
    status: mvp
    group: Objects, data & lifecycle
    description: Choose this when your domain is entity-and-operation heavy and you want a mechanical check that every entity has a create, read, update, and delete path before wireframing. It produces an HTML coverage matrix crossing each entity against the four lifecycle operations, marking each cell delivered, granted-not-delivered, forgotten, or intentional, plus a lifecycle-hole register and an optional role view with Segregation-of-Duties flags. Use the filled cells as a screen-and-action checklist against the blueprint and chase the flagged holes — especially rights §6.5 grants that no function delivers — before building.
    output_path: analyse-requirements/CRUD-COVERAGE/crud-matrix.html
    reference_asset: framework/assets/analyses/crud-coverage-reference.md
    template_asset: framework/assets/analyses/template-crud-coverage.html
    map_skill: framework/skills/map-crud-coverage-to-ui.md
    analyser_agent: framework/agents/analyses/crud-coverage-analyser.md
    character: framework/assets/characters/crud-coverage-analysis.md
  - name: decision-tables
    status: mvp
    group: Objects, data & lifecycle
    description: Choose this when your requirements are dense with conditional logic — validation, conditional fields, eligibility, status-and-role-driven enable/disable — and you want it pulled into structured rule tables and checked for gaps before building. It produces an HTML set of DMN decision tables (condition columns to a conclusion, with a hit policy per table), a completeness check flagging unhandled condition combinations, and a consistency check flagging conflicting rules, with the rule model embedded for re-ingestion. Use the tables as the form-validation, conditional-visibility, and action-enablement spec your screens enforce, chase the flagged gaps and conflicts before wireframing, and re-drop the HTML into input/ so /requirements turns each blocking gap into a question.
    output_path: analyse-requirements/DECISION-TABLES/decision-tables.html
    reference_asset: framework/assets/analyses/decision-tables-reference.md
    template_asset: framework/assets/analyses/template-decision-tables.html
    map_skill: framework/skills/map-decision-tables-to-ui.md
    analyser_agent: framework/agents/analyses/decision-tables-analyser.md
    character: framework/assets/characters/decision-tables-analysis.md
  - name: task-flows
    status: mvp
    group: Processes & flows
    description: Choose this when you need the step-by-step paths a user takes to reach a goal before designing screens, wizards, or form sequences. It produces an HTML task-flow map decomposing each goal into its ordered steps and decision points. Use the flows to decide screen sequencing, wizard splits, and where a single form should branch.
    output_path: analyse-requirements/TASK-FLOWS/task-flows.html
    reference_asset: framework/assets/analyses/task-flows-reference.md
    template_asset: framework/assets/analyses/template-task-flows.html
    map_skill: framework/skills/map-task-flows-to-ui.md
    analyser_agent: framework/agents/analyses/task-flows-analyser.md
    character: framework/assets/characters/task-flows-analysis.md
  - name: trade-off-dimension-analysis
    status: mvp
    group: Design posture
    description: Choose this when you want a clear design posture per user goal — fast versus accurate, simple versus powerful, automated versus controlled — before wireframing. It produces an HTML matrix scoring each user goal against a curated set of UX trade-off dimensions. Use each goal's scores to set the design stance for its screens and to brief divergent wireframe variants.
    output_path: analyse-requirements/TRADE-OFF-DIMENSIONS/trade-off-matrix.html
    reference_asset: framework/assets/analyses/trade-off-dimension-reference.md
    template_asset: framework/assets/analyses/template-trade-off-dimension.html
    map_skill: framework/skills/map-trade-off-dimension-to-ui.md
    analyser_agent: framework/agents/analyses/trade-off-dimension-analyser.md
    character: framework/assets/characters/trade-off-dimension-analysis.md
---

# analyses/registry.md

**Purpose:** Methodology registry for `/analyse-requirement`. The frontmatter above is the **machine-readable** contract — `framework/skills/analysis-selector.md` filters `status == "mvp"` to present options to the consultant; `framework/orchestrators/analyse-requirement-orch.md` looks up `analyser_agent` for the chosen methodology and invokes it; downstream design-spec consumers (when they exist) look up `output_path` and `map_skill` per file produced.

**Used by:**

- `framework/skills/analysis-selector.md` — reads MVP-status rows; presents them as a printed numbered list clustered by `group`, with `★ suggested next` / `✓ already run` marks derived from each row's `output_path` presence on disk.
- `framework/skills/select-supporting-analyses.md` — reads MVP-status rows; filters to completed-on-disk subset for the `/wireframe` Stage-1b numbered list; derives each selection's `sidecar_path` from the row's `output_path` directory plus the canonical convention.
- `framework/orchestrators/analyse-requirement-orch.md` — reads the chosen row's `analyser_agent` and `output_path` to drive invocation and the prior-artefact gate.
- `framework/agents/analyses/<method>-analyser.md` — each analyser reads its own `reference_asset`, `character`, and `template_asset` paths at activation, and writes both the prose artefact at `output_path` AND the structured JSON sidecar at `<dirname(output_path)>/<name>.sidecar.json` per `framework/assets/analyses/sidecar-schema.md`.
- `framework/agents/blueprint-architect.md` — at step 2.6 reads the structured sidecar instead of the prose `output_path` when the sidecar is present (the prose stays consultant-readable on disk; the sidecar is what feeds the architect's downstream steps without context bloat). See `framework/assets/analyses/sidecar-schema.md` for the canonical shape.

**Sidecar projection (downstream context-cost optimisation).** Every MVP analyser is expected to emit a structured JSON sidecar alongside its prose artefact, conforming to the canonical schema at `framework/assets/analyses/sidecar-schema.md`. The sidecar carries `architect_projection` keyed by the closed-enum `architect_roles` defined in `framework/skills/select-supporting-analyses.md > Static method → architect_roles mapping`. Downstream consumers (today: `framework/agents/blueprint-architect.md`) read the small (≤ 20 KB) sidecar in place of the large prose artefact (which can exceed 100 KB), avoiding context bloat. **Sidecar emission is being rolled out one methodology per PR**; analysers that have not yet been updated trip the legacy-fallback path documented in `framework/shared/refusal-registry.md > RF-09`, capped at 60 KB on-disk prose size.

**Adding a new methodology:**

1. Pick a candidate from `plans/` (see `plans/README.md` for the roadmap) and follow its build checklist — its "Turning this into a plan" section mirrors these steps — or author a brand-new methodology not yet in `plans/`.
2. Append the row to the frontmatter with `status: mvp` and populate the fields: `name`, `status`, `description`, `output_path`, `reference_asset`, `template_asset` (may be `null`), `map_skill`, `analyser_agent`, `character`, and the optional `group` (assign a lens group; omitting it drops the row into a trailing `Other` group). Place the row at its best-practice position within its group so the selector's `★ suggested next` flag stays sensible.
3. Author the analyser agent, the reference asset, the character file, and (if needed) the template asset.
4. Implement sidecar emission in the analyser per `framework/assets/analyses/sidecar-schema.md` — write the structured JSON to `<dirname(output_path)>/<name>.sidecar.json`, populating only the `architect_projection[<role>]` entries for roles the method actually exposes per the `select-supporting-analyses.md` static mapping. Verify the write via `framework/skills/verify-artifact-write.md`. Skipping this step is permitted only as a temporary migration measure — the analyser will trigger the `RF-09` legacy-fallback path on selection in `/wireframe`.
5. Append a row to the static `architect_roles` mapping in `framework/skills/select-supporting-analyses.md > Static method → architect_roles mapping`.
6. No orchestrator changes required — the selector skill picks the new row up automatically.

**Field semantics:**

- `name` — kebab-case slug. Used as the subdirectory name under `analyse-requirements/` and as the path component in the analyser agent file.
- `status` — currently always `mvp`. The selector filters to `status == mvp` defensively (discarding any row whose status is absent or non-`mvp`); planned, not-yet-built methodologies live in `plans/`, not as registry rows.
- `group` — optional lens-group label (e.g. `Objects, data & lifecycle`, `Processes & flows`). The selector clusters MVP rows by this value (groups in first-appearance order, registry order preserved within each group) and renders it as a header. Rows with no `group` fall into a trailing `Other` group. Consultant-facing — keep it short and human-readable.
- `description` — short consultant-facing blurb surfaced in the selector's printed list, written as three succinct sentences (why/when to choose it → what it produces → how to use the output).
- `output_path` — relative path of the artefact the analyser writes. Drives the prior-artefact gate in the orchestrator.
- `reference_asset` — the methodology reference the analyser follows.
- `template_asset` — file scaffold the analyser populates (may be `null` for methodologies that emit pure Markdown).
- `map_skill` — translates the analysis output into UI inventory entries for downstream design consumption. Stub for OOUX; not invoked by `/analyse-requirement`.
- `analyser_agent` — the foreground agent invoked by the orchestrator.
- `character` — stance the Unicorn adopts while running the analyser.
