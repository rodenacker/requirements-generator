---
role: asset
kind: registry
methodologies:
  # MVP — fully implemented and selectable via /analyse. Listed alphabetically; none privileged.
  - name: data-model
    status: mvp
    description: Logical Data Model (entities × attributes × relationships × cardinalities × business rules × normalisation notes) plus consultant-selected ERD views — none/one/several/all of Crow's Foot, Chen, UML. Data Model always rendered; ERD views optional.
    output_path: analyses/DATA-MODEL/data-model.html
    reference_asset: framework/assets/analyses/data-model-reference.md
    template_asset: framework/assets/analyses/template-data-model.html
    map_skill: framework/skills/map-data-model-to-ui.md
    analyser_agent: framework/agents/analyses/data-model-analyser.md
    character: framework/assets/characters/data-model-analysis.md
  - name: jtbd
    status: mvp
    description: Jobs-to-be-Done analysis (situations × jobs × outcomes; hybrid Christensen-Moesta + Ulwick)
    output_path: analyses/JTBD/jtbd-job-map.html
    reference_asset: framework/assets/analyses/jtbd-reference.md
    template_asset: framework/assets/analyses/template-jtbd.html
    map_skill: framework/skills/map-jtbd-to-ui.md
    analyser_agent: framework/agents/analyses/jtbd-analyser.md
    character: framework/assets/characters/jtbd-analysis.md
  - name: ooux
    status: mvp
    description: Object-oriented UX analysis (ORCA process — objects / relationships / CTAs / attributes / CCPs)
    output_path: analyses/OOUX/ooux-object-map.html
    reference_asset: framework/assets/analyses/ooux-reference.md
    template_asset: framework/assets/analyses/template-ooux.html
    map_skill: framework/skills/map-ooux-to-ui.md
    analyser_agent: framework/agents/analyses/ooux-analyser.md
    character: framework/assets/characters/ooux-analysis.md
  - name: use-cases
    status: mvp
    description: Use Cases analysis (Cockburn fully-dressed — actors × goals × preconditions × main flows × extensions)
    output_path: analyses/USE-CASES/use-cases-map.html
    reference_asset: framework/assets/analyses/use-cases-reference.md
    template_asset: framework/assets/analyses/template-use-cases.html
    map_skill: framework/skills/map-use-cases-to-ui.md
    analyser_agent: framework/agents/analyses/use-cases-analyser.md
    character: framework/assets/characters/use-cases-analysis.md
  - name: user-journeys
    status: mvp
    description: User-journeys analysis (NN/G canonical — persona × scenario × phases × {actions, thoughts, emotions, touchpoints, pain-points, opportunities}; tabular swimlane + inline-SVG emotion curve)
    output_path: analyses/USER-JOURNEYS/user-journeys-map.html
    reference_asset: framework/assets/analyses/user-journeys-reference.md
    template_asset: framework/assets/analyses/template-user-journeys.html
    map_skill: framework/skills/map-user-journeys-to-ui.md
    analyser_agent: framework/agents/analyses/user-journeys-analyser.md
    character: framework/assets/characters/user-journeys-analysis.md
  # Future — stub-only; no analyser agent on disk. Promote by flipping status, populating
  # the remaining fields, and authoring the analyser + reference + character + template.
  - { name: user-stories, status: future }
  - { name: quality-signals-analysis, status: future }
  - { name: glossary-domain, status: future }
  - { name: personas, status: future }
  - { name: thematic-analysis, status: future }
  - { name: opportunity-solution-trees, status: future }
  - { name: storytelling-narrative-synthesis, status: future }
  - { name: five-whys, status: future }
  - { name: double-diamond, status: future }
  - { name: card-sorting, status: future }
  - { name: task-analysis, status: future }
  - { name: highest-value-paths, status: future }
  - { name: storyboarding, status: future }
  - { name: scenarios, status: future }
  - { name: activity-diagrams, status: future }
  - { name: decision-matrix, status: future }
---

# analyses/registry.md

**Purpose:** Methodology registry for `/analyse`. The frontmatter above is the **machine-readable** contract — `framework/skills/analysis-selector.md` filters `status == "mvp"` to present options to the consultant; `framework/orchestrators/analyse-orch.md` looks up `analyser_agent` for the chosen methodology and invokes it; downstream design-spec consumers (when they exist) look up `output_path` and `map_skill` per file produced.

**Used by:**

- `framework/skills/analysis-selector.md` — reads MVP-status rows; presents them via `AskUserQuestion`.
- `framework/orchestrators/analyse-orch.md` — reads the chosen row's `analyser_agent` and `output_path` to drive invocation and the prior-artefact gate.
- `framework/agents/analyses/<method>-analyser.md` — each analyser reads its own `reference_asset`, `character`, and `template_asset` paths at activation.

**Adding a new methodology:**

1. Append a row to the frontmatter (or flip an existing `future` row to `mvp`).
2. Populate all eight fields: `name`, `status`, `description`, `output_path`, `reference_asset`, `template_asset` (may be `null`), `map_skill`, `analyser_agent`, `character`.
3. Author the analyser agent, the reference asset, the character file, and (if needed) the template asset.
4. No orchestrator changes required — the selector skill picks the new row up automatically.

**Field semantics:**

- `name` — kebab-case slug. Used as the subdirectory name under `analyses/` and as the path component in the analyser agent file.
- `status` — `mvp` (selectable now) or `future` (not yet built).
- `description` — one-line label surfaced in the `AskUserQuestion` choice list.
- `output_path` — relative path of the artefact the analyser writes. Drives the prior-artefact gate in the orchestrator.
- `reference_asset` — the methodology reference the analyser follows.
- `template_asset` — file scaffold the analyser populates (may be `null` for methodologies that emit pure Markdown).
- `map_skill` — translates the analysis output into UI inventory entries for downstream design consumption. Stub for OOUX; not invoked by `/analyse`.
- `analyser_agent` — the foreground agent invoked by the orchestrator.
- `character` — stance the Unicorn adopts while running the analyser.
