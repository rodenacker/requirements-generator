---
stadium_asset: modules
app: RMB_Onboarding
file_guid: 87ea91de-6125-4686-8437-806216cb0ec0
designer_version: 6.14.3378.13771
selected_package: 3f1ddf96-3519-47b8-905d-b44703776f78.sapz
deployment_count: 1
last_published: 2026-06-30 12:19:12.1887333
extracted_from: C:\Stadium 6 Web Apps\87ea91de-6125-4686-8437-806216cb0ec0
provenance: deterministic extraction from the Stadium 6 design model + administration.db
marker_legend: Tier-A lines are authoritative facts ([SRC]-quotable); Tier-B lines are advisory design signals.
---
# Custom JS / modules — RMB_Onboarding

## Tier-A — detected modules

_No stadium-software modules detected (comment-URL, function-name, or CSS footprint)._

- global-scripts.js present: True
- Module CSS footprint: none

## Tier-B — modernization & UX signals (advisory)

- Library-copy ratio: ~0 `stadium-software` library block(s) across ~1 global-scripts function(s) (~0%) — modernization would replace copy-pasted module JS with shared components. [from global-scripts] `[AI-SUGGESTED]`
- Mock / non-prod backend(s): `Stadium` — integration point(s) not yet pointed at production. [from design model] `[AI-SUGGESTED]`
- Validation density: 15 validated control(s) across 88 input control(s). [from design model] `[AI-SUGGESTED]`
- State handling: screen edge/empty/loading states are managed via ad-hoc visibility toggles (see `business-rules` state signals), not a formal state machine. `[AI-SUGGESTED]`

## Tier-B — implication (advisory)
- Detected modules indicate behaviour beyond standard CRUD controls (must be captured as required interactions). `[AI-SUGGESTED]`
