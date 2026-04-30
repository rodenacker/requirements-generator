<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: notification-banner

```yaml
id: notification-banner
kind: composite-pattern
purpose: Persistent, dismissible message at the top of a region or page; for
  state that the user should see and acknowledge but not block on.

when-to-use:
  - System-wide announcement (maintenance window, new release)
  - Account-level state that persists across the session (trial expires soon)
  - Section-level info / warning (read-only mode, missing config)
  - State that warrants more attention than a toast but doesn't block

when-not-to-use:
  - Transient outcome → notification-toast
  - Blocking required → dialog or modal-confirmation
  - Field-level → inline-error / inline-success

variants:
  - info: state-info styling
  - success: state-success styling
  - warning: state-warning styling
  - error: state-danger styling
  - announcement: brand-styled; for product-marketing announcements
  - with-action: CTA inside the banner (Upgrade / Learn more / Configure)

default-trade-offs:
  speed-accuracy: 0
  density-focus: 0
  flexibility-consistency: +1

required-slots:
  - kind: info / success / warning / error / announcement
  - message

optional-slots:
  - heading (when message warrants emphasis)
  - action (CTA inside the banner)
  - dismiss (per-user dismissal — sticky)

states:
  default: visible
  dismissed: hidden until next eligible session / event

behaviours-built-in:
  - dismissal persists per-user (when scope warrants — e.g., per-release)
  - keyboard-reachable; action and dismiss reachable via Tab
  - links / actions inside banners follow normal focus rules

composition-rules:
  may-contain: icon, heading, message, action button, link, dismiss
  must-not-contain: forms, tables, complex content
  parent-restrictions: page-top, section-top, modal-top, drawer-top

token-roles-consumed:
  - surface-elevated, text-default, text-inverse,
    state-info, state-success, state-warning, state-danger, focus-ring

accessibility:
  - role=status (info/success) or role=alert (warning/error)
  - dismiss button has aria-label
  - sufficient contrast in all variants
  - reduced-motion: entrance animation disabled

spec-author-cues:
  - banner copy must be specific and actionable
  - if banner is system-wide, scope dismissal correctly (per-release vs per-session)
  - error-banner with no recovery CTA is a smell — give the user something to do
```
