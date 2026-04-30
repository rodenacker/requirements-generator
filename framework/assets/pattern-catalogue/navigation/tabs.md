<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: tabs

```yaml
id: tabs
kind: layout-pattern
purpose: Partition mutually-exclusive content panels under one context, switching
  between them without a route change.

when-to-use:
  - One context has 2–6 distinct sub-views with low content overlap
  - Task is multi-view but NOT sequential (no enforced order — that's a wizard)
  - Goal is "review different facets of the same object"
  - Persona signals "switch between" or "compare aspects of"

when-not-to-use:
  - Content depends on prior selection in another tab → use multi-step-wizard
  - >6 panels → use settings-shell side-nav or accordion; tabs become overflow noise
  - Mobile-primary with text labels that don't fit horizontally → segmented-control or accordion
  - Panels short enough to coexist on one view → use a stack
  - Forms with cross-tab validation — anti-pattern (errors hide in unfocused tabs)

variants:
  - underline: label-only, content-context default
  - pill: filled-active, filter-style use
  - vertical: tab strip on the side; for >5 tabs or long labels
  - icon+label: when memorability matters
  - icon-only: compact toolbars — flips Memorability-Density to +1

default-trade-offs:
  speed-accuracy: +1
  power-simplicity: 0
  density-focus: -1
  control-automation: +1
  flexibility-consistency: 0
  memorability-density: -1

required-slots:
  - tabs: ordered list of {id, label, icon?, badge?, disabled?}
  - default-tab: id of the tab active on first render
  - panel-renderers: one renderer per tab id

states:
  default: active tab highlighted, panel rendered
  loading: panel-level loading; tab strip remains interactive
  empty: panel-level empty-state; tabs remain
  error: panel-level error; user can switch tabs to escape
  disabled-tab: individual tab disabled with tooltip explaining why
  badged: tab carries a count or status indicator

behaviours-built-in:
  - tab-click switches active panel
  - keyboard: Left/Right arrow moves between tabs; Enter/Space activates;
    Tab key exits tablist into panel content
  - manual-activation: arrow moves focus, activation requires Enter/Space
    (prevents accidental loads on keyboard scan)
  - state-preservation: panels preserve scroll/form state across switches by default
  - url-sync (optional): active-tab id mirrors to URL hash for deep-linking

composition-rules:
  may-contain (in panel): any pattern except another tabs at the same nesting level
    (one level of nesting permitted but discouraged)
  must-not-contain (in tab strip): icons-only > 6, text labels >20 chars (truncate with tooltip)
  parent-restrictions: legal inside layout-primitives, modals (M+), drawers;
    illegal inside tables, list-rows, popovers

token-roles-consumed:
  - text-default, text-muted
  - surface-default
  - border-emphasis
  - focus-ring
  - motion-fast

accessibility:
  - role=tablist + role=tab + role=tabpanel
  - aria-selected on active tab; aria-controls links each tab to its panel
  - manual-activation by default
  - reduced-motion: indicator slide disabled

spec-author-cues:
  - persona is novice + tabs > 4 → vertical variant with descriptive labels
  - §3 task requires comparing fields across panels → tabs is wrong; use side-by-side or split-view
  - any panel contains a long form → reconsider whether tabs should be a wizard
  - mobile-primary → segmented-control variant or fall back to accordion

mapping-helpers:
  ooux-signal: object with multiple "facet" attributes
    (e.g., Account → {Profile, Security, Billing, Activity})
  user-stories-signal: "as a {role} I want to see {object}'s {facet}, {facet}, and {facet}"
  jtbd-signal: job has multiple aspects the user toggles between
  journeys-signal: not a primary signal — tabs are organisation, not journey stages
```
