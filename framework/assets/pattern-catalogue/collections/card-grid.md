<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: card-grid

```yaml
id: card-grid
kind: composite-pattern
purpose: Visually-rich record grid; each card carries image / icon + meta + CTA.
  The "browse-and-pick" surface for content where visuals matter.

when-to-use:
  - Records have meaningful visual content (image, thumbnail, illustration)
  - Browsing / discovery is the primary task, not comparison
  - Mobile and desktop both render naturally (cards reflow)
  - Marketing-style or media-style products

when-not-to-use:
  - Records are scanned for cross-comparison → table
  - Records are mostly text → data-list
  - Density matters more than richness → table

variants:
  - default: image header + title + meta + CTA
  - dense: smaller cards, more per row
  - feature-tile: large hero card + smaller siblings
  - product-card: with price / rating / status (e-commerce shape)
  - status-card: with prominent state indicator (kanban-like)

default-trade-offs:
  speed-accuracy: 0
  density-focus: -1
  control-automation: 0

required-slots:
  - data: ordered list of records
  - card-renderer: how each card renders (image / heading / meta / actions)

optional-slots:
  - filter-bar
  - sort-control
  - pagination
  - empty-state

states:
  default: cards render
  loading: skeleton cards
  empty: empty-state replaces grid
  error: error block with retry
  selected (per card): selectable variant for bulk-action

behaviours-built-in:
  - card-tap navigates to detail (or selects in selectable variant)
  - keyboard: arrow keys navigate the grid; Enter activates
  - responsive: cards-per-row adapts to viewport

composition-rules:
  may-contain (per card): image, heading, paragraph, chip / badge, button, icon
  must-not-contain (per card): table, dashboard, multi-step-wizard
  parent-restrictions: legal in any layout-primitive

token-roles-consumed:
  - surface-default, surface-elevated, text-default, text-muted, border-subtle,
    elevation-card, radius-md, focus-ring

accessibility:
  - role=list / role=listitem (cards as items)
  - keyboard navigation; primary CTA reachable per card
  - alt-text on card images
  - reduced-motion: hover / entrance animations disabled

spec-author-cues:
  - visual-rich brief (catalogue, gallery, listings) → card-grid
  - feature-tile variant when one card should dominate (campaign / promotion)
  - product-card variant for e-commerce briefs
```
