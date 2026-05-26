# Blueprint: importer-workflow

## Sources

**Functional:** F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14, F-21
**Business rules:** BR-01, BR-02, BR-08
**UI needs:** UI-01, UI-02, UI-03, UI-04, UI-06, UI-08, UI-12, UI-13, UI-14, UI-16
**Goals:** G-01, G-03, G-05
**Task flows:** §5 Flow: File Upload, §5 Flow: File Log Overview, §5 Flow: Transaction Review, §5 Flow: File Summary View, §5 Flow: Search and Filter
**Data shapes:** §7 FileLog, §7 Transaction, §7 FileSetting (§7.X File Summary derivation)

> `requirements.md` sha256 at scope-selection time: `a1d0ad212a1a15e93c79f2fd1b3f0875421fda9c9a3bf21c89e8b71d20ab5869`

## Available personas (from `requirements/requirements.md` §3)

- **Importer** — operational user; comfortable selecting and uploading files, reading status indicators, applying search and filter. Daily during business hours. Responsible for getting transaction files into the system correctly so downstream Approver review can begin.
- **Approver** — financially literate reviewer; comfortable interpreting amounts, currencies, references, and applying judgement under audit. Daily during business hours. Read-only access to this scope's transaction views (approve / reject actions deliberately out of scope per intent `full importer workflow - excluding login`).

## Screen inventory

| Screen ID | Intent | Sources | Properties | Secondary intent |
|---|---|---|---|---|
| S-01 | File Log list and overview | F-05, F-10, F-11, BR-01, BR-02, BR-08, UI-02, UI-12, UI-14, UI-16, G-03, G-05, §5 Flow: File Log Overview, §7 FileLog | FileLog.FileName, FileLog.ProcessDate, FileLog.RecordCount, FileLog.CurrentStatus, FileLog.SettingName, FileLog.LastExecutedActivityName, FileLog.HasBulkErrorFile, FileLog.IsActive | with row-level cancel (F-10) and retry-validation (F-11) actions, IsActive filter, and an empty-state upload CTA shown only to Importers (BR-08) |
| S-02 | File upload form | F-04, UI-01, UI-13, BR-08, G-01, §5 Flow: File Upload, §7 FileSetting | F-04:FileSettingId, F-04:FileSettingName, F-04:FileName, FileSetting.Name, FileSetting.IsActive | with file-setting picker, required-field markers (UI-13), and success / failure feedback inline on the same screen |
| S-03 | File Log detail view | F-06, F-07, F-08, F-09, F-10, F-11, BR-01, BR-02, G-03, §7 FileLog | FileLog.FileName, FileLog.ProcessDate, FileLog.RecordCount, FileLog.CurrentStatus, FileLog.LastExecutedActivityName, FileLog.SettingName, FileLog.HasBulkErrorFile, F-06:ProcessLogEntries | with downloads (F-07 parsed / F-08 original / F-09 bulk-error when present) and process-log timeline |
| S-04 | Validation errors table | F-12, F-13, BR-02 | F-12:Columns, F-13:Rows | reachable only when the parent File Log is in Failed state (BR-02); columns and rows are opaque payloads — see Architect notes |
| S-05 | File Summary dashboard | UI-08, G-03, §5 Flow: File Summary View | FileSummary.TotalRecords, FileSummary.ImportedCount, FileSummary.ApprovedCount, FileSummary.RejectedCount | per-status counts derived from Transaction.Status (§7.X Derivations) |
| S-06 | Transaction list with filter and search | F-14, F-21, UI-03, UI-04, UI-06, UI-12, UI-14, UI-16, G-05, §5 Flow: Transaction Review, §5 Flow: Search and Filter, §7 Transaction | Transaction.Reference, Transaction.TransactionDate, Transaction.AccountNumber, Transaction.Amount, Transaction.Currency, Transaction.Status, Transaction.UserNote | reached via UI-03 drilldown from S-01 (file-filtered) or as the standalone all-files transaction list; sortable columns, observable active-filter set (UI-06), pagination (UI-12), status badges (UI-14), zero-results empty state (UI-16) |

Notes:
- Every row's `Sources` list is the set of requirement IDs this screen exists to satisfy. The variant-generators propagate these into `data-src` attributes on rendered elements.
- Every row's `Properties` list is the **closed set** of object properties the screen may render. Each entry resolves to either (a) a §7 data-shape property using `Shape.Property` notation, or (b) an F-NN-named property using `F-NN:ParamName` notation when the F-NN names a parameter not in §7. The variant-generator embeds `data-prop` attributes on each data-bound element naming the property it binds to; rendering a property outside this list is a self-validation FAIL. **UI-only controls (search, sort, pagination, filter chips, expand/collapse, save/cancel buttons, progress indicators) are exempt from the property contract and do not need a `data-prop` attribute.**
- Secondary intent is optional. When present, it captures a slot a variant may want to populate with a non-primary pattern (e.g. "with inline validation"); when blank, the variant decides freely.

## Flow

S-01 → S-02 → S-01 on upload result; S-01 → S-03 on row drilldown; S-03 → S-04 on Failed-state validation-errors drilldown; S-03 → S-05 on file-summary view; S-01 → S-06 on transaction drill via UI-03; S-03 → S-06 from file detail; S-03 → S-01 on cancel-or-back.

## Pattern-coverage preflight

`verdict: ok` — 6 of 6 screens have a direct-match T1 catalogue pattern for the primary slot (`collections/table` for S-01, S-04, S-06; `forms/single-form` for S-02; `collections/detail-page` for S-03; `collections/dashboard` + `collections/kpi-tile` for S-05; `forms/search-and-filter` co-bound on S-01 and S-06). No AI-SUGGESTED gaps.

(Output of `framework/skills/check-pattern-coverage.md` run by the architect during design-brief preflight. A gap here would have fired the orchestrator's conditional gate; on a clean preflight this section is informational.)

## Self-validation

| Check | Result |
|---|---|
| Bijection (every scope source referenced; no orphan screens) | PASS |
| Conflicts (no requirement pair foreclosing each other) | NONE |
| Properties (every property resolves to §7 or a cited F-NN's named parameter) | PASS |

## Architect notes

6 screens authored against 12 functional + 3 business-rule + 10 UI + 3 goal scope sources, plus 3 §7 shapes and the §7.X File Summary derivation. Entry screen is S-01 File Log Overview (the dashboard a freshly-authenticated Importer or Approver lands on, with authentication itself deliberately out of scope); S-02 is the Importer-bound upload surface gated by BR-08 (the upload affordance must be hidden from non-Importers — the §6.5 RBAC matrix restricts FileUpload to Importer only). S-04 Validation Errors is reachable only when the parent File Log is in Failed state per BR-02 (extraction failure → File Log → Failed → retry-validation action available); F-12 returns the system-defined column definitions for the validation-error view of that file, F-13 returns the per-row error data as a single JSON array string — both are **opaque payloads** in the sense of `framework/agents/blueprint-architect/steps/step-03-author-blueprint.md > 3.2b`: their row shape is not documented in §7, so the closed-set entries `F-12:Columns` and `F-13:Rows` are placeholders for runtime-system-defined columns and the variant-generator may render sub-columns derived from the F-12 / F-13 prose using `data-prop="F-12:Columns[<column>]"` / `data-prop="F-13:Rows[<column>]"` attributes naming column identifiers that appear verbatim in the F-12 / F-13 text — no other shape. S-03 carries a similar opaque-payload entry `F-06:ProcessLogEntries`: F-06 returns the activity history for a single File Log; the row shape is unspec'd in §7, so the variant-generator should render the process log as an activity feed bound to `data-prop="F-06:ProcessLogEntries"` on the container, with entry sub-fields treated as runtime-defined and named verbatim from any F-06 prose. S-05 File Summary derives from §7.X Derivations' four named outputs (TotalRecords, ImportedCount, ApprovedCount, RejectedCount); the FileSummary shape used in the Properties cell adopts those four names as its closed-set surface. S-06 Transaction List is read-only in this scope — approve / reject row-level actions on Imported transactions are Approver-only and would normally be bound to F-15 / F-16, but the consultant's `full importer workflow - excluding login` intent deliberately excludes those functional requirements; both personas are retained in `personas_available` for read-only access, and variant-generators must not render approve / reject affordances on S-06 in this scope. UI-13 (required-field markers) is bound to S-02 only, where the upload form has three required fields (FileSettingId, FileSettingName, FileName) per §6.3. UI-14 (status badges with paired icon/text) is bound to S-01 (FileLog.CurrentStatus) and S-06 (Transaction.Status). UI-12 (pagination with rows-per-page selector) is bound to S-01 and S-06; per `GR-NN` deterministic defaults the rows-per-page default is 20 with selector {5, 10, 20, 50}. UI-16 (empty states) is bound to S-01 (no-files-yet copy + upload CTA Importer-only) and S-06 (zero-results-from-filter shows active filter chips and clear-all). No analyses were consumed (Stage 1b returned `selected-none`); the blueprint relies exclusively on `requirements.md` + the architect's domain inference. No bijection violations, no conflicts, no fabricated properties; pattern-coverage preflight summary slotted in by step 4.
