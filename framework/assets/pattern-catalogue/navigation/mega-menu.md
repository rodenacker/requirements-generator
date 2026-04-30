<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: mega-menu

```yaml
id: mega-menu
kind: layout-pattern
purpose: Multi-column dropdown with sections, descriptions, and visual elements;
  a wide menu surface for content-heavy navigation (typically marketing or large e-commerce).
status: stub

when-to-use:
  - Topnav with many destinations grouped into themes
  - Marketing site with multiple categories of content
  - E-commerce with product taxonomies

when-not-to-use:
  - Authenticated app navigation (use sidebar-nav or simple topnav dropdowns)
  - Few destinations (use simple dropdown)
  - Mobile-primary (use accordion or section-list inside a hamburger drawer)

variant-clusters: with-illustration, with-featured-item, with-search, sectioned

related: app-shell-with-topnav, marketing-shell
```

> **Author the full entry when:** the first marketing-shell brief demands rich navigation.
