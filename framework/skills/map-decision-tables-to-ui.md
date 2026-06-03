# map-decision-tables-to-ui.md

**Purpose:** Translate a `decision-tables` analysis artefact into UI-inventory entries (form-validation guards, conditional-visibility toggles, action-enablement rules) for downstream design consumption. **Stub at MVP** — like the other analyses' map-skills, this is registry metadata read by a future design-spec-drafter, **not** invoked by `/analyse-requirement`. Decision-tables exposes only the `upstream-only` sidecar role at MVP, so the blueprint-architect does not consume the rule model directly; this file documents the wider mapping for human design authors and for the day a dedicated `interaction-logic` architect role is added.

## Inputs

- `analyse-requirements/DECISION-TABLES/decision-tables.html` — the decision-tables artefact (or its embedded `<pre><code class="language-json" id="decision-tables-body">` model for the structured subset).

## Mapping

### Condition → UI guard

| Condition kind | UI realisation |
|---|---|
| a `status` / `role` / boolean / category condition | a **guard** on a surface — show/hide a field or control, enable/disable an action, require/relax a field, depending on the current value. |
| a `named-band` numeric condition | a **threshold guard** — the boundary the spec named drives the branch (e.g. an approval step above an amount band). |
| an `un-banded` condition (flagged `needs-a-threshold`) | **not** a guard yet — a design unknown to settle before the surface is built. |

### Conclusion → surface / field state

- **`required` / `optional`** → the field's validation state on the owning surface (per `GR-05` timing: on blur for sync rules, on submit for cross-field).
- **`enabled` / `disabled`** → an action control's state; a disabled destructive action stays modal-gated per `GR-04` when enabled.
- **`visible` / `hidden`** → conditional rendering of a field/section on the surface.
- **a derived value / routing target / eligibility verdict** → a read-only display, a routed next-surface, or a status the screen reflects.

### Register → design signal

- **completeness gap** → not a surface; an `[AI-SUGGESTED]` resolver question to settle before building (a combination whose outcome is undefined).
- **consistency conflict** → a contradiction to resolve in `requirements.md` before design — two rules cannot both drive the same control.

## Note

No widening. Every guard/state this mapping proposes must trace to a rule that traces to a `§6.1`/`§6.4`/`§6.5`/`§5`/`§7` source. The mapping never introduces a decision, condition, value, or outcome the analysis did not carry.
