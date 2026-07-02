# stadium/glossary.md — Stadium-6 conceptual model & glossary

> **Scope: application-domain vocabulary, not system vocabulary.** This glossary defines the concepts of the *Twenty57 Stadium 6 platform* — the thing being reverse-engineered. It must **NOT** be merged into the system glossary at `framework/assets/glossary.md` (which defines *this requirements-generator's* own terms: surface, screen, blueprint, posture, etc.). When a Stadium term and a system term collide (e.g. "Page" the Stadium artefact vs "surface" the system concept), keep them separate; the extractor and drafter translate Stadium *Pages* into system *surfaces*, they are not the same noun.
>
> **Source:** the Stadium documentation site <https://docs.stadium.software/6/>. Most facts below are also directly observable in the extracted design model.

## Designer vs runtime (read this first)

A Stadium app exists in two forms, and the extractor reads both:

- **Design-time** — the **Stadium Designer** (a desktop authoring tool) publishes a **`.sapz`** deployment package: a ZIP wrapping a file named `sqlitedata`, which is a **SQLite database** holding the Designer's clean, normalized design model (pages, controls, scripts, connectors, the data dictionary). This is the authoritative model. See `sapz-spec.md`.
- **Runtime** — the **deployed app** is a generated **ASP.NET (.NET) backend + Vue 2 frontend** build sitting in the app folder (`ClientApp/`, `wwwroot/`, a `.csproj`, `appsettings.json`, `administration.db`). The same design model is **transpiled** into readable `.vue` / `.cs` source. The deployed source is therefore a *superset* of the `.sapz` model for requirements purposes (it carries the generated SQL, the security DB, the custom JS modules, the CSS) — which is why the extractor reads the app folder, not just the `.sapz`.

One consequence: deployed source **mangles** design-time identifiers with an ASCII encoding (`_95` = `_`, `_46` = `.`), whereas the `.sapz` model keeps clean names. Prefer the design-model name when both are available.

---

## Glossary

**Application** — the top-level unit: one deployed Stadium web app. Carries a `Name`, a `DesignerVersion`, a stable `FileGuid` (equal to the app's folder name, and to `administration.db > Applications.FileGuid`), a chosen `Theme`, a session timeout, and an optional app-level custom `StyleSheet`. One `StartPage`.

**Page** — a navigable screen. Has a `Name`, an optional `Title`, an `IsStartPage` flag, an optional **Load** event handler script that runs on open, and a tree of **Controls**. A page renders inside a **Template**. (In system terms a Page maps to a *surface*/*screen* — but keep the nouns distinct; see scope note above.)

**Template** — a master-page layout that wraps page content with shared chrome (logo, navigation menu, header, footer, busy indicator). Most apps have a single `DefaultTemplate`. The generated template controller lists its member pages via a `[PageUse("PageA","PageB",...)]` attribute. See `template-model.md`.

**Control** — a UI element placed in a page/template tree. The observed catalogue:
- *Layout / containers:* `StackLayout` (vertical/horizontal stack), `GridLayout` (CSS-grid container), `Grid` + its `CellGridLayout` / `CellStackLayout` cell wrappers, `Container`, `Panel`.
- *Display:* `Label`, `Image`.
- *Input:* `TextBox`, `DropDown`, `DatePicker`, `CheckBox`.
- *Data / collections:* `DataGrid` (tabular, with selectable/clickable columns and row actions), `Repeater` (repeats a template per item).
- *Action / navigation:* `Button`, `Menu`.
Stadium appends a 32-hex suffix to auto-generated layout control names; the extractor strips it (`friendly_name`).

**Script & Event Handler** — a **Script** is a named, ordered sequence of **Actions**. A script attached to a control event (e.g. `SaveButton.Click`, `MembersDataGrid.Delete.Click`) or a page/template `Load` is an **event handler** (`IsEventHandlerScript`). Scripts are where all app behaviour lives — Stadium has no free-form code, only composed actions.

**Action** — one step in a script. The observed catalogue:
- `ExecuteConnector` — run a **ConnectorFunction** (e.g. a SQL query) and capture its result.
- `SetValue` — assign a value to a control property, session variable, or field (the main data-binding mechanism).
- `NavigateToPage` — go to another **Page** (the source of the navigation graph).
- `DisplayMessageBox` — modal dialog, typically a confirm (e.g. delete confirmation).
- `Notification` — transient toast message.
- `CallScript` — invoke another **Script** (composition / reuse).
- `ForEach` — iterate over a list.
- `Decision` — branch on a condition (if/else).
- `DownloadFile` — stream a file to the browser (export).
- `JavaScript` — run inline custom JS (escape hatch; often calls a **Module** via `this.$globalScripts().<Fn>()`).

**Connector & ConnectorFunction** — a **Connector** is a named external data source; observed types: **Database** (SQL Server, stores a `ConnectionString`), **FileSystem** (reads/writes files on a path), **WebService** (HTTP/REST). A connector owns one or more **ConnectorFunctions** — the *only* way data enters/leaves the app, and the authoritative source of the data model + CRUD operations. Three function flavours, all mined by the extractor (see `sapz-spec.md` + `asset-schemas.md` §(e)):
- **Database / SQL** — carries a **SQL query** (`Text`, incl. views) + typed **Parameters** (`@Name`, `DbType`); entity+columns parsed from the SQL.
- **StoredProcedure** — `Text` is just the proc **name** (`dbo.prc_Stadium_WO_Select`); entity+op come from the name pattern and the **fields are the parameters** (minus `Success`/`Message`/`RaiseExceptions`).
- **WebService** — carries `HttpMethod` + `Path` + `BodyType`/`ResponseType` GuidReferences; the entity **name** resolves through a `CustomType`, its **fields** from the function's bound request/response struct.
Across the corpus WebService functions are as common as SQL, and ~half the apps are API- or proc-backed — SQL alone would miss most of their data model.

**Type / CustomType / StructDataType / Field / SimpleDataType** — the data model:
- **StructDataType** — a composite (record/struct) type: a set of named **Fields**. The Designer uses one per data-bound shape (a query result row, a request/response body, a control's bound object) — so there are many anonymous instances. It has *no* Name column; name it transitively via the **function that binds it** (parent `Parameter`/`DataResult` under a `ConnectorFunction` whose Body/Response `GuidReference → CustomType.Name`), falling back to field-set-to-SQL matching.
- **Field** — a named member of a StructDataType. Carries an **`IsDataField`** flag (nominally: true = a real persisted attribute) that exists only in the design model — but it is **uniformly `0`** across observed deployed models, so it is not a usable discriminator and the extractor does not gate on it. Primitive type comes from the child **SimpleDataType** node.
- **SimpleDataType** — a primitive type instance (`String`, `Int32`, `DateTime`, `Boolean`, `Decimal`, …). Attached to a Field to give it a concrete type; often the weak `System.Object` for API shapes (then the field is kept by name, type omitted).
- **CustomType** — a user-defined named type. **Heavily used in web-service apps** as the **name dictionary** a WebService Body/ResponseType `GuidReference` resolves against (`fullmember`, `payment`, …); its own `JsonData.Fields` GUIDs don't resolve via table joins, so read a type's fields from the function-bound struct, not the CustomType node. (Frequently empty in SQL-only apps.)

**Session Variable** — an app-scoped value persisted for the user's session (e.g. a selected fund ID carried across pages, the logged-in user). Set/read by `SetValue` and connector parameters.

**Validation / Validator** — a rule constraining input (required, format, range) with a message. Modelled as **Validators** in the design model — but frequently absent; required-ness is more often expressed as a control's `Required` property than as a Validator. Treat absence as "validation rules unknown", a stakeholder gap.

**Embedded File** — a static asset (image, CSS, JS, document) bundled into the app, listed in the design model's `EmbeddedFileItem` and present under `wwwroot/Content/EmbeddedFiles/`. Custom CSS here is the key styling signal (see `theming-model.md`).

**Theme** — the app's stock visual theme, one of **11**: `Cobalt`, `Dark`, `DarkRed`, `Default`, `Forest`, `Grey`, `Orange`, `PinkBlue`, `Purple`, `Scarlet`, `Teal`. The chosen theme name is on the Application. The 11 theme *folders* under `ClientApp/src/assets/themes/<Name>/theme.scss` are identical boilerplate across apps — ignore their contents; only the *chosen name* + any *custom* CSS are signal.

**Module** — a `stadium-software/<slug>` open-source extension: a self-contained vanilla-JS (+ CSS) widget that adds behaviour beyond the stock control set (filterable grids, modals, tabs, collapsible panels, loaders, etc.). Wired into an app via `global-scripts.js` and called from `JavaScript` actions as `this.$globalScripts().<Fn>()`. See `module-catalogue.md`. Module presence = required interactions beyond standard CRUD.
