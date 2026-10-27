---
name: step-02-inputs
description: 'Collect the brand references (URLs and/or PDF brand guides in documentation/) directly from the consultant via a single prose prompt. No upstream file lookup; never scans documentation/.'
---

# Step 2: Collect the Brand References

**Fresh run state.** On entry (a first run or a step-07 Restart), unset `{{references}}`, `{{reference_urls}}`, `{{reference_pdfs}}`, `{{lead_url}}`, `{{declared}}`, `{{merged_sources}}` and `{{extraction_status}}`. Workspace files from an earlier run are never trusted: step-05 reads only files belonging to this run's `used` references.

One input is collected here: the **brand references**. They come from the consultant directly — never from any file under `generated-docs/requirements/`, `framework/state/`, or any other agent's output. The styler reads **only** the files the consultant names: it never scans `documentation/` (it cannot tell a brand guide from a requirements PDF).

Two reference kinds are accepted:

1. **URL**, public or intranet — fetched in step-04.
2. **PDF brand guide** already in `documentation/` — read in step-04b.

Screenshots / images and saved web pages are **not** accepted (a screenshot would yield guessed hex values; a saved page needs file access the browser does not have).

## 2a. Ask for the references (single prose prompt)

Ask with **one** conversational message — not via `AskUserQuestion`:

> *"Give me the brand references: one or more website URLs (public or intranet; for a style guide, its home or overview page rather than the colour-swatch page), and/or PDF brand guides you've put in `documentation/`. The first URL sets the background and text colours. I can't use screenshots or pages behind a login. For those, add the PDF brand guide."*

Wait for the consultant's reply, then parse every reference from that single message.

## 2b. Parse the reply

Walk the reply's tokens **in order** and build `{{references}}` — an ordered list of `{kind, ref, status}`, in the order the consultant gave them, every `status` starting as `pending`:

- **URL** — an `http(s)://` token, or a clear domain-like token (e.g. `acme.io`, `www.acme.com`). Validate:
  - Trim surrounding whitespace.
  - Must start with `http://` or `https://`. If it lacks a protocol prefix, prepend `https://`.
  - → `{kind: "url", ref: "<validated url>", status: "pending"}`.
- **File name** — a token ending in a file extension (`brand-guide.pdf`, `documentation/brand guide.pdf`, `logo.png`). Resolve it to `documentation/<name>` (a leading `documentation/` is accepted and not doubled).
  - `.pdf` → `{kind: "pdf", ref: "documentation/<name>", status: "pending"}`. Existence and location are checked in step-04b, which marks a missing or out-of-folder file `skipped`.
  - Any other extension (image, `.html`, `.docx`, …) → not a reference: say so in one line (§2c) and never read it. It does not enter `{{references}}`.

Derive the two working lists, each in `{{references}}` order:

- `{{reference_urls}}` — every `kind: "url"` entry.
- `{{reference_pdfs}}` — every `kind: "pdf"` entry.

**No references at all** (an empty reply, `skip` / `none`, or nothing that parses as a URL or a PDF) → raise **`RF-14`** per `framework/shared/refusal-registry.md > RF-14 — brand_reference_missing` and end the run. Nothing is written.

## 2c. Echo the references

Echo one short Unicorn-voice line per reference. This is **informational, not a confirmation gate** — it lets the consultant catch a mis-parse; if the interpretation is wrong they correct it at step-07's Restart:

- *"URL 1: `<url>` (sets the background and text colours)."* — the first URL only; later URLs: *"URL <n>: `<url>`."*
- *"PDF: `<path>`."*
- *"Not using `<name>`: only URLs and PDF brand guides are references (screenshots and images would give guessed colours)."*

---

**Next:**

- If `{{reference_urls}}` is non-empty, read fully and follow `step-04-site-fetching.md`. (Step 3 is intentionally a no-op in this agent — the orchestrator handles re-run gating.)
- Otherwise set `{{extraction_status}} = "not_applicable"` and skip directly to `step-04b-pdf-references.md`.
