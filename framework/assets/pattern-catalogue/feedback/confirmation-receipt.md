<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: confirmation-receipt

```yaml
id: confirmation-receipt
kind: composite-pattern
purpose: Post-action summary surface — what happened, key details, what's next.
  The "you did the thing" page after a meaningful submission.

when-to-use:
  - End of a multi-step-wizard or auth-flow-shell
  - After a high-stakes / financial / irreversible submission
  - Marketing-style "thank you" pages
  - Anywhere the user needs a record to refer back to (or print)

when-not-to-use:
  - Routine save → notification-toast is enough
  - In-app create where the user continues working immediately
  - Small reversible actions

variants:
  - default: heading + summary + next-steps
  - receipt-style: with reference number, dates, line items
  - email-confirmation: explanation that an email has been sent
  - account-created: with onboarding next-steps
  - print-friendly: degrades cleanly to print-shell

default-trade-offs:
  speed-accuracy: 0
  density-focus: -1
  flexibility-consistency: +1

required-slots:
  - heading: confirmation statement
  - summary: what happened (object names, ids, timestamps)
  - next-step: primary CTA or guidance

optional-slots:
  - reference-number / id: for support reference
  - line-items: details of what was submitted
  - print-action
  - share / forward action
  - secondary-cta

states:
  default: rendered
  loading: skeleton (rare; receipts are usually post-action)

behaviours-built-in:
  - URL is deep-linkable (user can return to the receipt)
  - print-friendly CSS
  - copy-reference action (where applicable)

composition-rules:
  may-contain: heading, paragraph text, attribute-list, line-item table, button cluster
  must-not-contain: forms, multi-step-wizard, dashboard
  parent-restrictions: usually a routed page; sometimes inside a final wizard step

token-roles-consumed:
  - surface-default, surface-elevated, text-default, text-muted, state-success,
    border-subtle, elevation-card, focus-ring

accessibility:
  - heading is h1 (page-level confirmation)
  - state-success colour is paired with icon + text (not colour alone)
  - reduced-motion: no entrance animation

spec-author-cues:
  - high-stakes submission (payment, legal, regulatory) → confirmation-receipt is mandatory
  - include reference-number when user might need support follow-up
  - next-step CTA must give the user a meaningful onward path
```
