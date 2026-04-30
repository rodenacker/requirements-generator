<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: app-shell-with-topnav

```yaml
id: app-shell-with-topnav
kind: layout-primitive
purpose: Horizontal primary navigation across the top, main content area below;
  lighter shell for consumer-facing apps and products with few top-level destinations.

when-to-use:
  - Authenticated app with 2–6 top-level destinations
  - Consumer-facing product with brand presence in the header
  - Mobile-primary or responsive product (top-nav collapses to hamburger cleanly)
  - Content-heavy pages where vertical real estate matters

when-not-to-use:
  - >6 destinations (sidebar handles density better)
  - Power-user / dashboard tools where compact persistent nav matters (use sidebar)
  - Marketing pages (use marketing-shell)

variants:
  - default: logo left, nav center or left, user-menu right
  - sticky: nav pinned to top during scroll
  - transparent: nav transparent over a hero, solidifies on scroll (consumer-facing)
  - with-search: search input embedded in the nav bar
  - with-tabs: secondary tabs row beneath the primary nav

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: -1
  density-focus: -1
  control-automation: 0
  flexibility-consistency: +1
  memorability-density: 0

required-slots:
  - brand
  - primary-nav
  - main-content
  - user-menu

optional-slots:
  - search
  - notifications
  - secondary-nav: tabs row beneath primary nav
  - announcement
  - footer

states:
  default: top-nav visible, main scrolls
  loading: main-content skeleton; top-nav always interactive
  error: main-content error; top-nav always interactive
  mobile: hamburger toggles a slide-down or drawer menu
  scrolled: sticky variant compacts (smaller logo, denser spacing)

behaviours-built-in:
  - active-route highlight on the matching nav entry
  - mobile menu open / dismiss on outside tap or Escape
  - sticky-on-scroll behaviour (sticky variant)
  - keyboard: tab through nav, Enter activates
  - focus trap in mobile menu when open

composition-rules:
  may-contain (in main-content): any pattern except another shell
  must-not-contain (in top-nav): forms, tables; top-nav is for navigation + brand only
  parent-restrictions: top-level — cannot be nested

token-roles-consumed:
  - surface-default, surface-elevated
  - text-default, text-muted
  - state-selected
  - border-subtle
  - motion-default
  - focus-ring
  - elevation-toast            # for sticky-variant scroll shadow

accessibility:
  - landmark: nav + main
  - skip-link to main-content
  - mobile menu: focus trap, aria-modal, dismiss on Escape
  - reduced-motion: sticky compact transition disabled

spec-author-cues:
  - mobile-primary persona → this pattern beats sidebar
  - if destinations grow past 6 → restructure into sidebar or use mega-menu within topnav
  - consumer-facing brief with strong brand → transparent variant on landing-style pages
  - if §3 task density per route is high (lots of tools per page) → consider sidebar for the working area

mapping-helpers:
  ooux-signal: few top-level objects, each with rich detail pages
  user-stories-signal: stories center on consuming/browsing rather than producing/managing
  jtbd-signal: occasional or self-service personas
  journeys-signal: short, focused sessions
```
