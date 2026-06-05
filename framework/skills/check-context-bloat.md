# check-context-bloat.md

**Purpose:** Decide whether the conversation context has accumulated enough material before invoking an agent that the agent risks degraded output. Caller-agnostic: the skill takes its target paths as inputs so the same heuristic serves multi-agent orchestrators (where bloat builds between same-pipeline stages) and single-agent orchestrators (where the proxy is whatever prior pipeline state exists on disk in the same conversation thread). Heuristic uses on-disk file bytes — deterministic, auditable, and cheap to compute — rather than token counts, which are model-specific and not portable across harnesses.

**Inputs (caller-supplied):**
- `artefact_dir` — **required** — directory whose direct (non-recursive) `.md` and `.json` files contribute to `bytes_total`. Example callers: `requirements/` (requirements-orch), `requirements/` (design-system-orch — same directory because the design-system pipeline uses prior `/requirements` state as its bloat proxy).
- `manifest_path` — **optional** — path to a manifest JSON whose non-`Unsupported` rows contribute to `bytes_total` (via `original_path` for `Native-text` / `Native-multimodal` rows and `converted_sibling` for `Supported-via-MCP` rows) and to `row_count`. Omit when the caller has no manifest **or when the consuming agent does not read the manifest-referenced input files** — the derived-artefact pipelines (`analyse-requirement`, `review-requirement`, `wireframe`, `design-system`) read `requirements/requirements.md` and their own framework assets, never the raw `input/` corpus, so passing the manifest would inflate the measurement (bytes *and* `row_count`) with files the agent never loads. When omitted, `row_count` is `0` for the trigger check and the manifest contribution to `bytes_total` is skipped.
- `progress_path` — **optional** — path to a progress file that gates the predicate on the presence of at least one `completed` event. Omit when the caller has no progress file (single-agent pipelines): in that case the predicate is computed unconditionally and the gating early-return below does not apply.
- `threshold_bytes` — **optional** — byte ceiling for `bytes_total`. Defaults to `500_000` (500 KB) when omitted or non-positive. Callers whose load profile differs from the default may pass a calibrated value — e.g. an input-reading pipeline that legitimately ingests a large, *irreducible* client corpus (where `/clear` cannot help) may warrant a higher ceiling than a derived pipeline that reads only a bounded `requirements.md`. Set per-caller overrides from accumulated run evidence, not a single trip.
- `threshold_rows` — **optional** — row ceiling for `row_count`. Defaults to `25` when omitted or non-positive. Only meaningful when `manifest_path` is supplied (otherwise `row_count` is `0` and this never fires).

**Outputs:** exactly one of:
- `ok` — the orchestrator advances and writes the next `called` event (or simply proceeds, in single-agent callers).
- `RF-05 trigger` — the orchestrator surfaces the predicate per `framework/shared/refusal-registry.md > RF-05 prior_stage_context_bloated`.

**Used by:** all nine pipeline orchestrators call this skill at a preflight (and `requirements-orch` / `generate-prd-orch` re-call it before each post-input stage). Each passes its own `progress_path` (or omits it where the pipeline keeps no progress file). The `artefact_dir` + `manifest_path` arguments track **what the pipeline's agent actually loads**, which splits the callers into two classes:

| Orchestrator | `artefact_dir` | `manifest_path` | Why |
|---|---|---|---|
| `requirements-orch` | `requirements/` | passed | drafter reads the raw input corpus |
| `generate-prd-orch` | `prd/` | passed | PRD drafter reads the raw input corpus |
| `analyse-inputs-orch` | `input/` | passed | analyser reads the raw input corpus |
| `review-inputs-orch` | `input/` | passed | reviewer reads the raw input corpus |
| `analyse-requirement-orch` | `requirements/` | **omitted** | analyser reads only `requirements.md` + its method assets |
| `review-requirement-orch` | `requirements/` | **omitted** | reviewer reads only `requirements.md` + its method assets |
| `wireframe-orch` | `requirements/` | **omitted** | architect reads `requirements.md` + selected analyses sidecars, never the raw corpus |
| `design-system-orch` | `requirements/` | **omitted** | styler reads nothing under `requirements/`; the dir is a thread-bloat proxy only |
| `prototype-orch` | `prototypes/.specs/` | omitted | reads its own spec state |

A pipeline passes `manifest_path` **only when its agent reads the raw `input/` corpus**. The derived-artefact pipelines omit it so the manifest's input bytes and `row_count` do not inflate the measurement with files the agent never loads. Thresholds are the per-caller `threshold_bytes` / `threshold_rows` overrides (defaulting to 500 KB / 25); no caller overrides the defaults today.

## Heuristic

Compute two scalars from the on-disk state:

1. **`bytes_total`** — sum of byte sizes of (a) every `.md` and `.json` file directly under `artefact_dir`, plus (b) when `manifest_path` is supplied, every file referenced by a manifest row's `original_path` (when `tier ∈ {Native-text, Native-multimodal}`) or `converted_sibling` (when `tier = Supported-via-MCP`). Skip `Unsupported` rows — the consuming agent does not read them.
2. **`row_count`** — number of non-Unsupported rows in the manifest at `manifest_path`. When `manifest_path` is omitted, `row_count = 0`.

Trigger `RF-05` if **either**:
- `bytes_total > threshold_bytes` (default `500_000` / 500 KB), OR
- `row_count > threshold_rows` (default `25`).

Otherwise return `ok`.

The defaults are starting heuristics. Either tripping is sufficient — neither is dominant. Tune the defaults (here, the canonical home of the numbers) and any per-caller `threshold_bytes` / `threshold_rows` overrides together as real runs accumulate evidence.

## Self-validation

- When `progress_path` is supplied: the file exists and has at least one `completed` event. If not, the predicate has no prior stage to compare against and the skill returns `ok` without computing the heuristic. When `progress_path` is omitted: skip this gate entirely and proceed to the heuristic.
- When `manifest_path` is supplied: the file exists and parses as JSON. If it does not, the predicate cannot be evaluated; return `ok` (the upstream agent's own self-validation catches manifest corruption). When `manifest_path` is omitted: skip the manifest contribution and use only `artefact_dir` bytes.
- When `threshold_bytes` / `threshold_rows` are omitted or non-positive, use the defaults (`500_000` / `25`). The thresholds are defined here only; callers reference them, never restate the digits.
- When `artefact_dir` does not exist or is empty, `bytes_total` is `0` (from this contribution) and the threshold is checked against whatever the manifest contributed.
- The skill performs no write — its only side effect is the optional `RF-05` surface call by the calling orchestrator.

## Anti-Patterns

- Do not count tokens. Token counts depend on the active model's tokeniser and on conversation history not visible to the skill; on-disk bytes are the only auditable signal.
- Do not assume a specific `artefact_dir`, `manifest_path`, or `progress_path`. The skill is caller-agnostic; hard-coding any of them couples it to one orchestrator and breaks reuse by the other.
- Do not include files outside the supplied `artefact_dir` and the manifest's referenced inputs. Framework files (`framework/`) and progress sidecars are infrastructure, not consultant material.
- Do not raise the threshold opportunistically when a single run trips the predicate. The threshold is a project-wide knob; calibrate it across runs, not for one stage that happened to bloat.
- Do not run this skill at a point where there is no prior-stage state to bloat against. In multi-agent pipelines that means: not before the first agent's `called` event. In single-agent pipelines that means: not at points where the heuristic cannot meaningfully fire (e.g., before the agent has even been considered for invocation).
