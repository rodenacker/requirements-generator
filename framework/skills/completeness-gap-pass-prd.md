# completeness-gap-pass-prd.md

**Purpose:** Walk a populated PRD draft against the bijection invariants in `framework/assets/topics-prd.md` and decide for each gap whether to fabricate the missing element with `[AI-SUGGESTED: PAI-NNN]` or accept that no fabrication is needed. Used by the `prd-drafter` agent at workflow step 4 (post-fill, pre-write-final).

Distinct from `framework/skills/completeness-gap-pass.md` (the requirements-pipeline gap-pass): the PRD gap-pass has a smaller decision tree (only two possible marker outcomes — `[SRC: PC-NNN]` or `[AI-SUGGESTED: PAI-NNN]`), no general-rules lookup, no out-of-scope routing, and no visual-manifestation Tier D. The PRD's invariants are PRD-specific (B1–B10) and the requirements-pipeline invariants (A1–A15, B1–B5) do not apply here.

**Inputs:**
- The in-memory populated PRD draft (template-prd.md filled top-to-bottom from inputs and inferred fills; **no `[AI-SUGGESTED]` markers yet**).
- `framework/assets/topics-prd.md` — bijection invariants B1–B10 (Tier A) and SB1–SB3 (Tier B soft).

**Outputs:**
- A list of `(rule_id, location, action, marker_kind, marker_payload, draft_context)` tuples that the drafter applies to the draft via Edit / Write.
- The next-available `PAI-NNN` index, continuing the existing counter.

`draft_context` is a single, one-line string emitted on tuples whose `marker_kind = "AI-SUGGESTED"`. It is a brief, plain-English orientation for the consultant — what the field represents, what kind of answer is expected, and (when useful) the candidate value set — phrased so the consultant can answer without re-locating the cell in the draft. Example for a §5.2 metric baseline: `"§5.2 success metric M-03 baseline — what is today's median underwriting cycle time? (typical: 24-72 hours for SMB lending)"`. Example for a §6.1 falsification condition: `"§6.1 H-04 — what observable signal would prove the hypothesis wrong? (specific, measurable, time-bounded)"`. Tuples carry no `draft_context` if their `marker_kind = "none"` (which only happens when an input quote fully grounds the field).

## Decision tree (per gap)

For every field or element required by the template that is not directly stated in the inputs, walk these steps in order. Stop at the first match.

1. **Stated-in-inputs.** If the inputs supply a verbatim quote that grounds the value, use it. **No marker — append `[SRC: PC-NNN]` and emit a sidecar line.** (Handled by drafter step 2 against the populated template, not by this skill — included for completeness.)
2. **Required by Tier A bijection (B1–B10).** If the field/element is required by a B-NN rule below, fabricate the missing element. Marker: `[AI-SUGGESTED: PAI-NNN | blocking|non-blocking]` per the drafter's classification rubric (`framework/agents/prd-drafter.md > Classification`).
3. **Tier B soft (SB1–SB3).** Emit a warn-only flag to the drafter's gap-pass log. **No fabrication, no marker.**
4. **Template-required, not stated, not B-bijection-gated.** Fabricate with a domain-default inference. Marker: `[AI-SUGGESTED: PAI-NNN | non-blocking]`. The PRD pipeline emits no `[OUT-OF-SCOPE]` and no `[STANDARD-RULE]` — every fabricated value either confirms an input citation or becomes a Q&A item.

The PRD pipeline has **no `[STANDARD-RULE: GR-NN]` path** (the `GR-NN` rules govern UI behaviour, not PRD content). The PRD pipeline has **no `[OUT-OF-SCOPE: domain-default]` path** (§10 is the out-of-scope section; a marker inside §10 saying "out of scope" would be self-referential). Every gap that is not a `[SRC:]` citation becomes an `[AI-SUGGESTED]` marker.

## Tier A — hard bijections (gap → fabricate + `[AI-SUGGESTED]`)

| # | Rule | Fabrication action |
|---|---|---|
| B1 | Every §5.2 M-NN cites at least one §2 problem or §6 hypothesis in its `Tied to` cell | resolve the cross-reference; if no plausible §2 problem or §6 hypothesis exists yet, fabricate one in the cited section first (with `[AI-SUGGESTED]`) before back-referencing. |
| B2 | Every §6.1 H-NN row's `Falsification condition` cell is non-empty and observable | fabricate a specific, measurable, time-bounded observable signal that would disconfirm the hypothesis; `[AI-SUGGESTED: blocking]` (riskiness of a non-falsifiable hypothesis is high). |
| B3 | Every §11 R-NN row's `Mitigation` cell is non-empty | fabricate a plausible mitigation drawn from the risk's category (commercial → contract terms; regulatory → legal review; adoption → change management; operational → runbook; technical-debt → tracking & schedule); `[AI-SUGGESTED: non-blocking]`. |
| B4 | Every §7.1 primary persona appears in at least one §9.1 phase's `Audience served` column | add the persona to the most plausible phase (typically MVP for the most acute pain-carrier); `[AI-SUGGESTED: blocking]`. |
| B5 | Every §4 stakeholder row's `Sign-off domain` cell is non-empty and not "no sign-off needed" | fabricate a sign-off domain inferred from the stakeholder's role (e.g. CFO → budget gate; CISO → security review; PM lead → MVP scope); `[AI-SUGGESTED: blocking]`. |
| B6 | Every §9.1 phase has at least one §13 RC-NN release criterion citing it | fabricate a release criterion derived from the phase's `Definition of done` cell, rephrased as an observable gate; `[AI-SUGGESTED: non-blocking]`. |
| B7 | Every §9.1 phase has at least one §14 milestone citing it | fabricate a typical milestone (e.g. "MVP design freeze", "MVP engineering complete", "MVP internal beta", "MVP general availability"); `[AI-SUGGESTED: non-blocking]`. |
| B8 | Every §8.2 C-NN row cites at least one §5 metric / §6 hypothesis / §7 job in its `Why this matters` cell | resolve the cross-reference; if none exist yet, the capability is scope bloat and should be dropped — emit a warn flag for the drafter to consider removal rather than auto-fabricating an upstream tie. |
| B9 | §3 has at least one row, and at least one row is a real competitor or named alternative | if §3 is empty, fabricate at least one named alternative from domain heuristics (typical candidates: incumbent in-house tool, the dominant off-the-shelf vendor in the domain, "do nothing"); `[AI-SUGGESTED: blocking]`. |
| B10 | §10 has at least one row | if §10 is empty, fabricate at least one plausible scope-creep candidate from domain heuristics (typical candidates per CRUD-app domain: "real-time collaboration", "mobile native app", "deep analytics dashboard", "third-party integration X"); `[AI-SUGGESTED: blocking]`. |

## Tier B — soft / warn (no fabrication)

| # | Rule | Action |
|---|---|---|
| SB1 | §9.1 has a row labelled "MVP" (or domain-equivalent first phase) | warn only; some PRDs use different phase naming conventions. |
| SB2 | §5.3 has at least one explicit non-goal | warn only; small products may have none. |
| SB3 | No §6.2 assumption row's text duplicates a §6.1 hypothesis row's text | warn only; if duplication is found, prefer keeping the hypothesis (testable) and dropping the assumption (taken as given). |

## Blocking vs non-blocking classification (drafter rubric, applied here)

The PRD-drafter's classification rubric (`framework/agents/prd-drafter.md > Classification`) applies to every `[AI-SUGGESTED]` marker emitted by this skill:

- **Blocking** = wrong guess invalidates a load-bearing PRD claim (problem framing, primary success metric, MVP definition, top-tier risk, sign-off authority).
- **Non-blocking** = wrong guess is a refinement detail (one risk among many, secondary metric, timeline grain, secondary stakeholder).

In the table above, the recommended classification per rule is the default; the drafter may upgrade non-blocking → blocking when domain context warrants. Tie-breaker: when in doubt, classify as **blocking** — false positives cost a question, false negatives cost a guess shipping unchallenged.

## Algorithm (deterministic; the skill performs no LLM call itself)

1. Walk the populated draft section-by-section.
2. For each rule in Tier A (B1–B10), evaluate the predicate against the draft state.
3. For each violation, produce a `(rule_id, location, action, marker_kind, marker_payload, draft_context)` tuple with `marker_kind = "AI-SUGGESTED"`, the recommended classification from the table above, and a one-line `draft_context` derived from the rule + location + (when useful) the candidate value set.
4. For each Tier B rule (SB1–SB3), evaluate the predicate; on failure, emit a warn-only log entry. No tuple is produced.
5. Emit the tuple list to the drafter, plus the running `PAI-NNN` counter.
6. The drafter applies the tuples to the draft (via Edit) before writing the final file. The drafter also carries each tuple's `draft_context` into the resolver's manifest at the resolver's first-turn build step (per `framework/agents/prd-resolver.md > Working state`); the field is observability for the resolver and never written into the draft body itself.

## Used by

- `framework/agents/prd-drafter.md` — workflow step 4 (post-fill, pre-write).

## Anti-Patterns

- Do not call an LLM inside this skill. The decision tree is deterministic; inference (when needed) is performed by the drafter consuming the tuple list.
- Do not consult `framework/shared/general-rules.md` — the `GR-NN` rules govern UI behaviour and do not apply to PRD content. (`GR-20` is enforced as a single post-Write Grep guard against §8 only, by the drafter — see `framework/agents/prd-drafter.md > Self-validation`. It is not a decision-tree input here.)
- Do not consult `framework/shared/prototype-scope.md` — the PRD has no prototype-scope concern; every PRD section is in-scope by definition.
- Do not emit `[STANDARD-RULE: GR-NN]` markers from this skill. The PRD pipeline does not use them.
- Do not emit `[OUT-OF-SCOPE: domain-default]` markers from this skill. The PRD pipeline does not use them; §10 is the section that discusses out-of-scope content, and it is filled like every other section (via `[SRC:]` or `[AI-SUGGESTED]`).
- Do not emit `[REQ: §X.Y]` cross-doc pointers. The PRD pipeline is fully independent of `requirements/requirements.md`.
- Do not emit warn-only flags as tuples — Tier B (SB1–SB3) emits log entries that the drafter surfaces alongside the gap-pass output but does not apply as draft Edits.
- Do not fabricate a §8.2 capability that has no upstream tie (B8). If a capability appears in the draft with no plausible §5 metric / §6 hypothesis / §7 job to cite, surface a warn flag and let the drafter consider removing the row — scope bloat is a more serious problem than a missing AI-SUGGESTED resolution.
