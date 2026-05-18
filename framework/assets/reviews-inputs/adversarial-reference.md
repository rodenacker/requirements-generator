<!-- ROLE: asset (P2 review reference). Loaded by framework/agents/reviews-inputs/adversarial-reviewer.md at activation. -->

# reviews-inputs/adversarial-reference.md

**Purpose:** Methodology reference for Adversarial Review of the **raw consultant input set** enumerated by `requirements/source-manifest.json`. The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews-inputs/adversarial-reviewer.md` — drives the agent's seven-dimension process plus the quality-gate sweep.

**Output produced by the reviewer:** `reviews/inputs/ADVERSARIAL/adversarial-review.md` — a markdown punch-list of cited, severity-graded, dispositioned findings using `framework/assets/reviews-inputs/template-adversarial.md` as scaffold.

**Sibling lens:** `framework/assets/reviews/adversarial-reference.md` runs the same methodology against the synthesised `requirements/requirements.md` after `/requirements` has produced it. The two references are complementary, not redundant — this one critiques the *source of truth*; the sibling critiques the *derivation*. Fixing input-set defects shifts ground truth; fixing finished-doc defects only re-litigates whatever the inputs already let through. The dimensions, examples, and citation format differ; the BMAD rule, finding schema, disposition rubric, clustering, triage, and verdict mapping are preserved.

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
- `framework/assets/reviews-inputs/template-adversarial.md` (the markdown scaffold — read once at render time by the parent).

The reviewer does **not** read:

- `requirements/requirements.md`, `requirements/requirements-draft.md`, `requirements/consultant-answers.md`, `requirements/draft-claims*.ndjson` — derivative artefacts; the review's contract is to critique the raw inputs themselves, not anything `/requirements` has already synthesised.
- `analyses/*` or `analyses/inputs/*` outputs — derived; reviewing the raw inputs against a parallel analysis of those same inputs conflates "what the source material says" with "what an analyser inferred". The review's contract is to critique the inputs as the inputs.
- `design-system/*`, `reviews/*` (including the requirement-doc adversarial review), `framework/state/*`, `framework/shared/*` (except as textual references in this document) — out of scope.

The raw consultant input set is the contract. If the inputs don't say it, the inputs don't say it — and that is a finding. **Inputs re-ingested from `/analyse-inputs` outputs (a thematic-analysis or opportunity-solution-tree artefact re-dropped into `input/`) are part of the input set and are reviewed as such**; they are not skipped or treated specially. The whole point is that the merged input corpus is what `/requirements` will draft from.

---

## The seven review dimensions

Seven dimensions, executed in order. Each is its own pass; the reviewer does not collapse passes. The dimension-by-dimension structure is what makes the review auditable: every finding maps to exactly one dimension, every dimension reports either ≥1 finding or a Justification block.

The seven dimensions are tuned for **raw consultant inputs** — they differ from the eight dimensions of `/review-requirement` adversarial because input-set defects differ from finished-doc defects. Testability does not apply when no requirements exist yet; dependency-ordering does not apply across heterogeneous PDFs / decks / transcripts. The dimensions are re-synthesised from elicitation-quality literature (Wiegers, IIBA BABOK, Volere) plus BMAD's must-find-issues posture.

### Dimension 1 — Stakeholder & Role Coverage

**Question:** Does every role / persona that will use the system have voice in the inputs?

**What to check:**

- Every named role or persona has at least one **direct quote** in the inputs — an interview transcript line, a survey response, a workshop note attributed to them, a labelled screenshot, a brief paragraph that names them as the source.
- Every role mentioned in passing (in a brief or in an executive deck) has supporting elicitation material from *that role*. A role mentioned only by an executive is a coverage gap — the executive does not speak for the role.
- The corpus reflects all role categories that will use the system: end-users (often multiple sub-roles by job function), administrators / power users, operators / support staff, auditors / compliance officers, regulators if applicable, integration partners if external systems are involved.
- Skipped-source visibility: if a stakeholder is mentioned only in an `Unsupported`-tier file (e.g., `proposal.pages`), the inputs do not currently surface that voice; flag it as a finding citing the skipped filename.
- Cross-source corroboration: a stakeholder voice that appears in only one source is weaker than one that appears in two or more. A single-source role is a finding when that source is hedge-laden or aspirational.

**Common failure modes to scan for:**

- A brief that names "Finance Manager" as a primary user, but no interview, transcript, or workshop note quotes a Finance Manager.
- A role mentioned ("we'll need an admin role") with zero supporting material defining what admin does, who currently performs it, or what tooling they use today.
- A regulator or auditor role implied by compliance language ("must be POPIA compliant") but no quote, no email, no actual auditor or compliance-officer voice in the corpus.
- A user-segment mentioned only as a number on a deck slide ("50,000 end-users") with no qualitative material from any of them.

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

### Dimension 7 — Bias, Sampling & Stakeholder Self-Selection

**Question:** Is the input set itself biased — by who was sampled, by tier distribution, by time window, or by self-selection?

**What to check:**

- Distinct-source count: a corpus with 1–2 sources is sampling-collapsed regardless of what those sources contain. 3–5 is marginal. 6+ with role diversity is healthy. (Counts are heuristic — judgement applies.)
- Distinct-author / -role count: 10 transcripts all from the same interviewee is one voice repeated, not multiple voices.
- Time-window distribution: every source dated within a single workshop week is a sampling collapse — the corpus reflects one elicitation event, not iterated discovery.
- Tier-distribution skew: 12 screenshots and 0 interview transcripts is visual-only sampling; 5 PDFs and 0 user-voice material is document-only sampling. Each tier reveals different defects; missing a tier is a finding.
- Self-selection in interview transcripts: which user agreed to talk? The loudest power user? An executive sponsor? If the same role appears in multiple transcripts but always from the same persona type (e.g., always from the most engaged users), the corpus has self-selection bias.
- Aspirational-vs-current ratio: if every source describes the future system and no source describes the *current* state, the inputs cannot ground the as-is required for `/requirements` to write a migration plan.
- Source-recency skew: a corpus dominated by year-old material with no recent confirmation is a staleness finding; one dominated by very recent material with no historical baseline misses cycle context.
- Provenance-tier skew: every source is hedge-laden ("I think...", "we used to...") with no authoritative sources (signed brief, executive decision, written policy) — a credibility-floor finding.

**Common failure modes to scan for:**

- A corpus of 18 files, all from the same client off-site three weeks ago, no follow-up confirmation since.
- 25 screenshots of the existing system, zero quotes from anyone who uses it.
- Three interview transcripts all from the same executive sponsor and his two direct reports — no end-user voice.
- "We surveyed 200 users" in a brief with no transcript, no quote, no survey-result file in the corpus — the claim is unsupported by the corpus itself.
- A corpus with two sources: a deck from 2023 and a transcript from 2026 — the gap is suspicious; what happened in between?
- Every source is aspirational (proposals, decks, mockups) with no description of the current state — `/requirements` cannot draft a migration path against vapour.

---

## Finding schema

Every finding has all eight fields populated, in this order:

```
ID:             ADV-NN          (sequential per run, zero-padded — ADV-01, ADV-02, …)
Dimension:      1..7            (which review dimension the finding maps to)
Severity:       Blocker | Major | Minor
Disposition:    Patch | Defer | Reject
Location:       <filename>      (the manifest row's `filename` field — basename + extension)
Evidence:       direct verbatim quote from the cited source, ≤5 lines
Problem:        one sentence — what is wrong/missing/unclear/conflicted in the source material
Recommendation: one sentence — concrete corrective action (typically elicitation guidance)
```

**Field rules:**

- **ID** is unique per run and reset to `ADV-01` on every fresh invocation. Revise loops keep their IDs; only Restart resets the sequence. The pipeline is **full overwrite** per run — each run's artefact reflects only the current input set, with no carried-over findings from prior runs.
- **Dimension** is exactly one integer 1–7. A finding that spans dimensions must be decomposed into one finding per dimension.
- **Severity** is exactly one of three. No "Critical" or "Trivial" or "Cosmetic".
- **Disposition** is exactly one of three (Patch / Defer / Reject). See the rubric below.
- **Location** is the manifest row's `filename` field — basename plus extension (e.g., `brief.docx`, `workshop-notes.md`, `whiteboard-photo.png`, `interview-transcript.md`). **No line numbers**, no section anchors. Multimodal sources have no lines; markitdown-converted siblings re-anchor on `.converted.md` (different from the original); line numbers rot. The audit unit is `<filename>` + verbatim quote ≤5 lines.
- **Evidence** is a verbatim quote from the cited source's `text_or_transcription` content as captured by the parent reviewer into the evidence bundle (Native-text content is the file's bytes; Native-multimodal content is the parent's verbatim transcription of visible text + structural observations). Do not paraphrase. If the offending text is longer than 5 lines, decompose the finding into multiple findings each citing a ≤5-line slice. For `Unsupported`-tier files cited in Dimension 1 (stakeholder mentioned only in skipped file): Evidence is the literal string `*(file skipped — tier: Unsupported; reason: <conversion-failure-reason>)*` — a sanctioned non-verbatim form because the file's content was never read.
- **Problem** is one sentence stating the defect. *"`brief.docx` lists 'Finance Manager' as a primary user but no source quotes a Finance Manager directly"* — not *"stakeholder coverage gap"*.
- **Recommendation** is one sentence proposing a concrete elicitation action, not a rewrite of the input. *"Add an interview transcript with a Finance Manager describing their reconciliation workflow before `/requirements` drafts"* — not *"clarify the Finance Manager role"*.

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

- The defect is **real** and **specific**, but addressable in a later iteration of elicitation without blocking the current scope.
- Common pattern: a missing edge-case workflow that affects a post-MVP feature; a missing role voice for a role that only matters in phase 2; an integration whose contract belongs to a later phase.
- Logged for the next elicitation cycle but does not block `/requirements` from drafting the MVP.

### Reject

- **Blocking.** `/requirements` cannot draft from these inputs until this is resolved.
- Common patterns: a primary user role with zero voice in the inputs; a core workflow named with no supporting material; a POPIA-bearing data flow described only in one hedge-laden transcript line; cross-source factual conflicts on the central data model.
- Any single Reject finding makes the overall verdict `BLOCKED`.

### Disposition → Verdict mapping

The artefact's Executive Summary states one verdict:

| Verdict | When |
|---|---|
| `BLOCKED` | At least one `Reject` disposition exists, **or** at least one Blocker severity finding exists. |
| `NEEDS-REVISION` | No Rejects/Blockers, but ≥1 finding total. |
| `ACCEPTED-WITH-FIXES` | Zero findings on all seven dimensions, **and** every dimension carries a non-empty Justification block. (Rare — strict-BMAD rule below makes this expensive.) |

There is no fourth verdict. "Looks good" is not a verdict.

---

## The strict-BMAD halt rule

**Zero findings on a dimension is a stop signal, not a success.**

If a dimension pass produces zero findings, the worker (and on Revise loops, the parent acting as that dimension's surrogate) **must**:

1. State this in-thread (parent surrogate path) or in the worker's `anti_confirmation_prompts` log: *"Dimension N — zero findings on first pass. Strict-BMAD rule fires: re-running with sharper skepticism."*
2. Re-run that dimension with explicit anti-confirmation prompts. For each consumable source, force-articulate at least one way it could fail the current dimension's check. Add findings if any anti-confirmation produces a real defect. Dimension-specific anti-confirmation prompts:
    - **Dimension 1:** "Force-articulate at least one role likely to use this system that has zero direct quotes in any consumable source."
    - **Dimension 2:** "Force-articulate at least one workflow named in the inputs whose non-happy-path behaviour is not described in any source."
    - **Dimension 3:** "Force-articulate at least one vague verb / noun / quantifier / hedge in a load-bearing position across the corpus."
    - **Dimension 4:** "Force-articulate at least one factual claim that two sources state differently, or one source that fails the attributable-origin check."
    - **Dimension 5:** "Force-articulate at least one NFR or KPI signal the inputs imply but never quantify."
    - **Dimension 6:** "Force-articulate at least one feature mentioned without a scope tag, or one out-of-scope topic the inputs never name."
    - **Dimension 7:** "Force-articulate at least one sampling-collapse signal: source count, role diversity, time window, tier distribution, or self-selection."
3. If the re-run still produces zero findings, **write a `Justification` block** for that dimension in the artefact. The justification:
    - **Must** cite specific evidence (filenames, verbatim quotes, source-roster shape) that rules out each common failure mode listed for that dimension.
    - **Must** be at least 3 sentences. *"Clean"* is not a justification; *"The corpus carries 11 consumable sources spanning 4 distinct authors and 3 tiers (Native-text: 4, Supported-via-MCP: 5, Native-multimodal: 2); every named role (Finance Manager, External Auditor, Compliance Officer) has at least one direct-quote source; no source-count, tier-distribution, or self-selection signal fires"* is.
    - **Must** name the specific anti-confirmation prompts attempted in step 2 and why each failed to produce a finding.

4. **Never silently move on.** A dimension with zero findings and no justification block is a methodology violation; the quality-gate sweep treats it as a gate failure.

This rule applies independently to all seven dimensions.

---

## Output presentation

The artefact renders as a structured markdown report following `framework/assets/reviews-inputs/template-adversarial.md`. The fixed section ordering is:

1. **Header** — title, generated-at timestamp, manifest fingerprint, reviewer identity.
2. **Executive Summary** — total findings, severity tally, disposition tally, verdict line.
3. **Triage** — "Top issues to address first" callout (≤10 entries: every Reject and Blocker plus cluster-lead Majors). Lets the consultant chase the highest-impact missing material before scanning the full table.
4. **Clusters** — findings sharing a root cause grouped under a `CL-NN` cluster ID. Each cluster lists its member ADV-NNs and a one-line theme; the full detail for each finding still appears in the per-dimension sections below.
5. **Findings Table** — compact tabular view of every finding (ID, Dim, Sev, Disp, Cluster, Location, one-line problem), sorted Blocker → Major → Minor.
6. **Per-Dimension Sections (1–7)** — full findings for each dimension, or a Justification block if zero findings + strict-BMAD re-run passed.
7. **Diagnostics** — quality-gate results, coverage map (which sources each dimension touched), strict-BMAD re-run log, override log, **Source roster (Consumed)** and **Source roster (Skipped)** tables.

The artefact is a punch-list, not a narrative. Prose between findings is minimised; the consultant should be able to read the Triage callout in under two minutes, scan the Clusters block to see which findings share a root cause, and jump straight to the per-dimension section for context on any finding. The Source-roster tables in Diagnostics tell the consultant which files were consumed (so findings can be traced back to source) and which files were skipped (so the consultant knows what coverage was unavailable).

---

## Consolidation & Triage

After the seven-dimension sweep merges and IDs are assigned (Step 3b of `adversarial-reviewer.md`), one consolidation pass (Step 3c) annotates findings with **cluster IDs** and computes a **triage list**. The pass is a reader-aid: no finding is dropped, no finding's fields are rewritten, no `ADV-NN` is renumbered.

**Cluster rule.** Two or more findings cluster when they share a root cause — detected from a combination of cited filename, shared concept keywords in their `problem` field, and shared cross-source membership when applicable. Concept-keyword signals tuned for input-set defects:

- *Stakeholder voice missing* / *role unquoted* (Dim 1).
- *Happy-path-only coverage* / *no error-state material* (Dim 2).
- *Entity X never grounded* / *field-level detail absent* (Dim 2 or 4).
- *Vague verb 'support' / 'handle' / 'manage'* (Dim 3).
- *POPIA referenced without scope* / *PII fields not enumerated* (Dim 5).
- *Cross-source naming drift* / *RBAC table conflict* (Dim 4).
- *Single-source / hedge-laden provenance* (Dim 4 or 7).
- *Time-window collapse* / *single-workshop sampling* (Dim 7).
- *Tier skew: screenshots-only / transcripts-absent* (Dim 7).

A cluster has ≥2 members; singletons are never clustered. Each finding belongs to at most one cluster. Cluster IDs are `CL-01`, `CL-02`, … assigned in order of each cluster's lead (lowest-ADV-NN) member.

**Triage rule.** The "Top issues to address first" callout selects up to 10 findings, deterministically, in this priority order:

1. Every Reject, in `ADV-NN` ascending order.
2. Every Blocker not already included, in `ADV-NN` ascending order.
3. Major findings that are the lead of a cluster of size ≥3, ordered by cluster size descending then lead `ADV-NN` ascending. (A large cluster fronted by a single elicitation visit is high-leverage.)
4. Remaining Major findings in `ADV-NN` ascending order.
5. Hard cap at 10. Never includes Minor findings.

**What this preserves.** Every quality gate is unaffected — `cluster_id` is metadata, not a 9th required schema field; the Findings Table row count still equals the sum of per-dimension counts (clustering does not drop, merge, or duplicate findings). The per-dimension sections render unchanged, in their original within-dimension order; the severity-driven sort applies only to the Findings Table. The deterministic ID assignment from Step 3b is final; Step 3c only annotates and selects.

**Why it exists.** A run with 60+ findings is correct but un-scannable. The Triage callout lets a consultant prioritise the must-resolve-now list (typically 5–10 entries) in one sitting; the Clusters block lets them see that nine separate findings citing "no Finance Manager voice" share one underlying gap, so the elicitation list is shorter than the finding count. Both are navigation aids over the audit-grade detail that remains in the per-dimension sections.

---

## Quality gates (run after Dimension 7, before write)

Eleven gates. All are hard. If any gate fails, the reviewer does **not** write the artefact — it surfaces a structured error and halts. (See `framework/agents/reviews-inputs/adversarial-reviewer.md > Step 10 — Validate` for the halt contract.)

1. **Every finding has all eight schema fields populated.** Missing-field findings are invalid.
2. **Every finding's Dimension is exactly one integer 1–7.** Multi-dimension findings must be decomposed.
3. **Every finding's Severity is exactly one of `Blocker | Major | Minor`.**
4. **Every finding's Disposition is exactly one of `Patch | Defer | Reject`.**
5. **Every finding's Evidence field is verbatim (≤5 lines) and exists in the per-source quote index for the cited filename** — OR the finding cites an `Unsupported`-tier filename and Evidence is the literal `*(file skipped — tier: Unsupported; reason: <reason>)*` placeholder. Paraphrased or fabricated evidence is a gate failure.
6. **Every finding's Location matches a `consumed_rows[*].filename` or a `skipped_rows[*].filename`** (the latter only when Evidence is the skipped-placeholder form). Citations to non-manifest filenames are a gate failure.
7. **Every dimension reports either ≥1 finding or a non-empty Justification block.** Silent zero-finding dimensions are a methodology violation.
8. **Every Justification block (if any) cites specific evidence and is ≥3 sentences.** Stub justifications are a gate failure.
9. **The verdict line is consistent with the disposition tally** (any Reject or Blocker → `BLOCKED`; otherwise findings present → `NEEDS-REVISION`; zero findings everywhere → `ACCEPTED-WITH-FIXES`).
10. **The Findings Table row count equals the sum of per-dimension finding counts.** Drift is a render bug.
11. **The artefact's `MANIFEST_FINGERPRINT` field matches the SHA-256 of `requirements/source-manifest.json` captured at Step 2, AND every Source-roster (Consumed) `sha256[:8]` column matches its manifest row's `sha256` field.** Mismatch means the artefact analysed one version of the input set and reports against another.

---

## Anti-patterns

- **Returning "looks good".** The methodology forbids this. Re-run; write a justification; never silently pass.
- **Fabricating evidence.** Every Evidence field must be a verbatim quote from the cited source's bundle entry (or the sanctioned skipped-placeholder form for `Unsupported`-tier findings). If you cannot find a quote, you do not have a finding — drop it.
- **Generic findings.** *"The inputs could be clearer"* is not a finding. Cite the specific source, quote the specific sentence (or its absence), state the specific defect, propose the specific elicitation step.
- **Severity inflation.** Calling every finding a Blocker dilutes the signal. Reserve Blocker for findings that genuinely prevent `/requirements` from drafting.
- **Disposition collapse.** Disposition (Patch / Defer / Reject) is orthogonal to severity. A Minor finding can be a Reject (e.g., a small but blocking POPIA gap); a Major finding can be a Defer (e.g., a significant role-voice gap for a phase-2 persona).
- **Collapsing dimensions.** Each dimension is its own pass with its own gate. Running them in a single combined sweep hides reasoning and breaks the diagnostics block. The parent reviewer dispatches seven parallel workers; collapsing into a single agent pass defeats per-dimension auditability.
- **Reviewing against the synthesised requirements doc.** Do not consult `requirements/requirements.md` or any other `/requirements`-pipeline derivative. The review's contract is to critique the **raw inputs**; `/requirements` has not run yet (or if it has, that run's correctness is downstream and out of scope here).
- **Reviewing against parallel analyses.** Do not consult `analyses/inputs/<METHOD>/*` outputs to triangulate findings. Each input-pipeline lens is independently grounded in the manifest; cross-reading creates implicit dependencies and conflates source material with derived structures.
- **Skipping re-ingested analysis artefacts.** Do not skip manifest rows whose filename suggests they are this framework's own output (e.g., `opportunity-solution-tree.md`, `thematic-analysis.md`). Re-ingested analysis artefacts are part of the input set; `/requirements` will draft from them as it would any other source. Dimension 3 (Ambiguity) and Dimension 4 (Consistency) catch defects they contain — silent skipping based on filename pattern would hide a real audit signal.
- **Line numbers in Location.** The Location field is `filename` only — no line numbers, no section anchors. Line numbers in `.converted.md` siblings drift between markitdown runs; multimodal sources have no lines.
- **Inline `[SRC: ...]` markers in findings.** The Evidence + Location pair is the citation; do not duplicate it with inline markers in the Problem or Recommendation fields. The artefact's source-roster tables in Diagnostics aggregate filenames so the consultant can navigate.

---

## Voice and stance

The reviewer's stance is defined in `framework/assets/characters/adversarial-inputs-review.md` — skeptical, evidence-required, must-find-issues, no rubber-stamping, focused on the input set as the audit subject. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

---

## References

- **BMAD method** — Breakthrough Method for Agile AI-Driven Development. Adversarial review docs at `docs.bmad-method.org/explanation/adversarial-review/`; core tools (including `bmad-review-adversarial-general` and `bmad-review-edge-case-hunter`) at `docs.bmad-method.org/reference/core-tools/`; repo at `github.com/bmad-code-org/BMAD-METHOD`. The "must find issues" rule, the Patch/Defer/Reject disposition bucket, and the false-positive caveat all originate here.
- **Karl Wiegers — Writing Quality Requirements** (`processimpact.com/articles/qualreqs.pdf`). Six requirements-quality dimensions: completeness, correctness, feasibility, necessity, prioritization, verifiability. Dimensions 1, 2, and 5 of this reference are direct descendants, re-framed for elicitation-stage defects rather than finished-doc defects.
- **IIBA BABOK v3 — Business Analysis Body of Knowledge.** Elicitation quality and stakeholder analysis chapters underpin Dimensions 1, 4, and 7. The bias / sampling lens of Dimension 7 is BABOK's stakeholder-coverage check applied to the corpus itself.
- **Volere Requirements Specification Template (Atlantic Systems Guild).** "Rationale" and "Fit Criterion" fields drive Dimension 5 (Quantitative & Measurable Signal); "Customer Satisfaction / Dissatisfaction" pair drives the scope-signal lens in Dimension 6.
- **IEEE Std 830 — Recommended Practice for Software Requirements Specifications.** Establishes the formal inspection pattern. Dimensions 2 and 4 align with IEEE 830's coverage and consistency categories.
- **Sibling reference for finished-doc critique:** `framework/assets/reviews/adversarial-reference.md` — applies the same BMAD methodology to `requirements/requirements.md` after `/requirements` has synthesised it. Eight dimensions tuned for finished-doc defects (completeness, ambiguity, testability, scope, dependency, consistency, edge cases, feasibility).

The synthesised seven-dimension structure is this reference's own contribution: it integrates BMAD's adversarial rule, Wiegers's quality categories, BABOK's stakeholder-coverage lens, Volere's measurement and satisfaction lenses, and IEEE 830's inspection scope into one auditable pass-per-dimension methodology applied to the raw consultant input corpus. The sampling / bias lens of Dimension 7 has no `/review-requirement` analogue — it is a defect of the input set itself that cannot exist in a finished doc.
