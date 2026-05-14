# Adversarial Review — `Financial services / banking back-office`

- **Domain:** Financial services / banking back-office
- **Generated:** 2026-05-14T12:00:00Z
- **Requirements SHA-256:** `6f9272bbb30d1dce025b843f5319e790bdaa5ac2a07103204bbea7144694f0ae`
- **Reviewer:** Adversarial Review (BMAD-style, strict mode)

---

## Executive Summary

- **Total findings:** 81
  - Severity — Blocker: **5** · Major: **57** · Minor: **19**
  - Disposition — Patch: **78** · Defer: **3** · Reject: **0**
- **Verdict:** `BLOCKED`

> Verdict legend: `BLOCKED` — at least one Reject or Blocker, requirements doc cannot be consumed downstream. `NEEDS-REVISION` — findings present but none blocking. `ACCEPTED-WITH-FIXES` — zero findings on all eight dimensions, every dimension carries a Justification block (rare under strict-BMAD).

---

## Findings Table

| ID | Dim | Severity | Disposition | Location | Problem |
|----|-----|----------|-------------|----------|---------|
| ADV-01 | 1 | Major | Patch | §6.5 | The User entity has only Read permissions in the RBAC matrix for both roles, leaving no actor authorised to Create, Update, or Delete users, so user provisioning has no defined owner. |
| ADV-02 | 1 | Major | Patch | §6.6.1 | Step-up authentication is asserted as a security requirement but no functional requirement, business rule, or task flow describes when the challenge is issued, what credential is required, or how a failed step-up affects the approve/reject action. |
| ADV-03 | 1 | Major | Patch | §6.6.1 | MFA is declared mandatory for Approvers but no functional requirement, flow, or business rule covers enrollment, challenge, recovery, or what happens if an Approver lacks an enrolled factor. |
| ADV-04 | 1 | Major | Patch | §6.6.1 | Account lockout is specified as a security control but no functional requirement, task flow, or business rule describes the user-facing lockout message, counter reset semantics, or unlock path. |
| ADV-05 | 1 | Major | Patch | §6.6.1 | A 60-second idle warning is specified, but no user-facing requirement defines how the warning is rendered, what action extends the session, or what happens at expiry. |
| ADV-06 | 1 | Major | Patch | BR-07 | BR-07 references "until retry succeeds" but no functional requirement, task flow, or business rule defines the retry action for a Failed file log — who can trigger it, what it does, or what state the file moves to. |
| ADV-07 | 1 | Major | Patch | §7 | FileSetting is referenced as an entity in the data model and is required at upload, but §7 contains no Entity: FileSetting definition (fields, types, validations) and no requirement governs its CRUD lifecycle. |
| ADV-08 | 1 | Major | Patch | §6.1 | Functional requirements in §6.1 are stated as bare capabilities without acceptance criteria or pass/fail predicates, leaving each requirement unverifiable as written. |
| ADV-09 | 1 | Major | Defer | G-04 | G-04's quality signal "at-a-glance status" is closed by the dashboard, but no requirement addresses proactive notification when a file fails, so an Importer who does not open the dashboard can miss a Failed state indefinitely. |
| ADV-10 | 1 | Major | Patch | §6.6.4 | POPIA compliance is asserted but the document contains no requirement covering data-subject access, deletion / right-to-erasure, processing register, or breach-notification flow, leaving the POPIA claim un-evidenced. |
| ADV-11 | 1 | Major | Patch | §7 | The File Log entity exposes an IsActive soft-delete flag, but no functional requirement, business rule, or task flow describes who can deactivate a File Log, when, or how IsActive=false affects visibility in lists, exports, and summary views. |
| ADV-12 | 1 | Minor | Patch | §6.6.3 | Availability targets are stated but no observability, alerting, or health-check requirement exists, so there is no documented mechanism to detect breach of the 99.5%/99.0% targets or to trigger the RTO/RPO recovery process. |
| ADV-13 | 1 | Minor | Patch | §6.4 | The user-facing standard names a "session-about-to-expire" banner but no functional requirement defines its activation threshold, dismiss behaviour, or coupling to the 60-second idle warning in §6.6.1. |
| ADV-14 | 2 | Minor | Patch | §6.4 | The auto-dismiss interval is given as a vague range (4–8 s) rather than a single deterministic value, leaving implementers and testers unable to verify the requirement. |
| ADV-15 | 2 | Major | Defer | §6.6.1 | "Step-up authentication" names no mechanism, no trigger frequency, and no credential factor, so the requirement is unbuildable as stated. |
| ADV-16 | 2 | Minor | Patch | §7 | "Complexity per security policy" references an external policy that is not defined or linked anywhere in the document, leaving complexity rules ambiguous. |
| ADV-17 | 2 | Major | Patch | BR-07 | BR-07 references "retry" as a precondition for re-enabling drill-down, but no retry flow, retry action, or retry trigger is defined anywhere in §5 or §6.1. |
| ADV-18 | 2 | Minor | Patch | §5 File Summary View | The hedge word "may" on the counts-incomplete clause makes it indeterminate whether incomplete counts are expected, permitted, or guaranteed in Processing/Failed states. |
| ADV-19 | 2 | Major | Patch | §6.6.3 | "Business hours" is undefined — no timezone, no start/end times, no working-day calendar — so the SLA cannot be measured. |
| ADV-20 | 2 | Minor | Patch | §10 | "Typically" and "≈" make the concurrency target non-binding, leaving capacity planners without a hard ceiling to design against. |
| ADV-21 | 2 | Minor | Patch | §6.3 | "Transaction detail surface" is a generic noun phrase for a screen that is not defined in §5 task flows or anywhere else in the document. |
| ADV-22 | 2 | Major | Patch | §6.1 | "Process" is a vague verb with no specification of parsing rules, validation, error handling, or batch semantics for turning a file into Transaction rows. |
| ADV-23 | 2 | Minor | Patch | §6.6.5 | "Primary actions" is not defined; without an enumerated set, the requirement is not testable. |
| ADV-24 | 2 | Minor | Patch | §6.4 | "Session-about-to-expire" implies a warning threshold but does not name it, so the banner's trigger window is ambiguous against the 60-second lead-time mentioned in §6.6.1. |
| ADV-25 | 3 | Major | Patch | §6.6.5 | The accessibility requirement names no enumerated checklist, no audit tool, no severity threshold, and no list of "primary actions" or required screen-reader semantics, so a tester cannot write a pass/fail predicate. |
| ADV-26 | 3 | Major | Patch | §6.6.2 | Performance targets give thresholds but omit sample size, measurement window, environment (network/CPU profile), and starting state, so a tester cannot reproduce the percentile calculation deterministically. |
| ADV-27 | 3 | Major | Patch | BR-06 | "Without a manual refresh" sets no time threshold, transport mechanism, or maximum staleness, so a tester cannot decide between a 200 ms websocket push and a 60 s poll, both satisfy the wording. |
| ADV-28 | 3 | Major | Patch | §6.6.1 | Step-up authentication has no enumerated mechanism (password re-entry vs MFA vs WebAuthn), no scope window (per session, per action, per N minutes), and no failure behaviour, so no failing-then-passing test can be written. |
| ADV-29 | 3 | Major | Patch | §6.6.4 | "PII" is not enumerated for this domain (account number? email? user name? amount?), so a tester cannot decide whether a toast containing "AccountNumber 1234567890 not found" violates the rule. |
| ADV-30 | 3 | Major | Patch | §6.4 | "2–3 key columns" is non-deterministic — the designer can pick any two-or-three from the column set and still pass, so two implementations producing different cards both pass the same predicate. |
| ADV-31 | 3 | Major | Defer | §5 Approve / Reject Transaction | Concurrent-update edge case is unnamed: two Approvers acting on the same Imported transaction at the same time has no specified outcome (lost-update, optimistic-lock error, last-write-wins), so neither service nor UI test can be authored. |
| ADV-32 | 3 | Minor | Patch | §5 File Upload | Network-loss / partial-failure edge cases for the upload flow are not named (resumability, retry, partial-bytes scenario), so a tester cannot author a network-interruption test against the spec. |
| ADV-33 | 3 | Minor | Patch | §6.4 | Sort behaviour for null/empty values and tie-breakers is unspecified, so two implementations producing different orderings both satisfy the requirement. |
| ADV-34 | 3 | Minor | Patch | §6.6.3 | "Business hours" is undefined (timezone, days, span), and no measurement window or downtime accounting is given, so the SLA is not verifiable. |
| ADV-35 | 4 | Blocker | Patch | §6 | The document has no MVP designation anywhere — §6 lists all requirements as a flat catalogue with no scope tier, so every functional/business/data/user-facing/NFR item is implicitly MVP, which is the textbook scope-creep signal. |
| ADV-36 | 4 | Blocker | Patch | §10 (document end) | A 501-line requirements document terminates at §10 Volumes with no "Out of scope" / "Non-goals" section, so engineers must infer the exclusions (bulk approve, transaction edit, file deletion, admin features, password reset, MFA enrolment UI) — exactly the failure mode this dimension flags. |
| ADV-37 | 4 | Major | Patch | §6.6.1 | Step-up auth, account lockout, and MFA ("required for Approver") are non-trivial multi-week features layered onto an MVP that otherwise covers only upload/approve/reject/export, yet they are listed at the same priority — a clear MVP cost-vs-scope mismatch with no tagging that they are post-MVP or already-provided. |
| ADV-38 | 4 | Major | Patch | §6.4 | A responsive mobile/card-list rendering is mixed in with desktop table requirements with no scope tag, despite the personas (§3) describing "primary working surface is the transaction table" for daily desktop use — this is a candidate for post-MVP that currently straddles the line. |
| ADV-39 | 4 | Major | Patch | §6.6.3 | Availability targets (99.5%/99.0%, RTO 4h / RPO 1h) imply HA infrastructure, backups, and a runbook that are operational/Phase-2 concerns, but they sit unflagged alongside functional MVP items, conflating buildable scope with steady-state SLA commitments. |
| ADV-40 | 4 | Major | Patch | §6.6.4 | A 7-year retention policy and POPIA conformance are scope-heavy compliance commitments (archival storage, access logs, data-subject request handling) being asserted as if equivalent to a UI requirement — with no MVP/Post-MVP scoping, the engineer can't tell if year-7 retention must ship at v1. |
| ADV-41 | 4 | Major | Patch | BR-07 | BR-07 references a "retry" capability ("until retry succeeds") but no retry flow exists in §5 Task flows and no retry requirement exists in §6.1 — the rule straddles the MVP line by depending on an unscoped feature. |
| ADV-42 | 4 | Major | Patch | §3 vs §6.5 | The RBAC matrix grants "User: R" to both Importer and Approver, implying a user-management/listing surface, but §3 only describes Importer and Approver personas — no Admin is named, no user-management screen is in §5 Task flows, and there is no scope statement about whether user CRUD is MVP or post-MVP. |
| ADV-43 | 5 | Major | Patch | §7 File Log | The File Log entity in §7 depends on a FileSetting entity that is never introduced in §2 Domain model nor defined in §7 Data entities, so an engineer cannot determine when/how FileSetting must exist before File Upload. |
| ADV-44 | 5 | Major | Patch | §4.1 (G-02, G-03) | G-02 and G-03 implicitly depend on G-01 (files uploaded) and on authentication being live, but neither dependency is stated, so an engineer could legitimately start implementing approval/export before the upload pipeline or auth exists. |
| ADV-45 | 5 | Major | Patch | BR-06 | BR-06 mandates real-time status reflection without a manual refresh but no upstream requirement, integration, or transport (WebSocket, SSE, polling cadence) is sequenced or declared anywhere in the doc, leaving the dependency undiscoverable. |
| ADV-46 | 5 | Major | Patch | §6.6.1 vs §5 Approve / Reject | Step-up authentication is declared as required for approve/reject, but the Approve and Reject flows in §5 do not include a step-up step, and no MFA/step-up integration is declared as a prerequisite, so the ordering between MFA provisioning and approve/reject features is undiscoverable. |
| ADV-47 | 5 | Major | Patch | §6.6.1 vs §5 Authentication | Approver MFA is declared mandatory but the Authentication flow in §5 lists only "email + password" with no MFA step, no MFA provisioning requirement, and no enrolment dependency, so engineers cannot tell whether MFA infrastructure must be built before the Approver login can be released. |
| ADV-48 | 5 | Major | Patch | §4.2 / §5 File Upload | Upload requires FileSettingId and FileSettingName, but the doc never describes how a FileSetting is created, listed, or selected, nor sequences "FileSetting management" before file upload — making the upload requirement implementable only after a hidden, undefined dependency. |
| ADV-49 | 5 | Minor | Patch | §6.1 (logout) | Only Approvers are granted a logout requirement, but §6.5 grants Importers Authentication X (login) — leaving an Importer with no defined way out; the ordering of "who gets logout when" is incoherent with the auth flow. |
| ADV-50 | 5 | Minor | Patch | §6.5 (User column) | Both roles have `User: R` but the doc never specifies a user-administration surface or sequences when a User-management capability must be built, and no requirement explains who creates Users — making login depend on an undefined provisioning step. |
| ADV-51 | 5 | Minor | Patch | BR-07 | BR-07 references a "retry" operation as a precondition for drill-down, but no retry requirement, flow, or endpoint is defined anywhere in the doc — the dependency target does not exist. |
| ADV-52 | 6 | Blocker | Patch | §6.6.1 vs §5 / §6.5 | The Security & session table mandates step-up re-auth and required MFA for Approver actions, but no task flow (Approve, Reject), business rule, RBAC cell, or functional requirement mentions any re-auth or MFA step — the matrix shows plain `A†BR-01` / `A†BR-02` with no MFA gate. |
| ADV-53 | 6 | Blocker | Patch | §6.6.2 vs §10 / §6.6.2 CSV row | The transactions GET p99 target is bounded at ≤1 000 rows on the page-TTI line but unqualified on the API line, while §10 states 10³–10⁵ transactions retained per active file log overall — implying GETs and exports beyond the implied 1 000-row scope have no defined performance target. |
| ADV-54 | 6 | Major | Patch | §6.1 vs §6.5 | Only Approvers are named as able to log out in §6.1, but the RBAC matrix grants both Importer and Approver `X` on Authentication and §5 Flow: Authentication is open to both roles; logout availability is therefore contradicted between sections. |
| ADV-55 | 6 | Major | Patch | §2.4 vs §7 File Log | The class diagram shows `CurrentStatus` as the FileLog status attribute, but §7 makes `LastExecutedActivityName` the required, enum-constrained, user-visible status and demotes `CurrentStatus` to an optional "Operational status complement" — the diagram contradicts the canonical entity definition. |
| ADV-56 | 6 | Major | Patch | §2.4 + §6.3 vs §7 Transaction | The Mermaid Transaction omits `TransactionType` (required, enum {C,D} in §7) and `Description`, and §6.3 Data does not mention persisting TransactionType or FileName denormalisation — the canonical entity in §7 introduces fields that contradict the simpler shape declared elsewhere. |
| ADV-57 | 6 | Major | Patch | §2.1 / §5 / §7 / §9 (FileSetting naming) | Upload flow and functional requirements name the inputs `FileSettingId` and `FileSettingName`, but §7's File Log entity stores them as `SettingId` / `SettingName`; furthermore `FileSetting` is recognised in §9 terminology but never appears as a Concept in §2.1 — a naming/scope drift across three sections. |
| ADV-58 | 6 | Major | Patch | §7 File Log RecordCount | RecordCount is declared as `string` with `numeric` validation in §7, but the Mermaid diagram lists it as a plain `+RecordCount` attribute and §6.4 ties pagination and sorting to numeric semantics — typing it as a string in the canonical entity contradicts the way it is rendered/sorted elsewhere. |
| ADV-59 | 6 | Major | Patch | §7 Transaction UserNote | §7 marks UserNote as "yes when Status = Rejected", implying conditional required, but the Required column header is binary and the §2.4 diagram shows `+UserNote` unconditionally on Transaction; BR-02 enforces non-empty only at Reject — three sections describe the same field with subtly conflicting required semantics. |
| ADV-60 | 6 | Major | Patch | §6.5 Importer File Log vs §5 File Upload / BR-04 | The matrix grants Importer `C R` on File Log but only `X` on File Upload; meanwhile File Upload flow states "Available to Importer only" and BR-04 hides the Upload route for Approver — the conflation of "Create File Log" and "Execute File Upload" is internally ambiguous and contradicts the prose that treats upload as Importer-exclusive. |
| ADV-61 | 6 | Minor | Patch | §6.6.4 vs §6.3 | §6.6.4 lists login and logout among audited events using `LastChangedUser` / `LastChangedDate`, but §6.3 scopes those audit fields to "mutating action against File Log, Transaction, and User entities" — login/logout are not mutations on those entities, so the two sections disagree on where the audit record lives. |
| ADV-62 | 7 | Blocker | Patch | §6.1 / §5 File Upload | The file-upload requirement names no maximum file size, no allowed file types/extensions, no virus/malware scan, and no per-row parse-failure handling — exactly the canonical "file upload with no max size, no virus check, no failure mode" gap called out in Dimension 7. |
| ADV-63 | 7 | Major | Patch | §6.6.2 / §10 | Volumes go up to 10⁵ transactions per file log but the only export SLA is for ≤10 000 rows, and there is no defined behaviour when an Approver triggers an export of a filtered set that exceeds this limit (no row cap, no async/email-delivery fallback, no truncation warning). |
| ADV-64 | 7 | Major | Patch | §5 Approve / Reject / BR-06 | There is no concurrency rule for the case where two Approvers act on the same Imported transaction simultaneously — BR-01 only hides actions after status changes locally; nothing defines server-side last-write semantics, optimistic-lock errors, or what the losing Approver's UI shows. |
| ADV-65 | 7 | Major | Patch | §5 Approve / Reject Transaction | Neither approve nor reject defines what happens on network failure / server error after the confirmation modal is submitted — no state-preservation contract (does the modal stay open?), no retry affordance, no idempotency guarantee against double-clicks resubmitting the same approval. |
| ADV-66 | 7 | Major | Patch | §5 File Upload | Upload idempotency is undefined: if an Importer re-submits the same file (same FileHash) — intentionally or after a flaky network — there is no rule saying whether a duplicate File Log is created, deduplicated, or rejected, despite §7 already capturing a SHA-256 FileHash on File Log. |
| ADV-67 | 7 | Major | Patch | §6.4 / §6.6.5 | Validation behaviour is described generically but individual named requirements lack per-field validation rules: max length of the mandatory rejection UserNote (§7 only says "non-empty"), max length of FileName / FileSettingName at upload, and the email format error message — leaving "invalid email, oversize file, malformed input" surfaces unspecified. |
| ADV-68 | 7 | Major | Patch | §6.6.1 | There is no defined recovery behaviour when the session expires mid-action: an Approver halfway through typing a rejection note, or an Importer mid-upload, will silently lose work — no "preserve draft, prompt re-auth, replay action" rule exists. |
| ADV-69 | 7 | Major | Patch | §5 Authentication / §6.6.1 | Lockout policy is defined but there is no password-reset / account-recovery flow anywhere in §5 task flows, §6.1 functional requirements, or §6.5 RBAC — meaning a locked Approver has no documented recovery path, which is a canonical Dimension 7 recovery-path gap. |
| ADV-70 | 7 | Major | Patch | BR-07 / §5 File Summary View | BR-07 names a "retry" but no requirement, flow, or RBAC cell defines a retry action: there is no actor, trigger, endpoint, or success/failure behaviour for retrying a Failed File Log, so the rule cannot be implemented as written. |
| ADV-71 | 7 | Major | Patch | §5 Approve Transaction / §6.1 | Story text claims Approve is "reversible only by separate workflow" but no such workflow exists in §5 task flows, §6.1 functional requirements, or §6.5 RBAC — so the documented undo/recovery path for the system's most consequential action is absent. |
| ADV-72 | 7 | Major | Patch | §5 Authentication / §6.5 | There is no defined authorization-failure UX when a role lands on a forbidden route directly (e.g., an Approver navigating to /upload or an Importer to /export): BR-03/BR-04 only say controls are hidden, not what a deep-link request returns or how the UI handles a 403. |
| ADV-73 | 7 | Major | Patch | §5 Export Transactions / §6.4 | Export has no network-failure or partial-failure surface: if CSV generation fails server-side (timeout, 5xx), or the browser cancels the download, there is no documented retry, no resumption, and no audit of failed export attempts despite §6.6.4 mandating audit of every approve/reject/upload/login/logout event. |
| ADV-74 | 8 | Major | Patch | §6.6.4 | POPIA is named only as "implied" with no concrete treatment of data residency, PII inventory, consent flows, retention windows per data class, or subject-access/erasure obligations — yet the system handles AccountNumber, Email, names, and financial transactions which are POPIA-bearing. |
| ADV-75 | 8 | Major | Patch | §6.6.2 | Performance thresholds are stated without reference to the implementation stack, expected indexing, or measurement methodology — and the CSV-export budget of 3 s for 10 000 rows is suspect for a synchronous browser download without a streaming/async strategy named. |
| ADV-76 | 8 | Major | Patch | §6.6.1 | Step-up auth, MFA-for-Approver, and account-lockout are asserted with no mechanism named (TOTP? WebAuthn? SMS?) and no integration point — the auth-api source only documents password + session cookie, so these requirements are not buildable as written. |
| ADV-77 | 8 | Major | Patch | §6.6.3 | Availability targets (99.5 %, RTO 4 h / RPO 1 h) are stated but the document names no logging, monitoring, alerting, backup, or DR mechanism — so the operational claim "we will run this in production" is unsupported and the RPO is unverifiable. |
| ADV-78 | 8 | Major | Patch | §6.6.4 | A 7-year retention is asserted for audit but no retention window is given for the underlying Transaction, File Log, or User records — and POPIA Section 14 requires retention to be no longer than necessary per data class, so a single 7-year blanket is non-compliant by omission. |
| ADV-79 | 8 | Minor | Patch | §6.4 (breakpoint) | The only device-class statement is a 768 px breakpoint; there is no named browser/version matrix or OS target, making the surface "works everywhere" rather than testable. |
| ADV-80 | 8 | Minor | Patch | §1 header | The document is marked final but states no delivery timeline, team size, or cost envelope — feasibility cannot be assessed against constraints that are not present. |
| ADV-81 | 8 | Minor | Patch | BR-06 | BR-06 mandates real-time reflection of status changes with no latency budget and no mechanism (polling cadence? websocket? SSE?) — a "real-time" requirement without a latency budget is a classic feasibility flag. |

---

## Dimension 1 — Completeness & Gaps

### Findings

#### ADV-01 — User CRUD has no defined actor

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.5
- **Evidence:**
  > | Importer | R | C R | R | X | X | X | X | X | — | — | — | X |
  > | Approver | R | R | R U†BR-01 | X | — | X | X | X | A†BR-01 | A†BR-02 | X | X |
- **Problem:** The User entity has only Read permissions in the RBAC matrix for both roles, leaving no actor authorised to Create, Update, or Delete users, so user provisioning has no defined owner.
- **Recommendation:** Add an Admin (or System) role to §3 and §6.5 with explicit C/R/U/D permissions on User, or state explicitly that user provisioning is out of scope and handled by an external IdP.

#### ADV-02 — Step-up auth declared with no flow

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** Step-up authentication is asserted as a security requirement but no functional requirement, business rule, or task flow describes when the challenge is issued, what credential is required, or how a failed step-up affects the approve/reject action.
- **Recommendation:** Add a functional requirement and a task-flow step (under Approve Transaction and Reject Transaction in §5) describing the step-up trigger, the credential type accepted, and the failure path.

#### ADV-03 — MFA declared mandatory with no enrolment / challenge / recovery requirements

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** MFA is declared mandatory for Approvers but no functional requirement, flow, or business rule covers enrollment, challenge, recovery, or what happens if an Approver lacks an enrolled factor.
- **Recommendation:** Add an MFA functional requirement plus an MFA enrolment/challenge flow under §5 covering enrolled-factor types, challenge timing, and the no-factor-enrolled failure path.

#### ADV-04 — Account lockout policy has no user-facing requirement

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Account lockout policy | 5 failed attempts → 15-minute cooldown; cooldown resets on successful authentication | inferred |
- **Problem:** Account lockout is specified as a security control but no functional requirement, task flow, or business rule describes the user-facing lockout message, counter reset semantics, or unlock path.
- **Recommendation:** Add a functional requirement and Authentication-flow exception path covering the lockout message shown to the user, where the counter is tracked, and the unlock mechanism (time-based vs. admin-driven).

#### ADV-05 — Idle warning lead-time has no UI requirement

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Idle warning lead-time | 60 seconds before idle logout | inferred (financial domain default) |
- **Problem:** A 60-second idle warning is specified, but no user-facing requirement defines how the warning is rendered, what action extends the session, or what happens at expiry.
- **Recommendation:** Add a §6.4 user-facing requirement describing the idle-warning banner/modal, the extend-session interaction, and the silent-logout transition at expiry.

#### ADV-06 — BR-07 references undefined "retry"

- **Severity:** Major
- **Disposition:** Patch
- **Location:** BR-07
- **Evidence:**
  > | BR-07 | When a file log is in Failed state, then the file summary view must surface the failure prominently and inhibit drill-down into transactions until retry succeeds. | UI | → §2.3 File Log invariant | major |
- **Problem:** BR-07 references "until retry succeeds" but no functional requirement, task flow, or business rule defines the retry action for a Failed file log — who can trigger it, what it does, or what state the file moves to.
- **Recommendation:** Add a functional requirement and a Retry Failed Upload task flow in §5 defining who can retry, the trigger control, and the resulting state transitions on retry success/failure.

#### ADV-07 — FileSetting entity referenced but never defined

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §7
- **Evidence:**
  > | SettingId | int | yes | references FileSetting.Id | Upload-time setting reference. |
  > | SettingName | string | yes | — | Snapshot of FileSetting.Name at upload. |
- **Problem:** FileSetting is referenced as an entity (and required at upload) but §7 contains no Entity: FileSetting definition (fields, types, validations) and no requirement governs its CRUD lifecycle.
- **Recommendation:** Add an Entity: FileSetting subsection to §7 with fields, validations, and relationships, and add a functional requirement or flow describing how FileSettings are created, listed, and selected at upload time.

#### ADV-08 — Functional requirements have no acceptance criteria

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.1
- **Evidence:**
  > - Authenticate users with username and password against a server-side bcrypt-hashed credential store; on success, issue an HttpOnly, Secure, SameSite=Strict session cookie.- Allow Importers to upload a transaction file with FileSettingId, FileSettingName, and FileName, and create a corresponding File Log on the server.
- **Problem:** Functional requirements in §6.1 are stated as bare capabilities without acceptance criteria or pass/fail predicates, leaving each requirement unverifiable as written.
- **Recommendation:** Append an explicit acceptance-criterion clause (Given/When/Then or a measurable predicate) to each §6.1 bullet so each requirement is independently testable.

#### ADV-09 — G-04 closes status visibility but not proactive failure notification

- **Severity:** Major
- **Disposition:** Defer
- **Location:** G-04
- **Evidence:**
  > | G-04 | Monitor the processing status of uploaded files. | At-a-glance status, drill-down to detail | top-level | dashboard list | tabular file log with status column |
- **Problem:** G-04's quality signal "at-a-glance status" is closed by the dashboard, but no requirement addresses proactive notification when a file fails, so an Importer who does not open the dashboard can miss a Failed state indefinitely.
- **Recommendation:** Add either an explicit "no proactive notification" scope statement closing G-04, or a functional requirement defining the notification channel (in-app banner, email) on File Log Failed.

#### ADV-10 — POPIA asserted without subject-rights or breach-notification requirements

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.4
- **Evidence:**
  > - POPIA (South Africa) — implied by the use of ZAR currency in the sample dataset and South African account-number formats.- Audit trail: every approve, reject, upload, login, and logout event is recorded with `LastChangedUser` and `LastChangedDate`; retain 7 years.
- **Problem:** POPIA compliance is asserted but the document contains no requirement covering data-subject access, deletion / right-to-erasure, processing register, or breach-notification flow, leaving the POPIA claim un-evidenced.
- **Recommendation:** Add explicit POPIA-bearing requirements covering data-subject request handling, retention/deletion controls on Transaction/User data, and breach-notification responsibility, or downgrade the claim to a scoped subset with stated exclusions.

#### ADV-11 — IsActive soft-delete has no governing requirement

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §7
- **Evidence:**
  > | IsActive | boolean | yes | — | Soft-delete / archival flag. |
- **Problem:** The File Log entity exposes an IsActive soft-delete flag, but no functional requirement, business rule, or task flow describes who can deactivate a File Log, when, or how IsActive=false affects visibility in lists, exports, and summary views.
- **Recommendation:** Add a functional requirement defining the File Log deactivate/archive action with the actor, trigger, and downstream filtering behaviour for IsActive=false records.

#### ADV-12 — Availability targets without observability mechanism

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.3
- **Evidence:**
  > | Target uptime | 99.5 % during business hours; 99.0 % overall | inferred |
  > | Maintenance window | Weekly Sunday 02:00–04:00 local time | inferred |
  > | RTO / RPO | RTO 4 hours / RPO 1 hour | inferred |
- **Problem:** Availability targets are stated but no observability, alerting, or health-check requirement exists, so there is no documented mechanism to detect breach of the 99.5%/99.0% targets or to trigger the RTO/RPO recovery process.
- **Recommendation:** Add §6.6 subsection (or non-functional bullet) for Observability covering health-check endpoints, uptime monitoring, alert routing, and the trigger for RTO/RPO recovery procedures.

#### ADV-13 — Session-about-to-expire banner has no governing requirement

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.4
- **Evidence:**
  > Persistent state (offline, session-about-to-expire, file-failed banners) uses banners.
- **Problem:** The user-facing standard names a "session-about-to-expire" banner but no functional requirement defines its activation threshold, dismiss behaviour, or coupling to the 60-second idle warning in §6.6.1.
- **Recommendation:** Add a functional requirement tying the session-about-to-expire banner to the idle-warning lead-time, specifying dismiss/extend interactions and what the banner shows at expiry.

---

## Dimension 2 — Ambiguity & Clarity

### Findings

#### ADV-14 — Auto-dismiss range is non-deterministic

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.4
- **Evidence:**
  > Transient confirmations (approval / rejection / export complete) use toasts auto-dismissing in 4–8 s, top-right.
- **Problem:** The auto-dismiss interval is given as a vague range (4–8 s) rather than a single deterministic value, leaving implementers and testers unable to verify the requirement.
- **Recommendation:** Replace the range with a single concrete value (e.g., "auto-dismissing after 6 s") or specify the rule that picks within the range.

#### ADV-15 — "Step-up authentication" names no mechanism

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §6.6.1
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** "Step-up authentication" names no mechanism, no trigger frequency, and no credential factor, so the requirement is unbuildable as stated.
- **Recommendation:** Specify the step-up mechanism (e.g., password re-entry vs. MFA), when it is challenged (every action, per session, after N minutes), and which factor is required.

#### ADV-16 — Password complexity references undefined "security policy"

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §7
- **Evidence:**
  > | Password | string (write-only) | yes (create) | min length 8; complexity per security policy | Stored as bcrypt hash; never returned. |
- **Problem:** "Complexity per security policy" references an external policy that is not defined or linked anywhere in the document, leaving complexity rules ambiguous.
- **Recommendation:** Inline the complexity rules (character classes, min entropy, banned-list policy) or link to the explicit policy artefact.

#### ADV-17 — "retry" in BR-07 is undefined

- **Severity:** Major
- **Disposition:** Patch
- **Location:** BR-07
- **Evidence:**
  > | BR-07 | When a file log is in Failed state, then the file summary view must surface the failure prominently and inhibit drill-down into transactions until retry succeeds. | UI | → §2.3 File Log invariant | major |
- **Problem:** BR-07 references "retry" as a precondition for re-enabling drill-down, but no retry flow, retry action, or retry trigger is defined anywhere in §5 or §6.1.
- **Recommendation:** Either define a Retry flow in §5 and a corresponding FR in §6.1, or replace "until retry succeeds" with a concrete observable state transition (e.g., "until the file log re-enters Completed state").

#### ADV-18 — "may be incomplete" is a hedge on a behavioural rule

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §5 File Summary View
- **Evidence:**
  > | Exception paths | If the file is still Processing or Failed, counts may be incomplete; the view shows the file's current state prominently. |
- **Problem:** The hedge word "may" on the counts-incomplete clause makes it indeterminate whether incomplete counts are expected, permitted, or guaranteed in Processing/Failed states.
- **Recommendation:** Replace "may be incomplete" with the deterministic rule (e.g., "counts reflect only transactions parsed so far; the Processing/Failed state is shown alongside").

#### ADV-19 — "Business hours" undefined

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.3
- **Evidence:**
  > | Target uptime | 99.5 % during business hours; 99.0 % overall | inferred |
- **Problem:** "Business hours" is undefined — no timezone, no start/end times, no working-day calendar — so the SLA cannot be measured.
- **Recommendation:** Define business hours explicitly (e.g., "Mon–Fri 07:00–19:00 SAST excluding South African public holidays").

#### ADV-20 — "Typically" and "≈" leave concurrency non-binding

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §10
- **Evidence:**
  > | Concurrency | Typically one concurrent user per role only (≈ 1 Importer + 1 Approver active at a time) | consultant-corrected |
- **Problem:** "Typically" and "≈" make the concurrency target non-binding, leaving capacity planners without a hard ceiling to design against.
- **Recommendation:** Replace with a concrete maximum (e.g., "Maximum 2 concurrent users overall: 1 Importer and 1 Approver").

#### ADV-21 — "transaction detail surface" undefined

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.3
- **Evidence:**
  > Capture the rejecting user's note against the Transaction; expose it on the transaction detail surface.
- **Problem:** "Transaction detail surface" is a generic noun phrase for a screen that is not defined in §5 task flows or anywhere else in the document.
- **Recommendation:** Name the specific surface (e.g., transaction row expand, modal, or a defined Transaction Detail flow in §5) where the note is exposed.

#### ADV-22 — "Process" is a vague verb for the parsing pipeline

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.1
- **Evidence:**
  > Process uploaded files into Transactions; expose the file's lifecycle via `LastExecutedActivityName` / `CurrentStatus` on the File Log.
- **Problem:** "Process" is a vague verb with no specification of parsing rules, validation, error handling, or batch semantics for turning a file into Transaction rows.
- **Recommendation:** Replace "Process" with the explicit pipeline (parse → validate → persist), and reference the FileSetting-driven parsing contract that determines column mapping and validation.

#### ADV-23 — "primary actions" not enumerated

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.5
- **Evidence:**
  > - WCAG 2.2 AA conformance, full keyboard reach for all primary actions, screen-reader semantics on status badges.
- **Problem:** "Primary actions" is not defined; without an enumerated set, the requirement is not testable.
- **Recommendation:** Enumerate the primary actions (Upload, Approve, Reject, Export, Login, Logout, Filter Apply, Filter Clear-all) or scope the requirement to "every interactive control in §5 flows".

#### ADV-24 — "session-about-to-expire" threshold unnamed

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.4
- **Evidence:**
  > Persistent state (offline, session-about-to-expire, file-failed banners) uses banners.
- **Problem:** "Session-about-to-expire" implies a warning threshold but does not name it, so the banner's trigger window is ambiguous against the 60-second lead-time mentioned in §6.6.1.
- **Recommendation:** Bind the banner to the explicit §6.6.1 idle warning lead-time (e.g., "shown 60 s before idle logout per §6.6.1").

---

## Dimension 3 — Testability & Verifiability

### Findings

#### ADV-25 — Accessibility requirement has no enumerated checklist

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.5 Accessibility
- **Evidence:**
  > - WCAG 2.2 AA conformance, full keyboard reach for all primary actions, screen-reader semantics on status badges.
- **Problem:** The accessibility requirement names no enumerated checklist, no audit tool, no severity threshold, and no list of "primary actions" or required screen-reader semantics, so a tester cannot write a pass/fail predicate.
- **Recommendation:** Replace with a concrete acceptance set, e.g., "axe-core scan reports zero serious/critical violations on the five primary screens; each status badge exposes role=status with text label X; tab order on Transaction Table is documented and asserted by a Playwright keyboard test."

#### ADV-26 — Performance thresholds without sample / window / environment

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.2 Performance
- **Evidence:**
  > | p95 page TTI on Transaction Table | ≤ 2 s for ≤ 1 000 rows | inferred |
  > | API p99 latency for `/v1/transactions` GET | ≤ 500 ms | inferred |
  > | API p99 latency for approve / reject | ≤ 800 ms | inferred |
  > | CSV export ready-to-download | ≤ 3 s for ≤ 10 000 rows | inferred |
- **Problem:** Performance targets give thresholds but omit sample size, measurement window, environment (network/CPU profile), and starting state, so a tester cannot reproduce the percentile calculation deterministically.
- **Recommendation:** Add for each row: sample N (e.g., "over 1000 requests in a 10-minute window"), environment (warm cache, k6 from staging region, simulated 4G), and starting state, so the predicate is unambiguous.

#### ADV-27 — BR-06 "without a manual refresh" has no time / mechanism predicate

- **Severity:** Major
- **Disposition:** Patch
- **Location:** BR-06
- **Evidence:**
  > | BR-06 | When a transaction's status changes (Approved or Rejected), then the new status must be reflected in the transaction table without a manual refresh. | UI | → §2.3 Transaction invariant | major |
- **Problem:** "Without a manual refresh" sets no time threshold, transport mechanism, or maximum staleness, so a tester cannot decide between a 200 ms websocket push and a 60 s poll, both satisfy the wording.
- **Recommendation:** Specify a measurable predicate, e.g., "the new status is visible in the same browser tab within 2 s of the API 200 response, verified by polling the DOM at 250 ms intervals."

#### ADV-28 — Step-up auth has no enumerated mechanism / cadence / failure

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1 Security & session
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** Step-up authentication has no enumerated mechanism (password re-entry vs MFA vs WebAuthn), no scope window (per session, per action, per N minutes), and no failure behaviour, so no failing-then-passing test can be written.
- **Recommendation:** Either remove the row or specify mechanism + cadence, e.g., "Approver must re-enter password if last successful auth >5 minutes ago at the moment Approve/Reject is submitted; failed re-auth blocks the action and increments lockout counter."

#### ADV-29 — "No PII in toasts / console" is not enumerated

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.4 Compliance & audit
- **Evidence:**
  > - No PII is rendered in error toasts or browser console.
- **Problem:** "PII" is not enumerated for this domain (account number? email? user name? amount?), so a tester cannot decide whether a toast containing "AccountNumber 1234567890 not found" violates the rule.
- **Recommendation:** List the forbidden fields explicitly, e.g., "AccountNumber, Email, FirstName/LastName, and full UserNote MUST NOT appear in toast copy or console.log output; assertions live in src/test/pii-redaction.spec.ts."

#### ADV-30 — "2–3 key columns" is non-deterministic

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.4 User-facing
- **Evidence:**
  > On screens below 768 px, tables collapse into a vertical card list (primary identifier + 2–3 key columns + overflow).
- **Problem:** "2–3 key columns" is non-deterministic — the designer can pick any two-or-three from the column set and still pass, so two implementations producing different cards both pass the same predicate.
- **Recommendation:** Enumerate exactly, e.g., "Transaction card shows Reference (primary), TransactionDate, Amount+Currency; remaining columns hidden behind an overflow disclosure."

#### ADV-31 — Concurrent approve/reject edge case unnamed

- **Severity:** Major
- **Disposition:** Defer
- **Location:** §5 Approve / Reject Transaction
- **Evidence:**
  > | Steps | 1. Select transaction. 2. Click Approve. 3. Confirm action in modal. 4. Status updates to Approved. |
- **Problem:** Concurrent-update edge case is unnamed: two Approvers acting on the same Imported transaction at the same time has no specified outcome (lost-update, optimistic-lock error, last-write-wins), so neither service nor UI test can be authored.
- **Recommendation:** Add a row "Exception paths" item, e.g., "If a concurrent action has already transitioned the transaction out of Imported, the second submit returns 409 Conflict and the UI shows a toast 'This transaction was already actioned by <user>'."

#### ADV-32 — Upload flow's network-loss edge case unspecified

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §5 File Upload
- **Evidence:**
  > | Exception paths | Success / failure feedback is rendered after upload. On failure, the file is not parsed and no File Log row is created in a Completed state. |
- **Problem:** Network-loss / partial-failure edge cases for the upload flow are not named (resumability, retry, partial-bytes scenario), so a tester cannot author a network-interruption test against the spec.
- **Recommendation:** Add explicit edge cases, e.g., "On client-side connection loss before upload completes, no File Log is created; on server-side parse failure mid-stream, the File Log moves to Failed with a non-empty error message exposed on the summary view."

#### ADV-33 — Sort behaviour for null / tie undefined

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.4 User-facing
- **Evidence:**
  > - All table columns are sortable; sorting is single-column, ascending on first click, descending on second; persists for the session.
- **Problem:** Sort behaviour for null/empty values and tie-breakers is unspecified, so two implementations producing different orderings both satisfy the requirement.
- **Recommendation:** Specify, e.g., "NULL/empty values sort last regardless of direction; ties break by Id ascending."

#### ADV-34 — Availability SLA not verifiable

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.3 Availability
- **Evidence:**
  > | Target uptime | 99.5 % during business hours; 99.0 % overall | inferred |
- **Problem:** "Business hours" is undefined (timezone, days, span), and no measurement window or downtime accounting is given, so the SLA is not verifiable.
- **Recommendation:** Define, e.g., "Business hours = Mon–Fri 07:00–19:00 SAST; uptime measured monthly via external probe at 1-minute intervals; planned maintenance excluded."

---

## Dimension 4 — Scope & MVP Boundaries

### Findings

#### ADV-35 — No MVP designation anywhere

- **Severity:** Blocker
- **Disposition:** Patch
- **Location:** §6
- **Evidence:**
  > ## 6. Requirements
  >
  > ### 6.1 Functional
- **Problem:** The document has no MVP designation anywhere — §6 lists all requirements as a flat catalogue with no scope tier, so every functional/business/data/user-facing/NFR item is implicitly MVP, which is the textbook scope-creep signal.
- **Recommendation:** Add an explicit MVP tag (e.g., `MVP` / `Post-MVP` column) to each requirement in §6.1–§6.6 or split §6 into 'MVP' and 'Post-MVP' subsections so the cut line is unambiguous.

#### ADV-36 — No "Out of scope" section

- **Severity:** Blocker
- **Disposition:** Patch
- **Location:** §10 (document end)
- **Evidence:**
  > ## 10. Volumes
  >
  > | Metric | Value | Source |
- **Problem:** A 501-line requirements document terminates at §10 Volumes with no "Out of scope" / "Non-goals" section, so engineers must infer the exclusions (e.g., bulk approve, transaction edit, file deletion, admin features, password reset, MFA enrolment UI) — exactly the failure mode this dimension flags.
- **Recommendation:** Add a §11 "Out of scope" section enumerating deliberately excluded capabilities (bulk approve/reject, transaction editing, file deletion/retry, admin/user-management UI, password reset, MFA enrolment, multi-currency conversion, downstream consumer integration) with one-line rationale each.

#### ADV-37 — Step-up / lockout / MFA priority not separated from MVP

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
  > | Account lockout policy | 5 failed attempts → 15-minute cooldown; cooldown resets on successful authentication | inferred |
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** Step-up auth, account lockout, and MFA ("required for Approver") are non-trivial multi-week features layered onto an MVP that otherwise covers only upload/approve/reject/export, yet they are listed at the same priority — a clear MVP cost-vs-scope mismatch with no tagging that they are post-MVP or already-provided.
- **Recommendation:** Either tag these three rows as Post-MVP / dependency-on-IdP, or add a "Source/Owner" note confirming they are delivered by an external auth provider so they are not in the build estimate for this system.

#### ADV-38 — Mobile responsive collapse straddles MVP line

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.4
- **Evidence:**
  > On screens below 768 px, tables collapse into a vertical card list (primary identifier + 2–3 key columns + overflow).
- **Problem:** A responsive mobile/card-list rendering is mixed in with desktop table requirements with no scope tag, despite the personas (§3) describing "primary working surface is the transaction table" for daily desktop use — this is a candidate for post-MVP that currently straddles the line.
- **Recommendation:** Either explicitly mark the <768 px responsive collapse as Post-MVP, or justify mobile support in §3 personas (frequency/device) so its MVP inclusion is defensible.

#### ADV-39 — Availability / DR targets unflagged

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.3
- **Evidence:**
  > | Target uptime | 99.5 % during business hours; 99.0 % overall | inferred |
  > | Maintenance window | Weekly Sunday 02:00–04:00 local time | inferred |
  > | RTO / RPO | RTO 4 hours / RPO 1 hour | inferred |
- **Problem:** Availability targets (99.5%/99.0%, RTO 4h / RPO 1h) imply HA infrastructure, backups, and a runbook that are operational/Phase-2 concerns, but they sit unflagged alongside functional MVP items, conflating buildable scope with steady-state SLA commitments.
- **Recommendation:** Move §6.6.3 into a separate "Operational targets (post-launch)" subsection, or tag each row with a phase indicator (e.g., "Target for GA, not MVP demo") so the engineer does not size DR work into the MVP.

#### ADV-40 — POPIA + 7-year retention compete with MVP requirements

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.4
- **Evidence:**
  > - POPIA (South Africa) — implied by the use of ZAR currency in the sample dataset and South African account-number formats.- Audit trail: every approve, reject, upload, login, and logout event is recorded with `LastChangedUser` and `LastChangedDate`; retain 7 years.
- **Problem:** A 7-year retention policy and POPIA conformance are scope-heavy compliance commitments (archival storage, access logs, data-subject request handling) being asserted as if equivalent to a UI requirement — with no MVP/Post-MVP scoping, the engineer can't tell if year-7 retention must ship at v1.
- **Recommendation:** Split into "MVP audit logging (capture events)" vs "Post-MVP retention & POPIA tooling (7-year archive, DSR endpoints)" so the long-tail compliance work is explicitly deferred.

#### ADV-41 — BR-07 depends on unscoped retry feature

- **Severity:** Major
- **Disposition:** Patch
- **Location:** BR-07
- **Evidence:**
  > | BR-07 | When a file log is in Failed state, then the file summary view must surface the failure prominently and inhibit drill-down into transactions until retry succeeds. | UI | → §2.3 File Log invariant | major |
- **Problem:** BR-07 references a 'retry' capability ('until retry succeeds') but no retry flow exists in §5 Task flows and no retry requirement exists in §6.1 — the rule straddles the MVP line by depending on an unscoped feature.
- **Recommendation:** Either add a 'Retry Failed File' task flow and corresponding §6.1 requirement (and tag its MVP status), or rewrite BR-07 to remove the retry dependency (e.g., 'inhibit drill-down on Failed; retry is Post-MVP').

#### ADV-42 — User resource in RBAC without UI / scope statement

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §3 vs §6.5
- **Evidence:**
  > | Importer | R | C R | R | X | X | X | X | X | — | — | — | X |
  > | Approver | R | R | R U†BR-01 | X | — | X | X | X | A†BR-01 | A†BR-02 | X | X |
- **Problem:** The RBAC matrix grants "User: R" to both Importer and Approver, implying a user-management/listing surface, but §3 only describes Importer and Approver personas — no Admin is named, no user-management screen is in §5 Task flows, and there is no scope statement about whether user CRUD is MVP or post-MVP.
- **Recommendation:** Either remove "User: R" from the matrix (it has no UI), add a §5 "User Management" flow with explicit MVP/Post-MVP tagging, or add a one-line note: "User administration is out of scope; users are provisioned externally."

---

## Dimension 5 — Dependency & Ordering

### Findings

#### ADV-43 — FileSetting dependency undefined for File Log

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §7 File Log / §2.1 Concepts
- **Evidence:**
  > | SettingId | int | yes | references FileSetting.Id | Upload-time setting reference. |
  > | SettingName | string | yes | — | Snapshot of FileSetting.Name at upload. |
- **Problem:** The File Log entity in §7 depends on a FileSetting entity that is never introduced in the §2 Domain model nor defined in §7 Data entities, so an engineer cannot determine when/how FileSetting must exist before File Upload.
- **Recommendation:** Add a FileSetting concept to §2.1 (and a stub Entity: FileSetting in §7) declaring its lifecycle and that it must be provisioned before any File Upload requirement is implementable.

#### ADV-44 — G-02 / G-03 dependencies on G-01 unstated

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §4.1 (G-02, G-03)
- **Evidence:**
  > | G-02 | Review and approve or reject queued transactions. | Accuracy, throughput, decision confidence | top-level | data-table working surface | row-action approve/reject + confirm modal |
  > | G-03 | Export approved or filtered transactions for downstream consumption. | Faithfulness to current filter, predictable format | sub-level | action in table toolbar | one-click CSV export |
- **Problem:** G-02 and G-03 implicitly depend on G-01 (files uploaded) and on authentication being live, but neither dependency is stated, so an engineer could legitimately start implementing approval/export before the upload pipeline or auth exists.
- **Recommendation:** Add an explicit "Depends on" column or note in §4.1 declaring G-02 depends on G-01 + Authentication flow, and G-03 depends on G-02.

#### ADV-45 — BR-06 real-time push dependency undisclosed

- **Severity:** Major
- **Disposition:** Patch
- **Location:** BR-06
- **Evidence:**
  > | BR-06 | When a transaction's status changes (Approved or Rejected), then the new status must be reflected in the transaction table without a manual refresh. | UI | → §2.3 Transaction invariant | major |
- **Problem:** BR-06 mandates real-time status reflection without a manual refresh but no upstream requirement, integration, or transport (WebSocket, SSE, polling cadence) is sequenced or declared anywhere in the doc, leaving the dependency undiscoverable.
- **Recommendation:** Add a functional requirement in §6.1 specifying the push/poll mechanism BR-06 depends on (e.g., "SSE channel on /v1/transactions/stream") and sequence it before the approve/reject UI work.

#### ADV-46 — Step-up auth dependency not sequenced against approve/reject

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1 vs §5 Approve / Reject
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** Step-up authentication is declared as required for approve/reject, but the Approve Transaction and Reject Transaction flows in §5 do not include a step-up step, and no MFA/step-up integration is declared as a prerequisite, so the ordering between MFA provisioning and approve/reject features is undiscoverable.
- **Recommendation:** Either add an explicit step-up step to the §5 Approve/Reject flows and a functional requirement sequencing MFA infrastructure before approve/reject, or remove/relax the §6.6.1 re-auth claim to match the flows.

#### ADV-47 — MFA-for-Approver dependency missing from Authentication flow

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1 vs §5 Authentication
- **Evidence:**
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** Approver MFA is declared mandatory but the Authentication flow in §5 lists only "email + password" with no MFA step, no MFA provisioning requirement, and no enrolment dependency, so engineers cannot tell whether MFA infrastructure must be built before the Approver login can be released.
- **Recommendation:** Add an MFA-enrolment requirement and an MFA-challenge step to the Authentication flow, and explicitly state in §6.1 that Approver login depends on MFA infrastructure being live.

#### ADV-48 — FileSetting picker / provisioning undefined for upload

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §4.2 story / §5 File Upload
- **Evidence:**
  > | Objective | Submit a single transaction file via the upload UI, providing FileSettingId, FileSettingName, and FileName, and receive immediate feedback on whether the file was accepted. |
- **Problem:** Upload requires FileSettingId and FileSettingName, but the doc never describes how a FileSetting is created, listed, or selected, nor sequences "FileSetting management" before file upload — making the upload requirement implementable only after a hidden, undefined dependency.
- **Recommendation:** Add either a functional requirement "Provide a FileSetting picker/management surface" in §6.1 with explicit sequencing before File Upload, or document that FileSettings are provisioned out-of-band and reference where.

#### ADV-49 — Logout for Importer not provided

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.1 (logout)
- **Evidence:**
  > Provide a file summary view showing total records and a count by status (Imported / Approved / Rejected).- Allow Approvers to log out via an endpoint that invalidates the session cookie.
- **Problem:** Only Approvers are granted a logout requirement, but §6.5 grants Importers Authentication X (login) — leaving an Importer with no defined way out; the ordering of "who gets logout when" is incoherent with the auth flow.
- **Recommendation:** Change the bullet to "Allow all authenticated users (Importer and Approver) to log out" and confirm in §6.5 that Authentication X for Importer includes the logout endpoint.

#### ADV-50 — User provisioning ordering undefined

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.5 (User column)
- **Evidence:**
  > | Importer | R | C R | R | X | X | X | X | X | — | — | — | X |
  > | Approver | R | R | R U†BR-01 | X | — | X | X | X | A†BR-01 | A†BR-02 | X | X |
- **Problem:** Both roles have `User: R` but the doc never specifies a user-administration surface or sequences when a User-management capability must be built, and no requirement explains who creates Users — making login (G-02 prerequisite) depend on an undefined provisioning step.
- **Recommendation:** Add a §6.1 functional requirement (or explicit dependency note) describing user provisioning/management (admin-side or seeding) and sequence it before any role-gated requirement.

#### ADV-51 — BR-07 "retry" precondition does not exist

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** BR-07
- **Evidence:**
  > | BR-07 | When a file log is in Failed state, then the file summary view must surface the failure prominently and inhibit drill-down into transactions until retry succeeds. | UI | → §2.3 File Log invariant | major |
- **Problem:** BR-07 references a "retry" operation as a precondition for drill-down, but no retry requirement, flow, or endpoint is defined anywhere in the doc — the dependency target does not exist.
- **Recommendation:** Either add a Retry-File flow and corresponding functional requirement (sequenced after File Upload), or reword BR-07 to remove the retry precondition and describe the actual recovery path.

---

## Dimension 6 — Consistency & Internal Conflict

### Findings

#### ADV-52 — Step-up / MFA mandated but absent from flows, BRs, RBAC, FRs

- **Severity:** Blocker
- **Disposition:** Patch
- **Location:** §6.6.1 vs §5 / §6.2 / §6.5
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
  > | Account lockout policy | 5 failed attempts → 15-minute cooldown; cooldown resets on successful authentication | inferred |
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** The Security & session table mandates step-up re-auth and required MFA for Approver actions, but no task flow (Approve Transaction, Reject Transaction), business rule (BR-01..BR-07), RBAC matrix, or functional requirement mentions any re-auth or MFA step — the matrix shows plain `A†BR-01` / `A†BR-02` with no MFA gate.
- **Recommendation:** Either delete the step-up and MFA rows from §6.6.1 or add explicit steps, a business rule (e.g., BR-08), and matrix annotation (`A†BR-08`) for the Approve/Reject flows so all sections agree.

#### ADV-53 — Transactions GET p99 target inconsistent with stated volumes

- **Severity:** Blocker
- **Disposition:** Patch
- **Location:** §6.6.2 vs §10 / §6.6.2 CSV row
- **Evidence:**
  > | p95 page TTI on Transaction Table | ≤ 2 s for ≤ 1 000 rows | inferred |
  > | API p99 latency for `/v1/transactions` GET | ≤ 500 ms | inferred |
  > | API p99 latency for approve / reject | ≤ 800 ms | inferred |
  > | CSV export ready-to-download | ≤ 3 s for ≤ 10 000 rows | inferred |
- **Problem:** The transactions GET p99 target is bounded at ≤1 000 rows on the page-TTI line but unqualified on the API line, while §10 states `10³–10⁵ transactions retained per active file log overall` and CSV export is sized to ≤10 000 rows — implying GETs and exports beyond the implied 1 000-row scope have no defined performance target and may not meet 500 ms.
- **Recommendation:** Add an explicit row-count qualifier (and pagination assumption) to the `/v1/transactions` GET target, or state a separate target for large/export queries consistent with the 10⁵ retained volume.

#### ADV-54 — Logout requirement contradicts RBAC matrix

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.1 vs §6.5
- **Evidence:**
  > - Allow Approvers to log out via an endpoint that invalidates the session cookie.
- **Problem:** Only Approvers are named as able to log out in §6.1, but the RBAC matrix grants both Importer and Approver `X` on Authentication and §5 Flow: Authentication is open to both roles; logout availability is therefore contradicted between sections.
- **Recommendation:** Reword the functional bullet to "Allow all authenticated users to log out…" (or otherwise broaden it) so it aligns with the RBAC matrix and the Authentication flow.

#### ADV-55 — Mermaid FileLog uses CurrentStatus while §7 mandates LastExecutedActivityName

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §2.4 Diagram vs §7 Entity: File Log
- **Evidence:**
  > class FileLog {
  >       +Id
  >       +FileName
  >       +RecordCount
  >       +ProcessDate
  >       +CurrentStatus
  >       +IsActive
  >     }
- **Problem:** The class diagram shows `CurrentStatus` as the FileLog status attribute, but §7 makes `LastExecutedActivityName` the required, enum-constrained, user-visible status and demotes `CurrentStatus` to an optional "Operational status complement" — the diagram contradicts the canonical entity definition.
- **Recommendation:** Update the Mermaid FileLog class to include `+LastExecutedActivityName` (and either drop or annotate `+CurrentStatus`) so it matches §7's required/optional split.

#### ADV-56 — Mermaid Transaction omits required fields from §7

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §2.4 + §6.3 vs §7 Entity: Transaction
- **Evidence:**
  > class Transaction {
  >       +Id
  >       +FileLogId
  >       +Reference
  >       +TransactionDate
  >       +AccountNumber
  >       +Amount
  >       +Currency
  >       +Status
  >       +UserNote
  >     }
- **Problem:** The Mermaid Transaction omits `TransactionType` (required, enum {C,D} in §7) and `Description`, and §6.3 Data does not mention persisting TransactionType or FileName denormalisation — the canonical entity in §7 introduces fields that contradict the simpler shape declared elsewhere.
- **Recommendation:** Either add `TransactionType`, `Description`, and `FileName` to the diagram and the §6.3 data bullets, or remove them from §7 if they are not in scope.

#### ADV-57 — FileSetting / FileSettingId / SettingId naming drift

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §2.1 / §5 / §7 / §9
- **Evidence:**
  > | SettingId | int | yes | references FileSetting.Id | Upload-time setting reference. |
  > | SettingName | string | yes | — | Snapshot of FileSetting.Name at upload. |
- **Problem:** Upload flow and functional requirements name the inputs `FileSettingId` and `FileSettingName`, but §7's File Log entity stores them as `SettingId` / `SettingName`; furthermore `FileSetting` is recognised in §9 terminology but never appears as a Concept in §2.1 — a naming/scope drift across three sections.
- **Recommendation:** Pick one canonical name (`FileSettingId` / `FileSettingName`) and use it consistently in §5, §6.1, and §7, and add `FileSetting` to the §2.1 Concepts table.

#### ADV-58 — RecordCount type contradiction across sections

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §7 Entity: File Log
- **Evidence:**
  > | RecordCount | string | yes | numeric | Number of transactions parsed from the file; API returns as string. |
- **Problem:** RecordCount is declared as `string` with `numeric` validation in §7, but the Mermaid diagram lists it as a plain `+RecordCount` attribute and §6.4 ties pagination and sorting to numeric semantics — typing it as a string in the canonical entity contradicts the way it is rendered/sorted elsewhere.
- **Recommendation:** Either change the type to `int`/`number` in §7 and note the API-string quirk separately, or explicitly document a parse-on-read convention so downstream sorting/display is unambiguous.

#### ADV-59 — UserNote required-flag semantics conflict across §2.4 / §7 / BR-02

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §7 Entity: Transaction UserNote
- **Evidence:**
  > | UserNote | string | yes when Status = Rejected | non-empty on Reject | Rejection rationale. |
- **Problem:** §7 marks UserNote as `yes when Status = Rejected`, implying conditional required, but the Required column header is binary and the §2.4 diagram shows `+UserNote` unconditionally on Transaction; BR-02 enforces non-empty only at Reject — three sections describe the same field with subtly conflicting required semantics.
- **Recommendation:** Change Required to `conditional` (or `no` with a validation expression) and add a footnote referencing BR-02; keep the diagram annotation aligned by marking UserNote optional unless Status = Rejected.

#### ADV-60 — Importer `C` on File Log conflates with File Upload action

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.5 vs §5 File Upload / BR-04
- **Evidence:**
  > | Importer | R | C R | R | X | X | X | X | X | — | — | — | X |
- **Problem:** The matrix grants Importer `C R` on `File Log` but only `X` on `File Upload`; however the File Upload flow states `Available to Importer only; Approver cannot upload`, while BR-04 hides the Upload route for Approver — meanwhile the matrix also lets Approver execute `Authentication` (`X`) and read `File Log` (`R`) but assigns `—` on `File Upload`, which is consistent only if `C` on File Log implies upload. The conflation of `Create File Log` and `Execute File Upload` is internally ambiguous and contradicts the prose that treats upload as Importer-exclusive.
- **Recommendation:** Either remove `C` from Importer's File Log cell (since creation only happens via File Upload, already separately listed) or annotate `C†File-Upload-only` so the matrix unambiguously matches §5 and BR-04.

#### ADV-61 — Audit fields scope contradicted across §6.3 and §6.6.4

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.6.4 vs §6.3
- **Evidence:**
  > - Audit trail: every approve, reject, upload, login, and logout event is recorded with `LastChangedUser` and `LastChangedDate`; retain 7 years.
- **Problem:** §6.6.4 lists login and logout among audited events using `LastChangedUser` / `LastChangedDate`, but §6.3 scopes those audit fields to `mutating action against File Log, Transaction, and User entities` — login/logout are not mutations on those entities, so the two sections disagree on where the audit record lives.
- **Recommendation:** Either add an explicit Auth/Session audit log scope to §6.3 (e.g., `Capture LastChangedUser/Date on auth events`) or remove login/logout from the §6.6.4 audit-trail enumeration.

---

## Dimension 7 — Edge Cases & Error Handling

### Findings

#### ADV-62 — File upload has no size / type / virus / partial-failure rules

- **Severity:** Blocker
- **Disposition:** Patch
- **Location:** §6.1 Functional / §5 File Upload
- **Evidence:**
  > - Allow Importers to upload a transaction file with FileSettingId, FileSettingName, and FileName, and create a corresponding File Log on the server.
  > - Process uploaded files into Transactions; expose the file's lifecycle via `LastExecutedActivityName` / `CurrentStatus` on the File Log.
- **Problem:** The file-upload requirement names no maximum file size, no allowed file types/extensions, no virus/malware scan, and no per-row parse-failure handling — exactly the canonical 'file upload with no max size, no virus check, no failure mode' gap called out in Dimension 7.
- **Recommendation:** Add explicit limits (max file size, allowed MIME types/extensions, max rows per file, malware-scan step) and define partial-failure handling: how many bad rows abort the file, how parse errors are surfaced per row, and what File State a partially-parseable file lands in.

#### ADV-63 — Export volume exceeds documented SLA without fallback

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.2 / §10
- **Evidence:**
  > | Data volume | 10²–10⁴ transactions per file; 10³–10⁵ transactions retained per active file log overall | inferred |
- **Problem:** Volumes go up to 10⁵ transactions per file log but the only export SLA is for ≤10 000 rows, and there is no defined behaviour when an Approver triggers an export of a filtered set that exceeds this limit (no row cap, no async/email-delivery fallback, no truncation warning).
- **Recommendation:** Specify the maximum exportable row count and the UI behaviour when exceeded: e.g., reject with a guidance message, force a narrower filter, or switch to async generation with an in-app notification when ready.

#### ADV-64 — Concurrent approve/reject has no server-side conflict rule

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 Approve / Reject / BR-06
- **Evidence:**
  > | BR-06 | When a transaction's status changes (Approved or Rejected), then the new status must be reflected in the transaction table without a manual refresh. | UI | → §2.3 Transaction invariant | major |
- **Problem:** There is no concurrency rule for the case where two Approvers act on the same Imported transaction simultaneously — BR-01 only hides actions after status changes locally; nothing defines server-side last-write semantics, optimistic-lock errors, or what the losing Approver's UI shows.
- **Recommendation:** Add a business rule and exception path for concurrent approve/reject: e.g., server rejects the second mutation with a 409 "transaction no longer Imported", UI shows a non-dismissible toast naming the winning actor and refreshes the row.

#### ADV-65 — Approve / Reject network-failure path undefined

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 Approve / Reject Transaction / §6.1
- **Evidence:**
  > | Steps | 1. Select transaction. 2. Click Approve. 3. Confirm action in modal. 4. Status updates to Approved. |
  > | Decision points | Confirmation modal naming the affected transaction. |
  > | Exception paths | If the transaction is not in Imported status, Approve is hidden per BR-01. |
- **Problem:** Neither approve nor reject defines what happens on network failure / server error after the confirmation modal is submitted — no state-preservation contract (does the modal stay open?), no retry affordance, no idempotency guarantee against double-clicks resubmitting the same approval.
- **Recommendation:** Add explicit exception paths for network and 5xx failures (keep modal open, surface inline error, offer retry) and require an idempotency key on POST approve/reject so resubmits do not double-record audit entries.

#### ADV-66 — Upload idempotency undefined

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 File Upload / §6.2
- **Evidence:**
  > | Steps | 1. Select file (drag & drop supported). 2. Provide FileSettingId, FileSettingName, FileName. 3. Submit upload. 4. System creates File Log. 5. Status shown in UI. |
  > | Decision points | Required metadata must be provided before upload can proceed: FileSettingId, FileSettingName, FileName. |
  > | Exception paths | Success / failure feedback is rendered after upload. On failure, the file is not parsed and no File Log row is created in a Completed state. |
- **Problem:** Upload idempotency is undefined: if an Importer re-submits the same file (same FileHash) — intentionally or after a flaky network — there is no rule saying whether a duplicate File Log is created, deduplicated, or rejected, despite §7 already capturing a SHA-256 FileHash on File Log.
- **Recommendation:** Add a business rule: "When an Importer uploads a file whose FileHash already exists in a non-Failed File Log, the server rejects with a duplicate-upload error and the UI offers a link to the existing File Log."

#### ADV-67 — Per-field validation rules absent

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.4 / §6.6.5
- **Evidence:**
  > - Synchronous form validation (format, required, length) runs on blur; cross-field and server-side validation runs on submit; no validation runs on keystroke.
- **Problem:** Validation behaviour is described generically but individual named requirements lack per-field validation rules: max length of the mandatory rejection UserNote (§7 only says "non-empty"), max length of FileName / FileSettingName at upload, and the email format error message — leaving "invalid email, oversize file, malformed input" surfaces unspecified.
- **Recommendation:** For each user-supplied field (UserNote, FileName, SettingName, Email, Password), specify min/max length, allowed character set, and the exact inline error message; for oversize files, define the pre-upload UI rejection before the network call.

#### ADV-68 — Session-expiry mid-action recovery missing

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Idle session timeout | 15 minutes | inferred (financial domain default) |
  > | Absolute session timeout | 8 hours | inferred (financial domain default) |
  > | Idle warning lead-time | 60 seconds before idle logout | inferred (financial domain default) |
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
- **Problem:** There is no defined recovery behaviour when the session expires mid-action: an Approver halfway through typing a rejection note, or an Importer mid-upload, will silently lose work — no "preserve draft, prompt re-auth, replay action" rule exists.
- **Recommendation:** Add a requirement: on 401 during a mutating action, preserve the in-flight form state (rejection note, upload metadata), surface a step-up re-auth modal, and replay the original action on success.

#### ADV-69 — No password-reset / account-recovery flow

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 Authentication / §6.6.1
- **Evidence:**
  > | Account lockout policy | 5 failed attempts → 15-minute cooldown; cooldown resets on successful authentication | inferred |
- **Problem:** Lockout policy is defined but there is no password-reset / account-recovery flow anywhere in §5 task flows, §6.1 functional requirements, or §6.5 RBAC — meaning a locked Approver has no documented recovery path, which is a canonical Dimension 7 recovery-path gap.
- **Recommendation:** Either add an out-of-scope marker stating recovery is handled by an external IdP, or specify a password-reset flow with verification channel, token TTL, and UI entry point from the login error state.

#### ADV-70 — Retry-failed-file flow does not exist

- **Severity:** Major
- **Disposition:** Patch
- **Location:** BR-07 / §5 File Summary View
- **Evidence:**
  > | BR-07 | When a file log is in Failed state, then the file summary view must surface the failure prominently and inhibit drill-down into transactions until retry succeeds. | UI | → §2.3 File Log invariant | major |
- **Problem:** BR-07 names a "retry" but no requirement, flow, or RBAC cell defines a retry action: there is no actor, trigger, endpoint, or success/failure behaviour for retrying a Failed File Log, so the rule cannot be implemented as written.
- **Recommendation:** Add a "Retry Failed File" flow in §5 with actor (Importer), trigger, steps, and exception paths, plus a corresponding RBAC cell and functional requirement; or relax BR-07 to permanent failure with a re-upload pathway.

#### ADV-71 — Approve reversal workflow referenced but absent

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 Approve Transaction / §6.1
- **Evidence:**
  > | Context (frequency / expertise / stakes) | Many per day; senior reviewer; reversible only by separate workflow. |
- **Problem:** Story text claims Approve is "reversible only by separate workflow" but no such workflow exists in §5 task flows, §6.1 functional requirements, or §6.5 RBAC — so the documented undo/recovery path for the system's most consequential action is absent, despite Dimension 7 explicitly listing undo as a recovery path to check.
- **Recommendation:** Either remove the "reversible only by separate workflow" claim from the Approve story, or add the reversal flow (likely an Approver-initiated "Reverse Approval" with mandatory note, audit entry, and BR governing eligibility window).

#### ADV-72 — No authorization-failure UX for direct route access

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 Authentication / §6.5
- **Evidence:**
  > | Importer | R | C R | R | X | X | X | X | X | — | — | — | X |
  > | Approver | R | R | R U†BR-01 | X | — | X | X | X | A†BR-01 | A†BR-02 | X | X |
- **Problem:** There is no defined authorization-failure UX when a role lands on a forbidden route directly (e.g., an Approver navigating to /upload or an Importer to /export): BR-03/BR-04 only say controls are hidden, not what a deep-link request returns or how the UI handles a 403.
- **Recommendation:** Add a requirement: "Direct navigation to a route the current role lacks redirects to the role's landing page and surfaces a non-blocking toast naming the missing permission; the server returns 403 with no resource disclosure."

#### ADV-73 — Export failure path / audit undefined

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §5 Export Transactions / §6.4
- **Evidence:**
  > | Exception paths | An empty filtered dataset still produces a header-only CSV; the user is informed via a toast. |
- **Problem:** Export has no network-failure or partial-failure surface: if CSV generation fails server-side (timeout, 5xx), or the browser cancels the download, there is no documented retry, no resumption, and no audit of failed export attempts despite §6.6.4 mandating audit of "every approve, reject, upload, login, and logout event".
- **Recommendation:** Add an exception path for export failure (toast with retry CTA, no partial file written) and extend the audit-trail list in §6.6.4 to include export events so failed-export attempts are traceable.

---

## Dimension 8 — Feasibility & Constraints

### Findings

#### ADV-74 — POPIA mentioned without concrete controls

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.4
- **Evidence:**
  > - POPIA (South Africa) — implied by the use of ZAR currency in the sample dataset and South African account-number formats.- Audit trail: every approve, reject, upload, login, and logout event is recorded with `LastChangedUser` and `LastChangedDate`; retain 7 years.
  > - No PII is rendered in error toasts or browser console.
- **Problem:** POPIA is named only as "implied" with no concrete treatment of data residency, PII inventory, consent flows, retention windows per data class, or subject-access/erasure obligations — yet the system handles AccountNumber, Email, names, and financial transactions which are POPIA-bearing.
- **Recommendation:** Add explicit POPIA controls: a PII inventory (Email, FirstName/LastName, AccountNumber, Amount, Reference), data-residency requirement (RSA region), retention per data class (transactions vs audit vs user records), lawful-basis statement, and subject-access/erasure procedure.

#### ADV-75 — Performance thresholds lack stack / index / measurement context

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.2
- **Evidence:**
  > | p95 page TTI on Transaction Table | ≤ 2 s for ≤ 1 000 rows | inferred |
  > | API p99 latency for `/v1/transactions` GET | ≤ 500 ms | inferred |
  > | API p99 latency for approve / reject | ≤ 800 ms | inferred |
  > | CSV export ready-to-download | ≤ 3 s for ≤ 10 000 rows | inferred |
- **Problem:** Performance thresholds are stated without reference to the implementation stack, expected indexing, or measurement methodology — and the CSV-export budget of 3 s for 10 000 rows is suspect for a synchronous browser download without a streaming/async strategy named.
- **Recommendation:** Either qualify each threshold with the stack/index assumptions and a measurement method (synthetic load, percentile window, dataset size), or downgrade the CSV-export target and specify an async/streaming export mechanism with a job-status surface.

#### ADV-76 — Step-up / MFA / lockout asserted with no mechanism

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.1
- **Evidence:**
  > | Re-auth scope | Step-up authentication required for approve and reject actions | inferred (financial domain default) |
  > | Account lockout policy | 5 failed attempts → 15-minute cooldown; cooldown resets on successful authentication | inferred |
  > | MFA requirement | Optional for Importer; required for Approver | inferred |
- **Problem:** Step-up auth, MFA-for-Approver, and account-lockout are asserted with no mechanism named (TOTP? WebAuthn? SMS?) and no integration point — the auth-api source only documents password + session cookie, so these requirements are not buildable as written.
- **Recommendation:** Either bind each control to a concrete mechanism and endpoint (e.g., "TOTP via POST /v1/auth/step-up, cached for N minutes per session"), or mark them as out-of-scope-for-MVP until the auth API supports them.

#### ADV-77 — Availability SLA without observability / backup / DR support

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.3
- **Evidence:**
  > | Target uptime | 99.5 % during business hours; 99.0 % overall | inferred |
  > | Maintenance window | Weekly Sunday 02:00–04:00 local time | inferred |
  > | RTO / RPO | RTO 4 hours / RPO 1 hour | inferred |
- **Problem:** Availability targets (99.5 %, RTO 4 h / RPO 1 h) are stated but the document names no logging, monitoring, alerting, backup, or DR mechanism — so the operational claim "we will run this in production" is unsupported and the RPO is unverifiable.
- **Recommendation:** Add a §6.6 subsection on operability covering structured-log destinations, metrics/alerting thresholds (for the p95/p99 budgets), backup cadence consistent with RPO 1 h, and a DR runbook reference.

#### ADV-78 — Audit retention without per-entity policy

- **Severity:** Major
- **Disposition:** Patch
- **Location:** §6.6.4
- **Evidence:**
  > Audit trail: every approve, reject, upload, login, and logout event is recorded with `LastChangedUser` and `LastChangedDate`; retain 7 years.
- **Problem:** A 7-year retention is asserted for audit but no retention window is given for the underlying Transaction, File Log, or User records — and POPIA Section 14 requires retention to be no longer than necessary per data class, so a single 7-year blanket is non-compliant by omission.
- **Recommendation:** Define per-entity retention: e.g., Transaction 7 y (financial-record statutory), File Log payload 90 days post-Completed, User records purged 30 days after deactivation, audit events 7 y immutable — and cite the statutory basis for each.

#### ADV-79 — No browser / OS / device matrix

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §6.4 (breakpoint)
- **Evidence:**
  > - On screens below 768 px, tables collapse into a vertical card list (primary identifier + 2–3 key columns + overflow).
- **Problem:** The only device-class statement is a 768 px breakpoint; there is no named browser/version matrix or OS target, making the surface "works everywhere" rather than testable.
- **Recommendation:** Add a "Supported runtimes" row to §6.6 naming concrete versions (e.g., Chrome ≥120, Edge ≥120, Firefox ≥120, Safari ≥17; Windows 10+, macOS 13+; no IE/Edge-Legacy).

#### ADV-80 — No delivery / team / cost constraint stated

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** §1 header
- **Evidence:**
  > **Created:** 2026-05-13 · **Status:** final · **Last finalised at:** 2026-05-13
- **Problem:** The document is marked final but states no delivery timeline, team size, or cost envelope — feasibility cannot be assessed against constraints that are not present.
- **Recommendation:** Add a "Delivery constraints" note (target ship date, team composition assumption, hosting-cost envelope) or explicitly mark these as out-of-scope-for-requirements so reviewers know the omission is intentional.

#### ADV-81 — BR-06 "real-time" without latency budget

- **Severity:** Minor
- **Disposition:** Patch
- **Location:** BR-06
- **Evidence:**
  > | BR-06 | When a transaction's status changes (Approved or Rejected), then the new status must be reflected in the transaction table without a manual refresh. | UI | → §2.3 Transaction invariant | major |
- **Problem:** BR-06 mandates real-time reflection of status changes with no latency budget and no mechanism (polling cadence? websocket? SSE?) — a "real-time" requirement without a latency budget is a classic feasibility flag.
- **Recommendation:** Bind BR-06 to a concrete latency target and mechanism, e.g., "reflected within 2 s via short-poll at 1 Hz" or "via SSE channel /v1/transactions/stream with p95 ≤ 1 s", and budget the additional load on §6.6.2.

---

## Diagnostics

### Quality gates

| Gate | Result | Notes |
|------|--------|-------|
| 1. All findings have 8 schema fields populated | PASS | 81/81 findings have Dimension, Severity, Disposition, Location, Evidence, Problem, Recommendation (ID assigned at merge). |
| 2. All Dimension fields are 1..8                | PASS | Distribution 13/11/10/8/9/10/12/8 across Dim 1..8 sums to 81. |
| 3. All Severity fields are valid                | PASS | Blocker/Major/Minor only; lowercased worker values were normalised at Step 3b merge. |
| 4. All Disposition fields are valid             | PASS | Patch/Defer/Reject only; no out-of-vocabulary values. |
| 5. All Evidence quotes are verbatim & ≤5 lines  | PASS (post-normalisation) | 9 worker quotes spliced non-adjacent rows or exceeded 5 lines; Step 3b normalised them to strict-verbatim contiguous spans without altering finding substance — see normalisation log below. |
| 6. All Location anchors exist in requirements   | PASS | Every Location field references a section / BR / G ID / line that exists in the doc's anchor index. |
| 7. Every dimension has ≥1 finding or Justification | PASS | All eight dimensions returned Variant A (findings list ≥1); no Justification blocks needed. |
| 8. All Justifications are ≥3 sentences          | N/A | No Justification blocks produced (no zero-finding dimensions). |
| 9. Verdict matches disposition tally            | PASS | 5 Blocker severities → BLOCKED per the disposition→verdict mapping. |
| 10. Findings Table row count = per-dim sum      | PASS | 81 table rows = 13+11+10+8+9+10+12+8. |
| 11. REQUIREMENTS_SHA256 matches Step-2 capture  | PASS | Header SHA equals Step-2 capture `6f9272bbb30d1dce025b843f5319e790bdaa5ac2a07103204bbea7144694f0ae`. |

### Coverage map

| Dimension | Sections / IDs touched | Finding count |
|-----------|------------------------|---------------|
| 1. Completeness & Gaps        | §6.5, §6.6.1, §6.6.3, §6.6.4, §6.4, §6.1, §7, G-04, BR-07 | 13 |
| 2. Ambiguity & Clarity        | §6.4, §6.6.1, §6.6.3, §6.6.5, §6.3, §6.1, §7, §10, §5 File Summary View, BR-07 | 11 |
| 3. Testability & Verifiability| §6.6.5, §6.6.2, §6.6.1, §6.6.3, §6.6.4, §6.4, §5 (Approve/Reject/Upload), BR-06 | 10 |
| 4. Scope & MVP Boundaries     | §6, §10 (doc end), §6.6.1, §6.4, §6.6.3, §6.6.4, §3 vs §6.5, BR-07 | 8 |
| 5. Dependency & Ordering      | §7 File Log, §4.1, §6.6.1, §5 (Auth/Approve/Reject/Upload), §6.1, §6.5, BR-06, BR-07 | 9 |
| 6. Consistency & Internal Conflict | §6.6.1, §6.6.2, §6.1, §2.4, §7, §6.5, §6.3, §6.6.4 | 10 |
| 7. Edge Cases & Error Handling | §5 (Upload/Approve/Reject/Auth/Export/Summary), §6.1, §6.4, §6.5, §6.6.1, §6.6.5, BR-06, BR-07 | 12 |
| 8. Feasibility & Constraints  | §1 header, §6.4, §6.6.1, §6.6.2, §6.6.3, §6.6.4, BR-06 | 8 |

### Strict-BMAD re-run log

No dimensions triggered the strict-BMAD re-run rule.

### Override log

All quality gates passed; no override invoked.

### Step 3b evidence-normalisation log

Nine worker-emitted Evidence quotes were normalised at merge to satisfy gate 5 (verbatim, ≤5 lines, contiguous span). Substance of each finding is unchanged; only the quote boundary was tightened:

- ADV-31 (Dim 3 F7): worker quoted lines 269–274 partially (six display lines, ending mid-row); narrowed to the single contiguous Steps row at line 275.
- ADV-48 (Dim 5 F6): worker dropped leading `| ` / trailing ` |` on a table-cell quote; restored to the full verbatim cell.
- ADV-52 (Dim 6 F1): worker spliced lines 366 + 368, omitting line 367, and fabricated `(financial domain default)` on the MFA row; replaced with verbatim lines 366–368 contiguously.
- ADV-53 (Dim 6 F2): worker spliced non-adjacent §6.6.2 rows; replaced with contiguous lines 376–379.
- ADV-57 (Dim 6 F6): worker quote contained a literal `...` ellipsis between non-adjacent rows; narrowed to the contiguous SettingId/SettingName rows (lines 431–432).
- ADV-63 (Dim 7 F2): worker spliced §6.6.2 CSV row + §10 Volume row from different sections; narrowed to the single §10 Volume row.
- ADV-65 (Dim 7 F4): worker spliced Approve-flow Steps + Exception paths, omitting the Decision points row between them; replaced with contiguous lines 275–277.
- ADV-66 (Dim 7 F5): worker spliced File-Upload Steps + Exception paths, omitting Decision points; replaced with contiguous lines 231–233.
- ADV-68 (Dim 7 F7): worker spliced Idle session + Idle warning + Re-auth rows, omitting the Absolute session row between them; replaced with contiguous lines 363–366.

This normalisation was performed silently at Step 3b under the standing "work without stopping for clarifying questions" directive. It is documented here for auditability; the consultant's Step-13 Accept/Revise/Restart loop remains the final filter.
