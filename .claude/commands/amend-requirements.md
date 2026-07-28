---
description: Change a finished requirements.md — state the changes, and they are recorded as a new consultant-approved input document plus a transient Amendments section in the document.
---

Launch the amend-requirements orchestrator at `framework/orchestrators/amend-requirements-orch.md`.

Follow the orchestrator exactly — single-shot, single foreground agent:

1. Pre-flight on `requirements/requirements.md` — bounded `Grep` for the header's `Status` / `Last finalised at` plus the existing `AMD-NN` and `### Run ` counts (friendly exit when the document is absent; a non-`final` `Status` is surfaced as an advisory, **never** a gate).
2. Stale-draft gate on `amend-requirements/amendments-draft.md` (Discard / Cancel).
3. `framework/agents/amend-requirements-drafter.md` runs in the foreground: one full read of the document to build the anchor index, a printed intake for the consultant's changes (with a `list` affordance), per-change resolution with **per-item confirmation** — a fully-specified change is recorded as stated, a vague one gets ≥2 grounded candidate amendments to choose from, and there is **no accept-all path** — reconciliation against existing amendments, staged draft + accept/revise/restart, then finalise to a NEW dated `input/amendments-<date>.md` (never overwriting; same-day collisions suffix `-2`, `-3`, …). The drafter's Step 9 then applies the same accepted amendments as the transient `## Amendments (pending re-merge)` section in `requirements/requirements.md` via `framework/skills/apply-amendments-section.md` — **unconditionally**, since that projection is the pipeline's purpose. Step 10 prints a bounded advisory report: the amendment load, which downstream artefacts now predate the document (`blueprints/*/scope.json` + the application export), and explicitly what was not checked.

Honour the stale-draft gate and the drafter's handback gate defined in the orchestrator. Do not perform any task that is not listed in the orchestrator.

The `input/` document is the **durable** record — the next `/requirements` run ingests it as corpus and folds it into the body with `[SRC: C-NNN]` citations. The Amendments section is only its cache and disappears at that re-merge. A section write without the paired `input/` file is data loss, never a shortcut.

The pipeline is stand-alone: no progress file, no timing events, no input-handler invocation; the new input file is picked up by the next source-manifest create/refresh. This command is also reachable as the `amend` branch of `/requirements` Step 0 when a completed run is detected — same gates, same agent.
