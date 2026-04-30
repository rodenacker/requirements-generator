<!-- ROLE: asset (P2 analysis reference). STATUS: stub — author during phase-2 build-order step 8 or 9. -->

# analyses/jtbd-reference.md

**Purpose:** Methodology reference for Jobs-to-be-Done analysis. Statement form: _"When `<situation>`, I want to `<motivation>`, so I can `<expected outcome>`."_ Job typology: main (functional), emotional, social — separate rows when relevant. Priority: importance × satisfaction gap; jobs with high importance + low current satisfaction drive primary tasks. Quality checks: situation is concrete (never "when using the app"); motivation is a job the product could be hired for (never a feature request); outcome is measurable.

**Used by:**
- `framework/agents/analyses/jtbd-analyser/agent.md` — drives the agent's process.
- `framework/skills/map-jtbd-to-ui.md` — JTBD → primary-task weighting + Core Content Priority signals for screen prioritisation.
- `framework/assets/persona-llm.md` — loaded into persona context (if registered + present).

**Output:** `artifacts/requirements/analyses/jtbd.md` — markdown with `##` per job cluster, bullet per statement + importance/satisfaction scoring.

> Content TBD per `plan/v7b-Brief.md > §analyses/jtbd-reference.md`.
