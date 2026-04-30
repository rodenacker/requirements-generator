<!-- ROLE: asset (P2 analysis reference). STATUS: stub — author during phase-2 build-order step 8 or 9. -->

# analyses/ooux-reference.md

**Purpose:** Methodology reference for Object-Oriented UX analysis (Sophia Prater's ORCA process). Six rounds in order: Discovery → Objects → Relationships → CTAs → Attributes → Prioritisation (Core Content Priorities). Quality checks: every Object has ≥1 CTA; every CTA attached to exactly one Object; every nested Relationship declares cardinality; every Object has ≥1 Attribute marked CCP; no orphan Attributes. Stop-condition: all required Objects from §Task flows are represented with CTAs + CCPs. **Upstream input:** the analyser starts from `requirements.md > §2 Domain model > Concepts` — OOUX is a UX-lens refinement of the BA's domain model, never a parallel inventory. Object names match §2.1 concept names verbatim; OOUX adds CTAs, relationship-navigation intent, and grid attributes the domain model doesn't carry.

**Used by:**
- `framework/agents/analyses/ooux-analyser/agent.md` — drives the agent's six-round process.
- `framework/skills/map-ooux-to-ui.md` — uses the object-map structure to derive UI inventory entries.
- `framework/assets/persona-llm.md` — loaded into Unicorn's persona context (if registered + present on disk).

**Output:** `artifacts/requirements/analyses/ooux.html` — self-contained HTML object-map grid using `template-ooux.html` as scaffold.

> Content TBD per `plan/v7b-Brief.md > §analyses/ooux-reference.md`.
