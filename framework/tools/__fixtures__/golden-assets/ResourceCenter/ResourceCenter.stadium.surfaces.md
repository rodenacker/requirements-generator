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

> Columns Page / Start / Design-surface / Reachable are **Tier-A** facts (design model + administration.db). **Inferred kind** is **Tier-B** `[AI-SUGGESTED]` (name-suffix taxonomy; bare nouns → entity-maintenance).

| Page | Start? | Design surface? | Reachable via nav? | Inferred kind |
|---|:---:|:---:|:---:|---|
| FAQ |  | ✓ |  | entity-maintenance `[AI-SUGGESTED]` |
| Docs |  | ✓ |  | entity-maintenance `[AI-SUGGESTED]` |
| Page | ✓ | ✓ |  | entity-maintenance `[AI-SUGGESTED]` |

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

## Page ⭐ start  ·  title: Page  ·  roles: User
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `Label` — "Resource Center Landing Page"

## Action affordances → candidate tasks

_No action-verb affordances detected on any surface._

## Tier-A — screen ↔ entity (best-effort)

| Page | Likely entity |
|---|---|
| FAQ | — |
| Docs | — |
| Page | — |
