<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 3. -->

# completeness-report.md

**Purpose:** Reusable adversarial review skill used by both `/requirements` and `/design`. Produces a structured report with three categories of finding (AI-suggested / vague / contradictory) and three severity levels (blocker / major / minor — informational, not gating). Writes `completeness_hash` into `.progress.json` and persists the report to disk.

**Inputs:** the relevant spec file (`requirements.md` or `design-spec.md`), `assets/topics-*.md`, the stage-specific review character (`characters/requirements-review.md` or `characters/design-review.md`).

**Outputs:**
- Terminal: report surfaced in conversation.
- Disk: `artifacts/<stage>/completeness-reports/completeness-report.md` (single file, overwritten each run).
- `.progress.json`: `completeness_hash = sha256(<spec>)`, increments `completeness_iterations`.

**Used by:**
- `framework/orchestrators/requirements-orch.md` — step 4.
- `framework/orchestrators/design-orch.md` — step 3.

**Used how:** Domain-free skill; loaded with the stage-specific review character. Capped at 3 iterations since last Accept attempt. The Accept gate refuses unless `completeness_hash == sha256(current_spec)`.

**Topic-driven checks (requirements stage):** sourced from `assets/topics-requirements.md > Pre-authoring invariants` and aligned with the Tier A/B/D rules in `framework/skills/completeness-gap-pass.md`. The skill emits a finding when any of the following fails:

- **Tier A (hard bijections):** `personas_without_stories == 0` (A1); `stories_without_goal_ref == 0` (A2); `personas_missing_from_rbac == 0` (A3); `entities_unscoped_in_rbac == 0` (A4); `flows_unscoped_in_rbac == 0` (A5); `persistent_concepts_without_entity == 0` (A6); `entity_domain_concept_dangling == 0` (A7); `flow_actor_dangling == 0` (A8); `volumes_complete == true` (all three §10 fields filled, `[AI-SUGGESTED]` counts as present) (A9).
- **Tier B (soft references):** `goals_without_story_ref == 0` (B1); `rbac_conditional_cells_dangling == 0` (B2); `entity_relationships_misaligned_with_2_2` warns only (B3, no fabrication).
- **Tier D (mixed, in-scope only when visually manifested):** `aggregate_invariants_without_br == 0` (D1; every §2.3 invariant produces a §6.2 BR — marker chosen by visual-manifestation test, but the row must exist); `entity_field_marker_correctness` (D2; UI-display fields use `[AI-SUGGESTED]` when inferred, FK/index/audit fields use `[OUT-OF-SCOPE]`).
- **Tier C (out-of-scope, do not gate suggestions):** `nfr_5_accessibility_present == true` (§6.6.5 only). The other §6.6 sub-sections (§6.6.1 Security & session, §6.6.2 Performance, §6.6.3 Availability, §6.6.4 Compliance & audit) are filled with domain defaults under `[OUT-OF-SCOPE: domain-default]` and **no longer gate** completeness — empty there is acceptable.
- **Marker hygiene:** every `[AI-SUGGESTED]` field passes the precedence check — no `framework/shared/general-rules.md` rule covered the case (else it would be `[STANDARD-RULE]`); no `[AI-SUGGESTED]` is present inside Tier C sections (must be `[OUT-OF-SCOPE]`).

> Content TBD per `plan/v7b-Brief.md > §Completeness report (reusable skill)`. Design-time rubric seed lives in `plan/completeness-report-rubric-seed.md`.
