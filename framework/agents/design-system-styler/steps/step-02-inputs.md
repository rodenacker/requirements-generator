---
name: step-02-inputs
description: 'Collect domain (required) and reference URL (optional) directly from the consultant via AskUserQuestion. No upstream file lookup.'
---

# Step 2: Collect Consultant Inputs

Two pieces of input are needed: the **domain** (required) and a **reference URL** (optional). Both come from the consultant directly — never from any file under `requirements/`, `framework/state/`, or any other agent's output.

## 2a. Ask for the domain

Use `AskUserQuestion` with seven curated options + free-text:

- Question: *"Which domain best describes this product? Pick from the curated list — these have hand-tuned token defaults — or pick **Other** and type your own."*
- Header: `Domain`
- multiSelect: false
- Options (in this order):
  1. `retail-banking` — Trustworthy, conservative, blue-dominant. (Recommended for banking apps.)
  2. `education-saas` — Friendly, energetic, warm primary, generous line-heights.
  3. `healthcare-booking` — Calm, clean, accessibility-conscious cool palette.
  4. `internal-tooling` — Dense, functional, neutral grayscale + utility accent.
  5. `ecommerce` — Confident, action-forward, conversion-oriented.
  6. `fintech-consumer` — Modern, sharp, vibrant primary against deep neutrals.
  7. `government-services` — Plain, accessible, high-contrast, no decorative shadows.

Plus the automatic `Other` option from the harness, which lets the consultant type a free-text domain string.

### Capture and classify

- If the consultant picked one of the seven curated values: store as `{{domain}}` and set `{{domain_source}} = "curated"`.
- If the consultant picked `Other` and typed a free-text answer: store the free-text answer as `{{domain}}` (verbatim, lower-cased trimmed) and set `{{domain_source}} = "free-text"`.

The domain must always be set after this sub-step. If the consultant somehow returns no answer, re-ask. There is no skip option for the domain.

## 2b. Ask for the reference URL

Use `AskUserQuestion` with two options + free-text:

- Question: *"Optional reference URL for brand extraction. Paste a public URL and I'll extract colours and typography from its CSS, or skip and I'll use the `{{domain}}` defaults for everything."*
- Header: `Reference URL`
- multiSelect: false
- Options:
  1. `Skip — use domain defaults only` — every token will be tagged `inferred-from-domain`.
  2. `Provide URL` — followed up by the consultant typing the URL in the next message OR using the `Other` free-text option.

If the consultant chooses the **Provide URL** option, accept the URL from their next message (or the `Other` free-text answer). If they chose **Skip**, set `{{reference_url}} = null`.

### URL validation

If a URL was provided:

- Must start with `http://` or `https://`. If it lacks a protocol prefix, prepend `https://`.
- Trim surrounding whitespace.
- Store the validated URL as `{{reference_url}}`.

If no URL was provided (`{{reference_url}}` is null), record this as a deliberate skip — not a failure — and let the workflow route every token through step-05b.

## 2c. Echo the captured inputs

Before advancing, echo the captured inputs back to the consultant in one short Unicorn-voice line:

- With URL: *"Domain: `{{domain}}` (`{{domain_source}}`). URL: `{{reference_url}}`. Fetching CSS now."*
- Without URL: *"Domain: `{{domain}}` (`{{domain_source}}`). No URL — filling everything from defaults."*

---

**Next:**

- If `{{reference_url}}` is set, read fully and follow `step-04-site-fetching.md`. (Step 3 is intentionally a no-op in this agent — the orchestrator handles re-run gating.)
- If `{{reference_url}}` is null, set `{{extraction_status}} = "no_url"` and skip directly to `step-05b-domain-fill.md`.
