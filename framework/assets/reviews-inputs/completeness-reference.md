<!-- ROLE: asset (P2 review reference). Loaded by framework/agents/reviews-inputs/completeness-reviewer.md at activation. -->

# reviews-inputs/completeness-reference.md

**Purpose:** Methodology reference for Completeness Review of the **raw consultant input set** enumerated by `requirements/source-manifest.json`. The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews-inputs/completeness-reviewer.md` — drives the agent's ten-dimension sequential sweep, disposition assignment, coverage-matrix construction, and quality-gate sweep.

**Output produced by the reviewer:** `review-inputs/COMPLETENESS-REVIEW/completeness-review.html` — a self-contained HTML gap register of cited, severity-and-disposition-graded findings, plus a coverage matrix (10 dimensions × N consumed sources, rendered as a sticky-thead HTML table) and a per-source elicitation-question list scoped to `Needs-Clarification`-disposition findings. The reviewer renders it by substituting into the scaffold `framework/assets/reviews-inputs/template-completeness.html`.

**Sibling lenses under `/review-inputs`:**

- `framework/assets/reviews-inputs/adversarial-reference.md` — sweeps a broader seven-dimension BMAD critique (stakeholder coverage, workflow coverage, ambiguity & vague language, provenance & conflict, quantitative signal, scope & MVP, bias & sampling). Adversarial's Dimension 1 (Stakeholder & Role Coverage) and Dimension 2 (Domain & Workflow Coverage) overlap this reference at a coarser, thematic grain — adversarial reports "stakeholder roster thin" as one clustered finding; this reviewer decomposes coverage into ten orthogonal dimensions anchored to IEEE 29148 / IEEE 830 / Volere / BABOK / Wiegers / INCOSE, and pre-classifies every finding with a Disposition flag that maps onto the `/requirements` drafter's marker vocabulary.
- `framework/assets/reviews-inputs/ambiguity-reference.md` — sweeps a seven-dimension linguistic-ambiguity taxonomy (Berry/Kamsties + Femmer). Ambiguity's central rule is the **≥2-interpretations test**: every finding lists ≥2 plausible readings. Completeness's central rule is the inverse — the **absent-vs-out-of-scope test**: every finding confirms the corpus contains neither explicit content nor explicit exclusion of the topic before logging. Ambiguity catches multi-readable spans; completeness catches missing spans. The two reviewers are complementary, not redundant: a single corpus span can be both ambiguous *and* under-specified, and each lens would log it under its own dimension and disposition.

---

## What "completeness review" means

A raw input set is **complete** when every topic a downstream requirements engineer would need to draft an unambiguous, testable specification is either present in some source, deterministically fillable by a documented `[STANDARD-RULE: GR-NN]` rule, or explicitly out of scope for this phase. Anything else is a **gap** — the reviewer's deliverable.

The discipline is rooted in the requirements-engineering literature on the *completeness* quality attribute:

1. **IEEE Std 830-1998 §4.3.** Lists eight SRS quality attributes — correct, **unambiguous**, **complete**, consistent, ranked-for-importance, verifiable, modifiable, traceable. Completeness = *every requirement is included* + *every input situation is addressed* + *every reference is satisfied (no TBDs except those with a tracked owner)*.
2. **ISO/IEC/IEEE 29148:2018 §5.2.4 (completeness as a stakeholder-requirement attribute) and §6.4.2.3 (the nine completeness checks for a system requirements specification).** Supersedes IEEE 830 and provides the operational checklist: stakeholders, operational scenarios, lifecycle phases, environmental conditions, abnormal conditions, performance/quality, design constraints, applicable laws, derived-requirement traceability. **This is the canonical authority.**
3. **Wiegers & Beatty, *Software Requirements* (3rd ed.).** Enumerates eleven typical input-side completeness gaps: missing functional requirements, missing NFRs, missing actors, missing data definitions, missing exception/error handling, missing acceptance criteria, missing constraints, missing assumptions, missing dependencies, missing UI behaviour, missing business rules. Wiegers explicitly separates *absent* from *out-of-scope* — the discipline this reviewer enforces.
4. **Robertson & Robertson, *Mastering the Requirements Process* (Volere).** A 35-section template with explicit Open-Issues (§18) and Waiting-Room (§26) sections for tracking known gaps; the "Trawling for Requirements" technique is the elicitation-side gap-surfacing instrument.
5. **BABOK v3.** §3.4 requirements verification and §7.5 specify-and-model practice; §10.43 Stakeholder List, §10.5 Business Rules Analysis, §10.10 Concept Modelling are the practitioner-grade instruments this reviewer's dimensions map onto.
6. **INCOSE Guide for Writing Requirements (v4).** R3 (Completeness), R37 / R38 (set-level completeness), R39 (Bounded — explicit scope boundaries), R29 (Verifiable). The R3 rule is the reviewer's single-sentence operating motto: *"A requirement set is complete if it states what is needed and nothing important is missing."*

This reference consolidates the above into **ten non-overlapping dimensions**, sized to cover IEEE 29148's nine checks plus Volere's terminology dimension. Sibling reviewers ship seven dimensions because their underlying taxonomies are seven-shaped; completeness's underlying authority surface is wider, so the dimension count is wider — but every dimension is anchored to a specific authority section so the reviewer never invents grounds.

The discipline's **central rule:** every finding satisfies the **absent-vs-out-of-scope test** — the reviewer must confirm, before logging, that:

1. The corpus does **not** contain explicit content satisfying the dimension's coverage threshold; **AND**
2. The corpus does **not** contain an explicit statement excluding the topic from this phase.

If the corpus is silent (`ABSENT`), the finding is logged. If the corpus carries an explicit exclusion (e.g., *"phase-2 only"*, *"out of scope for this release"*), the finding is logged with `Disposition: Out-of-Scope` and the explicit-exclusion quote becomes the Evidence — the reviewer surfaces it so the drafter knows to render `[OUT-OF-SCOPE: domain-default]` markers. If the topic is covered by an active `GR-NN` rule (read from `framework/shared/general-rules.md`), the finding is logged with `Disposition: Standard-Rule-Applies` and the rule ID becomes the Authority — the reviewer surfaces it so the drafter knows to render `[STANDARD-RULE: GR-NN]` markers. Only if the corpus is genuinely silent *and* no `GR-NN` covers the dimension *and* no explicit out-of-scope statement exists does the finding carry `Disposition: Needs-Clarification` — the only disposition that drives a stakeholder elicitation question.

This three-way classification is the methodology's load-bearing pipeline contribution: it pre-classifies every gap into the same three categories the `/requirements` drafter must produce markers for. The drafter consumes the gap register downstream and renders `[AI-SUGGESTED: AI-NNN | blocking]` / `[STANDARD-RULE: GR-NN]` / `[OUT-OF-SCOPE: domain-default]` markers per the reviewer's pre-classification.

---

## Upstream input contract

The reviewer reads:

- `requirements/source-manifest.json` (the manifest enumerating consumable input files; read once at the reviewer's Step 2). The `target` field (`prototype` | `application` | `null`) governs which scope predicate applies at the disposition step.
- For each manifest row whose `tier != "Unsupported"`, the file selected by the Read-path resolution rule in `framework/skills/build-source-manifest.md` (read `converted_sibling` when non-null, else `original_path` — only `Native-text` is read at `original_path`). For `Native-multimodal` / `Vector-renderable` rows the `converted_sibling` is a frozen textual description prepared by the input-handler — it already captures labels, field captions, table contents, status/error states, KPI values, and a structured breakdown; treat it as the canonical text source and do **not** re-interpret pixels. `Supported-via-MCP` rows read the markitdown sibling. Read once by the reviewer at Step 3.
- `framework/assets/characters/completeness-inputs-review.md` (the character — loaded once at activation).
- `framework/assets/reviews-inputs/completeness-reference.md` (this file — loaded once at activation).
- `framework/shared/general-rules.md` — loaded **read-only** at the disposition step (Step 14). Authoritative source of `GR-NN` ids the reviewer maps `Standard-Rule-Applies`-disposition findings against. The reviewer does **not** invent `GR-NN` ids — only existing rules are referenced.
- `framework/shared/prototype-scope.md` — loaded **read-only** at the disposition step (Step 14) when the manifest's `target` field is `prototype` or `null` (the prototype-scope predicate is the framework default per CLAUDE.md). When `target == "application"`, the prototype-scope filter is **not applied** — every dimension is in-scope by construction and `Out-of-Scope` dispositions can only fire on explicit-exclusion quotes from the corpus.

The reviewer does **not** read:

- `requirements/requirements.md`, `requirements/requirements-draft.md`, `requirements/consultant-answers.md`, `requirements/draft-claims*.ndjson` — derivative artefacts; the review's contract is to critique the raw inputs themselves.
- `review-inputs/ADVERSARIAL/adversarial-review.html`, `review-inputs/AMBIGUITY-REVIEW/ambiguity-review.html` even when present — each input-pipeline lens is independently grounded in the manifest; cross-reading would conflate the methodologies and produce correlated noise.
- `analyse-requirements/*`, `analyse-inputs/*` outputs — derived; each lens reads the manifest independently.
- `design-system/*`, `review-requirements/*`, `framework/state/*`, `framework/shared/prototype-invariants.md`, `framework/shared/refusal-registry.md` (except as textual references in this document and the agent file) — out of scope.
- `framework/skills/completeness-gap-pass.md` — **explicitly not loaded.** That skill is `/requirements`-private (it walks a synthesised draft against `topics-requirements.md` bijection invariants); this reviewer walks raw inputs against IEEE/Volere/BABOK dimension checklists. The conceptual decision-tree (Stated → Rule → Scope → Default) is shared inspiration but the implementations are independent.

---

## The ten completeness dimensions

Ten dimensions, swept **sequentially** (one per agent step, in dimension order, Steps 4–13). Cross-dimension consolidation at Step 14 collapses same-span multi-dimension hits into single multi-tag findings, so the per-dimension sweeps can be lenient on overlap.

Every dimension is anchored to at least one canonical authority (IEEE 29148 / IEEE 830 / Volere / BABOK / Wiegers / INCOSE / ISO 25010). The dimension's `Authority:` field becomes the finding's Authority field verbatim when logged.

### Dimension 1 — Stakeholder & Role Coverage

**Authority:** IEEE 29148 §5.2.4 item 1 (stakeholders); BABOK §10.43 (Stakeholder List); Volere §2 (Stakeholders); Wiegers gap #3 (missing actors).

**Question:** Does the corpus carry direct, first-hand voice from every actor named in any source? Or does any named actor appear only as a second-hand reference?

**What to check:**

- Build an actor set: every role / persona / user-type / team / role-name / job-title named in any source (e.g., `Finance Manager`, `External Auditor`, `Customer Service Rep`, `Admin`, `End User`, `System Integrator`).
- For each actor, scan the corpus for **first-hand voice**: a transcript of an interview with that actor, a written persona profile authored from primary research, a workshop note quoting the actor by name, or a screenshot/photo of the actor's current tooling.
- Actors named only by reference (*"the Finance Manager will approve invoices"*) without any source carrying their first-hand voice are `ABSENT` on Dimension 1.
- Stakeholders mentioned by category but never enumerated (*"various business users"*, *"the team"*, *"external partners"*) are `PARTIAL` on Dimension 1 — the category is named but the specific actors are not.

**Coverage thresholds (used by the coverage-matrix step):**

- `COVERED` — actor is named **and** the corpus carries ≥1 first-hand-voice source for the actor.
- `PARTIAL` — actor is named but the only sources covering them are second-hand references (briefs, decks, mentions in other actors' transcripts).
- `ABSENT` — an obviously-relevant actor for the system's domain is never named (e.g., a payment-handling product with no source mentioning a Finance role at all).
- `OUT-OF-SCOPE-EXPLICIT` — the corpus carries an explicit statement excluding the actor from this phase (*"phase-2 personas: External Auditor, Compliance Officer"*).

**What is NOT a Dimension 1 finding:**

- An actor whose first-hand voice is present in any source, even briefly. *"`workshop-notes.md` line 12: 'Maria (Finance Mgr) says she opens the reconciliation report at 8am every Tuesday'"* is first-hand voice; do not flag.
- Generic project stakeholders (sponsors, project managers, BAs themselves) who are not users of the system. Stakeholder list ≠ user list; this dimension is about **system actors**.
- Vendor / third-party roles named only as integration partners (those belong to Dimension 8 — Integrations).

**Worked example — positive find:**

> Sources: `brief.docx`, `interview-jane-cs.md`, `interview-tom-admin.md`, `workshop-notes.md`
>
> *Brief names primary users: Customer Service Rep, Admin, Finance Manager. Interview transcripts exist for Customer Service Rep (Jane) and Admin (Tom). No interview, no persona, no workshop quote, no screenshot of tooling exists for Finance Manager — the role is named four times across `brief.docx` and `workshop-notes.md` but no source carries Finance Manager voice.*
>
> Finding: `COMP-04 — Dim 1 — Major — Needs-Clarification — Location: corpus-wide`.
>
> Authority: IEEE 29148 §5.2.4 item 1; BABOK §10.43; Wiegers gap #3.

**Worked example — near-miss (do NOT flag):**

> Sources: `brief.docx`, `interview-finance.md`
>
> *Brief names Finance Manager; `interview-finance.md` is a 40-minute transcript with Carlos, the Finance Manager, covering his daily workflow, common errors, and what "done" looks like.*
>
> Dimension 1 is `COVERED` for Finance Manager. Do not flag — the threshold is *"at least one source carrying first-hand voice"*, and the transcript satisfies it.

### Dimension 2 — Scope Boundaries (in / out / deferred)

**Authority:** Volere §26 (Waiting Room — explicit exclusions); INCOSE R39 (Bounded); BABOK §10.41 (Scope Modelling); Wiegers gap #7 (missing constraints — phase boundary is a constraint).

**Question:** Does the corpus carry an explicit statement of what is **excluded** from this phase, in addition to what is included?

**What to check:**

- Inclusion alone is insufficient. A brief that lists features to build, with no exclusion list, leaves every conceivable feature as ambiguous-in-scope — the reviewer cannot tell whether (e.g.) *"reporting"* implies the dashboard the brief mentions only, or also scheduled email exports the brief never mentions.
- Look for explicit exclusion language: *"out of scope for this phase"*, *"phase 2"*, *"not in this release"*, *"deferred"*, *"future work"*, *"not handled here"*.
- Look for an explicit MVP-vs-future demarcation: a section titled *"Out of scope"*, *"Non-goals"*, *"Phase-2 wishlist"*, *"Future considerations"*.
- The reviewer is strict here: a single MVP/Phase-1 bullet list with no paired exclusion list is `PARTIAL`. *"V1 includes A, B, C"* does not say what V1 excludes.

**Coverage thresholds:**

- `COVERED` — the corpus carries an explicit exclusion list (or non-goals section, or phase-2 wishlist) **and** every named feature in the inclusion list has a corresponding presence/absence statement.
- `PARTIAL` — only an inclusion list exists; the corpus is silent on what is excluded.
- `ABSENT` — the corpus carries neither an inclusion list nor an exclusion list; scope is entirely implicit.
- `OUT-OF-SCOPE-EXPLICIT` — does not apply to Dimension 2 (a scope-statement cannot itself be out of scope).

**What is NOT a Dimension 2 finding:**

- A passing mention of *"phase 2"* without an enumerated list — that's `PARTIAL`, not `COVERED`. The reviewer logs it.
- A specific feature absence (e.g., *"no mention of password reset flow"*) — that's the feature's home dimension (likely Dimension 4 — Workflows), not Dimension 2.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *Brief lists 12 features for V1 under the heading "MVP scope". No "Out of scope" section. No "Phase 2" list. No statement about, e.g., whether mobile is included, whether multi-tenant is included, whether the existing legacy system continues to coexist.*
>
> Finding: `COMP-07 — Dim 2 — Blocker — Needs-Clarification — Location: brief.docx`.
>
> Evidence: *"V1 scope: 1) customer list, 2) invoice generation, ..."* (the inclusion list as the verbatim quote demonstrating the absent-exclusion-list).
>
> Authority: Volere §26; INCOSE R39; Wiegers gap #7.

**Worked example — near-miss (do NOT flag):**

> Source: `brief.docx`
>
> *Brief has a Scope section: "V1: customer list, invoice generation, payment status. Out of scope for V1: mobile app (phase 2), multi-tenant (phase 3), legacy migration (handled outside this project)."*
>
> Dimension 2 is `COVERED`. Do not flag.

### Dimension 3 — Data Entities & Attributes

**Authority:** Volere §7 (Data); IEEE 29148 §6.4.3 (data requirements); BABOK §10.10 (Concept Modelling); Wiegers gap #4 (missing data definitions).

**Question:** For every entity mentioned in any workflow, does the corpus enumerate its key fields, identity, lifecycle states, and persistence semantics?

**What to check:**

- Build an entity set: every business noun referenced in any source as a thing the system stores, retrieves, or manipulates (e.g., `Invoice`, `Customer`, `Policy`, `Order`, `Reconciliation`, `User`, `Audit Log`, `Attachment`).
- For each entity, check:
  - **Key fields named.** At least the primary identifier and 3–5 core attributes (Invoice → invoice number, customer, amount, due date, status).
  - **Lifecycle states named** when the entity has obvious lifecycle (e.g., `Invoice`: draft → sent → paid → overdue → archived). Entities without lifecycle (e.g., `Country`) require no state list.
  - **Persistence semantics named** when ambiguous: is this entity a long-lived record, a session-scoped object, a cached projection, an event in a log? Briefs often name an entity without saying whether it persists, expires, archives, etc.
  - **Identity rules.** Is the entity uniquely identified by a system-generated ID, by a business identifier (e.g., invoice number), by composite keys? Briefs frequently mention entities by business identifier without saying whether the business identifier is enforced unique.

**Coverage thresholds:**

- `COVERED` — entity is named, key fields enumerated (≥3 core attributes), lifecycle states named where applicable, identity rule stated.
- `PARTIAL` — entity is named with ≥1 attribute or operation but key fields / lifecycle / identity not enumerated.
- `ABSENT` — entity is mentioned only by name (*"the system tracks invoices"*) with no attributes, no lifecycle, no identity rules.
- `OUT-OF-SCOPE-EXPLICIT` — corpus says the entity is read-only-projection-only (e.g., *"customer is owned by the CRM; we display read-only"*) — completeness for storage-layer attributes is then explicitly out of scope; only display-relevant fields need enumeration.

**What is NOT a Dimension 3 finding:**

- A storage-layer concern (table indexes, foreign-key constraints, partitioning) — these are explicitly out of scope per `framework/shared/prototype-scope.md` for `target: prototype` runs. The dimension fires on *displayable* attributes only when target is prototype.
- A field-level UI-presentation concern (which fields are required, which are optional, validation rules) — those belong to Dimension 6 (Business Rules) or are governed by `GR-NN` (e.g., `GR-05` validation timing, `GR-06` required-field marking) under `Disposition: Standard-Rule-Applies`.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"The system manages Invoices. Users can create, view, send, and mark paid."*
>
> No source enumerates: what are the fields on an Invoice (number, customer, amount, currency, line items, tax, due date, status, sent-at, paid-at, archived-at, attachments)? What states besides Paid (Draft, Sent, Overdue, Cancelled, Voided)? Is the invoice number system-generated or user-supplied? Are invoices immutable once sent?
>
> Finding: `COMP-12 — Dim 3 — Blocker — Needs-Clarification — Location: brief.docx`.
>
> Authority: Volere §7; IEEE 29148 §6.4.3; BABOK §10.10; Wiegers gap #4.

**Worked example — near-miss (do NOT flag):**

> Sources: `brief.docx`, `invoice-fields-spec.xlsx`
>
> *Brief names Invoice; spreadsheet lists all 14 fields (number/customer/amount/currency/lineItems/tax/dueDate/status/sentAt/paidAt/archivedAt/attachments/notes/createdBy), all 6 statuses (Draft/Sent/Paid/Overdue/Cancelled/Voided), identity rule (system-generated 8-digit number), immutability rule (immutable after Sent).*
>
> Dimension 3 is `COVERED` for Invoice. Do not flag.

### Dimension 4 — Functional Workflows (including non-happy paths)

**Authority:** IEEE 29148 §6.4.2.3 item 5 (operational scenarios); IEEE 830 §4.3 item 2 (every realisable input situation addressed); Wiegers gap #5 (missing exception/error handling).

**Question:** For every named workflow / use case / feature, does the corpus describe the failure / exception / abnormal-path behaviour, not only the happy path?

**What to check:**

- Build a workflow set: every named user action / use case / feature flow in any source (e.g., *"create invoice"*, *"approve refund"*, *"reconcile statement"*, *"export report"*, *"upload attachment"*).
- For each workflow, check whether the corpus describes:
  - **Network / connectivity failure** behaviour (lost connection mid-flow, slow response, partial success).
  - **Validation / input-error** behaviour (what happens when the user submits invalid input; how errors are surfaced).
  - **Permission-denied** behaviour (what happens when a user attempts the workflow without authorisation — see also `GR-02` for the prototype standard rule).
  - **Concurrent-modification** behaviour (two users editing the same record; stale data; merge conflicts).
  - **Timeout** behaviour (session expiry mid-flow, server timeout, retry behaviour).
  - **Partial-completion** behaviour (multi-step flows where step 3 of 5 fails — does the system roll back, hold, or proceed?).
  - **External-system failure** behaviour (when an integration the workflow depends on is unavailable).

The reviewer is not strict that **every** failure mode is documented for **every** workflow — only that **at least one** non-happy-path is described for each critical workflow. The `[STANDARD-RULE: GR-NN]` family covers common UI failure-state defaults (e.g., `GR-08` empty states, `GR-09` no-results, `GR-10` loading thresholds) — when a missing failure mode is covered by an active `GR-NN`, the disposition is `Standard-Rule-Applies`, not `Needs-Clarification`.

**Coverage thresholds:**

- `COVERED` — every named workflow has ≥1 documented non-happy-path; or every uncovered failure mode is `Standard-Rule-Applies`.
- `PARTIAL` — happy paths are described but non-happy-paths are entirely absent; some failure modes are `Standard-Rule-Applies` but others (e.g., financial reversal, permission edge-cases) need clarification.
- `ABSENT` — workflows are named but neither happy nor non-happy paths are described in any source.
- `OUT-OF-SCOPE-EXPLICIT` — corpus says workflow is read-only / display-only / phase-2 (no error paths needed in this phase).

**What is NOT a Dimension 4 finding:**

- A backend retry / queue-processing concern — those are server-side per `framework/shared/prototype-scope.md` for prototype target. Visual failure feedback (toast/banner per `GR-14`) is in scope; the retry mechanism itself is not.
- An ambiguity in the happy path itself — that's Dimension 4 (Vague predicates) of ambiguity-review territory, not completeness.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"User uploads attachment. System stores it and shows it in the invoice detail page."*
>
> No source describes: what happens when the upload fails? What happens when the user uploads a file type the system doesn't support? What happens when the file exceeds size limits? What happens when the user uploads concurrently from two tabs?
>
> Finding: `COMP-18 — Dim 4 — Major — Needs-Clarification — Location: brief.docx`.
>
> Authority: IEEE 29148 §6.4.2.3 item 5; Wiegers gap #5.

**Worked example — near-miss (do NOT flag):**

> Sources: `brief.docx`, `workshop-notes.md`
>
> *Brief describes upload happy path; `workshop-notes.md` covers failure modes ("we discussed: file-too-large shows inline error with max size; wrong-format shows inline error listing accepted types; network failure shows retry button; concurrent upload from two tabs wins-last-write with a warning toast").*
>
> Dimension 4 is `COVERED` for upload. Do not flag.

### Dimension 5 — Non-Functional Requirements

**Authority:** ISO/IEC 25010 (system & software quality model); Volere §10–17 (performance, accessibility, usability, security, availability, scalability, maintainability, portability); IEEE 29148 §6.4.2.3 item 6 (performance/quality requirements); Wiegers gap #2 (missing NFRs).

**Question:** For every NFR keyword in the corpus, does the corpus carry a measurable target?

**What to check:**

NFR keyword detection categories (the reviewer scans the corpus for any of):

- **Performance / latency:** *"fast"*, *"responsive"*, *"performant"*, *"low-latency"*, *"real-time"*, *"high throughput"*, *"scalable"*, response-time / page-load mentions without a millisecond budget.
- **Availability / reliability:** *"available"*, *"uptime"*, *"resilient"*, *"reliable"*, *"robust"*, *"stable"*, mentions without an SLO or failure-rate target.
- **Security:** *"secure"*, *"compliant"*, *"GDPR-compliant"*, *"POPIA-compliant"*, *"HIPAA-compliant"*, *"encrypted"*, *"audit-logged"*, mentions without specifying which fields, which retention period, which access controls, which audit events.
- **Accessibility:** *"accessible"*, *"WCAG-compliant"*, *"a11y"*, mentions without specifying WCAG level (A / AA / AAA), target audience (screen-reader users, keyboard-only users), conformance scope.
- **Usability:** *"intuitive"*, *"easy-to-use"*, *"user-friendly"*, *"polished"*, *"modern"* — these typically appear without operational measures (and are also ambiguity-review territory under Dimension 5 of that lens, by linguistic-subjectivity grounds; this lens flags them under completeness grounds when no measure exists anywhere in corpus).
- **Scalability / capacity:** *"scales to"*, *"handles N users"*, *"supports large datasets"*, mentions without enumerated concurrent users, data volumes, or growth assumptions.
- **Maintainability / extensibility:** *"easy to maintain"*, *"extensible"*, *"modular"*, mentions without operational criteria (code-quality target, deployment cadence, rollout strategy).

For each NFR keyword found in the corpus:

- Confirm whether the corpus carries a **measurable target** for that NFR within any source.
- A measurable target is: a number with units (ms, RPS, %, MB, concurrent-users), a standards reference (WCAG 2.1 AA), a regulatory citation (POPIA §X), or an SLA-style commitment (*"99.9% uptime during business hours"*).
- Bare keywords without thresholds are `PARTIAL` (the topic was raised but the requirement is untestable).
- NFR keywords absent entirely for a domain that obviously needs them (e.g., a financial system with zero mention of audit logging, encryption, or compliance) are `ABSENT`.

**Coverage thresholds:**

- `COVERED` — every NFR keyword in the corpus has a paired measurable target; or the obviously-relevant NFR categories for the system's domain are all addressed.
- `PARTIAL` — NFR keywords appear but lack measurable targets (e.g., *"system must be fast"* with no latency budget).
- `ABSENT` — obviously-relevant NFR categories for the domain are never mentioned (e.g., a healthcare system with zero security/compliance mention).
- `OUT-OF-SCOPE-EXPLICIT` — corpus says NFR category is deferred (*"performance tuning is phase 2"*).

**What is NOT a Dimension 5 finding:**

- A vague-predicate ambiguity (*"the system should be fast"* with no threshold) — log it under both lenses; ambiguity-review flags it as Dim-4 ambiguity, completeness-review flags it as Dim-5 incomplete-NFR. The cross-dimension consolidation step does **not** merge across reviewers (each artefact is independent); both findings are useful to the consultant.
- An NFR keyword with an explicit threshold *anywhere in the corpus* — even if the threshold appears in a different source than the keyword (the reviewer correlates across sources by topic, not by sentence).
- Storage-layer NFRs (DB query latency, index sizing) on `target: prototype` runs — these are out-of-scope-by-domain-default per `framework/shared/prototype-scope.md`.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"The system shall be POPIA-compliant."*
>
> No source enumerates: which fields constitute personal information, what retention period applies per field, what consent flow the existing system collects, what data-subject-rights operations must be exposed (access, rectification, erasure, portability), what audit-logging is required, where breach-notification responsibilities live.
>
> Finding: `COMP-22 — Dim 5 — Blocker — Needs-Clarification — Location: brief.docx`.
>
> Authority: Volere §12 (Security); Wiegers gap #2; ISO/IEC 25010 §7 (Security).

**Worked example — near-miss (do NOT flag):**

> Sources: `brief.docx`, `compliance-spec.md`
>
> *Brief names POPIA compliance; `compliance-spec.md` enumerates PII fields (name, ID number, email, address), retention (7 years per category), consent (opt-in at signup + reaffirm annually), data-subject rights (access via Settings → Privacy, erasure via support ticket), audit log (every read/write on PII tables, retained 7 years), breach response (notify within 72 hours via legal team).*
>
> Dimension 5 is `COVERED` for POPIA compliance. Do not flag.

### Dimension 6 — Business Rules & Decision Logic

**Authority:** BABOK §10.5 (Business Rules Analysis); Volere §9 (Business Rules); Wiegers gap #11 (missing business rules).

**Question:** For every conditional behaviour ("if X then Y") in the corpus, is the trigger condition specified to a level where a developer could implement a decision table?

**What to check:**

- Build a conditional set: every *"if … then …"*, *"when … the system should …"*, *"users can … unless …"*, *"approvals are required for …"*, etc.
- For each conditional, check whether:
  - The **trigger** is unambiguously specified (e.g., *"if invoice amount exceeds R10,000 then …"* — both threshold and currency unambiguous).
  - The **outcome** is unambiguously specified (e.g., *"… then require approval from a Finance Manager"* — both action and actor unambiguous).
  - The **else-branch** is specified or trivially absent (sometimes *"otherwise no approval required"* is implicit; sometimes it must be explicit because the else-branch has its own side effects).
- Implicit business rules — rules the reviewer would expect for the domain but that don't appear at all in the corpus — are `ABSENT`. *Examples: a payment system with no rule for refund eligibility; an HR system with no rule for leave-approval routing.*
- Cross-cutting policies (RBAC, auth, lifecycle) that are partially specified are `PARTIAL`.

**Coverage thresholds:**

- `COVERED` — every conditional behaviour in the corpus has unambiguous trigger and outcome; obvious-for-domain business rules are present.
- `PARTIAL` — some conditionals are well-specified, but other obviously-needed business rules (refund eligibility, approval routing, escalation triggers) are silent.
- `ABSENT` — the corpus contains business-flow descriptions but no decision logic at all.
- `OUT-OF-SCOPE-EXPLICIT` — corpus says decision logic is handled by an external rule engine (*"business rules live in BizRules-Pro; we just consume the outcome"*).

**What is NOT a Dimension 6 finding:**

- A vague-predicate threshold (*"if the user has been inactive for a while, log them out"*) — `inactive for a while` is ambiguity-review Dim-4 territory. Completeness logs this *only* if the rule itself is entirely missing, not because its threshold is fuzzy. (Both lenses may fire; that is correct — they are complementary.)
- A standard rule covered by `GR-NN`. Example: `GR-19` covers session-timeout defaults by domain — if the corpus is silent on idle/absolute timeouts and the domain is identified, the disposition is `Standard-Rule-Applies` (Authority: `GR-19`), not `Needs-Clarification`.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"Users can issue refunds for invoices marked Paid."*
>
> No source describes: refund eligibility (within how many days of payment?), refund amount (full only, partial allowed?), approval rules (do refunds above a threshold require manager approval, like the issue-invoice flow?), audit trail (must refund actions appear in the invoice's history?), reversal of accounting entries (does the refund automatically generate a credit-memo invoice?), or the customer-facing notification (do they receive an email on refund?).
>
> Finding: `COMP-26 — Dim 6 — Blocker — Needs-Clarification — Location: brief.docx`.
>
> Authority: BABOK §10.5; Wiegers gap #11.

**Worked example — near-miss (do NOT flag):**

> Sources: `brief.docx`, `refund-policy.md`
>
> *Brief names refund flow; `refund-policy.md` enumerates eligibility (within 90 days of Paid status), amount (partial allowed, line-item-level), approval (Finance Manager required ≥R5,000), audit (line item appended to invoice history), accounting (auto-generated credit memo with link), notification (email to customer email-on-file, deferred to next batch send).*
>
> Dimension 6 is `COVERED` for refund. Do not flag.

### Dimension 7 — Acceptance Criteria & Success Metrics

**Authority:** Volere "Fit Criterion" (per requirement); BABOK §11.5 (Acceptance and Evaluation Criteria); INCOSE R29 (Verifiable); Wiegers gap #6 (missing acceptance criteria).

**Question:** For every feature / requirement-candidate in the corpus, is there at least one measurable acceptance criterion (quantitative target, given/when/then scenario, or *"user can verify by …"* clause)?

**What to check:**

- Build a feature set: every named feature / use case / capability in any source.
- For each feature, check whether **any source** carries:
  - A **quantitative target** the feature must meet (e.g., *"page loads in <500ms p95"*, *"refund process completes in <3 business days"*).
  - A **given/when/then scenario** or equivalent (e.g., *"Given an invoice is Paid, when the user clicks Refund, then a Refund modal opens listing eligible line items"*).
  - A **verification clause** (*"user can verify by …"*, *"acceptance: …"*, *"done when …"*, *"success looks like …"*).
- Success metrics at the *system* level (e.g., *"reduce reconciliation time by 50%"*, *"target 80% adoption within 3 months"*) are also evidence of completeness; their absence on a flagship feature is `PARTIAL` or `ABSENT`.

**Coverage thresholds:**

- `COVERED` — every flagship feature has ≥1 acceptance criterion, and the corpus carries at least one system-level success metric.
- `PARTIAL` — some features have acceptance criteria, others (especially supporting features) do not; or system-level success metrics are absent.
- `ABSENT` — the corpus describes feature behaviour but no source states what "done" looks like for any feature.
- `OUT-OF-SCOPE-EXPLICIT` — corpus says acceptance criteria are owned by QA / will be written in a separate doc / are part of UAT planning.

**What is NOT a Dimension 7 finding:**

- A feature without testable acceptance because the feature *itself* is vague — that is, the feature can't be testable because nobody can tell what it does. That's an ambiguity-review issue (Dim 4/5/6 of that lens). Completeness logs acceptance-absent only on features that are themselves well-defined.
- Standard-rule-covered UI feedback (`GR-08` empty states, `GR-10` loading thresholds, `GR-14` toast/banner) — these have implicit acceptance via the standard rule; disposition is `Standard-Rule-Applies` when relevant.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"V1 features: customer list, invoice generation, payment status, refund flow, reconciliation report. Sprint-1 demo by end of month."*
>
> No source carries: acceptance criteria for any of the five features (no given/when/then, no target latency, no quantitative success criterion). No system-level success metric (no target reduction in reconciliation time, no target adoption, no target error-rate). The "end of month" is a delivery date, not an acceptance criterion.
>
> Finding: `COMP-31 — Dim 7 — Blocker — Needs-Clarification — Location: corpus-wide`.
>
> Authority: Volere Fit Criterion; BABOK §11.5; INCOSE R29; Wiegers gap #6.

**Worked example — near-miss (do NOT flag):**

> Sources: `brief.docx`, `acceptance-criteria.md`
>
> *Brief names features; `acceptance-criteria.md` carries per-feature given/when/then scenarios with target counts (e.g., "Given 1,000 invoices loaded, when the user filters by Customer, then the table updates in <500ms p95"). Brief states system-level goal: "reduce manual reconciliation time by 50% within 3 months of rollout, measured by support-ticket volume on the reconciliation queue."*
>
> Dimension 7 is `COVERED`. Do not flag.

### Dimension 8 — Integrations & External Dependencies

**Authority:** IEEE 29148 §6.4.2.3 item 3 (environmental conditions / external interfaces); Volere §13 (Maintainability / Portability / External Interfaces); Wiegers gap #9 (missing dependencies).

**Question:** For every external system named (database, API, third-party service, internal service), does the corpus state owner, contract (sync/async, schema, auth), and failure-mode behaviour?

**What to check:**

- Build an integration set: every external system mentioned (e.g., *"the CRM"*, *"the billing system"*, *"Stripe"*, *"Salesforce"*, *"the legacy system"*, *"the reporting database"*, *"our identity provider"*).
- For each integration, check whether the corpus states:
  - **Owner** — who runs this system (us / another team / a vendor)?
  - **Contract** — sync API (REST / GraphQL / RPC), async (webhook / queue / event stream), batch (file drop / SFTP)? What's the schema (link to OpenAPI / Protobuf / JSON-Schema, or at least the field names this system needs)?
  - **Auth** — how does this system authenticate to / from the new app (OAuth / API key / mTLS / service account)?
  - **Failure mode** — what does the new app do when this integration is unavailable, slow, returns errors, or returns stale data?
- Internal services within the new app are not external dependencies; this dimension is about systems whose contracts the new app cannot change.

**Coverage thresholds:**

- `COVERED` — every named integration has owner + contract + auth + failure-mode in some source.
- `PARTIAL` — integrations are named with partial detail (e.g., owner known, contract known, but no auth or failure-mode).
- `ABSENT` — integrations are named only by reference (*"we'll pull from the CRM"*) with no further detail.
- `OUT-OF-SCOPE-EXPLICIT` — corpus says the integration is "handled by another team" or "available via the existing API gateway" — the new project's responsibility ends at consumption.

**What is NOT a Dimension 8 finding:**

- An internal microservice within the new app (those belong to Dimension 3 (Data Entities) or Dimension 4 (Workflows)).
- A standard infrastructure dependency (the DB the new app uses, the cloud the new app runs on) — these are out-of-scope-by-domain-default on `target: prototype` per `framework/shared/prototype-scope.md`.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"The new system will pull customer data from the CRM and push invoices to the billing system."*
>
> No source states: who owns CRM / billing? What's the API contract (REST? webhook? batch)? Auth (OAuth? API key)? What happens when CRM is down (block invoice creation, queue and retry, use cached customer)? What happens when push to billing fails (rollback the new invoice, retry, alert)?
>
> Finding: `COMP-35 — Dim 8 — Blocker — Needs-Clarification — Location: brief.docx`.
>
> Authority: IEEE 29148 §6.4.2.3 item 3; Volere §13; Wiegers gap #9.

**Worked example — near-miss (do NOT flag):**

> Sources: `brief.docx`, `integration-spec.md`
>
> *Brief names CRM and billing; `integration-spec.md` enumerates: CRM owned by Sales team, REST sync (OpenAPI at link), OAuth client-credentials with refresh, on CRM-down show banner "Customer data temporarily unavailable" and disable Create-Invoice CTA; billing owned by Finance team, webhook async (schema-link), API key in vault, on push-fail enqueue and retry with exponential backoff, surface to user "Invoice queued for delivery" toast.*
>
> Dimension 8 is `COVERED` for both. Do not flag.

### Dimension 9 — Constraints, Assumptions & Open Issues

**Authority:** Volere §3 (Drivers), §5 (Assumptions), §18 (Open Issues); IEEE 830 §4.3 (TBD policy); Wiegers gaps #7 (constraints) and #8 (assumptions).

**Question:** Does the corpus carry explicit lists of assumptions (technology, infrastructure, organisational), constraints (regulatory, budget, timeline, contractual), and known open issues?

**What to check:**

- **Assumptions:** Does the corpus state assumptions explicitly? Common types:
  - **Technology assumptions** (*"we will use the existing React + Postgres stack"*, *"deployable to AWS only"*).
  - **Infrastructure assumptions** (*"runs in our existing Kubernetes cluster"*, *"behind the existing API gateway"*).
  - **Organisational assumptions** (*"Finance team will define the chart of accounts"*, *"a designer will produce final styles"*).
  - **User assumptions** (*"users have broadband"*, *"users are familiar with our existing CRM"*).
- **Constraints:**
  - **Regulatory** (*"must comply with POPIA, Section 14 timeline"*).
  - **Budget / timeline** (*"must launch by Q3 end"*, *"max 3-person team"*).
  - **Contractual** (*"vendor contract expires Dec; integration must move off legacy by Nov"*).
  - **Technical** (*"must not increase database load on the existing DB"*).
- **Open issues:** Volere §18 — issues the team knows exist but has not resolved. *"We're not sure whether refunds should be visible to customers directly or only via support."* — that's an open issue, not an absence; it should appear in an open-issues section.

The reviewer is looking for the **presence of these sections**, not their content. A brief that says *"Assumptions: (none listed)"* is more complete on Dimension 9 than a brief that has no assumption section at all — the former tells the reviewer the consultant considered assumptions; the latter leaves it ambiguous whether the consultant simply forgot.

**Coverage thresholds:**

- `COVERED` — corpus carries explicit assumption list, explicit constraints list, and explicit open-issues list.
- `PARTIAL` — one or two of (assumptions / constraints / open-issues) are present; the others absent.
- `ABSENT` — none of the three lists exist.
- `OUT-OF-SCOPE-EXPLICIT` — corpus says these lists will be maintained by the project team in a separate doc / ticket / wiki page.

**What is NOT a Dimension 9 finding:**

- An implicit assumption surfaced by the reviewer that the corpus doesn't carry (e.g., *"the brief assumes users have admin rights to the existing system but doesn't say so"*) — that's a finding, with severity Major and Disposition `Needs-Clarification`. (Implicit assumptions become explicit findings; the reviewer surfaces them.)
- A constraint stated in the corpus but not in a dedicated constraint section (e.g., *"must launch by Q3"* mentioned in passing in the brief intro) — this counts as covered if the statement is unambiguous; the reviewer doesn't require a "Constraints" header, only the content.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *Brief is a 4-page narrative document. No explicit Assumptions section. No explicit Constraints section. No explicit Open Issues section. The only constraint visible is "team of 3, launch Q3" buried in §2.*
>
> Finding: `COMP-40 — Dim 9 — Major — Needs-Clarification — Location: brief.docx`.
>
> *"The brief carries no explicit Assumptions list, no explicit Constraints list, and no explicit Open Issues list. Implicit assumptions surfaced during review: (a) users are inside the corporate VPN [no VPN requirement stated]; (b) the existing reconciliation file format will not change [no version-control of file format stated]; (c) Finance team can train end-users [no training plan stated]."*
>
> Authority: Volere §3, §5, §18; Wiegers gaps #7, #8.

**Worked example — near-miss (do NOT flag):**

> Source: `brief.docx`
>
> *Brief has three sections: "Assumptions: (1) AWS deployment, (2) existing Postgres, (3) users on broadband.", "Constraints: (1) POPIA compliance, (2) Q3 launch, (3) 3-person team.", "Open Issues: (1) refund-visibility-to-customers decision pending, (2) phase-2 mobile pending."*
>
> Dimension 9 is `COVERED`. Do not flag.

### Dimension 10 — Glossary, Terminology & Naming Consistency

**Authority:** IEEE 830 §4.3 item 5 (consistency); Volere §4 (Naming Conventions and Glossary); INCOSE R6 (unique definition for each term); BABOK §10.22 (Glossary).

**Question:** Does every domain-specific term used in more than one source have a definition somewhere in the corpus? Does the corpus avoid terminology drift (different terms for the same concept across sources)?

**What to check:**

- Build a term set: every domain-specific noun appearing across multiple sources (e.g., `Reconciliation`, `Statement`, `Invoice`, `Client`, `Customer`, `Account`, `Order`, `Refund`, `Audit`, `Approval`).
- For each term:
  - **Defined once?** Is there a glossary entry, in-passage definition (*"a reconciliation is …"*), or unambiguous-by-context use?
  - **Used consistently?** Or does the corpus use *Client* in one source and *Customer* in another for the same concept? *Invoice* in one and *Bill* in another? *Approval* in one and *Sign-off* in another? Cross-source terminology drift is `Major Needs-Clarification` because it forces the drafter to invent a canonical term and downstream may diverge from input usage.
- A glossary on disk (e.g., `glossary.md`, `terms.md`) is preferred but not required; in-passage definitions count as covered.

**Coverage thresholds:**

- `COVERED` — every domain term used cross-source has a definition somewhere; no terminology drift.
- `PARTIAL` — most terms defined, but ≥1 case of cross-source drift, or ≥1 domain term used cross-source without definition.
- `ABSENT` — no glossary, no in-passage definitions, multiple drifts.
- `OUT-OF-SCOPE-EXPLICIT` — corpus says glossary will be built downstream (*"we'll do a glossary in design phase"*).

**What is NOT a Dimension 10 finding:**

- A common English word with non-domain meaning (*"the system shall log every action"* — `log` is a common verb, not a domain term).
- A domain term used in only one source (single-source terms don't yet have drift to flag; cross-source consistency is the load-bearing test). They may appear under Dimension 3 (entity) or Dimension 6 (rule) depending on context.
- An ambiguity-review Dim-1 (lexical-ambiguity) issue — that fires on multi-meaning words. Completeness Dim-10 fires on undefined terms or drifted terms across sources; both may fire on the same word.

**Worked example — positive find:**

> Sources: `brief.docx`, `workshop-notes.md`, `interview-jane.md`
>
> *`brief.docx` uses **Client** throughout; `workshop-notes.md` uses **Customer** for the same entity (the company being billed); `interview-jane.md` uses **Account** in a finance-account sense — possibly the same entity, possibly different. No glossary on disk. No in-passage definitions for any of the three terms.*
>
> Finding: `COMP-44 — Dim 10 — Major — Needs-Clarification — Location: corpus-wide`.
>
> *"Cross-source terminology drift: Client (brief.docx) / Customer (workshop-notes.md) / Account (interview-jane.md) appear to refer to the same business entity but no source defines them or maps them as synonyms. The drafter will be forced to invent a canonical term, risking divergence from any source's preferred usage."*
>
> Authority: IEEE 830 §4.3 item 5; Volere §4; INCOSE R6; BABOK §10.22.

**Worked example — near-miss (do NOT flag):**

> Sources: `brief.docx`, `glossary.md`
>
> *Brief uses Client and Customer interchangeably; `glossary.md` defines: "Client: the company being billed. Customer: synonym for Client (legacy term used in the old CRM)."*
>
> Dimension 10 is `COVERED`. Do not flag.

---

## Finding schema

Every finding has all nine fields populated, in this order:

```
ID:                    COMP-NN              (sequential per run, zero-padded — COMP-01, COMP-02, …)
Dimension(s):          1..10                (multi-tag findings from Step 14 carry a sorted list e.g. [3, 6])
Severity:              Blocker | Major | Minor
Disposition:           Needs-Clarification | Standard-Rule-Applies | Out-of-Scope
Location:              corpus-wide | <filename>   (corpus-wide for absences across all sources; filename for partial-coverage where one source covers but others don't, or for explicit-exclusion quotes)
Evidence:              verbatim quote of the explicit-exclusion or partial-mention, OR the sentinel `(no mention in consumed corpus)`
Authority:             IEEE 29148 §X.Y / Volere §N / Wiegers gap #N / BABOK §X.Y / INCOSE R-NN / ISO/IEC 25010 §X / GR-NN  (one or more, semicolon-separated)
Problem:               one sentence — what is absent (or partially-covered, or explicitly excluded) and why it matters downstream
Elicitation question:  one sentence — ready-to-paste for stakeholder; required when Disposition = Needs-Clarification; the literal string `(not applicable — disposition resolves via standard rule)` for Disposition = Standard-Rule-Applies; the literal string `(not applicable — explicit out-of-scope)` for Disposition = Out-of-Scope
```

**Field rules:**

- **ID** is unique per run and reset to `COMP-01` on every fresh invocation. Revise loops keep their IDs; only Restart resets the sequence. The pipeline is **full overwrite** per run.
- **Dimension(s)** is a non-empty list of integers in [1, 10]. A single-dimension finding has a list of length 1; a multi-tag finding (output of Step 14 consolidation) has length ≥2. The list is sorted ascending. The **primary dimension** for sorting / ID purposes is the lowest entry.
- **Severity** is exactly one of three. No "Critical" or "Trivial".
- **Disposition** is exactly one of three: `Needs-Clarification` (corpus is silent and no rule applies — stakeholder elicitation needed), `Standard-Rule-Applies` (corpus is silent but an active `GR-NN` covers the gap deterministically), `Out-of-Scope` (corpus carries an explicit-exclusion statement OR the topic is out-of-scope-by-domain-default per `prototype-scope.md` when `target: prototype`).
- **Location** is either the literal string `corpus-wide` (for findings that span all sources, typically `ABSENT` cases on the coverage matrix) or a manifest row's `filename` field (for `PARTIAL` cases where one source partially covers the dimension, or for `OUT-OF-SCOPE-EXPLICIT` cases where one source carries the exclusion quote). **No line numbers**, no section anchors.
- **Evidence** is one of:
  - A verbatim quote ≤5 lines from the cited source (for `PARTIAL` findings — the partial mention is the evidence — or for `OUT-OF-SCOPE-EXPLICIT` findings — the exclusion quote is the evidence). The quote must be a substring of the corpus content the reviewer captured at Step 3.
  - The literal sentinel string `(no mention in consumed corpus)` for `ABSENT` findings where the entire corpus is silent on the topic. No fabrication — the sentinel is the explicit acknowledgement of silence.
- **Authority** is one or more authority references, semicolon-separated. The reviewer must cite at least one canonical authority per finding (IEEE / Volere / Wiegers / BABOK / INCOSE / ISO 25010) drawn from the dimension's `Authority:` header. For `Standard-Rule-Applies`-disposition findings, the `GR-NN` rule id must also appear in this field (Step 15 gate 12 enforces existence of the rule id in `framework/shared/general-rules.md`).
- **Problem** is one sentence stating which dimension fired, why the absence matters downstream, and (for `corpus-wide` Location) what would have been a covered alternative. *"`brief.docx` names 'Finance Manager' as primary user but no source carries first-hand voice; downstream `/requirements` cannot draft Finance Manager acceptance criteria from inputs that contain no Finance Manager perspective."*
- **Elicitation question** is:
  - For `Needs-Clarification` findings: a one-sentence stakeholder-facing question. Must end with `?`, must contain the Location field's filename as a substring **unless** Location is `corpus-wide` (in which case the question must name at least one consumed source filename in its prose so the stakeholder knows what the reviewer was looking at). Must be specific enough that a one-sentence answer or a single artefact (interview, doc, file) resolves the gap. Must not embed a candidate answer as the expected response (non-leading).
  - For `Standard-Rule-Applies` findings: the literal string `(not applicable — disposition resolves via standard rule)`. No question is generated — the drafter will render `[STANDARD-RULE: GR-NN]` automatically downstream.
  - For `Out-of-Scope` findings: the literal string `(not applicable — explicit out-of-scope)`. No question is generated — the drafter will render `[OUT-OF-SCOPE: domain-default]` automatically downstream.

A finding missing any field is invalid. Step 15 gate 1 enforces this.

---

## Severity rubric

The reviewer assigns exactly one severity per finding using this rubric. Severity drives the triage callout and the verdict mapping (independently of disposition).

### Blocker

- The gap will cause **divergent implementation or blocked drafting** — the drafter cannot produce `/requirements` content without resolving this gap, or different developers reading the inputs will build incompatible features.
- Typical patterns:
  - Dimension 1 — primary actor named but no first-hand voice in any source (drafter cannot write acceptance criteria for them).
  - Dimension 2 — no exclusion list (drafter cannot draw scope boundaries).
  - Dimension 3 — flagship entity named but no key fields enumerated.
  - Dimension 4 — happy path described but no non-happy-path on a critical workflow (e.g., financial transaction).
  - Dimension 5 — compliance keyword (POPIA / GDPR / HIPAA) with no measurable target.
  - Dimension 6 — financial / regulatory business rule entirely absent.
  - Dimension 7 — flagship feature with no acceptance criteria anywhere.
  - Dimension 8 — financial / data-flow integration with no contract or failure-mode.

### Major

- The gap will require a **clarification round before implementation**, but isn't fatal.
- Typical patterns:
  - Dimension 1 — secondary actor named with no first-hand voice.
  - Dimension 3 — secondary entity with partial attributes.
  - Dimension 4 — non-critical workflow with one missing failure mode.
  - Dimension 5 — non-core NFR keyword with no measurable target (e.g., *"the dashboard should be modern"*).
  - Dimension 9 — implicit assumption the reviewer can surface; constraint stated only informally.
  - Dimension 10 — terminology drift across sources for a common business concept.

### Minor

- **Stylistic.** The gap could be resolved by inference, convention, or design-phase elaboration; flagging it produces a cleaner spec.
- Typical patterns:
  - Dimension 3 — diagnostic / debug entities with partial attributes.
  - Dimension 6 — auxiliary business rules covered by `GR-NN` (these are typically `Standard-Rule-Applies`, severity Minor).
  - Dimension 7 — supporting features with partial acceptance criteria.

### Severity → Verdict mapping

The artefact's Executive Summary states one verdict:

| Verdict | When |
|---|---|
| `BLOCKED` | At least one `Blocker` severity finding exists with `Disposition: Needs-Clarification`. |
| `NEEDS-ELICITATION` | No Blockers (or Blockers exist but all carry `Disposition: Standard-Rule-Applies` / `Out-of-Scope`), but ≥1 finding with `Disposition: Needs-Clarification`. |
| `ACCEPTED-WITH-GAPS` | All findings carry `Disposition: Standard-Rule-Applies` or `Out-of-Scope`. Zero stakeholder questions to ask. |

There is no fourth verdict. "Looks good" / "Clean" / "All covered" are not verdicts.

A truly clean run — zero findings on all ten dimensions — requires every dimension to carry a Justification block ≥3 sentences; the verdict is then `ACCEPTED-WITH-GAPS` and the Executive Summary explicitly notes "zero findings, all Justifications present".

---

## Disposition rubric (the absent-vs-out-of-scope test)

Disposition is the methodology's load-bearing pipeline contribution. Every finding carries exactly one of three values; the reviewer determines disposition at Step 14 of the agent (the disposition-assignment step) per the following decision tree:

### Step 1 of the decision tree — explicit out-of-scope quote?

For each candidate finding, scan the corpus for explicit exclusion language naming the topic:

- *"out of scope"*, *"phase 2"*, *"phase 3"*, *"not in this release"*, *"deferred"*, *"future work"*, *"not handled here"*, *"won't fix"*, *"won't address"*, *"backlog"*, *"non-goal"*, *"explicit non-objective"*.
- Topic-naming: the exclusion quote must name the dimension's topic (e.g., *"mobile is phase 2"* for a UI-on-mobile gap; *"compliance is in scope only for V2"* for a Dim-5 compliance gap).

If found: `Disposition = Out-of-Scope`, Evidence = the exclusion quote (verbatim, ≤5 lines), Location = the filename of the source carrying the exclusion. Elicitation question = `(not applicable — explicit out-of-scope)`.

### Step 2 — covered by an active `GR-NN` rule?

Load `framework/shared/general-rules.md`. For each candidate finding, check whether any `GR-NN` rule's `Applies to:` predicate covers the dimension's topic for the candidate. The reviewer must match by content, not by string match — `GR-01` (Viewer role action hiding) covers RBAC-on-Viewer gaps under Dimension 1 (Stakeholder & Role Coverage) **only** when the Viewer role is named in the corpus and the RBAC-on-Viewer scope falls within the rule's predicate.

If found: `Disposition = Standard-Rule-Applies`, Authority = `<authority headers from dimension>` + `; GR-NN`, Evidence = `(no mention in consumed corpus)` (the rule is the resolution, not the corpus). Elicitation question = `(not applicable — disposition resolves via standard rule)`.

### Step 3 — out-of-scope by domain default?

If `target == "prototype"` (read from the manifest at Step 2 of the agent), load `framework/shared/prototype-scope.md`. If the dimension's topic falls under the *"Not Prototypable (Filter Out)"* section (e.g., backend API implementation, database schema, DevOps, performance optimization techniques), the finding is out-of-scope by domain default.

If matched: `Disposition = Out-of-Scope`, Evidence = `(no mention in consumed corpus)`, Authority = `<authority headers from dimension>` + `; prototype-scope.md`. Elicitation question = `(not applicable — explicit out-of-scope)`.

If `target == "application"` or `target == null`: this step does **not** fire — every dimension is in-scope for application builds, and `null` defaults to prototype-policy-relaxed-on-domain-defaults (the reviewer surfaces all such cases as `Needs-Clarification` until the consultant sets the target via the `/requirements` pipeline). The reviewer flags target-ambiguity as a Diagnostics-block note rather than a finding.

### Step 4 — default

If none of Steps 1–3 fired: `Disposition = Needs-Clarification`. Evidence = `(no mention in consumed corpus)` for `corpus-wide` Location, OR a partial-coverage quote for filename-scoped Location. Elicitation question = a one-sentence stakeholder-facing question per the elicitation-question authoring rules below.

### Severity is independent of disposition

A finding can be `Blocker` + `Out-of-Scope` (the gap is severe but excluded), or `Major` + `Standard-Rule-Applies` (the gap is moderate but rule-covered), or `Minor` + `Needs-Clarification`. The severity → verdict mapping above explicitly inspects disposition: `Blocker` findings that resolve via `Standard-Rule-Applies` or `Out-of-Scope` do **not** trigger `BLOCKED`. Only `Blocker + Needs-Clarification` triggers `BLOCKED`.

---

## Cross-dimension consolidation rule (Step 14 of the agent — note: the agent's step layout puts disposition assignment immediately after consolidation, so consolidation is Step 14 in the agent and dispositions are Step 15. The reference here numbers consolidation as the procedure regardless of agent step number.)

A single corpus span (for `PARTIAL`-style findings) or a single topic (for `ABSENT`-style findings) can trip multiple dimensions:

- *"the system shall manage Customers"* with no key fields and no first-hand-voice from any user-of-customers trips Dimension 3 (entity attributes absent) and Dimension 1 (actor voice absent).
- A mention of *"reconciliation should be fast"* with no threshold and no error-path trips Dimension 5 (NFR target absent) and Dimension 4 (failure modes absent).

The consolidation rule (applied at the agent's consolidation step, before disposition assignment):

1. After the ten sequential sweeps emit candidate findings, walk the candidate list.
2. For **`ABSENT`-style** findings (Location = `corpus-wide`, Evidence = `(no mention in consumed corpus)`): merge any two candidates whose `Problem` paragraphs reference the same topic (e.g., same entity name, same actor name, same workflow name) and whose dimensions are not the same. Set `Dimensions(s)` to the sorted-distinct list, concatenate the Problem sentences with `; ` separators (de-dup on exact-string match), and use the lowest dimension as the **primary dimension** for ID-ordering and section-rendering.
3. For **`PARTIAL`-style** findings (Location = a filename, Evidence = a partial-coverage quote): merge two candidates whose Evidence spans overlap by ≥80% (using the shorter span as the denominator). Apply the same dimension-list / Problem-concatenation rules.
4. **Do not merge across disposition.** A finding with `Disposition: Needs-Clarification` is never merged with a finding with `Disposition: Out-of-Scope` even if topics overlap — the disposition difference signals a real semantic split (one is unanswered, the other is resolved-by-exclusion).
5. **Do not merge across severity.** A `Blocker` finding is never merged with a `Minor` finding even on the same topic; the severity split indicates the merged finding would carry the higher severity in some interpretations and the lower in others, and the gap-register loses precision.

The merged finding's Dimension(s) is the sorted-distinct list (e.g., `[1, 3]` for *"Customer entity has no fields and no actor voice"*). The Findings Table renders the multi-tag finding's `Dim(s)` column as a bracketed list (e.g., `[1, 3]`). The merged finding renders once in its primary dimension's per-dimension section; the other dimension sections do not re-list it (Step 15 gate 9's row-count accounting depends on each finding counting once against its primary dimension).

---

## The absent-vs-out-of-scope test

The methodology's load-bearing rule, applied at logging time and enforced at gate-sweep time.

Before logging any candidate finding, the reviewer must answer **three** questions in order:

1. **Is the corpus silent on this topic?** Scan all consumed sources. If a source carries explicit content satisfying the dimension's coverage threshold, the candidate is **not** absent — drop it. If multiple sources together cover the topic at threshold, the candidate is not absent — drop it.
2. **Does the corpus explicitly exclude this topic?** Scan for exclusion language naming the topic. If found, the candidate is logged with `Disposition: Out-of-Scope` — keep it (the drafter needs to see the exclusion to render `[OUT-OF-SCOPE: domain-default]` markers).
3. **Does a `GR-NN` rule cover this topic?** Scan `framework/shared/general-rules.md`. If found, the candidate is logged with `Disposition: Standard-Rule-Applies` — keep it (the drafter needs to see the gap to render `[STANDARD-RULE: GR-NN]` markers).

If none of the three fire, the candidate is logged with `Disposition: Needs-Clarification`.

**The discipline:** the reviewer does not silently drop `Out-of-Scope` or `Standard-Rule-Applies` findings; the pipeline value comes from surfacing the pre-classification so the drafter has the full picture downstream. Silent drops would force the drafter to re-derive the disposition, defeating the methodology's contribution.

**False positives are inevitable.** A reviewer who over-detects absences (e.g., flags every NFR keyword the corpus didn't quantify) produces noise. The mitigation: the strict dimension-by-dimension coverage thresholds above (PARTIAL / COVERED) and the consultant Revise loop at Step 17. The reviewer must filter at logging time, not at write time — but the consultant strikes false positives in Revise.

---

## Elicitation-question authoring rules

Only `Needs-Clarification`-disposition findings carry elicitation questions. `Standard-Rule-Applies` and `Out-of-Scope` carry sentinel strings (see Finding schema above). The four rules below govern composition of the `Needs-Clarification` questions (enforced at Step 15 gate 11):

1. **Specific enough that a one-sentence answer or a single artefact resolves the gap.** *"In `brief.docx`, can we schedule a one-hour interview with a Finance Manager to capture their daily workflow, common errors, and what 'done' looks like for them?"* — the answer is yes/no + a scheduled time, or a substitute (existing meeting recording, persona doc). *"What does Finance Manager do?"* is too open-ended.
2. **Ends with `?`.** A clarification question that doesn't end with a question mark is not a question. Gate 11 enforces this syntactically.
3. **References the source filename or surfaces multi-source context.**
   - For findings with `Location: <filename>`: the question must contain the filename as a substring (*"In `brief.docx`, …"*).
   - For findings with `Location: corpus-wide`: the question must name at least one consumed source filename in its prose so the stakeholder has context for where the reviewer was looking. *"`brief.docx` names Finance Manager as primary user; can we schedule a one-hour interview to capture their workflow?"*
4. **Non-leading.** The question must not embed an obvious answer as the expected response. *"Is the Finance Manager interview missing because the role hasn't been hired yet?"* primes the stakeholder to confirm one explanation. *"Can we schedule a Finance Manager interview, or — if the role isn't filled — point to a substitute (workshop, persona doc, existing meeting recording)?"* leaves open.

For multi-tag findings (Step 14 consolidation output), the question addresses the most-actionable dimension first, or — when severities tie — produces a compound question naming both dimensions:

> *"In `brief.docx`, for the Customer entity: what are the key fields and lifecycle states, and can we schedule a Finance Manager (the primary user-of-customers) interview to capture the daily-use perspective?"*

---

## Quality gates (run after Dimension 10, after consolidation, after disposition assignment, before write)

Twelve gates. All are hard. If any gate fails, the reviewer does **not** write the artefact — it surfaces a structured error via `AskUserQuestion`. See `framework/agents/reviews-inputs/completeness-reviewer.md > Step 15` for the halt contract.

1. **Every finding has all nine schema fields populated.** Missing-field findings are invalid.
2. **Every finding's `Dimension(s)` is exactly one integer 1–10 (for single-dimension) or a sorted-distinct list of ≥2 integers in [1, 10] (for multi-tag).** No dimension 0; no dimension 11+.
3. **Every finding's Severity is exactly one of `Blocker | Major | Minor`.**
4. **Every finding's Evidence is either a verbatim substring of `quote_index_by_filename[location]` (for filename-scoped Locations with quoted evidence) or the literal sentinel `(no mention in consumed corpus)` (for `corpus-wide` Locations with sentinel evidence).** Paraphrased or fabricated evidence is a gate failure.
5. **Every finding's Location is either the literal string `corpus-wide` or matches a `corpus[*].filename`.** Citations to non-corpus filenames are a gate failure. Findings citing `Unsupported`-tier filenames are not permitted.
6. **Every finding's Disposition is exactly one of `Needs-Clarification | Standard-Rule-Applies | Out-of-Scope`.**
7. **Every finding's Authority field contains at least one canonical authority reference matching the dimension's `Authority:` header (IEEE / Volere / Wiegers / BABOK / INCOSE / ISO 25010).** Authority lookups missing the canonical-source prefix are a gate failure.
8. **Every dimension reports ≥1 finding or a non-empty Justification block ≥3 sentences citing specific evidence and naming at least one filename from the corpus.** Silent zero-finding dimensions are a methodology violation.
9. **The Findings Table row count equals the sum of per-primary-dimension finding counts.** Multi-tag findings count once, against their primary dimension. Drift is a render bug.
10. **The artefact's `MANIFEST_FINGERPRINT` field equals the SHA-256 of `requirements/source-manifest.json` captured at Step 2, AND every Source-roster (Consumed) `sha256[:8]` matches its manifest row's `sha256` field.** Mismatch means the artefact reviewed one version of the input set and reports against another.
11. **Every `Needs-Clarification`-disposition finding has a non-sentinel Elicitation question ending with `?`. For `Location: <filename>` findings, the question contains the filename as a substring; for `Location: corpus-wide` findings, the question contains at least one consumed-source filename as a substring.** Every `Standard-Rule-Applies` finding has the literal sentinel `(not applicable — disposition resolves via standard rule)`. Every `Out-of-Scope` finding has the literal sentinel `(not applicable — explicit out-of-scope)`.
12. **Every `Standard-Rule-Applies`-disposition finding cites at least one existing `GR-NN` id from `framework/shared/general-rules.md` in its Authority field, and the cited id exists as a heading in that file.** The reviewer does not invent `GR-NN` ids.

---

## Coverage matrix construction

The coverage matrix is a 10-row × N-column grid (where N = number of consumed sources from the corpus). It appears between the Executive Summary and the Triage callout in the rendered artefact.

**Cell values:**

- `COVERED` — this source's content satisfies the dimension's coverage threshold (either alone or in combination with other sources; see the per-dimension threshold definitions).
- `PARTIAL` — this source partially addresses the dimension (mentions the topic but doesn't meet threshold).
- `ABSENT` — this source does not address the dimension at all.
- `OUT-OF-SCOPE-EXPLICIT` — this source carries an explicit-exclusion quote for the dimension.

**Matrix-row semantics:** a dimension's row aggregates per-source coverage from each source independently. A dimension is `COVERED` for the **corpus** if *any* source carries `COVERED` (per-dimension threshold met). A finding fires only when the **corpus-wide** coverage falls short, not when a single source falls short while others cover.

**Matrix-column semantics:** each consumed source has its own column. Sources with `tier: Unsupported` are not in the matrix (they are in the Skipped roster only). A source can be `COVERED` on some dimensions and `ABSENT` on others — that is the expected shape (a brief covers scope and assumptions but not data entities; a spec doc covers entities but not stakeholders).

**Rendering convention:** the matrix is a sticky-thead HTML table (`<table class="coverage-matrix">` in `framework/assets/reviews-inputs/template-completeness.html` — no heatmap / inline-SVG). The first column (`<th scope="row">`) is the dimension name (with the dimension number in parentheses). Subsequent columns are one per consumed-source filename. Cells render the four cell-value tokens above as coverage chips (`cov-Covered` / `cov-Partial` / `cov-Absent` / `cov-Out-of-scope-explicit`).

---

## Output presentation

The artefact renders as a self-contained HTML report (the reviewer substitutes pre-escaped values + pre-rendered HTML fragments into `framework/assets/reviews-inputs/template-completeness.html`; one inline `<style>`, no external CSS/JS/fonts, no diagram/heatmap — coverage is the HTML table). The per-block HTML schemas (coverage-matrix table, triage table, findings table, per-dimension finding `<article>`s, elicitation groups, source roster, diagnostics `<details>`) live in the template's leading comment. The fixed section ordering is:

0. **In plain terms** — the `{{PLAIN_SUMMARY}}` lead block: 2–5 plain-English sentences answering what this review is, what it found, and what to do next. A faithful condensation of the findings below — introduces no finding, count, or claim not already in the punch-list. Rendered as `<section id="plain-terms">` immediately before the Executive Summary; listed first in the TOC. See `framework/shared/output-readability.md` and the `## Reader & plain language` section of `framework/assets/characters/completeness-inputs-review.md`.
1. **Header (Overview)** — title (`<h1 id="top">` + `<title>`) + a `dl.meta-grid` metadata block: `Domain`, `Generated` (ISO-8601 UTC), `Manifest SHA-256` (SHA-256 of `requirements/source-manifest.json`), `Target` (the manifest's `target` field, or `(unset)`), `Reviewer` (fixed string *"Completeness Review (IEEE 29148 / IEEE 830 / Volere / BABOK / Wiegers / INCOSE, ten-dimension, inputs-side)"*), `Sources consumed` (count), `Sources skipped` (count).
2. **Executive Summary** — total findings, severity tally (Blocker / Major / Minor), disposition tally (Needs-Clarification / Standard-Rule-Applies / Out-of-Scope), per-dimension counts, single-sentence verdict per the verdict-mapping table.
3. **Verdict** — exactly one of `BLOCKED` / `NEEDS-ELICITATION` / `ACCEPTED-WITH-GAPS`, rendered in the Executive Summary as a `<span class="verdict verdict-{VERDICT}">` banner (the token also drives the banner's colour class). It carries no other prose.
4. **Coverage matrix** — a sticky-thead HTML table (10 rows × N consumed-source columns; see construction rules above; no heatmap/SVG). Provides the executive bird's-eye view; the consultant should read this section in under thirty seconds.
5. **Triage** — *"Top issues to address first"* callout (≤10 entries: every `Blocker + Needs-Clarification` first, then `Major + Needs-Clarification` findings sorted by primary dimension ascending, then within-dimension by COMP-NN ascending; never includes `Standard-Rule-Applies` or `Out-of-Scope` findings even if Blocker severity, because those have no action item for the stakeholder).
6. **Source roster** — Consumed + Skipped tables.
   - **Consumed table.** Columns: `filename`, `tier`, `sha256[:8]`, `dimensions-covered`, `dimensions-partial`, `dimensions-absent`. One row per `corpus[*]` entry.
   - **Skipped table.** Columns: `filename`, `reason`. One row per `skipped_rows[*]` entry, or the italic *"(no sources skipped this run)"* line if empty.
7. **Findings table** — one row per finding. Columns: `ID`, `Dim(s)`, `Sev`, `Disposition`, `Location`, `Problem (one line)`. Sorted Blocker → Major → Minor, then within-severity by primary dimension ascending, then by COMP-NN ascending. Pipe characters in Problem strings escaped as `\|`.
8. **Per-Dimension sections (1–10)** — one `<section id="dim-N">` per dimension, in dimension order, each headed `Dimension N — <dimension name>`. Variants (full per-block HTML schema in the template comment):
   - **Variant A (≥1 finding on this primary dimension):** a `<div class="findings-list">` of finding `<article id="COMP-NN">`s. Each finding carries all nine schema fields: ID, Severity, Disposition, Dimensions (`[N]` or `[N, M]` for multi-tag), Location (`corpus-wide | filename`), Evidence (verbatim quote ≤5 lines in a `<blockquote class="evidence"><pre>`, OR the sentinel `(no mention in consumed corpus)` in a `<blockquote class="evidence sentinel">`), Authority (semicolon-separated), Problem (one sentence), Elicitation question (ends with `?`, names filename; OR a sentinel string).
   - **Variant B (zero findings on this primary dimension):** a `<div class="justification">` of ≥3 sentences citing specific evidence (filenames + verbatim quotes) explaining why the dimension is covered across the consumed corpus. *"Clean"* / *"Looks fine"* / *"Nothing to report"* are not justifications.
9. **Suggested elicitation questions (grouped by source filename)** — one `<div class="elicitation-group">` per consumed filename that contributed ≥1 `Needs-Clarification` finding (where the finding's `Location` is the filename, OR `corpus-wide` with the filename named in the elicitation question prose). Each group heads with the filename and lists its elicitation questions in COMP-NN ascending order as an `<ol class="elicitation-list">`, ready to paste into a client follow-up. `Standard-Rule-Applies` and `Out-of-Scope` findings are excluded from this section. If a finding has Location = `corpus-wide`, it appears under each filename it names in its prose. If multiple filenames qualify, the finding appears under each. Example (rendered as one group per filename): a group headed *"Questions for stakeholders of `brief.docx`"* containing *"In brief.docx, can we schedule a one-hour interview with a Finance Manager … (COMP-04)"* and *"In brief.docx, for the Customer entity: what are the key fields, lifecycle states, and identity rules? (COMP-12)"*.
10. **Diagnostics** — a collapsed `<details>` wrapping five subsections:
    - **Quality gates** — table listing all 12 gates with `PASS` / `FAIL` + flagged items.
    - **Coverage map** — one row per consumed filename: `filename`, `tier`, total finding-count contributed, `dimensions-with-findings`, `dimensions-with-justification`.
    - **Disposition breakdown** — per-dimension counts of each disposition: `Dim | Needs-Clarification | Standard-Rule-Applies | Out-of-Scope`. Verifies the disposition-step assignment didn't silently drop or mis-route findings.
    - **Override log** — if Step 15 returned via Override, list every failing gate and its flagged items. Otherwise the single line *"All quality gates passed; no override invoked."*
    - **Run history** — single line *"Full overwrite per run; no carried-over findings."* (Mirrors the no-additive-merge contract.)

The artefact is a gap register + action list, not a narrative. Prose between findings is minimised; the consultant should be able to read the Coverage Matrix in under thirty seconds, the Triage callout in under two minutes, jump to the per-dimension section for context on any finding, and copy the elicitation-questions section into a client email in one selection.

---

## Anti-patterns

- **Logging a candidate without applying the absent-vs-out-of-scope test.** The test is the methodology's load-bearing rule. If you cannot confirm the corpus is silent on the topic *and* check for explicit-exclusion quotes *and* check for active `GR-NN` rules, the candidate is incompletely classified — finish the classification before logging.
- **Fabricating evidence.** For `PARTIAL` findings, the Evidence quote must be verbatim from the cited source. For `ABSENT` findings, the sentinel `(no mention in consumed corpus)` is the only permitted Evidence value — paraphrasing or summarising the silence is fabrication. Gate 4 enforces this at the artefact-validation layer.
- **Inventing `GR-NN` ids.** The `Standard-Rule-Applies` disposition requires citing an existing rule from `framework/shared/general-rules.md`. Gate 12 enforces this. If the dimension's gap is rule-shaped but no rule exists yet, the disposition is `Needs-Clarification` and the elicitation question is the stakeholder follow-up. Do not propose new `GR-NN` ids in the artefact — `general-rules.md` is appended to via a separate process.
- **Silently dropping `Out-of-Scope` or `Standard-Rule-Applies` findings.** These findings exist precisely to surface the pre-classification to the drafter. Dropping them defeats the methodology's contribution. Every dimension's findings include all three disposition types when applicable.
- **Conflating completeness with ambiguity.** A vague phrase (*"the system should be fast"*) admits multiple interpretations — that's an ambiguity-review Dim-4 finding. The completeness lens fires on the absence of a measurable target. Both lenses may fire on the same source span; that is correct and complementary. Do **not** suppress completeness findings because ambiguity-review will catch them.
- **Conflating completeness with adversarial.** Adversarial-review's Dimension 1 (Stakeholder & Role Coverage) and Dimension 2 (Domain & Workflow Coverage) overlap completeness Dimensions 1 and 4 at a coarser, thematic grain. The completeness lens is granular (per-dimension findings, anchored per-authority). Both lenses may fire; each surface their own findings under their own COMP-NN / ADV-NN id sequences.
- **Conflating absent with under-specified.** Under-specified content is in the corpus and could be more detailed (that's typically ambiguity-review or another lens). Absent content is *not in the corpus at all* and is the completeness-review focus. The two are different; the reviewer files in the right lens.
- **Failing to check for explicit exclusions before logging absence.** A finding logged as `Needs-Clarification` when the corpus has an `out-of-scope` quote naming the topic is a methodology violation — the disposition is wrong, and the drafter will produce `[AI-SUGGESTED]` markers where `[OUT-OF-SCOPE: domain-default]` is correct.
- **Punching single sources for corpus-wide gaps.** *"`brief.docx` does not enumerate Customer fields"* is wrong if `customer-spec.md` does — the corpus-wide coverage is what matters, not per-source coverage. Use `Location: corpus-wide` for `ABSENT` cases (the entire corpus is silent on the topic). Use `Location: <filename>` only when the finding is about that source specifically (e.g., an explicit-exclusion quote, or a partial-coverage statement that's directly cited).
- **Generic findings.** *"`brief.docx` is incomplete"* is not a finding. Cite the specific dimension, the specific topic, the specific authority, the specific elicitation question.
- **Inflating severity.** Reserve `Blocker` for gaps that will block drafting or cause divergent implementation. A missing terminology drift on a non-core noun is not a Blocker.
- **Collapsing severity into binary.** Severity drives triage. `Blocker / Major / Minor` is a three-bucket prioritisation, not "important / not".
- **Citing line numbers in Location.** The Location field is `corpus-wide` or a `filename`. Multimodal sources have no lines; `.converted.md` line numbers drift between markitdown runs.
- **Using inline `[SRC: <filename>]` markers inside Problem, Authority, Elicitation-question fields.** The Evidence + Location pair is the citation; do not duplicate it in prose.
- **Skipping cross-dimension consolidation.** A topic tripping dimensions 1 and 3 (no first-hand voice, no key fields) on the same entity must emit one consolidated finding with `Dimensions: [1, 3]`, not two separate findings. Step 14 of the agent handles this; bypassing it produces double-counting in gate 9.
- **Reviewing against the synthesised requirements doc.** Do not consult `requirements/requirements.md` or any other `/requirements`-pipeline derivative. The review's contract is to critique the **raw inputs**.
- **Reviewing against parallel reviews.** Do not consult `review-inputs/ADVERSARIAL/adversarial-review.html` or `review-inputs/AMBIGUITY-REVIEW/ambiguity-review.html` to triangulate findings. Each input-pipeline lens is independently grounded in the manifest.
- **Skipping the strict-Justification rule.** A dimension with zero findings requires a non-empty Justification block ≥3 sentences citing specific evidence and naming at least one filename. *"Clean"* is not a Justification.

---

## Voice and stance

The reviewer's stance is defined in `framework/assets/characters/completeness-inputs-review.md` — coverage-skeptical, authority-bound, evidence-required, absent-vs-out-of-scope-disciplined, no-rubber-stamping. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact additionally follows `framework/shared/output-readability.md` (human-readability standard): the reviewer writes the "In plain terms" lead preserving severity verbatim; glosses review jargon (severity, disposition, dimension, verdict, coverage threshold, elicitation question) at first use in human-readable prose; leaves client domain vocabulary (e.g. Finance Manager, POPIA, Invoice, Customer) unglossed; keeps punch-list discipline below the lead; preserves Location + verbatim Evidence for every finding; adds no `[SRC:]` markers (reviews have no downstream machine consumer). The lead is the one sanctioned narrative exception to the punch-list — all other sections remain telegraphic.

---

## References

- **IEEE Std 830-1998 — Recommended Practice for Software Requirements Specifications.** §4.3 enumerates the eight quality attributes including *complete*; §4.3.5 defines completeness as *every requirement included* + *every input situation addressed* + *no TBDs except those with tracked owners*.
- **ISO/IEC/IEEE 29148:2018 — Systems and software engineering — Life cycle processes — Requirements engineering.** §5.2.4 (completeness as a stakeholder requirement attribute); §6.4.2.3 (the nine system-requirement completeness checks: stakeholders, operational scenarios, lifecycle phases, environmental conditions, abnormal conditions, performance/quality, design constraints, applicable laws, derived-requirement traceability); §6.4.3 (data requirements). The canonical authority.
- **Wiegers, K. E. & Beatty, J. (2013).** *Software Requirements* (3rd ed.). Microsoft Press. Chapter 19 (Verification and validation) and the 11-gap catalogue (missing functional reqs, NFRs, actors, data definitions, exceptions, acceptance criteria, constraints, assumptions, dependencies, UI behaviour, business rules) inform Dimensions 1, 3, 4, 5, 6, 7, 8, 9.
- **Robertson, S. & Robertson, J. (2012).** *Mastering the Requirements Process: Getting Requirements Right* (3rd ed.). Addison-Wesley. The Volere template's 35 sections; §3 Drivers, §4 Naming Conventions and Glossary, §5 Assumptions, §7 Data, §9 Business Rules, §10–17 Non-Functional Requirements, §13 External Interfaces, §18 Open Issues, §26 Waiting Room (out-of-scope tracking).
- **IIBA (2015).** *Business Analysis Body of Knowledge (BABOK Guide v3).* §3.4 (Requirements verification), §10.5 (Business Rules Analysis), §10.10 (Concept Modelling), §10.22 (Glossary), §10.41 (Scope Modelling), §10.43 (Stakeholder List), §11.5 (Acceptance and Evaluation Criteria).
- **INCOSE (2019).** *Guide for Writing Requirements (v4).* INCOSE-TP-2010-006-04. R3 (Completeness), R6 (unique definition for each term), R29 (Verifiable), R37 (set completeness), R38 (no missing requirements), R39 (Bounded — explicit scope).
- **ISO/IEC 25010:2011 — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models.** §4 (Quality in use); §7 (Product quality characteristics — Functional suitability, Performance efficiency, Compatibility, Usability, Reliability, Security, Maintainability, Portability). Anchors Dimension 5 NFR coverage.
- **Sibling lenses under `/review-inputs`:** `framework/assets/reviews-inputs/adversarial-reference.md` (thematic seven-dimension critique) and `framework/assets/reviews-inputs/ambiguity-reference.md` (linguistic seven-dimension ambiguity sweep). Completeness is the granular gap-register sibling; the three lenses run independently and the consultant can run all three for layered coverage.
- **Companion `/requirements`-pipeline skill (inspiration, not load target):** `framework/skills/completeness-gap-pass.md` — walks a synthesised draft against the `topics-requirements.md` bijection invariants and the same `general-rules.md` / `prototype-scope.md` decision tree this reviewer uses. The drafter consumes that skill; the reviewer here surfaces gaps upstream of drafting. The conceptual decision tree (Stated → Rule → Scope → Default) is shared between the two; the implementations are independent because the input artefacts differ.
