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

**Topic-driven checks (requirements stage):** sourced from `assets/topics-requirements.md > Pre-authoring invariants`. The skill emits a finding when any of the following fails — `personas_without_stories == 0`, `stories_without_goal_ref == 0`, `aggregate_invariants_without_br == 0` (every §2.3 invariant has a BR row in §6.2), `personas_missing_from_rbac == 0` (every §3 persona is a row in §6.5), `entities_unscoped_in_rbac == 0` and `flows_unscoped_in_rbac == 0` (every §7 entity and §5 flow is a column or scoped action), `nfr_session_timeout_present == true` (idle and absolute timeout values present in §6.6.1, `[AI-SUGGESTED]` counts as present), `nfr_subsection_empty_count == 0` (each §6.6 sub-section has ≥1 row).

> Content TBD per `plan/v7b-Brief.md > §Completeness report (reusable skill)`. Design-time rubric seed lives in `plan/completeness-report-rubric-seed.md`.
