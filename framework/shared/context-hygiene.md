# context-hygiene.md

**Purpose.** Canonical wording + placement rule for the non-blocking "clear the conversation" suggestion each pipeline emits when it finishes successfully. This replaces the retired context-bloat preflight (`RF-05`, removed 2026-06-15 — see `framework/shared/refusal-registry.md`). Instead of a blocking gate keyed to a disk-byte proxy that did not track conversation context, the system offers a one-line suggestion at the point where `/clear` is actually actionable: the boundary between commands.

## The tip (canonical text — emit verbatim)

> Tip: before running another workflow in this conversation, consider `/clear` to keep context sharp. The resumable pipelines (`/requirements`, `/generate-prd`, `/prototype`) pick up where they left off when you re-invoke them after clearing.

## Placement rule

- Emit **once**, only on a pipeline's **successful completion** terminal — the consultant has accepted the final artefact / the orchestrator has reached its Definition of Done. **Never** on a cancel, prerequisite-exit, or refusal-halt branch.
- Plain text only. **No `AskUserQuestion`, no gate, no state write.** It is advisory; the consultant ignores or acts on it freely.
- The selection-loop pipelines (`/analyse-requirement`, `/analyse-inputs`) append it to their existing *"Done — ran N … this session."* exit line (the ran-≥1 branch only), rather than emitting a second message.
- The review pipelines (`/review-requirement`, `/review-inputs`) do **not** emit the tip — they emit the **review completion message** below in its place.
- The `/start` dispatcher carries a softer, conditional variant in its menu (see `.claude/commands/start.md`).

## The review completion message (canonical text — emit verbatim, placeholders filled)

A review run ends the moment its artefact is accepted — the conversation is then carrying a full review, so the useful next steps are `/clear` and `/resolve-review`, not another review in the same context.

> ✓ {{method_name}} review accepted and saved to `{{output_path}}`.
> Next: 1) `/clear` to free up context. 2) `/resolve-review` and pick **{{METHOD_DIR}}** under *{{group}}* to turn its findings into decisions.

- `{{method_name}}` — the chosen registry row's `name`; `{{output_path}}` — its `output_path`.
- `{{METHOD_DIR}}` — the directory name directly containing `output_path` (e.g. `ADVERSARIAL`), which is how the `/resolve-review` picker labels the artefact.
- `{{group}}` — the `/resolve-review` picker group the artefact appears in: `Requirement reviews` for `/review-requirement`, `Input reviews` for `/review-inputs`. Needed because the same method dir can exist under both roots.

Placement: once, on the accepted-review terminal only (after the completion commit) — never on a cancel, `Keep`, prerequisite-exit, or refusal-halt branch. Plain text only; no `AskUserQuestion`, no gate, no state write.

## Referenced by

`framework/orchestrators/{requirements,generate-prd,design-system,analyse-requirement,analyse-inputs,review-requirement,review-inputs,wireframe,prototype,export-application,resolve-review}-orch.md` and `.claude/commands/start.md`. The review completion message is referenced by `framework/orchestrators/{review-requirement,review-inputs}-orch.md`. The wording is defined **here only** (canonical-source rule); callers reference this file, they do not restate the line.
