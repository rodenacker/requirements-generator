# Consultant Answers

> Resolutions for every `[AI-SUGGESTED]` marker in `requirements/requirements-draft.md`. Rendered once, after Phase 1 (blocking) and Phase 2 (non-blocking) Q&A and the resolver's self-validation passed.

---

### AI-001
- **Source location:** §1 Business goal
- **Original suggestion:** Provide an auditable approval trail for every imported transaction, enforce role-segregation between upload and approval, and make rejection grounds explicit so downstream reconciliation has a documented reason for every non-approval.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Provide an auditable approval trail for every imported transaction, enforce role-segregation between upload and approval, and make rejection grounds explicit so downstream reconciliation has a documented reason for every non-approval.

---

### AI-002
- **Source location:** §3 Importer · Role / job title
- **Original suggestion:** Operations user responsible for getting transaction files into the system
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Operations user responsible for getting transaction files into the system

---

### AI-003
- **Source location:** §3 Approver · Role / job title
- **Original suggestion:** Senior operations user / financial controller responsible for transaction decisions
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Senior operations user / financial controller responsible for transaction decisions

---

### AI-004
- **Source location:** §4.2 Importer story 'retry validation' · Objective
- **Original suggestion:** Re-trigger validation against the existing File Log row.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Re-trigger validation against the existing File Log row.

---

### AI-005
- **Source location:** §5 Flow: Authenticate · Role-conditional behaviour
- **Original suggestion:** Importer lands on Upload page; Approver lands on Transactions page.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Importer lands on Upload page; Approver lands on Transactions page.

---

### AI-006
- **Source location:** §5 Flow: Export Transactions · Steps (CSV filename pattern)
- **Original suggestion:** Trigger browser download with timestamped filename `transactions_<YYYY-MM-DD>_<HHmm>.csv`.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Trigger browser download with timestamped filename `transactions_<YYYY-MM-DD>_<HHmm>.csv`.

---

### AI-007
- **Source location:** §6.2 BR-05 (audit trail UserNote)
- **Original suggestion:** When a transaction is rejected, then the recorded UserNote must accompany the status change in the audit trail.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** When a transaction is rejected, then the recorded UserNote must accompany the status change in the audit trail.

---

### AI-008
- **Source location:** §6.2 BR-07 (Processing-state row affordance)
- **Original suggestion:** When a File Log is in Processing state, then the row must show a non-clickable in-progress indicator and not allow drill-through into Transactions yet.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** When a File Log is in Processing state, then the row must show a non-clickable in-progress indicator and not allow drill-through into Transactions yet.

---

### AI-009
- **Source location:** §6.2 BR-10 (re-auth + filter preservation)
- **Original suggestion:** When a user's session reaches the §6.6.1 idle timeout, then a re-auth prompt must replace the screen content while preserving the active Filter Set on resume.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** When a user's session reaches the §6.6.1 idle timeout, then a re-auth prompt must replace the screen content while preserving the active Filter Set on resume.

---

### AI-010
- **Source location:** §6.6.4 POPIA consent banner
- **Original suggestion:** POPIA (South African Protection of Personal Information Act) — drives consent banner on first login and PII handling for Account Number / Description fields.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** POPIA (South African Protection of Personal Information Act) — drives consent banner on first login and PII handling for Account Number / Description fields.

---

### AI-011
- **Source location:** §6.6.4 Audit fields on detail
- **Original suggestion:** Audit fields visible on transaction detail: LastChangedUser, LastChangedDate, UserNote (if Rejected).
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Audit fields visible on transaction detail: LastChangedUser, LastChangedDate, UserNote (if Rejected).

---

### AI-012
- **Source location:** §6.6.5 WCAG target
- **Original suggestion:** WCAG 2.2 AA.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** WCAG 2.2 AA.

---

### AI-013
- **Source location:** §6.6.5 Keyboard support
- **Original suggestion:** Keyboard support: full keyboard navigation including row-level Approve / Reject and modal flows.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Keyboard support: full keyboard navigation including row-level Approve / Reject and modal flows.

---

### AI-014
- **Source location:** §7 Transaction · Reference pattern
- **Original suggestion:** Reference: non-empty; expected pattern `TXN-YYYYMMDD-NNNN` (sample format).
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Reference: non-empty; expected pattern `TXN-YYYYMMDD-NNNN` (sample format).

---

### AI-015
- **Source location:** §10 Volumes · Data volume
- **Original suggestion:** 10²–10⁴ Transactions retained over 90 days (≈ 100 – 10 000 active rows; sample shows ~150 / day)
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** 10²–10⁴ Transactions retained over 90 days (≈ 100 – 10 000 active rows; sample shows ~150 / day)

---

### AI-016
- **Source location:** §10 Volumes · Frequency
- **Original suggestion:** 1–10 file uploads per day; review cycle daily within business hours
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** 1–10 file uploads per day; review cycle daily within business hours

---

### AI-017
- **Source location:** §10 Volumes · Concurrency
- **Original suggestion:** 5–20 concurrent users (small ops team)
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** 5–20 concurrent users (small ops team)
