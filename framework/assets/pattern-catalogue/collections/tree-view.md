<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: tree-view

```yaml
id: tree-view
kind: composite-pattern
purpose: Hierarchical expandable list — node has children, children expand/collapse,
  selection traverses the hierarchy.
status: stub

when-to-use:
  - File-system-like browsing
  - Org-chart / category navigation
  - Hierarchical data with deep nesting

when-not-to-use:
  - Flat list (use data-list)
  - Two-level only (use grouped data-list with section headers)
  - Hierarchy is browsable but not editable in tree (use drilldown navigation instead)

variant-clusters: file-tree, category-tree, with-checkboxes (multi-select),
  draggable, lazy-loaded, with-actions-per-node

related: data-list, sidebar-nav
```

> **Author the full entry when:** the first brief involves hierarchical data browsing.
