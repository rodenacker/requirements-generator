---
stadium_asset: overview
app: PaymentsApp
file_guid: be54c8c9-dc03-43d5-bc2b-fba14e07f360
designer_version: 6.14.3378.13771
selected_package: 2211275f-1cb9-495c-91cf-4ff48dc4c142.sapz
extracted_from: C:\Stadium 6 Web Apps\be54c8c9-dc03-43d5-bc2b-fba14e07f360
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Stadium app — PaymentsApp

## Tier-A — facts

- App name: **PaymentsApp** [from design model]
- Designer version: 6.14.3378.13771 [from design model]
- Authentication: Cookie [from appsettings]
- Theme: Default [from design model]
- Session timeout: 60 min [from design model]
- Counts: 22 pages, 1459 controls, 5 connectors, 216 scripts, 1 roles [from design model]
- Deployment package: 2211275f-1cb9-495c-91cf-4ff48dc4c142.sapz (of 1 deployments) [from administration.db]
- Last published: 2026-06-30 12:29:25.6302212 (designer 6.14.3378.13771) [from administration.db]

## Tier-B — inferred domain (advisory)
- Candidate domain entities (from data operations): ApprovalLevel, ApprovalLevelAmount, ApprovalLevelRule, Bank, BankAccount, BankAccountType, BankPaymentMethod, BankPaymentSetup `[AI-SUGGESTED: domain inference]`

## Gaps (not ascertainable from source)
- Connector 'FileSystem' references an external filesystem path; the actual files/content are not in the repo. `[AI-SUGGESTED: blocking]`
- Business intent, target users, and success criteria are not present in source and must come from a stakeholder. `[AI-SUGGESTED: blocking]`
- Non-functional requirements (performance, scale, availability, accessibility, browser support, compliance) are not in source. `[AI-SUGGESTED: blocking]`
- Acceptance criteria / test cases are not present in source. `[AI-SUGGESTED: blocking]`

## Asset index
- `PaymentsApp.stadium.data-model.md`
- `PaymentsApp.stadium.data-sources.md`
- `PaymentsApp.stadium.business-rules.md`
- `PaymentsApp.stadium.access-control.md`
- `PaymentsApp.stadium.surfaces.md`
- `PaymentsApp.stadium.tasks.md`
- `PaymentsApp.stadium.navigation.md`
- `PaymentsApp.stadium.glossary.md`
- `PaymentsApp.stadium.design-signals.md`
- `PaymentsApp.stadium.modules.md`
- `PaymentsApp.stadium.task-flows.md`
- `PaymentsApp.stadium.quality-signals.md`
