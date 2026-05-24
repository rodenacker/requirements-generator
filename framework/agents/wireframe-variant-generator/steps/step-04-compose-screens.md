---
name: step-04-compose-screens
description: 'Loop over every S-NN row. Compose per-screen HTML by token-substituting template-screen.html; embed data-src attributes; record bindings into the manifest accumulator; write and verify each screen file.'
---

# Step 4: Compose screens

Initialise the manifest accumulator: `manifest.screens = {}` (an empty object that step 5 will serialise into `manifest.json > screens`).

For each screen `S` in `screens` (the in-memory inventory from step 2.1), execute sub-steps 4.1–4.8 in order. Order is fixed (S-01, S-02, …, S-NN) so that the cross-screen prev/next nav is deterministic.

## 4.1 Selectively read pattern files

Read the primary pattern's catalogue file:

```
Read tool: framework/assets/pattern-catalogue/<S.primary_category>/<S.primary_pattern>.md
```

Capture the pattern's `variants:` block, `required-slots`, `optional-slots`, `states`, `composition-rules`, `token-roles-consumed`, `accessibility`. Confirm `S.primary_pattern_variant` is present in `variants:`; if not, fall back to `variants.default` and record a warning into `manifest.screens[S.screen_id].notes`.

For each secondary pattern in `S.secondary_patterns`, read its file similarly. Skip T3 stub patterns silently — they have no body to compose.

Confirm composition is legal per the primary pattern's `composition-rules.may-contain` and `must-not-contain`. Illegal composition (e.g. `single-form` containing `table`) is a structural error — drop the offending secondary and record a warning.

## 4.2 Compose the primary pattern HTML

Render the primary pattern's HTML using its catalogue entry's `required-slots` + `optional-slots`, with token-role-consumed classes resolved against `wireframe-ds.css` class names (`wf-form`, `wf-field`, `wf-btn`, `wf-table`, etc.). The pattern variant chosen (`compact`, `comfortable`, `spacious`, `two-column`, etc.) determines per-class density modifiers per `tradeoff-dimensions-registry.md > Section 3`.

Examples:

- `forms/single-form` + `variant: compact` → `<form class="wf-form">` containing `<div class="wf-field">` per field, two columns when density permits, no `help-aside`, submit-on-Enter wiring.
- `collections/table` + `variant: compact` → `<div class="wf-table"><table>…</table></div>` with 6+ visible columns, small row height (inherited from CSS), `bulk-select` checkbox column if density-+2.
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

## 4.4 Embed `data-src` attributes

For every interactive element in the composed HTML (primary + secondary), add a `data-src` attribute naming the requirement IDs it satisfies. Boundaries per the variant character file:

- Forms (`<form>` element) → `data-src="<full sources list>"`.
- Primary actions (`<button class="wf-btn primary">`, `<button type="submit">`) → `data-src="<primary action's source IDs>"`.
- Table columns whose value is a record field → the column header's `<th>` carries `data-src="<the field's source ID>"`.
- Validation regions (`<p class="wf-validation-error">`, `<div class="wf-banner" data-tone="danger">`) → `data-src="<the BR-NN or UI-NN driving the validation>"`.
- Error / empty states (`<div class="wf-empty">`) → `data-src="<the screen's primary source ID>"`.
- Heading (`<h1>`) → `data-src="<screen's full sources list>"` (already in the template).

Every `data-src` ID **must** be present in `S.sources` (the blueprint's source list for this screen). Fabricated IDs are a self-validation failure at step 6 and a structural bug; halt and re-compose.

## 4.5 Compose cross-screen + cross-variant nav

Every cross-screen and cross-variant link carries `target="_blank" rel="noopener"` so a click opens the destination in a new tab — the consultant arranges tabs as side-by-side windows using the browser's native tab-drag, without losing the current screen. The "back to index" link in the page chrome (filled by `{{SET_INDEX_HREF}}` in the template) is the **only** link without `target="_blank"`; it is back-navigation to the scope landing and naturally replaces the current tab.

Cross-screen nav (`{{CROSS_SCREEN_NAV}}`): a `<nav>` block with prev / current / next links derived from the blueprint's flow notation. Example for S-02 of a 5-screen flow:

```html
<a href="screen-01-login.html" target="_blank" rel="noopener">‹ S-01 Login</a>
<strong>S-02 File picker</strong>
<a href="screen-03-validation.html" target="_blank" rel="noopener">S-03 Validation ›</a>
```

For the entry screen (S-01) the prev link is absent; for the terminal screen the next link is absent. Error-loop flows (`S-03 → S-02 on validation failure`) are rendered as an additional `<a>` with a clarifying suffix: `<a href="screen-02-file-picker.html" target="_blank" rel="noopener">↺ on validation failure</a>`.

Cross-variant nav (`{{CROSS_VARIANT_NAV}}`): derived from `variants_path` — the sub-agent does NOT re-read variants.json (it already has own.variant_id from step 2.2), but it knows the variant directory structure. The nav links each other variant's matching screen at the same `S-NN` slot:

```html
<a href="../<VARIANT-B>/screen-02-file-picker.html" target="_blank" rel="noopener">Open in V-B</a>
<button aria-pressed="true">Current: V-A</button>
<a href="../<VARIANT-C>/screen-02-file-picker.html" target="_blank" rel="noopener">Open in V-C</a>
```

The sub-agent enumerates other variant IDs from the variants.json read at step 2.2 (own-entry skip applied) — this is the **only** other-variant data the sub-agent reads, and it is metadata-only (IDs and inferred screen filenames), not content.

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

Token-substitute every slot in `template_screen` from in-memory state:

- `{{DS_PATH}}` → `"wireframe-ds.css"` (always; the per-variant DS is one directory level up from … wait, actually the screen file lives in `<output_dir>/screen-NN.html` and the DS lives in `<output_dir>/wireframe-ds.css` — both at the same depth, so the relative path is exactly `"wireframe-ds.css"` with no directory prefix).
- `{{SCOPE_SLUG}}` → `<scope_slug>`.
- `{{VARIANT_ID}}` → `<variant_id>`.
- `{{SCREEN_ID}}` → `S.screen_id`.
- `{{SCREEN_SLUG}}` → derived screen_slug from 2.6.
- `{{SCREEN_INTENT}}` → `S.intent`.
- `{{SCREEN_SOURCES}}` → comma-separated `S.sources`.
- `{{PERSONA_BINDING}}` → `own.persona_binding`.
- `{{CROSS_SCREEN_NAV}}` → from 4.5.
- `{{CROSS_VARIANT_NAV}}` → from 4.5.
- `{{PRIMARY_PATTERN_HTML}}` → from 4.2 + 4.4 (data-src embedded).
- `{{SECONDARY_PATTERN_HTML}}` → from 4.3 + 4.4.
- `{{POSITION_TAGLINE}}` → from 4.5b (plain-English position labels joined with ` · `).
- `{{STATES_RENDERED}}` → pipe-separated names from `S.states_rendered`.
- `{{COMPARISON_HREF}}` → `"../comparison.html"`.
- `{{SET_INDEX_HREF}}` → `"../index.html"`.

Confirm zero literal `{{...}}` remain (any surviving placeholder is a structural bug; re-render and fix the missing slot).

## 4.7 Write the screen file

Compute the sha256 of the rendered HTML.

```
Write tool: <output_dir>/screen-{NN-zero-padded}-{screen_slug}.html  (contents: rendered HTML)
```

## 4.8 Verify the write and record bindings

Call `framework/skills/verify-artifact-write.md` with:

- `path = <output_dir>/screen-NN-<slug>.html`
- `expected_sha256 = <hash from 4.7>`
- `expected_min_bytes = 512` (a minimal-shape screen with template chrome + one primary pattern is above 512 bytes).

On `pass`, append a record to the manifest accumulator:

```python
manifest.screens[S.screen_id] = {
  "screen_file": "screen-NN-<slug>.html",
  "primary_pattern": S.primary_pattern,
  "primary_pattern_variant": S.primary_pattern_variant,
  "secondary_patterns": S.secondary_patterns,
  "states_rendered": S.states_rendered,
  "data_src_targets": S.sources,
  "notes": "...optional warnings..."
}
```

On `RF-04 trigger`, return `failed` per the registry semantics.

## 4.9 Loop

Advance to the next screen `S`. Repeat 4.1–4.8 until every row in `screens` has been processed.

---

**Next:** Read fully and follow `step-05-write-landing-and-sidecars.md`.
