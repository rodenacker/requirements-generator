# Vector Renderer — Setup Instructions

Install copy referenced by `RF-01 dependency_missing` in `framework/shared/refusal-registry.md`. Surfaced to the consultant when the input-handler's step-4b preflight (`framework/skills/preflight-cli.md`) finds **no** vector-renderer binary on `PATH` and at least one input file's tier is `Vector-renderable` (`.svg`, `.drawio`, `.vsdx`).

The renderer turns a vector diagram into a raster so the system can produce a faithful textual description of it. Without it, `.svg`/`.vsdx` files are recorded as `Unsupported` for the run (their geometry — ERD cardinality, flow direction, swim-lane partitioning — cannot be reliably read from raw XML).

**`.drawio` degrades gracefully — it does not need a renderer to be usable.** When `drawio` is absent (or a render fails), the input-handler falls back to reading the diagram's mxGraph XML directly (`framework/skills/decode-drawio-xml.md`): explicit content — node/entity labels, edge connectivity, and cardinality/direction read from edge-style tokens — is captured authoritatively, while anything that depends on visual geometry (lane membership, positional grouping) is flagged as inferred (`[AI-SUGGESTED]`) rather than asserted. Installing draw.io Desktop is still preferred (the rendered-then-vision path reads geometry directly, at full fidelity), but a missing draw.io no longer loses the file.

You only need the renderer(s) for the formats you actually drop in `input/`. The preflight succeeds if **any** suitable binary is found.

## Install

**Fastest for `.drawio`:** `/setup drawio` installs draw.io Desktop if needed and — the part that trips people up on Windows — writes the `drawio` PATH shim for you (and adds its folder to your user PATH), then a Claude Code restart makes `drawio` resolve. For `.svg` / `.vsdx`, `/setup inkscape` / `/setup libreoffice` install those renderers. The manual steps below are the equivalents.

Pick per the formats you use (any one satisfies its row):

- **SVG** — Inkscape (recommended) or librsvg:
  - Inkscape: download from https://inkscape.org and ensure `inkscape` is on `PATH`. Verify: `inkscape --version`.
  - librsvg: provides `rsvg-convert`. On Windows, install via MSYS2/Chocolatey (`choco install rsvg-convert`) or use the binaries bundled with many GTK distributions.
- **.drawio** — draw.io Desktop CLI. On Windows, install via winget (recommended):

  ```
  winget install --exact --id JGraph.Draw
  ```

  On macOS/Linux, or to avoid winget, download draw.io Desktop from https://github.com/jgraph/drawio-desktop/releases. After installing, confirm it resolves under the name the pipeline probes for — `drawio` — with `drawio --version`. On Windows the executable ships as `draw.io.exe` (with dots), so a successful install can still leave `drawio` unresolved; see **Troubleshooting → draw.io installed but RF-01 still fires** below.
- **.vsdx** (Visio) — LibreOffice (best-effort): install from https://www.libreoffice.org and ensure `soffice` is on `PATH`. Verify: `soffice --version`.

After installing, restart Claude Code so a fresh `PATH` is picked up, then re-invoke the pipeline. The renderers are plain CLI binaries — no `.mcp.json` entry is required.

## Verify

After restarting Claude Code, the input-handler's step-4b preflight runs automatically on the next pipeline invocation whenever a `Vector-renderable` file is present. To verify out-of-band, confirm at least one of the binaries resolves:

- `inkscape --version` (or `rsvg-convert --version`) for SVG
- `drawio --version` for `.drawio`
- `soffice --version` for `.vsdx`

The step-4b preflight tests presence with `Get-Command <name>` (PowerShell) / `command -v <name>` (Bash) for `drawio`, `inkscape`, `rsvg-convert`, `soffice` — so each binary must be resolvable under *exactly* that name, not merely installed somewhere on disk.

## Troubleshooting

- **`<binary>: command not found` after install** — the install dir is not on `PATH`. Add it (e.g. Inkscape's `bin/`) and restart Claude Code; the session caches `PATH` at start.
- **draw.io installed but RF-01 still fires / `drawio --version` is "not recognized" (Windows)** — the draw.io Desktop executable is named `draw.io.exe` (with dots), but the preflight wants a command named exactly `drawio`. winget often registers a `DrawIO` shim on `PATH` for you (Windows command lookup is case-insensitive, so `Get-Command drawio` resolves) — **check first** with `Get-Command drawio`. If it comes back empty, drop a one-line `drawio.cmd` shim into a folder already on `PATH` (the winget Links folder usually qualifies). From PowerShell:

  ```powershell
  # locate the installed executable
  $exe = Get-ChildItem "$env:LOCALAPPDATA\Programs","$env:ProgramFiles","${env:ProgramFiles(x86)}" `
           -Recurse -Filter draw.io.exe -ErrorAction SilentlyContinue |
           Select-Object -First 1 -ExpandProperty FullName
  # write a shim named `drawio` onto PATH
  "@echo off`r`n`"$exe`" %*" | Set-Content "$env:LOCALAPPDATA\Microsoft\WinGet\Links\drawio.cmd" -Encoding ascii
  ```

  (Installed manually instead of via winget? Put `drawio.cmd` in any directory already on your `PATH` and point it at your `draw.io.exe`.) Then restart Claude Code (the session caches `PATH` at start) and re-invoke the pipeline; `Get-Command drawio` should now resolve.
- **Render produces a tiny/blurry raster and the description misses labels** — increase the export width in `framework/skills/render-visual-to-raster.md` (target ≥ 1500 px on the long edge).
- **`.vsdx` fails to render (LibreOffice)** — `.vsdx` support is **best-effort**: complex Visio stencils or password-protected files may not convert. If LibreOffice errors, the row demotes to `Unsupported` (`conversions_applied: "failed — render"`). Workaround: open the file in Visio/LibreOffice and export it to `.svg` or `.png` yourself, then drop that into `input/` instead.
- **`.drawio` renders only the first page** — multi-page `.drawio`/`.vsdx` sources render their primary page only in MVP. Export each page separately if you need all of them.

## Uninstall

Uninstall the renderer(s) via the same channel you installed them (the OS package manager or the app's uninstaller). After uninstall, re-running a pipeline with any `Vector-renderable` file in `input/` will fire `RF-01` again at step 4b.
