---
role: asset
kind: registry
methodologies:
  # MVP — fully implemented in Phase 2; listed alphabetically; none privileged.
  - name: jtbd
    status: mvp
    description: Jobs-to-be-Done — situation / motivation / expected outcome
    output_path: artifacts/requirements/analyses/jtbd.md
    reference_asset: assets/analyses/jtbd-reference.md
    template_asset: null
    map_skill: skills/map-jtbd-to-ui.md
    analyser_agent: agents/analyses/jtbd-analyser/agent.md
    character: assets/characters/jtbd-analysis.md
  - name: ooux
    status: mvp
    description: Object-oriented UX analysis (ORCA process — objects / relationships / CTAs / attributes / CCPs)
    output_path: artifacts/requirements/analyses/ooux.html
    reference_asset: assets/analyses/ooux-reference.md
    template_asset: assets/analyses/template-ooux.html
    map_skill: skills/map-ooux-to-ui.md
    analyser_agent: agents/analyses/ooux-analyser/agent.md
    character: assets/characters/ooux-analysis.md
  - name: user-journeys
    status: mvp
    description: Per-persona temporal flow maps with stages / touchpoints / actions / thoughts / emotions / pain-points / opportunities
    output_path: artifacts/requirements/analyses/user-journeys.md
    reference_asset: assets/analyses/user-journeys-reference.md
    template_asset: null
    map_skill: skills/map-user-journeys-to-ui.md
    analyser_agent: agents/analyses/user-journeys-analyser/agent.md
    character: assets/characters/user-journeys-analysis.md
  - name: user-stories
    status: mvp
    description: As-a / I want / so that with Given/When/Then acceptance criteria
    output_path: artifacts/requirements/analyses/user-stories.md
    reference_asset: assets/analyses/user-stories-reference.md
    template_asset: null
    map_skill: skills/map-user-stories-to-ui.md
    analyser_agent: agents/analyses/user-stories-analyser/agent.md
    character: assets/characters/user-stories-analysis.md
  # Future — stub-only; no reference asset, no analyser agent.
  - { name: use-cases, status: future }
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

<!-- ROLE: asset. STATUS: stub — author during phase-2 build-order step 8. -->

# analyses/registry.md

**Purpose:** Methodology registry. The frontmatter above is the **machine-readable** contract — `analysis-selector` filters `status == "mvp"` to present options to the consultant; `design-spec-drafter` looks up `output_path` and `map_skill` per file in `artifacts/requirements/analyses/`; `persona-llm.md` loads `reference_asset` for every MVP-status row that exists on disk.

**Used by:**
- `framework/skills/analysis-selector.md` — reads MVP-status rows; presents to consultant.
- `framework/agents/design-spec-drafter/agent.md` — iterates `artifacts/requirements/analyses/` and maps each file by name → registry row → map skill.
- `framework/assets/persona-llm.md` — loads MVP reference assets at activation (if registered + present on disk).
- `framework/skills/recommend-next-option.md` — when offering `/analyse` as a side action, recommends among registered MVP methodologies.

**Used how:** Adding a new methodology = append a frontmatter row + author analyser agent + reference asset + (optionally) template asset + `map-*-to-ui` skill + character file. **No orchestrator changes.** Promoting a future row to MVP = flip `status` and add the missing fields.

> Body narrative TBD; the frontmatter is the source of truth.
