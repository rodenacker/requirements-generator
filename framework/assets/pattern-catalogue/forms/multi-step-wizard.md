<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: multi-step-wizard

```yaml
id: multi-step-wizard
kind: composite-pattern
purpose: Sequential multi-step flow with validated forward progress; each step
  isolates a coherent slice of work, prior steps must validate before next.

when-to-use:
  - Capture / configure with logical sequencing (later steps depend on earlier)
  - Persona is novice or task is high-stakes (Focus + Accuracy beats Density)
  - Onboarding, setup, multi-section submission with clear order
  - 3–7 steps total

when-not-to-use:
  - Steps are non-sequential / freely re-orderable → use settings-shell or tabs
  - <3 steps → single-form is enough
  - >7 steps → reconsider scope; users abandon long wizards
  - Each step deserves a deep-linkable URL → multi-page-form (T3)

variants:
  - linear: forward-only; cannot revisit a completed step
  - reviewable: can revisit any completed step; shown in stepper as clickable
  - branching: step path varies based on earlier answers
  - draftable: can save draft and resume later
  - with-summary: penultimate step is a review-and-confirm of all data

default-trade-offs:
  speed-accuracy: -1
  power-simplicity: -1
  density-focus: -2
  control-automation: 0
  flexibility-consistency: +1
  memorability-density: -1

required-slots:
  - steps: ordered list of {id, label, validator, body-renderer}
  - current-step: id of the active step
  - completed-steps: ids already validated

optional-slots:
  - stepper-indicator: paired pattern at the top
  - draft-save: explicit "save and exit" action
  - review-step: paired with-summary variant
  - exit-confirmation

states:
  default: current step rendered with prev / next actions
  loading (per step): step body skeleton while resolving data
  submitting (forward): next button shows progress; fields disabled
  error (per step): step-level validation errors block forward
  draft-saved: confirmation banner; user can leave and resume
  complete: final state — usually replaced by confirmation-receipt

behaviours-built-in:
  - forward navigation only after current step validates
  - back navigation returns to the prior step preserving its state
  - exiting prompts confirmation if any step is dirty
  - keyboard: Tab through fields → next; Enter submits step; Esc cancels (with confirmation)
  - URL reflects current step (?step=N) so refresh / back work
  - draft-save persists state and allows resumption (draftable variant)

composition-rules:
  may-contain (per step): single-form sections, repeater, file-upload (T3),
    inline-error, banner, help-aside
  must-not-contain: another wizard (no nesting), table (each step is a form, not a list),
    modal (modals interrupt the flow)
  parent-restrictions: legal in any layout-primitive; common inside auth-flow-shell
    or as a routed page in app-shell

token-roles-consumed:
  - surface-default, surface-elevated
  - text-default, text-muted
  - state-selected             # current step in stepper
  - state-success              # completed steps
  - focus-ring
  - motion-default             # step transition

accessibility:
  - heading per step (h1) communicates current step purpose
  - stepper-indicator follows its own accessibility rules
  - error summary on step submit failure
  - reduced-motion: step transitions disabled

spec-author-cues:
  - always pair with stepper-indicator
  - branching variant adds significant build cost — only when the branching has clear cause in §4 task-flow
  - high-stakes / regulatory submission → with-summary variant (review before commit)
  - draftable variant when persona context can interrupt mid-flow (mobile, multi-session)
  - if step body grows beyond a screen, that step is too big — split it

mapping-helpers:
  ooux-signal: not a primary signal; wizards serve task flows over object creation
  user-stories-signal: stories that decompose into "step 1 / step 2 / …" with sequencing
  jtbd-signal: setup / submit / onboard jobs with sequential structure
  journeys-signal: explicit multi-stage journey rendered as a single flow
```
