<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 4. -->

# derive-ui-inventory.md

**Purpose:** Produce the design-spec UI inventory directly from `requirements.md` when no analyses are present in `artifacts/requirements/analyses/` — the requirements-only fallback. Screens by task flow, CTAs by user goals, structure by entity model.

**Inputs:** `requirements.md`, `assets/taxonomy-screens.md`, `assets/taxonomy-tasks.md`, `assets/topics-design.md`.

**Outputs:** UI inventory rows with `taxonomy_id`, `taxonomy_kind`, `taxonomy_modifier`, `parent_id`, `object_refs`, `role`, `visual_form`, `states`, `behaviours`.

**Used by:** `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when no analyses are present. When analyses exist, the drafter calls the `map-*-to-ui.md` skills instead (or in addition, accruing). Output of this skill is weaker than analysis-backed output but functional.

> Content TBD per `plan/v7b-Brief.md > §Analyses > Downstream consumption` (fallback case).
