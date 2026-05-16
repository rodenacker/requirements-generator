<!-- ROLE: asset (review reference). Loaded by framework/agents/reviews/first-principles-reviewer.md at activation. -->

# reviews/first-principles-reference.md

**Purpose:** Methodology reference for the **First Principles** review of every numbered item in `requirements/requirements.md > §4 User goals & stories`, `§6 Requirements`, and `§7 Data entities`. The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews/first-principles-reviewer.md` — drives the agent's enumeration, per-subject Q1–Q6 evaluation, Q7 coverage pass, filter, ranking, validate, render, and write workflow.

**Output produced by the reviewer:** `reviews/FIRST-PRINCIPLES/first-principles-review.md` — a markdown document that (a) rates every subject in §4.1, §4.2, §6, and §7 against six per-subject defensibility questions, (b) surfaces the ten least defensible subjects in a deep-dive callout, (c) walks the doc once more to find orphan goals / personas / stories / requirements / entities (Q7), and (d) records every gate result + score histogram + filter drops in a diagnostics block.

The scaffold for the artefact is `framework/assets/reviews/template-first-principles.md`.

---

## What "First Principles Review" means

The discipline is the one Aristotle described in the *Posterior Analytics* and that Toyota's Sakichi Toyoda operationalised as the Five Whys on the factory floor: *strip a claim back to the irreducible reality it depends on; if the chain to that reality does not exist, the claim is not yet justified*. Applied to a requirements document, the question becomes: *given the business reality stated elsewhere in this same doc, does each artefact in it actually need to exist, and is anything critical missing?*

The reviewer reads every numbered item in §4 (goals + stories), §6 (requirements), and §7 (data entities) and asks the user's seven backbone questions of each:

1. **Why does this exist?**
2. **Which business goal does it support?**
3. **Which problem does it solve?**
4. **What operational outcome does it improve?**
5. **Is it the simplest valid way to achieve that outcome?**
6. **What happens if we remove it?**
7. **Is anything critical missing to achieve the stated goals?**

Q1–Q6 are *per-subject* — they probe whether one artefact is defensible against the rest of the doc. Q7 is *per-document* — it walks the artefact graph (goals → stories → requirements → entities) and surfaces every node that should have a counterpart but doesn't. Q7 is the coverage pass; Q1–Q6 produce a defensibility score.

The output is **two views of the same evidence chain**:

- A **full defensibility ratings table** — one row per subject, scored 0–6, showing the weakest question per row. Consultants scan top-to-bottom for the score distribution.
- A **Top 10 Least Defensible** callout — the 10 lowest-scoring subjects deep-dived, with every Q1–Q6 answer and its evidence quote (or absence-reasoning) surfaced. Consultants triage from here.

Plus a separate **Critical missing artefacts** section that lists Q7 orphans as `blocking` findings.

### How this differs from the other four `/review-requirement` lenses

| Lens | Stance | What gets surfaced | Remediation owner |
|---|---|---|---|
| **adversarial** | *"What is wrong with what's written?"* | Defects in the doc (ambiguity, untestability, contradictions). | Consultant — edits the doc. |
| **ten-ba-questions** | *"What's missing from a BA's perspective?"* | Questions for stakeholders. | Stakeholder — answers. |
| **ten-ux-questions** | *"What's missing from a designer's perspective?"* | Questions for designers. | Designer — interprets. |
| **user-stories** | *"Which §4.2 stories are not yet good stories?"* | Story-quality defects. | Consultant — rewrites stories. |
| **first-principles** | *"Given the stated business reality, does each artefact need to exist, and is anything critical missing?"* | Subjects with weak justification chains + orphan artefacts. | Consultant — re-anchors, re-scopes, removes, merges, or adds the missing artefact. |

A requirements document can be adversarially clean (every sentence is unambiguous, every requirement is testable), story-clean (every §4.2 story passes the six story-quality criteria), and still **first-principles indefensible** — every artefact internally well-formed but disconnected from a stated business goal. Conversely it can be first-principles solid but adversarially defective (every requirement is grounded in a goal but the prose is ambiguous). First Principles is the lens that asks the upstream question.

---

## Sources and defensibility

The 7-question backbone and the defensibility-grading rubric synthesise:

- **First-principles reasoning (Aristotle, *Posterior Analytics* §I.2; later: Descartes; modern application: Elon Musk, *"reason from first principles, not by analogy"*, multiple interviews).** Canonical prior art for the discipline of decomposing a claim back to its irreducible justification. The reviewer's Q1 (*"Why does this exist?"*) is the entry point of that decomposition; Q6 (*"What happens if we remove it?"*) is its dual — if removal has no observable consequence, the first-principles chain is empty.
- **Toyota Production System — Five Whys** (Sakichi Toyoda, 1930s; codified by Taiichi Ohno). The framework's existing `analyses/FIVE-WHYS/` lens uses this technique to interrogate goal chains in §4.1; this review uses the same chain-walking discipline but applied to every numbered item in §4–§7 and graded on whether the chain *reaches* a stated business reality, not on the chain's depth. Five Whys asks *"why?"* recursively; First Principles asks *"is the chain present, and does it terminate at a stated business reality?"*.
- **Karl Wiegers — *Software Requirements*** (Microsoft Press, 3rd ed. 2013). The requirements-quality dimensions (*correctness, completeness, traceability, feasibility, modifiability, prioritisation*) underpin Q3 (problem solved) and Q4 (operational outcome). A requirement that cannot be traced upstream to a stated user or business need is, in Wiegers's terms, *untraceable* — which here is a Q1 / Q2 failure.
- **INVEST — Bill Wake, 2003** (the *Valuable* attribute in particular). A user story is *Valuable* iff its `so that …` clause names an outcome that someone in the business actually wants. Q2 (which goal it supports) and Q4 (which operational outcome it improves) are direct applications of *Valuable* expanded from stories to all artefacts.
- **BABOK® Guide v3** (IIBA, 2015). *Requirements Analysis and Design Definition* validates upstream-justification auditing as a core BA competency distinct from elicitation. The stance is gap-aware but evidence-based: a subject is defensible or not by its observable trace through the document, not by the reviewer's preference for what should be there.
- **Lean/MVP minimalism (Eric Ries, *The Lean Startup*, 2011, ch. 9 "Build-Measure-Learn"; YAGNI principle from Kent Beck's XP).** Q5 (*"Is it the simplest valid way?"*) and Q6 (*"What happens if we remove it?"*) are direct applications: anything that does not pay rent in observable outcome is a removal candidate.

The synthesis is this reference's contribution: integrate Aristotelian first-causes with the framework's existing chain-walking discipline (Five Whys for goals), bind it to Wiegers's traceability dimension and INVEST's *Valuable*, then test the chain at five points (Q1 existence, Q2 business goal, Q3 problem solved, Q4 operational outcome, Q6 removal consequence) plus one minimalism test (Q5 simplicity) per subject, with a separate coverage sweep (Q7 missing artefacts). The score is binary per question (`yes-with-evidence` or zero), so defensibility is *the count of question-answers that survive evidence-grounding*, not the count that *sound* plausible.

---

## Scope: what gets rated

The reviewer rates every numbered item in:

- **§4.1 Goals** — each `G-NN` business / user goal.
- **§4.2 Stories by persona** — each `##### Story:` heading under each persona's `####` heading. (Distinct from the User Stories review, which audits *story craft*; First Principles asks whether the story should exist at all given the stated business reality.)
- **§6 Requirements** — every `BR-NN` business requirement and every `FR-NN` functional requirement.
- **§7 Data entities** — every entity defined in §7.

Other sections of the doc are upstream context the reviewer reads but does not rate:

- §1 (Application context) — provides the business reality Q2/Q3 reference against.
- §3 (Target users / personas) — provides the persona pain Q3 references against.
- §5 (Task flows) — provides the workflow operational outcomes Q4 references against.

Out of scope: anything in §2, §8+, the diagnostics blocks of other artefacts, or any §-numbered cross-reference whose target does not resolve. The Q1–Q6 evaluation does not invent context the doc doesn't contain.

A subject ID is assigned at runtime in `{type-prefix}-NN` form, zero-padded:

- `G-NN` for §4.1 goals (use the doc's own ID if present; otherwise assign in document order).
- `US-NN` for §4.2 stories (assigned in document order across personas — Importer stories first, then the next persona, etc., matching the User Stories review's `US-NN` convention).
- `BR-NN` / `FR-NN` for §6 requirements (use the doc's own IDs).
- `EN-NN` for §7 entities (assigned in document order).

The reviewer also notes `subject_type ∈ {goal, story, requirement, entity}` on each subject record so the ratings table can be sorted by type when needed.

---

## The 7-question rubric

### Q1 — Why does this exist?

**Probe:** is there a traceable reason in `requirements/requirements.md` for this subject's presence?

**Per-subject-type application:**

| Subject type | What counts as `yes-with-evidence` |
|---|---|
| §4.1 goal | A §1 (context) or §3 (persona) quote naming a current-process pain, regulatory pressure, or user outcome that the goal exists to deliver. |
| §4.2 story | A `\| Goal \|` row pointing to a specific §4.1 `G-NN`, **and** the quoted G-NN exists. Alternative: the story's persona has a §3-stated pain that the story's `I want …` clause addresses directly. |
| §6 BR-NN / FR-NN | A rationale annotation tying the requirement to a §4.1 `G-NN`, a §4.2 story, a §1 business outcome, or a `[STANDARD-RULE: GR-NN]` marker. |
| §7 entity | ≥1 §6 requirement quotes the entity name as something to read, write, or constrain. |

**Failure modes (counted as `no`):**

- Subject is named but has no `Rationale` or `Goal` annotation.
- Annotation exists but points to a non-existent target (`Goal: G-99` when §4.1 stops at G-12).
- Subject's existence is justified only by analogy (*"systems like ours usually have one"*) — that's not first-principles, it's pattern-matching.

`partial`: the chain exists but lands on a vague upstream node (a goal whose own Q1 returns `no`).

### Q2 — Which business goal does it support?

**Probe:** can a specific business outcome be named from the doc?

| Subject type | What counts as `yes-with-evidence` |
|---|---|
| §4.1 goal | The goal's own text contains business-outcome wording — a KPI, a measurable target (numbers + units, percentages, time bounds), a regulatory citation, or an outcome verb (*reduce, increase, eliminate, achieve, comply with*). |
| §4.2 story | The `\| Goal \|` row names a §4.1 `G-NN` **and** that goal's Q2 returns `yes-with-evidence`. Alternative: the `so that …` clause names a measurable outcome directly. |
| §6 BR-NN / FR-NN | An upstream `G-NN` quote that satisfies its own Q2, **or** a `[STANDARD-RULE: GR-NN]` reference (those are framework-justified business goals by construction). |
| §7 entity | The goal of *any* §6 requirement that uses the entity, transitively satisfying Q2. |

**Failure modes (`no`):**

- Subject supports something but that "something" is itself another subject with a failing Q1/Q2 (the chain ascends but never lands on a business outcome).
- The named goal is hortatory rather than measurable (*"deliver an excellent user experience"* — not measurable, fails).
- The goal is an internal-system property dressed as a business goal (*"keep the database normalised"* is a constraint, not a business goal).

### Q3 — Which problem does it solve?

**Probe:** can a specific named pain in the doc be identified?

| Subject type | What counts as `yes-with-evidence` |
|---|---|
| §4.1 goal | §1 (context) or §3 (persona) names a current-process friction, manual workload, error class, compliance gap, or stakeholder complaint that the goal removes. |
| §4.2 story | The story's persona has a §3-stated pain; the story's `I want …` action addresses it. Alternative: the linked §5 task flow has a stated friction the story resolves. |
| §6 BR-NN / FR-NN | An upstream story or goal whose Q3 returns `yes-with-evidence`, **or** a `[STANDARD-RULE: GR-NN]` marker (the framework rules exist to resolve known classes of problem). |
| §7 entity | A data-state need (*"we cannot answer X without storing Y"*) named in §1, §3, §4.1, or §5. |

**Failure modes (`no`):**

- No §1 / §3 pain text exists at all.
- The named pain exists but is unrelated (the subject's `I want …` and the named pain are different domains).
- The "problem" is a self-referential one (*"we don't have feature X yet"* — the absence of the feature is not a problem; the user-experience consequence of its absence might be).

### Q4 — What operational outcome does it improve?

**Probe:** can a measurable operational outcome be stated?

| Subject type | What counts as `yes-with-evidence` |
|---|---|
| §4.1 goal | Time-bound or count-bound or threshold-bound outcome (*"reduce close-of-month from 5 days to 2"*, *"zero unreconciled exceptions per week"*). |
| §4.2 story | `so that …` clause names a measurable user/business outcome distinct from the `I want …` action. *"so that I can approve faster"* fails (not measurable). *"so that the back-office team closes the day inside the regulator's 17:00 window"* passes. |
| §6 BR-NN / FR-NN | An associated **acceptance criterion** is testable: a tester can name in one sentence what they would check to declare the requirement done. |
| §7 entity | The entity enables a measurable workflow outcome (named in any §6 requirement's AC) — not just *"records data"*. |

**Failure modes (`no`):**

- Outcome wording is hortatory (*"improve user satisfaction"*, *"deliver value"*).
- Outcome is restated input (*"so that I can {action}"*).
- Acceptance criterion is missing or is itself unmeasurable (*"works correctly"*).

### Q5 — Is it the simplest valid way to achieve that outcome?

**Probe:** is the subject over-specified or gold-plated relative to the outcome it claims?

This is the only **pass-by-default** question. The reviewer only marks `no` when there is an obvious over-specification signal:

- **Mechanism-over-outcome wording.** The subject specifies *how* (a technology, a UI pattern, a data structure) when *what* would suffice. *"FR-12: Use SAML 2.0 over HTTPS with SHA-256 signatures"* in a doc whose stated need is *"single sign-on to the corporate IDP"* — the *what* is one sentence; the *how* belongs in the design system / architecture spec, not the requirements doc.
- **Gold-plating.** The subject's scope is materially wider than the supporting context warrants. A goal that names six measurable outcomes when §1 only states one driver. A story whose `I want …` clause covers four verbs.
- **Orphan attributes (entities only).** An entity has fields that no §6 requirement reads, writes, or constrains. The entity is wider than the requirements need it to be.

**Pass conditions (`yes-with-evidence`):**

- Subject is stated as an outcome, not a mechanism — quote the outcome wording.
- Subject's scope matches the §1 / §3 / §4.1 / §5 context — quote the matching context.
- Entity's attributes all have §6 readers/writers — list the matching requirement IDs.

**Failure modes (`no`):**

- One specific mechanism / over-scope / orphan-attribute pattern triggered — quote the offending text and the unsupported context.

This question is filtered at Step 6 against `GR-NN` and `PI-NN`. A requirement that specifies a confirmation modal is *not* over-spec — `GR-04` makes confirmation modals the framework default and the requirement is correctly explicit. A requirement that specifies a stub backend is not gold-plating — `PI-01` foreclosed real backend so the stub is the simplest valid path.

### Q6 — What happens if we remove it?

**Probe:** can a specific, document-grounded consequence be named for removing this subject?

**`yes-with-evidence` posture:** the reviewer composes a one-sentence consequence-of-removal that cites at least one verbatim quote from the doc. *"Removing G-04 leaves §1's regulatory pressure 'monthly POPIA reporting must be auditable' with no goal-level coverage."*

**`partial`:** removal has an inferable consequence but no quote backs it directly.

**`no`:** removal leaves the doc operationally unchanged (no quote contradicts the removal, no other artefact depends on this one). **This is the smoking gun for least-defensible.** A subject for which "what happens if we remove it?" is "nothing visible" has failed first-principles — it exists without anchoring to a stated reality.

Q6's evidence is the *consequence sentence + the cited quote*, captured verbatim in the per-subject deep-dive.

### Q7 — Is anything critical missing to achieve the stated goals?

**Probe (coverage pass, not per-subject):** does every artefact in the doc that should have a downstream counterpart have one?

Run once, after Q1–Q6 evaluation completes:

| Coverage relation | Orphan finding kind | Severity |
|---|---|---|
| Every §4.1 `G-NN` has ≥1 §6 requirement that traces to it (via rationale annotation or via §4.2 story whose `\| Goal \|` row points to it). | `orphan-goal` | `blocking` |
| Every §3 persona has ≥1 §4.2 story whose persona-heading matches. | `orphan-persona` | `blocking` |
| Every §4.2 story has ≥1 §6 requirement traceable to it. | `orphan-story` | `blocking` |
| Every §6 `BR-NN` business requirement has ≥1 §6 `FR-NN` realising it (if both layers are present in the doc). | `orphan-business-rule` | `blocking` |
| Every §7 entity has ≥1 §6 requirement that reads or writes it. | `orphan-entity` | `blocking` |

Coverage findings render in their own **Critical missing artefacts** section. Each finding cites:

- The orphan's anchor (`§4.1 / G-04`, `§3 / Auditor`, etc.).
- The expected counterpart's absence (*"no §6 requirement references G-04"*).
- The shortest evidence-grounded statement of consequence (e.g., *"G-04 is unimplemented — closing the gap requires either adding a requirement that delivers G-04 or striking G-04 from §4.1"*).

If the doc has zero orphans, the section renders the single line *"No orphans — every goal has a requirement, every persona has a story, every story has a requirement, every entity is used by a requirement."*

---

## Scoring rubric

For each subject, Q1–Q6 yield one of:

- `yes-with-evidence` — the answer is anchored by a verbatim quote (≤5 lines) from `requirements/requirements.md`. Quote captured.
- `partial` — the chain exists but lands somewhere weak (e.g., on another subject whose own Q1/Q2 returns `no`), or the evidence is inferable from adjacent context but not verbatim-quotable. Reasoning line captured (1–2 sentences).
- `no` — not answerable from the doc. Reasoning line captured (1 sentence stating what is missing).

**Defensibility score = count of `yes-with-evidence` answers across Q1–Q6.** Range: integer 0–6.

`partial` and `no` both count as zero for the score. The score expresses *evidence-grounded* defensibility, not *plausible-sounding* fit. A subject that scores 4/6 has four questions answered with verbatim evidence; the other two are unsupported.

**Weakest question marker:** the lowest-numbered question whose answer is not `yes-with-evidence`. Tie-break by Q-order (Q1 weakness is "worst" because the chain has no entry point; Q5 weakness is "least bad" because Q5 is pass-by-default). Recorded as `Q1 | Q2 | Q3 | Q4 | Q5 | Q6` per subject.

**Recommended action** (the per-subject deep-dive includes one):

- `re-anchor` — the subject needs an explicit upstream pointer (rationale annotation, goal reference, or persona pain quote).
- `re-scope` — the subject is broader than its supporting context.
- `remove` — Q6's consequence-of-removal is `nothing visible`; the subject is not paying rent.
- `merge` — the subject overlaps with another better-anchored subject; consolidate.
- `clarify` — wording is hortatory/ambiguous; the chain exists but the language obscures it.

Recommended action is chosen by the reviewer per subject; it is descriptive, not prescriptive — the consultant decides whether to act.

---

## Ranking & Top-10 selection

Sort all rated subjects ascending by score. Ties broken by:

1. **Subject-type order: entity → requirement → story → goal.** Entities and requirements are downstream artefacts; if a downstream artefact scores low, the chain fails at a point closer to the actual build cost. A weak goal can sometimes be re-anchored cheaply; a weak entity carrying multiple requirements upstream is more expensive to fix. Surface the more expensive failures first.
2. **Anchor ascending** within the same type (`§4.1 / G-01` before `§4.1 / G-02`; `§6 / BR-01` before `§6 / FR-01`).

**Top-10 callout** = the first 10 of this ascending sort. If `|subjects| ≤ 10`, the callout lists all of them; if more, exactly 10. The callout for each entry contains:

- Subject ID, anchor, type, verbatim statement (quoted).
- Q1–Q6 answers (each: `yes-with-evidence` + quote, or `partial`/`no` + reasoning).
- Score (`N/6`) and weakest-question marker.
- Recommended action (one of `re-anchor | re-scope | remove | merge | clarify`) + one-sentence rationale.

The **full defensibility ratings table** contains *every* rated subject, in the same sort order; one row per subject with anchor, type, statement, score, weakest answer, and recommended action. Consultants scan the full table to see whether the doc has uniformly weak chains (many low scores) or a few outliers (top-10 ≪ rest).

---

## Verdict mapping

The artefact's `Verdict` line is derived deterministically:

| Verdict | Trigger |
|---|---|
| `BLOCKED` | ≥1 orphan-goal (Q7 coverage failure on the goal layer) **OR** ≥1 subject scored `0/6` **OR** ≥3 subjects scored `≤2/6`. |
| `NEEDS-REVISION` | Top-10 contains any score `≤3/6`, but no `BLOCKED` triggers. |
| `ACCEPTED-WITH-CONCERNS` | Top-10 minimum score `≥4/6` and no orphans. (First Principles never returns `ACCEPTED` unconditionally; the lens always surfaces a Top-10 and the lowest member always merits a look.) |

A `BLOCKED` verdict does not halt the orchestrator — the reviewer still writes the artefact and hands back via the Accept/Revise/Restart loop. The verdict is information for the consultant, not a hard gate.

---

## Filter rules

After Q1–Q6 evaluation, before ranking, walk every captured `no` or `partial` answer and apply two filters:

1. **`GR-NN` no-flag filter.** If a Q5 `no` (mechanism-over-outcome / over-spec) is foreclosed by an active `GR-NN`, drop the question's `no` and re-mark it as `yes-with-evidence: standard-rule GR-NN`. The score is incremented accordingly. Most relevant: `GR-04` (confirmation-modal policy for irreversible actions) — a requirement that specifies confirmation modals is correctly explicit, not over-spec. `GR-19` (session timeout by domain class) — a requirement that specifies a timeout is correctly explicit.
2. **`PI-NN` premise filter.** If a Q5 `no` or a Q3 `no` rests on a premise contradicted by an active `PI-NN`, drop the `no` and re-mark `yes-with-evidence: prototype-invariant PI-NN`. Most relevant: `PI-01` (no real backend) — a requirement specifying a stub backend is the simplest valid path; not gold-plating. `PI-02..PI-05` similarly.

The filters apply only to Q3 and Q5. Q1, Q2, Q4, Q6 cannot be `GR-NN`/`PI-NN`-rescued because the underlying chain (existence / business-goal anchor / measurable outcome / removal consequence) is the subject's own work, not the framework's.

Every drop is recorded in the diagnostics block as `{subject_id, question, source: GR-NN | PI-NN}`. Score adjustments produced by filter rescue are also recorded — consultants need to see whether a subject's `4/6` is `4/6 native` or `3/6 native + 1 rescued`.

---

## Quality gates

Eleven hard gates. Every gate is a `pass | fail` decision; gate 8 has a `warn` variant. The reviewer runs them before writing the artefact; gate failures halt the write unless the consultant chooses Override at the Step 8 prompt.

1. **Every §4.1, §4.2, §6, §7 numbered item was rated.** `evaluated_count == enumerated_count`.
2. **Every rating has all six Q1–Q6 answers populated.** No subject is missing an answer field.
3. **Every `yes-with-evidence` answer carries a verbatim evidence quote** that exists as a substring of `requirements/requirements.md` (validate against the Step-2 quote index).
4. **Every `partial` and `no` answer carries a reasoning line** ≥1 sentence, non-empty. Stub reasoning (*"unclear"*, *"vague"*) fails.
5. **Every score ∈ integer {0, 1, 2, 3, 4, 5, 6}**.
6. **Every weakest-question marker ∈ {Q1, Q2, Q3, Q4, Q5, Q6}**.
7. **Top-10 callout list has exactly `min(10, |subjects|)` entries**, sorted ascending by score, ties broken by `subject_type` then anchor per the ranking rule.
8. **Coverage pass evaluated every §4.1 goal, every §3 persona, every §4.2 story, every §6 BR-NN, every §7 entity.** The coverage section either lists ≥1 finding per orphan or renders the documented "No orphans" line. *(warn if any coverage relation could not be evaluated because the layer is absent — e.g., no §7 entities — and the omission is documented in diagnostics)*.
9. **Every orphan finding has severity `blocking`** and cites both the orphan's anchor and the expected-counterpart's absence.
10. **Verdict line is consistent with the score distribution and orphan counts** per the verdict-mapping table above. (Defence-in-depth: the reviewer should not display `ACCEPTED-WITH-CONCERNS` when the Top-10 minimum is `2/6`.)
11. **`REQUIREMENTS_SHA256` field equals the Step-2 SHA-256** captured at read time.

**On any hard gate failure (gates 1–7, 9, 10, 11):** the reviewer does **not** write the artefact. It surfaces the failure to the consultant via `AskUserQuestion` with `Revise | Override | Restart` (same shape as `user-stories-reviewer.md > Step 6`).

**On gate 8 `warn`:** the reviewer surfaces a one-line note and asks `Continue | Revise`; on `Continue` the warn is recorded in the diagnostics override-log and the run advances.

---

## Anti-patterns (binding on the reviewer)

- **Do not invent evidence.** Every `yes-with-evidence` answer cites a verbatim quote that exists in the quote index (gate 3 enforces this). If a quote cannot be found, the answer is `partial` or `no`.
- **Do not paraphrase upstream-pointer quotes.** Q1, Q2, Q3 quotes are short (≤5 lines) and verbatim. *"§1 mentions regulatory pressure"* is not a quote; *"POPIA requires monthly export of access logs to the regulator within 5 working days"* is.
- **Do not rescue subjects with analogies.** First-principles requires the chain to land on a stated reality in *this* doc. *"Most CRUD systems have a settings table; that's why §7 has FileSetting"* is reasoning by analogy — fails Q1.
- **Do not score subjects that aren't in §4.1, §4.2, §6, §7.** Goals are rated; stories are rated; requirements are rated; entities are rated. §1 / §3 / §5 are upstream context, not subjects.
- **Do not bundle questions.** A subject that fails both Q1 and Q2 has two separate captured answers, not one. The score reflects the count of individual passes, not the count of *kinds* of failure.
- **Do not let Q5 default to `no`.** Q5 is pass-by-default. Only mark `no` when an obvious over-specification signal triggers (mechanism, gold-plate, orphan attribute).
- **Do not enforce a quota across the score range.** A clean doc can score uniformly `5/6` or `6/6` — the lens still surfaces a Top-10 (it's the 10 lowest, not "10 problems"); the Top-10 is information, not a hit list.
- **Do not skip the coverage pass.** Q7 is structurally different; folding it into Q1–Q6 produces the wrong shape (one Q7 answer repeated per subject) and misses orphans.
- **Do not collapse the Top-10 deep-dive into the ratings table.** The Top-10 carries every Q1–Q6 quote / reasoning line; the ratings table carries only score + weakest-question + recommended-action. Two views, same evidence chain.
- **Do not write `[SRC: …]` or `[AI-SUGGESTED: AI-NN]` markers in the artefact.** Per `feedback_no_inline_provenance`, the review artefact is clean of inline source markers. Q1–Q6 quotes carry their own block-quote formatting; provenance is the anchor (`§4.1 / G-04`, `§6 / FR-12`), not a marker.
- **Do not read draft sidecars.** The stand-alone-ish constraint is the agent's most load-bearing invariant. If a subject's "why" lives only in `requirements/requirements-draft.md` or `requirements/draft-claims.ndjson`, *that is the finding* — Q1 returns `no` and the consultant lifts the rationale into the merged doc on the next `/requirements` pass.
- **Do not double-rate a subject.** A §4.2 story is rated against Q1–Q6 once, as a story. The §6 requirements it produces are rated separately, on their own merits. The Q7 coverage pass connects them.
- **Do not silently pass a subject whose chain is incomplete.** First-principles rigour forbids it. If Q1 returns `no`, the score is `0/6` regardless of how Q2–Q6 read (because Q2–Q6 chains land on a Q1-missing node anyway — the per-subject scoring rubric is binary per question, but consultants reading the deep-dive should see *why* a `1/6` or `2/6` happened even when later questions appear individually answerable).
- **Do not author replacement subjects.** Recommended actions are concise hints (one of `re-anchor | re-scope | remove | merge | clarify` + a sentence). Re-anchoring is not the reviewer's job; surfacing the missing anchor is.
- **Do not paste the artefact body into the conversation.** The file lands on disk; the consultant opens it.

---

## Stance summary

First Principles asks one upstream question: *given the stated business reality, does each artefact in §4–§7 need to exist, and is anything critical missing?* Q1–Q6 walk the chain per subject; Q7 walks the artefact graph for orphans. The score is the count of `yes-with-evidence` answers; the rank is ascending; the Top-10 deep-dives the worst.

A reviewer that returns "all subjects defensible" on a doc whose chains do not land on §1 / §3 quotes has not done the audit. A reviewer that complains about wording (an adversarial finding) or about a missing story (a BA / completeness finding) has crossed lanes. A reviewer that rescues a chain by analogy or by reading a draft sidecar has bent the methodology beyond its contract.

Exhaustive Q1–Q6 evaluation across every numbered item in §4–§7 + a Q7 coverage pass + honest scoring + an ascending-rank Top-10 callout produces a useful first-principles audit; partial evaluation, paraphrased evidence, or quota-padded findings produce noise.
