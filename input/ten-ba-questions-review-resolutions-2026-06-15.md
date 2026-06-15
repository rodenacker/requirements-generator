# Review Resolutions — 10 BA Questions (review-requirements/TEN-BA-QUESTIONS)

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
| Source review | `review-requirements/TEN-BA-QUESTIONS/ten-ba-questions-review.html` |
| Source review sha256 | `286d8ee2558f9a167ead40e56fa06f7a964eb6c57258ea91fee28b27f9c1f0c9` |
| Review's source fingerprint | `88eb974feca6569e8aae57ab9e112ecd3da89a60897c1f7d2758d10d5e431b98` |
| Fingerprint target (`requirements/requirements.md`) at resolution time | `88eb974feca6569e8aae57ab9e112ecd3da89a60897c1f7d2758d10d5e431b98` |
| Source drift | none |
| Methodology | `ten-ba-questions` |
| Resolution date | 2026-06-15 |
| Findings resolved | BAQ-01, BAQ-02, BAQ-03, BAQ-04, BAQ-05, BAQ-06, BAQ-07, BAQ-08, BAQ-09, BAQ-10 |
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

### BAQ-01 — What is the current process for importing and approving transactions today, and what about it…

**Finding (verbatim, from the review):**
> What is the current process for importing and approving transactions today, and what about it — cost, error rate, delay, or risk — makes it unsustainable enough to justify building this system?

**Problem as stated by the review:** The document specifies the solution — a dual-role import-and-approval frontend — in depth across seventy-five amendments, but never states the problem it replaces or what the status quo costs. Without that anchor the team cannot tell which of the seven in-scope screens relieves real pain and which is merely convenient, and scope trade-offs are made blind.

**Review's actionable payload:** Gap-surfacing elicitation question (category C1 Problem & justification; anchor `missing-section: problem-justification`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Today transaction files are imported and approved through a manual, fragmented process — spreadsheets and ad-hoc tooling — that is slow, error-prone, and lacks a clear audit trail. This system replaces that process with a single role-based review surface in which Importers upload and track files and Approvers review and action transactions, giving the work a reliable, status-visible home. This status-quo baseline is a stated assumption to be validated with the client.

**Grounding:** [assumption — confirm with client] — commits the document to a stated status-quo baseline that justifies the seven in-scope screens; the baseline must be validated with the client before it anchors scope trade-offs.

**Supersedes:** (supersedes nothing — net-new information)

---

### BAQ-02 — Is transaction approval uniform for every Imported transaction, or do transactions above a monetary…

**Finding (verbatim, from the review):**
> Is transaction approval uniform for every Imported transaction, or do transactions above a monetary threshold — or of a particular type or currency — require additional or more-senior approval?

**Problem as stated by the review:** §6.2 defines approve and reject as a single uniform action with no amount-based tier, yet threshold-based authorisation is a near-universal control in financial transaction approval. If a tier exists, the approval workflow becomes multi-stage and RBAC gains an approval-limit dimension — a materially different build from the flat model the document implies.

**Review's actionable payload:** Gap-surfacing elicitation question (category C5 Business rules & decisions; anchor `§6.2`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Transaction approval is uniform: every Imported transaction is approved or rejected by a single Approver action regardless of amount, type, or currency. No monetary threshold, tiered authorisation, or approval-limit dimension applies in the MVP; the approval workflow stays a flat single-action model and no approval-limit field is added to the User or Role data.

**Grounding:** [grounded: §6.2] — keeps the §6.2 flat single-action approve/reject model; commits the build to no multi-stage approval and no approval-limit dimension on RBAC.

**Supersedes:** (supersedes nothing — net-new information)

---

### BAQ-03 — Can any Approver action any Imported transaction from a shared pool, or are transactions routed or…

**Finding (verbatim, from the review):**
> Can any Approver action any Imported transaction from a shared pool, or are transactions routed or assigned to specific Approvers by file, amount, team, or owner?

**Problem as stated by the review:** §6.1 F-08 and the §6.5 RBAC matrix imply any Approver may action any Imported transaction, but the document never states whether transactions are routed to named approvers. Assignment introduces queues, ownership, and hand-off — a materially different workflow and Transaction-table design from a shared review pool.

**Review's actionable payload:** Gap-surfacing elicitation question (category C5 Business rules & decisions; anchor `§6.1`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Any Approver may action any Imported transaction from a shared review pool; transactions are not routed or assigned to specific Approvers by file, amount, team, or owner. The Transaction Table is a shared work surface for all Approvers, with no assignment or ownership field and no per-approver queue. This is consistent with AMD-66 (the shared global/file-scoped review model) and AMD-70 (no acting-Approver attribution).

**Grounding:** [grounded: §6.1] — keeps the shared pool implied by §6.1 F-08 and the §6.5 RBAC matrix; commits the build to no assignment field, no per-approver queue, and no hand-off/reassignment flow.

**Supersedes:** (supersedes nothing — net-new information)

---

### BAQ-04 — When a transaction is approved or rejected in error, what is the business recourse, given that §2.3…

**Finding (verbatim, from the review):**
> When a transaction is approved or rejected in error, what is the business recourse, given that §2.3 and BR-02 make the Approved and Rejected states terminal and immutable with no correction or reversal path?

**Problem as stated by the review:** The Approver's stated fear in §3 is actioning the wrong transaction, yet every action is terminal and irreversible with no correction, reversal, or re-import flow defined. The business must say whether erroneous actions are absorbed downstream or need an in-system remedy — the answer decides whether a correction surface enters scope.

**Review's actionable payload:** Gap-surfacing elicitation question (category C5 Business rules & decisions; anchor `§2.3`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Approve and reject are terminal and irreversible in the frontend, with no in-system correction, reversal, or re-action surface. An erroneous action is handled outside this system — by a backend correction or an upstream re-import — so the §2.3/BR-02 terminal-immutability invariant stands and erroneous-action recourse is an operational/backend concern. This is consistent with AMD-71 (the two-action model, with no third actioning outcome).

**Grounding:** [grounded: §2.3] — preserves the §2.3/BR-02 terminal-immutable invariant; commits the build to no correction or reversal UI, with error recourse handled outside the system.

**Supersedes:** (supersedes nothing — net-new information)

---

### BAQ-05 — Beyond the two operator roles, who is the business owner accountable for this system's outcomes…

**Finding (verbatim, from the review):**
> Beyond the two operator roles, who is the business owner accountable for this system's outcomes, and who has the authority to sign off these requirements and accept the delivered system?

**Problem as stated by the review:** §3 describes the Importer and Approver who use the screens but names no decision-maker, budget owner, or sign-off authority. Without a named owner the open business decisions in this list have no one to route to, and acceptance of the delivered system has no defined approver.

**Review's actionable payload:** Gap-surfacing elicitation question (category C2 Stakeholders & users; anchor `§3`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
Naming the accountable business owner and the requirements sign-off / delivery-acceptance authority is a project-governance concern outside this frontend requirements document. The system models only the two operator personas, Importer and Approver; stakeholder governance — the accountable owner, requirements sign-off, and acceptance authority — is recorded in the PRD or project charter rather than in requirements.md, and no additional persona or RBAC role is added to §3 or §6.5 on its account.

**Grounding:** [domain-default] — frontend requirements model the system's users, not project governance; commits the document to no new persona or RBAC role, with owner/sign-off tracked outside the FE spec.

**Supersedes:** (supersedes nothing — net-new information)

---

### BAQ-06 — Is this system the system of record for transactions, or are the uploaded files produced by an…

**Finding (verbatim, from the review):**
> Is this system the system of record for transactions, or are the uploaded files produced by an upstream ledger or banking system that remains authoritative for the underlying data?

**Problem as stated by the review:** Transactions enter only via uploaded files (§2.1, §5 File Upload), which implies an upstream producer, but the document never says whether this system owns the transaction data or reviews a copy of it. The answer governs whether discrepancies, corrections, and re-imports are this system's concern or the upstream system's.

**Review's actionable payload:** Gap-surfacing elicitation question (category C6 Data, entities & integrations; anchor `§2.1`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
This system is not the system of record for transactions. Transactions originate from files produced by an upstream source — a ledger or banking system — that remains authoritative for the underlying data, and this system is a read-oriented review-and-approval surface that reflects that data (per §1, §2.1). Discrepancies, corrections, and re-imports are the upstream system's concern, not this system's. This is consistent with the §1 "reflect / read-oriented" framing, the BAQ-04 decision that erroneous-action recourse is external, and AMD-65 (no in-system Failed-file recovery).

**Grounding:** [grounded: §2.1] — affirms the read-oriented review surface implied by §1 and §2.1; commits the build to no data-ownership or correction features, leaving discrepancy handling to the upstream system.

**Supersedes:** (supersedes nothing — net-new information)

---

### BAQ-07 — Can a single file or the retained transaction set contain more than one Currency, and if so what is…

**Finding (verbatim, from the review):**
> Can a single file or the retained transaction set contain more than one Currency, and if so what is the business rule for mixed currencies in the file summary counts and the CSV export?

**Problem as stated by the review:** §7 carries a free-form Currency field per transaction with no single-currency constraint, yet the file summary (RPT-01) and export (RPT-02) aggregate across transactions. If files can mix currencies, cross-currency totals are meaningless and the summary and export need per-currency grouping — a rule the document does not state.

**Review's actionable payload:** Gap-surfacing elicitation question (category C6 Data, entities & integrations; anchor `§7`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
A single file and the retained transaction set may contain multiple currencies; no single-currency constraint applies. No cross-currency aggregation is performed: the file summary (RPT-01) counts records by status and does not sum amounts, and the export (RPT-02) lists each transaction's own Amount and Currency per row. Mixed currencies therefore need no special grouping rule, and Currency remains a free-form per-transaction field displayed as-is.

**Grounding:** [grounded: §7] — relies on RPT-01 counting records (not summing amounts) and RPT-02 exporting per-row values; commits the build to no per-currency grouping or currency-total feature.

**Supersedes:** (supersedes nothing — net-new information)

---

### BAQ-08 — Does FileLog.RecordCount count every row in the uploaded file, or only the transactions that parsed…

**Finding (verbatim, from the review):**
> Does FileLog.RecordCount count every row in the uploaded file, or only the transactions that parsed successfully, and what should the user see when those two numbers differ?

**Problem as stated by the review:** §1.5 places file-validation-error review out of scope, so some rows may never become transactions, yet RecordCount is displayed (F-04) and drives the file summary (RPT-01) with no definition of what it counts. If RecordCount and the visible transaction count can diverge, a user will read a partially-ingested file as complete.

**Review's actionable payload:** Gap-surfacing elicitation question (category C6 Data, entities & integrations; anchor `§7`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
FileLog.RecordCount counts every row in the uploaded file, including rows that failed to parse. To prevent a partially-ingested file reading as complete, the file summary shows both the total row count and the count of successfully ingested transactions, surfacing any difference as an explicit "N of M rows ingested" indicator. The ingested-transaction count is a PROPOSED ADDITION to the FileLog summary (not currently a §7 property); it must be confirmed before the closed property set is treated as extended.

**Grounding:** [domain-default] — showing ingested-versus-total is a standard file-ingestion transparency control; commits the build to a second count alongside RecordCount and a divergence indicator on the file summary.

**Supersedes:** (supersedes nothing — net-new information)

---

### BAQ-09 — Is the File Status enum the frontend renders — Uploaded, Processing, Completed, Failed — a closed…

**Finding (verbatim, from the review):**
> Is the File Status enum the frontend renders — Uploaded, Processing, Completed, Failed — a closed set the backend guarantees, or could the backend's activity-name-to-status derivation emit a value the frontend has no chip for?

**Problem as stated by the review:** The amendments make File Status backend-owned and rendered verbatim (AMD-02, AMD-12, AMD-29), so the frontend now wholly depends on the backend's emitted enum matching the four §7 values. If that dependency is an unconfirmed assumption, an unmapped status would render as a blank or broken chip — a risk-bearing dependency that should be contracted, not assumed.

**Review's actionable payload:** Gap-surfacing elicitation question (category C8 Assumptions, dependencies & sequencing; anchor `§6.10`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
The four File Status values — Uploaded, Processing, Completed, Failed — are a closed set the backend contractually guarantees: the §6.10 consumed File Logs contract specifies that Status is always one of these four, so the frontend renders exactly one chip per value and no other value occurs. This converts the backend-owned "render verbatim" dependency recorded in AMD-02 / AMD-12 / AMD-29 into an explicit frontend-facing contract rather than an unconfirmed assumption; the File Status enum is no longer "inferred, provisional" but a contracted closed set, so no unknown-value fallback chip is required.

**Grounding:** [grounded: AMD-29] — builds on the AMD-29 backend-owned, render-verbatim dependency; commits the build to treating the four-value File Status enum as a contracted §6.10 guarantee with no fallback-chip logic.

**Supersedes:** This supersedes the statement in `requirements/requirements.md` regarding the §6.10 File Logs contract and the §7 FileLog Status enum — previously "inferred, provisional" — which is now a backend-guaranteed closed set of exactly four values.

---

### BAQ-10 — What event or pressure triggered this work now — a regulatory change, an audit finding, a rising…

**Finding (verbatim, from the review):**
> What event or pressure triggered this work now — a regulatory change, an audit finding, a rising error rate, or growth — that should set the timeline and the priority order of the goals?

**Problem as stated by the review:** §1 states the purpose as a capability (a file-driven ingestion-and-approval surface) but names no triggering event, so the relative urgency of the five goals is unanchored. Knowing why now lets the team sequence the seven screens against the real driver rather than guessing.

**Review's actionable payload:** Gap-surfacing elicitation question (category C1 Problem & justification; anchor `§1`). The question above is the actionable payload; the rationale is quoted under Problem. The review offers no recommendation — the resolution is a consultant decision among drafted candidates.

**Resolution** `[AI-INFERRED, CONSULTANT-CONFIRMED]`
No triggering event is stated in the corpus; the work is a capability-delivery initiative — building the file-driven ingestion-and-approval surface — with no external time pressure. Goal sequencing therefore follows the §4.1 goal priorities and the §3 persona needs rather than an external driver, and no deadline or urgency requirement enters scope.

**Grounding:** [grounded: §1] — affirms §1's framing of the work as a capability; commits goal ordering to the §4.1 priorities and §3 persona fears, with no deadline/urgency requirement.

**Supersedes:** (supersedes nothing — net-new information)

---

## Findings considered but skipped

(none — every selected finding was resolved)
