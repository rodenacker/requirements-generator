---
stadium_asset: overview
app: MemberAdmin
file_guid: 785d3104-7f1a-4d0d-9689-566e0c21295b
designer_version: 6.14.3378.13771
selected_package: 9edc4a95-3fde-45b4-899a-2a59d1c23452.sapz
extracted_from: C:\Stadium 6 Web Apps\785d3104-7f1a-4d0d-9689-566e0c21295b
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Stadium app — MemberAdmin

## Tier-A — facts

- App name: **MemberAdmin** [from design model]
- Designer version: 6.14.3378.13771 [from design model]
- Authentication: Cookie [from appsettings]
- Theme: Default [from design model]
- Session timeout: 60 min [from design model]
- Counts: 3 pages, 113 controls, 1 connectors, 12 scripts, 3 roles [from design model]
- Deployment package: 9edc4a95-3fde-45b4-899a-2a59d1c23452.sapz (of 3 deployments) [from administration.db]
- Last published: 2026-06-24 08:45:30.9660341 (designer 6.14.3378.13771) [from administration.db]

## Tier-B — inferred domain (advisory)
- Candidate domain entities (from data operations): Cities, Members `[AI-SUGGESTED: domain inference]`

## Gaps (not ascertainable from source)
- Data schema for connector 'Members' is implied by SQL in 'MembersSelect' but the live database schema/constraints are external. `[AI-SUGGESTED: blocking]`
- Business intent, target users, and success criteria are not present in source and must come from a stakeholder. `[AI-SUGGESTED: blocking]`
- Non-functional requirements (performance, scale, availability, accessibility, browser support, compliance) are not in source. `[AI-SUGGESTED: blocking]`
- Acceptance criteria / test cases are not present in source. `[AI-SUGGESTED: blocking]`

## Asset index
- `MemberAdmin.stadium.data-model.md`
- `MemberAdmin.stadium.data-sources.md`
- `MemberAdmin.stadium.business-rules.md`
- `MemberAdmin.stadium.access-control.md`
- `MemberAdmin.stadium.surfaces.md`
- `MemberAdmin.stadium.navigation.md`
- `MemberAdmin.stadium.glossary.md`
- `MemberAdmin.stadium.design-signals.md`
- `MemberAdmin.stadium.modules.md`
- `MemberAdmin.stadium.task-flows.md`
- `MemberAdmin.stadium.quality-signals.md`
