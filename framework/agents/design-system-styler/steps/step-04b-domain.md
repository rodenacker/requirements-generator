---
name: step-04b-domain
description: 'Set the domain — suggested from the fetched page when business signals are available (AskUserQuestion menu), or collected via a free-text prose prompt when no URL was given / the fetch did not yield signals. Always runs.'
# Variables referenced (inherited from agent):
# domain_suggestion: 'framework/agents/design-system-styler/prompt-templates/domain-suggestion.md'
---

# Step 4b: Set the Domain (suggest-from-URL, or collect directly)

This step **always runs**, on every path out of step-04 except the RF-06 *Install* branch (which aborts the run cleanly). It is the single place the `{{domain}}` is set. The domain is required: the styler infers a per-run token set from it in step-05b, so it must end this step non-null.

Two branches, decided by whether step-04 captured `{{business_signals}}`:

- **Signals present** (`{{business_signals}}` is non-null) → **§A. Suggest from the page.**
- **No signals** (`{{reference_url}}` was null, or the fetch failed / yielded no usable signals, or the consultant chose *Drop URL* at the RF-06 prompt) → **§B. Collect directly.**

---

## A. Suggest the domain from the fetched page

Reached when `{{business_signals}}` is non-null (Playwright or WebFetch captured page metadata/text in step-04).

1. **Load the suggestion contract:**

   ```
   Read tool: framework/agents/design-system-styler/prompt-templates/domain-suggestion.md
   ```

2. **Synthesise.** Apply the contract to `{{business_signals}}`. Produce:
   - `{{suggested_domain}}` — one short domain descriptor in the same style as the `domain-inference.md` examples (e.g. `retail-banking`, `pet-grooming-marketplace`, `internal HR portal`), lowercased and trimmed.
   - 1–2 **alternative interpretations** (`{{domain_alt_1}}`, `{{domain_alt_2}}`) — distinct, plausible readings of the same page. Always produce at least one alternative so the menu below is well-formed; if the page is unambiguous, derive an adjacent interpretation (broader/narrower scope, or a sibling sub-sector).
   - A one-line confidence/rationale note naming the signal(s) that drove the pick (for the question body).

3. **Present the menu.** Use `AskUserQuestion`:
   - Question: *"Reading `{{reference_url}}`, this looks like a **`{{suggested_domain}}`** product ({{one-line rationale}}). Use this as the domain, or pick another?"*
   - Header: `Domain`
   - multiSelect: false
   - Options (the `Other` free-text option is provided automatically by the tool):
     1. `{{suggested_domain}}` *(Recommended)* — the primary inference.
     2. `{{domain_alt_1}}` — first alternative interpretation.
     3. `{{domain_alt_2}}` — second alternative interpretation (omit if only one alternative is warranted).

4. **Resolve the choice → `{{domain}}`:**
   - Consultant picked option 1, 2, or 3 → set `{{domain}}` to that option's descriptor.
   - Consultant typed an `Other` free-text value → set `{{domain}}` to that value.
   - Lower-case and trim `{{domain}}`.

5. **Record provenance:**
   - If the consultant accepted option 1 (the suggestion) → `{{domain_provenance}} = "suggested-from-url-accepted"`.
   - If the consultant picked an alternative or typed their own → `{{domain_provenance}} = "suggested-from-url-overridden"`.

Proceed to **§C. Validate and advance.**

---

## B. Collect the domain directly (no signals)

Reached when `{{business_signals}}` is null. Ask the domain with a single prose prompt — **not** via `AskUserQuestion`, and without a list of options (the domain must stay free-text):

> *"What domain best describes this product? (e.g. `retail-banking`, `pet-grooming-marketplace`, `internal HR portal`). I'll infer every token from it."*

Wait for the reply, take the free-text descriptor, trim and lower-case it, and store it as `{{domain}}`. Set `{{domain_provenance}} = "consultant-typed"`.

Proceed to **§C. Validate and advance.**

---

## C. Validate and advance

1. **Required-field check.** `{{domain}}` must be a non-empty string after trimming. If it is empty (e.g. the consultant submitted blank `Other` text, or an empty prose reply), re-prompt:
   - On the §A path, re-present the menu once; if still empty, fall through to the §B prose prompt.
   - On the §B path, re-ask the prose prompt until a usable domain is given. There is no skip for the domain.

2. **Echo (informational, not a gate).** Output one short Unicorn-voice line so the consultant can catch a mis-parse (corrected later at step-07's Restart):
   - §A path: *"Domain: `{{domain}}` (from `{{reference_url}}`). Extracting brand tokens now."*
   - §B path: *"Domain: `{{domain}}`. Inferring every token from it."*

---

**Next:** Read fully and follow `step-05-brand-extraction.md`. (Step-05 self-skips to `step-05b-domain-inference.md` when no CSS was captured.)
