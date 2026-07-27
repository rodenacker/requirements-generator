# Cross-Mode Derivation — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by `framework/agents/design-system-styler/steps/step-05b-domain-inference.md` — by **§B** (per-token scheme-aware gap-fill) and by **§F** (whole-set derivation of the opposite mode). Contains the rules for deriving one colour mode's token set from the other's, in **both** directions.

---

## 1. What this file is for

The pipeline extracts a brand palette from a URL once. **Whichever colour scheme that site ships is the scheme the styler extracts** — many sites are dark by default. The extracted scheme is therefore the **hue source**, and the *other* mode is derived from it by the rules below.

There is no privileged direction:

| Extracted scheme (hue source) | Derived mode | Rules used |
|---|---|---|
| `light` | `dark` | §3 Light → dark |
| `dark` | `light` | §4 Dark → light |
| none (no URL / failed fetch) — domain inference is light-anchored | `dark`, if requested | §3 Light → dark |

**Input** = the final, contrast-validated hue-source token set. **Output** = the opposite mode's token set, derived from the *same brand hues*.

**A derived palette is never claimed as extracted.** See §6.

---

## 2. Shared tokens (19 of the 33) — copied verbatim

Only **11 colours + 3 shadows** get per-mode variants. The remaining 19 tokens are copied across modes **verbatim** — same value, same `prov`, same `source`:

- All 15 typography tokens (`heading_family`, `heading_weight`, `body_family`, `body_weight`, `size_xs`..`size_4xl`, `lh_tight`, `lh_base`, `lh_loose`).
- `transition_fast`, `transition_base`, `transition_slow`, `easing_standard`.

Type and motion are not mode-dependent. Do not re-derive, re-round, or re-source them; do not change their provenance markers.

---

## 3. Light → dark

Work in HSL terms and convert back to `#RRGGBB`. Preserve brand hue throughout — this is a *re-lighting* of the same brand, not a new palette.

### 3.1 Neutrals

- **`background`** — near-black, tinted with the **primary's hue**: saturation ~10–15%, lightness ~8–12%. **Never `#000000`** — a pure-black background loses the brand tint and makes every shadow invisible.
- **`surface`** — the same hue as `background`, ~6–10 lightness points **above** it. In dark palettes elevation is carried by a *lighter* surface, not by a heavier shadow.
- **`text`** — near-white, brand-tinted (lightness ~90–95). **Never `#FFFFFF`** — pure white on near-black is harsh and drops the brand tint.
- **`text_muted`** — lightness ~62–72. Must clear 4.5:1 against **both** the dark `background` and the dark `surface`; §5 re-validates.

### 3.2 Brand colours

- **`primary`, `secondary`, `accent`** — preserve hue (**±8° maximum**), raise lightness ~+10–20, and desaturate moderately. Saturated mid-lightness fills that read well on white are usually too heavy on near-black.

### 3.3 Status colours

- **`success`, `warning`, `error`, `info`** — keep their semantic hues (green / amber / red / blue). Brighten for legibility on the dark `background` **and** the dark `surface`.
- **Ambers are the trap:** darkening or over-desaturating a warning amber muddies it to brown. Raise lightness and hold saturation.

### 3.4 Shadows

`shadow_sm`, `shadow_md`, `shadow_lg` keep the **light mode's geometry verbatim** — same offsets, blur, and spread. Raise the black alpha by ~1.5–2×.

Shadows stay **black**. Do not switch them to white: on dark surfaces the visible separation comes primarily from the lighter `surface` value (§3.1), with the shadow as a secondary cue. A raised-alpha black shadow on a dark card reads subtly by design.

---

## 4. Dark → light

The mirror of §3, and **not** merely §3's numbers reversed — one asymmetry matters (§4.2).

### 4.1 Neutrals

- **`background`** — near-white, optionally carrying a very slight primary-hue tint: lightness ~97–100.
- **`surface`** — 2–5 lightness points **below** `background`; or equal to it, with separation carried by a border. (Light palettes commonly invert the dark convention: the raised surface is the *whiter* one, so a card on a tinted page background may sit at pure white.)
- **`text`** — near-black, brand-tinted (lightness ~10–18). **Never `#000000`**.
- **`text_muted`** — lightness ~35–45. Must clear 4.5:1 against **both** the light `background` and the light `surface`; §5 re-validates.

### 4.2 Brand colours

- **`primary`, `secondary`, `accent`** — preserve hue (**±8° maximum**), **lower** lightness ~10–20, and **resaturate moderately**.
- **This is the asymmetry.** Dark-theme brand colours are frequently *desaturated and lightened* by their designers so they sit calmly on a dark background. Simply darkening such a colour yields a muddy, washed-out fill on white. Saturation must be **restored**, not merely preserved.

### 4.3 Status colours

- **`success`, `warning`, `error`, `info`** — keep their semantic hues; darken for legibility on the light `background` **and** the light `surface`.
- The amber trap applies in reverse: a bright dark-mode amber darkened without holding saturation becomes brown.

### 4.4 Shadows

Keep the dark mode's geometry verbatim; **lower** the black alpha by the same ~1.5–2× ratio in reverse. Light-mode elevation is carried by the shadow rather than by the surface step, so the shadow does real work here.

---

## 5. Constraints that hold in both directions

1. **Hue fidelity.** Every derived brand colour stays within ±8° of its seed hue. A derived palette that reads as a *different brand* is a failure, however pleasant it looks.
2. **Lightness ladder.** The derived set keeps a consistent, monotonic ladder — dark: `background` < `surface` < `text_muted` < `text`; light: the reverse.
3. **No pure black or pure white** for `background` or `text` in either direction.
4. **No unshifted saturated fills.** A brand colour copied across modes without a lightness/saturation shift is the single most common derivation defect.
5. **Contrast re-validation is mandatory.** Run `framework/agents/design-system-styler/data/contrast-validation.md` over the derived set, using the **derived** scheme's adjustment direction. The derived set gets its own four pair ratios and its own adjustment log; it does not inherit the hue-source set's results.
6. **Fill legibility (guidance, not a gate).** `component-catalogue.md` uses `colours.surface` as the on-fill label colour for primary / secondary / destructive buttons and all four badges. Derived brand and status fills must therefore stay far enough in lightness from the derived `surface` that the label reads against them — in a dark palette that means keeping fills light enough for near-black label text. This is a derivation constraint to honour while choosing values; it is **not** added to the four-pair validation gate.

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

If contrast validation (§5.5) subsequently adjusts a derived value, it **retains** this marker and source — adjustment is a downstream correction, not a re-source.

---

## 7. Gap-fill helper contract (used by step-05b §B)

`prompt-templates/domain-inference.md` produces **light** values by construction — it anchors `background` to `#FFFFFF`. So on a run whose extracted scheme is **dark**, filling an unset token straight from domain inference would inject a near-white neutral into a dark palette.

Step-05b §B therefore calls **§3 (Light → dark) one token at a time** as a helper: the value is inferred as a light value first, then converted here before being stored. This keeps dark neutral targets defined in exactly one place — this file — rather than duplicating them into the inference contract.

Such a token's provenance is:

- **Marker:** `prov: "inferred-from-domain"` (unchanged — it *is* domain-inferred).
- **Source string:** `domain-inference ({{domain}}) → dark variant`

This is distinct from the §6 form, which is reserved for whole-set derivation of the opposite mode in §F. A token that was gap-filled during §B belongs to the hue-source set; it was never a cross-mode derivation.
