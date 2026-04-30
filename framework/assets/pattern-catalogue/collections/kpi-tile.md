<!-- ROLE: asset (pattern). v7b-specific. -->

# Pattern: kpi-tile

```yaml
id: kpi-tile
kind: composite-pattern
purpose: Single-metric display — value + label + optional delta + optional sparkline +
  optional drill-down. The atom of dashboard composition.

when-to-use:
  - One number tells the user something useful at a glance
  - Inside a dashboard, alongside other tiles
  - On a detail-page summary row
  - In an executive / status surface

when-not-to-use:
  - Number lacks context (always pair with label + comparison)
  - Multiple correlated metrics → use a chart instead
  - Real-time / streaming metric where the number flickers (use chart)

variants:
  - default: value + label
  - with-delta: + change vs prior period (positive / negative styled)
  - with-sparkline: + tiny line / bar chart trend
  - with-target: + progress toward goal (bar or %)
  - status-tile: with prominent state colour (good / warn / bad)
  - clickable: drills down to a detail surface

default-trade-offs:
  speed-accuracy: +1
  density-focus: +1
  control-automation: 0

required-slots:
  - value: the metric value (formatted)
  - label: what the metric represents

optional-slots:
  - delta: { value, direction, period }
  - sparkline: time-series data
  - target: { value, progress }
  - drill-down link
  - footnote: e.g., "as of {timestamp}"

states:
  default: rendered
  loading: skeleton (label visible, value placeholder)
  error: tile shows error icon + label preserved
  empty: "No data" within the tile (rare; usually means metric source missing)
  stale: timestamp / staleness indicator visible

behaviours-built-in:
  - drill-down on click (when clickable variant)
  - keyboard-reachable when interactive
  - hover / focus reveals footnote / definition

composition-rules:
  may-contain: number, label, delta indicator, mini-sparkline, progress bar, link
  must-not-contain: forms, tables, complex content
  parent-restrictions: typically inside a dashboard tile slot or a detail-page summary row

token-roles-consumed:
  - surface-elevated, text-default, text-muted, state-success, state-warning,
    state-danger, elevation-card, radius-md, focus-ring

accessibility:
  - value + label associated semantically
  - delta direction announced (not colour alone)
  - reduced-motion: sparkline animation disabled

spec-author-cues:
  - always pair value with comparator (delta or target) — bare numbers lack meaning
  - status-tile only for genuinely state-bearing metrics (uptime, error rate)
  - keep value formatting consistent across tiles in the same dashboard
```
