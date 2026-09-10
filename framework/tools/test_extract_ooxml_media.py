#!/usr/bin/env python3
r"""test_extract_ooxml_media.py -- Regression harness for the OOXML embedded-media extractor.

Corpus-independent by construction: every test synthesises its own OOXML package in a
temp dir, so the suite never depends on a real client document being present. The
packages are minimal but structurally faithful -- real relationship parts, real
`r:embed` references, real PNG/JPEG headers.

What is locked here, and why each matters:

  * Content-hash naming (`img-<8 hex>.png`). The whole safety argument for deleting
    orphans rests on an unchanged image re-extracting to a byte-identical filename.
  * Referenced-only extraction. An image sitting in `word/media/` but referenced from
    nowhere in the body is page chrome and must not become an input.
  * The filter floors, and the deliberate keep-on-unknown-dimensions rule.
  * Deduplication by content hash, including that the duplicate's placement is still
    recorded rather than lost.
  * Never deletes. Orphans are reported, and pre-existing files survive extraction.
  * The `document_context` sentence, which is the only thing locating an image for the
    downstream description.

Run: python -m pytest framework/tools/test_extract_ooxml_media.py
 or: python framework/tools/test_extract_ooxml_media.py
"""

import os
import struct
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import extract_ooxml_media as mod  # noqa: E402


# --------------------------------------------------------------------------- builders


def png_bytes(width, height, pad=20000, filler=b"\x00"):
    """A PNG with a valid signature and IHDR, padded to a chosen size.

    The pixel data is deliberately junk -- the extractor only ever reads the header,
    and a real encoder would be a dependency.
    """
    head = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", width, height)
    ihdr += b"\x08\x06\x00\x00\x00" + b"\x00\x00\x00\x00"
    return head + ihdr + b"IDAT" + filler * pad


def jpeg_bytes(width, height, pad=20000):
    """A JPEG with an APP0 segment followed by a SOF0 carrying real dimensions."""
    out = b"\xff\xd8"
    out += b"\xff\xe0" + struct.pack(">H", 16) + b"JFIF\x00" + b"\x00" * 9
    sof = b"\x08" + struct.pack(">HH", height, width) + b"\x03"
    out += b"\xff\xc0" + struct.pack(">H", len(sof) + 2) + sof
    out += b"\xff\xda" + struct.pack(">H", 2) + b"\x00" * pad + b"\xff\xd9"
    return out


RELS_OPEN = (
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
)
IMAGE_REL_TYPE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
)


def rels(entries):
    """`entries` is a list of `(rId, target)` or `(rId, target, "External")`."""
    body = []
    for entry in entries:
        mode = ' TargetMode="External"' if len(entry) > 2 else ""
        body.append(
            '<Relationship Id="%s" Type="%s" Target="%s"%s/>'
            % (entry[0], IMAGE_REL_TYPE, entry[1], mode)
        )
    return (RELS_OPEN + "".join(body) + "</Relationships>").encode("utf-8")


W_NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
A_NS = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
R_NS = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'


def w_para(text="", style=None, blip_rid=None):
    out = "<w:p>"
    if style:
        out += '<w:pPr><w:pStyle w:val="%s"/></w:pPr>' % style
    if text:
        out += "<w:r><w:t>%s</w:t></w:r>" % text
    if blip_rid:
        out += '<w:r><w:drawing><a:blip r:embed="%s"/></w:drawing></w:r>' % blip_rid
    return out + "</w:p>"


def docx_document(paragraphs):
    return (
        '<?xml version="1.0"?><w:document %s %s %s><w:body>%s</w:body></w:document>'
        % (W_NS, A_NS, R_NS, "".join(paragraphs))
    ).encode("utf-8")


def write_zip(path, entries):
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in entries.items():
            zf.writestr(name, data)
    return path


def build_docx(path, paragraphs, rel_entries, media):
    entries = {
        "word/document.xml": docx_document(paragraphs),
        "word/_rels/document.xml.rels": rels(rel_entries),
    }
    entries.update(media)
    return write_zip(path, entries)


# --------------------------------------------------------------------------- base case


class TestDocxExtraction(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.addCleanup(self.tmp.cleanup)
        self.screenshot = png_bytes(1200, 800)
        self.icon = png_bytes(24, 24, pad=200)
        self.docx = build_docx(
            os.path.join(self.dir, "spec.docx"),
            [
                w_para("Case Reassignment", style="Heading1"),
                w_para("A supervisor reassigns an open case."),
                w_para(blip_rid="rId1"),
                w_para("Figure 1 - the Case Queue screen", style="Caption"),
                w_para("Bulleted point", blip_rid="rId2"),
            ],
            [("rId1", "media/image1.png"), ("rId2", "media/image2.png")],
            {"word/media/image1.png": self.screenshot, "word/media/image2.png": self.icon},
        )
        self.media_dir = os.path.join(self.dir, "spec.docx.media")

    def run_extract(self, **kwargs):
        return mod.extract(self.docx, self.media_dir, quiet=True, **kwargs)

    def test_keeps_the_screenshot_and_filters_the_icon(self):
        report = self.run_extract()
        self.assertEqual(report["counts"]["referenced"], 2)
        self.assertEqual(report["counts"]["extracted"], 1)
        reasons = [f["reason"] for f in report["filtered"]]
        self.assertEqual(reasons, ["below-min-bytes"])

    def test_filename_is_the_content_hash(self):
        import hashlib

        report = self.run_extract()
        expected = "img-%s.png" % hashlib.sha256(self.screenshot).hexdigest()[:8]
        self.assertEqual(report["images"][0]["filename"], expected)
        self.assertTrue(os.path.isfile(os.path.join(self.media_dir, expected)))

    def test_reextraction_is_byte_identical(self):
        """The property the whole orphan-deletion argument rests on."""
        first = self.run_extract()["images"][0]["filename"]
        second = self.run_extract()["images"][0]["filename"]
        self.assertEqual(first, second)
        self.assertEqual(os.listdir(self.media_dir).count(first), 1)

    def test_dimensions_and_bytes_are_reported(self):
        image = self.run_extract()["images"][0]
        self.assertEqual(image["dimensions"], [1200, 800])
        self.assertEqual(image["bytes"], len(self.screenshot))

    def test_context_locates_the_image(self):
        context = self.run_extract()["images"][0]["document_context"]
        self.assertIn("spec.docx", context)
        self.assertIn("paragraph 3", context)
        self.assertIn("Case Reassignment", context)
        self.assertIn("Figure 1 - the Case Queue screen", context)

    def test_marker_is_written(self):
        self.run_extract()
        self.assertTrue(os.path.isfile(os.path.join(self.media_dir, mod.MARKER_FILENAME)))

    def test_parent_sha256_is_recorded(self):
        import hashlib

        with open(self.docx, "rb") as fh:
            expected = hashlib.sha256(fh.read()).hexdigest()
        self.assertEqual(self.run_extract()["parent_sha256"], expected)

    def test_min_px_floor_is_honoured(self):
        """A large-in-bytes but small-in-pixels image is still dropped."""
        wide = png_bytes(150, 150, pad=30000)
        build_docx(
            self.docx,
            [w_para(blip_rid="rId1")],
            [("rId1", "media/image1.png")],
            {"word/media/image1.png": wide},
        )
        report = self.run_extract()
        self.assertEqual(report["counts"]["extracted"], 0)
        self.assertEqual(report["filtered"][0]["reason"], "below-min-dimensions")
        self.assertEqual(report["filtered"][0]["dimensions"], [150, 150])


class TestFilteringRules(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.addCleanup(self.tmp.cleanup)

    def extract_docx(self, paragraphs, rel_entries, media, **kwargs):
        path = build_docx(
            os.path.join(self.dir, "in.docx"), paragraphs, rel_entries, media
        )
        return mod.extract(path, os.path.join(self.dir, "out"), quiet=True, **kwargs)

    def test_unreferenced_media_is_never_extracted(self):
        """The referenced-only rule -- header/footer chrome lives in the package unreferenced."""
        report = self.extract_docx(
            [w_para("No images here")],
            [],
            {
                "word/media/image1.png": png_bytes(1000, 1000),
                "word/media/header-logo.png": png_bytes(1000, 1000),
            },
        )
        self.assertEqual(report["counts"]["referenced"], 0)
        self.assertEqual(report["counts"]["extracted"], 0)

    def test_vector_metafiles_are_dropped(self):
        report = self.extract_docx(
            [w_para(blip_rid="rId1")],
            [("rId1", "media/image1.emf")],
            {"word/media/image1.emf": b"\x01" * 60000},
        )
        self.assertEqual(report["counts"]["extracted"], 0)
        self.assertEqual(report["filtered"][0]["reason"], "vector-metafile")

    def test_duplicates_collapse_but_keep_their_placement(self):
        logo = png_bytes(900, 900)
        report = self.extract_docx(
            [
                w_para("Intro", style="Heading1"),
                w_para(blip_rid="rId1"),
                w_para("Appendix", style="Heading1"),
                w_para(blip_rid="rId2"),
            ],
            [("rId1", "media/a.png"), ("rId2", "media/b.png")],
            {"word/media/a.png": logo, "word/media/b.png": logo},
        )
        self.assertEqual(report["counts"]["extracted"], 1)
        self.assertTrue(report["filtered"][0]["reason"].startswith("duplicate-of-img-"))
        placements = report["images"][0]["placements"]
        self.assertEqual(len(placements), 1)
        self.assertIn("Appendix", placements[0])

    def test_external_links_are_skipped(self):
        """A linked image has no bytes in the package, so it cannot be extracted."""
        report = self.extract_docx(
            [w_para(blip_rid="rId1")],
            [("rId1", "http://example.invalid/x.png", "External")],
            {},
        )
        self.assertEqual(report["counts"]["extracted"], 0)
        self.assertEqual(report["counts"]["filtered"], 0)

    def test_missing_part_is_reported_not_crashed(self):
        report = self.extract_docx(
            [w_para(blip_rid="rId1")], [("rId1", "media/gone.png")], {}
        )
        self.assertEqual(report["filtered"][0]["reason"], "missing-from-package")

    def test_unknown_format_is_kept_not_dropped(self):
        """Keep-on-unknown: a false drop loses content, a false keep costs one description."""
        report = self.extract_docx(
            [w_para(blip_rid="rId1")],
            [("rId1", "media/image1.tiff")],
            {"word/media/image1.tiff": b"II*\x00" + b"\x7f" * 40000},
        )
        self.assertEqual(report["counts"]["extracted"], 1)
        self.assertIsNone(report["images"][0]["dimensions"])

    def test_legacy_vml_images_are_found(self):
        """Word still emits VML `<v:imagedata>` for some pasted screenshots."""
        vml = (
            '<?xml version="1.0"?><w:document %s %s %s '
            'xmlns:v="urn:schemas-microsoft-com:vml"><w:body>'
            '<w:p><w:r><w:pict><v:shape><v:imagedata r:id="rId1"/></v:shape>'
            "</w:pict></w:r></w:p></w:body></w:document>" % (W_NS, A_NS, R_NS)
        ).encode("utf-8")
        path = write_zip(
            os.path.join(self.dir, "vml.docx"),
            {
                "word/document.xml": vml,
                "word/_rels/document.xml.rels": rels([("rId1", "media/image1.png")]),
                "word/media/image1.png": png_bytes(600, 400),
            },
        )
        report = mod.extract(path, os.path.join(self.dir, "vml-out"), quiet=True)
        self.assertEqual(report["counts"]["extracted"], 1)


class TestNeverDeletes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.addCleanup(self.tmp.cleanup)
        self.media_dir = os.path.join(self.dir, "d.docx.media")
        os.makedirs(self.media_dir)
        self.stale = os.path.join(self.media_dir, "img-deadbeef.png")
        with open(self.stale, "wb") as fh:
            fh.write(b"stale")
        with open(os.path.join(self.media_dir, "img-deadbeef.png.converted.md"), "w") as fh:
            fh.write("# frozen description")
        self.docx = build_docx(
            os.path.join(self.dir, "d.docx"),
            [w_para(blip_rid="rId1")],
            [("rId1", "media/image1.png")],
            {"word/media/image1.png": png_bytes(800, 600)},
        )

    def test_orphans_are_reported_and_left_on_disk(self):
        report = mod.extract(self.docx, self.media_dir, quiet=True)
        self.assertEqual(report["orphans"], ["img-deadbeef.png"])
        self.assertTrue(os.path.isfile(self.stale))

    def test_descriptions_are_never_counted_as_orphans(self):
        """`*.converted.md` siblings are the input-handler's business, not the extractor's."""
        report = mod.extract(self.docx, self.media_dir, quiet=True)
        self.assertNotIn("img-deadbeef.png.converted.md", report["orphans"])

    def test_surviving_image_description_is_untouched(self):
        first = mod.extract(self.docx, self.media_dir, quiet=True)["images"][0]["filename"]
        desc = os.path.join(self.media_dir, first + ".converted.md")
        with open(desc, "w", encoding="utf-8") as fh:
            fh.write("hand-edited by the consultant")
        mod.extract(self.docx, self.media_dir, quiet=True)
        with open(desc, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "hand-edited by the consultant")


class TestPptx(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.addCleanup(self.tmp.cleanup)

    def test_slide_title_becomes_the_context(self):
        slide = (
            '<?xml version="1.0"?><p:sld '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            "%s %s><p:cSld><p:spTree>"
            "<p:sp><p:nvSpPr><p:nvPr><p:ph type=\"title\"/></p:nvPr></p:nvSpPr>"
            "<p:txBody><a:p><a:r><a:t>Queue Management</a:t></a:r></a:p></p:txBody></p:sp>"
            "<p:sp><p:txBody><a:p><a:r><a:t>Supervisors triage here</a:t></a:r></a:p>"
            "</p:txBody></p:sp>"
            '<p:pic><p:blipFill><a:blip r:embed="rId3"/></p:blipFill></p:pic>'
            "</p:spTree></p:cSld></p:sld>" % (A_NS, R_NS)
        ).encode("utf-8")
        path = write_zip(
            os.path.join(self.dir, "deck.pptx"),
            {
                "ppt/slides/slide1.xml": slide,
                "ppt/slides/_rels/slide1.xml.rels": rels([("rId3", "../media/image7.jpeg")]),
                "ppt/media/image7.jpeg": jpeg_bytes(1280, 720),
                # Template chrome on the layout: present, referenced from a layout we
                # never walk, therefore never extracted.
                "ppt/slideLayouts/slideLayout1.xml": b"<x/>",
                "ppt/media/image99.png": png_bytes(1000, 1000),
            },
        )
        report = mod.extract(path, os.path.join(self.dir, "out"), quiet=True)
        self.assertEqual(report["counts"]["extracted"], 1)
        image = report["images"][0]
        self.assertEqual(image["dimensions"], [1280, 720])
        self.assertIn("slide 1", image["document_context"])
        self.assertIn("Queue Management", image["document_context"])
        self.assertIn("Supervisors triage here", image["document_context"])

    def test_slides_are_walked_in_numeric_order(self):
        entries = {}
        for n in (1, 2, 10):
            entries["ppt/slides/slide%d.xml" % n] = (
                '<?xml version="1.0"?><p:sld '
                'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
                '%s %s><p:pic><a:blip r:embed="rId1"/></p:pic></p:sld>' % (A_NS, R_NS)
            ).encode("utf-8")
            entries["ppt/slides/_rels/slide%d.xml.rels" % n] = rels(
                [("rId1", "../media/i%d.png" % n)]
            )
            entries["ppt/media/i%d.png" % n] = png_bytes(400 + n, 400)
        path = write_zip(os.path.join(self.dir, "order.pptx"), entries)
        report = mod.extract(path, os.path.join(self.dir, "order-out"), quiet=True)
        locations = [i["document_context"] for i in report["images"]]
        self.assertEqual(
            [l.split(" at ")[1].split(",")[0].split(".")[0] for l in locations],
            ["slide 1", "slide 2", "slide 10"],
        )


class TestXlsx(unittest.TestCase):
    def test_sheet_name_becomes_the_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            workbook = (
                '<?xml version="1.0"?><workbook '
                'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" %s>'
                '<sheets><sheet name="Case Volumes" sheetId="1" r:id="rId1"/></sheets>'
                "</workbook>" % R_NS
            ).encode("utf-8")
            drawing = (
                '<?xml version="1.0"?><xdr:wsDr '
                'xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/'
                'spreadsheetDrawing" %s %s><xdr:pic><xdr:blipFill>'
                '<a:blip r:embed="rId1"/></xdr:blipFill></xdr:pic></xdr:wsDr>'
                % (A_NS, R_NS)
            ).encode("utf-8")
            path = write_zip(
                os.path.join(tmp, "book.xlsx"),
                {
                    "xl/workbook.xml": workbook,
                    "xl/_rels/workbook.xml.rels": rels([("rId1", "worksheets/sheet1.xml")]),
                    "xl/worksheets/sheet1.xml": b"<worksheet/>",
                    "xl/worksheets/_rels/sheet1.xml.rels": rels(
                        [("rId1", "../drawings/drawing1.xml")]
                    ),
                    "xl/drawings/drawing1.xml": drawing,
                    "xl/drawings/_rels/drawing1.xml.rels": rels([("rId1", "../media/c.png")]),
                    "xl/media/c.png": png_bytes(700, 500),
                },
            )
            report = mod.extract(path, os.path.join(tmp, "out"), quiet=True)
            self.assertEqual(report["counts"]["extracted"], 1)
            self.assertIn("Case Volumes", report["images"][0]["document_context"])


class TestImageSize(unittest.TestCase):
    def test_png(self):
        self.assertEqual(mod.image_size(png_bytes(320, 240)), (320, 240))

    def test_jpeg(self):
        self.assertEqual(mod.image_size(jpeg_bytes(640, 480)), (640, 480))

    def test_gif(self):
        data = b"GIF89a" + struct.pack("<HH", 300, 200) + b"\x00" * 100
        self.assertEqual(mod.image_size(data), (300, 200))

    def test_bmp(self):
        data = b"BM" + b"\x00" * 16 + struct.pack("<ii", 128, -64) + b"\x00" * 40
        self.assertEqual(mod.image_size(data), (128, 64))

    def test_webp_vp8x(self):
        data = (
            b"RIFF" + b"\x00" * 4 + b"WEBP" + b"VP8X" + b"\x00" * 8
            + (799).to_bytes(3, "little") + (599).to_bytes(3, "little") + b"\x00" * 10
        )
        self.assertEqual(mod.image_size(data), (800, 600))

    def test_garbage_is_unknown_not_an_exception(self):
        self.assertIsNone(mod.image_size(b"\x00\x01\x02"))
        self.assertIsNone(mod.image_size(b""))


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.addCleanup(self.tmp.cleanup)

    def test_default_media_dir_uses_the_append_form(self):
        """`spec.docx` and `spec.pptx` must not collide on one directory."""
        self.assertEqual(
            mod.default_media_dir("documentation/spec.docx"), "documentation/spec.docx.media"
        )
        self.assertNotEqual(
            mod.default_media_dir("documentation/spec.docx"),
            mod.default_media_dir("documentation/spec.pptx"),
        )

    def test_json_out_is_written(self):
        import json

        docx = build_docx(
            os.path.join(self.dir, "a.docx"),
            [w_para(blip_rid="rId1")],
            [("rId1", "media/i.png")],
            {"word/media/i.png": png_bytes(900, 700)},
        )
        out = os.path.join(self.dir, "state", "a.docx.json")
        code = mod.main([docx, "--media-dir", os.path.join(self.dir, "m"), "--json-out", out, "--quiet"])
        self.assertEqual(code, 0)
        with open(out, encoding="utf-8") as fh:
            self.assertEqual(json.load(fh)["counts"]["extracted"], 1)

    def test_unsupported_extension_exits_one(self):
        path = os.path.join(self.dir, "x.pdf")
        with open(path, "wb") as fh:
            fh.write(b"%PDF-1.4")
        self.assertEqual(mod.main([path, "--quiet"]), 1)

    def test_non_zip_exits_one(self):
        path = os.path.join(self.dir, "x.docx")
        with open(path, "wb") as fh:
            fh.write(b"not a zip")
        self.assertEqual(mod.main([path, "--quiet"]), 1)

    def test_thresholds_are_overridable(self):
        docx = build_docx(
            os.path.join(self.dir, "t.docx"),
            [w_para(blip_rid="rId1")],
            [("rId1", "media/i.png")],
            {"word/media/i.png": png_bytes(50, 50, pad=100)},
        )
        strict = mod.extract(docx, os.path.join(self.dir, "s"), quiet=True)
        loose = mod.extract(
            docx, os.path.join(self.dir, "l"), min_px=10, min_bytes=10, quiet=True
        )
        self.assertEqual(strict["counts"]["extracted"], 0)
        self.assertEqual(loose["counts"]["extracted"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
