<!--
ROLE: asset (cross-pipeline template). Used by framework/agents/blueprint-architect.md
to populate blueprints/<scope-slug>/blueprint.md.

NO PATTERN BINDINGS APPEAR IN THIS TEMPLATE. Pattern decisions live per-variant in
wireframes/<scope-slug>/<VARIANT>/manifest.json — they vary by variant and (in a
future /prototype run) by fidelity. The blueprint is the convergence point: same
screen inventory, same flow, same scope→screen trace, no design opinions.

Slots filled by the architect (every {{PLACEHOLDER}} must be replaced or removed
before write; the architect's self-validation flags any literal {{...}} surviving):
  {{SCOPE_SLUG}}                — kebab-case scope slug.
  {{SOURCES_LIST}}              — comma-separated requirement IDs (Functional, BR, UI, Goals, Task flows, Data shapes).
  {{PERSONAS_AVAILABLE_LIST}}   — bulleted list of §3 persona names with their one-line characteristic from requirements.md §3.
  {{SCREEN_INVENTORY_TABLE}}    — markdown table of {S-NN | Intent | Sources | Secondary intent (optional)}.
  {{FLOW_DESCRIPTION}}          — prose + arrow notation (e.g. "S-01 → S-02 → S-03; S-03 → S-02 on validation failure").
  {{PATTERN_COVERAGE_SUMMARY}}  — one or two lines from check-pattern-coverage skill's `notes` field.
  {{SELF_VALIDATION_BIJECTION}} — "PASS" / "FAIL with reason".
  {{SELF_VALIDATION_CONFLICTS}} — "NONE" / "<conflict description>".
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

| Screen ID | Intent | Sources | Secondary intent |
|---|---|---|---|
{{SCREEN_INVENTORY_TABLE}}

Notes:
- Every row's `Sources` list is the set of requirement IDs this screen exists to satisfy. The variant-generators propagate these into `data-src` attributes on rendered elements.
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

## Architect notes

{{ARCHITECT_NOTES}}
