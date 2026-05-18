# Five Whys Justification Analysis — Financial services / banking back-office

Generated: 2026-05-16T08:12:04Z
Requirements SHA-256: 6f9272bbb30d1dce025b843f5319e790bdaa5ac2a07103204bbea7144694f0ae

## Summary

- Candidate requirements auto-extracted for rationale analysis: 5
- Category mix: 0 business goals, 1 op capability, 4 workflow constraints, 0 policy-driven, 0 no-category-match
- Consultant-stated requirements analysed: 0
- Total requirements analysed: 4
- Total why-levels: 13
- Root justifications identified (PASS Sufficiency Test): 4
- Incomplete chains (source exhausted or cap-reached): 0
- Coverage gaps: 1
- AI-suggested rows: 0 (0% density)

## Rationale-analysis priority scoring (Round 1)

| Rank | Requirement | Source | Detected categories (primary first) | §5 anchors | §4 anchors | Modal | Other refs | Depth | Impl-detail penalty | Score |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Allow Approvers to approve or reject individual transactions… | §6.1 F-06 | [OP-CAPABILITY], [WORKFLOW-CONSTRAINT] | 3 (§5 Approve Transaction, §5 Reject Transaction, §5 Transaction Table) | 3 (§4.1 G-02, §4.2 approve story, §4.2 reject story) | must | 2 (§2.3, §7) | 1 | 0 | 21 |
| 2 | When the authenticated role is Importer, then the Approve and… | §6.2 BR-03 | [WORKFLOW-CONSTRAINT], [POLICY-DRIVEN] | 3 (§5 Approve Transaction, §5 Reject Transaction, §5 Transaction Table) | 0 | must | 1 (§6.5 RBAC) | 1 | 0 | 17 |
| 3 | Require a mandatory user note for every rejection. | §6.1 F-07 | [WORKFLOW-CONSTRAINT], [POLICY-DRIVEN] | 1 (§5 Reject Transaction) | 1 (§4.2 reject story) | must | 2 (§2.3, §7 UserNote) | 1 | 0 | 15 |
| 4 | When a transaction's status is not Imported, then the Approve… | §6.2 BR-01 | [WORKFLOW-CONSTRAINT] | 3 (§5 Approve Transaction, §5 Reject Transaction, §5 Transaction Table) | 2 (§4.2 approve story, §4.2 reject story) | must | 1 (§2.3) | 1 | 0 | 15 |
| 5 | When an Approver rejects a transaction, then a non-empty user… | §6.2 BR-02 | [WORKFLOW-CONSTRAINT], [POLICY-DRIVEN] | 1 (§5 Reject Transaction) | 1 (§4.2 reject story) | must | 2 (§2.3, §7 UserNote) | 1 | 0 | 15 |

---

## Requirement 1 — Allow Approvers to approve or reject individual transactions `[OP-CAPABILITY]`

**Source:** `§6.1 F-06` (`from-§6` — auto-extracted)
**Detected categories:** op-capability (primary), workflow-constraint
**Statement** (verbatim): "Allow Approvers to approve or reject individual transactions while they are in the Imported state."

### Why chain R1

| Level | Why? | Answer | Evidence | Provenance |
|---|---|---|---|---|
| Requirement | — | Allow Approvers to approve or reject individual transactions while they are in the Imported state. | §6.1 F-06 | from-§6 |
| Why 1 | Why does this requirement exist? | To apply a two-stage human review before any approved record is consumed downstream. | §1 Business goal: *"Provide a controlled, file-driven pipeline for ingesting transactional records and applying a two-stage human review before any approved record is consumed downstream."* | from-requirements |
| Why 2 | Why apply a two-stage human review before downstream consumption? | Because mistakes propagate downstream — Approvers are personally accountable for every approval and rejections must carry a defensible reason. | §3 Approver Stakes: *"Personally accountable for every approval; rejections must carry a defensible reason. Mistakes propagate downstream."* | from-§3 |
| Why 3 | Why does downstream impact and personal accountability drive this design? | **Root justification: the system operates in the financial-services / banking back-office domain, where downstream consumers act on approved records and reversal is costly or impossible — pre-consumption human review is the immutable control.** | §1 Domain: *"Financial services / banking back-office"*; §1 Business goal: *"before any approved record is consumed downstream"*. | derived-from-§1 |

**Termination:** PASS — Justification Sufficiency Test satisfied: root names an axiomatic domain driver anchored in `§1` (financial-services back-office with downstream irreversibility). Going further would require leaving the requirements doc.

### Coverage check

Root justification `financial-services back-office domain irreversibility at downstream boundary` — `cited` (anchored in `§1 Domain`: *"Financial services / banking back-office"* and `§1 Business goal`: *"applying a two-stage human review before any approved record is consumed downstream"*).

---

## Requirement 2 — When role is Importer, hide Approve/Reject across the UI `[WORKFLOW-CONSTRAINT]`

**Source:** `§6.2 BR-03` (`from-§6` — auto-extracted)
**Detected categories:** workflow-constraint (primary), policy-driven
**Statement** (verbatim): "When the authenticated role is Importer, then the Approve and Reject actions must be hidden across the UI."

### Why chain R2

| Level | Why? | Answer | Evidence | Provenance |
|---|---|---|---|---|
| Requirement | — | When the authenticated role is Importer, then the Approve and Reject actions must be hidden across the UI. | §6.2 BR-03 | from-§6 |
| Why 1 | Why does this requirement exist? | Because the Importer role is not authorised to approve or reject — only Approvers are; the RBAC matrix gives Importer `—` for Approve Transaction and Reject Transaction. | §3 Importer: *"A user authorised to upload files and view transactions, but not to approve or reject."*; §6.5 RBAC matrix row (Importer × Approve Transaction = `—`; Importer × Reject Transaction = `—`). | from-requirements |
| Why 2 | Why is the Importer role denied approve/reject authority? | Because the system implements role separation between the uploader and the approver — the same principal cannot both submit a transaction (via Importer) and authorise it (via Approver). | §1 Business goal: *"applying a two-stage human review"*; §3 distinguishes Importer (uploads, views) from Approver (reviews, approves, rejects, exports). | derived-from-§1 |
| Why 3 | Why role separation between uploader and approver? | **Root justification: segregation of duties is the regulated control for financial-services back-office workflows — authoring an action and authorising it must be performed by different principals.** | §1 Domain: *"Financial services / banking back-office"*; §6.6.4 Compliance & audit (POPIA + 7-year audit retention); §6.6.1 step-up authentication for approve/reject. | derived-from-§1 |

**Termination:** PASS — Justification Sufficiency Test satisfied: root names a regulated-control driver anchored in `§1` Domain and `§6.6.4` compliance. Going further would require interview data on the specific regulatory regime the consultant designs against.

### Coverage check

Root justification `segregation of duties is a regulated control for financial-services authoring/authorising separation` — `gap` — the phrase *segregation of duties* is not used verbatim anywhere in `§1`, `§6.6.1`, or `§6.6.4`; the principle is implied by the *"two-stage human review"* phrase and the Importer/Approver role split, but the named root is not anchored. **Consultant should add an explicit cite to §1 Application context or §6.6.4 Compliance & audit naming segregation-of-duties as the driver, then re-run `/requirements` + `/analyse-requirement five-whys` to verify the gap is closed.**

---

## Requirement 3 — Mandatory user note on every rejection `[WORKFLOW-CONSTRAINT]`

**Source:** `§6.1 F-07` (`from-§6` — auto-extracted)
**Detected categories:** workflow-constraint (primary), policy-driven
**Statement** (verbatim): "Require a mandatory user note for every rejection."

### Why chain R3

| Level | Why? | Answer | Evidence | Provenance |
|---|---|---|---|---|
| Requirement | — | Require a mandatory user note for every rejection. | §6.1 F-07 | from-§6 |
| Why 1 | Why does this requirement exist? | To capture the rejection rationale for audit. | §4.2 Approver story (reject): *"As an Approver, I want to reject a transaction with a mandatory note, so that the rejection rationale is captured for audit."* | from-requirements |
| Why 2 | Why must the rejection rationale be captured for audit? | Because the system maintains an audit trail of every approve / reject / upload / login / logout event with `LastChangedUser` and `LastChangedDate`, retained for 7 years. | §6.6.4 Compliance & audit: *"Audit trail: every approve, reject, upload, login, and logout event is recorded with `LastChangedUser` and `LastChangedDate`; retain 7 years."* | from-§6.6.4 |
| Why 3 | Why a 7-year audit retention of approve/reject events? | **Root justification: POPIA (South Africa, anchored in §6.6.4 by the ZAR-currency sample dataset) and the financial-services regulatory baseline for transactional audit records mandate multi-year retention of who-decided-what evidence.** | §6.6.4 Compliance & audit: *"POPIA (South Africa) — implied by the use of ZAR currency in the sample dataset and South African account-number formats."*; §1 Domain: *"Financial services / banking back-office"*. | derived-from-§6.6.4 |

**Termination:** PASS — Justification Sufficiency Test satisfied: root names a regulatory mandate (POPIA + financial-services audit baseline) anchored in `§6.6.4`. Going further would require external citation of the specific POPIA / FCA / SOX article requiring 7-year retention.

### Coverage check

Root justification `POPIA + financial-services regulatory baseline mandating 7-year audit-record retention of approve/reject events` — `cited` (anchored in `§6.6.4 Compliance & audit`: *"POPIA (South Africa)…"* and *"Audit trail: every approve, reject, upload, login, and logout event is recorded with `LastChangedUser` and `LastChangedDate`; retain 7 years."*).

---

## Requirement 4 — Hide Approve/Reject when status is not Imported `[WORKFLOW-CONSTRAINT]`

**Source:** `§6.2 BR-01` (`from-§6` — auto-extracted)
**Detected categories:** workflow-constraint (primary)
**Statement** (verbatim): "When a transaction's status is not Imported, then the Approve and Reject row actions must be hidden."

### Why chain R4

| Level | Why? | Answer | Evidence | Provenance |
|---|---|---|---|---|
| Requirement | — | When a transaction's status is not Imported, then the Approve and Reject row actions must be hidden. | §6.2 BR-01 | from-§6 |
| Why 1 | Why does this requirement exist? | Because the Transaction aggregate invariant restricts the Approve and Reject actions to the Imported state. | §2.3 Transaction invariant: *"Approve and reject are only available while the transaction is in Imported state. Rejection requires a mandatory user note."* | from-§2.3 |
| Why 2 | Why are Approve and Reject restricted to the Imported state? | Because the Transaction lifecycle is `Imported → Approved \| Rejected` — Approved and Rejected are terminal states from which no further approve/reject transition is valid. | §2.3 Transaction lifecycle states: *"Imported → Approved \| Rejected"*. | derived-from-§2.3 |
| Why 3 | Why are Approved and Rejected terminal states? | Because once a transaction is approved, downstream consumers may act on it; reversing the decision must go through a separate workflow rather than re-toggling status on the same record. | §1 Business goal: *"before any approved record is consumed downstream"*. | derived-from-§1 |
| Why 4 | Why does the system protect against re-toggling decided transactions? | **Root justification: the system operates in the financial-services / banking back-office domain, where downstream record flows are irreversible at the consumer boundary and any reversal carries an independent control surface.** | §1 Domain: *"Financial services / banking back-office"*; §1 Business goal: *"before any approved record is consumed downstream"*. | derived-from-§1 |

**Termination:** PASS — Justification Sufficiency Test satisfied: root names an axiomatic domain driver anchored in `§1` (financial-services back-office with downstream irreversibility). Going further would require leaving the requirements doc.

### Coverage check

Root justification `financial-services back-office domain irreversibility at downstream consumer boundary` — `cited` (anchored in `§1 Domain`: *"Financial services / banking back-office"* and `§1 Business goal`: *"before any approved record is consumed downstream"*).

---

## Diagnostics

- Quality checks: 10/10 pass
  - PASS: check-1 (every requirement sourced to §6.N), check-2 (Round 1 scoring captured for all 5 candidates), check-3 (every retained chain has ≥ 1 why-row), check-4 (every why-row carries exactly one provenance marker), check-5 (every why-row has non-empty Evidence), check-6 (no blame tokens — no *user error*, *operator failed*, *negligence*, *carelessness*, *stupidity*, *incompetence*), check-7 (no self-loops — Jaccard between consecutive answers below 0.80 on every chain), check-8 (every chain terminates exactly once — 4× PASS), check-9 (caps respected — 5 candidates auto-extracted, 0 chains exceed 7 levels, 0 branches), check-10 (every coverage row ∈ {cited, gap, n/a}).
- AI-suggested density: 0% (0 / 13 why-rows).
- Cross-requirement links:
  - R1 (F-06) and R4 (BR-01) share root justification *"financial-services back-office domain irreversibility at downstream boundary"* — consider documenting the shared driver explicitly in `§1 Application context` so the two requirements can ladder up to one cited root rather than two derived ones, or consolidating their treatment in §6.
- Coverage gaps: 1 chain terminated at a root justification not anchored verbatim in §1 or §6.
  - R2 (BR-03): root *"segregation of duties is a regulated control"* — concept is implied by §1 *"two-stage human review"* + §3 Importer/Approver role split + §6.6.4 audit retention, but the phrase *segregation of duties* is not used verbatim anywhere in the requirements doc. Recommended consultant action: add an explicit cite in §1 Application context or §6.6.4 Compliance & audit naming segregation-of-duties as the policy driver, then re-run `/requirements` + `/analyse-requirement five-whys` to verify the gap is closed.

## Round 2 surfacing note

`AskUserQuestion` caps options at 4; the methodology surfaces the top 5. The 4 highest-scoring candidates (F-06 / BR-03 / F-07 / BR-01) were surfaced as direct options; the 5th candidate (BR-02, score 15, [WORKFLOW-CONSTRAINT] + [POLICY-DRIVEN]) was named verbatim in the prompt question with a path to add via Other. The consultant declined to add it. The Round 1 scoring table above preserves all 5 candidates with their full breakdowns — auditing invariant unaffected. BR-02 ("When an Approver rejects a transaction, then a non-empty user note must be supplied") is closely related to F-07 (R3 above); its justification chain would terminate at the same POPIA + audit-retention root.
