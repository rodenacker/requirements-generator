# scope-selector.md

**Purpose:** Capture a named scope of requirement IDs from `requirements/requirements.md` (functional `F-NN`, business rules `BR-NN`, UI feature needs `UI-NN`, goals `G-NN`, §3 personas, §5 task flows, §7 data shapes) and write a structured `scope.json` to a caller-supplied directory. Pipeline-neutral: the same skill drives `/wireframe` today and will drive a future `/prototype` without modification.

**Intent-first by default.** The happy path asks the consultant one direction prompt (free-form intent) and one confirmation. Everything else — slug derivation, requirement-ID resolution, persona enumeration, default dimension profile, and (when `propose_divergence_axes == true`) the recommended divergence profile extrapolated from the spec's user goals + persona goal-types — is auto-inferred by the LLM from the intent prose + `requirements/requirements.md` + `framework/assets/wireframes/domain-defaults.md` + `framework/assets/wireframes/divergence-heuristics.md`. The consultant can override at the confirmation gate via `Edit scope` (per-ID structural pickers, the legacy structural-mode logic preserved as opt-in) or `Edit dimensions` (override the default diverging dimensions and cardinality before the architect runs — this supersedes any recommended divergence profile).

The skill is **interactive**: it uses `AskUserQuestion` for the intent prompt, the confirmation gate, and (when entered) the Edit branches. It does **one** write per invocation — the `scope.json` artefact — and verifies via `framework/skills/verify-artifact-write.md`.

## Inputs

- `output_dir` — repo-relative root directory under which `<output_dir>/<scope_slug>/scope.json` is written. **Required.** Wireframe pipeline passes `"blueprints/"`. A future `/prototype` pipeline passes `"blueprints/"` as well (the shared `blueprints/` directory is the cross-pipeline architectural contract — both pipelines can author against the same scope-slug without duplication; the consultant explicitly accepts overwrite at the calling orchestrator's prior-set gate). The skill writes to `<output_dir>/<scope_slug>/scope.json`; the calling orchestrator owns the prior-set overwrite gate (see `framework/orchestrators/wireframe-orch.md > Pipeline > step 0d`).
- `pipeline_name` — short string used in the surfaced prompts and in the `scope.json`'s `pipeline_origin` field. **Required.** Wireframe passes `"wireframe"`; future `/prototype` passes `"prototype"`. The skill never branches on this value beyond surfacing it; per-pipeline behaviour stays in the caller.
- `requirements_path` — optional repo-relative path to the requirements doc. Defaults to `"requirements/requirements.md"`. The skill reads this file in full to ground intent resolution and to enumerate personas.
- `domain_defaults_path` — optional repo-relative path to the domain-defaults asset. Defaults to `"framework/assets/wireframes/domain-defaults.md"`. Read at confirmation time to surface the default dimension profile so the consultant sees what the architect will do.
- `propose_divergence_axes` — optional bool. **Default `false`.** When `true`, the skill executes the new Step 3.5 (goal/persona-driven divergence inference per `framework/assets/wireframes/divergence-heuristics.md`) and persists the result to `scope.json > divergence_profile`. When `false`, Step 3.5 is skipped entirely and `divergence_profile` is set to `null` — the skill behaves exactly as it did before this parameter existed. Wireframe-orch passes `true`; a future `/prototype` orchestrator passes `false` (or omits it), preserving today's neutral flow. The skill **never branches on `pipeline_name` for this behaviour** — the flag is the only switch.

## Outputs

Exactly one of:

- **`selected`** — the in-memory return payload `{ scope_slug, mode, scope_path }` where `scope_path = <output_dir>/<scope_slug>/scope.json`. The orchestrator captures `scope_slug` into its in-memory variable. The skill has already written and verify-artifact-write'd `scope.json`.
- **`cancelled`** — the consultant chose to cancel at any prompt. The orchestrator exits cleanly without invoking any downstream agent. No file is written.

## Used by

- `framework/orchestrators/wireframe-orch.md` — step 0c, with `output_dir: "blueprints/"`, `pipeline_name: "wireframe"`, default `requirements_path`, `propose_divergence_axes: true` (so the goal/persona-driven divergence profile is inferred and persisted).
- A future `framework/orchestrators/prototype-orch.md` — analogous step, with `output_dir: "blueprints/"`, `pipeline_name: "prototype"`, `propose_divergence_axes: false` (or omitted — the default). **Zero skill changes required** when that pipeline ships; the flag keeps `/prototype` on today's neutral flow.

## Procedure

### Step 1 — Capture intent

Surface a single `AskUserQuestion`:

- Question: *"Describe what to `{{pipeline_name}}` (free-form prose). For example: 'the file-upload flow including validation and confirmation', 'the approval queue with bulk-decision', 'the transaction table view with filters'."*
- Header: `Scope intent`
- `multiSelect: false`
- Options:
    1. `Enter intent` — description: `"Type the intent prose in the response."`
    2. `Cancel — exit without writing scope`

On `Cancel`, return `cancelled`. On `Enter intent`, the consultant's next conversation turn is the prose. Capture as `intent_description`. Trim leading/trailing whitespace; reject empty (re-prompt up to 2 times, then return `cancelled`).

### Step 2 — Auto-derive slug

Inline reasoning. Derive a kebab-case slug from `intent_description` by:

- Extracting 2–4 of the most concrete nouns + verb-stems (e.g. `file-upload-flow`, `approval-queue`, `transaction-table-view`).
- Lowercasing, replacing whitespace with `-`, dropping articles (`the`, `a`, `an`), dropping connective phrases (`including`, `with`).
- Normalising the result to match `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`.

If the derivation is unambiguous, capture as `scope_slug` and advance. If the intent prose is too generic to yield a stable slug (e.g. *"wireframe the app"*, *"the main thing"*) or the derived slug would clash with a generic placeholder (`main`, `app`, `tool`, `feature`), surface a single `AskUserQuestion`:

- Question: *"Couldn't derive a clear slug from `{{intent_description}}`. Please type a kebab-case slug (e.g. `file-upload-flow`)."*
- Header: `Scope slug`
- Options:
    1. `Enter slug`
    2. `Cancel — exit without writing scope`

On `Cancel`, return `cancelled`. On `Enter slug`, parse the next turn, normalise, validate against `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`. Retry budget: 2 re-prompts on invalid; third invalid returns `cancelled`.

### Step 3 — Auto-resolve scope from intent

3.1 **Read the requirements doc.** `Read` the file at `requirements_path`. The orchestrator's prerequisite gate has already guaranteed it exists and is non-empty. Compute and remember its `sha256` for the artefact's `requirements_sha256` field.

3.2 **Resolve the intent to candidate IDs.** Inline reasoning over the full requirements doc. For each candidate, capture: `{ id_or_name, category, requirement_text_first_line }`. Categories: `functional`, `business_rules`, `ui_needs`, `goals`, `task_flows`, `data_shapes`. The resolution must be evidence-based — every candidate must be justified by a verbatim phrase or topic match in the doc; speculative inference without textual anchor is not added. Truncate `requirement_text_first_line` to 120 chars.

3.3 **Enumerate personas.** Walk §3 of the requirements doc and capture every `### <Name>` header as a persona name. Populate `personas_available`.

3.4 **Read the domain defaults.** `Read` the file at `domain_defaults_path` and extract the default dimension profile (Section 1 of `domain-defaults.md` gives `D3 density-focus` + `D1 speed-accuracy`; Section 2 gives default cardinality 2). The defaults are surfaced verbatim in the confirmation prompt at Step 4. If `domain_defaults_path` is unreadable, treat as a hard halt and surface *"Could not read `{{domain_defaults_path}}` — scope-selector cannot complete without the default dimension profile. Aborting."* and return `cancelled`.

### Step 3.5 — Infer divergence profile

**Run this step only when `propose_divergence_axes == true`.** When the flag is `false` (a future `/prototype` invocation, or any caller that wants today's flow), skip this step entirely and set the in-memory `divergence_profile = null`; advance to Step 4 with the static-default confirmation text.

3.5.1 **Read the heuristics asset.** `Read` `framework/assets/wireframes/divergence-heuristics.md`. If it is unreadable, do **not** hard-halt — degrade gracefully: log an in-thread note *"Could not read divergence-heuristics.md; falling back to the static default dimension profile."*, set `divergence_profile = null`, and advance to Step 4 with the static-default confirmation text (the architect's `domain-defaults.md` fallback still produces a valid `variants.json`).

3.5.2 **Execute §1–§4 over the in-scope goals + personas.** Using the full requirements doc already read at Step 3.1, the auto-resolved scope from Step 3.2, and the `personas_available` from Step 3.3:

- **§1 goal-type inference** — for each in-scope goal (`scope.sources.goals` plus goals reached by in-scope task-flows / stories), classify into a registry-§2 goal-type, first-hit-wins, citing the verbatim anchor for each hit.
- **§2 persona goal-type assignment** — for each persona in `personas_available`, derive `(frequency, expertise, role, dominant-goal-type)` using the architect's trait-extraction vocabulary referenced by the heuristics (`framework/agents/blueprint-architect/steps/step-02-read-inputs.md > 2.4`).
- **§3 divergence decision** — apply exactly one of Rule P / Rule D / Rule W.
- **§4 realization recommendation** — populate `realization_recommendation` per bound persona's dominant goal-type.
- **§4b posture recommendation** — for each `variant_bindings[i]`, look up `recommended_posture` (`P1`..`P6`) + `posture_label` from `framework/assets/wireframes/design-philosophies.md > Posture selection by persona goal-type`, keyed by the binding's `(persona_goal_type, traits, pole)`, pole-consistent with the binding's `pole`. (If `design-philosophies.md` is unreadable, leave both fields `null` — the architect then falls back to today's position-derived structural choices; do not hard-halt.)

3.5.3 **Produce the in-memory `divergence_profile`.** Assemble the object per the schema in Step 7 (`source` left provisional — the scope-selector finalises it at Step 4: `"recommended-confirmed"` for an accepted Rule-P profile, `"static-default"` for Rule D / Rule W). Capture `evidence_strength`, `dimensions`, `cardinality`, `variant_bindings[]` (with verbatim `evidence` **and** `recommended_posture` + `posture_label` per §4b), and `realization_recommendation`. **Do not write anything yet** — the profile is surfaced for confirmation at Step 4 and persisted only at Step 7.

### Step 4 — Confirmation gate

Surface a single `AskUserQuestion`:

- Question text: a multi-line string prefaced by *"Resolved your intent `{{intent_description}}` to scope `{{scope_slug}}`. Review and accept, or edit."*. Below the preface, render:
    - **Slug:** `{{scope_slug}}`
    - **Requirement IDs** (counts per category): e.g. *"3 functional, 2 business rules, 4 UI needs, 1 goal, 1 task flow, 1 data shape"* — render `0` categories as omitted.
    - **Personas in scope:** comma-separated `personas_available`.
    - **Variant divergence** — render this block per the divergence profile produced at Step 3.5 (or the static default when Step 3.5 was skipped):
        - **When Step 3.5 produced a Rule-P profile** (`source` provisional `"recommended-confirmed"`, `evidence_strength: "strong"`): render the recommendation as **"(Recommended)"** — one line per variant in `variant_bindings[]` formatted as *"`{{persona}}` → {{posture_label}} · {{plain-English pole label}} — {{one-line rationale}}"*, where `posture_label` is the binding's `recommended_posture` label (e.g. *"Efficiency-First"*; omit only if `null`) and the pole label comes from `framework/assets/wireframes/position-vocabulary.md` for the separating dimension's recommended position (never the cryptic `D3+`/`-1` notation). Lead the block with *"Recommended (from your goals + personas): variants diverge on `{{separating dimension}}`, one per persona — each gets a UX posture (design philosophy)."* and append *"The architect picks exact polar positions automatically and applies each posture's layout/workflow recommendations. Choose `Edit dimensions` to override this recommendation with a manual dimension set."*
        - **When Step 3.5 produced a Rule-D / Rule-W profile, OR Step 3.5 was skipped** (`propose_divergence_axes == false` / heuristics unreadable): render today's static text — *"density-focus · speed-accuracy"* (the two defaults per `domain-defaults.md > Section 1`), appended with *"Default variants: 2 (`CAREFUL-DEFAULT`, `POWER-DENSE`). The architect picks polar positions automatically — see `framework/assets/wireframes/domain-defaults.md > Section 3` for the exact positions."* When the profile is Rule W (weak evidence), annotate the block *"(static default — goal evidence weak/uniform)"* so the consultant knows it is a fallback rather than a goal-extrapolated divergence.
- Header: `Scope`
- `multiSelect: false`
- Options:
    1. `Accept — write scope.json (Recommended)`
    2. `Edit scope — change slug, add or remove requirement IDs`
    3. `Edit dimensions — override the default trade-off dimensions or cardinality`
    4. `Cancel — exit without writing scope`

Branch:

- **Accept** — advance to Step 7 with `scope_mode = "intent"`, `dimension_override = null`. **Finalise the divergence profile:** if Step 3.5 produced a profile, set its `source = "recommended-confirmed"` (Rule P) or `source = "static-default"` (Rule D / Rule W) and carry it into Step 7 to be persisted as `scope.json > divergence_profile`. If Step 3.5 was skipped, `divergence_profile` stays `null`.
- **Edit scope** — advance to Step 5. The divergence profile (if any) is carried through unchanged — editing the scope IDs does not invalidate the persona/goal divergence recommendation, but the consultant returns to Step 4 where the recommendation is re-surfaced.
- **Edit dimensions** — advance to Step 6. **The manual dimension override supersedes the recommendation:** when the consultant confirms a `dimension_override` at Step 6, the divergence profile carried into Step 7 is tagged `source = "manual-override-supersedes"` (its `dimensions` / `cardinality` mirror the override so downstream readers see one coherent record; `dimension_override` remains the field the architect's precedence consumes first). If Step 3.5 was skipped, `divergence_profile` stays `null` and only `dimension_override` is populated.
- **Cancel** — return `cancelled`.

### Step 5 — Edit scope (legacy structural-mode pickers, opt-in)

This branch reuses the legacy structural-multi-select logic so consultants who want per-ID control still have it.

5.1 **Edit slug (optional sub-prompt).** Surface a single `AskUserQuestion`:

- Question: *"Current slug `{{scope_slug}}`. Edit?"*
- Header: `Edit slug`
- Options:
    1. `Keep — proceed to scope-ID editing`
    2. `Enter new slug`
    3. `Cancel — go back to confirmation`

On `Keep`, advance to step 5.2. On `Enter new slug`, parse the next turn, normalise, validate against `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`. Retry budget: 2 re-prompts on invalid. On `Cancel`, return to Step 4 (re-surface the confirmation prompt).

5.2 **Walk the requirements doc to enumerate selectable IDs.** Extract:

- Every `F-NN`, `BR-NN`, `UI-NN`, `G-NN` ID — canonically defined in §4 / §6 table rows (§1.7 is always present as scope-noted application-build guidance, but it remains a secondary reference for these IDs — never a design input; rely on §4 / §6).
- Every §5 task flow name (`### Flow: <name>` headers).
- Every §6.4.x UI feature row.
- Every §7 data shape name (`### <Name>` headers under §7).

Treat the auto-resolved IDs from Step 3.2 as the **pre-selected** starting set; the consultant edits from there rather than starting blank.

5.3 **Surface a sequence of multi-select prompts**, one per category, in this order: Functional, Business rules, UI needs, Goals, Task flows, Data shapes. For each category, use `AskUserQuestion` with `multiSelect: true`. Question text: *"Which `{{category}}` items are in scope for `{{scope_slug}}`?"*. Header: `Scope ({{category}})`. Options: each enumerated ID/name with the auto-resolved ones marked *"(Recommended)"* in their label; description = the one-line summary truncated to 80 chars. Add a final option `None / Skip this category` and a `Cancel — go back to confirmation` option. On `Cancel`, return to Step 4. If a category has zero enumerated items, skip its prompt silently.

5.4 Compile the selection into the `sources` block. Return to Step 4 (re-surface the confirmation prompt) with the updated slug + sources so the consultant can review or accept.

### Step 6 — Edit dimensions (override domain defaults)

This branch lets the consultant change the dimensions the architect will diverge on and the cardinality. Without this branch, the architect uses `domain-defaults.md`'s defaults.

6.1 **Capture cardinality.** Surface a single `AskUserQuestion`:

- Question: *"How many variants? Default 2. The hard cap is 3."*
- Header: `Variant cardinality`
- `multiSelect: false`
- Options:
    1. `2 — A/B comparison (Recommended)`
    2. `3 — three-way comparison (hard cap)`
    3. `Cancel — go back to confirmation`

On `Cancel`, return to Step 4.

6.2 **Capture diverging dimensions.** Surface a single `AskUserQuestion` with `multiSelect: true`. The selection size must equal the chosen cardinality (one dimension per variant). Question text: *"Which trade-off dimensions should variants diverge on? Pick exactly `{{cardinality}}`. Defaults (recommended for internal-productivity scopes): density-focus, speed-accuracy."* Header: `Diverging dimensions`. Options (label format: `<name> — <careful pole> vs <power pole>`):

1. `speed-accuracy — careful vs throughput-oriented` (mark *"(Recommended)"* if `speed-accuracy` is in defaults)
2. `power-simplicity — novice-first vs expert-first`
3. `density-focus — spacious vs dense` (mark *"(Recommended)"* if `density-focus` is in defaults)
4. `control-automation — manual vs auto-fill / auto-decide`
5. `flexibility-consistency — bespoke vs rigidly uniform`
6. `Cancel — go back to confirmation`

(`memorability-discoverability` is omitted — inactive per `framework/assets/wireframes/tradeoff-dimensions-registry.md > Section 1`.)

On `Cancel`, return to Step 4. On selection mismatch (consultant ticks more or fewer than `cardinality`), re-prompt with the same options and a corrective note in the question text. Retry budget: 2 re-prompts; third mismatch returns to Step 4.

6.3 Compile `dimension_override = { dimensions: ["density-focus", "speed-accuracy", ...], cardinality: <int> }` (dimension names in selection order; matches the key format the architect uses in `variants.json > dimension_positions`). When a `divergence_profile` was produced at Step 3.5, the manual override **supersedes** it — Step 4's Edit-dimensions branch tags the carried profile `source = "manual-override-supersedes"` and mirrors the override's `dimensions` / `cardinality` into it (so `scope.json` holds one coherent record), while `dimension_override` remains the field the architect's precedence consumes first. Return to Step 4 (re-surface the confirmation prompt) so the consultant sees the updated dimension profile and can accept or further edit.

### Step 7 — Write `scope.json`

7.1 **Compose the artefact** per the schema below. Include the optional `divergence_profile` object **alongside** `dimension_override` (never overloading it): the finalised profile carried from Step 4 (Rule P → `source: "recommended-confirmed"`; Rule D / Rule W → `source: "static-default"`; manual override at Step 6 → `source: "manual-override-supersedes"`), or `null` when Step 3.5 was skipped (`propose_divergence_axes == false`) or the heuristics asset was unreadable.

7.2 **Compute the sha256** of the rendered JSON string.

7.3 **Ensure the parent directory exists.** `Bash mkdir -p <output_dir>/<scope_slug>` (on PowerShell-only environments, the harness handles directory creation transparently via the Write tool; retry once via `mkdir` if the first Write fails on path-missing).

7.4 **Write the artefact.** `Write <output_dir>/<scope_slug>/scope.json` with the rendered JSON.

7.5 **Verify the write.** Call `framework/skills/verify-artifact-write.md` with `path = <output_dir>/<scope_slug>/scope.json`, `expected_sha256 = <rendered sha256>`, `expected_min_bytes = 96`. On `pass`, return `selected`. On `RF-04 trigger`, propagate the hard halt per `framework/shared/refusal-registry.md > RF-04`.

### Step 8 — Return

Return `selected` with the in-memory payload `{ scope_slug, mode, scope_path }`. `mode` reflects the path taken: `"intent"` if the consultant accepted at Step 4 without editing; `"structural"` if they took the Step 5 Edit-scope branch (legacy semantics for downstream compatibility); `"intent"` if they only took the Step 6 Edit-dimensions branch (the IDs remained auto-resolved).

## `scope.json` schema

```json
{
  "scope_slug": "file-upload-flow",
  "pipeline_origin": "wireframe",
  "scope_mode": "intent",
  "selected_at": "2026-05-24T14:32:00Z",
  "requirements_sha256": "<hex digest of requirements/requirements.md at selection time>",
  "intent_description": "wireframe the file-upload flow including validation and confirmation",
  "sources": {
    "functional": ["F-01", "F-02", "F-03"],
    "business_rules": ["BR-01", "BR-02"],
    "ui_needs": ["UI-03", "UI-04", "UI-05"],
    "goals": ["G-02"],
    "task_flows": ["§5.2 File Upload"],
    "data_shapes": ["§7 ImportFile"]
  },
  "personas_available": ["Importer", "Approver"],
  "dimension_override": null,
  "divergence_profile": null
}
```

When `dimension_override` is non-null:

```json
"dimension_override": {
  "dimensions": ["density-focus", "speed-accuracy"],
  "cardinality": 2
}
```

When `divergence_profile` is non-null (a Rule-P recommendation accepted at Step 4 — `dimension_override` stays `null` on this path):

```json
"divergence_profile": {
  "source": "recommended-confirmed",
  "evidence_strength": "strong",
  "dimensions": ["density-focus"],
  "cardinality": 2,
  "variant_bindings": [
    {
      "variant_index": 0,
      "persona": "Importer",
      "persona_goal_type": "high-throughput input",
      "pole": "power",
      "recommended_posture": "P1",
      "posture_label": "Efficiency-First / Power-Operator",
      "rationale": "Daily operator scans and acts on a high-volume table; dense layout suits throughput.",
      "evidence": [
        "§4 G-01 'Successfully import transaction files for downstream approval'",
        "§3 Importer wants 'fast review of file content'"
      ]
    },
    {
      "variant_index": 1,
      "persona": "Approver",
      "persona_goal_type": "read-only browsing + audit",
      "pole": "careful",
      "recommended_posture": "P4",
      "posture_label": "Error-Averse / High-Stakes",
      "rationale": "Auditor reviews each record deliberately under audit; spacious one-record focus suits judgement.",
      "evidence": [
        "§4 G-02 'Maintain control over which transactions are approved and which are rejected with reason'",
        "§3 Approver expertise 'applying judgement under audit'"
      ]
    }
  ],
  "realization_recommendation": {
    "high-throughput input": { "prefer": ["inline-drawer", "inline-expand", "modal"], "avoid": ["wizard-split"] },
    "read-only browsing + audit": { "prefer": ["standalone-screen", "wizard-split", "modal"], "avoid": ["inline-expand"] }
  }
}
```

**Schema notes:**

- `scope_slug` — the validated slug.
- `pipeline_origin` — the `pipeline_name` input (`"wireframe"`, `"prototype"`). Records who first authored this scope; not normative for downstream readers, who must accept any value.
- `scope_mode` — `"intent"` | `"structural"` | `"free-form"`. `"intent"` is the new default. `"structural"` indicates the consultant exercised the Edit-scope branch (Step 5). `"free-form"` is retained for backward-compatibility with any caller that surfaces a pure-prose flow; the present skill always emits `"intent"` or `"structural"`.
- `selected_at` — ISO-8601 UTC timestamp captured at Step 7.1.
- `requirements_sha256` — hex digest of the requirements doc at selection time. Lets downstream agents detect requirements drift between scope selection and consumption.
- `intent_description` — the verbatim consultant prose from Step 1. Always present (the new flow always captures intent).
- `sources` — six arrays, one per category. Each may be empty. Functional / business_rules / ui_needs / goals carry stable IDs; task_flows carries `"§N.M <flow name>"` strings; data_shapes carries `"§N <shape name>"` strings.
- `personas_available` — every §3 persona name in the requirements doc.
- `dimension_override` — `null` (default; architect uses `framework/assets/wireframes/domain-defaults.md`) OR an object `{ dimensions: ["<name>", "<name>", ...], cardinality: <int> }` where each name is a canonical dimension name from `tradeoff-dimensions-registry.md > Section 1` (e.g. `density-focus`, `speed-accuracy`). When non-null, the architect uses the consultant's chosen dimensions and cardinality instead of the domain defaults; polar positions are still derived by the architect from `tradeoff-dimensions-registry.md > Section 3`. Length of `dimensions` always equals `cardinality`.
- `divergence_profile` — **optional, sits alongside `dimension_override` (never overloads it).** `null` (default — emitted whenever `propose_divergence_axes == false`, i.e. today's flow and a future `/prototype`; or when the heuristics asset was unreadable) OR an object produced by Step 3.5 per `framework/assets/wireframes/divergence-heuristics.md`. Shape:
  ```
  {
    "source": "recommended-confirmed" | "static-default" | "manual-override-supersedes" | null,
    "evidence_strength": "strong" | "weak",
    "dimensions": ["<canonical dimension name>", ...],
    "cardinality": <int>,
    "variant_bindings": [
      { "variant_index": <int>, "persona": "<name>", "persona_goal_type": "<registry-§2 goal-type>",
        "pole": "careful" | "power" | "mixed",
        "recommended_posture": "P1".."P6" | null, "posture_label": "<posture label>" | null,
        "rationale": "<one line>", "evidence": ["§3 …", "§4 …"] }
    ],
    "realization_recommendation": { "<goal-type>": { "prefer": ["<realization>", ...], "avoid": ["<realization>", ...] } }
  }
  ```
  - `source` — `"recommended-confirmed"` (Rule P, consultant accepted the goal/persona-extrapolated recommendation at Step 4); `"static-default"` (Rule D uniform personas, or Rule W weak evidence — the architect's `domain-defaults.md` fallback applies); `"manual-override-supersedes"` (consultant entered Edit-dimensions at Step 6 — `dimension_override` is the field the architect's precedence consumes first, and this profile mirrors the override's `dimensions` / `cardinality` for a coherent record).
  - `evidence_strength` — `"strong"` for an anchored Rule-P recommendation or a well-evidenced uniform Rule D; `"weak"` for Rule W (could not cite ≥ 1 verbatim anchor per goal-bearing persona). A `"weak"` profile **always** has `source: "static-default"`.
  - `dimensions` — the separating axis (Rule P, typically a single dimension) or the static defaults `["density-focus", "speed-accuracy"]` (Rule D / W).
  - `cardinality` — `== variant_bindings.length`. Hard cap 3.
  - `variant_bindings[]` — one entry per variant. `persona` must be ∈ `personas_available`. `pole` is abstract (the architect maps it to concrete `-2..+2` positions per `tradeoff-dimensions-registry.md > Section 3`). Rule-P bindings carry ≥ 1 verbatim `evidence` anchor; Rule-D / Rule-W bindings mirror the `domain-defaults.md` `CAREFUL-DEFAULT` / `POWER-DENSE` split and may carry lighter rationale.
  - `recommended_posture` / `posture_label` — the UX posture (`P1`..`P6`) + its label, looked up per binding at Step 3.5's §4b from `framework/assets/wireframes/design-philosophies.md > Posture selection by persona goal-type` (keyed by `persona_goal_type` + traits + `pole`, pole-consistent with `pole`). The architect consumes it **verbatim** as a structural/realization + naming overlay (it does not change `dimension_positions`). Both are `null` only when `design-philosophies.md` was unreadable at Step 3.5 — the architect then uses today's position-derived structural choices. Posture is owned by `design-philosophies.md`, never defined here.
  - `realization_recommendation` — keyed by each bound persona's dominant goal-type per `divergence-heuristics.md > Section 4`; consumed by the architect when it intersects with each surface's `allowed_realizations`. May be omitted on Rule D / W (the architect then uses each surface's `default_realization`). `combined` is never recommended (fast-follow).
  - **Back-compat.** An absent or `null` `divergence_profile` behaves exactly as today — the architect's precedence falls straight through to `domain-defaults.md`. Existing `scope.json` files that predate this field need **zero** migration; downstream readers treat a missing key as `null`.

## Self-validation

- The scope-slug returned to the caller matches the validated slug from Step 2 or 5.1.
- `scope.json` exists at `<output_dir>/<scope_slug>/scope.json`, parses as JSON, conforms to the schema above, and was verify-artifact-write'd (`pass` returned).
- `scope_mode` matches the branch the consultant took (`"intent"` for direct accept or Edit-dimensions-only; `"structural"` for Edit-scope).
- `requirements_sha256` is the hex digest of `requirements_path` at the time of Step 3.1 (re-computable; downstream agents may sample-check on next invocation if drift detection is needed).
- `intent_description` is non-empty and is the verbatim consultant prose.
- `personas_available` is non-empty whenever the requirements doc has any `### <Name>` headers under §3.
- The intent prompt at Step 1 was surfaced exactly once (only re-surfaced on retry-budget invalid intents).
- The confirmation prompt at Step 4 was surfaced at least once and the consultant explicitly chose `Accept`, `Edit scope`, `Edit dimensions`, or `Cancel`.
- `dimension_override` is either `null` or an object whose `dimensions.length == cardinality` and whose `dimensions` are all in the active set `{speed-accuracy, power-simplicity, density-focus, control-automation, flexibility-consistency}` (canonical names per `tradeoff-dimensions-registry.md > Section 1`; `memorability-discoverability` is excluded — inactive).
- `divergence_profile` is `null` **iff** `propose_divergence_axes == false` (or the heuristics asset was unreadable at Step 3.5). When `propose_divergence_axes == true` and the heuristics asset was readable, `divergence_profile` is a non-null object conforming to the schema above.
- When `divergence_profile` is non-null: every `variant_bindings[i].persona` is ∈ `personas_available`; `cardinality == variant_bindings.length`; `dimensions` are all in the active canonical set (same set as `dimension_override`).
- When `divergence_profile` is non-null and `design-philosophies.md` was readable at Step 3.5: every `variant_bindings[i].recommended_posture` is a valid posture id (`P1`..`P6`) with a non-null `posture_label`, and is **pole-consistent** with `variant_bindings[i].pole` — `power` → `{P1, P3}`, `careful` → `{P2, P4, P5}`, `mixed` → `{P6}`. (When `design-philosophies.md` was unreadable, both `recommended_posture` and `posture_label` are `null` for every binding.)
- When `divergence_profile.source == "recommended-confirmed"` (Rule P): every `variant_bindings[i]` carries ≥ 1 verbatim `evidence` anchor, and no two bindings share the same `persona` (Rule P binds each variant to a *distinct* persona).
- When `divergence_profile.evidence_strength == "weak"`: `source == "static-default"` (weak evidence never produces a Rule-P persona-divergence).
- When the consultant entered Edit-dimensions (Step 6) on a run with `propose_divergence_axes == true`: `divergence_profile.source == "manual-override-supersedes"` and its `dimensions` / `cardinality` mirror the non-null `dimension_override`.

## Anti-Patterns

- Do not hardcode the output directory or pipeline name. `output_dir` and `pipeline_name` are required input parameters; the skill must work unchanged for `/wireframe` today and for `/prototype` later.
- Do not write any file other than `<output_dir>/<scope_slug>/scope.json`. The skill produces exactly one artefact per invocation.
- Do not skip `verify-artifact-write.md` on the scope.json write.
- Do not surface more than one intent prompt on the happy path. The whole point of the simplification is that direction = intent prose and the rest is auto-inferred.
- Do not skip the confirmation prompt at Step 4. Silent writes after auto-resolution would let resolution errors slip through.
- Do not infer candidate IDs without textual anchors in the requirements doc. Intent resolution is evidence-based; speculative IDs that aren't supported by a verbatim phrase or topic match are not added.
- Do not invoke any downstream skill or agent from within scope-selector. Selection and downstream invocation are separate concerns — the orchestrator owns invocation.
- Do not branch behaviour on the calling pipeline's name. Per-call differences are expressed through `output_dir` and `pipeline_name`; the skill's logic is identical for both.
- Do not include `memorability-discoverability` in the Step 6 dimension picker. It is inactive per the registry's upstream-pending block.
- Do not loosen the cardinality cap to 4+. The cap of 3 is enforced by the architect and mirrored here for user clarity.
- Do not embed `D1+`/`D3+`/etc. notation in any consultant-facing prompt text. Use the plain-English labels from `framework/assets/wireframes/position-vocabulary.md`.
- Do not auto-pick a slug like `main`, `app`, `tool`, `feature`, `wireframe`, or `prototype`. These are placeholder slugs that mask the intent's lack of specificity; prompt the consultant for a real slug in that case (Step 2's fallback).
- Do not silently apply `dimension_override` without the consultant explicitly entering the Edit-dimensions branch and confirming.
- Do not omit `intent_description` from `scope.json` on any code path. The intent is the load-bearing record of what the consultant asked for; downstream agents (notably `blueprint-architect.md`) may surface it back in their own prompts.
- Do not surface or persist a divergence recommendation when `propose_divergence_axes == false`. The flag keeps a future `/prototype` neutral — Step 3.5 is skipped and `divergence_profile` is `null`, preserving today's flow byte-for-byte.
- Do not branch the divergence behaviour on `pipeline_name`. The only switch is the `propose_divergence_axes` flag; the skill's logic is otherwise identical for every caller.
- Do not emit a Rule-P persona-divergence without verbatim goal/persona evidence. Every Rule-P `variant_bindings[i]` cites ≥ 1 verbatim `§3` / `§4` anchor; un-anchored or weak-evidence runs fall back to the static default (`source: "static-default"`, `evidence_strength: "weak"`).
- Do not bypass the Step-4 confirmation gate for the recommendation. The divergence profile is always surfaced to the consultant before it is persisted — Accept persists it, Edit dimensions supersedes it, Cancel discards it.
- Do not overload `dimension_override` with the divergence profile. `divergence_profile` is a separate, optional `scope.json` field; the two coexist (the architect's precedence reads `dimension_override` first, then `divergence_profile`, then `domain-defaults.md`).
- Do not define or invent dimension names in the recommendation. Separating axes are canonical registry §1 dimensions only; the heuristics asset (`divergence-heuristics.md`) governs which axis is chosen and defers concrete polar positions to the architect.
- Do not define or invent postures. `recommended_posture` / `posture_label` are looked up at Step 3.5 §4b from `framework/assets/wireframes/design-philosophies.md` (the canonical owner); the lookup must be pole-consistent with the binding's `pole`. A posture id outside `P1`..`P6`, or one whose pole contradicts the binding, is a mapping defect — never emit it.
