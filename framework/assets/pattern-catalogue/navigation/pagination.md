<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: pagination

```yaml
id: pagination
kind: layout-pattern
purpose: Page-by-page navigation through a long collection that exceeds what fits
  in a single render.

when-to-use:
  - Collections with >50 items in typical use
  - Result regions for search-and-filter where total count matters
  - Tables / data-lists / card-grids with large datasets
  - Predictable, repeatable navigation needed (vs continuous scroll)

when-not-to-use:
  - Collections that fit in one render (just show them all)
  - Streaming / chronological feeds where infinite-scroll fits the mental model better
  - Highly-curated short lists (<50 items)

variants:
  - numbered: 1, 2, 3, …, N — for known-bounded collections
  - prev-next: arrows + current-position indicator — for unknown-bounded
  - load-more: explicit button appends next page in place
  - jump-to-page: input field + go button (very large datasets)
  - cursor: opaque cursor tokens (API-driven, no page numbers)

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: 0
  density-focus: 0
  control-automation: +1
  flexibility-consistency: 0
  memorability-density: 0

required-slots:
  - current-page or current-cursor
  - on-change: handler that loads the requested page
  - has-next, has-previous: boundary signals

optional-slots:
  - total-count: displayed as "{n} results" or "{x}–{y} of {n}"
  - page-size-selector: 10 / 25 / 50 / 100 per page
  - jump-to-page input

states:
  default: pagination controls render; current page highlighted
  loading: controls disabled while next page loads
  boundary: previous / next disabled at first / last page
  empty: pagination hidden when collection is empty (empty-state takes over)

behaviours-built-in:
  - URL sync: current page reflects in the URL (?page=N or cursor token)
    so back-button and deep-link work
  - page-size change resets to first page
  - keyboard: arrow keys move between page numbers; Enter activates;
    Home/End jump to first/last (numbered variant)
  - load-more variant: button shows progress while fetching

composition-rules:
  may-contain: page-number atoms, prev/next buttons, page-size dropdown,
    total-count text
  must-not-contain: filters, sort controls (those belong in search-and-filter or table header)
  parent-restrictions: lives beneath the collection it paginates
    (table, data-list, card-grid, search-results)

token-roles-consumed:
  - text-default, text-muted
  - state-selected
  - border-subtle
  - focus-ring

accessibility:
  - role=navigation with aria-label="Pagination"
  - current page has aria-current="page"
  - prev / next buttons announce their target ("Go to page 4")
  - disabled buttons set aria-disabled, do not remove from tab order silently

spec-author-cues:
  - if dataset is unbounded or streaming → cursor or load-more variant
  - if user needs to share a deep-link to a specific result → numbered variant (URL-friendly)
  - if persona is mobile-primary → load-more variant beats numbered (touch-friendly)
  - keep page-size options consistent across paginated collections in the same product

mapping-helpers:
  ooux-signal: not a primary signal; pagination is an attribute of any object collection
  user-stories-signal: "as a {role} I want to browse / search / find within {collection}"
  jtbd-signal: collection-browsing job
  journeys-signal: stage = "review" or "select-from-many"
```
