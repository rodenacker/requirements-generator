# check-manifest-freshness.md

**Purpose:** Compare the on-disk state of `input_dir` against the rows recorded in the manifest at `manifest_path`. Return a structured verdict the caller can branch on. Pure read-only — never writes, never mutates, never surfaces `AskUserQuestion`.

**Inputs:**
- `manifest_path` — repo-relative path to the manifest JSON. Required.
- `input_dir` — repo-relative path to the input folder. Required.

**Outputs:**
- A structured verdict row returned to the caller:
  - `{ verdict: "fresh" }` — manifest fully matches disk.
  - `{ verdict: "stale", removed: [...], added: [...], modified: [...] }` — at least one set of files differs. Lists are repo-relative `original_path`-shaped strings, sorted in lexicographical order for deterministic output.
  - `{ verdict: "corrupt-manifest" }` — manifest fails to parse or fails schema check.

**Used by:**
- `framework/agents/input-handler.md` — called at the agent's step 0 (the new manifest-action gate) to decide whether to no-op (fresh), surface the drift prompt (stale), halt (corrupt), or fall through to the create flow (absent — note: absence is the caller's branch, not this skill's; absence is included defensively below but is not the normal entry path).

## Algorithm

1. **Read manifest.**
    - Glob `manifest_path`. If absent → return `{ verdict: "corrupt-manifest" }` defensively (callers are expected to test absence themselves before invoking this skill; reaching here with an absent manifest is a caller bug).
    - Otherwise `Read manifest_path` and JSON-parse the contents. If parse fails → return `{ verdict: "corrupt-manifest" }`.
    - Schema check: the parsed object must have root-level `schema_version`, `generated_at`, `target`, `rows`; every row in `rows` must have all seven row-level fields per `framework/skills/build-source-manifest.md > Schema` (`filename`, `tier`, `kind`, `sha256`, `conversions_applied`, `original_path`, `converted_sibling`). On any schema failure → return `{ verdict: "corrupt-manifest" }`.

2. **Enumerate disk.** Glob `input_dir`, excluding:
    - Dotfiles (paths whose basename begins with `.`).
    - Any path the consultant has reserved as a scratch file by prefixing it with `.`.
    - `*.converted.md` siblings — these are input-handler outputs, not consultant-dropped originals. (Same exclusion the input-handler applies at its own enumeration step.)
    - **Stadium application units** — `*.stadium` pointer files, and every path under a directory that directly contains `administration.db` (a deployed Stadium 6 app folder). These are never manifest rows: the `/ingest-stadium` command turns them into `input/<AppName>.stadium-assets/*.md` assets (which **are** enumerated here as ordinary files), and the input-handler's Step S keeps the raw app folder / pointer out of enumeration. Including the app folder/pointer would generate spurious `added` drift on every run. (Same exclusion the input-handler applies at its Step-1 enumeration.)
    Call this set `disk_files` (set of repo-relative paths of the same shape as the manifest's `original_path` field).

3. **Extract manifest rows.** From the parsed manifest, build `manifest_files` — the set of every row's `original_path`, regardless of `tier`. Unsupported rows are included; the freshness check is about whether the manifest's *enumeration* still matches disk, not about whether files are consumable.

4. **Compute set diff.**
    - `removed = manifest_files − disk_files` — paths the manifest records but disk no longer has.
    - `added = disk_files − manifest_files` — paths disk has but the manifest does not record.

5. **Compute hash diff over the intersection.** For each file in `manifest_files ∩ disk_files`:
    - Compute sha256 of the file's current bytes (PowerShell `Get-FileHash -Algorithm SHA256`; lower-case the hex digest to match the manifest's emission convention).
    - Compare against the manifest row's `sha256` field.
    - Collect non-matches as `modified`.

6. **Verdict.**
    - If `removed`, `added`, and `modified` are all empty → return `{ verdict: "fresh" }`.
    - Otherwise → return `{ verdict: "stale", removed, added, modified }`.

## Self-validation

- The manifest was parsed via JSON-decode and conformed to the schema in `framework/skills/build-source-manifest.md > Schema` before any comparison ran.
- The `disk_files` enumeration applied all four documented exclusions (dotfiles, scratch-prefixed, `*.converted.md` siblings, Stadium application units).
- For every file in `manifest_files ∩ disk_files`, a sha256 was computed against the current bytes and compared.
- The returned verdict is exactly one of `fresh`, `stale`, or `corrupt-manifest`.
- When the verdict is `stale`, at least one of `removed`, `added`, or `modified` is non-empty. When the verdict is `fresh`, all three are empty.

## Tools

- Read — read the file at `manifest_path`.
- Glob — enumerate `input_dir`; check existence of `manifest_path`.
- Bash — compute sha256 over each file in `manifest_files ∩ disk_files` (PowerShell `Get-FileHash -Algorithm SHA256`). No other Bash usage is permitted; in particular, the skill never writes to disk or modifies any file.

## Anti-Patterns

- Do not write to disk. This skill is pure read-only — the caller decides what to do with the verdict.
- Do not surface `AskUserQuestion` from inside this skill. Consultant interaction on a stale manifest is the caller's responsibility (the input-handler's drift prompt at its step 0). Surfacing a prompt from here would couple the skill to one caller's UX.
- Do not include `*.converted.md` siblings in `disk_files`. The manifest's row set does not include them as separate entries (per `framework/skills/build-source-manifest.md > Anti-Patterns`); including them in `disk_files` would generate spurious `added` rows on every call after the input-handler's first successful conversion.
- Do not compute sha256 over a `*.converted.md` sibling. The manifest's `sha256` is on the original; comparing against a sibling's bytes would always report `modified`.
- Do not interpret the manifest's `target`, `schema_version`, or `generated_at` fields. The freshness check is bounded to the `rows` array.
- Do not return additional fields beyond `verdict`, `removed`, `added`, `modified`. Callers branch only on these.
- Do not call `framework/skills/verify-artifact-write.md`. That skill is for write-side verification of a freshly-emitted artefact; this skill performs a read-side comparison and writes nothing.
- Do not rebuild or modify the manifest on a `stale` verdict. Refresh is the caller's responsibility (the input-handler's create-or-refresh workflow); this skill only diagnoses.
- Do not silently classify `stale` as `fresh` when only `sha256` differs but the file lists match. A modified file is a manifest drift; the caller must decide whether to refresh or proceed-stale, and that decision needs the `modified` list to be honest.
