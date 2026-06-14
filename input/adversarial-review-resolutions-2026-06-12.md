# Review Resolutions — Adversarial (ADVERSARIAL)

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
| Source review sha256 | `665c35318d168152d6afd8593d047c7bb4273d3684c18f21fb95833670f506a5` |
| Review's source fingerprint | `2b16d0d9c837595a7faeead809553aa5822d10e198bcb581af1d759ecabe45ae` |
| Fingerprint target (`requirements/source-manifest.json`) at resolution time | `2b16d0d9c837595a7faeead809553aa5822d10e198bcb581af1d759ecabe45ae` |
| Source drift | none |
| Methodology | `adversarial` |
| Resolution date | 2026-06-12 |
| Findings resolved | ADV-04, ADV-05, ADV-18, ADV-19, ADV-23 |
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

### ADV-04 — Export non-happy paths uncovered

**Finding (verbatim, from the review):**
> - Uses filtered dataset (no explicit endpoint provided → simulate)

**Problem as stated by the review:** The Export workflow is named and given UI/screen treatment, but the corpus describes no behaviour for an empty filtered dataset, a partial/failed CSV serialization, or a large-result export — only the happy path of formatting the current grid.

**Review's actionable payload:** Recommendation — "Treat as silence — downstream must mark export empty/large/failure behaviour as unspecified and apply a simulate-only default, not invent error semantics." Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Export behaviour for empty, oversized, and partially-failed result sets is unspecified. The prototype generates the CSV client-side from the currently filtered transactions grid, shows a no-op state when the filtered set is empty, and defines no server-side export-failure handling.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-05 — 'Failed' file-state recovery uncovered

**Finding (verbatim, from the review):**
> ### File States (inferred)

**Problem as stated by the review:** The 'Failed' file state is asserted by inference, yet no flow describes what an Importer sees or does on file failure, despite a validation-failure subsystem existing in the API.

**Review's actionable payload:** Recommendation — "Treat as second-hand — the file-state set is author-inferred (not source-grounded); downstream must label the Failed-state recovery flow as unspecified rather than authoritative." Disposition — Defer.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The file lifecycle states Uploaded, Processing, Completed, and Failed are a business-analyst inference rather than a confirmed state model. The user-facing recovery flow for a Failed file is unspecified and is to be treated as not-yet-defined, not as authoritative.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-18 — Login endpoint path contradicts across sources

**Finding (verbatim, from the review):**
> - `POST /v1/users/login`

**Problem as stated by the review:** The Brief states the login endpoint as POST /v1/users/login, but auth-api.yaml (operationId AuthLogin) gives POST /v1/auth/login for the same authentication action — two sources contradict on a load-bearing endpoint path with nothing in-corpus resolving it.

**Review's actionable payload:** Recommendation — "Reconcile in-corpus — treat auth-api.yaml's /v1/auth/login as canonical and correct the Brief's /v1/users/login reference (or vice versa) before drafting the auth flow." Disposition — Reject.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The authentication endpoint is POST /v1/auth/login, as defined in auth-api.yaml. The brief's reference to POST /v1/users/login is incorrect and does not apply.

**Supersedes:** This supersedes the statement in `BriefV2.md` regarding the login endpoint (POST /v1/users/login).

---

### ADV-19 — RBAC roles absent from API specs

**Finding (verbatim, from the review):**
> - ❌ Cannot approve/reject

**Problem as stated by the review:** The Brief builds the entire RBAC model around roles 'Importer' and 'Approver', but neither API contains those roles (both only example 'Viewer'); the load-bearing permission model has no corresponding role vocabulary in the specs and nothing reconciles them.

**Review's actionable payload:** Recommendation — "Reconcile in-corpus — establish whether Importer/Approver are seeded role records or app-level role constants, and align the API role vocabulary with the Brief before drafting role-gated screens." Disposition — Reject.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The application's two roles are Importer and Approver, as defined in the brief; these are the canonical role vocabulary for role-gated screens. The 'Viewer' value appearing in the API schema examples is an illustrative placeholder, not an authoritative list of roles.

**Supersedes:** (supersedes nothing — net-new information)

---

### ADV-23 — CSV 'C'/'D' contradicts API 'Debit'

**Finding (verbatim, from the review):**
> TXN-20260415-0002,2026/04/15 08:34,1001-2034-5567,Woolworths Sandton,487.32,D,ZAR

**Problem as stated by the review:** The CSV encodes TransactionType as single letters 'C'/'D', while transactions-api.yaml's TransactionRead.TransactionType example is the spelled-out word 'Debit' — the import data and the API contract disagree on the domain of a load-bearing field, with no mapping declared anywhere in the corpus.

**Review's actionable payload:** Recommendation — "Reconcile in-corpus — declare the canonical TransactionType domain (codes vs words) and the import-to-API mapping so the displayed value is unambiguous." Disposition — Reject.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
TransactionType is represented by the full words 'Credit' and 'Debit' (the API contract value). The import CSV's single-letter codes map C → Credit and D → Debit, and the full word is what the UI displays.

**Supersedes:** This supersedes the statement in `transactions_2026-04-15.csv` regarding the TransactionType code values (C/D).

---

## Findings considered but skipped

(none — every selected finding was resolved)
