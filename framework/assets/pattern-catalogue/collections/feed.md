<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: feed

```yaml
id: feed
kind: composite-pattern
purpose: Chronologically-streaming list of posts / events / updates; infinite-scroll,
  freshness signals, optional reactions / comments per item.
status: stub

when-to-use:
  - Social-style streams
  - Notification inbox
  - Real-time activity surfaces

when-not-to-use:
  - Auditable structured history → timeline
  - Bounded record collection → data-list with pagination

variant-clusters: post-feed, activity-feed, notification-feed, real-time-streaming,
  with-pull-to-refresh, with-new-content-banner

related: timeline, data-list
```

> **Author the full entry when:** the first social or notification-stream brief lands.
