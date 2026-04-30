<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: settings-shell

```yaml
id: settings-shell
kind: layout-primitive
purpose: Sectioned navigation on the left + section content on the right;
  the canonical shell for preferences, account, team, billing, and any sectioned
  configuration surface.

when-to-use:
  - Preferences / account / profile / team / billing / integrations surfaces
  - Any cluster of forms grouped into 3+ sections that the user navigates between freely
  - Configuration surfaces inside the authenticated app

when-not-to-use:
  - Single settings form (use single-form on a normal app-shell page)
  - Sequential setup (use multi-step-wizard or auth-flow-shell)
  - User-facing destinations (this is for management, not consumption)

variants:
  - default: vertical section nav left, section content right
  - grouped: section-nav with category headers (e.g., "Account", "Workspace", "Billing")
  - tabbed: top tabs instead of side nav (use when sections ≤4 and short labels)
  - mobile-stacked: section nav becomes a list page; selecting a section navigates to its content

default-trade-offs:
  speed-accuracy: 0
  power-simplicity: -1
  density-focus: -1
  control-automation: +1
  flexibility-consistency: +1
  memorability-density: 0

required-slots:
  - section-nav: ordered list of {id, label, icon?, badge?}
  - section-content: routed pane for the active section
  - heading: section title at the top of the content pane

optional-slots:
  - description: subheading beneath the section title
  - save-bar: sticky save / discard footer (when sections have unsaved changes)
  - search: filter sections by label

states:
  default: section selected, content rendered
  loading: content-pane skeleton; section-nav remains interactive
  error: content-pane error; section-nav remains interactive
  unsaved-changes: save-bar visible; navigating away prompts confirmation
  empty (per section): some sections legitimately have nothing to show until configured

behaviours-built-in:
  - active-section highlight in section-nav
  - URL reflects active section (deep-link friendly)
  - unsaved-changes prompt blocks navigation unless confirmed
  - keyboard: arrow keys navigate sections; Enter activates; Tab cycles content
  - mobile-stacked: back-link returns to section list

composition-rules:
  may-contain (in section-content): single-form (most common), table, data-list,
    notification-banner, repeater, file-upload, attribute-list-style displays
  must-not-contain: another shell, multi-step-wizard (settings are non-sequential)
  parent-restrictions: typically lives inside an app-shell as a routed section
    ("/settings/*"), not at the very top level

token-roles-consumed:
  - surface-default, surface-elevated
  - text-default, text-muted
  - state-selected
  - border-subtle
  - elevation-toast            # for save-bar
  - focus-ring

accessibility:
  - landmark: nav (section-nav) + main (content)
  - heading hierarchy resets per section: section title is h1 of the section pane
  - unsaved-changes prompt is an accessible dialog, not a browser confirm
  - reduced-motion: pane transition disabled

spec-author-cues:
  - if §3 has 3+ settings-style tasks → use this shell, not a flat page
  - if §3 has only one settings form → use single-form on a normal app-shell page; this pattern is overkill
  - tabbed variant fits naturally for ≤4 short section labels; default vertical scales further
  - if any section is sequential (e.g., onboarding-style team setup) → that section uses multi-step-wizard inside the content pane

mapping-helpers:
  ooux-signal: object "user account" / "workspace" / "team" with sub-aspects
  user-stories-signal: "as a user I want to manage my {account / preferences / team / billing}"
  jtbd-signal: "configure-the-product" or "manage-my-account" jobs
  journeys-signal: not a primary signal; settings are typically off-journey
```
