# User Tasks — v1

This document catalogues the tasks users perform in the Operations Portal, organised by role and area. Each task includes a frequency rating to help prioritise UI placement, optimisation, and design attention.

## Frequency Scale

| Rating | Meaning | Design implication |
|--------|---------|-------------------|
| **Very high** | Multiple times per day by many users | Must be fastest to reach; optimise for speed and minimal clicks |
| **High** | Daily or several times per week | Should be prominent and easy to find from main navigation |
| **Medium** | Weekly or a few times per month | Accessible but need not dominate primary UI surfaces |
| **Low** | Monthly or during specific events (new project, new hire) | Can live in settings or secondary menus |
| **Very low** | A few times per year or during initial setup | Acceptable in deeper menus; prioritise clarity over speed |

---

## 1. All Authenticated Users

These tasks apply regardless of role. Every user performs them.

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-ALL-01 | Log in (SSO or email/password) | High | AUTH-01 to AUTH-04 |
| T-ALL-02 | Switch tenant context | Medium | AUTH-06, TEN-06 |
| T-ALL-03 | View and edit own profile (display name) | Low | USR-10 |
| T-ALL-04 | Log out | High | AUTH-05 |

---

## 2. Platform Administrator

Platform administrators manage tenants and the platform itself. This is a small number of users performing infrequent but high-impact tasks.

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-PADM-01 | View list of all tenants (name, status, creation date, project count) | Medium | PADM-04 |
| T-PADM-02 | Create a new tenant (display name, url_id, first tenant admin) | Low | PADM-02, PADM-03 |
| T-PADM-03 | Suspend a tenant | Very low | PADM-05 |
| T-PADM-04 | Reactivate a suspended tenant | Very low | PADM-05 |
| T-PADM-05 | Delete a tenant (type url_id to confirm) | Very low | PADM-06 |
| T-PADM-06 | Grant platform administrator role to another user | Very low | PADM-08 |
| T-PADM-07 | Revoke platform administrator role from a user | Very low | PADM-08 |
| T-PADM-08 | View per-tenant summary detail (platform view) | Low | PADM-10 |
| T-PADM-09 | View platform audit trail | Medium | PADM-09, AUD-01 |

---

## 3. Tenant Administrator

Tenant administrators manage users, projects, and tenant-level settings. A handful of users per tenant, performing these tasks as the team changes.

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-TEN-01 | View tenant user directory (members, roles, project assignments, last login) | Medium | USR-04 |
| T-TEN-02 | Invite a user to the tenant by email | Low | USR-01, USR-02 |
| T-TEN-03 | Re-send a failed invitation email | Low | USR-02 |
| T-TEN-04 | Deactivate a user's tenant membership | Low | USR-05 |
| T-TEN-05 | Reactivate a user's tenant membership | Low | USR-06 |
| T-TEN-06 | Assign a user to a project with a role | Low | PRJ-04, USR-08 |
| T-TEN-07 | Remove a user from a project | Low | USR-08 |
| T-TEN-08 | Change a user's role on a project or environment | Low | RBAC-03, USR-08 |
| T-TEN-09 | Create a new project (display name, url_id, description) | Low | PRJ-01 |
| T-TEN-10 | Delete an empty project (confirm) | Very low | PRJ-07 |
| T-TEN-11 | Configure tenant settings (display name, identity providers) | Very low | TEN-07 |

---

## 4. Project Administrator

Project administrators manage environments, users within the project, and project-level settings. Typically a lead per project.

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-PRJ-01 | View project dashboard (environments, applications, statuses) | Very high | PRJ-08 |
| T-PRJ-02 | Edit project name and description | Low | PRJ-06 |
| T-PRJ-03 | View project user directory (members, roles per environment) | Medium | USR-07 |
| T-PRJ-04 | Assign a tenant member to the project | Low | USR-08 |
| T-PRJ-05 | Invite a new user to tenant and assign to project | Low | USR-08, USR-01 |
| T-PRJ-06 | Remove a member from the project | Low | USR-08 |
| T-PRJ-07 | Manage member roles within the project | Low | USR-08 |
| T-PRJ-08 | Create an environment (display name, url_id) | Low | ENV-01 |
| T-PRJ-09 | Edit an environment's display name | Low | ENV-08 |
| T-PRJ-10 | Delete an empty environment (confirm) | Very low | ENV-09 |
| T-PRJ-11 | Manage project integrations (Git provider credentials: GitHub, BitBucket) | Low | APP-02 |
| T-PRJ-12 | Re-send a failed project-scoped invitation | Low | USR-02, USR-08 |

---

## 5. Operator — Application & Build Management

Operators are the primary daily users. They register, build, deploy, and monitor applications. Most portal traffic comes from these tasks.

### 5.1 Application Lifecycle

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-APP-01 | View list of all applications in the project | Very high | APP-04 |
| T-APP-02 | View application detail (Git repo, metadata, per-environment instance status) | Very high | APP-05 |
| T-APP-03 | Register a new application (Git provider, repo URL, branch, optional subdirectory) | Low | APP-01, APP-02, APP-03 |
| T-APP-04 | Edit application metadata (name, description) | Low | APP-06 |
| T-APP-05 | Change build branch | Low | BLD-02 |
| T-APP-06 | Delete an application (confirm, only if no running instances) | Very low | APP-07 |

### 5.2 Builds

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-BLD-01 | View build history for an application (build number, status, trigger, commit, duration) | Very high | BLD-06 |
| T-BLD-02 | Watch a build in progress (status + streaming logs) | High | BLD-04, BLD-05 |
| T-BLD-03 | View build detail (logs, error output, commit SHA) | High | BLD-04, BLD-07 |
| T-BLD-04 | Manually trigger a build | Medium | BLD-13 |
| T-BLD-05 | Cancel an in-progress build | Low | BLD-14 |

### 5.3 Deployment & Instance Management

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-INS-01 | View environment overview (all instances, versions, health) | Very high | ENV-05 |
| T-INS-02 | Check instance health status | Very high | INS-09 |
| T-INS-03a | Create a new application instance in an environment | Low | INS-01, INS-01a, INS-07, INS-10, INS-13 |
| T-INS-03b | Deploy a new build to an existing instance | Medium | INS-01 |
| T-INS-04 | Start a stopped instance | Medium | INS-03 |
| T-INS-05 | Stop a running instance | Medium | INS-03 |
| T-INS-06 | Restart an instance | Medium | INS-03 |
| T-INS-07 | Roll back an instance to a previous build | Low | INS-05 |
| T-INS-08 | View deployment history for an instance | Medium | INS-06 |
| T-INS-09 | Change replica count (scale 1–10) | Low | INS-07 |
| T-INS-10 | Change resource profile (Small / Medium / Large) | Low | INS-10, INS-11 |
| T-INS-11 | Override health check path and port | Low | INS-14 |

### 5.4 Observability

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-OBS-01 | View instance logs (filter by time, keyword, severity) | Very high | OBS-02 |
| T-OBS-02 | Tail instance logs in real time | Very high | OBS-03 |
| T-OBS-03 | View instance metrics dashboard (CPU, memory, error rate, restarts) | High | OBS-11, OBS-12 |
| T-OBS-04 | View request rate and latency dashboard (for publicly exposed instances) | High | OBS-12 |

### 5.5 Configuration & Secrets

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-CFG-01 | View environment-level configuration values | Medium | CFG-01, ENV-06 |
| T-CFG-02 | Add/edit/delete an environment-level configuration value | Medium | CFG-01 |
| T-CFG-03 | View instance-level configuration values (with environment defaults shown) | Medium | CFG-02 |
| T-CFG-04 | Add/edit/delete an instance-level configuration value | Medium | CFG-02 |
| T-CFG-05 | Create a secret (write value, mark as secret) | Low | CFG-05, SEC-01 |
| T-CFG-06 | Rotate (update) a secret value | Low | SEC-07 |
| T-CFG-07 | View secret metadata and version history (no values shown) | Low | SEC-04, SEC-08 |
| T-CFG-08 | Delete a configuration value or secret | Low | — |

### 5.6 Databases

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-DB-01 | View databases in an environment (status, linked applications) | Medium | DB-03 |
| T-DB-02 | Provision a new database | Low | DB-01 |
| T-DB-03 | Delete a database (type name to confirm, blocked if linked) | Very low | DB-06 |

### 5.7 Object Storage

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-OBJ-01 | View storage buckets in an environment (status, usage, linked applications)  | Medium | OBJ-02, OBJ-05 |
| T-OBJ-02 | Create a new storage bucket | Low | OBJ-01, OBJ-02 |
| T-OBJ-03 | Delete a storage bucket (type name to confirm, blocked if linked) | Very low | OBJ-02 |

### 5.8 Resource Linking

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-LNK-01 | View resources linked to an instance (databases, storage buckets) | Medium | LNK-05 |
| T-LNK-02 | Link a database or storage bucket to an instance — may be initiated from the instance's Linked Resources view or from the resource detail drawer on the environment overview | Low | LNK-01, LNK-02, LNK-04 |
| T-LNK-03 | Unlink a resource from an instance (triggers restart) | Low | LNK-06 |

### 5.9 Networking & Public Access

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-NET-01 | View internal address for an instance | Medium | NET-01 |
| T-NET-02 | Expose an instance publicly via the API gateway | Low | NET-02, NET-03 |
| T-NET-03 | View the generated public URL for an exposed instance | Medium | NET-04 |
| T-NET-04 | Remove public access from an instance | Low | NET-03 |

### 5.10 Backups & Restore

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-BAK-01 | View backup status for databases and storage buckets | Medium | NFR-63 |
| T-BAK-02 | Trigger a manual backup of a database or storage bucket | Low | NFR-62 |
| T-BAK-03 | Restore a database or storage bucket from a backup (confirm) | Very low | NFR-64 |

---

## 6. Viewer

Viewers have read-only access. They monitor but cannot change anything. Their tasks are a subset of operator tasks.

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-VIEW-01 | View project dashboard | Very high | PRJ-08 |
| T-VIEW-02 | View application list and details | Very high | APP-04, APP-05 |
| T-VIEW-03 | View environment overview (instances, health, versions) | Very high | ENV-05 |
| T-VIEW-04 | View build history and build detail | High | BLD-06, BLD-04 |
| T-VIEW-05 | View instance logs (filter, search, tail) | Very high | OBS-02, OBS-03 |
| T-VIEW-06 | View metrics dashboards | High | OBS-11, OBS-12 |
| T-VIEW-07 | View deployment history | Medium | INS-06 |
| T-VIEW-08 | View configuration values (secrets masked) | Medium | CFG-01, CFG-02, SEC-04 |
| T-VIEW-09 | View databases and storage buckets | Medium | DB-03, OBJ-02 |
| T-VIEW-10 | View backup status | Medium | NFR-63 |

---

## 7. Audit Trail (Cross-Role)

Available to administrators and operators (scoped by their access level).

| ID | Task | Frequency | Requirements |
|----|------|-----------|--------------|
| T-AUD-01 | Search/filter audit log (by user, project, action, resource, time, environment) | Medium | AUD-04 |
| T-AUD-02 | View audit entry detail | Medium | AUD-03 |

---

## 8. Frequency Summary

The following table ranks task groups by frequency to guide UI prioritisation. Tasks at the top should be the fastest and most prominent in the interface.

| Priority | Task group | Frequency | Typical role |
|----------|-----------|-----------|--------------|
| 1 | Check instance health status | Very high | Operator, Viewer |
| 2 | View instance logs / tail logs | Very high | Operator, Viewer |
| 3 | View project dashboard | Very high | All project members |
| 4 | View environment overview | Very high | Operator, Viewer |
| 5 | View application list and detail | Very high | Operator, Viewer |
| 6 | View build history / watch build | High | Operator, Viewer |
| 7 | View metrics dashboards | High | Operator, Viewer |
| 8 | Deploy a build to an environment | High | Operator |
| 9 | Start / stop / restart instance | Medium | Operator |
| 10 | Manage configuration values | Medium | Operator |
| 11 | View / manage databases and storage | Medium | Operator |
| 12 | Search audit trail | Medium | Admin, Operator |
| 13 | Manage users and roles | Low | Tenant Admin, Project Admin |
| 14 | Manage networking / public access | Low | Operator |
| 15 | Register application / provision resources | Low | Operator |
| 16 | Manage tenant and platform settings | Very low | Platform Admin, Tenant Admin |
