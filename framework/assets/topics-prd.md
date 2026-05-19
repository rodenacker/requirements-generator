<!-- ROLE: asset. Canonical topic list mirroring `framework/assets/template-prd.md` one-to-one. -->

# topics-prd.md

**Purpose:** Canonical list of the topics every PRD must cover, with per-topic acceptance criteria and minimum-useful-content rules. Every section is unconditional (always emit). The PRD audience is human (consultant, client stakeholders, sign-off authorities) — distinct from `requirements/requirements.md` which is LLM-audience.

**Used by:**
- `framework/assets/template-prd.md` — section skeleton mirrors this list one-to-one.
- `framework/agents/prd-drafter.md` — drives extraction + categorisation + citation scope.
- `framework/skills/completeness-gap-pass-prd.md` — per-topic completeness checks (Tier A / Tier B rules).

**How used:** Loaded by drafter + gap-pass skill. Authoring a new topic requires updating this file, the template, and the gap-pass rules together.

## Section list (mirrors template 1:1)

| § | Topic | Emit predicate |
| --- | --- | --- |
| 1 | Document metadata & reading list | always |
| 2 | Problem & opportunity | always |
| 3 | Competitive context | always |
| 4 | Stakeholders & sign-off authority | always |
| 5 | Business goals & success metrics | always |
| 6 | Hypotheses & assumptions | always |
| 7 | Users & jobs-to-be-done | always |
| 8 | Solution overview & key capabilities | always |
| 9 | Scope, MVP definition & phasing | always |
| 10 | Out of scope & rationale | always |
| 11 | Risks & mitigations | always |
| 12 | Cross-functional dependencies | always |
| 13 | Release criteria | always |
| 14 | Timeline & milestones | always |

The PRD has no conditional sections. Every gap becomes either a `[SRC: PC-NNN]` citation (input-grounded) or an `[AI-SUGGESTED: PAI-NNN]` marker that the resolver Q&A turns into a final value. There is no "Open questions" section — unresolved items are unacceptable on the merged document.

## Pre-authoring invariants (preserve when filling in)

- §1 metadata includes a **reading list** of companion artefacts (`requirements/requirements.md`, `design-system/design-system.html`, analyses, reviews) when they exist. Pointers are by filename only — never restate content from those files inside the PRD.
- §2 problem statement leads with user/stakeholder pain in plain language, then sizes the opportunity. §2.3 opportunity-size dimensions (affected users, frequency, cost of inaction, trend) are all required cells.
- §3 competitive context names competitors, alternatives, and "do nothing" — never abstract phrasing like "the market alternative." This is the section most likely to need vendor names and is exempt from `GR-20`.
- §4 stakeholders includes a sign-off domain for every row. "No sign-off needed" is not a valid sign-off domain; if a person doesn't sign off on anything, they belong in §12 dependencies, not §4 stakeholders.
- §5 splits goals (business outcomes, BG-NN) from metrics (M-NN). Every metric carries baseline + target + cadence + owner; metrics without baselines are unmeasurable and fail completeness.
- §5.3 non-goals is required — explicit declarations of what this product is **not** trying to do.
- §6.1 hypotheses are typed rows (H-NN). Each row carries a falsification condition. A hypothesis without a falsification condition is a wish; the gap-pass treats it as a hard fail.
- §6.2 assumptions are typed rows (A-NN), distinct from hypotheses. Assumptions are taken as given; hypotheses are testable.
- §7.1 primary personas: ≤4. More than four primary personas is a scoping problem.
- §7.3 jobs-to-be-done use the canonical JTBD template ("When {situation}, I want to {motivation}, so I can {expected_outcome}") and tie each job to a persona from §7.1.
- §8.2 capability rows are capability-level only — **`GR-20` applies here**. Vendor names, framework names, product names are a hard fail in §8 cells. (§3 competitive context, §11 risks, §12 dependencies are exempt — they legitimately need vendor names.)
- §8.2 every capability cites at least one upstream tie-in (§5 metric / §6 hypothesis / §7 job). Orphan capabilities are scope bloat.
- §9 phasing has at minimum an MVP phase. Every phase has a definition of done that is observable (not "we feel good about it").
- §10 out-of-scope is required and unconditional. If the drafter cannot find any explicit out-of-scope content in the inputs, it fabricates at least one common scope-creep candidate per domain heuristics and marks it `[AI-SUGGESTED]` — the resolver Q&A makes the consultant explicitly confirm or correct it. Empty §10 is treated as a completeness failure.
- §11 risks are categorised as commercial / regulatory / adoption / operational / technical-debt. Pure technical build risks ("the DB might be slow") belong in the requirements doc, not here.
- §11 every risk has a mitigation. Risks without mitigations are complaints.
- §12 internal team dependencies and external vendor dependencies are separate sub-blocks. Vendor names are required for §12.2 rows.
- §13 release criteria are concrete and observable. "Quality is good" fails the template. Every criterion ties to a §9 phase.
- §14 timeline is a snapshot, not a contract — drift is expected. Every milestone ties to a §9 phase.

## Completeness checks (aligned with Tier A / Tier B in `framework/skills/completeness-gap-pass-prd.md`)

- **Tier A (hard bijection — gap → fabricate + `[AI-SUGGESTED]`):**
  - **B1** `metric_ties_to_problem_or_hypothesis == true` — every §5.2 M-NN cites at least one §2 problem or §6 hypothesis. Orphan metrics are a gap-pass failure.
  - **B2** `hypothesis_has_falsification_condition == true` — every §6.1 H-NN row's `Falsification condition` cell is non-empty and observable.
  - **B3** `risk_has_mitigation == true` — every §11 R-NN row's `Mitigation` cell is non-empty.
  - **B4** `persona_served_by_phase == true` — every §7.1 primary persona appears in at least one §9.1 phase's `Audience served` column.
  - **B5** `stakeholder_has_signoff_domain == true` — every §4 stakeholder row's `Sign-off domain` cell is non-empty and not "no sign-off needed."
  - **B6** `phase_has_release_criterion == true` — every §9.1 phase has at least one §13 RC-NN release criterion citing it.
  - **B7** `phase_has_milestone == true` — every §9.1 phase has at least one §14 milestone citing it.
  - **B8** `capability_has_upstream_tie == true` — every §8.2 C-NN row cites at least one §5 metric / §6 hypothesis / §7 job in its `Why this matters` cell.
  - **B9** `competitive_landscape_named == true` — §3 has at least one row, and at least one row is a real competitor or named alternative (not "the market").
  - **B10** `out_of_scope_nonempty == true` — §10 has at least one row. If inputs are silent, drafter fabricates a plausible domain-heuristic row and marks `[AI-SUGGESTED]`.

- **Tier B (soft / warn):**
  - **SB1** `mvp_phase_present == true` — §9.1 has a row labelled "MVP" (or domain-equivalent first phase). Warn-only — some PRDs use different phase naming conventions.
  - **SB2** `non_goals_present == true` — §5.3 has at least one explicit non-goal. Warn-only — small products may have none.
  - **SB3** `assumption_distinct_from_hypothesis == true` — no §6.2 assumption row's text duplicates a §6.1 hypothesis row's text. Warn-only.

The PRD pipeline has no Tier C (out-of-scope sections) and no Tier D (visual-manifestation gating). Those tiers exist in `topics-requirements.md` because the requirements doc gates on UI manifestation and prototype scope; the PRD has neither concern — it's a strategic-framing document for humans, and every section is in-scope by definition.

## Marker semantics

The PRD pipeline emits exactly two markers:

- `[SRC: PC-NNN]` — input-cited fact. PRD-namespaced (`PC-` for **P**RD **C**laim) to avoid visual collision with requirements `C-NNN` IDs. Sidecar at `prd/draft-claims.ndjson`. Retained verbatim in the final merged `prd/prd.md`.
- `[AI-SUGGESTED: PAI-NNN | blocking|non-blocking]` — inferred fill. PRD-namespaced (`PAI-` for **P**RD **AI**-suggested). Resolver Q&As; merger strips after applying resolution.

**Not emitted:**
- `[STANDARD-RULE: GR-NN]` — the `GR-NN` rules in `framework/shared/general-rules.md` are UI behaviour guardrails (validation timing, badge mapping, table sorting). None apply to PRD content.
- `[OUT-OF-SCOPE: domain-default]` — the PRD's §10 *is* the out-of-scope discussion. A marker inside §10 saying "out of scope" would be self-referential nonsense, and §10 is not the only place out-of-scope content appears — it's just the discussion of it.
- `[REQ: §X.Y]` — the PRD pipeline is fully independent of `requirements/requirements.md`. It reads only `requirements/source-manifest.json` and the input files under `input/`. Cross-doc pointers into `requirements.md` would widen the closed marker set forbidden by CLAUDE.md §1.

## Citation scope

`[SRC: PC-NNN]` tags are required on every **unmarked, template-defined field value** in the following scope. Free-prose narrative paragraphs are excluded.

- §1 every metadata field value, every reading-list entry.
- §2.1 problem-statement (when input-grounded — typical), §2.2 current-state, §2.3 every cell.
- §3 every cell (competitor name, strengths, weaknesses, why-not), the differentiation-thesis one-liner.
- §4 every stakeholder row's name (when known), sign-off domain, cadence; RACI summary.
- §5.1 every BG-NN goal-statement; §5.2 every M-NN row's metric, baseline, target, cadence, owner; §5.3 every non-goal.
- §6.1 every H-NN row's hypothesis, falsification condition, riskiness, test-owner; §6.2 every A-NN row's assumption, source, validation plan.
- §7.1 every persona's role, day-summary, goals, frustrations, current-tools, authority-scope; §7.2 every secondary persona; §7.3 every job statement, hired-by, outcome, current-alternative.
- §8.1 solution one-liner; §8.2 every C-NN row's capability, why-this-matters, phase; §8.3 interaction-surfaces narrative when input-grounded.
- §9.1 every phase row's capability list, audience, definition of done, target date; §9.2 MVP rationale.
- §10 every row's item, rationale, disposition.
- §11 every R-NN row's risk, category, likelihood, impact, mitigation, owner, escalation trigger.
- §12.1 every team-dependency row; §12.2 every vendor-dependency row.
- §13 every RC-NN row's criterion, phase, verification method, owner.
- §14 every milestone row; critical-path summary.

Marked fields (`[AI-SUGGESTED]`) carry no `[SRC:]` tag — the marker and the tag are mutually exclusive on a per-field basis. No field carries both.

## What's intentionally absent

- **No `[STANDARD-RULE]` path** — the PRD pipeline does not consult `framework/shared/general-rules.md` at draft time. (`GR-20` is enforced as a single post-Write Grep guard against §8 only — see `framework/agents/prd-drafter.md > Self-validation`. It is not consulted as a decision-tree input.)
- **No `[OUT-OF-SCOPE]` path** — §10 is the out-of-scope section. The gap-pass never emits an OOS marker.
- **No `[REQ:]` cross-doc pointer** — PRD pipeline is fully independent of `requirements.md`.
- **No conditional sections** — every §1–§14 always emits.
- **No "Open questions" residual section** — every gap is resolved via `[AI-SUGGESTED]` Q&A before merge.
- **No mermaid diagrams** — PRDs are prose + tables; the drafter skips the mermaid-validator step entirely.
- **No `## Prototype invariants` append** — PI-NN are prototype-build invariants for the FE spec, not PRD content. The merger explicitly does not append them.
