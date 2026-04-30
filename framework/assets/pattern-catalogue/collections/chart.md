<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: chart

```yaml
id: chart
kind: composite-pattern
purpose: Data visualisation surface; a single entry covering the meaningful chart
  variant clusters. Renders inside dashboards, detail-pages, kpi-tile sparklines.
status: stub

when-to-use:
  - Trend / comparison / proportion / distribution / correlation visible in data
  - Numeric data benefits from visual scanning vs tabular reading
  - Inside dashboards, executive summaries, analytics surfaces

when-not-to-use:
  - Bare value with comparator → kpi-tile is enough
  - Tabular comparison across many rows → table
  - Single metric with no time component → kpi-tile

variant-clusters:
  - time-series (line, area, multi-line)
  - categorical (bar, column, stacked-bar, grouped-bar)
  - proportional (pie, donut, treemap)
  - distribution (histogram, box-plot, violin)
  - correlation (scatter, bubble, heatmap)
  - flow (sankey, chord) — rare

required-slots-baseline: data, encoding (x/y/category), axes, legend
common-states: default, loading, empty, error, no-data, filtered-empty
key-tokens: surface-default, text-default, text-muted, focus-ring, motion-fast,
  state-success/warning/danger (for thresholds)

related: kpi-tile, dashboard
```

> **Author the full entry when:** the first analytics-heavy brief lands. Cluster the variants under one entry; do not split per chart type. Accessibility matters most: every chart needs an accessible-name + a tabular alt-view.
