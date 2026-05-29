<!--
ROLE: asset (cross-pipeline template). Used by framework/agents/blueprint-architect.md
to populate blueprints/<scope-slug>/blueprint.md.

NO PATTERN BINDINGS OR REALIZATION PICKS APPEAR IN THIS TEMPLATE. Both pattern
decisions and realization decisions (how many physical screens a surface becomes)
live per-variant in wireframes/<scope-slug>/variants.json > surface_plan and the
per-variant manifest.json — they vary by variant and (in a future /prototype run)
by fidelity. The blueprint is the convergence point: same **logical surface
inventory** (decomposition-agnostic LS-NN surfaces), same logical flow, same
scope→surface trace, same per-surface property closed set, same per-surface
*allowed* realization set — no design opinions, no chosen realization.

LOGICAL SURFACES vs PHYSICAL SCREENS. A logical surface (LS-NN) is a unit of
user-facing capability (e.g. "View file detail"). A variant *realizes* each
surface as physical screen(s): standalone-screen (its own file), inline-drawer /
inline-expand / modal (folded onto a host surface's screen, no own file), or
wizard-split (one surface → N sequential sub-screens). The blueprint lists the
*allowed* realizations per surface and a *default*; the variant picks one in its
surface_plan. BASELINE: when every surface is realized standalone-screen, LS-NN
maps 1:1 to a single physical screen S-NN and the output is identical to a
pre-realization run.

PROPERTY CLOSED SET. The blueprint's Properties column is the **canonical closed
set** of object properties each screen may render — drawn exclusively from §7
data shapes (e.g. `FileSetting.Name`, `FileLog.CurrentStatus`) or from the
specific F-NN's text when an F-NN names properties not present in §7 (e.g.
F-05 names `FileSettingId` as a query parameter; that parameter is a renderable
property even though §7 FileSetting calls it `Id`). The variant-generator must
not render any data-bound field whose property is not in this closed set —
fabricated fields are a self-validation FAIL. UI-only controls (search, sort,
pagination, filter chips, expand/collapse, view toggles, save/cancel buttons,
progress indicators) are exempt: they do not bind to entity values.

Slots filled by the architect (every {{PLACEHOLDER}} must be replaced or removed
before write; the architect's self-validation flags any literal {{...}} surviving):
  {{SCOPE_SLUG}}                — kebab-case scope slug.
  {{SOURCES_LIST}}              — comma-separated requirement IDs (Functional, BR, UI, Goals, Task flows, Data shapes).
  {{PERSONAS_AVAILABLE_LIST}}   — bulleted list of §3 persona names with their one-line characteristic from requirements.md §3.
  {{SURFACE_INVENTORY_TABLE}}   — markdown table of {LS-NN | Intent | Sources | Properties | Allowed realizations | Default realization | Host surface | Secondary intent (optional)}.
                                  Properties cell shape: comma-separated `Shape.Property` references (e.g. `FileLog.ProcessDate, FileLog.CurrentStatus`) and/or `F-NN:ParamName` references for F-NN-named parameters not in §7 (e.g. `F-05:FileSettingId`). Use `none` for surfaces that render no entity-bound fields (rare; only pure-UI surfaces like a confirmation modal preview).
                                  Allowed realizations: a closed subset of {standalone-screen, inline-drawer, inline-expand, wizard-split, modal} (see framework/assets/wireframes/realization-strategies.md), derived by the architect from the surface's nature + relationships; always includes standalone-screen. Default realization: exactly one member of that set (the /prototype + baseline pick). Host surface: the LS-NN a foldable surface folds onto (inline-drawer/inline-expand/modal), or `—`.
  {{LOGICAL_FLOW_DESCRIPTION}}  — logical flow over surfaces in arrow notation (e.g. "LS-01 → LS-02 → LS-03; LS-03 → LS-02 on validation failure"). Each variant derives its *physical* flow from this plus its chosen realizations.
  {{PATTERN_COVERAGE_SUMMARY}}  — one or two lines from check-pattern-coverage skill's `notes` field.
  {{SELF_VALIDATION_BIJECTION}} — "PASS" / "FAIL with reason". Bijection is source ↔ **logical surface** (every scope source referenced by ≥1 surface; every surface references ≥1 in-scope source).
  {{SELF_VALIDATION_CONFLICTS}} — "NONE" / "<conflict description>".
  {{SELF_VALIDATION_PROPERTIES}} — "PASS" / "FAIL with reason". Verifies every Properties entry resolves to a §7 data-shape property or an F-NN-named property whose F-NN is in the screen's Sources cell. Fabricated property references fail here.
  {{ARCHITECT_NOTES}}           — optional one-paragraph rationale (omit the whole heading if empty).
  {{REQUIREMENTS_SHA256}}       — propagated from scope.json so downstream readers can detect requirements drift.
-->

# Blueprint: {{SCOPE_SLUG}}

## Sources

{{SOURCES_LIST}}

> `requirements.md` sha256 at scope-selection time: `{{REQUIREMENTS_SHA256}}`

## Available personas (from `requirements/requirements.md` §3)

{{PERSONAS_AVAILABLE_LIST}}

## Surface inventory

| Surface ID | Intent | Sources | Properties | Allowed realizations | Default realization | Host surface | Secondary intent |
|---|---|---|---|---|---|---|---|
{{SURFACE_INVENTORY_TABLE}}

Notes:
- A **logical surface** (`LS-NN`) is a decomposition-agnostic unit of user-facing capability. A variant *realizes* each surface as physical screen(s) per its `surface_plan`. When every surface is realized `standalone-screen` (the default), `LS-NN` maps 1:1 to a single physical screen and the output matches a pre-realization run.
- Every row's `Sources` list is the set of requirement IDs this surface exists to satisfy. The variant-generators propagate these into `data-src` attributes on the surface's rendered element(s).
- Every row's `Properties` list is the **closed set** of object properties the surface may render. Each entry resolves to either (a) a §7 data-shape property using `Shape.Property` notation, or (b) an F-NN-named property using `F-NN:ParamName` notation when the F-NN names a parameter not in §7. The variant-generator embeds `data-prop` attributes on each data-bound element naming the property it binds to; rendering a property outside this list is a self-validation FAIL. **UI-only controls (search, sort, pagination, filter chips, expand/collapse, save/cancel buttons, progress indicators) are exempt from the property contract and do not need a `data-prop` attribute.**
- `Allowed realizations` is the closed subset of realization strategies the architect deems valid for this surface (per `framework/assets/wireframes/realization-strategies.md`); `Default realization` (always including `standalone-screen`) is what `/prototype` and the baseline use; `Host surface` names the LS-NN a foldable surface folds onto (inline-drawer/inline-expand/modal), or `—`.
- Secondary intent is optional. When present, it captures a slot a variant may want to populate with a non-primary pattern (e.g. "with inline validation"); when blank, the variant decides freely.

## Logical flow

{{LOGICAL_FLOW_DESCRIPTION}}

(Flow is expressed over **logical surfaces** (LS → LS). Each variant derives its concrete physical flow from this plus its chosen realizations — a folded surface adds no standalone navigation node; a wizard-split surface adds intra-surface steps.)

## Pattern-coverage preflight

{{PATTERN_COVERAGE_SUMMARY}}

(Output of `framework/skills/check-pattern-coverage.md` run by the architect during design-brief preflight. A gap here would have fired the orchestrator's conditional gate; on a clean preflight this section is informational.)

## Self-validation

| Check | Result |
|---|---|
| Bijection (every scope source referenced by ≥1 surface; no orphan surfaces) | {{SELF_VALIDATION_BIJECTION}} |
| Conflicts (no requirement pair foreclosing each other) | {{SELF_VALIDATION_CONFLICTS}} |
| Properties (every property resolves to §7 or a cited F-NN's named parameter) | {{SELF_VALIDATION_PROPERTIES}} |

## Architect notes

{{ARCHITECT_NOTES}}
