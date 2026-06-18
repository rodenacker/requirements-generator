---
name: step-02-inputs
description: 'Collect domain (required) and reference URL (optional) directly from the consultant via a single prose prompt. No upstream file lookup.'
---

# Step 2: Collect Consultant Inputs

Two pieces of input are needed: the **domain** (required) and a **reference URL** (optional). Both come from the consultant directly — never from any file under `requirements/`, `framework/state/`, or any other agent's output.

## 2a. Ask for domain + optional URL (single prose prompt)

Ask for both in **one** conversational message — not via `AskUserQuestion`, and without a list of options (the domain must stay free-text):

> *"What domain best describes this product? (e.g. `retail-banking`, `pet-grooming-marketplace`, `internal HR portal`). Optionally paste a reference URL for brand extraction, or say `skip` to infer everything from the domain."*

Wait for the consultant's reply, then parse the domain and the optional URL from that single message.

## 2b. Parse the reply

**Domain (required):**

- Take the free-text descriptor from the reply (excluding any URL token). Trim surrounding whitespace and lower-case it; store the result as `{{domain}}`.
- The domain must always be set. If the reply yields no usable domain, re-prompt. There is no skip option for the domain — the styler always infers tokens per-run from this string in step-05b.

**Reference URL (optional):**

- If the reply contains an `http(s)://` token, or a clear domain-like token (e.g. `acme.io`, `www.acme.com`), treat it as the reference URL and apply the **URL validation** below.
- If the reply says `skip` / `none` / `no url`, or contains no URL token at all, set `{{reference_url}} = null`. This is a deliberate skip — not a failure. Do **not** re-prompt for a missing URL.

### URL validation

If a URL token was found:

- Trim surrounding whitespace.
- Must start with `http://` or `https://`. If it lacks a protocol prefix, prepend `https://`.
- Store the validated URL as `{{reference_url}}`.

## 2c. Echo the captured inputs

Before advancing, echo the captured inputs back to the consultant in one short Unicorn-voice line. This is **informational, not a confirmation gate** — it lets the consultant catch a mis-parse; if the interpretation is wrong they correct it at step-07's Restart, so the single-round-trip saving is preserved:

- With URL: *"Domain: `{{domain}}`. URL: `{{reference_url}}`. Fetching CSS now."*
- Without URL: *"Domain: `{{domain}}`. No URL — inferring every token from the domain."*

---

**Next:**

- If `{{reference_url}}` is set, read fully and follow `step-04-site-fetching.md`. (Step 3 is intentionally a no-op in this agent — the orchestrator handles re-run gating.)
- If `{{reference_url}}` is null, set `{{extraction_status}} = "no_url"` and skip directly to `step-05b-domain-inference.md`.
