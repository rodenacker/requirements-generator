<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: modal-form

```yaml
id: modal-form
kind: surface-pattern
purpose: A blocking overlay containing a small form — typically used for create
  or quick-edit flows that don't warrant a full page.

when-to-use:
  - Create / edit ≤8 fields where the parent context matters
  - Quick action that the user expects to complete and dismiss
  - Avoid losing the user's place in the parent surface

when-not-to-use:
  - Form has >8 fields or section groups → drawer-form or single-form on a page
  - Multi-step → multi-step-wizard (not in a modal; it traps users)
  - User needs to reference parent content while filling → drawer-form (non-modal)

variants:
  - default: heading + body + cancel + submit
  - with-banner: top banner inside modal (info / warning)
  - destructive: submit styled as danger (rare; usually means modal-confirmation suits better)
  - large: full single-form inside (M+ size; reconsider whether it should be a page)

default-trade-offs:
  speed-accuracy: 0
  density-focus: -1
  control-automation: +1

required-slots:
  - heading
  - form-content: a single-form-shape body
  - submit-action
  - cancel-action

optional-slots:
  - banner
  - help-link

states:
  default: open, form ready
  loading: submit shows progress; fields disabled
  error: field-level errors + optional banner; modal stays open
  success: closes; outer surface refreshes; toast confirms
  unsaved-changes: closing prompts confirmation when dirty

behaviours-built-in:
  - focus into modal on open; trap; return to trigger on close
  - Escape closes (with unsaved-changes guard)
  - Enter submits (when focus on submit; not in multi-line fields)
  - autofocus first field

composition-rules:
  may-contain: heading, single-form sections, banner, button cluster
  must-not-contain: another modal, multi-step-wizard, table, dashboard
  parent-restrictions: opened from any pattern via a CTA

token-roles-consumed:
  - surface-overlay, surface-elevated, text-default, state-danger, state-success,
    elevation-modal, focus-ring, motion-default

accessibility:
  - role=dialog, aria-modal=true, aria-labelledby (heading)
  - focus trap; close returns focus to trigger
  - reduced-motion: open / close animation disabled

spec-author-cues:
  - if user must reference outer content → drawer-form, not modal-form
  - if multi-step → never in a modal
  - keep field count low; modals feel cramped past ~8
```
