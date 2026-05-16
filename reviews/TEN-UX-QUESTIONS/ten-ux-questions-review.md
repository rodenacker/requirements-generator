# 10 UX Questions — Transaction Import & Approval System

- **Domain:** Financial services / banking back-office
- **Generated:** 2026-05-16T13:55:30Z
- **Requirements SHA-256:** `6f9272bbb30d1dce025b843f5319e790bdaa5ac2a07103204bbea7144694f0ae`
- **Reviewer:** 10 UX Questions Review (experienced UX designer lens)

---

## Executive Summary

- **Total questions:** 10
  - Priority — Blocking: **2** · Major: **8** · Minor: **0**
- **Candidate pool size:** 50 (≤ 50)
- **Category coverage:** 6 of 8 (C2, C4, C5, C6, C7, C8)

> Priority legend: **blocking** — without an answer, the design cannot proceed (two or more plausible interpretations yield contradictory designs). **major** — an answer materially changes design direction; design can proceed with a stated default at the cost of re-design risk. **minor** — answer affects refinement only; a reasonable default produces an acceptable design.

> Source: `requirements/requirements.md` only. Categories: C1 Users & segmentation · C2 Context of use · C3 Goals & success signals · C4 Tasks, flows, decision points · C5 Data & content for decisions · C6 Errors, edge cases, recovery · C7 Collaboration & concurrency · C8 Trust, transparency, audit.

---

## Triage

Read this table top-to-bottom; UXQ-01 is the highest-priority question. The full question text and rationale for each entry is in the **Questions** section below.

| Rank | ID | Priority | Category | Anchor | Question (first line) |
|------|----|----------|----------|--------|------------------------|
| 1 | UXQ-01 | major | C2 Context of use | missing-section: context-of-use | In what physical environment do Approvers review transactions — private office, open-plan back-office, or branch counter… |
| 2 | UXQ-02 | major | C2 Context of use | missing-section: context-of-use | Are Approvers working against a daily cut-off, or is review steady-state with no externally imposed deadline? |
| 3 | UXQ-03 | blocking | C4 Tasks, flows, decision points | §5 | Can an Approver multi-select Imported transactions and approve them in one confirmation step, or is approval strictly… |
| 4 | UXQ-04 | blocking | C4 Tasks, flows, decision points | §5 | When multiple Imported transactions need rejecting for the same reason, can an Approver multi-select and supply one shared… |
| 5 | UXQ-05 | major | C5 Data & content for decisions | missing-section: trust-transparency | When an Approver clicks a transaction row, does a detail view open, and if so what does it show beyond the table columns? |
| 6 | UXQ-06 | major | C6 Errors, edge cases, recovery | §5 | When Approve fails server-side, does the status badge flip optimistically and revert, sit on a spinner until success, or… |
| 7 | UXQ-07 | major | C7 Collaboration & concurrency | missing-section: collaboration | How does an Approver know that new Imported transactions have arrived for review since their last visit? |
| 8 | UXQ-08 | major | C8 Trust, transparency, audit | §6.3 | Is the per-transaction change history visible to the Approver on a tab, side panel, or inline expandable row in the UI? |
| 9 | UXQ-09 | major | C8 Trust, transparency, audit | missing-section: trust-transparency | When an Approver re-opens a Rejected transaction days or weeks later, can they see the rejecter's identity and full… |
| 10 | UXQ-10 | major | C2 Context of use | missing-section: context-of-use | Is desktop the primary working surface for both roles, with mobile a fallback, or is tablet/mobile a first-class path? |

---

## Questions

### UXQ-01 — major — C2 Context of use — missing-section: context-of-use

> In what physical environment do Approvers review transactions — private office, open-plan back-office, or branch counter visible to customers or colleagues?

**Why this matters.** If Approvers work in a shared or customer-facing space, account numbers and amounts will need privacy treatment (last-4 masking, click-to-reveal) baked into the table, detail view, and export preview. If the environment is private, the same fields can render in plain view; retrofitting masking later forces a re-design of every transaction-data surface.

### UXQ-02 — major — C2 Context of use — missing-section: context-of-use

> Are Approvers working against a daily cut-off (e.g., end-of-business deadline by which the day's transactions must be approved for downstream consumption), or is review steady-state with no externally imposed deadline?

**Why this matters.** A daily cut-off justifies a queue header with a "X remaining before cut-off" countdown banner and an SLA-coloured row indicator on aging transactions. A steady-state review needs only a neutral count; the cut-off chrome would be noise.

### UXQ-03 — blocking — C4 Tasks, flows, decision points — §5

> When an Approver faces a queue of dozens of Imported transactions, can they select multiple rows and approve them in one confirmation step, or is approval strictly one-transaction-at-a-time as §6.1 ("individual transactions") implies?

**Why this matters.** Bulk approval requires a row-checkbox column, a bulk-action toolbar, and a multi-transaction confirmation modal — all visible on the table chrome. Strict single-action approval has none of that. The two table designs are not additive: adding bulk actions later means rebuilding the table's selection layer.

### UXQ-04 — blocking — C4 Tasks, flows, decision points — §5

> When multiple Imported transactions need to be rejected for the same reason (e.g., a whole file imported with the wrong settings), can an Approver multi-select and supply one shared rejection note, or must each rejection carry its own unique note per BR-02?

**Why this matters.** A shared-note bulk reject lets the Approver dispatch a problematic file in one flow with one note. Per-transaction notes force them through the reject modal N times. The two flows produce different shapes of the audit record and different reject-modal designs; the choice cannot be deferred until after the table chrome is built.

### UXQ-05 — major — C5 Data & content for decisions — missing-section: trust-transparency

> When an Approver clicks a transaction row, does a detail view open, and if so what does it show beyond the visible table columns — Description, source FileLog, audit history of who-acted-when, related transactions in the same file?

**Why this matters.** If a detail view is in scope, it needs a route or panel with its own field layout decisions (linear stack vs two-column, audit tab vs inline). If not, the row must self-contain every field the Approver needs to decide — driving column-pick decisions at the table level. The doc captures more fields on Transaction (§7) than the table shows (§5 Transaction Table), so something has to give.

### UXQ-06 — major — C6 Errors, edge cases, recovery — §5

> When an Approver clicks Approve and the simulated server returns a failure (or the request times out), does the status badge flip optimistically and revert on failure, sit on a spinner until success, or stay in Imported with an inline error toast offering retry?

**Why this matters.** BR-06 says the new status must appear without a manual refresh, but does not say at what point — before or after the server has confirmed. The choice between optimistic-revert, pessimistic-spinner, and pessimistic-toast-retry produces three distinct interaction designs and three different rollback experiences when something goes wrong.

### UXQ-07 — major — C7 Collaboration & concurrency — missing-section: collaboration

> How does an Approver know that new Imported transactions have arrived for review since their last visit — a queue badge in the primary navigation, an in-page banner on the Transaction Table, a notification panel, or only by manually checking the File Log dashboard?

**Why this matters.** Without an active notification surface, Approvers fall back to manual polling — viable but inefficient if the cadence is several uploads a day. A badge or banner is straightforward to add to the chrome but pre-supposes a "last-seen-cursor" state. The chosen surface affects both the navigation pattern and how the badge clears on dwell or click.

### UXQ-08 — major — C8 Trust, transparency, audit — §6.3

> Is the per-transaction change history (LastChangedUser, LastChangedDate, prior status transitions) visible to the Approver on a tab, side panel, or inline expandable row in the UI, or is it admin-only and reachable only through a separate audit screen?

**Why this matters.** §6.3 captures the audit fields but §5 and §6.4 do not name any user-facing surface that renders them. If the Approver needs to see who else has acted on a record (e.g., to avoid stepping on a colleague's review), the table or detail view needs an explicit audit slot. If audit is admin-only, the Approver's workspace stays simpler but cross-Approver coordination has no in-product surface.

### UXQ-09 — major — C8 Trust, transparency, audit — missing-section: trust-transparency

> When an Approver re-opens a Rejected transaction days or weeks after the original action, can they see the original rejecter's identity and the full UserNote rationale on the row or detail view, or is that information reachable only through a separate audit log?

**Why this matters.** Rejection rationale is the primary audit artefact per §6.2 BR-02; whether it lives on the transaction's UI surface or only in a back-office audit log changes whether the Approver workspace needs a detail view with an audit panel. The choice also affects how Rejected rows render in the table (compact note preview vs link-out to detail).

### UXQ-10 — major — C2 Context of use — missing-section: context-of-use

> Is desktop the primary working surface for both Importers and Approvers, with mobile a fallback for occasional checks, or is tablet/mobile expected to be a first-class path for any role? §6.4 names the 768 px table-to-card collapse but does not say whether the card view is a primary path or a rarely-used fallback.

**Why this matters.** If desktop-first, the Transaction Table can carry richer column sets and the mobile collapse is a safety net for the rare on-the-go check. If tablet/mobile is a real working surface (e.g., Approvers reviewing from a branch tablet), column-pick decisions and primary CTAs need to be optimised for touch-target sizing from the outset.

---

## Diagnostics

### Candidate pool

| Stat | Value |
|------|-------|
| Candidates generated (Step 3)            | 50              |
| Dropped: GR-NN match (Step 4)            | 3               |
| Dropped: PI-NN match (Step 4)            | 0               |
| Dropped: out-of-scope (Step 4)           | 0               |
| Surviving candidates after filter        | 47              |
| Selected (Step 5)                        | 10              |

### Category coverage

| Category                                  | Candidates generated | Candidates surviving filter | Selected |
|-------------------------------------------|----------------------|------------------------------|----------|
| C1 Users & segmentation                   | 6                    | 6                            | 0        |
| C2 Context of use                         | 6                    | 6                            | 3        |
| C3 Goals & success signals                | 6                    | 6                            | 0        |
| C4 Tasks, flows, decision points          | 8                    | 7                            | 2        |
| C5 Data & content for decisions           | 7                    | 7                            | 1        |
| C6 Errors, edge cases, recovery           | 6                    | 5                            | 1        |
| C7 Collaboration & concurrency            | 5                    | 5                            | 1        |
| C8 Trust, transparency, audit             | 6                    | 5                            | 2        |
| **Coverage of selected**                  | **—**                | **—**                        | **6 of 8** |

### Quality gates

| Gate | Result | Notes |
|------|--------|-------|
| 1. Exactly 10 questions in final output         | PASS | 10 selected |
| 2. Candidate pool size ≤ 50                     | PASS | 50 generated |
| 3. All priorities ∈ {blocking, major, minor}    | PASS | 2 blocking · 8 major · 0 minor |
| 4. All rationales are 1–3 sentences, non-empty  | PASS | every rationale 2–3 sentences |
| 5. All anchors valid or missing-section         | PASS | 5 §-anchors, 5 missing-section |
| 6. No question matches an active GR-NN          | PASS | 3 GR-matches dropped pre-selection (GR-02 ×1, GR-14 ×2) |
| 7. No question is out-of-scope                  | PASS | no matches |
| 8. Category coverage ≥ 5 of 8                   | PASS | 6 categories represented (C2, C4, C5, C6, C7, C8) |

### Override log

All quality gates passed; no override invoked.
