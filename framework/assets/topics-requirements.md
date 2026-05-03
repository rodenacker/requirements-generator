<!-- ROLE: asset. STATUS: stub — author during phase-1 build-order step 1. -->

# topics-requirements.md

**Purpose:** Canonical list of the 10 topics every requirements spec must cover (Application context / Domain model / Target users / User goals / Task flows / Requirements / Data entities / Source UI references / Key terminology / Volumes), with per-topic acceptance criteria and minimum-useful-content rules. **Domain model (§2)** is the BA's ubiquitous-language framing of the business — distinct from §7 Data entities (the implementation-prep view) and from `analyses/ooux.html` (the UX-lens refinement that reads §2 as upstream input).

**Used by:**
- `framework/assets/template-requirements.md` — section skeleton mirrors this list one-to-one.
- `framework/agents/requirements-drafter/agent.md` — drives extraction + categorisation.
- `framework/skills/categorise-by-topic.md` — bucket assignment.
- `framework/skills/completeness-report.md` — per-topic completeness checks.

**How used:** Loaded by drafter + completeness-report skill. Defines the canonical bucket list for the §What's well-defined section of completeness reports. Authoring a new topic requires updating this file plus the template.

> Content TBD per `plan/v7b-Brief.md > §topics-requirements.md`.

**Pre-authoring invariants (preserve when filling in):**
- §4 is split into **§4.1 Goals catalogue** (flat list, stable G-NN IDs, outcome-level: quality signals + goal kind live here) and **§4.2 Stories by persona** (Connextra-triple stories grouped by persona, each referencing a goal ID from §4.1). M:N: a single goal may be referenced by stories under multiple personas.
- Every persona in §3 Target users **MUST** have ≥1 user story in §4.2.
- Every story in §4.2 **MUST** reference exactly one goal ID from §4.1. Every goal in §4.1 SHOULD be referenced by ≥1 story (orphan goals are a vague-finding, not a blocker).
- Quality signals are recorded on the goal, never restated on the story.
- §6 Requirements has six sub-sections: §6.1 Functional, §6.2 Business rules, §6.3 Data, §6.4 User-facing, §6.5 Access control (RBAC), §6.6 Non-functional. The four-bucket free-form layout is deprecated.
- §6.2 Business rules are typed rows (BR-NN), not free bullets. Each row carries Statement / Enforcement point / Source / Severity. Bijection: every §2.3 aggregate `Key invariant` appears as a BR; every BR sourced from §2.3 cites it.
- §6.5 Access control (RBAC) is a roles-×-resources matrix. Bijection: every §3 persona is a row; every §7 persistent entity and every §5 flow is a column (or scoped action within one). Conditional cells cite a BR-NN from §6.2.
- §6.6 Non-functional **MUST** be filled even when inferred — empty NFRs are a vague-finding, not "not applicable". Required sub-sections: Security & session, Performance, Availability, Compliance & audit, Accessibility. Within Security & session, idle timeout / absolute timeout / idle warning lead-time / re-auth scope / lockout / MFA are all required fields. Marker chosen per the drafter's decision tree (`framework/agents/requirements-drafter.md > Classification`): §6.6.5 Accessibility is in-scope (uses `[AI-SUGGESTED]` when inferred); §6.6.1–§6.6.4 are out-of-scope per `framework/shared/prototype-scope.md` and use `[OUT-OF-SCOPE: domain-default]` instead.
- §10 Volumes is **in-scope** — projected volumes drive UI pattern selection. All three fields (data volume, frequency, concurrency) must be filled; inferred values carry `[AI-SUGGESTED]`.
- Completeness checks (aligned with Tier A/B/D in `framework/skills/completeness-gap-pass.md`):
    - **Tier A:** `personas_without_stories == 0`; `stories_without_goal_ref == 0`; `personas_missing_from_rbac == 0`; `entities_unscoped_in_rbac == 0`; `flows_unscoped_in_rbac == 0`; `persistent_concepts_without_entity == 0`; `entity_domain_concept_dangling == 0`; `flow_actor_dangling == 0`; `volumes_complete == true`.
    - **Tier B:** `goals_without_story_ref == 0`; `rbac_conditional_cells_dangling == 0`; `entity_relationships_misaligned_with_2_2` warns only.
    - **Tier D:** `aggregate_invariants_without_br == 0` (every §2.3 invariant produces a §6.2 BR row; marker chosen per visual-manifestation test).
    - **Tier C (do not gate):** §6.6.1–§6.6.4 emptiness no longer fails completeness; only §6.6.5 Accessibility gates (`nfr_5_accessibility_present == true`).
