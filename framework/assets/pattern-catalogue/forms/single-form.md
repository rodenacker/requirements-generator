<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: single-form

```yaml
id: single-form
kind: composite-pattern
purpose: One-step form on a page — section groups, fields, validation, submit;
  the canonical capture / edit surface for non-sequential input.

when-to-use:
  - Capturing or editing one record, all at once
  - 5–30 fields organised into 1–4 logical groups
  - User can fill in any order; no enforced sequence
  - Validation is field-level + form-level on submit

when-not-to-use:
  - Sequential dependencies between sections → multi-step-wizard
  - <5 fields with no grouping → use a simpler inline form or modal-form
  - >30 fields → split into multi-step-wizard or settings-shell

variants:
  - default: vertical stack of section groups + actions
  - two-column: paired fields side-by-side; for desk-class or wide layouts
  - compact: dense field layout; expert / power persona
  - scrollable-with-save-bar: long form with sticky save / discard footer
  - segmented: top tabs split sections (alternative to scrolling)
  - readonly-toggle: switches between view and edit mode

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: 0
  density-focus: 0
  control-automation: +1
  flexibility-consistency: 0
  memorability-density: 0

required-slots:
  - sections: ordered list of {id, label, fields}
  - fields: per-section list of {key, label, type, required?, validation, help-text?}
  - submit-action: primary CTA + handler

optional-slots:
  - cancel-action
  - save-bar: sticky footer for long forms
  - delete-action: destructive secondary (typically opens modal-confirmation)
  - banner: top-of-form info / warning
  - help-aside: contextual help panel (right side on wide layouts)

states:
  default: form ready
  loading: form rendered, fields disabled while initial data loads (edit mode)
  submitting: submit button shows progress; fields disabled
  error: field-level errors + optional form-level banner
  success: redirect, or confirmation-receipt, or stay-with-success-banner
  unsaved-changes: leaving prompts confirmation
  readonly: fields render as values; edit affordance restores edit mode

behaviours-built-in:
  - autofocus first field on mount (create mode)
  - autosave (optional): per-field commit; honours conflict resolution
  - validation timing: on-blur for sync, on-submit for async; never on-keystroke
  - error focus management: first invalid field gains focus on submit
  - keyboard: Tab through fields → submit → cancel; Enter submits from any field
    unless field is multiline
  - dirty-tracking: unsaved-changes prompt only when truly dirty

composition-rules:
  may-contain: field atoms, section group, fieldset, repeater, file-upload (T3),
    inline-error, banner, help-text, button cluster
  must-not-contain: another single-form, multi-step-wizard, table, dashboard
  parent-restrictions: legal in any layout-primitive, in modal (M+ → modal-form),
    in drawer (drawer-form), in settings-shell content pane

token-roles-consumed:
  - surface-default, surface-elevated
  - text-default, text-muted
  - border-subtle, border-emphasis
  - state-danger               # error state
  - state-success              # success banner
  - focus-ring
  - elevation-toast            # save-bar

accessibility:
  - landmark: form
  - each field has a visible label and aria-describedby links to help / error
  - required fields marked semantically (aria-required) and visually
  - error summary announced on submit failure (aria-live polite)
  - autocomplete attributes match field semantics
  - reduced-motion: save-bar slide-in disabled

spec-author-cues:
  - field count drives variant: ≤8 default; 9–20 with section groups;
    >20 escalate to multi-step-wizard or settings-shell
  - if §3 has high-stakes signal → add save-bar + explicit confirmation on destructive
  - if persona daily-frequency expert → compact variant
  - readonly-toggle when the same form serves view + edit (common in detail pages)

mapping-helpers:
  ooux-signal: object create / edit CTA
  user-stories-signal: "as a {role} I want to add / edit / update {object}"
  jtbd-signal: capture / record / configure jobs
  journeys-signal: stage = "input" or "edit"
```
