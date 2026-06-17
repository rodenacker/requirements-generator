<!-- ROLE: asset (review reference). Loaded by framework/agents/reviews-inputs/ten-ux-questions-reviewer.md at activation. -->

# reviews-inputs/ten-ux-questions-reference.md

**Purpose:** Methodology reference for the **10 UX Questions** review of the **raw consultant input set** — the material in `input/` enumerated by `requirements/source-manifest.json`. The reviewer follows this document literally and exhaustively. This is the inputs-side sibling of `framework/assets/reviews/ten-ux-questions-reference.md` (which runs the same lens against the merged `requirements/requirements.md`); the two are deliberately parallel so a consultant who knows one can read the other without re-learning the structure. It is also the UX-lens twin of `framework/assets/reviews-inputs/ten-ba-questions-reference.md` — the two inputs-side question reviews occupy mutually-exclusive lanes (see the filter's BA-lens-drop rule below).

**Used by:**

- `framework/agents/reviews-inputs/ten-ux-questions-reviewer.md` — drives the agent's source-ingest, candidate-generation, filter, score-and-select, validate, render, and write workflow.

**Output produced by the reviewer:** `review-inputs/TEN-UX-QUESTIONS/ten-ux-questions-review.html` — a self-contained HTML report listing the ten most pressing **unanswered** UX questions an experienced UX designer would ask after carefully reading the raw input corpus, each tagged `blocking | major | minor`, each carrying a source provenance (`[SRC: <filename>]` for material a consumed source partially touches, or `absent-from-corpus` when the whole topic is missing from every source), each with a 1–2 sentence rationale on the design impact of leaving the question unanswered. Selection is from a candidate pool of up to 50.

The scaffold for the artefact is `framework/assets/reviews-inputs/template-ten-ux-questions.html`.

---

## What "10 UX Questions" means (inputs-side)

The discipline mirrors how an experienced UX designer reviews a pile of raw client material — briefs, interview notes, decks, screenshots, spreadsheets, workshop captures — **before** turning it into a structured requirements document, and well before sketching a screen. After reading the gathered material carefully, the designer asks: *"Before I let this be drafted into requirements and start a wireframe, what are the things I do not know that — if I had to guess — would force me to make a design decision the business has not yet made?"*. The answer is rarely "everything is clear"; it is also rarely "everything is missing". It is usually a **short, prioritised list of questions** that span a few UX-discovery categories, each of which would change the eventual design if answered differently.

This methodology operationalises that practice as a deterministic, registry-driven review. The reviewer:

1. Reads `requirements/source-manifest.json` and ingests every consumable source file (Step 2–3 of the agent workflow).
2. Generates up to **50 candidate questions** across **8 UX gap categories** (Step 4).
3. Filters the candidates against the framework's deterministic answer set and against the adjacent BA-questions lens (Step 5) — dropping any question whose answer is already encoded in the framework, whose topic is out of scope, or whose lens belongs to the 10 BA Questions methodology.
4. Scores each surviving candidate by `(design-impact × answerability-gap)` and selects the **top 10** (Step 6).
5. Assigns each selected question a priority — `blocking | major | minor` — per the rubric below (Step 6).
6. Renders the output with provenance, rationale, and a triage table (Steps 8–9).

The output is a **design-discovery punch-list**, not a corpus defect report and not a business-scope critique. It tells the consultant: *here are the ten user-experience things you should pin down before `/requirements` drafts from this material, so the wireframe is not built against guesses.* Because the inputs are pre-spec, discovery is unambiguously still open — this lens is at its most natural one stage earlier than its requirements-side twin.

The output is a critique artefact (it identifies gaps), not a draft answer set (it does not propose answers). This preserves the lane separation: the `/requirements` resolver proposes `[AI-SUGGESTED]` answers; this reviewer surfaces questions.

### How this differs from the other `/review-inputs` lenses

| Lens | Stance | Output | Remediation owner |
|---|---|---|---|
| **adversarial** | *"What is wrong inside the corpus?"* (defect extraction) | A cited finding of fact about a corpus defect, with a corpus-handling disposition (Patch / Defer / Reject). | Consultant — handles the existing material. |
| **completeness-review** | *"What's missing, measured against the BA canon (IEEE/Volere/BABOK)?"* (exhaustive coverage audit) | Every coverage gap across ten dimensions, each classified Needs-Clarification / Standard-Rule-Applies / Out-of-Scope, with a per-finding elicitation question. | Stakeholder — answers the elicitation questions. |
| **gap-analysis** | *"What's missing, measured against this project's requirements template?"* | Every gap scored Impact × Confidence → MoSCoW, each Must/Should carrying a shall-form candidate requirement. | Consultant — ratifies, edits, or rejects each candidate. |
| **ambiguity-review** | *"What is worded loosely?"* (clarity defects) | Every ambiguous passage, keyed by ambiguity type, with a clarifying stakeholder question. | Stakeholder — pins down the intended meaning. |
| **ten-ba-questions** | *"What's missing from a Business Analyst's perspective — the most consequential things the business hasn't told us yet?"* (consequence-ranked **scope/rules/data** gap-discovery) | **Exactly 10** consequence-ranked stakeholder questions across the 8 BA gap categories. | Stakeholder — answers; the consultant folds the answers into `input/`. |
| **ten-ux-questions** | *"What's missing from a UX designer's perspective — the most consequential things I'd need before I could design a screen?"* (consequence-ranked **user/task/interaction** gap-discovery) | **Exactly 10** consequence-ranked design-discovery questions across the 8 UX gap categories — **no per-finding disposition, no candidate requirement, no per-passage defect**; a scannable design punch-list. | Stakeholder / designer — answers; the consultant folds the answers into `input/` before drafting. |

The load-bearing differentiator from its **BA twin**: `ten-ba-questions` asks *what the business must decide* — scope, rules, data ownership, sign-off authority, success metrics. `ten-ux-questions` asks *what the user must be able to do and see, and what the designer needs to know to design that* — who the user is at the screen, their context of use, their task decision-points, the data they need on-screen to decide, their failure-and-recovery experience, and how they verify the system did what they expected. The two are complementary, run alongside each other, and are kept orthogonal by the BA-lens-drop filter (Step 5, rule 4) and gate 9. The load-bearing differentiator from the **exhaustive** siblings (`completeness-review`, `gap-analysis`): this is a **ruthless top-10 triage** — *"if you only get to ask ten design questions before we draft, ask these."*

### Why "10"? Why "from 50"?

10 is small enough that a consultant can review every question in one sitting and decide which to send back to the stakeholder. 50 is the working-pool ceiling: broad enough that the score-and-select pass has meaningful options across categories, tight enough that one agent pass can generate, score, and rank deterministically without context bloat. The 50 → 10 ratio is the prioritisation mechanism — without a candidate pool, "top 10" would just be the first 10.

The two numbers mirror the existing 10 BA Questions and (requirements-side) 10 UX Questions methodologies for two reasons:

- **Parity** — consultants who already know a sibling flavour can read this one without re-learning the structure.
- **Practical sitting-time** — 10 questions × ~30 seconds each = a single 5-minute review cycle for the consultant.

---

## Sources and defensibility

The eight-category taxonomy and the priority rubric are not inventions of this file. They are the inputs-side restatement of the synthesised discovery framework defined in `framework/assets/reviews/ten-ux-questions-reference.md`, which integrates five reputable sources:

- **Erika Hall — *Just Enough Research*** (Rosenfeld Media, 2nd ed. 2019). Discovery-phase question framework: users, contexts, goals, behaviours. The eight-category structure folds her four into a finer split, separating user segmentation (C1) from context-of-use (C2), and goals (C3) from tasks (C4).
- **Nielsen Norman Group — Discovery-phase questions.** NN/g's standard discovery framework covers users, content, tasks, business, context-of-use. Categories C1, C4, C5, and C2 are direct descendants.
- **Bob Moesta — Jobs-To-Be-Done interview structure** (in *Demand-Side Sales 101*, Lioncrest 2020). Forces (push, pull, anxiety, habit) underpin C3 (goals & success signals) and C6 (errors & recovery — the user's anxiety about doing something irreversible signals where confirmation flows should live).
- **Don Norman — *The Design of Everyday Things*** (Basic Books, revised 2013). Gulfs of execution and evaluation underpin C5 (data for decisions) and C8 (trust & transparency — the gulf of evaluation is the user's question *"did it work?"*).
- **Lou Rosenfeld, Peter Morville, Jorge Arango — *Information Architecture*** (O'Reilly, 4th ed. 2015). Content-and-structure starter questions underpin C5 (decision-supporting content) and C7 (collaboration & visibility — IA's classic *"who sees what?"*).

The synthesis is the requirements-side reference's contribution; this file's contribution is to map those eight categories onto the **raw input corpus** (where the gaps surface as `absent-from-corpus` or partially-touched material rather than under-specified requirements sections) and to bind the lens against the adjacent BA-questions lens (`framework/assets/reviews-inputs/ten-ba-questions-reference.md`) so the two stay orthogonal. The priority labels (`blocking / major / minor`) follow canonical defect-severity practice, mapped onto *unanswered design questions* instead of *implemented-but-broken behaviour*.

---

## Upstream input contract

The reviewer reads **only** the following:

- `requirements/source-manifest.json` — the manifest enumerating consumable input files. Read once at Step 2. This is the entry point to the critique target.
- The files the manifest enumerates — for each row where `tier != "Unsupported"`, the file selected by the Read-path resolution rule in `framework/skills/build-source-manifest.md` (read `converted_sibling` when non-null, else `original_path` — only `Native-text` is read at `original_path`). For `Native-multimodal` / `Vector-renderable` rows the `converted_sibling` is a frozen textual description prepared by the input-handler — it already captures labels, field captions, table contents, status/error states, KPI values, and a structured breakdown; treat it as the canonical text source and do **not** re-interpret pixels. `Supported-via-MCP` rows read the markitdown sibling. Read once per row at Step 3. These are the critique target.
- `framework/assets/characters/ten-ux-questions-inputs-review.md` — the character file. Read once at Step 1.
- `framework/assets/reviews-inputs/ten-ux-questions-reference.md` — this document. Read once at Step 1.
- `framework/assets/reviews-inputs/template-ten-ux-questions.html` — the HTML scaffold. Read once at Step 8 (render).
- `framework/shared/general-rules.md` — read at Step 5 as a **filter source**. The reviewer scans each candidate question against the `GR-NN` rule list and drops candidates whose topic is deterministically answered.
- `framework/shared/prototype-invariants.md` — read at Step 5 as a **filter source**. The reviewer drops candidates whose underlying premise contradicts a `PI-NN` invariant.
- `framework/shared/prototype-scope.md` — read at Step 5 as a **filter source**. The reviewer drops candidates whose topic is out-of-scope for prototype mode.
- `framework/assets/reviews-inputs/ten-ba-questions-reference.md` — read at Step 5 as a **filter source** for the BA-lens-drop rule (rule 4 below). The reviewer drops candidates whose question shape matches a BA category from that reference. (This is the symmetric inverse of how the 10 BA Questions reviewer reads `reviews/ten-ux-questions-reference.md` to drop UX-shaped candidates; the inputs-side BA reference is reused read-only purely as the BA-classification rubric — it carries the canonical UX-vs-BA boundary table.)

It does **not** consult:

- `requirements/requirements.md`, `requirements/requirements-draft.md`, `requirements/consultant-answers.md`, `requirements/draft-claims*.ndjson` — `/requirements`-pipeline artefacts. The review's contract is to critique **raw inputs**, not anything synthesised from them. Reviewing the inputs against a document drafted from those same inputs would conflate "what the corpus says" with "what the drafter inferred".
- `analyse-requirements/*`, `analyse-inputs/<METHOD>/*` outputs — derived artefacts; each input-pipeline lens is independently grounded in the manifest.
- `design-system/*` outputs — not relevant to a UX questions review.
- `framework/state/*` — pipeline state is not a review input.
- Any other file under `framework/shared/` (e.g. `refusal-registry.md`) — referenced by ID only, not read by this agent.

The raw input corpus is the contract. If no source says it, and no `GR-NN` / `PI-NN` answers it, and it's in-scope per `prototype-scope.md`, and it doesn't belong to the BA lens — it is a candidate gap.

---

## The eight UX gap categories

Eight categories, applied to every candidate question. The categories cover the UX-relevant surface a designer needs before sketching a screen. They are deliberately framed around **decisions a designer must make**, not around document sections — a question can target a topic wholly absent from the corpus as readily as one a single source mentions in passing.

### C1 — Users & segmentation

**Question shape:** Who is the user, in enough detail that a designer can pick screen density, terminology, and default settings?

**What to ask about:**

- Sub-segments hidden under one role name. *"The interview names an 'Importer' — are there power-users (bulk-import 100+ files daily) and casual-users (one file per week) within this persona, and do their screens differ?"*
- Expertise level. Domain experts vs novices need different defaults, terminology, inline help.
- Frequency of use. Several-times-a-day, weekly, monthly — drives at-a-glance density vs context-per-record layout.
- Cross-segment behaviour. Do two personas share a screen? Who is the *primary* user of that screen?
- New-user onboarding posture. Is there a first-time-user state, and what does it look like?

**Where this surfaces in a corpus:** personas, stakeholder maps, or interview rosters when present; commonly a partially-touched gap when the inputs name roles without design-relevant detail (expertise, frequency, segmentation), and an `absent-from-corpus` gap when no source profiles the user at all. (Note: questions about *who has stake / sign-off authority* belong to the BA lens; this category asks who the user is *at the screen*.)

### C2 — Context of use

**Question shape:** Where, when, and on what device does the user interact with the system? What are they doing immediately before and after?

**What to ask about:**

- Device. Desktop only, mobile, tablet, multiple? Drives layout density and touch-target choices.
- Environment. Open-plan office, lab, retail floor, field service? Drives privacy affordances, font size, light/dark defaults.
- Time pressure. Is the task done under deadline, or at the user's leisure? Drives quick-action affordances vs review-and-confirm flows.
- Interruptions. Is the user expected to complete a task in one sitting, or pick it up later? Drives draft persistence, resume affordances.
- Concurrent tools. Is the user copy-pasting from another system? Drives clipboard-aware input patterns.

**Where this surfaces in a corpus:** rarely declared explicitly; usually an `absent-from-corpus` gap. Briefs, decks, and mockups almost never state device, environment, or time pressure, yet each materially changes the screen.

### C3 — Goals & success signals

**Question shape:** What does the user count as a successful outcome, measurably enough that a designer can show progress toward it?

**What to ask about:**

- Quality signals. If the inputs name a goal without a notion of "good outcome", the designer cannot show *"you're making progress"* or *"you're done"*.
- Outcome definitions. *"The deck lists a goal to 'manage approvals' — when is the user 'done' with approvals? Inbox-zero? End of business day? A specific record approved?"*
- Time-to-outcome. Is the user trying to finish in 30 seconds, or willing to spend 20 minutes?
- Multi-outcome flows. Does one task have multiple acceptable endings? (Approve, defer, reject — each a different success.)
- Negative outcomes. What does "failed to achieve the goal" look like? Is there an escape hatch?

**Where this surfaces in a corpus:** goal lists, OKR docs, or success slides when present; commonly partially-touched when the inputs name goals without user-facing success signals, and `absent-from-corpus` when they describe features but not outcomes. (Note: questions about the *business* metric of success — revenue, sign-off authority — belong to the BA lens; this category asks what *the user on the screen* perceives as done.)

### C4 — Tasks, flows, decision points

**Question shape:** What does the user do, in what order, with what decisions? Where do flows branch?

**What to ask about:**

- Happy-path completeness. Do the inputs cover the most-common flow end-to-end, or stop at a midpoint?
- Decision points. Does the user choose between options mid-flow? Are the choices listed, or implicit?
- Role-conditional behaviour. Does the same flow look different for different roles? The inputs may say what each role *can* do without saying where the roles diverge in the same task.
- Abandonment. What happens if the user starts a task and leaves halfway? Is state preserved? Is there a re-entry point?
- Partial completion. Does the user save-and-continue-later? What does *"in-progress"* look like in lists and detail views?
- Bulk operations. Do the inputs say "import 10 rows" without saying what happens if the user selects 1, or 100, or 10,000?

**Where this surfaces in a corpus:** process docs, workshop notes, demo scripts, or annotated mockups when present; mockups and demo scripts commonly show only the happy path, leaving branches and exceptions `absent-from-corpus`.

### C5 — Data & content for decisions

**Question shape:** What information does the user need on-screen to make the decisions the task demands?

**What to ask about:**

- Decision-supporting content. A data dictionary lists what is *stored*; the question is what is *displayed* at decision time. *"A spreadsheet lists 12 fields on a Transaction — which three does the approver need at-a-glance to decide approve vs reject?"*
- Context fields. To approve a transaction, does the user need the prior approval history of the same submitter? The inputs may not say.
- Comparison views. Does the user need to compare two records side-by-side, or a record against its prior version?
- Aggregations. Does the user need totals, counts, averages, trends — and at what time granularity?
- Drill-through paths. From a list, does the user click into a detail view, an edit view, or both? What's the default?
- Off-screen content. What goes in the empty state, the loading state, the no-results-found state — given the user's decision context?

**Where this surfaces in a corpus:** data dictionaries, sample spreadsheets, ERDs, or mockups when present; the *what-is-displayed-at-decision-time* slice is frequently partially-touched (storage is listed, decision-support is not). (Note: questions about *who owns / governs* the data belong to the BA lens; this category asks what the user must *see* to decide.)

### C6 — Errors, edge cases, recovery

**Question shape:** What happens when the happy path breaks? How does the user know, and what can they do?

**What to ask about:**

- Failure modes. Validation failure, network failure, server failure, partial failure (8 of 10 bulk rows succeeded — what does the user see now?).
- Recovery affordances. Retry, undo, redo, save-as-draft, contact-support — which apply where?
- Partial-success surfaces. Does a 90%-success bulk import live on the same screen as the failed rows, or branch into a recovery view?
- Conflict resolution. Two users edit the same record concurrently — what does each user *see*? A "someone else changed this" banner? A conflict screen?
- Authorisation failures. What does a user see when they hit a screen they cannot access via a direct link?
- Time-bound recovery. How long is a soft-deleted item recoverable, and how is that surfaced to the user?

**Where this surfaces in a corpus:** runbooks, exception logs, or annotated error-state mockups when present; frequently an `absent-from-corpus` gap when the inputs cover only happy paths (the common case for mockups and demo scripts). (Note: questions about the *business policy* for partial failure — retry vs escalate as a rule — belong to the BA lens; this category asks what the *user sees and can do* when it breaks.)

### C7 — Collaboration & concurrency

**Question shape:** What happens when more than one user is involved in the same record or task?

**What to ask about:**

- Concurrent edits. Two users open the same record — what does each see? Are edits broadcast? Is there a lock indicator?
- Handoffs. A submits, B reviews, C approves — what does each role see in their queue? How does a record appear as routed to them?
- Visibility differences across roles. The same record renders differently to different roles — what is hidden vs disabled vs read-only on screen?
- Notifications. When A submits, does B get a toast, a badge, a notification panel entry? (Notifications are prototypable as UI elements.)
- @mentions, comments, threads. Do the inputs imply a collaborative dimension without specifying the surface?
- Audit visibility across users. Can A see what B did on a record? Is that a tab, a side panel, admin-only?

**Where this surfaces in a corpus:** interview/workshop notes that mention multi-user workflows; commonly under-specified across sources and frequently an `absent-from-corpus` gap when the inputs assume a single user.

### C8 — Trust, transparency, audit

**Question shape:** How does the user know the system did what they expected, and what does the user need to be able to look back at?

**What to ask about:**

- Confirmation feedback. After an action completes, what does the user see that confirms it happened?
- Audit trail. Can the user see "who changed what when" on a record? Is this a tab, a side panel, a separate screen?
- System-generated content. If the system auto-categorises, auto-fills, or auto-flags, how does the user know which fields are system-touched vs user-touched?
- Why-this-happened explanations. If a record is flagged or rejected by a rule, can the user see which rule fired?
- Versioning. Can the user see prior versions of a record? Restore them? Compare them?
- Permissions visibility. Can the user see *why* they cannot do something, beyond a generic "denied" message?

**Where this surfaces in a corpus:** compliance docs, audit-requirement slides, or mockups with history panels when present; frequently an `absent-from-corpus` gap — trust and transparency are among the most-missed surfaces in a raw input set. (Note: questions about *compliance obligations* or *who owns the audit policy* belong to the BA lens; this category asks what the *user* must be able to verify and look back at.)

---

## Candidate-pool generation rules (Step 4 of the agent workflow)

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

The quotas are **soft**: they aim for ~50 candidates spread across 8 categories. If the corpus is genuinely silent on a whole category (e.g., a single-user app has no meaningful C7 concurrency candidates), the candidate count for that category may be zero — but the agent must record in the diagnostics block why the category produced zero, not just emit zero silently.

### Candidate schema (in-memory; never written verbatim to disk)

Each candidate is a JSON-shaped record in memory:

```
q_id_temp:          T-NN          (temporary index used during scoring; overwritten with UXQ-NN at selection)
category:           C1..C8
question_text:      one-sentence question, ≤ 2 lines, designer-phrased (kick-off-meeting voice)
source:             "[SRC: <filename>]" (a filename in the consumed-filename set) | "absent-from-corpus" | "absent-from-corpus: <topic>"
design_impact:      1..5           (how much the answer changes the design — 5 = different layout/control/flow; 1 = polish-pass)
answerability_gap:  1..5           (how unanswered the question is across the corpus — 5 = no source touches it; 1 = one source mentions it in passing)
draft_priority:     blocking | major | minor   (the priority the reviewer would assign if this candidate were selected)
rationale:          1–2 sentences explaining the design impact of leaving the question unanswered
```

A candidate missing any field is invalid and not eligible for selection.

### Candidate-quality rules (applied during generation)

- **One question per candidate.** A candidate that bundles two questions (*"who are the users and how often do they import?"*) is split into two candidates.
- **Specific source provenance only.** A candidate grounded in material the corpus partially touches cites the **specific filename** where that material sits: `[SRC: <filename>]` (the basename from the manifest row). If the whole topic is absent from every consumed source, mark `source: absent-from-corpus` (optionally `absent-from-corpus: <topic>` for a one-word topic tag).
- **Designer-phrased questions.** The question text reads as something a designer would ask in a kick-off meeting. *"How frequently does an Importer process imports — daily, weekly, monthly?"* — not *"the brief is unclear about import frequency"*.
- **No GR / PI / scope / BA-lens violations.** If a candidate's answer is deterministically supplied by an active `GR-NN`, or contradicts a `PI-NN` invariant, or falls outside `prototype-scope.md`, or fits a BA category from `ten-ba-questions-reference.md`, drop it at Step 5 — but it is fine for it to be generated in Step 4 and then filtered, as long as the filter catches it.
- **No tentative answers.** The reviewer does not include proposed answers in candidate `question_text` or `rationale`. The rationale explains design impact, not what the answer should be.

---

## Filter rules (Step 5 of the agent workflow)

After generating the candidate pool, the reviewer reads four filter sources and drops every candidate that matches one of the rules below.

### Filter source reads (Step 5 only)

- `framework/shared/general-rules.md`
- `framework/shared/prototype-invariants.md`
- `framework/shared/prototype-scope.md`
- `framework/assets/reviews-inputs/ten-ba-questions-reference.md`

The four reads are scoped to this step and are the agent's **only** reads outside its own asset set, the manifest, and the manifest-enumerated source files.

### Rule 1 — `GR-NN` no-re-ask filter

Each active `GR-NN` rule has a topic; a candidate whose question is answered by the rule is dropped. The live set lives in `framework/shared/general-rules.md` — the reviewer reads that file at Step 5 and walks the active rule IDs. Because UX-shaped questions are exactly what the `GR-NN` set forecloses (validation timing, required-field marking, empty-state copy, loading thresholds, pagination defaults, sortable columns, toast-vs-banner, badge caps, status colours, icon-only labelling, mobile collapse, session timeout), this filter is **load-bearing for the UX lens** — far more candidates collide here than for the BA lens.

| `GR-NN` | Topic | UX question pattern the rule forecloses |
|---|---|---|
| GR-01 | Viewer-role excluded actions → hidden | *"How should denied actions appear for a read-only role?"* |
| GR-02 | Permission-denied on deep links → in-page banner | *"What does a user see following a link to a screen they cannot access?"* |
| GR-03 | Archived / read-only entities → suppressed actions + banner | *"How should an archived record's edit screen behave?"* |
| GR-04 | Irreversible actions → modal confirmation, cancel-focused | *"How should the system confirm a destructive action?"* |
| GR-05 | Validation timing — blur for sync, submit for async | *"When should form validation fire?"* |
| GR-06 | Required-field marking — asterisk + legend | *"How should required vs optional fields be marked?"* |
| GR-07 | Autofocus first editable field | *"Which field is focused when a form opens?"* |
| GR-08 | Empty-state copy — entity name + creation CTA | *"What should an empty list show?"* |
| GR-09 | No-results vs empty distinction | *"How should zero filter-results differ from an empty list?"* |
| GR-10 | Loading thresholds — skeleton bands | *"When should a spinner or skeleton appear?"* |
| GR-11 | Pagination — render, 5/10/20/50, default 20 | *"What pagination control and page size?"* |
| GR-12 | Sortable columns by default | *"Should table columns be sortable?"* |
| GR-13 | Form-length escalation — sections / wizard | *"How should a long form be laid out?"* |
| GR-14 | Toast vs banner | *"Should this feedback be a toast or a banner?"* |
| GR-15 | Badge count cap — 99+ | *"How should badge counts be displayed?"* |
| GR-16 | Status colour mapping + icon redundancy | *"What colour and icon for each status?"* |
| GR-17 | Icon-only controls — tooltip + aria-label | *"How should icon-only buttons be made accessible?"* |
| GR-18 | Mobile table-to-card collapse below 768px | *"What should a table look like on mobile?"* |
| GR-19 | Session timeout by domain | *"What should the session timeout be?"* |

If a candidate falls under multiple `GR-NN` topics, the filter logs the first match and drops the candidate with `reason: gr-match: GR-NN`.

### Rule 2 — `PI-NN` premise filter

A candidate whose underlying premise contradicts a prototype invariant is dropped. The five active invariants:

| `PI-NN` | Invariant | UX question pattern the invariant forecloses |
|---|---|---|
| PI-01 | Server behaviour is simulated | *"What does the API endpoint return when…?"*, *"How is the transaction committed?"* |
| PI-02 | Data is fixture-backed | *"How is data imported from the production system?"*, *"What's the migration UX?"* |
| PI-03 | Validation is visual only | *"How does the server enforce uniqueness?"*, *"What's the rate-limit message?"* |
| PI-04 | Third-party integrations are visual | *"What's the email-service SLA shown to the user?"*, *"Which payment provider?"* |
| PI-05 | Role switcher exists in prototype chrome | *"How does the user log in as a different role?"* (the switcher is chrome, not in-app) |

A candidate whose only honest answer is "the prototype does not exercise that concern" is dropped with `reason: pi-match: PI-NN`.

### Rule 3 — `prototype-scope.md` scope filter

A candidate whose topic is in the "Not Prototypable" section of `prototype-scope.md` is dropped. The broad out-of-scope categories per that file:

1. Backend API implementation details
2. Database schema and migration specifics
3. Authentication / authorization implementation
4. DevOps, CI/CD, infrastructure
5. Performance optimisation techniques
6. Data migration strategies
7. Security implementation details
8. Third-party service integration internals

A candidate that names a server-side topic in its `question_text` is dropped with `reason: out-of-scope: <topic>`. A candidate that names a UI surface but whose only resolution would require a backend change is also dropped (e.g., *"how should the real latency budget be displayed?"* — the prototype has no real latency).

### Rule 4 — BA-lens drop

A candidate whose question shape fits a BA category from `framework/assets/reviews-inputs/ten-ba-questions-reference.md > C1–C8` is dropped. The BA-vs-UX boundary (the inverse of the table in that reference):

| BA-lens question (drop here) | UX-lens question (keep here) |
|---|---|
| *"What is the decision logic for the approval workflow?"* | *"What does the approver need on-screen to decide approve vs reject?"* |
| *"What is the business rule for when records appear in vs disappear from this list?"* | *"What should the empty / no-results state show the user?"* |
| *"What is the business policy for what data may be visible at decision time, given privacy constraints?"* | *"Which fields does the user need at-a-glance vs on drill-through?"* |
| *"What is the business policy when 8 of 10 bulk records succeed — retry, accept partial, or escalate?"* | *"What does partial-success of a bulk import look like to the user, and how do they recover?"* |
| *"Which roles exist, and who has sign-off authority on the role list?"* | *"How does each role's view of the same record differ — hidden vs disabled vs read-only?"* |
| *"Why does this system exist and what is the status-quo cost?"* | *"What does the first-time-user state need to show so a new user can start?"* |

The shorthand: **BA asks *what / why / who-has-authority / when / how-much* about the requirement (scope, rules, data ownership, success metrics); UX asks *which user, what context, which task-decision, what on-screen data, what failure-state, what trust-signal* about the user-facing behaviour.** A question about business scope, rule ownership, sign-off authority, justification, or a business success metric is a BA question and belongs in the 10 BA Questions methodology.

The reviewer drops BA-lens candidates with `reason: ba-lens: <BA-Cn>` (the C-ID is the closest matching BA category from `ten-ba-questions-reference.md`).

This rule keeps the lens honest. If gate 9 (no-BA-overlap) fires at Step 7, the root cause is almost always a Step-5 rule-4 false-negative: a question that should have been dropped here escaped to selection.

### Diagnostics record

Every dropped candidate is logged in the in-memory diagnostics block with `{q_id_temp, category, reason}`. The diagnostics block in the final artefact summarises the drop counts (broken out per rule); it does not list every dropped question (the artefact stays scannable).

---

## Score-and-select rule (Step 6 of the agent workflow)

After Step-5 filtering, the reviewer scores each surviving candidate and selects the top 10.

**Score formula:**

```
score = design_impact × answerability_gap
```

Both factors are 1..5. Maximum score is 25 (a question that would massively change the design *and* is entirely untouched by the corpus). Minimum score is 1 (refinement-pass details the corpus mostly settles).

**Sort:** descending by `score`.

**Tie-breaker order** (deterministic):

1. Higher `design_impact` wins (a high-impact question is preferred to an equally-scored low-impact one with high gap).
2. Earlier category index wins (C1 before C2, etc.), so `Users & segmentation` is preferred to `Trust, transparency, audit` on a tie.
3. Original generation order (the `T-NN` index assigned at Step 4) wins.

**Select:** the top 10 candidates.

**Final ID assignment:** Selected candidates are renumbered `UXQ-01` through `UXQ-10` in score-descending order (`UXQ-01` is the highest-scoring question, `UXQ-10` is the lowest of the ten selected). This makes the rendered Triage table's top entry the highest-priority question, regardless of category.

**Priority confirmation:** For each of the ten selected, re-confirm the `draft_priority` against the rubric below:

- If `draft_priority: minor` and `design_impact ≥ 4`: escalate to `major` (a high-impact question is never `minor`).
- If `draft_priority: blocking` and `design_impact ≤ 2`: downgrade to `major` (`blocking` requires real design impact).
- Otherwise: keep `draft_priority` as the final priority.

Re-confirmation is **per-candidate**. There is no global quota.

---

## Priority rubric (canonical)

Every selected question carries exactly one of three priorities. The rubric is operational, not philosophical — the test below is what the designer actually applies.

### blocking

- Without an answer, the design **cannot proceed** because two or more plausible interpretations of the question would yield **contradictory designs**.
- Operational test: *"Could a designer sketch a sensible first wireframe without the answer?"* — **No.**
- Typical signal: `design_impact = 5` (different layout/control/flow) **and** `answerability_gap = 4..5` (no source gives the designer purchase to default).
- Example: *"The interview names 'Approver' and 'Reviewer' separately, but the workshop notes attribute 'review and approve' to a single actor — are these one role or two?"*. Until resolved, the role-switcher chrome (`PI-05`) and the queue screens cannot be designed: one approver role has one switcher entry and one queue; two distinct roles need two.

### major

- An answer **materially changes design direction** (different screen, different control type, different flow), but design can proceed with a **stated default** while the stakeholder decides, at documented downstream cost.
- Operational test: *"Could a designer sketch a sensible first wireframe without the answer?"* — **Yes, but with a documented assumption that may be wrong.**
- Typical signal: `design_impact = 3..5` and `answerability_gap = 2..4`.
- Example: *"How frequently does an Importer process imports — daily, weekly, monthly?"*. Drives at-a-glance density vs context-per-record layout. A designer can default to "weekly" and ship a wireframe, but the cost of being wrong is a re-design of the primary screen.

### minor

- Answer affects **refinement only**. A reasonable default produces an **acceptable** design that can be tuned later without re-thinking the screen's structure.
- Operational test: *"Could a designer sketch a sensible first wireframe without the answer?"* — **Yes, and a reasonable default will probably stick.**
- Typical signal: `design_impact = 1..2` and `answerability_gap = 1..3`.
- Example: *"Should the import history list show absolute timestamps or relative-time strings ('5 minutes ago')?"*. Either is workable; the answer is a polish-pass detail.

There is no fourth priority. *"Could-be-clearer"* is not a priority — either the answer changes the design (`major` or `blocking`) or it tunes a detail (`minor`), or it isn't a UX question at all and should not have survived the filter.

---

## Output presentation

The artefact renders as a self-contained HTML report following `framework/assets/reviews-inputs/template-ten-ux-questions.html`. The fixed section ordering is:

1. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead: what this review is, what it found, what the consultant should do next. The first content section, above the Executive Summary. A faithful condensation of the findings — it introduces no finding or count not in the punch-list, and **preserves priority verbatim** (a blocking question is stated unsoftened). Review jargon is glossed at first use here; client domain terms are not. Per `framework/shared/output-readability.md`.
2. **Header** — title, generated-at timestamp, manifest fingerprint, reviewer identity, priority counts (blocking / major / minor), category coverage summary.
3. **Triage** — single ordered table listing all 10 questions with rank, ID, priority, category, source, and the question's first line.
4. **Questions** — one block per question (`UXQ-01` … `UXQ-10`) with full text, source, priority, category, and the 1–2 sentence rationale.
5. **Diagnostics** — candidate pool size, drop counts (`GR-NN`, `PI-NN`, out-of-scope, BA-lens), category coverage (which of C1..C8 produced at least one finalist), quality-gate results, **Corpus Shape**, and the **source rosters** (consumed + skipped).

The artefact is a **triage list**, not a narrative — with **one** sanctioned narrative exception: the "In plain terms" lead at the very top (a short plain-English orientation that preserves priority, never softens it). Prose between questions is minimised; the consultant should be able to read the Triage table in under two minutes, then jump straight to the question block for context on any entry.

---

## Voice and stance

The reviewer's stance is defined in `framework/assets/characters/ten-ux-questions-inputs-review.md` — experienced UX designer, pattern-aware, accessibility-conscious, gap-discovery, non-confrontational, asks designer kick-off questions not corpus-defect citations and not business-scope questions. The reference defines **what** to do; the character file defines **how** the agent talks while doing it. The `Reader & plain language` section of the character file specifically governs the "In plain terms" lead (`{{PLAIN_SUMMARY}}`): plain-English orientation, jargon glossed at first use, client domain terms not glossed, priority preserved verbatim, punch-list discipline below.

---

## Quality gates (run after Step 6, before write)

Eleven gates. All are hard. If any gate fails, the reviewer does **not** write the artefact — it surfaces a structured error and halts. (See `framework/agents/reviews-inputs/ten-ux-questions-reviewer.md > Step 7 — Validate` for the halt contract.)

1. **Exactly 10 questions in the final output.** No padding, no overflow.
2. **Candidate pool size ≤ 50.** The Step-4 cap is enforced. The pool size is recorded in the diagnostics block.
3. **Every question has a `priority ∈ {blocking, major, minor}`.** No `critical`, no `nit`, no blank.
4. **Every question has a non-empty 1–2 sentence rationale.** Rationale ≥ 1 sentence, ≤ 3 sentences. Stub rationales (*"important"*, *"matters"*) are a gate failure.
5. **Every question has source provenance.** Either (a) `[SRC: <filename>]` where `<filename>` is a consumed source from the Step-2/3 manifest ingest (a filename in the consumed-filename set), or (b) `absent-from-corpus` (optionally `absent-from-corpus: <topic>`) for a topic absent from every consumed source.
6. **No question's topic is resolved by any active `GR-NN`.** Verified by re-running the Step-5 rule-1 check against the selected ten.
7. **No question is out-of-scope per `prototype-scope.md`.** Verified by re-running the Step-5 rule-3 check.
8. **Category coverage: the 10 questions span ≥ 5 of the 8 UX categories.** Prevents the score-only ranking from collapsing the output into one or two categories.
9. **No BA-lens overlap.** Verified by re-running the Step-5 rule-4 check against the selected ten. Any BA-categorised question is a defence-in-depth catch of a filter false-negative. This is the methodology's most distinctive guard — the orthogonality contract between the UX and BA lenses.
10. **Manifest fingerprint recorded and consistent.** The artefact's `MANIFEST_FINGERPRINT` field is non-empty and equals the SHA-256 of `requirements/source-manifest.json` captured at Step 2 — so the artefact records exactly which manifest version it reviewed.
11. **Source roster complete.** Every manifest row is accounted for: each `tier != "Unsupported"` row appears in the Source roster (Consumed) table, and each `tier == "Unsupported"` row appears in the Source roster (Skipped) table with its reason. No manifest row is silently dropped.

---

## Anti-patterns

- **Returning fewer or more than 10 questions.** The output is a fixed-size triage list. The selection rule is the value of this methodology.
- **Skipping the candidate pool.** *"Top 10"* without a 50-candidate pool means *"first 10"* — the prioritisation is performative without the larger surface to sort against.
- **Crossing into adversarial-review.** *"This mockup is poorly drawn"* is an adversarial finding, not a UX question. If a candidate reads like a corpus-defect citation, rewrite it as a question about what the user-experience the inputs have not yet settled, or drop it.
- **Crossing into BA-review.** *"What is the decision logic for the approval?"* is a BA question; *"What does the approver need on-screen to decide?"* is the UX question. Rule 4 of Step 5 drops the former; gate 9 catches escapees. A UX reviewer that asks scope / rules / data-ownership / sign-off-authority / business-metric questions is implementing the wrong methodology.
- **Asking design-decision questions instead of discovery questions.** *"Should this be a table or cards?"* is a design decision the system holds authority over — not a stakeholder question. The UX lens surfaces what the designer needs to *know* (who the user is, their context, their task decisions, the data they need to see), not what the designer will *choose*. The "which control / which layout" decisions are the system's to make downstream.
- **Proposing answers.** This reviewer does not draft tentative answers. *"How often do they import? (Likely weekly.)"* is forbidden. The `[AI-SUGGESTED]` lane belongs to the `/requirements` drafter.
- **Re-asking what the framework already resolves.** Any candidate whose answer is in a `GR-NN`, contradicts a `PI-NN`, or contradicts `prototype-scope.md` is dropped at Step 5 — and gate 6 or 7 catches it if it escapes. This bites hardest for the UX lens, whose surface overlaps the `GR-NN` set the most.
- **Mono-category output.** Ten questions all in C4 (tasks & flows) is a coverage failure even if every one scores highly. Gate 8 enforces ≥ 5 of 8 categories.
- **Bundling questions.** *"Who is the user and how often and on what device?"* is three candidates. Split.
- **Padding the blocking count.** A corpus that genuinely covers the basics legitimately produces zero blockings. *"Make sure there's at least one blocking"* is not a quota; the priority distribution falls out of the corpus.
- **Generic questions.** *"What about the user experience?"* is not a finding. Cite the source (or mark it absent-from-corpus); state the specific design decision the answer would unlock.
- **Phantom sources.** A question citing `[SRC: ghost.docx]` when no manifest row consumed `ghost.docx` is a gate-5 failure. Use the Step-2/3 consumed-filename set to validate every citation. Cite filenames only — never line numbers (multimodal sources have no lines; `.converted.md` line numbers drift between markitdown runs).
- **Reviewing against derivatives.** Do not consult `requirements/requirements.md` or `analyse-*` outputs to triangulate gaps. The review's contract is to read the **raw inputs** enumerated by the manifest as the source of truth.

---

## References

- **Erika Hall — *Just Enough Research*** (Rosenfeld Media, 2nd ed. 2019). Discovery-phase question framework: users, contexts, goals, behaviours.
- **Nielsen Norman Group — Discovery-phase questions.** The standard discovery framework covers users, content, tasks, business, context-of-use; C1, C4, C5, and C2 are direct descendants.
- **Bob Moesta — Jobs-To-Be-Done interview structure** (*Demand-Side Sales 101*, Lioncrest 2020). The JTBD forces underpin C3 (goals & success signals) and C6 (errors & recovery).
- **Don Norman — *The Design of Everyday Things*** (Basic Books, revised 2013). The gulfs of execution and evaluation underpin C5 (data for decisions) and C8 (trust & transparency).
- **Rob Fitzpatrick — *The Mom Test*** (CreateSpace 2013). The distinction between *decision-changing* questions and *opinion-soliciting* questions underpins the priority rubric — a question only counts as `blocking` if its answer changes the design.
- **Lou Rosenfeld, Peter Morville, Jorge Arango — *Information Architecture*** (O'Reilly, 4th ed. 2015). Content-and-structure starter questions underpin C5 (decision-supporting content) and C7 (collaboration & visibility).

The synthesised eight-category structure is shared with `framework/assets/reviews/ten-ux-questions-reference.md`; this reference's own contribution is mapping it onto the raw input corpus (where gaps surface as `absent-from-corpus` or partially-touched material), binding the lens orthogonally against the adjacent 10 BA Questions methodology (`reviews-inputs/ten-ba-questions-reference.md`), and respecting the framework's deterministic-answer set (`GR-NN`, `PI-NN`, `prototype-scope.md`).
