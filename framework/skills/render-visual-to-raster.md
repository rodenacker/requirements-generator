# render-visual-to-raster.md

**Purpose:** Render one `Vector-renderable` input file (`.svg`, `.drawio`, `.vsdx`) to a **temporary raster** (PNG) so that `framework/skills/describe-visual-input.md` can vision-describe it. Vector diagrams encode their meaning in geometry (crow's-foot cardinality, arrow direction, lane partitioning) that is lost when their XML is read as text — rendering to a raster recovers the visual semantics for the describer. The renderer is an external CLI binary, gated upstream by `framework/skills/preflight-cli.md` (input-handler step 4b). The original vector file is left untouched; the raster is scratch, consumed immediately and not registered in the manifest.

**Inputs:**
- `vector_path` — the `.svg`/`.drawio`/`.vsdx` file under `input/` to render.
- `renderer` — the resolved CLI binary name(s) returned by `framework/skills/preflight-cli.md` (e.g. `inkscape`, `rsvg-convert`, `drawio`, `soffice`). Guaranteed present by the preflight having run first.

**Outputs:**
- `raster_path` — a temporary PNG at `framework/state/.visual-render-scratch/<filename-with-ext>.png`, consumed by `describe-visual-input.md` and then removed. Never written under `input/` (it must not be enumerated as a new input).
- A status: `ok` (raster produced, non-empty) or `failed — render` (the renderer errored or produced an empty/zero-byte raster). On `failed — render` the input-handler demotes the row's `tier` to `Unsupported`.

**Used by:**
- `framework/agents/input-handler.md` — step 5, once per `Vector-renderable` row, immediately before `describe-visual-input.md`. Shared across all four input-handler-using pipelines.

## Procedure

1. Choose the renderer command by the vector file's extension and the available `renderer` binary, per the table below. Prefer the first available binary in the table row.
2. Ensure the scratch dir `framework/state/.visual-render-scratch/` exists (create lazily). Build the output path `framework/state/.visual-render-scratch/<filename-with-ext>.png`.
3. Shell out (PowerShell on Windows; the call operator `&` for binaries with spaced paths) to render to the output PNG at a legible resolution (target ≥ 1500 px on the long edge so small labels remain readable to vision; e.g. Inkscape `--export-width=1600`).
4. Confirm the output PNG exists and is non-zero bytes. If so, return `ok` with `raster_path`. Otherwise return `failed — render`.
5. (Caller responsibility) after `describe-visual-input.md` has read the raster, the input-handler removes the scratch PNG. The scratch dir is also swept by the `/requirements` orchestrator's Reset procedure.

## Per-format render command table

Commands are reference defaults; the concrete toolchain is documented in `framework/shared/setup-instructions/visual-render.md`. First available binary per row wins.

| Extension | Preferred renderer(s) | Reference command (Windows / PowerShell) |
|---|---|---|
| `.svg` | `inkscape`, `rsvg-convert` | `inkscape "<in>.svg" --export-type=png --export-filename="<out>.png" --export-width=1600` — or — `rsvg-convert -w 1600 "<in>.svg" -o "<out>.png"` |
| `.drawio` | `drawio` (drawio-desktop CLI) | `drawio --export --format png --width 1600 --output "<out>.png" "<in>.drawio"` |
| `.vsdx` | `soffice` (LibreOffice) | `soffice --headless --convert-to png --outdir "<scratch-dir>" "<in>.vsdx"` (best-effort; see Risks in setup-instructions) |

A multi-page source (multi-page `.drawio`/`.vsdx`) renders its first/primary page; note `multi-page-source-first-page-only` is appended by the describer's `conversions_applied` if more pages exist. (Per-page rendering is a future enhancement, not MVP.)

## Refusal handling

- This skill surfaces **no** refusal directly. Renderer **absence** is handled upstream by `preflight-cli.md` → `RF-01` at input-handler step 4b. Renderer **failure at render time** (corrupt file, unsupported variant, `.vsdx` LibreOffice can't open) returns `failed — render`, which the input-handler treats as a per-file demotion to `Unsupported` (mirroring `convert-input-file.md`'s `failed — corrupt`). The manifest's `RF-02`/`RF-03` logic then applies at the manifest level.

## Self-validation

- The output raster is written under `framework/state/.visual-render-scratch/`, never under `input/`.
- On `ok`, the raster exists and is non-zero bytes.
- On `failed — render`, no partial raster is left behind (a zero-byte output is deleted), and the original vector under `input/` is untouched.
- The skill never modifies the original vector file.

## Anti-Patterns

- Do not write the raster under `input/`. A raster under `input/` would be enumerated as a new `Native-multimodal` input on the next run, creating a phantom file and a second description. Scratch lives under `framework/state/`.
- Do not register the raster in the manifest. Only the original vector gets a row; its `converted_sibling` is the description, not the raster. The raster is transient.
- Do not call this skill before `preflight-cli.md` has confirmed a renderer. Doing so risks a runtime failure inside the render call rather than a clean `RF-01` surface.
- Do not describe the raster here. Rendering and describing are separate skills; this one produces a raster and returns. `describe-visual-input.md` owns the vision step.
- Do not hardcode a single renderer. Pick by extension and availability from the table; the toolchain varies by machine and is configured in `visual-render.md`.
