<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: modal-confirmation

```yaml
id: modal-confirmation
kind: surface-pattern
purpose: A blocking overlay that confirms a destructive or irreversible action
  before commit; the canonical "are you sure?" surface.

when-to-use:
  - Action is destructive (delete, remove, archive)
  - Action is irreversible or expensive to reverse (publish, send, charge, deploy)
  - Persona has high stakes signal ("must not contain errors")
  - User is one click away from regret

when-not-to-use:
  - Action is reversible and lightweight (just do it; offer undo via toast instead)
  - Action requires meaningful re-input from the user → modal-form
  - Multiple distinct outcome paths beyond confirm/cancel → use dialog (T3)
  - Action is part of a flow already gated by an explicit submit (don't double-gate)

variants:
  - default: heading + body + cancel + confirm
  - destructive: confirm button uses danger style (delete / remove)
  - typed-confirm: user must type a phrase ("DELETE") to enable confirm
  - irreversible-warning: explicit "this cannot be undone" copy
  - with-input: short input (e.g., reason for deletion); for moderate friction without becoming a form

default-trade-offs:
  speed-accuracy: -1
  power-simplicity: -1
  density-focus: -1
  control-automation: +1
  flexibility-consistency: +1
  memorability-density: 0

required-slots:
  - heading: question or statement of the action
  - body: explanation of what will happen
  - confirm-action: primary CTA + handler
  - cancel-action: secondary CTA (always present)

optional-slots:
  - typed-confirm-phrase: required text the user must match
  - input: short reason / note input
  - banner: warning banner inside the modal

states:
  default: modal open, confirm enabled (or disabled until typed-confirm matches)
  loading: confirm button shows progress; cancel still available
  error: error banner inside modal; modal does not close
  success: modal closes; outer surface refreshes; toast announces success

behaviours-built-in:
  - focus moves into the modal on open; focus trapped while open
  - Escape closes (cancel); Enter submits confirm (when focus is on confirm)
  - clicking the backdrop closes (cancel) — except for typed-confirm variant
  - on close, focus returns to the trigger element
  - typed-confirm: confirm button enabled only when input matches phrase
    (case-insensitive by default)

composition-rules:
  may-contain: heading, paragraph text, banner, single short input (with-input variant),
    list of consequences
  must-not-contain: forms with multiple sections (use modal-form),
    tables, dashboards, another modal
  parent-restrictions: opened from any pattern via a destructive trigger

token-roles-consumed:
  - surface-overlay            # backdrop
  - surface-elevated           # modal panel
  - text-default
  - state-danger               # destructive variant
  - elevation-modal
  - focus-ring
  - motion-default             # open / close

accessibility:
  - role=dialog, aria-modal=true
  - aria-labelledby points to heading; aria-describedby to body
  - focus trapped within modal
  - reduced-motion: backdrop / panel transitions disabled
  - destructive variant uses both colour and an icon (not colour alone)

spec-author-cues:
  - destructive-action that's reversible → toast with undo, NOT modal-confirmation
  - high-stakes irreversible (e.g., "delete entire workspace") → typed-confirm variant
  - if user needs to *provide* something to proceed → modal-form, not modal-confirmation
  - keep body short; users skim modals — anything important must be in the heading or first sentence

mapping-helpers:
  ooux-signal: destructive CTA on any object (delete, remove, archive)
  user-stories-signal: "as a {role} I want to delete / remove / archive {object}" — wrap in confirmation
  jtbd-signal: not a primary signal
  journeys-signal: pain-point = "I deleted by accident"
```
