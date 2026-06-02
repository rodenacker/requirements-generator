---
description: Run a review methodology (e.g. Adversarial Review) to critique requirements/requirements.md.
---

Launch the review orchestrator at `framework/orchestrators/review-requirement-orch.md`.

Follow the orchestrator exactly — run the chosen reviewer in the prescribed foreground:

1. Prerequisite gate — `requirements/requirements.md` must exist and be non-empty. If absent, exit cleanly with the prerequisite message; do not invoke any agent.
2. Methodology selection — `framework/skills/analysis-selector.md` (invoked with `list_label: "reviews"`, `verb_label: "review"`) reads `framework/assets/reviews/registry.md` and presents the `status: mvp` rows as a grouped numbered list (clustered by `group`, with `★ suggested next` / `✓ already run` marks).
3. Prior-artefact gate per methodology — Overwrite / Keep / Cancel against `<chosen.output_path>`.
4. The selected reviewer agent (e.g. `framework/agents/reviews/adversarial-reviewer.md`) runs in the foreground — wait for the artefact to be accepted.

Honour the prerequisite gate, the context-bloat preflight (RF-05 review-requirement-orch surface variant), the per-methodology prior-artefact gate (Overwrite / Keep / Cancel), and the reviewer's handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator. The pipeline is stand-alone — the orchestrator and reviewer do not write to `requirements/`, `design-system/`, `analyse-requirements/`, `framework/state/`, or `framework/shared/`; the reviewer reads `requirements/requirements.md` only and writes a single artefact under `review-requirements/<METHOD>/`. For the Adversarial Review MVP, the final artefact is `review-requirements/ADVERSARIAL/adversarial-review.html`.
