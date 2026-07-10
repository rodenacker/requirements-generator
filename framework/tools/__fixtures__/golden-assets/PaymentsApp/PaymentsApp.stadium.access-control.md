---
stadium_asset: access-control
app: PaymentsApp
file_guid: be54c8c9-dc03-43d5-bc2b-fba14e07f360
designer_version: 6.14.3378.13771
selected_package: 2211275f-1cb9-495c-91cf-4ff48dc4c142.sapz
deployment_count: 1
last_published: 2026-06-30 12:29:25.6302212
extracted_from: C:\Stadium 6 Web Apps\be54c8c9-dc03-43d5-bc2b-fba14e07f360
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Access control & actors — PaymentsApp

## Tier-A — roles & page access

- Authentication: Cookie [from appsettings]
- Roles: User [from admin.db: Roles]

## Tier-A — RBAC posture

- RBAC is effectively **unconfigured** in the deployed app — 1 role (`User`), 1 page grant (the start page), and the operator holds the administrator flag (administrators bypass page-role checks). Actor differentiation is **not modelled** in the app; persona differentiation must come from stakeholder input. [from admin.db]

### Full capability surface (single operator)

> Every inventory page/task is available to the single operator:
- Roles
- Users
- CostCentres
- BusinessUnits
- Beneficiaries
- Banks
- BankAccounts
- BankPaymentSetup
- Department
- PaymentReason
- PaymentEnquiries
- PaymentDetails
- PaymentSetup
- DraftManualPaymentCapture
- TransactionCoding
- PaymentsDetails
- BeneficiaryDetails
- AttachmentsAndNotes
- Review
- ApprovalLevels
- UserApprovalLevels
- ApprovalLevelRules

## Tier-A — permission model (beyond admin.db)

> For richer apps the real authorization model lives in the `.sapz Setting` table (approver/role configuration) and in API `Role` / `ApprovalLevel` / `*Permission` data entities — not the (often trivial single-User) admin.db page-role matrix above.

- RBAC data entities (roles / approval-levels / permissions modelled as data): `ApprovalLevel`, `ApprovalLevelAmount`, `ApprovalLevelRule`, `Role`, `UserApprovalLevel`, `UserApprovalLevelAmount` [from data-model]

## Tier-B — actor candidates (advisory; interpretive review gate)

- Distinct task clusters — `capture`, `reporting` — suggest more than one operator role even under a single RBAC role (a capture operator and an approver need not be the same person). `[AI-SUGGESTED]`
> Toast/dialog notifications target the current operator only and are **not** an actor signal.

## Tier-B — actor / persona scaffold (interpretive review gate)

> Grounded skeleton per candidate actor (task-clusters, surfaces, notifications). Persona fields the `.sapz` cannot ground are left as explicit gap prompts — authoring a name/goal/motivation here would fabricate. Skeleton rendered, flesh refused. `[AI-SUGGESTED]`

### Actor candidate: Operator A (capture)  `[AI-SUGGESTED: actor candidate]`
- Task clusters: capture
- Surfaces touched: ApprovalLevels, AttachmentsAndNotes, DraftManualPaymentCapture, Review, Users
- Notifications sent/received: "'Are you sure you want to delete the approval level ?\n\n'+ {0} +'\n'+ {1} +'\n'+ {2} +'\n'" (dialog); "'Are you sure you want to delete the approval level amount ?\n\n'+ {0}" (dialog); "'Are you sure you want to delete the attachement document ?\n\n ' + {0}" (dialog); "'Are you sure you want to edit this note?\n\n ' + {0}" (dialog); "'Are you sure you want to add this Note ?\n\n ' + {0}" (dialog); "'Are you sure you want to cancel the payment capture ?'" (dialog)
- name: `[AI-SUGGESTED: blocking]`
- goal: `[AI-SUGGESTED: blocking]`
- motivation: `[AI-SUGGESTED: blocking]`
- pain-points: `[AI-SUGGESTED: blocking]`
- success-metric: `[AI-SUGGESTED: blocking]`

### Actor candidate: Operator B (reporting)  `[AI-SUGGESTED: actor candidate]`
- Task clusters: reporting
- Surfaces touched: PaymentEnquiries
- Notifications sent/received: —
- name: `[AI-SUGGESTED: blocking]`
- goal: `[AI-SUGGESTED: blocking]`
- motivation: `[AI-SUGGESTED: blocking]`
- pain-points: `[AI-SUGGESTED: blocking]`
- success-metric: `[AI-SUGGESTED: blocking]`

## Tier-A — user population (counts only; identities not extracted)

- 1 user account(s), 1 with the administrator flag; individual identities (name / email) not extracted — PII. [from admin.db: Users]
