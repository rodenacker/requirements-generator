# Input Exclusions

Single source of truth for **what is *not* a source-manifest input** when an agent enumerates the
consultant-dropped input folder (`input_dir`, canonically `input/`). Every path that matches an exclusion
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
this file is authoritative — a caller that diverges from an `IX-NN` definition is the bug.

## IX-01 — Dotfiles and consultant scratch files

Any path whose **basename** begins with `.` — dotfiles, and any file/folder the consultant has reserved as a
scratch item by prefixing its name with `.`. Basename only: the leaf name is tested, not intermediate path
components. *(Note: a dot-prefixed **directory** is excluded as a path, but this rule alone does not exclude
its non-dot-prefixed children — do not rely on a dot-directory to hide contents; use an explicit `IX-NN`.)*

## IX-02 — Conversion siblings

Any `*.converted.md` sibling. These are input-handler outputs (markitdown renderings and frozen visual
descriptions), referenced from their parent row's `converted_sibling` field — never independent rows.
Including them would generate spurious `added` drift on every run after the first successful conversion.

## IX-03 — Stadium application units

The raw, un-ingested form of a Stadium 6 application dropped in `input/`. Two shapes, both excluded in full:

- a **`*.stadium` pointer file** — a one-line text file whose content is the absolute path to a deployed
  Stadium app folder; and
- every path under a **sub-directory carrying the Stadium signature** — a directory that directly contains
  **`administration.db`**, **OR** `App_Data/Updates/*.sapz`, **OR** a `ClientApp/` folder.

The full three-part signature (`administration.db` OR `App_Data/Updates/*.sapz` OR `ClientApp/`) is
authoritative here; both enumeration sites use it identically. Extraction of these units into requirement
assets is the standalone `/ingest-stadium` command's job; the raw app folder / pointer are never manifest
rows. The **extracted** `input/<AppName>.stadium-assets/*.md` assets are ordinary `Native-text` inputs and
**are** enumerated (subject to IX-04).

## IX-04 — Stadium extracted brand chrome

Every path under an `embedded/` sub-directory located directly inside a `*.stadium-assets/` directory —
i.e. `input/*.stadium-assets/embedded/**`. These are advisory brand images (icons + product logo) copied
verbatim by the `/ingest-stadium` extractor as design signals; they are UI *how*, not requirement *what*,
and are never manifest inputs. The exclusion is bounded to the `*.stadium-assets/embedded/` shape so a
consultant folder incidentally named `embedded/` elsewhere in `input/` is unaffected.

> Within a `*.stadium-assets/` directory, only the top-level `*.md` files are manifest inputs; any
> sub-directory (today: `embedded/`) is an advisory sidecar, never enumerated.

The `embedded/` assets remain on disk for downstream *non-manifest* consumers (e.g. the product logo surfaced
into a prototype via `framework/skills/extract-brand-theme.md`); excluding them from the manifest does not
delete or move them.

## IX-05 — Stadium `design-signals` asset (`/requirements` read-scope only)

The extracted `input/*.stadium-assets/*.stadium.design-signals.md` asset (theme / styling classification —
entirely Tier-B, purely `/design-system` material; it grounded **0** requirement claims in the DataShift
engagement) is **not read by the `/requirements` drafter**.

**Unlike `IX-01`..`IX-04`, this is a pipeline-scoped, *consumer-side* exclusion, not a universal
enumeration-side one.** The asset **stays a manifest row** — the input-handler still enumerates it (so the
shared `requirements/source-manifest.json` is identical across pipelines, and `/generate-prd`,
`/analyse-inputs`, `/review-inputs` still consume it). Only the `/requirements` drafter *skips reading* the
row, per the pipeline-scoped clause of the Read-path resolution rule in
`framework/skills/build-source-manifest.md`. The file is never deleted or moved (`IS-02`).

The `glossary` asset was **considered for the same exclusion and deliberately kept** — it grounded 7 claims at
a higher density than the retained `surfaces`/`business-rules` assets, so excluding it would have contradicted
the north star for a negligible token saving.
