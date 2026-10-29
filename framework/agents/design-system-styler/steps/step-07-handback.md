---
name: step-07-handback
description: 'Present the artefact summary in the Unicorn voice, run the accept/revise/restart loop, clean up the workspace, and hand back to the orchestrator.'
# Variables referenced (inherited from agent):
# workspace_path: 'generated-docs/design-system/.workspace'
---

# Step 7: Hand Back

## A-0. Palette Choice (only when two palettes were offered)

Runs only when `{{palette_option}}` is `null` **and** either step-06 did a review render (`{{palette_options}}` non-null) or the orchestrator resumed a run at the palette choice (`{{resume_palette_choice}}`). Skip to §A otherwise. Once a palette is picked, §A-0 never runs again in this run — after the collapse, step-06 returns here and you go straight to §A.

1. **On resume only:** read `generated-docs/design-system/.workspace/options.json` and restore the run state from it: `files_to_write`, `hue_source_mode`, `hue_source`, `mode_choice`, `references`, and `shared` (`{{assign_decisions}}`, `{{brand}}`, `{{brand_fonts}}`, the font-rejection fields, the attribution inputs). Set `{{palette_options}}` non-null (both palettes exist) and rebuild `{{palettes}}` from the two palettes' per-mode `tokens` / `on_colours` / `adjustments` exactly as step-06 §F.3 maps them for a final render. **Do not re-`Write` the review files** — they are large, and round-tripping their bytes risks truncating the file the consultant is about to judge. Print each `review_files` entry as a `file:///<absolute path>` link and ask the consultant to open both before answering.
2. Say, in one line, why there are two options (from `{{assign_decisions}}`): the brand colour is reserved for status, and the site's own non-reserved colour is in only marginal use — so the choice is genuinely open.
3. Ask with `AskUserQuestion`:
   - Header: `Palette`
   - Question: *"Two palettes are open in your browser (Option 1 / Option 2 tabs in each review file). They differ only in primary, secondary and accent. Which one should the design system use?"*
   - Options — **neither is marked Recommended**; the choice is genuinely open:
     1. `Option 1 — neutral (primary {{neutral_primary_hex}})` — a brand-tinted charcoal primary; the brand colour stays visible as identity (header strip), never as an action colour.
     2. `Option 2 — site colour (primary {{site_colour_primary_hex}})` — the site's own non-reserved colour as primary; may read less like the brand, because the site uses it sparingly.
   - Free-text `Other` → coerce to the nearest option ("the blue one" → Option 2); if unreadable, re-ask once; still unclear → re-ask, never default.
4. Set `{{palette_option}}` = `neutral` or `site-colour` (palette key `neutral` / `site_colour`).
5. **Collapse.** Re-enter step-06 for a **final render** with only the chosen palette: each mode file is rendered from that palette's `tokens` (with `meta.palette_option` set), one `:root` palette block, empty `{{PALETTE_TABS}}`, written to the real path and verified as usual. The review files and `options.json` stay in `.workspace/` until §C.
6. Continue at §A, which now also prints the palette line below.

## A. Summary in Unicorn Voice

Output one short, concrete summary listing the written file(s), token counts, and provenance breakdown. No marketing language. No chatbot warmth.

Lead with the hue-source file (the grounded one), then the derived file if there is one.

**Single-file template:**

> "Wrote `generated-docs/design-system/design-system-{{mode}}.html` — `{{n_colors_extracted}}/12` colour tokens and `{{n_fonts_extracted}}/4` font tokens extracted from the references; the rest are system-derived (house defaults, neutral ladder, `HOUSE_STATUS`). Contrast: `{{cv_pass_count_<mode>}}/4` pairs pass at WCAG AA (`{{cv_adjustment_count_<mode>}}` adjustments). Opened in your browser (if not, open it via `file://`). Ready, or want changes?"

**Two-file template:**

> "Wrote two files. `generated-docs/design-system/design-system-{{hue_source_mode}}.html` — **primary**, the extracted palette: `{{n_colors_extracted}}/12` colour tokens and `{{n_fonts_extracted}}/4` font tokens extracted from the references; the rest are system-derived (house defaults, neutral ladder, `HOUSE_STATUS`). Contrast `{{cv_pass_count_<hue>}}/4` (`{{cv_adjustment_count_<hue>}}` adjustments).
> `generated-docs/design-system/design-system-{{derived_mode}}.html` — derived from the same brand hues, not separately extracted; 11 colours + 3 shadows re-lit, the `brand` identity colour, typography and motion shared verbatim. Contrast `{{cv_pass_count_<derived>}}/4` (`{{cv_adjustment_count_<derived>}}` adjustments).
> Opened in your browser, hue-source first (if they didn't open, open them via `file://`). On a revise, only the re-rendered file(s) re-open.
> Ready, or want changes?"

Variants — prepend whichever apply:

- **Always — one line per reference**, in the order given: *"`<kind>` `<ref>`: `<status>`; contributed <token groups>."* — e.g. *"pdf `documentation/acme-brand-guide.pdf`: used; contributed brand, secondary, fonts."*, *"url `https://intranet/brand`: failed — login page."* Token groups: `brand`, `primary` / `secondary` / `accent`, `neutrals`, `fonts`, `area weights`.
- **Always, when a fill misses its contrast target** — any `{{cv_adjustments_<mode>}}` line reading `<fill>: fill … below 3:1` or `best label … below 4.5:1`, in either written mode: *"`<fill>` `<hex>` is only `<ratio>`:1 against the `<mode>` surface — extracted fills are reported, never moved. If it reads too faint, say Revise and name a lighter / darker value."* One line per fill. **This line is not optional**: it is most likely when the fill and the surface come from different references (e.g. a PDF's navy primary on a dark site's surface), and otherwise it is visible only inside the artefact's contrast section.
- **When any PDF had CMYK / Pantone-only colours** (step-04b `ignored`): *"Ignored (CMYK / Pantone only, not converted): <list>."*

- **Always, when a colour role was rejected or filled by the helper** — print `{{assign_decisions}}` as a short list (one line each, e.g. *"primary #FA551E rejected: reserved zone (H37 C0.210)"*). Then the one of these that applies, if any (a pick rejected as `not found among the page's rendered colours` and refilled from an extracted colour needs neither):
  - two palettes were offered → *"You picked **{{palette_option}}** (primary {{primary_hex}}); the other option was discarded."*
  - the primary fell back to a brand-tinted neutral and no second option existed → *"No alternative palette was offered: no non-reserved site colour was in use, even marginally."*
- If `brand` differs from `primary`: *"The brand colour {{brand_hex}} is kept as an identity colour (header / logo strip / brand mark) — never a button, link or badge colour."*

- If `{{hue_source}} == "declared-light"`: *"No reference declared a background, so the light palette is the hue source and the neutrals come from the neutral ladder."*
- If `{{extracted_scheme}} == "dark"`: *"The site shipped a **dark** palette, so dark is the hue source here and light is the derived mode."* — this inverts the common case and the consultant should not have to infer it from the filenames.
- If `{{font_rejected_heading}}` or `{{font_rejected_body}}` is set: *"The site's `{{slot}}` font resolved to `{{font_rejected_<slot>}}` — a system face, not a brand typeface — so that family is the interim fallback (`Inter`) instead."* Name both slots if both were rejected. **This line is not optional.** Without it the extracted-typography count drops by one or two and the family reads `system-derived` with nothing explaining why, which looks like a weak extraction rather than a deliberate rejection. If the consultant wants that font anyway, the revise branch in §B is where they say so — and where it is declined, with reasons.
- If a `{{brand_fonts}}.families` entry has `status: "substituted"` and `evidence` beginning `site @font-face`: *"The site declares its `{{slot}}` font as `{{brand}}` but serves it as **`{{loadable}}`**, so that is what the file shows. `{{brand}}` stays first in the token stack."* Use this line instead of the next one for that slot — the face is not licensed-and-missing, the site itself renders `{{loadable}}`.
- If any other `{{brand_fonts}}.families` entry has `status: "substituted"`: *"The site's `{{slot}}` font is `{{brand}}` — a licensed face that is not available from Google Fonts — so the artefact loads **`{{loadable}}`** as its substitute. `{{brand}}` stays first in the token stack, so a machine with it installed renders the real face."* Name both slots if both were substituted. **This line is not optional.** Without it the consultant sees a specimen rendering in a font nobody chose, with the brand name still on the label, and reads it as the pipeline getting the brand wrong. Say which face they are looking at. If they want a different substitute, the revise branch in §B takes it — the alternates are in `data/font-availability-rules.md` §3.
- If any `{{brand_fonts}}.families` entry has `status: "unverified"`: *"I couldn't confirm whether `{{brand}}` is on Google Fonts, so the file shows **`{{loadable}}`** behind it. `{{brand}}` stays first in the stack, so a machine with it installed renders the real face."* **Also not optional**: the specimen shows a stand-in the consultant did not choose, on unconfirmed evidence. If they want a different stand-in, the revise branch in §B takes it.
- If any `{{brand_fonts}}.families` entry has `delivery: "link"`: *"`{{loadable}}` couldn't be embedded (`{{reason}}`), so it loads from Google Fonts; without a network connection that sample falls back to the system font."* `{{reason}}` is that param's `failed` reason from `{{font_embed_report}}`. One line per such family. **Not optional**: the file otherwise renders the same offline as online, and this is the one case where it does not.
- If `{{files_to_write}}` contains a mode the consultant did **not** ask for (they chose one mode but the hue-source file was written too): *"You asked for `{{requested_mode}}` only; I also wrote the `{{hue_source_mode}}` file because that's the palette the references actually set — it's kept as the grounded record and marked primary."*

Always name which file is primary when two were written. `{{primary_mode}}` is always `{{hue_source_mode}}`.

## B. Accept/Revise/Restart Loop

Use `AskUserQuestion`:

- Question: *"Accept the design system, request specific changes, or restart from inputs?"*
- Header: `Accept?`
- multiSelect: false
- Options:
  1. `Accept — hand back to orchestrator (Recommended)`
  2. `Revise — change specific tokens`
  3. `Restart — re-enter inputs`

### Branches

- **Accept** — proceed to §C (workspace cleanup), then declare done.
- **Revise** — acts on the **collapsed** (final) files only; the palette choice is made by then and is not re-asked. To switch options, the consultant picks Restart. Accept the consultant's revision instructions in their next message. Revisions are **mode-scoped**; establish which mode a named token belongs to before applying it (ask if genuinely ambiguous). Apply the changes:
   - **Colour revisions go through the helper** (`framework/tools/colour-tokens.cjs`), never hand arithmetic. A revised **hue-source** colour: update the hue-source set, run `measure` on it (new on-colours, pairs, adjustments), **and** — unless the other mode is extracted (`extracted-both`) — run `derive` on the measured set to re-derive the counterpart; take the derived colours, on-colours and numbers from its output. Write every result back into `{{palettes}}` (step-06 §C checks the rendered hexes against it) before re-entering step-06.
   - **A reserved colour is declined for `primary`, `secondary` or `accent`.** If the requested hex is in the reserved red → orange → amber zone (check with the helper — never by eye), say that red / orange / amber are kept for error and warning in this design system, offer to put it on `brand` (identity only) instead, and re-present §A's prompt. `brand` itself may be any colour.
   - **Revising a hue-source token** — the helper step above re-derives the affected counterpart token(s) in the derived set, which preserves the invariant that the two files describe the same brand. Re-deriving is what preserves the invariant that the two files describe the same brand; silently leaving the derived value stale would break it. If the consultant explicitly scopes the change to one mode ("only in light"), honour that and skip the re-derivation — but say that the two files now diverge.
   - **Revising a derived token** — override that value in the derived set only (then `measure` that mode, as below). Do **not** propagate backwards into the hue-source set: the hue source is the grounded record, and a consultant tweak to a derived value is a downstream correction, not new evidence about the brand.
   - For colour overrides in either mode: run `measure` on that mode's revised set so its pairs, fills, on-colours and adjustments are current.
   - For typography or effect overrides: write the new value into the corresponding in-memory structure. Note that the 19 shared tokens (typography + motion) are shared across modes — revising one changes **both** files.
   - **After revising `heading-family` or `body-family`, re-run `embed` and rebuild `{{brand_fonts}}`** — run step-05b §G's `node framework/tools/font-embed.cjs embed …` over the new distinct `param`s (it overwrites `.workspace/font-faces.css`), then rebuild that slot's `families` entry, `delivery`, the deduped `links` list and `embedded_bytes`, per `data/font-availability-rules.md` §6.2–§6.4. A stale `brand_fonts` or faces file would make the artefact embed the *previous* face while the token names the new one, and step-06 §C's availability assertions would halt the re-render. Do both before re-entering step-06, not after; step-06 renders a fresh file with an empty marker block, so no faces from the previous family survive.
   - **A revision that names a non-brand family is declined.** If the consultant asks for `Arial`, `Helvetica`, `Segoe UI`, `system-ui`, or anything else in `data/font-rules.md` §1 as `heading-family` or `body-family`, do not write it. Say plainly that the design system does not use system faces as brand typefaces, name the nearest allowed alternative from `data/font-availability-rules.md` §5, and re-present §A's prompt. Then honour whatever they choose next.
     - Decline it **here**, conversationally. Revise re-enters step-06, whose §C brand-family assertion would catch it — but that surfaces as a hard halt with no recovery path, which is a dead end for someone who just asked a reasonable-sounding question. This guard is the graceful surface; §C stays the fail-closed backstop.
     - A genuine exception is recorded downstream, not bought by weakening the generator — the same escape hatch `framework/assets/design-system-standards.html` §7 already establishes for component-level exceptions.
   - **A revision that names a proprietary family is accepted, not declined.** If the consultant asks for a real branded typeface that is not on Google Fonts — `Gotham`, `Circular`, `Satoshi`, their own commissioned face — write it, and run `data/font-availability-rules.md` §1's ladder over it exactly as step-05 §4b would: the family goes in first position, its substitute behind it, and the §A disclosure line names both on the next pass. Do **not** reach for the decline above; that is the other axis. The consultant has told us what the brand *is*, which is evidence, and refusing it would discard the very thing this pipeline is trying to capture.
     - If they name a substitute directly ("use Montserrat behind Gotham"), honour it — check only that it is in §4.1 and not in §4.2, and say so plainly if it is not, offering that row's alternates.
     - If the ladder returns `unverified` (no network), write the family with §3's classification-fallback substitute behind it, as step-05 §4b would, and say availability could not be confirmed this run.
   - For provenance: a revised value retains the marker that was on it before — the consultant's edit is treated as a downstream correction, not a re-source. (Per the locked decision, there is no `consultant-specified` marker in v1.) A revised derived token also keeps its `derived: …` source string.
   - Re-render **only the affected file(s)** by re-entering step-06's per-mode procedure for those modes, including per-file sha256 + `verify-artifact-write`. When a hue-source token changed and was re-derived, both files are affected.
   - Loop back to §A and present the updated summary.
- **Restart** — first delete `generated-docs/design-system/.workspace/options.json` (if present) so a later invocation cannot offer to resume a palette choice this restart abandoned; then re-enter `step-02-inputs.md`. The previously-written `design-system-*.html` files are left in place; the next step-06 will overwrite them. Note that extraction runs again, so the scheme is re-detected and the step-05b §E mode question is re-asked — the mode choice is not sticky across a restart.

The accept/revise/restart loop continues until the consultant chooses Accept.

## C. Workspace Cleanup

After acceptance:

1. Delete `generated-docs/design-system/.workspace/` and its contents: `Bash rm -rf generated-docs/design-system/.workspace`.
2. If deletion fails, log a warning but do not halt — workspace cleanup is best-effort.
3. If any URL reference was given, call `mcp__playwright__browser_close()` once more — a backstop for a tab left open after step-04. With nothing open it is a no-op and launches nothing; ignore its result.

## D. Hand Back to Orchestrator

Output the final handback line:

> "Design system accepted. Handing back to the orchestrator."

The orchestrator's handback gate is satisfied when:

- **Every** mode in `{{files_to_write}}` has its `generated-docs/design-system/design-system-<mode>.html` on disk, each verified by `verify-artifact-write` with a `pass`. This always includes `{{hue_source_mode}}`.
- Exactly one written file carries `meta.primary: true`, and it is the `{{hue_source_mode}}` file.
- The consultant has chosen Accept.
- The workspace folder has been removed.

A partial pair — hue-source file verified but the requested derived file missing — does **not** satisfy the gate.

---

**STOP** — design-system-styler workflow complete.
