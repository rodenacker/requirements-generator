# Consultant Answers — Resolver Output

Resolved entries for every `[AI-SUGGESTED]` ID in `requirements/requirements-draft.md`. Rendered from `framework/state/resolver-answers.json` after self-validation.

---

### AI-001
- **Source location:** §1 Domain (also document header)
- **Original suggestion:** Financial services / back-office transaction processing
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm
- **Follow-ups:** none
- **Resolved value:** Financial services / back-office transaction processing

### AI-002
- **Source location:** §1 Business goal
- **Original suggestion:** Enforce a separation-of-duties workflow over batch-imported financial transactions so that no transaction reaches a downstream system without an Approver's explicit decision, while preserving a per-file audit trail of file logs, transaction status, and reject reasons.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm
- **Follow-ups:** none
- **Resolved value:** Enforce a separation-of-duties workflow over batch-imported financial transactions so that no transaction reaches a downstream system without an Approver's explicit decision, while preserving a per-file audit trail of file logs, transaction status, and reject reasons.

### AI-003
- **Source location:** §3 Importer / Role / job title
- **Original suggestion:** Operations clerk / data-ingest specialist
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### Importer)
- **Follow-ups:** none
- **Resolved value:** Operations clerk / data-ingest specialist

### AI-004
- **Source location:** §3 Importer / Expertise level
- **Original suggestion:** Comfortable with file-upload tools and tabular data; not a transaction reviewer
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### Importer)
- **Follow-ups:** none
- **Resolved value:** Comfortable with file-upload tools and tabular data; not a transaction reviewer

### AI-005
- **Source location:** §3 Importer / Stakes
- **Original suggestion:** Late or failed uploads delay the Approver queue and hold up downstream settlement
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### Importer)
- **Follow-ups:** none
- **Resolved value:** Late or failed uploads delay the Approver queue and hold up downstream settlement

### AI-006
- **Source location:** §3 Importer / Frequency of use
- **Original suggestion:** Daily, batch-driven (one or more uploads per business day)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### Importer)
- **Follow-ups:** none
- **Resolved value:** Daily, batch-driven (one or more uploads per business day)

### AI-007
- **Source location:** §3 Approver / Role / job title
- **Original suggestion:** Finance officer / authorised signatory
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### Approver)
- **Follow-ups:** none
- **Resolved value:** Finance officer / authorised signatory

### AI-008
- **Source location:** §3 Approver / Expertise level
- **Original suggestion:** Strong domain knowledge of transactions, reconciliation, and policy; modest tolerance for UI friction
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### Approver)
- **Follow-ups:** none
- **Resolved value:** Strong domain knowledge of transactions, reconciliation, and policy; modest tolerance for UI friction

### AI-009
- **Source location:** §3 Approver / Stakes
- **Original suggestion:** Approving an erroneous transaction causes downstream financial impact and audit exposure; rejecting valid ones causes operational delay
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm
- **Follow-ups:** none
- **Resolved value:** Approving an erroneous transaction causes downstream financial impact and audit exposure; rejecting valid ones causes operational delay.

### AI-010
- **Source location:** §3 Approver / Frequency of use
- **Original suggestion:** Several sessions per day; longer working sessions per file batch
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### Approver)
- **Follow-ups:** none
- **Resolved value:** Several sessions per day; longer working sessions per file batch

### AI-011
- **Source location:** §4.1 G-01 / UX-pattern pref
- **Original suggestion:** Single-step credentials
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### 4.1 Goals catalogue)
- **Follow-ups:** none
- **Resolved value:** Single-step credentials

### AI-012
- **Source location:** §4.1 G-02 / UX-pattern pref
- **Original suggestion:** Upload-with-progress
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### 4.1 Goals catalogue)
- **Follow-ups:** none
- **Resolved value:** Upload-with-progress

### AI-013
- **Source location:** §4.1 G-03 / UX-pattern pref
- **Original suggestion:** Sortable/filterable list
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### 4.1 Goals catalogue)
- **Follow-ups:** none
- **Resolved value:** Sortable/filterable list

### AI-014
- **Source location:** §4.1 G-07 / UX-pattern pref
- **Original suggestion:** CSV download
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### 4.1 Goals catalogue)
- **Follow-ups:** none
- **Resolved value:** CSV download

### AI-015
- **Source location:** §4.1 G-08 / UX-pattern pref
- **Original suggestion:** Multi-facet filtering with chips
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### 4.1 Goals catalogue)
- **Follow-ups:** none
- **Resolved value:** Multi-facet filtering with chips

### AI-016
- **Source location:** §5 Authentication / Role-conditional behaviour
- **Original suggestion:** A User holding both roles defaults to Approver landing with a role-switch control
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** corrected
- **Consultant answer:** Drop dual-role support; users hold exactly one role.
- **Follow-ups:** none
- **Resolved value:** A User holds exactly one of { Importer, Approver }. No role-switch control. Authentication routes deterministically by the User's single role: Importer → Upload + File Logs landing; Approver → File Logs landing. The User × Role cardinality is 1..1, not many-to-many.

### AI-017
- **Source location:** §5 Transaction Export / Steps
- **Original suggestion:** Browser downloads the CSV (download mechanism — direct browser download)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### Flow: Transaction Export (Approver))
- **Follow-ups:** none
- **Resolved value:** On Export click, the browser triggers a direct CSV download (no email/queue/async pickup pattern).

### AI-018
- **Source location:** §6.2 BR-09 (per-role amount threshold for step-up auth)
- **Original suggestion:** When an Approver attempts to Approve a Transaction whose amount exceeds a per-role threshold, then a step-up authentication is required.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm threshold rule
- **Follow-ups:**
    - Q: BR-09 threshold value (ZAR) above which step-up authentication is required for Approve.
    - A: ZAR 100 000
- **Resolved value:** BR-09: When an Approver attempts to Approve a Transaction whose Amount ≥ ZAR 100 000, then a step-up authentication is required before the status transitions to Approved. Below the threshold, no step-up is required (only the standard confirmation modal per GR-04).

### AI-019
- **Source location:** §6.3 Data + §7 Transaction / TransactionType
- **Original suggestion:** Surface TransactionType (`C` / `D`) as a labelled badge
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### 6.3 Data)
- **Follow-ups:** none
- **Resolved value:** TransactionType (`C` / `D`) is surfaced as a labelled badge (e.g., 'Credit' green, 'Debit' grey, paired with text per GR-16).

### AI-020
- **Source location:** §6.3 File Log columns
- **Original suggestion:** Setting Name surfaced as a column on the File Log table
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### 6.3 Data)
- **Follow-ups:** none
- **Resolved value:** File Log table includes a 'Setting Name' column alongside File Name, Process Date, Record Count, Status, and Bulk-Error indicator.

### AI-021
- **Source location:** §6.3 Reject Reason length
- **Original suggestion:** 1–500 characters
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all in batch (### 6.3 Data)
- **Follow-ups:** none
- **Resolved value:** Reject Reason (UserNote on rejection) length: 1–500 characters; required when status transitions to Rejected (BR-02).

### AI-022
- **Source location:** §6.4 Login form / Forgot password
- **Original suggestion:** A 'Forgot password' link is not included in this prototype
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining non-blocking
- **Follow-ups:** none
- **Resolved value:** Login form does not include a 'Forgot password' link in this prototype.

### AI-023
- **Source location:** §6.4 Transaction table / bulk selection
- **Original suggestion:** Bulk selection with Approve / Reject available to Approver
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm
- **Follow-ups:** none
- **Resolved value:** Bulk select with bulk Approve and bulk Reject is included for the Approver. Bulk Reject opens a single shared User Note dialog; the entered note is applied to every selected row. Bulk actions remain gated by BR-01 (only `Imported` rows participate) and BR-09 (any selected Transaction with Amount ≥ ZAR 100 000 forces step-up before the bulk Approve completes).

### AI-024
- **Source location:** §6.4 Notification badge counts
- **Original suggestion:** Notification badge counts (e.g., 'Files awaiting your decision') use the 99+ cap per GR-15
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining non-blocking
- **Follow-ups:** none
- **Resolved value:** Notification badge counts (e.g., 'Files awaiting your decision' for Approvers) use the 99+ cap per GR-15.

### AI-025
- **Source location:** §6.6.4 / POPIA scope
- **Original suggestion:** POPIA-aligned handling of personal data captured in transaction descriptions and account numbers; account numbers displayed in full to authorised roles, with no public-facing exposure of the system
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** dropped
- **Consultant answer:** Drop
- **Follow-ups:** none
- **Resolved value:** Compliance regime is not asserted for this prototype. Account numbers continue to be displayed in full (matching the input sample format `NNNN-NNNN-NNNN`); no public-facing exposure of the system is implied. Remove POPIA-specific copy from §6.6.4.

### AI-026
- **Source location:** §6.6.4 / Audit trail UI
- **Original suggestion:** Immutable audit trail for every Approve and Reject action capturing actor, timestamp, prior status, and (for rejection) the User Note; surfaced in UI as a per-Transaction history panel
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** corrected
- **Consultant answer:** Correct — backend only
- **Follow-ups:** none
- **Resolved value:** Audit capture (actor, timestamp, prior status, reject note) is server-side only and is NOT surfaced in this prototype's UI. No per-Transaction history panel, no detail-view audit drawer. Remove the corresponding UI bullet from §6.6.4 and from §6.4.

### AI-027
- **Source location:** §6.6.5 Accessibility target
- **Original suggestion:** WCAG 2.2 AA target across all interactive views
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining non-blocking
- **Follow-ups:** none
- **Resolved value:** WCAG 2.2 AA target across all interactive views.

### AI-028
- **Source location:** §7 Role / Enums
- **Original suggestion:** Role.Name constrained to { Importer, Approver } for this prototype
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm
- **Follow-ups:** none
- **Resolved value:** Role.Name is constrained to { Importer, Approver } for this prototype. No role-management UI is included; the API's role/page CRUD endpoints are out of scope for the prototype's screens.

### AI-029
- **Source location:** §8 Source UI references
- **Original suggestion:** No source UI references (screenshots, wireframes, existing-tool screens) were supplied with the brief; the prototype is greenfield from PrototypeBrief.md and openapi.json.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining non-blocking
- **Follow-ups:** none
- **Resolved value:** No source UI references (screenshots, wireframes, existing-tool screens) were supplied; the prototype is greenfield from PrototypeBrief.md and openapi.json.

### AI-030
- **Source location:** §10 Data volume
- **Original suggestion:** ~10²–10⁴ Transactions per File Log; tens of File Logs per business day; cumulative ~10⁵–10⁶ Transactions in a working window
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm
- **Follow-ups:** none
- **Resolved value:** ~10²–10⁴ Transactions per File Log; tens of File Logs per business day; cumulative ~10⁵–10⁶ Transactions in a working window.

### AI-031
- **Source location:** §10 Frequency
- **Original suggestion:** Multiple uploads per business day; review activity throughout the working day
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining non-blocking
- **Follow-ups:** none
- **Resolved value:** Multiple uploads per business day; review activity throughout the working day.

### AI-032
- **Source location:** §10 Concurrency
- **Original suggestion:** 5–20 concurrent users across both roles in a single tenant
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining non-blocking
- **Follow-ups:** none
- **Resolved value:** 5–20 concurrent users across both roles in a single tenant.
