<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: master-detail-list

```yaml
id: master-detail-list
kind: composite-pattern
purpose: A list / table on one side and a detail pane on the other; selecting
  a row in the list updates the detail without a route change.

when-to-use:
  - Records are scanned-and-inspected repeatedly within a session (inbox, queue, ticket list)
  - Detail pane content is meaningful but doesn't warrant a full route
  - Persona stays in "browse + inspect + act" loop rather than "browse → leave → return"
  - Desktop-primary or wide-tablet; works on mobile via stacked variant

when-not-to-use:
  - Detail content is sparse — list alone is enough
  - Detail content is rich enough to need its own route (use detail-page)
  - Mobile-primary product where the split layout collapses always
    (use list → detail-page navigation instead)

variants:
  - default: list left, detail right, fixed split
  - resizable-split: user drags the divider
  - stacked-mobile: on narrow viewports, list and detail become two routes
  - inline-detail: detail expands inline beneath the selected row (table expandable-row variant)
  - drawer-detail: list left, detail enters as a drawer (when split would be too narrow)

default-trade-offs:
  speed-accuracy: +1
  power-simplicity: +1
  density-focus: 0
  control-automation: +1
  flexibility-consistency: 0
  memorability-density: +1

required-slots:
  - list: a table or data-list pattern
  - detail-renderer: function that renders the detail pane for the selected record
  - selected-id: id of the currently-selected record

optional-slots:
  - filter-bar: above the list
  - detail-actions: CTAs in the detail header
  - empty-detail: placeholder when no record is selected

states:
  default: list visible, no selection — empty-detail rendered
  selected: list shows selected row highlighted, detail rendered
  detail-loading: list interactive, detail-pane skeleton
  detail-error: list interactive, detail-pane error + retry
  list-loading: list shows skeleton rows; detail unchanged
  list-empty: empty-state in the list region; detail unchanged
  unsaved-changes (in detail): switching list selection prompts confirmation

behaviours-built-in:
  - selecting a row updates the detail pane and the URL (deep-link friendly)
  - keyboard: arrow-keys move list selection (auto-loads detail);
    Tab moves focus into detail
  - mobile / stacked: tapping a row navigates; back-button returns to list
  - unsaved-changes prompt blocks selection change until confirmed

composition-rules:
  may-contain (list slot): table, data-list, card-grid (rare)
  may-contain (detail slot): attribute-list-style content, tabs (for facets),
    actions, related-records lists, inline-edit affordances
  must-not-contain: another master-detail-list (no nesting)
  parent-restrictions: typically a top-level routed page within app-shell

token-roles-consumed:
  - surface-default, surface-elevated
  - text-default, text-muted
  - border-subtle              # split divider
  - state-selected             # selected row in list
  - focus-ring
  - motion-fast                # detail-pane transition

accessibility:
  - landmark: nav (list) + main (detail) within a single route
  - selected-row uses aria-current="true"
  - focus order: list → detail; back-tab returns
  - mobile / stacked: list and detail are separate routes — back-button restores selection
  - reduced-motion: detail-pane transition disabled

spec-author-cues:
  - §4 object presentation has "browse + inspect" loop → this pattern beats list-then-detail-page
  - persona daily / batch-processing → selectable variant in the list slot for bulk-actions
  - if detail commonly takes the whole viewport (rich, deep) → use detail-page navigation instead
  - if list rows are sparse / image-heavy → use card-grid in the list slot

mapping-helpers:
  ooux-signal: object with rich detail attributes accessed in tight loop with the list
  user-stories-signal: "as a {role} I want to review / triage / process {object}s"
  jtbd-signal: triage / queue / inbox jobs
  journeys-signal: stage = "review and act on each item"
```
