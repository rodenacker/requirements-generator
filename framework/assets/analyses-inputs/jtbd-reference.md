<!-- ROLE: asset (analysis reference). Methodology definition for the JTBD input-analyser. Modelled on framework/assets/analyses/jtbd-reference.md (the requirements-doc-lensing sibling). Industry framing: hybrid Christensen-Moesta (canonical statement form + four forces of progress) + Ulwick (importance × satisfaction = opportunity scoring), adapted for raw consultant inputs enumerated via `requirements/source-manifest.json`. -->

# JTBD reference (input-analysis variant)

> **Method:** Walk every consumable source enumerated in `requirements/source-manifest.json`; extract actor + situation candidates from input prose, slide-deck text, and transcribed visual notes (Round 1); write canonical *"When `<situation>`, I want to `<motivation>`, so I can `<outcome>`."* statements (Round 2); classify Functional / Emotional / Social (Round 3); refine outcomes against measurable signals in the inputs (Round 4); score Importance × Satisfaction (Round 5); group into clusters and capture the four forces of progress where the inputs name them (Round 6). Every job carries `[SRC: <filename>]` citations. Outcomes without anchorable measures carry `(no-metric-in-inputs)`. Scores without anchorable signals carry `consultant-assigned-no-signal`. Forces with no input mention render as `not-named-in-inputs`. Across re-runs the artefact is **additive**: prior job cards, cluster headings, and force lines are preserved; new manifest content extends them.

**Output file:** `analyse-inputs/JTBD/jtbd-job-map.html` — a self-contained HTML job-card grid + opportunity matrix using `framework/assets/analyses-inputs/template-jtbd.html` as scaffold.

**Analyser agent:** `framework/agents/analyses-inputs/jtbd-analyser.md`

**Character:** `framework/assets/characters/jtbd-inputs-analysis.md`

**Sibling under `/analyse-requirement`:** `framework/assets/analyses/jtbd-reference.md` is the parallel methodology canon for lensing the synthesised `requirements/requirements.md`. The two references share the same hybrid framing (Christensen-Moesta + Ulwick), the same six rounds, the same opportunity formula, and the same seven quality gates. They differ **only** in the per-round source-extraction guidance (this reference reads raw inputs via the manifest; the sibling reads section anchors `§Personas` / `§Task flows` / `§Acceptance criteria` in `requirements/requirements.md`) and in the textual provenance markers (`[SRC: <filename>]` here vs the sibling's `provenance-from-personas` / `src-from-task-flows`-class markers; `(no-metric-in-inputs)` here vs the sibling's `(no-metric-in-requirements)`; `not-named-in-inputs` here vs the sibling's `not-named-in-requirements`; `consultant-assigned-no-signal` is identical in both).

---

## Industry framing — Christensen-Moesta + Ulwick adapted for raw consultant inputs

The two halves of the hybrid:

- **Christensen-Moesta** supplies the canonical statement form (*"When `<situation>`, I want to `<motivation>`, so I can `<outcome>`."*) and the four **forces of progress** (push / pull / anxiety / habit). Switch-interview methodology — Bob Moesta's original framing — was built for primary stakeholder voice: interview transcripts, complaint emails, sales-call notes. Raw consultant inputs are **JTBD's native habitat**.
- **Ulwick** ("Outcome-Driven Innovation") supplies the importance × satisfaction = opportunity scoring formula `Opportunity = Importance + max(0, Importance - Satisfaction)` with the 1–5 scale.

This analyser sits firmly in the **extraction** camp. The subject of every job is anchored to a verbatim or near-verbatim extract from a manifest-enumerated source; every outcome is either measurable from input prose or explicitly marked; every score is either anchored to an input signal or explicitly marked; every force is either a quoted input phrase or explicitly marked absent.

### Why apply JTBD to raw inputs?

| Lens | Methodology | Question answered | Operates on |
|---|---|---|---|
| Cross-cutting pattern recognition | thematic-analysis (input variant) | What recurring patterns do the inputs carry? | raw `input/` |
| Outcome-tree discovery | opportunity-solution-trees (input variant) | What desired outcomes do the inputs name and which opportunities ladder up? | raw `input/` |
| Current-state workflow mapping | journey-mapping (input variant) | What is the as-is user workflow described in the inputs? | raw `input/` |
| Hierarchical task decomposition | task-analysis (input variant) | How do the inputs decompose user goals into sub-goals and operations? | raw `input/` |
| **Jobs × situations × outcomes × forces** | **jtbd (input variant)** | **What jobs are users hiring the product to do, and what forces drive or resist their progress?** | **raw `input/`** |

JTBD on raw inputs is the **right complement** to the existing `/analyse-requirement` JTBD because:

1. The sibling lenses the synthesised `requirements/requirements.md`, which has already normalised consultant phrasing into *"the system shall …"* clauses — JTBD on that document surfaces jobs the **normaliser** preserved, not the jobs the **inputs** named.
2. Push / Pull / Anxiety / Habit signals live in primary source material (interviews, complaints, "we've always done it this way" prose). Synthesised requirements strip those signals out. Surfacing them **before** synthesis preserves the rich motivation data JTBD depends on.
3. The output can be **fed back** to `/requirements` as an additional source (manual copy into `input/`) — letting the consultant anchor the next requirements draft in extracted user motivation rather than feature wishlist.

### Why this analyser uses HTML, not Markdown + Mermaid

- **Visual job-card grid + opportunity matrix.** The methodology depends on a 5×5 importance × satisfaction grid with an innovation-zone highlight, and on cluster-grouped job cards with sticky-note clause boxes (WHEN amber, WANT-TO blue, SO-I-CAN green) + scoring dot rows + forces strips. None of that renders cleanly in markdown.
- **Mirror of the sibling.** `/analyse-requirement` JTBD also uses HTML with the same job-card grid + opportunity matrix; keeping the formats aligned makes side-by-side comparison trivial when a consultant runs both.
- **Re-ingestibility intact.** HTML still classifies as `Native-text` per `framework/skills/classify-input-tier.md` (UTF-8 passes the sniff; the `[SRC: <filename>]` markers survive as plain text). When the consultant copies the HTML into `input/`, the drafter reads its job-card content as candidate-requirement seeds directly. Markitdown conversion is **not** invoked for `Native-text` HTML — the drafter reads the HTML in-context.

---

## Output structure

The artefact has a fixed top-to-bottom shape (rendered by the template; placeholders are substituted by the analyser):

0. **In plain terms** (`<section id="plain-terms">`). `{{PLAIN_SUMMARY}}` — a 2–5 sentence plain-English lead (what this job map is, what it found, what the consultant should do with it). First section, above the meta-grid. Faithful condensation of the content below; introduces no new fact, count, or citation; carries no `[SRC]` of its own. Methodology jargon (job, job map, outcome, forces of progress, opportunity score) glossed at first use; client domain terms not glossed. Per `framework/shared/output-readability.md`.
1. **Overview block.** Title, subtitle, meta-grid (Domain, Generated timestamp, Manifest fingerprint, Source count + tier breakdown, Jobs, Clusters, Functional / Emotional / Social counts, High-Opportunity count).
2. **JTBD-meta** HTML comment carrying the additive-merge cursor (`manifest_fingerprint`, `run_count`).
3. **TOC** — static top-level anchors (Overview, Diagrams, Tabular information, Diagnostics).
4. **Job-card grid** (`<section id="diagrams">`). One `<section class="job-cluster">` per `(actor, main-goal)` pair; inside each cluster, one `<article class="job-card">` per job. Each card:
   - Type badge (Functional / Emotional / Social).
   - Priority badge (P1 / P2 / P3 from opportunity band).
   - Job ID (`J-NN`).
   - Actor row with `[SRC: <filename>]` source chip(s).
   - Statement stack: WHEN (situation) sticky / I WANT TO (motivation) sticky / SO I CAN (outcome — measurable or `(no-metric-in-inputs)`) sticky.
   - Scoring strip: Importance dots (5), Satisfaction dots (5), Opportunity score + band chip. Scores carry `consultant-assigned-no-signal` marker in Diagnostics if unsignaled.
   - Forces strip: Push / Pull / Anxiety / Habit lines; forces with no input mention render as `not-named-in-inputs` with the `not-named` CSS class.
5. **Opportunity matrix** (`<section id="tables">`). 5×5 grid plotting jobs by Importance (Y) × Satisfaction (X). Top-right quadrant (Imp ≥ 4 ∧ Sat ≤ 2) highlighted as the innovation-opportunity zone.
6. **Diagnostics** (`<details id="diagnostics">`, collapsed by default). Manifest fingerprint, source roster (Consumed table + Skipped table), gate results (1–7 pass / fail), provenance counts (jobs cited from each source), measure counts (measurable / `(no-metric-in-inputs)`), scoring marker counts (`consultant-assigned-no-signal`), force counts (named / `not-named-in-inputs`), run history.
7. **Downstream-use footer** (`<details class="downstream-toggle">`, collapsed by default). Re-ingestion instructions (how to copy this file into `input/` for a subsequent `/requirements` run). Pipeline-machinery prose; visible only on expand.

---

## The JTBD-X process

Six rounds, executed in order. The analyser does not skip rounds and does not collapse rounds into a single pass — each round's output feeds the next, and round-by-round structure is what makes the methodology auditable. The six rounds map to twelve workflow steps in the analyser agent (Activate / Read manifest / Detect prior artefact / Rounds 1–6 / Validate / Write / Handback).

### Round 1 — Situations & Actors

Read every consumable manifest row in full per its tier:

- `Native-text` → `Read original_path` directly as text.
- `Native-multimodal` → `Read original_path`; the Read tool surfaces image bytes automatically; the analyser transcribes visible text and structurally significant observations (whiteboard photos, sticky-note shots, screenshot captures of interview slides, etc.) to memory.
- `Supported-via-MCP` → `Read converted_sibling` (the `.converted.md`) — the input-handler has already converted the source via markitdown; the analyser does not re-invoke conversion.
- `Unsupported` → skipped; record the row in `skipped_rows` with the manifest's `conversions_applied` value as the reason.

Extract every actor + every situation candidate. Each candidate carries:

```
{
  candidate_id,
  actor,                                // verbatim or near-verbatim role name from the source
  actor_source_filename,                // the manifest row that named the actor
  situation,                            // verbatim or near-verbatim trigger condition from the source
  situation_source_filename             // the manifest row that named the situation (may differ from actor source)
}
```

**Actor sources.** Raw inputs do not have a `§Personas` section. Actor names come from:

1. **Role titles named in input prose** (briefs, decks, interview transcripts) — *"the Procurement Manager"*, *"the field engineer"*, *"a tier-1 customer service rep"*.
2. **Persona shorthand in interview notes** — first-person actor reference: *"as a buyer, I …"*.
3. **Descriptor fallback** — if a source describes an actor without naming a role title, lift the descriptor verbatim: *"the buyer mentioned in `brief.docx` para 12"*. The card still cites `[SRC: brief.docx]`; the descriptor is the actor field.

**No `[derived-actor]` marker.** Unlike the requirements-doc-lensing sibling JTBD analyser, this analyser does not distinguish `from-personas` vs `derived-actor` because raw inputs have no canonical persona section. All actors are `[SRC: <filename>]`-cited.

**Situation sources.** Each candidate situation is a verbatim or near-verbatim extract from input prose, slide-deck text, or transcribed visual notes. Forbidden vague phrases (rejected in Round 2 and as Gate 1): *"when using the app"*, *"when using the system"*, *"during a session"*, *"when the user opens the system"*, *"in general"*, *"sometimes"*.

**Output of Round 1:** an unfiltered candidate `{actor, situation, actor_source_filename, situation_source_filename}` list. Synonyms and near-duplicates are kept at this stage; deduplication happens in Round 2.

State the per-source candidate counts aloud:

> *"Round 1 (Situations & Actors): generated 24 candidates across 4 sources — `brief.docx`: 9 candidates (4 actors, 9 situations), `whiteboard-photo.png`: 3 candidates (2 actors, 3 situations), `interview-notes.md`: 8 candidates (3 actors, 8 situations), `slack-export.md`: 4 candidates (2 actors, 4 situations)."*

### Round 2 — Job Extraction

For each `(actor, situation)` candidate, write the canonical job statement:

> *"When `<situation>`, I want to `<motivation>`, so I can `<outcome>`."*

**Filter rules:**

- Merge near-duplicate jobs (same actor, near-identical situation + motivation). Prefer the more specific wording.
- Reject motivations that name **UI affordances**. Forbidden tokens in the motivation clause: `click`, `tap`, `navigate to`, `open the … dialog`, `select … from the dropdown`, `see … on the dashboard`, `view the … page`, `enter … in the field`. These are design-phase concerns, not jobs. Rewrite to the underlying intent (*"I want to click the export button"* → *"I want to retrieve the report's content in a portable format"*).
- Reject motivations that name a specific **product feature** by name (e.g., *"I want to use the new bulk-edit feature"*). Rewrite to the job the feature serves.
- Retain motivations the consultant's actor would name as a desired job outcome, even if the input prose phrases it as a feature.

**Output of Round 2:** the final job list. Each row carries:

```
{
  job_id,                          // J-NN zero-padded in discovery order
  actor,
  situation,
  motivation,
  outcome,                          // refined in Round 4
  source_filenames: [<filename>]    // union of actor_source_filename + situation_source_filename + motivation source if distinct
}
```

State the post-extraction count aloud:

> *"Round 2 (Job Extraction): wrote 12 jobs from 24 candidates (merged 9 near-duplicates, rejected 3 for UI-token leak in motivation: J-c-04 `I want to click export to PDF` rewritten to `I want to retrieve the report's content in a portable format`; J-c-07 `I want to use the dashboard filters` rewritten to `I want to narrow the visible records to the time-window I care about`; J-c-19 `I want to open the user profile dialog` rewritten to `I want to confirm my counterpart's role before signing off`)."*

### Round 3 — Job Typology

Classify each job as one of:

- **Functional** — the main, task-completion job. *"I want to restore inventory levels."*
- **Emotional** — how the actor wants to feel during or after the job. *"I want to feel confident the order will arrive in time."*
- **Social** — how the actor wants to be perceived by others. *"I want to be seen as the buyer who never lets us run out."*

**Rules:**

- A single `(actor, situation)` may yield jobs of multiple types — emit them as **separate rows**, each with its own `job_id`. A Functional job is not a parent of its Emotional or Social siblings; they coexist.
- Where the inputs have no Emotional or Social signal for a given Functional job, **do not invent** Emotional / Social rows. The cluster is `functional-only`. Surface the count in the Diagnostics block.
- Functional is the typology default. If a job's typology is ambiguous, classify as Functional and flag for consultant review.

**Output of Round 3:** the job list with `type ∈ {functional, emotional, social}` populated on every row.

State the typology shape aloud:

> *"Round 3 (Job Typology): 12 jobs typed — 9 functional, 2 emotional (J-04 `I want to feel confident the supplier will deliver on time` `[SRC: interview-notes.md]`, J-08 `I want to feel that the audit log will absolve me in a dispute` `[SRC: brief.docx]`), 1 social (J-11 `I want to be seen as the team member who catches errors before sign-off` `[SRC: slack-export.md]`)."*

### Round 4 — Outcome Refinement

For every job, the outcome clause must be **measurable**. A measurable outcome carries a unit of measure: time (*"in under 5 minutes"*), count (*"without re-entering data"*), threshold (*"with one confirmation step"*), absence (*"without missing the delivery deadline"*), or comparative (*"faster than the current email approval chain"*).

**Sources for measures, in priority order:**

1. **Explicit success metrics in briefs / decks / KPIs documents** — *"target: same-day reconciliation"*, *"SLA: 99.5% on-time delivery"*.
2. **Comparative figures in interview transcripts** — *"approval used to take 2 days; we want same-day"* → *"in under 1 day"*.
3. **Pain magnitudes in complaint emails / interview notes** — *"we lose 3 hours per reconciliation cycle"* → *"in under 1 hour"*.
4. **Threshold language in slide decks** — *"reduce error rate from 5% to under 1%"* → *"with fewer than 1% errors"*.

If no measure can be anchored from any source, **do not fabricate one**. Replace the outcome clause with a best-effort intent phrase plus the explicit literal marker `(no-metric-in-inputs)`, and surface the count in the Diagnostics block. Example: *"so I can avoid stockout (no-metric-in-inputs)"*.

**Output of Round 4:** the job list with every `outcome` clause either measurable (with `[SRC: <filename>]` on the measure source) or carrying the `(no-metric-in-inputs)` marker.

State the outcome shape aloud:

> *"Round 4 (Outcome Refinement): 12 outcomes refined — 7 measurable (5 from explicit metrics in `brief.docx`, 1 from comparative in `interview-notes.md`, 1 from pain magnitude in `slack-export.md`), 5 marked `(no-metric-in-inputs)`."*

### Round 5 — Importance & Satisfaction Scoring

For every job, assign:

- **Importance** — 1 to 5, on Ulwick's scale (1 = inconsequential, 3 = matters, 5 = critical to the actor's success).
- **Satisfaction** — 1 to 5, current-state with the actor's existing tools / process (1 = totally unsatisfied, 5 = fully satisfied).

**Sources for importance, in priority order:**

1. **Pain magnitude in input prose** — *"this blocks every quarter-end close"* → Imp ≥ 4; *"we lose 3 hours per cycle"* → Imp ≥ 4.
2. **Cross-source repetition** — a job named in ≥ 3 of 4 consumed sources → Imp ≥ 4.
3. **Explicit prioritisation language** — *"top three problems"*, *"the #1 thing we need to fix"* → Imp ≥ 4.
4. **Implicit role-criticality** — input prose describing the job as part of the actor's *"daily routine"* / *"core responsibility"* → Imp ≥ 3.

**Sources for satisfaction, in priority order:**

1. **Explicit critique of the current tool in input prose** — *"the spreadsheet falls over once we hit 50 line items"* → Sat ≤ 2; *"the current process works fine but is slow"* → Sat ≈ 3.
2. **Complaint phrasing in emails / Slack exports** — strong complaint → Sat ≤ 2; mild complaint → Sat ≈ 3.
3. **"We've always done it this way" prose** — implies the current solution is tolerated but not loved → Sat ≈ 2–3.
4. **Absence of any signal** → default Sat = 3 and mark `consultant-assigned-no-signal`.

Where the inputs have no scoring signal for a given dimension, mark the score with `consultant-assigned-no-signal` rather than inventing a confident number. Surface the count in the Diagnostics block.

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

State the scoring shape aloud:

> *"Round 5 (Scoring): 12 jobs scored — 4 P1 (Opp 8–10), 5 P2 (Opp 6–7), 3 P3 (Opp ≤ 5). 6 `consultant-assigned-no-signal` markers (3 importance defaults, 3 satisfaction defaults)."*

### Round 6 — Forces & Clusters

**Cluster jobs.** Group jobs into clusters. The default clustering rule is one cluster per `(actor, main-goal)` pair — collect every job (Functional + Emotional + Social) that shares an actor and serves the same overarching goal. A cluster typically holds 1 Functional + 0 – 3 Emotional + 0 – 2 Social rows.

**Capture forces of progress.** For each cluster, record the four Moesta forces where the inputs name them:

| Force | Definition | Source signal in raw inputs |
| --- | --- | --- |
| **Push** | Pain of the current situation that drives the actor toward change. | Complaint phrasing in interview notes / Slack exports; pain magnitude in briefs (*"we lose 3 hours per cycle"*); "the current process is broken" prose. |
| **Pull** | Attraction of a new solution. | Goal statements in briefs and decks (*"we want same-day reconciliation"*); value propositions in stakeholder presentations; "imagine if we could …" phrasing. |
| **Anxiety** | Fear or doubt about switching to the new solution. | Change-resistance prose (*"the team won't adopt anything new"*); risk language (*"we can't afford to break the audit trail during migration"*); concerns about training / disruption. |
| **Habit** | Inertia / sunk cost of the existing tool. | "We've always done it this way" prose; references to long-standing spreadsheets / processes; "the team is used to …" phrasing. |

**If a force is not named anywhere in the consumed inputs, render it as the literal string `not-named-in-inputs`.** This is a content-gap marker, not a hard fail — most raw input sets name Push and Pull but rarely name Anxiety and Habit. Surfacing the absence is the point: it tells the consultant which switch-interview questions are still missing.

**Output of Round 6:** the cluster list with `{cluster_id, actor, main_goal, job_ids[], push, pull, anxiety, habit}` populated. Each force is either a quoted phrase from input prose (with `[SRC: <filename>]` citation) or the literal string `not-named-in-inputs`.

State the cluster + force shape aloud:

> *"Round 6 (Forces & Clusters): 12 jobs into 5 clusters. Forces named across 5 clusters: 5 Push (all named, mostly from `interview-notes.md` and `slack-export.md`), 4 Pull (1 cluster has no Pull signal in inputs), 1 Anxiety (4 clusters carry `not-named-in-inputs` — switch-interview gap), 0 Habit (every cluster carries `not-named-in-inputs` — strong signal the consultant should add interview material on existing-tool inertia)."*

---

## Provenance markers

| Marker | Used in artefact section | Payload | Meaning |
|---|---|---|---|
| `[SRC: <filename>]` | Actor row chip, situation source chip, motivation source (rare; usually inherited from situation), outcome measure source (when measurable), force quoted phrase | basename including extension, matching a manifest row's `filename` field | The cited actor / situation / outcome / force phrase is anchored to this manifest source; the phrase is verbatim or a minimally rephrased lift from the row's content (or, for `Native-multimodal` rows, from the transcribed visual notes the analyser captured at Round 1) |
| `(no-metric-in-inputs)` | Outcome clause | (literal string, no payload) | The outcome clause has no anchorable unit of measure from input prose; carries a best-effort intent phrase plus the marker |
| `consultant-assigned-no-signal` | Importance dot row, Satisfaction dot row (rendered in Diagnostics not on the card) | (literal string) | The score has no anchorable signal from input prose; defaults to 3 |
| `not-named-in-inputs` | Forces strip | (literal string) | The named force has no lexical mention in any consumed source; renders with the `not-named` CSS class (muted italic) |

**No fifth marker.** **No `[AI-SUGGESTED]` markers anywhere in the artefact** — JTBD on raw inputs is extraction, not inference.

---

## Quality gates (7 hard gates)

Run at Round 6 close, before render. Each gate operates on the in-memory state. Failure handling follows the Revise / Override / Restart pattern (see § Failure handling below).

1. **Every situation is concrete.** Forbidden situation phrases (case-insensitive substring match): *"when using the app"*, *"when using the system"*, *"during a session"*, *"when the user opens the system"*, *"in general"*, *"sometimes"*. Flag offending jobs by `job_id` + the offending text + the situation source citation.
2. **Every motivation is solution-agnostic.** Reject motivations containing UI-affordance tokens: `click`, `tap`, `navigate to`, `open the … dialog`, `select … from the dropdown`, `see … on the dashboard`, `view the … page`, `enter … in the field`. Flag offending jobs.
3. **Every outcome is measurable OR carries the `(no-metric-in-inputs)` marker.** Silent unmeasurable outcomes break downstream consumption — the next `/requirements` run or design phase has no acceptance signal. Flag the silent-unmeasurable jobs.
4. **Every job has a primary actor + at least one `[SRC: <filename>]` source chip.** Anonymous or uncited jobs are weak signal. Flag offending jobs.
5. **No orphan source citations.** A `[SRC: <filename>]` payload that is not in the manifest's consumed rows is a data inconsistency — either spelling drift, or a citation for a source the manifest does not enumerate. Flag offending jobs.
6. **Every statement parses as the canonical form.** All three clauses (When / I want to / So I can) must be present and non-empty. One-clause-missing is malformed. Flag offending jobs.
7. **No solution-leak in outcomes.** Reject outcomes containing UI-affordance tokens (same list as Gate 2) plus the additional outcome-specific tokens `see the dashboard`, `view the report`, `download the file` (when the file is a UI artefact, not the actual deliverable). Outcomes describe states of the world the actor reaches, not UI artefacts. Flag offending jobs.

### Failure handling (Revise / Override / Restart)

On any hard-gate failure: do **not** write the artefact. Surface `AskUserQuestion` with three options:

1. `Revise — exit so the consultant can enrich input/ and re-invoke /analyse-inputs (Recommended)`
2. `Override — proceed and write a known-defective artefact (Run-history bullet records every violation)`
3. `Restart — re-run from Round 1 with a fresh manifest pass`

On **Revise**: hand back to the orchestrator with a `failed-handback` state.
On **Override**: record each failing gate in the Run-history bullet for this run; proceed to render.
On **Restart**: re-enter Round 1. Cap at three fail-Restart cycles; on the fourth, force the Revise path.

---

## Source-of-truth hierarchy

The analyser reads exactly the files the manifest enumerates, plus the prior artefact (for additive merge) and its own three asset files (character, reference, template). The manifest's `tier` field dictates the read path:

| Tier | Source location | Read mechanism |
|---|---|---|
| `Native-text` | `original_path` | `Read` directly as text |
| `Native-multimodal` | `original_path` | `Read` — Claude's vision surfaces image bytes; transcribe visible text/structure to a per-source notes buffer |
| `Supported-via-MCP` | `converted_sibling` | `Read` the `.converted.md` (markitdown's output, produced by input-handler) |
| `Unsupported` | — | Skipped; recorded in the Diagnostics block's Source roster > Skipped table |

The analyser **never** reads:

- Any path under `requirements/` other than `requirements/source-manifest.json`. In particular: not `requirements/requirements.md` (the requirements-doc-lensing sibling JTBD analyser is a separate run); not `requirements/requirements-draft.md`; not `requirements/consultant-answers.md`; not `requirements/draft-claims*.ndjson`.
- Any path under `framework/state/`.
- Any path under `framework/shared/` (textual references to `RF-NN` / `GR-NN` in this file and in the analyser are links for the reader, not file loads).
- Other analyses' artefacts (`analyse-requirements/<OTHER-METHOD>/...`, `analyse-inputs/<OTHER-METHOD>/...`).
- Any pattern-catalogue or design-system file.

---

## Anti-patterns

- **Treating personas as jobs.** A persona is *who*; a job is *what they're hiring the product to do*. *"`Procurement Manager`"* is not a job; *"restore inventory levels when stock dips"* is.
- **Treating features as jobs.** A feature is the product's affordance; a job is the actor's intent. *"I want to use the bulk-edit feature"* is feature-leak; *"I want to update 50 prices in one operation"* is the underlying job.
- **Inventing measures from thin air.** If the consumed inputs do not anchor a measure (no success metric, no comparative figure, no pain magnitude, no threshold language), mark `(no-metric-in-inputs)` rather than guessing *"in under 5 minutes"*. The marker is honest; the guess is invented data.
- **Inventing Emotional / Social jobs.** If the inputs name no emotional or social signal for a functional job, do not fabricate one. Functional-only is a legitimate state for many B2B / data-management products. Raw inputs are typically thinner on Emotional / Social than synthesised requirements docs — the sparsity is a signal, not a defect.
- **Collapsing rounds.** Do not write jobs and outcomes in the same pass. The round-by-round structure is what makes the map reviewable — collapsing rounds hides reasoning.
- **Editorialising.** The analyser is a literal lens onto the consultant's raw inputs. It does not propose new product features; it surfaces jobs the inputs already document (verbatim where named, near-verbatim where lightly rephrased from prose).
- **Inventing forces.** If the consumed inputs do not name a force, mark `not-named-in-inputs`. Most raw input sets name Push and Pull but rarely Anxiety and Habit; surfacing the absence is the point — it tells the consultant which switch-interview questions are still missing.
- **Inventing scoring confidence.** If the inputs do not anchor Importance or Satisfaction, default the score to 3 and mark `consultant-assigned-no-signal`. The consultant fills the gap at the handback or in a subsequent run with enriched inputs.
- **Reading `requirements/requirements.md`.** The merged requirements document is the *sibling* JTBD analyser's input. This analyser's source contract is `requirements/source-manifest.json` + the per-tier manifest rows. Crossing into `requirements.md` collapses the two analysers into one and erases the input-vs-derived distinction that makes the parallel pair valuable.
- **Re-invoking `markitdown-mcp`.** Conversions are the input-handler's responsibility; the manifest's `converted_sibling` path is the contract. Re-converting would produce drift between the analyser's reads and the manifest's recorded `sha256` field.
- **Bundling external JS / CSS.** The artefact is self-contained HTML (template-driven). No `<script>` tags, no external links, no font URLs — the template's inlined `<style>` block is the only styling source.

---

## Re-run semantics

- The cursor (`manifest_fingerprint`, `run_count`) lives in the artefact's HTML-comment header: `<!-- jtbd-meta: manifest_fingerprint=…, run_count=N -->`. No state file under `framework/state/`.
- On re-run, the analyser compares the current manifest fingerprint to the prior cursor's value:
  - **No change** → pure additive widening; only new jobs from new or changed manifest rows are appended (to the matching prior cluster if the new job shares the cluster's actor + main-goal, or as a new cluster if no prior cluster matches).
  - **Change** → the analyser surfaces a drift prompt: `append-new-jobs-only` (default; preserves prior cards verbatim, appends new jobs), `re-extract-everything` (re-runs Rounds 1–6 from scratch; cluster headings preserved where re-extraction produces equivalent clusters), or `abort` (exit without writing).
- The artefact is monotonically growing across runs unless the consultant explicitly chose `re-extract-everything` or manually edited the file.

---

## Downstream usage — `/requirements` round-trip

The JTBD-inputs artefact is **re-ingestible by `/requirements`** as a fresh source. The contract:

1. Consultant copies `analyse-inputs/JTBD/jtbd-job-map.html` into `input/` (file copy; the orchestrator does not automate this).
2. Consultant re-invokes `/requirements` (or any of `/analyse-inputs`, `/review-inputs`, `/generate-prd`).
3. The shared `framework/agents/input-handler.md` agent detects the new file on its drift check; surfaces the manifest-refresh prompt; classifies the file via `framework/skills/classify-input-tier.md` as `Native-text` (HTML passes the UTF-8 / printable-ratio sniff); adds it to `requirements/source-manifest.json` as a new row.
4. The `/requirements` drafter reads the new row's `original_path` (no markitdown conversion needed — `Native-text` is read directly) and extracts candidate-requirement seeds from the job-card content. The `[SRC: <filename>]` markers inside the JTBD artefact reference the original briefs / interview notes; the drafter's own `[SRC: C-NNN]` claim IDs cite the JTBD artefact; the audit trail is preserved end-to-end through the dual-citation chain.

This pathway is **consultant-driven**, not automated. The orchestrator does not move files across pipelines; the analyser's Step 12 handback message tells the consultant about the round-trip and they decide whether to use the JTBD map as `/requirements` input or as a stand-alone discovery artefact.

The `framework/skills/map-jtbd-from-inputs-to-ui.md` skill (stub on framework first-ship) sketches the broader signal-to-pattern mapping for future downstream design-spec authors.

---

## Stop-condition

The analysis is complete when:

- `final_jobs` is non-empty (or the consultant Override'd a zero-job run with a recorded reason in Run-history).
- All 7 hard gates pass, or the consultant chose Override and the failures are recorded in Diagnostics.
- `analyse-inputs/JTBD/jtbd-job-map.html` has been written and `verify-artifact-write` returned `pass`.
- The consultant chose Accept in the Step 12 handback loop.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/jtbd-inputs-analysis.md` — extraction-only, citation-bound, motivation-anchored, force-honest, additive. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

The analyser also follows `framework/shared/output-readability.md` (operative rules restated in the character's *Reader & plain language* block, so no `framework/shared/` read is needed at run time): writes the "In plain terms" lead, glosses methodology jargon at first use in human-readable prose (job, job map, outcome, forces of progress, opportunity score), leaves client domain vocabulary unglossed (GLOSSARY territory), keeps every `[SRC: <filename>]` marker; plain prose confined to the lead + glosses; the structured body (cards, matrix, diagnostics) keeps its concrete, telegraphic discipline.
