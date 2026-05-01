# Consultant Answers

> One entry per `[AI-SUGGESTED]` ID from `requirements/requirements-draft.md`. Captured by the requirements-resolver agent.

---

### AI-005
- **Source location:** §1 Application context › Business goal
- **Original suggestion:** Enable consulting companies (and on-premise customers) to deliver, operate, and govern AI-generated custom software for their own clients on a per-project basis, with strict tenant and project isolation, predictable build/deploy/observe workflows, and minimal infrastructure expertise required from end users. The prototype will be demoed to stakeholders as an interactive prototype to gather feedback before full development.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** Enable consulting companies (and on-premise customers) to deliver, operate, and govern AI-generated custom software for their own clients on a per-project basis, with strict tenant and project isolation, predictable build/deploy/observe workflows, and minimal infrastructure expertise required from end users. The prototype will be demoed to stakeholders as an interactive prototype to gather feedback before full development.

---

### AI-006
- **Source location:** §2.2 Relationships
- **Original suggestion:** Application runs as Instance in an Environment [0..* per Application; one per (Application, Environment) by convention]
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** corrected
- **Consultant answer:** Exactly one per (App, Env)
- **Follow-ups:** none
- **Resolved value:** Application runs as Instance in an Environment [0..* per Application; **exactly one** Instance per (Application, Environment) — uniqueness enforced]

---

### AI-007
- **Source location:** §2.3 Aggregates › Project lifecycle states
- **Original suggestion:** Active → Deleted
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Active → Deleted only
- **Follow-ups:** none
- **Resolved value:** Project lifecycle states: Active → Deleted (hard-delete gated by PRJ-07; no soft-delete or archival in v1).

---

### AI-008
- **Source location:** §2.3 Aggregates › Environment lifecycle states
- **Original suggestion:** Active → Deleted
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Active → Deleted only
- **Follow-ups:** none
- **Resolved value:** Environment lifecycle states: Active → Deleted (hard-delete gated by ENV-09; no archival in v1).

---

### AI-009
- **Source location:** §2.3 Aggregates › Application lifecycle states
- **Original suggestion:** Registered → Deleted
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Registered → Deleted only
- **Follow-ups:** none
- **Resolved value:** Application lifecycle states: Registered → Deleted (hard-delete gated by APP-07; no Disabled/Archived in v1).

---

### AI-010
- **Source location:** §2.3 Aggregates › Database / ObjectStorageBucket › Error status semantics
- **Original suggestion:** Provisioning → Available → Deleting; Error (terminal/transient)
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** corrected
- **Consultant answer:** Recoverable; auto-retry, surface for manual deletion if it persists
- **Follow-ups:** none
- **Resolved value:** `Error` is a recoverable state. The platform automatically retries the in-flight provisioning or deletion operation; if the resource remains in `Error` after retries are exhausted, the resource is surfaced to the user with the option to delete it manually.

---

### AI-011
- **Source location:** §3 Personas › Platform Administrator › Expertise level
- **Original suggestion:** High — comfortable with multi-tenant SaaS administration; understands isolation, audit, lifecycle, but does not need DevOps depth.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** High — comfortable with multi-tenant SaaS administration; understands isolation, audit, lifecycle, but does not need DevOps depth.

---

### AI-012
- **Source location:** §3 Personas › Platform Administrator › Stakes
- **Original suggestion:** High — actions affect every tenant on the platform; suspension/deletion are destructive.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** High — actions affect every tenant on the platform; suspension/deletion are destructive.

---

### AI-015
- **Source location:** §3 Personas › Tenant Administrator › Expertise level
- **Original suggestion:** Medium-high — strong in user/access governance and SaaS administration, light on container/orchestration concepts.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** Medium-high — strong in user/access governance and SaaS administration, light on container/orchestration concepts.

---

### AI-016
- **Source location:** §3 Personas › Tenant Administrator › Stakes
- **Original suggestion:** High — actions affect the tenant's user base, projects, and cross-project access.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** High — actions affect the tenant's user base, projects, and cross-project access.

---

### AI-019
- **Source location:** §3 Personas › Project Administrator › Expertise level
- **Original suggestion:** Medium-high — comfortable with environments and Git basics; not a DevOps specialist.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** Medium-high — comfortable with environments and Git basics; not a DevOps specialist.

---

### AI-020
- **Source location:** §3 Personas › Project Administrator › Stakes
- **Original suggestion:** Medium — affects the project's environments, members, and integrations but not other projects.
- **Initial classification:** blocking
- **Revised classification:** unchanged
- **Status:** confirmed
- **Consultant answer:** Confirm as-is
- **Follow-ups:** none
- **Resolved value:** Medium — affects the project's environments, members, and integrations but not other projects.
