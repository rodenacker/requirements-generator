---
name: step-03-author-blueprint
description: 'Compose the screen inventory + flow + scope→screen trace; run bijection and conflict self-validation. Skipped on non-create modes.'
---

# Step 3: Author the blueprint

Runs **only** on `mode = "create"`. On `regenerate-variants` and `add-variant`, the blueprint is reused from disk (see step 2.5) and this step is skipped entirely.

**Supporting analyses consumed at this step.** When step 2.6 cached one or more analyses, this step consumes those whose `architect_roles` include `screen-inventory`, `screen-inventory-entity-bijection`, `screen-flow`, or `screen-properties-cross-check` — accessed via the role-keyed in-memory map `cached_projections[<role>][<source-name>]` (per the sidecar schema at `framework/assets/analyses/sidecar-schema.md`), falling through to `cached_legacy_full_reads[<source-name>].content` for the bounded prose branch when a sidecar is absent on disk (see `step-02-read-inputs.md > 2.6.2`). The analyses **augment `requirements.md`** with refining detail (entity attributes, goal decomposition, entity lifecycles, multi-actor flow) and additional instructions about screen breakdown; they do **not widen** the feature scope of `requirements.md` (a screen for a feature absent from `requirements.md` is a flagged requirements gap, never an inventory entry) and they do **not widen** the per-screen Properties closed set (DATA-MODEL discrepancies are flagged in blueprint prose; the closed set remains §7 + F-NN).

## 3.1 Derive candidate screens from scope sources

Walk `scope.sources` category-by-category:

- **Functional (`F-NN`)** — each `F-NN` is a candidate screen seed. Group functional IDs that share a §5 task-flow step into a single screen seed (e.g. F-01 + F-02 both inside §5.2 step 1 → one "File picker" screen seed). Use the in-memory `scope_summaries[<id>]` for the seed's preliminary intent.
- **Business rules (`BR-NN`)** — usually attach to an existing screen seed (their parent functional context). If a BR has no obvious parent screen, surface it as a candidate "BR-driven screen" (typically a validation or guard surface).
- **UI feature needs (`UI-NN`)** — each UI-NN is a candidate screen seed *or* a secondary-intent annotation on an existing seed. Use the UI-NN's summary text to decide (a UI-NN naming "file log overview" is its own screen; a UI-NN naming "with inline-edit on row" is a secondary intent on its parent screen).
- **Goals (`G-NN`)** — goals do not become screens directly; they shape which screens get composed. Record the goal IDs in the architect's notes section but do not seed screens from them.
- **Task flows (`§5.x`)** — each step in a §5 flow that consumes a scope source is a screen seed. Use the flow name as a sequence hint.
- **Data shapes (`§7.x`)** — data shapes do not become screens; they populate slots inside form / detail screens. Record them in the architect's notes for downstream awareness.

The output of 3.1 is an unfiltered candidate list. Each entry carries `{seed_id, candidate_intent, candidate_sources}`.

## 3.2 Consolidate and number screens

Merge candidates that obviously represent the same screen (same intent + overlapping sources). The architect's judgement at this step is the source of truth — the consolidation rule is conservative ("when in doubt, two screens"). Each surviving screen gets a stable `S-NN` ID assigned in flow order (S-01 is the entry screen; S-NN is the terminal screen on the happy path).

For every surviving screen, populate the row shape per `framework/assets/templates/template-blueprint.md > {{SCREEN_INVENTORY_TABLE}}`:

```
| S-NN | <intent string> | <comma-separated source IDs> | <comma-separated property list> | <optional secondary-intent string> |
```

The `intent` string is a short noun-phrase summarising what the screen does (`File picker`, `Validation results`, `Confirmation`, `Upload log`). The `properties` list is composed in 3.2b below — it is the **closed set** of object properties the screen may render. The `secondary-intent` is optional and only present when a UI-NN annotation or a `secondary_intent_hint` from the §6.4 row says one is needed.

## 3.2b Author the per-screen Properties closed set

For each surviving screen, derive the **closed set of object properties** the screen may render. This list is the canonical contract the variant-generator renders against — fields outside this list will fail the variant-generator's self-validation.

Walk the screen's `Sources` and collect property references from two places only:

1. **§7 data shapes** — when the Sources list cites `§7 <ShapeName>` (or when the intent implies an entity is rendered, even if §7 isn't cited explicitly), enumerate the relevant fields from that shape. Use the `Shape.Field` notation, e.g. `FileLog.ProcessDate, FileLog.SettingName, FileLog.CurrentFileName, FileLog.RecordCount, FileLog.CurrentStatus, FileLog.HasBulkErrorFile`. Honour each row's `UI-display` hint (`hidden` fields like `Id` are typically excluded unless the screen needs them; `table-col` / `detail` / `chip` / `form-input` fields are renderable).

2. **F-NN-named parameters** — when an `F-NN` in Sources names input/query/path parameters that are not §7 fields (e.g. F-05's `FileSettingId`, `FileSettingName`, `FileName` query parameters), enumerate them using `F-NN:ParamName` notation. The F-NN's exact prose is the only authority — if F-05 says "FileSettingId, FileSettingName, and FileName", those are the three; do not invent additional parameters.

Compose the Properties cell as a comma-separated list mixing both notations as needed:

```
FileLog.ProcessDate, FileLog.SettingName, FileLog.CurrentFileName, FileLog.RecordCount, FileLog.CurrentStatus, F-05:FileSettingId, F-05:FileSettingName, F-05:FileName
```

Special cases:

- **Pure UI screens** (a confirmation-modal preview screen with no entity binding, an empty navigation hub) — write `none` in the Properties cell.
- **Opaque payloads** — when the shape exists in §7 but its field is intentionally opaque (e.g. `ValidationErrors.JsonArray` — a JSON-array string of per-row error objects whose row shape is not documented in §7), list the shape field anyway (`ValidationErrors.JsonArray`) and add an `[OPAQUE-PAYLOAD]` suffix in the architect notes. The variant-generator may render columns derived from the F-NN's prose (e.g. F-18's "per-row error objects") but each such column must carry a `data-prop="ValidationErrors.JsonArray[<column>]"` attribute and the column name must appear in the cited F-NN's text. Anything outside that contract is a fabrication and self-validation FAIL.
- **Derived shapes (§7.X Derivations)** — when a screen renders a §7.X derived concept (e.g. `File Summary`), list the derivation's named outputs explicitly, e.g. `FileSummary.ImportedCount, FileSummary.ApprovedCount, FileSummary.RejectedCount, FileLog.HasBulkErrorFile` per the derivation rule's output names. If the derivation rule does not name its outputs precisely, surface a conflict in step 3.5 and let the conditional gate fire.

**UI-only controls are NOT listed in Properties.** Search inputs, sort toggles, pagination, filter chips, expand/collapse, view toggles, save/cancel buttons, progress indicators, drag-and-drop affordances, breadcrumb chrome, modal close buttons — these are pattern chrome that does not bind to entity values. The variant-generator renders them per its pattern-catalogue selections without a `data-prop` attribute and they are exempt from the property contract.

**DATA-MODEL cross-check (role `screen-properties-cross-check`).** When `cached_projections["screen-properties-cross-check"]["data-model"]` is populated (sidecar branch — preferred) **or** `cached_legacy_full_reads["data-model"]` is populated (legacy bounded-prose branch — fallback), run this cross-check once per screen after composing the Properties cell from §7 + F-NN: for each entity bound on the screen, walk the projection's `entities[].attributes[]` payload (per `framework/assets/analyses/sidecar-schema.md > 2.4`) — or, on the legacy branch, best-effort-extract the equivalent attribute list from the prose `<Entities|Attributes|Relationships>` tables — and identify any attribute the analysis lists that is **absent** from the §7 shape's row set. Do not add the attribute to the Properties cell. Instead, record a `data-model-discrepancy` flag in `validation.data_model_discrepancies = [{screen_id, entity, analysis_attribute, expected_in_§7, source: "sidecar" | "legacy-prose"}]` and surface it in 3.6's architect notes as plain English: *"Note: DATA-MODEL lists `<Entity>.<attribute>` not in `requirements.md` §7 — likely a requirements gap; not bound on this screen."*. The closed set on the Properties cell remains exclusively §7 + F-NN per `CLAUDE.md > Constraints > Wireframe pipeline never invents object properties`.

## 3.2c Cross-check inventory against cached analyses (screen-inventory roles)

Read role-keyed projections from `cached_projections["screen-inventory"]`, `cached_projections["screen-inventory-entity-bijection"]`, and `cached_projections["screen-flow"]` (each a `{ <source-name>: <payload> }` map per `framework/assets/analyses/sidecar-schema.md > Sections 2.1, 2.2, 2.3`). For source-names whose entry is missing in the role-keyed projection but present in `cached_legacy_full_reads`, fall through to that slot's `content` field and best-effort-extract role-relevant portions from the prose (the projection shape in the sidecar schema names what to extract per role; on the legacy branch the architect locates the same shapes by re-reading the prose's tables / lists in-place).

For each source whose projection or legacy content is available, re-walk the consolidated inventory from 3.2 and cross-reference:

- **`task-flows` / `use-cases`** — the projection's `screens[]` entries (or, on legacy fallback, the prose's goal-decomposition tree / main+extension flows) name sequences of operations the consultant identified as in-scope. For each `screen[]` entry whose `intent` maps to a screen seed you missed at 3.1, consult its `covered_in_requirements` field (sidecar) or re-walk `requirements.md` (legacy) to confirm coverage by an `F-NN` / `BR-NN` / `UI-NN` in `scope.sources`. If covered, add the missed screen seed with citation `augmented by: task-flows:<source_anchor>` or `augmented by: use-cases:<source_anchor>` (verbatim from the projection's `source_anchor` field, or a best-effort anchor on the legacy branch) in the `Architect notes` for that row. If not covered, record a requirements-gap flag in 3.6's architect notes — do **not** add the screen.
- **`state-diagram`** — the projection's `screens[]` (intent-by-state entries) implies state-driven screens. For each entity state that a screen in your inventory should render but you missed (no screen surfaces it), apply the same `requirements.md`-coverage check as above before adding the screen.
- **`user-journeys`** — the projection's `screens[]` (journey-phase touchpoints) surface screen prioritisation but rarely a missed screen; primarily inform 3.6's architect notes and step 5's `variant-philosophy` consumer.
- **`ooux`** — the projection's `entities[]` under role `screen-inventory-entity-bijection` (per sidecar schema §2.2) lists every core object's expected list + detail surfaces. For each entry whose `name` has zero corresponding screen in your inventory, apply the coverage check.
- **`sequence-diagram`** — the projection's `flow_steps[]` under role `screen-flow` (per sidecar schema §2.3) names external-service handoffs. For each step whose `condition` implies an async / polling screen (a "submitting…" surface, a "queued for processing" surface) absent from your inventory, apply the coverage check.
- **`activity-diagram`** — same as `sequence-diagram` plus multi-actor swim lanes imply role-bound screens (e.g. an "approver dashboard" distinct from a "submitter dashboard"). Apply the coverage check.

For each screen added during this pass, record in the row's `Architect notes` (or 3.6's notes section) the source name and projection anchor (`augmented by: <source-name>:<source_anchor>`). Do not silently absorb analyses-driven additions — the citation is the audit trail.

For analyses with role `screen-properties-cross-check` (today: `data-model`), the cross-check happens inside 3.2b on the Properties closed-set — handled there, not here.

**Fall-through note on missing role payloads.** If a selection's sidecar exists but `architect_projection[<role>]` is absent in it (the analyser PR for that method has not yet projected that role per `framework/assets/analyses/sidecar-schema.md > Section 1 — absence is signal-by-omission`), skip that source-role pair silently and proceed; do not halt. The selection is still consumed for any other roles it does expose.

## 3.3 Author the flow

Compose the flow as a single concise prose-plus-arrow notation:

```
S-01 → S-02 → S-03 → S-04 → S-05; S-03 → S-02 on validation failure
```

Rules:
- Use `→` for forward flow.
- Use `;` to separate independent flow paths.
- Annotate error / exception loops with `on <condition>`.
- Cycles are allowed only as error-handling loops; any other cycle is a structural warning (note in the architect's in-thread output, do not block).

## 3.4 Self-validation — Bijection

Run the bijection check in both directions:

- **Source coverage**: for every requirement ID in `scope.sources`, is it referenced by ≥1 screen's `Sources` column? Any unreferenced source is an **orphan source**. Record into in-memory `validation.bijection.orphan_sources = [...]`.
- **Screen justification**: for every screen, is at least one of its source IDs in `scope.sources`? Any screen whose sources are entirely outside `scope.sources` is an **orphan screen**. Record into `validation.bijection.orphan_screens = [...]`.

If either list is non-empty, `validation.bijection.result = "FAIL"` plus a one-line reason for the blueprint's self-validation table. Otherwise `result = "PASS"`.

Orphan sources are the more common case (the consultant scoped an ID the architect missed) — the architect attempts a one-shot self-revision before failing: re-walk 3.1 with the orphan IDs as forced seeds and consolidate at 3.2. If still orphaned after self-revision, the conditional gate fires at step 7.

## 3.5 Self-validation — Conflicts

Walk every pair of source IDs assigned to the same screen and detect requirement-pair conflicts. Conflicts are defined as one ID stating a constraint that the other contradicts on the same screen. Examples:

- `F-05 "single-step submission"` + `BR-04 "two-stage approval required"` on the same screen → conflict.
- `UI-08 "always-on read-only view"` + `F-09 "inline edit on row"` on the same screen → conflict.
- `BR-12 "no destructive action without confirmation"` + `F-14 "one-click bulk delete"` on the same screen → conflict (resolvable by composing modal-confirmation, but the architect surfaces the conflict regardless because the variant-generators need the resolution intent explicit).

For every detected conflict, record `validation.conflicts.entries = [{screen_id, source_a, source_b, conflict_reason}]`. `validation.conflicts.result = "NONE"` if the list is empty; otherwise `"FAIL with conflicts: <count>"`.

Conflict resolution is **not** auto-resolved by the architect — the conditional gate fires at step 7 with the conflict list, and the consultant decides whether to (a) disambiguate which interpretation wins, (b) narrow scope to exclude the conflict, or (c) cancel and run `/review-requirement → ADVERSARIAL` to resolve the conflict in `requirements.md`.

## 3.5b Self-validation — Properties

Walk every screen's Properties cell and verify every entry resolves:

- `Shape.Field` entries — `Shape` must be a header in `requirements/requirements.md > §7` (or §7.X Derivations) and `Field` must be a row in that shape's table. The architect may need to Read §7 selectively to confirm; the lookup is per-screen and is bounded by the screen's Sources list (the architect only checks shapes named in Sources or implied by the intent).
- `F-NN:ParamName` entries — `F-NN` must be in the screen's Sources cell **and** `ParamName` must appear verbatim in the F-NN's prose in `requirements/requirements.md` §6.1. Use the requirement's exact name; do not normalise.
- `none` is always valid; record `validation.properties.entries[<screen>] = []`.

Fabricated entries (Shape doesn't exist, Field isn't in the shape, F-NN doesn't name the param) record into `validation.properties.fabricated_entries = [{screen_id, property, reason}]`.

If `fabricated_entries` is non-empty: `validation.properties.result = "FAIL with <count> fabricated entries"` and the conditional gate fires at step 7. The architect attempts a one-shot self-revision before failing: re-walk 3.2b with the fabricated entries removed (and a flag noting the consultant must confirm the omission) before surfacing the gate.

If empty: `validation.properties.result = "PASS"`.

## 3.6 Architect notes

Compose a one-paragraph optional note for the blueprint's `{{ARCHITECT_NOTES}}` slot. Examples:

- *"5 screens, 11 functional sources, 3 personas available. Goal G-02 (`upload accepted`) drives the flow; G-03 (`audit trail`) shapes secondary intent on S-05."*
- *"4 screens consolidated from 7 candidates. Two §5 flows merge at S-03 (Validation)."*
- *"6 screens; 2 added during 3.2c cross-check against task-flows and state-diagram (augmented by: task-flows:T-2.3, state-diagram:Approval-States). DATA-MODEL flagged 1 discrepancy: lists `Order.shippedAt` not in §7 — likely a requirements gap; not bound."*

Always include in this section (when populated) every analysis-driven screen addition from 3.2c and every DATA-MODEL discrepancy from 3.2b's cross-check. The notes are the consultant's audit trail for analyses augmentation.

Omit the section entirely if there is nothing structurally noteworthy to record.

---

**Next:** Read fully and follow `step-04-check-pattern-coverage.md`.
