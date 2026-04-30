# Data Domain Model — v1

This document defines the data domain model derived from the Operations Portal v1 requirements (`requirements-v1.md`). It describes all entities, their attributes, relationships, and key constraints.

---

## 1. Entity Overview

```
User (is_platform_admin)
 ├── TenantMembership ──► Tenant (status: active/suspended)
 └── RoleAssignment ──► Tenant | Project | Environment (via resource_id)

Tenant
 └── Project
      ├── Application
      │    └── Build ──► ContainerImage
      └── Environment
           ├── Instance (Application × Environment)
           │    ├── InstancePort (0..*)
           │    ├── Deployment
           │    ├── ResourceLink ──► Database | ObjectStorageBucket
           │    └── ConfigurationValue / Secret
           ├── Database
           ├── ObjectStorageBucket
           └── ConfigurationValue / Secret (environment-level)

AuditEntry (cross-cutting, immutable)
Backup (cross-cutting, linked to Database | ObjectStorageBucket)
```

---

## 2. Entities

### 2.1 User

A person who uses the portal. Exists at the system level, independent of any tenant.

| Attribute         | Type      | Constraints                 | Source           |
| ----------------- | --------- | --------------------------- | ---------------- |
| id                | UUID      | PK                          | —                |
| email             | String    | Unique, immutable, not null | AUTH-06, USR-01  |
| display_name      | String    | Editable by user            | USR-10           |
| is_platform_admin | Boolean   | Not null, default false     | PADM-01, PADM-08 |
| created_at        | Timestamp | Not null                    | —                |

**Notes:**

- Password management is handled by the identity provider, not stored by the portal (USR-10).
- A user may have zero or more tenant memberships.
- Platform administrator status is independent of tenant memberships — a user may be a platform admin with or without any tenant memberships (PADM-01).
- The platform must prevent removal of the last platform administrator (PADM-08).

---

### 2.2 Tenant

A consulting company or organisation. Top-level isolation boundary.

| Attribute | Type | Constraints | Source |
| --- | --- | --- | --- |
| id | UUID | PK | — |
| url_id | String | Unique, immutable, lowercase alphanumeric + hyphens | Naming Convention |
| display_name | String | Editable, not null | Naming Convention, TEN-07 |
| status | Enum | `active`, `suspended`. Not null, default `active` | PADM-05 |
| identity_providers | List\<String\> | Not empty. Includes `email_password` as a provider alongside SSO providers (e.g., `google`, `microsoft`, `oidc`). `email_password` may only be removed if at least one other provider remains. | AUTH-04, TEN-07 |
| created_at | Timestamp | Not null | — |

**Constraints:**

- Maximum 100 tenants system-wide (NFR-40).
- Full data, compute, database, and storage isolation between tenants (TEN-01 through TEN-04, TEN-06).
- Suspension prevents all tenant members from accessing the tenant and stops all running instances. Data is preserved (PADM-05).
- Deletion only permitted if the tenant is suspended and has no running instances, databases, or storage buckets. Requires typing the tenant url_id to confirm (PADM-06).

---

### 2.3 TenantMembership

The association between a User and a Tenant.

| Attribute     | Type      | Constraints           | Source |
| ------------- | --------- | --------------------- | ------ |
| id            | UUID      | PK                    | —      |
| user_id       | UUID      | FK → User, not null   | USR-01 |
| tenant_id     | UUID      | FK → Tenant, not null | USR-01 |
| last_login_at | Timestamp | Nullable              | USR-04 |
| created_at    | Timestamp | Not null              | —      |

**Constraints:**

- Unique on (user_id, tenant_id).
- Removing a user from a tenant deletes the TenantMembership and all their RoleAssignments for that tenant and its descendant resources. Audit history and resource attribution are preserved via the User reference (USR-05).
- A user operates in one tenant context at a time (TEN-06).

---

### 2.4 RoleAssignment

Grants a user a role on a specific resource (tenant, project, or environment). Scope is encoded in the role name prefix. Note: the Platform Administrator role is stored on the User entity (`is_platform_admin`), not as a RoleAssignment, because it is system-level and not scoped to any tenant.

| Attribute            | Type      | Constraints                                                | Source  |
| -------------------- | --------- | ---------------------------------------------------------- | ------- |
| id                   | UUID      | PK                                                         | —       |
| tenant_membership_id | UUID      | FK → TenantMembership, not null                            | RBAC-03 |
| resource_id          | UUID      | Polymorphic — references a Tenant, Project, or Environment | RBAC-03 |
| role                 | Enum      | See role list below                                        | RBAC-05 |
| created_at           | Timestamp | Not null                                                   | —       |

**Roles:**

- **Tenant-scoped** (resource_id → Tenant): `tenant_admin`
- **Project-scoped** (resource_id → Project): `project_admin`, `project_operator`, `project_viewer`
- **Environment-scoped** (resource_id → Environment): `env_operator`, `env_viewer`

**Constraints:**

- Unique on (tenant_membership_id, resource_id, role).
- The role prefix must match the resource type (enforced by application logic).
- A user is assigned to a project if any RoleAssignment exists where resource_id is that project or an environment within it (PRJ-02).
- A user may have different roles on different projects (PRJ-05).
- Permission resolution: most specific scope wins. An environment-level role overrides the project-level role for that environment; a project-level role overrides the tenant-level role for that project.
- Role assignments must be audited (RBAC-06).
- Each tenant must have at least one `tenant_admin` role assignment at all times. The system must prevent any action (role reassignment, membership deactivation, or membership removal) that would leave a tenant with zero tenant administrators (RBAC-07).

---

### 2.5 Project

A client engagement or initiative within a tenant.

| Attribute    | Type      | Constraints                                                       | Source                    |
| ------------ | --------- | ----------------------------------------------------------------- | ------------------------- |
| id           | UUID      | PK                                                                | —                         |
| tenant_id    | UUID      | FK → Tenant, not null                                             | PRJ-01                    |
| url_id       | String    | Unique within tenant, immutable, lowercase alphanumeric + hyphens | Naming Convention         |
| display_name | String    | Editable, not null                                                | PRJ-06, Naming Convention |
| description  | String    | Editable, nullable                                                | PRJ-06                    |
| created_at   | Timestamp | Not null                                                          | —                         |

**Constraints:**

- Deletion only permitted when no associated resources exist (environments, applications, databases, storage, secrets) (PRJ-07).
- All resources are scoped to a project (PRJ-03).

---

### 2.6 Environment

A logical grouping within a project (e.g., dev, staging, production).

| Attribute    | Type      | Constraints                                                        | Source                    |
| ------------ | --------- | ------------------------------------------------------------------ | ------------------------- |
| id           | UUID      | PK                                                                 | —                         |
| project_id   | UUID      | FK → Project, not null                                             | ENV-01                    |
| url_id       | String    | Unique within project, immutable, lowercase alphanumeric + hyphens | Naming Convention         |
| display_name | String    | Editable, not null                                                 | ENV-08, Naming Convention |
| created_at   | Timestamp | Not null                                                           | —                         |

**Constraints:**

- Each environment has its own instances, configuration, databases, and storage (ENV-02).
- Deletion only permitted when no running instances, databases, or storage buckets exist (ENV-09).

---

### 2.7 Application

A deployable unit of software defined at the project level.

| Attribute          | Type      | Constraints                         | Source |
| ------------------ | --------- | ----------------------------------- | ------ |
| id                 | UUID      | PK                                  | —      |
| project_id         | UUID      | FK → Project, not null              | APP-01 |
| display_name       | String    | Editable, not null                  | APP-06 |
| description        | String    | Editable, nullable                  | APP-06 |
| git_provider       | Enum      | `github`, `bitbucket`               | APP-01 |
| git_repository_url | String    | Not null, validated at registration | APP-01 |
| git_subdirectory   | String    | Nullable (defaults to repo root)    | APP-03 |
| build_branch       | String    | Not null, editable                  | BLD-02 |
| created_at         | Timestamp | Not null                            | —      |

**Constraints:**

- Multiple applications may reference the same Git repository (APP-03).
- Deletion only permitted if the application has no running instances (APP-07).
- Git credentials are stored as project-level secrets (APP-02).

---

### 2.8 Instance

The per-environment running form of an application.

| Attribute | Type | Constraints | Source |
| --- | --- | --- | --- |
| id | UUID | PK | — |
| application_id | UUID | FK → Application, not null | INS-01 |
| environment_id | UUID | FK → Environment, not null | INS-01 |
| url_id | String | Unique within environment, immutable, lowercase alphanumeric + hyphens | Naming Convention, NET-01, NET-04 |
| current_build_id | UUID | FK → Build, nullable (null if not yet deployed). The build's build_number is the user-facing version shown in the UI. | BLD-03, INS-01 |
| health_status | Enum | `running`, `degraded`, `stopped`, `failed` | INS-09 |
| replica_count | Integer | 1–10 (default 1); represents desired replica count | INS-07 |
| resource_profile | Enum | `small`, `medium`, `large` | INS-10, INS-11 |
| health_check | String | Default `:8080/health`, format `:<port><path>`, overridable | INS-13, INS-14 |
| created_at | Timestamp | Not null | — |

**Constraints:**

- Internal DNS: reachable at `<instance-url-id>` within its environment (NET-01).
- Public URL (when exposed via InstancePort): `<instance-url-id>.<env-url-id>.<project-url-id>.<tenant-url-id>.<portal-domain><path_prefix>` routes to the corresponding internal port (NET-04).
- If no InstancePort records exist, the instance is not publicly accessible.
- Rolling updates with automatic rollback on health check failure (INS-04).

---

### 2.9 InstancePort

An exposed port mapping for an instance, enabling multiple ports to be publicly routable with distinct path prefixes.

| Attribute     | Type      | Constraints                        | Source |
| ------------- | --------- | ---------------------------------- | ------ |
| id            | UUID      | PK                                 | —      |
| instance_id   | UUID      | FK → Instance, not null            | NET-03 |
| internal_port | Integer   | Not null, 1–65535                  | NET-03 |
| path_prefix   | String    | Not null, default `/`              | NET-03 |
| display_name  | String    | Nullable (e.g., "API", "Admin UI") | —      |
| created_at    | Timestamp | Not null                           | —      |

**Constraints:**

- Unique on (instance_id, internal_port) — a port can only be exposed once per instance.
- Unique on (instance_id, path_prefix) — each path prefix must be unique within the instance to allow unambiguous routing.

---

### 2.10 Build

The process of compiling source code into a container image.

| Attribute | Type | Constraints | Source |
| --- | --- | --- | --- |
| id | UUID | PK | — |
| application_id | UUID | FK → Application, not null | BLD-01 |
| build_number | Integer | Auto-incrementing per application, not null. Primary user-facing version identifier (e.g., Build #1, #2, #3). | BLD-03 |
| status | Enum | `queued`, `in_progress`, `succeeded`, `failed`, `cancelled` | BLD-05, BLD-14 |
| git_commit_sha | String | Not null. Retained for source traceability; displayed in build details. | BLD-03 |
| triggered_by | UUID | FK → User, nullable (null if auto-triggered) | BLD-06, BLD-13 |
| trigger_type | Enum | `automatic`, `manual` | BLD-02, BLD-13 |
| started_at | Timestamp | Nullable | BLD-06 |
| completed_at | Timestamp | Nullable | BLD-06 |
| duration_seconds | Integer | Nullable, computed | BLD-06 |
| log_output | Text | Build logs, captured in real time | BLD-04, BLD-07 |
| created_at | Timestamp | Not null | — |

**Constraints:**

- Automatic trigger: changes to build branch (filtered to subdirectory for monorepos) (BLD-02).
- Builds use a standard platform-provided build image with fixed resource allocations (BLD-12).
- Builds exceeding system-wide timeout are auto-cancelled (BLD-12).

---

### 2.11 ContainerImage

A versioned, runnable container image produced by a build.

| Attribute      | Type      | Constraints                | Source |
| -------------- | --------- | -------------------------- | ------ |
| id             | UUID      | PK                         | —      |
| build_id       | UUID      | FK → Build, not null       | REG-02 |
| application_id | UUID      | FK → Application, not null | REG-03 |
| tag            | String    | Git commit SHA             | BLD-03 |
| created_at     | Timestamp | Not null                   | —      |

**Constraints:**

- Images are scoped to the project that produced them (REG-03).
- Retention policy: retain latest build image, any currently deployed image, and the two most recently previously-deployed images per instance. All others are auto-deleted (REG-04).

---

### 2.12 Deployment

A record of deploying a container image version to an instance.

| Attribute          | Type      | Constraints                          | Source |
| ------------------ | --------- | ------------------------------------ | ------ |
| id                 | UUID      | PK                                   | —      |
| instance_id        | UUID      | FK → Instance, not null              | INS-06 |
| container_image_id | UUID      | FK → ContainerImage, not null        | INS-01 |
| deployed_by        | UUID      | FK → User, not null                  | INS-06 |
| outcome            | Enum      | `succeeded`, `failed`, `rolled_back` | INS-06 |
| deployed_at        | Timestamp | Not null                             | INS-06 |

---

### 2.13 Database

A provisioned PostgreSQL database scoped to an environment.

| Attribute | Type | Constraints | Source |
| --- | --- | --- | --- |
| id | UUID | PK | — |
| environment_id | UUID | FK → Environment, not null | DB-02 |
| database_name | String | Unique within environment, immutable, lowercase alphanumeric + hyphens. User-chosen; also used as the URI slug. | DB-05, Naming Convention |
| status | Enum | `provisioning`, `available`, `deleting`, `error` | DB-03 |
| created_by | UUID | FK → User, not null | — |
| created_at | Timestamp | Not null | — |

**Constraints:**

- Databases are isolated at the database level within their environment (DB-01).
- Deletion blocked if linked to any instance; otherwise requires typing database name to confirm (DB-06).
- Schema migrations are the application's responsibility (DB-07).

---

### 2.14 ObjectStorageBucket

An S3-compatible object storage bucket scoped to a project and environment.

| Attribute | Type | Constraints | Source |
| --- | --- | --- | --- |
| id | UUID | PK | — |
| environment_id | UUID | FK → Environment, not null | OBJ-03 |
| bucket_name | String | Unique within environment, immutable, lowercase alphanumeric + hyphens. User-chosen; also used as the URI slug. | OBJ-04, Naming Convention |
| status | Enum | `provisioning`, `available`, `deleting`, `error` | — |
| created_by | UUID | FK → User, not null | — |
| created_at | Timestamp | Not null | — |

**Constraints:**

- Deletion blocked if linked to any instance; otherwise requires typing bucket name to confirm (OBJ-02).

---

### 2.15 ResourceLink

An association linking a Database or ObjectStorageBucket to an Instance. All must be within the same environment.

| Attribute     | Type      | Constraints                                    | Source |
| ------------- | --------- | ---------------------------------------------- | ------ |
| id            | UUID      | PK                                             | —      |
| instance_id   | UUID      | FK → Instance, not null                        | LNK-01 |
| resource_type | Enum      | `database`, `object_storage_bucket`            | LNK-01 |
| resource_id   | UUID      | FK → Database or ObjectStorageBucket, not null | LNK-01 |
| created_by    | UUID      | FK → User, not null                            | —      |
| created_at    | Timestamp | Not null                                       | —      |

**Constraints:**

- Unique on (instance_id, resource_type, resource_id).
- The linked resource and the instance must be in the same environment (LNK-01).
- On link: connection details are auto-injected into the instance (LNK-02, LNK-04).
- On unlink: injected details are removed and instance is restarted (LNK-06).
- On resource deletion: all links are removed and affected instances are restarted (LNK-07).

---

### 2.16 ConfigurationValue

A key-value configuration entry scoped to either an environment or an instance.

| Attribute | Type | Constraints | Source |
| --- | --- | --- | --- |
| id | UUID | PK | — |
| environment_id | UUID | FK → Environment, nullable (set for environment-level) | CFG-01, SEC-06 |
| instance_id | UUID | FK → Instance, nullable (set for instance-level) | CFG-02, SEC-06 |
| key | String | Not null | CFG-01 |
| value | String | Not null. For plain values, holds the actual value. For secrets, holds the vault path/key referencing the external vault. | CFG-05 |
| is_secret | Boolean | Not null, immutable once set to true | CFG-05 |
| created_at | Timestamp | Not null | — |
| updated_at | Timestamp | Not null | — |

**Constraints:**

- Exactly one of environment_id or instance_id must be set (not both, not neither).
- Unique on (environment_id, key) for environment-level; unique on (instance_id, key) for instance-level.
- Instance-level values override environment-level defaults where keys overlap (CFG-02, SEC-06).
- Secret values cannot be unmarked — must delete and recreate as plain (CFG-05).
- Secret values are stored in an external vault; the portal stores only the vault path/key, never the secret itself (SEC-04).
- Secret versioning and rotation are managed by the vault, not by the portal.
- Changes trigger automatic instance restart (CFG-03).

---

### 2.17 AuditEntry

An immutable record of a significant action in the system.

| Attribute            | Type      | Constraints                                                        | Source          |
| -------------------- | --------- | ------------------------------------------------------------------ | --------------- |
| id                   | UUID      | PK                                                                 | —               |
| timestamp            | Timestamp | Not null (serves as creation time)                                 | AUD-03          |
| user_id              | UUID      | FK → User, not null                                                | AUD-03          |
| tenant_id            | UUID      | FK → Tenant, nullable (null for platform-level actions)            | AUD-03, PADM-09 |
| project_id           | UUID      | FK → Project, nullable                                             | AUD-03          |
| environment_id       | UUID      | FK → Environment, nullable                                         | AUD-03          |
| action               | String    | Not null (e.g., `user.invite`, `instance.deploy`, `build.trigger`) | AUD-02, AUD-03  |
| target_resource_type | String    | Not null                                                           | AUD-03          |
| target_resource_id   | UUID      | Not null                                                           | AUD-03          |
| outcome              | Enum      | `success`, `failure`                                               | AUD-03          |
| details              | JSON      | Nullable, additional context                                       | —               |

**Constraints:**

- Immutable — cannot be modified or deleted by any user including administrators (AUD-05).
- Retained for minimum 1 year; older entries may be archived to cold storage but must remain retrievable (AUD-06).
- Searchable/filterable by user, project, action type, resource, time range, and environment (AUD-04).

---

### 2.18 Backup

A record of a backup operation for a stateful resource.

| Attribute            | Type      | Constraints                                    | Source         |
| -------------------- | --------- | ---------------------------------------------- | -------------- |
| id                   | UUID      | PK                                             | —              |
| resource_type        | Enum      | `database`, `object_storage_bucket`            | NFR-60         |
| resource_id          | UUID      | FK → Database or ObjectStorageBucket, not null | NFR-60         |
| backup_type          | Enum      | `automatic`, `manual`                          | NFR-61, NFR-62 |
| status               | Enum      | `in_progress`, `succeeded`, `failed`           | NFR-63         |
| created_at           | Timestamp | Not null                                       | NFR-63         |
| completed_at         | Timestamp | Nullable                                       | —              |
| size_bytes           | Long      | Nullable                                       | —              |
| retention_expires_at | Timestamp | Not null                                       | NFR-61         |

**Constraints:**

- Automatic backups run daily. Daily backups retained for 7 days; weekly backups retained for 30 days (NFR-61).
- Manual backups may be triggered at any time (NFR-62).
- Restore overwrites the target resource fully; linked instances are restarted (NFR-64).
- RPO: 24 hours, RTO: 4 hours (NFR-66).

---

### 2.19 Invitation

A pending invitation for a user to join a tenant. Deleted on acceptance or expiry; historical record is captured via AuditEntry.

| Attribute    | Type      | Constraints                                        | Source |
| ------------ | --------- | -------------------------------------------------- | ------ |
| id           | UUID      | PK                                                 | —      |
| tenant_id    | UUID      | FK → Tenant, not null                              | USR-01 |
| email        | String    | Not null                                           | USR-01 |
| invited_by   | UUID      | FK → User, not null                                | USR-01 |
| project_id   | UUID      | FK → Project, nullable (auto-assign on acceptance) | USR-08 |
| project_role | Enum      | Nullable, set if project_id is set                 | USR-08 |
| created_at   | Timestamp | Not null                                           | —      |

**Constraints:**

- Only pending invitations exist in this entity. On acceptance, the invitation is deleted and a TenantMembership (and optional RoleAssignment) is created. On expiry, the invitation is deleted.
- Email delivery failures are logged and surfaced; invitations may be re-sent (USR-02).

---

## 3. Relationship Diagram

```
┌─────────────────────────┐
│   User                  │
│  (is_platform_admin)    │
└──┬───┬──────────────────┘
   │   │
   │   │ 1..*
   │   ▼
   │  ┌──────────────────┐       ┌─────────────────────────┐
   │  │ TenantMembership │──────►│  Tenant                 │
   │  └──────────────────┘ *..1  │  (status: active/susp.) │
   │                             └─────────────────────────┘
   │                                   │ 1..*
   │ 1..*                              ▼
   ▼                             ┌───────────┐
┌────────────────┐               │  Project  │
│ RoleAssignment │ ─ ─ ─ ─ ─ ─ ─►└─────┬─────┘  resource_id
└────────────────┘  (polymorphic)      │         (polymorphic)
         │                             ├── 1..* ──► Application ──► Build ──► ContainerImage
         │                             │
         └── ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─►└── 1..* ──► Environment
                                                       │
                                                       ├──► Instance ◄── (Application × Environment)
                                                       │       │
                                                       │       ├──► InstancePort (0..*)
                                                       │       ├──► Deployment
                                                       │       ├──► ResourceLink
                                                       │       └──► ConfigurationValue (instance-level)
                                                       │
                                                       ├──► Database
                                                       ├──► ObjectStorageBucket
                                                       └──► ConfigurationValue (environment-level)
```

---

## 4. Key Enumerations

| Enumeration | Values | Source |
| --- | --- | --- |
| Role | `tenant_admin`, `project_admin`, `project_operator`, `project_viewer`, `env_operator`, `env_viewer` (Platform Admin is stored as `is_platform_admin` on User, not as a Role enum value) | RBAC-05, PADM-01 |
| TenantStatus | `active`, `suspended` | PADM-05 |
| HealthStatus | `running`, `degraded`, `stopped`, `failed` | INS-09 |
| BuildStatus | `queued`, `in_progress`, `succeeded`, `failed`, `cancelled` | BLD-05, BLD-14 |
| BuildTriggerType | `automatic`, `manual` | BLD-02, BLD-13 |
| DeploymentOutcome | `succeeded`, `failed`, `rolled_back` | INS-04, INS-06 |
| ResourceProfile | `small`, `medium`, `large`, `custom` | INS-10, INS-11 |
| ResourceType | `database`, `object_storage_bucket` | LNK-01 |
| GitProvider | `github`, `bitbucket` | APP-01 |
| AuditOutcome | `success`, `failure` | AUD-03 |
| BackupType | `automatic`, `manual` | NFR-61, NFR-62 |
| BackupStatus | `in_progress`, `succeeded`, `failed` | NFR-63 |
| ProvisioningStatus | `provisioning`, `available`, `deleting`, `error` | — |

---

## 5. Cross-Cutting Concerns

### 5.1 URL ID Pattern

Tenants, projects, environments, and instances follow the same naming convention: an editable **display_name** and an immutable **url_id** (lowercase alphanumeric + hyphens, unique within scope). The url_id is used in DNS, URLs, and service discovery. Applications do not have a url_id — they are referenced by display_name and internal id. Databases and object storage buckets use their domain name (**database_name** / **bucket_name**) as the immutable URI slug instead of a separate url_id.

### 5.2 Isolation Boundaries

- **Tenant isolation**: Compute (namespace), database (separate instances), storage (separate volumes), networking (TEN-01 through TEN-04).
- **Project isolation**: Access control — users only see assigned projects (PRJ-02). All resources scoped to project (PRJ-03).
- **Environment isolation**: Separate instances, configuration, databases, storage. No cross-environment networking by default (ENV-04).

### 5.3 Cascade and Deletion Rules

| Entity                            | Deletion Rule                                                                                                | Source  |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------- |
| Tenant                            | Only if suspended and no running instances, databases, or storage buckets; requires typing url_id to confirm | PADM-06 |
| Project                           | Only if no resources exist                                                                                   | PRJ-07  |
| Environment                       | Only if no running instances, databases, or storage buckets                                                  | ENV-09  |
| Application                       | Only if no running instances                                                                                 | APP-07  |
| Database                          | Only if not linked to any instance; requires name confirmation                                               | DB-06   |
| ObjectStorageBucket               | Only if not linked to any instance; requires name confirmation                                               | OBJ-02  |
| ResourceLink (on resource delete) | Auto-removed; affected instances restarted                                                                   | LNK-07  |

### 5.4 Configuration Precedence

Instance-level configuration values override environment-level defaults where keys overlap. This applies to both plain configuration values and secrets (CFG-02, SEC-06).

### 5.5 Audit Coverage

All significant actions are audited (AUD-02). Every entity mutation (create, update, delete) and access-control change must produce an AuditEntry.
