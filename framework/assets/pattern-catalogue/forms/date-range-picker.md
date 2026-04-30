<!-- ROLE: asset (pattern). STATUS: T3 stub — author full entry on first use. -->

# Pattern: date-range-picker

```yaml
id: date-range-picker
kind: composite-pattern
purpose: Two-date selection with presets and a calendar surface; powers reporting,
  filtering, and any "from X to Y" range input.
status: stub

when-to-use:
  - Filter / report scoping by date range
  - Booking / scheduling within a window
  - Analytics surfaces (paired with chart)

when-not-to-use:
  - Single date → use a normal date picker (an atom-level field)
  - Recurring schedules → specialised scheduling pattern (deferred)

variant-clusters: with-presets (Today / Last 7 / Month-to-date), inline-calendar,
  popover-calendar, dual-month, time-of-day-aware, relative-only ("last 7 days")

required-slots-baseline: start, end, on-change, presets
key-tokens: surface-elevated, text-default, state-selected, focus-ring, motion-fast

related: search-and-filter, chart, dashboard
```

> **Author the full entry when:** the first analytics or reporting brief lands. Locale + timezone handling matters; surface in the full entry.
