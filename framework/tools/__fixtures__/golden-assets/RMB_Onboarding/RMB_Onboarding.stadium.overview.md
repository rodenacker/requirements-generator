---
stadium_asset: overview
app: RMB_Onboarding
file_guid: 87ea91de-6125-4686-8437-806216cb0ec0
designer_version: 6.14.3378.13771
selected_package: 3f1ddf96-3519-47b8-905d-b44703776f78.sapz
deployment_count: 1
last_published: 2026-06-30 12:19:12.1887333
extracted_from: C:\Stadium 6 Web Apps\87ea91de-6125-4686-8437-806216cb0ec0
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Stadium app — RMB_Onboarding

## Tier-A — facts

- App name: **RMB_Onboarding** [from design model]
- Authentication: Cookie [from appsettings]
- Theme: Orange [from design model]
- Session timeout: 60 min [from design model]
- Technology baseline: backend **net8.0-windows**, frontend **Vue ^3.5.22** (22 backend package(s), 16 frontend dep(s)) [from .csproj / package.json]

## Tier-B — inferred domain (advisory)
- Candidate domain entities (from data operations): Administrators, ApplicationDocument, ApplicationSteps, BalanceHostToHost, BalanceSetup, BalanceStatementBankAccount, BankAccount, ClientApplications `[AI-SUGGESTED: domain inference]`

## Gaps (not ascertainable from source)
- Data schema for connector 'OnboardingStandardBankCIB' is implied by SQL in 'GetClients' but the live database schema/constraints are external. `[AI-SUGGESTED: blocking]`
- Connector 'FileSystem' references an external filesystem path; the actual files/content are not in the repo. `[AI-SUGGESTED: blocking]`
- Connector 'FileSystemDemo' references an external filesystem path; the actual files/content are not in the repo. `[AI-SUGGESTED: blocking]`
- Connector 'FileSystemData' references an external filesystem path; the actual files/content are not in the repo. `[AI-SUGGESTED: blocking]`
- Data schema for connector 'IDB' is implied by SQL in 'get_AllClientDetails' but the live database schema/constraints are external. `[AI-SUGGESTED: blocking]`
- Business intent, target users, and success criteria are not present in source and must come from a stakeholder. `[AI-SUGGESTED: blocking]`
- Non-functional requirements (performance, scale, availability, accessibility, browser support, compliance) are not in source. `[AI-SUGGESTED: blocking]`
- Acceptance criteria / test cases are not present in source. `[AI-SUGGESTED: blocking]`

## Asset index
- `RMB_Onboarding.stadium.data-model.md`
- `RMB_Onboarding.stadium.data-sources.md`
- `RMB_Onboarding.stadium.business-rules.md`
- `RMB_Onboarding.stadium.access-control.md`
- `RMB_Onboarding.stadium.surfaces.md`
- `RMB_Onboarding.stadium.tasks.md`
- `RMB_Onboarding.stadium.navigation.md`
- `RMB_Onboarding.stadium.glossary.md`
- `RMB_Onboarding.stadium.design-signals.md`
- `RMB_Onboarding.stadium.modules.md`
- `RMB_Onboarding.stadium.task-flows.md`
- `RMB_Onboarding.stadium.quality-signals.md`
