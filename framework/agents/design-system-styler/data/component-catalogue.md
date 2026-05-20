# Component Catalogue

**Role:** Data file consumed by `framework/agents/design-system-styler/steps/step-06-artifact-generation.md` to populate the **Components** section of `design-system/design-system.html`.

**Why this file exists:** the component visualisation section is the single most-edited piece of the design-system artefact — consultants will routinely tune which components render, what their visuals look like, and which states are shown. Keeping everything component-related in one file means a single edit touches one place.

## How the styler consumes this file

Step-06 reads this file once after reading the HTML template, then:

1. Parses the **Render order** list below — components whose slug is *commented out* (a line beginning with `<!--` inside the list, or a leading `#` before the bullet) are skipped.
2. Concatenates the single **Component CSS** block (one fenced `css` block) into a substitution buffer.
3. For each enabled component family, in render order, extracts the family's two fenced `html` blocks — **Live demo** then **States matrix** — wraps each pair in the standard `<div class="cv-family">` wrapper with the family title + note, and appends them to a specimens buffer.
4. Token-substitutes both buffers: for every reference of the form `{{colours.<token>.hex}}`, `{{typography.<token>.value}}`, or `{{effects.<token>.value}}`, substitutes the actual value from the in-memory token set built in step-05 / step-05b. No other substitution semantics — just literal string replacement.
5. Substitutes the CSS buffer into the template's `{{COMPONENT_STYLES}}` placeholder and the specimens buffer into `{{COMPONENT_SPECIMENS}}`.

**No HTML escaping required.** Token values are hex codes (`#RRGGBB`), CSS lengths (`16px`), font-family stacks (`"Segoe UI", system-ui, sans-serif`), shadow declarations (`0 1px 2px rgba(0,0,0,0.08)`), durations (`200ms`), and easing curves (`cubic-bezier(0.4, 0, 0.2, 1)`). None contain HTML-special characters.

**Determinism:** for a fixed token set, the rendered components section is byte-identical across runs. The styler does not interpret the catalogue prose — it extracts code blocks and substitutes tokens.

## Token reference syntax

Inside the CSS block and the HTML snippets below, any reference of the form `{{<json-path>}}` is replaced with the in-memory token value at that path:

| Reference pattern | Substituted value example |
|---|---|
| `{{colours.<name>.hex}}` | `#3b82f6` |
| `{{typography.<name>.value}}` | `"Segoe UI", system-ui, sans-serif` or `600` or `16px` |
| `{{effects.<name>.value}}` | `0 1px 2px rgba(0,0,0,0.08)` or `200ms` or `cubic-bezier(0.4,0,0.2,1)` |

Token paths used in this catalogue must exist in the JSON shape defined in the template header comment. Adding a reference to a token that isn't in that shape will leave a literal `{{...}}` after substitution and trigger the step-06 self-check halt.

## State-forcing convention

The component CSS pairs every **live-state selector** with a matching **forced-state class**. For example:

```css
.cv-btn-primary:hover,
.cv-btn-primary.cv-force-hover { filter: brightness(0.92); }
```

Live demos use the bare semantic markup (`<button class="cv-btn cv-btn-primary">`) — real `:hover` / `:focus` / `:active` work when the consultant interacts in a browser. State matrices use the forced classes (`.cv-force-hover`, `.cv-force-active`, `.cv-force-focus`, `.cv-force-disabled`) so every state is visible in static screenshots or PDF export.

`disabled` and `:checked` use the genuine HTML attribute / pseudo-class — no force class needed.

---

## Render order

Render the families listed below, in this order. Comment out a line (prefix with `<!--`) to skip that family without deleting it from this file.

1. buttons
2. form-inputs
3. alerts
4. badges
5. cards
6. data-table
7. tabs
8. modal

---

## Component CSS

The styler substitutes the *contents* of this single fenced block (no fences, no surrounding text) into the template's `{{COMPONENT_STYLES}}` placeholder. Tokens are substituted first; the resulting CSS string lands inside the template's existing `<style>` block.

```css
/* === Component visualisation (cv-*) ====================================
   Brand-defining properties (colour, font, shadow, motion) reference
   tokens via {{...}} substitution. Structural properties (padding,
   border-radius, gap, border-width, focus-ring offset) are hardcoded
   neutral constants — they are pattern decisions, not brand decisions.

   Every live :hover / :focus / :active / :disabled / :checked rule is
   paired with a .cv-force-{state} sibling so the static state matrix
   renders the same visuals without user interaction.
   ====================================================================== */

/* Layout */
.cv-family { margin: 24px 0 32px 0; }
.cv-family:not(:last-child) {
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.cv-family > h3 {
  font-family: {{typography.heading_family.value}};
  font-weight: {{typography.heading_weight.value}};
  font-size: 15px;
  margin: 0 0 4px 0;
  color: {{colours.text.hex}};
  text-transform: none;
  letter-spacing: 0;
}
.cv-family > p.cv-note {
  font-size: 11px;
  color: var(--muted);
  margin: 0 0 12px 0;
}

.cv-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  padding: 16px;
  background: {{colours.background.hex}};
  border-radius: 6px;
  margin-bottom: 12px;
}
.cv-row.cv-row-col { flex-direction: column; align-items: stretch; }

.cv-state-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(160px, 100%), 1fr));
  gap: 12px;
  padding: 16px;
  background: {{colours.background.hex}};
  border-radius: 6px;
}
.cv-state-cell {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  padding: 12px;
  background: {{colours.surface.hex}};
  border-radius: 4px;
  border: 1px solid rgba(0,0,0,0.08);
  min-width: 0;
}
.cv-state-cell .cv-input,
.cv-state-cell .cv-textarea,
.cv-state-cell .cv-select {
  width: 100%;
  max-width: 100%;
}
.cv-state-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: {{colours.text_muted.hex}};
}

/* --- Buttons ----------------------------------------------------------- */
.cv-btn {
  display: inline-block;
  padding: 8px 16px;
  border: 1px solid transparent;
  border-radius: 4px;
  font-family: {{typography.body_family.value}};
  font-weight: 600;
  font-size: 13px;
  line-height: 1.4;
  cursor: pointer;
  text-decoration: none;
  user-select: none;
  transition: filter {{effects.transition_base.value}} {{effects.easing_standard.value}},
              background {{effects.transition_base.value}} {{effects.easing_standard.value}},
              box-shadow {{effects.transition_base.value}} {{effects.easing_standard.value}};
}
.cv-btn:focus-visible,
.cv-btn.cv-force-focus {
  outline: 2px solid {{colours.primary.hex}};
  outline-offset: 2px;
}
.cv-btn:disabled,
.cv-btn.cv-force-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}
.cv-btn-primary { background: {{colours.primary.hex}}; color: {{colours.surface.hex}}; }
.cv-btn-primary:hover, .cv-btn-primary.cv-force-hover { filter: brightness(0.92); }
.cv-btn-primary:active, .cv-btn-primary.cv-force-active { filter: brightness(0.82); }
.cv-btn-secondary { background: {{colours.secondary.hex}}; color: {{colours.surface.hex}}; }
.cv-btn-secondary:hover, .cv-btn-secondary.cv-force-hover { filter: brightness(0.92); }
.cv-btn-secondary:active, .cv-btn-secondary.cv-force-active { filter: brightness(0.82); }
.cv-btn-ghost {
  background: transparent;
  color: {{colours.text.hex}};
  border-color: rgba(0,0,0,0.20);
}
.cv-btn-ghost:hover, .cv-btn-ghost.cv-force-hover { background: rgba(0,0,0,0.04); }
.cv-btn-ghost:active, .cv-btn-ghost.cv-force-active { background: rgba(0,0,0,0.08); }
.cv-btn-destructive { background: {{colours.error.hex}}; color: {{colours.surface.hex}}; }
.cv-btn-destructive:hover, .cv-btn-destructive.cv-force-hover { filter: brightness(0.92); }
.cv-btn-destructive:active, .cv-btn-destructive.cv-force-active { filter: brightness(0.82); }

/* --- Form inputs ------------------------------------------------------- */
.cv-field { display: flex; flex-direction: column; gap: 4px; min-width: 220px; }
.cv-field-label {
  font-family: {{typography.body_family.value}};
  font-size: 12px;
  font-weight: 600;
  color: {{colours.text.hex}};
}
.cv-field-hint {
  font-size: 11px;
  color: {{colours.text_muted.hex}};
}
.cv-field-error {
  font-size: 11px;
  color: {{colours.error.hex}};
}
.cv-input, .cv-textarea, .cv-select {
  font-family: {{typography.body_family.value}};
  font-size: 13px;
  padding: 8px 12px;
  border: 1px solid rgba(0,0,0,0.20);
  border-radius: 4px;
  background: {{colours.surface.hex}};
  color: {{colours.text.hex}};
  transition: border-color {{effects.transition_base.value}} {{effects.easing_standard.value}},
              box-shadow {{effects.transition_base.value}} {{effects.easing_standard.value}};
}
.cv-input:focus, .cv-input.cv-force-focus,
.cv-textarea:focus, .cv-textarea.cv-force-focus,
.cv-select:focus, .cv-select.cv-force-focus {
  outline: none;
  border-color: {{colours.primary.hex}};
  box-shadow: 0 0 0 3px rgba(0,0,0,0.04);
}
.cv-input.cv-error, .cv-input.cv-force-error,
.cv-textarea.cv-error, .cv-textarea.cv-force-error {
  border-color: {{colours.error.hex}};
}
.cv-input:disabled, .cv-input.cv-force-disabled,
.cv-textarea:disabled, .cv-textarea.cv-force-disabled,
.cv-select:disabled, .cv-select.cv-force-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: {{colours.background.hex}};
}
.cv-textarea { resize: vertical; min-height: 64px; }

/* Checkbox / Radio */
.cv-check-row { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.cv-check-row input[type="checkbox"],
.cv-check-row input[type="radio"] {
  width: 16px; height: 16px;
  accent-color: {{colours.primary.hex}};
  cursor: pointer;
  margin: 0;
}
.cv-check-row span {
  font-family: {{typography.body_family.value}};
  font-size: 13px;
  color: {{colours.text.hex}};
}

/* Toggle switch (CSS-only via :checked) */
.cv-switch { position: relative; display: inline-block; width: 40px; height: 22px; flex: 0 0 auto; }
.cv-switch input { opacity: 0; width: 0; height: 0; position: absolute; }
.cv-switch .cv-switch-track {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.20);
  border-radius: 11px;
  transition: background {{effects.transition_base.value}} {{effects.easing_standard.value}};
}
.cv-switch .cv-switch-track::before {
  content: "";
  position: absolute;
  top: 2px; left: 2px;
  width: 18px; height: 18px;
  background: {{colours.surface.hex}};
  border-radius: 50%;
  transition: transform {{effects.transition_base.value}} {{effects.easing_standard.value}};
  box-shadow: {{effects.shadow_sm.value}};
}
.cv-switch input:checked + .cv-switch-track { background: {{colours.primary.hex}}; }
.cv-switch input:checked + .cv-switch-track::before { transform: translateX(18px); }
.cv-switch input:focus-visible + .cv-switch-track { outline: 2px solid {{colours.primary.hex}}; outline-offset: 2px; }
.cv-switch.cv-force-on .cv-switch-track { background: {{colours.primary.hex}}; }
.cv-switch.cv-force-on .cv-switch-track::before { transform: translateX(18px); }
.cv-switch.cv-force-disabled { opacity: 0.5; pointer-events: none; }

/* --- Alerts ------------------------------------------------------------ */
.cv-alert {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 6px;
  border-left: 4px solid;
  font-family: {{typography.body_family.value}};
  font-size: 13px;
  line-height: 1.5;
  width: 100%;
  max-width: 480px;
}
.cv-alert strong { font-weight: 600; }
.cv-alert-success { background: {{colours.surface.hex}}; border-left-color: {{colours.success.hex}}; color: {{colours.text.hex}}; }
.cv-alert-success strong { color: {{colours.success.hex}}; }
.cv-alert-warning { background: {{colours.surface.hex}}; border-left-color: {{colours.warning.hex}}; color: {{colours.text.hex}}; }
.cv-alert-warning strong { color: {{colours.warning.hex}}; }
.cv-alert-error { background: {{colours.surface.hex}}; border-left-color: {{colours.error.hex}}; color: {{colours.text.hex}}; }
.cv-alert-error strong { color: {{colours.error.hex}}; }
.cv-alert-info { background: {{colours.surface.hex}}; border-left-color: {{colours.info.hex}}; color: {{colours.text.hex}}; }
.cv-alert-info strong { color: {{colours.info.hex}}; }

/* --- Badges ------------------------------------------------------------ */
.cv-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-family: {{typography.body_family.value}};
  font-size: 11px;
  font-weight: 600;
  line-height: 1.6;
  letter-spacing: 0.02em;
}
.cv-badge-success { background: {{colours.success.hex}}; color: {{colours.surface.hex}}; }
.cv-badge-warning { background: {{colours.warning.hex}}; color: {{colours.surface.hex}}; }
.cv-badge-error   { background: {{colours.error.hex}};   color: {{colours.surface.hex}}; }
.cv-badge-info    { background: {{colours.info.hex}};    color: {{colours.surface.hex}}; }
.cv-badge-neutral { background: rgba(0,0,0,0.08); color: {{colours.text.hex}}; }

/* --- Cards ------------------------------------------------------------- */
.cv-card {
  background: {{colours.surface.hex}};
  border-radius: 8px;
  padding: 16px;
  box-shadow: {{effects.shadow_sm.value}};
  transition: box-shadow {{effects.transition_base.value}} {{effects.easing_standard.value}},
              transform {{effects.transition_base.value}} {{effects.easing_standard.value}};
  width: 100%;
  max-width: 280px;
  font-family: {{typography.body_family.value}};
  font-size: 13px;
  color: {{colours.text.hex}};
}
.cv-card:hover, .cv-card.cv-force-hover {
  box-shadow: {{effects.shadow_md.value}};
  transform: translateY(-1px);
}
.cv-card .cv-card-title {
  font-family: {{typography.heading_family.value}};
  font-weight: {{typography.heading_weight.value}};
  font-size: {{typography.size_lg.value}};
  margin: 0 0 6px 0;
  color: {{colours.text.hex}};
}
.cv-card .cv-card-body { color: {{colours.text_muted.hex}}; margin: 0 0 12px 0; }
.cv-card .cv-card-actions { display: flex; gap: 8px; }

/* --- Data table -------------------------------------------------------- */
.cv-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-family: {{typography.body_family.value}};
  font-size: 13px;
  color: {{colours.text.hex}};
  background: {{colours.surface.hex}};
  border-radius: 6px;
  overflow: hidden;
  box-shadow: {{effects.shadow_sm.value}};
}
.cv-table thead th {
  text-align: left;
  padding: 10px 12px;
  background: {{colours.background.hex}};
  color: {{colours.text_muted.hex}};
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid rgba(0,0,0,0.08);
  cursor: pointer;
  transition: background {{effects.transition_base.value}} {{effects.easing_standard.value}};
}
.cv-table thead th:hover, .cv-table thead th.cv-force-hover {
  background: rgba(0,0,0,0.04);
  color: {{colours.text.hex}};
}
.cv-table thead th .cv-sort-arrow { font-size: 9px; margin-left: 4px; color: {{colours.primary.hex}}; }
.cv-table tbody tr { transition: background {{effects.transition_base.value}} {{effects.easing_standard.value}}; }
.cv-table tbody tr:nth-child(even) { background: {{colours.background.hex}}; }
.cv-table tbody tr:hover, .cv-table tbody tr.cv-force-hover { background: rgba(0,0,0,0.04); }
.cv-table tbody tr.cv-row-selected,
.cv-table tbody tr.cv-force-selected {
  background: color-mix(in srgb, {{colours.primary.hex}} 10%, transparent);
  box-shadow: inset 3px 0 0 {{colours.primary.hex}};
}
.cv-table td { padding: 10px 12px; border-bottom: 1px solid rgba(0,0,0,0.04); }
.cv-table tbody tr:last-child td { border-bottom: 0; }

/* --- Tabs (pure CSS via hidden radios + :checked) ---------------------- */
.cv-tabs { width: 100%; max-width: 520px; }
.cv-tabs input[type="radio"] {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}
.cv-tabs .cv-tab-strip {
  display: flex;
  flex-wrap: wrap;
  border-bottom: 1px solid rgba(0,0,0,0.12);
}
.cv-tabs .cv-tab-label {
  padding: 8px 14px;
  font-family: {{typography.body_family.value}};
  font-size: 13px;
  font-weight: 500;
  color: {{colours.text_muted.hex}};
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: color {{effects.transition_base.value}} {{effects.easing_standard.value}},
              border-color {{effects.transition_base.value}} {{effects.easing_standard.value}};
}
.cv-tabs .cv-tab-label:hover { color: {{colours.text.hex}}; }
.cv-tabs .cv-tab-panel {
  display: none;
  padding: 16px;
  font-family: {{typography.body_family.value}};
  font-size: 13px;
  color: {{colours.text.hex}};
  background: {{colours.surface.hex}};
  border-radius: 0 0 6px 6px;
}
.cv-tabs input[id="cv-tab-1"]:checked ~ .cv-tab-strip label[for="cv-tab-1"],
.cv-tabs input[id="cv-tab-2"]:checked ~ .cv-tab-strip label[for="cv-tab-2"],
.cv-tabs input[id="cv-tab-3"]:checked ~ .cv-tab-strip label[for="cv-tab-3"] {
  color: {{colours.primary.hex}};
  border-bottom-color: {{colours.primary.hex}};
  font-weight: 600;
}
.cv-tabs input[id="cv-tab-1"]:checked ~ .cv-tab-panels .cv-tab-panel-1,
.cv-tabs input[id="cv-tab-2"]:checked ~ .cv-tab-panels .cv-tab-panel-2,
.cv-tabs input[id="cv-tab-3"]:checked ~ .cv-tab-panels .cv-tab-panel-3 {
  display: block;
}

/* --- Modal / Dialog (pure CSS via <details>) --------------------------- */
.cv-modal { font-family: {{typography.body_family.value}}; }
.cv-modal summary {
  list-style: none;
  cursor: pointer;
  display: inline-block;
}
.cv-modal summary::-webkit-details-marker { display: none; }
.cv-modal .cv-modal-window {
  margin-top: 12px;
  max-width: 420px;
  background: {{colours.surface.hex}};
  border-radius: 8px;
  padding: 20px;
  box-shadow: {{effects.shadow_lg.value}};
  color: {{colours.text.hex}};
}
.cv-modal .cv-modal-title {
  font-family: {{typography.heading_family.value}};
  font-weight: {{typography.heading_weight.value}};
  font-size: {{typography.size_lg.value}};
  margin: 0 0 8px 0;
}
.cv-modal .cv-modal-body {
  font-size: 13px;
  color: {{colours.text_muted.hex}};
  margin: 0 0 16px 0;
  line-height: 1.5;
}
.cv-modal .cv-modal-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
.cv-modal .cv-modal-window { position: relative; }
.cv-modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: 0;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  color: {{colours.text_muted.hex}};
  padding: 4px 8px;
  border-radius: 3px;
}
.cv-modal-close:hover { color: {{colours.text.hex}}; background: rgba(0,0,0,0.04); }

/* --- Icons (inline SVG, inherits currentColor) ------------------------- */
.cv-icon {
  display: inline-block;
  width: 14px;
  height: 14px;
  vertical-align: -2px;
  flex: 0 0 auto;
}
.cv-btn .cv-icon { margin-right: 6px; }

/* --- Button loading state --------------------------------------------- */
.cv-btn-loading { pointer-events: none; }
.cv-btn-loading::before {
  content: "";
  display: inline-block;
  width: 11px;
  height: 11px;
  border-radius: 50%;
  border: 2px solid currentColor;
  border-right-color: transparent;
  vertical-align: -1px;
  margin-right: 8px;
  animation: cv-spin 720ms linear infinite;
}
@keyframes cv-spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) {
  .cv-btn-loading::before { animation: none; }
}

/* --- Form: required indicator + input-with-icon ----------------------- */
.cv-required {
  color: {{colours.error.hex}};
  margin-left: 2px;
  font-weight: 600;
}
.cv-input-wrap { position: relative; display: block; }
.cv-input-wrap .cv-input { padding-right: 34px; }
.cv-input-wrap .cv-input-icon {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  color: {{colours.text_muted.hex}};
  pointer-events: none;
}
.cv-field-error {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

/* --- Alerts: icon + dismiss ------------------------------------------ */
.cv-alert { align-items: center; }
.cv-alert .cv-alert-icon { flex: 0 0 auto; width: 16px; height: 16px; vertical-align: 0; }
.cv-alert-success .cv-alert-icon { color: {{colours.success.hex}}; }
.cv-alert-warning .cv-alert-icon { color: {{colours.warning.hex}}; }
.cv-alert-error .cv-alert-icon { color: {{colours.error.hex}}; }
.cv-alert-info .cv-alert-icon { color: {{colours.info.hex}}; }
.cv-alert-body { flex: 1 1 auto; min-width: 0; }
.cv-alert-dismiss {
  flex: 0 0 auto;
  background: transparent;
  border: 0;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  color: {{colours.text_muted.hex}};
  padding: 4px 8px;
  border-radius: 3px;
}
.cv-alert-dismiss:hover { color: {{colours.text.hex}}; background: rgba(0,0,0,0.04); }

/* --- Data table: numeric alignment, actions column, pagination, states */
.cv-table th.cv-cell-num,
.cv-table td.cv-cell-num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
.cv-table th.cv-cell-actions,
.cv-table td.cv-cell-actions {
  text-align: right;
  white-space: nowrap;
}
.cv-table .cv-cell-actions .cv-btn {
  padding: 4px 8px;
  font-size: 12px;
  margin-left: 4px;
}
.cv-table th[aria-sort="ascending"],
.cv-table th[aria-sort="descending"] {
  color: {{colours.text.hex}};
}
.cv-table th[aria-sort="ascending"] .cv-sort-arrow,
.cv-table th[aria-sort="descending"] .cv-sort-arrow {
  color: {{colours.primary.hex}};
  opacity: 1;
}
.cv-sort-arrow.cv-sort-inactive {
  color: {{colours.text_muted.hex}};
  opacity: 0.5;
}
.cv-table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px 12px;
  background: {{colours.surface.hex}};
  border: 1px solid rgba(0,0,0,0.08);
  border-top: 0;
  border-radius: 0 0 6px 6px;
  font-family: {{typography.body_family.value}};
  font-size: 12px;
  color: {{colours.text_muted.hex}};
  margin-top: -1px;
}
.cv-pagination {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.cv-pagination .cv-btn {
  padding: 4px 10px;
  font-size: 12px;
}
.cv-pagesize {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.cv-pagesize select {
  font-family: {{typography.body_family.value}};
  font-size: 12px;
  padding: 3px 6px;
  border: 1px solid rgba(0,0,0,0.20);
  border-radius: 3px;
  background: {{colours.surface.hex}};
  color: {{colours.text.hex}};
}
.cv-table-state {
  padding: 24px 12px;
  text-align: center;
  color: {{colours.text_muted.hex}};
  font-size: 12px;
  background: {{colours.surface.hex}};
  border-radius: 6px;
  width: 100%;
}
.cv-table-state strong {
  color: {{colours.text.hex}};
  display: block;
  margin-bottom: 4px;
  font-size: 13px;
}
```

---

## buttons

**Tokens consumed:** `colours.primary`, `colours.secondary`, `colours.error`, `colours.surface`, `colours.text`, `typography.body_family`, `effects.transition_base`, `effects.easing_standard`.

### Live demo

```html
<div class="cv-row">
  <button type="button" class="cv-btn cv-btn-primary">Save changes</button>
  <button type="button" class="cv-btn cv-btn-secondary">Cancel</button>
  <button type="button" class="cv-btn cv-btn-ghost">Archive</button>
  <button type="button" class="cv-btn cv-btn-destructive">
    <svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M6 2h4v1h3v1H3V3h3V2zm-1 3h6l-.5 8.5a1.5 1.5 0 0 1-1.5 1.4H7a1.5 1.5 0 0 1-1.5-1.4L5 5zm2 1v7h1V6H7zm2 0v7h1V6H9z"/></svg>
    Delete record
  </button>
  <button type="button" class="cv-btn cv-btn-primary cv-btn-loading">Saving…</button>
  <button type="button" class="cv-btn cv-btn-primary" disabled>Disabled</button>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Default</span><button type="button" class="cv-btn cv-btn-primary">Save</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Hover</span><button type="button" class="cv-btn cv-btn-primary cv-force-hover">Save</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Active</span><button type="button" class="cv-btn cv-btn-primary cv-force-active">Save</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Focus</span><button type="button" class="cv-btn cv-btn-primary cv-force-focus">Save</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Disabled</span><button type="button" class="cv-btn cv-btn-primary cv-force-disabled">Save</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Loading</span><button type="button" class="cv-btn cv-btn-primary cv-btn-loading">Saving…</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Default</span><button type="button" class="cv-btn cv-btn-secondary">Cancel</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Hover</span><button type="button" class="cv-btn cv-btn-secondary cv-force-hover">Cancel</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Active</span><button type="button" class="cv-btn cv-btn-secondary cv-force-active">Cancel</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Focus</span><button type="button" class="cv-btn cv-btn-secondary cv-force-focus">Cancel</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Disabled</span><button type="button" class="cv-btn cv-btn-secondary cv-force-disabled">Cancel</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Default</span><button type="button" class="cv-btn cv-btn-ghost">Archive</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Hover</span><button type="button" class="cv-btn cv-btn-ghost cv-force-hover">Archive</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Active</span><button type="button" class="cv-btn cv-btn-ghost cv-force-active">Archive</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Focus</span><button type="button" class="cv-btn cv-btn-ghost cv-force-focus">Archive</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Disabled</span><button type="button" class="cv-btn cv-btn-ghost cv-force-disabled">Archive</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Default</span><button type="button" class="cv-btn cv-btn-destructive"><svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M6 2h4v1h3v1H3V3h3V2zm-1 3h6l-.5 8.5a1.5 1.5 0 0 1-1.5 1.4H7a1.5 1.5 0 0 1-1.5-1.4L5 5z"/></svg>Delete</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Hover</span><button type="button" class="cv-btn cv-btn-destructive cv-force-hover"><svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M6 2h4v1h3v1H3V3h3V2zm-1 3h6l-.5 8.5a1.5 1.5 0 0 1-1.5 1.4H7a1.5 1.5 0 0 1-1.5-1.4L5 5z"/></svg>Delete</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Active</span><button type="button" class="cv-btn cv-btn-destructive cv-force-active"><svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M6 2h4v1h3v1H3V3h3V2zm-1 3h6l-.5 8.5a1.5 1.5 0 0 1-1.5 1.4H7a1.5 1.5 0 0 1-1.5-1.4L5 5z"/></svg>Delete</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Focus</span><button type="button" class="cv-btn cv-btn-destructive cv-force-focus"><svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M6 2h4v1h3v1H3V3h3V2zm-1 3h6l-.5 8.5a1.5 1.5 0 0 1-1.5 1.4H7a1.5 1.5 0 0 1-1.5-1.4L5 5z"/></svg>Delete</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Disabled</span><button type="button" class="cv-btn cv-btn-destructive cv-force-disabled"><svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M6 2h4v1h3v1H3V3h3V2zm-1 3h6l-.5 8.5a1.5 1.5 0 0 1-1.5 1.4H7a1.5 1.5 0 0 1-1.5-1.4L5 5z"/></svg>Delete</button></div>
</div>
```

---

## form-inputs

**Tokens consumed:** `colours.primary`, `colours.error`, `colours.surface`, `colours.background`, `colours.text`, `colours.text_muted`, `typography.body_family`, `effects.transition_base`, `effects.easing_standard`, `effects.shadow_sm`.

### Live demo

```html
<div class="cv-row cv-row-col">
  <div class="cv-field">
    <label class="cv-field-label" for="cv-demo-text">Full name<span class="cv-required" aria-hidden="true">*</span></label>
    <input id="cv-demo-text" type="text" class="cv-input" placeholder="Jane Doe" required aria-required="true">
    <span class="cv-field-hint">First and last as on your ID.</span>
  </div>
  <div class="cv-field">
    <label class="cv-field-label" for="cv-demo-email">Work email<span class="cv-required" aria-hidden="true">*</span></label>
    <input id="cv-demo-email" type="email" class="cv-input" placeholder="name@company.com" required aria-required="true">
  </div>
  <div class="cv-field">
    <label class="cv-field-label" for="cv-demo-date">Start date</label>
    <div class="cv-input-wrap">
      <input id="cv-demo-date" type="date" class="cv-input" placeholder="DD/MM/YYYY">
      <svg class="cv-icon cv-input-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M5 1v2H3a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1h-2V1h-1v2H6V1H5zm-2 4h10v8H3V5zm2 2v2h2V7H5zm3 0v2h2V7H8zm3 0v2h2V7h-2z"/></svg>
    </div>
    <span class="cv-field-hint">Calendar picker — typed dates parsed in DD/MM/YYYY.</span>
  </div>
  <div class="cv-field">
    <label class="cv-field-label" for="cv-demo-textarea">Notes</label>
    <textarea id="cv-demo-textarea" class="cv-textarea" placeholder="Optional context…"></textarea>
  </div>
  <div class="cv-field">
    <label class="cv-field-label" for="cv-demo-select">Country</label>
    <select id="cv-demo-select" class="cv-select">
      <option>United Kingdom</option>
      <option>United States</option>
      <option>South Africa</option>
    </select>
  </div>
  <label class="cv-check-row"><input type="checkbox" checked><span>Email me product updates</span></label>
  <label class="cv-check-row"><input type="radio" name="cv-demo-radio" checked><span>Standard delivery</span></label>
  <label class="cv-check-row"><input type="radio" name="cv-demo-radio"><span>Express delivery</span></label>
  <div class="cv-check-row">
    <label class="cv-switch">
      <input type="checkbox" checked>
      <span class="cv-switch-track"></span>
    </label>
    <span>Two-factor authentication</span>
  </div>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Default</span><input type="text" class="cv-input" value="Jane Doe"></div>
  <div class="cv-state-cell"><span class="cv-state-label">Focus</span><input type="text" class="cv-input cv-force-focus" value="Jane Doe"></div>
  <div class="cv-state-cell"><span class="cv-state-label">Error</span>
    <input type="text" class="cv-input cv-force-error" value="" aria-invalid="true" aria-describedby="cv-demo-err">
    <span id="cv-demo-err" class="cv-field-error">
      <svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm-.9 3.5h1.8L8.7 9.5H7.3l-.2-5zM8 11.2a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>
      Full name is required
    </span>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Disabled</span><input type="text" class="cv-input cv-force-disabled" value="Jane Doe" disabled></div>
  <div class="cv-state-cell"><span class="cv-state-label">Date</span>
    <div class="cv-input-wrap"><input type="date" class="cv-input"><svg class="cv-icon cv-input-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M5 1v2H3a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1h-2V1h-1v2H6V1H5zm-2 4h10v8H3V5z"/></svg></div>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Switch off</span><label class="cv-switch"><input type="checkbox"><span class="cv-switch-track"></span></label></div>
  <div class="cv-state-cell"><span class="cv-state-label">Switch on</span><span class="cv-switch cv-force-on"><span class="cv-switch-track"></span></span></div>
  <div class="cv-state-cell"><span class="cv-state-label">Switch disabled</span><span class="cv-switch cv-force-disabled"><span class="cv-switch-track"></span></span></div>
  <div class="cv-state-cell"><span class="cv-state-label">Checkbox</span><label class="cv-check-row"><input type="checkbox" checked><span>Subscribe</span></label></div>
  <div class="cv-state-cell"><span class="cv-state-label">Radio</span><label class="cv-check-row"><input type="radio" checked><span>Choose me</span></label></div>
</div>
```

---

## alerts

**Tokens consumed:** `colours.success`, `colours.warning`, `colours.error`, `colours.info`, `colours.surface`, `colours.text`, `typography.body_family`.

### Live demo

```html
<div class="cv-row cv-row-col">
  <div class="cv-alert cv-alert-success" role="status">
    <svg class="cv-icon cv-alert-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm3.5 4.7-4 5.3a.7.7 0 0 1-1 .1L4 8.5l1-1 1.9 2 3.4-4.5 1.2.7z"/></svg>
    <div class="cv-alert-body"><strong>Saved.</strong> Your changes were saved.</div>
    <button type="button" class="cv-alert-dismiss" aria-label="Dismiss">×</button>
  </div>
  <div class="cv-alert cv-alert-warning" role="status">
    <svg class="cv-icon cv-alert-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M7.1 1.7a1 1 0 0 1 1.8 0l6 11A1 1 0 0 1 14 14H2a1 1 0 0 1-.9-1.3l6-11zM8 5v4h1V5H8zm0 5.5a.8.8 0 1 0 0 1.6.8.8 0 0 0 0-1.6z"/></svg>
    <div class="cv-alert-body"><strong>Heads up.</strong> Your session expires in 5 minutes.</div>
    <button type="button" class="cv-alert-dismiss" aria-label="Dismiss">×</button>
  </div>
  <div class="cv-alert cv-alert-error" role="alert">
    <svg class="cv-icon cv-alert-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zM5.6 5l2.4 2.4L10.4 5l1 1L9 8.4l2.4 2.5-1 1L8 9.4 5.6 12l-1-1 2.4-2.5L4.6 6l1-1z"/></svg>
    <div class="cv-alert-body"><strong>Couldn't reach the server.</strong> Check your connection and try again.</div>
  </div>
  <div class="cv-alert cv-alert-info" role="status">
    <svg class="cv-icon cv-alert-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zM8 4.2a.9.9 0 1 1 0 1.8.9.9 0 0 1 0-1.8zM7.2 7h1.6v4.8h.9V13H6.3v-1.2h.9V8.2h-.9V7h.9z"/></svg>
    <div class="cv-alert-body"><strong>FYI.</strong> A new version of the dashboard is available.</div>
    <button type="button" class="cv-alert-dismiss" aria-label="Dismiss">×</button>
  </div>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Success</span><div class="cv-alert cv-alert-success"><svg class="cv-icon cv-alert-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm3.5 4.7-4 5.3a.7.7 0 0 1-1 .1L4 8.5l1-1 1.9 2 3.4-4.5 1.2.7z"/></svg><div class="cv-alert-body"><strong>Saved.</strong></div></div></div>
  <div class="cv-state-cell"><span class="cv-state-label">Warning</span><div class="cv-alert cv-alert-warning"><svg class="cv-icon cv-alert-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M7.1 1.7a1 1 0 0 1 1.8 0l6 11A1 1 0 0 1 14 14H2a1 1 0 0 1-.9-1.3l6-11zM8 5v4h1V5H8zm0 5.5a.8.8 0 1 0 0 1.6.8.8 0 0 0 0-1.6z"/></svg><div class="cv-alert-body"><strong>Heads up.</strong></div></div></div>
  <div class="cv-state-cell"><span class="cv-state-label">Error</span><div class="cv-alert cv-alert-error"><svg class="cv-icon cv-alert-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zM5.6 5l2.4 2.4L10.4 5l1 1L9 8.4l2.4 2.5-1 1L8 9.4 5.6 12l-1-1 2.4-2.5L4.6 6l1-1z"/></svg><div class="cv-alert-body"><strong>Error.</strong></div></div></div>
  <div class="cv-state-cell"><span class="cv-state-label">Info</span><div class="cv-alert cv-alert-info"><svg class="cv-icon cv-alert-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zM8 4.2a.9.9 0 1 1 0 1.8.9.9 0 0 1 0-1.8zM7.2 7h1.6v4.8h.9V13H6.3v-1.2h.9V8.2h-.9V7h.9z"/></svg><div class="cv-alert-body"><strong>FYI.</strong></div></div></div>
</div>
```

---

## badges

**Tokens consumed:** `colours.success`, `colours.warning`, `colours.error`, `colours.info`, `colours.surface`, `colours.text`, `typography.body_family`.

### Live demo

```html
<div class="cv-row">
  <span class="cv-badge cv-badge-success">Active</span>
  <span class="cv-badge cv-badge-warning">Pending</span>
  <span class="cv-badge cv-badge-error">Failed</span>
  <span class="cv-badge cv-badge-info">Beta</span>
  <span class="cv-badge cv-badge-neutral">Draft</span>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Success</span><span class="cv-badge cv-badge-success">Active</span></div>
  <div class="cv-state-cell"><span class="cv-state-label">Warning</span><span class="cv-badge cv-badge-warning">Pending</span></div>
  <div class="cv-state-cell"><span class="cv-state-label">Error</span><span class="cv-badge cv-badge-error">Failed</span></div>
  <div class="cv-state-cell"><span class="cv-state-label">Info</span><span class="cv-badge cv-badge-info">Beta</span></div>
  <div class="cv-state-cell"><span class="cv-state-label">Neutral</span><span class="cv-badge cv-badge-neutral">Draft</span></div>
</div>
```

---

## cards

**Tokens consumed:** `colours.surface`, `colours.text`, `colours.text_muted`, `typography.heading_family`, `typography.body_family`, `typography.size_lg`, `effects.shadow_sm`, `effects.shadow_md`, `effects.transition_base`, `effects.easing_standard`.

### Live demo

```html
<div class="cv-row">
  <div class="cv-card">
    <div class="cv-card-title">Customer record</div>
    <div class="cv-card-body">Hover this card to see the elevation animate from <code>shadow-sm</code> to <code>shadow-md</code> using the brand's transition timing.</div>
    <div class="cv-card-actions">
      <button type="button" class="cv-btn cv-btn-primary">Open</button>
      <button type="button" class="cv-btn cv-btn-ghost">Archive</button>
    </div>
  </div>
  <div class="cv-card">
    <div class="cv-card-title">Order #4821</div>
    <div class="cv-card-body">Shipped 2 hours ago. Expected delivery tomorrow.</div>
    <div class="cv-card-actions">
      <button type="button" class="cv-btn cv-btn-secondary">Track</button>
    </div>
  </div>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Resting</span>
    <div class="cv-card">
      <div class="cv-card-title">Resting</div>
      <div class="cv-card-body">shadow-sm</div>
    </div>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Hover</span>
    <div class="cv-card cv-force-hover">
      <div class="cv-card-title">Hover</div>
      <div class="cv-card-body">shadow-md</div>
    </div>
  </div>
</div>
```

---

## data-table

**Tokens consumed:** `colours.surface`, `colours.background`, `colours.text`, `colours.text_muted`, `colours.primary`, `typography.body_family`, `effects.shadow_sm`, `effects.transition_base`, `effects.easing_standard`.

### Live demo

```html
<div class="cv-row cv-row-col">
  <table class="cv-table" aria-label="Customer records">
    <thead>
      <tr>
        <th aria-sort="ascending">Name <span class="cv-sort-arrow">▲</span></th>
        <th aria-sort="none">Status <span class="cv-sort-arrow cv-sort-inactive">⇅</span></th>
        <th aria-sort="none">Updated <span class="cv-sort-arrow cv-sort-inactive">⇅</span></th>
        <th aria-sort="none">Owner <span class="cv-sort-arrow cv-sort-inactive">⇅</span></th>
        <th aria-sort="none" class="cv-cell-num">Value <span class="cv-sort-arrow cv-sort-inactive">⇅</span></th>
        <th class="cv-cell-actions">Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Acme Corp.</td>
        <td><span class="cv-badge cv-badge-success">Active</span></td>
        <td>2 hours ago</td>
        <td>J. Doe</td>
        <td class="cv-cell-num">£12,480</td>
        <td class="cv-cell-actions">
          <button type="button" class="cv-btn cv-btn-ghost">View</button>
          <button type="button" class="cv-btn cv-btn-ghost">Edit</button>
        </td>
      </tr>
      <tr class="cv-row-selected">
        <td>Globex Ltd.</td>
        <td><span class="cv-badge cv-badge-warning">Pending</span></td>
        <td>1 day ago</td>
        <td>A. Smith</td>
        <td class="cv-cell-num">£8,120</td>
        <td class="cv-cell-actions">
          <button type="button" class="cv-btn cv-btn-ghost">View</button>
          <button type="button" class="cv-btn cv-btn-ghost">Edit</button>
        </td>
      </tr>
      <tr>
        <td>Initech</td>
        <td><span class="cv-badge cv-badge-error">Failed</span></td>
        <td>3 days ago</td>
        <td>M. Mole</td>
        <td class="cv-cell-num">£430</td>
        <td class="cv-cell-actions">
          <button type="button" class="cv-btn cv-btn-ghost">View</button>
          <button type="button" class="cv-btn cv-btn-ghost">Edit</button>
        </td>
      </tr>
      <tr>
        <td>Umbrella plc.</td>
        <td><span class="cv-badge cv-badge-info">Beta</span></td>
        <td>5 days ago</td>
        <td>R. Park</td>
        <td class="cv-cell-num">£24,900</td>
        <td class="cv-cell-actions">
          <button type="button" class="cv-btn cv-btn-ghost">View</button>
          <button type="button" class="cv-btn cv-btn-ghost">Edit</button>
        </td>
      </tr>
    </tbody>
  </table>
  <div class="cv-table-footer">
    <span>Showing 1–4 of 240 records</span>
    <div class="cv-pagination" role="navigation" aria-label="Pagination">
      <button type="button" class="cv-btn cv-btn-ghost">‹ Back</button>
      <span>Page 1 of 12</span>
      <button type="button" class="cv-btn cv-btn-ghost">Next ›</button>
    </div>
    <label class="cv-pagesize">
      <span>Rows per page</span>
      <select aria-label="Rows per page">
        <option>5</option>
        <option>10</option>
        <option selected>20</option>
        <option>50</option>
      </select>
    </label>
  </div>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Header hover</span>
    <table class="cv-table"><thead><tr><th class="cv-force-hover">Name <span class="cv-sort-arrow">▲</span></th></tr></thead></table>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Sort inactive</span>
    <table class="cv-table"><thead><tr><th>Owner <span class="cv-sort-arrow cv-sort-inactive">⇅</span></th></tr></thead></table>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Row hover</span>
    <table class="cv-table"><tbody><tr class="cv-force-hover"><td>Hovered row</td></tr></tbody></table>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Row selected</span>
    <table class="cv-table"><tbody><tr class="cv-force-selected"><td>Selected row</td></tr></tbody></table>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Zebra row</span>
    <table class="cv-table"><tbody><tr><td>Odd row</td></tr><tr><td>Even row</td></tr></tbody></table>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Empty</span>
    <div class="cv-table-state"><strong>No records yet</strong>Add your first customer to get started.</div>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Loading</span>
    <div class="cv-table-state"><strong>Loading…</strong>Fetching records.</div>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Error</span>
    <div class="cv-table-state"><strong>Couldn't load records</strong>Check your connection and try again.</div>
  </div>
</div>
```

---

## tabs

**Tokens consumed:** `colours.primary`, `colours.surface`, `colours.text`, `colours.text_muted`, `typography.body_family`, `effects.transition_base`, `effects.easing_standard`.

### Live demo

```html
<div class="cv-row cv-row-col">
  <div class="cv-tabs">
    <input type="radio" name="cv-tabs-demo" id="cv-tab-1" checked>
    <input type="radio" name="cv-tabs-demo" id="cv-tab-2">
    <input type="radio" name="cv-tabs-demo" id="cv-tab-3">
    <div class="cv-tab-strip">
      <label for="cv-tab-1" class="cv-tab-label">Overview</label>
      <label for="cv-tab-2" class="cv-tab-label">Activity</label>
      <label for="cv-tab-3" class="cv-tab-label">Settings</label>
    </div>
    <div class="cv-tab-panels">
      <div class="cv-tab-panel cv-tab-panel-1">The overview panel. Click another tab — the panel switches without any JavaScript.</div>
      <div class="cv-tab-panel cv-tab-panel-2">Recent activity for this record would appear here.</div>
      <div class="cv-tab-panel cv-tab-panel-3">Per-record settings and permissions live in this panel.</div>
    </div>
  </div>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Inactive tab</span>
    <span class="cv-tab-label">Overview</span>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Active tab</span>
    <span class="cv-tab-label" style="color: {{colours.primary.hex}}; border-bottom: 2px solid {{colours.primary.hex}}; font-weight: 600;">Overview</span>
  </div>
</div>
```

---

## modal

**Tokens consumed:** `colours.surface`, `colours.text`, `colours.text_muted`, `typography.heading_family`, `typography.body_family`, `typography.size_lg`, `effects.shadow_lg`.

### Live demo

```html
<div class="cv-row cv-row-col">
  <details class="cv-modal">
    <summary><span class="cv-btn cv-btn-destructive">
      <svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M6 2h4v1h3v1H3V3h3V2zm-1 3h6l-.5 8.5a1.5 1.5 0 0 1-1.5 1.4H7a1.5 1.5 0 0 1-1.5-1.4L5 5zm2 1v7h1V6H7zm2 0v7h1V6H9z"/></svg>
      Delete invoice
    </span></summary>
    <div class="cv-modal-window" role="dialog" aria-modal="true" aria-labelledby="cv-modal-title">
      <button type="button" class="cv-modal-close" aria-label="Close dialog">×</button>
      <div class="cv-modal-title" id="cv-modal-title">Delete invoice INV-1042?</div>
      <div class="cv-modal-body">Invoice <strong>INV-1042</strong> for Acme Corp. (£12,480) will be permanently removed. This action cannot be undone.</div>
      <div class="cv-modal-actions">
        <button type="button" class="cv-btn cv-btn-ghost">Cancel</button>
        <button type="button" class="cv-btn cv-btn-destructive">
          <svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M6 2h4v1h3v1H3V3h3V2zm-1 3h6l-.5 8.5a1.5 1.5 0 0 1-1.5 1.4H7a1.5 1.5 0 0 1-1.5-1.4L5 5z"/></svg>
          Delete invoice
        </button>
      </div>
    </div>
  </details>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Closed</span>
    <span class="cv-btn cv-btn-destructive"><svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M6 2h4v1h3v1H3V3h3V2zm-1 3h6l-.5 8.5a1.5 1.5 0 0 1-1.5 1.4H7a1.5 1.5 0 0 1-1.5-1.4L5 5z"/></svg>Delete invoice</span>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Open</span>
    <div class="cv-modal-window" role="dialog" aria-modal="true" aria-labelledby="cv-modal-title-static">
      <button type="button" class="cv-modal-close" aria-label="Close dialog">×</button>
      <div class="cv-modal-title" id="cv-modal-title-static">Delete invoice INV-1042?</div>
      <div class="cv-modal-body">Invoice <strong>INV-1042</strong> for Acme Corp. will be permanently removed.</div>
      <div class="cv-modal-actions">
        <button type="button" class="cv-btn cv-btn-ghost">Cancel</button>
        <button type="button" class="cv-btn cv-btn-destructive"><svg class="cv-icon" viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M6 2h4v1h3v1H3V3h3V2zm-1 3h6l-.5 8.5a1.5 1.5 0 0 1-1.5 1.4H7a1.5 1.5 0 0 1-1.5-1.4L5 5z"/></svg>Delete</button>
      </div>
    </div>
  </div>
</div>
```
