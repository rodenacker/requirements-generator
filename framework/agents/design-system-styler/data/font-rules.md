# Font Extraction Rules — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by step-05 (Brand Extraction). Contains font family extraction heuristics. Ported from v3's `font-border-rules.md`; the border-radius section has been removed (border-radius is out of v1 scope per the design-system plan). Typography scale, weights, and line-heights are governed by `typography-scale-rules.md`.

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
- **No custom font detected:** If all `font-family` values are generic families (e.g., only `sans-serif`, `system-ui`), leave the token unset. Step-05b fills it from `framework/assets/domain-defaults/{{domain}}.md`.
- **Quoted font names:** Strip surrounding quotes from font names (e.g., `"Inter"` → `Inter`).
- **Tag provenance:** When a font family is found via this rules file, tag it `extracted-from-url` and record the source selector (e.g. `h1, h2 font-family`) in the Source Context column. When the token is left unset (and later filled by step-05b), the agent tags it `inferred-from-domain`.
