---
stadium_asset: business-rules
app: RMB_Onboarding
file_guid: 87ea91de-6125-4686-8437-806216cb0ec0
designer_version: 6.14.3378.13771
selected_package: 3f1ddf96-3519-47b8-905d-b44703776f78.sapz
extracted_from: C:\Stadium 6 Web Apps\87ea91de-6125-4686-8437-806216cb0ec0
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Business rules & behaviour — RMB_Onboarding

## Tier-A — event logic (scripts → action sequences)

> Each script is classified by its **trigger** (0g): *user-initiated* (a control event — `.Click/.Change/…`), *automatic-on-open* (a page/template `.Load`), or *other* (a helper invoked via CallScript, or a timer/lifecycle hook). User-initiated scripts are rendered gesture-first; the *goal* a gesture serves is advisory (Tier-B), the gesture itself is fact.

### User-initiated — gesture → outcome

#### btnAddServiceRequest.Click  [from script, surface: ClientServiceRequest]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=pgClientDetails

#### dgSearchCustomers.Launch.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks `dgSearchCustomers` → runs the flow below
- Sequence: NavigateToPage → JavaScript
  - NavigateToPage: Destination=ClientServiceRequest
  - JavaScript  `[opaque: custom JS]`

#### btnCloseModal.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: SetValue → SetValue
  - SetValue: Target=Panel_Customers; Value=False
  - SetValue: Target=Panel_Products; Value=True

#### DataGrid.Edit.Click  [from script, surface: ClientApplications]
- Trigger: **user-initiated**  (`.click`)
- User clicks `DataGrid` → runs the flow below
- Sequence: Decision → IfPath → SetValue → SetValue → NavigateToPage → Notification
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `NextActionSequence < 50` →
      - SetValue: Target=ApplicationID; Value=ApplicationID
      - SetValue: Target=WOID; Value=WOID
      - NavigateToPage: Destination=pgModularInformation / ClientNumber / ApplicationID / WOID
    - ELSE →
      - Notification: Message=ApplicationID

#### DataGrid.Download.Click  [from script, surface: ClientApplications]
- Trigger: **user-initiated**  (`.click`)
- User clicks `DataGrid` → runs the flow below
- Sequence: Decision → IfPath → ExecuteConnector → Decision → IfPath → ExecuteConnector → Decision → IfPath → ExecuteConnector → DownloadFile → Notification → Notification → Notification
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `NextActionSequence >= 50` →
      - ExecuteConnector: ConnectorFunction=get_ApplicationFile
      - **Decision** *(has else)*
        - IF `FileName != ''` →
          - ExecuteConnector: ConnectorFunction=FileExists
          - **Decision** *(has else)*
            - IF `FileSystemData_FileExists == true` →
              - ExecuteConnector: ConnectorFunction=ReadFile
              - DownloadFile
            - ELSE →
              - Notification: Message=FileName
        - ELSE →
          - Notification: Message=No file returned
    - ELSE →
      - Notification: Message=Application file not generated; Title=File not available

#### DataGrid.History.Click  [from script, surface: ClientApplications]
- Trigger: **user-initiated**  (`.click`)
- User clicks `DataGrid` → runs the flow below
- Sequence: CallScript → SetValue → SetValue → ExecuteConnector → SetValue
  - CallScript: ScriptToCall=ModalOpen
  - SetValue: Target=tbApplicationNumer; Value=ApplicationID
  - SetValue: Target=tbCustomerName; Value=ClientName
  - ExecuteConnector: ConnectorFunction=Sp_History_Get
  - SetValue: Target=Data; Value=Results

#### btnCloseModal.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=ModalClose

#### dgClientApplicationUnlocated.AllocateLink.Click  [from script, surface: Enablement]
- Trigger: **user-initiated**  (`.click`)
- User clicks `dgClientApplicationUnlocated` → runs the flow below
- Sequence: Decision → IfPath → Notification → ExecuteConnector → Decision → IfPath → ExecuteConnector → Notification → CallScript → Notification
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `Status == 60` →
      - Notification: Message=Application already vetted
    - ELSE →
      - ExecuteConnector: ConnectorFunction=Sp_ClientApplications_Allocate_Insert
      - **Decision** *(has else)*
        - IF `Success == 1` →
          - ExecuteConnector: ConnectorFunction=Prc_WOHistory_insert1
          - Notification: Message=Application allocated
          - CallScript: ScriptToCall=LoadDatagrids
        - ELSE →
          - Notification: Message=Message

#### dgClientApplicationAllocated.Vetting.Click  [from script, surface: Enablement]
- Trigger: **user-initiated**  (`.click`)
- User clicks `dgClientApplicationAllocated` → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → Variable → SetValue → SetValue → SetValue → SetValue → CallScript → CallScript → Decision → IfPath → SetValue → SetValue → Notification
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Sp_FileImage_Get
  - **Decision** *(has else)*
    - IF `Count > 0` →
      - Variable: Value=ApplicationID
      - SetValue: Target=ApplicationID; Value=ApplicationID
      - SetValue: Target=WOID; Value=WOID
      - SetValue: Target=Container_Enablement_ClientApplications; Value=False
      - SetValue: Target=Container_Enablement_VettingScreen; Value=True
      - CallScript: ScriptToCall=SetValueVettingInfo
      - CallScript: ScriptToCall=LoadImage
      - **Decision** *(has else)*
        - IF `ActionSequence == 60` →
          - SetValue: Target=Container_AcceptRejectButtons; Value=False
        - ELSE →
          - SetValue: Target=Container_AcceptRejectButtons; Value=True
    - ELSE →
      - Notification: Message=Application Loading

#### btnNextPageLeft.Click  [from script, surface: Enablement]
- Trigger: **user-initiated**  (`.click`)
- User clicks "<" → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → Variable → Variable → Decision → IfPath → Variable → ExecuteConnector → SetValue → SetValue → SetValue
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Sp_FileImage_Get
  - **Decision** *(has else)*
    - IF `Success == 1` →
      - Variable: Value=lblPageNumber
      - Variable: Value=Count
      - **Decision** *(has else)*
        - IF `VariableCurrentPage > 1` →
          - Variable: Value=lblPageNumber
          - ExecuteConnector: ConnectorFunction=ReadFile
          - SetValue: Target=imgVettingInfo_Document; Value=FileSystem_ReadFile
          - SetValue: Target=lblPageCount; Value=Count
          - SetValue: Target=lblPageNumber; Value=VariableNextPage
        - ELSE →
    - ELSE →

#### btnNextPageRight.Click  [from script, surface: Enablement]
- Trigger: **user-initiated**  (`.click`)
- User clicks ">" → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → Variable → Variable → Decision → IfPath → ExecuteConnector → SetValue → SetValue → SetValue
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Sp_FileImage_Get
  - **Decision** *(has else)*
    - IF `Success == 1` →
      - Variable: Value=lblPageNumber
      - Variable: Value=Count
      - **Decision** *(has else)*
        - IF `VariableCurrentPage < Count` →
          - ExecuteConnector: ConnectorFunction=ReadFile
          - SetValue: Target=imgVettingInfo_Document; Value=FileSystem_ReadFile
          - SetValue: Target=lblPageNumber; Value=VariableCurrentPage
          - SetValue: Target=lblPageCount; Value=Count
        - ELSE →
    - ELSE →

#### cbJointly.Change  [from script, surface: Enablement]
- Trigger: **user-initiated**  (`.change`)
- User changes `cbJointly` → runs the flow below
- Sequence: SetValue → SetValue
  - SetValue: Target=lblJointCount; Value=cbJointly
  - SetValue: Target=tbCount; Value=cbJointly

#### btnEnablementReject.Click  [from script, surface: Enablement]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Reject" → runs the flow below
- Sequence: SetValue → SetValue
  - SetValue: Target=Container_Reject; Value=True
  - SetValue: Target=Container_AcceptRejectButtons; Value=False

#### btnEnablement_Accept.Click  [from script, surface: Enablement]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Accept" → runs the flow below
- Sequence: Async → ExecuteConnector → ExecuteConnector → Notification → SetValue → SetValue → SetValue → SetValue → CallScript
  - ExecuteConnector: ConnectorFunction=Prc_WO_Update
  - ExecuteConnector: ConnectorFunction=Prc_WOHistory_insert1
  - Notification: Message=Application has been accepted; Title=Accepted
  - SetValue: Target=Container_AcceptRejectButtons; Value=False
  - SetValue: Target=Container_Enablement_ClientApplications; Value=True
  - SetValue: Target=Container_Enablement_VettingScreen; Value=False
  - SetValue: Target=WOID; Value=0
  - CallScript: ScriptToCall=LoadDatagrids

#### btnCancelReject_Back.Click  [from script, surface: Enablement]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Back" → runs the flow below
- Sequence: SetValue → SetValue → SetValue
  - SetValue: Target=tbEnablement_RejectReason
  - SetValue: Target=Container_Reject; Value=False
  - SetValue: Target=Container_AcceptRejectButtons; Value=True

#### btnAcceptReject.Click  [from script, surface: Enablement]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Reject" → runs the flow below
- Sequence: ExecuteConnector → ExecuteConnector → ExecuteConnector → Notification → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=Prc_WO_update
  - ExecuteConnector: ConnectorFunction=Prc_WOHistory_insert
  - ExecuteConnector: ConnectorFunction=Prc_WO_update
  - Notification: Message=Application has been rejected; Title=Accepted
  - SetValue: Target=Container_AcceptRejectButtons; Value=False
  - SetValue: Target=Container_Reject; Value=False
  - SetValue: Target=tbEnablement_RejectReason

#### btnEnablement_Vetting_Close.Click  [from script, surface: Enablement]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: SetValue → SetValue
  - SetValue: Target=Container_Enablement_ClientApplications; Value=True
  - SetValue: Target=Container_Enablement_VettingScreen; Value=False

#### btnClose.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=ClientServiceRequest

#### btnSave.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: ExecuteConnector → CallScript
  - ExecuteConnector: ConnectorFunction=Prc_ClientDetails_Insert
  - CallScript: ScriptToCall=Application_Create

#### dgExistingClient.Launch.Click  [from script, surface: pgClientDetails]
- Trigger: **user-initiated**  (`.click`)
- User clicks `dgExistingClient` → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=Application_Create

#### chbLinkCCN.Change  [from script, surface: pgModularInformation]
- Trigger: **user-initiated**  (`.change`)
- User changes `chbLinkCCN` → runs the flow below
- Sequence: Decision → IfPath → SetValue → SetValue
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `chbLinkCCN == True` →
      - SetValue: Target=LayoutTable3; Value=True
    - ELSE →
      - SetValue: Target=LayoutTable3; Value=False

#### btnSave.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → ExecuteConnector → Notification → ExecuteConnector → Notification
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=get_CheckModularInformationExists
  - **Decision** *(has else)*
    - IF `ModularInformationExists == 1` →
      - ExecuteConnector: ConnectorFunction=Prc_ModularInformation_Update
      - Notification: Message=Details Updated Successfully; Title=Success
    - ELSE →
      - ExecuteConnector: ConnectorFunction=Prc_ModularInformation_Insert
      - Notification: Message=Details Captured Successfully; Title=Success

#### btnClose.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=ClientServiceRequest

#### btnNext.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Next" → runs the flow below
- Sequence: CallScript → Decision → IfPath → ExecuteConnector → Decision → IfPath → ExecuteConnector → Notification → NavigateToPage → ExecuteConnector → Notification → NavigateToPage → ExecuteConnector → Notification
- Flow (branch-structured):
  - CallScript: ScriptToCall=Validate
  - **Decision** *(has else)*
    - IF `Valid == true` →
      - ExecuteConnector: ConnectorFunction=get_CheckModularInformationExists
      - **Decision** *(has else)*
        - IF `ModularInformationExists == 1` →
          - ExecuteConnector: ConnectorFunction=Prc_ModularInformation_Update
          - Notification: Message=Details Updated Successfully; Title=Success
          - NavigateToPage: Destination=pgCollections / ApplicationID / ClientID / WOID
        - ELSE →
          - ExecuteConnector: ConnectorFunction=Prc_ModularInformation_Insert
          - Notification: Message=Details Captured Successfully; Title=Success
          - NavigateToPage: Destination=pgCollections / ApplicationID / ClientID / WOID
      - ExecuteConnector: ConnectorFunction=sp_Create_Application_Steps_UpdateValid
    - ELSE →
      - Notification: Message=Invalid Fields

#### dgModularEntities.View.Click  [from script, surface: pgModularInformation]
- Trigger: **user-initiated**  (`.click`)
- User clicks `dgModularEntities` → runs the flow below
- Sequence: ExecuteConnector → CallScript → CallScript → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=get_ModularEntity
  - CallScript: ScriptToCall=LoadEntities_ModalView
  - CallScript: ScriptToCall=OpenModal
  - SetValue: Target=btnModalAdd; Value=False
  - SetValue: Target=btnModalUpdate; Value=True

#### btnAddEntity.Click  [from script, surface: pgModularInformation]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add Entity" → runs the flow below
- Sequence: CallScript → CallScript → SetValue → SetValue
  - CallScript: ScriptToCall=OpenModal
  - CallScript: ScriptToCall=ClearModal
  - SetValue: Target=btnModalAdd; Value=True
  - SetValue: Target=btnModalUpdate; Value=False

#### btnModalAdd.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add" → runs the flow below
- Sequence: ExecuteConnector → CallScript → Notification → CallScript
  - ExecuteConnector: ConnectorFunction=Prc_ModularEntity_Insert
  - CallScript: ScriptToCall=CloseModal
  - Notification: Message=Success; Title=Entity Captured Successfully
  - CallScript: ScriptToCall=LoadEntities

#### btnModalUpdate.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Update" → runs the flow below
- Sequence: ExecuteConnector → CallScript → Notification → CallScript
  - ExecuteConnector: ConnectorFunction=Prc_ModularEntity_Update
  - CallScript: ScriptToCall=CloseModal
  - Notification: Message=Success; Title=Entity Updated Successfully
  - CallScript: ScriptToCall=LoadEntities

#### btnModalClose.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=CloseModal

#### btnAdd.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add" → runs the flow below
- Sequence: CallScript → CallScript → SetValue → SetValue
  - CallScript: ScriptToCall=OpenModal
  - CallScript: ScriptToCall=ClearModal
  - SetValue: Target=btnModalAdd; Value=True
  - SetValue: Target=btnModalUpdate; Value=False

#### btnView.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "View" → runs the flow below
- Sequence: ExecuteConnector → CallScript → CallScript → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=get_CollectionsContactPerson
  - CallScript: ScriptToCall=LoadContactPersons_ModalView
  - CallScript: ScriptToCall=OpenModal
  - SetValue: Target=btnModalAdd; Value=False
  - SetValue: Target=btnModalUpdate; Value=True

#### btnRemove.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Remove" → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → CallScript → Notification → Notification
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Prc_CollectionsContactPerson_Disable
  - **Decision** *(has else)*
    - IF `Success == 1` →
      - CallScript: ScriptToCall=LoadContactPersons
      - Notification: Message=Signatory Removed
    - ELSE →
      - Notification: Message=Could not delete

#### btnPrevious.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Previous" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=pgModularInformation / ApplicationID / ClientID / WOID

#### btnNext.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Next" → runs the flow below
- Sequence: CallScript → Decision → IfPath → ExecuteConnector → Decision → IfPath → ExecuteConnector → Notification → ExecuteConnector → Notification → ExecuteConnector → NavigateToPage → Notification
- Flow (branch-structured):
  - CallScript: ScriptToCall=Validate
  - **Decision** *(has else)*
    - IF `Valid == true` →
      - ExecuteConnector: ConnectorFunction=get_CheckCollectionsExists
      - **Decision** *(has else)*
        - IF `CollectionsExists == 1` →
          - ExecuteConnector: ConnectorFunction=Prc_Collections_Update
          - Notification: Message=Details Updated Successfully; Title=Success
        - ELSE →
          - ExecuteConnector: ConnectorFunction=Prc_Collections_Insert
          - Notification: Message=Details Captured Successfully; Title=Success
      - ExecuteConnector: ConnectorFunction=sp_Create_Application_Steps_UpdateValid
      - NavigateToPage: Destination=pgAdministrators
    - ELSE →
      - Notification: Message=Information needed

#### btnModalAdd.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add" → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → SetValue → CallScript → CallScript → Notification
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Prc_CollectionsContactPerson_Insert
  - **Decision** *(has else)*
    - IF `Success == 1` →
      - SetValue: Target=List; Value=[]
      - CallScript: ScriptToCall=LoadContactPersons
      - CallScript: ScriptToCall=CloseModal
      - Notification: Message=Contact Person Captured Successfully; Title=Success
    - ELSE →

#### btnModalUpdate.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Update" → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → CallScript → CallScript → Notification
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Prc_CollectionsContactPerson_Update
  - **Decision** *(has else)*
    - IF `Success == 1` →
      - CallScript: ScriptToCall=LoadContactPersons
      - CallScript: ScriptToCall=CloseModal
      - Notification: Message=Success; Title=Contact Person Updated Successfully
    - ELSE →

#### btnModalClose.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=CloseModal

#### btnView.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "View" → runs the flow below
- Sequence: ExecuteConnector → CallScript → CallScript → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=get_Administrator
  - CallScript: ScriptToCall=OpenModal
  - CallScript: ScriptToCall=LoadAdministrators_ModalView
  - SetValue: Target=btnModalUpdate; Value=True
  - SetValue: Target=btnModalAdd; Value=False

#### btnRemove.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Remove" → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → CallScript → Notification → Notification
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Prc_Administrators_Disable
  - **Decision** *(has else)*
    - IF `Success == 1` →
      - CallScript: ScriptToCall=LoadAdministrators
      - Notification: Message=Administrator Removed
    - ELSE →
      - Notification: Message=Could not delete

#### btnAdd.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add" → runs the flow below
- Sequence: CallScript → CallScript → SetValue → SetValue
  - CallScript: ScriptToCall=OpenModal
  - CallScript: ScriptToCall=ClearModal
  - SetValue: Target=btnModalAdd; Value=True
  - SetValue: Target=btnModalUpdate; Value=False

#### btnPrevious.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Previous" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=pgCollections

#### btnNext.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Next" → runs the flow below
- Sequence: CallScript → Decision → IfPath → NavigateToPage → ExecuteConnector → Notification
- Flow (branch-structured):
  - CallScript: ScriptToCall=Validate
  - **Decision** *(has else)*
    - IF `Valid == true` →
      - NavigateToPage: Destination=pgAccounts
      - ExecuteConnector: ConnectorFunction=sp_Create_Application_Steps_UpdateValid
    - ELSE →
      - Notification: Message=Add administrators to continue

#### ddAddUSer_IDType.Change  [from script, surface: pgAdministrators]
- Trigger: **user-initiated**  (`.change`)
- User changes `ddAddUSer_IDType` → runs the flow below
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### btnModalAdd.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add" → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → CallScript → Notification → CallScript
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Prc_Administrators_Insert
  - **Decision** *(has else)*
    - IF `Success == 1` →
      - CallScript: ScriptToCall=CloseModal
      - Notification: Message=Administrator Captured Successfully; Title=Success
      - CallScript: ScriptToCall=LoadAdministrators
    - ELSE →

#### btnModalUpdate.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Update" → runs the flow below
- Sequence: ExecuteConnector → CallScript → Notification → CallScript
  - ExecuteConnector: ConnectorFunction=Prc_Administrators_Update
  - CallScript: ScriptToCall=CloseModal
  - Notification: Message=Success; Title=Administrator Updated Successfully
  - CallScript: ScriptToCall=LoadAdministrators

#### btnModalClose.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=CloseModal

#### btnLinkAccount1.Click  [from script, surface: pgAccounts]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Link Account" → runs the flow below
- Sequence: CallScript → CallScript → SetValue → SetValue
  - CallScript: ScriptToCall=OpenModal
  - CallScript: ScriptToCall=ClearModal
  - SetValue: Target=btnModalAdd; Value=True
  - SetValue: Target=btnModalUpdate; Value=False

#### btnAddSubgroup.Click  [from script, surface: pgAccounts]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add Sub Group" → runs the flow below
- Sequence: SetValue → SetValue
  - SetValue: Target=fbSubGroup2; Value=True
  - SetValue: Target=btnRemoveSubgroup; Value=True

#### btnView.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "View" → runs the flow below
- Sequence: ExecuteConnector → CallScript → CallScript → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=get_PartiesHeirarchyTable
  - CallScript: ScriptToCall=LoadLinkedAccounts_ModalView
  - CallScript: ScriptToCall=OpenModal
  - SetValue: Target=btnModalAdd; Value=False
  - SetValue: Target=btnModalUpdate; Value=True

#### btnLinkAccount2.Click  [from script, surface: pgAccounts]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Link Account" → runs the flow below
- Sequence: SetValue
  - SetValue: Value=True

#### btnRemoveSubgroup.Click  [from script, surface: pgAccounts]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Remove Sub Group" → runs the flow below
- Sequence: SetValue → SetValue → SetValue
  - SetValue: Target=fbSubGroup2; Value=False
  - SetValue: Value=False
  - SetValue: Target=btnRemoveSubgroup; Value=False

#### btnPrevious.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Previous" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=pgAdministrators

#### btnNext.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Next" → runs the flow below
- Sequence: CallScript → Decision → IfPath → ExecuteConnector → Decision → IfPath → ExecuteConnector → Notification → NavigateToPage → ExecuteConnector → Notification → NavigateToPage → ExecuteConnector → Notification
- Flow (branch-structured):
  - CallScript: ScriptToCall=Validate
  - **Decision** *(has else)*
    - IF `Valid == true` →
      - ExecuteConnector: ConnectorFunction=get_EntitiesExist
      - **Decision** *(has else)*
        - IF `EntitiesExists == 1` →
          - ExecuteConnector: ConnectorFunction=Prc_HeirarchyEntities_Update
          - Notification: Message=Details Updated Successfully; Title=Success
          - NavigateToPage: Destination=pgSignatories
        - ELSE →
          - ExecuteConnector: ConnectorFunction=Prc_HeirarchyEntities_Insert
          - Notification: Message=Details Captured Successfully; Title=Success
          - NavigateToPage: Destination=pgSignatories
      - ExecuteConnector: ConnectorFunction=sp_Create_Application_Steps_UpdateValid
    - ELSE →
      - Notification: Message=Missing Information

#### btnModalAdd.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add" → runs the flow below
- Sequence: Decision → IfPath → ExecuteConnector → Decision → IfPath → SetValue → CallScript → CallScript → Notification → Notification → Notification
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `tbAccountName != '' AND tbAccountNumber != ''` →
      - ExecuteConnector: ConnectorFunction=Prc_PartiesHeirarchy_Insert
      - **Decision** *(has else)*
        - IF `Success == 1` →
          - SetValue: Target=List; Value=[]
          - CallScript: ScriptToCall=LoadLinkedAccounts
          - CallScript: ScriptToCall=CloseModal
          - Notification: Message=Account Linked Succesfully; Title=Success
        - ELSE →
          - Notification: Message=Account Could not be linked; Title=Failed to link
    - ELSE →
      - Notification: Message=Account Linked Succesfully; Title=Validation

#### btnModalUpdate.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Update" → runs the flow below
- Sequence: Decision → IfPath → ExecuteConnector → Decision → IfPath → SetValue → CallScript → CallScript → Notification → Notification → Notification
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `tbAccountName != '' AND tbAccountNumber != ''` →
      - ExecuteConnector: ConnectorFunction=Prc_PartiesHeirarchy_Update
      - **Decision** *(has else)*
        - IF `Success == 1` →
          - SetValue: Target=List; Value=[]
          - CallScript: ScriptToCall=LoadLinkedAccounts
          - CallScript: ScriptToCall=CloseModal
          - Notification: Message=Linked account updated; Title=Success
        - ELSE →
          - Notification: Message=Account could not be updated; Title=Failed to update
    - ELSE →
      - Notification: Message=Account Linked Succesfully; Title=Validation

#### btnModalClose.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=CloseModal

#### btnView.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "View" → runs the flow below
- Sequence: ExecuteConnector → CallScript → CallScript → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=get_Signatory
  - CallScript: ScriptToCall=OpenModal
  - CallScript: ScriptToCall=LoadSignatories_ModalView
  - SetValue: Target=btnModalUpdate; Value=True
  - SetValue: Target=btnModalAdd; Value=False

#### btnRemove.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Remove" → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → CallScript → Notification → Notification
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Prc_SignatureField_Disable
  - **Decision** *(has else)*
    - IF `Success == 1` →
      - CallScript: ScriptToCall=LoadSignatories
      - Notification: Message=Signatory Removed
    - ELSE →
      - Notification: Message=Could not delete

#### btnAdd.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add" → runs the flow below
- Sequence: CallScript → CallScript → SetValue → SetValue
  - CallScript: ScriptToCall=OpenModal
  - CallScript: ScriptToCall=ClearModal
  - SetValue: Target=btnModalAdd; Value=True
  - SetValue: Target=btnModalUpdate; Value=False

#### btnPrevious.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Previous" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=pgAccounts

#### btnNext.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Next" → runs the flow below
- Sequence: CallScript → Decision → IfPath → ExecuteConnector → NavigateToPage → Notification
- Flow (branch-structured):
  - CallScript: ScriptToCall=Validate
  - **Decision** *(has else)*
    - IF `Valid == true` →
      - ExecuteConnector: ConnectorFunction=sp_Create_Application_Steps_UpdateValid
      - NavigateToPage: Destination=pgGenerate
    - ELSE →
      - Notification: Message=Add signatories to continue

#### ddAddIDType.Change  [from script, surface: pgSignatories]
- Trigger: **user-initiated**  (`.change`)
- User changes `ddAddIDType` → runs the flow below
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### btnModalAdd.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add" → runs the flow below
- Sequence: Decision → IfPath → ExecuteConnector → Decision → IfPath → SetValue → CallScript → CallScript → Notification → Notification → Notification
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `txtModalFullName != '' AND txtModalDesignation != '' AND txtModalIDPassport != ''` →
      - ExecuteConnector: ConnectorFunction=Prc_SignatureField_Insert
      - **Decision** *(has else)*
        - IF `Success == 1` →
          - SetValue: Target=List; Value=[]
          - CallScript: ScriptToCall=LoadSignatories
          - CallScript: ScriptToCall=CloseModal
          - Notification: Message=Account Linked Succesfully; Title=Success
        - ELSE →
          - Notification: Message=Signatory could not be added; Title=Failed to add
    - ELSE →
      - Notification: Message=Information Needed; Title=Validation

#### btnModalUpdate.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Update" → runs the flow below
- Sequence: ExecuteConnector → CallScript → CallScript → Notification
  - ExecuteConnector: ConnectorFunction=Prc_Signatories_Update
  - CallScript: ScriptToCall=CloseModal
  - CallScript: ScriptToCall=LoadSignatories
  - Notification: Message=Signatory Updated

#### btnModalClose.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=CloseModal

#### btnPrevious.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Previous" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=pgSignatories

#### btnGenerate.Click  [from script, surface: pgGenerate]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Generate" → runs the flow below
- Sequence: CallScript → Decision → IfPath → ExecuteConnector → ExecuteConnector → Notification → NavigateToPage
- Flow (branch-structured):
  - CallScript: ScriptToCall=Validate
  - **Decision** *(has else)*
    - IF `Valid == true` →
      - ExecuteConnector: ConnectorFunction=Prc_WO_Update
      - ExecuteConnector: ConnectorFunction=Prc_WOHistory_insert1
      - Notification: Message=Application has been generated; Title=Generated
      - NavigateToPage: Destination=ClientApplications
    - ELSE →

#### imgOpenMenu.Click  [from script, surface: DefaultTemplate]
- Trigger: **user-initiated**  (`.click`)
- User clicks `imgOpenMenu` → runs the flow below
- Sequence: JavaScript → SetValue → SetValue
  - JavaScript  `[opaque: custom JS]`
  - SetValue: Target=imgOpenMenu; Value=False
  - SetValue: Target=imgCloseMenu; Value=True

#### imgCloseMenu.Click  [from script, surface: DefaultTemplate]
- Trigger: **user-initiated**  (`.click`)
- User clicks `imgCloseMenu` → runs the flow below
- Sequence: JavaScript → SetValue → SetValue
  - JavaScript  `[opaque: custom JS]`
  - SetValue: Target=imgOpenMenu; Value=True
  - SetValue: Target=imgCloseMenu; Value=False

#### imgLogo.Click  [from script, surface: DefaultTemplate]
- Trigger: **user-initiated**  (`.click`)
- User clicks `imgLogo` → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=StartPage

#### btnClose.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Close" → runs the flow below
- Sequence: JavaScript → SetValue → SetValue
  - JavaScript  `[opaque: custom JS]`
  - SetValue: Target=imgOpenMenu; Value=True
  - SetValue: Target=imgCloseMenu; Value=False

### Automatic — on page / template open

#### ClientServiceRequest.Load  [from script, surface: ClientServiceRequest]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → CallScript → SetValue → SetValue → CallScript
  - CallScript: ScriptToCall=SetMenu
  - CallScript: ScriptToCall=Tiles
  - SetValue: Target=Panel_Customers; Value=False
  - SetValue: Target=Panel_Products; Value=True
  - CallScript: ScriptToCall=SetDataGrid

#### ClientApplications.Load  [from script, surface: ClientApplications]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → ExecuteConnector → SetValue
  - CallScript: ScriptToCall=SetMenu
  - ExecuteConnector: ConnectorFunction=Prc_Application_GetAll
  - SetValue: Target=Data

#### Enablement.Load  [from script, surface: Enablement]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → SetValue → SetValue → SetValue → Variable → CallScript
  - CallScript: ScriptToCall=SetMenu
  - SetValue: Target=lblEnablement_Header; Value=Client Applications
  - SetValue: Target=Container_Enablement_ClientApplications; Value=True
  - SetValue: Target=Container_Enablement_VettingScreen; Value=False
  - CallScript: ScriptToCall=LoadDatagrids

#### Dashboard.Load  [from script, surface: Dashboard]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=SetMenu

#### pgClientDetails.Load  [from script, surface: pgClientDetails]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → CallScript → ExecuteConnector → SetValue
  - CallScript: ScriptToCall=ProgressBar
  - CallScript: ScriptToCall=ProgressBarUpdate
  - ExecuteConnector: ConnectorFunction=get_AllClientDetails
  - SetValue: Target=Data

#### pgModularInformation.Load  [from script, surface: pgModularInformation]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → CallScript → CallScript → ExecuteConnector → SetValue → SetValue → ExecuteConnector → Decision → IfPath → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue → Decision → IfPath → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
- Flow (branch-structured):
  - CallScript: ScriptToCall=ProgressBar
  - CallScript: ScriptToCall=ProgressBarUpdate
  - CallScript: ScriptToCall=LoadEntities
  - ExecuteConnector: ConnectorFunction=get_ClientDetails
  - SetValue: Target=txtClientName; Value=ClientName
  - SetValue: Target=txtClientRegNo; Value=ClientRegistrationNumber
  - ExecuteConnector: ConnectorFunction=get_CheckModularInformationExists
  - **Decision** *(has else)*
    - IF `ModularInformationExists == 1` →
      - ExecuteConnector: ConnectorFunction=get_ModularInformation
      - SetValue: Target=chbNomAccPayments; Value=ModularNominatedAccountPayments
      - SetValue: Target=chbOnceOffPayments; Value=ModularOnceOffPayments
      - SetValue: Target=chbTransfers; Value=ModularTransfers
      - SetValue: Target=chbCollections; Value=ModularCollections
      - SetValue: Target=chbSignatories; Value=ModularAandBSignatories
      - **Decision** *(has else)*
        - IF `ModularLinkCCNNumber1 == ? AND ModularLinkCCNNumber2 == ? AND ModularLinkCCNNumber3 == ? AND ModularLinkCCNNumber4 == ? AND ModularLinkCCNNumber5 == ? AND ModularLinkCCNNumber6 == ?` →
          - SetValue: Target=chbLinkCCN; Value=False
          - SetValue: Target=LayoutTable3; Value=False
        - ELSE →
          - SetValue: Target=chbLinkCCN; Value=True
          - SetValue: Target=LayoutTable3; Value=True
          - SetValue: Target=txtCCN1; Value=ModularLinkCCNNumber1
          - SetValue: Target=txtCCN2; Value=ModularLinkCCNNumber2
          - SetValue: Target=txtCCN3; Value=ModularLinkCCNNumber3
          - SetValue: Target=txtCCN4; Value=ModularLinkCCNNumber4
          - SetValue: Target=txtCCN5; Value=ModularLinkCCNNumber5
          - SetValue: Target=txtCCN6; Value=ModularLinkCCNNumber6
      - SetValue: Target=chbCashman; Value=ModularCashman
      - SetValue: Target=chbCashmanReports; Value=ModularCashmanReports
      - SetValue: Target=chbNAEDO; Value=ModularNAEDO
      - SetValue: Target=chbOnlineSettlementLimits; Value=ModularOnlineSettlementLimits
      - SetValue: Target=chbFTPDeliveryMechanism; Value=ModularFTPDeliveryMechanism
      - SetValue: Target=conModularEntities; Value=True
    - ELSE →

#### pgCollections.Load  [from script, surface: pgCollections]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → CallScript → JavaScript → JavaScript → CallScript → ExecuteConnector → SetValue → SetValue → ExecuteConnector → Decision → IfPath → ExecuteConnector → SetValue → SetValue → SetValue
- Flow (branch-structured):
  - CallScript: ScriptToCall=ProgressBar
  - CallScript: ScriptToCall=ProgressBarUpdate
  - JavaScript  `[opaque: custom JS]`
  - JavaScript  `[opaque: custom JS]`
  - CallScript: ScriptToCall=LoadContactPersons
  - ExecuteConnector: ConnectorFunction=get_ClientDetails
  - SetValue: Target=txtClientName; Value=ClientName
  - SetValue: Target=txtClientRegNo; Value=ClientRegistrationNumber
  - ExecuteConnector: ConnectorFunction=get_CheckCollectionsExists
  - **Decision** *(has else)*
    - IF `CollectionsExists == 1` →
      - ExecuteConnector: ConnectorFunction=get_Collections
      - SetValue: Target=txtCollAppClientName; Value=CollAppClientName
      - SetValue: Target=txtCollAppAccountNumber; Value=CollAppAccountNumber
      - SetValue: Target=txtCollAppBranchCode; Value=CollAppBranchCode
    - ELSE →

#### pgAdministrators.Load  [from script, surface: pgAdministrators]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → CallScript → CallScript → ExecuteConnector → SetValue → SetValue
  - CallScript: ScriptToCall=ProgressBar
  - CallScript: ScriptToCall=ProgressBarUpdate
  - CallScript: ScriptToCall=LoadAdministrators
  - ExecuteConnector: ConnectorFunction=get_ClientDetails
  - SetValue: Target=txtClientName; Value=ClientName
  - SetValue: Target=txtClientRegNo; Value=ClientRegistrationNumber

#### pgAccounts.Load  [from script, surface: pgAccounts]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → CallScript → ExecuteConnector → SetValue → SetValue → ExecuteConnector → CallScript → Decision → IfPath → ExecuteConnector → SetValue → SetValue
- Flow (branch-structured):
  - CallScript: ScriptToCall=ProgressBar
  - CallScript: ScriptToCall=ProgressBarUpdate
  - ExecuteConnector: ConnectorFunction=get_ClientDetails
  - SetValue: Target=txtClientName; Value=ClientName
  - SetValue: Target=txtClientRegNo; Value=ClientRegistrationNumber
  - ExecuteConnector: ConnectorFunction=get_CheckHeirarchyEntitiesExists
  - CallScript: ScriptToCall=LoadLinkedAccounts
  - **Decision** *(has else)*
    - IF `HeirarchyEntitiesExists == 1` →
      - ExecuteConnector: ConnectorFunction=get_HeirarchyEntities
      - SetValue: Target=txtEntityName1; Value=EntityName
      - SetValue: Target=txtEntityNumber1; Value=EntityNumber
    - ELSE →

#### pgSignatories.Load  [from script, surface: pgSignatories]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → CallScript → CallScript → ExecuteConnector → SetValue → SetValue
  - CallScript: ScriptToCall=ProgressBar
  - CallScript: ScriptToCall=ProgressBarUpdate
  - CallScript: ScriptToCall=LoadSignatories
  - ExecuteConnector: ConnectorFunction=get_ClientDetails
  - SetValue: Target=txtClientName; Value=ClientName
  - SetValue: Target=txtClientRegNo; Value=ClientRegistrationNumber

#### pgGenerate.Load  [from script, surface: pgGenerate]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → CallScript → ExecuteConnector → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → JavaScript
  - CallScript: ScriptToCall=ProgressBar
  - CallScript: ScriptToCall=ProgressBarUpdate
  - ExecuteConnector: ConnectorFunction=sp_Application_Steps_Get
  - ExecuteConnector: ConnectorFunction=get_ClientDetails
  - SetValue: Target=txtClientName; Value=ClientName
  - SetValue: Target=txtClientRegNo; Value=ClientRegistrationNumber
  - SetValue: Target=Data; Value=Results
  - SetValue: Target=tbEmail
  - JavaScript  `[opaque: custom JS]`

#### DefaultTemplate.Load  [from script, surface: app]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

### Other — helper scripts / timers / lifecycle

#### SetMenu  [from script, surface: ClientServiceRequest]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### GetClientsInformation  [from script, surface: ClientServiceRequest]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=GetClients
  - SetValue: Target=Data

#### Tiles  [from script, surface: ClientServiceRequest]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### SetDataGrid  [from script, surface: ClientServiceRequest]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### SetMenu  [from script, surface: ClientApplications]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### ModalClose  [from script, surface: ClientApplications]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### ModalOpen  [from script, surface: ClientApplications]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### DataGridFormat  [from script, surface: ClientApplications]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### SetMenu  [from script, surface: Enablement]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### ModalClose  [from script, surface: Enablement]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### ModalOpen  [from script, surface: Enablement]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### LoadDatagrids  [from script, surface: Enablement]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue → ExecuteConnector → SetValue → CallScript
  - ExecuteConnector: ConnectorFunction=Sp_ClientApplications_Get
  - SetValue: Target=Data
  - ExecuteConnector: ConnectorFunction=Sp_ClientApplicationsUnallocated_Get
  - SetValue: Target=Data
  - CallScript: ScriptToCall=DataGridFormat

#### DataGridFormat  [from script, surface: Enablement]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### SetValueVettingInfo  [from script, surface: Enablement]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue
  - SetValue: Target=tbVettingInfo_ApplicationID; Value=ClickedRow
  - SetValue: Target=tbVettingInfo_ClientName; Value=ClickedRow
  - SetValue: Target=tbVettingInfo_ClientNumber; Value=ClickedRow

#### LoadImage  [from script, surface: Enablement]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → Decision → IfPath → Variable → Variable → ExecuteConnector → SetValue → SetValue → SetValue
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Sp_FileImage_Get
  - **Decision** *(has else)*
    - IF `Success == 1` →
      - Variable: Value=Count
      - Variable: Value=Results
      - ExecuteConnector: ConnectorFunction=ReadFile
      - SetValue: Target=imgVettingInfo_Document; Value=FileSystem_ReadFile
      - SetValue: Target=lblPageNumber; Value=1
      - SetValue: Target=lblPageCount; Value=Count
    - ELSE →

#### SetMenu  [from script, surface: Dashboard]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### Tiles  [from script, surface: Dashboard]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### ProgressBar  [from script, surface: pgClientDetails]
- Trigger: **other (helper script)**
- Sequence: Variable → JavaScript
  - Variable: Value=PanelID
  - JavaScript  `[opaque: custom JS]`

#### ProgressBarUpdate  [from script, surface: pgClientDetails]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### Application_Create  [from script, surface: pgClientDetails]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → Decision → IfPath → ExecuteConnector → ExecuteConnector → ExecuteConnector → SetValue → SetValue → SetValue → NavigateToPage
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=Prc_WO_Insert_1
  - **Decision** *(has else)*
    - IF `WOID > 0` →
      - ExecuteConnector: ConnectorFunction=Prc_Application_Insert
      - ExecuteConnector: ConnectorFunction=sp_Create_Application_Steps
      - ExecuteConnector: ConnectorFunction=sp_Create_Application_Steps_UpdateValid
      - SetValue: Target=ApplicationID; Value=ApplicationID_Returned
      - SetValue: Target=ClientID; Value=Client_ID
      - SetValue: Target=WOID; Value=WOID
      - NavigateToPage: Destination=pgModularInformation / ClientID / ApplicationID / WOID
    - ELSE →

#### Validate  [from script, surface: pgClientDetails]
- Trigger: **other (helper script)**
- Sequence: SetValue
  - SetValue: Target=Valid; Value=true

#### OpenModal  [from script, surface: pgModularInformation]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### CloseModal  [from script, surface: pgModularInformation]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### ProgressBar  [from script, surface: pgModularInformation]
- Trigger: **other (helper script)**
- Sequence: Variable → JavaScript
  - Variable: Value=PanelID
  - JavaScript  `[opaque: custom JS]`

#### LoadEntities  [from script, surface: pgModularInformation]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=Prc_ModularEntity_GetList
  - SetValue: Target=Data; Value=Results

#### LoadEntities_ModalView  [from script, surface: pgModularInformation]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue
  - SetValue: Target=txtModalEntityID; Value=EntityID
  - SetValue: Target=txtModalEntityName; Value=EntityName
  - SetValue: Target=txtModalEntityNumber; Value=EntityNumber

#### ClearModal  [from script, surface: pgModularInformation]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue
  - SetValue: Target=txtModalEntityName
  - SetValue: Target=txtModalEntityNumber

#### ProgressBarUpdate  [from script, surface: pgModularInformation]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### Validate  [from script, surface: pgModularInformation]
- Trigger: **other (helper script)**
- Sequence: SetValue
  - SetValue: Target=Valid; Value=true

#### OpenModal  [from script, surface: pgCollections]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### CloseModal  [from script, surface: pgCollections]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### ProgressBar  [from script, surface: pgCollections]
- Trigger: **other (helper script)**
- Sequence: Variable → JavaScript
  - Variable: Value=PanelID
  - JavaScript  `[opaque: custom JS]`

#### LoadContactPersons  [from script, surface: pgCollections]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=Prc_CollectionsContactPerson_GetList
  - SetValue: Target=List; Value=Results

#### ClearModal  [from script, surface: pgCollections]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - SetValue: Target=txtModalAbbreviatedName
  - SetValue: Target=txtModalAccountNo
  - SetValue: Target=txtModalCompanyName
  - SetValue: Target=txtModalContactEmail
  - SetValue: Target=txtModalContactName
  - SetValue: Target=txtModalContactTel

#### LoadContactPersons_ModalView  [from script, surface: pgCollections]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - SetValue: Target=txtModalContactPersonID; Value=ContactPersonID
  - SetValue: Target=txtModalAbbreviatedName; Value=ContPAbbreviatedName
  - SetValue: Target=txtModalAccountNo; Value=ContPAccountNumber
  - SetValue: Target=txtModalCompanyName; Value=ContPCompanyName
  - SetValue: Target=txtModalContactEmail; Value=ContPContactEmail
  - SetValue: Target=txtModalContactName; Value=ContPContactName
  - SetValue: Target=txtModalContactTel; Value=ContPContactTelNo

#### ProgressBarUpdate  [from script, surface: pgCollections]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### Validate  [from script, surface: pgCollections]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=get_ContactPersonCount
  - SetValue: Target=Valid; Value=Count

#### rptContactPerson.ItemLoad  [from script, surface: pgCollections]
- Trigger: **other (timer / lifecycle)**  (`.itemload`)
- Sequence: SetValue → SetValue → SetValue
  - SetValue: Target=txtContactPersonID; Value=ListItem
  - SetValue: Target=txtCompanyName; Value=ListItem
  - SetValue: Target=txtAccountNumber; Value=ListItem

#### CloseModal  [from script, surface: pgAdministrators]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### OpenModal  [from script, surface: pgAdministrators]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### ProgressBar  [from script, surface: pgAdministrators]
- Trigger: **other (helper script)**
- Sequence: Variable → JavaScript
  - Variable: Value=PanelID
  - JavaScript  `[opaque: custom JS]`

#### LoadAdministrators  [from script, surface: pgAdministrators]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=Prc_Administrators_GetList
  - SetValue: Target=List; Value=Results

#### ClearModal  [from script, surface: pgAdministrators]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue
  - SetValue: Target=txtModalFullName
  - SetValue: Target=txtModalIDPassport
  - SetValue: Target=txtModalCapacity

#### LoadAdministrators_ModalView  [from script, surface: pgAdministrators]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue → SetValue → SetValue
  - SetValue: Target=txtModalFullName; Value=AdminFullName
  - SetValue: Target=txtModalIDPassport; Value=AdminIDPassport
  - SetValue: Target=txtModalCapacity; Value=AdminCapacity
  - SetValue: Target=txtModalAdministratorID; Value=AdministratorID
  - SetValue: Target=ddAddUSer_IDType; Value=IDType

#### ProgressBarUpdate  [from script, surface: pgAdministrators]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### Validate  [from script, surface: pgAdministrators]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=get_AdministratorCount
  - SetValue: Target=Valid; Value=Count

#### ValidateID  [from script, surface: pgAdministrators]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### rptAdministrators.ItemLoad  [from script, surface: pgAdministrators]
- Trigger: **other (timer / lifecycle)**  (`.itemload`)
- Sequence: SetValue → SetValue → SetValue → SetValue
  - SetValue: Target=txtAdministratorID; Value=ListItem
  - SetValue: Target=txtFullName; Value=ListItem
  - SetValue: Target=txtIDPassport; Value=ListItem
  - SetValue: Target=txtCapacity; Value=ListItem

#### ProgressBar  [from script, surface: pgAccounts]
- Trigger: **other (helper script)**
- Sequence: Variable → JavaScript
  - Variable: Value=PanelID
  - JavaScript  `[opaque: custom JS]`

#### ProgressBarUpdate  [from script, surface: pgAccounts]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → Decision → IfPath → JavaScript → JavaScript
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=sp_Application_Step_Status
  - **Decision** *(has else)*
    - IF `IsValid == 1` →
      - JavaScript  `[opaque: custom JS]`
    - ELSE →
      - JavaScript  `[opaque: custom JS]`

#### OpenModal  [from script, surface: pgAccounts]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### ClearModal  [from script, surface: pgAccounts]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue
  - SetValue: Target=tbAccountName
  - SetValue: Target=tbAccountNumber
  - SetValue: Target=tbPartiesHeirarchyID

#### CloseModal  [from script, surface: pgAccounts]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### LoadLinkedAccounts  [from script, surface: pgAccounts]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=Prc_PartiesHeirarchy_GetList
  - SetValue: Target=List; Value=Results

#### Validate  [from script, surface: pgAccounts]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=get_PartiesHierarchCount
  - SetValue: Target=Valid; Value=Count

#### LoadLinkedAccounts_ModalView  [from script, surface: pgAccounts]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue
  - SetValue: Target=tbAccountName; Value=AccountName
  - SetValue: Target=tbAccountNumber; Value=AccountNumber
  - SetValue: Target=tbPartiesHeirarchyID; Value=PartiesHeirarchyID

#### rptLinkedContacts1.ItemLoad  [from script, surface: pgAccounts]
- Trigger: **other (timer / lifecycle)**  (`.itemload`)
- Sequence: SetValue → SetValue → SetValue
  - SetValue: Target=txtAccountName1; Value=ListItem
  - SetValue: Target=txtAccountNumber1; Value=ListItem
  - SetValue: Target=txtPartiesHeirarchyID; Value=ListItem

#### CloseModal  [from script, surface: pgSignatories]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### OpenModal  [from script, surface: pgSignatories]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### ProgressBar  [from script, surface: pgSignatories]
- Trigger: **other (helper script)**
- Sequence: Variable → JavaScript
  - Variable: Value=PanelID
  - JavaScript  `[opaque: custom JS]`

#### ProgressBarUpdate  [from script, surface: pgSignatories]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### Validate  [from script, surface: pgSignatories]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=get_SignatoryCount
  - SetValue: Target=Valid; Value=Count

#### LoadSignatories_ModalView  [from script, surface: pgSignatories]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue → SetValue → SetValue
  - SetValue: Target=txtModalFullName; Value=FullName
  - SetValue: Target=txtModalIDPassport; Value=IDPassport
  - SetValue: Target=txtModalDesignation; Value=Capacity
  - SetValue: Target=txtModalSignatoryID; Value=SignatoryID
  - SetValue: Target=ddAddIDType; Value=IDType

#### LoadSignatories  [from script, surface: pgSignatories]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=Prc_SignatureField_GetList
  - SetValue: Target=List; Value=Results

#### ClearModal  [from script, surface: pgSignatories]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue
  - SetValue: Target=txtModalFullName
  - SetValue: Target=txtModalIDPassport
  - SetValue: Target=txtModalDesignation

#### rptSignatories.ItemLoad  [from script, surface: pgSignatories]
- Trigger: **other (timer / lifecycle)**  (`.itemload`)
- Sequence: SetValue → SetValue → SetValue → SetValue → SetValue
  - SetValue: Target=txtFullName; Value=ListItem
  - SetValue: Target=txtDesignation; Value=ListItem
  - SetValue: Target=txtIDPassport; Value=ListItem
  - SetValue: Target=ddAddIDType; Value=ListItem
  - SetValue: Target=txtSignatoryID1; Value=ListItem

#### ProgressBar  [from script, surface: pgGenerate]
- Trigger: **other (helper script)**
- Sequence: Variable → JavaScript
  - Variable: Value=PanelID
  - JavaScript  `[opaque: custom JS]`

#### ProgressBarUpdate  [from script, surface: pgGenerate]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

#### Validate  [from script, surface: pgGenerate]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → Decision → IfPath → Decision → IfPath → SetValue → SetValue → Notification → Notification
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=get_InvalidSteps
  - **Decision** *(has else)*
    - IF `Count == 0` →
      - **Decision** *(has else)*
        - IF `tbEmail != ''` →
          - SetValue: Target=Valid; Value=true
        - ELSE →
          - SetValue: Target=Valid; Value=false
          - Notification: Message=Email is required to generate application; Title=Email required
    - ELSE →
      - Notification: Message=Fill in all information; Title=Missing Information

#### JumpToPageTop  [from script, surface: DefaultTemplate]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[opaque: custom JS]`

## Tier-A — notification points

> Verbatim message text (expressions preserved), severity decoded from `NotificationType` (1=success, 3=error, other=info), and dialog (blocking confirm) vs toast. These target the **current operator** (not an actor signal — see access-control).

- `DataGrid.Edit.Click` (ClientApplications) · toast · info — "'Cannot edit this Application: ' + {0}" [from design model]
- `DataGrid.Download.Click` (ClientApplications) · toast · info — "'File does not exist: ' + {0}" [from design model]
- `DataGrid.Download.Click` (ClientApplications) · toast · info — "No file returned" [from design model]
- `DataGrid.Download.Click` (ClientApplications) · toast · info — "Application file not generated" [from design model]
- `dgClientApplicationUnlocated.AllocateLink.Click` (Enablement) · toast · info — "Application already vetted" [from design model]
- `dgClientApplicationUnlocated.AllocateLink.Click` (Enablement) · toast · info — "Application allocated" [from design model]
- `dgClientApplicationUnlocated.AllocateLink.Click` (Enablement) · toast · info — "'User could not be allocated: ' + {0}" [from design model]
- `dgClientApplicationAllocated.Vetting.Click` (Enablement) · toast · info — "Application Loading" [from design model]
- `btnEnablement_Accept.Click` (Enablement) · toast · success — "Application has been accepted" [from design model]
- `btnAcceptReject.Click` (Enablement) · toast · info — "Application has been rejected" [from design model]
- `btnSave.Click` (app) · toast · success — "Details Updated Successfully" [from design model]
- `btnSave.Click` (app) · toast · success — "Details Captured Successfully" [from design model]
- `btnNext.Click` (app) · toast · success — "Details Updated Successfully" [from design model]
- `btnNext.Click` (app) · toast · success — "Details Captured Successfully" [from design model]
- `btnNext.Click` (app) · toast · info — "Invalid Fields" [from design model]
- `btnModalAdd.Click` (app) · toast · success — "Success" [from design model]
- `btnModalUpdate.Click` (app) · toast · success — "Success" [from design model]
- `btnRemove.Click` (app) · toast · info — "Signatory Removed" [from design model]
- `btnRemove.Click` (app) · toast · info — "Could not delete" [from design model]
- `btnNext.Click` (app) · toast · info — "Information needed" [from design model]
- `btnModalAdd.Click` (app) · toast · success — "Contact Person Captured Successfully" [from design model]
- `btnRemove.Click` (app) · toast · info — "Administrator Removed" [from design model]
- `btnNext.Click` (app) · toast · info — "Add administrators to continue" [from design model]
- `btnModalAdd.Click` (app) · toast · success — "Administrator Captured Successfully" [from design model]
- `btnNext.Click` (app) · toast · info — "Missing Information" [from design model]
- `btnModalAdd.Click` (app) · toast · success — "Account Linked Succesfully" [from design model]
- `btnModalAdd.Click` (app) · toast · error — "Account Could not be linked" [from design model]
- `btnModalAdd.Click` (app) · toast · info — "Account Linked Succesfully" [from design model]
- `btnModalUpdate.Click` (app) · toast · success — "Linked account updated" [from design model]
- `btnModalUpdate.Click` (app) · toast · error — "Account could not be updated" [from design model]
- `btnModalUpdate.Click` (app) · toast · info — "Account Linked Succesfully" [from design model]
- `btnNext.Click` (app) · toast · info — "Add signatories to continue" [from design model]
- `btnModalAdd.Click` (app) · toast · error — "Signatory could not be added" [from design model]
- `btnModalAdd.Click` (app) · toast · info — "Information Needed" [from design model]
- `btnModalUpdate.Click` (app) · toast · info — "Signatory Updated" [from design model]
- `Validate` (app) · toast · info — "Email is required to generate application" [from design model]
- `Validate` (app) · toast · info — "Fill in all information" [from design model]
- `btnGenerate.Click` (pgGenerate) · toast · success — "Application has been generated" [from design model]

## Tier-A — validation

- `txtCollAppClientName` · required · "Please enter some text" [from design model]
- `txtCollAppAccountNumber` · required · "Please enter some text" [from design model]
- `txtCollAppBranchCode` · required · "Please enter some text" [from design model]
- `txtModalContactPersonID` · required · "Please enter some text" [from design model]
- `txtModalAccountNo` · required · "Please enter some text" [from design model]
- `txtModalContactTel` · required · "Please enter some text" [from design model]
- `txtModalContactEmail` · required+email · /^[a-zA-Z0-9.!#$%&''*+\\/=?^_``{|}~-]{1,64}@[a-zA-Z0-9-]{1,64}\.[.a-zA-Z0-9-]{1,64}$/.test({0}) · "Please enter a valid email address" [from design model]  `[AI-SUGGESTED: email]`
- `txtModalFullName` · required · "Please enter some text" [from design model]
- `txtModalIDPassport` · required · "Please enter some text" [from design model]
- `txtModalCapacity` · required · "Please enter some text" [from design model]
- `txtEntityName1` · required · "Please enter some text" [from design model]
- `txtEntityNumber1` · required+numeric · /^[+-]?[0-9]\d*$/.test({0}) · "Please enter numbers only" [from design model]  `[AI-SUGGESTED: numeric]`
- `tbAccountName` · required · "Please enter some text" [from design model]
- `tbAccountNumber` · required · "Please enter some text" [from design model]
- `tbEmail` · required+email · /^[a-zA-Z0-9.!#$%&''*+\\/=?^_``{|}~-]{1,64}@[a-zA-Z0-9-]{1,64}\.[.a-zA-Z0-9-]{1,64}$/.test({0}) · "Please enter a valid email address" [from design model]  `[AI-SUGGESTED: email]`

## Tier-A — edge / empty / error / loading state signals

> The toggle / error-type / guard predicate is Tier-A (provably in the model). The **state classification** (loading vs empty vs error vs permission) is a Tier-B reading — a hidden control is ambiguous (busy vs empty vs initial-hide). See 0a / 0f above.

- **error notification** · `btnModalAdd.Click` (app) — "Account Could not be linked" [from design model]
- **error notification** · `btnModalUpdate.Click` (app) — "Account could not be updated" [from design model]
- **error notification** · `btnModalAdd.Click` (app) — "Signatory could not be added" [from design model]
- **visibility/loading toggle** · `Enablement.Load` (Enablement) — `Container_Enablement_ClientApplications` = True [from design model] `[AI-SUGGESTED: state=shown]`
- **visibility/loading toggle** · `Enablement.Load` (Enablement) — `Container_Enablement_VettingScreen` = False [from design model] `[AI-SUGGESTED: state=empty/hidden]`
- **visibility/loading toggle** · `dgClientApplicationAllocated.Vetting.Click` (Enablement) — `Container_Enablement_ClientApplications` = False [from design model] `[AI-SUGGESTED: state=empty/hidden]`
- **visibility/loading toggle** · `dgClientApplicationAllocated.Vetting.Click` (Enablement) — `Container_Enablement_VettingScreen` = True [from design model] `[AI-SUGGESTED: state=shown]`
- **visibility/loading toggle** · `dgClientApplicationAllocated.Vetting.Click` (Enablement) — `Container_AcceptRejectButtons` = False [from design model] `[AI-SUGGESTED: state=empty/hidden]`
- **visibility/loading toggle** · `dgClientApplicationAllocated.Vetting.Click` (Enablement) — `Container_AcceptRejectButtons` = True [from design model] `[AI-SUGGESTED: state=shown]`
- **visibility/loading toggle** · `btnEnablementReject.Click` (Enablement) — `Container_Reject` = True [from design model] `[AI-SUGGESTED: state=shown]`
- **visibility/loading toggle** · `btnCancelReject_Back.Click` (Enablement) — `Container_Reject` = False [from design model] `[AI-SUGGESTED: state=empty/hidden]`
- **empty/edge guard** · `dgClientApplicationAllocated.Vetting.Click` (Enablement) — IF `Count > 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `btnNextPageRight.Click` (Enablement) — IF `VariableCurrentPage < Count` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `Application_Create` (app) — IF `WOID > 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `Validate` (app) — IF `Count == 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
