---
stadium_asset: business-rules
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
# Business rules & behaviour — PaymentsApp

## Tier-A — event logic (scripts → action sequences)

> Each script is classified by its **trigger** (0g): *user-initiated* (a control event — `.Click/.Change/…`), *automatic-on-open* (a page/template `.Load`), or *other* (a helper invoked via CallScript, or a timer/lifecycle hook). User-initiated scripts are rendered gesture-first; the *goal* a gesture serves is advisory (Tier-B), the gesture itself is fact.

### User-initiated — gesture → outcome

#### SyncRolesButton.Click  [from script, surface: Roles]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Sync Stadium Roles" → runs the flow below
- Sequence: Async → ExecuteConnector → CallScript → Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=RoleSync
  - CallScript: ScriptToCall=NotificationHandler
  - ExecuteConnector: ConnectorFunction=RoleGetList
  - SetValue: Target=Data

#### AddUserButton.Click  [from script, surface: Users]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add User" → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → CallScript → SetValue → SetValue
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=EmailTextBox
  - SetValue: Target=FirstNameTextBox
  - SetValue: Target=LastNameTextBox
  - SetValue: Target=PasswordTextBox
  - SetValue: Target=IsAdministartorCheckBox; Value=False
  - SetValue: Target=RolesCheckBoxList; Value=[]
  - SetValue: Target=BusinessUnitDropDown
  - CallScript: ScriptToCall=LoadDropdownsAndCheckboxlists
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=false
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=false
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### UsersDataGrid.Edit.Click  [from script, surface: Users]
- Trigger: **user-initiated**  (`.click`)
- User clicks `UsersDataGrid` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → CallScript → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=UserGetById
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=EmailTextBox; Value=Email
  - SetValue: Target=FirstNameTextBox; Value=FirstName
  - SetValue: Target=LastNameTextBox; Value=LastName
  - CallScript: ScriptToCall=LoadDropdownsAndCheckboxlists
  - SetValue: Target=RolesCheckBoxList
  - SetValue: Target=BusinessUnitDropDown; Value=BusinessUnitId
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList
  - SetValue: Target=IsAdministartorCheckBox; Value=IsAdministrator
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### UsersDataGrid.Delete.Click  [from script, surface: Users]
- Trigger: **user-initiated**  (`.click`)
- User clicks `UsersDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript
  - DisplayMessageBox: Message=Email
  - ExecuteConnector: ConnectorFunction=UserDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=RefreshUsers

#### UsersDataGrid.ViewAssignedApprovalLevels.Click  [from script, surface: Users]
- Trigger: **user-initiated**  (`.click`)
- User clicks `UsersDataGrid` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → ExecuteConnector → SetValue
  - JavaScript  `[library JS: popups]`
  - ExecuteConnector: ConnectorFunction=UserApprovalLevelGetListByUserId
  - SetValue: Target=Data
  - _(+2 UI-state SetValue(s) folded into the state-signals section)_

#### UsersDataGrid.AssignApprovalLevels.Click  [from script, surface: Users]
- Trigger: **user-initiated**  (`.click`)
- User clicks `UsersDataGrid` → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=UserApprovalLevels / BusinessUnitId / Id

#### BusinessUnitDropDown.Change  [from script, surface: app]
- Trigger: **user-initiated**  (`.change`)
- User changes `BusinessUnitDropDown` → runs the flow below
- Sequence: ExecuteConnector → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=BusinessUnitDepartmentGetListById
  - SetValue: Target=Options
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=[]
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=true
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=DismissPopup

#### EditSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: Decision → IfPath → SetValue → DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → SetValue
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `SelectedOptions != 0` →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=True
      - DisplayMessageBox: Message=EmailTextBox
    - ELSE →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=False

#### AddSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: Decision → IfPath → SetValue → DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → SetValue
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `SelectedOptions != 0` →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=True
      - DisplayMessageBox: Message=EmailTextBox
    - ELSE →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=False

#### CancelViewApprovedLevelsButton.Click  [from script, surface: Users]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshUsers
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### AddCostCentreButton.Click  [from script, surface: CostCentres]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AddCostCentreButton` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → CallScript → SetValue
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox
  - SetValue: Target=DescriptionTextBox
  - CallScript: ScriptToCall=LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions
  - SetValue: Target=BusinessUnitDropDown
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### CostCentreDataGrid.Edit.Click  [from script, surface: CostCentres]
- Trigger: **user-initiated**  (`.click`)
- User clicks `CostCentreDataGrid` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → CallScript → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=CostCentreGetById
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox; Value=Name
  - SetValue: Target=DescriptionTextBox; Value=Description
  - CallScript: ScriptToCall=LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions
  - SetValue: Target=BusinessUnitDropDown; Value=BusinessUnitId
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### CostCentreDataGrid.Delete.Click  [from script, surface: CostCentres]
- Trigger: **user-initiated**  (`.click`)
- User clicks `CostCentreDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=Name
  - ExecuteConnector: ConnectorFunction=CostCentreDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshCostCentre

#### BusinessUnitDropDown.Change  [from script, surface: app]
- Trigger: **user-initiated**  (`.change`)
- User changes `BusinessUnitDropDown` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=BusinessUnitDepartmentGetListById
  - SetValue: Target=Options
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=[]
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=true
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=DismissPopup

#### EditSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: Decision → IfPath → SetValue → DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → SetValue
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `SelectedOptions != 0` →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=True
      - DisplayMessageBox: Message=NameTextBox
    - ELSE →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=False

#### AddSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: Decision → IfPath → SetValue → DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → SetValue
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `SelectedOptions != 0` →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=True
      - DisplayMessageBox: Message=NameTextBox
    - ELSE →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=False

#### AddBusinessUnitButton.Click  [from script, surface: BusinessUnits]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AddBusinessUnitButton` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → CallScript → SetValue
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox
  - SetValue: Target=DescriptionTextBox
  - SetValue: Target=CodeTextBox
  - CallScript: ScriptToCall=LoadDepartmentCheckboxListOptions
  - SetValue: Target=DepartmentsCheckBoxList; Value=[]
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### BusinessUnitDataGrid.Edit.Click  [from script, surface: BusinessUnits]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BusinessUnitDataGrid` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → CallScript → SetValue
  - ExecuteConnector: ConnectorFunction=BusinessUnitGetById
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox; Value=Name
  - SetValue: Target=DescriptionTextBox; Value=Description
  - SetValue: Target=CodeTextBox; Value=Code
  - CallScript: ScriptToCall=LoadDepartmentCheckboxListOptions
  - SetValue: Target=DepartmentsCheckBoxList
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### BusinessUnitDataGrid.Delete.Click  [from script, surface: BusinessUnits]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BusinessUnitDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=Name
  - ExecuteConnector: ConnectorFunction=BusinessUnitDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBusinessUnits

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=DismissPopup

#### EditSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=NameTextBox
  - ExecuteConnector: ConnectorFunction=BusinessUnitUpdate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBusinessUnits

#### AddSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=NameTextBox
  - ExecuteConnector: ConnectorFunction=BusinessUnitCreate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBusinessUnits

#### AddBeneficiaryButton.Click  [from script, surface: Beneficiaries]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AddBeneficiaryButton` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → CallScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - JavaScript  `[library JS: popups]`
  - CallScript: ScriptToCall=LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions
  - SetValue: Target=BankDropDown
  - SetValue: Target=AccountTypeDropDown
  - SetValue: Target=BusinessUnitDropDown
  - SetValue: Target=NameTextBox
  - SetValue: Target=AccountNameTextBox
  - SetValue: Target=AccountNumberTextBox
  - SetValue: Target=IbanTextBox
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### BeneficiaryDataGrid.Edit.Click  [from script, surface: Beneficiaries]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BeneficiaryDataGrid` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → CallScript → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=BeneficiaryGetById
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox; Value=Name
  - SetValue: Target=AccountNameTextBox; Value=AccountName
  - SetValue: Target=AccountNumberTextBox; Value=AccountNumber
  - SetValue: Target=IbanTextBox; Value=Iban
  - CallScript: ScriptToCall=LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions
  - SetValue: Target=BankDropDown; Value=BankId
  - SetValue: Target=AccountTypeDropDown; Value=BankAccountTypeId
  - SetValue: Target=BusinessUnitDropDown; Value=BusinessUnitId
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### BeneficiaryDataGrid.Delete.Click  [from script, surface: Beneficiaries]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BeneficiaryDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=Name
  - ExecuteConnector: ConnectorFunction=BeneficiaryDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBeneficiary

#### BusinessUnitDropDown.Change  [from script, surface: app]
- Trigger: **user-initiated**  (`.change`)
- User changes `BusinessUnitDropDown` → runs the flow below
- Sequence: ExecuteConnector → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=BusinessUnitDepartmentGetListById
  - SetValue: Target=Options
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=[]
  - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=true
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=DismissPopup

#### EditSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: Decision → IfPath → SetValue → DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → SetValue
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `SelectedOptions != 0` →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=True
      - DisplayMessageBox: Message=NameTextBox
    - ELSE →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=False

#### AddSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: Decision → IfPath → SetValue → DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → SetValue
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `SelectedOptions != 0` →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=True
      - DisplayMessageBox: Message=NameTextBox
    - ELSE →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=False

#### AddBankButton.Click  [from script, surface: Banks]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AddBankButton` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox
  - SetValue: Target=UniversalBranchCodeTextBox
  - SetValue: Target=UniversalSwiftCodeTextBox
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### BankDataGrid.Edit.Click  [from script, surface: Banks]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BankDataGrid` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=BankGetById
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox; Value=Name
  - SetValue: Target=UniversalBranchCodeTextBox; Value=UniversalBranchCode
  - SetValue: Target=UniversalSwiftCodeTextBox; Value=UniversalSwiftCode
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### BankDataGrid.Delete.Click  [from script, surface: Banks]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BankDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=Name
  - ExecuteConnector: ConnectorFunction=BankDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBank

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=DismissPopup

#### EditSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=NameTextBox
  - ExecuteConnector: ConnectorFunction=BankUpdate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBank

#### AddSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=NameTextBox
  - ExecuteConnector: ConnectorFunction=BankCreate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBank

#### AddBankAccountButton.Click  [from script, surface: BankAccounts]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AddBankAccountButton` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=AccountNameTextBox
  - SetValue: Target=AccountNumberTextBox
  - SetValue: Target=IbanTextBox
  - ExecuteConnector: ConnectorFunction=BankAccountTypeGetList
  - SetValue: Target=Options
  - ExecuteConnector: ConnectorFunction=BankGetList
  - SetValue: Target=Options
  - ExecuteConnector: ConnectorFunction=BusinessUnitGetList
  - SetValue: Target=Options
  - SetValue: Target=AccountTypeDropDown
  - SetValue: Target=BankDropDown
  - SetValue: Target=BusinessUnitDropDown
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### BankAccountDataGrid.Edit.Click  [from script, surface: BankAccounts]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BankAccountDataGrid` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=BankAccountGetById
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=AccountNameTextBox; Value=AccountName
  - SetValue: Target=AccountNumberTextBox; Value=AccountNumber
  - SetValue: Target=IbanTextBox; Value=Iban
  - ExecuteConnector: ConnectorFunction=BankAccountTypeGetList
  - SetValue: Target=Options
  - ExecuteConnector: ConnectorFunction=BankGetList
  - SetValue: Target=Options
  - ExecuteConnector: ConnectorFunction=BusinessUnitGetList
  - SetValue: Target=Options
  - SetValue: Target=AccountTypeDropDown; Value=BankAccountTypeId
  - SetValue: Target=BankDropDown; Value=BankId
  - SetValue: Target=BusinessUnitDropDown; Value=BusinessUnitId
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### BankAccountDataGrid.Delete.Click  [from script, surface: BankAccounts]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BankAccountDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=AccountName
  - ExecuteConnector: ConnectorFunction=BankAccountDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBankAccounts

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript → CallScript
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBankAccounts

#### EditSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=AccountNameTextBox
  - ExecuteConnector: ConnectorFunction=BankAccountUpdate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBankAccounts

#### AddSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=AccountNameTextBox
  - ExecuteConnector: ConnectorFunction=BankAccountCreate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBankAccounts

#### AddBankPaymentSetupButton.Click  [from script, surface: BankPaymentSetup]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AddBankPaymentSetupButton` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → SetValue → SetValue
  - JavaScript  `[library JS: popups]`
  - ExecuteConnector: ConnectorFunction=BankGetList
  - SetValue: Target=Options
  - SetValue: Target=BankDropDown
  - ExecuteConnector: ConnectorFunction=BankPaymentMethodGetList
  - SetValue: Target=Options
  - SetValue: Target=BankPaymentMethodDropDown
  - ExecuteConnector: ConnectorFunction=LookupDataGetList
  - SetValue: Target=Options
  - SetValue: Target=TransferMethodDropDown
  - ExecuteConnector: ConnectorFunction=LookupDataGetList
  - SetValue: Target=Options
  - SetValue: Target=ServiceLevelCodeDropDown
  - ExecuteConnector: ConnectorFunction=LookupDataGetList
  - SetValue: Target=Options
  - SetValue: Target=ChargeBearerDropDown
  - SetValue: Target=CutOffTimeTextBox
  - SetValue: Target=ApiEnabledCheckBox
  - _(+4 UI-state SetValue(s) folded into the state-signals section)_

#### BankPaymentSetupDataGrid.Edit.Click  [from script, surface: BankPaymentSetup]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BankPaymentSetupDataGrid` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → JavaScript → SetValue → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=BankPaymentSetupGetById
  - JavaScript  `[library JS: popups]`
  - ExecuteConnector: ConnectorFunction=BankGetList
  - SetValue: Target=Options
  - SetValue: Target=BankDropDown; Value=BankId
  - ExecuteConnector: ConnectorFunction=BankPaymentMethodGetList
  - SetValue: Target=Options
  - SetValue: Target=BankPaymentMethodDropDown; Value=BankPaymentMethodId
  - ExecuteConnector: ConnectorFunction=LookupDataGetList
  - SetValue: Target=Options
  - SetValue: Target=TransferMethodDropDown; Value=TransferMethodId
  - ExecuteConnector: ConnectorFunction=LookupDataGetList
  - SetValue: Target=Options
  - SetValue: Target=ServiceLevelCodeDropDown; Value=ServiceLevelCodeId
  - ExecuteConnector: ConnectorFunction=LookupDataGetList
  - SetValue: Target=Options
  - SetValue: Target=ChargeBearerDropDown; Value=ChargeBearerId
  - SetValue: Target=CutOffTimeTextBox; Value=CutOffTime
  - SetValue: Target=ApiEnabledCheckBox; Value=ApiEnabled
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### BankPaymentSetupDataGrid.Delete.Click  [from script, surface: BankPaymentSetup]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BankPaymentSetupDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=text / text
  - ExecuteConnector: ConnectorFunction=BankPaymentSetupDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBankPaymentSetup

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript → CallScript
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBankPaymentSetup

#### EditSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=text / text
  - ExecuteConnector: ConnectorFunction=BankPaymentSetupUpdate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBankPaymentSetup

#### AddSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - DisplayMessageBox: Message=text / text
  - ExecuteConnector: ConnectorFunction=BankPaymentSetupCreate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshBankPaymentSetup

#### AddDepartmentButton.Click  [from script, surface: Department]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AddDepartmentButton` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox
  - SetValue: Target=DescriptionTextBox
  - _(+4 UI-state SetValue(s) folded into the state-signals section)_

#### DepartmentDataGrid.Edit.Click  [from script, surface: Department]
- Trigger: **user-initiated**  (`.click`)
- User clicks `DepartmentDataGrid` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=DepartmentGetById
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox; Value=Name
  - SetValue: Target=DescriptionTextBox; Value=Description
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### DepartmentDataGrid.Delete.Click  [from script, surface: Department]
- Trigger: **user-initiated**  (`.click`)
- User clicks `DepartmentDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=Name
  - ExecuteConnector: ConnectorFunction=DepartmentDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshDepartmentSetup

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript → CallScript
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshDepartmentSetup

#### EditSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=NameTextBox
  - ExecuteConnector: ConnectorFunction=DepartmentUpdate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshDepartmentSetup

#### AddSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=NameTextBox
  - ExecuteConnector: ConnectorFunction=DepartmentCreate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshDepartmentSetup

#### AddPaymentReasonButton.Click  [from script, surface: PaymentReason]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AddPaymentReasonButton` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox
  - SetValue: Target=DescriptionTextBox
  - SetValue: Target=CodeTextBox
  - _(+4 UI-state SetValue(s) folded into the state-signals section)_

#### PaymentReasonDataGrid.Edit.Click  [from script, surface: PaymentReason]
- Trigger: **user-initiated**  (`.click`)
- User clicks `PaymentReasonDataGrid` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=PaymentReasonGetById
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NameTextBox; Value=Name
  - SetValue: Target=DescriptionTextBox; Value=Description
  - SetValue: Target=CodeTextBox; Value=Code
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### PaymentReasonDataGrid.Delete.Click  [from script, surface: PaymentReason]
- Trigger: **user-initiated**  (`.click`)
- User clicks `PaymentReasonDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=Name
  - ExecuteConnector: ConnectorFunction=PaymentReasonDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshPaymentReason

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript → CallScript
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshPaymentReason

#### EditSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=NameTextBox
  - ExecuteConnector: ConnectorFunction=PaymentReasonUpdate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshPaymentReason

#### AddSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=NameTextBox
  - ExecuteConnector: ConnectorFunction=PaymentReasonCreate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshPaymentReason

#### ApplyFilterButton.Click  [from script, surface: PaymentEnquiries]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Apply Filters" → runs the flow below
- Sequence: List → CallScript → SetValue → SetValue
  - List: Value=DataLabel
  - CallScript: ScriptToCall=ApplyFilters
  - SetValue: Target=Data; Value=Data
  - SetValue: Target=PaymentEnquiryDataGrid; Value=True

#### ClearFilterButton.Click  [from script, surface: PaymentEnquiries]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Clear Filters" → runs the flow below
- Sequence: CallScript → Variable → List → SetValue → SetValue
  - CallScript: ScriptToCall=ClearFilters
  - Variable: Value=DataLabel
  - List: Value=TemporaryDataStorageVariable
  - SetValue: Target=Data; Value=FilterList
  - SetValue: Target=PaymentEnquiryDataGrid; Value=False

#### PaymentEnquiryDataGrid.PaymentDetail.Click  [from script, surface: PaymentEnquiries]
- Trigger: **user-initiated**  (`.click`)
- User clicks `PaymentEnquiryDataGrid` → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=PaymentDetails / TrackingNumber

#### BackToPaymentEnquiryPageLink.Click  [from script, surface: PaymentDetails]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BackToPaymentEnquiryPageLink` → runs the flow below
- Sequence: Decision → IfPath → NavigateToPage → Decision → IfPath → NavigateToPage
- Flow (branch-structured):
  - **Decision**
    - IF `Page == Payment enquiries` →
      - NavigateToPage: Destination=PaymentEnquiries
  - **Decision**
    - IF `Page == Draft Transactions` →
      - NavigateToPage: Destination=DraftManualPaymentCapture

#### SupportingDocumentsDataGrid.Download.Click  [from script, surface: PaymentDetails]
- Trigger: **user-initiated**  (`.click`)
- User clicks `SupportingDocumentsDataGrid` → runs the flow below
- Sequence: ExecuteConnector → DownloadFile
  - ExecuteConnector: ConnectorFunction=ReadFile

#### AddPaymentSetupButton.Click  [from script, surface: PaymentSetup]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AddPaymentSetupButton` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - JavaScript  `[library JS: popups]`
  - ExecuteConnector: ConnectorFunction=BusinessUnitGetList
  - SetValue: Target=Options
  - ExecuteConnector: ConnectorFunction=TransactionTypeGetList
  - SetValue: Target=Options
  - ExecuteConnector: ConnectorFunction=BankPaymentMethodGetList
  - SetValue: Target=Options
  - ExecuteConnector: ConnectorFunction=PaymentReasonGetList
  - SetValue: Target=Options
  - ExecuteConnector: ConnectorFunction=BankAccountGetList
  - SetValue: Target=Options
  - SetValue: Target=TransactionTypeDropDown
  - SetValue: Target=PaymentMethodDropDown
  - SetValue: Target=PaymentReasonDropDown
  - SetValue: Target=BankAccountDropDown
  - SetValue: Target=BusinessUnitDropDown
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### PaymentSetupDataGrid.Edit.Click  [from script, surface: PaymentSetup]
- Trigger: **user-initiated**  (`.click`)
- User clicks `PaymentSetupDataGrid` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → ExecuteConnector → SetValue → SetValue → Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=PaymentSetupGetById
  - JavaScript  `[library JS: popups]`
  - ExecuteConnector: ConnectorFunction=BusinessUnitGetList
  - SetValue: Target=Options
  - SetValue: Target=BusinessUnitDropDown; Value=BusinessUnitId
  - ExecuteConnector: ConnectorFunction=TransactionTypeGetList
  - SetValue: Target=Options
  - SetValue: Target=TransactionTypeDropDown; Value=TransactionTypeId
  - ExecuteConnector: ConnectorFunction=BankPaymentMethodGetList
  - SetValue: Target=Options
  - SetValue: Target=PaymentMethodDropDown; Value=BankPaymentMethodId
  - ExecuteConnector: ConnectorFunction=PaymentReasonGetList
  - SetValue: Target=Options
  - SetValue: Target=PaymentReasonDropDown; Value=PaymentReasonId
  - ExecuteConnector: ConnectorFunction=BankAccountGetList
  - SetValue: Target=Options
  - SetValue: Target=BankAccountDropDown; Value=BankAccountId
  - ExecuteConnector: ConnectorFunction=BusinessUnitDepartmentGetListById
  - SetValue: Target=Options
  - SetValue: Target=DepartmentDropDown; Value=BusinessUnitDepartmentId
  - SetValue: Target=DepartmentDropDown; Value=True
  - _(+6 UI-state SetValue(s) folded into the state-signals section)_

#### PaymentSetupDataGrid.Delete.Click  [from script, surface: PaymentSetup]
- Trigger: **user-initiated**  (`.click`)
- User clicks `PaymentSetupDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=text / text / text / text
  - ExecuteConnector: ConnectorFunction=PaymentSetupDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshPaymentSetup

#### BusinessUnitDropDown.Change  [from script, surface: app]
- Trigger: **user-initiated**  (`.change`)
- User changes `BusinessUnitDropDown` → runs the flow below
- Sequence: SetValue → SetValue → Async → ExecuteConnector → SetValue → SetValue
  - SetValue: Target=DepartmentDropDown; Value=True
  - ExecuteConnector: ConnectorFunction=BusinessUnitDepartmentGetListById
  - SetValue: Target=Options
  - SetValue: Target=DepartmentDropDown
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript → CallScript
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshPaymentSetup

#### EditSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=text / text / text / text
  - ExecuteConnector: ConnectorFunction=PaymentSetupUpdate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshPaymentSetup

#### AddSaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=text / text / text / text
  - ExecuteConnector: ConnectorFunction=PaymentSetupCreate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshPaymentSetup

#### DraftTransactionsDataGrid.Detail.Click  [from script, surface: DraftManualPaymentCapture]
- Trigger: **user-initiated**  (`.click`)
- User clicks `DraftTransactionsDataGrid` → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=PaymentDetails / TrackingNumber

#### DraftTransactionsDataGrid.Edit.Click  [from script, surface: DraftManualPaymentCapture]
- Trigger: **user-initiated**  (`.click`)
- User clicks `DraftTransactionsDataGrid` → runs the flow below
- Sequence: Decision → IfPath → NavigateToPage → Decision → IfPath → NavigateToPage → Decision → IfPath → NavigateToPage → Decision → IfPath → NavigateToPage → Decision → IfPath → NavigateToPage
- Flow (branch-structured):
  - **Decision**
    - IF `TransactionManualCaptureStepId == 0` →
      - NavigateToPage: Destination=TransactionCoding / TrackingNumber
  - **Decision**
    - IF `TransactionManualCaptureStepId == 1` →
      - NavigateToPage: Destination=PaymentsDetails / TrackingNumber
  - **Decision**
    - IF `TransactionManualCaptureStepId == 2` →
      - NavigateToPage: Destination=BeneficiaryDetails / TrackingNumber
  - **Decision**
    - IF `TransactionManualCaptureStepId == 3` →
      - NavigateToPage: Destination=AttachmentsAndNotes / TrackingNumber
  - **Decision**
    - IF `TransactionManualCaptureStepId == 4` →
      - NavigateToPage: Destination=Review / TrackingNumber

#### DraftTransactionsDataGrid.Delete.Click  [from script, surface: DraftManualPaymentCapture]
- Trigger: **user-initiated**  (`.click`)
- User clicks `DraftTransactionsDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → ExecuteConnector → CallScript → Decision → IfPath → CallScript
  - DisplayMessageBox: Message='Are you sure you want to delete this draft payment transaction ?'
  - ExecuteConnector: ConnectorFunction=TransactionDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=RefreshDraftPayments

#### CancelLink.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: DisplayMessageBox → ExecuteConnector → NavigateToPage
  - DisplayMessageBox: Message='Are you sure you want to cancel the payment capture ?'
  - ExecuteConnector: ConnectorFunction=TransactionDelete
  - NavigateToPage: Destination=TransactionCoding

#### BusinessUnitDropDown.Change  [from script, surface: app]
- Trigger: **user-initiated**  (`.change`)
- User changes `BusinessUnitDropDown` → runs the flow below
- Sequence: CallScript → CallScript → CallScript
  - CallScript: ScriptToCall=PopulateDropdownsNewEntry
  - CallScript: ScriptToCall=ClearSelections
  - CallScript: ScriptToCall=ReadOnlyFields

#### BusinessUnitDepartmentDropDown.Change  [from script, surface: TransactionCoding]
- Trigger: **user-initiated**  (`.change`)
- User changes `BusinessUnitDepartmentDropDown` → runs the flow below
- Sequence: CallScript → CallScript → CallScript
  - CallScript: ScriptToCall=PopulateDropdownsNewEntry
  - CallScript: ScriptToCall=ClearSelections
  - CallScript: ScriptToCall=ReadOnlyFields

#### TransactionTypeDropDown.Change  [from script, surface: app]
- Trigger: **user-initiated**  (`.change`)
- User changes `TransactionTypeDropDown` → runs the flow below
- Sequence: CallScript → CallScript → CallScript
  - CallScript: ScriptToCall=PopulateDropdownsNewEntry
  - CallScript: ScriptToCall=ClearSelections
  - CallScript: ScriptToCall=ReadOnlyFields

#### BankAccountDropDown.Change  [from script, surface: app]
- Trigger: **user-initiated**  (`.change`)
- User changes `BankAccountDropDown` → runs the flow below
- Sequence: CallScript → CallScript → CallScript
  - CallScript: ScriptToCall=PopulateDropdownsNewEntry
  - CallScript: ScriptToCall=ClearSelections
  - CallScript: ScriptToCall=ReadOnlyFields

#### BankPaymentMethodDropDown.Change  [from script, surface: app]
- Trigger: **user-initiated**  (`.change`)
- User changes `BankPaymentMethodDropDown` → runs the flow below
- Sequence: CallScript → CallScript → CallScript
  - CallScript: ScriptToCall=PopulateDropdownsNewEntry
  - CallScript: ScriptToCall=ClearSelections
  - CallScript: ScriptToCall=ReadOnlyFields

#### SaveDraftButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save Draft" → runs the flow below
- Sequence: Decision → IfPath → Async → ExecuteConnector → Decision → IfPath → Notification → SetValue → Async → ExecuteConnector → Decision → IfPath → Notification
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `TrackingNumberValue == ''` →
      - Async
      - **Decision**
        - IF `MessageType == Success` →
          - Notification: Message=Transaction progress saved
    - ELSE →
      - Async
      - **Decision**
        - IF `MessageType == Success` →
          - Notification: Message=Transaction progress saved
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### NextButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Next" → runs the flow below
- Sequence: Decision → IfPath → Async → ExecuteConnector → CallScript → Decision → IfPath → NavigateToPage → Async → ExecuteConnector → CallScript → Decision → IfPath → NavigateToPage
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `TrackingNumberValue == ''` →
      - Async
      - CallScript: ScriptToCall=NotificationHandler
      - **Decision**
        - IF `MessageType == Success` →
          - NavigateToPage: Destination=PaymentsDetails / Id
    - ELSE →
      - Async
      - CallScript: ScriptToCall=NotificationHandler
      - **Decision**
        - IF `MessageType == Success` →
          - NavigateToPage: Destination=PaymentsDetails / Id

#### CancelLink.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: DisplayMessageBox → ExecuteConnector → NavigateToPage
  - DisplayMessageBox: Message='Are you sure you want to cancel the payment capture ?'
  - ExecuteConnector: ConnectorFunction=TransactionDelete
  - NavigateToPage: Destination=TransactionCoding

#### BackButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Back" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=TransactionCoding / TrackingNumber

#### SaveDraftButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save Draft" → runs the flow below
- Sequence: Async → ExecuteConnector → Decision → IfPath → Notification
- Flow (branch-structured):
  - Async
  - **Decision**
    - IF `MessageType == Success` →
      - Notification: Message=Transaction progress saved

#### NextButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Next" → runs the flow below
- Sequence: Async → ExecuteConnector → CallScript → Decision → IfPath → NavigateToPage
- Flow (branch-structured):
  - Async
  - CallScript: ScriptToCall=NotificationHandler
  - **Decision**
    - IF `MessageType == Success` →
      - NavigateToPage: Destination=BeneficiaryDetails / TrackingNumber

#### CancelLink.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: DisplayMessageBox → ExecuteConnector → NavigateToPage → NavigateToPage
  - DisplayMessageBox: Message='Are you sure you want to cancel the payment capture ?'
  - ExecuteConnector: ConnectorFunction=TransactionDelete
  - NavigateToPage: Destination=TransactionCoding
  - NavigateToPage: Destination=BeneficiaryDetails / TrackingNumber

#### WhitelistAndAdhocRadioButtonList.Change  [from script, surface: BeneficiaryDetails]
- Trigger: **user-initiated**  (`.change`)
- User changes `WhitelistAndAdhocRadioButtonList` → runs the flow below
- Sequence: ExecuteConnector → Decision → IfPath → CallScript → Decision → IfPath → Decision → IfPath → CallScript → CallScript
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=TransactionGetById
  - **Decision**
    - IF `value == 1` →
      - CallScript: ScriptToCall=RadioButtonChange
  - **Decision**
    - IF `value == 2` →
      - **Decision** *(has else)*
        - IF `BeneficiaryId != 0` →
          - CallScript: ScriptToCall=RadioButtonChange
        - ELSE →
          - CallScript: ScriptToCall=RadioButtonChange

#### WhitelistedBeneficiaryDataGrid.Select.Click  [from script, surface: BeneficiaryDetails]
- Trigger: **user-initiated**  (`.click`)
- User clicks `WhitelistedBeneficiaryDataGrid` → runs the flow below
- Sequence: SetValue → Notification
  - Notification: Message=Name
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### BackButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Back" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=PaymentsDetails / TrackingNumber

#### SaveDraftButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save Draft" → runs the flow below
- Sequence: Decision → IfPath → Decision → IfPath → CallScript → Notification → Decision → IfPath → CallScript
- Flow (branch-structured):
  - **Decision**
    - IF `value == 1` →
      - **Decision** *(has else)*
        - IF `SelectedDatagridRowIdLabel != 0` →
          - CallScript: ScriptToCall=TransactionUpdate
        - ELSE →
          - Notification: Message='Please select a whitelisted beneficiary or unselect the whitelisted beneficiary button'
  - **Decision**
    - IF `value == 2` →
      - CallScript: ScriptToCall=TransactionUpdate

#### NextButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Next" → runs the flow below
- Sequence: Decision → IfPath → Decision → IfPath → CallScript → NavigateToPage → Notification → Decision → IfPath → CallScript → NavigateToPage
- Flow (branch-structured):
  - **Decision**
    - IF `value == 1` →
      - **Decision** *(has else)*
        - IF `SelectedDatagridRowIdLabel != 0` →
          - CallScript: ScriptToCall=TransactionUpdate
          - NavigateToPage: Destination=AttachmentsAndNotes / TrackingNumber
        - ELSE →
          - Notification: Message=Please select a whitelisted beneficiary or unselect the whitelisted beneficiary button
  - **Decision**
    - IF `value == 2` →
      - CallScript: ScriptToCall=TransactionUpdate
      - NavigateToPage: Destination=AttachmentsAndNotes / TrackingNumber

#### CancelLink.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: DisplayMessageBox → ExecuteConnector → NavigateToPage → NavigateToPage
  - DisplayMessageBox: Message='Are you sure you want to cancel the payment capture ?'
  - ExecuteConnector: ConnectorFunction=TransactionDelete
  - NavigateToPage: Destination=TransactionCoding
  - NavigateToPage: Destination=AttachmentsAndNotes / TrackingNumber

#### AttachmentsDataGrid.Delete.Click  [from script, surface: AttachmentsAndNotes]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AttachmentsDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → ExecuteConnector → CallScript → CallScript
  - DisplayMessageBox: Message=FileName
  - ExecuteConnector: ConnectorFunction=TransactionSupportingDocumentDelete
  - ExecuteConnector: ConnectorFunction=DeleteFile
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=RefreshAttachementGrid

#### AddNoteButton.Click  [from script, surface: AttachmentsAndNotes]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add Note" → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NoteTextBox
  - _(+4 UI-state SetValue(s) folded into the state-signals section)_

#### NoteDataGrid.Edit.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks `NoteDataGrid` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=NoteTextBox; Value=Note
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### NoteDataGrid.Delete.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks `NoteDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=NoteTextBox
  - ExecuteConnector: ConnectorFunction=TransactionNoteDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshNoteGrid

#### NoteCancelButton.Click  [from script, surface: AttachmentsAndNotes]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript → CallScript
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshNoteGrid

#### NoteEditSaveButton.Click  [from script, surface: AttachmentsAndNotes]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=NoteTextBox
  - ExecuteConnector: ConnectorFunction=TransactionNoteUpdate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshNoteGrid

#### NoteAddSaveButton.Click  [from script, surface: AttachmentsAndNotes]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → CallScript
  - DisplayMessageBox: Message=NoteTextBox
  - ExecuteConnector: ConnectorFunction=TransactionNoteCreate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshNoteGrid

#### ProceedButton.Click  [from script, surface: AttachmentsAndNotes]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Proceed" → runs the flow below
- Sequence: SetValue → JavaScript → NavigateToPage
  - JavaScript  `[library JS: popups]`
  - NavigateToPage: Destination=AttachmentsAndNotes / TrackingNumber
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### CancelDuplicateTransactionButton.Click  [from script, surface: AttachmentsAndNotes]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: SetValue → JavaScript → DisplayMessageBox → ExecuteConnector → NavigateToPage → NavigateToPage
  - JavaScript  `[library JS: popups]`
  - DisplayMessageBox: Message='Are you sure you want to cancel the payment capture ?'
  - ExecuteConnector: ConnectorFunction=TransactionDelete
  - NavigateToPage: Destination=TransactionCoding
  - NavigateToPage: Destination=AttachmentsAndNotes / TrackingNumber
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### BackButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Back" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=BeneficiaryDetails / TrackingNumber

#### SaveDraftButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save Draft" → runs the flow below
- Sequence: Async → ExecuteConnector → Decision → IfPath → Notification
- Flow (branch-structured):
  - Async
  - **Decision**
    - IF `MessageType == Success` →
      - Notification: Message=Transaction progress saved

#### NextButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Next" → runs the flow below
- Sequence: Async → ExecuteConnector → NavigateToPage
  - ExecuteConnector: ConnectorFunction=TransactionUpdate
  - NavigateToPage: Destination=Review / TrackingNumber

#### BackButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Back" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=AttachmentsAndNotes / TrackingNumber

#### SaveDraftButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save Draft" → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=TransactionUpdate

#### SubmitButton.Click  [from script, surface: Review]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Submit" → runs the flow below
- Sequence: CallScript → NavigateToPage
  - CallScript: ScriptToCall=TransactionUpdate
  - NavigateToPage: Destination=TransactionCoding

#### AddApprovalLevelButton.Click  [from script, surface: ApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AddApprovalLevelButton` → runs the flow below
- Sequence: CallScript → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → CallScript → ObjectInstance → CallScript
  - CallScript: ScriptToCall=PageLoader
  - JavaScript  `[library JS: popups]`
  - SetValue: Target=BusinessUnitDropDown
  - SetValue: Target=DepartmentDropDown
  - SetValue: Target=TransactionTypeDropDown
  - CallScript: ScriptToCall=LoadDropDowns
  - CallScript: ScriptToCall=InitialiseDataList
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### ApprovalLevelDataGrid.Edit.Click  [from script, surface: ApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks `ApprovalLevelDataGrid` → runs the flow below
- Sequence: CallScript → SetValue → JavaScript → SetValue → SetValue → SetValue → SetValue → CallScript → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → ExecuteConnector → ObjectInstance → List → ForEach → CallScript → SetValue → List → CallScript
  - CallScript: ScriptToCall=PageLoader
  - JavaScript  `[library JS: popups]`
  - CallScript: ScriptToCall=LoadDropDowns
  - SetValue: Target=BusinessUnitDropDown; Value=BusinessUnitId
  - SetValue: Target=DepartmentDropDown; Value=DepartmentId
  - SetValue: Target=TransactionTypeDropDown; Value=TransactionTypeId
  - SetValue: Target=BusinessUnitDropDown; Value=True
  - SetValue: Target=DepartmentDropDown; Value=True
  - SetValue: Target=TransactionTypeDropDown; Value=True
  - SetValue: Target=DepartmentDropDown; Value=True
  - ExecuteConnector: ConnectorFunction=ApprovalLevelAmountGetList
  - List: Value=[
  {{
    "Level": 1,
    "MaxApprovalAmount": 0
  }},
  {{
    "Level": 2,
    "MaxApprovalAmount": 0
  }},
  {{
    "Level": 3,
    "MaxApprovalAmount": 0
  }},
  {{
    "Level": 4,
    "MaxApprovalAmount": 0
  }},
  {{
    "Level": 5,
    "MaxApprovalAmount": 0
  }},
  {{
 
  - ForEach: List=ApprovalLevelAmounts
  - CallScript: ScriptToCall=ScriptToUpdateAmountDatagridWithPrePopulatedValues
  - SetValue: Target=DataList; Value=DataList
  - List: Value=[{{
 "name": "Level",
 "header": "Level"
}},{{
 "name": "MaxApprovalAmount",
 "header": "Max Approval Amount (only digits)"
}}]
  - CallScript: ScriptToCall=ClientSideRepeaterDataGrid
  - _(+6 UI-state SetValue(s) folded into the state-signals section)_

#### ApprovalLevelDataGrid.Delete.Click  [from script, surface: ApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks `ApprovalLevelDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript
  - DisplayMessageBox: Message=BusinessUnit / Department / TransactionType
  - ExecuteConnector: ConnectorFunction=ApprovalLevelDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=RefreshApprovalLevels

#### ApprovalLevelDataGrid.ViewApprovalLevelAmounts.Click  [from script, surface: ApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks `ApprovalLevelDataGrid` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → CallScript
  - JavaScript  `[library JS: popups]`
  - CallScript: ScriptToCall=RefreshApprovalLevelAmountDatagrid
  - _(+2 UI-state SetValue(s) folded into the state-signals section)_

#### BusinessUnitDropDown.Change  [from script, surface: app]
- Trigger: **user-initiated**  (`.change`)
- User changes `BusinessUnitDropDown` → runs the flow below
- Sequence: Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=BusinessUnitDepartmentGetListById
  - SetValue: Target=Options
  - SetValue: Target=DepartmentDropDown
  - SetValue: Target=DepartmentDropDown; Value=true
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript → CallScript
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshApprovalLevels

#### CreateApprovalLevelButton.Click  [from script, surface: ApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Create Approval Level" → runs the flow below
- Sequence: Decision → IfPath → SetValue → SetValue → CallScript
- Flow (branch-structured):
  - **Decision** *(has else)*
    - IF `value == ""` →
      - SetValue: Target=DepartmentDropDown; Value=False
    - ELSE →
      - SetValue: Target=DepartmentDropDown; Value=True
      - CallScript: ScriptToCall=CreateAndEditApprovalLevelScript

#### EditSaveApprovalLevelButton.Click  [from script, surface: ApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks `EditSaveApprovalLevelButton` → runs the flow below
- Sequence: CallScript
  - CallScript: ScriptToCall=CreateAndEditApprovalLevelScript

#### AmountDataGrid.Delete.Click  [from script, surface: ApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks `AmountDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript
  - DisplayMessageBox: Message=Amounts
  - ExecuteConnector: ConnectorFunction=ApprovalLevelAmountDelete
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=RefreshApprovalLevelAmountDatagrid

#### CancelViewApprovedLevelAmountsButton.Click  [from script, surface: ApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshApprovalLevels
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### ParentDataGrid.MaxApprovalAmounts.Click  [from script, surface: UserApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks `ParentDataGrid` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → CallScript
  - JavaScript  `[library JS: popups]`
  - CallScript: ScriptToCall=RefreshChildDataGrid
  - _(+2 UI-state SetValue(s) folded into the state-signals section)_

#### BackToUsersPageLink.Click  [from script, surface: UserApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks `BackToUsersPageLink` → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=Users

#### ChildDataGrid.Assign.Click  [from script, surface: UserApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks `ChildDataGrid` → runs the flow below
- Sequence: ExecuteConnector → CallScript → Decision → IfPath → CallScript
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=UserApprovalLevelCreate
  - CallScript: ScriptToCall=NotificationHandler
  - **Decision**
    - IF `MessageType == Success` →
      - CallScript: ScriptToCall=RefreshChildDataGrid

#### ChildDataGrid.Unassign.Click  [from script, surface: UserApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks `ChildDataGrid` → runs the flow below
- Sequence: ExecuteConnector → CallScript → Decision → IfPath → CallScript
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=UserApprovalLevelDelete
  - CallScript: ScriptToCall=NotificationHandler
  - **Decision**
    - IF `MessageType == Success` →
      - CallScript: ScriptToCall=RefreshChildDataGrid

#### CancelChildGridPopupButton.Click  [from script, surface: UserApprovalLevels]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: SetValue
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### ApprovalLevelRulesDataGrid.ViewApprovalLevelRules.Click  [from script, surface: ApprovalLevelRules]
- Trigger: **user-initiated**  (`.click`)
- User clicks `ApprovalLevelRulesDataGrid` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → ExecuteConnector → SetValue
  - JavaScript  `[library JS: popups]`
  - ExecuteConnector: ConnectorFunction=ApprovalLevelRuleGetList
  - SetValue: Target=Data
  - _(+2 UI-state SetValue(s) folded into the state-signals section)_

#### ApprovalLevelRulesDataGrid.EditApprovalLevelRules.Click  [from script, surface: ApprovalLevelRules]
- Trigger: **user-initiated**  (`.click`)
- User clicks `ApprovalLevelRulesDataGrid` → runs the flow below
- Sequence: SetValue → JavaScript → SetValue → ObjectInstance → List → ExecuteConnector → CallScript
  - JavaScript  `[library JS: popups]`
  - List: Value=[{{
 "name": "ApprovalLevelId",
 "header": "ApprovalLevelId",
 "visible": false,
 "sortable": false
}},{{
 "name": "ApprovalAmount",
 "header": "Approval Amount",
 "sortable": false
}},{{
 "name": "ManagerialApproval",
 "header": "Managerial Approval",
 "sortable": false
}},{{
 "name":
  - ExecuteConnector: ConnectorFunction=ApprovalLevelRuleGetList
  - CallScript: ScriptToCall=ClientSideRepeaterDataGrid
  - _(+2 UI-state SetValue(s) folded into the state-signals section)_

#### EditCancelButton.Click  [from script, surface: ApprovalLevelRules]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: CallScript → CallScript
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshApprovalLevelRules

#### EditSaveApprovalLevelRulesButton.Click  [from script, surface: ApprovalLevelRules]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: Variable → CallScript → ForEach → ExecuteConnector → Decision → IfPath → SetValue → Decision → IfPath → Notification → CallScript → Notification
- Flow (branch-structured):
  - Variable: Value=1
  - CallScript: ScriptToCall=ClientSideRepeaterDataGridGetData
  - ForEach: List=Data
  - **Decision** *(has else)*
    - IF `SuccessVariable == 1` →
      - Notification: Message='Approval Level rules have been successfully updated'
      - CallScript: ScriptToCall=DismissPopup
    - ELSE →
      - Notification: Message='Approval Level rules update has been unsuccessful'

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: SetValue
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

### Automatic — on page / template open

#### Roles.Load  [from script, surface: Roles]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=RoleGetList
  - SetValue: Target=Data

#### Users.Load  [from script, surface: Users]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshUsers

#### CostCentres.Load  [from script, surface: CostCentres]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshCostCentre

#### BusinessUnits.Load  [from script, surface: BusinessUnits]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshBusinessUnits

#### Beneficiaries.Load  [from script, surface: Beneficiaries]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshBeneficiary

#### Banks.Load  [from script, surface: Banks]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshBank

#### BankAccounts.Load  [from script, surface: BankAccounts]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshBankAccounts

#### BankPaymentSetup.Load  [from script, surface: BankPaymentSetup]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshBankPaymentSetup

#### Department.Load  [from script, surface: Department]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshDepartmentSetup

#### PaymentReason.Load  [from script, surface: PaymentReason]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshPaymentReason

#### PaymentEnquiries.Load  [from script, surface: PaymentEnquiries]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: SetValue → Async → ExecuteConnector → ExecuteConnector → ExecuteConnector → SetValue → List → CallScript
  - SetValue: Target=PaymentEnquiryDataGrid; Value=False
  - ExecuteConnector: ConnectorFunction=TransactionGetList
  - ExecuteConnector: ConnectorFunction=TransactionTypeGetList
  - ExecuteConnector: ConnectorFunction=BusinessUnitGetList
  - List: Value=Transactions / TransactionTypes / BusinessUnits
  - CallScript: ScriptToCall=GenerateFilters
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### PaymentDetails.Load  [from script, surface: PaymentDetails]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript → Async → ExecuteConnector → ExecuteConnector → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - CallScript: ScriptToCall=Tabs
  - ExecuteConnector: ConnectorFunction=TransactionGetById
  - ExecuteConnector: ConnectorFunction=TransactionNoteGetList
  - ExecuteConnector: ConnectorFunction=TransactionSupportingDocumentGetList
  - SetValue: Target=Data
  - SetValue: Target=Data
  - _(+9 UI-state SetValue(s) folded into the state-signals section)_

#### PaymentSetup.Load  [from script, surface: PaymentSetup]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshPaymentSetup

#### DraftManualPaymentCapture.Load  [from script, surface: DraftManualPaymentCapture]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshDraftPayments

#### TransactionCoding.Load  [from script, surface: TransactionCoding]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: SetValue → List → CallScript → Decision → IfPath → CallScript → CallScript → CallScript → CallScript → CallScript
- Flow (branch-structured):
  - List
  - CallScript: ScriptToCall=WorkflowSteps
  - **Decision** *(has else)*
    - IF `TrackingNumberValue == ''` →
      - CallScript: ScriptToCall=PopulateDropdownsNewEntry
      - CallScript: ScriptToCall=ReadOnlyFields
    - ELSE →
      - CallScript: ScriptToCall=PopulateDropdownsExistingEntry
      - CallScript: ScriptToCall=SelectDropdowns
      - CallScript: ScriptToCall=ReadOnlyFields
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### PaymentsDetails.Load  [from script, surface: PaymentsDetails]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: List → CallScript → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → Decision → IfPath → SetValue → Decision → IfPath → SetValue → Decision → IfPath → SetValue → Decision → IfPath → SetValue
- Flow (branch-structured):
  - List
  - CallScript: ScriptToCall=WorkflowSteps
  - Async
  - SetValue: Target=Options
  - Async
  - **Decision**
    - IF `Amount != 0` →
      - SetValue: Target=AmountTextBox; Value=Amount
  - **Decision**
    - IF `CurrencyId != 0` →
      - SetValue: Target=CurrencyTypeDropDown; Value=CurrencyId
  - **Decision**
    - IF `ExecutionDate != ?` →
      - SetValue: Target=ExecutionDatePicker; Value=ExecutionDate
  - **Decision**
    - IF `PaymentReference != ?` →
      - SetValue: Target=PaymentReferenceTextBox; Value=PaymentReference

#### BeneficiaryDetails.Load  [from script, surface: BeneficiaryDetails]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: List → CallScript → CallScript → CallScript
  - CallScript: ScriptToCall=WorkflowSteps
  - CallScript: ScriptToCall=ToggleButton
  - CallScript: ScriptToCall=LoadScript

#### AttachmentsAndNotes.Load  [from script, surface: AttachmentsAndNotes]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: List → CallScript → CallScript → CallScript → ExecuteConnector → Decision → IfPath → SetValue → JavaScript → SetValue → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
- Flow (branch-structured):
  - List
  - CallScript: ScriptToCall=WorkflowSteps
  - CallScript: ScriptToCall=RefreshAttachementGrid
  - CallScript: ScriptToCall=RefreshNoteGrid
  - ExecuteConnector: ConnectorFunction=DuplicateTransactionGetList
  - **Decision** *(has else)*
    - IF `Transactions != 0` →
      - JavaScript  `[library JS: popups]`
      - SetValue: Target=Data
      - ExecuteConnector: ConnectorFunction=TransactionGetById
    - ELSE →
  - _(+13 UI-state SetValue(s) folded into the state-signals section)_

#### Review.Load  [from script, surface: Review]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: List → CallScript → ExecuteConnector → Decision → IfPath → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue → ExecuteConnector → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
- Flow (branch-structured):
  - List
  - CallScript: ScriptToCall=WorkflowSteps
  - ExecuteConnector: ConnectorFunction=TransactionGetById
  - **Decision** *(has else)*
    - IF `BeneficiaryId != 0` →
      - ExecuteConnector: ConnectorFunction=BeneficiaryGetById
    - ELSE →
  - ExecuteConnector: ConnectorFunction=TransactionSupportingDocumentGetList
  - ExecuteConnector: ConnectorFunction=TransactionNoteGetList
  - SetValue: Target=Data
  - SetValue: Target=Data
  - _(+15 UI-state SetValue(s) folded into the state-signals section)_

#### ApprovalLevels.Load  [from script, surface: ApprovalLevels]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshApprovalLevels

#### UserApprovalLevels.Load  [from script, surface: UserApprovalLevels]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=UserApprovalLevelGetListByBusinessUnitIdUserId
  - SetValue: Target=Data

#### ApprovalLevelRules.Load  [from script, surface: ApprovalLevelRules]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=RefreshApprovalLevelRules

#### DefaultTemplate.Load  [from script, surface: app]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=FixHeaders

### Other — helper scripts / timers / lifecycle

#### RefreshUsers  [from script, surface: Users]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue → List → CallScript
  - ExecuteConnector: ConnectorFunction=UserGetList
  - SetValue: Target=Data
  - CallScript: ScriptToCall=ConditionalColumnsStyling

#### DismissPopup  [from script, surface: Users]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshUsers
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### LoadDropdownsAndCheckboxlists  [from script, surface: Users]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → Decision → IfPath → Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue
- Flow (branch-structured):
  - Async
  - SetValue: Target=Options
  - Async
  - SetValue: Target=Options
  - **Decision** *(has else)*
    - IF `BusinessUnitId != ?` →
      - Async
      - SetValue: Target=Options
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=true
    - ELSE →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=false
  - _(+2 UI-state SetValue(s) folded into the state-signals section)_

#### RefreshCostCentre  [from script, surface: CostCentres]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=CostCentreGetList
  - SetValue: Target=Data

#### DismissPopup  [from script, surface: CostCentres]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshCostCentre
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions  [from script, surface: CostCentres]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue → Decision → IfPath → Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue
- Flow (branch-structured):
  - Async
  - SetValue: Target=Options
  - **Decision** *(has else)*
    - IF `BusinessUnitId != ?` →
      - Async
      - SetValue: Target=Options
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=true
    - ELSE →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=false
  - _(+2 UI-state SetValue(s) folded into the state-signals section)_

#### RefreshBusinessUnits  [from script, surface: BusinessUnits]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=BusinessUnitGetList
  - SetValue: Target=Data

#### DismissPopup  [from script, surface: BusinessUnits]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshBusinessUnits
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### LoadDepartmentCheckboxListOptions  [from script, surface: BusinessUnits]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=DepartmentGetList
  - SetValue: Target=Options

#### RefreshBeneficiary  [from script, surface: Beneficiaries]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=BeneficiaryGetList
  - SetValue: Target=Data

#### DismissPopup  [from script, surface: Beneficiaries]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshBeneficiary
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### LoadBusinessUnitDropDownOptionsBusinessUnitDepartmentOptions  [from script, surface: Beneficiaries]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue → Decision → IfPath → Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue
- Flow (branch-structured):
  - Async
  - SetValue: Target=Options
  - **Decision** *(has else)*
    - IF `BusinessUnitId != ?` →
      - Async
      - SetValue: Target=Options
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=true
    - ELSE →
      - SetValue: Target=BusinessUnitDepartmentsCheckBoxList; Value=false
  - Async
  - SetValue: Target=Options
  - Async
  - SetValue: Target=Options
  - _(+2 UI-state SetValue(s) folded into the state-signals section)_

#### RefreshBank  [from script, surface: Banks]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=BankGetList
  - SetValue: Target=Data

#### DismissPopup  [from script, surface: Banks]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshBank
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### RefreshBankAccounts  [from script, surface: BankAccounts]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=BankAccountGetList
  - SetValue: Target=Data

#### DismissPopup  [from script, surface: BankAccounts]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshBankAccounts
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### RefreshBankPaymentSetup  [from script, surface: BankPaymentSetup]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=BankPaymentSetupGetList
  - SetValue: Target=Data

#### DismissPopup  [from script, surface: BankPaymentSetup]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshBankPaymentSetup
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### RefreshDepartmentSetup  [from script, surface: Department]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=DepartmentGetList
  - SetValue: Target=Data

#### DismissPopup  [from script, surface: Department]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshDepartmentSetup
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### RefreshPaymentReason  [from script, surface: PaymentReason]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=PaymentReasonGetList
  - SetValue: Target=Data

#### DismissPopup  [from script, surface: PaymentReason]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshPaymentReason
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### DismissPopup  [from script, surface: PaymentSetup]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshPaymentSetup
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### RefreshPaymentSetup  [from script, surface: PaymentSetup]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=PaymentSetupGetList
  - SetValue: Target=Data

#### RefreshDraftPayments  [from script, surface: DraftManualPaymentCapture]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=DraftTransactionGetList
  - SetValue: Target=Data

#### PopulateDropdownsNewEntry  [from script, surface: TransactionCoding]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → Decision → IfPath → SetValue → Decision → IfPath → SetValue → Decision → IfPath → SetValue → Decision → IfPath → SetValue → Decision → IfPath → SetValue → Decision → IfPath → SetValue
- Flow (branch-structured):
  - Async
  - **Decision**
    - IF `BusinessUnitId == ? AND TrackingNumber != ?` →
      - SetValue: Target=Options; Value=PaymentSetups
  - **Decision**
    - IF `BusinessUnitId != ? AND BusinessUnitDepartmentId == ? AND TrackingNumber != ?` →
      - SetValue: Target=Options; Value=PaymentSetups
  - **Decision**
    - IF `BusinessUnitDepartmentId != ? AND TransactionTypeId == ? AND TrackingNumber != ?` →
      - SetValue: Target=Options; Value=PaymentSetups
  - **Decision**
    - IF `TransactionTypeId != ? AND BankAccountId == ? AND TrackingNumber != ?` →
      - SetValue: Target=Options; Value=PaymentSetups
  - **Decision**
    - IF `BankAccountId != ? AND BankPaymentMethodId == ? AND TrackingNumber != ?` →
      - SetValue: Target=Options; Value=PaymentSetups
  - **Decision**
    - IF `BankPaymentMethodId != ? AND PaymentReasonId == ? AND TrackingNumber != ?` →
      - SetValue: Target=Options; Value=PaymentSetups

#### ReadOnlyFields  [from script, surface: TransactionCoding]
- Trigger: **other (helper script)**
- Sequence: SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - SetValue: Target=BusinessUnitDropDown; Value=BusinessUnit
  - SetValue: Target=BusinessUnitDepartmentDropDown; Value=BusinessUnitDepartment
  - SetValue: Target=TransactionTypeDropDown; Value=TransactionType
  - SetValue: Target=BankAccountDropDown; Value=BankAccount
  - SetValue: Target=BankPaymentMethodDropDown; Value=BankPaymentMethod
  - SetValue: Target=PaymentReasonDropDown; Value=PaymentReason

#### ClearSelections  [from script, surface: TransactionCoding]
- Trigger: **other (helper script)**
- Sequence: Decision → IfPath → SetValue → Decision → IfPath → SetValue → Decision → IfPath → SetValue → Decision → IfPath → SetValue → Decision → IfPath → SetValue → Decision → IfPath → SetValue
- Flow (branch-structured):
  - **Decision**
    - IF `ClearBusinessUnit == 1` →
      - SetValue: Target=BusinessUnitDropDown
  - **Decision**
    - IF `ClearBusinessUnitDepartment == 1` →
      - SetValue: Target=BusinessUnitDepartmentDropDown
  - **Decision**
    - IF `ClearTransactionType == 1` →
      - SetValue: Target=TransactionTypeDropDown
  - **Decision**
    - IF `ClearBankAccount == 1` →
      - SetValue: Target=BankAccountDropDown
  - **Decision**
    - IF `ClearBankPaymentMethod == 1` →
      - SetValue: Target=BankPaymentMethodDropDown
  - **Decision**
    - IF `ClearPaymentReason == 1` →
      - SetValue: Target=PaymentReasonDropDown

#### SelectDropdowns  [from script, surface: TransactionCoding]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=TransactionGetById
  - SetValue: Target=BusinessUnitDepartmentDropDown; Value=BusinessUnitDepartmentId
  - SetValue: Target=BusinessUnitDropDown; Value=BusinessUnitId
  - SetValue: Target=TransactionTypeDropDown; Value=TransactionTypeId
  - SetValue: Target=BankAccountDropDown; Value=BankAccountId
  - SetValue: Target=BankPaymentMethodDropDown; Value=BankPaymentMethodId
  - SetValue: Target=PaymentReasonDropDown; Value=PaymentReasonId

#### PopulateDropdownsExistingEntry  [from script, surface: TransactionCoding]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=TransactionGetById
  - ExecuteConnector: ConnectorFunction=PaymentSetupTransactionCodingGetList
  - SetValue: Target=Options; Value=PaymentSetups
  - ExecuteConnector: ConnectorFunction=PaymentSetupTransactionCodingGetList
  - SetValue: Target=Options; Value=PaymentSetups
  - ExecuteConnector: ConnectorFunction=PaymentSetupTransactionCodingGetList
  - SetValue: Target=Options; Value=PaymentSetups
  - ExecuteConnector: ConnectorFunction=PaymentSetupTransactionCodingGetList
  - SetValue: Target=Options; Value=PaymentSetups
  - ExecuteConnector: ConnectorFunction=PaymentSetupTransactionCodingGetList
  - SetValue: Target=Options; Value=PaymentSetups
  - ExecuteConnector: ConnectorFunction=PaymentSetupTransactionCodingGetList
  - SetValue: Target=Options; Value=PaymentSetups

#### TransactionUpdate  [from script, surface: BeneficiaryDetails]
- Trigger: **other (helper script)**
- Sequence: Decision → IfPath → Async → ExecuteConnector → ExecuteConnector → CallScript → Decision → IfPath → ExecuteConnector → CallScript
- Flow (branch-structured):
  - **Decision**
    - IF `value == 1` →
      - Async
      - ExecuteConnector: ConnectorFunction=TransactionUpdate
      - CallScript: ScriptToCall=NotificationHandler
  - **Decision**
    - IF `value == 2` →
      - ExecuteConnector: ConnectorFunction=TransactionUpdate
      - CallScript: ScriptToCall=NotificationHandler

#### LoadScript  [from script, surface: BeneficiaryDetails]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → Decision → IfPath → SetValue → CallScript → Decision → IfPath → SetValue → CallScript
- Flow (branch-structured):
  - ExecuteConnector: ConnectorFunction=TransactionGetById
  - **Decision** *(has else)*
    - IF `BeneficiaryId != 0` →
      - SetValue: Target=WhitelistAndAdhocRadioButtonList; Value=1
      - CallScript: ScriptToCall=RadioButtonChange
    - ELSE →
      - **Decision**
        - IF `BeneficiaryName != ?` →
          - SetValue: Target=WhitelistAndAdhocRadioButtonList; Value=2
          - CallScript: ScriptToCall=RadioButtonChange

#### RadioButtonChange  [from script, surface: BeneficiaryDetails]
- Trigger: **other (helper script)**
- Sequence: Decision → IfPath → SetValue → Async → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → Decision → IfPath → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
- Flow (branch-structured):
  - **Decision**
    - IF `RadioButttonSelectedValue == 1` →
      - SetValue: Target=WhitelistedBeneficiaryDataGrid; Value=True
      - Async
      - SetValue: Target=Data
  - **Decision**
    - IF `RadioButttonSelectedValue == 2` →
      - SetValue: Target=WhitelistedBeneficiaryDataGrid; Value=False
      - SetValue: Target=NameTextBox; Value=Name
      - SetValue: Target=AccountNumberTextBox; Value=AccountNumber
      - SetValue: Target=SortCodeTextBox; Value=SortCode
  - _(+5 UI-state SetValue(s) folded into the state-signals section)_

#### DismissPopup  [from script, surface: AttachmentsAndNotes]
- Trigger: **other (helper script)**
- Sequence: SetValue → CallScript
  - CallScript: ScriptToCall=RefreshNoteGrid
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### RefreshNoteGrid  [from script, surface: AttachmentsAndNotes]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=TransactionNoteGetList
  - SetValue: Target=Data

#### RefreshAttachementGrid  [from script, surface: AttachmentsAndNotes]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=TransactionSupportingDocumentGetList
  - SetValue: Target=Data

#### UploadFile.FileUploaded  [from script, surface: AttachmentsAndNotes]
- Trigger: **other (timer / lifecycle)**  (`.fileuploaded`)
- Sequence: ForEach → ExecuteConnector → Async → ExecuteConnector → CallScript → CallScript
  - ForEach: List=Files
  - ExecuteConnector: ConnectorFunction=WriteFile
  - ExecuteConnector: ConnectorFunction=TransactionSupportingDocumentCreate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=RefreshAttachementGrid

#### TransactionUpdate  [from script, surface: Review]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → ExecuteConnector → CallScript
  - ExecuteConnector: ConnectorFunction=TransactionGetById
  - ExecuteConnector: ConnectorFunction=TransactionUpdate
  - CallScript: ScriptToCall=NotificationHandler

#### DismissPopup  [from script, surface: ApprovalLevels]
- Trigger: **other (helper script)**
- Sequence: SetValue
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### RefreshApprovalLevels  [from script, surface: ApprovalLevels]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=DistinctApprovalLevelGetList
  - SetValue: Target=Data

#### InitialiseDataList  [from script, surface: ApprovalLevels]
- Trigger: **other (helper script)**
- Sequence: ObjectInstance → List → List → CallScript
  - ObjectInstance: Value=State
  - List: Value=[
  {{
    "Level": 1,
    "MaxApprovalAmount": 0
  }},
  {{
    "Level": 2,
    "MaxApprovalAmount": 0
  }},
  {{
    "Level": 3,
    "MaxApprovalAmount": 0
  }},
  {{
    "Level": 4,
    "MaxApprovalAmount": 0
  }},
  {{
    "Level": 5,
    "MaxApprovalAmount": 0
  }},
  {{
 
  - List: Value=[{{
 "name": "Level",
 "header": "Level"
}},{{
 "name": "MaxApprovalAmount",
 "header": "Max Approval Amount (only digits)"
}}]
  - CallScript: ScriptToCall=ClientSideRepeaterDataGrid

#### ScriptToUpdateAmountDatagridWithPrePopulatedValues  [from script, surface: ApprovalLevels]
- Trigger: **other (helper script)**
- Sequence: JavaScript → SetValue
  - JavaScript  `[custom JS]` — `// Inputs: // DataList = list of { Level, MaxApprovalAmount } // LoopValue = current item from API (contains MaxApproval…`
  - SetValue: Target=DataList; Value=JavaScript

#### LoadDropDowns  [from script, surface: ApprovalLevels]
- Trigger: **other (helper script)**
- Sequence: Async → ExecuteConnector → SetValue → Decision → IfPath → Async → ExecuteConnector → SetValue → Async → ExecuteConnector → SetValue
- Flow (branch-structured):
  - Async
  - SetValue: Target=Options
  - **Decision**
    - IF `BusinessUnitId != ?` →
      - Async
      - SetValue: Target=Options
  - Async
  - SetValue: Target=Options

#### CreateAndEditApprovalLevelScript  [from script, surface: ApprovalLevels]
- Trigger: **other (helper script)**
- Sequence: Variable → Variable → Variable → CallScript → List → DisplayMessageBox → ForEach → SetValue → ForEach → Decision → IfPath → SetValue → Decision → IfPath → SetValue → SetValue → Decision → IfPath → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript → Async → ExecuteConnector → CallScript → Decision → IfPath → CallScript → CallScript
  - Variable: Value=Action
  - Variable: Value=1
  - CallScript: ScriptToCall=ClientSideRepeaterDataGridGetData
  - DisplayMessageBox: Message=Action / text / text / text
  - ForEach: List=Data
  - SetValue: Target=MaxApprovalAmountList
  - ForEach: List=MaxApprovalAmountList
  - SetValue: Target=MaxApprovalAmounts; Value=Amount
  - SetValue: Target=MaxApprovalAmounts; Value=MaxApprovalAmounts / Amount
  - SetValue: Target=Count; Value=Count
  - ExecuteConnector: ConnectorFunction=ApprovalLevelCreate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshApprovalLevels
  - ExecuteConnector: ConnectorFunction=ApprovalLevelUpdate
  - CallScript: ScriptToCall=NotificationHandler
  - CallScript: ScriptToCall=DismissPopup
  - CallScript: ScriptToCall=RefreshApprovalLevels

#### RefreshApprovalLevelAmountDatagrid  [from script, surface: ApprovalLevels]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=ApprovalLevelAmountGetList
  - SetValue: Target=Data

#### RefreshChildDataGrid  [from script, surface: UserApprovalLevels]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=UserApprovalLevelAmountGetList
  - SetValue: Target=Data

#### RefreshApprovalLevelRules  [from script, surface: ApprovalLevelRules]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=DistinctApprovalLevelGetList
  - SetValue: Target=Data

#### Initialise  [from script, surface: ApprovalLevelRules]
- Trigger: **other (helper script)**
- Sequence: ObjectInstance → List
  - ObjectInstance: Value=State

#### DismissPopup  [from script, surface: ApprovalLevelRules]
- Trigger: **other (helper script)**
- Sequence: SetValue
  - _(+1 UI-state SetValue(s) folded into the state-signals section)_

#### FixHeaders  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[library JS: full-width-top-bar]`

#### GenerateFilters  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[library JS: filter-grid]`

#### ApplyFilters  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript → SetValue
  - JavaScript  `[library JS: filter-grid]`
  - SetValue: Target=Data; Value=JavaScript

#### ClearFilters  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[library JS: filter-grid]`

#### SetFilters  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[library JS: filter-grid]`

#### Tabs  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[library JS: tabs]`

#### NotificationHandler  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: Decision → IfPath → Notification → Decision → IfPath → Notification → Decision → IfPath → Notification → Decision → IfPath → Notification → SetValue
- Flow (branch-structured):
  - **Decision**
    - IF `MessageType == Success` →
      - Notification: Message=Message
  - **Decision**
    - IF `MessageType == Error` →
      - Notification: Message=Message
  - **Decision**
    - IF `MessageType == Info` →
      - Notification: Message=Message
  - **Decision**
    - IF `MessageType == Warning` →
      - Notification: Message=Message
  - SetValue: Target=MessageType; Value=MessageType

#### WorkflowSteps  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[library JS: workflow-steps]`

#### ToggleButton  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[DOM-manipulation JS]`

#### ClientSideRepeaterDataGrid  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[library JS: repeater-datagrid-client-side]`

#### ClientSideRepeaterDataGridState  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript → SetValue
  - JavaScript  `[library JS: repeater-datagrid-client-side]`
  - SetValue: Target=State; Value=JavaScript

#### ClientSideRepeaterDataGridGetData  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript → SetValue
  - JavaScript  `[library JS: repeater-datagrid-client-side]`
  - SetValue: Target=Data; Value=JavaScript

#### PageLoader  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[library JS: page-loader]`

#### ConditionalColumnsStyling  [from script, surface: app]
- Trigger: **other (helper script)**
- Sequence: JavaScript
  - JavaScript  `[library JS: conditional-datagrid-styling]`

## Tier-A — notification points

> Verbatim message text (expressions preserved), severity decoded from `NotificationType` (1=success, 3=error, other=info), and dialog (blocking confirm) vs toast. These target the **current operator** (not an actor signal — see access-control).

- `UsersDataGrid.Delete.Click` (Users) · dialog — "'Are you sure you want to delete this user?\n\n ' + {0}" [from design model]
- `EditSaveButton.Click` (app) · dialog — "'Are you sure you want to edit this user?\n\n ' + {0}" [from design model]
- `AddSaveButton.Click` (app) · dialog — "'Are you sure you want to add this user?\n\n ' + {0}" [from design model]
- `CostCentreDataGrid.Delete.Click` (CostCentres) · dialog — "'Are you sure you want to delete this cost centre?\n\n ' +{0}" [from design model]
- `EditSaveButton.Click` (app) · dialog — "'Are you sure you want to edit this cost centre?\n\n ' + {0}" [from design model]
- `AddSaveButton.Click` (app) · dialog — "'Are you sure you want to add this cost centre?\n\n ' + {0}" [from design model]
- `BusinessUnitDataGrid.Delete.Click` (BusinessUnits) · dialog — "'Are you sure you want to delete this business unit?\n\n ' + {0}" [from design model]
- `EditSaveButton.Click` (app) · dialog — "'Are you sure you want to edit this business unit?\n\n ' + {0}" [from design model]
- `AddSaveButton.Click` (app) · dialog — "'Are you sure you want to add this business unit?\n\n ' + {0}" [from design model]
- `BeneficiaryDataGrid.Delete.Click` (Beneficiaries) · dialog — "'Are you sure you want to delete this beneficiary?\n\n'+ {0}" [from design model]
- `EditSaveButton.Click` (app) · dialog — "'Are you sure you want to edit this beneficiary?\n\n ' + {0}" [from design model]
- `AddSaveButton.Click` (app) · dialog — "'Are you sure you want to add this beneficiary?\n\n ' + {0}" [from design model]
- `BankDataGrid.Delete.Click` (Banks) · dialog — "'Are you sure you want to delete this bank?\n\n ' +{0}" [from design model]
- `EditSaveButton.Click` (app) · dialog — "'Are you sure you want to edit this bank?\n\n ' + {0}" [from design model]
- `AddSaveButton.Click` (app) · dialog — "'Are you sure you want to add this bank?\n\n ' + {0}" [from design model]
- `BankAccountDataGrid.Delete.Click` (BankAccounts) · dialog — "'Are you sure you want to delete this bank account?\n\n ' + {0}" [from design model]
- `EditSaveButton.Click` (app) · dialog — "'Are you sure you want to edit this bank account?\n\n ' + {0}" [from design model]
- `AddSaveButton.Click` (app) · dialog — "'Are you sure you want to add this bank account?\n\n ' + {0}" [from design model]
- `BankPaymentSetupDataGrid.Delete.Click` (BankPaymentSetup) · dialog — "'Are you sure you want to delete this bank payment setup ?\n\n' + {0}+' - '+ {1}" [from design model]
- `EditSaveButton.Click` (app) · dialog — "'Are you sure you want to edit this bank payment setup?\n\n ' + {0}+' - '+ {1}" [from design model]
- `AddSaveButton.Click` (app) · dialog — "'Are you sure you want to add this bank payment setup?\n\n ' + {0}+' - '+ {1}" [from design model]
- `DepartmentDataGrid.Delete.Click` (Department) · dialog — "'Are you sure you want to delete this department ?\n\n' + {0}" [from design model]
- `EditSaveButton.Click` (app) · dialog — "'Are you sure you want to edit this department setup?\n\n ' + {0}" [from design model]
- `AddSaveButton.Click` (app) · dialog — "'Are you sure you want to add this department ?\n\n ' + {0}" [from design model]
- `PaymentReasonDataGrid.Delete.Click` (PaymentReason) · dialog — "'Are you sure you want to delete this payment reason ?\n\n' + {0}" [from design model]
- `EditSaveButton.Click` (app) · dialog — "'Are you sure you want to edit this payment reason ?\n\n ' + {0}" [from design model]
- `AddSaveButton.Click` (app) · dialog — "'Are you sure you want to add this payment reason ?\n\n ' + {0}" [from design model]
- `PaymentSetupDataGrid.Delete.Click` (PaymentSetup) · dialog — "'Are you sure you want to delete this payment setup ?\n\n'+ 'Transaction Type '+': '+{0}+'\n'+ 'Payment Method '+': '+{1}+'\n'+ 'Payment Reason '+': '+{2}+'\n'+ 'Bank Account '+': '+{3}" [from design model]
- `EditSaveButton.Click` (app) · dialog — "'Are you sure you want to edit this payment setup?\n\n'+ 'Transaction Type '+': '+{0}+'\n'+ 'Payment Method '+': '+{1}+'\n'+ 'Payment Reason '+': '+{2}+'\n'+ 'Bank Account '+': '+{3}" [from design model]
- `AddSaveButton.Click` (app) · dialog — "'Are you sure you want to add this payment setup?\n\n'+ 'Transaction Type '+': '+{0}+'\n'+ 'Payment Method '+': '+{1}+'\n'+ 'Payment Reason '+': '+{2}+'\n'+ 'Bank Account '+': '+{3}" [from design model]
- `DraftTransactionsDataGrid.Delete.Click` (DraftManualPaymentCapture) · dialog — "'Are you sure you want to delete this draft payment transaction ?'" [from design model]
- `CancelLink.Click` (app) · dialog — "'Are you sure you want to cancel the payment capture ?'" [from design model]
- `SaveDraftButton.Click` (app) · toast · info — "Transaction progress saved" [from design model]
- `WhitelistedBeneficiaryDataGrid.Select.Click` (BeneficiaryDetails) · toast · success — "'Whitelisted beneficiary: '+ {0}+' is successfully selected'" [from design model]
- `SaveDraftButton.Click` (app) · toast · info — "'Please select a whitelisted beneficiary or unselect the whitelisted beneficiary button'" [from design model]
- `NextButton.Click` (app) · toast · info — "Please select a whitelisted beneficiary or unselect the whitelisted beneficiary button" [from design model]
- `AttachmentsDataGrid.Delete.Click` (AttachmentsAndNotes) · dialog — "'Are you sure you want to delete the attachement document ?\n\n ' + {0}" [from design model]
- `NoteDataGrid.Delete.Click` (app) · dialog — "'Are you sure you want to delete this note?\n\n ' + {0}" [from design model]
- `NoteEditSaveButton.Click` (AttachmentsAndNotes) · dialog — "'Are you sure you want to edit this note?\n\n ' + {0}" [from design model]
- `NoteAddSaveButton.Click` (AttachmentsAndNotes) · dialog — "'Are you sure you want to add this Note ?\n\n ' + {0}" [from design model]
- `CancelDuplicateTransactionButton.Click` (AttachmentsAndNotes) · dialog — "'Are you sure you want to cancel the payment capture ?'" [from design model]
- `CreateAndEditApprovalLevelScript` (app) · dialog — "'Are you sure you want to '+ {0} +' the approval level ?\n\n'+ {1}+'\n'+ {2}+'\n'+ {3}" [from design model]
- `ApprovalLevelDataGrid.Delete.Click` (ApprovalLevels) · dialog — "'Are you sure you want to delete the approval level ?\n\n'+ {0} +'\n'+ {1} +'\n'+ {2} +'\n'" [from design model]
- `AmountDataGrid.Delete.Click` (ApprovalLevels) · dialog — "'Are you sure you want to delete the approval level amount ?\n\n'+ {0}" [from design model]
- `EditSaveApprovalLevelRulesButton.Click` (ApprovalLevelRules) · toast · success — "'Approval Level rules have been successfully updated'" [from design model]
- `EditSaveApprovalLevelRulesButton.Click` (ApprovalLevelRules) · toast · error — "'Approval Level rules update has been unsuccessful'" [from design model]
- `NotificationHandler` (app) · toast · success — "⟨Message⟩" [from design model]
- `NotificationHandler` (app) · toast · error — "⟨Message⟩" [from design model]
- `NotificationHandler` (app) · toast · info — "⟨Message⟩" [from design model]

## Tier-A — validation

- `EmailTextBox` · required+email · /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test({0}) · "Please enter a valid email" [from design model]  `[AI-SUGGESTED: email]`
- `BusinessUnitDepartmentsCheckBoxList` · validation · "Please select a department" [from design model]
- `NameTextBox` · required · "Please enter a name" [from design model]
- `DescriptionTextBox` · required · "Please enter a description" [from design model]
- `BusinessUnitDropDown` · required · "Please select a business unit" [from design model]
- `CodeTextBox` · required · "Please enter a code" [from design model]
- `DepartmentsCheckBoxList` · required · "Please select a department" [from design model]
- `AccountNameTextBox` · required · "Please enter an account name" [from design model]
- `AccountNumberTextBox` · required+numeric · /^[0-9]+$/.test({0}) [from design model]  `[AI-SUGGESTED: numeric]`
- `AccountTypeDropDown` · required · "Please select an account type" [from design model]
- `BankDropDown` · required · "Please select a bank" [from design model]
- `IbanTextBox` · required · "Please enter a Iban" [from design model]
- `BusinessUnitDropDown` · validation · "Please select a business unit" [from design model]
- `UniversalBranchCodeTextBox` · required+numeric · /^\d{6}$/.test({0}) · "Please enter a 6-digit branch code" [from design model]  `[AI-SUGGESTED: numeric]`
- `UniversalSwiftCodeTextBox` · required+length · /^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$/.test({0}) [from design model]  `[AI-SUGGESTED: length]`
- `AccountNameTextBox` · required · "Please enter a account name" [from design model]
- `AccountNumberTextBox` · required+numeric · /^\d{6,11}$/.test({0}) [from design model]  `[AI-SUGGESTED: numeric]`
- `BankPaymentMethodDropDown` · required · "Please select a payment method" [from design model]
- `TransferMethodDropDown` · required · "Please select a transfer method" [from design model]
- `ServiceLevelCodeDropDown` · required · "Please select a service level code" [from design model]
- `ChargeBearerDropDown` · required · "Please select a charge bearer" [from design model]
- `CutOffTimeTextBox` · required · "Please enter a cut off time" [from design model]
- `BusinessUnitDropDown` · required · "Please enter a business unit" [from design model]
- `DepartmentDropDown` · required · "Select a department" [from design model]
- `TransactionTypeDropDown` · required · "Please enter a transaction type" [from design model]
- `PaymentMethodDropDown` · required · "Please enter a payment method" [from design model]
- `PaymentReasonDropDown` · required · "Please enter a payment reason" [from design model]
- `BankAccountDropDown` · required · "Please enter a bank account" [from design model]
- `BusinessUnitDepartmentDropDown` · required · "Please select a business unit department" [from design model]
- `TransactionTypeDropDown` · required · "Please select a transaction type" [from design model]
- `BankAccountDropDown` · required · "Please select a bank account" [from design model]
- `BankPaymentMethodDropDown` · required · "Please select a bank payment method" [from design model]
- `PaymentReasonDropDown` · required · "Please select a payment reason" [from design model]
- `AmountTextBox` · required · "Please enter an amount" [from design model]
- `CurrencyTypeDropDown` · required · "Please select a currency" [from design model]
- `ExecutionDatePicker` · required · "Please select a date" [from design model]
- `PaymentReferenceTextBox` · required · "Please enter a payment reference" [from design model]
- `AccountNumberTextBox` · required+numeric · /^\d{1,16}$/.test(String({0})) · "Please enter a correctly formatted account number (Numeric,16 digits)" [from design model]  `[AI-SUGGESTED: numeric]`
- `SortCodeTextBox` · required+numeric · /^\d{6}$/.test(String({0})) · "Please enter a correctly formatted sort code (Numeric, 6 digits)" [from design model]  `[AI-SUGGESTED: numeric]`
- `DepartmentDropDown` · validation · "Please select a department" [from design model]
- `MaxApprovalAmountTextBox` · numeric · /^\d+$/.test(String({0})) · "Please enter only numbers" [from design model]  `[AI-SUGGESTED: numeric]`
- `ApprovalAmount` · numeric · /^\d+$/.test(String({0})) · "Please enter only numbers" [from design model]  `[AI-SUGGESTED: numeric]`
- `ManagerialApproval` · pattern · /^[1-3]$/.test(String({0})) · "Please enter a valid number (between 1-3)" [from design model]  `[AI-SUGGESTED: pattern]`
- `TreasuryApproval` · pattern · /^[1-3]$/.test(String({0})) · "Please enter a valid number (between 1-3)" [from design model]  `[AI-SUGGESTED: pattern]`
- `BankReleaseApproval` · pattern · /^[1-3]$/.test(String({0})) · "Please enter a valid number (between 1-3)" [from design model]  `[AI-SUGGESTED: pattern]`
- Required inputs (from control `Required` flags): `FirstNameTextBox`, `LastNameTextBox`, `PasswordTextBox`, `BusinessUnitDropDown`, `RolesCheckBoxList`, `IbanTextBox` [from design model]

## Tier-A — edge / empty / error / loading state signals

> The toggle / error-type / guard predicate is Tier-A (provably in the model). The **state classification** (loading vs empty vs error vs permission) is a Tier-B reading — a hidden control is ambiguous (busy vs empty vs initial-hide). See 0a / 0f above.

- **error notification** · `EditSaveApprovalLevelRulesButton.Click` (ApprovalLevelRules) — "'Approval Level rules update has been unsuccessful'" [from design model]
- **error notification** · `NotificationHandler` (app) — "⟨Message⟩" [from design model]
- **visibility/loading toggles**: 173 distinct SetValue state write(s) across 19 surface(s) — classified 119 state, 48 shown, 6 empty/hidden [from design model] `[AI-SUGGESTED: state classification]`
  - targets: `AddSaveButton`, `AdhocBeneficiaryGrid`, `AdhocBeneficiaryLabel`, `AmountDescriptionLabel`, `AmountValueLabel`, `BankAccountValueLabel`, `BankLabel`, `BankPaymentMethodValueLabel`, `BankValueLabel`, `BeneficiaryAccountNumberValueLabel`, `BeneficiaryNameValueLabel`, `BeneficiarySortCodeValueLabel`, `BeneficiaryValueLabel`, `BusinessUnitDepartmentsLabel`, `BusinessUnitValueLabel` _(+35 more)_ [from design model]
- **empty/edge guard** · `EditSaveButton.Click` (app) — IF `SelectedOptions != 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `DraftTransactionsDataGrid.Edit.Click` (DraftManualPaymentCapture) — IF `TransactionManualCaptureStepId == 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `PaymentsDetails.Load` (PaymentsDetails) — IF `Amount != 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `PaymentsDetails.Load` (PaymentsDetails) — IF `CurrencyId != 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `LoadScript` (app) — IF `BeneficiaryId != 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `WhitelistAndAdhocRadioButtonList.Change` (BeneficiaryDetails) — IF `BeneficiaryId != 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `SaveDraftButton.Click` (app) — IF `SelectedDatagridRowIdLabel != 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `AttachmentsAndNotes.Load` (AttachmentsAndNotes) — IF `Transactions != 0` [from design model] `[AI-SUGGESTED: empty/count guard]`
- **empty/edge guard** · `Review.Load` (Review) — IF `BeneficiaryId != 0` [from design model] `[AI-SUGGESTED: empty/count guard]`

## Tier-A — bespoke inline-JS rules

> The app's own inline logic blocks, verbatim (capped). Copy-pasted `stadium-software` library JS and DOM/timing helpers are excluded (framework UI, catalogued in `modules`). A Tier-2 advisory summary of what these rules DO is added by the extraction skill (Phase B).

- `ScriptToUpdateAmountDatagridWithPrePopulatedValues` (ApprovalLevels) — `// Inputs: // DataList = list of { Level, MaxApprovalAmount } // LoopValue = current item from API (contains MaxApproval…` [from script, surface: ApprovalLevels]
