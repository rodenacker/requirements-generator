---
stadium_asset: surfaces
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
# Surfaces (screens, controls, layout) — MemberAdmin

> Tier-A = which surfaces/controls/data exist (authoritative). Tier-B = layout & control-choice (advisory; the system holds design authority).

## View / task / feature inventory

> Columns Page / Title / Route / Start / Design-surface / Reachable / Route-declared are **Tier-A** facts (design model + administration.db + rendered `page-routes.js`). **Inferred kind** is **Tier-B** `[AI-SUGGESTED]` (name-suffix taxonomy; bare nouns → entity-maintenance). Title + Route come from the rendered router `[from rendered routes]`.

| Page | Title | Route | Start? | Design surface? | Reachable via nav? | Route-declared? | Inferred kind |
|---|---|---|:---:|:---:|:---:|:---:|---|
| Members | Members | `/Members` | ✓ | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |
| MemberAdd | Member Add | `/MemberAdd` |  | ✓ | ✓ | ✓ | create `[AI-SUGGESTED]` |
| MemberUpdate | Member Update | `/MemberUpdate` |  | ✓ | ✓ | ✓ | entity-maintenance `[AI-SUGGESTED]` |

## Members ⭐ start  ·  title: Members  ·  roles: User, Viewer, AllAccess
  - Button: `MemberAddButton` — "Add Member"
  - DataGrid: `MembersDataGrid`  ·  grid: searchable
    - columns (in order): "Edit"(action), "Delete"(action), "ID"(hidden), `FirstName` "First Name", `LastName` "Last Name", "Email", "DOB", "City", `CityID` "City ID"(hidden), "Subscribed" [from design model]
- Visible terms: "Members" [from design model]
> Layout: 2 meaningful control(s) within 4 layout container(s); max control-tree nesting depth 3 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — Members (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `MembersDataGrid` → `Members.MemberDelete`
- `MembersDGLoad` → `Members.MembersSelect`

## MemberAdd  ·  title: Member Add  ·  roles: AllAccess
  - TextBox: `FirstNameTextBox`
  - TextBox: `LastNameTextBox`
  - TextBox: `EmailTextBox`
  - TextBox: `PasswordTextBox`
  - DatePicker: `DOBDatePicker`  ·  hint: "Select a date"
  - DropDown: `CityDropDown`  ·  hint: "Select a city" · dynamic choices (bound)
  - CheckBox: `SubscribedCheckBox`
  - Button: `SaveButton` — "Save"
  - Button: `CancelButton` — "Cancel"
- Visible terms: "Add Member", "First Name", "Last Name", "Email", "Password", "DOB", "City", "Subscribed" [from design model]
> Layout: 9 meaningful control(s) within 33 layout container(s); max control-tree nesting depth 6 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — MemberAdd (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `SaveButton` → `Members.MemberInsert`
- `MemberAdd` → `Members.CitiesSelect`

## MemberUpdate  ·  title: Member Update  ·  roles: AllAccess
  - TextBox: `FirstNameTextBox`
  - TextBox: `LastNameTextBox`
  - TextBox: `EmailTextBox`
  - TextBox: `PasswordTextBox`
  - DatePicker: `DOBDatePicker`  ·  hint: "Select a date"
  - DropDown: `CityDropDown`  ·  hint: "Select a city" · dynamic choices (bound)
  - CheckBox: `SubscribedCheckBox`
  - Button: `SaveButton` — "Save"
  - Button: `CancelButton` — "Cancel"
- Visible terms: "Update Member", "First Name", "Last Name", "Email", "Password", "DOB", "City", "Subscribed" [from design model]
> Layout: 9 meaningful control(s) within 33 layout container(s); max control-tree nesting depth 6 (per-node layout omitted — see model.json). Advisory.

### source-UI reference — MemberUpdate (from rendered view)
> Backend operations the deployed page invokes (UI control → connector.function), decoded verbatim from the rendered route strings. §8 existing-tool reference (Tier-A).
- `SaveButton` → `Members.MemberUpdate`
- `MemberUpdate` → `Members.CitiesSelect`
- `MemberUpdate` → `Members.MemberSelect`

## User tasks (per view)

> The per-view user-task inventory — the verb-labelled action affordances triangulated with wired backend operations, DataGrids and page-kinds, with a ≥1-task-per-view completeness guarantee — is emitted as its own asset: see `MemberAdmin.stadium.tasks.md`.

## Tier-A — screen ↔ entity (best-effort)

| Page | Likely entity |
|---|---|
| Members | Members |
| MemberAdd | — |
| MemberUpdate | — |
