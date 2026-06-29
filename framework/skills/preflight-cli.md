# preflight-cli.md

**Purpose:** Confirm that a **CLI binary** the input-handler may need is currently installed and on `PATH`. Presence-only check — no version validation, no functional render. Runs as the conditional preflight step 4b of `framework/agents/input-handler.md` (when at least one input row has classified as `Vector-renderable`), before per-file render begins, so a missing renderer surfaces as `RF-01 dependency_missing` immediately rather than mid-render. CLI sibling of `framework/skills/preflight-mcp.md` (which probes MCP tools); both return the same trigger shape so the caller's `RF-01` surface is identical.

**Inputs:**
- `binaries` — an ordered list of candidate CLI binary names to probe, e.g. `["inkscape", "rsvg-convert", "drawio", "soffice"]`. The probe succeeds if **any** candidate is found (the render skill picks the first available per format). Required.
- `advice_path` — the repo-relative path to the setup-instructions copy for this dependency. The input-handler passes `framework/shared/setup-instructions/visual-render.md`.
- `rf_predicate` — *optional* — the refusal-registry predicate ID the caller surfaces on absence. Defaults to `RF-01`.

**Outputs:** exactly one of:
- `ok` — at least one candidate binary is on `PATH`. Returns the resolved binary name(s) so the caller/render skill knows which renderer to use. The agent advances.
- `<rf_predicate> trigger` — no candidate binary is found. The agent surfaces the predicate per `framework/shared/refusal-registry.md > <rf_predicate>`, including the `advice_path` in the question text. The skill returns the trigger; the *caller* applies the registry entry. (For `RF-01`, that choice set includes `install-now`, which runs the matching `framework/tools/setup-environment.ps1 -Component <X>` on the consultant's behalf.)

**Used by:**
- `framework/agents/input-handler.md` — step 4b, once per session, when at least one row is `Vector-renderable`. Uses default `rf_predicate = RF-01`, `advice_path = framework/shared/setup-instructions/visual-render.md`. Shared across `/requirements`, `/generate-prd`, `/analyse-inputs`, `/review-inputs`.

## Procedure

1. For each candidate in `binaries`, probe presence on `PATH` with a non-executing check: PowerShell `Get-Command <name> -ErrorAction SilentlyContinue` (or Bash `command -v <name>`). The check is presence-only.
2. If any candidate resolves, return `ok` with the list of resolved binaries (first-found order preserved). Otherwise trigger `RF-01`.
3. Do not run the binary to render a test file. The probe is presence-only; invoking a renderer with a sentinel file risks slow-paths and scratch-file residue.

## Conditional invocation

The input-handler must call this skill when, and only when, the post-classification view of `input/` shows at least one file whose tier is `Vector-renderable`. Calling it on a run with no vector inputs would surface `RF-01` for a renderer the agent does not need, and is a defect. (Symmetric to `preflight-mcp.md`'s conditional-invocation rule for `Supported-via-MCP`.)

## Self-validation

- The skill performs no write and renders nothing. Its only side effect is the conditional refusal surface raised by the calling agent.
- `binaries`, `advice_path`, and `rf_predicate` are all supplied by the caller. Hard-coding any of them inside this skill would couple it to one caller.
- The probe is a presence check only (`Get-Command` / `command -v`); it never executes the candidate binary.

## Anti-Patterns

- Do not execute the probed binary. Presence-only is the contract — running a renderer to test it can leave scratch files and can falsely succeed if the binary is present but broken (surface that as troubleshooting in `visual-render.md`, not here).
- Do not version-check. Renderer versions are out of scope; if a version regression is suspected, document it in the setup-instructions copy.
- Do not run this skill unconditionally. If the run has no `Vector-renderable` files, the renderer is not required and `RF-01` would be a false positive.
- Do not skip this skill when a `Vector-renderable` file is present. Discovering a missing renderer mid-render strands the consultant with a partial manifest.
