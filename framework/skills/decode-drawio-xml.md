# decode-drawio-xml.md

**Purpose:** Fallback reader for a single `.drawio` input when the **primary** path (render to raster via the `drawio` desktop CLI, then vision-describe) is unavailable — the `drawio` binary is absent, or `framework/skills/render-visual-to-raster.md` returned `failed — render`. Instead of demoting the file to `Unsupported`, this skill reads the diagram's **mxGraph XML** directly and writes the same frozen description sibling the render path would have produced, so a `.drawio` is never lost merely because draw.io Desktop isn't installed. This is a **lower-fidelity** path: explicit XML content (labels, edge endpoints, edge-style cardinality tokens) is read faithfully, but anything that depends on visual geometry (lane membership, grouping by position) is only *inferred* and is marked accordingly.

The primary render path remains preferred (geometry is read by vision, not guessed). This skill is the graceful-degradation tier — see `framework/shared/setup-instructions/visual-render.md`.

**Inputs:**
- `vector_path` — the `.drawio` file under `input/` to decode.
- `sibling_path` — the description sibling to write: `input/<filename-with-ext>.converted.md` (append-extension form, e.g. `flow.drawio.converted.md`), matching the render path's sibling exactly so downstream Read-path resolution is identical.

**Outputs:** exactly one of:
- `ok` — the sibling at `sibling_path` was written (template fully populated, marker discipline applied) and verified via `framework/skills/verify-artifact-write.md`. The input-handler retains the row's `tier: "Vector-renderable"` and records `conversions_applied: "drawio-xml-fallback[; multi-page-source-first-page-only]"`.
- `failed — render` — the file could not be decoded (no recoverable mxGraph XML, decompression failed, or the verify failed). The input-handler demotes the row to `Unsupported` with `conversions_applied: "failed — render"` (same bucket as a render failure — the vector could not be converted by any path).

**Used by:**
- `framework/agents/input-handler.md` — step 5, `Vector-renderable` dispatch, `.drawio` branch only, when `drawio` is not on PATH or the render returned `failed — render`. Shared across all four input-handler-using pipelines.

## Procedure

1. **Recover the mxGraph XML.** `Read` `vector_path` as text.
   - If it contains `<mxGraphModel` directly, the diagram XML is stored uncompressed — use it as-is.
   - Otherwise the diagram content is the compressed payload inside `<diagram …>…</diagram>` (draw.io's default save: `pako` raw-deflate → base64 → `encodeURIComponent`). Decode the **first** `<diagram>` element's text with a Node one-liner (Node is a base dependency):
     ```
     node -e "const z=require('zlib');const b=Buffer.from(process.argv[1],'base64');process.stdout.write(decodeURIComponent(z.inflateRawSync(b).toString('binary')))" "<base64-payload>"
     ```
     The result is the `<mxGraphModel>` XML. If a file has more than one `<diagram>` (multi-page), decode only the first/primary page and remember to append `multi-page-source-first-page-only`.
   - If neither form yields parseable `<mxGraphModel>` XML, return `failed — render`.
2. **Read the structure from the XML, not from geometry.** mxGraph stores each shape as an `<mxCell vertex="1" value="<label>" style="…">` with an `<mxGeometry x y width height>`; each connector as `<mxCell edge="1" source="<id>" target="<id>" value="<label>" style="…">`. Extract: vertex labels (entity/field/node names), edge source→target pairs and edge labels, and edge-style tokens that carry meaning (e.g. `startArrow=ERmany` / `endArrow=ERone` for ERD cardinality; `edgeStyle`/arrow direction for flow direction).
3. **Populate `framework/assets/template-visual-description.md` top-to-bottom**, exactly as the render path's `describe-visual-input.md` does — same sections, same closed marker set — so the sibling is indistinguishable in shape to downstream consumers. Set the `Rendered from vector?` row to `no — decoded from .drawio XML (geometry inferred)`.
4. **Apply the fidelity guardrail** (the rule that protects the citation guarantee):
   - **Explicit XML content is authoritative → `[SRC: <filename>]`:** vertex `value` labels (entity / field / node names), edge `source`/`target` connectivity, edge labels, and cardinality/direction read from explicit edge-style tokens. These are *read*, not guessed.
   - **Spatially-inferred structure is not reliable from XML → `[AI-SUGGESTED: AI-NNN | blocking]`:** swim-lane / group membership, containment, or any relationship deduced from x/y position rather than an explicit parent/edge. Numbered per-description from `AI-001`; `blocking` when it would materially change a downstream requirement (e.g. which actor owns a step). Itemise each in the template's "Ambiguities" section as a resolver-ready question.
   - Never assert a property as real data unless an explicit `value` label shows it. The closed-property-set discipline is unchanged.
5. **Write** the populated template to `sibling_path` and verify via `framework/skills/verify-artifact-write.md`. On verify failure, return `failed — render`; otherwise return `ok`.

## Self-validation

- The sibling is written to `sibling_path` (append-extension form), never under a different name, never overwriting the original `.drawio`.
- The original `.drawio` at `vector_path` is read-only; this skill never modifies or deletes it.
- No `{{placeholder}}` remains in the populated template; every section is populated or carries the empty sentinel.
- Every Tier-A item is either `[SRC: <filename>]` (explicit XML content) or `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` (geometry-inferred). Only the two canonical markers appear — no ad-hoc tags.
- The `Rendered from vector?` row records the XML-decode provenance (geometry inferred), so a reader can see this is the lower-fidelity path.

## Anti-Patterns

- Do not present geometry-inferred structure (lane membership, grouping) as `[SRC]`. The whole point of the guardrail is that the XML proves connectivity and labels, not visual grouping — assert the latter only as `[AI-SUGGESTED]`.
- Do not run this skill when the `drawio` binary is present and the render succeeded. The render-then-vision path is higher fidelity; this is the fallback, invoked by the input-handler only on binary-absence or render failure.
- Do not fabricate fields. A vertex with no `value` is an unlabelled node, not an entity with invented properties — record it as unlabelled and `[AI-SUGGESTED]` if its role matters.
- Do not write the raster or any scratch file. This path has no raster; it reads XML and writes one sibling.
- Do not decode pages beyond the first. Multi-page `.drawio` renders/decodes its primary page only in MVP (mirrors `render-visual-to-raster.md`); append `multi-page-source-first-page-only` so the limitation is on record.
- Do not invent a new sibling-naming form or a new manifest tier. The sibling is the same `<filename-with-ext>.converted.md`; the tier stays `Vector-renderable`; only `conversions_applied` distinguishes the fallback (`drawio-xml-fallback`).
