# Consultant Answers

Resolutions for every [AI-SUGGESTED] marker in requirements/requirements-draft.md. Produced by the requirements-resolver agent.

### AI-001
- **Source location:** ## 1. Application context | draft line 39
- **Original suggestion:** **Domain:** financial transaction management [AI-SUGGESTED: AI-001 | blocking]
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Mostly correct, but the approval process is done by one person only
- **Follow-ups:**
    - Q: Dual-control framing clarification
      A: Approval is done by one Approver only -- not dual-approver. AI-002 business-goal text must be corrected to remove two-person approval / dual-control phrasing. (action: ask)
- **Resolved value:** financial transaction management

### AI-002
- **Source location:** ## 1. Application context | draft line 41
- **Original suggestion:** **Business goal:** Provide controlled file-based transaction ingestion with auditable two-person approval to reduce manual processing errors and enforce dual-control over financial postings. [AI-SUGGESTED: AI-002 | non-blocking]
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** corrected
- **Consultant answer:** review-individually -> confirm corrected text
- **Follow-ups:**
    - Q: Final wording confirmation
      A: Confirm corrected single-Approver text (action: ask)
- **Resolved value:** Provide controlled file-based transaction ingestion with single-Approver review of each transaction to reduce manual processing errors and produce an auditable transaction-decision trail.

### AI-003
- **Source location:** ## 1.5 Scope | draft line 54
- **Original suggestion:** | Out | server-side file parsing internals [AI-SUGGESTED: AI-003 | non-blocking], backend identity provider implementation [AI-SUGGESTED: AI-004 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-004
- **Source location:** ## 1.5 Scope | draft line 54
- **Original suggestion:** | Out | server-side file parsing internals [AI-SUGGESTED: AI-003 | non-blocking], backend identity provider implementation [AI-SUGGESTED: AI-004 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-005
- **Source location:** ## 1.5 Scope | draft line 55
- **Original suggestion:** | Deferred | bulk file setting configuration UI [AI-SUGGESTED: AI-005 | non-blocking], scheduled / unattended file imports [AI-SUGGESTED: AI-006 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-006
- **Source location:** ## 1.5 Scope | draft line 55
- **Original suggestion:** | Deferred | bulk file setting configuration UI [AI-SUGGESTED: AI-005 | non-blocking], scheduled / unattended file imports [AI-SUGGESTED: AI-006 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-007
- **Source location:** ## 1.7 Architectural implications | draft line 81
- **Original suggestion:** | Client-side search / filtering | → §6.1 F-21 / → §6.7 RPT-01 | in-memory index acceptable given ≤10⁴ records per file [AI-SUGGESTED: AI-007 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-008
- **Source location:** ## 1.7 Architectural implications | draft line 82
- **Original suggestion:** | File upload / binary blob handling | → §6.1 F-04 | binary blob storage tier required [AI-SUGGESTED: AI-008 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-009
- **Source location:** ### 2.1 Concepts | draft line 102
- **Original suggestion:** | Role | persistent | A named bundle of access permissions assigned to one or more Users. [AI-SUGGESTED: AI-009 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-010
- **Source location:** ### 2.2 Relationships | draft line 113
- **Original suggestion:** - User **holds** Role [1..* per User] [AI-SUGGESTED: AI-010 | non-blocking]
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-011
- **Source location:** #### File Log | draft line 125
- **Original suggestion:** | Key invariants   | A File Log cannot transition to Completed while any contained Transaction is still being processed. [AI-SUGGESTED: AI-011 | blocking] |
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** A File Log cannot transition to Completed while any contained Transaction is still being processed.

### AI-012
- **Source location:** #### File Log | draft line 206
- **Original suggestion:** | Uploaded → Processing | server begins extracting transactions from the uploaded file [SRC: C-030] | the file has been received by the backend [SRC: C-031] | the File Log row shows status Processing in the file log list [AI-SUGGESTED: AI-012 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-013
- **Source location:** #### File Log | draft line 207
- **Original suggestion:** | Processing → Completed | all transactions extracted and persisted [AI-SUGGESTED: AI-013 | non-blocking] | → §6.2 BR-01 [AI-SUGGESTED: AI-014 | non-blocking] | the File Log row shows status Completed and the file summary becomes available [SRC: C-032] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-014
- **Source location:** #### File Log | draft line 207
- **Original suggestion:** | Processing → Completed | all transactions extracted and persisted [AI-SUGGESTED: AI-013 | non-blocking] | → §6.2 BR-01 [AI-SUGGESTED: AI-014 | non-blocking] | the File Log row shows status Completed and the file summary becomes available [SRC: C-032] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-015
- **Source location:** #### File Log | draft line 208
- **Original suggestion:** | Processing → Failed | extraction encountered an unrecoverable error [SRC: C-033] | → §6.2 BR-02 [AI-SUGGESTED: AI-015 | non-blocking] | the File Log row shows status Failed and a retry-validation action becomes available [SRC: C-034] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-016
- **Source location:** ### 4.1 Goals catalogue | draft line 259
- **Original suggestion:** | G-01 | Successfully import transaction files for downstream approval [SRC: C-044] | uploads visibly succeed; record counts match expectation; processing status is observable [AI-SUGGESTED: AI-016 | non-blocking] | top-level | — | — |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-017
- **Source location:** ### 4.1 Goals catalogue | draft line 260
- **Original suggestion:** | G-02 | Maintain control over which transactions are approved and which are rejected with reason [SRC: C-045] | each transaction has a deliberate decision; rejected transactions carry a captured reason; status changes are immediate [AI-SUGGESTED: AI-017 | non-blocking] | top-level | — | — |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-018
- **Source location:** ### 4.1 Goals catalogue | draft line 263
- **Original suggestion:** | G-05 | Locate specific transactions and files quickly across the working set [SRC: C-006] | filter and search return results within a perceptibly short time; active filters are visible [AI-SUGGESTED: AI-018 | non-blocking] | interaction-level | — | — |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-019
- **Source location:** ### Flow: Approve Transaction | draft line 417
- **Original suggestion:** | Exception paths            | {transaction is no longer in Imported state when confirm is invoked → inline message that the action is no longer applicable → user re-opens the transaction or applies a different filter} [AI-SUGGESTED: AI-019 | blocking] |
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** transaction is no longer in Imported state when confirm is invoked -> inline message that the action is no longer applicable -> user re-opens the transaction or applies a different filter

### AI-020
- **Source location:** ### Flow: Reject Transaction | draft line 428
- **Original suggestion:** | Exception paths            | {note is empty → inline required-field error message → user enters a non-empty note} [STANDARD-RULE: GR-06]; {transaction is no longer in Imported state when submit is invoked → inline message that the action is no longer applicable → user re-opens the transaction or applies a different filter} [AI-SUGGESTED: AI-020 | blocking] |
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** transaction is no longer in Imported state when submit is invoked -> inline message that the action is no longer applicable -> user re-opens the transaction or applies a different filter

### AI-021
- **Source location:** ### 6.1 Functional | draft line 473
- **Original suggestion:** | F-02 | The system signs the user out and invalidates the active session. [SRC: C-092] | Given the user is signed in, when they invoke logout, then the active session is invalidated and the user is returned to the login surface. [AI-SUGGESTED: AI-021 | non-blocking] | stated / → §6.10 |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-022
- **Source location:** ### 6.1 Functional | draft line 477
- **Original suggestion:** | F-06 | The system retrieves per-File-Log process log entries for a specific LogId. [SRC: C-096] | Given the user opens process detail for a specific File Log, when the entries are requested, then the system returns the activity history for that File Log. [AI-SUGGESTED: AI-022 | non-blocking] | stated / → §6.10 |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-023
- **Source location:** ### 6.1 Functional | draft line 478
- **Original suggestion:** | F-07 | The system supports downloading the parsed data file for a File Log by LogId. [SRC: C-097] | Given the user requests the parsed data file for a File Log, when the request is invoked, then the file content is returned as a binary stream. [AI-SUGGESTED: AI-023 | non-blocking] | stated / → §6.10 |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-024
- **Source location:** ### 6.1 Functional | draft line 479
- **Original suggestion:** | F-08 | The system supports downloading the original uploaded file for a File Log by FileLogId. [SRC: C-098] | Given the user requests the original uploaded file, when the request is invoked, then the file content is returned as a binary stream. [AI-SUGGESTED: AI-024 | non-blocking] | stated / → §6.10 |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-025
- **Source location:** ### 6.1 Functional | draft line 488
- **Original suggestion:** | F-17 | The system lists, creates, updates, and deletes Users (administrative scope). [SRC: C-110] | Given an administrator invokes user-management operations, when each operation is submitted, then the system reflects the resulting User set and the operating user's identity is recorded on each change. [AI-SUGGESTED: AI-025 | non-blocking] | stated / → §6.10 |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-026
- **Source location:** ### 6.1 Functional | draft line 489
- **Original suggestion:** | F-18 | The system lists, creates, updates, and deletes Roles, including Role-to-Page assignment (administrative scope). [SRC: C-111] | Given an administrator invokes role-management operations, when each operation is submitted, then the system reflects the resulting Role set and Page assignments. [AI-SUGGESTED: AI-026 | non-blocking] | stated / → §6.10 |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-027
- **Source location:** ### 6.4 UI feature needs | draft line 542
- **Original suggestion:** | UI-11 | The application chrome shows the authenticated user's name and offers a logout affordance. [SRC: C-094] | → §6.1 F-03 / → §6.1 F-02 | The chrome reflects the authenticated user; invoking logout invalidates the session and returns the user to the login surface. [AI-SUGGESTED: AI-027 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-028
- **Source location:** #### 6.4.5 Edge, empty & error states | draft line 563
- **Original suggestion:** | → UI-07                  | error | Export failure surfaces an actionable error message; the action remains invokable. [AI-SUGGESTED: AI-028 | non-blocking] | User retries the export. [AI-SUGGESTED: AI-029 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-029
- **Source location:** #### 6.4.5 Edge, empty & error states | draft line 563
- **Original suggestion:** | → UI-07                  | error | Export failure surfaces an actionable error message; the action remains invokable. [AI-SUGGESTED: AI-028 | non-blocking] | User retries the export. [AI-SUGGESTED: AI-029 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-030
- **Source location:** #### 6.6.1 Session UX | draft line 589
- **Original suggestion:** | Account lockout messaging | After 5 failed login attempts the account is temporarily locked and an in-page message instructs the user to retry after 15 minutes or contact support. [AI-SUGGESTED: AI-030 | blocking] | inferred |
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** corrected
- **Consultant answer:** mostly - 5-attempt lockout is not needed
- **Follow-ups:** none
- **Resolved value:** No account-lockout messaging in the initial scope; failed login attempts surface the standard generic credentials-incorrect message only.

### AI-031
- **Source location:** #### 6.6.2 Frontend performance budgets | draft line 596
- **Original suggestion:** | Time to interactive (p95)                             | p95 ≤ 2.0 s [AI-SUGGESTED: AI-031 | non-blocking] | inferred |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-032
- **Source location:** #### 6.6.2 Frontend performance budgets | draft line 597
- **Original suggestion:** | Initial bundle size budget                            | ≤ 300 KB gzipped [AI-SUGGESTED: AI-032 | non-blocking] | inferred |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-033
- **Source location:** #### 6.6.2 Frontend performance budgets | draft line 598
- **Original suggestion:** | Render budget for largest list/table                  | p95 ≤ 500 ms for a page of 50 transaction rows [AI-SUGGESTED: AI-033 | non-blocking] | inferred |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-034
- **Source location:** #### 6.6.2 Frontend performance budgets | draft line 599
- **Original suggestion:** | Time to meaningful content                            | p95 ≤ 1.5 s on the file log overview [AI-SUGGESTED: AI-034 | non-blocking] | inferred |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-035
- **Source location:** #### 6.6.4 Compliance UI behaviour | draft line 604
- **Original suggestion:** - PII fields (account number, user name) are not masked in the visible UI; access is controlled by RBAC rather than masking. [AI-SUGGESTED: AI-035 | non-blocking]
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-036
- **Source location:** #### 6.6.4 Compliance UI behaviour | draft line 605
- **Original suggestion:** - No regional UI variants are required in the initial scope. [AI-SUGGESTED: AI-036 | non-blocking]
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-037
- **Source location:** #### 6.6.5 Accessibility | draft line 609
- **Original suggestion:** - WCAG 2.2 AA is the accessibility target across all screens. [AI-SUGGESTED: AI-037 | non-blocking]
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-038
- **Source location:** ### 6.8 Notification points | draft line 628
- **Original suggestion:** | NT-01 | A File Log has finished processing (Completed or Failed). | Importer | in-app | → §6.2 BR-01 / → §6.2 BR-02 [AI-SUGGESTED: AI-038 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-039
- **Source location:** ### 6.8 Notification points | draft line 629
- **Original suggestion:** | NT-02 | A File Log is now ready for Approver review (all transactions Imported). | Approver | in-app | → §6.2 BR-01 [AI-SUGGESTED: AI-039 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-040
- **Source location:** ### 6.9 Audit-trail UI feature | draft line 637
- **Original suggestion:** | Transaction    | Status, UserNote, LastChangedUser, LastChangedDate [SRC: C-122]     | most recent change per Transaction visible in the detail view; full history retention is the backend doc's concern [AI-SUGGESTED: AI-040 | non-blocking] | Approver |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-041
- **Source location:** ### 6.9 Audit-trail UI feature | draft line 638
- **Original suggestion:** | FileLog | LastChangedUser, LastChangedDate, CurrentStatus, LastExecutedActivityName [SRC: C-123] | most recent change per File Log visible in the detail view [AI-SUGGESTED: AI-041 | non-blocking] | Importer, Approver |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-042
- **Source location:** #### Under `target = application` | draft line 664
- **Original suggestion:** | UserGetList / UserCreate / UserGetById / UserUpdate / UserDelete (/v1/users) | → backend doc operations for User CRUD [SRC: C-110] | Administrative User management; each mutating operation also carries the operating user's identity in a header. [AI-SUGGESTED: AI-042 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-043
- **Source location:** #### Under `target = application` | draft line 665
- **Original suggestion:** | RoleGetList / RoleCreate / RoleUpdate / RoleDelete (/v1/roles) | → backend doc operations for Role CRUD [SRC: C-111] | Administrative Role management. [AI-SUGGESTED: AI-043 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-044
- **Source location:** #### Under `target = application` | draft line 667
- **Original suggestion:** | FileSetting / FileSource / FileType / FileLocationType / FileLocation / ProcessDefinition / BulkFileSettingDatabase / BulkFileSetting list and update operations | → backend doc operations for file-settings management | Administrative configuration of file-handling parameters. [AI-SUGGESTED: AI-044 | non-blocking] |
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-045
- **Source location:** ### Shape: Role | draft line 749
- **Original suggestion:** **Enums:** Name ∈ {Importer, Approver, …} (extensible via Role administration) [AI-SUGGESTED: AI-045 | non-blocking]
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-046
- **Source location:** ### Shape: FileSetting | draft line 764
- **Original suggestion:** **Enums:** Direction ∈ {Inbound, Outbound} [AI-SUGGESTED: AI-046 | non-blocking]
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** drafter-emitted value retained (verbatim from draft)

### AI-047
- **Source location:** ## 9. Key terminology | draft line 800
- **Original suggestion:** | Login endpoint | The user-authentication endpoint. | The project brief names this `POST /v1/users/login` [SRC: C-018]; the authentication API contract names this `POST /v1/auth/login` [SRC: C-090]. The contract is the authoritative source. [AI-SUGGESTED: AI-047 | blocking] |
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** The api definition is correct
- **Follow-ups:** none
- **Resolved value:** The authentication API contract is authoritative. The login endpoint is POST /v1/auth/login.

### AI-048
- **Source location:** ## 10. Volumes | draft line 812
- **Original suggestion:** | Data volume | 10²–10⁴ transactions per File Log; 10³–10⁵ Transactions in the active working set per Approver session [AI-SUGGESTED: AI-048 | blocking] | inferred from sample CSV (20 rows) and typical batch import scale |
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** 10^2 to 10^4 transactions per File Log; 10^3 to 10^5 Transactions in the active working set per Approver session

### AI-049
- **Source location:** ## 10. Volumes | draft line 813
- **Original suggestion:** | Frequency   | 1–10 file uploads per Importer per day; 10²–10³ approve/reject actions per Approver per day [AI-SUGGESTED: AI-049 | blocking] | inferred |
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** 1 to 10 file uploads per Importer per day; 10^2 to 10^3 approve/reject actions per Approver per day

### AI-050
- **Source location:** ## 10. Volumes | draft line 814
- **Original suggestion:** | Concurrency | 1–10 concurrent Importer + Approver sessions [AI-SUGGESTED: AI-050 | blocking] | inferred |
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** confirm
- **Follow-ups:** none
- **Resolved value:** 1 to 10 concurrent Importer plus Approver sessions

