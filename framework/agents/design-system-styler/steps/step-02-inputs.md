---
name: step-02-inputs
description: 'Collect the reference URL (optional) directly from the consultant via a single prose prompt. URL-first: the page is fetched in step-04 and the business is suggested as the domain in step-04b. No upstream file lookup.'
---

# Step 2: Collect the Reference URL

One piece of input is collected here: a **reference URL** (optional). It comes from the consultant directly — never from any file under `requirements/`, `framework/state/`, or any other agent's output. The **domain** is not collected here — when a URL is given, step-04b suggests it from the fetched page; when no URL is given, step-04b asks for it directly.

## 2a. Ask for the URL first (single prose prompt)

Ask with **one** conversational message — not via `AskUserQuestion`:

> *"Paste a reference URL and I'll read the page to suggest the domain — or say `skip` and you can tell me the domain yourself."*

Wait for the consultant's reply, then parse the optional URL from that single message.

## 2b. Parse the reply

**Reference URL (optional):**

- If the reply contains an `http(s)://` token, or a clear domain-like token (e.g. `acme.io`, `www.acme.com`), treat it as the reference URL and apply the **URL validation** below.
- If the reply says `skip` / `none` / `no url`, or contains no URL token at all, set `{{reference_url}} = null`. This is a deliberate skip — not a failure. Do **not** re-prompt for a missing URL; step-04b will collect the domain directly.

### URL validation

If a URL token was found:

- Trim surrounding whitespace.
- Must start with `http://` or `https://`. If it lacks a protocol prefix, prepend `https://`.
- Store the validated URL as `{{reference_url}}`.

## 2c. Echo the captured URL

Before advancing, echo the captured URL back in one short Unicorn-voice line. This is **informational, not a confirmation gate** — it lets the consultant catch a mis-parse; if the interpretation is wrong they correct it at step-07's Restart:

- With URL: *"URL: `{{reference_url}}`. Fetching the page now."*
- Without URL: *"No URL — I'll ask you for the domain next."*

---

**Next:**

- If `{{reference_url}}` is set, read fully and follow `step-04-site-fetching.md`. (Step 3 is intentionally a no-op in this agent — the orchestrator handles re-run gating.)
- If `{{reference_url}}` is null, set `{{extraction_status}} = "no_url"`, set `{{business_signals}} = null`, and skip directly to `step-04b-domain.md` (which will ask for the domain directly).
