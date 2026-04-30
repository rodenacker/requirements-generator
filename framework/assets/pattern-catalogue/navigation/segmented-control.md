<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: segmented-control

```yaml
id: segmented-control
kind: layout-pattern
purpose: 2–4 mutually-exclusive options rendered as a single horizontal control;
  a compact, mobile-friendly alternative to tabs.

when-to-use:
  - 2–4 mutually-exclusive options with short labels
  - Mobile-primary surface where tabs would feel heavy
  - Filter-style toggling (e.g., "All / Mine / Team")
  - View-mode switching (e.g., "List / Grid")

when-not-to-use:
  - >4 options → use tabs
  - Long labels that won't fit horizontally
  - Selection should not change content immediately (use radio buttons in a form)
  - Each option needs distinct content in its own panel structure (use tabs)

variants:
  - default: equal-width segments
  - icon-only: very compact; pairs with tooltips
  - icon+label: emphasises memorability
  - filter-style: visually subordinate; for filter chips above results

default-trade-offs:
  speed-accuracy: +1
  density-focus: 0
  flexibility-consistency: +1

required-slots:
  - options: ordered list of {id, label, icon?, disabled?}
  - selected: id of the active option

optional-slots:
  - on-change handler

states:
  default: one option selected
  loading: control disabled, value preserved
  disabled-option: individual options can be disabled

behaviours-built-in:
  - click selects an option; one selection at a time
  - keyboard: arrow keys move selection within the control; activates on focus by default
  - URL sync (optional)

composition-rules:
  may-contain: text label, icon, badge (small)
  must-not-contain: complex content
  parent-restrictions: legal in any container; common above results, in toolbars,
    inside dashboard tiles

token-roles-consumed:
  - surface-elevated, text-default, text-muted, state-selected, border-subtle,
    focus-ring, motion-fast

accessibility:
  - role=radiogroup with role=radio per option (or tablist if changing panels)
  - aria-checked on selected option
  - reduced-motion: indicator slide disabled

spec-author-cues:
  - mobile-primary + ≤4 options → segmented-control beats tabs
  - if total label width might overflow → switch to tabs or pills
  - icon-only variant always pairs with tooltip for label discoverability
```
