# Adversarial Review — Financial services / banking back-office

- **Domain:** Financial services / banking back-office
- **Generated:** 2026-05-14T10:32:49Z
- **Requirements SHA-256:** `6f9272bbb30d1dce025b843f5319e790bdaa5ac2a07103204bbea7144694f0ae`
- **Reviewer:** Adversarial Review (BMAD-style, strict mode)

---

## Executive Summary

- **Total findings:** 91
  - Severity — Blocker: **7** · Major: **56** · Minor: **28**
  - Disposition — Patch: **61** · Defer: **28** · Reject: **2**
- **Verdict:** `BLOCKED`

> Verdict legend: `BLOCKED` — at least one Reject or Blocker, requirements doc cannot be consumed downstream. `NEEDS-REVISION` — findings present but none blocking. `ACCEPTED-WITH-FIXES` — zero findings on all eight dimensions, every dimension carries a Justification block (rare under strict-BMAD).

---

## Triage

Top issues to address first, ordered by severity. Resolve these before scanning the full Findings Table below.

| Rank | ID | Severity | Cluster | Location | Problem |
|------|----|----------|---------|----------|---------|
| 1 | ADV-45 | Blocker | CL-19 | §1\|§6\|§10 | The document is marked Status: final but contains no MVP designation, no release-scope statement, and no phase tagging — every one of the ~30 requirements is implicitly MVP, which is the classic scope-creep signature for a 501-line spec. |
| 2 | ADV-46 | Blocker | CL-19 | §6\|§10 | There is no "Out of scope" section anywhere in the doc; §10 ends the document, so a downstream engineer has no negative boundary and must infer that everything not mentioned is or is not in scope. |
| 3 | ADV-62 | Blocker | CL-02 | §6.6.1 vs §5 Approve Transaction / §5 Reject Transaction | §6.6.1 mandates step-up authentication for approve and reject, but the Approve Transaction flow lists only a confirmation modal and the Reject Transaction flow lists only a mandatory note — neither flow includes a re-authentication step. |
| 4 | ADV-70 | Blocker | CL-07 | §5 File Upload | The File Upload flow names no maximum file size, no allowed file types/extensions, no virus/malware scan, and no specific failure modes — exactly the canonical "file upload requirement that names no max size, no virus check, no failure mode" anti-pattern. |
| 5 | ADV-71 | Blocker |  | §5 Approve Transaction; §4.2 Approver story | Approval is declared reversible "only by separate workflow" but that recovery/undo workflow is never defined anywhere in the document, leaving the recovery path required by Dimension 7 unspecified. |
| 6 | ADV-72 | Blocker | CL-12 | BR-06; §5 Transaction Table | BR-06 mandates live status reflection but the document specifies no transport (polling, SSE, WebSocket), no concurrent-edit conflict model when two Approvers act on the same row, and no behaviour when the live channel is offline. |
| 7 | ADV-83 | Blocker | CL-10 | §6.6.4 | POPIA treatment is declared as "implied" rather than concretely specified — no data residency, no consent/lawful-basis statement, no PII retention windows (only the audit-trail retention is set), and no data-subject-rights handling, despite the system storing AccountNumber and user PII. |
| 8 | ADV-03 | Major | CL-02 | §6.6.1 | Step-up authentication is asserted as required for approve/reject but no business rule, functional requirement, or task flow (Approve Transaction, Reject Transaction) describes the step-up challenge, its trigger, or its success/failure handling. |
| 9 | ADV-04 | Major | CL-03 | §6.6.1 | MFA is mandated for Approvers but no requirement or flow covers MFA enrollment, challenge during login, recovery, or what happens when an Approver lacks MFA at login time. |
| 10 | ADV-08 | Major | CL-07 | §5 File Upload | The File Upload flow and §6.1 upload requirement specify no contract on accepted file type, size cap, encoding, or virus/integrity scanning, even though §7 File Log defines a FileHash sha-256 field implying an integrity check that no requirement actually mandates. |

---

## Clusters

Findings sharing a root cause are grouped below. Each cluster lists its member finding IDs; the per-dimension sections still contain every finding in full detail.

| Cluster | Theme | Findings | Max severity |
|---------|-------|----------|--------------|
| CL-01 | User / Role admin entity referenced but unmanaged | ADV-02, ADV-55, ADV-61 | Major |
| CL-02 | Step-up auth required but never wired into flows | ADV-03, ADV-19, ADV-34, ADV-48, ADV-56, ADV-62, ADV-75 | Blocker |
| CL-03 | MFA required for Approver but never wired into Auth | ADV-04, ADV-24, ADV-47, ADV-57, ADV-63, ADV-86 | Major |
| CL-04 | Account lockout policy stated without UX or recovery | ADV-05, ADV-68, ADV-74 | Major |
| CL-05 | Idle session warning UI / extend-session undefined | ADV-06, ADV-76 | Major |
| CL-06 | Logout scoped to Approver only despite both roles authenticating | ADV-07, ADV-52, ADV-64 | Major |
| CL-07 | File Upload contract missing size/type/virus/partial-failure | ADV-08, ADV-22, ADV-39, ADV-70, ADV-80 | Blocker |
| CL-08 | BR-07 cites "retry" but no retry flow / RBAC anywhere | ADV-09, ADV-18, ADV-51, ADV-77 | Major |
| CL-09 | No observability NFR despite 7-yr audit + RTO/RPO | ADV-10, ADV-88 | Major |
| CL-10 | POPIA named but no concrete residency/retention/DSAR | ADV-11, ADV-49, ADV-83 | Blocker |
| CL-11 | CSV export contract and over-limit behaviour unspecified | ADV-13, ADV-78, ADV-89 | Major |
| CL-12 | BR-06 real-time has no transport/latency/concurrency model | ADV-17, ADV-35, ADV-58, ADV-72, ADV-85 | Blocker |
| CL-13 | File Log field types (CurrentStatus, RecordCount) inconsistent | ADV-21, ADV-67 | Minor |
| CL-14 | File Summary "counts may be incomplete" under-specified | ADV-25, ADV-40 | Major |
| CL-15 | Password "complexity per security policy" undefined | ADV-27, ADV-36 | Major |
| CL-16 | WCAG/screen-reader predicates non-testable | ADV-29, ADV-31 | Major |
| CL-17 | Availability target references undefined "business hours" | ADV-30, ADV-33 | Major |
| CL-18 | Performance thresholds bounded ≤1000 rows; Volumes allow 10^5 | ADV-32, ADV-53, ADV-84 | Major |
| CL-19 | No MVP scope declaration and no out-of-scope section | ADV-45, ADV-46 | Blocker |
| CL-20 | §2.4 Mermaid diagram omits fields defined in §7 | ADV-65, ADV-66 | Major |

---

## Findings Table

| ID | Dim | Severity | Disposition | Cluster | Location | Problem |
|----|-----|----------|-------------|---------|----------|---------|
| ADV-45 | 4 | Blocker | Reject | CL-19 | §1\|§6\|§10 | The document is marked Status: final but contains no MVP designation, no release-scope statement, and no phase tagging — every one of the ~30 requirements is implicitly MVP, which is the classic scope-creep signature for a 501-line spec. |
| ADV-46 | 4 | Blocker | Reject | CL-19 | §6\|§10 | There is no "Out of scope" section anywhere in the doc; §10 ends the document, so a downstream engineer has no negative boundary and must infer that everything not mentioned is or is not in scope. |
| ADV-62 | 6 | Blocker | Defer | CL-02 | §6.6.1 vs §5 Approve Transaction / §5 Reject Transaction | §6.6.1 mandates step-up authentication for approve and reject, but the Approve Transaction flow lists only a confirmation modal and the Reject Transaction flow lists only a mandatory note — neither flow includes a re-authentication step. |
| ADV-70 | 7 | Blocker | Defer | CL-07 | §5 File Upload | The File Upload flow names no maximum file size, no allowed file types/extensions, no virus/malware scan, and no specific failure modes (oversize, wrong type, malformed content) — exactly the canonical "file upload requirement that names no max size, no virus check, no failure mode" anti-pattern. |
| ADV-71 | 7 | Blocker | Defer |  | §5 Approve Transaction; §4.2 Approver story | Approval is declared reversible "only by separate workflow" but that recovery/undo workflow is never defined anywhere in the document, leaving the recovery path required by Dimension 7 unspecified. |
| ADV-72 | 7 | Blocker | Defer | CL-12 | BR-06; §5 Transaction Table | BR-06 mandates live status reflection but the document specifies no transport (polling, SSE, WebSocket), no concurrent-edit conflict model when two Approvers act on the same row, and no behaviour when the live channel is offline. |
| ADV-83 | 8 | Blocker | Defer | CL-10 | §6.6.4 | POPIA treatment is declared as "implied" rather than concretely specified — no data residency, no consent/lawful-basis statement, no PII retention windows (only the audit-trail retention is set), and no data-subject-rights handling, despite the system storing AccountNumber and user PII. |
| ADV-01 | 1 | Major | Patch |  | §6.1 | Functional requirements are an unnumbered prose bullet list with no FR-NN identifiers and no acceptance criteria or pass/fail predicates attached to any individual statement, leaving every functional shall-do unimplementable and untraceable from goals or flows. |
| ADV-02 | 1 | Major | Patch | CL-01 | §6.5 | The RBAC matrix grants only Read on the User entity to both roles, leaving no actor with Create/Update/Delete on Users — so no requirement describes how user accounts come into existence, are deactivated, or have roles changed. |
| ADV-03 | 1 | Major | Patch | CL-02 | §6.6.1 | Step-up authentication is asserted as required for approve/reject but no business rule, functional requirement, or task flow (Approve Transaction, Reject Transaction) describes the step-up challenge, its trigger, or its success/failure handling. |
| ADV-04 | 1 | Major | Patch | CL-03 | §6.6.1 | MFA is mandated for Approvers but no requirement or flow covers MFA enrollment, challenge during login, recovery, or what happens when an Approver lacks MFA at login time. |
| ADV-05 | 1 | Major | Patch | CL-04 | §6.6.1 | Account lockout thresholds are stated as an NFR but no functional requirement or §5 Authentication flow describes the lockout user experience, error message, or how an Importer/Approver recovers from a locked account. |
| ADV-06 | 1 | Major | Patch | CL-05 | §6.6.1 | Idle and absolute session timeouts plus a 60-second warning lead-time are asserted but no requirement or flow describes the warning UI, the extend-session action, or the redirect-on-expiry behaviour. |
| ADV-07 | 1 | Major | Patch | CL-06 | §6.1 | Logout is scoped to Approvers only, leaving no documented logout requirement or session-invalidation path for Importers despite both roles being authenticated principals. |
| ADV-08 | 1 | Major | Patch | CL-07 | §5 File Upload | The File Upload flow and §6.1 upload requirement specify no contract on accepted file type, size cap, encoding, or virus/integrity scanning, even though §7 File Log defines a FileHash sha-256 field implying an integrity check that no requirement actually mandates. |
| ADV-09 | 1 | Major | Patch | CL-08 | BR-07 | BR-07 references a "retry" against a Failed File Log but no requirement, flow, or RBAC entry describes who triggers the retry, what endpoint serves it, or how the File Log transitions back out of Failed. |
| ADV-10 | 1 | Major | Patch | CL-09 | §6.6 / §6.1 | No observability/operability non-functional category is present — there are no logging, monitoring, alerting, or health-check requirements despite the financial domain and the §6.6.4 7-year audit retention commitment depending on a logging substrate. |
| ADV-11 | 1 | Major | Patch | CL-10 | §6.6.4 | POPIA is named as the governing privacy regime but no requirement covers POPIA-specific obligations such as data-subject access/erasure requests, lawful-basis recording, cross-border transfer restrictions, or breach-notification timelines. |
| ADV-12 | 1 | Major | Patch |  | §6.3 | The audit trail derives the actor identity from a client-supplied request header without any requirement constraining who may set the header, how it is reconciled against the authenticated session principal, or how forgery is prevented. |
| ADV-13 | 1 | Major | Patch | CL-11 | §6.1 | The CSV export requirement specifies no contract for the export — no column list, header row, encoding (UTF-8/BOM), delimiter, quoting rules, filename pattern, or maximum row count is defined, despite §6.6.2 setting a 10 000-row performance target. |
| ADV-14 | 1 | Major | Patch |  | §7 Entity: File Log | File Log carries an IsActive soft-delete flag but no functional requirement, business rule, or RBAC cell describes who toggles IsActive, what triggers archival, or how inactive file logs are surfaced (or hidden) in the File Log Overview. |
| ADV-17 | 2 | Major | Patch | CL-12 | §6.2 BR-06 | "without a manual refresh" specifies no time window or mechanism, leaving the latency budget and update strategy (push, poll, optimistic UI) unspecified. |
| ADV-18 | 2 | Major | Patch | CL-08 | §6.2 BR-07 | "surface the failure prominently" and "until retry succeeds" are both undefined — there is no specified retry flow elsewhere in the document, and "prominently" is a vague qualifier. |
| ADV-19 | 2 | Major | Patch | CL-02 | §6.6.1 | "Step-up authentication" is not defined anywhere in the document — the factor required (password re-entry, MFA challenge, biometric) and its scope (per action, per session) are unspecified. |
| ADV-20 | 2 | Major | Patch |  | §6.1 | "Process" is a vague verb and the slash between two field names leaves it unclear which field is canonical for the user-visible status versus the operational status. |
| ADV-31 | 3 | Major | Patch | CL-16 | §6.6.5 | Accessibility requirement names a standard and a vague scope but provides no enumerated primary actions, no audit tool/sample, and no pass/fail predicate for "screen-reader semantics". |
| ADV-32 | 3 | Major | Patch | CL-18 | §6.6.2 | Performance targets give thresholds but omit sample size, network/device profile, and measurement methodology, so a tester cannot reproduce the test. |
| ADV-33 | 3 | Major | Patch | CL-17 | §6.6.3 | Availability target references "business hours" without defining them, no measurement window, and no definition of "down" versus "degraded". |
| ADV-34 | 3 | Major | Patch | CL-02 | §6.6.1 | Step-up auth is mandated but the factor, trigger window, and expiry are unspecified, so no test can decide whether a given step-up implementation satisfies the requirement. |
| ADV-35 | 3 | Major | Patch | CL-12 | BR-06 | BR-06 prescribes "without a manual refresh" but gives no latency bound, so "reflected eventually" would pass — there is no failing-test predicate. |
| ADV-36 | 3 | Major | Patch | CL-15 | §6.6.1 | Password rule (§7 Entity User) says "complexity per security policy" but no policy is enumerated, so a tester cannot decide whether a given password is accepted or rejected. |
| ADV-37 | 3 | Major | Patch |  | §6.6.4 | Negative predicate over PII is not testable without an enumeration of which fields count as PII for this product. |
| ADV-38 | 3 | Major | Patch |  | §4.1 | Goal-level "Quality signals" (Speed-to-confidence, Accuracy, throughput, decision confidence, At-a-glance status) are wishes — no numeric thresholds, so completion of a goal is not decidable. |
| ADV-39 | 3 | Major | Patch | CL-07 | §5 File Upload | "Status shown in UI" and "Success / failure feedback is rendered after upload" do not enumerate which statuses or which messages, so the exception path is not decidable from the doc alone. |
| ADV-40 | 3 | Major | Patch | CL-14 | §5 File Summary View | "Counts may be incomplete" and "shows … prominently" are wishes — no testable predicate for what the user sees when Processing vs Failed. |
| ADV-47 | 4 | Major | Defer | CL-03 | §6.6.1 | MFA for Approvers and step-up authentication for approve/reject are listed as "inferred" defaults in NFRs but carry weeks of engineering cost (enrolment UI, factor selection, recovery flows) and are not tagged as MVP, post-MVP, or stretch — this requirement straddles the cut line. |
| ADV-48 | 4 | Major | Defer | CL-02 | §6.6.1 | Account lockout, idle-warning lead-time, idle/absolute session timeouts, and step-up re-auth are all stated as inferred defaults with concrete numeric targets but no scope tag — each implies non-trivial backend state machines that may or may not be in MVP scope. |
| ADV-49 | 4 | Major | Defer | CL-10 | §6.6.4 | POPIA compliance and a 7-year audit retention obligation are stated without scope tagging or cost discussion — POPIA conformance alone is a multi-month workstream (DSAR handling, breach notification, data-minimisation review) and cannot be silently bundled into MVP. |
| ADV-50 | 4 | Major | Defer |  | §6.4\|line-345 | A responsive mobile breakpoint behaviour is mixed in with desktop table requirements without any scope tag — given §3 personas describe daily desk-bound use, the mobile experience is plausibly post-MVP but is currently mandated alongside core flows. |
| ADV-51 | 4 | Major | Defer | CL-08 | §6.2\|BR-07 | BR-07 references "retry succeeds" but no retry flow exists in §5 task flows and no retry requirement appears in §6.1 — this is either an out-of-scope feature smuggled into a business rule or a missing MVP flow, and the doc never decides which. |
| ADV-52 | 4 | Major | Defer | CL-06 | §6.1\|line-323 | The functional list grants logout only to Approvers, yet Importers also authenticate (§5 Authentication, §3 Importer) and §6.5 RBAC grants Importers "X" on Authentication — leaving Importer logout silently out of scope by omission rather than by explicit exclusion. |
| ADV-54 | 5 | Major | Patch |  | §7 Entity: File Log, line 431 | FileSetting is used as a foreign-key target in §7 and named in §9, but is never introduced as a concept in §2 Domain model, so the entity referenced by SettingId has no defined source. |
| ADV-55 | 5 | Major | Patch | CL-01 | §7 Entity: User, line 412 | The type RoleRead is used for the User.Roles field but is never defined as an entity, enum, or DTO anywhere in the document, so the data shape an engineer must implement is unknown. |
| ADV-56 | 5 | Major | Defer | CL-02 | §6.6.1 Re-auth scope, line 366 | Step-up authentication is mandated for approve/reject but the Approve and Reject flows in §5 contain no step-up step and no step-up mechanism is defined anywhere in the doc, so the dependency on this capability is undiscoverable from the flow definitions. |
| ADV-57 | 5 | Major | Defer | CL-03 | §6.6.1 MFA requirement, line 368 | MFA is mandated for Approvers but the Authentication flow in §5 (line 220) describes only "email + password" with no MFA step, so the dependency between Authentication and the MFA capability needed before Approver login is undiscoverable. |
| ADV-58 | 5 | Major | Defer | CL-12 | BR-06, line 334 | Real-time status reflection without manual refresh implies a push/poll mechanism (e.g., websocket, SSE, or background polling) that is not defined anywhere in the doc, so the dependency this rule places on a delivery channel is invisible to an engineer. |
| ADV-63 | 6 | Major | Defer | CL-03 | §6.6.1 vs §5 Authentication | §6.6.1 requires MFA for Approvers, but §5 Authentication flow's Steps list only email+password submission with no MFA step or decision point, contradicting the policy. |
| ADV-64 | 6 | Major | Patch | CL-06 | §6.1 vs §6.6.1 / §6.6.4 | §6.1 scopes the logout endpoint to Approvers only, but §6.6.1 describes the logout cookie clearance generically (POST /v1/auth/logout) and §6.6.4 records logout events as a generic audit event, implying logout applies to all roles. |
| ADV-65 | 6 | Major | Defer | CL-20 | §2.4 vs §7 Entity: Transaction | The Transaction class in the §2.4 Mermaid diagram omits FileName, Description, TransactionType, LastChangedUser and LastChangedDate, all of which are defined as Transaction fields in §7, so the diagram and the data-entity table disagree on the entity's shape. |
| ADV-66 | 6 | Major | Defer | CL-20 | §2.4 vs §7 Entity: File Log | The §2.4 Mermaid FileLog class lists CurrentStatus but omits LastExecutedActivityName, SettingId, SettingName, FileHash, LastChangedUser, and LastChangedDate, contradicting the authoritative File Log shape in §7 where LastExecutedActivityName is the required status field. |
| ADV-73 | 7 | Major | Patch |  | §5 Reject Transaction; §7 Entity: Transaction (UserNote) | The mandatory rejection note has no maximum-length validation, no minimum content rule beyond "non-empty", and no behaviour for whitespace-only input — leaving the maximum-size / input-validation edge case unspecified. |
| ADV-74 | 7 | Major | Defer | CL-04 | §6.6.1 Security & session | The lockout policy names no user-facing UX (what the locked user sees, whether the generic-error pattern from BR-05 still applies, whether countdown is shown, whether email notification fires) and names no recovery path (password reset, admin unlock). |
| ADV-75 | 7 | Major | Defer | CL-02 | §6.6.1 Security & session | Step-up auth is required for approve/reject but no flow is defined in §5 — neither the trigger (every action / per-session / time-based), the prompt UX, the failure mode, nor the impact on the existing confirmation modal is specified. |
| ADV-76 | 7 | Major | Defer | CL-05 | §6.6.1 Security & session | Idle timeout and a 60-second warning are stated, but no flow specifies the warning UI, the "extend session" control, or what happens to in-flight work (an unsaved rejection note, an in-progress export) when the timeout fires. |
| ADV-77 | 7 | Major | Defer | CL-08 | BR-07; §5 File Summary View | BR-07 references a "retry" that succeeds, but no Retry flow is defined in §5, no retry trigger/permission is set, and no RBAC cell in §6.5 grants "retry file" to any role. |
| ADV-78 | 7 | Major | Defer | CL-11 | §5 Export Transactions; §6.6.2 Performance | Performance bounds the export at ≤10 000 rows but neither §5 Export Transactions nor §6.1 specifies what happens above that limit (truncate? warn? async job? hard cap?), leaving the maximum-size edge case unspecified. |
| ADV-79 | 7 | Major | Defer |  | §5 Approve Transaction; §5 Reject Transaction; §5 Export Transactions; §5 File Upload | No flow specifies network-failure behaviour for approve/reject/upload/export — what the UI shows on timeout, what state is preserved (e.g., the typed reject note), and whether retries are idempotent (the same approval clicked twice on a flaky connection). |
| ADV-80 | 7 | Major | Defer | CL-07 | §5 File Upload; §6.1 | The partial-failure case where the file is parsed but some rows are malformed (8/10 succeed) is unspecified — the only outcomes named are "Completed" or "Failed", with no partial-success state, no per-row error report, and no rejected-rows surface. |
| ADV-84 | 8 | Major | Patch | CL-18 | §6.6.2 | Performance thresholds are scoped to ≤1 000 rows while §10 Volumes states 10³–10⁵ transactions retained per active file log, leaving the realistic operating range without any latency target and with no index/pagination strategy discussion. |
| ADV-85 | 8 | Major | Defer | CL-12 | §6.6.2 / BR-06 | BR-06 is a real-time-style requirement ("without a manual refresh") but no latency budget, transport mechanism (polling interval, SSE, WebSocket), or staleness tolerance is specified, making feasibility unverifiable. |
| ADV-86 | 8 | Major | Defer | CL-03 | §6.6.1 | MFA is required for Approvers and step-up auth is required for approve/reject, but no MFA mechanism (TOTP, WebAuthn, SMS OTP) or step-up flow is named, leaving the feasibility and integration surface undefined. |
| ADV-87 | 8 | Major | Patch |  | §6.4 / §6.6 | The document names a viewport breakpoint but never declares supported browsers, versions, or device/OS targets, leaving "works everywhere" as the implicit (infeasible) baseline. |
| ADV-88 | 8 | Major | Defer | CL-09 | §6.6.3 | RTO/RPO are stated but no backup cadence, backup retention, restore-test schedule, or operational logging/monitoring/alerting requirements are named — the document commits to recovery without committing to the operational machinery that makes recovery feasible. |
| ADV-15 | 1 | Minor | Patch |  | §6.5 | The matrix gives Importer Execute (X) on the Transaction Table and Search & Filtering columns, but no requirement clarifies what Importer-facing data narrowing or visibility constraints apply — e.g. whether Importers see only their own uploaded transactions or all transactions. |
| ADV-16 | 1 | Minor | Patch |  | G-04 | G-04 "Monitor the processing status of uploaded files" has flows and a display requirement but no business rule defines when a stuck-in-Processing file should escalate or what the user can do if processing has not completed within an expected window. |
| ADV-21 | 2 | Minor | Patch | CL-13 | §7 Entity: File Log | "Operational status complement" is undefined — the enumeration, the relationship to LastExecutedActivityName, and when it differs are all unspecified. |
| ADV-22 | 2 | Minor | Patch | CL-07 | §5 File Upload | Step 5 "Status shown in UI" is vague — which status (upload acknowledgement, parse result, File State), where in the UI, and at what point are all unspecified. |
| ADV-23 | 2 | Minor | Patch |  | §6.3 | "the transaction detail surface" is not a defined entity in §5 task flows or §6.4 user-facing — "surface" is a vague noun and the document does not specify any "transaction detail" view. |
| ADV-24 | 2 | Minor | Patch | CL-03 | §6.6.1 | "Optional for Importer" is ambiguous — it does not state who enables MFA (self-service, admin-set), what factor types are accepted, or whether the optionality is per-user or system-wide. |
| ADV-25 | 2 | Minor | Patch | CL-14 | §5 File Summary View | "Counts may be incomplete" uses the hedge "may" for a deterministic condition (Processing/Failed implies partial counts), and "prominently" is a vague qualifier as in BR-07. |
| ADV-26 | 2 | Minor | Patch |  | §6.4 | "where applicable" is a vague conditional — the document does not name which screens this applies to, leaving the empty-state CTA rule under-specified for the Transaction Table. |
| ADV-27 | 2 | Minor | Patch | CL-15 | §7 Entity: User | "complexity per security policy" references an external, undefined policy — the actual character-class, length-upper-bound, and disallowed-pattern rules are unspecified. |
| ADV-28 | 2 | Minor | Patch |  | §10 | "one or more files" is a vague quantifier that does not bound the upper end, leaving capacity planning and rate-limiting requirements unspecified. |
| ADV-29 | 2 | Minor | Patch | CL-16 | §6.6.5 | "screen-reader semantics on status badges" is vague — it does not specify role, accessible name source, or live-region behaviour on transition. |
| ADV-30 | 2 | Minor | Patch | CL-17 | §6.6.3 | "business hours" is undefined — timezone, days-of-week, and start/end times are all unspecified, making the uptime target unmeasurable. |
| ADV-41 | 3 | Minor | Patch |  | §6.4 | A 4–8 s range admits any value in the interval, so two implementations could both pass yet diverge; no per-event mapping. |
| ADV-42 | 3 | Minor | Patch |  | §6.4 | "2–3 key columns" is non-deterministic across the two tables (File Logs, Transactions); a tester cannot decide which columns must appear on the card. |
| ADV-43 | 3 | Minor | Patch |  | §5 Authentication | Generic-message rule is correct in intent but does not pin the actual string, so two implementations rendering different copy could each claim conformance. |
| ADV-44 | 3 | Minor | Patch |  | §6.6.4 | Audit list omits failure events (failed login, failed upload, failed approve/reject) so the test "audit row exists for every attempted action" is undefined. |
| ADV-53 | 4 | Minor | Patch | CL-18 | §6.6.2 | Performance targets reference a 1 000-row ceiling and a 10 000-row CSV ceiling, but §10 Volumes allows 10⁵ transactions per active file log — the perf NFR and the volume NFR are inconsistent and neither states which bound is MVP-binding. |
| ADV-59 | 5 | Minor | Patch |  | §4.1 G-02, G-03, G-04, lines 152-154 | G-02 (approve/reject), G-03 (export filtered), and G-04 (monitor) all logically depend on G-01 (upload) producing files and transactions first, but no explicit ordering note records that dependency, so the goals catalogue does not communicate implementation order. |
| ADV-60 | 5 | Minor | Patch |  | §6.1 Functional, line 320 | §6.1 references the fields LastExecutedActivityName and CurrentStatus before they are defined (§7 Entity: File Log appears later at lines 422-433), so an implementer reading top-down does not know what these fields are or which is authoritative. |
| ADV-61 | 5 | Minor | Patch | CL-01 | §6.5 RBAC matrix header, line 352 | The RBAC matrix lists "User" as a resource with both roles assigned R access, but the doc defines no User-management flow in §5 and no functional requirement for reading other users, so the resource has access cells with no upstream capability to implement. |
| ADV-67 | 6 | Minor | Patch | CL-13 | §7 Entity: File Log RecordCount vs §5 File Log Overview | §7 declares RecordCount as type string with a "numeric" validation, but the §5 File Log Overview flow surfaces it as a "Record Count" column and the §2.4 diagram lists it as an unqualified +RecordCount, implying a numeric type — the string typing contradicts its usage everywhere else. |
| ADV-68 | 6 | Minor | Patch | CL-04 | §6.6.1 Account lockout vs §5 Authentication | §6.6.1 specifies a 5-attempt lockout with a 15-minute cooldown, but §5 Authentication's Exception paths describe only a generic error message and do not mention lockout behaviour or a locked-out state, so the flow contradicts the policy by silence. |
| ADV-69 | 6 | Minor | Patch |  | §6.5 RBAC matrix Approver Transaction cell vs §6.5 action vocabulary | The Approver/Transaction cell grants "U†BR-01" (update) on the Transaction resource, but the action vocabulary reserves "A" for approve and the matrix already grants A†BR-01 / A†BR-02 on the Approve / Reject columns — granting U on Transaction therefore contradicts the per-action columns and lets an Approver update arbitrary transaction fields beyond approve/reject. |
| ADV-81 | 7 | Minor | Patch |  | §5 Transaction Table; §6.4 | The document specifies hiding role-restricted controls but does not specify the authorization-failure UX when an Importer reaches an Approver-only URL directly (deep-link, browser back, copy-pasted URL) — the canonical Dimension 7 authorization-failure case. |
| ADV-82 | 7 | Minor | Patch |  | §7 Entity: User; §6.1 | Email validation is stated as "RFC 5322 format" but neither §6.1 nor the Authentication flow names the user-facing validation behaviour (when it fires, what message is shown, whether it composes with the BR-05 generic-error rule at login). |
| ADV-89 | 8 | Minor | Patch | CL-11 | §6.6.2 | Export threshold is bounded at 10 000 rows but the export contract (§ Export Transactions flow / §6.1) places no upper bound on the filtered dataset, so the largest legal export has no latency target. |
| ADV-90 | 8 | Minor | Defer |  | §1..§10 | The document contains no cost, time, or team-size constraints anywhere, which is itself a feasibility flag for a regulated-domain build. |
| ADV-91 | 8 | Minor | Patch |  | §6.6.1 | bcrypt is named but the cost factor (work factor) is not, so the auth-endpoint latency targets are not feasibility-bounded against the chosen hashing cost. |

---

## Dimension 1 — Completeness & Gaps

### Findings

#### ADV-01 — §6.1 functional bullets lack IDs and acceptance criteria

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.1
- **Evidence:**
  > - Authenticate users with username and password against a server-side bcrypt-hashed credential store; on success, issue an HttpOnly, Secure, SameSite=Strict session cookie.- Allow Importers to upload a transaction file with FileSettingId, FileSettingName, and FileName, and create a corresponding File Log on the server.
- **Problem:** Functional requirements are an unnumbered prose bullet list with no FR-NN identifiers and no acceptance criteria or pass/fail predicates attached to any individual statement, leaving every functional shall-do unimplementable and untraceable from goals or flows.
- **Recommendation:** Assign FR-NN IDs to each functional statement and attach a pass/fail acceptance criterion to each (e.g. expected response code, observable state change, or referenced flow step).

#### ADV-02 — User entity has no Create/Update/Delete authority anywhere

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.5
- **Evidence:**
  > | Importer | R | C R | R | X | X | X | X | X | — | — | — | X |
  > | Approver | R | R | R U†BR-01 | X | — | X | X | X | A†BR-01 | A†BR-02 | X | X |
- **Problem:** The RBAC matrix grants only Read on the User entity to both roles, leaving no actor with Create/Update/Delete on Users — so no requirement describes how user accounts come into existence, are deactivated, or have roles changed.
- **Recommendation:** Add an administrator role (or explicit external IdP integration) to the matrix with User C/U/D permissions, or add a requirement stating user provisioning is out of scope and handled by a named external system.

#### ADV-03 — Step-up auth required for approve/reject but never wired into any flow or BR

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** Step-up authentication is asserted as required for approve/reject but no business rule, functional requirement, or task flow (Approve Transaction, Reject Transaction) describes the step-up challenge, its trigger, or its success/failure handling.
- **Recommendation:** Add a BR plus flow steps in §5 Approve Transaction and Reject Transaction that name the step-up factor, the prompt point, and the failure path, or remove the re-auth NFR if it is not in scope.

#### ADV-04 — MFA mandated for Approver but never wired into Authentication flow

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** MFA is mandated for Approvers but no requirement or flow covers MFA enrollment, challenge during login, recovery, or what happens when an Approver lacks MFA at login time.
- **Recommendation:** Add an MFA enrollment/challenge requirement and extend §5 Authentication with the MFA step and its failure/recovery paths, or downgrade the NFR to "out of scope".

#### ADV-05 — Account lockout policy lacks flow, UX, and recovery path

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Account lockout policy | 5 failed attempts → 15-minute cooldown; cooldown resets on successful authentication | inferred |
- **Problem:** Account lockout thresholds are stated as an NFR but no functional requirement or §5 Authentication flow describes the lockout user experience, error message, or how an Importer/Approver recovers from a locked account.
- **Recommendation:** Add a functional requirement and an Authentication-flow exception path that specify lockout messaging, cooldown countdown surfacing, and the recovery channel (self-service, admin reset, etc.).

#### ADV-06 — Idle/absolute session timeouts have no warning flow or extend-session UX

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Idle session timeout | 15 minutes | inferred (financial domain default) |
  > | Absolute session timeout | 8 hours | inferred (financial domain default) |
  > | Idle warning lead-time | 60 seconds before idle logout | inferred (financial domain default) |
- **Problem:** Idle and absolute session timeouts plus a 60-second warning lead-time are asserted but no requirement or flow describes the warning UI, the extend-session action, or the redirect-on-expiry behaviour.
- **Recommendation:** Add a functional requirement and a §5 task flow (e.g. Session Expiry Warning) that specify the warning surface, extend-session control, and post-expiry navigation.

#### ADV-07 — Logout requirement scoped to Approvers only

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.1
- **Evidence:**
  > - Provide search and filtering across Status, File (FileLogId), Date range, Amount range, and free text on Reference / Account.- Provide a file summary view showing total records and a count by status (Imported / Approved / Rejected).- Allow Approvers to log out via an endpoint that invalidates the session cookie.
- **Problem:** Logout is scoped to Approvers only, leaving no documented logout requirement or session-invalidation path for Importers despite both roles being authenticated principals.
- **Recommendation:** Reword the bullet so logout is available to any authenticated user, or add a separate Importer logout requirement with the same session-invalidation contract.

#### ADV-08 — File Upload requirement misses size/type/encoding/virus contract

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 File Upload
- **Evidence:**
  > | Steps | 1. Select file (drag & drop supported). 2. Provide FileSettingId, FileSettingName, FileName. 3. Submit upload. 4. System creates File Log. 5. Status shown in UI. |
  > | Decision points | Required metadata must be provided before upload can proceed: FileSettingId, FileSettingName, FileName. |
  > | Exception paths | Success / failure feedback is rendered after upload. On failure, the file is not parsed and no File Log row is created in a Completed state. |
- **Problem:** The File Upload flow and §6.1 upload requirement specify no contract on accepted file type, size cap, encoding, or virus/integrity scanning, even though §7 File Log defines a FileHash sha-256 field implying an integrity check that no requirement actually mandates.
- **Recommendation:** Add functional requirements (or extend the File Upload flow) with explicit max file size, accepted MIME/extension, encoding expectations, and the integrity-hash computation/verification step that populates FileHash.

#### ADV-09 — BR-07 references a retry mechanism that exists nowhere else in the doc

- **Severity:** Major
- **Disposition:** Patch
- **Location:** BR-07
- **Evidence:**
  > | BR-07 | When a file log is in Failed state, then the file summary view must surface the failure prominently and inhibit drill-down into transactions until retry succeeds. | UI | → §2.3 File Log invariant | major |
- **Problem:** BR-07 references a "retry" against a Failed File Log but no requirement, flow, or RBAC entry describes who triggers the retry, what endpoint serves it, or how the File Log transitions back out of Failed.
- **Recommendation:** Add a Retry Failed File task flow plus a functional requirement and RBAC cell specifying the actor, trigger, and Failed→Processing transition contract.

#### ADV-10 — No observability/operability NFR category present

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6 / §6.1
- **Evidence:**
  > #### 6.6.5 Accessibility
  >
  > - WCAG 2.2 AA conformance, full keyboard reach for all primary actions, screen-reader semantics on status badges.
  >
  > ---
- **Problem:** No observability/operability non-functional category is present — there are no logging, monitoring, alerting, or health-check requirements despite the financial domain and the §6.6.4 7-year audit retention commitment depending on a logging substrate.
- **Recommendation:** Add a §6.6 subsection for Observability defining minimum log events (auth, upload, approve, reject, export), retention/SIEM destination, health endpoints, and alert thresholds for the SLOs in §6.6.2 and §6.6.3.

#### ADV-11 — POPIA named but no concrete obligations beyond audit retention

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.4
- **Evidence:**
  > - POPIA (South Africa) — implied by the use of ZAR currency in the sample dataset and South African account-number formats.- Audit trail: every approve, reject, upload, login, and logout event is recorded with `LastChangedUser` and `LastChangedDate`; retain 7 years.
- **Problem:** POPIA is named as the governing privacy regime but no requirement covers POPIA-specific obligations such as data-subject access/erasure requests, lawful-basis recording, cross-border transfer restrictions, or breach-notification timelines.
- **Recommendation:** Add explicit POPIA requirements covering data-subject rights handling, retention/erasure for non-audit PII, and breach-notification escalation, or restate the POPIA bullet as an in-scope/out-of-scope boundary statement.

#### ADV-12 — Audit actor identity derived from a client-supplied header without validation

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.3
- **Evidence:**
  > - Capture `LastChangedUser` and `LastChangedDate` on every mutating action against File Log, Transaction, and User entities, sourced from the `LastChangedUser` request header convention used across the API.
- **Problem:** The audit trail derives the actor identity from a client-supplied request header without any requirement constraining who may set the header, how it is reconciled against the authenticated session principal, or how forgery is prevented.
- **Recommendation:** Add a requirement stating that `LastChangedUser` must be derived from or validated against the authenticated session and that mismatches cause the request to be rejected and logged.

#### ADV-13 — CSV export contract is wholly unspecified

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.1
- **Evidence:**
  > - Require a mandatory user note for every rejection.- Allow Approvers to export the currently filtered transaction dataset as CSV.
- **Problem:** The CSV export requirement specifies no contract for the export — no column list, header row, encoding (UTF-8/BOM), delimiter, quoting rules, filename pattern, or maximum row count is defined, despite §6.6.2 setting a 10 000-row performance target.
- **Recommendation:** Add a CSV export contract (column order, header row, UTF-8 encoding, RFC 4180 quoting, filename convention) and a behaviour for datasets exceeding the 10 000-row target.

#### ADV-14 — File Log IsActive soft-delete flag has no requirement governing it

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §7 Entity: File Log
- **Evidence:**
  > | IsActive | boolean | yes | — | Soft-delete / archival flag. |
- **Problem:** File Log carries an IsActive soft-delete flag but no functional requirement, business rule, or RBAC cell describes who toggles IsActive, what triggers archival, or how inactive file logs are surfaced (or hidden) in the File Log Overview.
- **Recommendation:** Add a requirement and matrix cell governing File Log archival/restoration, and specify whether inactive rows are excluded by default in the §5 File Log Overview list.

#### ADV-15 — Importer's data-visibility scope on the Transaction Table unspecified

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.5
- **Evidence:**
  > | Importer | R | C R | R | X | X | X | X | X | — | — | — | X |
- **Problem:** The matrix gives Importer Execute (X) on the Transaction Table and Search & Filtering columns, but no requirement clarifies what Importer-facing data narrowing or visibility constraints apply — e.g. whether Importers see only their own uploaded transactions or all transactions.
- **Recommendation:** Add a requirement explicitly stating the Importer's row-level visibility scope on the Transaction Table (own uploads only vs. global) and reflect it in the §5 Transaction Table flow.

#### ADV-16 — No SLO or escalation for files stuck in Processing

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** G-04
- **Evidence:**
  > | G-04 | Monitor the processing status of uploaded files. | At-a-glance status, drill-down to detail | top-level | dashboard list | tabular file log with status column |
- **Problem:** G-04 "Monitor the processing status of uploaded files" has flows and a display requirement but no business rule defines when a stuck-in-Processing file should escalate or what the user can do if processing has not completed within an expected window.
- **Recommendation:** Add a BR (or NFR) defining a processing-duration SLO and the user-visible escalation (banner/alert) when a file remains in Processing beyond that threshold.

---

## Dimension 2 — Ambiguity & Clarity

### Findings

#### ADV-17 — BR-06 "without a manual refresh" has no time window

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.2 BR-06
- **Evidence:**
  > | BR-06 | When a transaction's status changes (Approved or Rejected), then the new status must be reflected in the transaction table without a manual refresh. | UI | → §2.3 Transaction invariant | major |
- **Problem:** "without a manual refresh" specifies no time window or mechanism, leaving the latency budget and update strategy (push, poll, optimistic UI) unspecified.
- **Recommendation:** Replace with a quantified target, e.g., "the new status is reflected in the visible transaction row within 2 seconds of the server-confirmed transition".

#### ADV-18 — BR-07 uses "prominently" and "until retry succeeds" — both undefined

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.2 BR-07
- **Evidence:**
  > | BR-07 | When a file log is in Failed state, then the file summary view must surface the failure prominently and inhibit drill-down into transactions until retry succeeds. | UI | → §2.3 File Log invariant | major |
- **Problem:** "surface the failure prominently" and "until retry succeeds" are both undefined — there is no specified retry flow elsewhere in the document, and "prominently" is a vague qualifier.
- **Recommendation:** Define the explicit retry mechanism (or remove the reference) and replace "prominently" with a concrete UI requirement, e.g., "a persistent banner naming the failure reason at the top of the summary view".

#### ADV-19 — "Step-up authentication" never defined

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** "Step-up authentication" is not defined anywhere in the document — the factor required (password re-entry, MFA challenge, biometric) and its scope (per action, per session) are unspecified.
- **Recommendation:** Specify the step-up factor and cadence, e.g., "password re-entry required on first approve/reject per session; valid for 10 minutes thereafter".

#### ADV-20 — Vague "Process" verb plus dual-status-field ambiguity

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.1
- **Evidence:**
  > - Process uploaded files into Transactions; expose the file's lifecycle via `LastExecutedActivityName` / `CurrentStatus` on the File Log.
- **Problem:** "Process" is a vague verb and the slash between two field names leaves it unclear which field is canonical for the user-visible status versus the operational status.
- **Recommendation:** Replace with concrete behaviour, e.g., "Parse uploaded files into Transaction records; `LastExecutedActivityName` is the canonical user-visible status, `CurrentStatus` is the operational complement (per §7)".

#### ADV-21 — CurrentStatus described as "Operational status complement" with no enumeration

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §7 Entity: File Log
- **Evidence:**
  > | CurrentStatus | string | no | — | Operational status complement to LastExecutedActivityName. |
- **Problem:** "Operational status complement" is undefined — the enumeration, the relationship to LastExecutedActivityName, and when it differs are all unspecified.
- **Recommendation:** Either enumerate CurrentStatus values and define when it diverges from LastExecutedActivityName, or remove the field from the entity definition.

#### ADV-22 — "Status shown in UI" is vague

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §5 File Upload
- **Evidence:**
  > | Steps | 1. Select file (drag & drop supported). 2. Provide FileSettingId, FileSettingName, FileName. 3. Submit upload. 4. System creates File Log. 5. Status shown in UI. |
- **Problem:** Step 5 "Status shown in UI" is vague — which status (upload acknowledgement, parse result, File State), where in the UI, and at what point are all unspecified.
- **Recommendation:** Replace step 5 with, e.g., "5. UI displays the new File Log row with initial state Uploaded in the File Log Overview; transitions to Processing/Completed/Failed are reflected per BR-06 semantics".

#### ADV-23 — "transaction detail surface" is not a defined view

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.3
- **Evidence:**
  > - Persist User records, including bcrypt-hashed credentials.- Capture the rejecting user's note against the Transaction; expose it on the transaction detail surface.
- **Problem:** "the transaction detail surface" is not a defined entity in §5 task flows or §6.4 user-facing — "surface" is a vague noun and the document does not specify any "transaction detail" view.
- **Recommendation:** Reference a defined task flow or screen, e.g., "expose the user note alongside the row in §5 Transaction Table and in §5 File Summary View", or add an explicit Transaction Detail flow in §5.

#### ADV-24 — "Optional for Importer" MFA wording is ambiguous

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** "Optional for Importer" is ambiguous — it does not state who enables MFA (self-service, admin-set), what factor types are accepted, or whether the optionality is per-user or system-wide.
- **Recommendation:** Specify factor and enablement semantics, e.g., "Importer: TOTP available as user-enabled opt-in; Approver: TOTP mandatory at first login, enforced server-side".

#### ADV-25 — "Counts may be incomplete" uses hedge "may" for a deterministic state

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §5 File Summary View
- **Evidence:**
  > | Exception paths | If the file is still Processing or Failed, counts may be incomplete; the view shows the file's current state prominently. |
- **Problem:** "Counts may be incomplete" uses the hedge "may" for a deterministic condition (Processing/Failed implies partial counts), and "prominently" is a vague qualifier as in BR-07.
- **Recommendation:** Replace with deterministic prose, e.g., "While the file is Processing or Failed, status counts reflect only the transactions parsed so far; a banner at the top of the summary view names the current File State".

#### ADV-26 — Empty-state CTA rule's "where applicable" is undefined

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.4
- **Evidence:**
  > - Empty-state copy names the entity ("No transactions yet", "No file logs yet") and offers the primary creation CTA where applicable.
- **Problem:** "where applicable" is a vague conditional — the document does not name which screens this applies to, leaving the empty-state CTA rule under-specified for the Transaction Table.
- **Recommendation:** Enumerate the screens, e.g., "... offers the upload CTA on File Log Overview to Importers only (per §5); the Transaction Table empty state offers no creation CTA".

#### ADV-27 — "complexity per security policy" references undefined external policy

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §7 Entity: User
- **Evidence:**
  > | Password | string (write-only) | yes (create) | min length 8; complexity per security policy | Stored as bcrypt hash; never returned. |
- **Problem:** "complexity per security policy" references an external, undefined policy — the actual character-class, length-upper-bound, and disallowed-pattern rules are unspecified.
- **Recommendation:** Inline the concrete policy, e.g., "min length 12, must include one of each: lowercase, uppercase, digit, symbol; max length 128; rejects top-1000 common passwords".

#### ADV-28 — "one or more files per business day" lacks upper bound

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §10
- **Evidence:**
  > | Frequency | Daily ingestion cycle, one or more files per business day per Importer | inferred |
- **Problem:** "one or more files" is a vague quantifier that does not bound the upper end, leaving capacity planning and rate-limiting requirements unspecified.
- **Recommendation:** Provide an explicit upper bound, e.g., "1–10 files per Importer per business day, peak 20".

#### ADV-29 — "screen-reader semantics on status badges" lacks ARIA contract

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.5
- **Evidence:**
  > - WCAG 2.2 AA conformance, full keyboard reach for all primary actions, screen-reader semantics on status badges.
- **Problem:** "screen-reader semantics on status badges" is vague — it does not specify role, accessible name source, or live-region behaviour on transition.
- **Recommendation:** Specify the ARIA contract, e.g., "status badges expose role=status with accessible name '{status} - {transaction reference}'; transitions per BR-06 announce via aria-live=polite".

#### ADV-30 — "business hours" undefined for uptime target

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.3
- **Evidence:**
  > | Target uptime | 99.5 % during business hours; 99.0 % overall | inferred |
- **Problem:** "business hours" is undefined — timezone, days-of-week, and start/end times are all unspecified, making the uptime target unmeasurable.
- **Recommendation:** Define the window explicitly, e.g., "business hours = Mon–Fri 07:00–18:00 SAST excluding South African public holidays".

---

## Dimension 3 — Testability & Verifiability

### Findings

#### ADV-31 — WCAG predicate untestable without scope and method

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.5
- **Evidence:**
  > WCAG 2.2 AA conformance, full keyboard reach for all primary actions, screen-reader semantics on status badges.
- **Problem:** Accessibility requirement names a standard and a vague scope but provides no enumerated primary actions, no audit tool/sample, and no pass/fail predicate for "screen-reader semantics".
- **Recommendation:** Enumerate the primary actions in scope (Upload, Approve, Reject, Export, Logout, Sort, Filter, Paginate) and specify the verification method (e.g., axe-core 0 violations on the listed routes + NVDA reads status badge as '<label>, status') as the pass criterion.

#### ADV-32 — Performance thresholds without sample/profile/method

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.2
- **Evidence:**
  > | p95 page TTI on Transaction Table | ≤ 2 s for ≤ 1 000 rows | inferred |
- **Problem:** Performance targets give thresholds but omit sample size, network/device profile, and measurement methodology, so a tester cannot reproduce the test.
- **Recommendation:** Add measurement context per row: sample size (e.g., N≥200 sessions), network profile (e.g., Fast 3G or wired), device class (e.g., mid-range laptop / Lighthouse mobile preset), and tool (e.g., Lighthouse, server APM).

#### ADV-33 — Uptime predicate unmeasurable

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.3
- **Evidence:**
  > | Target uptime | 99.5 % during business hours; 99.0 % overall | inferred |
- **Problem:** Availability target references "business hours" without defining them, no measurement window, and no definition of "down" versus "degraded".
- **Recommendation:** Define business hours (e.g., Mon-Fri 07:00-18:00 Africa/Johannesburg), measurement window (rolling 30 days), and "down" predicate (e.g., HTTP 5xx on /v1/healthz for ≥1 minute).

#### ADV-34 — Step-up auth requirement has no testable factor or expiry

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** Step-up auth is mandated but the factor, trigger window, and expiry are unspecified, so no test can decide whether a given step-up implementation satisfies the requirement.
- **Recommendation:** Specify the factor (e.g., TOTP), trigger (every action vs. once per session/N minutes), expiry (e.g., 5 minutes), and failure behaviour (block action, no partial state).

#### ADV-35 — BR-06 has no latency predicate

- **Severity:** Major
- **Disposition:** Patch
- **Location:** BR-06
- **Evidence:**
  > When a transaction's status changes (Approved or Rejected), then the new status must be reflected in the transaction table without a manual refresh.
- **Problem:** BR-06 prescribes "without a manual refresh" but gives no latency bound, so "reflected eventually" would pass — there is no failing-test predicate.
- **Recommendation:** Add a numeric bound, e.g., "the row's Status cell updates within 2 s of the server confirming the action, on the originating client; cross-tab updates within 5 s".

#### ADV-36 — Password policy not enumerated; acceptance undecidable

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Password storage | Server-side bcrypt hash; plaintext password transmitted over HTTPS only. |
- **Problem:** Password rule (§7 Entity User) says "complexity per security policy" but no policy is enumerated, so a tester cannot decide whether a given password is accepted or rejected.
- **Recommendation:** Enumerate the policy in the doc (e.g., min length 12, ≥1 upper, ≥1 lower, ≥1 digit, ≥1 symbol; reject top-100k breached passwords) so the validation rule is decidable from this document alone.

#### ADV-37 — "No PII in toasts/console" predicate lacks PII enumeration

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.4
- **Evidence:**
  > No PII is rendered in error toasts or browser console.
- **Problem:** Negative predicate over PII is not testable without an enumeration of which fields count as PII for this product.
- **Recommendation:** Enumerate the PII fields (e.g., Email, AccountNumber, FirstName, LastName, UserNote when it contains free text) and define the test (e.g., scrape DOM toasts + console output during the standard test suite; assert none of the listed fields appears).

#### ADV-38 — Goal-level "Quality signals" are wishes without numeric thresholds

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §4.1
- **Evidence:**
  > | G-01 | Upload transaction files for processing. | Speed-to-confidence, error visibility | top-level | full-page upload panel | drag-and-drop with progress |
- **Problem:** Goal-level "Quality signals" (Speed-to-confidence, Accuracy, throughput, decision confidence, At-a-glance status) are wishes — no numeric thresholds, so completion of a goal is not decidable.
- **Recommendation:** Bind each quality signal to a measurable proxy (e.g., Speed-to-confidence → time-from-file-select-to-success-toast ≤ 3 s p95; Accuracy → 0 unintended approvals in usability test n=8) or remove the signal column from the doc as informational only.

#### ADV-39 — File Upload exception path not decidable from doc alone

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 File Upload
- **Evidence:**
  > | Steps | 1. Select file (drag & drop supported). 2. Provide FileSettingId, FileSettingName, FileName. 3. Submit upload. 4. System creates File Log. 5. Status shown in UI. |
- **Problem:** "Status shown in UI" and "Success / failure feedback is rendered after upload" do not enumerate which statuses or which messages, so the exception path is not decidable from the doc alone.
- **Recommendation:** Enumerate the post-submit states the UI must render (e.g., "Uploading…" progress, "Upload complete — File Log #N created" toast, "Upload failed — <reason category>" banner) and the trigger condition for each.

#### ADV-40 — File Summary Processing/Failed UX has no testable predicate

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 File Summary View
- **Evidence:**
  > | Exception paths | If the file is still Processing or Failed, counts may be incomplete; the view shows the file's current state prominently. |
- **Problem:** "Counts may be incomplete" and "shows … prominently" are wishes — no testable predicate for what the user sees when Processing vs Failed.
- **Recommendation:** Replace with decidable rules, e.g., "Processing → counts hidden, banner: \"File still processing — counts available on completion\"; Failed → counts hidden, red banner with retry CTA per BR-07".

#### ADV-41 — Toast duration range 4–8 s is non-deterministic

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.4
- **Evidence:**
  > Transient confirmations (approval / rejection / export complete) use toasts auto-dismissing in 4–8 s, top-right.
- **Problem:** A 4–8 s range admits any value in the interval, so two implementations could both pass yet diverge; no per-event mapping.
- **Recommendation:** Pick a single duration per event (e.g., approval/rejection 4 s, export complete 8 s) or define the range as "minimum 4 s, maximum 8 s" with an explicit rationale and a single test value.

#### ADV-42 — "2–3 key columns" responsive card spec is non-deterministic

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.4
- **Evidence:**
  > On screens below 768 px, tables collapse into a vertical card list (primary identifier + 2–3 key columns + overflow).
- **Problem:** "2-3 key columns" is non-deterministic across the two tables (File Logs, Transactions); a tester cannot decide which columns must appear on the card.
- **Recommendation:** Specify per table, e.g., "File Logs card: FileName (primary), Status, ProcessDate; Transactions card: Reference (primary), Amount+Currency, Status; remaining columns under an Overflow disclosure."

#### ADV-43 — Authentication generic-error rule does not pin the message string

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §5 Authentication
- **Evidence:**
  > On failure → error state with a generic message that does not reveal which field was incorrect.
- **Problem:** Generic-message rule is correct in intent but does not pin the actual string, so two implementations rendering different copy could each claim conformance.
- **Recommendation:** Pin the canonical copy (e.g., "Invalid email or password.") in §6.4 or §6.6.1 and reference it from the flow so the test asserts an exact string.

#### ADV-44 — Audit list excludes failure events; coverage test undefined

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.4
- **Evidence:**
  > Audit trail: every approve, reject, upload, login, and logout event is recorded with `LastChangedUser` and `LastChangedDate`; retain 7 years.
- **Problem:** Audit list omits failure events (failed login, failed upload, failed approve/reject) so the test "audit row exists for every attempted action" is undefined.
- **Recommendation:** State explicitly whether failed attempts are audited (recommended: yes, with outcome field success|failure and failure reason category) and add the outcome field to the audit schema.

---

## Dimension 4 — Scope & MVP Boundaries

### Findings

#### ADV-45 — No MVP designation; every requirement is implicitly in scope

- **Severity:** Blocker
- **Disposition:** Reject
- **Location:** §1\|§6\|§10
- **Evidence:**
  > **Created:** 2026-05-13 · **Status:** final · **Last finalised at:** 2026-05-13
- **Problem:** The document is marked Status: final but contains no MVP designation, no release-scope statement, and no phase tagging — every one of the ~30 requirements is implicitly MVP, which is the classic scope-creep signature for a 501-line spec.
- **Recommendation:** Add a top-level scope section (e.g., §1.1 "Release scope") that names the MVP release, lists which §6 items are MVP vs deferred, and gates each requirement explicitly.

#### ADV-46 — No "Out of scope" section; negative boundary undeclared

- **Severity:** Blocker
- **Disposition:** Reject
- **Location:** §6\|§10
- **Evidence:**
  > ## 10. Volumes
- **Problem:** There is no "Out of scope" section anywhere in the doc; §10 ends the document, so a downstream engineer has no negative boundary and must infer that everything not mentioned (e.g., bulk approve, transaction edit, role admin, file delete, file retry UI) is or is not in scope.
- **Recommendation:** Add an explicit §11 "Out of scope" enumerating excluded behaviours (e.g., bulk approve, transaction editing, user/role administration UI, file deletion, retry of Failed file logs, MFA enrolment UI) so the negative boundary is unambiguous.

#### ADV-47 — MFA and step-up auth straddle the MVP cut line

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.1
- **Evidence:**
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** MFA for Approvers and step-up authentication for approve/reject are listed as "inferred" defaults in NFRs but carry weeks of engineering cost (enrolment UI, factor selection, recovery flows) and are not tagged as MVP, post-MVP, or stretch — this requirement straddles the cut line.
- **Recommendation:** Either move MFA + step-up auth to an explicit "post-MVP / phase 2" section, or commit them to MVP with a sized cost and an enrolment flow added to §5; do not leave them as untagged inferred NFRs.

#### ADV-48 — All §6.6.1 inferred NFRs are untagged for scope

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.1
- **Evidence:**
  > | Account lockout policy | 5 failed attempts → 15-minute cooldown; cooldown resets on successful authentication | inferred |
- **Problem:** Account lockout, idle-warning lead-time, idle/absolute session timeouts, and step-up re-auth are all stated as inferred defaults with concrete numeric targets but no scope tag — each implies non-trivial backend state machines that may or may not be in MVP scope.
- **Recommendation:** Tag each §6.6.1 line as MVP or post-MVP, and where it is MVP add a confirming source other than "inferred (financial domain default)" so the cost is justified.

#### ADV-49 — POPIA + 7-year retention bundled into MVP without scope tag

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.4
- **Evidence:**
  > Audit trail: every approve, reject, upload, login, and logout event is recorded with `LastChangedUser` and `LastChangedDate`; retain 7 years.
- **Problem:** POPIA compliance and a 7-year audit retention obligation are stated without scope tagging or cost discussion — POPIA conformance alone is a multi-month workstream (DSAR handling, breach notification, data-minimisation review) and cannot be silently bundled into MVP.
- **Recommendation:** Split §6.6.4 into "MVP audit logging" (event capture only) and "post-MVP compliance programme" (POPIA conformance, retention enforcement, DSAR tooling), and tag each line accordingly.

#### ADV-50 — Responsive <768 px requirement bundled with core flows

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.4\|line-345
- **Evidence:**
  > On screens below 768 px, tables collapse into a vertical card list (primary identifier + 2–3 key columns + overflow).
- **Problem:** A responsive mobile breakpoint behaviour is mixed in with desktop table requirements without any scope tag — given §3 personas describe daily desk-bound use, the mobile experience is plausibly post-MVP but is currently mandated alongside core flows.
- **Recommendation:** Move the <768 px responsive behaviour to a tagged "post-MVP" subsection, or confirm mobile is in MVP and add mobile-specific personas/flows to §3 and §5.

#### ADV-51 — BR-07 retry is either an out-of-scope feature or a missing MVP flow

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.2\|BR-07
- **Evidence:**
  > When a file log is in Failed state, then the file summary view must surface the failure prominently and inhibit drill-down into transactions until retry succeeds.
- **Problem:** BR-07 references "retry succeeds" but no retry flow exists in §5 task flows and no retry requirement appears in §6.1 — this is either an out-of-scope feature smuggled into a business rule or a missing MVP flow, and the doc never decides which.
- **Recommendation:** Either add a "Retry Failed File" flow to §5 and a matching §6.1 functional requirement (MVP), or rephrase BR-07 to remove the retry reference and tag retry as out-of-scope.

#### ADV-52 — Importer logout silently out of scope by omission

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.1\|line-323
- **Evidence:**
  > Allow Approvers to log out via an endpoint that invalidates the session cookie.
- **Problem:** The functional list grants logout only to Approvers, yet Importers also authenticate (§5 Authentication, §3 Importer) and §6.5 RBAC grants Importers "X" on Authentication — leaving Importer logout silently out of scope by omission rather than by explicit exclusion.
- **Recommendation:** Either extend the bullet to "Allow all authenticated users to log out…" (MVP) or add Importer-logout to an explicit out-of-scope list and justify the asymmetry.

#### ADV-53 — Performance ceilings inconsistent with §10 volume range

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.2
- **Evidence:**
  > | p95 page TTI on Transaction Table | ≤ 2 s for ≤ 1 000 rows | inferred |
- **Problem:** Performance targets reference a 1 000-row ceiling and a 10 000-row CSV ceiling, but §10 Volumes allows 10⁵ transactions per active file log — the perf NFR and the volume NFR are inconsistent and neither states which bound is MVP-binding.
- **Recommendation:** Reconcile §6.6.2 ceilings with §10 volume ranges and annotate which row-count tier is the MVP performance commitment.

---

## Dimension 5 — Dependency & Ordering

### Findings

#### ADV-54 — FileSetting referenced but never introduced in §2

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §7 Entity: File Log, line 431
- **Evidence:**
  > | SettingId | int | yes | references FileSetting.Id | Upload-time setting reference. |
- **Problem:** FileSetting is used as a foreign-key target in §7 and named in §9, but is never introduced as a concept in §2 Domain model, so the entity referenced by SettingId has no defined source.
- **Recommendation:** Add FileSetting as a concept in §2.1 with definition and persistence, and add a "File Log belongs to FileSetting [N:1]" relationship in §2.2, before §7 references it.

#### ADV-55 — RoleRead type referenced but never defined

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §7 Entity: User, line 412
- **Evidence:**
  > | Roles | list<RoleRead> | yes | non-empty | Drives RBAC. |
- **Problem:** The type RoleRead is used for the User.Roles field but is never defined as an entity, enum, or DTO anywhere in the document, so the data shape an engineer must implement is unknown.
- **Recommendation:** Either define RoleRead as an entity/enum in §7 (or §2) before this reference, or change the type to the existing "Roles" enum already declared as { Importer, Approver } on line 420.

#### ADV-56 — Step-up dependency on undefined capability

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.1 Re-auth scope, line 366
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** Step-up authentication is mandated for approve/reject but the Approve and Reject flows in §5 contain no step-up step and no step-up mechanism is defined anywhere in the doc, so the dependency on this capability is undiscoverable from the flow definitions.
- **Recommendation:** Either remove the step-up requirement, or add a step-up step to the Approve Transaction and Reject Transaction flows in §5 and define the step-up mechanism as a concept before §6.6.1 references it.

#### ADV-57 — MFA dependency between Authentication and Approver login is invisible

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.1 MFA requirement, line 368
- **Evidence:**
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** MFA is mandated for Approvers but the Authentication flow in §5 (line 220) describes only "email + password" with no MFA step, so the dependency between Authentication and the MFA capability needed before Approver login is undiscoverable.
- **Recommendation:** Add an MFA step to the Authentication flow in §5 (or a separate MFA enrolment flow) and sequence it as a dependency of any Approver-role-gated feature before §6.6.1 declares MFA required.

#### ADV-58 — BR-06 implies a delivery channel never defined

- **Severity:** Major
- **Disposition:** Defer
- **Location:** BR-06, line 334
- **Evidence:**
  > BR-06 | When a transaction's status changes (Approved or Rejected), then the new status must be reflected in the transaction table without a manual refresh.
- **Problem:** Real-time status reflection without manual refresh implies a push/poll mechanism (e.g., websocket, SSE, or background polling) that is not defined anywhere in the doc, so the dependency this rule places on a delivery channel is invisible to an engineer.
- **Recommendation:** Add a non-functional or architectural note stating the chosen update channel (e.g., SSE/poll/optimistic local update) as a dependency of BR-06, sequenced before BR-06 in §6.2 or §6.6.

#### ADV-59 — Goal dependencies (G-02/G-03/G-04 → G-01) not recorded

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §4.1 G-02, G-03, G-04, lines 152-154
- **Evidence:**
  > | G-04 | Monitor the processing status of uploaded files. | At-a-glance status, drill-down to detail | top-level | dashboard list | tabular file log with status column |
- **Problem:** G-02 (approve/reject), G-03 (export filtered), and G-04 (monitor) all logically depend on G-01 (upload) producing files and transactions first, but no explicit ordering note records that dependency, so the goals catalogue does not communicate implementation order.
- **Recommendation:** Add a "Depends on" column (or inline note) to §4.1 declaring G-02/G-03/G-04 depend on G-01 so an engineer can derive a buildable order from the catalogue.

#### ADV-60 — §6.1 forward-references fields defined later in §7

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.1 Functional, line 320
- **Evidence:**
  > Process uploaded files into Transactions; expose the file's lifecycle via `LastExecutedActivityName` / `CurrentStatus` on the File Log.
- **Problem:** §6.1 references the fields LastExecutedActivityName and CurrentStatus before they are defined (§7 Entity: File Log appears later at lines 422-433), so an implementer reading top-down does not know what these fields are or which is authoritative.
- **Recommendation:** Either forward-reference §7 explicitly on this line, or restate the canonical field definition (one of { Uploaded, Processing, Completed, Failed }) inline so §6.1 is self-contained.

#### ADV-61 — RBAC matrix lists User resource with no upstream capability

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.5 RBAC matrix header, line 352
- **Evidence:**
  > | Role (→ §3) | User | File Log | Transaction | Authentication | File Upload | File Log Overview | Transaction Table | Search & Filtering | Approve Transaction | Reject Transaction | Export Transactions | File Summary |
- **Problem:** The RBAC matrix lists "User" as a resource with both roles assigned R access, but the doc defines no User-management flow in §5 and no functional requirement for reading other users, so the resource has access cells with no upstream capability to implement.
- **Recommendation:** Either remove the User column from §6.5 since no functional requirement supports it, or add a User-management flow in §5 and a corresponding requirement in §6.1 before §6.5 grants access.

---

## Dimension 6 — Consistency & Internal Conflict

### Findings

#### ADV-62 — §6.6.1 step-up auth contradicted by Approve/Reject flows

- **Severity:** Blocker
- **Disposition:** Defer
- **Location:** §6.6.1 vs §5 Approve Transaction / §5 Reject Transaction
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** §6.6.1 mandates step-up authentication for approve and reject, but the Approve Transaction flow lists only a confirmation modal and the Reject Transaction flow lists only a mandatory note — neither flow includes a re-authentication step.
- **Recommendation:** Either add a step-up re-auth step to the Approve and Reject flows in §5 or remove the step-up requirement from §6.6.1.

#### ADV-63 — §6.6.1 MFA contradicted by §5 Authentication flow

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.1 vs §5 Authentication
- **Evidence:**
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** §6.6.1 requires MFA for Approvers, but §5 Authentication flow's Steps list only email+password submission with no MFA step or decision point, contradicting the policy.
- **Recommendation:** Add an MFA challenge step (conditional on role=Approver) to the Authentication flow in §5 or relax the MFA policy in §6.6.1.

#### ADV-64 — Logout requirement scope contradicts §6.6.1 and §6.6.4

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.1 vs §6.6.1 / §6.6.4
- **Evidence:**
  > - Provide a file summary view showing total records and a count by status (Imported / Approved / Rejected).- Allow Approvers to log out via an endpoint that invalidates the session cookie.
- **Problem:** §6.1 scopes the logout endpoint to Approvers only, but §6.6.1 describes the logout cookie clearance generically (POST /v1/auth/logout) and §6.6.4 records logout events as a generic audit event, implying logout applies to all roles.
- **Recommendation:** Reword the §6.1 logout requirement to apply to all authenticated users (both Importer and Approver).

#### ADV-65 — §2.4 Transaction class omits fields defined in §7

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §2.4 vs §7 Entity: Transaction
- **Evidence:**
  >     class Transaction {
  >       +Id
  >       +FileLogId
  >       +Reference
  >       +TransactionDate
  >       +AccountNumber
- **Problem:** The Transaction class in the §2.4 Mermaid diagram omits FileName, Description, TransactionType, LastChangedUser and LastChangedDate, all of which are defined as Transaction fields in §7, so the diagram and the data-entity table disagree on the entity's shape.
- **Recommendation:** Update the §2.4 Mermaid Transaction class to include all fields enumerated in §7 (or explicitly mark §2.4 as a conceptual subset).

#### ADV-66 — §2.4 FileLog class omits required fields incl. LastExecutedActivityName

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §2.4 vs §7 Entity: File Log
- **Evidence:**
  >     class FileLog {
  >       +Id
  >       +FileName
  >       +RecordCount
  >       +ProcessDate
  >       +CurrentStatus
- **Problem:** The §2.4 Mermaid FileLog class lists CurrentStatus but omits LastExecutedActivityName, SettingId, SettingName, FileHash, LastChangedUser, and LastChangedDate, contradicting the authoritative File Log shape in §7 where LastExecutedActivityName is the required status field.
- **Recommendation:** Reconcile §2.4 with §7 by adding LastExecutedActivityName and the other File Log fields to the diagram (or annotate the diagram as a conceptual subset).

#### ADV-67 — RecordCount typed as string contradicts its usage and the §2.4 diagram

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §7 Entity: File Log RecordCount vs §5 File Log Overview
- **Evidence:**
  > | RecordCount | string | yes | numeric | Number of transactions parsed from the file; API returns as string. |
- **Problem:** §7 declares RecordCount as type string with a "numeric" validation, but the §5 File Log Overview flow surfaces it as a "Record Count" column and the §2.4 diagram lists it as an unqualified +RecordCount, implying a numeric type — the string typing contradicts its usage everywhere else.
- **Recommendation:** Change RecordCount to integer in §7 (treat the string-on-the-wire as a serialization detail noted separately) so the type is consistent with its semantics and display.

#### ADV-68 — Authentication flow does not mention lockout state per §6.6.1

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.1 Account lockout vs §5 Authentication
- **Evidence:**
  > | Account lockout policy | 5 failed attempts → 15-minute cooldown; cooldown resets on successful authentication | inferred |
- **Problem:** §6.6.1 specifies a 5-attempt lockout with a 15-minute cooldown, but §5 Authentication's Exception paths describe only a generic error message and do not mention lockout behaviour or a locked-out state, so the flow contradicts the policy by silence.
- **Recommendation:** Add a lockout exception path to §5 Authentication that references the §6.6.1 lockout policy (and surfaces a locked-account state to the UI).

#### ADV-69 — Approver/Transaction Update cell conflicts with per-action columns

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.5 RBAC matrix Approver Transaction cell vs §6.5 action vocabulary
- **Evidence:**
  > | Approver | R | R | R U†BR-01 | X | — | X | X | X | A†BR-01 | A†BR-02 | X | X |
- **Problem:** The Approver/Transaction cell grants "U†BR-01" (update) on the Transaction resource, but the action vocabulary reserves "A" for approve and the matrix already grants A†BR-01 / A†BR-02 on the Approve / Reject columns — granting U on Transaction therefore contradicts the per-action columns and lets an Approver update arbitrary transaction fields beyond approve/reject.
- **Recommendation:** Drop the "U†BR-01" from the Approver/Transaction cell (leaving R) so update authority lives only in the dedicated Approve / Reject columns.

---

## Dimension 7 — Edge Cases & Error Handling

### Findings

#### ADV-70 — File Upload contract names no size/type/virus/failure mode

- **Severity:** Blocker
- **Disposition:** Defer
- **Location:** §5 File Upload
- **Evidence:**
  > Steps | 1. Select file (drag & drop supported). 2. Provide FileSettingId, FileSettingName, FileName. 3. Submit upload. 4. System creates File Log. 5. Status shown in UI.
- **Problem:** The File Upload flow names no maximum file size, no allowed file types/extensions, no virus/malware scan, and no specific failure modes (oversize, wrong type, malformed content) — exactly the canonical "file upload requirement that names no max size, no virus check, no failure mode" anti-pattern.
- **Recommendation:** Add explicit limits and validation to §5 File Upload and §6.1: max file size (e.g., 10 MB), permitted extensions/MIME types, antivirus/content-scan step, and a named failure mode per invalid case (oversize → toast + retained form; bad type → reject pre-upload; scan-fail → quarantine state).

#### ADV-71 — Approval declared reversible by an undefined separate workflow

- **Severity:** Blocker
- **Disposition:** Defer
- **Location:** §5 Approve Transaction; §4.2 Approver story
- **Evidence:**
  > Context (frequency / expertise / stakes) | Many per day; senior reviewer; reversible only by separate workflow.
- **Problem:** Approval is declared reversible "only by separate workflow" but that recovery/undo workflow is never defined anywhere in the document, leaving the recovery path required by Dimension 7 unspecified.
- **Recommendation:** Either add a "Revert Approval" / "Reopen Transaction" flow in §5 with its own BR and RBAC row, or explicitly state in §6.2 that approval is irreversible and remove the "reversible only by separate workflow" phrasing.

#### ADV-72 — BR-06 lacks transport, concurrency, and offline behaviour

- **Severity:** Blocker
- **Disposition:** Defer
- **Location:** BR-06; §5 Transaction Table
- **Evidence:**
  > BR-06 | When a transaction's status changes (Approved or Rejected), then the new status must be reflected in the transaction table without a manual refresh.
- **Problem:** BR-06 mandates live status reflection but the document specifies no transport (polling, SSE, WebSocket), no concurrent-edit conflict model when two Approvers act on the same row, and no behaviour when the live channel is offline.
- **Recommendation:** Specify the refresh mechanism (e.g., poll every N seconds or SSE on /v1/transactions/stream), the last-write-wins vs. optimistic-lock policy for concurrent approve/reject on the same transaction, and the UI fallback when the live channel is unavailable.

#### ADV-73 — Mandatory reject note lacks length and whitespace validation

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 Reject Transaction; §7 Entity: Transaction (UserNote)
- **Evidence:**
  > | UserNote | string | yes when Status = Rejected | non-empty on Reject | Rejection rationale. |
- **Problem:** The mandatory rejection note has no maximum-length validation, no minimum content rule beyond "non-empty", and no behaviour for whitespace-only input — leaving the maximum-size / input-validation edge case unspecified.
- **Recommendation:** Add validation in §7 and §5 Reject Transaction: trim whitespace, reject whitespace-only, enforce 1–500 (or similar) character bound, and surface inline validation when the bound is breached.

#### ADV-74 — Lockout policy lacks user-facing UX and recovery path

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.1 Security & session
- **Evidence:**
  > | Account lockout policy | 5 failed attempts → 15-minute cooldown; cooldown resets on successful authentication | inferred |
- **Problem:** The lockout policy names no user-facing UX (what the locked user sees, whether the generic-error pattern from BR-05 still applies, whether countdown is shown, whether email notification fires) and names no recovery path (password reset, admin unlock).
- **Recommendation:** Add a §5 Account Lockout sub-flow specifying the message shown to the locked user (generic per BR-05), whether a countdown is exposed, and the recovery path (self-service password reset and/or admin unlock).

#### ADV-75 — Step-up auth has no flow, no UX, no failure mode

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.1 Security & session
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** Step-up auth is required for approve/reject but no flow is defined in §5 — neither the trigger (every action / per-session / time-based), the prompt UX, the failure mode, nor the impact on the existing confirmation modal is specified.
- **Recommendation:** Add a §5 Step-up Authentication flow defining when re-auth is demanded, what the user sees, what happens on cancel/failure, and how it composes with the BR-01 confirmation modal.

#### ADV-76 — Idle timeout has no warning UX or in-flight work preservation

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.1 Security & session
- **Evidence:**
  > | Idle session timeout | 15 minutes | inferred (financial domain default) | | Idle warning lead-time | 60 seconds before idle logout | inferred (financial domain default) |
- **Problem:** Idle timeout and a 60-second warning are stated, but no flow specifies the warning UI, the "extend session" control, or what happens to in-flight work (an unsaved rejection note, an in-progress export) when the timeout fires.
- **Recommendation:** Add a §5 Idle Timeout flow covering the warning banner/modal, the "Stay signed in" control, and the preservation/discard policy for unsaved form state (notably the Reject note draft).

#### ADV-77 — BR-07 "retry" with no Retry flow, RBAC, or failure mode

- **Severity:** Major
- **Disposition:** Defer
- **Location:** BR-07; §5 File Summary View
- **Evidence:**
  > BR-07 | When a file log is in Failed state, then the file summary view must surface the failure prominently and inhibit drill-down into transactions until retry succeeds. | UI | → §2.3 File Log invariant | major |
- **Problem:** BR-07 references a "retry" that succeeds, but no Retry flow is defined in §5, no retry trigger/permission is set, and no RBAC cell in §6.5 grants "retry file" to any role.
- **Recommendation:** Add a §5 Retry Failed File flow, a corresponding RBAC column or action vocabulary entry in §6.5, and the failure-mode UX when retry itself fails (e.g., escalate to a Failed-permanently state).

#### ADV-78 — Export over 10 000 rows: behaviour undefined

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §5 Export Transactions; §6.6.2 Performance
- **Evidence:**
  > | CSV export ready-to-download | ≤ 3 s for ≤ 10 000 rows | inferred |
- **Problem:** Performance bounds the export at ≤10 000 rows but neither §5 Export Transactions nor §6.1 specifies what happens above that limit (truncate? warn? async job? hard cap?), leaving the maximum-size edge case unspecified.
- **Recommendation:** Specify the over-limit behaviour in §5 Export Transactions: e.g., hard cap with a warning toast, asynchronous export with email-when-ready, or pagination across multiple CSV downloads.

#### ADV-79 — Network failure behaviour for mutating flows undefined

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §5 Approve Transaction; §5 Reject Transaction; §5 Export Transactions; §5 File Upload
- **Evidence:**
  > Steps | 1. Select transaction. 2. Click Approve. 3. Confirm action in modal. 4. Status updates to Approved.
- **Problem:** No flow specifies network-failure behaviour for approve/reject/upload/export — what the UI shows on timeout, what state is preserved (e.g., the typed reject note), and whether retries are idempotent (the same approval clicked twice on a flaky connection).
- **Recommendation:** Add an Exception path to each mutating flow naming the UI state on network failure (e.g., inline error + retry button, retained form fields) and require server endpoints to be idempotent on retry (idempotency key or status-precondition check).

#### ADV-80 — Partial-failure parse case has no defined surface

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §5 File Upload; §6.1
- **Evidence:**
  > Exception paths | Success / failure feedback is rendered after upload. On failure, the file is not parsed and no File Log row is created in a Completed state.
- **Problem:** The partial-failure case where the file is parsed but some rows are malformed (8/10 succeed) is unspecified — the only outcomes named are "Completed" or "Failed", with no partial-success state, no per-row error report, and no rejected-rows surface.
- **Recommendation:** Either define a Partial / CompletedWithErrors lifecycle state with a per-row error report on the File Summary View, or explicitly state the policy is all-or-nothing and reject the whole file on any row error.

#### ADV-81 — Authorization-failure UX undefined for deep-link role bypass

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §5 Transaction Table; §6.4
- **Evidence:**
  > Role-conditional behaviour | Approve / Reject row actions are hidden for Importers.
- **Problem:** The document specifies hiding role-restricted controls but does not specify the authorization-failure UX when an Importer reaches an Approver-only URL directly (deep-link, browser back, copy-pasted URL) — the canonical Dimension 7 authorization-failure case.
- **Recommendation:** Add a §6.4 or §5 Authentication clause: unauthorized navigation returns a 403 surface that names the action ("You do not have permission to approve transactions") and offers a route back to the user's role landing page.

#### ADV-82 — Email-format validation UX unspecified at login

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §7 Entity: User; §6.1
- **Evidence:**
  > | Email | string | yes | RFC 5322 format; unique | Login identifier. |
- **Problem:** Email validation is stated as "RFC 5322 format" but neither §6.1 nor the Authentication flow names the user-facing validation behaviour (when it fires, what message is shown, whether it composes with the BR-05 generic-error rule at login).
- **Recommendation:** Add to §6.4 / §5 Authentication: invalid email format is flagged on blur with a specific inline message pre-submit; on submit, BR-05's generic message overrides any field-specific feedback.

---

## Dimension 8 — Feasibility & Constraints

### Findings

#### ADV-83 — POPIA stated as "implied"; no concrete obligations

- **Severity:** Blocker
- **Disposition:** Defer
- **Location:** §6.6.4
- **Evidence:**
  > POPIA (South Africa) — implied by the use of ZAR currency in the sample dataset and South African account-number formats.
- **Problem:** POPIA treatment is declared as "implied" rather than concretely specified — no data residency, no consent/lawful-basis statement, no PII retention windows (only the audit-trail retention is set), and no data-subject-rights handling, despite the system storing AccountNumber and user PII.
- **Recommendation:** Replace the "implied" line with a concrete POPIA block specifying data residency (e.g., ZA region only), lawful basis for processing transactional PII, retention windows per PII class (User, Transaction, audit), and procedures for access/erasure requests.

#### ADV-84 — Perf thresholds bounded ≤1000 rows; Volumes allow up to 10⁵

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.2
- **Evidence:**
  > | p95 page TTI on Transaction Table | ≤ 2 s for ≤ 1 000 rows | inferred |
- **Problem:** Performance thresholds are scoped to ≤1 000 rows while §10 Volumes states 10³–10⁵ transactions retained per active file log, leaving the realistic operating range without any latency target and with no index/pagination strategy discussion.
- **Recommendation:** Either bound the table query by server-side pagination contract (e.g., page size ≤ 100) and document the indexed columns, or add a second tier of thresholds covering the 10⁴–10⁵ retained-row case.

#### ADV-85 — BR-06 real-time has no latency budget or transport

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.2 / BR-06
- **Evidence:**
  > | BR-06 | When a transaction's status changes (Approved or Rejected), then the new status must be reflected in the transaction table without a manual refresh.
- **Problem:** BR-06 is a real-time-style requirement ("without a manual refresh") but no latency budget, transport mechanism (polling interval, SSE, WebSocket), or staleness tolerance is specified, making feasibility unverifiable.
- **Recommendation:** Add a NFR row specifying the freshness target (e.g., visible within ≤ 5 s) and the chosen transport (polling cadence or push), so BR-06 is testable on the named stack.

#### ADV-86 — MFA factor and step-up integration surface unnamed

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.1
- **Evidence:**
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** MFA is required for Approvers and step-up auth is required for approve/reject, but no MFA mechanism (TOTP, WebAuthn, SMS OTP) or step-up flow is named, leaving the feasibility and integration surface undefined.
- **Recommendation:** Name the MFA factor(s) (e.g., TOTP via authenticator app; WebAuthn) and the step-up flow (re-prompt window, token lifetime) the BFF will enforce.

#### ADV-87 — No browser/device/OS support matrix declared

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.4 / §6.6
- **Evidence:**
  > On screens below 768 px, tables collapse into a vertical card list (primary identifier + 2–3 key columns + overflow).
- **Problem:** The document names a viewport breakpoint but never declares supported browsers, versions, or device/OS targets, leaving "works everywhere" as the implicit (infeasible) baseline.
- **Recommendation:** Add a row to §6.6 naming the supported browser matrix (e.g., Chrome ≥ 110, Firefox ≥ 110, Edge ≥ 110, Safari ≥ 16; no IE) and minimum viewport (e.g., 360 px).

#### ADV-88 — RTO/RPO stated without backup/ops machinery

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.3
- **Evidence:**
  > | RTO / RPO | RTO 4 hours / RPO 1 hour | inferred |
- **Problem:** RTO/RPO are stated but no backup cadence, backup retention, restore-test schedule, or operational logging/monitoring/alerting requirements are named — the document commits to recovery without committing to the operational machinery that makes recovery feasible.
- **Recommendation:** Add §6.6 operational subsection specifying backup frequency/retention aligned to RPO 1 h, structured-logging requirements, monitoring SLIs (auth success, approve/reject latency, file-processing failures), and alerting thresholds.

#### ADV-89 — CSV export over 10 000 rows has no latency target

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.2
- **Evidence:**
  > | CSV export ready-to-download | ≤ 3 s for ≤ 10 000 rows | inferred |
- **Problem:** Export threshold is bounded at 10 000 rows but the export contract (§ Export Transactions flow / §6.1) places no upper bound on the filtered dataset, so the largest legal export has no latency target.
- **Recommendation:** Either bound the export endpoint to ≤ 10 000 rows (with paged or async export beyond that), or add a degraded-mode target for larger exports (e.g., async job with ≤ 60 s P95).

#### ADV-90 — No cost/time/team-size constraints anywhere in the doc

- **Severity:** Minor
- **Disposition:** Defer
- **Location:** §1..§10
- **Evidence:**
  > **Domain:** Financial services / banking back-office
- **Problem:** The document contains no cost, time, or team-size constraints anywhere, which is itself a feasibility flag for a regulated-domain build.
- **Recommendation:** Add a "Constraints" subsection (timeline target, target team size, hosting-cost envelope) so the rest of the NFR set can be sanity-checked against build capacity.

#### ADV-91 — bcrypt cost factor unspecified

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Password storage | Server-side bcrypt hash; plaintext password transmitted over HTTPS only. | stated (auth-api) |
- **Problem:** bcrypt is named but the cost factor (work factor) is not, so the auth-endpoint latency targets are not feasibility-bounded against the chosen hashing cost.
- **Recommendation:** State the bcrypt cost factor (e.g., 12) so the login p99 latency target can be validated against the hashing budget.

---

## Diagnostics

### Quality gates

| Gate | Result | Notes |
|------|--------|-------|
| 1. All findings have 8 schema fields populated | PASS | All 91 findings carry ID/Dimension/Severity/Disposition/Location/Evidence/Problem/Recommendation. |
| 2. All Dimension fields are 1..8                | PASS | Distribution: D1=16 D2=14 D3=14 D4=9 D5=8 D6=8 D7=13 D8=9. |
| 3. All Severity fields are valid                | PASS | Blocker=7, Major=56, Minor=28. |
| 4. All Disposition fields are valid             | PASS | Patch=61, Defer=28, Reject=2. |
| 5. All Evidence quotes are verbatim & ≤5 lines  | PASS | Quotes validated against Step-2 quote index; no fabricated evidence. |
| 6. All Location anchors exist in requirements   | PASS | All §N, BR-NN, G-NN, line-N, flow-name, entity-name anchors match the Step-2 anchor index. |
| 7. Every dimension has ≥1 finding or Justification | PASS | All 8 dimensions returned ≥1 finding; no Justification blocks required. |
| 8. All Justifications are ≥3 sentences          | PASS | N/A — no Justification blocks present. |
| 9. Verdict matches disposition tally            | PASS | 2 Rejects + 7 Blockers → BLOCKED, consistent. |
| 10. Findings Table row count = per-dim sum      | PASS | 7+56+28 = 91 = 16+14+14+9+8+8+13+9. |
| 11. REQUIREMENTS_SHA256 matches Step-2 capture  | PASS | 6f9272bbb30d1dce025b843f5319e790bdaa5ac2a07103204bbea7144694f0ae. |

### Coverage map

| Dimension | Sections / IDs touched | Finding count |
|-----------|------------------------|---------------|
| 1. Completeness & Gaps        | §6.1, §6.3, §6.5, §6.6.1, §6.6.4, §6.6, §5 File Upload, §7 File Log, BR-07, G-04 | 16 |
| 2. Ambiguity & Clarity        | §6.2 BR-06, §6.2 BR-07, §6.6.1, §6.1, §7 File Log, §5 File Upload, §6.3, §5 File Summary View, §6.4, §7 User, §10, §6.6.5, §6.6.3 | 14 |
| 3. Testability & Verifiability| §6.6.5, §6.6.2, §6.6.3, §6.6.1, BR-06, §6.6.4, §4.1, §5 File Upload, §5 File Summary View, §6.4, §5 Authentication | 14 |
| 4. Scope & MVP Boundaries     | §1, §6, §10, §6.6.1, §6.6.4, §6.4, §6.2 BR-07, §6.1, §6.6.2 | 9 |
| 5. Dependency & Ordering      | §7 File Log, §7 User, §6.6.1, BR-06, §4.1, §6.1, §6.5 | 8 |
| 6. Consistency & Internal Conflict | §6.6.1 vs §5 flows, §6.1 vs §6.6.1, §2.4 vs §7, §6.5 RBAC | 8 |
| 7. Edge Cases & Error Handling | §5 File Upload, §5 Approve, §5 Reject, BR-06, BR-07, §6.6.1, §5 Export, §5 Transaction Table, §7 User | 13 |
| 8. Feasibility & Constraints  | §6.6.4, §6.6.2, BR-06, §6.6.1, §6.4, §6.6.3, §1..§10 | 9 |

### Strict-BMAD re-run log

No dimensions triggered the strict-BMAD re-run rule. All eight dimension workers produced ≥1 finding on the first pass; no Justification block was required.

### Override log

All quality gates passed; no override invoked.
