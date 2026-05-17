# preflight-mcp.md

**Purpose:** Confirm that an MCP-backed tool the input-handler may need is currently available in the harness's tool list. Presence-only check — no version validation, no functional probe. Runs as the conditional preflight step of `framework/agents/input-handler.md` (when at least one input row has classified as `Supported-via-MCP`), before per-file conversion begins, so a missing dependency surfaces as `RF-01 dependency_missing` immediately rather than mid-conversion.

**Inputs:**
- `tool_name` — the fully-qualified MCP tool name to probe. Examples: `mcp__markitdown__convert_to_markdown`, `mcp__playwright__browser_navigate`.
- `advice_path` — the repo-relative path to the setup-instructions copy for this dependency. Examples: `framework/shared/setup-instructions/markitdown.md`, `framework/shared/setup-instructions/playwright.md`.
- `rf_predicate` — *optional* — the refusal-registry predicate ID the caller will surface on absence. Defaults to `RF-01` for backwards compatibility. Callers with a different choice set (e.g. design-system-styler with a three-way Install / Fallback / Drop prompt) pass their own predicate ID, e.g. `RF-06`.

**Outputs:** exactly one of:
- `ok` — the tool is in the available tool list. The agent advances.
- `<rf_predicate> trigger` — the tool is absent. The agent surfaces the predicate per `framework/shared/refusal-registry.md > <rf_predicate>`, including the `advice_path` in the question text. The skill itself does not pick the surface mechanism — it returns the trigger and the *caller* applies the registry entry.

**Used by:**
- `framework/agents/input-handler.md` — called once per session after classification, when at least one row is `Supported-via-MCP`. Uses default `rf_predicate = RF-01`. Shared between `/requirements` and `/analyse-inputs`.
- `framework/agents/design-system-styler/steps/step-04-site-fetching.md` — called only when the consultant supplied a non-null `{{reference_url}}`. Passes `tool_name = mcp__playwright__browser_navigate`, `advice_path = framework/shared/setup-instructions/playwright.md`, `rf_predicate = RF-06`.

## Procedure

1. Inspect the harness's tool list. The check is presence-only: if a function with name exactly equal to `tool_name` is callable, return `ok`. Otherwise trigger `RF-01`.
2. Do not call the tool to test it. The probe is name-based; calling the tool with a sentinel argument risks side effects (file writes, network calls) and slow-paths the preflight.

## Conditional invocation

The input-handler must call this skill when, and only when, the post-classification view of `input/` shows at least one file whose tier is `Supported-via-MCP`. Calling preflight-mcp on a run with only Native-text and Native-multimodal inputs would surface `RF-01` for a tool the agent does not need, and is a defect.

A clean ordering for the input-handler:
1. Enumerate `input/`.
2. Classify each file via `framework/skills/classify-input-tier.md`.
3. **If any classified row has `tier = Supported-via-MCP`, call this skill.** Otherwise skip.
4. Proceed to conversion (or skip the conversion step if no MCP-tier files remain).

## Self-validation

- The skill performs no write and no MCP call. Its only side effect is the conditional refusal surface raised by the calling agent.
- `tool_name`, `advice_path`, and `rf_predicate` are all supplied by the caller. Hard-coding any of them inside this skill would couple it to one caller; the skill is reused by callers that probe different MCP tools and surface different predicates.

## Anti-Patterns

- Do not call the probed tool. Presence-only is the contract — invoking the tool to test it can trigger side effects and can falsely succeed if the tool is registered but unhealthy.
- Do not version-check. The MCP server's published version is not part of the available tool list; gating on a version string requires an out-of-band registry that does not exist. If a version regression is suspected, surface it as troubleshooting in the setup-instructions copy, not as a preflight check.
- Do not run this skill unconditionally. If the run has no `Supported-via-MCP` files, the dependency is not required and `RF-01` would be a false positive.
- Do not skip this skill when a `Supported-via-MCP` file is present. Discovering a missing dependency mid-conversion strands the consultant with a partial manifest and an ambiguous failure.
