<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: repeater

```yaml
id: repeater
kind: composite-pattern
purpose: Add / remove / reorder a list of items inline within a form (line items,
  team members, key-value pairs, contact methods).
status: stub

when-to-use:
  - Form has a sub-collection of items (invoice line-items, recipients, options)
  - Users need to dynamically add / remove rows during input
  - Item shape is uniform (same fields per row)

when-not-to-use:
  - Items are heterogeneous → separate form per item
  - List is fixed-size → render fields directly
  - Bulk imports → file-upload + parse, not repeater

variant-clusters: rows (one row per item), keyed-pairs (key + value),
  reorderable (drag handles), with-row-actions, nested

related: single-form, file-upload (T3, for bulk import)
```

> **Author the full entry when:** the first form with a dynamic sub-collection lands.
