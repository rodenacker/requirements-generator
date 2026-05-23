# check-wireframe-set-freshness.md

**Purpose:** Detect partial / stale / fresh wireframe-set state on disk for a given `scope_slug`, so the calling orchestrator can choose between Overwrite / Regenerate-variants / Add-variant / Keep / Cancel at its prior-set gate without re-implementing the per-scope detection logic inline.

Pipeline-private to `/wireframe`. Read-only.

## Inputs

- `scope_slug` — the kebab-case slug of the scope being checked. **Required.** Captured by the calling orchestrator's scope-selector return.
- `blueprints_root` — optional, defaults to `"blueprints/"`. Allows future relocation without skill edits.
- `wireframes_root` — optional, defaults to `"wireframes/"`. Same rationale.

## Outputs

A single structured return value:

```yaml
verdict: clean | partial-blueprint | partial-variants | complete
detected_paths:
  scope_json: blueprints/<scope_slug>/scope.json (present|absent)
  blueprint_md: blueprints/<scope_slug>/blueprint.md (present|absent)
  variants_json: wireframes/<scope_slug>/variants.json (present|absent)
  variant_dirs: [<list of variant subdir names>]
  comparison_html: wireframes/<scope_slug>/comparison.html (present|absent)
  index_html: wireframes/<scope_slug>/index.html (present|absent)
variant_state:
  - variant_id: POWER-DENSITY-EXPERT
    completeness: complete | partial | empty
    missing: [list of required-but-absent files]
notes: "<one short line summarising the state>"
```

Verdicts:

- **`clean`** — neither `blueprints/<scope_slug>/` nor `wireframes/<scope_slug>/` exists. The orchestrator skips the prior-set gate and proceeds to a fresh pipeline run.
- **`partial-blueprint`** — `blueprints/<scope_slug>/scope.json` exists but `blueprints/<scope_slug>/blueprint.md` does not. A prior run was interrupted before the architect completed Stage 2. The orchestrator surfaces the prior-set gate; `Overwrite` is the natural choice (resume by full restart). The plan does not currently expose a "resume-from-architect" branch — interruption recovery is the consultant's responsibility on the overwrite path.
- **`partial-variants`** — `blueprint.md` and `variants.json` exist; at least one variant subdir is `partial` or `empty` (a Stage-3 sub-agent did not complete its full file set). The orchestrator surfaces the prior-set gate; `Regenerate variants only` is the natural choice.
- **`complete`** — `blueprint.md`, `variants.json`, every variant subdir's required file set, plus `comparison.html` and `index.html` all present and parseable. The orchestrator surfaces the full prior-set gate; the consultant may choose any of the five options.

## Used by

- `framework/orchestrators/wireframe-orch.md` — step 0d, immediately after scope-slug capture, before the prior-set gate is surfaced. The orchestrator may compose its prompt text using the returned `notes` line.

## Procedure

1. **Glob the two roots.** `Glob blueprints/<scope_slug>/*` and `Glob wireframes/<scope_slug>/*`. If both globs return zero entries, return `verdict: clean` immediately with empty `detected_paths` and `variant_state`.

2. **Detect blueprint-side files.** Test for existence of `blueprints/<scope_slug>/scope.json` and `blueprints/<scope_slug>/blueprint.md`. Record in `detected_paths`.

3. **Detect wireframe-side top-level files.** Test for existence of `wireframes/<scope_slug>/variants.json`, `wireframes/<scope_slug>/comparison.html`, `wireframes/<scope_slug>/index.html`. Record in `detected_paths`.

4. **Enumerate variant subdirs.** Every direct child directory under `wireframes/<scope_slug>/` is a variant subdir (its directory name is the `variant_id`). Glob `wireframes/<scope_slug>/*/` and capture each as a row in `variant_state`.

5. **Per-variant completeness check.** For each variant subdir, test for the **required-by-shape** file set (per `framework/agents/wireframe-variant-generator.md > Output`):

    - `wireframes.html` (variant landing)
    - `wireframe-ds.css` (linked DS, one per variant dir)
    - `manifest.json` (per-screen pattern bindings)
    - `variant-position.json` (self-scored sidecar)
    - at least one `screen-NN-*.html` file

    Compute `completeness`:

    - **`complete`** — every required file is present **and** the count of `screen-NN-*.html` files matches the screen inventory in `blueprints/<scope_slug>/blueprint.md` (the skill reads the blueprint once, on demand, only for this comparison — skipped if `blueprint.md` is absent, in which case the count check is replaced by "≥1 screen file" and the variant is treated as `partial`).
    - **`partial`** — at least one required file is present but the full set is incomplete.
    - **`empty`** — the variant subdir exists but contains zero required files (a defensive case — a directory that was created but never populated).

    Populate `missing` with every required-but-absent filename.

6. **Compute the aggregate verdict.**

    - If neither `blueprints/<scope_slug>/scope.json` nor any `wireframes/<scope_slug>/` content exists → `clean`.
    - Else if `blueprint.md` is absent → `partial-blueprint`.
    - Else if any variant row has `completeness ∈ { partial, empty }`, **or** `variants.json` is absent, **or** `comparison.html`/`index.html` is absent → `partial-variants`.
    - Else → `complete`.

7. **Compose `notes`.** One short line summarising the state (used by the orchestrator's prior-set gate prompt for clarity). Examples:

    - `clean` — *"No prior wireframe set for `{{scope_slug}}`."*
    - `partial-blueprint` — *"Prior scope-selection exists but blueprint was not produced — likely interrupted."*
    - `partial-variants` — *"Prior blueprint + 1 of 2 variants complete; `WIZARD-NOVICE` is missing `manifest.json` and `variant-position.json`."*
    - `complete` — *"Full wireframe set on disk: 2 variants, comparison + index produced."*

8. **Return** the structured payload.

## Self-validation

- Every variant subdir under `wireframes/<scope_slug>/` is enumerated in `variant_state` (1:1 by directory name).
- `verdict` follows the deterministic rules in step 6 (no smoothing).
- The skill performs zero writes.
- When `blueprint.md` is absent, the per-variant screen-count check is skipped (no comparison source); `partial` is still assignable based on the required-file set.

## Anti-Patterns

- Do not parse the blueprint beyond extracting the screen-inventory count. Deeper parsing belongs to the architect / variant-generator / comparator.
- Do not auto-decide for the orchestrator. The skill returns a verdict; the orchestrator surfaces the prior-set gate and lets the consultant choose.
- Do not write any file. The skill is purely diagnostic — even a debug log would couple it to a single caller's filesystem layout.
- Do not assume the per-variant required-file shape independently. The shape is documented in `framework/agents/wireframe-variant-generator.md > Output` — that file is the source of truth; this skill mirrors it. If a future variant-generator change adds or removes a required file, update both files together.
- Do not silently treat an unknown directory under `wireframes/<scope_slug>/` as a variant. Every direct child *is* a variant by construction (the orchestrator writes only per-variant subdirs and the three top-level files); the skill records them all without filtering. Unexpected entries surface in `variant_state` with whatever `completeness` they evaluate to — the orchestrator surfaces them to the consultant if anything looks off.
