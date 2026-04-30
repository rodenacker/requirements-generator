<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: omnibar

```yaml
id: omnibar
kind: surface-pattern
purpose: Combined search + navigate + recent-actions input; prominent persistent
  search bar that does multiple jobs — find records, run actions, jump to routes.
status: stub

when-to-use:
  - Large product where global search is the dominant entry-point
  - Power-user persona that mixes search and navigation
  - Apps where multiple result kinds (records / pages / actions) matter

when-not-to-use:
  - Small product (search-and-filter inside the page is enough)
  - When command-palette covers the action / navigation use cases

variant-clusters: with-categories, with-shortcuts-hint, instant-results, scoped

related: command-palette, search-and-filter
```

> **Author the full entry when:** the first brief calls for a persistent global search bar with multi-kind results.
