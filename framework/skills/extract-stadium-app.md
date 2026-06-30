# extract-stadium-app.md

**Purpose:** Convert one detected **Stadium 6 application** (a deployed app folder, or the path a `*.stadium` pointer resolves to) into a set of lean, citation-ready **requirement assets** written into `input/`. This is the Stadium analogue of `convert-input-file.md` / `describe-visual-input.md`: a deterministic converter that produces markdown siblings the downstream pipelines read as ordinary `Native-text` inputs. It runs **once per app** — the caller (the input-handler pre-pass) skips already-processed apps via the processed-ledger.

Two phases:
- **Phase A — deterministic (Python).** Shell out to `framework/tools/extract_stadium_app.py --emit-assets`, which does **all** sharding/projection in Python and emits the Tier-1 assets (overview, data-model, data-sources, business-rules, access-control, surfaces, navigation, glossary, design-signals, modules) plus the full forensic `model.json` to the state dir. The LLM never loads `model.json`.
- **Phase B — bounded inference (LLM).** From the Tier-1 assets just written, synthesise the two **advisory** Tier-2 assets (`task-flows`, `quality-signals`), every line marked `[AI-SUGGESTED]`. This is the same kind of bounded, template-disciplined inference `describe-visual-input.md` performs for visuals — not free-form requirement mining.

The skill does **not** author requirements, personas, or business-purpose narratives — those remain downstream work for `/requirements`, `/generate-prd`, and `/analyse-inputs`.

## Inputs

- `app_path` — absolute path to the deployed Stadium application folder (the caller resolves a `*.stadium` pointer to this path before invoking). Required.
- `assets_dir` — repo-relative directory to write the per-app assets into, conventionally `input/<AppName>.stadium-assets/`. Required.
- `stem` — filename stem for the emitted assets (e.g. `MemberAdmin`); the extractor sanitises the app name if not supplied. Required.
- `kb_dir` — path to the Stadium knowledge base, `framework/assets/stadium`. Supplies module glosses + theming thresholds to the extractor. Required.
- `model_out` — path to write the full forensic `model.json`, conventionally `framework/state/stadium/<app-id>/model.json` (outside `input/`, never manifested). Required.

## Outputs

A structured row returned to the caller:
- `{ status: "ok", assets: [<basenames>], app_name: <str>, file_guid: <str> }` — Phase A and B both succeeded; the Tier-1 + Tier-2 assets exist under `assets_dir` and were write-verified (Tier-2) / parse-checked (Tier-1).
- `{ status: "failed", reason: "stadium-extract" }` — the extractor exited non-zero (the caller demotes/records `conversions_applied: "failed — stadium-extract"` and writes no assets).

On disk: `assets_dir/<stem>.stadium.<category>.md` for the ten Tier-1 categories + the two Tier-2 categories; `assets_dir/embedded/` for any extracted brand assets (logo, embedded docs); and the forensic `model.json` at `model_out`. The Stadium app folder itself is **never** written to or copied.

## Procedure

1. **Validate the unit.** Confirm `app_path` is a directory and looks like a Stadium app: it has `administration.db`, OR `App_Data/Updates/*.sapz`, OR `ClientApp/`. If none match, return `{ status: "failed", reason: "stadium-extract" }` (not a Stadium app — the caller treats the dropped item as an ordinary input instead).

2. **Phase A — run the extractor.** Via Bash:
   ```
   python framework/tools/extract_stadium_app.py "<app_path>" --emit-assets "<assets_dir>" --stem "<stem>" --kb "<kb_dir>" --model-out "<model_out>"
   ```
   The extractor selects the latest `.sapz` by deploy timestamp, redacts connection-string passwords (`sanitize_conn`), and degrades gracefully (no `.sapz` → `degraded-no-sapz`; no `administration.db` → `degraded-no-admin-db`) while still emitting assets. If the process exits non-zero, return `{ status: "failed", reason: "stadium-extract" }`. Capture the printed asset list and the `file_guid` / `App:` name from stdout (also recoverable from the `overview.md` provenance header).

3. **Parse-check Phase-A assets.** Each Tier-1 `*.stadium.*.md` exists and is non-empty (a lightweight read; these are compile-covered analogues — a truncated emit surfaces as an empty/short file). If any required Tier-1 asset is missing, treat as `failed — stadium-extract`.

4. **Phase B — synthesise the two advisory assets.** Read the Tier-1 assets `overview.md`, `navigation.md`, `surfaces.md`, `business-rules.md`, `access-control.md`, `data-model.md` from `assets_dir`. Then write, with the same YAML provenance header style as the Tier-1 assets (copy the header block from `overview.md`, changing `stadium_asset:` to the new category) and **every substantive line marked `[AI-SUGGESTED]`**:
   - `<stem>.stadium.task-flows.md` — task flows / user journeys, **grounded in the real navigation edges + ordered script action sequences** (e.g. `Members list → MemberAdd (SaveButton: MemberInsert → Notification → back to Members)`). Fold user-tasks/use-cases in as the steps of each flow. Do not invent flows with no nav/script basis.
   - `<stem>.stadium.quality-signals.md` — quality signals / trade-off dimensions inferred from the app (e.g. dense data grids → efficiency-over-simplicity posture; multi-step approval flows → guidance/safety posture; per the `framework/assets/trade-off-dimensions.md` vocabulary). These feed `/wireframe` + `/prototype` variant philosophy.
   The interpretation discipline mirrors `framework/assets/template-visual-description.md`'s Tier-B: advisory only, never authoritative, never `[SRC]`-cited.

5. **Verify the Phase-B writes.** Call `framework/skills/verify-artifact-write.md` on each of the two Tier-2 assets (sha256 + min-bytes). A mismatch is an `RF-04` hard halt per `framework/shared/refusal-registry.md > RF-04`. (Phase-A assets are not per-write-verified here — they are the extractor's compile-covered output, parse-checked at step 3.)

6. **Return** `{ status: "ok", assets: [...all 12 basenames...], app_name, file_guid }`. The caller records the result and updates the processed-ledger keyed by the app identity; this skill does **not** touch the ledger.

## Self-validation

- The extractor was invoked via `framework/tools/extract_stadium_app.py` (never re-implemented inline) and exited zero.
- All ten Tier-1 assets and both Tier-2 assets exist under `assets_dir` and are non-empty.
- Both Tier-2 assets were verified via `verify-artifact-write.md`.
- The Stadium app folder at `app_path` was only **read** — never written, copied, or modified.
- The full `model.json` was written to `model_out` (outside `input/`).
- Every substantive line in the Tier-2 assets carries `[AI-SUGGESTED]`; no Tier-2 line is phrased as an authoritative `[SRC]`-quotable fact.

## Tools

- Bash — run `framework/tools/extract_stadium_app.py` (Phase A); validate `app_path` shape (existence probes). Python is the only runtime dependency; it is preflighted by the caller (`RF-01`) before this skill is invoked.
- Read — read the Tier-1 assets for Phase B; bounded parse-check reads of the emitted assets.
- Write — write the two Tier-2 assets under `assets_dir`. No other writes.

## Anti-Patterns

- Do not re-implement extraction in the LLM. All deterministic facts come from the Python extractor; the LLM only synthesises the two clearly-advisory Tier-2 assets from the already-emitted Tier-1 assets.
- Do not load the full `model.json` into the LLM. It is a forensic, non-LLM artefact (often >1 MB). Phase B reads only the lean Tier-1 markdown assets.
- Do not author business purpose, personas/target users, or final user stories here. Those are deliberately left to `/generate-prd`, `/requirements`, and `/analyse-inputs` to avoid double-inference; over-reaching here would smuggle unfounded `[AI-SUGGESTED]` facts into every downstream pipeline.
- Do not `[SRC]`-cite anything in the Tier-2 assets. They are advisory; only the deterministic Tier-1 assets carry authoritative, quotable facts.
- Do not write into the Stadium app folder, copy it into `input/`, or modify it. Only `assets_dir` (under `input/`) and `model_out` (under `framework/state/`) are written.
- Do not update the processed-ledger from this skill. Ledger lifecycle (check-before / write-after) is owned by the input-handler pre-pass, so a failed extraction never marks an app as processed.
- Do not reproduce the app's screens as wireframes/HTML. Visual structure is captured as advisory signals in `surfaces.md`/`navigation.md` only; the system holds design authority over the *how* (per the canonical doctrine in `CLAUDE.md`).
