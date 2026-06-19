# Domain Suggestion — Prompt Template

**Purpose:** Reusable instruction block for inferring a short **domain descriptor** for a business from the signals captured off its website, so the styler can *suggest* it to the consultant in step-04b. This is the bridge between the page fetched in step-04 and the per-run token inference in step-05b, which consumes the chosen `{{domain}}` string.

**Usage:** Read this file using the Read tool. Apply its instructions to `{{business_signals}}` (captured in step-04 from the same fetch that grabbed the CSS — no second fetch). Produce a primary descriptor + 1–2 alternatives + a one-line rationale, which step-04b presents via `AskUserQuestion`. This template **does not** fetch anything and **does not** produce design tokens — token inference is `domain-inference.md`'s job, and it runs later in step-05b against whichever domain the consultant confirms.

---

## 1. Inputs: the business signals

`{{business_signals}}` is an in-memory object captured in step-04. Its fields depend on the fetch path:

**Playwright path** — structured page metadata:

- `title` — `document.title`.
- `metaDescription` — `<meta name="description">` content.
- `ogSiteName`, `ogTitle`, `ogType`, `ogDescription` — Open Graph tags (`og:site_name`, `og:title`, `og:type`, `og:description`).
- `h1` — text of the first `<h1>`.
- `nav` — array of primary navigation link labels (top nav / header).
- `heroText` — the most prominent above-the-fold heading/sub-heading text, if distinct from `h1`.
- `jsonLd` — any schema.org JSON-LD objects found, especially an `Organization` / `LocalBusiness` node and its `@type`, `description`, `industry`, or `knowsAbout` fields.

**WebFetch fallback path** — `{{business_signals}}` is the LLM-summarised page content WebFetch returned (prose describing what the site/company is). Treat it as a single free-text description; the same synthesis rules apply.

Any individual field may be absent. Reason from whatever is present.

---

## 2. Synthesis rules

### 2.1 Primary descriptor (`{{suggested_domain}}`)

Produce **one** short domain descriptor that names *what kind of product/business this is* — the same kind of string a consultant would type, and the same shape `domain-inference.md` expects:

- Style: lowercase, hyphenated where natural, 1–4 words. Examples: `retail-banking`, `pet-grooming-marketplace`, `legal services SaaS`, `internal HR portal`, `healthcare-booking`.
- Name the **sector/function**, not the company. `acme-bank.com` → `retail-banking`, **not** `acme`.
- Prefer the strongest signals in this order: schema.org `industry`/`@type` → `metaDescription` / `ogDescription` → `title` / `ogSiteName` → `h1` / `heroText` → `nav` labels. JSON-LD industry fields are the highest-signal when present; nav labels are a weak last resort.
- Capture the product's **frontend character** when the signals make it clear (e.g. distinguish a `marketplace` from a single-vendor `storefront`, an `internal-tooling` admin from a public `saas` app), since this biases the downstream voice. Do not over-reach beyond what the signals support.
- Lowercase and trim the result.

### 2.2 Alternatives (`{{domain_alt_1}}`, optional `{{domain_alt_2}}`)

Produce 1–2 **genuinely distinct** alternative readings of the same page — not synonyms of the primary. Good sources of a real alternative:

- A broader or narrower scope (`digital-banking-platform` vs `retail-banking`; `fintech-lending` if lending is prominent).
- A sibling sub-sector the signals also support.
- Public-facing vs internal framing, single-vendor vs marketplace, B2B vs B2C — when the page is genuinely ambiguous between them.

Always emit **at least one** alternative so step-04b's menu has ≥2 concrete options. If the page is unambiguous, the alternative is the nearest adjacent interpretation (e.g. broaden the scope by one level). Never pad with a near-duplicate of the primary.

### 2.3 Rationale (one line)

One short clause naming the signal(s) that drove the primary pick, for the question body — e.g. *"its meta description calls it a 'mobile-first business bank'"* or *"schema.org lists industry: Veterinary"*. Keep it to a phrase; it is context for the consultant's decision, not a justification essay.

---

## 3. Output contract

Return, in memory, for step-04b to consume:

- `{{suggested_domain}}` — non-empty, lowercased, trimmed.
- `{{domain_alt_1}}` — non-empty; distinct from `{{suggested_domain}}`.
- `{{domain_alt_2}}` — optional; distinct from both above. Omit rather than duplicate.
- A one-line rationale string.

Do **not** invent design tokens, voice statements, colours, or any token-level inference here — that is `domain-inference.md` in step-05b. This template stops at the descriptor.

---

## 4. Anti-patterns

- Do not return the company / brand name as the domain (`acme`, `acme-bank`). The domain names the *kind of business*.
- Do not fetch anything. Operate only on `{{business_signals}}` already captured in step-04.
- Do not return only one option with no alternative — the menu requires ≥2 concrete choices.
- Do not make the alternatives synonyms or trivial rephrasings of the primary.
- Do not over-specify beyond the signals (don't claim a sub-sector the page gives no evidence for); when uncertain, prefer a broader, defensible descriptor and let an alternative carry the narrower guess.
