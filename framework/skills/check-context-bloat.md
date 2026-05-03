# check-context-bloat.md

**Purpose:** Decide whether the conversation context has accumulated enough material between agents that the next agent risks degraded output. Runs at the orchestrator's entry to each `called` event after `requirements-input-handler`, when the prior agent has a `completed` event in `framework/state/.progress.json`. Heuristic uses on-disk file bytes — deterministic, auditable, and cheap to compute — rather than token counts, which are model-specific and not portable across harnesses.

**Inputs:**
- `framework/state/.progress.json` — read for the prior agent's `completed` event (the predicate only fires when a prior agent has finished).
- `requirements/source-manifest.json` — read for the list of `original_path` and `converted_sibling` entries.
- `requirements/` — the artefact directory; the skill sums byte sizes of every `.md` and `.json` file directly under it (non-recursive).

**Outputs:** exactly one of:
- `ok` — the orchestrator advances and writes the next `called` event.
- `RF-05 trigger` — the orchestrator surfaces the predicate per `framework/shared/refusal-registry.md > RF-05 prior_stage_context_bloated`.

**Used by:**
- `framework/orchestrators/requirements-orch.md` — immediately before each `called` event written for `requirements-resolver` and `requirements-merger`.

## Heuristic

Compute two scalars from the on-disk state:

1. **`bytes_total`** — sum of byte sizes of (a) every `.md` and `.json` file directly under `requirements/`, plus (b) every file referenced by a manifest row's `original_path` (when `tier ∈ {Native-text, Native-multimodal}`) or `converted_sibling` (when `tier = Supported-via-MCP`). Skip `Unsupported` rows — the drafter does not read them.
2. **`row_count`** — number of non-Unsupported rows in `requirements/source-manifest.json`.

Trigger `RF-05` if **either**:
- `bytes_total > 250_000` (250 KB), OR
- `row_count > 25`.

Otherwise return `ok`.

The two thresholds are starting heuristics. Either tripping is sufficient — neither is dominant. Tune both together as real runs accumulate evidence.

## Self-validation

- `framework/state/.progress.json` exists and has at least one `completed` event. If not, the predicate has no prior stage to compare against and the skill returns `ok` without computing the heuristic.
- `requirements/source-manifest.json` exists and parses. If it does not, the predicate cannot be evaluated; return `ok` (the input-handler's own self-validation catches manifest corruption upstream).
- The skill performs no write — its only side effect is the optional `RF-05` surface call by the calling orchestrator.

## Anti-Patterns

- Do not count tokens. Token counts depend on the active model's tokeniser and on conversation history not visible to the skill; on-disk bytes are the only auditable signal.
- Do not include files outside `requirements/` and the manifest's referenced inputs. Framework files (`framework/`) and progress sidecars are infrastructure, not consultant material.
- Do not raise the threshold opportunistically when a single run trips the predicate. The threshold is a project-wide knob; calibrate it across runs, not for one merger that happened to bloat.
- Do not run this skill at orchestrator startup or before the input-handler's `called` event. There is no prior-stage state to bloat against; the predicate is meaningless.
