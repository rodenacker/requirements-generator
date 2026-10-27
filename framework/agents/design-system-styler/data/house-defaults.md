# House Defaults — Design-System-Styler Data File

**Role:** the single place the non-colour house values live. Read by step-05b §A and applied in its §B fill loop. Every value here is `prov: system-derived` with `source: "house default"` (fonts: `"interim font fallback"`).

**Scope:** internal, CRUD-heavy data-management tools; never varies by client or industry. These tokens are **never extracted** from a brand reference, even when the reference declares them: a marketing site's sizes and motion are not an internal tool's.

**Baseline only:** `/prototype` adapts the type ramp by D3 (`framework/assets/prototypes/visual-craft-standard.md` §6); these values are the baseline it chooses steps from.

Colours are not here: the status set (`HOUSE_STATUS`) and the neutral ladder live in `framework/tools/colour-tokens.cjs`.

---

## 1. Type scale

| Token | Value |
|---|---|
| `size_xs` | `0.6875rem` |
| `size_sm` | `0.8125rem` |
| `size_base` | `0.9375rem` |
| `size_lg` | `1rem` |
| `size_xl` | `1.125rem` |
| `size_2xl` | `1.375rem` |
| `size_3xl` | `1.625rem` |
| `size_4xl` | `2rem` |
| `lh_tight` | `1.2` |
| `lh_base` | `1.45` |
| `lh_loose` | `1.65` |

Mode-invariant. `source: "house default"`.

## 2. Shadows

| Token | Value |
|---|---|
| `shadow_sm` | `0 1px 2px 0 rgba(<text-rgb>, 0.05)` |
| `shadow_md` | `0 4px 6px -1px rgba(<text-rgb>, 0.08)` |
| `shadow_lg` | `0 10px 15px -3px rgba(<text-rgb>, 0.10)` |

- **Light hue-source set:** `<text-rgb>` = the set's `text` colour as `r, g, b` (subtle but visible, tinted like the text).
- **Dark hue-source set:** today's dark-shadow treatment, `cross-mode-derivation-rules.md` §3.5: the geometry above, shadows black (`<text-rgb>` = `0, 0, 0`), alpha raised as §3.5 says. Do not copy its numbers here.
- A derived other mode takes its shadows from step-05b §F (the same §3.5 rule).

`source: "house default"`.

## 3. Motion

| Token | Value |
|---|---|
| `transition_fast` | `100ms` |
| `transition_base` | `160ms` |
| `transition_slow` | `240ms` |
| `easing_standard` | `cubic-bezier(0.4, 0, 0.2, 1)` |

Mode-invariant. `source: "house default"`.

## 4. Interim font fallback

Used only for a family (or weight) no reference supplied:

| Token | Value |
|---|---|
| `heading_family` | `'Inter', sans-serif` |
| `body_family` | `'Inter', sans-serif` |
| `heading_weight` | `600` |
| `body_weight` | `400` |

Availability record for a fallback family: `{ brand: "Inter", loadable: "Inter", param: "Inter", status: "google-native", delivery: <set by step-05b §G>, evidence: "interim font fallback (verified Google-hosted)" }`. `source: "interim font fallback"`.

Replaced by the fonts topic.
