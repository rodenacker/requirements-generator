<!-- ROLE: asset (P2 analysis reference). STATUS: stub — author during phase-2 build-order step 8 or 9. -->

# analyses/user-stories-reference.md

**Purpose:** Methodology reference for User Stories analysis. Statement form: _"As a `<role>`, I want to `<action>`, so that `<outcome>`."_ Acceptance criteria use Given/When/Then. Grouping: by primary target-user persona, then by MoSCoW priority (must / should / could / won't). Traceability: every story cites the requirement IDs it expresses + the user goal it serves. Quality checks: role is a named target-user persona (never "user"); action is specific (never "manage"/"handle"); outcome is measurable or observable. Stop-condition: every task-flow leaf produces ≥1 story; every user goal is covered by ≥1 story.

**Used by:**
- `framework/agents/analyses/user-stories-analyser/agent.md` — drives the agent's process.
- `framework/skills/map-user-stories-to-ui.md` — stories → acceptance criteria per screen + CTAs.
- `framework/assets/persona-llm.md` — loaded into persona context (if registered + present).

**Output:** `artifacts/requirements/analyses/user-stories.md` — markdown with `##` per target-user persona, `###` per priority, bullet per story + acceptance criteria.

> Content TBD per `plan/v7b-Brief.md > §analyses/user-stories-reference.md`.
