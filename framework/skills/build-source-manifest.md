# build-source-manifest.md

**Purpose:** Emit a source manifest from the post-classification, post-conversion view of the consultant-dropped input folder. The manifest is the downstream consumer's sole input enumeration — consumers do not glob the input folder and do not classify files. Every readable file a consumer will consume has a row here; unsupported files are recorded for forensic record but not read.

**Inputs:**
- `manifest_path` — repo-relative path to the manifest file to write. Required. The four input-handler-using pipelines (`/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`) all pass `requirements/source-manifest.json` so they share a single canonical manifest on disk; future pipelines may pass a different path.
- `inherited_target` — string or `null`. Optional, default `null`. Must be one of `"prototype"`, `"application"`, or `null`. When non-null, emit as the manifest's root-level `target` field instead of `null`; the input-handler passes this only on a refresh (when an existing manifest's `target` is being preserved across a rebuild) — see `framework/agents/input-handler.md` step 0. When omitted or `null`, the manifest's `target` field is emitted as `null` (today's behaviour on create / first build).
- The list of classified rows produced by `framework/skills/classify-input-tier.md`.
- For each `Supported-via-MCP` row that converted successfully: the sibling path returned by `framework/skills/convert-input-file.md` and that skill's `conversions_applied` string.
- For each `Native-multimodal` (raster) row that described successfully: the sibling path returned by `framework/skills/describe-visual-input.md` and that skill's `conversions_applied` string (`vision-described[; ...]`).
- For each `Vector-renderable` row that rendered + described successfully: the sibling path returned by `framework/skills/describe-visual-input.md` (fed the raster from `framework/skills/render-visual-to-raster.md`) and its `conversions_applied` string (`vision-described; rendered-from-vector; render-tool=<name>`).
- For each row that failed conversion/description/render: the row's tier is rewritten to `Unsupported` and `conversions_applied` carries the failure sub-tag (`failed — encrypted`, `failed — corrupt`, `failed — vision`, or `failed — render`).
- For each `Unsupported` row (originally Unsupported or demoted from a failed conversion): no conversion is attempted.

**Outputs:**
- The manifest file written at `manifest_path`.
- A signal back to the caller indicating whether the manifest contains any non-Unsupported rows (relevant for `RF-03 input_no_supported_files`).

**Used by:**
- `framework/agents/input-handler.md` — called once after enumeration, classification, and the per-file conversion loop have completed. The agent passes through its own `manifest_path` parameter so all four input-handler-using pipelines (`/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`) resolve to the same canonical manifest path (`requirements/source-manifest.json`) today. On a refresh (input-handler's `mode = "refresh"` branch), the agent also passes `inherited_target` to preserve the existing manifest's `target` value across the rebuild; on a create, `inherited_target` is `null` and `target` is emitted as `null`.

## Schema

```json
{
  "schema_version": 1,
  "generated_at": "<ISO-8601 UTC>",
  "target": "prototype | application | null",
  "rows": [
    {
      "filename": "<basename>",
      "tier": "Native-text | Native-multimodal | Vector-renderable | Supported-via-MCP | Unsupported",
      "kind": "primary",
      "sha256": "<hex of original_path file bytes>",
      "conversions_applied": "none | markitdown-mcp[; sub-tag...] | vision-described[; sub-tag...] | drawio-xml-fallback[; sub-tag...] | failed — <reason>",
      "original_path": "input/<basename>",
      "converted_sibling": "input/<basename>.converted.md | input/<filename-with-ext>.converted.md | null"
    }
  ]
}
```

Field rules:
- `filename` — basename only, including extension.
- `tier` — exactly one of the five documented values (`Native-text`, `Native-multimodal`, `Vector-renderable`, `Supported-via-MCP`, `Unsupported`).
- `kind` — `"primary"` for every row in this MVP. The `"derived"` value is reserved for future extensions (style assets, UI evidence) and is not produced today.
- `sha256` — hex digest of the bytes of `original_path` on disk at manifest-build time. Used by `framework/skills/check-manifest-freshness.md` to detect input drift on a re-invocation.
- `conversions_applied` — `"none"` for Native-text and originally-Unsupported rows. `"markitdown-mcp[; sub-tag...]"` for successful `Supported-via-MCP` conversions. `"vision-described[; sub-tag...]"` for successful `Native-multimodal` (raster) descriptions and rendered `Vector-renderable` descriptions; on a rendered `Vector-renderable` row the sub-tags carry `rendered-from-vector` and `render-tool=<name>`. `"drawio-xml-fallback[; sub-tag...]"` for a `.drawio` `Vector-renderable` row that was read via the XML-decode fallback (`framework/skills/decode-drawio-xml.md`) instead of rendered — used when the `drawio` binary is absent or the render failed; the optional sub-tag is `multi-page-source-first-page-only`. `"failed — <reason>"` for rows whose conversion/description failed (the row's tier in the same emit is `"Unsupported"`); reasons include `markitdown` failures (`failed — encrypted`, `failed — corrupt`), `failed — vision` (the describer could not interpret the image), and `failed — render` (the vector could not be converted by any path — for `.drawio`, both render and the XML fallback failed).
- `original_path` — repo-relative.
- `converted_sibling` — repo-relative path of the `*.converted.md` sibling that downstream consumers read **instead of** `original_path`. Non-null for three row kinds: successful `Supported-via-MCP` rows (markitdown rendering), described `Native-multimodal` rows (frozen vision description), and rendered `Vector-renderable` rows (frozen vision description of the rendered raster). `null` for `Native-text` and `Unsupported` rows. **Naming convention:** `Supported-via-MCP` siblings *replace* the extension (`spec.docx` → `spec.converted.md`); `Native-multimodal` and `Vector-renderable` siblings *append* to the full filename (`chart.png` → `chart.png.converted.md`, `flow.svg` → `flow.svg.converted.md`) so a visual never collides with a same-stem Office file's sibling. Both forms match the `*.converted.md` glob used by freshness/reset.
- `target` — exactly one of `"prototype"`, `"application"`, or `null`. On a **create** invocation (input-handler's first build for a manifest, called with `inherited_target: null` or omitted), this skill emits `null` — the target has not yet been set at manifest-build time. On a **refresh** invocation (input-handler's `mode = "refresh"` branch, called with a non-null `inherited_target` captured from the pre-rebuild manifest), this skill emits the inherited value verbatim — preservation across the rebuild, never origination. The `/requirements` orchestrator's Step 1b is the only place that *originates* a `target` value (via `framework/skills/set-build-target.md`, auto-set to `"prototype"` after the consultant accepts the manifest). The `/generate-prd`, `/analyse-inputs`, and `/review-inputs` orchestrators never invoke `set-build-target.md`; on a first-mover invocation of any of those three pipelines, `target` stays `null` indefinitely (and is preserved as `null` across any subsequent refresh). Downstream `/requirements`-pipeline agents (drafter, merger) Read this field on a legacy manifest that omits the field entirely and treat the absence as `"prototype"` (one-time additive migration; no rewrite). The resolver does not Read this field — its behaviour is target-agnostic. Input-analysers under `/analyse-inputs` and input-reviewers under `/review-inputs` ignore this field entirely. The `/generate-prd` drafter Reads the field as informational reference in §1 metadata but does not branch on it.

## Read-path resolution (canonical)

This skill is the canonical home of the rule every downstream input-consumer follows to decide which file to read for a manifest row. Consumers (the `/requirements` drafter, the `/generate-prd` drafter, every `/analyse-inputs` analyser, every `/review-inputs` reviewer) **reference this rule rather than re-deriving a per-tier branch**:

> **Read-path resolution.** For each manifest row: if `converted_sibling` is non-null, read `converted_sibling`; otherwise read `original_path`. Skip rows with `tier: "Unsupported"`. Skip = do not read; the row's file is never deleted or moved (see `framework/shared/input-safety.md`, `IS-02`).

The rule is intentionally tier-agnostic: a consumer never needs to know *why* a sibling exists (markitdown conversion, frozen vision description, or rendered-then-described vector). The sibling is always the consumer-facing surface when present. This means a row's `original_path` is read only for `Native-text` (which never carries a sibling) — every other consumable row is read through `converted_sibling`. Consumers must **not** read the `original_path` of a row that carries a non-null `converted_sibling` (e.g. re-interpreting an image's pixels when a frozen description exists defeats the single-interpretation contract).

### Pipeline-scoped read exclusion (`/requirements` only) — `IX-05`

The manifest is shared verbatim across the four input-handler pipelines (it is built once, enumeration-identical), so **no** row is removed at build time for a single pipeline. Instead, **one consumer applies a scoped skip**:

> **`/requirements` drafter only:** skip any row whose `filename` matches `*.stadium.design-signals.md`. It is a Stadium `design-signals` asset — entirely Tier-B styling material owned by `/design-system`, which grounded 0 requirement claims. Skip = do not read; the row stays in the manifest and the file is never moved/deleted (`framework/shared/input-exclusions.md`, `IX-05` + `IS-02`).

Every **other** consumer — the `/generate-prd` drafter, all `/analyse-inputs` analysers, all `/review-inputs` reviewers — ignores this clause and reads the `design-signals` row normally via the base Read-path rule above. The `glossary` asset is **not** excluded by any pipeline (it grounds requirement claims — see `IX-05`).

## Row-construction algorithm

For each classified row from `classify-input-tier.md`, in input-order:

1. Compute `sha256` of the bytes at `original_path`.
2. Fill `filename`, `original_path`, `kind: "primary"`.
3. Branch on tier:
    - `Native-text` — `tier` as classified, `conversions_applied: "none"`, `converted_sibling: null`.
    - `Native-multimodal` and description succeeded — `tier: "Native-multimodal"`, `conversions_applied: "vision-described[; sub-tag...]"`, `converted_sibling: "input/<filename-with-ext>.converted.md"`.
    - `Vector-renderable` and render+description succeeded — `tier: "Vector-renderable"`, `conversions_applied: "vision-described; rendered-from-vector; render-tool=<name>"`, `converted_sibling: "input/<filename-with-ext>.converted.md"`.
    - `Vector-renderable` `.drawio` read via XML-decode fallback (renderer absent or render failed, but `decode-drawio-xml.md` returned `ok`) — `tier: "Vector-renderable"`, `conversions_applied: "drawio-xml-fallback[; multi-page-source-first-page-only]"`, `converted_sibling: "input/<filename-with-ext>.converted.md"`.
    - `Native-multimodal` description failed or `Vector-renderable` render/description failed (for `.drawio`, the XML fallback also failed) — `tier: "Unsupported"`, `conversions_applied: "failed — vision"` or `"failed — render"`, `converted_sibling: null`.
    - `Supported-via-MCP` and conversion succeeded — `tier: "Supported-via-MCP"`, `conversions_applied: "markitdown-mcp[; sub-tag...]"`, `converted_sibling: "input/<basename>.converted.md"`.
    - `Supported-via-MCP` and conversion failed — `tier: "Unsupported"`, `conversions_applied: "failed — <reason>"`, `converted_sibling: null`.
    - `Unsupported` (originally) — `tier: "Unsupported"`, `conversions_applied: "none"`, `converted_sibling: null`.

After all rows are constructed, set `schema_version: 1`, `generated_at: <ISO-8601 UTC of manifest-build time>`, and `target: <inherited_target>` (the value of the caller-supplied `inherited_target` parameter; `null` when omitted or explicitly `null`). Type-check `inherited_target` before emission: it must be exactly one of `"prototype"`, `"application"`, or `null`. Any other value (including the string `"null"`, or any other string) is a programming error — halt with an `RF-04`-style refusal rather than emitting it. Serialise the JSON with two-space indentation and a trailing newline. `Write` to `manifest_path`. The `target` field's lifecycle is owned by `framework/skills/set-build-target.md` (originate) and this skill (preserve via `inherited_target`); this skill never *originates* a non-null value, only *preserves* one the caller has already read from an existing manifest. `/generate-prd`, `/analyse-inputs`, and `/review-inputs` invocations never call `set-build-target.md`, so a manifest first-built by one of those pipelines retains `target: null` indefinitely (and across any subsequent refresh, since preservation of `null` is `null`); downstream input-analysers and input-reviewers ignore the field, and the PRD drafter reads it as informational only.

## Self-validation

- Every input file from the classifier produced exactly one row.
- Every row has all seven fields, with the correct types per the schema.
- For every row with `tier ∈ {"Supported-via-MCP", "Native-multimodal", "Vector-renderable"}`, `converted_sibling` is non-null and points to an existing file under `input/` (markitdown rendering for Supported-via-MCP; frozen vision description for the other two).
- For every row with `tier ∈ {"Native-text", "Unsupported"}`, `converted_sibling` is `null`.
- `schema_version` is `1`. `generated_at` parses as ISO-8601 UTC. `target` equals the caller-supplied `inherited_target` (which is `null` on create, or one of `"prototype"` / `"application"` on refresh).
- The manifest is written via `Write` and verified via `framework/skills/verify-artifact-write.md` with `expected_min_bytes` set to the byte length of the smallest legal manifest (a manifest with `rows: []` is the lower bound — the input-handler only reaches this skill when `input/` is non-empty, but the schema permits it).

After self-validation passes, the input-handler inspects the manifest to decide whether to surface `RF-03 input_no_supported_files`: if every row has `tier: "Unsupported"`, fire `RF-03`. Otherwise hand back to the calling orchestrator.

## Anti-Patterns

- Do not write the manifest as markdown or any format other than the JSON schema above. Consumers parse with `Read` + JSON-decode; markdown tables are fragile to hand-editing.
- Do not omit Unsupported rows. The forensic record is the point — the consultant can see exactly what a consumer could not consume.
- Do not include rows for `*.converted.md` siblings. They are referenced from their parent row's `converted_sibling` field, not as separate entries.
- Do not compute `sha256` over the `*.converted.md` sibling. The manifest's `sha256` is on the original — that is what `check-manifest-freshness.md` compares against to detect input drift.
- Do not write the manifest before every per-file conversion has completed (or failed). Partial manifests cause consumers to read stale or absent siblings.
- Do not skip `verify-artifact-write.md` on the manifest write. A truncated manifest masquerades as a successful write and the consumer's first `Read` produces a JSON parse error far from the failure site.
- Do not *originate* a `target` value. The build-target *selection* (origination) happens at the requirements orchestrator's Step 1b via `framework/skills/set-build-target.md`; this skill must never anticipate or infer the choice from inputs, file content, or any heuristic. The only path by which this skill emits a non-null `target` is *preservation* via the caller-supplied `inherited_target` parameter — and even then, the skill must verify the value matches one of the three legal forms (`"prototype"` / `"application"` / `null`) before emitting. `/generate-prd`, `/analyse-inputs`, and `/review-inputs` invocations leave `target: null` on disk (their orchestrators never invoke `set-build-target.md` and they never pass a non-null `inherited_target` on a first build).
- Do not hardcode the manifest path. `manifest_path` is an input parameter; the skill must work unchanged when a future pipeline passes a path other than `requirements/source-manifest.json`.
