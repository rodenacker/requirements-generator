<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: notification-toast

```yaml
id: notification-toast
kind: surface-pattern
purpose: Transient, non-blocking message reporting the outcome of a recent action
  or a system event; auto-dismisses after a few seconds.

when-to-use:
  - Confirming a successful action ("Saved", "Deleted", "Sent")
  - Reporting a non-blocking error ("Connection lost — retrying")
  - Surfacing a low-priority system event (mention received, file ready)
  - Pairing with destructive-but-reversible actions to offer Undo

when-not-to-use:
  - Persistent message that must remain until acknowledged → notification-banner
  - Blocking error that requires user response → modal-confirmation or dialog
  - Form-field validation errors → inline-error (convention)
  - Long copy or rich content → banner or dialog

variants:
  - success: state-success styling; auto-dismiss default
  - info: state-info styling
  - warning: state-warning styling; longer auto-dismiss
  - error: state-danger styling; persists longer or until dismissed
  - with-undo: action button inside the toast (Undo / Retry)
  - with-link: text link to a related surface ("View details")

default-trade-offs:
  speed-accuracy: +1
  power-simplicity: 0
  density-focus: 0
  control-automation: +1
  flexibility-consistency: +1
  memorability-density: 0

required-slots:
  - kind: success / info / warning / error
  - message: short text (≤90 chars ideal)

optional-slots:
  - action: button label + handler (Undo / Retry / View)
  - dismiss: explicit close button
  - title: short heading for emphasis (rare)

states:
  default: visible
  entering: slide / fade in
  exiting: slide / fade out
  paused: hover / focus pauses auto-dismiss timer
  dismissed: removed from queue

behaviours-built-in:
  - position: configured globally per design-system (top-right default desktop;
    bottom for mobile)
  - stack: multiple toasts stack vertically; oldest dismisses first when over limit
  - auto-dismiss timer: success/info ~4s, warning ~6s, error ~8s or sticky
  - hover / focus pauses the timer
  - keyboard-reachable: each toast is focusable; Esc dismisses focused toast

composition-rules:
  may-contain: icon, short text, single action button, dismiss button
  must-not-contain: forms, tables, multiple actions, long-form copy
  parent-restrictions: rendered into a global toast-region near the viewport edge;
    not nested inside any pattern

token-roles-consumed:
  - surface-elevated
  - text-default, text-inverse        # for high-contrast variants
  - state-success, state-info, state-warning, state-danger
  - elevation-toast
  - focus-ring
  - motion-fast               # enter / exit

accessibility:
  - role=status (success/info) or role=alert (warning/error) — chosen by kind
  - aria-live polite for non-critical, assertive for errors
  - keyboard reachable; Esc dismisses focused toast
  - sufficient contrast in all colour variants
  - reduced-motion: enter / exit animation disabled

spec-author-cues:
  - reversible destructive action → toast with Undo (not modal-confirmation)
  - if user must see and acknowledge → banner, not toast
  - keep message short; toast width is constrained
  - error toasts that may need retry → with-action variant carrying Retry

mapping-helpers:
  ooux-signal: not a primary signal
  user-stories-signal: outcome statements ("a success message confirms…")
  jtbd-signal: not a primary signal
  journeys-signal: pain-point = "I never know if my action worked"
```
