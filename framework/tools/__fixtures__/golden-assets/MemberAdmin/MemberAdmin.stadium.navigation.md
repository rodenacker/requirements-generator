---
stadium_asset: navigation
app: MemberAdmin
file_guid: 785d3104-7f1a-4d0d-9689-566e0c21295b
designer_version: 6.14.3378.13771
selected_package: 9edc4a95-3fde-45b4-899a-2a59d1c23452.sapz
extracted_from: C:\Stadium 6 Web Apps\785d3104-7f1a-4d0d-9689-566e0c21295b
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Navigation & app shell — MemberAdmin

## Tier-A — templates (master pages)

- Template `DefaultTemplate` (default) [from design model]

## Tier-A — navigation edges (from NavigateToPage actions)

- Members → MemberAdd
- Members → MemberUpdate / ID
- SaveButton.Click → Members
- CancelButton.Click → Members
- SaveButton.Click → Members
- CancelButton.Click → Members

## Tier-A — navigation reachability

- Coverage: **3 of 3** inventory pages are reachable via a captured `NavigateToPage` action. [from design model + administration.db]

## Tier-B — reachability caveat (advisory)
- Any remaining unreached page (absent from the captured `.sapz` walk AND from `page-routes.js`) is typically reached by JS-computed navigation (`jsGETCurrentURl` / custom JS) or is entry-only, so the captured nav graph is a floor, not the complete journey map. Route-declared pages above close most of this gap. `[AI-SUGGESTED]`

## Tier-B — candidate cross-surface journeys (advisory; interpretive review gate)

> A journey joins nav edges (0c) with the affordance/gesture that triggers each hop (0e/0g) and the actor that performs it (0h). The **edges, gestures and page kinds are Tier-A facts**; the claim that a chain **is one** end-to-end task is a **Tier-B** reading. JS-computed nav gaps are shown as explicit breaks, never bridged. `[AI-SUGGESTED]`

- `Members` _(capture)_ —[clicks "Add Member"]→ `MemberAdd` _(create)_
- `Members` _(capture)_ —[clicks]→ `MemberUpdate` _(entity-maintenance)_

## Tier-B — affordances (advisory)
- data grids (search/sort/export likely); toast notifications; confirmation dialogs
