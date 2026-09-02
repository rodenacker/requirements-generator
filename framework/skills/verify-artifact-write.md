# verify-artifact-write.md

**Purpose:** Confirm that a freshly-written artefact on disk matches the in-memory render that produced it, and — for `.html` artefacts — that those bytes can be parsed as the document they were meant to be. Run by **every artefact-producing agent and step**, immediately after `Write` and before any schema or self-validation. Catches truncation, encoding glitches, wrong paths, silent `Write` failures, and doctype-losing HTML before downstream steps or a consultant's browser consume a corrupt, absent, or unparseable artefact.

**Inputs:**
- `path` — absolute or repo-relative path of the file just written.
- `expected_sha256` — sha256 of the in-memory render the writer just emitted.
- `expected_min_bytes` — caller-supplied lower bound on file size; defaults to `1` (non-empty).

**Outputs:** exactly one of:
- `pass` — the agent advances.
- `re-render required` — the file exists and hashes correctly, but is not doctype-first. The caller re-renders (see step 2b) and calls this skill **fresh**; this skill's work is done.
- `RF-04 trigger` — the agent halts per the `RF-04 artifact_write_unverified` surface in `framework/shared/refusal-registry.md`.

**Used by:** every artefact-producing agent and step, across every pipeline — each drafter, resolver, merger, exporter, analyser, reviewer, wireframe and prototype writer, and every `*.converted.md` sibling. There is no enumerated caller list to keep in sync: if a step calls `Write` on an artefact, it calls this skill next. Only the call sites carrying information a reader cannot derive are named:

- `framework/agents/input-handler.md` — **two** call sites: after writing each `*.converted.md` sibling, and after writing the source-manifest at `manifest_path` (always `generated-docs/requirements/source-manifest.json` in current usage). Shared between `/requirements` and `/analyse-inputs`.
- `framework/agents/requirements-merger.md` — after writing `generated-docs/requirements/requirements.md`, the document every downstream pipeline reads.
- `framework/agents/export-application-exporter.md` — after writing `generated-docs/export-application/requirements-application.md`. `expected_min_bytes` is **derived** (`source byte length − 6000`), never hard-coded: the export removes a near-constant PI appendix plus the §0.1 table and adds the provenance block, so the shortfall is constant in absolute terms while a ratio floor would loosen as documents grow.

## Procedure

Walk in order. Stop and return `pass` at the first attempt that satisfies every applicable predicate; return `re-render required` on a doctype-first failure; trigger `RF-04` after a second consecutive failure.

1. **Attempt 1 — read-back and check.**
    - `Read` the file at `path`.
    - **Existence:** the file exists.
    - **Non-empty:** the file is at least `expected_min_bytes` bytes.
    - **Hash match:** sha256 of the file's bytes equals `expected_sha256`.
    - **Doctype-first (`.html` only):** the file's first bytes are `<!doctype html>` (case-insensitive), ignoring an optional UTF-8 BOM and any leading whitespace. A BOM is not whitespace and browsers tolerate it — a naive "first non-whitespace bytes" reading would hard-fail a file that renders perfectly. This predicate applies to **every** `.html` write, not only review artefacts.
    - If every applicable predicate holds, return `pass`.
2. **Branch on which predicate failed.**
    - **2a. Existence / min-bytes / hash failed — silent retry.**
        - `Write` the same in-memory render to `path` again. No consultant message; this is silent.
        - `Read` and re-evaluate the predicates.
        - If they all hold, return `pass`. Otherwise go to step 3.
    - **2b. Doctype-first failed (existence, min-bytes and hash all held) — return `re-render required`.**
        - Do **not** re-`Write` the same bytes: they are the bytes the caller emitted, and re-writing them reproduces the same defect.
        - Do **not** re-render here. This skill is a pure verifier — a re-render produces different bytes, which makes the `expected_sha256` it was handed stale and forces the hash predicate to fail on any internal retry.
        - The **caller** re-renders, emitting from `<!doctype html>` (a template's header comment is scaffolding documentation and is never emitted), recomputes `expected_sha256` on the new bytes, `Write`s, and invokes this skill **fresh**. A second doctype-first failure goes to step 3.
3. **Trigger `RF-04`.**
    - The agent surfaces the predicate per `framework/shared/refusal-registry.md > RF-04 artifact_write_unverified` (plain-text halt, failed handback, no `AskUserQuestion`).
    - The orchestrator does not write a `completed` event for the calling agent.

## Caller obligation on `re-render required`

The calling agent treats `re-render required` as its **own self-validation FAIL** — the path its `Self-validation` section already documents via the `Self-contained HTML:` bullet — not as a transport failure. A malformed render is a content defect the agent produced; `RF-04`'s message points the consultant at disk and write investigation, which would misdirect. Only a **second** failure, after the re-render, escalates to `RF-04 artifact_write_unverified`. There is no new `RF-NN` and no change to `framework/shared/refusal-registry.md`.

## Self-validation

- Caller has supplied a non-null `expected_sha256` computed on the same byte-string passed to `Write`. A mismatch caused by hashing the rendered string vs the byte-encoded form is a caller bug, not a write failure — the hash must be computed on the bytes that landed on disk.
- `expected_min_bytes` is set deliberately by the caller. The default of `1` only catches truncation-to-empty; callers writing structured artefacts (the manifest, the draft, the merged spec) should set a tighter bound (e.g. the byte length of the smallest legal render).
- On a `.html` path, the doctype-first predicate was evaluated. It is not optional and not scoped to a pipeline — skipping it for one methodology is the hole this predicate exists to close.

## Anti-Patterns

- Do not retry more than once. The point of the predicate is to escalate persistent failure quickly so the consultant can investigate. Multi-retry loops mask filesystem misconfiguration and burn consultant time.
- **Do not treat a matching sha256 as licence to skip the structural predicate.** A hash match says the bytes on disk are the bytes that were emitted; it says nothing about whether those bytes parse. Both broken artefacts that motivated this predicate were byte-complete and hash-clean.
- **Do not re-render inside this skill.** It would invalidate the `expected_sha256` the caller supplied and turn a content defect into a spurious hash failure. Return `re-render required` and let the caller own the re-render.
- Do not surface `RF-04` via `AskUserQuestion`. The choice set would be empty — there is no recoverable option when prior work cannot be verified on disk.
- Do not skip this skill on a "small" artefact. Truncation hits the manifest as readily as the merged spec; every artefact-producing step calls it.
- Do not run schema validation before this skill. Schema-validate only on `pass` — validating a corrupt file produces misleading errors that send the consultant looking in the wrong place.
