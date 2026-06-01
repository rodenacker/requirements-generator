# Ambiguity Review (inputs-side)

| Field | Value |
|---|---|
| Generated-At | 2026-05-30T12:31:45Z |
| MANIFEST_FINGERPRINT | `b460d2680e5dc32866c0f881fc7a84f76ff60db425ffa02be8c1afdae14589e9` |
| Sources Consumed | 1 |
| Sources Skipped | 0 |
| Reviewer Identity | Ambiguity Review (Berry/Kamsties + Femmer, seven-dimension, inputs-side) |

---

## Executive Summary

**Total findings: 11** — Blocker: **1**, Major: **8**, Minor: **2**.

Per-dimension counts (by primary dimension):

| Dim | Name | Findings |
|---|---|---|
| 1 | Lexical ambiguity | 3 |
| 2 | Syntactic ambiguity | 1 |
| 3 | Referential ambiguity | 0 (Justification) |
| 4 | Vague predicates | 4 |
| 5 | Subjective qualifiers | 2 |
| 6 | Weak / non-specific verbs | 0 (consolidated → Justification) |
| 7 | Optionality + agentless passive | 1 |

Two multi-tag findings span ≥2 dimensions: **AMB-05** `[4, 6]` and **AMB-10** `[5, 6]`. Every Dimension-6 hit overlapped a vague-predicate or subjective span and consolidated under its lowest-dimension primary, so Dimension 6 carries a Justification block rather than standalone findings.

**Verdict: `BLOCKED`** — at least one Blocker-severity finding (AMB-05) will cause divergent implementation if it reaches `/requirements` unresolved.

---

## Triage — top issues to address first

9 entries (every Blocker, then multi-dimension Majors, then remaining Majors; Minors excluded):

1. **AMB-05** (Blocker, `[4, 6]`) — "shift most … verification … activities to a self-service digital experience": does the app authenticate identity or only collect documents, and which activities stay advisor-led?
2. **AMB-10** (Major, `[5, 6]`) — acceptance criterion "feeling confident … handling … professionally and responsibly": how is it verified and what data operations are in scope?
3. **AMB-01** (Major, dim 1) — "investment profile" vs "risk profile": same object or different?
4. **AMB-02** (Major, dim 1) — "session": carries an identifier, or is it just localStorage data?
5. **AMB-03** (Major, dim 1) — "Funding source" (Student) vs "Source of Funds": one field or two?
6. **AMB-04** (Major, dim 2) — "required for KYC and suitability assessments": does the app perform the suitability assessment or just collect its inputs?
7. **AMB-06** (Major, dim 4) — "20 most common countries": common by what measure?
8. **AMB-08** (Major, dim 4) — "Validation consistent across steps": same rules per field, or uniform timing/UX?
9. **AMB-09** (Major, dim 5) — "professional, trustworthy, and secure experience": real security controls or perceived-security UI?

---

## Source roster

### Consumed

| filename | tier | sha256[:8] | findings |
|---|---|---|---|
| brief.md | Native-text | `538fd17d` | 11 |

### Skipped

*(no sources skipped this run)*

---

## Findings table

| ID | Dim(s) | Sev | Location | Problem (one line) |
|---|---|---|---|---|
| AMB-05 | [4, 6] | Blocker | brief.md | "shift most … verification … activities" leaves the verification operation (dim 6) and the "most" remainder (dim 4) undefined — app authenticates identity or only collects documents? |
| AMB-01 | [1] | Major | brief.md | "investment profile" (Overview) vs "risk profile" (Step 5) — same object, or a broader Step 4–5 bundle? |
| AMB-02 | [1] | Major | brief.md | "session" — a localStorage data blob, or an identified onboarding instance with a session ID? |
| AMB-03 | [1] | Major | brief.md | Student "Funding source" vs the main "Source of Funds" dropdown — one field or two? |
| AMB-04 | [2] | Major | brief.md | "required for KYC and suitability assessments" — coordination scope: app performs the assessment or only collects its inputs? |
| AMB-06 | [4] | Major | brief.md | "the 20 most common countries" — no measure given for "common". |
| AMB-08 | [4] | Major | brief.md | "Validation consistent across steps" — identical rules per repeated field, or uniform validation timing/UX? |
| AMB-09 | [5] | Major | brief.md | "professional, trustworthy, and secure experience" — real security controls vs perceived-security UI, judged against what? |
| AMB-10 | [5, 6] | Major | brief.md | Acceptance criterion "feeling confident … handling … professionally and responsibly" — untestable as written (dim 5) + non-specific "handling" (dim 6). |
| AMB-07 | [4] | Minor | brief.md | "short explanation" — no length bound for the per-step copy. |
| AMB-11 | [7] | Minor | brief.md | "should communicate professionalism, transparency, and care" — modal strength (MUST vs SHOULD) ambiguous. |

---

## Per-dimension sections

### Dimension 1 — Lexical ambiguity

- **AMB-01** — Severity: `Major` — Location: `brief.md` — Dimensions: `[1]`
  - Evidence: > allowing clients to submit their personal information, supporting documentation, and investment profile before their appointment.
  - Interpretations:
    (a) "investment profile" denotes exactly the Step 5 risk-profile result (risk category + score) and nothing more.
    (b) "investment profile" denotes the combined financial picture — employment, source of funds, income bracket, AND risk tolerance — i.e. everything from Steps 4–5.
    (c) "investment profile" is a distinct, not-yet-specified data object separate from both.
  - Problem: brief.md uses "investment profile" (Overview) and "risk profile" (Step 5) without stating whether they denote the same object, so the data set submitted and displayed is undefined.
  - Elicitation question: In brief.md, does "investment profile" refer only to the Step 5 risk-profile result, or does it also include the Step 4 employment and source-of-funds data?

- **AMB-02** — Severity: `Major` — Location: `brief.md` — Dimensions: `[1]`
  - Evidence: > * Begin onboarding
    > * Create onboarding session
    > * Store session locally for resumption
  - Interpretations:
    (a) "session" = a client-side data blob in localStorage holding form progress; there is no session identifier or server record.
    (b) "session" = a uniquely identified onboarding instance (with a generated session ID) that the resume flow and mock endpoint key off.
  - Problem: brief.md uses "session" for the resumable-onboarding construct without defining whether it carries an identifier or is purely a localStorage data blob, leaving the data model and resume key undefined.
  - Elicitation question: In brief.md, does an onboarding "session" include a generated session identifier, or is it solely the form data persisted in localStorage?

- **AMB-03** — Severity: `Major` — Location: `brief.md` — Dimensions: `[1]`
  - Evidence: > #### Student
    > * Institution name
    > * Funding source
  - Interpretations:
    (a) The Student "Funding source" field is the same control as the main Step 4 "Source of Funds" dropdown (Salary / Savings / Inheritance / …).
    (b) "Funding source" is a separate, student-specific field (e.g. loan, scholarship, family support) distinct from "Source of Funds".
  - Problem: brief.md uses "Funding source" (Student) and "Source of Funds" (all applicants) without stating whether they are one field or two, so the conditional data model is undefined.
  - Elicitation question: In brief.md, is the Student "Funding source" field the same dropdown as the main "Source of Funds" field, or a separate student-specific field with its own options?

### Dimension 2 — Syntactic ambiguity

- **AMB-04** — Severity: `Major` — Location: `brief.md` — Dimensions: `[2]`
  - Evidence: > Collect all information required for KYC and suitability assessments before advisor review.
  - Interpretations:
    (a) Parse: collect [all information required for {KYC and suitability assessments}] — the system only gathers input data; the assessments themselves are performed later by the advisor.
    (b) Parse: collect [all information required for KYC] and [perform suitability assessments] before advisor review — the system both gathers KYC data AND produces the suitability assessment.
  - Problem: the coordination scope of "required for KYC and suitability assessments" admits two parses that differ on whether the system performs the suitability assessment or merely collects inputs for it.
  - Elicitation question: In brief.md, does the application itself produce the suitability assessment before advisor review, or only collect the data the advisor uses to perform it?

### Dimension 3 — Referential ambiguity

**Justification (zero findings):** Dimension 3 (Referential ambiguity) produced zero findings. `brief.md` is written predominantly in imperative bullet lists and field enumerations with few pronouns or demonstratives, and where they occur the antecedent is unambiguous. For example, "This provides a minimum identity check without requiring a full authentication system." (Save & Resume) — "This" refers unambiguously to the immediately preceding action of re-entering the email address; "Requiring them to navigate Steps 4–5 again would create unnecessary friction" (Review Editing Behaviour) — "them" resolves to "users", the only plural antecedent in the clause; and "verify that they were received correctly" (User Goals) — "they" resolves to "documents". No pronoun or demonstrative in the corpus admits ≥2 plausible antecedents that would produce different requirements downstream.

### Dimension 4 — Vague predicates

- **AMB-05** — Severity: `Blocker` — Location: `brief.md` — Dimensions: `[4, 6]` (multi-tag)
  - Evidence: > The objective of this project is to shift most information gathering, verification, and risk assessment activities to a self-service digital experience that clients can complete from home.
  - Interpretations:
    (a) "verification" = the application performs automated identity verification (document authenticity / data checks); "most … activities" means nearly all advisor verification work moves to the app.
    (b) "verification" = the application only collects documents for later verification by an advisor / back-office; no verification logic is in scope.
    (c) "most" leaves an unspecified remainder of gathering / verification / risk-assessment activities advisor-led, and which remainder is undefined.
  - Problem: "shift most … verification … activities to a self-service digital experience" leaves "verification" (a non-specific operation, dim 6) and "most" (a vague quantifier, dim 4) undefined, so whether the app authenticates identity or merely collects documents — and which activities remain advisor-led — is unresolved.
  - Elicitation question: In brief.md, does "verification" in the project objective mean the application performs identity-document authentication, or only collects documents for an advisor to verify, and which gathering or verification activities remain advisor-led?

- **AMB-06** — Severity: `Major` — Location: `brief.md` — Dimensions: `[4]`
  - Evidence: > Nationality and tax residency dropdowns must include at least the 20 most common countries.
  - Interpretations:
    (a) "most common" = the 20 most populous countries globally.
    (b) "most common" = the 20 countries most frequent among Northstar Wealth's existing or target client base.
    (c) "most common" = a recognised standard list (e.g. a top-20 economic index or a region-scoped ISO subset).
  - Problem: "the 20 most common countries" gives no measure for "common", so which 20 countries populate the Nationality and Tax-residency dropdowns is undefined.
  - Elicitation question: In brief.md, by what measure are the "20 most common countries" chosen for the Nationality and Tax-residency dropdowns — global population, Northstar's client base, or a specified standard list?

- **AMB-08** — Severity: `Major` — Location: `brief.md` — Dimensions: `[4]`
  - Evidence: > * No data loss during refresh
    > * Validation consistent across steps
  - Interpretations:
    (a) "consistent" = the same field (e.g. email) is validated by identical rules wherever it appears across steps.
    (b) "consistent" = validation behaviour and timing are uniform (e.g. all fields validate on blur and on Next, with the same error-display pattern) across steps.
  - Problem: "Validation consistent across steps" does not say whether consistency refers to identical rules for repeated fields or to uniform validation timing / UX, which yield different implementations.
  - Elicitation question: In brief.md, does "Validation consistent across steps" mean identical rules for repeated fields, uniform validation timing and error-display behaviour, or both?

- **AMB-07** — Severity: `Minor` — Location: `brief.md` — Dimensions: `[4]`
  - Evidence: > Each step includes a short explanation describing why the information is required.
  - Interpretations:
    (a) "short" = a single sentence (≈ ≤120 characters).
    (b) "short" = a brief paragraph of 2–3 sentences.
  - Problem: "short explanation" gives no length bound, so the per-step explanatory copy could range from one sentence to a paragraph, affecting step layout.
  - Elicitation question: In brief.md, what maximum length (in sentences or characters) defines the "short explanation" shown on each step?

### Dimension 5 — Subjective qualifiers

- **AMB-09** — Severity: `Major` — Location: `brief.md` — Dimensions: `[5]`
  - Evidence: > The application must create a professional, trustworthy, and secure experience that reflects the expectations of financial services clients while complying with Know Your Customer (KYC) and Anti-Money Laundering (AML) onboarding practices.
  - Interpretations:
    (a) "secure experience" = real security controls (encryption in transit / at rest, secure auth) must be implemented.
    (b) "secure experience" = the perception of security via trust signals (copy, design, badges), given the prototype uses localStorage + base64 + mock endpoints with no real backend security.
    (c) "professional / trustworthy" = adherence to a specific visual design system vs measured user-trust outcomes.
  - Problem: "professional, trustworthy, and secure experience" has no operational definition, and "secure" in particular is unresolved between real security controls and perceived-security UI given the mock / localStorage technical scope.
  - Elicitation question: In brief.md, does a "secure experience" require actual security controls, or only trust-signalling UI given the localStorage and mock-endpoint architecture, and against what measure are "professional" and "trustworthy" judged?

- **AMB-10** — Severity: `Major` — Location: `brief.md` — Dimensions: `[5, 6]` (multi-tag)
  - Evidence: > leaves the client feeling confident that Northstar Wealth is handling their personal information professionally and responsibly.
  - Interpretations:
    (a) "feeling confident" is verified by a post-submission user survey / trust metric, and "handling" = the visible data-handling UX (consent, explain-why copy).
    (b) "feeling confident" is an aspirational, untested criterion, and "handling … professionally and responsibly" = back-end data governance (storage, retention, access) out of scope for the mock build.
    (c) "handling" = the literal operations performed on PII (store in localStorage, base64-encode, clear on submit) — a data-lifecycle reading.
  - Problem: the acceptance criterion's "feeling confident" (subjective and untestable as written, dim 5) and "handling their personal information" (non-specific verb, dim 6) leave both how the criterion is verified and what data operations are in scope undefined.
  - Elicitation question: In brief.md, how is the acceptance criterion "leaves the client feeling confident" to be verified, and what specific data-handling operations does "handling their personal information professionally and responsibly" require?

### Dimension 6 — Weak / non-specific verbs

**Justification (zero standalone findings — consolidated):** Dimension 6 (Weak / non-specific verbs) fired during the sweep but produced no standalone finding: both weak-verb hits overlapped vague-predicate or subjective spans and were consolidated under their lowest-dimension primaries per the cross-dimension consolidation rule. "shift most information gathering, verification, and risk assessment activities to a self-service digital experience" (Project Overview, `brief.md`) — the non-specific "verification" operation merged with the vague quantifier "most" into **AMB-05** (dimensions `[4, 6]`); and "leaves the client feeling confident that Northstar Wealth is handling their personal information professionally and responsibly" (Acceptance Criteria, `brief.md`) — the weak verb "handling" merged with the subjective span into **AMB-10** (dimensions `[5, 6]`). Other common weak verbs were checked and found sufficiently operationalised in `brief.md`: "support" appears only as "Supported File Types" (JPG / PNG / PDF) and "Browser Support" (1280px and above) with concrete enumerations; "manage" is not used as a feature verb; and "error handling" is operationalised by the Helpful Errors principles with worked examples. No un-consolidated weak-verb ambiguity remains on this dimension.

### Dimension 7 — Optionality + agentless passive

- **AMB-11** — Severity: `Minor` — Location: `brief.md` — Dimensions: `[7]`
  - Evidence: > The experience should communicate professionalism, transparency, and care.
  - Interpretations:
    (a) "should" = MUST — this is a hard requirement and the trust principles below are mandatory.
    (b) "should" = SHOULD / aspirational — the principles are recommended, and a build that omits some is still acceptable.
  - Problem: the modal "should" on the trust mandate leaves its enforcement strength ambiguous (mandatory vs recommended), even though the principles that follow operationalise the subjective terms themselves.
  - Elicitation question: In brief.md, is "The experience should communicate professionalism, transparency, and care" a mandatory requirement (MUST) or an aspirational guideline (SHOULD) for the build?

---

## Suggested elicitation questions

### Questions for stakeholders of `brief.md`

1. In brief.md, does "investment profile" refer only to the Step 5 risk-profile result, or does it also include the Step 4 employment and source-of-funds data? (AMB-01)
2. In brief.md, does an onboarding "session" include a generated session identifier, or is it solely the form data persisted in localStorage? (AMB-02)
3. In brief.md, is the Student "Funding source" field the same dropdown as the main "Source of Funds" field, or a separate student-specific field with its own options? (AMB-03)
4. In brief.md, does the application itself produce the suitability assessment before advisor review, or only collect the data the advisor uses to perform it? (AMB-04)
5. In brief.md, does "verification" in the project objective mean the application performs identity-document authentication, or only collects documents for an advisor to verify, and which gathering or verification activities remain advisor-led? (AMB-05)
6. In brief.md, by what measure are the "20 most common countries" chosen for the Nationality and Tax-residency dropdowns — global population, Northstar's client base, or a specified standard list? (AMB-06)
7. In brief.md, what maximum length (in sentences or characters) defines the "short explanation" shown on each step? (AMB-07)
8. In brief.md, does "Validation consistent across steps" mean identical rules for repeated fields, uniform validation timing and error-display behaviour, or both? (AMB-08)
9. In brief.md, does a "secure experience" require actual security controls, or only trust-signalling UI given the localStorage and mock-endpoint architecture, and against what measure are "professional" and "trustworthy" judged? (AMB-09)
10. In brief.md, how is the acceptance criterion "leaves the client feeling confident" to be verified, and what specific data-handling operations does "handling their personal information professionally and responsibly" require? (AMB-10)
11. In brief.md, is "The experience should communicate professionalism, transparency, and care" a mandatory requirement (MUST) or an aspirational guideline (SHOULD) for the build? (AMB-11)

---

## Diagnostics

### Quality gates

| Gate | Check | Status | Flagged items |
|---|---|---|---|
| 1 | All 8 schema fields populated | PASS | — |
| 2 | Dimension(s) ∈ [1,7], single int or sorted-distinct list | PASS | — |
| 3 | Severity ∈ {Blocker, Major, Minor} | PASS | — |
| 4 | Evidence verbatim substring of source | PASS | — |
| 5 | Location matches a consumed filename | PASS | — |
| 6 | Interpretations list ≥2 entries | PASS | — |
| 7 | Elicitation question ends with `?` and names the filename | PASS | — |
| 8 | Every dimension has ≥1 finding or a Justification block | PASS | Dims 3, 6 carry Justification blocks |
| 9 | Findings-table row count = sum of per-primary-dimension counts | PASS | 11 = 3+1+0+4+2+0+1 |
| 10 | MANIFEST_FINGERPRINT + per-source sha256[:8] match manifest | PASS | — |

### Coverage map

| filename | tier | findings | dimensions-with-findings | dimensions-with-justification |
|---|---|---|---|---|
| brief.md | Native-text | 11 | 1, 2, 4, 5, 7 | 3, 6 |

### Override log

All quality gates passed; no override invoked.

### Run history

Full overwrite per run; no carried-over findings.
