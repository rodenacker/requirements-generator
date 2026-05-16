# 10 BA Questions — Transaction Import & Approval System

- **Domain:** Financial services / banking back-office
- **Generated:** 2026-05-16T13:35:37Z
- **Requirements SHA-256:** `6f9272bbb30d1dce025b843f5319e790bdaa5ac2a07103204bbea7144694f0ae`
- **Reviewer:** 10 BA Questions Review (experienced Business Analyst lens, BABOK-aware)

---

## Executive Summary

- **Total questions:** 10
  - Priority — Blocking: **4** · Major: **6** · Minor: **0**
- **Candidate pool size:** 50 (≤ 50)
- **Category coverage:** 6 of 8 (C1, C2, C3, C4, C5, C7)

> Priority legend: **blocking** — without an answer, design / estimation / scope cannot proceed (two or more plausible interpretations would yield fundamentally different implementations). **major** — an answer materially changes direction; the team can proceed with a stated default while the stakeholder decides, at documented risk. **minor** — answer affects refinement only; a reasonable default produces an acceptable solution.

> Source: `requirements/requirements.md` only. Categories: C1 Problem & justification · C2 Stakeholders & users · C3 Success & acceptance criteria · C4 Scope & MVP boundaries · C5 Business rules & decisions · C6 Data, entities & integrations · C7 Edge cases & exception flows · C8 Assumptions, dependencies & sequencing.

---

## Triage

Read this table top-to-bottom; BAQ-01 is the highest-priority question. The full question text and rationale for each entry is in the **Questions** section below.

| Rank | ID | Priority | Category | Anchor | Question (first line) |
|------|----|----------|----------|--------|------------------------|
| 1 | BAQ-01 | blocking | C2 Stakeholders & users | §3 | Are there approval-limit tiers for Approvers, or do all Approvers have identical authority? |
| 2 | BAQ-02 | blocking | C5 Business rules & decisions | §6.5 | Is the approval workflow single-stage, or does "two-stage human review" name a maker/checker pattern with two separate sign-offs? |
| 3 | BAQ-03 | blocking | C5 Business rules & decisions | §6.2 | Once a transaction is Approved or Rejected, is the decision reversible, by whom, and under what conditions? |
| 4 | BAQ-04 | blocking | C7 Edge cases & exception flows | §5 | When a file is parsed and 80% of records succeed but 20% fail validation, what is the business policy? |
| 5 | BAQ-05 | major | C1 Problem & justification | §1 | What are the system's anti-goals — what is it explicitly NOT trying to do? |
| 6 | BAQ-06 | major | C1 Problem & justification | §1 | What is the target reduction in import errors, manual review time, or approval cycle time that the business would call success at year-1? |
| 7 | BAQ-07 | major | C2 Stakeholders & users | §3 | Who within the business owns sign-off authority on the requirements doc, persona definitions, the RBAC matrix, and the approval-workflow stages? |
| 8 | BAQ-08 | major | C3 Success & acceptance criteria | §4.1 | What measurable threshold makes each §4.1 goal "successful"? |
| 9 | BAQ-09 | major | C4 Scope & MVP boundaries | §6.1 | Is bulk approve / bulk reject explicitly out of scope, deferred to a future phase, or implied for the MVP but not yet documented? |
| 10 | BAQ-10 | major | C5 Business rules & decisions | §9 | Who owns the FileSetting lifecycle, and is a FileSetting administration UI in scope or an external dependency? |

---

## Questions

### BAQ-01 — blocking — C2 Stakeholders & users — §3

> §3 names "Approver" as a single persona without segmentation — are there approval-limit tiers (e.g., junior approver up to ZAR X, senior approver above), or do all Approvers have identical authority?

**Why this matters.** Approval-limit tiers fundamentally change the §6.5 RBAC matrix (BR-01 currently gates only on Status, not Amount), introduce a referral workflow when a transaction exceeds a tier's limit, and require a per-tier limit field that the data model does not yet carry. Until the tier policy is settled, neither the RBAC matrix nor the approval flow can be finalised for design or estimation.

### BAQ-02 — blocking — C5 Business rules & decisions — §6.5

> §1 describes "a two-stage human review" but BR-01..BR-07 imply a single Approver per transaction — is the approval workflow single-stage (one Approver = final), or does "two-stage" name a maker/checker pattern with two separate sign-offs?

**Why this matters.** Single-stage and two-stage approvals require fundamentally different §6.5 RBAC entries, transaction-status enums (§2.3 currently lists only Imported / Approved / Rejected), queue-routing logic, and audit trails. The §1 wording currently contradicts the rule set in §6.2, and the doc cannot be implemented until the contradiction is resolved.

### BAQ-03 — blocking — C5 Business rules & decisions — §6.2

> Once a transaction's status is Approved or Rejected, is the decision reversible — by the same Approver, by a different Approver, or by a separate role — and if so, under what business conditions?

**Why this matters.** Reversibility introduces an additional status transition (Approved → Imported, or a new Reversed state), overrides BR-01's status gate on Approve / Reject row actions, and creates a separate audit-trail surface with reversal-reason capture. Without an answer the team cannot scope the approval lifecycle or its audit shape, and §6.6.4 retention scope is left undefined.

### BAQ-04 — blocking — C7 Edge cases & exception flows — §5

> When a file is parsed and 80% of records succeed but 20% fail validation, what is the business policy — accept the parsed records and surface failures separately, reject the whole file until it is clean, or escalate to operations?

**Why this matters.** Accept-partial persists transactions per File Log with mixed parsed / unparsed states; reject-whole means no transactions exist until 100% parse; escalate adds a third workflow and an operator role. The §2.3 File Log lifecycle, the §6.3 data persistence rules, and the §5 File Upload exception path all differ by choice.

### BAQ-05 — major — C1 Problem & justification — §1

> §1 declares the business goal as "a controlled, file-driven pipeline" but does not state anti-goals — is the system explicitly NOT trying to do real-time fraud detection, ledger posting, or reconciliation, and is there an authoritative anti-goal list the team should treat as out-of-scope?

**Why this matters.** Without stated anti-goals, the team risks absorbing adjacent functionality during build (e.g., adding fraud-flag fields on Transaction, reconciliation reports, ledger-side effects). A short anti-goal list keeps scope tight and prevents downstream stakeholders from assuming the system covers responsibilities it does not.

### BAQ-06 — major — C1 Problem & justification — §1

> §1 describes a business goal but does not quantify the expected outcome — what is the target reduction in import errors, manual review time, or approval cycle time that the business would call success at year-1?

**Why this matters.** Without a quantified outcome target, the §4.1 quality signals (Speed-to-confidence, Throughput, Decision confidence, At-a-glance status) have no testable threshold. The team can build to specification but cannot prove the system has solved the business problem, and §6.6.2 performance targets remain inferred rather than business-anchored.

### BAQ-07 — major — C2 Stakeholders & users — §3

> Who within the business owns sign-off authority on this requirements doc — and specifically on changes to the persona definitions, the §6.5 RBAC matrix, and the approval-workflow stages — by name or by role?

**Why this matters.** With no named sign-off owner, every requirement change defaults to whoever is in the room, which produces inconsistent priorities and re-litigated decisions. The named owner is also the routing point for the blocking-priority questions surfaced by this review.

### BAQ-08 — major — C3 Success & acceptance criteria — §4.1

> §4.1 names quality signals per goal (Speed-to-confidence, Throughput, Decision confidence, At-a-glance status) but does not quantify them — what measurable threshold makes each goal "successful" (e.g., upload feedback in ≤ N seconds, ≥ N transactions approved per Approver per hour)?

**Why this matters.** Quality signals without thresholds cannot drive acceptance criteria for §6.1 functional requirements or anchor the inferred §6.6.2 performance targets to business expectations. The team will build to assumed thresholds, and a year-1 success review will have no objective signal of whether the system is performing acceptably.

### BAQ-09 — major — C4 Scope & MVP boundaries — §6.1

> §6.1 lists approve and reject as one-transaction-at-a-time, and the modal-confirm pattern in §5 confirms it — is bulk approve / bulk reject explicitly out of scope for this release, deferred to a future phase, or implied for the MVP but not yet documented?

**Why this matters.** With approval volumes potentially 10²–10⁴ transactions per file (§10) and concurrency stated as ≈ 1 Approver active at a time (§10), one-at-a-time approval may not be operationally viable. The decision changes the §5 flow, the BR set, the audit trail per decision, and the throughput target in §4.1 G-02.

### BAQ-10 — major — C5 Business rules & decisions — §9

> §9 names "FileSetting" as a configuration record referenced by FileSettingId at upload time, and §7 File Log carries SettingId / SettingName, but no entity definition or management flow appears for FileSetting itself — who owns the FileSetting lifecycle (add, edit, retire), and is a FileSetting administration UI in scope for this project or an external dependency?

**Why this matters.** A missing FileSetting management surface either adds a whole admin subsystem to this build (with its own RBAC, screens, and entity model) or designates a separate team's deliverable as a prerequisite. Either answer changes the project's scope and its sequencing relative to other workstreams.

---

## Diagnostics

### Candidate pool

| Stat | Value |
|------|-------|
| Candidates generated (Step 3)            | 50 (≤ 50)       |
| Dropped: GR-NN match (Step 4)            | 0               |
| Dropped: PI-NN match (Step 4)            | 1               |
| Dropped: out-of-scope (Step 4)           | 0               |
| Dropped: UX-lens (Step 4)                | 3               |
| Surviving candidates after filter        | 46              |
| Selected (Step 5)                        | 10              |

### Category coverage

| Category                                       | Candidates generated | Candidates surviving filter | Selected |
|------------------------------------------------|----------------------|------------------------------|----------|
| C1 Problem & justification                     | 6                    | 6                            | 2        |
| C2 Stakeholders & users                        | 6                    | 5                            | 2        |
| C3 Success & acceptance criteria               | 6                    | 6                            | 1        |
| C4 Scope & MVP boundaries                      | 6                    | 4                            | 1        |
| C5 Business rules & decisions                  | 7                    | 7                            | 3        |
| C6 Data, entities & integrations               | 7                    | 6                            | 0        |
| C7 Edge cases & exception flows                | 7                    | 7                            | 1        |
| C8 Assumptions, dependencies & sequencing      | 5                    | 5                            | 0        |
| **Coverage of selected**                       | **—**                | **—**                        | **6 of 8** |

### Quality gates

| Gate | Result | Notes |
|------|--------|-------|
| 1. Exactly 10 questions in final output         | PASS | 10 selected |
| 2. Candidate pool size ≤ 50                     | PASS | 50 generated |
| 3. All priorities ∈ {blocking, major, minor}    | PASS | 4 blocking, 6 major, 0 minor |
| 4. All rationales are 1–3 sentences, non-empty  | PASS | All within bounds |
| 5. All anchors valid or missing-section         | PASS | All 10 anchor to §N or §N.N present in the doc |
| 6. No question matches an active GR-NN          | PASS | 0 matches |
| 7. No question is out-of-scope                  | PASS | 0 matches |
| 8. Category coverage ≥ 5 of 8                   | PASS | 6 of 8 (C1, C2, C3, C4, C5, C7) |
| 9. No UX-lens overlap                           | PASS | 0 matches |

### Override log

All quality gates passed; no override invoked.
