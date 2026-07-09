---
stadium_asset: tasks
app: RMB_Onboarding
file_guid: 87ea91de-6125-4686-8437-806216cb0ec0
designer_version: 6.14.3378.13771
selected_package: 3f1ddf96-3519-47b8-905d-b44703776f78.sapz
extracted_from: C:\Stadium 6 Web Apps\87ea91de-6125-4686-8437-806216cb0ec0
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# User tasks — RMB_Onboarding

> One row per derivable USER TASK per view. Each task's EVIDENCE — the view, the wired control→op (`[from rendered view]`), the grid / action column (`[from design model]`), the title (`[from rendered routes]`) — is **Tier-A** (authoritative, `[SRC]`-citable via the inline locator). The task's verb / name is **Tier-B** `[AI-SUGGESTED]` (interpretation). Entities are drawn only from the reconciled set (see `data-model`) — never invented. Every view yields ≥1 row; a view with no derivable task says so explicitly. Confidence: high (wired op + resolved entity) / medium (labelled affordance, grid action, or op without entity) / low (page-kind/title fallback).

## Task inventory

| View | Task `[AI-SUGGESTED]` | Verb | Entity | Conf. | Evidence [from …] |
|---|---|---|---|:--:|---|
| ClientServiceRequest | Browse Clients | SELECT | Clients | high | grid `dgSearchCustomers` (searchable) [from design model]; `GetClientsInformation` → `OnboardingStandardBankCIB.GetClients` [from rendered view] |
| ClientServiceRequest | Add Clients | INSERT | Clients | medium | affordance `btnAddServiceRequest` "Add" [from design model]; wired to `btnAddServiceRequest.Click`; affordance `Button2` "Add" [from design model]; wired to `Button2.Click` |
| ClientApplications | Browse History | SELECT | History | high | grid `DataGrid` (searchable) [from design model]; `DataGrid` → `IDB.Sp_History_Get` [from rendered view]; grid `dgSearchCustomers` [from design model] |
| ClientApplications | Update History | UPDATE | History | medium | action column "Edit" on `DataGrid` [from design model] |
| Enablement | Browse FileImage | SELECT | FileImage | high | grid `dgClientApplicationUnlocated` [from design model]; `dgClientApplicationAllocated` → `IDB.Sp_FileImage_Get` [from rendered view]; `btnNextPageLeft` → `OnboardingStandardBankCIB.Sp_FileImage_Get` [from rendered view]; `btnNextPageRight` → `OnboardingStandardBankCIB.Sp_FileImage_Get` [from rendered view]; `LoadImage` → `IDB.Sp_FileImage_Get` [from rendered view]; grid `dgClientApplicationAllocated` [from design model]; grid `dgSignatories` [from design model] |
| Enablement | Add (object unresolved) | INSERT | — | medium | `dgClientApplicationUnlocated` → `IDB.Prc_WOHistory_insert1` [from rendered view]; `btnEnablement_Accept` → `IDB.Prc_WOHistory_insert1` [from rendered view] |
| Enablement | Add ClientApplicationsAllocate | INSERT | ClientApplicationsAllocate | high | `dgClientApplicationUnlocated` → `IDB.Sp_ClientApplications_Allocate_Insert` [from rendered view] |
| Enablement | Add WOHistory | INSERT | WOHistory | high | `btnAcceptReject` → `OnboardingStandardBankCIB.Prc_WOHistory_insert` [from rendered view] |
| Enablement | Update (object unresolved) | UPDATE | — | medium | `btnAcceptReject` → `OnboardingStandardBankCIB.Prc_WO_updateNAS75` [from rendered view]; `btnAcceptReject` → `OnboardingStandardBankCIB.Prc_WO_updateNAS1000` [from rendered view] |
| Enablement | Update WO | UPDATE | WO | high | `btnEnablement_Accept` → `IDB.Prc_WO_Update` [from rendered view] |
| Enablement | Accept (object unresolved) | accept | — | medium | affordance `btnEnablement_Accept` "Accept" [from design model]; wired to `btnEnablement_Accept.Click` |
| Enablement | Reject (object unresolved) | reject | — | medium | affordance `btnEnablementReject` "Reject" [from design model]; wired to `btnEnablementReject.Click`; affordance `btnAcceptReject` "Reject" [from design model]; wired to `btnAcceptReject.Click` |
| pgClientDetails | Browse (object unresolved) | SELECT | — | medium | grid `dgExistingClient` (searchable) [from design model]; `pgClientDetails` → `IDB.get_AllClientDetails` [from rendered view] |
| pgClientDetails | Add (object unresolved) | INSERT | — | medium | `Application_Create` → `IDB.Prc_WO_Insert_1` [from rendered view] |
| pgClientDetails | Add ApplicationSteps | INSERT | ApplicationSteps | high | `Application_Create` → `IDB.sp_Create_Application_Steps` [from rendered view] |
| pgClientDetails | Add tbl_ClientDetails | INSERT | tbl_ClientDetails | high | `btnSave` → `IDB.Prc_ClientDetails_Insert` [from rendered view] |
| pgClientDetails | Add tblApplications | INSERT | tblApplications | high | `Application_Create` → `IDB.Prc_Application_Insert` [from rendered view] |
| pgClientDetails | Update (object unresolved) | UPDATE | — | medium | `Application_Create` → `IDB.sp_Create_Application_Steps_UpdateValid` [from rendered view] |
| pgModularInformation | Browse ModularEntity | SELECT | ModularEntity | high | grid `dgModularEntities` [from design model]; `dgModularEntities` → `IDB.get_ModularEntity` [from rendered view]; `LoadEntities` → `IDB.Prc_ModularEntity_GetList` [from rendered view] |
| pgModularInformation | Add Entity | INSERT | ModularInformation | high | `btnSave` → `IDB.Prc_ModularInformation_Insert` [from rendered view]; `btnNext` → `IDB.Prc_ModularInformation_Insert` [from rendered view]; affordance `btnAddEntity` "Add Entity" [from design model]; wired to `btnAddEntity.Click`; affordance `btnModalAdd` "Add" [from design model]; wired to `btnModalAdd.Click` |
| pgModularInformation | Add ModularEntity | INSERT | ModularEntity | high | `btnModalAdd` → `IDB.Prc_ModularEntity_Insert` [from rendered view] |
| pgModularInformation | Update ModularEntity | UPDATE | ModularEntity | high | `btnModalUpdate` → `IDB.Prc_ModularEntity_Update` [from rendered view] |
| pgModularInformation | Update ModularInformation | UPDATE | ModularInformation | high | `btnSave` → `IDB.Prc_ModularInformation_Update` [from rendered view]; `btnNext` → `IDB.Prc_ModularInformation_Update` [from rendered view]; `btnNext` → `IDB.sp_Create_Application_Steps_UpdateValid` [from rendered view]; affordance `btnModalUpdate` "Update" [from design model]; wired to `btnModalUpdate.Click` |
| pgCollections | Add Collections | INSERT | Collections | high | `btnNext` → `IDB.Prc_Collections_Insert` [from rendered view]; affordance `btnAdd` "Add" [from design model]; wired to `btnAdd.Click`; affordance `btnModalAdd` "Add" [from design model]; wired to `btnModalAdd.Click` |
| pgCollections | Add tbl_CollectionsContactPerson | INSERT | tbl_CollectionsContactPerson | high | `btnModalAdd` → `IDB.Prc_CollectionsContactPerson_Insert` [from rendered view] |
| pgCollections | Update Collections | UPDATE | Collections | high | `btnNext` → `IDB.Prc_Collections_Update` [from rendered view]; `btnNext` → `IDB.sp_Create_Application_Steps_UpdateValid` [from rendered view]; affordance `btnModalUpdate` "Update" [from design model]; wired to `btnModalUpdate.Click` |
| pgCollections | Update tbl_CollectionsContactPerson | UPDATE | tbl_CollectionsContactPerson | high | `btnModalUpdate` → `IDB.Prc_CollectionsContactPerson_Update` [from rendered view] |
| pgCollections | Delete Collections | DELETE | Collections | medium | affordance `btnRemove` "Remove" [from design model]; wired to `btnRemove.Click` |
| pgCollections | Delete tbl_CollectionsContactPerson | DELETE | tbl_CollectionsContactPerson | high | `btnRemove` → `IDB.Prc_CollectionsContactPerson_Disable` [from rendered view] |
| pgCollections | View Collections | view | Collections | medium | affordance `btnView` "View" [from design model]; wired to `btnView.Click` |
| pgAdministrators | Add Admin | INSERT | Administrators | high | `btnModalAdd` → `IDB.Prc_Administrators_Insert` [from rendered view]; affordance `btnAdd` "Add Admin" [from design model]; wired to `btnAdd.Click`; affordance `btnModalAdd` "Add" [from design model]; wired to `btnModalAdd.Click` |
| pgAdministrators | Update Administrators | UPDATE | Administrators | high | `btnNext` → `IDB.sp_Create_Application_Steps_UpdateValid` [from rendered view]; `btnModalUpdate` → `IDB.Prc_Administrators_Update` [from rendered view]; affordance `btnModalUpdate` "Update" [from design model]; wired to `btnModalUpdate.Click` |
| pgAdministrators | Delete Administrators | DELETE | Administrators | high | `btnRemove` → `IDB.Prc_Administrators_Disable` [from rendered view]; affordance `btnRemove` "Remove" [from design model]; wired to `btnRemove.Click` |
| pgAdministrators | View Administrators | view | Administrators | medium | affordance `btnView` "View" [from design model]; wired to `btnView.Click` |
| pgAccounts | Add PartiesHeirarchy | INSERT | PartiesHeirarchy | high | `btnModalAdd` → `IDB.Prc_PartiesHeirarchy_Insert` [from rendered view] |
| pgAccounts | Add Sub Group | INSERT | — | medium | affordance `btnAddSubgroup` "Add Sub Group" [from design model]; wired to `btnAddSubgroup.Click`; affordance `btnModalAdd` "Add" [from design model]; wired to `btnModalAdd.Click` |
| pgAccounts | Add tbl_HeirarchyEntities | INSERT | tbl_HeirarchyEntities | high | `btnNext` → `IDB.Prc_HeirarchyEntities_Insert` [from rendered view] |
| pgAccounts | Update (object unresolved) | UPDATE | — | medium | `btnNext` → `IDB.sp_Create_Application_Steps_UpdateValid` [from rendered view]; affordance `btnModalUpdate` "Update" [from design model]; wired to `btnModalUpdate.Click` |
| pgAccounts | Update PartiesHeirarchy | UPDATE | PartiesHeirarchy | high | `btnModalUpdate` → `IDB.Prc_PartiesHeirarchy_Update` [from rendered view] |
| pgAccounts | Update tbl_HeirarchyEntities | UPDATE | tbl_HeirarchyEntities | high | `btnNext` → `IDB.Prc_HeirarchyEntities_Update` [from rendered view] |
| pgAccounts | Delete (object unresolved) | DELETE | — | medium | affordance `btnRemove` "Remove" [from design model]; wired to `btnRemove.Click`; affordance `btnRemoveSubgroup` "Remove Sub Group" [from design model]; wired to `btnRemoveSubgroup.Click`; affordance `btnRemove2` "Remove" [from design model] |
| pgAccounts | Link Account | link | — | medium | affordance `btnLinkAccount1` "Link Account" [from design model]; wired to `btnLinkAccount1.Click`; affordance `btnLinkAccount2` "Link Account" [from design model]; wired to `btnLinkAccount2.Click` |
| pgAccounts | View (object unresolved) | view | — | medium | affordance `btnView` "View" [from design model]; wired to `btnView.Click`; affordance `btnView2` "View" [from design model] |
| pgSignatories | Add (object unresolved) | INSERT | — | medium | affordance `btnModalAdd` "Add" [from design model]; wired to `btnModalAdd.Click` |
| pgSignatories | Add Signatory | INSERT | Signatory | medium | affordance `btnAdd` "Add Signatory" [from design model]; wired to `btnAdd.Click` |
| pgSignatories | Add tbl_SignatureField | INSERT | tbl_SignatureField | high | `btnModalAdd` → `IDB.Prc_SignatureField_Insert` [from rendered view] |
| pgSignatories | Update (object unresolved) | UPDATE | — | medium | `btnNext` → `IDB.sp_Create_Application_Steps_UpdateValid` [from rendered view]; affordance `btnModalUpdate` "Update" [from design model]; wired to `btnModalUpdate.Click` |
| pgSignatories | Update Signatory | UPDATE | Signatory | high | `btnModalUpdate` → `IDB.Prc_Signatories_Update` [from rendered view] |
| pgSignatories | Delete (object unresolved) | DELETE | — | medium | affordance `btnRemove` "Remove" [from design model]; wired to `btnRemove.Click` |
| pgSignatories | Delete tbl_SignatureField | DELETE | tbl_SignatureField | high | `btnRemove` → `IDB.Prc_SignatureField_Disable` [from rendered view] |
| pgSignatories | View (object unresolved) | view | — | medium | affordance `btnView` "View" [from design model]; wired to `btnView.Click` |
| pgGenerate | Browse ApplicationSteps | SELECT | ApplicationSteps | high | grid `dgValidationStatus` [from design model]; `pgGenerate` → `IDB.sp_Application_Steps_Get` [from rendered view] |
| pgGenerate | Add (object unresolved) | INSERT | — | medium | `btnGenerate` → `IDB.Prc_WOHistory_insert1` [from rendered view] |
| pgGenerate | Update WO | UPDATE | WO | high | `btnGenerate` → `IDB.Prc_WO_Update` [from rendered view] |
| pgGenerate | Generate (object unresolved) | generate | — | medium | affordance `btnGenerate` "Generate" [from design model]; wired to `btnGenerate.Click` |
| StartPage | Start Page | UPDATE | — | low | kind `entity-maintenance` `[AI-SUGGESTED]`; title "Start Page" [from rendered routes] |

## Per-view notes

- **ClientApplications** — supporting reads (lookups / pre-fill, not tasks): `DataGrid` → `IDB.get_ApplicationFile` [from rendered view]; `DataGrid` → `FileSystemData.ReadFile` [from rendered view]; `ClientApplications` → `IDB.Prc_Application_GetAll` [from rendered view]
- **Enablement** — supporting reads (lookups / pre-fill, not tasks): `btnNextPageLeft` → `FileSystem.ReadFile` [from rendered view]; `btnNextPageRight` → `FileSystem.ReadFile` [from rendered view]; `LoadDatagrids` → `IDB.Sp_ClientApplications_Get` [from rendered view]; `LoadDatagrids` → `IDB.Sp_ClientApplicationsUnallocated_Get` [from rendered view]; `LoadImage` → `FileSystem.ReadFile` [from rendered view]
- **pgModularInformation** — supporting reads (lookups / pre-fill, not tasks): `btnSave` → `IDB.get_CheckModularInformationExists` [from rendered view]; `btnNext` → `IDB.get_CheckModularInformationExists` [from rendered view]; `pgModularInformation` → `IDB.get_ClientDetails` [from rendered view]; `pgModularInformation` → `IDB.get_CheckModularInformationExists` [from rendered view]; `pgModularInformation` → `IDB.get_ModularInformation` [from rendered view]
- **pgCollections** — supporting reads (lookups / pre-fill, not tasks): `btnView` → `IDB.get_CollectionsContactPerson` [from rendered view]; `btnNext` → `IDB.get_CheckCollectionsExists` [from rendered view]; `pgCollections` → `IDB.get_ClientDetails` [from rendered view]; `pgCollections` → `IDB.get_CheckCollectionsExists` [from rendered view]; `pgCollections` → `IDB.get_Collections` [from rendered view]; `LoadContactPersons` → `IDB.Prc_CollectionsContactPerson_GetList` [from rendered view]; `Validate` → `IDB.get_ContactPersonCount` [from rendered view]
- **pgAdministrators** — supporting reads (lookups / pre-fill, not tasks): `btnView` → `IDB.get_Administrator` [from rendered view]; `pgAdministrators` → `IDB.get_ClientDetails` [from rendered view]; `LoadAdministrators` → `IDB.Prc_Administrators_GetList` [from rendered view]; `Validate` → `IDB.get_AdministratorCount` [from rendered view]
- **pgAccounts** — supporting reads (lookups / pre-fill, not tasks): `btnView` → `IDB.get_PartiesHeirarchyTable` [from rendered view]; `btnNext` → `IDB.get_EntitiesExist` [from rendered view]; `pgAccounts` → `IDB.get_ClientDetails` [from rendered view]; `pgAccounts` → `IDB.get_CheckHeirarchyEntitiesExists` [from rendered view]; `pgAccounts` → `IDB.get_HeirarchyEntities` [from rendered view]; `LoadLinkedAccounts` → `IDB.Prc_PartiesHeirarchy_GetList` [from rendered view]; `Validate` → `IDB.get_PartiesHierarchCount` [from rendered view]
- **pgSignatories** — supporting reads (lookups / pre-fill, not tasks): `btnView` → `IDB.get_Signatory` [from rendered view]; `pgSignatories` → `IDB.get_ClientDetails` [from rendered view]; `Validate` → `IDB.get_SignatoryCount` [from rendered view]; `LoadSignatories` → `IDB.Prc_SignatureField_GetList` [from rendered view]
- **pgGenerate** — supporting reads (lookups / pre-fill, not tasks): `pgGenerate` → `IDB.get_ClientDetails` [from rendered view]; `Validate` → `IDB.get_InvalidSteps` [from rendered view]
- **StartPage** — actor roles: User [from admin.db: PageRole]

## Views with no derivable user task

- `Dashboard` — authentication / landing surface (no data operation)

## Coverage

- **11 / 12** views have ≥1 derived user task; 1 view(s) with no derivable task (listed above).
