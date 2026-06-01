---
name: step-06-self-validate-and-handback
description: 'Run the structural self-validation checks. On pass, return ok. On fail, return a structured failed payload.'
---

# Step 6: Self-validation and handback

## 6.1 Run the self-validation checks

Walk through the **Self-validation** list in `framework/agents/wireframe-variant-generator.md` in order. For each check:

- If `pass`, record `checks[<id>] = "pass"` and continue.
- If `fail`, attempt one in-loop fix:
    - Missing screen file → re-run step 4's compose+write for the missing `S-NN`.
    - Fabricated `data-src` → re-render the offending screen with the cleaned attribute set; re-write; re-verify.
    - **Fabricated `data-prop` (property not in the owning unit's `covers_properties`)** → re-render the offending screen with the fabricated field removed (or its `data-prop` retargeted to a real property in the owning unit's `covers_properties` if the field is semantically the same — host-surface elements against the physical screen's slice; fold sub-tree elements against the fold's own `covers_properties`); re-write; re-verify. If the pattern's required slots cannot be filled from the owning unit's `covers_properties` alone after the fabricated field is removed, halt with `checks[<id>] = "fail (unrecoverable)"` and surface as a `failed` handback at step 6.2 — the authored closed set is too narrow and the architect (not this sub-agent) must broaden it.
    - **Missing `data-prop` on a data-bound element** → re-render the offending element with the correct `data-prop` attribute. If the element binds to a property not in the owning unit's `covers_properties`, treat it as a fabricated-`data-prop` case (above): drop the field or escalate.
    - **Authored pattern/variant absent from the catalogue** → not recoverable by substitution. Halt with `checks[<id>] = "fail (unrecoverable)"` and surface as a `failed` handback — this is an architect bug (author-time catalogue validation should have caught it); the generator never silently falls back to `variants.default`.
    - Wrong DS link → re-render the offending screen with corrected `{{DS_PATH}}` slot; re-write; re-verify.
    - Drift in `variant-position.json > dimension_positions` (or `posture` / `posture_label`) vs `variants.json own-entry` → re-render `variant-position.json`; re-write; re-verify.
    - Invalid catalogue pattern ID in `manifest.json` → halt (this is a step-4 composition bug; the agent does not have safe automatic remediation since the pattern was already rendered into the screen HTML). Record `checks[<id>] = "fail (unrecoverable)"`.

If after one fix attempt the check still fails, the sub-agent's run is unrecoverable.

## 6.2 Compose the handback message

On all-pass:

```
*"Variant <variant_id>: ok"*
```

(Single short plain-text line. The orchestrator's Stage-3 dispatch interprets this verbatim; do not add commentary.)

On any fail (unrecoverable):

```
*"Variant <variant_id> failed: <one-line structured reason>"*
```

The structured reason names the failing check ID and the affected file. Examples:

- *"Variant POWER-DENSITY-EXPERT failed: data-src fabrication on S-04 (`screen-04-approval.html`) — `data-src='F-99'` is not in blueprint sources for this screen."*
- *"Variant CAREFUL-DEFAULT failed: data-prop fabrication on S-01 (`screen-01-upload-form.html`) — `data-prop='FileSetting.AccountingPeriod'` is not in blueprint properties for this screen (closed set: `F-05:FileSettingId, F-05:FileSettingName, F-05:FileName`). Drop the fabricated field, or escalate to the architect to broaden the closed set."*
- *"Variant FOCUS-NOVICE failed: dimension-position mirror drift — variant-position.json declares density-focus: -1 but variants.json own-entry declares density-focus: -2."*
- *"Variant AUDIT-FIRST failed: pattern-coverage gap surfaced at compose time — S-04 (Three-way disposition) has no catalogue pattern available; architect's preflight missed this."*
- *"Variant POWER-DENSITY-EXPERT failed: authored pattern absent from catalogue — surface_plan for LS-02 names primary_pattern_variant `super-compact` not in `collections/table` variants: block. Render-vs-plan cannot proceed; no silent fallback. Architect must fix the authored surface_plan."*
- *"Variant CAREFUL-DEFAULT failed: fold host did not materialise — surface_plan folds LS-03 (inline-drawer) onto rendered_on=S-01, but no physical screen for S-01 was produced this variant (no-fold-of-fold violated upstream)."*

## 6.3 Hand back

Emit the handback message as the final line of the sub-agent's run. The orchestrator's Stage-3 dispatch awaits this line per-sub-agent; the variant-completion gate in `framework/orchestrators/wireframe-orch.md > Handback gates > Stage 3 handback` is now evaluable for this variant.

---

End of variant-generator workflow.
