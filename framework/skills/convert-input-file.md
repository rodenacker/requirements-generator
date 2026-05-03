# convert-input-file.md

**Purpose:** Convert one `Supported-via-MCP` input file into a markdown sibling the drafter can read. Office formats (`.docx`, `.xlsx`, `.pptx`) and PDFs are routed through `mcp__markitdown__convert_to_markdown` with a `file:///` URI. The original is left in place; the converted sibling is written next to it under `input/` with the suffix `.converted.md`. Each conversion is one call; the skill is invoked once per `Supported-via-MCP` row in the in-progress manifest.

**Inputs:**
- A single `Supported-via-MCP` file path under `input/` (e.g. `input/spec.docx`).
- The MCP tool `mcp__markitdown__convert_to_markdown` must be present in the available tool list — guaranteed by the input-handler having run `framework/skills/preflight-mcp.md` first.

**Outputs:**
- A sibling file at `input/<basename>.converted.md` containing the markdown rendering.
- A `conversions_applied` string for the manifest row, in the form `"markitdown-mcp"` plus optional sub-tags separated by `; ` — for example `"markitdown-mcp; embedded-images-extracted"`, `"markitdown-mcp; tables-flattened"`, or `"failed — encrypted"`.

**Used by:**
- `framework/agents/requirements-input-handler.md` — called once per row that classifies as `Supported-via-MCP`.

## Procedure

1. Build the file URI: `file:///` followed by the absolute path of the input file. On Windows, normalise backslashes to forward slashes.
2. Call `mcp__markitdown__convert_to_markdown` with the URI. The tool returns a markdown string.
3. Determine the sibling path: replace the original file's extension with `.converted.md`. For `input/spec.docx` the sibling is `input/spec.converted.md`. If a file already exists at the sibling path, overwrite it — re-runs are idempotent.
4. `Write` the markdown string to the sibling path.
5. Compute sha256 of the markdown bytes and call `framework/skills/verify-artifact-write.md` with `path: <sibling>`, `expected_sha256: <hash>`, `expected_min_bytes: 1`. On `RF-04 trigger`, the input-handler halts per the registry; this skill returns control without writing a manifest row.
6. On `pass`, return `conversions_applied: "markitdown-mcp"` (plus any applicable sub-tags) to the caller. The caller writes the manifest row.

## Sub-tag conventions

The `conversions_applied` string is consultant-facing and forensic; the input-handler embeds it in the manifest row. Sub-tags are append-only — add new ones rather than rephrasing existing ones.

- `markitdown-mcp` — the file was successfully converted via markitdown. Always present on a successful conversion.
- `embedded-images-extracted` — markitdown extracted image captions or summaries from images embedded in the source. Append when applicable.
- `tables-flattened` — markitdown rendered tables as text rather than markdown tables (typical for `.xlsx` with merged cells). Append when applicable.
- `failed — encrypted` — markitdown errored out because the source is password-protected. The sibling is not written; the input-handler reclassifies the row to `tier: "Unsupported"` and skips it.
- `failed — corrupt` — markitdown errored out for any other reason. Same handling as encrypted.

## Refusal handling (RF-02)

This skill does not surface `RF-02 input_format_unsupported` directly. `RF-02` is a manifest-level pause: it fires when the manifest contains at least one `Unsupported` row alongside non-Unsupported rows. A conversion failure here (`failed — encrypted` or `failed — corrupt`) demotes a single row from `Supported-via-MCP` to `Unsupported`, which the manifest writer then catches as `RF-02` if applicable.

## Self-validation

- The sibling exists at `input/<basename>.converted.md` after a successful conversion. Its byte size is non-zero.
- The sha256 returned to the caller matches the bytes on disk (verified via `verify-artifact-write.md`).
- On a failed conversion, the sibling is **not** written. The caller is told via the `conversions_applied` string; the original file remains in place, untouched.
- The original file under `input/` is never modified. The skill is read-only on the source.

## Anti-Patterns

- Do not call this skill on a tier other than `Supported-via-MCP`. Native-text and Native-multimodal files are `Read` directly by the drafter; passing them through markitdown loses fidelity (text gets re-flowed; images lose multimodal context).
- Do not call this skill before `preflight-mcp.md` has confirmed the tool is available. Doing so risks a runtime failure inside the conversion call rather than a clean `RF-01` surface.
- Do not invent sibling paths outside `input/`. The drafter's manifest contract assumes `converted_sibling` is co-located with the original under `input/`; placing the sibling under `requirements/` or `framework/state/` breaks rerun detection (input content-hash deltas) and the orchestrator's reset procedure.
- Do not skip `verify-artifact-write.md`. The conversion's markdown string can be megabytes for a `.pptx` deck; truncated writes are real and silent.
- Do not append free-text to `conversions_applied`. Only the documented sub-tags. Free-text breaks downstream parsing.
