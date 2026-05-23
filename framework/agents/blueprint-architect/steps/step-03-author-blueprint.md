---
name: step-03-author-blueprint
description: 'Compose the screen inventory + flow + scope→screen trace; run bijection and conflict self-validation. Skipped on non-create modes.'
---

# Step 3: Author the blueprint

Runs **only** on `mode = "create"`. On `regenerate-variants` and `add-variant`, the blueprint is reused from disk (see step 2.5) and this step is skipped entirely.

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
| S-NN | <intent string> | <comma-separated source IDs> | <optional secondary-intent string> |
```

The `intent` string is a short noun-phrase summarising what the screen does (`File picker`, `Validation results`, `Confirmation`, `Upload log`). The `secondary-intent` is optional and only present when a UI-NN annotation or a `secondary_intent_hint` from the §6.4 row says one is needed.

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

## 3.6 Architect notes

Compose a one-paragraph optional note for the blueprint's `{{ARCHITECT_NOTES}}` slot. Examples:

- *"5 screens, 11 functional sources, 3 personas available. Goal G-02 (`upload accepted`) drives the flow; G-03 (`audit trail`) shapes secondary intent on S-05."*
- *"4 screens consolidated from 7 candidates. Two §5 flows merge at S-03 (Validation)."*

Omit the section entirely if there is nothing structurally noteworthy to record.

---

**Next:** Read fully and follow `step-04-check-pattern-coverage.md`.
