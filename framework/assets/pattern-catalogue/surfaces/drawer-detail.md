<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: drawer-detail

```yaml
id: drawer-detail
kind: surface-pattern
purpose: A side-entering panel that shows record detail without leaving the current
  surface; the main view remains visible behind / beside it.

when-to-use:
  - User needs detail on a record while keeping list / context visible
  - Detail is medium-rich — too much for a popover, too light for a full route
  - Mobile and desktop both need to work (drawer scales gracefully)
  - Quick-glance pattern: open, scan, close, repeat

when-not-to-use:
  - Detail is light → popover (T2) is enough
  - Detail is rich and warrants a deep-link → detail-page
  - User needs to compare detail with list side-by-side — use master-detail-list
  - User edits detail substantially → drawer-form (edit-mode) or modal-form

variants:
  - right-side: enters from the right (default for desktop)
  - left-side: enters from the left (rare; usually for nav drawers)
  - bottom-sheet: enters from the bottom (mobile-primary; deferred pattern)
  - persistent: drawer can be pinned open (split-view-like behaviour)
  - non-modal: doesn't dim the background; main view stays interactive

default-trade-offs:
  speed-accuracy: +1
  power-simplicity: 0
  density-focus: 0
  control-automation: +1
  flexibility-consistency: +1
  memorability-density: 0

required-slots:
  - heading: record title at the top of the drawer
  - body: structured detail content
  - close-action: always present

optional-slots:
  - actions: top-right cluster (open in detail-page, edit, delete)
  - tabs: when detail has multiple facets
  - footer: secondary action row at the bottom

states:
  default: drawer open, detail rendered
  loading: skeleton inside drawer; outer surface unchanged
  error: error block inside drawer + retry; outer surface unchanged
  empty: rare — when drawer opens with no detail to show
  closed: drawer fully off-screen; trigger restores it

behaviours-built-in:
  - opens from a row click / CTA on the outer surface
  - Escape closes; backdrop click closes (modal variants)
  - on close, focus returns to the trigger element
  - keyboard: focus moves into the drawer on open; trap when modal
  - URL sync (optional): drawer state can mirror to URL for deep-link
  - non-modal variant: outer surface remains fully interactive

composition-rules:
  may-contain: heading, attribute-list-style content, tabs, table (small),
    data-list, action cluster, inline-edit affordances, file-upload (T3)
  must-not-contain: another drawer (no nesting), full-page error-shell,
    multi-step-wizard (use drawer-form for sequential editing)
  parent-restrictions: opened from any pattern; lives at the layout-primitive level

token-roles-consumed:
  - surface-overlay            # backdrop (modal variant)
  - surface-elevated           # drawer panel
  - text-default, text-muted
  - border-subtle
  - elevation-drawer
  - focus-ring
  - motion-default             # slide in / out

accessibility:
  - role=dialog with aria-modal=true (modal variant) or aria-modal=false (non-modal)
  - aria-labelledby points to heading
  - focus trap when modal; focus return to trigger on close
  - reduced-motion: slide animation disabled
  - persistent variant: announces state change ("Drawer pinned")

spec-author-cues:
  - if detail is read-mostly with light edits → drawer-detail
  - if detail is primarily edit → drawer-form
  - mobile-primary: drawer enters as a bottom-sheet (deferred pattern); plan accordingly
  - persistent variant when persona uses the drawer continuously (rare; check if master-detail-list is better)

mapping-helpers:
  ooux-signal: object with quick-look detail accessed from a list / table / card-grid
  user-stories-signal: "as a {role} I want to peek at / preview {object}"
  jtbd-signal: scan-and-inspect jobs
  journeys-signal: stage = "review without leaving context"
```
