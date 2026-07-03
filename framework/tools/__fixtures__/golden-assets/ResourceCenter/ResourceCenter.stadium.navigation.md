---
stadium_asset: navigation
app: ResourceCenter
file_guid: 27cac42c-3dc4-44fd-99a0-84d001ccd971
designer_version: 6.14.3378.13771
selected_package: 4dd7964f-aadd-4ba2-ad82-9cf8fa1f9aa7.sapz
extracted_from: C:\Stadium 6 Web Apps\27cac42c-3dc4-44fd-99a0-84d001ccd971
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Navigation & app shell — ResourceCenter

## Tier-A — templates (master pages)

- Template `DefaultTemplate` (default) [from design model]

## Tier-A — navigation edges (from NavigateToPage actions)

_No explicit page-navigation actions found._

## Tier-A — navigation reachability

- Coverage: **0 of 3** inventory pages are reachable via a captured `NavigateToPage` action. [from design model + administration.db]
- Orphans (no inbound captured edge): `FAQ`, `Docs`, `Page` _(includes the start page `Page`, the entry point)_

## Tier-B — reachability caveat (advisory)
- Unreached pages are typically reached by JS-computed navigation (`jsGETCurrentURl` / custom JS) or are entry-only, so the captured nav graph is a floor, not the complete journey map. `[AI-SUGGESTED]`

## Tier-B — candidate cross-surface journeys (advisory; interpretive review gate)

> A journey joins nav edges (0c) with the affordance/gesture that triggers each hop (0e/0g) and the actor that performs it (0h). The **edges, gestures and page kinds are Tier-A facts**; the claim that a chain **is one** end-to-end task is a **Tier-B** reading. JS-computed nav gaps are shown as explicit breaks, never bridged. `[AI-SUGGESTED]`

_No navigation affordances from which to derive journeys._

## Tier-B — affordances (advisory)
- file download/export
