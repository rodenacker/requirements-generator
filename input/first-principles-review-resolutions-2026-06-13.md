# Review Resolutions — First Principles (review-requirements/FIRST-PRINCIPLES)

<!-- Consultant-approved input document produced by /resolve-review.
     Corpus material: the next source-manifest build ingests this file like any
     other input/ file (Native-text tier). Finding IDs below are per-run labels
     from the source review and reset whenever that review is re-run — the
     verbatim finding quotes are the durable anchors. Where a resolution changes
     a fact stated elsewhere in the corpus, its Supersedes line is authoritative:
     treat the superseded statement as replaced, not contradicted. -->

## Provenance

| Field | Value |
|---|---|
| Source review | `review-requirements/FIRST-PRINCIPLES/first-principles-review.html` |
| Source review sha256 | `ed4a4494eac4695b115c51bcdef02e72f5d1995f3049a3fda038e979ab1b2b21` |
| Review's source fingerprint | `a8c551059a6affd50c20f2d4de43d7bf4d21e5aea9d81e954c56a96d8f3de214` |
| Fingerprint target (`requirements/requirements.md`) at resolution time | `6a97ee682066ce9520f298217bccdcf42f492898c691119701cb5a0c91f39171` |
| Source drift | DRIFT — the review predates the current requirements document |
| Methodology | `first-principles` |
| Resolution date | 2026-06-13 |
| Findings resolved | BR-08, F-16, US-06, US-03, G-03, G-04, EN-01, EN-02, EN-03, BR-06, CS:1, CS:2 |
| Findings skipped | (none) |

<!-- No addendum row: the Step-9b addendum outcome is decided after this document is
     finalised, and recording transient requirements.md state in a durable corpus file
     would mislead after the next re-merge removes the addendum. The pairing is recorded
     on the addendum side (its Run sub-block names this file). -->

**Origin markers:** `[CONSULTANT-STATED]` — the consultant supplied the resolution
content. `[AI-INFERRED, CONSULTANT-CONFIRMED]` — drafted from the review finding's
own actionable payload and individually confirmed by the consultant. Every
resolution below carries exactly one.

## Resolutions

### BR-08 — score 3/6, weakest Q2 — clarify

**Finding (verbatim, from the review):**
> When a File Log is displayed, then its Status is derived from LastExecutedActivityName via an activity-name-to-status mapping

**Problem as stated by the review:** The acceptance criterion has no [SRC] backing and restates the rule ("display the Status mapped from LastExecutedActivityName") without a measurable, testable threshold; §9 also notes the mapping is "not enumerated in the corpus," so the AC is not measurably testable.

**Review's actionable payload:** clarify — Q4 fails: the acceptance criterion restates the rule and the activity-name-to-status mapping is unenumerated (§9), so there is no measurable test.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
BR-08 exists so that every File Log carries a single derived Status computed from its most recent processing activity (the LastExecutedActivityName field) via an activity-name-to-status mapping, so users see one consistent file state rather than raw activity names. That mapping must be enumerated in the corpus — each activity name and the Status it produces — so the derived Status is testable.

**Supersedes:** (supersedes nothing — net-new information)

---

### F-16 — score 3/6, weakest Q2 — clarify

**Finding (verbatim, from the review):**
> Verify session validity and render a welcome on page load

**Problem as stated by the review:** Q2 — "The rationale 'Serves → §3 Importer' points to a persona, not a measurable business goal; no G-NN is named or reachable." Q3 — "No §1/§3 friction is named that session-verification-on-load removes; it states an internal-system property rather than a user pain."

**Review's actionable payload:** clarify — Q2 and Q3 fail: this "Could" requirement names neither a measurable goal nor a stated problem it solves.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
F-16 is a convenience capability at priority Could: on page load the application verifies that the existing session is still valid and greets the authenticated user. It is not tied to a measurable business goal and addresses no stated user pain; it exists to confirm session state and personalise the landing, and may be dropped without affecting any Must or Should outcome.

**Supersedes:** (supersedes nothing — net-new information)

---

### US-06 — score 3/6, weakest Q2 — clarify

**Finding (verbatim, from the review):**
> As an Approver, I want to export the filtered transactions, so that I can use the data elsewhere

**Problem as stated by the review:** Q3 — "The Approver's §3 stated fears are 'Approving or rejecting the wrong transaction' — no stated pain about exporting or using data elsewhere that this story's I want addresses." Q4 — "The so that clause 'so that I can use the data elsewhere' names no measurable operational outcome distinct from the export action; it is hortatory."

**Review's actionable payload:** clarify — Q3 and Q4 fail: the export story names no Approver pain it removes and no measurable outcome beyond "use the data elsewhere."

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
US-06 lets an Approver export the currently filtered transaction set to CSV so the data can be used in tools outside this application, such as spreadsheets or downstream reporting. The exported set mirrors the on-screen filtered set; it is a convenience for downstream use rather than a fix for a stated Approver pain, and carries no measurable target.

**Supersedes:** (supersedes nothing — net-new information)

---

### US-03 — score 3/6, weakest Q2 — clarify

**Finding (verbatim, from the review):**
> As an Importer, I want to search and filter transactions, so that I can review the records of a file

**Problem as stated by the review:** Q3 — "The Importer persona's stated pain concerns ingestion failure, not difficulty finding records, and the linked §5 Search & Filtering flow states no friction the I want resolves." Q4 — "The 'so that I can review the records of a file' clause restates review intent with no measurable outcome distinct from the I want."

**Review's actionable payload:** clarify — Q3 and Q4 fail: no stated Importer pain about locating records and no measurable outcome in the "so that" clause.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
US-03 lets an Importer search and filter the transactions of a file so they can review that file's records — confirming what was ingested and spotting anomalies. It supports review of a file's contents; it is not tied to a measurable target and does not resolve the Importer's stated ingestion-failure pain.

**Supersedes:** (supersedes nothing — net-new information)

---

### G-03 — score 3/6, weakest Q2 — clarify

**Finding (verbatim, from the review):**
> Export the filtered transaction set

**Problem as stated by the review:** Q2 — "The goal text 'Export the filtered transaction set' names no KPI, measurable target, regulatory citation, or outcome verb." Q3 — "No §1 or §3 text names a current friction, manual workload, or complaint that exporting removes; the Approver persona's wants/fears concern review accuracy, not export." Q4 — "The quality signal 'Exported CSV matches the on-screen filtered set' is a correctness property with no time, count, or threshold-bound measure."

**Review's actionable payload:** clarify — Q2/Q3/Q4 fail: the goal names no measurable outcome and no §1/§3 problem that export removes.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
G-03 ("Export the filtered transaction set") is a capability-level goal. Its success criterion is correctness — the exported CSV exactly matches the on-screen filtered set — not a measured business target such as time saved or volume processed. No KPI or regulatory driver is claimed for it.

**Supersedes:** (supersedes nothing — net-new information)

---

### G-04 — score 3/6, weakest Q2 — clarify

**Finding (verbatim, from the review):**
> Find specific transactions quickly via search and filter

**Problem as stated by the review:** Q2 — "The adverb 'quickly' is hortatory; the goal text carries no number, unit, percentage, time, or outcome verb naming a measurable business outcome." Q3 — "No §1 or §3 text names a current friction about locating transactions; the personas' stated pains concern ingestion failure and wrong actioning, not search difficulty." Q4 — "The quality signal 'Target transactions located within a few filter actions' uses 'a few', which is not a count-, time-, or threshold-bound measure."

**Review's actionable payload:** clarify — Q2/Q3/Q4 fail: "quickly" and "a few filter actions" are hortatory, with no measurable target or stated problem.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
G-04 ("Find specific transactions quickly via search and filter") is a capability-level goal aimed at efficient review: users locate target transactions by filtering on status, file, date range, amount range, and free text. Its quality signal ("located within a few filter actions") is directional, not a measured threshold; no numeric target is claimed.

**Supersedes:** (supersedes nothing — net-new information)

---

### EN-01 — score 4/6, weakest Q2 — re-scope

**Finding (verbatim, from the review):**
> Shape: FileLog

**Problem as stated by the review:** IsActive (boolean, hidden, "internal active flag; not displayed") has no §6 requirement that reads, writes, or constrains it — an orphan attribute with no §6 reader.

**Review's actionable payload:** re-scope — Q5 fails: the IsActive attribute has no §6 reader or writer, so the entity is wider than the requirements need.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The FileLog shape's IsActive attribute (a hidden internal active-flag) is out of scope for the frontend: no requirement reads, writes, or displays it. FileLog's frontend-relevant fields are those F-04 surfaces — file name, process date, record count, and status. IsActive may be omitted from the frontend data model.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding the §7/FileLog IsActive attribute.

---

### EN-02 — score 4/6, weakest Q2 — re-scope

**Finding (verbatim, from the review):**
> Shape: Transaction

**Problem as stated by the review:** Description (string, table-col, "included in the displayed model") has no §6 requirement that reads, writes, or constrains it — F-06's column list (reference, date, account, amount, currency, status) omits Description, making it an orphan attribute with no §6 reader.

**Review's actionable payload:** re-scope — Q5 fails: the Description attribute is in the displayed model but no §6 requirement lists it as a column.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The Transaction shape's Description attribute is not part of the frontend transaction table: F-06's column set is reference, date, account, amount, currency, and status, which omits Description. Description may be dropped from the displayed model unless a requirement names it.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding the §7/Transaction Description attribute being in the displayed model.

---

### EN-03 — score 4/6, weakest Q2 — re-scope

**Finding (verbatim, from the review):**
> Shape: User

**Problem as stated by the review:** FirstName (string, detail, "user given name") and LastName (string, detail, "user surname") have no §6 requirement that reads, writes, or constrains them — F-16's "render the authenticated user's welcome" names no specific field, leaving these as orphan attributes with no §6 reader.

**Review's actionable payload:** re-scope — Q5 fails: FirstName and LastName have no §6 reader; the welcome requirement names no field.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The User shape's FirstName and LastName attributes are out of frontend scope as written: no requirement reads or writes them, and F-16's welcome names no field. Unless the welcome surface is specified to display the user's name, FirstName and LastName may be omitted from the frontend data model.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding the §7/User FirstName and LastName attributes.

---

### BR-06 — score 4/6, weakest Q2 — clarify

**Finding (verbatim, from the review):**
> When the user is an Approver, then upload must be hidden

**Problem as stated by the review:** Q2 — "The Source points to §6.5 RBAC, a role-permission anchor, not a measurable business outcome; no upstream G-NN naming a measurable goal is reachable." Q3 — "No §1/§3 friction names a pain that hiding upload from Approvers removes; the Approver persona's fear is about wrong approve/reject decisions, not about seeing an upload control, so the problem link is inferable but not stated."

**Review's actionable payload:** clarify — Q2 and Q3 are partial: the rule lands on the §6.5 RBAC table with no measurable goal and no stated §1/§3 pain.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
BR-06 enforces role-based access: the upload control is hidden from Approvers because uploading is an Importer-only action per the §6.5 RBAC model. Its purpose is correct role separation — keeping Approvers to review-and-action and out of ingestion — not a measurable business target; it has no standalone KPI.

**Supersedes:** (supersedes nothing — net-new information)

---

### CS:1 — Acting user not recorded on transactions

**Finding (verbatim, from the review):**
> §4.1 / G-02: Review and action (approve/reject) transactions accurately [SRC: C-022] | Transactions actioned correctly, with the acting user recorded
> §7 / Transaction: | UserNote | string | no | detail | note captured on rejection [SRC: C-055] |
> §6 / F-09: When a note is supplied, the system shall set status to Rejected and record the note [SRC: C-019].

**Problem as stated by the review:** G-02's quality signal commits to transactions being actioned "with the acting user recorded", but the §7 Transaction shape carries no acting-user field and F-08/F-09 record only the status change and the rejection note.

**Review's actionable payload:** The entity model and the approve/reject requirements as written cannot deliver G-02's "acting user recorded" signal, since no Transaction field or requirement captures who actioned a transaction. (Observational cross-subject finding — the review issues no recommendation; resolution stated by the consultant.)

**Resolution** `[CONSULTANT-STATED]`
Capturing the acting user on a transaction is out of frontend scope: the frontend does not record or display who approved or rejected a transaction, and goal G-02's "with the acting user recorded" signal is not delivered by the frontend.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §4.1/G-02's "actioned correctly, with the acting user recorded" quality signal.

---

### CS:2 — Failed file leaves no user recovery path

**Finding (verbatim, from the review):**
> §1.5: User-facing recovery flow for a Failed file (unspecified, treated as not-yet-defined) [SRC: C-069]
> §2.5 / File Log: | Processing → Failed | backend processing fails (out-of-FE-scope context) | processing encountered an error | File Status reflects Failed on the File Log list; recovery flow unspecified [SRC: C-069] |

**Problem as stated by the review:** The File Log lifecycle includes a Failed terminal state that F-04 surfaces on the file-log list, but §1.5 defers the user-facing recovery flow and §2.5 marks it "recovery flow unspecified".

**Review's actionable payload:** The doc displays a Failed file state but omits any requirement defining the user's next action, leaving a Failed file as a dead-end in the prototype. (Observational cross-subject finding — the review issues no recommendation; resolution stated by the consultant.)

**Resolution** `[CONSULTANT-STATED]`
The user-facing recovery flow for a Failed file is out of frontend scope. A Failed file's status is display-only on the File Log list; the frontend defines no recovery action (such as re-upload or error drill-down) for it.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding §1.5's deferred (not-yet-defined) Failed-file recovery flow.

---

## Findings considered but skipped

(none — every selected finding was resolved)
