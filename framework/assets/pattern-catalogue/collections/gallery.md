<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: gallery

```yaml
id: gallery
kind: composite-pattern
purpose: Image / media-first grid — emphasises visual content, supports lightbox /
  full-screen viewing, optional masonry-style layout.
status: stub

when-to-use:
  - Image / video / media collections
  - Portfolio / showcase / asset library
  - Product catalogue where imagery dominates

when-not-to-use:
  - Records have meaningful non-visual fields → card-grid
  - Records have no images → data-list or table

variant-clusters: uniform-grid, masonry, with-lightbox, with-filters, with-bulk-select

related: card-grid, lightbox (deferred)
```

> **Author the full entry when:** the first media-heavy brief lands. Lightbox dependency is significant; consider the lightbox stub becoming a sibling.
