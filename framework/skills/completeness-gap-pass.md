# completeness-gap-pass.md

**Purpose:** Walk a populated requirements draft against the relatedness graph (Tier A/B/D rules) and the prototype scope boundary, decide for each gap whether to fabricate the missing element with `[AI-SUGGESTED]`, apply a deterministic answer from `general-rules.md` with `[STANDARD-RULE]`, or fill with a domain default tagged `[OUT-OF-SCOPE: domain-default]`. Used by the requirements-drafter at workflow step 5 (post-fill, pre-write-final).

**Inputs:**
- The in-memory populated draft (template-requirements.md filled top-to-bottom from inputs and domain defaults; **no `[AI-SUGGESTED]` markers yet**).
- `framework/shared/prototype-scope.md` — in-scope vs out-of-scope predicate.
- `framework/shared/general-rules.md` — catalogue of `GR-NN` deterministic rules.
- `framework/assets/topics-requirements.md` — bijection invariants.

**Outputs:**
- A list of `(rule_id, location, action, marker_kind, marker_payload)` tuples that the drafter applies to the draft via Edit / Write.
- The next-available `AI-NNN` index, continuing the existing counter.

## Decision tree (per gap)

For every field or element required by the template that is not directly stated in the inputs, walk these steps in order. Stop at the first match.

1. **Stated-in-inputs.** If the inputs supply the value, use it verbatim. **No marker.** (Handled by drafter step 3, not by this skill — included for completeness.)
2. **General-rules lookup.** Read `framework/shared/general-rules.md`. If a `GR-NN` rule's scope predicate matches this field/element, apply the rule's canonical answer. Marker: `[STANDARD-RULE: GR-NN]`.
3. **Completeness-required (Tier A/B).** If the field/element is required by a Tier A or Tier B rule below:
    - Tier A or B1/B2 → fabricate the missing element. Marker: `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` per the drafter's classification rubric (`requirements-drafter.md > Classification`).
    - B3 → emit a soft warning to the drafter's gap-pass log. **No fabrication, no marker.**
4. **In-scope per prototype-scope.md.** If completeness-required AND in-scope, fall through to step 3 (already covered). If completeness-required but **out-of-scope**, fill with a domain default. Marker: `[OUT-OF-SCOPE: domain-default]`.
5. **Not completeness-required, not stated.** Fill with a domain default. Marker: `[OUT-OF-SCOPE: domain-default]`.

The Tier C sections below are short-circuited at step 4 — they are completeness-required by the template (`fill every field`) but explicitly out-of-prototype-scope.

## Tier A — hard bijections (gap → fabricate + `[AI-SUGGESTED]`)

| # | Rule | Fabrication action |
|---|---|---|
| A1 | Every §3 persona has ≥1 story in §4.2 | create story under persona heading; set `Goal: → §4.1 G-NN` (creating a goal via A2 if needed) |
| A2 | Every §4.2 story references exactly one §4.1 goal-id | create new `G-NN` row in §4.1 with inferred goal statement |
| A3 | Every §3 persona is a row in §6.5 RBAC | add row; per-cell `[AI-SUGGESTED]` on inferred CRUD/X/A/— values |
| A4 | Every §7 entity is a column (or scoped action) in §6.5 | add column; per-cell `[AI-SUGGESTED]` |
| A5 | Every §5 task flow is a column (or scoped action) in §6.5 | add column or scoped action; per-cell `[AI-SUGGESTED]` |
| A6 | Every §2.1 *persistent* concept appears as a §7 entity | create entity stub: name + minimal field set inferred from concept definition + `Domain concept: <concept_name>` |
| A7 | Every §7 entity's "Domain concept" field names an existing §2.1 concept | if reference dangles: prefer adding the concept to §2.1 (with `[AI-SUGGESTED]`) over silently renaming the entity, unless inputs more strongly support the rename |
| A8 | Every §5 flow's Actor names an existing §3 persona | prefer adding the persona to §3 (with `[AI-SUGGESTED]`) over silently renaming the flow's Actor, unless inputs more strongly support the rename |
| A9 | §10 Volumes has all three fields filled (data volume, frequency, concurrency) | infer bands per domain heuristics (e.g. SaaS B2B: 10²–10⁴ records, daily frequency, 10¹–10² concurrent users); per-field `[AI-SUGGESTED]` |

## Tier B — soft references

| # | Rule | Action |
|---|---|---|
| B1 | Every §4.1 goal is referenced by ≥1 §4.2 story | fabricate story under most plausible persona; mark `[AI-SUGGESTED]` |
| B2 | Every §6.5 conditional cell `<action>†BR-NN` names a real §6.2 BR-NN | fabricate BR-NN row in §6.2 inferred from the role + action + entity context; mark `[AI-SUGGESTED]` |
| B3 | §7 entity relationships align with §2.2 | warn only; **no fabrication** (FK fabrication is too error-prone without input support) |

## Tier D — mixed (in-scope only when visually manifested)

**D1 — §2.3 invariant → §6.2 BR projection.** Every §2.3 invariant must produce a §6.2 BR row (the bijection is preserved). The marker depends on visual manifestation:

- Mark `[AI-SUGGESTED]` if the invariant maps to **any one** of:
  - a status badge transition (a §2.3 lifecycle state change),
  - a conditional UI visibility (button/field shown/hidden based on state),
  - a role-gated action (visible only to certain personas),
  - an inline validation error (form-field error message).
- Otherwise (pure server-side computation, scheduling, audit trail, ledger reconciliation) mark `[OUT-OF-SCOPE: domain-default]`.

§2.3 itself is **not** filtered — all invariants stay in the domain model artefact for downstream design.

**D2 — §7 entity field-level (UI-display test).** A field gates `[AI-SUGGESTED]` only if it appears in a UI surface: form input, table column, detail-view label, status chip, dropdown enum, search filter. FK columns, internal IDs, audit timestamps, indexes → `[OUT-OF-SCOPE: domain-default]`.

## Tier C — out-of-scope sections (fill + `[OUT-OF-SCOPE: domain-default]`, no Q&A)

| Section | Rationale |
|---|---|
| §6.6.1 Security & session (idle/absolute timeout, idle warning, re-auth, lockout, MFA) | `prototype-scope.md` "Authentication/authorization implementation", "Security implementation details" |
| §6.6.2 Performance | `prototype-scope.md` "Performance optimization techniques" |
| §6.6.3 Availability (uptime, maintenance window, RTO/RPO) | `prototype-scope.md` "DevOps, CI/CD, infrastructure" |
| §6.6.4 Compliance & audit | `prototype-scope.md` "Security implementation details" — **exception:** regimes that drive consent banners or PII screen redaction → `[AI-SUGGESTED]` |
| §7 entity FK / index / DB-only fields | `prototype-scope.md` Data model elements — explicit exclusion of "database table definitions, indexes, foreign key constraints" |

§6.6.5 Accessibility is **in-scope** — drives design tokens & screen states.

## Algorithm (deterministic; the skill performs no LLM call itself)

1. Walk the populated draft section-by-section.
2. For each rule in Tier A, B, D, evaluate the predicate against the draft state.
3. For each violation, run the decision tree above to produce a `(rule_id, location, action, marker_kind, marker_payload)` tuple.
4. Emit the tuple list to the drafter, plus the running `AI-NNN` counter.
5. The drafter applies the tuples to the draft (via Edit) before writing the final file.

## Used by

- `framework/agents/requirements-drafter.md` — workflow step 5 (post-fill, pre-write).

## Anti-Patterns

- Do not call an LLM inside this skill. The decision tree is deterministic; inference (when needed) is performed by the drafter consuming the tuple list.
- Do not emit `[AI-SUGGESTED]` for any tuple whose decision tree resolved at step 2 (general-rules) or step 4 (out-of-scope).
- Do not skip the `general-rules.md` lookup; it must precede every `[AI-SUGGESTED]` decision.
- Do not modify §2.3 — invariant filtering applies only at the §2.3 → §6.2 projection.
