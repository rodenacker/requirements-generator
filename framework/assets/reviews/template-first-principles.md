<!--
  ROLE: asset (Markdown template). Populated by framework/agents/reviews/first-principles-reviewer.md.

  Purpose: Markdown skeleton for the First Principles review. Plain markdown
  (no HTML wrapper, no inlined CSS) so it renders in any markdown viewer and
  diffs cleanly in git. The reviewer substitutes the documented {{placeholders}}
  with HTML-escaped content (markdown special characters preserved in
  statements, evidence quotes, and reasoning lines; pipe characters inside
  table cells become `\|`).

  Placeholders the reviewer substitutes (string substitution, all values
  pre-escaped for markdown):

    {{TITLE}}                       — short title (e.g. "First Principles Review — Project X")
    {{DOMAIN}}                      — domain string (from requirements §1 if present, else "(not declared in requirements.md)")
    {{GENERATED_AT}}                — ISO-8601 UTC timestamp the artefact was rendered
    {{REQUIREMENTS_SHA256}}         — sha256 of requirements/requirements.md at read time
    {{REVIEWER_IDENTITY}}           — fixed string "First Principles Review (Aristotelian decomposition; 7-question defensibility audit)"
    {{TOTAL_SUBJECTS}}              — count of subjects rated (§4.1 + §4.2 + §6 + §7 numbered items)
    {{GOALS_COUNT}}                 — count of §4.1 goals rated
    {{STORIES_COUNT}}               — count of §4.2 stories rated
    {{REQUIREMENTS_COUNT}}          — count of §6 BR-NN + FR-NN rated
    {{ENTITIES_COUNT}}              — count of §7 entities rated
    {{SCORE_HISTOGRAM}}             — pre-rendered one-line histogram: "0: NN · 1: NN · 2: NN · 3: NN · 4: NN · 5: NN · 6: NN"
    {{TOP_TEN_SCORE_RANGE}}         — "min N/6 … max N/6" across the top-10 entries
    {{ORPHAN_COUNT}}                — count of Q7 coverage findings (orphans)
    {{ORPHAN_COUNT_BY_KIND}}        — one-line breakdown: "goal: NN · persona: NN · story: NN · business-rule: NN · entity: NN"
    {{CS_FINDINGS_COUNT}}           — count of cross-subject findings after Step-6 rescue and after post-scan consolidation (clusters with multiple lens-tags count as 1)
    {{CS_FINDINGS_BY_SEVERITY}}     — one-line breakdown: "blocking: NN · major: NN · minor: NN"
    {{CS_FINDINGS_BY_LENS}}         — one-line breakdown: "CS1: NN · CS2: NN · CS3: NN · CS4: NN · CS5: NN" (raw lens hits — sum may exceed CS_FINDINGS_COUNT if consolidation merged multi-lens findings)
    {{VERDICT}}                     — one of BLOCKED | NEEDS-REVISION | ACCEPTED-WITH-CONCERNS
    {{TOP_TEN_BLOCK}}               — pre-rendered deep-dive block per TOP-TEN BLOCK SCHEMA below
    {{RATINGS_TABLE}}               — pre-rendered ratings table per RATINGS TABLE SCHEMA below
    {{COVERAGE_FINDINGS_BLOCK}}     — pre-rendered orphan findings per COVERAGE BLOCK SCHEMA below
    {{CS_FINDINGS_BLOCK}}           — pre-rendered cross-subject findings per CS BLOCK SCHEMA below
    {{DIAGNOSTICS_BLOCK}}           — pre-rendered diagnostics per DIAGNOSTICS SCHEMA below

  Output: reviews/FIRST-PRINCIPLES/first-principles-review.md.

  TOP-TEN BLOCK SCHEMA — {{TOP_TEN_BLOCK}} is one heading per entry, in
  ascending-score order (lowest first), tie-broken by subject-type
  (entity → requirement → story → goal) then anchor ascending. Each entry:

      #### {{RANK}}. {{SUBJECT_ID}} — score {{SCORE}}/6 — weakest: {{WEAKEST_Q}}

      - **Type:** {{SUBJECT_TYPE}}
      - **Anchor:** {{ANCHOR}}
      - **Statement:**

      > {{STATEMENT_VERBATIM}}

      **Q1 — Why does this exist?** ({{Q1_ANSWER}})

      > {{Q1_EVIDENCE_OR_REASONING}}

      **Q2 — Which business goal does it support?** ({{Q2_ANSWER}})

      > {{Q2_EVIDENCE_OR_REASONING}}

      **Q3 — Which problem does it solve?** ({{Q3_ANSWER}})

      > {{Q3_EVIDENCE_OR_REASONING}}

      **Q4 — What operational outcome does it improve?** ({{Q4_ANSWER}})

      > {{Q4_EVIDENCE_OR_REASONING}}

      **Q5 — Is it the simplest valid way?** ({{Q5_ANSWER}})

      > {{Q5_EVIDENCE_OR_REASONING}}

      **Q6 — What happens if we remove it?** ({{Q6_ANSWER}})

      > {{Q6_CONSEQUENCE_PLUS_EVIDENCE}}

      **Recommended action:** {{ACTION}} — {{ACTION_RATIONALE}}

    Field rules:
      - {{RANK}} is 1..10 (1-based), in ascending-score order.
      - {{SUBJECT_ID}} is the runtime-assigned ID (`G-NN | US-NN | BR-NN | FR-NN | EN-NN`).
      - {{SCORE}} is integer 0..6.
      - {{WEAKEST_Q}} is one of `Q1 | Q2 | Q3 | Q4 | Q5 | Q6`.
      - {{SUBJECT_TYPE}} is one of `goal | story | requirement | entity`.
      - {{ANCHOR}} is the section / persona / position anchor (e.g. `§4.1 / G-04`,
        `§4.2 / Approver / story #1`, `§6 / FR-12`, `§7 / FileSetting`).
      - {{STATEMENT_VERBATIM}} is the subject's verbatim text as a markdown
        blockquote (`>` prefix each line).
      - Each Q-answer label is one of `yes-with-evidence | partial | no`.
      - The block following each Q-heading is a markdown blockquote:
          - For `yes-with-evidence`: the verbatim evidence quote (≤5 lines).
          - For `partial` or `no`: the reasoning line (1–2 sentences).
          - For Q6: the consequence-of-removal sentence + the cited quote on
            the next line.
        Pipe characters inside any blockquote line are NOT escaped (we are
        not in a table); they are preserved verbatim. Markdown special
        characters inside the verbatim quote are preserved.
      - For Q5 specifically: if the answer was filter-rescued to
        `yes-with-evidence` by a `GR-NN` or `PI-NN` match, the label reads
        `yes-with-evidence (GR-NN rescue)` or `yes-with-evidence (PI-NN rescue)`
        and the blockquote names the active rule.
      - {{ACTION}} is one of `re-anchor | re-scope | remove | merge | clarify`.
      - {{ACTION_RATIONALE}} is 1 sentence.
      - One blank line between entries.

    If `|subjects| < 10`, the block renders fewer entries (exactly `|subjects|`).
    If `|subjects| == 0`, substitute the single line
    `_No subjects to rate — §4–§7 are empty. The First Principles audit has nothing to evaluate._`.

  RATINGS TABLE SCHEMA — {{RATINGS_TABLE}} is a single markdown table listing
  every subject in the same ascending-score sort order as the Top-10:

      | Rank | ID | Type | Anchor | Score | Weakest | Statement (truncated) | Recommended action |
      |------|----|------|--------|-------|---------|-----------------------|--------------------|
      | 1    | EN-03 | entity      | §7 / FileSetting        | 0/6 | Q1 | FileSetting — stores per-file config rows … | remove |
      | 2    | FR-19 | requirement | §6 / FR-19              | 1/6 | Q1 | The system shall expose a settings panel … | re-anchor |
      | 3    | G-04  | goal        | §4.1 / G-04             | 2/6 | Q2 | Improve back-office throughput …            | clarify |
      | ...

    Field rules:
      - Rank is the 1-based position in the ascending-score sort. Top-10
        entries are ranks 1..10; the full ratings table continues to N for
        |subjects| > 10.
      - ID, Type, Anchor as for the Top-10 block.
      - Score is integer 0..6, rendered as `N/6`.
      - Weakest is one of `Q1 | Q2 | Q3 | Q4 | Q5 | Q6`.
      - Statement (truncated) is the subject's verbatim text trimmed to ≤80
        characters with a trailing ellipsis if truncated. Markdown special
        characters inside are NOT escaped except pipes (which become `\|`)
        because the cell is a table cell.
      - Recommended action is one of the five canonical actions.
      - Pipe characters inside any cell are escaped as `\|`.

    If `|subjects| == 0`, render the single row
    `| — | — | — | — | — | — | _No subjects rated — §4–§7 empty._ | — |`.

  COVERAGE BLOCK SCHEMA — {{COVERAGE_FINDINGS_BLOCK}} is one heading per
  orphan, in coverage-relation order (orphan-goal → orphan-persona →
  orphan-story → orphan-business-rule → orphan-entity), within each
  category by anchor ascending. Each finding:

      ### {{ORPHAN_KIND}} — {{ANCHOR}}

      - **Severity:** blocking
      - **Anchor:** {{ANCHOR}}
      - **Expected counterpart:** {{EXPECTED_COUNTERPART}}
      - **Consequence:** {{CONSEQUENCE_SENTENCE}}

    Field rules:
      - {{ORPHAN_KIND}} is one of `orphan-goal | orphan-persona | orphan-story
        | orphan-business-rule | orphan-entity`.
      - {{ANCHOR}} as for the Top-10 block.
      - {{EXPECTED_COUNTERPART}} is a one-line statement of what is missing
        (e.g. *"no §6 requirement traces to this goal"*, *"no §4.2 story uses
        this persona as actor"*).
      - {{CONSEQUENCE_SENTENCE}} is one sentence explaining what fixing the
        orphan looks like (*"adding a requirement that delivers G-04, or
        striking G-04 from §4.1"*).
      - One blank line between findings.

    If `{{ORPHAN_COUNT}} == 0`, substitute the single line
    `_No orphans — every goal has a requirement, every persona has a story, every story has a requirement, every business rule has a functional realisation, every entity is used by a requirement._`.

    For any coverage relation that is `not-applicable` (e.g. no §7 entities
    exist in the doc, so the entity-coverage check is vacuous), the
    diagnostics block records the relation as `not-applicable` and the
    coverage findings section does not list orphans for that relation.

  CS BLOCK SCHEMA — {{CS_FINDINGS_BLOCK}} is one heading per finding (or
  per consolidated cluster), in severity-then-lens-then-anchor order
  (blocking > major > minor; CS1 → CS2 → CS3 → CS4 → CS5; first anchor
  ascending). Each finding renders as:

      ### {{LENS_TAGS}} — {{SEVERITY}} — {{HEADLINE}}

      - **Lenses:** {{LENS_TAGS_EXPANDED}}
      - **Severity:** {{SEVERITY}}
      - **Anchors:**
        - {{ANCHOR_1}}
        - {{ANCHOR_2}}
        - …

      **Evidence:**

      > {{ANCHOR_1}}: {{QUOTE_1_VERBATIM}}

      > {{ANCHOR_2}}: {{QUOTE_2_VERBATIM}}

      > …

      **Relation:** {{RELATION_SENTENCE}}

      **Consequence:** {{CONSEQUENCE_SENTENCE}}

    Field rules:
      - {{LENS_TAGS}} is one or more of `CS1 | CS2 | CS3 | CS4 | CS5`,
        joined by `+` if the consolidation pass merged multiple lenses on
        the same anchor set (e.g. `CS1+CS3+CS5`).
      - {{LENS_TAGS_EXPANDED}} is the human-readable list with names
        (e.g. *"CS1 (Contradictory Objectives), CS3 (Missing System
        Thinking)"*).
      - {{SEVERITY}} is one of `blocking | major | minor`. For a multi-
        lens cluster, severity is the max across cluster members
        (blocking > major > minor).
      - {{HEADLINE}} is a short noun-phrase summary the reviewer composes
        (≤8 words, no prescriptive verbs).
      - {{ANCHOR_N}} is a §-anchor from the Step-2 anchor index
        (`§4.1 / G-04`, `§6 / FR-12`, `§7 / FileSetting`, etc.). For
        relational lenses (CS1, CS3) there are ≥2 anchors; for others ≥1.
      - {{QUOTE_N_VERBATIM}} is a verbatim substring of
        `requirements/requirements.md` (≤3 lines per quote), prefixed
        with `> ` to render as a blockquote. The leading `{{ANCHOR_N}}: `
        is reviewer prose, not part of the quote.
      - For a multi-lens cluster, the **Relation** and **Consequence**
        lines repeat per lens, each prefixed with the lens tag
        (e.g. `**Relation (CS1):**`, `**Relation (CS3):**`, etc.).
      - {{RELATION_SENTENCE}} is one sentence stating what the cited
        anchors collectively show.
      - {{CONSEQUENCE_SENTENCE}} is one sentence stating the outcome
        the doc as written cannot deliver. Observational verbs only —
        prescriptive verbs (`add`, `include`, `specify`, `define`,
        `require`, `mandate`, `must`, `should`) fail gate 13.
      - One blank line between findings.

    If {{CS_FINDINGS_COUNT}} == 0, substitute the single line
    `_No cross-subject coherence findings — the doc's §4–§7 subjects, taken together, do not exhibit contradictions, hidden assumptions, system-thinking gaps, operational-reality omissions, or human-cost allocation issues that exceed Step-6 GR-NN / PI-NN rescues._`.

  DIAGNOSTICS SCHEMA — the {{DIAGNOSTICS_BLOCK}} contains:

    ## Diagnostics

    ### Subject counts

    | Stat | Value |
    |------|-------|
    | Subjects rated (total)              | NN |
    | §4.1 goals rated                    | NN |
    | §4.2 stories rated                  | NN |
    | §6 requirements rated (BR + FR)     | NN |
    | §7 entities rated                   | NN |

    ### Score histogram

    | Score | Count |
    |-------|-------|
    | 0/6   | NN |
    | 1/6   | NN |
    | 2/6   | NN |
    | 3/6   | NN |
    | 4/6   | NN |
    | 5/6   | NN |
    | 6/6   | NN |

    ### Weakest-question distribution

    | Question | Count |
    |----------|-------|
    | Q1 (Why does this exist?)                 | NN |
    | Q2 (Which business goal?)                 | NN |
    | Q3 (Which problem?)                       | NN |
    | Q4 (What operational outcome?)            | NN |
    | Q5 (Simplest valid way?)                  | NN |
    | Q6 (What if we remove it?)                | NN |

    ### Coverage pass (Q7)

    | Coverage relation                                    | Result | Orphans |
    |------------------------------------------------------|--------|---------|
    | Every §4.1 goal has ≥1 §6 requirement                | PASS / FAIL / N-A | NN |
    | Every §3 persona has ≥1 §4.2 story                   | PASS / FAIL / N-A | NN |
    | Every §4.2 story has ≥1 §6 requirement               | PASS / FAIL / N-A | NN |
    | Every §6 BR-NN has ≥1 §6 FR-NN                       | PASS / FAIL / N-A | NN |
    | Every §7 entity has ≥1 §6 requirement reader/writer  | PASS / FAIL / N-A | NN |

    ### Cross-subject pass (CS1–CS5)

    | Lens | Result | Findings | Rescued | Highest severity |
    |------|--------|----------|---------|------------------|
    | CS1 (Contradictory Objectives)                         | PASS / FAIL | NN | NN | blocking / major / minor / — |
    | CS2 (Hidden Assumptions / False Constraints)           | PASS / FAIL | NN | NN | blocking / major / minor / — |
    | CS3 (Missing System Thinking / Arch Consequence)       | PASS / FAIL | NN | NN | blocking / major / minor / — |
    | CS4 (Missing Operational Reality)                      | PASS / FAIL | NN | NN | blocking / major / minor / — |
    | CS5 (Human Cost Allocation)                            | PASS / FAIL | NN | NN | blocking / major / minor / — |

    `Result` is PASS when the lens ran and emitted 0..N findings (zero
    is fine); FAIL when the lens was silently skipped. `Findings` is the
    post-rescue, post-consolidation count attributed to this lens
    (cluster findings count under every lens-tag they carry). `Rescued`
    is the count of findings dropped by GR-NN / PI-NN at Step 6. The
    `Highest severity` is `—` if Findings == 0.

    ### Filter drops & rescues

    | Filter source | Q3/Q5 drops | Q3/Q5 rescues | CS rescues |
    |---------------|-------------|---------------|------------|
    | GR-NN match (Step 6 rule 1)     | NN | NN | NN |
    | PI-NN match (Step 6 rule 2)     | NN | NN | NN |

    A "Q3/Q5 rescue" is a Q3 or Q5 `no` re-marked to `yes-with-evidence`
    because an active `GR-NN` or `PI-NN` foreclosed the underlying
    premise; the rescue adds 1 to the affected subject's score. A "CS
    rescue" is a CS2 / CS4 / CS5 finding dropped because the underlying
    premise is foreclosed by an active `GR-NN` or `PI-NN`; CS rescues
    have no score effect (CS findings have severity, not score).

    ### Quality gates

    | Gate | Result | Notes |
    |------|--------|-------|
    | 1. Every §4–§7 subject was rated                              | PASS / FAIL | {{evaluated}}/{{enumerated}} |
    | 2. Every rating has all six Q1–Q6 answers                     | PASS / FAIL | {{flagged}} |
    | 3. Every `yes-with-evidence` carries a verbatim quote          | PASS / FAIL | {{flagged}} |
    | 4. Every `partial`/`no` carries a reasoning line               | PASS / FAIL | {{flagged}} |
    | 5. Every score ∈ integer {0..6}                                | PASS / FAIL | {{flagged}} |
    | 6. Every weakest-question marker ∈ {Q1..Q6}                    | PASS / FAIL | {{flagged}} |
    | 7. Top-10 list has min(10, \|subjects\|) entries, sort order   | PASS / FAIL | {{flagged}} |
    | 8. Coverage pass evaluated every layer                         | PASS / WARN / FAIL | {{not-applicable layers}} |
    | 9. Every orphan finding cites anchor + expected counterpart    | PASS / FAIL | {{flagged}} |
    | 10. Verdict line matches score, orphan counts, CS blocking     | PASS / FAIL | {{flagged}} |
    | 11. REQUIREMENTS_SHA256 matches Step-2 capture                 | PASS / FAIL | {{actual sha}} |
    | 12. Every CS finding's anchors resolve; quotes are verbatim     | PASS / FAIL | {{flagged}} |
    | 13. Every CS consequence uses observational verbs only          | PASS / FAIL | {{flagged}} |
    | 14. Every CS lens (CS1–CS5) was evaluated                       | PASS / FAIL | {{flagged}} |

    ### Override log

    {{If the consultant chose Override at the Step-8 quality-gate sweep, or
       if gate 8 fired its `warn` and the consultant chose to proceed, list
       each gate by number with the items flagged. Otherwise write
       "All quality gates passed; no override invoked."}}

-->

# {{TITLE}}

- **Domain:** {{DOMAIN}}
- **Generated:** {{GENERATED_AT}}
- **Requirements SHA-256:** `{{REQUIREMENTS_SHA256}}`
- **Reviewer:** {{REVIEWER_IDENTITY}}

---

## Executive Summary

- **Subjects rated:** {{TOTAL_SUBJECTS}}
  - Goals (§4.1): **{{GOALS_COUNT}}** · Stories (§4.2): **{{STORIES_COUNT}}** · Requirements (§6): **{{REQUIREMENTS_COUNT}}** · Entities (§7): **{{ENTITIES_COUNT}}**
- **Score histogram (out of 6):** {{SCORE_HISTOGRAM}}
- **Top 10 score range:** {{TOP_TEN_SCORE_RANGE}}
- **Orphans (Q7 coverage):** **{{ORPHAN_COUNT}}** — {{ORPHAN_COUNT_BY_KIND}}
- **Cross-subject findings (CS1–CS5):** **{{CS_FINDINGS_COUNT}}** — {{CS_FINDINGS_BY_SEVERITY}} — by lens: {{CS_FINDINGS_BY_LENS}}
- **Verdict:** **{{VERDICT}}**

> Verdict legend: **BLOCKED** — at least one orphan-goal, at least one `0/6` score, three-plus `≤2/6` scores, or at least one `blocking` cross-subject finding. **NEEDS-REVISION** — Top-10 contains any `≤3/6` score but no blocking triggers. **ACCEPTED-WITH-CONCERNS** — Top-10 minimum `≥4/6`, zero orphans, and no `blocking` cross-subject findings. Major and minor cross-subject findings do not block this verdict — they appear in the summary count for triage. First Principles never accepts unconditionally — the Top-10 always merits a look.

> Source: `requirements/requirements.md` only. Subjects: every numbered item in §4.1, §4.2, §6, §7. Questions: Q1 *Why does this exist?* · Q2 *Which business goal?* · Q3 *Which problem?* · Q4 *What operational outcome?* · Q5 *Simplest valid way?* · Q6 *What if we remove it?* · Q7 *Anything critical missing?* (coverage pass). Scoring: count of `yes-with-evidence` answers across Q1–Q6 (0–6 integer). Cross-subject lenses CS1–CS5 audit collective coherence across the requirement set; findings carry severity, not score.

---

## Top 10 Least Defensible

Subjects with the weakest evidence-grounded justification chain, in ascending-score order (lowest first). Each entry deep-dives every Q1–Q6 answer with the verbatim evidence (or absence-reasoning) that produced the score.

{{TOP_TEN_BLOCK}}

---

## Full defensibility ratings

Every rated subject, in the same ascending-score sort order. Use this table to see the full distribution and to spot-check whether the entries just outside the Top-10 are clustered close to the cut.

{{RATINGS_TABLE}}

---

## Critical missing artefacts

Q7 coverage findings. Each is a `blocking` orphan: an artefact that exists at one layer of the doc and should have a counterpart at another but doesn't.

{{COVERAGE_FINDINGS_BLOCK}}

---

## Cross-subject coherence findings

CS1–CS5 findings. Each cites ≥1 anchor in the doc and observes a relation the subjects collectively cannot satisfy: a contradiction between objectives, a hidden assumption or false constraint, a system-thinking or architectural-consequence gap, a missing operational reality, or a human-cost allocation problem. Findings carry severity (blocking / major / minor) rather than a per-subject score, and consequence sentences observe what the doc as written cannot deliver — they never prescribe what to add.

{{CS_FINDINGS_BLOCK}}

---

{{DIAGNOSTICS_BLOCK}}
