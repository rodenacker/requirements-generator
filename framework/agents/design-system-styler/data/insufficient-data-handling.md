# Insufficient Data Handling — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by step-05 (Brand Extraction). Defines the minimum color threshold for URL extraction and the procedure when CSS lacks enough data. Adapted from v3 b3-style-extractor: instead of a hard exit, "insufficient data" routes the entire token set to step-05b for domain-defaults fill.

---

## 8. Insufficient Data Handling

Before attempting color-to-token mapping (Section 3 of `color-extraction-rules.md`), check whether the CSS contains enough color data for meaningful extraction.

### Minimum Threshold

Count the number of **distinct non-white/non-black hex colors** (excluding near-white and near-black, but **including** neutral grays) found in the CSS:

- **3 or more distinct non-white/non-black colors:** Proceed with extraction.
- **Fewer than 3 distinct non-white/non-black colors:** Insufficient data — skip extraction; all tokens fall through to step-05b for domain-defaults fill.

### Insufficient-Data Path

If the threshold is not met:

1. Set `{{extraction_status}}: "insufficient_data"`.
2. Log:
   ```
   STYLER BRAND EXTRACTION — INSUFFICIENT DATA
   ───────────────────────────────────────────
   Reference URL: {{reference_url}}
   CSS content size: {{css_size}} characters
   Distinct chromatic colors found: {{color_count}} (minimum required: 3)
   Total color values scanned: {{total_colors}}
   Analysis: CSS lacks sufficient brand color variety for meaningful extraction.
   Impact: All tokens will be filled from `framework/assets/domain-defaults/{{domain}}.md` (or per-run inference if {{domain}} is free-text).
   ```
3. Skip the remaining extraction sub-steps (font, contrast). Step-05b handles every token.
4. Continue to step-05b — do NOT halt. The agent always produces a complete artefact under the stand-alone constraint, even when the URL yielded nothing usable.
