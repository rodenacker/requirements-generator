---
stadium_asset: surfaces
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
# Surfaces (screens, controls, layout) — PaymentsApp

> Tier-A = which surfaces/controls/data exist (authoritative). Tier-B = layout & control-choice (advisory; the system holds design authority).

## View / task / feature inventory

> Columns Page / Title / Route / Start / Design-surface / Reachable / Route-declared are **Tier-A** facts (design model + administration.db + rendered `page-routes.js`). **Inferred kind** is **Tier-B** `[AI-SUGGESTED]` (name-suffix taxonomy; bare nouns → entity-maintenance). Title + Route come from the rendered router `[from rendered routes]`.

| Page | Title | Route | Start? | Design surface? | Reachable via nav? | Route-declared? | Inferred kind |
|---|---|---|:---:|:---:|:---:|:---:|---|
| Roles | Roles | `/Roles` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| Users | Users | `/Users` | ✓ | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| CostCentres | Users | `/CostCentres` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| BusinessUnits | Users | `/BusinessUnits` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| Beneficiaries | Users | `/Beneficiaries` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| Banks | Users | `/Banks` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| BankAccounts | Users | `/BankAccounts` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| BankPaymentSetup | Users | `/BankPaymentSetup` |  | ✓ |  | ✓ | configure `[AI-SUGGESTED]` |
| Department | Users | `/Department` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| PaymentReason | Users | `/PaymentReason` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| PaymentEnquiries | Payment Enquiries | `/PaymentEnquiries` |  | ✓ | ✓ | ✓ | reporting `[AI-SUGGESTED]` |
| PaymentDetails | Payment Details | `/PaymentDetails` |  | ✓ | ✓ | ✓ | detail `[AI-SUGGESTED]` |
| PaymentSetup | Payment Setup | `/PaymentSetup` |  | ✓ |  | ✓ | configure `[AI-SUGGESTED]` |
| DraftManualPaymentCapture | Draft Manual Payment Capture | `/DraftManualPaymentCapture` |  | ✓ | ✓ | ✓ | workflow-step `[AI-SUGGESTED]` |
| TransactionCoding | Transaction Coding | `/TransactionCoding` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| PaymentsDetails | Payments Details | `/PaymentsDetails` |  | ✓ | ✓ | ✓ | detail `[AI-SUGGESTED]` |
| BeneficiaryDetails | Beneficiary Details | `/BeneficiaryDetails` |  | ✓ | ✓ | ✓ | detail `[AI-SUGGESTED]` |
| AttachmentsAndNotes | Attachments And Notes | `/AttachmentsAndNotes` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| Review | Review | `/Review` |  | ✓ | ✓ | ✓ | list `[AI-SUGGESTED]` |
| ApprovalLevels | Approval Levels | `/ApprovalLevels` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| UserApprovalLevels | User Approval Levels | `/UserApprovalLevels` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| ApprovalLevelRules | Approval Level Rules | `/ApprovalLevelRules` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |

## Tier-A — reports & dashboards

- Report surfaces (export-enabled grid or reporting page-kind): `Roles`, `Users`, `CostCentres`, `BusinessUnits`, `Beneficiaries`, `Banks`, `BankAccounts`, `BankPaymentSetup`, `Department`, `PaymentReason`, `PaymentEnquiries`, `PaymentSetup` [from design model]

## Roles  ·  title: Roles  ·  roles: —
  - Button: `SyncRolesButton` — "Sync Stadium Roles"
  - DataGrid: `RolesDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Id"(hidden), `Name` "Role" [from design model]
- Visible terms: "Roles" [from design model]
> Layout: 2 meaningful control(s) within 5 layout container(s); max control-tree nesting depth 3 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — Roles (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `SyncRolesButton` → `PaymentsApiUsers.RoleSync`
- `SyncRolesButton` → `PaymentsApiUsers.RoleGetList`
- `Roles` → `PaymentsApiUsers.RoleGetList`

## Users ⭐ start  ·  title: Users  ·  roles: User
  - Button: `AddUserButton` — "Add User"
  - DataGrid: `UsersDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Edit"(action), "Delete"(action), `ViewAssignedApprovalLevels` "View Assigned Approval Levels"(action), `AssignApprovalLevels` "Assign Approval Levels", "Id"(hidden), `StadiumUserId` "Stadium User Id"(hidden), "Email", `FirstName` "First Name", `LastName` "Last Name", `IsAdministrator` "Is Administrator", `RolesString` "Roles", "Roles"(hidden), `BusinessUnit` "Business Unit", `BusinessUnitId` "Business Unit Id"(hidden), `BusinessUnitDepartmentString` "Department", `BusinessUnitDepartments` "Business Unit Departments"(hidden), `LastChangedUser` "Last Changed User", `LastChangedDate` "Last Changed Date" [from design model]
  - TextBox: `EmailTextBox`
  - TextBox: `FirstNameTextBox`
  - TextBox: `LastNameTextBox`
  - CheckBox: `IsAdministartorCheckBox`
  - TextBox: `PasswordTextBox`  ·  password-masked
  - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
  - CheckBoxList: `BusinessUnitDepartmentsCheckBoxList`  ·  dynamic choices (bound)
  - CheckBoxList: `RolesCheckBoxList`  ·  dynamic choices (bound)
  - Button: `CancelButton` — "Cancel"
  - Button: `EditSaveButton` — "Save"
  - Button: `AddSaveButton` — "Save"
  - DataGrid: `ViewAssignedApprovalLevelsDataGrid`
    - columns (in order): `BusinessUnitId` "Business Unit Id"(hidden), `BusinessUnit` "Business Unit", "Department", `DepartmentId` "Department Id"(hidden), `TransactionTypeId` "Transaction Type Id"(hidden), `TransactionType` "Transaction Type", `MaxApprovalAmount` "Max Approval Amount" [from design model]
  - Button: `CancelViewApprovedLevelsButton` — "Cancel"
- Visible terms: "Users", "Email", "First Name", "Last Name", "Administrator", "Password", "BusinessUnits", "Departments", "Roles" [from design model]
> Layout: 15 meaningful control(s) within 64 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — Users (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `UsersDataGrid` → `PaymentsApiUsers.UserGetById`
- `UsersDataGrid` → `PaymentsApiUsers.UserDelete`
- `UsersDataGrid` → `PaymentsApiPaymentApprovals.UserApprovalLevelGetListByUserId`
- `BusinessUnitDropDown` → `PaymentsApiSetup.BusinessUnitDepartmentGetListById`
- `EditSaveButton` → `PaymentsApiUsers.UserUpdate`
- `AddSaveButton` → `PaymentsApiUsers.UserCreate`
- `RefreshUsers` → `PaymentsApiUsers.UserGetList`
- `LoadDropdownsAndCheckboxlists` → `PaymentsApiUsers.RoleGetList`
- `LoadDropdownsAndCheckboxlists` → `PaymentsApiSetup.BusinessUnitGetList`
- `LoadDropdownsAndCheckboxlists` → `PaymentsApiSetup.BusinessUnitDepartmentGetListById`

## CostCentres  ·  title: Users  ·  roles: —
  - DataGrid: `CostCentreDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name", "Description", `BusinessUnit` "Business Unit", `BusinessUnitId` "Business Unit Id"(hidden), "BusinessUnitDepartments"(hidden), `BusinessUnitDepartmentString` "Departments" [from design model]
  - TextBox: `NameTextBox`
  - TextBox: `DescriptionTextBox`
  - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
  - CheckBoxList: `BusinessUnitDepartmentsCheckBoxList`  ·  dynamic choices (bound)
  - Button: `CancelButton` — "Cancel"
  - Button: `EditSaveButton` — "Save"
  - Button: `AddSaveButton` — "Save"
- Visible terms: "Cost Centres", "Name", "Description", "BusinessUnits", "Departments" [from design model]
> Layout: 8 meaningful control(s) within 41 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — CostCentres (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `CostCentreDataGrid` → `PaymentsApiSetup.CostCentreGetById`
- `CostCentreDataGrid` → `PaymentsApiSetup.CostCentreDelete`
- `BusinessUnitDropDown` → `PaymentsApiSetup.BusinessUnitDepartmentGetListById`
- `EditSaveButton` → `PaymentsApiSetup.CostCentreUpdate`
- `AddSaveButton` → `PaymentsApiSetup.CostCentreCreate`
- `RefreshCostCentre` → `PaymentsApiSetup.CostCentreGetList`
- `LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions` → `PaymentsApiSetup.BusinessUnitGetList`
- `LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions` → `PaymentsApiSetup.BusinessUnitDepartmentGetListById`

## BusinessUnits  ·  title: Users  ·  roles: —
  - DataGrid: `BusinessUnitDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name"(hidden), "Description", "Code", `DepartmentString` "Transaction types", "Departments"(hidden) [from design model]
  - TextBox: `NameTextBox`
  - TextBox: `DescriptionTextBox`
  - TextBox: `CodeTextBox`
  - CheckBoxList: `DepartmentsCheckBoxList`  ·  dynamic choices (bound)
  - Button: `CancelButton` — "Cancel"
  - Button: `EditSaveButton` — "Save"
  - Button: `AddSaveButton` — "Save"
- Visible terms: "Business Units", "Name", "Description", "Code", "Departments" [from design model]
> Layout: 8 meaningful control(s) within 41 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — BusinessUnits (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `BusinessUnitDataGrid` → `PaymentsApiSetup.BusinessUnitGetById`
- `BusinessUnitDataGrid` → `PaymentsApiSetup.BusinessUnitDelete`
- `EditSaveButton` → `PaymentsApiSetup.BusinessUnitUpdate`
- `AddSaveButton` → `PaymentsApiSetup.BusinessUnitCreate`
- `RefreshBusinessUnits` → `PaymentsApiSetup.BusinessUnitGetList`
- `LoadDepartmentCheckboxListOptions` → `PaymentsApiSetup.DepartmentGetList`

## Beneficiaries  ·  title: Users  ·  roles: —
  - DataGrid: `BeneficiaryDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name"(hidden), `AccountName` "Account Name", `AccountNumber` "Account Number", `BankAccountTypeName` "Bank Account Type", `BankName` "Bank", "IBAN", `BankId` "Bank Id"(hidden), `BankAccountTypeId` "Bank Account Type Id"(hidden), `BusinessUnitId`(hidden), `BusinessUnit` "Business Unit", `BusinessUnitDepartments` "Business Unit Departments"(hidden), `BusinessUnitDepartmentString` "Departments" [from design model]
      - ⚠ `BusinessUnitId` header resolves to "Business Unit " (design header is an unresolved binding) [from rendered view]
  - TextBox: `NameTextBox`
  - TextBox: `AccountNameTextBox`
  - TextBox: `AccountNumberTextBox`  ·  hint: "Only numbers are allowed"
  - DropDown: `AccountTypeDropDown`  ·  hint: "Select an account type" · dynamic choices (bound)
  - DropDown: `BankDropDown`  ·  hint: "Select a bank" · dynamic choices (bound)
  - TextBox: `IbanTextBox`
  - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
  - CheckBoxList: `BusinessUnitDepartmentsCheckBoxList`  ·  dynamic choices (bound)
  - Button: `CancelButton` — "Cancel"
  - Button: `EditSaveButton` — "Save"
  - Button: `AddSaveButton` — "Save"
- Visible terms: "Beneficiaries", "Name", "Account Name", "Account Number", "Account Type", "Bank", "Business Unit", "Departments" [from design model]
> Layout: 12 meaningful control(s) within 57 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — Beneficiaries (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `BeneficiaryDataGrid` → `PaymentsApiSetup.BeneficiaryGetById`
- `BeneficiaryDataGrid` → `PaymentsApiSetup.BeneficiaryDelete`
- `BusinessUnitDropDown` → `PaymentsApiSetup.BusinessUnitDepartmentGetListById`
- `EditSaveButton` → `PaymentsApiSetup.BeneficiaryUpdate`
- `AddSaveButton` → `PaymentsApiSetup.BeneficiaryCreate`
- `RefreshBeneficiary` → `PaymentsApiSetup.BeneficiaryGetList`
- `LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions` → `PaymentsApiSetup.BusinessUnitGetList`
- `LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions` → `PaymentsApiSetup.BusinessUnitDepartmentGetListById`
- `LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions` → `PaymentsApiSetup.BankGetList`
- `LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions` → `PaymentsApiSetup.BankAccountTypeGetList`

## Banks  ·  title: Users  ·  roles: —
  - DataGrid: `BankDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name", `UniversalBranchCode` "Universal Branch Code", `UniversalSwiftCode` "Universal Swift Code" [from design model]
  - TextBox: `NameTextBox`
  - TextBox: `UniversalBranchCodeTextBox`
  - TextBox: `UniversalSwiftCodeTextBox`
  - Button: `CancelButton` — "Cancel"
  - Button: `EditSaveButton` — "Save"
  - Button: `AddSaveButton` — "Save"
- Visible terms: "Banks", "Name", "Universal Branch Code", "Universal Swift Code" [from design model]
> Layout: 7 meaningful control(s) within 37 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — Banks (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `BankDataGrid` → `PaymentsApiSetup.BankGetById`
- `BankDataGrid` → `PaymentsApiSetup.BankDelete`
- `EditSaveButton` → `PaymentsApiSetup.BankUpdate`
- `AddSaveButton` → `PaymentsApiSetup.BankCreate`
- `RefreshBank` → `PaymentsApiSetup.BankGetList`

## BankAccounts  ·  title: Users  ·  roles: —
  - DataGrid: `BankAccountDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), `AccountName` "Account Name", `AccountNumber` "Account Number", `BankAccountTypeName` "Bank Account Type", `BankAccountTypeId` "Bank Account Type Id"(hidden), "IBAN", `BankName` "Bank", `BankId` "Bank Id"(hidden), `BusinessUnit` "Business Unit", `BusinessUnitId` "Business Unit Id"(hidden) [from design model]
  - TextBox: `AccountNameTextBox`
  - TextBox: `AccountNumberTextBox`
  - DropDown: `AccountTypeDropDown`  ·  hint: "Select an Account type" · dynamic choices (bound)
  - DropDown: `BankDropDown`  ·  hint: "Select a Bank" · dynamic choices (bound)
  - TextBox: `IbanTextBox`
  - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a Business unit" · dynamic choices (bound)
  - Button: `CancelButton` — "Cancel"
  - Button: `EditSaveButton` — "Save"
  - Button: `AddSaveButton` — "Save"
- Visible terms: "Bank Accounts", "Account Name", "Account Number", "Account Type", "Bank", "IBAN", "Business Unit" [from design model]
> Layout: 10 meaningful control(s) within 49 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — BankAccounts (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `AddBankAccountButton` → `PaymentsApiSetup.BankAccountTypeGetList`
- `AddBankAccountButton` → `PaymentsApiSetup.BankGetList`
- `AddBankAccountButton` → `PaymentsApiSetup.BusinessUnitGetList`
- `BankAccountDataGrid` → `PaymentsApiSetup.BankAccountGetById`
- `BankAccountDataGrid` → `PaymentsApiSetup.BankAccountTypeGetList`
- `BankAccountDataGrid` → `PaymentsApiSetup.BankGetList`
- `BankAccountDataGrid` → `PaymentsApiSetup.BusinessUnitGetList`
- `BankAccountDataGrid` → `PaymentsApiSetup.BankAccountDelete`
- `EditSaveButton` → `PaymentsApiSetup.BankAccountUpdate`
- `AddSaveButton` → `PaymentsApiSetup.BankAccountCreate`
- `RefreshBankAccounts` → `PaymentsApiSetup.BankAccountGetList`

## BankPaymentSetup  ·  title: Users  ·  roles: —
  - DataGrid: `BankPaymentSetupDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Bank", `PaymentMethod` "Payment Method", `TransferMethod` "Transfer Method", `ServiceLevelCode` "Service Level Code", `ChargeBearer` "Charge Bearer", `CutOffTime` "Cut Off Time", `ApiEnabled` "Api Enabled" [from design model]
  - DropDown: `BankDropDown`  ·  hint: "Select a bank" · dynamic choices (bound)
  - DropDown: `BankPaymentMethodDropDown`  ·  hint: "Select a payment method" · dynamic choices (bound)
  - DropDown: `TransferMethodDropDown`  ·  hint: "Select a transfer method" · dynamic choices (bound)
  - DropDown: `ServiceLevelCodeDropDown`  ·  hint: "Select a service level code" · dynamic choices (bound)
  - DropDown: `ChargeBearerDropDown`  ·  hint: "Select a charge bearer" · dynamic choices (bound)
  - TextBox: `CutOffTimeTextBox`  ·  hint: "Please provide time in format hh:mm"
  - CheckBox: `ApiEnabledCheckBox`
  - Button: `CancelButton` — "Cancel"
  - Button: `EditSaveButton` — "Save"
  - Button: `AddSaveButton` — "Save"
- Visible terms: "Bank Payment Setup", "Bank", "Bank Payment Method", "Transfer Method", "Service Level Code", "Charge Bearer", "Cut Off Time", "Api Enabled" [from design model]
> Layout: 11 meaningful control(s) within 53 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — BankPaymentSetup (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `AddBankPaymentSetupButton` → `PaymentsApiSetup.BankGetList`
- `AddBankPaymentSetupButton` → `PaymentsApiSetup.BankPaymentMethodGetList`
- `AddBankPaymentSetupButton` → `PaymentsApiSetup.LookupDataGetList_TransferMethod`
- `AddBankPaymentSetupButton` → `PaymentsApiSetup.LookupDataGetList_ServiceLevelCode`
- `AddBankPaymentSetupButton` → `PaymentsApiSetup.LookupDataGetList_ChargeBearer`
- `BankPaymentSetupDataGrid` → `PaymentsApiSetup.BankPaymentSetupGetById`
- `BankPaymentSetupDataGrid` → `PaymentsApiSetup.BankGetList`
- `BankPaymentSetupDataGrid` → `PaymentsApiSetup.BankPaymentMethodGetList`
- `BankPaymentSetupDataGrid` → `PaymentsApiSetup.LookupDataGetList_TransferMethod`
- `BankPaymentSetupDataGrid` → `PaymentsApiSetup.LookupDataGetList_ServiceLevelCode`
- `BankPaymentSetupDataGrid` → `PaymentsApiSetup.LookupDataGetList_ChargeBearer`
- `BankPaymentSetupDataGrid` → `PaymentsApiSetup.BankPaymentSetupDelete`
- `EditSaveButton` → `PaymentsApiSetup.BankPaymentSetupUpdate`
- `AddSaveButton` → `PaymentsApiSetup.BankPaymentSetupCreate`
- `RefreshBankPaymentSetup` → `PaymentsApiSetup.BankPaymentSetupGetList`

## Department  ·  title: Users  ·  roles: —
  - DataGrid: `DepartmentDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name", "Description" [from design model]
  - TextBox: `NameTextBox`
  - TextBox: `DescriptionTextBox`
  - Button: `CancelButton` — "Cancel"
  - Button: `EditSaveButton` — "Save"
  - Button: `AddSaveButton` — "Save"
- Visible terms: "Name", "Description" [from design model]
> Layout: 6 meaningful control(s) within 33 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — Department (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `DepartmentDataGrid` → `PaymentsApiSetup.DepartmentGetById`
- `DepartmentDataGrid` → `PaymentsApiSetup.DepartmentDelete`
- `EditSaveButton` → `PaymentsApiSetup.DepartmentUpdate`
- `AddSaveButton` → `PaymentsApiSetup.DepartmentCreate`
- `RefreshDepartmentSetup` → `PaymentsApiSetup.DepartmentGetList`

## PaymentReason  ·  title: Users  ·  roles: —
  - DataGrid: `PaymentReasonDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name", "Description", "Code" [from design model]
  - TextBox: `NameTextBox`
  - TextBox: `DescriptionTextBox`
  - TextBox: `CodeTextBox`
  - Button: `CancelButton` — "Cancel"
  - Button: `EditSaveButton` — "Save"
  - Button: `AddSaveButton` — "Save"
- Visible terms: "Name", "Description", "Code" [from design model]
> Layout: 7 meaningful control(s) within 37 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — PaymentReason (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `PaymentReasonDataGrid` → `PaymentsApiPaymentTransactions.PaymentReasonGetById`
- `PaymentReasonDataGrid` → `PaymentsApiPaymentTransactions.PaymentReasonDelete`
- `EditSaveButton` → `PaymentsApiPaymentTransactions.PaymentReasonUpdate`
- `AddSaveButton` → `PaymentsApiPaymentTransactions.PaymentReasonCreate`
- `RefreshPaymentReason` → `PaymentsApiPaymentTransactions.PaymentReasonGetList`

## PaymentEnquiries  ·  title: Payment Enquiries  ·  roles: —
  - Button: `ApplyFilterButton` — "Apply Filters"
  - Button: `ClearFilterButton` — "Clear Filters"
  - DataGrid: `PaymentEnquiryDataGrid`
    - columns (in order): `PaymentDetail` "Payment Detail"(action), `TrackingNumber` "Tracking Number", "Status", `DateCreated` "Date Created", `RequestedBy` "Requested By", `BusinessUnit` "Business Unit", `TransactionType` "Transaction Type", `BankPaymentMethod` "Bank Payment Method", `BeneficiaryName` "Beneficiary", `PaymentReference` "Payment Reference", `ExecutionDate` "Execution Date", "Currency", "Amount" [from design model]
- Visible terms: "Payment Enquiries" [from design model]
> Layout: 3 meaningful control(s) within 10 layout container(s); max control-tree nesting depth 4 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — PaymentEnquiries (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `PaymentEnquiries` → `PaymentsApiPaymentTransactions.TransactionGetList`
- `PaymentEnquiries` → `PaymentsApiPaymentTransactions.TransactionTypeGetList`
- `PaymentEnquiries` → `PaymentsApiSetup.BusinessUnitGetList`

## PaymentDetails  ·  title: Payment Details  ·  roles: —
  - Panel: `Panel` — "Payment Summary"
  - DataGrid: `NotesDataGrid`
    - columns (in order): "Notes", "User", `DateCreated` "Date Created" [from design model]
  - DataGrid: `SupportingDocumentsDataGrid`
    - columns (in order): "Document", "User", `DateCreated` "Date Created", "Download"(action), `FileLocation` "File Location"(hidden) [from design model]
- Visible terms: "Payment Details", "Amount", "Beneficiary", "Requested By", "Status", "Bank Payment Method", "PaymentReference", "Transaction Type", "Business Unit", "Date Created", "Audit Log", "Notes", "Supporting Documents", "Payment Audit Log", "Payment Notes", "Payment Supporting Documents" [from design model]
> Layout: 3 meaningful control(s) within 62 layout container(s); max control-tree nesting depth 9 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — PaymentDetails (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `SupportingDocumentsDataGrid` → `FileSystem.ReadFile`
- `PaymentDetails` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `PaymentDetails` → `PaymentsApiPaymentTransactions.TransactionNoteGetList`
- `PaymentDetails` → `PaymentsApiPaymentTransactions.TransactionSupportingDocumentGetList`

## PaymentSetup  ·  title: Payment Setup  ·  roles: —
  - DataGrid: `PaymentSetupDataGrid`  ·  grid: exportable / searchable
    - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), `BusinessUnit` "Business Unit", "Department", `TransactionType` "Transaction Type", `PaymentMethod` "Payment Method", `PaymentReason` "Payment Reason", `BankAccount` "Bank Account" [from design model]
  - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
  - DropDown: `DepartmentDropDown`  ·  dynamic choices (bound)
  - DropDown: `TransactionTypeDropDown`  ·  hint: "Select a transaction type" · dynamic choices (bound)
  - DropDown: `PaymentMethodDropDown`  ·  hint: "Select a payment method" · dynamic choices (bound)
  - DropDown: `PaymentReasonDropDown`  ·  hint: "Select a payment reason" · dynamic choices (bound)
  - DropDown: `BankAccountDropDown`  ·  hint: "Select a bank account" · dynamic choices (bound)
  - Button: `CancelButton` — "Cancel"
  - Button: `EditSaveButton` — "Save"
  - Button: `AddSaveButton` — "Save"
- Visible terms: "Payment Setup", "BusinessUnit", "Department", "Transaction Type", "Payment Method", "Payment Reason", "Bank Account" [from design model]
> Layout: 10 meaningful control(s) within 49 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — PaymentSetup (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `AddPaymentSetupButton` → `PaymentsApiSetup.BusinessUnitGetList`
- `AddPaymentSetupButton` → `PaymentsApiPaymentTransactions.TransactionTypeGetList`
- `AddPaymentSetupButton` → `PaymentsApiSetup.BankPaymentMethodGetList`
- `AddPaymentSetupButton` → `PaymentsApiPaymentTransactions.PaymentReasonGetList`
- `AddPaymentSetupButton` → `PaymentsApiSetup.BankAccountGetList`
- `PaymentSetupDataGrid` → `PaymentsApiPaymentTransactions.PaymentSetupGetById`
- `PaymentSetupDataGrid` → `PaymentsApiSetup.BusinessUnitGetList`
- `PaymentSetupDataGrid` → `PaymentsApiPaymentTransactions.TransactionTypeGetList`
- `PaymentSetupDataGrid` → `PaymentsApiSetup.BankPaymentMethodGetList`
- `PaymentSetupDataGrid` → `PaymentsApiPaymentTransactions.PaymentReasonGetList`
- `PaymentSetupDataGrid` → `PaymentsApiSetup.BankAccountGetList`
- `PaymentSetupDataGrid` → `PaymentsApiSetup.BusinessUnitDepartmentGetListById`
- `PaymentSetupDataGrid` → `PaymentsApiPaymentTransactions.PaymentSetupDelete`
- `BusinessUnitDropDown` → `PaymentsApiSetup.BusinessUnitDepartmentGetListById`
- `EditSaveButton` → `PaymentsApiPaymentTransactions.PaymentSetupUpdate`
- `AddSaveButton` → `PaymentsApiPaymentTransactions.PaymentSetupCreate`
- `RefreshPaymentSetup` → `PaymentsApiPaymentTransactions.PaymentSetupGetList`

## DraftManualPaymentCapture  ·  title: Draft Manual Payment Capture  ·  roles: —
  - DataGrid: `DraftTransactionsDataGrid`
    - columns (in order): "Detail"(action), "Edit"(action), `TrackingNumber` "Tracking Number", `TransactionManualCaptureStepId` "Transaction Manual Capture Step Id"(hidden), `TransactionManualCaptureStep` "Last saved step", `DateCreated` "Date Created", `RequestedBy` "Requested By", `BusinessUnit` "Business Unit", `TransactionType` "Transaction Type", `BankPaymentMethod` "Bank Payment Method", `BeneficiaryName` "Beneficiary", `PaymentReference` "Payment Reference", `ExecutionDate` "Execution Date", "Currency", "Amount", "Delete"(action) [from design model]
- Visible terms: "Draft Transactions" [from design model]
> Layout: 1 meaningful control(s) within 5 layout container(s); max control-tree nesting depth 3 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — DraftManualPaymentCapture (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `DraftTransactionsDataGrid` → `PaymentsApiPaymentTransactions.TransactionDelete`
- `RefreshDraftPayments` → `PaymentsApiPaymentTransactions.DraftTransactionGetList`

## TransactionCoding  ·  title: Transaction Coding  ·  roles: —
  - Link: `CancelLink` — "Cancel"
  - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
  - DropDown: `BusinessUnitDepartmentDropDown`  ·  hint: "Select a department" · read-only · dynamic choices (bound)
  - DropDown: `TransactionTypeDropDown`  ·  hint: "Select a transaction type" · read-only · dynamic choices (bound)
  - DropDown: `BankAccountDropDown`  ·  hint: "Select a bank account" · read-only · dynamic choices (bound)
  - DropDown: `BankPaymentMethodDropDown`  ·  hint: "Select a bank payment method" · read-only · dynamic choices (bound)
  - DropDown: `PaymentReasonDropDown`  ·  hint: "Select a payment reason" · read-only · dynamic choices (bound)
  - Button: `SaveDraftButton` — "Save Draft"
  - Button: `NextButton` — "Next"
- Visible terms: "Transaction Coding", "Business Unit", "Department", "Transaction Type", "Bank Account", "Bank Payment Method", "Payment Reason" [from design model]
> Layout: 9 meaningful control(s) within 49 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — TransactionCoding (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `CancelLink` → `PaymentsApiPaymentTransactions.TransactionDelete`
- `SaveDraftButton` → `PaymentsApiPaymentTransactions.TransactionCreate`
- `SaveDraftButton` → `PaymentsApiPaymentTransactions.TransactionUpdate`
- `NextButton` → `PaymentsApiPaymentTransactions.TransactionCreate`
- `NextButton` → `PaymentsApiPaymentTransactions.TransactionUpdate`
- `PopulateDropdownsNewEntry` → `PaymentsApiPaymentTransactions.PaymentSetupTransactionCodingGetList`
- `SelectDropdowns` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `PopulateDropdownsExistingEntry` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `PopulateDropdownsExistingEntry` → `PaymentsApiPaymentTransactions.PaymentSetupTransactionCodingGetList`
- `PopulateDropdownsExistingEntry` → `PaymentsApiPaymentTransactions.PaymentSetupTransactionCodingGetList1`
- `PopulateDropdownsExistingEntry` → `PaymentsApiPaymentTransactions.PaymentSetupTransactionCodingGetList2`
- `PopulateDropdownsExistingEntry` → `PaymentsApiPaymentTransactions.PaymentSetupTransactionCodingGetList3`
- `PopulateDropdownsExistingEntry` → `PaymentsApiPaymentTransactions.PaymentSetupTransactionCodingGetList4`
- `PopulateDropdownsExistingEntry` → `PaymentsApiPaymentTransactions.PaymentSetupTransactionCodingGetList5`

## PaymentsDetails  ·  title: Payments Details  ·  roles: —
  - Link: `CancelLink` — "Cancel"
  - TextBox: `AmountTextBox`
  - DropDown: `CurrencyTypeDropDown`  ·  hint: "Select a currency" · dynamic choices (bound)
  - DatePicker: `ExecutionDatePicker`  ·  hint: "Select a date"
  - TextBox: `PaymentReferenceTextBox`
  - Button: `BackButton` — "Back"
  - Button: `SaveDraftButton` — "Save Draft"
  - Button: `NextButton` — "Next"
- Visible terms: "Payment Details", "Amount", "Currency", "Execution Date", "Payment Reference" [from design model]
> Layout: 8 meaningful control(s) within 41 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — PaymentsDetails (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `CancelLink` → `PaymentsApiPaymentTransactions.TransactionDelete`
- `SaveDraftButton` → `PaymentsApiPaymentTransactions.TransactionUpdate`
- `NextButton` → `PaymentsApiPaymentTransactions.TransactionUpdate`
- `PaymentsDetails` → `PaymentsApiSetup.LookupDataGetList`
- `PaymentsDetails` → `PaymentsApiPaymentTransactions.TransactionGetById`

## BeneficiaryDetails  ·  title: Beneficiary Details  ·  roles: —
  - Link: `CancelLink` — "Cancel"
  - RadioButtonList: `WhitelistAndAdhocRadioButtonList`  ·  choices: "WhiteListed", "Ad-hoc"
  - DataGrid: `WhitelistedBeneficiaryDataGrid`
    - columns (in order): "Select"(action), "Id"(hidden), "Name", "Bank", `Account` "Account Details", `AccountNumber` "Account Number"(hidden) [from design model]
  - TextBox: `NameTextBox`
  - TextBox: `AccountNumberTextBox`  ·  hint: "Please enter a numeric value (16 digits)"
  - TextBox: `SortCodeTextBox`  ·  hint: "Please provide a numeric value (6 digits)"
  - Button: `BackButton` — "Back"
  - Button: `SaveDraftButton` — "Save Draft"
  - Button: `NextButton` — "Next"
- Visible terms: "Beneficiary Details", "Create an Adhoc Beneficiary", "Name", "Account Number", "Sort Code" [from design model]
> Layout: 9 meaningful control(s) within 40 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — BeneficiaryDetails (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `CancelLink` → `PaymentsApiPaymentTransactions.TransactionDelete`
- `WhitelistAndAdhocRadioButtonList` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `TransactionUpdate` → `PaymentsApiSetup.BeneficiaryGetById`
- `TransactionUpdate` → `PaymentsApiPaymentTransactions.TransactionUpdate`
- `TransactionUpdate` → `PaymentsApiPaymentTransactions.TransactionUpdate_Adhoc`
- `LoadScript` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `RadioButtonChange` → `PaymentsApiSetup.BeneficiaryGetList`

## AttachmentsAndNotes  ·  title: Attachments And Notes  ·  roles: —
  - Link: `CancelLink` — "Cancel"
  - UploadFile: `UploadFile`
  - DataGrid: `AttachmentsDataGrid`
    - columns (in order): "Delete"(action), "Id"(hidden), `FileName` "File Name", `FileLocation` "File Location" [from design model]
  - Button: `AddNoteButton` — "Add Note"
  - DataGrid: `NoteDataGrid`
    - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Note" [from design model]
  - TextBox: `NoteTextBox`  ·  hint: "Please enter a note" · multi-line (8 rows)
  - Button: `NoteCancelButton` — "Cancel"
  - Button: `NoteEditSaveButton` — "Save"
  - Button: `NoteAddSaveButton` — "Save"
  - Panel: `DuplicateTransactionPanel` — "Review the payment history below to ensure you're not creating a duplicate payment."
    - DataGrid: `DuplicateTransactionDataGrid`
      - columns (in order): `BusinessUnit` "Business Unit", "Department", `ExecutionDate` "Execution Date", `BankAccount` "Bank Account", "Currency", "Amount", `TransactionType` "Transaction Type", `PaymentReference` "Payment Reference", `PaymentReason` "Payment Reason", `BeneficiaryName` "Beneficiary Name", `BeneficiarySortCode` "Beneficiary Sort Code", `BeneficiaryAccountNumber` "Beneficiary Account Number" [from design model]
    - Button: `ProceedButton` — "Proceed"
    - Button: `CancelDuplicateTransactionButton` — "Cancel"
  - Button: `BackButton` — "Back"
  - Button: `SaveDraftButton` — "Save Draft"
  - Button: `NextButton` — "Next"
- Visible terms: "Attachments and Notes", "Upload Attachments", "Notes", "Note", "Existing Duplicate Transaction", "Newly captured Transaction", "Business Unit", "Department", "Execution Date", "Bank Account", "Currency", "Amount", "Transaction Type", "Payment Reference", "Payment Reason", "Beneficiary", "Beneficiary Sort Code", "Beneficiary Account Number" [from design model]
> Layout: 16 meaningful control(s) within 127 layout container(s); max control-tree nesting depth 21 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — AttachmentsAndNotes (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `CancelLink` → `PaymentsApiPaymentTransactions.TransactionDelete`
- `UploadFile` → `FileSystem.WriteFile`
- `UploadFile` → `PaymentsApiPaymentTransactions.TransactionSupportingDocumentCreate`
- `AttachmentsDataGrid` → `PaymentsApiPaymentTransactions.TransactionSupportingDocumentDelete`
- `AttachmentsDataGrid` → `FileSystem.DeleteFile`
- `NoteDataGrid` → `PaymentsApiPaymentTransactions.TransactionNoteDelete`
- `NoteEditSaveButton` → `PaymentsApiPaymentTransactions.TransactionNoteUpdate`
- `NoteAddSaveButton` → `PaymentsApiPaymentTransactions.TransactionNoteCreate`
- `CancelDuplicateTransactionButton` → `PaymentsApiPaymentTransactions.TransactionDelete`
- `SaveDraftButton` → `PaymentsApiPaymentTransactions.TransactionUpdate`
- `NextButton` → `PaymentsApiPaymentTransactions.TransactionUpdate`
- `AttachmentsAndNotes` → `PaymentsApiPaymentTransactions.DuplicateTransactionGetList`
- `AttachmentsAndNotes` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `RefreshNoteGrid` → `PaymentsApiPaymentTransactions.TransactionNoteGetList`
- `RefreshAttachementGrid` → `PaymentsApiPaymentTransactions.TransactionSupportingDocumentGetList`

## Review  ·  title: Review  ·  roles: —
  - Panel: `PaymentSummaryPanel` — "Payment Summary"
  - Panel: `TransactionCodingPanel` — "Transaction Coding"
  - Panel: `BeneficiaryDetailsPanel` — "Beneficiary Details"
  - Panel: `AttachementsAndNotesPanel` — "Attachments And Notes"
    - DataGrid: `AttachmentDataGrid`
      - columns (in order): `FileName` "File Name" [from design model]
    - DataGrid: `NoteDataGrid`
      - columns (in order): "Note" [from design model]
  - Button: `BackButton` — "Back"
  - Button: `SaveDraftButton` — "Save Draft"
  - Button: `SubmitButton` — "Submit"
- Visible terms: "Review", "Amount", "Payment Method", "Execution Date", "Payment Reference", "Business Unit", "Transaction Coding", "Cost Centre", "Pay from account", "Type", "Name", "Bank", "Pay To Account", "Attachments", "Notes" [from design model]
> Layout: 9 meaningful control(s) within 87 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — Review (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `Review` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `Review` → `PaymentsApiSetup.BeneficiaryGetById`
- `Review` → `PaymentsApiPaymentTransactions.TransactionSupportingDocumentGetList`
- `Review` → `PaymentsApiPaymentTransactions.TransactionNoteGetList`
- `TransactionUpdate` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `TransactionUpdate` → `PaymentsApiPaymentTransactions.TransactionUpdate`

## ApprovalLevels  ·  title: Approval Levels  ·  roles: —
  - DataGrid: `ApprovalLevelDataGrid`  ·  grid: searchable
    - columns (in order): "Edit"(action), "Delete"(action), `BusinessUnit` "Business Unit", "Department", `TransactionType` "Transaction Type", `BusinessUnitId` "Business Unit Id"(hidden), `DepartmentId` "Department Id"(hidden), `TransactionTypeId` "Transaction Type Id"(hidden), `ViewApprovalLevelAmounts` "View Approval Level Amounts"(action) [from design model]
  - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
  - DropDown: `DepartmentDropDown`  ·  hint: "Select a department" · dynamic choices (bound)
  - DropDown: `TransactionTypeDropDown`  ·  hint: "Select a transaction type" · dynamic choices (bound)
  - TextBox: `MaxApprovalAmountTextBox`
  - Button: `CancelButton` — "Cancel"
  - Button: `CreateApprovalLevelButton` — "Create Approval Level"
  - DataGrid: `AmountDataGrid`
    - columns (in order): "Delete"(action), "Amounts", `ApprovalLevelId` "Approval Level Id"(hidden), `BusinessUnitId` "Business Unit Id"(hidden), `DepartmentId` "Department Id"(hidden), `TransactionTypeId` "Transaction Type Id"(hidden) [from design model]
  - Button: `CancelViewApprovedLevelAmountsButton` — "Cancel"
- Visible terms: "Approval Levels", "Business Unit", "Department", "Transaction Type", "Amount Limit" [from design model]
> Layout: 9 meaningful control(s) within 63 layout container(s); max control-tree nesting depth 18 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — ApprovalLevels (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `ApprovalLevelDataGrid` → `PaymentsApiPaymentApprovals.ApprovalLevelAmountGetList`
- `ApprovalLevelDataGrid` → `PaymentsApiPaymentApprovals.ApprovalLevelDelete`
- `BusinessUnitDropDown` → `PaymentsApiSetup.BusinessUnitDepartmentGetListById`
- `AmountDataGrid` → `PaymentsApiPaymentApprovals.ApprovalLevelAmountDelete`
- `RefreshApprovalLevels` → `PaymentsApiPaymentApprovals.DistinctApprovalLevelGetList`
- `LoadDropDowns` → `PaymentsApiSetup.BusinessUnitGetList`
- `LoadDropDowns` → `PaymentsApiSetup.BusinessUnitDepartmentGetListById`
- `LoadDropDowns` → `PaymentsApiPaymentTransactions.TransactionTypeGetList`
- `CreateAndEditApprovalLevelScript` → `PaymentsApiPaymentApprovals.ApprovalLevelCreate`
- `CreateAndEditApprovalLevelScript` → `PaymentsApiPaymentApprovals.ApprovalLevelUpdate`
- `RefreshApprovalLevelAmountDatagrid` → `PaymentsApiPaymentApprovals.ApprovalLevelAmountGetList`

## UserApprovalLevels  ·  title: User Approval Levels  ·  roles: —
  - DataGrid: `ParentDataGrid`  ·  grid: searchable
    - columns (in order): `BusinessUnitId` "Business Unit Id"(hidden), `BusinessUnit` "Business Unit", `DepartmentId` "Department Id"(hidden), "Department", `TransactionTypeId` "Transaction Type Id"(hidden), `TransactionType` "Transaction Type", `MaxApprovalAmounts` "Assign Approval Amounts"(action) [from design model]
  - DataGrid: `ChildDataGrid`
    - columns (in order): `MaxApprovalAmount` "Max Approval Amount", `ApprovalLevelId` "Approval Level Id"(hidden), "Status", "Assign"(action), "Unassign"(action), `BusinessUnitId` "Business Unit Id"(hidden), `DepartmentId` "Department Id"(hidden), `TransactionTypeId` "Transaction Type Id"(hidden) [from design model]
  - Button: `CancelChildGridPopupButton` — "Cancel"
- Visible terms: "Assign Approval Level Amounts" [from design model]
> Layout: 3 meaningful control(s) within 22 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — UserApprovalLevels (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `ChildDataGrid` → `PaymentsApiPaymentApprovals.UserApprovalLevelCreate`
- `ChildDataGrid` → `PaymentsApiPaymentApprovals.UserApprovalLevelDelete`
- `UserApprovalLevels` → `PaymentsApiPaymentApprovals.UserApprovalLevelGetListByBusinessUnitIdUserId`
- `RefreshChildDataGrid` → `PaymentsApiPaymentApprovals.UserApprovalLevelAmountGetList`

## ApprovalLevelRules  ·  title: Approval Level Rules  ·  roles: —
  - DataGrid: `ApprovalLevelRulesDataGrid`  ·  grid: searchable
    - columns (in order): `BusinessUnit` "Business Unit", "Department", `TransactionType` "Transaction Type", `BusinessUnitId` "Business Unit Id"(hidden), `DepartmentId` "Department Id"(hidden), `TransactionTypeId` "Transaction Type Id"(hidden), `ViewApprovalLevelRules` "View Approval Level Rules"(action), `EditApprovalLevelRules` "Edit Approval Level Rules"(action) [from design model]
  - TextBox: `ApprovalLevelId`  ·  read-only
  - TextBox: `ApprovalAmount`  ·  read-only
  - TextBox: `ManagerialApproval`
  - TextBox: `TreasuryApproval`
  - TextBox: `BankReleaseApproval`
  - Button: `EditCancelButton` — "Cancel"
  - Button: `EditSaveApprovalLevelRulesButton` — "Save"
  - DataGrid: `ViewApprovalLevelRulesDataGrid`
    - columns (in order): `ApprovalLevelAmount` "Approval Level Amount", `ManagerialApproval` "Managerial Approval", `TreasuryApproval` "Treasury Approval", `BankReleaseApproval` "Bank Release Approval" [from design model]
  - Button: `CancelButton` — "Cancel"
- Visible terms: "Approval Level Rules" [from design model]
> Layout: 10 meaningful control(s) within 50 layout container(s); max control-tree nesting depth 18 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — ApprovalLevelRules (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `ApprovalLevelRulesDataGrid` → `PaymentsApiPaymentApprovals.ApprovalLevelRuleGetList`
- `EditSaveApprovalLevelRulesButton` → `PaymentsApiPaymentApprovals.ApprovalLevelRulesUpdate`
- `RefreshApprovalLevelRules` → `PaymentsApiPaymentApprovals.DistinctApprovalLevelGetList`

## User tasks (per view)

> The per-view user-task inventory — the verb-labelled action affordances triangulated with wired backend operations, DataGrids and page-kinds, with a ≥1-task-per-view completeness guarantee — is emitted as its own asset: see `PaymentsApp.stadium.tasks.md`.

## Tier-A — screen ↔ entity (best-effort)

| Page | Likely entity |
|---|---|
| Roles | Role |
| Users | User |
| CostCentres | CostCentre |
| BusinessUnits | BusinessUnit |
| Beneficiaries | — |
| Banks | Bank |
| BankAccounts | Bank |
| BankPaymentSetup | Bank |
| Department | BusinessUnitDepartment |
| PaymentReason | PaymentReason |
| PaymentEnquiries | — |
| PaymentDetails | — |
| PaymentSetup | BankPaymentSetup |
| DraftManualPaymentCapture | — |
| TransactionCoding | Transaction |
| PaymentsDetails | — |
| BeneficiaryDetails | Beneficiary |
| AttachmentsAndNotes | — |
| Review | — |
| ApprovalLevels | ApprovalLevel |
| UserApprovalLevels | ApprovalLevel |
| ApprovalLevelRules | ApprovalLevel |
