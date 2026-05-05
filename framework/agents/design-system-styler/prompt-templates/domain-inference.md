# Domain Inference — Prompt Template

**Purpose:** Reusable instruction block for inferring a coherent design-system token set from the consultant's free-text domain string. The design-system-styler workflow loads this file in step-05b and applies its instructions to fill every token still unset after step-05 (or the entire token set, when step-05 was skipped).

**Usage:** Read this file using the Read tool. Apply the instructions to `{{domain}}` (the consultant's typed domain, lowercased and trimmed). Produce the same output shape as `brand-extraction.md`'s §7 (so step-06 can serialize it without branching), with every value tagged Source Context = `domain-inference ({{domain}})` and Provenance = `inferred-from-domain`.

---

## 1. Inference Contract

The inference must produce **33 tokens**, by name, matching `framework/assets/template-design-system.md`:

- **11 colours:** `primary`, `secondary`, `accent`, `background`, `surface`, `text`, `text-muted`, `success`, `warning`, `error`, `info`
- **15 typography tokens:** `heading-family`, `heading-weight`, `body-family`, `body-weight`, `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`, `text-4xl`, `line-height-tight`, `line-height-base`, `line-height-loose`
- **7 effects tokens:** `shadow-sm`, `shadow-md`, `shadow-lg`, `transition-fast`, `transition-base`, `transition-slow`, `easing-standard`

Every token must have a non-null value. No invention of new tokens. No omission of any listed token.

---

## 2. Step A — Voice Synthesis

Before deriving any token, synthesise a one-line **Voice statement** from `{{domain}}`. The voice anchors the rest of the inference; tokens flow from it.

The Voice statement has two parts:

1. **Three adjectives** capturing the brand's stylistic intent. Pick adjectives that describe how the product should *feel*, not what it does.
2. **One sentence** elaborating the visual translation: which colour family leads, how prominent shadows are, how dense the type scale is, how fast motion is.

**Examples** (match this shape):

| `{{domain}}`              | Voice                                                                                                                                                          |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `retail-banking`          | trustworthy, conservative, calm. Blue-dominant palette, generous spacing, classic-modern sans for body and a slightly heavier weight for headings.             |
| `ecommerce`               | confident, action-forward, conversion-oriented. High-contrast primary action colour, white-heavy backgrounds, strong shadows for product cards, snappy motion. |
| `government-services`     | plain, accessible, high-contrast. Single trustworthy primary, no decorative shadows, conservative motion.                                                      |
| `internal-tooling`        | dense, functional, work-focused. Neutral grayscale with a single utility-blue accent. Tight line-heights, narrow type scale, fast transitions.                 |
| `healthcare-booking`      | calm, clean, clinical. Cool blue/green palette with high contrast for accessibility-conscious users, generous line-heights, soft shadows.                      |
| `pet-grooming-marketplace`| warm, approachable, image-rich. Soft saturated primary against creamy off-whites, rounded type with friendly weights, gentle shadows.                          |
| `legal services SaaS`     | precise, authoritative, restrained. Deep navy primary, monochromatic neutrals, classical serif-leaning sans, small shadows, deliberate motion.                 |

Free-text domains that don't map to a known industry should still produce a coherent voice — reason from the words in `{{domain}}` directly (e.g. "luxury", "kids", "B2B", "marketplace", "DAW", "clinical") to adjective and palette choices. Preserve `{{domain}}` exactly as the consultant typed it (lowercased) for traceability; the Voice is your interpretation of it.

Hold the synthesised Voice in memory. Every subsequent rule references it.

---

## 3. Step B — Colour Derivation

Derive the 11 colour tokens. Hex values, uppercase, 6-digit `#RRGGBB`.

### B.1 Brand colours (primary, secondary, accent)

- **`primary`** — the dominant brand colour, derived from the Voice. The first adjective usually drives the hue family:
  - "trustworthy" / "calm" / "clinical" / "professional" → blues, teals
  - "confident" / "action-forward" / "energetic" / "alert" → reds, oranges, hot pinks
  - "modern" / "tech" / "optimistic" → indigo, violet, cyan
  - "warm" / "friendly" / "approachable" → warm oranges, coral, soft red
  - "luxury" / "premium" → deep navy, gold, rich greens, off-blacks
  - "natural" / "organic" / "wellness" → forest greens, sage, terracotta
- **`secondary`** — a supporting tone. Either a darker neutral (slate/charcoal in the same temperature as primary) or a desaturated cousin of the primary hue. Should not compete with primary at glance.
- **`accent`** — a contrast partner for occasional emphasis. Pick a hue 90°–180° away from primary on the wheel, or a warm complement to a cool primary (gold/amber against navy/teal).

### B.2 Neutrals (background, surface, text, text-muted)

- **`background`** — almost always `#FFFFFF`. Only deviate (very-near-white tints, e.g. `#FAFAFA`, `#FDF8F0`) when the Voice explicitly signals warmth, paper, or off-white minimalism.
- **`surface`** — a near-white tinted toward the primary's temperature. Cool primaries → cool surface (`#F1F5F9`, `#F8FAFC`). Warm primaries → warm surface (`#FAF7F2`, `#FFFAF5`). Use ~5–8% lightness step from background.
- **`text`** — near-black with a tint matching surface temperature. Conventional values: `#0F172A`, `#111827`, `#1A1F2E`. Avoid pure `#000000` unless the Voice is explicitly austere/government.
- **`text-muted`** — mid-grey, same temperature family as `text`. Range `#475569`–`#6B7280`. Must validate ≥4.5:1 against both background and surface (contrast validation runs in §D after all tokens are filled).

### B.3 Status colours (success, warning, error, info)

Status colours follow conventional semantics, tuned to the Voice's saturation and warmth:

- **`success`** — green family. Conservative voices (banking, government) → deeper greens (`#15803D`, `#1E8449`). Energetic voices → brighter greens (`#16A34A`, `#10B981`).
- **`warning`** — amber/yellow family. `#F59E0B` for vivid voices, `#B45309` / `#CA8A04` / `#B7950B` for restrained voices. Avoid pure yellow (poor contrast on white).
- **`error`** — red family. `#DC2626` / `#EF4444` for assertive voices, `#B91C1C` / `#C0392B` for restrained voices.
- **`info`** — blue family. Often equal-or-darker than `primary` if `primary` is also blue, otherwise a clear blue (`#2563EB`, `#3B82F6`, `#0EA5E9`, `#0369A1`).

The four status colours are **always** filled here regardless of any URL extraction, with Provenance `inferred-from-domain`.

### B.4 Coherence rules (colours)

- Temperature consistency — surface, text, and text-muted share the primary's temperature family (cool primary → cool neutrals).
- Contrast headroom — `text` on `background` should clear ~7:1; `text-muted` on `surface` must clear 4.5:1. The contrast loop in §D auto-adjusts text/text-muted if a pair fails; pick conservative neutrals up front to minimise adjustments.
- No clashing accent — `accent` must not collide with any status colour at glance (e.g. don't pick a green accent if it sits next to `success`).

---

## 4. Step C — Typography Derivation

### C.1 Families and weights

- **`heading-family`** — pick from common, broadly-licensed sans-serifs unless the Voice signals otherwise. Defaults: `Inter`, `Manrope`, `Poppins`, `Source Sans Pro`, `DM Sans`. Use a serif (`Source Serif 4`, `Playfair Display`) only when the Voice is explicitly editorial, legal, or luxury.
- **`heading-weight`** — `600` (medium-bold) for clean/clinical/professional voices; `700` (bold) for confident/energetic/conversion voices.
- **`body-family`** — `Inter` is the safe default. Match `heading-family` (single-family stack) for dense/utilitarian voices (internal-tooling, government); diverge (different family for body) only when the Voice signals editorial contrast.
- **`body-weight`** — always `400` unless the Voice signals otherwise (rare).

### C.2 Size scale

Use rem values. Pick from one of three scale shapes based on Voice density:

- **Tight scale** (dense / utilitarian / internal): `0.6875rem`, `0.8125rem`, `0.9375rem`, `1rem`, `1.125rem`, `1.375rem`, `1.625rem`, `2rem`.
- **Standard scale** (default for most voices): `0.75rem`, `0.875rem`, `1rem`, `1.125rem`, `1.25rem`, `1.5rem`, `1.875rem`, `2.25rem`.
- **Expressive scale** (confident / editorial / energetic): `0.75rem`, `0.875rem`, `1rem`, `1.125rem`, `1.375rem`, `1.75rem`, `2.25rem`, `3rem`.

### C.3 Line heights

- **Tight line-height range** (dense / utilitarian): `1.2`, `1.45`, `1.65`.
- **Standard line-height range** (default): `1.25`, `1.5`, `1.75`.
- **Generous line-height range** (long-form / accessibility-priority / education / healthcare / government): `1.3`, `1.6`, `1.8`.

### C.4 Coherence rules (typography)

- Body-weight `400` and body-size `1rem` are near-universal; deviate only with explicit Voice justification.
- A heavier `heading-weight` (700) pairs with the expressive scale; a moderate weight (600) pairs with standard or tight.
- Line-height range matches scale density: tight scale → tight line-heights; expressive scale → standard or generous line-heights for breathing room.

---

## 5. Step D — Effects Derivation

### D.1 Shadows

Three elevations: `shadow-sm`, `shadow-md`, `shadow-lg`. Use the format `0 {y}px {blur}px {spread} rgba({r}, {g}, {b}, {alpha})`.

- **Subtle** (government, austere voices): low blur, low alpha. Example progression: `0 1px 2px 0 rgba(17, 24, 39, 0.05)` → `0 2px 4px 0 rgba(17, 24, 39, 0.08)` → `0 4px 8px 0 rgba(17, 24, 39, 0.10)`.
- **Standard** (most voices): medium blur, medium alpha. Example: `0 1px 2px 0 rgba(15, 23, 42, 0.05)` → `0 4px 6px -1px rgba(15, 23, 42, 0.08)` → `0 10px 15px -3px rgba(15, 23, 42, 0.10)`.
- **Strong** (confident, conversion, premium): higher blur, higher alpha, occasionally tinted with the primary hue. Example: `0 2px 4px 0 rgba(17, 24, 39, 0.06)` → `0 6px 10px -2px rgba(17, 24, 39, 0.10)` → `0 14px 24px -6px rgba(17, 24, 39, 0.14)`.

The shadow's `rgb` should match the `text` colour's RGB family (cool text → cool shadow). For premium/tech voices, shadow-md and shadow-lg may use the primary's RGB tint at 0.15–0.20 alpha for a coloured-glow effect.

### D.2 Motion

Three durations + one easing.

- **Fast voices** (dense / utilitarian / energetic): `transition-fast: 100ms`, `transition-base: 150–180ms`, `transition-slow: 220–280ms`.
- **Standard voices** (most): `transition-fast: 150–180ms`, `transition-base: 200–240ms`, `transition-slow: 300–360ms`.
- **Considered voices** (premium / editorial / fintech-modern): `transition-fast: 180ms`, `transition-base: 260ms`, `transition-slow: 400ms`.

`easing-standard` defaults to `cubic-bezier(0.4, 0, 0.2, 1)` (Material). Use distinctive easings only for explicit Voice signals — `cubic-bezier(0.16, 1, 0.3, 1)` (overshoot, modern), `cubic-bezier(0.32, 0.72, 0, 1)` (snappy, conversion).

### D.3 Coherence rules (effects)

- Shadow alpha must match background/text contrast. White background + dark text → cool low-alpha shadow. Off-white background → slightly warmer shadow.
- Motion speed should match information density. Dense screens want fast transitions (so the user moves quickly); marketing-style screens want considered transitions.

---

## 6. Output Format

Produce the same structure as `brand-extraction.md`'s §7 output, with every token populated. Every token's `source` field is `domain-inference ({{domain}})`; never leave a `source` empty.

```yaml
extraction_status: "{{preserved_from_step_05}}"   # do not overwrite — step-05b only fills tokens

extracted_colors:
  primary:     { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }
  secondary:   { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }
  accent:      { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }
  background:  { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }
  surface:     { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }
  text:        { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }
  text-muted:  { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }
  success:     { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }
  warning:     { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }
  error:       { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }
  info:        { hex: "#RRGGBB", source: "domain-inference ({{domain}})" }

extracted_typography:
  heading_family: { value: "Font Name", source: "domain-inference ({{domain}})" }
  heading_weight: { value: 600,         source: "domain-inference ({{domain}})" }
  body_family:    { value: "Font Name", source: "domain-inference ({{domain}})" }
  body_weight:    { value: 400,         source: "domain-inference ({{domain}})" }
  size_xs:        { value: "0.75rem",   source: "domain-inference ({{domain}})" }
  # ...through size_4xl, lh_tight, lh_base, lh_loose
extracted_effects:
  shadow_sm:       { value: "0 1px 2px 0 rgba(...)", source: "domain-inference ({{domain}})" }
  # ...through shadow_lg, dur_fast, dur_base, dur_slow, easing_standard
```

Tokens that step-05 already filled (provenance `extracted-from-url`) are **not** overwritten. Their existing `source` (a CSS selector or property) is preserved untouched. This template only populates rows whose value was `null` after step-05, plus the four status colours which are always domain-filled.

---

## 7. Hold Voice in the Diagnostic Summary

When step-07 prints the styler diagnostic, include the synthesised Voice as a single line under the extraction summary:

```
Voice: <three-adjective sentence + visual elaboration>
```

This makes the inference legible to the consultant — they can see *why* the tokens look the way they do without reading the file.

---

## 8. Anti-Patterns

- Do not invent token names not in §1. The 33-token contract is closed.
- Do not produce a value without a Voice statement first. Tokens that don't trace back to the Voice are incoherent.
- Do not mix temperatures (warm primary + cool surface, or vice versa) without a deliberate Voice reason.
- Do not deviate from `body-weight: 400` or `background: #FFFFFF` casually. Both are near-universal anchors.
- Do not produce identical token sets for different `{{domain}}` strings. The Voice must register in the values; reuse across domains is a sign of failed inference.
- Do not skip status colours when step-05 succeeded. Status is always domain-filled regardless of URL outcome.
