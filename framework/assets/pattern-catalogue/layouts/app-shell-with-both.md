<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: app-shell-with-both

```yaml
id: app-shell-with-both
kind: layout-primitive
purpose: Sidebar + topnav combined; for large multi-product apps where the topnav
  switches between products / workspaces and the sidebar navigates within one.
status: stub

when-to-use:
  - Multi-product suite where users switch contexts often
  - Workspace + section navigation as two orthogonal axes
  - Enterprise apps with role + module + section hierarchy

when-not-to-use:
  - Single-product app — just use one of sidebar or topnav
  - <3 modules in topnav — collapse into sidebar groups

variant-clusters: workspace-switcher-topnav, product-switcher-topnav, with-org-banner

related: app-shell-with-sidebar, app-shell-with-topnav
```

> **Author the full entry when:** the first brief involves multi-product / multi-workspace navigation.
