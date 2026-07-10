---
stadium_asset: navigation
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
# Navigation & app shell — PaymentsApp

## Tier-A — templates (master pages)

- Template `DefaultTemplate` (default) [from design model]

## Tier-A — navigation edges (from NavigateToPage actions)

- Users → UserApprovalLevels / BusinessUnitId / Id
- PaymentEnquiries → PaymentDetails / TrackingNumber
- PaymentDetails → PaymentEnquiries
- PaymentDetails → DraftManualPaymentCapture
- DraftManualPaymentCapture → PaymentDetails / TrackingNumber
- DraftManualPaymentCapture → TransactionCoding / TrackingNumber
- DraftManualPaymentCapture → PaymentsDetails / TrackingNumber
- DraftManualPaymentCapture → BeneficiaryDetails / TrackingNumber
- DraftManualPaymentCapture → AttachmentsAndNotes / TrackingNumber
- DraftManualPaymentCapture → Review / TrackingNumber
- CancelLink.Click → TransactionCoding
- NextButton.Click → PaymentsDetails / Id
- NextButton.Click → PaymentsDetails / Id
- CancelLink.Click → TransactionCoding
- BackButton.Click → TransactionCoding / TrackingNumber
- NextButton.Click → BeneficiaryDetails / TrackingNumber
- CancelLink.Click → TransactionCoding
- CancelLink.Click → BeneficiaryDetails / TrackingNumber
- BackButton.Click → PaymentsDetails / TrackingNumber
- NextButton.Click → AttachmentsAndNotes / TrackingNumber
- NextButton.Click → AttachmentsAndNotes / TrackingNumber
- CancelLink.Click → TransactionCoding
- CancelLink.Click → AttachmentsAndNotes / TrackingNumber
- AttachmentsAndNotes → AttachmentsAndNotes / TrackingNumber
- AttachmentsAndNotes → TransactionCoding
- AttachmentsAndNotes → AttachmentsAndNotes / TrackingNumber
- BackButton.Click → BeneficiaryDetails / TrackingNumber
- NextButton.Click → Review / TrackingNumber
- BackButton.Click → AttachmentsAndNotes / TrackingNumber
- Review → TransactionCoding
- UserApprovalLevels → Users

## Tier-A — navigation reachability

- Coverage: **10 of 22** inventory pages are reachable via a captured `NavigateToPage` action. [from design model + administration.db]
- Additionally reachable via a declared client route (not on the captured `.sapz` walk): `Roles`, `CostCentres`, `BusinessUnits`, `Beneficiaries`, `Banks`, `BankAccounts`, `BankPaymentSetup`, `Department`, `PaymentReason`, `PaymentSetup`, `ApprovalLevels`, `ApprovalLevelRules` [from rendered routes]

## Tier-B — reachability caveat (advisory)
- Any remaining unreached page (absent from the captured `.sapz` walk AND from `page-routes.js`) is typically reached by JS-computed navigation (`jsGETCurrentURl` / custom JS) or is entry-only, so the captured nav graph is a floor, not the complete journey map. Route-declared pages above close most of this gap. `[AI-SUGGESTED]`

## Tier-B — candidate cross-surface journeys (advisory; interpretive review gate)

> A journey joins nav edges (0c) with the affordance/gesture that triggers each hop (0e/0g) and the actor that performs it (0h). The **edges, gestures and page kinds are Tier-A facts**; the claim that a chain **is one** end-to-end task is a **Tier-B** reading. JS-computed nav gaps are shown as explicit breaks, never bridged. `[AI-SUGGESTED]`

- `PaymentEnquiries` _(reporting)_ —[clicks]→ `PaymentDetails` _(detail)_ —[clicks]→ `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `AttachmentsAndNotes` _(capture)_ —[clicks "Cancel"]→ `TransactionCoding` _(entity-maintenance)_
- `PaymentEnquiries` _(reporting)_ —[clicks]→ `PaymentDetails` _(detail)_ —[clicks]→ `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `Review` _(capture)_ —[clicks "Submit"]→ `TransactionCoding` _(entity-maintenance)_
- `PaymentEnquiries` _(reporting)_ —[clicks]→ `PaymentDetails` _(detail)_ —[clicks]→ `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `BeneficiaryDetails` _(detail)_
- `PaymentEnquiries` _(reporting)_ —[clicks]→ `PaymentDetails` _(detail)_ —[clicks]→ `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `PaymentsDetails` _(detail)_
- `PaymentEnquiries` _(reporting)_ —[clicks]→ `PaymentDetails` _(detail)_ —[clicks]→ `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `TransactionCoding` _(entity-maintenance)_
- `PaymentDetails` _(detail)_ —[clicks]→ `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `AttachmentsAndNotes` _(capture)_ —[clicks "Cancel"]→ `TransactionCoding` _(entity-maintenance)_
- `PaymentDetails` _(detail)_ —[clicks]→ `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `Review` _(capture)_ —[clicks "Submit"]→ `TransactionCoding` _(entity-maintenance)_
- `PaymentDetails` _(detail)_ —[clicks]→ `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `BeneficiaryDetails` _(detail)_
- `PaymentDetails` _(detail)_ —[clicks]→ `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `PaymentsDetails` _(detail)_
- `PaymentDetails` _(detail)_ —[clicks]→ `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `TransactionCoding` _(entity-maintenance)_
- `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `AttachmentsAndNotes` _(capture)_ —[clicks "Cancel"]→ `TransactionCoding` _(entity-maintenance)_
- `DraftManualPaymentCapture` _(capture)_ —[clicks]→ `PaymentDetails` _(detail)_ —[clicks]→ `PaymentEnquiries` _(reporting)_
- **JS-nav gaps** — interactive pages with no captured inbound edge (reached via JS-computed nav): `ApprovalLevels` `[gap: JS-computed nav]`

## Tier-B — affordances (advisory)
- data grids (search/sort/export likely); file download/export; toast notifications; confirmation dialogs
