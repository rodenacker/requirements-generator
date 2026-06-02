<!-- ROLE: asset (P2 review reference). Loaded by framework/agents/reviews-inputs/ambiguity-reviewer.md at activation. -->

# reviews-inputs/ambiguity-reference.md

**Purpose:** Methodology reference for Ambiguity Review of the **raw consultant input set** enumerated by `requirements/source-manifest.json`. The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews-inputs/ambiguity-reviewer.md` — drives the agent's seven-dimension sequential sweep plus the quality-gate sweep.

**Output produced by the reviewer:** `review-inputs/AMBIGUITY-REVIEW/ambiguity-review.html` — a self-contained HTML punch-list of cited, severity-graded findings, with an ambiguity register (a table keyed by ambiguity type, one row per finding) carrying a ready-to-paste stakeholder elicitation question per finding. The reviewer renders it by substituting into the scaffold `framework/assets/reviews-inputs/template-ambiguity.html`.

**Sibling lens:** The `/review-inputs` adversarial reviewer (`framework/assets/reviews-inputs/adversarial-reference.md`) sweeps a broader seven-dimension critique (stakeholder coverage, workflow coverage, ambiguity & vague language, provenance & conflict, quantitative signal, scope & MVP, bias & sampling). Adversarial's Dimension 3 (Ambiguity & Vague Language) overlaps this reference, but at a coarser grain: adversarial reports "vague verb in load-bearing position" as a single finding; this reviewer decomposes that into the specific linguistic taxonomy class (lexical / syntactic / referential / vague-predicate / subjective / weak-verb / optionality-passive), produces ≥2 plausible interpretations per finding, and emits a ready-to-paste elicitation question. The two reviewers are complementary: run adversarial when you want the broad coverage punch-list; run this one when you have a draft of the requirements thinking and need to flush specific ambiguities before drafting.

---

## What "ambiguity review" means

A requirement is **ambiguous** if a competent reader of the inputs can plausibly interpret it in more than one way, where each plausible reading produces a different downstream requirement. The discipline is rooted in two complementary taxonomies from the requirements-engineering literature:

1. **Berry & Kamsties (2004), *Ambiguity in Requirements Specification*.** Four linguistic categories — lexical, syntactic, semantic, pragmatic — plus two related phenomena: vagueness and generality. The canonical academic taxonomy.
2. **Femmer et al., *Requirements Smells* (Smella).** Nine operational quality smells: anaphora, coordination ambiguity, vagueness, passive voice, referential integrity, subjectivity, nocuous ambiguity, multiple interpretations, consistency. The operational checklist that surfaces the linguistic categories in practical reviewer prompts.

This reference consolidates the two taxonomies into **seven non-overlapping dimensions**, sized to mirror the parallel adversarial reviewer's seven-dimension structure and tuned for raw consultant inputs (briefs, decks, transcripts, screenshots) rather than finished requirements docs. Berry/Kamsties' four linguistic categories are preserved (with their semantic class split into referential and vague-predicate). Femmer's three operationally-distinct smells (subjective, weak verb, optionality-passive) are added.

Recent 2024 work (DEAR — MDPI Electronics 2024; *A Short Survey on Formalising Software Requirements with LLMs* — arXiv 2024) shows in-context LLM prompting outperforms classical NLP smell-detectors when given concrete demonstrations of each ambiguity type. This reference therefore inlines 2 worked examples per dimension — one clear positive find, one near-miss with explanation — so the reviewer has pattern-match anchors.

The discipline's **central rule:** every finding lists **≥2 plausible interpretations**, each of which would produce a different requirement when downstream `/requirements` drafts. If you cannot produce two interpretations, the candidate isn't ambiguous — it might be wrong, incomplete, or unclear, but those are adversarial-review territory, not this reviewer's. Drop the candidate.

The motivation: ambiguity is, by definition, **multi-readable**. A reader who only finds one reading isn't doing the review carefully — they're rubber-stamping their own first interpretation. Forcing the reviewer to articulate ≥2 readings before logging the finding breaks the rubber-stamp habit. False positives are still possible (the consultant can strike them at Revise time); false negatives are reduced because the discipline is structural, not motivational.

---

## Upstream input contract

The reviewer reads:

- `requirements/source-manifest.json` (the manifest enumerating consumable input files; read once at the parent reviewer's Step 2).
- For each manifest row whose `tier != "Unsupported"`: the file at `original_path` (for `Native-text` / `Native-multimodal`) or `converted_sibling` (for `Supported-via-MCP`). Read once by the parent at Step 3.
- `framework/assets/characters/ambiguity-inputs-review.md` (the character — loaded once at activation).
- `framework/assets/reviews-inputs/ambiguity-reference.md` (this file — loaded once at activation).

The reviewer does **not** read:

- `requirements/requirements.md`, `requirements/requirements-draft.md`, `requirements/consultant-answers.md`, `requirements/draft-claims*.ndjson` — derivative artefacts; the review's contract is to critique the raw inputs themselves.
- `review-inputs/ADVERSARIAL/adversarial-review.html` even when present — each input-pipeline lens is independently grounded in the manifest; cross-reading would conflate adversarial's defect taxonomy with this reviewer's linguistic taxonomy.
- `analyse-requirements/*` or `analyse-inputs/*` outputs — derived; each lens reads the manifest independently.
- `design-system/*`, `review-requirements/*`, `framework/state/*`, `framework/shared/*` (except as textual references in this document) — out of scope.

---

## The seven ambiguity dimensions

Seven dimensions, swept **sequentially** (one per agent step, in dimension order). Cross-dimension consolidation in Step 11 of the agent collapses same-span multi-dimension hits into single multi-tag findings, so the per-dimension sweeps can be lenient on overlap.

The dimensions are tuned for **raw consultant inputs** (briefs, decks, transcripts, screenshots) — they overlap but do not coincide with the four-category linguistic taxonomy or with the nine-smell operational checklist; each dimension has a sharp test the reviewer can apply without consulting the others.

### Dimension 1 — Lexical ambiguity

**Question:** Is there a single word in the corpus that carries ≥2 plausible meanings in context, where each meaning would produce a different requirement downstream?

**What to check:**

- Domain-overloaded words: `system` (the application? the database? the OS? the integrated platform of N components?), `user` (end-user? admin? authenticated session? user-record?), `report` (PDF? on-screen dashboard? scheduled export? data-warehouse query?), `service` (HTTP endpoint? microservice? human-staffed service?), `client` (customer-organisation? customer-employee? technical client library?).
- Polysemous verbs used as nouns or vice versa: `record` (the entity, the action of recording), `change` (the verb, the noun for a delta).
- Words inherited from one team's jargon and used by another team with a different meaning: `account` (finance? auth? CRM?), `order` (purchase order? sort order?), `field` (form field? database column? business domain?).

**What is NOT a Dimension 1 finding:**

- A word that has only one plausible meaning in context — even if its dictionary entry has multiple senses. Lexical ambiguity is about **plausible** alternative readings in **this corpus**, not abstract polysemy.
- A word used inconsistently across sources (that's Dimension 3 or a downstream consistency issue, not lexical ambiguity in a single span).

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"The system shall allow users to manage their account."*
>
> **Three plausible readings of `account`:**
> (a) An authentication account (login credentials, password, MFA).
> (b) A billing/finance account (invoice history, payment methods, subscription).
> (c) A CRM account (the company the user works for, used in B2B contexts).
>
> Different readings produce wildly different requirements. Flag.

**Worked example — near-miss (do NOT flag):**

> Source: `interview-transcript.md`
>
> *"The user logs in, navigates to settings, and clicks 'Update profile'."*
>
> `User` here has only one plausible reading in context (the authenticated end-user performing the action). Do not flag — the surrounding verbs (`logs in`, `navigates`, `clicks`) anchor the reading.

### Dimension 2 — Syntactic ambiguity

**Question:** Does any sentence in the corpus admit ≥2 grammatical parses, each producing a different requirement?

**What to check:**

- **Coordination scope.** `A and B with C` — does `C` attach to `B` only or to `A and B`? Example: *"export users and reports with audit fields"* — audit fields on reports only, or on both?
- **Attachment ambiguity.** *"The form for users that submit complaints"* — does `that submit complaints` modify `users` or `form`?
- **Conjunction grouping.** *"either A or B and C"* — `(A or B) and C` vs `A or (B and C)`.
- **Negation scope.** *"The system shall not log passwords or session tokens"* — is the prohibition on both, or only on passwords (with session-token-logging unaffected)?

**What is NOT a Dimension 2 finding:**

- A sentence that is grammatically unambiguous but stylistically awkward — that's editorial preference, not ambiguity.
- A long sentence that's hard to read but admits only one parse.

**Worked example — positive find:**

> Source: `whiteboard-photo.png` (transcribed)
>
> *"Notify managers and external auditors with read-only access."*
>
> **Two plausible parses:**
> (a) Notify (managers) and (external auditors with read-only access) — only the auditors have read-only access.
> (b) Notify (managers and external auditors) with read-only access — both groups have read-only access.

**Worked example — near-miss:**

> Source: `workshop-notes.md`
>
> *"Users can edit their own profile or admin profiles."*
>
> This sentence has only one plausible parse (users can edit their own profile, OR admin profiles). The scope of `their own` is clear (binds to the first `profile`); it does not extend to `admin profiles`. Do not flag.

### Dimension 3 — Referential ambiguity

**Question:** Does any pronoun or demonstrative (`it`, `this`, `that`, `they`, `these`, `those`, `the former`, `the latter`) in the corpus have ≥2 plausible antecedents?

**What to check:**

- Pronouns where the preceding sentence introduces multiple candidate antecedents.
- Demonstratives (`this`, `that`) used as standalone subjects where the referent is a prior **clause** or **concept**, not a noun phrase.
- Cross-paragraph references that span source boundaries (a `they` in workshop-notes.md whose plausible antecedents are introduced in brief.docx).
- Implicit subjects in agentless passive constructions (covered also in Dimension 7, but the referential-ambiguity angle is distinct: who is the actor?).

**What is NOT a Dimension 3 finding:**

- A pronoun whose antecedent is unambiguous from the immediately preceding noun phrase.
- A demonstrative whose referent is the entire prior sentence and where any sub-component reading produces the same requirement.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"The form validates the email field. It must be submitted within 30 seconds."*
>
> **Two plausible antecedents for `it`:**
> (a) The form (the whole form has a 30-second submission timeout).
> (b) The email field (the field has a 30-second auto-submit-on-blur).
>
> A third reading — `it` refers to the validation step — is less plausible but not impossible.

**Worked example — near-miss:**

> Source: `interview-transcript.md`
>
> *"Each user has a profile. They can edit it from the settings page."*
>
> `They` resolves to `users` (the only plural antecedent); `it` resolves to `profile` (the only singular antecedent). Do not flag.

### Dimension 4 — Vague predicates

**Question:** Does any adjective, adverb, or quantifier in the corpus admit borderline cases — i.e., a competent reader cannot tell whether a given case satisfies the predicate?

**What to check:**

- **Fuzzy speed/time:** `fast`, `quickly`, `slow`, `slowly`, `soon`, `recent`, `eventually`, `near real-time`, `real-time` (without a latency budget).
- **Fuzzy size/volume:** `large`, `small`, `many`, `few`, `lots of`, `several`, `a number of`.
- **Fuzzy quality:** `appropriate`, `reasonable`, `acceptable`, `adequate`, `sufficient`, `proper`.
- **Fuzzy ease:** `easy`, `user-friendly`, `straightforward`, `simple to use`, `effortless`.
- **Fuzzy reliability:** `reliable`, `robust`, `stable`, `resilient` (without an SLO or failure-rate target).

**What is NOT a Dimension 4 finding:**

- A vague predicate with an explicit threshold nearby in the same sentence/paragraph (e.g., *"fast (≤200ms p95)"* — the threshold resolves the vagueness).
- Vague subjective qualifiers (`intuitive`, `modern`, `world-class`) — those belong to Dimension 5.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"The system shall respond quickly under normal load."*
>
> **Three plausible thresholds for `quickly`:**
> (a) `<100ms p99` — human-perceptual instant.
> (b) `<500ms p95` — typical web-app target.
> (c) `<2s p95` — acceptable for batch / dashboard queries.
>
> Each produces a different non-functional requirement.

**Worked example — near-miss:**

> Source: `workshop-notes.md`
>
> *"The system shall respond fast (≤200ms p95) under typical load (1000 concurrent users)."*
>
> `Fast` has an explicit threshold in the same sentence (`≤200ms p95`); `typical load` has an explicit threshold (`1000 concurrent users`). Both vague predicates are resolved inline. Do not flag.

### Dimension 5 — Subjective qualifiers

**Question:** Does any adjective in the corpus carry opinion-laden / marketing content that has no decidable operational meaning?

**What to check:**

- `intuitive`, `user-friendly`, `easy-to-use` (when not paired with a usability metric).
- `modern`, `contemporary`, `up-to-date`, `current` (style judgments).
- `robust`, `enterprise-grade`, `production-quality`, `industrial-strength` (no SLO or test attached).
- `seamless`, `smooth`, `delightful`, `elegant`, `clean`, `polished` (purely aesthetic).
- `best-in-class`, `world-class`, `industry-leading`, `top-tier`, `premier` (comparative without baseline).
- `comprehensive`, `complete`, `thorough`, `extensive` (coverage claims without scope).

**What is NOT a Dimension 5 finding:**

- A subjective term that is operationalised in the same source (e.g., *"intuitive — measured by ≥80% first-time task completion without help"*).
- A measured-but-undefined claim that is actually vague-predicate (Dimension 4) — e.g., `large` is Dim 4, `enterprise-grade` is Dim 5; the cue is *opinion-laden* vs *fuzzy-quantitative*.

**Worked example — positive find:**

> Source: `deck.pdf` (converted)
>
> *"The UI must be intuitive and modern."*
>
> **Three plausible operational readings of `intuitive` / `modern`:**
> (a) Intuitive = ≥80% of first-time users complete the core task without help; modern = uses 2024–2026 design conventions (cards, glassmorphism, dark mode).
> (b) Intuitive = task-completion time within 1.2× of expert baseline; modern = follows the company's existing design system.
> (c) Intuitive = no training video needed; modern = avoids skeuomorphism and bevels.

**Worked example — near-miss:**

> Source: `brief.docx`
>
> *"The UI should target Nielsen heuristic-evaluation score ≥4/5 on first usability test."*
>
> The qualifier is operationalised (Nielsen heuristic + target score + test point). Do not flag.

### Dimension 6 — Weak / non-specific verbs

**Question:** Does any verb in the corpus abstract over the actual operation, where ≥2 plausible operations would each produce a different requirement?

**What to check:**

- `support` — read? write? read+write? validate? render? convert? accept-and-discard?
- `handle` — process? respond to? log? queue? reject? swallow?
- `manage` — create? read? update? delete? configure? administer?
- `deal with` — same as handle, but vaguer.
- `process` — transform? validate? store? forward? compute?
- `facilitate` — provide a UI for? automate? expose an API for? remind users to?
- `enable` — make possible at all? make easy? make required? make default?
- `provide` — return as data? render as UI? expose as API? document?

**What is NOT a Dimension 6 finding:**

- A weak verb paired with a specific direct object that resolves the operation (e.g., *"the system shall manage user sessions: create on login, refresh every 30 minutes, delete on logout"* — the colon and clauses operationalise `manage`).
- Common verbs (`store`, `read`, `validate`, `display`, `compute`, `notify`) that are sufficiently specific for the context.

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"The system must support multiple file formats."*
>
> **Four plausible operations for `support`:**
> (a) Read (parse and display content) but not write.
> (b) Read and write (round-trip preserved).
> (c) Validate (check format conformance) only — no rendering, no editing.
> (d) Convert (transform one format to another on import).

**Worked example — near-miss:**

> Source: `interview-transcript.md`
>
> *"The system manages user sessions: it creates a session on login, refreshes the token every 15 minutes, and deletes the session on logout or after 8 hours of inactivity."*
>
> `Manages` is operationalised by the three clauses that follow. Do not flag.

### Dimension 7 — Optionality + agentless passive

**Question:** Does the corpus use weak modal verbs (`may`, `might`, `could`, `should-as-non-MUST`, `if possible`, `as required`, `when appropriate`) on what should be hard requirements, or agentless passive constructions that drop the actor?

**What to check:**

- **Weak modals on commitments.** *"The system may encrypt PII at rest"* — `may` permits the system to never encrypt, which collapses testability. RFC 2119 reserves `MAY` for genuine optionality; in elicitation material, weak modals frequently leak from "consultant brainstorm" to "stated commitment" without rewriting.
- **Hedge phrases.** *"if possible"*, *"as required"*, *"when appropriate"*, *"as needed"*, *"where applicable"*, *"if feasible"* — the system has discretion to decide the trigger condition, which makes the requirement untestable.
- **Agentless passive.** Passive constructions that drop the actor: *"data shall be encrypted"* (by whom — the application layer, the DB, the OS, a sidecar?), *"the user shall be notified"* (by email, SMS, in-app, push?). Passives **with** an explicit agent (*"data shall be encrypted by the application before persistence"*) are not flagged.
- **Cross-source modal drift.** Source A says *"must encrypt"*, source B says *"should encrypt"* — flag the inconsistency (this is a Dimension 7 finding because the modal-strength disagreement collapses the requirement, not a cross-source-conflict finding).

**What is NOT a Dimension 7 finding:**

- Genuine optionality (e.g., a brief explicitly lists *"phase-2 nice-to-haves"* and uses `may` to mark them).
- Passives with explicit agents.
- `should` used in the RFC-2119 sense alongside `must` and `may` (when the corpus shows the consultant is using the three-level modal taxonomy deliberately).

**Worked example — positive find:**

> Source: `brief.docx`
>
> *"PII data should be encrypted at rest."*
>
> **Three plausible enforcement strengths and actors for `should be encrypted`:**
> (a) `MUST per RFC 2119`, by the application before write — hard requirement.
> (b) `SHOULD per RFC 2119`, by the database via TDE — log exception if disabled.
> (c) `MAY`, by the OS via disk-level encryption — purely informational; consultant was brainstorming.
>
> Also: the actor is dropped (`be encrypted` — by what layer?), which is a second Dimension 7 angle on the same sentence (consolidation in Step 11 keeps it as one finding with both dimension hits).

**Worked example — near-miss:**

> Source: `workshop-notes.md`
>
> *"The application MUST encrypt PII fields (first_name, last_name, ssn, email) before INSERT, using AES-256-GCM with key rotation every 90 days."*
>
> The modal is explicit (`MUST`), the actor is named (the application), the algorithm and rotation are specified. Do not flag.

---

## Finding schema

Every finding has all eight fields populated, in this order:

```
ID:                    AMB-NN              (sequential per run, zero-padded — AMB-01, AMB-02, …)
Dimension(s):          1..7                (multi-tag findings from Step 11 carry a sorted list e.g. [4, 6])
Severity:              Blocker | Major | Minor
Location:              <filename>          (the manifest row's `filename` field — basename + extension)
Evidence:              direct verbatim quote from the cited source, ≤5 lines
Interpretations:       list of ≥2 plausible readings, each producing a different requirement
Problem:               one sentence — what is ambiguous and why it matters downstream
Elicitation question:  one sentence — ready-to-paste question for the stakeholder, ends with `?`, names the source filename
```

**Field rules:**

- **ID** is unique per run and reset to `AMB-01` on every fresh invocation. Revise loops keep their IDs; only Restart resets the sequence. The pipeline is **full overwrite** per run.
- **Dimension(s)** is a non-empty list of integers in [1, 7]. A single-dimension finding has a list of length 1; a multi-tag finding (output of Step 11 consolidation) has length ≥2. The list is sorted ascending. The **primary dimension** for sorting/ID purposes is the lowest entry.
- **Severity** is exactly one of three. No "Critical" or "Trivial".
- **Location** is the manifest row's `filename` field — basename plus extension (e.g., `brief.docx`, `workshop-notes.md`, `whiteboard-photo.png`). **No line numbers**, no section anchors.
- **Evidence** is a verbatim quote from the cited source's `text` field as captured by the parent reviewer into the corpus. Do not paraphrase. If the offending text is longer than 5 lines, decompose the finding into multiple findings each citing a ≤5-line slice.
- **Interpretations** is a list of ≥2 entries, each being a parenthesised letter `(a)`, `(b)`, `(c)` followed by a one-sentence operational reading. The ≥2-interpretations rule is the methodology's central discipline — if you cannot produce two readings, the candidate isn't ambiguous; drop it.
- **Problem** is one sentence stating which dimension fired and why the ambiguity matters. *"`brief.docx` uses `quickly` (vague predicate, dimension 4) on a core NFR — different readings yield latency targets between 100ms and 2s"*. Not *"this is unclear"*.
- **Elicitation question** is a one-sentence stakeholder-facing question. Must end with `?`, must contain the Location field's filename, must be specific enough that a one-sentence answer resolves the ambiguity, must not embed one of the candidate interpretations as the expected answer (non-leading).

A finding missing any field is invalid. Step-13 gate 1 enforces this.

---

## Severity rubric

The reviewer assigns exactly one severity per finding using this rubric. Severity drives the triage callout and the verdict mapping.

### Blocker

- The ambiguity will cause **divergent implementation** — different developers reading the input will build incompatible features.
- Typical patterns:
    - Vague predicate on a core NFR (latency, throughput, retention, availability).
    - Weak modal on a security or compliance requirement (encryption, audit logging, access control, POPIA/GDPR).
    - Agentless passive on a data-flow boundary (who encrypts? who validates? who routes?).
    - Lexical ambiguity on an entity name appearing across multiple sources (different readings of `account` in three different sources = three different data models).
    - Weak verb on a financial / regulatory operation (`handle refunds`, `manage compliance`).

### Major

- The ambiguity will require a **clarification round** before implementation, but isn't fatal.
- Typical patterns:
    - Vague predicate on a non-core metric (e.g., a dashboard refresh frequency).
    - Subjective qualifier on a UI element (e.g., `the dashboard must be intuitive`).
    - Referential ambiguity on a non-critical-path workflow.
    - Weak verb on a non-core operation (e.g., `support notifications` where the notification channel is settled but the trigger logic isn't).
    - Coordination/scope ambiguity on a feature list (audit fields on which entities?).

### Minor

- **Stylistic.** The ambiguity could be resolved by inference or convention, but flagging it produces a cleaner spec.
- Typical patterns:
    - Weak verbs on non-core operations (`facilitate user onboarding`).
    - Vague quantifiers on diagnostic / debug content (`log many events`).
    - Pronoun antecedents that are clear from context but technically have ≥2 candidates.
    - Mild subjectivity on internal-facing documentation.

### Severity → Verdict mapping

The artefact's Executive Summary states one verdict:

| Verdict | When |
|---|---|
| `BLOCKED` | At least one `Blocker` severity finding exists. |
| `NEEDS-REVISION` | No Blockers, but ≥1 finding total. |
| `ACCEPTED-WITH-NOTES` | Zero findings on all seven dimensions, **and** every dimension carries a non-empty Justification block. (Rare — the seven-dimension surface area is wide; clean runs typically only occur on small, heavily-glossaried corpora.) |

There is no fourth verdict. "Looks good" is not a verdict.

---

## Cross-dimension consolidation rule (Step 11 of the agent)

A single source span can trip multiple dimensions: *"the system shall handle large files efficiently"* trips dimension 4 (vague: `large`, `efficiently`) and dimension 6 (weak verb: `handle`). The consolidation rule:

1. After the seven sequential sweeps emit candidate findings (Step 4–10), walk the candidate list and look for findings whose Evidence spans overlap by ≥80% (using the shorter span as the denominator).
2. Merge overlapping findings into a single multi-tag finding:
    - `dimensions` becomes the sorted-distinct list of all overlapping findings' dimension values (e.g., `[4, 6]`).
    - `interpretations` becomes the concatenation of overlapping findings' interpretations (de-dup by exact-string match).
    - `Problem` becomes a single sentence concatenating the per-dimension problem clauses with `; ` separators.
3. The merged finding's **primary dimension** (for ID-ordering, severity tally, and per-dimension section assignment) is the **lowest** entry in `dimensions`. The merged finding renders once in the primary dimension's per-dimension section; the other dimension sections do not re-list it (Step 13 gate 9's row-count accounting depends on each finding counting once against its primary dimension).
4. The Findings Table renders the multi-tag finding's `Dim(s)` column as a bracketed list (e.g., `[4, 6]`).

The consolidation is **not** clustering (which adversarial-review uses for navigation). Consolidation collapses **identical-span overlaps** within the same source; clustering groups **different-span thematically-related findings** across sources. Ambiguity-review does not cluster — the seven-dimension structure already provides natural navigation.

---

## The ≥2-interpretations test

The discipline's load-bearing rule. Before logging any candidate finding, the reviewer must produce ≥2 plausible interpretations of the cited span, each of which would generate a **different requirement** downstream.

**Plausible** means:

- The interpretation is consistent with the surrounding text.
- The interpretation is the kind of reading a competent developer or business analyst would entertain.
- The interpretation is **different in substance** from the others — not synonymous phrasings.

**Examples of failing the test (drop the candidate):**

- *"`brief.docx` says 'users can edit their profile'"* — only one reading (the authenticated user edits their own profile). Drop.
- *"`brief.docx` says 'the system supports OAuth 2.0'"* — only one reading (OAuth 2.0 as defined by RFC 6749 is implemented for authentication). Drop. (If the corpus omits which grant types are supported, that's a different kind of finding — *missing* specificity, not ambiguity — and belongs in the adversarial-review, not here.)
- *"`brief.docx` says 'the form has 5 fields'"* — only one reading. Drop.

**Examples of passing the test (keep the candidate):**

- *"`brief.docx` says 'the system shall handle reports'"* — at least three readings: render, generate, archive. Keep.
- *"`brief.docx` says 'PII may be encrypted at rest'"* — at least two readings: optional with logging-on-skip, hard requirement misphrased. Keep.

The ≥2-interpretations test is reapplied **during** Step 4–10 sweeps (drop the candidate when only one reading exists) and **enforced** at Step 13 gate 6 (Interpretations list has ≥2 entries).

---

## Elicitation-question authoring rules

The Elicitation question field is what makes ambiguity-review actionable beyond a punch-list — it gives the consultant a ready-to-paste question for the stakeholder. Four rules govern its composition (enforced at Step 13 gate 7):

1. **Specific enough that a one-sentence answer resolves the ambiguity.** *"In `brief.docx`, what p95 response time, in milliseconds, defines 'quickly'?"* is specific (the answer is a number). *"What did you mean by 'quickly'?"* is open-ended (the answer might be a 500-word essay; that's an interview, not a clarification).
2. **Ends with `?`.** A clarification question that doesn't end with a question mark is not a question. Step 13 gate 7 enforces this syntactically.
3. **References the source filename.** *"In `brief.docx`, ..."* / *"In `workshop-notes.md`, ..."*. The stakeholder needs to know which document the question is about, and gate 7 enforces the filename appears in the question text (substring match).
4. **Non-leading.** The question must not embed one of the candidate interpretations as the expected answer. Bad: *"In `brief.docx`, when you said 'quickly', did you mean `<500ms p95`?"* (leads the stakeholder to confirm one interpretation). Good: *"In `brief.docx`, what p95 response time, in milliseconds, defines 'quickly' under normal load?"* (asks the stakeholder to specify; the interpretation list is the reviewer's hypothesis, not the question's framing).

For multi-tag findings (Step 11 output), the elicitation question addresses the strongest dimension first, or — when severities tie — produces a compound question naming both dimensions:

> *"In `brief.docx`, for the phrase 'handle large files efficiently': what specific operation does 'handle' perform on which file size (in MB), with what latency budget?"*

---

## Quality gates (run after Dimension 7, before write)

Ten gates. All are hard. If any gate fails, the reviewer does **not** write the artefact — it surfaces a structured error via `AskUserQuestion`. See `framework/agents/reviews-inputs/ambiguity-reviewer.md > Step 13` for the halt contract.

1. **Every finding has all eight schema fields populated.** Missing-field findings are invalid.
2. **Every finding's Dimension(s) is exactly one integer 1–7 (for single-dimension) or a sorted-distinct list of ≥2 integers in [1, 7] (for multi-tag).** No dimension 0; no dimension 8+.
3. **Every finding's Severity is exactly one of `Blocker | Major | Minor`.**
4. **Every finding's Evidence is verbatim from `quote_index_by_filename[location]`** — substring match against the cited source's content as captured by the parent reviewer into the corpus. Paraphrased or fabricated evidence is a gate failure.
5. **Every finding's Location matches a `corpus[*].filename`.** Citations to non-corpus filenames are a gate failure. Findings citing `Unsupported`-tier filenames are not permitted — those files have no content for the reviewer to ambiguity-check.
6. **Every finding's Interpretations list has ≥2 entries.** This enforces the ≥2-interpretations test at the artefact-validation layer.
7. **Every finding's Elicitation question ends with `?` and contains the Location filename as a substring.** Step 13 gate 7 is a syntactic check; the four authoring rules above are the spirit, gate 7 is the enforceable letter.
8. **Every dimension has ≥1 finding or a non-empty Justification block ≥3 sentences citing specific evidence and naming at least one filename from the corpus.** Silent zero-finding dimensions are a methodology violation.
9. **The Findings Table row count equals the sum of per-primary-dimension finding counts.** Multi-tag findings count once, against their primary dimension. Drift is a render bug.
10. **The artefact's `MANIFEST_FINGERPRINT` field equals the SHA-256 of `requirements/source-manifest.json` captured at Step 2, AND every Source-roster (Consumed) `sha256[:8]` matches its manifest row's `sha256` field.** Mismatch means the artefact reviewed one version of the input set and reports against another.

---

## Output presentation

The artefact renders as a self-contained HTML report (the reviewer substitutes pre-escaped values + pre-rendered HTML fragments into `framework/assets/reviews-inputs/template-ambiguity.html`; one inline `<style>`, no external CSS/JS/fonts). The per-block HTML schemas (triage table, ambiguity register, findings table, per-dimension finding `<article>`s, elicitation groups, source roster, diagnostics `<details>`) live in the template's leading comment. The fixed section ordering is:

1. **Header (Overview)** — title (`<h1 id="top">` + `<title>`) + a `dl.meta-grid`: Domain, Generated-at timestamp, Manifest SHA-256, sources-consumed/skipped counts, reviewer identity.
2. **Executive Summary** — total findings, severity tally, single-sentence verdict (a `<span class="verdict verdict-{VERDICT}">` banner).
3. **Triage** — *"Top issues to address first"* callout (≤10 entries: every Blocker plus highest-impact Majors per the deterministic selection rule).
4. **Ambiguity Register** — the load-bearing table, keyed by ambiguity type (the seven dimensions): one row per finding carrying ID, Type(s), Severity, Location, Evidence, ≥2 Interpretations, and a ready-to-paste stakeholder question. Sorted Blocker → Major → Minor, then ambiguity type ascending, then AMB-NN.
5. **Source roster** — Consumed + Skipped tables.
6. **Findings Table** — compact tabular view of every finding (ID, Dim(s), Sev, Location, one-line problem), sorted Blocker → Major → Minor.
7. **Per-Dimension Sections (1–7)** — full findings for each dimension (finding `<article>`s), or a Justification block if zero findings + ≥3-sentence justification provided.
8. **Suggested elicitation questions** — grouped by source filename, one `<ol>` per filename. This is the section the consultant pastes into the client follow-up.
9. **Diagnostics** — a collapsed `<details>`: quality-gate results, coverage map, override log, run history.

The artefact is a punch-list + action list, not a narrative. Prose between findings is minimised; the consultant should be able to read the Triage callout in under two minutes, scan the ambiguity register keyed by type, jump to the per-dimension section for context on any finding, and copy the elicitation-questions section into a client email in one selection.

---

## Anti-patterns

- **Logging a candidate without ≥2 interpretations.** The ≥2-interpretations test is the methodology's load-bearing rule. If you cannot produce two readings, the candidate isn't ambiguous — drop it (or escalate to adversarial-review, where *missing* specificity is the right framing).
- **Fabricating evidence.** Every Evidence field must be a verbatim quote from the cited source's corpus entry. If you cannot find a quote, you do not have a finding.
- **Generic findings.** *"`brief.docx` is unclear"* is not a finding. Cite the specific span, list the specific interpretations, propose the specific elicitation question.
- **Inflating severity.** Reserve Blocker for ambiguities that will cause divergent implementation. A vague predicate on a marketing tagline is not a Blocker.
- **Collapsing severity into binary.** Severity drives triage. Blocker/Major/Minor is a three-bucket prioritisation, not "important / not".
- **Inline `[SRC: ...]` markers in findings.** The Evidence + Location pair is the citation; do not duplicate it in Problem, Interpretations, or Elicitation question.
- **Generating leading elicitation questions.** *"Did you mean X?"* primes the stakeholder. Ask *"What is X?"* instead — the interpretation list is the reviewer's hypothesis, not the question's framing.
- **Citing `Unsupported`-tier filenames.** Those files have no content for the reviewer to ambiguity-check. If a stakeholder mentions an ambiguous term only in a skipped file, the ambiguity is downstream of conversion failure — surface the skip in adversarial-review's Dim 1, not here.
- **Skipping cross-dimension consolidation.** A sentence tripping dimensions 4 and 6 must emit one finding with `dimensions: [4, 6]`, not two duplicate findings. Step 11 of the agent handles this; bypassing it produces double-counting in gate 9.
- **Reviewing against the synthesised requirements doc.** Do not consult `requirements/requirements.md` or any other `/requirements`-pipeline derivative. The review's contract is to critique the **raw inputs**.
- **Reviewing against parallel reviews.** Do not consult `review-inputs/ADVERSARIAL/adversarial-review.html` to triangulate findings. Each input-pipeline lens is independently grounded in the manifest.
- **Line numbers in Location.** The Location field is `filename` only.
- **Skipping the strict-Justification rule.** A dimension with zero findings requires a non-empty Justification block ≥3 sentences. *"Clean"* is not a Justification.

---

## Voice and stance

The reviewer's stance is defined in `framework/assets/characters/ambiguity-inputs-review.md` — linguist-skeptical, taxonomy-bound, evidence-required, ≥2-interpretations test, no rubber-stamping. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

---

## References

- **Berry, D. M. & Kamsties, E. (2004).** *Ambiguity in Requirements Specification.* In: *Perspectives on Software Requirements* (Springer). The canonical four-category linguistic taxonomy (lexical, syntactic, semantic, pragmatic) plus the separately-treated vagueness and generality categories. This reference's Dimensions 1, 2, 3, 4 are direct descendants; Berry/Kamsties' semantic category is split into referential (Dim 3) and vague-predicate (Dim 4) for operational sharpness.
- **Femmer, H. et al.** *Rapid Quality Assurance with Requirements Smells.* Plus the Smella tool (a POS-tag + lemmatisation rule-based detector for nine smells: anaphora, coordination ambiguity, vagueness, passive voice, referential integrity, subjectivity, nocuous ambiguity, multiple interpretations, consistency). This reference's Dimensions 5, 6, 7 are direct descendants — Femmer's subjective, weak-verb (Smella categorises as part of vagueness), and optionality/passive smells.
- **DEAR: DEtecting Ambiguous Requirements as a Way to Develop Skills in Requirement Specifications** (MDPI Electronics, 2024). Empirical evidence that structured taxonomy training + worked examples improves reviewer agreement on ambiguity classification. The two-worked-examples-per-dimension structure of this reference is informed by DEAR's pedagogical findings.
- **A Short Survey on Formalising Software Requirements with Large Language Models** (arXiv, 2024). Empirical evidence that LLMs achieve ~20% lift on ambiguity classification when prompted with in-context demonstrations of each ambiguity type. The decision to inline 2 worked examples per dimension in this reference (rather than abstract category descriptions only) is grounded in this finding.
- **Reducing Requirements Ambiguity via Gamification: Comparison with Traditional Techniques** (PMC, 2022). Comparative study showing taxonomy-trained reviewers outperform free-form reviewers on inter-rater agreement.
- **IEEE Std 830 — Recommended Practice for Software Requirements Specifications.** The eight quality attributes (correct, unambiguous, complete, consistent, ranked, verifiable, modifiable, traceable) underpin the structure of input-side ambiguity review; this reference operationalises the *unambiguous* attribute applied to the inputs themselves.
- **RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels.** The three-level modal taxonomy (MUST / SHOULD / MAY) underpins Dimension 7's distinction between weak modals (collapse testability) and explicit-strength modals (do not).
- **Sibling reference for broader input critique:** `framework/assets/reviews-inputs/adversarial-reference.md` — applies a seven-dimension BMAD-style critique to the same input set. Adversarial's Dimension 3 (Ambiguity & Vague Language) overlaps this reference at a coarser grain; the two methodologies are complementary, not substitutes.
