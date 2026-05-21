<!-- ROLE: asset (analysis reference). Methodology definition for the swim-lane-process-mapping input-analyser. Modelled on framework/assets/analyses-inputs/task-analysis-reference.md (sibling input-side HTML+YAML MVP) and framework/assets/analyses/activity-diagram-reference.md (requirements-side Mermaid + swimlane cousin). Industry framing: Rummler-Brache Cross-Functional Process Mapping + Disconnect Analysis (Rummler & Brache 1990, *Improving Performance: How to Manage the White Space on the Organization Chart*), framed under BABOK 10.35 Process Modelling. Distinct from the analyse-requirements/activity-diagram methodology: this analyser operates on RAW inputs (manifest + per-tier files), produces Rummler-Brache cross-functional flowcharts + a Disconnect Register, and emits a self-contained HTML artefact whose embedded YAML process model is the downstream re-ingestion contract for /requirements. -->

# Swim-Lane Process Mapping reference

> **Method:** Walk every consumable source enumerated in `requirements/source-manifest.json` and produce a **Rummler-Brache cross-functional process map + Disconnect Analysis** (Rummler & Brache 1990) of every discrete process the inputs describe. Each process is rendered as a Mermaid `flowchart TD` with one `subgraph` swim-lane per actor; every node carries a `[SRC: <filename>]` citation to a manifest row (or `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` if inferred). The analytical core is the **Disconnect Register** — every lane-to-lane handoff is classified `clean | ambiguous-trigger | missing-actor | unstated-exception | conflicting-source`, exposing the "white-space" gaps Rummler attributed 80% of process failures to. Inferred routing nodes and inferred lane assignments are permitted but must be marked `inferred: true` and surfaced; **inferred trigger events on the disconnect register are forbidden** (a fabricated trigger would propagate a fabricated requirement downstream).

**Output file:** `analyse-inputs/SWIM-LANE-PROCESS-MAPPING/swim-lane-process-mapping.html` — a self-contained HTML5 artefact with inline CSS, an inline YAML process model inside a `<pre><code class="language-yaml">` block (the LLM-readable copy that survives markitdown HTML→MD conversion when re-ingested via `input/`), a process gallery of Mermaid `flowchart TD` diagrams with swim-lane `subgraph`s, an actor inventory table, a **Disconnect Register**, and a collapsed diagnostics section. Browsable directly via `file://`.

**Analyser agent:** `framework/agents/analyses-inputs/swim-lane-process-mapping-analyser.md`

**Character:** `framework/assets/characters/swim-lane-process-mapping-inputs-analysis.md`

**Template:** `framework/assets/analyses-inputs/template-swim-lane-process-mapping.html`

---

## Industry framing — Rummler-Brache + BABOK 10.35

### A. Rummler-Brache Cross-Functional Process Mapping

- **Origin.** Rummler, G. A., & Brache, A. P. (1990). *Improving Performance: How to Manage the White Space on the Organization Chart*. Jossey-Bass. Second edition 1995, third edition 2013. The book introduced the **swim-lane diagram** to process modelling (since trademarked by iGrafx in 1996 as "Swimlane", but the methodology is in the original Rummler & Brache work).
- **Central claim.** *"Most process failures occur not within a department, but at the handoff points between departments — in the 'white space' of the organization chart."* Rummler estimated up to **80% of process problems** trace back to these inter-actor interfaces. The swim-lane notation makes the handoffs visually obvious; the analytical follow-on is the **Disconnect Analysis** — every handoff classified for completeness.
- **Three Levels of Performance.** Organization / Process / Job (Performer). This analyser operates at the **Process** level — the swim-lane diagram is its canonical artefact. The Organization level (organisation chart, value chain) and the Job level (per-performer job model, performance variables) are out of scope; see §C below.
- **Output shape.** Per process: a directed flow graph rendered with one `subgraph` swim-lane per actor (`actor` = role / department / system / external service). Nodes are typed (`start`, `end`, `process`, `decision`, `data-store`, `external-system`). Edges are typed (`flow` — control passes within a lane; `handoff` — control crosses between lanes). Handoffs are first-class because they are the methodology's analytical target.

### B. Disconnect Analysis (the analytical core)

Rummler & Brache (1990, ch. 6 "Designing the New Process") introduce **disconnects** as the unit of analysis for process improvement. Every handoff is examined for one of five disconnect categories — five rather than the original Rummler-Brache three because under-specified prose inputs evidence two additional failure modes (`missing-actor`, `conflicting-source`) that the original 1990 framing assumed away (real-world processes have known actors and a single source of truth):

| Category | Detection signal in inputs | Why it matters |
|---|---|---|
| `clean` | The inputs explicitly name **(a) the source actor / step, (b) the trigger event, (c) the receiving actor, (d) the payload that crosses the lane boundary**. All four are present and unambiguous. | The handoff is sound. No follow-up needed. |
| `ambiguous-trigger` | The inputs describe the handoff but the trigger event is under-specified ("once approved, finance pays the vendor" — *who* signals approval to finance? An email? A status change? A queue?). | Downstream requirements will guess at the integration shape. Surface for consultant follow-up. |
| `missing-actor` | The inputs describe an outbound action from one lane without naming the receiver ("the system sends a notification" — to whom? Customer? Manager? Audit log?). | A missing receiver corrupts the lane set; downstream design can't allocate ownership. |
| `unstated-exception` | The happy-path handoff is present but the failure / exception / timeout path is not described ("manager approves the expense" — what if the manager doesn't approve, or doesn't respond?). | Acceptance criteria will be silently incomplete; the exception branch becomes a runtime surprise. |
| `conflicting-source` | Two manifest sources describe the same handoff with materially different details (brief says "manager approves over $1000"; interview notes say "director approves over $500"). | A real conflict the consultant must resolve before requirements drafting; silent merging hides the disagreement. |

A handoff that fits none of the five categories falls back to `clean` (the analyser is conservative — it does not invent disconnects to inflate the register; spurious disconnects waste consultant attention more than they help).

Every disconnect entry carries:

```
{
  disconnect_id,                              // DC-NNN sequential within the run
  process_id,                                 // which process the handoff belongs to
  from_step_id,                               // the step the handoff originates from
  from_lane,                                  // the source lane id
  to_step_id,                                 // the step the handoff terminates at
  to_lane,                                    // the receiver lane id
  category,                                   // one of the five above
  description,                                // one short sentence stating the disconnect
  sources,                                    // [SRC: <filename>] for the handoff and the discrepancy
  consultant_follow_up: yes | no,             // yes for everything except `clean`
  suggested_question,                         // the resolver-style prompt the consultant would answer
  ai_id                                       // AI-NNN if the disconnect is itself inferred (rare)
}
```

The register is the artefact's analytical bite — without it, the methodology degrades to "here is a flowchart" and provides almost none of the value claimed for Rummler-Brache.

### C. Variants considered and rejected

| Variant | Rejected because |
|---|---|
| Full Rummler-Brache Nine Performance Variables (Org × Process × Job × Goals/Design/Management matrix) | A strategic-improvement framework requiring stakeholder interviews and organisational KPI data. The evidence is not in the documents. Process-level disconnect analysis is the load-bearing depth. |
| BPMN 2.0 (OMG 2011) | A formal notation standard with pools / message flows / intermediate events / compensation handlers / signal events. Mermaid has no native BPMN renderer; under-specified consultant inputs cannot supply BPMN-level rigor; using BPMN here would force pervasive `[AI-SUGGESTED]` on shape semantics. May be promoted from `status: future` to `status: mvp` later if input fidelity justifies it. |
| Value Stream Mapping (Rother & Shook 1999, *Learning to See*) | A Lean methodology focused on value-add vs non-value-add time and waste identification (over-processing, waiting, transport). Strong for manufacturing and operations; consultant inputs for software products rarely supply the quantitative cycle-time data VSM requires. May be promoted later as a separate `value-stream-mapping` row. |
| IDEF3 Process Description Capture Method (KBSI 1995) | Distinguishes Process Schematics (UOB Networks) from Object Schematics; requires formal junction logic (`&`/`X`/`O` types). Useful for DoD process modelling; overkill for raw consultant inputs in a CRUD software context. |
| Pure flowchart (ANSI X3.5 / ISO 5807) | A notation standard without an analytical layer. Without the disconnect register the artefact would be "here is a flowchart" — methodologically thin. Rummler-Brache layers analysis on top, which is the value-add. |
| UML Activity Diagrams (OMG 2.5) | The `/analyse-requirement/activity-diagram` methodology already covers this — operating on synthesised `requirements/requirements.md`. The input-side variant deliberately picks Rummler-Brache to anchor the methodological emphasis on **disconnect analysis** rather than full UML control-node fidelity. |

### D. Why apply swim-lane process mapping to raw inputs (not the synthesised requirements doc)

| Lens | Methodology | Question answered | Operates on |
|---|---|---|---|
| Vocabulary × definitions | glossary (input variant) | Which terms appear in the raw material? | raw `input/` |
| Cross-cutting patterns | thematic-analysis | What recurring patterns do the inputs carry? | raw `input/` |
| Discovery tree | opportunity-solution-trees | Outcomes → opportunities → solutions in the inputs? | raw `input/` |
| Current-state user workflow | journey-mapping | How does the user move through the as-is workflow? (linear, persona-shaped) | raw `input/` |
| Goal decomposition × per-terminal data | task-analysis | What atomic operations does the user perform, in what coordination structure, against what data? (hierarchical, goal-shaped) | raw `input/` |
| **Cross-functional process × handoff disconnects** | **swim-lane-process-mapping** | **What discrete processes do the inputs describe, who owns each step, and where do the handoffs between actors break down?** | **raw `input/`** |

Swim-lane process mapping is **complementary** to `journey-mapping` and `task-analysis`: a journey map is linear and persona-shaped (one persona's emotional arc through a workflow); an HTA is hierarchical and goal-shaped (root goal → sub-goals → terminals); a swim-lane process map is **multi-actor and handoff-shaped** (cross-functional flow with explicit responsibility transfer). The three methodologies surface different signals — running all three before `/requirements` is the high-leverage combination when the inputs describe multi-stakeholder processes (claim approval, onboarding, dispute resolution, escalation paths).

### E. Distinction from `/analyse-requirements/activity-diagram`

The `/analyse-requirements/` pipeline ships a sibling methodology called `activity-diagram` (UML 2.5 activity-diagram catalogue with swim-lane partitioning). It reads the synthesised `requirements/requirements.md`. **This analyser is distinct** for four reasons:

1. **Different input source.** `activity-diagram` reads `requirements/requirements.md`; this analyser reads `requirements/source-manifest.json` + the raw `input/*` files it enumerates.
2. **Different citation grammar.** `activity-diagram` cites `§5.N` task-flow sections; this analyser uses `[SRC: <filename>]` (manifest row `filename` field).
3. **Different methodological emphasis.** `activity-diagram` produces a UML 2.5 catalogue (initial / activity-final / decision / merge / fork / join + control-flow edges) for design-spec authoring; this analyser produces a **Rummler-Brache cross-functional map + Disconnect Register** for surfacing the gaps in the consultant's input set before `/requirements` runs.
4. **Different downstream contract.** `activity-diagram` is read by design-spec authors after requirements are merged; this analyser's primary downstream consumer is the consultant (the Disconnect Register drives the follow-up elicitation) and secondarily the `/requirements` drafter (the embedded YAML process model becomes acceptance-criteria scaffolding).

The two are complementary; consultants commonly run this one before `/requirements` and the other after.

### F. Why this analyser uses HTML + embedded Mermaid + embedded YAML

- **Multi-process gallery.** A process map gallery (one diagram per discrete process) is markedly easier to scan as HTML sections than as a single Markdown stream. Sibling `journey-mapping`, `task-analysis`, and `jtbd` are the input-side HTML precedents.
- **Mermaid source-as-text.** The analyser embeds each process's Mermaid `flowchart TD` source inside `<pre class="mermaid-source">` blocks (matching the requirements-side `activity-diagram` precedent). The artefact ships **no inline Mermaid runtime and no external CDN** — the no-CDN, no-external-resources constraint is framework-wide. Consultants view the rendered diagram via either `mmdc` (the validator's own CLI) or a Mermaid live editor (`https://mermaid.live`) by copy-pasting the source block. Validation via `framework/skills/mermaid-validator.md` before write confirms every embedded Mermaid block parses cleanly.
- **Re-ingestible structure.** The artefact's secondary downstream use is as a re-fed input to `/requirements`. The consultant copies `analyse-inputs/SWIM-LANE-PROCESS-MAPPING/swim-lane-process-mapping.html` into `input/`, the input-handler classifies it as `Supported-via-MCP`, markitdown converts to `input/swim-lane-process-mapping.html.converted.md`, and the drafter reads the converted markdown via the manifest. **`<pre><code class="language-yaml">` blocks survive markitdown's HTML→MD conversion as fenced code** — so the structured YAML process model lives in a `<pre><code>` block (not a `<script type="application/json">` block, which markitdown strips). The Mermaid source blocks also degrade to `<pre>` text in the converted markdown, so the drafter sees both the structured model and the diagram source.
- **Self-contained.** Inline `<style>`, no external CSS / fonts / CDN / JS. Network-isolated; browsable via `file://`; shareable as a single attachment.

---

## Output structure

The artefact has a fixed top-to-bottom shape, populated into `framework/assets/analyses-inputs/template-swim-lane-process-mapping.html` via documented placeholder substitution:

1. **Header banner** (`<header id="overview">`) — title, generation timestamp, manifest sha256 (first 12 chars), manifest row count consumed / skipped, target-mode (prototype / application, from the manifest's `target` field if present), run number, summary counts (processes / actors / steps / handoffs / disconnects-by-category). Includes a `<nav class="toc-processes">` with jump-links to each process section.
2. **Process gallery** (`<section id="processes">`) — for each discrete process: `<article class="process-block" id="process-{process-slug}">`. Each article contains:
   - `<h2>` with process id + name + a one-line goal statement (cited).
   - **Mermaid source** (`<pre class="mermaid-source">` containing the `flowchart TD` source with `subgraph` swim-lanes per actor — see "Mermaid emission shape" below). Rendered visual is out-of-band (consultants use `mmdc` or `https://mermaid.live` to view).
   - **Steps table** — every step in the process: id, label, lane, type (`start` / `end` / `process` / `decision` / `data-store` / `external-system`), source citation.
   - **Decisions table** — every decision node with its branch labels and source citations.
3. **Actor inventory** (`<section id="actors">`) — `<table>` listing every lane discovered across all processes: id, display name, kind (`role` / `system` / `external-service`), processes it appears in, source citations.
4. **Disconnect Register** (`<section id="disconnects">`) — the analytical core. A table with one row per handoff: disconnect id, process, from-step + lane, to-step + lane, category pill (colour-coded), description, source citations, consultant follow-up flag, suggested question. Followed by a per-category summary (counts of `clean` / `ambiguous-trigger` / `missing-actor` / `unstated-exception` / `conflicting-source`).
5. **Structured YAML model** (`<section id="structured-model">`) — `<pre><code class="language-yaml">` block carrying the full machine-readable process model. Schema below. This is the load-bearing re-ingestion contract for the `/requirements` drafter when the consultant copies the artefact into `input/`.
6. **Gaps and inferred nodes** (`<section id="gaps">`) — every `inferred: true` node, every `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` marker in the tree, with the suggested consultant prompt and the source span where the inference was made. Distinct from the Disconnect Register (which classifies handoffs); this section classifies inferred nodes / lanes / routing.
7. **Diagnostics** (collapsed `<details id="diagnostics">`) — counts summary, the 9 quality-gate results (PASS / FAIL), source roster (consumed + skipped tables), manifest fingerprint, run history (append-only bullet list), Mermaid validation results.
8. **Next steps banner** (after diagnostics) — instructions to copy the artefact into `input/` for `/requirements` re-ingestion; reminder that the Disconnect Register is the primary elicitation surface for the next consultant conversation.

Section order lives in the template, not in the analyser. The analyser emits the same placeholder blocks regardless; the template decides where they land.

### Mermaid emission shape (per process)

```
flowchart TD
    subgraph lane_user["User"]
        s1["Submit expense<br/>[SRC: brief.docx]"]
        s2["Attach receipt<br/>[SRC: brief.docx]"]
    end
    subgraph lane_finance["Finance"]
        s3{"Amount > $1000?<br/>[SRC: brief.docx]"}
        s4["Validate claim<br/>[SRC: interview-notes.md]"]
        s5["Pay vendor<br/>[SRC: brief.docx]"]
    end
    subgraph lane_manager["Manager"]
        s6["Approve / Reject<br/>[SRC: brief.docx]"]
    end
    s1 --> s2 --> s3
    s3 -->|"≤ $1000"| s4
    s3 -->|"> $1000"| s6
    s6 -->|"approved"| s4
    s6 -->|"rejected"| send[(end: rejected<br/>[AI-SUGGESTED: AI-001 | blocking])]
    s4 --> s5 --> ende[(end: paid<br/>[SRC: brief.docx])]
```

Conventions:

- One `subgraph` per actor lane. Lane id = `lane_<kebab-actor-id>`. Display name = the actor's name in `"…"`.
- Step nodes: `s<N>` (sequential per process), label inside `["..."]` with `<br/>` between label and citation.
- Decision nodes: `{"..."}` (rhombus shape in Mermaid).
- Terminal nodes: `[(end: ...)]` (stadium shape) for `end`; `([start: ...])` (rounded) for `start`. Each process must have ≥ 1 start and ≥ 1 end.
- Decision branches carry guard labels: `s3 -->|"guard expression"| target`.
- Inferred nodes and inferred handoffs carry `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` in their label text after a `<br/>`.

The Mermaid runtime renders this in-browser. The `framework/skills/mermaid-validator.md` skill is invoked at Step 10 sub-step C with the extracted Mermaid source per process to confirm syntactic validity before write.

### Structured-model YAML schema (embedded in `<pre><code class="language-yaml">`)

```yaml
swim_lane_process_mapping:
  manifest_sha256: <hex>
  generated_at: <ISO-8601 UTC>
  run_count: <int ≥ 1>
  target: prototype | application | (not declared in manifest)
  actors:
    - id: <kebab-case>
      display_name: <verbatim from inputs or sentence-case derivation>
      kind: role | system | external-service
      processes: [<process_id>, ...]
      sources: ["[SRC: <filename>]", ...]
      inferred: false
      confidence: high | medium | low
  processes:
    - id: <kebab-case>
      display_name: <sentence-case>
      goal: <one-line outcome statement, cited>
      trigger: <event that starts the process, cited>
      sources: ["[SRC: <filename>]", ...]
      steps:
        - id: <s1, s2, …>
          label: <verb phrase or decision question>
          type: start | end | process | decision | data-store | external-system
          lane: <actor_id>
          branches:                           # populated for type: decision only
            - guard: <expression cited>
              target_step_id: <id>
              sources: [...]
          sources: [...]
          inferred: false
          confidence: high | medium | low
      handoffs:
        - id: <h1, h2, …>
          from_step_id: <id>
          to_step_id: <id>
          payload: <what crosses the lane boundary, cited or inferred>
          sources: [...]
      disconnects:                            # the analytical core
        - id: DC-NNN
          handoff_id: <h_id>
          category: clean | ambiguous-trigger | missing-actor | unstated-exception | conflicting-source
          description: <one short sentence>
          sources: [...]
          consultant_follow_up: yes | no
          suggested_question: <resolver-style prompt>
          ai_id: AI-NNN                       # present only if the disconnect itself is inferred
```

YAML invariants:

- `actors` is a flat array; `processes` is a flat array; each process embeds its `steps`, `handoffs`, and `disconnects`.
- Every step has `lane ∈ actors[*].id`.
- Every handoff has `from_step_id` and `to_step_id` whose `lane` differs (intra-lane edges are not handoffs).
- Every handoff has exactly one corresponding `disconnect` entry (1:1 mapping; `category: clean` for the sound handoffs).
- Every node has at least one source citation OR `inferred: true`.
- Each process has ≥ 1 step with `type: start` and ≥ 1 step with `type: end`.

### Multi-process handling

The expected shape is **≥ 1 discrete process per analysis**. If the inputs evidence ≥ 5 viable processes (broad scope — a full enterprise workflow set), surface an `AskUserQuestion` at Round 2 with two options: `All — render all {{N}} processes (Recommended for completeness)` and `Top-{{K}} — render the K highest-evidence processes; defer the rest to a follow-up run`. Multi-process artefacts render each process in its own `<article class="process-block">` with its own Mermaid diagram; the YAML carries multiple entries under `processes`.

If the inputs evidence **zero** discrete processes (no source describes a multi-step workflow with at least two actors and at least one handoff), halt with: *"Cannot produce a swim-lane process map without any cross-functional process named in the inputs — `requirements/source-manifest.json` enumerates files but none of them describe a multi-step workflow with at least two actors. If the inputs describe a single-actor workflow, consider `/analyse-inputs` → `task-analysis` instead. If they describe persona-shaped user emotion, consider `journey-mapping`. Add a brief, interview note, or process description that names ≥ 2 actors with a handoff between them, then re-invoke `/analyse-inputs`."* No `AskUserQuestion`; this is a hard halt analogous to RF-03.

---

## Workflow rounds (8 rounds + 4 operational steps = 12 workflow steps)

Each round produces a distinct, named in-memory output. The analyser does not write the artefact until Round 8 is complete and all 9 hard quality checks have passed (or the consultant chose Override).

### Round 1 — Process discovery

- For each row in `consumed_rows`, scan the content for **process candidates** — sequences of steps that involve ≥ 2 actors with at least one explicit handoff. Signals:
  - Numbered workflows ("1. User submits ... 2. Finance validates ... 3. Manager approves ...").
  - Process diagrams in `Native-multimodal` rows (the Read tool surfaces image bytes — transcribe steps and arrows).
  - Section headers naming workflows ("Expense submission", "Customer onboarding", "Dispute resolution").
  - Verb chains crossing actor mentions ("the user uploads X, then finance validates Y and forwards to the manager").
- A process candidate is `{candidate_id, candidate_display_name, source_filenames, source_quote, evidence_strength: high|medium|low}`.
- **No invented processes.** A candidate must be traceable to verbatim mentions in ≥ 1 source.
- **Multi-process cap.** If candidates > 5 with comparable evidence weight, surface the `AskUserQuestion` per §Multi-process handling.

Output: a `process_candidates` list. Deduplicate cross-source mentions of the same process; merge `source_filenames`.

### Round 2 — Actor extraction

For each process candidate, enumerate the actors:

- Walk the candidate's source spans for **named subjects of verb actions** ("the user submits", "Finance validates", "the manager approves", "the system sends"). Each named subject becomes a candidate actor.
- Classify each actor's `kind`:
  - `role` — a human role (User, Customer, Manager, Finance, Approver, Reviewer, Admin).
  - `system` — an internal system component (Order Service, Notification Service, Approval Workflow Engine).
  - `external-service` — a third-party or external system (Payment Gateway, Identity Provider, Email Service).
- **Naming consistency across processes.** An actor named "Finance" in process A must be the same actor in process B. Pick canonical names; alias variants in notes.
- **Inferred actors permitted, inferred *named* actors forbidden.** If a verb action has no subject ("the request is approved" — passive voice), do not invent a named actor; mark the step as missing-actor in Round 6 and surface the `[AI-SUGGESTED]` for the lane assignment specifically, with `ai_id` flagged blocking.

Output: per process, the `actors` list; plus the global actor inventory (deduplicated across processes).

### Round 3 — Step extraction + typing

For each process, walk the source spans and extract the **steps in evidenced order**:

- Each step carries `{id, label, type, lane, source_filenames, source_quote, inferred, confidence}`.
- `id` is `s1, s2, …` sequential within each process.
- `label` is a short verb phrase for `process` / `start` / `end` steps; a yes/no question or decision phrase for `decision` steps; a noun for `data-store` / `external-system` steps.
- `type` is one of:
  - `start` — process entry point (exactly ≥ 1 per process). Typically named ("triggered when X happens") or inferred from the first verb in the source's evidenced order.
  - `end` — process exit point (≥ 1 per process; multiple ends are common — approved-path end + rejected-path end + timeout end).
  - `process` — an atomic step performed by an actor. The default.
  - `decision` — a branching point. Must have ≥ 2 outgoing edges with explicit guard labels (Round 4).
  - `data-store` — a persistent record the process reads or writes (database table, log, document store).
  - `external-system` — an out-of-system service call (payment, email, SMS, identity).
- `lane` references an actor from Round 2. If the step has no named subject, the lane is inferred (mark `inferred: true` with `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` per Round 6).
- **Inferred routing steps permitted; inferred trigger events on handoffs forbidden.** If a step is implied by the surrounding context but not named in the inputs, mark `inferred: true`. If a *handoff trigger* (the event that causes one lane to pass control to another — see Round 4) would have to be inferred, do not invent it: surface as an `ambiguous-trigger` disconnect in Round 6 instead.
- **No "and" / "then" / "etc" in step labels.** A label like `validate and approve` is two steps; split.

Output: per process, the `steps` list, ordered by evidenced sequence.

### Round 4 — Edge labelling + handoff identification

For each process:

- Walk consecutive step pairs `(s_i, s_{i+1})` in evidenced order. For each pair:
  - If `lane(s_i) == lane(s_{i+1})`: emit a `flow` edge (intra-lane; no handoff).
  - If `lane(s_i) != lane(s_{i+1})`: emit a `handoff` edge `{id, from_step_id, to_step_id, payload, sources, inferred, confidence}`. **Handoffs are first-class because they are the Disconnect Analysis target.**
- For each `decision` step, emit one outgoing edge per branch. Capture the guard expression verbatim where the inputs name it; `[AI-SUGGESTED]` mark inferred guards (especially unstated "else" branches — surface as `unstated-exception` in Round 6 if the unstated branch corresponds to a failure path).
- The `payload` field describes **what crosses the lane boundary** (a form, a record, a status, a notification, a signal). Cite the source span describing it; mark `inferred: true` if the inputs imply but don't name the payload.

Output: per process, the `handoffs` list and the decision-branch edge set.

### Round 5 — Disconnect classification (the analytical core)

For every handoff in every process, apply the five-category classification from §B above:

- Walk the handoff's source citations and adjacent source spans.
- Check the four cleanliness conditions (named source / trigger / receiver / payload). If all four are present and unambiguous → `clean`.
- Otherwise, apply the disconnect rubric in this order (first match wins, except that `conflicting-source` always preempts others when a real conflict exists):
  1. `conflicting-source` — same handoff described materially differently across ≥ 2 manifest sources. Document both descriptions in `description`; cite both filenames.
  2. `missing-actor` — outbound from a lane with no named receiver. The "to_lane" was inferred; mark it `[AI-SUGGESTED]`.
  3. `unstated-exception` — a happy-path handoff present, but a corresponding failure / timeout / rejection path is missing (e.g., manager approves → finance pays; but what happens on rejection?).
  4. `ambiguous-trigger` — handoff present, but the trigger event is under-specified (silent on "how" the handoff fires — email? status change? polling?).
- Allocate `DC-NNN` ids sequentially across the run (not per process — the global counter makes the Disconnect Register a single audit surface).
- Each disconnect entry's `consultant_follow_up: yes` for everything except `clean`. The `suggested_question` is the resolver-style prompt: *"What event triggers the handoff from `<from-lane>` to `<to-lane>` after `<from-step-label>`?"* / *"Who receives the notification from `<from-lane>` after `<from-step-label>`?"* / *"What happens on the failure / rejection branch of `<from-step-label>` in `<from-lane>`?"* / *"`<filename-A>` and `<filename-B>` describe the handoff from `<from-lane>` to `<to-lane>` differently — which is correct?"*

Output: per process, the `disconnects` list; the global Disconnect Register is the union.

### Round 6 — Gap classification (inferred-node level, distinct from disconnects)

Walk the in-memory model and classify every `inferred: true` node:

- **Inferred actors** that have no `[SRC: <filename>]` anywhere → block downstream lane assignment; mark `blocking: true` and allocate `AI-NNN`.
- **Inferred routing steps** (steps implied but not named) → `blocking: false` if low-leverage (the process flow is comprehensible without them); `blocking: true` if the step is gated by a decision branch with a stated guard.
- **Inferred handoff payloads** → `blocking: false` (the integration shape can be resolved later); becomes a soft signal for `/requirements` `§7 Data entities`.
- **Inferred decision guards** (especially silent "else" branches) → already classified as `unstated-exception` disconnects in Round 5; do not double-count.

Each gap entry carries `{ai_id, marker: "[AI-SUGGESTED: AI-NNN | blocking|non-blocking]", kind, node_id, blocking, suggested_prompt, source_span}`. Use the shared `AI-NNN` namespace with `framework/shared/general-rules.md` and the `/requirements` drafter / resolver — same grammar as `task-analysis` and the drafter itself.

The model is **closed** at the end of Round 6. Steps 10–11 must not add steps, handoffs, disconnects, or gap entries.

### Round 7 — Self-validate (9 hard gates + 4 structural integrity checks)

Run all 9 hard gates from §Quality gates below, plus four structural integrity checks. On any failure → §Failure handling.

### Round 8 — Render + write + verify

- Read `framework/assets/analyses-inputs/template-swim-lane-process-mapping.html` once.
- Build the substitution map (placeholders documented in the template's header comment + §Output structure above).
- HTML-escape every consultant-supplied string before injection (`<`, `>`, `&`, `"`, `'`). Mermaid source inside `<pre class="mermaid">` is rendered as plain text (the Mermaid runtime parses it at page-load); do **not** HTML-escape `-->`, `|`, `[`, `]`, `{`, `}` inside the Mermaid blocks (those are Mermaid syntax). YAML inside `<pre><code class="language-yaml">` is rendered as plain text within the block — do not double-escape inside YAML.
- For each process, invoke `framework/skills/mermaid-validator.md` with the extracted Mermaid source. On `not-installed` → halt per the validator's own contract. On syntax errors → fix and re-validate until clean (the validator skill auto-fixes per its own workflow).
- Compute the SHA-256 of the in-memory composed HTML.
- `Write analyse-inputs/SWIM-LANE-PROCESS-MAPPING/swim-lane-process-mapping.html`. Invoke `framework/skills/verify-artifact-write.md` with `expected_sha256` and `expected_min_bytes = 4096`. On `RF-04 trigger` → halt and fail handback.
- Hand back to the orchestrator with the Accept / Revise / Restart loop.

---

## Provenance markers

Every node, every actor, every handoff, every disconnect, and every gap carries either source citations or an inference marker. Three marker shapes:

| Marker | Used in | Payload | Meaning |
|---|---|---|---|
| `[SRC: <filename>]` | YAML `sources` arrays, Mermaid node label suffixes, table source-citation cells, process header citations | basename + extension, matching a manifest row's `filename` field | The node / actor / handoff / disconnect is anchored to this manifest source. |
| `[AI-SUGGESTED: AI-NNN \| blocking\|non-blocking]` | inferred non-trigger nodes, inferred lane assignments, inferred routing steps, inferred handoff payloads (only) | sequential AI-NNN from the shared namespace; classification per Round 6 | The node / lane / step / payload was inferred from context, not directly cited. Surface to consultant via resolver. **Never used on disconnect triggers** (a fabricated trigger would propagate fabricated requirements). |
| `[DISCONNECT: DC-NNN]` | Mermaid edge label suffixes for non-`clean` handoffs (optional; the register is the canonical surface), Disconnect Register row anchors | sequential DC-NNN per run | Diagnostics-side marker linking a Mermaid edge to its register entry. |

**No fourth marker.** **`[AI-SUGGESTED]` on disconnect triggers is forbidden** — a fabricated trigger event in the disconnect register is the worst failure mode (it propagates a fabricated requirement downstream).

---

## Source-of-truth hierarchy

The analyser walks the manifest in this order:

1. **`Native-text` rows** → read `original_path` directly as text. The richest source for actor and verb extraction.
2. **`Native-multimodal` rows** → read `original_path` (Claude vision surfaces image bytes). Transcribe visible text and structurally significant observations. Process diagrams, BPMN sketches, whiteboard photos often carry the explicit handoff structure the prose lacks — these are high-leverage sources for this analyser.
3. **`Supported-via-MCP` rows** → read `converted_sibling` (the `.converted.md` that the input-handler produced via markitdown). Do **not** re-invoke `markitdown-mcp` — the manifest's `converted_sibling` is the contract.
4. **`Unsupported` rows** → skipped; recorded in `Source roster > Skipped` with the manifest's `conversions_applied` reason.

The analyser **never** reads:

- Any path under `requirements/` other than `requirements/source-manifest.json` and the manifest-enumerated source files.
- Any path under `framework/state/`.
- Any path under `framework/shared/` (textual `RF-NN` / `GR-NN` references are links for the reader, not file loads).
- Other analyses' artefacts (`analyse-requirements/<OTHER-METHOD>/...`, `analyse-inputs/<OTHER-METHOD>/...`). Optionally re-reads the prior `analyse-inputs/SWIM-LANE-PROCESS-MAPPING/swim-lane-process-mapping.html` for the additive merge.

---

## Quality gates (9 hard gates)

Run at Round 7 close, before render. Each check operates on the in-memory state.

1. **Citation completeness.** Every actor, every step, every handoff, every disconnect carries either ≥ 1 `[SRC: <filename>]` matching a manifest row's `filename` exactly, OR `inferred: true`. **Disconnect trigger events are never `inferred: true`** (gate 9 below enforces this separately).
2. **No invented processes.** Every process has ≥ 1 source citation tracing the process name + boundary (start + end) to verbatim mentions in the inputs.
3. **Every process has ≥ 2 actors and ≥ 1 handoff.** A process with one actor and zero handoffs is a single-actor workflow — wrong methodology lens. Drop the candidate or escalate to consultant disambiguation.
4. **Every step has a non-empty `label` and a `lane` referencing an existing actor.** Labels are verb phrases for `process` / `start` / `end`; decision phrases for `decision`; nouns for `data-store` / `external-system`. Forbidden literal values: empty, `and`, `then`, `etc`.
5. **Every decision step has ≥ 2 outgoing edges with non-empty guard expressions.** Selection without explicit branches is silent confabulation; surface as `unstated-exception` if any branch is silent.
6. **Every handoff has a corresponding disconnect entry.** 1:1 mapping. Cleanliness check applied; `clean` is the explicit "no issue" classification — not the silent default. (The default for a handoff with under-specified data is one of the four non-`clean` categories, not silently `clean`.)
7. **Every process has ≥ 1 step with `type: start` and ≥ 1 step with `type: end`.** Processes without bounded entry/exit are incomplete; either surface as a `[GAP-PROCESS-UNBOUNDED]` diagnostic with explicit consultant prompt or refuse to render the process.
8. **Manifest fingerprint + source roster.** The artefact's embedded `<script type="application/json" id="swim-lane-process-mapping-meta">` block carries `manifest_sha256` equal to the Step 2 value; the diagnostics source-roster `Consumed` table enumerates every manifest row whose `tier != "Unsupported"`; the `Skipped` table enumerates every `Unsupported` row.
9. **Mermaid validity.** Every embedded Mermaid block parses cleanly via `framework/skills/mermaid-validator.md`. The validator's auto-fix loop closes any syntax issues; if a process's Mermaid cannot be made valid in three retries, drop the diagram for that process and emit a `[GAP-MERMAID-INVALID]` diagnostic naming the process.

Plus four **structural integrity checks**:

- Every `lane` reference in every step exists in the process's `actors` set.
- Every `from_step_id` / `to_step_id` in every handoff exists in the process's `steps` set; the lanes of the two steps differ (intra-lane edges aren't handoffs).
- Every `handoff_id` in every disconnect exists in the process's `handoffs` set; the mapping is 1:1 (no orphan disconnects, no handoffs missing a disconnect).
- The 5-category disconnect distribution sums to `len(handoffs)`.

### Failure handling (Revise / Override / Restart)

On any hard-gate failure: do **not** write the artefact. Surface `AskUserQuestion` with three options:

1. `Revise — exit so the consultant can enrich input/ and re-invoke /analyse-inputs (Recommended)`
2. `Override — proceed and write a known-defective artefact (Run-history bullet records every violation)`
3. `Restart — re-run from Round 1 with a fresh manifest pass`

On **Revise**: hand back to the orchestrator with a `failed-handback` state.
On **Override**: record each failing gate in the Run-history bullet for this run; proceed to render. Note: gate 6 (every handoff has a disconnect entry — the methodology's analytical-bite gate) is `Override`-able only in extremis and should almost never be; gate 9 (Mermaid validity) `Override` writes an artefact with un-renderable diagrams and is a serious accessibility failure.
On **Restart**: re-enter Round 1. Cap at three fail-Restart cycles; on the fourth, force the Revise path.

---

## Anti-patterns

All five are documented in the literature or framework conventions; each maps to a hard gate above.

1. **Confabulated processes.** The LLM analogue of inventing a process the consultant never described. Symptom: a process appears in the artefact with no `[SRC: <filename>]` citation, or with citations that don't actually describe the process. **Enforcement:** Gate 2 — every process must cite its name and boundary to verbatim mentions.

2. **Invented actors / lanes.** Symptom: a lane named "Compliance" appears in the Mermaid swim-lanes when no source names "Compliance". **Enforcement:** Round 2 inferred-actor rule (passive-voice subjects do not become invented named actors; they become `missing-actor` disconnects).

3. **Inflated disconnect register.** Symptom: every handoff classified as a disconnect to make the artefact look analytically dense. Counter-productive: spurious disconnects waste consultant attention and erode trust in the methodology. **Enforcement:** Round 5 conservatism — the cleanliness check is conjunctive (named source AND trigger AND receiver AND payload); any handoff meeting all four is `clean`. Reserve the four non-`clean` categories for handoffs that genuinely fail the test.

4. **Fabricated triggers.** Symptom: a disconnect register entry describes the trigger event ("manager's approval triggers a database update") when the inputs never name the trigger. **Enforcement:** the `[AI-SUGGESTED]` ban on disconnect triggers — surface as `ambiguous-trigger` instead; the resolver question is *"What event triggers the handoff?"* not a fabricated answer.

5. **Merged actors with different responsibilities.** Symptom: collapsing "Finance Admin" and "Finance Manager" into one "Finance" lane when the inputs treat them as distinct. **Enforcement:** Round 2 naming consistency rule — keep distinct names where the inputs distinguish them; surface a `[GAP-ACTOR-CONFLATION]` diagnostic if you collapse and the inputs later contradict the choice.

Two additional anti-patterns are framework-wide:

6. **Do not bundle external CDN / fonts / non-Mermaid JS.** The artefact is self-contained — inline CSS, an inline Mermaid runtime block (vetted minified copy from the template), no fonts, no external resources. (Frame-wide invariant; mirrors `journey-mapping`.)
7. **Do not auto-copy the artefact to `input/`.** The agent's write-isolation rule (CLAUDE.md §"Stand-alone constraints") forbids `/analyse-inputs` from writing outside `analyse-inputs/<METHOD>/*`. The trailing **Next steps** banner in the artefact instructs the consultant to copy manually; the analyser does not.

---

## Stop-condition

The analysis is complete when:

- Every process has a populated step graph, ≥ 1 start and ≥ 1 end, ≥ 1 handoff, every handoff is classified in the Disconnect Register.
- All 9 hard gates pass, or the consultant chose Override and the failures are recorded in the Run-history bullet.
- Every Mermaid block parses cleanly via the validator.
- `analyse-inputs/SWIM-LANE-PROCESS-MAPPING/swim-lane-process-mapping.html` has been written and `verify-artifact-write` returned `pass`.
- The consultant chose Accept in the handback loop.

---

## Re-run semantics

- The cursor lives in the artefact's `<script type="application/json" id="swim-lane-process-mapping-meta">` block — `manifest_sha256`, `run_count`, per-process step counts and disconnect counts. No state file under `framework/state/`.
- On re-run, the analyser compares the current manifest fingerprint to the prior cursor:
  - **No change** → pure additive widening; previously-inferred lanes may be confirmed by consultant Revise (flip `inferred: false`) when the consultant adds a new citation; previously-classified disconnects may be reclassified (e.g., from `ambiguous-trigger` to `clean` if the consultant supplies the missing trigger event).
  - **Change** → drift prompt: `append-only` (preserves prior processes verbatim; appends new processes / actors / steps where new manifest rows justify them; flags conflicts), `re-extract` (re-runs Rounds 1–7 from scratch on the current manifest; ids preserved where re-extraction produces equivalent labels), or `abort` (exit without writing).
- The artefact is monotonically growing across runs unless the consultant chose `re-extract` or manually edited the file.

---

## Downstream consumption (handled by `framework/skills/map-swim-lane-process-mapping-from-inputs-to-ui.md`)

The analyser has **two** primary downstream consumers:

1. **The consultant** — directly via the Disconnect Register. The register is the elicitation surface for the next consultant conversation; every non-`clean` disconnect carries a `suggested_question` the consultant can either answer (closing the disconnect) or push back to the original source.
2. **The `/requirements` drafter** — secondarily via re-ingestion when the consultant copies the artefact into `input/`. The drafter consumes:
   - **YAML structured model** → bijection target for `framework/skills/completeness-gap-pass.md`. Every process should map to ≥ 1 `§5 Task flows` entry; every handoff should map to ≥ 1 integration / acceptance criterion in `§6 Requirements`.
   - **Actor inventory** → `§3 Target users` and `§4 User goals & stories` hints. Roles become persona seeds; systems and external services become `§2 Domain model` aggregate-root candidates.
   - **Disconnect Register** → resolver questions. Every `consultant_follow_up: yes` row maps to a resolver-pipeline `AI-NNN` question using the existing grammar — no schema changes needed.
   - **Decision branch guards** → acceptance-criteria fodder. *"Given amount > $1000, when manager-approves, then finance-pays"* in `§6` requirements.
   - **`data-store` and `external-system` steps** → `§7 Data entities` and `§2 Domain model` external-system hints.

The `map-swim-lane-process-mapping-from-inputs-to-ui.md` skill is a stub at MVP — the canonical mapping list lives in this section.

---

## Next steps (rendered in the artefact's footer banner)

The trailing **Next steps** banner in the artefact instructs the consultant:

> *"This artefact's primary value is the **Disconnect Register** — the table flagging every handoff where the inputs leave a question open. Each non-`clean` row carries a suggested question; bring those to the next consultant conversation (or back to the source author). Closing disconnects before `/requirements` runs prevents fabricated integration requirements downstream. To re-ingest this artefact into `/requirements`, copy this file into `input/` (e.g. `input/swim-lane-process-mapping.html`) and re-run `/requirements`. The input-handler will classify it as `Supported-via-MCP`, markitdown will convert it to `input/swim-lane-process-mapping.html.converted.md` (preserving the structured YAML block as fenced code and the Mermaid source as `<pre>` blocks), and the drafter will consume it via the refreshed manifest. The YAML structured model becomes a bijection target for `/requirements`'s completeness gap pass; decision branch guards seed acceptance-criteria branches; `data-store` and `external-system` steps hint at `§7 Data entities` and `§2 Domain model` aggregates; any `[AI-SUGGESTED: AI-NNN | blocking]` and unresolved disconnects flow into the resolver as consultant questions."*

The analyser does **not** auto-copy. The consultant copies manually.
