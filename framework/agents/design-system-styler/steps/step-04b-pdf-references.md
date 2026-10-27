---
name: step-04b-pdf-references
description: 'Read each PDF brand guide the consultant named in step-02 as text (markitdown, in memory) and take its declared colours, roles and font names as {{declared}}. Never writes a .converted.md sibling. Always runs; with no PDF references it passes straight through.'
# Variables referenced (inherited from agent):
# markitdown_setup: 'framework/shared/setup-instructions/markitdown.md'
---

# Step 4b: Read the PDF Brand Guides

This step **always runs**, on every path out of step-04 except the RF-06 *Install* branch (which aborts the run). With an empty `{{reference_pdfs}}` it does nothing and advances.

A PDF brand guide is **declared** evidence: hex codes, role labels ("Primary", "Secondary") and font names, taken as stated. It has no area data. What a PDF states **wins, per token,** over the rendered pages (step-05 applies the precedence). A declared role never overrides the reserved zones: the colour helper still checks every pick.

## A. For each PDF in `{{reference_pdfs}}`, in order

1. **Check the file.**
   - The resolved path is outside `documentation/` (e.g. `documentation/../x.pdf`, or an absolute path elsewhere) → `status = skipped — outside documentation/`, one line naming it, next PDF.
   - The file does not exist on disk → `status = skipped — not found`, one line naming it, next PDF.
2. **Check the converter.** `mcp__markitdown-mcp__convert_to_markdown` is not in the available tool list → `status = skipped — markitdown not available (see framework/shared/setup-instructions/markitdown.md)`, one line, next PDF. (Every remaining PDF gets the same status.)
3. **Convert in memory.** Build the `file:///` URI exactly as `framework/skills/convert-input-file.md` step 1 does (absolute path, backslashes → forward slashes) and call `mcp__markitdown-mcp__convert_to_markdown` with it. Hold the returned markdown **in memory only**. **Never write a `.converted.md` sibling** — those belong to the input-handler (`framework/skills/convert-input-file.md`), and the input file itself is never moved or changed (`framework/shared/input-safety.md`). A conversion error → `status = failed — could not read (<error>)`, one line, next PDF.
4. **Read the colours.**
   - **Hex codes** (`#RRGGBB`; expand `#RGB` to six digits) and **sRGB triplets** written as `RGB r g b` / `RGB r, g, b` / `rgb(r, g, b)` with 0–255 channels. Convert each triplet exactly to `#RRGGBB` (two upper-case hex digits per channel). Nothing else counts as a colour.
   - **CMYK- or Pantone-only entries** (a swatch whose only values are `C… M… Y… K…` or `Pantone …` / `PMS …`) → add the swatch's name or value to `ignored` as written (e.g. `"Pantone 186 C"`). Never convert or approximate them: a conversion is lossy, and a lookup table would itself be an invention. A swatch that gives both a hex / RGB value and a Pantone code uses the hex / RGB value and is not ignored.
5. **Map role labels to `{{declared}}`.** Take the label printed next to (or as the heading of) each colour, case-insensitive:

   | Label in the guide | `{{declared}}` field |
   |---|---|
   | *Primary*, *Brand*, *Corporate*, *Main* | `brand` **and** `primary` |
   | *Secondary*, *Supporting* | `secondary` |
   | *Accent*, *Highlight* | `accent` |
   | *Background*, *Paper* | `background` |
   | *Text*, *Body copy colour* | `text` |

   - Numbered variants (*Primary 1*, *Accent 2*, *Supporting palette*) map by their word; the first one listed fills the field, the rest are ordinary colours.
   - A field already filled by an earlier colour in the same PDF keeps the first one.
   - **No role labels at all** → the first colour listed is `brand`; the others are ordinary colours with no role.
   - Every colour read (labelled or not) is also added to `colours` (in document order, de-duplicated) so step-05 can offer them to the helper as candidates.
6. **Read the fonts.** A font name next to *Heading* / *Display* / *Headline* → `heading_family`; next to *Body* / *Text* → `body_family`. A single typeface named for the whole brand fills both. Apply `font-rules.md` §1 (a system face or generic is not a brand font: leave the field `null`).
7. **Record the page.** For every field filled, set `source_page.<field>` = `p.N` when the converted text shows page breaks, else omit it; and keep the colour **as written** for the `source` string (e.g. `"RGB 11 61 145"`).
8. **Store** `{{declared}}[<path>]` = `{ brand, primary, secondary, accent, background, surface, text, text_muted: hex | null, heading_family, body_family: string | null, colours: [hex, …], ignored: [string, …], source_page: { <field>: "p.N" }, as_written: { <field>: "<as written>" } }`.
   - No hex or RGB colour found anywhere → `status = failed — no hex or RGB colours` (fonts alone do not make a brand reference). A guide whose colours are **all** CMYK / Pantone lands here too, with its `ignored` list kept for the status line.
   - Otherwise `status = used`.
9. **Status line** (one per PDF): *"`<path>`: <n> colours<, brand `<hex>`><, fonts `<family>`>."* When `ignored` is non-empty, add one more line: *"Ignored (CMYK / Pantone only, not converted): <ignored, comma-separated>."*

## B. Advance

Nothing is decided here about whether the run can continue: step-05's **reference gate** does that, over every reference together.

---

**Next:** Read fully and follow `step-05-brand-extraction.md`.
