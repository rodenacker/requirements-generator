# scope-selector.md

**Purpose:** Capture a named scope of requirement IDs from `requirements/requirements.md` (functional `F-NN`, business rules `BR-NN`, UI feature needs `UI-NN`, goals `G-NN`, §3 personas, §5 task flows, §7 data shapes) and write a structured `scope.json` to a caller-supplied directory. Pipeline-neutral: the same skill drives `/wireframe` today and will drive a future `/prototype` without modification. Dual-mode: a **structural** branch lets the consultant multi-select known IDs / flows / sections and auto-writes (no accept gate); a **free-form** branch lets the consultant type a description, the skill resolves it to IDs via inline LLM reasoning over the requirements doc, and surfaces an accept/edit gate before writing.

The skill is **interactive**: it uses `AskUserQuestion` for scope-naming and mode selection, structural multi-pick prompts, and the free-form accept/edit gate. It does **one** write per invocation — the `scope.json` artefact — and verifies via `framework/skills/verify-artifact-write.md`.

## Inputs

- `output_dir` — repo-relative root directory under which `<output_dir>/<scope_slug>/scope.json` is written. **Required.** Wireframe pipeline passes `"blueprints/"`. A future `/prototype` pipeline passes `"blueprints/"` as well (the shared `blueprints/` directory is the cross-pipeline architectural contract — both pipelines can author against the same scope-slug without duplication; the consultant explicitly accepts overwrite at the calling orchestrator's prior-set gate). The skill writes to `<output_dir>/<scope_slug>/scope.json`; the calling orchestrator owns the prior-set overwrite gate (see `framework/orchestrators/wireframe-orch.md > Pipeline > step 0d`).
- `pipeline_name` — short string used in the surfaced prompts and in the `scope.json`'s `pipeline_origin` field. **Required.** Wireframe passes `"wireframe"`; future `/prototype` passes `"prototype"`. The skill never branches on this value beyond surfacing it; per-pipeline behaviour stays in the caller.
- `requirements_path` — optional repo-relative path to the requirements doc. Defaults to `"requirements/requirements.md"`. The skill reads this file in full to enumerate selectable IDs (structural branch) and to ground free-form resolution (free-form branch).

## Outputs

Exactly one of:

- **`selected`** — the in-memory return payload `{ scope_slug, mode, scope_path }` where `scope_path = <output_dir>/<scope_slug>/scope.json`. The orchestrator captures `scope_slug` into its in-memory variable. The skill has already written and verify-artifact-write'd `scope.json`.
- **`cancelled`** — the consultant chose to cancel at the scope-naming, mode-selection, structural-pick, or free-form-accept gate. The orchestrator exits cleanly without invoking any downstream agent. No file is written.

## Used by

- `framework/orchestrators/wireframe-orch.md` — step 0c, with `output_dir: "blueprints/"`, `pipeline_name: "wireframe"`, default `requirements_path`.
- A future `framework/orchestrators/prototype-orch.md` — analogous step, with `output_dir: "blueprints/"`, `pipeline_name: "prototype"`. **Zero skill changes required** when that pipeline ships.

## Procedure

### Step 1 — Capture scope-slug

Surface a single `AskUserQuestion`:

- Question: *"Name this scope (a short kebab-case slug — e.g. `file-upload-flow`, `approval-flow`, `transaction-table-view`). This is the directory name your `{{pipeline_name}}` set will be written under."*
- Header: `Scope name`
- `multiSelect: false`
- Options:
    1. `Enter slug` — description: `"Type the slug in the response."`
    2. `Cancel — exit without writing scope`

On `Cancel`, return `cancelled`.

On `Enter slug`, the consultant's reply is the next conversation turn. Normalise: trim, lowercase, replace internal whitespace with `-`, collapse repeated `-`. Validate against `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`. On match, capture as `scope_slug` and advance to Step 2. On mismatch, print *"Invalid slug. Use lowercase letters, digits, and `-` only (starts and ends with a letter or digit). Try again, or type `cancel` to exit."* and re-prompt (parse on the next turn). Retry budget: **2** re-prompts; on the third invalid, print *"Too many invalid slugs. Cancelling."* and return `cancelled`.

### Step 2 — Mode selection

Surface a single `AskUserQuestion`:

- Question: *"How would you like to define the scope for `{{scope_slug}}`?"*
- Header: `Scope mode`
- `multiSelect: false`
- Options:
    1. `Structural — multi-select known IDs / flows / sections (Recommended)`
    2. `Free-form — describe the scope in prose; I'll resolve it to IDs and ask you to confirm`
    3. `Cancel — exit without writing scope`

On `Cancel`, return `cancelled`.

On `Structural`, advance to Step 3.
On `Free-form`, advance to Step 4.

### Step 3 — Structural branch

3.1 **Read the requirements doc.** `Read` the file at `requirements_path`. The orchestrator's prerequisite gate has already guaranteed it exists and is non-empty. Compute and remember its `sha256` for the artefact's `requirements_sha256` field.

3.2 **Enumerate selectable IDs and sections.** Walk the doc and extract:

- Every `F-NN`, `BR-NN`, `UI-NN`, `G-NN` ID that appears as a header anchor or as the row label in §1.7 / §6 tables.
- Every §5 task flow name (each `### Flow: <name>` header).
- Every §6.4.x UI feature row (each numbered table row under §6.4).
- Every §7 data shape name (each `### <Name>` header under §7).
- Every §3 persona name (each `### <Name>` header under §3 — used to populate `personas_available`, not as a selectable scope element).

3.3 **Surface a sequence of multi-select prompts**, one per category, in this order: Functional (`F-NN`), Business rules (`BR-NN`), UI feature needs (`UI-NN`), Goals (`G-NN`), Task flows (§5), Data shapes (§7). For each category, use `AskUserQuestion` with `multiSelect: true`. Question text: *"Which `{{category}}` items are in scope for `{{scope_slug}}`?"*. Header: `Scope ({{category}})`. Options: each enumerated ID/name (label = the ID/name verbatim; description = its one-line summary from the doc, truncated to 80 chars). Add one final option per prompt: *`None / Skip this category`*. The consultant may also choose `Cancel — exit without writing scope` at any prompt (always present as the last option); on `Cancel` return `cancelled`.

If a category has zero enumerated items, skip its prompt silently and surface a note in the next prompt's question text: *"(No `{{empty_category}}` rows found in the requirements doc — skipping.)"*.

3.4 **Compile the selection into a `sources` block** with the shape documented in **`scope.json` schema** below. Populate `personas_available` with every §3 persona name detected at step 3.2.

3.5 Advance to Step 5 with `mode: "structural"` and **no accept-gate** (per the plan, structural is auto-write).

### Step 4 — Free-form branch

4.1 **Capture the free-form description.** Surface a single `AskUserQuestion`:

- Question: *"Describe the scope for `{{scope_slug}}` in prose. Example: 'wireframe the file-upload flow including validation and confirmation'."*
- Header: `Scope description`
- `multiSelect: false`
- Options:
    1. `Enter description`
    2. `Cancel — exit without writing scope`

On `Cancel`, return `cancelled`. On `Enter description`, the consultant's next conversation turn is the prose. Capture as `freeform_description`.

4.2 **Read the requirements doc.** `Read` the file at `requirements_path` (full). Compute and remember its `sha256`.

4.3 **Resolve the description to candidate IDs.** Inline reasoning, no separate skill (per the plan's "Dropped from previous plan" note that `resolve-freeform-scope.md` is folded into this skill). For each candidate, capture: `{ id_or_name, category, requirement_text_first_line }`. Categories: `functional`, `business_rules`, `ui_needs`, `goals`, `task_flows`, `data_shapes`. The resolution must be evidence-based — every candidate must be justified by a verbatim phrase or topic match in the requirements doc; speculative inference without textual anchor is not added. Truncate `requirement_text_first_line` to 120 chars.

4.4 **Surface the resolution for accept/edit.** Surface a single `AskUserQuestion`:

- Question text: a multi-line string prefaced by *"Resolved `{{freeform_description}}` to the following requirement IDs (each shown with its first-line text). Accept, edit, or cancel?"*, followed by a printed list of every candidate in the form `- {{id_or_name}} ({{category}}) — {{requirement_text_first_line}}`.
- Header: `Resolution`
- `multiSelect: false`
- Options:
    1. `Accept — write scope.json with these IDs`
    2. `Edit — remove or add IDs interactively`
    3. `Cancel — exit without writing scope`

On `Cancel`, return `cancelled`.

On `Accept`, populate `personas_available` with every §3 persona name detected from a full re-walk of the doc's §3 (`### <Name>` headers under §3). Advance to Step 5 with `mode: "free-form"`.

On `Edit`, fall through to step 4.5 (interactive remove + add). After every Edit cycle, re-surface the step 4.4 accept/edit/cancel prompt with the updated candidate list. Loop until the consultant accepts or cancels.

4.5 **Interactive remove + add.**
- **Remove**: surface a single `AskUserQuestion` with `multiSelect: true`. Options: each current candidate's `{{id_or_name}} ({{category}})`. Header: `Remove from scope`. The consultant ticks the ones to drop; submit removes them.
- **Add**: surface a single `AskUserQuestion`:
    - Question: *"Add additional IDs (comma-separated, e.g. `F-15, BR-04, §5.3`). Or `Skip`."*
    - Header: `Add to scope`
    - Options:
        1. `Enter IDs`
        2. `Skip — no additions`
    - On `Enter IDs`, parse the consultant's next turn as a comma-separated list. For each entry, look it up in the requirements doc (re-walk to validate the ID exists). Invalid entries are reported back via plain-text print *"Skipping unknown ID `{{entry}}` — not found in `{{requirements_path}}`."* and dropped silently.
- Re-surface step 4.4 with the updated list.

### Step 5 — Write `scope.json`

5.1 **Compose the artefact** per the schema below.

5.2 **Compute the sha256** of the rendered JSON string.

5.3 **Ensure the parent directory exists.** `Bash mkdir -p <output_dir>/<scope_slug>` (works on POSIX bash; on PowerShell-only environments, the calling orchestrator's harness handles directory creation transparently via the Write tool itself — verify by retrying once via `mkdir` if the first Write fails on path-missing).

5.4 **Write the artefact.** `Write <output_dir>/<scope_slug>/scope.json` with the rendered JSON.

5.5 **Verify the write.** Call `framework/skills/verify-artifact-write.md` with `path = <output_dir>/<scope_slug>/scope.json`, `expected_sha256 = <rendered sha256>`, `expected_min_bytes = 64` (a minimum-shape scope.json — `scope_slug` + `pipeline_origin` + `mode` + `selected_at` + a one-empty-category `sources` block — is comfortably above 64 bytes). On `pass`, return `selected`. On `RF-04 trigger`, propagate the hard halt per `framework/shared/refusal-registry.md > RF-04` (the calling orchestrator surfaces it).

### Step 6 — Return

Return `selected` with the in-memory payload `{ scope_slug, mode, scope_path }`.

## `scope.json` schema

```json
{
  "scope_slug": "file-upload-flow",
  "pipeline_origin": "wireframe",
  "scope_mode": "structural",
  "selected_at": "2026-05-23T14:32:00Z",
  "requirements_sha256": "<hex digest of requirements/requirements.md at selection time>",
  "freeform_description": null,
  "sources": {
    "functional": ["F-01", "F-02", "F-03"],
    "business_rules": ["BR-01", "BR-02"],
    "ui_needs": ["UI-03", "UI-04", "UI-05"],
    "goals": ["G-02"],
    "task_flows": ["§5.2 File Upload"],
    "data_shapes": ["§7 ImportFile"]
  },
  "personas_available": ["Importer", "Approver"]
}
```

**Schema notes:**

- `scope_slug` — the validated slug from step 1.
- `pipeline_origin` — the `pipeline_name` input (e.g. `"wireframe"`, `"prototype"`). Records who first authored this scope; not normative for downstream readers, who must accept any value.
- `scope_mode` — `"structural"` or `"free-form"`. Mirrors the `mode` field returned to the caller.
- `selected_at` — ISO-8601 UTC timestamp captured at step 5.1 (just before write).
- `requirements_sha256` — hex digest of the requirements doc at selection time. Lets downstream agents detect requirements drift between scope selection and their own consumption.
- `freeform_description` — the verbatim consultant prose (free-form branch) or `null` (structural branch).
- `sources` — six arrays, one per category. Each may be empty (the consultant skipped the category at step 3.3, or no candidates resolved at step 4.3). The shape of values: `functional` / `business_rules` / `ui_needs` / `goals` carry stable IDs; `task_flows` carries `"§N.M <flow name>"` strings; `data_shapes` carries `"§N <shape name>"` strings.
- `personas_available` — every §3 persona name in the requirements doc. Not selectable scope itself; downstream agents (notably `blueprint-architect.md`) read this to constrain variant persona-binding.

## Self-validation

- The scope-slug returned to the caller matches the validated slug at step 1.
- `scope.json` exists at `<output_dir>/<scope_slug>/scope.json`, parses as JSON, conforms to the schema above, and was verify-artifact-write'd (`pass` returned).
- `scope_mode` matches the branch the consultant took (`"structural"` or `"free-form"`).
- `requirements_sha256` is the hex digest of the bytes at `requirements_path` at the time of step 3.1 / 4.2 (re-computable; the calling agent may sample-check on next invocation if drift detection is needed).
- `personas_available` is non-empty whenever the requirements doc has any `### <Name>` headers under §3. (Empty `personas_available` on a doc with §3 personas is a bug — the persona walk missed entries.)
- The structural branch had **no** accept-gate between selection and write (step 3.5 transitions directly to step 5).
- The free-form branch had at least one accept-gate (step 4.4); the consultant either accepted, edited then accepted, or cancelled.
- The retry budget at step 1 was respected — at most 2 re-prompts for invalid slugs.

## Anti-Patterns

- Do not hardcode the output directory or pipeline name. `output_dir` and `pipeline_name` are required input parameters; the skill must work unchanged for `/wireframe` today and for `/prototype` later.
- Do not write any file other than `<output_dir>/<scope_slug>/scope.json`. The skill produces exactly one artefact per invocation.
- Do not skip `verify-artifact-write.md` on the scope.json write. Truncation hits the manifest as readily as any other artefact.
- Do not surface a structural-branch accept gate. Per the plan's Design Decisions row 1, structural is auto-write; an accept gate there would re-introduce the friction the plan deliberately removed.
- Do not surface a free-form-branch silent write. Per the plan, free-form always presents the resolution for accept/edit before writing; silent free-form writes would let resolution errors slip through.
- Do not infer candidate IDs without textual anchors in the requirements doc. Free-form resolution is evidence-based; speculative IDs that aren't supported by a verbatim phrase or topic match are not added.
- Do not loop the slug-validation re-prompt indefinitely. Retry budget: 2 re-prompts; third invalid returns `cancelled` with a clear *"Too many invalid slugs. Cancelling."* line.
- Do not invoke any downstream skill or agent from within scope-selector. Selection and downstream invocation are separate concerns — the orchestrator owns invocation.
- Do not branch behaviour on the calling pipeline's name. Per-call differences are expressed through `output_dir` and `pipeline_name`; the skill's logic is identical for both.
- Do not author `scope.json` rows for IDs that don't exist in the requirements doc. Every value in `sources.functional`, `sources.business_rules`, `sources.ui_needs`, `sources.goals` must have been enumerated at step 3.2 or validated at step 4.5. Unknown IDs are dropped silently with a plain-text notice in the free-form branch; in the structural branch they can't appear because the selection UI only offers enumerated values.
- Do not omit `personas_available` even when no variant work follows. The field is part of the canonical schema; downstream agents that rely on it (notably the blueprint-architect's persona-binding step) will halt on a missing key.
