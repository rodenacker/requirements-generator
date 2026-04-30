<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: app-shell-with-sidebar

```yaml
id: app-shell-with-sidebar
kind: layout-primitive
purpose: Vertical primary navigation on the left, main content area on the right;
  the dominant shell for SaaS / internal tools / admin dashboards.

when-to-use:
  - Authenticated app with ≥4 top-level destinations
  - Navigation persists across the whole product (not flow-specific)
  - Desktop-first or responsive product (sidebar collapses on mobile)
  - Power-user / expert / daily-frequency persona signals

when-not-to-use:
  - Public / marketing surfaces (use marketing-shell)
  - Single-task linear flows (use centered-form or auth-flow-shell)
  - Mobile-primary product where sidebar collapse becomes the dominant state (consider top-nav variants)
  - <3 destinations — sidebar is overhead

variants:
  - default: expanded labels, icons, optional grouping headers
  - compact: icon-only, hover/click reveals labels
  - collapsible: user toggles between expanded and compact
  - grouped: section headers separating destination clusters
  - with-secondary: sidebar + a secondary nav rail (e.g., workspace switcher)

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: +1
  density-focus: 0
  control-automation: +1
  flexibility-consistency: +1
  memorability-density: +1

required-slots:
  - brand: logo / wordmark slot at top
  - primary-nav: list of top-level destinations
  - main-content: the routed page region
  - user-menu: account / signout entry point

optional-slots:
  - secondary-nav: workspace / org / project switcher
  - search: global search anchor
  - notifications: bell / inbox anchor
  - footer: legal / version / help link cluster
  - announcement: dismissible system banner

states:
  default: sidebar visible, main content scrolls
  loading: main-content area shows skeleton; sidebar always interactive
  error: main-content full-area error; sidebar always interactive (escape route)
  collapsed: sidebar in icon-only state (compact variant)
  mobile: sidebar slides in over content as a drawer

behaviours-built-in:
  - active-route highlight on the matching nav entry
  - collapse / expand toggle persists per user
  - keyboard: tab cycles through nav entries; Enter activates
  - mobile drawer dismisses on outside tap and on Escape
  - focus trapped inside drawer when open on mobile

composition-rules:
  may-contain (in main-content): any pattern except marketing-shell or another app-shell
  must-not-contain (in sidebar): forms, tables, charts; sidebar is for navigation only
  parent-restrictions: top-level — this IS the page; cannot be nested

token-roles-consumed:
  - surface-default            # main background
  - surface-elevated           # sidebar background
  - surface-overlay            # mobile drawer
  - text-default, text-muted   # nav labels active vs inactive
  - state-selected             # active route indicator
  - border-subtle              # sidebar / main divider
  - elevation-drawer           # mobile drawer shadow
  - motion-default             # collapse / expand
  - focus-ring

accessibility:
  - landmark: nav role on sidebar, main role on content area
  - skip-link to main-content as the first focusable element
  - mobile drawer manages focus trap and aria-modal correctly
  - reduced-motion: collapse animation disabled

spec-author-cues:
  - if §3 has ≥6 destinations and persona is novice → grouped variant with section headers
  - if persona is daily / expert and screen real estate matters → compact or collapsible variant
  - if mobile-primary brief → consider app-shell-with-topnav instead; this pattern's mobile fallback is a drawer, not a first-class layout

mapping-helpers:
  ooux-signal: many top-level objects (≥4) each warranting its own destination
  user-stories-signal: stories cluster around stable destinations rather than linear flows
  jtbd-signal: persona returns repeatedly to perform varied jobs
  journeys-signal: journey spans multiple sessions over time (vs single linear arc)
```
