<!-- ROLE: asset (review reference). Loaded by framework/agents/reviews/ten-ux-questions-reviewer.md at activation. -->

# reviews/ten-ux-questions-reference.md

**Purpose:** Methodology reference for the **10 UX Questions** review of `requirements/requirements.md`. The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews/ten-ux-questions-reviewer.md` — drives the agent's candidate-generation, filter, score-and-select, validate, render, and write workflow.

**Output produced by the reviewer:** `review-requirements/TEN-UX-QUESTIONS/ten-ux-questions-review.html` — a self-contained HTML report listing the ten most pressing unanswered UX questions an experienced UX designer would ask after reading `requirements/requirements.md`, each tagged `blocking | major | minor`, each anchored to a section or marked as a missing-section gap, each with a 1–2 sentence rationale on the design impact of leaving the question unanswered. Selection is from a candidate pool of up to 50.

The scaffold for the artefact is `framework/assets/reviews/template-ten-ux-questions.html`.

---

## What "10 UX Questions" means

The discipline mirrors how an experienced UX designer kicks off a project. After reading the requirements doc once, they ask: *"Before I sketch a single screen, what are the things I do not know that — if I had to guess — would force me to make a design decision the consultant has not yet made?"*. The answer is rarely "everything is missing"; it is also rarely "everything is here". It is usually a **short, prioritised list of questions** that span a few categories, each of which would change the design if answered differently.

This methodology operationalises that practice as a deterministic, registry-driven review. The reviewer:

1. Generates up to **50 candidate questions** across **8 UX gap categories** (Step 3 of the agent workflow).
2. Filters the candidates against the framework's deterministic answers — `GR-NN` general rules, `PI-NN` prototype invariants, and the `prototype-scope.md` boundary — dropping any question whose answer is already encoded in the framework or whose topic is out of scope (Step 4).
3. Scores each surviving candidate by `(design-impact × answerability-gap)` and selects the **top 10** (Step 5).
4. Assigns each selected question a priority — `blocking | major | minor` — per the rubric below (Step 5).
5. Renders the output with provenance, rationale, and a triage table (Steps 7–8).

The output is a critique artefact (it identifies gaps), not a draft answer set (it does not propose answers). This preserves the lane separation: the `/requirements` resolver proposes `[AI-SUGGESTED]` answers; this reviewer surfaces questions.

### Why "10"? Why "from 50"?

10 is small enough that a consultant can review every question in one sitting and decide which to send back through `/requirements` for resolution. 50 is the working-pool ceiling: it is broad enough that the score-and-select pass has meaningful options across categories, but tight enough that one agent pass can generate, score, and rank deterministically without context bloat. The 50 → 10 ratio is the prioritisation mechanism — without a candidate pool, "top 10" would just be the first 10.

The two numbers are not magic. They reflect three things:

- **A 5× selection ratio** gives the scoring step real choice. A 2× ratio would barely sort; a 10× ratio would overwhelm context.
- **Practical sitting-time**: 10 questions × ~30 seconds each to read and form an opinion = a single 5-minute review cycle for the consultant.
- **Distinct from the adversarial top-10 triage**: the adversarial review's triage callout is also capped at 10 — that's the consultant's threshold for "what fits on one screen of attention". This methodology's final output is sized to that same threshold.

---

## Upstream input contract

The reviewer reads **only** the following:

- `requirements/requirements.md` — the merged requirements document. Read once at Step 2. This is the critique target.
- `framework/assets/characters/ten-ux-questions-review.md` — the character file. Read once at Step 1.
- `framework/assets/reviews/ten-ux-questions-reference.md` — this document. Read once at Step 1.
- `framework/assets/reviews/template-ten-ux-questions.html` — the HTML scaffold. Read once at Step 7 (render).
- `framework/shared/general-rules.md` — read at Step 4 as a **filter source**. The reviewer scans each candidate question against the `GR-NN` rule list and drops candidates whose topic is deterministically answered. The character file's voice rules and the filter-list table later in this reference both refer to this file.
- `framework/shared/prototype-invariants.md` — read at Step 4 as a **filter source**. The reviewer drops candidates whose underlying premise contradicts a `PI-NN` invariant.
- `framework/shared/prototype-scope.md` — read at Step 4 as a **filter source**. The reviewer drops candidates whose topic is out-of-scope for prototype mode.

It does **not** consult:

- `requirements/requirements-draft.md`, `requirements/source-manifest.json`, `requirements/consultant-answers.md`, `requirements/draft-claims*.ndjson` — pipeline-internal.
- `analyse-requirements/*` outputs — derived artefacts; reviewing the requirements doc against derivatives of itself would conflate "what the doc says" with "what an analyser inferred". The review's contract is to identify gaps in the source doc.
- `design-system/*` outputs — not relevant to a UX questions review.
- `framework/state/*` — pipeline state is not a review input.

The merged requirements document is the contract. If the doc doesn't say it, and no `GR-NN` / `PI-NN` answers it, and it's in-scope per `prototype-scope.md` — it is a candidate gap.

---

## The eight UX gap categories

Eight categories, applied to every candidate question. The categories cover the UX-relevant surface a designer needs before sketching a screen. They are deliberately framed around **decisions a designer must make**, not around document sections — a question can target a missing section as readily as an under-specified one.

### C1 — Users & segmentation

**Question shape:** Who is the user, in enough detail that a designer can pick screen density, terminology, and default settings?

**What to ask about:**

- Sub-segments hidden under one persona name. *"§3 names 'Importer' — are there power-users (bulk-import 100+ files daily) and casual-users (one file per week) within this persona?"*
- Expertise level. Domain experts vs novices need different defaults, different terminology, different inline help.
- Frequency of use. Several-times-a-day, weekly, monthly — drives at-a-glance density vs context-per-record layout.
- Cross-segment behaviour. Do two personas share a screen? Who is the *primary* user of that screen?
- New-user onboarding posture. Is there a first-time-user state, and what does it look like?

**Where this category lives in the requirements template:** primarily `§3 Target users`; secondarily `§6.5 RBAC`. May be a missing-section gap if §3 lists roles without any persona detail.

### C2 — Context of use

**Question shape:** Where, when, and on what device does the user interact with the system? What are they doing immediately before and after?

**What to ask about:**

- Device. Desktop only, mobile, tablet, multiple? Drives layout density and touch-target choices.
- Environment. Open-plan office, lab, retail floor, field service? Drives privacy affordances, font size, light/dark defaults.
- Time pressure. Is the task done under deadline, or at the user's leisure? Drives quick-action affordances vs review-and-confirm flows.
- Interruptions. Is the user expected to complete a task in one sitting, or pick it up later? Drives draft persistence, resume affordances.
- Concurrent tools. Is the user copy-pasting from another system? Drives clipboard-aware input patterns.

**Where this category lives in the requirements template:** rarely declared explicitly; usually a missing-section gap. The framework's template has no dedicated *"context of use"* section, so most candidate questions here cite `missing-section: context-of-use`.

### C3 — Goals & success signals

**Question shape:** What does the user count as a successful outcome, measurably enough that a designer can show progress toward it?

**What to ask about:**

- Quality signals. `§4 User goals & stories` has a quality-signal field per goal; if it's empty or vague, the designer cannot show *"you're making progress"* or *"you're done"*.
- Outcome definitions. *"§4 G-02 says the user can 'manage approvals' — when is the user 'done' with approvals? Inbox-zero? End of business day? Specific record approved?"*
- Time-to-outcome. Is the user trying to finish in 30 seconds, or willing to spend 20 minutes?
- Multi-outcome flows. Does one task have multiple acceptable endings? (Approve, defer, reject — each is a different success.)
- Negative outcomes. What does "failed to achieve the goal" look like? Is there an escape hatch?

**Where this category lives in the requirements template:** `§4 User goals & stories`, especially the §4.1 quality-signals subsection.

### C4 — Tasks, flows, decision points

**Question shape:** What does the user do, in what order, with what decisions? Where do flows branch?

**What to ask about:**

- Happy-path completeness. Does §5 cover the most-common flow end-to-end, or stop at a midpoint?
- Decision points. Does the user choose between options mid-flow? Are the choices listed, or implicit?
- Role-conditional behaviour. Does the same flow look different for different roles? `§6.5 RBAC` may say what each role *can* do, but the flow narrative may not say where the roles diverge in the same task.
- Abandonment. What happens if the user starts a task and leaves halfway? Is state preserved? Is there a re-entry point?
- Partial completion. Does the user save-and-continue-later? What does *"in-progress"* look like in lists and detail views?
- Bulk operations. Does the doc say "import 10 rows" without saying what happens if the user selects 1, or 100, or 10,000?

**Where this category lives in the requirements template:** `§5 Task flows`, especially the exceptions and decision-point subsections; secondarily `§6.5 RBAC` for role-conditional behaviour.

### C5 — Data & content for decisions

**Question shape:** What information does the user need on-screen to make the decisions the task demands?

**What to ask about:**

- Decision-supporting content. The data model (§7) lists what is *stored*; the question is what is *displayed* at decision time. *"§7 says a Transaction has 12 fields — which three does the approver need to see at-a-glance to decide approve vs reject?"*
- Context fields. To approve a transaction, does the user need to see the prior approval history of the same submitter? The doc may not say.
- Comparison views. Does the user need to compare two records side-by-side, or a record against its prior version?
- Aggregations. Does the user need to see totals, counts, averages, trends — and at what time granularity?
- Drill-through paths. From a list, does the user click into a detail view, an edit view, or both? What's the default?
- Off-screen content. What goes in the empty state, the loading state, the no-results-found state — given the user's decision context?

**Where this category lives in the requirements template:** `§6.4 user-facing requirements` and `§7 Data entities` jointly.

### C6 — Errors, edge cases, recovery

**Question shape:** What happens when the happy path breaks? How does the user know, and what can they do?

**What to ask about:**

- Failure modes. Validation failure, network failure, server failure, partial failure (8 of 10 bulk rows succeeded — what now?).
- Recovery affordances. Retry, undo, redo, save-as-draft, contact-support — which apply where?
- Partial-success surfaces. Does a 90%-success bulk import live on the same screen as the failed rows, or branch into a recovery view?
- Conflict resolution. Two users edit the same record concurrently — who wins? Last-write? Conflict screen? Optimistic-lock with a "someone else changed this" banner?
- Authorisation failures. What does a user see when they hit a screen they cannot access via a direct link? (`GR-02` partly answers this — but only if the doc names the action; if the doc is silent on the role's denied actions, the gap is upstream of `GR-02`.)
- Time-bound recovery. How long is a soft-deleted item recoverable? What happens after?

**Where this category lives in the requirements template:** `§5 Task flows > Exceptions` and `§6.4 user-facing requirements > Error handling` jointly; often a missing-section gap when the doc only covers happy paths.

### C7 — Collaboration & concurrency

**Question shape:** What happens when more than one user is involved in the same record or task?

**What to ask about:**

- Concurrent edits. Two users open the same record — what does each see? Are edits broadcast? Is there a lock?
- Handoffs. A submits, B reviews, C approves — what does each role see in their queue? How is a record routed?
- Visibility differences across roles. The same record renders differently to different roles — what is hidden vs disabled vs read-only? (`GR-01` covers viewer-role hiding; the gap is when the doc does not say which actions are which.)
- Notifications. When A submits, does B get notified? In-app, email, both? With what delay? (Notifications are prototypable per `prototype-scope.md` as UI elements — toasts, badges, notification panels.)
- @mentions, comments, threads. Does the doc imply a collaborative dimension without specifying the surface?
- Audit visibility across users. Can A see what B did? Or is the audit log admin-only?

**Where this category lives in the requirements template:** spans `§3 Target users`, `§5 Task flows`, `§6.5 RBAC`; commonly under-specified across all three. Often a missing-section gap.

### C8 — Trust, transparency, audit

**Question shape:** How does the user know the system did what they expected, and what does the user need to be able to look back at?

**What to ask about:**

- Confirmation feedback. After an action completes, what does the user see that confirms it happened? (`GR-14` covers toast-vs-banner placement — but only if the doc names the feedback at all.)
- Audit trail. Can the user see "who changed what when" on a record? Is this a tab, a side panel, a separate screen?
- System-generated content. If the system auto-categorises, auto-fills, or auto-flags, how does the user know which fields are system-touched vs user-touched?
- Why-this-happened explanations. If a record is flagged or rejected by a rule, can the user see which rule fired?
- Versioning. Can the user see prior versions of a record? Restore them? Compare them?
- Permissions visibility. Can the user see *why* they cannot do something, beyond a generic "denied" message?

**Where this category lives in the requirements template:** spans `§6.4 user-facing requirements`, `§6.6 non-functional > Compliance`, `§7 Data entities > audit fields`. Frequently a missing-section gap.

---

## Candidate-pool generation rules (Step 3 of the agent workflow)

The reviewer produces up to **50** candidate questions in a single pass, with explicit per-category quotas:

| Category | Soft quota (candidates) |
|---|---|
| C1 Users & segmentation | 5–7 |
| C2 Context of use | 5–7 |
| C3 Goals & success signals | 5–7 |
| C4 Tasks, flows, decision points | 6–8 |
| C5 Data & content for decisions | 6–8 |
| C6 Errors, edge cases, recovery | 5–7 |
| C7 Collaboration & concurrency | 4–6 |
| C8 Trust, transparency, audit | 4–6 |

The quotas are **soft**: they aim for ~50 candidates spread across 8 categories. If a doc is genuinely silent on a whole category (e.g., a single-user app has no C7 candidates), the candidate count for that category may be zero — but the agent must record in the diagnostics block why the category produced zero, not just emit zero silently.

### Candidate schema (in-memory; never written verbatim to disk)

Each candidate is a JSON-shaped record in memory:

```
q_id_temp:          T-NN          (temporary index used during scoring; overwritten with UXQ-NN at selection)
category:           C1..C8
question_text:      string         (one-sentence question, ≤ 2 lines)
anchor:             §N.N | "missing-section: <slug>"
design_impact:      1..5           (how much the answer changes the design — 5 = different layout/control/flow; 1 = polish-pass)
answerability_gap:  1..5           (how unanswered the question is in the doc — 5 = no information at all; 1 = barely mentioned)
draft_priority:     blocking | major | minor   (the priority the reviewer would assign if this candidate were selected)
rationale:          string         (1–2 sentences explaining the design impact of leaving the question unanswered)
```

A candidate missing any field is invalid and not eligible for selection.

### Candidate-quality rules (applied during generation)

- **One question per candidate.** A candidate that bundles two questions (*"who are the users and how often do they import?"*) is split into two candidates.
- **Specific anchors only.** A candidate citing `§6` (no subsection) gets re-anchored to the most specific subsection that contains the gap. If the gap spans the whole section, mark `provenance: missing-section: <category-slug>` instead of citing the bare section.
- **Designer-phrased questions.** The question text reads as something a designer would ask in a kick-off meeting. *"What is the expected typical-vs-peak ratio of imports per Importer per day?"* — not *"the doc is unclear about import frequency"*.
- **No GR / PI / scope violations.** If a candidate's answer is deterministically supplied by an active `GR-NN`, or contradicts a `PI-NN` invariant, or falls outside `prototype-scope.md`, drop it at Step 4 (filter pass) — but it is fine for it to be generated in Step 3 and then filtered, as long as the filter catches it.
- **No tentative answers.** The reviewer does not include proposed answers in candidate `question_text` or `rationale`. The rationale explains design impact, not what the answer should be.

---

## Filter rules (Step 4 of the agent workflow)

After generating the candidate pool, the reviewer reads `framework/shared/general-rules.md`, `framework/shared/prototype-invariants.md`, and `framework/shared/prototype-scope.md`, then drops every candidate that matches one of the rules below.

### `GR-NN` no-re-ask filter

Each active `GR-NN` rule has a topic; a candidate whose question is answered by the rule is dropped. The table below maps the live `GR-NN` set to the question patterns it forecloses. Update this table when a new `GR-NN` is appended to `framework/shared/general-rules.md`; never renumber.

| `GR-NN` | Topic | Question pattern the rule forecloses |
|---|---|---|
| GR-01 | Viewer-role excluded actions → hidden | *"How should denied actions appear for a Viewer / read-only role?"* |
| GR-02 | Permission-denied on deep links → in-page banner | *"What does a user see when they follow a shared link to a screen they cannot access?"* |
| GR-03 | Archived / read-only entities → suppressed actions + banner | *"How should an archived record's edit screen behave?"* |
| GR-04 | Irreversible actions → modal confirmation, cancel-focused | *"How should the system confirm a destructive action like delete or submit?"* |
| GR-05 | Validation timing — blur for sync, submit for async, never keystroke | *"When should form validation fire?"* |
| GR-06 | Required-field marking — asterisk + legend (or "(optional)" if ≥80% required) | *"How should required vs optional fields be marked?"* |
| GR-07 | Autofocus first editable field on form open | *"Which field should be focused when a form opens?"* |
| GR-08 | Empty-state copy — entity name + creation CTA | *"What should an empty list / table show?"* |
| GR-09 | No-results vs empty — distinguish filter zero-results from zero-data | *"How should zero filter results differ from an empty list?"* |
| GR-10 | Loading thresholds — <300ms hide, 300ms–3s skeleton, >3s skeleton + message | *"When should a spinner or skeleton appear?"* |
| GR-11 | Pagination — always render, 5/10/20/50, default 20 | *"What pagination control and page size should the table use?"* |
| GR-12 | Sortable columns by default, single-column, session-persisted | *"Should table columns be sortable, and how?"* |
| GR-13 | Form-length escalation — ≤8 single, 9–20 with section headers, >20 wizard/tabs | *"How should a long form be laid out?"* |
| GR-14 | Toast vs banner — transient confirmations = toast; persistent state = banner | *"Should this feedback be a toast or a banner?"* |
| GR-15 | Badge count cap — exact ≤99, then `99+`, hide at 0 | *"How should notification badge counts be displayed?"* |
| GR-16 | Status colour mapping — success/error/warning/info/draft + icon redundancy | *"What colour and icon should be used for each status?"* |
| GR-17 | Icon-only controls — tooltip + aria-label; never icon-only destructive | *"How should icon-only buttons be made accessible?"* |
| GR-18 | Mobile table-to-card collapse below 768px | *"What should a table look like on mobile?"* |
| GR-19 | Session timeout by domain — financial 15m, internal 30m, public 60m | *"What should the session timeout be?"* |

If a candidate falls under multiple `GR-NN` topics, the filter logs the first match and drops the candidate.

### `PI-NN` premise filter

A candidate whose underlying premise contradicts a prototype invariant is dropped. The five active invariants:

| `PI-NN` | Invariant | Question pattern the invariant forecloses |
|---|---|---|
| PI-01 | Server behaviour is simulated | *"What should the API endpoint return when…?"*, *"How is the database transaction committed?"* |
| PI-02 | Data is fixture-backed | *"How is data imported from the production system?"*, *"What's the migration strategy from the old DB?"* |
| PI-03 | Validation is visual only | *"How does the server enforce uniqueness?"*, *"What's the rate-limit policy?"* |
| PI-04 | Third-party integrations are visual | *"What's the email-service SLA?"*, *"Which payment provider?"* |
| PI-05 | Role switcher exists in prototype chrome | *"How does the user log in as a different role?"* (the switcher is chrome, not in-app) |

A candidate that asks about a server-side concern phrased as a UX question (*"how does the user know their data is encrypted in transit?"*) is dropped under `PI-01` because the prototype does not exercise transport security. The reviewer cannot expose a question whose only honest answer is "the prototype does not do that".

### `prototype-scope.md` scope filter

A candidate whose topic is in the "Not Prototypable" section of `prototype-scope.md` is dropped. The eight broad out-of-scope categories per that file:

1. Backend API implementation details
2. Database schema and migration specifics
3. Authentication / authorization implementation
4. DevOps, CI/CD, infrastructure
5. Performance optimization techniques
6. Data migration strategies
7. Security implementation details
8. Third-party service integration internals

A candidate that names a server-side topic in its `question_text` is dropped. A candidate that names a UI surface but whose only resolution would require a backend change is also dropped (e.g., *"how should the latency budget be displayed?"* — the prototype has no real latency).

### Diagnostics record

Every dropped candidate is logged in the in-memory diagnostics block with `{q_id_temp, category, reason (gr-match: GR-NN | pi-match: PI-NN | out-of-scope: <topic>)}`. The diagnostics block in the final artefact summarises the drop counts; it does not list every dropped question (the artefact stays scannable).

---

## Score-and-select rule (Step 5 of the agent workflow)

After Step-4 filtering, the reviewer scores each surviving candidate and selects the top 10.

**Score formula:**

```
score = design_impact × answerability_gap
```

Both factors are 1..5. Maximum score is 25 (a question that would massively change the design *and* is entirely unanswered in the doc). Minimum score is 1 (polish-pass details that are barely under-specified).

**Sort:** descending by `score`.

**Tie-breaker order** (deterministic):

1. Higher `design_impact` wins (a high-impact question is preferred to an equally-scored low-impact one with high gap).
2. Earlier category index wins (C1 before C2, etc.), so `Users & segmentation` is preferred to `Trust, transparency, audit` on a tie.
3. Original generation order (the `T-NN` index assigned at Step 3) wins.

**Select:** the top 10 candidates.

**Final ID assignment:** Selected candidates are renumbered `UXQ-01` through `UXQ-10` in score-descending order (i.e., `UXQ-01` is the highest-scoring question, `UXQ-10` is the lowest of the ten selected). This makes the rendered Triage table's top entry the highest-priority question, regardless of category.

**Priority confirmation:** For each of the ten selected, re-confirm the `draft_priority` against the rubric below. If the candidate was scored with `draft_priority: minor` but its `design_impact` is 5, escalate to `major` (a high-impact question is never `minor`). If it was scored `blocking` but `design_impact` is ≤2, downgrade — *"blocking the design"* requires real impact. Re-confirmation is **per-candidate**; there is no global quota.

---

## Priority rubric (canonical)

Every selected question carries exactly one of three priorities.

### blocking

- Without an answer, the design **cannot proceed** because two or more plausible interpretations of the question would yield **contradictory designs**.
- Typical signal: `design_impact = 5` (different layout/control/flow) **and** `answerability_gap = 4..5` (the doc gives the designer no purchase to default).
- Example: *"§3 names 'Approver' and 'Reviewer' separately, but §4 G-02 attributes 'review and approve' to a single actor — are these one role or two?"*. Until resolved, the role-switcher chrome (`PI-05`) cannot be designed: a single approver role has one switcher entry; two distinct roles need two.

### major

- An answer **materially changes design direction** (different screen, different control type, different flow), but design can proceed with a **stated default** while the consultant decides.
- Typical signal: `design_impact = 3..5` and `answerability_gap = 2..4`. The doc gives some signal, but not enough to settle the choice without a default-and-revisit risk.
- Example: *"How frequently does an Importer process imports — daily, weekly, monthly?"*. Drives at-a-glance density vs context-per-record layout. A designer can default to "weekly" and ship a wireframe, but the cost of being wrong is a re-design of the primary screen.

### minor

- Answer affects **refinement only**. A reasonable default produces an **acceptable** design that can be tuned later without re-thinking the screen's structure.
- Typical signal: `design_impact = 1..2` and `answerability_gap = 1..3`.
- Example: *"Should the import history list show absolute timestamps or relative-time strings ('5 minutes ago')?"*. Either is workable; the answer is a polish-pass detail.

There is no fourth priority. *"Could-be-clearer"* is not a priority — either the answer changes the design (`major` or `blocking`) or it tunes a detail (`minor`), or it isn't a UX question at all and should not have survived the filter.

---

## Output presentation

The artefact renders as a self-contained HTML report following `framework/assets/reviews/template-ten-ux-questions.html`. The fixed section ordering is:

1. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead: what this review is, what it found, what the consultant should do next. The **first content section**, above the Executive Summary. A faithful condensation of the findings — it introduces no finding or count not in the punch-list, and **preserves severity verbatim** (a blocking priority is stated unsoftened). Review jargon (priority, category, anchor, candidate pool) is glossed at first use here; client domain terms are not glossed. Per `framework/shared/output-readability.md`.
2. **Header** — title, generated-at timestamp, requirements SHA-256, reviewer identity, priority counts (blocking / major / minor), category coverage summary.
3. **Triage** — single ordered table listing all 10 questions with rank, ID, priority, category, anchor, and the question's first line.
4. **Questions** — one block per question with full text, anchor, priority, category, and the 1–2 sentence rationale.
5. **Diagnostics** — candidate pool size, drop counts (`GR-NN` matches, `PI-NN` matches, out-of-scope), category coverage (which of C1..C8 produced at least one finalist), quality-gate results.

The artefact is a **triage list** with one sanctioned narrative exception: the "In plain terms" lead at the very top. Below that lead, prose between questions is minimised; the consultant should be able to read the Triage table in under two minutes, then jump straight to the question block for context on any entry.

---

## Voice and stance

The reviewer's stance is defined in `framework/assets/characters/ten-ux-questions-review.md` — experienced UX designer, pattern-aware, accessibility-conscious, non-confrontational, asks gap-questions not defect-citations. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it. The character's *Reader & plain language* block sets the human-readability standard (canonical: `framework/shared/output-readability.md`): write the "In plain terms" lead, gloss review jargon at first use, preserve severity verbatim, keep the punch-list below the lead.

---

## Quality gates (run after Step 5, before write)

Eight gates. All are hard. If any gate fails, the reviewer does **not** write the artefact — it surfaces a structured error and halts. (See `framework/agents/reviews/ten-ux-questions-reviewer.md > Step 6 — Validate` for the halt contract.)

1. **Exactly 10 questions in the final output.** No padding, no overflow.
2. **Candidate pool size ≤ 50.** The Step-3 cap is enforced. The pool size is recorded in the diagnostics block.
3. **Every question has a `priority ∈ {blocking, major, minor}`.** No `critical`, no `nit`, no blank.
4. **Every question has a non-empty 1–2 sentence rationale.** Rationale ≥ 1 sentence, ≤ 3 sentences (a 1–2 sentence guideline with a one-sentence buffer). Stub rationales (*"important"*) are a gate failure.
5. **Every question has provenance.** Either (a) a valid `§N.N` anchor that exists in the requirements-doc anchor index built at Step 2, or (b) `provenance: missing-section: <slug>` for a category absent from the doc. Citations to non-existent sections are a gate failure.
6. **No question's topic is resolved by any active `GR-NN`.** Verified by cross-referencing each question's category and topic against the `GR-NN` table in this reference. Any match is a Step-4 filter failure that escaped to selection — a gate failure.
7. **No question's topic is out-of-scope per `prototype-scope.md`.** Same posture: a Step-4 filter failure that escaped to selection is a gate failure.
8. **Category coverage: the 10 questions span ≥ 5 of the 8 categories.** Prevents the score-only ranking from collapsing the output into one or two categories. If `< 5` categories are represented, the reviewer must surface the failure: either the candidate pool was too narrow (re-generate) or the doc genuinely has few gaps in most categories (Override to write a known-narrow review).

---

## Anti-patterns

- **Returning fewer or more than 10 questions.** The output is a fixed-size triage list. The selection rule is the value of this methodology.
- **Skipping the candidate pool.** *"Top 10"* without a 50-candidate pool means *"first 10"* — the prioritisation is performative without the larger surface to sort against.
- **Crossing into adversarial-review.** *"This requirement is poorly written"* is an adversarial finding, not a UX question. If a candidate reads like a defect citation, rewrite it as a designer's question about what's missing, or drop it.
- **Proposing answers.** This reviewer does not draft tentative answers. *"What's the import frequency? (Likely weekly.)"* is forbidden. The `[AI-SUGGESTED]` lane belongs to the `/requirements` drafter.
- **Re-asking what the framework already resolves.** Any candidate whose answer is in a `GR-NN`, `PI-NN`, or contradicts `prototype-scope.md` is dropped at Step 4 — and gate 6 or 7 catches it if it escapes.
- **Mono-category output.** Ten questions all in C4 (tasks & flows) is a coverage failure even if every one of them scores highly. Gate 8 enforces ≥ 5 of 8 categories. The diversity check is not a quota; it is a sanity bound on the score-only ranking.
- **Generic questions.** *"What about the user experience?"* is not a finding. Cite the section (or the missing section); state the specific decision the answer would unlock.
- **Phantom anchors.** A question citing `§4.3.2` when the doc has no `§4.3.2` is a gate-5 failure. Use the Step-2 anchor index to validate every citation.
- **Hidden quotas.** *"Make at least one blocking question"* is not a quota the reviewer enforces. The priority distribution falls out of the doc; a clean doc produces zero blockings legitimately.
- **Reviewing against derivatives.** Do not consult `analyse-requirements/*` outputs to triangulate gaps. The review's contract is to read `requirements/requirements.md` as the source of truth.
- **Inline `[SRC: ...]` markers.** Per project convention (`feedback_no_inline_provenance`), the merged requirements doc is clean of provenance markers; the review artefact is also clean. Questions cite by section number, not by `[SRC: ...]`.

---

## References

- **Erika Hall — *Just Enough Research*** (Rosenfeld Media, 2nd ed. 2019). Discovery-phase question framework: users, contexts, goals, behaviours. The eight-category structure here folds her four into a finer split, separating user segmentation (C1) from context-of-use (C2), and goals (C3) from tasks (C4).
- **Nielsen Norman Group — Discovery-phase questions.** NN/g's standard discovery framework covers users, content, tasks, business, context-of-use. Categories C1, C4, C5, and C2 are direct descendants.
- **Bob Moesta — Jobs-To-Be-Done interview structure** (in *Demand-Side Sales 101*, Lioncrest 2020). Forces (push, pull, anxiety, habit) underpin C3 (goals & success signals) and C6 (errors & recovery — the user's anxiety about doing something irreversible is a signal of where confirmation flows should live).
- **Don Norman — *The Design of Everyday Things*** (Basic Books, revised 2013). Gulfs of execution and evaluation underpin C5 (data for decisions) and C8 (trust & transparency — the gulf of evaluation is the user's question *"did it work?"*).
- **Rob Fitzpatrick — *The Mom Test*** (CreateSpace 2013). The distinction between *decision-changing* questions and *opinion-soliciting* questions underpins the priority rubric — a question only counts as `blocking` if its answer changes the design, not if the answer would merely be interesting.
- **Lou Rosenfeld, Peter Morville, Jorge Arango — *Information Architecture*** (O'Reilly, 4th ed. 2015). Content-and-structure starter questions underpin C5 (decision-supporting content) and C7 (collaboration & visibility — IA's classic question *"who sees what?"*).

The synthesised eight-category structure is this reference's own contribution: it integrates Hall's four discovery dimensions, NN/g's five, Moesta's JTBD forces, Norman's two gulfs, and Rosenfeld's IA starters into one auditable pass-per-category methodology that maps cleanly onto the framework's existing template sections and respects its deterministic-answer set (`GR-NN`, `PI-NN`, `prototype-scope.md`).
