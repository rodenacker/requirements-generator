<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: inline-edit

```yaml
id: inline-edit
kind: composite-pattern
purpose: Edit-in-place for a single field within a row, panel, or detail surface;
  no modal, no separate form — click / activate to edit, blur or commit to save.

when-to-use:
  - Quick edits on individual fields where context matters more than form structure
  - Power-user persona; daily editing
  - Table rows with editable cells (table editable variant)
  - Detail panels / pages where occasional field edits are common

when-not-to-use:
  - Multiple fields edit together (use single-form or modal-form)
  - High-stakes irreversible edits (force a confirmation)
  - Validation requires cross-field rules
  - Novice persona — discoverability is poor

variants:
  - click-to-edit: read-only by default; click to enter edit mode
  - hover-affordance: edit icon visible on hover/focus
  - always-editable: field is always an input
  - autosave: commits on blur
  - explicit-commit: per-field save / cancel buttons

default-trade-offs:
  speed-accuracy: +1
  power-simplicity: +1
  control-automation: +1

required-slots:
  - value: current field value
  - on-commit: handler that persists the new value

optional-slots:
  - validate: per-field validation
  - on-cancel: handler when user cancels
  - undo: post-commit toast offering undo

states:
  default: read-only display
  editing: input focused, value editable
  saving: input disabled with progress
  saved: brief confirmation (transient — fades)
  error: error message inline; field returns to editing
  invalid: validation message visible without committing

behaviours-built-in:
  - Enter commits; Escape cancels; click-outside commits (autosave variant)
    or cancels (explicit-commit variant)
  - Tab commits and moves to next editable field (table editable variant)
  - rollback on commit-failure: value reverts, error visible

composition-rules:
  may-contain: input atom (text, number, select, date), inline-error, inline-success
  must-not-contain: complex content, multi-line form, modal
  parent-restrictions: lives inside a table cell, data-list row, detail-panel field,
    detail-page editable variant

token-roles-consumed:
  - surface-default, text-default, border-emphasis, focus-ring, state-danger,
    state-success, motion-fast

accessibility:
  - editable affordance announced (e.g., "Editable. Press Enter to edit.")
  - state changes announced (saving, saved, error)
  - escape returns to read-only without commit
  - reduced-motion: confirmation fade disabled

spec-author-cues:
  - power-user persona + frequent edit signal → inline-edit beats modal-form
  - high-stakes destructive field edit → require confirmation, not raw inline-edit
  - always pair commit with toast confirmation when commit is async
```
