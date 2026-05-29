<!-- ROLE: asset (analysis reference). Methodology definition for the User Goal Analysis input-analyser. Industry framing: a pragmatic synthesis of Goal-Oriented Requirements Engineering (van Lamsweerde / KAOS goal refinement; Yu / i* actor dependencies) + Cooper's three goal types + the hard/soft (functional/quality) goal split (Chung et al. NFR framework) + means-end laddering (Gutman) and Five-Whys for inferring unstated goals, adapted for raw consultant inputs enumerated via `requirements/source-manifest.json`. -->

# User Goal Analysis reference (input-analysis variant)

> **Method:** Walk every consumable source enumerated in `requirements/source-manifest.json`; inventory the actors who hold goals (Pass 1); harvest every **explicitly stated** goal from input prose, deck text, and transcribed visual notes (Pass 2); derive **inferred** goals by laddering UP from stated solutions / pain-points / quality-adjectives via one named technique — anchored to a source, never from world knowledge (Pass 3); classify each goal by Cooper type + hardness + actor (Pass 4); arrange goals into a KAOS-style AND/OR refinement hierarchy and attach them to actors (Pass 5); write canonical *"`<Actor>` wants to `<outcome>` so that `<higher-level goal>`."* statements, run the SMART-ish quality gate, and surface goal conflicts (Pass 6). Every **explicit** goal carries `[SRC: <filename>]`. Every **inferred** goal carries `[AI-SUGGESTED: AI-NN | blocking|non-blocking]` PLUS the anchor `[SRC: <filename>]` it was laddered from PLUS the named technique used. Hard goals without an anchorable measure carry `(no-metric-in-inputs)`; soft goals without a threshold carry `(no-satisficing-criterion-in-inputs)`. Across re-runs the artefact is **additive**: prior goal cards, the hierarchy, and the actor map are preserved; new manifest content extends them.

**Output file:** `analyse-inputs/USER-GOAL-ANALYSIS/user-goal-analysis.html` — a self-contained, readability-optimised HTML goal register using `framework/assets/analyses-inputs/template-user-goal-analysis.html` as scaffold.

**Analyser agent:** `framework/agents/analyses-inputs/user-goal-analysis-analyser.md`

**Character:** `framework/assets/characters/user-goal-analysis-inputs-analysis.md`

**No `/analyse-requirement` sibling.** Unlike JTBD or OOUX, User Goal Analysis ships only on the inputs side. The synthesised `requirements/requirements.md` has already normalised consultant phrasing into *"the system shall …"* clauses — by then the *latent* goals the inputs implied have been collapsed into features. Surfacing goals **before** synthesis (and feeding the register back into `/requirements`) is the entire value; a requirements-doc-lensing variant would surface only the goals the normaliser preserved, which is the gap this method exists to close.

---

## Industry framing — a pragmatic GORE core adapted for raw consultant inputs

User Goal Analysis is **not** a single named author's framework; it is a deliberate synthesis of the most load-bearing ideas across the user-goal literature, kept lean enough to execute by carefully reading documents. The chosen core:

| Building block | Source | What it contributes |
|---|---|---|
| **Three goal types** — life / end / experience | Alan Cooper, *About Face* (Goal-Directed Design) | The primary classification axis. Life goals = who the actor wants to be (identity/aspiration); end goals = what they want to accomplish; experience goals = how they want to feel. They are three complementary dimensions, **not** a hierarchy. |
| **Hard vs soft goals** | Chung et al., NFR framework; van Lamsweerde | The secondary classification axis. Hard goals have a clear satisfaction test (*"reconcile within one business day"*); soft goals are *satisficed* to a degree (*"feel confident the data is current"*, *"keep the workflow simple"*). |
| **AND/OR goal refinement** | van Lamsweerde, KAOS | The hierarchy spine. A goal refines into sub-goals: **AND** (all sub-goals required) or **OR** (alternative strategies). Refinement stops at goals concrete enough to operationalise as a requirement. |
| **Actor↔goal dependency (lite)** | Eric Yu, i* | The actor map. Each goal belongs to ≥1 actor; some goals are *dependencies* one actor relies on another (or the system) to satisfy. Full i* SD/SR diagrams are **out of scope** — this is a who-holds-what / who-depends-on-whom table, not a strategic-rationale model. |
| **Means-end laddering + Five-Whys** | Gutman (means-end chains); Toyota/Lean (Five-Whys) | The **inference engine** for unstated goals. Take a stated solution/feature/pain-point and ask "why does that matter?" repeatedly to climb to the underlying goal. |
| **Solution-reframe ("faster horse")** | Christensen/Ulwick lineage; classic Ford apocrypha | The discipline that separates a goal from a stated solution. *"Implement a REST API"* is not a goal; the goal is *"let third parties pull our data without manual export."* |
| **SMART-ish quality + canonical statement form** | Locke & Latham (goal-setting theory) | The quality gate and the statement template *"`<Actor>` wants to `<outcome>` so that `<higher-level goal>`."* |

This analyser sits in a **bounded-inference** camp, not the pure-extraction camp that JTBD occupies. Inference is the explicit point of the method — but it is **anchored**: every inferred goal is a transformation of cited input evidence via a named, reproducible technique, never an author's free-floating idea. (See the precedent already set by `task-analysis-analyser` and `swim-lane-process-mapping-analyser`, which permit `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` inference under anti-confabulation rules, and `ooux-analyser`'s `inferred-from-<filename>` marker.)

### Why apply User Goal Analysis to raw inputs (and how it differs from its neighbours)

| Lens | Methodology | Question answered | Operates on |
|---|---|---|---|
| Cross-cutting pattern recognition | thematic-analysis | What recurring patterns do the inputs carry? | raw `input/` |
| Outcome-tree discovery | opportunity-solution-trees | What desired outcomes do the inputs name and which **solutions** ladder down from them? | raw `input/` |
| Current-state workflow mapping | journey-mapping | What is the as-is user workflow? | raw `input/` |
| Hierarchical task decomposition | task-analysis (HTA) | How does a **given** goal decompose DOWN into sub-goals + operations? | raw `input/` |
| Jobs × situations × outcomes × forces | jtbd | What jobs are users hiring the product to do? (extraction only) | raw `input/` |
| **Goals — stated + inferred — classified + refined** | **user-goal-analysis** | **What do the actors actually want to achieve (explicitly AND latently), of what type, in what hierarchy?** | **raw `input/`** |

The scope boundaries are **hard** — they are enforced as analyser anti-patterns and as the character's discipline:

- **vs JTBD.** A job is *situational progress* (*"When invoices arrive mid-month, I want to reconcile against the PO…"*). A goal is the *desired end-state or aspiration* behind it (*"keep the ledger trustworthy"*). User Goal Analysis **never** writes a `When … I want … so I can …` job statement and **never** scores push/pull/anxiety/habit. It classifies by Cooper type and builds a hierarchy — JTBD does neither.
- **vs TASK-ANALYSIS (HTA).** HTA takes a goal as **given** and decomposes it *downward* into sub-goals → operations → keystrokes, with Plans. User Goal Analysis runs *upstream* of HTA: it **discovers** the goals (explicit + inferred) and refines them only as far as the goal level. It **never** descends into operations, keystrokes, or Plans. The handoff is clean: User Goal Analysis output is a legitimate *input* to a subsequent HTA.
- **vs OPPORTUNITY-SOLUTION-TREES.** OST runs outcome → opportunities → **solutions** → assumption-tests. User Goal Analysis **never proposes a solution** — a stated solution is only ever recorded as the *anchor* of an inferred goal, never as a goal or a recommendation.
- **vs FIVE-WHYS (`/analyse-requirement`).** Five-Whys produces a root-**cause** chain for a problem. User Goal Analysis *uses* the why-laddering motion as one inference technique, but its output is a classified goal register + refinement hierarchy, not a cause chain.

### Why this analyser uses HTML, not Markdown

- **Readability is the deliverable.** The consultant explicitly wants a report optimised for reading: grouped goal cards, a visual refinement tree, an actor map, a conflicts table, with explicit-vs-inferred goals visually distinguished at a glance. A self-contained HTML page renders that cleanly in any browser with no tooling.
- **Inferred goals must be obvious.** Inference is the method's signature output and its main risk surface; the template gives inferred goals a distinct `.ai-suggested` visual treatment (badge + technique + anchor) so a reviewing consultant can audit them immediately.
- **Dependency-free.** The hierarchy renders as a CSS-only nested tree — **no Mermaid, no `mmdc`, no `RF-07` dependency, no CDN, no `<script>`**. The page opens offline and prints cleanly.
- **Re-ingestibility intact.** HTML still classifies as `Native-text` per `framework/skills/classify-input-tier.md`; the embedded JSON body block and the nested-list hierarchy survive a markitdown HTML→MD round-trip as a fenced code block and indented lists respectively, so a downstream `/requirements` run consumes the full goal model.

---

## Output structure

The artefact has a fixed top-to-bottom shape (rendered by the template; placeholders are substituted by the analyser):

1. **Overview block.** Title, subtitle, meta-grid (Domain, Generated timestamp, Manifest fingerprint, Sources consumed, Tier breakdown, Total goals, Explicit / Inferred counts, Life / End / Experience counts, Hard / Soft counts, Conflicts count).
2. **`user-goal-meta` HTML comment** carrying the additive-merge cursor (`manifest_fingerprint`, `run_count`).
3. **TOC** — static top-level anchors (Overview, Goal hierarchy, Goal register, Actor map, Conflicts, Use in /requirements, Diagnostics).
4. **Goal hierarchy** (`<section id="hierarchy">`) — **the diagram, placed first among the content sections** (diagram-first ordering, mirroring journey-mapping / affinity-mapping: compact overview, then the prominent diagram, then the rest). A CSS-only nested `<ul>` tree of the KAOS AND/OR refinement; each branch node labelled `AND` or `OR`; leaves are operationalisable goals; inferred nodes marked inline. No JS, no Mermaid.
5. **Goal register** (`<section id="register">`). Goal cards grouped by Cooper type (Life / End / Experience sub-sections). Each `<article class="goal-card">`:
   - Cooper-type badge (Life / End / Experience) + hardness pill (Hard / Soft) + Goal ID (`G-NN`).
   - Provenance badge: `Explicit` (green) or `Inferred` (amber `.ai-suggested`). Inferred cards also show the **technique** chip and the **anchor** `[SRC: <filename>]` they laddered from + the `AI-NN | blocking|non-blocking` flag.
   - The canonical goal statement (*"`<Actor>` wants to `<outcome>` so that `<higher-level goal>`."*).
   - Actor chips (one per holding actor, `A-NN`).
   - Criterion line: a success measure (hard) or satisficing threshold (soft), or the `(no-metric-in-inputs)` / `(no-satisficing-criterion-in-inputs)` marker.
6. **Actor map** (`<section id="actor-map">`). A table: actor `A-NN` × the goals they hold and the goals they depend on another actor/the system to satisfy.
7. **Conflicts** (`<section id="conflicts">`). A table of goal pairs that pull against each other (e.g. a security goal vs an ease-of-access goal), each with a one-line tension note and `[SRC: <filename>]` on the evidence. Empty is a legitimate state (rendered as "no goal conflicts surfaced in the consumed inputs").
8. **JSON body block** (`<section id="body">` → `<pre><code class="language-json" id="user-goal-analysis-body">`). The machine-readable re-ingestion contract per the JSON SCHEMA below.
9. **Round-trip footer** (`<section id="round-trip">`). Static paragraph telling the consultant how to feed the register into a subsequent `/requirements` run.
10. **Diagnostics** (`<details id="diagnostics">`, collapsed). Manifest fingerprint, source roster (Consumed + Skipped tables), 7 gate results, provenance counts (explicit / inferred per source), inference-technique breakdown, criterion counts, flagged low-confidence inferred goals, run history.

---

## The six-pass process

Six passes, executed in order. The analyser does not skip or collapse passes — each pass feeds the next, and pass-by-pass structure is what makes the goal model auditable. The six passes map to twelve workflow steps in the analyser agent (Activate / Read manifest / Detect prior artefact / Passes 1–6 / Validate / Write / Handback).

### Pass 1 — Actor inventory

Read every consumable manifest row in full per its tier (`Native-text` / `Native-multimodal` → `original_path`; `Supported-via-MCP` → `converted_sibling`; `Unsupported` → skipped + recorded). Lift every actor / role / persona that **holds a goal** — verbatim or near-verbatim from input prose, deck text, screenshot labels, or transcribed visual notes. Each actor carries:

```
{ actor_id, name, source_filenames: [<filename>], kind }   // kind ∈ {role, system, external-party}
```

Actor sources mirror JTBD's: role titles in prose (*"the Procurement Manager"*), first-person persona shorthand (*"as a buyer, I…"*), or a descriptor fallback (*"the approver mentioned in `brief.docx` para 12"*). Every actor is `[SRC: <filename>]`-cited. The system-under-design and external parties (regulators, suppliers) are actors too when goals depend on them.

State the per-source actor counts aloud.

### Pass 2 — Explicit goal harvest (broad pass)

Scan every consumed source for **outcome language** and lift each stated goal verbatim or near-verbatim. Signal vocabulary:

- Outcome verbs: *enable, allow, let, improve, reduce, increase, ensure, avoid, prevent, speed up, simplify, support.*
- Rationale connectives: *so that, in order to, because, to achieve, the point is to.*
- Aspiration/strategy markers: *vision, mission, our goal is, we want, the objective, success looks like.*
- Pain language that names the desired relief: *currently we can't…, the problem is…, today it takes N hours…* (the relief is the goal; the pain is its evidence).

Each explicit goal carries:

```
{ goal_id, raw_text, source_filenames: [<filename>], provenance: "explicit" }
```

Capture broadly here; classification, statement-writing, and de-duplication happen in later passes. State the post-harvest count aloud (per source).

### Pass 3 — Inferred goal derivation (anchored)

This is the method's signature pass and its primary risk surface. For each **stated solution, feature, pain-point, or quality-adjective** found in the sources that does **not** already have an explicit goal above it, climb to the underlying goal via exactly **one** named technique (closed set below). The inferred goal carries:

```
{
  goal_id,
  statement,                       // the inferred goal, written as an outcome (never a solution)
  provenance: "inferred",
  ai_id,                           // AI-NN, zero-padded, assigned in discovery order
  blocking,                        // true|false — see blocking semantics below
  inference: {
    technique,                     // one of the 5 named techniques
    anchor_text,                   // the verbatim stated solution/pain/adjective it laddered from
    anchor_source_filenames: [<filename>]   // ≥1 — the [SRC] anchor; an inferred goal with no anchor is FORBIDDEN
  }
}
```

**Anti-confabulation rule (load-bearing — Gate G2).** No inferred goal may exist without ≥1 source anchor and exactly one named technique. A goal "the actor probably also wants…" with no anchor in any consumed source is **forbidden** — it is invention, not inference. This mirrors `task-analysis-analyser`'s "inferred terminals forbidden" (Diaper & Stanton anti-confabulation rule).

**Blocking vs non-blocking.** `blocking: true` marks an inferred goal that is **load-bearing** for the spec — typically a high-level / root goal that, if wrong, would misdirect requirements (the consultant MUST confirm it before it seeds a requirement). `blocking: false` marks a supporting / leaf inferred goal that can proceed as an AI-suggested seed for the consultant to accept or trim. This flag is what the downstream `/requirements` resolver reads to decide which inferred goals become mandatory Q&A items.

State the inference shape aloud (count per technique).

### Pass 4 — Classification

For each goal (explicit + inferred), assign:

- **Cooper type** ∈ {life, end, experience}. End goals dominate data-management inputs; life and experience goals are often sparse — that sparsity is a **signal**, surfaced honestly (`no-life-signal-in-inputs` / `no-experience-signal-in-inputs` absence markers in Diagnostics), never padded with invented goals.
- **Hardness** ∈ {hard, soft}. Hard = clear satisfaction test; soft = satisficed to a degree.
- **Actors** — ≥1 actor `A-NN` from Pass 1 who holds this goal.

State the classification shape aloud (counts by type and hardness).

### Pass 5 — Hierarchy + actor↔goal map

**Build the refinement hierarchy (KAOS AND/OR).** Arrange goals from the most abstract (root) down to operationalisable leaves. Each non-leaf goal refines into children via **AND** (every child required to satisfy the parent) or **OR** (children are alternative strategies). Refinement stops when a goal is concrete enough that a single requirement could operationalise it. Every goal appears exactly once in the tree (Gate G5). Inferred goals participate in the tree like any other, retaining their `.ai-suggested` marking.

**Build the actor map.** For each actor, list the goals they **hold** and the goals they **depend on** another actor or the system-under-design to satisfy (i*-lite dependency). This surfaces cross-actor reliance and is the seam where conflicts often live.

State the hierarchy shape aloud (root count, max depth, AND/OR node counts).

### Pass 6 — Quality gate, conflicts, and statements

**Write the canonical statement** for every goal: *"`<Actor>` wants to `<outcome>` so that `<higher-level goal>`."* For a root goal, the *so that* clause names the strategic value; for a leaf, it names its parent goal. The outcome clause is solution-free.

**Run the SMART-ish quality check** (this is the input to the hard gates, not a separate gate): Specific (not vague — *"improve UX"* fails), Measurable-or-satisficeable (hard → a measure; soft → a satisficing threshold or the honest marker), verb+object outcome form, Relevant (traces up to a parent or strategic value), not solution-biased (Gate G3).

**Surface goal conflicts.** Identify pairs of goals that pull against each other — typically a soft goal vs another soft goal, or a soft goal vs a hard goal (e.g. *"keep data access frictionless"* vs *"enforce per-record authorisation"*). Each conflict carries a one-line tension note and `[SRC: <filename>]` on the evidence that both goals are real. Conflicts are **surfaced, never resolved** — resolution is the consultant's call (often a `/requirements` trade-off decision).

State the final shape aloud (statements written, conflicts surfaced).

---

## Named inference techniques (Pass 3 closed set)

Each inferred goal records **exactly one** technique. Adding a technique means appending to this list (never renumbering):

| Technique | Motion | Example (anchor → inferred goal) |
|---|---|---|
| `laddering` | Means-end: "why does this attribute/feature matter?" climbed one or more rungs to the value/outcome. | *"real-time dashboard"* → wants to **act on current status without waiting for a report** so that decisions use fresh data. |
| `five-whys` | Repeated "why is this a problem?" on a pain-point until a domain goal surfaces. | *"users are locked out after password expiry"* → wants to **stay continuously able to do their work** so that service to customers is not interrupted. |
| `solution-reframe` | Strip the technology/UI prescription; recover the outcome it serves. | *"build a mobile app"* → wants to **complete the task away from a desk** so that fieldwork isn't blocked. |
| `obstacle-analysis` | A named blocker/risk implies a goal to remove or contain it (KAOS obstacles, lite). | *"we can't afford to break the audit trail during migration"* → wants to **preserve an unbroken audit trail through any change** so that compliance holds. |
| `softgoal-from-quality-adjective` | A quality adjective (*fast, intuitive, reliable, secure, simple*) names a soft goal; attach a satisficing criterion if the inputs give one, else the honest marker. | *"the screen must feel fast"* → soft goal: wants to **perceive the system as responsive** (satisficing: *"sub-2s on common actions"* if stated, else `(no-satisficing-criterion-in-inputs)`). |

**Laddering stop-rule (anti-vacuity).** Climb only as far as the **first domain-specific goal**. A rung that produces a universal platitude (*"be successful"*, *"be happy"*, *"make money"*, *"save time"* with no domain object) is **over-climbed** — stop at the rung below it. Root goals must remain anchored to the project's domain; Gate G3 rejects platitude roots.

**Near-duplicate merge.** Multiple anchors can ladder to the same goal. Merge them into one inferred goal carrying all contributing anchors; do not emit one inferred goal per sentence. The coverage gate (G7) asks for ≥1 candidate per source, **not** exhaustion of every sentence.

---

## Provenance markers

| Marker | Used in artefact section | Payload | Meaning |
|---|---|---|---|
| `[SRC: <filename>]` | Explicit goal card, actor chip source, inferred-goal **anchor**, conflict evidence, criterion source | basename incl. extension, matching a manifest row's `filename` field | The cited goal / actor / anchor / evidence is anchored to this manifest source; the phrase is verbatim or a minimally rephrased lift (or, for `Native-multimodal`, from the transcribed visual notes captured at Pass 1). |
| `[AI-SUGGESTED: AI-NN \| blocking\|non-blocking]` | Inferred goal card | `AI-NN` local id + blocking flag | The goal was **inferred**, not stated. Always co-present with a named technique and ≥1 anchor `[SRC: <filename>]`. The blocking flag drives downstream resolver treatment. |
| `(no-metric-in-inputs)` | Criterion line on a **hard** goal | (literal string) | The hard goal has no anchorable success measure in input prose; carries a best-effort intent phrase plus the marker. |
| `(no-satisficing-criterion-in-inputs)` | Criterion line on a **soft** goal | (literal string) | The soft goal has no anchorable satisficing threshold in input prose. |
| `irrelevant-to-goals` | Diagnostics > Source roster | (literal string + one-line reason) | A consumed manifest row yielded no goal candidate (explicit or anchor). Surfaces silent skips, mirroring OOUX Gate 8. |
| `no-life-signal-in-inputs` / `no-experience-signal-in-inputs` | Diagnostics | (literal string) | A Cooper category has zero goals because the inputs carry no signal for it — an honest absence, never a prompt to invent. |

**No seventh marker.** Every goal carries exactly one provenance shape (`[SRC]` for explicit, `[AI-SUGGESTED: AI-NN | …]`+anchor for inferred). No unmarked goal. `[AI-SUGGESTED]` is used **only** for anchored inference and **never** for a goal with no source anchor.

---

## Quality gates (7 hard gates)

Run at Pass 6 close, before render. Each operates on the in-memory state. Failure handling follows the Revise / Override / Restart pattern below.

1. **G1 Provenance.** Every goal carries either an explicit `[SRC: <filename>]` OR an inferred `[AI-SUGGESTED: AI-NN | blocking|non-blocking]` co-present with a named technique and ≥1 anchor `[SRC]`. No unmarked goal. Flag offenders by `goal_id`.
2. **G2 Anti-confabulation** *(load-bearing).* Every inferred goal has ≥1 source anchor and exactly one technique from the closed set. An anchorless inferred goal, or one citing a technique not in the set, fails. Flag offenders + the missing element.
3. **G3 Solution-bias / anti-vacuity.** No goal statement names a UI affordance, technology, or product feature as the goal itself (forbidden tokens: `click`, `tap`, `button`, `dashboard`, `the … screen`, `API`, `mobile app`, `database`, and named features). No root goal is a universal platitude. Solution-framed text must appear as an inferred goal's *anchor*, never as the goal. Flag offenders.
4. **G4 Classification.** Every goal has a Cooper type ∈ {life, end, experience}, a hardness ∈ {hard, soft}, and ≥1 actor `A-NN` drawn from the Pass-1 inventory. Flag offenders.
5. **G5 Hierarchy integrity.** Every goal appears exactly once in the refinement tree; every non-leaf node is labelled `AND` or `OR` and has ≥2 children; every non-root goal has exactly one parent; no orphan and no cycle. Flag offenders.
6. **G6 Criterion.** Every hard goal carries a success measure or `(no-metric-in-inputs)`; every soft goal carries a satisficing threshold or `(no-satisficing-criterion-in-inputs)`. Silent criterionless goals break downstream acceptance. Flag offenders.
7. **G7 Coverage.** Every consumed manifest row contributes ≥1 goal candidate (explicit goal OR inference anchor) OR is marked `irrelevant-to-goals` with a one-line reason. Surfaces silent skips the synthesised `requirements.md` would have hidden. Flag uncovered rows.

### Failure handling (Revise / Override / Restart)

On any hard-gate failure: do **not** write the artefact. Surface `AskUserQuestion` with three options:

1. `Revise — exit so the consultant can enrich input/ and re-invoke /analyse-inputs (Recommended)`
2. `Override — proceed and write a known-defective register (Run-history bullet records every violation)`
3. `Restart — re-run from Pass 1 with a fresh manifest pass`

On **Revise**: hand back with a `failed-handback` state. On **Override**: record each failing gate in the Run-history bullet; proceed to render. On **Restart**: re-enter Pass 1. Cap at three fail-Restart cycles; on the fourth, force Revise.

---

## Source-of-truth hierarchy

The analyser reads exactly the files the manifest enumerates, plus the prior artefact (additive merge) and its own three asset files (character, reference, template). The `tier` field dictates the read path:

| Tier | Source location | Read mechanism |
|---|---|---|
| `Native-text` | `original_path` | `Read` directly as text |
| `Native-multimodal` | `original_path` | `Read` — vision surfaces image bytes; transcribe visible text/structure to a per-source notes buffer |
| `Supported-via-MCP` | `converted_sibling` | `Read` the `.converted.md` (markitdown's output, produced by input-handler) |
| `Unsupported` | — | Skipped; recorded in Diagnostics > Source roster > Skipped |

The analyser **never** reads: any path under `requirements/` other than `requirements/source-manifest.json` (not `requirements.md`, not `requirements-draft.md`, not `consultant-answers.md`, not `draft-claims*.ndjson`); any path under `framework/state/`; any path under `framework/shared/` (RF-/GR- references are textual links, not file loads); other analyses' artefacts under `analyse-requirements/` or `analyse-inputs/<OTHER-METHOD>/`; any pattern-catalogue or design-system file.

---

## Anti-patterns

- **Inventing a goal with no anchor.** The single worst failure mode. An inferred goal with no source anchor is fabrication; it propagates into requirements seeds with no audit trail. If you cannot name the anchor + technique, the goal does not exist. (G2.)
- **Recording a solution as a goal.** *"Use a Kanban board"*, *"add SSO"*, *"build a mobile app"* are solutions. Record them as inference *anchors* and ladder up; never enter them in the register as goals. (G3.)
- **Decomposing into tasks/operations.** That is TASK-ANALYSIS's job. Stop at the goal level; never write keystrokes, operations, or Plans. User Goal Analysis is upstream of HTA.
- **Writing job statements.** That is JTBD's job. Never write `When … I want … so I can …`; never score push/pull/anxiety/habit.
- **Proposing solutions.** That is OPPORTUNITY-SOLUTION-TREES's job. The register discovers goals; it makes no recommendation.
- **Over-climbing the ladder.** Stopping at *"be successful"* / *"save time"* produces a vacuous root. Stop at the first domain-specific rung. (Stop-rule + G3.)
- **Padding sparse Cooper categories.** If the inputs carry no life or experience goals, mark `no-life-signal-in-inputs` / `no-experience-signal-in-inputs`. Sparsity on data-management CRUD inputs is expected and is a signal, not a defect.
- **Collapsing passes.** Do not harvest, infer, classify, and refine in one sweep. Pass-by-pass structure is what makes the register reviewable.
- **Resolving conflicts.** Surface goal tensions; do not pick a winner. Resolution is a consultant trade-off decision (often deferred to `/requirements`).
- **Reading `requirements/requirements.md`.** The source contract is `requirements/source-manifest.json` + the per-tier rows. There is no requirements-doc sibling for this method.
- **Re-invoking `markitdown-mcp`.** Conversions are the input-handler's job; the manifest's `converted_sibling` path is the contract.
- **Bundling external JS / CSS / Mermaid.** The artefact is self-contained, dependency-free HTML. No `<script>`, no external links, no font URLs, no Mermaid — the template's inlined `<style>` and the CSS-only nested tree are the only rendering machinery.

---

## Re-run semantics

- The cursor (`manifest_fingerprint`, `run_count`) lives in the artefact's HTML-comment header: `<!-- user-goal-meta: manifest_fingerprint=…, run_count=N -->`. No state file under `framework/state/`.
- On re-run, the analyser compares the current manifest fingerprint to the prior cursor:
  - **No change** → additive widening; only goals from new or changed manifest rows are added (into the matching hierarchy branch / actor, or as new nodes).
  - **Change** → drift prompt: `append-new-goals-only` (default; preserves prior cards, hierarchy, and actor map verbatim, appends new), `re-extract-everything` (re-runs Passes 1–6 from scratch; the hierarchy is rebuilt; cards that no longer survive are dropped with a Run-history note), or `abort`.
- `AI-NN` ids are stable across additive runs: existing inferred goals keep their id; new inferred goals continue the numbering. On `re-extract-everything`, ids are re-minted from `AI-01`.

---

## JSON body-block schema (the re-ingestion contract)

Emitted into `<pre><code class="language-json" id="user-goal-analysis-body">`. Survives markitdown HTML→MD as a fenced code block. Shape:

```json
{
  "domain": "string",
  "manifest_fingerprint": "sha256",
  "run_count": 1,
  "actors": [
    { "id": "A-01", "name": "Procurement Manager", "kind": "role", "src": ["brief.docx"] }
  ],
  "goals": [
    {
      "id": "G-01",
      "statement": "The Procurement Manager wants to reconcile invoices within one business day so that payments clear on time.",
      "cooper_type": "end",
      "hardness": "hard",
      "actors": ["A-01"],
      "provenance": "explicit",
      "src": ["brief.docx"],
      "inference": null,
      "criterion": "within one business day",
      "parent": "G-00",
      "refinement": null
    },
    {
      "id": "G-05",
      "statement": "The Procurement Manager wants to act on current spend without waiting for a report so that decisions use fresh data.",
      "cooper_type": "end",
      "hardness": "soft",
      "actors": ["A-01"],
      "provenance": "inferred",
      "src": [],
      "inference": {
        "technique": "laddering",
        "anchor_text": "real-time dashboard",
        "anchor_src": ["ux-notes.md"],
        "ai_id": "AI-03",
        "blocking": false
      },
      "criterion": "(no-satisficing-criterion-in-inputs)",
      "parent": "G-02",
      "refinement": null
    }
  ],
  "conflicts": [
    { "between": ["G-04", "G-09"], "note": "frictionless access pulls against per-record authorisation", "src": ["brief.docx", "security-memo.pdf"] }
  ]
}
```

`refinement` is `"AND"` / `"OR"` on a node that has children, else `null`. `parent` is the parent `goal_id`, or `null` for a root. `src` is `[]` for inferred goals (their citation lives under `inference.anchor_src`).

---

## Downstream usage — `/requirements` round-trip

The User Goal Analysis register is **re-ingestible by `/requirements`** as a fresh source. The contract:

1. Consultant copies `analyse-inputs/USER-GOAL-ANALYSIS/user-goal-analysis.html` into `input/` (file copy; the orchestrator does not automate this).
2. Consultant re-invokes `/requirements` (or `/analyse-inputs`, `/review-inputs`, `/generate-prd`).
3. The shared `framework/agents/input-handler.md` detects the new file, surfaces the manifest-refresh prompt, classifies it via `framework/skills/classify-input-tier.md` as `Native-text` (HTML passes the UTF-8 / printable-ratio sniff), and adds it as a manifest row.
4. The `/requirements` drafter reads the register:
   - **Explicit goals** (`[SRC]`) seed `§4 User goals & stories` as user-story stacks — *"As a `<actor>` I want `<outcome>` so that `<higher-level goal>`"* — and the hierarchy seeds goal grouping.
   - **Inferred goals** (`[AI-SUGGESTED: AI-NN | blocking|non-blocking]`) surface to the **resolver as `AI-NNN` questions in the existing grammar**. `blocking: true` inferred goals become mandatory confirmation items (the consultant accepts or rejects each before it can seed a requirement); `blocking: false` ones become non-blocking suggestions. This is the safety loop: **AI inference at analyse time → consultant validation at requirements time.** It mirrors swim-lane's `consultant_follow_up: yes → resolver AI-NNN` pattern and reuses the existing `AI-NNN` namespace and blocking grammar — no new machinery.

This pathway is **consultant-driven**, not automated. Step 12's handback message tells the consultant about the round-trip; they decide whether to use the register as `/requirements` input or as a stand-alone discovery artefact.

The `framework/skills/map-user-goal-analysis-from-inputs-to-ui.md` skill (stub on framework first-ship) sketches the broader goal-to-pattern mapping for future downstream design-spec authors. It is **not** invoked by `/analyse-inputs` — registry metadata only.

---

## Stop-condition

The analysis is complete when:

- `final_goals` is non-empty (or the consultant Override'd a zero-goal run with a recorded reason in Run-history).
- All 7 hard gates pass, or the consultant chose Override and the failures are recorded in Diagnostics.
- `analyse-inputs/USER-GOAL-ANALYSIS/user-goal-analysis.html` has been written and `verify-artifact-write` returned `pass`.
- The consultant chose Accept in the Step 12 handback loop.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/user-goal-analysis-inputs-analysis.md` — analytical, citation-bound, inference-disciplined, anti-confabulation, additive. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

---

## Bibliography (for defensibility — cited in the Overview footer credit, not loaded at runtime)

- Alan Cooper et al., *About Face: The Essentials of Interaction Design*, 4th ed. (Wiley, 2014) — life / end / experience goal types; Goal-Directed Design.
- Donald A. Norman, *The Design of Everyday Things*, rev. ed. (Basic Books, 2013) — the action cycle (goal → intention → action → evaluation); gulfs of execution/evaluation.
- Axel van Lamsweerde, "Goal-Oriented Requirements Engineering: A Guided Tour," *RE'01* (2001) — KAOS, AND/OR goal refinement, obstacles, hard vs soft goals.
- Eric Yu, "Towards Modelling and Reasoning Support for Early-Phase Requirements Engineering," *RE'97* — i* actors, goals, softgoals, dependencies.
- Lawrence Chung, Brian A. Nixon, Eric Yu & John Mylopoulos, *Non-Functional Requirements in Software Engineering* (Kluwer, 2000) — the NFR framework; softgoals and satisficing.
- Jonathan Gutman, "A Means-End Chain Model Based on Consumer Categorization Processes," *Journal of Marketing* 46(2) (1982) — means-end laddering.
- Edwin A. Locke & Gary P. Latham, "Building a Practically Useful Theory of Goal Setting and Task Motivation," *American Psychologist* 57(9) (2002) — goal-setting theory; the SMART-ish quality lens.
- Charles S. Carver & Michael F. Scheier, *On the Self-Regulation of Behavior* (Cambridge, 1998) — hierarchical goal organisation (be-goals / do-goals), the conceptual basis for goal refinement levels.
