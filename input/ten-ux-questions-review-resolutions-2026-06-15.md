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
| Source review sha256 | `1755be3cd4e0a02164398960808a98a6778155264e5b056abaeb202df1e4cab7` |
| Review's source fingerprint | `88eb974feca6569e8aae57ab9e112ecd3da89a60897c1f7d2758d10d5e431b98` |
| Fingerprint target (`requirements/requirements.md`) at resolution time | `9ad6c62cab01b3a22430a172e4172c59564252e29102fb4d5c567d36b8daaf78` |
| Source drift | DRIFT — the review predates the current requirements document |
| Methodology | `ten-ux-questions` |
| Resolution date | 2026-06-15 |
| Findings resolved | UXQ-01, UXQ-02, UXQ-03, UXQ-04, UXQ-05, UXQ-06, UXQ-07, UXQ-08, UXQ-09, UXQ-10 |
| Findings skipped | (none) |

<!-- No addendum row: the Step-9b addendum outcome is decided after this document is
     finalised, and recording transient requirements.md state in a durable corpus file
     would mislead after the next re-merge removes the addendum. The pairing is recorded
     on the addendum side (its Run sub-block names this file). -->

**Origin markers:** `[CONSULTANT-STATED]` — the consultant supplied the resolution
content. `[AI-INFERRED, CONSULTANT-CONFIRMED]` — drafted by the resolver from the
review finding's own actionable payload, or (for gap-surfacing question findings) from
the resolver's domain reasoning, and explicitly confirmed by the consultant (per
finding, or — confirmation-type flows only — via an explicit "Accept all remaining as
drafted" choice). Every resolution below carries exactly one. Resolutions drafted to
close an elicited gap also carry a **grounding tag** on their Grounding line.

## Resolutions

### UXQ-01 — When an Approver rejects a transaction, is the mandatory note captured inline on the row, inside the…

**Finding (verbatim, from the review):**
> When an Approver rejects a transaction, is the mandatory note captured inline on the row, inside the approve/reject confirmation step, or on a separate screen — and does the same containment apply to the approve confirmation?

**Problem as stated by the review:** §5 Reject Transaction says a note field is presented and GR-04 already puts approve/reject behind a confirmation, but where the note is entered shapes the whole reject interaction — an inline cell, a field inside the confirmation dialog, and a dedicated step are three different layouts. The designer must settle this before sketching the table's primary action.

**Review's actionable payload:** Gap-surfacing elicitation question (category C4 Tasks, flows, decision points; anchor `§5`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
When an Approver rejects a transaction, the mandatory note is captured inside the approve/reject confirmation dialog — the confirmation gate GR-04 already requires. Rejecting opens that dialog with the mandatory note field, and the Approver enters the note and confirms in a single modal step; approve uses the same confirmation dialog with no note field. The note is not captured inline on the row or on a separate screen.

**Grounding:** [grounded: §5] — realizes §5's "a note field is presented" within GR-04's existing confirmation gate; commits both actions to one confirmation-modal pattern, with reject adding a required-note field.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-02 — How does an Approver learn that new Imported transactions are waiting to be reviewed — a notification…

**Finding (verbatim, from the review):**
> How does an Approver learn that new Imported transactions are waiting to be reviewed — a notification, a badge, a manual refresh, or simply re-opening the table — given §6.8 notifies on action results but not on new arrivals?

**Problem as stated by the review:** §6.8 defines notifications for upload and action results, and AMD-75 makes File Log status manual-refresh, but nothing says how the Approver discovers that fresh transactions need attention. The answer decides whether the design needs a new-items notification or badge, a refresh affordance, or nothing at all.

**Review's actionable payload:** Gap-surfacing elicitation question (category C7 Collaboration & concurrency; anchor `§6.8`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
An Approver discovers that new Imported transactions are waiting by opening or manually refreshing the Transaction Table. The system provides a visible manual-refresh control but no push notification, badge, or auto-updating count for new arrivals; the manual-refresh model already adopted for the File Log Overview extends to the Transaction Table.

**Grounding:** [grounded: AMD-75] — applies AMD-75's manual-refresh decision to the Transaction Table; commits the build to a refresh control and no real-time or notification infrastructure.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-03 — The File Log Overview and the Transaction Table are shared by both Importer and Approver (§5) — which…

**Finding (verbatim, from the review):**
> The File Log Overview and the Transaction Table are shared by both Importer and Approver (§5) — which role is the primary user that each shared screen should optimise its default layout and density for?

**Problem as stated by the review:** §5 marks both screens as shared but names no primary user, and the two roles approach them differently — an Importer confirming ingestion versus an Approver working a review queue. The default column set, density, and emphasis differ by which role the screen is tuned for.

**Review's actionable payload:** Gap-surfacing elicitation question (category C1 Users & segmentation; anchor `§5`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Each shared screen is tuned to the role whose core task it serves: the File Log Overview defaults to the Importer's ingestion-confirmation needs, and the Transaction Table defaults to the Approver's review-queue needs. There is no single global primary user across both screens; the default column set, density, and emphasis on each screen follow that screen's dominant §3 task.

**Grounding:** [grounded: §3] — maps each shared screen to the persona whose driving §3 task it carries; commits the build to two per-screen default layouts and no per-role view branching.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-04 — How many transactions does a typical Approver review in one sitting, and how often — several times a…

**Finding (verbatim, from the review):**
> How many transactions does a typical Approver review in one sitting, and how often — several times a day or once a cycle — so the table density and at-a-glance layout can be tuned to the real working volume?

**Problem as stated by the review:** §3 describes the Approver as reviewing pending transactions per cycle without a volume or cadence, and §10 gives an overall band rather than a per-session figure. A high-volume several-times-a-day reviewer needs a dense, keyboard-fast table; an occasional reviewer needs more context per row.

**Review's actionable payload:** Gap-surfacing elicitation question (category C1 Users & segmentation; anchor `§3`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The Transaction Table's density and at-a-glance layout are tuned to the ~1,000-row planning working-set already adopted (the §10 / AMD-16 figure), using pagination and virtualization rather than a fixed per-session volume. The typical Approver's per-session transaction count and review cadence are not specified and are recorded as an open assumption to confirm with the client; approval remains an at-leisure task (per AMD-68).

**Grounding:** [grounded: AMD-16] — rests density on the already-adopted ~1,000-row planning working-set; commits the build to pagination/virtualization sized to that figure, with per-session volume left an explicit unknown.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-05 — If an Approver starts rejecting a transaction, types part of the mandatory note, then navigates away…

**Finding (verbatim, from the review):**
> If an Approver starts rejecting a transaction, types part of the mandatory note, then navigates away and returns, is the in-progress note preserved or discarded?

**Problem as stated by the review:** §5 Reject Transaction treats the note as a single submit step and says nothing about an interrupted rejection. Whether the design must preserve a draft note (and signal that it did) versus discarding it changes the reject control and the user's confidence in leaving a row mid-action.

**Review's actionable payload:** Gap-surfacing elicitation question (category C4 Tasks, flows, decision points; anchor `§5`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[CONSULTANT-STATED]`
An in-progress rejection note is discarded when the Approver navigates away from the reject interaction, with no warning prompt and no draft preservation; re-opening reject starts with a blank note.

**Grounding:** [assumption — confirm with client] — commits the build to silently discarding an unsaved mandatory rejection note on navigation; because the note is compliance-relevant, the absence of an unsaved-changes warning carries a silent-loss risk that should be validated with the client.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-06 — When a user drills from a File Log row into that file's transactions (F-05) versus opening the…

**Finding (verbatim, from the review):**
> When a user drills from a File Log row into that file's transactions (F-05) versus opening the global Transaction Table (F-02), how does the screen show which scope is active, and how does the user return to the full set?

**Problem as stated by the review:** §6.1 F-05 allows drilling into one file's transactions while F-02/F-06 present the global table, but the document never says how the two views are visually distinguished or navigated between. Without a scope cue and a way back, a user cannot tell whether they are seeing one file or all transactions.

**Review's actionable payload:** Gap-surfacing elicitation question (category C4 Tasks, flows, decision points; anchor `§6.1`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
When the Transaction Table is scoped to a single file (drilled into via F-05), the screen shows a persistent scope indicator naming the file (for example "Showing: <FileName>") and a one-click control to return to the global transaction set (F-02); the global view shows no scope indicator. Both the file-scoped and global views remain available (per AMD-66).

**Grounding:** [domain-default] — a persistent scope banner plus an explicit return control is the conventional master-detail drill pattern; commits the build to a file-scope indicator and a clear-scope/return affordance on the table.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-07 — Immediately after an Approver approves or rejects a transaction, does the row remain visible in the…

**Finding (verbatim, from the review):**
> Immediately after an Approver approves or rejects a transaction, does the row remain visible in the current view with its new status, or leave the view — and does that depend on the active filter?

**Problem as stated by the review:** §2.5 says the status chip changes and the approve/reject actions are removed, but not whether the row stays in the list or disappears. If the table is showing only Imported transactions the actioned row would vanish, which can feel like data loss; if it shows all statuses the row stays — a materially different post-action experience the designer must choose.

**Review's actionable payload:** Gap-surfacing elicitation question (category C4 Tasks, flows, decision points; anchor `§2.5`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Immediately after an Approver approves or rejects a transaction, the row updates in place — its status chip changes and the approve/reject actions are removed (per §2.5) — and it remains visible if it still matches the active filter. If the active filter excludes the new status (for example a filter showing only Imported transactions), the row leaves the view on the next re-filter, and the existing action-result notification (NT-02) confirms the action so its disappearance is not read as data loss. Post-action row visibility therefore depends on the active filter.

**Grounding:** [grounded: §2.5] — realizes §2.5's chip-change-and-action-removal as an in-place update governed by the active filter; commits the build to filter-driven post-action visibility plus the NT-02 action-result toast.

**Supersedes:** (supersedes nothing — net-new information)

---

### UXQ-08 — Where should the Transaction fields not in the F-06 column set — TransactionType (Credit/Debit),…

**Finding (verbatim, from the review):**
> Where should the Transaction fields not in the F-06 column set — TransactionType (Credit/Debit), Description, and UserNote — be surfaced, given AMD-73 leaves a dedicated detail view to design discretion?

**Problem as stated by the review:** §7 marks TransactionType as a chip, Description as a table column, and UserNote as detail, and AMD-04 places them in a detail view, yet AMD-73 says no detail view is mandated. The designer needs to know whether these three fields appear as extra columns, an expandable row, a side panel, or are omitted from the main surface.

**Review's actionable payload:** Gap-surfacing elicitation question (category C5 Data & content for decisions; anchor `§7`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The Transaction fields outside the F-06 column set — TransactionType, Description, and UserNote — are surfaced via an expandable disclosure row on the Transaction Table: the main row keeps the F-06 columns (reference, date, account, amount, currency, status), and expanding the row reveals TransactionType, Description, and UserNote inline. No separate transaction detail view or screen is required; every Transaction field thus has a defined read location without a dedicated detail surface.

**Grounding:** [grounded: AMD-73] — uses the design discretion AMD-73 grants (no mandated detail view) to place the non-column fields in an inline expandable row; commits the build to an expand-row interaction carrying TransactionType, Description, and UserNote.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding AMD-04 (the placement of TransactionType, Description, and UserNote in a per-transaction detail view) — they are now surfaced in an inline expandable row rather than a separate detail view.

---

### UXQ-09 — When a transaction has been Rejected, can a user later see the rejection note that was captured, and…

**Finding (verbatim, from the review):**
> When a transaction has been Rejected, can a user later see the rejection note that was captured, and where — so the reason a transaction was rejected is visible after the fact?

**Problem as stated by the review:** §7 stores UserNote as detail-display and §6.2 BR-03 captures it at rejection, but nothing says the note is shown when reviewing a Rejected transaction afterwards. Whether the rejection reason is visible (and where) determines whether the system can answer the user's why-was-this-rejected question or strands the note as write-only data.

**Review's actionable payload:** Gap-surfacing elicitation question (category C8 Trust, transparency, audit; anchor `§7`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[CONSULTANT-STATED]`
Completed transactions carry a "view" link in the Transaction Table that opens a modal showing the action's audit detail. For a Rejected transaction the modal shows the rejecting user, the action date and time, and the rejection note (UserNote). For an Approved transaction the modal shows the approving user, the action date and time, and the other pertinent action detail. This makes the rejection reason — and the approval provenance — retrievable after the fact.

This resolution requires action-attribution data the §7 Transaction shape does not currently carry: the acting user and the action date-time for approve and reject. These are PROPOSED ADDITIONS to the Transaction data shape (an acting-user reference and an action timestamp), to be confirmed before the closed property set is treated as extended; UserNote already exists in §7. The data must be supplied by the backend.

**Grounding:** [assumption — confirm with client] — commits the build to a per-transaction action-audit modal reached from a "view" link, and to new acting-user and action-timestamp data on the Transaction shape; it reverses the prior decisions that acting-user attribution is out of frontend scope and depends on the backend supplying the actor and timestamp.

**Supersedes:** This supersedes the statements in `requirements/requirements.md` regarding AMD-64 and AMD-70 (that capturing and surfacing the acting user is out of frontend scope, and that no actor field is added to the §7 Transaction shape) — the frontend now displays the acting user and action time for completed transactions in a view modal.

---

### UXQ-10 — While a file is uploading (F-03), what does progress look like for a large file, and can the Importer…

**Finding (verbatim, from the review):**
> While a file is uploading (F-03), what does progress look like for a large file, and can the Importer cancel an in-progress upload before it completes?

**Problem as stated by the review:** §6.1 F-03 and UI-01 promise upload progress and a result but do not say whether the progress is determinate or whether a long upload can be cancelled. The answer tunes the upload control but does not reshape the screen, so it is a refinement-level decision.

**Review's actionable payload:** Gap-surfacing elicitation question (category C6 Errors, edge cases, recovery; anchor `§6.1`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
While a file is uploading (F-03), the upload shows a determinate progress bar (the percentage of the file sent) for large files, and the Importer can cancel an in-progress upload via a cancel control; cancelling aborts the upload and returns to the pre-upload state with no File Log created. Upload progress is determinate and cancellable.

**Grounding:** [domain-default] — a determinate progress bar with a cancel affordance is the standard large-file upload pattern; commits the build to a determinate progress indicator and a clean abort path (simulated per PI-01).

**Supersedes:** (supersedes nothing — net-new information)

---

## Findings considered but skipped

(none — every selected finding was resolved)
