<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: drawer-form

```yaml
id: drawer-form
kind: surface-pattern
purpose: A side-entering panel containing a form — for create / edit flows that
  benefit from staying in context with the parent surface.

when-to-use:
  - Form is medium length (8–20 fields) and benefits from longer vertical space than a modal
  - User wants / needs to see parent surface while filling (non-modal variant)
  - Edit a record from a list / table without leaving the list

when-not-to-use:
  - Short form (≤8 fields) → modal-form
  - Long form (>20 fields) or multi-section → single-form on a page
  - Multi-step → multi-step-wizard on a page; not in a drawer

variants:
  - modal-drawer: dims background; user must finish or cancel
  - non-modal: outer surface remains interactive
  - right-side / left-side / bottom-sheet (mobile)
  - persistent: pinnable open

default-trade-offs:
  speed-accuracy: 0
  density-focus: 0
  flexibility-consistency: +1

required-slots:
  - heading
  - form-content
  - submit-action
  - cancel-action

optional-slots:
  - banner
  - footer with secondary actions
  - help-aside

states:
  default: open, form ready
  loading / submitting / error / success: as single-form
  unsaved-changes: closing prompts confirmation when dirty

behaviours-built-in:
  - focus into drawer on open; trap when modal
  - Escape closes (with guard); Enter submits when focus on submit
  - URL sync (optional)
  - non-modal variant: parent surface stays interactive

composition-rules:
  may-contain: single-form sections, banner, button cluster, repeater, file-upload (T3)
  must-not-contain: another drawer, multi-step-wizard, dashboard
  parent-restrictions: opened from any pattern

token-roles-consumed:
  - surface-overlay (modal variant), surface-elevated, text-default, state-danger,
    state-success, elevation-drawer, focus-ring, motion-default

accessibility:
  - role=dialog with aria-modal matching variant
  - heading via aria-labelledby
  - focus trap (modal variant); focus return to trigger
  - reduced-motion: slide animation disabled

spec-author-cues:
  - if user references outer content while filling → non-modal variant
  - mobile-primary → consider bottom-sheet variant (deferred pattern)
  - persistent variant rare; only when continuous-edit alongside list is the dominant flow
```
