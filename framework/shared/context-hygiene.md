# context-hygiene.md

**Purpose.** Canonical wording + placement rule for the non-blocking "clear the conversation" suggestion each pipeline emits when it finishes successfully. This replaces the retired context-bloat preflight (`RF-05`, removed 2026-06-15 — see `framework/shared/refusal-registry.md`). Instead of a blocking gate keyed to a disk-byte proxy that did not track conversation context, the system offers a one-line suggestion at the point where `/clear` is actually actionable: the boundary between commands.

## The tip (canonical text — emit verbatim)

> Tip: before running another workflow in this conversation, consider `/clear` to keep context sharp. The resumable pipelines (`/requirements`, `/generate-prd`, `/prototype`) pick up where they left off when you re-invoke them after clearing.

## Placement rule

- Emit **once**, only on a pipeline's **successful completion** terminal — the consultant has accepted the final artefact / the orchestrator has reached its Definition of Done. **Never** on a cancel, prerequisite-exit, or refusal-halt branch.
- Plain text only. **No `AskUserQuestion`, no gate, no state write.** It is advisory; the consultant ignores or acts on it freely.
- The selection-loop pipelines (`/analyse-requirement`, `/analyse-inputs`, `/review-requirement`, `/review-inputs`) append it to their existing *"Done — ran N … this session."* exit line (the ran-≥1 branch only), rather than emitting a second message.
- The `/start` dispatcher carries a softer, conditional variant in its menu (see `.claude/commands/start.md`).

## Referenced by

`framework/orchestrators/{requirements,generate-prd,design-system,analyse-requirement,analyse-inputs,review-requirement,review-inputs,wireframe,prototype,export-application,resolve-review}-orch.md` and `.claude/commands/start.md`. The wording is defined **here only** (canonical-source rule); callers reference this file, they do not restate the line.
