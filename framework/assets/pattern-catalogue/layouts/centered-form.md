<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: centered-form

```yaml
id: centered-form
kind: layout-primitive
purpose: Single isolated form on a neutral background, vertically and horizontally
  centered; the canonical shell for auth, simple capture, and one-shot interactions
  where ambient navigation would distract.

when-to-use:
  - Authentication: login, signup, password reset, MFA prompt, email verification
  - Simple one-shot capture: feedback form, RSVP, simple intake
  - Pre-app surfaces where the user has no context yet
  - Single-purpose surfaces where Focus is the dominant trade-off

when-not-to-use:
  - In-app multi-step flows with branching (use multi-step-wizard inside an app-shell)
  - Forms with >10 fields or section groups (use single-form inside app-shell)
  - Anything requiring access to other app destinations during the flow

variants:
  - default: centered card on neutral background
  - branded: background image / gradient with logo above the card
  - split: form on one side, brand imagery / value-prop on the other
  - compact: minimal chrome, small card; for lightweight prompts

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: -1
  density-focus: -2
  control-automation: 0
  flexibility-consistency: +1
  memorability-density: -1

required-slots:
  - form-content: the form itself (typically a single-form instance)
  - heading: form title

optional-slots:
  - brand: logo above the form
  - subheading: short context line beneath the heading
  - alternate-action: secondary CTA below the form ("Already have an account? Sign in")
  - legal: ToS / privacy line at the bottom
  - background-media: image / illustration (split or branded variants)

states:
  default: form ready
  loading: submit button shows progress; fields disabled
  error: inline field errors + optional banner above the form
  success: replaced with a confirmation receipt, or redirect away
  rate-limited: form disabled with explanatory banner

behaviours-built-in:
  - autofocus on the first field on mount
  - submit on Enter from any field
  - error focus management (move focus to first invalid field on submit)
  - keyboard: Tab cycles fields → submit → alternate-action → legal links
  - browser autofill is honoured (semantic field names required)

composition-rules:
  may-contain: single-form (typical), heading, link, button, image, legal-text, banner
  must-not-contain: app-shell, sidebar, top-nav (this layout replaces them);
    multi-step-wizard (use auth-flow-shell instead);
    tables, dashboards (wrong shell entirely)
  parent-restrictions: top-level — cannot be nested

token-roles-consumed:
  - surface-default            # background
  - surface-elevated           # card
  - text-default, text-muted
  - border-subtle
  - elevation-card
  - focus-ring
  - state-danger               # error variant

accessibility:
  - main landmark wraps the card
  - heading is h1 (this is the page's primary purpose)
  - autocomplete attributes match field semantics (email, current-password, new-password, one-time-code)
  - error association: aria-describedby links each invalid field to its error message
  - reduced-motion: no entrance animation if reduced-motion preferred

spec-author-cues:
  - if the brief includes auth flows, every auth surface uses this pattern
  - if the form is meaningfully > one screen of fields, escalate to single-form inside app-shell or multi-step-wizard
  - if the form is the entire app's first screen, branded or split variant carries the brand introduction
  - keep the alternate-action visually subordinate to the primary submit

mapping-helpers:
  ooux-signal: not a primary signal; this pattern serves cross-cutting capture / auth
  user-stories-signal: "as a user I want to {sign in / sign up / reset password / verify}"
  jtbd-signal: "get-into-the-product" or "recover-access" jobs
  journeys-signal: journey-stage = "entry" or "re-entry"
```
