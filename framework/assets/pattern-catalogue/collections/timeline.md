<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: timeline

```yaml
id: timeline
kind: composite-pattern
purpose: Chronological event display — vertical or horizontal stream of events with
  timestamps, actors, and content per event. The canonical "audit log" / "activity"
  surface.
status: stub

when-to-use:
  - Activity feed / audit log / history per object
  - Project / case / claim chronology
  - Onboarding "what happened when"

when-not-to-use:
  - Real-time streaming chat / messaging → feed or chat-thread
  - Tabular event records with comparison → table

variant-clusters: vertical-list, horizontal-strip, grouped-by-day, with-actor-avatars,
  branchable (parallel tracks)

related: feed, detail-page (activity section)
```

> **Author the full entry when:** the first audit-log or activity-history brief lands.
