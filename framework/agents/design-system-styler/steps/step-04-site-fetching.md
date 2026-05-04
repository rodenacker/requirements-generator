---
name: step-04-site-fetching
description: 'Two-pass site fetching: WebFetch homepage → identify primary stylesheet → WebFetch stylesheet. Skipped entirely when reference_url is null.'
# Variables referenced (inherited from agent):
# prompt_site_fetching: 'framework/agents/design-system-styler/prompt-templates/site-fetching.md'
# prompt_css_identification: 'framework/agents/design-system-styler/prompt-templates/css-identification.md'
# workspace_path: 'design-system/.workspace'
---

# Step 4: Two-Pass Site Fetching

**Skip condition:** if `{{reference_url}}` is null (consultant skipped the URL prompt in step-02), do not run any sub-step here. Skip directly to `step-05b-domain-fill.md` with `{{extraction_status}} = "no_url"`.

Read the site-fetching prompt template before executing:

```
Read tool: framework/agents/design-system-styler/prompt-templates/site-fetching.md
```

Apply its instructions to perform the two-pass fetch.

## Pass 1: Fetch Homepage HTML

1. Use WebFetch to retrieve the homepage at `{{reference_url}}`.
2. Store the full HTML response as `{{homepage_html}}`.

**If WebFetch fails (network error, timeout, HTTP 4xx/5xx):**

- Log: "Failed to fetch homepage: {error_description}"
- Set `{{extraction_status}} = "fetch_failed"`
- Set `{{extraction_error}} = "{error_description}"`
- Skip to `step-05b-domain-fill.md`. Do NOT halt.

**If WebFetch succeeds:** Verify the response is HTML by checking that the content contains `<html`, `<!doctype`, or `<head` (case-insensitive). If not HTML (e.g., JSON, plain text, binary):

- Log: "Fetched content from {{reference_url}} is not HTML (likely an API endpoint or non-web-page URL)"
- Set `{{extraction_status}} = "fetch_failed"`
- Set `{{extraction_error}} = "Response is not an HTML page"`
- Skip to `step-05b-domain-fill.md`.

## CSS Source Identification

Read the css-identification prompt template:

```
Read tool: framework/agents/design-system-styler/prompt-templates/css-identification.md
```

Apply its classification rules to `{{homepage_html}}`:

1. Scan for `<link rel="stylesheet" href="...">` tags
2. Scan for inline `<style>` blocks
3. Classify the CSS source per the prompt template heuristics

**If no CSS sources found:**

- Log: "No identifiable CSS sources in homepage HTML"
- Set `{{extraction_status}} = "no_css"`
- Skip to `step-05b-domain-fill.md`.

**If CSS sources found:** Select the primary source per the prompt template heuristics and store as `{{primary_css_source}}` with `{{css_source_type}}` ("external" or "inline").

## Pass 2: Fetch Primary Stylesheet (External Sources Only)

**If `{{primary_css_source}}` is external:**

1. Resolve the stylesheet URL per the URL Resolution Rules in the prompt template.
2. Use WebFetch to retrieve the stylesheet at the resolved URL.
3. Store the CSS content as `{{primary_css_content}}`.

**If WebFetch fails for the stylesheet:**

- Check if an inline `<style>` block exists as fallback.
- If fallback available: use the largest inline `<style>` block as `{{primary_css_content}}`; log "External stylesheet fetch failed, using inline style fallback".
- If no fallback: set `{{extraction_status}} = "css_fetch_failed"`, skip to `step-05b-domain-fill.md`.

**If `{{primary_css_source}}` is inline:**

- Extract the content of the identified `<style>` block as `{{primary_css_content}}`.

## Content Size Management

If `{{primary_css_content}}` exceeds approximately 100,000 characters:

- Truncate to the first ~100,000 characters.
- Log: "CSS content truncated from {original_size} to ~100KB for context management".

## Workspace Write

Persist state to disk for inter-step access:

1. Create the workspace directory: `Bash mkdir -p design-system/.workspace`
2. Write `design-system/.workspace/css-content.txt` — the full `{{primary_css_content}}`.
3. Write `design-system/.workspace/metadata.json`:
    ```json
    {
        "css_source_type": "{{css_source_type}}",
        "css_source_url": "{{css_source_url}}",
        "reference_url": "{{reference_url}}"
    }
    ```

Store the final results in agent memory:

- `{{homepage_html}}` — Full homepage HTML
- `{{primary_css_content}}` — Primary CSS content
- `{{css_source_type}}` — "external" or "inline"
- `{{css_source_url}}` — URL of the stylesheet (if external) or "inline"

**Note:** Do not set `{{extraction_status}}` to `"success"` here — it is set by step-05 after extraction completes. Setting it prematurely could mask downstream extraction failures.

---

**Next:** Read fully and follow `step-05-brand-extraction.md`.
