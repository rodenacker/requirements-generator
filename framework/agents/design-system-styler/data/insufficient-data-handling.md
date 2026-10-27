# Insufficient Data Handling — Design-System-Styler Data File

**Role:** Pure reference knowledge consumed by step-05 (Brand Extraction). Defines the minimum color threshold for the lead URL's extraction and the procedure when its CSS lacks enough data. An insufficient URL is a **failed reference**, not a route to anything else: the run continues with the other references, and step-05's reference gate raises `RF-14` if none is usable.

---

## 8. Insufficient Data Handling

Before attempting color-to-token mapping (Section 3 of `color-extraction-rules.md`), check whether the CSS contains enough color data for meaningful extraction.

### Minimum Threshold

Count the number of **distinct non-white/non-black hex colors** (excluding near-white and near-black, but **including** neutral grays) found in the CSS:

- **3 or more distinct non-white/non-black colors:** Proceed with extraction.
- **Fewer than 3 distinct non-white/non-black colors:** Insufficient data — skip this URL's extraction; its reference is `failed — too few colours`.

### Insufficient-Data Path

If the threshold is not met:

1. Set `{{extraction_status}}: "insufficient_data"`.
2. Log:
   ```
   STYLER BRAND EXTRACTION — INSUFFICIENT DATA
   ───────────────────────────────────────────
   Reference URL: {{lead_url}}
   CSS content size: {{css_size}} characters
   Distinct chromatic colors found: {{color_count}} (minimum required: 3)
   Total color values scanned: {{total_colors}}
   Analysis: CSS lacks sufficient brand color variety for meaningful extraction.
   Impact: This URL is a failed reference; the other references are still used.
   ```
3. Set the lead URL's reference `status` to `failed — too few colours`.
4. Skip the lead URL's remaining extraction sub-steps and go to step-05 §7 (merge + reference gate) — do NOT halt here. With no other usable reference, the gate raises `RF-14`.
