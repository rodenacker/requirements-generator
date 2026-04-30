<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: data-list

```yaml
id: data-list
kind: composite-pattern
purpose: Stacked list of records with primary + secondary text per row, optional
  trailing meta or action; lighter than a table, denser than a card-grid.

when-to-use:
  - Records have 1–3 fields the user actually scans
  - Mobile-primary or responsive products
  - Records are heterogeneous in length / shape (table's column-alignment hurts)
  - Casual browsing (vs comparison or batch action)

when-not-to-use:
  - Records have ≥4 comparable fields per row → use table
  - Records are visually rich (images, media) → use card-grid
  - User needs to compare across rows → table is built for that

variants:
  - default: primary line + secondary line + optional trailing meta
  - leading-avatar: avatar / icon on the left of each row
  - leading-checkbox: selectable; pairs with bulk-action toolbar
  - trailing-action: row-end CTA per row
  - grouped: section headers (e.g., date groups, alphabetical groups)
  - dividerless: no row dividers, more breathing room

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: -1
  density-focus: 0
  control-automation: 0
  flexibility-consistency: 0
  memorability-density: 0

required-slots:
  - data: ordered list of records
  - row-renderer: how each record renders (primary/secondary/avatar/action slots)
  - row-id-key: stable identifier per record

optional-slots:
  - bulk-actions: when leading-checkbox variant is in use
  - empty-state
  - pagination or infinite-scroll

states:
  default: rows render
  loading: skeleton rows
  empty: empty-state replaces the list
  error: error block with retry
  selected (per row): row highlighted

behaviours-built-in:
  - row-tap navigates to detail (or selects, in selectable variant)
  - keyboard: arrow keys navigate rows; Enter activates primary action
  - long-press (mobile) opens row-action menu
  - swipe-actions (mobile): optional swipe-to-archive / delete

composition-rules:
  may-contain (in row): avatar, icon, text, chip, badge, button (in trailing slot),
    progress-inline
  must-not-contain (in row): forms, multi-line input, charts, nested lists
  parent-restrictions: legal in any layout-primitive, in master-detail-list,
    in modal (M+), in drawer

token-roles-consumed:
  - surface-default
  - text-default, text-muted
  - border-subtle
  - state-selected
  - focus-ring

accessibility:
  - role=list / role=listitem
  - selected row uses aria-current="true"
  - keyboard navigation is row-level, not cell-level (different from table)
  - reduced-motion: swipe-action animations disabled

spec-author-cues:
  - mobile-primary brief → data-list almost always beats table for collections
  - group-by signal in requirements (e.g., "by date", "by status") → grouped variant
  - if row content grows beyond two lines → consider card-grid
  - if user wants to multi-select → leading-checkbox variant + bulk-actions

mapping-helpers:
  ooux-signal: object with 1–3 displayable attributes per record
  user-stories-signal: "as a {role} I want to see my recent / pending / assigned {object}s"
  jtbd-signal: lightweight browsing or mobile-context jobs
  journeys-signal: stage = "scan recent items"
```
