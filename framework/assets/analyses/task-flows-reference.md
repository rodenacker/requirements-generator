<!-- ROLE: asset (analysis reference). Methodology definition for the task-flows analyser. Modelled on framework/assets/analyses/activity-diagram-reference.md. Industry framing: Hierarchical Task Analysis (Annett & Duncan 1967; Stanton 2006) plus Task Flow Diagrams (NN/G; Hackos & Redish 1998) — single-actor, decomposition-first, user-mental-model fidelity. -->

# Task Flows analysis reference

> **Method:** Extract a **per-task catalogue** (tasks, subgoals/operations, plans, decision points, exception paths, cross-task operation matrix) from `requirements/requirements.md` once. The tabular catalogue is always rendered. The consultant then picks **none, one, several, or all** of the discovered top-level tasks to add as inline-SVG figures — each selected task produces **two** diagrams: a **Hierarchical Task Analysis (HTA) tree** (goal → subgoals → operations) and a **Task-Flow Diagram (TFD)** (linear narrative, start → steps → exits). Same data, two views per task.

**Output file:** `analyse-requirements/TASK-FLOWS/task-flows.html` — a self-contained HTML artefact containing the tabular catalogue (always) plus zero or more inline-SVG figures (per consultant selection). No external CSS/JS dependencies; viewable by opening `file://` in a browser.

**Analyser agent:** `framework/agents/analyses/task-flows-analyser.md`

**Character:** `framework/assets/characters/task-flows-analysis.md`.

**Readability:** the artefact is human-read (and consumed downstream by `/wireframe`'s `blueprint-architect` via the per-analysis sidecar), so the analyser also follows `framework/shared/output-readability.md` — it writes the "In plain terms" lead, glosses methodology jargon (task flow, HTA, plan, decision point, exception path) at first use in human-readable prose, leaves client domain vocabulary unglossed (GLOSSARY territory), and keeps every `[SRC: C-NNN]` marker. The plain-language layer is confined to the lead + first-use glosses; the catalogue tables, SVG figures, and diagnostics keep their concrete discipline.

---

## Industry framing — HTA + TFD

UX Task Analysis is the practitioner umbrella for two complementary, well-established techniques. Both are dominant standards with stable notations that map cleanly to **extraction from requirements**, not authoring.

### A. Hierarchical Task Analysis (HTA)

- **Origin.** Annett, J., & Duncan, K. D. (1967). *Task analysis and training design*, Occupational Psychology, 41, 211–221. Refined by Stanton, N. A. (2006). *Hierarchical task analysis: developments, applications, and extensions*, Applied Ergonomics, 37(1), 55–79.
- **Output shape.** A hierarchy of **goals → subgoals → operations** with **plans** annotating each non-leaf node.
- **Plans (Annett's three control-structure types, extended by practitioners to four).**
  - `sequence` — procedure / chain ("do 1, then 2, then 3").
  - `selection` — if/then routing ("do 1 if `<guard>`, else do 2").
  - `iteration` — loop ("repeat 1.1–1.3 until `<condition>`").
  - `concurrent` — time-sharing ("do 1 and 2 in parallel").
- **P × C stop rule.** Decomposition stops when the product of Probability-of-failure × Cost-of-failure is acceptably low. For UX, the practitioner default is to stop at the **atomic user-action level** (a single click, key-press, or form-submit).
- **Subgoals-per-level rule.** **3–10 subgoals per parent** (Stanton HTA-7 step 4; Stanton 2006). Fewer than 3 implies the level is redundant; more than 10 implies the parent should be split.
- **Representation forms (Stanton 2004).** List, narrative, flow diagram, hierarchical diagram, table. This analyser uses **table (Tier 1) + hierarchical tree diagram (Tier 2)**.

### B. Task Flow Diagrams (TFD)

- **Practitioner convention** (Nielsen Norman Group; Hackos & Redish 1998 ch. *Thinking About Tasks*). A **linear, single-path** representation of one user task from start state to exit state, with optional inline decision diamonds.
- **Distinct from User Flow** (which branches across all paths) and from **UML Activity Diagrams** (which carry multi-actor swimlanes). Task flow visualises *one chosen path* through the goal — the "golden path" plus its named exception exits.
- **Output.** Numbered steps; each step is a verb-phrase; decision points are inline (`→ option A | option B`); exit states are explicit (`success` / `abort` / `escalate` / `retry` / `compensate`).

### Why HTA + TFD as one methodology

HTA gives the **what** (decomposition); TFD gives the **how** (sequenced path). Both per goal. Both single-actor. They are the canonical pair in NN/G's *Task Analysis* article and in Hackos & Redish's *User and Task Analysis for Interface Design* (1998).

This pair fills a real gap in the analysis set:

| Lens | Methodology | Fidelity |
|---|---|---|
| Multi-actor process flow with swimlanes | activity-diagram (UML 2.5) | component / system |
| Per-scenario inter-component interaction | sequence-diagram (UML 2.5) | message-level |
| Per-entity lifecycle | state-diagram (UML 2.5) | aggregate root |
| Actor goals × main flows × extensions | use-cases (Cockburn) | behavioural |
| **Single-actor decomposition + linear sequenced narrative** | **task-flows (HTA + TFD)** | **goal / user mental model** |

The pair is **extraction-shaped**: HTA decomposes content already in `§5 Task flows` *Steps* (which carry an ordered step sequence); TFD composes that sequence into a narrative. Neither requires invention.

---

## Output structure

The artefact opens with an **In plain terms** lead (`<section id="plain-terms">` carrying `{{PLAIN_SUMMARY}}`) as its **first content section**, above the overview — a 2–5 sentence plain-English summary (what this catalogue is, what it found, what to do with it), per `framework/shared/output-readability.md`. It is a faithful condensation introducing no task, count, or `[SRC]` not already present; methodology jargon is glossed at first use, client domain terms are not. The HTA + TFD figures remain the first *visual* after the lead/overview. Below the lead, the artefact has two tiers.

### Tier 1 — Task-flows catalogue (always rendered)

Seven tabular sections, in this order (six catalogue blocks + one diagnostics block):

1. **Tasks table** — `id` (kebab-case `T-N`), `display_name`, `lead_persona` (§3 persona id), `trigger`, `completion_criterion`, `top_plan` (the root node's plan type), `depth` (deepest decomposition level), `operation_count`, `provenance`.
2. **Subgoals & operations table** — `task_id`, `hierarchical_id` (`T-N.M.K`), `label`, `kind` ∈ {`subgoal`, `operation`}, `parent_id`, `provenance`.
3. **Plans table** — `node_id` (a non-leaf hierarchical id), `plan_type` ∈ {`sequence`, `selection`, `iteration`, `concurrent`}, `plan_text` (Annett-style English, e.g. *"Do T-1.1; if `valid` do T-1.2 else do T-1.3"*), `provenance`.
4. **Decision points table** — `task_id`, `at_step` (TFD step number where the decision sits), `guard` (expression), `branches` (list of `{guard, target_step}`), `provenance`.
5. **Exception paths table** — `task_id`, `trigger_condition`, `flow` (exception-side sequence of operation ids), `exit_type` ∈ {`abort`, `escalate`, `retry`, `compensate`}, `provenance`.
6. **Cross-task operation matrix** — pivoted view: rows = canonical operation labels, columns = task ids, cell = ✓ if operation appears in that task. Surfaces shared operations that warrant first-class shared components downstream.
7. **Diagnostics block** — counts summary, per-marker provenance summary, the 10 check result lines (PASS / FAIL), the density-warning line.

Platform-agnostic. No DBMS-specific types appear in any column.

### Tier 2 — Inline-SVG diagrams (0..N tasks selected; **two SVGs per selected task**)

After the catalogue is extracted, the analyser surfaces a `multiSelect: true` prompt with one option per discovered top-level task plus a "select all" affordance. The consultant picks any combination:

- **Empty selection is valid** — produces a catalogue-only output (Tier 1 only, no SVG blocks). The tabular catalogue is itself a recognised deliverable form.
- **Single selection** — one per-task pair section containing two `<figure>` blocks (HTA tree first, TFD second) under one `<h3>{task_display_name}>` heading.
- **N selections** — N per-task pair sections, each containing two `<figure>` blocks (HTA first, TFD second) under one `<h3>{task_display_name}>` heading. Pairs render in registry order; HTA and TFD for the same task sit together, not in separate type-grouped lists.

Each `<figure>` carries:

**HTA tree (vertical, top-down).**

- **Goal node (root)** — rounded rectangle, thick border, sentence-case label.
- **Subgoal nodes** — rounded rectangles, normal border, sentence-case labels.
- **Operation nodes (leaves)** — sharp rectangles, light fill, lowerCamelCase verb-phrase labels.
- **Plan badges** — small pills (`SEQ` / `SEL` / `ITER` / `CONC`) attached top-right of every non-leaf node.
- **Edges** — thin lines, no arrowheads (hierarchy implied by position).
- **`ai-suggested` nodes** — dashed border + italic label, per the framework-wide convention.

**Task-Flow Diagram (horizontal, left-to-right).**

- **Start state** — oval, green border, label from Round 2 trigger.
- **Step nodes** — rectangles, blue border, numbered label `N. {{text}}`.
- **Decision nodes** — diamonds, amber border, guard label inside.
- **Exit states** — ovals: green-filled for success, red-bordered for `abort` / `escalate` / `retry` / `compensate`, exit-type label inside.
- **Edges** — arrowheads (open triangle); decision-out edges carry the branch label as inline text.

All HTA trees in a single render share a **`node_height`** (max label width × 1.4 + padding). All TFDs in a single render share a **`step_height`**. Both grids are computed once across selected tasks and reused, so figures align visually when the consultant scrolls between them.

---

## Source-of-truth hierarchy

The analyser walks `requirements/requirements.md` in this order:

1. **`§5 Task flows`** — primary. Each top-level task-flow row in the template (`framework/assets/template-requirements.md:122–135`) carries six sub-cells: `Actor`, `Trigger`, `Steps`, `Decision points`, `Exception paths`, `Role-conditional behaviour`. Every methodology field maps to a sub-cell:

| Methodology field | `§5` sub-cell | Notes |
|---|---|---|
| Top-level task title | the *Flow* row heading itself | One row → one candidate top-level task. |
| Lead persona (actor) | *Actor* → `§3` persona id | If *Actor* names a generic noun ("the user"), match to `§3` by role inference; mark `ai-suggested` if no match. |
| Trigger | *Trigger* | Verbatim where present; else infer from §4 story preface as `ai-suggested`. |
| Subgoals + operations | *Steps* | Each step is either a subgoal (multi-action outcome) or an operation (atomic action). Recursive decomposition where a step itself names multiple actions. |
| `selection` plans | *Decision points* + *Role-conditional behaviour* | Branches → plan text; role gates → conditional subgoal access. |
| Exception paths | *Exception paths* | Each clause → one TFD exit-state. |

2. **`§5` *Decision points*** — every "if X then Y else Z" / "when Q is met, …" clause becomes a candidate TFD decision diamond + an HTA `selection` plan on the parent node.
3. **`§5` *Exception paths*** — every "on failure, …" / "if invalid, …" / "on timeout, …" clause becomes a TFD exception-exit state. `exit_type` is inferred from the verb (`reject` → `abort`; `escalate` → `escalate`; `retry` → `retry`; `roll back` / `undo` → `compensate`).
4. **`§5` *Role-conditional behaviour*** — every "available only to <role>" / "approved by <role>" clause influences subgoal visibility; reflected in the plan text on the affected non-leaf node.
5. **`§4 User goals & stories`** — supplementary top-level tasks. A story without a matching `§5` task surfaces as a candidate task with provenance `derived-from-§4`. The story's *Objective* becomes the goal.
6. **`§3 Target users`** — personas resolve actor / lead-persona references.
7. **`§6 Requirements`** — business rules become **decision guards** (e.g., `amount > 10000`), **iteration triggers** (`for each`, `repeat until`), **concurrency markers** (`concurrently`, `in parallel`), and **acceptance criteria** that anchor completion criteria.
8. **`§7 Data entities`** — informs the `notes` field on operations when an operation manipulates a named entity. Not surfaced as a separate column at MVP.

If `§5 Task flows` is absent or empty, the analyser **degrades gracefully** to `§4 + §6` derivation. Density of `ai-suggested` markers will be high; the soft warning surfaces this in diagnostics.

---

## Seven-round discipline

Each round produces a distinct, named in-memory output. The analyser does not write the artefact until Round 7 is complete and all 10 hard quality checks have passed (or the consultant chose Override).

### Round 1 — Top-level task discovery (exploratory and inclusive)

- Walk `§5 Task flows`: every top-level flow row is a candidate top-level task `{candidate_id, candidate_display_name, source: "§5.N", source_line_offset}`. The `candidate_id` is kebab-case from the flow's heading.
- Walk `§4 User goals & stories`: every story whose verb-phrase does not appear in any `§5` flow is a candidate with provenance `derived-from-§4`.

Output (in memory): the candidate task list. Do not dedupe yet — Round 2 handles that.

**Cap rule:** if the candidate list exceeds **8 top-level tasks**, state the cap aloud (*"Selecting 8 of 11 candidate tasks: the 6 from §5 plus 2 from §4 with highest step density. Discarded: …"*). The artefact is a focused deliverable, not an exhaustive task catalogue. The 8-cap follows NN/G's practitioner recommendation: an HTA artefact with more than 8 top-level tasks is harder to scan than two split artefacts.

### Round 2 — Actor, trigger, completion (sourced)

For every candidate task:

- **Lead persona.** Extract from `§5 Task flows` *Actor* sub-cell:
  - Verbatim `§3` persona id → provenance `from-task-flow`.
  - Generic noun ("the user", "an admin") matched to `§3` by role inference → provenance `derived-from-§3`.
  - No match → propose `user` as `ai-suggested`.
- **Trigger.** Extract from `§5 Task flows` *Trigger* sub-cell verbatim → provenance `from-task-flow`. Else infer from `§4` story preface or `§6` constraint phrasing → `derived-from-§N`. Else default to *"The actor initiates the task"* → `ai-suggested`.
- **Completion criterion.** Extract from `§6 Requirements` acceptance criteria that match the task scope → provenance `derived-from-§6`. Else infer from the last `§5` step's outcome verb ("the order is recorded" → *"The order is recorded in the system"*) → `derived-from-§5`. Else default to *"Task ends when the last operation completes"* → `ai-suggested`.

Drop candidates that cannot anchor a lead persona (after generic-noun resolution and `ai-suggested` fallback) — these are not valid HTA tasks. Output: the task list with `actor`, `trigger`, `completion_criterion` populated.

### Round 3 — HTA decomposition

Per task, walk `§5 Task flows` *Steps* recursively. Build the hierarchical tree:

- **Goal (root).** Hierarchical id `T-N`. Label is the task's `display_name`. Provenance matches the task's overall provenance.
- **Subgoals.** A `§5` step whose verb phrase implies a multi-action outcome ("validate the order", "collect customer details") becomes a subgoal. Hierarchical id `T-N.M`. Label is sentence-case from the step.
- **Operations (leaves).** A `§5` step whose verb phrase names an atomic user action ("click submit", "enter the amount", "select the file") becomes an operation. Hierarchical id `T-N.M.K` (or `T-N.M` if the parent is the root and the step doesn't decompose further). Label is lowerCamelCase verb-phrase (`clickSubmit`, `enterAmount`, `selectFile`). Forbidden tokens: `and`, `then`, `etc`, empty.
- **Recursive decomposition.** If a step like "validate the order — check stock, check credit, check address" packs multiple sub-actions into one step, decompose into one subgoal (`Validate the order`) + three operation children (`checkStock`, `checkCredit`, `checkAddress`). Provenance per child: `derived-from-§5` (the verbs come from §5 but the decomposition into separate operations is the analyser's structural choice — this is consistent with the activity-diagram analyser's treatment of compound steps).

**Stop rule** (Stanton HTA-7 step 6; Annett-Duncan P × C heuristic; UX default per UXmatters and NN/G): stop at the atomic user-action level. An operation is atomic when its verb names a single discrete user action that cannot be meaningfully decomposed without crossing into design fidelity (mouse-level coordinates, keystroke timing). The framework's `feedback_analyses_are_extraction_not_authoring` rule reinforces this: only decompose what `§5` actually names.

**Caps:**

- **Decomposition depth ≤ 3 levels** (root + 2 nested levels — operations at `T-N.M.K`). If `§5` step density implies deeper, state the cap aloud and surface the underdescribed branch in diagnostics. Depths > 3 turn the HTA into a procedural transcript and lose the lens's value.
- **Subgoals per parent ≤ 10** (Stanton). If a parent has >10 children, state aloud and surface the overloaded parent in diagnostics for the consultant to split. Subgoals-per-parent < 3 is also flagged (likely redundant level) but is not capped.

Each node carries `{hierarchical_id, label, kind ∈ {goal, subgoal, operation}, parent_id, notes, provenance}`. The goal kind appears exactly once per task (the root); every other node is `subgoal` or `operation`.

### Round 4 — Plans (Annett control structures)

Per non-leaf node (every node where `kind == goal` or `kind == subgoal`), assign a plan:

- **`sequence`** — default. Plan text: *"Do {{ordered child id list}}"*. Provenance:
    - `from-task-flow` if `§5` *Steps* list the children in clear sequence.
    - `ai-suggested` if no other signal (this is the most common default).
- **`selection`** — from `§5` *Decision points* (clauses like *"if amount > 10000, route to senior approver, else self-approve"*) or `§5` *Role-conditional behaviour* (clauses like *"available only to team leads"*). Plan text: *"Do {{child_id}} if `{{guard}}`, else do {{other_child_id}}"*. Provenance `derived-from-§5`. Multi-way selections use comma-separated guard/child pairs.
- **`iteration`** — from `§5`/`§6` clauses with `for each`, `repeat until`, `for every`, `until X holds`. Plan text: *"Repeat {{child_id_range}} until `{{condition}}`"*. Provenance `derived-from-§5` or `derived-from-§6`.
- **`concurrent`** — from `§5`/`§6` clauses with `concurrently`, `in parallel`, `while X, also Y`, `at the same time`. Plan text: *"Do {{child_id}} and {{other_child_id}} concurrently"*. Provenance `derived-from-§5` or `derived-from-§6`.

Plan text is Annett-style English (one sentence) — the methodology's canonical form. The pill badge (`SEQ` / `SEL` / `ITER` / `CONC`) carries the plan_type in the diagram; the table carries both the type and the text.

### Round 5 — TFD narrative

Per top-level task, compose a numbered linear flow:

- **Start state** — from Round 2 trigger. Rendered as the first node (oval) in the TFD SVG; text is the trigger phrase verbatim.
- **Steps** — walk the HTA in **left-DFS order** (depth-first, leftmost-child-first), emitting one TFD step per operation (leaf). Steps inherit `seq` (1..N integer); each step carries `text` (sentence-case form of the operation label), `refs` (single-element list with the operation's hierarchical id), and `provenance` (matches the operation's).
- **Decision points** — inline diamonds inserted before the step branches diverge. The TFD takes the **golden path** branch (the first branch by guard ordering) as the main flow; alternative branches become inline `→ if <guard> → step N-alt` annotations and (where they lead to non-success outcomes) become exception exits.
- **Exception exits** — one per `§5 Task flows` *Exception paths* clause. Each becomes a TFD exit node positioned below the main flow line at the step where the exception is triggered. `exit_type` is inferred from the verb (`reject` → `abort`; `escalate` → `escalate`; `retry` → `retry`; `roll back` / `undo` → `compensate`).
- **Success exit** — from Round 2 completion criterion. Rendered as the final node (green-filled oval) at the right end of the main flow.

Each TFD step carries `{step_no, text, refs, decision?, exit?, provenance}`. The TFD is the **golden path plus its named exception exits** — not the full branching tree (that's the activity-diagram analyser's job; mirroring its work here would duplicate and confuse).

**TFD step-count rule:** golden path 3–25 steps. Fewer than 3 implies the task is too small to warrant a TFD (mark as `trivial-task` warning in diagnostics; render anyway); more than 25 implies the task should be split (cap with the soft warning, render anyway).

### Round 6 — Cross-task consistency

Final normalisation before render:

- **Operation-label consistency.** If two tasks perform the same logical operation, the operation label must be identical. Pick the canonical lowerCamelCase label once (longest verbatim match in `§5`; else first occurrence in registry order) and rewrite all references in HTA nodes, TFD step refs, and the cross-task operation matrix.
- **Subgoal-label consistency.** Same rule for subgoals (sentence-case canonical label).
- **Build the cross-task operation matrix.** Pivot: `matrix[operation_label][task_id] = true` if the operation appears in any node of that task's HTA. The matrix is its own Tier-1 table.

### Round 7 — Pre-render layout sanity

- Count nodes per HTA tree; if any tree has > 30 nodes, flag a soft warning in diagnostics: *"Tree `submit-order` has 38 nodes — SVG height will be tall; consider splitting the task into sub-tasks"*.
- Count steps per TFD; if any TFD has > 25 steps, flag a soft warning: *"TFD `onboard-customer` has 31 steps — SVG width will be wide; consider splitting into sub-tasks"*.
- Compute shared layout grids: `node_height` (max node label width × 1.4 + padding) reused across all HTA trees in the run; `step_height` similarly reused across all TFDs.

Output: normalised catalogue + layout grids.

---

## Provenance markers (3 — exhaustive)

Every task, node (HTA), plan, decision point, exception path, and operation-matrix entry carries exactly one of:

| Marker | CSS class | When |
|---|---|---|
| `from-task-flow` | `.provenance-from-task-flow` | Content appears verbatim in a `§5 Task flows` sub-cell. |
| `derived-from-§N` | `.provenance-derived` | Content was extracted from a named section (`§2`, `§3`, `§4`, `§6`, `§7`) but is not verbatim in `§5`. The source section is recorded in a `data-source="§N"` attribute on the row. |
| `ai-suggested` | `.provenance-ai-suggested` | Content was inferred (e.g., an `ai-suggested` plan default, an inferred completion criterion, an inferred actor when only a generic noun appears, an inferred operation-subgoal split when a §5 step packs multiple actions). Prefixed with `[AI-SUGGESTED]` in the text content. |

No fourth marker. No row unmarked. Honours the framework-wide `feedback_ai_suggested_invariant` — the marker is reserved for facts not traceable to inputs and not covered by a `GR-NN` general rule.

---

## Quality checks (10 hard gates)

All checks operate on the catalogue — they are **independent of which tasks the consultant selects for rendering**. The catalogue must be valid regardless of presentation.

1. **Every top-level task has a kebab-case id, a display name, and a lead persona id referenced in `§3`.** Id matches `[a-z0-9-]+`; persona is a §3 entry (verbatim) or the `ai-suggested` fallback `user`.
2. **Every top-level task has a non-empty `trigger` and a non-empty `completion_criterion`** (sourced, derived, or `ai-suggested`). Both fields are required.
3. **Every HTA tree has at least one decomposition level** (i.e., the goal has at least one subgoal-or-operation child). Zero-depth trees (a goal with no children) restate the goal without analysing it; flagged.
4. **Every non-leaf HTA node has a `plan` value in {`sequence`, `selection`, `iteration`, `concurrent`}** and a non-empty `plan_text`.
5. **Every leaf operation has a non-empty lowerCamelCase verb-phrase label.** Forbidden tokens: `and`, `then`, `etc`, empty string. Validation: regex `^[a-z][a-zA-Z0-9]+$`.
6. **Every TFD has a start state, ≥1 numbered step, and ≥1 exit state** (success exit + zero-or-more exception exits).
7. **Caps respected.** Total top-level tasks ≤ 8. Decomposition depth ≤ 3 levels. Subgoals per non-leaf parent ≤ 10. (If exceeded after a cap-aloud, the surplus is dropped from the catalogue with a note.)
8. **Every operation referenced in a TFD step `refs` exists in the HTA** (cross-table integrity check).
9. **Every row in every Tier-1 table carries exactly one provenance marker** — never zero, never two.
10. **Every decision point has ≥2 outgoing branches, each with a non-empty guard expression** (mirrors the activity-diagram analyser's check on decision nodes).

**Soft check (warning, not gate):**

- **AI-SUGGESTED density.** Compute `density_operations = ai_suggested_operations / total_operations`. If > 50%, emit a `density-warning` line in diagnostics and the handback summary: *"`§5 Task flows` is thin — most operations were inferred. Enrich `§5` *Steps* and re-run for higher-confidence trees."*. Does not block writing.

---

## Task-selection sub-step

After all 10 hard checks pass (or the consultant chose Override at Step 8), the analyser surfaces a single `AskUserQuestion` with `multiSelect: true`:

- **Question:** *"The task-flows catalogue has been extracted and validated. Which tasks should be rendered as inline-SVG diagrams (HTA tree + Task-Flow Diagram per task)? Pick none, one, several, or all — the catalogue tables above are always rendered."*
- **Header:** `Diagrams`
- **Options:** one option per discovered top-level task, labelled `<display_name> — <node_count> nodes, <step_count> TFD steps`. Default ordering: registry / discovery order. The first option is suffixed `(Recommended)` if it is the highest-node-count task.

Empty selection is **valid**. Cancelling the prompt outright (closing the dialog rather than submitting) hands control back to the accept/revise/restart loop, not to silent emission.

---

## Stop-condition

The analysis is complete when:

- Every top-level task has a row in the Tasks table with a populated actor, trigger, completion criterion, and at least one decomposition level.
- Every node in any HTA has a row in the Subgoals & operations table.
- Every non-leaf node has a row in the Plans table.
- Every decision point and exception path has a row in its respective table.
- All 10 hard quality checks pass, or the consultant chose Override.
- The consultant chose Accept in the Step 11 accept/revise/restart loop.

---

## Input-coverage asymmetry

`§5 Task flows` carries the step sequence and the actor cleanly. The columns it does **not** typically carry:

- **Goal-level outcome statement.** Task flows describe steps, not the strategic goal. The analyser composes a goal label from the flow's heading + `§4` story *Objective*; if the heading is gerund-form ("Submitting an order"), it is rewritten to the canonical active form ("Submit an order").
- **Completion criterion.** `§5` rarely names "task ends when…"; the analyser pulls from `§6` acceptance criteria where possible, else infers from the last step's outcome verb, else applies the `ai-suggested` default.
- **Plan types on intermediate subgoals.** `§5` *Decision points* and *Role-conditional behaviour* mark the selection plans; `§6` constraints mark iteration and concurrency; the analyser defaults the rest to `sequence` (`ai-suggested`).
- **Atomic-action verbs.** `§5` steps are often phrased at the subgoal level ("validate the order"); the analyser decomposes into operations when the step packs multiple actions, marking the operation labels `derived-from-§5` (the verbs come from the step, the splitting is structural).
- **Exit types.** `§5` *Exception paths* name the failure but not the exit type; the analyser classifies (`abort` / `escalate` / `retry` / `compensate`) by verb inference and marks `derived-from-§5`.

Richer inputs → richer catalogue. Methodology degrades gracefully: with thin `§5`, the catalogue is mostly inferred and flagged.

---

## Output shape (HTML schema)

The artefact is a single self-contained HTML file at `analyse-requirements/TASK-FLOWS/task-flows.html`. The analyser populates `framework/assets/analyses/template-task-flows.html` via documented placeholder substitution. Every substituted value is HTML-escaped before injection (XML-escape inside `<svg><text>` nodes).

### Header placeholders

| Placeholder | Value |
|---|---|
| `{{TITLE}}` | *"Task Analysis & Task Flows — `<domain>`"* if `§1` declares a domain, else *"Task Analysis & Task Flows"*. |
| `{{DOMAIN}}` | Verbatim from `§1 Application context > Domain` if present, else *"(not declared in requirements.md)"*. |
| `{{GENERATED_AT}}` | ISO-8601 UTC, captured at render time. |
| `{{REQUIREMENTS_SHA256}}` | SHA-256 of `requirements/requirements.md` captured at Step 2. |
| `{{TASK_COUNT}}` | Number of rows in the Tasks table. |
| `{{SUBGOAL_COUNT}}` | Number of rows in the Subgoals & operations table with `kind == subgoal`. |
| `{{OPERATION_COUNT}}` | Number of rows in the Subgoals & operations table with `kind == operation`. |
| `{{PLAN_COUNT}}` | Number of rows in the Plans table. |
| `{{DECISION_COUNT}}` | Number of rows in the Decision points table. |
| `{{EXCEPTION_COUNT}}` | Number of rows in the Exception paths table. |
| `{{AI_SUGGESTED_COUNT}}` | Total items (tasks + nodes + plans + decisions + exceptions) marked `ai-suggested`. |
| `{{TASKS_RENDERED}}` | Comma-separated list of task display names whose SVGs were emitted, or *"none — catalogue only"* if zero were selected. |

### Body placeholders

| Placeholder | Value |
|---|---|
| `{{DIAGNOSTICS_BLOCK}}` | Pre-rendered `<section class="diagnostics">` containing: counts summary line, per-marker provenance summary, the 10 check result lines (PASS/FAIL), the density-warning line (`class="hidden"` if ≤ 50%), and (on Override runs) per-flagged-item lines. |
| `{{CATALOGUE_BLOCK}}` | Pre-rendered `<section class="catalogue">` containing the six Tier-1 tables in fixed order (Tasks, Subgoals & operations, Plans, Decision points, Exception paths, Cross-task operation matrix). The diagnostics section is rendered separately via `{{DIAGNOSTICS_BLOCK}}` — not duplicated inside the catalogue block. |
| `{{TASK_DIAGRAMS_BLOCK}}` | Pre-rendered `<section class="task-diagrams">` containing one `<section class="task-pair task-{slug}">` per selected task. Each pair section carries a single `<h3>{task_display_name}>` heading, a combined `<p class="task-meta">` line (HTA + TFD counts), one `<figure class="hta-tree task-{slug}">` (with `<figcaption><h4>HTA tree</h4></figcaption>`), and one `<figure class="tfd task-{slug}">` (with `<figcaption><h4>Task flow</h4></figcaption>`), in that order. Pairs render in registry order so HTA + TFD for the same task sit together. If the consultant selected zero tasks, this placeholder renders as `<section class="task-diagrams"><p class="diagrams-empty">No diagrams were selected. The catalogue tables above are the deliverable.</p></section>`. |
| `{{MERMAID_BLOCK}}` | Pre-rendered `<details class="mermaid-source">` containing zero-to-N Mermaid blocks: per selected task, one `graph TB` source for the HTA tree + one `flowchart LR` source for the TFD. If zero tasks selected, renders as `<!-- no mermaid equivalents -->`. Captions clearly label each block as "text source for copy-paste into mermaid.live; not rendered inline". |

### SVG conventions

- `viewBox="0 0 W H"` per `<svg>`. For HTA: W = max_breadth × column_width + padding; H = depth × level_height + padding. For TFD: W = step_count × column_width + padding; H = step_height + (exception_lane_count × exception_height) + padding.
- `role="img"` + `aria-label="HTA tree for <task_display_name>"` / `aria-label="Task flow for <task_display_name>"` on every `<svg>`.
- All `<text>` nodes XML-escape labels and guards.
- **Shared `node_height` / `step_height` across all rendered figures in a single render** — keeps trees and flows visually aligned when the consultant scrolls between them. (Mirrors the activity-diagram analyser's shared `lane_height` invariant.)
- Arrowhead marker (`<defs><marker id="tfd-arrow-{slug}">`) defined once per TFD SVG. HTA SVGs do not emit arrowheads (hierarchy implied by position).
- Labels truncated to 40 chars with `<title>` tooltip carrying the full text.

### CSS class contract used by the analyser

The template scaffold owns CSS variables, layout, and typography. The analyser emits HTML using the following named classes:

- `.catalogue` — outer container for Tier 1 tables.
- `.tasks-table`, `.nodes-table`, `.plans-table`, `.decisions-table`, `.exceptions-table`, `.op-matrix-table` — one per Tier-1 section.
- `.task-diagrams` — outer container for Tier 2 per-task pairs.
- `.task-pair` — wraps one HTA + TFD pair for one task; carries a `.task-{slug}` modifier.
- `.hta-tree` / `.tfd` — applied to every `<figure>`; one `.task-{slug}` modifier per task.
- `.diagrams-empty` — applied to the `<p>` when zero tasks selected.
- Inside HTA SVG: `.hta-goal`, `.hta-subgoal`, `.hta-operation`, `.hta-label`, `.hta-edge`, `.plan-badge`, `.plan-badge-seq`, `.plan-badge-sel`, `.plan-badge-iter`, `.plan-badge-conc`.
- Inside TFD SVG: `.tfd-start`, `.tfd-step`, `.tfd-decision`, `.tfd-exit-success`, `.tfd-exit-abort`, `.tfd-exit-escalate`, `.tfd-exit-retry`, `.tfd-exit-compensate`, `.tfd-step-label`, `.tfd-edge`, `.tfd-edge-guard`, `.tfd-edge-guard-bg`.
- `.kind-goal`, `.kind-subgoal`, `.kind-operation` — pill badges in the nodes table.
- `.plan-type-sequence`, `.plan-type-selection`, `.plan-type-iteration`, `.plan-type-concurrent` — pill badges in the plans table.
- `.exit-type-abort`, `.exit-type-escalate`, `.exit-type-retry`, `.exit-type-compensate` — pill badges in the exceptions table.
- `.provenance-from-task-flow`, `.provenance-derived`, `.provenance-ai-suggested` — exactly one per content row in any table.
- `.ai-suggested` — applied to any cell whose content carries the `[AI-SUGGESTED]` prefix. Renders italic + dim background.
- `.matrix-cell-present`, `.matrix-cell-absent` — operation-matrix table cell variants.
- `.mermaid-source` — applied to the `<details>` wrapping the Mermaid `<pre>` blocks.
- `.rev-marker` — applied to any row flagged by a failed quality check on an Override run.

The analyser does **not** edit the template's CSS or layout — only the documented `{{placeholders}}` are substituted.

---

## Downstream consumption (handled by `framework/skills/map-task-flows-to-ui.md`)

- **Top-level tasks** → screen-flow inventory entries. Each task maps to a sequence of screen transitions in the design spec.
- **HTA subgoals** → screen / step grouping (a subgoal often equals a screen or wizard step).
- **HTA operations** → form fields / CTAs / atomic UI affordances (each operation maps to one user-visible control).
- **Plans** → routing logic: `sequence` → linear wizard; `selection` → branching screen; `iteration` → list / repeater pattern; `concurrent` → tab / dashboard pattern.
- **Decision points** → branching UI affordances (conditional sections, gated CTAs).
- **Exception paths** → error-state UI (toast, banner, modal, recovery screen).
- **Cross-task operation matrix** → component-reuse hints (an operation present in 3+ tasks warrants a first-class shared component in the design system).

`framework/skills/map-task-flows-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character file and for future downstream design-spec authors.
