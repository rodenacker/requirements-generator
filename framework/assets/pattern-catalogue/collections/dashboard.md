<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: dashboard

```yaml
id: dashboard
kind: composite-pattern
purpose: A composition of KPI tiles, summary cards, charts, and recent-items lists
  on a single surface; the canonical "at-a-glance" home for a role or domain.

when-to-use:
  - Persona returns to the same surface as the entry point of every session
  - Multiple data dimensions worth glancing at simultaneously (vs going to each one)
  - Quality signals "at a glance", "dense", "what changed", "what needs attention"
  - Role-specific home (per-role dashboards are common)

when-not-to-use:
  - Persona enters with a specific task in mind (use the task surface directly)
  - Single metric matters → kpi-tile on a normal page is enough
  - Data depth requires drilling — dashboard becomes a teaser; ensure each tile links to its detail surface

variants:
  - default: fixed grid of tiles
  - configurable: user can add / remove / reorder tiles (Power-leaning, big build)
  - role-scoped: different dashboard layouts per role
  - time-scoped: top filter (today / week / month) re-scopes all tiles
  - minimal: ≤4 tiles, no chrome — for narrow personas

default-trade-offs:
  speed-accuracy: +1
  power-simplicity: +1
  density-focus: +2
  control-automation: 0
  flexibility-consistency: 0
  memorability-density: +1

required-slots:
  - tiles: ordered list of {id, kind, span, content-renderer}
  - heading: dashboard title

optional-slots:
  - time-filter
  - role-filter
  - last-updated indicator
  - refresh action
  - drill-down anchors (each tile typically links to its detail surface)

states:
  default: all tiles render
  loading: each tile shows its own skeleton (per-tile, not page-level)
  partial-error: some tiles error individually, others succeed
    — dashboard does NOT fail page-level on one tile's failure
  empty (per tile): tiles handle their own empty-state per their kind
  stale: last-updated indicator shows age + refresh CTA

behaviours-built-in:
  - per-tile loading / error isolation (one tile failing must not break the rest)
  - drill-down: clicking a tile navigates to its detail surface
  - time-filter: changes the scope of every tile that subscribes to it
  - keyboard: tiles are tabbable; Enter activates drill-down

composition-rules:
  may-contain (per tile): kpi-tile, chart, summary-card, data-list (recent items),
    table (small), notification-banner, link-cluster
  must-not-contain (per tile): multi-step-wizard, forms, modal-confirmation;
    a dashboard is a read surface
  parent-restrictions: typically a top-level routed page in app-shell

token-roles-consumed:
  - surface-default, surface-elevated
  - text-default, text-muted
  - border-subtle
  - state-selected, state-success, state-warning, state-danger
  - elevation-card             # per-tile elevation
  - focus-ring
  - radius-md
  - motion-fast

accessibility:
  - landmark: main wraps the dashboard
  - each tile has a clear heading (h2) — dashboards are scanned by heading
  - time-filter changes are announced (aria-live polite)
  - reduced-motion: chart-entry animations disabled

spec-author-cues:
  - if §3 has "what's the state of X" or "what needs my attention" goals → dashboard
  - if persona is novice and tile count > 6 → reduce; dashboards over-tile fast
  - role-scoped variant when §5 role-gating shows distinct role-conditional content
  - configurable variant is a meaningful build — only when persona is power-user and uses dashboard daily

mapping-helpers:
  ooux-signal: meta-object summarising other objects (e.g., "Workspace", "Today")
  user-stories-signal: "as a {role} I want to see the state / status / activity of {domain}"
  jtbd-signal: orient-myself / what-needs-attention jobs
  journeys-signal: journey-stage = "session entry" / "morning check-in"
```
