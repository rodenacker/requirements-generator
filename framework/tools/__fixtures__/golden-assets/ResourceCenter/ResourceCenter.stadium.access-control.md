---
stadium_asset: access-control
app: ResourceCenter
file_guid: 27cac42c-3dc4-44fd-99a0-84d001ccd971
designer_version: 6.14.3378.13771
selected_package: 4dd7964f-aadd-4ba2-ad82-9cf8fa1f9aa7.sapz
extracted_from: C:\Stadium 6 Web Apps\27cac42c-3dc4-44fd-99a0-84d001ccd971
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Access control & actors — ResourceCenter

## Tier-A — roles & page access

- Authentication: Cookie [from appsettings]
- Roles: User [from admin.db: Roles]
- **1 role(s), 3 page grant(s) configured** [from admin.db: PageRole]

| Page | Roles with access |
|---|---|
| Docs | User |
| FAQ | User |
| Page | User |

## Tier-B — capability split (advisory)
- `User` → standard operator `[AI-SUGGESTED]`

## Tier-B — actor candidates (advisory; interpretive review gate)

- No action-verb affordances detected, so no task-cluster actor split can be read. `[AI-SUGGESTED]`
> Toast/dialog notifications target the current operator only and are **not** an actor signal.

## Tier-B — actor / persona scaffold (interpretive review gate)

> Grounded skeleton per candidate actor (task-clusters, surfaces, notifications). Persona fields the `.sapz` cannot ground are left as explicit gap prompts — authoring a name/goal/motivation here would fabricate. Skeleton rendered, flesh refused. `[AI-SUGGESTED]`

### Actor candidate: Role: User  `[AI-SUGGESTED: actor candidate]`
- Task clusters: —
- Surfaces touched: Docs, FAQ, Page
- Notifications sent/received: —
- name: `[AI-SUGGESTED: blocking]`
- goal: `[AI-SUGGESTED: blocking]`
- motivation: `[AI-SUGGESTED: blocking]`
- pain-points: `[AI-SUGGESTED: blocking]`
- success-metric: `[AI-SUGGESTED: blocking]`

## Tier-A — user population (counts only; identities not extracted)

- 1 user account(s), of which 1 hold the administrator flag. Individual user identities (name / email) are intentionally **not** extracted — PII, and not needed for requirements; the roles + page-access matrix above is the actor model. [from admin.db: Users]
