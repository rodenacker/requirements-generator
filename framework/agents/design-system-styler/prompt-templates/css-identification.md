# CSS Identification — Prompt Template

**Purpose:** This is a reusable instruction block for classifying CSS sources found in a homepage HTML document and handling graceful exit conditions. The design-system-styler workflow loads this file after HTML parsing to determine the CSS source type and handle cases where no usable CSS exists. Ported from v3 b3-style-extractor.

**Usage:** Read this file using the Read tool. Apply the classification rules to the parsed HTML results from the site-fetching step.

---

## 1. CSS Source Classification

After parsing the homepage HTML, classify the result into one of these categories:

### Category A: External Stylesheet Found

**Condition:** At least one `<link rel="stylesheet">` tag found with a non-framework `href` (per site-fetching.md exclusion patterns).

**Action:**
- Set `{{css_source_type}}` = `"external"`
- Set `{{css_source_url}}` = resolved URL of the selected stylesheet
- Proceed to Pass 2 (fetch the stylesheet)

**Diagnostic output:**
```
CSS Source: External stylesheet
URL: {{css_source_url}}
Selection: 1st non-framework of {{total_count}} external stylesheets found
Excluded: {{excluded_count}} framework/CDN stylesheets skipped
```

### Category B: Inline Style Only

**Condition:** No qualifying external stylesheets found, but at least one non-empty `<style>` block exists.

**Action:**
- Set `{{css_source_type}}` = `"inline"`
- Set `{{css_source_url}}` = `"inline"`
- Extract the content of the largest `<style>` block as `{{primary_css_content}}`
- Skip Pass 2 (no external fetch needed)

**Diagnostic output:**
```
CSS Source: Inline <style> block
Size: {{style_size}} characters
Selection: Largest of {{total_inline_count}} inline style blocks
Note: No external stylesheets found; using inline styles for brand analysis
```

### Category C: No CSS Found

**Condition:** No `<link rel="stylesheet">` tags and no non-empty `<style>` blocks in the homepage HTML.

**Action:**
- Set `{{extraction_status}}` = `"no_css"`
- Log the diagnostic output below
- Skip URL extraction; route every token through step-05b (domain-inference)

**Diagnostic output:**
```
CSS Source: None found
HTML size: {{html_size}} characters
Analysis: Homepage contains no identifiable CSS sources
  - External stylesheets (<link rel="stylesheet">): 0
  - Inline style blocks (<style>): 0
Impact: All tokens will be inferred per-run from `{{domain}}`.
```

---

## 2. Graceful Exit Conditions

The styler never halts. These are the exit conditions that bypass CSS fetching and route every token through step-05b for domain-inference:

### Exit: No Reference URL

**Trigger:** Consultant skipped the URL prompt in step-02.
**Status:** `extraction_status: "no_url"`
**Log message:** "No reference site URL provided. Inferring every token per-run from `{{domain}}`."

### Exit: Homepage Fetch Failed

**Trigger:** WebFetch for the homepage returned an error (network, timeout, HTTP error).
**Status:** `extraction_status: "fetch_failed"`
**Log message:** "Failed to fetch homepage at {{reference_url}}: {{error_description}}"

### Exit: No CSS Sources

**Trigger:** Category C classification — homepage has no CSS.
**Status:** `extraction_status: "no_css"`
**Log message:** "Homepage at {{reference_url}} contains no identifiable CSS sources."

### Exit: Stylesheet Fetch Failed (No Fallback)

**Trigger:** External stylesheet WebFetch failed AND no inline `<style>` fallback available.
**Status:** `extraction_status: "css_fetch_failed"`
**Log message:** "Failed to fetch stylesheet at {{css_source_url}}: {{error_description}}. No inline style fallback available."

---

## 3. Diagnostic Output Format

Every execution of the CSS identification step produces a diagnostic summary, regardless of outcome. This is logged for transparency and debugging.

### Success Format

```
STYLER CSS IDENTIFICATION
─────────────────────────
Reference URL: {{reference_url}}
Homepage fetch: ✓ ({{html_size}} chars)
External stylesheets found: {{external_count}}
  Excluded (framework/CDN): {{excluded_count}}
  Selected: {{selected_url}}
Inline style blocks found: {{inline_count}}
  Largest: {{largest_inline_size}} chars
Primary CSS source: {{css_source_type}} ({{css_source_url}})
CSS content size: {{css_size}} chars
Extraction status: success
```

### Failure Format

```
STYLER CSS IDENTIFICATION
─────────────────────────
Reference URL: {{reference_url}}
Homepage fetch: {{✓ | ✗}} {{error_if_failed}}
External stylesheets found: {{external_count}}
Inline style blocks found: {{inline_count}}
Primary CSS source: none
Extraction status: {{extraction_status}}
Reason: {{extraction_error}}
Impact: All tokens will be inferred per-run from `{{domain}}`.
```
