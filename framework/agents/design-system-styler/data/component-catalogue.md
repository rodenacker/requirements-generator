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
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
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
```

---

## buttons

**Tokens consumed:** `colours.primary`, `colours.secondary`, `colours.error`, `colours.surface`, `colours.text`, `typography.body_family`, `effects.transition_base`, `effects.easing_standard`.

### Live demo

```html
<div class="cv-row">
  <button type="button" class="cv-btn cv-btn-primary">Primary</button>
  <button type="button" class="cv-btn cv-btn-secondary">Secondary</button>
  <button type="button" class="cv-btn cv-btn-ghost">Ghost</button>
  <button type="button" class="cv-btn cv-btn-destructive">Delete</button>
  <button type="button" class="cv-btn cv-btn-primary" disabled>Disabled</button>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Default</span><button type="button" class="cv-btn cv-btn-primary">Primary</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Hover</span><button type="button" class="cv-btn cv-btn-primary cv-force-hover">Primary</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Active</span><button type="button" class="cv-btn cv-btn-primary cv-force-active">Primary</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Focus</span><button type="button" class="cv-btn cv-btn-primary cv-force-focus">Primary</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Disabled</span><button type="button" class="cv-btn cv-btn-primary cv-force-disabled">Primary</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Default</span><button type="button" class="cv-btn cv-btn-secondary">Secondary</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Hover</span><button type="button" class="cv-btn cv-btn-secondary cv-force-hover">Secondary</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Active</span><button type="button" class="cv-btn cv-btn-secondary cv-force-active">Secondary</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Focus</span><button type="button" class="cv-btn cv-btn-secondary cv-force-focus">Secondary</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Disabled</span><button type="button" class="cv-btn cv-btn-secondary cv-force-disabled">Secondary</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Default</span><button type="button" class="cv-btn cv-btn-ghost">Ghost</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Hover</span><button type="button" class="cv-btn cv-btn-ghost cv-force-hover">Ghost</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Active</span><button type="button" class="cv-btn cv-btn-ghost cv-force-active">Ghost</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Focus</span><button type="button" class="cv-btn cv-btn-ghost cv-force-focus">Ghost</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Disabled</span><button type="button" class="cv-btn cv-btn-ghost cv-force-disabled">Ghost</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Default</span><button type="button" class="cv-btn cv-btn-destructive">Delete</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Hover</span><button type="button" class="cv-btn cv-btn-destructive cv-force-hover">Delete</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Active</span><button type="button" class="cv-btn cv-btn-destructive cv-force-active">Delete</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Focus</span><button type="button" class="cv-btn cv-btn-destructive cv-force-focus">Delete</button></div>
  <div class="cv-state-cell"><span class="cv-state-label">Disabled</span><button type="button" class="cv-btn cv-btn-destructive cv-force-disabled">Delete</button></div>
</div>
```

---

## form-inputs

**Tokens consumed:** `colours.primary`, `colours.error`, `colours.surface`, `colours.background`, `colours.text`, `colours.text_muted`, `typography.body_family`, `effects.transition_base`, `effects.easing_standard`, `effects.shadow_sm`.

### Live demo

```html
<div class="cv-row cv-row-col">
  <div class="cv-field">
    <label class="cv-field-label" for="cv-demo-text">Full name</label>
    <input id="cv-demo-text" type="text" class="cv-input" placeholder="Jane Doe">
    <span class="cv-field-hint">First and last as on your ID.</span>
  </div>
  <div class="cv-field">
    <label class="cv-field-label" for="cv-demo-textarea">Notes</label>
    <textarea id="cv-demo-textarea" class="cv-textarea" placeholder="Optional context..."></textarea>
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
  <div class="cv-state-cell"><span class="cv-state-label">Error</span><input type="text" class="cv-input cv-force-error" value="Jane Doe"><span class="cv-field-error">Required</span></div>
  <div class="cv-state-cell"><span class="cv-state-label">Disabled</span><input type="text" class="cv-input cv-force-disabled" value="Jane Doe" disabled></div>
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
  <div class="cv-alert cv-alert-success"><strong>Success.</strong> Your changes were saved.</div>
  <div class="cv-alert cv-alert-warning"><strong>Heads up.</strong> Your session expires in 5 minutes.</div>
  <div class="cv-alert cv-alert-error"><strong>Error.</strong> We couldn't reach the server. Try again.</div>
  <div class="cv-alert cv-alert-info"><strong>FYI.</strong> A new version of the dashboard is available.</div>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Success</span><div class="cv-alert cv-alert-success"><strong>Saved.</strong></div></div>
  <div class="cv-state-cell"><span class="cv-state-label">Warning</span><div class="cv-alert cv-alert-warning"><strong>Heads up.</strong></div></div>
  <div class="cv-state-cell"><span class="cv-state-label">Error</span><div class="cv-alert cv-alert-error"><strong>Error.</strong></div></div>
  <div class="cv-state-cell"><span class="cv-state-label">Info</span><div class="cv-alert cv-alert-info"><strong>FYI.</strong></div></div>
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
  <table class="cv-table">
    <thead>
      <tr>
        <th>Name <span class="cv-sort-arrow">▲</span></th>
        <th>Status</th>
        <th>Updated</th>
        <th>Owner</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Acme Corp.</td><td><span class="cv-badge cv-badge-success">Active</span></td><td>2 hours ago</td><td>J. Doe</td></tr>
      <tr class="cv-row-selected"><td>Globex Ltd.</td><td><span class="cv-badge cv-badge-warning">Pending</span></td><td>1 day ago</td><td>A. Smith</td></tr>
      <tr><td>Initech</td><td><span class="cv-badge cv-badge-error">Failed</span></td><td>3 days ago</td><td>M. Mole</td></tr>
      <tr><td>Umbrella plc.</td><td><span class="cv-badge cv-badge-info">Beta</span></td><td>5 days ago</td><td>R. Park</td></tr>
    </tbody>
  </table>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Header hover</span>
    <table class="cv-table"><thead><tr><th class="cv-force-hover">Name <span class="cv-sort-arrow">▲</span></th></tr></thead></table>
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
    <summary><span class="cv-btn cv-btn-primary">Open dialog</span></summary>
    <div class="cv-modal-window">
      <div class="cv-modal-title">Confirm delete</div>
      <div class="cv-modal-body">You're about to permanently delete this record. This action cannot be undone.</div>
      <div class="cv-modal-actions">
        <button type="button" class="cv-btn cv-btn-ghost">Cancel</button>
        <button type="button" class="cv-btn cv-btn-destructive">Delete</button>
      </div>
    </div>
  </details>
</div>
```

### States matrix

```html
<div class="cv-state-grid">
  <div class="cv-state-cell"><span class="cv-state-label">Closed</span>
    <span class="cv-btn cv-btn-primary">Open dialog</span>
  </div>
  <div class="cv-state-cell"><span class="cv-state-label">Open</span>
    <div class="cv-modal-window">
      <div class="cv-modal-title">Confirm delete</div>
      <div class="cv-modal-body">Permanent action.</div>
      <div class="cv-modal-actions">
        <button type="button" class="cv-btn cv-btn-ghost">Cancel</button>
        <button type="button" class="cv-btn cv-btn-destructive">Delete</button>
      </div>
    </div>
  </div>
</div>
```
