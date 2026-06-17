<!-- ROLE: asset (analysis reference). Methodology definition for the Business Context Definition input-analyser. Industry framing: a pragmatic synthesis of enterprise-motivation modelling — OMG Business Motivation Model (BMM: Ends = Vision / Goal / Objective) + IIBA BABOK (Define Business Need; underlying-cause-vs-symptom) + Five-Whys / root-cause analysis (Toyoda) + Gause & Weinberg problem-as-gap discipline + Design Thinking POV / "How Might We" reframing + KAOS AND/OR goal refinement (van Lamsweerde) kept at the enterprise tier, adapted for raw consultant inputs enumerated via `requirements/source-manifest.json`. -->

# Business Context Definition reference (input-analysis variant)

> **Method:** Walk every consumable source enumerated in `requirements/source-manifest.json`; inventory the organisational entities that hold motivation — sponsor, owning business unit, affected stakeholders, external forces (Pass 1); harvest every **explicitly stated** Business Problem, Business Need, Business Goal, Objective, and Problem Statement from input prose, deck text, and the frozen visual descriptions (Pass 2); derive **inferred** items by laddering along the problem→need→goal chain via one named technique — anchored to a source, never from world knowledge (Pass 3); classify each item into exactly one bucket, type the goals against the BMM Ends ladder, and tag each need problem-/opportunity-driven (Pass 4); assemble the problem→need→goal→problem-statement causal chain (Five-Whys per problem; KAOS AND/OR refinement of goals into objectives) (Pass 5); write canonical statements, frame the human-centered POV+HMW Problem Statement, run the seven hard gates, and surface goal/need conflicts (Pass 6). Every **explicit** item carries `[SRC: <filename>]`. Every **inferred** item carries `[AI-SUGGESTED: AI-NN | blocking|non-blocking]` PLUS the anchor `[SRC: <filename>]` it was laddered from PLUS the named technique used. Objectives without an anchorable target carry `(no-target-in-inputs)`. Across re-runs the artefact is **additive**: prior cards, the causal chain, and the goal hierarchy are preserved; new manifest content extends them.

**Output file:** `analyse-inputs/BUSINESS-CONTEXT-DEFINITION/business-context-definition.html` — a self-contained, readability-optimised HTML business-context report using `framework/assets/analyses-inputs/template-business-context-definition.html` as scaffold, carrying the four mandated artefacts (Business Needs Assessment, Business Problem Statement, Business Goals collection, Problem Statement) plus the causal chain that links them.

**Analyser agent:** `framework/agents/analyses-inputs/business-context-definition-analyser.md`

**Character:** `framework/assets/characters/business-context-definition-inputs-analysis.md`

**No `/analyse-requirement` sibling.** Like User Goal Analysis, Business Context Definition ships only on the inputs side. The synthesised `requirements/requirements.md` has already normalised the consultant's brief into *"the system shall …"* clauses — by then the *enterprise motivation* (why the organisation is funding any change at all) has been collapsed into features. Surfacing the business context **before** synthesis (and feeding it back into `/requirements` as strategic framing) is the entire value; a requirements-doc-lensing variant would surface only the motivation the normaliser happened to preserve.

---

## Scope — enterprise motivation only

Business Context Definition answers one question: **"Why is the sponsoring organisation funding any change at all?"** It operates at the **enterprise / sponsor altitude** — market position, cost, compliance, revenue, capability, risk — and produces a causal account of the organisation's problem, need, goal, and a solution-neutral problem framing.

**Hard boundary against `user-goal-analysis` (the load-bearing scope rule).** A **Business Goal** is an *organisational end-state* (BMM sense — *"become the most reliable next-day supplier in the region"*). A **user goal** is an *actor's task / life / experience goal* (Cooper sense — *"find a supplier in under a minute"*, *"feel confident the order will arrive"*). The two methods are **complementary, not overlapping**: run both on one `input/` and get the sponsor's "why fund this" (BCD) and the actor's "what do I want to do" (User Goal Analysis) as two clean registers. BCD never extracts actor goals; any actor-goal material it encounters is **routed, not lost** — recorded in Diagnostics as `deferred-to-user-goal-analysis` and ejected before classification (decision tree D0) and re-checked at gate time (Q6). The disambiguator: *organisational subject (market / cost / compliance / capability / revenue)* → enterprise → BCD; *a person doing a task at their desk* → actor → User Goal Analysis.

---

## Industry framing — an enterprise-motivation core adapted for raw consultant inputs

Business Context Definition is **not** a single named author's framework; it is a deliberate synthesis of the most load-bearing ideas across business analysis and goal-oriented requirements engineering, kept lean enough to execute by carefully reading documents. The chosen core:

| Building block | Source | What it contributes |
|---|---|---|
| **Ends ladder — Vision / Goal / Objective** | OMG **Business Motivation Model** (BMM 1.3) | The backbone of the Business Goals collection. A **Goal** is qualitative + long-term (*"be the reliability leader"*); an **Objective** is its measurable + time-bound child (*"cut late shipments to <2% by FY27"*). A **Vision** is the apex amplified by goals — recorded only if explicitly stated. |
| **Business Need = problem OR opportunity** | IIBA **BABOK** (*Define Business Need*) | The Business Needs Assessment. A need is the *imperative for change* — the gap between current and desired state — driven by a problem to remove **or** an opportunity to capture. |
| **Underlying-cause vs symptom** | IIBA **BABOK** (Root Cause Analysis, 10.40) | The discipline that separates a Business Problem's symptom from its root cause; feeds the Five-Whys ladder in Pass 5. |
| **Five-Whys / root-cause analysis** | Sakichi Toyoda / Toyota | The Business Problem decomposition: climb from a stated symptom to an organisationally-actionable root cause. Also one inference technique. |
| **Problem-as-gap** | Gause & Weinberg, *Are Your Lights On?* | *"A problem is the difference between things as perceived and things as desired."* The framing discipline behind both the Business Problem and the human-centered Problem Statement. |
| **POV + "How Might We"** | Design Thinking (d.school / IDEO lineage) | The human-centered Problem Statement (artefact #4): a solution-neutral reframe naming who is affected, what they need, and why, opened as a *"how might we…"* prompt to orient solution exploration. |
| **AND/OR goal refinement** | van Lamsweerde, **KAOS** | The goal hierarchy spine, kept at the enterprise tier: a Goal refines into sub-goals (AND = all required, OR = alternative strategies) and bottoms out in measurable Objectives. |

This analyser sits in the **bounded-inference** camp, not the pure-extraction camp that JTBD occupies — the same camp as the already-shipped `user-goal-analysis`, `task-analysis`, and `swim-lane-process-mapping` analysers. Inference is an explicit point of the method (business problems, needs, and goals are frequently implicit in a brief) — but it is **anchored**: every inferred item is a transformation of cited input evidence via a named, reproducible technique, never an author's free-floating idea.

### Why apply Business Context Definition to raw inputs (and how it differs from its neighbours)

| Lens | Methodology | Question answered | Operates on |
|---|---|---|---|
| Cross-cutting pattern recognition | thematic-analysis | What recurring patterns do the inputs carry? | raw `input/` |
| Outcome-tree discovery | opportunity-solution-trees | What desired outcomes do the inputs name and which **solutions** ladder down? | raw `input/` |
| Jobs × situations × outcomes × forces | jtbd | What jobs are users hiring the product to do? (extraction only) | raw `input/` |
| **User** goals — stated + inferred — classified + refined | user-goal-analysis | What do the **actors** want to achieve (of what Cooper type, in what hierarchy)? | raw `input/` |
| **Enterprise** motivation — problem → need → goal → problem-statement | **business-context-definition** | **Why is the sponsoring organisation funding any change at all?** | **raw `input/`** |

The scope boundaries are **hard** — enforced as analyser anti-patterns, the character's discipline, and quality gate Q6:

- **vs USER-GOAL-ANALYSIS.** The sharpest and most important boundary. BCD's subject is always the *organisation*; User Goal Analysis's subject is always an *actor*. A Business Goal names a market/cost/compliance/capability end-state; an actor goal names what a person accomplishes. BCD ejects actor-goal material to `deferred-to-user-goal-analysis` (D0 + Q6) — it never classifies it as a Business Goal.
- **vs OPPORTUNITY-SOLUTION-TREES.** OST runs outcome → opportunities → **solutions** → assumption-tests. BCD **never proposes a solution** — a stated solution is only ever an inference *anchor*; the human-centered Problem Statement (artefact #4) is deliberately solution-**neutral** (a "how might we", never a "we will build").
- **vs FIVE-WHYS (`/analyse-requirement`).** Five-Whys produces a root-cause chain for a single given problem. BCD *uses* the why-laddering motion as one inference technique inside a larger account, but its output is a four-artefact business-context report with a problem→need→goal causal chain, not a bare cause chain.
- **vs JTBD.** A job is situational progress for an actor. BCD writes no `When … I want … so I can …` statements and scores no forces; it works at enterprise altitude.

### Why this analyser uses HTML, not Markdown

- **Readability is the deliverable.** The consultant wants a report optimised for reading: a causal-chain map, need/problem/goal cards, a 5-Whys ladder, a POV+HMW frame, with explicit-vs-inferred items visually distinguished at a glance. A self-contained HTML page renders that cleanly in any browser with no tooling.
- **The #2-vs-#4 distinction must be visible.** The "Business Problem Statement" (#2) and the human-centered "Problem Statement" (#4) collide on the word *problem*; the template gives each its own section with an inline caption, and the causal-chain map shows #4 as the downstream *mouth* of the chain so the reader is never confused.
- **Inferred items must be obvious.** Inference is the method's main risk surface; the template gives inferred items a distinct `.ai-suggested` amber treatment (badge + technique + anchor) so a reviewing consultant can audit each immediately.
- **Dependency-free.** The causal-chain map and the goal hierarchy render as **CSS-only** structures — **no Mermaid, no `mmdc`, no `RF-07` dependency, no CDN, no `<script>`**. The page opens offline and prints cleanly.
- **Re-ingestibility intact.** HTML still classifies as `Native-text` per `framework/skills/classify-input-tier.md`; the embedded JSON body block survives a markitdown HTML→MD round-trip as a fenced code block, so a downstream `/requirements` run consumes the full business-context model.

---

## The four mandated artefacts — crisp definitions, governing framework, and litmus test

Each artefact is one section of the report. The four litmus tests are mutually exclusive by construction (see the decision tree).

### 1. Business Need — the Business Needs Assessment (`#needs`)

- **Definition.** The organisation's *imperative for change* — the gap between the current and the desired state, driven by a problem to remove **or** an opportunity to capture. (BABOK *Define Business Need*; Gause & Weinberg problem-as-gap.)
- **Litmus test.** *"Does the statement assert the organisation must change because a gap exists between where it is and where it needs to be?"* → Business Need.
- **Canonical form.** *"The organisation needs to close the gap between `<current>` and `<desired>` because `<strategic / tactical pressure>`."* Tagged `problem-driven` | `opportunity-driven`.
- **Id:** `BN-NN`.

### 2. Business Problem — the Business Problem Statement (`#problems`)

- **Definition.** The *current, undesired organisational state or dysfunction* — what is going wrong now — with a Five-Whys ladder separating symptom from root cause. (BABOK underlying-cause-vs-symptom; Five-Whys.) Diagnostic, present-tense.
- **Litmus test.** *"Does the statement describe a present-tense organisational dysfunction (symptom or root cause) without naming the desired end-state or a solution?"* → Business Problem.
- **Canonical form.** A symptom → cause ladder (`why_chain`), each rung cited or anchored, terminating at an organisationally-actionable root cause.
- **Id:** `BP-NN`.
- **Load-bearing asymmetry.** A Business Problem is only the **problem-driven** half of the need landscape. An **opportunity-driven** Business Need has **no** Business Problem beneath it — there is no dysfunction, only unrealised upside. Enforced by gate **Q4d** and visible on the page.

### 3. Business Goal — the Business Goals collection (`#goals`)

- **Definition.** A *desired organisational end-state* the enterprise wants to reach or sustain (BMM **End**). Qualitative + long-term. Refined via KAOS AND/OR into measurable, time-bound **Objectives** (also BMM Ends, one tier down).
- **Litmus test.** *"Does the statement name a desired organisational end-state the enterprise wants to reach or sustain (not an actor's task, not present dysfunction)?"* → Business Goal. **Goal-vs-Objective sub-test:** qualitative + long-term → **Goal** (`BG-NN`); measurable + time-bound → **Objective** (`OBJ-NN`, always the child of a Goal).
- **Canonical form (Goal):** *"`<Organisation/BU>` wants to `<qualitative end-state>`."* **(Objective):** *"`<measurable target>` by `<deadline>`."*
- **Ids:** `BG-NN` (goals), `OBJ-NN` (objectives). A **Vision** is recorded only if explicitly stated, as the apex of the hierarchy (no separate id prefix — it is `BG-00` / labelled `vision` in `bmm_tier`); a Vision is **never inferred** (an inferred vision is always a platitude — see the STOP rule).

### 4. Problem Statement — the human-centered reframe (`#problem-statement`)

- **Definition.** A *solution-neutral, human-centered reframing* of the business problem/opportunity that orients solution exploration without prescribing a solution. (Design Thinking POV + "How Might We"; Gause & Weinberg.)
- **Litmus test.** *"Is the statement a solution-neutral 'how might we…' / POV framing, derived from a Business Problem or opportunity, naming an affected party's need but no solution?"* → Problem Statement.
- **Canonical form.** **POV:** *"`<affected party>` needs `<need>` because `<insight>`."* **+ HMW:** *"How might we `<enable the need>` so that `<business goal>`?"*
- **Id:** `PS-NN`.

### Resolving the #2-vs-#4 collision (mandatory — the analyser must keep these distinct)

The two artefacts share the word *problem* but differ on four orthogonal axes:

| Axis | #2 Business Problem Statement | #4 Problem Statement |
|---|---|---|
| **Tense / orientation** | Present-tense **diagnosis** (what is broken now) | Forward-looking **brief** (what to explore) |
| **Subject** | The **organisation** (process, cost, risk, capability) | The **human affected** at enterprise altitude (the sponsor's stakeholder), framed for empathy |
| **Governing lens** | BABOK + Five-Whys (root-cause) | Design Thinking POV + HMW (reframe) |
| **Posture** | **Analytical** — establishes the cause | **Generative** — opens the solution space |
| **Causal-chain role** | The **root** of the chain (or its opportunity twin) | The **mouth** of the chain — the handoff to `/requirements` |

**One-sentence rule the consultant memorises (printed inline on the page):** *"The Business Problem Statement says what is wrong with the organisation today and why (diagnosis, looks backward to root cause); the Problem Statement says how we might help the people affected, framed so a solution search can begin (brief, looks forward)."* Artefact #4 is always **derived from** #2 (or an opportunity), never independent — enforced by gate **Q5c**.

---

## Output structure

The artefact has a fixed top-to-bottom shape (rendered by the template; placeholders are substituted by the analyser). **Diagram-first** ordering: the causal-chain map — the connective tissue of the whole method — leads, so the reader sees how the four artefacts connect before meeting the detail cards.

0. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead: what this business-context analysis is, what it found, and what the consultant should do with it. The **first** section, above the overview/meta-grid. A faithful condensation of the content below — it introduces no fact, count, or citation not already present, and carries no `[SRC]` of its own. Methodology jargon (business goal, stakeholder, causal chain, BMM Ends, KAOS AND/OR, etc.) is glossed at first use here; client domain terms are not glossed (the GLOSSARY methodology owns those). Per `framework/shared/output-readability.md`.
1. **Overview block.** Title, subtitle, meta-grid (Domain, Generated timestamp, Manifest fingerprint, Sources consumed, Tier breakdown, Problems / Needs / Goals / Objectives / Problem-Statements counts, Explicit / Inferred counts, Problem-driven / Opportunity-driven need split, Tensions count).
2. **`bcd-meta` HTML comment** carrying the additive-merge cursor (`manifest_fingerprint`, `run_count`).
3. **TOC** — static top-level anchors.
4. **Causal-chain map** (`<section id="causal-map">`) — **the diagram, placed first among the content sections.** A CSS-only four-column grid swimlane (Problem | Need | Goal/Objective | Problem-Statement) with styled connectors; one row per chain. Inferred nodes carry the `.ai-suggested` amber treatment. No JS, no Mermaid.
5. **Business Needs Assessment** (`<section id="needs">`, artefact #1). `BN-NN` cards tagged `problem-driven`/`opportunity-driven`, each with the current→desired gap, the strategic pressure, provenance, and links to the problem(s) below / goal(s) above.
6. **Business Problem Statement** (`<section id="problems">`, artefact #2). `BP-NN` cards each carrying a CSS-only Five-Whys symptom→root-cause ladder, provenance, and the need(s) it feeds. (Opportunity-driven needs correctly show **no** problem here.)
7. **Business Goals** (`<section id="goals">`, artefact #3). BMM-tiered: Vision (only if explicitly stated) → Goals → Objectives, as a nested CSS-only KAOS AND/OR tree plus per-goal cards. Objectives show their SMART target or `(no-target-in-inputs)`.
8. **Problem Statement** (`<section id="problem-statement">`, artefact #4). `PS-NN` cards in POV+HMW form, naming the affected party and the goal served, each with an explicit "derived from `BP-NN` / opportunity" link. An inline caption restates the #2-vs-#4 distinction.
9. **Tensions** (`<section id="tensions">`). A table of goal/need pairs that pull against each other, surfaced never resolved, with `[SRC: <filename>]` evidence. Empty is a legitimate state.
10. **Machine-readable model** (`<section id="body">` → `<pre><code class="language-json" id="bcd-body">`). The re-ingestion contract per the JSON schema below.
11. **Round-trip footer** (`<section id="round-trip">`). Static paragraph telling the consultant how to feed the report into a subsequent `/requirements` run.
12. **Diagnostics** (`<details id="diagnostics">`, collapsed). Totals, provenance counts, inference-technique breakdown, confidence distribution, problem-/opportunity-driven split, need-without-problem honest markers, Source roster (Consumed + Skipped), 7 gate results, the `deferred-to-user-goal-analysis` boundary-audit log, flagged low-confidence inferred items, run history.

---

## The six-pass process

Six passes, executed in order. The analyser does not skip or collapse passes — each pass feeds the next, and pass-by-pass structure is what makes the business-context model auditable. The six passes map to twelve workflow steps in the analyser agent (Activate / Read manifest / Detect prior artefact / Passes 1–6 / Validate / Write / Handback).

### Pass 1 — Sponsor & context inventory

Read every consumable manifest row in full per its tier (`Native-text` → `original_path`; `Native-multimodal` / `Vector-renderable` / `Supported-via-MCP` → `converted_sibling`; `Unsupported` → skipped + recorded — see the Read-path resolution rule in `framework/skills/build-source-manifest.md`). The `converted_sibling` for a visual tier is a frozen textual description prepared by the input-handler; treat it as the canonical text source and do **not** re-interpret pixels. Lift every **organisational entity** that holds or shapes motivation — verbatim or near-verbatim. Each entity carries:

```
{ org_id, name, kind, source_filenames: [<filename>] }   // kind ∈ {sponsor, business-unit, stakeholder, external-force}
```

`external-force` covers regulators, competitors, market shifts, and other SWOT-style influencers named in the inputs. Every entity is `[SRC: <filename>]`-cited. The organisation-under-analysis and its sponsor are entities; an end-user persona doing a desk task is **not** (that is User Goal Analysis territory — note it for D0). State the per-source entity counts aloud.

### Pass 2 — Explicit harvest (broad pass)

Scan every consumed source and lift each **stated** Business Problem, Business Need, Business Goal, Objective, or Problem Statement verbatim or near-verbatim, routing each through the decision tree (below) to a provisional bucket. Signal vocabulary:

- **Problem signals:** *currently, today, the problem is, we can't, we struggle to, it takes N hours, error-prone, manual, bottleneck, costs us, we lose.*
- **Need signals:** *we need to, we must, there is a need for, to stay competitive, in order to scale, the business requires.*
- **Goal / Objective signals:** *our goal is, our vision is, we aim to, we want to become, the objective is, target, by FY/Q, KPI, success looks like, by `<date>`, reduce X to Y.*
- **Problem-statement signals:** *how might we, the challenge is to, from the customer's point of view, what users need is.*

Each explicit item carries `{ id, raw_text, source_filenames: [<filename>], provenance: "explicit", bucket }`. Ids are minted per-bucket in discovery order (`BP-/BN-/BG-/OBJ-/PS-NN`). **Stated solutions / features / technologies / quality-adjectives are NOT items** — set them aside as Pass-3 anchors (decision-tree D5). Capture broadly; de-duplication, BMM typing, and statement-writing happen in later passes. State the post-harvest counts aloud (per bucket, per source).

### Pass 3 — Inferred derivation (anchored)

This is the method's signature pass and its primary risk surface. For each **stated solution, feature, pain-point, market signal, or quality-adjective** that does not already have an explicit item, derive the underlying problem / need / goal / problem-statement via exactly **one** named technique (closed set below). The inferred item carries:

```
{
  id,                              // BP-/BN-/BG-/OBJ-/PS-NN, continuing the per-bucket numbering
  ...bucket-specific fields,
  provenance: "inferred",
  ai_id,                           // AI-NN, zero-padded, assigned in discovery order (stable across append-only runs)
  blocking,                        // true|false — see blocking semantics below
  confidence,                      // HIGH|MEDIUM|LOW — secondary metadata (see below)
  inference: {
    technique,                     // one of the 6 named techniques
    anchor_text,                   // the verbatim stated solution/pain/signal/adjective it laddered from
    anchor_source_filenames: [<filename>]   // ≥1 — REQUIRED; an inferred item with no anchor is FORBIDDEN (Q2)
  }
}
```

**Anti-confabulation rule (load-bearing — Gate Q2).** No inferred item may exist without ≥1 source anchor and exactly one named technique. An item "the organisation probably also wants…" with no anchor in any consumed source is **forbidden** — it is invention, not inference. This mirrors `user-goal-analysis`'s anti-confabulation gate and `task-analysis`'s "inferred terminals forbidden".

State the inference shape aloud (count per technique).

### Pass 4 — Classification & well-formedness typing

For each item (explicit + inferred):

- **Confirm the bucket** per the decision tree; resolve any provisional ties.
- **Goals:** assign `bmm_tier ∈ {vision, goal, objective}`; confirm a Goal is **qualitative** (not a smuggled requirement, not a bare number) and an Objective is **SMART** (or carries `(no-target-in-inputs)`).
- **Needs:** tag `driver ∈ {problem-driven, opportunity-driven}`.
- **Problem Statements:** confirm solution-neutral + human-centered (POV+HMW form, names an affected party, no solution token).
- **Inferred items:** assign `confidence ∈ {HIGH, MEDIUM, LOW}` and the canonical `blocking|non-blocking` flag (mapping below).

State the classification shape aloud (counts by bucket; BMM tier counts; need driver split).

### Pass 5 — Causal-chain assembly + decomposition

**Build the causal chain.** Link the four artefacts into the problem→need→goal→problem-statement chain:

- Run **Five-Whys** per Business Problem: a `why_chain` from the stated symptom to an organisationally-actionable root cause (each rung cited or `[SRC]`-anchored; the floor stop-rule prevents descent into actor-task mechanics or individual blame).
- Each **Need** links to ≥1 Business Problem (`from_problems`) **or** ≥1 opportunity (`from_opportunities`) — never zero (Q4a).
- Each **Goal** links to ≥1 Need it serves (`from_needs`) (Q4b).
- Each **Objective** is the child of exactly one Goal (`parent_goal`) (Q4c).
- Each **Problem Statement** links to ≥1 Business Problem or opportunity it was reframed from (`derived_from`) and names the Goal it serves (Q5c).

**Build the goal hierarchy (KAOS AND/OR).** Arrange Goals (and the Vision, if stated) from apex down to Objectives. Each non-leaf node refines via **AND** (all children required) or **OR** (alternative strategies); leaves are Objectives or operationalisable Goals. Every Goal/Objective appears exactly once. Record typed edges in `causal_links`.

State the chain shape aloud (chain count, max why-depth, AND/OR node counts).

### Pass 6 — Statement framing + gates + tensions

**Write canonical statements** for every item per the forms in the four-artefact definitions above. The Business Problem renders its `why_chain`; the Goal renders qualitatively; the Objective renders its SMART target; the Problem Statement renders POV+HMW.

**Surface tensions.** Identify pairs of Goals or Needs that pull against each other (e.g. *"next-day reliability"* vs *"cut logistics cost 10%"*). Each tension carries `{ between: [id, id], note: <one-line tension>, source_filenames: [<filename>] }`. **Surface, never resolve** — resolution is the consultant's call (often a `/requirements` trade-off). An empty tension set is legitimate.

Close `final_org`, `final_problems`, `final_needs`, `final_goals`, `final_objectives`, `final_problem_statements`, `final_causal_links`, and `final_tensions`. The validate sweep (Step 10) adds no entities.

State the final shape aloud (statements written, tensions surfaced).

---

## Named inference techniques (Pass 3 closed set)

Each inferred item records **exactly one** technique. Adding a technique means appending to this list (never renumbering):

| Technique | Motion | Produces | Example (anchor → inferred item) |
|---|---|---|---|
| `five-whys-root-cause` | Repeated "why?" on a stated symptom until an organisationally-actionable root cause surfaces. | a **Business Problem** (root cause) | *"orders ship late"* → root: **fulfilment lacks real-time cross-warehouse stock visibility**. |
| `bmm-laddering` | Means-end climb from a Need/Problem to the organisational end-state it serves. | a **Business Goal** | *"stop losing enterprise deals to slow onboarding"* → Goal: **be the fastest-to-value vendor in our segment**. |
| `opportunity-reframe` | Recast a capability gap or market signal as an opportunity-driven Need (not dysfunction). | an opportunity-driven **Need** | *"competitors launched self-serve"* → Need: **capture the self-serve segment before it consolidates**. |
| `abductive-best-explanation` | Given stated effects with no stated cause, infer the **single most economical** organisational cause. | a **Business Problem** (root) | *"churn up, NPS flat, export tickets rising"* → **the export workflow is the dominant dissatisfaction driver**. |
| `swot-influencer-inference` | A named external force (regulation, competitor, market shift) implies a Need or Goal to respond. | a **Need** or **Goal** | *"data-residency law lands 2027"* → Need: **achieve in-region residency ahead of the 2027 deadline**. |
| `pov-hmw-reframe` | Transform a Business Problem/opportunity into a solution-neutral human-centered Problem Statement. | a **Problem Statement** (#4) | BP *"manual reconciliation costs 3 days/quarter"* → PS: *"Finance leads need reconciliation to keep pace with close. How might we let them close without manual matching so month-end is never the bottleneck?"* |

**STOP rules (anti-over-climb + anti-fabrication):**

1. **Vision-ceiling stop.** `bmm-laddering` / `swot-influencer-inference` climb only to the **first domain-specific organisational end-state**; stop one rung below any platitude (*"maximise shareholder value"*, bare *"grow revenue"* with no domain object). A platitude root fails Q5d. A BMM **Vision** is recorded **only if explicitly stated** in a source — it is never inferred (an inferred vision is always a platitude).
2. **Root-cause floor stop.** `five-whys-root-cause` / `abductive-best-explanation` stop at the first **organisationally-actionable** cause — never descend into individual blame or actor-task mechanics (that crosses into user-goal / task-analysis territory and fails Q6).
3. **Single-leap economy.** `abductive-best-explanation` infers **one** best explanation per effect-cluster, marks it `blocking`, and notes alternatives in Diagnostics for the consultant to adjudicate.
4. **No anchorless item.** No anchor `[SRC]` + technique → the item does not exist (Q2).

**Near-duplicate merge.** Multiple anchors may ladder to the same item; merge into one carrying all contributing anchors. Do not emit one item per sentence. The coverage gate (Q7) asks for ≥1 candidate per source, **not** exhaustion of every sentence.

---

## Provenance markers

| Marker | Used in artefact section | Payload | Meaning |
|---|---|---|---|
| `[SRC: <filename>]` | Explicit item card, org-entity source, inferred-item **anchor**, why-chain rung, tension evidence | basename incl. extension, matching a manifest row's `filename` field | The cited item / entity / anchor / evidence is anchored to this manifest source; the phrase is verbatim or a minimally rephrased lift (or, for `Native-multimodal` / `Vector-renderable`, from the frozen textual description the input-handler prepared). |
| `[AI-SUGGESTED: AI-NN \| blocking\|non-blocking]` | Inferred item card | `AI-NN` local id + blocking flag | The item was **inferred**, not stated. Always co-present with a named technique and ≥1 anchor `[SRC: <filename>]`. The blocking flag drives downstream resolver treatment. |
| `(no-target-in-inputs)` | Objective card | (literal string) | An Objective has no anchorable measurable target/deadline in input prose; carries a best-effort intent phrase plus the marker. |
| `irrelevant-to-business-context` | Diagnostics > Source roster | (literal string + one-line reason) | A consumed manifest row yielded no business-context candidate. Surfaces silent skips, mirroring OOUX Gate 8 / User Goal Analysis G7. |
| `deferred-to-user-goal-analysis` | Diagnostics > boundary-audit log | (literal text + reason + `[SRC]`) | A statement that is an actor/end-user goal (Cooper sense), ejected by D0 / Q6 and **routed** to the sibling method rather than misclassified as a Business Goal. |
| `no-vision-stated-in-inputs` | Diagnostics / Goals section | (literal string) | No BMM Vision was explicitly stated; the hierarchy has no apex Vision node. An honest absence — a Vision is never inferred. |

**No further marker.** Every item carries exactly one provenance shape (`[SRC]` for explicit, `[AI-SUGGESTED: AI-NN | …]` + anchor + technique for inferred). No unmarked item. `[AI-SUGGESTED]` is used **only** for anchored inference and **never** for an item with no source anchor — honouring the framework-wide `feedback_ai_suggested_invariant` (never widen the marker into *anchorless* authoring).

**Confidence is secondary metadata, not a marker.** `HIGH|MEDIUM|LOW` confidence is recorded inside the inferred-item card and the JSON body for the reviewing consultant, but the canonical, downstream-consumed signal stays the `blocking|non-blocking` flag. **Default mapping:** `LOW → blocking` (least sure — must be confirmed before it seeds strategic framing); `HIGH|MEDIUM → non-blocking` (defensible enough to proceed as a suggestion). **Two named, auditable overrides of the default (and only these):** (a) any *root* Business Problem or *root* Business Goal that is inferred is `blocking` regardless of confidence — a wrong root misdirects the whole downstream spec; (b) any `abductive-best-explanation` item is always `blocking` — abduction is the least certain technique (asserting a cause from effects).

---

## Quality gates (7 hard gates)

Run at Pass 6 close, before render. Each operates on the in-memory state and captures `{gate_id, status: pass|fail, flagged_items: [...]}`. Failure handling follows the Revise / Override / Restart pattern below.

1. **Q1 Provenance.** Every item carries either an explicit `[SRC: <filename>]` OR an inferred `[AI-SUGGESTED: AI-NN | blocking|non-blocking]` co-present with a named technique and ≥1 anchor `[SRC]`. No unmarked item. Flag offenders by id.
2. **Q2 Anti-confabulation** *(load-bearing).* Every inferred item has ≥1 source anchor and exactly one technique from the closed set. An anchorless inferred item, or one citing a technique not in the set, fails. Flag offenders + the missing element.
3. **Q3 Classification correctness.** Every item sits in exactly one bucket per the decision tree; no item is double-booked across buckets; D0–D4 exclusivity holds. Flag offenders.
4. **Q4 Causal-chain integrity.** (a) Each Need links to ≥1 Business Problem or opportunity. (b) Each Goal links to ≥1 Need. (c) Each Objective is the child of exactly one Goal. (d) Each problem-driven Need has ≥1 Business Problem; each opportunity-driven Need has **none** (the §1.2 asymmetry). No orphan, no cycle. Flag offenders + the missing link.
5. **Q5 Well-formedness.** (a) Every Business Goal is **qualitative** — no "shall", no UI/tech token, no bare-number-as-goal (not a smuggled requirement). (b) Every Objective is **SMART** or carries `(no-target-in-inputs)`. (c) Every Problem Statement is **solution-neutral + human-centered** (POV+HMW, names an affected party, no solution token) **and** derived from a problem/opportunity. (d) No root Goal is a universal platitude. Flag offenders.
6. **Q6 Enterprise-scope (boundary vs user-goal-analysis)** *(load-bearing).* No item is an actor/end-user goal (Cooper task/life/experience); every item names an **organisational** subject. Actor-goal material appears only in the Diagnostics `deferred-to-user-goal-analysis` log. Forbidden-subject heuristic: an item whose subject is a single named persona performing a desk task fails. Flag offenders. *(Validated at both ends: D0 ejects actor goals before classification; Q6 re-verifies none leaked through inference — the realistic failure is a `bmm-laddering` climb that accidentally lands on an actor goal.)*
7. **Q7 Coverage.** Every consumed manifest row contributes ≥1 candidate (item or inference anchor) OR is marked `irrelevant-to-business-context` with a one-line reason. Surfaces silent skips the synthesised `requirements.md` would have hidden. Flag uncovered rows.

### Failure handling (Revise / Override / Restart)

On any hard-gate failure: do **not** write the artefact. Surface `AskUserQuestion` with three options:

1. `Revise — exit so the consultant can enrich input/ and re-invoke /analyse-inputs (Recommended)`
2. `Override — proceed and write a known-defective report (Run-history bullet records every violation)`
3. `Restart — re-run from Pass 1 with a fresh manifest pass`

On **Revise**: hand back with a `failed-handback` state. On **Override**: record each failing gate (+ flagged items) in the Run-history bullet; proceed to render. On **Restart**: re-enter Pass 1. Cap at three fail-Restart cycles; on the fourth, force Revise.

---

## Source-of-truth hierarchy

The analyser reads exactly the files the manifest enumerates, plus the prior artefact (additive merge) and its own three asset files (character, reference, template). The `tier` field dictates the read path:

| Tier | Source location | Read mechanism |
|---|---|---|
| `Native-text` | `original_path` | `Read` directly as text |
| `Native-multimodal` | `converted_sibling` | `Read` the frozen textual description (do **not** re-interpret pixels) |
| `Vector-renderable` | `converted_sibling` | `Read` the frozen textual description (do **not** re-interpret pixels) |
| `Supported-via-MCP` | `converted_sibling` | `Read` the `.converted.md` (markitdown's output, produced by input-handler) |
| `Unsupported` | — | Skipped; recorded in Diagnostics > Source roster > Skipped |

The analyser **never** reads: any path under `requirements/` other than `requirements/source-manifest.json` (not `requirements.md`, not `requirements-draft.md`, not `consultant-answers.md`, not `draft-claims*.ndjson`); any path under `framework/state/`; any path under `framework/shared/` (RF-/GR- references are textual links, not file loads); other analyses' artefacts under `analyse-requirements/` or `analyse-inputs/<OTHER-METHOD>/` (**including `analyse-inputs/USER-GOAL-ANALYSIS/` — the enterprise-vs-actor boundary is enforced by classification discipline, not by reading the sibling's output**); any pattern-catalogue or design-system file.

---

## Anti-patterns

- **Inventing an item with no anchor.** The single worst failure mode. An inferred problem/need/goal with no source anchor is fabrication; it propagates into requirements strategic-framing seeds with no audit trail. If you cannot name the anchor + technique, the item does not exist. (Q2.)
- **Extracting an actor / end-user goal as a Business Goal.** The load-bearing scope error. An actor's task/life/experience goal (Cooper sense) is User Goal Analysis's lane; route it to `deferred-to-user-goal-analysis`, never classify it as a Business Goal. (D0 + Q6.)
- **Confusing the Business Problem Statement (#2) with the Problem Statement (#4).** #2 is a present-tense diagnosis of organisational dysfunction with a root-cause ladder; #4 is a forward-looking, solution-neutral POV+HMW brief derived from #2. Keep them in their separate sections.
- **Recording a solution as a problem/need/goal, or smuggling a solution into the Problem Statement.** Stated solutions are inference *anchors* only; the Problem Statement is a "how might we", never a "we will build". (Q5c.)
- **Proposing solutions or recommendations.** That is OPPORTUNITY-SOLUTION-TREES's job. BCD stops at problem→need→goal→problem-statement; it never authors "the system shall…" (that is `/requirements`).
- **Over-climbing to a platitude.** Stopping `bmm-laddering` at *"maximise shareholder value"* / bare *"grow revenue"* yields a vacuous goal. Stop at the first domain-specific end-state; never infer a Vision. (Vision-ceiling stop + Q5d.)
- **Descending below the organisational root cause.** Five-Whys stops at the first organisationally-actionable cause; never blame an individual or descend into desk-task mechanics. (Root-cause floor stop + Q6.)
- **Inventing a Business Problem under an opportunity-driven Need.** An opportunity has no dysfunction beneath it; leave the problem slot empty. (Q4d.)
- **Padding the report.** A thin brief yields a thin, honest report (sparse cards, `(no-target-in-inputs)`, `no-vision-stated-in-inputs`, opportunity-needs with no problem). Sparsity is a signal, not a defect.
- **Collapsing passes.** Do not harvest, infer, classify, and chain in one sweep. Pass-by-pass structure is what makes the report reviewable.
- **Resolving tensions.** Surface goal/need tensions with `[SRC]` evidence; do not pick a winner. Resolution is a consultant trade-off (often deferred to `/requirements`).
- **Reading `requirements/requirements.md`, `framework/state/`, `framework/shared/`, or other analyses' artefacts** (including the User Goal Analysis output). The source contract is `requirements/source-manifest.json` + the per-tier rows.
- **Re-invoking `markitdown-mcp`.** Conversions are the input-handler's job; the manifest's `converted_sibling` path is the contract.
- **Bundling external JS / CSS / Mermaid.** The artefact is self-contained, dependency-free HTML. No `<script>`, no external links, no font URLs, no Mermaid — the template's inlined `<style>`, the CSS-only causal-chain grid, and the CSS-only AND/OR tree are the only rendering machinery.

---

## Re-run semantics

- The cursor (`manifest_fingerprint`, `run_count`) lives in the artefact's HTML-comment header: `<!-- bcd-meta: manifest_fingerprint=…, run_count=N -->`. No state file under `framework/state/`.
- On re-run, the analyser compares the current manifest fingerprint to the prior cursor:
  - **No change** → additive widening; only items from new or changed manifest rows are added (into the matching chain / hierarchy branch, or as new nodes).
  - **Change** → drift prompt: `append-new-items-only` (default; preserves prior cards, the causal chain, and the goal hierarchy verbatim, appends new), `re-extract-everything` (re-runs Passes 1–6 from scratch; the chain and hierarchy are rebuilt; items that no longer survive are dropped with a Run-history note), or `abort`.
- `AI-NN` ids are stable across additive runs: existing inferred items keep their id; new inferred items continue the numbering. On `re-extract-everything`, ids are re-minted from `AI-01`.

---

## JSON body-block schema (the re-ingestion contract)

Emitted into `<pre><code class="language-json" id="bcd-body">`. Survives markitdown HTML→MD as a fenced code block. `src` is `[]` for inferred items (their citation lives under `inference.anchor_src`). `causal_links` is the explicit edge set so `/requirements` need not re-derive the chain. Shape:

```json
{
  "domain": "string",
  "manifest_fingerprint": "sha256",
  "run_count": 1,
  "organisation": [
    { "id": "O-01", "name": "Procurement BU", "kind": "business-unit", "src": ["brief.docx"] }
  ],
  "business_problems": [
    { "id": "BP-01", "symptom": "Orders ship late",
      "root_cause": "No real-time cross-warehouse stock visibility",
      "why_chain": ["orders ship late", "pickers chase stock by phone", "stock counts are batch-nightly", "no real-time visibility"],
      "provenance": "explicit", "src": ["ops-review.pdf"], "inference": null,
      "confidence": "HIGH", "feeds_needs": ["BN-01"] }
  ],
  "business_needs": [
    { "id": "BN-01", "statement": "Close the gap between batch-nightly and real-time stock accuracy so fulfilment can scale.",
      "driver": "problem-driven", "from_problems": ["BP-01"], "from_opportunities": [],
      "provenance": "explicit", "src": ["brief.docx"], "inference": null,
      "confidence": "HIGH", "serves_goals": ["BG-01"] }
  ],
  "business_goals": [
    { "id": "BG-01", "statement": "Become the most reliable next-day supplier in the region.",
      "bmm_tier": "goal", "qualitative": true, "from_needs": ["BN-01"],
      "parent": null, "refinement": "AND",
      "provenance": "explicit", "src": ["brief.docx"], "inference": null, "confidence": "HIGH" }
  ],
  "business_objectives": [
    { "id": "OBJ-01", "statement": "Cut late-shipment rate from 9% to under 2% by end of FY27.",
      "smart": true, "target": "under 2% by end FY27", "parent_goal": "BG-01",
      "provenance": "explicit", "src": ["brief.docx"], "inference": null, "confidence": "HIGH" }
  ],
  "problem_statements": [
    { "id": "PS-01",
      "pov": "Fulfilment leads need stock truth at pick time because guesswork is the late-shipment driver.",
      "hmw": "How might we give fulfilment real-time stock truth so that next-day reliability holds at scale?",
      "affected_party": "Fulfilment leads", "solution_neutral": true,
      "derived_from": { "problems": ["BP-01"], "opportunities": [] }, "serves_goal": "BG-01",
      "provenance": "inferred", "src": [],
      "inference": { "technique": "pov-hmw-reframe", "anchor_text": "orders ship late; pickers chase stock by phone",
        "anchor_src": ["ops-review.pdf"], "ai_id": "AI-02", "blocking": false },
      "confidence": "MEDIUM" }
  ],
  "causal_links": [
    { "from": "BP-01", "to": "BN-01", "type": "problem->need" },
    { "from": "BN-01", "to": "BG-01", "type": "need->goal" },
    { "from": "BG-01", "to": "OBJ-01", "type": "goal->objective" },
    { "from": "BP-01", "to": "PS-01", "type": "problem->problem-statement" }
  ],
  "tensions": [
    { "between": ["BG-01", "BG-03"], "note": "next-day reliability investment pulls against the cost-reduction goal", "src": ["brief.docx", "finance-memo.pdf"] }
  ],
  "deferred_to_user_goal_analysis": [
    { "text": "buyers want to find a supplier in under a minute", "reason": "actor task goal (Cooper end goal) — user-goal-analysis lane", "src": ["interview.md"] }
  ]
}
```

`refinement` is `"AND"` / `"OR"` on a Goal node that has children, else `null`. `parent` is the parent Goal id, or `null` for a root / the Vision. `bmm_tier ∈ {vision, goal, objective}`.

---

## Downstream usage — `/requirements` round-trip

The Business Context Definition report is **re-ingestible by `/requirements`** as a fresh source. The contract (consultant-driven, not automated):

1. Consultant copies `analyse-inputs/BUSINESS-CONTEXT-DEFINITION/business-context-definition.html` into `input/`.
2. Consultant re-invokes `/requirements` (or `/analyse-inputs`, `/review-inputs`, `/generate-prd`).
3. The shared `framework/agents/input-handler.md` detects the new file, surfaces the manifest-refresh prompt, classifies it via `framework/skills/classify-input-tier.md` as `Native-text` (HTML passes the UTF-8 / printable-ratio sniff), and adds it as a manifest row.
4. The `/requirements` drafter reads the report:
   - **Explicit Goals / Objectives / Needs** (`[SRC]`) seed the **strategic framing** — the business-context / objectives front-matter that justifies *why* each requirement exists. The `causal_links` seed traceability (requirement → goal → need → problem).
   - **Problem Statements (#4)** seed the scope / solution-exploration framing.
   - **Inferred items** (`[AI-SUGGESTED: AI-NN | blocking|non-blocking]`) surface to the **resolver as `AI-NNN` questions in the existing grammar**. `blocking: true` items (inferred root causes, inferred root goals, abductive explanations) become **mandatory confirmations** the consultant accepts/rejects before they can frame a requirement; `blocking: false` items become non-blocking suggestions. This is the safety loop: **AI inference at analyse time → consultant validation at requirements time.** It reuses the existing `AI-NNN` namespace and blocking grammar — no new machinery.

BCD **stops at the requirement boundary** — it owns problem→need→goal→problem-statement and never authors "the system shall…". The Problem Statement (#4) is the explicit handoff token: the most-downstream BCD artefact, the most-upstream `/requirements` input.

The `framework/skills/map-business-context-definition-from-inputs-to-ui.md` skill (stub on first ship) sketches the broader business-context-to-design mapping for future downstream design-spec authors. It is **not** invoked by `/analyse-inputs` — registry metadata only.

---

## Stop-condition

The analysis is complete when:

- At least one of the four artefact collections is non-empty (or the consultant Override'd an empty run with a recorded reason in Run-history).
- All 7 hard gates pass, or the consultant chose Override and the failures are recorded in Diagnostics.
- `analyse-inputs/BUSINESS-CONTEXT-DEFINITION/business-context-definition.html` has been written and `verify-artifact-write` returned `pass`.
- The consultant chose Accept in the Step 12 handback loop.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/business-context-definition-inputs-analysis.md` — analytical, citation-bound, inference-disciplined, anti-confabulation, enterprise-altitude, additive. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact is human-read (and re-ingested by `/requirements`), so the analyser also follows `framework/shared/output-readability.md`: it writes the "In plain terms" lead (`{{PLAIN_SUMMARY}}`), glosses methodology jargon (business goal, stakeholder, context boundary/scope, success metric/objective, constraint, BMM Ends, KAOS AND/OR, causal chain) at first use in human-readable prose, leaves client domain vocabulary unglossed (GLOSSARY territory), and keeps every `[SRC: <filename>]` marker. The plain-language layer is confined to the lead and first-use glosses; the cards, causal-chain map, goal hierarchy, JSON body, and diagnostics keep their concrete, telegraphic discipline.

---

## Bibliography (for defensibility — cited in the Overview footer credit, not loaded at runtime)

- Object Management Group, *Business Motivation Model (BMM)*, v1.3 (OMG, 2015) — Ends (Vision / Goal / Objective) vs Means (Mission / Strategy / Tactic); the Goal-vs-Objective distinction.
- International Institute of Business Analysis, *A Guide to the Business Analysis Body of Knowledge (BABOK Guide)*, v3 (IIBA, 2015) — Define Business Need; Business Goals & Objectives; Root Cause Analysis (10.40); underlying-cause-vs-symptom.
- Donald C. Gause & Gerald M. Weinberg, *Are Your Lights On? How to Figure Out What the Problem Really Is* (Dorset House, 1990) — a problem is the difference between perceived and desired; "whose problem is it?".
- Sakichi Toyoda / Toyota Production System — the Five Whys root-cause technique.
- Axel van Lamsweerde, "Goal-Oriented Requirements Engineering: A Guided Tour," *RE'01* (2001) — KAOS, AND/OR goal refinement, obstacles, hard vs soft goals.
- IDEO / Stanford d.school — Design Thinking; the Point-of-View (POV) statement and the "How Might We" reframing.
- ISO/IEC/IEEE 29148:2018 — requirements well-formedness criteria; the SMART lens for objectives.
- Eric Yu, "Towards Modelling and Reasoning Support for Early-Phase Requirements Engineering," *RE'97* — actors, goals, and dependencies (the intentional-modelling backdrop the enterprise tier inherits).
