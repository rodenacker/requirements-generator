# stadium/registry.md

**What this is.** The Stadium-6 knowledge base (KB): a set of **durable, app-independent** reference files describing how a Twenty57 **Stadium 6** web application is structured on disk and what its extracted facts mean. It is read by the Stadium extractor (`framework/tools/extract_stadium_app.py`, via its `--kb` flag — today only `module-catalogue.md`, for module glosses) and by the requirements drafter (to interpret the per-app extracted assets it ingests). These facts hold across every Stadium app and rarely change; they belong here, not in any one app's inputs.

**Distinct from per-app extracted assets.** When a consultant points the extractor at one Stadium app folder, it emits per-app assets (`<stem>.stadium.<category>.md`) into that engagement's `input/` directory. Those describe *one* application and live with the engagement. This KB describes the *platform* and is checked into the framework. `asset-schemas.md` is the bridge — it documents the shape of those per-app assets and how the drafter cites them.

## Files

| File | Purpose |
|---|---|
| `registry.md` | This index. |
| `glossary.md` | Stadium-6 conceptual model + glossary (application-domain vocabulary — **not** the system glossary). Defines Application, Page, Template, Control, Script/Action, Connector, Type/Field, Theme, Module, etc. |
| `admindb-schema.md` | The `administration.db` reference: its 14-table schema (stable across all apps), the RBAC join recipes, and which tables carry security/deploy facts vs are unused. |
| `module-catalogue.md` | Empirical catalogue of `stadium-software/<module>` extensions (slug + capability gloss). **Machine-parsed by the extractor's `--kb` flag** to gloss detected modules. Also documents the detection recipe. |
| `theming-model.md` | Styling/theming reference + the plain / themed / extensively-customized classification recipe (the discriminating signal is custom EmbeddedFiles CSS, not the stock theme folders). |
| `template-model.md` | Templates as master pages — shared chrome (logo, nav, header/footer, busy indicator) extracted once, not per page; the `[PageUse(...)]` member-page attribute. |
| `sapz-spec.md` | What to take from (and avoid in) the `.sapz` `sqlitedata` design model — the clean central data model vs the verbose `JsonData` prop bags; **and the script/action behavioural model** (Script→ExecutionPath→Actions; Decision→IfPath→{Conditions,Actions}), the GUID `bytes_le` normalization rule, and the Operator/Join enum table. |
| `rendered-clientapp-spec.md` | The **rendered `ClientApp/src`** axis (Cluster C) — the generated Vue front-end Stadium builds from the `.sapz`: the `page-routes.js` titled-page list (#7), the `types.js` FE↔API class/field/variant/nested grammar + envelope denylist (#6), and the `views/*.vue` `columnDefinitions` wrapper grammar + `_46`/`_95` endpoint encoding + deployed-vs-design divergence rendering (#8). A complement to the `.sapz` (reconciled against it; `.sapz` wins on conflict). |
| `asset-schemas.md` | Canonical schema-doc for the per-app extracted assets (Tier-1 deterministic + Tier-2 LLM-inferred), the Tier-A/Tier-B citation discipline, and the asset → `requirements.md`-section / downstream-pipeline mapping table. |
