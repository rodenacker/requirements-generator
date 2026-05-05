---
name: step-04-site-fetching
description: 'Playwright-driven site fetching: resize → navigate → settle → aggregate stylesheets + computed :root + sample elements. Falls back to two-pass WebFetch only when the consultant elects it at the preflight prompt. Skipped entirely when reference_url is null.'
# Variables referenced (inherited from agent):
# workspace_path: 'design-system/.workspace'
# Variables read for the WebFetch fallback path only:
# prompt_site_fetching: 'framework/agents/design-system-styler/prompt-templates/site-fetching.md'
# prompt_css_identification: 'framework/agents/design-system-styler/prompt-templates/css-identification.md'
---

# Step 4: Site Fetching (Playwright-preferred, WebFetch fallback)

**Skip condition:** if `{{reference_url}}` is null (consultant skipped the URL prompt in step-02), do not run any sub-step here. Skip directly to `step-05b-domain-inference.md` with `{{extraction_status}} = "no_url"`. No preflight, no Playwright invocation.

---

## 4.0 Preflight: Confirm Playwright MCP is available

When `{{reference_url}}` is non-null, before any navigation, run the preflight skill:

```
Read tool: framework/skills/preflight-mcp.md
```

Apply the skill's procedure with the following inputs:

- `tool_name = mcp__playwright__browser_navigate`
- `advice_path = framework/shared/setup-instructions/playwright.md`
- `rf_predicate = RF-06`

**If the skill returns `ok`:** advance to §4.A (Playwright path).

**If the skill returns `RF-06 trigger`:** surface the predicate per `framework/shared/refusal-registry.md > RF-06 style_extraction_dependency_missing`. Use `AskUserQuestion` with three options. The question text must include the path `framework/shared/setup-instructions/playwright.md` and the verbatim fidelity warning for option B.

| Option header | Label                                  | Description (shown to consultant)                                                                                                                                                                                                                                                                                  |
| ------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Install       | Install Playwright and retry           | Highest fidelity. Stop now, install per `framework/shared/setup-instructions/playwright.md`, then re-run `/design-system`. The agent will exit cleanly after this prompt.                                                                                                                                          |
| WebFetch      | Use WebFetch instead (degraded fidelity) | WebFetch returns LLM-summarised content rather than raw CSS. Exact hex codes, custom properties, and computed font/shadow values are typically lost. Brand-token extraction will be lower fidelity than Playwright; many tokens may end up `inferred-from-domain` instead of `extracted-from-url`.                  |
| Drop URL      | Drop the URL and infer from the domain   | Most predictable. The run proceeds without any URL extraction; every token is inferred per-run from `{{domain}}` and tagged `inferred-from-domain`.                                                                                                                                                                |

**Branch on the consultant's selection:**

- **Install** → emit a single-line handback note pointing at `framework/shared/setup-instructions/playwright.md`, set `{{extraction_status}} = "playwright_unavailable"` in agent memory, and exit step-04 by terminating the agent run cleanly. Do NOT advance to step-05 or step-05b on this branch — the consultant must install and re-run.
- **WebFetch** → set `{{extraction_method}} = "webfetch-fallback"` in agent memory and advance to §4.B (WebFetch fallback path).
- **Drop URL** → set `{{reference_url}} = null`, set `{{extraction_status}} = "playwright_unavailable"`, and skip to `step-05b-domain-inference.md`.

---

## 4.A Playwright path (preferred)

Reached when preflight returned `ok`. Sets `{{extraction_method}} = "playwright"` in agent memory.

### 4.A.1 Pass 1 — Navigate with desktop viewport and settling wait

1. Resize the viewport to desktop *before* navigation, so the captured tokens reflect desktop breakpoints (not mobile):
   ```
   mcp__playwright__browser_resize({ width: 1440, height: 900 })
   ```
2. Navigate:
   ```
   mcp__playwright__browser_navigate({ url: "{{reference_url}}" })
   ```
3. Settle for late-loading styles (CSS-in-JS injection — styled-components, emotion, vanilla-extract, etc.):
   ```
   mcp__playwright__browser_evaluate({
     function: "async () => { await document.fonts.ready; await new Promise(r => setTimeout(r, 1500)); return true; }"
   })
   ```
4. Capture the rendered HTML:
   ```
   mcp__playwright__browser_evaluate({ function: "() => document.documentElement.outerHTML" })
   ```
   Store the result as `{{homepage_html}}`.

**Validation:** verify `{{homepage_html}}` contains `<html`, `<!doctype`, or `<head` (case-insensitive). If not (JSON, plain text, binary):

- Log: "Fetched content from {{reference_url}} is not HTML (likely an API endpoint or non-web-page URL)"
- Set `{{extraction_status}} = "fetch_failed"`
- Set `{{extraction_error}} = "Response is not an HTML page"`
- Close the browser (`mcp__playwright__browser_close()`) and skip to `step-05b-domain-inference.md`.

**On any navigation/evaluate error** (timeout, DNS failure, HTTP 4xx/5xx surfaced by Playwright):

- Log: "Playwright failed to load {{reference_url}}: {error_description}"
- Set `{{extraction_status}} = "fetch_failed"` and `{{extraction_error}} = "{error_description}"`
- Close the browser if it is still open. Skip to `step-05b-domain-inference.md`.

### 4.A.2 Pass 2 — Aggregate stylesheets and computed tokens

Single `browser_evaluate` returning a JSON object:

```
mcp__playwright__browser_evaluate({
  function: `
    () => {
      const sheetTexts = [];
      const sources = [];
      for (const sheet of document.styleSheets) {
        try {
          const rules = Array.from(sheet.cssRules).map(r => r.cssText).join("\n");
          sheetTexts.push(rules);
          sources.push(sheet.href || "inline");
        } catch (e) {
          if (sheet.href) sources.push({ corsBlocked: sheet.href });
        }
      }
      const inlineStyles = Array.from(document.querySelectorAll("style"))
        .map(s => s.textContent).join("\n");

      const rootStyle = getComputedStyle(document.documentElement);
      const customProperties = {};
      for (let i = 0; i < rootStyle.length; i++) {
        const name = rootStyle[i];
        if (name.startsWith("--")) customProperties[name] = rootStyle.getPropertyValue(name).trim();
      }

      const sample = (sel) => {
        const el = document.querySelector(sel);
        if (!el) return null;
        const cs = getComputedStyle(el);
        return {
          color: cs.color, backgroundColor: cs.backgroundColor,
          fontFamily: cs.fontFamily, fontSize: cs.fontSize,
          fontWeight: cs.fontWeight, lineHeight: cs.lineHeight,
          boxShadow: cs.boxShadow,
          transitionDuration: cs.transitionDuration,
          transitionTimingFunction: cs.transitionTimingFunction
        };
      };

      return {
        rawCss: sheetTexts.join("\n\n") + "\n\n" + inlineStyles,
        sources,
        customProperties,
        sampleElements: {
          body: sample("body"),
          h1: sample("h1"), h2: sample("h2"), h3: sample("h3"),
          h4: sample("h4"), h5: sample("h5"), h6: sample("h6"),
          link: sample("a"),
          button: sample('button, .btn, [role="button"]'),
          input: sample("input, textarea, select")
        }
      };
    }
  `
})
```

Store the result as `{{eval_payload}}`.

### 4.A.3 CORS fallback for cross-origin stylesheets

For each entry in `{{eval_payload}}.sources` that is an object with a `corsBlocked` href:

1. Call `mcp__playwright__browser_network_request({ url: <corsBlocked href>, method: "GET" })`.
2. On success, append the body text to `{{eval_payload}}.rawCss` (separated by `\n\n`).
3. On per-sheet failure (network error, non-200 status), log "CORS-fallback fetch failed for {href}" and continue to the next blocked sheet. Do NOT abort the run for one failed sheet.

### 4.A.4 Close the browser

```
mcp__playwright__browser_close()
```

### 4.A.5 Filter framework custom properties

Filter `{{eval_payload}}.customProperties` into two maps before synthesizing the `:root` block. Drop keys matching any of these prefixes (extends v3's framework-source blacklist from stylesheet *files* to custom-property *names*, since Playwright resolves every `:root` var at runtime regardless of which stylesheet declared it):

```
--tw-       (Tailwind utility runtime vars)
--bs-       (Bootstrap)
--mui-      (Material UI)
--mdc-      (Material Design Components)
--chakra-   (Chakra)
--mantine-  (Mantine)
--ion-      (Ionic)
--ant-      (Ant Design)
--ng-       (Angular Material runtime)
--vuetify-  (Vuetify)
--ck-       (CKEditor)
--swiper-   (Swiper carousel)
```

Move matching keys into a separate map `{{framework_properties}}`. Keep the remaining keys in `{{custom_properties}}` — these are the brand-relevant tokens.

### 4.A.6 Synthesize the brand `:root` block

Build a synthetic CSS block from `{{custom_properties}}`:

```
:root {
  --<name>: <value>;
  ...
}
```

Use the resolved values returned by `getComputedStyle` (already concrete strings, not raw declarations with `var(...)` references). This restores the highest-signal source for the existing `color-extraction-rules.md` "CSS Custom Properties (Highest Signal)" path even on sites whose underlying CSS uses runtime-resolved variables.

### 4.A.7 Empty-CSS guard

If **all** of the following are true:
- `{{eval_payload}}.rawCss` is empty (whitespace only),
- `{{custom_properties}}` is empty after framework filtering,
- every entry in `{{eval_payload}}.sampleElements` is null,

then:

- Log: "No identifiable CSS content captured from {{reference_url}}"
- Set `{{extraction_status}} = "no_css"`
- Skip to `step-05b-domain-inference.md`. (The browser is already closed.)

### 4.A.8 Content size management

Concatenate the synthetic `:root` block (from §4.A.6) with `{{eval_payload}}.rawCss`, separated by `\n\n`, into `{{primary_css_content}}`. If the result exceeds approximately 100,000 characters:

- Truncate to the first ~100,000 characters.
- Log: "CSS content truncated from {original_size} to ~100KB for context management."
- Justification (preserved from v3): brand-defining styles are typically declared early in a stylesheet.

### 4.A.9 Workspace write

1. Create the workspace directory if absent: `Bash mkdir -p design-system/.workspace`
2. Write `design-system/.workspace/css-content.txt` — the full `{{primary_css_content}}` (synthetic `:root` block + concatenated CSS, post-truncation).
3. Write `design-system/.workspace/computed-tokens.json`:
   ```json
   {
     "customProperties": { ... },
     "frameworkProperties": { ... },
     "sampleElements": {
       "body": { ... },
       "h1": { ... }, ...
     },
     "sources": [ ... ]
   }
   ```
4. Write `design-system/.workspace/metadata.json`:
   ```json
   {
     "extraction_method": "playwright",
     "css_source_type": "browser-aggregate",
     "css_source_url": "{{reference_url}}",
     "stylesheet_sources": [ ... ],
     "reference_url": "{{reference_url}}"
   }
   ```

Store the final results in agent memory:

- `{{homepage_html}}` — full rendered HTML (only if needed by step-05; typically discarded after this step).
- `{{primary_css_content}}` — synthetic `:root` block + raw CSS.
- `{{custom_properties}}` — filtered brand custom properties (resolved values).
- `{{sample_elements}}` — computed styles for body / h1–h6 / link / button / input.
- `{{css_source_type}}` — `"browser-aggregate"`.
- `{{css_source_url}}` — `{{reference_url}}` (the homepage URL, since stylesheets are aggregated).

**Note:** Do not set `{{extraction_status}}` to `"success"` here — it is set by step-05 after extraction completes. Setting it prematurely could mask downstream extraction failures.

---

## 4.B WebFetch fallback path (degraded fidelity)

Reached only when the consultant explicitly selected option **B (Use WebFetch instead)** at the §4.0 preflight prompt. Sets `{{extraction_method}} = "webfetch-fallback"` and proceeds with the legacy two-pass WebFetch logic. **Do not write `computed-tokens.json` on this path** — the rules files in `framework/agents/design-system-styler/data/` detect its absence and use legacy text-pattern matching against `{{primary_css_content}}` only.

Read the site-fetching prompt template before executing:

```
Read tool: framework/agents/design-system-styler/prompt-templates/site-fetching.md
```

Apply its instructions to perform the two-pass fetch.

### 4.B.1 Pass 1: Fetch Homepage HTML

1. Use WebFetch to retrieve the homepage at `{{reference_url}}`.
2. Store the full HTML response as `{{homepage_html}}`.

**If WebFetch fails (network error, timeout, HTTP 4xx/5xx):**

- Log: "Failed to fetch homepage: {error_description}"
- Set `{{extraction_status}} = "fetch_failed"`
- Set `{{extraction_error}} = "{error_description}"`
- Skip to `step-05b-domain-inference.md`. Do NOT halt.

**If WebFetch succeeds:** Verify the response is HTML by checking that the content contains `<html`, `<!doctype`, or `<head` (case-insensitive). If not HTML (e.g., JSON, plain text, binary):

- Log: "Fetched content from {{reference_url}} is not HTML (likely an API endpoint or non-web-page URL)"
- Set `{{extraction_status}} = "fetch_failed"`
- Set `{{extraction_error}} = "Response is not an HTML page"`
- Skip to `step-05b-domain-inference.md`.

### 4.B.2 CSS Source Identification

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
- Skip to `step-05b-domain-inference.md`.

**If CSS sources found:** Select the primary source per the prompt template heuristics and store as `{{primary_css_source}}` with `{{css_source_type}}` (`"external"` or `"inline"`).

### 4.B.3 Pass 2: Fetch Primary Stylesheet (External Sources Only)

**If `{{primary_css_source}}` is external:**

1. Resolve the stylesheet URL per the URL Resolution Rules in the prompt template.
2. Use WebFetch to retrieve the stylesheet at the resolved URL.
3. Store the CSS content as `{{primary_css_content}}`.

**If WebFetch fails for the stylesheet:**

- Check if an inline `<style>` block exists as fallback.
- If fallback available: use the largest inline `<style>` block as `{{primary_css_content}}`; log "External stylesheet fetch failed, using inline style fallback".
- If no fallback: set `{{extraction_status}} = "css_fetch_failed"`, skip to `step-05b-domain-inference.md`.

**If `{{primary_css_source}}` is inline:**

- Extract the content of the identified `<style>` block as `{{primary_css_content}}`.

### 4.B.4 Content Size Management

If `{{primary_css_content}}` exceeds approximately 100,000 characters:

- Truncate to the first ~100,000 characters.
- Log: "CSS content truncated from {original_size} to ~100KB for context management".

### 4.B.5 Workspace Write (WebFetch fallback)

Persist state to disk for inter-step access:

1. Create the workspace directory: `Bash mkdir -p design-system/.workspace`
2. Write `design-system/.workspace/css-content.txt` — the full `{{primary_css_content}}`.
3. **Do NOT write `design-system/.workspace/computed-tokens.json` on this path.** Step-05's rules files detect its absence and use legacy text-pattern matching exclusively.
4. Write `design-system/.workspace/metadata.json`:
   ```json
   {
       "extraction_method": "webfetch-fallback",
       "css_source_type": "{{css_source_type}}",
       "css_source_url": "{{css_source_url}}",
       "reference_url": "{{reference_url}}"
   }
   ```

Store the final results in agent memory:

- `{{homepage_html}}` — Full homepage HTML
- `{{primary_css_content}}` — Primary CSS content
- `{{css_source_type}}` — `"external"` or `"inline"`
- `{{css_source_url}}` — URL of the stylesheet (if external) or `"inline"`

---

**Next:** Read fully and follow `step-05-brand-extraction.md`.
