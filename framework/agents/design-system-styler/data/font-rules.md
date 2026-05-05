# Font Extraction Rules — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by step-05 (Brand Extraction). Contains font family extraction heuristics. Ported from v3's `font-border-rules.md`; the border-radius section has been removed (border-radius is out of v1 scope per the design-system plan). Typography scale, weights, and line-heights are governed by `typography-scale-rules.md`.

---

## 0. Highest-signal source: `computed-tokens.json`

If `design-system/.workspace/computed-tokens.json` exists (Playwright path in step-04), prefer values from it over text-pattern matches against `{{primary_css_content}}`.

| Token             | Preferred source from `computed-tokens.json`                                                                                                  |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `heading-family`  | `sampleElements.h1.fontFamily`. If null, try `h2` then `h3`.                                                                                  |
| `body-family`     | `sampleElements.body.fontFamily`.                                                                                                             |

The values arrive as full font-family chains, e.g. `"Inter", "Helvetica Neue", sans-serif`. Strip surrounding quotes from each name and pick the first **non-generic** family per the existing rules below. Generic families to skip (existing list): `sans-serif`, `serif`, `monospace`, `cursive`, `fantasy`, `system-ui`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`.

If the first family is generic across the entire chain (e.g. the body resolves to `system-ui, sans-serif`), leave the token unset — step-05b infers it per-run from the domain. Tag computed-source extractions `extracted-from-url` and record the source as `sampleElements.h1` / `sampleElements.body`.

**If `computed-tokens.json` is absent (WebFetch fallback path):** skip this section and use the legacy text-pattern logic in §4 below against `{{primary_css_content}}` only.

---

## 4. Font Extraction

### Find Font Declarations

Scan `{{primary_css_content}}` for `font-family` declarations (including within `font` shorthand).

### Heading Font

Search these selectors in priority order:
1. `:root`, `html`, or CSS custom properties containing `--font-heading`, `--font-display`, `--heading-font`
2. `h1`, `h2`, `h3` selectors
3. `.heading`, `.title`, `.display` class selectors

Extract the **first non-generic** family name from the `font-family` value:
- Generic families to skip: `sans-serif`, `serif`, `monospace`, `cursive`, `fantasy`, `system-ui`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`
- The first non-generic name is the branded heading font

Extract `font-weight` if declared alongside the heading selectors:
- Default heading weight: `600` if not explicitly found

### Body Font

Search these selectors in priority order:
1. `:root`, `html`, `body`, or CSS custom properties containing `--font-body`, `--font-base`, `--body-font`
2. `p`, `.text`, `.body`, `.content` selectors

Extract the first non-generic family name using the same rules as heading.

Extract `font-weight`:
- Default body weight: `400` if not explicitly found

### Font Output Rules

- **Max 2 fonts:** Report heading font + body font. If the site uses the same font for both, report it once and reuse.
- **No custom font detected:** If all `font-family` values are generic families (e.g., only `sans-serif`, `system-ui`), leave the token unset. Step-05b infers it per-run from `{{domain}}`.
- **Quoted font names:** Strip surrounding quotes from font names (e.g., `"Inter"` → `Inter`).
- **Tag provenance:** When a font family is found via this rules file, tag it `extracted-from-url` and record the source selector (e.g. `h1, h2 font-family`) in the Source Context column. When the token is left unset (and later filled by step-05b), the agent tags it `inferred-from-domain`.
