<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: stepper-indicator

```yaml
id: stepper-indicator
kind: layout-pattern
purpose: Progress display for a multi-step flow — shows total steps, completed steps,
  current step, and (optionally) remaining steps. The visual contract for any wizard.

when-to-use:
  - Inside a multi-step-wizard (always pair these two)
  - Multi-step onboarding / setup flows (auth-flow-shell)
  - Multi-step checkout / submission flows
  - Any sequential flow with ≥3 steps where progress matters to the user

when-not-to-use:
  - 2-step flows (the second step's heading is enough)
  - Non-sequential tabs (wrong mental model; use tabs)
  - Flows where steps are dynamic and unknowable upfront (use prev-next pagination)

variants:
  - linear-numbered: 1 → 2 → 3 with labels beneath
  - linear-titled: step titles beside or beneath number markers
  - progress-bar: continuous bar with percentage / "Step n of N"
  - vertical: stacked steps (mobile-friendly or for >5 steps)
  - segmented: thin coloured segments per step (very compact)

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: -1
  density-focus: 0
  control-automation: 0
  flexibility-consistency: +1
  memorability-density: 0

required-slots:
  - steps: ordered list of {id, label, optional?: boolean}
  - current-step: id of the active step
  - completed-steps: list of step ids already completed

optional-slots:
  - on-step-click: handler if backward navigation is allowed
  - error-step: id of a step the user must return to (error variant)

states:
  default: current step highlighted, completed steps marked, future steps muted
  error: a completed step shows an error indicator (validation regressed)
  optional-skipped: an optional step user skipped is marked distinctly
  fully-complete: all steps done; usually unmounts as the flow completes

behaviours-built-in:
  - step-click navigates only to already-completed steps (forward is wizard-controlled)
  - keyboard: Tab into the indicator; Enter on a clickable step navigates
  - non-completed steps are not focusable (announce as "not yet available")

composition-rules:
  may-contain: number marker, label, icon (check / error / current)
  must-not-contain: actions, forms; this is a status indicator, not an interactive form
  parent-restrictions: lives at the top of a multi-step-wizard or auth-flow-shell;
    not standalone

token-roles-consumed:
  - text-default, text-muted
  - state-selected             # current step
  - state-success              # completed
  - state-danger               # error step
  - border-emphasis            # connector lines
  - focus-ring

accessibility:
  - role=list with role=listitem per step
  - current step has aria-current="step"
  - completed steps announce as "completed"; future steps as "not yet available"
  - reduced-motion: progress-fill animation disabled

spec-author-cues:
  - always pair with multi-step-wizard
  - linear-titled variant when step purposes are non-obvious from numbers alone
  - vertical variant when ≥5 steps or mobile-primary
  - progress-bar variant when steps are uncountable in advance but progress is measurable
  - error variant only when wizard supports back-navigation

mapping-helpers:
  ooux-signal: not a primary signal
  user-stories-signal: stories that decompose into "step 1 / step 2 / …" beats
  jtbd-signal: setup / onboarding / checkout jobs
  journeys-signal: any multi-stage journey rendered as a single flow
```
