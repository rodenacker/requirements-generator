---
role: asset
kind: registry
methodologies:
  # MVP — fully implemented and selectable via /analyse. Listed alphabetically; none privileged.
  - name: data-model
    status: mvp
    description: Logical Data Model (entities × attributes × relationships × cardinalities × business rules × normalisation notes) plus consultant-selected ERD views — none/one/several/all of Crow's Foot, Chen, UML. Data Model always rendered; ERD views optional. Choose this option to surface the entities, fields, and relationships already in the requirements, before designing forms, lists, or detail views.
    output_path: analyses/DATA-MODEL/data-model.html
    reference_asset: framework/assets/analyses/data-model-reference.md
    template_asset: framework/assets/analyses/template-data-model.html
    map_skill: framework/skills/map-data-model-to-ui.md
    analyser_agent: framework/agents/analyses/data-model-analyser.md
    character: framework/assets/characters/data-model-analysis.md
  - name: jtbd
    status: mvp
    description: Jobs-to-be-Done analysis (situations × jobs × outcomes; hybrid Christensen-Moesta + Ulwick). Choose this option to surface the jobs and outcomes users hire the product for, so design decisions can anchor to them.
    output_path: analyses/JTBD/jtbd-job-map.html
    reference_asset: framework/assets/analyses/jtbd-reference.md
    template_asset: framework/assets/analyses/template-jtbd.html
    map_skill: framework/skills/map-jtbd-to-ui.md
    analyser_agent: framework/agents/analyses/jtbd-analyser.md
    character: framework/assets/characters/jtbd-analysis.md
  - name: ooux
    status: mvp
    description: Object-oriented UX analysis (ORCA process — objects / relationships / CTAs / attributes / CCPs). Choose this option to identify the core objects, attributes, and CTAs implied by the requirements, before structuring screens and navigation.
    output_path: analyses/OOUX/ooux-object-map.html
    reference_asset: framework/assets/analyses/ooux-reference.md
    template_asset: framework/assets/analyses/template-ooux.html
    map_skill: framework/skills/map-ooux-to-ui.md
    analyser_agent: framework/agents/analyses/ooux-analyser.md
    character: framework/assets/characters/ooux-analysis.md
  - name: sequence-diagram
    status: mvp
    description: UML 2.5 Sequence Diagrams — per-scenario interaction views at system-level fidelity (persona × system components × external systems), with sync/async/return messages and alt/opt/loop fragments. Consultant selects which scenarios to render; tabular catalogues always emitted, inline-SVG diagrams per selected scenario. Choose this option to clarify how the user, system components, and external services interact across a scenario, before specifying APIs or async flows.
    output_path: analyses/SEQUENCE-DIAGRAM/sequence-diagram.html
    reference_asset: framework/assets/analyses/sequence-diagram-reference.md
    template_asset: framework/assets/analyses/template-sequence-diagram.html
    map_skill: framework/skills/map-sequence-diagram-to-ui.md
    analyser_agent: framework/agents/analyses/sequence-diagram-analyser.md
    character: framework/assets/characters/sequence-diagram-analysis.md
  - name: use-cases
    status: mvp
    description: Use Cases analysis (Cockburn fully-dressed — actors × goals × preconditions × main flows × extensions). Choose this option to surface the actor goals, preconditions, and main/extension flows already implied by the requirements, before designing screens or APIs.
    output_path: analyses/USE-CASES/use-cases-map.html
    reference_asset: framework/assets/analyses/use-cases-reference.md
    template_asset: framework/assets/analyses/template-use-cases.html
    map_skill: framework/skills/map-use-cases-to-ui.md
    analyser_agent: framework/agents/analyses/use-cases-analyser.md
    character: framework/assets/characters/use-cases-analysis.md
  - name: user-journeys
    status: mvp
    description: User-journeys analysis (NN/G canonical — persona × scenario × phases × {actions, thoughts, emotions, touchpoints, pain-points, opportunities}; tabular swimlane + inline-SVG emotion curve). Choose this option to map the experience phases, pain-points, and opportunities the requirements describe, before prioritising features.
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
  - { name: personas, status: future }
  - { name: thematic-analysis, status: future }
  - name: opportunity-solution-trees
    status: mvp
    description: Opportunity Solution Tree (Teresa Torres, *Continuous Discovery Habits*) — a reverse-discovery audit that ladders the requirements document upwards from its features to the customer needs they address and the business/product outcome they serve, plus a best-effort fourth layer of assumption tests where the doc names risks or open questions. Output is a four-band tree (Outcome → Opportunities → Solutions → Assumption Tests) with SVG connectors; orphan solutions, vague opportunities, and unaddressed opportunities are surfaced in diagnostics rather than fabricated. Choose this option to audit whether the document's features actually ladder up to its stated goals, and to surface gaps where opportunities are unaddressed or assumption tests are missing.
    output_path: analyses/OPPORTUNITY-SOLUTION-TREES/opportunity-solution-tree.html
    reference_asset: framework/assets/analyses/opportunity-solution-trees-reference.md
    template_asset: framework/assets/analyses/template-opportunity-solution-trees.html
    map_skill: framework/skills/map-opportunity-solution-trees-to-ui.md
    analyser_agent: framework/agents/analyses/opportunity-solution-trees-analyser.md
    character: framework/assets/characters/opportunity-solution-trees-analysis.md
  - { name: storytelling-narrative-synthesis, status: future }
  - name: five-whys
    status: mvp
    description: Five Whys justification analysis (Toyota Production System root-cause technique, applied to requirement justification) — auto-extract the 5 highest-priority candidate requirements for rationale analysis from §6 (scored by Five-Whys-fitness category match — business goal / operational capability / workflow constraint / policy-driven behaviour — plus §5 task-flow anchors, §4 user-goal anchors, modal strength, and an implementation-detail penalty), allow the consultant to add their own (anchored back to the requirements doc), then drill each selected requirement's why-chain down to the underlying user goal, business driver, or external mandate. Chains terminate at the Justification Sufficiency Test (an axiomatic / immutable driver) or when source material is exhausted (marked INCOMPLETE), never padded. Choose this option to interrogate why each requirement exists before designing features against it — thin-justification chains signal requirements that may need consultant interview. Output: markdown.
    output_path: analyses/FIVE-WHYS/five-whys.md
    reference_asset: framework/assets/analyses/five-whys-reference.md
    template_asset: null
    map_skill: framework/skills/map-five-whys-to-ui.md
    analyser_agent: framework/agents/analyses/five-whys-analyser.md
    character: framework/assets/characters/five-whys-analysis.md
  - name: glossary
    status: mvp
    description: Glossary — surface the project's domain vocabulary from requirements.md. Walks the doc at a consultant-chosen scope tier (1 = nouns + roles + statuses → 2 += acronyms → 3 += action verbs → 4 += field names; each tier strictly extends the prior). Defined-term entries lift the definition verbatim from an explicit-definition pattern (an "is a" clause, a definition-list row, a §2 entity row, a §7 attribute row, or a §3 role entry) with a section-ref citation. Terms used in the document but not defined explicitly are surfaced in a separate "used without explicit definition" section with use-site citations only — no Claude-supplied gloss, no [AI-SUGGESTED] markers. Re-runs are additive: the artefact carries an HTML-comment cursor so the consultant can widen scope tier by tier across runs; prior entries are preserved verbatim unless the consultant explicitly chooses to re-extract on the drift gate. Choose this option to produce an alphabetical, citation-bound vocabulary inventory before designing copy, labels, status pills, or role surfaces. Output: markdown.
    output_path: analyses/GLOSSARY/glossary.md
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
    description: UML 2.5 Activity Diagrams — per-flow process views with horizontal swimlanes (actor + system components + external systems), decision/merge nodes for branching, fork/join for parallelism, initial/final markers. Consultant selects which flows to render; tabular catalogues always emitted, inline-SVG diagrams per selected flow. Choose this option to clarify multi-actor process flow, branching, and parallel paths in the requirements, before designing the screens that drive them.
    output_path: analyses/ACTIVITY-DIAGRAM/activity-diagram.html
    reference_asset: framework/assets/analyses/activity-diagram-reference.md
    template_asset: framework/assets/analyses/template-activity-diagram.html
    map_skill: framework/skills/map-activity-diagram-to-ui.md
    analyser_agent: framework/agents/analyses/activity-diagram-analyser.md
    character: framework/assets/characters/activity-diagram-analysis.md
  - name: state-diagram
    status: mvp
    description: UML 2.5 § 14 State Diagrams — per-entity behaviour state machines, one diagram per aggregate root or status-bearing entity (states × transitions × triggers × guards × effects × entry/exit/do activities). Lean MVP subset: simple/composite states, initial/final/choice/junction pseudostates; orthogonal regions, history pseudostates, submachine states deferred. Consultant selects which entities to render; tabular catalogues always emitted, inline-SVG diagrams plus copy-pasteable Mermaid `stateDiagram-v2` source per selected entity. Choose this option to surface entity lifecycles — statuses, transitions, and guards — implicit in the requirements, before designing status-driven UI.
    output_path: analyses/STATE-DIAGRAM/state-diagram.html
    reference_asset: framework/assets/analyses/state-diagram-reference.md
    template_asset: framework/assets/analyses/template-state-diagram.html
    map_skill: framework/skills/map-state-diagram-to-ui.md
    analyser_agent: framework/agents/analyses/state-diagram-analyser.md
    character: framework/assets/characters/state-diagram-analysis.md
  - { name: decision-matrix, status: future }
  - name: task-flows
    status: mvp
    description: UX Task Analysis & Task Flows — Hierarchical Task Analysis (Annett-Duncan 1967; Stanton 2006) plus per-task Task-Flow Diagrams (NN/G; Hackos & Redish 1998). Single-actor, decomposition-first, user-mental-model fidelity. Per-task catalogue (tasks × subgoals × operations × plans × decisions × exceptions × cross-task operation matrix); consultant selects which tasks to render; each selected task produces an HTA tree (vertical) + a Task-Flow Diagram (horizontal) inline-SVG pair. Choose this option to surface the goal-decomposition structure and step-by-step user paths implicit in the requirements, before designing screens, wizards, or form sequences.
    output_path: analyses/TASK-FLOWS/task-flows.html
    reference_asset: framework/assets/analyses/task-flows-reference.md
    template_asset: framework/assets/analyses/template-task-flows.html
    map_skill: framework/skills/map-task-flows-to-ui.md
    analyser_agent: framework/agents/analyses/task-flows-analyser.md
    character: framework/assets/characters/task-flows-analysis.md
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
