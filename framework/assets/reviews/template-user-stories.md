<!--
  ROLE: asset (Markdown template). Populated by framework/agents/reviews/user-stories-reviewer.md.

  Purpose: Markdown skeleton for the User Stories review. Plain markdown
  (no HTML wrapper, no inlined CSS) so it renders in any markdown viewer and
  diffs cleanly in git. The reviewer substitutes the documented {{placeholders}}
  with HTML-escaped content (markdown special characters preserved in story
  text, reasons, and fixes; pipe characters inside table cells become `\|`).

  Placeholders the reviewer substitutes (string substitution, all values
  pre-escaped for markdown):

    {{TITLE}}                       — short title (e.g. "User Stories Review — Project X")
    {{DOMAIN}}                      — domain string (from requirements §1 if present)
    {{GENERATED_AT}}                — ISO-8601 UTC timestamp the artefact was rendered
    {{REQUIREMENTS_SHA256}}         — sha256 of requirements/requirements.md at read time
    {{REVIEWER_IDENTITY}}           — fixed string "User Stories Review (product-owner / BA lens; six-criterion story-quality audit)"
    {{TOTAL_STORIES}}               — total number of stories enumerated in §4.2
    {{PASS_COUNT}}                  — stories that passed all six criteria (no surviving issues)
    {{FAIL_COUNT}}                  — stories with one or more surviving issues (findings)
    {{BLOCKING_COUNT}}              — findings with headline_priority = blocking
    {{MAJOR_COUNT}}                 — findings with headline_priority = major
    {{MINOR_COUNT}}                 — findings with headline_priority = minor
    {{PERSONA_LIST}}                — comma-separated list of personas under §4.2 (in document order)
    {{CRITERION_COVERAGE}}          — "N of 6 (criterion-list)" where criterion-list is the comma-separated names of criteria with at least one surviving issue
    {{TRIAGE_BLOCK}}                — pre-rendered triage table per TRIAGE BLOCK SCHEMA below
    {{BLOCKING_FINDINGS_BLOCK}}     — pre-rendered findings for headline_priority = blocking (or "_None._")
    {{MAJOR_FINDINGS_BLOCK}}        — pre-rendered findings for headline_priority = major (or "_None._")
    {{MINOR_FINDINGS_BLOCK}}        — pre-rendered findings for headline_priority = minor (or "_None._")
    {{DIAGNOSTICS_BLOCK}}           — pre-rendered diagnostics per DIAGNOSTICS SCHEMA below

  Output: review-requirements/USER-STORIES/user-stories-review.md.

  TRIAGE BLOCK SCHEMA — {{TRIAGE_BLOCK}} is a single markdown table listing
  every finding in sort order (priority → persona → anchor):

      | Priority | Story | Persona | Anchor | Criteria violated |
      |----------|-------|---------|--------|-------------------|
      | blocking | US-04 | Approver | §4.2 / Approver / story #1 | Testable, Scoped |
      | major    | US-01 | Importer | §4.2 / Importer / story #1 | Outcome-aligned |
      | ...

    Field rules:
      - Priority is one of `blocking | major | minor` (lowercase, no decoration); this is the headline priority of the finding.
      - Story is the runtime-assigned ID `US-NN` (zero-padded; numbered in document order across §4.2).
      - Persona is the persona name from the §4.2 `####` heading the story sits under.
      - Anchor is `§4.2 / {Persona} / story #{N}` where {N} is the 1-based position of the story under that persona.
      - Criteria violated is the comma-separated list of distinct criteria with surviving issues for the story, in reference order (Meaningful → Implementable → Testable → Coherent → Scoped → Outcome-aligned).
      - Pipe characters inside any cell are escaped as `\|`.
      - If there are zero findings, render `| — | — | — | — | — |` in a single data row and add a note above the table: "_All stories passed all six criteria. See Diagnostics for counts._".

  FINDING BLOCK SCHEMA — each finding inside a priority section contains:

      ### {{STORY_ID}} — {{HEADLINE_PRIORITY}} — {{PERSONA}}

      > {{CONNEXTRA_TEXT}}

      **Issues**

      - **{{CRITERION}}** ({{SEVERITY}}): {{REASON}}
        - *Fix*: {{FIX}}
      - **{{CRITERION}}** ({{SEVERITY}}): {{REASON}}
        - *Fix*: {{FIX}}
      - ...

      *Anchor*: §4.2 / {{PERSONA}} / story #{{N}}

    Field rules:
      - Heading line uses em-dashes (—), not hyphens, as separators.
      - {{STORY_ID}} is `US-NN`, zero-padded.
      - {{HEADLINE_PRIORITY}} is the lowercase label (blocking | major | minor) — max severity across the finding's issues.
      - {{PERSONA}} is the persona name from the §4.2 `####` heading.
      - {{CONNEXTRA_TEXT}} is rendered as a markdown blockquote (`>` prefix). Verbatim from the story's `##### Story:` heading text; markdown special characters inside the story text are preserved.
      - Issues are sorted within the finding by severity descending (blocking issues first within the finding), then by criterion-order in the reference.
      - Each issue line uses **bolded criterion name** followed by `(severity)` in plain parentheses, then a colon, then the reason. Reason is 1–3 sentences of plain prose.
      - The nested `- *Fix*: …` bullet under each issue carries a directional hint (1–2 sentences). Italicised `Fix` keyword; no boldface on the fix text itself.
      - The `*Anchor*: …` line is the last line of the finding block; italicised `Anchor` keyword.
      - Blank line between findings.

  DIAGNOSTICS SCHEMA — the {{DIAGNOSTICS_BLOCK}} contains:

    ## Diagnostics

    ### Story counts

    | Stat | Value |
    |------|-------|
    | Stories enumerated in §4.2          | NN |
    | Stories evaluated                   | NN |
    | Stories passing all six criteria    | NN |
    | Stories with findings               | NN |
    | Findings — blocking                 | NN |
    | Findings — major                    | NN |
    | Findings — minor                    | NN |

    ### Per-criterion failure counts

    Counts of surviving issues by criterion (a single story may contribute to multiple criteria):

    | Criterion          | Surviving issues |
    |--------------------|------------------|
    | Meaningful         | NN |
    | Implementable      | NN |
    | Testable           | NN |
    | Coherent           | NN |
    | Scoped             | NN |
    | Outcome-aligned    | NN |
    | **Criterion coverage** | **N of 6** |

    ### Filter drops

    | Filter source | Drops |
    |---------------|-------|
    | GR-NN match (Step 4 rule 1)     | NN |
    | PI-NN match (Step 4 rule 2)     | NN |
    | Scope filter (not applied)      | — (every §4.2 story is in-scope by definition) |
    | UX-lens drop (not applied)      | — (criteria are orthogonal to UX/BA framing) |

    ### Quality gates

    | Gate | Result | Notes |
    |------|--------|-------|
    | 1. Every §4.2 story was evaluated                       | PASS / FAIL | {{evaluated}}/{{enumerated}} |
    | 2. Every finding has all required fields                | PASS / FAIL | {{flagged}} |
    | 3. Every issue has all required fields                  | PASS / FAIL | {{flagged}} |
    | 4. No issue cites a criterion outside the six           | PASS / FAIL | {{flagged}} |
    | 5. No issue foreclosed by GR-NN or PI-NN                | PASS / FAIL | {{matches}} |
    | 6. Headline priority = max issue severity per finding   | PASS / FAIL | {{flagged}} |
    | 7. Sort order: priority → persona → anchor              | PASS / FAIL | {{flagged}} |
    | 8. Criterion coverage ≥ 4 of 6                          | PASS / WARN | {{criteria represented}} |
    | 9. Diagnostics block reports all required fields        | PASS / FAIL | {{flagged}} |

    ### Override log

    {{If the consultant chose Override at the Step-6 quality-gate sweep, or
       if gate 8 fired its narrow-review WARN and the consultant chose to
       proceed, list each gate by number with the items flagged. Otherwise
       write "All quality gates passed; no override invoked."}}

-->

# {{TITLE}}

- **Domain:** {{DOMAIN}}
- **Generated:** {{GENERATED_AT}}
- **Requirements SHA-256:** `{{REQUIREMENTS_SHA256}}`
- **Reviewer:** {{REVIEWER_IDENTITY}}

---

## Executive Summary

- **Stories evaluated:** {{TOTAL_STORIES}}
- **Stories passing all six criteria:** {{PASS_COUNT}}
- **Stories with findings:** {{FAIL_COUNT}}
  - Priority — Blocking: **{{BLOCKING_COUNT}}** · Major: **{{MAJOR_COUNT}}** · Minor: **{{MINOR_COUNT}}**
- **Personas covered:** {{PERSONA_LIST}}
- **Criterion coverage:** {{CRITERION_COVERAGE}}

> Priority legend: **blocking** — the story cannot be built, tested, or accepted as written. **major** — the story is buildable but ambiguous; multiple correct implementations are possible. **minor** — refinement opportunity; a reasonable interpretation produces an acceptable story.

> Source: `requirements/requirements.md > §4.2 Stories by persona` only. Criteria: Meaningful · Implementable · Testable · Coherent · Appropriately scoped · Outcome-aligned. Passing stories are recorded in Diagnostics but not surfaced in the body.

---

## Triage

Read this table top-to-bottom; findings are sorted by priority (blocking → major → minor), then by persona, then by anchor. The full reason and fix suggestion for each entry is in the corresponding **Blocking / Major / Minor** section below.

{{TRIAGE_BLOCK}}

---

## Blocking ({{BLOCKING_COUNT}})

{{BLOCKING_FINDINGS_BLOCK}}

---

## Major ({{MAJOR_COUNT}})

{{MAJOR_FINDINGS_BLOCK}}

---

## Minor ({{MINOR_COUNT}})

{{MINOR_FINDINGS_BLOCK}}

---

{{DIAGNOSTICS_BLOCK}}
