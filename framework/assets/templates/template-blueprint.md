<!--
ROLE: asset (cross-pipeline template). Used by framework/agents/blueprint-architect.md
to populate blueprints/<scope-slug>/blueprint.md.

NO PATTERN BINDINGS APPEAR IN THIS TEMPLATE. Pattern decisions live per-variant in
wireframes/<scope-slug>/<VARIANT>/manifest.json — they vary by variant and (in a
future /prototype run) by fidelity. The blueprint is the convergence point: same
screen inventory, same flow, same scope→screen trace, same property closed set,
no design opinions.

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
  {{SCREEN_INVENTORY_TABLE}}    — markdown table of {S-NN | Intent | Sources | Properties | Secondary intent (optional)}.
                                  Properties cell shape: comma-separated `Shape.Property` references (e.g. `FileLog.ProcessDate, FileLog.CurrentStatus`) and/or `F-NN:ParamName` references for F-NN-named parameters not in §7 (e.g. `F-05:FileSettingId`). Use `none` for screens that render no entity-bound fields (rare; only screens that are pure UI like a confirmation modal preview).
  {{FLOW_DESCRIPTION}}          — prose + arrow notation (e.g. "S-01 → S-02 → S-03; S-03 → S-02 on validation failure").
  {{PATTERN_COVERAGE_SUMMARY}}  — one or two lines from check-pattern-coverage skill's `notes` field.
  {{SELF_VALIDATION_BIJECTION}} — "PASS" / "FAIL with reason".
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

## Screen inventory

| Screen ID | Intent | Sources | Properties | Secondary intent |
|---|---|---|---|---|
{{SCREEN_INVENTORY_TABLE}}

Notes:
- Every row's `Sources` list is the set of requirement IDs this screen exists to satisfy. The variant-generators propagate these into `data-src` attributes on rendered elements.
- Every row's `Properties` list is the **closed set** of object properties the screen may render. Each entry resolves to either (a) a §7 data-shape property using `Shape.Property` notation, or (b) an F-NN-named property using `F-NN:ParamName` notation when the F-NN names a parameter not in §7. The variant-generator embeds `data-prop` attributes on each data-bound element naming the property it binds to; rendering a property outside this list is a self-validation FAIL. **UI-only controls (search, sort, pagination, filter chips, expand/collapse, save/cancel buttons, progress indicators) are exempt from the property contract and do not need a `data-prop` attribute.**
- Secondary intent is optional. When present, it captures a slot a variant may want to populate with a non-primary pattern (e.g. "with inline validation"); when blank, the variant decides freely.

## Flow

{{FLOW_DESCRIPTION}}

## Pattern-coverage preflight

{{PATTERN_COVERAGE_SUMMARY}}

(Output of `framework/skills/check-pattern-coverage.md` run by the architect during design-brief preflight. A gap here would have fired the orchestrator's conditional gate; on a clean preflight this section is informational.)

## Self-validation

| Check | Result |
|---|---|
| Bijection (every scope source referenced; no orphan screens) | {{SELF_VALIDATION_BIJECTION}} |
| Conflicts (no requirement pair foreclosing each other) | {{SELF_VALIDATION_CONFLICTS}} |
| Properties (every property resolves to §7 or a cited F-NN's named parameter) | {{SELF_VALIDATION_PROPERTIES}} |

## Architect notes

{{ARCHITECT_NOTES}}
