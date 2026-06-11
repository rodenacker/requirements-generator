<!-- ROLE: asset. Canonical topic list mirroring `framework/assets/template-requirements.md` one-to-one. -->

# topics-requirements.md

**Purpose:** Canonical list of the topics every requirements spec must cover, with per-topic acceptance criteria and minimum-useful-content rules. Sections marked *conditional* are emitted only when their predicate holds. **Domain model (§2)** is the BA's ubiquitous-language framing — distinct from §7 Data shapes (the FE-consumed view) and from `analyse-requirements/OOUX/ooux-object-map.html` (the UX-lens refinement that reads §2 as upstream input).

**Used by:**
- `framework/assets/template-requirements.md` — section skeleton mirrors this list one-to-one.
- `framework/agents/requirements-drafter.md` — drives extraction + categorisation + citation scope.
- `framework/skills/completeness-gap-pass.md` — per-topic completeness checks (Tier A/B/C/D rules).
- `framework/agents/reviews-inputs/gap-analysis-reviewer.md` — reads the `Dimension` column verbatim at runtime to classify per-topic gaps emitted against raw inputs (SPoT-owned dimension classification).

**How used:** Loaded by drafter + gap-pass skill + gap-analysis reviewer. Authoring a new topic requires updating this file, the template, and the gap-pass rules together; the new topic's row must include a `Dimension` value from the closed taxonomy.

**`Dimension` column (closed taxonomy, eight values).** Each topic is classified into exactly one dimension so consumers (currently the `/review-inputs` `gap-analysis-reviewer`; the `completeness-gap-pass` skill may consume it for AI-SUGGESTED prioritisation in future) can group, rank, and report per-dimension without maintaining a separate per-topic dimension table. The closed values:

- `Stakeholder` — personas, roles, actor identities, RBAC scopes (§3, §4, §6.5).
- `Scope` — context, boundaries (in/out/deferred), assumptions, architectural implications, source UI references (§0.1, §1, §1.5–§1.7, §8).
- `Domain` — concepts, relationships, aggregates, lifecycles, state transitions, glossary (§2.*, §9).
- `Functional` — features, business rules, validation rules, UI feature needs, reporting (§6.1–§6.4, §6.7).
- `Process` — task flows, edge/empty/error states, notification points (§5, §6.4.5, §6.8).
- `Non-functional` — session UX, FE performance budgets, accessibility, volumes (§6.6.1, §6.6.2, §6.6.5, §10).
- `Compliance` — compliance UI behaviour, audit-trail UI feature (§6.6.4, §6.9).
- `Integration` — consumed backend contracts (§6.10).
- `Data` — data shapes consumed by the FE, derivations (§7, §7.X).

Adding a new topic ships its `Dimension` value with the row; consumers read the value verbatim and never invent a classification.

## Section list (mirrors template 1:1)

| § | Topic | Emit predicate | Dimension |
| --- | --- | --- | --- |
| 0.1 | Target-mode applicability reference | always | Scope |
| 1 | Application context | always | Scope |
| 1.5 | Scope (in / out / deferred) | always | Scope |
| 1.6 | Assumptions & dependencies | conditional — ≥1 assumption / dependency stated or domain-implied (no filler rows) | Scope |
| 1.7 | Architectural implications | always (drafter-derived; scope-noted application-build guidance — see template §0.1) | Scope |
| 2.1 | Concepts | always | Domain |
| 2.2 | Relationships | always | Domain |
| 2.3 | Aggregates & lifecycles | always | Domain |
| 2.4 | Diagram (Mermaid) | always | Domain |
| 2.5 | State-transition matrix | conditional — ≥1 aggregate has >2 lifecycle states | Domain |
| 3 | Target users (personas) | always | Stakeholder |
| 4.1 | Goals catalogue | always | Stakeholder |
| 4.2 | Stories by persona | always | Stakeholder |
| 5 | Task flows | always | Process |
| 6.1 | Functional requirements | always | Functional |
| 6.2 | Business rules | always | Functional |
| 6.3 | Validation rules | always (may be empty) | Functional |
| 6.4 | UI feature needs (formerly "User-facing") | always | Functional |
| 6.4.5 | Edge, empty & error states | conditional — ≥1 §5 flow has `exception_paths` OR ≥1 §6.4 row implies state branching | Process |
| 6.5 | Access control (RBAC) | always | Stakeholder |
| 6.6.1 | Session UX | always (scope-noted application-build guidance — not a prototype design input, PI-01/PI-03; see template §0.1) | Non-functional |
| 6.6.2 | FE performance budgets | always (scope-noted application-build guidance — not a prototype design input, PI-08; see template §0.1) | Non-functional |
| 6.6.4 | Compliance UI behaviour | always (may be `[OUT-OF-SCOPE]` if not applicable) | Compliance |
| 6.6.5 | Accessibility | always | Non-functional |
| 6.7 | Reporting feature needs | conditional — inputs name reports/dashboards/exports, or domain implies them | Functional |
| 6.8 | Notification points | conditional — inputs name notifications/alerts, or domain implies them | Process |
| 6.9 | Audit-trail UI feature | conditional — §6.6.4 or inputs call for user-visible audit history | Compliance |
| 6.10 | Consumed backend contracts | always (sub-block matches `manifest.target`) | Integration |
| 7 | Data shapes consumed by the FE | always | Data |
| 7.X | Derivations | conditional — ≥1 §2.1 concept marked `Persistence = derived` | Data |
| 8 | Source UI references | conditional — ≥1 consultant-supplied screenshot / wireframe / existing-tool screen | Scope |
| 9 | Key terminology | conditional — ≥1 inconsistency flag / alternate-term usage (full glossary lives in the GLOSSARY analysis) | Domain |
| 10 | Volumes | always | Non-functional |

Sections retired vs. prior versions: **§6.6.3 Availability** (backend concern; lives in sibling backend doc). The §6.3 slot — previously retired as `Data` (subsumed into §7 + §6.4) — is now **reinstated** as **Validation rules** (visible field-level UI validation; backend invariants remain in §6.2 / sibling backend doc).

## Pre-authoring invariants (preserve when filling in)

- §4 is split into **§4.1 Goals catalogue** (flat list, stable G-NN IDs, outcome-level — quality signals + goal kind live here) and **§4.2 Stories by persona** (Connextra-triple stories grouped by persona, each referencing a goal ID from §4.1). M:N: a single goal may be referenced by stories under multiple personas.
- Every persona in §3 **MUST** have ≥1 user story in §4.2.
- Every story in §4.2 **MUST** reference exactly one goal ID from §4.1. Every goal in §4.1 SHOULD be referenced by ≥1 story (orphan goals are a vague-finding, not a blocker).
- Quality signals are recorded on the goal, never restated on the story. Quality signals on **top-level** goals SHOULD be measurable outcome signals where the inputs support one (the lightweight stand-in for a success-metrics section when no PRD is run; full success metrics stay in the PRD §5.2). No separate column.
- §4.2 stories, §6.1 functional reqs, §6.2 business rules, and every §5 task-flow step **MUST** carry an Acceptance criteria value (`GR-21` applies — no visual phrasing). **Acceptance-criteria syntax is hybrid per `GR-23`:** §6.1 functional reqs and §6.2 business rules use **EARS** keywords (`When/While/Where/If-Then … the system shall …`, ≤3 preconditions); §4.2 stories, §5 flow steps, and §6.4 UI feature needs keep observable-signal / Given-When-Then phrasing. §6.3 validation rows are already in EARS event-driven form by construction (Rule → Error message). Drafter auto-fabricates from observable signals when input is silent (Tier B5).
- §4.2 stories, §6.1 functional reqs (F-NN), and §6.4 UI feature needs (UI-NN) **MUST** carry a `Priority` value (`Must` / `Should` / `Could` / `Won't`). Default derived per `GR-24` (carries `[STANDARD-RULE: GR-24]`); input-stated priority carries `[SRC: C-NNN]`. Priority enables MVP slicing for downstream wireframe / prototype generation. Soft completeness check B6.
- §6 sub-sections: §6.1 Functional, §6.2 Business rules, §6.3 Validation rules, §6.4 UI feature needs, §6.4.5 Edge / empty / error states (conditional), §6.5 RBAC, §6.6 NFR (FE-only), §6.7 Reporting (conditional), §6.8 Notifications (conditional), §6.9 Audit-trail UI (conditional), §6.10 Consumed backend contracts.
- §6.2 Business rules are typed rows (BR-NN), not free bullets. Each row carries Statement / Enforcement point / Acceptance criteria / Source / Severity. Bijection: every §2.3 aggregate `Key invariant` appears as a BR; every BR sourced from §2.3 cites it.
- §6.3 Validation rules capture the *visible* field-level validation surface (required-field markers, format / range / length / enum / cross-field errors). Field cell references a §7 shape field; `business-rule-ref` cells cite a §6.2 BR-NN. Backend enforcement of business invariants belongs to §6.2 and the sibling backend doc. Validation *timing* (real-time / on-blur / on-submit) is governed by `GR-05` and captured in §6.4.
- §6.4 UI feature needs are typed rows (UI-NN). `GR-21` forbids layout vocabulary; cells describe *what must exist*, not *how it is arranged*. Rows deterministically resolved by `GR-05..GR-18` carry `[STANDARD-RULE: GR-NN]`.
- §6.4.5 Edge, empty & error states is emitted when ≥1 §5 flow has `exception_paths` OR a §6.4 row implies state branching. Surface cell references a §4.2 story, §5 flow, or §6.4 UI-NN; condition uses the closed vocabulary `{empty, partial, error, offline, loading, permission-denied}`. Behavioural phrasing only (`GR-21`).
- §6.5 RBAC is a roles-×-resources matrix. Bijection: every §3 persona is a row; every §7 entity and every §5 flow is a column (or scoped action). Conditional cells cite a BR-NN from §6.2.
- §6.6 NFR is **FE-only**. Sub-sections: §6.6.4 Compliance UI behaviour + §6.6.5 Accessibility are emitted under **both** targets (FE-relevant; `[AI-SUGGESTED]` when inferred). §6.6.1 Session UX + §6.6.2 FE performance budgets are emitted under **both** targets as scope-noted application-build guidance (not a prototype design input — server/auth simulated per PI-01/PI-03; the prototype is a review harness per PI-08); `GR-19` supplies §6.6.1 defaults, gap-pass rule B7 covers the rest. Backend availability / throughput / persistence concerns belong in the sibling backend doc.
- §6.7 Reporting needs **never** specify chart type or layout (`GR-21`). Source concept(s) must reference §2.1; audience must reference §3.
- §6.8 Notification points use capability-level channel names only (`in-app`, `email`, `sms`, `webhook`, `push`); no vendor name (`GR-20`).
- §6.10 Consumed backend contracts emits exactly one sub-block — the one matching `manifest.target`. Prototype variant rows reference fixture paths; application variant rows are *pointers only* into the sibling backend doc and never restate the contract.
- §7 Data shapes captures the FE-consumed shape only — persistence design (indexes, FKs, storage layout) is the backend doc's concern. Validation *rules* live in §6.3; validation *timing* (when feedback appears) is captured in §6.4 with `GR-05`.
- §7.X Derivations is emitted only when ≥1 §2.1 concept has `Persistence = derived`. Rule cells are business-language; computation tier appears in §1.7.
- §10 Volumes is **in-scope** — projected volumes drive UI pattern selection. All three fields (data volume, frequency, concurrency) must be filled; inferred values carry `[AI-SUGGESTED]`. Capacity planning is the backend doc's concern.

## Completeness checks (aligned with Tier A/B/C/D in `framework/skills/completeness-gap-pass.md`)

- **Tier A (hard bijection):**
  - `personas_without_stories == 0`
  - `stories_without_goal_ref == 0`
  - `personas_missing_from_rbac == 0`
  - `entities_unscoped_in_rbac == 0`
  - `flows_unscoped_in_rbac == 0`
  - `persistent_concepts_without_entity == 0`
  - `entity_domain_concept_dangling == 0`
  - `flow_actor_dangling == 0`
  - `volumes_complete == true`
  - **A10** `scope_has_at_least_one_in_row == true` — §1.5 has ≥1 In bucket entry; drafter fabricates from §1 purpose if absent.
  - **A11** `state_transition_invariants_covered == true` — every §2.3 invariant naming a state appears as a §2.5 row (only when §2.5 is emitted).
  - **A12** `reporting_source_concept_resolves == true` — every §6.7 row names ≥1 existing §2.1 concept.
  - **A13** `notification_audience_resolves == true` — every §6.8 row's Audience names an existing §3 persona.
  - **A14** `backend_op_maps_to_functional_req == true` — every §6.10 Operation maps to a §6.1 F-NN.
  - **A15** `derived_shape_resolves == true` — every §7.X concept exists in §2.1 with `Persistence = derived`.
- **Tier B (soft / warn or fabricate):**
  - `goals_without_story_ref == 0`
  - `rbac_conditional_cells_dangling == 0`
  - `entity_relationships_misaligned_with_2_2` — warn only.
  - **B4** `architectural_implication_cites_requirement == true` — every §1.7 row's Driving requirement cell cross-refs ≥1 §6 / §10 row; warn-only. Active under both targets (§1.7 is emitted on every run).
  - **B5** `acceptance_criteria_populated == true` — every §4.2 story / §6.1 F-NN / §6.2 BR-NN / §5 flow step has a populated Acceptance criteria cell; drafter auto-fabricates from observable signals when silent (`[AI-SUGGESTED]`). §6.1 / §6.2 cells use EARS per `GR-23`.
  - **B6** `priority_populated == true` — every §4.2 story / §6.1 F-NN / §6.4 UI-NN has a `Priority` value (`Must` / `Should` / `Could` / `Won't`); default derived per `GR-24` (`[STANDARD-RULE: GR-24]`), so this never gates as AI-SUGGESTED. Warn-only if a row is missing one.
  - **B7** `application_guidance_fields_populated == true` — every §6.6.1 field not resolved by `GR-19` and every §6.6.2 metric has a populated value; fabricated from domain + §10 volumes (`[AI-SUGGESTED: non-blocking]`).
- **Tier C (do not gate — domain-default fill):**
  - §6.6 sub-sections are FE-relevant under both targets; emptiness no longer fails completeness because they always populate from `GR-19` defaults or `[AI-SUGGESTED]` inferences. (§6.6.3 Availability is retired entirely from the template — backend concern.)
- **Tier D (visual-manifestation gating):**
  - `aggregate_invariants_without_br == 0` — every §2.3 invariant produces a §6.2 BR row; marker chosen per visual-manifestation test.
  - **D3** `state_transitions_server_only_marked == true` — §2.5 rows whose Visible effect is purely server-side carry `[OUT-OF-SCOPE]` (prototype) / no marker (application).
  - **D4** `reporting_audience_has_rbac_read == true` — every §6.7 row's audience persona has read access to the named source concept per §6.5; mismatch is a warn-level Tier B flag.
