# scope-selector.md

**Purpose:** Capture a named scope of requirement IDs from `requirements/requirements.md` (functional `F-NN`, business rules `BR-NN`, UI feature needs `UI-NN`, goals `G-NN`, §3 personas, §5 task flows, §7 data shapes) and write a structured `scope.json` to a caller-supplied directory. Pipeline-neutral: the same skill drives `/wireframe` today and will drive a future `/prototype` without modification.

**Intent-first by default.** The happy path asks the consultant one direction prompt (free-form intent) and one confirmation. Everything else — slug derivation, requirement-ID resolution, persona enumeration, default dimension profile — is auto-inferred by the LLM from the intent prose + `requirements/requirements.md` + `framework/assets/wireframes/domain-defaults.md`. The consultant can override at the confirmation gate via `Edit scope` (per-ID structural pickers, the legacy structural-mode logic preserved as opt-in) or `Edit dimensions` (override the default diverging dimensions and cardinality before the architect runs).

The skill is **interactive**: it uses `AskUserQuestion` for the intent prompt, the confirmation gate, and (when entered) the Edit branches. It does **one** write per invocation — the `scope.json` artefact — and verifies via `framework/skills/verify-artifact-write.md`.

## Inputs

- `output_dir` — repo-relative root directory under which `<output_dir>/<scope_slug>/scope.json` is written. **Required.** Wireframe pipeline passes `"blueprints/"`. A future `/prototype` pipeline passes `"blueprints/"` as well (the shared `blueprints/` directory is the cross-pipeline architectural contract — both pipelines can author against the same scope-slug without duplication; the consultant explicitly accepts overwrite at the calling orchestrator's prior-set gate). The skill writes to `<output_dir>/<scope_slug>/scope.json`; the calling orchestrator owns the prior-set overwrite gate (see `framework/orchestrators/wireframe-orch.md > Pipeline > step 0d`).
- `pipeline_name` — short string used in the surfaced prompts and in the `scope.json`'s `pipeline_origin` field. **Required.** Wireframe passes `"wireframe"`; future `/prototype` passes `"prototype"`. The skill never branches on this value beyond surfacing it; per-pipeline behaviour stays in the caller.
- `requirements_path` — optional repo-relative path to the requirements doc. Defaults to `"requirements/requirements.md"`. The skill reads this file in full to ground intent resolution and to enumerate personas.
- `domain_defaults_path` — optional repo-relative path to the domain-defaults asset. Defaults to `"framework/assets/wireframes/domain-defaults.md"`. Read at confirmation time to surface the default dimension profile so the consultant sees what the architect will do.

## Outputs

Exactly one of:

- **`selected`** — the in-memory return payload `{ scope_slug, mode, scope_path }` where `scope_path = <output_dir>/<scope_slug>/scope.json`. The orchestrator captures `scope_slug` into its in-memory variable. The skill has already written and verify-artifact-write'd `scope.json`.
- **`cancelled`** — the consultant chose to cancel at any prompt. The orchestrator exits cleanly without invoking any downstream agent. No file is written.

## Used by

- `framework/orchestrators/wireframe-orch.md` — step 0c, with `output_dir: "blueprints/"`, `pipeline_name: "wireframe"`, default `requirements_path`.
- A future `framework/orchestrators/prototype-orch.md` — analogous step, with `output_dir: "blueprints/"`, `pipeline_name: "prototype"`. **Zero skill changes required** when that pipeline ships.

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

### Step 4 — Confirmation gate

Surface a single `AskUserQuestion`:

- Question text: a multi-line string prefaced by *"Resolved your intent `{{intent_description}}` to scope `{{scope_slug}}`. Review and accept, or edit."*. Below the preface, render:
    - **Slug:** `{{scope_slug}}`
    - **Requirement IDs** (counts per category): e.g. *"3 functional, 2 business rules, 4 UI needs, 1 goal, 1 task flow, 1 data shape"* — render `0` categories as omitted.
    - **Personas in scope:** comma-separated `personas_available`.
    - **Default trade-off dimensions** (the architect will diverge variants on these unless overridden): *"density-focus · speed-accuracy"* (the two defaults per `domain-defaults.md > Section 1`). Append: *"Default variants: 2 (`CAREFUL-DEFAULT`, `POWER-DENSE`). The architect picks polar positions automatically — see `framework/assets/wireframes/domain-defaults.md > Section 3` for the exact positions."*
- Header: `Scope`
- `multiSelect: false`
- Options:
    1. `Accept — write scope.json (Recommended)`
    2. `Edit scope — change slug, add or remove requirement IDs`
    3. `Edit dimensions — override the default trade-off dimensions or cardinality`
    4. `Cancel — exit without writing scope`

Branch:

- **Accept** — advance to Step 7 with `scope_mode = "intent"`, `dimension_override = null`.
- **Edit scope** — advance to Step 5.
- **Edit dimensions** — advance to Step 6.
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

- Every `F-NN`, `BR-NN`, `UI-NN`, `G-NN` ID from header anchors or §1.7 / §6 table rows.
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

6.3 Compile `dimension_override = { dimensions: ["density-focus", "speed-accuracy", ...], cardinality: <int> }` (dimension names in selection order; matches the key format the architect uses in `variants.json > dimension_positions`). Return to Step 4 (re-surface the confirmation prompt) so the consultant sees the updated dimension profile and can accept or further edit.

### Step 7 — Write `scope.json`

7.1 **Compose the artefact** per the schema below.

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
  "dimension_override": null
}
```

When `dimension_override` is non-null:

```json
"dimension_override": {
  "dimensions": ["density-focus", "speed-accuracy"],
  "cardinality": 2
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
