<!-- ROLE: asset (analysis reference). Methodology definition for the five-whys analyser. Modelled on framework/assets/analyses/task-flows-reference.md. Industry framing: Five Whys (Toyota Production System; Sakichi Toyoda 1930s, Taiichi Ohno 1950s) — root-cause interrogation, applied here to requirement justification (not pain analysis). -->

# Five Whys analysis reference

> **Method:** Auto-extract the **5 highest-priority candidate requirements for rationale analysis** from `requirements/requirements.md > §6 Requirements`, scored by Five-Whys-fitness category match (business goal / operational capability / workflow constraint / policy-driven behaviour) plus secondary signals (workflow anchors, modal strength, depth, implementation-detail penalty). Present the 5 to the consultant as a `multiSelect: true` prompt; let the consultant add additional requirements via the built-in Other input; anchor each consultant-stated requirement back to its `§6` source clause before analysing. For every requirement in the final analysis set, build a why-chain that interrogates **"why does this requirement exist?"** — drilling level by level toward the underlying user goal, business driver, or external mandate.

**Output file:** `analyse-requirements/FIVE-WHYS/five-whys.md` — a self-contained markdown document containing the scoring table, per-requirement why-chains, coverage checks, and diagnostics. **No template scaffold:** Five Whys is the first MVP analyser to exercise the registry's `template_asset: null` clause (pure markdown, no HTML / SVG / Mermaid).

**Analyser agent:** `framework/agents/analyses/five-whys-analyser.md`

**Character:** `framework/assets/characters/five-whys-analysis.md`.

---

## Industry framing — Five Whys (Toyota Production System)

Five Whys is the canonical root-cause technique of the Toyota Production System (TPS):

- **Origin.** Devised by **Sakichi Toyoda** (founder of Toyota Industries) in the 1930s; formalised by **Taiichi Ohno** in the 1950s as a core component of TPS and the Kaizen continuous-improvement philosophy. The technique is documented in Ohno's *Toyota Production System: Beyond Large-Scale Production* (1988).
- **Procedure.** Given a subject (problem, requirement, decision, incident), ask "why?" repeatedly until the chain terminates at an actionable root. Each answer becomes the next "why's" subject. The "5" is mnemonic, not literal — depth is whatever the **termination rule** requires.
- **Termination rule (canonical).** The **Corrective Action Test**: stop when fixing / understanding the named root cause would prevent recurrence (for pain analysis) or fully justify the surface subject (for justification analysis). If the team's answer is "yes, this is the actionable terminus," stop. If "maybe," keep asking.
- **Evidence-backed.** Every answer must be supported by evidence (logs, metrics, testimony, document quote) — not guessed. Unevidenced answers are the canonical failure mode.
- **Blame the process, not the person.** A Toyota rule: a why-chain that terminates at a named individual's "carelessness" or "negligence" is a defective chain. Root causes are systemic — process, training, tooling, incentive structure — not human shame.
- **Branching is allowed.** When a why-answer enumerates two-or-more causes, the chain forks. Each branch runs the same termination rule. Fishbone (Ishikawa) is the canonical visual overlay for fork-heavy analyses.
- **Common failure modes.** Stopping too early (terminating at a symptom); rephrasing the prior answer as the next answer (self-loop); blaming individuals; jumping to unevidenced guesses; padding to five when source is exhausted.

### Why apply Five Whys to requirement justification in this workspace?

Canonical Five Whys interrogates *pains* / *incidents* / *decisions*. The consultant has chosen to apply it to **requirements themselves** — the subject of each chain is a requirement clause in `§6`, and the chain asks *"why does this requirement exist?"*. This fills a real gap in the analysis set:

| Lens | Methodology | Question answered |
|---|---|---|
| Per-entity lifecycle | state-diagram | What states does this entity move through? |
| Per-scenario interaction | sequence-diagram | How do components talk to each other? |
| Multi-actor process flow | activity-diagram | Who does what, in what order? |
| Actor goals × main flows | use-cases | What does the user want to achieve? |
| Goal-decomposition + sequenced path | task-flows (HTA + TFD) | How does the user accomplish each task? |
| Core objects × CTAs × CCPs | ooux | What things does the system manipulate? |
| **Per-requirement justification** | **five-whys** | **Why does each requirement exist?** |

The other nine analyses decompose *what* the requirements describe. Five Whys is the first analyser whose primary output is a *justification audit*: it surfaces requirements with thin justification chains (a clause with no traceable driver), requirements whose root justification is named but not anchored in `§1` (coverage gaps), and requirements that share root justifications (consolidation opportunities).

### Why this analyser uses markdown, not HTML

Five Whys is causal-tabular text. There is no diagram component (no SVG, no Mermaid, no figure-pair structure). HTML scaffolding adds ceremony without value. The registry's `template_asset: null` clause exists precisely for this case — pure-markdown analyses compose the artefact as a string and write it directly, retaining the SHA-256 + min-bytes verify discipline that every analyser shares.

---

## Output structure

The artefact has a fixed top-to-bottom shape. No tier-1 / tier-2 split (single tier — every section is always rendered).

1. **Title + meta.** Title, generation timestamp, requirements SHA-256.
2. **Summary.** Counts: auto-extracted (≤5), category mix, consultant-stated additions, total analysed, total why-levels, root-justifications-identified, incomplete chains, coverage gaps, AI-suggested rows + density.
3. **Rationale-analysis priority scoring (Round 1 table).** One row per auto-extracted candidate. Columns: Rank, Requirement (short title + verbatim quote), Source (`§6.N`), Detected categories (primary first), §5 anchors (count + sections), §4 anchors (count + sections), Modal, Other refs (count + sections), Depth, Impl-detail penalty, Score.
4. **Per-requirement sections.** One `## Requirement {n}` block per requirement in the final analysis set (extracted + anchored-consultant-stated). Each block carries:
   - Source line (origin + anchoring details if consultant-stated)
   - Detected categories
   - Statement (verbatim)
   - Why-chain table: Level | Why? | Answer | Evidence | Provenance
   - Termination row: PASS (Justification Sufficiency Test) | INCOMPLETE | CAP
   - Coverage check: `cited` (with location) or `gap` (with consultant guidance)
5. **Diagnostics.** Quality-check results (10 PASS / FAIL lines + flagged items), AI-suggested density, cross-requirement links, dropped-requirements notes, cap notes, Override flag-list if applicable.

---

## Source-of-truth hierarchy

The analyser walks `requirements/requirements.md` in this order:

1. **`§6 Requirements`** — primary. Every top-level clause is a candidate for Round 1 scoring. The clause's full text drives Five-Whys-fitness category detection.
2. **`§5 Task flows`** — workflow-relevance signal. Anchor counts feed the secondary score; chain construction uses `§5` *Steps* and *Decision points* as evidence sources for derived why-answers.
3. **`§4 User goals & stories`** — user-visibility signal + chain evidence. A requirement's "why" often terminates at a `§4` *Objective* clause (a user goal the requirement implements). Anchor counts feed the secondary score.
4. **`§1 Application context`** — business / domain context. The why-chain's deepest levels often terminate here: business drivers, market positioning, regulatory framing.
5. **`§3 Target users`** — persona context for chains whose root justification is user-need-driven.
6. **`§7 Data entities`** — informs the chain when a requirement constrains a named entity (e.g., audit-trail requirements often trace to entity-level data-retention drivers).
7. **`§2 Domain model`** — supplementary; cited when a requirement is justified by domain invariants.

If `§6` is empty, the analyser halts cleanly with the same structured error pattern as other analysers (Round 1 returns zero candidates → consultant prompted with empty-list note).

---

## Round 1 — Identify the 5 highest-priority candidate requirements for rationale analysis

Walk `§6 Requirements` extracting every top-level clause. Each candidate carries:

```
{
  candidate_id,
  requirement_statement (verbatim),
  source: "§6.N",
  depth,
  modal ∈ {"must", "shall", "should", "may"},
  §5_anchors: [{ref, snippet}],
  §4_anchors: [{ref, snippet}],
  other_refs: [{ref, snippet}],
  detected_categories: [{name, evidence_snippet}]  # primary listed first
}
```

### Category match (primary signal — `+4` per matched category, no upper bound on multi-category matches)

Five Whys works best on four kinds of requirements. Detect each via lexical / structural patterns:

#### `[BUSINESS-GOAL]`

Outcome-oriented language tying the requirement to a stated business outcome.

- **Outcome verbs:** *achieve*, *deliver*, *enable*, *grow*, *reduce*, *increase*, *maximise*, *minimise*, *improve*.
- **Quantified targets:** numbers + units, percentages, KPIs (e.g., *"reduce processing time by 40%"*, *"support 10,000 active users"*).
- **Goal nouns:** *goal*, *objective*, *target*, *outcome*, *KPI*, *metric*.
- **Rationale connectives:** explicit *"in order to ..."*, *"so that ..."*, *"to achieve ..."*.

#### `[OP-CAPABILITY]`

Capability declarations — what the system must do, expose, integrate with, or handle.

- **Capability verbs:** *support*, *handle*, *process*, *integrate with*, *interoperate with*, *expose*, *accept*, *provide*.
- **Volume / performance modifiers:** *concurrent*, *per second*, *throughput*, *latency*, *SLA*, *availability*, *uptime*.
- **Capability shape:** *"the system must [verb] [object]"*, *"must support [N] [units] [object]"*, *"must integrate with [system]"*.

#### `[WORKFLOW-CONSTRAINT]`

Conditional or gating phrases that shape user / system workflows.

- **Gating phrases:** *must X before Y*, *only when ...*, *only if ...*, *requires ...*, *subject to ...*, *prerequisite*, *X is blocked until Y*, *X cannot proceed without Y*.
- **Approval shape:** *approval required*, *approved by*, *cannot ... without sign-off*.
- **Ordering shape:** *X must precede Y*, *Y is only available after X*.

#### `[POLICY-DRIVEN]`

Explicit external / internal policy references.

- **Regulatory citations:** *GDPR*, *PCI-DSS*, *PCI*, *SOX*, *HIPAA*, *ISO 27001*, *ISO*, *NIST*, *FCA*, *MiFID*, *FATCA*, *AML*, *KYC*.
- **Compliance / standard nouns:** *compliance*, *regulation*, *regulatory*, *standard*, *policy*, *audit*, *retention*, *data residency*, *segregation of duties*.
- **Internal-policy markers:** *two-person approval*, *four-eyes*, *audit trail required*, *non-repudiation*, *immutable record*.

A clause may match multiple categories (e.g., a workflow-constraint that is policy-driven). The **primary category** is the one with the strongest evidence (most pattern matches; ties broken by registry-listed order: business-goal > op-capability > workflow-constraint > policy-driven). All matched categories are recorded; the primary is surfaced first in the consultant prompt and the scoring table.

### Secondary signals

- `+2` per anchor in `§5 Task flows` — a task flow exercises or depends on this requirement (workflow relevance).
- `+1` per anchor in `§4 User goals & stories` — the requirement implements a user-visible goal.
- `+2` if modal ∈ {*must*, *shall*}; `+1` if {*should*}; `0` if {*may*} — mandatory requirements are higher-priority for rationale audit.
- `+1` per cross-reference from `§1 Application context` or `§7 Data entities`.

### Penalties

- `−2` if depth ≥ 2 (sub-clause, not top-level). Top-level clauses are the unit of rationale; sub-clauses are typically operational refinements.
- `−3` if the requirement matches an **implementation-detail** pattern. Five Whys produces shallow chains on these (their "why" terminates at "we decided to" in one step). Patterns:
   - Specific UI labels in quotes (e.g., *"the 'Submit Order' button"*, *"the label reads 'Cancel'"*).
   - Exact field-name references (e.g., *"the customer_id field must be 12 chars"* — unless the field-shape is itself a policy-driven constraint, in which case `[POLICY-DRIVEN]` wins).
   - Exact screen layouts (*"three columns, sidebar on the left"*).
   - Exact error-message text (*"display 'Invalid input'"* — unless the message text is regulatorily mandated).
   - Pixel / colour / typography values.

### Selection rule

Select the top 5 by score. Ties broken by ordinal position in `§6` (lowest first). If fewer than 5 candidates exist, surface all candidates (Round 2 prompt notes the under-supply).

### No-category-match handling

A candidate with **zero category match** can still appear in the top 5 (if `§6` is sparse in better candidates). Stamp the candidate `[NO-CATEGORY-MATCH — Five Whys may yield a shallow chain]` and surface this stamp in the Round 2 prompt + scoring table. The chain still runs; the marker is an honest signal to the consultant.

### Score narration

State the scoring aloud in one line per selected candidate so the consultant can audit the decision: *"`§6.BR-04` `[WORKFLOW-CONSTRAINT]` (+4) + `[POLICY-DRIVEN]` (+4), 2 anchors in §5 (+4), 1 anchor in §4 (+1), modal `must` (+2) → score 15. Detected categories: workflow-constraint (primary), policy-driven."*

---

## Round 2 — Consultant selection + Other input

Surface a single `AskUserQuestion` with `multiSelect: true`:

- **Question:** *"The 5 highest-priority candidate requirements for rationale analysis are listed below. Five Whys works best on **business goals, operational capabilities, workflow constraints, and policy-driven behaviour** — each candidate is tagged with its detected category. Implementation-detail requirements (UI labels, error-message text, exact layouts) have been deprioritised. Pick any subset to analyse. You can also choose Other to state another requirement (in your own words or as a verbatim quote) — the analyser will locate it in `requirements/requirements.md` and analyse it from there. Empty selection plus no Other is valid and produces a scoring-summary-only output."*
- **Header:** `Requirements`
- **multiSelect:** `true`
- **Options:** one per extracted candidate, labelled `{short_title} — §6.N [{PRIMARY-CATEGORY}] (score {S})`. First option suffixed `(Recommended)` if it has the highest score.

Capture: `selected_extracted: Set[candidate_id]`, `stated_by_consultant: List[free_text]` (one per Other selection — re-prompt for additional statements if needed).

Empty selection (no extracted + no Other) is valid; the artefact will contain Summary + scoring table + diagnostics only.

---

## Round 3 — Anchor consultant-stated requirements

For each entry in `stated_by_consultant`, locate it in `requirements/requirements.md`. The anchoring is a **requirement-document-only** operation — the analyser refuses to analyse a consultant-stated requirement that cannot be anchored.

### Anchoring procedure

1. Tokenise the consultant text on whitespace + punctuation; drop English stopwords (*the*, *a*, *an*, *of*, *to*, *and*, *or*, *is*, *are*, *be*, *will*, *would*).
2. For each top-level `§6` clause, compute the token-overlap ratio: `matched_tokens / max(consultant_tokens, clause_tokens)`. (Symmetric ratio penalises both spurious matches and partial coverage.)
3. Classify by best-match ratio:
   - **Strong match (≥ 60%)** with a single clause → surface confirmation prompt (see below).
   - **Multiple candidates (each ≥ 40%)** → surface pick-one prompt with the top 3.
   - **No match (top ratio < 40%)** → surface rejection prompt.

### Strong-match confirmation

`AskUserQuestion`:

- **Question:** *"You stated: `{consultant_text}`. The closest match in requirements.md is `§6.N: {full clause}` (`{pct}`% token overlap). Use this section as the source, pick a different section, or refine your statement?"*
- **Header:** `Anchor`
- **Options:** `Use this section (Recommended)`, `Pick another match — show me alternatives`, `Refine — let me restate`.

### Multiple-candidates pick-one

`AskUserQuestion`:

- **Question:** *"Multiple sections in requirements.md partially match your statement. Pick the one you meant:"*
- **Header:** `Anchor`
- **Options:** one per top-3 match, labelled `§6.N — {full clause} ({pct}%)`. Final option `Refine — none of these match`.

### No-match rejection

`AskUserQuestion`:

- **Question:** *"`{consultant_text}` does not appear in `requirements/requirements.md`. Analyses extract from the requirements doc — they cannot interrogate requirements that aren't in the document. Options: refine the statement to match an existing requirement, specify the §6.N section manually if the analyser missed a match, or drop this requirement from the run."*
- **Header:** `Not in requirements`
- **Options:** `Refine — let me restate`, `Specify §6.N manually`, `Drop — exclude from this run`.

### Recording

On `Use this section` (or successful manual `§6.N` specification): record `{statement: <anchored clause verbatim>, source: §6.N, consultant_stated: true, overlap_pct: {pct}}` and add to the analysis set.

**Never analyse an un-anchored consultant-stated requirement.** This invariant preserves the stand-alone-ish constraint (analyses read only `requirements/requirements.md`) and the SHA-256 traceability claim.

---

## Round 4 — Why-chain construction (per analysed requirement)

For each requirement in the final analysis set (extracted + anchored-consultant-stated), build a why-chain. The chain interrogates *"Why does this requirement exist?"*.

### Source-of-truth hierarchy per chain level

Evaluated in order at every level:

1. **`from-requirements`** — `§1 Application context`, `§4 User goals & stories` *Objective* clauses, or explicit rationale phrases in `§6` (*"to ensure ..."*, *"because ..."*, *"this exists to ..."*, *"in order to ..."*, *"so that ..."*) name the justification. Quote verbatim into the Evidence column with the source ref.
2. **`derived-from-§N`** — no explicit "why" phrase, but the requirement plainly implements a user goal from `§4` or a context-driver from `§1` (logical implication, not text match). The Evidence column cites the section + a one-line derivation note explaining the inference.
3. **`ai-suggested`** — neither of the above; the analyser proposes a plausible next-why. Row text prefixed with `[AI-SUGGESTED]`; an inline Rationale column states *why this inference and not another*.

### Termination rule (evaluated in order)

1. **PASS — Justification Sufficiency Test.** A row's answer names an **axiomatic / immutable driver**:
   - Regulatory mandate (e.g., *"GDPR Art. 17 right-to-erasure"*) — provenance must be `from-requirements` or `derived-from-§1`.
   - Market reality (e.g., *"customers expect mobile-first interaction"* with explicit `§1` anchor).
   - Stakeholder mandate (e.g., *"board-approved Q3 priority"* with explicit `§1` anchor).
   - A `§4 User goals` *Objective* that the analyser cannot meaningfully ask "why" of without leaving the requirements doc (the user's goal is the rationale terminus by definition — going further requires interview data).

   Stop. Mark the row `Root justification: yes; sufficiency-test: pass`.

2. **INCOMPLETE — source exhausted.** Three consecutive levels are `ai-suggested`, OR no source supports the next why at any provenance tier. Stop. Mark the final row `[INCOMPLETE: insufficient-source-detail — consultant interview needed to anchor root justification]`. **Never pad to five.**

3. **CAP — depth limit.** 7 levels reached. Cap-aloud. Mark the final row `[INCOMPLETE: cap-reached — chain capped at 7 levels; further drilling did not converge on an axiomatic driver]`. Same INCOMPLETE marker plus cap notice in diagnostics.

### Per-chain minimum

**No fewer than 1 why-row per requirement.** A requirement that drills to zero why-rows is **dropped** from the analysis set with a single-line diagnostics note: *"Requirement `§6.X` could not be drilled — no anchor in §1, §4, or §5. Consultant interview needed."* The dropped requirement does **not** appear as an empty chain in the artefact.

---

## Round 5 — Branching (multi-driver requirements)

When a why-row's answer in the requirements explicitly enumerates two-or-more drivers, emit branched sub-chains. Triggers:

- *"to satisfy both X and Y"*
- *"caused by either A or B"*
- *"justified by both regulatory compliance and user-experience goals"*
- Comma-separated multi-driver enumeration in a single rationale phrase.

Each sub-chain runs the same Round 4 termination rules independently. Identifier scheme: `R{n}.B1`, `R{n}.B2`, ….

**Cap: 3 sub-chains per requirement.** On overflow, cap-aloud, surface the first 3 by source order, list the rest in diagnostics as *"requirement `R{n}` has {N} enumerated drivers — surfacing the first 3 (`{labels}`); excluded: `{rest}`"*.

If no multi-driver enumeration is detected at any level, the requirement has exactly one chain (no branching) — this is the common case.

---

## Round 6 — Coverage check

For each chain (and each sub-chain branch), perform a **binary text-search check** asking *"Does the requirements doc adequately reference the named root justification?"*

### Procedure

1. Extract the root justification label (the final-row Answer text, or `[NO-ROOT — INCOMPLETE]` if the chain terminated INCOMPLETE).
2. Tokenise the label; drop stopwords.
3. Search `§1 Application context` and all `§6` clauses for any token overlap ≥ 50% with the label tokens.
4. **If a match is found:** row `coverage: cited` with location (e.g., *"`§1` Application context line 12: 'GDPR compliance is a core constraint'"*).
5. **If no match is found:** row `coverage: gap — root justification named but not anchored in requirements.md; consultant should add the cite to §1 or §6`.
6. **If the chain is INCOMPLETE:** row `coverage: n/a — chain did not reach an actionable root justification`.

### Invariant

Coverage is a **binary text-search outcome**, not an inference. Markers ∈ `{cited, gap, n/a}` only. **Never `[AI-SUGGESTED]` a coverage assertion.**

This replaces the classic Five Whys "countermeasures" section. Countermeasures are authoring (proposing solutions); coverage is extraction (does the doc cite its own justification?). The analyser is the latter, not the former.

---

## Round 7 — Cross-requirement consistency

After all chains have been built and Round 6 has run, detect cross-requirement links:

- For every pair of (chain, sub-chain) terminations across the analysis set: compute the token-overlap ratio between the two root-justification labels (after stopword removal and lemma normalisation).
- If overlap ≥ 70%, emit a cross-requirement note in diagnostics: *"Requirements `R{a}` and `R{b}` trace to the same root justification (`{shared_label}`) — consider consolidating in §6 or documenting the shared driver explicitly in §1."*

Soft note, **not a merge**. Each chain is rendered independently in the artefact; the diagnostics block surfaces the shared-root signal so the consultant can act on it.

---

## Provenance markers (4 — exhaustive)

Every row in every why-chain table carries exactly one of:

| Marker | Markdown rendering | When |
|---|---|---|
| `from-requirements` | `from-requirements` | The why-answer is justified by an explicit rationale phrase in `§1`, `§4`, or `§6` (*"to ensure ..."*, *"because ..."*, *"in order to ..."*, *"so that ..."*). Quote verbatim into Evidence. |
| `from-§N` | `from-§N` (literal section number) | The why-answer is a verbatim *Objective* / context statement / business driver text in `§N` (typically the Requirement-row entry itself or the terminal-driver row). Quote verbatim into Evidence. |
| `derived-from-§N` | `derived-from-§N` (literal section number) | The why-answer is logically implied by `§N` but not verbatim. Evidence carries a one-line derivation note explaining the inference. |
| `ai-suggested` | `ai-suggested` | The why-answer was inferred by the analyser. Row text prefixed with `[AI-SUGGESTED]`. Evidence column carries the analyser's Rationale explanation. |

Every coverage row carries exactly one of `{cited, gap, n/a}` (Round 6 invariant — never `ai-suggested`).

No fifth provenance marker. No row unmarked. Honours the framework-wide `feedback_ai_suggested_invariant`.

---

## Quality checks (10 hard gates + 1 soft warning)

Run after Round 7. All hard checks operate on the in-memory analysis set — they are independent of the markdown rendering step.

### Hard checks

1. **Every analysed requirement statement is sourced** (`from-§6.N`); none is invented. Consultant-stated requirements must have been anchored in Round 3 with `overlap_pct` recorded.
2. **The Round 1 scoring computation is captured in memory and rendered to the artefact** (5 rows or fewer if `§6` thin; each row carries the score breakdown — categories, anchors, modal, refs, depth, penalty, score). Auditability invariant.
3. **Every retained chain has ≥ 1 why-row.** Requirements that drill to zero rows are dropped (per Round 4 minimum) with a diagnostics note. The artefact never contains an empty chain.
4. **Every why-row carries exactly one provenance marker** — never zero, never two. Markers ∈ `{from-requirements, from-§N, derived-from-§N, ai-suggested}`.
5. **Every why-row has a non-empty Evidence column** citing the source section. Even `[AI-SUGGESTED]` rows cite the section whose absence motivated the inference (e.g., *"§1 (no business-driver text found for this level)"*).
6. **No why-row blames a named individual or role with shame language.** Forbidden tokens (case-insensitive): *user error*, *operator failed*, *negligence*, *carelessness*, *stupidity*, *incompetence*. (Toyota rule.)
7. **No why-row recursively rephrases the prior row's answer.** Compute Jaccard similarity between consecutive answer-row token sets (after stopword removal). Fail if similarity ≥ 0.80 — that's a self-loop, the canonical Five Whys failure mode.
8. **Every chain terminates exactly once** with one of `Root justification: yes` (PASS), `[INCOMPLETE: insufficient-source-detail]`, or `[INCOMPLETE: cap-reached]`. Never zero terminators, never two.
9. **Caps respected.** 5 auto-extracted (or fewer if `§6` thin); consultant additions anchored via Round 3; ≤ 7 why-levels per chain; ≤ 3 branches per requirement.
10. **Every coverage row is `cited`, `gap`, or `n/a`** — never `[AI-SUGGESTED]`. Round 6 invariant.

### Soft check (warning, not gate)

- **AI-suggested density.** Compute `density = ai_suggested_rows / total_why_rows` across all chains. If `density > 0.40`, emit a `density-warning` line in diagnostics and in the handback summary: *"Justification chains are largely inferred — `requirements/requirements.md` does not establish the why-structure. Enrich `§1 Application context` with explicit business drivers and `§4 User goals & stories` with explicit objectives, then re-run for higher-confidence chains."* Non-blocking.

### Failure handling

On any hard-check failure: do **not** write the artefact. Surface `AskUserQuestion` with three options:

1. `Revise requirements — exit so the consultant can edit requirements/requirements.md and re-invoke /analyse-requirement (Recommended)`
2. `Override — proceed and write a known-incomplete artefact (the diagnostics block will record every violation)`
3. `Restart — re-run from Round 1 with a fresh extraction`

On **Revise**: hand back to the orchestrator with a `failed-handback` state.
On **Override**: record each failing check in the diagnostics block, then proceed to render.
On **Restart**: re-enter Round 1. Do not loop more than three times in a single invocation; on the fourth fail-and-restart, force the Revise path with a one-line note that further iteration is not productive without consultant input.

---

## Stop-condition

The analysis is complete when:

- Every retained candidate has a row in the Round 1 scoring table.
- Every requirement in the analysis set has a complete `## Requirement {n}` section with a chain table, termination row, and coverage row.
- The Diagnostics section reports the 10 hard-check results, AI-suggested density, cross-requirement links (if any), dropped-requirements notes (if any), and cap notes (if any).
- All 10 hard quality checks pass, or the consultant chose Override.
- The consultant chose Accept in the Step 13 accept/revise/restart loop.

---

## Input-coverage asymmetry

`§6 Requirements` carries the clauses but rarely carries their justifications inline. The asymmetry mirrors task-flows' asymmetry (§5 carries steps but rarely carries actor / completion / plan signals):

- **Business-goal justification.** Often stated only in `§1 Application context`. The analyser cross-references requirement keywords with `§1` text to detect implicit goal anchoring.
- **User-goal justification.** Often inferred from `§4 User goals & stories` *Objective* clauses. The analyser walks `§4` looking for *Objective* statements that match a requirement's domain noun.
- **Policy / regulatory justification.** Sometimes cited inline in `§6` (good case); often stated only in `§1` (typical case); sometimes nowhere in the requirements doc (coverage-gap case — surfaced in Round 6).
- **Workflow-constraint justification.** Often justified by `§5 Task flows` *Decision points* or *Exception paths*. The analyser walks `§5` for matching constraint phrases.

Richer inputs (rationale-rich `§1`, explicit *Objective* clauses in `§4`, regulatory cites in `§6`) → richer chains. Methodology degrades gracefully: with thin inputs, chains are mostly `ai-suggested` and the soft density warning surfaces this. The right consultant action is to enrich the requirements doc and re-run, not to override silently.

---

## Output shape (markdown)

The artefact is a single self-contained markdown file at `analyse-requirements/FIVE-WHYS/five-whys.md`. No template scaffold — the analyser composes the markdown string directly from in-memory tables. Top-to-bottom section order is fixed.

### Header block

```markdown
# Five Whys Justification Analysis — {domain}

Generated: {ISO-8601 UTC}
Requirements SHA-256: {sha256 of requirements/requirements.md}
```

`{domain}` is verbatim from `§1 Application context > Domain` if present, else *"(not declared in requirements.md)"*.

### Summary block

```markdown
## Summary

- Candidate requirements auto-extracted for rationale analysis: {N≤5}
- Category mix: {n_business_goal} business goals, {n_op_capability} op capabilities, {n_workflow_constraint} workflow constraints, {n_policy_driven} policy-driven, {n_no_category} no-category-match
- Consultant-stated requirements analysed: {M}
- Total requirements analysed: {N_used + M}
- Total why-levels: {L}
- Root justifications identified (PASS Sufficiency Test): {R}
- Incomplete chains (source exhausted or cap-reached): {I}
- Coverage gaps: {G}
- AI-suggested rows: {A} ({A/L%} density)
```

### Scoring block

```markdown
## Rationale-analysis priority scoring (Round 1)

| Rank | Requirement | Source | Detected categories (primary first) | §5 anchors | §4 anchors | Modal | Other refs | Depth | Impl-detail penalty | Score |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | {short_title} | §6.BR-04 | [WORKFLOW-CONSTRAINT], [POLICY-DRIVEN] | 2 (§5.1, §5.3) | 1 (§4.2) | must | 1 (§1) | 1 | 0 | 15 |
| 2 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

### Per-requirement block (one per requirement in the analysis set)

```markdown
## Requirement {n} — {short-title} `[PRIMARY-CATEGORY]`

**Source:** `§6.N` (`from-§6` — auto-extracted) *or* `§6.N` (`from-§6` — consultant-stated, anchored via {pct}% token match)
**Detected categories:** {primary}, {others...} *or* `[NO-CATEGORY-MATCH — Five Whys may yield a shallow chain]`
**Statement** (verbatim): "{requirement quote}"

### Why chain R{n}

| Level | Why? | Answer | Evidence | Provenance |
|---|---|---|---|---|
| Requirement | — | {requirement text} | §6.N | from-§6 |
| Why 1 | Why does this requirement exist? | {answer 1} | §4.X "..." | from-requirements |
| Why 2 | Why {answer 1}? | [AI-SUGGESTED] {answer 2}. *Rationale: {one-line analyser explanation}* | §1 (no business-driver text found for this level) | ai-suggested |
| ... | ... | ... | ... | ... |
| Why k | Why {prior}? | **Root justification: {answer k}** | §1.X "..." | from-requirements |

**Termination:** PASS — Justification Sufficiency Test satisfied: root names an axiomatic driver (`§1.X`).
*(or: **INCOMPLETE** — three consecutive `ai-suggested` rows; consultant interview needed.)*
*(or: **CAP** — 7-level depth limit hit; chain did not converge on an axiomatic driver.)*

### Coverage check

Root justification `{label}` — `cited` (anchored in `§1.X`: *"{cite quote}"*).
*(or: `gap` — root justification named but not anchored anywhere in §1 or §6; consultant should add the cite.)*
*(or: `n/a` — chain did not reach an actionable root justification.)*

---
```

If the requirement has Round 5 branches, render one `### Why chain R{n}.B{m}` sub-section per branch, each with its own termination row and coverage row.

### Diagnostics block

```markdown
## Diagnostics

- Quality checks: {n_pass}/10 pass
  - PASS: check-{i}, check-{j}, ...
  - FAIL: check-{k} — flagged items: {list of {requirement_id, row_no, reason}}
- AI-suggested density: {pct}% ({A}/{L})
- Cross-requirement links:
  - R{a} and R{b} share root justification "{label}" — consider consolidation in §6 or anchor in §1.
- Dropped requirements (zero-why-rows):
  - R{x}: {note}
- Coverage gaps: {G} chains terminated at justifications not anchored in §1 or §6.
- Cap notes: ...
- (On Override:) Quality-check violations accepted as known. Flagged items: ...
```

---

## Downstream consumption (handled by `framework/skills/map-five-whys-to-ui.md`)

The analyser does not author solutions, so the downstream mapping is **signal-based**, not affordance-based:

- **Thin-justification chains** (chains with high `ai-suggested` density or INCOMPLETE termination) → flagged for consultant interview before design proceeds. A requirement without traceable justification is unsafe to design against.
- **Coverage gaps** (root justifications named in chains but not anchored in `§1` or `§6`) → flagged for `/requirements` enrichment. The consultant adds the cite, re-runs `/requirements`, re-runs Five Whys.
- **Cross-requirement consolidation candidates** (multiple requirements sharing a root justification) → flagged for `/requirements` consolidation review.
- **Policy-driven requirement chains** terminating at regulatory cites → routed to compliance-pattern-catalogue entries in the design system.
- **Business-goal requirement chains** terminating at quantified targets → routed to KPI-dashboard-pattern entries.

`framework/skills/map-five-whys-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character file and for future downstream design-spec authors.
