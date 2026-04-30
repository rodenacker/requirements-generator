# Consultant Answers — Requirements Q&A

**Source draft:** `requirements/requirements-draft.md`
**Captured by:** Requirements Resolver agent (interactive run)
**Captured at:** 2026-04-30
**Consultant:** franz.rodenacker@twenty57.com

## Mode

Level 1 individual Q&A per `framework/skills/run-qa-level1.md`, with the option to switch to Level 2 (accept-all-remaining) at any point.

## Entries

### AI-001
- **Source location:** §0 Header (Domain field) and §1 Domain
- **Original suggestion:** DevOps / Platform-as-a-Service for technical business users
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** DevOps / Platform-as-a-Service for technical business users

### AI-002
- **Source location:** §0 Header (Last finalised at)
- **Original suggestion:** 2026-04-30
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** 2026-04-30

### AI-003
- **Source location:** §1 Business goal
- **Original suggestion:** Enable consulting companies and their technical business-user teams to operate AI-generated custom software without container orchestration or DevOps expertise, while preserving strict tenant and project isolation, full auditability, and enterprise-grade security. The immediate scope is an interactive prototype for stakeholder demo and feedback before committing to full development.
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** Enable consulting companies and their technical business-user teams to operate AI-generated custom software without container orchestration or DevOps expertise, while preserving strict tenant and project isolation, full auditability, and enterprise-grade security. The immediate scope is an interactive prototype for stakeholder demo and feedback before committing to full development.

### AI-004
- **Source location:** §3 Domain entities — Notification row
- **Original suggestion:** Notification | persistent | An asynchronous-operation completion notification delivered to the invoking user.
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** Notification (persistent) — An asynchronous-operation completion notification delivered to the invoking user.

### AI-005
- **Source location:** §3 Relationships — User receives Notification
- **Original suggestion:** User **receives** Notification for asynchronous operations they invoked [1:0..*]
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** User **receives** Notification for asynchronous operations they invoked [1:0..*]

### AI-006
- **Source location:** §6 Platform Administrator persona — Expertise level
- **Original suggestion:** High — comfortable with platform/infrastructure concepts; typically the consulting company's internal IT lead or the on-premise customer's platform owner.
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** High — comfortable with platform/infrastructure concepts; typically the consulting company's internal IT lead or the on-premise customer's platform owner.

### AI-007
- **Source location:** §6 Platform Administrator persona — Driving forces (wants)
- **Original suggestion:** Reliable tenant onboarding, clear visibility of tenant status, clean separation from tenant-internal data, full audit trail.
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** Reliable tenant onboarding, clear visibility of tenant status, clean separation from tenant-internal data, full audit trail.

## Accept-all-remaining

The consultant chose **accept-all-remaining** when asked about AI-008. Per `framework/skills/run-qa-level2.md` and the resolver agent's accept-all-remaining provision, every AI-SUGGESTED ID from AI-008 through AI-087 (inclusive) is recorded below with status `accepted-as-is` and the drafter's verbatim suggestion as the resolved value.

### AI-008
- **Source location:** §6 Platform Administrator persona — Driving forces (fears)
- **Original suggestion:** Accidentally accessing tenant-internal data; deleting an active tenant; leaving the platform without an admin (PADM-08).
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining
- **Follow-ups:** none
- **Resolved value:** Accidentally accessing tenant-internal data; deleting an active tenant; leaving the platform without an admin (PADM-08).

### AI-009
- **Source location:** §6 Tenant Administrator persona — Role / job title
- **Original suggestion:** Tenant Administrator — typically a consulting-company partner, delivery lead, or operations manager.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Tenant Administrator — typically a consulting-company partner, delivery lead, or operations manager.

### AI-010
- **Source location:** §6 Tenant Administrator persona — Expertise level
- **Original suggestion:** Medium-high — comfortable with org/role concepts, OAuth/SSO providers, and project structure; not a DevOps specialist.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Medium-high — comfortable with org/role concepts, OAuth/SSO providers, and project structure; not a DevOps specialist.

### AI-011
- **Source location:** §6 Tenant Administrator persona — Driving forces (wants)
- **Original suggestion:** Quick user onboarding, clear directory of who has access to what, ability to enforce SSO-only login, confidence that membership changes are auditable.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Quick user onboarding, clear directory of who has access to what, ability to enforce SSO-only login, confidence that membership changes are auditable.

### AI-012
- **Source location:** §6 Tenant Administrator persona — Driving forces (fears)
- **Original suggestion:** Letting a former employee retain access; locking the tenant out by removing the last admin; accidentally deleting a project with live resources.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Letting a former employee retain access; locking the tenant out by removing the last admin; accidentally deleting a project with live resources.

### AI-013
- **Source location:** §6 Project Administrator persona — Role / job title
- **Original suggestion:** Project Administrator — the lead for a specific client engagement.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Project Administrator — the lead for a specific client engagement.

### AI-014
- **Source location:** §6 Project Administrator persona — Expertise level
- **Original suggestion:** Medium-high — technically literate business user; understands environments, Git providers, role-based access, but not container orchestration.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Medium-high — technically literate business user; understands environments, Git providers, role-based access, but not container orchestration.

### AI-015
- **Source location:** §6 Project Administrator persona — Frequency of use
- **Original suggestion:** Medium — daily project dashboard checks; environment and membership changes a few times per week.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Medium — daily project dashboard checks; environment and membership changes a few times per week.

### AI-016
- **Source location:** §6 Project Administrator persona — Driving forces (wants)
- **Original suggestion:** A clear project dashboard, simple environment management, reliable Git integration, easy assignment of operators and viewers.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** A clear project dashboard, simple environment management, reliable Git integration, easy assignment of operators and viewers.

### AI-017
- **Source location:** §6 Project Administrator persona — Driving forces (fears)
- **Original suggestion:** Losing track of which member has which role across environments; misconfigured Git credentials breaking builds; deleting an environment that still has resources.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Losing track of which member has which role across environments; misconfigured Git credentials breaking builds; deleting an environment that still has resources.

### AI-018
- **Source location:** §6 Operator persona — Stakes
- **Original suggestion:** High in the moment — incorrect deploys or stopped instances directly affect running applications and clients.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** High in the moment — incorrect deploys or stopped instances directly affect running applications and clients.

### AI-019
- **Source location:** §6 Operator persona — Driving forces (wants)
- **Original suggestion:** Fastest path to deploy, fastest path to logs, immediate visibility of instance health, confidence that rollback is one click away.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Fastest path to deploy, fastest path to logs, immediate visibility of instance health, confidence that rollback is one click away.

### AI-020
- **Source location:** §6 Operator persona — Driving forces (fears)
- **Original suggestion:** Deploying a broken build to production; losing log context during an incident; accidentally deleting an instance, database, or bucket; not noticing a degraded instance.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Deploying a broken build to production; losing log context during an incident; accidentally deleting an instance, database, or bucket; not noticing a degraded instance.

### AI-021
- **Source location:** §6 Viewer persona — Role / job title
- **Original suggestion:** Viewer — read-only stakeholder (often the client, a QA engineer, or a non-technical project lead).
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Viewer — read-only stakeholder (often the client, a QA engineer, or a non-technical project lead).

### AI-022
- **Source location:** §6 Viewer persona — Expertise level
- **Original suggestion:** Low-medium — wants to see status without having to interpret infrastructure terms.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Low-medium — wants to see status without having to interpret infrastructure terms.

### AI-023
- **Source location:** §6 Viewer persona — Stakes
- **Original suggestion:** Low — cannot change anything; risk is misreading status.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Low — cannot change anything; risk is misreading status.

### AI-024
- **Source location:** §6 Viewer persona — Frequency of use
- **Original suggestion:** Very high for dashboard/log viewing during demos, releases, and support windows.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Very high for dashboard/log viewing during demos, releases, and support windows.

### AI-025
- **Source location:** §6 Viewer persona — Driving forces (wants)
- **Original suggestion:** A clear at-a-glance picture of project health, easy navigation to logs and dashboards, masked secrets so they can be shown freely.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** A clear at-a-glance picture of project health, easy navigation to logs and dashboards, masked secrets so they can be shown freely.

### AI-026
- **Source location:** §6 Viewer persona — Driving forces (fears)
- **Original suggestion:** Misreporting status to stakeholders; accidentally trying an action they don't have rights for.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Misreporting status to stakeholders; accidentally trying an action they don't have rights for.

### AI-027
- **Source location:** Goals catalogue — G-01 (UX preference column)
- **Original suggestion:** SSO buttons + email/password fallback
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** SSO buttons + email/password fallback

### AI-028
- **Source location:** Goals catalogue — G-02 (Layout/screen column)
- **Original suggestion:** top bar tenant switcher
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** top bar tenant switcher

### AI-029
- **Source location:** Goals catalogue — G-03 (UX preference column)
- **Original suggestion:** summary cards + status badges
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** summary cards + status badges

### AI-030
- **Source location:** Goals catalogue — G-04 (UX preference column)
- **Original suggestion:** build picker + confirm modal
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** build picker + confirm modal

### AI-031
- **Source location:** Goals catalogue — G-05 (UX preference column)
- **Original suggestion:** log viewer with tail toggle; metric tiles
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** log viewer with tail toggle; metric tiles

### AI-032
- **Source location:** Goals catalogue — G-06 (Layout/screen column)
- **Original suggestion:** application detail → builds tab
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** application detail → builds tab

### AI-033
- **Source location:** Goals catalogue — G-07 (Layout/screen column)
- **Original suggestion:** application settings
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** application settings

### AI-034
- **Source location:** Goals catalogue — G-08 (UX preference column)
- **Original suggestion:** inline action buttons + side panel form
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** inline action buttons + side panel form

### AI-035
- **Source location:** Goals catalogue — G-09 (Layout/screen column)
- **Original suggestion:** environment → databases tab
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** environment → databases tab

### AI-036
- **Source location:** Goals catalogue — G-10 (Layout/screen column)
- **Original suggestion:** environment → buckets tab
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** environment → buckets tab

### AI-037
- **Source location:** Goals catalogue — G-11 (UX preference column)
- **Original suggestion:** link/unlink action with restart-warning modal
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** link/unlink action with restart-warning modal

### AI-038
- **Source location:** Goals catalogue — G-12 (UX preference column)
- **Original suggestion:** key/value table with secret toggle
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** key/value table with secret toggle

### AI-039
- **Source location:** Goals catalogue — G-13 (UX preference column)
- **Original suggestion:** toggle + path/port editor
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** toggle + path/port editor

### AI-040
- **Source location:** Goals catalogue — G-14 (UX preference column)
- **Original suggestion:** backup list + restore wizard
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** backup list + restore wizard

### AI-041
- **Source location:** Goals catalogue — G-15 (UX preference column)
- **Original suggestion:** toast + bell tray
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** toast + bell tray

### AI-042
- **Source location:** Goals catalogue — G-16 (UX preference column)
- **Original suggestion:** directory table + invite modal
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** directory table + invite modal

### AI-043
- **Source location:** Goals catalogue — G-17 (UX preference column)
- **Original suggestion:** matrix or per-user editor
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** matrix or per-user editor

### AI-044
- **Source location:** Goals catalogue — G-18 (UX preference column)
- **Original suggestion:** list + create wizard
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** list + create wizard

### AI-045
- **Source location:** Goals catalogue — G-19 (UX preference column)
- **Original suggestion:** list + create wizard
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** list + create wizard

### AI-046
- **Source location:** Goals catalogue — G-20 (UX preference column)
- **Original suggestion:** filter form + paginated table
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** filter form + paginated table

### AI-047
- **Source location:** Goals catalogue — G-21 (Layout/screen column)
- **Original suggestion:** tenant list + side drawer detail
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** tenant list + side drawer detail

### AI-048
- **Source location:** Goals catalogue — G-22 (UX preference column)
- **Original suggestion:** grantee picker + confirm modal
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** grantee picker + confirm modal

### AI-049
- **Source location:** Goals catalogue — G-23 (Layout/screen column)
- **Original suggestion:** instance overview side panel
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** instance overview side panel

### AI-050
- **Source location:** §8 User-task analysis — Context (frequency / expertise / stakes)
- **Original suggestion:** High / medium / high.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** High / medium / high.

### AI-051
- **Source location:** §8 User-task analysis — Decision points (sign-in flow)
- **Original suggestion:** If email/password is disabled by the tenant, only SSO buttons are shown (AUTH-04). If user has a single tenant membership, route directly to that tenant; otherwise show tenant chooser.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** If email/password is disabled by the tenant, only SSO buttons are shown (AUTH-04). If user has a single tenant membership, route directly to that tenant; otherwise show tenant chooser.

### AI-052
- **Source location:** §8 User-task analysis — Role-conditional behaviour (sign-in flow)
- **Original suggestion:** Platform Administrators may have no tenant membership; route them to the platform admin console instead of a tenant chooser.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Platform Administrators may have no tenant membership; route them to the platform admin console instead of a tenant chooser.

### AI-053
- **Source location:** §8 User-task analysis — Exception paths (tenant suspend)
- **Original suggestion:** Stop-instance failure does not block suspension; failed stops are recorded for retry.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Stop-instance failure does not block suspension; failed stops are recorded for retry.

### AI-054
- **Source location:** §8 User-task analysis — Actor (instance lifecycle task)
- **Original suggestion:** Operator (or Project Administrator)
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Operator (or Project Administrator)

### AI-055
- **Source location:** §8 User-task analysis — Exception paths (instance restart)
- **Original suggestion:** Restart failure → instance enters failed state and surfaces in logs/metrics.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Restart failure → instance enters failed state and surfaces in logs/metrics.

### AI-056
- **Source location:** §8 User-task analysis — Exception paths (restore from backup)
- **Original suggestion:** Restore failure → previous state preserved where possible; failure surfaced in notifications and audit.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Restore failure → previous state preserved where possible; failure surfaced in notifications and audit.

### AI-057
- **Source location:** §RBAC — Action vocabulary legend
- **Original suggestion:** `C` create · `R` read · `U` update · `D` delete · `X` execute / invoke · `A` approve · `—` no access. Suffix with a BR ref for conditional access (e.g. `U†BR-07` = update gated by BR-07). Cells below are inferred from PADM-*, TEN-*, PRJ-*, RBAC-*, USR-*, APP-*, BLD-*, INS-*, ENV-*, DB-*, OBJ-*, CFG-*, SEC-*, NET-*, NFR-6x and the user-tasks document; the detailed permission matrix is to be finalised during design (RBAC-04).
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** `C` create · `R` read · `U` update · `D` delete · `X` execute / invoke · `A` approve · `—` no access. Suffix with a BR ref for conditional access (e.g. `U†BR-07` = update gated by BR-07). Cells below are inferred from PADM-*, TEN-*, PRJ-*, RBAC-*, USR-*, APP-*, BLD-*, INS-*, ENV-*, DB-*, OBJ-*, CFG-*, SEC-*, NET-*, NFR-6x and the user-tasks document; the detailed permission matrix is to be finalised during design (RBAC-04).

### AI-058
- **Source location:** §RBAC — Notes (inferred)
- **Original suggestion:** [The inferred RBAC matrix notes block immediately following the matrix.]
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Accept the inferred RBAC notes block as drafted.

### AI-059
- **Source location:** §NFR Security — Idle session timeout
- **Original suggestion:** 30 minutes
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** 30 minutes

### AI-060
- **Source location:** §NFR Security — Absolute session timeout
- **Original suggestion:** 12 hours
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** 12 hours

### AI-061
- **Source location:** §NFR Security — Idle warning lead-time
- **Original suggestion:** 60 seconds
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** 60 seconds

### AI-062
- **Source location:** §NFR Security — Re-auth scope
- **Original suggestion:** Step-up re-auth for: tenant deletion, platform-admin role grant/revoke, secret rotation, restore-from-backup.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Step-up re-auth for: tenant deletion, platform-admin role grant/revoke, secret rotation, restore-from-backup.

### AI-063
- **Source location:** §NFR Security — Account lockout policy
- **Original suggestion:** 5 failed attempts → 15-minute cooldown for email/password; SSO failures handled by IdP.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** 5 failed attempts → 15-minute cooldown for email/password; SSO failures handled by IdP.

### AI-064
- **Source location:** §NFR Security — MFA requirement
- **Original suggestion:** Required for Platform Administrators; recommended for Tenant Administrators; otherwise per IdP policy.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Required for Platform Administrators; recommended for Tenant Administrators; otherwise per IdP policy.

### AI-065
- **Source location:** §NFR Performance — p95 page TTI on dashboard screens
- **Original suggestion:** < 2s
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** < 2s

### AI-066
- **Source location:** §NFR Performance — Log tail end-to-end latency
- **Original suggestion:** < 3s
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** < 3s

### AI-067
- **Source location:** §NFR Availability — Target uptime
- **Original suggestion:** 99.9%
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** 99.9%

### AI-068
- **Source location:** §NFR Availability — Maintenance window
- **Original suggestion:** Outside business hours, customer-configurable per installation
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Outside business hours, customer-configurable per installation

### AI-069
- **Source location:** §NFR Compliance — Data residency
- **Original suggestion:** Data residency determined by the on-premise / hosted installation choice; the portal does not assume a specific jurisdiction.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Data residency determined by the on-premise / hosted installation choice; the portal does not assume a specific jurisdiction.

### AI-070
- **Source location:** §NFR Compliance — POPIA / GDPR alignment
- **Original suggestion:** POPIA / GDPR alignment expected for hosted deployments; specific compliance regimes to be confirmed per installation.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** POPIA / GDPR alignment expected for hosted deployments; specific compliance regimes to be confirmed per installation.

### AI-071
- **Source location:** §NFR Compliance — PCI-DSS scope
- **Original suggestion:** PCI-DSS scope: out of scope (the portal does not process payment card data).
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** PCI-DSS scope: out of scope (the portal does not process payment card data).

### AI-072
- **Source location:** §NFR Accessibility — WCAG target
- **Original suggestion:** WCAG 2.2 AA target.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** WCAG 2.2 AA target.

### AI-073
- **Source location:** §NFR Accessibility — Keyboard / focus / contrast
- **Original suggestion:** Keyboard-navigable enterprise console; visible focus states; sufficient contrast within the provided colour tokens.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Keyboard-navigable enterprise console; visible focus states; sufficient contrast within the provided colour tokens.

### AI-074
- **Source location:** §NFR Accessibility — Screen-reader support
- **Original suggestion:** Screen-reader support for primary tasks (dashboards, logs, deploys).
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Screen-reader support for primary tasks (dashboards, logs, deploys).

### AI-075
- **Source location:** §9 Domain entity detail (Instance) — Enums note
- **Original suggestion:** HealthStatus = {`running`, `degraded`, `stopped`, `failed`}; ResourceProfile = {`small`, `medium`, `large`}. (The domain model also lists `custom`; v1 inputs only define Small/Medium/Large, so `custom` is excluded from v1.)
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** HealthStatus = {`running`, `degraded`, `stopped`, `failed`}; ResourceProfile = {`small`, `medium`, `large`}. (`custom` excluded from v1.)

### AI-076
- **Source location:** §9 Domain entity detail (Notification) — read_at attribute row
- **Original suggestion:** read_at | Timestamp | no | — | NOT-03
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** read_at | Timestamp | no | — | NOT-03

### AI-077
- **Source location:** §9 Domain entity detail — Notification domain concept tag
- **Original suggestion:** Domain concept: Notification
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Domain concept: Notification

### AI-078
- **Source location:** §9 Notification — NotificationEvent enum
- **Original suggestion:** NotificationEvent = {`build`, `deployment`, `resource_provisioning`}
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** NotificationEvent = {`build`, `deployment`, `resource_provisioning`}

### AI-079
- **Source location:** §9 Notification — NotificationPhase enum
- **Original suggestion:** NotificationPhase = {`start`, `completion`}
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** NotificationPhase = {`start`, `completion`}

### AI-080
- **Source location:** §9 Notification — NotificationStatus enum
- **Original suggestion:** NotificationStatus = {`succeeded`, `failed`, `cancelled`, `rolled_back`}
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** NotificationStatus = {`succeeded`, `failed`, `cancelled`, `rolled_back`}

### AI-081
- **Source location:** §Glossary — Container vs ContainerImage cross-walk
- **Original suggestion:** "Container" is requirements terminology; the equivalent persistent entity is ContainerImage in the domain model.
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** "Container" is requirements terminology; the equivalent persistent entity is ContainerImage in the domain model.

### AI-082
- **Source location:** §Volumes — Projects per tenant
- **Original suggestion:** Up to ~50
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Up to ~50

### AI-083
- **Source location:** §Volumes — Applications per project
- **Original suggestion:** Up to ~30
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Up to ~30

### AI-084
- **Source location:** §Volumes — Instances per environment
- **Original suggestion:** Up to ~30
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Up to ~30

### AI-085
- **Source location:** §Volumes — Builds per application per day
- **Original suggestion:** Up to ~20
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Up to ~20

### AI-086
- **Source location:** §Volumes — Concurrent users (portal-wide)
- **Original suggestion:** Up to ~500
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Up to ~500

### AI-087
- **Source location:** §Volumes — Concurrent users (per tenant)
- **Original suggestion:** Up to ~50
- **Status:** accepted-as-is
- **Consultant answer:** Accept all remaining (bulk)
- **Follow-ups:** none
- **Resolved value:** Up to ~50

