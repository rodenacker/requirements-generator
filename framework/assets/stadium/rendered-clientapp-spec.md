# stadium/rendered-clientapp-spec.md — the rendered `ClientApp/src` axis (Cluster C)

**What this is.** The reference for the **generated Vue front-end** (`ClientApp/src`) that Stadium builds from the `.sapz` design model, and the deterministic, requirement-bearing signal the extractor mines from three of its files. `sapz-spec.md` covers the `.sapz` design model; this file covers the *rendered* artifact — a distinct source axis.

**The structural fact that governs everything here.** `ClientApp/src` is **generated from the `.sapz`**, so Cluster C is a **complement, not a replacement**. Every rendered fact is stamped with a `[from rendered …]` locator and **reconciled against the `.sapz`, which wins on type conflict**. The rendered source is also the **last *deployed* render**, whereas the extractor selects the latest `.sapz` package by deploy timestamp — so the two can diverge. That divergence is a feature the extractor surfaces (deployed-vs-design), not a bug it hides.

The three files parsed (all under `ClientApp/src/`), and why each carries signal the `.sapz` lacks or renders weakly:

| File | Signal | `.sapz` gap it closes |
|---|---|---|
| `router/page-routes.js` | the complete, titled page/route list | the `.sapz` `NavigateToPage` walk is only a *floor* (JS-computed nav is opaque) — this is the definitive enumeration |
| `types/types.js` | the FE↔API data shapes (fields + Read/Write/… variants + nested relationships) | for the web-service apps the `.sapz` type reconciliation collapses (e.g. CosmoCrm ~4/247 fields typed) |
| `views/*.vue` | per-grid page→connector-function **endpoints**; a deployed-vs-design column cross-check | the `.sapz` renders the view→function binding weakly |

**Parsing approach (all three).** Regex + **bracket-balancing over bounded declarative regions** (the route array, class bodies, the `columnDefinitions` array) — deliberately **no JS AST** (Python ships none; a new dependency is rejected). This matches the `read_modules` regex-over-JS precedent: the declarative blocks parse clean, so **no debug-log strip pre-pass is needed** (debug noise lives only in handler *bodies*, which are out of scope). Shared helpers in `extract_stadium_app.py`: `_read_client_src` (BOM-stripping safe read; `""` when absent), `_balanced_block` (string-aware `[..]`/`{..}` bounding), `_split_object_literals`, `_peel`, `_obj_value`. Every reader returns an empty result when its file is absent, so pure-SQL apps and bare-`.sapz` inputs no-op.

---

## #7 — `router/page-routes.js` (clean, uniform; all 20 corpus apps carry it)

```js
import Members from '@/views/Members.vue';                 // component → view-file map
const pageRoutes = [
  { path: '/', redirect: '/Members' },                     // redirect entry — no component → SKIP
  { path: '/Members', component: Members, meta: { title: 'Members' } },
  ...
];
export default pageRoutes;
```

- **Reader:** `read_page_routes(app_dir)` → `[{path, title, component}]`. Parses the `const pageRoutes = [ … ]` array only; skips redirect-only entries (no `component`). Some files carry a **UTF-8 BOM** (CosmoCrm) — stripped by `utf-8-sig`.
- **Critical:** `router/` also holds `routes.js` + `index.js` (framework admin/auth/error routes). **Parse `page-routes.js` ONLY** — it is exactly the app payload.
- **Page name** = the component identifier (matches the `.sapz` page name and the `.vue` filename), falling back to the last path segment.
- **Rendered into** `surfaces` (Title + Route + Route-declared columns on the inventory) and `navigation` (a page declared in the router but absent from the `.sapz` nav walk is reclassified **"reachable via a declared client route"** rather than an orphan; the JS-computed-nav caveat narrows to pages absent from *both* signals). **Determinism 5.** Locator: `[from rendered routes]`.
- **Yield (DA#6, 20-app sweep):** 18/20 apps have ≥1 route-declared page the `.sapz` walk missed — a genuine completeness win, not cosmetic.

---

## #6 — `types/types.js` (clean, deterministic; **web-service apps only**)

```js
export class SampleUsersAPI_Types_UserRead {              // <API>_Types_<Entity><Variant>
    Id = undefined;                                        // <Field> = undefined;  (no type, no nullability)
    Email = undefined;
    Roles = undefined;
    _getFieldTypeName(fieldName) {                          // nested/relationship map
        let customTypes = { Roles: '_SampleUsersAPI_Types_UserRead_Roles_Type' };
        return customTypes[fieldName];
    }
}
export class _SampleUsersAPI_Types_UserRead_Roles_Type extends Array {   // Array wrapper
    _getItemTypeName() { return 'SampleUsersAPI_Types_Role'; }           // → element type → UserRead.Roles = Role[]
}
```

- **Reader:** `read_client_types(app_dir)` → `[{api, entity, variant, authority, norm, fields:[{name, authority}], relations:{field: element_entity}}]`.
- **A DOMAIN class carries the `<API>_Types_` prefix.** This is the marker of a genuine web-service contract type. **Bare `Types_*` classes are excluded** — they are stadium-module framework scaffolding (`Types_Filter`, `Types_Column`, `Types_WorkflowStep`, `Types_ConditionalColumn`, `Types_State`, `Types_DataSet`, …) and occasionally app-local config/flag types (e.g. RMB_Onboarding's `Types_ProductsPaymentTypes` — a feature-entitlement bag), neither of which is a FE↔API domain shape.
- **Fields:** `<Name> = undefined;` — deterministic; **no type, no nullability** here. Required-ness comes from Cluster A #1's `.sapz` control props, not from `types.js`.
- **Variants → entity stem + authority.** The trailing variant token is stripped to reach the entity stem (`_rendered_entity_stem`), longest-first. `Basic` binds to its Read (`CustomerBasicRead → Customer`); **`Status` does NOT strip** (`CustomerStatusRead → CustomerStatus`, a distinct sub-resource). Authority: `Read`/`BasicRead`/`List` → **display**; `Write`/`Add`/`Update`/`Put`/`Post` → **editable**; `Convert`/`Cancel`/`Complete`/`Close` → **action**; bare (no variant) → display.
- **Excluded classes (never §7 entities):** `extends Array` wrappers (parsed only for the relationship element type); `*List` collection wrappers (`ReadList`/`WriteList` — a self-collection the item entity already implies); transport/response envelopes (`DefaultResponse`, `GeneralError`, `GeneralResponseId`, `ResponseId`, `ResponseMessage`, `ValidationResult`); `*Validation` result DTOs.
- **Relationships:** `_getFieldTypeName` → `_..._Type extends Array` → `_getItemTypeName()` resolves e.g. `UserRead.Roles → Role[]` (feeds §2.2 cardinality).
- **Coverage:** ~11/20 corpus apps carry `<API>_Types_` domain classes (23–3417 non-empty lines); 5/20 are empty (pure-SQL apps → #6 no-ops); the remaining ~4 carry only bare `Types_*` scaffolding/config → also no-op.
- **Reconciliation.** Fed into `reconcile_entities` as a **new evidence class `rendered-types`** (`_SOURCE_RANK` = 2 — below `sql`/3, above `web-service`/1; the `.sapz` type/spelling still wins on conflict, and since types.js carries no type there is never a *type* clash — rendered fields only ADD to the closed set). Each rendered field carries a `[from rendered types]` locator + a per-field authority (Tier-B). A **variant-consolidation pass** (`_variant_norm`, gated on rendered types being present so pure-SQL apps stay byte-identical) folds the web-service shapes keyed on raw type names (`CustomerRead`, `CustomerWrite`, `BeneficiaryReadList`) onto the clean rendered stem (`Customer`, `Beneficiary`) — this both de-duplicates the rendered↔WS split and cleans the pre-existing sparse-WS-entity sprawl.
- **Rendered into** `data-model` (Tier-A §7 fields with authority + nested relations). **Determinism 5** for names/fields/relations/variant-collapse/envelope-deny; **4** for the display/editable/action authority mapping. Locator: `[from rendered types]`.
- **§7 closed-set growth (the one contract event in Cluster C).** #6 adds Tier-A properties to `data-model`, so the `/wireframe` closed property set expands to include rendered `types.js` fields. This is #6's purpose (web-service apps are otherwise near-untyped); fields are reconciled (not blindly added), provenance-stamped, and the `.sapz` type wins on conflict. #7 and #8 add **no** `data-model` property.

---

## #8 — `views/*.vue` `columnDefinitions` + endpoints (**wrapper grammar; huge files**)

```js
BeneficiaryDataGridColumnDefinitions: [
  { name: errorHandling.invoke(() => ('AccountName')),                                   // field id
    headerText: errorHandling.invoke(() => (typeResolver.toString('Account Name'))),      // HUMAN LABEL
    hasClickEvent: false,                                                                  // plain bool
    visible: errorHandling.invoke(() => (true)),                                           // wrapped bool
    staticText: null, cellAlignment: errorHandling.invoke(() => ('left')) },
  ...
]
```

- **Every value is wrapped** in `errorHandling.invoke(() => (X))`; labels additionally in `typeResolver.toString('X')`; bools sometimes in `typeResolver.toBoolean(X)`. `_peel` unwraps these to the literal (returns `None` on an unrecognised shape → caller falls back to the field name, never fabricates). A naive literal read gets nothing.
- **Endpoints are generated route strings, NOT `$http.post`:** `api/Documents/Pages/<View>/<Control>_46<Event>…Click_46<Connector>_95<Function>` where `_46`=`.` and `_95`=`_`. Decoded, the last dotted segment is `<Connector>_<Function>` (connector/function split on the first `_`; corpus connector names carry no `_`). `_decode_endpoint` → `{control, connector, function, decoded}`.
- **View files are enormous** (CustomerDetailsView.vue = 1.3 MB; LeadsView = 500 KB) — the parser **bounds to each `…ColumnDefinitions: [` block via `_balanced_block`**, never structuring the whole file. (DA#5: the 20-app sweep parses every app, incl. the 1.3 MB views, in ≤2.8 s.)
- **Reader:** `read_view_columns(app_dir)` → `{view: {grids: {grid_var: [{name,label,visible,clickable}]}, endpoints:[…]}}`. Parses only top-level `views/*.vue` (excludes the `administration/`, `authentication/`, `errors/`, `layout/`, `templates/` subdirs and `StartPage.vue`). The capital-`C` `ColumnDefinitions:` pattern naturally excludes the lowercase template binding.
- **Divergence-aware rendering (important).** Cluster A #2 already resolves label / visibility / clickability from the `.sapz` for ~all columns (probe: 213/214 on PaymentsApp), and the `.sapz` column dict already carries the field-binding `name`. So #8's column half **does not restate** those. Instead:
  - The `.sapz` #2 column line is upgraded once to show the **field-name binding** (`` `AccountName` "Account Name" ``) — the wireframe `data-prop` — and to render an unresolved `Expression`-valued header **by name** rather than dumping the raw binding blob.
  - The rendered view is joined onto the `.sapz` columns (by page → grid control name → column name) and surfaces **only divergences** (`⚠ … [from rendered view]`): a resolved `Expression` header, a label/visibility/clickability mismatch, or a rendered-only column. This is the **deployed-vs-design staleness cross-check** — the genuine, non-redundant value of the column half.
- **Endpoints** render as a per-page `### source-UI reference — <Page> (from rendered view)` block (control → connector.function) — §8 existing-tool reference material.
- **Determinism 5** (verbatim labels/flags after peel; mechanical `_46`/`_95` decode). Locator: `[from rendered view]`.
- **Deferred (confirmed present, scoped out):** the `eventId: '<GUID>'` bindings (a join key to `.sapz` events) and `.mapAsync(MapItem => ({…}))` row-mappings. Future hooks for a behaviour-axis view↔event join; not extracted today.

---

## Provenance locators (added to the `asset-schemas.md` legend)

| Locator | Source | Asset |
|---|---|---|
| `[from rendered routes]` | `page-routes.js` | `surfaces` (title/route), `navigation` (route reachability) |
| `[from rendered types]` | `types.js` | `data-model` (§7 fields + authority + relations) |
| `[from rendered view]` | `views/*.vue` | `surfaces` (column divergences + endpoints) |

Asset count is unchanged (**10 Tier-1 + 2 Tier-2**): Cluster C enriches `data-model`, `surfaces` and `navigation` — it adds no new category.
