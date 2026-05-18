<!-- ROLE: asset (analysis reference). Methodology definition for the activity-diagram analyser. Modelled on framework/assets/analyses/sequence-diagram-reference.md. Industry framing: OMG UML 2.5 activity-diagram subset — one diagram per flow, swimlane-partitioned, control-flow only (object flow deferred). -->

# Activity Diagram analysis reference

> **Method:** Extract a **per-flow activity-diagram catalogue** (flows, swimlanes, actions, control nodes, edges, cross-flow swimlane matrix) from `requirements/requirements.md` once. The tabular catalogue is always rendered. The consultant then picks **none, one, several, or all** of the discovered flows to add as inline-SVG `<figure>` blocks. Same data, the visuals are views onto the flows already listed in the catalogue.

**Output file:** `analyse-requirements/ACTIVITY-DIAGRAM/activity-diagram.html` — a self-contained HTML artefact containing the per-flow tabular catalogue (always) plus zero or more inline-SVG activity-diagram figures (per consultant selection). No external CSS/JS dependencies; viewable by opening `file://` in a browser.

**Analyser agent:** `framework/agents/analyses/activity-diagram-analyser.md`

**Character:** `framework/assets/characters/activity-diagram-analysis.md`.

---

## Industry framing — UML 2.5 activity-diagram subset

Per OMG UML 2.5 § 15.2 (Activity Diagrams), an activity diagram models the flow of control (and optionally data) through a sequence of action nodes within named partitions (swimlanes). The full UML notation has 30+ node types and rich features (object nodes, expansion regions, interruptible regions, accept-event/send-signal actions, activity parameters, pins). This methodology restricts the subset to elements that map cleanly to requirements text:

| Element | UML name | Included | Why included / why excluded |
|---|---|---|---|
| Action | OpaqueAction | yes | Every `§5 Task flows` step is an action node. |
| Initial node | InitialNode | yes | One per flow. Often inferred (`ai-suggested`) when `§5` omits an explicit start. |
| Activity final node | ActivityFinalNode | yes | One or more per flow. Terminates the entire flow. |
| Flow final node | FlowFinalNode | yes | Terminates a single concurrent branch without ending the activity. |
| Decision node | DecisionNode | yes | From `§5` *Decision points* and `§6` constraints (if/else, guard branches). |
| Merge node | MergeNode | yes | Where decision branches converge. Often inferred (`ai-suggested`). |
| Fork node | ForkNode | yes | From "concurrently", "in parallel", "while" clauses. |
| Join node | JoinNode | yes | Where parallel branches reconverge. Often inferred (`ai-suggested`). |
| Swimlane | ActivityPartition | yes | Horizontal rows; one per actor / system component / external system. |
| Control flow edge | ControlFlow | yes | Default sequencing between nodes. Carries `guard` only on decision-out edges. |
| Object node / object flow | ObjectNode / ObjectFlow | **no — MVP** | Adds richness but raises `ai-suggested` density (§5 rarely names per-step payloads); revisit post-MVP. |
| Send-signal / accept-event action | SendSignalAction / AcceptEventAction | **no — MVP** | Cross-cuts sequence-diagram message space; defer. |
| Expansion region | ExpansionRegion | **no — MVP** | Iteration over collections — encodes implementation pattern, not requirements. |
| Interruptible activity region | InterruptibleActivityRegion | **no — MVP** | Cross-cutting exception handling — design intent, not requirements. |
| Pin / parameter / activity parameter | Pin / Parameter / ActivityParameterNode | **no — MVP** | Method-level fidelity out of scope. |
| Nested partition | nested ActivityPartition | **no — MVP** | Flat partition model only. |

System-level fidelity: swimlanes are **the persona actor + named system components/aggregates from `§2 Domain model` + inferred external systems**. Per-method fidelity is out of scope — most rows would be `ai-suggested` (design speculation), which degrades the audit trail.

---

## Output structure

The artefact has two tiers:

### Tier 1 — Activity-diagram catalogue (always rendered)

Seven tabular sections, in this order (six catalogue blocks + one diagnostics block):

1. **Flows table** — `id` (kebab-case), `display_name`, `type` (`primary` / `extension` / `recovery`), `actor` (persona id of the lead actor swimlane), `goal` (one-line outcome), `source` (`§5.N` task-flow id, `§4.N` story id, or `derived`), `action_count`, `provenance`.
2. **Swimlanes table** — `id` (kebab-case), `display_name`, `kind` (`actor` / `system-component` / `external-system`), `role` (one-line description), `flows` (comma-separated flow ids that reference this swimlane), `provenance`.
3. **Actions table** — `flow_id`, `seq` (integer 1..N within flow), `id` (kebab-case `A-NN` within the flow), `label` (lowerCamelCase verb-phrase), `owning_swimlane` (swimlane id), `kind` (`action` / `decision-prep` / `external-call`), `notes`, `provenance`.
4. **Control nodes table** — `flow_id`, `id` (`N-NN` zero-padded), `type` (`initial` / `activity-final` / `flow-final` / `decision` / `merge` / `fork` / `join`), `owning_swimlane` (swimlane id; for decision/merge/fork/join, the swimlane that owns the decision logic — defaults to the most-frequent upstream action's swimlane), `notes`, `provenance`.
5. **Edges table** — `flow_id`, `source` (action id or control-node id), `target` (action id or control-node id), `guard` (expression text; non-empty only on edges leaving a decision node), `provenance`.
6. **Cross-flow swimlane matrix** — pivoted view: rows = swimlanes, columns = flows, cell = check mark or empty. Helps the consultant spot swimlanes used in only one flow (may be flow-specific) or in every flow (load-bearing — first-class component).
7. **Diagnostics block** — counts summary, per-marker provenance summary, the 10 check result lines (PASS / FAIL), the density-warning line.

Platform-agnostic. No DBMS-specific types appear in any column.

### Tier 2 — Inline-SVG activity diagrams (0..N, consultant-selected)

After the catalogue is extracted, the analyser surfaces a `multiSelect: true` prompt with one option per discovered flow plus a "select all" affordance. The consultant picks any combination:

- **Empty selection is valid** — produces a catalogue-only output (Tier 1 only, no SVG blocks). The tabular catalogue is itself a recognised deliverable form.
- **Single selection** — one `<figure class="activity-diagram flow-{slug}">` with one inline `<svg>`.
- **N selections** — N figures, one per selected flow. All figures share the same `lane_height` so swimlanes align horizontally across flows when the consultant scrolls between them.

Each SVG carries:

- **Swimlane bands** (horizontal rows) — one band per swimlane (actor topmost; system-components middle; external-systems bottom). Each band has a left-side label and a horizontal divider.
- **Action nodes** — rounded rectangles (`rx="8"`) positioned within their owning swimlane band at `(x_seq, y_swimlane)`.
- **Decision / Merge nodes** — diamond shapes (rotated squares), guards labelled on outgoing arrows.
- **Fork / Join bars** — thick horizontal black bars spanning the relevant swimlanes.
- **Initial node** — small filled black circle.
- **Activity final node** — bullseye (filled circle inside open circle).
- **Flow final node** — circle with an X.
- **Control-flow edges** — open arrowheads connecting nodes; edges crossing swimlane boundaries draw vertical segments at the partition boundary.

---

## Source-of-truth hierarchy

The analyser walks `requirements/requirements.md` in this order:

1. **`§5 Task flows`** — primary. Each top-level task flow becomes a candidate flow. Each step in the flow becomes a candidate action. The first noun in each step is a candidate swimlane owner.
2. **`§5` *Decision points* sub-cell** — every "if X then Y else Z" or "when Q is met, …" branch becomes a candidate decision node with `guard = X` or `Q`.
3. **`§5` *Exception paths* sub-cell** — every "on failure, …" / "if invalid, …" / "on timeout, …" clause becomes a candidate decision-out edge plus a downstream action sequence (often terminating in a flow-final).
4. **`§5` *Role-conditional behaviour* sub-cell** — every "available only to <role>" / "approved by <role>" clause influences swimlane assignment of nearby actions.
5. **`§4 User goals & stories`** — supplementary flows. A story without a matching task flow surfaces as an `ai-suggested` flow (the user clearly wants the goal; no task-flow walks through it).
6. **`§2 Domain model`** — default swimlane catalogue:
    - `§2.1 Concepts` — entities become candidate `system-component` swimlanes when actions interact with them directly.
    - `§2.3 Aggregates & lifecycles` — aggregate roots become primary `system-component` swimlanes (aggregates own the action surface in DDD-style architectures).
7. **`§3 Target users`** — personas become the `actor` swimlane of flows they participate in.
8. **`§6 Requirements`** — business rules become **decision-node guards** (`amount > 10000`) and **alternative branches** (error / recovery paths). Constraints flagged with `concurrently` / `in parallel` become fork nodes; "wait for all" / "synchronise" become join nodes.
9. **`§7 Data entities`** — informs `notes` field on actions when the action operates on a named entity. (Object flow nodes deferred for MVP — entity name surfaces in notes only.)

If `§5 Task flows` is absent or empty, the analyser degrades gracefully to `§4 + §6` derivation. Density of `ai-suggested` markers will be high; the soft warning surfaces this in diagnostics.

---

## Seven-round discipline

Each round produces a distinct, named in-memory output. The analyser does not write the artefact until Round 7 is complete and all 10 hard quality checks have passed (or the consultant chose Override).

### Round 1 — Flow discovery (exploratory and inclusive)

- Walk `§5 Task flows`: every top-level task flow is a candidate flow `{candidate_id, candidate_display_name, source: "§5.N", source_line_offset}`. The `candidate_id` is kebab-case from the task-flow title.
- Walk `§4 User goals & stories`: every story with a clearly separate verb-phrase from any task-flow is a candidate (e.g. "As an Owner I want to reset my password" — typically not in task flows). Provenance `derived-from-§4`.
- Walk `§6 Requirements` for **explicit recovery / error flows** ("on failed payment, the system must retry up to 3 times and then escalate"). These become recovery-type candidate flows. Provenance `derived-from-§6`.

Output: candidate flow list. Do not dedupe yet — Round 2 handles that. **Cap rule:** if the candidate list exceeds 20 flows, state the cap aloud, surface the top 12 by source frequency (§5 first, then §4, then §6), and discard the rest with a note in diagnostics.

### Round 2 — Flow refinement (decisive)

Per **Quality checks 1, 2, 3**:

- **Merge synonyms.** When candidates describe the same outcome ("submit order" and "create order" and "place order"), pick the canonical id from `§5` if present, else from the most-frequent occurrence. Record the alias in the flow's notes field.
- **Pair happy paths with recoveries.** When `§6` declares a recovery flow whose precondition matches a `§5` task flow, mark them as a `primary` + `recovery` pair (same actor, same goal phrasing, different outcome). Each is its own flow row.
- **Classify type.** Every flow is one of:
    - `primary` — happy path from `§5` task flow or a `§4` story.
    - `extension` — `§5` task flow with branching ("the user can choose to skip step 4") that warrants a separate diagram.
    - `recovery` — error / retry / compensation path from `§6` constraints or `§5` *Exception paths* sub-cell.
- **Assign kebab-case id and display name.** Id: `submit-order`, `cancel-order`, `retry-failed-payment`. Display name: `Submit an order`, `Cancel an order`, `Retry failed payment` (sentence-case from the source title).
- **Assign goal.** One-line outcome statement. From the source `§5` task-flow's *Trigger* or first sentence, or from the `§4` story's "I want to..." clause.
- **Assign provenance marker** per the three-marker contract (see Provenance markers below).
- **Drop candidates** that cannot be sourced after merging.

Output: the flow list as `[{id, display_name, type, actor: null, goal, source, source_line_offset, provenance, notes}]`. The `actor` field stays null until Round 3 assigns it. Flow IDs are kebab-case; uniqueness is enforced.

### Round 3 — Swimlane extraction

Per **Quality checks 2, 9**:

- **Actor swimlane.** For each flow, identify the lead actor:
    - If the source `§5` task flow names a persona in the *Actor* field (e.g. "Owner"), the persona's `§3` id is the actor. Provenance `from-task-flow` (verbatim from §5).
    - If only a generic noun appears ("the user submits..."), match to a `§3` persona by role inference; if multiple personas qualify, mark the actor as the most-frequent persona in the flow's source section. Provenance `derived-from-§3`.
    - If no persona can be matched, propose a generic `user` swimlane as `ai-suggested`.
- **System-component swimlanes.** Walk the source `§5` task-flow steps:
    - Every aggregate-root mentioned in `§2.3` that appears in the steps becomes a system-component swimlane. Provenance `from-task-flow` if verbatim in §5, else `derived-from-§2`.
    - Every concept from `§2.1` that the actor interacts with directly becomes a system-component swimlane. Provenance `derived-from-§2`.
- **External-system swimlanes.** Walk the steps for terms that imply outside-the-system services (payment gateway, email service, identity provider, third-party API). If `§2` does not name them explicitly, propose as `ai-suggested` `external-system` swimlanes. Naming convention: `PascalCase` ending in a kind suffix (`PaymentGateway`, `NotificationSvc`, `IdentityProvider`).
- **Aggregate the global Swimlanes table.** A swimlane referenced across multiple flows appears once in the global table with a comma-separated `flows` field.
- **Cap rule on external swimlanes.** If proposed `ai-suggested` external-system swimlanes > 5 in a single run, surface a one-line note in diagnostics suggesting the consultant name them in `§2 Domain model` so they leave the `ai-suggested` density.

Output: the per-flow swimlane set + the global Swimlanes table. Update each flow's `actor` field with the actor swimlane id. **Every flow has ≥1 actor swimlane and ≥1 system-component swimlane.**

### Round 4 — Action extraction

Per **Quality checks 3, 4, 8**:

For every flow, walk the source `§5` task-flow *Steps* in order. Per step:

- **Identify the verb.** The step's verb phrase becomes the action label (e.g. "submit the order" → `submitOrder`). Strip articles and convert to lowerCamelCase. **Never** use `and` / `then` / `etc` as verbs.
- **Identify `owning_swimlane`.** The swimlane responsible for the step:
    - If the step's subject is the actor ("Owner submits..."), the owning swimlane is the actor swimlane.
    - If the step's subject is a system component verbatim ("OrderSvc validates..."), use that swimlane.
    - If the step names a domain object only ("submit the order"), use the aggregate-root component that owns the object (`Order` → `OrderSvc`).
    - If the step names an external service ("send notification email"), use the matching `external-system` swimlane.
- **Assign `seq`.** Sequential integer starting at 1 per flow.
- **Assign `id`.** `A-NN` (zero-padded) per flow.
- **Assign provenance.** `from-task-flow` if the verb+owning-swimlane pair is verbatim derivable from a single `§5` step; `derived-from-§N` if extracted from `§4`/`§6`; `ai-suggested` if the action is implicit routing (e.g., an implicit `validate()` between two stated steps).

Output: the actions list per flow. **Every flow has ≥1 action.**

### Round 5 — Action classification + owning-swimlane refinement

Per **Quality checks 4, 8**:

For every action, determine:

- **Kind.** One of:
    - `action` — default. An atomic step of work.
    - `decision-prep` — an action whose output is consumed by an immediately-following decision node (e.g., `evaluateAmount` preceding a decision on `amount > 10000`). Hint to Round 6 that a decision node follows.
    - `external-call` — an action whose owning swimlane is an `external-system`. Used by the renderer to apply distinct styling.
- **Owning-swimlane refinement.** Re-check Round 4 swimlane assignment against Round 3's swimlane set. If the assignment names a swimlane not in the flow's swimlane set, either:
    - Add the swimlane to the flow's swimlane set (if it's in the global Swimlanes table), or
    - Reassign the action to the nearest containing swimlane (typically the aggregate-root component), and mark the action `ai-suggested`.

Output: the actions list with `kind` and validated `owning_swimlane`.

### Round 6 — Control-flow node assembly

Per **Quality checks 5, 6, 7, 8**:

For every flow, build the control-node structure:

- **Initial node.** Exactly one per flow. Provenance:
    - `from-task-flow` if `§5` explicitly states a start ("Triggered when the user clicks Submit").
    - `ai-suggested` otherwise — most flows omit an explicit start.
- **Activity-final node.** At least one per flow. Provenance follows the same rule as initial; usually `ai-suggested` unless `§5` *Steps* explicitly states "the flow ends when...".
- **Flow-final nodes.** Per `§5` *Exception paths* clause that terminates a branch without ending the activity (e.g., "on validation failure, display error and abort"). One flow-final per terminating branch. Provenance `derived-from-§5`.
- **Decision nodes.** Per `§5` *Decision points* sub-cell clause and per `§6` constraint with explicit branches:
    - 1 incoming edge, ≥2 outgoing edges.
    - Each outgoing edge carries a non-empty `guard` expression (e.g., `valid` / `invalid`, `amount > 10000` / `amount ≤ 10000`).
    - Provenance `derived-from-§5` (from *Decision points* sub-cell) or `derived-from-§6` (from `§6` constraint).
- **Merge nodes.** Where decision branches converge:
    - ≥2 incoming edges, 1 outgoing edge.
    - Inferred at the smallest action-id span that covers all branches.
    - Provenance: `derived-from-§5` if `§5` explicitly names the re-convergence point; `ai-suggested` if inferred.
- **Fork nodes.** Per `§5`/`§6` clause stating parallelism ("concurrently", "in parallel", "while X, also Y"):
    - 1 incoming edge, ≥2 outgoing edges.
    - Provenance `derived-from-§5` (if verbatim) or `derived-from-§6`.
- **Join nodes.** Where parallel branches reconverge:
    - ≥2 incoming edges, 1 outgoing edge.
    - Every fork has a matching join unless one parallel branch terminates with a flow-final.
    - Provenance: `derived-from-§5` if `§5` names the synchronisation point; `ai-suggested` if inferred.
- **Build the edges list.** For every consecutive action-pair, control-node, and decision-out branch, emit an edge `{flow_id, source, target, guard, provenance}`. Guard is empty except on decision-out edges. Edge provenance matches the source action/node's provenance (fall back to `ai-suggested` if any endpoint is `ai-suggested`).

**Every node referenced in any edge must exist** in the flow's nodes list (check 8). **Every action's `owning_swimlane` must exist** in the flow's swimlanes set (also check 8).

Output: the control-nodes list + edges list per flow.

### Round 7 — Cross-flow consistency

Per **Quality checks 4, 9**:

- **Swimlane naming consistency.** A swimlane used in flow A as `OrderSvc` must be `OrderSvc` (not `OrderService`, not `Order Service`) in flow B. Pick the canonical name once (longest verbatim match in §2; else PascalCase of the §2 noun) and rewrite all flows.
- **Action-label reuse.** If two flows perform the same logical operation (`OrderSvc.submitOrder()`), the action label must be identical (`submitOrder`, not `submit` in one and `submitOrder` in another). Pick the canonical label once.
- **Pre-render layout sanity.** Count swimlanes per flow; if any flow has > 8 swimlanes, flag a soft layout warning in diagnostics ("Flow `submit-order` has 11 swimlanes — SVG height will be tall; consider decomposing into sub-flows"). Count actions per flow; if any flow has > 30 actions, flag a soft layout warning ("Flow `onboard-user` has 42 actions — SVG width will be wide; consider splitting").
- **Build the cross-flow swimlane matrix.** Pivot: matrix[swimlane][flow] = true if the swimlane appears in any action of that flow.

Output: normalised swimlane names + action labels across all flows; the cross-flow swimlane matrix.

---

## Provenance markers (3 — exhaustive)

Every flow, swimlane, action, control node, and edge carries exactly one of:

| Marker | CSS class | When |
|---|---|---|
| `from-task-flow` | `.provenance-from-task-flow` | Content appears verbatim in a `§5 Task flows` step. Analogous to `from-domain-model` in data-model. |
| `derived-from-§N` | `.provenance-derived` | Content was extracted from a named section (`§2`, `§3`, `§4`, `§6`, `§7`) but is not verbatim in `§5`. The source section is recorded in a `data-source="§N"` attribute on the row. |
| `ai-suggested` | `.provenance-ai-suggested` | Content was inferred (e.g., an inferred initial/final marker, an inferred merge after if/else, an inferred join after fork, an inferred swimlane for an ambiguous action). Prefixed with `[AI-SUGGESTED]` in the text content. |

No fourth marker. No item unmarked. Honours the framework-wide `[AI-SUGGESTED]` invariant — the marker is reserved for facts not traceable to inputs.

---

## Quality checks (10 hard gates)

All checks operate on the catalogue — they are **independent of which flows the consultant selects for rendering**. The catalogue must be valid regardless of presentation.

1. **Every flow has a kebab-case id and a display name.** Both non-empty; id matches `[a-z0-9-]+`.
2. **Every flow has ≥1 actor swimlane and ≥1 system-component swimlane.** A flow with zero actor or zero system swimlanes cannot represent a business process with responsibility partitioning.
3. **Every flow has ≥1 action, exactly one initial node, and ≥1 final node (`activity-final` or `flow-final`).** A flow with zero actions or zero initial/final markers is structurally incomplete.
4. **Every action has a non-empty `label` (lowerCamelCase verb-phrase) and an `owning_swimlane`.** Labels are lowerCamelCase verb-phrases; forbidden values include `and`, `then`, `etc`, empty string. `owning_swimlane` must reference a swimlane in the flow's swimlane set.
5. **Every edge's `source` and `target` reference existing node ids in the flow.** Cross-check against the flow's nodes set (actions + control nodes built in Rounds 4–6).
6. **Every decision node has ≥2 outgoing edges, each with a non-empty guard expression.** Guard is non-empty string; outgoing-edge count ≥ 2.
7. **Every fork node has ≥2 outgoing edges; every join node has ≥2 incoming edges; forks and joins are matched.** Any fork in a flow has a corresponding join, unless one parallel branch terminates with a flow-final.
8. **Every node referenced in any edge appears in the flow's nodes list; every action's `owning_swimlane` appears in the flow's swimlanes set.** Cross-check actions, control nodes, swimlanes.
9. **Every swimlane referenced in ≥1 flow appears in the global Swimlanes table.** Cross-check per-flow swimlane sets vs the global table.
10. **Every row in every Tier-1 table carries exactly one provenance marker** (`from-task-flow` / `derived-from-§N` / `ai-suggested`) — never zero, never two.

**Soft check (warning, not gate):**

- **AI-SUGGESTED density.** Compute `density_actions = ai_suggested_actions / total_actions`. If > 50%, emit a `density-warning` line in diagnostics and the handback summary: *"`§5 Task flows` is thin — most actions were inferred. Enrich `§5` and re-run for higher-confidence flows."* Does not block writing.

---

## Flow-selection sub-step

After all 10 hard checks pass (or the consultant chose Override at Step 8), the analyser surfaces a single `AskUserQuestion` with `multiSelect: true`:

- **Question:** *"The activity-diagram catalogue has been extracted and validated. Which flows should be rendered as inline-SVG diagrams? Pick none, one, several, or all — the catalogue tables above are always rendered."*
- **Header:** `Diagrams`
- **Options:** one option per discovered flow, labelled `<display_name> — <type> (<action_count> actions)`. Default ordering: `primary` first, then `extension`, then `recovery`; alphabetical within each group. The first option is suffixed `(Recommended)` if it is the highest-action-count `primary` flow.

Empty selection is **valid**. Cancelling the prompt outright (closing the dialog rather than submitting an empty selection) hands control back to the accept/revise/restart loop, not to silent emission.

---

## Stop-condition

The analysis is complete when:

- Every task flow declared in `§5` (or derived from §4/§6 when §5 is absent) has a row in the Flows table with at least one action, one initial node, and one final node.
- Every swimlane referenced in any flow appears in the global Swimlanes table.
- Every decision node has ≥2 guarded outgoing edges.
- Every fork is matched with a join (or one branch terminates in a flow-final).
- All 10 hard quality checks pass, or the consultant chose Override.
- The consultant chose Accept in the Step 11 accept/revise/restart loop.

---

## Input-coverage asymmetry

`§5 Task flows` carries flow shape, action sequence, and actor cleanly. The columns it does **not** typically carry:

- **Initial / activity-final / flow-final markers.** Task-flow steps describe user-visible actions, not start/end markers. The analyser inserts one initial and ≥1 final per flow as `ai-suggested`.
- **Merge nodes after if/else.** Task flows describe the branches but rarely name the re-convergence point. The analyser infers a merge at the smallest action-id span covering all branches.
- **Join nodes after fork.** Task flows describe parallel work but rarely name the synchronisation point. The analyser pairs each fork with a join unless one branch terminates with a flow-final.
- **Swimlane assignment for "the system…" steps.** Task flows often say "the system validates" without naming the component. The analyser flattens to the aggregate-root naming (`§2.3`) and marks ambiguous assignments `ai-suggested`.
- **External-system swimlanes.** Payment gateways, email services, identity providers — rarely named in `§2`. Almost always `ai-suggested`.
- **Decision-node guard expressions.** `§6` carries the conditions (`if amount > 10000`); `§5` carries the steps. The analyser stitches them at Round 6.

Richer inputs → richer catalogue. Methodology degrades gracefully: with thin `§5`, the catalogue is mostly inferred and flagged.

---

## Output shape (HTML schema)

The artefact is a single self-contained HTML file at `analyse-requirements/ACTIVITY-DIAGRAM/activity-diagram.html`. The analyser populates `framework/assets/analyses/template-activity-diagram.html` via documented placeholder substitution. Every substituted value is HTML-escaped before injection (XML-escape inside `<svg><text>` nodes).

### Header placeholders

| Placeholder | Value |
|---|---|
| `{{TITLE}}` | *"Activity Diagrams — `<domain>`"* if `§1` declares a domain, else *"Activity Diagrams"*. |
| `{{DOMAIN}}` | Verbatim from `§1 Application context > Domain`, else *"(not declared in requirements.md)"*. |
| `{{GENERATED_AT}}` | ISO-8601 UTC, captured at render time. |
| `{{REQUIREMENTS_SHA256}}` | SHA-256 of `requirements/requirements.md` captured at Step 2. |
| `{{FLOW_COUNT}}` | Number of rows in the Flows table. |
| `{{SWIMLANE_COUNT}}` | Number of rows in the global Swimlanes table. |
| `{{ACTION_COUNT}}` | Number of rows in the Actions table (across all flows). |
| `{{CONTROL_NODE_COUNT}}` | Number of rows in the Control nodes table (across all flows). |
| `{{EDGE_COUNT}}` | Number of rows in the Edges table (across all flows). |
| `{{AI_SUGGESTED_COUNT}}` | Total items (flows + swimlanes + actions + control nodes + edges) marked `ai-suggested`. |
| `{{FLOWS_RENDERED}}` | Comma-separated list of flow display names whose SVG was emitted, or *"none — catalogue only"* if zero were selected. |

### Body placeholders

| Placeholder | Value |
|---|---|
| `{{DIAGNOSTICS_BLOCK}}` | Pre-rendered `<section class="diagnostics">` containing: counts summary line, per-marker provenance summary, the 10 check result lines (PASS/FAIL), the AI-SUGGESTED density-warning line (with `class="hidden"` if ≤ 50%), and (on Override runs) per-flagged-item lines. |
| `{{CATALOGUE_BLOCK}}` | Pre-rendered `<section class="catalogue">` containing the six Tier-1 tables in fixed order (Flows, Swimlanes, Actions, Control nodes, Edges, Cross-flow swimlane matrix). The diagnostics section is rendered separately via `{{DIAGNOSTICS_BLOCK}}` — not duplicated inside the catalogue block. |
| `{{SVG_DIAGRAMS_BLOCK}}` | Pre-rendered `<section class="activity-diagrams">` containing zero-to-N `<figure class="activity-diagram flow-{slug}">` blocks. If the consultant selected zero flows, this placeholder renders as a single `<p class="diagrams-empty">No diagrams were selected. The catalogue tables above are the deliverable.</p>`. |
| `{{MERMAID_BLOCK}}` | Pre-rendered `<details class="mermaid-source">` containing zero-to-N `<pre>` blocks: one Mermaid `flowchart TD` source per selected flow, in the same order as the SVG figures. If zero flows selected, renders as `<!-- no mermaid equivalents -->`. Mermaid does not have first-class activity diagrams; the analyser uses `flowchart TD` with one `subgraph` per swimlane as the canonical approximation, clearly labelled in a caption. |

### SVG conventions

- `viewBox="0 0 W H"` where `W` is computed from action count × `column_width` + padding, and `H` from swimlane count × `lane_height` + padding.
- `role="img"` + `aria-label="Activity diagram for <flow_display_name>"` on every `<svg>`.
- All `<text>` nodes XML-escape swimlane labels, action labels, and guard expressions.
- **Shared `lane_height` across all flows in a single render.** `lane_height = max(80, longest_swimlane_label_pixels + 40)` computed across the union of swimlanes from selected flows. This keeps swimlanes visually aligned when the consultant scrolls between figures.
- Arrowhead marker (`<defs><marker id="flow-arrow-{slug}">`) defined once per SVG.
- Action labels truncated to 40 chars with `<title>` tooltip carrying the full text.
- Decision-out edge guard labels are positioned at the midpoint of the edge with a small offset to avoid overlapping the arrow line.

### Layout grid (per SVG)

- **Swimlane bands.** `y_lane[k] = padding_y + k * lane_height` for swimlane index `k` (0-based, top-to-bottom: actor first, system-components middle, external-systems last). Each band has a left-side label column of fixed width `lane_label_width = 140`, then a horizontal divider line at `y = y_lane[k]` and `y = y_lane[k] + lane_height`.
- **Action columns.** Actions placed at `x = padding_x + lane_label_width + (col_index * column_width) + column_width/2` where `col_index` follows the topological order of the action graph (one column per discrete sequence position; parallel branches occupy the same column index but different lanes).
- **Action nodes.** Rounded rectangles, width `action_width = 140`, height `action_height = 36`, `rx="8"`. Centred at `(x_col, y_lane_centre)` where `y_lane_centre = y_lane[owning_swimlane] + lane_height/2`.
- **Decision / Merge nodes.** Diamonds, edge length `diamond_size = 36`. Centred at `(x_col, y_lane_centre)`.
- **Fork / Join bars.** Thick horizontal bars (height `bar_thickness = 4`, width `bar_width = column_width`). Centred at `(x_col, y_lane_centre)`. When a fork/join spans multiple lanes, the bar is drawn at the topmost lane and the outgoing/incoming edges fan out vertically.
- **Initial node.** Small filled circle, radius `r = 8`. Drawn at the first column of the first flow lane.
- **Activity-final node.** Bullseye: outer circle `r = 10` (open), inner circle `r = 5` (filled).
- **Flow-final node.** Circle `r = 9` (open) with an X through it (two lines from corners).
- **Control-flow edges.** Polylines: source's right edge → 1-2 vertical/horizontal segments → target's left edge, with an arrowhead marker. Edges crossing swimlane boundaries draw vertical segments at the column boundary (between `x_col_source` and `x_col_target`) so the line clearly separates source and target lanes.
- **Edge guards.** `<text class="edge-guard">{guard}</text>` placed at the midpoint of the edge polyline with a small background `<rect class="edge-guard-bg">` for legibility.

### CSS class contract used by the analyser

The template scaffold owns CSS variables, layout, and typography. The analyser emits HTML using the following named classes:

- `.catalogue` — outer container for Tier 1 tables.
- `.flows-table`, `.swimlanes-table`, `.actions-table`, `.control-nodes-table`, `.edges-table`, `.matrix-table` — one per Tier-1 section.
- `.activity-diagrams` — outer container for Tier 2 figures.
- `.activity-diagram` — applied to every `<figure>`; one `.flow-{slug}` modifier per flow.
- `.diagrams-empty` — applied to the `<p>` when zero flows selected.
- `.flow-diagram`, `.swimlane`, `.swimlane-label`, `.swimlane-divider`, `.action-node`, `.action-label`, `.decision-node`, `.merge-node`, `.fork-bar`, `.join-bar`, `.initial-node`, `.final-node`, `.flow-edge`, `.edge-guard`, `.edge-guard-bg` — inside SVG.
- `.action-kind-action`, `.action-kind-decision-prep`, `.action-kind-external-call` — applied to action nodes per kind.
- `.kind-actor`, `.kind-system-component`, `.kind-external-system` — pill badges in the swimlanes table.
- `.flow-type-primary`, `.flow-type-extension`, `.flow-type-recovery` — pill badges in the flows table.
- `.node-type-initial`, `.node-type-activity-final`, `.node-type-flow-final`, `.node-type-decision`, `.node-type-merge`, `.node-type-fork`, `.node-type-join` — pill badges in the control-nodes table.
- `.provenance-from-task-flow`, `.provenance-derived`, `.provenance-ai-suggested` — exactly one per content row in any table.
- `.ai-suggested` — applied to any cell whose content carries the `[AI-SUGGESTED]` prefix. Renders italic + dim background.
- `.matrix-cell-present`, `.matrix-cell-absent` — matrix table cell variants.
- `.mermaid-source` — applied to the `<details>` wrapping the Mermaid `<pre>` blocks.
- `.rev-marker` — applied to any row flagged by a failed quality check on an Override run.

The analyser does **not** edit the template's CSS or layout — only the documented `{{placeholders}}` are substituted.

---

## Downstream consumption (handled by `framework/skills/map-activity-diagram-to-ui.md`)

- **Flows** → screen-flow inventory. Each `primary` flow maps to a sequence of screen transitions in the design spec, one screen per action group within an actor swimlane.
- **Swimlanes** → component-ownership hints for the design system: actor swimlane = user-facing surface area; system-component swimlane = backend integration point; external-system swimlane = third-party integration boundary.
- **Decision nodes** → branching UI affordances (conditional sections, gated CTAs, decision modals — one branch per outgoing guard).
- **Merge nodes** → re-convergence UI patterns where divergent states funnel back to a shared screen.
- **Fork nodes** → parallel UI patterns (split panes, concurrent progress bars, batch dashboards).
- **Join nodes** → synchronisation UI affordances (wait-for-all indicators, "all approvals received" gates).
- **Cross-flow swimlane matrix** → component-reuse hints (a swimlane present in 5+ flows warrants a first-class shared component in the design system).

`framework/skills/map-activity-diagram-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character file and for future downstream design-spec authors.
