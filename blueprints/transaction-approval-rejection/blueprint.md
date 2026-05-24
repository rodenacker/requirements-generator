# Blueprint: transaction-approval-rejection

## Sources

Functional: F-08, F-09, F-10, F-11, F-12, F-15. Business rules: BR-01, BR-02, BR-07, BR-08, BR-10, BR-11. UI feature needs: UI-08, UI-09, UI-10, UI-11, UI-12. Goals: G-02, G-03. Task flows: §5 Transaction Table, §5 Approve Transaction, §5 Reject Transaction. Data shapes: §7 Transaction, §7 TransactionRejectWrite.

> `requirements.md` sha256 at scope-selection time: `8139af430390f934ea05d2691660fdbce12ceb7f7a86c0e4b05be2134f27b8c7`

## Available personas (from `requirements/requirements.md` §3)

- **Importer** — Daily frequency; Intermediate expertise; familiar with file-ingestion workflows. Wants reliable upload feedback and clear file-summary visibility. (No Approve/Reject permission per §6.5.)
- **Approver** — Daily frequency; Senior expertise; empowered to apply approve/reject decisions. Wants correct, auditable decisions; fears approving a wrong row or losing the rejection rationale.

## Screen inventory

| Screen ID | Intent | Sources | Properties | Secondary intent |
|---|---|---|---|---|
| S-01 | Transactions table | F-08, F-09, F-12, UI-08, UI-09, UI-10, BR-02, BR-10, G-02, §5 Transaction Table, §7 Transaction | Transaction.Reference, Transaction.TransactionDate, Transaction.AccountNumber, Transaction.Amount, Transaction.TransactionType, Transaction.Currency, Transaction.Status | with row-level Approve/Reject actions for Imported transactions (Approver only) |
| S-02 | Approve confirmation | F-10, F-15, BR-07, BR-11, UI-11, G-03, §5 Approve Transaction, §7 Transaction | Transaction.Reference, Transaction.AccountNumber, Transaction.Amount, Transaction.Currency, Transaction.Status | — |
| S-03 | Reject form | F-11, F-15, BR-01, BR-08, BR-11, UI-12, G-03, §5 Reject Transaction, §7 Transaction, §7 TransactionRejectWrite | Transaction.Reference, Transaction.AccountNumber, Transaction.Amount, Transaction.Currency, Transaction.Status, TransactionRejectWrite.UserNote | — |

Notes:
- Every row's `Sources` list is the set of requirement IDs this screen exists to satisfy. The variant-generators propagate these into `data-src` attributes on rendered elements.
- Every row's `Properties` list is the **closed set** of object properties the screen may render. Each entry resolves to a §7 data-shape property using `Shape.Property` notation. The variant-generator embeds `data-prop` attributes on each data-bound element naming the property it binds to; rendering a property outside this list is a self-validation FAIL. **UI-only controls (search, sort, pagination, filter chips, expand/collapse, save/cancel buttons, progress indicators) are exempt from the property contract and do not need a `data-prop` attribute.**
- Secondary intent is optional. When present, it captures a slot a variant may want to populate with a non-primary pattern.

## Flow

S-01 → S-02 → S-01 on approve confirmed; S-01 → S-03 → S-01 on reject submitted; S-02 → S-01 on cancel; S-03 → S-01 on cancel.

## Pattern-coverage preflight

3 of 3 screens have a direct-match catalogue pattern for the primary slot. S-01 maps to `collections/table` + `forms/search-and-filter`; S-02 maps to `surfaces/modal-confirmation`; S-03 maps to `surfaces/modal-form` + `forms/single-form`.

(Output of `framework/skills/check-pattern-coverage.md` run by the architect during design-brief preflight. A gap here would have fired the orchestrator's conditional gate; on a clean preflight this section is informational.)

## Self-validation

| Check | Result |
|---|---|
| Bijection (every scope source referenced; no orphan screens) | PASS |
| Conflicts (no requirement pair foreclosing each other) | NONE |
| Properties (every property resolves to §7 or a cited F-NN's named parameter) | PASS |

## Architect notes

3 screens consolidated from 19 sources covering the approval/rejection decision flow. S-01 is the shared entry surface (both Importer and Approver may view it per §6.5); S-02 and S-03 are decision dialogs visible only to the Approver per BR-10 / UI-09. Goals G-02 (review efficiency) and G-03 (auditable decisions) shape divergence across variants. Persona-binding fallback applied: both available personas (Importer, Approver) are daily-frequency, so domain-defaults.md Section 4 Rule 3 fires — both variants bind to `Approver` (alphabetically first AND the only persona with Approve/Reject permissions per §6.5). Per `tradeoff-dimensions-registry.md > Section 5`, daily personas hard-reject D3 density-focus ≤ -1; CAREFUL-DEFAULT's D3 position has been capped at 0 (neutral) rather than the canonical -1 to satisfy the constraint. Variants remain distinct on D3 (0 vs +2) and D1 (-1 vs +1).
