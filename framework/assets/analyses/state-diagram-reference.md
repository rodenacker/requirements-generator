<!-- ROLE: asset (analysis reference). Methodology definition for the state-diagram analyser. Modelled on framework/assets/analyses/activity-diagram-reference.md. Industry framing: OMG UML 2.5 § 14 (Behavior StateMachines) — one diagram per stateful entity (aggregate root or status-bearing entity), states × transitions × triggers × guards × effects × entry/exit/do activities. -->

# State Diagram analysis reference

> **Method:** Extract a **per-entity state-diagram catalogue** (entities, states, internal activities, transitions, events, cross-entity state coverage matrix) from `requirements/requirements.md` once. The tabular catalogue is always rendered. The consultant then picks **none, one, several, or all** of the discovered entities to add as inline-SVG `<figure>` blocks. Same data, the visuals are views onto the state machines already listed in the catalogue.

**Output file:** `analyse-requirements/STATE-DIAGRAM/state-diagram.html` — a self-contained HTML artefact containing the per-entity tabular catalogue (always) plus zero or more inline-SVG state-diagram figures (per consultant selection). No external CSS/JS dependencies; viewable by opening `file://` in a browser.

**Analyser agent:** `framework/agents/analyses/state-diagram-analyser.md`

**Character:** `framework/assets/characters/state-diagram-analysis.md`.

---

## Industry framing — UML 2.5 state-machine subset

Per OMG UML 2.5 § 14 (Behavior StateMachines), a state diagram models the lifecycle of an instance: discrete states with internal activities, plus transitions triggered by events, optionally guarded by boolean expressions, optionally performing effects. The full UML notation is rich (orthogonal regions, history pseudostates, submachine states, deferred events, protocol state machines, entry/exit points, terminate pseudostate, change/time events, signal-receipt actions). This methodology restricts the subset to elements that map cleanly to requirements text:

| Element | UML name | Included | Why included / why excluded |
|---|---|---|---|
| Simple state | State | yes | One per named lifecycle phase in `§2.3 Aggregates & lifecycles` or per enum value in a `§7` status field. |
| Composite state | State (with region) | yes | One level of nesting only. Useful when `§2.3` describes a phase that contains sub-phases (`Approved` containing `Awaiting-funding` then `Funded`). |
| Initial pseudostate | Pseudostate (kind=initial) | yes | Exactly one per entity. Often inferred (`ai-suggested`) when `§2.3` starts the lifecycle at the first named state without an explicit start marker. |
| Final state | FinalState | yes | One or more per entity. Terminates the lifecycle. Inferred where `§2.3` does not name an explicit terminus. |
| Choice pseudostate | Pseudostate (kind=choice) | yes | Diamond. Dynamic conditional branching where the guard is evaluated at run time after a preceding action computes the value. From `§5` *Decision points* or `§6` constraints. |
| Junction pseudostate | Pseudostate (kind=junction) | yes | Small filled circle. Static merge where multiple transitions converge to one outgoing path. Inferred where two or more source states transition to the same target via different triggers. |
| Transition | Transition | yes | From `§5 Task flows` step verbs, `§4` user-initiated actions, and `§6` rule-driven changes. Carries `trigger [guard] / effect`. |
| Entry activity | Behavior (entry) | yes | From `§2.3` clauses like *"on entering Submitted, notify the supplier"*. Often `ai-suggested` when not stated. |
| Exit activity | Behavior (exit) | yes | From `§2.3` clauses like *"on leaving Draft, lock for editing"*. Often `ai-suggested`. |
| Do activity | Behavior (doActivity) | yes | From `§2.3` clauses describing ongoing behaviour while in a state (*"while Processing, periodically poll the gateway"*). Often `ai-suggested`. |
| Internal (on-event) transition | InternalTransition | yes | An event handled inside a state without leaving it (`on heartbeat / refreshTimer`). From `§5` or `§6` clauses naming intra-state event handling. |
| Orthogonal region | Region (parallel) | **no — MVP** | Concurrent sub-state machines (a `Subscription` simultaneously `Billed` and `Provisioned`). Almost never anchored in requirements; raises `ai-suggested` density. Revisit post-MVP. |
| History pseudostate (shallow / deep) | Pseudostate (kind=shallowHistory / deepHistory) | **no — MVP** | Resume-from-where-you-left-off semantics. Useful but rarely named explicitly in `§2.3`; would force inference of resume points. Defer. |
| Submachine state | State (with submachine ref) | **no — MVP** | A state machine nested inside another state. Adds composition richness; deferred to a later release when nesting depth is consultant-driven. |
| Entry point / Exit point | Pseudostate (kind=entryPoint / exitPoint) | **no — MVP** | Composite-state-boundary connection points. Method-level fidelity; out of scope. |
| Terminate pseudostate | Pseudostate (kind=terminate) | **no — MVP** | Instance destruction. Indistinguishable from a Final state at requirements fidelity. |
| Deferred events | DeferredEventKind | **no — MVP** | Events held until the entity reaches a state that can handle them. Implementation detail. |
| Protocol state machine | ProtocolStateMachine | **no — MVP** | Behavioural state machines only. |
| Change event | ChangeEvent | yes (as `change-event` event kind) | A transition triggered by a boolean expression becoming true. Recognisable in `§6` constraints. |
| Time event | TimeEvent | yes (as `time-event` event kind) | A transition triggered by elapsed time or a clock. Recognisable in `§6` clauses (*"after 30 days of inactivity"*). |

System-level fidelity: state machines are per **aggregate root** (from `§2.3 Aggregates & lifecycles`) and per **status-bearing entity** (from `§7 Data entities` when the entity carries a `status` field with an enum). Per-attribute or per-method state machines are out of scope — most rows would be `ai-suggested` (design speculation), which degrades the audit trail.

---

## Output structure

The artefact has two tiers:

### Tier 1 — State-diagram catalogue (always rendered)

Seven tabular sections, in this order (six catalogue blocks + one diagnostics block):

1. **Entities table** — `id` (kebab-case aggregate or entity name), `display_name` (PascalCase), `kind` (`aggregate` / `entity`), `source` (`§2.3.N` aggregate id, `§7.N` entity id, or `derived`), `state_count`, `transition_count`, `provenance`.
2. **States table** — `entity_id`, `id` (`S-NN` zero-padded within entity), `display_name` (sentence-case or canonical enum value), `kind` (`initial` / `simple` / `composite` / `final` / `choice` / `junction`), `parent` (composite parent state id, or empty), `notes`, `provenance`.
3. **Internal activities table** — `entity_id`, `state_id`, `kind` (`entry` / `exit` / `do` / `on-event`), `event` (for `on-event` only; references an `events.id`; empty for entry/exit/do), `action` (lowerCamelCase verb-phrase), `provenance`.
4. **Transitions table** — `entity_id`, `id` (`T-NN` zero-padded within entity), `source` (state id), `target` (state id), `trigger` (event id; empty only when `guard` is non-empty — see check 5), `guard` (boolean expression; empty when not present), `effect` (lowerCamelCase verb-phrase; empty when not present), `notes`, `provenance`.
5. **Events table** — `id` (kebab-case), `display_name` (sentence-case), `kind` (`user-action` / `system-event` / `time-event` / `change-event`), `used_in_entities` (comma-separated entity ids), `source` (`§2.3.N` / `§5.N` / `§4.N` / `§6.N` / `derived`), `provenance`.
6. **Cross-entity state coverage matrix** — pivoted view: rows = entities, columns = canonical lifecycle phases (`created`, `active`, `suspended`, `closed`, `cancelled`, `failed`, `archived`), cell = name of the entity's state that maps to that phase (or em-dash if absent). Helps the consultant spot entities with gaps (`Order` has `active` but no terminal state) or inconsistent lifecycle vocabulary across the domain.
7. **Diagnostics block** — counts summary, per-marker provenance summary, the 10 check result lines (PASS / FAIL), the density-warning line.

Platform-agnostic. No DBMS-specific types appear in any column.

### Tier 2 — Inline-SVG state diagrams (0..N, consultant-selected)

After the catalogue is extracted, the analyser surfaces a `multiSelect: true` prompt with one option per discovered entity. The consultant picks any combination:

- **Empty selection is valid** — produces a catalogue-only output (Tier 1 only, no SVG blocks). The tabular catalogue is itself a recognised deliverable form.
- **Single selection** — one `<figure class="state-diagram entity-{slug}">` with one inline `<svg>`.
- **N selections** — N figures, one per selected entity. All figures share a common visual style (state-rectangle width, padding, font sizes, arrow geometry) so the consultant can compare entity lifecycles side-by-side.

Each SVG carries:

- **State nodes** — rounded rectangles (`rx="12"`). State name centred. Entry/exit/do activities listed in a sub-compartment beneath the name.
- **Composite states** — outer rounded rectangle with a horizontal divider; nested substate rectangles drawn inside.
- **Initial pseudostate** — small filled black circle.
- **Final state** — bullseye (filled inner circle inside open outer circle).
- **Choice pseudostate** — diamond.
- **Junction pseudostate** — small filled black circle (smaller than initial; distinguished by sizing and incoming/outgoing edge counts).
- **Transitions** — arrows from source to target, label `trigger [guard] / effect` placed at the arrow midpoint with a small background rectangle for legibility.
- **Self-transitions** — small loop drawn off the right edge of the source state, label positioned to the right of the loop.

---

## Source-of-truth hierarchy

The analyser walks `requirements/requirements.md` in this order:

1. **`§2.3 Aggregates & lifecycles`** — primary. Each aggregate root becomes a candidate entity. State names mentioned in the lifecycle text (*"draft → submitted → approved"*) become candidate states. Inline phrases like *"on entering Submitted, …"* become entry activities; *"while Processing, …"* become do activities. Transitions stated verbatim (*"a Draft order becomes Submitted when the user clicks Submit"*) become candidate transitions with `trigger = clickSubmit`.
2. **`§7 Data entities`** — supplementary. Every entity carrying a `status` field with an enum becomes a candidate entity if not already discovered via `§2.3`. Enum values become candidate states; provenance `derived-from-§7`.
3. **`§9 Key terminology`** — definitions of state names (when `§9` defines `Draft` as *"an order being assembled and not yet submitted"*) anchor state semantics. Used to disambiguate synonyms (`active`/`enabled`/`live`).
4. **`§5 Task flows`** — primary for transitions. Each task-flow step that moves an entity between states is a candidate transition. The step's verb phrase becomes the `trigger` event (lowerCamelCase); the actor becomes the event's `user-action` kind; the entity affected becomes the transition's owning entity. Steps that perform an action *within* a state (without state change) become candidate `on-event` internal activities.
5. **`§4 User goals & stories`** — supplementary for user-initiated triggers. Stories whose verb phrase moves an entity between states surface as candidate transitions when not already captured by `§5`. Provenance `derived-from-§4`.
6. **`§6 Requirements`** — primary for guards and constraints. Rules of the form *"only orders with status=Draft can be edited"* anchor guard expressions on transitions. Rules of the form *"after 30 days of inactivity, an account becomes Suspended"* anchor `time-event` triggers. Rules of the form *"when the inventory drops to zero, the listing becomes Sold-out"* anchor `change-event` triggers.
7. **`§3 Target users`** — supplementary. Persona ids inform the `user-action` event kind classification when a transition's trigger originates from a specific persona.
8. **Inference** — only for required pseudostates (initial, final) and obviously-missing transitions. Inferred items carry the `ai-suggested` marker and the `[AI-SUGGESTED]` text prefix.

If `§2.3 Aggregates & lifecycles` is absent or empty, the analyser degrades gracefully to `§7` status-field enums + `§5`/`§6` derivation. Density of `ai-suggested` markers will be high; the soft warning surfaces this in diagnostics.

---

## Seven-round discipline

Each round produces a distinct, named in-memory output. The analyser does not write the artefact until Round 7 is complete and all 10 hard quality checks have passed (or the consultant chose Override).

### Round 1 — Entity discovery (exploratory and inclusive)

- Walk `§2.3 Aggregates & lifecycles`: every aggregate root is a candidate entity `{candidate_id, candidate_display_name, source: "§2.3.N", source_line_offset, kind: "aggregate"}`.
- Walk `§7 Data entities`: every entity carrying a `status` field (or any field whose values name an enum of lifecycle phases) is a candidate entity with `kind: "entity"`. Provenance `derived-from-§7`.
- Walk `§2.1 Concepts` for nouns that have lifecycle verbs applied to them in `§5` (e.g. *"submit", "approve", "cancel"* applied to *"Invoice"*) — surface as candidate entities only if not already captured.

Output: candidate entity list. **Cap rule:** if the candidate list exceeds 12 entities, state the cap aloud (*"Selecting 8 of 14 candidate entities: the 6 from §2.3 aggregate roots plus 2 from §7 status-bearing entities with the densest state transitions. Discarded: …"*) and surface the top 8 by transition density.

### Round 2 — Entity refinement (decisive)

Per **Quality checks 1, 2**:

- **Merge synonyms.** When candidates describe the same entity (`order`, `purchase-order`, `po`), pick the canonical id from `§2.3` if present, else from the most-frequent occurrence. Record the alias in the entity's notes field.
- **Classify kind.** Each entity is one of:
    - `aggregate` — root entity from `§2.3 Aggregates & lifecycles`. Owns the action surface in DDD-style architectures.
    - `entity` — status-bearing entity from `§7` that is not an aggregate root (typically a child entity with its own lifecycle).
- **Assign kebab-case id and PascalCase display name.** Id: `order`, `subscription`, `invoice`, `support-ticket`. Display name: `Order`, `Subscription`, `Invoice`, `SupportTicket`.
- **Assign provenance marker** per the three-marker contract (see Provenance markers below).
- **Drop candidates** that cannot be sourced to `§2.3`, `§7`, or `§2.1` + `§5` after merging.

Output: the entity list as `[{id, display_name, kind, source, source_line_offset, provenance, notes}]`. Entity IDs are kebab-case; uniqueness is enforced.

### Round 3 — State extraction

Per **Quality checks 1, 2, 9, 10**:

For each entity, build the state set:

- **Primary source — `§2.3` lifecycle text.** Each named lifecycle phase becomes a state. The first state mentioned in the lifecycle is a candidate initial; the last is a candidate final unless `§2.3` names an explicit terminus. State display names use the canonical capitalisation from `§2.3`. Provenance `from-lifecycle` when verbatim.
- **Secondary source — `§7` status-field enum.** Each enum value of an entity's status field becomes a state if not already captured. Provenance `derived-from-§7`.
- **Definitions from `§9`.** Where `§9` defines a state-name term (e.g. *"Suspended: an account that cannot be used until the suspension is lifted"*), record the definition in the state's `notes` field. This does not add new states; it anchors existing ones.
- **Initial pseudostate.** Exactly one per entity. Add as a separate state with `kind: "initial"` and `id: "S-init"`. Provenance:
    - `from-lifecycle` if `§2.3` explicitly states *"a new Order starts in Draft"*.
    - `ai-suggested` otherwise (most lifecycles begin at the first named state without an explicit start marker).
- **Final states.** At least one per entity unless the lifecycle is purely cyclic (proven by transition graph). Add as states with `kind: "final"`. Provenance:
    - `from-lifecycle` if `§2.3` names an explicit terminus (*"Archived is terminal — no transitions out"*).
    - `derived-from-§7` if the enum has a clearly-terminal value (`Cancelled`, `Closed`, `Archived`).
    - `ai-suggested` otherwise.
- **Composite states.** A state mentioned in `§2.3` as containing sub-phases (*"Approved → Awaiting-funding → Funded → Active"* where Approved encloses the sub-states) becomes a composite. One level of nesting only — nested composites are not emitted. Sub-states carry the composite's id in their `parent` field. Provenance `from-lifecycle`.
- **Choice / Junction pseudostates.** Choice nodes are added in Round 4 when transitions branch on dynamic conditions. Junction nodes are added when multiple transitions converge to the same target via different triggers (Round 6).

Per state: `{entity_id, id, display_name, kind, parent, notes, provenance}`. State IDs are zero-padded `S-NN` within the entity (e.g. `S-01`, `S-02`); the initial is `S-init` and finals are `S-final-NN`.

Output: per-entity state set. **Every entity has ≥1 state, exactly one initial pseudostate, and ≥1 final state (unless the lifecycle is purely cyclic).**

### Round 4 — Transition extraction

Per **Quality checks 4, 5, 6, 8**:

For every entity, walk `§5 Task flows`, `§4`, `§2.3`, and `§6` for clauses that move the entity between states:

- **Source — `§2.3` verbatim transitions.** Phrases like *"a Draft order becomes Submitted when the user clicks Submit"* yield a transition `{source: draft, target: submitted, trigger: clickSubmit}`. Provenance `from-lifecycle`.
- **Source — `§5 Task flows` steps.** Each step that changes the entity's state contributes a transition. The step's verb-phrase becomes the `trigger` event id (lowerCamelCase, kebab-cased to event id). Example: a `§5.2` step *"the Owner submits the order"* yields a transition from `draft` to `submitted` with `trigger = submit`. The owning persona's id classifies the event as `user-action`. Provenance `from-lifecycle` if the source/target states are named verbatim in `§5`; `derived-from-§5` if only the trigger is in `§5` and the source/target states are inferred from `§2.3`.
- **Source — `§4 User goals & stories`.** Stories with verb phrases that move an entity between states yield transitions not already in `§5`. Provenance `derived-from-§4`.
- **Source — `§6 Requirements` rule-driven changes.** Rules of the form *"after 30 days of inactivity, an account becomes Suspended"* yield a transition `{source: active, target: suspended, trigger: timer-30d, kind: time-event}`. Rules of the form *"when the inventory drops to zero, the listing becomes Sold-out"* yield a transition with `trigger: inventoryZero, kind: change-event`. Provenance `derived-from-§6`.
- **Choice pseudostates.** When a transition branches on a dynamic condition (one trigger, two or more guards), insert a `kind: "choice"` pseudostate between the source state and the targets. Each outgoing edge of the choice carries a `guard`. Example: trigger `submit` from `draft` either goes to `pending-payment` (guard `items.size > 0`) or back to `draft` (guard `items.size == 0`) — insert a choice node. Provenance `derived-from-§5` (or `derived-from-§6` if the condition comes from a `§6` constraint).
- **Junction pseudostates.** When multiple source states transition to the same target via *different* triggers, optionally insert a junction node to share the incoming arrow head. Inferred (`ai-suggested`) — junctions are a visual simplification, not a semantic requirement.
- **Effects.** Where `§5` or `§6` names an action performed *during* the transition (*"on submitting, charge the payment method"*), record it as the transition's `effect` (lowerCamelCase verb-phrase). Provenance follows the trigger's provenance.
- **Internal (on-event) transitions vs external transitions.** A step that updates the entity *without* changing its state (*"while Active, the user can update billing details"*) is an `on-event` internal activity (Round 5), not a transition. A step that changes the state is a transition.

Per transition: `{entity_id, id, source, target, trigger, guard, effect, notes, provenance}`. Transition IDs are zero-padded `T-NN` within the entity. Trigger references an event id (resolved in Round 6); guard is a boolean expression text; effect is a lowerCamelCase verb-phrase.

Output: the transitions list per entity. **Every entity has ≥0 transitions; an entity with zero transitions is allowed only when the state set has exactly one state (a degenerate entity) — flagged as `ai-suggested` density.**

### Round 5 — Internal-activity extraction

Per **Quality check 4**:

For every state, walk `§2.3` and `§5`/`§6` for clauses that describe behaviour while in the state:

- **Entry activity.** A clause like *"on entering Submitted, notify the supplier"* yields an internal activity `{kind: entry, state: submitted, action: notifySupplier}`. Provenance `from-lifecycle`.
- **Exit activity.** A clause like *"on leaving Draft, lock for editing"* yields `{kind: exit, state: draft, action: lockForEditing}`. Provenance `from-lifecycle`.
- **Do activity.** A clause like *"while Processing, periodically poll the gateway"* yields `{kind: do, state: processing, action: pollGateway}`. Provenance `from-lifecycle`.
- **On-event internal transitions.** A clause like *"while Active, the user can update billing details — this does not change state"* yields `{kind: on-event, state: active, event: updateBilling, action: updateBillingDetails}`. Provenance `from-lifecycle` or `derived-from-§5`.

Each internal-activity row: `{entity_id, state_id, kind, event, action, provenance}`. The `event` column is empty for entry/exit/do; it references an event id for `on-event`.

Most internal activities are `ai-suggested` when `§2.3` doesn't state them — entry/exit/do behaviour is rarely fully specified in requirements. If density of `ai-suggested` internal activities is high, that is fine — internal activities are an enrichment of the state-machine, not its skeleton, and the soft density check (Round 7) does not include internal activities in its denominator.

Output: the internal-activities list. May be empty for any state.

### Round 6 — Event consolidation

Per **Quality checks 4, 7, 8**:

For every transition's `trigger` and every internal activity's `event`, consolidate the event catalogue:

- **Collect every distinct trigger/event id.** Deduplicate by id (case-sensitive). An event referenced by both an entity transition and an entity's `on-event` internal activity is one event row.
- **Assign `display_name`.** Sentence-case version of the event id (`click-submit` → `Click submit`; `inventory-zero` → `Inventory drops to zero`).
- **Classify `kind`.** One of:
    - `user-action` — triggered by a persona (`§3`). Recognisable by `§5` step subjects like *"the Owner clicks…"*, *"the customer submits…"*.
    - `system-event` — triggered by another part of the system (a different aggregate's transition, a domain event, a workflow step). Recognisable by `§5` step subjects like *"OrderSvc emits…"*, *"the payment gateway returns…"*.
    - `time-event` — triggered by elapsed time. Recognisable by `§6` clauses like *"after N days"*, *"at midnight"*, *"every N hours"*. Id convention: `timer-NN-unit` (e.g. `timer-30d`).
    - `change-event` — triggered by a boolean expression becoming true. Recognisable by `§6` clauses like *"when the inventory drops to zero"*, *"when balance < threshold"*. Id convention: a kebab-case expression name (e.g. `inventory-zero`, `balance-below-threshold`).
- **Compute `used_in_entities`.** Comma-separated list of entity ids whose transitions or internal activities reference this event.
- **Assign `source`.** The first section where this event appears (`§2.3.N` / `§5.N` / `§4.N` / `§6.N` / `derived`).
- **Assign `provenance`.** Follows the source.

Per event: `{id, display_name, kind, used_in_entities, source, provenance}`. Event IDs are kebab-case.

Output: the global Events table. **Every event referenced as a transition trigger or an `on-event` internal-activity event appears here exactly once (check 7).**

### Round 7 — Cross-entity consistency

Per **Quality checks 8, 9, 10**:

Final normalisation before render:

- **State-name vocabulary consistency.** If `§9 Key terminology` defines `active`/`enabled`/`live` as synonyms, collapse them to the canonical term across all entities. If multiple entities use *"Suspended"* for visually-different lifecycle phases (an account suspension vs a subscription pause), keep them distinct but flag in diagnostics for consultant review.
- **Event-name reuse.** A trigger named `submit` in entity `order` is the same event as `submit` in entity `report` only if `§5`/`§6` indicates they are the same. If they are coincidentally identically named but semantically distinct, assign a more specific id (`submit-order` / `submit-report`).
- **Pre-render layout sanity.** Count states per entity; if any entity has > 12 states, flag a soft layout warning in diagnostics (*"Entity `support-ticket` has 17 states — SVG will be wide; consider decomposing the lifecycle into sub-phases via a composite state"*). Count transitions per entity; if any entity has > 30 transitions, flag a soft layout warning.
- **Build the cross-entity state coverage matrix.** Define seven canonical lifecycle phases: `created`, `active`, `suspended`, `closed`, `cancelled`, `failed`, `archived`. For each entity × phase, fill the matrix cell with the entity's state name that maps to that phase (best-fit by state name match: `Draft` → `created`; `Active`/`Live`/`Enabled` → `active`; `Paused`/`Suspended`/`On-hold` → `suspended`; `Closed`/`Completed` → `closed`; `Cancelled`/`Voided` → `cancelled`; `Failed`/`Errored` → `failed`; `Archived` → `archived`). Cells with no match show an em-dash.

Output: normalised state names + event ids across all entities; the cross-entity state coverage matrix.

---

## Provenance markers (3 — exhaustive)

Every entity, state, internal activity, transition, and event carries exactly one of:

| Marker | CSS class | When |
|---|---|---|
| `from-lifecycle` | `.provenance-from-lifecycle` | Content appears verbatim in `§2.3 Aggregates & lifecycles`. Analogue of `from-task-flow` in the activity-diagram analyser. |
| `derived-from-§N` | `.provenance-derived` | Content was extracted from a named section (`§2.1`, `§3`, `§4`, `§5`, `§6`, `§7`, `§9`) but is not verbatim in `§2.3`. The source section is recorded in a `data-source="§N"` attribute on the row. |
| `ai-suggested` | `.provenance-ai-suggested` | Content was inferred (e.g., an inferred initial/final pseudostate, an inferred junction, an inferred entry/exit activity, an inferred state for a non-self-terminating cycle). Prefixed with `[AI-SUGGESTED]` in the text content. |

No fourth marker. No item unmarked. Honours the framework-wide `[AI-SUGGESTED]` invariant — the marker is reserved for facts not traceable to inputs.

---

## Quality checks (10 hard gates)

All checks operate on the catalogue — they are **independent of which entities the consultant selects for rendering**. The catalogue must be valid regardless of presentation.

1. **Every entity has a kebab-case id, a PascalCase display name, and ≥1 state.** Id matches `[a-z0-9-]+`; display name non-empty; state count ≥ 1.
2. **Every entity has exactly one initial pseudostate.** Zero or two-plus initial pseudostates is a hard fail.
3. **Every entity has ≥1 final state OR a transition graph with a stable cycle** (every state is reachable from the initial and the graph has no terminal sink that lacks a final marker). A finite entity with no final and no cycle is structurally incomplete.
4. **Every state has ≥1 incoming or outgoing transition** (no orphan states; the initial pseudostate is excluded — it only has outgoing). A state with zero transitions is dead code in the lifecycle.
5. **Every transition has a trigger OR a guard (or both).** A transition with neither is a naked transition — meaningless. Internal `on-event` activities always have an event (trigger); entry/exit/do activities are not transitions and are exempt from this check.
6. **Every transition's source and target states belong to the same entity.** Cross-entity transitions are not modelled at MVP fidelity — they would require submachine states (deferred). A transition referencing a state outside the owning entity is a hard fail.
7. **Every event referenced as a transition trigger or an `on-event` internal-activity event appears in the Events table.** No dangling event references.
8. **No two transitions from the same source state share the same `(trigger, guard)` pair.** Deterministic dispatch: ambiguous transitions are a hard fail. (Choice pseudostates are a structured way to model conditional branching — multiple outgoing edges from a choice pseudostate are not duplicate transitions.)
9. **Every composite state contains ≥1 substate.** An empty composite is structurally invalid.
10. **Every state name is unique within its entity** (case-insensitive). Distinct states with the same display name within one entity are a hard fail. (Cross-entity reuse of state names is allowed — see Round 7 consistency normalisation.)

**Soft check (warning, not gate):**

- **AI-SUGGESTED density.** Compute `density_states = ai_suggested_states / total_states` and `density_transitions = ai_suggested_transitions / total_transitions` (excluding internal activities from both denominators — see Round 5). If either exceeds 50%, emit a `density-warning` line in diagnostics and the handback summary: *"`§2.3 Aggregates & lifecycles` is thin — most states/transitions were inferred. Enrich `§2.3` and re-run for higher-confidence lifecycles."* Does not block writing.

---

## Entity-selection sub-step

After all 10 hard checks pass (or the consultant chose Override at Step 8), the analyser surfaces a single `AskUserQuestion` with `multiSelect: true`:

- **Question:** *"The state-diagram catalogue has been extracted and validated. Which entities should be rendered as inline-SVG diagrams? Pick none, one, several, or all — the catalogue tables above are always rendered."*
- **Header:** `Diagrams`
- **Options:** one option per discovered entity, labelled `<display_name> — <kind> (<state_count> states, <transition_count> transitions)`. Default ordering: `aggregate` first, then `entity`; alphabetical within each group. The first option is suffixed `(Recommended)` if it is the highest-transition-count `aggregate` entity.

Empty selection is **valid**. Cancelling the prompt outright (closing the dialog rather than submitting an empty selection) hands control back to the accept/revise/restart loop, not to silent emission.

---

## Stop-condition

The analysis is complete when:

- Every aggregate root declared in `§2.3` (or derived from `§7` status-bearing entities when `§2.3` is absent) has a row in the Entities table with at least one state, exactly one initial pseudostate, and (typically) one final state.
- Every state referenced in any transition appears in the States table.
- Every event referenced in any transition trigger or `on-event` internal activity appears in the Events table.
- Every composite state contains at least one substate.
- All 10 hard quality checks pass, or the consultant chose Override.
- The consultant chose Accept in the Step 11 accept/revise/restart loop.

---

## Input-coverage asymmetry

`§2.3 Aggregates & lifecycles` carries state names, lifecycle shape, and (often) the most important transitions cleanly. The columns it does **not** typically carry:

- **Initial and final pseudostates.** `§2.3` typically lists the named lifecycle phases but rarely names an explicit start marker or terminus. The analyser inserts one initial per entity and (usually) ≥1 final per entity as `ai-suggested`.
- **Triggers for transitions.** `§2.3` names *that* a state changes; `§5 Task flows` names *what causes* the change. The analyser stitches them at Round 4.
- **Guards on transitions.** `§6 Requirements` carries the conditions (*"only orders with status=Draft can be edited"*); `§5` carries the steps. The analyser stitches them at Round 4.
- **Entry/exit/do activities.** Rarely fully specified. Most are `ai-suggested` unless `§2.3` is explicit.
- **Junction pseudostates.** Visual simplifications inferred at Round 6 — most are `ai-suggested`.
- **Time- and change-event triggers.** Anchored in `§6` constraints; the analyser classifies them at Round 6.

Richer inputs → richer catalogue. Methodology degrades gracefully: with thin `§2.3`, the catalogue is mostly inferred and flagged.

---

## Output shape (HTML schema)

The artefact is a single self-contained HTML file at `analyse-requirements/STATE-DIAGRAM/state-diagram.html`. The analyser populates `framework/assets/analyses/template-state-diagram.html` via documented placeholder substitution. Every substituted value is HTML-escaped before injection (XML-escape inside `<svg><text>` nodes).

### Header placeholders

| Placeholder | Value |
|---|---|
| `{{TITLE}}` | *"State Diagrams — `<domain>`"* if `§1` declares a domain, else *"State Diagrams"*. |
| `{{DOMAIN}}` | Verbatim from `§1 Application context > Domain`, else *"(not declared in requirements.md)"*. |
| `{{GENERATED_AT}}` | ISO-8601 UTC, captured at render time. |
| `{{REQUIREMENTS_SHA256}}` | SHA-256 of `requirements/requirements.md` captured at Step 2. |
| `{{ENTITY_COUNT}}` | Number of rows in the Entities table. |
| `{{STATE_COUNT}}` | Number of rows in the States table (across all entities, including initial/final pseudostates). |
| `{{TRANSITION_COUNT}}` | Number of rows in the Transitions table (across all entities). |
| `{{EVENT_COUNT}}` | Number of rows in the global Events table. |
| `{{AI_SUGGESTED_COUNT}}` | Total items (entities + states + internal activities + transitions + events) marked `ai-suggested`. |
| `{{ENTITIES_RENDERED}}` | Comma-separated list of entity display names whose SVG was emitted, or *"none — catalogue only"* if zero were selected. |

### Body placeholders

| Placeholder | Value |
|---|---|
| `{{DIAGNOSTICS_BLOCK}}` | Pre-rendered `<section class="diagnostics">` containing: counts summary line, per-marker provenance summary, the 10 check result lines (PASS/FAIL), the AI-SUGGESTED density-warning line (with `class="hidden"` if ≤ 50%), and (on Override runs) per-flagged-item lines. |
| `{{CATALOGUE_BLOCK}}` | Pre-rendered `<section class="catalogue">` containing the six Tier-1 tables in fixed order (Entities, States, Internal activities, Transitions, Events, Cross-entity state coverage matrix). The diagnostics section is rendered separately via `{{DIAGNOSTICS_BLOCK}}` — not duplicated inside the catalogue block. |
| `{{SVG_DIAGRAMS_BLOCK}}` | Pre-rendered `<section class="state-diagrams">` containing zero-to-N `<figure class="state-diagram entity-{slug}">` blocks. If the consultant selected zero entities, this placeholder renders as a single `<p class="diagrams-empty">No diagrams were selected. The catalogue tables above are the deliverable.</p>`. |
| `{{MERMAID_BLOCK}}` | Pre-rendered `<details class="mermaid-source">` containing zero-to-N `<pre>` blocks: one Mermaid `stateDiagram-v2` source per selected entity, in the same order as the SVG figures. Each `<pre>` is preceded by a `<div class="mermaid-caption">` naming the entity. If zero entities selected, renders as `<!-- no mermaid equivalents -->`. Mermaid `stateDiagram-v2` is a direct equivalent for UML state diagrams (unlike activity diagrams, which require a `flowchart TD` approximation). |

### SVG conventions

- `viewBox="0 0 W H"` where `W` is computed from layout columns × `state_width` + padding, and `H` from layout rows × `state_height` + padding plus internal-activity rows.
- `role="img"` + `aria-label="State diagram for <entity_display_name>"` on every `<svg>`.
- All `<text>` nodes XML-escape state names, transition labels, guards, effects, and internal-activity actions.
- Arrowhead marker (`<defs><marker id="state-arrow-{slug}">`) defined once per SVG.
- State names truncated to 28 chars in headers with `<title>` tooltip carrying the full name; internal-activity actions truncated to 32 chars.
- Transition labels (`trigger [guard] / effect`) positioned at the polyline midpoint with a small background rectangle for legibility.

### Layout grid (per SVG)

- **State nodes.** Rounded rectangles, default width `state_width = 160`, default height `state_height = 60` (taller when internal activities are present — height grows by 12px per internal-activity row up to a cap). `rx="12"`.
- **Composite states.** Outer rectangle with `state_width = 320` (twice default) and height to contain substates with 16px padding. Substates use default `state_width = 140`.
- **Initial pseudostate.** Small filled circle, radius `r = 8`. Placed top-left of the layout.
- **Final state.** Bullseye: outer circle `r = 12` (open), inner circle `r = 6` (filled).
- **Choice pseudostate.** Diamond, edge length `diamond_size = 32`.
- **Junction pseudostate.** Small filled circle, radius `r = 6` (smaller than initial; distinguished by sizing).
- **Layout algorithm.** Simple topological sort: states are placed in columns based on longest-path-from-initial; ties broken by transition density. Composite states occupy two adjacent columns (their substate sub-layout reuses the same algorithm internally).
- **Transitions.** Polylines from source state's right edge → 1-2 vertical/horizontal segments → target state's left edge, with arrowhead marker. Self-transitions draw a small loop off the right edge of the source state.
- **Transition labels.** `<text class="transition-label">{trigger} [{guard}] / {effect}</text>` placed at the polyline midpoint with `<rect class="transition-label-bg">` for legibility. Guard and effect omitted when empty.

### CSS class contract used by the analyser

The template scaffold owns CSS variables, layout, and typography. The analyser emits HTML using the following named classes:

- `.catalogue` — outer container for Tier 1 tables.
- `.entities-table`, `.states-table`, `.internal-activities-table`, `.transitions-table`, `.events-table`, `.matrix-table` — one per Tier-1 section.
- `.state-diagrams` — outer container for Tier 2 figures.
- `.state-diagram` — applied to every `<figure>`; one `.entity-{slug}` modifier per entity.
- `.diagrams-empty` — applied to the `<p>` when zero entities selected.
- `.state-node`, `.state-label`, `.state-activities`, `.composite-state`, `.composite-divider`, `.initial-node`, `.final-node`, `.final-outer`, `.final-inner`, `.choice-node`, `.junction-node`, `.transition-edge`, `.transition-label`, `.transition-label-bg` — inside SVG.
- `.state-kind-initial`, `.state-kind-simple`, `.state-kind-composite`, `.state-kind-final`, `.state-kind-choice`, `.state-kind-junction` — pill badges in the states table.
- `.activity-kind-entry`, `.activity-kind-exit`, `.activity-kind-do`, `.activity-kind-on-event` — pill badges in the internal-activities table.
- `.event-kind-user-action`, `.event-kind-system-event`, `.event-kind-time-event`, `.event-kind-change-event` — pill badges in the events table.
- `.entity-kind-aggregate`, `.entity-kind-entity` — pill badges in the entities table.
- `.provenance-from-lifecycle`, `.provenance-derived`, `.provenance-ai-suggested` — exactly one per content row in any Tier-1 table.
- `.ai-suggested` — applied to any cell whose content carries the `[AI-SUGGESTED]` prefix. Renders italic + dim background.
- `.matrix-cell-present`, `.matrix-cell-absent` — matrix table cell variants.
- `.mermaid-source` — applied to the `<details>` wrapping the Mermaid `<pre>` blocks.
- `.rev-marker` — applied to any row flagged by a failed quality check on an Override run.

The analyser does **not** edit the template's CSS or layout — only the documented `{{placeholders}}` are substituted.

---

## Downstream consumption (handled by `framework/skills/map-state-diagram-to-ui.md`)

- **Entities** → screen-state inventory. Each entity's state set defines the discrete screen states an entity-detail screen must support (a `Draft` screen-state shows the editor; an `Active` screen-state shows the read-only view with action affordances).
- **States** → conditional UI rendering. State value drives which buttons, fields, and panels are visible.
- **Transitions with `trigger.kind == user-action`** → action affordances (buttons, links, menu items). One affordance per user-initiated transition. The transition's `effect` informs success-state UI; the transition's `guard` informs the affordance's enabled/disabled state.
- **Transitions with `trigger.kind == time-event` or `change-event`** → backend automation hooks, not UI affordances. Surface as background-process indicators in the design spec.
- **Internal activities of kind `entry`/`exit`/`do`** → page lifecycle hooks (onMount / onUnmount / polling intervals) for the design system.
- **Composite states** → screen groupings (an Approved composite with substates Awaiting-funding / Funded / Active maps to a single screen with a sub-state indicator strip).
- **Guards** → form-level validation rules and affordance-level disabled states. A transition `submit` guarded by `[items.size > 0]` means the `Submit` button is disabled when the cart is empty.
- **Cross-entity state coverage matrix** → cross-entity navigation hints. Entities sharing canonical lifecycle phases (multiple things in `active`) suggest a unified status filter / dashboard pattern.

`framework/skills/map-state-diagram-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character file and for future downstream design-spec authors.
