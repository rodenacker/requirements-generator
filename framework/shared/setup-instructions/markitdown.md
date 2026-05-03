# Markitdown MCP — Setup Instructions

Install copy referenced by `RF-01 dependency_missing` in `framework/shared/refusal-registry.md`. Surfaced to the consultant when the input-handler's preflight does not find `mcp__markitdown__convert_to_markdown` in the available tool list.

## Install

```
pip install markitdown-mcp==0.0.1a4
```

Python 3.10+ is required. Install into the same Python environment that Claude Code's MCP launcher resolves `markitdown-mcp` from. After installing, restart Claude Code so the MCP server is loaded.

The repo's `.mcp.json` already declares `markitdown-mcp` as an MCP server. No further configuration is required after install.

## Verify

After restarting Claude Code, the input-handler's preflight runs automatically on the next `/requirements` invocation. To verify out-of-band:

1. Confirm `markitdown-mcp` is on `PATH`: `markitdown-mcp --help`.
2. Confirm Claude Code lists the MCP server: the `mcp__markitdown__convert_to_markdown` tool should appear in the available tool list.

## Troubleshooting

- **`markitdown-mcp: command not found`** — the install went into a different Python environment. Activate the right venv (or use the absolute Python path) and re-run `pip install markitdown-mcp==0.0.1a4`.
- **Tool still missing after install** — Claude Code caches the MCP server list at session start. Quit and restart Claude Code, do not just reload the workspace.
- **Conversion fails on a `.docx` after install** — the file may be corrupt or password-protected. Open it locally and re-save before retrying. Markitdown does not handle encrypted Office files.

## Uninstall

```
pip uninstall markitdown-mcp
```

After uninstall, re-running `/requirements` with any `Supported-via-MCP` file in `input/` will fire `RF-01` again.
