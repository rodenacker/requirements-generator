# Consultant Answers

> Captured resolutions for every `[AI-SUGGESTED]` marker in `requirements/requirements-draft.md`. The consultant chose `accept-all-remaining-non-blocking` at the first Phase 2 batch, so every non-blocking item is recorded as `accepted-as-is` with the drafter's inferred value as the resolved value. There were zero blocking items; Phase 1 was skipped by construction.

### AI-001
- **Source location:** §1.6.row[abstract-service:binary-blob]
- **Original suggestion:** A binary blob storage tier for uploaded files and bulk-error files
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A binary blob storage tier for uploaded files and bulk-error files

### AI-002
- **Source location:** §1.7.row[client-state]
- **Original suggestion:** Client-side state management category — no specific recommendation
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Client-side state management category — no specific recommendation

### AI-003
- **Source location:** §1.7.row[search-filter]
- **Original suggestion:** in-memory index acceptable at ≤10⁴ records per file
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** in-memory index acceptable at ≤10⁴ records per file

### AI-004
- **Source location:** §1.7.row[file-upload]
- **Original suggestion:** binary blob storage tier required
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** binary blob storage tier required

### AI-005
- **Source location:** §1.7.row[export]
- **Original suggestion:** CSV-only at this stage
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** CSV-only at this stage

### AI-006
- **Source location:** §1.7.row[role-conditional]
- **Original suggestion:** Role-conditional rendering category — no specific recommendation
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Role-conditional rendering category — no specific recommendation

### AI-007
- **Source location:** §1.7.row[audit-viewer]
- **Original suggestion:** Audit-trail viewer category — no specific recommendation
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Audit-trail viewer category — no specific recommendation

### AI-008
- **Source location:** §1.7.row[notifications]
- **Original suggestion:** category-level only
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** category-level only

### AI-009
- **Source location:** §2.5.FileLog.Uploaded→Processing.effect
- **Original suggestion:** status badge advances to "Processing"
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** status badge advances to "Processing"

### AI-010
- **Source location:** §2.5.FileLog.Processing→Completed.effect
- **Original suggestion:** status badge advances to "Completed"; transactions become visible
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** status badge advances to "Completed"; transactions become visible

### AI-011
- **Source location:** §3.Importer.expertise
- **Original suggestion:** Intermediate — familiar with file-ingestion workflows
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Intermediate — familiar with file-ingestion workflows

### AI-012
- **Source location:** §3.Importer.frequency
- **Original suggestion:** Daily — one or more files per business day
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Daily — one or more files per business day

### AI-013
- **Source location:** §3.Importer.negative-drivers
- **Original suggestion:** Silent ingestion failures; unclear validation errors
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Silent ingestion failures; unclear validation errors

### AI-014
- **Source location:** §3.Approver.expertise
- **Original suggestion:** Senior — empowered to apply approve/reject decisions
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Senior — empowered to apply approve/reject decisions

### AI-015
- **Source location:** §3.Approver.frequency
- **Original suggestion:** Daily — reviewing the day's ingested transactions
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Daily — reviewing the day's ingested transactions

### AI-016
- **Source location:** §3.Approver.negative-drivers
- **Original suggestion:** Approving a wrong row; losing the rejection rationale
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Approving a wrong row; losing the rejection rationale

### AI-017
- **Source location:** §5.Authentication.role-conditional
- **Original suggestion:** Landing differs by role assignment
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Landing differs by role assignment

### AI-018
- **Source location:** §6.1.F-04.AC
- **Original suggestion:** A 200 response returns the user's profile fields (e.g. Username, Email, RolesString)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A 200 response returns the user's profile fields (e.g. Username, Email, RolesString)

### AI-019
- **Source location:** §6.1.F-21.AC
- **Original suggestion:** Requests without the cookie return 401
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Requests without the cookie return 401

### AI-020
- **Source location:** §6.3.UserNote.error
- **Original suggestion:** A reject reason is required
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A reject reason is required

### AI-021
- **Source location:** §6.3.FileSettingId.error
- **Original suggestion:** A file-setting id is required
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A file-setting id is required

### AI-022
- **Source location:** §6.3.FileSettingName.error
- **Original suggestion:** A file-setting name is required
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A file-setting name is required

### AI-023
- **Source location:** §6.3.FileName.error
- **Original suggestion:** A file name is required
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A file name is required

### AI-024
- **Source location:** §6.4.5.UI-08-UI-10.partial
- **Original suggestion:** Show the filter chips and a Clear-all action; copy references the active filter
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Show the filter chips and a Clear-all action; copy references the active filter

### AI-025
- **Source location:** §6.4.5.UI-09.permission-denied
- **Original suggestion:** Hide the action; on direct URL access show an in-page permission-denied banner naming the missing permission
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Hide the action; on direct URL access show an in-page permission-denied banner naming the missing permission

### AI-026
- **Source location:** §6.6.1.mfa
- **Original suggestion:** Not required at this stage
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Not required at this stage

### AI-027
- **Source location:** §6.6.2.tti
- **Original suggestion:** ≤ 2.0 s p95 time-to-interactive
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** ≤ 2.0 s

### AI-028
- **Source location:** §6.6.2.bundle
- **Original suggestion:** ≤ 300 KB gzipped initial bundle
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** ≤ 300 KB gzipped

### AI-029
- **Source location:** §6.6.2.render
- **Original suggestion:** ≤ 1.0 s p95 render at 10⁴ rows
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** ≤ 1.0 s p95 at 10⁴ rows

### AI-030
- **Source location:** §6.6.2.tmc
- **Original suggestion:** ≤ 1.5 s p95 time-to-meaningful-content
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** ≤ 1.5 s p95

### AI-031
- **Source location:** §6.6.5.keyboard
- **Original suggestion:** Keyboard-only path through Login → File Log Overview → Transaction Table → Approve/Reject/Export
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Keyboard-only path through Login → File Log Overview → Transaction Table → Approve/Reject/Export must be available

### AI-032
- **Source location:** §6.9.FileLog.audited-fields
- **Original suggestion:** CurrentStatus, LastChangedUser-equivalent (file process logs)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** CurrentStatus, LastChangedUser-equivalent (file process logs)

### AI-033
- **Source location:** §7.FileSetting.Direction
- **Original suggestion:** Inbound or outbound
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Inbound or outbound

### AI-034
- **Source location:** §10.data-volume
- **Original suggestion:** 10²–10⁴ transactions per file; 10³–10⁵ transactions retained per active FileLog
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** 10²–10⁴ transactions per file; 10³–10⁵ transactions retained per active FileLog

### AI-035
- **Source location:** §10.concurrency
- **Original suggestion:** 10¹–10² concurrent users across Importer and Approver roles
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** 10¹–10² concurrent users across Importer and Approver roles
