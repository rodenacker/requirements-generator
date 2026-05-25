# Analysis Sidecar Schema

**Purpose.** Defines the canonical JSON sidecar shape every `framework/agents/analyses/<method>-analyser.md` writes alongside its prose artefact. Downstream agents (today: `framework/agents/blueprint-architect.md` at step 2.6) read the sidecar instead of the prose to avoid context bloat — the prose stays on disk for consultants; the sidecar carries the small, role-keyed projection agents actually consume.

**Scope.** This file is the **canonical source** for:

- The sidecar envelope (top-level keys, drift detection, truncation flags).
- The per-role payload shapes keyed by the closed-enum `architect_roles` declared in `framework/skills/select-supporting-analyses.md > Static method → architect_roles mapping`.

Per `CLAUDE.md > Canonical-source rule`, every other file that uses the sidecar schema references this file rather than re-defining it.

**Status.** Infrastructure-first ship: the architect's step-02 reads sidecars when present and falls back to bounded full-Read of the prose otherwise (see `framework/shared/refusal-registry.md > RF-09`). Per-method analysers add sidecar emission in follow-up PRs (one method per PR, starting with the largest on-disk artefacts).

---

## 1. Envelope (top-level shape)

Every sidecar conforms to this top-level shape regardless of methodology:

```json
{
  "schema_version": "1",
  "method": "<registry slug, e.g. data-model>",
  "source_path": "analyse-requirements/<METHOD>/<artefact>.{html,md}",
  "source_sha256": "<sha256 of the prose artefact at write time>",
  "generated_at": "<ISO-8601 UTC timestamp>",
  "architect_projection": {
    "<role-key>": { /* per-role payload — see Section 2 */ },
    "...": { /* one entry per architect_role the method exposes */ }
  },
  "truncated": false
}
```

**Field semantics:**

- `schema_version` — literal string `"1"` for this revision. Increment only on breaking shape changes; additive role payloads do not bump the version.
- `method` — the kebab-case slug from `framework/assets/analyses/registry.md > methodologies[].name`. Must match the row whose `output_path` is `source_path`.
- `source_path` — repo-relative path to the prose artefact this sidecar projects. The architect uses this to compute the drift sha256 at read time.
- `source_sha256` — sha256 hex digest of the entire byte content of `source_path` at the moment the analyser wrote the sidecar. Used by the architect's step-02 drift check (mismatch → `RF-08`).
- `generated_at` — ISO-8601 UTC timestamp. Forensic only; the architect does not gate on it.
- `architect_projection` — object keyed by closed-enum role values from `select-supporting-analyses.md`. **Only roles the method actually exposes are present**; absent roles are signal-by-omission (`upstream-only` methods write an empty object). The architect reads only the role keys it needs at the step it needs them — see `framework/agents/blueprint-architect/steps/step-02-read-inputs.md > block 2.6`.
- `truncated` — top-level boolean. `true` iff **any** role payload was truncated to stay within the per-sidecar size cap. Surfaced as an in-thread architect note but not a hard halt.

**Hard size cap.** Each sidecar must be ≤ 20 KB on disk. If a method's full projection would exceed 20 KB, the analyser truncates the longest-tail collection within the lowest-priority role payload (priority order per the method's reference doc), sets `truncated: true` at top level, and adds a `truncated: true` flag inside the affected role's payload. Critical role payloads (those consumed at step 3 of the architect) take priority over step-5-only roles when trimming.

**Drift detection.** The architect's step-02 reads `source_path` from disk after reading the sidecar, computes its sha256, and compares against `source_sha256`. Mismatch fires `RF-08 stale_analysis_sidecar` and the architect halts cleanly (the consultant re-runs the analyser to regenerate the sidecar).

**Naming convention.** The sidecar lives next to its prose artefact: `analyse-requirements/<METHOD>/<METHOD-lowercase>.sidecar.json`. Example: `analyse-requirements/DATA-MODEL/data-model.sidecar.json`. The convention is fixed; `registry.md` does not need a per-row `sidecar_path` field as long as the convention holds.

---

## 2. Per-role payload shapes

The payload shape is keyed by the role, not the method — two methodologies that both expose `copy-vocabulary` write the same shape. This keeps the architect's consumer logic uniform across methods. Methods choose which roles to expose per the `Static method → architect_roles mapping` in `framework/skills/select-supporting-analyses.md`.

Every role payload also carries an optional `truncated: <boolean>` flag (default `false`) and an optional `notes: "<short prose>"` field — both omitted in the canonical happy path.

### 2.1 `screen-inventory`

Surfaces screen seeds the analysis implies. The architect cross-checks these against the inventory it derived from `scope.sources` at step-03 block 3.2c; missed screens are added (after a `requirements.md`-coverage check). Never widens the feature set.

```json
{
  "screens": [
    {
      "intent": "<noun-phrase, e.g. \"Pending approval list\">",
      "source_anchor": "<analysis-internal pointer, e.g. \"task-flows:T-2.3\" or \"state-diagram:pending-state\">",
      "covered_in_requirements": "<F-NN | BR-NN | UI-NN | §5.x | null>",
      "rationale": "<one-line prose, ≤ 120 chars>"
    }
  ]
}
```

`covered_in_requirements` is the analyser's best-effort hint — `null` means the analyser could not cite a `requirements.md` ID for the screen, which surfaces as a flagged requirements gap at step 3.2c (the architect does not add the screen).

### 2.2 `screen-inventory-entity-bijection`

Object-to-screen bijection (every core object expects a list + detail surface). Used at step 3.2c.

```json
{
  "entities": [
    {
      "name": "<EntityName>",
      "expected_screens": ["list", "detail", "<other>"],
      "source_anchor": "<analysis-internal pointer>",
      "rationale": "<one-line prose, ≤ 120 chars>"
    }
  ]
}
```

### 2.3 `screen-flow`

Sequence / branching of screens. Used at step 3.2c and step 3.3.

```json
{
  "flow_steps": [
    {
      "from": "<screen-hint or step-name>",
      "to": "<screen-hint or step-name>",
      "condition": "<plain-English trigger, e.g. \"on validation failure\" or \"happy path\">",
      "source_anchor": "<analysis-internal pointer>"
    }
  ]
}
```

### 2.4 `screen-properties-cross-check`

Entity attributes the analysis surfaces. **Cross-check only — never widens the §7 + F-NN closed set.** Used at step 3.2b.

```json
{
  "entities": [
    {
      "name": "<EntityName>",
      "attributes": [
        {
          "name": "<attributeName>",
          "type": "<short type hint, e.g. \"string\" | \"datetime\" | \"integer\" | null>",
          "source_anchor": "<analysis-internal pointer>"
        }
      ]
    }
  ]
}
```

Discrepancies between this list and `requirements.md > §7` are flagged in blueprint prose by step 3.2b's DATA-MODEL cross-check; entries are never added to the per-screen Properties closed set.

### 2.5 `per-screen-cta-set`

Primary CTA labels per screen. Used at step 5.3.4 (variant copy) and propagated to per-variant `manifest.json`.

```json
{
  "ctas": [
    {
      "screen_hint": "<intent-noun-phrase, matches a screen's Intent in the blueprint when possible>",
      "label": "<verb-phrase, e.g. \"Approve and submit\">",
      "context": "<short prose hint, ≤ 80 chars>",
      "source_anchor": "<analysis-internal pointer>"
    }
  ]
}
```

### 2.6 `per-screen-state-chips`

Status badge sets per entity / screen. Used at step 5.3.4 and per-variant state composition.

```json
{
  "entity_states": [
    {
      "entity": "<EntityName>",
      "chip_set": ["<StateA>", "<StateB>", "..."],
      "transitions": [
        {
          "from": "<StateA>",
          "to": "<StateB>",
          "trigger": "<event-name or plain-English condition>"
        }
      ],
      "source_anchor": "<analysis-internal pointer>"
    }
  ]
}
```

### 2.7 `per-screen-async-states`

Polling / pending screen variants implied by external-service handoffs. Used at step 5 for async-screen variants.

```json
{
  "async_screens": [
    {
      "screen_hint": "<intent-noun-phrase>",
      "trigger": "<external service or event, e.g. \"submit to external validator\">",
      "states": ["submitting", "queued", "polling", "complete", "failed"],
      "source_anchor": "<analysis-internal pointer>"
    }
  ]
}
```

### 2.8 `per-screen-role-visibility`

Persona-bound screen visibility (multi-actor swim lanes). Used at step 5 for role-bound variants.

```json
{
  "role_visibility": [
    {
      "actor": "<Persona name verbatim from requirements.md §3, or analysis's actor label if not yet bound>",
      "screens_visible": ["<screen-hint>", "..."],
      "screens_hidden": ["<screen-hint>", "..."],
      "source_anchor": "<analysis-internal pointer>"
    }
  ]
}
```

### 2.9 `variant-philosophy`

Pain-points / jobs / journey-phase emphasis that feeds variant `design_philosophy` prose. Used at step 5.3.4. The architect's prose composition keeps `design_philosophy` ≤ 100 chars and plain-English; this payload carries the raw inputs the architect refines into prose.

```json
{
  "philosophy_inputs": [
    {
      "phase_or_job": "<journey phase, JTBD job-string, or pain-point label>",
      "pain_or_opportunity": "<short prose, ≤ 120 chars>",
      "design_implication": "<short prose, ≤ 120 chars>",
      "source_anchor": "<analysis-internal pointer>"
    }
  ]
}
```

### 2.10 `variant-dimension-applicability`

Per-goal × dimension scoring (replaces the legacy full Read of `analyse-requirements/TRADE-OFF-DIMENSIONS/trade-off-matrix.html` at step 2.7). Used at step 5.2.

```json
{
  "dimension_scores": [
    {
      "goal_id": "<G-NN>",
      "goal_label": "<verbatim §4 goal label>",
      "dimension": "<density-focus | speed-accuracy | power-simplicity | control-automation | flexibility-consistency>",
      "score": -2,
      "rationale": "<short prose, ≤ 120 chars>"
    }
  ]
}
```

`score` is an integer in `-2..+2`. The architect's step 5.2 reads this payload directly when a `trade-off-dimension-analysis` selection is cached; the prose-HTML fallback at step 2.7 only fires when this payload is absent (and the consultant did not select trade-off-dimensions).

### 2.11 `copy-vocabulary`

Labels / hints / help text / error messages. Used at step 5.3.4. The architect picks term names; per-variant copy realisation happens at the variant-generator's step 4.

```json
{
  "terms": [
    {
      "term": "<word or phrase>",
      "definition": "<one-line definition, ≤ 200 chars>",
      "ui_use": "<label | hint | status | error | help | empty-state | null>",
      "source_anchor": "<analysis-internal pointer>"
    }
  ]
}
```

### 2.12 `feature-presence`

Features in / out of variant scope (Opportunity-Solution-Tree style). Used at step 5 for per-variant feature emphasis.

```json
{
  "features": [
    {
      "name": "<feature-name, ideally a §6 F-NN or §1.7 capability label>",
      "in_scope": true,
      "rationale": "<short prose, ≤ 120 chars>",
      "source_anchor": "<analysis-internal pointer>"
    }
  ]
}
```

### 2.13 `upstream-only`

Sentinel role for methods that exist as upstream requirements-review aids only and never thread into the architect's workflow (today: `five-whys`). The architect records the selection in its in-memory state but does not consume the payload. The payload is therefore intentionally minimal.

```json
{
  "notes": "Methodology is upstream-only; the architect does not consume this payload."
}
```

Analysers exposing `upstream-only` may set `architect_projection: { "upstream-only": { "notes": "..." } }` and omit every other role.

---

## 3. Consumer contract

### 3.1 Architect read path (step-02 block 2.6)

1. Read `selections[i].sidecar_path` (or derive it from the convention `analyse-requirements/<METHOD>/<method-lowercase>.sidecar.json` when the field is absent).
2. JSON-parse the envelope. Verify `schema_version == "1"` and `method == selections[i].name`; mismatch is a structural error (halt plain-text).
3. Compute sha256 of `source_path` on disk; compare against `source_sha256`. Mismatch fires `RF-08 stale_analysis_sidecar`.
4. For each role in `selections[i].architect_roles`, read `architect_projection[<role>]` into `cached_projections[<role>][<selections[i].name>]`. Skip the role if absent in `architect_projection` (the method does not expose it — silent skip, no warning).
5. Discard the rest of `architect_projection` (roles the architect did not request).

### 3.2 Architect step consumption

Step 3 reads `cached_projections[<role>][<source-name>]` for roles `screen-inventory`, `screen-inventory-entity-bijection`, `screen-flow`, `screen-properties-cross-check`.

Step 5 reads `cached_projections[<role>][<source-name>]` for roles `variant-philosophy`, `variant-dimension-applicability`, `per-screen-state-chips`, `per-screen-async-states`, `per-screen-role-visibility`, `per-screen-cta-set`, `copy-vocabulary`, `feature-presence`.

Role `upstream-only` is recorded in `cached_projections["upstream-only"]` but never consumed by any step file.

### 3.3 Fallback when no sidecar exists (legacy artefacts)

When `selections[i].sidecar_present == false` (or the sidecar file is absent on disk):

1. The architect logs `[ANALYSIS-FALLBACK: <selections[i].name>]` in its blueprint's Architect notes section.
2. The architect computes the byte size of `selections[i].output_path`. If > 60 KB, fire `RF-09 legacy_analysis_too_large` and halt — the consultant must re-run the analyser to regenerate the sidecar.
3. Otherwise, full-Read `output_path` **at the step that needs it** (defer step-5-only roles to step-05 to avoid step-02 cache bloat), populate `cached_legacy_full_reads[<selections[i].name>]` keyed by source name, and consume the prose directly within the step using best-effort role-relevant extraction. Drop the entry from cache at step boundary.

The fallback path is the one-cycle deprecation: existing prose-only analyses keep working while their analysers are updated; the 60 KB cap forces regeneration of the largest offenders first (TASK-FLOWS 109 KB, USE-CASES 102 KB, TRADE-OFF-DIMENSIONS 106 KB, DATA-MODEL 83 KB — all currently above the cap on disk).

---

## 4. Used by

- `framework/agents/blueprint-architect/steps/step-02-read-inputs.md` — block 2.6 reads sidecars per Section 3.1.
- `framework/agents/blueprint-architect/steps/step-03-author-blueprint.md` — consumes `cached_projections[<role>][<source-name>]` per Section 3.2.
- `framework/agents/blueprint-architect/steps/step-05-compose-variants.md` — same.
- `framework/skills/select-supporting-analyses.md` — stamps `sidecar_path` and `sidecar_present` per selection in `analyses-inputs.json` so the architect has zero ambiguity.
- `framework/agents/analyses/<method>-analyser.md` (each analyser, follow-up PRs) — emits a sidecar matching this schema at write time, alongside the prose artefact.
- `framework/assets/analyses/registry.md` — links to this file from its prose section.
- `framework/shared/refusal-registry.md > RF-08, RF-09` — the two predicates that fire on stale or oversized legacy artefacts.

---

## 5. Anti-patterns

- Do not embed the prose artefact's HTML / Markdown body inside the sidecar. The sidecar carries projected, structured fields only; the prose remains the canonical consultant-readable source of truth on disk.
- Do not write a role payload for a role the method does not expose per `select-supporting-analyses.md`'s static mapping. Omit the key entirely; absence is signal.
- Do not invent new role keys outside the closed enum. Adding a role is a coordinated change across `select-supporting-analyses.md`, this file, and every consumer step file.
- Do not omit `source_sha256`. Drift detection is the only protection against the consultant hand-editing the prose; without the hash the architect would silently consume stale projections.
- Do not bump `schema_version` for additive role payloads. The version is reserved for breaking shape changes (envelope rename, payload restructuring).
- Do not exceed 20 KB. If a method's natural projection is larger, truncate the longest-tail collection per Section 1's priority rule and set `truncated: true`.
- Do not write the sidecar to a path other than `<output_path's directory>/<method-lowercase>.sidecar.json`. The convention is what lets the architect derive the path when `selections[i].sidecar_path` is absent.
