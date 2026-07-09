---
stadium_asset: surfaces
app: ResourceCenter
file_guid: 27cac42c-3dc4-44fd-99a0-84d001ccd971
designer_version: 6.14.3378.13771
selected_package: 4dd7964f-aadd-4ba2-ad82-9cf8fa1f9aa7.sapz
extracted_from: C:\Stadium 6 Web Apps\27cac42c-3dc4-44fd-99a0-84d001ccd971
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Surfaces (screens, controls, layout) — ResourceCenter

> Tier-A = which surfaces/controls/data exist (authoritative). Tier-B = layout & control-choice (advisory; the system holds design authority).

## View / task / feature inventory

> Columns Page / Title / Route / Start / Design-surface / Reachable / Route-declared are **Tier-A** facts (design model + administration.db + rendered `page-routes.js`). **Inferred kind** is **Tier-B** `[AI-SUGGESTED]` (name-suffix taxonomy; bare nouns → entity-maintenance). Title + Route come from the rendered router `[from rendered routes]`.

| Page | Title | Route | Start? | Design surface? | Reachable via nav? | Route-declared? | Inferred kind |
|---|---|---|:---:|:---:|:---:|:---:|---|
| FAQ | FAQ | `/FAQ` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| Docs | Docs | `/Docs` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| Page | Page | `/Page` | ✓ | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |

## FAQ  ·  title: FAQ  ·  roles: User
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container`
        - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `Label1` — "FAQ"
    - StackLayout: `StackLayout`
      - Repeater: `Repeater`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `Label`

## Docs  ·  title: Docs  ·  roles: User
  - GridLayout: `GridLayout`

### source-UI reference — Docs (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `Docs` → `FileSystem.ReadFile`

## Page ⭐ start  ·  title: Page  ·  roles: User
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `Label` — "Resource Center Landing Page"

## User tasks (per view)

> The per-view user-task inventory — the verb-labelled action affordances triangulated with wired backend operations, DataGrids and page-kinds, with a ≥1-task-per-view completeness guarantee — is emitted as its own asset: see `ResourceCenter.stadium.tasks.md`.

## Tier-A — screen ↔ entity (best-effort)

| Page | Likely entity |
|---|---|
| FAQ | — |
| Docs | — |
| Page | — |
