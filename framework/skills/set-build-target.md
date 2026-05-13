# set-build-target.md

**Purpose:** Set the root-level `target` field of `requirements/source-manifest.json` to the consultant's build-target choice (`"prototype"` or `"application"`) captured at the orchestrator's Step 1b, then verify the write. The build-target choice governs whether the drafter's gap-pass emits `[OUT-OF-SCOPE: domain-default]` markers and whether the merger appends `framework/shared/prototype-invariants.md` to the final spec. This skill is the single mediator for that mutation — the orchestrator never Edits the manifest directly.

**Inputs:**
- `target` — exactly one of `"prototype"` or `"application"`. Any other value (including `null`) is a caller bug; this skill does not validate the choice set, but `framework/orchestrators/requirements-orch.md > Step 1b` constrains the prompt's choice set.
- `manifest_path` — repo-relative path of the manifest to mutate. Always `"requirements/source-manifest.json"` in current usage.

**Outputs:** exactly one of:
- `pass` — the manifest on disk now carries `"target": <target>` and the write has been verified.
- `RF-04 trigger` — the verification step failed; the orchestrator halts per `framework/shared/refusal-registry.md > RF-04 artifact_write_unverified`.

**Used by:**
- `framework/orchestrators/requirements-orch.md` — Step 1b, immediately after the consultant's build-target answer.

## Procedure

1. `Read` the manifest at `manifest_path`. It must parse as JSON per the schema in `framework/skills/build-source-manifest.md` and must already have `schema_version: 1`.
2. Set the root-level field `target` to `target`. If the field is already present (re-invocation in the same run), overwrite it. Do not touch any other field — `schema_version`, `generated_at`, and every entry under `rows[]` stay byte-identical.
3. Serialise the JSON with the same two-space indentation and trailing newline used by `build-source-manifest.md` so the diff is minimal.
4. `Write` the result back to `manifest_path`.
5. Call `framework/skills/verify-artifact-write.md` with `path: manifest_path`, `expected_sha256: <sha256 of the bytes just written>`, `expected_min_bytes: <byte length of the rendered manifest>`. On `pass`, return `pass`. On `RF-04 trigger`, return `RF-04 trigger`.

## Self-validation

- After step 2, exactly one root-level field has changed: `target`. `rows[]`, `schema_version`, and `generated_at` are byte-identical to the pre-Edit manifest.
- `target` is exactly one of `"prototype"` or `"application"` — never `null`, never any other string.
- The verify-artifact-write call ran and its result is propagated to the caller.

## Anti-Patterns

- Do not modify `rows[]`, `schema_version`, or `generated_at`. The manifest's content lineage is anchored on `generated_at`; mutating it during build-target selection would imply the inputs were re-enumerated, which they were not.
- Do not infer `target` from the manifest's rows or any other source. The orchestrator's Step 1b is the sole authority for this choice.
- Do not skip `verify-artifact-write.md`. A truncated manifest after this skill strands the drafter on a half-written file at workflow start.
- Do not set `target` to `null`. `null` is the input-handler's initial value; reverting to it here would be a regression of the consultant's choice.
- Do not call this skill outside the orchestrator's Step 1b flow. Mid-run mutation of `target` would change the gap-pass's emission contract halfway through the pipeline.
