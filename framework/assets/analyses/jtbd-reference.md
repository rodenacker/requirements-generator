<!-- ROLE: asset (P2 analysis reference). Loaded by framework/agents/analyses/jtbd-analyser.md at activation. -->

# analyses/jtbd-reference.md

**Purpose:** Methodology reference for Jobs-to-be-Done analysis. Hybrid Christensen-Moesta + Ulwick: Christensen-Moesta supplies the canonical statement form (*"When `<situation>`, I want to `<motivation>`, so I can `<outcome>`."*) and the forces of progress (push / pull / anxiety / habit); Ulwick supplies the importance × satisfaction = opportunity scoring. The analyser follows this document literally and exhaustively.

**Used by:**

- `framework/agents/analyses/jtbd-analyser.md` — drives the agent's six-round process plus the quality-gate sweep.
- `framework/skills/map-jtbd-to-ui.md` — uses the job-map structure to derive primary-task weighting + per-screen Core Content Priority signals (downstream consumer; stub).

**Output produced by the analyser:** `analyse-requirements/JTBD/jtbd-job-map.html` — self-contained HTML job-card grid using `framework/assets/analyses/template-jtbd.html` as scaffold.

---

## Upstream input contract

JTBD is a **UX-lens refinement** of the BA's persona + task-flow material, never a parallel inventory of features. The analyser anchors on:

- `§Personas` — canonical source of **actors**. Each actor named in `§Personas` is a candidate primary-actor for jobs.
- `§Task flows` and `§User stories` — canonical source of **situations**. Each step / story that names a trigger condition is a candidate situation.
- `§1 Domain` and `§Pains` — supplementary source of situations where `§Task flows` / `§User stories` is sparse.
- `§Acceptance criteria`, `§Constraints`, `§Success metrics` — canonical source of **measurable outcomes**.
- `§Existing solutions`, `§Current process` — canonical source of **current-state satisfaction baseline** (informs Round 5 scoring).

If `§Personas` is absent or empty, the analyser falls back to extracting candidate actor names from `§Task flows`, `§User stories`, or running prose — flagging each fallback actor with the `derived-actor` provenance marker. The same fallback discipline applies to situations (`from-prose` marker when neither `§Task flows` nor `§User stories` named the situation).

---

## The JTBD-X process

Six rounds, executed in order. The analyser does not skip rounds and does not collapse rounds into a single pass — each round's output feeds the next, and round-by-round structure is what makes the methodology auditable.

### Round 1 — Situations & Actors

Read `requirements/requirements.md` in full. Extract every actor + every situation candidate.

**Actor sources, in priority order:**

1. `§Personas` — canonical.
2. `§Task flows` / `§User stories` — names referenced as the "user" / "actor" in story prefaces.
3. `§1 Domain` / running prose — last resort; mark `derived-actor`.

**Situation sources, in priority order:**

1. `§Task flows` — each step's preconditions / triggers.
2. `§User stories` — the *"As a … when … I want …"* preface clause.
3. `§1 Domain`, `§Pains`, running prose — supplementary.

**Output of Round 1:** an unfiltered candidate `{actor, situation, actor_source, situation_source}` list. Synonyms and near-duplicates are kept at this stage; deduplication happens in Round 2.

### Round 2 — Job Extraction

For each `(actor, situation)` pair from Round 1, write the canonical job statement:

> *"When `<situation>`, I want to `<motivation>`, so I can `<outcome>`."*

**Filter rules:**

- Merge near-duplicate jobs (same actor, near-identical situation + motivation). Prefer the more specific wording.
- Reject motivations that name **UI affordances**. Forbidden tokens in the motivation clause: `click`, `tap`, `navigate to`, `open the … dialog`, `select … from the dropdown`, `see … on the dashboard`, `view the … page`, `enter … in the field`. These are design-phase concerns, not jobs. Rewrite to the underlying intent (*"I want to click the export button"* → *"I want to retrieve the report's content in a portable format"*).
- Reject motivations that name a specific **product feature** by name (e.g., *"I want to use the new bulk-edit feature"*). Rewrite to the job the feature serves.
- Retain motivations the consultant's actor would name as a desired job outcome, even if the requirements doc phrases it as a feature.

**Output of Round 2:** the final job list. Each row carries `{job_id, actor, situation, motivation, outcome, actor_source, situation_source}`. Job IDs are `J-NN` zero-padded in discovery order.

### Round 3 — Job Typology

Classify each job from Round 2 as one of:

- **Functional** — the main, task-completion job. *"I want to restore inventory levels."*
- **Emotional** — how the actor wants to feel during or after the job. *"I want to feel confident the order will arrive in time."*
- **Social** — how the actor wants to be perceived by others. *"I want to be seen as the buyer who never lets us run out."*

**Rules:**

- A single `(actor, situation)` may yield jobs of multiple types — emit them as **separate rows**, each with its own `job_id`. A Functional job is not a parent of its Emotional or Social siblings; they coexist.
- Where the requirements doc has no Emotional or Social signal for a given Functional job, **do not invent** Emotional / Social rows. The cluster is `functional-only`. Surface the count in the diagnostics block.
- Functional is the typology default. If a job's typology is ambiguous, classify as Functional and flag for consultant review.

**Output of Round 3:** the job list with `type ∈ {functional, emotional, social}` populated on every row.

### Round 4 — Outcome Refinement

For every job, the outcome clause must be **measurable**. A measurable outcome carries a unit of measure: time (*"in under 5 minutes"*), count (*"without re-entering data"*), threshold (*"with one confirmation step"*), absence (*"without missing the delivery deadline"*), or comparative (*"faster than the legacy email approval"*).

**Sources for measures, in priority order:**

1. `§Acceptance criteria` — the strongest source; explicit pass/fail conditions.
2. `§Constraints` — required / format / range conditions that imply a measure.
3. `§Success metrics` — explicit KPIs the consultant has set.
4. `§Pains` — implicit measures derived from the pain phrasing (*"approval takes 2 days"* → *"in under 1 day"*).

If no measure can be anchored from any source, **do not fabricate one**. Replace the outcome clause with the explicit marker `(no-metric-in-requirements)` appended to a best-effort intent phrase, and surface the count in the diagnostics block. Example: *"so I can avoid stockout `(no-metric-in-requirements)`"*.

**Output of Round 4:** the job list with every `outcome` clause either measurable or carrying the `no-metric-in-requirements` marker.

### Round 5 — Importance & Satisfaction Scoring

For every job, assign:

- **Importance** — 1 to 5, on Ulwick's scale (1 = inconsequential, 3 = matters, 5 = critical to the actor's success).
- **Satisfaction** — 1 to 5, current-state with the actor's existing tools / process (1 = totally unsatisfied, 5 = fully satisfied).

**Sources for importance, in priority order:**

1. `§Pains` — high-pain situations imply Importance ≥ 4.
2. `§Goals` / `§Outcomes` — primary business goals imply Importance ≥ 4 for the jobs that achieve them.
3. `§Personas` — *"key responsibilities"* / *"daily tasks"* prose implies Importance ≥ 3.

**Sources for satisfaction, in priority order:**

1. `§Existing solutions` / `§Current process` — explicit critique of the current tool implies Satisfaction ≤ 2; explicit praise implies Satisfaction ≥ 4.
2. `§Pains` — the pain itself implies Satisfaction ≤ 2 for the affected jobs.
3. Absence of a section: default Satisfaction = 3 and mark `consultant-assigned-no-signal`.

Where the requirements doc has no scoring signal for a given dimension, mark the score with `consultant-assigned-no-signal` rather than inventing a confident number. Surface the count in the diagnostics block.

**Compute Opportunity Score:**

```
Opportunity = Importance + max(0, Importance - Satisfaction)
```

(Ulwick's canonical formula. Range: 1 to 10. Importance × low Satisfaction drives the score upward.)

**Priority bands:**

| Opportunity range | Band | Visual |
| --- | --- | --- |
| `≥ 8` | High | P1 (highlighted) |
| `6 – 7` | Medium | P2 |
| `≤ 5` | Low | P3 |

**Output of Round 5:** the job list with `importance`, `satisfaction`, `opportunity`, and `band` populated on every row, plus the `consultant-assigned-no-signal` marker count.

### Round 6 — Forces & Clusters

**Cluster jobs.** Group jobs into clusters. The default clustering rule is one cluster per `(actor, main-goal)` pair — collect every job (Functional + Emotional + Social) that shares an actor and serves the same overarching goal. A cluster typically holds 1 Functional + 0 – 3 Emotional + 0 – 2 Social rows.

**Capture forces of progress.** For each cluster, record the four Moesta forces where the requirements doc names them:

| Force | Definition | Source signal |
| --- | --- | --- |
| **Push** | Pain of the current situation that drives the actor toward change. | `§Pains`, complaint phrasing in `§Personas`. |
| **Pull** | Attraction of a new solution. | `§Goals`, value statements in `§1 Domain`, the product's promised benefit. |
| **Anxiety** | Fear or doubt about switching to the new solution. | `§Risks`, `§Constraints`, change-resistance prose. |
| **Habit** | Inertia / sunk cost of the existing tool. | `§Existing solutions`, `§Current process`, *"we've always done it this way"* prose. |

**If a force is not named anywhere in requirements, render it as `not-named-in-requirements`.** This is a content-gap marker, not a hard fail — most requirements docs name Push and Pull but rarely Anxiety and Habit. Surfacing the absence is the point.

**Output of Round 6:** the cluster list with `{cluster_id, actor, main_goal, job_ids[], push, pull, anxiety, habit}` populated. Each force is either a quoted phrase from requirements or the literal string `not-named-in-requirements`.

---

## Output presentation

The artefact's surfaces, in rendered (DOM) order:

0. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead: what this job map is, what it found, what the consultant should do with it. The **first** section, above the meta-grid. A faithful condensation of the map below — it introduces no job, count, or citation not already present, and carries no `[SRC]` of its own. Methodology jargon (job, job map, outcome, circumstance/context, forces of progress) is glossed at first use here; client domain terms are not glossed (the GLOSSARY methodology owns those). Per `framework/shared/output-readability.md`.

The artefact then renders as a job-card grid grouped by cluster headings. Color contract:

| Element        | Color               | What it carries                                                                |
|----------------|---------------------|--------------------------------------------------------------------------------|
| Type badge — Functional | blue           | Round 3 type = `functional`                                                    |
| Type badge — Emotional  | violet         | Round 3 type = `emotional`                                                     |
| Type badge — Social     | rose           | Round 3 type = `social`                                                        |
| WHEN sticky    | amber               | Round 2 situation clause                                                       |
| WANT-TO sticky | blue                | Round 2 motivation clause                                                      |
| SO-I-CAN sticky| green               | Round 4 outcome clause (or `(no-metric-in-requirements)`)                       |
| Scoring strip  | mixed dots + chip   | Importance dots (5), Satisfaction dots (5), Opportunity score + band chip      |
| Forces strip   | muted-italic when absent | Round 6 push/pull/anxiety/habit lines; `not-named-in-requirements` styled muted |

Plus a top-level **Opportunity Matrix** — a 5×5 HTML grid plotting jobs by `(importance, satisfaction)`. The top-right quadrant (Importance ≥ 4 ∧ Satisfaction ≤ 2) is highlighted as the "innovation opportunity zone".

---

## Quality gates (run after Round 6, before write)

Every gate is a hard gate. If any gate fails, the analyser does **not** write the artefact — it surfaces a structured error to the consultant and halts. (See `framework/agents/analyses/jtbd-analyser.md > Step 8 — Validate` for the halt contract.)

1. **Every situation is concrete.** Forbidden situation phrases (case-insensitive substring match): *"when using the app"*, *"when using the system"*, *"during a session"*, *"when the user opens the system"*, *"in general"*, *"sometimes"*. Flag offending jobs by `job_id` + the offending text.
2. **Every motivation is solution-agnostic.** Reject motivations containing UI-affordance tokens: `click`, `tap`, `navigate to`, `open the … dialog`, `select … from the dropdown`, `see … on the dashboard`, `view the … page`, `enter … in the field`. Flag offending jobs.
3. **Every outcome is measurable OR carries the `no-metric-in-requirements` marker.** Silent unmeasurable outcomes break downstream design consumption — the design phase has no acceptance signal. Flag the silent-unmeasurable jobs.
4. **Every job has a primary actor.** Anonymous jobs are weak signal. If `§Personas` is absent, allow a fallback actor `User (no persona section in requirements)` with the `derived-actor` marker; jobs without even that fallback are flagged.
5. **No orphan jobs.** A job whose actor name is not in `§Personas` and is not marked `derived-actor` is a data inconsistency — either spelling drift between `§Personas` and the job's actor field, or a missed marker assignment. Flag offending jobs.
6. **Every statement parses as the canonical form.** All three clauses (When / I want to / So I can) must be present and non-empty. One-clause-missing is malformed. Flag offending jobs.
7. **No solution-leak in outcomes.** Reject outcomes containing UI-affordance tokens (same list as Gate 2) plus the additional outcome-specific tokens `see the dashboard`, `view the report`, `download the file` (when the file is a UI artefact, not the actual deliverable). Outcomes describe states of the world the actor reaches, not UI artefacts. Flag offending jobs.

---

## Anti-patterns

- **Treating personas as jobs.** A persona is *who*; a job is *what they're hiring the product to do*. *"`Procurement Manager`"* is not a job; *"restore inventory levels when stock dips"* is.
- **Treating features as jobs.** A feature is the product's affordance; a job is the actor's intent. *"I want to use the bulk-edit feature"* is feature-leak; *"I want to update 50 prices in one operation"* is the underlying job.
- **Inventing measures from thin air.** If `§Acceptance criteria` / `§Constraints` / `§Success metrics` / `§Pains` do not anchor a measure, mark `no-metric-in-requirements` rather than guessing *"in under 5 minutes"*. The marker is honest; the guess is invented data.
- **Inventing Emotional / Social jobs.** If the requirements doc names no emotional or social signal, do not fabricate one. Functional-only is a legitimate state for many B2B / data-management products.
- **Collapsing rounds.** Do not write jobs and outcomes in the same pass. The round-by-round structure is what makes the map reviewable — collapsing rounds hides reasoning.
- **Editorialising.** The analyser is a literal lens onto the requirements doc. It does not propose new product features; it surfaces jobs the BA already documented (verbatim where named, derived where implied).
- **Inventing forces.** If `§Pains` / `§Goals` / `§Risks` / `§Existing solutions` do not name a force, mark `not-named-in-requirements`. Most requirements docs name 2 of 4 forces; surfacing the absence is the point.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/jtbd-analysis.md` — analytical, thorough, literal. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact is human-read (and optionally consumed by `/wireframe`'s `blueprint-architect` via the per-analysis sidecar), so the analyser also follows `framework/shared/output-readability.md`: it writes the "In plain terms" lead, glosses methodology jargon (job, job map, outcome, circumstance/context, forces of progress) at first use in human-readable prose, leaves client domain vocabulary unglossed (GLOSSARY territory), and keeps every `[SRC: C-NNN]` marker. The plain-language layer is confined to the lead and first-use glosses; the job map, scoring tables, and diagnostics keep their concrete, named-job, telegraphic discipline.
