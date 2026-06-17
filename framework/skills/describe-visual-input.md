# describe-visual-input.md

**Purpose:** Produce **one frozen, structured, citable textual description** of a single visual input — a UI mock-up, wireframe, screenshot, ERD, flow chart, use-case diagram, or the like — as a markdown sibling that every downstream input-consumer reads **instead of** re-interpreting the pixels. This is the "interpret-once" contract: the visual is interpreted a single time at ingestion, the result is reviewable and correctable by the consultant, and the `/requirements` drafter, the `/generate-prd` drafter, every `/analyse-inputs` analyser, and every `/review-inputs` reviewer consume the same text. The original is left in place; the sibling is written next to it under `input/` with the suffix `.converted.md` (append-extension form). Each description is one invocation; the skill is invoked once per `Native-multimodal` row, and once per `Vector-renderable` row after `framework/skills/render-visual-to-raster.md` has produced a raster.

The skill is the **bounded interpretation** the input-handler delegates (see `framework/agents/input-handler.md` Persona). Its discipline is fixed by the template it populates (`framework/assets/template-visual-description.md`) and the anti-patterns below — it transcribes and structures what the visual *shows*; it does not mine requirements, infer business intent, or invent data not visible.

**Inputs:**
- `image_path` — the raster image to vision-read. For a `Native-multimodal` row this is the `original_path`. For a `Vector-renderable` row this is the **temporary raster** returned by `framework/skills/render-visual-to-raster.md`.
- `original_path` — the `input/` file the sibling is named after (the consultant-dropped original). For raster rows this equals `image_path`; for vector rows it is the `.svg`/`.drawio`/`.vsdx` original, **not** the temporary raster.
- `source_kind` — `"raster"` or `"rendered-vector"`. Drives the `conversions_applied` sub-tags.
- `render_tool` — the renderer name (e.g. `inkscape`, `drawio`, `libreoffice`), present only when `source_kind == "rendered-vector"`.
- The template asset `framework/assets/template-visual-description.md` (read once, populated top-to-bottom).
- No external/MCP tool is required — Claude's vision is native via `Read`.

**Outputs:**
- A sibling file at `input/<filename-with-ext>.converted.md` (e.g. `input/wireframe-login.png.converted.md`, `input/erd.svg.converted.md`) containing the populated description.
- A `conversions_applied` string for the manifest row: `"vision-described"` plus optional sub-tags separated by `; ` — for example `"vision-described; ui-mockup"`, `"vision-described; erd; rendered-from-vector; render-tool=inkscape"`, or the failure form `"failed — vision"`.

**Used by:**
- `framework/agents/input-handler.md` — step 5, once per `Native-multimodal` row (directly) and once per `Vector-renderable` row (after render). Shared across `/requirements`, `/generate-prd`, `/analyse-inputs`, and `/review-inputs` because all four call the input-handler.

## Procedure

1. Determine the sibling path: append `.converted.md` to the **full original filename** (extension included). For `input/wireframe.png` the sibling is `input/wireframe.png.converted.md`; for `input/erd.svg` it is `input/erd.svg.converted.md`. The append-extension form (not extension-replace) prevents a visual from colliding with a same-stem Office file's sibling (`chart.png.converted.md` vs `chart.converted.md`). If a file already exists at the sibling path, the **input-handler's step-5 idempotency guard** decides whether this skill is even invoked — this skill always (over)writes when invoked.
2. `Read` `image_path` to surface the image as multimodal vision input.
3. `Read` `framework/assets/template-visual-description.md` and populate it **top-to-bottom in one pass**, classifying the diagram type and filling every section. Apply the marker discipline exactly:
   - Cite every Tier-A (*what*) item with `[SRC: <original-filename>]` — the original's filename, not the temp raster's.
   - Mark inferred or low-confidence items with `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]`. **Every extracted data property/field that may be placeholder rather than real data carries `[AI-SUGGESTED: AI-NNN | blocking]`** — see the template's property section.
   - Use no marker outside the canonical set (`[SRC]`, `[AI-SUGGESTED]`). Do **not** invent a `[CONFIDENCE]` marker.
   - Leave no `{{placeholder}}` unfilled and no section blank (use the template's empty-section sentinel where a section genuinely does not apply to this diagram type).
4. `Write` the populated description to the sibling path.
5. Compute sha256 of the description bytes and call `framework/skills/verify-artifact-write.md` with `path: <sibling>`, `expected_sha256: <hash>`, `expected_min_bytes: 256` (a defensive floor that exceeds an unpopulated template; a truncated description is a real and silent failure). On `RF-04 trigger`, the input-handler halts per the registry; this skill returns control without a successful row.
6. On `pass`, return `conversions_applied: "vision-described"` plus the applicable sub-tags (diagram-type tag; `rendered-from-vector` + `render-tool=<name>` when `source_kind == "rendered-vector"`) to the caller. The caller (input-handler) writes the manifest row with `tier` retained and `converted_sibling` set to the sibling path.

## Sub-tag conventions

The `conversions_applied` string is consultant-facing and forensic; the input-handler embeds it in the manifest row. Sub-tags are append-only — add new ones rather than rephrasing existing ones.

- `vision-described` — the visual was successfully described via Claude vision. Always present on success.
- Diagram-type tag (exactly one): `ui-mockup` | `wireframe` | `screenshot` | `erd` | `flowchart` | `use-case-diagram` | `sequence-diagram` | `activity-diagram` | `state-diagram` | `org-chart` | `dashboard` | `whiteboard` | `other-visual`. The describer's classification of what the visual is.
- `rendered-from-vector` — the described raster was produced by `render-visual-to-raster.md` from an `.svg`/`.drawio`/`.vsdx` original. Append only when `source_kind == "rendered-vector"`.
- `render-tool=<name>` — the renderer used (e.g. `render-tool=inkscape`). Append only alongside `rendered-from-vector`.
- `failed — vision` — the describer could not interpret the image (unreadable, blank, or vision returned nothing usable). The sibling is **not** written; the input-handler reclassifies the row to `tier: "Unsupported"` and skips it.

## Refusal handling

- **RF-04 (write-verify):** surfaced via `verify-artifact-write.md` at step 5, exactly as `convert-input-file.md` does. Hard halt per `framework/shared/refusal-registry.md > RF-04`.
- **No RF for vision availability:** Claude vision is native, so there is no preflight and no `RF-01` for this skill. (Vector rows do gate a renderer via `RF-01` — but that gate lives in the input-handler's step 4b / `render-visual-to-raster.md`, not here.)
- **Description failure (`failed — vision`)** is a per-file demotion, not a refusal pause — it mirrors `convert-input-file.md`'s `failed — corrupt` handling. The manifest's `RF-02`/`RF-03` logic then applies at the manifest level as usual.

## Self-validation

- The sibling exists at `input/<filename-with-ext>.converted.md` after a successful description. Its byte size is ≥ 256.
- The sha256 returned to the caller matches the bytes on disk (verified via `verify-artifact-write.md`).
- Every `{{placeholder}}` in the template was replaced; no section was left blank (empty sections carry the template's explicit sentinel).
- Every Tier-A (*what*) item carries a `[SRC: <original-filename>]` citation naming the **original** file (not the temporary raster). No marker outside `[SRC]` / `[AI-SUGGESTED]` appears.
- On a failed description, the sibling is **not** written; the caller is told via `conversions_applied: "failed — vision"`; the original under `input/` is untouched.
- The original consultant-dropped file is never modified. For a vector row, the temporary raster is the skill's scratch input; the skill does not leave it under `input/`.

## Anti-Patterns

- Do not call this skill on a tier other than `Native-multimodal` or (post-render) `Vector-renderable`. Native-text is read directly; Supported-via-MCP goes through `convert-input-file.md`.
- Do not mine requirements or infer business intent. Describe what the visual *shows* (objects, fields, controls, flows, states, actors), structured by the template's *what/how* split. Interpretation of *why* and translation into requirements is downstream work (the drafter, the analysers, the reviewers).
- Do not invent data properties to make a form or table look complete. A field visible only as placeholder/lorem text is flagged `[AI-SUGGESTED: AI-NNN | blocking]`, never asserted as a real `[SRC]`-cited property. This is the load-bearing guard against fabricated requirements entering the closed property set downstream.
- Do not invent a `[CONFIDENCE]` (or any other) marker. Express uncertainty through the canonical `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` channel only — it routes to the resolver. Inventing a marker widens the framework-wide marker contract.
- Do not name the sibling after the temporary raster. The sibling and every `[SRC: …]` citation use the **original** consultant-dropped filename, so provenance points at what the consultant actually provided.
- Do not skip `verify-artifact-write.md`. A populated description can be kilobytes; truncated writes are real and silent.
- Do not append free-text to `conversions_applied`. Only the documented sub-tags. Free-text breaks downstream parsing.
- Do not overwrite a sibling the input-handler's idempotency guard chose to keep. This skill is only invoked when the guard decided to (re)generate; it must not be called to "refresh" an unchanged visual, because that would discard consultant edits.
