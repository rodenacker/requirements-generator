# completeness-gap-pass.md

**Purpose:** Walk a populated requirements draft against the relatedness graph (Tier A/B/D rules) and the prototype scope boundary, decide for each gap whether to fabricate the missing element with `[AI-SUGGESTED]`, apply a deterministic answer from `general-rules.md` with `[STANDARD-RULE]`, or fill with a domain default tagged `[OUT-OF-SCOPE: domain-default]`. Used by the requirements-drafter at workflow step 5 (post-fill, pre-write-final).

**Inputs:**
- The in-memory populated draft (template-requirements.md filled top-to-bottom from inputs and domain defaults; **no `[AI-SUGGESTED]` markers yet**).
- `target` — exactly one of `"prototype"` or `"application"`. Sourced from `requirements/source-manifest.json > target` (auto-set to `"prototype"` by the orchestrator's Step 1b; `"application"` occurs only on legacy manifests). Governs whether `[OUT-OF-SCOPE: domain-default]` markers are emitted (`prototype`) or suppressed (`application`) — nothing else. **Does not change the set of `[AI-SUGGESTED]` outputs** — the same fields are AI-SUGGESTED under both targets.
- `framework/shared/prototype-scope.md` — in-scope vs out-of-scope predicate. Consulted under both targets to identify which fields are historically out-of-prototype-scope; the decision is then routed to "emit OOS marker" (prototype) or "fill with domain default, emit no marker" (application).
- `framework/shared/general-rules.md` — catalogue of `GR-NN` deterministic rules.
- `framework/assets/topics-requirements.md` — bijection invariants.

**Outputs:**
- A list of `(rule_id, location, action, marker_kind, marker_payload, draft_context, priority_score)` tuples that the drafter applies to the draft via Edit / Write.
- The next-available `AI-NNN` index, continuing the existing counter.

`draft_context` is a single, optional, one-line string emitted on tuples whose `marker_kind = "AI-SUGGESTED"` (only). It is a brief, plain-English orientation for the consultant — what the field represents, what kind of answer is expected, and (when useful) the candidate value set — phrased so the consultant can answer without re-locating the cell in the draft. Example for an RBAC matrix cell: `"RBAC matrix cell — what access does the Importer role need to the User entity? (typical answers: R = Read, X = none, C = Create, U = Update)"`. Tuples with `marker_kind ∈ {"STANDARD-RULE", "OUT-OF-SCOPE", "none"}` do not carry `draft_context` (those markers do not surface to the resolver's Q&A). The drafter is the sole author of `draft_context`; the resolver copies it onto the manifest line on first turn (per `framework/agents/requirements-resolver.md > Working state`) and never invents one. A tuple that is **demoted** by the cap step (see Algorithm step 6) has its `draft_context` cleared along with its `marker_kind` change to `"none"`.

`priority_score` is an integer in `0..10` assigned to every tuple. Tuples with `marker_kind = "AI-SUGGESTED"` carry a real score per the Priority scoring table below; tuples with any other `marker_kind` carry `priority_score = 0` (unused). Consumed only by the cap step at the end of the algorithm — the drafter does not write it into the draft body.

## Priority scoring (consumed by the cap step)

Every tuple whose decision tree resolves to `marker_kind = "AI-SUGGESTED"` is assigned a `priority_score` (integer, 0–10) drawn from the closed table below. The score is keyed on the `rule_id` that emitted the tuple — A1..A15, B1..B7, D1..D4. Tuples whose `marker_kind` is not `"AI-SUGGESTED"` carry `priority_score = 0` and the score is unused.

| Rule(s) | Score | Rationale |
|---|---|---|
| A1 personas↔stories · A3 personas↔RBAC · A9 §10 volumes · A10 §1.5 In-scope rows · A13 §6.8 notification audiences | 10 | Cross-cuts UI pattern choice and drives §6.5 / §6.7 / §6.8 — wrong guesses propagate. |
| A2 goals↔stories · A8 §5 flow actors · A11 §2.5 state-transition rows · A12 §6.7 report source concepts · D3 visible state-transition effects | 7 | Drives flow logic and UI narrative; revision is bounded but costs design rework. |
| A14 §6.10 operations · B2 conditional `<action>†BR-NN` rows · B5 acceptance-criteria fabrications | 5 | Behavioural detail. Adjustable post-hoc; surfacing is valuable but not load-bearing. |
| A4 entity-RBAC columns · A5 flow-RBAC columns · A6 persistent entity stubs · A7 entity↔concept refs · A15 §7.X derived shapes · B1 goal→story filler · B7 §6.6.1/§6.6.2 guidance fields · D1 server-side §6.2 BR projections · D2 hidden-field defaults | 3 | Bijection-filler / scope-noted application-build guidance — structural completeness, low decision-value per item. The set that the cap demotes first. |

Tier C is never AI-SUGGESTED (it routes to `[OUT-OF-SCOPE]` or value-only by target), so it has no row here. Tier B3 (warn-only), B4 (warn-only), and B6 (warn-only; priority is filled by `GR-24` as `[STANDARD-RULE]`) emit no AI-SUGGESTED tuples, so they have no row either.

The table is the **closed set** of priority scores. Adding a new Tier A/B/D rule to this skill must include an explicit row here when the rule ships; otherwise the cap step has no basis to rank that rule's tuples and they would tie at score 0 (sorted last among AI-SUGGESTED items, demoted first).

## Decision tree (per gap)

For every field or element required by the template that is not directly stated in the inputs, walk these steps in order. Stop at the first match.

1. **Stated-in-inputs.** If the inputs supply the value, use it verbatim. **No marker.** (Handled by drafter step 3, not by this skill — included for completeness.) Identical under both targets.
2. **General-rules lookup.** Read `framework/shared/general-rules.md`. If a `GR-NN` rule's scope predicate matches this field/element, apply the rule's canonical answer. Marker: `[STANDARD-RULE: GR-NN]`. Identical under both targets.
3. **Completeness-required (Tier A/B).** If the field/element is required by a Tier A or Tier B rule below:
    - Tier A or B1/B2 → fabricate the missing element. Marker: `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` per the drafter's classification rubric (`requirements-drafter.md > Classification`). Identical under both targets.
    - B3 → emit a soft warning to the drafter's gap-pass log. **No fabrication, no marker.** Identical under both targets.
4. **In-scope per prototype-scope.md.** If completeness-required AND in-scope, fall through to step 3 (already covered). If completeness-required but **out-of-scope** per `framework/shared/prototype-scope.md`, fill with a domain default. **Marker depends on `target`:**
    - `target == "prototype"` → marker `[OUT-OF-SCOPE: domain-default]`.
    - `target == "application"` → **no marker**. The value is filled with the same domain default that prototype mode would have used; the OOS marker is suppressed because application builds carry no prototype scope filter.
5. **Not completeness-required, not stated.** Fill with a domain default. **Marker depends on `target`:**
    - `target == "prototype"` → marker `[OUT-OF-SCOPE: domain-default]`.
    - `target == "application"` → **no marker**. Same domain default as prototype mode; OOS marker suppressed.

The Tier C sections below are short-circuited at step 4 — they are completeness-required by the template (`fill every field`) but explicitly out-of-prototype-scope. Under `target == "prototype"` they carry `[OUT-OF-SCOPE: domain-default]`; under `target == "application"` they carry the same domain-default values with **no marker**. The set of `[AI-SUGGESTED]` fields is identical under both targets — Tier C is never AI-SUGGESTED in either mode, and Tier A/B fabrications stay AI-SUGGESTED in both modes.

## Tier A — hard bijections (gap → fabricate + `[AI-SUGGESTED]`)

| # | Rule | Fabrication action |
|---|---|---|
| A1 | Every §3 persona has ≥1 story in §4.2 | create story under persona heading; set `Goal: → §4.1 G-NN` (creating a goal via A2 if needed) |
| A2 | Every §4.2 story references exactly one §4.1 goal-id | create new `G-NN` row in §4.1 with inferred goal statement |
| A3 | Every §3 persona is a row in §6.5 RBAC | add row; per-cell `[AI-SUGGESTED]` on inferred CRUD/X/A/— values |
| A4 | Every §7 entity is a column (or scoped action) in §6.5 | add column; per-cell `[AI-SUGGESTED]` |
| A5 | Every §5 task flow is a column (or scoped action) in §6.5 | add column or scoped action; per-cell `[AI-SUGGESTED]` |
| A6 | Every §2.1 *persistent* concept appears as a §7 entity | create entity stub: name + minimal field set inferred from concept definition + `Domain concept: <concept_name>` |
| A7 | Every §7 entity's "Domain concept" field names an existing §2.1 concept | if reference dangles: prefer adding the concept to §2.1 (with `[AI-SUGGESTED]`) over silently renaming the entity, unless inputs more strongly support the rename |
| A8 | Every §5 flow's Actor names an existing §3 persona | prefer adding the persona to §3 (with `[AI-SUGGESTED]`) over silently renaming the flow's Actor, unless inputs more strongly support the rename |
| A9 | §10 Volumes has all three fields filled (data volume, frequency, concurrency) | infer bands per domain heuristics (e.g. SaaS B2B: 10²–10⁴ records, daily frequency, 10¹–10² concurrent users); per-field `[AI-SUGGESTED]` |
| A10 | §1.5 Scope has ≥1 In row (`[OUT-OF-SCOPE]` is **not** valid in this section) | fabricate ≥1 In bucket entry inferred from §1 purpose; `[AI-SUGGESTED: blocking]`. Empty Out and Deferred buckets are acceptable. |
| A11 | When §2.5 is emitted (≥1 §2.3 aggregate has >2 states), every §2.3 invariant naming a state appears as a §2.5 row | fabricate §2.5 row from invariant; per-cell `[AI-SUGGESTED]`. When §2.5 is **not** emitted, this rule is skipped entirely. |
| A12 | Every §6.7 row names ≥1 existing §2.1 concept in `Source concept(s)` | resolve cross-reference; if the named concept does not exist, prefer adding it to §2.1 (with `[AI-SUGGESTED]`) over silently renaming the report's source. |
| A13 | Every §6.8 row's `Audience` names an existing §3 persona | prefer adding the persona to §3 (with `[AI-SUGGESTED]`) over silently renaming the notification's audience, unless inputs more strongly support the rename. |
| A14 | Every §6.10 row's `Operation` maps to a §6.1 F-NN | fabricate F-NN if missing; `[AI-SUGGESTED]`. Under `target == "application"` the row's pointer column still references the sibling backend doc — that pointer is not gap-pass-validated. |
| A15 | When §7.X is emitted (≥1 §2.1 concept has `Persistence = derived`), every §7.X row names an existing §2.1 concept with `Persistence = derived` | if the named concept is not in §2.1 or is not `derived`, prefer updating §2.1 (set the concept's persistence to `derived`, with `[AI-SUGGESTED]` on the cell) over dropping the §7.X row. When §7.X is **not** emitted, this rule is skipped. |

## Tier B — soft references

| # | Rule | Action |
|---|---|---|
| B1 | Every §4.1 goal is referenced by ≥1 §4.2 story | fabricate story under most plausible persona; mark `[AI-SUGGESTED]` |
| B2 | Every §6.5 conditional cell `<action>†BR-NN` names a real §6.2 BR-NN | fabricate BR-NN row in §6.2 inferred from the role + action + entity context; mark `[AI-SUGGESTED]` |
| B3 | §7 entity relationships align with §2.2 | warn only; **no fabrication** (FK fabrication is too error-prone without input support) |
| B4 | Every §1.7 row's `Driving requirement(s)` cell cross-refs ≥1 §6 / §10 row | warn only when the cross-ref is missing or dangles; the drafter's `derive-architectural-implications` substep is responsible for setting it. No fabrication here. Active under both targets — §1.7 is emitted on every run. |
| B5 | Every §4.2 story / §6.1 F-NN / §6.2 BR-NN / §5 task-flow step has a populated `Acceptance criteria` cell | fabricate from observable signals when input is silent; `[AI-SUGGESTED: non-blocking]`. Phrase behaviourally per `GR-21`; never visually. §6.1 / §6.2 cells use EARS keywords per `GR-23`; §4.2 / §5 / §6.4 stay observable-signal. |
| B6 | Every §4.2 story / §6.1 F-NN / §6.4 UI-NN has a `Priority` value (`Must` / `Should` / `Could` / `Won't`) | **no fabrication, no `[AI-SUGGESTED]`.** Priority is filled at decision-tree step 2 by `GR-24` (`[STANDARD-RULE: GR-24]`) when the input is silent. Warn only if a row is still missing a priority after the GR-24 pass. |
| B7 | Every §6.6.1 field not resolved by `GR-19` and every §6.6.2 metric has a populated value | fabricate from the §1 domain + §10 volume bands; `[AI-SUGGESTED: non-blocking]` (the sections are scope-noted application-build guidance — a wrong guess cannot propagate into the prototype build). This rule pulls §6.6.x fields into decision-tree step 3 so they are never OOS-routed at steps 4/5; `framework/shared/prototype-scope.md` confirms these sections are not Filter-Out content. |

## Tier D — mixed (in-scope only when visually manifested)

**D1 — §2.3 invariant → §6.2 BR projection.** Every §2.3 invariant must produce a §6.2 BR row (the bijection is preserved). The marker depends on visual manifestation **and** on `target`:

- If the invariant maps to **any one** of:
  - a status badge transition (a §2.3 lifecycle state change),
  - a conditional UI visibility (button/field shown/hidden based on state),
  - a role-gated action (visible only to certain personas),
  - an inline validation error (form-field error message),
  
  → mark `[AI-SUGGESTED]`. Identical under both targets.
- Otherwise (pure server-side computation, scheduling, audit trail, ledger reconciliation):
  - `target == "prototype"` → mark `[OUT-OF-SCOPE: domain-default]`.
  - `target == "application"` → fill with the same domain-default BR row, **no marker**.

§2.3 itself is **not** filtered — all invariants stay in the domain model artefact for downstream design.

**D2 — §7 shape field-level (UI-display test).** A field gates `[AI-SUGGESTED]` only if its `UI-display` cell names a visible surface (`form-input`, `table-col`, `detail`, `chip`, `enum`) — identical under both targets. Fields whose `UI-display` is `hidden` (internal IDs, opaque keys) are treated as Tier C: `target == "prototype"` → `[OUT-OF-SCOPE: domain-default]`; `target == "application"` → filled with the same domain default, **no marker**. §7 no longer carries explicit FK / index / validation-timing columns — those concerns now live in the backend doc (FKs / indexes) and §6.4 with `GR-05` (validation timing) respectively.

**D3 — §2.5 state-transition visible-effect test.** Every §2.5 row's `Visible effect` cell is evaluated:

- If the effect manifests in the UI (status-badge change, screen route, action gained/lost, banner appears) → `[AI-SUGGESTED]` per Tier A11. Identical under both targets.
- Otherwise (purely server-side state change — scheduled job, audit append, server-side reconciliation):
  - `target == "prototype"` → `[OUT-OF-SCOPE: domain-default]`.
  - `target == "application"` → filled with the same domain-default row, **no marker**.

**D4 — §6.7 audience-has-RBAC-read test.** Every §6.7 row's `Audience` persona must have read access to the row's `Source concept(s)` per §6.5. Mismatch emits a warn-only Tier B-style flag in the gap-pass log (not a fabrication; the drafter resolves by adjusting either §6.5 or the report's audience after consulting the gap-pass log).

## Tier C — out-of-scope sections (per-target marker emission)

Tier C sections are completeness-required by the template (`fill every field`) but historically out-of-prototype-scope. Under `target == "prototype"`, each row's field is filled with a domain default and marked `[OUT-OF-SCOPE: domain-default]`. Under `target == "application"`, the same field is filled with the same domain default but carries **no marker** — the consultant may edit the value during the merger's accept/edit/reject loop if needed. The set of `[AI-SUGGESTED]` items in Tier C is empty under both targets (Tier C is never AI-SUGGESTED).

| Section | Rationale (basis for the prototype-mode OOS marker; application mode suppresses the marker) |
|---|---|
| §7 shape fields with `UI-display = hidden` (internal IDs, opaque keys) | `prototype-scope.md` Data model elements — explicit exclusion of "database table definitions, indexes, foreign key constraints"; FE never displays these so they cannot be `[AI-SUGGESTED]` (no UI surface to validate against) |
| §2.5 transitions whose `Visible effect` is purely server-side | per **D3** above |
| §6.10 sub-block not matching `manifest.target` | drafter emits only the matching variant; the off-mode sub-block is suppressed entirely (no marker, no row). This is a structural conditional, not a Tier C row in the traditional sense, but is listed here for symmetry. |

**In-scope under both targets** (fields carry `[AI-SUGGESTED]` / `[STANDARD-RULE]` as applicable; the first three are scope-noted application-build guidance — the template blockquote carries the "not a prototype design input (PI-01/PI-03/PI-08)" semantics in-document):

- §1.7 Architectural implications — drafter-derived capability plan, emitted on every run. Rows are authored by the drafter's step 6 (not gap-pass tuples); every row carries `[AI-SUGGESTED: non-blocking]` (B4 checks the cross-ref).
- §6.6.1 Session UX — emitted on every run. `GR-19` provides `[STANDARD-RULE]` domain defaults for the timeout fields when input is silent; remaining fields per B7 (`[AI-SUGGESTED: non-blocking]`).
- §6.6.2 FE performance budgets — TTI, bundle size, render budgets, emitted on every run. Per B7: `[AI-SUGGESTED: non-blocking]` when inferred from volumes (§10).
- §6.1 `Rationale` cells — drafter-authored and **per-cell optional**; the gap pass never fabricates them (no tier row; blank is a valid resolution).
- §6.6.3 Availability — **retired entirely from the template** (backend concern; FE doc no longer has this section).
- §6.6.4 Compliance UI behaviour — consent banners, PII screen redaction, regional UI variants. `[AI-SUGGESTED]` when inferred from domain. Backend audit retention is the backend doc's concern and is not in this section.
- §6.6.5 Accessibility — drives design tokens & screen states.

## Algorithm (deterministic; the skill performs no LLM call itself)

1. Walk the populated draft section-by-section.
2. For each rule in Tier A, B, D, evaluate the predicate against the draft state.
3. For each violation, run the decision tree above (parameterised by `target`) to produce a `(rule_id, location, action, marker_kind, marker_payload, draft_context, priority_score)` tuple. Under `target == "application"`, any tuple whose decision tree resolves to "OUT-OF-SCOPE" is emitted with `marker_kind = "none"` and a domain-default `marker_payload` value — the drafter still applies the value via Edit, but no `[OUT-OF-SCOPE: domain-default]` tag is written into the draft. For tuples with `marker_kind = "AI-SUGGESTED"`, emit a one-line `draft_context` derived from the tuple's `rule_id` + `location` + (when useful) the candidate value set — this is consumed by the resolver's Q&A presentation, not written into the draft body — and assign `priority_score` from the Priority scoring table above. Tuples with any other `marker_kind` carry no `draft_context` and `priority_score = 0`.
4. Emit the tuple list to the drafter, plus the running `AI-NNN` counter.
5. The drafter applies the tuples to the draft (via Edit) before writing the final file. The drafter also carries each `AI-SUGGESTED` tuple's `draft_context` into the resolver's manifest at the resolver's first-turn build step (per `framework/agents/requirements-resolver.md > Working state`); the field is observability for the resolver and never written into the draft body itself.
6. **Apply the cap.** Use the AI-SUGGESTED cap value from `GR-22` (default 50). The `general-rules.md` catalogue was already loaded at step 2, so the `GR-22` cap is in context — do **not** issue a second Read. (If, defensively, the catalogue is not in context — e.g. a summarised run — read only the `GR-22` row from the slim `framework/shared/general-rules.index.md`, which carries the cap, not the full body.) On the in-memory tuple list:
    - Partition AI-SUGGESTED tuples by `marker_payload` classification (`blocking` vs `non-blocking`). Tuples with any other `marker_kind` are unaffected by this step.
    - Keep **all** blocking tuples regardless of count.
    - Sort the `non-blocking` tuples by `(priority_score desc, AI-NNN asc)` — higher priority first, AI-NNN tiebreaker for stable ordering.
    - Walk the sorted non-blocking list and keep tuples until `blocking_count + kept_non_blocking_count == cap`. Once the cap is reached, **demote** every remaining non-blocking tuple: set `marker_kind = "none"`, clear `draft_context` (`null`), keep the existing `marker_payload` value (the domain-default fill the gap pass produced), and clear `priority_score` to 0. The demoted tuple's `rule_id` is preserved for forensic logging in the drafter's gap-pass output but the field is not consumed downstream.
    - **Renumber AI-NNN** monotonically over the surviving `[AI-SUGGESTED]` set (blocking + kept non-blocking, processed in their pre-cap AI-NNN order), starting at AI-001, so the drafter's tag-assignment stays gap-free in the written draft. Demoted tuples no longer carry an AI-NNN identifier.
    - If `blocking_count >= cap`, keep every blocking tuple anyway (the cap is a floor for blocking, not a ceiling) and demote every non-blocking tuple.

**Invariant.** For the same draft state, the set of tuples with `marker_kind = "AI-SUGGESTED"` **after the cap step at step 6** is byte-for-byte identical under `target == "prototype"` and `target == "application"`. Only `marker_kind = "OUT-OF-SCOPE"` tuples differ between targets (emitted as OOS under prototype; emitted with `marker_kind = "none"` under application). §1.7 / §6.6.1 / §6.6.2 contribute identically under both targets — they are emitted on every run, so they no longer break this invariant the way the retired emit-conditional regime did. The cap step is applied uniformly under both targets — it narrows the AI-SUGGESTED set, never widens it, so the invariant is preserved across the cap. Demoted tuples land on the `marker_kind = "none"` branch under both targets and are indistinguishable from application-mode OOS-routed fills in the produced draft.

## Used by

- `framework/agents/requirements-drafter.md` — workflow step 5 (post-fill, pre-write).

## Anti-Patterns

- Do not call an LLM inside this skill. The decision tree is deterministic; inference (when needed) is performed by the drafter consuming the tuple list.
- Do not emit `[AI-SUGGESTED]` for any tuple whose decision tree resolved at step 2 (general-rules) or step 4 (out-of-scope). This rule holds under both targets — `target == "application"` suppresses the `[OUT-OF-SCOPE]` marker but does not promote those tuples to `[AI-SUGGESTED]`.
- Do not skip the `general-rules.md` lookup; it must precede every `[AI-SUGGESTED]` decision.
- Do not Read `general-rules.md` a second time at the cap step (Algorithm step 6); the `GR-22` cap is already loaded from the step-2 lookup (or, on a summarised run, read only the `GR-22` row from the slim `general-rules.index.md`).
- Do not modify §2.3 — invariant filtering applies only at the §2.3 → §6.2 projection.
- Do not emit tuples for conditional sections whose emit-predicate is false. §2.5 / §6.9 / §7.X / the off-mode sub-block of §6.10 produce zero tuples when not emitted; §1.6 / §8 / §9 produce zero tuples when their content-conditional predicate is false. The drafter's self-validation does not require their presence in those cases.
- Do not enforce `GR-20` (no stack specifics) or `GR-21` (no UI layout) here — those are drafter pre-Write Grep guards over the produced draft, not gap-pass decision-tree outcomes. The gap-pass produces values that are themselves capability-category and behavioural; the drafter's self-validation catches any leak.
- Do not widen the AI-SUGGESTED set when `target == "application"`. The contract with the consultant is that they answer questions only about facts the AI fabricated; widening the set under application mode would surface redundant or ungrounded questions. The application-mode behavioural change is OOS-marker suppression only.
- Do not skip the prototype-scope predicate evaluation under `target == "application"`. The predicate is still needed to identify which tuples would have been OOS, so the skill can route them to the `marker_kind = "none"` branch. The file is consulted under both targets.
- Do not apply the cap step differently across targets. The cap is a uniform narrowing rule; per-target caps would break the byte-for-byte identical-set invariant the skill enforces at step 6.
- Do not cap blocking items. Blocking is the tie-breaker-of-record from the drafter's classification rubric — capping blocking would silently swallow exactly the items consultants need to see. If `blocking_count >= cap`, every blocking tuple is still kept and the non-blocking budget is zero.
- Do not promote a demoted (`marker_kind = "none"`) tuple back to AI-SUGGESTED in a later pass or by post-hoc edit. The cap is one-shot at the end of the algorithm; promoting a demoted tuple would either re-introduce the over-emission the cap exists to prevent or break the AI-NNN gap-free renumber.
- Do not introduce ad-hoc `priority_score` values outside the Priority scoring table. New scoring rows ship with the gap-pass rule they describe; off-table scores would break the ranking's reproducibility across runs.
