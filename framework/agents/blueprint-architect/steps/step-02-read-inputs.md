---
name: step-02-read-inputs
description: 'Read the scope manifest, the requirements document, and (on non-create modes) the existing blueprint and variants.json.'
---

# Step 2: Read inputs

## 2.1 Read the scope manifest

```
Read tool: <scope_path>
```

JSON-parse the contents. Capture into in-memory state:

- `scope.scope_slug` — must equal the input parameter `scope_slug`. Mismatch is a structural error: surface plain-text *"Scope-slug mismatch: scope.json carries `{{scope.scope_slug}}` but agent was invoked with `{{scope_slug}}`. Cancelling — re-run scope-selector."* and fail handback. The orchestrator does not write a completed event.
- `scope.sources` — the six categorised lists. Empty categories are valid (the consultant chose to skip them at scope-selector); zero non-empty categories is a structural error (re-run scope-selector).
- `scope.personas_available` — the list of §3 persona names from the requirements doc at selection time.
- `scope.freeform_description` — optional prose (free-form branch) or `null` (structural branch). Used in the architect's notes only.
- `scope.requirements_sha256` — propagated into the blueprint's `REQUIREMENTS_SHA256` slot for drift detection by downstream readers.

## 2.2 Read the requirements doc

```
Read tool: requirements/requirements.md
```

Full read; the orchestrator's prerequisite gate guaranteed it exists and is non-empty.

**Drift check:** compute the sha256 of the bytes just read. If it does not match `scope.requirements_sha256`, the requirements doc has changed since scope-selection. Surface a structured warning in the architect's in-thread announcement (do **not** fail; the consultant may have intentionally edited the doc): *"⚠ `requirements/requirements.md` has changed since scope-selection (new sha256 `{{actual_sha256}}` vs scope.json `{{scope.requirements_sha256}}`). Proceeding with current requirements; any scope sources no longer present will surface as bijection violations in step 3."*

## 2.3 Locate scope-restricted slices

Walk the requirements doc and locate the lines that reference each ID / name in `scope.sources`. Capture the one-line summary text per ID (typically the first content line under the ID's anchor) into in-memory `scope_summaries[<id>] = "<first-line>"`. Truncate each summary to 120 chars.

## 2.4 Extract §3 personas

Walk `## 3. Target users` and locate every `### <Name>` header. For each, capture:

- `personas[<Name>].name` — the verbatim header text.
- `personas[<Name>].characteristic` — the first one-or-two-line description below the header.
- `personas[<Name>].traits` — heuristic-extracted traits used by `tradeoff-dimensions-registry.md > Section 5`:
    - `frequency` ∈ `{daily | weekly | occasional | first-time}` (extract from copy like "daily high-volume", "occasional", "first-time").
    - `expertise` ∈ `{novice | intermediate | expert}` (extract from copy like "expert", "novice", "trained operator").
    - `role` ∈ `{operator | reviewer | approver | auditor | viewer | admin}` (extract from copy or the persona's name).

Cross-check `personas` against `scope.personas_available` — every persona name in `scope.personas_available` should be in `personas`. A mismatch (e.g. requirements doc renamed a persona) is a structural warning, not a hard fail; surface in-thread and use the requirements doc's current names as authoritative.

## 2.5 (Non-create modes only) Read prior artefacts

On `mode = "regenerate-variants"`:

```
Read tool: <blueprint_output_path>
```

Capture the screen inventory + flow + sources from the existing blueprint. Re-use the in-memory variables that `step-03-author-blueprint.md` would produce, but skip the authoring logic. Note the existing blueprint's sha256 into in-memory state (will be re-verified at step 7 to confirm step 6 did not overwrite it).

On `mode = "add-variant"`:

```
Read tool: <blueprint_output_path>
Read tool: <variants_output_path>
```

Capture both. The variants.json's `variants[]` list is preserved verbatim through step 5; step 5 surfaces a single new-variant prompt and appends one entry only.

## 2.6 (Optional) Read trade-off matrix

Test whether `analyse-requirements/TRADE-OFF-DIMENSIONS/trade-off-matrix.html` exists. If yes, `Read` it (the file is HTML; extract the per-goal × dimension scoring from its `<table>` body). Use the scoring at step 5 to inform the dimension-applicability filter — goals scoring near the poles on a given dimension reinforce that dimension's applicability. Absent → skip silently; the architect falls back to the heuristic rules in `tradeoff-dimensions-registry.md > Section 2`.

---

**Next:** On `mode = "create"`, read fully and follow `step-03-author-blueprint.md`. On `mode = "regenerate-variants"` or `mode = "add-variant"`, skip to `step-05-compose-variants.md` (step 3 is skipped because the blueprint is reused; step 4 is also skipped because the blueprint did not change and the prior preflight result is no longer needed — `variants.json` regeneration is purely a re-composition of trade-off positions and personas, not a re-evaluation of pattern coverage).
