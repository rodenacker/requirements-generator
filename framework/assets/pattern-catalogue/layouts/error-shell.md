<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: error-shell

```yaml
id: error-shell
kind: layout-primitive
purpose: Full-page surface for terminal failure states — 404, 500, maintenance,
  no-permission, account-locked. Replaces the normal app shell.

when-to-use:
  - HTTP-level error (404 / 500) where the requested resource is genuinely unreachable
  - Maintenance window where the whole app is unavailable
  - Account-level block (suspended, locked) where in-app navigation is meaningless
  - No-permission state at the route level (vs in-page permission-gate)

when-not-to-use:
  - Section-level error inside the app (use the surface's error state)
  - Recoverable error (use error state with retry CTA in-context)
  - Form validation error (use inline-error / banner)

variants:
  - 404-not-found: with search / browse alternatives
  - 500-server: with retry CTA and status-page link
  - maintenance: with eta and alternate channel
  - no-permission: with contact-admin CTA
  - account-locked: with reason + recovery action

default-trade-offs:
  speed-accuracy: 0
  density-focus: -2
  flexibility-consistency: +1

required-slots:
  - kind: 404 / 500 / maintenance / no-permission / account-locked
  - heading
  - body: explanation
  - primary-cta: home / retry / contact

optional-slots:
  - illustration
  - secondary-cta
  - status-link
  - search (for 404)

states:
  default: error rendered

behaviours-built-in:
  - retry CTA re-attempts the failed request
  - back link returns to last good state when meaningful

composition-rules:
  may-contain: heading, body text, illustration, button cluster, link, search (404)
  must-not-contain: app-shell, marketing-shell, dashboard, table
  parent-restrictions: top-level

token-roles-consumed:
  - surface-default, text-default, text-muted, state-danger, focus-ring

accessibility:
  - heading is h1
  - status code visually present + announced
  - reduced-motion: illustration animation disabled

spec-author-cues:
  - copy must be specific and non-blaming
  - 404 with search-context lets users recover without leaving
  - never use error-shell for transient failures; reserve it for terminal states
```
