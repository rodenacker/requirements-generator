# verify-artifact-write.md

**Purpose:** Confirm that a freshly-written artefact on disk matches the in-memory render that produced it. Run by every artefact-producing step (input-handler manifest, drafter draft, resolver answers, merger requirements, plus any sibling `*.converted.md` written by `convert-input-file.md`, plus every analyser's HTML/MD artefact across `/analyse-requirement` and `/analyse-inputs`) immediately after `Write` and before any schema or self-validation. Catches truncation, encoding glitches, wrong paths, and silent `Write` failures before downstream steps consume corrupt or absent artefacts.

**Inputs:**
- `path` — absolute or repo-relative path of the file just written.
- `expected_sha256` — sha256 of the in-memory render the writer just emitted.
- `expected_min_bytes` — caller-supplied lower bound on file size; defaults to `1` (non-empty).

**Outputs:** exactly one of:
- `pass` — the agent advances.
- `RF-04 trigger` — the agent halts per the `RF-04 artifact_write_unverified` surface in `framework/shared/refusal-registry.md`.

**Used by:**
- `framework/agents/input-handler.md` — after writing each `*.converted.md` sibling and after writing the source-manifest at `manifest_path` (always `requirements/source-manifest.json` in current usage). Shared between `/requirements` and `/analyse-inputs`.
- `framework/agents/requirements-drafter.md` — after writing `requirements/requirements-draft.md`.
- `framework/agents/requirements-resolver.md` — after writing `requirements/consultant-answers.md`.
- `framework/agents/requirements-merger.md` — after writing `requirements/requirements.md`.

## Procedure

Walk in order. Stop and return `pass` at the first attempt that satisfies all three predicates; stop and trigger `RF-04` after a second consecutive failure.

1. **Attempt 1 — read-back and check.**
    - `Read` the file at `path`.
    - **Existence:** the file exists.
    - **Non-empty:** the file is at least `expected_min_bytes` bytes.
    - **Hash match:** sha256 of the file's bytes equals `expected_sha256`.
    - If all three predicates hold, return `pass`.
2. **Silent retry — re-write and re-check.**
    - `Write` the in-memory render to `path` again. No consultant message; this is silent.
    - `Read` and re-evaluate the three predicates.
    - If all three hold, return `pass`.
3. **Trigger `RF-04`.**
    - The agent surfaces the predicate per `framework/shared/refusal-registry.md > RF-04 artifact_write_unverified` (plain-text halt, failed handback, no `AskUserQuestion`).
    - The orchestrator does not write a `completed` event for the calling agent.

## Self-validation

- Caller has supplied a non-null `expected_sha256` computed on the same byte-string passed to `Write`. A mismatch caused by hashing the rendered string vs the byte-encoded form is a caller bug, not a write failure — the hash must be computed on the bytes that landed on disk.
- `expected_min_bytes` is set deliberately by the caller. The default of `1` only catches truncation-to-empty; callers writing structured artefacts (the manifest, the draft, the merged spec) should set a tighter bound (e.g. the byte length of the smallest legal render).

## Anti-Patterns

- Do not retry more than once. The point of the predicate is to escalate persistent failure quickly so the consultant can investigate. Multi-retry loops mask filesystem misconfiguration and burn consultant time.
- Do not surface `RF-04` via `AskUserQuestion`. The choice set would be empty — there is no recoverable option when prior work cannot be verified on disk.
- Do not skip this skill on a "small" artefact. Truncation hits the manifest as readily as the merged spec; every artefact-producing step calls it.
- Do not run schema validation before this skill. Schema-validate only on `pass` — validating a corrupt file produces misleading errors that send the consultant looking in the wrong place.
