---
stadium_asset: modules
app: PaymentsApp
file_guid: be54c8c9-dc03-43d5-bc2b-fba14e07f360
designer_version: 6.14.3378.13771
selected_package: 2211275f-1cb9-495c-91cf-4ff48dc4c142.sapz
extracted_from: C:\Stadium 6 Web Apps\be54c8c9-dc03-43d5-bc2b-fba14e07f360
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Custom JS / modules — PaymentsApp

## Tier-A — detected modules

- **conditional-datagrid-styling** — Conditional row/cell styling in a DataGrid driven by data value — https://github.com/stadium-software/conditional-datagrid-styling [detected via: comment-URL]
- **datagrid-advanced-search** — Multi-field / advanced search panel over a DataGrid — https://github.com/stadium-software/datagrid-advanced-search [detected via: function-name]
- **filter-grid** — Attribute-based filtering of DataGrid rows by column value — https://github.com/stadium-software/filter-grid [detected via: comment-URL]
- **full-width-top-bar** — Full-width top app bar / header chrome — https://github.com/stadium-software/full-width-top-bar [detected via: comment-URL]
- **icons** — Icon helper (Font Awesome / glyph injection) — https://github.com/stadium-software/icons [detected via: function-name]
- **page-loader** — Full-page loading indicator / busy spinner during async work — https://github.com/stadium-software/page-loader [detected via: comment-URL]
- **popups** — Modal dialogs / toast popups — https://github.com/stadium-software/popups [detected via: CSS footprint]
- **repeater-datagrid-client-side** — Client-side DataGrid rendered from a Repeater, paged/sorted in-browser — https://github.com/stadium-software/repeater-datagrid-client-side [detected via: comment-URL]
- **tabs** — Tabbed container — switch between panels in one surface — https://github.com/stadium-software/tabs [detected via: comment-URL]
- **workflow-steps** — Stepper / progress-step indicator for multi-step flows — https://github.com/stadium-software/workflow-steps [detected via: comment-URL]

## Tier-A — module-driven behaviours

- multi-step (stepper) workflow — a required multi-step interaction [from global-scripts]

- global-scripts.js present: True
- Module CSS footprint: modal-variables.css, modal.css

## Tier-B — implication (advisory)
- Detected modules indicate behaviour beyond standard CRUD controls (must be captured as required interactions). `[AI-SUGGESTED]`
