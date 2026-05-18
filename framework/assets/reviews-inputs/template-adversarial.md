<!--
  ROLE: asset (Markdown template). Populated by framework/agents/reviews-inputs/adversarial-reviewer.md.

  Purpose: Markdown skeleton for the Adversarial Review (inputs-side) report. Plain markdown
  (no HTML wrapper, no inlined CSS) so it renders in any markdown viewer and
  diffs cleanly in git. The reviewer substitutes the documented {{placeholders}}
  with HTML-escaped content (markdown special characters preserved in Evidence
  quotes are escaped per markdown rules — e.g. `|` inside a table cell becomes
  `\|`).

  Sibling template: framework/assets/reviews/template-adversarial.md — same structural
  shape, eight dimension blocks instead of seven, REQUIREMENTS_SHA256 instead of
  MANIFEST_FINGERPRINT, no Source-roster tables in the diagnostics block (because
  the requirements-doc reviewer has one input file, not a manifest).

  Placeholders the reviewer substitutes (string substitution, all values
  pre-escaped for markdown):

    {{TITLE}}                  — short title (e.g. "Adversarial Review (inputs-side) — Project X")
    {{DOMAIN}}                 — domain string (best-effort: from brief.docx §1 if a candidate
                                 source has a recognisable domain heading; otherwise "(not declared in inputs)")
    {{GENERATED_AT}}           — ISO-8601 UTC timestamp the artefact was rendered
    {{MANIFEST_FINGERPRINT}}   — sha256 of requirements/source-manifest.json at Step 2 read time
    {{REVIEWER_IDENTITY}}      — fixed string "Adversarial Review (BMAD-style, strict mode, inputs-side)"
    {{TOTAL_FINDINGS}}         — count of findings across all dimensions
    {{BLOCKER_COUNT}}          — count of Severity: Blocker
    {{MAJOR_COUNT}}            — count of Severity: Major
    {{MINOR_COUNT}}            — count of Severity: Minor
    {{PATCH_COUNT}}            — count of Disposition: Patch
    {{DEFER_COUNT}}            — count of Disposition: Defer
    {{REJECT_COUNT}}           — count of Disposition: Reject
    {{VERDICT}}                — one of BLOCKED | NEEDS-REVISION | ACCEPTED-WITH-FIXES
    {{TRIAGE_BLOCK}}           — pre-rendered "Top issues to address first" callout per TRIAGE BLOCK SCHEMA below
    {{CLUSTERS_BLOCK}}         — pre-rendered cluster summary per CLUSTERS BLOCK SCHEMA below
    {{FINDINGS_TABLE}}         — pre-rendered markdown table body (one row per finding) per FINDINGS TABLE SCHEMA below
    {{DIMENSION_1_BLOCK}}      — pre-rendered dimension section: either findings list or Justification block
    {{DIMENSION_2_BLOCK}}      — (likewise)
    {{DIMENSION_3_BLOCK}}
    {{DIMENSION_4_BLOCK}}
    {{DIMENSION_5_BLOCK}}
    {{DIMENSION_6_BLOCK}}
    {{DIMENSION_7_BLOCK}}
    {{DIAGNOSTICS_BLOCK}}      — pre-rendered diagnostics per DIAGNOSTICS SCHEMA below (includes Quality gates, Coverage map, Strict-BMAD re-run log, Override log, Source roster Consumed + Skipped tables)

  Output: reviews/inputs/ADVERSARIAL/adversarial-review.md.

  FINDINGS TABLE SCHEMA — each row the reviewer emits has the shape:

      | ADV-NN | D | Sev | Disp | CL-NN | filename | one-line problem |

    where:
      - ADV-NN is the finding ID (zero-padded sequence per run; assigned at Step 3b)
      - D is the Dimension integer 1..7
      - Sev is one of Blocker | Major | Minor
      - Disp is one of Patch | Defer | Reject
      - CL-NN is the cluster ID assigned at Step 3c, or blank for singletons (findings not grouped with any other finding)
      - filename is the Location field (manifest row's `filename` basename + extension)
      - one-line problem is the Problem field; pipe characters inside are escaped as \|

    Row order is severity-driven, not ID-driven:
      1. Sort key 1: Severity, descending — Blocker, then Major, then Minor.
      2. Sort key 2: Dimension, ascending (1..7).
      3. Sort key 3: within (Severity, Dimension), preserve the worker's emitted order (matches ADV-NN ascending within that bucket).
    ADV-NN IDs are unchanged by this sort — they retain the dimension-order × within-dimension-order
    assignment from Step 3b so audit trails that reference a specific ADV-NN still resolve.

  TRIAGE BLOCK SCHEMA — the {{TRIAGE_BLOCK}} contains a "Top issues to address first"
  callout (the outer "## Triage" heading is in the scaffold; the block body is just the table):

      Top issues to address first, ordered by severity. Resolve these before scanning the full
      Findings Table below.

      | Rank | ID | Severity | Cluster | Location | Problem |
      |------|----|----------|---------|----------|---------|
      | 1 | ADV-NN | Blocker | CL-NN | filename | one-line problem |
      | 2 | ADV-NN | ... | ... | ... | ... |

    Selection rule, applied deterministically:
      1. Every finding with Disposition = Reject (in ADV-NN ascending order).
      2. Every finding with Severity = Blocker not already included (in ADV-NN ascending order).
      3. If fewer than 10 entries so far, fill with Major findings that are the *lead* finding of a
         cluster (lowest ADV-NN within a cluster of size ≥3), ordered by cluster size descending,
         tie-broken by lead ADV-NN ascending.
      4. If still fewer than 10, fill with remaining Major findings in ADV-NN ascending order.
      5. Hard cap at 10 entries. Never fill with Minor findings (the consultant can scan the full
         table for minors). If total findings <10, render whatever exists; no padding.
    Rank column is the 1-based row index after sorting. Cluster column is blank for singletons.
    If zero findings exist run-wide, render the single line "No findings — strict-BMAD justification
    blocks below cover all seven dimensions." instead of the table.

  CLUSTERS BLOCK SCHEMA — the {{CLUSTERS_BLOCK}} contains a cluster summary (the outer
  "## Clusters" heading is in the scaffold; the block body is the prose line plus the table):

      Findings sharing a root cause are grouped below. Each cluster lists its member finding IDs;
      the per-dimension sections still contain every finding in full detail.

      | Cluster | Theme | Findings | Max severity |
      |---------|-------|----------|--------------|
      | CL-NN | one-line theme (e.g. "Finance Manager voice missing") | ADV-AA, ADV-BB, ADV-CC | Blocker |

    Cluster IDs are CL-01, CL-02, ... zero-padded, assigned at Step 3c in order of the lead
    (lowest ADV-NN) finding's ID. A cluster has ≥2 members; singletons are not clustered.
    Findings within a cluster are listed in ADV-NN ascending order. Max severity is the highest
    severity among the cluster's members (Blocker > Major > Minor).
    If Step 3c produced zero clusters, render the single line "No clusters — every finding stands
    on its own root cause." instead of the table.

  DIMENSION BLOCK SCHEMA — each {{DIMENSION_N_BLOCK}} contains either:

    Variant A — findings present (one or more):

        ### Findings

        #### ADV-NN — {{one-line-problem}}

        - **Severity:** Blocker | Major | Minor
        - **Disposition:** Patch | Defer | Reject
        - **Location:** {{filename}}
        - **Evidence:**
          > {{verbatim quote, ≤5 lines, as markdown blockquote — OR the literal
          >  `*(file skipped — tier: Unsupported; reason: <reason>)*` placeholder
          >  for Unsupported-tier findings in Dimension 1}}
        - **Problem:** {{one-sentence statement of the defect in the source material}}
        - **Recommendation:** {{one-sentence concrete elicitation action}}

        (repeat per finding within this dimension)

    Variant B — zero findings + strict-BMAD justification:

        ### Justification (zero findings — strict-BMAD re-run passed)

        {{≥3-sentence justification citing specific evidence (filenames, verbatim quotes,
          source-roster shape) and naming the anti-confirmation prompts attempted}}

  DIAGNOSTICS SCHEMA — the {{DIAGNOSTICS_BLOCK}} contains:

    ## Diagnostics

    ### Quality gates

    | Gate | Result | Notes |
    |------|--------|-------|
    | 1. All findings have 8 schema fields populated | PASS / FAIL | {{flagged item count}} |
    | 2. All Dimension fields are 1..7                | PASS / FAIL | {{...}} |
    | 3. All Severity fields are valid                | PASS / FAIL | {{...}} |
    | 4. All Disposition fields are valid             | PASS / FAIL | {{...}} |
    | 5. All Evidence quotes are verbatim & ≤5 lines (or sanctioned skipped placeholder) | PASS / FAIL | {{...}} |
    | 6. All Location anchors match a manifest filename (consumed or skipped)            | PASS / FAIL | {{...}} |
    | 7. Every dimension has ≥1 finding or Justification | PASS / FAIL | {{...}} |
    | 8. All Justifications are ≥3 sentences          | PASS / FAIL | {{...}} |
    | 9. Verdict matches disposition tally            | PASS / FAIL | {{...}} |
    | 10. Findings Table row count = per-dim sum      | PASS / FAIL | {{...}} |
    | 11. MANIFEST_FINGERPRINT + Source-roster sha256 prefixes match manifest | PASS / FAIL | {{...}} |

    ### Coverage map

    | Dimension | Filenames touched | Finding count |
    |-----------|-------------------|---------------|
    | 1. Stakeholder & Role Coverage                        | {{list}} | {{n}} |
    | 2. Domain & Workflow Coverage (incl. non-happy paths) | {{list}} | {{n}} |
    | 3. Ambiguity & Vague Language                         | {{list}} | {{n}} |
    | 4. Source Provenance, Consistency & Conflict          | {{list}} | {{n}} |
    | 5. Quantitative & Measurable Signal                   | {{list}} | {{n}} |
    | 6. Scope & MVP Signal                                 | {{list}} | {{n}} |
    | 7. Bias, Sampling & Stakeholder Self-Selection        | {{list}} | {{n}} |

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

    ### Source roster — Consumed

    | filename | tier | sha256 | findings-from-this-source |
    |----------|------|--------|---------------------------|
    | {{filename}} | {{tier}} | {{sha256[:8]}} | {{n}} |

    (one row per manifest row where tier != "Unsupported"; the n column is the
     count of findings whose Location field equals this filename)

    ### Source roster — Skipped

    | filename | reason |
    |----------|--------|
    | {{filename}} | {{conversion-failure-reason from manifest}} |

    (one row per manifest row where tier == "Unsupported"; if no Unsupported
     rows exist, render the single italic line "*(no sources skipped this run)*")

-->

# {{TITLE}}

- **Domain:** {{DOMAIN}}
- **Generated:** {{GENERATED_AT}}
- **Manifest fingerprint:** `{{MANIFEST_FINGERPRINT}}`
- **Reviewer:** {{REVIEWER_IDENTITY}}

---

## Executive Summary

- **Total findings:** {{TOTAL_FINDINGS}}
  - Severity — Blocker: **{{BLOCKER_COUNT}}** · Major: **{{MAJOR_COUNT}}** · Minor: **{{MINOR_COUNT}}**
  - Disposition — Patch: **{{PATCH_COUNT}}** · Defer: **{{DEFER_COUNT}}** · Reject: **{{REJECT_COUNT}}**
- **Verdict:** `{{VERDICT}}`

> Verdict legend: `BLOCKED` — at least one Reject or Blocker, `/requirements` cannot draft from these inputs as-is. `NEEDS-REVISION` — findings present but none blocking. `ACCEPTED-WITH-FIXES` — zero findings on all seven dimensions, every dimension carries a Justification block (rare under strict-BMAD).

---

## Triage

{{TRIAGE_BLOCK}}

---

## Clusters

{{CLUSTERS_BLOCK}}

---

## Findings Table

| ID | Dim | Severity | Disposition | Cluster | Location | Problem |
|----|-----|----------|-------------|---------|----------|---------|
{{FINDINGS_TABLE}}

---

## Dimension 1 — Stakeholder & Role Coverage

{{DIMENSION_1_BLOCK}}

---

## Dimension 2 — Domain & Workflow Coverage (including non-happy paths)

{{DIMENSION_2_BLOCK}}

---

## Dimension 3 — Ambiguity & Vague Language

{{DIMENSION_3_BLOCK}}

---

## Dimension 4 — Source Provenance, Consistency & Conflict

{{DIMENSION_4_BLOCK}}

---

## Dimension 5 — Quantitative & Measurable Signal

{{DIMENSION_5_BLOCK}}

---

## Dimension 6 — Scope & MVP Signal

{{DIMENSION_6_BLOCK}}

---

## Dimension 7 — Bias, Sampling & Stakeholder Self-Selection

{{DIMENSION_7_BLOCK}}

---

{{DIAGNOSTICS_BLOCK}}
