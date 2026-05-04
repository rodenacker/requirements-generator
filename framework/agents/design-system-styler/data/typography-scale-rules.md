# Typography Scale Extraction Rules — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by step-05 (Brand Extraction). Defines extraction heuristics for the font-size scale, font-weight set, and line-height set from CSS content. Authored for v7b-test (no v3 equivalent). Tokens that cannot be confidently extracted fall through to step-05b for domain-defaults fill.

---

## A. Font-Size Scale (`text-xs` … `text-4xl`)

### Token Targets

| Token       | Default semantic role             | Typical value range |
| ----------- | --------------------------------- | ------------------- |
| `text-xs`   | meta / label / fine print         | 0.6875rem – 0.8rem  |
| `text-sm`   | secondary body                    | 0.8rem – 0.9rem     |
| `text-base` | primary body                      | 0.9rem – 1.0625rem  |
| `text-lg`   | emphasised body / lead paragraph  | 1.0625rem – 1.25rem |
| `text-xl`   | minor heading / section title     | 1.25rem – 1.5rem    |
| `text-2xl`  | page subtitle                     | 1.5rem – 1.875rem   |
| `text-3xl`  | page title                        | 1.875rem – 2.5rem   |
| `text-4xl`  | hero / display                    | 2.5rem – 3.5rem     |

### Extraction Strategy

1. **Custom properties first.** Search CSS custom properties for any of: `--text-xs`, `--text-sm`, `--text-base`, `--text-lg`, `--text-xl`, `--text-2xl`, `--text-3xl`, `--text-4xl`, `--font-size-*`, `--fs-*`, `--type-scale-*`. If a token name matches one of the eight targets exactly, use that value.
2. **Heading selectors.** If custom properties don't cover the scale, scan element selectors:
   - `h1` → candidate for `text-3xl` or `text-4xl` (use the larger of the two if both have heading sizes ≥ 2rem)
   - `h2` → candidate for `text-2xl` or `text-3xl`
   - `h3` → candidate for `text-xl` or `text-2xl`
   - `h4` → candidate for `text-lg` or `text-xl`
   - `h5`, `h6` → candidate for `text-base` or `text-lg`
3. **Body selectors.** `body`, `html`, `p` `font-size` → candidate for `text-base`. The most common body `font-size` value across the CSS is the strongest signal for `text-base`.
4. **Small-text selectors.** `small`, `.text-sm`, `.caption`, `.label`, `[class*="muted"]` → candidate for `text-sm` or `text-xs`.

### Normalisation

- All extracted values must be reported in `rem` (preferred) or `px`. If the CSS uses `em`, `%`, or unitless numbers, convert to `rem` assuming the standard 16px base when possible. If conversion is uncertain, leave the token unset.
- Round to 4 decimal places to avoid noisy values like `1.0624999rem`.
- Reject values outside the typical range for that token by more than 50% (e.g. a `body` rule with `font-size: 4rem` is almost certainly a one-off override, not the body scale).

### Coverage Threshold

- If **fewer than 3** of the 8 size tokens can be confidently extracted, leave **all 8** unset — partial scales are confusing. Step-05b will fill the entire scale from domain defaults.
- If **3 or more** can be extracted, fill what was found and let step-05b backfill the gaps.

---

## B. Font Weights

Extract `heading-weight` and `body-weight` only. The font-rules.md file already covers heading + body family extraction; weights extend that work.

| Token            | Heuristic                                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ |
| `heading-weight` | `font-weight` declared on `h1`, `h2`, `h3`, `.heading`, `.title`, or `--heading-weight` custom property. Default if absent: leave unset. |
| `body-weight`    | `font-weight` declared on `body`, `html`, `p`, or `--body-weight` custom property. Default if absent: leave unset.        |

### Normalisation

- Convert keyword weights to integers: `normal → 400`, `bold → 700`, `lighter → 300`, `bolder → 700`.
- Round non-standard weights (e.g. `450`) to the nearest 100 unless the CSS uses variable font axes — in which case keep the exact value.

---

## C. Line-Heights

Extract three line-height tokens.

| Token                | Heuristic                                                                            |
| -------------------- | ------------------------------------------------------------------------------------ |
| `line-height-tight`  | `line-height` declared on `h1`, `h2`, `h3`, `.heading`, or values ≤ 1.3 on display selectors. |
| `line-height-base`   | `line-height` declared on `body`, `html`, `p`, or the most common line-height across `<p>`-shaped selectors. Range 1.4 – 1.7. |
| `line-height-loose`  | `line-height` declared on `.lead`, `.prose`, `article p`, or values ≥ 1.7 on long-form selectors. |

### Normalisation

- Prefer unitless values (e.g. `1.5`). If the CSS uses `px` line-heights, convert to a unitless ratio against the body `font-size`. If conversion is uncertain, leave the token unset.
- All three tokens are independent — extracting one and missing the other two is fine; step-05b fills the missing two.

---

## D. Provenance Tagging

For every typography token written by this rules file:

- If the value was found in the CSS, tag the token `extracted-from-url` and record the source selector or custom-property name in the Source Context column.
- If the token was left unset and later filled by step-05b, the agent tags it `inferred-from-domain` and writes the source as `domain-default ({{domain}})` (curated) or `domain-inference ({{domain}})` (free-text).
