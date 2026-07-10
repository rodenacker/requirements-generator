---
stadium_asset: business-rules
app: MemberAdmin
file_guid: 785d3104-7f1a-4d0d-9689-566e0c21295b
designer_version: 6.14.3378.13771
selected_package: 9edc4a95-3fde-45b4-899a-2a59d1c23452.sapz
deployment_count: 3
last_published: 2026-06-24 08:45:30.9660341
extracted_from: C:\Stadium 6 Web Apps\785d3104-7f1a-4d0d-9689-566e0c21295b
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Business rules & behaviour — MemberAdmin

## Tier-A — event logic (scripts → action sequences)

> Each script is classified by its **trigger** (0g): *user-initiated* (a control event — `.Click/.Change/…`), *automatic-on-open* (a page/template `.Load`), or *other* (a helper invoked via CallScript, or a timer/lifecycle hook). User-initiated scripts are rendered gesture-first; the *goal* a gesture serves is advisory (Tier-B), the gesture itself is fact.

### User-initiated — gesture → outcome

#### MemberAddButton.Click  [from script, surface: Members]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Add Member" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=MemberAdd

#### MembersDataGrid.Edit.Click  [from script, surface: Members]
- Trigger: **user-initiated**  (`.click`)
- User clicks `MembersDataGrid` → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=MemberUpdate / ID

#### MembersDataGrid.Delete.Click  [from script, surface: Members]
- Trigger: **user-initiated**  (`.click`)
- User clicks `MembersDataGrid` → runs the flow below
- Sequence: DisplayMessageBox → ExecuteConnector → Notification → CallScript
  - DisplayMessageBox: Message=Email
  - ExecuteConnector: ConnectorFunction=MemberDelete
  - Notification: Message=Email
  - CallScript: ScriptToCall=MembersDGLoad

#### SaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: ExecuteConnector → Notification → NavigateToPage
  - ExecuteConnector: ConnectorFunction=MemberInsert
  - Notification: Message=EmailTextBox
  - NavigateToPage: Destination=Members

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=Members

#### SaveButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Save" → runs the flow below
- Sequence: ExecuteConnector → Notification → NavigateToPage
  - ExecuteConnector: ConnectorFunction=MemberUpdate
  - Notification: Message=EmailTextBox
  - NavigateToPage: Destination=Members

#### CancelButton.Click  [from script, surface: app]
- Trigger: **user-initiated**  (`.click`)
- User clicks "Cancel" → runs the flow below
- Sequence: NavigateToPage
  - NavigateToPage: Destination=Members

### Automatic — on page / template open

#### Members.Load  [from script, surface: Members]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: CallScript
  - CallScript: ScriptToCall=MembersDGLoad

#### MemberAdd.Load  [from script, surface: MemberAdd]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=CitiesSelect
  - SetValue: Target=Options

#### MemberUpdate.Load  [from script, surface: MemberUpdate]
- Trigger: **automatic-on-open**  (`.load`)
- Sequence: ExecuteConnector → SetValue → ExecuteConnector → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue → SetValue
  - ExecuteConnector: ConnectorFunction=CitiesSelect
  - SetValue: Target=Options
  - ExecuteConnector: ConnectorFunction=MemberSelect
  - SetValue: Target=FirstNameTextBox; Value=FirstName
  - SetValue: Target=LastNameTextBox; Value=LastName
  - SetValue: Target=EmailTextBox; Value=Email
  - SetValue: Target=PasswordTextBox; Value=Password
  - SetValue: Target=DOBDatePicker; Value=DOB
  - SetValue: Target=CityDropDown; Value=CityID
  - SetValue: Target=SubscribedCheckBox; Value=Subscribed

### Other — helper scripts / timers / lifecycle

#### MembersDGLoad  [from script, surface: Members]
- Trigger: **other (helper script)**
- Sequence: ExecuteConnector → SetValue
  - ExecuteConnector: ConnectorFunction=MembersSelect
  - SetValue: Target=Data

## Tier-A — notification points

> Verbatim message text (expressions preserved), severity decoded from `NotificationType` (1=success, 3=error, other=info), and dialog (blocking confirm) vs toast. These target the **current operator** (not an actor signal — see access-control).

- `MembersDataGrid.Delete.Click` (Members) · dialog — "'Are you sure you want to delete "' + {0} + '"?'" [from design model]
- `MembersDataGrid.Delete.Click` (Members) · toast · success — "'Member "' + {0} + '" deleted'" [from design model]
- `SaveButton.Click` (app) · toast · success — "'User "' + {0} + '" added'" [from design model]
- `SaveButton.Click` (app) · toast · success — "'User "' + {0} + '" updated'" [from design model]

## Tier-A — validation

- `FirstNameTextBox` · required · "Please add a value" [from design model]
- `LastNameTextBox` · required · "Please add a value" [from design model]
- `EmailTextBox` · required+email · /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test({0… · "Please enter a valid email address" [from design model]  `[AI-SUGGESTED: email]`
- `PasswordTextBox` · required+length · /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[\w!@#$%^&*]{8,16}$/.test({0}) · "8 – 16 characters, at least one number, at least one special character, upper and lowercase characters" [from design model]  `[AI-SUGGESTED: length]`
- `DOBDatePicker` · required+date · dayjs({0}) < dayjs().add(-18,'year') · "The member must be over 18" [from design model]  `[AI-SUGGESTED: date]`
- `CityDropDown` · required · "Please select a value" [from design model]

## Tier-A — edge / empty / error / loading state signals

_No explicit spinner/visibility toggles, error notifications, or empty/null guards in the design model._

## Tier-A — bespoke inline-JS rules

_No bespoke (non-library, non-DOM/timing) inline-JS blocks in the design model._
