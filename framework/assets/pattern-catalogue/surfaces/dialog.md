<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: dialog

```yaml
id: dialog
kind: surface-pattern
purpose: Blocking overlay for irreversible actions with multiple distinct outcomes
  (vs binary modal-confirmation). The pattern when there are 3+ paths the user can take.
status: stub

when-to-use:
  - Action has ≥3 meaningful outcomes ("Save / Save as draft / Discard")
  - Discard / Save / Cancel triple
  - High-stakes choice that warrants explicit reading

when-not-to-use:
  - Binary confirm/cancel → modal-confirmation
  - The user just needs information → notification-banner

variant-clusters: triple-choice, save-or-discard, lifecycle (publish / draft / archive),
  with-explanation-list

related: modal-confirmation, modal-form
```

> **Author the full entry when:** the first brief presents a ≥3-outcome blocking decision. Most products manage with `modal-confirmation`; reach for `dialog` only when truly multi-path.
