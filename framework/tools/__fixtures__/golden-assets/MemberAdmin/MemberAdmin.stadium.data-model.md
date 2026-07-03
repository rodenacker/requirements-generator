---
stadium_asset: data-model
app: MemberAdmin
file_guid: 785d3104-7f1a-4d0d-9689-566e0c21295b
designer_version: 6.14.3378.13771
selected_package: 9edc4a95-3fde-45b4-899a-2a59d1c23452.sapz
extracted_from: C:\Stadium 6 Web Apps\785d3104-7f1a-4d0d-9689-566e0c21295b
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Data model — MemberAdmin

> Entities + fields reconciled across SQL queries/views, stored procedures and web-service calls (union by name). Every field carries a `[from …]` locator naming its exact source.

## Tier-A — entities & fields

### Cities  ·  sources: sql  ·  operations: SELECT
- `Cities.City` : String [from connector: CitiesSelect]
- `Cities.ID` : Int32 [from connector: CitiesSelect]

### Members  ·  sources: sql  ·  operations: DELETE, INSERT, SELECT, UPDATE
- `Members.City` : String [from connector: MembersSelect]
- `Members.CityID` : String [from connector: MembersSelect]  _(+2 more)_
- `Members.DOB` : String [from connector: MembersSelect]  _(+2 more)_
- `Members.Email` : String [from connector: MembersSelect]  _(+2 more)_
- `Members.FirstName` : String [from connector: MembersSelect]  _(+2 more)_
- `Members.ID` : String [from connector: MembersSelect]  _(+1 more)_
- `Members.LastName` : String [from connector: MembersSelect]  _(+2 more)_
- `Members.Password` : String [from connector: MemberInsert]  _(+1 more)_
- `Members.Subscribed` : String [from connector: MembersSelect]  _(+2 more)_
- `Members.UpdateDateTime` [from connector: MemberInsert]

> The design model defines 26 internal data-type instances (control/result/parameter bindings); field types above are sourced from them where concrete. Full detail is in the forensic model.json.

## Tier-A — CRUD matrix

| Entity | SELECT | INSERT | UPDATE | DELETE | Evidence |
|---|:---:|:---:|:---:|:---:|---|
| Cities | ✓ |  |  |  | sql |
| Members | ✓ | ✓ | ✓ | ✓ | sql |
