# Mermaid CLI (`mmdc`) — Setup Instructions

Install copy referenced by `RF-07 mermaid_render_dependency_missing` in `framework/shared/refusal-registry.md`. **`RF-07` has no active surfacer, and no `/analyse-inputs` analyser depends on `mmdc`, as of the inline-SVG conversion.** Every diagram-emitting `/analyse-inputs` analyser — `thematic-analysis`, `opportunity-solution-trees`, `affinity-mapping`, `swim-lane-process-mapping` — now pre-renders its diagram as inline `<svg>` and embeds the Mermaid source as an unvalidated export adjunct. This doc + the `mermaid-validator.md` skill are retained as the canonical install reference for any **future** methodology that chooses to validate a Mermaid source.

(Other pipelines outside `/analyse-inputs` still use the validator — e.g. the `/requirements` drafter for the `requirements.md` §2 domain-model Mermaid diagram. Same install instructions apply there. The inputs-side `ooux` no longer emits a diagram at all.)

## Install

**Fastest:** `/setup mmdc` (or `/setup`) installs and verifies this for you.

```
npm install -g @mermaid-js/mermaid-cli
```

Node.js 18+ is required (the Mermaid CLI bundles `mermaid` v10.x or v11.x, both of which support the `mindmap` diagram type — stable since v10.0.0).

After installing, restart Claude Code so any `PATH` propagation completes cleanly.

## Verify

After installation:

1. Confirm `mmdc` is on `PATH`: run `mmdc --version` from any shell. Expected output: a version string like `Mermaid CLI v10.6.1` or later.
2. Confirm a minimal render succeeds:

    ```
    echo "mindmap`n  root((test))`n    Branch A`n    Branch B" > $env:TEMP\mmdc-smoke.mmd
    mmdc -i $env:TEMP\mmdc-smoke.mmd -o $env:TEMP\mmdc-smoke.svg
    ```

   (PowerShell syntax; on POSIX shells use `/tmp/` paths and `\n` line breaks.) Expected output: `$env:TEMP\mmdc-smoke.svg` exists and contains valid SVG (open in a browser to confirm).

3. No current `/analyse-inputs` methodology validates Mermaid — they all pre-render inline SVG — so this step applies only to a future Mermaid-validating methodology or an `/analyse-requirement` analyser that uses `mermaid-validator.md`: its invocation now finds `mmdc` on PATH and proceeds.

## Troubleshooting

- **`mmdc: command not found` after install** — `npm install -g` placed the binary in a directory not on PATH. Run `npm bin -g` to print the global bin directory; add it to `PATH` and restart the shell.
- **`Error: Could not find Chrome (rev ...)` on first run** — Mermaid CLI uses Puppeteer, which requires a Chromium binary. Run `npx puppeteer browsers install chrome` (Puppeteer ≥ 19) or install a system Chrome / Chromium and set `PUPPETEER_EXECUTABLE_PATH=<path-to-chrome>` in your environment.
- **`Error: ENOENT: no such file or directory, open '.../config.json'` on first invocation** — older Mermaid CLI versions need an empty `puppeteer-config.json`. Create one with `{}` content and pass `-p ./puppeteer-config.json` to `mmdc`.
- **Mermaid CLI installed but Claude Code's `mermaid-validator` still reports "not installed"** — the validator skill shells out to `mmdc` via `Bash`. Confirm `Bash` resolves `mmdc` in the same shell context Claude Code spawns (run `bash -c "which mmdc"` from outside Claude Code; if empty, fix `PATH` in your shell rc file).
- **`mindmap` rejected as unknown diagram type** — Mermaid versions < 10.0.0 do not support `mindmap`. Upgrade with `npm install -g @mermaid-js/mermaid-cli@latest` and confirm `mmdc --version` reports v10.0.0 or later.

## Uninstall

```
npm uninstall -g @mermaid-js/mermaid-cli
```

After uninstall, no `/analyse-inputs` analyser is affected — they all pre-render inline SVG with no `mmdc` dependency. Only a future methodology (or an `/analyse-requirement` analyser) that validates a Mermaid source via `mermaid-validator.md` would halt on the validator's `not-installed` path until `mmdc` is reinstalled.

## Alternative — mermaid.live (no install required)

When installing `mmdc` is not feasible (locked-down environment, CI without Chromium, etc.), the consultant can choose the `skip-mermaid-validation-with-warning` branch at the `RF-07` prompt. The analyser then writes the artefact with the Mermaid source verbatim in `<pre class="mermaid-source">` but with a diagnostics warning recording the skipped validation. The consultant can paste the Mermaid source into [https://mermaid.live](https://mermaid.live) to confirm it renders. The artefact remains valid and re-ingestible by `/requirements`; only the local pre-write validation step was skipped.
