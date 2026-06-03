<!-- ROLE: asset (review reference). Loaded by framework/agents/reviews/user-stories-reviewer.md at activation. -->

# reviews/user-stories-reference.md

**Purpose:** Methodology reference for the **User Stories** review of `requirements/requirements.md > §4.2 Stories by persona`. The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews/user-stories-reviewer.md` — drives the agent's enumeration, criterion-by-criterion evaluation, filter, grouping, validate, render, and write workflow.

**Output produced by the reviewer:** `review-requirements/USER-STORIES/user-stories-review.html` — a self-contained HTML report listing every user story in §4.2 that fails one or more of six quality criteria, sorted by priority (`blocking | major | minor`), grouped within each priority by persona then anchor, each finding annotated with the persona group, the violated criteria, the reason for each violation, and a concise fix suggestion. Passing stories are not surfaced in the body; their pass-count is recorded in the diagnostics block.

The scaffold for the artefact is `framework/assets/reviews/template-user-stories.html`.

---

## What "User Stories Review" means

The discipline mirrors how an experienced product owner / Business Analyst audits a story set before sending it into refinement, design, or estimation. After reading `§4.2 Stories by persona` carefully, the reviewer asks: *"Of the stories already in the doc, which ones are not yet ready for the next phase, and why?"*. The answer is rarely "everything is fine" and rarely "everything is broken"; it is usually a **priority-sorted punch-list of defective stories**, each with one or more issues that the consultant can address in a single rewrite per story.

This methodology operationalises that practice as a deterministic, registry-driven review. The reviewer:

1. Enumerates **every user story** in §4.2 — there is no candidate cap and no candidate pool, every story is evaluated (Step 2 of the agent workflow).
2. Evaluates each story against **six criteria** (Meaningful, Implementable, Testable, Coherent, Appropriately scoped, Outcome-aligned) and records one issue row per `(story, violated criterion)` pair (Step 3).
3. Filters issues against the framework's deterministic answer set (`GR-NN`, `PI-NN`) — Step 4.
4. Groups surviving issue rows into one finding per story; headline priority = max issue severity (Step 5).
5. Validates against 9 quality gates; halts on failure (Step 6).
6. Renders by priority (`Blocking` → `Major` → `Minor` sections), and within each priority by persona then anchor (Step 7–8).

The output is a **story-quality punch-list**, not a gap-discovery list and not a defect citation against the rest of the doc. It tells the consultant: *here are the stories you need to rewrite before the next phase, and here's why each is currently not ready.*

### How this differs from the other three `/review-requirement` lenses

| Lens | Stance | Output | Remediation owner |
|---|---|---|---|
| **adversarial** | *"What is wrong with this doc?"* (defect-finding) | A finding of fact about something malformed in the doc. | Consultant — edits the doc. |
| **ten-ba-questions** | *"What's missing from a Business Analyst's perspective?"* (BA gap-discovery) | A question about problem, scope, rules, data, success, stakeholders, dependencies. | Stakeholder — answers. |
| **ten-ux-questions** | *"What's missing from a designer's perspective?"* (UX gap-discovery) | A question about layouts, controls, copy, screen flows, interaction states. | Designer — interprets and decides. |
| **user-stories** | *"Which stories in §4.2 are not yet good stories?"* (story-quality audit) | A finding about a specific story that fails one or more of the six criteria, with reason and fix hint. | Consultant — rewrites the story. |

A requirements document can be BA-complete and story-defective (the rules and scope are clear, but the stories that encode them are vague), or story-clean and BA-incomplete (every story is well-formed but the underlying business decisions haven't been made). Running this lens alongside the BA-questions lens covers both cases.

### Why no cap on findings?

The two "10 questions" methodologies cap at 10 because a stakeholder-conversation list has a fixed sitting-time budget. A story-quality punch-list does not — every defective story is signal that needs surfacing, and the consultant fixes them one at a time. Capping would risk hiding low-headline-priority stories that are nonetheless legitimately broken. Diagnostics counts make the volume scannable; sort order (priority → persona → anchor) makes the body navigable.

---

## Sources and defensibility

The six criteria and the priority rubric synthesise five reputable sources, adapted to the framework's data-management/productivity-app target domain (CRUD-shaped, per `CLAUDE.md`'s framework-domain constraint):

- **Mike Cohn — *User Stories Applied* and the INVEST mnemonic** (Bill Wake, 2003). INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable) is canonical prior art for story-quality criteria. Three INVEST attributes are absorbed directly into this methodology's criteria: **Valuable → Meaningful + Outcome-aligned**, **Estimable → Implementable**, **Testable → Testable**, **Small → Appropriately scoped**. The two INVEST attributes deliberately not adopted here — **Independent** and **Negotiable** — are framework-mode concerns (managed by the consultant's story-ordering practice and by the resolver pass, respectively) rather than properties of a single story; including them would conflate story-quality with backlog-management.
- **Connextra format** (As-a / I-want / so-that, originated at Connextra in 2001). Direct prior art for the story shape this methodology audits; the `Outcome-aligned` criterion explicitly tests the `so that …` clause against measurable user/business outcome rather than against re-statement-of-the-action.
- **Karl Wiegers — *Software Requirements*** (Microsoft Press, 3rd ed. 2013). The requirements-quality dimensions (clarity, completeness, ambiguity, testability, correctness, consistency, traceability, feasibility, modifiability, prioritisation) underpin the `Meaningful`, `Coherent`, and `Testable` criteria. A blocking story-quality finding maps to a clarity / testability / completeness failure that would prevent downstream test-case design.
- **BABOK® Guide v3** (IIBA, 2015). The *Requirements Analysis and Design Definition* knowledge area validates story-level quality auditing as a core BA competency distinct from elicitation. The auditor's stance is gap-aware but evidence-based: a story is good or not-good by its observable properties, not by the auditor's preference.
- **QA Madness — *Bug Severity vs Priority*** (`qamadness.com`). Canonical precedent for the `blocking / major / minor` severity tier semantics, mapped from "implemented-but-broken behaviour" onto "story that cannot be built / tested / accepted as written". The mapping is consistent with the priority rubric used by the two "10 questions" review methodologies in this framework.

The synthesis is this reference's own contribution: integrate INVEST's quality attributes (minus the backlog-management two), the Connextra shape contract, and Wiegers's requirements-quality dimensions, then bind them to canonical defect-severity practice — yielding an auditable per-story, per-criterion methodology that respects the framework's deterministic-answer set (`GR-NN`, `PI-NN`) and that does not cross into the adjacent review lenses (no UX critique, no BA gap-questions, no adversarial out-of-§4.2 findings).

### Why not adopt INVEST directly?

A dedicated strict-INVEST review is kept as a candidate at `plans/BA/invest-story-review.md` (it would adopt INVEST verbatim). The consultant chose to add this methodology alongside (not in place of) that candidate because:

- INVEST's *Independent* and *Negotiable* are backlog-management properties, not single-story-quality properties. Auditing them story-by-story produces false positives.
- This methodology adds *Coherent* (internal consistency of role/intent/benefit and consistency with §3 personas and §4.1 goals) — a property INVEST does not name explicitly but that prototype reviews need.
- This methodology folds *Valuable* into two finer criteria (*Meaningful* — the story expresses real user value, and *Outcome-aligned* — the `so that` clause states a measurable outcome) because, in practice, a story can be meaningful with a vague benefit clause or shallow with a sharp one, and the two fail modes need different fixes.

If the consultant wants strict INVEST later, the `invest-story-review` candidate (`plans/BA/invest-story-review.md`) is ready to build as a distinct fourth methodology.

---

## Upstream input contract

The reviewer reads **only** the following:

- `requirements/requirements.md` — the merged requirements document. Read once at Step 2. This is the critique target.
- `framework/assets/characters/user-stories-review.md` — the character file. Read once at Step 1.
- `framework/assets/reviews/user-stories-reference.md` — this document. Read once at Step 1.
- `framework/assets/reviews/template-user-stories.html` — the HTML scaffold. Read once at Step 7 (render).
- `framework/shared/general-rules.md` — read at Step 4 as a **filter source**. The reviewer drops issue rows whose root cause is deterministically resolved by an active `GR-NN`.
- `framework/shared/prototype-invariants.md` — read at Step 4 as a **filter source**. The reviewer drops issue rows whose underlying premise contradicts a `PI-NN` invariant.

It does **not** consult:

- `requirements/requirements-draft.md`, `requirements/source-manifest.json`, `requirements/consultant-answers.md`, `requirements/draft-claims*.ndjson` — pipeline-internal.
- `analyse-requirements/*` outputs — derived artefacts; the review's contract is to audit the stories in the source doc.
- `design-system/*` outputs — not relevant to a user-stories quality review.
- `framework/state/*` — pipeline state is not a review input.
- `framework/shared/prototype-scope.md` — every story under §4.2 is by definition in-scope for the prototype (a story narrating an out-of-scope concern would have been caught at `/requirements` time). The scope filter would have nothing to drop, so the file is not read; the omission saves a read and is documented in diagnostics as `scope-filter: not-applicable`.
- `framework/assets/reviews/ten-ux-questions-reference.md` — the UX-lens drop is irrelevant to story-quality criteria. A story can be a perfectly-formed UX-shaped story (e.g., *"As an Approver, I want a 'reject' button that opens a confirmation modal …"*) and still pass the six criteria; conversely, a poorly-formed BA-shaped story fails them. The UX/BA orthogonality contract is irrelevant here.
- Any other file under `framework/shared/` (e.g. `refusal-registry.md`) — referenced by ID only, not read by this agent.
- Other reviewers' references and templates — not inputs to this agent.

The merged requirements document is the contract. If a story in §4.2 violates one or more of the six criteria, and the violation is not foreclosed by `GR-NN` or `PI-NN`, it is a finding.

---

## The six criteria

Six criteria, applied to every story in §4.2. The criteria are defined exhaustively — they are not flexible.

### 1. Meaningful

**Definition:** the story expresses real user value, not a feature-as-story or an implementation step. The `As a {role}, I want {intent}` clause names a user-visible activity, not a system-internal mechanic or a UI affordance disguised as a need.

**What good looks like:** *"As an Approver, I want to reject a transaction with a mandatory note, so that the rejection rationale is captured for audit."* — the intent (reject + note) is a user-visible activity tied to a recognisable user goal.

**What failure looks like:**
- *"As a User, I want a button on the screen, so that I can use the system."* (feature-as-story; the button is not a user-visible activity, the screen is the affordance, *"use the system"* is not value.)
- *"As an Admin, I want the database to be backed up nightly, so that we don't lose data."* (implementation step disguised as user story; the user's value, if any, is *"never lose data"*, which is a non-functional requirement, not a story.)
- *"As a User, I want to manage things, so that work flows."* (so abstract the intent is unverifiable.)

**Default severity at violation:**
- `major` — the story is intelligible but the value is hard to assess and the team would build the wrong thing in significant cases.
- `minor` — the story is meaningful but the wording is slightly abstract; a rewrite recovers a useful story.

### 2. Implementable

**Definition:** the story can be built within the prototype's `PI-NN` invariants and is concrete enough that an engineer can begin without re-asking the consultant. "Implementable" here is the prototype-build sense: visual-only validation, fixture-backed data, simulated server behaviour — anything within the prototype's contract is implementable; anything that would require real backend / production migration / live integration is not.

**What good looks like:** *"As an Approver, I want to approve a single transaction with a confirmation step, so that I do not approve by accident."* — the prototype can deliver this with a row-action button, a confirm modal (per `GR-04`), and a fixture state transition.

**What failure looks like:**
- *"As an Operator, I want the system to deduplicate incoming records against a live CRM, so that no duplicates are created."* (requires a live integration with another system — out of prototype reach per `PI-04`; should be dropped at Step-4 filter as a `PI-NN` premise mismatch, but if it survives, this is the failure.)
- *"As an Auditor, I want all events to be cryptographically signed, so that we can prove authenticity."* (a cryptographic-signing implementation is not a prototype concern; the underlying business desire — *"events are non-repudiable"* — is implementable as a fixture-backed audit log, but the story as written specifies the mechanism.)
- *"As a User, I want it to be fast, so that I can work efficiently."* (no concrete behaviour to implement; a non-functional sentiment.)

**Default severity at violation:**
- `blocking` — there is no path forward within the prototype's invariants; the story must be rewritten or dropped.
- `major` — the story is implementable but specifies a mechanism instead of an outcome; the team would need to re-derive the actual user need before starting.

### 3. Testable

**Definition:** the story has an observable outcome that a tester or visual reviewer can verify. A senior engineer reading the story can name, in one sentence, what they would check on screen / in a fixture / in a status field to declare the story done.

**What good looks like:** *"As an Approver, I want to approve a transaction with a confirmation step, so that I do not approve by accident."* — observable outcome: status transitions from `Imported` to `Approved`; confirm modal appears before transition.

**What failure looks like:**
- *"As a User, I want the system to be reliable, so that I can trust it."* (no observable outcome; *"reliable"* and *"trust"* are not testable.)
- *"As an Approver, I want to manage approvals, so that work flows."* (no concrete check; *"manage"* covers create / read / update / delete / approve / reject and the tester cannot pick.)
- *"As an Admin, I want good performance, so that users are happy."* (sentiment; not a story.)

**Default severity at violation:**
- `blocking` — the most common cause of `blocking` priority. If no-one can verify the story is done, no-one can build it correctly either.

### 4. Coherent

**Definition:** the story is internally consistent (role / intent / benefit do not contradict each other) and does not conflict with §3 personas, §4.1 goals, or other §4.2 stories in the doc.

**What good looks like:** *"As an Importer, I want to upload a transaction file with the required metadata, so that the system can ingest it into a File Log."* — Importer is a §3 persona; the goal (G-01) is in §4.1; the intent matches the goal; the benefit names a recognisable outcome.

**What failure looks like:**
- *"As an Auditor, I want to upload transaction files, so that they can be processed."* (Auditor is not the persona for upload — §3 names Importer for that, or no Auditor exists; cross-section contradiction.)
- *"As an Approver, I want to reject a transaction without leaving a note, so that the rejection rationale is captured."* (intent contradicts benefit; the `so that` clause names "rationale captured" but the intent explicitly removes the rationale-capture mechanism.)
- Two stories that overlap so closely they cannot both be true — e.g., *"As an Importer, I want to upload single files"* and *"As an Importer, I want bulk upload only with no single-file path"*. (cross-story contradiction.)

**Default severity at violation:**
- `blocking` — a contradictory story cannot be built (which interpretation wins?) and the contradiction propagates into design.

### 5. Appropriately scoped

**Definition:** the story is one verb on one object for one persona; not a feature umbrella or a multi-flow saga. A well-scoped story is typically estimable in a single sprint, addressable by a single PR, and acceptance-criteria-able in 1–3 short sentences.

**What good looks like:** *"As an Importer, I want to upload a transaction file with the required metadata, so that the system can ingest it into a File Log."* — one verb (upload), one object (transaction file), one persona (Importer).

**What failure looks like:**
- *"As an Approver, I want to manage approvals, so that work flows."* (one verb but the verb is a saga: approve + reject + amend + escalate + delegate; should be ≥ 2 stories.)
- *"As a User, I want to upload, review, approve, and export transactions."* (four verbs; four stories.)
- *"As a Team Lead, I want the dashboard to show everything I need."* (one persona but the object is the whole screen; unscope-able without splitting per element.)

**Default severity at violation:**
- `major` — the story is buildable but the team will mis-scope its estimate; a single sprint becomes three.
- `blocking` — escalates to `blocking` if splitting the story would produce more than 4 stories (the original is a feature umbrella, not a story).

### 6. Outcome-aligned

**Definition:** the `so that …` clause names a measurable user or business outcome, not a re-statement of the action. The reader can answer *"why does the user want this?"* without re-reading the `I want …` clause.

**What good looks like:** *"As an Approver, I want to reject a transaction with a mandatory note, so that the rejection rationale is captured for audit."* — outcome (rationale captured for audit) is a recognisable business outcome distinct from the action (reject + note).

**What failure looks like:**
- *"As an Approver, I want to reject a transaction, so that I can reject it."* (so-that restates the action.)
- *"As an Importer, I want to upload files, so that files are uploaded."* (tautology.)
- *"As a User, I want to use the system, so that the system is used."* (degenerate.)
- *"As an Approver, I want to manage approvals, so that work flows."* (vague outcome; *"work flows"* is not measurable.)
- Missing `so that` clause entirely.

**Default severity at violation:**
- `minor` — the most common Outcome-aligned failure is a vague benefit clause; the story is buildable, the outcome inferable, and a wording fix closes it.
- `major` — escalates to `major` if the benefit clause is missing entirely or is a tautology (the story has no stated outcome at all, which is more than a wording issue).

---

## Issue schema (in-memory; never written verbatim to disk)

Each issue is a JSON-shaped record in memory, one per `(story, violated criterion)` pair:

```
story_id:           US-NN          (assigned at Step 2 in document order; zero-padded)
persona:            string         (the persona name from the §4.2 #### heading)
anchor:             "§4.2 / {Persona} / story #{N}"   (N is 1-based position under the persona)
connextra_text:     string         (verbatim "As a … I want … so that …" from the story heading)
criterion:          one of {Meaningful, Implementable, Testable, Coherent, Scoped, Outcome-aligned}
severity:           blocking | major | minor
reason:             string         (1–3 sentences explaining the property of the story that fails the criterion)
fix:                string         (1–2 sentences, directional hint; never a re-authored story)
```

A story may produce zero, one, or many issue rows depending on how many criteria it violates. An issue row is invalid (and not eligible for grouping) if any field is missing.

---

## Filter rules (Step 4 of the agent workflow)

After generating the issue rows, the reviewer reads two filter sources and drops every issue row that matches one of the rules below.

### Filter source reads (Step 4 only)

- `framework/shared/general-rules.md`
- `framework/shared/prototype-invariants.md`

The two reads are scoped to this step and are the agent's **only** reads outside its own asset set and the merged requirements doc.

### Rule 1 — `GR-NN` no-flag filter

If an issue's root cause is deterministically resolved by an active `GR-NN` rule, drop the issue. The most relevant collisions:

| `GR-NN` | Topic | Issue pattern the rule forecloses |
|---|---|---|
| GR-04 | Irreversible actions require modal confirmation | An issue flagging a story for "no mention of confirmation modal" on an irreversible action — `GR-04` resolves the confirmation policy; the story doesn't need to restate it. |
| GR-19 | Session timeout by domain class | An issue flagging *"the story doesn't say what happens on session timeout"* — `GR-19` resolves it deterministically. |

Drop with `reason: gr-match: GR-NN` in the diagnostics record. The body does not list dropped issues.

### Rule 2 — `PI-NN` premise filter

If an issue's underlying premise contradicts an active `PI-NN` prototype invariant, drop the issue. The five active invariants:

| `PI-NN` | Invariant | Issue pattern the invariant forecloses |
|---|---|---|
| PI-01 | Server behaviour is simulated | An issue flagging *"no mention of database commit"* on an action-bearing story. |
| PI-02 | Data is fixture-backed | An issue flagging *"no data migration strategy"* on a data-touching story. |
| PI-03 | Validation is visual only | An issue flagging *"no server-side validation"* on a form story. |
| PI-04 | Third-party integrations are visual | An issue flagging *"no real integration with X"* on an integration-adjacent story. |
| PI-05 | Role switcher exists in prototype chrome | An issue flagging *"how does the user log in as a different role"* on a role-aware story. |

Drop with `reason: pi-match: PI-NN`. The body does not list dropped issues.

### Why two filter rules, not four?

The `ten-ba-questions` and `ten-ux-questions` reviewers apply four filter rules each. This reviewer applies two:

- **No `prototype-scope.md` (out-of-scope) filter** — every story in §4.2 is by definition in-scope for the prototype; the scope filter would have nothing to drop. Documented as `scope-filter: not-applicable` in diagnostics.
- **No UX-lens drop** — story-quality criteria (Meaningful / Implementable / Testable / Coherent / Scoped / Outcome-aligned) are orthogonal to UX-vs-BA framing; a UX-shaped story can be a perfectly-formed story and a BA-shaped story can be poorly formed. Documented as `ux-lens-filter: not-applicable` in diagnostics.

### Diagnostics record

Every dropped issue is logged in the in-memory diagnostics block with `{story_id, criterion, reason}`. The diagnostics block in the final artefact summarises the drop counts; it does not list every dropped issue.

---

## Group rule (Step 5 of the agent workflow)

After Step-4 filtering, the reviewer groups surviving issue rows into per-story findings.

**Grouping key:** `story_id`.

**Group output:** one finding per `story_id` with:

- `story_id`, `persona`, `anchor`, `connextra_text` — copied from any issue row for the story (consistent across rows by construction).
- `issues` — the full list of surviving issues for the story, sorted by severity descending (blocking issues first within the finding) then by criterion-order in the reference (Meaningful → Implementable → Testable → Coherent → Scoped → Outcome-aligned).
- `headline_priority` — the **maximum severity** across the story's issues. A story with `[blocking, minor, minor]` has headline `blocking`. A story with `[major, minor]` has headline `major`. A story with `[minor]` has headline `minor`.
- `criteria_violated` — the comma-separated list of distinct criteria violated, in reference order (used by the Triage table's *Criteria violated* column).

**Final sort order:** findings are sorted by:

1. `headline_priority` (blocking → major → minor).
2. `persona` (alphabetical within each priority — Approver before Importer).
3. `anchor` (story #1 before story #2 within a persona).

This sort order is the gate-7 contract and is what the rendered body presents.

A story whose surviving issue rows is zero (because Step-4 dropped all its issues) is **not** a finding and does not appear in the body. Its `story_id` contributes to the pass-count in diagnostics.

---

## Priority rubric (canonical)

Every issue carries one of three severities. The headline priority of a finding is the maximum severity across its issues.

The rubric is operational, not philosophical — the test below is what the reviewer actually applies per issue:

### blocking

- Without a fix, **the story cannot be built, tested, or accepted** as written.
- Operational test: *"Could a senior engineer pick this up and start work?"* — **No.**
- Most common at violation of: **Testable** (no observable outcome), **Coherent** (story is contradictory), **Implementable** (no path within `PI-NN`), **Scoped** (saga that would split into > 4 stories).

### major

- The story is **buildable but ambiguous**; multiple correct implementations are possible. The team can ship with a stated assumption but the assumption may be wrong.
- Operational test: *"Could a senior engineer pick this up?"* — **Yes, but with a documented assumption that may be wrong.**
- Most common at violation of: **Scoped** (over-broad story that would split into 2–4 stories), **Meaningful** (value-unclear story), **Implementable** (specifies mechanism instead of outcome), **Outcome-aligned** (benefit clause missing entirely).

### minor

- Refinement opportunity. A reasonable interpretation produces an acceptable story; the issue tunes wording or fills a small gap.
- Operational test: *"Could a senior engineer pick this up?"* — **Yes, and a reasonable default will probably stick.**
- Most common at violation of: **Outcome-aligned** (vague benefit clause), **Meaningful** (slightly abstract wording).

There is no fourth severity. *"Could-be-clearer"* is not a severity — either the story is unimplementable / untestable / contradictory (`blocking`), or it is ambiguous (`major`), or it is a wording-pass (`minor`), or it is not a story-quality finding at all and should not have survived the criteria evaluation.

The severity distribution **falls out of the story set**. A clean set produces few or no blocking findings; a hastily-written set produces several. No quota enforcement — the spread is honest signal about the stories' state.

---

## Output presentation

The artefact renders as a self-contained HTML report following `framework/assets/reviews/template-user-stories.html`. The fixed section ordering is:

1. **Header** — title, generated-at timestamp, requirements SHA-256, reviewer identity, story counts (evaluated / pass / fail), priority counts (blocking / major / minor), persona list.
2. **Executive Summary** — counts, priority legend, source statement.
3. **Triage** — single ordered table listing every finding with priority, story ID, persona, anchor, and the comma-separated list of criteria violated.
4. **Blocking** — one finding block per blocking-headline story, sorted by persona then anchor. If zero, render the heading and `_None._`.
5. **Major** — same shape, for major-headline stories.
6. **Minor** — same shape, for minor-headline stories.
7. **Diagnostics** — per-criterion failure counts, filter-drop counts, gate-results table, override log.

The artefact is a **punch-list**, not an essay. Prose between findings is minimised; the consultant should be able to read the Triage table in under two minutes, then jump to the relevant priority section to pick a story to fix next.

---

## Quality gates (run after Step 5, before write)

Nine gates. All are hard. If any gate fails, the reviewer does **not** write the artefact — it surfaces a structured error and halts. (See `framework/agents/reviews/user-stories-reviewer.md > Step 6 — Validate` for the halt contract.)

1. **Every story in §4.2 was evaluated.** `evaluated_count == enumerated_count` (the Step-2 enumeration of `##### Story:` headings is the denominator).
2. **Every finding has all required fields.** Non-empty `story_id`, `persona`, `anchor`, `connextra_text`, `headline_priority`, and `issues` with `len ≥ 1`.
3. **Every issue has all required fields.** `criterion ∈ {Meaningful, Implementable, Testable, Coherent, Scoped, Outcome-aligned}`, `severity ∈ {blocking, major, minor}`, `reason` is a non-empty 1–3-sentence string, `fix` is a non-empty 1–2-sentence string. Stub reasons or fixes (`"unclear"`, `"fix this"`) fail.
4. **No issue cites a criterion outside the six.** Defence-in-depth against introducing a stray criterion at issue generation time.
5. **No issue is foreclosed by `GR-NN` or `PI-NN`.** Re-run the Step-4 rule-1 and rule-2 checks against the surviving issue set.
6. **Headline-priority consistency.** For every finding, `headline_priority == max(severity for issue in finding.issues)`. (Order: blocking > major > minor.)
7. **Sort order: priority → persona → anchor.** The rendered findings list is in this order.
8. **Criterion-coverage sanity.** ≥ 4 of the 6 criteria are represented across the surviving issue set. If fewer, the gate fires a `narrow-review` warning (not a hard fail — single-criterion sweeps may be legitimate on small story sets, but the consultant should confirm); on consultant Override, the warning is recorded in diagnostics and the run proceeds. Zero-finding runs auto-pass this gate (a clean story set is not a coverage failure).
9. **Diagnostics block completeness.** The diagnostics block reports `total_stories_evaluated`, `pass_count`, `fail_count`, `per_criterion_failure_counts` (all six criteria, zero-counts allowed), `per_priority_counts`, `gr_drop_count`, `pi_drop_count`, and `gate_results` for all 9 gates.

---

## Anti-patterns

- **Capping findings.** This methodology has no "top N" cap. Every defective story is signal.
- **Authoring replacement stories.** Fixes are concise hints (one sentence or two short bullets), never authored Connextra triples. *"Rewrite as 'As an Approver, I want to approve a request, so that …'"* is overreach; *"Split into 'approve a request' and 'reject a request with reason'"* is the right shape.
- **Surfacing passing stories in the body.** The body is for failing stories only. Pass-counts live in diagnostics.
- **Scoring stories that aren't in §4.2.** Goals (§4.1), task flows (§5), requirements (§6) are not user stories. They are out of scope for this lens.
- **Crossing into adjacent review lenses.** Findings about missing personas in §3, missing screens, missing flows, or missing data entities are not story-quality findings — they belong to BA-questions, UX-questions, or adversarial reviews.
- **Phantom anchors.** A finding citing `§4.2 / Auditor / story #1` when the doc has no Auditor persona is a gate-2 failure. Use the Step-2 enumeration as the source of truth.
- **Bundled criteria in one issue.** *"Untestable and too broad"* is two issues, not one. Split.
- **Padding the blocking count.** A clean set legitimately produces zero blocking findings. The priority distribution is honest signal; no quota enforcement.
- **Generic issues.** *"This story is unclear"* is not a finding. Cite the specific criterion and the specific property of the story that fails it.
- **Re-flagging GR-NN / PI-NN-resolved concerns.** Step-4 filters them; gate 5 catches escapees. A finding whose root cause is `GR-04` (confirmation modal policy) is dropped.
- **Reviewing against derivatives.** Do not consult `analyse-requirements/*` outputs to triangulate story quality. The review's contract is to read `requirements/requirements.md` as the source of truth.
- **Inline `[SRC: ...]` markers.** Per project convention (`feedback_no_inline_provenance`), the merged requirements doc is clean of provenance markers; the review artefact is also clean. Findings cite by `§4.2 / Persona / story #N`, not by `[SRC: ...]`.
- **Editing the template scaffold.** Only the documented `{{placeholders}}` are substituted; section ordering, table column headers, and the diagnostics layout are fixed.

---

## Voice and stance

The reviewer's stance is defined in `framework/assets/characters/user-stories-review.md` — experienced product owner / Business Analyst auditing story quality, evidence-driven, constructive, non-confrontational, observation-based. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

---

## References

- **Bill Wake — *INVEST in Good Stories, and SMART Tasks*** (`xp123.com`, 2003). Canonical six-attribute mnemonic for story quality; four of the six map onto this methodology's criteria (Valuable → Meaningful + Outcome-aligned; Estimable → Implementable; Testable → Testable; Small → Scoped). Independent and Negotiable are deliberately not adopted because they are backlog-management properties, not single-story properties.
- **Mike Cohn — *User Stories Applied: For Agile Software Development*** (Addison-Wesley, 2004). The Connextra-format story shape and the discipline of one-verb / one-object / one-persona stories underpin the Scoped criterion.
- **Karl Wiegers — *Software Requirements*** (Microsoft Press, 3rd ed. 2013). Requirements-quality dimensions (clarity, completeness, testability, consistency) underpin the Testable, Meaningful, and Coherent criteria.
- **IIBA — *A Guide to the Business Analysis Body of Knowledge® (BABOK® Guide), v3*** (IIBA, 2015). The *Requirements Analysis and Design Definition* knowledge area validates per-story quality auditing as a BA practice distinct from elicitation.
- **Connextra format originators** (Connextra, 2001). The *As-a / I-want / so-that* shape is the contract this methodology audits; the Outcome-aligned criterion specifically tests the `so that …` clause.
- **QA Madness — *Bug Severity vs Priority*** (`qamadness.com`). Canonical precedent for the `blocking / major / minor` severity tier semantics, used consistently across the four `/review-requirement` lenses in this framework.

The synthesised six-criterion structure is this reference's own contribution: it integrates INVEST's quality attributes (minus the two backlog-management ones), splits Valuable into Meaningful and Outcome-aligned because the two failure modes need different fixes, adds Coherent as an explicit consistency check, and binds the severity labels to canonical defect-severity practice — yielding an auditable per-story, per-criterion methodology that respects the framework's deterministic-answer set (`GR-NN`, `PI-NN`) and that does not cross into the adjacent review lenses.
