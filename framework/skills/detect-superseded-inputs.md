# detect-superseded-inputs.md

**Purpose:** Decide which enumerated inputs are **left out** of the source manifest because they are an **exact duplicate** of another input or an **old version** the consultant has confirmed. Real client drops carry old versions, archive folders and copies; mining an old version is worse than missing a current one, so the consultant confirms every old-version call once, and the answer persists. Detection uses **names, folders and hashes only** — never file contents.

A left-out input is never deleted, moved or renamed (`framework/shared/input-safety.md`, `IS-01`, `IS-02`). It becomes a manifest row with `tier: "Unsupported"`, so every consumer, the Read-path rule and the grounding verifier already skip it (`framework/skills/build-source-manifest.md > Field rules`).

**Inputs:**
- `candidates` — every enumerated path to consider: `[{ relpath, sha256, mtime, kind }]`. `relpath` is relative to `documentation_dir` with forward slashes (the manifest `filename`). `kind` is `"file"` or `"stadium-unit"`. For a `stadium-unit`, `relpath` is the unit's folder or `*.stadium` pointer, and `sha256` is the pointer file's digest or, for a folder, the digest of the UTF-8 `app_id` string; a unit also carries `app_id`.
- `state_path` — the decisions file. Default `framework/state/.input-versions.json`.
- `exempt` — optional extra globs (relative to `documentation_dir`) exempt from detection, added to the fixed list in **1. Exemptions**. Default `[]`.

**Outputs:**
- `{ left_out: { <relpath>: <conversions_applied string> }, advisories: [<string>] }`. Each value is one of the left-out strings in `framework/skills/build-source-manifest.md > Field rules`: `skipped — duplicate of <relpath>`, `skipped — superseded by <relpath>`, `skipped — superseded (archive folder)`, `skipped — marked old by consultant`. `advisories` holds the plain-text status lines for the caller to emit.
- The state file at `state_path`, written and verified only when the gate was answered.

**Used by:**
- `framework/agents/input-handler.md` — Step V, over the pass's single enumeration (`kind: "file"`).
- `framework/agents/stadium-ingestor.md` — before extraction, over the detected Stadium units (`kind: "stadium-unit"`).

## State file

`state_path` holds one JSON object keyed by `relpath`:

```json
{
  "spec/spec-v1.md": { "sha256": "<hex>", "decision": "superseded", "superseded_by": "spec/spec-v2.md", "decided_at": "<ISO-8601 UTC>" },
  "spec/spec-v2.md": { "sha256": "<hex>", "decision": "current", "superseded_by": null, "decided_at": "<ISO-8601 UTC>" }
}
```

- `decision` is exactly one of `current`, `superseded`, `excluded-by-consultant`. A **keep** is recorded as `current`, so a kept file is never re-asked.
- `superseded_by` is the current file's `relpath`, or `null` for an archive-folder file with no partner and for `current` / `excluded-by-consultant`.
- Treat an absent or unparseable file as `{}`. No reset deletes it; it is staged by `framework/skills/commit-run-outputs.md` for the input pipelines.

## Procedure

Run the sections in order.

### 1. Exemptions

These are never duplicates and never versions — skip them entirely (they stay live inputs):

- top-level `amendments-*.md` (`/amend-requirements` documents are cumulative, each one a separate consultant-approved input);
- top-level `<filename_stem>-<date>[-N].md` for every `filename_stem` in `framework/assets/resolve-review/methodology-map.md` (`/resolve-review` documents, likewise cumulative);
- top-level `*.analysis.md` (re-ingestion extracts);
- anything under `**/*.stadium-assets/**` or `**/*.media/**` (framework-generated directories follow their source: `/ingest-stadium` units for the first, the parent document for the second — see the input-handler's Step V for how a media directory inherits its parent's status);
- every glob in `exempt`.

### 2. Duplicates

Among the remaining `kind: "file"` candidates, every set of two or more sharing one `sha256` is a duplicate set. **No question** — the outcome is determined. Keep one canonical copy, chosen by, in order:

1. not in an archive folder (signal in **3**) over in one;
2. the **5. Ranking** order, steps 1–4 only — never `mtime`: identical bytes carry no recency signal, and a sync or re-copy that touches `mtime` must not flip which copy is canonical (that would retire a cited `filename` and raise drift with nothing changed);
3. the shallowest path;
4. the lexicographically first `relpath`.

Every other copy is left out as `skipped — duplicate of <canonical relpath>` and takes no further part below. Add one advisory when at least one copy was left out: `Duplicates: N file(s) left out as exact copies.`

Byte-identical files are resolved here, before versions, so an identical copy is never put to the consultant as an "old version". The archive- and rank-aware choice is what guarantees the surviving copy is the current one — `current/policy.md` survives over an identical `archive/policy.md`.

### 3. Signals and grouping

Compute for each remaining candidate (for a `stadium-unit`, use the unit folder's basename or the pointer's stem as the name):

- **Normalised stem.** Lowercase; drop the extension; remove date tokens (`\d{4}-\d{2}-\d{2}`, `\d{2}\.\d{2}\.\d{4}`, `\d{8}`, `\d{4}-\d{2}`) and copy counters (`\(\d+\)`); split the rest into tokens on spaces, `-`, `_` and `.`; drop version tokens (`v\d+`, `rev\d+`, `r\d+`, and `v` / `version` followed by a number token) and status words (`final`, `draft`, `old`, `latest`, `new`, `updated`, `copy`, and `of` directly after `copy`); join the remaining tokens with single spaces. If nothing remains, the normalised stem is the lowercase stem unchanged.
- **Version token** (highest number wins), **in-name date** (latest wins), **status word** (rank `final`/`latest`/`new`/`updated` > none > `draft`/`old`/`copy`), each read from the name.
- **Archive signal** — any folder component of `relpath` is, case-insensitively, `old`, `archive`, `archived`, `superseded`, `previous`, `deprecated` or `backup`.

Then:

- **Version group** — candidates sharing a normalised stem, across folders and extensions. For `stadium-unit`s, units sharing an `app_id` always form one group too.
- **Series rule.** A group whose members' **names** (stems, ignoring folder and extension) differ only by date tokens and/or copy counters, with no member carrying a version token, a status word or the archive signal, is a **series** (`minutes-2026-01-05.md` / `minutes-2026-01-12.md`, `Screenshot (1).png` / `Screenshot (2).png`): every member is current and the group is **not** a candidate. Differing folders or extensions do not disqualify a series (`meetings/jan/minutes-2026-01-05.md` / `meetings/feb/minutes-2026-02-02.md` is a series).
- **Low confidence.** A group whose members carry no version token, status word or archive signal, and do not differ by date token or copy counter — they differ only by folder and/or extension (`a/notes.md` / `b/notes.md`) — is a candidate flagged `low confidence`. **Exception:** a group of `stadium-unit`s sharing an `app_id` is never `low confidence` — only one deployment of an app can be current, so the gate must name exactly one.
- **Every other group of two or more** is a candidate.
- **Lone archive file.** A candidate with the archive signal and no group partner is a candidate on its own.

### 4. Prior decisions

A candidate whose `relpath` has a state entry with the **same** `sha256` is **decided**; any other candidate is **undecided**. A changed `sha256` makes it undecided again.

A decided entry is applied whether or not its file forms a group this run: an `excluded-by-consultant` file never had a group, and a `superseded` file may have lost its partner. Every non-exempt input `candidates` path with a matching entry takes that entry's decision (**7**).

- A group (or lone archive file) whose members are all decided is not re-asked: apply the recorded decisions.
- A group with at least one undecided member is re-ranked (**5**) and re-proposed. Members already decided `superseded` or `excluded-by-consultant` keep that decision and are not listed again; a member decided `current` that no longer ranks top **is** listed, as newly superseded.

### 5. Ranking

Inside a group the top member is **current** and the rest are proposed as superseded. Compare, in order:

1. highest version token;
2. latest in-name date;
3. not in an archive folder over in one;
4. `final` / `latest` / `new` / `updated` over no status word over `draft` / `old` / `copy` (including `copy of` and `- Copy`) — a copy is never preferred to its original;
5. latest `mtime`;
6. lexicographically first `relpath` (determinism only).

A member **without** a version token ranks below every member with one; likewise a member without an in-name date ranks below every member with one.

An archive-folder member is always proposed as superseded, even when it ranks top: if every member is in an archive folder, each is proposed as `superseded (archive folder)`; otherwise archive members are superseded by the top non-archive member.

### 6. Gate

Fires **only** when the proposal contains something to decide: at least one file **newly** proposed to be ignored in a normal group, or a `low confidence` group none of whose members has a state entry yet. Otherwise the outcome is determined — e.g. the consultant edited the current file of a group, which makes it undecided but proposes nothing new — so there is no question: record the re-proposed members as `current` with their new `sha256` (merged and verified as below) and continue. On a run with nothing undecided there is no question either.

Build the proposal: one line per group or lone file — group name, current file, files to ignore, the deciding signal (`version token`, `in-name date`, `archive folder`, `status word`, `newer file`), and `low confidence` where it applies. Files in a normal group are **ticked** (to be ignored). Files in a `low confidence` group are **unticked** (kept) unless the consultant ticks them — a same-name pair with no other signal is too weak to drop by default.

Surface one `AskUserQuestion`, header `Old versions`, single-select. Question text: *"`{documentation_dir}` contains files that look like old versions. Ignored files stay on disk but are not read or cited. How would you like to proceed?"* Every option carries the full proposal table in its `preview`. Options:

1. *"Ignore them as proposed"* (Recommended) — apply the ticks as shown.
2. *"Let me adjust the list"* — ask the consultant, in plain text, which files to keep and which other files to ignore; apply the changes and re-present this gate with the updated proposal. Repeat until option 1 or 3 is chosen.
3. *"Keep everything"* — every listed file is kept.

Write the state file **immediately** after the answer, before anything else in the caller runs, so the answer survives a later *Cancel*. **Merge** into the existing parsed object — the file has two writers (the input-handler and `/ingest-stadium`), so every key this gate did not decide is preserved byte-for-byte: one entry per listed file and per group's current file — `superseded` (with `superseded_by`), `current`, or `excluded-by-consultant` for a file the consultant added that the proposal did not list. `Write` the whole object, then call `framework/skills/verify-artifact-write.md` (`RF-04` hard halt on mismatch).

### 7. Result

Build `left_out` from the duplicates (**2**) and every non-exempt input `candidates` path whose state entry (same `sha256`) is now `superseded` or `excluded-by-consultant` — grouped this run or not:

- `superseded` with a `superseded_by` → `skipped — superseded by <superseded_by>`;
- `superseded` with `superseded_by: null` → `skipped — superseded (archive folder)`;
- `excluded-by-consultant` → `skipped — marked old by consultant`.

When at least one old version is left out, add the advisory `Old versions: N file(s) left out (decisions in framework/state/.input-versions.json).`

## Self-validation

- No exempt path appears in `left_out`.
- Every duplicate set kept exactly one copy, and that copy is not in `left_out`.
- No series group was a candidate.
- The gate fired if and only if the proposal had something to decide (**6**); whenever the state file was written it was merged, not replaced, and verified before return.
- No `stadium-unit` group sharing an `app_id` was flagged `low confidence`; no series was split by folder or extension.
- Every `left_out` value is one of the four strings above, and every `superseded by <relpath>` names a path that is not itself left out as a duplicate.
- No file was read beyond its hash and modification time; nothing was deleted, moved or renamed.

## Anti-Patterns

- Do not read file contents to decide "is this a version of that". Names, folders and hashes only; a content diff costs a conversion per file and is still a guess.
- Do not delete, move or rename a left-out file. Ignoring is a manifest row (`IS-02`).
- Do not default to *Keep everything*, and do not drop the gate because the proposal looks obvious: an old version is a consultant call. Only exact duplicates are decided without asking.
- Do not treat a dated or numbered series as versions, or a framework-authored dated document as an old version of its predecessor (**1**, **3**).
- Do not re-ask a decided file whose `sha256` is unchanged, and do not forget a *keep*: it is recorded as `current`.
- Do not pre-tick a `low confidence` group.
