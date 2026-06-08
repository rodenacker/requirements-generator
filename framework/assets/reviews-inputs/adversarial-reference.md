<!-- ROLE: asset (P2 review reference). Loaded by framework/agents/reviews-inputs/adversarial-reviewer.md at activation. -->

# reviews-inputs/adversarial-reference.md

**Purpose:** Methodology reference for Adversarial Review of the **raw consultant input set** enumerated by `requirements/source-manifest.json`. The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews-inputs/adversarial-reviewer.md` — drives the agent's six-dimension process plus the quality-gate sweep.

**Output produced by the reviewer:** `review-inputs/ADVERSARIAL/adversarial-review.html` — a self-contained HTML punch-list of cited, severity-graded, dispositioned findings using `framework/assets/reviews-inputs/template-adversarial.html` as scaffold. The HTML ships with an inlined `<style>` block, a sticky TOC, severity/disposition colour-coded chips, and back-to-top links after every H2 section; it opens directly via `file://` and prints sensibly via the browser's native Print dialog.

**Sibling lens:** `framework/assets/reviews/adversarial-reference.md` runs the same methodology against the synthesised `requirements/requirements.md` after `/requirements` has produced it. The two references are complementary, not redundant — this one critiques the *source of truth*; the sibling critiques the *derivation*. Fixing input-set defects shifts ground truth; fixing finished-doc defects only re-litigates whatever the inputs already let through. The dimensions, examples, and citation format differ; the BMAD rule, finding schema, disposition rubric, clustering, triage, and verdict mapping are preserved.

---

## Principle: the input corpus IS the stakeholder voice

This methodology starts from a single contract: **the raw input set IS the stakeholder voice.** It is not evidence-of-elicitation; it is the elicitation. There is no further corpus to compare against, no other interview to schedule, no second sample to balance the first. The voice is whatever the corpus says, in whatever shape it says it.

Four implications follow:

1. **Silences are silences, not elicitation gaps.** A role mentioned without a direct-quote source, an entity referenced without field-level detail, a workflow named without supporting material — each stands as a finding about *what the voice did not say*, not as a request for more documents. Recommendations propose how `/requirements` and downstream consumers must handle the silence (apply a `GR-NN` default, mark `[OUT-OF-SCOPE]`, surface as `[AI-SUGGESTED]` assumption), not how to expand the corpus.
2. **Recommendations are corpus-handling actions, not elicitation actions.** Five sanctioned forms only (see *Finding schema > Recommendation*). Never *"schedule an interview"*, *"elicit X"*, *"go ask the stakeholder"* — there is no second visit; the corpus is what the voice said.
3. **Reject narrows.** Reserved for internal-corpus defects downstream cannot resolve via defaults — cross-source factual contradiction on a load-bearing concept, POPIA / legal scope claim with no in-corpus enumeration, load-bearing ambiguity unresolvable at draft time. Silences alone do not trigger Reject; they are Patch or Defer because downstream can apply defaults.
4. **The sampling / bias lens does not apply.** Critiquing corpus shape (source count, role diversity, time window, tier distribution) as *inadequate* presupposes a should-be larger corpus. There is no should-be — the voice is whatever it is. Corpus-shape data is reported in the Diagnostics block for downstream context, not as findings. (See *Output presentation > Diagnostics > Corpus Shape*.)

This principle changes *what counts as an issue* under the BMAD must-find-issues rule — not whether the reviewer must find one. The strict-BMAD halt rule still fires on zero-finding dimensions; the reviewer still finds defects (ambiguity, contradiction, hedges, silences-with-downstream-impact, second-hand voice mistaken for first-hand); rubber-stamping is still forbidden. What shifts is that the defects live inside the voice the corpus carries — not in the consultant's choice of which interviews to schedule.

---

## What "adversarial review" means

Adversarial Review is the **opposite** of confirmatory review. A confirmatory reviewer asks "do these inputs look reasonable?" and returns "yes, mostly". An adversarial reviewer asks "in how many ways will these inputs produce weak requirements when `/requirements` drafts from them next week?" and returns the list.

The discipline is rooted in the **BMAD method** (Breakthrough Method for Agile AI-Driven Development), an open-source agentic planning framework. BMAD's adversarial-review docs prescribe an uncompromising rule:

> *"Adversarial review is a review technique where the reviewer must find issues. No 'looks good' allowed. Zero findings trigger a halt — re-analysis becomes mandatory or justification required."*

The motivation: confirmation bias makes confirmatory reviewers useless. A reviewer who is permitted to return "clean" will return "clean" on an inadequate input set, because the path of least cognitive resistance is approval. Forcing the reviewer to find issues (or write an explicit, evidenced defense of why none exist) breaks the bias.

BMAD also warns of the symmetric failure mode:

> *"Because the AI is instructed to find problems, it will find problems — even when they don't exist."*

The mitigation is **human filtering**: the consultant's Accept/Revise/Restart loop at handback time. The reviewer is exhaustive; the consultant strikes false positives during Revise. False positives are part of the protocol, not a failure of it.

This reference operationalises BMAD's rule with explicit input-set dimensions, a finding schema, a disposition rubric, and a halt contract.

---

## Upstream input contract

The reviewer reads:

- `requirements/source-manifest.json` (the manifest enumerating consumable input files; read once at the parent reviewer's Step 2).
- For each manifest row whose `tier != "Unsupported"`: the file at `original_path` (for `Native-text` / `Native-multimodal`) or `converted_sibling` (for `Supported-via-MCP`). Read once by the parent at Step 3.
- `framework/assets/characters/adversarial-inputs-review.md` (the character — loaded once at activation by the parent).
- `framework/assets/reviews-inputs/adversarial-reference.md` (this file — loaded once at activation by the parent).
- `framework/assets/reviews-inputs/template-adversarial.html` (the HTML scaffold — read once at render time by the parent).

The reviewer does **not** read:

- `requirements/requirements.md`, `requirements/requirements-draft.md`, `requirements/consultant-answers.md`, `requirements/draft-claims*.ndjson` — derivative artefacts; the review's contract is to critique the raw inputs themselves, not anything `/requirements` has already synthesised.
- `analyse-requirements/*` or `analyse-inputs/*` outputs — derived; reviewing the raw inputs against a parallel analysis of those same inputs conflates "what the source material says" with "what an analyser inferred". The review's contract is to critique the inputs as the inputs.
- `design-system/*`, `review-requirements/*` (including the requirement-doc adversarial review), `framework/state/*`, `framework/shared/*` (except as textual references in this document) — out of scope.

The raw consultant input set is the contract. If the inputs don't say it, the inputs don't say it — and that is a finding. **Inputs re-ingested from `/analyse-inputs` outputs (a thematic-analysis or opportunity-solution-tree artefact re-dropped into `input/`) are part of the input set and are reviewed as such**; they are not skipped or treated specially. The whole point is that the merged input corpus is what `/requirements` will draft from.

---

## The six review dimensions

Six dimensions, executed in order. Each is its own pass; the reviewer does not collapse passes. The dimension-by-dimension structure is what makes the review auditable: every finding maps to exactly one dimension, every dimension reports either ≥1 finding or a Justification block.

The six dimensions are tuned for **raw consultant inputs** — they differ from the eight dimensions of `/review-requirement` adversarial because input-set defects differ from finished-doc defects. Testability does not apply when no requirements exist yet; dependency-ordering does not apply across heterogeneous PDFs / decks / transcripts. The dimensions are re-synthesised from elicitation-quality literature (Wiegers, IIBA BABOK, Volere) plus BMAD's must-find-issues posture — re-framed under the *corpus IS the voice* principle so that the "what to check" remains operational while the "what to recommend" becomes corpus-handling, not elicitation. The seventh dimension that used to live here (Bias, Sampling & Stakeholder Self-Selection) was structurally incompatible with the principle (its premise was that the corpus should-be larger / more diverse — but under the principle there is no should-be); its observability content survives as the **Corpus Shape** subsection of the Diagnostics block.

### Dimension 1 — Stakeholder & Role Coverage

**Question:** Does every role / persona named in the corpus carry *some* supporting material — and where a role is entirely unsupported, is the silence itself flagged so downstream knows what cannot be drafted from the corpus?

**Primary lens — role coverage (load-bearing).** The dimension's central check is *coverage*: does each role the system will serve have at least one source describing its perspective, needs, or permissions, **first- or second-hand**? Where the corpus is silent on a role, the Recommendation form is *Treat as silence* (downstream applies `[OUT-OF-SCOPE: domain-default]` or marks role-specific flows as unsupported by corpus voice).

**Secondary lens — voice authenticity (narrow; do not over-fire).** The corpus is consultant-relayed: the consultant collects whatever the client gives them, so **second-hand voice is the expected norm, not a defect.** A role whose material is second-hand (a brief or deck attributing a position to it) is *not* a finding on those grounds alone — flagging second-handedness across the corpus would fire on nearly every role and drown the review in noise of no downstream consequence. Raise a voice-authenticity finding **only** when *all four* hold:

1. **Load-bearing** — the claim will drive a requirement, a permission, a workflow rule, or a scope cut (not a passing characterisation).
2. **Specific and strong** — a definite assertion (*"Finance Managers require two-eyes approval"*), not a vague mention (*"finance will be involved"*).
3. **No first-hand corroboration** — no interview line, survey response, attributed note, or signed document from that role anywhere in the corpus supports it.
4. **Mis-reading would change the draft** — if downstream took it as established stakeholder fact rather than BA interpretation, `/requirements` would draft something materially different from what it would draft knowing the claim is unconfirmed.

When all four hold, emit **one Minor finding** with Recommendation form *Treat as second-hand* (downstream marks it as BA-interpretation to confirm, not established stakeholder position). Corpus-level provenance mix (how much of the corpus is first- vs second-hand) is descriptive context for the Diagnostics *Corpus Shape* block — never a per-role finding.

*(First-hand sources: interview transcripts, direct quotes, survey responses, signed stakeholder documents, attributed workshop notes, screenshots / mockups the role produced. Second-hand sources: consultant- or BA-authored briefs, executive decks, summary memos, derived analysis artefacts, unattributed notes.)*

**What to check:**

- Every named role or persona has at least one source describing its perspective — first- *or* second-hand. A role with **no** supporting material of any kind is a coverage silence (Recommendation form *Treat as silence*).
- The corpus reflects the role categories that will use the system: end-users (often multiple sub-roles by job function), administrators / power users, operators / support staff, auditors / compliance officers, regulators if applicable, integration partners if external systems are involved. A whole category absent is a coverage silence.
- Skipped-source visibility: if a role is mentioned only in an `Unsupported`-tier file (e.g., `proposal.pages`), the corpus does not currently surface that voice; flag as a coverage finding citing the skipped filename, Recommendation form *Treat as silence*.
- Voice authenticity (narrow): scan only for the four-part load-bearing case above — a strong, specific, draft-driving claim attributed to a role with zero first-hand corroboration. Do **not** flag a role merely because its only material is second-hand.

**Common failure modes to scan for:**

- A role mentioned ("we'll need an admin role") with zero material of any kind defining what admin does — the corpus is fully silent on the role. Recommendation: *Treat as silence*.
- A regulator or auditor role implied by compliance language ("must be POPIA compliant") but no material from any auditor or compliance-officer perspective in the corpus. Recommendation: *Treat as silence* — downstream marks compliance-officer-specific acceptance criteria as unsupported by corpus voice.
- A user-segment mentioned only as a number on a deck slide ("50,000 end-users") with no qualitative material from any of them — the voice is statistical, not utterance. Recommendation: *Treat as silence*.
- **(Narrow voice-authenticity case.)** A brief asserts a *load-bearing* rule — *"Finance Managers require two-eyes approval"* — that a requirement will hinge on, with no first-hand Finance Manager source anywhere in the corpus to confirm it. One **Minor** finding, Recommendation form *Treat as second-hand*: downstream drafts the rule but marks it BA-interpretation to confirm. **Contrast:** a brief merely *naming* "Finance Manager" as a primary user is **not** a finding — second-hand naming is the norm, not a defect.

### Dimension 2 — Domain & Workflow Coverage (including non-happy paths)

**Question:** Does every major workflow named in the inputs have supporting material, and does that material cover what happens when the happy path breaks?

**What to check:**

- Every workflow named in the inputs (in a brief, deck, or interview) has at least one supporting source describing **how it currently runs**: a flow diagram, an annotated screenshot, a transcript walkthrough, a process narrative.
- Every entity referenced in the inputs is grounded by at least one source describing its **shape**: field names, types, cardinalities, sample values. An entity referenced (e.g., "invoice") with no field-level detail in any source is a coverage gap.
- Non-happy-path coverage: the inputs describe what happens when workflows fail — errors, validation failures, empty / max states, concurrent edits, network failures, partial failures, authorization failures, recovery paths. If only happy paths exist, the inputs are insufficient for `/requirements` to draft realistic acceptance criteria.
- Integration touch-points are described with contracts: protocol, payload shape, failure mode for every external system the inputs name (auth, payments, email, SMS, storage, ERP, CRM).
- Volume / scale signals exist for each workflow: typical record count, peak load, growth rate, retention period — at least the qualitative shape, even if no numeric threshold.

**Common failure modes to scan for:**

- A brief listing "approval workflow" as a feature with no transcript or flow describing what approval currently looks like (single approver? two-eyes? escalation chain? what triggers it?).
- An entity ("order") referenced across multiple sources with no source describing its fields, status values, or lifecycle.
- Five screenshots of happy-path user journeys, zero screenshots of error states, validation messages, or empty states.
- A "bulk import" workflow named with no source describing what happens when 3 of 100 rows fail validation.
- Network / offline behaviour never mentioned in any source for a workflow that obviously involves data transfer.

### Dimension 3 — Ambiguity & Vague Language

**Question:** Is the language across the input corpus precise enough that `/requirements` can draft unambiguous requirements from it?

**What to check:**

- Vague verbs across the corpus: "support", "handle", "manage", "deal with", "automate", "streamline", "be aware of", "consider", "leverage". Each instance — verbatim — is a flag.
- Vague nouns when the corpus has a defined entity vocabulary: "stuff", "thing", "item", "data" used where a specific entity exists.
- Vague quantifiers: "many", "few", "some", "frequently", "occasionally", "in some cases", "most of the time".
- Vague time windows: "recent", "soon", "later", "after a while", "in the background", "real-time" (without a latency budget), "near real-time".
- Pronouns with unclear antecedents across paragraphs or sources: "it", "they", "this", "that".
- Hedge words on what are meant to be commitments: "may", "might", "could", "would ideally", "should probably", "we're thinking about".
- Undefined jargon: domain-specific abbreviations or terms used without a definition anywhere in the corpus.
- Marketing / vendor-brochure abstraction copied wholesale into a brief: "best-in-class", "seamless", "intuitive", "world-class" — language with no decidable content.

**Common failure modes to scan for:**

- *"The system should support approval workflow"* — "support" is the vague verb; nothing in the inputs specifies who approves, what triggers approval, what the criteria are.
- *"Reports should be available real-time"* — "real-time" without a latency budget is undefined.
- *"Users will need to manage their settings"* — "manage" + "users" + "settings" all generic.
- *"We're thinking about adding bulk operations"* — hedge ("thinking about") plus undefined scope (which operations? which entities?).
- An interview transcript that uses "the system" twenty times without ever distinguishing between the *current* system and the *future* one.

### Dimension 4 — Source Provenance, Consistency & Conflict

**Question:** Is every source attributable, and do the sources agree with each other on factual claims?

**What to check:**

- Every source is attributable to an identifiable origin: author / role, date, and (where applicable) the meeting or document it comes from. An anonymous brief is weaker than a brief signed by a named stakeholder.
- Aspirational vs current-state material is distinguishable. A screenshot of a current production system is different from a mockup of a future system; if both are in the corpus, each should be tagged. Mockups labelled as current-state are a finding.
- Cross-source conflicts on factual claims: two sources disagree on a role's permissions, an entity's field types, a workflow's steps, a metric's value.
- Entity naming drift across sources: `Order` in the brief, `Purchase Order` in the deck, `orders` in the workshop notes, `PO` in the interview transcript — three or four names for one concept.
- Role naming drift: "Approver" in one source, "Reviewer" in another, "Manager" in a third — for what appears to be the same role.
- Process flow conflicts: source A describes a three-step approval; source B describes a two-step approval; source C describes a single-step approval. The conflict itself is the finding (regardless of which is "right").
- Date-stamped contradictions: an older source claims X; a newer source claims not-X. The newer claim does not silently override the older — the conflict is logged so the consultant can confirm.
- Hedge-laden material: a key claim sourced only from a transcript line beginning *"I think..."*, *"maybe..."*, *"we used to..."* — provenance is weak; flag as a finding.

**Common failure modes to scan for:**

- A brief with no author, no date, no version.
- A mockup PNG in the corpus with no caption distinguishing it from a real screenshot.
- Two interview transcripts where the Finance Manager says approval is "two-eyes" and the Compliance Officer says approval is "single-step", with no source resolving the contradiction.
- An RBAC table on a deck slide that contradicts the role permissions described in an interview transcript.
- The same entity referred to as "Customer", "Account", "Client", and "User" across four different sources, with no glossary anywhere mapping them.

### Dimension 5 — Quantitative & Measurable Signal

**Question:** Does the corpus carry quantitative signal — volumes, latencies, scales, deadlines, success criteria — so `/requirements` can write testable non-functional requirements?

**What to check:**

- NFR signals: peak load (requests / sec, concurrent users), data volume (rows, file size, document count), latency budgets (p50, p95, p99 if mentioned), scale targets (records per year, growth rate).
- Business-metric signals: KPIs the project will be measured against (revenue lift, cost reduction, retention, cycle time, throughput), with current baseline and target.
- Deadline signals: project go-live, regulatory deadline, business-event deadline (year-end, audit cycle).
- Cost / budget signals: rough size of the engagement, team size, infrastructure budget. Missing entirely is a finding; their presence is what makes feasibility findings actionable in Dimension 6.
- Acceptance criteria signals: language in the inputs that says "we'll know it's working when..." — even informal, even qualitative. Total absence is a finding.
- Compliance / regulatory signals with concrete scope: POPIA (South African context — this framework's default target), GDPR, PCI-DSS, HIPAA — with what data, in what retention window, with what consent flow.

**Common failure modes to scan for:**

- A brief that says "the system must be fast" with no latency number anywhere in the corpus.
- A brief that says "scale to 1M users" with no growth-rate signal, no current-user-count baseline, no concurrency model.
- A POPIA reference in passing (*"...must be POPIA-compliant..."*) with no source describing which fields are personal information, what retention is needed, or what consent flow exists today.
- A project with a go-live mentioned ("Q3 next year") and no source naming what "go-live" means (MVP? phase 1? phase 2?).
- An engagement scoped without any team-size or budget signal — making feasibility findings unanchored.

**Scope note.** Many signals here are `backend-only` (peak load, infra capacity, scaling targets, infra budget) — raise them, but they are capped at Step 4s (`Major`, never `Blocker`). Signals with a UI surface stay higher: a missing latency budget that gates a *user-visible* "real-time" expectation is `fe-facing-contract`; POPIA / accessibility scope is `fe-facing-contract` (consent UI, WCAG-driven states). Classify by whether the frontend draft would encode the signal.

### Dimension 6 — Scope & MVP Signal

**Question:** Do the inputs distinguish in-scope from out-of-scope, MVP from post-MVP, must-have from nice-to-have?

**What to check:**

- At least one source explicitly names what is **in scope** for the engagement (or "this phase", "the MVP", "phase 1"). Absent: every feature mentioned is implicitly in scope, which usually means scope creep is encoded in the inputs.
- At least one source explicitly names what is **out of scope**. Untouched topics are not "implicitly out of scope" — they are unaddressed.
- "Nice-to-have", "future", "phase 2", "wishlist" items are tagged as such in the source where they appear. Untagged future items mixed with MVP requirements blur the cut line.
- Cost / time / team-size constraints scope what's buildable: a six-week engagement with three engineers cannot deliver a six-month feature surface. If the inputs name no constraints, scope is unbounded — a finding.
- Roadmap signals exist: a phased plan, a release sequence, a "first we'll do X, then Y" narrative.
- Browser / device / OS targets are named: "Chrome ≥110 desktop" is in scope, "all browsers" is not feasible.
- Accessibility targets are explicit: "WCAG 2.1 AA" is in scope, "accessible" is not testable.

**Common failure modes to scan for:**

- A 30-page brief with no section titled "out of scope" and no equivalent narrative.
- A deck with a "future ideas" or "stretch goals" slide that reads like a second copy of the main feature list, with no separator between MVP and stretch.
- An interview transcript where the consultant says "for the first version we'll keep it simple" and never specifies what "simple" excludes.
- "Mobile-first" in one source and no signal anywhere about whether desktop is in scope or out.
- "Will integrate with existing ERP" with no source naming which ERP, which modules, which version, which protocol.

---

## Finding schema

Every finding has all eight fields populated, in this order:

```
ID:             ADV-NN          (sequential per run, zero-padded — ADV-01, ADV-02, …)
Dimension:      1..6            (which review dimension the finding maps to)
Severity:       Blocker | Major | Minor
Disposition:    Patch | Defer | Reject
Location:       <filename>      (the manifest row's `filename` field — basename + extension)
Evidence:       direct verbatim quote from the cited source, ≤5 lines
Problem:        one sentence — what is wrong/missing/unclear/conflicted in the source material
Recommendation: one sentence — corpus-handling action in one of five sanctioned forms:
                Reconcile in-corpus | Label / annotate | Treat as silence |
                Treat as second-hand | Resolve at draft time. NEVER elicitation.
```

**Field rules:**

- **ID** is unique per run and reset to `ADV-01` on every fresh invocation. Revise loops keep their IDs; only Restart resets the sequence. The pipeline is **full overwrite** per run — each run's artefact reflects only the current input set, with no carried-over findings from prior runs.
- **Dimension** is exactly one integer 1–6. A finding that spans dimensions must be decomposed into one finding per dimension.
- **Severity** is exactly one of three. No "Critical" or "Trivial" or "Cosmetic".
- **Disposition** is exactly one of three (Patch / Defer / Reject). See the rubric below.
- **Location** is the manifest row's `filename` field — basename plus extension (e.g., `brief.docx`, `workshop-notes.md`, `whiteboard-photo.png`, `interview-transcript.md`). **No line numbers**, no section anchors. Multimodal sources have no lines; markitdown-converted siblings re-anchor on `.converted.md` (different from the original); line numbers rot. The audit unit is `<filename>` + verbatim quote ≤5 lines.
- **Evidence** is a verbatim quote from the cited source's `text_or_transcription` content as captured by the parent reviewer into the evidence bundle (Native-text content is the file's bytes; Native-multimodal content is the parent's verbatim transcription of visible text + structural observations). Do not paraphrase. If the offending text is longer than 5 lines, decompose the finding into multiple findings each citing a ≤5-line slice. For `Unsupported`-tier files cited in Dimension 1 (stakeholder mentioned only in skipped file): Evidence is the literal string `*(file skipped — tier: Unsupported; reason: <conversion-failure-reason>)*` — a sanctioned non-verbatim form because the file's content was never read.
- **Problem** is one sentence stating the defect of the voice. *"`brief.docx` asserts the load-bearing rule 'Finance Managers require two-eyes approval' but no first-hand Finance Manager source corroborates it, so downstream would draft the rule as established fact"* — not *"stakeholder coverage gap"*. (Note: a role merely *listed* in a brief is not a finding — second-hand naming is the corpus norm; only load-bearing, draft-changing claims with no first-hand backing fire the narrow voice-authenticity lens.)
- **Recommendation** is one sentence proposing a concrete *corpus-handling* action — what `/requirements` and downstream consumers must do given this defect of the voice. The corpus IS the voice; the reviewer does not propose new elicitation. Five sanctioned forms, exhaustive:
    1. **Reconcile in-corpus** — when two sources contradict (Dim 4), name which source the consultant treats as canonical and which as superseded. *"Treat `interview-2026-03.md` RBAC table as canonical; supersede the older RBAC table in `proposal-deck.pdf` slide 12."*
    2. **Label / annotate** — in-corpus annotation that costs no new elicitation: mark a mockup as aspirational, attribute an anonymous brief, add a glossary entry mapping entity-name drift. *"Label `whiteboard-photo.png` as aspirational (future-state mockup, not current-state screenshot)."*
    3. **Treat as silence** — instruct downstream to apply a default or mark as unspecified. *"Treat as silence — `/requirements` applies the default latency budget from `framework/shared/general-rules.md` and marks the NFR as not-quantified-by-voice."* Most Dim 1, 2, 5, 6 silence findings land here.
    4. **Treat as second-hand** — for a *load-bearing* claim attributed to a role with no first-hand corroboration, instruct downstream to mark as BA-interpretation to confirm, not established stakeholder position. *"Treat `brief.docx` claim 'Finance Managers require two-eyes approval' as BA-interpretation; no first-hand Finance Manager voice in corpus to confirm."* Reserved for the **narrow** Dim 1 voice-authenticity case (load-bearing + specific + no first-hand backing + mis-reading would change the draft); second-hand voice in general is the expected norm in a consultant-relayed corpus, not a defect, so this form does **not** fire on every second-hand-sourced role.
    5. **Resolve at draft time** — surface the defect in the consultant-answers loop during `/requirements` draft for explicit consultant choice. Reserved for load-bearing ambiguities (Dim 3) where downstream cannot apply a default. *"Resolve at draft time — surface 'real-time reporting' to consultant-answers; latency budget is load-bearing and cannot be defaulted."*

  **Forbidden forms:** *"schedule an interview"*, *"elicit X"*, *"interview Y"*, *"workshop with Z"*, *"go ask the stakeholder"*, *"contact the customer"*, *"add an interview transcript"*. The corpus IS the voice; there is no second visit. A finding whose Recommendation falls outside the five sanctioned forms above is a worker self-validation failure (quality gate 5a).

A finding missing any field is invalid. The quality-gate sweep enforces this.

---

## Disposition rubric (BMAD's three buckets)

Identical to the `/review-requirement` adversarial rubric — the rubric is about **defect cost**, not source type. The reviewer assigns exactly one disposition per finding using this rubric:

### Patch

- The defect is **auto-fixable** by the consultant editing or annotating the input material **without new elicitation**.
- Editing effort is **< 15 minutes**: add a missing date to a source, label a mockup as aspirational, rename an entity consistently across sources, attribute an anonymous brief.
- The defect does not require talking to a stakeholder.
- Examples: an anonymous brief that the consultant can re-attribute from their own notes; a mockup that the consultant can label "aspirational"; a glossary the consultant can add for consistent entity naming.

### Defer

- The defect is **real** and **specific**, but downstream can handle it without consultant in-corpus reconciliation — typically by applying a `GR-NN` default, marking `[OUT-OF-SCOPE: domain-default]`, surfacing as `[AI-SUGGESTED]`, or treating a role-claim as second-hand.
- Common pattern: a missing edge-case workflow that affects a post-MVP feature (Recommendation form *Treat as silence*); a role with no corpus material that only matters in phase 2 (*Treat as silence*); a load-bearing second-hand claim for a phase-2 persona (*Treat as second-hand*); an integration whose contract belongs to a later phase (*Treat as silence*).
- Logged as a downstream-handling instruction in the artefact; does not block `/requirements` from drafting the MVP.

### Reject

- **Blocking — but narrowly.** `/requirements` cannot draft from these inputs because the defect cannot be resolved by applying a default, marking a silence, treating a claim as second-hand, or surfacing at draft time. The voice's defect requires consultant in-corpus reconciliation before any downstream interpretation is possible.
- Under the *corpus IS the voice* principle, Reject is reserved for three concrete patterns:
    1. **Cross-source factual contradiction on a load-bearing concept** (Dim 4). Two first-hand sources name different RBAC permissions for the same role, different workflow step counts, different field types for the same entity. No default can pick between them; the consultant must reconcile in-corpus (Recommendation form: *Reconcile in-corpus*).
    2. **POPIA / legal scope claim with no in-corpus enumeration** (Dim 5). A source claims POPIA / GDPR / PCI-DSS / HIPAA compliance but no source enumerates which fields are personal information, which retention applies, which consent flow exists. Legal frameworks that genuinely require explicit enumeration cannot be defaulted via `GR-NN`.
    3. **Load-bearing ambiguity unresolvable at draft time** (Dim 3). An ambiguous claim that downstream consultant-answers cannot resolve without external information (which the principle forbids), AND for which no `GR-NN` default can substitute. Rare — most ambiguities resolve via Recommendation form *Resolve at draft time*.
- **Silences are NOT Reject.** Missing role voice (Dim 1), missing workflow detail (Dim 2), missing latency budget (Dim 5), unbounded scope (Dim 6) — these are **Patch** (in-corpus annotation, label as aspirational, attribute brief) or **Defer** (downstream handles via *Treat as silence* or *Treat as second-hand* Recommendation form). Reject demands consultant in-corpus reconciliation; silence does not — downstream has a default.
- **A `backend-only` finding is never `Reject`** (and never `Blocker`). Per *Purpose-aware scope recalibration*, a defect bearing only on backend / infra / server-side concerns cannot block a **frontend** draft. The three Reject patterns above inherently fire on `fe-relevant` / `fe-facing-contract` concerns (a load-bearing contradiction is load-bearing *for a frontend requirement*; POPIA is `fe-facing-contract`). Should a worker mark a `backend-only` finding `Reject`, Step 4s caps it to `Defer` and re-expresses its Recommendation to *Treat as silence*.
- Any single Reject finding makes the overall verdict `BLOCKED`. This verdict is meaningful precisely because Reject is narrow. (The tally is read **after** Step 4s scope recalibration.)

### Disposition → Verdict mapping

The artefact's Executive Summary states one verdict:

| Verdict | When |
|---|---|
| `BLOCKED` | At least one `Reject` disposition exists, **or** at least one Blocker severity finding exists. |
| `NEEDS-REVISION` | No Rejects/Blockers, but ≥1 finding total. |
| `ACCEPTED-WITH-FIXES` | Zero findings on all six dimensions, **and** every dimension carries a non-empty Justification block. (Rare — strict-BMAD rule below makes this expensive.) |

There is no fourth verdict. "Looks good" is not a verdict.

The disposition and severity tallies that drive this mapping are read **after** the purpose-aware scope recalibration below: a `backend-only` finding can never carry `Blocker` or `Reject`, so it cannot force `BLOCKED` — but it still counts toward `NEEDS-REVISION`.

---

## Purpose-aware scope recalibration

`/requirements` drafts a **frontend** spec from this corpus, and every consumer of that spec is a frontend pipeline. A corpus defect about a backend / infra / operational concern with no UI surface should be **raised, not suppressed**, but rated for what it is: a note that does not block frontend drafting. After the six-dimension sweep merges (Step 4b), the reviewer classifies every finding by its **finding-scope class** (`framework/shared/prototype-scope.md > Finding-scope classification`) and recalibrates the rating of `backend-only` findings, per `framework/skills/recalibrate-scope-severity.md`. The procedure runs at **Step 4s** of `framework/agents/reviews-inputs/adversarial-reviewer.md`.

**The three finding-scope classes** (canonical definitions in `prototype-scope.md`):

- **`fe-relevant`** — the corpus defect bears on something the frontend spec will encode (a role-gated screen, a workflow the UI drives, a field the UI displays, a validation message, an error/empty state). No recalibration.
- **`fe-facing-contract`** — a backend **contract the FE consumes** or **POPIA / PII handling** (which surfaces as consent banners, on-screen masking, retention notices). Severity preserved; `Reject` preserved where the enumeration genuinely gates frontend drafting.
- **`backend-only`** — the defect bears only on backend / infra / server-side concerns the frontend spec never encodes (server-side compute, persistence design, infra capacity, monitoring, queues). **This is the recalibration target.**

**No target signal here.** Unlike the `/review-requirement` sibling, this pipeline has **no build target** — the corpus carries no PI-block and `/review-inputs` leaves `source-manifest.json > target` `null`. So the skill is invoked with `target: null`, which applies the **conservative cap**: a `backend-only` finding's severity is capped at **`Major`** (never `Blocker`). The conservative cap preserves more signal — the fail-safe choice when scope cannot be confirmed.

**Strong alignment with the corpus-IS-the-voice principle.** Under this methodology "load-bearing" means *drives a requirement* — and `/requirements` drafts a **frontend** requirement. So the load-bearing checks that fire `Reject` (cross-source contradiction on RBAC / workflow steps / field types; POPIA enumeration) inherently bear on `fe-relevant` or `fe-facing-contract` concerns; a purely `backend-only` concern is by definition **not** load-bearing for a frontend draft, so it lands as a silence (`Treat as silence` → `Defer`), which is already non-blocking. Recalibration therefore mostly (a) caps any `backend-only` finding a worker over-rated to `Blocker` severity, and (b) tags `scope_class` for every finding.

**The disposition ↔ Recommendation coupling.** This methodology couples disposition to the five sanctioned Recommendation forms (`Reject` ↔ *Reconcile in-corpus* / *Resolve at draft time*; `Defer` ↔ *Treat as silence* / *Treat as second-hand*; `Patch` ↔ *Label / annotate*). The skill is Recommendation-agnostic and only changes severity/disposition; so in the rare case it demotes a `backend-only` finding's disposition away from `Reject`, **the reviewer re-expresses that finding's Recommendation to the coupled non-Reject form (`Treat as silence`)** at Step 4s as a methodology-specific normalization (logged in the Scope recalibration log). Every other finding's Recommendation is untouched, so the five sanctioned forms remain intact.

Every recalibration is recorded in the artefact's **Scope recalibration log** (Diagnostics) and is reversible by the consultant in the Revise loop.

---

## The strict-BMAD halt rule

**Zero findings on a dimension is a stop signal, not a success.**

If a dimension pass produces zero findings, the worker (and on Revise loops, the parent acting as that dimension's surrogate) **must**:

1. State this in-thread (parent surrogate path) or in the worker's `anti_confirmation_prompts` log: *"Dimension N — zero findings on first pass. Strict-BMAD rule fires: re-running with sharper skepticism."*
2. Re-run that dimension with explicit anti-confirmation prompts. For each consumable source, force-articulate at least one way it could fail the current dimension's check. Add findings if any anti-confirmation produces a real defect. The prompts produce silence-with-downstream-impact, voice-authenticity, ambiguity, contradiction, or unquantified-NFR findings — each carrying a Recommendation in one of the five sanctioned forms (never an elicitation step). Dimension-specific anti-confirmation prompts:
    - **Dimension 1:** "Force-articulate at least one role mentioned in any source that has **zero supporting material of any kind** in the corpus — no source describes its perspective, needs, or permissions — a coverage silence (Recommendation form *Treat as silence*). Escalate to a voice-authenticity finding only in the narrow four-part case: a strong, specific, draft-driving claim attributed to a role with no first-hand corroboration where mis-reading it as fact would change the draft (one Minor finding, *Treat as second-hand*). Do **not** manufacture a finding merely because a role's only material is second-hand — that is the corpus norm, not a defect."
    - **Dimension 2:** "Force-articulate at least one workflow named in the inputs whose non-happy-path behaviour is silent across the corpus, AND state how downstream must treat the silence (default applies / mark as unspecified)."
    - **Dimension 3:** "Force-articulate at least one vague verb / noun / quantifier / hedge in a load-bearing position across the corpus, AND classify whether downstream can resolve at draft time or whether it is Reject-grade load-bearing."
    - **Dimension 4:** "Force-articulate at least one factual claim that two sources state differently, or one source that fails the attributable-origin check — both Reject-grade in-corpus defects that no default can resolve."
    - **Dimension 5:** "Force-articulate at least one NFR or KPI signal the inputs imply but never quantify, AND state whether the silence is Reject-grade legal-enumeration (POPIA / GDPR / PCI / HIPAA) or Patch/Defer-grade silence handled by a `GR-NN` default."
    - **Dimension 6:** "Force-articulate at least one feature mentioned without a scope tag, AND state whether downstream applies `framework/shared/prototype-scope.md` default or surfaces at draft time."
3. If the re-run still produces zero findings, **write a `Justification` block** for that dimension in the artefact. The justification:
    - **Must** cite specific evidence (filenames, verbatim quotes, source-roster shape) that rules out each common failure mode listed for that dimension.
    - **Must** be at least 3 sentences. *"Clean"* is not a justification; *"The corpus carries 11 consumable sources spanning 4 distinct authors and 3 tiers (Native-text: 4, Supported-via-MCP: 5, Native-multimodal: 2); every named role (Finance Manager, External Auditor, Compliance Officer) has at least one direct-quote source; no source-count, tier-distribution, or self-selection signal fires"* is.
    - **Must** name the specific anti-confirmation prompts attempted in step 2 and why each failed to produce a finding.

4. **Never silently move on.** A dimension with zero findings and no justification block is a methodology violation; the quality-gate sweep treats it as a gate failure.

This rule applies independently to all six dimensions.

---

## Output presentation

The artefact renders as a self-contained HTML report following `framework/assets/reviews-inputs/template-adversarial.html`. The fixed section ordering is:

1. **Header** — title, generated-at timestamp, manifest fingerprint, reviewer identity.
2. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead: what this review is, what it found, what the consultant should do next. The first content section, above the Executive Summary. A faithful condensation of the findings — it introduces no finding or count not in the punch-list, and **preserves severity verbatim** (a Blocker / `BLOCKED` verdict is stated unsoftened). Review jargon is glossed at first use here; client domain terms are not. Per `framework/shared/output-readability.md`.
3. **Executive Summary** — total findings, severity tally, disposition tally, verdict line.
4. **Triage** — "Top issues to address first" callout (≤10 entries: every Reject and Blocker plus cluster-lead Majors). Lets the consultant chase the highest-impact missing material before scanning the full table.
5. **Clusters** — findings sharing a root cause grouped under a `CL-NN` cluster ID. Each cluster lists its member ADV-NNs and a one-line theme; the full detail for each finding still appears in the per-dimension sections below.
6. **Findings Table** — compact tabular view of every finding (ID, Dim, Sev, Disp, Cluster, Location, one-line problem), sorted Blocker → Major → Minor.
7. **Per-Dimension Sections (1–6)** — full findings for each dimension, or a Justification block if zero findings + strict-BMAD re-run passed. Each finding card carries a `scope_class` chip (`fe-relevant | fe-facing-contract | backend-only`) alongside its severity and disposition chips.
8. **Diagnostics** — quality-gate results, coverage map (which sources each dimension touched), strict-BMAD re-run log, the **Scope recalibration log** (`target: null` declared, then every finding whose rating was recalibrated, original → adjusted, with foreclosing authority), override log, **Corpus Shape** (source count, distinct-author count, time-window span, tier distribution — the observability data that the dropped Dim 7 used to surface, now reported as descriptive shape, never as findings), **Source roster (Consumed)** and **Source roster (Skipped)** tables.

The artefact is a punch-list, not a narrative — with **one** sanctioned narrative exception: the "In plain terms" lead at the very top (a short plain-English orientation that preserves severity, never softens it). Everywhere below the lead, prose between findings is minimised; the consultant should be able to read the Triage callout in under two minutes, scan the Clusters block to see which findings share a root cause, and jump straight to the per-dimension section for context on any finding. The Source-roster tables in Diagnostics tell the consultant which files were consumed (so findings can be traced back to source) and which files were skipped (so the consultant knows what coverage was unavailable).

---

## Consolidation & Triage

After the six-dimension sweep merges and IDs are assigned (Step 4b of `adversarial-reviewer.md`) and the purpose-aware scope recalibration runs (Step 4s — see *Purpose-aware scope recalibration*), one consolidation pass (Step 4c) annotates findings with **cluster IDs** and computes a **triage list**. Because triage selection keys on `Reject` / `Blocker` membership, it runs **after** Step 4s so it reflects the recalibrated ratings. The pass is a reader-aid: no finding is dropped, no finding's fields are rewritten, no `ADV-NN` is renumbered.

**Cluster rule.** Two or more findings cluster when they share a root cause — detected from a combination of cited filename, shared concept keywords in their `problem` field, and shared cross-source membership when applicable. Concept-keyword signals tuned for input-set defects:

- *Role unsupported* / *coverage silence* (Dim 1); *load-bearing claim with no first-hand backing* (Dim 1 voice-authenticity, narrow).
- *Happy-path-only coverage* / *no error-state material* (Dim 2).
- *Entity X never grounded* / *field-level detail absent* (Dim 2 or 4).
- *Vague verb 'support' / 'handle' / 'manage'* (Dim 3).
- *POPIA referenced without scope* / *PII fields not enumerated* (Dim 5).
- *Cross-source naming drift* / *RBAC table conflict* (Dim 4).
- *Single-source / hedge-laden provenance* (Dim 4).

A cluster has ≥2 members; singletons are never clustered. Each finding belongs to at most one cluster. Cluster IDs are `CL-01`, `CL-02`, … assigned in order of each cluster's lead (lowest-ADV-NN) member.

**Triage rule.** The "Top issues to address first" callout selects up to 10 findings, deterministically, in this priority order:

1. Every Reject, in `ADV-NN` ascending order.
2. Every Blocker not already included, in `ADV-NN` ascending order.
3. Major findings that are the lead of a cluster of size ≥3, ordered by cluster size descending then lead `ADV-NN` ascending. (A large cluster fronted by a single elicitation visit is high-leverage.)
4. Remaining Major findings in `ADV-NN` ascending order.
5. Hard cap at 10. Never includes Minor findings.

**What this preserves.** Every quality gate is unaffected — `cluster_id` is metadata, not a 9th required schema field; the Findings Table row count still equals the sum of per-dimension counts (clustering does not drop, merge, or duplicate findings). The per-dimension sections render unchanged, in their original within-dimension order; the severity-driven sort applies only to the Findings Table. The deterministic ID assignment from Step 4b is final; Step 4s recalibrates ratings and Step 4c only annotates and selects.

**Why it exists.** A run with 60+ findings is correct but un-scannable. The Triage callout lets a consultant prioritise the must-resolve-now list (typically 5–10 entries) in one sitting; the Clusters block lets them see that nine separate findings citing "no Finance Manager voice" share one underlying gap, so the elicitation list is shorter than the finding count. Both are navigation aids over the audit-grade detail that remains in the per-dimension sections.

---

## Quality gates (run after Dimension 6, before write)

Thirteen gates. All are hard. If any gate fails, the reviewer does **not** write the artefact — it surfaces a structured error and halts. (See `framework/agents/reviews-inputs/adversarial-reviewer.md > Step 10 — Validate` for the halt contract.)

1. **Every finding has all eight schema fields populated.** Missing-field findings are invalid.
2. **Every finding's Dimension is exactly one integer 1–6.** Multi-dimension findings must be decomposed.
3. **Every finding's Severity is exactly one of `Blocker | Major | Minor`** — AND every `backend-only` finding's Severity is at or below the conservative cap (`Major`); a `backend-only` finding is never `Blocker`.
4. **Every finding's Disposition is exactly one of `Patch | Defer | Reject`** — AND no `backend-only` finding's Disposition is `Reject`.
5. **Every finding's Evidence field is verbatim (≤5 lines) and exists in the per-source quote index for the cited filename** — OR the finding cites an `Unsupported`-tier filename and Evidence is the literal `*(file skipped — tier: Unsupported; reason: <reason>)*` placeholder. Paraphrased or fabricated evidence is a gate failure.
6. **Every finding's Location matches a `consumed_rows[*].filename` or a `skipped_rows[*].filename`** (the latter only when Evidence is the skipped-placeholder form). Citations to non-manifest filenames are a gate failure.
7. **Every dimension reports either ≥1 finding or a non-empty Justification block.** Silent zero-finding dimensions are a methodology violation.
8. **Every Justification block (if any) cites specific evidence and is ≥3 sentences.** Stub justifications are a gate failure.
9. **The verdict line is consistent with the post-recalibration disposition/severity tally** (any Reject or Blocker → `BLOCKED`; otherwise findings present → `NEEDS-REVISION`; zero findings everywhere → `ACCEPTED-WITH-FIXES`). The tally is read **after** Step 4s scope recalibration, so no `backend-only` finding contributes a Reject/Blocker.
10. **The Findings Table row count equals the sum of per-dimension finding counts.** Drift is a render bug.
11. **The artefact's `MANIFEST_FINGERPRINT` field matches the SHA-256 of `requirements/source-manifest.json` captured at Step 2, AND every Source-roster (Consumed) `sha256[:8]` column matches its manifest row's `sha256` field.** Mismatch means the artefact analysed one version of the input set and reports against another.
12. **The Corpus Shape subsection in Diagnostics is populated with non-empty values for source count, distinct-author count, time-window span, and tier distribution.** This preserves the observability that the dropped Dim 7 used to provide; an empty shape block is a render bug.
13. **Every finding's Recommendation matches one of the five sanctioned forms** (`Reconcile in-corpus`, `Label / annotate`, `Treat as silence`, `Treat as second-hand`, `Resolve at draft time`). Recommendations containing the substrings *"interview"*, *"elicit"*, *"workshop"*, *"schedule"*, *"go ask"*, *"contact the"*, or otherwise proposing new elicitation are a gate failure under the *corpus IS the voice* principle.

Beyond the thirteen numbered gates, the reviewer's self-validation also verifies that **every finding carries a `scope_class`** (`fe-relevant | fe-facing-contract | backend-only`) and that **every recalibrated finding has a matching entry in the Scope recalibration log** (rendered in the Diagnostics block). `scope_class` is metadata, not a 9th schema field, so it does not affect gate 1. Any `backend-only` finding whose disposition Step 4s demoted away from `Reject` also has its Recommendation normalised to the coupled `Treat as silence` form, so gate 13 still passes.

---

## Anti-patterns

- **Returning "looks good".** The methodology forbids this. Re-run; write a justification; never silently pass.
- **Fabricating evidence.** Every Evidence field must be a verbatim quote from the cited source's bundle entry (or the sanctioned skipped-placeholder form for `Unsupported`-tier findings). If you cannot find a quote, you do not have a finding — drop it.
- **Elicitation-form Recommendations.** Do not write Recommendations of the form *"interview X"*, *"elicit Y"*, *"schedule a workshop with Z"*, *"add an interview transcript"*, *"go ask the stakeholder"*. The corpus IS the voice; there is no second visit. Every Recommendation must match one of the five sanctioned forms (Reconcile in-corpus / Label / Treat as silence / Treat as second-hand / Resolve at draft time). Quality gate 13 enforces this.
- **Treating second-hand voice as first-hand.** A BA-authored brief stating *"Finance Managers want X"* is the brief author's voice about Finance Managers, not Finance Manager voice. Dim 1 findings should distinguish: a role for whom only second-hand voice exists is a voice-authenticity defect with Recommendation form *Treat as second-hand* (downstream marks as BA-interpretation). Treating the brief's claim as if it were the Finance Manager's own utterance erases the consultant's authorial layer — a real audit signal.
- **Generic findings.** *"The inputs could be clearer"* is not a finding. Cite the specific source, quote the specific sentence (or its absence), state the specific defect of the voice, propose a specific corpus-handling Recommendation in one of the five sanctioned forms.
- **Severity inflation.** Calling every finding a Blocker dilutes the signal. Reserve Blocker for findings that genuinely prevent `/requirements` from drafting.
- **Disposition collapse.** Disposition (Patch / Defer / Reject) is orthogonal to severity. A Minor finding can be a Reject (e.g., a small but blocking POPIA gap — `fe-facing-contract`); a Major finding can be a Defer (e.g., a significant role-voice gap for a phase-2 persona).
- **Dropping a backend-only finding.** Scope recalibration (Step 4s) *raises and re-rates*; it never drops. A defect bearing only on backend / infra concerns is still a finding — capped at `Major` (never `Blocker`/`Reject`) and logged in the Scope recalibration log, not deleted.
- **Mis-classing a UI-actionable finding as `backend-only`.** Classify by whether the frontend draft would encode the concern. A workflow the UI drives, a field the UI displays, a role-gated screen, POPIA consent UI is `fe-relevant` / `fe-facing-contract` and keeps its severity. When undecided, choose `fe-facing-contract` — bias toward not suppressing.
- **Collapsing dimensions.** Each dimension is its own pass with its own gate. Running them in a single combined sweep hides reasoning and breaks the diagnostics block. The parent reviewer dispatches six parallel workers; collapsing into a single agent pass defeats per-dimension auditability.
- **Reviewing against the synthesised requirements doc.** Do not consult `requirements/requirements.md` or any other `/requirements`-pipeline derivative. The review's contract is to critique the **raw inputs**; `/requirements` has not run yet (or if it has, that run's correctness is downstream and out of scope here).
- **Reviewing against parallel analyses.** Do not consult `analyse-inputs/<METHOD>/*` outputs to triangulate findings. Each input-pipeline lens is independently grounded in the manifest; cross-reading creates implicit dependencies and conflates source material with derived structures.
- **Skipping re-ingested analysis artefacts.** Do not skip manifest rows whose filename suggests they are this framework's own output (e.g., `opportunity-solution-tree.html`, `thematic-analysis.html`). Re-ingested analysis artefacts are part of the input set; `/requirements` will draft from them as it would any other source. Dimension 3 (Ambiguity) and Dimension 4 (Consistency) catch defects they contain — silent skipping based on filename pattern would hide a real audit signal.
- **Line numbers in Location.** The Location field is `filename` only — no line numbers, no section anchors. Line numbers in `.converted.md` siblings drift between markitdown runs; multimodal sources have no lines.
- **Inline `[SRC: ...]` markers in findings.** The Evidence + Location pair is the citation; do not duplicate it with inline markers in the Problem or Recommendation fields. The artefact's source-roster tables in Diagnostics aggregate filenames so the consultant can navigate.

---

## Voice and stance

The reviewer's stance is defined in `framework/assets/characters/adversarial-inputs-review.md` — skeptical, evidence-required, must-find-issues, no rubber-stamping, focused on the input set as the audit subject. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact is human-read (and has no downstream machine consumer), so the reviewer also follows `framework/shared/output-readability.md`: it writes the "In plain terms" lead (preserving severity, never softening), glosses review jargon (severity, disposition, dimension, verdict, cluster) at first use in human-readable prose, leaves client domain vocabulary unglossed, and keeps the punch-list discipline everywhere below the lead. Traceability stays as Location + verbatim Evidence; reviews carry no `[SRC:]`.

---

## References

- **BMAD method** — Breakthrough Method for Agile AI-Driven Development. Adversarial review docs at `docs.bmad-method.org/explanation/adversarial-review/`; core tools (including `bmad-review-adversarial-general` and `bmad-review-edge-case-hunter`) at `docs.bmad-method.org/reference/core-tools/`; repo at `github.com/bmad-code-org/BMAD-METHOD`. The "must find issues" rule, the Patch/Defer/Reject disposition bucket, and the false-positive caveat all originate here.
- **Karl Wiegers — Writing Quality Requirements** (`processimpact.com/articles/qualreqs.pdf`). Six requirements-quality dimensions: completeness, correctness, feasibility, necessity, prioritization, verifiability. Dimensions 1, 2, and 5 of this reference are direct descendants, re-framed for elicitation-stage defects rather than finished-doc defects.
- **IIBA BABOK v3 — Business Analysis Body of Knowledge.** Elicitation quality and stakeholder analysis chapters underpin Dimensions 1 and 4 — re-framed under the *corpus IS the voice* principle so that stakeholder-coverage gaps land as **coverage-silence** findings (Recommendation form *Treat as silence*) rather than as elicitation triggers. Voice authenticity (first- vs second-hand) is retained only as a **narrow secondary lens** for load-bearing claims with no first-hand backing — in a consultant-relayed corpus second-hand voice is the norm, so it is not findings-generating on its own.
- **Volere Requirements Specification Template (Atlantic Systems Guild).** "Rationale" and "Fit Criterion" fields drive Dimension 5 (Quantitative & Measurable Signal); "Customer Satisfaction / Dissatisfaction" pair drives the scope-signal lens in Dimension 6.
- **IEEE Std 830 — Recommended Practice for Software Requirements Specifications.** Establishes the formal inspection pattern. Dimensions 2 and 4 align with IEEE 830's coverage and consistency categories.
- **Sibling reference for finished-doc critique:** `framework/assets/reviews/adversarial-reference.md` — applies the same BMAD methodology to `requirements/requirements.md` after `/requirements` has synthesised it. Eight dimensions tuned for finished-doc defects (completeness, ambiguity, testability, scope, dependency, consistency, edge cases, feasibility).

The synthesised six-dimension structure is this reference's own contribution: it integrates BMAD's adversarial rule, Wiegers's quality categories, BABOK's stakeholder-coverage lens, Volere's measurement and satisfaction lenses, and IEEE 830's inspection scope into one auditable pass-per-dimension methodology applied to the raw consultant input corpus.

**Divergence from the lineage's elicitation framing.** Wiegers and BABOK use stakeholder coverage as an *elicitation driver* — gaps imply more interviews. This reference, under the *corpus IS the voice* principle, replaces that lens with a **voice-handling** lens: gaps imply downstream defaults / `[OUT-OF-SCOPE]` annotations (and, in the narrow load-bearing case, second-hand markers), never elicitation. Note that voice authenticity (first- vs second-hand provenance) is a **narrow secondary lens** here, not a primary driver — in a consultant-relayed corpus almost everything is second-hand, so coverage (does the role have *any* material) is the load-bearing check and authenticity fires only on load-bearing, draft-changing claims with no first-hand backing. The ambiguity / consistency / completeness sub-lenses (Dimensions 2, 3, 4, 5, 6) preserve their lineage operationally — what to scan for is unchanged — but their Recommendation contract follows the five sanctioned corpus-handling forms instead of proposing elicitation actions. A prior seventh dimension (Bias / Sampling / Self-Selection) existed in earlier drafts and was structurally incompatible with the principle (its premise was that the corpus *should be* larger / more diverse — but under the principle there is no should-be); its observability content survives as the Diagnostics block's Corpus Shape subsection.
