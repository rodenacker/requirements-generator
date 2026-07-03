---
stadium_asset: data-model
app: PaymentsApp
file_guid: be54c8c9-dc03-43d5-bc2b-fba14e07f360
designer_version: 6.14.3378.13771
selected_package: 2211275f-1cb9-495c-91cf-4ff48dc4c142.sapz
extracted_from: C:\Stadium 6 Web Apps\be54c8c9-dc03-43d5-bc2b-fba14e07f360
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Data model — PaymentsApp

> Entities + fields reconciled across SQL queries/views, stored procedures and web-service calls (union by name). Every field carries a `[from …]` locator naming its exact source.

## Tier-A — entities & fields

### ApprovalLevelAmountReadList  ·  sources: web-service  ·  operations: SELECT
- `ApprovalLevelAmountReadList.ApprovalLevelAmounts` [from web-service: GET /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]
- `ApprovalLevelAmountReadList.ApprovalLevelAmounts.ApprovalLevelId` [from web-service: GET /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]
- `ApprovalLevelAmountReadList.ApprovalLevelAmounts.MaxApprovalAmount` [from web-service: GET /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]
> related shapes: `UserApprovalLevelAmountReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ApprovalLevelReadList  ·  sources: web-service  ·  operations: SELECT
- `ApprovalLevelReadList.ApprovalLevels` [from web-service: GET /v1/approval-levels]  _(+1 more)_
- `ApprovalLevelReadList.ApprovalLevels.BusinessUnit` [from web-service: GET /v1/approval-levels]
- `ApprovalLevelReadList.ApprovalLevels.BusinessUnitDepartmentId` [from web-service: GET /v1/approval-levels]
- `ApprovalLevelReadList.ApprovalLevels.BusinessUnitId` [from web-service: GET /v1/approval-levels]
- `ApprovalLevelReadList.ApprovalLevels.Department` [from web-service: GET /v1/approval-levels]
- `ApprovalLevelReadList.ApprovalLevels.DepartmentId` [from web-service: GET /v1/approval-levels]
- `ApprovalLevelReadList.ApprovalLevels.TransactionType` [from web-service: GET /v1/approval-levels]
- `ApprovalLevelReadList.ApprovalLevels.TransactionTypeId` [from web-service: GET /v1/approval-levels]
> related shapes: `UserApprovalLevelReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ApprovalLevelRuleRead  ·  sources: web-service  ·  operations: UPDATE
- `ApprovalLevelRuleRead.ApprovalAmount` [from web-service: PUT /v1/approval-level-rules]
- `ApprovalLevelRuleRead.ApprovalLevelId` [from web-service: PUT /v1/approval-level-rules]
- `ApprovalLevelRuleRead.BankReleaseApproval` [from web-service: PUT /v1/approval-level-rules]
- `ApprovalLevelRuleRead.ManagerialApproval` [from web-service: PUT /v1/approval-level-rules]
- `ApprovalLevelRuleRead.TreasuryApproval` [from web-service: PUT /v1/approval-level-rules]
> related shapes: `ApprovalLevelRuleReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ApprovalLevelRuleReadList  ·  sources: web-service  ·  operations: SELECT
- `ApprovalLevelRuleReadList.ApprovalLevelRules` [from web-service: GET /v1/approval-level-rules/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]
> related shapes: `ApprovalLevelRuleRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ApprovalLevelWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `ApprovalLevelWrite.BusinessUnitId` [from web-service: POST /v1/approval-levels/]  _(+1 more)_
- `ApprovalLevelWrite.DepartmentId` [from web-service: POST /v1/approval-levels/]  _(+1 more)_
- `ApprovalLevelWrite.MaxApprovalAmounts` [from web-service: POST /v1/approval-levels/]  _(+1 more)_
- `ApprovalLevelWrite.TransactionTypeId` [from web-service: POST /v1/approval-levels/]  _(+1 more)_
> related shapes: `UserApprovalLevelWrite` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankAccountRead  ·  sources: web-service  ·  operations: SELECT
- `BankAccountRead.AccountName` [from web-service: GET /v1/bank-accounts/{Id}]
- `BankAccountRead.AccountNumber` [from web-service: GET /v1/bank-accounts/{Id}]
- `BankAccountRead.BankAccountTypeId` [from web-service: GET /v1/bank-accounts/{Id}]
- `BankAccountRead.BankAccountTypeName` [from web-service: GET /v1/bank-accounts/{Id}]
- `BankAccountRead.BankId` [from web-service: GET /v1/bank-accounts/{Id}]
- `BankAccountRead.BankName` [from web-service: GET /v1/bank-accounts/{Id}]
- `BankAccountRead.BusinessUnit` [from web-service: GET /v1/bank-accounts/{Id}]
- `BankAccountRead.BusinessUnitId` [from web-service: GET /v1/bank-accounts/{Id}]
- `BankAccountRead.Iban` [from web-service: GET /v1/bank-accounts/{Id}]
- `BankAccountRead.Id` [from web-service: GET /v1/bank-accounts/{Id}]
> related shapes: `BankAccountReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankAccountReadList  ·  sources: web-service  ·  operations: SELECT
- `BankAccountReadList.BankAccounts` [from web-service: GET /v1/bank-accounts]
> related shapes: `BankAccountRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankAccountTypeReadList  ·  sources: web-service  ·  operations: SELECT
- `BankAccountTypeReadList.BankAccountTypes` [from web-service: GET /v1/bank-account-types]

### BankAccountWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `BankAccountWrite.AccountName` [from web-service: POST /v1/bank-accounts]  _(+1 more)_
- `BankAccountWrite.AccountNumber` [from web-service: POST /v1/bank-accounts]  _(+1 more)_
- `BankAccountWrite.BankAccountTypeId` [from web-service: POST /v1/bank-accounts]  _(+1 more)_
- `BankAccountWrite.BankId` [from web-service: POST /v1/bank-accounts]  _(+1 more)_
- `BankAccountWrite.BusinessUnitId` [from web-service: POST /v1/bank-accounts]  _(+1 more)_
- `BankAccountWrite.Iban` [from web-service: POST /v1/bank-accounts]  _(+1 more)_

### BankPaymentMethodReadList  ·  sources: web-service  ·  operations: SELECT
- `BankPaymentMethodReadList.BankPaymentMethods` [from web-service: GET /v1/bank-payment-methods]

### BankPaymentSetupRead  ·  sources: web-service  ·  operations: SELECT
- `BankPaymentSetupRead.ApiEnabled` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.BankId` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.BankName` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.BankPaymentMethodId` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.BankPaymentMethodName` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.ChargeBearerId` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.ChargeBearerName` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.CutOffTime` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.Id` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.ServiceLevelCodeId` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.ServiceLevelCodeName` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.TransferMethodId` [from web-service: GET /v1/bank-payment-setups/{Id}]
- `BankPaymentSetupRead.TransferMethodName` [from web-service: GET /v1/bank-payment-setups/{Id}]
> related shapes: `BankPaymentSetupReadList`, `PaymentSetupRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankPaymentSetupReadList  ·  sources: web-service  ·  operations: SELECT
- `BankPaymentSetupReadList.BankPayments` [from web-service: GET /v1/bank-payment-setups]
> related shapes: `BankPaymentSetupRead`, `PaymentSetupRead`, `PaymentSetupReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankPaymentSetupWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `BankPaymentSetupWrite.ApiEnabled` [from web-service: POST /v1/bank-payment-setups]  _(+1 more)_
- `BankPaymentSetupWrite.BankId` [from web-service: POST /v1/bank-payment-setups]  _(+1 more)_
- `BankPaymentSetupWrite.BankPaymentMethodId` [from web-service: POST /v1/bank-payment-setups]  _(+1 more)_
- `BankPaymentSetupWrite.ChargeBearerId` [from web-service: POST /v1/bank-payment-setups]  _(+1 more)_
- `BankPaymentSetupWrite.CutOffTime` [from web-service: POST /v1/bank-payment-setups]  _(+1 more)_
- `BankPaymentSetupWrite.ServiceLevelCodeId` [from web-service: POST /v1/bank-payment-setups]  _(+1 more)_
- `BankPaymentSetupWrite.TransferMethodId` [from web-service: POST /v1/bank-payment-setups]  _(+1 more)_
> related shapes: `PaymentSetupWrite` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankRead  ·  sources: web-service  ·  operations: SELECT
- `BankRead.Id` [from web-service: GET /v1/banks/{Id}]
- `BankRead.Name` [from web-service: GET /v1/banks/{Id}]
- `BankRead.UniversalBranchCode` [from web-service: GET /v1/banks/{Id}]
- `BankRead.UniversalSwiftCode` [from web-service: GET /v1/banks/{Id}]
> related shapes: `BankReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankReadList  ·  sources: web-service  ·  operations: SELECT
- `BankReadList.Banks` [from web-service: GET /v1/banks]
> related shapes: `BankRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `BankWrite.Name` [from web-service: POST /v1/banks]  _(+1 more)_
- `BankWrite.UniversalBranchCode` [from web-service: POST /v1/banks]  _(+1 more)_
- `BankWrite.UniversalSwiftCode` [from web-service: POST /v1/banks]  _(+1 more)_

### BeneficiaryRead  ·  sources: web-service  ·  operations: SELECT
- `BeneficiaryRead.AccountName` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.AccountNumber` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BankAccountTypeId` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BankAccountTypeName` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BankId` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BankName` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BusinessUnit` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BusinessUnitDepartments` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BusinessUnitDepartments.BusinessUnitDepartmentId` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BusinessUnitDepartments.DepartmentId` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BusinessUnitDepartments.DepartmentName` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BusinessUnitDepartmentString` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.BusinessUnitId` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.Iban` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.Id` [from web-service: GET /v1/beneficiaries/{Id}]
- `BeneficiaryRead.Name` [from web-service: GET /v1/beneficiaries/{Id}]
> related shapes: `BeneficiaryReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BeneficiaryReadList  ·  sources: web-service  ·  operations: SELECT
- `BeneficiaryReadList.Beneficiaries` [from web-service: GET /v1/beneficiaries]
> related shapes: `BeneficiaryRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BeneficiaryWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `BeneficiaryWrite.AccountName` [from web-service: POST /v1/beneficiaries]  _(+1 more)_
- `BeneficiaryWrite.AccountNumber` [from web-service: POST /v1/beneficiaries]  _(+1 more)_
- `BeneficiaryWrite.BankAccountTypeId` [from web-service: POST /v1/beneficiaries]  _(+1 more)_
- `BeneficiaryWrite.BankId` [from web-service: POST /v1/beneficiaries]  _(+1 more)_
- `BeneficiaryWrite.BusinessUnitDepartments` [from web-service: POST /v1/beneficiaries]  _(+1 more)_
- `BeneficiaryWrite.BusinessUnitDepartments.BusinessUnitDepartmentId` [from web-service: POST /v1/beneficiaries]  _(+1 more)_
- `BeneficiaryWrite.BusinessUnitDepartments.DepartmentId` [from web-service: POST /v1/beneficiaries]  _(+1 more)_
- `BeneficiaryWrite.BusinessUnitDepartments.DepartmentName` [from web-service: POST /v1/beneficiaries]  _(+1 more)_
- `BeneficiaryWrite.BusinessUnitId` [from web-service: POST /v1/beneficiaries]  _(+1 more)_
- `BeneficiaryWrite.Iban` [from web-service: POST /v1/beneficiaries]  _(+1 more)_
- `BeneficiaryWrite.Name` [from web-service: POST /v1/beneficiaries]  _(+1 more)_

### BusinessUnitDepartmentReadList  ·  sources: web-service  ·  operations: SELECT
- `BusinessUnitDepartmentReadList.BusinessUnitDepartments` [from web-service: GET /v1/business-unit-departments]
- `BusinessUnitDepartmentReadList.BusinessUnitDepartments.BusinessUnitDepartmentId` [from web-service: GET /v1/business-unit-departments]
- `BusinessUnitDepartmentReadList.BusinessUnitDepartments.DepartmentId` [from web-service: GET /v1/business-unit-departments]
- `BusinessUnitDepartmentReadList.BusinessUnitDepartments.DepartmentName` [from web-service: GET /v1/business-unit-departments]
> related shapes: `DepartmentRead`, `DepartmentReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BusinessUnitRead  ·  sources: web-service  ·  operations: SELECT
- `BusinessUnitRead.Code` [from web-service: GET /v1/business-units/{Id}]
- `BusinessUnitRead.Departments` [from web-service: GET /v1/business-units/{Id}]
- `BusinessUnitRead.DepartmentString` [from web-service: GET /v1/business-units/{Id}]
- `BusinessUnitRead.Description` [from web-service: GET /v1/business-units/{Id}]
- `BusinessUnitRead.Id` [from web-service: GET /v1/business-units/{Id}]
- `BusinessUnitRead.Name` [from web-service: GET /v1/business-units/{Id}]
> related shapes: `BusinessUnitReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BusinessUnitReadList  ·  sources: web-service  ·  operations: SELECT
- `BusinessUnitReadList.BusinessUnits` [from web-service: GET /v1/business-units]
> related shapes: `BusinessUnitRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BusinessUnitWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `BusinessUnitWrite.Code` [from web-service: POST /v1/business-units]  _(+1 more)_
- `BusinessUnitWrite.Departments` [from web-service: POST /v1/business-units]  _(+1 more)_
- `BusinessUnitWrite.Departments.Description` [from web-service: POST /v1/business-units]  _(+1 more)_
- `BusinessUnitWrite.Departments.Id` [from web-service: POST /v1/business-units]  _(+1 more)_
- `BusinessUnitWrite.Departments.Name` [from web-service: POST /v1/business-units]  _(+1 more)_
- `BusinessUnitWrite.Description` [from web-service: POST /v1/business-units]  _(+1 more)_
- `BusinessUnitWrite.Name` [from web-service: POST /v1/business-units]  _(+1 more)_

### CostCentreRead  ·  sources: web-service  ·  operations: SELECT
- `CostCentreRead.BusinessUnit` [from web-service: GET /v1/cost-centres/{Id}]
- `CostCentreRead.BusinessUnitDepartments` [from web-service: GET /v1/cost-centres/{Id}]
- `CostCentreRead.BusinessUnitDepartments.BusinessUnitDepartmentId` [from web-service: GET /v1/cost-centres/{Id}]
- `CostCentreRead.BusinessUnitDepartments.DepartmentId` [from web-service: GET /v1/cost-centres/{Id}]
- `CostCentreRead.BusinessUnitDepartments.DepartmentName` [from web-service: GET /v1/cost-centres/{Id}]
- `CostCentreRead.BusinessUnitDepartmentString` [from web-service: GET /v1/cost-centres/{Id}]
- `CostCentreRead.BusinessUnitId` [from web-service: GET /v1/cost-centres/{Id}]
- `CostCentreRead.Description` [from web-service: GET /v1/cost-centres/{Id}]
- `CostCentreRead.Id` [from web-service: GET /v1/cost-centres/{Id}]
- `CostCentreRead.Name` [from web-service: GET /v1/cost-centres/{Id}]
> related shapes: `CostCentreReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### CostCentreReadList  ·  sources: web-service  ·  operations: SELECT
- `CostCentreReadList.CostCentres` [from web-service: GET /v1/cost-centres]
> related shapes: `CostCentreRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### CostCentreWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `CostCentreWrite.BusinessUnitDepartments` [from web-service: POST /v1/cost-centres]  _(+1 more)_
- `CostCentreWrite.BusinessUnitDepartments.BusinessUnitDepartmentId` [from web-service: POST /v1/cost-centres]  _(+1 more)_
- `CostCentreWrite.BusinessUnitDepartments.DepartmentId` [from web-service: POST /v1/cost-centres]  _(+1 more)_
- `CostCentreWrite.BusinessUnitDepartments.DepartmentName` [from web-service: POST /v1/cost-centres]  _(+1 more)_
- `CostCentreWrite.BusinessUnitId` [from web-service: POST /v1/cost-centres]  _(+1 more)_
- `CostCentreWrite.Description` [from web-service: POST /v1/cost-centres]  _(+1 more)_
- `CostCentreWrite.Name` [from web-service: POST /v1/cost-centres]  _(+1 more)_

### DefaultResponse  ·  sources: web-service  ·  operations: DELETE, INSERT
- `DefaultResponse.Id` [from web-service: DELETE /v1/beneficiaries/{Id}]  _(+16 more)_
- `DefaultResponse.Messages` [from web-service: DELETE /v1/beneficiaries/{Id}]  _(+16 more)_
- `DefaultResponse.MessageType` [from web-service: DELETE /v1/beneficiaries/{Id}]  _(+16 more)_

### DepartmentRead  ·  sources: web-service  ·  operations: SELECT
- `DepartmentRead.Description` [from web-service: GET /v1/departments/{Id}]
- `DepartmentRead.Id` [from web-service: GET /v1/departments/{Id}]
- `DepartmentRead.Name` [from web-service: GET /v1/departments/{Id}]
> related shapes: `BusinessUnitDepartmentReadList`, `DepartmentReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### DepartmentReadList  ·  sources: web-service  ·  operations: SELECT
- `DepartmentReadList.Departments` [from web-service: GET /v1/departments]
> related shapes: `BusinessUnitDepartmentReadList`, `DepartmentRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### DepartmentWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `DepartmentWrite.Description` [from web-service: POST /v1/departments]  _(+1 more)_
- `DepartmentWrite.Name` [from web-service: POST /v1/departments]  _(+1 more)_

### LookupDataReadList  ·  sources: web-service  ·  operations: SELECT
- `LookupDataReadList.LookupDatas` [from web-service: GET /v1/lookup-datas/{LookupId}]

### PaymentDetailAuditLogReadList  ·  sources: web-service  ·  operations: SELECT
- `PaymentDetailAuditLogReadList.PaymentDetailAuditLogs` [from web-service: GET /v1/payment-detail-audit-logs]

### PaymentReasonRead  ·  sources: web-service  ·  operations: SELECT
- `PaymentReasonRead.Code` [from web-service: GET /v1/payment-reasons/{Id}]
- `PaymentReasonRead.Description` [from web-service: GET /v1/payment-reasons/{Id}]
- `PaymentReasonRead.Id` [from web-service: GET /v1/payment-reasons/{Id}]
- `PaymentReasonRead.Name` [from web-service: GET /v1/payment-reasons/{Id}]
> related shapes: `PaymentReasonReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### PaymentReasonReadList  ·  sources: web-service  ·  operations: SELECT
- `PaymentReasonReadList.PaymentReasons` [from web-service: GET /v1/payment-reasons]
> related shapes: `PaymentReasonRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### PaymentReasonWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `PaymentReasonWrite.Code` [from web-service: POST /v1/payment-reasons]  _(+1 more)_
- `PaymentReasonWrite.Description` [from web-service: POST /v1/payment-reasons]  _(+1 more)_
- `PaymentReasonWrite.Name` [from web-service: POST /v1/payment-reasons]  _(+1 more)_

### PaymentSetupRead  ·  sources: web-service  ·  operations: SELECT
- `PaymentSetupRead.BankAccount` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.BankAccountId` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.BankAccountNumber` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.BankPaymentMethodId` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.BusinessUnit` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.BusinessUnitDepartmentId` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.BusinessUnitId` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.Department` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.DepartmentId` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.PaymentMethod` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.PaymentReason` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.PaymentReasonId` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.PaymentSetupId` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.TransactionType` [from web-service: GET /v1/payment-setups/{Id}]
- `PaymentSetupRead.TransactionTypeId` [from web-service: GET /v1/payment-setups/{Id}]
> related shapes: `BankPaymentSetupRead`, `BankPaymentSetupReadList`, `PaymentSetupReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### PaymentSetupReadList  ·  sources: web-service  ·  operations: SELECT
- `PaymentSetupReadList.PaymentSetups` [from web-service: GET /v1/payment-setups]  _(+1 more)_
> related shapes: `BankPaymentSetupReadList`, `PaymentSetupRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### PaymentSetupWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `PaymentSetupWrite.BankAccountId` [from web-service: POST /v1/payment-setups]  _(+1 more)_
- `PaymentSetupWrite.BankPaymentMethodId` [from web-service: POST /v1/payment-setups]  _(+1 more)_
- `PaymentSetupWrite.BusinessUnitDepartmentId` [from web-service: POST /v1/payment-setups]  _(+1 more)_
- `PaymentSetupWrite.PaymentReasonId` [from web-service: POST /v1/payment-setups]  _(+1 more)_
- `PaymentSetupWrite.TransactionTypeId` [from web-service: POST /v1/payment-setups]  _(+1 more)_
> related shapes: `BankPaymentSetupWrite` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### RoleReadList  ·  sources: web-service  ·  operations: SELECT
- `RoleReadList.Roles` [from web-service: GET /v1/roles]

### TransactionNoteReadList  ·  sources: web-service  ·  operations: SELECT
- `TransactionNoteReadList.TransactionNotes` [from web-service: GET /v1/transaction-notes]

### TransactionNoteWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `TransactionNoteWrite.DateCreated` [from web-service: POST /v1/transaction-notes]  _(+1 more)_
- `TransactionNoteWrite.Note` [from web-service: POST /v1/transaction-notes]  _(+1 more)_
- `TransactionNoteWrite.StadiumUserUuid` [from web-service: POST /v1/transaction-notes]  _(+1 more)_
- `TransactionNoteWrite.TransactionId` [from web-service: POST /v1/transaction-notes]  _(+1 more)_

### TransactionRead  ·  sources: web-service  ·  operations: SELECT
- `TransactionRead.Amount` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BankAccount` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BankAccountId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BankAccountNumber` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BankPaymentMethod` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BankPaymentMethodId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BeneficiaryAccountNumber` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BeneficiaryId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BeneficiaryName` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BeneficiarySortCode` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BusinessUnit` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BusinessUnitDepartmentId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.BusinessUnitId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.CostCentre` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.Currency` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.CurrencyId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.DateCreated` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.Department` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.DepartmentId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.ExecutionDate` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.InstructionId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.PaymentReason` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.PaymentReasonId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.PaymentReference` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.ProcessInstanceId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.RequestedBy` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.Status` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.TrackingNumber` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.TransactionManualCaptureStep` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.TransactionManualCaptureStepId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.TransactionType` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.TransactionTypeId` [from web-service: GET /v1/transactions/{Id}]
- `TransactionRead.UserId` [from web-service: GET /v1/transactions/{Id}]
> related shapes: `TransactionReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### TransactionReadList  ·  sources: web-service  ·  operations: SELECT
- `TransactionReadList.Transactions` [from web-service: GET /v1/transactions]  _(+2 more)_
- `TransactionReadList.Transactions.Amount` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BankAccount` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BankAccountId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BankAccountNumber` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BankPaymentMethod` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BankPaymentMethodId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BeneficiaryAccountNumber` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BeneficiaryId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BeneficiaryName` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BeneficiarySortCode` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BusinessUnit` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BusinessUnitDepartmentId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.BusinessUnitId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.CostCentre` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.Currency` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.CurrencyId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.DateCreated` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.Department` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.DepartmentId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.ExecutionDate` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.InstructionId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.PaymentReason` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.PaymentReasonId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.PaymentReference` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.ProcessInstanceId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.RequestedBy` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.Status` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.TrackingNumber` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.TransactionManualCaptureStep` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.TransactionManualCaptureStepId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.TransactionType` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.TransactionTypeId` [from web-service: GET /v1/transactions]
- `TransactionReadList.Transactions.UserId` [from web-service: GET /v1/transactions]
> related shapes: `TransactionRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### TransactionSupportingDocumentReadList  ·  sources: web-service  ·  operations: SELECT
- `TransactionSupportingDocumentReadList.TransactionSupportingDocuments` [from web-service: GET /v1/transaction-supporting-documents]

### TransactionSupportingDocumentWrite  ·  sources: web-service  ·  operations: INSERT
- `TransactionSupportingDocumentWrite.DateCreated` [from web-service: POST /v1/transaction-supporting-documents]
- `TransactionSupportingDocumentWrite.FileLocation` [from web-service: POST /v1/transaction-supporting-documents]
- `TransactionSupportingDocumentWrite.FileName` : String [from web-service: POST /v1/transaction-supporting-documents]
- `TransactionSupportingDocumentWrite.StadiumUserUuid` [from web-service: POST /v1/transaction-supporting-documents]
- `TransactionSupportingDocumentWrite.TransactionId` [from web-service: POST /v1/transaction-supporting-documents]

### TransactionTypeReadList  ·  sources: web-service  ·  operations: SELECT
- `TransactionTypeReadList.TransactionTypes` [from web-service: GET /v1/transaction-types]

### TransactionWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `TransactionWrite.Amount` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.BankAccountId` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.BankPaymentMethodId` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.BeneficiaryAccountNumber` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.BeneficiaryId` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.BeneficiaryName` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.BeneficiarySortCode` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.BusinessUnitDepartmentId` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.BusinessUnitId` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.CurrencyId` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.DateCreated` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.ExecutionDate` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.InstructionId` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.PaymentReasonId` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.PaymentReference` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.ProcessInstanceId` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.StadiumUserUuid` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.TransactionManualCaptureStepId` [from web-service: POST /v1/transactions]  _(+1 more)_
- `TransactionWrite.TransactionTypeId` [from web-service: POST /v1/transactions]  _(+1 more)_

### UserApprovalLevelAmountReadList  ·  sources: web-service  ·  operations: SELECT
- `UserApprovalLevelAmountReadList.UserApprovalLevelAmounts` [from web-service: GET /v1/user-approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]
> related shapes: `ApprovalLevelAmountReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserApprovalLevelReadList  ·  sources: web-service  ·  operations: SELECT
- `UserApprovalLevelReadList.UserApprovalLevels` [from web-service: GET /v1/user-approval-levels/{UserId}]
> related shapes: `ApprovalLevelReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserApprovalLevelWrite  ·  sources: web-service  ·  operations: INSERT
- `UserApprovalLevelWrite.ApprovalLevelId` [from web-service: POST /v1/user-approval-levels]
- `UserApprovalLevelWrite.UserId` [from web-service: POST /v1/user-approval-levels]
> related shapes: `ApprovalLevelWrite` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserRead  ·  sources: web-service  ·  operations: SELECT
- `UserRead.ApprovalLevelAssignStatus` [from web-service: GET /v1/users/{Id}]
- `UserRead.BusinessUnit` [from web-service: GET /v1/users/{Id}]
- `UserRead.BusinessUnitDepartments` [from web-service: GET /v1/users/{Id}]
- `UserRead.BusinessUnitDepartmentString` [from web-service: GET /v1/users/{Id}]
- `UserRead.BusinessUnitId` [from web-service: GET /v1/users/{Id}]
- `UserRead.Email` [from web-service: GET /v1/users/{Id}]
- `UserRead.FirstName` [from web-service: GET /v1/users/{Id}]
- `UserRead.Id` [from web-service: GET /v1/users/{Id}]
- `UserRead.IsAdministrator` [from web-service: GET /v1/users/{Id}]
- `UserRead.LastChangedDate` [from web-service: GET /v1/users/{Id}]
- `UserRead.LastChangedUser` [from web-service: GET /v1/users/{Id}]
- `UserRead.LastName` [from web-service: GET /v1/users/{Id}]
- `UserRead.Roles` [from web-service: GET /v1/users/{Id}]
- `UserRead.RolesString` [from web-service: GET /v1/users/{Id}]
- `UserRead.StadiumUserId` [from web-service: GET /v1/users/{Id}]
> related shapes: `UserReadList` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserReadList  ·  sources: web-service  ·  operations: SELECT
- `UserReadList.Users` [from web-service: GET /v1/users]
- `UserReadList.Users.ApprovalLevelAssignStatus` [from web-service: GET /v1/users]
- `UserReadList.Users.BusinessUnit` [from web-service: GET /v1/users]
- `UserReadList.Users.BusinessUnitDepartments` [from web-service: GET /v1/users]
- `UserReadList.Users.BusinessUnitDepartmentString` [from web-service: GET /v1/users]
- `UserReadList.Users.BusinessUnitId` [from web-service: GET /v1/users]
- `UserReadList.Users.Email` [from web-service: GET /v1/users]
- `UserReadList.Users.FirstName` [from web-service: GET /v1/users]
- `UserReadList.Users.Id` [from web-service: GET /v1/users]
- `UserReadList.Users.IsAdministrator` [from web-service: GET /v1/users]
- `UserReadList.Users.LastChangedDate` [from web-service: GET /v1/users]
- `UserReadList.Users.LastChangedUser` [from web-service: GET /v1/users]
- `UserReadList.Users.LastName` [from web-service: GET /v1/users]
- `UserReadList.Users.Roles` [from web-service: GET /v1/users]
- `UserReadList.Users.RolesString` [from web-service: GET /v1/users]
- `UserReadList.Users.StadiumUserId` [from web-service: GET /v1/users]
> related shapes: `UserRead` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserWrite  ·  sources: web-service  ·  operations: INSERT, UPDATE
- `UserWrite.BusinessUnitDepartments` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.BusinessUnitDepartments.BusinessUnitDepartmentId` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.BusinessUnitDepartments.DepartmentName` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.BusinessUnitId` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.Email` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.FirstName` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.IsAdministrator` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.LastName` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.Password` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.Roles` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.Roles.Id` [from web-service: POST /v1/users]  _(+1 more)_
- `UserWrite.Roles.Name` [from web-service: POST /v1/users]  _(+1 more)_

> The design model defines 1378 internal data-type instances (control/result/parameter bindings); field types above are sourced from them where concrete. Full detail is in the forensic model.json.

## Tier-A — CRUD matrix

| Entity | SELECT | INSERT | UPDATE | DELETE | Evidence |
|---|:---:|:---:|:---:|:---:|---|
| ApprovalLevelAmountReadList | ✓ |  |  |  | web-service |
| ApprovalLevelReadList | ✓ |  |  |  | web-service |
| ApprovalLevelRuleRead |  |  | ✓ |  | web-service |
| ApprovalLevelRuleReadList | ✓ |  |  |  | web-service |
| ApprovalLevelWrite |  | ✓ | ✓ |  | web-service |
| BankAccountRead | ✓ |  |  |  | web-service |
| BankAccountReadList | ✓ |  |  |  | web-service |
| BankAccountTypeReadList | ✓ |  |  |  | web-service |
| BankAccountWrite |  | ✓ | ✓ |  | web-service |
| BankPaymentMethodReadList | ✓ |  |  |  | web-service |
| BankPaymentSetupRead | ✓ |  |  |  | web-service |
| BankPaymentSetupReadList | ✓ |  |  |  | web-service |
| BankPaymentSetupWrite |  | ✓ | ✓ |  | web-service |
| BankRead | ✓ |  |  |  | web-service |
| BankReadList | ✓ |  |  |  | web-service |
| BankWrite |  | ✓ | ✓ |  | web-service |
| BeneficiaryRead | ✓ |  |  |  | web-service |
| BeneficiaryReadList | ✓ |  |  |  | web-service |
| BeneficiaryWrite |  | ✓ | ✓ |  | web-service |
| BusinessUnitDepartmentReadList | ✓ |  |  |  | web-service |
| BusinessUnitRead | ✓ |  |  |  | web-service |
| BusinessUnitReadList | ✓ |  |  |  | web-service |
| BusinessUnitWrite |  | ✓ | ✓ |  | web-service |
| CostCentreRead | ✓ |  |  |  | web-service |
| CostCentreReadList | ✓ |  |  |  | web-service |
| CostCentreWrite |  | ✓ | ✓ |  | web-service |
| DefaultResponse |  | ✓ |  | ✓ | web-service |
| DepartmentRead | ✓ |  |  |  | web-service |
| DepartmentReadList | ✓ |  |  |  | web-service |
| DepartmentWrite |  | ✓ | ✓ |  | web-service |
| LookupDataReadList | ✓ |  |  |  | web-service |
| PaymentDetailAuditLogReadList | ✓ |  |  |  | web-service |
| PaymentReasonRead | ✓ |  |  |  | web-service |
| PaymentReasonReadList | ✓ |  |  |  | web-service |
| PaymentReasonWrite |  | ✓ | ✓ |  | web-service |
| PaymentSetupRead | ✓ |  |  |  | web-service |
| PaymentSetupReadList | ✓ |  |  |  | web-service |
| PaymentSetupWrite |  | ✓ | ✓ |  | web-service |
| RoleReadList | ✓ |  |  |  | web-service |
| TransactionNoteReadList | ✓ |  |  |  | web-service |
| TransactionNoteWrite |  | ✓ | ✓ |  | web-service |
| TransactionRead | ✓ |  |  |  | web-service |
| TransactionReadList | ✓ |  |  |  | web-service |
| TransactionSupportingDocumentReadList | ✓ |  |  |  | web-service |
| TransactionSupportingDocumentWrite |  | ✓ |  |  | web-service |
| TransactionTypeReadList | ✓ |  |  |  | web-service |
| TransactionWrite |  | ✓ | ✓ |  | web-service |
| UserApprovalLevelAmountReadList | ✓ |  |  |  | web-service |
| UserApprovalLevelReadList | ✓ |  |  |  | web-service |
| UserApprovalLevelWrite |  | ✓ |  |  | web-service |
| UserRead | ✓ |  |  |  | web-service |
| UserReadList | ✓ |  |  |  | web-service |
| UserWrite |  | ✓ | ✓ |  | web-service |

## Tier-B — entity lifecycle / states (inferred)
- Status-like fields suggest stateful entities: `ApprovalAmount`, `ApprovalLevelAmounts`, `ApprovalLevelAmounts.ApprovalLevelId`, `ApprovalLevelAmounts.MaxApprovalAmount`, `ApprovalLevelAssignStatus`, `ApprovalLevelId`, `ApprovalLevelRules`, `ApprovalLevels`, `ApprovalLevels.BusinessUnit`, `ApprovalLevels.BusinessUnitDepartmentId`, `ApprovalLevels.BusinessUnitId`, `ApprovalLevels.Department`, `ApprovalLevels.DepartmentId`, `ApprovalLevels.TransactionType`, `ApprovalLevels.TransactionTypeId`, `BankReleaseApproval`, `ManagerialApproval`, `MaxApprovalAmounts`, `Status`, `Transactions.Status`, `TreasuryApproval`, `UserApprovalLevelAmounts`, `UserApprovalLevels`, `Users.ApprovalLevelAssignStatus` `[AI-SUGGESTED]`
