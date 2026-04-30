<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: table

```yaml
id: table
kind: composite-pattern
purpose: Display a homogeneous collection of records with column-aligned fields,
  sortable, optionally selectable, optionally with row actions.

when-to-use:
  - Object/collection from OOUX with ≥4 displayable fields and a need to scan/compare across records
  - Task involves "review", "compare", "filter", "approve a list of"
  - Persona signals "50 a day", "bulk", "batch", or "compliance" → strong table signal
  - Power-leaning UI for expert personas

when-not-to-use:
  - Objects with rich/hierarchical/media-heavy content (use card-grid or master-detail)
  - Typical record count <3 (use stacked list or inline detail)
  - Mobile-primary with >5 dense columns (use master-detail or cards)
  - Focus-leaning task ("one thing at a time") — wrong density

variants:
  - default: bordered rows, single-row-tall, sortable headers
  - compact: tighter row height, denser type — Density+1 / Memorability+1
  - selectable: leading checkbox column + bulk-action toolbar
  - expandable-row: each row reveals a detail panel inline
  - editable: cells editable inline — Power+2
  - virtualised: for >1k rows; "empty" state suppressed if streaming
  - sticky-header: header pinned during scroll; default-on for ≥20 rows

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: +1
  density-focus: +1
  control-automation: +1
  flexibility-consistency: 0
  memorability-density: +1

required-slots:
  - data: ordered list of records
  - columns: ordered list of {key, label, type, sortable?, width-hint?}
  - row-id-key: stable identifier per record

optional-slots:
  - row-actions: list of CTAs available per row
  - bulk-actions: list of CTAs available on selection (selectable variant)
  - empty-state: copy + optional CTA when data is empty
  - filter-bar: slot above the table
  - pagination: slot below the table

states:
  default: rows render normally
  loading: skeleton rows (count = page size); header visible
  empty: empty-state slot rendered in body; header preserved
  error: error row spanning all columns + retry CTA; header preserved
  success: not applicable (transient success belongs to the action that triggered it)
  disabled: non-interactive, columns muted, no sort/select

behaviours-built-in:
  - column-sort: click header → toggle asc/desc; one column sorted at a time
  - row-select (selectable variant): click row → select; shift-click → range
  - bulk-select-all: header checkbox toggles entire visible page
  - keyboard: arrow-keys move row focus; Space toggles selection;
    Enter triggers primary row action

composition-rules:
  may-contain: text, link, chip, badge, button (in row-actions slot), inline-icon,
    progress-inline, avatar
  must-not-contain: another table, modal, drawer, multi-line form fields
    (use expandable-row instead)
  parent-restrictions: requires layout-primitive with horizontal scroll room;
    illegal inside modals smaller than M-size

token-roles-consumed:
  - surface-default, surface-elevated
  - text-default, text-muted
  - border-subtle
  - focus-ring
  - state-selected
  - motion-fast

accessibility:
  - role=table with rowheader/columnheader semantics
  - full keyboard: row+cell navigation; sort headers reachable via Tab
  - screen-reader: announces sort-order change + selection count
  - reduced-motion: row-fade and sort-shuffle transitions disabled

spec-author-cues:
  - §3 task says "approve in batch" → selectable + bulk-actions
  - persona stakes high + bulk-action is destructive → wrap bulk-action in modal-confirmation
  - frequency = daily + density signal in §3 → compact variant
  - columns > 7 → reconsider; usually master-detail-list is the right pattern

mapping-helpers:
  ooux-signal: object with attributes-list-grid + ≥1 CTA + relationships pointing at it
  user-stories-signal: "as a {role} I want to see/review/manage {plural noun}"
  jtbd-signal: job involves "see at a glance" or "compare X vs Y"
  journeys-signal: stage = "review" or "select-from-many"
```
