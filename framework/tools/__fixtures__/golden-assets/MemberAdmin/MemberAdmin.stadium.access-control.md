---
stadium_asset: access-control
app: MemberAdmin
file_guid: 785d3104-7f1a-4d0d-9689-566e0c21295b
designer_version: 6.14.3378.13771
selected_package: 9edc4a95-3fde-45b4-899a-2a59d1c23452.sapz
deployment_count: 3
last_published: 2026-06-24 08:45:30.9660341
extracted_from: C:\Stadium 6 Web Apps\785d3104-7f1a-4d0d-9689-566e0c21295b
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Access control & actors — MemberAdmin

## Tier-A — roles & page access

- Authentication: Cookie [from appsettings]
- Roles: AllAccess, User, Viewer [from admin.db: Roles]
- **3 role(s), 5 page grant(s) configured** [from admin.db: PageRole]

| Page | Roles with access |
|---|---|
| MemberAdd | AllAccess |
| MemberUpdate | AllAccess |
| Members | AllAccess, User, Viewer |

## Tier-B — capability split (advisory)
- `AllAccess` → full edit / manage `[AI-SUGGESTED]`
- `User` → standard operator `[AI-SUGGESTED]`
- `Viewer` → read-only (view) `[AI-SUGGESTED]`

## Tier-B — actor candidates (advisory; interpretive review gate)

- A single task cluster (`capture`) is evident; the affordances imply no multi-actor split. `[AI-SUGGESTED]`
> Toast/dialog notifications target the current operator only and are **not** an actor signal.

## Tier-B — actor / persona scaffold (interpretive review gate)

> Grounded skeleton per candidate actor (task-clusters, surfaces, notifications). Persona fields the `.sapz` cannot ground are left as explicit gap prompts — authoring a name/goal/motivation here would fabricate. Skeleton rendered, flesh refused. `[AI-SUGGESTED]`

### Actor candidate: Role: AllAccess  `[AI-SUGGESTED: actor candidate]`
- Task clusters: capture
- Surfaces touched: MemberAdd, MemberUpdate, Members
- Notifications sent/received: "'Are you sure you want to delete "' + {0} + '"?'" (dialog); "'Member "' + {0} + '" deleted'" (success)
- name: `[AI-SUGGESTED: blocking]`
- goal: `[AI-SUGGESTED: blocking]`
- motivation: `[AI-SUGGESTED: blocking]`
- pain-points: `[AI-SUGGESTED: blocking]`
- success-metric: `[AI-SUGGESTED: blocking]`

### Actor candidate: Role: User  `[AI-SUGGESTED: actor candidate]`
- Task clusters: capture
- Surfaces touched: Members
- Notifications sent/received: "'Are you sure you want to delete "' + {0} + '"?'" (dialog); "'Member "' + {0} + '" deleted'" (success)
- name: `[AI-SUGGESTED: blocking]`
- goal: `[AI-SUGGESTED: blocking]`
- motivation: `[AI-SUGGESTED: blocking]`
- pain-points: `[AI-SUGGESTED: blocking]`
- success-metric: `[AI-SUGGESTED: blocking]`

### Actor candidate: Role: Viewer  `[AI-SUGGESTED: actor candidate]`
- Task clusters: capture
- Surfaces touched: Members
- Notifications sent/received: "'Are you sure you want to delete "' + {0} + '"?'" (dialog); "'Member "' + {0} + '" deleted'" (success)
- name: `[AI-SUGGESTED: blocking]`
- goal: `[AI-SUGGESTED: blocking]`
- motivation: `[AI-SUGGESTED: blocking]`
- pain-points: `[AI-SUGGESTED: blocking]`
- success-metric: `[AI-SUGGESTED: blocking]`

## Tier-A — user population (counts only; identities not extracted)

- 4 user account(s), 1 with the administrator flag; individual identities (name / email) not extracted — PII. [from admin.db: Users]
