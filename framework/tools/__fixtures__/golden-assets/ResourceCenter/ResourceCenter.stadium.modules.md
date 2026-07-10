---
stadium_asset: modules
app: ResourceCenter
file_guid: 27cac42c-3dc4-44fd-99a0-84d001ccd971
designer_version: 6.14.3378.13771
selected_package: 4dd7964f-aadd-4ba2-ad82-9cf8fa1f9aa7.sapz
deployment_count: 4
last_published: 2026-06-03 11:01:11.2158983
extracted_from: C:\Stadium 6 Web Apps\27cac42c-3dc4-44fd-99a0-84d001ccd971
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Custom JS / modules — ResourceCenter

## Tier-A — detected modules

_No stadium-software modules detected (comment-URL, function-name, or CSS footprint)._

- global-scripts.js present: True
- Module CSS footprint: none

## Tier-B — modernization & UX signals (advisory)

- Library-copy ratio: ~0 `stadium-software` library block(s) across ~1 global-scripts function(s) (~0%) — modernization would replace copy-pasted module JS with shared components. [from global-scripts] `[AI-SUGGESTED]`
- State handling: screen edge/empty/loading states are managed via ad-hoc visibility toggles (see `business-rules` state signals), not a formal state machine. `[AI-SUGGESTED]`

## Tier-B — implication (advisory)
- Detected modules indicate behaviour beyond standard CRUD controls (must be captured as required interactions). `[AI-SUGGESTED]`
