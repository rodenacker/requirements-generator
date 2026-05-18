<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 9. -->

# map-state-diagram-to-ui.md

**Purpose:** Translate a UML 2.5 § 14 state-diagram catalogue (`analyse-requirements/STATE-DIAGRAM/state-diagram.html`) into UI inventory entries: entities → screen-state inventories (each entity's state set defines the discrete screen states an entity-detail screen must support — a `Draft` state shows the editor; an `Active` state shows the read-only view with action affordances); states → conditional UI rendering rules (state value drives which buttons, fields, and panels are visible); transitions with `trigger.kind == user-action` → action affordances (buttons, links, menu items) — one affordance per user-initiated transition, with the transition's `effect` informing success-state UI and the transition's `guard` informing the affordance's enabled/disabled state; transitions with `trigger.kind == time-event` or `change-event` → backend automation hooks, not UI affordances (surfaced as background-process indicators in the design spec); internal activities of kind `entry`/`exit`/`do` → page lifecycle hooks (onMount / onUnmount / polling intervals) for the design system; composite states → screen groupings (an `Approved` composite with substates `Awaiting-funding` / `Funded` / `Active` maps to a single screen with a sub-state indicator strip); guards → form-level validation rules and affordance-level disabled states (a transition `submit` guarded by `[items.size > 0]` means the `Submit` button is disabled when the cart is empty); cross-entity state coverage matrix → cross-entity navigation hints (entities sharing canonical lifecycle phases — multiple things in `active` — suggest a unified status filter / dashboard pattern).

**Inputs:** `analyse-requirements/STATE-DIAGRAM/state-diagram.html`, `assets/taxonomy-screens.md`.

**Outputs:** UI inventory rows for the design spec.

**Used by:** `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when the state-diagram analysis is present. Combines with other `map-*-to-ui` skills (including `map-activity-diagram-to-ui.md` and `map-sequence-diagram-to-ui.md` when those behavioural analyses have been run, and `map-data-model-to-ui.md` for entity-level CRUD surfacing) via the accrue-all pattern. Entity selection in the state-diagram artefact does not affect the mapping — the mapping consumes the Tier-1 catalogue tables (Entities, States, Internal activities, Transitions, Events, Cross-entity state coverage matrix), which are always present.

> Content TBD per `framework/assets/analyses/state-diagram-reference.md > Downstream consumption`.
