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
- **Goal–requirement misalignment.** Subject names a `G-NN` anchor but the anchored goal's outcome does not match the subject's stated effect. *(Example: FR-12 cites G-04, but G-04 is about regulator latency and FR-12 is about UI polish — the anchor exists but does not address the subject.)* Q2 fails even with an anchor present; the chain points somewhere but lands on a node whose content is unrelated to the subject's effect. The reviewer captures both quotes (the subject and the anchored goal) and the reasoning line names the domain mismatch.

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
- **Problem–requirement misalignment.** Subject cites a verbatim pain quote, but the pain's domain does not match the subject's effect. *(Example: FR-19 quotes §3 persona-pain about month-end approver bottleneck, but FR-19 is about user-profile editing — the pain exists in the doc but is in a different domain.)* Verbatim matching alone is not enough — the cited pain must be one the subject's action actually removes. The reviewer captures both quotes (the subject and the pain) and the reasoning line names the domain mismatch.
- **Misunderstanding of user needs (stories only).** For §4.2 stories: the cited persona-pain comes from a sibling persona, not the persona the story is for. *(Example: an Approver story cites an Importer pain quote — the quote exists but the pain belongs to a different actor.)* Persona-pain evidence must come from the §3 persona named in the story's `As a …` clause; cross-persona miscitation fails Q3.

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

## Cross-subject coherence pass (CS1–CS5)

The Q1–Q6 rubric audits each subject **in isolation**; the Q7 pass audits **set-theoretic coverage** (every X has ≥1 Y). Neither catches **collective-coherence failures** — places where the doc's subjects each pass their per-subject audit but cannot, in their combination, deliver the stated business outcome. The cross-subject pass fills that axis.

Framing test the user named: *requirements that appear reasonable individually but collectively cannot achieve the stated business outcome.* Q1–Q6 cannot detect this — every subject can pass — and Q7 cannot detect it — every counterpart can be present. The collective failure lives in the *relations* between subjects.

The pass runs **once across the whole doc**, after the Q7 coverage pass and before the Step 6 filter (so CS findings can be GR-NN/PI-NN-rescued by the same filter). Each of five lenses applies a relational predicate over the requirement set and emits 0..N findings. The lenses share evidence (the same anchor pair can trigger multiple lenses); single-pass execution is the methodology choice and a post-scan consolidation step clusters findings by shared anchor-set so the rendered output shows one item with multiple lens-tags rather than duplicates.

### Lens definitions

#### CS1 — Contradictory Objectives

**Predicate:** ≥2 anchors in §4.1 / §6 whose stated outcomes are mutually exclusive or whose thresholds contradict.

**`finding` triggers when:**
- Two §4.1 goals state outcomes that cannot both be true (*G-02: "reduce approver workload 50%"* + *G-07: "approver reviews every transaction"*).
- A §6 requirement's threshold contradicts a §4.1 goal's threshold (*FR-08 sets retention to 7 days*; *G-05 requires 30-day audit trail*).
- Two §6 requirements impose conflicting policies on the same entity / workflow (*BR-04: "exports are read-only"*; *FR-11: "exports may be edited inline"*).

**`finding` does NOT trigger when:**
- Two requirements address different aspects of the same workflow without contradiction.
- A threshold is restated at multiple anchors with the same value (consistency, not contradiction).
- The apparent contradiction is foreclosed by a `[STANDARD-RULE: GR-NN]` or `[PROTOTYPE-INVARIANT: PI-NN]` reference (filter at Step 6 catches these).

**Default severity:** `blocking` — a contradiction cannot be implemented; either anchor is wrong.

#### CS2 — Hidden Assumptions / False Constraints

**Predicate:** a §4–§7 subject depends on a fact, capability, or interpretation the doc does not state; or, a constraint stated as fixed is actually negotiable and the doc does not flag it.

**`finding` triggers when:**
- A requirement assumes a data source's availability the doc never names (*FR-15 reads from "the corporate LDAP"; no §1/§3/§5 quote establishes that LDAP exists or is accessible from this system*).
- A goal assumes a user's prior training, certification, or knowledge that no §3 persona statement records.
- A regulatory citation is given as if it has only one interpretation, but the doc does not show the interpretation has been chosen and validated.
- A constraint is stated as fixed (*"must use SAML"*, *"must run on-premise"*) but the doc gives no §1/§3/§5 evidence that the constraint cannot be relaxed.

**`finding` does NOT trigger when:**
- The assumption is named in `[STANDARD-RULE: GR-NN]` or `[PROTOTYPE-INVARIANT: PI-NN]` (filter rescues at Step 6).
- The assumption is *named* somewhere in the doc, even if not at the subject's anchor — the chain exists, even if weak (this is a Q1 finding, not CS2).
- The "constraint" is stated as a stakeholder preference and the doc explicitly marks it negotiable.

**Default severity:** `major` — the doc may still be buildable; the consultant decides whether to surface the assumption to the stakeholder or revise the requirement.

#### CS3 — Missing System Thinking / Architectural Consequence Blindness

**Predicate:** the requirement set + §7 entity model, taken together, cannot achieve a §4.1 goal — the gap is between subjects, not in any one of them.

**`finding` triggers when:**
- A §4.1 goal commits to a measurable outcome, but no combination of the §6 requirements that cite it could deliver that outcome (*G-02 commits to a 50% reduction in approver workload, but every §6 requirement preserves approver-on-every-transaction*).
- A §4.1 goal implies a capability the doc never states as a requirement (*G-09 promises "regulatory-grade audit"; no §6 requirement establishes immutable storage, signed exports, or auditor access*).
- The §7 entity model is the wrong shape to support a §6 requirement (*FR-22 requires "show all transactions per customer"; §7 has Transaction with no customer foreign key — the entity model precludes the requirement*).
- A §6 requirement triggers architectural consequences (transaction boundaries, eventual consistency, retry semantics) the doc never names.

**`finding` does NOT trigger when:**
- The gap is a single missing requirement at a single anchor (Q7 orphan-goal catches this).
- The gap is one subject's quality (Q1–Q6 catches this).
- The "missing capability" is foreclosed by `PI-NN` (filter rescues at Step 6).

**Default severity:** `blocking` if the goal's measurable outcome cannot be delivered by any combination of cited requirements; `major` otherwise.

#### CS4 — Missing Operational Reality

**Predicate:** the doc names operational concerns nowhere — error recovery, partial failure, day-2 operations, who runs the system, what happens after-hours, monitoring, rollback.

**`finding` triggers when:**
- The doc has §6 requirements that mutate state but no requirement names what happens on partial failure (e.g., FR-X writes to two stores; nothing names rollback).
- The doc names a user-facing workflow that depends on a background process; no requirement names who restarts the process if it fails.
- The doc commits to availability or latency (in §1 / §4.1) but no §6 requirement establishes how it is measured or who is paged.

**`finding` does NOT trigger when:**
- `PI-NN` forecloses the operational concern (*PI-01* makes day-2 ops findings PI-resolved for prototype-mode docs; filter rescues at Step 6).
- The doc is explicitly scoped to a slice that excludes operations (e.g., `[OUT-OF-SCOPE]` annotation present at the relevant anchor).
- An adjacent runbook or operations document is named — even if not read.

**Default severity:** `major` — operations gaps are real but rarely block the build phase; the consultant lifts them into the next pass.

#### CS5 — Human Cost Allocation

**Predicate:** the requirement set loads labour onto a human role when the system could absorb it, stacks cognitive demands beyond a single user's capacity within one workflow, or fails to eliminate now-mechanisable work.

**`finding` triggers when:**
- A §6 requirement specifies a human review/approval step for a class of records where automation is available and not foreclosed (*BR-07: "approver must review every transaction"; no §1/§3 evidence that every transaction needs human judgement*).
- A §4.2 story stacks ≥3 distinct cognitive demands on one actor within one workflow step (read, decide, document, navigate, confirm).
- A §6 requirement preserves existing manual work the new system was supposed to eliminate per §1 (*§1: "automate the monthly close"; FR-X: "user enters the close date manually"*).

**`finding` does NOT trigger when:**
- The human step is foreclosed by `GR-NN` (e.g., a confirmation modal is the framework default; that's not "over-reliance on human intervention", that's GR-04 doing its job).
- The doc's §1 or §3 explicitly names judgement, discretion, or accountability as the reason for the human step.
- The cognitive demand is split across separate workflow steps (the story's `I want …` clause names one action).

**Default severity:** `major` — labour-cost questions are rarely blocking; the consultant decides whether to push back on stakeholders.

### Cross-subject finding schema

```
lens:                 CS1 | CS2 | CS3 | CS4 | CS5
severity:             blocking | major | minor
anchors:              [list of §-anchors, length ≥1; ≥2 for relational lenses CS1 and CS3]
evidence_per_anchor:  [{anchor: "§…", quote: verbatim ≤3 lines from quote index}]
relation:             one sentence — what the cited anchors collectively show
consequence:          one sentence — the stated outcome the doc as written cannot deliver
```

**Bounds (gate-enforced):**

- Each quote ≤3 lines and a verbatim substring of `requirements/requirements.md` (validated against the Step-2 quote index — same discipline as Q1–Q6 evidence).
- ≤5 quotes per finding (the cross-subject pair-or-set need not be exhaustive — cite the smallest set that shows the relation).
- `relation` and `consequence` are reviewer prose: each non-empty ≥1 sentence; combined ≤2 sentences.
- `consequence` must use **observational verbs** (`leaves`, `cannot`, `does not constrain`, `assumes`, `implies`, `precludes`, `omits`). It must **NOT** use **prescriptive verbs** (`add`, `include`, `specify`, `define`, `require`, `mandate`, `must`, `should`). Lexically gate-enforced at gate 13. The methodology never authors replacement subjects; it observes what the doc as written cannot deliver.

### Severity rubric

- **blocking** — direct contradiction (CS1); capability gap for a load-bearing goal (CS3) where the goal's measurable outcome cannot be delivered by any combination of cited requirements.
- **major** — significant gap that requires consultant input. Default for CS2, CS4, CS5 findings.
- **minor** — informational; the doc names the issue at one anchor but does not trace implications.

### Ranking

Findings sorted by `severity` (blocking > major > minor), then by lens order (CS1 → CS2 → CS3 → CS4 → CS5), then by first anchor ascending.

### Post-scan consolidation

After all five lenses emit findings independently, run a single consolidation pass that clusters findings sharing the **same `anchors` set** (set-equality after sorting). For a cluster:

- Render one finding-block in the artefact (the heading carries all the lens-tags it triggered, e.g. `CS1+CS3+CS5 — Approver workload contradiction`).
- Each lens's `relation` and `consequence` lines are preserved inside the block (as labelled sub-bullets).
- Severity is the **max** across cluster members (blocking > major > minor).

Consolidation is descriptive — it never drops a finding, never merges relation/consequence text, never invents new wording. Independent findings (different `anchors` sets) render separately.

### Filter (GR-NN / PI-NN rescue) for CS findings

The Step 6 filter is extended to cover CS findings. Only **CS2** (hidden assumptions) and **CS4** (operational reality) are rescuable, and **CS5** may be rescued only against GR-NN rules covering work allocation (none exist today; the hook is correct for future GR-NN additions).

- **`GR-NN` no-flag rescue.** If a CS2 finding's named "hidden assumption" is itself an active `GR-NN` (the rule names the assumption), the finding is reclassified as `rescued` and dropped from the rendered list. Same for CS5 work-allocation findings whose human step is foreclosed by GR-NN.
- **`PI-NN` premise rescue.** If a CS2 / CS4 finding's premise is contradicted by an active `PI-NN`, the finding is reclassified as `rescued` and dropped. Most relevant: `PI-01` (no real backend — operational-reality findings about day-2 ops are PI-resolved). `PI-02..PI-05` similarly.

CS1 (contradictions) and CS3 (portfolio gaps) cannot be GR-NN/PI-NN-rescued — they describe internal-doc relations whose validity is not foreclosable by an external framework rule. A `PI-NN` that resolved a CS1 contradiction would not eliminate the contradiction; it would only re-anchor one side.

Every rescue is recorded in diagnostics: `{lens, anchors, rescue_source: GR-NN | PI-NN, rule_summary}`.

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

The artefact's `Verdict` line is derived deterministically from three signals: the score distribution (Q1–Q6), the orphan count (Q7), and the cross-subject finding severities (CS1–CS5).

| Verdict | Trigger |
|---|---|
| `BLOCKED` | ≥1 orphan-goal (Q7 coverage failure on the goal layer) **OR** ≥1 subject scored `0/6` **OR** ≥3 subjects scored `≤2/6` **OR** **≥1 `blocking` CS finding** (after consolidation and after Step-6 rescue). |
| `NEEDS-REVISION` | Top-10 contains any score `≤3/6`, but no `BLOCKED` triggers. |
| `ACCEPTED-WITH-CONCERNS` | Top-10 minimum score `≥4/6`, no orphans, and no `blocking` CS findings. Major or minor CS findings DO NOT block this verdict — they appear in the executive summary count and rank list; the consultant triages them. (First Principles never returns `ACCEPTED` unconditionally; the lens always surfaces a Top-10 and the lowest member always merits a look.) |

**Why the floor stays at `blocking` CS only.** Major CS findings (operational reality, hidden assumptions) are systematically common at prototype stage — many are PI-rescuable but not all. Lifting the floor to `≥1 major CS → NEEDS-REVISION` would make `ACCEPTED-WITH-CONCERNS` unreachable for any non-trivial doc and destroy the verdict ladder. Majors influence ranking and the executive-summary count; only blocking findings — direct contradictions and load-bearing capability gaps — promote the verdict.

A `BLOCKED` verdict does not halt the orchestrator — the reviewer still writes the artefact and hands back via the Accept/Revise/Restart loop. The verdict is information for the consultant, not a hard gate.

---

## Filter rules

After Q1–Q6 evaluation, before ranking, walk every captured `no` or `partial` answer and apply two filters:

1. **`GR-NN` no-flag filter.** If a Q5 `no` (mechanism-over-outcome / over-spec) is foreclosed by an active `GR-NN`, drop the question's `no` and re-mark it as `yes-with-evidence: standard-rule GR-NN`. The score is incremented accordingly. Most relevant: `GR-04` (confirmation-modal policy for irreversible actions) — a requirement that specifies confirmation modals is correctly explicit, not over-spec. `GR-19` (session timeout by domain class) — a requirement that specifies a timeout is correctly explicit.
2. **`PI-NN` premise filter.** If a Q5 `no` or a Q3 `no` rests on a premise contradicted by an active `PI-NN`, drop the `no` and re-mark `yes-with-evidence: prototype-invariant PI-NN`. Most relevant: `PI-01` (no real backend) — a requirement specifying a stub backend is the simplest valid path; not gold-plating. `PI-02..PI-05` similarly.

The filters apply only to Q3 and Q5 for per-subject ratings. Q1, Q2, Q4, Q6 cannot be `GR-NN`/`PI-NN`-rescued because the underlying chain (existence / business-goal anchor / measurable outcome / removal consequence) is the subject's own work, not the framework's.

**For cross-subject findings**, the same two filters apply (in the same Step 6 pass) but only to CS2 (hidden assumptions), CS4 (operational reality), and CS5 (human cost — GR-NN only). CS1 (contradictions) and CS3 (portfolio gaps) are not rescuable: they describe internal-doc relations whose validity is not foreclosable by an external framework rule. A rescued CS finding is reclassified as `rescued` and dropped from the rendered list — it is not a score increment (CS findings have severity, not score). See **Cross-subject coherence pass → Filter** above for details.

Every drop is recorded in the diagnostics block as `{subject_id_or_lens, question_or_anchor_set, source: GR-NN | PI-NN}`. Score adjustments produced by Q3/Q5 filter rescue are also recorded — consultants need to see whether a subject's `4/6` is `4/6 native` or `3/6 native + 1 rescued`. CS rescues are recorded by lens + anchor set rather than by score.

---

## Quality gates

Fourteen hard gates. Every gate is a `pass | fail` decision; gate 8 has a `warn` variant. The reviewer runs them before writing the artefact; gate failures halt the write unless the consultant chooses Override at the Step 8 prompt.

1. **Every §4.1, §4.2, §6, §7 numbered item was rated.** `evaluated_count == enumerated_count`.
2. **Every rating has all six Q1–Q6 answers populated.** No subject is missing an answer field.
3. **Every `yes-with-evidence` answer carries a verbatim evidence quote** that exists as a substring of `requirements/requirements.md` (validate against the Step-2 quote index).
4. **Every `partial` and `no` answer carries a reasoning line** ≥1 sentence, non-empty. Stub reasoning (*"unclear"*, *"vague"*) fails.
5. **Every score ∈ integer {0, 1, 2, 3, 4, 5, 6}**.
6. **Every weakest-question marker ∈ {Q1, Q2, Q3, Q4, Q5, Q6}**.
7. **Top-10 callout list has exactly `min(10, |subjects|)` entries**, sorted ascending by score, ties broken by `subject_type` then anchor per the ranking rule.
8. **Coverage pass evaluated every §4.1 goal, every §3 persona, every §4.2 story, every §6 BR-NN, every §7 entity.** The coverage section either lists ≥1 finding per orphan or renders the documented "No orphans" line. *(warn if any coverage relation could not be evaluated because the layer is absent — e.g., no §7 entities — and the omission is documented in diagnostics)*.
9. **Every orphan finding has severity `blocking`** and cites both the orphan's anchor and the expected-counterpart's absence.
10. **Verdict line is consistent with the score distribution, orphan counts, AND blocking CS findings** per the verdict-mapping table above. (Three-axis truth table: the reviewer should not display `ACCEPTED-WITH-CONCERNS` when the Top-10 minimum is `2/6`, OR when an orphan-goal exists, OR when a blocking CS finding exists.)
11. **`REQUIREMENTS_SHA256` field equals the Step-2 SHA-256** captured at read time.
12. **Every CS finding's `anchors` list resolves** — every anchor exists in the Step-2 anchor index. Cross-subject findings cannot cite imaginary subjects. Every `evidence_per_anchor.quote` is a verbatim substring of `requirements/requirements.md` (validated against the Step-2 quote index, same discipline as gate 3).
13. **Every CS finding's `consequence` line uses observational verbs only.** Prescriptive verbs (`add`, `include`, `specify`, `define`, `require`, `mandate`, `must`, `should`) fail. The methodology never authors replacement subjects — this gate enforces the anti-author invariant lexically.
14. **Every CS lens was evaluated.** CS1, CS2, CS3, CS4, CS5 each ran and produced a result (0..N findings; zero findings + an explicit "no findings" diagnostic is acceptable). A silently-skipped lens fails. Each lens's filter rescue (CS2, CS4, CS5 against GR-NN/PI-NN) is recorded in diagnostics.

**On any hard gate failure (gates 1–7, 9, 10, 11, 12, 13, 14):** the reviewer does **not** write the artefact. It surfaces the failure to the consultant via `AskUserQuestion` with `Revise | Override | Restart` (same shape as `user-stories-reviewer.md > Step 6`).

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
- **(Cross-subject pass) Do not author replacement subjects in `consequence` lines.** The cross-subject pass observes incoherence; it does not propose new requirements. *"G-02 commits to a 50% reduction in approver workload, but every §6 requirement preserves approver-on-every-transaction — the requirement set as written cannot deliver G-02"* is observational. *"Add an auto-approve requirement"* is authoring — banned by gate 13. The lexical filter on prescriptive verbs catches the failure shape before it lands in the artefact.
- **(Cross-subject pass) Do not collapse CS findings into Q1–Q6 ratings.** A subject that fails Q2 (anchor exists but content mismatched) is a per-subject finding; a portfolio of three FR-NNs that each cite G-04 but none deliver G-04's outcome is a CS3 finding. The first lives in the ratings table; the second lives in the cross-subject section.
- **(Cross-subject pass) Do not flag findings as `blocking` to escalate impact.** Severity is determined by the lens's predicate: CS1 contradiction → `blocking`; CS3 load-bearing-goal capability gap → `blocking`; CS2/CS4/CS5 default → `major`. Reclassifying a `major` finding as `blocking` to force a verdict change is gate-10-flagged and is methodology-violating.
- **(Cross-subject pass) Do not exceed five lenses.** A sixth lens (separate "weak domain modelling", separate "missing core capabilities") is folded into CS3 by predicate extension. Beyond five, the "lenses share evidence" claim that justifies single-pass execution starts to fail and the methodology becomes adversarial-with-different-categories.

---

## Stance summary

First Principles asks two questions across three axes: *given the stated business reality, does each artefact in §4–§7 need to exist?* (Q1–Q6 per subject), *is anything critical missing from the artefact graph?* (Q7 coverage), and *can the subjects collectively deliver the stated business outcome?* (CS1–CS5 cross-subject). The first axis walks each subject's chain in isolation; the second walks set-theoretic coverage; the third walks relations between subjects. The score (0–6) is the count of `yes-with-evidence` answers; the rank is ascending; the Top-10 deep-dives the worst; orphans surface as `blocking` Q7 findings; CS findings surface separately with their own severities.

A reviewer that returns "all subjects defensible" on a doc whose chains do not land on §1 / §3 quotes has not done the Q1–Q6 audit. A reviewer that complains about wording (an adversarial finding) or about a missing story (a BA / completeness finding) has crossed lanes. A reviewer that rescues a chain by analogy or by reading a draft sidecar has bent the methodology beyond its contract. A reviewer that authors replacement subjects in CS consequence lines has crossed from observation into prescription — banned by gate 13.

Exhaustive Q1–Q6 evaluation across every numbered item in §4–§7 + a Q7 coverage pass + a CS1–CS5 cross-subject pass + honest scoring + an ascending-rank Top-10 callout + observational consequence lines produces a useful first-principles audit; partial evaluation, paraphrased evidence, quota-padded findings, or authored consequences produce noise.
