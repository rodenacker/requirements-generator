---
stadium_asset: overview
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
# Stadium app — ResourceCenter

## Tier-A — facts

- App name: **ResourceCenter** [from design model]
- Authentication: Cookie [from appsettings]
- Theme: Default [from design model]
- Session timeout: 60 min [from design model]
- Technology baseline: backend **net8.0-windows**, frontend **Vue ^3.5.22** (22 backend package(s), 16 frontend dep(s)) [from .csproj / package.json]

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
- `ResourceCenter.stadium.tasks.md`
- `ResourceCenter.stadium.navigation.md`
- `ResourceCenter.stadium.glossary.md`
- `ResourceCenter.stadium.design-signals.md`
- `ResourceCenter.stadium.modules.md`
- `ResourceCenter.stadium.task-flows.md`
- `ResourceCenter.stadium.quality-signals.md`
