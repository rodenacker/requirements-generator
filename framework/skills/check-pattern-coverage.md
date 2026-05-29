# check-pattern-coverage.md

**Purpose:** Verify, per blueprint **logical surface** (`LS-NN`), that **at least one** pattern in `framework/assets/pattern-catalogue/` can fill that surface's primary slot (and, where the blueprint identifies them, the secondary slots). Produce a per-surface viability tier (`ok | borderline | gap`) so the calling agent can either proceed cleanly (`ok` everywhere), surface a gate (any `borderline` or `gap`), or halt (a `gap` the consultant declines to accept).

The blueprint inventory rows are now keyed `LS-NN` (logical surfaces — decomposition-agnostic units of capability, per `framework/assets/templates/template-blueprint.md`), not `S-NN` physical screens. The skill's **return shape is unchanged** — it still returns `per_screen` with `primary_slot.candidate_patterns` (these are stable contract keys consumed downstream); each `per_screen[i].screen_id` value is now a logical surface ID `LS-NN`. The skill matches catalogue patterns against each surface's *logical* intent; realization (how many physical screens a surface becomes) is a variant-level decision the skill does not see.

Pipeline-neutral: invoked today by `framework/agents/blueprint-architect.md` during its design-brief preflight; reusable by a future `/prototype` agent that authors blueprints at higher fidelity. The skill never invents a pattern; it only matches existing catalogue entries against a surface's intent.

The skill is **read-only**. It reads the blueprint, the pattern-catalogue index, and selectively-loaded catalogue entries. It writes nothing and surfaces no consultant prompts — its return value drives the caller's decisions.

## Inputs

- `blueprint_path` — repo-relative path to `blueprints/<scope_slug>/blueprint.md`. **Required.** The blueprint must be in the format produced by `framework/assets/templates/template-blueprint.md` (logical surface inventory + logical flow + scope→surface trace; no pattern bindings, no chosen realization).
- `catalogue_index_path` — optional, defaults to `"framework/assets/pattern-catalogue/_index.md"`. Reusable for future drift if the catalogue relocates.
- `mode` — optional, one of `"preflight"` (default) or `"audit"`. `preflight` is the architect's design-brief call (cheap; reads only the index + surface primary slots). `audit` is a deeper retroactive check that also matches secondary-slot requirements (used by future debugging tools, not yet wired into any orchestrator).

## Outputs

A single structured return value:

```yaml
verdict: ok | borderline | gap
per_screen:                  # key unchanged; each screen_id value is now a logical surface LS-NN
  - screen_id: LS-01
    intent: "Login"
    primary_slot:
      tier: ok | borderline | gap
      candidate_patterns: ["auth/login-form", "layouts/centered-form"]
      reason: "Direct match — auth/login-form covers required-slots."
    secondary_slots: [...]   # only populated when mode == "audit"
ai_suggested_gaps:
  - screen_id: LS-03
    requirement_id: "F-09"
    description: "Approval action with three named outcomes (approve / reject / escalate) — closest catalogue match is forms/single-form, but it does not natively model three-way disposition."
notes: "<one or two lines for the caller's gate prompt>"
```

(The `per_screen` / `screen_id` / `primary_slot` keys are the stable downstream contract — the architect reads `per_screen[*].primary_slot.candidate_patterns` into `pattern_candidates[<LS>]`. Only the *values* of `screen_id` changed from `S-NN` to `LS-NN`.)

`verdict` is the worst tier across all surfaces. Tier ordering (worst-first): `gap > borderline > ok`.

Possible final verdicts:

- **`ok`** — every surface has at least one direct-match catalogue pattern for its primary slot; no AI-SUGGESTED gaps. The caller (blueprint-architect) proceeds without a gate.
- **`borderline`** — every surface has at least one candidate pattern, but at least one is a soft match (the pattern's `when-to-use` covers the surface's intent only partially; the pattern's `when-not-to-use` is not explicitly violated). The caller surfaces the per-surface reasons to the consultant via its conditional gate **only if the caller's own self-validation has otherwise flagged the surface** (the architect's design-brief gate doesn't fire on borderline alone — it fires on `gap` or on its own bijection / conflict checks).
- **`gap`** — at least one surface has zero direct-match catalogue patterns and no acceptable soft match. The caller surfaces the gap via its conditional gate; the consultant either accepts an `[AI-SUGGESTED]` stub, narrows scope, or cancels.

## Used by

- `framework/agents/blueprint-architect.md` — preflight call during its design-brief step (run after the surface inventory is settled and before `variants.json` is composed). Caller passes `mode: "preflight"`.
- A future `framework/agents/prototype-architect.md` or debug tool — `mode: "audit"` invocations. **Zero skill changes required** when those land.

## Procedure

### Step 1 — Read the blueprint

`Read` the file at `blueprint_path`. Parse the surface inventory section (every `LS-NN` row, each row carrying `intent`, `sources`, optional `secondary_intent`). The row also carries `Allowed realizations` / `Default realization` / `Host surface` columns — the skill ignores them; realization is a variant-level decision the coverage check does not consider. Extract into an in-memory list, recording each row's `LS-NN` ID as its `screen_id` (the unchanged return key). If the blueprint lacks a surface inventory section (zero `LS-NN` rows), return `verdict: gap` with a single `notes: "Blueprint has zero surfaces in its inventory — pattern coverage cannot be evaluated."` This is a structural error in the blueprint, not a pattern-catalogue gap; the caller halts and the architect re-emits the blueprint.

### Step 2 — Read the pattern-catalogue index

`Read` the file at `catalogue_index_path`. Parse into an in-memory list of `{ id, category, tier, purpose, file_path }` rows. The index is the source of truth for what patterns exist; never enumerate filesystem files instead. `tier` is one of `T1`, `T2`, `T3`.

### Step 3 — Per-surface primary-slot matching

For each surface in the blueprint inventory, derive a **surface intent vector** from the blueprint's `intent` field plus its `sources` list (the IDs in `sources` carry one-line summaries from §1.7 / §6 of `requirements.md` that the architect propagates into the blueprint — the skill reads them from the blueprint, not the requirements doc).

Compute a category-level shortlist using these heuristics (deterministic, not LLM-judgement at this layer):

- `intent` contains "login" / "sign-in" / "authenticate" → `auth/`, `layouts/centered-form`.
- `intent` contains "list" / "table" / "browse" / "filter" → `collections/`, `forms/search-and-filter`.
- `intent` contains "edit" / "create" / "configure" / "submit" → `forms/`.
- `intent` contains "confirm" / "approve" / "review" → `surfaces/modal-confirmation`, `forms/single-form` (with confirmation modal), `feedback/confirmation-receipt`.
- `intent` contains "dashboard" / "overview" / "summary" → `collections/dashboard`, `collections/kpi-tile`.
- `intent` contains "detail" / "view" / "drill" → `collections/detail-page`, `collections/detail-panel`, `surfaces/drawer-detail`.
- `intent` contains "error" / "404" / "no-permission" → `layouts/error-shell`.
- `intent` contains "upload" / "import" → `forms/file-upload` (T3 stub — likely borderline), `forms/single-form` with file slot, `forms/multi-step-wizard`.
- Any surface whose intent matches none of the above falls back to a full-catalogue scan in step 3.5.

For each shortlisted pattern category, read the pattern entries (only those candidates' files, not the entire catalogue) and evaluate against the surface:

3.1 **Direct match** — the pattern's `purpose` covers the surface's `intent`; the pattern's `when-to-use` block lists at least one condition the surface satisfies; the pattern's `when-not-to-use` does not foreclose. Tier: `ok`.

3.2 **Soft match** — the pattern's `purpose` is adjacent (related noun/verb category) but neither directly covers nor explicitly forecloses the intent. Tier: `borderline`.

3.3 **Foreclosed** — the pattern's `when-not-to-use` explicitly rules out the surface's intent. Drop the candidate.

3.4 **Compile candidates** for the surface: keep all direct-match patterns and (if no direct-match exists) all soft-match patterns.

3.5 **Fallback full-catalogue scan** — if the shortlist yielded zero candidates after step 3.4, read every T1 + T2 catalogue entry (skip T3 stubs — they're not authored bodies) and re-run 3.1–3.3. If still zero candidates, the surface's `primary_slot.tier` is `gap`. Append a row to `ai_suggested_gaps` with `screen_id` (the `LS-NN`), the surface's first `sources` ID, and a one-line `description` noting the closest near-miss with the reason it doesn't fit.

### Step 4 — Per-surface secondary-slot matching (audit mode only)

Skipped when `mode == "preflight"`.

When `mode == "audit"`, walk each surface's `secondary_intent` (e.g. "with inline validation", "with cross-record bulk action") and repeat steps 3.1–3.5 against shortlisted secondary-slot patterns (e.g. `feedback/inline-validation`, `forms/bulk-edit`). Append to the surface's `secondary_slots` list with the same `tier`, `candidate_patterns`, `reason` shape.

### Step 5 — Aggregate verdict

`verdict` is the worst tier across all surfaces (per the ordering `gap > borderline > ok`). Compose `notes` as a one-or-two-line summary the caller can quote in its conditional gate prompt. Examples:

- `verdict: ok` — *"5 of 5 surfaces have a direct-match catalogue pattern for the primary slot."*
- `verdict: borderline` — *"4 of 5 surfaces direct-match; LS-04 (`Confirmation`) is a soft match against `feedback/confirmation-receipt`."*
- `verdict: gap` — *"LS-03 (`Three-way disposition`) has no catalogue pattern that natively models three named outcomes; closest near-miss is `forms/single-form`. Consultant must accept an [AI-SUGGESTED] stub, narrow scope, or cancel."*

### Step 6 — Return

Return the structured payload from the **Outputs** section above. The caller (blueprint-architect) decides how to act per its own conditional-gate predicates.

## Self-validation

- Every `LS-NN` row in the blueprint's inventory has a corresponding entry in `per_screen` (1:1 by `screen_id`, whose value is the `LS-NN`).
- Every `candidate_patterns` entry is a valid catalogue ID present in the index at `catalogue_index_path`.
- No candidate is a T3 stub (T3 entries are stubs only and have no body to compose against); if a T3 was the closest near-miss, it is recorded only in `ai_suggested_gaps.description`, not in `candidate_patterns`.
- `verdict` is exactly the worst tier across all surfaces — no smoothing, no rounding.
- `ai_suggested_gaps` is empty when `verdict == "ok"`; non-empty whenever `verdict == "gap"`.
- The skill performed zero writes.

## Anti-Patterns

- Do not propose a pattern not in the catalogue index. The skill's job is to match existing patterns to surfaces, not to invent new ones. AI-SUGGESTED gaps go in `ai_suggested_gaps`, not into `candidate_patterns`.
- Do not skip the `when-not-to-use` block when evaluating a candidate. A pattern whose purpose is adjacent but whose `when-not-to-use` explicitly rules out the surface's intent is **foreclosed**, not `borderline`.
- Do not consult `requirements/requirements.md` directly. The blueprint is the contract; the architect has already propagated the relevant requirement IDs and their summaries into the blueprint. Reading the requirements doc from this skill would couple it to a single pipeline's source layout and break cross-pipeline reuse.
- Do not surface an `AskUserQuestion`. The skill returns a structured verdict; the caller decides whether to gate.
- Do not write any file. The skill is read-only; even a debug log would couple it to a single caller's filesystem layout.
- Do not raise the intent heuristics' specificity opportunistically when one blueprint pushes back. The heuristics are project-wide tuning; calibrate them across runs, not for one surface that happened to confuse the matcher.
- Do not load every catalogue entry on every call. The shortlist in step 3 selectively reads only the candidates' files; the fallback full-catalogue scan is rare (and skips T3 stubs). Loading 50 files per call wastes context for no benefit on the median path.
- Do not silently re-classify a `gap` to `borderline` to spare the caller a gate. Pattern gaps are signal — the architect's gate is the consultant's chance to decide before N variants are rendered against an impossible blueprint.
