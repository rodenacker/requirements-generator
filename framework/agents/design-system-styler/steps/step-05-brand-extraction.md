---
name: step-05-brand-extraction
description: 'Orchestrate brand extraction by loading data files together (one batched read) and applying extraction logic to {{primary_css_content}}.'
# Variables referenced (inherited from agent):
# prompt_brand_extraction: 'framework/agents/design-system-styler/prompt-templates/brand-extraction.md'
# data_color_rules: 'framework/agents/design-system-styler/data/color-extraction-rules.md'
# data_font_rules: 'framework/agents/design-system-styler/data/font-rules.md'
# data_font_availability_rules: 'framework/agents/design-system-styler/data/font-availability-rules.md'
# data_typography_scale_rules: 'framework/agents/design-system-styler/data/typography-scale-rules.md'
# data_shadow_motion_rules: 'framework/agents/design-system-styler/data/shadow-motion-rules.md'
# data_contrast_validation: 'framework/agents/design-system-styler/data/contrast-validation.md'
# data_insufficient_handling: 'framework/agents/design-system-styler/data/insufficient-data-handling.md'
# workspace_path: 'design-system/.workspace'
---

# Step 5: Brand Extraction (URL-driven)

**Skip condition:** this step runs **only** when step-04 captured CSS to extract from. Skip it entirely and route to `step-05b-domain-inference.md` whenever **any** of the following holds (every run now reaches this step via step-04b, so this guard must catch every no-CSS path):

- `{{reference_url}}` is null (consultant skipped the URL), or
- `{{extraction_status}}` is set to any non-CSS value — `no_url`, `fetch_failed`, `no_css`, `css_fetch_failed`, or `playwright_unavailable` (the RF-06 *Drop URL* / unavailable path), or
- no `design-system/.workspace/css-content.txt` was written (equivalently, `{{primary_css_content}}` is unavailable).

In all those cases, step 5b infers every token per-run from the `{{domain}}` set in step-04b. (Note: `{{extraction_status}}` is not yet `"success"` at this point — step-04 deliberately defers setting it; on the happy path it is unset here and set to `"success"` after extraction.)

## Workspace Read

Read CSS content from disk (not from in-memory state of step-04):

1. Read `design-system/.workspace/css-content.txt` → store as `{{primary_css_content}}`.
2. Read `design-system/.workspace/metadata.json` → confirm `css_source_type`, `css_source_url`, `reference_url`.

**If workspace file read fails:**

- Log: "Workspace read failed — css-content.txt not found or unreadable".
- Set `{{extraction_status}} = "workspace_read_failed"`.
- Skip to `step-05b-domain-inference.md`.

## Extraction Orchestration

Read all seven data files in a **single batched message** (the harness runs the reads concurrently) — they are independent, so there is no reason to serialise the reads:

- `framework/agents/design-system-styler/prompt-templates/brand-extraction.md` (extraction overview + Section 7 output format)
- `framework/agents/design-system-styler/data/insufficient-data-handling.md`
- `framework/agents/design-system-styler/data/color-extraction-rules.md`
- `framework/agents/design-system-styler/data/font-rules.md`
- `framework/agents/design-system-styler/data/font-availability-rules.md`
- `framework/agents/design-system-styler/data/typography-scale-rules.md`
- `framework/agents/design-system-styler/data/shadow-motion-rules.md`

With all seven in context, apply their rules to `{{primary_css_content}}` in the reasoning order below — **critically, the insufficient-data gate (section 2) first**: if it short-circuits, route to `step-05b-domain-inference.md` *before* doing any colour / typography / effect extraction. (`contrast-validation.md` is **not** read here — contrast validation is a step-05b concern, run against the final token set after the domain-inference fill.)

### 1. Extraction Overview (already loaded)

From `brand-extraction.md` (read in the batch above), use:

- Extraction purpose and the data-file application order.
- Section 7 output format — the target structure for in-memory extraction results.

### 2. Insufficient-Data Check

Apply `insufficient-data-handling.md` (already loaded) — its threshold check:

- Count distinct non-white/non-black hex colors in `{{primary_css_content}}`.
- **If fewer than 3:** Set `{{extraction_status}} = "insufficient_data"`, log the diagnostic, and skip to `step-05b-domain-inference.md`. Do NOT halt.
- **If 3 or more:** Continue.

### 3. Colour Extraction (7 brand tokens)

Apply `color-extraction-rules.md` (already loaded):

- Section 1: CSS Analysis Strategy.
- Section 2: Colour Extraction (collect, normalize to `#RRGGBB`, deduplicate, rank).
- Section 3: Colour-to-Token Mapping for the 7 brand tokens (primary, secondary, accent, background, surface, text, text-muted) using heuristics and derivation fallbacks.

Status colours (`success`, `warning`, `error`, `info`) are NOT extracted here — they are always populated by step-05b.

Store: `{{extracted_colors}}` as the structure defined in `brand-extraction.md` Section 7. Tokens that could not be extracted remain `null`.

### 4. Typography — Families

Apply `font-rules.md` (already loaded) to extract `heading_family`, `heading_weight`, `body_family`, `body_weight` — its Section 0 on the Playwright path (`computed-tokens.json` present), its Section 4 on the WebFetch fallback. Tokens that could not be extracted remain `null`.

Both paths reject **non-brand families** per `font-rules.md` §1 (system faces such as `Arial`, `Helvetica`, `Segoe UI`; generics; `next/font` hash aliases). A chain with no surviving candidate leaves the family `null` for step-05b to infer — this is the ordinary unset path, not an error. When that happens, also store the rejection record §1 calls for:

- `{{font_rejected_heading}}` / `{{font_rejected_body}}` — the first *named* family in the rejected chain (the value the pre-§1 rule would have selected), or `null` if the chain held no named family at all. Step-07 surfaces it so the consultant sees why the family is domain-inferred.

### 4b. Typography — Availability & Substitution

Apply `font-availability-rules.md` (already loaded) to each family Section 4 **selected** — a family left `null` there is skipped entirely and handled by step-05b's inference instead. This is the second of the two axes that file's §0 defines: Section 4 above decided *"is it a brand?"*, this sub-step decides *"can we fetch it?"*.

Run its §1 evidence ladder per family, canonicalising the name per §2 before any lookup or probe:

1. **E1** — the evidence is already on disk from step-04, so read it rather than fetching anything:
   - `design-system/.workspace/computed-tokens.json` → `sources` — a `fonts.googleapis.com` href naming this family proves it is Google-hosted, and its `family=` segment is the canonical spelling. Prefer that spelling over §2's derived one. **Playwright path only** — this file is absent on the WebFetch fallback, in which case skip this bullet rather than treating the missing file as evidence of anything.
   - `{{primary_css_content}}` (already in memory, both paths) → an `@font-face` for this family whose `src: url(...)` points at a self-hosted or licensed-foundry origin. **Suspicion only — never a verdict.** Many Google-hosted faces are self-hosted; concluding here is the documented way to implement this wrongly.
   - On the **WebFetch fallback** path, expect E1 to resolve rarely: the content is LLM-summarised rather than raw CSS, so `@font-face` blocks and link hrefs are frequently absent. That pushes families to E2/E3, which is the correct outcome — it does **not** license a guess.
2. **E2** — the curated tables: §4.1 → `google-native`; §3 → `substituted`.
3. **E3** — only if E1 and E2 were both inconclusive: `WebFetch` probes over §2's candidate list (first two candidates per family) plus one `Inter` control for the run, per §1's verdict table. Never combine families in one request; ceiling is 5 requests per run.
4. **E4** — otherwise `unverified`.

For each family, store the record `font-availability-rules.md` §6.2 specifies:

- `{{font_availability_heading}}` / `{{font_availability_body}}` — `{ brand, loadable, param, status, evidence }`, with `status` one of `google-native | substituted | unverified`.

For a `substituted` family, rewrite that token's value to the three-name shape in §6.1 — `'<Brand>', '<Loadable>', <generic>`. **Do not change `prov`**: the family is still exactly as extracted, and availability is not a provenance question (`prov` has two values, and this is not one of them). Leave `google-native` and `unverified` values in the two-name shape.

**When §2 resolved a different spelling than the CSS declared, rewrite the token to the resolved name** (per §6.1) and record the raw alias in `evidence`. A site names faces after its own build — `GeistSans` is `Geist`, `sohne-var` is `Söhne` — and the raw form neither loads nor means anything elsewhere. This applies on the `google-native` path too, not only when substituting.

**Never unset a family because it is unavailable.** That is the §1-rejection outcome, on the other axis. Here the brand evidence is real and is preserved in first position no matter what the ladder returns.

### 5. Typography — Scale, Weights, Line-Heights

Apply `typography-scale-rules.md` (already loaded) Sections A–C to extract:

- 8 size tokens (`size_xs` … `size_4xl`)
- font weights (already covered by Section 4 — re-confirm against the heading/body-weight heuristics if those weren't found)
- 3 line-height tokens (`lh_tight`, `lh_base`, `lh_loose`)

Apply the coverage threshold from Section A: if fewer than 3 of the 8 size tokens can be confidently extracted, leave **all 8** unset and let step-05b infer the entire size scale per-run.

### 6. Effects — Shadows and Motion

Apply `shadow-motion-rules.md` (already loaded):

- Section E to extract `shadow_sm`, `shadow_md`, `shadow_lg`.
- Section F to extract `dur_fast`, `dur_base`, `dur_slow`, `easing_standard`.

All seven effects tokens are independent — fill what was found, leave the rest `null`.

### 7. Assemble In-Memory Extraction Results

Assemble the structured output per Section 7 format from `brand-extraction.md`:

- `{{extracted_colors}}` — 7 brand tokens (status colours not included)
- `{{extracted_typography}}` — 15 typography tokens
- `{{extracted_effects}}` — 7 effect tokens
- `{{extraction_status}} = "success"` (only if extraction completed without an early skip; otherwise the prior status is preserved)
- `{{font_rejected_heading}}` / `{{font_rejected_body}}` — set per Section 4 above, else `null`. Carry them through step-05b unchanged (they describe what the *URL* held, so a domain-inferred fill does not clear them) so step-07 §A can state why a family is `inferred-from-domain`.
- `{{font_availability_heading}}` / `{{font_availability_body}}` — set per Section 4b above for each family Section 4 selected, else `null` (an unset family has no availability question until step-05b fills it). Step-05b §G assembles them into `meta.brand_fonts`; step-07 §A discloses every `substituted` and `unverified` outcome.

Contrast validation runs **after** step-05b, not here — it must validate against the final token set, including any domain-inferred fills.

---

**Next:** Read fully and follow `step-05b-domain-inference.md`.
