# Shadow & Motion Extraction Rules — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by step-05 (Brand Extraction). Defines extraction heuristics for `box-shadow` elevation tokens and `transition-duration` / `transition-timing-function` tokens from CSS content. Authored for v7b-test (no v3 equivalent). Tokens that cannot be confidently extracted fall through to step-05b for domain-inference.

---

## 0. Highest-signal source: `computed-tokens.json`

If `design-system/.workspace/computed-tokens.json` exists (Playwright path in step-04), prefer values from it over text-pattern matches against `{{primary_css_content}}`.

**Shadows:**
- Prefer `customProperties` keys matching `shadow-sm` / `shadow-md` / `shadow-lg` / `elevation-1` / `elevation-2` / `elevation-3` for direct mapping.
- Otherwise, collect non-`none` `boxShadow` values from `sampleElements` (typically present on `button`, `input`, and occasionally `body`). Apply the existing classification bands in §E.3 (small / medium / large by y-offset and blur).
- The legacy strategy (§E.2 — collect every distinct value across the CSS string and rank by frequency) remains valid for shadows that don't appear on the sampled elements; treat the computed-source pass as a higher-priority *first* pass, then fall through to the CSS-string scan.

**Motion:**
- `transition-fast` / `transition-base` / `transition-slow`: prefer `customProperties` keys matching `duration-fast` / `duration-base` / `duration-slow` / `transition-fast` / `transition-slow`. Otherwise use `sampleElements.button.transitionDuration` (and `.link.transitionDuration` as a secondary source) — classify into the existing bands in §F.3 (fast ≤ 180ms, base 181–280ms, slow > 280ms).
- `easing-standard`: prefer `customProperties` keys matching `ease-standard` / `easing-standard` / `ease`. Otherwise use `sampleElements.button.transitionTimingFunction`. Apply the existing keyword-to-cubic-bezier translation in §F's Easing section.

Computed `transitionDuration` arrives as `0.2s` or `200ms`; normalize to `ms` per §F's existing rule. `transitionTimingFunction` arrives as either a `cubic-bezier(...)` literal or a keyword — apply the existing translation table.

Tag computed-source extractions `extracted-from-url`; record the source as `sampleElements.<element>.<property>` or the matched custom-property name.

**If `computed-tokens.json` is absent (WebFetch fallback path):** skip this section entirely and use the legacy text-pattern logic in §E–§F below against `{{primary_css_content}}` only.

---

## E. Shadows (`shadow-sm` / `shadow-md` / `shadow-lg`)

### Token Targets

| Token       | Semantic role            | Typical y-offset / blur                |
| ----------- | ------------------------ | -------------------------------------- |
| `shadow-sm` | hairline / subtle border | 0–2px y-offset, ≤ 4px blur              |
| `shadow-md` | card / panel             | 2–6px y-offset, 6–12px blur             |
| `shadow-lg` | floating / modal / popover | 6–20px y-offset, 12–32px blur          |

### Extraction Strategy

1. **Custom properties first.** Search for `--shadow-sm`, `--shadow-md`, `--shadow-lg`, `--elevation-1`, `--elevation-2`, `--elevation-3`. If found, map by name (e.g. `--elevation-1` → `shadow-sm`).
2. **Property declarations.** Collect every distinct `box-shadow` value across `{{primary_css_content}}`, deduplicated.
3. **Classify each `box-shadow` value by elevation.** Parse the value to extract y-offset and blur. Use these bands:
   - **Small:** y-offset ≤ 2px **and** blur ≤ 4px
   - **Medium:** 2px < y-offset ≤ 6px **or** 4px < blur ≤ 12px (and not classified as small)
   - **Large:** y-offset > 6px **or** blur > 12px
4. **Pick the most-frequent value in each band.**
   - `shadow-sm` ← most-frequent Small value
   - `shadow-md` ← most-frequent Medium value
   - `shadow-lg` ← most-frequent Large value

### Normalisation

- Preserve the original syntax (e.g. `0 4px 6px -1px rgba(0,0,0,0.1)`) — do not normalise to a different shorthand.
- Convert any RGB shadows to RGBA with explicit alpha (assume 1.0 if unspecified).
- Reject inset shadows (`inset 0 ...`) — they are interior fills, not elevation tokens.
- Reject shadows whose alpha is ≥ 0.4 — those are decorative/branded shadows, not elevation tokens.

### Coverage Threshold

- If **none** of the three bands have any matching shadows, leave all three tokens unset.
- If **at least one** band has a value, fill what was found; step-05b backfills the missing bands per-run from the domain inference (the same band that was found stays as `extracted-from-url`; the others are tagged `inferred-from-domain`).

---

## F. Motion (`transition-fast` / `transition-base` / `transition-slow` + `easing-standard`)

### Token Targets

| Token             | Semantic role              | Typical value          |
| ----------------- | -------------------------- | ---------------------- |
| `transition-fast` | hover / micro-feedback     | 100–180ms              |
| `transition-base` | standard state change      | 180–280ms              |
| `transition-slow` | deliberate / showcase      | 280–500ms              |
| `easing-standard` | default cubic-bezier curve | `cubic-bezier(...)` or named (e.g. `ease-in-out`) |

### Duration Extraction Strategy

1. **Custom properties first.** Search for `--duration-fast`, `--duration-base`, `--duration-slow`, `--transition-fast`, `--transition-slow`, `--ease-*`. Direct name match wins.
2. **Property declarations.** Collect every distinct `transition-duration` value (and the duration portion of any `transition` shorthand). Deduplicate.
3. **Classify by band:**
   - **Fast:** ≤ 180ms
   - **Base:** 181ms – 280ms
   - **Slow:** > 280ms
4. **Pick the most-frequent value in each band.** If a band has no values, leave the token unset.

### Easing Extraction Strategy

1. Look for `--ease-standard`, `--easing-standard`, `--ease`, `--ease-out`, etc.
2. Otherwise, find the most common `transition-timing-function` value across non-keyframe transitions. If the most common is a named keyword (`ease`, `ease-in`, `ease-out`, `ease-in-out`, `linear`), translate to `cubic-bezier` form for token consistency:
   - `ease` → `cubic-bezier(0.25, 0.1, 0.25, 1)`
   - `ease-in` → `cubic-bezier(0.42, 0, 1, 1)`
   - `ease-out` → `cubic-bezier(0, 0, 0.58, 1)`
   - `ease-in-out` → `cubic-bezier(0.42, 0, 0.58, 1)`
   - `linear` → keep as `linear`
3. If no easing is declared, leave the token unset.

### Normalisation

- Always report durations in `ms` (e.g. `200ms`, not `0.2s`).
- Always report easing as either a `cubic-bezier(...)` value or `linear`. No keywords.

### Coverage Threshold

- All four motion tokens are independent. Fill what was found; step-05b fills the rest.

---

## G. Provenance Tagging

For every effect token written by this rules file:

- If the value was found in the CSS, tag the token `extracted-from-url` and record the source selector or custom-property name in the Source Context column.
- If the token was left unset and later filled by step-05b, the agent tags it `inferred-from-domain`.
