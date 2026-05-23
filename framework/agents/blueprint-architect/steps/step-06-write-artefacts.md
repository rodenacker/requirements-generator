---
name: step-06-write-artefacts
description: 'Write variants.json (always when variants_output_path != null). Blueprint.md was already written at step 4 on mode = create.'
---

# Step 6: Write artefacts

## 6.1 Blueprint status

On `mode = "create"`, the blueprint was written at step 4.1 + re-written at step 4.3 (after the preflight verdict landed in `{{PATTERN_COVERAGE_SUMMARY}}`). It exists on disk and was verify-artifact-write'd twice. **No write in this step.**

On `mode = "regenerate-variants"` and `mode = "add-variant"`, the blueprint is reused from disk; no write occurred or will occur from this agent.

## 6.2 Write `variants.json`

Skipped when `variants_output_path == null`.

1. Ensure the parent directory exists: `Bash mkdir -p $(dirname <variants_output_path>)` (the parent is typically `wireframes/<scope_slug>/` which may not exist yet on a fresh scope-slug).
2. Render the in-memory `variants.json` payload from step 5.7 as a JSON string with two-space indentation. Compute the sha256.
3. `Write <variants_output_path>` with the rendered content.
4. Call `framework/skills/verify-artifact-write.md` with `path = <variants_output_path>`, `expected_sha256 = <rendered hash>`, `expected_min_bytes = 200` (a minimal-shape variants.json with 1 variant + the meta fields is comfortably above 200 bytes).

On `pass`, capture `wrote_variants = true` and advance. On `RF-04 trigger`, propagate the hard halt per `framework/shared/refusal-registry.md > RF-04` (fail handback; the orchestrator does not advance to Stage 3).

## 6.3 Cross-validation of `blueprint_sha256`

After the variants.json write succeeds, re-Read `<blueprint_output_path>` and re-compute its sha256. Confirm it matches the `blueprint_sha256` field embedded inside the variants.json. A mismatch means the blueprint file was modified between step 4.3 and step 6.2 (an external write race; rare but possible). On mismatch, halt with structured error *"Blueprint sha256 drift detected between step 4 and step 6 — `<blueprint_output_path>` was modified mid-run. Re-invoke `/wireframe`."* and fail handback.

---

**Next:** Read fully and follow `step-07-handback.md`.
