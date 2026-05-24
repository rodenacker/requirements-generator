# Blueprint: file-upload

## Sources

F-05, F-06, F-17, F-18, F-19, BR-06, BR-09, UI-04, UI-05, UI-15, UI-17, UI-18, G-01, §5 File Upload, §7 FileLog, §7 ValidationErrors

> `requirements.md` sha256 at scope-selection time: `8139af430390f934ea05d2691660fdbce12ceb7f7a86c0e4b05be2134f27b8c7`

## Available personas (from `requirements/requirements.md` §3)

- **Importer** — Intermediate operator familiar with file-ingestion workflows; daily frequency; primary stake is successful ingestion of transaction files for downstream approval; wants reliable upload feedback, clear file-summary visibility, and fast search/filter; fears silent ingestion failures and unclear validation errors.

## Screen inventory

| Screen ID | Intent | Sources | Secondary intent |
|---|---|---|---|
| S-01 | Upload form | F-05, BR-09, UI-04, UI-05, G-01, §5 File Upload | drag-and-drop file selection with parameter capture and indeterminate progress state |
| S-02 | Upload accepted | F-06, BR-06, §5 File Upload, §7 FileLog | post-action confirmation surfacing the newly-created FileLog row |
| S-03 | Upload failed — validation errors | F-17, F-18, F-19, UI-15, UI-17, UI-18, §5 File Upload, §7 ValidationErrors | error inspection list with retry and bulk-error download |

Notes:
- Every row's `Sources` list is the set of requirement IDs this screen exists to satisfy. The variant-generators propagate these into `data-src` attributes on rendered elements.
- Secondary intent is optional. When present, it captures a slot a variant may want to populate with a non-primary pattern (e.g. "with inline validation"); when blank, the variant decides freely.

## Flow

S-01 → S-02 on successful upload; S-01 → S-03 on validation failure; S-03 → S-01 on retry validation

## Pattern-coverage preflight

Verdict: **ok** — 3 of 3 screens have a direct-match catalogue pattern for the primary slot. S-01 → `forms/single-form` (T1) with file slot + parameter inputs; S-02 → `feedback/confirmation-receipt` (T2) over `collections/detail-page` (T1); S-03 → `collections/table` (T1) for the validation-error list paired with `feedback/notification-banner` (T2) for the failure banner.

(Output of `framework/skills/check-pattern-coverage.md` run by the architect during design-brief preflight. A gap here would have fired the orchestrator's conditional gate; on a clean preflight this section is informational.)

## Self-validation

| Check | Result |
|---|---|
| Bijection (every scope source referenced; no orphan screens) | PASS |
| Conflicts (no requirement pair foreclosing each other) | NONE |

## Architect notes

3 screens, 12 typed sources (5 functional, 2 business rules, 5 UI needs) + 1 goal (G-01) + 1 task flow (§5 File Upload) + 2 data shapes (§7 FileLog, §7 ValidationErrors). Single persona in scope: Importer — both variants will bind to Importer per `framework/assets/wireframes/domain-defaults.md > Section 4 rule 2`. Goal G-01 ("ingest transaction files reliably") drives the flow; the strong feedback-richness scoring for G-01 in `analyse-requirements/TRADE-OFF-DIMENSIONS/trade-off-matrix.html` (Pole A 'Feedback Richness' -2) reinforces the default `CAREFUL-DEFAULT` variant's accuracy-leaning position on D1 speed-accuracy. S-02 (Upload progress) was consolidated into S-01 since UI-05's progress feedback is a state of the upload form, not a separate screen.
