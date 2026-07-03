---
stadium_asset: overview
app: ResourceCenter
file_guid: 27cac42c-3dc4-44fd-99a0-84d001ccd971
designer_version: 6.14.3378.13771
selected_package: 4dd7964f-aadd-4ba2-ad82-9cf8fa1f9aa7.sapz
extracted_from: C:\Stadium 6 Web Apps\27cac42c-3dc4-44fd-99a0-84d001ccd971
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Stadium app — ResourceCenter

## Tier-A — facts

- App name: **ResourceCenter** [from design model]
- Designer version: 6.14.3378.13771 [from design model]
- Authentication: Cookie [from appsettings]
- Theme: Default [from design model]
- Session timeout: 60 min [from design model]
- Counts: 3 pages, 18 controls, 1 connectors, 4 scripts, 1 roles [from design model]
- Deployment package: 4dd7964f-aadd-4ba2-ad82-9cf8fa1f9aa7.sapz (of 4 deployments) [from administration.db]
- Last published: 2026-06-03 11:01:11.2158983 (designer 6.14.3378.13771) [from administration.db]

## Tier-B — inferred domain (advisory)
- Candidate domain entities (from data operations): — `[AI-SUGGESTED: domain inference]`

## Gaps (not ascertainable from source)
- Connector 'FileSystem' references an external filesystem path; the actual files/content are not in the repo. `[AI-SUGGESTED: blocking]`
- Validation not modelled in the design model (no validators, required-field flags, or control validation rules). `[AI-SUGGESTED: blocking]`
- Business intent, target users, and success criteria are not present in source and must come from a stakeholder. `[AI-SUGGESTED: blocking]`
- Non-functional requirements (performance, scale, availability, accessibility, browser support, compliance) are not in source. `[AI-SUGGESTED: blocking]`
- Acceptance criteria / test cases are not present in source. `[AI-SUGGESTED: blocking]`

## Asset index
- `ResourceCenter.stadium.data-model.md`
- `ResourceCenter.stadium.data-sources.md`
- `ResourceCenter.stadium.business-rules.md`
- `ResourceCenter.stadium.access-control.md`
- `ResourceCenter.stadium.surfaces.md`
- `ResourceCenter.stadium.navigation.md`
- `ResourceCenter.stadium.glossary.md`
- `ResourceCenter.stadium.design-signals.md`
- `ResourceCenter.stadium.modules.md`
- `ResourceCenter.stadium.task-flows.md`
- `ResourceCenter.stadium.quality-signals.md`
