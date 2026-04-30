<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: login-form

```yaml
id: login-form
kind: composite-pattern
purpose: Authentication form — email / password (or username), optional remember-me,
  forgot-password link, optional OAuth provider buttons. A configured `centered-form`.
status: stub

when-to-use:
  - Returning-user authentication into the app
  - Always inside `centered-form` (or `auth-flow-shell` if multi-step)

when-not-to-use:
  - Signup → signup-form
  - MFA prompt → mfa-prompt (deferred)
  - Password reset → password-reset-flow (deferred)

variant-clusters: email-password, username-password, with-oauth (Google / GitHub / SSO),
  passwordless-magic-link, with-mfa-step, with-organisation-selector

required-slots-baseline: identifier-field (email / username), password-field, submit,
  forgot-password-link, signup-link
key-tokens: surface-elevated, text-default, state-danger, focus-ring

related: centered-form, signup-form, auth-flow-shell
```

> **Author the full entry when:** the first product brief includes auth. Lift validated patterns from auth provider conventions; do not reinvent.
