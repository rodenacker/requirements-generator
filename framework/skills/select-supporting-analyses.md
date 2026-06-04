# select-supporting-analyses.md

**Purpose:** Read the `framework/assets/analyses/registry.md` methodology registry, filter the methodologies whose `status` is `mvp` **and** whose `output_path` currently resolves on disk (i.e. the consultant has actually completed that analysis), present the completed-on-disk subset to the consultant as a printed numbered list, parse a comma-separated multi-select reply, capture confirmation via `AskUserQuestion`, and write the consultant's selections to `<output_dir>/<scope_slug>/analyses-inputs.json`. The selected analyses are then read by the `blueprint-architect` agent alongside `requirements/requirements.md` to augment and refine the wireframe brief.

The skill is wireframe-private (today's only caller is `framework/orchestrators/wireframe-orch.md` at step 0c-bis). The wireframe-private placement is deliberate: a future `/prototype` pipeline will consume analyses differently (FK constraints, validation rules, default values vs. the wireframe's screen-shape consumption) and should author its own selector with its own per-method-to-role mapping.

The skill borrows the print-and-parse interaction shape from `framework/skills/analysis-selector.md` (registry → numbered list → typed reply → 2-retry budget), extends it to comma-separated multi-select, and adds:

- An on-disk-presence filter (the load-bearing rule: never surface a methodology whose output does not exist).
- A static per-method `architect_roles` mapping the skill stamps into the JSON.
- A per-selection `sidecar_path` + `sidecar_present` stamp pointing at the analyser's structured JSON sidecar (per `framework/assets/analyses/sidecar-schema.md` — the architect's step-02 prefers the sidecar over the prose to avoid context bloat).
- A confirmation `AskUserQuestion` after parse (`Confirm / Edit / Cancel`).
- A `verify-artifact-write` post-write check.
- A `check-context-bloat` re-check after write (because the selected analyses become additional architect inputs).

## Inputs

- `registry_path` — repo-relative path to the analyses registry. Required. Wireframe-orch passes `"framework/assets/analyses/registry.md"`.
- `scope_slug` — kebab-case slug captured at the calling orchestrator's earlier scope-selector step. Required. Drives the output path.
- `output_dir` — repo-relative path of the per-pipeline output root. Required. Wireframe-orch passes `"wireframes/"`. The skill writes to `<output_dir><scope_slug>/analyses-inputs.json` (the caller is responsible for trailing-slash convention).

## Outputs

Exactly one of:

- **`selected`** — `selections[]` is non-empty; `analyses-inputs.json` has been written and `verify-artifact-write` returned `pass`. The orchestrator advances.
- **`selected-none`** — the consultant explicitly accepted "no supporting analyses" (typed `none`, replied empty), or the skill **auto-proceeded on the zero-on-disk branch**; an empty-`selections[]` JSON has been written and verified. The orchestrator advances (the architect runs without consuming analyses).
- **`cancelled`** — the consultant chose to cancel out of the prompt (typed `0` / `cancel` / `q` / `exit`, hit the retry budget, or chose `Cancel` at confirmation). No JSON is written. The orchestrator exits cleanly.

## Used by

- `framework/orchestrators/wireframe-orch.md` — step 0c-bis, with `registry_path: "framework/assets/analyses/registry.md"`, `scope_slug: <chosen.scope_slug>`, `output_dir: "wireframes/"`.

## Static method → architect_roles mapping

The skill stamps an `architect_roles` array into every `selections[]` row, drawn from this static table. The architect consumes the roles to decide where in its workflow to thread each selected analysis. Adding a new `mvp` methodology to `framework/assets/analyses/registry.md` requires also appending a row here.

| `name` (registry slug) | `architect_roles` |
|---|---|
| `data-model` | `screen-properties-cross-check`, `screen-inventory-entity-bijection` |
| `task-flows` | `screen-inventory`, `screen-flow`, `per-screen-cta-set` |
| `state-diagram` | `screen-inventory`, `per-screen-state-chips` |
| `use-cases` | `screen-inventory`, `screen-flow`, `per-screen-cta-set` |
| `user-journeys` | `screen-inventory`, `variant-philosophy` |
| `sequence-diagram` | `screen-flow`, `per-screen-async-states` |
| `activity-diagram` | `screen-flow`, `per-screen-role-visibility` |
| `ooux` | `screen-inventory-entity-bijection` |
| `jtbd` | `variant-philosophy` |
| `trade-off-dimension-analysis` | `variant-dimension-applicability` |
| `glossary` | `copy-vocabulary` |
| `opportunity-solution-trees` | `feature-presence`, `variant-philosophy` |
| `crud-coverage` | `screen-inventory-entity-bijection`, `per-screen-cta-set` |
| `decision-tables` | `upstream-only` |
| `five-whys` | `upstream-only` |
| `mvp-slicing` | `upstream-only` |
| `faceted-classification` | `upstream-only` |

Role semantics (closed enum, consumed by `blueprint-architect.md`):

- `screen-inventory` — analysis can surface a screen the architect missed by re-reading `requirements.md`. Cannot widen the feature set (see Anti-Pattern below).
- `screen-flow` — analysis informs the order/branching of screens within the inventory.
- `screen-properties-cross-check` — analysis is cross-checked against the §7 + F-NN closed set. Discrepancies are flagged in blueprint prose; the closed set is **never widened**.
- `screen-inventory-entity-bijection` — analysis informs the object-to-screen bijection (CRUD list/detail).
- `per-screen-cta-set` — analysis informs primary CTA labelling and presence per screen.
- `per-screen-state-chips` — analysis informs status-badge set per screen.
- `per-screen-async-states` — analysis informs polling/pending screen variants.
- `per-screen-role-visibility` — analysis informs persona-bound visibility per screen.
- `variant-philosophy` — analysis informs the per-variant `design_philosophy` / strengths / weaknesses / use-when prose.
- `variant-dimension-applicability` — analysis informs which trade-off dimensions are coherent for the scope.
- `copy-vocabulary` — analysis informs labels, hints, help text, error messages.
- `feature-presence` — analysis informs which features make it into the variant set.
- `upstream-only` — analysis is for upstream requirements review only; the architect ignores it (today: `five-whys`).

## Procedure

1. **Read the registry.** `Read` the file at `<registry_path>`. Parse the YAML frontmatter. Locate the `methodologies:` list.
2. **Filter to MVP.** Retain rows whose `status` is the literal string `mvp`. Discard `future` rows.
3. **Filter to completed-on-disk.** For each MVP row, `Glob` the row's `output_path` to determine whether the file exists. **Drop every row whose output does not exist.** This is the load-bearing filter — the consultant must never see a methodology they have not produced. Do not annotate missing rows; do not append "(not yet run)" hints; do not append "Run /analyse-requirement first" hints inside the numbered list. Missing methodologies are simply absent from the list.
4. **Auto-proceed — zero on-disk analyses.** If the filtered list (MVP ∩ on-disk) is empty, do **not** prompt. Print exactly one plain-text line:

    *"No analyses on disk; proceeding from `requirements.md` alone — run `/analyse-requirement` first if you want goal/journey augmentation."*

    Then jump to step 8 with an empty selection set, write the empty-`selections[]` JSON (step 9 — the write stays **inside this skill**; the calling orchestrator is a strict delegator and must not write the artefact itself), verify via `framework/skills/verify-artifact-write.md`, and return `selected-none`. Do **not** surface any `AskUserQuestion`. Zero analyses is the common first-run case, not a decision; a full interaction round for it is removed. The consultant retains a Cancel affordance at the architect's conditional gate (Stage 2) and the orchestrator-owned Stage-4b accept gate, and can abort the whole pipeline at any prompt — so no decision is lost. Supporting analyses are **optional augmentation**, not a prerequisite (the architect runs from `requirements.md` alone on `selected-none`). This is the **only** step in the skill that gestures at methodologies that don't yet exist; it does not enumerate them by name, and it prints the notice **outside** any numbered list.
5. **Build the numbered list** (only when ≥1 on-disk MVP rows remain). Number the retained rows starting at **1**, in **registry order**. Do not re-sort. For each row, format a three-line block:

    `{{n}}. {{name}}`
    `{{description}}`
    `Output: {{output_path}}`

    Rows are separated by a single blank line. After the methodology lines, append a blank line and the cancel line:

    `0. Cancel — exit without changes`

    Let `N` be the count of completed-on-disk MVP rows.

6. **Surface the prompt and parse the reply.** Print the assembled block to the consultant as plain text:

    ```
    Available supporting analyses (completed under analyse-requirements/):

    1. <name>
    <description>
    Output: <output_path>

    2. <name>
    <description>
    Output: <output_path>

    …

    N. <name>
    <description>
    Output: <output_path>

    0. Cancel — exit without changes

    Enter comma-separated numbers (e.g. `1,3,4`), or `all` for every analysis listed, or `none` to skip, or `0`/`cancel` to abort:
    ```

    Then end the turn. On the consultant's next chat message:

    1. **Normalise** the reply — trim leading/trailing whitespace, lowercase.
    2. **Cancel keywords** — if the normalised reply equals `0`, `cancel`, `q`, or `exit`, return `cancelled` (skip to step 9).
    3. **None keywords** — if the reply equals `none` or is empty after trim, jump to step 8 with an empty selection set and return `selected-none` after verify.
    4. **All keyword** — if the reply equals `all`, select every on-disk MVP row and advance to step 7.
    5. **Comma-separated numeric parse** — split on `,`, trim each token, validate every token parses as an integer `k` with `1 ≤ k ≤ N`. Deduplicate. If every token is valid and the deduplicated set is non-empty, advance to step 7 with the selected rows.
    6. **Invalid** — anything else (non-numeric token, out-of-range number, empty token between commas, mixed text+number, only `0`/`cancel` mid-list) is invalid. Print one line:

        *"Invalid selection. Enter comma-separated numbers from 1–{{N}} (e.g. `1,3,4`), or `all` / `none` / `0` / `cancel`."*

        Then re-print the full numbered list + prompt line (same shape as above), end the turn, and parse the next reply through the same loop.

    7. **Retry budget** — keep an in-memory counter of invalid replies. The budget is **2 re-prompts**; on the third invalid reply (counter would become 3), print one final line *"Too many invalid selections. Cancelling."*, and return `cancelled`. Do not persist the counter.

7. **Confirmation gate.** Surface a single `AskUserQuestion`:
    - Question: *"Confirm selecting these N supporting analyses for wireframe scope `{{scope_slug}}`? They will be read by the blueprint-architect alongside `requirements/requirements.md` to augment and refine the wireframe brief."*
    - Header: `Confirm analyses`
    - `multiSelect: false`
    - Options:
        1. `Confirm — write analyses-inputs.json and proceed (Recommended)`
        2. `Edit — re-prompt the numbered list`
        3. `Cancel — exit without changes`
    - Branch:
        - **Confirm** — advance to step 8.
        - **Edit** — return to step 5 with a fresh retry counter; the selected set is reset.
        - **Cancel** — return `cancelled` without writing.

    Render the question text with the selected method names enumerated in the question body (e.g. *"Confirm selecting these 4 supporting analyses (data-model, task-flows, state-diagram, glossary) for wireframe scope `file-upload-flow`?"*).

8. **Compute sidecar paths.** For each selection, derive the structured-sidecar path via the canonical convention defined in `framework/assets/analyses/sidecar-schema.md > Section 1 (Naming convention)`:

    - Take the directory of `output_path` (e.g. `analyse-requirements/DATA-MODEL/`).
    - Append `<method-lowercase>.sidecar.json` using the registry `name` slug (e.g. `data-model.sidecar.json`).
    - Result: `analyse-requirements/<METHOD>/<name>.sidecar.json` (e.g. `analyse-requirements/DATA-MODEL/data-model.sidecar.json`).

    `Glob` the derived path. Set `sidecar_present = true` iff the file exists on disk, `false` otherwise. The skill does **not** read the sidecar's contents — the architect reads it at step-02 block 2.6 (with drift detection per `RF-08`). When `sidecar_present == false`, the architect falls back to a bounded prose Read per `framework/shared/refusal-registry.md > RF-09` (60 KB cap; consultant prompted on overflow).

9. **Write the JSON artefact.** Render the document below to `<output_dir><scope_slug>/analyses-inputs.json` (create the `<scope_slug>/` parent directory lazily if absent). The JSON has exactly four top-level fields and no others (do not add `skipped_absent`, `available_to_run`, or any field that tracks methodologies the consultant did not pick because they have not yet produced them):

    ```json
    {
      "scope_slug": "<scope_slug>",
      "selected_at": "<ISO-8601 timestamp at write>",
      "registry_path": "<registry_path>",
      "selections": [
        {
          "name": "<row.name>",
          "output_path": "<row.output_path>",
          "format": "<\"html\" | \"md\" — inferred from output_path extension>",
          "registry_description": "<row.description verbatim>",
          "architect_roles": ["<role>", "<role>"],
          "sidecar_path": "<convention path computed at step 8>",
          "sidecar_present": true
        }
      ]
    }
    ```

    On `selected-none` paths, `selections` is an empty array. `architect_roles` per selection is drawn verbatim from the static table above; do not infer or omit. `format` is `"html"` when `output_path` ends in `.html`, `"md"` when it ends in `.md` (today's two formats); any other extension is an internal contract violation and the skill halts with a structured error. `sidecar_path` is always populated (it is the *conventional* path — present or absent on disk does not affect the field value); `sidecar_present` reflects the Glob result from step 8.

    Compute sha256 of the rendered JSON, then invoke `framework/skills/verify-artifact-write.md` with `path: "<output_dir><scope_slug>/analyses-inputs.json"`, `expected_sha256: <digest>`, `expected_min_bytes: 64`. On `RF-04 trigger`, surface the predicate per `framework/shared/refusal-registry.md > RF-04` and return without advancing.

    **Soft warn on absent sidecars.** After verify-artifact-write returns `pass`, if any `selections[i].sidecar_present == false` AND `selections[i]` belongs to a method whose `output_path` exceeds 60 KB on disk (i.e. would trip `RF-09` at architect-read time), surface a single in-thread plain-text warning *"Note: selected analyses {{names}} have no structured sidecar on disk yet and their prose artefacts exceed the 60 KB legacy-fallback cap. The blueprint-architect will surface `RF-09` at step-02; choose `regenerate-and-retry` after re-running `/analyse-requirement` for these methods, or `proceed-with-bounded-read` to accept degraded-fidelity prose extraction."*. This warning is informational only — the skill returns `selected` regardless; the architect surfaces the actionable `AskUserQuestion` later.

10. **Context-bloat re-check.** On a non-empty `selections[]`, compute the per-selection context-cost estimate: when `sidecar_present == true` for a selection, use 20 KB as its bound (the hard cap defined in `framework/assets/analyses/sidecar-schema.md`); when `sidecar_present == false`, use the on-disk byte size of its `output_path` (the architect will fall back to a bounded prose Read, capped at 60 KB by `RF-09`). Sum across `selections[]`. If the sum exceeds 200 KB (a soft threshold below `check-context-bloat`'s 250 KB hard threshold, leaving headroom for `requirements.md` + the pattern catalogue + the in-thread orchestrator state), surface a single `AskUserQuestion`:
    - Question: *"Selected analyses total {{KB}} KB estimated architect-side context cost (sidecars capped at 20 KB each; legacy prose-only selections counted at their on-disk size). Combined with `requirements.md` and the pattern catalogue, this approaches the context-bloat threshold (`RF-05`). The wireframe pipeline may struggle to read every selected file in full. Re-pick a smaller set?"*
    - Header: `Context risk`
    - `multiSelect: false`
    - Options:
        1. `Re-pick — return to the numbered list (Recommended)`
        2. `Proceed anyway — accept the risk; architect may degrade`
        3. `Cancel — exit without changes (the JSON write at step 9 is left on disk and will be reused on re-invoke)`
    - Branch:
        - **Re-pick** — return to step 5 with a fresh retry counter and a fresh selection set; the JSON written at step 9 will be overwritten on re-confirmation. (The Edit-cycle is bounded by the consultant's patience; the skill imposes no additional cap here.)
        - **Proceed anyway** — return `selected`.
        - **Cancel** — return `cancelled`. The previously-written JSON remains on disk; the orchestrator's next invocation will detect it on the `mode = "regenerate-variants"` / `mode = "add-variant"` reuse path.

11. **Return the consultant's choice.**
    - If step 5–7 produced a valid non-empty selection and the JSON was written + verified: return `selected`.
    - If step 5 returned a `none` / empty path, or step 4 auto-proceeded on the zero-on-disk branch, the empty-`selections[]` JSON was written + verified: return `selected-none`.
    - If any step returned a cancel keyword, retry-budget exhaustion, `Cancel` option, or write-verify failure: return `cancelled` (no further work).

## Self-validation

- The numbered list was printed at most three times in total (initial print plus up to two re-prompts on invalid input). The skill never loops indefinitely.
- On the zero-on-disk branch, **no `AskUserQuestion` was surfaced**: a single plain-text notice was printed, the numbered list was not rendered, and an empty-`selections[]` JSON was written + verified before returning `selected-none`.
- Methodologies were numbered in registry order; no row was re-sorted alphabetically or otherwise.
- The on-disk filter was applied **before** the numbered list was rendered; the printed list contains zero rows whose `output_path` does not resolve on disk.
- The JSON artefact contains exactly four top-level fields (`scope_slug`, `selected_at`, `registry_path`, `selections`); it does not carry a `skipped_absent`, `not_yet_run`, `available_to_run`, or any other field that enumerates methodologies the consultant did not pick because they have not been produced.
- Every `selections[i]` has `name`, `output_path`, `format`, `registry_description`, `architect_roles`, `sidecar_path`, `sidecar_present` populated.
- Every `selections[i].output_path` resolves on disk (the existence check at step 3 was not bypassed).
- Every `selections[i].architect_roles` array is drawn verbatim from the static table; values come from the closed enum listed above.
- Every `selections[i].sidecar_path` matches the canonical convention `<dirname(output_path)>/<name>.sidecar.json` (the skill does not invent a different path).
- Every `selections[i].sidecar_present` reflects an actual `Glob` of `sidecar_path` at step 8; the field is never assumed `true` without the check.
- `verify-artifact-write` returned `pass` for every write path.
- The retry budget was respected — exactly **2** re-prompts; the third invalid reply returns `cancelled`.
- On a `cancelled` return, no JSON was written.

## Anti-Patterns

- Do not surface methodologies whose `output_path` does not resolve on disk. The completed-on-disk filter at step 3 is the **load-bearing rule**; appending "(not yet run)" suffixes, "Run /analyse-requirement first" hints, or "coming soon" annotations to absent rows defeats the rule. The consultant is selecting *from what they have produced*, not browsing the methodology catalogue.
- Do not record absent methodologies anywhere in the JSON. No `skipped_absent` field, no `available_to_run` field, no audit trail of "what the consultant didn't pick because they hadn't produced it." The on-disk subset is the universe; absent rows are out of scope.
- Do not hardcode methodology names or paths. The registry is canonical; the static `architect_roles` table keys on the registry's `name` slug.
- Do not invoke `AskUserQuestion` for the multi-select itself. The list cardinality (17 mvp rows in the registry today, ≤ that many on disk) exceeds the 4-option cap. Print-and-parse handles arbitrary cardinality in one prompt; the `AskUserQuestion` calls in this skill are limited to (a) post-parse Confirm/Edit/Cancel, and (b) the optional context-bloat re-check.
- Do not surface an `AskUserQuestion` on the zero-on-disk branch. Zero analyses is not a decision — auto-proceed with a printed notice and return `selected-none`. The Cancel affordance lives at the architect's conditional gate (Stage 2) and the orchestrator's Stage-4b accept gate, not here.
- Do not omit the confirmation step. The print-and-parse step accepts comma-separated text; the `AskUserQuestion` confirmation is the consultant's structured chance to verify the parse landed correctly.
- Do not write the JSON before confirmation. The confirmation step is the commit point; an Edit response must not leave a stale JSON on disk.
- Do not write the JSON outside `<output_dir><scope_slug>/`. The skill is parameterised on `output_dir`; cross-pipeline contamination (e.g. writing into `blueprints/` because the architect reads from there) is a structural bug.
- Do not invoke the `blueprint-architect` agent from this skill. Selection and consumption are separate concerns — the orchestrator owns invocation; the architect owns consumption.
- Do not invent `architect_roles` values outside the closed enum. The architect consumes the enum to thread roles into specific step files; an unknown role would be silently ignored.
- Do not skip `verify-artifact-write`. Write-verify is the only protection against partial writes that the orchestrator's Stage-1 handback gate depends on.
- Do not silently allow an analysis to introduce new bindable properties downstream. The skill does not validate the architect's downstream behaviour, but the closed enum's `screen-properties-cross-check` role is semantically "**cross-check, do not widen**" — the architect's step files (step-04 onwards) enforce the no-widening invariant per `CLAUDE.md > Constraints > Wireframe pipeline never invents object properties`.
