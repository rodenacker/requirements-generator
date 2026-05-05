---
name: step-02-inputs
description: 'Collect domain (required) and reference URL (optional) directly from the consultant via AskUserQuestion. No upstream file lookup.'
---

# Step 2: Collect Consultant Inputs

Two pieces of input are needed: the **domain** (required) and a **reference URL** (optional). Both come from the consultant directly — never from any file under `requirements/`, `framework/state/`, or any other agent's output.

## 2a. Ask for the domain

Collect the domain as free text only — do **not** present a list of options to choose from. Prompt the consultant directly in the conversation:

> *"What domain best describes this product? Type a short descriptor (e.g. `retail-banking`, `pet-grooming-marketplace`, `internal HR portal`)."*

Wait for the consultant's reply, then capture.

### Capture

- Trim surrounding whitespace and lower-case the consultant's answer; store the result as `{{domain}}`.

The domain must always be set after this sub-step. If the consultant returns an empty answer, re-prompt. There is no skip option for the domain. The styler always infers tokens per-run from this string in step-05b.

## 2b. Ask for the reference URL

Use `AskUserQuestion` with two options + free-text:

- Question: *"Optional reference URL for brand extraction. Paste a public URL and I'll extract colours and typography from its CSS, or skip and I'll infer every token from `{{domain}}`."*
- Header: `Reference URL`
- multiSelect: false
- Options (in this order):
  1. `Provide URL` (Recommended) — followed up by the consultant typing the URL in the next message OR using the `Other` free-text option.
  2. `Skip — infer everything from the domain` — every token will be tagged `inferred-from-domain`.

If the consultant chooses the **Provide URL** option, accept the URL from their next message (or the `Other` free-text answer). If they chose **Skip**, set `{{reference_url}} = null`.

### URL validation

If a URL was provided:

- Must start with `http://` or `https://`. If it lacks a protocol prefix, prepend `https://`.
- Trim surrounding whitespace.
- Store the validated URL as `{{reference_url}}`.

If no URL was provided (`{{reference_url}}` is null), record this as a deliberate skip — not a failure — and let the workflow route every token through step-05b.

## 2c. Echo the captured inputs

Before advancing, echo the captured inputs back to the consultant in one short Unicorn-voice line:

- With URL: *"Domain: `{{domain}}`. URL: `{{reference_url}}`. Fetching CSS now."*
- Without URL: *"Domain: `{{domain}}`. No URL — inferring every token from the domain."*

---

**Next:**

- If `{{reference_url}}` is set, read fully and follow `step-04-site-fetching.md`. (Step 3 is intentionally a no-op in this agent — the orchestrator handles re-run gating.)
- If `{{reference_url}}` is null, set `{{extraction_status}} = "no_url"` and skip directly to `step-05b-domain-inference.md`.
