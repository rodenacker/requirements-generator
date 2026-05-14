<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 9. -->

# map-activity-diagram-to-ui.md

**Purpose:** Translate a UML 2.5 activity-diagram catalogue (`analyses/ACTIVITY-DIAGRAM/activity-diagram.html`) into UI inventory entries: flows → screen-flow sequences (each `primary` flow becomes an ordered list of screen transitions, one screen per action node group within an actor swimlane); swimlanes → component-ownership hints for the design system (an actor swimlane defines the user-facing surface area; a system-component swimlane defines a backend integration point; an external-system swimlane defines a third-party integration boundary); decision nodes → branching UI affordances (conditional sections, gated CTAs, decision modals — one branch per outgoing guard); merge nodes → re-convergence points where divergent UI states funnel back to a shared screen; fork nodes → parallel UI patterns (split panes, concurrent progress bars, batch dashboards); join nodes → synchronisation UI affordances (wait-for-all indicators, "all approvals received" gates); cross-flow swimlane matrix → component-reuse hints (a swimlane present in 5+ flows warrants a first-class shared component in the design system).

**Inputs:** `analyses/ACTIVITY-DIAGRAM/activity-diagram.html`, `assets/taxonomy-screens.md`.

**Outputs:** UI inventory rows for the design spec.

**Used by:** `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when the activity-diagram analysis is present. Combines with other `map-*-to-ui` skills (including `map-sequence-diagram-to-ui.md` when both behavioural analyses have been run) via the accrue-all pattern. Flow selection in the activity-diagram artefact does not affect the mapping — the mapping consumes the Tier-1 catalogue tables (Flows, Swimlanes, Actions, Control nodes, Edges, Cross-flow swimlane matrix), which are always present.

> Content TBD per `plan/v7b-Brief.md > §Analyses > Downstream consumption` and per `framework/assets/analyses/activity-diagram-reference.md > Downstream consumption`.
