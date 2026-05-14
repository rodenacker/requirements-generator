<!--
  ROLE: asset (Markdown template). Populated by framework/agents/reviews/adversarial-reviewer.md.

  Purpose: Markdown skeleton for the Adversarial Review report. Plain markdown
  (no HTML wrapper, no inlined CSS) so it renders in any markdown viewer and
  diffs cleanly in git. The reviewer substitutes the documented {{placeholders}}
  with HTML-escaped content (markdown special characters preserved in Evidence
  quotes are escaped per markdown rules — e.g. `|` inside a table cell becomes
  `\|`).

  Placeholders the reviewer substitutes (string substitution, all values
  pre-escaped for markdown):

    {{TITLE}}                  — short title (e.g. "Adversarial Review — Project X")
    {{DOMAIN}}                 — domain string (from requirements §1 if present)
    {{GENERATED_AT}}           — ISO-8601 UTC timestamp the artefact was rendered
    {{REQUIREMENTS_SHA256}}    — sha256 of requirements/requirements.md at read time
    {{REVIEWER_IDENTITY}}      — fixed string "Adversarial Review (BMAD-style, strict mode)"
    {{TOTAL_FINDINGS}}         — count of findings across all dimensions
    {{BLOCKER_COUNT}}          — count of Severity: Blocker
    {{MAJOR_COUNT}}            — count of Severity: Major
    {{MINOR_COUNT}}            — count of Severity: Minor
    {{PATCH_COUNT}}            — count of Disposition: Patch
    {{DEFER_COUNT}}            — count of Disposition: Defer
    {{REJECT_COUNT}}           — count of Disposition: Reject
    {{VERDICT}}                — one of BLOCKED | NEEDS-REVISION | ACCEPTED-WITH-FIXES
    {{FINDINGS_TABLE}}         — pre-rendered markdown table body (one row per finding) per FINDINGS TABLE SCHEMA below
    {{DIMENSION_1_BLOCK}}      — pre-rendered dimension section: either findings list or Justification block
    {{DIMENSION_2_BLOCK}}      — (likewise)
    {{DIMENSION_3_BLOCK}}
    {{DIMENSION_4_BLOCK}}
    {{DIMENSION_5_BLOCK}}
    {{DIMENSION_6_BLOCK}}
    {{DIMENSION_7_BLOCK}}
    {{DIMENSION_8_BLOCK}}
    {{DIAGNOSTICS_BLOCK}}      — pre-rendered diagnostics per DIAGNOSTICS SCHEMA below

  Output: reviews/ADVERSARIAL/adversarial-review.md.

  FINDINGS TABLE SCHEMA — each row the reviewer emits has the shape:

      | ADV-NN | D | Sev | Disp | §loc | one-line problem |

    where:
      - ADV-NN is the finding ID (zero-padded sequence per run)
      - D is the Dimension integer 1..8
      - Sev is one of Blocker | Major | Minor
      - Disp is one of Patch | Defer | Reject
      - §loc is the Location field (§N.N, BR-NN, G-NN, FR-NN, or line-N)
      - one-line problem is the Problem field; pipe characters inside are escaped as \|

  DIMENSION BLOCK SCHEMA — each {{DIMENSION_N_BLOCK}} contains either:

    Variant A — findings present (one or more):

        ### Findings

        #### ADV-NN — {{one-line-problem}}

        - **Severity:** Blocker | Major | Minor
        - **Disposition:** Patch | Defer | Reject
        - **Location:** {{location-anchor}}
        - **Evidence:**
          > {{verbatim quote, ≤5 lines, as markdown blockquote}}
        - **Problem:** {{one-sentence statement of the defect}}
        - **Recommendation:** {{one-sentence concrete corrective action}}

        (repeat per finding within this dimension)

    Variant B — zero findings + strict-BMAD justification:

        ### Justification (zero findings — strict-BMAD re-run passed)

        {{≥3-sentence justification citing specific evidence
          and naming the anti-confirmation prompts attempted}}

  DIAGNOSTICS SCHEMA — the {{DIAGNOSTICS_BLOCK}} contains:

    ## Diagnostics

    ### Quality gates

    | Gate | Result | Notes |
    |------|--------|-------|
    | 1. All findings have 8 schema fields populated | PASS / FAIL | {{flagged item count}} |
    | 2. All Dimension fields are 1..8                | PASS / FAIL | {{...}} |
    | 3. All Severity fields are valid                | PASS / FAIL | {{...}} |
    | 4. All Disposition fields are valid             | PASS / FAIL | {{...}} |
    | 5. All Evidence quotes are verbatim & ≤5 lines  | PASS / FAIL | {{...}} |
    | 6. All Location anchors exist in requirements   | PASS / FAIL | {{...}} |
    | 7. Every dimension has ≥1 finding or Justification | PASS / FAIL | {{...}} |
    | 8. All Justifications are ≥3 sentences          | PASS / FAIL | {{...}} |
    | 9. Verdict matches disposition tally            | PASS / FAIL | {{...}} |
    | 10. Findings Table row count = per-dim sum      | PASS / FAIL | {{...}} |
    | 11. REQUIREMENTS_SHA256 matches Step-2 capture  | PASS / FAIL | {{...}} |

    ### Coverage map

    | Dimension | Sections / IDs touched | Finding count |
    |-----------|------------------------|---------------|
    | 1. Completeness & Gaps        | {{list}} | {{n}} |
    | 2. Ambiguity & Clarity        | {{list}} | {{n}} |
    | 3. Testability & Verifiability| {{list}} | {{n}} |
    | 4. Scope & MVP Boundaries     | {{list}} | {{n}} |
    | 5. Dependency & Ordering      | {{list}} | {{n}} |
    | 6. Consistency & Internal Conflict | {{list}} | {{n}} |
    | 7. Edge Cases & Error Handling | {{list}} | {{n}} |
    | 8. Feasibility & Constraints  | {{list}} | {{n}} |

    ### Strict-BMAD re-run log

    {{One line per dimension where the strict-BMAD halt rule fired,
       stating: dimension number, anti-confirmation prompts attempted,
       outcome (additional findings produced / justification written).
       If no dimension triggered the rule, write "No dimensions triggered
       the strict-BMAD re-run rule."}}

    ### Override log

    {{If the consultant chose Override at the Step-10 quality-gate sweep,
       list each failed gate by number and the items flagged. Otherwise
       write "All quality gates passed; no override invoked."}}

-->

# {{TITLE}}

- **Domain:** {{DOMAIN}}
- **Generated:** {{GENERATED_AT}}
- **Requirements SHA-256:** `{{REQUIREMENTS_SHA256}}`
- **Reviewer:** {{REVIEWER_IDENTITY}}

---

## Executive Summary

- **Total findings:** {{TOTAL_FINDINGS}}
  - Severity — Blocker: **{{BLOCKER_COUNT}}** · Major: **{{MAJOR_COUNT}}** · Minor: **{{MINOR_COUNT}}**
  - Disposition — Patch: **{{PATCH_COUNT}}** · Defer: **{{DEFER_COUNT}}** · Reject: **{{REJECT_COUNT}}**
- **Verdict:** `{{VERDICT}}`

> Verdict legend: `BLOCKED` — at least one Reject or Blocker, requirements doc cannot be consumed downstream. `NEEDS-REVISION` — findings present but none blocking. `ACCEPTED-WITH-FIXES` — zero findings on all eight dimensions, every dimension carries a Justification block (rare under strict-BMAD).

---

## Findings Table

| ID | Dim | Severity | Disposition | Location | Problem |
|----|-----|----------|-------------|----------|---------|
{{FINDINGS_TABLE}}

---

## Dimension 1 — Completeness & Gaps

{{DIMENSION_1_BLOCK}}

---

## Dimension 2 — Ambiguity & Clarity

{{DIMENSION_2_BLOCK}}

---

## Dimension 3 — Testability & Verifiability

{{DIMENSION_3_BLOCK}}

---

## Dimension 4 — Scope & MVP Boundaries

{{DIMENSION_4_BLOCK}}

---

## Dimension 5 — Dependency & Ordering

{{DIMENSION_5_BLOCK}}

---

## Dimension 6 — Consistency & Internal Conflict

{{DIMENSION_6_BLOCK}}

---

## Dimension 7 — Edge Cases & Error Handling

{{DIMENSION_7_BLOCK}}

---

## Dimension 8 — Feasibility & Constraints

{{DIMENSION_8_BLOCK}}

---

{{DIAGNOSTICS_BLOCK}}
