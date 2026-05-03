# preflight-mcp.md

**Purpose:** Confirm that an MCP-backed tool the input-handler may need is currently available in the harness's tool list. Presence-only check — no version validation, no functional probe. Runs as the first action of `requirements-input-handler.md`, before any file enumeration or classification, so a missing dependency surfaces as `RF-01 dependency_missing` immediately rather than mid-conversion.

**Inputs:**
- `tool_name` — the fully-qualified MCP tool name to probe. MVP: `mcp__markitdown__convert_to_markdown`.
- `advice_path` — the repo-relative path to the setup-instructions copy for this dependency. MVP: `framework/shared/setup-instructions/markitdown.md`.

**Outputs:** exactly one of:
- `ok` — the tool is in the available tool list. The agent advances.
- `RF-01 trigger` — the tool is absent. The agent surfaces the predicate per `framework/shared/refusal-registry.md > RF-01 dependency_missing`, including the `advice_path` in the question text.

**Used by:**
- `framework/agents/requirements-input-handler.md` — first workflow step. Called once per session, before file enumeration.

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

- The skill performs no write and no MCP call. Its only side effect is the conditional `RF-01` surface by the calling agent.
- `tool_name` and `advice_path` are both supplied by the caller. Hard-coding the MVP values inside this skill would couple the skill to markitdown; future predicates that probe other MCP tools reuse the same skill with different arguments.

## Anti-Patterns

- Do not call the probed tool. Presence-only is the contract — invoking the tool to test it can trigger side effects and can falsely succeed if the tool is registered but unhealthy.
- Do not version-check. The MCP server's published version is not part of the available tool list; gating on a version string requires an out-of-band registry that does not exist. If a version regression is suspected, surface it as troubleshooting in the setup-instructions copy, not as a preflight check.
- Do not run this skill unconditionally. If the run has no `Supported-via-MCP` files, the dependency is not required and `RF-01` would be a false positive.
- Do not skip this skill when a `Supported-via-MCP` file is present. Discovering a missing dependency mid-conversion strands the consultant with a partial manifest and an ambiguous failure.
