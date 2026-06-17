# Vector Renderer — Setup Instructions

Install copy referenced by `RF-01 dependency_missing` in `framework/shared/refusal-registry.md`. Surfaced to the consultant when the input-handler's step-4b preflight (`framework/skills/preflight-cli.md`) finds **no** vector-renderer binary on `PATH` and at least one input file's tier is `Vector-renderable` (`.svg`, `.drawio`, `.vsdx`).

The renderer turns a vector diagram into a raster so the system can produce a faithful textual description of it. Without it, `.svg`/`.drawio`/`.vsdx` files are recorded as `Unsupported` for the run (their geometry — ERD cardinality, flow direction, swim-lane partitioning — cannot be reliably read from raw XML).

You only need the renderer(s) for the formats you actually drop in `input/`. The preflight succeeds if **any** suitable binary is found.

## Install

Pick per the formats you use (any one satisfies its row):

- **SVG** — Inkscape (recommended) or librsvg:
  - Inkscape: download from https://inkscape.org and ensure `inkscape` is on `PATH`. Verify: `inkscape --version`.
  - librsvg: provides `rsvg-convert`. On Windows, install via MSYS2/Chocolatey (`choco install rsvg-convert`) or use the binaries bundled with many GTK distributions.
- **.drawio** — draw.io Desktop CLI: install draw.io Desktop from https://github.com/jgraph/drawio-desktop/releases; ensure `drawio` is on `PATH`. Verify: `drawio --version`.
- **.vsdx** (Visio) — LibreOffice (best-effort): install from https://www.libreoffice.org and ensure `soffice` is on `PATH`. Verify: `soffice --version`.

After installing, restart Claude Code so a fresh `PATH` is picked up, then re-invoke the pipeline. The renderers are plain CLI binaries — no `.mcp.json` entry is required.

## Verify

After restarting Claude Code, the input-handler's step-4b preflight runs automatically on the next pipeline invocation whenever a `Vector-renderable` file is present. To verify out-of-band, confirm at least one of the binaries resolves:

- `inkscape --version` (or `rsvg-convert --version`) for SVG
- `drawio --version` for `.drawio`
- `soffice --version` for `.vsdx`

## Troubleshooting

- **`<binary>: command not found` after install** — the install dir is not on `PATH`. Add it (e.g. Inkscape's `bin/`) and restart Claude Code; the session caches `PATH` at start.
- **Render produces a tiny/blurry raster and the description misses labels** — increase the export width in `framework/skills/render-visual-to-raster.md` (target ≥ 1500 px on the long edge).
- **`.vsdx` fails to render (LibreOffice)** — `.vsdx` support is **best-effort**: complex Visio stencils or password-protected files may not convert. If LibreOffice errors, the row demotes to `Unsupported` (`conversions_applied: "failed — render"`). Workaround: open the file in Visio/LibreOffice and export it to `.svg` or `.png` yourself, then drop that into `input/` instead.
- **`.drawio` renders only the first page** — multi-page `.drawio`/`.vsdx` sources render their primary page only in MVP. Export each page separately if you need all of them.

## Uninstall

Uninstall the renderer(s) via the same channel you installed them (the OS package manager or the app's uninstaller). After uninstall, re-running a pipeline with any `Vector-renderable` file in `input/` will fire `RF-01` again at step 4b.
