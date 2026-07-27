# WCAG AA Contrast Validation — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by `step-05b-domain-inference.md` — by **§A-bis** (scheme detection), by **§D** (validating the hue-source token set), and by **§F** (validating the derived opposite-mode set). Contains the scheme-detection rule, contrast ratio calculation rules, and the scheme-conditional adjustment strategy for accessibility compliance. Ported from v3 b3-style-extractor; the luminance math is verbatim, the adjustment strategy gained a dark-set branch when light/dark mode support was added.

---

## 6. WCAG AA Contrast Validation

After assigning all 7 brand color tokens (regardless of whether they came from the URL, from domain inference, or from cross-mode derivation), validate text/background contrast for accessibility compliance. This runs once per colour mode.

### Required Passing Pairs

All 4 pairs must achieve a minimum contrast ratio of **4.5:1** (WCAG AA for normal body text):

| Pair | Foreground Token | Background Token |
|---|---|---|
| 1 | `text` | `background` |
| 2 | `text` | `surface` |
| 3 | `text-muted` | `background` |
| 4 | `text-muted` | `surface` |

### Contrast Ratio Calculation

**Step 1 — Convert hex to linear RGB:**

For each channel (R, G, B) of a `#RRGGBB` color:
1. Parse the 2-digit hex to decimal (0–255)
2. Divide by 255 to get sRGB value (0.0–1.0)
3. Linearize:
   - If sRGB ≤ 0.04045: `linear = sRGB / 12.92`
   - If sRGB > 0.04045: `linear = ((sRGB + 0.055) / 1.055) ^ 2.4`

**Step 2 — Relative luminance:**

`L = 0.2126 * R_linear + 0.7152 * G_linear + 0.0722 * B_linear`

**Step 3 — Contrast ratio:**

`ratio = (L_lighter + 0.05) / (L_darker + 0.05)`

Where `L_lighter` is the higher luminance value and `L_darker` is the lower.

### Scheme Detection

Used by step-05b §A-bis to classify **which colour scheme was actually extracted**. The reference URL may ship a dark palette as readily as a light one; nothing in this pipeline assumes light.

Compute the relative luminance `L` of the `background` token (Steps 1–2 above), then:

| Condition | Scheme |
|---|---|
| `L >= 0.5` | `light` |
| `L < 0.5` | `dark` |

If no URL was given, or extraction did not reach its happy path, the scheme is **`light`** — the domain-inference contract is light-anchored by construction (it anchors `background` to `#FFFFFF`), so an all-inferred token set is a light set.

No new math: this reuses the luminance formula already defined above. Cite this subsection rather than restating it.

### Adjustment Strategy When Contrast Fails

The direction of adjustment depends on the **scheme of the token set being validated** — established by Scheme Detection above — not on which file is being written. A derived set is validated in its own scheme's direction.

If any pair's ratio is below 4.5:

**On a `light` set:**

1. **Darken the text color** — reduce each RGB channel proportionally until 4.5 is met:
   - Multiply each channel by a factor `f < 1.0`, decreasing `f` in steps of 0.05 until the ratio passes
   - Re-convert to hex after adjustment

2. **If darkening text doesn't reach 4.5** (text is already very dark):
   - **Lighten the background** — increase each RGB channel proportionally until 4.5 is met
   - Only lighten `background`/`surface`, never darken them (to preserve the intended light theme)

**On a `dark` set (the mirror):**

1. **Lighten the text color** — increase each RGB channel proportionally until 4.5 is met:
   - Multiply each channel by a factor `f > 1.0`, increasing `f` in steps of 0.05 until the ratio passes; **clamp each channel at 255**
   - Re-convert to hex after adjustment

2. **If lightening text doesn't reach 4.5** (text is already very light):
   - **Darken the background** — reduce each RGB channel proportionally until 4.5 is met
   - Only darken `background`/`surface`, **never lighten** them (to preserve the intended dark theme)

**Both schemes:**

3. **Log every adjustment**, prefixed with the scheme of the set:
   ```
   Contrast adjustment ({light|dark}): {token} adjusted from {original_hex} to {adjusted_hex}
   Reason: {foreground} on {background} ratio was {original_ratio}:1, needed 4.5:1
   New ratio: {new_ratio}:1
   ```

4. **Maximum adjustment iterations:** Stop after 20 adjustment steps per color. If 4.5:1 cannot be achieved within 20 steps, accept the best achieved ratio and log: `"Contrast warning: {pair} best ratio {ratio}:1 after max adjustments (target 4.5:1)"`

5. **After adjustment:** Re-validate ALL 4 pairs (adjusting one color may affect multiple pairs).

### Provenance Note

If a token's value is changed by this validation step, retain the original provenance marker (`extracted-from-url` or `inferred-from-domain`) — adjustment is a downstream correction, not a re-source. Append the adjustment record to the Contrast Validation table's `Adjustments` line in the artefact.

This applies equally to a **derived** token: an adjusted cross-mode value keeps both its `inferred-from-domain` marker and its `derived: <target> variant of <source> <token> (<source-hex>)` source string. The source records where the value *came from*, not what it currently is, so adjustment never rewrites it.

Each set gets its **own** adjustment log. A derived set does not inherit the hue-source set's ratios, statuses, or adjustments — it is validated independently, and the artefact for each mode reports that mode's own results.
