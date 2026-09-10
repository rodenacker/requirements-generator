#!/usr/bin/env python3
"""
extract_ooxml_media.py  --  Extract embedded images from one OOXML input as citable files.

Unpacks the images a consultant embedded in a `.docx` / `.pptx` / `.xlsx` dropped into
`documentation/`, so each one becomes a first-class, describable, citable input rather
than being silently dropped by the markitdown text conversion.

It does NOT interpret the images -- it only reports what is provably present in the
package, plus the surrounding document text that locates each image.

WHAT MAKES AN IMAGE SURVIVE
    Only images actually *referenced* from body content are extracted (relationship walk),
    which removes header/footer chrome and orphaned package parts far better than any
    size threshold. Referenced images are then filtered by minimum pixel dimensions,
    minimum bytes, and media type, and de-duplicated by content hash.

NAMING
    `img-<first 8 hex of the image's own sha256>.<ext>`. Content-hash naming is deliberate:
    an unchanged image re-extracts to a byte-identical filename, so the frozen description
    beside it still binds and the input-handler's idempotency guard reuses it. Sequential
    naming would shift every index when one image is removed from the source, silently
    rebinding descriptions to the wrong images.

DELETION
    This tool NEVER deletes. It reports an `orphans` list -- files present in the media
    directory that the current extraction did not produce -- and the caller decides.
    See `framework/shared/input-safety.md` (`IS-04`): removal is consultant-initiated
    via the input-handler's manifest-drift gate.

USAGE
    python extract_ooxml_media.py <ooxml_file> --media-dir <dir> [--json-out <path>]
                                  [--min-px N] [--min-bytes N] [--quiet]

EXIT CODES
    0  extraction completed (including "the document contains no images")
    1  the file is unreadable, not a ZIP, or not a supported OOXML format
"""

import argparse
import hashlib
import json
import os
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone

# --------------------------------------------------------------------------- constants

#: Filter floors. Tuned to drop inline icons, bullet glyphs and spacer rules while
#: keeping any image large enough to carry requirement content (a screenshot, a mockup,
#: a diagram). Referenced-only extraction does most of the work; these catch the rest.
MIN_PIXELS_PER_SIDE = 200
MIN_BYTES = 8192

#: Vector metafile formats. Windows-only, not renderable by the visual-description path,
#: and in practice always chrome (Visio paste, Office shape export).
DROPPED_EXTENSIONS = {".emf", ".wmf", ".emz", ".wmz"}

#: Written into every media directory this tool creates. Marker-gated deletion: the
#: framework may only reconcile a directory carrying this file, so a directory a
#: consultant hand-created at the same path is never touched. Dot-prefixed, so
#: `framework/shared/input-exclusions.md` (`IX-01`) already excludes it from enumeration.
MARKER_FILENAME = ".extracted-by-framework"

MEDIA_DIR_SUFFIX = ".media"

SUPPORTED_EXTENSIONS = {".docx", ".pptx", ".xlsx"}

# OOXML namespaces. Only the ones actually walked.
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "p": "http://schemas.presentationml.org/2006/main",
    "pml": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "v": "urn:schemas-microsoft-com:vml",
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
}

R_EMBED = "{%s}embed" % NS["r"]
R_LINK = "{%s}link" % NS["r"]
R_ID = "{%s}id" % NS["r"]


# --------------------------------------------------------------------------- helpers


def _log(msg, quiet=False):
    if not quiet:
        print(msg, file=sys.stderr)


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _localname(tag):
    """`{ns}foo` -> `foo`. ElementTree gives fully-qualified tags."""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _collapse(text):
    """Squash whitespace; OOXML text is split across runs and full of newlines."""
    return re.sub(r"\s+", " ", text or "").strip()


def _truncate(text, limit=400):
    text = _collapse(text)
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _resolve_part(base_part, target):
    """
    Resolve a relationship target against the part that declared it.

    Relationship targets are relative to the declaring part's directory, and routinely
    walk upward (`../media/image1.png` from `ppt/slides/slide1.xml`). Returns a
    forward-slash package path with no leading slash, matching `ZipFile.namelist()`.
    """
    if target.startswith("/"):
        return target.lstrip("/")
    base_dir = os.path.dirname(base_part)
    joined = os.path.normpath(os.path.join(base_dir, target))
    return joined.replace(os.sep, "/").lstrip("/")


def _read_rels(zf, part_name):
    """
    Read the relationship map for one part.

    `word/document.xml` -> `word/_rels/document.xml.rels`. Returns `{rId: package path}`,
    external (linked, not embedded) relationships excluded -- a linked image has no bytes
    in the package and cannot be extracted.
    """
    rels_name = "%s/_rels/%s.rels" % (
        os.path.dirname(part_name),
        os.path.basename(part_name),
    )
    rels_name = rels_name.lstrip("/")
    if rels_name not in zf.namelist():
        return {}
    out = {}
    try:
        root = ET.fromstring(zf.read(rels_name))
    except ET.ParseError:
        return {}
    for rel in root:
        if _localname(rel.tag) != "Relationship":
            continue
        if (rel.get("TargetMode") or "").lower() == "external":
            continue
        rid = rel.get("Id")
        target = rel.get("Target")
        if rid and target:
            out[rid] = _resolve_part(part_name, target)
    return out


def _blip_rids(element):
    """
    Every embedded-image relationship id reachable from this element, in document order.

    Covers both the modern DrawingML path (`<a:blip r:embed>`) and the legacy VML path
    (`<v:imagedata r:id>`) that Word still emits for pasted screenshots.
    """
    rids = []
    for node in element.iter():
        name = _localname(node.tag)
        if name == "blip":
            rid = node.get(R_EMBED) or node.get(R_LINK)
            if rid:
                rids.append(rid)
        elif name == "imagedata":
            rid = node.get(R_ID)
            if rid:
                rids.append(rid)
    return rids


# ------------------------------------------------------------------ image introspection


def _png_size(head):
    if len(head) >= 24 and head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
        return struct.unpack(">II", head[16:24])
    return None


def _gif_size(head):
    if len(head) >= 10 and head[:3] == b"GIF":
        return struct.unpack("<HH", head[6:10])
    return None


def _bmp_size(head):
    if len(head) >= 26 and head[:2] == b"BM":
        w, h = struct.unpack("<ii", head[18:26])
        return (abs(w), abs(h))
    return None


def _webp_size(data):
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    chunk = data[12:16]
    if chunk == b"VP8X":
        w = int.from_bytes(data[24:27], "little") + 1
        h = int.from_bytes(data[27:30], "little") + 1
        return (w, h)
    if chunk == b"VP8 " and len(data) >= 30:
        return struct.unpack("<HH", data[26:30])
    if chunk == b"VP8L" and len(data) >= 25:
        bits = int.from_bytes(data[21:25], "little")
        return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
    return None


def _jpeg_size(data):
    """Walk JPEG segment markers to the first SOF and read its frame dimensions."""
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return None
    i = 2
    end = len(data)
    while i < end - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        # Standalone markers carry no length payload.
        if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg_len = struct.unpack(">H", data[i + 2 : i + 4])[0]
        # SOF0..SOF15, excluding the DHT/JPG/DAC markers interleaved in that range.
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5 : i + 9])
            return (w, h)
        i += 2 + seg_len
    return None


def image_size(data):
    """
    Pixel dimensions of an image, or `None` when the format is not introspectable.

    Stdlib only -- no Pillow, matching the zero-dependency constraint the Stadium
    extractor works under. `None` means "unknown", and an unknown-size image is kept
    rather than filtered: a false drop loses requirement content, a false keep costs
    one description.
    """
    try:
        return (
            _png_size(data[:24])
            or _gif_size(data[:10])
            or _bmp_size(data[:26])
            or _webp_size(data[:30])
            or _jpeg_size(data)
        )
    except (struct.error, IndexError):
        return None


# --------------------------------------------------------------------------- docx walk


def _para_text(para):
    return _collapse("".join(node.text or "" for node in para.iter() if _localname(node.tag) == "t"))


def _para_style(para):
    for node in para.iter():
        if _localname(node.tag) == "pStyle":
            return node.get("{%s}val" % NS["w"]) or ""
    return ""


def _is_heading(style):
    return bool(re.match(r"^(Heading[1-9]|Title|Subtitle)$", style or "", re.IGNORECASE))


def _is_caption(style):
    return (style or "").lower() == "caption"


def walk_docx(zf):
    """
    Every referenced image in a `.docx`, in reading order, with its located context.

    Walks `word/document.xml` paragraph by paragraph so an image inherits the heading
    it sits under, an adjacent `Caption`-styled paragraph, and the nearest non-empty
    body text. Only `word/document.xml` is walked, which is what excludes headers,
    footers, footnotes and comments -- exactly the parts that carry page chrome.
    """
    part = "word/document.xml"
    if part not in zf.namelist():
        return []
    rels = _read_rels(zf, part)
    try:
        root = ET.fromstring(zf.read(part))
    except ET.ParseError:
        return []

    body = next((el for el in root if _localname(el.tag) == "body"), root)
    paras = [el for el in body.iter() if _localname(el.tag) == "p"]

    texts = [_para_text(p) for p in paras]
    styles = [_para_style(p) for p in paras]

    hits = []
    heading = None
    for idx, para in enumerate(paras):
        if _is_heading(styles[idx]) and texts[idx]:
            heading = texts[idx]
        for rid in _blip_rids(para):
            target = rels.get(rid)
            if not target:
                continue
            caption = None
            for probe in (idx + 1, idx - 1):
                if 0 <= probe < len(paras) and _is_caption(styles[probe]) and texts[probe]:
                    caption = texts[probe]
                    break
            nearby = texts[idx] or next(
                (
                    texts[j]
                    for j in range(idx - 1, max(-1, idx - 4), -1)
                    if texts[j] and not _is_heading(styles[j])
                ),
                None,
            )
            hits.append(
                {
                    "part": target,
                    "location": "paragraph %d" % (idx + 1),
                    "section": heading,
                    "caption": caption,
                    "nearby_text": _truncate(nearby) if nearby else None,
                }
            )
    return hits


# --------------------------------------------------------------------------- pptx walk


def _slide_sort_key(name):
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def _slide_title(root):
    """
    The slide's title placeholder text, when it has one.

    A shape is the title when its non-visual placeholder carries `type="title"` or
    `"ctrTitle"`; PowerPoint omits the attribute for the default title placeholder,
    so a missing type on a placeholder with index 0 also counts.
    """
    for shape in root.iter():
        if _localname(shape.tag) != "sp":
            continue
        ph = next((n for n in shape.iter() if _localname(n.tag) == "ph"), None)
        if ph is None:
            continue
        ph_type = (ph.get("type") or "").lower()
        if ph_type in ("title", "ctrtitle") or (not ph_type and ph.get("idx") in (None, "0")):
            text = _collapse(
                " ".join(n.text or "" for n in shape.iter() if _localname(n.tag) == "t")
            )
            if text:
                return text
    return None


def walk_pptx(zf):
    """
    Every referenced image across the slides of a `.pptx`, in slide order.

    Context is the slide number plus its title and body text -- for a deck, that is
    the caption. Layouts and masters are deliberately not walked: their images are
    template chrome present on every slide, never requirement content.
    """
    slides = sorted(
        (n for n in zf.namelist() if re.match(r"^ppt/slides/slide\d+\.xml$", n)),
        key=_slide_sort_key,
    )
    hits = []
    for part in slides:
        rels = _read_rels(zf, part)
        try:
            root = ET.fromstring(zf.read(part))
        except ET.ParseError:
            continue
        number = _slide_sort_key(part)
        title = _slide_title(root)
        body = _collapse(" ".join(n.text or "" for n in root.iter() if _localname(n.tag) == "t"))
        for rid in _blip_rids(root):
            target = rels.get(rid)
            if not target:
                continue
            hits.append(
                {
                    "part": target,
                    "location": "slide %d" % number,
                    "section": title,
                    "caption": None,
                    "nearby_text": _truncate(body) if body else None,
                }
            )
    return hits


# --------------------------------------------------------------------------- xlsx walk


def _sheet_names_by_part(zf):
    """
    `{worksheet part path: sheet name}`.

    The visible sheet name lives in `xl/workbook.xml`, but the part path it maps to
    lives in the workbook's relationships, joined on `r:id`.
    """
    if "xl/workbook.xml" not in zf.namelist():
        return {}
    rels = _read_rels(zf, "xl/workbook.xml")
    try:
        root = ET.fromstring(zf.read("xl/workbook.xml"))
    except ET.ParseError:
        return {}
    out = {}
    for sheet in root.iter():
        if _localname(sheet.tag) != "sheet":
            continue
        target = rels.get(sheet.get(R_ID) or "")
        if target:
            out[target] = sheet.get("name") or target
    return out


def walk_xlsx(zf):
    """
    Every referenced image in a `.xlsx`, by sheet.

    Spreadsheet images are indirect: a worksheet relates to a drawing part, and the
    drawing relates to the media. Context is the sheet name -- the only locating text
    a spreadsheet reliably offers.
    """
    sheet_names = _sheet_names_by_part(zf)
    names = zf.namelist()
    hits = []
    for part in sorted(n for n in names if re.match(r"^xl/worksheets/sheet\d+\.xml$", n)):
        sheet_name = sheet_names.get(part, os.path.basename(part))
        for drawing in _read_rels(zf, part).values():
            if not re.match(r"^xl/drawings/drawing\d+\.xml$", drawing) or drawing not in names:
                continue
            drawing_rels = _read_rels(zf, drawing)
            try:
                root = ET.fromstring(zf.read(drawing))
            except ET.ParseError:
                continue
            for rid in _blip_rids(root):
                target = drawing_rels.get(rid)
                if not target:
                    continue
                hits.append(
                    {
                        "part": target,
                        "location": "sheet '%s'" % sheet_name,
                        "section": sheet_name,
                        "caption": None,
                        "nearby_text": None,
                    }
                )
    return hits


WALKERS = {".docx": walk_docx, ".pptx": walk_pptx, ".xlsx": walk_xlsx}


# --------------------------------------------------------------------------- extraction


def build_context(hit, parent_filename):
    """
    The one-line human sentence handed to the visual-description skill as
    `document_context`. It locates the image; it never describes it.
    """
    parts = ["Embedded in %s at %s" % (parent_filename, hit["location"])]
    if hit.get("section"):
        parts.append('under the heading "%s"' % hit["section"])
    if hit.get("caption"):
        parts.append('captioned "%s"' % hit["caption"])
    elif hit.get("nearby_text"):
        parts.append('surrounding text: "%s"' % hit["nearby_text"])
    return ". ".join([parts[0] + (", " + ", ".join(parts[1:]) if len(parts) > 1 else "")]) + "."


def extract(ooxml_path, media_dir, min_px=MIN_PIXELS_PER_SIDE, min_bytes=MIN_BYTES, quiet=False):
    """
    Extract, filter and write the embedded images of one OOXML file.

    Returns the report dict that `--json-out` serialises. Never deletes anything;
    pre-existing files the current extraction did not produce are reported under
    `orphans` for the caller to reconcile.
    """
    ext = os.path.splitext(ooxml_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "unsupported extension %r (expected one of %s)"
            % (ext, ", ".join(sorted(SUPPORTED_EXTENSIONS)))
        )
    if not os.path.isfile(ooxml_path):
        raise ValueError("not a file: %s" % ooxml_path)
    if not zipfile.is_zipfile(ooxml_path):
        raise ValueError("not a readable OOXML package (not a ZIP): %s" % ooxml_path)

    parent_filename = os.path.basename(ooxml_path)
    report = {
        "schema_version": 1,
        "generated_at": _now(),
        "parent_filename": parent_filename,
        "parent_path": ooxml_path.replace(os.sep, "/"),
        "parent_sha256": None,
        "media_dir": media_dir.replace(os.sep, "/"),
        "images": [],
        "filtered": [],
        "orphans": [],
        "counts": {},
    }

    with open(ooxml_path, "rb") as fh:
        report["parent_sha256"] = hashlib.sha256(fh.read()).hexdigest()

    with zipfile.ZipFile(ooxml_path) as zf:
        hits = WALKERS[ext](zf)
        names = set(zf.namelist())

        kept = {}  # filename -> record
        seen_digests = {}  # full digest -> filename
        filtered = []

        for order, hit in enumerate(hits, start=1):
            part = hit["part"]
            if part not in names:
                filtered.append({"part": part, "reason": "missing-from-package"})
                continue

            part_ext = os.path.splitext(part)[1].lower()
            if part_ext in DROPPED_EXTENSIONS:
                filtered.append({"part": part, "reason": "vector-metafile"})
                continue

            data = zf.read(part)
            digest = hashlib.sha256(data).hexdigest()

            if digest in seen_digests:
                # Same bytes already kept -- the repeated logo case. Record the extra
                # placement on the existing image rather than writing a second copy.
                kept[seen_digests[digest]]["placements"].append(
                    build_context(hit, parent_filename)
                )
                filtered.append({"part": part, "reason": "duplicate-of-%s" % seen_digests[digest]})
                continue

            if len(data) < min_bytes:
                filtered.append(
                    {"part": part, "reason": "below-min-bytes", "bytes": len(data)}
                )
                continue

            size = image_size(data)
            if size and (size[0] < min_px or size[1] < min_px):
                filtered.append(
                    {"part": part, "reason": "below-min-dimensions", "dimensions": list(size)}
                )
                continue

            filename = "img-%s%s" % (digest[:8], part_ext or ".bin")
            seen_digests[digest] = filename
            kept[filename] = {
                "filename": filename,
                "reading_order": order,
                "source_part": part,
                "sha256": digest,
                "bytes": len(data),
                "dimensions": list(size) if size else None,
                "document_context": build_context(hit, parent_filename),
                "placements": [],
                "_data": data,
            }

    os.makedirs(media_dir, exist_ok=True)
    marker_path = os.path.join(media_dir, MARKER_FILENAME)
    with open(marker_path, "w", encoding="utf-8") as fh:
        fh.write(
            "Generated by framework/tools/extract_ooxml_media.py from %s.\n"
            "Derived output, not consultant input. Reconciliation is gated on this "
            "marker -- see framework/shared/input-safety.md (IS-04).\n" % parent_filename
        )

    for record in kept.values():
        data = record.pop("_data")
        path = os.path.join(media_dir, record["filename"])
        # Content-hash naming means an identical file is already the right bytes;
        # skipping the write keeps mtime stable so nothing downstream sees churn.
        if not (os.path.isfile(path) and os.path.getsize(path) == len(data)):
            with open(path, "wb") as fh:
                fh.write(data)
        report["images"].append(record)

    produced = set(kept) | {MARKER_FILENAME}
    for existing in sorted(os.listdir(media_dir)):
        if existing in produced or existing.endswith(".converted.md"):
            continue
        if os.path.isfile(os.path.join(media_dir, existing)):
            report["orphans"].append(existing)

    report["filtered"] = filtered
    report["counts"] = {
        "referenced": len(hits),
        "extracted": len(report["images"]),
        "filtered": len(filtered),
        "orphans": len(report["orphans"]),
    }

    _log(
        "%s: %d extracted / %d filtered / %d orphaned (from %d referenced)"
        % (
            parent_filename,
            report["counts"]["extracted"],
            report["counts"]["filtered"],
            report["counts"]["orphans"],
            report["counts"]["referenced"],
        ),
        quiet,
    )
    return report


def default_media_dir(ooxml_path):
    """
    `documentation/spec.docx` -> `documentation/spec.docx.media`.

    Append form, not extension-replace, so `spec.docx` and `spec.pptx` cannot collide --
    the same reason `framework/skills/describe-visual-input.md` appends.
    """
    return ooxml_path + MEDIA_DIR_SUFFIX


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Extract embedded images from one OOXML input as citable files."
    )
    ap.add_argument("ooxml_file", help="Path to the .docx / .pptx / .xlsx input")
    ap.add_argument(
        "--media-dir",
        default=None,
        help="Directory to write images into (default: <ooxml_file>.media)",
    )
    ap.add_argument("--json-out", default=None, help="Write the extraction report JSON here")
    ap.add_argument(
        "--min-px",
        type=int,
        default=MIN_PIXELS_PER_SIDE,
        help="Minimum pixels per side (default: %d)" % MIN_PIXELS_PER_SIDE,
    )
    ap.add_argument(
        "--min-bytes",
        type=int,
        default=MIN_BYTES,
        help="Minimum image size in bytes (default: %d)" % MIN_BYTES,
    )
    ap.add_argument("--quiet", action="store_true", help="Suppress the summary line on stderr")
    args = ap.parse_args(argv)

    media_dir = args.media_dir or default_media_dir(args.ooxml_file)
    try:
        report = extract(
            args.ooxml_file,
            media_dir,
            min_px=args.min_px,
            min_bytes=args.min_bytes,
            quiet=args.quiet,
        )
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print("extract_ooxml_media: %s" % exc, file=sys.stderr)
        return 1

    if args.json_out:
        os.makedirs(os.path.dirname(os.path.abspath(args.json_out)), exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    else:
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
