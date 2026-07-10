---
stadium_asset: tasks
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
# User tasks — MemberAdmin

> One row per derivable USER TASK per view. Each task's EVIDENCE — the view, the wired control→op (`[from rendered view]`), the grid / action column (`[from design model]`), the title (`[from rendered routes]`) — is **Tier-A** (authoritative, `[SRC]`-citable via the inline locator). The task's verb / name is **Tier-B** `[AI-SUGGESTED]` (interpretation). Entities are drawn only from the reconciled set (see `data-model`) — never invented. Every view yields ≥1 row; a view with no derivable task says so explicitly. Confidence: high (wired op + resolved entity) / medium (labelled affordance, grid action, or op without entity) / low (page-kind/title fallback).

## Task inventory

| View | Task `[AI-SUGGESTED]` | Verb | Entity | Conf. | Evidence [from …] |
|---|---|---|---|:--:|---|
| Members | Browse Members | SELECT | Members | high | grid `MembersDataGrid` (searchable) [from design model]; `MembersDGLoad` → `Members.MembersSelect` [from rendered view] |
| Members | Add Member | INSERT | Members | medium | affordance `MemberAddButton` "Add Member" [from design model]; wired to `MemberAddButton.Click` |
| Members | Update Members | UPDATE | Members | medium | action column "Edit" on `MembersDataGrid` [from design model] |
| Members | Delete Members | DELETE | Members | high | `MembersDataGrid` → `Members.MemberDelete` [from rendered view]; action column "Delete" on `MembersDataGrid` [from design model] |
| MemberAdd | Add Members | INSERT | Members | high | `SaveButton` → `Members.MemberInsert` [from rendered view] |
| MemberUpdate | Update Members | UPDATE | Members | high | `SaveButton` → `Members.MemberUpdate` [from rendered view] |

## Per-view notes

- **Members** — actor roles: User, Viewer, AllAccess [from admin.db: PageRole]
- **MemberAdd** — actor roles: AllAccess [from admin.db: PageRole] · supporting reads (lookups / pre-fill, not tasks): `MemberAdd` → `Members.CitiesSelect` [from rendered view]
- **MemberUpdate** — actor roles: AllAccess [from admin.db: PageRole] · supporting reads (lookups / pre-fill, not tasks): `MemberUpdate` → `Members.CitiesSelect` [from rendered view]; `MemberUpdate` → `Members.MemberSelect` [from rendered view]

## Views with no derivable user task

- _(none — every view yielded ≥1 task)_

## Coverage

- **3 / 3** views have ≥1 derived user task; 0 view(s) with no derivable task (listed above).
