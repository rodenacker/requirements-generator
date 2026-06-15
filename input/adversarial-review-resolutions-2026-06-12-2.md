# Review Resolutions — Adversarial Review (ADVERSARIAL)

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
| Source review | `review-inputs/ADVERSARIAL/adversarial-review.html` |
| Source review sha256 | `a9a864434c27827fc41e9c68eeb46a04a1490468cbf410fe8a946bbfe8b0fa0d` |
| Review's source fingerprint | `bb6d87d7c4246dfb1ae732afdf6fe9f29b57b22aa2bcf3610b2c9eb316e34d14` |
| Fingerprint target (`requirements/source-manifest.json`) at resolution time | `bb6d87d7c4246dfb1ae732afdf6fe9f29b57b22aa2bcf3610b2c9eb316e34d14` |
| Source drift | none |
| Methodology | `adversarial` |
| Resolution date | 2026-06-12 |
| Findings resolved | ADV-01, ADV-02, ADV-03, ADV-04, ADV-05, ADV-06, ADV-07, ADV-08, ADV-09, ADV-10, ADV-11, ADV-12, ADV-13, ADV-14, ADV-15, ADV-16, ADV-17, ADV-18, ADV-19, ADV-20, ADV-21, ADV-22, ADV-23, ADV-24, ADV-25, ADV-26, ADV-27, ADV-28, ADV-29, ADV-30, ADV-31, ADV-32, ADV-33, ADV-34, ADV-35, ADV-36 |
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

### ADV-01 — An entire user/role-administration persona is exposed by the API but absent from the corpus voice.

**Finding (verbatim, from the review):**
> ```
>   /v1/users:
>     get:
>       tags:
>         - Users
>       operationId: UserGetList
> ```

**Problem as stated by the review:** The corpus exposes full user/role/page administration endpoints (e.g. UserCreate, RoleCreate, RoleDelete) but names no admin or power-user persona anywhere to perform them, leaving an entire role category unsupported by corpus voice.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream marks the user/role-administration persona as unsupported by corpus voice and applies an [OUT-OF-SCOPE: domain-default]." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
User and role administration — creating, updating, or deleting users and roles — is out of frontend scope for the MVP. The corpus names no admin or power-user persona to perform these operations, so no administration screens are built unless added later.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-02 — An audit-trail actor is recorded everywhere, but no auditor/compliance persona exists in the corpus.

**Finding (verbatim, from the review):**
> ```
>         - name: LastChangedUser
>           in: header
>           description: Name of user performing the action
> ```

**Problem as stated by the review:** Every mutating endpoint records a LastChangedUser actor for accountability, yet no auditor or compliance persona is named anywhere in the corpus to govern or consume that audit trail, leaving the auditor/compliance role category a coverage silence.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream marks auditor/compliance-specific acceptance criteria as unsupported by corpus voice." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
No auditor or compliance persona is in scope. Although every mutating operation records the acting user (LastChangedUser), the corpus defines no audit-review surface, so auditor- or compliance-specific behaviour and acceptance criteria are out of scope.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-03 — The API's only role example ('Viewer') risks being mistaken for an authoritative role vocabulary.

**Finding (verbatim, from the review):**
> ```
>         RolesString:
>           type: string
>           example: 'Viewer'
> ```

**Problem as stated by the review:** The auth API presents 'Viewer' as its only role example with no first-hand role material, which could be mis-read as an authoritative role vocabulary conflicting with the brief's Importer/Approver model if left unannotated.

**Review's actionable payload:** Recommendation — "Label / annotate — mark the API's 'Viewer' role examples as illustrative placeholders (per the consultant-confirmed resolution), not an authoritative role list." · Disposition: Patch · Scope: fe-facing-contract.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The auth API's 'Viewer' role example is an illustrative placeholder only, not an authoritative role list. The authoritative user roles are the brief's Importer and Approver.

**Supersedes:** This supersedes the statement in `auth-api.yaml` regarding the 'Viewer' role example being read as an authoritative role vocabulary.

---

### ADV-04 — A whole file-validation-error subsystem in the API has no UI counterpart in the brief.

**Finding (verbatim, from the review):**
> ```
>       summary: Get invalid rows for a specific file as a single JSON array
> ```

**Problem as stated by the review:** The API exposes a full file-validation-error subsystem (validation-errors, validation-errors/columns, retry-validation, bulk-errors/download) that the brief's §5 workflows never surface as any UI, so whether validation-error review is a frontend surface is left entirely to silence.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream marks the validation-error-review workflow as out-of-corpus-scope unless surfaced at draft time. _(Downgraded from Blocker / Reject in the Revise loop: a coverage silence / scope question, not an in-corpus contradiction.)_" · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Review of file-validation errors is out of frontend scope for the MVP. The API's validation-error subsystem (the validation-errors, validation-errors/columns, retry-validation, and bulk-errors/download endpoints) has no UI in this corpus and will not be surfaced unless explicitly added.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-05 — Concurrent action on the same transaction by two Approvers is undefined.

**Finding (verbatim, from the review):**
> ```
> 1. Select transaction
> 2. Click approve
> 3. Confirm action
> 4. Status updates to Approved
> ```

**Problem as stated by the review:** The Approve/Reject flows describe no behaviour when two Approvers act on the same transaction concurrently, leaving the UI's handling of a stale or already-actioned transaction undefined.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream applies a default stale-action guard and marks concurrent-edit behaviour as not specified by the corpus." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
When two Approvers act on the same transaction at the same time, the UI applies a stale-action guard: a transaction that has already been actioned cannot be actioned again, and the second user is shown that its status has changed. Concurrent-edit behaviour beyond this guard is not specified by the corpus.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-06 — Named table filters have no server-side parameters; client- vs server-side filtering is unstated.

**Finding (verbatim, from the review):**
> ```
>       operationId: TransactionGetList
>       summary: Get a list of all transactions
>       description: Get a list of all transactions with their status
> ```

**Problem as stated by the review:** Workflow 5.5 names Status/File/Date/Amount/text filters on the transactions table, but the only transactions endpoint returns the full list with no filter or pagination parameters, leaving whether filtering is client- or server-side unstated.

**Review's actionable payload:** Recommendation — "Resolve at draft time — surface client- vs server-side filtering/pagination to the consultant-answers loop (the corpus leans client-side: the export resolution generates CSV from the filtered grid). _(Downgraded from Reject in the Revise loop: resolvable at draft time, not an unresolvable contradiction.)_" · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Transaction-table filtering (by Status, File, Date, Amount, and free text) is performed client-side over the full list returned by the transactions endpoint, and CSV export is generated from the filtered grid. Server-side filter or pagination parameters are not required of the API.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-07 — Whether a terminal Approved/Rejected status can be reversed is silent.

**Finding (verbatim, from the review):**
> ```
> Disable approve/reject if not “Imported”
> ```

**Problem as stated by the review:** Beyond disabling approve/reject when status is not Imported, the corpus is silent on whether a terminal Approved/Rejected transaction can be re-actioned or reversed.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream defaults terminal statuses to immutable and marks reversal as unspecified." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Terminal transaction statuses (Approved and Rejected) are immutable: once a transaction is approved or rejected it cannot be re-actioned or reversed in the UI. Reversal of a terminal status is not provided.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-08 — Bulk-error file fields exist on FileLog with no flow describing their UI.

**Finding (verbatim, from the review):**
> ```
>         HasBulkErrorFile:
>           type: string
> ```

**Problem as stated by the review:** The FileLog entity carries HasBulkErrorFile / BulkErrorFile fields with no workflow describing how the UI exposes or acts on a bulk-error download, leaving that touch-point ungrounded as a flow.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream marks the bulk-error-file flow as unspecified by the corpus." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The bulk-error file flow (the FileLog HasBulkErrorFile and BulkErrorFile fields) has no defined UI in the corpus and is out of scope for the MVP unless added later.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-09 — The import sample has no malformed-row or empty-file fixture for the upload non-happy path.

**Finding (verbatim, from the review):**
> ```
> Reference,TransactionDate,AccountNumber,Description,Amount,TransactionType,Currency
> ```

**Problem as stated by the review:** The sole import sample is 20 clean rows with no empty-file or malformed-row example, so the upload workflow's non-happy path (validation failure / partial import) has no grounding fixture in the corpus.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream synthesises validation-error fixtures and marks malformed-import behaviour as unspecified." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The corpus provides no malformed-row or empty-file import fixture, so the upload workflow's non-happy path (validation failure or partial import) is unspecified. Validation-error fixtures may be synthesised for the prototype, and malformed-import behaviour is treated as not defined by the corpus.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-10 — "instantly" sets a user-visible refresh expectation with no latency budget.

**Finding (verbatim, from the review):**
> ```
> Reflect status changes instantly
> ```

**Problem as stated by the review:** "instantly" sets a user-visible refresh expectation with no latency budget the UI must meet.

**Review's actionable payload:** Recommendation — "Resolve at draft time — surface a concrete refresh-latency target to the consultant-answers loop." · Disposition: Defer · Scope: fe-facing-contract.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
After an Approve or Reject action completes, the transaction's new status appears in the UI within about one second (a perceived-instant refresh budget).

**Supersedes:** This supersedes the statement in `BriefV2.md` regarding the unquantified "reflect status changes instantly" expectation.

---

### ADV-11 — The activity-name-to-file-status mapping is undefined.

**Finding (verbatim, from the review):**
> ```
> `LastExecutedActivityName` (To be used as status of file)
> ```

**Problem as stated by the review:** The mapping from activity names to file statuses is undefined, so the file Status field cannot be derived unambiguously.

**Review's actionable payload:** Recommendation — "Resolve at draft time — enumerate the activity-name-to-status mapping in the consultant-answers loop." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The file Status is derived from the LastExecutedActivityName field via an explicit mapping from activity names to the file-status set. The corpus does not enumerate this mapping; it must be supplied before file Status can be displayed unambiguously.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-12 — The file-state model is flagged "inferred" — unconfirmed, not authoritative.

**Finding (verbatim, from the review):**
> ```
> ### File States (inferred)
> ```

**Problem as stated by the review:** The word "inferred" signals the file-state model (Uploaded/Processing/Completed/Failed) is an unconfirmed inference rather than an authoritative state set.

**Review's actionable payload:** Recommendation — "Treat as second-hand — downstream marks the file-state set as inferred (to confirm), consistent with the consultant-approved resolution, not authoritative." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The file-state set (Uploaded, Processing, Completed, Failed) is an inferred, provisional model rather than an authoritative state set, and is treated as to-be-confirmed.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-13 — "Status shown in UI" leaves which status, surface, and form unspecified.

**Finding (verbatim, from the review):**
> ```
> 5. Status shown in UI
> ```

**Problem as stated by the review:** "Status shown in UI" does not specify which status, on which surface, or in what form (chip / column / badge).

**Review's actionable payload:** Recommendation — "Resolve at draft time — the presentation is a how-decision the drafter defaults and the consultant confirms." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Transaction status is shown in the UI as a status chip — in the transaction table as a Status column and in the transaction detail/action view — and file status is shown on the File Log list. The exact presentation is a design (how) decision.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-14 — The verb "reflect" is vague about display vs enforce vs mirror.

**Finding (verbatim, from the review):**
> ```
> The system must reflect:
> ```

**Problem as stated by the review:** The verb "reflect" is vague about whether the FE displays, enforces, or merely mirrors file ingestion, lifecycle states, and role constraints.

**Review's actionable payload:** Recommendation — "Treat as silence — the drafter defaults "reflect" to display/surface for a read-oriented data-management UI." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Where the brief says the system must "reflect" file ingestion, lifecycle states, and role constraints, this means the frontend displays and surfaces them (it is read-oriented); it does not mean the frontend enforces them.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-15 — "the system" never distinguishes current backend from future frontend.

**Finding (verbatim, from the review):**
> ```
> 4. System creates FileLog
> ```

**Problem as stated by the review:** "the system" is used throughout without distinguishing the current backend from the future frontend, an unclear antecedent for FE-scope decisions.

**Review's actionable payload:** Recommendation — "Label / annotate — tag backend-owned "system" steps as out-of-FE-scope context." · Disposition: Patch · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
References to "the system" performing steps such as file ingestion and FileLog creation denote the existing backend, not the frontend being built; such steps are out-of-frontend-scope context.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-16 — "attempt to fix data" is a vague backend mechanism with no defined outcome.

**Finding (verbatim, from the review):**
> ```
> Retry validation for a file and attempt to fix data
> ```

**Problem as stated by the review:** "attempt to fix data" describes a vague backend mechanism with no defined outcome the UI can reflect.

**Review's actionable payload:** Recommendation — "Treat as second-hand — the FE only triggers this, so downstream treats it as an opaque retry action." · Disposition: Defer · Scope: fe-facing-contract.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The backend's "attempt to fix data" retry-validation step is an opaque action from the frontend's point of view: the UI only triggers a retry and reflects its result; it does not define or display how the data is fixed.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-17 — "stadium" appears to be a garbled term in a column-definitions endpoint.

**Finding (verbatim, from the review):**
> ```
> Get stadium column definitions for a specific table
> ```

**Problem as stated by the review:** "stadium" is an apparently garbled/erroneous term in the endpoint description, leaving the column-definition endpoint's intent unclear.

**Review's actionable payload:** Recommendation — "Label / annotate — flag "stadium" as a likely typo and read the endpoint as "column definitions" only." · Disposition: Patch · Scope: fe-facing-contract.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The term "stadium" in the column-definitions endpoint description is a typo; the endpoint is read as returning column definitions for a specific table.

**Supersedes:** This supersedes the statement in `transactions-api.yaml` regarding the garbled "stadium column definitions" wording.

---

### ADV-18 — Post-login routing is deferred to the FE without a stated role-landing rule.

**Finding (verbatim, from the review):**
> ```
> The frontend decides where to navigate next
> ```

**Problem as stated by the review:** Post-login routing is deferred to the frontend without stating the role-specific landing rule, leaving the destination ambiguous.

**Review's actionable payload:** Recommendation — "Resolve at draft time — map each role (Importer / Approver) to its landing surface in the consultant-answers loop." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
After login, the frontend routes each role to its primary landing surface: Importers land on the File Upload / File Log area, and Approvers land on the Transaction Table.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-19 — The brief is anonymous and unversioned.

**Finding (verbatim, from the review):**
> ```
> # Brief: Transaction Import & Approval System
> ```

**Problem as stated by the review:** BriefV2.md opens with no author, date, or version stamp, making it an anonymous, unversioned source whose claims cannot be attributed to an origin.

**Review's actionable payload:** Recommendation — "Label / annotate — add a provenance header (author/date/version) so the brief's claims are attributable and its precedence against the API specs is auditable." · Disposition: Patch · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
BriefV2.md is treated as the consultant-supplied product brief. Absent an explicit author, date, or version stamp, its claims are attributed to the consultant, and where it conflicts with the API specs on intended behaviour the brief takes precedence.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-20 — The SessionCookie description cites a phantom /ping endpoint and the wrong path prefix.

**Finding (verbatim, from the review):**
> ```
> Required by /auth/logout, /auth/userinfo, and /ping.
> ```

**Problem as stated by the review:** The SessionCookie description references a non-existent /ping endpoint (the real probe is GET /v1/health) and drops the /v1 prefix used everywhere else, so the documented session scope contradicts the actual API surface.

**Review's actionable payload:** Recommendation — "Label / annotate — correct the SessionCookie description to /v1/auth/logout, /v1/auth/userinfo and the real /v1/health probe, removing the phantom /ping reference." · Disposition: Patch · Scope: fe-facing-contract.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The session cookie is required by /v1/auth/logout, /v1/auth/userinfo, and the real /v1/health probe. The SessionCookie description's reference to a non-existent /ping endpoint and its dropped /v1 prefix are errors and do not describe the actual API surface.

**Supersedes:** This supersedes the statement in `transactions-api.yaml` regarding the SessionCookie being required by "/auth/logout, /auth/userinfo, and /ping".

---

### ADV-21 — TransactionDate format diverges between the CSV and the API example.

**Finding (verbatim, from the review):**
> ```
> TXN-20260415-0002,2026/04/15 08:34,1001-2034-5567,Woolworths Sandton,487.32,D,ZAR
> ```

**Problem as stated by the review:** TransactionDate is slash-formatted "2026/04/15 08:34" in the CSV but dash-formatted "2025-04-30 15:00:00" in the transactions-api.yaml TransactionRead example, an unreconciled date-format divergence on a UI-displayed field.

**Review's actionable payload:** Recommendation — "Resolve at draft time — declare one canonical TransactionDate display/parse format and treat the divergent source format as ingest-normalisation input." · Disposition: Defer · Scope: fe-facing-contract.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
TransactionDate is displayed and parsed in a single canonical format — YYYY-MM-DD HH:mm, matching the API's dash-formatted example — and the slash-formatted values in the CSV are treated as ingest input to be normalised, not as a display format.

**Supersedes:** This supersedes the statement in `transactions_2026-04-15.csv` regarding the slash-formatted TransactionDate being a display format.

---

### ADV-22 — AccountNumber format diverges between the CSV and the API example.

**Finding (verbatim, from the review):**
> ```
> TXN-20260415-0002,2026/04/15 08:34,1001-2034-5567,Woolworths Sandton,487.32,D,ZAR
> ```

**Problem as stated by the review:** AccountNumber is hyphen-grouped "1001-2034-5567" in the CSV but plain digits "1234567890" in the transactions-api.yaml TransactionRead example, an unreconciled format divergence on a UI-displayed field.

**Review's actionable payload:** Recommendation — "Resolve at draft time — fix a canonical AccountNumber representation and treat the hyphenated CSV form as a presentation/ingest variant." · Disposition: Defer · Scope: fe-facing-contract.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
AccountNumber has one canonical representation in the UI — plain digits, matching the API example — and the hyphen-grouped form in the CSV is treated as a presentation/ingest variant to be normalised on import. (On-screen masking of AccountNumber is governed by the resolution to ADV-28.)

**Supersedes:** This supersedes the statement in `transactions_2026-04-15.csv` regarding the hyphen-grouped AccountNumber being a canonical format.

---

### ADV-23 — The brief's Transaction model omits fields the CSV and API both carry.

**Finding (verbatim, from the review):**
> ```
> - `Status` (Imported / Approved / Rejected)
> - `UserNote`
> ```

**Problem as stated by the review:** The brief's Transaction key-attribute list ends at UserNote and omits Description and TransactionType, yet both the CSV header and the transactions-api.yaml TransactionRead carry them, so the brief's domain model under-specifies fields the UI must display.

**Review's actionable payload:** Recommendation — "Resolve at draft time — reconcile the Transaction shape to the union evidenced across the API and CSV, adding Description and TransactionType." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The Transaction model the UI displays includes Description and TransactionType in addition to the brief's listed attributes, reconciling the brief to the union of fields evidenced by the CSV and the transactions API.

**Supersedes:** This supersedes the statement in `BriefV2.md` regarding the Transaction key-attribute list ending at UserNote.

---

### ADV-24 — FileLog.RecordCount is typed as a string despite being a count.

**Finding (verbatim, from the review):**
> ```
>         RecordCount:
>           type: string
> ```

**Problem as stated by the review:** FileLog.RecordCount is typed as string despite representing a count, a likely field-type mismatch that no source reconciles.

**Review's actionable payload:** Recommendation — "Resolve at draft time — confirm RecordCount's canonical type (integer vs string) before binding any UI count display or sort to it." · Disposition: Defer · Scope: fe-facing-contract.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
FileLog.RecordCount represents a count and its canonical type is integer; the API's string typing is treated as a serialization quirk, and RecordCount is bound to UI count displays and sorting as a number.

**Supersedes:** This supersedes the statement in `transactions-api.yaml` regarding RecordCount being typed as a string.

---

### ADV-25 — The transactions list is unbounded with no pagination or volume cap.

**Finding (verbatim, from the review):**
> ```
>       summary: Get a list of all transactions
> ```

**Problem as stated by the review:** The transactions list endpoint returns an unbounded list with no pagination, limit, or volume cap stated anywhere in the corpus, leaving the FE no data-volume signal to size list rendering against.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream applies a sensible pagination/virtualisation default rather than a corpus-stated cap." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The corpus states no transaction-volume cap, so the transaction list applies a sensible default of client-side pagination (or virtualisation) over the full list rather than a corpus-stated limit.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-26 — "instantly" has no latency number for a testable timing NFR.

**Finding (verbatim, from the review):**
> ```
> Reflect status changes instantly
> ```

**Problem as stated by the review:** The user-visible "instantly" status-refresh expectation carries no quantified latency budget, so no testable FE timing NFR can be written.

**Review's actionable payload:** Recommendation — "Treat as silence — the draft applies a default perceived-latency target for the status-update interaction." · Disposition: Defer · Scope: fe-facing-contract.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The status-update interaction has a default perceived-latency target of about one second; no corpus-stated latency budget exists, so this default stands as the testable timing target. (Consistent with the refresh budget in the resolution to ADV-10.)

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-27 — The file-summary counts carry no baseline/target KPI framing.

**Finding (verbatim, from the review):**
> ```
> - Count by status:
> ```

**Problem as stated by the review:** The file-summary metrics (total records, count by status) are descriptive counts with no baseline-plus-target framing, so no measurable success KPI can be derived.

**Review's actionable payload:** Recommendation — "Treat as silence — surface the counts as display fields only, not as success-criteria KPIs." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The file-summary counts (total records, count by status) are display fields only, not success-criteria KPIs; the corpus frames no baseline or target for them.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-28 — Personal financial data is processed with no masking/retention/consent and no POPIA claim.

**Finding (verbatim, from the review):**
> ```
> TXN-20260415-0001,2026/04/15 08:12,1001-2034-5567,Salary deposit - April,15750,C,ZAR
> ```

**Problem as stated by the review:** The corpus processes clearly personal financial data (account numbers, amounts) with no masking, retention, or consent statement and no POPIA/GDPR/PCI claim anywhere, so the FE-facing on-screen handling of personal data is unspecified.

**Review's actionable payload:** Recommendation — "Treat as silence — no compliance claim exists (so not Reject-grade); default to POPIA-aligned on-screen masking of AccountNumber pending consultant confirmation." · Disposition: Defer · Scope: fe-facing-contract.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
AccountNumber is masked on screen by default (showing only its last group of digits), reflecting POPIA-aligned handling of personal financial data. The corpus claims no compliance regime, so this on-screen masking is the default handling of personal data.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-29 — The resolutions file adds only functional resolutions, no quantitative signal.

**Finding (verbatim, from the review):**
> ```
> (none — every selected finding was resolved)
> ```

**Problem as stated by the review:** The consultant-approved resolutions file contributes only functional resolutions and adds no NFR, KPI, deadline, or compliance signal, leaving every quantitative gap unfilled by the authoritative corpus voice.

**Review's actionable payload:** Recommendation — "Treat as silence — /requirements stamps testable NFRs from domain defaults rather than the corpus." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The resolutions corpus contributes functional decisions only; non-functional requirements, KPIs, deadlines, and compliance signals are not supplied by the corpus and are stamped from domain defaults by /requirements.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-30 — User-administration CRUD is exposed but never scoped.

**Finding (verbatim, from the review):**
> ```
>       operationId: UserCreate
> ```

**Problem as stated by the review:** The API exposes admin-grade user administration (UserCreate / UserUpdate / UserDelete) that no source places in or out of the frontend scope.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream defaults user-administration screens out of MVP scope unless surfaced at draft time." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
User administration (UserCreate / UserUpdate / UserDelete) is out of frontend MVP scope; no source places it in scope, so no user-administration screens are built unless added later.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-31 — Role-administration CRUD is exposed but never tagged in/out of scope.

**Finding (verbatim, from the review):**
> ```
>       operationId: RoleCreate
> ```

**Problem as stated by the review:** Role administration (RoleCreate / RoleUpdate / RoleDelete) is exposed by the API but never tagged in- or out-of-scope by the brief.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream applies a scope default excluding role administration unless surfaced at draft time." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Role administration (RoleCreate / RoleUpdate / RoleDelete) is out of frontend MVP scope; the brief tags it neither in nor out, so it is excluded by default unless added later.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-32 — File-settings endpoints have no screen in §8 and no scope tag.

**Finding (verbatim, from the review):**
> ```
>   /v1/file-settings:
> ```

**Problem as stated by the review:** File-settings configuration endpoints have no corresponding screen in the brief's §8 Key Screens and no scope tag, leaving in/out status undefined.

**Review's actionable payload:** Recommendation — "Treat as silence — resolve file-settings management scope at draft time against the brief's seven named screens." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
File-settings configuration has no screen among the brief's key screens and is out of frontend MVP scope unless surfaced later.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-33 — Process-definition endpoints expand the surface with no MVP signal.

**Finding (verbatim, from the review):**
> ```
>   /v1/process-definitions:
> ```

**Problem as stated by the review:** Process-definition endpoints expand the surface beyond the brief's slice with no MVP / post-MVP signal.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream defers process-definition management to post-MVP by default." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Process-definition management is out of frontend scope for the MVP and is deferred to post-MVP by default; the brief gives it no MVP signal.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-34 — The seven named screens are never labelled the MVP/in-scope set.

**Finding (verbatim, from the review):**
> ```
> 1. Login
> 2. File Log List (Dashboard)
> 3. File Upload (Importer)
> 4. Transaction Table (Shared core)
> 5. Transaction Detail / Action modal
> ```

**Problem as stated by the review:** The brief enumerates seven key screens but never labels them as the MVP / in-scope set versus the much larger API surface, so the scope boundary is implicit.

**Review's actionable payload:** Recommendation — "Label / annotate — mark the §8 screen list as the explicit in-scope MVP set so anything outside it is treated out-of-scope by default." · Disposition: Patch · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The brief's seven named key screens are the explicit in-scope MVP set; anything outside that set (such as the larger API surface) is out of scope by default.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-35 — No browser/device/OS target and no accessibility target are stated.

**Finding (verbatim, from the review):**
> ```
> ## 7. Information Architecture
> ```

**Problem as stated by the review:** The brief's scope sections name no browser/device/OS target and no accessibility (e.g. WCAG) target, leaving these fe-relevant scope dimensions unbounded.

**Review's actionable payload:** Recommendation — "Label / annotate — record an explicit device/accessibility scope default (desktop-first, baseline accessibility) on the brief." · Disposition: Patch · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The application targets desktop browsers first and meets a baseline accessibility standard; the corpus names no specific browser/device/OS or WCAG target, so these defaults apply.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-36 — No MVP cut, release sequence, timeline, team size, or budget bounds the build.

**Finding (verbatim, from the review):**
> ```
> The frontend SPA and the BFF must share an eTLD+1
> ```

**Problem as stated by the review:** This deployment constraint is the only scope-adjacent bound stated, yet no source defines an MVP cut, release sequence, timeline, team size, or budget to bound what is buildable.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream treats the absence of phasing/resourcing as unspecified and sequences MVP at draft time." · Disposition: Defer · Scope: fe-relevant.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
No MVP cut, release sequence, timeline, team size, or budget is defined by the corpus; MVP scope and sequencing are therefore decided at draft time rather than read from the corpus.

**Supersedes:** (supersedes nothing — net-new information)

---

## Findings considered but skipped

(none — every selected finding was resolved)
