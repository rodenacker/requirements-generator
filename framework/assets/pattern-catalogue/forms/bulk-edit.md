<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: bulk-edit

```yaml
id: bulk-edit
kind: composite-pattern
purpose: Select multiple records, then apply a change or action to all selected
  in one operation; the canonical Power-leaning batch pattern.

when-to-use:
  - Persona signals "bulk", "batch", "50 a day", "in one go"
  - Collection has many records of the same kind
  - Common operations apply uniformly across selections (status change, delete, assign)
  - Power-user persona

when-not-to-use:
  - Operations vary per record → individual edits beat bulk
  - Selection is small (≤3) — individual is faster
  - Operations have different validation per record (bulk hides errors)

variants:
  - toolbar-on-select: action toolbar appears when ≥1 row selected
  - inline-action: per-row action bar; bulk is a multiplier
  - bulk-form: drawer / modal form applying changes to N items
  - bulk-confirmation: bulk action behind a modal-confirmation

default-trade-offs:
  speed-accuracy: +1
  power-simplicity: +2
  control-automation: +1

required-slots:
  - selection: list of selected record ids
  - actions: list of {label, kind: change/delete/assign/etc., handler}
  - selection-count display

optional-slots:
  - select-all (within page or all matching filters)
  - clear-selection
  - filter-aware-select-all ("Select all 250 matching")

states:
  default: no selection, toolbar hidden
  selecting: ≥1 row selected, toolbar visible with count
  applying: action in progress; selection preserved; toolbar shows progress
  partial-success: some succeeded, some failed; per-id failure list shown
  error: action failed entirely; selection preserved; user can retry
  cleared: selection emptied; toolbar hidden

behaviours-built-in:
  - selection persists across pagination (when supported)
  - destructive actions wrap in modal-confirmation
  - keyboard: shift-click range, cmd/ctrl-click toggle, Esc clears selection
  - on success → toast announcing count + Undo (when reversible)

composition-rules:
  may-contain: bulk-action toolbar, action buttons, selection-count, modal-confirmation,
    drawer-form (bulk-form variant)
  must-not-contain: another bulk-edit
  parent-restrictions: lives above a table (selectable variant), data-list (leading-checkbox),
    or card-grid (selectable)

token-roles-consumed:
  - surface-elevated, text-default, state-selected, state-danger, focus-ring,
    elevation-toast

accessibility:
  - selection count announced on change (aria-live polite)
  - destructive actions visually + semantically distinct
  - cleared selection announces "Selection cleared"
  - reduced-motion: toolbar slide-in disabled

spec-author-cues:
  - if persona is "50 a day" or "compliance" → bulk-edit is high-value
  - filter-aware-select-all only when collections often exceed visible page
  - partial-success state must surface failures clearly; never silently drop them
```
