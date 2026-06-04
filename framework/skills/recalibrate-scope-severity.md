# recalibrate-scope-severity.md

**Purpose:** Make an ADVERSARIAL review **purpose-aware**. Given a merged finding set, classify each
finding by its **finding-scope class** (per `framework/shared/prototype-scope.md > Finding-scope
classification`) and **recalibrate the rating of `backend-only` findings** so that a concern outside
the system's frontend purpose can be *raised* but cannot *block* a frontend deliverable. This is
**raise-and-recalibrate, never drop** — every finding survives; only the rating of out-of-scope
findings is bounded, and every change is logged. Invoked in the foreground by the parent reviewer at
its consolidation step (requirements-adversarial Step 3s; inputs-adversarial between Step 4b and 4c).

This skill is shared by **two** callers — `framework/agents/reviews/adversarial-reviewer.md`
(`/review-requirement`) and `framework/agents/reviews-inputs/adversarial-reviewer.md`
(`/review-inputs`). It is vocabulary-parameterised so the same procedure serves both.

## Inputs

- `finding_list` — the merged, ID-assigned in-memory findings. Each finding carries at least
  `{id, dimension, severity, disposition, location, evidence, problem, recommendation}`. (The
  requirements caller has 8 dimensions; the inputs caller has 6 — the skill is dimension-count-agnostic.)
- `target` — exactly one of `"prototype"`, `"application"`, or `null`. Governs the `backend-only`
  severity cap (see *Recalibration rules*). The requirements caller detects this from the document
  (PI-01..PI-08 block present → `"prototype"`; absent → `"application"`). The inputs caller has **no
  target signal** and always passes `null`.
- `severity_vocab` — the caller's severity tiers, **ordered highest → lowest**. Both adversarial
  callers pass `["Blocker", "Major", "Minor"]`.
- `disposition_vocab` — the caller's disposition set + which value is the blocking one. Both callers
  pass `{ values: ["Patch", "Defer", "Reject"], blocking: "Reject", safe_non_blocking: "Defer" }`.
- (reference) `framework/shared/prototype-scope.md > Finding-scope classification` — the canonical
  class definitions. The one-line glosses below are sufficient to execute at runtime; Read the full
  section only when a borderline finding needs the precise bullet wording.

## Outputs

- The same `finding_list`, with each finding annotated with a new metadata field
  `scope_class ∈ {"fe-relevant", "fe-facing-contract", "backend-only"}` and — where the rules below
  fire — an adjusted `severity` and/or `disposition`. `scope_class` is **metadata, not a required
  schema field** (it does not count toward the caller's "every finding has all N schema fields" gate,
  exactly like `cluster_id`).
- `recalibration_log` — a list of entries, **one per finding whose rating changed**:
  `{finding_id, scope_class, target, original_severity, adjusted_severity, original_disposition,
  adjusted_disposition, foreclosing_authority}`. `fe-relevant` findings and any finding left unchanged
  produce **no** log entry (their `scope_class` is still set on the finding for rendering).
- **The finding count is invariant.** No finding is added, removed, merged, or renumbered. No
  finding's `evidence`, `problem`, or `recommendation` text is edited. (For the inputs caller this
  guarantees the five sanctioned Recommendation forms are left untouched — the skill changes the
  *rating*, never the *handling action*.)

## Class glosses (canonical definitions in `prototype-scope.md`)

- **`fe-relevant`** — subject **and** corrective action live in the UI layer (screens, navigation,
  form fields, validation **display**, data **display**, status indicators, loading/empty/error
  **states**, role-gated **screen states**, the **UI surface** of a backend event). No recalibration.
- **`fe-facing-contract`** — a backend **contract the FE consumes** (§6.10 shape / enum / failure
  mode) or **POPIA / PII handling** (surfaces as consent banners, on-screen masking, regional
  variants, retention notices). Severity preserved; disposition bounded only if it does not block a
  frontend consumer.
- **`backend-only`** — subject **and** corrective action live entirely in backend / infra /
  server-side implementation (endpoint logic, persistence / DB schema, server-side computation,
  queues, DevOps / CI-CD, monitoring / alerting / backups / DR, caching / query-optimisation, at-rest
  encryption, ETL / migration, SDK / webhook internals). No UI surface. **This is the recalibration
  target.**

## Classification rule (applied with judgment, per finding)

Key on **what would satisfy the finding's `recommendation`**, not on how "backend" the topic sounds:

1. If the fix lands in the UI → **`fe-relevant`**.
2. Else if the fix is "define the contract / shape / enum / failure-mode / compliance surface the UI
   renders against" → **`fe-facing-contract`**.
3. Else if the fix can **exclusively** be satisfied by backend / infra / server-side work (it matches
   the *Not Prototypable* list and has no UI surface) → **`backend-only`**.
4. **Genuinely dual** findings (a UI surface in scope + a backend mechanism out of scope — e.g. a
   network-failure finding whose retry **banner** is FE but whose retry **mechanism** is backend) →
   **`fe-facing-contract`**, never `backend-only`.

**Bias toward not suppressing.** When undecided between `fe-facing-contract` and `backend-only`,
choose `fe-facing-contract`. The cost of leaving severity too high (a visible note) is far smaller
than the cost of burying a frontend-relevant defect.

**"Blocks a frontend consumer"** (used in the rules below) means a downstream frontend pipeline
literally cannot produce its artefact without the missing fact. For the requirements caller the
frontend consumers are `/design-system`, `/analyse-requirement`, `/wireframe`, `/prototype` (e.g. an
absent role-permission section blocks role-gated screen states; a missing data-model anchor blocks the
`/wireframe` `data-prop` closed set — both are `fe-relevant`, not backend-only). For the inputs caller
the frontend consumer is `/requirements` drafting the frontend spec (e.g. a load-bearing cross-source
RBAC contradiction blocks coherent drafting — `fe-relevant`). A backend monitoring / scale / infra gap
blocks **none** of these.

## Recalibration rules (deterministic, given the class)

Let `cap_severity = "Minor"` when `target == "prototype"`, else `"Major"` (i.e. for `"application"`
**and** for `null`). "Cap a severity to X" = if it ranks higher than X in `severity_vocab`, lower it
to X; otherwise leave it.

- **`fe-relevant`** — no change. (No log entry.)
- **`fe-facing-contract`** — severity **unchanged**. Disposition: if it is the blocking value
  (`Reject`) **and** the gap does **not** block a frontend consumer, demote it to `safe_non_blocking`
  (`Defer`); otherwise unchanged. Log only if a value changed (`foreclosing_authority =
  "prototype-scope.md §6.10 contract boundary"`).
- **`backend-only`** — **retained and raised, never dropped**, then:
  - **Severity** capped to `cap_severity`. (Never `Blocker`.)
  - **Disposition**: if it is the blocking value (`Reject`), demote to `safe_non_blocking` (`Defer`).
    Other dispositions unchanged. (A `backend-only` finding is never `Reject`; in practice it is
    `Defer`.)
  - **`foreclosing_authority`**: under `target == "prototype"`, the prototype invariant that
    forecloses the concern — `PI-01` (server simulated) for server/integration/compute gaps, `PI-02`
    (fixtures) for persistence/data gaps, `PI-03` (validation visual-only) for server-side validation
    gaps, `PI-08` (review harness) for perf/ops gaps; default `PI-01`. Under `target ∈ {application,
    null}`, the authority is `prototype-scope.md "Not Prototypable" — backend reqs belong in the
    sibling backend document`.
  - Always emit a log entry for a `backend-only` finding when any value changed (an already-`Minor`
    `Defer` backend-only finding needs no change but still gets its `scope_class` set on the finding).

## Verdict interaction (caller's responsibility)

After this skill returns, the caller **recomputes its severity/disposition tallies and verdict from
the recalibrated values**. The consequence is the whole point: because no `backend-only` finding can
carry `Blocker` or `Reject`, backend gaps can **no longer force `BLOCKED`** — but they **still count**
toward `NEEDS-REVISION` (capped-but-counted). A frontend spec whose only "blockers" were backend gaps
now reads `NEEDS-REVISION`, with the backend notes visible and logged, instead of `BLOCKED`.

## Determinism & override

Classification (steps 1–4) is a **judgment call** the caller performs in-thread — like the worker's
original severity assignment, it is bounded (grounded in the concrete *Not Prototypable* / *In Scope*
lists) and auditable (every adjustment is logged), but it is not a pure table lookup. The cap
arithmetic and disposition demotion are fully deterministic given the class. The consultant may
**override** any recalibration in the caller's Revise loop (e.g. restore a severity the skill capped);
the recalibration log makes every adjustment visible so an override is an informed choice.

## Used by

- `framework/agents/reviews/adversarial-reviewer.md` — Step 3s (`target` from PI-block detection).
- `framework/agents/reviews-inputs/adversarial-reviewer.md` — consolidation sub-step (`target: null`).

## Anti-Patterns

- **Do not drop a finding.** This skill never removes a finding — that would defeat its purpose
  (backend concerns must still be *raised*). Dropping is the GR/PI "rescue" model this skill exists to
  replace.
- **Do not edit `evidence`, `problem`, or `recommendation` text.** Only `severity`, `disposition`,
  and the added `scope_class` may change. For the inputs caller this keeps the five sanctioned
  Recommendation forms intact.
- **Do not classify `backend-only` when the recommendation is UI-actionable.** Key on the corrective
  action; a network-failure UI state is `fe-relevant`, not backend-only.
- **Do not collapse a dual finding to `backend-only`.** Dual → `fe-facing-contract`. Bias toward not
  suppressing.
- **Do not recalibrate `fe-relevant` or (severity of) `fe-facing-contract` findings.** Only
  `backend-only` severities are capped; `fe-facing-contract` keeps its severity.
- **Do not raise a severity.** This skill only ever caps (lowers) or leaves unchanged. It never
  promotes a Minor backend finding to Major.
- **Do not skip the log.** Every changed rating produces a `recalibration_log` entry citing its
  `foreclosing_authority`; silent recalibration breaks the audit trail and the consultant's ability to
  override.
- **Do not infer `target`.** It is supplied by the caller. The requirements caller detects it from
  the PI-block; the inputs caller passes `null`. The skill never reads `source-manifest.json`.
