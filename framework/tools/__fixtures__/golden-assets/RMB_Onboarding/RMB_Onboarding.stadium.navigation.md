---
stadium_asset: navigation
app: RMB_Onboarding
file_guid: 87ea91de-6125-4686-8437-806216cb0ec0
designer_version: 6.14.3378.13771
selected_package: 3f1ddf96-3519-47b8-905d-b44703776f78.sapz
extracted_from: C:\Stadium 6 Web Apps\87ea91de-6125-4686-8437-806216cb0ec0
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Navigation & app shell — RMB_Onboarding

## Tier-A — templates (master pages)

- Template `DefaultTemplate` (default) [from design model]

## Tier-A — navigation edges (from NavigateToPage actions)

- ClientServiceRequest → pgClientDetails
- dgSearchCustomers.Launch.Click → ClientServiceRequest
- ClientApplications → pgModularInformation / ClientNumber / ApplicationID / WOID
- Application_Create → pgModularInformation / ClientID / ApplicationID / WOID
- btnClose.Click → ClientServiceRequest
- btnClose.Click → ClientServiceRequest
- btnNext.Click → pgCollections / ApplicationID / ClientID / WOID
- btnNext.Click → pgCollections / ApplicationID / ClientID / WOID
- btnPrevious.Click → pgModularInformation / ApplicationID / ClientID / WOID
- btnNext.Click → pgAdministrators
- btnPrevious.Click → pgCollections
- btnNext.Click → pgAccounts
- btnPrevious.Click → pgAdministrators
- btnNext.Click → pgSignatories
- btnNext.Click → pgSignatories
- btnPrevious.Click → pgAccounts
- btnNext.Click → pgGenerate
- btnPrevious.Click → pgSignatories
- pgGenerate → ClientApplications
- DefaultTemplate → StartPage

## Tier-A — navigation reachability

- Coverage: **10 of 12** inventory pages are reachable via a captured `NavigateToPage` action. [from design model + administration.db]
- Additionally reachable via a declared client route (not on the captured `.sapz` walk): `Enablement`, `Dashboard` [from rendered routes]

## Tier-B — reachability caveat (advisory)
- Any remaining unreached page (absent from the captured `.sapz` walk AND from `page-routes.js`) is typically reached by JS-computed navigation (`jsGETCurrentURl` / custom JS) or is entry-only, so the captured nav graph is a floor, not the complete journey map. Route-declared pages above close most of this gap. `[AI-SUGGESTED]`

## Tier-B — candidate cross-surface journeys (advisory; interpretive review gate)

> A journey joins nav edges (0c) with the affordance/gesture that triggers each hop (0e/0g) and the actor that performs it (0h). The **edges, gestures and page kinds are Tier-A facts**; the claim that a chain **is one** end-to-end task is a **Tier-B** reading. JS-computed nav gaps are shown as explicit breaks, never bridged. `[AI-SUGGESTED]`

- `pgGenerate` _(reporting)_ —[clicks "Generate"]→ `ClientApplications` _(entity-maintenance)_ —[clicks]→ `pgModularInformation` _(capture, maintain)_
- `ClientServiceRequest` _(capture)_ —[clicks "Add"]→ `pgClientDetails` _(detail)_
- **JS-nav gaps** — interactive pages with no captured inbound edge (reached via JS-computed nav): `Enablement` `[gap: JS-computed nav]`

## Tier-B — affordances (advisory)
- data grids (search/sort/export likely); file download/export; toast notifications
