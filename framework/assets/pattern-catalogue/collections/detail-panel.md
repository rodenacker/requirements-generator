<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: detail-panel

```yaml
id: detail-panel
kind: composite-pattern
purpose: Inline or side detail for a selected record — lighter than a detail-page,
  more persistent than a popover. Common as the right-side pane of master-detail-list
  or as an inline-expanded row.

when-to-use:
  - Detail accompanies a list / table within the same surface
  - Content is moderate (more than popover, less than detail-page)
  - User benefits from staying in context (no route change)

when-not-to-use:
  - Detail rich enough for its own route → detail-page
  - Detail trivial enough for a tooltip / popover
  - Edit-heavy interaction → drawer-form or modal-form

variants:
  - side-panel: inside master-detail-list (default)
  - inline-expanded: inline-row expansion below the selected row
  - sticky-bottom: fixed at viewport bottom (mobile; rare)

default-trade-offs:
  speed-accuracy: +1
  density-focus: 0
  flexibility-consistency: +1

required-slots:
  - record-id
  - heading
  - body

optional-slots:
  - actions (top-right cluster)
  - tabs (for facets)
  - related-records summary
  - link-to-detail-page ("Open full view")

states:
  default: rendered
  loading: skeleton
  error: error block + retry
  empty: placeholder (no record selected)

behaviours-built-in:
  - selection in the parent list updates the panel content
  - keyboard: focus follows selection; Tab moves into panel
  - URL sync (optional): selected record id in URL

composition-rules:
  may-contain: heading, attribute-list-style content, tabs, data-list, action cluster
  must-not-contain: another detail-panel, full-page error-shell, multi-step-wizard
  parent-restrictions: lives within master-detail-list, table (expandable-row),
    dashboard tile

token-roles-consumed:
  - surface-elevated, text-default, text-muted, border-subtle, elevation-card,
    focus-ring

accessibility:
  - heading is h2 (or h3 inside an expanded row)
  - aria-live polite for content swap on selection
  - reduced-motion: expand animation disabled

spec-author-cues:
  - if detail length grows beyond ~one screen → use detail-page or drawer-detail
  - link-to-detail-page is helpful when the panel is a teaser; users can deepen
```
