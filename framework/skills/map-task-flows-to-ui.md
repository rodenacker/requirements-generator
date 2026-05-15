<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order step 9. -->

# map-task-flows-to-ui.md

**Purpose:** Translate a Task Analysis & Task Flows catalogue (`analyses/TASK-FLOWS/task-flows.html`) into UI inventory entries: top-level tasks → screen-flow inventory entries (each task becomes a sequence of screen transitions in the design spec, anchored to a single lead persona); HTA subgoals → screen / wizard-step groupings (a subgoal often equals a screen or a logically-grouped step); HTA operations → atomic UI affordances (each operation maps to one user-visible control — a button, form field, link, or trigger); plans → routing logic for the UI (a `sequence` plan becomes a linear wizard; a `selection` plan becomes a branching screen with a decision point; an `iteration` plan becomes a list / repeater pattern; a `concurrent` plan becomes a tab / dashboard pattern); decision points → branching UI affordances (conditional sections, gated CTAs, decision modals); exception paths → error-state UI (toast / banner / modal / recovery screen per `exit_type` — `abort` = blocking error, `escalate` = notification + handoff, `retry` = retry CTA + countdown, `compensate` = undo / rollback affordance); cross-task operation matrix → component-reuse hints (an operation present in 3+ tasks warrants a first-class shared component in the design system).

**Inputs:** `analyses/TASK-FLOWS/task-flows.html`, `assets/taxonomy-screens.md`.

**Outputs:** UI inventory rows for the design spec.

**Used by:** `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when the task-flows analysis is present. Combines with other `map-*-to-ui` skills (e.g. `map-activity-diagram-to-ui.md` when the multi-actor lens has also been run, `map-use-cases-to-ui.md` when behavioural fidelity has been captured) via the accrue-all pattern — each skill contributes complementary entries to the same UI inventory. The task-flows skill focuses on **single-actor screen sequences and decomposition-to-affordance mapping**; the activity-diagram skill focuses on **multi-actor swimlane partitioning**; the use-cases skill focuses on **acceptance criteria per actor goal**. Task selection in the task-flows artefact does not affect the mapping — the mapping consumes the Tier-1 catalogue tables (Tasks, Subgoals & operations, Plans, Decision points, Exception paths, Cross-task operation matrix), which are always present.

> Content TBD per `plan/v7b-Brief.md > §Analyses > Downstream consumption` and per `framework/assets/analyses/task-flows-reference.md > Downstream consumption`.
