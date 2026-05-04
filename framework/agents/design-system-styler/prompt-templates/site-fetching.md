# Site Fetching — Prompt Template

**Purpose:** This is a reusable instruction block for the two-pass site fetching strategy. The design-system-styler workflow loads this file and applies its instructions to fetch and identify the primary CSS source from a reference website.

**Usage:** Read this file using the Read tool. Apply the instructions within to perform the two-pass fetch on `{{reference_url}}`.

Ported from v3 b3-style-extractor verbatim.

---

## 1. Pass 1 — Homepage HTML Fetching

Fetch the homepage at the provided `{{reference_url}}` using the WebFetch tool.

**Request:**
- URL: `{{reference_url}}`
- No additional headers or authentication — only publicly accessible pages are supported

**On success:** Store the complete HTML response. Do NOT attempt to parse CSS at this stage — the goal is only to retrieve the HTML document.

**On failure:** Record the error and exit gracefully. Common failure modes:
- DNS resolution failure → site domain doesn't exist or is unreachable
- Connection timeout → site is slow or blocking automated requests
- HTTP 403/429 → site blocks non-browser requests
- HTTP 404 → homepage URL is incorrect
- HTTP 5xx → server-side error

---

## 2. HTML Parsing for CSS Sources

Scan the homepage HTML for all CSS sources. Identify two types:

### External Stylesheets

Search for `<link>` tags matching this pattern:
- Must have `rel="stylesheet"` (or `rel='stylesheet'`)
- Must have an `href` attribute with a non-empty value
- Ignore `<link>` tags with `rel="preload"`, `rel="prefetch"`, or `rel="preconnect"` (these are resource hints, not active stylesheets)
- Ignore `<link>` tags inside `<noscript>` blocks

Collect all matching `href` values in document order.

### Inline Styles

Search for `<style>` tags:
- Capture the full text content between `<style>` and `</style>`
- Ignore `<style>` tags with `type` attributes other than `text/css` (e.g., ignore `type="text/javascript"`)
- Ignore empty `<style>` blocks
- Record the character count of each inline block

---

## 3. CSS Source Selection Heuristics

From the collected CSS sources, select the **primary** stylesheet — the one most likely to contain the site's custom brand styles.

### Priority Order

1. **First non-framework external stylesheet** — The first `<link rel="stylesheet">` whose `href` does NOT match any of the exclusion patterns below
2. **Largest inline `<style>` block** — If no qualifying external stylesheets exist, use the inline block with the most characters
3. **Any inline `<style>`** — Last resort

### External Stylesheet Exclusion Patterns

These patterns identify third-party CSS frameworks and resets that are unlikely to contain brand-specific styling. Exclude from primary selection (but keep as fallback):

| Pattern in href | Likely Source |
|----------------|--------------|
| `normalize` | CSS Reset (Normalize.css) |
| `reset` | CSS Reset |
| `bootstrap` | Bootstrap framework |
| `tailwind` | Tailwind CSS |
| `bulma` | Bulma framework |
| `foundation` | Foundation framework |
| `materialize` | Materialize CSS |
| `font-awesome`, `fontawesome` | Icon fonts |
| `fonts.googleapis.com` | Google Fonts (font loading, not brand CSS) |
| `cdnjs.cloudflare.com` | Generic CDN library |
| `unpkg.com` | Generic CDN library |
| `jsdelivr.net` | Generic CDN library |

**Match rule:** Case-insensitive substring match against the full `href` value.

**Important:** Framework and CDN stylesheets are excluded entirely — they do not contain brand-specific styling. If ALL external stylesheets match exclusion patterns, fall through to inline `<style>` blocks or the "no CSS" exit condition.

---

## 4. URL Resolution Rules

External stylesheet `href` values may be relative. Resolve them against the **effective base URL**.

### Determine the Base URL

1. Check the HTML for a `<base href="...">` tag in the `<head>` section
2. If a `<base href>` exists with an absolute URL: use that as the base URL for resolving relative hrefs
3. If no `<base href>` exists: use the origin of `{{reference_url}}` as the base URL

**Origin** = scheme + host from `{{reference_url}}` (e.g., `https://example.com` from `https://example.com/about`).

### Resolution Table

| href Format | Resolution | Example (base: `https://example.com`) |
|-------------|-----------|---------|
| Absolute (`https://...`) | Use as-is | `https://example.com/css/main.css` |
| Protocol-relative (`//...`) | Prepend `https:` | `//cdn.example.com/style.css` → `https://cdn.example.com/style.css` |
| Root-relative (`/...`) | Prepend origin | `/css/main.css` → `https://example.com/css/main.css` |
| Relative (`css/...`) | Prepend base URL + `/` | `css/main.css` → `https://example.com/css/main.css` |

---

## 5. Content Size Limit

If the fetched CSS content exceeds approximately 100,000 characters (~100KB for ASCII CSS):

1. Keep only the first ~100KB of content
2. Log: "CSS content truncated from {original_size} to ~100KB for context management"
3. This truncation is acceptable — brand-defining styles (colors, fonts, custom properties) are typically declared early in a stylesheet

**Rationale:** The CSS content is consumed by an LLM for brand analysis. Keeping it under 100KB ensures the analysis fits within context limits without losing the brand-relevant portions.
