<!-- ROLE: asset. Section order matches `framework/assets/topics-prd.md` one-to-one. Audience is human (consultant, client stakeholders, sign-off authorities). -->

# Product Requirements Document: {{product_name}}

**Domain:** {{domain}} <!-- inferred from inputs; flag [AI-SUGGESTED] if not stated explicitly --> **Status:** draft | final **Created:** {{date}} **Last finalised at:** {{last_finalised_at}}

> **Authoring guardrails.** Cells across §1–§14 must obey:
> - **`GR-20` (selective).** No framework, library, vendor, product, version, or brand name in **§8 Solution overview** cells — that section is the most likely to be consumed by downstream LLM analysers, so it stays capability-level. All other sections (§3 Competitive context, §11 Risks, §12 Dependencies in particular) **may** name specific vendors, competitors, regulators, and tools — those are load-bearing for human stakeholder decisions.
> - **No `GR-21` enforcement.** The PRD is human-audience; layout-vocab phrasing is acceptable in any section where it aids understanding (e.g., "the dashboard surfaces three KPI cards").
>
> Inferred content is marked inline with one of two markers per the drafter's decision tree (`framework/agents/prd-drafter.md > Classification`):
> - `[SRC: PC-NNN]` — input-cited fact (PRD-namespaced; sidecar at `prd/draft-claims.ndjson`).
> - `[AI-SUGGESTED: PAI-NNN | blocking|non-blocking]` — inferred fill; resolver Q&A's it; merger strips it.
>
> No `[STANDARD-RULE]`, `[OUT-OF-SCOPE]`, or `[REQ:]` markers are emitted by the PRD pipeline — see `framework/agents/prd-drafter.md > Classification` for the rationale.
>
> Field-level marking when only some sub-fields are inferred; heading-level marking when the whole item is invented. **Fill every field — no blanks, no "TBD" values, no residual "Open questions" section.** Every gap becomes either a `[SRC: PC-NNN]` citation or an `[AI-SUGGESTED: PAI-NNN]` marker that the resolver Q&A turns into a final value.

---

## 1. Document metadata

| Field | Value |
| --- | --- |
| Product name | {{product_name}} |
| Owner / author | {{owner}} <!-- typically the consultant / PM authoring this PRD --> |
| Audience | {{audience}} <!-- typically: client decision-makers, internal stakeholders, sign-off authorities --> |
| Document version | {{version}} <!-- semver or date-based; e.g. 1.0, 2026-05-19 --> |
| Build target reference | {{build_target}} <!-- "prototype" or "application" if a sibling requirements.md exists; else "to-be-determined" --> |
| Reading time | {{reading_time}} <!-- estimate, e.g. "15 minutes" --> |

**Reading list (companion artefacts):**

- {{companion_doc_1}} <!-- e.g. "requirements/requirements.md — the FE spec derived from this PRD" -->
- {{companion_doc_2}} <!-- e.g. "design-system/design-system.html — the design tokens" -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 2. Problem & opportunity

> The "why we're building this." Lead with the user/stakeholder pain in plain language, then size the opportunity. This section justifies the rest of the PRD — if §2 is weak, every downstream commitment is weak.

### 2.1 Problem statement

{{problem_statement}} <!-- 1-3 paragraphs. Plain language. Cite consultant interview quotes, market data, or stakeholder claims where possible. -->

### 2.2 Current state

{{current_state}} <!-- How users solve this problem today — workarounds, manual processes, competing tools. One paragraph. -->

### 2.3 Opportunity size

| Dimension | Value |
| --- | --- |
| Affected users | {{affected_user_count}} <!-- order of magnitude is fine: "~500 underwriters across 12 branches" --> |
| Frequency of pain | {{pain_frequency}} <!-- "daily", "every loan application", "monthly close" --> |
| Cost of inaction | {{cost_of_inaction}} <!-- time wasted, errors made, deals lost, compliance risk --> |
| Trend | {{trend}} <!-- "growing", "stable", "regulatory deadline pressure" --> |

<!-- rev: run-N YYYY-MM-DD -->

---

## 3. Competitive context

> What's already out there. Name names — vendors, products, internal predecessors, off-the-shelf alternatives. Without this, stakeholders can't tell if the build-vs-buy call has been considered.

| Competitor / alternative | What it does well | What it does poorly | Why we're not adopting it |
| --- | --- | --- | --- |
| {{competitor_name}} | {{strengths}} | {{weaknesses}} | {{why_not}} |

<!-- repeat per alternative; include "do nothing" and "buy off-the-shelf X" as named rows when applicable -->

**Differentiation thesis:** {{differentiation_one_liner}} <!-- One sentence: what we are uniquely positioned to do that the alternatives cannot. -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 4. Stakeholders & sign-off authority

> Who needs to agree for this to ship. Map roles, not just names — a stakeholder map without role context rots when people change jobs.

| Role | Name (if known) | Sign-off domain | Cadence |
| --- | --- | --- | --- |
| {{stakeholder_role}} | {{stakeholder_name}} | {{signoff_domain}} <!-- e.g. "compliance language in §6.6.4", "MVP scope", "release date" --> | {{cadence}} <!-- "weekly review", "release gate only", "ad-hoc" --> |

<!-- every row must have a sign-off domain; "no sign-off needed" is not a valid value — that stakeholder belongs in §12 dependencies, not here -->

**RACI summary:** {{raci_summary}} <!-- 2-3 sentences naming who is Responsible, Accountable, Consulted, Informed across the build phases. -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 5. Business goals & success metrics

> Goals are outcomes the business wants; metrics are how we'll know if we got them. **Every metric must tie to a §2 problem or a §6 hypothesis** — orphan metrics are a planning smell.

### 5.1 Business goals

| ID | Goal | Tied to (§2 problem / §6 hypothesis) |
| --- | --- | --- |
| BG-{{nn}} | {{business_goal}} <!-- outcome-level, not feature-level. "Reduce underwriting cycle time by 30%" not "Add a dashboard." --> | → §2.1 / → §6 H-NN |

### 5.2 Success metrics

| ID | Metric | Tied to (BG-NN) | Type | Baseline | Target | Measurement cadence | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M-{{nn}} | {{metric}} <!-- e.g. "Median time from application receipt to underwriter decision" --> | → §5.1 BG-NN | leading / lagging | {{baseline_value}} | {{target_value}} | daily / weekly / monthly / per-release | {{owner_role}} |

<!-- every metric MUST have both baseline and target; every metric MUST cite a BG-NN; metric type (leading/lagging) drives when to expect movement -->

### 5.3 Non-goals

- {{non_goal}} <!-- explicit things this product is NOT trying to achieve, even if related. E.g. "Replace the core LOS system" — distinguishes scope from ambition. -->

<!-- repeat per non-goal -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 6. Hypotheses & assumptions

> What we're betting on. Hypotheses are testable; assumptions are taken as given. **Every hypothesis must declare a falsification condition** — if you can't say what would prove it wrong, it's not a hypothesis, it's a wish.

### 6.1 Hypotheses (with falsification conditions)

| ID | Hypothesis | Falsification condition | Riskiness | Test owner |
| --- | --- | --- | --- | --- |
| H-{{nn}} | We believe {{population}} will {{behaviour}} because {{reason}} | We will know we are wrong if {{observable_signal}} <!-- specific, measurable, time-bounded --> | high / medium / low | {{role}} |

<!-- "riskiness = high" means: if wrong, MVP scope changes materially. Order rows by riskiness descending. -->

### 6.2 Assumptions (taken as given for this PRD)

| ID | Assumption | Source | Validation plan (if any) |
| --- | --- | --- | --- |
| A-{{nn}} | {{assumption}} | stated / inferred / industry-standard | {{validation_plan_or_"accepted-as-given"}} |

<!-- repeat per assumption -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 7. Users & jobs-to-be-done

> Who is this for, and what job are they hiring this product to do. Personas here are the same humans referenced in §3 of the sibling `requirements.md` when one exists; the framing here is JTBD (motivation, context, success), not behavioural stories.

### 7.1 Primary personas

#### {{persona_name}}

| Field | Value |
| --- | --- |
| Role / title | {{role}} |
| Day-in-the-life summary | {{day_summary}} <!-- 2-3 sentences. What does this person actually do all day? --> |
| Goals they pursue | {{personal_goals}} |
| Frustrations they carry | {{frustrations}} |
| Tools they use today | {{current_tools}} |
| Decision-making authority | {{authority_scope}} |

<!-- repeat per primary persona; ≤4 primary personas (more than that is a scoping problem, not a persona inventory) -->

### 7.2 Secondary personas (mentioned but not primary targets)

- {{secondary_persona}} — {{why_secondary}}

<!-- repeat per secondary -->

### 7.3 Jobs-to-be-done

| ID | Job statement | Hired by (persona → §7.1) | Outcome the user wants | Current alternative |
| --- | --- | --- | --- | --- |
| J-{{nn}} | When {{situation}}, I want to {{motivation}}, so I can {{expected_outcome}} | → §7.1 {{persona}} | {{outcome}} | {{how_they_do_it_today}} |

<!-- repeat per job; JTBD is functional/emotional/social — note which dimension dominates if helpful -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 8. Solution overview & key capabilities

> What we're building, at the capability level. **`GR-20` applies here** — speak in capability categories, not stack picks. Downstream `/analyse-requirement` analysers may consume this section, so vendor noise hurts.

### 8.1 Solution one-liner

{{solution_one_liner}} <!-- One sentence a stakeholder can repeat back. "A web app that lets underwriters approve loans 30% faster by surfacing the relevant policy checks inline." -->

### 8.2 Key capabilities (capability-level only)

| ID | Capability | Why this matters (→ §5 metric / §6 hypothesis / §7 job) | Phase (→ §9) |
| --- | --- | --- | --- |
| C-{{nn}} | {{capability_category}} <!-- e.g. "policy-check surfacing", "document upload & classification", "approval workflow with audit trail" --> | → §5 M-NN / → §6 H-NN / → §7 J-NN | mvp / phase-2 / phase-3 |

<!-- repeat per capability; every row MUST cite at least one upstream tie-in; orphan capabilities are scope bloat -->

### 8.3 Key interaction surfaces (capability-level)

{{interaction_surfaces_narrative}} <!-- 1-2 paragraphs describing the major surfaces users interact with — in capability terms, not screen layouts. "Underwriters see a worklist of pending applications, drill into each to a structured decision view, and complete approvals from the decision view itself." Layout decisions are downstream. -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 9. Scope, MVP definition & phasing

> What ships when. The MVP definition here is load-bearing — every §11 risk and §13 release criterion ties back to a phase declared here.

### 9.1 Phasing

| Phase | Capabilities (→ §8.2 C-NN) | Audience served (→ §7.1) | Definition of done | Target date |
| --- | --- | --- | --- | --- |
| MVP | {{mvp_capability_list}} | {{mvp_audience}} | {{mvp_dod}} <!-- crisp, observable. "Underwriter X can complete an end-to-end approval in the staging environment." --> | {{mvp_date}} |
| Phase 2 | {{phase2_capability_list}} | {{phase2_audience}} | {{phase2_dod}} | {{phase2_date}} |
| Phase 3+ | {{phase3_capability_list}} | {{phase3_audience}} | {{phase3_dod}} | {{phase3_date}} |

<!-- every persona in §7.1 MUST appear in at least one phase's audience column (B4 bijection) -->

### 9.2 MVP scope rationale

{{mvp_rationale}} <!-- 1-2 paragraphs. Why this slice and not a different one? What signal does the MVP buy us? What's deferred and why? -->

### 9.3 Capability-to-phase matrix

| Capability (→ §8.2) | MVP | Phase 2 | Phase 3+ |
| --- | --- | --- | --- |
| C-{{nn}} | ✓ / — | ✓ / — | ✓ / — |

<!-- one row per §8.2 capability; ✓ means included in that phase, — means not in that phase -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 10. Out of scope & rationale

> What we are explicitly NOT building, and why. This is the single most-skipped section in real-world PRDs and the source of most scope creep — fill it with care.

| Item | Why out of scope | Where it might live (if anywhere) |
| --- | --- | --- |
| {{out_of_scope_item}} | {{rationale}} <!-- e.g. "Already handled by the LOS", "Cost > value for MVP", "Regulatory uncertainty", "Belongs to backend team" --> | {{disposition}} <!-- e.g. "Backend roadmap Q3", "Existing tool Y", "Not planned" --> |

<!-- repeat per out-of-scope item; this section is unconditional (Rules: B-bijection of §1.5 IN/§9 phases) - if no items, fabricate at least one common scope-creep candidate per domain heuristics and mark [AI-SUGGESTED] -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 11. Risks & mitigations

> Every risk needs a mitigation. A risk without a mitigation is just a complaint.

| ID | Risk | Category | Likelihood | Impact | Mitigation | Owner | Trigger to escalate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-{{nn}} | {{risk_statement}} | commercial / regulatory / adoption / operational / technical-debt | high / medium / low | high / medium / low | {{mitigation}} | {{role}} | {{escalation_trigger}} <!-- specific event or threshold --> |

<!-- repeat per risk; every risk MUST have a mitigation cell populated; technical-build risks (e.g. "the database might be slow") belong in the requirements doc, not here — this section is about commercial, regulatory, adoption, and operational risk -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 12. Cross-functional dependencies

> Other teams and external vendors whose work must complete (or proceed in parallel) for this build to ship. Naming names is fine in this section.

### 12.1 Internal team dependencies

| Team | What we need from them | By when | Status | Contact |
| --- | --- | --- | --- | --- |
| {{team_name}} | {{deliverable}} | {{date_or_phase}} | not-started / in-progress / blocked / done | {{contact}} |

<!-- repeat per internal dependency; common rows: design ops (design tokens), legal (compliance review), data (analytics events), security (auth review), CX (training materials) -->

### 12.2 External / vendor dependencies

| Vendor / external party | What they provide | Contract status | Risk if unavailable | Backup plan |
| --- | --- | --- | --- | --- |
| {{vendor_name}} | {{provision}} | signed / pending / negotiating / n/a | {{risk}} | {{backup_or_"none"}} |

<!-- repeat per external dependency -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 13. Release criteria

> Concrete go/no-go gates per phase. **Every criterion ties to a §9 phase.** Vague criteria ("quality is good") fail this template — be observable.

| ID | Criterion | Phase (→ §9.1) | How verified | Owner |
| --- | --- | --- | --- | --- |
| RC-{{nn}} | {{release_criterion}} <!-- e.g. "P95 page load < 2s in staging", "All §5 M-NN metrics instrumented and reporting", "Compliance sign-off recorded against §4 stakeholder X" --> | mvp / phase-2 / phase-3 | {{verification_method}} <!-- e.g. "manual test plan A-12", "automated suite", "stakeholder sign-off email" --> | {{role}} |

<!-- repeat per criterion; every §9 phase MUST have ≥1 release criterion (B6 bijection) -->

<!-- rev: run-N YYYY-MM-DD -->

---

## 14. Timeline & milestones

> The when. Each milestone references a §9 phase. Timeline drift expected — this section is a snapshot, not a contract.

| Milestone | Phase (→ §9.1) | Target date | Confidence | Dependencies (→ §12) |
| --- | --- | --- | --- | --- |
| {{milestone_name}} | mvp / phase-2 / phase-3 | {{date}} | high / medium / low | {{dependency_refs}} |

<!-- repeat per milestone; every §9 phase MUST have ≥1 milestone (B7 bijection); typical milestones per phase: "design freeze", "engineering complete", "internal beta", "limited rollout", "general availability" -->

**Critical path summary:** {{critical_path}} <!-- 2-3 sentences naming the milestones whose slip would slip the MVP date. -->

<!-- rev: run-N YYYY-MM-DD -->

---
