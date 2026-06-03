# grounding-verifier.md

**Purpose:** Confirm that every unmarked template-field value in `requirements/requirements-draft.md` is grounded in an input document via a verbatim source-quote citation. Deterministic — no LLM calls. The check is a literal substring match (`Grep --fixed-strings`) of each `source_quote` against its claimed `source_file`, plus a bidirectional cross-check between `[SRC: C-NNN]` tags in the draft body and entries in `requirements/draft-claims.ndjson`. If the drafter cannot cite a verbatim substring for a field, that field must instead carry an `[AI-SUGGESTED]` marker — verbatim citation or `[AI-SUGGESTED]` is the closed system this skill enforces.

**Inputs (caller-supplied):**
- `claims_path` — **required** — repo-relative path to the drafter's claims sidecar (NDJSON, one JSON object per non-empty line). Defaults are not supplied; the caller must pass `requirements/draft-claims.ndjson`.
- `manifest_path` — **required** — path to `requirements/source-manifest.json`. Used to derive the allowlist of valid `source_file` paths (every row's `original_path` for `Native-text` / `Native-multimodal`, every row's `converted_sibling` for `Supported-via-MCP`; `Unsupported` rows contribute nothing).
- `draft_path` — **required** — path to `requirements/requirements-draft.md`. Used to extract the set of `[SRC: C-NNN]` tags present in the draft body for the bidirectional cross-check.
- `verification_path` — **required** — path the skill writes its NDJSON output to. Defaults are not supplied; the caller passes `requirements/draft-claims-verification.ndjson`.

**Outputs:** writes `verification_path` and prints a single summary line. Exit signal:
- `pass` — `failed: 0`. The agent advances.
- `fail` — `failed: > 0`. The agent loops per its own remediation contract; the orchestrator's drafter-handoff gate refuses to write a `completed` event until a subsequent run yields `pass`.

The skill itself does not surface refusal predicates. The drafter consumes the output and edits the draft + sidecar (or converts fields to `[AI-SUGGESTED]`) until `failed: 0`.

**Used by:**
- `framework/agents/requirements-drafter.md` — at workflow step 7b, after writing `draft-claims.ndjson`. Run repeatedly until `failed: 0`.
- `framework/agents/reviews/requirements-traceability-reviewer.md` — at its Band-A citation-integrity step, invoked with `draft_path = requirements/requirements.md` (the **final, merged** doc — whose retained `[SRC: C-NNN]` tags are the body under audit) and `verification_path` under `review-requirements/REQUIREMENTS-TRACEABILITY/.workspace/`. Run **once** (not to convergence — this is a read-only audit, not a remediation loop). The reviewer consumes the NDJSON, not the pass/fail exit signal.

**Final-doc caller note (the traceability reviewer):** This skill is artefact-neutral — `draft_path` may be the draft *or* the merged `requirements/requirements.md`. The Pass-2 reasons mean the same thing mechanically, but the **traceability reviewer re-interprets `sidecar_entry_without_tag` as a warn (DEAD-PROVENANCE), not a failure**: against the final doc, a sidecar entry with no tag means the merger legitimately dropped a cited field (e.g. a `dropped` resolution removed a cited row), which is informational, not an ungrounded fact. `tag_without_sidecar_entry`, `quote_not_found`, and `source_not_in_manifest` remain hard BROKEN-CITATION signals. When the input source files have been deleted post-generation (the merger permits this), the reviewer skips Pass 1 and substitutes the draft-time record in `requirements/draft-claims-verification.ndjson`; the skill itself is unchanged.

## Procedure

### Pass 0 — load

1. `Read` `manifest_path` and parse JSON. Build the `allowlist` set:
   - For each row with `tier ∈ {"Native-text", "Native-multimodal"}`: add `original_path`.
   - For each row with `tier = "Supported-via-MCP"`: add `converted_sibling`.
   - Skip rows with `tier = "Unsupported"`.
2. `Read` `claims_path`. Parse each non-empty line as one JSON object: `{claim_id, draft_locator, claim_text, source_file, source_quote}`. Build `sidecar` keyed by `claim_id`. A duplicate `claim_id` is a FAIL with reason `duplicate_claim_id` recorded against the second-and-later occurrence; the first occurrence still runs Pass 1.
3. `Read` `draft_path`. Extract every `[SRC: C-NNN]` token via Grep with pattern `\[SRC: C-\d{3}\]`. Build `draft_ids` as a set of the `C-NNN` strings.

### Pass 1 — sidecar quote check (the core grounding test)

For each entry in `sidecar`, in `claim_id` order, emit one NDJSON line to `verification_path`:

```
{"claim_id":"C-NNN","status":"pass|fail","reason":"<reason>"}
```

Predicates (first failure short-circuits to FAIL for that claim):

- `source_file_in_manifest`: `source_file` ∈ `allowlist`. Otherwise FAIL with `reason: source_not_in_manifest`.
- `quote_found`: run `Grep` against `source_file` with the literal `source_quote` as the pattern, using fixed-string semantics (Grep's default is regex; pass the quote so its bytes match literally — escape only the regex metacharacters `[ ] ( ) { } . * + ? ^ $ | \` if calling Grep directly, or use a tool flag equivalent to `--fixed-strings`). At least one match is required. Otherwise FAIL with `reason: quote_not_found`.

Both predicates pass → emit `status: "pass"` with `reason: "ok"`.

### Pass 2 — bidirectional cross-check

After Pass 1 completes, compute:

- `tag_without_sidecar = draft_ids − sidecar.keys()` — every `C-NNN` tag in the draft body has a sidecar entry.
- `sidecar_without_tag = sidecar.keys() − draft_ids` — every sidecar entry has a tag in the draft body.

For each `id` in `tag_without_sidecar`, emit:

```
{"claim_id":"C-NNN","status":"fail","reason":"tag_without_sidecar_entry"}
```

For each `id` in `sidecar_without_tag`, emit:

```
{"claim_id":"C-NNN","status":"fail","reason":"sidecar_entry_without_tag"}
```

If a `claim_id` already has a Pass 1 line, the Pass 2 line is appended as an additional record — both signals are kept for the drafter's remediation report.

### Summary line

After all NDJSON lines are written, print exactly one summary line to stdout:

```
grounding-verifier: total=<N> passed=<P> failed=<F>
```

Where `total` is the count of entries in `sidecar` (Pass 1 denominators), `passed` is Pass-1 entries with `status: "pass"`, and `failed` is the count of `status: "fail"` lines emitted across both passes (so cross-check failures count toward `failed` even when they have no Pass-1 line).

`failed: 0` is the only condition under which the drafter may advance.

## Self-validation

- All three input paths are supplied by the caller; the skill has no defaults and refuses to run with any missing.
- `claims_path` is parsed strictly as NDJSON: one JSON object per non-empty line. A line that fails to parse is itself a FAIL with `reason: ndjson_parse_error` recorded against synthetic `claim_id: "<line:N>"`.
- The `Grep` for `quote_found` matches as a literal byte-substring of `source_file`'s contents; multi-line quotes are supported when the underlying Grep tool supports them (the caller selects multiline mode where applicable). Whitespace inside `source_quote` is matched verbatim — leading or trailing whitespace differences cause a FAIL.
- `verification_path` is written even on `failed: 0` so the drafter and orchestrator's handoff gate can read the file and trust its summary line without re-running the skill.
- The skill performs no transformation of the draft, the sidecar, or the manifest. Its only side effect is the write to `verification_path` and the summary print.

## Anti-Patterns

- Do not call any LLM. The check is purely deterministic substring matching plus set-difference.
- Do not "soft-match" a quote — no whitespace normalisation, no case folding, no punctuation stripping. The drafter's contract is verbatim citation; loosening the match would let paraphrase masquerade as grounding.
- Do not infer `source_file` from `source_quote` if the manifest lookup fails. A FAIL with `reason: source_not_in_manifest` is the correct signal — the drafter must edit either the citation or the manifest, not have the verifier guess.
- Do not modify the draft, the sidecar, or the manifest. Remediation is the drafter's job; this skill only reports.
- Do not skip Pass 2. A draft tag with no sidecar entry is a silent ungrounded fact; a sidecar entry with no draft tag is dead provenance pointing at content that may have been deleted. Both must surface.
- Do not run Pass 1 before Pass 0 has parsed the manifest and the sidecar. Out-of-order execution can falsely PASS a claim whose `source_file` is not actually allowlisted, because the allowlist set was empty at the time of the check.
