# Markitdown MCP — Setup Instructions

Install copy referenced by `RF-01 dependency_missing` in `framework/shared/refusal-registry.md`. Surfaced to the consultant when the input-handler's preflight does not find `mcp__markitdown__convert_to_markdown` in the available tool list, **or** when it is found but an Office/PDF conversion fails because the format's converter is missing.

## Fastest path — let Claude do it

```
/setup markitdown
```

`/setup` runs `framework/tools/setup-environment.ps1 -Component markitdown`, which installs the converters and the MCP server in the right order, tests every converter, and reports. Restart Claude Code afterwards so the MCP server reloads. Everything below is the manual equivalent.

## Install (manual)

Python 3.10+ is required. Run these into the same Python environment Claude Code's MCP launcher resolves `markitdown-mcp` from:

```
pip install "markitdown[docx,pptx,xlsx,xls,pdf,outlook]"
pip install --no-deps markitdown-mcp==0.0.1a4
pip install "mcp~=1.8.0"
```

- **Line 1** installs the markitdown library **with its Office/PDF converters** — `python-pptx`, `openpyxl`, `xlrd`, `pdfminer.six`, `mammoth`, `olefile`. Without the scoped extras you get bare markitdown, which converts only plain formats and **silently fails on `.pptx` / `.xlsx` / `.xls` / `.pdf`**.
- **Lines 2–3** install the MCP server. The `--no-deps` is deliberate: `markitdown-mcp==0.0.1a4` declares a dependency on `markitdown[all]`, whose `youtube-transcript-api` / `onnxruntime` pins have **no wheels on newer Python (e.g. 3.14)**, so a plain `pip install markitdown-mcp` aborts with `ResolutionImpossible`. Installing it `--no-deps` and adding its real runtime dep (`mcp`) separately sidesteps that — markitdown itself is already present from line 1.

Do **not** use `markitdown[all]` or `--upgrade` here. The repo's `.mcp.json` already declares `markitdown-mcp` as an MCP server; no further configuration is required. After installing, **restart Claude Code** so the MCP server is loaded with the new converters.

## Verify

After restarting, the input-handler's preflight runs automatically on the next pipeline invocation. To verify out-of-band:

1. Confirm every Office/PDF converter imports:
   ```
   python -c "import mammoth, pptx, openpyxl, xlrd, pdfminer; print('office converters OK')"
   ```
2. Confirm `markitdown-mcp` is on `PATH`: `markitdown-mcp --help`.
3. Confirm Claude Code lists the MCP server: `mcp__markitdown__convert_to_markdown` should appear in the available tool list.

`/setup markitdown` (or `/setup`) re-runs checks 1–2 for you and reports a status row; check 3 is what `/setup` adds on top (only Claude can see the live tool list).

## Troubleshooting

- **`ResolutionImpossible` mentioning `markitdown[all]`, `youtube-transcript-api`, or `onnxruntime`** — you installed `markitdown-mcp` (or `markitdown[all]`) without `--no-deps` on a Python the `[all]` pins don't cover. Use the three-line sequence above; never `markitdown[all]`.
- **`.pptx`/`.xlsx`/`.pdf` convert to nothing or error, but `.docx` works** — the converters are incomplete (only `mammoth` present). Re-run line 1 above (or `/setup markitdown`).
- **`markitdown-mcp: command not found`** — the install went into a different Python environment. Activate the right venv (or use the absolute Python path) and re-run.
- **Tool still missing after install** — Claude Code caches the MCP server list at session start. Quit and restart Claude Code, do not just reload the workspace.
- **Conversion fails on a `.docx` after install** — the file may be corrupt or password-protected. Open it locally and re-save. Markitdown does not handle encrypted Office files.

## Uninstall

```
pip uninstall markitdown-mcp
```

After uninstall, re-running `/requirements` with any `Supported-via-MCP` file in `input/` will fire `RF-01` again.
