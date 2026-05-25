# Blueprint: file-upload-log

## Sources

F-05, F-06, F-07, F-08, F-14, F-16, F-17, F-18, F-19, F-20, BR-06, BR-09, BR-10, UI-04, UI-05, UI-06, UI-07, UI-14, UI-15, UI-16, UI-17, UI-18, UI-19, G-01, G-05, §5 File Upload, §5 File Log Overview, §5 File Summary, §7 FileLog, §7 FileProcessLog, §7 ValidationErrors

> `requirements.md` sha256 at scope-selection time: `8139af430390f934ea05d2691660fdbce12ceb7f7a86c0e4b05be2134f27b8c7`

## Available personas (from `requirements/requirements.md` §3)

- **Importer** — Intermediate, familiar with file-ingestion workflows; daily, one or more files per business day. Primary stake: successful ingestion of transaction files for downstream approval.
- **Approver** — Senior, empowered to apply approve/reject decisions; daily, reviewing the day's ingested transactions. Primary stake: correct, auditable approve/reject decisions on transactions.

## Screen inventory

| Screen ID | Intent | Sources | Properties | Secondary intent |
|---|---|---|---|---|
| S-01 | File Upload (Importer-only) | F-05, F-06, BR-06, BR-09, BR-10, UI-04, UI-05, G-01, §5 File Upload | F-05:FileSettingId, F-05:FileSettingName, F-05:FileName | with drag-and-drop + indeterminate upload progress |
| S-02 | File Log Overview | F-07, F-08, F-16, F-17, F-19, F-20, UI-06, UI-07, UI-15, UI-16, UI-17, UI-18, UI-19, §5 File Log Overview, §7 FileLog | FileLog.CurrentFileName, FileLog.ProcessDate, FileLog.RecordCount, FileLog.CurrentStatus, FileLog.HasBulkErrorFile | with per-row download / retry / cancel actions and drill to transactions |
| S-03 | File Summary (per FileLog) | F-14, UI-14, UI-15, G-05, §5 File Summary, §7 FileLog, §7 FileProcessLog | FileSummary.ImportedCount, FileSummary.ApprovedCount, FileSummary.RejectedCount, FileLog.RecordCount, FileLog.HasBulkErrorFile, FileLog.CurrentFileName, FileLog.CurrentStatus, FileLog.ProcessDate, FileProcessLog.ActivityName, FileProcessLog.DecisionResult, FileProcessLog.StartDate, FileProcessLog.EndDate | with processing-step timeline + error indicator |
| S-04 | Validation Errors (per FileLog) | F-18, §7 ValidationErrors | ValidationErrors.JsonArray | per-row validation error list reached from S-02 (HasBulkErrorFile=true) or S-03 |

Notes:
- Every row's `Sources` list is the set of requirement IDs this screen exists to satisfy. The variant-generators propagate these into `data-src` attributes on rendered elements.
- Every row's `Properties` list is the **closed set** of object properties the screen may render. Each entry resolves to either (a) a §7 data-shape property using `Shape.Property` notation, or (b) an F-NN-named property using `F-NN:ParamName` notation when the F-NN names a parameter not in §7. The variant-generator embeds `data-prop` attributes on each data-bound element naming the property it binds to; rendering a property outside this list is a self-validation FAIL. **UI-only controls (search, sort, pagination, filter chips, expand/collapse, save/cancel buttons, progress indicators) are exempt from the property contract and do not need a `data-prop` attribute.**
- Secondary intent is optional. When present, it captures a slot a variant may want to populate with a non-primary pattern (e.g. "with inline validation"); when blank, the variant decides freely.
- `ValidationErrors.JsonArray` on S-04 is an **[OPAQUE-PAYLOAD]**: §7 ValidationErrors carries one field (`JsonArray` — a JSON-array string of per-row error objects). F-18's prose says "per-row error objects". The variant-generator may render columns derived from F-18's text but each rendered column must carry `data-prop="ValidationErrors.JsonArray[<column>]"` and the column name must appear in F-18's verbatim text or in a sample row of the JSON array. Anything outside that contract is a fabrication.

## Flow

S-01 → S-02 on upload success (new FileLog row appears); S-02 → S-03 on row "View summary" action; S-02 → S-04 on row "View validation errors" action when FileLog.HasBulkErrorFile is true; S-03 → S-04 on "View errors" link when FileLog.HasBulkErrorFile is true; S-02 → (transactions table, out of scope) on row primary drill click per F-08 / UI-07; S-01 → S-01 on validation failure (inline error region, retry available per §6.4.5 UI-04/UI-05 error state).

## Pattern-coverage preflight

`verdict: ok` — 4 of 4 screens have direct-match catalogue patterns for the primary slot. S-01 → `forms/single-form` (with file slot for F-05's three named query parameters + drag-and-drop chrome); S-02 → `collections/table` (paginated FileLog list per F-07 with row actions for F-16/F-17/F-19/F-20/F-08); S-03 → `collections/dashboard` + `collections/kpi-tile` (FileSummary counts + HasBulkErrorFile indicator + processing-step timeline per FileProcessLog); S-04 → `collections/table` or `surfaces/drawer-detail` (per-row validation errors decoded from the opaque JsonArray payload per F-18).

## Self-validation

| Check | Result |
|---|---|
| Bijection (every scope source referenced; no orphan screens) | PASS |
| Conflicts (no requirement pair foreclosing each other) | NONE |
| Properties (every property resolves to §7 or a cited F-NN's named parameter) | PASS |

## Architect notes

4 screens, 10 functional sources, 3 business rules, 10 UI needs, 2 goals, 3 task flows, 3 data shapes. 2 personas: Importer (intermediate, daily — primary for S-01) and Approver (senior, daily — read-only on S-02/S-03/S-04). Goal G-01 (ingest reliably) drives S-01's "with drag-and-drop + progress" secondary intent; G-05 (visibility into processing state) drives S-02's HasBulkErrorFile chip and S-03's error indicator + processing timeline.

Analyses augmentation (Stage 1b — `wireframes/file-upload-log/analyses-inputs.json`, sidecar-first protocol with legacy bounded prose fallback per RF-09 `proceed-with-bounded-read`):

- **data-model** (legacy fallback, >60 KB consultant-accepted): `screen-properties-cross-check` — cross-checked the per-screen Properties closed set against §7. No discrepancies surfaced for the in-scope shapes (FileLog, FileProcessLog, ValidationErrors) beyond what §7 documents. `screen-inventory-entity-bijection` — File Log + Transaction + User are the OOUX core objects; only File Log is bound on these screens (Transaction surfaces only on the out-of-scope drill target). Augmented by: data-model.
- **ooux** (legacy fallback): `screen-inventory-entity-bijection` — confirms File Log as the navigable object with CTAs "Upload file / Browse file logs / Filter file logs / Sort file logs / View file summary"; each CTA maps onto S-01 (Upload), S-02 (Browse/Filter/Sort), S-03 (View summary). No new screens. Augmented by: ooux.
- **use-cases** (legacy fallback, >60 KB consultant-accepted): `screen-inventory` + `screen-flow` — UC-02 Upload (S-01), UC-03 Monitor processing status (S-02 + S-03 + S-04), UC-09 View file summary (S-03). No missed screens. Flow ordering confirms S-01 → S-02 → S-03/S-04. Augmented by: use-cases.
- **user-journeys** (legacy fallback): `screen-inventory` — confirms the file-upload and file-log-overview journeys; AI-SUGGESTED opportunities (FileSettingId typeahead, inline parse-success row count, "View in File Logs" toast, default-sort by Process Date DESC, "Failed only" filter chip) are noted as variant-philosophy hints (consumed at step 5) but not bound on the inventory — they are pattern-chrome decisions for variant-generators, not new screens or new properties. Augmented by: user-journeys.
- **task-flows** (legacy fallback, >60 KB consultant-accepted): `screen-inventory` + `screen-flow` — T-2 File Upload HTA (selectFile + provideFileSettingId/Name + provideFileName + submitUpload + createFileLog + displayStatus) maps to S-01; T-3 File Log Overview HTA (openDashboard + viewFileList + drillIntoTransactions) maps to S-02. No missed screens; flow ordering confirmed. Augmented by: task-flows.
- **jtbd** — deferred to step 5 (role `variant-philosophy`, no step-3 roles).
- **trade-off-dimension-analysis** — deferred to step 5 (role `variant-dimension-applicability`, no step-3 roles).
- **five-whys** — selected but role is `upstream-only`; not consumed by the architect.

No analysis-driven screen additions. No DATA-MODEL discrepancies. The §7 + F-NN closed sets stand without widening.
