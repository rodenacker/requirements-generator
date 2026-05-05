# WCAG AA Contrast Validation — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by step-05 (Brand Extraction). Contains contrast ratio calculation rules and adjustment strategy for accessibility compliance. Ported verbatim from v3 b3-style-extractor.

---

## 6. WCAG AA Contrast Validation

After assigning all 7 brand color tokens (regardless of whether they came from the URL or from domain inference), validate text/background contrast for accessibility compliance.

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

### Adjustment Strategy When Contrast Fails

If any pair's ratio is below 4.5:

1. **Darken the text color** — reduce each RGB channel proportionally until 4.5 is met:
   - Multiply each channel by a factor `f < 1.0`, decreasing `f` in steps of 0.05 until the ratio passes
   - Re-convert to hex after adjustment

2. **If darkening text doesn't reach 4.5** (text is already very dark):
   - **Lighten the background** — increase each RGB channel proportionally until 4.5 is met
   - Only lighten `background`/`surface`, never darken them (to preserve the intended light/dark theme)

3. **Log every adjustment:**
   ```
   Contrast adjustment: {token} adjusted from {original_hex} to {adjusted_hex}
   Reason: {foreground} on {background} ratio was {original_ratio}:1, needed 4.5:1
   New ratio: {new_ratio}:1
   ```

4. **Maximum adjustment iterations:** Stop after 20 adjustment steps per color. If 4.5:1 cannot be achieved within 20 steps, accept the best achieved ratio and log: `"Contrast warning: {pair} best ratio {ratio}:1 after max adjustments (target 4.5:1)"`

5. **After adjustment:** Re-validate ALL 4 pairs (adjusting one color may affect multiple pairs).

### Provenance Note

If a token's value is changed by this validation step, retain the original provenance marker (`extracted-from-url` or `inferred-from-domain`) — adjustment is a downstream correction, not a re-source. Append the adjustment record to the Contrast Validation table's `Adjustments` line in the artefact.
