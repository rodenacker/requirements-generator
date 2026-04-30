<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: popover

```yaml
id: popover
kind: surface-pattern
purpose: A small contextual surface anchored to a trigger; non-blocking; closes
  on outside click. For lightweight detail, options, or short forms.

when-to-use:
  - Lightweight detail / options that don't warrant a drawer or modal
  - Trigger-anchored content (filter dropdown, action menu, mini-form)
  - User benefits from inline / contextual placement
  - Short interactions: pick one, dismiss

when-not-to-use:
  - Content is rich → drawer-detail
  - Form has >3 fields → modal-form or drawer-form
  - User needs to interact with the content for sustained time → drawer
  - Mobile-primary if anchor positioning is fragile (use bottom-sheet)

variants:
  - menu: list of actions
  - filter-popover: filter facet detail
  - mini-form: 1–3 fields with submit
  - confirmation-popover: lightweight confirm without modal blocking
  - info-popover: read-only short content (richer than tooltip)

default-trade-offs:
  speed-accuracy: +1
  density-focus: 0

required-slots:
  - anchor: trigger element popover attaches to
  - content: what the popover shows

optional-slots:
  - heading (info / filter variants)
  - actions (menu / mini-form / confirmation variants)

states:
  default: open
  closed: hidden; anchor restores it
  loading (when fetching content): inline skeleton

behaviours-built-in:
  - opens on trigger click (or hover for info variant — discouraged for actions)
  - closes on outside click, Escape, or selecting an action
  - position: anchor-relative with collision detection
  - keyboard: Tab cycles content; Esc closes; arrow-key navigation in menu variant
  - focus: moves into popover on open (action variants); returns to trigger on close

composition-rules:
  may-contain: short text, list of actions, 1–3 form fields, filter chips
  must-not-contain: tables, multi-step content, another popover (no nesting)
  parent-restrictions: anchored to a trigger element in any pattern

token-roles-consumed:
  - surface-elevated, text-default, text-muted, border-subtle, elevation-card,
    radius-md, focus-ring, motion-fast

accessibility:
  - role=dialog (form / confirmation) or role=menu (menu variant)
  - aria-labelledby when heading present
  - focus management on open / close
  - reduced-motion: open / close animation disabled

spec-author-cues:
  - default to a popover before reaching for a modal
  - menu variant: avoid more than ~7 items (use a different surface)
  - mini-form variant should auto-close on submit success; toast confirms
```
