<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: multi-page-form

```yaml
id: multi-page-form
kind: composite-pattern
purpose: Like multi-step-wizard but each step is its own route — deep-linkable,
  back-button-friendly, refresh-safe per step. Used when steps must be shareable
  or resumable across sessions.
status: stub

when-to-use:
  - Steps need deep-linking (support / collaboration / mid-flow handoff)
  - Long-running flows that span sessions
  - Government / regulatory / heavy submissions where each step archives

when-not-to-use:
  - Tight sequential flow within one session → multi-step-wizard
  - Brief signup / onboarding → auth-flow-shell

variant-clusters: linear, branching, draftable, with-summary-page, with-resume-token

related: multi-step-wizard, auth-flow-shell
```

> **Author the full entry when:** the first deep-linkable multi-step flow lands. Differs from `multi-step-wizard` chiefly in routing semantics.
