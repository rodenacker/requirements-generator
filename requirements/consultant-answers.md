# Consultant Answers — Transaction Import & Approval System

> Resolutions of every `[AI-SUGGESTED]` marker in `requirements/requirements-draft.md`. Rendered from `framework/state/resolver-answers.ndjson` after resolver self-validation passed. Phase 1 (blocking) resolved individually; Phase 2 (non-blocking) accepted in bulk via `accept-all-remaining-non-blocking`.

## Phase 1 — Blocking

### AI-011
- **Source location:** §6.2 BR-08.Acceptance criteria
- **Original suggestion:** the system shall display the Status mapped from LastExecutedActivityName per the activity-name-to-status mapping
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Accept as drafted
- **Follow-ups:** none
- **Resolved value:** File Status is derived from LastExecutedActivityName via an activity-name-to-status mapping; in the prototype, File Log fixtures carry the Status value directly (Uploaded/Processing/Completed/Failed) and the real activity-name-to-status mapping is deferred to the application build.

### AI-019
- **Source location:** §10 Data volume.Value
- **Original suggestion:** ~20 transactions per imported file; no corpus-stated overall cap, so a client-side band of 10^2–10^4 retained transactions is assumed
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Accept 10^2–10^4 band
- **Follow-ups:** none
- **Resolved value:** ~20 transactions per imported file; retained-transaction band 10^2–10^4; UI uses client-side pagination over the full list (no virtualization required at this scale).

## Phase 2 — Non-blocking (accepted as drafted)

### AI-001
- **Source location:** §1.7 row[Client-side state management].Recommendation
- **Original suggestion:** Client-side state management driving §6.1 F-06/F-07/F-08; recommendation blank
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Client-side state management capability row driving F-06/F-07/F-08; no specific recommendation.

### AI-002
- **Source location:** §1.7 row[Client-side search / filtering].Recommendation
- **Original suggestion:** in-memory index acceptable at this volume
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Client-side search / filtering; in-memory index acceptable at this volume.

### AI-003
- **Source location:** §1.7 row[File upload / binary blob handling].Recommendation
- **Original suggestion:** binary blob storage tier required
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** File upload / binary blob handling; binary blob storage tier required (application build).

### AI-004
- **Source location:** §1.7 row[Export rendering capability].Recommendation
- **Original suggestion:** Export rendering capability driving §6.1 F-11/§6.7 RPT-02; recommendation blank
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Export rendering capability driving F-11/RPT-02; no specific recommendation.

### AI-005
- **Source location:** §1.7 row[Notification delivery surface].Recommendation
- **Original suggestion:** in-app channel
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Notification delivery surface; in-app channel.

### AI-006
- **Source location:** §1.7 row[Role-conditional rendering].Recommendation
- **Original suggestion:** Role-conditional rendering driving §6.5/§6.1 F-02; recommendation blank
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Role-conditional rendering driving the RBAC matrix and F-02; no specific recommendation.

### AI-007
- **Source location:** §2.5 File Log row[Uploaded → Processing].Trigger
- **Original suggestion:** backend processing begins (out-of-FE-scope context)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** File Log Uploaded -> Processing trigger: backend processing begins (out-of-FE-scope context; FE displays resulting status).

### AI-008
- **Source location:** §2.5 File Log row[Processing → Completed].Trigger
- **Original suggestion:** backend processing succeeds (out-of-FE-scope context)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** File Log Processing -> Completed trigger: backend processing succeeds (out-of-FE-scope context).

### AI-009
- **Source location:** §2.5 File Log row[Processing → Failed].Trigger
- **Original suggestion:** backend processing fails (out-of-FE-scope context)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** File Log Processing -> Failed trigger: backend processing fails (out-of-FE-scope context); user-facing recovery flow unspecified.

### AI-010
- **Source location:** §6.1 F-16.Acceptance criteria
- **Original suggestion:** the system shall verify session validity and render the authenticated user's welcome
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** F-16 acceptance criterion: when the application loads, the system shall verify session validity and render the authenticated user's welcome.

### AI-012
- **Source location:** §6.3 Transaction.Amount.Rule
- **Original suggestion:** Amount must be a number
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Transaction.Amount inline validation: Amount must be a number.

### AI-013
- **Source location:** §6.6.1 Account lockout messaging.Value
- **Original suggestion:** Generic locked-account message after repeated failed logins
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Account lockout messaging: generic locked-account message after repeated failed logins.

### AI-014
- **Source location:** §6.6.1 MFA prompt scope.Value
- **Original suggestion:** No MFA prompt in the MVP
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** MFA prompt scope: no MFA prompt in the MVP.

### AI-015
- **Source location:** §6.6.2 Time to interactive (p95).Target
- **Original suggestion:** p95 ≤ 2.5 s
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Time to interactive (p95): p95 <= 2.5 s.

### AI-016
- **Source location:** §6.6.2 Initial bundle size budget.Target
- **Original suggestion:** ≤ 300 KB gzipped
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Initial bundle size budget: <= 300 KB gzipped.

### AI-017
- **Source location:** §6.6.2 Render budget for largest list/table.Target
- **Original suggestion:** p95 ≤ 500 ms for the transaction table
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Render budget for largest list/table: p95 <= 500 ms for the transaction table.

### AI-018
- **Source location:** §6.6.2 Time to meaningful content.Target
- **Original suggestion:** ≤ 1.5 s
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Time to meaningful content: <= 1.5 s.

### AI-020
- **Source location:** §10 Frequency.Value
- **Original suggestion:** Daily file imports (one or more files per business day)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Frequency: daily file imports (one or more files per business day).

### AI-021
- **Source location:** §10 Concurrency.Value
- **Original suggestion:** A small team of Importers and Approvers (10^1 order)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Concurrency: a small team of Importers and Approvers (10^1 order).
