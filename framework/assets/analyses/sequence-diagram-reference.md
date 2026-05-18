<!-- ROLE: asset (analysis reference). Methodology definition for the sequence-diagram analyser. Modelled on framework/assets/analyses/data-model-reference.md. Industry framing: OMG UML 2.5 sequence-diagram subset — one diagram per scenario, system-level fidelity (actor × system components × external systems × messages × combined fragments). -->

# Sequence Diagram analysis reference

> **Method:** Extract a **per-scenario sequence-diagram catalogue** (scenarios, participants, messages, combined fragments, cross-scenario participant matrix) from `requirements/requirements.md` once. The tabular catalogue is always rendered. The consultant then picks **none, one, several, or all** of the discovered scenarios to add as inline-SVG `<figure>` blocks. Same data, the visuals are views onto the scenarios already listed in the catalogue.

**Output file:** `analyse-requirements/SEQUENCE-DIAGRAM/sequence-diagram.html` — a self-contained HTML artefact containing the per-scenario tabular catalogue (always) plus zero or more inline-SVG sequence-diagram figures (per consultant selection). No external CSS/JS dependencies; viewable by opening `file://` in a browser.

**Analyser agent:** `framework/agents/analyses/sequence-diagram-analyser.md`

**Character:** `framework/assets/characters/sequence-diagram-analysis.md`.

---

## Industry framing — UML 2.5 sequence-diagram subset

Per OMG UML 2.5 § 17.4 (Sequence Diagrams), a sequence diagram models an interaction between participants over time. The full UML notation has eight combined-fragment operators and rich features (state invariants, found/lost messages, gates, decomposition refs). This methodology restricts the subset to elements that map cleanly to requirements text:

| Element | UML name | Included | Why included / why excluded |
|---|---|---|---|
| Lifeline | Lifeline | yes | Every participant is a lifeline. |
| Synchronous message | sync MessageSort | yes | Solid arrow with filled arrowhead. Default for inter-component calls. |
| Asynchronous message | async MessageSort | yes | Solid arrow with open arrowhead. For fire-and-forget or queued. |
| Return message | reply MessageSort | yes | Dashed arrow back to caller. Pairs every sync. |
| Self-message | sync to same lifeline | yes | Allowed (`OrderSvc → OrderSvc: validate()`). |
| Activation bar | ExecutionSpecification | yes | Rectangle on receiver lifeline for the duration of the message handling. |
| `alt` fragment | alt | yes | Alternative branches by guard. |
| `opt` fragment | opt | yes | Optional fragment by guard. |
| `loop` fragment | loop | yes | Loop fragment by guard. |
| `par` fragment | par | **no — MVP** | Needs concurrency intent not in requirements. Defer. |
| `ref` fragment | ref | **no — MVP** | Cross-diagram reference; adds nesting complexity. Defer. |
| `break` / `critical` / `neg` / `strict` / `seq` / `ignore` / `consider` / `assert` | various | **no — MVP** | Design-intent operators not derivable from requirements. Defer. |
| State invariant on lifeline | StateInvariant | **no — MVP** | Cross-cuts data-model; defer. |
| Found / lost message | found/lost | **no — MVP** | Boundary cases; defer. |

System-level fidelity: participants are **the persona actor + named system components/aggregates from `§2 Domain model` + inferred external systems**. Per-class or per-method fidelity is out of scope — most rows would be `ai-suggested` (design speculation), which degrades the audit trail.

---

## Output structure

The artefact has two tiers:

### Tier 1 — Sequence-diagram catalogue (always rendered)

Six tabular sections, in this order:

1. **Scenarios table** — `id` (kebab-case), `display_name`, `type` (`primary` / `extension` / `recovery`), `actor` (persona id), `goal` (one-line outcome), `source` (`§5.N` task-flow id, `§4.N` story id, or `derived`), `message_count`, `provenance`.
2. **Participants table** — `id` (kebab-case), `display_name`, `kind` (`actor` / `system-component` / `external-system`), `role` (one-line description), `scenarios` (comma-separated scenario ids that reference this participant), `provenance`.
3. **Messages table** — `scenario_id`, `seq` (integer 1..N within scenario), `from` (participant id), `to` (participant id), `kind` (`sync` / `async` / `return`), `label` (verb phrase), `data` (payload type from `§7` or empty), `notes` (`fire-and-forget: true` flag, return-pairing notes), `provenance`.
4. **Combined fragments table** — `scenario_id`, `id` (`F-NN` zero-padded), `type` (`alt` / `opt` / `loop`), `guard` (expression text), `span_first` (first message seq), `span_last` (last message seq), `branch` (for `alt`: which guard this row represents — empty for `opt`/`loop`), `provenance`.
5. **Cross-scenario participant matrix** — pivoted view: rows = participants, columns = scenarios, cell = check mark or empty. Helps the consultant spot participants used in only one scenario (may be unnecessary) or in every scenario (load-bearing).
6. **Diagnostics block** — counts summary, per-marker provenance summary, the 10 check result lines (PASS / FAIL), the density-warning line.

Conceptual types only for payload columns. Platform-agnostic. No DBMS-specific types.

### Tier 2 — Inline-SVG sequence diagrams (0..N, consultant-selected)

After the catalogue is extracted, the analyser surfaces a `multiSelect: true` prompt with one option per discovered scenario plus a "select all (Recommended)" affordance. The consultant picks any combination:

- **Empty selection is valid** — produces a catalogue-only output (Tier 1 only, no SVG blocks). The tabular catalogue is itself a recognised deliverable form.
- **Single selection** — one `<figure class="sequence-diagram seq-{slug}">` with one inline `<svg>`.
- **N selections** — N figures, one per selected scenario. All figures share the same `lane_width` so participants align vertically across scenarios when the consultant scrolls between them.

Each SVG carries:

- **Header band** at the top with participant boxes (rectangle per participant, label inside).
- **Lifelines** — dashed vertical lines drawn down from each participant box.
- **Messages** — horizontal arrows between lifelines at successive `y` positions. Sync = solid arrow with filled arrowhead; async = solid arrow with open arrowhead; return = dashed arrow with open arrowhead.
- **Activation bars** — small rectangles centred on the receiver lifeline spanning from the call to the matched return.
- **Combined-fragment frames** — rectangles with a top-left label tab (`[alt: guard]`, `[opt: guard]`, `[loop: guard]`) framing the messages in the fragment's span.

---

## Source-of-truth hierarchy

The analyser walks `requirements/requirements.md` in this order:

1. **`§5 Task flows`** — primary. Each top-level task flow becomes a candidate scenario. Each step in the flow becomes a candidate message. The first noun in each step is a candidate participant.
2. **`§4 User goals & stories`** — supplementary scenarios. A story without a matching task flow surfaces as an `ai-suggested` scenario (the user clearly wants the goal; no task-flow walks through it).
3. **`§2 Domain model`** — default participant catalogue:
    - `§2.1 Concepts` — entities become candidate `system-component` participants.
    - `§2.3 Aggregates & lifecycles` — aggregate roots become primary `system-component` participants (aggregates own the call surface in DDD-style architectures).
4. **`§3 Target users`** — personas become the `actor` participant of scenarios they participate in. The scenario's `actor` field is the persona id from `§3`.
5. **`§7 Data entities`** — payloads carried by messages. When `§5.N.step` says "submit the order details", the data column carries `Order` (from `§7`).
6. **`§6 Requirements`** — business rules become **fragment guards** (`opt [if amount > 10000]`) and **alt branches** (error / recovery paths).

If `§5 Task flows` is absent or empty, the analyser degrades gracefully to `§4 + §6` derivation. Density of `ai-suggested` markers will be high; the soft warning surfaces this in diagnostics.

---

## Seven-round discipline

Each round produces a distinct, named in-memory output. The analyser does not write the artefact until Round 7 is complete and all 10 hard quality checks have passed (or the consultant chose Override).

### Round 1 — Scenario discovery (exploratory and inclusive)

- Walk `§5 Task flows`: every top-level task flow is a candidate scenario `{candidate_id, candidate_display_name, source: "§5.N", source_line_offset}`. The `candidate_id` is kebab-case from the task-flow title.
- Walk `§4 User goals & stories`: every story with a clearly separate verb-phrase from any task-flow is a candidate (e.g. "As an Owner I want to reset my password" — typically not in task flows). Provenance `derived-from-§4`.
- Walk `§6 Requirements` for **explicit recovery / error scenarios** ("on failed payment, the system must retry up to 3 times and then escalate"). These become recovery-type candidate scenarios. Provenance `derived-from-§6`.

Output: candidate scenario list. Do not dedupe yet — Round 2 handles that. **Cap rule:** if the candidate list exceeds 20 scenarios, state the cap aloud, surface the top 12 by source frequency (§5 first, then §4, then §6), and discard the rest with a note in diagnostics.

### Round 2 — Scenario refinement (decisive)

Per **Quality checks 1, 2, 3**:

- **Merge synonyms.** When candidates describe the same outcome ("submit order" and "create order" and "place order"), pick the canonical id from `§5` if present, else from the most-frequent occurrence. Record the alias in the scenario's notes field.
- **Pair happy paths with recoveries.** When `§6` declares a recovery scenario whose precondition matches a `§5` task flow, mark them as a `primary` + `recovery` pair (same actor, same goal phrasing, different outcome). Each is its own scenario row.
- **Classify type.** Every scenario is one of:
    - `primary` — happy path from `§5` task flow or a `§4` story.
    - `extension` — `§5` task flow with branching ("the user can choose to skip step 4") that warrants a separate diagram.
    - `recovery` — error / retry / compensation path from `§6` constraints.
- **Assign kebab-case id and display name.** Id: `submit-order`, `cancel-order`, `retry-failed-payment`. Display name: `Submit an order`, `Cancel an order`, `Retry failed payment` (sentence-case from the source title).
- **Assign provenance marker** per the three-marker contract (see Provenance markers below).
- **Drop candidates** that cannot be sourced after merging.

Output: the scenario list as `[{id, display_name, type, actor: null, goal, source, source_line_offset, provenance, notes}]`. The `actor` field stays null until Round 3 assigns it. Scenario IDs are kebab-case; uniqueness is enforced.

### Round 3 — Participant extraction

Per **Quality checks 2, 9**:

- **Actor.** For each scenario, identify the primary actor:
    - If the source `§5` task flow names a persona (e.g. "Owner submits the order"), the persona's `§3` id is the actor. Provenance `from-task-flow` (verbatim from §5) for the participant row entry.
    - If only a generic noun appears ("the user submits..."), match to a `§3` persona by role inference; if multiple personas qualify, mark the actor as the most-frequent persona in the scenario's source section. Provenance `derived-from-§3`.
    - If no persona can be matched, propose a generic `user` actor as `ai-suggested`.
- **System-component participants.** Walk the source `§5` task-flow steps:
    - Every aggregate-root mentioned in `§2.3` that appears in the steps becomes a system-component participant. Provenance `from-task-flow` if verbatim in §5, else `derived-from-§2`.
    - Every concept from `§2.1` that the actor interacts with directly becomes a system-component participant. Provenance `derived-from-§2`.
- **External systems.** Walk the steps for terms that imply outside-the-system services (payment gateway, email service, identity provider, third-party API). If `§2` does not name them explicitly, propose as `ai-suggested` `external-system` participants. Naming convention: `PascalCase` ending in a kind suffix (`PaymentGateway`, `NotificationSvc`, `IdentityProvider`).
- **Aggregate the global Participants table.** A participant referenced across multiple scenarios appears once in the global table with a comma-separated `scenarios` field.
- **Cap rule on external systems.** If proposed `ai-suggested` external systems > 5 in a single run, surface a one-line note in diagnostics suggesting the consultant name them in `§2 Domain model` so they leave the `ai-suggested` density.

Output: the per-scenario participant set + the global participants table. Update each scenario's `actor` field.

### Round 4 — Message extraction

Per **Quality checks 3, 4, 5**:

For every scenario, walk the source `§5` task-flow steps in order. Per step:

- **Identify the verb.** The step's verb is the message label (e.g. "submit the order" → `submitOrder`). Strip articles and convert to lowerCamelCase. **Never** use `and` / `then` / `etc` as verbs.
- **Identify `from`.** The step's subject — usually the actor on user-initiated steps, or the previous receiver on chained system-to-system steps.
- **Identify `to`.** The step's object's owner — typically a system component (e.g. "submit the order" → `OrderSvc`). Inference rules:
    - If the step names a system component verbatim ("calls the OrderSvc"), use it.
    - If the step names a domain object ("submit the order"), use the aggregate-root component that owns the object (`Order` → `OrderSvc`).
    - If the step names an external service ("send notification email"), use the matching `external-system` participant.
- **Assign seq.** Sequential integer starting at 1 per scenario.
- **Assign provenance.** `from-task-flow` if the verb+from+to triple is verbatim derivable from a single `§5` step; `derived-from-§N` if extracted from `§4`/`§6`; `ai-suggested` if the message is implicit (e.g., an implicit `validate()` between two stated steps, or any return message that the source does not explicitly mention).

Output: the messages list per scenario. **Every scenario has ≥1 message.**

### Round 5 — Message typing + data payloads

Per **Quality checks 4, 6**:

For every message, determine:

- **Kind.** One of:
    - `sync` — the sender waits for a response. Default for actor → system and component → component calls.
    - `async` — fire-and-forget or queued. Use when the source `§5`/`§6` explicitly states "send", "publish", "enqueue", "emit event", or when the target is a notification/email service.
    - `return` — paired reply to an earlier `sync` message. Same scenario, lower seq.
- **Pair every `sync` with a `return`.** If the source step does not explicitly describe a return, generate an `ai-suggested` return message with an inferred response label (`orderId`, `confirmation`, `ack`) and the original sender as `to`, original receiver as `from`. Annotate the return's notes as `paired with seq N`.
- **Mark fire-and-forget exceptions.** If a `sync` is intentionally fire-and-forget (rare — e.g. a logging call the sender does not block on), set `kind: sync` and notes `fire-and-forget: true` instead of generating a return. **Every `sync` either has a paired `return` or is marked `fire-and-forget: true`** (check 6).
- **Data payload.** From `§7 Data entities`, identify the entity carried in the message. If the message label is `submitOrder` and `§7` defines an `Order` entity, the data field is `Order`. Provenance for the data field follows the message's provenance.
- **Allowed payload types.** Same nine conceptual types as data-model: `text` / `number` / `date` / `timestamp` / `boolean` / `enum` / `UUID` / `reference` / `binary`. Plus entity-typed payloads (`Order`, `Payment`) — these are references to `§7` entity ids. **Never** DBMS-specific types.

Output: the messages list with `kind`, `data`, return pairing.

### Round 6 — Combined fragments (alt / opt / loop only)

Per **Quality checks 7, 8**:

For every scenario, walk `§6 Requirements` for clauses that constrain the source `§5` task flow:

- **`opt` (optional).** A `§6` constraint like "if the amount exceeds 10,000, dual approval is required" becomes an `opt` fragment with guard `amount > 10000` framing the messages that implement the approval. Span: `[first_message_id, last_message_id]` covering the conditional messages.
- **`alt` (alternative).** Mutually-exclusive branches: "on payment success, confirm; on payment failure, escalate". Two `alt` fragment rows with the same `id` (e.g. `F-01`) but different `branch` and `guard` (`payment success` / `payment failure`). Span on each row covers that branch's messages.
- **`loop` (iterate).** A `§5` step like "for each item in the cart, validate" or a `§6` constraint like "retry up to 3 times" becomes a `loop` fragment with guard `item in cart` or `attempt < 3`. Span covers the loop body messages.

**Every fragment must:**

- Name a type ∈ {`alt`, `opt`, `loop`}.
- Carry a non-empty guard expression (no empty `[]`).
- Span ≥1 message, all of whose seq ids exist in the scenario's messages.

Provenance:
- `derived-from-§6` if the constraint text is in §6.
- `derived-from-§5` if the loop / branch is in §5 task-flow phrasing.
- `ai-suggested` if the fragment was inferred (the analyser should be conservative here — only emit `ai-suggested` fragments when omitting them would render the diagram misleading, e.g. a missing error path that §6 implies but does not enumerate).

Output: the combined-fragments list per scenario.

### Round 7 — Cross-scenario consistency

Per **Quality checks 5, 9**:

- **Participant naming consistency.** A participant used in scenario A as `OrderSvc` must be `OrderSvc` (not `OrderService`, not `Order Service`) in scenario B. Pick the canonical name once (longest verbatim match in §2; else PascalCase of the §2 noun) and rewrite all scenarios.
- **Message-label reuse.** If two scenarios call the same logical operation (`OrderSvc.submitOrder()`), the message label must be identical (`submitOrder`, not `submit` in one and `submitOrder` in another). Pick the canonical label once.
- **Pre-render layout sanity.** Count participants per scenario; if any scenario has > 8 participants, flag a soft layout warning in diagnostics ("Scenario `submit-order` has 11 participants — SVG width will be wide; consider decomposing into sub-scenarios").
- **Build the cross-scenario participant matrix.** Pivot the messages list → matrix[participant][scenario] = true if the participant appears in any message of that scenario.

Output: normalised participant names + message labels across all scenarios; the cross-scenario participant matrix.

---

## Provenance markers (3 — exhaustive)

Every scenario, participant, message, and combined fragment carries exactly one of:

| Marker | CSS class | When |
|---|---|---|
| `from-task-flow` | `.provenance-from-task-flow` | Content appears verbatim in a `§5 Task flows` step. Analogous to `from-domain-model` in data-model. |
| `derived-from-§N` | `.provenance-derived` | Content was extracted from a named section (`§2`, `§3`, `§4`, `§6`, `§7`) but is not verbatim in `§5`. The source section is recorded in a `data-source="§N"` attribute on the row. |
| `ai-suggested` | `.provenance-ai-suggested` | Content was inferred (e.g., an inferred return message, an inferred external participant, an inferred opt-fragment guard). Prefixed with `[AI-SUGGESTED]` in the text content. |

No fourth marker. No item unmarked. Honours the framework-wide `[AI-SUGGESTED]` invariant — the marker is reserved for facts not traceable to inputs.

---

## Quality checks (10 hard gates)

All checks operate on the catalogue — they are **independent of which scenarios the consultant selects for rendering**. The catalogue must be valid regardless of presentation.

1. **Every scenario has a kebab-case id and a display name.** Both non-empty; id matches `[a-z0-9-]+`.
2. **Every scenario has ≥1 actor participant and ≥1 system participant.** A scenario with zero actors or zero system components cannot represent an interaction.
3. **Every scenario has ≥1 message.** Empty scenarios are dropped or flagged.
4. **Every message has a non-empty `from`, `to`, and verb-phrase label.** Labels are lowerCamelCase verb-phrases; forbidden values include `and`, `then`, `etc`, empty string.
5. **Every message's `from` and `to` reference existing participants in the scenario's participant set.** Cross-check against the per-scenario participant set built in Round 3.
6. **Every sync message either has a paired return message or is annotated `fire-and-forget: true` in notes.** Paired return: same scenario, lower seq, kind=`return`, from/to swapped.
7. **Every fragment names a type ∈ {`alt`, `opt`, `loop`}, a guard expression, and a span covering ≥1 message.** Guard is non-empty string; span first/last are valid message seq ids.
8. **Every fragment's span resolves to existing message ids in the scenario.** `span_first` and `span_last` exist in the scenario's messages list.
9. **Every participant referenced in ≥1 scenario appears in the global Participants table.** Cross-check messages-set participants vs the global table.
10. **Every row in every Tier-1 table carries exactly one provenance marker** (`from-task-flow` / `derived-from-§N` / `ai-suggested`) — never zero, never two.

**Soft check (warning, not gate):**

- **AI-SUGGESTED density.** Compute `density_messages = ai_suggested_messages / total_messages`. If > 50%, emit a `density-warning` line in diagnostics and the handback summary: *"`§5 Task flows` is thin — most messages were inferred. Enrich `§5` and re-run for higher-confidence interactions."* Does not block writing.

---

## Scenario-selection sub-step

After all 10 hard checks pass (or the consultant chose Override at Step 8), the analyser surfaces a single `AskUserQuestion` with `multiSelect: true`:

- **Question:** *"The sequence-diagram catalogue has been extracted and validated. Which scenarios should be rendered as inline-SVG diagrams? Pick none, one, several, or all — the catalogue tables above are always rendered."*
- **Header:** `Diagrams`
- **Options:** one option per discovered scenario, labelled `<display_name> — <type> (<message_count> msgs)`. Default ordering: `primary` first, then `extension`, then `recovery`; alphabetical within each group. The first option is suffixed `(Recommended)` if it is the highest-message-count `primary` scenario.

Empty selection is **valid**. Cancelling the prompt outright (closing the dialog rather than submitting an empty selection) hands control back to the accept/revise/restart loop, not to silent emission.

---

## Stop-condition

The analysis is complete when:

- Every task flow declared in `§5` (or derived from §4/§6 when §5 is absent) has a row in the Scenarios table with at least one message.
- Every participant referenced in any scenario appears in the global Participants table.
- Every sync message is either paired with a return or marked `fire-and-forget: true`.
- Every combined fragment names a type, a guard, and a span resolving to existing message ids.
- All 10 hard quality checks pass, or the consultant chose Override.
- The consultant chose Accept in the Step 11 accept/revise/restart loop.

---

## Input-coverage asymmetry

`§5 Task flows` carries scenario shape, message sequence, and actor cleanly. The columns it does **not** typically carry:

- **Return messages.** Task-flow steps describe user-visible actions, not RPC return values. The analyser pairs every sync with an `ai-suggested` return.
- **Internal-component routing.** Task flows often say "submit the order" without naming whether the call lands on `WebApp → OrderSvc` or `WebApp → OrderController → OrderSvc`. The analyser flattens to the aggregate-root naming (`§2.3`) and marks intermediate components `ai-suggested` if proposed.
- **External-system participants.** Payment gateways, email services, identity providers — rarely named in `§2`. Almost always `ai-suggested`.
- **Combined-fragment guards.** `§6` carries the conditions (`if amount > 10000`); `§5` carries the steps. The analyser stitches them at Round 6.

Richer inputs → richer catalogue. Methodology degrades gracefully: with thin `§5`, the catalogue is mostly inferred and flagged.

---

## Output shape (HTML schema)

The artefact is a single self-contained HTML file at `analyse-requirements/SEQUENCE-DIAGRAM/sequence-diagram.html`. The analyser populates `framework/assets/analyses/template-sequence-diagram.html` via documented placeholder substitution. Every substituted value is HTML-escaped before injection (XML-escape inside `<svg><text>` nodes).

### Header placeholders

| Placeholder | Value |
|---|---|
| `{{TITLE}}` | *"Sequence Diagrams — `<domain>`"* if `§1` declares a domain, else *"Sequence Diagrams"*. |
| `{{DOMAIN}}` | Verbatim from `§1 Application context > Domain`, else *"(not declared in requirements.md)"*. |
| `{{GENERATED_AT}}` | ISO-8601 UTC, captured at render time. |
| `{{REQUIREMENTS_SHA256}}` | SHA-256 of `requirements/requirements.md` captured at Step 2. |
| `{{SCENARIO_COUNT}}` | Number of rows in the Scenarios table. |
| `{{PARTICIPANT_COUNT}}` | Number of rows in the global Participants table. |
| `{{MESSAGE_COUNT}}` | Number of rows in the Messages table (across all scenarios). |
| `{{FRAGMENT_COUNT}}` | Number of rows in the Combined fragments table. |
| `{{AI_SUGGESTED_COUNT}}` | Total items (scenarios + participants + messages + fragments) marked `ai-suggested`. |
| `{{SCENARIOS_RENDERED}}` | Comma-separated list of scenario display names whose SVG was emitted, or *"none — catalogue only"* if zero were selected. |

### Body placeholders

| Placeholder | Value |
|---|---|
| `{{DIAGNOSTICS_BLOCK}}` | Pre-rendered `<section class="diagnostics">` containing: counts summary line, per-marker provenance summary, the 10 check result lines (PASS/FAIL), the AI-SUGGESTED density-warning line (with `class="hidden"` if ≤ 50%), and (on Override runs) per-flagged-item lines. |
| `{{CATALOGUE_BLOCK}}` | Pre-rendered `<section class="catalogue">` containing the six Tier-1 tables in fixed order (Scenarios, Participants, Messages, Combined fragments, Cross-scenario matrix). The diagnostics section is rendered separately via `{{DIAGNOSTICS_BLOCK}}` — not duplicated inside the catalogue block. |
| `{{SVG_DIAGRAMS_BLOCK}}` | Pre-rendered `<section class="sequence-diagrams">` containing zero-to-N `<figure class="sequence-diagram seq-{slug}">` blocks. If the consultant selected zero scenarios, this placeholder renders as a single `<p class="diagrams-empty">No diagrams were selected. The catalogue tables above are the deliverable.</p>`. |
| `{{MERMAID_BLOCK}}` | Pre-rendered `<details class="mermaid-source">` containing zero-to-N `<pre>` blocks: one Mermaid `sequenceDiagram` source per selected scenario, in the same order as the SVG figures. If zero scenarios selected, renders as `<!-- no mermaid equivalents -->`. |

### SVG conventions

- `viewBox="0 0 W H"` where `W` is computed from participant count × `lane_width` + padding, and `H` from message count × `message_row_height` + header/footer padding.
- `role="img"` + `aria-label="Sequence diagram for <scenario_display_name>"` on every `<svg>`.
- All `<text>` nodes XML-escape participant ids, message labels, and guard expressions.
- **Shared `lane_width` across all scenarios in a single render.** `lane_width = max(160, longest_participant_label_pixels + 40)` computed across the union of participants from selected scenarios. This keeps participants visually aligned when the consultant scrolls between figures.
- Arrowhead markers (`<defs><marker id="sync-arrow">`, `id="async-arrow"`, `id="return-arrow"`) defined once per SVG.
- Message labels truncated to 60 chars with `<title>` tooltip carrying the full text.

### Layout grid (per SVG)

- **Participant columns.** `x_i = padding_x + i * lane_width + lane_width / 2` for participant index `i` (0-based, left-to-right in topological order of first invocation, actor leftmost, external systems rightmost).
- **Header band.** Participant boxes drawn at `y = padding_y` with `height = header_height`. Box centred on `x_i`.
- **Lifelines.** Dashed vertical lines from `(x_i, padding_y + header_height)` to `(x_i, padding_y + header_height + n_messages * message_row_height)` with `stroke-dasharray="4 4"`.
- **Message rows.** Each message at `y = padding_y + header_height + (seq - 0.5) * message_row_height`. Arrow from sender `x_from` to receiver `x_to` at this `y`.
- **Activation bars.** `<rect class="activation-bar" x="x_to - 5" y="y_call" width="10" height="(y_return - y_call)"/>` centred on receiver lifeline. Spans from the sync call's y to the matching return's y. For fire-and-forget syncs, span is one `message_row_height`.
- **Fragment frames.** `<rect class="fragment-frame" x="frame_x" y="frame_y" width="frame_w" height="frame_h"/>` where `frame_x = lane_x_min - padding_frame`, `frame_y = y_span_first - margin`, `frame_h = y_span_last - y_span_first + 2 * margin`. Top-left tab: `<rect class="fragment-tab"/>` with `<text class="fragment-label">[alt: guard]</text>` inside.

### CSS class contract used by the analyser

The template scaffold owns CSS variables, layout, and typography. The analyser emits HTML using the following named classes:

- `.catalogue` — outer container for Tier 1 tables.
- `.scenarios-table`, `.participants-table`, `.messages-table`, `.fragments-table`, `.matrix-table` — one per section.
- `.sequence-diagrams` — outer container for Tier 2 figures.
- `.sequence-diagram` — applied to every `<figure>`; one `.seq-{slug}` modifier per scenario.
- `.diagrams-empty` — applied to the `<p>` when zero scenarios selected.
- `.lifeline`, `.participant-box`, `.participant-label`, `.activation-bar`, `.message-arrow`, `.message-label`, `.message-label-bg`, `.fragment-frame`, `.fragment-tab`, `.fragment-label` — inside SVG.
- `.arrow-sync`, `.arrow-async`, `.arrow-return` — applied to `<path>` elements per message kind.
- `.kind-actor`, `.kind-system-component`, `.kind-external-system` — pill badges in the participants table.
- `.fragment-type-alt`, `.fragment-type-opt`, `.fragment-type-loop` — pill badges in the fragments table.
- `.provenance-from-task-flow`, `.provenance-derived`, `.provenance-ai-suggested` — exactly one per content row in any table.
- `.ai-suggested` — applied to any cell whose content carries the `[AI-SUGGESTED]` prefix. Renders italic + dim background.
- `.matrix-cell-present`, `.matrix-cell-absent` — matrix table cell variants.
- `.mermaid-source` — applied to the `<details>` wrapping the Mermaid `<pre>` blocks.
- `.rev-marker` — applied to any row flagged by a failed quality check on an Override run.

The analyser does **not** edit the template's CSS or layout — only the documented `{{placeholders}}` are substituted.

---

## Downstream consumption (handled by `framework/skills/map-sequence-diagram-to-ui.md`)

- **Scenarios** → screen-flow inventory. Each `primary` scenario maps to a sequence of screen transitions in the design spec.
- **External-system participants** → UI integration points: loading states, error banners, retry CTAs, timeout messages.
- **`alt` branches** → error-state UI variants (e.g., the `payment failure` branch becomes an error screen or modal).
- **`opt` fragments** → conditional UI sections (e.g., dual-approval CTA appears only when `amount > 10000`).
- **`loop` fragments** → list/iterative UI patterns (e.g., batch operations, retry indicators).
- **Cross-scenario participant matrix** → component-reuse hints for the design system (a participant used in 5+ scenarios warrants a first-class component).

`framework/skills/map-sequence-diagram-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character file and for future downstream design-spec authors.
