---
name: step-07-handback
description: 'Fire the conditional gate only when self-validation flagged structural issues. Otherwise auto-accept and hand back.'
---

# Step 7: Handback

## 7.1 Decide whether the conditional gate fires

The gate fires if **any** of these three predicates is true (from in-memory state captured in earlier steps):

- `validation.bijection.result == "FAIL"` (orphan source(s) and/or orphan screen(s) survived the step-3 self-revision attempt).
- `validation.conflicts.result != "NONE"` (one or more requirement-pair conflicts inside a screen).
- `pattern_coverage.verdict == "gap"` (one or more screens with no catalogue pattern fit; AI-SUGGESTED stubs needed).

Otherwise the gate does **not** fire (auto-accept path); skip to 7.4.

## 7.2 Fire the conditional gate

Compose a structured prompt for `AskUserQuestion`:

- Question text: a multi-line preamble naming the structural issue(s) with their per-row details (orphan source IDs, conflict pairs, gap screen IDs + descriptions). Use concise plain text — IDs, no marketing language. Example:

    ```
    Blueprint self-validation surfaced structural issues for scope `file-upload-flow`:

    Bijection failures:
      - Orphan source: F-12 (not referenced by any screen)

    Pattern-coverage gaps:
      - S-04 Three-way disposition — no catalogue pattern fits; closest is forms/single-form (does not natively model 3 outcomes).

    Conflicts:
      - S-03 (Validation): F-05 "single-step submission" + BR-04 "two-stage approval gate required" foreclose each other.

    What would you like to do?
    ```

- Header: `Design-brief gate`
- `multiSelect: false`
- Options:
    1. `Accept as-is — proceed with AI-SUGGESTED stubs and warnings recorded` (only present when `verdict == "gap"` is the sole issue; absent when bijection or conflict failures are present, since those require explicit resolution)
    2. `Revise inventory — re-author the blueprint with my edits (you'll be re-prompted for inventory adjustments)`
    3. `Revise variants — re-run only the variant composition (keep blueprint as-is)` (only present when `mode = "create"` reached step 5 cleanly; absent when blueprint itself is the failing layer)
    4. `Narrow scope — exit so I can re-run /wireframe with a tighter scope.json`
    5. `Escalate to /review-requirement — exit so I can run an adversarial review and resolve the underlying requirement conflicts first`
    6. `Cancel — exit without writing variants.json` (the blueprint may have been written at step 4; the consultant accepts that residue)

### 7.3 Branch on the consultant's choice

- **Accept as-is** — record warnings in the architect's final summary (next sub-step). Step 5's variants.json was already written; auto-accept the gate.
- **Revise inventory** — surface a follow-up `AskUserQuestion` to capture the specific revision intent (free text). Re-run step 3 with the revision applied; re-run step 4 (the blueprint will be re-written); re-run step 5 (variants will be re-prompted from scratch); re-evaluate the gate. Loop until accept or cancel.
- **Revise variants** — re-run step 5 only (variants are re-prompted from scratch); re-write `variants.json`; re-evaluate the gate. The blueprint is unchanged.
- **Narrow scope** — fail handback cleanly with structured plain-text *"Cancelled at design-brief gate. The blueprint at `<blueprint_output_path>` may still exist on disk; remove it by re-running `/wireframe` with the same `scope_slug` and choosing `Overwrite` at the prior-set gate."*
- **Escalate to /review-requirement** — fail handback cleanly with the same structured plain-text plus *"Then run `/review-requirement → ADVERSARIAL` against `requirements/requirements.md` to surface and resolve the conflict before re-invoking `/wireframe`."*
- **Cancel** — fail handback cleanly with the structured plain-text.

The orchestrator does not advance to Stage 3 on any of the three exit paths (Narrow scope / Escalate / Cancel).

## 7.4 Compose the architect's in-thread summary

Whether or not the gate fired, emit a single Unicorn-voice summary block to the consultant:

```
Blueprint for `<scope_slug>`:
- <N> screens (S-01 … S-NN); <M> sources covered.
- Flow: <one-line flow description>.
- Bijection: <PASS | FAIL with reason>.
- Conflicts: <NONE | count + first conflict pair>.
- Pattern coverage: <verdict>; <notes>.

Variants for `<scope_slug>`:
- <N> variants, diverging on: <comma-separated dimensions>.
- V-A: <variant_id> bound to <persona>; positions <key:value list>.
- V-B: <variant_id> bound to <persona>; positions <key:value list>.
- (V-C if present.)
- Persona-position soft conflicts: <none | list>.

Handing back to /wireframe for Stage 3 (parallel variant generation).
```

## 7.5 Hand back

The architect's run is complete. Step 5's variants.json (if `wrote_variants` is true) and step 4's blueprint.md (if `mode = "create"`) are on disk and verify-artifact-write'd. The orchestrator's Stage-2 handback gate (see `framework/orchestrators/wireframe-orch.md > Handback gates`) is now satisfiable.

---

End of architect workflow.
