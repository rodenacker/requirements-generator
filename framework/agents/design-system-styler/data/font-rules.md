# Font Extraction Rules — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by step-05 (Brand Extraction). Contains font family extraction heuristics, and is the **canonical source of the non-brand-family (prohibited) set** in §1 — `step-05`, `step-06`, `step-07`, `prompt-templates/domain-inference.md`, and the agent's Self-validation all reference §1 by number and never restate the list. Ported from v3's `font-border-rules.md`; the border-radius section has been removed (border-radius is out of v1 scope per the design-system plan). Typography scale, weights, and line-heights are governed by `typography-scale-rules.md`.

---

## 0. Highest-signal source: `computed-tokens.json`

If `design-system/.workspace/computed-tokens.json` exists (Playwright path in step-04), prefer values from it over text-pattern matches against `{{primary_css_content}}`.

| Token             | Preferred source from `computed-tokens.json`                                                                                                  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `heading-family`  | `sampleElements.h1.fontFamily`. If null, try `h2` then `h3`.                                                                                  |
| `body-family`     | `sampleElements.body.fontFamily`.                                                                                                             |

The values arrive as full font-family chains, e.g. `"Inter", "Helvetica Neue", sans-serif`. Strip surrounding quotes from each name and pick the first family that is **not** a non-brand family per §1 below. In that example `Inter` is the brand font; `"Helvetica Neue"` is a system face serving as a fallback and is rejected, as is the `sans-serif` terminal.

If **every** family in the chain is non-brand (e.g. the body resolves to `Arial, Helvetica, sans-serif`, or to `system-ui, sans-serif`), leave the token unset — step-05b infers it per-run from the domain. Tag computed-source extractions `extracted-from-url` and record the source as `sampleElements.h1` / `sampleElements.body`.

**If `computed-tokens.json` is absent (WebFetch fallback path):** skip this section and use the legacy text-pattern logic in §4 below against `{{primary_css_content}}` only.

---

## 1. Non-brand families (prohibited)

**Canonical definition — this section is the single source of truth for the prohibited set.** §0 and §4 both reference it; neither restates the list.

A **non-brand family** is a font-family name that is not a deliberate brand typeface. A brand family token must never be one. There are four groups:

**(a) CSS generic keywords.** `sans-serif`, `serif`, `monospace`, `cursive`, `fantasy`, `system-ui`, `ui-sans-serif`, `ui-serif`, `ui-monospace`, `ui-rounded`, `math`, `emoji`, `fangsong`.

**(b) System faces and their metric clones.** `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Segoe UI Variable`, `SF Pro`, `San Francisco`, `Arial`, `Arial Nova`, `Helvetica`, `Helvetica Neue`, `Verdana`, `Tahoma`, `Trebuchet MS`, `Calibri`, `Candara`, `Georgia`, `Times`, `Times New Roman`, `Courier`, `Courier New`, `Lucida Grande`, `MS Sans Serif`, `Consolas`, `Menlo`, `Monaco`, `SFMono-Regular`, `Liberation Sans`, `Liberation Serif`, `Liberation Mono`, `Nimbus Sans`, `Arimo`, `Tinos`, `Cousine`, `DejaVu Sans`.

These are pre-installed OS faces (or metric-compatible substitutes for them). A site declaring one is stating a *fallback*, not a brand. `Arial` in particular is a **named** family, so the pre-2026 "skip generic families" rule let it through and shipped it as a client's brand font — that is the defect this section closes.

**(c) Position-dependent faces.** `Roboto`, `Noto Sans`, `Ubuntu`, `Cantarell`, `Oxygen`, `Droid Sans`.

These are genuine, licensable webfonts **and** Android/Linux system defaults, so position decides:

- **First named family in the chain → accepted.** A deliberate brand choice (`Roboto, sans-serif` is a real brand stack).
- **Anywhere after another named family → non-brand.** It is serving as a platform fallback (`Inter, Roboto, sans-serif` yields `Inter`; the `Roboto` is skipped, not selected).

**Position is measured against the original chain, not the surviving remainder.** So `Arial, Roboto, sans-serif` yields *nothing*: `Arial` is rejected under (b), and `Roboto` is still in second position, so it stays a fallback and is rejected too — the token is left unset. That is the correct outcome; a stack led by `Arial` is a system-fallback stack throughout, and promoting its second entry would smuggle the fallback in as a brand.

**(d) Unusable aliases.** Reject and keep scanning the chain:

- Any name beginning `__` or containing `_Fallback` — a `next/font` build hash (`__Inter_abc123`, `__Inter_Fallback_abc123`). It names a locally-scoped alias that exists only inside that site's build, so it is meaningless in our artefact even though it looks like a real family.
- Any `var(--…)` reference — an unresolved custom property, not a family name.
- Any single-character or purely-numeric name.

**Scope.** This set governs **brand family tokens in `/design-system`** — `heading-family` and `body-family`. It does not govern:

- The artefact's **documentation chrome**, which deliberately uses the platform UI font (`system-ui`) so the reviewer's eye separates document furniture from brand specimens. See the `DOC CHROME` comment in `framework/assets/template-design-system.html`.
- The **generic terminal** of an emitted stack, which is required — see *Font Output Rules* in §4.
- `/wireframe`, which uses system fonts by design (`framework/assets/design-systems/wireframe-ds.html`). Nothing here applies to it.

---

## 4. Font Extraction

### Find Font Declarations

Scan `{{primary_css_content}}` for `font-family` declarations (including within `font` shorthand).

### Heading Font

Search these selectors in priority order:
1. `:root`, `html`, or CSS custom properties containing `--font-heading`, `--font-display`, `--heading-font`
2. `h1`, `h2`, `h3` selectors
3. `.heading`, `.title`, `.display` class selectors

Extract the first family name from the `font-family` value that is **not** a non-brand family per §1:
- Scan the chain left to right, skipping every non-brand family (all four groups — do not restate the list, apply §1)
- The first surviving name is the branded heading font
- If the chain is exhausted without a survivor, leave the token unset (see *Font Output Rules* below)

Extract `font-weight` if declared alongside the heading selectors:
- Default heading weight: `600` if not explicitly found

### Body Font

Search these selectors in priority order:
1. `:root`, `html`, `body`, or CSS custom properties containing `--font-body`, `--font-base`, `--body-font`
2. `p`, `.text`, `.body`, `.content` selectors

Extract the first family name that is not a non-brand family, using the same §1 rules as heading.

Extract `font-weight`:
- Default body weight: `400` if not explicitly found

### Font Output Rules

- **Max 2 fonts:** Report heading font + body font. If the site uses the same font for both, report it once and reuse.
- **No brand font detected:** If every `font-family` value in the chain is a non-brand family per §1 (e.g. `Arial, Helvetica, sans-serif`, or only `sans-serif`, `system-ui`), leave the token unset. Step-05b infers it per-run from `{{domain}}`.
- **Never repair a non-brand family in place.** Do not substitute a "closest webfont", do not keep the name with a note, and do not downgrade it to a weaker marker. The only outcome for a rejected chain is *unset*, which routes to the existing step-05b gap-fill path — that path already proposes real webfonts only, so the correct value arrives for free.
- **Emitted stack shape:** a family token's value is exactly `'<Family>', <one generic>` — e.g. `'Manrope', sans-serif`. One named family, one generic terminal, nothing else. Never carry a captured chain's fallback tail into the token: the tail is where system faces live, and every emitted `font-family:` declaration in the artefact is substituted from these two token values.
  - The **generic terminal is required, not merely tolerated.** A bare family with no fallback lets the browser reach for its default *serif* when the face is absent — worse than the problem being solved. A generic keyword is not a named system face, so it is not a violation of §1.
  - Match the terminal to the family's classification: `sans-serif` for a sans family, `serif` for a serif family.
- **Quoted font names:** Strip surrounding quotes from font names while scanning (e.g., `"Inter"` → `Inter`). Re-quote the selected family with single quotes in the emitted stack.
- **Record a rejection:** when a chain is rejected because every candidate was non-brand, store the name that would have been selected under the pre-§1 rule — the first *named* family in the chain — as `{{font_rejected_heading}}` / `{{font_rejected_body}}`. Step-07 uses it to tell the consultant *why* the family is domain-inferred rather than extracted; without it the extracted-token count silently drops with no explanation.
- **Tag provenance:** When a font family is found via this rules file, tag it `extracted-from-url` and record the source selector (e.g. `h1, h2 font-family`) in the Source Context column. When the token is left unset (and later filled by step-05b), the agent tags it `inferred-from-domain`.
