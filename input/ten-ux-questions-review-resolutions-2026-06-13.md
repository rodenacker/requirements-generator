# Review Resolutions — 10 UX Questions (review-requirements/TEN-UX-QUESTIONS)

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
| Source review | `review-requirements/TEN-UX-QUESTIONS/ten-ux-questions-review.html` |
| Source review sha256 | `4c99507bb0e1a9ed22e6a1d5fa5f9f177fbbe9f4dd2692d1dbea707ea7f091bb` |
| Review's source fingerprint | `a8c551059a6affd50c20f2d4de43d7bf4d21e5aea9d81e954c56a96d8f3de214` |
| Fingerprint target (`requirements/requirements.md`) at resolution time | `f14f6d78db74e5a86243bc0ceace3be61ffbe3bf63af496e9691079b05d04828` |
| Source drift | DRIFT — the review predates the current requirements document |
| Methodology | `ten-ux-questions` |
| Resolution date | 2026-06-13 |
| Findings resolved | UXQ-01, UXQ-02, UXQ-03, UXQ-04, UXQ-05, UXQ-06, UXQ-07, UXQ-08, UXQ-09, UXQ-10 |
| Findings skipped | (none) |

<!-- No addendum row: the Step-9b addendum outcome is decided after this document is
     finalised, and recording transient requirements.md state in a durable corpus file
     would mislead after the next re-merge removes the addendum. The pairing is recorded
     on the addendum side (its Run sub-block names this file). -->

**Origin markers:** `[CONSULTANT-STATED]` — the consultant supplied the resolution
content. `[AI-INFERRED, CONSULTANT-CONFIRMED]` — drafted from the review finding's
own actionable payload and individually confirmed by the consultant. Every
resolution below carries exactly one.

> **Note on this run.** Every finding in this review is a UX design question whose answer the review could not know; the consultant resolved each by declaring its topic **out of scope for the prototype**. Each decision was taken individually, finding by finding. Because these findings carry no verbatim quote from `requirements/requirements.md` (the finding *is* a question, not a quoted statement), no resolution names a superseded statement — every resolution is net-new scope information.

## Resolutions

### UXQ-01 — Unit of completion for the Approver's review cycle (global queue vs file-scoped)

**Finding (verbatim, from the review):**
> When is an Approver 'done' for a cycle — when every Imported transaction across all files is actioned (a global pending queue), or when every transaction in one file is actioned — given that they land on the global Transaction Table (F-02) but can also drill into a single file (F-05)?

**Problem as stated by the review:** The unit of completion determines whether the Approver's home screen is a global pending queue or a file-scoped review — two structurally different primary surfaces. The designer cannot choose which screen the Approver opens to until this is settled.

**Review's actionable payload:** Elicitation question (C3 Goals & success signals; anchor §4.1) — the finding is itself the question quoted above.

**Resolution** `[CONSULTANT-STATED]`
Out of scope for the prototype: defining a fixed unit of completion for the Approver's review cycle. The prototype need not decide whether an Approver is "done" when every Imported transaction across all files is actioned (a global pending queue) or when every transaction in a single file is actioned; both the global Transaction Table (F-02) and the single-file drill-in (F-05) remain available, with no prescribed completion boundary.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-02 — Bulk (multi-select) actioning vs one transaction at a time

**Finding (verbatim, from the review):**
> Can an Approver approve or reject several transactions in one action (multi-select), or is actioning strictly one transaction at a time, as F-08 and F-09 describe?

**Problem as stated by the review:** Bulk actioning changes the table's core mechanics — row selection, a bulk-action bar, and how the mandatory rejection note (BR-03) applies across many rows — versus a per-row-only design. The two layouts cannot both be the default.

**Review's actionable payload:** Elicitation question (C4 Tasks, flows, decision points; anchor §6.1) — the finding is itself the question quoted above.

**Resolution** `[CONSULTANT-STATED]`
Out of scope for the prototype: bulk (multi-select) approval or rejection of transactions. Actioning remains one transaction at a time; the prototype need not provide row multi-select or a bulk-action bar, and the mandatory rejection note (BR-03) is captured per individual rejection.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-03 — Deadline/cut-off vs at-leisure approval (context of use)

**Finding (verbatim, from the review):**
> Is transaction approval bound by a daily cut-off or service-level deadline (for example, all of a day's imports must be actioned by end of business), or is it an at-leisure task the Approver picks up when convenient?

**Problem as stated by the review:** A deadline-driven task needs aging cues, a pending-count focus, and urgency sorting, whereas an at-leisure task is served by a plain list. The document declares no context of use, so the designer has nothing to default to.

**Review's actionable payload:** Elicitation question (C2 Context of use; anchor missing-section: context-of-use — net-new by construction) — the finding is itself the question quoted above.

**Resolution** `[CONSULTANT-STATED]`
Out of scope for the prototype: any daily cut-off or service-level deadline on transaction approval. Approval is treated as an at-leisure task the Approver picks up when convenient; the prototype need not provide aging cues, urgency sorting, or a deadline/pending-count focus.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-04 — Cross-record context at the moment of decision

**Finding (verbatim, from the review):**
> To judge a transaction, does the Approver need context from related records — other transactions from the same AccountNumber, or the other transactions in the same file — visible at the moment of decision?

**Problem as stated by the review:** A need for cross-record context would add a related-transactions panel or a comparison view that a single-row decision model omits entirely. The document specifies what each transaction stores but not what supports the approve/reject judgement.

**Review's actionable payload:** Elicitation question (C5 Data & content for decisions; anchor §6.4) — the finding is itself the question quoted above.

**Resolution** `[CONSULTANT-STATED]`
Out of scope for the prototype: surfacing context from related records (other transactions sharing an AccountNumber, or other transactions in the same file) at the moment of decision. The approve/reject judgement is supported by the transaction's own fields; no related-transactions panel or comparison view is required.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-05 — Surfacing the acting Approver (G-02 vs the §7 data shape)

**Finding (verbatim, from the review):**
> §4.1 G-02's quality signal says actions are recorded 'with the acting user', yet the §7 Transaction shape carries no actor field and no screen shows who actioned a transaction — where, and whether, is the acting Approver surfaced?

**Problem as stated by the review:** The stated goal cannot be satisfied by the closed §7 property set, so the designer cannot show who actioned a transaction without the consultant resolving whether an actor field exists and where it appears. This is a contradiction between the goal and the data shape, not a styling choice.

**Review's actionable payload:** Elicitation question (C7 Collaboration & concurrency; anchor §4.1) — the finding is itself the question quoted above.

**Resolution** `[CONSULTANT-STATED]`
Out of scope for the prototype: surfacing which Approver actioned a transaction. No screen need display acting-user attribution, and the prototype does not add an actor field to the §7 Transaction shape (which carries none). G-02's recording of actions "with the acting user" is treated as a backend concern that the prototype does not surface.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-06 — A third actioning outcome beyond approve/reject

**Finding (verbatim, from the review):**
> Beyond approve and reject, does an Approver ever need a third outcome — defer, skip, or flag-for-more-information — when they are uncertain about a transaction?

**Problem as stated by the review:** A holding outcome would add a third action and a new lifecycle state, breaking the current two-action Imported → Approved/Rejected model and changing the row's action set. Designing only two actions forecloses an escape hatch the work may require.

**Review's actionable payload:** Elicitation question (C3 Goals & success signals; anchor §2.3) — the finding is itself the question quoted above.

**Resolution** `[CONSULTANT-STATED]`
Out of scope for the prototype: any third actioning outcome beyond approve and reject (such as defer, skip, or flag-for-more-information). The two-action Imported → Approved/Rejected model stands; no holding state or third action is required.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-07 — Default status filter on the Transaction Table

**Finding (verbatim, from the review):**
> When an Approver lands on the Transaction Table (F-02), is it pre-filtered to actionable (Imported) transactions, or does it show all statuses by default?

**Problem as stated by the review:** The default filter on the Approver's primary screen decides whether they open straight into a focused work-queue or an everything-list they must narrow first. It sets the initial state of the most-used surface.

**Review's actionable payload:** Elicitation question (C4 Tasks, flows, decision points; anchor §5) — the finding is itself the question quoted above.

**Resolution** `[CONSULTANT-STATED]`
Out of scope for the prototype: prescribing, as a binding requirement, the default status filter shown when the Approver lands on the Transaction Table (F-02). Whether F-02 opens pre-filtered to actionable (Imported) transactions or shows all statuses is left to design discretion rather than fixed by requirement.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-08 — A transaction detail view reached from a row

**Finding (verbatim, from the review):**
> Is there a transaction detail view reached by selecting a row — the §7 UserNote and Description fields are marked for 'detail' display — or are all fields shown inline in the table, with no detail surface at all?

**Problem as stated by the review:** §7 implies a detail surface that no task flow or UI feature need defines, leaving its existence unresolved. Whether a row opens a detail view changes the navigation model and what selecting a row does.

**Review's actionable payload:** Elicitation question (C4 Tasks, flows, decision points; anchor §7) — the finding is itself the question quoted above.

**Resolution** `[CONSULTANT-STATED]`
Out of scope for the prototype: mandating a dedicated transaction detail view reached by selecting a row. The §7 UserNote and Description fields marked for "detail" display do not require a separate detail surface; whether and how to present them is left to design discretion rather than fixed by requirement.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-09 — The decision-supporting field set vs displayed columns

**Finding (verbatim, from the review):**
> At the approve/reject moment, which fields does the Approver actually need to see to decide — the six columns in F-06 (reference, date, account, amount, currency, status), or also Description, the rejection note, and the originating file?

**Problem as stated by the review:** The decision-supporting field set determines what the confirmation step and any detail view must surface beyond the default columns. F-06 lists what is displayed, but not what the decision requires, and the two may differ.

**Review's actionable payload:** Elicitation question (C5 Data & content for decisions; anchor §6.4) — the finding is itself the question quoted above.

**Resolution** `[CONSULTANT-STATED]`
Out of scope for the prototype: specifying a decision-support field set distinct from the displayed columns. The fields available for the approve/reject decision are those listed in F-06 (reference, date, account, amount, currency, status); the prototype need not surface additional decision-only fields (Description, the rejection note, or the originating file) beyond what F-06 defines.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-10 — Live vs manual-refresh status on the File Log Overview

**Finding (verbatim, from the review):**
> On the File Log Overview, does the list reflect status progression (Uploaded → Processing → Completed/Failed) live as it changes, or must the Importer manually refresh to see a file leave Processing?

**Problem as stated by the review:** A live-updating list needs an auto-refreshing surface with an in-progress indicator, while a manual model needs a refresh control and a staleness cue — different interaction designs for the same screen. The document is silent on how the Importer learns that processing has finished.

**Review's actionable payload:** Elicitation question (C6 Errors, edge cases, recovery; anchor §5) — the finding is itself the question quoted above.

**Resolution** `[CONSULTANT-STATED]`
Out of scope for the prototype: live (auto-refreshing) status progression on the File Log Overview. The prototype need not update files automatically as they move Uploaded → Processing → Completed/Failed; a manual-refresh model is acceptable and real-time updating is not required.

**Supersedes:** (supersedes nothing — net-new information)

---

## Findings considered but skipped

(none — every selected finding was resolved)
