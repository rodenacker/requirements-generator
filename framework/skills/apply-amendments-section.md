# apply-amendments-section.md

**Purpose:** Insert or extend the single transient `## Amendments (pending re-merge)` section in `requirements/requirements.md` from a set of consultant-approved amendment entries held in memory, and verify the write. Owns the mechanics that must not diverge between callers: the placement rule, `AMD-NN` continuation numbering, the byte-isolation guarantee, the pairing assertion against the paired `input/` document, and the write-verify. The **shape** of the section and of each `AMD-NN` block is not defined here — it is canonical in `framework/assets/resolve-review/template-addendum.md`, which this skill reads.

Extracted from `framework/agents/resolve-review-drafter.md` Step 9b (items 2–6) when a second caller appeared; the caller-specific parts — deciding *whether* to apply the section, and composing the entry content — deliberately stay with the callers.

**Inputs:**
- `doc_path` — the host document. Always `requirements/requirements.md` in current usage.
- `doc_content` — the **full current text** of `doc_path`, as the caller read it in this run. Passed in rather than re-read so the caller's existing read is reused (both callers already hold the full document at the point they invoke this skill). The caller must not have written `doc_path` between its read and this invocation.
- `entries[]` — ordered amendment entries, one per accepted amendment, each an object:
    - `one_liner` — the block heading text (the one-line problem or change).
    - `amends` — the fully-rendered Amends payload: the base anchor (`§N.N` / `F-NN` / `BR-NN` / `US-NN` / `Shape.Field` / an existing `AMD-NN`) plus a short verbatim quote of the superseded base text, **or** the template's net-new sentinel.
    - `amendment_prose` — the declarative resolution/amendment prose, verbatim as accepted.
    - `origin_marker` — exactly one of `CONSULTANT-STATED` / `AI-INFERRED, CONSULTANT-CONFIRMED`.
    - `grounding` — the fully-rendered Grounding payload (tag + one-line implication), or `null` to omit the line entirely.
- `run_header` — the fully-rendered `### Run …` sub-block header line. Caller-specific by design: `/resolve-review` renders the review-sourced form, `/amend-requirements` the consultant-sourced form. Both forms are defined in `template-addendum.md`.
- `source_doc_path` — the paired `input/` document written and verified **before** this invocation. Used for the pairing assertion; never modified.

**Outputs:** exactly one of:
- `pass` — the section was inserted or extended and the write verified. The caller records its applied outcome.
- `RF-04 trigger` — the write could not be verified. The caller halts per `framework/shared/refusal-registry.md > RF-04`, **leaving `source_doc_path` in place** (it is the durable record and is never rolled back), and reports the split outcome honestly.

**Used by:**
- `framework/agents/resolve-review-drafter.md` — Step 9b, review-**requirements**-sourced runs only, after its addendum opt-in returns Apply.
- `framework/agents/amend-requirements-drafter.md` — Step 9, unconditionally (applying the section is that pipeline's purpose, so it has no opt-in ask).

## Procedure

1. **Read the canonical shape.** `Read framework/assets/resolve-review/template-addendum.md` once. It defines the section heading text, the preamble blockquote, the `AMD-NN` block shape, the `### Run …` header forms, the placement rule, and the lifecycle note. Do not restate or re-derive any of them here — read them from the asset.
2. **Locate the section.** Search `doc_content` for the literal heading `## Amendments (pending re-merge)`.
    - **Present** → *extend* mode. Find the highest existing `AMD-NN` in that section; the first new entry is numbered from `highest + 1`. Do **not** insert a second section.
    - **Absent** → *insert* mode. The whole section is emitted, preamble blockquote included, and numbering starts at `AMD-01`.
    - More than one such heading found → the host document is already malformed. Return `RF-04 trigger` without writing; the caller reports it. (A second section would make supersession ambiguous for every downstream reader, so this fails closed rather than guessing which one is authoritative.)
3. **Render the entries.** For each element of `entries[]`, in the given order, render one block per the template's `#### AMD-NN — …` shape: heading with the assigned zero-padded number and `one_liner`; the `**Amends:**` line from `amends`; the `**Amendment**` line carrying `` `[<origin_marker>]` `` and `amendment_prose`; and the `**Grounding:**` line **only** when `grounding` is non-null (omit the whole line otherwise). Numbering is continuous and zero-padded, assigned in `entries[]` order. No `{{…}}` token may survive into the render.
4. **Place the render.**
    - *extend* mode → append `run_header` plus its rendered blocks at the end of the existing section's body, after the last existing block and **before** whatever follows the section.
    - *insert* mode → build the full section (heading, preamble blockquote with its placeholders resolved, `run_header`, blocks) and insert it immediately **before** the `## Prototype invariants` heading when that appendix exists; at EOF when it does not. The before-PI placement is load-bearing, not cosmetic: `/export-application` strips PI-heading→EOF, so anything placed after that heading is silently deleted at export.
    - In both modes, **no other byte of the document changes.** Every other section, the header line, the base text, and any pre-existing `AMD-NN` block are byte-identical in the output.
5. **Write and verify.** Compute the sha256 of the full amended document as assembled in memory. `Write doc_path`. Invoke `framework/skills/verify-artifact-write.md` with that `path`, that `expected_sha256`, and `expected_min_bytes = 1024`.
6. **Return.** `pass` from the verify → return `pass`. `RF-04 trigger` from the verify → return `RF-04 trigger`.

## Self-validation

Run against the in-memory render **before** the Write at step 5, and against the returned result after it:

- Exactly one `## Amendments (pending re-merge)` heading exists in the render.
- Every rendered block carries exactly one origin marker, spelled exactly as `framework/assets/resolve-review/template-resolutions.md` defines it (that file is the canonical marker legend; this skill neither redefines nor accepts a variant spelling).
- `AMD-NN` numbering is continuous, zero-padded, and — in *extend* mode — starts at one above the highest pre-existing entry. No number is reused.
- **Pairing invariant:** every entry's `amendment_prose` appears verbatim in `source_doc_path`. Nothing was added, dropped, or rephrased on the way into the document. An amendment that exists only in the host document is a contract violation — return `RF-04 trigger` rather than writing it.
- In *insert* mode the section sits immediately before the `## Prototype invariants` heading, or at EOF when no PI appendix exists.
- Diffing the render against `doc_content` shows changes **only** inside the inserted or extended section.
- Zero `{{…}}` placeholder tokens survive in the render.
- `source_doc_path` was not read for content beyond the pairing check, and was not modified.

## Anti-Patterns

- Do not decide **whether** the section should be applied. That is the caller's decision — an opt-in ask in `/resolve-review`, unconditional in `/amend-requirements`. This skill applies what it is given.
- Do not compose entry content. `amendment_prose`, `amends`, and `grounding` arrive fully rendered from the caller, which is the only component that knows what the consultant approved.
- Do not re-read `doc_path`. The caller passes `doc_content` precisely so the document is read once per run; a second read here would double the largest read in either pipeline.
- Do not insert a second `## Amendments (pending re-merge)` section, and do not merge two into one. One section, extended in place, always.
- Do not place the section after the `## Prototype invariants` heading. `/export-application` strips PI-heading→EOF and the amendments would vanish at export with no error.
- Do not touch a byte outside the section. In particular, do not restamp the header line, do not reflow neighbouring sections, and do not "tidy" pre-existing `AMD-NN` blocks.
- Do not roll back `source_doc_path` on an `RF-04`. The `input/` document is the durable record; the section is a cache. Losing the cache is recoverable, losing the record is not.
- Do not renumber or rewrite pre-existing `AMD-NN` entries to close gaps. Numbering is append-only within the section's life.
- Do not restate the section's shape, preamble text, or `### Run …` header forms in this file. They are read from `framework/assets/resolve-review/template-addendum.md` at step 1 (canonical-source rule, `docs/maintenance.md`).
