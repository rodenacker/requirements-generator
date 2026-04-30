<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: command-palette

```yaml
id: command-palette
kind: surface-pattern
purpose: Keyboard-first overlay for action launching, navigation, and search;
  invoked via shortcut (typically Cmd/Ctrl-K), surfaces a fuzzy-searchable list
  of commands.

when-to-use:
  - Power-user product where keyboard speed matters
  - Many discoverable actions / destinations behind a single entry point
  - Persona uses the product daily and benefits from muscle memory
  - Apps with deep navigation that benefits from search-as-you-type

when-not-to-use:
  - Casual / occasional persona — palette stays unused
  - <20 commands / destinations — overhead exceeds benefit
  - Mobile-primary product (no keyboard shortcut paradigm)

variants:
  - actions-only: only commands, no navigation
  - navigation-only: routes only
  - blended: actions + routes + search results
  - context-aware: top results adapt to current page / selection
  - with-categories: results grouped (Actions / Pages / Recent)

default-trade-offs:
  speed-accuracy: +2
  power-simplicity: +2
  flexibility-consistency: +1
  memorability-density: -1

required-slots:
  - command-source: list of {id, label, kind, handler, keywords?}
  - shortcut: keyboard binding (typically Cmd/Ctrl-K)

optional-slots:
  - recent-commands: most-recent / most-used
  - context-section: actions specific to the current page
  - empty-state for "no matches"

states:
  default: open, search-empty showing recent / suggested
  searching: results filter as user types
  no-results: empty-state ("No matches for '{query}'")
  executing: loading indicator while command runs

behaviours-built-in:
  - shortcut opens the palette; Esc closes
  - up/down arrows navigate results; Enter executes
  - fuzzy-match scoring across label + keywords
  - on close, focus returns to the trigger element
  - recent-commands tracking is per-user

composition-rules:
  may-contain: search input, list of command items (icon + label + shortcut hint),
    category headers, empty-state
  must-not-contain: forms with multi-field input, tables
  parent-restrictions: rendered globally; not nested

token-roles-consumed:
  - surface-overlay, surface-elevated, text-default, text-muted, state-selected,
    elevation-modal, focus-ring, motion-default

accessibility:
  - role=dialog with aria-modal=true
  - search input has aria-controls pointing to the result list
  - results announce active descendant (aria-activedescendant)
  - reduced-motion: open / close animation disabled

spec-author-cues:
  - power-user product → high value; ship in MVP if persona warrants
  - context-aware variant is the strongest version but adds build cost
  - always include shortcut hint visible in the trigger (e.g., "⌘K" badge)
```
