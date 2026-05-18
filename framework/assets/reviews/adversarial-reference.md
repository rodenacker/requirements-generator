<!-- ROLE: asset (P2 review reference). Loaded by framework/agents/reviews/adversarial-reviewer.md at activation. -->

# reviews/adversarial-reference.md

**Purpose:** Methodology reference for Adversarial Review of `requirements/requirements.md`. The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews/adversarial-reviewer.md` — drives the agent's eight-dimension process plus the quality-gate sweep.

**Output produced by the reviewer:** `review-requirements/ADVERSARIAL/adversarial-review.md` — a markdown punch-list of cited, severity-graded, dispositioned findings using `framework/assets/reviews/template-adversarial.md` as scaffold.

---

## What "adversarial review" means

Adversarial Review is the **opposite** of confirmatory review. A confirmatory reviewer asks "does this requirement look reasonable?" and returns "yes, mostly". An adversarial reviewer asks "in how many ways could this requirement fail when the engineer reads it next week?" and returns the list.

The discipline is rooted in the **BMAD method** (Breakthrough Method for Agile AI-Driven Development), an open-source agentic planning framework. BMAD's adversarial-review docs prescribe an uncompromising rule:

> *"Adversarial review is a review technique where the reviewer must find issues. No 'looks good' allowed. Zero findings trigger a halt — re-analysis becomes mandatory or justification required."*

The motivation: confirmation bias makes confirmatory reviewers useless. A reviewer who is permitted to return "clean" will return "clean" on a defective doc, because the path of least cognitive resistance is approval. Forcing the reviewer to find issues (or write an explicit, evidenced defense of why none exist) breaks the bias.

BMAD also warns of the symmetric failure mode:

> *"Because the AI is instructed to find problems, it will find problems — even when they don't exist."*

The mitigation is **human filtering**: the consultant's Accept/Revise/Restart loop at handback time. The reviewer is exhaustive; the consultant strikes false positives during Revise. False positives are part of the protocol, not a failure of it.

This reference operationalises BMAD's rule with explicit dimensions, a finding schema, a disposition rubric, and a halt contract.

---

## Upstream input contract

The reviewer reads **only** `requirements/requirements.md` (plus this reference, the character file, and the markdown template). It does not consult:

- `requirements/requirements-draft.md`, `requirements/source-manifest.json`, `requirements/consultant-answers.md`, `requirements/draft-claims*.ndjson` — pipeline-internal.
- `analyse-requirements/*` outputs (OOUX maps, JTBD job maps, Use Cases) — derived; reviewing the requirements doc against derivatives of itself would conflate "what the doc says" with "what the analyser inferred". The review's contract is to critique the source doc as the source doc.
- `design-system/*` outputs — not relevant to a requirements review.
- `framework/state/*` — pipeline state is not a review input.

The merged requirements document is the contract. If the doc doesn't say it, the doc doesn't say it — and that is a finding.

---

## The eight review dimensions

Eight dimensions, executed in order. Each is its own pass; the reviewer does not collapse passes. The dimension-by-dimension structure is what makes the review auditable: every finding maps to exactly one dimension, every dimension reports either ≥1 finding or a Justification block.

### Dimension 1 — Completeness & Gaps

**Question:** What is *not* here that should be?

**What to check:**

- Every user goal (`G-NN`) has at least one corresponding task flow and at least one corresponding requirement. Goals without flows are wishes; flows without requirements are sketches.
- Every requirement (`BR-NN`, `FR-NN`) has an acceptance criterion or a pass/fail predicate. Requirements without ACs are unimplementable.
- Every role mentioned in the doc (`§Target users`, `§Personas`) appears in the access-control matrix with explicit permissions. Roles without permissions are gaps.
- Every entity in the data model has its CRUD verbs covered by requirements. An entity that can be created but has no documented read/update/delete behaviour is a gap.
- Non-functional categories (performance, security, compliance, scale, observability, error-recovery) each have at least one explicit requirement. Absent NFRs are not "implied" — they are missing.
- Every external integration (auth, payments, email, SMS, storage) is named with its contract: protocol, payload shape, failure mode. Integrations referenced but not contracted are gaps.

**Common failure modes to scan for:**

- A user goal that the requirements doc never closes (`G-04 Receive notifications` mentioned in `§4`, but no `BR-NN` describes when, how, or to whom).
- A "shall support" verb followed by no detail (`"the system shall support reporting"` — supports *what*?).
- A role list that names "Admin" without defining what Admin can do that others cannot.

### Dimension 2 — Ambiguity & Clarity

**Question:** Is every requirement unambiguous to a reader who has not been in the consulting room?

**What to check:**

- Vague verbs: "support", "handle", "manage", "deal with", "be aware of", "consider". Each is a flag.
- Vague nouns: "user", "data", "item", "thing" — when the doc has a defined entity vocabulary, generic nouns indicate slip.
- Vague quantifiers: "many", "few", "some", "frequently", "occasionally", "in some cases".
- Vague time windows: "recent", "soon", "later", "after a while", "in the background".
- Pronouns with unclear antecedents: "it", "they", "this", "that" — especially across sentence boundaries.
- Hedge words: "may", "might", "could", "should" — when the requirement is meant to be mandatory, "may" creates a hole; when it is meant to be optional, "shall" creates a false obligation.

**Common failure modes to scan for:**

- *"BR-03 — the system shall handle approval workflow"* (vague verb, no flow, no roles).
- *"FR-12 — recently uploaded files appear at the top"* (recent = ?).
- *"G-02 — users can manage their settings"* (which users, which settings, what verbs?).

### Dimension 3 — Testability & Verifiability

**Question:** For every requirement, can a tester write a failing test today and a passing test on completion?

**What to check:**

- Each requirement has a pass/fail predicate. Wishes ("the system should feel fast") fail this; predicates ("the dashboard renders within 2s on a 50-row dataset") pass.
- Each non-functional requirement has a measurement: number, unit, sample, threshold. "Fast" is a wish; "p95 < 500ms over 1000 requests" is testable.
- Each acceptance criterion is decidable from the doc alone — no out-of-band consultant lookup required.
- Edge-case behaviour is named (empty state, max-size state, concurrent-update state, network-loss state, partial-failure state). "The system handles errors gracefully" is not testable; "on network loss, the form preserves draft state in localStorage and surfaces a retry banner" is.

**Common failure modes to scan for:**

- *"intuitive UI"* (untestable).
- *"reasonable performance"* (untestable without a threshold).
- *"appropriate error messages"* (untestable without enumeration).

### Dimension 4 — Scope & MVP Boundaries

**Question:** Is what is in scope clearly separated from what is out of scope?

**What to check:**

- The doc names an MVP explicitly. If it doesn't, every requirement is implicitly MVP, which usually means the doc has scope creep.
- "Nice-to-have" / "future" / "phase 2" requirements are clearly tagged. Untagged future work mixed with MVP requirements blurs the cut line.
- An explicit out-of-scope section exists. If the doc only says what *will* be built, the engineer infers everything else is also expected.
- No requirement straddles the MVP/post-MVP line. "Dashboard with optional advanced filters" is a smell — is the filter MVP or not?
- The cost of each requirement is at least estimable. A requirement that would clearly take three months in an MVP claimed to ship in six weeks is a scope failure.

**Common failure modes to scan for:**

- A 500-line requirements doc with no section titled "out of scope".
- A "stretch goals" subsection that reads like a second copy of the main requirements.
- A user role mentioned once (`Admin`) with no scope discussion of whether admin features are MVP or post-MVP.

### Dimension 5 — Dependency & Ordering

**Question:** Can the requirements be implemented in some buildable order, and is that order discoverable from the doc?

**What to check:**

- Implicit dependencies between requirements are named. *"G-04 Receive notifications"* depends on *"G-02 Have an account"*; if `G-04` doesn't say so, an engineer might start on it first.
- The data model is declared before requirements that depend on it. A requirement that references entity `Order.lineItems` before the data model defines `lineItems` is an ordering break.
- External integrations are sequenced. Auth before role-gated features; payment processor before checkout; email service before transactional emails.
- Phase transitions (MVP → phase 2) carry explicit dependency notes. "Phase 2 requires the data model from phase 1" is a load-bearing statement; its absence is a finding.
- No requirement references a concept the doc never defines.

**Common failure modes to scan for:**

- `BR-15` references a workflow defined nowhere in the doc.
- A "notifications" goal that doesn't say it depends on "user account creation".
- An entity used in `§7 Data entities` that wasn't introduced in `§2 Domain model`.

### Dimension 6 — Consistency & Internal Conflict

**Question:** Does any pair of statements in the doc contradict each other?

**What to check:**

- Two requirements that name the same field with different types, lengths, or constraints.
- The access-control matrix says "Approver can edit" while a flow says "only Importer can edit".
- A non-functional requirement says "p95 < 500ms" while a data section implies a 100-row report that would take >500ms to compute.
- Entity naming drift: `§2 Domain model > Order` vs `§5 Task flows > Purchase Order` vs `§7 Data entities > orders` — three names for one concept.
- Role naming drift: "Approver" in `§3 Target users`, "Reviewer" in `§4 User goals`, "approver" lowercase in `§6 Requirements`.
- A field is required in one section, optional in another.
- The Mermaid diagram or matrix in the doc contradicts the prose.

**Common failure modes to scan for:**

- A field whose type contradicts itself across sections.
- A role permission matrix that contradicts a flow narrative.
- A "max 100 items" constraint that contradicts a "supports bulk import of CSV" requirement with no row limit.

### Dimension 7 — Edge Cases & Error Handling

**Question:** What happens when the happy path breaks?

**What to check:**

- Empty states: what does each list/grid show when there are zero items?
- Maximum-size states: what happens at the row limit, the file-size limit, the character limit?
- Concurrent edits: two users edit the same record — who wins? Last-write? Conflict screen?
- Network failures: what does the UI show, what state is preserved, what retry is offered?
- Partial failures: a bulk import where 8/10 rows succeed — what is the surface?
- Authorization failures: what does an Approver see when they try to access an Importer-only screen?
- Input validation failures: invalid email, malformed date, oversize file — each named requirement should specify its validation behaviour.
- Idempotency: can the user re-submit the same operation safely?
- Recovery paths: undo, redo, restore-from-trash, recover-deleted, password-reset — which are required?

**Common failure modes to scan for:**

- A "file upload" requirement that names no max size, no virus check, no failure mode.
- A "shopping cart" requirement that doesn't say what happens to the cart after checkout, or after 30 days idle.
- An "approval workflow" requirement that doesn't say what happens if the approver is unavailable.

### Dimension 8 — Feasibility & Constraints

**Question:** Can this actually be built within the stated constraints?

**What to check:**

- Performance requirements have realistic thresholds for the stack the doc names (or implies). A "p95 < 50ms" requirement on a CRUD app over a 100k-row table without index discussion is suspect.
- Security/compliance requirements are concrete. For projects in the South African context (this framework's target), explicit **POPIA** treatment is required — data residency, PII handling, retention windows, consent flows.
- Scale targets are coherent. "1M users" in an MVP without infrastructure discussion is a flag.
- Cost / time / team-size constraints are mentioned at all. Their absence is a feasibility finding.
- Browser / device / OS targets are named. "Works on all browsers" is not feasible; "Chrome ≥110, Firefox ≥110, Safari ≥16, no IE" is.
- Accessibility targets are explicit. "Accessible" is not testable; "WCAG 2.1 AA" is.
- Operational requirements (logging, monitoring, alerting, backups, disaster recovery) are named. Their absence is a feasibility finding under "we will operate this in production but don't know how".

**Common failure modes to scan for:**

- POPIA-bearing data (ID numbers, addresses, financial info) handled without retention or consent requirements.
- A "real-time" requirement without a latency budget.
- A "scalable architecture" claim without a load model.

---

## Finding schema

Every finding has all eight fields populated, in this order:

```
ID:             ADV-NN          (sequential per run, zero-padded — ADV-01, ADV-02, …)
Dimension:      1..8            (which review dimension the finding maps to)
Severity:       Blocker | Major | Minor
Disposition:    Patch | Defer | Reject
Location:       §N.N | BR-NN | G-NN | FR-NN | line-N    (cite the most specific anchor available)
Evidence:       direct verbatim quote from requirements.md, ≤5 lines
Problem:        one sentence — what is wrong/missing/unclear
Recommendation: one sentence — concrete corrective action
```

**Field rules:**

- **ID** is unique per run and reset to `ADV-01` on every fresh invocation. Revise loops keep their IDs; only Restart resets the sequence.
- **Dimension** is exactly one integer 1–8. A finding that spans dimensions must be decomposed into one finding per dimension.
- **Severity** is exactly one of three. No "Critical" or "Trivial" or "Cosmetic".
- **Disposition** is exactly one of three (Patch / Defer / Reject). See the rubric below.
- **Location** uses the project's existing convention. Prefer the most specific anchor: an ID (`BR-03`) is better than a section (`§6.2`) is better than a line number (`line 247`). If multiple ID styles apply (a `BR-NN` that lives in `§6.2`), cite both: `§6.2 BR-03`.
- **Evidence** is a verbatim quote. Do not paraphrase. If the offending text is longer than 5 lines, decompose the finding into multiple findings each citing a ≤5-line slice.
- **Problem** is one sentence stating the defect. *"BR-03 says 'support approval workflow' with no flow, no roles, and no acceptance criteria"* — not *"BR-03 needs work"*.
- **Recommendation** is one sentence proposing a concrete change. *"Replace 'support approval workflow' with a Gherkin-style AC: 'Given a pending request, when an Approver clicks Approve, then the request transitions to Approved and the Importer is notified within 60s'"* — not *"clarify BR-03"*.

A finding missing any field is invalid. The quality-gate sweep enforces this.

---

## Disposition rubric (BMAD's three buckets)

BMAD categorises findings into three buckets: **Patch / Defer / Reject**. The reviewer assigns exactly one disposition per finding using this rubric:

### Patch

- The defect is **auto-fixable** by the consultant editing the requirements doc.
- Editing effort is **< 15 minutes**: rename, tighten, add a missing sentence, replace a vague verb with a concrete one.
- The defect does not require a stakeholder conversation, a design choice, or an architectural review.
- Examples: vague verb ("support" → "shall create, read, update, and delete"); missing time window ("recent" → "within 7 days"); missing field type; missing acceptance criterion on a clear requirement.

### Defer

- The defect is **real** and **specific**, but addressable in a later iteration without blocking the current scope.
- Common pattern: an edge case that affects post-MVP features; a non-functional requirement that doesn't gate MVP delivery; an integration whose absence is noticed but whose contract belongs to phase 2.
- Logged for the next requirements revision but does not block downstream consumption.

### Reject

- **Blocking.** The requirements doc cannot be consumed downstream until this is resolved.
- Common patterns: two requirements that directly contradict; an absent role-permission section that gates `/design-system`; a missing data-model anchor that prevents `/analyse-requirement` from running; a POPIA-bearing data flow with no compliance treatment.
- Any single Reject finding makes the overall verdict `BLOCKED`.

### Disposition → Verdict mapping

The artefact's Executive Summary states one verdict:

| Verdict | When |
|---|---|
| `BLOCKED` | At least one `Reject` disposition exists, **or** at least one Blocker severity finding exists. |
| `NEEDS-REVISION` | No Rejects/Blockers, but ≥1 finding total. |
| `ACCEPTED-WITH-FIXES` | Zero findings on all eight dimensions, **and** every dimension carries a non-empty Justification block. (Rare — strict-BMAD rule below makes this expensive.) |

There is no fourth verdict. "Looks good" is not a verdict.

---

## The strict-BMAD halt rule

**Zero findings on a dimension is a stop signal, not a success.**

If a dimension pass produces zero findings, the reviewer **must**:

1. State this in-thread: *"Dimension N — zero findings on first pass. Strict-BMAD rule fires: re-running with sharper skepticism."*
2. Re-run that dimension with explicit anti-confirmation prompts. For each requirement in the doc, force-articulate at least one way it could fail the current dimension's check. Add findings if any anti-confirmation produces a real defect.
3. If the re-run still produces zero findings, **write a `Justification` block** for that dimension in the artefact. The justification:
    - **Must** cite specific evidence (section numbers, IDs, sentences) that rules out each common failure mode listed for that dimension.
    - **Must** be at least 3 sentences. "Clean" is not a justification; "Every BR-NN in §6.2 carries a pass/fail predicate (e.g., BR-03's 'within 60 seconds'); §6.5 lists three measurable thresholds; no testability gap visible across the 14 reviewed requirements" is.
    - **Must** name the specific anti-confirmation prompts attempted in step 2 and why each failed to produce a finding.

4. **Never silently move on.** A dimension with zero findings and no justification block is a methodology violation; the quality-gate sweep treats it as a gate failure.

This rule applies independently to all eight dimensions.

---

## Output presentation

The artefact renders as a structured markdown report following `framework/assets/reviews/template-adversarial.md`. The fixed section ordering is:

1. **Header** — title, generated-at timestamp, requirements SHA-256, reviewer identity.
2. **Executive Summary** — total findings, severity tally, disposition tally, verdict line.
3. **Triage** — "Top issues to address first" callout (≤10 entries: every Reject and Blocker plus cluster-lead Majors). Lets the consultant resolve the highest-impact findings before scanning the full table.
4. **Clusters** — findings sharing a root cause grouped under a `CL-NN` cluster ID. Each cluster lists its member ADV-NNs and a one-line theme; the full detail for each finding still appears in the per-dimension sections below.
5. **Findings Table** — compact tabular view of every finding (ID, Dim, Sev, Disp, Cluster, Location, one-line problem), sorted Blocker → Major → Minor.
6. **Per-Dimension Sections (1–8)** — full findings for each dimension, or a Justification block if zero findings + strict-BMAD re-run passed.
7. **Diagnostics** — quality-gate results, coverage map (which sections each dimension touched), re-run log (which dimensions triggered the strict-BMAD re-run), provenance summary.

The artefact is a punch-list, not a narrative. Prose between findings is minimised; the consultant should be able to read the Triage callout in under two minutes, scan the Clusters block to see which findings share a root cause, and jump straight to the per-dimension section for context on any finding.

---

## Consolidation & Triage

After the eight-dimension sweep merges and IDs are assigned (Step 3b of `adversarial-reviewer.md`), one consolidation pass (Step 3c) annotates findings with **cluster IDs** and computes a **triage list**. The pass is a reader-aid: no finding is dropped, no finding's fields are rewritten, no `ADV-NN` is renumbered.

**Cluster rule.** Two or more findings cluster when they share a root cause — detected from a combination of section-level Location prefix (`§N`), anchor ID (e.g., `BR-07`), and load-bearing concept keywords in their `problem` field (e.g., MFA / step-up auth, retry, POPIA, RBAC matrix, FileSetting, availability/RTO, lockout). A cluster has ≥2 members; singletons are never clustered. Each finding belongs to at most one cluster. Cluster IDs are `CL-01`, `CL-02`, … assigned in order of each cluster's lead (lowest-ADV-NN) member.

**Triage rule.** The "Top issues to address first" callout selects up to 10 findings, deterministically, in this priority order:

1. Every Reject, in `ADV-NN` ascending order.
2. Every Blocker not already included, in `ADV-NN` ascending order.
3. Major findings that are the lead of a cluster of size ≥3, ordered by cluster size descending then lead `ADV-NN` ascending. (A large cluster fronted by a single fix is high-leverage.)
4. Remaining Major findings in `ADV-NN` ascending order.
5. Hard cap at 10. Never includes Minor findings.

**What this preserves.** Every quality gate is unaffected — `cluster_id` is metadata, not a 9th required schema field; the Findings Table row count still equals the sum of per-dimension counts (clustering does not drop, merge, or duplicate findings). The per-dimension sections render unchanged, in their original within-dimension order; the severity-driven sort applies only to the Findings Table. The deterministic ID assignment from Step 3b is final; Step 3c only annotates and selects.

**Why it exists.** A run with 80+ findings is correct but un-scannable. The Triage callout lets a consultant fix the must-fix-now list (typically 5–10 entries) in one sitting; the Clusters block lets them see that nine separate findings citing "step-up auth" share one underlying gap, so the fix list is shorter than the finding count. Both are navigation aids over the audit-grade detail that remains in the per-dimension sections.

---

## Quality gates (run after Dimension 8, before write)

Eleven gates. All are hard. If any gate fails, the reviewer does **not** write the artefact — it surfaces a structured error and halts. (See `framework/agents/reviews/adversarial-reviewer.md > Step 10 — Validate` for the halt contract.)

1. **Every finding has all eight schema fields populated.** Missing-field findings are invalid.
2. **Every finding's Dimension is exactly one integer 1–8.** Multi-dimension findings must be decomposed.
3. **Every finding's Severity is exactly one of `Blocker | Major | Minor`.**
4. **Every finding's Disposition is exactly one of `Patch | Defer | Reject`.**
5. **Every finding's Evidence field is a verbatim quote, ≤5 lines, that actually exists in `requirements/requirements.md`.** Paraphrased or fabricated evidence is a gate failure.
6. **Every finding's Location anchors a section, ID, or line that exists in the doc.** Citations to non-existent IDs are a gate failure.
7. **Every dimension reports either ≥1 finding or a non-empty Justification block.** Silent zero-finding dimensions are a methodology violation.
8. **Every Justification block (if any) cites specific evidence and is ≥3 sentences.** Stub justifications are a gate failure.
9. **The verdict line is consistent with the disposition tally** (any Reject or Blocker → `BLOCKED`; otherwise findings present → `NEEDS-REVISION`; zero findings everywhere → `ACCEPTED-WITH-FIXES`).
10. **The Findings Table row count equals the sum of per-dimension finding counts.** Drift is a render bug.
11. **The artefact's `REQUIREMENTS_SHA256` field matches the SHA-256 captured at Step 2.** Mismatch means the artefact analysed one version of the doc and reports against another.

---

## Anti-patterns

- **Returning "looks good".** The methodology forbids this. Re-run; write a justification; never silently pass.
- **Fabricating evidence.** Every Evidence field must be a verbatim quote from the requirements doc. If you cannot find a quote, you do not have a finding — drop it.
- **Generic findings.** *"`§6` could be clearer"* is not a finding. Cite the specific sentence; state the specific defect; propose the specific fix.
- **Severity inflation.** Calling every finding a Blocker dilutes the signal. Reserve Blocker for findings that genuinely prevent downstream consumption.
- **Disposition collapse.** Disposition (Patch / Defer / Reject) is orthogonal to severity. A Minor finding can be a Reject (e.g., a small but blocking POPIA gap); a Major finding can be a Defer (e.g., a significant feature gap that is genuinely post-MVP).
- **Collapsing dimensions.** Each dimension is its own pass with its own gate. Running them in a single combined sweep hides reasoning and breaks the diagnostics block.
- **Reviewing against derivatives.** Do not consult `analyse-requirements/*` outputs to triangulate findings. The review's contract is to critique `requirements/requirements.md` as the source of truth.
- **Inline `[SRC: ...]` markers.** Per project convention (`feedback_no_inline_provenance`), the merged requirements doc is clean of provenance markers; the review artefact is also clean. Findings cite by section/ID, not by `[SRC: ...]`.

---

## Voice and stance

The reviewer's stance is defined in `framework/assets/characters/adversarial-review.md` — skeptical, evidence-required, must-find-issues, no rubber-stamping. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

---

## References

- **BMAD method** — Breakthrough Method for Agile AI-Driven Development. Adversarial review docs at `docs.bmad-method.org/explanation/adversarial-review/`; core tools (including `bmad-review-adversarial-general` and `bmad-review-edge-case-hunter`) at `docs.bmad-method.org/reference/core-tools/`; repo at `github.com/bmad-code-org/BMAD-METHOD`. The "must find issues" rule, the Patch/Defer/Reject disposition bucket, and the false-positive caveat all originate here.
- **Karl Wiegers — Writing Quality Requirements** (`processimpact.com/articles/qualreqs.pdf`). Six requirements-quality dimensions: completeness, correctness, feasibility, necessity, prioritization, verifiability. Dimensions 1, 3, and 8 of this reference are direct descendants.
- **INVEST criteria for user stories** (Independent, Negotiable, Valuable, Estimable, Small, Testable). Dimension 5 (Dependency & Ordering) and Dimension 3 (Testability) draw from INVEST.
- **IEEE Std 830 — Recommended Practice for Software Requirements Specifications.** Establishes the formal review/inspection/walkthrough pattern for requirements docs. Dimensions 1, 2, 6, and 7 align with IEEE 830's checklist categories.

The synthesised eight-dimension structure is this reference's own contribution: it integrates BMAD's adversarial rule, Wiegers' quality categories, INVEST's testability lens, and IEEE 830's inspection scope into one auditable pass-per-dimension methodology.
