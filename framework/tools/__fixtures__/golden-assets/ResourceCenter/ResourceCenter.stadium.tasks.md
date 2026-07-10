---
stadium_asset: tasks
app: ResourceCenter
file_guid: 27cac42c-3dc4-44fd-99a0-84d001ccd971
designer_version: 6.14.3378.13771
selected_package: 4dd7964f-aadd-4ba2-ad82-9cf8fa1f9aa7.sapz
deployment_count: 4
last_published: 2026-06-03 11:01:11.2158983
extracted_from: C:\Stadium 6 Web Apps\27cac42c-3dc4-44fd-99a0-84d001ccd971
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# User tasks — ResourceCenter

> One row per derivable USER TASK per view. Each task's EVIDENCE — the view, the wired control→op (`[from rendered view]`), the grid / action column (`[from design model]`), the title (`[from rendered routes]`) — is **Tier-A** (authoritative, `[SRC]`-citable via the inline locator). The task's verb / name is **Tier-B** `[AI-SUGGESTED]` (interpretation). Entities are drawn only from the reconciled set (see `data-model`) — never invented. Every view yields ≥1 row; a view with no derivable task says so explicitly. Confidence: high (wired op + resolved entity) / medium (labelled affordance, grid action, or op without entity) / low (page-kind/title fallback).

## Task inventory

| View | Task `[AI-SUGGESTED]` | Verb | Entity | Conf. | Evidence [from …] |
|---|---|---|---|:--:|---|
| FAQ | Update (object unresolved) | UPDATE | — | low | kind `entity-maintenance` `[AI-SUGGESTED]`; title "FAQ" [from rendered routes] |
| Docs | Update (object unresolved) | UPDATE | — | low | kind `entity-maintenance` `[AI-SUGGESTED]`; title "Docs" [from rendered routes] |
| Page | Update (object unresolved) | UPDATE | — | low | kind `entity-maintenance` `[AI-SUGGESTED]`; title "Page" [from rendered routes] |

## Per-view notes

- **FAQ** — actor roles: User [from admin.db: PageRole]
- **Docs** — actor roles: User [from admin.db: PageRole] · supporting reads (lookups / pre-fill, not tasks): `Docs` → `FileSystem.ReadFile` [from rendered view]
- **Page** — actor roles: User [from admin.db: PageRole]

## Views with no derivable user task

- _(none — every view yielded ≥1 task)_

## Coverage

- **3 / 3** views have ≥1 derived user task; 0 view(s) with no derivable task (listed above).
