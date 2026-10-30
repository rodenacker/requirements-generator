# Input Exclusions

Single source of truth for **what is *not* a source-manifest input** when an agent enumerates the
consultant-dropped documentation folder (`documentation_dir`, canonically `documentation/`). Every path that matches an exclusion
below is skipped: it never becomes a manifest row and never counts as disk drift.

> **Excluding is not deleting.** A path excluded here is never read into a manifest row — it is **not** deleted or moved. Input files are consultant-owned; see `framework/shared/input-safety.md` (`IS-02`).

This registry exists because input enumeration happens in **two independent places** that must agree exactly
or a file silently becomes "drift":

- `framework/agents/input-handler.md` — **Step 1** (create/refresh enumeration) and **Step S** (Stadium
  detect-and-register, which runs first so a detected unit is excluded before both Step 1 and the Step-0
  freshness call).
- `framework/skills/check-manifest-freshness.md` — **Step 2** (disk enumeration for drift diffing).

Both apply the exclusions below verbatim. `framework/skills/build-source-manifest.md` does **not** enumerate —
it receives already-filtered rows — so it is not a third exclusion site.

Add new exclusions by appending a new `IX-NN`; never renumber. When a caller's prose summarises an exclusion,
this file is authoritative — a caller that diverges from an `IX-NN` definition is the bug. *(2026-10-30:
`IX-01`, `IX-03` and `IX-05` were amended in place for recursive enumeration; no `IX-NN` was renumbered.)*

## Enumeration depth

Both enumeration sites walk `documentation_dir` **recursively, at any folder depth**. A consultant may drop
material in topic folders (`pricing/workshop-notes.md`); it is an input exactly like a top-level file.

- **Pruning.** A directory that matches `IX-01` (a dot-prefixed component) or `IX-03` (a Stadium unit) is
  **pruned**: it is not descended into, so nothing beneath it is ever listed. Pruning is what keeps a
  nested Stadium app's `ClientApp/` tree, or a `.git/` folder, out of the walk entirely.
- **Every other rule** below applies to each file the walk reaches, wherever it sits.
- **Order.** Rows are ordered by path relative to `documentation_dir`, ascending (ordinal), with forward slashes.
- **Mechanism.** The walk is performed by one deterministic tool, `node framework/tools/enumerate-inputs.cjs <documentation_dir>` (`framework/tools/enumerate-inputs.cjs`, unit-tested by `enumerate-inputs.test.cjs`). It applies this section and `IX-01`..`IX-04` mechanically and prints `{ files: [{ relpath, sha256, mtime }], stadium_units: [{ relpath, kind }] }`. Every enumeration site calls it rather than the Glob tool: Glob cannot prune and silently truncates large result sets, so two sites globbing the same tree can list different paths. The tool is the rendering; this file stays the rule — a change here is a change to the tool and its tests.

A file's identity is its path relative to `documentation_dir` (the manifest `filename` — see
`framework/skills/build-source-manifest.md > Field rules`). Which reached files are then left out as old
versions or exact duplicates is decided after enumeration by `framework/skills/detect-superseded-inputs.md`;
those files are still enumerated (they become left-out rows), so that decision is not an exclusion here.

## IX-01 — Dotfiles and consultant scratch files

Any path in which **any component below `documentation_dir`** begins with `.` — dotfiles, dot-directories,
and any file/folder the consultant has reserved as a scratch item by prefixing its name with `.`. A
dot-prefixed directory excludes its **whole subtree** and is pruned (see *Enumeration depth*). The components
of `documentation_dir` itself are not tested.

*Rationale:* while enumeration was flat this rule tested the leaf name only, and a dot-directory's children
were never reached anyway. With recursion, `.git/`, `.obsidian/`, `.vscode/` and similar trees would
otherwise become inputs; a dot prefix on a folder means the same thing as on a file — "not material".

## IX-02 — Conversion siblings

Any `*.converted.md` sibling. These are input-handler outputs (markitdown renderings and frozen visual
descriptions), referenced from their parent row's `converted_sibling` field — never independent rows.
Including them would generate spurious `added` drift on every run after the first successful conversion.

## IX-03 — Stadium application units

The raw, un-ingested form of a Stadium 6 application dropped in `documentation/`. Two shapes, both excluded in full:

- a **`*.stadium` pointer file** — a one-line text file whose content is the absolute path to a deployed
  Stadium app folder; and
- every path under a **sub-directory carrying the Stadium signature** — a directory that directly contains
  **`administration.db`**, **OR** `App_Data/Updates/*.sapz`, **OR** a `ClientApp/` folder.

Either shape may sit **at any depth** below `documentation_dir`. A signature directory is pruned (see
*Enumeration depth*): the walk never descends into it.

The full three-part signature (`administration.db` OR `App_Data/Updates/*.sapz` OR `ClientApp/`) is
authoritative here; both enumeration sites use it identically. Extraction of these units into requirement
assets is the standalone `/ingest-stadium` command's job; the raw app folder / pointer are never manifest
rows. The **extracted** `documentation/<AppName>.stadium-assets/*.md` assets are ordinary `Native-text` inputs and
**are** enumerated (subject to IX-04).

## IX-04 — Stadium extracted brand chrome

Every path under an `embedded/` sub-directory located directly inside a `*.stadium-assets/` directory —
i.e. `documentation/*.stadium-assets/embedded/**`. These are advisory brand images (icons + product logo) copied
verbatim by the `/ingest-stadium` extractor as design signals; they are UI *how*, not requirement *what*,
and are never manifest inputs. The exclusion is bounded to the `*.stadium-assets/embedded/` shape so a
consultant folder incidentally named `embedded/` elsewhere in `documentation/` is unaffected. The shape stays
**top-level**: `/ingest-stadium` always writes `*.stadium-assets/` directly under `documentation/`, wherever
the Stadium unit itself sits.

> Within a `*.stadium-assets/` directory, only the top-level `*.md` files are manifest inputs; any
> sub-directory (today: `embedded/`) is an advisory sidecar, never enumerated.

The `embedded/` assets remain on disk for downstream *non-manifest* consumers (e.g. the product logo surfaced
into a prototype via `framework/skills/extract-brand-theme.md`); excluding them from the manifest does not
delete or move them.

## Not an exclusion — media directories **are** enumerated

`<full-filename>.media/` holds the images `framework/skills/extract-ooxml-media.md` unpacked from an
OOXML input, beside that input at whatever depth it sits (`documentation/spec.docx` → `documentation/spec.docx.media/`;
`documentation/decks/review.docx` → `documentation/decks/review.docx.media/`) — i.e. `documentation/**/<full-filename>.media/`. These images **are** manifest inputs —
one `kind: "derived"` row each — so both enumeration sites descend into a media directory and pick them up
exactly as they would a consultant-dropped `.png`. That is the whole point of the extraction: an embedded
screenshot becomes a citable input instead of being dropped by the parent's text conversion.

This is stated here explicitly because it is the **inverse** of the `IX-04` note above ("any sub-directory […] is an
advisory sidecar, never enumerated"), and that note is scoped to `*.stadium-assets/` alone. A media directory is
not a sidecar; do not generalise `IX-04` to it. For the same reason, the word *sidecar* is not used for media
directories anywhere in the framework — see `framework/assets/glossary.md > Media directory`.

Two paths inside a media directory are nonetheless excluded, by rules that already exist:

- `.extracted-by-framework` — the reconciliation marker (`IS-04`). Dot-prefixed basename, so **`IX-01`** covers it.
- `img-<hash>.<ext>.converted.md` — the frozen visual description of an extracted image. **`IX-02`** covers it:
  the rule matches any `*.converted.md` by basename and is not depth-limited, so a nested description is excluded
  identically to a top-level one, and is referenced only from its parent row's `converted_sibling` field.

## IX-05 — Stadium `design-signals` asset (`/requirements` read-scope only)

The extracted `documentation/*.stadium-assets/*.stadium.design-signals.md` asset (theme / styling classification —
entirely Tier-B, purely `/design-system` material; it grounded **0** requirement claims in the DataShift
engagement) is **not read by the `/requirements` drafter**.

**Unlike `IX-01`..`IX-04`, this is a pipeline-scoped, *consumer-side* exclusion, not a universal
enumeration-side one.** The asset **stays a manifest row** — the input-handler still enumerates it (so the
shared `generated-docs/requirements/source-manifest.json` is identical across pipelines, and `/generate-prd`,
`/analyse-inputs`, `/review-inputs` still consume it). Only the `/requirements` drafter *skips reading* the
row, per the pipeline-scoped clause of the Read-path resolution rule in
`framework/skills/build-source-manifest.md`. The match is on the row's **basename**
(`*.stadium.design-signals.md`), since `filename` is a relative path. The file is never deleted or moved (`IS-02`).

The `glossary` asset was **considered for the same exclusion and deliberately kept** — it grounded 7 claims at
a higher density than the retained `surfaces`/`business-rules` assets, so excluding it would have contradicted
the north star for a negligible token saving.
