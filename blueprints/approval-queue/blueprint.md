# Blueprint: approval-queue

## Sources

Functional: F-02, F-05, F-06, F-07, F-08, F-09, F-10, F-13, F-14. Business rules: BR-01, BR-02, BR-03, BR-04, BR-05, BR-07. UI needs: UI-03, UI-04, UI-05, UI-07. Goals: G-02, G-04, G-05. Task flows: §5 Transaction Table, §5 Approve Transaction, §5 Reject Transaction, §5 Search & Filtering. Data shapes: §7 Transaction, §7 User.

> `requirements.md` sha256 at scope-selection time: `ce19084bc68ff601dc83fb465013aeda9ebe04abec819ed8f1eae60c453807cf`

## Available personas (from `requirements/requirements.md` §3)

- **Importer** — uploads and reviews transaction files; intermediate, comfortable with file-based data tools; regular use per import cycle. On the approval queue the Importer reads the transaction table (RBAC R) and filters it; cannot approve/reject (BR-05).
- **Approver** — reviews, approves/rejects, and exports transactions; intermediate-to-advanced, familiar with transaction review; regular use per cycle; accountable for correct decisions (fears actioning the wrong transaction).

## Surface inventory

| Surface ID | Intent | Sources | Properties | Allowed realizations | Default realization | Host surface | Secondary intent |
|---|---|---|---|---|---|---|---|
| LS-01 | Transaction review queue | F-02, F-05, F-06, F-07, F-13, F-14, UI-03, UI-04, UI-05, UI-07, BR-01, BR-05, BR-07 | Transaction.Reference, Transaction.TransactionDate, Transaction.AccountNumber, Transaction.Amount, Transaction.Currency, Transaction.Status | standalone-screen | standalone-screen | — | Search/filter (F-07/UI-03), status chips (F-14/UI-05), file-scope cue + return (F-05/AMD-91), client-side pagination (UI-07), role-gated row actions (BR-05/BR-01), masked AccountNumber (F-13/BR-07) |
| LS-02 | Transaction detail (non-column fields) | F-06 | Transaction.TransactionType, Transaction.Description, Transaction.UserNote | standalone-screen, inline-drawer, inline-expand | standalone-screen | LS-01 | Disclosure of TransactionType, Description, UserNote (AMD-93) |
| LS-03 | Approve/reject confirmation | F-08, F-09, F-10, UI-04, BR-01, BR-02, BR-03, BR-04 | Transaction.Reference, Transaction.Amount, Transaction.Status, Transaction.UserNote | standalone-screen, modal | standalone-screen | LS-01 | Mandatory reject note captured in the same dialog (AMD-86); terminal/irreversible warning (BR-02); stale-action guard (F-10/BR-04) |

Notes:
- A **logical surface** (`LS-NN`) is a decomposition-agnostic unit of user-facing capability. A variant *realizes* each surface as physical screen(s) per its `surface_plan`. When every surface is realized `standalone-screen` (the default), `LS-NN` maps 1:1 to a single physical screen and the output matches a pre-realization run.
- Every row's `Sources` list is the set of requirement IDs this surface exists to satisfy. The variant-generators propagate these into `data-src` attributes on the surface's rendered element(s).
- Every row's `Properties` list is the **closed set** of object properties the surface may render, drawn exclusively from §7 data shapes. The variant-generator embeds `data-prop` attributes on each data-bound element; rendering a property outside this list is a self-validation FAIL. UI-only controls (search, sort, pagination, filter chips, expand/collapse, save/cancel buttons, progress indicators) are exempt from the property contract.
- `Allowed realizations` is the closed subset of realization strategies the architect deems valid for this surface (per `framework/assets/wireframes/realization-strategies.md`); `Default realization` (always including `standalone-screen`) is the baseline/`/prototype` pick; `Host surface` names the LS-NN a foldable surface folds onto, or `—`.

## Logical flow

LS-01 → LS-02 (open a transaction's detail); LS-01 → LS-03 (approve/reject a row); LS-03 → LS-01 on confirm; LS-03 ⟳ LS-03 on missing reject note.

(Flow is expressed over **logical surfaces** (LS → LS). Each variant derives its concrete physical flow from this plus its chosen realizations — a folded surface adds no standalone navigation node; a wizard-split surface adds intra-surface steps.)

## Pattern-coverage preflight

3 of 3 surfaces have a direct-match catalogue pattern for the primary slot — LS-01 → `collections/table`; LS-02 → `collections/detail-page` (standalone) / `collections/detail-panel` (inline-expand); LS-03 → `surfaces/modal-confirmation`. Verdict: ok; no AI-SUGGESTED gaps.

## Self-validation

| Check | Result |
|---|---|
| Bijection (every scope source referenced by ≥1 surface; no orphan surfaces) | PASS — all 19 F/BR/UI sources referenced; no orphan surface |
| Conflicts (no requirement pair foreclosing each other) | NONE |
| Properties (every property resolves to §7 or a cited F-NN's named parameter) | PASS — every Properties entry is a §7 Transaction field |

## Architect notes

3 logical surfaces consolidated from the in-scope decision queue. Goal G-02 (review and action approve/reject accurately) drives the flow; G-04 (find quickly via search/filter) and G-05 (status at a glance) shape LS-01's secondary intent. **Bulk multi-select actioning is excluded** (AMD-67 scopes it out of the prototype — no row multi-select, no bulk-action bar; `collections/table` is therefore bound without the `selectable` behaviour). Approve and reject share one confirmation surface (LS-03), with the mandatory reject note captured inside that dialog (AMD-86). LS-02 surfaces the non-column Transaction fields (TransactionType, Description, UserNote) per AMD-93's expandable-disclosure direction — its `inline-expand` allowed realization carries that amendment. LS-01 carries the file-scope cue + return path (AMD-91) and filter-driven post-action visibility (AMD-92) as secondary intent. The §7 User shape informs role-gating of LS-01's row actions (BR-05) and the PI-05 role switcher chrome; no User field is rendered as a queue column, so it binds no closed-set property. AMD-94's post-hoc action-audit modal is **out of this scope** — it is net-new (not tied to the in-scope F-NN sources) and depends on acting-user + action-timestamp fields that AMD-94 itself marks as PROPOSED ADDITIONS not yet in the §7 closed set; binding them would violate the no-invented-properties constraint.
