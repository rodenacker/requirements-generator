# Playwright MCP — Setup Instructions

Install copy referenced by `RF-01 dependency_missing` in `framework/shared/refusal-registry.md`. Surfaced to the consultant when the design-system-styler's preflight in `step-04-site-fetching.md` does not find `mcp__playwright__browser_navigate` in the available tool list.

## Why Playwright is needed

The design-system styler reads real stylesheet text and computed styles from the consultant's reference URL. WebFetch returns LLM-summarized content rather than raw CSS — exact hex codes, CSS custom properties on `:root`, and computed values (`font-size` resolved from `clamp()`, `box-shadow`, `transition-duration`) are typically lost. Playwright renders the page in a real Chromium browser so the styler can read actual values via `document.styleSheets` and `getComputedStyle()`.

## Install

The Playwright MCP server runs via `npx`. Register it with Claude Code:

```
claude mcp add playwright -- npx -y @playwright/mcp@latest
```

Then install the Chromium browser binary the server uses:

```
npx playwright install chromium
```

Restart Claude Code so the MCP server is loaded into the session.

## Verify

After restarting, the styler's preflight runs automatically the next time the consultant supplies a URL in `/design-system`. To verify out-of-band:

1. Confirm the MCP server is registered: `claude mcp list` should show `playwright` as connected.
2. Confirm the tool is in the available tool list: `mcp__playwright__browser_navigate` should be callable.

## Troubleshooting

- **`playwright` not in `claude mcp list` after install** — Claude Code caches the MCP server list at session start. Quit and restart Claude Code, do not just reload the workspace.
- **`Executable doesn't exist` when navigating** — the Chromium binary is missing. Run `npx playwright install chromium` (or `npx playwright install --with-deps chromium` on Linux to also pull system libraries).
- **Navigation hangs / times out on a specific site** — the page may have an infinite-load resource. Re-run with a different reference URL, or fall back to the WebFetch path at the preflight prompt.
- **`browser_evaluate` returns an empty payload** — the page likely uses CSS-in-JS injected after `load`. The styler already includes a 1.5s settling wait plus `document.fonts.ready`; if a site needs more, that is a per-site quirk and the consultant should choose the WebFetch fallback.
- **Sandbox / permissions issues on Windows** — Chromium occasionally fails to launch under restricted profiles. Run Claude Code from a terminal with normal user privileges (not elevated, not sandboxed).

## Uninstall

```
claude mcp remove playwright
```

After uninstall, re-running `/design-system` with a URL will fire `RF-01` again; the consultant gets the three-way preflight choice (install + retry, WebFetch fallback, or drop URL).
