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

## The script / action (behavioural) model — how app behaviour is stored

The `.sapz` also holds the **complete behavioural model** (not just the data model), and the extractor now walks it structurally (`build_action_tree` in `extract_stadium_app.py`, emitted as `scripts[].tree` alongside the flat back-compat `scripts[].actions`). The shapes:

- **Script → ExecutionPath → Actions.** A `Script` row (cols `IsEventHandlerScript, Name, ID, ParentID` — **no** `JsonData`) has exactly one child of type `Twenty57.Stadium.API.Scripts.ExecutionPath` whose `props["Actions"]` is the **ordered GUID list of the script's root actions**, in execution order. (Golden: MemberAdmin `MemberUpdate.Load` → 10 ordered actions — `__fixtures__/execpath-memberadmin-memberupdate-load.json`.) The flat `collect_actions` DFS is *approximately* right for linear scripts but **scrambles branches**, so the tree walk keys off the `ExecutionPath.Actions` order instead.
- **Decision → ExecutionPaths → IfPath → {Conditions, Actions}.** A `Decision.Decision` action carries `ShowElse` (bool) + `props["ExecutionPaths"]` (ordered GUID list) → `Decision.IfPath` nodes. Each `IfPath` carries `props["Actions"]` (that branch's ordered steps) + `props["Conditions"]` (predicate GUID list). Branch actions may themselves be `Decision`s (nesting confirmed; the walker caps depth and de-dupes with a `seen` set). The trailing **else** branch is a plain `ExecutionPath` node (no `Conditions`), present only when `ShowElse=True` — keyed off the type-suffix, not an `IfPath`.
- **Condition shape.** A `Conditions` GUID resolves to a `UniqueItemExpando` of type `Twenty57.Stadium.Actions.Decision.Condition` with props `{Value1: GuidReference{NamedItemID→control/field/variable}, Operator: <int enum>, Value2, Join: <int AND/OR>}`. A predicate reads `<operand> <op> <value>`; compound conditions join with each condition's own `Join` word.
- **Bounded JS opacity.** A `JavaScript` action's body (`Code.FormatString`) is captured, not resolved into the branch tree — but it is **classified** (§4.2): a copy-pasted `stadium-software` **library** block (`[library JS: <slug>]`), a **timing** hack (`[timing JS]`), **DOM** manipulation (`[DOM-manipulation JS]`), or bespoke **logic** (`[custom JS]` + the verbatim body, capped; also catalogued in `business-rules`' `bespoke inline-JS rules` section). JS-computed navigation (`jsGETCurrentURl` / custom JS) is still not a captured nav edge, rendered `[gap: JS-computed nav]`. Never bridged by a guess.

### GUID normalization (the `bytes_le` rule)

Table `ID`/`ParentID` columns are stored as **.NET binary GUID blobs** (`bytes_le`, mixed-endian), but the `Actions`/`Conditions`/`ExecutionPaths` **values** inside a `JsonData` prop bag are **string GUIDs**. Both must canonicalize to the same form before an id-index lookup: `str(uuid.UUID(bytes_le=<blob>))` for a 16-byte blob, `str(uuid.UUID(<string>))` for a string. The extractor's `norm_guid` handles both — always normalize *both* sides of a lookup (a raw un-normalized Actions string resolves to nothing, which is the classic false-negative that makes the behavioural model look empty).

### `Decision.Condition` Operator / Join enum table

The `Operator` and `Join` ints were decoded empirically over the 20-app corpus (correlating each condition's int against the operator phrase Stadium embeds in its auto-generated Decision node names — e.g. `…GreaterThanOrEquals0`, `dec…OrBefore` — plus literal-value samples). **Standard comparison ordering.** Any unmapped code degrades to `op<N>` / `join<N>` — never a wrong symbol.

| `Operator` | Symbol | Confidence |
|:---:|:---:|---|
| 0 | `==` | corpus-confirmed |
| 1 | `!=` | best-guess (consultant-approved 2026-07-02) |
| 2 | `<` | best-guess |
| 3 | `<=` | corpus-confirmed (`dec…OrBefore` names) |
| 4 | `>` | best-guess |
| 5 | `>=` | corpus-confirmed |

| `Join` | Word | Frequency |
|:---:|:---:|---|
| 0 | `AND` | dominant (1495×) |
| 1 | `OR` | 43× |

Codes live in `DECISION_OP_SYMBOLS` / `DECISION_JOIN_SYMBOLS` near the top of `extract_stadium_app.py`. (`op1`/`op2`/`op4` are the un-confirmed best-guesses; if a future corpus contradicts them, only these three change.)

### Control validation & field-behaviour props (Cluster A #1)

Input controls store their validation, help, editability and enum settings in the same `JsonData` bag. These are on the **`KEY_PROP_NAMES` allowlist** (so they flow into both `key_props` stores) and are rendered — validation into `business-rules` `## Tier-A — validation`, the rest inline in the `surfaces` control tree. All are **Tier-A verbatim facts** (`[from design model]`); only the validation *intent* label is a Tier-B `[AI-SUGGESTED]` reading.

- **`Required`** (bool) + **`IsValidRule`** + **`ErrorText`** — the validation triple. `IsValidRule` is `null` for a plain required-field rule, or an **Expression** dict `{FormatString, PlaceholderValues:[{NamedItemID}]}`. The `FormatString` is a JS predicate — a regex `/…/.test({0})` or a `dayjs(...)` date expression — using **.NET composite-format escaping**: literal braces are doubled (`{{8,16}}` = `{8,16}`) and `{0}` is the placeholder for the target control's own value. Un-escape the doubled braces for display; the target field is the owning control (identity implicit). `ErrorText` is the verbatim user-facing message and can be empty — emit the rule without a message, never `""`. The intent classifier (`_rule_intent`) labels email / numeric / date / length / pattern (advisory).
- **`Hint` / `ToolTip`** — inline help text (verbatim; also a §9 terminology signal where a label ≠ field name).
- **`ReadOnly` / `IsPassword`** — editability + password-masking facts.
- **`VisibleLines` / `Rows`** — a value > 1 signals a multi-line text area.
- **`Options` vs `OptionsField`** — a non-empty inline **`Options`** list (`[{text,value}…]`) is a **static enum** (rendered verbatim); an **`OptionsField`** GuidReference with an empty `Options` is a **runtime binding** (rendered "dynamic choices (bound)"; the values are not statically resolvable — never fabricated). The two co-exist on the same control.
- **`AllowExport` / `DisplaySearchBar` / `HasSelectableData`** — DataGrid affordance flags. **`AllowedExtensions` / `FilesField`** — file-upload constraints (sparse). **`AllowMultiple`** is unused across the corpus (0/5029) and is deliberately **not** whitelisted.

### DataGrid `Columns` resolution + `ColumnType` enum (Cluster A #2)

A `DataGrid` control's **`Columns`** prop is an **ordered GUID list** (whitelisted, previously kept unresolved). Each GUID resolves — via the same `norm_guid` + registry walk used for `Actions`/`Conditions`/`ExecutionPaths` — to a **`UniqueItemExpando` of type `…DataGrid.Column`**. Resolution runs at **model-build time** in `build_tree` (the registry is not in the returned `model`), is stored as `node["columns"]`, and is rendered as one ordered line under the grid in `surfaces`. Verified **100 % resolution** over 323 grids / 3262 columns across the 20-app corpus.

A Column's `props` carry: **`HeaderText`** (human label, 100 %), **`Name`** (camelCase identifier, 100 %), **`Visible`** (100 %; ~40 % are `false` — hidden ID/FK columns), **`ColumnType`** (int enum below), `CellDisplay` / `Alignment` (usually 0), and — on action columns only (~12 %) — a **`ClickEventHandlerScript`**. **There is NO per-column `DataField`** (0/3262): a column's data binding is order-based at the grid level, so #2 emits `HeaderText`/`Name`/visibility/kind as Tier-A facts and does **not** mint a data-model field binding (that join is deferred to the rendered-view axis, #8).

| `ColumnType` | Kind | Frequency (20-app corpus) |
|:---:|:---:|---|
| 0 | `data` | 2933 |
| 1 | `action` | 329 |

Only `{0,1}` occur across all 20 apps; any other int degrades to `type<N>` (`_decode_column_type`), never a guess.

### App settings — the `Setting` table (Cluster B #4-B)

The `sqlitedata` also carries a **`Setting`** table (cols `ID, ParentID, Name, Value, IsSecret`) holding app-level configuration the deployed `appsettings.json` does not: internal API URLs, a `DepartmentID` data-scope scalar, filesystem paths, and DB-connection / API-key rows. It is **sparse** (0–3 rows per app; empty or absent on many) and **secret-dominated**, so it is surfaced narrowly into the `data-sources` asset (`## Tier-A — app settings / integration`, locator `[from design model: Setting]`) as **handoff-only §1.7 integration signals**, never as §7 data-model fields.

- **`IsSecret` is UNRELIABLE — do not gate on it.** Across the corpus it is uniformly `0` even on rows whose `Value` is a password or API key. Secret detection is therefore **Name-pattern-driven** (`_redact_setting`: a `Name` matching `key|secret|password|pwd|token|apikey` collapses to a redacted **presence** signal — the value is never emitted). The flag is recorded in `model.json > settings[].is_secret_flag` for forensics only.
- **Redaction happens at read time**, so no secret value reaches `model.json`. Connection-string values reuse `sanitize_conn` (host/db kept, password redacted) and are deduped against the connector inventory; URL values keep scheme+host+path and drop the query/fragment; paths and scalars are PII-scrubbed (`_redact_pii`).
- **Formatting/timeout keys are NOT read.** The `appsettings.json Config.*` block (`DateFormat`, `SessionStateTimeout`, `SmtpDeliveryMethod`, …) was probed to be **byte-identical Stadium defaults across all apps** (zero per-app signal) and session-vars/timeout/auth are already extracted elsewhere — so Cluster B deliberately surfaces none of it (see `plans/stadium-extraction-enrichment/02-cluster-b-config-and-detection.md`).

## AVOID — the noise

- **`JsonData` property bags / `all_props`.** Every control/action node carries a `JsonData` blob of `{Name, ValueType, Value}` property items. The **requirement-bearing key props** — labels, validation (`IsValidRule`/`ErrorText`/`Required`), help (`Hint`/`ToolTip`), editability (`ReadOnly`/`IsPassword`), enums (`Options`), and DataGrid `Columns` — are on the `KEY_PROP_NAMES` allowlist and surfaced (see *Control validation & field-behaviour props* and *DataGrid `Columns` resolution* above). The **rest** of the bag is huge and almost entirely redundant with the deployed source. The forensic `model.json` keeps the full `all_props` for completeness — do not load it into the requirements flow.
- **`CustomType`** — **not** empty in web-service apps: it is the **name dictionary** a WebService Body/ResponseType `GuidReference` resolves against (dozens–hundreds per API app). Its own `JsonData.Fields` GUIDs do **not** resolve via table joins, so read a type's *fields* from the function-bound struct (above), not from the CustomType node. (In SQL-only apps it is frequently empty — check.)
- **`StructDataType` has no `Name` column.** You still cannot read a struct's name directly, but you no longer must guess only from SQL: a struct is named transitively via **the function that binds it** — its parent `Parameter`/`DataResult` under a `ConnectorFunction` whose Body/Response `GuidReference → CustomType.Name`. Field-set-to-SQL matching remains a fallback. Structs are numerous anonymous binding instances (parented by Field/ListDataType/DataResult/Parameter) — the extractor anchors entities on **functions**, not on the struct table.

## Net

Read the `.sapz` for the **clean typed data dictionary + unmangled names**; get **entity names + CRUD** from **three reconciled sources** — SQL tables/views, stored-proc names, and web-service CustomType refs (`reconcile_entities`, union by normalized name); get **field types** by precedence design-model `SimpleDataType` > SQL/proc `DbType` > web-service > omit-if-`Object`; get the **behavioural model** (branch-structured scripts + guard conditions + notification/state signals) from the script/action model above, resolved via `norm_guid`; get **security** from `administration.db`; get **modules + custom CSS** from the deployed `ClientApp`/`wwwroot`. No single source has everything — the extractor fuses them, which is why it reads the app folder, not just the `.sapz`.
