<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: signup-form

```yaml
id: signup-form
kind: composite-pattern
purpose: Account creation form — typically email + password + optional name +
  terms-of-service consent, with optional verification step afterward.
status: stub

when-to-use:
  - New-user account creation
  - Always inside `centered-form` (single-step) or `auth-flow-shell` (multi-step)

when-not-to-use:
  - Returning-user authentication → login-form
  - Onboarding / first-run product setup → checklist-onboarding (deferred)

variant-clusters: minimal (email + password), with-name-fields, with-organisation,
  with-oauth-shortcut, with-tos-checkbox, with-verification-step,
  invitation-bound (token-pre-fills email)

required-slots-baseline: email-field, password-field, submit, login-link, tos-link
key-tokens: surface-elevated, text-default, state-danger, state-success, focus-ring

related: centered-form, login-form, auth-flow-shell
```

> **Author the full entry when:** the first product brief includes signup. Password-strength + duplicate-email handling deserve careful state design.
