---
name: step-04-site-fetching
description: 'Playwright-driven site fetching for each URL reference: resize → navigate → settle (login-page check) → aggregate stylesheets + computed :root + sample elements. Falls back to two-pass WebFetch only when the consultant elects it at the preflight prompt. Skipped entirely when there are no URL references.'
# Variables referenced (inherited from agent):
# workspace_path: 'generated-docs/design-system/.workspace'
# Variables read for the WebFetch fallback path only:
# prompt_site_fetching: 'framework/agents/design-system-styler/prompt-templates/site-fetching.md'
# prompt_css_identification: 'framework/agents/design-system-styler/prompt-templates/css-identification.md'
---

# Step 4: Site Fetching (Playwright-preferred, WebFetch fallback)

**Skip condition:** if `{{reference_urls}}` is empty (no URL references), do not run any sub-step here. Set `{{extraction_status}} = "not_applicable"` and skip directly to `step-04b-pdf-references.md`. No preflight, no Playwright invocation.

**One URL at a time, in order.** Run §4.A once per entry of `{{reference_urls}}`, in the order the consultant gave them:

- **The lead URL** is the first URL whose capture succeeds. It does the **full capture** (§4.A.1–§4.A.9), unchanged: `css-content.txt`, `computed-tokens.json`, `metadata.json`. Its page sets the scheme and the neutrals, and it is the only source of `{{alt_scheme}}`. Set `{{lead_url}}` to it.
- **Every later URL** (once a lead exists) does the **lean capture**: §4.A.1, then the §4.A.2 evaluate unchanged, keeping only its `colourWeights` and `sampleElements` (font data), written to `generated-docs/design-system/.workspace/computed-tokens-<n>.json` (`<n>` = the URL's 1-based position in `{{reference_urls}}`; plain `Write`, workspace scratch). No CORS fallback, no `:root` synthesis, no `css-content.txt`. Close the browser (§4.A.4).
- **A failed URL** sets that reference's `status` to `failed — <reason>` (one line naming it) and the loop continues with the next URL. A failure never ends the run here: step-05's reference gate decides whether anything usable is left.
- Set the reference's `status` to `used` when its capture succeeds.

`{{extraction_status}}` describes the lead URL's capture; if no URL captured, it is the first URL's failure status. **Every exit from this step routes to `step-04b-pdf-references.md`** — except the RF-06 *Install* branch below, which aborts the run.

---

## 4.0 Preflight: Confirm Playwright MCP is available

When `{{reference_urls}}` is non-empty, before any navigation, run the preflight skill (once per run, not per URL):

```
Read tool: framework/skills/preflight-mcp.md
```

Apply the skill's procedure with the following inputs:

- `tool_name = mcp__playwright__browser_navigate`
- `advice_path = framework/shared/setup-instructions/playwright.md`
- `rf_predicate = RF-06`

**If the skill returns `ok`:** advance to §4.A (Playwright path).

**If the skill returns `RF-06 trigger`:** surface the predicate per `framework/shared/refusal-registry.md > RF-06 style_extraction_dependency_missing`. Use `AskUserQuestion` with three options — two when no PDF reference exists (*Continue without URLs* is offered **only** when `{{reference_pdfs}}` is non-empty). The question text must include the path `framework/shared/setup-instructions/playwright.md` and the verbatim fidelity warning for the WebFetch option.

| Option header | Label                                  | Description (shown to consultant)                                                                                                                                                                                                                                                                                  |
| ------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Install       | Install Playwright and retry           | Highest fidelity. Stop now, install per `framework/shared/setup-instructions/playwright.md`, then re-run `/design-system`. The agent will exit cleanly after this prompt.                                                                                                                                          |
| WebFetch      | Use WebFetch instead (degraded fidelity) | WebFetch returns LLM-summarised content rather than raw CSS. Exact hex codes, custom properties, and computed font values are typically lost, and only the first URL is read. Brand-colour extraction will be lower fidelity than Playwright; more colours may end up `system-derived` (helper fallbacks) instead of `extracted`. |
| Continue      | Continue without URLs                    | Only when a PDF brand guide was also given. Every URL reference is skipped; the run uses the PDF reference(s) only. |

**Branch on the consultant's selection:**

- **Install** (`install-and-retry`) → emit a single-line handback note pointing at `framework/shared/setup-instructions/playwright.md`, set `{{extraction_status}} = "playwright_unavailable"` in agent memory, and exit step-04 by terminating the agent run cleanly. Do NOT advance to step-05 or step-05b on this branch — the consultant must install and re-run.
- **WebFetch** (`use-webfetch-fallback`) → set `{{extraction_method}} = "webfetch-fallback"` in agent memory and advance to §4.B (WebFetch fallback path).
- **Continue** (`continue-without-urls`) → mark every URL reference `skipped — Playwright unavailable`, set `{{extraction_status}} = "playwright_unavailable"`, and skip to `step-04b-pdf-references.md`.

---

## 4.A Playwright path (preferred)

Reached when preflight returned `ok`. Sets `{{extraction_method}} = "playwright"` in agent memory. Below, `{{url}}` is the URL being captured in this pass of the loop.

### 4.A.1 Pass 1 — Navigate with desktop viewport and settling wait

1. Resize the viewport to desktop *before* navigation, so the captured tokens reflect desktop breakpoints (not mobile):
   ```
   mcp__playwright__browser_resize({ width: 1440, height: 900 })
   ```
2. Navigate:
   ```
   mcp__playwright__browser_navigate({ url: "{{url}}" })
   ```
3. Settle for late-loading styles (CSS-in-JS injection — styled-components, emotion, vanilla-extract, etc.) and return an HTML-validity flag and the login-page signals in the **same** call (no separate HTML capture — the full `outerHTML` is never consumed on the Playwright path):
   ```
   mcp__playwright__browser_evaluate({
     function: "async () => { await document.fonts.ready; await new Promise(r => setTimeout(r, 1500)); const pw = Array.from(document.querySelectorAll('input[type=password]')).some(el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; }); return { settled: true, isHtmlDoc: !!document.querySelector('html') || !!document.querySelector('head') || !!document.doctype, finalHost: location.host, finalPath: location.pathname, title: document.title, visiblePassword: pw }; }"
   })
   ```
   Store the returned `isHtmlDoc`, `finalHost`, `finalPath`, `title` and `visiblePassword`.

**Login-page check (before anything is captured).** Two signals, compared lower-cased:

- **Moved host** — `finalHost` differs from the requested URL's host, ignoring a leading `www.`.
- **Auth-like** — `finalHost`, `finalPath` or `title` contains one of `login`, `log-in`, `signin`, `sign-in`, `sign in`, `logon`, `sso`, `saml`, `oauth`, `openid`, `adfs`, `auth`, `idp`, `okta`.

The reference is a login page when **(moved host and (auth-like or `visiblePassword`)) or (`visiblePassword` and auth-like)**. Neither signal alone decides it: a bank homepage with an inline sign-in widget (password field, own host, ordinary path) and a regional or canonical redirect (`acme.de` → `acme.com`, no auth signal) are brand pages, not login pages. Then:

- Log one line: *"`{{url}}` is a login page (`<finalHost>`), not the brand. Skipping it; for a guide behind a login, add its PDF."*
- Set this reference's `status` to `failed — login page`, and `{{extraction_status}} = "fetch_failed"` with `{{extraction_error}} = "login page"` (lead attempt only). Never extract an identity provider's login page as the brand.
- Close the browser (`mcp__playwright__browser_close()`) and continue with the next URL.

**Validation:** if the returned `isHtmlDoc` flag is false (the live DOM has no `<html>` / `<head>` / doctype — e.g. JSON, plain text, binary):

- Log: "Fetched content from {{url}} is not HTML (likely an API endpoint or non-web-page URL)"
- Set `{{extraction_status}} = "fetch_failed"` (lead attempt only) and `{{extraction_error}} = "Response is not an HTML page"`; set this reference's `status` to `failed — not an HTML page`.
- Close the browser (`mcp__playwright__browser_close()`) and continue with the next URL.

**On any navigation/evaluate error** (timeout, DNS failure, HTTP 4xx/5xx surfaced by Playwright):

- Log: "Playwright failed to load {{url}}: {error_description}"
- Set `{{extraction_status}} = "fetch_failed"` (lead attempt only) and `{{extraction_error}} = "{error_description}"`; set this reference's `status` to `failed — could not load (<error_description>)`.
- Close the browser if it is still open, and continue with the next URL.

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

      // Colour area weights — which chromatic colours the page actually shows,
      // and how much of them. Feeds the `brand` pick and the "real use" test
      // in framework/tools/colour-tokens.cjs. Any CSS colour syntax is
      // normalised through a 1x1 canvas. Near-greys (max−min channel < 24)
      // and colours with alpha < 0.5 are skipped.
      const cv = document.createElement("canvas"); cv.width = cv.height = 1;
      const ctx = cv.getContext("2d", { willReadFrequently: true });
      const toHex = (c) => {
        if (!c || c === "transparent" || c === "none") return null;
        ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = "#000"; ctx.fillStyle = c; ctx.fillRect(0, 0, 1, 1);
        const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;
        if (a < 128) return null;
        if (Math.max(r, g, b) - Math.min(r, g, b) < 24) return null;
        return "#" + [r, g, b].map(v => v.toString(16).padStart(2, "0")).join("").toUpperCase();
      };
      const weights = {};
      const addW = (c, w) => { const h = toHex(c); if (h) weights[h] = (weights[h] || 0) + w; };
      for (const el of document.body.querySelectorAll("*")) {
        const rect = el.getBoundingClientRect();
        if (!rect.width || !rect.height) continue;
        const cs = getComputedStyle(el);
        if (cs.visibility === "hidden" || cs.display === "none" || Number(cs.opacity) === 0) continue;
        addW(cs.backgroundColor, Math.min(rect.width * rect.height, 200000) / 1000);
        if (Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim())) addW(cs.color, 1);
        for (const side of ["Top", "Right", "Bottom", "Left"]) {
          if (parseFloat(cs["border" + side + "Width"]) > 0 && cs["border" + side + "Style"] !== "none") addW(cs["border" + side + "Color"], 0.2);
        }
      }
      const colourWeights = Object.entries(weights)
        .map(([hex, weight]) => ({ hex, weight: Math.round(weight * 10) / 10 }))
        .sort((a, b) => b.weight - a.weight).slice(0, 30);

      // The site's own other scheme — every rule inside
      // @media (prefers-color-scheme: <opposite>) plus root-level theme-variant
      // rules ([data-*theme*=<opposite>], .<opposite>, [data-color-mode=<opposite>]).
      const bgRgb = (() => {
        for (const el of [document.body, document.documentElement]) {
          const m = getComputedStyle(el).backgroundColor.match(/[\d.]+/g);
          if (m && (m.length < 4 || Number(m[3]) > 0.5)) return m.slice(0, 3).map(Number);
        }
        return [255, 255, 255];
      })();
      const pageScheme = (0.2126 * bgRgb[0] + 0.7152 * bgRgb[1] + 0.0722 * bgRgb[2]) / 255 < 0.5 ? "dark" : "light";
      const opposite = pageScheme === "dark" ? "light" : "dark";
      const variantRe = new RegExp("^(:root|html|body)?\\s*(\\." + opposite + "\\b|\\[data-[\\w-]*(theme|mode|scheme)[\\w-]*=[\"']?" + opposite + "[\"']?\\])");
      const alt = { scheme: opposite, customProperties: {}, declarations: [] };
      const colourProp = /^(color|background(-color)?|border(-[a-z]+)?-color|fill|stroke|outline-color|box-shadow)$/;
      const isColour = (v) => { ctx.fillStyle = "#010203"; ctx.fillStyle = v; return ctx.fillStyle !== "#010203"; };
      const takeStyle = (rule) => {
        const rootSel = /^(:root|html|body|:host)\b/.test(rule.selectorText) || variantRe.test(rule.selectorText);
        for (const prop of rule.style) {
          const value = rule.style.getPropertyValue(prop).trim();
          if (!value) continue;
          if (prop.startsWith("--")) { if (rootSel && isColour(value)) alt.customProperties[prop] = value; }
          else if (colourProp.test(prop) && alt.declarations.length < 300) alt.declarations.push({ selector: rule.selectorText, prop, value });
        }
      };
      const walk = (rules, inScheme) => {
        for (const rule of rules) {
          if (rule.media && rule.cssRules) {
            walk(rule.cssRules, inScheme || rule.media.mediaText.includes("prefers-color-scheme: " + opposite));
          } else if (rule.cssRules && !rule.selectorText) {
            walk(rule.cssRules, inScheme);
          } else if (rule.selectorText && (inScheme || variantRe.test(rule.selectorText))) {
            takeStyle(rule);
          }
        }
      };
      for (const sheet of document.styleSheets) { try { walk(sheet.cssRules, false); } catch (e) {} }
      const altScheme = (Object.keys(alt.customProperties).length || alt.declarations.length) ? alt : null;

      return {
        finalHost: location.host, finalPath: location.pathname, title: document.title,
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
        },
        colourWeights,
        pageScheme,
        altScheme
      };
    }
  `
})
```

Store the result as `{{eval_payload}}`. **Re-run the login-page check** on its `finalHost` / `finalPath` / `title` (a script can redirect to an identity provider after Pass 1 settled); a hit fails the reference exactly as in §4.A.1, before anything from this payload is used. **Lean capture** (a URL after the lead): write `{ "colourWeights": …, "sampleElements": … }` from it to `computed-tokens-<n>.json`, set the reference's `status` to `used`, skip to §4.A.4 (close the browser), and continue with the next URL.

Also store `{{colour_weights}} = {{eval_payload}}.colourWeights` (area-weighted chromatic colours: background area / 1000, area capped at 200 000 px², + 1 per text use + 0.2 per visible border; sorted descending, top 30) and `{{alt_scheme}} = {{eval_payload}}.altScheme` (`null` when the site ships no opposite-scheme rules). Step-05 turns `{{colour_weights}}` into the `assign` candidates; step-05b §A-bis reads `{{alt_scheme}}`.

### 4.A.3 CORS fallback for cross-origin stylesheets

For each entry in `{{eval_payload}}.sources` that is an object with a `corsBlocked` href:

1. Call `mcp__playwright__browser_network_request({ url: <corsBlocked href>, method: "GET" })`.
2. On success, append the body text to `{{eval_payload}}.rawCss` (separated by `\n\n`). Also scan that text for `@media (prefers-color-scheme: <altScheme scheme, else the opposite of pageScheme>)` blocks and root-level theme-variant rules (same selectors as the evaluate's `variantRe`), and merge their custom properties / colour declarations into `{{alt_scheme}}` (creating it with `scheme` = the opposite of `pageScheme` if it was `null`).
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

- Log: "No identifiable CSS content captured from {{url}}"
- Set `{{extraction_status}} = "no_css"` and this reference's `status` to `failed — no CSS captured`.
- Continue with the next URL (the browser is already closed).

### 4.A.8 Content size management

Concatenate the synthetic `:root` block (from §4.A.6) with `{{eval_payload}}.rawCss`, separated by `\n\n`, into `{{primary_css_content}}`. If the result exceeds approximately 100,000 characters:

- Truncate to the first ~100,000 characters.
- **`@font-face` blocks are exempt.** Before truncating, collect every `@font-face { … }` block from the **untruncated** text (regex `/@font-face\s*\{[^}]*\}/g`), and append each distinct one after the truncated content under a `/* @font-face blocks kept past truncation */` comment. They are small, and they are step-05 §4b E1's only evidence of the face a site actually serves — sites routinely declare them after 100 KB of framework CSS.
- Log: "CSS content truncated from {original_size} to ~100KB for context management."
- Justification (preserved from v3): brand-defining styles are typically declared early in a stylesheet.

### 4.A.9 Workspace write

1. Create the workspace directory if absent: `Bash mkdir -p generated-docs/design-system/.workspace`
2. Write `generated-docs/design-system/.workspace/css-content.txt` — the full `{{primary_css_content}}` (synthetic `:root` block + concatenated CSS, post-truncation).
3. Write `generated-docs/design-system/.workspace/computed-tokens.json`:
   ```json
   {
     "customProperties": { ... },
     "frameworkProperties": { ... },
     "sampleElements": {
       "body": { ... },
       "h1": { ... }, ...
     },
     "sources": [ ... ],
     "colourWeights": [ { "hex": "#RRGGBB", "weight": 0 } ],
     "pageScheme": "light" | "dark",
     "altScheme": null | { "scheme": "dark" | "light", "customProperties": { ... }, "declarations": [ { "selector": "...", "prop": "...", "value": "..." } ] }
   }
   ```
4. Write `generated-docs/design-system/.workspace/metadata.json`:
   ```json
   {
     "extraction_method": "playwright",
     "css_source_type": "browser-aggregate",
     "css_source_url": "{{url}}",
     "stylesheet_sources": [ ... ],
     "lead_url": "{{url}}"
   }
   ```

Store the final results in agent memory:

- `{{primary_css_content}}` — synthetic `:root` block + raw CSS.
- `{{custom_properties}}` — filtered brand custom properties (resolved values).
- `{{sample_elements}}` — computed styles for body / h1–h6 / link / button / input.
- `{{css_source_type}}` — `"browser-aggregate"`.
- `{{css_source_url}}` — `{{url}}` (the page URL, since stylesheets are aggregated).
- `{{lead_url}}` — `{{url}}`; this reference's `status` = `used`. Every later URL does the lean capture.

**Note:** Do not set `{{extraction_status}}` to `"success"` here — it is set by step-05 after extraction completes. Setting it prematurely could mask downstream extraction failures.

---

## 4.B WebFetch fallback path (degraded fidelity)

Reached only when the consultant explicitly selected **Use WebFetch instead** at the §4.0 preflight prompt. Sets `{{extraction_method}} = "webfetch-fallback"` and proceeds with the legacy two-pass WebFetch logic. **One URL only:** WebFetch reads the first URL in `{{reference_urls}}` (`{{url}}` below); it yields no area data to pool, so every later URL is marked `skipped — WebFetch fallback reads the first URL only`. A first URL that fails here is marked `failed — <reason>` and the run continues to step-04b. WebFetch cannot see a password field reliably: a summary that describes a sign-in / login page is treated as `failed — login page`. **Do not write `computed-tokens.json` on this path** — the rules files in `framework/agents/design-system-styler/data/` detect its absence and use legacy text-pattern matching against `{{primary_css_content}}` only.

Read the site-fetching prompt template before executing:

```
Read tool: framework/agents/design-system-styler/prompt-templates/site-fetching.md
```

Apply its instructions to perform the two-pass fetch.

### 4.B.1 Pass 1: Fetch Homepage HTML

1. Use WebFetch to retrieve the page at `{{url}}`.
2. Store the full HTML response as `{{homepage_html}}`.

**If WebFetch fails (network error, timeout, HTTP 4xx/5xx):**

- Log: "Failed to fetch homepage: {error_description}"
- Set `{{extraction_status}} = "fetch_failed"`, `{{extraction_error}} = "{error_description}"`, and the reference's `status` to `failed — could not load (<error_description>)`.
- Skip to `step-04b-pdf-references.md`. Do NOT halt.

**If WebFetch succeeds:** Verify the response is HTML by checking that the content contains `<html`, `<!doctype`, or `<head` (case-insensitive). If not HTML (e.g., JSON, plain text, binary):

- Log: "Fetched content from {{url}} is not HTML (likely an API endpoint or non-web-page URL)"
- Set `{{extraction_status}} = "fetch_failed"`, `{{extraction_error}} = "Response is not an HTML page"`, and the reference's `status` to `failed — not an HTML page`.
- Skip to `step-04b-pdf-references.md`.

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
- Set `{{extraction_status}} = "no_css"` and the reference's `status` to `failed — no CSS captured`.
- Skip to `step-04b-pdf-references.md`.

**If CSS sources found:** Select the primary source per the prompt template heuristics and store as `{{primary_css_source}}` with `{{css_source_type}}` (`"external"` or `"inline"`).

### 4.B.3 Pass 2: Fetch Primary Stylesheet (External Sources Only)

**If `{{primary_css_source}}` is external:**

1. Resolve the stylesheet URL per the URL Resolution Rules in the prompt template.
2. Use WebFetch to retrieve the stylesheet at the resolved URL.
3. Store the CSS content as `{{primary_css_content}}`.

**If WebFetch fails for the stylesheet:**

- Check if an inline `<style>` block exists as fallback.
- If fallback available: use the largest inline `<style>` block as `{{primary_css_content}}`; log "External stylesheet fetch failed, using inline style fallback".
- If no fallback: set `{{extraction_status}} = "css_fetch_failed"` and the reference's `status` to `failed — stylesheet fetch failed`, and skip to `step-04b-pdf-references.md`.

**If `{{primary_css_source}}` is inline:**

- Extract the content of the identified `<style>` block as `{{primary_css_content}}`.

### 4.B.4 Content Size Management

If `{{primary_css_content}}` exceeds approximately 100,000 characters:

- Truncate to the first ~100,000 characters, keeping every `@font-face` block past the cut exactly as §4.A.8 describes.
- Log: "CSS content truncated from {original_size} to ~100KB for context management".

### 4.B.5 Workspace Write (WebFetch fallback)

Persist state to disk for inter-step access:

1. Create the workspace directory: `Bash mkdir -p generated-docs/design-system/.workspace`
2. Write `generated-docs/design-system/.workspace/css-content.txt` — the full `{{primary_css_content}}`.
3. **Do NOT write `generated-docs/design-system/.workspace/computed-tokens.json` on this path.** Step-05's rules files detect its absence and use legacy text-pattern matching exclusively. There is no `{{colour_weights}}` and no `{{alt_scheme}}` on this path: consumers treat both as absent (step-05 sends `weight: null` candidates; step-05b derives the other mode).
4. Write `generated-docs/design-system/.workspace/metadata.json`:
   ```json
   {
       "extraction_method": "webfetch-fallback",
       "css_source_type": "{{css_source_type}}",
       "css_source_url": "{{css_source_url}}",
       "lead_url": "{{url}}"
   }
   ```

Store the final results in agent memory:

- `{{homepage_html}}` — Full homepage HTML
- `{{primary_css_content}}` — Primary CSS content
- `{{css_source_type}}` — `"external"` or `"inline"`
- `{{css_source_url}}` — URL of the stylesheet (if external) or `"inline"`
- `{{lead_url}}` — `{{url}}`; the reference's `status` = `used`.

---

**Next:** Read fully and follow `step-04b-pdf-references.md` (reads any PDF brand guides; with none it passes straight through). Step-04b then proceeds to `step-05-brand-extraction.md`.
