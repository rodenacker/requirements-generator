<!-- ROLE: asset (review reference). Loaded by framework/agents/reviews-inputs/ten-ba-questions-reviewer.md at activation. -->

# reviews-inputs/ten-ba-questions-reference.md

**Purpose:** Methodology reference for the **10 BA Questions** review of the **raw consultant input set** — the material in `input/` enumerated by `requirements/source-manifest.json`. The reviewer follows this document literally and exhaustively. This is the inputs-side sibling of `framework/assets/reviews/ten-ba-questions-reference.md` (which runs the same lens against the merged `requirements/requirements.md`); the two are deliberately parallel so a consultant who knows one can read the other without re-learning the structure.

**Used by:**

- `framework/agents/reviews-inputs/ten-ba-questions-reviewer.md` — drives the agent's source-ingest, candidate-generation, filter, score-and-select, validate, render, and write workflow.

**Output produced by the reviewer:** `review-inputs/TEN-BA-QUESTIONS/ten-ba-questions-review.html` — a self-contained HTML report listing the ten most pressing **unanswered** questions an experienced Business Analyst (BABOK-aware) would put back to the business stakeholder after carefully reading the raw input corpus, each tagged `blocking | major | minor`, each carrying a source provenance (`[SRC: <filename>]` for material the corpus partially touches, or `absent-from-corpus` when the whole topic is missing from every source), each with a 1–2 sentence rationale on the business impact of leaving the question unanswered. Selection is from a candidate pool of up to 50.

The scaffold for the artefact is `framework/assets/reviews-inputs/template-ten-ba-questions.html`.

---

## What "10 BA Questions" means (inputs-side)

The discipline mirrors how an experienced Business Analyst reviews a pile of raw client material — briefs, interview notes, decks, screenshots, spreadsheets, workshop captures — **before** turning it into a structured requirements document. After reading the gathered material carefully, the BA asks: *"Before I let this be drafted into requirements, what are the unanswered questions whose answers would change the scope, the rules, the data model, or what 'done' means?"*. The answer is rarely "everything is clear"; it is also rarely "everything is missing". It is usually a **short, prioritised list of questions** that span a few requirements-shaping categories, each of which would change the eventual build if answered differently.

This methodology operationalises that practice as a deterministic, registry-driven review. The reviewer:

1. Reads `requirements/source-manifest.json` and ingests every consumable source file (Step 2–3 of the agent workflow).
2. Generates up to **50 candidate questions** across **8 BA gap categories** (Step 4).
3. Filters the candidates against the framework's deterministic answer set and against the adjacent UX-questions lens (Step 5) — dropping any question whose answer is already encoded in the framework, whose topic is out of scope, or whose lens belongs to the 10 UX Questions methodology.
4. Scores each surviving candidate by `(business-impact × answerability-gap)` and selects the **top 10** (Step 6).
5. Assigns each selected question a priority — `blocking | major | minor` — per the rubric below (Step 6).
6. Renders the output with provenance, rationale, and a triage table (Steps 8–9).

The output is a **stakeholder-conversation punch-list**, not a corpus defect report and not a design critique. It tells the consultant: *here are the ten things you should go back and ask the business about before `/requirements` drafts from this material.* Because the inputs are pre-spec, elicitation is unambiguously still open — this lens is at its most natural one stage earlier than its requirements-side twin.

### How this differs from the other `/review-inputs` lenses

| Lens | Stance | Output | Remediation owner |
|---|---|---|---|
| **adversarial** | *"What is wrong inside the corpus?"* (defect extraction) | A cited finding of fact about a corpus defect, with a corpus-handling disposition (Patch / Defer / Reject). | Consultant — handles the existing material. |
| **completeness-review** | *"What's missing, measured against the BA canon (IEEE/Volere/BABOK)?"* (exhaustive coverage audit) | Every coverage gap across ten dimensions, each classified Needs-Clarification / Standard-Rule-Applies / Out-of-Scope, with a per-finding elicitation question. | Stakeholder — answers the elicitation questions. |
| **gap-analysis** | *"What's missing, measured against this project's requirements template?"* | Every gap scored Impact × Confidence → MoSCoW, each Must/Should carrying a shall-form candidate requirement. | Consultant — ratifies, edits, or rejects each candidate. |
| **ambiguity-review** | *"What is worded loosely?"* (clarity defects) | Every ambiguous passage, keyed by ambiguity type, with a clarifying stakeholder question. | Stakeholder — pins down the intended meaning. |
| **ten-ba-questions** | *"What's missing from a Business Analyst's perspective — the most consequential things the business hasn't told us yet?"* (consequence-ranked gap-discovery) | **Exactly 10** consequence-ranked stakeholder questions across the 8 BA gap categories — **no per-finding disposition, no candidate requirement, no per-passage defect**; a scannable executive punch-list. | Stakeholder — answers; the consultant folds the answers into `input/` before drafting. |

The load-bearing differentiator: where `completeness-review` and `gap-analysis` are **exhaustive** coverage audits (every gap, each with a disposition or a candidate requirement), **ten-ba-questions is a ruthless top-10 triage** — *"if you only get to ask the business ten things before we draft, ask these."* It deliberately produces a fixed-size, consequence-ranked, scannable list rather than a full register. Running it alongside its siblings is the intended workflow: the BA questions are the executive shortlist; the others are the full coverage maps.

### Why "10"? Why "from 50"?

10 is small enough that a consultant can review every question in one sitting and decide which to send back to the stakeholder. 50 is the working-pool ceiling: broad enough that the score-and-select pass has meaningful options across categories, tight enough that one agent pass can generate, score, and rank deterministically without context bloat. The 50 → 10 ratio is the prioritisation mechanism — without a candidate pool, "top 10" would just be the first 10.

The two numbers mirror the existing 10 UX Questions and (requirements-side) 10 BA Questions methodologies for two reasons:

- **Parity** — consultants who already know the requirements-side flavour can read the inputs-side flavour without re-learning the structure.
- **Practical sitting-time** — 10 questions × ~30 seconds each = a single 5-minute review cycle for the consultant.

---

## Sources and defensibility

The eight-category taxonomy and the priority rubric are not inventions of this file. They synthesise five reputable sources:

- **BABOK® Guide v3** (IIBA, 2015). The *Elicitation & Collaboration* knowledge area validates systematic questioning as a core BA competency. BABOK lists 50 documented techniques across interviews, workshops, document analysis, brainstorming, and surveys; the categories here cover the gap-types those techniques are designed to surface. (Authoritative professional framework.)
- **TechCanvass — *10 Requirements Gathering Questions for a Business Analyst*** (Business Analyst blog series). Direct prior art for the "10 questions" framing; ten high-value BA questions across problem statement, status quo, users, success, current process, failure modes, decision support, anti-goals, error handling, and assumptions. Pull-quote: *"Requirements fail on clarity, and clarity almost always comes from asking better questions — not more questions."*
- **Kipling — *The Elephant's Child*** (*"Six Honest Serving Men"*: Who, What, When, Where, Why, How), revived as a BA heuristic by Mike Cohn and others. Used here as a cross-check: every BA category in this reference touches at least one of the Six Honest Serving Men so the question-space is fully covered.
- **Prolifics Testing — *Ten Attributes of a Testable Requirement*** (clarity, completeness, ambiguity, testability, correctness, consistency, traceability, feasibility, modifiability, prioritisation). The five quality dimensions a BA's question pulls on are reflected in the priority rubric (a blocking question maps to a clarity / ambiguity / completeness failure that prevents test-case design).
- **QA Madness — *Bug Severity vs Priority*** (canonical defect-management severity tiers: Blocker / Critical / Major / Minor). Direct prior art for the `blocking / major / minor` priority labels and their semantics, mapped onto *unanswered requirements questions* instead of *implemented-but-broken behaviour*.

The synthesis is this reference's own contribution: integrate BABOK's Elicitation taxonomy with the Six Honest Serving Men, map them onto the framework's data-management/productivity-app target domain (CRUD-shaped, per `CLAUDE.md`'s framework-domain constraint), and bind the priority labels to canonical defect-severity practice — yielding an auditable pass-per-category methodology that respects the framework's deterministic-answer set (`GR-NN`, `PI-NN`, `prototype-scope.md`) and the adjacent UX-questions lens (`framework/assets/reviews/ten-ux-questions-reference.md`).

---

## Upstream input contract

The reviewer reads **only** the following:

- `requirements/source-manifest.json` — the manifest enumerating consumable input files. Read once at Step 2. This is the entry point to the critique target.
- The files the manifest enumerates — for each row where `tier != "Unsupported"`: the file at `original_path` (for `Native-text` and `Native-multimodal`) or `converted_sibling` (for `Supported-via-MCP`). Read once per row at Step 3. These are the critique target.
- `framework/assets/characters/ten-ba-questions-inputs-review.md` — the character file. Read once at Step 1.
- `framework/assets/reviews-inputs/ten-ba-questions-reference.md` — this document. Read once at Step 1.
- `framework/assets/reviews-inputs/template-ten-ba-questions.html` — the HTML scaffold. Read once at Step 8 (render).
- `framework/shared/general-rules.md` — read at Step 5 as a **filter source**. The reviewer scans each candidate question against the `GR-NN` rule list and drops candidates whose topic is deterministically answered.
- `framework/shared/prototype-invariants.md` — read at Step 5 as a **filter source**. The reviewer drops candidates whose underlying premise contradicts a `PI-NN` invariant.
- `framework/shared/prototype-scope.md` — read at Step 5 as a **filter source**. The reviewer drops candidates whose topic is out-of-scope for prototype mode.
- `framework/assets/reviews/ten-ux-questions-reference.md` — read at Step 5 as a **filter source** for the UX-lens-drop rule (rule 4 below). The reviewer drops candidates whose question shape matches a UX category from that reference. (There is no inputs-side UX-questions methodology; this reference is reused read-only purely as the UX-classification rubric — the same way the requirements-side BA reviewer uses it.)

It does **not** consult:

- `requirements/requirements.md`, `requirements/requirements-draft.md`, `requirements/consultant-answers.md`, `requirements/draft-claims*.ndjson` — `/requirements`-pipeline artefacts. The review's contract is to critique **raw inputs**, not anything synthesised from them. Reviewing the inputs against a document drafted from those same inputs would conflate "what the corpus says" with "what the drafter inferred".
- `analyse-requirements/*`, `analyse-inputs/<METHOD>/*` outputs — derived artefacts; each input-pipeline lens is independently grounded in the manifest.
- `design-system/*` outputs — not relevant to a BA questions review.
- `framework/state/*` — pipeline state is not a review input.
- Any other file under `framework/shared/` (e.g. `refusal-registry.md`) — referenced by ID only, not read by this agent.

The raw input corpus is the contract. If no source says it, and no `GR-NN` / `PI-NN` answers it, and it's in-scope per `prototype-scope.md`, and it doesn't belong to the UX lens — it is a candidate gap.

---

## The eight BA gap categories

Eight categories, applied to every candidate question. They cover the requirements-shaping surface a Business Analyst needs to interrogate before the material is drafted into requirements. They are framed around **decisions a stakeholder must make**, not around document sections — a question can target a topic wholly absent from the corpus as readily as one that a single source mentions in passing.

### C1 — Problem & justification

**Question shape:** Why does this system exist? What does the status quo cost? What event or pressure triggered the work?

**What to ask about:**

- The actual problem being solved (often elided into a solution statement). *"The brief says we will build a 'centralised import tool' — what is the current state that makes the existing approach unsustainable?"*
- Status-quo cost. If the team doesn't build this, what continues to happen? Quantified or anecdotal cost.
- Triggering event. New regulation, lost revenue, competitor move, leadership directive — *why now?*
- Anti-goals. What this system explicitly is **not** trying to do, even though a casual reader of the inputs might assume otherwise.
- Alternative options considered. Buy-vs-build, incremental fix, process change instead of software change.

**Where this surfaces in a corpus:** problem framing usually lives in the kickoff brief or executive deck; commonly an `absent-from-corpus` gap when the inputs are solution-led (a feature list, a set of mockups) with no problem statement behind them.

### C2 — Stakeholders & users

**Question shape:** Who is impacted by this system, in enough detail that the BA can route questions, the designer can pick density, and the dev can scope role-based logic?

**What to ask about:**

- Decision-makers vs. operators vs. downstream consumers. Often only "users" appear in the inputs; the sign-off owner, the budget owner, and the consumer of the output are distinct stakeholders.
- Segmentation within a single role. *"The interview names an 'Importer' — are there power-users (bulk-import 100+ files daily) and casual-users (one file per week) within this persona, and do they have different needs?"*
- Expertise variance. Domain experts vs novices need different terminology, different inline help, different defaults.
- External stakeholders. Auditors, regulators, partners, customers — does any external party have a stake in this system's behaviour?
- Sign-off owner per requirement area. Who, by name or by role, has authority to call this requirement "right"?

**Where this surfaces in a corpus:** stakeholder maps, org charts, or interview rosters when present; frequently an `absent-from-corpus` gap when the inputs name roles only incidentally. (Note: questions about *how* a user interacts on-screen belong to the UX lens; this category asks *who* they are and *what stake* they have.)

### C3 — Success & acceptance criteria

**Question shape:** How will the business know this system did its job? What is the measurable signal of "done"? Who has authority to call it done?

**What to ask about:**

- Quantified success signals. Revenue, cost saved, time saved, error rate reduced, throughput increased — at what threshold is the business satisfied?
- Outcome definitions per goal. *"The deck lists a goal to 'manage approvals' — what business metric distinguishes successful manage-approvals from unsuccessful manage-approvals?"*
- Acceptance criteria per feature. The inputs may name features without any testable notion of "passing" — what does success look like for each?
- Time-to-value. When does the business expect to see the impact — at go-live, after 30 days, after a quarter?
- Sign-off authority. Who, by role, can declare a requirement satisfied?

**Where this surfaces in a corpus:** OKR docs, business cases, or success-metric slides when present; commonly `absent-from-corpus` when the inputs describe features but not outcomes.

### C4 — Scope & MVP boundaries

**Question shape:** What is in this release? What is explicitly deferred? What was considered and rejected? What is implied but unstated?

**What to ask about:**

- MVP vs post-MVP per feature. The inputs name features; which are mandatory for go-live and which are phase-two?
- Explicit non-goals. Features the inputs could be read as including but that the team has decided to defer.
- Phase ordering. If the team is shipping in phases, what is the dependency-respecting sequence?
- Implied scope creep. Phrases like "support workflow", "integrate with finance", "enable reporting" — how much of those is in scope vs aspirational?
- Out-of-scope clarifications. *"A slide mentions 'future reporting requirements' — is any reporting in this release, or is the note forward-looking only?"*

**Where this surfaces in a corpus:** roadmap decks, scope sections of a SOW, or MVP slides when present; often an `absent-from-corpus` gap when the inputs are a flat feature list with no phase markers.

### C5 — Business rules & decisions

**Question shape:** What is the decision logic the system implements? Who is the authoritative owner of each rule? What happens when rules conflict?

**What to ask about:**

- Decision logic per feature. *"A note says 'approve transactions over a threshold' — who sets the threshold, and what is it today?"*
- Approval workflows. Sequential, parallel, conditional? Who has veto authority? What happens on no-response?
- Eligibility rules. Which records or users qualify for a feature, and what data drives the qualification?
- Calculation rules. Pricing, scoring, scoring tiebreakers, rounding — the inputs may name the calculation without giving the formula.
- Rule ownership. When two rules conflict, whose call wins? What is the precedence?
- Rule lifecycle. How are rules added, retired, or versioned? Are old records evaluated under old rules?

**Where this surfaces in a corpus:** process docs, policy documents, or spreadsheets encoding rules when present; the most-asked category on rule-heavy domains, and frequently under-specified in raw inputs.

### C6 — Data, entities & integrations

**Question shape:** What is the authoritative source of each piece of data? How do entities relate? What systems must this exchange data with?

**What to ask about:**

- Authoritative source per entity. *"A spreadsheet references a `Customer` record — is this system the system of record, or does it pull from CRM?"*
- Identifier policy. Internal IDs, external IDs, natural keys — which is authoritative, and what are the uniqueness rules?
- Entity lifecycle. Creation source, edit authority, retention, archival, deletion — and which roles touch each phase.
- Required integrations. What external systems must this exchange data with, in what direction, at what cadence?
- Data residency / locality. Where is data stored? Are there jurisdictional rules (GDPR, POPIA, HIPAA) the inputs have implied but not stated?
- Volume and growth assumptions. What is the expected size at year-1 vs year-3?

**Where this surfaces in a corpus:** data dictionaries, ERDs, sample spreadsheets, or integration diagrams when present; an `absent-from-corpus` gap if the inputs name entities only by example without a data model.

### C7 — Edge cases & exception flows

**Question shape:** What happens when the assumed preconditions fail? How does the business want the system to recover?

**What to ask about:**

- Missing-data flows. What is the system's behaviour when a required field is unavailable at the moment of decision?
- Conflict resolution. Two users / two systems / two rules disagree — what is the business policy?
- Permission denial. The inputs list who *can* do things; what happens when someone tries who *can't*, and what does the business want logged?
- Partial-failure recovery. A bulk operation succeeds 80% — what is the business expectation: retry, accept partial, escalate?
- Timeouts and SLAs. What is the business's expectation when a downstream system doesn't respond?
- Exception escalation. Who is contacted when the system can't proceed? Via what channel?

**Where this surfaces in a corpus:** runbooks, exception logs, or support tickets when present; frequently an `absent-from-corpus` gap when the inputs cover only happy paths (the common case for mockups and demo scripts).

### C8 — Assumptions, dependencies & sequencing

**Question shape:** What is the corpus taking for granted? What must be true elsewhere before this can ship? In what order must things happen?

**What to ask about:**

- Implicit assumptions. *"The workshop notes assume the user is logged in before initiating an import — is authentication in scope, or does this feature ship behind an interim mechanism?"*
- Cross-team dependencies. What does this feature need from another team (data feed, API contract, design system, content) and is that on their roadmap?
- Cross-system dependencies. What must exist or be configured in an upstream system before this can go live?
- Sequencing constraints. Feature B cannot launch before Feature A — do the inputs say this?
- Resource assumptions. Headcount, vendor availability, training delivery — anything the inputs presume but don't name.
- Risk-bearing assumptions. The one or two assumptions that, if wrong, would force a major redesign.

**Where this surfaces in a corpus:** risk registers, dependency lists, or project plans when present; spans multiple sources and is commonly the most-missed category in a raw input set.

---

## Candidate-pool generation rules (Step 4 of the agent workflow)

The reviewer produces up to **50** candidate questions in a single pass, with explicit per-category quotas:

| Category | Soft quota (candidates) |
|---|---|
| C1 Problem & justification | 5–7 |
| C2 Stakeholders & users | 5–7 |
| C3 Success & acceptance criteria | 5–7 |
| C4 Scope & MVP boundaries | 5–7 |
| C5 Business rules & decisions | 6–8 |
| C6 Data, entities & integrations | 6–8 |
| C7 Edge cases & exception flows | 5–7 |
| C8 Assumptions, dependencies & sequencing | 5–7 |

The quotas are **soft**: they aim for ~50 candidates spread across 8 categories. If the corpus is genuinely silent on a whole category (e.g., a single-stakeholder app may have no meaningful C8 cross-team-dependency candidates), the candidate count for that category may be zero — but the agent must record in the diagnostics block why the category produced zero, not just emit zero silently.

### Candidate schema (in-memory; never written verbatim to disk)

Each candidate is a JSON-shaped record in memory:

```
q_id_temp:           T-NN          (temporary index used during scoring; overwritten with BAQ-NN at selection)
category:            C1..C8
question_text:       string         (one-sentence question, ≤ 2 lines, BA-phrased — kick-off-meeting voice)
source:              "[SRC: <filename>]" | "absent-from-corpus" | "absent-from-corpus: <topic>"
business_impact:     1..5           (how much the answer would change scope, estimate, or risk — 5 = different scope/rules/data; 1 = polish-pass)
answerability_gap:   1..5           (how unanswered the question is across the corpus — 5 = no source touches it at all; 1 = one source mentions it in passing)
draft_priority:      blocking | major | minor   (the priority the reviewer would assign if this candidate were selected)
rationale:           string         (1–2 sentences explaining the business impact of leaving the question unanswered)
```

A candidate missing any field is invalid and not eligible for selection.

### Candidate-quality rules (applied during generation)

- **One question per candidate.** A candidate that bundles two questions (*"who approves and what are the criteria?"*) is split into two candidates.
- **Specific source provenance only.** A candidate grounded in material the corpus partially touches cites the **specific filename** where that material appears: `[SRC: <filename>]` (the basename from the manifest row). If the whole topic is absent from every consumed source, mark `source: absent-from-corpus` (optionally `absent-from-corpus: <topic>` for a one-word topic tag).
- **BA-phrased questions.** The question text reads as something a BA would ask in a kick-off meeting with the business stakeholder. *"For the approval rule in `process-notes.md`, who is the authoritative decision-owner if two stakeholders disagree?"* — not *"`process-notes.md` is unclear about rule ownership"*.
- **No GR / PI / scope / UX-lens violations.** If a candidate's answer is deterministically supplied by an active `GR-NN`, or contradicts a `PI-NN` invariant, or falls outside `prototype-scope.md`, or fits a UX category from `ten-ux-questions-reference.md`, drop it at Step 5 — but it is fine for it to be generated in Step 4 and then filtered, as long as the filter catches it.
- **No tentative answers.** The reviewer does not include proposed answers in candidate `question_text` or `rationale`. The rationale explains business impact, not what the answer should be.

---

## Filter rules (Step 5 of the agent workflow)

After generating the candidate pool, the reviewer reads four filter sources and drops every candidate that matches one of the rules below.

### Filter source reads (Step 5 only)

- `framework/shared/general-rules.md`
- `framework/shared/prototype-invariants.md`
- `framework/shared/prototype-scope.md`
- `framework/assets/reviews/ten-ux-questions-reference.md`

The four reads are scoped to this step and are the agent's **only** reads outside its own asset set, the manifest, and the manifest-enumerated source files.

### Rule 1 — `GR-NN` no-re-ask filter

Each active `GR-NN` rule has a topic; a candidate whose question is answered by the rule is dropped. The live set lives in `framework/shared/general-rules.md` — the reviewer reads that file at Step 5 and walks the active rule IDs.

Most `GR-NN` rules answer UX-shaped questions (validation timing, required-field marking, pagination defaults, toast-vs-banner, etc.) and are therefore unlikely to collide with BA-shaped candidates. The collisions that **do** matter:

| `GR-NN` | Topic | BA question pattern the rule forecloses |
|---|---|---|
| GR-04 | Irreversible actions require modal confirmation | *"What is the business policy for irreversible operations? Should the system require explicit confirmation?"* (rule resolves it for the prototype) |
| GR-19 | Session timeout by domain (financial 15m, internal 30m, public 60m) | *"What is the session timeout policy?"* (rule resolves it by domain class) |

If a candidate falls under multiple `GR-NN` topics, the filter logs the first match and drops the candidate with `reason: gr-match: GR-NN`.

### Rule 2 — `PI-NN` premise filter

A candidate whose underlying premise contradicts a prototype invariant is dropped. The five active invariants:

| `PI-NN` | Invariant | BA question pattern the invariant forecloses |
|---|---|---|
| PI-01 | Server behaviour is simulated | *"What's the production API contract?"*, *"How is the database transaction committed?"* |
| PI-02 | Data is fixture-backed | *"What's the migration strategy from the old DB?"*, *"What is the data import frequency from production?"* |
| PI-03 | Validation is visual only | *"How does the server enforce uniqueness at scale?"*, *"What's the rate-limit policy in production?"* |
| PI-04 | Third-party integrations are visual | *"Which payment provider is contracted?"*, *"What's the email-service SLA?"* |
| PI-05 | Role switcher exists in prototype chrome | *"What's the production SSO provider?"*, *"How does the user log in as a different role outside the prototype?"* |

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

A candidate that names a server-side topic in its `question_text` is dropped with `reason: out-of-scope: <topic>`. BA questions about *business* policies for these areas (e.g., *"who owns the data-retention policy?"*) can be in-scope — the filter drops questions about *implementation*, not about *governance*.

### Rule 4 — UX-lens drop

A candidate whose question shape fits a UX category from `framework/assets/reviews/ten-ux-questions-reference.md > C1–C8` is dropped. The UX-vs-BA boundary:

| UX-lens question (drop here) | BA-lens question (keep here) |
|---|---|
| *"Which screen does the approval workflow live on?"* | *"What is the decision logic for the approval workflow?"* |
| *"What does the empty-state copy say when there are no records?"* | *"What is the business rule for when records appear in vs disappear from this list?"* |
| *"What information does the approver need on-screen to decide?"* | *"What is the business policy for what data may be visible at decision time, given privacy constraints?"* |
| *"What does partial-success of a bulk import look like to the user?"* | *"What is the business policy when 8 of 10 bulk-imported records succeed — retry, accept partial, or escalate?"* |
| *"How is the role-switcher exposed in the prototype chrome?"* | *"Which roles exist, who has sign-off authority on the role list, and what are the inter-role responsibilities?"* |

The shorthand: **BA asks *what / why / who / when / how-much* about the requirement; UX asks *which screen, which control, which layout, which interaction* about the user-facing behaviour.** A question that crosses the line is a UX question and belongs in the 10 UX Questions methodology.

The reviewer drops UX-lens candidates with `reason: ux-lens: <UX-Cn>` (the C-ID is the closest matching UX category from `ten-ux-questions-reference.md`).

This rule keeps the lens honest. If gate 9 (no-UX-overlap) fires at Step 7, the root cause is almost always a Step-5 rule-4 false-negative: a question that should have been dropped here escaped to selection.

### Diagnostics record

Every dropped candidate is logged in the in-memory diagnostics block with `{q_id_temp, category, reason}`. The diagnostics block in the final artefact summarises the drop counts (broken out per rule); it does not list every dropped question (the artefact stays scannable).

---

## Score-and-select rule (Step 6 of the agent workflow)

After Step-5 filtering, the reviewer scores each surviving candidate and selects the top 10.

**Score formula:**

```
score = business_impact × answerability_gap
```

Both factors are 1..5. Maximum score is 25 (a question that would massively change scope/rules/data *and* is entirely untouched by the corpus). Minimum score is 1 (refinement-pass details the corpus mostly settles).

**Sort:** descending by `score`.

**Tie-breaker order** (deterministic):

1. Higher `business_impact` wins (a high-impact question is preferred to an equally-scored low-impact one with high gap).
2. Earlier category index wins (C1 before C2, etc.), so `Problem & justification` is preferred to `Assumptions, dependencies & sequencing` on a tie.
3. Original generation order (the `T-NN` index assigned at Step 4) wins.

**Select:** the top 10 candidates.

**Final ID assignment:** Selected candidates are renumbered `BAQ-01` through `BAQ-10` in score-descending order (`BAQ-01` is the highest-scoring question, `BAQ-10` is the lowest of the ten selected). This makes the rendered Triage table's top entry the highest-priority question, regardless of category.

**Priority confirmation:** For each of the ten selected, re-confirm the `draft_priority` against the rubric below:

- If `draft_priority: minor` and `business_impact ≥ 4`: escalate to `major` (a high-impact question is never `minor`).
- If `draft_priority: blocking` and `business_impact ≤ 2`: downgrade to `major` (`blocking` requires real impact).
- Otherwise: keep `draft_priority` as the final priority.

Re-confirmation is **per-candidate**. There is no global quota.

---

## Priority rubric (canonical)

Every selected question carries exactly one of three priorities. The rubric is operational, not philosophical — the test below is what the BA actually applies.

### blocking

- Without an answer, **drafting requirements / estimation / scope cannot proceed**: two or more plausible answers would require **fundamentally different requirements**.
- Operational test: *"Could a senior BA draft a sensible requirement on this without the answer?"* — **No.**
- Typical signal: `business_impact = 5` (different scope or rules) **and** `answerability_gap = 4..5` (no source gives purchase to a default).
- Example: *"The interview names 'Approver' and 'Reviewer' separately, but the workshop notes attribute 'review and approve' to a single actor — are these one role or two?"*. Until resolved, the RBAC model and the approval workflow cannot be drafted: a single approver role has one decision path; two distinct roles have a two-stage workflow.

### major

- The answer **materially changes direction** (a workflow branch, an entity-model decision, a scope inclusion, a non-functional target). The team can draft with a **stated default** while the stakeholder decides, but the default carries documented risk.
- Operational test: *"Could a senior BA draft a sensible requirement on this without the answer?"* — **Yes, but with a documented assumption that may be wrong.**
- Typical signal: `business_impact = 3..5` and `answerability_gap = 2..4`.
- Example: *"What is the business policy for partial-failure on bulk import — retry, accept partial, or escalate?"* The team can default to "retry up to 3 times then surface the failed rows", but if the business wanted "fail-fast and escalate", the data-flow and the audit trail change.

### minor

- Answer affects **refinement only**. A reasonable default produces an acceptable requirement; the answer tunes details without re-thinking structure.
- Operational test: *"Could a senior BA draft a sensible requirement on this without the answer?"* — **Yes, and a reasonable default will probably stick.**
- Typical signal: `business_impact = 1..2` and `answerability_gap = 1..3`.
- Example: *"What is the business's expected retention period for audit-log entries — 90 days, 1 year, 7 years?"* Almost any reasonable answer is workable; the choice tunes a configuration value, not a feature.

There is no fourth priority. *"Could-be-clearer"* is not a priority — either the answer changes the requirement (`major` or `blocking`) or it tunes a detail (`minor`), or it isn't a BA question at all and should not have survived the filter.

---

## Output presentation

The artefact renders as a self-contained HTML report following `framework/assets/reviews-inputs/template-ten-ba-questions.html`. The fixed section ordering is:

1. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead: what this review is, what it found, what the consultant should do next. The first content section, above the Executive Summary. A faithful condensation of the findings — it introduces no finding or count not in the punch-list, and **preserves priority verbatim** (a blocking question is stated unsoftened). Review jargon is glossed at first use here; client domain terms are not. Per `framework/shared/output-readability.md`.
2. **Header** — title, generated-at timestamp, manifest fingerprint, reviewer identity, priority counts (blocking / major / minor), category coverage summary.
3. **Triage** — single ordered table listing all 10 questions with rank, ID, priority, category, source, and the question's first line.
4. **Questions** — one block per question (`BAQ-01` … `BAQ-10`) with full text, source, priority, category, and the 1–2 sentence rationale.
5. **Diagnostics** — candidate pool size, drop counts (`GR-NN`, `PI-NN`, out-of-scope, UX-lens), category coverage (which of C1..C8 produced at least one finalist), quality-gate results, **Corpus Shape**, and the **source rosters** (consumed + skipped).

The artefact is a **triage list**, not a narrative — with **one** sanctioned narrative exception: the "In plain terms" lead at the very top (a short plain-English orientation that preserves priority, never softens it). Prose between questions is minimised; the consultant should be able to read the Triage table in under two minutes, then jump straight to the question block for context on any entry.

---

## Quality gates (run after Step 6, before write)

Eleven gates. All are hard. If any gate fails, the reviewer does **not** write the artefact — it surfaces a structured error and halts. (See `framework/agents/reviews-inputs/ten-ba-questions-reviewer.md > Step 7 — Validate` for the halt contract.)

1. **Exactly 10 questions in the final output.** No padding, no overflow.
2. **Candidate pool size ≤ 50.** The Step-4 cap is enforced. The pool size is recorded in the diagnostics block.
3. **Every question has a `priority ∈ {blocking, major, minor}`.** No `critical`, no `nit`, no blank.
4. **Every question has a non-empty 1–2 sentence rationale.** Rationale ≥ 1 sentence, ≤ 3 sentences. Stub rationales (*"important"*, *"matters"*) are a gate failure.
5. **Every question has source provenance.** Either (a) `[SRC: <filename>]` where `<filename>` is a consumed source from the Step-2/3 manifest ingest (a filename in the consumed-filename set), or (b) `absent-from-corpus` (optionally `absent-from-corpus: <topic>`) for a topic absent from every consumed source.
6. **No question's topic is resolved by any active `GR-NN`.** Verified by re-running the Step-5 rule-1 check against the selected ten.
7. **No question is out-of-scope per `prototype-scope.md`.** Verified by re-running the Step-5 rule-3 check.
8. **Category coverage: the 10 questions span ≥ 5 of the 8 BA categories.** Prevents the score-only ranking from collapsing the output into one or two categories.
9. **No UX-lens overlap.** Verified by re-running the Step-5 rule-4 check against the selected ten. Any UX-categorised question is a defence-in-depth catch of a filter false-negative.
10. **Manifest fingerprint recorded and consistent.** The artefact's `MANIFEST_FINGERPRINT` field is non-empty and equals the SHA-256 of `requirements/source-manifest.json` captured at Step 2 — so the artefact records exactly which manifest version it reviewed.
11. **Source roster complete.** Every manifest row is accounted for: each `tier != "Unsupported"` row appears in the Source roster (Consumed) table, and each `tier == "Unsupported"` row appears in the Source roster (Skipped) table with its reason. No manifest row is silently dropped.

---

## Anti-patterns

- **Returning fewer or more than 10 questions.** The output is a fixed-size triage list. The selection rule is the value of this methodology.
- **Skipping the candidate pool.** *"Top 10"* without a 50-candidate pool means *"first 10"* — the prioritisation is performative without the larger surface to sort against.
- **Crossing into adversarial-review.** *"This brief is poorly written"* is an adversarial finding, not a BA question. If a candidate reads like a corpus-defect citation, rewrite it as a question about what the business has not yet answered, or drop it.
- **Crossing into UX-review.** *"Which screen does the approval live on?"* is a UX question; *"What is the decision logic for the approval?"* is the BA question. Rule 4 of Step 5 drops the former; gate 9 catches escapees. A BA reviewer that asks layout / control / copy / screen-flow questions is implementing the wrong methodology.
- **Proposing answers.** This reviewer does not draft tentative answers. *"Who is the approver? (Likely the Finance Manager.)"* is forbidden. The `[AI-SUGGESTED]` lane belongs to the `/requirements` drafter.
- **Re-asking what the framework already resolves.** Any candidate whose answer is in a `GR-NN`, contradicts a `PI-NN`, or contradicts `prototype-scope.md` is dropped at Step 5 — and gate 6 or 7 catches it if it escapes.
- **Mono-category output.** Ten questions all in C5 (business rules) is a coverage failure even if every one of them scores highly. Gate 8 enforces ≥ 5 of 8 categories.
- **Bundling questions.** *"Who approves and what are the criteria and what's the SLA?"* is three candidates. Split.
- **Padding the blocking count.** A corpus that genuinely covers the basics legitimately produces zero blockings. *"Make sure there's at least one blocking"* is not a quota the reviewer enforces; the priority distribution falls out of the corpus.
- **Generic questions.** *"What about scope?"* is not a finding. Cite the source (or mark it absent-from-corpus); state the specific decision the answer would unlock.
- **Phantom sources.** A question citing `[SRC: ghost.docx]` when no manifest row consumed `ghost.docx` is a gate-5 failure. Use the Step-2/3 consumed-filename set to validate every citation. Cite filenames only — never line numbers (multimodal sources have no lines; `.converted.md` line numbers drift between markitdown runs).
- **Reviewing against derivatives.** Do not consult `requirements/requirements.md` or `analyse-*` outputs to triangulate gaps. The review's contract is to read the **raw inputs** enumerated by the manifest as the source of truth.

---

## Voice and stance

The reviewer's stance is defined in `framework/assets/characters/ten-ba-questions-inputs-review.md` — experienced Business Analyst, BABOK-aware, gap-discovery, non-confrontational, asks stakeholder questions not corpus-defect citations and not designer questions. The reference defines **what** to do; the character file defines **how** the agent talks while doing it. The `Reader & plain language` section of the character file specifically governs the "In plain terms" lead (`{{PLAIN_SUMMARY}}`): plain-English orientation, jargon glossed at first use, client domain terms not glossed, severity preserved verbatim, punch-list discipline below.

---

## References

- **IIBA — *A Guide to the Business Analysis Body of Knowledge® (BABOK® Guide), v3*** (IIBA, 2015). The Elicitation & Collaboration knowledge area underpins the eight-category structure: every BA question category here surfaces a gap that one of BABOK's 50 documented elicitation techniques is designed to close.
- **TechCanvass — *10 Requirements Gathering Questions for a Business Analyst*** (`businessanalyst.techcanvass.com`). Direct prior art for the "10 questions" framing and a defensible mapping from problem-statement, status-quo, users, success, current-process, failure-mode, decision-support, anti-goal, error-handling, and assumption categories.
- **Rudyard Kipling — *The Elephant's Child*** (1902; the "Six Honest Serving Men" stanza). Used as a question-space coverage cross-check: each BA category in this reference must touch at least one of Who / What / When / Where / Why / How.
- **Karl Wiegers — *Software Requirements*** (Microsoft Press, 3rd ed. 2013). The requirements-quality dimensions (clarity, completeness, ambiguity, testability, correctness, consistency, traceability, feasibility, modifiability, prioritisation) underpin the priority rubric — a blocking question maps to a clarity or completeness failure that prevents downstream drafting or test-case design.
- **Tom Gilb — *Competitive Engineering*** (Elsevier, 2005). The Planguage notation for quantified requirements (scale, meter, must, plan, wish) is the origin of the C3 (success & acceptance criteria) emphasis on *measurable* signals.
- **B2B International — *Six Honest Serving Men in Market Research*** (2017, `b2binternational.com`). A modern restatement of the Kipling heuristic as a structured BA interview pattern.
- **QA Madness — *Bug Severity vs Priority*** (`qamadness.com`). Canonical precedent for the `blocking / major / minor` severity tier semantics, here mapped from "implemented-but-broken behaviour" onto "unanswered requirements question".

The synthesised eight-category structure is this reference's own contribution: it integrates BABOK's Elicitation taxonomy with the Six Honest Serving Men, the Wiegers/Gilb quality dimensions, and canonical defect-severity practice into one auditable pass-per-category methodology that maps cleanly onto the framework's raw input set and respects its deterministic-answer set (`GR-NN`, `PI-NN`, `prototype-scope.md`) and the adjacent UX-questions lens (`reviews/ten-ux-questions-reference.md`).
