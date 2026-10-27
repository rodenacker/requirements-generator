# Cross-Mode Derivation — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by `framework/agents/design-system-styler/steps/step-05b-domain-inference.md` — by **§B.1** (scheme-aware gap-fill) and by **§F** (whole-set derivation of the opposite mode). States the **policy** for deriving one colour mode's token set from the other's, in **both** directions; `framework/tools/colour-tokens.cjs` implements the colour part of it and owns every number.

---

## 1. What this file is for

The pipeline extracts a brand palette from a URL once. **Whichever colour scheme that site ships is the scheme the styler extracts** — many sites are dark by default. The extracted scheme is therefore the **hue source**, and the *other* mode is derived from it by the rules below.

There is no privileged direction:

| Extracted scheme (hue source) | Derived mode | Rules used |
|---|---|---|
| `light` | `dark` | §3 policy, `derive` with `source_mode: light` |
| `dark` | `light` | §3 policy, `derive` with `source_mode: dark` |
| both (the site ships its own other scheme) | — | nothing derived: the other mode is extracted (step-05b §A-bis.1) |

**Input** = the final, contrast-validated hue-source token set. **Output** = the opposite mode's token set, derived from the *same brand hues*.

**A derived palette is never claimed as extracted.** See §6.

---

## 2. Shared tokens (19 of the 34) — copied verbatim

Only **11 colours + 3 shadows** get per-mode variants. `brand` is a colour but **mode-invariant** — identity colours do not re-light — so it is copied verbatim too (only its on-colour is measured per mode). The remaining 19 tokens are copied across modes **verbatim** — same value, same `prov`, same `source`:

- All 15 typography tokens (`heading_family`, `heading_weight`, `body_family`, `body_weight`, `size_xs`..`size_4xl`, `lh_tight`, `lh_base`, `lh_loose`).
- `transition_fast`, `transition_base`, `transition_slow`, `easing_standard`.

Type and motion are not mode-dependent. Do not re-derive, re-round, or re-source them; do not change their provenance markers.

---

## 3. Colour policy — implemented by `framework/tools/colour-tokens.cjs derive`

The derived mode's 12 colours, its on-colours and its contrast numbers come from **one helper call** (step-05b §F). This section states the policy the helper implements so a reader knows what to expect; the numbers (lightness targets, contrast targets, step size, chroma thresholds) live only in the helper. Never restate or re-tune them here or in a step.

The helper works in **OKLCH**, not HSL, and the guiding rule is **minimum change**: a derived colour is the same brand colour, re-lit only as far as it must be.

### 3.1 Brand and status fills — minimum change

- `primary`, `secondary`, `accent`, `success`, `warning`, `error`, `info` **keep their hue-source hue and chroma**. Only lightness moves, and only as far as the fill needs to meet its contrast target against the derived `surface`. A fill that already meets it is **copied unchanged** — that is correct, not a defect.
- Gamut mapping only ever lowers chroma; hue never rotates. A derived palette that reads as a *different brand* is a failure.

### 3.2 Neutral `primary` / `secondary` — the flip

- A low-chroma (neutral) `primary` or `secondary` does **not** do minimum change: that lands in a muddy mid-grey that looks disabled. It **flips to the far end** of the derived lightness ladder — a near-white `primary` with a dark label in dark mode, a charcoal `primary` in light mode. A flipped `secondary` sits just off the `surface` as a tonal button.

### 3.3 Neutrals — the ladder

- `background`, `surface`, `text`, `text_muted` are rebuilt on a fixed ladder tinted with the **brand hue**: dark → `background` < `surface` < `text_muted` < `text`; light → the reverse. Never pure black or pure white for `background` or `text`. `text_muted` is moved until it clears its target against **both** `background` and `surface`.

### 3.4 On-colours — measured, never assumed

- The label colour on every fill (`primary`, `secondary`, `accent`, `brand`, the four status colours) is **measured**: whichever of a brand-tinted near-black or near-white gives the higher WCAG contrast against that fill. Fills never bend to suit a fixed label colour. A label below its target is reported as an adjustment line, never fixed by moving the fill.

### 3.5 Shadows (not in the helper)

- `shadow_sm`, `shadow_md`, `shadow_lg` keep the hue-source geometry verbatim — same offsets, blur, spread. Light → dark: raise the black alpha ~1.5–2×. Dark → light: lower it by the same ratio. Shadows stay **black**; on dark surfaces separation comes primarily from the lighter `surface`.

---

## 4. Direction

Both directions use the same policy; the helper picks the far end from `source_mode`. Dark → light is not "§3 reversed by hand" — the minimum-change rule already restores a calm dark-theme brand colour only as far as the light `surface` requires, so no separate resaturation rule exists.

---

## 5. Constraints that hold in both directions

1. **Hue fidelity.** Derived brand and status colours keep the seed hue (gamut mapping reduces chroma only).
2. **Lightness ladder** as in §3.3.
3. **No pure black or pure white** for `background` or `text`.
4. **Contrast re-validation is the helper's.** The derived set gets its own four pair ratios, fill ratios and adjustment lines from the `derive` output; it never inherits the hue-source set's numbers.
5. **Reserved zone in both modes.** `primary`, `secondary` and `accent` never sit in the red → orange → amber zone in either mode. Minimum change keeps hue, so a role that was safe in the hue source stays safe in the derived mode.

---

## 6. Provenance of derived tokens

A derived token was **not** extracted, and the system has exactly **two** provenance markers — `extracted-from-url` and `inferred-from-domain`. Do not invent a third.

- **Marker:** `prov: "inferred-from-domain"`.
- **Source string:** `derived: <target-mode> variant of <source-mode> <token> (<source-hex>)`

Examples:

```
derived: dark variant of light background (#FFFFFF)
derived: light variant of dark primary (#7AA2F7)
derived: dark variant of light shadow_md (0 4px 6px rgba(0,0,0,0.10))
```

The source string preserves traceability back to the seed value, so a reader can always see which hue-source token a derived value came from. The **shared** tokens of §2 keep their original markers and source strings unchanged.

If the helper subsequently adjusts a derived value, it **retains** this marker and source — adjustment is a downstream correction, not a re-source.

---

## 7. Gap-fill contract (used by step-05b §B.1)

`prompt-templates/domain-inference.md` produces **light** values by construction. On a run whose extracted scheme is **dark**, step-05b §B.1 therefore converts any domain-inferred neutral with **one** `colour-tokens.cjs derive` call and keeps only the unset tokens from its output — the dark neutral ladder is defined in exactly one place, the helper.

Such a token's provenance is:

- **Marker:** `prov: "inferred-from-domain"` (unchanged — it *is* domain-inferred).
- **Source string:** `domain-inference ({{domain}}) → dark variant`

This is distinct from the §6 form, which is reserved for whole-set derivation of the opposite mode in §F. A token that was gap-filled during §B belongs to the hue-source set; it was never a cross-mode derivation.
