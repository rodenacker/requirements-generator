# Playwright MCP — Setup Instructions

Install copy referenced by `RF-01 dependency_missing` in `framework/shared/refusal-registry.md`. Surfaced to the consultant when the design-system-styler's preflight in `step-04-site-fetching.md` does not find `mcp__playwright__browser_navigate` in the available tool list.

## Why Playwright is needed

The design-system styler reads real stylesheet text and computed styles from the consultant's reference URL. WebFetch returns LLM-summarized content rather than raw CSS — exact hex codes, CSS custom properties on `:root`, and computed values (`font-size` resolved from `clamp()`, `box-shadow`, `transition-duration`) are typically lost. Playwright renders the page in a real Chromium browser so the styler can read actual values via `document.styleSheets` and `getComputedStyle()`.

## Install

**Fastest:** `/setup playwright` (or `/setup`) warms the `npx` cache for the server and verifies the MCP tool is callable. The manual equivalent is below.

The Playwright MCP server runs via `npx`. The repo's `.mcp.json` already registers it, pinned and configured to drive the **browser already installed on your machine** (no downloaded Chromium):

```
npx -y @playwright/mcp@0.0.76 --browser chrome
```

`--browser chrome` makes the server use your installed Google Chrome — resolved at launch from the standard install locations (`%LOCALAPPDATA%`, `%PROGRAMFILES%`, `%PROGRAMFILES(X86)%` on Windows) — so **no `npx playwright install` is required**. On a Windows machine without Chrome, change `chrome` to `msedge` (Edge is preinstalled on Windows 10/11); for a non-standard Chrome location use `--executable-path <path>` instead.

To register it manually instead of via `.mcp.json`:

```
claude mcp add playwright -- npx -y @playwright/mcp@0.0.76 --browser chrome
```

Restart Claude Code so the MCP server is loaded into the session.

## Verify

After restarting, the styler's preflight runs automatically the next time the consultant supplies a URL in `/design-system`. To verify out-of-band:

1. Confirm the MCP server is registered: `claude mcp list` should show `playwright` as connected.
2. Confirm the tool is in the available tool list: `mcp__playwright__browser_navigate` should be callable.

## Troubleshooting

- **`playwright` not in `claude mcp list` after install** — Claude Code caches the MCP server list at session start. Quit and restart Claude Code, do not just reload the workspace.
- **`Executable doesn't exist` / `Chromium distribution 'chrome' is not found`** — the server cannot locate an installed Chrome. Confirm Chrome is installed in a standard location, switch the server's `--browser` arg to `msedge` (always present on Windows), or point it at the binary with `--executable-path <path>`. Only as a last resort, fall back to a downloaded browser with `npx playwright install chromium`.
- **Navigation hangs / times out on a specific site** — the page may have an infinite-load resource. Re-run with a different reference URL, or fall back to the WebFetch path at the preflight prompt.
- **`browser_evaluate` returns an empty payload** — the page likely uses CSS-in-JS injected after `load`. The styler already includes a 1.5s settling wait plus `document.fonts.ready`; if a site needs more, that is a per-site quirk and the consultant should choose the WebFetch fallback.
- **Sandbox / permissions issues on Windows** — Chromium occasionally fails to launch under restricted profiles. Run Claude Code from a terminal with normal user privileges (not elevated, not sandboxed).

## Uninstall

```
claude mcp remove playwright
```

After uninstall, re-running `/design-system` with a URL will fire `RF-01` again; the consultant gets the three-way preflight choice (install + retry, WebFetch fallback, or drop URL).
