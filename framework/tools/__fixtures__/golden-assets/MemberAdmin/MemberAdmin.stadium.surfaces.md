---
stadium_asset: surfaces
app: MemberAdmin
file_guid: 785d3104-7f1a-4d0d-9689-566e0c21295b
designer_version: 6.14.3378.13771
selected_package: 9edc4a95-3fde-45b4-899a-2a59d1c23452.sapz
extracted_from: C:\Stadium 6 Web Apps\785d3104-7f1a-4d0d-9689-566e0c21295b
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Surfaces (screens, controls, layout) — MemberAdmin

> Tier-A = which surfaces/controls/data exist (authoritative). Tier-B = layout & control-choice (advisory; the system holds design authority).

## View / task / feature inventory

> Columns Page / Start / Design-surface / Reachable are **Tier-A** facts (design model + administration.db). **Inferred kind** is **Tier-B** `[AI-SUGGESTED]` (name-suffix taxonomy; bare nouns → entity-maintenance).

| Page | Start? | Design surface? | Reachable via nav? | Inferred kind |
|---|:---:|:---:|:---:|---|
| Members | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| MemberAdd |  | ✓ | ✓ | create `[AI-SUGGESTED]` |
| MemberUpdate |  | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |

## Members ⭐ start  ·  title: Members  ·  roles: User, Viewer, AllAccess
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `PageTitleLabel` — "Members"
    - StackLayout: `StackLayout`
      - Button: `MemberAddButton` — "Add Member"
    - StackLayout: `StackLayout`
      - DataGrid: `MembersDataGrid`  ·  grid: searchable
        - columns (in order): "Edit"(action), "Delete"(action), "ID"(hidden), "First Name", "Last Name", "Email", "DOB", "City", "City ID"(hidden), "Subscribed" [from design model]

## MemberAdd  ·  title: Member Add  ·  roles: AllAccess
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `PageTitleLabel` — "Add Member"
    - StackLayout: `StackLayout`
      - Grid: `Grid`
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
            - Label: `EmailLabel` — "Email"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - TextBox: `EmailTextBox`
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - Label: `PasswordLabel` — "Password"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - TextBox: `PasswordTextBox`
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - Label: `DOBLabel` — "DOB"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - DatePicker: `DOBDatePicker`  ·  hint: "Select a date"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - Label: `CityLabel` — "City"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - DropDown: `CityDropDown`  ·  hint: "Select a city" · dynamic choices (bound)
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - Label: `SubscribedLabel` — "Subscribed"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - CheckBox: `SubscribedCheckBox`
    - StackLayout: `StackLayout`
      - Button: `SaveButton` — "Save"
      - Button: `CancelButton` — "Cancel"

## MemberUpdate  ·  title: Member Update  ·  roles: AllAccess
  - GridLayout: `GridLayout`
    - StackLayout: `StackLayout`
      - Label: `PageTitleLabel` — "Update Member"
      - Label: `IDLabel`
    - StackLayout: `StackLayout`
      - Grid: `Grid`
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
            - Label: `EmailLabel` — "Email"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - TextBox: `EmailTextBox`
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - Label: `PasswordLabel` — "Password"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - TextBox: `PasswordTextBox`
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - Label: `DOBLabel` — "DOB"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - DatePicker: `DOBDatePicker`  ·  hint: "Select a date"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - Label: `CityLabel` — "City"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - DropDown: `CityDropDown`  ·  hint: "Select a city" · dynamic choices (bound)
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - Label: `SubscribedLabel` — "Subscribed"
        - CellGridLayout: `CellGridLayout`
          - CellStackLayout: `CellStackLayout`
            - CheckBox: `SubscribedCheckBox`
    - StackLayout: `StackLayout`
      - Button: `SaveButton` — "Save"
      - Button: `CancelButton` — "Cancel"

## Action affordances → candidate tasks

> Per surface: actionable controls whose label carries an action verb. Control · label · wired script are **Tier-A** facts; the candidate **task** is **Tier-B** `[AI-SUGGESTED]` (verb taxonomy; UI chrome excluded). The flat visible-terms list in `glossary` is retained separately.

### Members
- `MemberAddButton` — "Add Member" — wired to `MemberAddButton.Click`  →  candidate task: **Add Member** `[AI-SUGGESTED]`

## Tier-A — screen ↔ entity (best-effort)

| Page | Likely entity |
|---|---|
| Members | Members |
| MemberAdd | — |
| MemberUpdate | — |
