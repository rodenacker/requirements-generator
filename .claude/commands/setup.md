---
description: Install, configure, and test the workspace dependencies (markitdown Office/PDF, Node, draw.io, Playwright). Runs once per machine.
---

You are the environment-setup driver for `/setup`. Your job is to bring this consultant's machine to a known-good state for every pipeline — by running the canonical setup script, verifying what only Claude can see (the MCP tool list), and reporting a clear status table. You install **user-scoped** tools (so a fresh repo clone never needs them re-installed) and you never touch pipeline artefacts.

The canonical, component-addressable installer is `framework/tools/setup-environment.ps1`. It is detection-first and idempotent: a dependency already present is verified and left untouched. Do **not** restate or re-implement its install commands — run it.

## Argument

`/setup` takes an optional component name (the consultant may type e.g. `/setup markitdown`). Valid values: `all` (default), `core`, `markitdown`, `drawio`, `node`, `python`, `playwright`, `inkscape`, `libreoffice`. `core` is the five core dependencies only (`python, markitdown, node, playwright` — i.e. `all` minus the `drawio` vector renderer and the on-demand `inkscape`/`libreoffice`); it is also what the standalone `framework/tools/setup-core.ps1` bootstrap runs. If the consultant passed no argument, use `all`. If they passed an unrecognised token, tell them the valid set and use `all`.

## Steps

1. **Run the script.** Invoke it with the **PowerShell tool** (it requires PowerShell 7):

   ```
   & framework/tools/setup-environment.ps1 -Component <chosen-component>
   ```

   Use install mode (no `-Probe`) — already-satisfied components self-skip, so this is safe to re-run. Capture the full stdout.

2. **Parse the summary.** Read the JSON array between the `===SETUP-ENVIRONMENT-SUMMARY-BEGIN===` and `===SETUP-ENVIRONMENT-SUMMARY-END===` sentinel lines. Each entry has `component`, `status` (`ready` | `installed-pending-restart` | `failed` | `absent` | `n/a`), `detail`, `gates`, `restartNeeded`.

3. **Verify the MCP tools** — the part the script cannot see, because only the harness exposes the live tool list:
   - `mcp__markitdown__convert_to_markdown` — callable? (gates Office/PDF inputs)
   - `mcp__playwright__browser_navigate` — callable? (gates `/design-system` URL extraction + `/prototype` smoke)

   A tool that is *callable now* is live in this session. A tool whose component the script just installed but that is *not yet callable* is **pending a restart** (the MCP server list is cached at session start).

4. **Print a status table.** One row per dependency: a ✅ / ⚠️ / ❌ glyph, the component, what it gates, and the detail. Map `ready` → ✅, `installed-pending-restart` (or installed-but-MCP-not-yet-callable) → ⚠️, `failed` → ❌, `absent`/`n/a` → note. Fold the two MCP checks from step 3 into the markitdown and playwright rows.

5. **Restart guidance.** If any row is ⚠️ (`restartNeeded` true, or an MCP tool was installed but isn't callable yet), tell the consultant plainly: **restart Claude Code**, then run `/setup` again — already-installed pieces will confirm as ✅ and the MCP tools will be callable. This is unavoidable on Windows: PATH and the MCP server list are read at session start. If every row is ✅, say setup is complete and no restart is needed.

6. **Offer the on-demand renderers.** The core run does **not** install the rarely-needed vector renderers. If the consultant works with `.svg` (Inkscape) or `.vsdx` (LibreOffice) inputs, mention they can run `/setup inkscape` or `/setup libreoffice` now — otherwise these install just-in-time the first time such an input appears (the `RF-01` handback offers it). Do not install them unprompted.

7. **Stop.** Do not run any other pipeline work. `/setup` only prepares the environment.

## Constraints

- Run the script; never paraphrase or re-implement its install commands — it is the single source of truth for what gets installed and how.
- Install user-scoped tools only. Never modify pipeline artefacts (`requirements/`, `prd/`, `framework/state/`, etc.) from `/setup`.
- Be honest about the restart constraint — a freshly installed PATH/MCP tool is not usable in the current session until Claude Code restarts. Never report a ⚠️ row as done.
- Report `failed` rows verbatim with the `detail` (it names the setup-instruction doc to consult) — do not hide a failure behind a green table.
