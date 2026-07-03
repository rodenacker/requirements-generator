# stadium/module-catalogue.md — `stadium-software` module catalogue

Stadium **Modules** are open-source `github.com/stadium-software/<slug>` extensions: self-contained vanilla-JS (+ optional CSS) widgets that add behaviour the stock control set does not have. They are the strongest signal of **required interactions beyond standard CRUD** — if an app pulls in `filter-grid`, "the user can filter the grid by column" is a binding requirement, not a nice-to-have.

> **This file is machine-parsed.** The extractor (`read_modules()`, via the `--kb` flag) reads the table below to gloss each detected module. It matches lines of the shape `| <slug> | <gloss> | …` — the **first** column is the module slug (the `<x>` in `github.com/stadium-software/<x>`), the **second** is the one-line capability gloss. Keep that contract: slug first, gloss second, slug optionally back-ticked. Header/separator rows (`Module`, `---`) are skipped by the parser.

## Detection recipe

A module is present in an app when any of these fire:

1. **`global-scripts.js` comment URL** — `ClientApp/src/global-scripts.js` contains a `// https://github.com/stadium-software/<slug>` reference (the module's install snippet leaves its source URL as a comment). This is the primary signal the extractor uses.
2. **EmbeddedFiles CSS** — `wwwroot/Content/EmbeddedFiles/CSS/` contains the module's stylesheet(s), e.g. `<name>.css` + `<name>-variables.css`. Some modules are CSS-only (no JS comment URL) and are detectable *only* this way — notably `theming-kit` (`theming-variables.css`) and `css-utilities`.
3. **Call sites** — `this.$globalScripts().<Fn>()` invocations in `JavaScript` actions / `global-scripts.js` name the module's exported functions (e.g. `ConstructSearchPhrase`, `ParseColumnHeading`, `Icons`, `ValidateComponentData`).

### Which signals the extractor implements (Cluster B #5)

All three signals now fire, and each detected module carries a **`detection_source`** tag (`comment-URL` / `function-name` / `CSS footprint`) in the `modules` asset:

- **Comment-URL stays PRIMARY.** Corpus probe: 53 URL hits vs 42 function hits (62% overlap); most 0-detect apps are genuine stubs. Function-name + CSS-footprint are strictly **complementary** — they recover URL-stripped / CSS-only modules (e.g. one corpus app, `FormsIntergration`, has *no* comment URLs yet clearly uses `datagrid-inline-row-edit` + `dynamic-datagrid` + `filter-grid`). On conflict, `url` wins, then `fn`, then `css`.
- **Function-name is a curated POSITIVE whitelist**, not an inventory: the extractor looks only for the known module function names below (`FN_MODULE_MAP` in `extract_stadium_app.py`), matched in a definition/property/call context so debug-log noise cannot false-positive. No strip pre-pass is needed (probe-confirmed the names survive the noise). Because it is a positive whitelist, there is no false-positive class; the `FN_EXCLUDE` set (framework/validation helpers such as `AddTextBoxComponentValidation`, `AreInputsValid`, `EventHandler`) is kept only to guard a future inventory-based approach.
- **CSS-footprint** maps distinctive `EmbeddedFiles/CSS` filename stems → slug (`CSS_MODULE_MAP`); ambiguous stems (`utils.css`) and pure-theming stems (`theming-variables.css` → `design-signals`) are deliberately omitted.
- **Module-driven behaviours (presence-only).** `WorkflowSteps` → *multi-step workflow* and `RoleSpecificStartPages`/`RolePages` → *role → landing-page navigation policy* are surfaced under a `## Tier-A — module-driven behaviours` block. The runtime step list / role→page map are function *arguments* (out of scope — behaviour axis). `RoleSpecificStartPages` is a pattern, not a catalogued github module, so it is surfaced **only** as a behaviour, never as a detected module.

Authoritative maps live in `extract_stadium_app.py`; the catalogue table below is the human-facing mirror (its "Detection signal" column names the same function/CSS signals).

## Catalogue

Slugs below were discovered empirically by grepping `global-scripts.js` across all apps in `C:\Stadium 6 Web Apps\*\` and cross-referencing the EmbeddedFiles CSS footprint. The trailing count in the source grep is shown only as a popularity hint; the parser ignores any column past the gloss.

| Module | Capability (gloss) | Detection signal |
|---|---|---|
| `filter-grid` | Attribute-based filtering of DataGrid rows by column value | comment URL; `[ftype]`/`[foperator]` attrs; `ConstructSearchPhrase` |
| `conditional-datagrid-styling` | Conditional row/cell styling in a DataGrid driven by data value | comment URL; `ConditionalColumnsStyling` call sites |
| `tabs` | Tabbed container — switch between panels in one surface | comment URL; `tabs.css` / `tabs-variables.css` |
| `workflow-steps` | Stepper / progress-step indicator for multi-step flows | comment URL; `workflow-steps.css` / `workflow-steps-variables.css` |
| `datagrid-inline-row-edit` | Edit DataGrid rows in place (no separate edit page) | comment URL; `datagrid-inline-edit.css` / `-variables.css` |
| `repeater-datagrid-client-side` | Client-side DataGrid rendered from a Repeater, paged/sorted in-browser | comment URL; `stadium-repeater-datagrid.css` |
| `datagrid-advanced-search` | Multi-field / advanced search panel over a DataGrid | comment URL; `datagrid-custom-filters.css` / `-variables.css` |
| `utils-custom-event` | Helper: raise/handle custom DOM events between controls | comment URL; `utils.css` / `utils-variables.css` |
| `utils-clear-upload-file-control` | Helper: reset/clear a file-upload control | comment URL; `utils.css` |
| `page-loader` | Full-page loading indicator / busy spinner during async work | comment URL; `page-loader.css` / `page-loader-variables.css` |
| `full-width-top-bar` | Full-width top app bar / header chrome | comment URL; `top-bar.css` / `top-bar-variables.css` |
| `dynamic-DataGrid` | DataGrid whose columns are built dynamically at runtime | comment URL; `ParseColumnHeading` call sites |
| `datagrid-showhide-columns-programatically` | Show/hide DataGrid columns programmatically | comment URL |
| `checkbox-list-all-options` | Checkbox list with a select-all/none master toggle | comment URL |
| `collapse-controls` | Collapsible / expandable containers | comment URL; `collapsible-control.css` / `collapsible-control-variables.css` |
| `popups` | Modal dialogs / toast popups | comment URL; `popup.css`, `modal.css` / `modal-variables.css` |
| `progress-bar` | Determinate/indeterminate progress bar | `progress-bar.css` / `progress-bar-variables.css` |
| `tooltips` | Hover tooltips on controls | comment URL |
| `show-control-on-hover` | Reveal a control only on hover of another | comment URL |
| `repeater-datagrid` | DataGrid composed from a Repeater (server-side variant) | comment URL |
| `icons` | Icon helper (Font Awesome / glyph injection) | comment URL; `icons.css` / `icons-variables.css`; `Icons` call sites |
| `environment-identifier` | Visual banner identifying the deploy environment (dev/UAT/prod) | comment URL; `environments.css` / `environments-variables.css` |
| `accordion` | Accordion — exclusive expand/collapse sections | comment URL; `accordion.css` / `accordion-variables.css` |
| `button-bar` | Grouped button toolbar | `button-bar.css` / `button-bar-variables.css` |
| `theming-kit` | CSS custom-property theming layer (built-in theming, no JS) | CSS-only: `theming-variables.css` present |
| `css-utilities` | Tailwind-like atomic utility CSS classes | CSS filename / class usage; no JS comment URL |

> The `theming-kit` and `css-utilities` rows are CSS-only modules — they have **no** `global-scripts.js` comment URL, so the extractor's module detector (which keys on JS comment URLs) will not list them. They surface instead through the **styling classification** in `design-signals` (see `theming-model.md`). They are included here so the catalogue is complete and the drafter can recognise their CSS filenames.

## What module presence means for requirements

Each detected module implies a **required interaction** that must be captured (per `CLAUDE.md` §1, "required interactions / behaviour" are *what* — authoritative, citation-bound). A grid app with `filter-grid` + `datagrid-advanced-search` + `datagrid-inline-row-edit` is specifying *filterable, searchable, inline-editable* grids — three binding behaviours, not generic CRUD. Capture each as a behaviour requirement traced to the module's presence (`[from page: …]` / module asset); the *realization* (which control, where the filter chips sit) remains a *how* the system decides. The module's `modules` asset (Tier-A detected list) is the citable source; the "implication" line in that asset is Tier-B / `[AI-SUGGESTED]` and is **not** `[SRC]`-citable.
