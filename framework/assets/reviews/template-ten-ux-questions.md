<!--
  ROLE: asset (Markdown template). Populated by framework/agents/reviews/ten-ux-questions-reviewer.md.

  Purpose: Markdown skeleton for the 10 UX Questions review. Plain markdown
  (no HTML wrapper, no inlined CSS) so it renders in any markdown viewer and
  diffs cleanly in git. The reviewer substitutes the documented {{placeholders}}
  with HTML-escaped content (markdown special characters preserved in question
  text and rationale; pipe characters inside table cells become `\|`).

  Placeholders the reviewer substitutes (string substitution, all values
  pre-escaped for markdown):

    {{TITLE}}                    — short title (e.g. "10 UX Questions — Project X")
    {{DOMAIN}}                   — domain string (from requirements §1 if present)
    {{GENERATED_AT}}             — ISO-8601 UTC timestamp the artefact was rendered
    {{REQUIREMENTS_SHA256}}      — sha256 of requirements/requirements.md at read time
    {{REVIEWER_IDENTITY}}        — fixed string "10 UX Questions Review (experienced UX designer lens)"
    {{TOTAL_QUESTIONS}}          — always 10 (gate-enforced; placeholder retained for visibility)
    {{BLOCKING_COUNT}}           — count of questions with priority = blocking
    {{MAJOR_COUNT}}              — count of questions with priority = major
    {{MINOR_COUNT}}              — count of questions with priority = minor
    {{CANDIDATE_POOL_SIZE}}      — number of candidates generated at Step 3 (≤ 50)
    {{CATEGORY_COVERAGE}}        — "N of 8 (C-list)" where C-list is the comma-separated category IDs represented (e.g. "6 of 8 (C1, C3, C4, C5, C6, C8)")
    {{TRIAGE_BLOCK}}             — pre-rendered triage table per TRIAGE BLOCK SCHEMA below
    {{QUESTION_1_BLOCK}}         — pre-rendered question section for UXQ-01
    {{QUESTION_2_BLOCK}}         — (likewise for UXQ-02)
    {{QUESTION_3_BLOCK}}
    {{QUESTION_4_BLOCK}}
    {{QUESTION_5_BLOCK}}
    {{QUESTION_6_BLOCK}}
    {{QUESTION_7_BLOCK}}
    {{QUESTION_8_BLOCK}}
    {{QUESTION_9_BLOCK}}
    {{QUESTION_10_BLOCK}}
    {{DIAGNOSTICS_BLOCK}}        — pre-rendered diagnostics per DIAGNOSTICS SCHEMA below

  Output: review-requirements/TEN-UX-QUESTIONS/ten-ux-questions-review.md.

  TRIAGE BLOCK SCHEMA — {{TRIAGE_BLOCK}} is a single markdown table listing
  every selected question in rank order (UXQ-01 first, UXQ-10 last):

      | Rank | ID | Priority | Category | Anchor | Question (first line) |
      |------|----|----------|----------|--------|------------------------|
      | 1 | UXQ-01 | blocking | C3 Goals & success signals | §4.1 | one-line question text |
      | 2 | UXQ-02 | major    | C4 Tasks, flows, decision points | §5 | ... |
      | ... |

    Field rules:
      - Rank is the 1-based row index after Step-5 score-descending sort. Rank 1 = UXQ-01.
      - ID is UXQ-NN, zero-padded.
      - Priority is one of `blocking | major | minor` (lowercase, no decoration).
      - Category is the C-ID and its human-readable label (e.g. "C3 Goals & success signals").
      - Anchor is either `§N.N` (a section that exists in the doc) or `missing-section: <slug>` (e.g. `missing-section: context-of-use`).
      - Question (first line) is the question text truncated at the first sentence or 100 chars, whichever is shorter; if truncated, append "…".
      - Pipe characters inside any cell are escaped as `\|`.

  QUESTION BLOCK SCHEMA — each {{QUESTION_N_BLOCK}} contains:

      ### UXQ-NN — {{priority}} — {{category-id}} {{category-label}} — {{anchor-or-missing}}

      > {{question_text}}

      **Why this matters.** {{rationale}}

    Field rules:
      - Heading line uses em-dashes (—), not hyphens, as separators.
      - {{priority}} is the lowercase label (blocking | major | minor).
      - {{category-id}} is C1..C8; {{category-label}} is the matching label from this file's category list.
      - {{anchor-or-missing}} is the same string as the Anchor column in the Triage table.
      - {{question_text}} is rendered as a markdown blockquote (`>` prefix on each line). The question is verbatim from the in-memory candidate's `question_text` field; markdown special characters inside the question are preserved (not stripped).
      - **Why this matters.** is bolded literal text followed by the rationale. The rationale is 1–3 sentences of plain prose; markdown special characters are preserved.

  DIAGNOSTICS SCHEMA — the {{DIAGNOSTICS_BLOCK}} contains:

    ## Diagnostics

    ### Candidate pool

    | Stat | Value |
    |------|-------|
    | Candidates generated (Step 3)            | NN (≤ 50)       |
    | Dropped: GR-NN match (Step 4)            | NN              |
    | Dropped: PI-NN match (Step 4)            | NN              |
    | Dropped: out-of-scope (Step 4)           | NN              |
    | Surviving candidates after filter        | NN              |
    | Selected (Step 5)                        | 10              |

    ### Category coverage

    | Category                                  | Candidates generated | Candidates surviving filter | Selected |
    |-------------------------------------------|----------------------|------------------------------|----------|
    | C1 Users & segmentation                   | NN                   | NN                           | NN       |
    | C2 Context of use                         | NN                   | NN                           | NN       |
    | C3 Goals & success signals                | NN                   | NN                           | NN       |
    | C4 Tasks, flows, decision points          | NN                   | NN                           | NN       |
    | C5 Data & content for decisions           | NN                   | NN                           | NN       |
    | C6 Errors, edge cases, recovery           | NN                   | NN                           | NN       |
    | C7 Collaboration & concurrency            | NN                   | NN                           | NN       |
    | C8 Trust, transparency, audit             | NN                   | NN                           | NN       |
    | **Coverage of selected**                  | **—**                | **—**                        | **N of 8** |

    ### Quality gates

    | Gate | Result | Notes |
    |------|--------|-------|
    | 1. Exactly 10 questions in final output         | PASS / FAIL | {{flagged count}} |
    | 2. Candidate pool size ≤ 50                     | PASS / FAIL | {{actual size}} |
    | 3. All priorities ∈ {blocking, major, minor}    | PASS / FAIL | {{flagged}} |
    | 4. All rationales are 1–3 sentences, non-empty  | PASS / FAIL | {{flagged}} |
    | 5. All anchors valid or missing-section         | PASS / FAIL | {{flagged}} |
    | 6. No question matches an active GR-NN          | PASS / FAIL | {{matches}} |
    | 7. No question is out-of-scope                  | PASS / FAIL | {{matches}} |
    | 8. Category coverage ≥ 5 of 8                   | PASS / FAIL | {{categories represented}} |

    ### Override log

    {{If the consultant chose Override at the Step-6 quality-gate sweep,
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

- **Total questions:** {{TOTAL_QUESTIONS}}
  - Priority — Blocking: **{{BLOCKING_COUNT}}** · Major: **{{MAJOR_COUNT}}** · Minor: **{{MINOR_COUNT}}**
- **Candidate pool size:** {{CANDIDATE_POOL_SIZE}} (≤ 50)
- **Category coverage:** {{CATEGORY_COVERAGE}}

> Priority legend: **blocking** — without an answer, the design cannot proceed (two or more plausible interpretations yield contradictory designs). **major** — an answer materially changes design direction; design can proceed with a stated default at the cost of re-design risk. **minor** — answer affects refinement only; a reasonable default produces an acceptable design.

> Source: `requirements/requirements.md` only. Categories: C1 Users & segmentation · C2 Context of use · C3 Goals & success signals · C4 Tasks, flows, decision points · C5 Data & content for decisions · C6 Errors, edge cases, recovery · C7 Collaboration & concurrency · C8 Trust, transparency, audit.

---

## Triage

Read this table top-to-bottom; UXQ-01 is the highest-priority question. The full question text and rationale for each entry is in the **Questions** section below.

{{TRIAGE_BLOCK}}

---

## Questions

{{QUESTION_1_BLOCK}}

{{QUESTION_2_BLOCK}}

{{QUESTION_3_BLOCK}}

{{QUESTION_4_BLOCK}}

{{QUESTION_5_BLOCK}}

{{QUESTION_6_BLOCK}}

{{QUESTION_7_BLOCK}}

{{QUESTION_8_BLOCK}}

{{QUESTION_9_BLOCK}}

{{QUESTION_10_BLOCK}}

---

{{DIAGNOSTICS_BLOCK}}
