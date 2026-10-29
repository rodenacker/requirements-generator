---
name: step-05-brand-extraction
description: 'Extract colours, font families and weights from the lead URL (one batched data-file read), merge every reference (later URLs, PDF brand guides — the PDF wins per token), run the reference gate (RF-14), and write the helper input.'
# Variables referenced (inherited from agent):
# prompt_brand_extraction: 'framework/agents/design-system-styler/prompt-templates/brand-extraction.md'
# data_color_rules: 'framework/agents/design-system-styler/data/color-extraction-rules.md'
# data_font_rules: 'framework/agents/design-system-styler/data/font-rules.md'
# data_font_availability_rules: 'framework/agents/design-system-styler/data/font-availability-rules.md'
# data_contrast_validation: 'framework/agents/design-system-styler/data/contrast-validation.md'
# data_insufficient_handling: 'framework/agents/design-system-styler/data/insufficient-data-handling.md'
# workspace_path: 'generated-docs/design-system/.workspace'
---

# Step 5: Brand Extraction and Reference Merge

**Runs whenever any reference is `used` or `pending`.** Three parts:

- **§1–§3, §4, §5, the lead URL** — only when step-04 captured a lead URL **in this run** (`{{lead_url}}` set by this run's step-04 and `generated-docs/design-system/.workspace/css-content.txt` written by it). Otherwise, and whenever a sub-step below says "skip to §7", skip those lead-URL sub-steps.
- **§4a + §4b, the font merge and availability** — always (on a PDF-only run, or after the lead URL failed, they run over the declared and later-URL families). A "skip to §7" from a lead-URL sub-step means: go to §4a, then §4b, then §7.
- **§7, the merge and the reference gate** — always.

**Only this run's `used` references count.** Every file read below (`computed-tokens.json`, `computed-tokens-<n>.json`, `css-content.txt`) is read only for a URL reference whose `status` in **this run's** `{{references}}` is `used`. A workspace file left by an earlier or restarted run, or by a reference that is now `failed` / `skipped`, is ignored.

No reference `used` or `pending` at all → go straight to §7's reference gate, which raises `RF-14`. Step-02 starts every run (including a Restart) with `{{lead_url}}`, `{{declared}}`, `{{extraction_status}}` and `{{merged_sources}}` unset.

(Note: `{{extraction_status}}` is not yet `"success"` at this point — step-04 deliberately defers setting it; on the happy path it is unset here and set to `"success"` after the lead URL's extraction.)

## Workspace Read

Read CSS content from disk (not from in-memory state of step-04):

1. Read `generated-docs/design-system/.workspace/css-content.txt` → store as `{{primary_css_content}}`.
2. Read `generated-docs/design-system/.workspace/metadata.json` → confirm `css_source_type`, `css_source_url`, `lead_url`.

**If workspace file read fails:**

- Log: "Workspace read failed — css-content.txt not found or unreadable".
- Set `{{extraction_status}} = "workspace_read_failed"` and the lead URL's reference `status` to `failed — workspace read failed`.
- Skip to §7.

## Extraction Orchestration

Read all five data files in a **single batched message** (the harness runs the reads concurrently) — they are independent, so there is no reason to serialise the reads:

- `framework/agents/design-system-styler/prompt-templates/brand-extraction.md` (extraction overview + Section 7 output format)
- `framework/agents/design-system-styler/data/insufficient-data-handling.md`
- `framework/agents/design-system-styler/data/color-extraction-rules.md`
- `framework/agents/design-system-styler/data/font-rules.md`
- `framework/agents/design-system-styler/data/font-availability-rules.md`

With all five in context, apply their rules to `{{primary_css_content}}` in the reasoning order below — **critically, the insufficient-data gate (section 2) first**: if it short-circuits, go to §7 *before* doing any colour / typography extraction. Sizes, line heights, shadows and motion are **never extracted**: step-05b fills them from `data/house-defaults.md`. (`contrast-validation.md` is **not** read here — contrast validation is a step-05b concern, run against the final token set.)

### 1. Extraction Overview (already loaded)

From `brand-extraction.md` (read in the batch above), use:

- Extraction purpose and the data-file application order.
- Section 7 output format — the target structure for in-memory extraction results.

### 2. Insufficient-Data Check

Apply `insufficient-data-handling.md` (already loaded) — its threshold check:

- Count distinct non-white/non-black hex colors in `{{primary_css_content}}`.
- **If fewer than 3:** Set `{{extraction_status}} = "insufficient_data"` and the lead URL's reference `status` to `failed — too few colours`, log the diagnostic, and skip to §7. Do NOT halt: later URLs and PDF references still count.
- **If 3 or more:** Continue.

### 3. Colour Extraction (7 brand tokens)

Apply `color-extraction-rules.md` (already loaded):

- Section 1: CSS Analysis Strategy.
- Section 2: Colour Extraction (collect, normalize to `#RRGGBB`, deduplicate, rank).
- Section 3: Colour-to-Token Mapping for the 7 brand tokens (primary, secondary, accent, background, surface, text, text-muted) using heuristics and derivation fallbacks. The `primary` / `secondary` / `accent` results are **picks**, not final roles: a missing pick stays `null`, and no hue is ever rotated or invented here.

Status colours (`success`, `warning`, `error`, `info`) are NOT extracted here — they are always populated by step-05b.

Store: `{{extracted_colors}}` as the structure defined in `brand-extraction.md` Section 7. Tokens that could not be extracted remain `null`.

These are the **lead URL's** colours. §7 merges them with every other reference and writes the helper input.

### 4. Typography — Families

Apply `font-rules.md` (already loaded) to extract `heading_family`, `heading_weight`, `body_family`, `body_weight` — its Section 0 on the Playwright path (`computed-tokens.json` present), its Section 4 on the WebFetch fallback. Tokens that could not be extracted remain `null`.

Both paths reject **non-brand families** per `font-rules.md` §1 (system faces such as `Arial`, `Helvetica`, `Segoe UI`; generics; `next/font` hash aliases). A chain with no surviving candidate leaves the family `null` — this is the ordinary unset path, not an error (§4a may still fill it from another reference; otherwise step-05b uses the interim font fallback). When that happens, also store the rejection record §1 calls for:

- `{{font_rejected_heading}}` / `{{font_rejected_body}}` — the first *named* family in the rejected chain (the value the pre-§1 rule would have selected), or `null` if the chain held no named family at all. Step-07 surfaces it so the consultant sees why the family is not the lead URL's.

### 4a. Typography — Merge the families across references

Per family slot (`heading_family`, `body_family`), first non-null wins:

1. **Declared** — the first PDF in `{{declared}}` (step-04b) that names it. `source`: `<file>.pdf p.N: "<as written>"` (drop `p.N` when unknown).
2. **The lead URL** — §4 above. `source`: `<lead url> <selector>`.
3. **Later URLs** — each `computed-tokens-<n>.json` in order: `sampleElements.h1` (then `h2`, `h3`) `.fontFamily` for heading, `sampleElements.body.fontFamily` for body, with `font-rules.md` §0/§1 applied exactly as for the lead. `source`: `<url> sampleElements.<element>`.

Weights follow the same order minus the PDF (a guide's weights are not taken): lead URL (§5), then later URLs' `sampleElements` per `font-rules.md` §5. Every merged family carries `prov: extracted`.

### 4b. Typography — Availability & Substitution

Apply `font-availability-rules.md` (already loaded) to each family §4a **selected** — a family left `null` there is skipped entirely and handled by step-05b's interim fallback instead. On a PDF-only run (no lead URL) read `font-availability-rules.md` now and run this sub-step on the declared families; E1 then has no evidence on disk, so the ladder starts at E2. This is the second of the two axes that file's §0 defines: Section 4 above decided *"is it a brand?"*, this sub-step decides *"can we fetch it?"*.

Run its §1 evidence ladder per family, canonicalising the name per §2 before any lookup or probe (`node framework/tools/font-embed.cjs candidates --name <raw>` — its `candidates[0]` is the name to look up, its `weight` is the weight the name carries):

1. **E1** — the evidence is already on disk from step-04, so read it rather than fetching anything:
   - `generated-docs/design-system/.workspace/computed-tokens.json` → `sources` — a `fonts.googleapis.com` href naming this family proves it is Google-hosted, and its `family=` segment is the canonical spelling. Prefer that spelling over §2's derived one. **Playwright path only** — this file is absent on the WebFetch fallback, in which case skip this bullet rather than treating the missing file as evidence of anything.
   - `{{primary_css_content}}` (already in memory, both paths) → an `@font-face` for this family whose `src: url(...)` points at a self-hosted or licensed-foundry origin. **Suspicion only — never a verdict.** Many Google-hosted faces are self-hosted; concluding here is the documented way to implement this wrongly.
   - The same `@font-face` blocks' `src` URLs → run `node framework/tools/font-embed.cjs file-family --url <url>` on each. A returned family that **differs** from the canonicalised declared name (`candidates[0]`) and resolves Google-hosted (§4.1, or the E3 `resolve` call) makes the slot `substituted` with that family as `loadable`, evidence `site @font-face for <declared> serves <file>`. This outranks E2 (§1 E1).
   - On the **WebFetch fallback** path, expect E1 to resolve rarely: the content is LLM-summarised rather than raw CSS, so `@font-face` blocks and link hrefs are frequently absent. That pushes families to E2/E3, which is the correct outcome — it does **not** license a guess.
2. **E2** — the curated tables: §4.1 → `google-native`; §3 → `substituted`.
3. **E3** — only if E1 and E2 were both inconclusive, or to confirm an E1 file-name family not in §4.1: **one** `node framework/tools/font-embed.cjs resolve --name <raw> [--name <raw>]` call per run carrying every name still open — the raw declared name for an unresolved slot, the `file-family` result itself for an E1 family to confirm — mapped per §1's verdict table. The helper owns the candidates, the control and the request ceiling.
4. **E4** — otherwise `unverified`, with §3's classification-fallback substitute as `loadable`.

For each family, store the record `font-availability-rules.md` §6.2 specifies:

- `{{font_availability_heading}}` / `{{font_availability_body}}` — `{ brand, loadable, param, status, evidence }`, with `status` one of `google-native | substituted | unverified` and `loadable` / `param` never `null`. `brand` is the resolved family; step-05b §G adds `delivery`.
- Keep, per slot, the `weight` E1's `file-family` returned for the file serving its face and the `weight` `candidates` reported for the declared name; §5 below applies `font-rules.md` §5's file/name-weight rule with them.

For a `substituted` or `unverified` family, rewrite that token's value to the three-name shape in §6.1 — `'<Brand>', '<Loadable>', <generic>`. **Do not change `prov`**: the family is still exactly as extracted, and availability is not a provenance question (`prov` has two values, and this is not one of them). Leave `google-native` values in the two-name shape.

**When §2 resolved a different spelling than the CSS declared, rewrite the token to the resolved name** (per §6.1) and record the raw alias in `evidence`. A site names faces after its own build — `GeistSans` is `Geist`, `sohne-var` is `Söhne` — and the raw form neither loads nor means anything elsewhere. This applies on the `google-native` path too, not only when substituting.

**Never unset a family because it is unavailable.** That is the §1-rejection outcome, on the other axis. Here the brand evidence is real and is preserved in first position no matter what the ladder returns.

### 5. Typography — Weights

Apply `font-rules.md` §5 (already loaded) to extract `heading_weight` and `body_weight` only, including its file/name-weight rule (§4b's `file-family` and `candidates` weights, first in that order, beat any computed weight and fill a missing one when they are within `400`–`700`). A weight not found stays `null`; step-05b fills it from the interim font fallback.

### 6. Assemble In-Memory Extraction Results

Assemble the structured output per Section 7 format from `brand-extraction.md`:

- `{{extracted_colors}}` — 7 brand tokens (status colours not included)
- `{{extracted_typography}}` — 4 tokens: `heading_family`, `heading_weight`, `body_family`, `body_weight` (the 11 size and line-height tokens are house defaults, never extracted)
- no effect tokens: shadows and motion are house defaults, never extracted
- `{{extraction_status}} = "success"` (only if extraction completed without an early skip; otherwise the prior status is preserved)
- `{{font_rejected_heading}}` / `{{font_rejected_body}}` — set per Section 4 above, else `null`. Carry them through step-05b unchanged (they describe what the *lead URL* held, so a fallback fill does not clear them) so step-07 §A can state why a family is `system-derived`.
- `{{font_availability_heading}}` / `{{font_availability_body}}` — set per Section 4b above for each family §4a selected, else `null` (an unset family has no availability question until step-05b fills it). Step-05b §G assembles them into `meta.brand_fonts`; step-07 §A discloses every `substituted` and `unverified` outcome.

### 7. Merge the References, Reference Gate, Helper Input

Runs always (§1–§6 may have been skipped).

**Candidates** (`assign` `candidates`):

- **Pooled area weights, plain sums.** Add up `colourWeights` across the URL workspace files of this run's `used` URL references only — `computed-tokens.json` (the lead, when its reference is still `used` after §1–§3) and each `computed-tokens-<n>.json` whose URL is `used` — summing the `weight` of the same hex. Sort descending. A lead URL that failed in §2 or the workspace read contributes nothing.
- **Rendered evidence** (`assign` `rendered`): the union of `renderedColours` across the same `used` URL workspace files, deduplicated. Evidence for the helper's real-use gate only — never added to `candidates`. Omit the field on the WebFetch path.
- **WebFetch path** (no `computed-tokens.json`): every deduplicated **chromatic** colour from the lead URL's Section 2, each with `weight: null`.
- **PDF colours:** every `{{declared}}[*].colours` hex not already present, each with `weight: null`, appended after the URL colours.

**Picks** (`assign` `picks`), per token — the first that states it wins:

1. `{{declared}}` — the first PDF (in `{{references}}` order) that declares `primary` / `secondary` / `accent`.
2. The lead URL's Section 3 pick.
3. `null` (the helper's cascade fills it).

`picks.brand` = the first PDF's declared `brand`, else `null` (the helper then picks the largest-area colour). A declared role never overrides the reserved zones: the helper checks every pick.

**Pick origins** (`assign` `pick_origins`): per non-null pick, `"pdf"` when rule 1 gave it, `"page"` when rule 2 did; omit a `null` pick. The helper drops a `"page"` pick that the page never renders (its real-use gate, `framework/tools/colour-tokens.cjs`), so a framework default such as Bootstrap 4's unthemed `--primary` cannot become a role.

**Neutrals** (`assign` `neutrals`) are taken **as a set**, so a light page's text never meets a dark page's background:

1. The first PDF that declares `background` → that PDF's declared `background`, `surface`, `text`, `text_muted`.
2. Else the lead URL's Section 3 neutrals.
3. Else the first PDF that declares any neutral → its declared ones.
4. Else none.

Every neutral not given is `null`; the helper fills it from its neutral ladder.

**Reference gate.** Zero candidates **and** zero non-null picks (every reference failed or skipped, or every PDF had no hex / RGB value) → raise **`RF-14`** per `framework/shared/refusal-registry.md > RF-14 — brand_reference_missing`: print its line plus one line per reference with its `status`, clean up `.workspace/` (step-07 §C), and end the run. Nothing is written; prior design-system files are untouched.

**Write the helper input.** Write `generated-docs/design-system/.workspace/assign-in.json` (plain `Write`; workspace scratch):

```json
{ "mode": null,
  "candidates": [ { "hex": "#RRGGBB", "weight": 0 } ],
  "picks": { "primary": "#RRGGBB" | null, "secondary": "#RRGGBB" | null, "accent": "#RRGGBB" | null, "brand": "#RRGGBB" | null },
  "pick_origins": { "primary": "page" | "pdf", "secondary": "page" | "pdf", "accent": "page" | "pdf" },
  "rendered": [ "#RRGGBB" ],
  "neutrals": { "background": "#RRGGBB" | null, "surface": "#RRGGBB" | null, "text": "#RRGGBB" | null, "text_muted": "#RRGGBB" | null } }
```

`mode` is set by step-05b §C once scheme detection (§A-bis) has classified the merged `background`. No `status` field — the helper starts from its house status set.

**Sources.** Every extracted value's `source` names its reference: `<url> <selector>` for a page, `<file>.pdf p.N: "<as written>"` for a PDF (e.g. `brand-guide.pdf p.4: "RGB 202 43 61"`). Keep a `{{merged_sources}}` map `{ <token>: <source> }` for step-05b §C, which tags the helper's output.

Contrast validation runs **after** step-05b, not here — it must validate against the final token set.

---

**Next:** Read fully and follow `step-05b-fill-and-derive.md`.
