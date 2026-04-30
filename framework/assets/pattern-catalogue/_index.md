<!-- ROLE: asset (pattern-catalogue index). v7b-specific. -->

# Pattern catalogue — index

50 patterns across 7 categories. The `design-system-drafter` selects from this catalogue; the design spec configures pattern instances per task / object / role. Each pattern lives in its own file so the drafter only loads what it actually selects.

**Tier markers**

- **T1** — MVP. Ships with phase-1 design-system. Covers ~80% of standard product briefs. Full entries.
- **T2** — Common. Widely used; condensed entries. Build out to full when a brief needs them.
- **T3** — Specialised. Stubs only. Author the full entry when the first brief requires the pattern.

---

## Layouts (page shells)

- [`app-shell-with-sidebar`](layouts/app-shell-with-sidebar.md) — **T1** — Vertical primary nav + main content; dominant SaaS shell.
- [`app-shell-with-topnav`](layouts/app-shell-with-topnav.md) — **T1** — Horizontal primary nav + main content; lighter / consumer-facing.
- [`centered-form`](layouts/centered-form.md) — **T1** — Single isolated form on neutral background; auth, simple capture.
- [`marketing-shell`](layouts/marketing-shell.md) — **T1** — Public-facing landing layout; hero + sections + footer.
- [`settings-shell`](layouts/settings-shell.md) — **T1** — Sectioned-nav layout for preferences / account / team / billing.
- [`error-shell`](layouts/error-shell.md) — **T2** — 404 / 500 / maintenance / no-permission full-page.
- [`auth-flow-shell`](layouts/auth-flow-shell.md) — **T2** — Multi-step onboarding / signup / MFA shell.
- [`print-shell`](layouts/print-shell.md) — **T3** — Invoice / report / receipt for print or PDF.
- [`app-shell-with-both`](layouts/app-shell-with-both.md) — **T3** — Sidebar + topnav for large multi-product apps.

## Navigation

- [`tabs`](navigation/tabs.md) — **T1** — Mutually-exclusive panel switching within one context.
- [`pagination`](navigation/pagination.md) — **T1** — Page-by-page navigation through a long collection.
- [`stepper-indicator`](navigation/stepper-indicator.md) — **T1** — Progress display for a multi-step flow.
- [`segmented-control`](navigation/segmented-control.md) — **T2** — 2–4 mutually-exclusive options; mobile-first tabs alternative.
- [`command-palette`](navigation/command-palette.md) — **T2** — Keyboard-first action / navigation launcher.
- [`mega-menu`](navigation/mega-menu.md) — **T3** — Multi-column dropdown with sections.
- [`omnibar`](navigation/omnibar.md) — **T3** — Combined search + navigate + recent-actions input.

## Collections / display

- [`table`](collections/table.md) — **T1** — Homogeneous record collection, columnar, sortable, optionally selectable.
- [`master-detail-list`](collections/master-detail-list.md) — **T1** — List on one side, selected-record detail on the other.
- [`data-list`](collections/data-list.md) — **T1** — Simple stacked list; lighter than a table; mobile-friendly.
- [`dashboard`](collections/dashboard.md) — **T1** — Composition of KPI tiles + summary cards + small charts.
- [`detail-page`](collections/detail-page.md) — **T1** — Full-page view of a single record.
- [`card-grid`](collections/card-grid.md) — **T2** — Visually-rich record grid; image + meta + CTA per card.
- [`kpi-tile`](collections/kpi-tile.md) — **T2** — Single-metric tile with delta / sparkline / context.
- [`detail-panel`](collections/detail-panel.md) — **T2** — Inline / side detail for a selected record.
- [`chart`](collections/chart.md) — **T3** — Time-series / categorical / proportional / distribution / correlation visualisations.
- [`timeline`](collections/timeline.md) — **T3** — Chronological event display.
- [`tree-view`](collections/tree-view.md) — **T3** — Hierarchical expandable list.
- [`feed`](collections/feed.md) — **T3** — Chronologically streaming posts / events.
- [`gallery`](collections/gallery.md) — **T3** — Image / media-first grid.

## Forms / input

- [`single-form`](forms/single-form.md) — **T1** — One-step form on a page; section groups, validation, submit.
- [`multi-step-wizard`](forms/multi-step-wizard.md) — **T1** — Sequential multi-step flow with validated forward progress.
- [`search-and-filter`](forms/search-and-filter.md) — **T1** — Search input + filter facets + result region.
- [`inline-edit`](forms/inline-edit.md) — **T2** — Edit-in-place within table rows or detail panels.
- [`bulk-edit`](forms/bulk-edit.md) — **T2** — Select-N + apply-changes flow for table or list.
- [`multi-page-form`](forms/multi-page-form.md) — **T3** — Wizard-like but each step is its own route.
- [`repeater`](forms/repeater.md) — **T3** — Add-multiple-items inline (line items, key-value pairs).
- [`date-range-picker`](forms/date-range-picker.md) — **T3** — Two-date selection with presets.
- [`file-upload`](forms/file-upload.md) — **T3** — Single or multi; drag-drop + browse + progress.

## Surfaces (overlays, transient containers)

- [`modal-confirmation`](surfaces/modal-confirmation.md) — **T1** — Destructive-action confirm before commit.
- [`drawer-detail`](surfaces/drawer-detail.md) — **T1** — Side-entering panel for read-mostly detail.
- [`modal-form`](surfaces/modal-form.md) — **T2** — Small form inside a modal (create / quick-edit).
- [`drawer-form`](surfaces/drawer-form.md) — **T2** — Form inside a drawer (longer than modal-form supports).
- [`popover`](surfaces/popover.md) — **T2** — Small contextual surface anchored to a trigger; non-blocking.
- [`dialog`](surfaces/dialog.md) — **T3** — Irreversible action with multiple distinct options.

## Feedback

- [`notification-toast`](feedback/notification-toast.md) — **T1** — Transient success / info / error; auto-dismiss.
- [`empty-state`](feedback/empty-state.md) — **T1** — "No data yet" surface with primer copy + CTA.
- [`notification-banner`](feedback/notification-banner.md) — **T2** — Persistent dismissible message at top of region or page.
- [`confirmation-receipt`](feedback/confirmation-receipt.md) — **T2** — Post-action summary; "what happened + what's next".

## Auth (specialised forms)

- [`login-form`](auth/login-form.md) — **T3** — Email/password + OAuth provider buttons.
- [`signup-form`](auth/signup-form.md) — **T3** — Account creation with optional verification.

---

## Lives elsewhere (not in this catalogue)

**Conventions** — single rules applied consistently across patterns. Live in `design-system.md > §5 State conventions` and `§6 Interaction conventions`:

`tooltip`, `breadcrumbs`, `back-link`, `loading-skeleton`, `inline-error`, `inline-success`, `progress-indicator`, `permission-gate`, `role-switcher`.

**Deferred** — known patterns, intentionally omitted until a brief requires them:

`kanban-board`, `calendar-month` / `-week` / `-day`, `chat-thread`, `comment-thread`, `inbox-list`, `query-builder`, `comparison-table`, `image-cropper`, `signature-capture`, `payment-form`, `address-input`, `audio-player`, `video-player`, `welcome-tour`, `tooltip-coachmark`, `checklist-onboarding`, `feature-announcement`, `csv-import-flow`, `media-uploader`, `kiosk-shell`, `embedded-shell`, `bottom-sheet`, `lightbox`, `mfa-prompt`, `password-reset-flow`, `consent-screen`, `instant-search-dropdown`, `faceted-search`.

---

## Entry shape (reference)

Every catalogue entry is a YAML block with these fields. Tier 3 stubs carry only `id`, `kind`, `purpose`, and a status note.

```
id, kind, purpose, when-to-use, when-not-to-use, variants, default-trade-offs,
required-slots, optional-slots, states, behaviours-built-in, composition-rules,
token-roles-consumed, accessibility, spec-author-cues, mapping-helpers
```
