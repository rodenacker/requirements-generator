<!-- ROLE: asset. STATUS: stub — author during phase-1 build-order step 1. -->

# taxonomy-screens.md

**Purpose:** Canonical hierarchy of UI element kinds — `screen` (required, ≥1) / `view` / `organism` / `molecule` / `atom` — plus modifiers (`modal` / `drawer` / `tab` / `list`), reusability rules, containment rules, per-kind trade-off resolution, and dropped-term vocabulary discipline (no "page", "widget", "component" without qualification).

**Used by:**
- `framework/agents/design-spec-drafter/agent.md` — assigns `taxonomy_kind` and `taxonomy_modifier` to every UI inventory row.
- `framework/skills/derive-ui-inventory.md` — uses the hierarchy to scaffold rows.
- `framework/skills/map-ooux-to-ui.md` — objects → screen-taxonomy elements.
- `framework/assets/topics-design.md`, `framework/assets/template-design-spec.md` — section + table references.

**How used:** The vocabulary used everywhere in the design spec. Every UI inventory row names exactly one `taxonomy_kind`. Adding a new kind requires updating containment + trade-off resolution tables here.

> Content TBD per `plan/v7b-Brief.md > §Screen taxonomy` (definitive content).
