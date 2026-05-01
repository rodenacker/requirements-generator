# Consultant Answers

> Captured answers for every `[AI-SUGGESTED]` item in `requirements/requirements-draft.md`. Entries appear in resolution order (Phase 1 blocking first, then Phase 2 non-blocking grouped by section heading).

## Phase 1 — Blocking items

> Consultant chose **accept-all-remaining-blocking** in response to the first blocking question (AI-006). All open blocking items are therefore captured as `accepted-as-is`. Per the resolver protocol, the resolver then advanced to Phase 2.

### AI-006
- **Source location:** §3 Target users → Platform Administrator → Stakes
- **Original suggestion:** Very high — actions span all tenants; tenant suspension/deletion are destructive and recorded in audit.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Very high — actions span all tenants; tenant suspension/deletion are destructive and recorded in audit.

### AI-009
- **Source location:** §3 Target users → Tenant Administrator → Stakes
- **Original suggestion:** High — controls memberships, roles, projects, and identity-provider configuration for the entire tenant.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** High — controls memberships, roles, projects, and identity-provider configuration for the entire tenant.

### AI-012
- **Source location:** §3 Target users → Project Administrator → Stakes
- **Original suggestion:** High for that project — controls environments, project members, and Git provider credentials.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** High for that project — controls environments, project members, and Git provider credentials.

### AI-015
- **Source location:** §3 Target users → Operator → Stakes
- **Original suggestion:** High — drives almost all production-affecting actions: builds, deploys, scaling, configuration, secrets, resource provisioning and linking.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** High — drives almost all production-affecting actions: builds, deploys, scaling, configuration, secrets, resource provisioning and linking.

### AI-019
- **Source location:** §3 Target users → Viewer → Stakes
- **Original suggestion:** Low — cannot mutate state but relies on accurate read-only views.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Low — cannot mutate state but relies on accurate read-only views.

### AI-070
- **Source location:** §5 Task flows → Flow: Platform-admin role management → Exception paths
- **Original suggestion:** Granting to unknown email → user is created at system level on next login; warning shown.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Granting to unknown email → user is created at system level on next login; warning shown.

### AI-072
- **Source location:** §5 Task flows → Flow: Manage Git provider credentials (project) → Exception paths
- **Original suggestion:** Validation failure → reason surfaced; credentials not stored on failure.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Validation failure → reason surfaced; credentials not stored on failure.

### AI-073
- **Source location:** §5 Task flows → Flow: Create instance → Decision points
- **Original suggestion:** If no build selected, instance is created without a current build and shown as `stopped` until first deploy.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** If no build selected, instance is created without a current build and shown as `stopped` until first deploy.

### AI-076
- **Source location:** §5 Task flows → Flow: Restore from backup → Role-conditional behaviour
- **Original suggestion:** env_operator or higher in source and target environments.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** env_operator or higher in source and target environments.

### AI-077
- **Source location:** §6.2 Business rules → BR-23 (row-level marker; severity treated as `major`)
- **Original suggestion:** When the user types into a name-confirmation field for a destructive action, then the value must match exactly (case-sensitive); otherwise the action is blocked. Severity: major.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** BR-23 (severity major) is retained as written: case-sensitive exact-match name confirmation for destructive actions.

### AI-080
- **Source location:** §6.5 Access control (RBAC) → matrix notes (whole matrix derivation)
- **Original suggestion:** Notes: Platform Admin operates at system scope and has no access to tenant-internal data. Tenant Admin, Project Admin, Operator, and Viewer all operate within a single tenant context. Project Admin and Operator scopes apply only to the projects/environments where the user holds the role; Viewer applies only where assigned. Role-prefix-to-scope rules from `domain-model-v1.md` §2.4 govern the matrix and are referenced by BR-17. The matrix below is the primary source of truth for portal action gating; cells were derived from the `requirements-v1.md` text and `user-tasks-v1.md` role assignments.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Retain the §6.5 RBAC matrix as drafted (cells, notes, action vocabulary) as the v1 source of truth for portal action gating.

### AI-081
- **Source location:** §6.6.1 Security & session → Idle session timeout
- **Original suggestion:** 30 minutes
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** 30 minutes

### AI-082
- **Source location:** §6.6.1 Security & session → Absolute session timeout
- **Original suggestion:** 12 hours
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** 12 hours

### AI-083
- **Source location:** §6.6.1 Security & session → Idle warning lead-time
- **Original suggestion:** 60 seconds
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** 60 seconds

### AI-084
- **Source location:** §6.6.1 Security & session → Re-auth scope
- **Original suggestion:** Step-up re-authentication required for: granting/revoking platform admin (PADM-08), deleting a tenant (PADM-06), deleting a project (PRJ-07), deleting a database or bucket (DB-06, OBJ-02), and rotating tenant identity-provider settings (TEN-07).
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Step-up re-authentication required for: granting/revoking platform admin (PADM-08), deleting a tenant (PADM-06), deleting a project (PRJ-07), deleting a database or bucket (DB-06, OBJ-02), and rotating tenant identity-provider settings (TEN-07).

### AI-085
- **Source location:** §6.6.1 Security & session → Account lockout policy
- **Original suggestion:** 10 failed login attempts in 15 minutes triggers a 15-minute cooldown lockout; lockout events are audited (AUTH-05).
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** 10 failed login attempts in 15 minutes triggers a 15-minute cooldown lockout; lockout events are audited (AUTH-05).

### AI-086
- **Source location:** §6.6.1 Security & session → MFA requirement
- **Original suggestion:** MFA delegated to the configured identity provider (Google / Microsoft / OIDC). For email/password (when enabled), MFA is required for Platform Admins and Tenant Admins; optional but recommended for Project Admins and Operators; not required for Viewers.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** MFA delegated to the configured identity provider (Google / Microsoft / OIDC). For email/password (when enabled), MFA is required for Platform Admins and Tenant Admins; optional but recommended for Project Admins and Operators; not required for Viewers.

### AI-089
- **Source location:** §6.6.3 Availability → Target uptime
- **Original suggestion:** 99.9% (≈ 8.8h/yr unplanned downtime)
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** 99.9% target uptime (≈ 8.8h/yr unplanned downtime)

### AI-090
- **Source location:** §6.6.3 Availability → Maintenance window
- **Original suggestion:** Outside business hours of the consulting tenant; scheduled, with advance notice; portal downtime does not affect running applications (NFR-21).
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Outside business hours of the consulting tenant; scheduled, with advance notice; portal downtime does not affect running applications (per NFR-21).

### AI-091
- **Source location:** §6.6.4 Compliance & audit → first bullet (regulatory regimes)
- **Original suggestion:** No specific regulatory regime is in scope for v1 of the prototype; the portal must be designed so that future PCI-DSS / GDPR / POPIA scoping (e.g. for a tenant in scope) is feasible without a re-architecture, primarily through tenant isolation (TEN-01..TEN-04) and audit immutability (AUD-05).
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** No specific regulatory regime is in scope for v1 of the prototype; the portal must be designed so future PCI-DSS / GDPR / POPIA scoping is feasible without a re-architecture, primarily via tenant isolation (TEN-01..TEN-04) and audit immutability (AUD-05).

### AI-092
- **Source location:** §6.6.4 Compliance & audit → data residency bullet
- **Original suggestion:** not specified in inputs; for the prototype, treat as single-region.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** Data residency: single-region for the prototype.

### AI-093
- **Source location:** §6.6.5 Accessibility → primary bullet
- **Original suggestion:** Target: WCAG 2.2 AA for the prototype's primary operator surfaces (project dashboard, environment overview, instance detail, logs/metrics, configuration), with full coverage planned for the productionised release. Assistive-tech scope: keyboard navigation and screen-reader labelling for all interactive elements (tables, buttons, modals, toasts).
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** WCAG 2.2 AA target on primary operator surfaces (project dashboard, environment overview, instance detail, logs/metrics, configuration); full-coverage AA planned for production. Assistive-tech scope: keyboard navigation and screen-reader labelling for tables, buttons, modals, and toasts.

### AI-105
- **Source location:** §6.2 Business rules → BR-24 (row-level marker)
- **Original suggestion:** When an authenticated session is idle past the idle timeout, then the user must be redirected to the login screen and a new authentication required (per §6.6.1 idle session timeout AI-081). Severity: blocker.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-blocking
- **Follow-ups:** none
- **Resolved value:** BR-24: When a session is idle past the idle session timeout (30 min, AI-081), redirect to login and require new authentication; severity blocker; enforced in service / UI per AUTH-06 + §6.6.1.

## Phase 2 — Non-blocking items

> Consultant chose **accept-all-remaining-non-blocking** in response to the first non-blocking batch (Document header batch). All open non-blocking items are therefore captured as `accepted-as-is`.

### AI-001
- **Source location:** Document header → Domain field (top-of-document line)
- **Original suggestion:** Cloud application operations / PaaS-style operator portal for custom software
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Cloud application operations / PaaS-style operator portal for custom software

### AI-002
- **Source location:** Document header → Last finalised at
- **Original suggestion:** n/a — document is in draft state
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** n/a — document is in draft state (will be replaced with finalisation timestamp by the merger)

### AI-003
- **Source location:** §1 Application context → Domain
- **Original suggestion:** Cloud application operations / PaaS-style operator portal for custom software
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Cloud application operations / PaaS-style operator portal for custom software

### AI-004
- **Source location:** §2.1 Concepts → Notification row
- **Original suggestion:** A user-scoped completion notice for an asynchronous operation (build, deployment, resource provisioning), retained per NOT-03.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A user-scoped completion notice for an asynchronous operation (build, deployment, resource provisioning), retained per NOT-03.

### AI-005
- **Source location:** §3 Target users → Platform Administrator → Expertise level
- **Original suggestion:** High — comfortable with multi-tenant SaaS administration; not necessarily a Kubernetes specialist
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** High — comfortable with multi-tenant SaaS administration; not necessarily a Kubernetes specialist

### AI-007
- **Source location:** §3 Target users → Platform Administrator → Driving forces — wants
- **Original suggestion:** Clear visibility of all tenants, fast and explicit tenant lifecycle controls, a strong audit trail of every platform-level action.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Clear visibility of all tenants, fast and explicit tenant lifecycle controls, a strong audit trail of every platform-level action.

### AI-008
- **Source location:** §3 Target users → Platform Administrator → Driving forces — fears
- **Original suggestion:** Accidentally suspending or deleting a live tenant; leaking tenant-internal data through the platform view.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Accidentally suspending or deleting a live tenant; leaking tenant-internal data through the platform view.

### AI-010
- **Source location:** §3 Target users → Tenant Administrator → Driving forces — wants
- **Original suggestion:** A clean directory view, frictionless invite/assign flows, easy tenant settings (display name, identity providers).
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A clean directory view, frictionless invite/assign flows, easy tenant settings (display name, identity providers).

### AI-011
- **Source location:** §3 Target users → Tenant Administrator → Driving forces — fears
- **Original suggestion:** Locking out the tenant by removing the last admin; accidentally enabling/disabling SSO incorrectly; granting the wrong role.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Locking out the tenant by removing the last admin; accidentally enabling/disabling SSO incorrectly; granting the wrong role.

### AI-013
- **Source location:** §3 Target users → Project Administrator → Driving forces — wants
- **Original suggestion:** A single overview screen showing the project's environments, applications, statuses; quick environment creation; clear control of project-level Git credentials.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A single overview screen showing the project's environments, applications, statuses; quick environment creation; clear control of project-level Git credentials.

### AI-014
- **Source location:** §3 Target users → Project Administrator → Driving forces — fears
- **Original suggestion:** Misconfiguring environments or Git credentials; missing failed builds or deployments because of a noisy UI.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Misconfiguring environments or Git credentials; missing failed builds or deployments because of a noisy UI.

### AI-016
- **Source location:** §3 Target users → Operator → Driving forces — wants
- **Original suggestion:** Fastest path to instance health and logs (priorities 1–5 in the frequency summary); confident, low-friction deploy with rollback; visible build progress and clear failure output; minimal click count for routine work (NFR-03).
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Fastest path to instance health and logs (priorities 1–5 in the frequency summary); confident, low-friction deploy with rollback; visible build progress and clear failure output; minimal click count for routine work (NFR-03).

### AI-017
- **Source location:** §3 Target users → Operator → Driving forces — fears
- **Original suggestion:** Deploying a broken build to production; losing logs or context during an incident; accidentally deleting a database or bucket; a surprise restart caused by a config change without warning.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Deploying a broken build to production; losing logs or context during an incident; accidentally deleting a database or bucket; a surprise restart caused by a config change without warning.

### AI-018
- **Source location:** §3 Target users → Viewer → Expertise level
- **Original suggestion:** Mixed — may be less technical than operators; should be guided by clear visualisations rather than infrastructure jargon.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Mixed — may be less technical than operators; should be guided by clear visualisations rather than infrastructure jargon.

### AI-020
- **Source location:** §3 Target users → Viewer → Driving forces — wants
- **Original suggestion:** A clear at-a-glance picture of project and environment health; logs and metrics they can read without help.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** A clear at-a-glance picture of project and environment health; logs and metrics they can read without help.

### AI-021
- **Source location:** §3 Target users → Viewer → Driving forces — fears
- **Original suggestion:** Silent failures hidden from view; secrets accidentally exposed in their read-only views (mitigated by SEC-04).
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Silent failures hidden from view; secrets accidentally exposed in their read-only views (mitigated by SEC-04).

### AI-022
- **Source location:** §4.1 Goals catalogue → G-01 → Quality signals
- **Original suggestion:** Low-friction, fast, secure, auditable
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Low-friction, fast, secure, auditable

### AI-023
- **Source location:** §4.1 Goals catalogue → G-01 → Layout pref
- **Original suggestion:** Login + tenant switcher in top bar
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Login + tenant switcher in top bar

### AI-024
- **Source location:** §4.1 Goals catalogue → G-01 → UX-pattern pref
- **Original suggestion:** SSO buttons + email/password fallback; tenant picker dropdown
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** SSO buttons + email/password fallback; tenant picker dropdown

### AI-025
- **Source location:** §4.1 Goals catalogue → G-02 → Quality signals
- **Original suggestion:** Auditable, explicit, hard-to-misuse
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Auditable, explicit, hard-to-misuse

### AI-026
- **Source location:** §4.1 Goals catalogue → G-02 → Layout pref
- **Original suggestion:** Dedicated platform-admin area, separate from tenant scope
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Dedicated platform-admin area, separate from tenant scope

### AI-027
- **Source location:** §4.1 Goals catalogue → G-02 → UX-pattern pref
- **Original suggestion:** List + detail with destructive-action confirmation typeahead
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** List + detail with destructive-action confirmation typeahead

### AI-028
- **Source location:** §4.1 Goals catalogue → G-03 → Quality signals
- **Original suggestion:** Auditable, role-aware, low-friction
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Auditable, role-aware, low-friction

### AI-029
- **Source location:** §4.1 Goals catalogue → G-03 → Layout pref
- **Original suggestion:** Tenant-scoped settings area in sidebar
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Tenant-scoped settings area in sidebar

### AI-030
- **Source location:** §4.1 Goals catalogue → G-03 → UX-pattern pref
- **Original suggestion:** User directory + invite modal; project list
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** User directory + invite modal; project list

### AI-031
- **Source location:** §4.1 Goals catalogue → G-04 → Quality signals
- **Original suggestion:** Discoverable, role-aware, audit-clear
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Discoverable, role-aware, audit-clear

### AI-032
- **Source location:** §4.1 Goals catalogue → G-04 → Layout pref
- **Original suggestion:** Project dashboard as landing surface (T-PRJ-01)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Project dashboard as landing surface (T-PRJ-01)

### AI-033
- **Source location:** §4.1 Goals catalogue → G-04 → UX-pattern pref
- **Original suggestion:** Summary cards for environments/applications + quick actions
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Summary cards for environments/applications + quick actions

### AI-034
- **Source location:** §4.1 Goals catalogue → G-05 → Quality signals
- **Original suggestion:** Low-friction, validated, visible Git status
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Low-friction, validated, visible Git status

### AI-035
- **Source location:** §4.1 Goals catalogue → G-05 → Layout pref
- **Original suggestion:** Application list + detail in project scope
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Application list + detail in project scope

### AI-036
- **Source location:** §4.1 Goals catalogue → G-05 → UX-pattern pref
- **Original suggestion:** Wizard for registration; metadata form for edits
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Wizard for registration; metadata form for edits

### AI-037
- **Source location:** §4.1 Goals catalogue → G-06 → Quality signals
- **Original suggestion:** Real-time, transparent, troubleshootable
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Real-time, transparent, troubleshootable

### AI-038
- **Source location:** §4.1 Goals catalogue → G-06 → Layout pref
- **Original suggestion:** Build history list with detail/log drawer
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Build history list with detail/log drawer

### AI-039
- **Source location:** §4.1 Goals catalogue → G-06 → UX-pattern pref
- **Original suggestion:** Streaming log viewer + status badges
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Streaming log viewer + status badges

### AI-040
- **Source location:** §4.1 Goals catalogue → G-07 → Quality signals
- **Original suggestion:** Confidence-building, reversible, fastest-to-reach
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Confidence-building, reversible, fastest-to-reach

### AI-041
- **Source location:** §4.1 Goals catalogue → G-07 → Layout pref
- **Original suggestion:** Environment overview with instance cards (T-INS-01)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Environment overview with instance cards (T-INS-01)

### AI-042
- **Source location:** §4.1 Goals catalogue → G-07 → UX-pattern pref
- **Original suggestion:** Deploy/rollback dialogs; lifecycle action menus
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Deploy/rollback dialogs; lifecycle action menus

### AI-043
- **Source location:** §4.1 Goals catalogue → G-08 → Quality signals
- **Original suggestion:** Real-time, filterable, comparable
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Real-time, filterable, comparable

### AI-044
- **Source location:** §4.1 Goals catalogue → G-08 → Layout pref
- **Original suggestion:** Tab inside instance detail
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Tab inside instance detail

### AI-045
- **Source location:** §4.1 Goals catalogue → G-08 → UX-pattern pref
- **Original suggestion:** Filterable log viewer; chart grid for metrics
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Filterable log viewer; chart grid for metrics

### AI-046
- **Source location:** §4.1 Goals catalogue → G-09 → Quality signals
- **Original suggestion:** Predictable precedence, auditable, write-only secrets
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Predictable precedence, auditable, write-only secrets

### AI-047
- **Source location:** §4.1 Goals catalogue → G-09 → Layout pref
- **Original suggestion:** Configuration tab with environment/instance toggles
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Configuration tab with environment/instance toggles

### AI-048
- **Source location:** §4.1 Goals catalogue → G-09 → UX-pattern pref
- **Original suggestion:** Key-value editor; rotation flow
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Key-value editor; rotation flow

### AI-049
- **Source location:** §4.1 Goals catalogue → G-10 → Quality signals
- **Original suggestion:** Self-serve, isolation-aware, deletion-safe
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Self-serve, isolation-aware, deletion-safe

### AI-050
- **Source location:** §4.1 Goals catalogue → G-10 → Layout pref
- **Original suggestion:** Environment-scoped resource lists
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Environment-scoped resource lists

### AI-051
- **Source location:** §4.1 Goals catalogue → G-10 → UX-pattern pref
- **Original suggestion:** Provision wizard; type-name-to-confirm delete
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Provision wizard; type-name-to-confirm delete

### AI-052
- **Source location:** §4.1 Goals catalogue → G-11 → Quality signals
- **Original suggestion:** Predictable, visible-side-effects (restart), auditable
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Predictable, visible-side-effects (restart), auditable

### AI-053
- **Source location:** §4.1 Goals catalogue → G-11 → Layout pref
- **Original suggestion:** Linked-resources panel on instance + drawer on resource
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Linked-resources panel on instance + drawer on resource

### AI-054
- **Source location:** §4.1 Goals catalogue → G-11 → UX-pattern pref
- **Original suggestion:** Picker scoped to same environment
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Picker scoped to same environment

### AI-055
- **Source location:** §4.1 Goals catalogue → G-12 → Quality signals
- **Original suggestion:** Explicit, reversible, URL-clear
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Explicit, reversible, URL-clear

### AI-056
- **Source location:** §4.1 Goals catalogue → G-12 → Layout pref
- **Original suggestion:** Networking tab on instance
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Networking tab on instance

### AI-057
- **Source location:** §4.1 Goals catalogue → G-12 → UX-pattern pref
- **Original suggestion:** Toggle + URL display + port mapping editor
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Toggle + URL display + port mapping editor

### AI-058
- **Source location:** §4.1 Goals catalogue → G-13 → Quality signals
- **Original suggestion:** Predictable, recoverable, confirmation-gated
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Predictable, recoverable, confirmation-gated

### AI-059
- **Source location:** §4.1 Goals catalogue → G-13 → Layout pref
- **Original suggestion:** Backups tab on each resource
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Backups tab on each resource

### AI-060
- **Source location:** §4.1 Goals catalogue → G-13 → UX-pattern pref
- **Original suggestion:** Backup list; restore wizard with target selector
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Backup list; restore wizard with target selector

### AI-061
- **Source location:** §4.1 Goals catalogue → G-14 → Quality signals
- **Original suggestion:** Immutable, searchable, scoped-by-permission
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Immutable, searchable, scoped-by-permission

### AI-062
- **Source location:** §4.1 Goals catalogue → G-14 → Layout pref
- **Original suggestion:** Audit page available at platform/tenant/project scopes
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Audit page available at platform/tenant/project scopes

### AI-063
- **Source location:** §4.1 Goals catalogue → G-14 → UX-pattern pref
- **Original suggestion:** Faceted search + entry detail
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Faceted search + entry detail

### AI-064
- **Source location:** §4.1 Goals catalogue → G-15 → Quality signals
- **Original suggestion:** Timely, low-noise, retained per NOT-03
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Timely, low-noise, retained per NOT-03

### AI-065
- **Source location:** §4.1 Goals catalogue → G-15 → Layout pref
- **Original suggestion:** Notification tray in top bar
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Notification tray in top bar

### AI-066
- **Source location:** §4.1 Goals catalogue → G-15 → UX-pattern pref
- **Original suggestion:** Toast + tray history list
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Toast + tray history list

### AI-067
- **Source location:** §4.1 Goals catalogue → G-16 → Quality signals
- **Original suggestion:** Clear, comprehensive, no-mutation paths
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Clear, comprehensive, no-mutation paths

### AI-068
- **Source location:** §4.1 Goals catalogue → G-16 → Layout pref
- **Original suggestion:** Same surfaces as Operator with action affordances disabled
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Same surfaces as Operator with action affordances disabled

### AI-069
- **Source location:** §4.1 Goals catalogue → G-16 → UX-pattern pref
- **Original suggestion:** Same dashboards/lists with read-only badges
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Same dashboards/lists with read-only badges

### AI-071
- **Source location:** §5 Task flows → Flow: Create environment → Decision points
- **Original suggestion:** tenant environment limit reached (NFR-41) → soft warning
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** When the tenant environment limit (NFR-41) is reached → show a soft warning.

### AI-074
- **Source location:** §5 Task flows → Flow: Rotate secret → Exception paths
- **Original suggestion:** Encryption write fails → no version stored, error surfaced.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Encryption write fails → no version stored, error surfaced.

### AI-075
- **Source location:** §5 Task flows → Flow: Link database to instance → Exception paths
- **Original suggestion:** Resource not in `available` state → blocked.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Resource not in `available` state → blocked.

### AI-078
- **Source location:** §6.3 Data → mock-data note bullet
- **Original suggestion:** all data shown in the prototype must be realistic mock data, not lorem ipsum, and no backend is required (per `brief.md` constraints).
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Mock-data note (prototype only): all data shown must be realistic mock data, not lorem ipsum; no backend is required (per `brief.md`).

### AI-079
- **Source location:** §6.4 User-facing → read-only roles affordance bullet
- **Original suggestion:** Read-only roles see all action affordances disabled rather than hidden, with hover/cursor cues.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Read-only roles see all action affordances disabled rather than hidden, with hover/cursor cues.

### AI-087
- **Source location:** §6.6.2 Performance → Project dashboard p95 TTI row
- **Original suggestion:** Project dashboard p95 TTI (PRJ-08): ≤ 2 seconds
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Project dashboard p95 TTI ≤ 2 seconds (specialisation of NFR-30 to the most frequent surface).

### AI-088
- **Source location:** §6.6.2 Performance → Streaming log latency row
- **Original suggestion:** Streaming log latency (display behind producer): ≤ 3 seconds
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Streaming log latency (display behind producer): ≤ 3 seconds.

### AI-094
- **Source location:** §6.6.5 Accessibility → colour contrast bullet
- **Original suggestion:** Colour contrast must meet WCAG 2.2 AA against the supplied tokens; status colours (`success`, `warning`, `danger`) must always pair with text or icon to avoid colour-only signalling.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Colour contrast must meet WCAG 2.2 AA against the supplied tokens; status colours (success, warning, danger) must always pair with text or icon — no colour-only signalling.

### AI-095
- **Source location:** §7 Data entities → Entity: User → Relationships
- **Original suggestion:** User 0..* Notification (per NOT-03).
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** User 0..* Notification (per NOT-03).

### AI-096
- **Source location:** §7 Data entities → Entity: Tenant → url_id validation
- **Original suggestion:** Regex `^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$` for url_id
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** url_id validation regex: `^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$` (applies to all url_id fields: tenant, project, environment, instance — and to database_name / bucket_name).

### AI-097
- **Source location:** §7 Data entities → Entity: Notification → tenant_id field
- **Original suggestion:** FK → Tenant (scope of notification)
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Notification.tenant_id: FK → Tenant (scope of notification), required.

### AI-098
- **Source location:** §7 Data entities → Entity: Notification → seen_at field
- **Original suggestion:** seen_at — Timestamp, nullable
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Notification.seen_at: Timestamp, nullable (set when the user marks a notification as seen).

### AI-099
- **Source location:** §7 Data entities → Entity: Notification → Enums note
- **Original suggestion:** Mixed event/outcome enums above.
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Notification enums are the inline event_type and outcome enumerations declared on the entity.

### AI-100
- **Source location:** §8 Source UI references → "(No screenshots / wireframes supplied)" row
- **Original suggestion:** The brief contains no consultant-supplied screenshots, mock-ups, or links to existing tools. UI structure must be proposed within the constraints of `brief.md` (design system, layout, density).
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** No consultant-supplied screenshots/mock-ups; UI must be proposed within the constraints of `brief.md` (design system, layout, density).

### AI-101
- **Source location:** §10 Volumes → Concurrent portal users (prototype demo)
- **Original suggestion:** ≈ 10 stakeholders concurrently in demo sessions
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Concurrent portal users (prototype demo): ≈ 10 stakeholders concurrently in demo sessions.

### AI-102
- **Source location:** §10 Volumes → Steady-state operators per tenant
- **Original suggestion:** ≈ 5–25 across roles
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Steady-state operators per tenant: ≈ 5–25 across roles.

### AI-103
- **Source location:** §10 Volumes → Applications per project
- **Original suggestion:** ≈ 1–20
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Applications per project: ≈ 1–20.

### AI-104
- **Source location:** §10 Volumes → Builds per application per day
- **Original suggestion:** ≈ 0–10
- **Initial classification:** non-blocking
- **Revised classification:** unchanged
- **Status:** accepted-as-is
- **Consultant answer:** accept-all-remaining-non-blocking
- **Follow-ups:** none
- **Resolved value:** Builds per application per day: ≈ 0–10.

