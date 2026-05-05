# check-context-bloat.md

**Purpose:** Decide whether the conversation context has accumulated enough material before invoking an agent that the agent risks degraded output. Caller-agnostic: the skill takes its target paths as inputs so the same heuristic serves multi-agent orchestrators (where bloat builds between same-pipeline stages) and single-agent orchestrators (where the proxy is whatever prior pipeline state exists on disk in the same conversation thread). Heuristic uses on-disk file bytes — deterministic, auditable, and cheap to compute — rather than token counts, which are model-specific and not portable across harnesses.

**Inputs (caller-supplied):**
- `artefact_dir` — **required** — directory whose direct (non-recursive) `.md` and `.json` files contribute to `bytes_total`. Example callers: `requirements/` (requirements-orch), `requirements/` (design-system-orch — same directory because the design-system pipeline uses prior `/requirements` state as its bloat proxy).
- `manifest_path` — **optional** — path to a manifest JSON whose non-`Unsupported` rows contribute to `bytes_total` (via `original_path` for `Native-text` / `Native-multimodal` rows and `converted_sibling` for `Supported-via-MCP` rows) and to `row_count`. Omit when the caller has no manifest; `row_count` is then `0` for the trigger check and the manifest contribution to `bytes_total` is skipped.
- `progress_path` — **optional** — path to a progress file that gates the predicate on the presence of at least one `completed` event. Omit when the caller has no progress file (single-agent pipelines): in that case the predicate is computed unconditionally and the gating early-return below does not apply.

**Outputs:** exactly one of:
- `ok` — the orchestrator advances and writes the next `called` event (or simply proceeds, in single-agent callers).
- `RF-05 trigger` — the orchestrator surfaces the predicate per `framework/shared/refusal-registry.md > RF-05 prior_stage_context_bloated`.

**Used by:**
- `framework/orchestrators/requirements-orch.md` — immediately before each `called` event written for `requirements-drafter`, `requirements-resolver`, and `requirements-merger`. Invoked with `artefact_dir = requirements/`, `manifest_path = requirements/source-manifest.json`, `progress_path = framework/state/.progress.json`.
- `framework/orchestrators/design-system-orch.md` — once at startup, immediately after the prior-artefact gate and before invoking `design-system-styler`. Invoked with `artefact_dir = requirements/`, `manifest_path = requirements/source-manifest.json`, `progress_path = framework/state/.progress.json`. The design-system pipeline is stand-alone and produces no requirements artefacts itself; reading these paths is a deliberate, narrow exception declared in the orchestrator for this preflight only.

## Heuristic

Compute two scalars from the on-disk state:

1. **`bytes_total`** — sum of byte sizes of (a) every `.md` and `.json` file directly under `artefact_dir`, plus (b) when `manifest_path` is supplied, every file referenced by a manifest row's `original_path` (when `tier ∈ {Native-text, Native-multimodal}`) or `converted_sibling` (when `tier = Supported-via-MCP`). Skip `Unsupported` rows — the consuming agent does not read them.
2. **`row_count`** — number of non-Unsupported rows in the manifest at `manifest_path`. When `manifest_path` is omitted, `row_count = 0`.

Trigger `RF-05` if **either**:
- `bytes_total > 250_000` (250 KB), OR
- `row_count > 25`.

Otherwise return `ok`.

The two thresholds are starting heuristics. Either tripping is sufficient — neither is dominant. Tune both together as real runs accumulate evidence.

## Self-validation

- When `progress_path` is supplied: the file exists and has at least one `completed` event. If not, the predicate has no prior stage to compare against and the skill returns `ok` without computing the heuristic. When `progress_path` is omitted: skip this gate entirely and proceed to the heuristic.
- When `manifest_path` is supplied: the file exists and parses as JSON. If it does not, the predicate cannot be evaluated; return `ok` (the upstream agent's own self-validation catches manifest corruption). When `manifest_path` is omitted: skip the manifest contribution and use only `artefact_dir` bytes.
- When `artefact_dir` does not exist or is empty, `bytes_total` is `0` (from this contribution) and the threshold is checked against whatever the manifest contributed.
- The skill performs no write — its only side effect is the optional `RF-05` surface call by the calling orchestrator.

## Anti-Patterns

- Do not count tokens. Token counts depend on the active model's tokeniser and on conversation history not visible to the skill; on-disk bytes are the only auditable signal.
- Do not assume a specific `artefact_dir`, `manifest_path`, or `progress_path`. The skill is caller-agnostic; hard-coding any of them couples it to one orchestrator and breaks reuse by the other.
- Do not include files outside the supplied `artefact_dir` and the manifest's referenced inputs. Framework files (`framework/`) and progress sidecars are infrastructure, not consultant material.
- Do not raise the threshold opportunistically when a single run trips the predicate. The threshold is a project-wide knob; calibrate it across runs, not for one stage that happened to bloat.
- Do not run this skill at a point where there is no prior-stage state to bloat against. In multi-agent pipelines that means: not before the first agent's `called` event. In single-agent pipelines that means: not at points where the heuristic cannot meaningfully fire (e.g., before the agent has even been considered for invocation).
