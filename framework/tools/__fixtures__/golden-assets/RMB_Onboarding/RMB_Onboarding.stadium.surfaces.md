---
stadium_asset: surfaces
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
# Surfaces (screens, controls, layout) — RMB_Onboarding

> Tier-A = which surfaces/controls/data exist (authoritative). Tier-B = layout & control-choice (advisory; the system holds design authority).

## View / task / feature inventory

> Columns Page / Title / Route / Start / Design-surface / Reachable / Route-declared are **Tier-A** facts (design model + administration.db + rendered `page-routes.js`). **Inferred kind** is **Tier-B** `[AI-SUGGESTED]` (name-suffix taxonomy; bare nouns → entity-maintenance). Title + Route come from the rendered router `[from rendered routes]`.

| Page | Title | Route | Start? | Design surface? | Reachable via nav? | Route-declared? | Inferred kind |
|---|---|---|:---:|:---:|:---:|:---:|---|
| ClientServiceRequest | Client Service Request | `/ClientServiceRequest` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| ClientApplications | Client Applications | `/ClientApplications` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| Enablement | Client Applications | `/Enablement` |  | ✓ |  | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| Dashboard | Client Applications | `/Dashboard` |  | ✓ |  | ✓ | landing `[AI-SUGGESTED]` |
| pgClientDetails | Client Details | `/pgClientDetails` |  | ✓ | ✓ | ✓ | detail `[AI-SUGGESTED]` |
| pgModularInformation | Modular Information | `/pgModularInformation` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| pgCollections | Collections | `/pgCollections` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| pgAdministrators | Administrators | `/pgAdministrators` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| pgAccounts | Accounts | `/pgAccounts` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| pgSignatories | Pg Signatories | `/pgSignatories` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| pgGenerate | Generate | `/pgGenerate` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| StartPage | Start Page | `/StartPage` | ✓ | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |

## Tier-A — reports & dashboards

- Dashboard / landing surfaces: `Dashboard` [from design model]

## ClientServiceRequest  ·  title: Client Service Request  ·  roles: —
  - Button: `btnAddServiceRequest` — "Add"
  - Button: `btnAddServiceService` — "Service"
  - Button: `Button2` — "Add"
  - Button: `btnAddServiceService1` — "Service"
  - DataGrid: `dgSearchCustomers`  ·  grid: searchable
    - columns (in order): `ID` "Customer Number", `CustomerName` "Customer Name", `Launch`(action) [from design model]
  - Button: `btnCloseModal` — "Close"
- Visible terms: "Client Service Request", "Electronic Banking", "Global Banking", "Electronic Banking Service Request" [from design model]
> Layout: 6 meaningful control(s) within 37 layout container(s); max control-tree nesting depth 18 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — ClientServiceRequest (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `GetClientsInformation` → `OnboardingStandardBankCIB.GetClients`

## ClientApplications  ·  title: Client Applications  ·  roles: —
  - DataGrid: `DataGrid`  ·  grid: searchable
    - columns (in order): "Edit"(action), `Download` "Document"(action), `History` "Audit Log"(action), `ApplicationID` "Application", `ClientName` "Client Name", `ClientNumber` "Client"(hidden), `SalesPersonID` "Sales Person ID"(hidden), `SalesPerson` "Sales Person", `WOActionDesc` "Application Status", `CreatedDate` "Created Date", `UpdatedDate` "Updated Date", `CurrentStepID` "Current Step ID"(hidden), "WOID"(hidden), `ProductID` "Product ID"(hidden), `ApplicationNumber` "Application Number"(hidden), `WOType` "WO Type"(hidden), `ActionSequence` "Action Sequence"(hidden), `BackUpFileName` "Back Up File Name"(hidden), `BackupFileLocation` "Backup File Location"(hidden), `NextActionSequence` "Next Action Sequence"(hidden) [from design model]
  - TextBox: `tbCustomerName`  ·  read-only
  - TextBox: `tbApplicationNumer`  ·  read-only
  - DataGrid: `dgSearchCustomers`
    - columns (in order): "Date", `ActionUser` "Action User", "Details" [from design model]
  - Button: `btnCloseModal` — "Close"
- Visible terms: "Client applications", "Audit log", "Client Name", "Application Number" [from design model]
> Layout: 5 meaningful control(s) within 38 layout container(s); max control-tree nesting depth 15 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — ClientApplications (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `DataGrid` → `IDB.get_ApplicationFile`
- `DataGrid` → `FileSystemData.FileExists`
- `DataGrid` → `FileSystemData.ReadFile`
- `DataGrid` → `IDB.Sp_History_Get`
- `ClientApplications` → `IDB.Prc_Application_GetAll`

## Enablement  ·  title: Client Applications  ·  roles: —
  - DataGrid: `dgClientApplicationUnlocated`
    - columns (in order): `AllocateLink`(action), `ApplicationID` "Application ID", `ClientName` "Client Name", `ClientNumber` "Client Number", `Status` "Application Status", "Salesperson", `SalespersonID` "Salesperson ID"(hidden), `CreatedDate` "Created Date", `UpdatedDate` "Updated Date", `ProductID` "Product ID"(hidden), `ApplicationNumber` "Application Number"(hidden), "WOID"(hidden), `WOActionID` "WO Action ID"(hidden), `WOAction` "WO Action"(hidden), `CurrentStepID` "Current Step ID"(hidden) [from design model]
  - DataGrid: `dgClientApplicationAllocated`
    - columns (in order): `Vetting`(action), `ApplicationID` "Application ID", `ClientName` "Client Name", `ClientNumber` "Client Number", `Status` "Application Status", "Salesperson", `SalespersonID` "Salesperson ID"(hidden), `CreatedDate` "Created Date", `UpdatedDate` "Updated Date", `ProductID` "Product ID"(hidden), `ApplicationNumber` "Application Number"(hidden), "WOID"(hidden), `WOActionID` "WO Action ID"(hidden), `WOAction` "WO Action"(hidden), `ActionSequence` "Action Sequence"(hidden), `CurrentStepID` "Current Step ID"(hidden), `AllocatedID` "Allocated ID"(hidden) [from design model]
  - Button: `btnNextPageLeft` — "<"
  - Button: `btnNextPageRight` — ">"
  - TextBox: `tbVettingInfo_ApplicationID`  ·  read-only
  - TextBox: `tbVettingInfo_ClientName` — "1202202210000001019"  ·  read-only
  - TextBox: `tbVettingInfo_ClientNumber`  ·  read-only
  - CheckBox: `cbJointly`
  - TextBox: `tbCount`
  - CheckBox: `cbSeverally`
  - DataGrid: `dgSignatories`
    - columns (in order): "ID"(hidden), `ApplicationID` "Application ID"(hidden), `UserName` "User Name", `UserMiddleName` "User Middle Name", `UserSurname` "User Surname", `IdentificationType` "Identification Type"(hidden), `IdentificationNumber` "Identification Number", `PassportNumber` "Passport Number"(hidden), `DriversLicenceNumber` "Drivers Licence Number"(hidden), `DateCreated` "Date Created"(hidden), `DateUpdated` "Date Updated"(hidden), `PhysicalAddress` "Physical Address"(hidden) [from design model]
  - Button: `btnEnablementReject` — "Reject"
  - Button: `btnEnablement_Accept` — "Accept"
  - TextBox: `tbEnablement_RejectReason`
  - Button: `btnCancelReject_Back` — "Back"
  - Button: `btnAcceptReject` — "Reject"
  - Button: `btnEnablement_Vetting_Close` — "Close"
- Visible terms: "Client applications", "Allocated", "Application Number", "Client Name", "Client Number", "Signing arrangements", "Joint", "Signatories Needed", "Severally", "Designated Persons" [from design model]
> Layout: 17 meaningful control(s) within 98 layout container(s); max control-tree nesting depth 27 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — Enablement (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `dgClientApplicationUnlocated` → `IDB.Sp_ClientApplications_Allocate_Insert`
- `dgClientApplicationUnlocated` → `IDB.Prc_WOHistory_insert1`
- `dgClientApplicationAllocated` → `IDB.Sp_FileImage_Get`
- `btnNextPageLeft` → `OnboardingStandardBankCIB.Sp_FileImage_Get`
- `btnNextPageLeft` → `FileSystem.ReadFile`
- `btnNextPageRight` → `OnboardingStandardBankCIB.Sp_FileImage_Get`
- `btnNextPageRight` → `FileSystem.ReadFile`
- `btnEnablement_Accept` → `IDB.Prc_WO_Update`
- `btnEnablement_Accept` → `IDB.Prc_WOHistory_insert1`
- `btnAcceptReject` → `OnboardingStandardBankCIB.Prc_WO_updateNAS75`
- `btnAcceptReject` → `OnboardingStandardBankCIB.Prc_WOHistory_insert`
- `btnAcceptReject` → `OnboardingStandardBankCIB.Prc_WO_updateNAS1000`
- `LoadDatagrids` → `IDB.Sp_ClientApplications_Get`
- `LoadDatagrids` → `IDB.Sp_ClientApplicationsUnallocated_Get`
- `LoadImage` → `IDB.Sp_FileImage_Get`
- `LoadImage` → `FileSystem.ReadFile`

## Dashboard  ·  title: Client Applications  ·  roles: —
  - Chart: `ChartApplicationCreateCount`
  - Chart: `ChartApplicationStatus`
- Visible terms: "Applications Dashboard", "Completed Applications", "Daily Average" [from design model]
> Layout: 2 meaningful control(s) within 25 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

## pgClientDetails  ·  title: Client Details  ·  roles: —
  - TextBox: `txtClientName`
  - TextBox: `txtClientRegNo`
  - TextBox: `txtClientSegment`
  - Button: `btnClose` — "Close"
  - Button: `btnSave` — "Save"
  - DataGrid: `dgExistingClient`  ·  grid: searchable
    - columns (in order): `ClientName` "Client Name", `ClientRegistrationNumber` "Client Registration Number", `ClientID` "Client ID", `ClientSegment` "Client Segment", `Launch`(action), `_ClientIDinternal`(hidden) [from design model]
- Visible terms: "Client Information", "New Client", "Client Name:", "Client Registration Number:", "Client Segment:", "Existing Client" [from design model]
> Layout: 6 meaningful control(s) within 37 layout container(s); max control-tree nesting depth 15 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — pgClientDetails (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `btnSave` → `IDB.Prc_ClientDetails_Insert`
- `pgClientDetails` → `IDB.get_AllClientDetails`
- `Application_Create` → `IDB.Prc_WO_Insert_1`
- `Application_Create` → `IDB.Prc_Application_Insert`
- `Application_Create` → `IDB.sp_Create_Application_Steps`
- `Application_Create` → `IDB.sp_Create_Application_Steps_UpdateValid`

## pgModularInformation  ·  title: Modular Information  ·  roles: —
  - TextBox: `txtClientName`  ·  read-only
  - TextBox: `txtClientRegNo`  ·  read-only
  - CheckBox: `chbNomAccPayments`
  - CheckBox: `chbOnceOffPayments`
  - CheckBox: `chbTransfers`
  - CheckBox: `chbCollections`
  - CheckBox: `chbSignatories`
  - CheckBox: `chbCashman`
  - CheckBox: `chbLinkCCN`
  - TextBox: `txtCCN1`
  - TextBox: `txtCCN2`
  - TextBox: `txtCCN3`
  - TextBox: `txtCCN4`
  - TextBox: `txtCCN5`
  - TextBox: `txtCCN6`
  - CheckBox: `chbCashmanReports`
  - CheckBox: `chbNAEDO`
  - CheckBox: `chbOnlineSettlementLimits`
  - CheckBox: `chbFTPDeliveryMechanism`
  - Button: `btnSave` — "Save"
  - Button: `btnClose` — "Close"
  - Button: `btnNext` — "Next"
  - DataGrid: `dgModularEntities`
    - columns (in order): `View`(action), `Remove`(action), `_ModEntityID` "Entity ID", `ModEntityName` "Entity Name", `ModEntityNumber` "Entity Number" [from design model]
  - Button: `btnAddEntity` — "Add Entity"
  - TextBox: `txtModalEntityID`  ·  read-only
  - TextBox: `txtModalEntityName`
  - TextBox: `txtModalEntityNumber`
  - Button: `btnModalAdd` — "Add"
  - Button: `btnModalUpdate` — "Update"
  - Button: `btnModalClose` — "Close"
- Visible terms: "Modular Information", "Client Name:", "Client Registration Number:", "*Please select the modules that you would like to utilise with the bank’s Online Banking Enterprise", "Nominated Account Payments", "Once off Payments", "Transfers", "Collections", "A and B Signatories", "Cashman", "Link CCN Number?", "CCN Number 1", "CCN Number 2", "CCN Number 3", "CCN Number 4", "CCN Number 5", "CCN Number 6", "Cashman Reports", "NAEDO", "Online Settlement Limits", "FTP Delivery Mechanism", "Complete the section below if applicable to Hierarchy", "Add Entity Details", "Entity Name", "Entity Number" [from design model]
> Layout: 30 meaningful control(s) within 147 layout container(s); max control-tree nesting depth 15 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — pgModularInformation (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `btnSave` → `IDB.get_CheckModularInformationExists`
- `btnSave` → `IDB.Prc_ModularInformation_Update`
- `btnSave` → `IDB.Prc_ModularInformation_Insert`
- `btnNext` → `IDB.get_CheckModularInformationExists`
- `btnNext` → `IDB.Prc_ModularInformation_Update`
- `btnNext` → `IDB.Prc_ModularInformation_Insert`
- `btnNext` → `IDB.sp_Create_Application_Steps_UpdateValid`
- `dgModularEntities` → `IDB.get_ModularEntity`
- `btnModalAdd` → `IDB.Prc_ModularEntity_Insert`
- `btnModalUpdate` → `IDB.Prc_ModularEntity_Update`
- `pgModularInformation` → `IDB.get_ClientDetails`
- `pgModularInformation` → `IDB.get_CheckModularInformationExists`
- `pgModularInformation` → `IDB.get_ModularInformation`
- `LoadEntities` → `IDB.Prc_ModularEntity_GetList`

## pgCollections  ·  title: Collections  ·  roles: —
  - TextBox: `txtClientName`  ·  read-only
  - TextBox: `txtClientRegNo`  ·  read-only
  - TextBox: `txtCollAppClientName`
  - TextBox: `txtCollAppAccountNumber`
  - TextBox: `txtCollAppBranchCode`
  - Button: `btnAdd` — "Add"
  - TextBox: `txtContactPersonID`
  - TextBox: `txtCompanyName`  ·  read-only
  - Button: `btnView` — "View"
  - Button: `btnRemove` — "Remove"
  - TextBox: `txtAccountNumber`  ·  read-only
  - Button: `btnPrevious` — "Previous"
  - Button: `btnNext` — "Next"
  - TextBox: `txtModalContactPersonID`  ·  read-only
  - TextBox: `txtModalAccountNo`
  - TextBox: `txtModalAbbreviatedName`  ·  hint: "Must be 10 characters for debit users."
  - TextBox: `txtModalCompanyName`
  - TextBox: `txtModalContactName`
  - TextBox: `txtModalContactTel`
  - TextBox: `txtModalContactEmail`
  - Button: `btnModalAdd` — "Add"
  - Button: `btnModalUpdate` — "Update"
  - Button: `btnModalClose` — "Close"
- Visible terms: "Collections Application", "Client Name:", "Client Registration Number:", "Account Name", "Account Number", "Branch Code", "The Contact person must be the person to whom Collections queries will be escalated.", "Company Name", "Contact Person ID", "Abbreviated Name", "Contact Name", "Contact Tel No", "Contact Email" [from design model]
> Layout: 23 meaningful control(s) within 111 layout container(s); max control-tree nesting depth 15 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — pgCollections (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `btnView` → `IDB.get_CollectionsContactPerson`
- `btnRemove` → `IDB.Prc_CollectionsContactPerson_Disable`
- `btnNext` → `IDB.get_CheckCollectionsExists`
- `btnNext` → `IDB.Prc_Collections_Update`
- `btnNext` → `IDB.Prc_Collections_Insert`
- `btnNext` → `IDB.sp_Create_Application_Steps_UpdateValid`
- `btnModalAdd` → `IDB.Prc_CollectionsContactPerson_Insert`
- `btnModalUpdate` → `IDB.Prc_CollectionsContactPerson_Update`
- `pgCollections` → `IDB.get_ClientDetails`
- `pgCollections` → `IDB.get_CheckCollectionsExists`
- `pgCollections` → `IDB.get_Collections`
- `LoadContactPersons` → `IDB.Prc_CollectionsContactPerson_GetList`
- `Validate` → `IDB.get_ContactPersonCount`

## pgAdministrators  ·  title: Administrators  ·  roles: —
  - TextBox: `txtClientName`  ·  read-only
  - TextBox: `txtClientRegNo`  ·  read-only
  - TextBox: `txtAdministratorID`  ·  read-only
  - TextBox: `txtFullName`
  - Button: `btnView` — "View"
  - Button: `btnRemove` — "Remove"
  - TextBox: `txtIDPassport`
  - TextBox: `txtCapacity`
  - Button: `btnAdd` — "Add Admin"
  - Button: `btnPrevious` — "Previous"
  - Button: `btnNext` — "Next"
  - TextBox: `txtModalFullName`
  - DropDown: `ddAddUSer_IDType`  ·  choices: "ID", "Passport"
  - TextBox: `txtModalIDPassport`  ·  hint: "Enter ID Number"
  - TextBox: `txtModalCapacity`
  - TextBox: `txtModalAdministratorID`
  - Button: `btnModalAdd` — "Add"
  - Button: `btnModalUpdate` — "Update"
  - Button: `btnModalClose` — "Close"
- Visible terms: "Appointment of Administrators", "Client Name:", "Client Registration Number:", "Administrator ID", "Full Name", "ID/Passport", "Capacity", "Add Administrator", "Identification Type" [from design model]
> Layout: 19 meaningful control(s) within 94 layout container(s); max control-tree nesting depth 15 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — pgAdministrators (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `btnView` → `IDB.get_Administrator`
- `btnRemove` → `IDB.Prc_Administrators_Disable`
- `btnNext` → `IDB.sp_Create_Application_Steps_UpdateValid`
- `btnModalAdd` → `IDB.Prc_Administrators_Insert`
- `btnModalUpdate` → `IDB.Prc_Administrators_Update`
- `pgAdministrators` → `IDB.get_ClientDetails`
- `LoadAdministrators` → `IDB.Prc_Administrators_GetList`
- `Validate` → `IDB.get_AdministratorCount`

## pgAccounts  ·  title: Accounts  ·  roles: —
  - TextBox: `txtClientName`  ·  read-only
  - TextBox: `txtClientRegNo`  ·  read-only
  - TextBox: `txtEntityName1`
  - TextBox: `txtEntityNumber1`
  - Button: `btnLinkAccount1` — "Link Account"
  - Button: `btnAddSubgroup` — "Add Sub Group"
  - TextBox: `txtAccountName1`  ·  read-only
  - Button: `btnView` — "View"
  - Button: `btnRemove` — "Remove"
  - TextBox: `txtAccountNumber1`  ·  read-only
  - TextBox: `txtPartiesHeirarchyID`  ·  read-only
  - TextBox: `txtEntityName2`
  - TextBox: `txtEntityNumber2`
  - Button: `btnLinkAccount2` — "Link Account"
  - Button: `btnRemoveSubgroup` — "Remove Sub Group"
  - TextBox: `txtAccountName2`  ·  read-only
  - Button: `btnView2` — "View"
  - Button: `btnRemove2` — "Remove"
  - TextBox: `txtAccountNumber2`  ·  read-only
  - Button: `btnPrevious` — "Previous"
  - Button: `btnNext` — "Next"
  - TextBox: `tbAccountName`
  - TextBox: `tbAccountNumber`
  - TextBox: `tbPartiesHeirarchyID`
  - Button: `btnModalAdd` — "Add"
  - Button: `btnModalUpdate` — "Update"
  - Button: `btnModalClose` — "Close"
- Visible terms: "Accounts", "Client Name:", "Client Registration Number:", "Create Sub Group 1", "Entity Name", "Entity Number", "Link an account below:", "Account Name", "Account Number", "Create Sub Group 2" [from design model]
> Layout: 27 meaningful control(s) within 135 layout container(s); max control-tree nesting depth 18 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — pgAccounts (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `btnView` → `IDB.get_PartiesHeirarchyTable`
- `btnNext` → `IDB.get_EntitiesExist`
- `btnNext` → `IDB.Prc_HeirarchyEntities_Update`
- `btnNext` → `IDB.Prc_HeirarchyEntities_Insert`
- `btnNext` → `IDB.sp_Create_Application_Steps_UpdateValid`
- `btnModalAdd` → `IDB.Prc_PartiesHeirarchy_Insert`
- `btnModalUpdate` → `IDB.Prc_PartiesHeirarchy_Update`
- `pgAccounts` → `IDB.get_ClientDetails`
- `pgAccounts` → `IDB.get_CheckHeirarchyEntitiesExists`
- `pgAccounts` → `IDB.get_HeirarchyEntities`
- `ProgressBarUpdate` → `IDB.sp_Application_Step_Status`
- `LoadLinkedAccounts` → `IDB.Prc_PartiesHeirarchy_GetList`
- `Validate` → `IDB.get_PartiesHierarchCount`

## pgSignatories  ·  title: Pg Signatories  ·  roles: —
  - TextBox: `txtClientName`  ·  read-only
  - TextBox: `txtClientRegNo`  ·  read-only
  - TextBox: `txtFullName`  ·  read-only
  - Button: `btnView` — "View"
  - Button: `btnRemove` — "Remove"
  - TextBox: `txtDesignation`  ·  read-only
  - TextBox: `txtIDPassport`  ·  read-only
  - TextBox: `txtSignatoryID1`  ·  read-only
  - Button: `btnAdd` — "Add Signatory"
  - Button: `btnPrevious` — "Previous"
  - Button: `btnNext` — "Next"
  - TextBox: `txtModalFullName`
  - DropDown: `ddAddIDType`  ·  choices: "ID", "Passport"
  - TextBox: `txtModalIDPassport`  ·  hint: "Enter ID Number"
  - TextBox: `txtModalDesignation`
  - TextBox: `txtModalSignatoryID`  ·  read-only
  - Button: `btnModalAdd` — "Add"
  - Button: `btnModalUpdate` — "Update"
  - Button: `btnModalClose` — "Close"
- Visible terms: "Signatories", "Client Name:", "Client Registration Number:", "Full Name and Surname", "Designation", "ID/Passport", "Add Signatory", "Identification Type", "Identity" [from design model]
> Layout: 19 meaningful control(s) within 93 layout container(s); max control-tree nesting depth 15 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — pgSignatories (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `btnView` → `IDB.get_Signatory`
- `btnRemove` → `IDB.Prc_SignatureField_Disable`
- `btnNext` → `IDB.sp_Create_Application_Steps_UpdateValid`
- `btnModalAdd` → `IDB.Prc_SignatureField_Insert`
- `btnModalUpdate` → `IDB.Prc_Signatories_Update`
- `pgSignatories` → `IDB.get_ClientDetails`
- `Validate` → `IDB.get_SignatoryCount`
- `LoadSignatories` → `IDB.Prc_SignatureField_GetList`

## pgGenerate  ·  title: Generate  ·  roles: —
  - TextBox: `txtClientName`  ·  read-only
  - TextBox: `txtClientRegNo`  ·  read-only
  - DataGrid: `dgValidationStatus`
    - columns (in order): "Description", `DateUpdated` "Date Updated", `StepValid` "Step Valid", "ID"(hidden), "WOID"(hidden), `CfgApplicationStepID` "Cfg Application Step ID"(hidden), `StepNumber` "Step Number"(hidden), `DateCompleted` "Date Completed"(hidden), `ProductID` "Product ID"(hidden), `DateCreated` "Date Created"(hidden), `StepName` "Step Name"(hidden) [from design model]
  - TextBox: `tbEmail`
  - Button: `btnPrevious` — "Previous"
  - Button: `btnGenerate` — "Generate"
- Visible terms: "Generate", "Client Name:", "Client Registration Number:", "Email address:" [from design model]
> Layout: 6 meaningful control(s) within 31 layout container(s); max control-tree nesting depth 12 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — pgGenerate (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `btnGenerate` → `IDB.Prc_WO_Update`
- `btnGenerate` → `IDB.Prc_WOHistory_insert1`
- `pgGenerate` → `IDB.sp_Application_Steps_Get`
- `pgGenerate` → `IDB.get_ClientDetails`
- `Validate` → `IDB.get_InvalidSteps`

## StartPage ⭐ start  ·  title: Start Page  ·  roles: User
- _(layout-only surface — no data-bound controls, grids, or labelled actions)_
> Layout: 0 meaningful control(s) within 1 layout container(s); max control-tree nesting depth 1 (per-node layout omitted — see model.json). Advisory.

## User tasks (per view)

> The per-view user-task inventory — the verb-labelled action affordances triangulated with wired backend operations, DataGrids and page-kinds, with a ≥1-task-per-view completeness guarantee — is emitted as its own asset: see `RMB_Onboarding.stadium.tasks.md`.

## Tier-A — screen ↔ entity (best-effort)

| Page | Likely entity |
|---|---|
| ClientServiceRequest | Clients |
| ClientApplications | ClientApplications |
| Enablement | — |
| Dashboard | — |
| pgClientDetails | — |
| pgModularInformation | ModularInformation |
| pgCollections | Collections |
| pgAdministrators | Administrators |
| pgAccounts | — |
| pgSignatories | — |
| pgGenerate | — |
| StartPage | — |
