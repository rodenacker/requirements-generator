# Prototype design spec: Approval Queue — Dense

```json
{
  "name_slug": "approval-queue-dense",
  "prototype_name": "Approval Queue — Dense",
  "scope_slug": "approval-queue",
  "posture": "P3",
  "posture_label": "Analytical / Information-Dense",
  "dimension_positions": { "D1": 0, "D2": 0, "D3": 2, "D4": 0, "D5": 0, "D6": 0 },
  "primary_persona": "Importer",
  "route": "/approval-queue-dense",
  "wireframe_basis": "DENSE-LEAN",
  "created_at": "2026-06-15T08:51:20Z"
}
```

**Provenance:** `[SRC: …]` tags are retained as the generator's provenance — requirement IDs (`F-NN`/`BR-NN`/`UI-NN`), data shapes (`§7.Shape`), blueprint surfaces (`LS-NN`), the wireframe-variant basis (`WF:DENSE-LEAN`), and explicit consultant directives (`consultant`). All resolution markers have been applied and stripped (zero `[AI-SUGGESTED]`, zero posture-default markers remain).

> **Post-build amendment — AMD-94 action-audit (consultant-confirmed 2026-06-15).** After the run completed, the consultant directed adding the acting user + action date/time for approved/rejected transactions (AMD-94). This **reverses §1's out-of-scope exclusion of AMD-94** and **extends the §7 Transaction closed set** with two properties — `Transaction.ActionedBy` (the active chrome role that actioned the row; AMD-62/AMD-71 keep named users out of frontend scope) and `Transaction.ActionedAt` (timestamp, `YYYY-MM-DD HH:mm`). Surfaced as an **Action audit** block in the LS-02 detail/View modal, shown only for Approved/Rejected rows; values are set in `transaction-store` on approve/reject (simulated clock, PI-01) and backfilled on the 5 pre-actioned fixture rows. requirements.md §7 still carries these as AMD-94 **PROPOSED ADDITIONS** — **run `/resolve-review` to formalise AMD-94 into requirements.md + the blueprint closed set** so the contract and prototype reconcile. Verify gate re-run green (lint + tsc + build + smoke).

---

## 1. Scope

| Field | Value |
|---|---|
| Requirement IDs in scope | F-02 [SRC: F-02], F-05 [SRC: F-05], F-06 [SRC: F-06], F-07 [SRC: F-07], F-08 [SRC: F-08], F-09 [SRC: F-09], F-10 [SRC: F-10], F-13 [SRC: F-13], F-14 [SRC: F-14]; BR-01 [SRC: BR-01], BR-02 [SRC: BR-02], BR-03 [SRC: BR-03], BR-04 [SRC: BR-04], BR-05 [SRC: BR-05], BR-07 [SRC: BR-07]; UI-03 [SRC: UI-03], UI-04 [SRC: UI-04], UI-05 [SRC: UI-05], UI-07 [SRC: UI-07]; G-02 [SRC: G-02], G-04 [SRC: G-04], G-05 [SRC: G-05]; data shapes §7 Transaction [SRC: §7.Transaction], §7 User [SRC: §7.User] |
| Logical surfaces (from blueprint) | **LS-01** Transaction review queue [SRC: LS-01]; **LS-02** Transaction detail — non-column fields [SRC: LS-02]; **LS-03** Approve/reject confirmation [SRC: LS-03] |
| Out of scope (explicit) | File upload (F-03/UI-01), file-log overview screen (F-04/UI-02 — only the file-scope cue + return path is retained on LS-01, AMD-91), CSV export (F-11/UI-06), authentication screens (F-01/F-15/F-16), file summary report (F-12/RPT-01), bulk multi-select actioning (excluded per blueprint AMD-67 — no row multi-select, no bulk-action bar), post-hoc action-audit modal (AMD-94, net-new, depends on properties not in the §7 closed set) |

## 2. Purpose

A clickable, client-side prototype of the approval-queue surface for an internal transaction-review app. It shows a dense, scannable transaction table (DENSE-LEAN basis) where reviewers search, filter, page, and inspect transactions, then approve or reject each via a confirmation modal (mandatory reason on reject). The transaction detail opens in a centred modal dialog rather than inline.

It lets the consultant experience one specific question: can a high-volume reviewer scan many imported transactions in a dense table, drill into a single record's detail in a focused modal, and action it (approve/reject with mandatory reason) — without the detail competing for space inside the dense rows?

## 3. UX posture & rationale

| Field | Value |
|---|---|
| Posture | Analytical / Information-Dense |
| Why it fits | The primary persona reviews transactions regularly per cycle and needs to read across many records to verify a file and spot what to action [SRC: §3.Importer]. The dense, scannable table maximises records-in-view for G-04 *find quickly via search and filter* [SRC: G-04] and G-05 *status at a glance* [SRC: G-05]; the Approver's *efficient review with clear status and quick actions* is served by the same dense layout with role-gated approve/reject [SRC: §3.Approver]. P3 is dense to *see relationships* (scan/compare rows), which matches a review queue better than a single-record focus posture. |
| Principles emphasized | Gestalt proximity/similarity/alignment to keep density legible; N1 visibility of system status (active filters/sorts always shown); N6 recognition over recall (visible facets, status chips); status never colour-alone (GR-16). |

## 4. Trade-off positions (design parameters)

| Dim | Position | Plain-English label | Basis |
|---|---|---|---|
| D1 speed-accuracy | 0 | Balanced | [SRC: WF:DENSE-LEAN] |
| D2 power-simplicity | 0 | Balanced | [SRC: WF:DENSE-LEAN] |
| D3 density-focus | +2 | Maximally dense | [SRC: WF:DENSE-LEAN] |
| D4 control-automation | 0 | Balanced | [SRC: WF:DENSE-LEAN] |
| D5 flexibility-consistency | 0 | Balanced | [SRC: WF:DENSE-LEAN] |
| D6 memorability-discoverability | 0 | *(inactive)* | stance captured in §6 disclosure prose |

> Positions adopt the DENSE-LEAN basis variant's single-axis profile (density-focus at the dense pole, every other dimension neutral) — the "mainly DENSE-LEAN" intent confirmed by the consultant at Step B, not the full P3 preset. Re-checked against `tradeoff-dimensions-registry.md §4/§5`: density-focus +2 with all other dimensions neutral raises no incoherent pair (D2×D3 density-vs-novice-spacious needs a novice-leaning D2; D2 = 0) and no §5 persona hard rule (daily/intermediate reviewer); coherent — no reconciliation needed.

**Structural choices implied** (P3 recommendations, moderated by the neutral D1/D2/D4/D5): navigation — persistent left sidebar + a visible filter/facet rail; primary data display — dense compact table (`collections/table` + `wf-table--compact`), sticky header, sort, colour-coded status chips; input philosophy — standard affordances (D2 = 0, not expert-only chrome); reading is primary, editing is the gated approve/reject action; disclosure — everything-visible at the summary row, drill into a single record's detail on demand (centred modal — see §5 LS-02); feedback/confirmation — standard, with a deliberate confirmation gate on the consequential approve/reject (D1 = 0, neutral); keyboard/bulk — row keyboard navigation present, **bulk de-emphasised** (multi-select excluded per blueprint AMD-67).

## 5. Per-surface realization decisions

### LS-01 — Transaction review queue

| Field | Value |
|---|---|
| Realization | standalone-screen [SRC: WF:DENSE-LEAN] |
| Host (if folded) | — |
| Why | The primary collection is its own screen; DENSE-LEAN realizes it standalone with a compact, high-density table for fast scanning of the batch [SRC: WF:DENSE-LEAN]. Carries search/filter (F-07/UI-03), client-side pagination (UI-07), status chips (F-14/UI-05), masked AccountNumber (F-13/BR-07), role-gated row actions (BR-05/BR-01), and the file-scope cue + return path (F-05). |

### LS-02 — Transaction detail (non-column fields)

| Field | Value |
|---|---|
| Realization | modal [SRC: consultant] |
| Host (if folded) | LS-01 · host_state `detail-modal-open` (rendered on the queue screen; no own route) |
| Why | **Consultant-directed divergence (captured at Step B).** DENSE-LEAN realizes this surface `inline-expand` (detail expands within the row); the consultant explicitly chose a **centred modal dialog** so the detail opens in a focused overlay rather than competing for space inside the dense rows. This diverges both from the DENSE-LEAN basis (`inline-expand`) **and** from LS-02's blueprint allowed-realizations (`standalone-screen, inline-drawer, inline-expand` — `modal` is the architect's reserved capture/confirm realization). The divergence is honoured because the prototype holds design authority over the *how* and the choice is an explicit consultant directive. **Property contract preserved per realization-strategies §3:** the modal sub-tree still stamps LS-02's closed-set `data-prop`s (Transaction.TransactionType, Transaction.Description, Transaction.UserNote) — see §8. The modal is **read-only** (detail disclosure), distinct from the action modal LS-03. |

> **Divergence note (for the resolver/merger + the generator):** LS-02 realization = `modal` is outside the reused blueprint's `allowed_realizations[LS-02]`. It is recorded as a consultant directive, not an architect pick. No blueprint edit was made (the blueprint is shared/reused). The generator renders a read-only detail modal using the `surfaces/modal-form` shell with read-only fields (no inputs), opened from a row "View" affordance on LS-01.

### LS-03 — Approve/reject confirmation

| Field | Value |
|---|---|
| Realization | modal [SRC: WF:DENSE-LEAN] |
| Host (if folded) | LS-01 · host_state `confirm-modal-open` (rendered on the queue screen; no own route) |
| Why | Both wireframe variants realize the approve/reject confirmation as a modal; it is the consequential-action gate [SRC: WF:DENSE-LEAN]. Approve and reject share one dialog (blueprint AMD-86) with the **mandatory reject note captured inside the dialog** (BR-03) [SRC: BR-03]; the dialog restates the terminal/irreversible nature (BR-02) [SRC: BR-02] and guards a stale/already-actioned transaction (F-10/BR-04) [SRC: F-10]. `surfaces/modal-confirmation` with an input. |

## 6. Interaction & workflow flows

**Flow 1: Scan & filter the queue** [SRC: §5 Flow: Search & Filtering / F-07]
1. Open `/approval-queue-dense` → LS-01 dense table renders with reference, date, masked account, amount, currency, status chip [SRC: F-06].
2. Apply status / file / date-range / amount-range / free-text filter → matching rows remain, active filters shown [SRC: UI-03]; client-side over the full list.
3. No matches → no-results state showing active filters + a clear-all action [SRC: §6.4.5].

**Flow 2: Inspect a transaction's detail** [SRC: LS-02 / F-06]
1. On a row, click **View** → centred detail modal opens (`detail-modal-open`) [SRC: consultant].
2. Modal shows the non-column fields: TransactionType (chip), Description, UserNote (read-only) [SRC: §7.Transaction].
3. Close / Esc → return to the queue (modal dismissed; N3 user control & freedom).

**Flow 3: Approve a transaction** [SRC: §5 Flow: Approve Transaction / F-08]
1. As Approver, on an **Imported** row, click **Approve** → confirmation modal (`confirm-modal-open`) restating reference, amount, status [SRC: F-08].
2. Confirm → status becomes Approved, reflected within ~1s; success feedback (NT-02) [SRC: F-08].
3. Guard: a non-Imported row offers no approve/reject (BR-01) [SRC: BR-01]; an already-actioned row shows a stale-action notice (F-10/BR-04) [SRC: F-10].

**Flow 4: Reject a transaction with a mandatory note** [SRC: §5 Flow: Reject Transaction / F-09]
1. As Approver, on an Imported row, click **Reject** → the shared confirmation modal presents a note field [SRC: F-09].
2. Submit with empty note → blocked, inline required-note error (BR-03) [SRC: BR-03].
3. Enter note → submit → status becomes Rejected, note recorded [SRC: F-09].

**Flow 5: Role-gated visibility** [SRC: BR-05 / §6.5]
1. Active role = Importer → approve/reject hidden on every row (BR-05); View + read remain [SRC: BR-05].
2. Active role = Approver → approve/reject offered on Imported rows only [SRC: UI-04].
3. The role is switched via the prototype chrome role switcher (PI-05), not an in-app control.

**Navigation model:** persistent left sidebar (dataset/role context) + a visible filter rail on the queue; the queue is the single primary screen, detail and actions are modal overlays on it.
**Disclosure model:** everything-visible at the summary row; single-record detail and consequential actions are drilled on demand via centred modals (carries the recall-leaning D6 stance while D6 is inactive — facets and status stay visible, detail is one click away).

## 7. Component inventory (shared set)

| Surface | Shared components composed | Reuse / New | Atomic tier (if new) |
|---|---|---|---|
| LS-01 | `DataTable` (dense/compact variant), `SearchFilterBar`, `StatusChip`, `Pagination`, `EmptyState`, `TableSkeleton`, `Button`, `MaskedValue` | new (authored into shared library) | organism (DataTable); molecule (SearchFilterBar, Pagination, EmptyState); atom (StatusChip, TableSkeleton, Button, MaskedValue) |
| LS-02 | `Modal` (read-only detail variant), `DescriptionList`, `StatusChip` (reuse) | `Modal`/`DescriptionList` new; `StatusChip` reuse | organism (Modal); molecule (DescriptionList) |
| LS-03 | `ConfirmModal` (composes `Modal`), `Textarea`, `InlineError`, `Button` (reuse), `StatusChip` (reuse) | `ConfirmModal`/`Textarea`/`InlineError` new; `Button`/`StatusChip` reuse | organism (ConfirmModal); atom (Textarea, InlineError) |

> Rule 15: every task component is authored into the **shared** library (atoms/molecules/organisms/templates/domain), never private to this prototype. The role switcher, data-reset, and scope/purpose/posture metadata are **prototype chrome** (PI-08) — outside the application UI, no `data-src`/`data-prop`.

## 8. Data binding (anti-fabrication contract)

| Surface | Property (closed set) | Fixture field | Store |
|---|---|---|---|
| LS-01 | Transaction.Reference [SRC: §7.Transaction] | `transactions[].Reference` | `useTransactionsStore` |
| LS-01 | Transaction.TransactionDate [SRC: §7.Transaction] | `transactions[].TransactionDate` | `useTransactionsStore` |
| LS-01 | Transaction.AccountNumber (masked, F-13/BR-07) [SRC: §7.Transaction] | `transactions[].AccountNumber` | `useTransactionsStore` |
| LS-01 | Transaction.Amount [SRC: §7.Transaction] | `transactions[].Amount` | `useTransactionsStore` |
| LS-01 | Transaction.Currency [SRC: §7.Transaction] | `transactions[].Currency` | `useTransactionsStore` |
| LS-01 | Transaction.Status (chip, F-14) [SRC: §7.Transaction] | `transactions[].Status` | `useTransactionsStore` |
| LS-02 | Transaction.TransactionType (chip) [SRC: §7.Transaction] | `transactions[].TransactionType` | `useTransactionsStore` |
| LS-02 | Transaction.Description [SRC: §7.Transaction] | `transactions[].Description` | `useTransactionsStore` |
| LS-02 | Transaction.UserNote [SRC: §7.Transaction] | `transactions[].UserNote` | `useTransactionsStore` |
| LS-03 | Transaction.Reference [SRC: §7.Transaction] | `transactions[].Reference` | `useTransactionsStore` |
| LS-03 | Transaction.Amount [SRC: §7.Transaction] | `transactions[].Amount` | `useTransactionsStore` |
| LS-03 | Transaction.Status [SRC: §7.Transaction] | `transactions[].Status` | `useTransactionsStore` |
| LS-03 | Transaction.UserNote (reject note input) [SRC: §7.Transaction] | `transactions[].UserNote` | `useTransactionsStore` |

> Every property above is a member of its surface's blueprint closed set (LS-01: Reference, TransactionDate, AccountNumber, Amount, Currency, Status; LS-02: TransactionType, Description, UserNote; LS-03: Reference, Amount, Status, UserNote). **No invented fields.** `Status` enum ∈ {Imported, Approved, Rejected}; `TransactionType` ∈ {Credit, Debit} [SRC: §7.Transaction]. Role-gating reads the active role (User.Role ∈ {Importer, Approver}) from the chrome (PI-05) — no User field is rendered as a queue column, so §7 User binds no displayed closed-set property [SRC: §7.User]. Fixtures: `fixtures/transactions.json` (§6.10), with `fixtures/transaction-approve.json` / `fixtures/transaction-reject.json` driving the simulated action results (PI-01/PI-06).

## 9. Accessibility & UX-principle checklist (from `ux-baseline-checklist.md`)

- [ ] Keyboard: table rows and the View / Approve / Reject affordances reachable and operable by keyboard; modals trap focus and restore it on close.
- [ ] Focus visible & not obscured (incl. inside modals; not hidden behind the sticky header).
- [ ] Name/role/value on all controls (filter inputs, row actions, modal buttons, note textarea).
- [ ] Three states (empty / loading / error) on the transaction table and on the approve/reject async action — skeleton table on load, no-results state with active filters + clear-all, plain-language error.
- [ ] Not colour-alone for status (GR-16): status chips carry a label + colour (Imported / Approved / Rejected); TransactionType chip carries the word Credit / Debit.
- [ ] Role switcher present (PI-05) — Importer / Approver, in the prototype chrome; switching updates visible row actions per BR-05.
- [ ] **P3-emphasized:** density stays legible via alignment/grouping (Gestalt); active filters & sort always visible (N1); masked AccountNumber shows only its last group of digits (F-13/BR-07).

## 10. Success criteria

- A high-volume reviewer can scan many transactions in a dense table, filter to a target set within a few actions [SRC: G-04], read status at a glance via chips [SRC: G-05], and open a single record's detail in a focused modal without losing the queue.
- An Approver can approve/reject an Imported transaction accurately through a confirmation gate, with a mandatory note on reject [SRC: G-02]; role-gating hides those actions from an Importer [SRC: BR-05].
- [ ] Playwright smoke: route `/approval-queue-dense` loads, no console errors, primary CTA (a row action / View) clickable; the detail modal and the approve/reject modal open and close.
- [ ] `npm run lint` + `tsc --noEmit` + `next build` pass.

## 11. Prototype invariants checklist

- [ ] PI-01 — All server-side behaviour — authentication, API calls, database operations, third-party integrations, scheduled jobs — is simulated by client-side stubs.
- [ ] PI-02 — All data displayed in the prototype is sourced from in-memory fixtures shipped with the build.
- [ ] PI-03 — Form-field validation messages and inline error feedback are rendered as specified by the requirements, but no server-side enforcement is exercised.
- [ ] PI-04 — Email, SMS, payment, mapping, file storage, and analytics integrations appear in the UI as visual confirmations or placeholder content.
- [ ] PI-05 — Every screen accessible to more than one role displays a role switcher in the prototype's surrounding chrome — outside the application UI under design — so reviewers can inspect each role's view without re-authenticating.
- [ ] PI-06 — Under the prototype target, the §6.10 fixture references *are* the backend; the §7 data shapes are the contract.
- [ ] PI-07 — §6.7 reporting feature needs render from fixture aggregates only.
- [ ] PI-08 — The prototype's surrounding chrome — role switching (PI-05), data reset, prototype metadata (scope / purpose / posture), and navigation between generated prototypes — sits **outside** the application UI under design and is **not part of any requirement**.
