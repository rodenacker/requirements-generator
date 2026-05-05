# Color Extraction Rules — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by step-05 (Brand Extraction). Contains CSS analysis strategy, color extraction rules, and color-to-token mapping heuristics. Ported from v3 b3-style-extractor with the status-color exclusion rule replaced by status-color *fallback to domain-inference* (status colours are populated by step-05b, not by this rules file).

---

## 0. Highest-signal source: `computed-tokens.json`

If `design-system/.workspace/computed-tokens.json` exists (Playwright path in step-04), prefer values from it over text-pattern matches against `{{primary_css_content}}`. The CSS string remains the fallback for tokens not present in the computed payload.

**Mapping from `computed-tokens.json` to colour tokens:**

| Token         | Preferred source from `computed-tokens.json`                                                                                                                          |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `primary`     | `customProperties` key matching `primary` / `brand` (case-insensitive substring). If multiple match, pick the one most frequently referenced in the rest of the CSS.    |
| `secondary`   | `customProperties` key matching `secondary`. Otherwise next most-frequent chromatic non-primary value across `sampleElements`.                                          |
| `accent`      | `customProperties` key matching `accent`. Otherwise the most saturated chromatic value not already assigned.                                                            |
| `background`  | `sampleElements.body.backgroundColor`.                                                                                                                                  |
| `surface`     | `customProperties` key matching `surface` / `card` / `panel`. Otherwise derive from `background` per §3.                                                                |
| `text`        | `sampleElements.body.color`.                                                                                                                                            |
| `text-muted`  | `customProperties` key matching `muted` / `subtle` / `secondary-text`. Otherwise derive from `text` per §3.                                                             |

Computed values arrive as `rgb(...)` / `rgba(...)` — run them through the existing rgb→hex normalization rule in §2. Custom-property values may already be hex; use as-is.

**If `computed-tokens.json` is absent (WebFetch fallback path):** skip this section entirely and use the legacy text-pattern logic in §1–§3 below against `{{primary_css_content}}` only. The synthetic `:root` block prepended to `{{primary_css_content}}` on the Playwright path is what makes the legacy heuristics still effective; without it (WebFetch path), the heuristics scan the raw fetched CSS as v3 did.

---

## 1. CSS Analysis Strategy

Analyze `{{primary_css_content}}` systematically by scanning these CSS constructs in order:

### CSS Custom Properties (Highest Signal)

Search for `--` prefixed declarations in `:root`, `html`, `body`, or `[data-theme]` selectors:
- Pattern: `--{name}: {value};`
- These are intentional design tokens and carry the strongest brand signal
- Collect all custom property names and their values

**Priority targets** (case-insensitive substring match on property name):
- `primary`, `brand`, `main`, `accent`, `secondary` → likely brand colors
- `background`, `bg`, `surface`, `card` → likely background/surface colors
- `text`, `foreground`, `body`, `heading` → likely text colors
- `font`, `family`, `typeface` → likely font declarations

### Class and Element Declarations

Scan standard CSS rules for color, background, and font properties:
- `color: {value}` — text colors
- `background-color: {value}` or `background: {value}` — background colors
- `font-family: {value}` — font declarations

**Context-aware selectors to prioritize:**
- `body`, `html`, `:root` → page-level defaults (background, text, font)
- `a`, `a:hover`, `.btn`, `.button`, `[class*="btn"]` → primary action color
- `h1`, `h2`, `h3`, `.heading`, `.title` → heading font
- `p`, `.text`, `.body`, `.content` → body font
- `.card`, `.panel`, `.surface`, `[class*="card"]` → surface colors
- `.nav`, `.navbar`, `.header`, `header` → may contain primary/secondary brand colors
- `.muted`, `.secondary`, `.subtle`, `.meta` → text-muted candidates

### Shorthand Properties

Expand shorthand declarations to extract individual values:
- `background: #hex url(...)` → extract the color portion
- `border: 1px solid #hex` → note the color but deprioritize (border colors are less brand-significant)
- `font: weight size/line-height family` → extract family and weight

---

## 2. Color Extraction

### Collect All Color Values

Scan `{{primary_css_content}}` for every color value. Normalize all formats to hex:

| Found Format | Conversion Rule |
|---|---|
| `#RRGGBB` | Use as-is |
| `#RGB` | Expand: `#ABC` → `#AABBCC` |
| `rgb(R, G, B)` | Convert: each channel 0-255 → 2-digit hex |
| `rgba(R, G, B, A)` | If alpha ≥ 0.9: convert RGB channels to hex (treat as opaque). If alpha < 0.9: **skip this color** — semi-transparent colors are overlays/shadows, not brand identity. |
| `hsl(H, S%, L%)` | Convert to RGB first, then to hex |
| `hsla(H, S%, L%, A)` | If alpha ≥ 0.9: convert HSL to RGB to hex. If alpha < 0.9: **skip** (overlay, not brand). |
| `oklch(...)`, `oklab(...)`, `lab(...)`, `lch(...)` | Convert to sRGB then hex (if conversion is uncertain, skip the value) |
| Named colors (`red`, `navy`, `white`, etc.) | Map to standard hex equivalents |

**Output constraint:** All extracted colors MUST be `#RRGGBB` format (6-digit hex, uppercase hash). Downstream consumers depend on the canonical hex format.

### Deduplicate and Rank

1. Deduplicate: merge identical hex values regardless of where they appeared
2. Count frequency: how many times each hex value appears across all declarations
3. Record context: which selectors/properties used each color (e.g., "used in .btn background, a:hover color")
4. Classify each color as:
   - **Chromatic** — has visible hue (not pure gray/white/black)
   - **Neutral** — grayscale: R=G=B, or near-equal channels (max channel difference ≤ 15)
   - **Near-white** — all channels ≥ 240
   - **Near-black** — all channels ≤ 25

---

## 3. Color-to-Token Mapping

Map the extracted and ranked colors to **7 brand tokens** (primary, secondary, accent, background, surface, text, text-muted). Use these heuristics in order:

### Primary Token Assignment

| Token | Assignment Heuristic |
|---|---|
| `primary` | Most frequent chromatic color appearing in action contexts (buttons, links, CTAs, nav highlights). If CSS custom properties contain `--primary` or `--brand`, use that value. |
| `secondary` | Second most frequent chromatic color distinct from primary (different hue family). Often found in secondary buttons, badges, or alternate nav items. If not found, derive from primary by shifting hue +120 degrees and desaturating 20%. |
| `accent` | Third chromatic color, or the most saturated/bright chromatic color not already assigned. Often used for highlights, notifications, or hover states. If not found, derive from primary by shifting hue -60 degrees. |
| `background` | Color assigned to `body` or `html` background. If not explicit, use the most common near-white color. If none found, default to `#ffffff`. |
| `surface` | Color used for card, panel, or modal backgrounds. Must differ from `background`. If not found, derive: if `background` is light, darken by ~3% (e.g., `#ffffff` → `#f8f9fa`); if dark, lighten by ~5%. |
| `text` | Color assigned to `body` or `html` `color` property. If not explicit, use the most common near-black color. If none found, default to `#1a1f2e`. |
| `text-muted` | Lighter text color found in secondary content, labels, placeholders, or `.muted`/`.secondary` classes. If not found, derive: blend `text` 30% toward `background`. |

### Hex-to-HSL Conversion (for Derivation)

When deriving colors via hue shifting, convert hex to HSL first:

1. Convert `#RRGGBB` to RGB (0–255), then normalize to 0.0–1.0
2. Find `max = max(R,G,B)`, `min = min(R,G,B)`, `delta = max - min`
3. **Lightness:** `L = (max + min) / 2`
4. **Saturation:** If `delta == 0`: `S = 0`. Else: `S = delta / (1 - |2L - 1|)`
5. **Hue:** If `delta == 0`: `H = 0`. Else if `max == R`: `H = 60 × ((G-B)/delta mod 6)`. If `max == G`: `H = 60 × ((B-R)/delta + 2)`. If `max == B`: `H = 60 × ((R-G)/delta + 4)`
6. After shifting H/S/L, convert back: HSL → RGB → hex `#RRGGBB`

### Derivation Fallbacks

When fewer than 7 distinct colors are available:

**1-2 chromatic colors found:**
- Assign the dominant one as `primary`
- Derive `secondary` by shifting primary's hue +120 degrees, keeping saturation
- Derive `accent` by shifting primary's hue -60 degrees, increasing saturation 15%

**Background/surface not found:**
- `background`: default `#ffffff` (light theme assumed unless most colors are light-on-dark)
- `surface`: derive from `background` as described above

**Text colors not found:**
- `text`: default `#1a1f2e`
- `text-muted`: derive from `text` blended 30% toward `background`

### Status-Colour Exclusion (Routed to step-05b)

Do NOT map any extracted colors to `success`, `warning`, `error`, or `info` tokens during this step. Even if the CSS contains green/yellow/red/blue colors that appear to be status indicators, leave the four status tokens unset here. Step-05b infers them per-run from the domain — that is the only path for status colours under the stand-alone constraint.
