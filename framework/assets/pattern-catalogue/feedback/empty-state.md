<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: empty-state

```yaml
id: empty-state
kind: composite-pattern
purpose: "No data yet" surface — illustration / icon + copy explaining why it's empty
  + a primary CTA that resolves the emptiness.

when-to-use:
  - First-run state of any collection (no records yet)
  - Filtered / searched state with no matches
  - Permission-restricted state (no access to anything in this scope)
  - Cleared inbox / triaged queue (positive empty)

when-not-to-use:
  - Loading state masquerading as empty → use loading-skeleton instead
  - Error state → use error block / error-shell
  - Inside a row / cell where space is too small → use a muted placeholder string

variants:
  - first-run: explanatory copy + primary CTA to create first record
  - no-results: short copy + clear-filters CTA
  - no-permission: explanation + contact-admin CTA
  - cleared: positive empty (you're done!) with optional next-step suggestion
  - illustrated: with a simple illustration or icon
  - text-only: minimal; for compact contexts (panel, drawer)

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: -1
  density-focus: -1
  control-automation: 0
  flexibility-consistency: 0
  memorability-density: -1

required-slots:
  - kind: first-run / no-results / no-permission / cleared
  - heading: short statement of the state
  - body: one or two sentences explaining
  - primary-cta: action that resolves the emptiness (or progresses the user)

optional-slots:
  - illustration / icon
  - secondary-cta: alternative path
  - help-link: docs / tour / explanation
  - filters-applied summary: for no-results variant ("No matches for 'foo' in Open status")

states:
  default: rendered as the body of a collection or surface
  (the empty-state itself does not have multiple sub-states; it IS a state)

behaviours-built-in:
  - primary-cta is keyboard-reachable
  - clear-filters CTA (no-results variant) resets the parent search-and-filter
  - first-run variant CTA opens create flow (modal-form, single-form, or wizard)

composition-rules:
  may-contain: illustration / icon, heading, paragraph text, button cluster, link
  must-not-contain: form, table, list, complex content
  parent-restrictions: rendered inside the empty-region of any collection pattern
    (table body, data-list region, dashboard tile, search-and-filter results)

token-roles-consumed:
  - surface-default
  - text-default, text-muted
  - focus-ring

accessibility:
  - heading is appropriate level for context (h2 inside a section, h1 if the page is empty)
  - illustration / icon has aria-hidden=true (decorative) or aria-label (informative)
  - reduced-motion: no entrance animation

spec-author-cues:
  - first-run variant is the most important — it shapes the user's first impression
  - copy must be specific to the object: "No clients yet. Add your first client to start tracking."
    NOT "No data."
  - primary-cta on first-run should match the most common create flow available
  - no-results variant must surface the applied filters / search so users know what to clear

mapping-helpers:
  ooux-signal: every collection of any object has an empty-state for first-run
  user-stories-signal: stories that imply collection growth ("as a {role} I want to add my first {object}")
  jtbd-signal: get-started jobs
  journeys-signal: stage = "first session" / "onboarding"
```
