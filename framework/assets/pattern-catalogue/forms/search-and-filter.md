<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: search-and-filter

```yaml
id: search-and-filter
kind: composite-pattern
purpose: Search input + filter facets + result region; the canonical "narrow down
  a collection" surface, used above tables, data-lists, and card-grids.

when-to-use:
  - Collection size makes scanning impractical
  - Multiple meaningful filter dimensions (status, owner, date, tag, etc.)
  - Persona returns to the same collection often, with varying intent
  - Result counts vary widely based on filters

when-not-to-use:
  - Collection is small enough to scan (<50 items typical)
  - Single filter dimension → just a chip-bar or segmented-control
  - Very expert / specific querying needs → query-builder (T3, deferred)

variants:
  - filters-inline: filter chips in a horizontal row above results
  - filters-sidebar: filters in a left rail (more facets, more space)
  - filters-popover: each filter opens a popover; compact bar
  - search-only: no filters, just a search input + results
  - filter-pills: applied filters render as removable pills above results

default-trade-offs:
  speed-accuracy: +1
  power-simplicity: +1
  density-focus: 0
  control-automation: +1
  flexibility-consistency: 0
  memorability-density: 0

required-slots:
  - search-input
  - filters: ordered list of {id, label, kind: enum/multi-enum/date-range/range/boolean,
    options-source}
  - results-region: a table / data-list / card-grid that renders filtered + searched data
  - result-count

optional-slots:
  - sort-control: sort dimension + direction
  - saved-views: per-user saved filter combinations
  - clear-all action
  - applied-filters pills row

states:
  default: results render
  searching: results region shows loading state
  no-results: empty-state ("No matches" + Clear filters CTA)
  error: results region error + retry
  filtering-loading: filter UI remains interactive while results re-fetch

behaviours-built-in:
  - search debounce (typically 300ms; configurable)
  - filters apply as user changes them (no explicit "apply" button by default)
  - URL sync: search + filter state encoded in URL params (deep-link friendly)
  - clear-all resets search + filters to default
  - keyboard: search input gets focus on / shortcut (when configured);
    Tab through filters
  - applied-filter pill removable via click or Backspace when focused

composition-rules:
  may-contain (results-region): table, data-list, card-grid, search-results-page (P2)
  must-not-contain: forms with multi-step state, modal (use popover for filter detail)
  parent-restrictions: typically a top-level routed surface in app-shell or
    embedded in master-detail-list as the list-side filter

token-roles-consumed:
  - surface-default, surface-elevated
  - text-default, text-muted
  - state-selected             # active filter values
  - border-subtle
  - focus-ring
  - motion-fast

accessibility:
  - search input has a visible label or aria-label
  - filter changes announce result count change (aria-live polite)
  - applied-filter pills are focusable and removable via keyboard
  - reduced-motion: result-region fade transitions disabled

spec-author-cues:
  - count of meaningful filter dimensions decides variant: 1–3 inline; 4+ sidebar
  - if persona uses the same filter combo repeatedly → saved-views slot
  - high-frequency persona → search-input shortcut convention (`/` or `cmd-k`)
  - if collection is paginated → ensure search/filter changes reset to page 1

mapping-helpers:
  ooux-signal: top-level collection of an object, with multiple filterable attributes
  user-stories-signal: "as a {role} I want to find / filter / search {object}s by {dimension}"
  jtbd-signal: find-the-needle jobs
  journeys-signal: stage = "narrow down" or "decide-from-many"
```
