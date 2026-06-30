# stadium/sapz-spec.md — the `.sapz` design model: what to take, what to avoid

The `.sapz` deployment package (a ZIP wrapping a `sqlitedata` SQLite file) is the Stadium Designer's clean design-time model and the extractor's primary source of truth. But not all of it is worth surfacing — some tables are gold, some are noise. This is the take/avoid guide.

## Selection

An app's `App_Data/Updates/` holds one `.sapz` per deployment, named `<GUID>.sapz`. The extractor picks the **most recent** by joining each package GUID to `administration.db > ApplicationUpdates.DateTime` (newest `DateTime` wins; falls back to file mtime). Older packages are previous deployments — ignore them.

## TAKE — the clean central data model

- **`Field` → `StructDataType` (via `Field.ParentID`)** — the normalized field-to-struct membership. A `StructDataType` is a record type; its `Field` children are its members.
- **Field primitive type — via the field's child `SimpleDataType`** — join `SimpleDataType.ParentID = Field.ID` to read the concrete primitive (`String`, `Int32`, `DateTime`, `Boolean`, `Decimal`, …). These design-model types are **more accurate than the SQL parameters**, which Stadium emits as uniform `String`; the extractor prefers the design-model type when enriching column types.
- **`Field.IsDataField`** — the flag distinguishing a real persisted data attribute from a transient/UI-only field. **This flag exists ONLY in the design model** — it is gone in the deployed source. It is the cleanest way to separate the true data shape from binding scaffolding.
- **Clean design-time identifiers.** Names here are unmangled. The deployed source applies an ASCII encoding to identifiers — `_95` = `_`, `_46` = `.` — so a deployed name like `Member_95Id` is `Member_Id` and `Members_46Email` is `Members.Email`. Prefer the `.sapz` name whenever both exist.

The extractor already projects the useful parts into `model.json > data_dictionary` (one entry per struct: `struct_id`, `field_count`, and each field's `name` / `type` / `is_data_field`). The per-app `data-model` asset's column types are sourced from it.

## AVOID — the noise

- **`JsonData` property bags / `all_props`.** Every control/action node carries a `JsonData` blob of `{Name, ValueType, Value}` property items. Useful key props (Text, Required, Visible, …) are already extracted; the *full* bag is huge and almost entirely redundant with the deployed source. The forensic `model.json` keeps `all_props` for completeness — do not load it into the requirements flow.
- **`CustomType`** — user-defined named types; **often empty** across apps. Check, but don't expect content.
- **`StructDataType` has no `Name` column.** You cannot read a struct's name directly. Identify it by **matching its field set to a SQL entity** (the connector queries name the real tables/columns; a struct whose fields are `{ID, FirstName, LastName, Email, …}` is the `Members` shape). The extractor leans on the connector SQL for entity names and uses the data dictionary only for *types*.

## Net

Read the `.sapz` for the **clean typed data dictionary + `IsDataField` + unmangled names**; get **entity names, CRUD operations, and SQL** from the connector queries (also in the model); get **security** from `administration.db`; get **modules + custom CSS** from the deployed `ClientApp`/`wwwroot`. No single source has everything — the extractor fuses them, which is why it reads the app folder, not just the `.sapz`.
