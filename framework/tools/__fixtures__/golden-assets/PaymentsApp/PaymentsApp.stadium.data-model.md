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

> Entities + fields reconciled across SQL queries/views, stored procedures, web-service calls and the rendered `types.js` FE↔API contract (union by name). Every field carries a `[from …]` locator naming its exact source; `[from rendered types]` fields carry a per-field authority (editable / read-only / action-input — Tier-B, read from the rendered variant).

## Tier-A — entities & fields

### ApprovalLevel  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `ApprovalLevel.ApprovalLevels` [from web-service: GET /v1/approval-levels]  _(+1 more)_
- `ApprovalLevel.ApprovalLevels.BusinessUnit` [from web-service: GET /v1/approval-levels]
- `ApprovalLevel.ApprovalLevels.BusinessUnitDepartmentId` [from web-service: GET /v1/approval-levels]
- `ApprovalLevel.ApprovalLevels.BusinessUnitId` [from web-service: GET /v1/approval-levels]
- `ApprovalLevel.ApprovalLevels.Department` [from web-service: GET /v1/approval-levels]
- `ApprovalLevel.ApprovalLevels.DepartmentId` [from web-service: GET /v1/approval-levels]
- `ApprovalLevel.ApprovalLevels.TransactionType` [from web-service: GET /v1/approval-levels]
- `ApprovalLevel.ApprovalLevels.TransactionTypeId` [from web-service: GET /v1/approval-levels]
- `ApprovalLevel.BusinessUnit` · read-only [from rendered types]
- `ApprovalLevel.BusinessUnitDepartmentId` · read-only [from rendered types]
- `ApprovalLevel.BusinessUnitId` · editable [from rendered types]  _(+2 more)_
- `ApprovalLevel.Department` · read-only [from rendered types]
- `ApprovalLevel.DepartmentId` · editable [from rendered types]  _(+2 more)_
- `ApprovalLevel.Id` [from web-service: DELETE /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]  _(+1 more)_
- `ApprovalLevel.MaxApprovalAmounts` · editable [from rendered types]  _(+2 more)_
- `ApprovalLevel.Messages` [from web-service: DELETE /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]  _(+1 more)_
- `ApprovalLevel.MessageType` [from web-service: DELETE /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]  _(+1 more)_
- `ApprovalLevel.TransactionType` · read-only [from rendered types]
- `ApprovalLevel.TransactionTypeId` · editable [from rendered types]  _(+2 more)_
> related shapes: `ApprovalLevelAmount`, `ApprovalLevelRule`, `UserApprovalLevel`, `UserApprovalLevelAmount` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ApprovalLevelAmount  ·  sources: rendered-types, web-service  ·  operations: SELECT
- `ApprovalLevelAmount.ApprovalLevelAmounts` [from web-service: GET /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]
- `ApprovalLevelAmount.ApprovalLevelAmounts.ApprovalLevelId` [from web-service: GET /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]
- `ApprovalLevelAmount.ApprovalLevelAmounts.MaxApprovalAmount` [from web-service: GET /v1/approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]
- `ApprovalLevelAmount.ApprovalLevelId` · read-only [from rendered types]
- `ApprovalLevelAmount.MaxApprovalAmount` · read-only [from rendered types]
> related shapes: `ApprovalLevel`, `UserApprovalLevelAmount` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### ApprovalLevelRule  ·  sources: rendered-types, web-service  ·  operations: SELECT, UPDATE
- `ApprovalLevelRule.ApprovalAmount` · read-only [from rendered types]  _(+1 more)_
- `ApprovalLevelRule.ApprovalLevelId` · read-only [from rendered types]  _(+1 more)_
- `ApprovalLevelRule.ApprovalLevelRules` [from web-service: GET /v1/approval-level-rules/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]
- `ApprovalLevelRule.BankReleaseApproval` · read-only [from rendered types]  _(+1 more)_
- `ApprovalLevelRule.ManagerialApproval` · read-only [from rendered types]  _(+1 more)_
- `ApprovalLevelRule.TreasuryApproval` · read-only [from rendered types]  _(+1 more)_
> related shapes: `ApprovalLevel` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### Bank  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `Bank.Banks` [from web-service: GET /v1/banks]
- `Bank.Id` · read-only [from web-service: DELETE /v1/banks/{Id}]  _(+2 more)_
- `Bank.Messages` [from web-service: DELETE /v1/banks/{Id}]
- `Bank.MessageType` [from web-service: DELETE /v1/banks/{Id}]
- `Bank.Name` · editable [from rendered types]  _(+3 more)_
- `Bank.UniversalBranchCode` · editable [from rendered types]  _(+3 more)_
- `Bank.UniversalSwiftCode` · editable [from rendered types]  _(+3 more)_
> related shapes: `BankAccount`, `BankAccountType`, `BankPaymentMethod`, `BankPaymentSetup` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankAccount  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `BankAccount.AccountName` · editable [from rendered types]  _(+3 more)_
- `BankAccount.AccountNumber` · editable [from rendered types]  _(+3 more)_
- `BankAccount.BankAccounts` [from web-service: GET /v1/bank-accounts]
- `BankAccount.BankAccountTypeId` · editable [from rendered types]  _(+3 more)_
- `BankAccount.BankAccountTypeName` · read-only [from rendered types]  _(+1 more)_
- `BankAccount.BankId` · editable [from rendered types]  _(+3 more)_
- `BankAccount.BankName` · read-only [from rendered types]  _(+1 more)_
- `BankAccount.BusinessUnit` · read-only [from rendered types]  _(+1 more)_
- `BankAccount.BusinessUnitId` · editable [from rendered types]  _(+3 more)_
- `BankAccount.Iban` · editable [from rendered types]  _(+3 more)_
- `BankAccount.Id` · read-only [from web-service: DELETE /v1/bank-accounts/{Id}]  _(+2 more)_
- `BankAccount.Messages` [from web-service: DELETE /v1/bank-accounts/{Id}]
- `BankAccount.MessageType` [from web-service: DELETE /v1/bank-accounts/{Id}]
> related shapes: `Bank`, `BankAccountType` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankAccountType  ·  sources: rendered-types, web-service  ·  operations: SELECT
- `BankAccountType.BankAccountTypes` [from web-service: GET /v1/bank-account-types]
- `BankAccountType.Id` · read-only [from rendered types]
- `BankAccountType.Name` · read-only [from rendered types]
> related shapes: `Bank`, `BankAccount` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankPaymentMethod  ·  sources: rendered-types, web-service  ·  operations: SELECT
- `BankPaymentMethod.BankPaymentMethods` [from web-service: GET /v1/bank-payment-methods]
- `BankPaymentMethod.Description` · read-only [from rendered types]
- `BankPaymentMethod.Id` · read-only [from rendered types]
- `BankPaymentMethod.Name` · read-only [from rendered types]
> related shapes: `Bank` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BankPaymentSetup  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `BankPaymentSetup.ApiEnabled` · editable [from rendered types]  _(+3 more)_
- `BankPaymentSetup.BankId` · editable [from rendered types]  _(+3 more)_
- `BankPaymentSetup.BankName` · read-only [from rendered types]  _(+1 more)_
- `BankPaymentSetup.BankPaymentMethodId` · editable [from rendered types]  _(+3 more)_
- `BankPaymentSetup.BankPaymentMethodName` · read-only [from rendered types]  _(+1 more)_
- `BankPaymentSetup.BankPayments` [from web-service: GET /v1/bank-payment-setups]
- `BankPaymentSetup.ChargeBearerId` · editable [from rendered types]  _(+3 more)_
- `BankPaymentSetup.ChargeBearerName` · read-only [from rendered types]  _(+1 more)_
- `BankPaymentSetup.CutOffTime` · editable [from rendered types]  _(+3 more)_
- `BankPaymentSetup.Id` · read-only [from web-service: DELETE /v1/bank-payment-setups/{Id}]  _(+2 more)_
- `BankPaymentSetup.Messages` [from web-service: DELETE /v1/bank-payment-setups/{Id}]
- `BankPaymentSetup.MessageType` [from web-service: DELETE /v1/bank-payment-setups/{Id}]
- `BankPaymentSetup.ServiceLevelCodeId` · editable [from rendered types]  _(+3 more)_
- `BankPaymentSetup.ServiceLevelCodeName` · read-only [from rendered types]  _(+1 more)_
- `BankPaymentSetup.TransferMethodId` · editable [from rendered types]  _(+3 more)_
- `BankPaymentSetup.TransferMethodName` · read-only [from rendered types]  _(+1 more)_
> related shapes: `Bank`, `PaymentSetup` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### Beneficiary  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `Beneficiary.AccountName` · editable [from rendered types]  _(+3 more)_
- `Beneficiary.AccountNumber` · editable [from rendered types]  _(+3 more)_
- `Beneficiary.BankAccountTypeId` · editable [from rendered types]  _(+3 more)_
- `Beneficiary.BankAccountTypeName` · read-only [from rendered types]  _(+1 more)_
- `Beneficiary.BankId` · editable [from rendered types]  _(+3 more)_
- `Beneficiary.BankName` · read-only [from rendered types]  _(+1 more)_
- `Beneficiary.Beneficiaries` [from web-service: GET /v1/beneficiaries]
- `Beneficiary.BusinessUnit` · read-only [from rendered types]  _(+1 more)_
- `Beneficiary.BusinessUnitDepartments` · editable [from rendered types]  _(+3 more)_
- `Beneficiary.BusinessUnitDepartments.BusinessUnitDepartmentId` [from web-service: POST /v1/beneficiaries]  _(+2 more)_
- `Beneficiary.BusinessUnitDepartments.DepartmentId` [from web-service: POST /v1/beneficiaries]  _(+2 more)_
- `Beneficiary.BusinessUnitDepartments.DepartmentName` [from web-service: POST /v1/beneficiaries]  _(+2 more)_
- `Beneficiary.BusinessUnitDepartmentString` · read-only [from rendered types]  _(+1 more)_
- `Beneficiary.BusinessUnitId` · editable [from rendered types]  _(+3 more)_
- `Beneficiary.Iban` · editable [from rendered types]  _(+3 more)_
- `Beneficiary.Id` · read-only [from web-service: DELETE /v1/beneficiaries/{Id}]  _(+2 more)_
- `Beneficiary.Messages` [from web-service: DELETE /v1/beneficiaries/{Id}]
- `Beneficiary.MessageType` [from web-service: DELETE /v1/beneficiaries/{Id}]
- `Beneficiary.Name` · editable [from rendered types]  _(+3 more)_
  - relation: `Beneficiary.BusinessUnitDepartments` → `BusinessUnitDepartment[]` (nested type) [from rendered types]

### BusinessUnit  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `BusinessUnit.BusinessUnits` [from web-service: GET /v1/business-units]
- `BusinessUnit.Code` · editable [from rendered types]  _(+3 more)_
- `BusinessUnit.Departments` · editable [from rendered types]  _(+3 more)_
- `BusinessUnit.Departments.Description` [from web-service: POST /v1/business-units]  _(+1 more)_
- `BusinessUnit.Departments.Id` [from web-service: POST /v1/business-units]  _(+1 more)_
- `BusinessUnit.Departments.Name` [from web-service: POST /v1/business-units]  _(+1 more)_
- `BusinessUnit.DepartmentString` · read-only [from rendered types]  _(+1 more)_
- `BusinessUnit.Description` · editable [from rendered types]  _(+3 more)_
- `BusinessUnit.Id` · read-only [from web-service: DELETE /v1/business-units/{Id}]  _(+2 more)_
- `BusinessUnit.Messages` [from web-service: DELETE /v1/business-units/{Id}]
- `BusinessUnit.MessageType` [from web-service: DELETE /v1/business-units/{Id}]
- `BusinessUnit.Name` · editable [from rendered types]  _(+3 more)_
  - relation: `BusinessUnit.Departments` → `Department[]` (nested type) [from rendered types]
> related shapes: `BusinessUnitDepartment` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### BusinessUnitDepartment  ·  sources: rendered-types, web-service  ·  operations: SELECT
- `BusinessUnitDepartment.BusinessUnitDepartmentId` · read-only [from rendered types]
- `BusinessUnitDepartment.BusinessUnitDepartments` [from web-service: GET /v1/business-unit-departments]
- `BusinessUnitDepartment.BusinessUnitDepartments.BusinessUnitDepartmentId` [from web-service: GET /v1/business-unit-departments]
- `BusinessUnitDepartment.BusinessUnitDepartments.DepartmentId` [from web-service: GET /v1/business-unit-departments]
- `BusinessUnitDepartment.BusinessUnitDepartments.DepartmentName` [from web-service: GET /v1/business-unit-departments]
- `BusinessUnitDepartment.DepartmentId` · read-only [from rendered types]
- `BusinessUnitDepartment.DepartmentName` · read-only [from rendered types]
> related shapes: `BusinessUnit`, `Department` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### CostCentre  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `CostCentre.BusinessUnit` · read-only [from rendered types]  _(+1 more)_
- `CostCentre.BusinessUnitDepartments` · editable [from rendered types]  _(+3 more)_
- `CostCentre.BusinessUnitDepartments.BusinessUnitDepartmentId` [from web-service: POST /v1/cost-centres]  _(+2 more)_
- `CostCentre.BusinessUnitDepartments.DepartmentId` [from web-service: POST /v1/cost-centres]  _(+2 more)_
- `CostCentre.BusinessUnitDepartments.DepartmentName` [from web-service: POST /v1/cost-centres]  _(+2 more)_
- `CostCentre.BusinessUnitDepartmentString` · read-only [from rendered types]  _(+1 more)_
- `CostCentre.BusinessUnitId` · editable [from rendered types]  _(+3 more)_
- `CostCentre.CostCentres` [from web-service: GET /v1/cost-centres]
- `CostCentre.Description` · editable [from rendered types]  _(+3 more)_
- `CostCentre.Id` · read-only [from web-service: DELETE /v1/cost-centres/{Id}]  _(+2 more)_
- `CostCentre.Messages` [from web-service: DELETE /v1/cost-centres/{Id}]
- `CostCentre.MessageType` [from web-service: DELETE /v1/cost-centres/{Id}]
- `CostCentre.Name` · editable [from rendered types]  _(+3 more)_
  - relation: `CostCentre.BusinessUnitDepartments` → `BusinessUnitDepartment[]` (nested type) [from rendered types]

### Department  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `Department.Departments` [from web-service: GET /v1/departments]
- `Department.Description` · editable [from rendered types]  _(+3 more)_
- `Department.Id` · read-only [from web-service: DELETE /v1/departments/{Id}]  _(+2 more)_
- `Department.Messages` [from web-service: DELETE /v1/departments/{Id}]
- `Department.MessageType` [from web-service: DELETE /v1/departments/{Id}]
- `Department.Name` · editable [from rendered types]  _(+3 more)_
> related shapes: `BusinessUnitDepartment` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### LookupData  ·  sources: rendered-types, web-service  ·  operations: SELECT
- `LookupData.Description` · read-only [from rendered types]
- `LookupData.Id` · read-only [from rendered types]
- `LookupData.LookupDatas` [from web-service: GET /v1/lookup-datas/{LookupId}]
- `LookupData.LookupId` · read-only [from rendered types]
- `LookupData.Value` : String · read-only [from rendered types]

### MaxApprovalAmount  ·  sources: rendered-types  ·  operations: —
- `MaxApprovalAmount.Amount` · read-only [from rendered types]
- `MaxApprovalAmount.Level` · read-only [from rendered types]

### PaymentDetailAuditLog  ·  sources: rendered-types, web-service  ·  operations: SELECT
- `PaymentDetailAuditLog.ActivityID` · read-only [from rendered types]
- `PaymentDetailAuditLog.Data` · read-only [from rendered types]
- `PaymentDetailAuditLog.EventName` · read-only [from rendered types]
- `PaymentDetailAuditLog.ID` · read-only [from rendered types]
- `PaymentDetailAuditLog.Message` · read-only [from rendered types]
- `PaymentDetailAuditLog.PaymentDetailAuditLogs` [from web-service: GET /v1/payment-detail-audit-logs]
- `PaymentDetailAuditLog.ProcessInstanceID` · read-only [from rendered types]
- `PaymentDetailAuditLog.Source` · read-only [from rendered types]
- `PaymentDetailAuditLog.Timestamp` · read-only [from rendered types]
> related shapes: `PaymentDetailAuditLogRead_Data` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### PaymentDetailAuditLogRead_Data  ·  sources: rendered-types  ·  operations: —
- `PaymentDetailAuditLogRead_Data.ActivityName` · read-only [from rendered types]
- `PaymentDetailAuditLogRead_Data.ProcessDefinitionName` · read-only [from rendered types]
> related shapes: `PaymentDetailAuditLog` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### PaymentReason  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `PaymentReason.Code` · editable [from rendered types]  _(+3 more)_
- `PaymentReason.Description` · editable [from rendered types]  _(+3 more)_
- `PaymentReason.Id` · read-only [from web-service: DELETE /v1/payment-reasons/{Id}]  _(+2 more)_
- `PaymentReason.Messages` [from web-service: DELETE /v1/payment-reasons/{Id}]
- `PaymentReason.MessageType` [from web-service: DELETE /v1/payment-reasons/{Id}]
- `PaymentReason.Name` · editable [from rendered types]  _(+3 more)_
- `PaymentReason.PaymentReasons` [from web-service: GET /v1/payment-reasons]

### PaymentSetup  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `PaymentSetup.BankAccount` · read-only [from rendered types]  _(+1 more)_
- `PaymentSetup.BankAccountId` · editable [from rendered types]  _(+3 more)_
- `PaymentSetup.BankAccountNumber` · read-only [from rendered types]  _(+1 more)_
- `PaymentSetup.BankPaymentMethodId` · editable [from rendered types]  _(+3 more)_
- `PaymentSetup.BusinessUnit` · read-only [from rendered types]  _(+1 more)_
- `PaymentSetup.BusinessUnitDepartmentId` · editable [from rendered types]  _(+3 more)_
- `PaymentSetup.BusinessUnitId` · read-only [from rendered types]  _(+1 more)_
- `PaymentSetup.Department` · read-only [from rendered types]  _(+1 more)_
- `PaymentSetup.DepartmentId` · read-only [from rendered types]  _(+1 more)_
- `PaymentSetup.Id` [from web-service: DELETE /v1/payment-setups/{Id}]
- `PaymentSetup.Messages` [from web-service: DELETE /v1/payment-setups/{Id}]
- `PaymentSetup.MessageType` [from web-service: DELETE /v1/payment-setups/{Id}]
- `PaymentSetup.PaymentMethod` · read-only [from rendered types]  _(+1 more)_
- `PaymentSetup.PaymentReason` · read-only [from rendered types]  _(+1 more)_
- `PaymentSetup.PaymentReasonId` · editable [from rendered types]  _(+3 more)_
- `PaymentSetup.PaymentSetupId` · read-only [from rendered types]  _(+1 more)_
- `PaymentSetup.PaymentSetups` [from web-service: GET /v1/payment-setups]  _(+1 more)_
- `PaymentSetup.TransactionType` · read-only [from rendered types]  _(+1 more)_
- `PaymentSetup.TransactionTypeId` · editable [from rendered types]  _(+3 more)_
> related shapes: `BankPaymentSetup` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### Role  ·  sources: rendered-types, web-service  ·  operations: SELECT
- `Role.Id` · read-only [from rendered types]
- `Role.Name` · read-only [from rendered types]
- `Role.Roles` [from web-service: GET /v1/roles]

### sync  ·  sources: web-service  ·  operations: INSERT
- `sync.Id` [from web-service: POST /v1/roles/sync]
- `sync.Messages` [from web-service: POST /v1/roles/sync]
- `sync.MessageType` [from web-service: POST /v1/roles/sync]

### Transaction  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `Transaction.Amount` · editable [from rendered types]  _(+3 more)_
- `Transaction.BankAccount` · read-only [from rendered types]  _(+1 more)_
- `Transaction.BankAccountId` · editable [from rendered types]  _(+3 more)_
- `Transaction.BankAccountNumber` · read-only [from rendered types]  _(+1 more)_
- `Transaction.BankPaymentMethod` · read-only [from rendered types]  _(+1 more)_
- `Transaction.BankPaymentMethodId` · editable [from rendered types]  _(+3 more)_
- `Transaction.BeneficiaryAccountNumber` · editable [from rendered types]  _(+3 more)_
- `Transaction.BeneficiaryId` · editable [from rendered types]  _(+3 more)_
- `Transaction.BeneficiaryName` · editable [from rendered types]  _(+3 more)_
- `Transaction.BeneficiarySortCode` · editable [from rendered types]  _(+3 more)_
- `Transaction.BusinessUnit` · read-only [from rendered types]  _(+1 more)_
- `Transaction.BusinessUnitDepartmentId` · editable [from rendered types]  _(+3 more)_
- `Transaction.BusinessUnitId` · editable [from rendered types]  _(+3 more)_
- `Transaction.CostCentre` · read-only [from rendered types]  _(+1 more)_
- `Transaction.Currency` · read-only [from rendered types]  _(+1 more)_
- `Transaction.CurrencyId` · editable [from rendered types]  _(+3 more)_
- `Transaction.DateCreated` · editable [from rendered types]  _(+3 more)_
- `Transaction.Department` · read-only [from rendered types]  _(+1 more)_
- `Transaction.DepartmentId` · read-only [from rendered types]  _(+1 more)_
- `Transaction.ExecutionDate` · editable [from rendered types]  _(+3 more)_
- `Transaction.Id` [from web-service: DELETE /v1/transactions/{Id}]
- `Transaction.InstructionId` · editable [from rendered types]  _(+3 more)_
- `Transaction.Messages` [from web-service: DELETE /v1/transactions/{Id}]
- `Transaction.MessageType` [from web-service: DELETE /v1/transactions/{Id}]
- `Transaction.PaymentReason` · read-only [from rendered types]  _(+1 more)_
- `Transaction.PaymentReasonId` · editable [from rendered types]  _(+3 more)_
- `Transaction.PaymentReference` · editable [from rendered types]  _(+3 more)_
- `Transaction.ProcessInstanceId` · editable [from rendered types]  _(+3 more)_
- `Transaction.RequestedBy` · read-only [from rendered types]  _(+1 more)_
- `Transaction.StadiumUserUuid` · editable [from rendered types]  _(+2 more)_
- `Transaction.Status` · read-only [from rendered types]  _(+1 more)_
- `Transaction.TrackingNumber` · read-only [from rendered types]  _(+1 more)_
- `Transaction.TransactionManualCaptureStep` · read-only [from rendered types]  _(+1 more)_
- `Transaction.TransactionManualCaptureStepId` · editable [from rendered types]  _(+3 more)_
- `Transaction.Transactions` [from web-service: GET /v1/transactions]  _(+2 more)_
- `Transaction.Transactions.Amount` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BankAccount` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BankAccountId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BankAccountNumber` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BankPaymentMethod` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BankPaymentMethodId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BeneficiaryAccountNumber` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BeneficiaryId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BeneficiaryName` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BeneficiarySortCode` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BusinessUnit` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BusinessUnitDepartmentId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.BusinessUnitId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.CostCentre` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.Currency` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.CurrencyId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.DateCreated` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.Department` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.DepartmentId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.ExecutionDate` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.InstructionId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.PaymentReason` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.PaymentReasonId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.PaymentReference` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.ProcessInstanceId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.RequestedBy` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.Status` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.TrackingNumber` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.TransactionManualCaptureStep` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.TransactionManualCaptureStepId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.TransactionType` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.TransactionTypeId` [from web-service: GET /v1/transactions]
- `Transaction.Transactions.UserId` [from web-service: GET /v1/transactions]
- `Transaction.TransactionType` · read-only [from rendered types]  _(+1 more)_
- `Transaction.TransactionTypeId` · editable [from rendered types]  _(+3 more)_
- `Transaction.UserId` · read-only [from rendered types]  _(+1 more)_
> related shapes: `TransactionNote`, `TransactionSupportingDocument`, `TransactionType` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### TransactionNote  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `TransactionNote.DateCreated` · editable [from rendered types]  _(+2 more)_
- `TransactionNote.Id` · read-only [from web-service: DELETE /v1/transaction-notes/{Id}]  _(+1 more)_
- `TransactionNote.Messages` [from web-service: DELETE /v1/transaction-notes/{Id}]
- `TransactionNote.MessageType` [from web-service: DELETE /v1/transaction-notes/{Id}]
- `TransactionNote.Note` · editable [from rendered types]  _(+2 more)_
- `TransactionNote.StadiumUserUuid` · editable [from rendered types]  _(+2 more)_
- `TransactionNote.TransactionId` · editable [from rendered types]  _(+2 more)_
- `TransactionNote.TransactionNotes` [from web-service: GET /v1/transaction-notes]
- `TransactionNote.User` · read-only [from rendered types]
- `TransactionNote.UserId` · read-only [from rendered types]
> related shapes: `Transaction` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### TransactionSupportingDocument  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT
- `TransactionSupportingDocument.DateCreated` · editable [from rendered types]  _(+1 more)_
- `TransactionSupportingDocument.FileLocation` · editable [from rendered types]  _(+1 more)_
- `TransactionSupportingDocument.FileName` : String · editable [from rendered types]  _(+1 more)_
- `TransactionSupportingDocument.Id` · read-only [from web-service: DELETE /v1/transaction-supporting-documents/{Id}]  _(+1 more)_
- `TransactionSupportingDocument.Messages` [from web-service: DELETE /v1/transaction-supporting-documents/{Id}]
- `TransactionSupportingDocument.MessageType` [from web-service: DELETE /v1/transaction-supporting-documents/{Id}]
- `TransactionSupportingDocument.StadiumUserUuid` · editable [from rendered types]  _(+1 more)_
- `TransactionSupportingDocument.TransactionId` · editable [from rendered types]  _(+1 more)_
- `TransactionSupportingDocument.TransactionSupportingDocuments` [from web-service: GET /v1/transaction-supporting-documents]
- `TransactionSupportingDocument.User` · read-only [from rendered types]
- `TransactionSupportingDocument.UserId` · read-only [from rendered types]
> related shapes: `Transaction` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### TransactionType  ·  sources: rendered-types, web-service  ·  operations: SELECT
- `TransactionType.Id` · read-only [from rendered types]
- `TransactionType.Name` · read-only [from rendered types]
- `TransactionType.TransactionTypes` [from web-service: GET /v1/transaction-types]
> related shapes: `Transaction` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### User  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `User.ApprovalLevelAssignStatus` · read-only [from rendered types]  _(+1 more)_
- `User.BusinessUnit` · read-only [from rendered types]  _(+1 more)_
- `User.BusinessUnitDepartments` · editable [from rendered types]  _(+3 more)_
- `User.BusinessUnitDepartments.BusinessUnitDepartmentId` [from web-service: POST /v1/users]  _(+1 more)_
- `User.BusinessUnitDepartments.DepartmentName` [from web-service: POST /v1/users]  _(+1 more)_
- `User.BusinessUnitDepartmentString` · read-only [from rendered types]  _(+1 more)_
- `User.BusinessUnitId` · editable [from rendered types]  _(+3 more)_
- `User.Email` · editable [from rendered types]  _(+3 more)_
- `User.FirstName` · editable [from rendered types]  _(+3 more)_
- `User.Id` · read-only [from web-service: DELETE /v1/users/{Id}]  _(+2 more)_
- `User.IsAdministrator` · editable [from rendered types]  _(+3 more)_
- `User.LastChangedDate` · read-only [from rendered types]  _(+1 more)_
- `User.LastChangedUser` · read-only [from rendered types]  _(+1 more)_
- `User.LastName` · editable [from rendered types]  _(+3 more)_
- `User.Messages` [from web-service: DELETE /v1/users/{Id}]
- `User.MessageType` [from web-service: DELETE /v1/users/{Id}]
- `User.Password` · editable [from rendered types]  _(+2 more)_
- `User.Roles` · editable [from rendered types]  _(+3 more)_
- `User.Roles.Id` [from web-service: POST /v1/users]  _(+1 more)_
- `User.Roles.Name` [from web-service: POST /v1/users]  _(+1 more)_
- `User.RolesString` · read-only [from rendered types]  _(+1 more)_
- `User.StadiumUserId` · read-only [from rendered types]  _(+1 more)_
- `User.Users` [from web-service: GET /v1/users]
- `User.Users.ApprovalLevelAssignStatus` [from web-service: GET /v1/users]
- `User.Users.BusinessUnit` [from web-service: GET /v1/users]
- `User.Users.BusinessUnitDepartments` [from web-service: GET /v1/users]
- `User.Users.BusinessUnitDepartmentString` [from web-service: GET /v1/users]
- `User.Users.BusinessUnitId` [from web-service: GET /v1/users]
- `User.Users.Email` [from web-service: GET /v1/users]
- `User.Users.FirstName` [from web-service: GET /v1/users]
- `User.Users.Id` [from web-service: GET /v1/users]
- `User.Users.IsAdministrator` [from web-service: GET /v1/users]
- `User.Users.LastChangedDate` [from web-service: GET /v1/users]
- `User.Users.LastChangedUser` [from web-service: GET /v1/users]
- `User.Users.LastName` [from web-service: GET /v1/users]
- `User.Users.Roles` [from web-service: GET /v1/users]
- `User.Users.RolesString` [from web-service: GET /v1/users]
- `User.Users.StadiumUserId` [from web-service: GET /v1/users]
  - relation: `User.BusinessUnitDepartments` → `BusinessUnitDepartment[]` (nested type) [from rendered types]
  - relation: `User.Roles` → `Role[]` (nested type) [from rendered types]
> related shapes: `UserApprovalLevel`, `UserApprovalLevelAmount` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserApprovalLevel  ·  sources: rendered-types, web-service  ·  operations: DELETE, INSERT, SELECT
- `UserApprovalLevel.ApprovalLevelId` · editable [from rendered types]  _(+1 more)_
- `UserApprovalLevel.BusinessUnit` · read-only [from rendered types]
- `UserApprovalLevel.BusinessUnitDepartmentId` · read-only [from rendered types]
- `UserApprovalLevel.BusinessUnitId` · read-only [from rendered types]
- `UserApprovalLevel.Department` · read-only [from rendered types]
- `UserApprovalLevel.DepartmentId` · read-only [from rendered types]
- `UserApprovalLevel.Id` [from web-service: DELETE /v1/user-approval-levels/{ApprovalLevelId},{UserId}]
- `UserApprovalLevel.MaxApprovalAmount` · read-only [from rendered types]
- `UserApprovalLevel.Messages` [from web-service: DELETE /v1/user-approval-levels/{ApprovalLevelId},{UserId}]
- `UserApprovalLevel.MessageType` [from web-service: DELETE /v1/user-approval-levels/{ApprovalLevelId},{UserId}]
- `UserApprovalLevel.TransactionType` · read-only [from rendered types]
- `UserApprovalLevel.TransactionTypeId` · read-only [from rendered types]
- `UserApprovalLevel.UserApprovalLevels` [from web-service: GET /v1/user-approval-levels/{UserId}]
- `UserApprovalLevel.UserEmail` · read-only [from rendered types]
- `UserApprovalLevel.UserId` · editable [from rendered types]  _(+1 more)_
- `UserApprovalLevel.UserName` · read-only [from rendered types]
> related shapes: `ApprovalLevel`, `User`, `UserApprovalLevelAmount` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

### UserApprovalLevelAmount  ·  sources: rendered-types, web-service  ·  operations: SELECT
- `UserApprovalLevelAmount.ApprovalLevelId` · read-only [from rendered types]
- `UserApprovalLevelAmount.MaxApprovalAmount` · read-only [from rendered types]
- `UserApprovalLevelAmount.Status` · read-only [from rendered types]
- `UserApprovalLevelAmount.UserApprovalLevelAmounts` [from web-service: GET /v1/user-approval-levels/{BusinessUnitId},{DepartmentId},{TransactionTypeId}]
> related shapes: `ApprovalLevel`, `ApprovalLevelAmount`, `User`, `UserApprovalLevel` (not merged — distinct field sets) `[AI-SUGGESTED: domain inference]`

> The design model defines 1378 internal data-type instances (control/result/parameter bindings); field types above are sourced from them where concrete. Full detail is in the forensic model.json.

## Tier-A — CRUD matrix

| Entity | SELECT | INSERT | UPDATE | DELETE | Evidence |
|---|:---:|:---:|:---:|:---:|---|
| ApprovalLevel | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| ApprovalLevelAmount | ✓ |  |  |  | rendered-types, web-service |
| ApprovalLevelRule | ✓ |  | ✓ |  | rendered-types, web-service |
| Bank | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| BankAccount | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| BankAccountType | ✓ |  |  |  | rendered-types, web-service |
| BankPaymentMethod | ✓ |  |  |  | rendered-types, web-service |
| BankPaymentSetup | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| Beneficiary | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| BusinessUnit | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| BusinessUnitDepartment | ✓ |  |  |  | rendered-types, web-service |
| CostCentre | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| Department | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| LookupData | ✓ |  |  |  | rendered-types, web-service |
| MaxApprovalAmount |  |  |  |  | rendered-types |
| PaymentDetailAuditLog | ✓ |  |  |  | rendered-types, web-service |
| PaymentDetailAuditLogRead_Data |  |  |  |  | rendered-types |
| PaymentReason | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| PaymentSetup | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| Role | ✓ |  |  |  | rendered-types, web-service |
| sync |  | ✓ |  |  | web-service |
| Transaction | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| TransactionNote | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| TransactionSupportingDocument | ✓ | ✓ |  | ✓ | rendered-types, web-service |
| TransactionType | ✓ |  |  |  | rendered-types, web-service |
| User | ✓ | ✓ | ✓ | ✓ | rendered-types, web-service |
| UserApprovalLevel | ✓ | ✓ |  | ✓ | rendered-types, web-service |
| UserApprovalLevelAmount | ✓ |  |  |  | rendered-types, web-service |

## Tier-B — entity lifecycle / states (inferred)
- Status-like fields suggest stateful entities: `ApprovalAmount`, `ApprovalLevelAmounts`, `ApprovalLevelAmounts.ApprovalLevelId`, `ApprovalLevelAmounts.MaxApprovalAmount`, `ApprovalLevelAssignStatus`, `ApprovalLevelId`, `ApprovalLevelRules`, `ApprovalLevels`, `ApprovalLevels.BusinessUnit`, `ApprovalLevels.BusinessUnitDepartmentId`, `ApprovalLevels.BusinessUnitId`, `ApprovalLevels.Department`, `ApprovalLevels.DepartmentId`, `ApprovalLevels.TransactionType`, `ApprovalLevels.TransactionTypeId`, `BankReleaseApproval`, `ManagerialApproval`, `MaxApprovalAmount`, `MaxApprovalAmounts`, `Status`, `Transactions.Status`, `TreasuryApproval`, `UserApprovalLevelAmounts`, `UserApprovalLevels`, `Users.ApprovalLevelAssignStatus` `[AI-SUGGESTED]`
