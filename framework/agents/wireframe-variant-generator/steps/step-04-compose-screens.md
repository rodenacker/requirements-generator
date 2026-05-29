---
name: step-04-compose-screens
description: 'Loop over the physical screens derived from the authored surface_plan (step 2.6 render_plan). Render exactly the architect-authored primary_pattern + primary_pattern_variant + modifiers + secondary_patterns per unit — never re-pick from the registry. Fold surfaces render as a host_state sub-tree on their host screen; wizard-split surfaces render one file per sub-step. Embed data-src + data-prop attributes; record the authored plan verbatim into the manifest accumulator; write and verify each physical screen file.'
---

# Step 4: Compose screens

Initialise the manifest accumulator: `manifest.screens = {}` (an empty object that step 5 will serialise into `manifest.json > screens`).

The unit of iteration is the **physical screen render unit** built at step 2.6 from the authored `own.surface_plan` — **not** a blueprint surface row directly. A logical surface (`LS-NN`) realizes into zero physical screens (folds), one (standalone), or N (wizard-split). For each **physical screen render unit** `U` in `render_plan` (the standalone + wizard-split units, in `physical_flow` order so cross-screen prev/next nav is deterministic), execute sub-steps 4.1–4.8 in order. **Fold render units do not iterate here** — they are rendered at 4.3b onto their host surface's physical screen, so they carry no loop iteration and produce no own file.

> **Render the authored plan; do not re-derive.** Every pattern decision for `U` was authored by the architect into the `surface_plan`: `U.primary_pattern`, `U.primary_pattern_variant`, `U.modifiers[]`, and `U.secondary_patterns[]`. This step renders exactly those values. It does **not** consult `tradeoff-dimensions-registry.md` or `pattern-bindings.md` (no longer read — see step 2.4). A plan naming a pattern/variant absent from the catalogue is an architect bug surfaced at author-time; at render time it is a hard `failed`, never a silent substitution.

## 4.1 Selectively read pattern files

Read the primary pattern's catalogue file (look up its category + file path from `_index.md`, captured at step 2.5):

```
Read tool: framework/assets/pattern-catalogue/<category>/<U.primary_pattern>.md
```

Capture the pattern's `variants:` block, `required-slots`, `optional-slots`, `states`, `composition-rules`, `token-roles-consumed`, `accessibility`. Confirm `U.primary_pattern_variant` is present in `variants:`. **If it is not present, this is a `failed` — no silent substitution.** The authored `surface_plan` is the single source of truth; a plan naming an absent variant is an architect bug that author-time catalogue validation should have caught (see `blueprint-architect.md > Self-validation > Author-time catalogue validity`). Returning `failed` with a structured payload surfaces the bug rather than masking it (the old "fall back to `variants.default` and warn" behaviour produced false-positive drift and is removed).

For each secondary pattern in `U.secondary_patterns`, read its file similarly. Skip T3 stub patterns silently — they have no body to compose.

Confirm composition is legal per the primary pattern's `composition-rules.may-contain` and `must-not-contain`. Illegal composition (e.g. `single-form` containing `table`) is a structural error — drop the offending secondary and record a warning into `manifest.screens[U.screen_id].notes`.

## 4.2 Compose the primary pattern HTML

Render the primary pattern's HTML using its catalogue entry's `required-slots` + `optional-slots`, with token-role-consumed classes resolved against `wireframe-ds.css` class names (`wf-form`, `wf-field`, `wf-btn`, `wf-table`, etc.). The authored `U.primary_pattern_variant` (`compact`, `comfortable`, `spacious`, `two-column`, etc.) selects the catalogue variant. **The density/behaviour modifiers come from the authored `U.modifiers[]` — not from a registry lookup.**

Apply `U.modifiers[]` as follows:

- **Density spacing classes** (`wf-table--spacious`, `wf-table--compact`, and their form analogues): add the named class verbatim to the corresponding container. E.g. `U.modifiers` contains `wf-table--compact` → render `<div class="wf-table wf-table--compact">`; `wf-table--spacious` → `<div class="wf-table wf-table--spacious">`. The architect authored exactly one density class per applicable container; do not add a second.
- **Combinable catalogue behaviours** (`selectable`, `editable`, and similar): compose the behaviour into the pattern. `selectable` on a `collections/table` → add the `bulk-select` checkbox column; `editable` → render inline-edit affordances on the cells. Multiple combinable behaviours compose together (e.g. `selectable` + `editable` → a selectable, inline-editable table).
- **Plain-text composition adjustments** (free-text modifier strings, e.g. `keyboard shortcuts`): apply as the catalogue pattern's optional-slot wiring permits; ignore any that the pattern does not support and record a one-line note into `manifest.screens[U.screen_id].notes`.

Examples:

- `forms/single-form` + `variant: compact` + `modifiers: []` → `<form class="wf-form">` containing `<div class="wf-field">` per field, two columns when the variant permits, no `help-aside`, submit-on-Enter wiring.
- `collections/table` + `variant: default` + `modifiers: ["wf-table--compact", "selectable"]` → `<div class="wf-table wf-table--compact"><table>…</table></div>` with 6+ visible columns, small row height, and a `bulk-select` checkbox column (from the `selectable` modifier).
- `auth/login-form` inside `layouts/centered-form` → `<main class="wf-shell"><form class="wf-form">…</form></main>` with email + password fields, OAuth-provider stubs if the screen sources reference OAuth.

The pattern HTML is rendered with **placeholder data**: realistic fixture-style content (fake names, fake IDs, fake totals) that demonstrates the pattern's slots. This is per the prototype invariants (`PI-02 fixtures only`); the wireframe pipeline inherits this without restating.

## 4.3 Compose secondary pattern HTML

For each secondary pattern, render its HTML and decide where it slots:

- `feedback/inline-validation` → inside the primary form, attached to specific fields.
- `feedback/notification-banner` → above the primary section.
- `surfaces/modal-confirmation` → as a sibling `<aside class="wf-modal">` block; rendered in `state: confirming` (the screen visualises the modal open).
- `surfaces/tooltip` → embedded on icon-only controls.
- `feedback/empty-state` → as the primary slot's empty-state visualisation (rendered as one of the `states_rendered`).
- `feedback/notification-toast` → as a fixed-position `<div class="wf-toast">`, rendered when `state: success` or `state: error` is in `states_rendered`.

Each secondary's HTML is appended into the `{{SECONDARY_PATTERN_HTML}}` slot of the screen template — concatenated in semantic order.

## 4.3b Render folded surfaces and wizard-split slices (realization rendering)

This is the load-bearing realization-rendering step. The current physical screen `U` belongs to a logical surface `U.surface_id`. Before moving on, render the realizations that **attach** to this screen:

**Folded surfaces (`inline-drawer` / `inline-expand` / `modal`).** For every **fold render unit** `Fld` in `render_plan` whose `Fld.rendered_on == U.screen_id` (i.e. `Fld` is hosted on this physical screen):

- Compose `Fld`'s `primary_pattern` + `primary_pattern_variant` + `modifiers[]` + `secondary_patterns[]` exactly as for a primary screen (4.1 + 4.2 + 4.3 apply to the fold's pattern too — read the fold's pattern catalogue file, apply the authored variant + modifiers). The fold's authored pattern is typically `surfaces/drawer-detail` (inline-drawer), an expandable-row / detail-panel (inline-expand), or `surfaces/modal-form` / `surfaces/modal-confirmation` (modal).
- Render that composed HTML as a **`host_state` sub-tree** on `U`'s screen — the named `Fld.host_state` (e.g. `drawer-detail-open`, `modal-form-open`, `row-expanded`). The step already renders modal/drawer states for secondary patterns (4.3); a folded surface is rendered the same way, except its content is the **whole folded surface**, not an auxiliary confirmation. Add `Fld.host_state` to the host screen's rendered states (it appears in `U`'s `states_rendered` so the host visualises the open state).
    - `inline-drawer` → a sibling `<aside class="wf-drawer" data-state="drawer-detail-open">…</aside>` slotted into `{{SECONDARY_PATTERN_HTML}}`.
    - `modal` → a sibling `<aside class="wf-modal" data-state="modal-form-open">…</aside>`.
    - `inline-expand` → an expanded `<tr class="wf-row-expanded">` / `<div class="wf-detail-panel">` region within the host collection.
- **CRITICAL — audit granularity survives the fold.** The folded surface keeps its **own** `data-src` and `data-prop` attributes (stamped at 4.4 / 4.4b using `Fld.sources` and `Fld.covers_properties` — *not* the host's). A property rendered inside the drawer/modal sub-tree binds to `Fld`'s closed set, so the fold's audit trail is preserved exactly as if it were a standalone screen. Do **not** let the host's source/property set absorb the fold's — they are validated independently at step 6 (the host screen's union of `data-prop` values must be a subset of `U.covers_properties` ∪ each hosted `Fld.covers_properties`). The fold contributes **no own file**; its entire footprint is this host-screen sub-tree.

**Wizard-split sub-screens.** When `U` is one sub-step of a `wizard-split` surface (`U.realization == "wizard-split"`, `U.sub_step` / `U.of` populated), render **only this sub-step's slice** of the surface — the fields/columns whose property is in `U.covers_properties` (the authored per-sub-screen subset), plus the `navigation/stepper-indicator` secondary pattern showing `step {U.sub_step} of {U.of}`. The union of every sub-screen's `covers_properties` across the wizard equals the surface's full closed property set (the architect guaranteed this at author-time); each individual sub-screen renders only its own slice. Cross-screen nav (4.5) wires the sub-screens sequentially (`screen-NNa → screen-NNb → …`).

No-fold-of-fold is an architect-time guarantee (a fold's `host_surface` always resolves to a surface with a real physical screen in this variant); at render time, if a `Fld.rendered_on` names a `screen_id` that no physical render unit produces, return `failed` (the host did not materialise — an architect bug).

## 4.4 Embed `data-src` and `data-prop` attributes

For every interactive element in the composed HTML (primary + secondary + any hosted fold sub-tree), add a `data-src` attribute naming the requirement IDs it satisfies. Boundaries per the variant character file:

- Forms (`<form>` element) → `data-src="<full sources list>"`.
- Primary actions (`<button class="wf-btn primary">`, `<button type="submit">`) → `data-src="<primary action's source IDs>"`.
- Table columns whose value is a record field → the column header's `<th>` carries `data-src="<the field's source ID>"`.
- Validation regions (`<p class="wf-validation-error">`, `<div class="wf-banner" data-tone="danger">`) → `data-src="<the BR-NN or UI-NN driving the validation>"`.
- Error / empty states (`<div class="wf-empty">`) → `data-src="<the screen's primary source ID>"`.
- Heading (`<h1>`) → `data-src="<screen's full sources list>"` (already in the template).

For elements belonging to the **host surface** (the screen `U`'s own pattern), `data-src` IDs must be present in `U.sources` (the host surface's source list). **For elements inside a hosted fold sub-tree (rendered at 4.3b), the `data-src` IDs must be present in that fold's `Fld.sources` — not the host's.** Each fold keeps its own audit identity. Fabricated IDs (an ID not in the relevant unit's source list) are a self-validation failure at step 6 and a structural bug; halt and re-compose.

### 4.4b `data-prop` — the no-fabricated-property contract

For every **data-bound** element (binding to or rendering an entity-property value), additionally embed a `data-prop` attribute naming the property the element renders. The attribute is **required** on:

- Form inputs (`<input>`, `<select>`, `<textarea>`) inside a `wf-field` that captures or displays an entity-property value.
- Table column headers (`<th>`) whose column renders an entity field.
- Detail-page definition terms (`<dt>`) whose value (`<dd>`) shows an entity field.
- Receipt-style attribute-list spans that name an entity field.
- Status badges / chips whose displayed value is an entity field.

Attribute syntax:

- §7 data-shape property: `data-prop="<Shape>.<Field>"` (e.g. `data-prop="FileLog.CurrentStatus"`, `data-prop="Transaction.AccountNumber"`).
- F-NN-named parameter: `data-prop="F-NN:<ParamName>"` (e.g. `data-prop="F-05:FileSettingId"`).
- Opaque-payload column (per blueprint's `[OPAQUE-PAYLOAD]` annotation): `data-prop="<Shape>.<OpaqueField>[<ColumnName>]"` (e.g. `data-prop="ValidationErrors.JsonArray[RowNumber]"`). The `<ColumnName>` portion must appear verbatim in the cited F-NN's prose.

**The closed-set check.** Every `data-prop` value must be present in the **closed property set of the unit that owns the element**:

- An element belonging to the host surface (`U`'s own pattern, or a wizard-split sub-step's slice) must use a `data-prop` in `U.covers_properties` (the authored per-physical-screen subset captured at step 2.6 from `surface_plan`). For a wizard-split sub-screen this is **only this sub-step's slice**; the union across the wizard's sub-screens is the surface's full closed set.
- **An element inside a hosted fold sub-tree (rendered at 4.3b) must use a `data-prop` in that fold's `Fld.covers_properties` — not the host's.** This is what preserves the folded surface's audit granularity: its drawer/modal sub-tree carries the fold's own properties, validated against the fold's own closed set, exactly as if the surface had its own standalone screen.

A `data-prop` value outside the owning unit's closed set is a **fabrication** — the cardinal sin of this contract. When this happens:

1. **Re-compose** by dropping the fabricated element. If the pattern still validates per its `composition-rules`, write the corrected HTML and continue.
2. **If the pattern's required slots cannot be filled** from the unit's closed set alone, escalate to `failed` at step 6 with a structured payload naming the missing property and the pattern that needed it. Do **not** smuggle the field in with a "best-guess" `data-prop` — the blueprint + authored `surface_plan` are the source of truth, and a missing property means the architect's closed set is too narrow and the consultant must broaden the blueprint via `/wireframe` Overwrite.

**UI-only controls** are **exempt** from the `data-prop` contract:

- Search inputs (`<input type="search">`, `role="search"` containers).
- Sort toggles on column headers (the `<th>` carries `data-prop` for the entity field; the sort affordance itself is exempt).
- Pagination chrome (`<nav>` with prev/next/page-number links).
- Filter chip toolbars.
- Expand/collapse toggles, view-mode toggles.
- Save / Cancel / Discard buttons, primary CTAs, secondary CTAs.
- Progress indicators (`role="progressbar"`, indeterminate spinners).
- Drag-and-drop dropzones (the file-picker `<input type="file">` carries `data-prop` for the FileName property; the dropzone container around it is exempt).
- Breadcrumb chrome, modal close buttons, dismiss-X buttons.
- Help text (`.wf-help`), legends, section headers, page titles.

Self-validation at step 6 distinguishes data-bound elements from UI-only chrome by class + control type; the variant-generator should compose with that boundary in mind and not stamp `data-prop` on chrome elements.

Record the in-memory union of every `data-prop` value used on this physical screen (host-surface elements **plus** every hosted fold sub-tree's elements) into `screen_properties_rendered[<U.screen_id>] = [...]`. Step 5 mirrors this into `manifest.screens[<U.screen_id>].properties_rendered`. (Because a fold's `data-prop` values live physically on the host screen, the host screen's `properties_rendered` is a subset of `U.covers_properties` ∪ each hosted `Fld.covers_properties` — step 6 validates against that union.)

## 4.5 Compose cross-screen + cross-variant nav

Every cross-screen and cross-variant link carries `target="_blank" rel="noopener"` so a click opens the destination in a new tab — the consultant arranges tabs as side-by-side windows using the browser's native tab-drag, without losing the current screen. The "back to index" link in the page chrome (filled by `{{SET_INDEX_HREF}}` in the template) is the **only** link without `target="_blank"`; it is back-navigation to the scope landing and naturally replaces the current tab.

Cross-screen nav (`{{CROSS_SCREEN_NAV}}`): a `<nav>` block with prev / current / next links derived from `own.physical_flow` (the variant's concrete physical screen flow, read at 2.2) — folded surfaces add no standalone node, wizard-split sub-screens are sequential intra-surface steps. Example for S-02 of a 5-screen flow:

```html
<a href="screen-01-login.html" target="_blank" rel="noopener">‹ S-01 Login</a>
<strong>S-02 File picker</strong>
<a href="screen-03-validation.html" target="_blank" rel="noopener">S-03 Validation ›</a>
```

For the entry screen the prev link is absent; for the terminal screen the next link is absent. Error-loop flows (`S-03 → S-02 on validation failure`) are rendered as an additional `<a>` with a clarifying suffix: `<a href="screen-02-file-picker.html" target="_blank" rel="noopener">↺ on validation failure</a>`. A folded surface that appears in `physical_flow` as a drawer/modal hop (e.g. `S-01 ⟳ drawer(LS-03)`) is **not** a cross-screen link (it has no own file) — it is the in-page `host_state` rendered at 4.3b.

Cross-variant nav (`{{CROSS_VARIANT_NAV}}`): **keyed by logical surface, not by `S-NN` slot.** The current physical screen `U` belongs to logical surface `U.surface_id`. For every sibling variant, resolve "open this same surface in variant B" by reading **B's realization of `U.surface_id`** from B's `surface_plan` (metadata only — realization + the physical_screens filenames + host). The resolution rules:

- B realizes the surface **`standalone-screen`** → link B's single screen file for that surface: `../<VARIANT-B>/<B's screen_file>`.
- B realizes it **`wizard-split`** → link B's **first** sub-screen and append a hint: `../<VARIANT-B>/<first sub-screen>` with text suffix `(N-step wizard)`.
- B realizes it **`inline-drawer` / `inline-expand` / `modal`** → link B's **host** physical screen (the surface has no own file in B) and append the hint `(shown inline)`: `../<VARIANT-B>/<B's host screen_file for the surface's host>`.

```html
<a href="../<VARIANT-B>/screen-02-file-picker.html" target="_blank" rel="noopener">Open in V-B</a>
<button aria-pressed="true">Current: V-A</button>
<a href="../<VARIANT-C>/screen-01-file-log-list.html" target="_blank" rel="noopener">Open in V-C (shown inline)</a>
```

To resolve these links, the sub-agent reads **each sibling variant's `surface_plan` realization map** from the variants.json read at step 2.2 — specifically each sibling's per-surface `realization`, `physical_screens[].screen_file`, and host fields. This is the **only** other-variant data the sub-agent reads, and it is metadata-only (realization + inferred screen filenames + host pointers), not screen content. A surface that B folds and that has the same surface folded onto a host with no matching screen is impossible by the architect's no-fold-of-fold guarantee; if B's `surface_plan` cannot resolve to any file for the surface, render the label as plain text `(not a standalone screen in V-B)` rather than a dead link.

## 4.5b Compose `{{POSITION_TAGLINE}}` (plain-English)

The chrome header surfaces a plain-English summary of the variant's non-neutral positions, used to substitute the template's `{{POSITION_TAGLINE}}` slot.

Read `framework/assets/wireframes/position-vocabulary.md` once at step 2 (already in memory by step 4). For each dimension in `own.dimension_positions`, look up the **short label** for the dimension's position. **Omit dimensions where the position is `0`** (neutral) — neutral positions add no signal to the tagline. Join the remaining short labels with ` · ` (space-bullet-space) in canonical dimension order (`speed-accuracy`, `power-simplicity`, `density-focus`, `control-automation`, `flexibility-consistency`).

Examples:

- `density-focus: +2, speed-accuracy: +1, others: 0` → `"Speed-leaning · Maximally dense"`.
- `density-focus: -1, speed-accuracy: -1, others: 0` → `"Accuracy-leaning · Spacious"`.
- All positions `0` → empty string (the template renders the chrome line with an empty tagline; downstream check at step 6 flags this as an authoring bug since at least one position should be non-neutral for a meaningful variant).

**No-jargon enforcement.** The composed string MUST NOT contain:

- Dimension notation: `D1`, `D2`, …, `D6`, `D1+`, `D1-`, `+1`, `-1`, `+2`, `-2`, `density-focus`, `speed-accuracy`, etc.
- Pattern-catalogue IDs: `table.compact`, `single-form.compact`, etc.
- General-rule references: `GR-01`, …, `GR-NN`.
- Bracketed annotations: `[STANDARD-RULE: …]`, `[DRIFT: …]`, `[AI-SUGGESTED: …]`.

The whole point of the tagline is plain-English skimmability. If a generated tagline contains any banned substring, re-compose by re-reading the short labels from position-vocabulary.md (the labels are pre-vetted to be plain-English; the violation will be in a hand-crafted addition by the sub-agent).

## 4.6 Fill the template slots

Token-substitute every slot in `template_screen` from in-memory state (all references are to the current physical render unit `U`):

- `{{DS_PATH}}` → `"wireframe-ds.css"` (always; the screen file lives in `<output_dir>/screen-NN.html` and the DS lives in `<output_dir>/wireframe-ds.css` — both at the same depth, so the relative path is exactly `"wireframe-ds.css"` with no directory prefix).
- `{{SCOPE_SLUG}}` → `<scope_slug>`.
- `{{VARIANT_ID}}` → `<variant_id>`.
- `{{SCREEN_ID}}` → `U.screen_id`.
- `{{SCREEN_SLUG}}` → derived `screen_slug` from 2.6.
- `{{SCREEN_INTENT}}` → the intent of `U.surface_id` (for a wizard-split sub-screen, suffix the step, e.g. `Upload file (step 1 of 3)`).
- `{{SCREEN_SOURCES}}` → comma-separated `U.sources` (the host surface's sources for this screen).
- `{{PERSONA_BINDING}}` → `own.persona_binding`.
- `{{CROSS_SCREEN_NAV}}` → from 4.5.
- `{{CROSS_VARIANT_NAV}}` → from 4.5.
- `{{PRIMARY_PATTERN_HTML}}` → from 4.2 + 4.4 (data-src embedded).
- `{{SECONDARY_PATTERN_HTML}}` → from 4.3 + 4.3b + 4.4 (secondary patterns **and** any hosted fold sub-trees, each carrying its own fold `data-src`/`data-prop`).
- `{{POSITION_TAGLINE}}` → from 4.5b (plain-English position labels joined with ` · `).
- `{{STATES_RENDERED}}` → pipe-separated names from `U.states_rendered` (including each hosted fold's `host_state`, added at 4.3b).
- `{{TRADE_OFF_MATRIX_HREF}}` → `"../index.html#trade-off-matrix"` (deep-links to §4 of the scope index; the standalone `comparison.html` is no longer authored).
- `{{SET_INDEX_HREF}}` → `"../index.html"`.

Confirm zero literal `{{...}}` remain (any surviving placeholder is a structural bug; re-render and fix the missing slot).

## 4.7 Write the physical screen file

Compute the sha256 of the rendered HTML. Use `U.screen_file` **verbatim** (authored by the architect into `surface_plan`):

- `standalone-screen` → `screen-NN-<slug>.html` (baseline reproduces the pre-realization filename exactly).
- `wizard-split` → `screen-NNa-<slug>.html`, `screen-NNb-<slug>.html`, … (one per sub-step).
- folds (`inline-drawer`/`inline-expand`/`modal`) → **NO file** (rendered onto the host at 4.3b). They do not reach this sub-step.

```
Write tool: <output_dir>/<U.screen_file>  (contents: rendered HTML)
```

**Ordinal gaps are EXPECTED, not errors.** A logical surface realized as a fold leaves no `screen-NN-*.html` file, so the screen-NN ordinals across a variant's directory can be non-contiguous (e.g. `screen-01`, `screen-02`, `screen-04` with `LS-03` folded into `S-01`). This is correct and must not trip a "missing screen" check at step 6.

## 4.8 Verify the write and record bindings

Call `framework/skills/verify-artifact-write.md` with:

- `path = <output_dir>/<U.screen_file>`
- `expected_sha256 = <hash from 4.7>`
- `expected_min_bytes = 512` (a minimal-shape screen with template chrome + one primary pattern is above 512 bytes).

On `pass`, append a record to the manifest accumulator. **The record is copied VERBATIM from the authored render unit (which mirrors `surface_plan`) — the generator records what it rendered, and it rendered exactly what was authored, so `manifest == plan`:**

```python
manifest.screens[U.screen_id] = {
  "screen_file": U.screen_file,
  "surface_id": U.surface_id,                       # the logical surface this physical screen realizes
  "realization": U.realization,                     # standalone-screen | wizard-split
  "primary_pattern": U.primary_pattern,             # verbatim from surface_plan
  "primary_pattern_variant": U.primary_pattern_variant,  # verbatim from surface_plan
  "modifiers": U.modifiers,                          # verbatim from surface_plan (density classes + combinable behaviours)
  "secondary_patterns": U.secondary_patterns,        # verbatim from surface_plan
  "states_rendered": U.states_rendered,              # incl. any hosted fold host_state added at 4.3b
  "data_src_targets": U.sources,
  "notes": "...optional warnings..."
}
```

For every **fold** hosted on this screen, also append a manifest record keyed by the fold's surface (so the comparator can align folds by logical surface and drift-check their patterns/modifiers):

```python
manifest.screens[Fld.surface_id] = {
  "screen_file": None,                               # a fold has no own file
  "surface_id": Fld.surface_id,
  "realization": Fld.realization,                    # inline-drawer | inline-expand | modal
  "host_surface": Fld.host_surface,
  "rendered_on": Fld.rendered_on,                    # the host physical screen_id
  "host_state": Fld.host_state,
  "primary_pattern": Fld.primary_pattern,            # verbatim from surface_plan
  "primary_pattern_variant": Fld.primary_pattern_variant,
  "modifiers": Fld.modifiers,
  "secondary_patterns": Fld.secondary_patterns,
  "states_rendered": Fld.states_rendered,
  "data_src_targets": Fld.sources,
  "notes": "...optional warnings..."
}
```

(Key folds by `Fld.surface_id` — `LS-NN` — since they have no `screen_id`. Standalone/wizard physical screens key by `U.screen_id` — `S-NN`/`S-NNa`. The comparator aligns by `surface_id` regardless.)

On `RF-04 trigger`, return `failed` per the registry semantics.

## 4.9 Loop

Advance to the next physical render unit `U`. Repeat 4.1–4.8 until every standalone + wizard-split unit in `render_plan` has been processed (folds were rendered at 4.3b onto their hosts and recorded above; they are not iterated here). After the loop, confirm every fold render unit's manifest record was appended (each fold's host screen was rendered and the fold's record exists).

---

**Next:** Read fully and follow `step-05-write-landing-and-sidecars.md`.
