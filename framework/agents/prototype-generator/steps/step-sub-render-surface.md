# step-sub-render-surface (per-surface sub-agent)

**Role:** the instruction set for ONE parallel sub-agent dispatched by `step-04`. It renders the **new shared components** for exactly one surface. It is the unit that makes generation parallel + safe.

**Activation:** load `framework/assets/persona-llm.md` + `framework/assets/characters/prototype-generator.md` (same stance as the driver).

**Assignment (passed in the dispatch prompt):** `{ surface_id, surface_intent, realization, host?, owned_files, components_to_reuse, data_bindings (Property→fixture-field→store), posture, dimension_positions, ux_baseline_subset }`.

## Hard rules (collision-safety)

- **Write ONLY the files in `owned_files`.** These are new shared components under `src/components/{atoms,molecules,organisms,templates,domain}/`.
- **Never** write route files (`src/app/**`), the data layer (`types`/`fixtures`/`stores`/`seed`), or any file not in `owned_files`. The driver owns those.
- **Never overwrite** an existing component — reuse it (it's in `components_to_reuse`).
- Read the existing shared library + the shadcn `ui/` primitives freely.

## Render contract

1. Compose each owned component from shared `ui/` primitives + existing shared components, themed by the fixed brand tokens (no new palette/type/radius — D1).
2. Apply the **posture + positions** to layout/density/disclosure/interaction only (e.g. dense table at D3+, inline-edit at D1+/P1, wizard step at P2, calm whitespace at P5). Realize the surface per its `realization` (the component(s) a drawer/modal/expand/standalone/wizard-step needs — the driver wires them into the route).
3. **Anti-fabrication:** every data-bound element binds to a Property in `data_bindings` (the blueprint closed set) and carries `data-prop="Entity.Field"` (or `F-NN:Param`). No invented fields. UI-only controls (search/sort/pagination/filters/save/cancel/density-toggle) are exempt and carry no `data-prop`.
4. **Baseline floor** (`ux_baseline_subset` from `ux-baseline-checklist.md`): render the three states (empty/loading/error) where the surface is a collection or async action; keyboard-operable + visible focus; name/role/value on controls; not-colour-alone for status; ≥24px targets. Self-check before writing.
5. Verify each written file via `framework/skills/verify-artifact-write.md`.

## Return (component manifest)

`{ surface_id, files_written: [...], components_created: [...], components_reused: [...], props_bound: ["Entity.Field", ...], states_rendered: ["default","loading","empty","error", ...], baseline_ok: true }` — or `failed { surface_id, reason }` (e.g. a binding not in the closed set, an unrenderable realization). The driver consumes the manifest in `step-05` to compose the route and in `step-07` to self-validate.

## Anti-patterns

- Do not write outside `owned_files`; do not touch routes or the data layer.
- Do not invent data fields or fixtures; bind only to the closed set.
- Do not add a private/per-prototype theme or component folder (rules 15–16; D1).
- Do not skip the three states or the baseline self-check.
- Do not return success with a fabricated binding — return `failed` so the driver can route to retry/`RF-12`.
