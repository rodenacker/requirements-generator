# Blueprint: file-upload-flow

## Sources

**Functional:** F-05, F-06, F-07, F-08, F-14, F-15, F-16, F-17, F-18, F-19, F-20
**Business rules:** BR-06, BR-09, BR-10
**UI feature needs:** UI-04, UI-05, UI-06, UI-07, UI-14, UI-15, UI-16, UI-17, UI-18, UI-19
**Goals:** G-02
**Task flows:** §5 File Upload, §5 File Log Overview, §5 File Summary
**Data shapes:** §7 FileLog, §7 FileSetting, §7 FileProcessLog, §7 ValidationErrors

> `requirements.md` sha256 at scope-selection time: `8139af430390f934ea05d2691660fdbce12ceb7f7a86c0e4b05be2134f27b8c7`

## Available personas (from `requirements/requirements.md` §3)

- **Importer** — Intermediate, familiar with file-ingestion workflows; daily, one or more files per business day; primary stake is successful ingestion of transaction files for downstream approval.
- **Approver** — Senior, empowered to apply approve/reject decisions; daily, reviewing the day's ingested transactions; primary stake is correct, auditable approve/reject decisions.

## Screen inventory

| Screen ID | Intent | Sources | Secondary intent |
|---|---|---|---|
| S-01 | File upload (file picker + metadata + progress) | F-05, F-06, BR-06, BR-09, BR-10, UI-04, UI-05, §5 File Upload, §7 FileSetting, §7 FileLog | with upload-progress indicator and validation outcome feedback |
| S-02 | File log overview (table + row actions + drill into transactions) | F-06, F-07, F-08, F-15, F-16, F-17, F-19, F-20, UI-06, UI-07, UI-15, UI-16, UI-17, UI-18, UI-19, §5 File Log Overview, §7 FileLog | with row-level Download / Retry / Cancel actions and HasBulkErrorFile indicator |
| S-03 | File summary (per-FileLog counts + bulk-error indicator) | F-14, F-15, F-17, UI-14, UI-15, UI-17, §5 File Summary, §7 FileLog, §7 FileProcessLog | with HasBulkErrorFile error indicator and bulk-error download |
| S-04 | Validation errors detail (per-file validation row list) | F-18, F-19, UI-15, UI-18, §7 ValidationErrors, §7 FileProcessLog | with retry-validation action and per-row error context |

Notes:
- Every row's `Sources` list is the set of requirement IDs this screen exists to satisfy. The variant-generators propagate these into `data-src` attributes on rendered elements.
- Secondary intent is optional. When present, it captures a slot a variant may want to populate with a non-primary pattern (e.g. "with inline validation"); when blank, the variant decides freely.

## Flow

S-01 → S-02 → S-03; S-02 → S-04 or S-03 → S-04 when HasBulkErrorFile is true; S-04 → S-02 on close; S-02 → S-01 on "Upload another" (Importer only per BR-09 / BR-10).

## Pattern-coverage preflight

verdict: ok — 4 of 4 screens have a direct-match T1 catalogue pattern for the primary slot (`forms/single-form` and `forms/multi-step-wizard` for S-01; `collections/table` with `surfaces/modal-confirmation` for S-02; `collections/dashboard` or `collections/detail-page` for S-03; `collections/table` or `collections/data-list` for S-04). No AI-SUGGESTED gaps.

(Output of `framework/skills/check-pattern-coverage.md` run by the architect during design-brief preflight. A gap here would have fired the orchestrator's conditional gate; on a clean preflight this section is informational.)

## Self-validation

| Check | Result |
|---|---|
| Bijection (every scope source referenced; no orphan screens) | PASS |
| Conflicts (no requirement pair foreclosing each other) | NONE |

## Architect notes

4 screens (S-01..S-04), 28 scope sources from §5 File Upload + §5 File Log Overview + §5 File Summary, 2 personas available (Importer daily-intermediate-operator; Approver daily-expert-approver). G-02 (Review uploaded transactions efficiently) is in scope but does not seed a screen — its quality signals (table loads within budget; filters apply quickly) shape layout density and recovery-friction decisions across S-02 and S-04. F-15 audit columns surface across S-02 and S-03. BR-09 makes S-01 Importer-only; BR-10 hides S-01 from Approver. UI-15 HasBulkErrorFile indicator surfaces on S-02 row, S-03 header, and is the trigger transition to S-04. The drill from S-02 → out-of-scope Transaction Table (F-08 / UI-07) is rendered as a stub destination by variant generators.
