# stadium/sapz-spec.md — the `.sapz` design model: what to take, what to avoid

The `.sapz` deployment package (a ZIP wrapping a `sqlitedata` SQLite file) is the Stadium Designer's clean design-time model and the extractor's primary source of truth. But not all of it is worth surfacing — some tables are gold, some are noise. This is the take/avoid guide.

## Selection

An app's `App_Data/Updates/` holds one `.sapz` per deployment, named `<GUID>.sapz`. The extractor picks the **most recent** by joining each package GUID to `administration.db > ApplicationUpdates.DateTime` (newest `DateTime` wins; falls back to file mtime). Older packages are previous deployments — ignore them.

## TAKE — the clean central data model

- **`Field` → `StructDataType` (via `Field.ParentID`)** — the normalized field-to-struct membership. A `StructDataType` is a record type; its `Field` children are its members.
- **Field primitive type — via the field's child `SimpleDataType`** — join `SimpleDataType.ParentID = Field.ID` to read the concrete primitive (`String`, `Int32`, `DateTime`, `Boolean`, `Decimal`, …). These design-model types are **more accurate than the SQL parameters**, which Stadium emits as uniform `String`; the extractor prefers the design-model type when enriching column types.
- **`Field.IsDataField`** — nominally the flag distinguishing a real persisted data attribute from a transient/UI-only field, and it exists ONLY in the design model. **In practice it is uniformly `0` across every deployed `.sapz` in the observed corpus** (data, proc and API apps alike), so it is **not** a usable discriminator and the extractor does **not** gate on it — the envelope denylist (`_ENVELOPE_DENY` / `_ENTITY_DENY` in `extract_stadium_app.py`) is the real guard against binding scaffolding. The flag is still recorded in `model.json > data_dictionary` for forensic completeness.
- **Clean design-time identifiers.** Names here are unmangled. The deployed source applies an ASCII encoding to identifiers — `_95` = `_`, `_46` = `.` — so a deployed name like `Member_95Id` is `Member_Id` and `Members_46Email` is `Members.Email`. Prefer the `.sapz` name whenever both exist.

The extractor already projects the useful parts into `model.json > data_dictionary` (one entry per struct: `struct_id`, `field_count`, and each field's `name` / `type` / `is_data_field`). The per-app `data-model` asset's column types are sourced from it.

## Stored procedures & web-service functions — also data-model sources

A `ConnectorFunction` is not always a SQL query. Two other flavours are first-class data-model evidence (see `extract_stadium_app.py` `_sp_shape` / `_ws_shape`, and `asset-schemas.md` §(e)):

- **Stored procedures** (`type == StoredProcedure`) — the function `Text` is only the **proc name** (`dbo.prc_Stadium_WO_Select`), so SQL parsing sees nothing. The **entity + operation** come from the name pattern `<prefix>_[Stadium_]<Entity>[_<qual>]_<Op>` (prefix ∈ {sp, prc, usp, fn, udf, proc}; rightmost op-keyword wins), and the **fields are the parameters** (minus the `Success`/`Message`/`RaiseExceptions` envelope). The name pattern is an **empirical Twenty57 convention, not a platform guarantee** — a proc whose name yields no entity/op is listed under a Tier-B "unclassified stored procedures" heading, never fabricated.
- **Web-service functions** (`type == WebServiceFunction`) — props carry `HttpMethod` (0=GET,1=POST,2=PUT,3=DELETE), `Path`, and `BodyType`/`ResponseType` **GuidReferences**. The **entity name** resolves via `NamedItemID → CustomType.Name` (e.g. `fullmember`, `payment`); the **fields** come from the function's own bound `Parameter(Body) → StructDataType → Field*` (request) and `DataResult(ResponseBody) → StructDataType → Field*` (response). The CRUD verb comes from the **path/name keyword** first (the corpus uses semantic `GET /deletemember`), falling back to the HTTP method. Field *types* are usually the weak `System.Object` here, so web-service fields are reliable by **name**, omitted by type.

## AVOID — the noise

- **`JsonData` property bags / `all_props`.** Every control/action node carries a `JsonData` blob of `{Name, ValueType, Value}` property items. Useful key props (Text, Required, Visible, …) are already extracted; the *full* bag is huge and almost entirely redundant with the deployed source. The forensic `model.json` keeps `all_props` for completeness — do not load it into the requirements flow.
- **`CustomType`** — **not** empty in web-service apps: it is the **name dictionary** a WebService Body/ResponseType `GuidReference` resolves against (dozens–hundreds per API app). Its own `JsonData.Fields` GUIDs do **not** resolve via table joins, so read a type's *fields* from the function-bound struct (above), not from the CustomType node. (In SQL-only apps it is frequently empty — check.)
- **`StructDataType` has no `Name` column.** You still cannot read a struct's name directly, but you no longer must guess only from SQL: a struct is named transitively via **the function that binds it** — its parent `Parameter`/`DataResult` under a `ConnectorFunction` whose Body/Response `GuidReference → CustomType.Name`. Field-set-to-SQL matching remains a fallback. Structs are numerous anonymous binding instances (parented by Field/ListDataType/DataResult/Parameter) — the extractor anchors entities on **functions**, not on the struct table.

## Net

Read the `.sapz` for the **clean typed data dictionary + unmangled names**; get **entity names + CRUD** from **three reconciled sources** — SQL tables/views, stored-proc names, and web-service CustomType refs (`reconcile_entities`, union by normalized name); get **field types** by precedence design-model `SimpleDataType` > SQL/proc `DbType` > web-service > omit-if-`Object`; get **security** from `administration.db`; get **modules + custom CSS** from the deployed `ClientApp`/`wwwroot`. No single source has everything — the extractor fuses them, which is why it reads the app folder, not just the `.sapz`.
