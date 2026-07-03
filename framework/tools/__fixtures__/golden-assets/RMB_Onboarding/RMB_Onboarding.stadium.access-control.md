---
stadium_asset: access-control
app: RMB_Onboarding
file_guid: 87ea91de-6125-4686-8437-806216cb0ec0
designer_version: 6.14.3378.13771
selected_package: 3f1ddf96-3519-47b8-905d-b44703776f78.sapz
extracted_from: C:\Stadium 6 Web Apps\87ea91de-6125-4686-8437-806216cb0ec0
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Access control & actors — RMB_Onboarding

## Tier-A — roles & page access

- Authentication: Cookie [from appsettings]
- Roles: User [from admin.db: Roles]

## Tier-A — RBAC posture

- RBAC is effectively **unconfigured** in the deployed app — 1 role (`User`), 1 page grant (the start page), and the operator holds the administrator flag (administrators bypass page-role checks). Actor differentiation is **not modelled** in the app; persona differentiation must come from stakeholder input. [from admin.db]

### Full capability surface (single operator)

> Every inventory page/task is available to the single operator:
- ClientServiceRequest
- ClientApplications
- Enablement
- Dashboard
- pgClientDetails
- pgModularInformation
- pgCollections
- pgAdministrators
- pgAccounts
- pgSignatories
- pgGenerate
- StartPage

## Tier-B — actor candidates (advisory; interpretive review gate)

- Distinct task clusters — `approve/decide`, `capture`, `maintain`, `reporting` — suggest more than one operator role even under a single RBAC role (a capture operator and an approver need not be the same person). `[AI-SUGGESTED]`
> Toast/dialog notifications target the current operator only and are **not** an actor signal.

## Tier-B — actor / persona scaffold (interpretive review gate)

> Grounded skeleton per candidate actor (task-clusters, surfaces, notifications). Persona fields the `.sapz` cannot ground are left as explicit gap prompts — authoring a name/goal/motivation here would fabricate. Skeleton rendered, flesh refused. `[AI-SUGGESTED]`

### Actor candidate: Operator A (approve/decide)  `[AI-SUGGESTED: actor candidate]`
- Task clusters: approve/decide
- Surfaces touched: Enablement
- Notifications sent/received: "Application already vetted" (info); "Application allocated" (info); "'User could not be allocated: ' + {0}" (info); "Application Loading" (info); "Application has been accepted" (success); "Application has been rejected" (info)
- name: `[AI-SUGGESTED: blocking]`
- goal: `[AI-SUGGESTED: blocking]`
- motivation: `[AI-SUGGESTED: blocking]`
- pain-points: `[AI-SUGGESTED: blocking]`
- success-metric: `[AI-SUGGESTED: blocking]`

### Actor candidate: Operator B (capture)  `[AI-SUGGESTED: actor candidate]`
- Task clusters: capture
- Surfaces touched: ClientServiceRequest, pgAccounts, pgAdministrators, pgCollections, pgModularInformation, pgSignatories
- Notifications sent/received: —
- name: `[AI-SUGGESTED: blocking]`
- goal: `[AI-SUGGESTED: blocking]`
- motivation: `[AI-SUGGESTED: blocking]`
- pain-points: `[AI-SUGGESTED: blocking]`
- success-metric: `[AI-SUGGESTED: blocking]`

### Actor candidate: Operator C (maintain)  `[AI-SUGGESTED: actor candidate]`
- Task clusters: maintain
- Surfaces touched: pgAccounts, pgAdministrators, pgCollections, pgModularInformation, pgSignatories
- Notifications sent/received: —
- name: `[AI-SUGGESTED: blocking]`
- goal: `[AI-SUGGESTED: blocking]`
- motivation: `[AI-SUGGESTED: blocking]`
- pain-points: `[AI-SUGGESTED: blocking]`
- success-metric: `[AI-SUGGESTED: blocking]`

### Actor candidate: Operator D (reporting)  `[AI-SUGGESTED: actor candidate]`
- Task clusters: reporting
- Surfaces touched: pgAccounts, pgAdministrators, pgCollections, pgGenerate, pgSignatories
- Notifications sent/received: "Application has been generated" (success)
- name: `[AI-SUGGESTED: blocking]`
- goal: `[AI-SUGGESTED: blocking]`
- motivation: `[AI-SUGGESTED: blocking]`
- pain-points: `[AI-SUGGESTED: blocking]`
- success-metric: `[AI-SUGGESTED: blocking]`

## Tier-A — user population (counts only; identities not extracted)

- 1 user account(s), of which 1 hold the administrator flag. Individual user identities (name / email) are intentionally **not** extracted — PII, and not needed for requirements; the roles + page-access matrix above is the actor model. [from admin.db: Users]
