---
role: asset
kind: registry
methodologies:
  # MVP — fully implemented and selectable via /analyse-requirement. Listed alphabetically; none privileged.
  - name: data-model
    status: mvp
    description: Surfaces the entities, attributes, and relationships implied by the requirements so forms, lists, and detail views can be designed against an explicit schema.
    output_path: analyse-requirements/DATA-MODEL/data-model.html
    reference_asset: framework/assets/analyses/data-model-reference.md
    template_asset: framework/assets/analyses/template-data-model.html
    map_skill: framework/skills/map-data-model-to-ui.md
    analyser_agent: framework/agents/analyses/data-model-analyser.md
    character: framework/assets/characters/data-model-analysis.md
  - name: jtbd
    status: mvp
    description: Surfaces the jobs and outcomes users hire the product for so design decisions anchor to user motivation rather than features.
    output_path: analyse-requirements/JTBD/jtbd-job-map.html
    reference_asset: framework/assets/analyses/jtbd-reference.md
    template_asset: framework/assets/analyses/template-jtbd.html
    map_skill: framework/skills/map-jtbd-to-ui.md
    analyser_agent: framework/agents/analyses/jtbd-analyser.md
    character: framework/assets/characters/jtbd-analysis.md
  - name: ooux
    status: mvp
    description: Identifies the core objects, attributes, and CTAs implied by the requirements so screens and navigation can be structured around them.
    output_path: analyse-requirements/OOUX/ooux-object-map.html
    reference_asset: framework/assets/analyses/ooux-reference.md
    template_asset: framework/assets/analyses/template-ooux.html
    map_skill: framework/skills/map-ooux-to-ui.md
    analyser_agent: framework/agents/analyses/ooux-analyser.md
    character: framework/assets/characters/ooux-analysis.md
  - name: sequence-diagram
    status: mvp
    description: Clarifies how the user, system components, and external services interact across a scenario before APIs and async flows are specified.
    output_path: analyse-requirements/SEQUENCE-DIAGRAM/sequence-diagram.html
    reference_asset: framework/assets/analyses/sequence-diagram-reference.md
    template_asset: framework/assets/analyses/template-sequence-diagram.html
    map_skill: framework/skills/map-sequence-diagram-to-ui.md
    analyser_agent: framework/agents/analyses/sequence-diagram-analyser.md
    character: framework/assets/characters/sequence-diagram-analysis.md
  - name: use-cases
    status: mvp
    description: Surfaces actor goals, preconditions, and main/extension flows implied by the requirements so screens and APIs are designed against explicit usage paths.
    output_path: analyse-requirements/USE-CASES/use-cases-map.html
    reference_asset: framework/assets/analyses/use-cases-reference.md
    template_asset: framework/assets/analyses/template-use-cases.html
    map_skill: framework/skills/map-use-cases-to-ui.md
    analyser_agent: framework/agents/analyses/use-cases-analyser.md
    character: framework/assets/characters/use-cases-analysis.md
  - name: user-journeys
    status: mvp
    description: Maps the experience phases, pain-points, and opportunities the requirements describe so feature prioritisation targets the moments that matter most.
    output_path: analyse-requirements/USER-JOURNEYS/user-journeys-map.html
    reference_asset: framework/assets/analyses/user-journeys-reference.md
    template_asset: framework/assets/analyses/template-user-journeys.html
    map_skill: framework/skills/map-user-journeys-to-ui.md
    analyser_agent: framework/agents/analyses/user-journeys-analyser.md
    character: framework/assets/characters/user-journeys-analysis.md
  # Future — stub-only; no analyser agent on disk. Promote by flipping status, populating
  # the remaining fields, and authoring the analyser + reference + character + template.
  - { name: user-stories, status: future }
  - { name: quality-signals-analysis, status: future }
  - { name: personas, status: future }
  - { name: thematic-analysis, status: future }
  - name: opportunity-solution-trees
    status: mvp
    description: Audits whether the document's features ladder up to its stated outcomes and surfaces unaddressed opportunities or missing assumption tests.
    output_path: analyse-requirements/OPPORTUNITY-SOLUTION-TREES/opportunity-solution-tree.html
    reference_asset: framework/assets/analyses/opportunity-solution-trees-reference.md
    template_asset: framework/assets/analyses/template-opportunity-solution-trees.html
    map_skill: framework/skills/map-opportunity-solution-trees-to-ui.md
    analyser_agent: framework/agents/analyses/opportunity-solution-trees-analyser.md
    character: framework/assets/characters/opportunity-solution-trees-analysis.md
  - { name: storytelling-narrative-synthesis, status: future }
  - name: five-whys
    status: mvp
    description: Drills each requirement's rationale down to a user goal, business driver, or external mandate so thin-justification chains can be flagged for consultant interview before features are designed against them.
    output_path: analyse-requirements/FIVE-WHYS/five-whys.md
    reference_asset: framework/assets/analyses/five-whys-reference.md
    template_asset: null
    map_skill: framework/skills/map-five-whys-to-ui.md
    analyser_agent: framework/agents/analyses/five-whys-analyser.md
    character: framework/assets/characters/five-whys-analysis.md
  - name: glossary
    status: mvp
    description: Produces an alphabetical, citation-bound vocabulary inventory before copy, labels, status pills, or role surfaces are designed.
    output_path: analyse-requirements/GLOSSARY/glossary.md
    reference_asset: framework/assets/analyses/glossary-reference.md
    template_asset: null
    map_skill: framework/skills/map-glossary-to-ui.md
    analyser_agent: framework/agents/analyses/glossary-analyser.md
    character: framework/assets/characters/glossary-analysis.md
  - { name: double-diamond, status: future }
  - { name: card-sorting, status: future }
  - { name: highest-value-paths, status: future }
  - { name: storyboarding, status: future }
  - { name: scenarios, status: future }
  - name: activity-diagram
    status: mvp
    description: Clarifies multi-actor process flow, branching, and parallel paths in the requirements before the screens that drive them are designed.
    output_path: analyse-requirements/ACTIVITY-DIAGRAM/activity-diagram.html
    reference_asset: framework/assets/analyses/activity-diagram-reference.md
    template_asset: framework/assets/analyses/template-activity-diagram.html
    map_skill: framework/skills/map-activity-diagram-to-ui.md
    analyser_agent: framework/agents/analyses/activity-diagram-analyser.md
    character: framework/assets/characters/activity-diagram-analysis.md
  - name: state-diagram
    status: mvp
    description: Surfaces entity lifecycles — statuses, transitions, and guards — implicit in the requirements before status-driven UI is designed.
    output_path: analyse-requirements/STATE-DIAGRAM/state-diagram.html
    reference_asset: framework/assets/analyses/state-diagram-reference.md
    template_asset: framework/assets/analyses/template-state-diagram.html
    map_skill: framework/skills/map-state-diagram-to-ui.md
    analyser_agent: framework/agents/analyses/state-diagram-analyser.md
    character: framework/assets/characters/state-diagram-analysis.md
  - { name: decision-matrix, status: future }
  - name: task-flows
    status: mvp
    description: Surfaces the goal-decomposition structure and step-by-step user paths implicit in the requirements before screens, wizards, or form sequences are designed.
    output_path: analyse-requirements/TASK-FLOWS/task-flows.html
    reference_asset: framework/assets/analyses/task-flows-reference.md
    template_asset: framework/assets/analyses/template-task-flows.html
    map_skill: framework/skills/map-task-flows-to-ui.md
    analyser_agent: framework/agents/analyses/task-flows-analyser.md
    character: framework/assets/characters/task-flows-analysis.md
  - name: trade-off-dimension-analysis
    status: mvp
    description: Scores each user goal against a curated set of UX trade-off dimensions (Speed vs Accuracy, Simplicity vs Power, Automation vs Control, ...) to guide wireframing posture per goal.
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

- `framework/skills/analysis-selector.md` — reads MVP-status rows; presents them via `AskUserQuestion`.
- `framework/skills/select-supporting-analyses.md` — reads MVP-status rows; filters to completed-on-disk subset for the `/wireframe` Stage-1b numbered list; derives each selection's `sidecar_path` from the row's `output_path` directory plus the canonical convention.
- `framework/orchestrators/analyse-requirement-orch.md` — reads the chosen row's `analyser_agent` and `output_path` to drive invocation and the prior-artefact gate.
- `framework/agents/analyses/<method>-analyser.md` — each analyser reads its own `reference_asset`, `character`, and `template_asset` paths at activation, and writes both the prose artefact at `output_path` AND the structured JSON sidecar at `<dirname(output_path)>/<name>.sidecar.json` per `framework/assets/analyses/sidecar-schema.md`.
- `framework/agents/blueprint-architect.md` — at step 2.6 reads the structured sidecar instead of the prose `output_path` when the sidecar is present (the prose stays consultant-readable on disk; the sidecar is what feeds the architect's downstream steps without context bloat). See `framework/assets/analyses/sidecar-schema.md` for the canonical shape.

**Sidecar projection (downstream context-cost optimisation).** Every MVP analyser is expected to emit a structured JSON sidecar alongside its prose artefact, conforming to the canonical schema at `framework/assets/analyses/sidecar-schema.md`. The sidecar carries `architect_projection` keyed by the closed-enum `architect_roles` defined in `framework/skills/select-supporting-analyses.md > Static method → architect_roles mapping`. Downstream consumers (today: `framework/agents/blueprint-architect.md`) read the small (≤ 20 KB) sidecar in place of the large prose artefact (which can exceed 100 KB), avoiding context bloat. **Sidecar emission is being rolled out one methodology per PR** following the migration plan documented in the plan file at `C:\Users\roden\.claude\plans\when-the-user-selects-unified-honey.md`; analysers that have not yet been updated trip the legacy-fallback path documented in `framework/shared/refusal-registry.md > RF-09`, capped at 60 KB on-disk prose size.

**Adding a new methodology:**

1. Append a row to the frontmatter (or flip an existing `future` row to `mvp`).
2. Populate all eight fields: `name`, `status`, `description`, `output_path`, `reference_asset`, `template_asset` (may be `null`), `map_skill`, `analyser_agent`, `character`.
3. Author the analyser agent, the reference asset, the character file, and (if needed) the template asset.
4. Implement sidecar emission in the analyser per `framework/assets/analyses/sidecar-schema.md` — write the structured JSON to `<dirname(output_path)>/<name>.sidecar.json`, populating only the `architect_projection[<role>]` entries for roles the method actually exposes per the `select-supporting-analyses.md` static mapping. Verify the write via `framework/skills/verify-artifact-write.md`. Skipping this step is permitted only as a temporary migration measure — the analyser will trigger the `RF-09` legacy-fallback path on selection in `/wireframe`.
5. Append a row to the static `architect_roles` mapping in `framework/skills/select-supporting-analyses.md > Static method → architect_roles mapping`.
6. No orchestrator changes required — the selector skill picks the new row up automatically.

**Field semantics:**

- `name` — kebab-case slug. Used as the subdirectory name under `analyse-requirements/` and as the path component in the analyser agent file.
- `status` — `mvp` (selectable now) or `future` (not yet built).
- `description` — one-line label surfaced in the `AskUserQuestion` choice list.
- `output_path` — relative path of the artefact the analyser writes. Drives the prior-artefact gate in the orchestrator.
- `reference_asset` — the methodology reference the analyser follows.
- `template_asset` — file scaffold the analyser populates (may be `null` for methodologies that emit pure Markdown).
- `map_skill` — translates the analysis output into UI inventory entries for downstream design consumption. Stub for OOUX; not invoked by `/analyse-requirement`.
- `analyser_agent` — the foreground agent invoked by the orchestrator.
- `character` — stance the Unicorn adopts while running the analyser.
