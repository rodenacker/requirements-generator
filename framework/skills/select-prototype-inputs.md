# select-prototype-inputs.md

**Purpose:** Present the consultant the `/prototype` input menu (rule 7) as a single numbered list across the optional source classes **B–E** (A = `requirements.md` is always included; an informational **Brand source** line surfaces the design-system status — never a pick), parse a comma-separated multi-select, designate a **primary wireframe basis** when ≥1 wireframe variant is picked, capture confirmation, and write `prototypes/.specs/<name_slug>/supporting-inputs.json`. The selections are read by `prototype-spec-drafter.md` to ground the design spec; a designated primary wireframe variant additionally triggers the **wireframe-seeded fast path** (`design-philosophies.md` + the orchestrator).

This skill is prototype-private. It borrows the print-and-parse + on-disk-presence-filter shape from `framework/skills/select-supporting-analyses.md` (which is wireframe-private and explicitly recommends `/prototype` author its own selector), extends it across four source classes with a static per-source `prototype_roles` mapping, and adds the primary-basis follow-up for wireframes.

## Inputs

- `scope_slug` — kebab-case scope slug from `scope-selector.md`. Required.
- `name_slug` — kebab-case prototype name-slug captured in orchestrator Step A. Required. Drives the output path.
- `analyses_registry_path` — default `"framework/assets/analyses/registry.md"` (source B).
- `analyses_inputs_registry_path` — default `"framework/assets/analyses-inputs/registry.md"` (source C).
- `wireframes_dir` — default `"wireframes/"`; the skill reads `<wireframes_dir><scope_slug>/variants.json` (source D).
- `manifest_path` — default `"requirements/source-manifest.json"` (source E).
- `output_dir` — default `"prototypes/.specs/"`; the skill writes `<output_dir><name_slug>/supporting-inputs.json`.
- `design_system_path` — default `"design-system/design-system.html"`. **Existence-only** (Glob); never read/parse the file here — parsing + theming is `framework/skills/extract-brand-theme.md`'s job at scaffold time.
- `scaffold_marker_path` — default `"prototypes/.scaffold.json"`. **Existence-only** (Glob); its presence means the shared app's brand was already locked at the first scaffold and is not re-applied this run.

## Outputs

Exactly one of:
- **`selected`** — ≥1 optional input chosen; JSON written + `verify-artifact-write` `pass`. If a wireframe variant was chosen, exactly one is flagged `primary_basis: true`.
- **`selected-none`** — the consultant skipped all optional inputs (typed `none`/empty), or **every** source class was empty on disk (auto-proceed, no prompt). An empty-sources JSON is written + verified. The drafter runs from `requirements.md` + blueprint alone.
- **`cancelled`** — consultant cancelled (typed `0`/`cancel`/`q`/`exit`, hit the 2-retry budget, or chose Cancel at confirmation). No JSON written.

## Static source → `prototype_roles` mapping (closed enum, consumed by `prototype-spec-drafter.md`)

| Source class | `name` | `prototype_roles` |
|---|---|---|
| B analyse-requirement | `data-model` | `data-binding`, `validation-rules` |
| B | `ooux` | `data-binding` |
| B | `task-flows` | `workflow-steps`, `cta-set` |
| B | `use-cases` | `workflow-steps`, `cta-set` |
| B | `user-journeys` | `workflow-steps`, `posture-evidence` |
| B | `sequence-diagram` | `workflow-steps` |
| B | `activity-diagram` | `workflow-steps` |
| B | `state-diagram` | `state-chips` |
| B | `jtbd` | `posture-evidence` |
| B | `opportunity-solution-trees` | `posture-evidence` |
| B | `five-whys` | `posture-evidence` |
| B | `glossary` | `copy-vocabulary` |
| B | `trade-off-dimension-analysis` | `posture-evidence` |
| C analyse-inputs | (any) | `context-only` + `posture-evidence` (default; a future per-method refinement may narrow this) |
| D wireframes | (variant) | `realization-basis` |
| E input docs | (file) | `context-only` |

Role semantics (the drafter threads these): `data-binding` → §8 Property usage; `validation-rules` → visual validation in forms (PI-03); `workflow-steps` → §6 flows; `cta-set` → per-surface primary actions; `state-chips` → status displays; `copy-vocabulary` → labels/help/errors; `posture-evidence` → posture/position rationale (§3/§4); `realization-basis` → per-surface realizations seeded from a wireframe variant's `surface_plan` (§5, fast path); `context-only` → background reference, never widens scope or the Property closed set.

## Procedure

1. **Build source B (analyse-requirement).** Read `analyses_registry_path`; retain `status: mvp` rows whose `output_path` resolves on disk (Glob). Compute each row's sidecar path per `framework/assets/analyses/sidecar-schema.md` convention; Glob to set `sidecar_present`.
2. **Build source C (analyse-inputs).** Read `analyses_inputs_registry_path`; retain `status: mvp` rows whose `output_path` resolves on disk.
3. **Build source D (wireframes).** Glob `<wireframes_dir><scope_slug>/variants.json`. If present, parse it and list each variant `{ variant_id, design_philosophy }`; compute each variant's `manifest_path` + `variant_position_path` under `<wireframes_dir><scope_slug>/<variant_id>/`. If absent → source D is empty.
4. **Build source E (input docs).** Read `manifest_path` if present; list rows whose `tier != "Unsupported"` as `{ filename, original_path, tier }`.
4b. **Brand-source status (existence-only).** Glob `design_system_path` → `ds_present`; Glob `scaffold_marker_path` → `brand_locked`. Do **not** open either file. These drive the single informational **Brand source** line printed in step 5 / step 6 (it is never a numbered pick and never enters `supporting-inputs.json`). The line text:

    | `ds_present` | `brand_locked` | Brand source line |
    |---|---|---|
    | yes | no | `Brand source: design-system/design-system.html — present; will theme this prototype's brand at first scaffold.` |
    | yes | yes | `Brand source: design-system/design-system.html — present; brand was locked at the first scaffold and is reused (not re-applied this run).` |
    | no  | no | `Brand source: none found. Recommended — run /design-system first to brand-lock this prototype; otherwise you'll choose brand tokens (URL / paste / neutral defaults) at scaffold.` |
    | no  | yes | `Brand source: none; the app's brand was locked at the first scaffold and is reused. (Running /design-system now won't re-theme existing prototypes.)` |
5. **Auto-proceed — all empty.** If B, C, D, E are all empty, print one plain-text line *"No optional inputs on disk; proceeding from `requirements.md` + the blueprint alone."* **followed by the step-4b Brand source line** (so the design-system status is always surfaced even when the numbered menu is skipped), jump to step 9 with empty sources, write the empty-sources JSON, verify, return `selected-none`. No `AskUserQuestion`.
6. **Build the combined numbered list.** Print, in source order B→C→D→E, a header per non-empty class and number the items **globally** starting at 1 (registry order within each class; do not re-sort). Always print the fixed pre-line for A. Shape:

    ```
    Inputs for prototype `<name_slug>` (scope `<scope_slug>`):

    A. requirements.md — always included (required).
    <Brand source line — the step-4b row for the current ds_present/brand_locked state; informational, not a pick.>

    Analyse-requirement outputs (B):
    1. <name> — <description>   Output: <output_path>
    2. …
    Analyse-inputs outputs (C):
    3. <name> — <description>   Output: <output_path>
    Wireframes for this scope (D):
    4. <variant_id> — <design_philosophy>
    Input documents (E):
    5. <filename> (<tier>)

    0. Cancel — exit without changes

    Enter comma-separated numbers (e.g. `1,4,5`), or `all`, or `none` to use only requirements.md + blueprint, or `0`/`cancel`:
    ```

    Let `N` be the highest number. Then end the turn; parse the reply on the next message: normalise; `0`/`cancel`/`q`/`exit` → `cancelled`; `none`/empty → step 9 empty → `selected-none`; `all` → select every listed item; otherwise comma-separated integers `1..N`, deduped, validated. Invalid → re-print + prompt; **2-retry budget**, third invalid → `cancelled`.
7. **Primary wireframe basis.** If the selection includes ≥1 source-D variant:
    - exactly one → flag it `primary_basis: true` automatically;
    - more than one → surface one `AskUserQuestion`: *"Which wireframe variant is the primary basis for this prototype's layout/workflow? (the others are advisory reference)"*, options = the selected variant ids + "None — treat all as advisory". The chosen one gets `primary_basis: true`; "None" leaves all `false` (no fast path).
8. **Confirmation gate.** One `AskUserQuestion` `{ Confirm, Edit, Cancel }` enumerating the chosen items by name. Edit → return to step 6 with a fresh retry counter; Cancel → `cancelled`.
9. **Write JSON.** Render to `<output_dir><name_slug>/supporting-inputs.json` (create parents lazily). Schema:

    ```json
    {
      "scope_slug": "<scope_slug>",
      "name_slug": "<name_slug>",
      "selected_at": "<ISO-8601>",
      "sources": {
        "requirement": { "path": "requirements/requirements.md", "always": true },
        "analyse_requirement": [ { "name": "", "output_path": "", "format": "html|md", "sidecar_path": "", "sidecar_present": true, "prototype_roles": [] } ],
        "analyse_inputs": [ { "name": "", "output_path": "", "format": "html|md", "prototype_roles": [] } ],
        "wireframes": [ { "variant_id": "", "manifest_path": "", "variant_position_path": "", "primary_basis": false } ],
        "input_docs": [ { "filename": "", "original_path": "", "tier": "" } ]
      }
    }
    ```

    Empty classes are empty arrays. `prototype_roles` per row is verbatim from the static table. Compute sha256, Write, then `framework/skills/verify-artifact-write.md` with `expected_min_bytes: 64`. On `RF-04 trigger`, surface and return without advancing.
10. **Selection-size re-check.** On non-empty selections, estimate architect/drafter-side cost (analysis sidecars at 20 KB; legacy prose at on-disk size; wireframe `variant-position.json` ~small; input docs at on-disk size). If the sum exceeds 200 KB, surface `AskUserQuestion` `{ Re-pick, Proceed anyway, Cancel }` (mirrors `select-supporting-analyses.md` step 10).
11. **Return** `selected` | `selected-none` | `cancelled`.

## Self-validation
- The on-disk filter ran before the list was built for B and C; no absent analysis appears. Source D only lists variants present in `variants.json`. Source E excludes `Unsupported` rows.
- A (requirements.md) is always represented as `sources.requirement.always = true`; it is never an optional pick.
- The Brand source line was printed (on both the menu path and the all-empty auto-proceed path) with text matching the `ds_present`/`brand_locked` row; it carries no pick number and does not appear in `supporting-inputs.json`. The `supporting-inputs.json` schema is unchanged by this line.
- Exactly one wireframe variant carries `primary_basis: true` iff ≥1 variant was selected and the consultant did not choose "None".
- Every selected row carries its `prototype_roles` verbatim from the closed table.
- The JSON write was verified; on `cancelled`, no JSON was written.
- The numbered list was printed at most three times (initial + 2 retries).

## Anti-patterns
- Do not surface analyses/inputs whose output does not resolve on disk (the load-bearing filter). No "(not yet run)" hints.
- Do not let source A be a pick — `requirements.md` is always included.
- Do not allow more than one `primary_basis: true` — the fast path needs a single basis.
- Do not invent `prototype_roles` outside the closed enum; `context-only` never widens scope or the Property closed set.
- Do not write outside `<output_dir><name_slug>/`.
- Do not read the selected files' contents here — selection and consumption are separate concerns (the drafter consumes them). This includes the design-system: Glob it for existence only; never open or parse it (the brand is captured at orchestrator Step F1 and themed by `extract-brand-theme.md`).
- Do not make the design-system a numbered/selectable item, give it a `prototype_role`, or add it to `supporting-inputs.json` — it is an informational Brand source line only.
- Do not skip the confirmation step or write the JSON before confirmation.
