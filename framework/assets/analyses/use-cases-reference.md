<!-- ROLE: asset (P2 analysis reference). Loaded by framework/agents/analyses/use-cases-analyser.md at activation. -->

# analyses/use-cases-reference.md

**Purpose:** Methodology reference for Use Cases analysis. Cockburn's *fully-dressed* template (*Writing Effective Use Cases*, 2000) is the canonical contract: every use case carries a primary actor, scope, sea-level classification, stakeholders, preconditions, success guarantees, minimal guarantees, trigger, main success scenario (numbered SVO steps), and extensions (numbered against main steps). Ivar Jacobson's *Use Case 2.0* (2011) layered an agile "slice" concept on top of the same template — the analyser produces the fully-dressed artefact; slicing is a delivery concern downstream. The analyser follows this document literally and exhaustively.

**Used by:**

- `framework/agents/analyses/use-cases-analyser.md` — drives the agent's six analytical rounds + quality-gate sweep + Round 7 UML diagram view derivation.
- `framework/skills/map-use-cases-to-ui.md` — uses the use-case map to derive screen + flow + guard + acceptance entries for downstream UI design consumption (stub).

**Output produced by the analyser:** `analyse-requirements/USE-CASES/use-cases-map.html` — self-contained HTML use-case card grid using `framework/assets/analyses/template-use-cases.html` as scaffold.

---

## Upstream input contract

Use Cases is a **behavioural lens** onto the BA's persona + task-flow + acceptance-criteria material. The analyser anchors on:

- `§Personas` — canonical source of **primary actors**. Each actor named in `§Personas` is a candidate primary-actor for a use case.
- `§Task flows` — canonical source of **main success scenarios**. Each task flow's step sequence maps directly to a UC's `main_steps[]`.
- `§User stories` — canonical source of **use-case titles** (the *"I want to <Y>"* clause becomes the active-verb UC title) and additional actors named only in stories.
- `§Goals` — supplementary source of use-case titles for business-level goals not anchored to a single user story.
- `§Acceptance criteria` — canonical source of **success guarantees** (postconditions on success); each AC maps to at least one UC's success guarantee.
- `§Constraints` — canonical source of **preconditions** (auth state, entity existence, capacity / format constraints) and **minimal guarantees** (data integrity, audit trail, no-partial-commit invariants).
- `§Risks`, `§Pains` — canonical source of **extensions** (alternative & exception flows derived from named failure modes and current-state breakdowns).
- `§Existing solutions`, `§Current process` — supplementary source of extensions where `§Risks` is sparse (current-state friction implies a likely failure mode in the new system).

If `§Personas` is absent or empty, the analyser falls back to extracting candidate actor names from `§Task flows`, `§User stories`, or running prose — flagging each fallback actor with the `derived-actor` provenance marker. The same fallback discipline applies to UC titles (`from-prose` marker when no §User stories / §Task flows / §Goals anchor exists) and to main flows (`flow-derived` marker when no §Task flows anchor exists).

---

## The Use Cases process

Six analytical rounds (1–6) plus one diagram-derivation round (7), executed in order. Rounds 1–6 produce the card grid and feed the quality-gate sweep; Round 7 derives the canonical UML use case diagram view from the gated card data after the sweep passes (or the consultant accepts Override). The analyser does not skip rounds and does not collapse rounds into a single pass — each round's output feeds the next, and round-by-round structure is what makes the methodology auditable.

### Round 1 — Actors & Scope

Read `requirements/requirements.md` in full. Extract every candidate actor and identify the system boundary.

**Actor sources, in priority order:**

1. `§Personas` — canonical primary actors.
2. `§Task flows` / `§User stories` — names referenced as the "user" / "actor" in story prefaces or step subjects.
3. `§1 Domain` / running prose — last resort; mark `derived-actor`.
4. `§Existing solutions` / `§Current process` — external systems referenced as supporting actors (integrations, third-party services).

**Actor role classification:**

- `primary` — the actor whose goal the UC achieves; one per UC.
- `secondary` — another human actor who participates in the flow (e.g., an approver).
- `supporting` — a system the UC depends on (e.g., a payment gateway, an authentication provider).

**System boundary signals:**

- `§Constraints` — explicit "the system shall" / "out of scope" statements.
- `§1 Domain` — entities the system owns vs. references.
- `§Existing solutions` / `§Current process` — systems we integrate with (outside the boundary).

**Output of Round 1:** an unfiltered candidate `{actor, role, actor_source, scope_signal}` list. Synonyms and near-duplicates are kept at this stage; deduplication happens in Round 2.

### Round 2 — Use Case Identification

For each `(primary_actor, user-goal)` pair, write a use-case title.

**Title format rules:**

- Active-verb + goal-noun: *"Submit expense claim"*, *"Approve purchase order"*, *"Reconcile bank statement"*.
- Forbidden vague verbs in the title: `manage`, `handle`, `process`, `do`, `work with`. *"Manage orders"* is not a use case — it is a feature category. Rewrite to the actual goal (*"Cancel an order"*, *"Re-route an order to a different warehouse"*).
- Forbidden affordance leak: the title names the goal, not the UI affordance (*"Click the submit button"* → *"Submit the claim"*).
- The title is the **completed** active verb form (*"Submit a claim"*, not *"Submitting a claim"* or *"Claim submission"*).

**Title source priority:**

1. `§User stories` — the *"I want to Y"* clause becomes the UC title (mark `from-user-stories`).
2. `§Task flows` — each flow's overall goal becomes a UC title (mark `from-task-flows`).
3. `§Goals` — business-level goals decompose into one or more UC titles (mark `from-goals`).
4. `§1 Domain` / running prose — last resort (mark `from-prose`).

**Filter rules:**

- Merge near-duplicate UCs (same primary actor, near-identical goal). Prefer the more specific title.
- If a story names a UI affordance (*"User clicks Approve"*), rewrite the goal (*"Approve the purchase order"*) and surface the rewrite count in the diagnostics block.

For every retained UC, write a one-line **goal in context** clause that situates the UC in the broader actor workflow: *"The Procurement Manager submits a purchase order against an approved supplier so the warehouse can fulfil a stock-out."* Goal-in-context anchors the UC to the actor's larger objective without leaking into preconditions or success guarantees.

**Output of Round 2:** the final UC list. Each row carries `{uc_id, title, primary_actor, goal_in_context, actor_provenance, goal_source}`. UC IDs are `UC-NN` zero-padded in discovery order.

### Round 3 — Levels & Stakeholders

Classify each UC at Cockburn's three sea-levels:

| Level | Visual | Definition | Step-count expectation |
|---|---|---|---|
| `summary` | kite | A multi-UC business process that orchestrates several user-goal UCs. *"Procure stock for the next quarter"*. | 3–9 steps, each referencing another UC by ID. |
| `user-goal` | sea | A single sitting; one primary actor; the actor walks away with the goal achieved or explicitly abandoned. *"Submit purchase order"*. **Default classification for ambiguous cases.** | 3–9 SVO steps. |
| `subfunction` | fish | A sub-step shared across multiple user-goal UCs (e.g., *"Authenticate"*, *"Resolve supplier address"*). | 1–3 SVO steps. |

**Classification heuristic:**

- If the UC completes when the actor walks away satisfied (in a single sitting), it is `user-goal`.
- If the UC spans multiple sittings / multiple actors / multiple user-goal UCs, it is `summary`.
- If the UC's only purpose is to support other UCs (no actor "walks away satisfied" — they're mid-flow), it is `subfunction`.

When ambiguous, default to `user-goal` per Cockburn's recommendation. Surface the count of `default-classified` UCs in the diagnostics block.

**Identify stakeholders.** Stakeholders are parties with an interest in the UC's outcome — **distinct from actors**, who participate in the flow. A stakeholder may be human (a compliance officer who never touches the system but cares the policy is enforced) or organisational (a regulatory body, a finance department).

**Stakeholder sources, in priority order:**

1. `§Personas` — supporting personas who don't participate but care (e.g., *"Audit team — needs every approval to be logged"*).
2. `§Constraints` — legal / compliance / regulatory parties named in constraint phrasing.
3. `§Risks` — regulatory bodies, security teams.
4. Running prose — last resort.

Each stakeholder is recorded as `{name, interest}` — e.g., *"Audit team — every approval is recorded with timestamp and approver identity."* If no stakeholder beyond the primary actor is named anywhere, the UC's stakeholder list contains a single self-referential entry (the primary actor's interest in achieving the goal).

**Output of Round 3:** the UC list with `level ∈ {summary, user-goal, subfunction}` and `stakeholders[]` populated on every row.

### Round 4 — Preconditions & Guarantees

For each UC, capture three conditions:

- **Preconditions** — what must be true before the UC can begin. Typically: actor authenticated; a domain entity exists; the actor has the required permission. Preconditions are not tested within the UC; they are assumed.
- **Success guarantees** — what is true after the UC ends successfully. Typically: a domain entity is in a new state; an event is recorded; a downstream actor is notified. Measurable where the source supports it; anchored to `§Acceptance criteria`.
- **Minimal guarantees** — what is preserved even if the UC fails partway through. Typically: data integrity is preserved; no partial commits; the audit trail records the attempt; the actor is informed of the failure.

**Source priority:**

| Condition class | Strongest source | Weaker sources | Marker when no source |
|---|---|---|---|
| Preconditions | `§Constraints` (auth / permission / capacity rules) | `§1 Domain` (entity existence) | `derived-from-stories` (rare; mostly always anchored) |
| Success guarantees | `§Acceptance criteria` | `§Goals`, `§Pains` (inverse — pain removed = success) | `derived-from-pains` (pain removal as success) |
| Minimal guarantees | `§Constraints` (data integrity / audit invariants) | `§Risks` (failure modes imply integrity rules) | `derived-from-risks` |

If a success guarantee cannot be anchored to `§Acceptance criteria` and is derived from `§Pains` (pain inversion), apply the `derived-from-pains` marker on that guarantee — do not silently fabricate a success guarantee with no source. The marker is honest; a guess is invented data.

If no minimal guarantee is named anywhere in requirements, default to the universal pair *"Data integrity is preserved (no partial commits)"* and *"The attempt is recorded in the audit trail"*, mark both with `derived-from-risks` if `§Risks` exists, else `derived-from-constraints`. Surface the count of default-minimal-guarantees in the diagnostics block.

**Output of Round 4:** the UC list with `preconditions[]`, `success_guarantees[]`, and `minimal_guarantees[]` populated. Each item carries either a verbatim §-section reference (e.g., *"AC-04: approval is recorded with timestamp"*) or a `derived-*` marker.

### Round 5 — Main Success Scenario

For each UC, capture the numbered step sequence — the canonical actor-system interaction that achieves the goal.

**Step form rules:**

- Each step is a **subject-verb-object** sentence. Subject is either a named actor (primary, secondary) or the literal token `System`.
- Steps alternate actor ↔ system. The first step is typically actor-initiated (the trigger); the last step is typically system-final (the goal-achieved acknowledgement). Strict alternation is not required, but two consecutive same-subject steps should be merged or split into different UCs.
- Forbidden tokens in step text (affordance leak): `click`, `tap`, `navigate to`, `open the … dialog`, `select … from the dropdown`, `enter … in the field`, `press the … button`, `see … on the screen`. Steps describe interactions, not UI affordances. Rewrite to the underlying intent (*"The user clicks Submit"* → *"The user submits the claim"*).
- A step does not name a specific product feature by name (*"The user uses the bulk-edit feature"* → *"The user updates the prices in one operation"*).

**Step-count rules per level:**

- `user-goal` UCs: 3–9 steps. Fewer than 3 = trivial (likely a `subfunction`); more than 9 = composite UC that should be decomposed into a `summary` UC + sub-UCs.
- `subfunction` UCs: 1–3 steps. Shared utility flows are short.
- `summary` UCs: 3–9 steps, where each step is *"Include UC-NN <Title>"* — i.e., the summary UC orchestrates other UCs by reference.

**Source priority for step sequences:**

1. `§Task flows` — the strongest source. Each task flow's step list maps directly (mark `flow-from-task-flows`).
2. `§User stories` prose + `§1 Domain` entity references — reconstruct the sequence from story prose and domain entities (mark `flow-derived`).
3. `§Acceptance criteria` — postcondition phrasing implies a final step ("the order is recorded" → final system step "The System records the order").
4. `§Existing solutions` / `§Current process` — implied sequence from current-state prose (last resort; mark `flow-derived`).

**Trigger.** The trigger is the event that initiates the UC. Captured as a one-line clause separate from the main scenario, sourced from `§Task flows` preconditions / `§User stories` situation prefaces / `§Personas` daily-task prose. Examples: *"A purchase order requiring approval is submitted"*, *"Stock on a high-velocity SKU drops below reorder threshold"*. If no trigger phrasing exists, default to *"The primary actor decides to <goal>"* and mark `derived-trigger`.

**Output of Round 5:** the UC list with `trigger` and `main_steps[]` populated on every row. Each step carries `{step_no, subject, text, subject_class ∈ {actor, system}}`. The UC carries a single `flow_source ∈ {flow-from-task-flows, flow-derived}` marker.

### Round 6 — Extensions

For each main step, identify alternative flows (different paths the goal can still be achieved) and exception flows (failure modes that prevent the goal). Number each extension against the main step it branches from:

- `3a` — alternative at main step 3.
- `3a1`, `3a2` — sub-steps within the alternative.
- `5a → exception` — exception at main step 5.

Extensions follow the same step-form rules as main steps (SVO; no affordance leak; named actor or `System`).

**Extension sources, in priority order:**

1. `§Risks` — explicit failure modes (data invalid, external system unavailable, permission denied).
2. `§Pains` — current-state breakdowns ("the approval bounces around for 2 days" → exception flow at the approval step).
3. `§Constraints` — validation rules imply exceptions at the steps where validation runs.
4. `§Acceptance criteria` — negative cases ("if the supplier is not approved, the system must reject the order" → exception at the supplier-validation step).

**Extension classification:**

- `alt` — alternative flow; goal is still achieved, just via a different path (*"3a. The user is offered a list of past approvers and selects one"*).
- `exception` — failure flow; goal is not achieved, but minimal guarantees still hold (*"5a-exception. The supplier is not approved. System rejects the order and logs the attempt."*).

If no extension can be sourced for any main step, mark the UC with `no-extensions-in-requirements` rather than fabricating one. This is a content-gap marker; surface the count in the diagnostics block. Most requirements docs name at least one exception per UC (validation failure, permission denial); an entire UC with no extensions is a likely gap in `§Risks` / `§Acceptance criteria`.

**Output of Round 6:** the UC list with `extensions[]` populated. Each extension carries `{branch_label, classification ∈ {alt, exception}, steps[], source}`.

### Round 7 — UML diagram view derivation

Runs only after the Round 6 output passes the quality-gate sweep (or the consultant explicitly accepts Override). Round 7 derives the canonical UML use case **diagram view** from the gated card data — no new claims are introduced. The diagrams are a visual presentation of facts the cards already carry; they cannot diverge from the gated map.

UML use case diagrams (UML 2.5 §18) are inherently **system-level** views: actors on the outside, use cases as ovals inside a system boundary, with association lines (actor↔UC), `«include»` arrows (one UC includes another's behaviour), `«extend»` arrows (a separate UC injects behaviour at a named extension point in the base UC), and generalization arrows (actor or UC hierarchies). The analyser produces this view as inline SVG + adjacent copy-pasteable Mermaid `flowchart LR` source. Mermaid has no first-class UML use case diagram syntax — the `flowchart` form is an approximation, and the caption on every Mermaid block discloses this honestly (matching the convention already established by the activity-diagram analyser, where Mermaid has no first-class UML activity diagram either).

#### Diagram inventory

- **System overview** — always emitted. One figure showing every primary actor and every UC inside the system boundary, plus all association edges and all derived `«include»` edges. This is the canonical UML use case view; emitting it unconditionally is the value-add over the card grid.
- **Per-actor focus diagrams** — 0..N, consultant-selected post-gate via the analyser's Step 8.6 `AskUserQuestion` multi-select. Each shows one actor and only their UCs, plus `«include»` edges whose both endpoints fall inside that actor's UC set. The actor-index sidebar already gives a tabular per-actor view; per-actor diagrams are useful but redundant for many runs, so opt-in is the default. When there is only one primary actor, the per-actor selection is skipped (a single-actor focus view would be identical to the overview).

#### Edge derivation rules

Three edge classes are derived; two are explicitly not derived.

- **Association edges (derived).** One per `(primary_actor, UC)` pair on the map. Endpoints come from Round 1 / Round 2 output. Never invent endpoints. UML associations are undirected; the SVG line carries no marker, the Mermaid form is `actor --- UC`.
- **`«include»` edges (derived).** Cockburn convention: `summary`-level UCs reference their constituent UCs by ID in step text (Gate 4 enforces this), and `user-goal` UCs frequently reference `subfunction` UCs by ID. Both are surfaced as `«include»` edges in the diagram. The derivation is purely lexical: walk the main-step text of every `summary` and `user-goal` UC for `UC-NN` tokens; for each token whose referenced UC exists in the UC node set, emit one `«include»` edge `{from_uc, to_uc}`. Deduplicate.
- **`«extend»` edges (NOT derived).** Cockburn extensions (Round 6 alternative and exception flows) are scenario-internal branches at numbered main-step points — they describe how the same UC behaves under variant conditions. UML `«extend»` is a fundamentally different concept: a separate UC injects additional behaviour at a named extension point in a base UC. Cockburn extensions and UML extensions share only the word; their semantics do not align. Fabricating `«extend»` edges from Round 6 extensions would mislead consultants who know UML. The analyser emits zero `«extend»` edges and discloses this in the diagnostics block: `«extend» edges: 0 (Cockburn extensions model scenario branches, not UML extension points)`.
- **Generalization edges (NOT derived).** No source in `requirements.md` anchors actor-generalization (e.g., `Manager` generalises `User`) or UC-generalization (e.g., *Pay by card* generalises *Pay*). The reference's source-priority rules forbid invention. The analyser emits zero generalization edges and discloses this in the diagnostics block: `«generalize» edges: 0 (no source signal in requirements)`.

#### Rendering contract

- **Self-contained inline SVG.** The artefact remains a single self-contained HTML file. No external CSS, no external JS, no external image references. Every UML SVG is inline; every Mermaid block is plain text.
- **Adjacent Mermaid source.** Each SVG diagram has a matching `<pre>` Mermaid block inside a single `<details class="uml-mermaid-source">` element. Mermaid is the copy-pasteable fallback / canonical-rep — the consultant pastes it into mermaid.live to regenerate, share, or modify.
- **Mermaid is a `flowchart LR` approximation.** The caption on every Mermaid block discloses this: *"Mermaid does not have first-class UML use case diagrams; this is a `flowchart LR` approximation."* Adopting the same caption convention used by the activity-diagram analyser keeps the consultant's mental model consistent.
- **SVG layout is deterministic.** Same inputs produce byte-identical SVG. The analyser specifies the geometry (`framework/agents/analyses/use-cases-analyser.md > Step 9`); this reference states only the contract — viewBox sized to data, actors on the left, system boundary as a rect, UCs stacked inside, association lines from actor to UC, dashed curved arrows for `«include»`.
- **Level colour parity.** Each UC ellipse fill uses the same level palette as the card border (summary violet, user-goal blue, subfunction grey). The consultant sees the same colour signal in both the card view and the diagram view.

#### No new quality gate

Round 7 introduces no hard quality gate. Every claim it visualises was already gated by the seven Round 6 gates. A diagram-specific gate would either re-validate gated data (redundant) or invent a constraint not anchored in the requirements (out of scope). Structural well-formedness of the rendered SVG and Mermaid blocks is enforced at handback by the analyser's self-validation checks (presence, counts, schema), not by a new gate.

**Output of Round 7:** `uml_inventory = {actors[], ucs[], assoc_edges[], include_edges[], extend_edges: [], generalize_edges: []}` plus the consultant's `chosen.actors[]` selection (set in Step 8.6 of the analyser). Track the diagnostics line: `UML diagrams: 1 overview, K per-actor; association edges: A; «include» edges: I; «extend» edges: 0; «generalize» edges: 0`.

---

## Output presentation

The artefact opens with an **In plain terms** lead (`<section id="plain-terms">` carrying `{{PLAIN_SUMMARY}}`) as its **first content section**, above the overview — a 2–5 sentence plain-English summary (what this map is, what it found, what to do with it), per `framework/shared/output-readability.md`. It is a faithful condensation introducing no use case, count, or `[SRC]` not already present; methodology jargon is glossed at first use, client domain terms are not.

Below the lead, the artefact renders as a use-case card grid grouped by level (summary → user-goal → subfunction), with a top-level UC index table and an actor-index sidebar. Color contract:

| Element | Color | What it carries |
|---|---|---|
| Level chip — Summary | violet | Round 3 level = `summary` (kite). |
| Level chip — User-Goal | blue | Round 3 level = `user-goal` (sea; the default). |
| Level chip — Subfunction | grey | Round 3 level = `subfunction` (fish). |
| Actor provenance dot | green / amber | `from-personas` (green) / `derived-actor` (amber). |
| Goal-source pill | blue / violet / green / amber | `from-user-stories` / `from-task-flows` / `from-goals` / `from-prose`. |
| Flow-source pill | blue / amber | `flow-from-task-flows` / `flow-derived`. |
| Step — actor | pale blue background | Main / extension step with `subject_class = actor`. |
| Step — system | pale grey background | Main / extension step with `subject_class = system`. |
| Extension — alt | indented under main step; left-border green | Alternative flow (goal still achieved). |
| Extension — exception | indented under main step; left-border red | Exception flow (goal not achieved; minimal guarantees hold). |
| `derived-*` marker | muted-italic | Anywhere a condition / step / trigger / extension is derived rather than verbatim-sourced. |

Plus a top-level **UC index table** listing every UC with `UC ID | Title | Primary Actor | Level | Steps | Extensions` columns, sortable visually by level (summary first, user-goal block, subfunction last). And an **actor index sidebar** with per-actor UC counts so the consultant can see which actor anchors which UCs at a glance.

The Round 7 **UML use case diagrams** are presented in their own section (`id="uml-diagrams"`) between the card grid and the UC index table. The always-on `<figure class="uml-diagram uml-overview">` shows every actor and UC; opt-in `<figure class="uml-diagram uml-per-actor">` blocks show one actor's slice each. UC ellipses carry the same level fill colours as the card borders (summary violet, user-goal blue, subfunction grey). Actor stick figures are uniform black (UML convention; no provenance colour-coding inside the diagram — provenance is carried on the card and on the actor-index sidebar). `«include»` edges are dashed curved arrows with an open arrowhead and a `«include»` label. Adjacent to the SVGs sits a single `<details class="uml-mermaid-source">` containing one `<pre>` per diagram (copy-pasteable Mermaid `flowchart LR` source), each preceded by a caption that discloses the `flowchart` approximation. The `<details>` is closed by default — the consultant opens it only when they need the source.

---

## Quality gates (run after Round 6, before write)

Every gate is a hard gate. If any gate fails, the analyser does **not** write the artefact — it surfaces a structured error to the consultant and halts. (See `framework/agents/analyses/use-cases-analyser.md > Step 8 — Validate` for the halt contract.)

1. **Every UC has exactly one primary actor.** Anonymous UCs are weak signal. If `§Personas` is absent, allow a fallback actor `User (no persona section in requirements)` with the `derived-actor` marker; UCs without even that fallback are flagged.
2. **Every UC title is an active-verb goal phrase.** Forbidden title verbs (case-insensitive substring match at the start of the title): `manage`, `handle`, `process`, `do`, `work with`. Forbidden affordance verbs anywhere in the title: `click`, `tap`, `select`, `enter`, `press`. Titles must be in completed active verb form (no gerunds: *"Submitting"*; no noun forms: *"Submission"*). Flag offending UCs by `uc_id` + offending title.
3. **Every UC has at least one precondition AND at least one success guarantee.** Silent missing pre/post conditions are the most common omission in informal UCs and break downstream design consumption (the design phase has no setup signal and no acceptance signal). Flag offending UCs.
4. **Step-count is within bounds for the UC's level.** `user-goal` UCs: 3 ≤ steps ≤ 9. `subfunction` UCs: 1 ≤ steps ≤ 3. `summary` UCs: 3 ≤ steps ≤ 9 and every step references another UC by ID. Out-of-bounds UCs are flagged with their step count and current level.
5. **Every step is a subject-verb-object sentence.** The subject is either a named actor from the UC's actor list or the literal token `System`. Steps missing a subject (e.g., *"Fills in the form"*), steps with a passive-voice subject (e.g., *"The form is filled in"*), or steps with an affordance subject (e.g., *"The button is clicked"*) are flagged. Forbidden affordance tokens in step text (same list as Round 5 step form rules) are flagged.
6. **Every UC has at least one extension OR carries the `no-extensions-in-requirements` marker.** A UC with no extensions and no marker is a silent gap; the consultant might mistake it for a complete UC. Either at least one extension exists (verbatim-sourced or derived with `derived-*`), or the marker is present.
7. **Every success guarantee anchors back to `§Acceptance criteria` OR carries the `derived-from-pains` marker.** Silent fabricated postconditions corrupt the acceptance contract downstream. Flag guarantees that name no source and have no marker.

---

## Anti-patterns

- **Vague titles.** *"Manage orders"*, *"Handle approvals"*, *"Process refunds"* are feature categories, not use cases. Each rewrites to one or more concrete UCs (*"Cancel an order"*, *"Re-route an order"*; *"Approve a purchase order"*, *"Reject a purchase order with comment"*). Gate 2 catches these.
- **Step explosion.** A UC with 20+ steps is almost always a composite — it should be re-classified `summary` and decomposed into 3–6 sub-UCs. Gate 4 catches these.
- **Affordance leak in step text.** *"User clicks Submit"* describes a UI affordance, not a behaviour. Rewrite to *"The user submits the claim"*. Affordance vocabulary belongs in the design phase, not the analysis. Gate 5 catches these.
- **Fabricated postconditions.** If `§Acceptance criteria` does not name a measurable success condition, do not invent one ("the order is processed quickly" — by what measure?). Either find an anchor in `§Pains` and apply `derived-from-pains`, or surface the gap via Step 8's Revise path.
- **Confusing actors with stakeholders.** An actor participates in the flow; a stakeholder has an interest in the outcome. A regulator who never touches the system but requires the audit trail is a stakeholder, not an actor. Conflating them inflates the actor list with non-participants.
- **Confusing preconditions with main-flow tests.** A precondition is assumed before the UC runs; if the UC actively tests something at runtime, that test is a main-flow step (and its failure is an extension), not a precondition.
- **Confusing extensions with new UCs.** An extension branches from a main step and either still achieves the goal (alt) or surfaces a failure with minimal guarantees intact (exception). If a "branch" actually describes a fundamentally different goal (a different actor walking away with a different outcome), it is its own UC, not an extension.
- **Collapsing rounds.** Do not write UCs, levels, conditions, scenarios, and extensions in a single pass. The round-by-round structure is what makes the map reviewable — collapsing rounds hides reasoning.
- **Editorialising.** The analyser is a literal lens onto the requirements doc. It does not propose new product features; it surfaces UCs the BA already documented (verbatim where named, derived where implied). If the requirements doc names no UC for a goal the analyser thinks should exist, the analyser flags the gap rather than inventing the UC.
- **Inventing flows where `§Task flows` is sparse.** If `§Task flows` is sparse, most UCs will carry `flow-derived` rather than `flow-from-task-flows`. Surface the count in the diagnostics block; the consultant addresses it by revising `§Task flows` and re-running.
- **Inventing extensions to satisfy Gate 6.** If `§Risks` / `§Pains` / `§Constraints` / `§Acceptance criteria` name no failure mode for a UC, mark `no-extensions-in-requirements` rather than guessing *"3a. The user cancels"*. The marker is honest; the guess is invented data.
- **Fabricating UML `«extend»` edges from Cockburn extensions.** Cockburn extensions (Round 6) are scenario-internal branches at numbered step points; UML `«extend»` represents a wholly separate UC injecting behaviour at a named extension point in a base UC. The words match; the semantics do not. Emit zero `«extend»` edges and disclose. Auditing consultants who know UML will catch a fabricated mapping immediately.
- **Fabricating UML generalization edges.** No source in `requirements.md` anchors actor or UC generalization. Emit zero and disclose. Generalization without an anchor is invented hierarchy.
- **Treating the UML diagrams as a replacement for the card grid.** The card grid is the canonical use-case deliverable — it carries goal-in-context, stakeholders, preconditions, success guarantees, minimal guarantees, trigger, main scenario, and extensions. The UML diagrams are a Tier-2 visualisation of the actor / UC / include topology only. They are additive, never substitutive. Downstream consumers (`map-use-cases-to-ui` skill, design-spec-drafter) read from the card grid, not the diagrams.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/use-cases-analysis.md` — analytical, thorough, literal, behaviour-faithful, sequence-faithful. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact is human-read (and consumed downstream by `/wireframe`'s `blueprint-architect` via the per-analysis sidecar), so the analyser also follows `framework/shared/output-readability.md`: it writes the "In plain terms" lead, glosses methodology jargon (use case, primary actor, main success scenario, extension, sea-level) at first use in human-readable prose, leaves client domain vocabulary unglossed (GLOSSARY territory), and keeps every `[SRC: C-NNN]` marker. The plain-language layer is confined to the lead + first-use glosses; the cards, index table, UML diagrams, and diagnostics keep their concrete, named-UC discipline.
