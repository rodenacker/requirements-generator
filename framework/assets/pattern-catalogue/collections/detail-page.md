<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: detail-page

```yaml
id: detail-page
kind: composite-pattern
purpose: Full-page view of a single record — heading + meta + structured content
  + actions; the canonical "show me everything about this one thing" surface.

when-to-use:
  - Record has rich enough detail to warrant its own route (deep-linkable, shareable)
  - Multiple sub-aspects of the record (use tabs within the detail page)
  - Actions on the record need room (multiple CTAs, comments, history)
  - Persona moves between records but each visit is substantial

when-not-to-use:
  - Detail content is light → use detail-panel (drawer or master-detail)
  - Records are scanned in tight loop with the list → use master-detail-list
  - Heavy editing as the dominant interaction → consider single-form on a normal page

variants:
  - default: heading + meta + tabbed body + actions
  - hero-detail: large media / status hero + body
  - read-only: no actions; archive / history view
  - editable: inline-edit affordances on key fields
  - with-related: side panel or footer section listing related records

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: 0
  density-focus: 0
  control-automation: +1
  flexibility-consistency: 0
  memorability-density: 0

required-slots:
  - record-id: identifier of the record being shown
  - heading: record title
  - body: structured content (typically tabs of facets, or sectioned attribute groups)

optional-slots:
  - meta-row: status / owner / dates / ids
  - primary-actions: top-right CTA cluster
  - secondary-actions: overflow menu
  - related-records: side panel or footer section
  - activity / history: audit log per record
  - breadcrumbs (convention, not pattern): parent path

states:
  default: record loaded, body rendered
  loading: skeleton heading + body
  error: error block + retry; heading hidden if 404
  not-found: 404 within the detail-page (preserves nav context)
  permission-denied: permission-gate convention surfaces the reason
  unsaved-changes (editable variant): leaving the page prompts confirmation
  archived / read-only: actions hidden; banner explains why

behaviours-built-in:
  - URL is the deep-link to this record
  - back-button returns to the prior list / search context
  - keyboard: action cluster reachable; tabs navigate facets
  - inline-edit (editable variant): per-field commit on blur or per-field commit button
  - print-friendly: detail-page degrades to print-shell cleanly when printed

composition-rules:
  may-contain: tabs (for facets), attribute-list-style sections, table (related records),
    data-list, chart (small), notification-banner, action-cluster, comment-thread
    (when added), file-upload (when added)
  must-not-contain: another shell, another detail-page (no nesting),
    full-page error-shell (states above handle errors locally)
  parent-restrictions: typically routed at /{object}/:id within app-shell

token-roles-consumed:
  - surface-default, surface-elevated
  - text-default, text-muted
  - border-subtle
  - state-success, state-warning, state-danger    # status indicators
  - focus-ring
  - elevation-card             # for floating action panels

accessibility:
  - landmark: main wraps the detail
  - heading is h1 of the page; record title is the truth
  - tabs (when used) follow the tabs pattern's accessibility rules
  - permission denial surfaces with clear explanation, not silent 404
  - reduced-motion: tab transitions disabled

spec-author-cues:
  - if record has multiple distinct facets (≥3) → tabs in the body slot
  - if persona triages many records sequentially → master-detail-list might be the better outer pattern
  - editable variant only when in-place edit is genuinely the dominant interaction;
    otherwise, view-then-modal-form-edit is simpler
  - related-records section feeds OOUX relationships → align with §4 of the spec

mapping-helpers:
  ooux-signal: top-level object with rich attribute set + relationships
  user-stories-signal: "as a {role} I want to see / open / view {object}"
  jtbd-signal: deep-inspect / decide-on jobs
  journeys-signal: stage = "review one item in depth"
```
