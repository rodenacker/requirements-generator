<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: auth-flow-shell

```yaml
id: auth-flow-shell
kind: layout-primitive
purpose: Multi-step shell for sequential pre-app flows — signup, onboarding, MFA,
  email verification. Like centered-form but accommodates a wizard inside.

when-to-use:
  - Sequential signup or onboarding (≥3 steps)
  - MFA / verification flows with multiple stages
  - Pre-app setup that gates entry to the product
  - Recovery flows (password reset → verify → set new)

when-not-to-use:
  - Single-step auth (use centered-form with a single-form inside)
  - In-app onboarding (use checklist-onboarding deferred pattern, or app-shell)

variants:
  - default: stepper-indicator at top + body
  - branded: with brand artwork on a side panel
  - minimal: stepper only, no chrome
  - return-anchored: persistent "Back to login" link

default-trade-offs:
  speed-accuracy: -1
  density-focus: -2

required-slots:
  - stepper-indicator
  - step-body: routed pane for the active step
  - exit-action: link or button to abandon flow

optional-slots:
  - brand
  - help-link
  - resume-token (draft variants)

states:
  default: current step visible
  loading: per-step skeleton
  error: per-step validation
  success: replaced by confirmation-receipt or app entry

behaviours-built-in:
  - URL reflects current step
  - exiting prompts confirmation if any step is dirty
  - keyboard-friendly across all steps

composition-rules:
  may-contain: stepper-indicator, multi-step-wizard body, single-form per step,
    notification-banner
  must-not-contain: app-shell, sidebar, dashboard
  parent-restrictions: top-level

token-roles-consumed:
  - surface-default, surface-elevated, text-default, text-muted, state-selected,
    state-success, focus-ring, motion-default

accessibility:
  - landmark: main
  - heading per step (h1)
  - reduced-motion: step transitions disabled

spec-author-cues:
  - if signup is single-step → centered-form, not this
  - branded variant when first-impression matters (consumer-facing)
  - keep step count ≤5 for pre-app flows
```
