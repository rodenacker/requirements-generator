<!-- ROLE: PRD (merged). Audience is human (consultant, client stakeholders, sign-off authorities) and downstream LLM analysers. `[SRC: PC-NNN]` tags are retained as inline provenance; `prd/draft-claims.ndjson` is the authoritative store of verbatim source quotes. -->

# Product Requirements Document: Transaction Import & Approval System [SRC: PC-001]

**Domain:** Financial operations / back-office transaction processing **Status:** final **Created:** 2026-05-19 **Last finalised at:** 2026-05-19

---

## 1. Document metadata

| Field | Value |
| --- | --- |
| Product name | Transaction Import & Approval System [SRC: PC-001] |
| Owner / author | Consultant / PM (to be confirmed) |
| Audience | Client decision-makers, internal product / engineering leadership, compliance sign-off authority |
| Document version | 0.1-draft |
| Build target reference | to-be-determined |
| Reading time | ~20 minutes |

**Reading list (companion artefacts):**

- requirements/requirements.md — the LLM-audience FE spec derived from this PRD (when produced)
- design-system/design-system.md — the design tokens (when produced)

<!-- rev: run-1 2026-05-19 -->

---

## 2. Problem & opportunity

### 2.1 Problem statement

Back-office finance and operations teams that ingest transactional data from upstream partners today rely on a mix of spreadsheets, email-based hand-offs, and ad-hoc database queries to move records from raw upload through human approval to downstream export. The process is slow, error-prone, and offers poor visibility into which transactions are awaiting which person's attention, leaving a gap between "data has landed" and "data has been signed off." This product replaces that hand-rolled flow with a dual-role web application that makes file ingestion, transaction-level review, and approval/rejection an explicit, audited lifecycle.

### 2.2 Current state

Today, the team typically receives transaction files via SFTP or email, manually loads them into a staging table, exports a working sheet to reviewers, collects approval/rejection decisions out-of-band (often in chat threads), and stitches the result back into a system of record. There is no single screen that shows file-level health, transaction-level status, and who-acted-on-what.

### 2.3 Opportunity size

| Dimension | Value |
| --- | --- |
| Affected users | ~10–50 importers and approvers across one or two operations teams in the initial client deployment |
| Frequency of pain | Daily — every business-day batch of inbound files triggers a full review cycle |
| Cost of inaction | Compounding manual-reconciliation overhead, missed cut-offs, and weak audit trail for rejected transactions |
| Trend | Growing — increasing transaction volumes and stricter audit / regulator scrutiny of decision provenance |

<!-- rev: run-1 2026-05-19 -->

---

## 3. Competitive context

| Competitor / alternative | What it does well | What it does poorly | Why we're not adopting it |
| --- | --- | --- | --- |
| Status quo: spreadsheets + email | Zero up-front tooling cost; familiar to staff | No audit trail, no role enforcement, no transaction-level state machine | The status quo is the problem we are solving |
| Generic workflow / BPM platform (e.g. Camunda, Pega) | Mature engines, broad integration surface | Heavy configuration overhead for a narrow file-ingestion-and-approval use case | Implementation cost and lead time exceed the value for a focused two-role workflow |
| Do nothing / extend existing internal tooling | No new vendor; predictable engineering ownership | The internal tooling does not currently model file-driven ingestion or role-based approval — extending it is comparable in effort to building the new app | Net build cost is similar; the new app gives a clean separation of concerns |

**Differentiation thesis:** A focused, two-role data-management app that treats the file → transaction → approval flow as a first-class lifecycle rather than a generic workflow, optimised for the specific shape of transactional ingestion the client already runs.

<!-- rev: run-1 2026-05-19 -->

---

## 4. Stakeholders & sign-off authority

| Role | Name (if known) | Sign-off domain | Cadence |
| --- | --- | --- | --- |
| Product sponsor | (to be confirmed) | Overall MVP scope and release date | Weekly review |
| Operations lead (Importer-side) | (to be confirmed) | Upload UX and file-log presentation | Weekly review |
| Approvals lead (Approver-side) | (to be confirmed) | Approval workflow, reject-note policy, export format | Weekly review |
| Compliance / audit | (to be confirmed) | Audit-trail completeness, retention policy | Release-gate sign-off only |
| Engineering lead | (to be confirmed) | Technical feasibility, integration with existing API surface | Weekly review |

**RACI summary:** Product sponsor is Accountable for MVP delivery; ops and approvals leads are Responsible for in-domain decisions; compliance is Consulted on audit-trail design and signs off at release; engineering is Responsible for build and Consulted on phasing.

<!-- rev: run-1 2026-05-19 -->

---

## 5. Business goals & success metrics

### 5.1 Business goals

| ID | Goal | Tied to (§2 problem / §6 hypothesis) |
| --- | --- | --- |
| BG-01 | Replace the manual file → review → approval workflow with a single auditable system | → §2.1 / → §6 H-01 |
| BG-02 | Reduce time from file upload to fully-actioned batch (approve/reject every transaction) | → §2.1 / → §6 H-02 |
| BG-03 | Produce a defensible, per-transaction audit trail for every approve and reject action | → §2.3 cost-of-inaction / → §6 H-03 |

### 5.2 Success metrics

| ID | Metric | Tied to (BG-NN) | Type | Baseline | Target | Measurement cadence | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M-01 | Median time from file upload to last-transaction action (approve or reject) | → BG-02 / → §6 H-02 | lagging | ~1 business day (estimate) | ≤ 4 hours | weekly | Approvals lead |
| M-02 | % of rejected transactions carrying a non-empty reviewer note | → BG-03 / → §6 H-03 | lagging | unknown (not currently captured) | 100% (enforced at submit) | per release | Compliance / audit |
| M-03 | % of importers using the in-app upload (vs. legacy SFTP / email) | → BG-01 / → §6 H-01 | leading | 0% (no prior in-app upload) | ≥ 80% within 60 days of MVP | monthly | Operations lead |
| M-04 | Number of file logs with at least one transaction in `Imported` state ageing > 24h | → BG-02 / → §2.1 | leading | unknown | trending downward week-over-week | weekly | Approvals lead |

### 5.3 Non-goals

- Replace the upstream transaction-producing systems or alter the file format they emit.
- Build a general-purpose workflow / BPM engine — the lifecycle is narrowly scoped to the file → transaction → approve/reject path.
- Provide a mobile-native client — the prototype is web-first.

<!-- rev: run-1 2026-05-19 -->

---

## 6. Hypotheses & assumptions

### 6.1 Hypotheses (with falsification conditions)

| ID | Hypothesis | Falsification condition | Riskiness | Test owner |
| --- | --- | --- | --- | --- |
| H-01 | We believe importers and approvers will adopt a single app for the file → review → action flow because it eliminates spreadsheet hand-offs | We will know we are wrong if < 50% of file uploads in the first 60 post-MVP days come through the app rather than legacy channels | high | Operations lead |
| H-02 | We believe approvers can clear a typical day's transaction backlog within 4 hours when the table supports search, filter, and bulk selection | We will know we are wrong if median time-to-action per file exceeds 8 hours across two consecutive measurement weeks post-MVP | high | Approvals lead |
| H-03 | We believe mandatory reject-notes will produce an audit-grade reason trail without adding meaningful friction to approver workflow | We will know we are wrong if approvers report (in post-MVP feedback) that the note requirement materially slows them down, OR if > 5% of rejects show notes shorter than a documented minimum length | medium | Approvals lead |
| H-04 | We believe a single shared transaction table is the right primary surface for both roles, with role-gated row actions sufficient to keep importers and approvers from confusing each other's intent | We will know we are wrong if usability sessions surface frequent role-confusion errors (importer attempting to approve, or approver expecting to upload from the table) | medium | Operations lead |

### 6.2 Assumptions (taken as given for this PRD)

| ID | Assumption | Source | Validation plan (if any) |
| --- | --- | --- | --- |
| A-01 | The system models exactly two operational roles — Importer and Approver — with no overlapping permissions [SRC: PC-002] | stated | accepted-as-given |
| A-02 | Authentication is handled via an existing user-login endpoint; no SSO integration is in scope for MVP | inferred | accepted-as-given |
| A-03 | Files arrive in a format the upstream upload endpoint already accepts; format negotiation is not part of this product | inferred | accepted-as-given |
| A-04 | The approve and reject endpoints persist status changes durably; the app's job is presentation + workflow, not transactional integrity | inferred | accepted-as-given |

<!-- rev: run-1 2026-05-19 -->

---

## 7. Users & jobs-to-be-done

### 7.1 Primary personas

#### Importer

| Field | Value |
| --- | --- |
| Role / title | Operations specialist responsible for moving inbound transactional files into the review pipeline [SRC: PC-003] |
| Day-in-the-life summary | Receives batches of transaction files from upstream partners, uploads each into the system, and confirms the file's record count and status before handing it on for approval |
| Goals they pursue | Get every inbound file uploaded, parsed, and visible to approvers before the daily cut-off |
| Frustrations they carry | No visibility into whether previously-uploaded files have been processed; today's hand-off is by email or chat |
| Tools they use today | SFTP client, spreadsheets, internal staging database |
| Decision-making authority | Decides which files to upload and in what order; cannot approve or reject individual transactions [SRC: PC-004] |

#### Approver

| Field | Value |
| --- | --- |
| Role / title | Reviewer with authority to approve or reject individual transactions, and to export approved data [SRC: PC-005] |
| Day-in-the-life summary | Reviews the day's uploaded transactions, applies approve or reject decisions row-by-row (or in bulk when confident), and exports the resulting dataset for downstream use |
| Goals they pursue | Action every queued transaction before the daily cut-off, with a defensible rationale on every reject |
| Frustrations they carry | Manual reconciliation between spreadsheet reviews and the system of record; no single screen showing what's pending |
| Tools they use today | Spreadsheets, email threads, internal reporting tool for after-the-fact reconciliation |
| Decision-making authority | Authoritative on approve / reject decisions for in-scope transactions; cannot upload files [SRC: PC-006] |

### 7.2 Secondary personas (mentioned but not primary targets)

- Compliance / audit reviewer — consumes the audit trail and reject-note history, but does not directly action transactions in this product.
- Engineering / operations support — investigates failed files and bulk-error conditions surfaced by the file-summary view.

### 7.3 Jobs-to-be-done

| ID | Job statement | Hired by (persona → §7.1) | Outcome the user wants | Current alternative |
| --- | --- | --- | --- | --- |
| J-01 | When a new batch of transaction files lands, I want to upload them into a system that immediately shows their parsing status, so I can confirm the work moved forward and is visible to the approver | → §7.1 Importer | Clear visibility that the file is now in the pipeline | Manual SFTP / email + chat ping to confirm receipt |
| J-02 | When a file's transactions arrive in the queue, I want to scan, filter, and approve or reject them quickly with a clear rejection rationale, so I can clear the day's backlog with an audit trail | → §7.1 Approver | A complete, defensible decision record for every queued transaction by end of day | Spreadsheet review with manual reconciliation back to the source system |
| J-03 | When I have finished actioning a batch, I want to export the approved subset in CSV, so downstream consumers can pick up the work | → §7.1 Approver | A clean, filter-respecting CSV ready for the downstream pipeline | Ad-hoc database query or hand-rolled export |
| J-04 | When I drill into a file, I want a summary of how many transactions are in each state and whether any bulk errors were encountered, so I can decide whether to investigate or move on | → §7.1 Importer & Approver | Quick per-file confidence (or a clear reason to look closer) | Manual SQL or operator-driven log inspection |

<!-- rev: run-1 2026-05-19 -->

---

## 8. Solution overview & key capabilities

### 8.1 Solution one-liner

A dual-role web application that ingests transactional files, presents the resulting transactions in a searchable, filterable table, and routes them through an approve-or-reject lifecycle with a defensible audit trail. [SRC: PC-007]

### 8.2 Key capabilities (capability-level only)

| ID | Capability | Why this matters (→ §5 metric / §6 hypothesis / §7 job) | Phase (→ §9) |
| --- | --- | --- | --- |
| C-01 | File-driven ingestion with a per-file log of upload, parse, and processing state [SRC: PC-008] | → §5 M-03 / → §6 H-01 / → §7 J-01 | mvp |
| C-02 | Transaction-level lifecycle with explicit states (imported, approved, rejected) [SRC: PC-009] | → §5 M-01 / → §6 H-02 / → §7 J-02 | mvp |
| C-03 | Role-based interaction constraints separating Importer and Approver permissions [SRC: PC-010] | → §6 H-04 / → §7 J-01, J-02 | mvp |
| C-04 | Tabular transaction review with search, filter, and (optional but high-value) bulk selection [SRC: PC-011] | → §5 M-01 / → §6 H-02 / → §7 J-02 | mvp |
| C-05 | Mandatory reject-note capture as part of the rejection action [SRC: PC-012] | → §5 M-02 / → §6 H-03 / → §7 J-02 | mvp |
| C-06 | CSV export of the current filtered transaction set [SRC: PC-013] | → §7 J-03 | mvp |
| C-07 | Per-file summary view showing counts per state and a flag for bulk-error files | → §6 H-01 / → §7 J-04 | mvp |
| C-08 | Authentication landing differentiated by role (Importer vs Approver) | → §6 H-04 / → §7 J-01, J-02 | mvp |
| C-09 | Cross-cutting search/filter that applies to both file logs and the transaction table | → §5 M-01 / → §7 J-02 | mvp |

### 8.3 Key interaction surfaces (capability-level)

The application is organised around three primary surfaces. The first is a file-log dashboard where users see the queue of uploaded files with their processing state and per-file metadata; row-level drill-in moves the user into the second surface. The second is the transaction table — the core working screen for both roles — which exposes the rows extracted from a file or, when filtered across all files, the user's full pending or actioned queue; this is where the approver does their work via row-level approve/reject (with the reject action gating on a mandatory note) and, where the application offers it, bulk selection. The third is the upload surface, available only to the Importer role, where a file is selected, named, and submitted into the file log. A file-summary view sits underneath the dashboard as a per-file detail surface, surfacing counts-by-state and bulk-error indicators. Throughout, role-based visibility hides the upload entry-point from Approvers and the approve/reject actions from Importers, so each role sees only the controls relevant to their work.

<!-- rev: run-1 2026-05-19 -->

---

## 9. Scope, MVP definition & phasing

### 9.1 Phasing

| Phase | Capabilities (→ §8.2 C-NN) | Audience served (→ §7.1) | Definition of done | Target date |
| --- | --- | --- | --- | --- |
| MVP | C-01, C-02, C-03, C-04, C-05, C-06, C-07, C-08, C-09 | Importer, Approver | An Importer can upload a file and an Approver can action every resulting transaction (approve or reject with mandatory note) and export the approved subset in CSV, end-to-end, in a hosted prototype environment | T+6 weeks from kickoff |
| Phase 2 | Audit-trail surfacing in-app (per-transaction action history), saved filter presets, role-aware notifications | Importer, Approver, Compliance reviewer | An auditor can answer "who actioned transaction X, when, and why" from inside the app, and approvers can re-use saved filter views across days | T+10 weeks |
| Phase 3+ | SSO integration, customisable export formats beyond CSV, multi-tenant administration | Importer, Approver, Compliance reviewer | The product can be on-boarded to a new client tenant without bespoke engineering work | T+16 weeks |

### 9.2 MVP scope rationale

The MVP slice deliberately covers the full operational loop — upload → review → action → export — for both roles, because the value of the product comes from removing the spreadsheet hand-off across that whole loop, not from any one screen. Cutting any one of those capabilities (upload, review, action, export) would leave the user back in the legacy workflow for that step, so the test of "do users adopt" is only meaningful with all four present. Deferred items (audit-trail surfacing inside the app, SSO, custom export formats) are valuable but not load-bearing for the first test of adoption.

### 9.3 Capability-to-phase matrix

| Capability (→ §8.2) | MVP | Phase 2 | Phase 3+ |
| --- | --- | --- | --- |
| C-01 File-driven ingestion | ✓ | — | — |
| C-02 Transaction lifecycle | ✓ | — | — |
| C-03 Role-based constraints | ✓ | — | — |
| C-04 Tabular review (search, filter, bulk) | ✓ | — | — |
| C-05 Mandatory reject-note | ✓ | — | — |
| C-06 CSV export | ✓ | — | — |
| C-07 Per-file summary view | ✓ | — | — |
| C-08 Role-aware authentication landing | ✓ | — | — |
| C-09 Cross-cutting search/filter | ✓ | — | — |

<!-- rev: run-1 2026-05-19 -->

---

## 10. Out of scope & rationale

| Item | Why out of scope | Where it might live (if anywhere) |
| --- | --- | --- |
| Mobile-native client | The working surfaces (file log, transaction table, upload, export) are desk-bound operational tasks; a mobile client would duplicate effort for no proven benefit at this phase | Not planned for MVP or Phase 2; revisit if mobile-first usage emerges |
| Real-time multi-user collaboration on a single transaction | The lifecycle is single-owner-per-action by design (one approver acts, one reject reason is captured); concurrent editing adds workflow ambiguity, not throughput | Not planned |
| Deep analytics dashboard / business-intelligence layer | The success metrics in §5.2 are operational, not analytical; dashboards belong to the BI tooling layer that consumes the exported CSVs | Existing internal BI tool |
| SSO / federated identity integration | The included login endpoint covers MVP; SSO is a Phase 3 enterprise-readiness concern | Phase 3 (§9.1) |
| Custom export formats beyond CSV | CSV is the documented default; alternative formats (Excel, JSON, downstream-system-specific) are deferred until a real downstream consumer asks for them | Phase 3 (§9.1) |

<!-- rev: run-1 2026-05-19 -->

---

## 11. Risks & mitigations

| ID | Risk | Category | Likelihood | Impact | Mitigation | Owner | Trigger to escalate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-01 | Approvers reject the in-app workflow and continue working from spreadsheets, leaving the product unused | adoption | medium | high | Run paired walkthroughs with the approvals lead during MVP build; ship a clear migration story from the legacy spreadsheet view; track M-03 weekly | Approvals lead | First weekly M-03 reading below 25% post-MVP |
| R-02 | Mandatory reject-note becomes a workflow blocker, with approvers writing throw-away notes ("n/a") that defeat the audit purpose | operational | medium | medium | Surface a brief reject-reason taxonomy alongside the free-text note; monitor M-02 with a minimum-length sub-metric | Approvals lead | First post-MVP audit review flags > 10% notes as low-information |
| R-03 | Compliance / audit team finds the per-transaction audit trail insufficient for regulator-grade evidence | regulatory | medium | high | Validate audit-trail design with compliance before MVP build; reserve scope in Phase 2 for in-app audit-trail surfacing | Compliance / audit | Compliance flags during pre-release review |
| R-04 | The included login endpoint is insufficient for the client's identity-management policy (e.g. forced SSO) | commercial | low | medium | Confirm with the client's IT / security stakeholders during stakeholder review (§4); document SSO as an explicit Phase 3 item | Engineering lead | Client IT raises SSO as a blocker before MVP release |
| R-05 | File-format edge cases (encoding, delimiter, oversize files) produce silent parse failures, eroding trust in the file-log status | operational | medium | medium | Surface a per-file bulk-error indicator (already in C-07); add explicit error rows to the file log; instrument a parse-failure counter | Engineering lead | Bulk-error rate exceeds 5% of files in any post-MVP week |
| R-06 | Stakeholder turnover changes the approver-side requirements mid-build | operational | low | medium | Keep the approvals-lead decision domains (§4) explicit and document each material change as a §14 milestone slip rationale | Product sponsor | Approvals lead role re-assigned before MVP release |

<!-- rev: run-1 2026-05-19 -->

---

## 12. Cross-functional dependencies

### 12.1 Internal team dependencies

| Team | What we need from them | By when | Status | Contact |
| --- | --- | --- | --- | --- |
| Backend / API team | Stable upload, file-log, transactions, approve, reject endpoints (per the brief's named routes) | MVP start | in-progress | Engineering lead |
| Design ops | Component-level design tokens for the table, drawer, and form patterns | MVP design freeze | not-started | Design ops contact (to be confirmed) |
| Compliance / legal | Sign-off on audit-trail shape and reject-note retention policy | Pre-MVP release | not-started | Compliance / audit (§4) |
| Operations training | Training materials and a brief switch-over note for both roles | MVP launch | not-started | Operations lead (§4) |

### 12.2 External / vendor dependencies

| Vendor / external party | What they provide | Contract status | Risk if unavailable | Backup plan |
| --- | --- | --- | --- | --- |
| Hosting provider for the prototype environment (e.g. AWS / Azure) | Hosted runtime for the prototype | n/a (using existing arrangement) | MVP demos slip | Local-only demo via the client-stub server |
| Upstream file producer(s) | Continued file delivery in the existing format | n/a (existing operational arrangement) | The file ingestion path has no input — entire MVP is blocked | Mock-data harness for the prototype phase |

<!-- rev: run-1 2026-05-19 -->

---

## 13. Release criteria

| ID | Criterion | Phase (→ §9.1) | How verified | Owner |
| --- | --- | --- | --- | --- |
| RC-01 | An Importer can complete an end-to-end file upload (drag-and-drop, name, submit, see file log row appear) on the hosted prototype | mvp | Stakeholder demo walkthrough | Operations lead |
| RC-02 | An Approver can approve and reject transactions (with mandatory note enforcement) and export the result as CSV in the hosted prototype | mvp | Stakeholder demo walkthrough | Approvals lead |
| RC-03 | Role-based UI gating is visibly correct: Importer cannot see approve/reject actions; Approver cannot see the upload entry-point | mvp | Manual test plan with both role accounts | Engineering lead |
| RC-04 | Compliance has reviewed the audit-trail shape (action, actor, timestamp, reject-note) and recorded sign-off | mvp | Compliance sign-off email referenced in §4 stakeholder record | Compliance / audit |
| RC-05 | Audit-trail surfacing in-app (Phase-2 scope) is usable by a compliance reviewer in a hosted environment | phase-2 | Stakeholder demo with compliance present | Compliance / audit |
| RC-06 | Saved filter presets persist across approver sessions | phase-2 | Manual test plan | Approvals lead |
| RC-07 | SSO integration completes a successful login round-trip in a client tenant | phase-3 | Tenant SSO test | Engineering lead |
| RC-08 | At least one custom export format beyond CSV is available end-to-end | phase-3 | Stakeholder demo | Approvals lead |

<!-- rev: run-1 2026-05-19 -->

---

## 14. Timeline & milestones

| Milestone | Phase (→ §9.1) | Target date | Confidence | Dependencies (→ §12) |
| --- | --- | --- | --- | --- |
| MVP design freeze | mvp | T+2 weeks | medium | Design ops, Approvals lead |
| MVP engineering complete | mvp | T+5 weeks | medium | Backend / API team |
| MVP internal beta with both roles | mvp | T+6 weeks | medium | Operations training, Compliance pre-review |
| MVP general availability (hosted prototype) | mvp | T+7 weeks | low | Hosting provider |
| Phase 2 design freeze (audit-trail in-app, saved filters) | phase-2 | T+9 weeks | low | Compliance / audit |
| Phase 2 release | phase-2 | T+11 weeks | low | Compliance / audit, Backend / API team |
| Phase 3 SSO / multi-tenant release | phase-3 | T+16 weeks | low | Engineering lead, Client IT |

**Critical path summary:** The MVP date is driven by backend endpoint readiness (file upload, transactions, approve, reject, file-log) and compliance pre-review of the audit-trail shape. Slip in either pushes the MVP general-availability milestone correspondingly.

<!-- rev: run-1 2026-05-19 -->

---
