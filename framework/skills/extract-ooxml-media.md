# extract-ooxml-media.md

**Purpose:** Extract the images embedded in one OOXML input (`.docx`, `.pptx`, `.xlsx`) under `documentation/` into a **media directory** of separate image files, each of which the input-handler then registers as its own `kind: "derived"` manifest row and describes once via `framework/skills/describe-visual-input.md`. Without this step an embedded screenshot, mockup or diagram is **silently lost**: markitdown renders the document's text and drops its media, so a client deck's most requirement-dense content never reaches a drafter.

This is the OOXML analogue of `extract-stadium-app.md`: a deterministic Python converter whose output is consumed as ordinary inputs. It is **not** a describer — it interprets nothing. It unpacks bytes and captures the surrounding document text that *locates* each image.

**Never deletes.** The tool reports an `orphans` list — files in the media directory the current extraction did not produce — and returns. Removal is the input-handler's business, consultant-initiated at the manifest-drift gate, per `framework/shared/input-safety.md` (`IS-04`).

## Inputs

- `ooxml_path` — repo-relative path to the `.docx` / `.pptx` / `.xlsx` input under `documentation/`. Required.
- `media_dir` — directory to write images into, conventionally `documentation/<full-filename>.media/` (append form, never extension-replace — see *Naming* below). Required.
- `json_out` — path for the extraction report, conventionally `framework/state/ooxml-media/<full-filename>.json` (outside `documentation/`, never manifested). Required.
- Python on `PATH` — the only runtime dependency, and the same one `extract-stadium-app.md` preflights. The tool is stdlib-only.

## Outputs

A structured row returned to the caller:

- `{ status: "ok", extracted: <int>, filtered: <int>, orphans: [<basenames>], report_path: <str> }` — the tool exited zero. `extracted: 0` is a **success**, not a failure: most documents contain no requirement-bearing images.
- `{ status: "failed", reason: "ooxml-media-extract" }` — the tool exited non-zero (unreadable, not a ZIP, or an unsupported extension). The caller records the failure on the parent row's `conversions_applied` and proceeds with the parent's text conversion regardless — a media-extraction failure must never block ingestion of the document itself.

On disk, inside `media_dir`:

- `img-<8 hex>.<ext>` — one file per surviving image. The 8 hex are the first 8 characters of that image's own sha256.
- `.extracted-by-framework` — the reconciliation marker. Dot-prefixed, so `IX-01` already excludes it from enumeration.
- (Later, written by the input-handler, not this skill: `img-<8 hex>.<ext>.converted.md` frozen descriptions, excluded from enumeration by `IX-02`.)

## Procedure

1. **Run the extractor.** Via Bash:
   ```
   python framework/tools/extract_ooxml_media.py "<ooxml_path>" --media-dir "<media_dir>" --json-out "<json_out>"
   ```
   Non-zero exit → return `{ status: "failed", reason: "ooxml-media-extract" }`. The summary line on stderr carries the `N extracted / M filtered / K orphaned (from R referenced)` counts the caller surfaces to the consultant.

2. **Read the report.** `json_out` is JSON with `counts`, `images[]`, `filtered[]` and `orphans[]`. Each `images[]` entry carries `filename`, `reading_order`, `source_part`, `sha256`, `bytes`, `dimensions`, `document_context`, and `placements[]` (additional locations of a de-duplicated image).

3. **Return the row.** The caller registers each `images[]` entry as a manifest row and passes its `document_context` through to `describe-visual-input.md`. This skill writes no manifest row itself.

## Naming

The media directory **appends** to the full filename, extension included: `documentation/spec.docx` → `documentation/spec.docx.media/`. Extension-replace would collide `spec.docx` and `spec.pptx` onto one directory — the same collision `describe-visual-input.md` avoids by appending.

Image filenames are the **content hash**, not a sequential index. This is load-bearing, not cosmetic: an unchanged image re-extracts to a byte-identical filename, so its frozen description still binds and the input-handler's Step-5 idempotency guard reuses the consultant's hand-edits. Sequential naming would shift every index when one image is removed from the source document, silently rebinding descriptions to the wrong images — a worse failure than losing them.

## What survives extraction

Filters apply in this order. Every rejection is recorded in `filtered[]` with a reason, so nothing is dropped silently:

1. **Referenced-only.** Only images reachable from body content via the relationship walk (`word/document.xml`, `ppt/slides/slideN.xml`, `xl/drawings/drawingN.xml`) are candidates. This is what excludes headers, footers, footnotes, comments, and PowerPoint layouts/masters — the parts that carry page chrome — and it does that job far better than any size threshold. External (linked) relationships are skipped: a linked image has no bytes in the package.
2. **Media type.** `.emf` / `.wmf` / `.emz` / `.wmz` dropped — Windows metafiles, not renderable by the visual-description path, in practice always chrome.
3. **Content-hash dedupe.** Identical bytes are written once; the repeat's location is appended to the kept image's `placements[]` rather than lost.
4. **Minimum bytes** (`MIN_BYTES`, 8192) and **minimum pixels per side** (`MIN_PIXELS_PER_SIDE`, 200), both named constants at the top of the tool and overridable via `--min-bytes` / `--min-px`.

**Unknown dimensions are kept, not dropped.** A format the stdlib header parsers do not recognise records `dimensions: null` and survives. A false drop loses requirement content permanently; a false keep costs one description.

## Document context

Each image carries a `document_context` sentence locating it — parent filename, position (`paragraph 12`, `slide 4`, `sheet 'Case Volumes'`), the heading or slide title it sits under, and its caption or nearest body text. The caller passes this to `describe-visual-input.md` as `document_context`.

This is what makes the vision call worth making. A screenshot described blind yields "a table with columns"; the same screenshot described with its context yields "the Case Queue screen referenced under §4.2 Reassignment" — the difference between noise and a requirement source. The context **locates** the image; it is not itself a requirement source, and `describe-visual-input.md` must not mine claims from it.

## Self-validation

- The tool was invoked via `framework/tools/extract_ooxml_media.py` (never re-implemented inline) and exited zero.
- Every `images[]` entry's `filename` exists in `media_dir` with non-zero size.
- `.extracted-by-framework` exists in `media_dir`.
- No file in `media_dir` was deleted or truncated by this skill.
- `json_out` parses as JSON and its `counts.extracted` equals `len(images)`.

## Anti-Patterns

- Do not call this skill on a `.pdf`. PDF media extraction is deliberately out of scope: PDFs are not ZIP containers and would need a third-party library, breaking the stdlib-only constraint. The tool exits 1 on any extension outside `.docx` / `.pptx` / `.xlsx`.
- Do not delete anything in a media directory from this skill. Reconciliation is gated on the `.extracted-by-framework` marker **and** on the consultant's Refresh choice at the drift gate (`IS-04`). An automatic delete here would be a defect under `IS-03`.
- Do not treat `extracted: 0` as a failure or surface it as a warning. Most documents contain no requirement-bearing images.
- Do not let a media-extraction failure block the parent's text conversion. The document's prose is the primary content; losing its images is a degradation, not a halt.
- Do not write the media directory anywhere but beside its parent under `documentation/`. Downstream enumeration, freshness diffing, and the read-path rule all assume co-location.
- Do not re-interpret an extracted image's pixels downstream. Once described, the frozen `*.converted.md` sibling is the only consumer-facing surface — the interpret-once contract applies to extracted media exactly as it does to a consultant-dropped `.png` (`framework/skills/build-source-manifest.md > Read-path resolution`).
- Do not mine requirements from `document_context`. It locates the image; the parent document's own `.converted.md` is where its prose is cited from.
