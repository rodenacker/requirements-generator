---
stadium_asset: surfaces
app: PaymentsApp
file_guid: be54c8c9-dc03-43d5-bc2b-fba14e07f360
designer_version: 6.14.3378.13771
selected_package: 2211275f-1cb9-495c-91cf-4ff48dc4c142.sapz
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

## Roles  ·  title: Roles  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `HeadingLabel` — "Roles"
    - StackLayout: `StackLayout`
      - Button: `SyncRolesButton` — "Sync Stadium Roles"
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `RolesDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Id"(hidden), `Name` "Role" [from design model]

### source-UI reference — Roles (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `SyncRolesButton` → `PaymentsApiUsers.RoleSync`
- `SyncRolesButton` → `PaymentsApiUsers.RoleGetList`
- `Roles` → `PaymentsApiUsers.RoleGetList`

## Users ⭐ start  ·  title: Users  ·  roles: User
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `HeadingLabel` — "Users"
    - StackLayout: `StackLayout`
      - Button: `AddUserButton` — "Add User"
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `UsersDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Edit"(action), "Delete"(action), `ViewAssignedApprovalLevels` "View Assigned Approval Levels"(action), `AssignApprovalLevels` "Assign Approval Levels", "Id"(hidden), `StadiumUserId` "Stadium User Id"(hidden), "Email", `FirstName` "First Name", `LastName` "Last Name", `IsAdministrator` "Is Administrator", `RolesString` "Roles", "Roles"(hidden), `BusinessUnit` "Business Unit", `BusinessUnitId` "Business Unit Id"(hidden), `BusinessUnitDepartmentString` "Department", `BusinessUnitDepartments` "Business Unit Departments"(hidden), `LastChangedUser` "Last Changed User", `LastChangedDate` "Last Changed Date" [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `Grid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IdLabel`
                    - CellGridLayout: `CellGridLayout`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `EmailLabel` — "Email"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `EmailTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `FirstNameLabel` — "First Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `FirstNameTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `LastNameLabel` — "Last Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `LastNameTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IsAdministratorLabel` — "Administrator"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - CheckBox: `IsAdministartorCheckBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PasswordLabel` — "Password"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `PasswordTextBox`  ·  password-masked
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitsLabel` — "BusinessUnits"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitDepartmentsLabel` — "Departments"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - CheckBoxList: `BusinessUnitDepartmentsCheckBoxList`  ·  dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `RolesLabel` — "Roles"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - CheckBoxList: `RolesCheckBoxList`  ·  dynamic choices (bound)
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `EditSaveButton` — "Save"
                        - Button: `AddSaveButton` — "Save"
      - Container: `ModalBackgroundContainerViewAssignedApprovalLevels`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainerViewAssignedApprovalLevel`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabelViewAssignedApprovalLevels`
                - StackLayout: `StackLayout`
                  - DataGrid: `ViewAssignedApprovalLevelsDataGrid`
                    - columns (in order): `BusinessUnitId` "Business Unit Id"(hidden), `BusinessUnit` "Business Unit", "Department", `DepartmentId` "Department Id"(hidden), `TransactionTypeId` "Transaction Type Id"(hidden), `TransactionType` "Transaction Type", `MaxApprovalAmount` "Max Approval Amount" [from design model]
                - StackLayout: `StackLayout`
                  - Container: `Container1`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelViewApprovedLevelsButton` — "Cancel"

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
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Cost Centres"
            - Button: `AddCostCentreButton`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `CostCentreDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name", "Description", `BusinessUnit` "Business Unit", `BusinessUnitId` "Business Unit Id"(hidden), "BusinessUnitDepartments"(hidden), `BusinessUnitDepartmentString` "Departments" [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `AddUserGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IdLabel`
                    - CellGridLayout: `CellGridLayout`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `NameLabel` — "Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `NameTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `DescriptionLabel` — "Description"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `DescriptionTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitsLabel` — "BusinessUnits"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitDepartmentsLabel` — "Departments"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - CheckBoxList: `BusinessUnitDepartmentsCheckBoxList`  ·  dynamic choices (bound)
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `EditSaveButton` — "Save"
                        - Button: `AddSaveButton` — "Save"

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
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Business Units"
            - Button: `AddBusinessUnitButton`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `BusinessUnitDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name"(hidden), "Description", "Code", `DepartmentString` "Transaction types", "Departments"(hidden) [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `Grid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IdLabel`
                    - CellGridLayout: `CellGridLayout`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `NameLabel` — "Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `NameTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `DescriptionLabel` — "Description"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `DescriptionTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `CodeLabel` — "Code"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `CodeTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `DepartmentsLabel` — "Departments"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - CheckBoxList: `DepartmentsCheckBoxList`  ·  dynamic choices (bound)
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `EditSaveButton` — "Save"
                        - Button: `AddSaveButton` — "Save"

### source-UI reference — BusinessUnits (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `BusinessUnitDataGrid` → `PaymentsApiSetup.BusinessUnitGetById`
- `BusinessUnitDataGrid` → `PaymentsApiSetup.BusinessUnitDelete`
- `EditSaveButton` → `PaymentsApiSetup.BusinessUnitUpdate`
- `AddSaveButton` → `PaymentsApiSetup.BusinessUnitCreate`
- `RefreshBusinessUnits` → `PaymentsApiSetup.BusinessUnitGetList`
- `LoadDepartmentCheckboxListOptions` → `PaymentsApiSetup.DepartmentGetList`

## Beneficiaries  ·  title: Users  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Beneficiaries"
            - Button: `AddBeneficiaryButton`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `BeneficiaryDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name"(hidden), `AccountName` "Account Name", `AccountNumber` "Account Number", `BankAccountTypeName` "Bank Account Type", `BankName` "Bank", "IBAN", `BankId` "Bank Id"(hidden), `BankAccountTypeId` "Bank Account Type Id"(hidden), `BusinessUnitId`(hidden), `BusinessUnit` "Business Unit", `BusinessUnitDepartments` "Business Unit Departments"(hidden), `BusinessUnitDepartmentString` "Departments" [from design model]
          - ⚠ `BusinessUnitId` header resolves to "Business Unit " (design header is an unresolved binding) [from rendered view]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `AddBeneficiaryGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IdLabel`
                    - CellGridLayout: `CellGridLayout`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `NameLabel` — "Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `NameTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `AccountNameLabel` — "Account Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `AccountNameTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `AccountNumberLabel` — "Account Number"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `AccountNumberTextBox`  ·  hint: "Only numbers are allowed"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `AccountTypeLabel` — "Account Type"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `AccountTypeDropDown`  ·  hint: "Select an account type" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BankLabel` — "Bank"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BankDropDown`  ·  hint: "Select a bank" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IBANLabel`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `IbanTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitsLabel` — "Business Unit"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitDepartmentsLabel` — "Departments"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - CheckBoxList: `BusinessUnitDepartmentsCheckBoxList`  ·  dynamic choices (bound)
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `EditSaveButton` — "Save"
                        - Button: `AddSaveButton` — "Save"

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
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Banks"
            - Button: `AddBankButton`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `BankDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name", `UniversalBranchCode` "Universal Branch Code", `UniversalSwiftCode` "Universal Swift Code" [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `AddUserGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IdLabel`
                    - CellGridLayout: `CellGridLayout`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `NameLabel` — "Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `NameTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `UniversalBranchCodeLabel` — "Universal Branch Code"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `UniversalBranchCodeTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `UniversalSwiftCodeLabel` — "Universal Swift Code"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `UniversalSwiftCodeTextBox`
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `EditSaveButton` — "Save"
                        - Button: `AddSaveButton` — "Save"

### source-UI reference — Banks (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `BankDataGrid` → `PaymentsApiSetup.BankGetById`
- `BankDataGrid` → `PaymentsApiSetup.BankDelete`
- `EditSaveButton` → `PaymentsApiSetup.BankUpdate`
- `AddSaveButton` → `PaymentsApiSetup.BankCreate`
- `RefreshBank` → `PaymentsApiSetup.BankGetList`

## BankAccounts  ·  title: Users  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Bank Accounts"
            - Button: `AddBankAccountButton`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `BankAccountDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), `AccountName` "Account Name", `AccountNumber` "Account Number", `BankAccountTypeName` "Bank Account Type", `BankAccountTypeId` "Bank Account Type Id"(hidden), "IBAN", `BankName` "Bank", `BankId` "Bank Id"(hidden), `BusinessUnit` "Business Unit", `BusinessUnitId` "Business Unit Id"(hidden) [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `Grid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IdLabel`
                    - CellGridLayout: `CellGridLayout`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `AccountNameLabel` — "Account Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `AccountNameTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `AccountNumberLabel` — "Account Number"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `AccountNumberTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `AccountTypeLabel` — "Account Type"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `AccountTypeDropDown`  ·  hint: "Select an Account type" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BankLabel` — "Bank"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BankDropDown`  ·  hint: "Select a Bank" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IbanLabel` — "IBAN"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `IbanTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitLabel` — "Business Unit"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a Business unit" · dynamic choices (bound)
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `EditSaveButton` — "Save"
                        - Button: `AddSaveButton` — "Save"

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
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Bank Payment Setup"
            - Button: `AddBankPaymentSetupButton`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `BankPaymentSetupDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Bank", `PaymentMethod` "Payment Method", `TransferMethod` "Transfer Method", `ServiceLevelCode` "Service Level Code", `ChargeBearer` "Charge Bearer", `CutOffTime` "Cut Off Time", `ApiEnabled` "Api Enabled" [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `AddBeneficiaryGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IdLabel`
                    - CellGridLayout: `CellGridLayout`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BankNameLabel` — "Bank"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BankDropDown`  ·  hint: "Select a bank" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BankPaymentMethodLabel` — "Bank Payment Method"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BankPaymentMethodDropDown`  ·  hint: "Select a payment method" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `TransferMethodLabel` — "Transfer Method"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `TransferMethodDropDown`  ·  hint: "Select a transfer method" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `ServiceLevelCodeLabel` — "Service Level Code"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `ServiceLevelCodeDropDown`  ·  hint: "Select a service level code" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `ChargeBearerLabel` — "Charge Bearer"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `ChargeBearerDropDown`  ·  hint: "Select a charge bearer" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `CutOffTimeLabel` — "Cut Off Time"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `CutOffTimeTextBox`  ·  hint: "Please provide time in format hh:mm"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `ApiEnabledLabel` — "Api Enabled"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - CheckBox: `ApiEnabledCheckBox`
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `EditSaveButton` — "Save"
                        - Button: `AddSaveButton` — "Save"

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
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel`
            - Button: `AddDepartmentButton`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `DepartmentDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name", "Description" [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `AddDepartmentGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IdLabel`
                    - CellGridLayout: `CellGridLayout`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `NameLabel` — "Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `NameTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `DescriptionLabel` — "Description"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `DescriptionTextBox`
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `EditSaveButton` — "Save"
                        - Button: `AddSaveButton` — "Save"

### source-UI reference — Department (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `DepartmentDataGrid` → `PaymentsApiSetup.DepartmentGetById`
- `DepartmentDataGrid` → `PaymentsApiSetup.DepartmentDelete`
- `EditSaveButton` → `PaymentsApiSetup.DepartmentUpdate`
- `AddSaveButton` → `PaymentsApiSetup.DepartmentCreate`
- `RefreshDepartmentSetup` → `PaymentsApiSetup.DepartmentGetList`

## PaymentReason  ·  title: Users  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel`
            - Button: `AddPaymentReasonButton`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `PaymentReasonDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Name", "Description", "Code" [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `AddPaymentReasonGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IdLabel`
                    - CellGridLayout: `CellGridLayout`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `NameLabel` — "Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `NameTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `DescriptionLabel` — "Description"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `DescriptionTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `CodeLabel` — "Code"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `CodeTextBox`
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `EditSaveButton` — "Save"
                        - Button: `AddSaveButton` — "Save"

### source-UI reference — PaymentReason (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `PaymentReasonDataGrid` → `PaymentsApiPaymentTransactions.PaymentReasonGetById`
- `PaymentReasonDataGrid` → `PaymentsApiPaymentTransactions.PaymentReasonDelete`
- `EditSaveButton` → `PaymentsApiPaymentTransactions.PaymentReasonUpdate`
- `AddSaveButton` → `PaymentsApiPaymentTransactions.PaymentReasonCreate`
- `RefreshPaymentReason` → `PaymentsApiPaymentTransactions.PaymentReasonGetList`

## PaymentEnquiries  ·  title: Payment Enquiries  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `HeadingLabel` — "Payment Enquiries"
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - Container: `FilterContainer`
        - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Button: `ApplyFilterButton` — "Apply Filters"
      - Button: `ClearFilterButton` — "Clear Filters"
    - StackLayout: `StackLayout`
      - DataGrid: `PaymentEnquiryDataGrid`
        - columns (in order): `PaymentDetail` "Payment Detail"(action), `TrackingNumber` "Tracking Number", "Status", `DateCreated` "Date Created", `RequestedBy` "Requested By", `BusinessUnit` "Business Unit", `TransactionType` "Transaction Type", `BankPaymentMethod` "Bank Payment Method", `BeneficiaryName` "Beneficiary", `PaymentReference` "Payment Reference", `ExecutionDate` "Execution Date", "Currency", "Amount" [from design model]
    - StackLayout: `StackLayout`
      - Label: `DataLabel`

### source-UI reference — PaymentEnquiries (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `PaymentEnquiries` → `PaymentsApiPaymentTransactions.TransactionGetList`
- `PaymentEnquiries` → `PaymentsApiPaymentTransactions.TransactionTypeGetList`
- `PaymentEnquiries` → `PaymentsApiSetup.BusinessUnitGetList`

## PaymentDetails  ·  title: Payment Details  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `HeadingLabel` — "Payment Details"
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - Link: `BackToPaymentEnquiryPageLink`
    - StackLayout: `StackLayout`
      - Panel: `Panel` — "Payment Summary"
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Grid: `Grid`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `AmountLabel` — "Amount"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `BeneficiaryLabel` — "Beneficiary"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `RequestedByLabel` — "Requested By"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `AmountValueLabel`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `BeneficiaryValueLabel`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `RequestedByValueLabel`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `StatusLabel` — "Status"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `BankPaymentMethodLabel` — "Bank Payment Method"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `PaymentReferenceLabel` — "PaymentReference"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `StatusValueLabel`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `BankPaymentMethodValueLabel`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `PaymentReferenceValueLabel`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `TransactionTypeLabel` — "Transaction Type"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `BusinessUnitLabel` — "Business Unit"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `DateCreatedLabel` — "Date Created"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `TransactionTypeValueLabel`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `BusinessUnitValueLabel`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `DateCreatedValueLabel`
    - StackLayout: `StackLayout`
      - Container: `Container`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `AuditLogLabel` — "Audit Log"
            - Label: `NotesLabel` — "Notes"
            - Label: `SupportingDocumentsLabel` — "Supporting Documents"
          - StackLayout: `StackLayout`
            - Container: `AuditLogsContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `AuditLogHeaderLabel` — "Payment Audit Log"
            - Container: `NotesContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `NotesHeaderLabel` — "Payment Notes"
                - StackLayout: `StackLayout`
                  - DataGrid: `NotesDataGrid`
                    - columns (in order): "Notes", "User", `DateCreated` "Date Created" [from design model]
            - Container: `SupportingDocumentsContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `SupportingDocumentsHeaderLabel` — "Payment Supporting Documents"
                - StackLayout: `StackLayout`
                  - DataGrid: `SupportingDocumentsDataGrid`
                    - columns (in order): "Document", "User", `DateCreated` "Date Created", "Download"(action), `FileLocation` "File Location"(hidden) [from design model]

### source-UI reference — PaymentDetails (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `SupportingDocumentsDataGrid` → `FileSystem.ReadFile`
- `PaymentDetails` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `PaymentDetails` → `PaymentsApiPaymentTransactions.TransactionNoteGetList`
- `PaymentDetails` → `PaymentsApiPaymentTransactions.TransactionSupportingDocumentGetList`

## PaymentSetup  ·  title: Payment Setup  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Payment Setup"
            - Button: `AddPaymentSetupButton`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `PaymentSetupDataGrid`  ·  grid: exportable / searchable
        - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), `BusinessUnit` "Business Unit", "Department", `TransactionType` "Transaction Type", `PaymentMethod` "Payment Method", `PaymentReason` "Payment Reason", `BankAccount` "Bank Account" [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `AddPaymentSetupGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `IdLabel`
                    - CellGridLayout: `CellGridLayout`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitLabel` — "BusinessUnit"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `DepartmentLabel` — "Department"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `DepartmentDropDown`  ·  dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `TransactionTypeLabel` — "Transaction Type"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `TransactionTypeDropDown`  ·  hint: "Select a transaction type" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PaymentMethodLabel` — "Payment Method"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `PaymentMethodDropDown`  ·  hint: "Select a payment method" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PaymentReasonLabel` — "Payment Reason"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `PaymentReasonDropDown`  ·  hint: "Select a payment reason" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BankAccountLabel` — "Bank Account"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BankAccountDropDown`  ·  hint: "Select a bank account" · dynamic choices (bound)
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `EditSaveButton` — "Save"
                        - Button: `AddSaveButton` — "Save"

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
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `HeadingLabel` — "Draft Transactions"
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `DraftTransactionsDataGrid`
        - columns (in order): "Detail"(action), "Edit"(action), `TrackingNumber` "Tracking Number", `TransactionManualCaptureStepId` "Transaction Manual Capture Step Id"(hidden), `TransactionManualCaptureStep` "Last saved step", `DateCreated` "Date Created", `RequestedBy` "Requested By", `BusinessUnit` "Business Unit", `TransactionType` "Transaction Type", `BankPaymentMethod` "Bank Payment Method", `BeneficiaryName` "Beneficiary", `PaymentReference` "Payment Reference", `ExecutionDate` "Execution Date", "Currency", "Amount", "Delete"(action) [from design model]

### source-UI reference — DraftManualPaymentCapture (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `DraftTransactionsDataGrid` → `PaymentsApiPaymentTransactions.TransactionDelete`
- `RefreshDraftPayments` → `PaymentsApiPaymentTransactions.DraftTransactionGetList`

## TransactionCoding  ·  title: Transaction Coding  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container`
        - GridLayout: `GridLayout`
      - Container: `Container3`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Transaction Coding"
          - StackLayout: `StackLayout`
            - Label: `TrackingNumberText`
            - Label: `TrackingNumberValue`
          - StackLayout: `StackLayout`
            - Label: `Label`
          - StackLayout: `StackLayout`
            - Flexbox: `Flexbox`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PageDescriptionLabel`
                  - Container: `Container4`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Link: `CancelLink` — "Cancel"
          - StackLayout: `StackLayout`
            - Container: `Container1`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Grid: `Grid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitLabel` — "Business Unit"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitDepartmentLabel` — "Department"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BusinessUnitDepartmentDropDown`  ·  hint: "Select a department" · read-only · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `TransactionTypeLabel` — "Transaction Type"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `TransactionTypeDropDown`  ·  hint: "Select a transaction type" · read-only · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BankAccountLabel` — "Bank Account"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BankAccountDropDown`  ·  hint: "Select a bank account" · read-only · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BankPaymentMethodLabel` — "Bank Payment Method"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BankPaymentMethodDropDown`  ·  hint: "Select a bank payment method" · read-only · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PaymentReasonLabel` — "Payment Reason"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `PaymentReasonDropDown`  ·  hint: "Select a payment reason" · read-only · dynamic choices (bound)
                - StackLayout: `StackLayout`
                  - Container: `Container2`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `SaveDraftButton` — "Save Draft"
                        - Button: `NextButton` — "Next"

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
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container`
        - GridLayout: `GridLayout`
      - Container: `Container3`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Payment Details"
          - StackLayout: `StackLayout`
            - Label: `TrackingNumberText`
          - StackLayout: `StackLayout`
            - Label: `Label`
          - StackLayout: `StackLayout`
            - Flexbox: `Flexbox1`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PageDescriptionLabel`
                  - Container: `Container5`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Link: `CancelLink` — "Cancel"
          - StackLayout: `StackLayout`
            - Container: `Container1`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Grid: `Grid1`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `AmountLabel` — "Amount"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `AmountTextBox`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `CurrencyTypeLabel` — "Currency"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `CurrencyTypeDropDown`  ·  hint: "Select a currency" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `ExecutionDateLabel` — "Execution Date"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DatePicker: `ExecutionDatePicker`  ·  hint: "Select a date"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PaymentReferenceLabel` — "Payment Reference"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - TextBox: `PaymentReferenceTextBox`
                - StackLayout: `StackLayout`
                  - Container: `Container2`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `BackButton` — "Back"
                        - Button: `SaveDraftButton` — "Save Draft"
                        - Button: `NextButton` — "Next"

### source-UI reference — PaymentsDetails (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `CancelLink` → `PaymentsApiPaymentTransactions.TransactionDelete`
- `SaveDraftButton` → `PaymentsApiPaymentTransactions.TransactionUpdate`
- `NextButton` → `PaymentsApiPaymentTransactions.TransactionUpdate`
- `PaymentsDetails` → `PaymentsApiSetup.LookupDataGetList`
- `PaymentsDetails` → `PaymentsApiPaymentTransactions.TransactionGetById`

## BeneficiaryDetails  ·  title: Beneficiary Details  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container`
        - GridLayout: `GridLayout`
      - Container: `Container3`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Beneficiary Details"
          - StackLayout: `StackLayout`
            - Label: `TrackingNumberText`
          - StackLayout: `StackLayout`
            - Label: `Label`
          - StackLayout: `StackLayout`
            - Flexbox: `Flexbox1`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PageDescriptionLabel`
                  - Container: `Container2`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Link: `CancelLink` — "Cancel"
          - StackLayout: `StackLayout`
            - RadioButtonList: `WhitelistAndAdhocRadioButtonList`  ·  choices: "WhiteListed", "Ad-hoc"
          - StackLayout: `StackLayout`
            - DataGrid: `WhitelistedBeneficiaryDataGrid`
              - columns (in order): "Select"(action), "Id"(hidden), "Name", "Bank", `Account` "Account Details", `AccountNumber` "Account Number"(hidden) [from design model]
            - Label: `SelectedDatagridRowIdLabel`
          - StackLayout: `StackLayout`
            - Label: `AdhocBeneficiaryLabel` — "Create an Adhoc Beneficiary"
          - StackLayout: `StackLayout`
            - Grid: `AdhocBeneficiaryGrid`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `NameLabel` — "Name"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - TextBox: `NameTextBox`
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `AccountNumber` — "Account Number"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - TextBox: `AccountNumberTextBox`  ·  hint: "Please enter a numeric value (16 digits)"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - Label: `SortCode` — "Sort Code"
              - CellGridLayout: `CellGridLayout`
                - CellStackLayout: `CellStackLayout`
                  - TextBox: `SortCodeTextBox`  ·  hint: "Please provide a numeric value (6 digits)"
          - StackLayout: `StackLayout`
            - Flexbox: `Flexbox`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Container: `Container1`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `BackButton` — "Back"
                        - Button: `SaveDraftButton` — "Save Draft"
                        - Button: `NextButton` — "Next"

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
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container4`
        - GridLayout: `GridLayout`
      - Container: `Container`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Attachments and Notes"
          - StackLayout: `StackLayout`
            - Label: `TrackingNumberText`
          - StackLayout: `StackLayout`
            - Label: `Label`
          - StackLayout: `StackLayout`
            - Flexbox: `Flexbox`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PageDescriptionLabel`
                  - Container: `Container1`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Link: `CancelLink` — "Cancel"
          - StackLayout: `StackLayout`
            - Flexbox: `AttachementFlexbox`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `UploadAttachementsLabel` — "Upload Attachments"
                  - UploadFile: `UploadFile`
          - StackLayout: `StackLayout`
            - DataGrid: `AttachmentsDataGrid`
              - columns (in order): "Delete"(action), "Id"(hidden), `FileName` "File Name", `FileLocation` "File Location" [from design model]
          - StackLayout: `StackLayout`
            - Label: `GapLabel`
          - StackLayout: `StackLayout`
            - Flexbox: `NotesFlexbox`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `NotesLabel` — "Notes"
                  - Container: `Container3`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `AddNoteButton` — "Add Note"
          - StackLayout: `StackLayout`
            - DataGrid: `NoteDataGrid`
              - columns (in order): "Edit"(action), "Delete"(action), "Id"(hidden), "Note" [from design model]
          - StackLayout: `StackLayout`
            - Container: `ModalBackgroundContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Container: `ModalContentContainer`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Label: `PopupHeadingLabel`
                      - StackLayout: `StackLayout`
                        - Grid: `AddNoteGrid`
                          - CellGridLayout: `CellGridLayout`
                            - CellStackLayout: `CellStackLayout`
                              - Label: `IdLabel`
                          - CellGridLayout: `CellGridLayout`
                          - CellGridLayout: `CellGridLayout`
                            - CellStackLayout: `CellStackLayout`
                              - Label: `NoteLabel` — "Note"
                          - CellGridLayout: `CellGridLayout`
                            - CellStackLayout: `CellStackLayout`
                              - TextBox: `NoteTextBox`  ·  hint: "Please enter a note" · multi-line (8 rows)
                      - StackLayout: `StackLayout`
                        - Container: `Container2`
                          - GridLayout: `GridLayout`
                            - StackLayout: `StackLayout`
                              - Button: `NoteCancelButton` — "Cancel"
                              - Button: `NoteEditSaveButton` — "Save"
                              - Button: `NoteAddSaveButton` — "Save"
          - StackLayout: `StackLayout`
            - Container: `ModalBackgroundContainerDuplicate`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Container: `ModelContentContainer`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Panel: `DuplicateTransactionPanel` — "Review the payment history below to ensure you're not creating a duplicate payment."
                          - GridLayout: `GridLayout`
                            - StackLayout: `StackLayout`
                              - Label: `ExistingDuplicateTransactionHeadingLabel` — "Existing Duplicate Transaction"
                              - DataGrid: `DuplicateTransactionDataGrid`
                                - columns (in order): `BusinessUnit` "Business Unit", "Department", `ExecutionDate` "Execution Date", `BankAccount` "Bank Account", "Currency", "Amount", `TransactionType` "Transaction Type", `PaymentReference` "Payment Reference", `PaymentReason` "Payment Reason", `BeneficiaryName` "Beneficiary Name", `BeneficiarySortCode` "Beneficiary Sort Code", `BeneficiaryAccountNumber` "Beneficiary Account Number" [from design model]
                            - StackLayout: `StackLayout`
                              - Label: `NewTransactionbeingcapturedLabel` — "Newly captured Transaction"
                            - StackLayout: `StackLayout`
                              - Grid: `Grid`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `BusinessUnitLabel` — "Business Unit"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `DepartmentLabel` — "Department"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `ExecutionDateLabel` — "Execution Date"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `BankAccountLabel` — "Bank Account"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `CurrencyLabel` — "Currency"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `AmountLabel` — "Amount"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `TransactionTypeLabel` — "Transaction Type"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `PaymentReferenceLabel` — "Payment Reference"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `PaymentReasonLabel` — "Payment Reason"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `BeneficiaryNameLabel` — "Beneficiary"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `BeneficiarySortCodeLabel` — "Beneficiary Sort Code"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `BeneficiaryAccountNumberLabel` — "Beneficiary Account Number"
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `BusinessUnitValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `DepartmentValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `ExecutionDateValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `BankAccountValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `CurrencyValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `AmountValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `TransactionTypeValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `PaymentReferenceValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `PaymentReasonValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `BeneficiaryNameValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `BeneficiarySortCodeValueLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `BeneficiaryAccountNumberValueLabel`
                            - StackLayout: `StackLayout`
                              - Label: `DuplidateTransactionLabel`
                            - StackLayout: `StackLayout`
                              - Flexbox: `Flexbox1`
                                - GridLayout: `GridLayout`
                                  - StackLayout: `StackLayout`
                                    - Container: `Container7`
                                      - GridLayout: `GridLayout`
                                        - StackLayout: `StackLayout`
                                          - Button: `ProceedButton` — "Proceed"
                                          - Button: `CancelDuplicateTransactionButton` — "Cancel"
          - StackLayout: `StackLayout`
            - Flexbox: `Flexbox2`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Container: `Container5`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `BackButton` — "Back"
                        - Button: `SaveDraftButton` — "Save Draft"
                        - Button: `NextButton` — "Next"
      - Container: `Container6`
        - GridLayout: `GridLayout`

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
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container`
        - GridLayout: `GridLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Review"
          - StackLayout: `StackLayout`
            - Label: `TrackingNumberText`
          - StackLayout: `StackLayout`
            - Label: `Label`
          - StackLayout: `StackLayout`
            - Panel: `PaymentSummaryPanel` — "Payment Summary"
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Grid: `PaymentSummaryGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `AmountLabel` — "Amount"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `AmountValueLabel`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PaymentMethodLabel` — "Payment Method"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PaymentMethodValueLabel`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `ExecutionDateLabel` — "Execution Date"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `ExecutionDateValueLabel`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PaymentReferenceLabel` — "Payment Reference"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PaymentReferenceValueLabel`
          - StackLayout: `StackLayout`
            - Panel: `TransactionCodingPanel` — "Transaction Coding"
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Grid: `TransactionCodingGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitLabel` — "Business Unit"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitValueLabel`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `TransactionTypeLabel` — "Transaction Coding"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `TransactionTypeValueLabel`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `CostCentreLabel` — "Cost Centre"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `CostCentreValueLabel`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PayFromAccountLabel` — "Pay from account"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PayFromAccountValueLabel`
            - Panel: `BeneficiaryDetailsPanel` — "Beneficiary Details"
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Grid: `BeneficiaryDetailsGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `TypeLabel` — "Type"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `TypeValueLabel`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `NameLabel` — "Name"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `NameValueLabel`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BankLabel` — "Bank"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BankValueLabel`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PayToAccountLabel` — "Pay To Account"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `PayToAccountValueLabel`
          - StackLayout: `StackLayout`
            - Panel: `AttachementsAndNotesPanel` — "Attachments And Notes"
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Grid: `AttachementsAndNotesGrid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `AttachementLabel` — "Attachments"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DataGrid: `AttachmentDataGrid`
                          - columns (in order): `FileName` "File Name" [from design model]
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `NotesLabel` — "Notes"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DataGrid: `NoteDataGrid`
                          - columns (in order): "Note" [from design model]
          - StackLayout: `StackLayout`
            - Flexbox: `Flexbox`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Container: `Container2`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `BackButton` — "Back"
                        - Button: `SaveDraftButton` — "Save Draft"
                        - Button: `SubmitButton` — "Submit"

### source-UI reference — Review (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `Review` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `Review` → `PaymentsApiSetup.BeneficiaryGetById`
- `Review` → `PaymentsApiPaymentTransactions.TransactionSupportingDocumentGetList`
- `Review` → `PaymentsApiPaymentTransactions.TransactionNoteGetList`
- `TransactionUpdate` → `PaymentsApiPaymentTransactions.TransactionGetById`
- `TransactionUpdate` → `PaymentsApiPaymentTransactions.TransactionUpdate`

## ApprovalLevels  ·  title: Approval Levels  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Label: `HeadingLabel` — "Approval Levels"
            - Button: `AddApprovalLevelButton`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `ApprovalLevelDataGrid`  ·  grid: searchable
        - columns (in order): "Edit"(action), "Delete"(action), `BusinessUnit` "Business Unit", "Department", `TransactionType` "Transaction Type", `BusinessUnitId` "Business Unit Id"(hidden), `DepartmentId` "Department Id"(hidden), `TransactionTypeId` "Transaction Type Id"(hidden), `ViewApprovalLevelAmounts` "View Approval Level Amounts"(action) [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel`
                - StackLayout: `StackLayout`
                  - Grid: `Grid`
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `BusinessUnitLabel` — "Business Unit"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `BusinessUnitDropDown`  ·  hint: "Select a business unit" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `DepartmentLabel` — "Department"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `DepartmentDropDown`  ·  hint: "Select a department" · dynamic choices (bound)
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - Label: `TransactionTypeLabel` — "Transaction Type"
                    - CellGridLayout: `CellGridLayout`
                      - CellStackLayout: `CellStackLayout`
                        - DropDown: `TransactionTypeDropDown`  ·  hint: "Select a transaction type" · dynamic choices (bound)
                - StackLayout: `StackLayout`
                  - Flexbox: `Flexbox`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Label: `AmountLimitLabel` — "Amount Limit"
                        - Label: `AmountDescriptionLabel`
                - StackLayout: `StackLayout`
                  - Container: `DataGridContainer`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Grid: `Grid1`
                          - CellGridLayout: `CellGridLayout`
                            - CellStackLayout: `CellStackLayout`
                              - GridRepeater: `Repeater`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - Label: `LevelLabel`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - TextBox: `MaxApprovalAmountTextBox`
                          - CellGridLayout: `CellGridLayout`
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"
                        - Button: `CreateApprovalLevelButton` — "Create Approval Level"
                        - Button: `EditSaveApprovalLevelButton`
      - Container: `ModalBackgroundContainerViewApprovalLevelAmounts`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainerViewApprovalLevelAmounts`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabelViewApprovalLevelAmounts`
                - StackLayout: `StackLayout`
                  - DataGrid: `AmountDataGrid`
                    - columns (in order): "Delete"(action), "Amounts", `ApprovalLevelId` "Approval Level Id"(hidden), `BusinessUnitId` "Business Unit Id"(hidden), `DepartmentId` "Department Id"(hidden), `TransactionTypeId` "Transaction Type Id"(hidden) [from design model]
                - StackLayout: `StackLayout`
                  - Container: `Container2`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelViewApprovedLevelAmountsButton` — "Cancel"

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
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `HeadingLabel`
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - Container: `Container1`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - DataGrid: `ParentDataGrid`  ·  grid: searchable
              - columns (in order): `BusinessUnitId` "Business Unit Id"(hidden), `BusinessUnit` "Business Unit", `DepartmentId` "Department Id"(hidden), "Department", `TransactionTypeId` "Transaction Type Id"(hidden), `TransactionType` "Transaction Type", `MaxApprovalAmounts` "Assign Approval Amounts"(action) [from design model]
          - StackLayout: `StackLayout`
            - Link: `BackToUsersPageLink`
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingLabel` — "Assign Approval Level Amounts"
                - StackLayout: `StackLayout`
                  - DataGrid: `ChildDataGrid`
                    - columns (in order): `MaxApprovalAmount` "Max Approval Amount", `ApprovalLevelId` "Approval Level Id"(hidden), "Status", "Assign"(action), "Unassign"(action), `BusinessUnitId` "Business Unit Id"(hidden), `DepartmentId` "Department Id"(hidden), `TransactionTypeId` "Transaction Type Id"(hidden) [from design model]
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelChildGridPopupButton` — "Cancel"

### source-UI reference — UserApprovalLevels (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `ChildDataGrid` → `PaymentsApiPaymentApprovals.UserApprovalLevelCreate`
- `ChildDataGrid` → `PaymentsApiPaymentApprovals.UserApprovalLevelDelete`
- `UserApprovalLevels` → `PaymentsApiPaymentApprovals.UserApprovalLevelGetListByBusinessUnitIdUserId`
- `RefreshChildDataGrid` → `PaymentsApiPaymentApprovals.UserApprovalLevelAmountGetList`

## ApprovalLevelRules  ·  title: Approval Level Rules  ·  roles: —
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `HeadingLabel` — "Approval Level Rules"
    - StackLayout: `StackLayout`
      - Label: `PageDescriptionLabel`
    - StackLayout: `StackLayout`
      - Label: `Label`
    - StackLayout: `StackLayout`
      - DataGrid: `ApprovalLevelRulesDataGrid`  ·  grid: searchable
        - columns (in order): `BusinessUnit` "Business Unit", "Department", `TransactionType` "Transaction Type", `BusinessUnitId` "Business Unit Id"(hidden), `DepartmentId` "Department Id"(hidden), `TransactionTypeId` "Transaction Type Id"(hidden), `ViewApprovalLevelRules` "View Approval Level Rules"(action), `EditApprovalLevelRules` "Edit Approval Level Rules"(action) [from design model]
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainer`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainer`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeading`
                - StackLayout: `StackLayout`
                  - Container: `DataGridContainer`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Grid: `Grid1`
                          - CellGridLayout: `CellGridLayout`
                            - CellStackLayout: `CellStackLayout`
                              - GridRepeater: `Repeater`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - TextBox: `ApprovalLevelId`  ·  read-only
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - TextBox: `ApprovalAmount`  ·  read-only
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - TextBox: `ManagerialApproval`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - TextBox: `TreasuryApproval`
                                - CellGridLayout: `CellGridLayout`
                                  - CellStackLayout: `CellStackLayout`
                                    - TextBox: `BankReleaseApproval`
                          - CellGridLayout: `CellGridLayout`
                          - CellGridLayout: `CellGridLayout`
                          - CellGridLayout: `CellGridLayout`
                          - CellGridLayout: `CellGridLayout`
                - StackLayout: `StackLayout`
                  - Container: `Container`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `EditCancelButton` — "Cancel"
                        - Button: `EditSaveApprovalLevelRulesButton` — "Save"
    - StackLayout: `StackLayout`
      - Container: `ModalBackgroundContainerViewApprovalLevelRules`
        - GridLayout: `GridLayout`
          - StackLayout: `StackLayout`
            - Container: `ModalContentContainerViewApprovalLevelRules`
              - GridLayout: `GridLayout`
                - StackLayout: `StackLayout`
                  - Label: `PopupHeadingViewApprovalLevelRules`
                - StackLayout: `StackLayout`
                  - DataGrid: `ViewApprovalLevelRulesDataGrid`
                    - columns (in order): `ApprovalLevelAmount` "Approval Level Amount", `ManagerialApproval` "Managerial Approval", `TreasuryApproval` "Treasury Approval", `BankReleaseApproval` "Bank Release Approval" [from design model]
                - StackLayout: `StackLayout`
                  - Container: `Container1`
                    - GridLayout: `GridLayout`
                      - StackLayout: `StackLayout`
                        - Button: `CancelButton` — "Cancel"

### source-UI reference — ApprovalLevelRules (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `ApprovalLevelRulesDataGrid` → `PaymentsApiPaymentApprovals.ApprovalLevelRuleGetList`
- `EditSaveApprovalLevelRulesButton` → `PaymentsApiPaymentApprovals.ApprovalLevelRulesUpdate`
- `RefreshApprovalLevelRules` → `PaymentsApiPaymentApprovals.DistinctApprovalLevelGetList`

## Action affordances → candidate tasks

> Per surface: actionable controls whose label carries an action verb. Control · label · wired script are **Tier-A** facts; the candidate **task** is **Tier-B** `[AI-SUGGESTED]` (verb taxonomy; UI chrome excluded). The flat visible-terms list in `glossary` is retained separately.

### Users
- `AddUserButton` — "Add User" — wired to `AddUserButton.Click`  →  candidate task: **Add User** `[AI-SUGGESTED]`

### AttachmentsAndNotes
- `AddNoteButton` — "Add Note" — wired to `AddNoteButton.Click`  →  candidate task: **Add Note** `[AI-SUGGESTED]`

### Review
- `SubmitButton` — "Submit" — wired to `SubmitButton.Click`  →  candidate task: **Submit** `[AI-SUGGESTED]`

### ApprovalLevels
- `CreateApprovalLevelButton` — "Create Approval Level" — wired to `CreateApprovalLevelButton.Click`  →  candidate task: **Create Approval Level** `[AI-SUGGESTED]`

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
