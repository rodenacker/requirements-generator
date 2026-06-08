<!-- ROLE: asset (analysis reference). Methodology definition for the task-analysis input-analyser. Modelled on framework/assets/analyses-inputs/thematic-analysis-reference.md (sibling input-side MVP) and framework/assets/analyses/task-flows-reference.md (requirements-side HTA cousin). Industry framing: Hierarchical Task Analysis (Annett & Duncan 1967; Stanton 2006) plus a Sub-Goal Template-derived information layer (Ormerod & Shepherd 2004 in Diaper & Stanton, eds.) — single-actor, decomposition-first, document-only extraction. Distinct from the analyse-requirements/task-flows methodology: this analyser operates on RAW inputs (manifest + per-tier files), produces pure HTA + per-terminal information requirements, and emits a self-contained HTML artefact whose embedded YAML structured block is the downstream re-ingestion contract for /requirements. -->

# Task Analysis reference

> **Method:** Walk every consumable source enumerated in `requirements/source-manifest.json` and produce a Hierarchical Task Analysis (HTA — Annett & Duncan 1967; reformalised by Stanton 2006) of the user goal(s) the inputs describe. Decompose each top-level goal into a numbered hierarchy of sub-goals and terminal operations, attach a Plan (sequence / selection / iteration / concurrent / discretionary) to every non-terminal node, annotate every terminal operation with the data nouns the actor reads or writes (Sub-Goal Template layer, Ormerod & Shepherd 2004), and cite a manifest source on every node via `[SRC: <filename>]`. Inferred sub-goals and inferred Plans are permitted but must be marked `inferred: true` and surfaced as resolver-style consultant prompts; **inferred terminal operations are forbidden** (Diaper & Stanton 2004 anti-confabulation rule). Coverage gaps surface as `[GAP-INFERRED]` and `[GAP-PLAN-SILENT]` markers in a diagnostics section — never as invented operations.

**Output file:** `analyse-inputs/TASK-ANALYSIS/task-analysis.html` — a self-contained HTML5 artefact with inline CSS, an inline YAML structured tree inside a `<pre><code class="language-yaml">` block (the LLM-readable copy that survives markitdown HTML→MD conversion when the file is re-ingested via `input/`), a visual nested `<ol>` / `<details>` tree, two tables (Plans, Information requirements), and a collapsed diagnostics section. Browsable directly via `file://`.

**Analyser agent:** `framework/agents/analyses-inputs/task-analysis-analyser.md`

**Character:** `framework/assets/characters/task-analysis-inputs-analysis.md`

**Template:** `framework/assets/analyses-inputs/template-task-analysis.html`

---

## Industry framing — HTA + SGT-derived information layer

### A. Hierarchical Task Analysis (HTA)

- **Origin.** Annett, J., & Duncan, K. D. (1967). *Task analysis and training design*. Occupational Psychology, 41, 211–221.
- **Canonical modern reference.** Stanton, N. A. (2006). *Hierarchical task analysis: developments, applications, and extensions*. Applied Ergonomics, 37(1), 55–79. Stanton catalogues twelve documented applications of HTA, including requirements specification, and explicitly endorses **document analysis as a valid evidence source** (§3) — interviews and observation are not required when work is well-documented.
- **Output shape.** A hierarchy of goals → sub-goals → terminal operations, with **Plans** annotating every non-terminal node. Numbering is hierarchical: `0` (super-ordinate goal), `1`, `2`, … (level-1 children), `1.1`, `1.2` … (level-2 children), and so on. Numbering encodes both depth and sibling order.
- **Plans (Annett's three control-structure types, extended by practitioners to five).** Per Stanton (2006, p. 60) — Plans are *"the most important and most often neglected component of HTA"*; making them mandatory in the artefact is the load-bearing methodology choice.
  - `sequence` — fixed order ("do 1, then 2, then 3"). The canonical default.
  - `selection` — if/then routing ("do 1 if `<guard>`, else do 2"). Multi-way selections name every guard and every child.
  - `iteration` — loop ("repeat 1.1–1.3 until `<condition>`"). Iteration plans always name the termination condition.
  - `concurrent` — time-sharing ("do 1 and 2 in parallel"). Surfaces session / state-locking requirements downstream.
  - `discretionary` — any order ("do 1, 2, 3 in any order"). Reserved for cases where the inputs explicitly state order-independence, **not** as a silent fallback for missing-Plan branches (see §Inferred-Plan three-tier escalation below).
- **Stopping rule (P × C).** Annett & Duncan (1967) — stop decomposing when **P × C** (Probability of inadequate performance × Cost of inadequate performance) is acceptably low. In a document-only setting both P and C are inferred. Concrete rendering for this analyser: **stop when an operation maps to a single user-visible UI action OR a single atomic data mutation**. An operation is atomic when its verb names one discrete user act (`submit form`, `enter amount`, `select category`, `click approve`) that cannot be meaningfully decomposed without crossing into device-level fidelity (mouse coordinates, keystroke timing) — see anti-patterns below.
- **Depth cap.** ≤ 5 levels (root counts as level 0; terminal operations at level 5 or shallower). Per Stanton (2006) empirical observation: HTAs deeper than 5 levels rarely add value and become procedural transcripts.
- **Sub-goals-per-parent.** 2–10 per parent (Stanton HTA-7 step 4). A parent with 1 child means the level is redundant (collapse); a parent with >10 children means the parent should be split. Both are diagnostics, not hard halts — surface and let the consultant decide.

### B. Sub-Goal Template (SGT) information layer

- **Origin.** Ormerod, T. C., & Shepherd, A. (2004). *Using task analysis for information requirements specification: The Sub-Goal Template method*. In Diaper, D., & Stanton, N. A. (eds.), *The Handbook of Task Analysis for Human-Computer Interaction*. Lawrence Erlbaum.
- **Why this analyser includes it.** Pure HTA gives a downstream requirements drafter the *structure* of the user's goals but not the *data* each terminal operation touches. SGT annotates each terminal operation with the information the actor reads or writes — *"3.2 Submit claim: reads {amount, currency, date, receipt}, writes {claim_status}"*. Those data nouns are direct precursors to `§7 Data entities` in the downstream `requirements/requirements.md`.
- **Why this analyser does NOT use full SGT.** The full SGT method imposes a heavy taxonomy of sub-goal templates and information categories (act / exchange / monitor / etc.). For document-only extraction, the full taxonomy is high cost to consultant validation. The MVP includes only the per-terminal `information_required` array (an array of `{noun, direction: read | write, sources}` objects). The full template can be added as a v2 lens if needed.

### C. Variants considered and rejected

| Variant | Rejected because |
|---|---|
| Cognitive Task Analysis (Schraagen, Chipman & Shalin 2000; Crandall, Klein & Hoffman 2006 *Working Minds*) | Requires Critical Decision Method interviews. The evidence (expert tacit cognition) is not in the documents. Cannot run on the manifest alone. |
| GOMS / KLM (Card, Moran & Newell 1983; Kieras 1996) | Models expert error-free interaction with a *known* UI at keystroke granularity. The UI does not yet exist — this analyser feeds a requirements drafter that precedes design. |
| Goal-Directed Task Analysis (Endsley 1995; Endsley, Bolté & Jones 2003) | Decomposes goals into situation-awareness requirements (Level 1 perception / Level 2 comprehension / Level 3 projection). Designed for safety-critical / monitoring domains. Overkill for the project's stated target of CRUD-heavy data-management apps. |
| Pure Sub-Goal Templates (Ormerod & Shepherd 2004) | The full SGT method is the most elaborate of the family; high cost to consultant validation. Best treated as a *layer* on HTA, not a replacement — which is what this analyser does. |

### D. Why apply task analysis to raw inputs (not the synthesised requirements doc)

| Lens | Methodology | Question answered | Operates on |
|---|---|---|---|
| Vocabulary × definitions | glossary (input variant) | Which terms appear in the raw material? | raw `input/` |
| Cross-cutting patterns | thematic-analysis | What recurring patterns do the inputs carry? | raw `input/` |
| Discovery tree | opportunity-solution-trees | Outcomes → opportunities → solutions in the inputs? | raw `input/` |
| Current-state user workflow | journey-mapping | How does the user move through the as-is workflow? | raw `input/` |
| **Goal decomposition × coordination logic × per-terminal data** | **task-analysis** | **What atomic operations does the user perform, in what coordination structure, against what data?** | **raw `input/`** |

Task analysis is **complementary** to `journey-mapping`: a journey map is linear and persona-shaped (start state → phases → end state, one persona per card); an HTA is hierarchical and goal-shaped (root goal → decomposed sub-goals → terminal operations, Plans encoding coordination). The same brief that yields a 4-phase Customer Service Rep journey often yields a different-shaped HTA — phases are not subgoals, and step sequence is not always Plan structure. The two methodologies surface different signals; running both before `/requirements` is the high-leverage combination for a structural-requirements drafter.

### E. Distinction from `/analyse-requirements/task-flows`

The `/analyse-requirements/` pipeline ships a sibling methodology called `task-flows` (HTA + Task-Flow Diagram combo). It reads the synthesised `requirements/requirements.md` and is purpose-built for a `§5 Task flows`-shaped source. **This analyser is distinct** for four reasons:

1. **Different input source.** `task-flows` reads `requirements/requirements.md`; this analyser reads `requirements/source-manifest.json` + the raw `input/*` files it enumerates.
2. **Different citation grammar.** `task-flows` uses `[SRC: C-NNN]` (claim IDs from the requirements pipeline's sidecar); this analyser uses `[SRC: <filename>]` (manifest row `filename` field).
3. **Different methodological emphasis.** `task-flows` pairs HTA with a Task-Flow Diagram for visual narrative; this analyser pairs HTA with an SGT-derived information layer for downstream requirements drafting.
4. **Different downstream contract.** `task-flows` is read by consultants and downstream design-spec authors; this analyser's primary downstream consumer is the `/requirements` drafter (after the consultant copies the HTML output into `input/` and re-runs `/requirements`).

The two are complementary; consultants commonly run this one before `/requirements` and the other after.

### F. Why this analyser uses HTML + embedded YAML

- **Visual hierarchy.** HTA trees beyond three levels degrade quickly in raw indented markdown; HTML's nested `<ol>` + `<details>` + Plan-type badges + colour cues are markedly easier to scan. Sibling `journey-mapping` is the input-side HTML precedent.
- **Re-ingestible structure.** The artefact's primary downstream use is as a re-fed input to `/requirements`. The consultant copies `analyse-inputs/TASK-ANALYSIS/task-analysis.html` into `input/`, the input-handler classifies it as `Supported-via-MCP`, markitdown converts it to `input/task-analysis.html.converted.md`, and the drafter reads the converted markdown via the manifest. **`<pre><code class="language-yaml">` blocks survive markitdown's HTML→MD conversion as fenced code** — so the structured tree is rendered into a `<pre><code>` block (not a `<script type="application/json">` block, which markitdown strips). The visual tree is rendered separately as nested `<ol>` / `<details>`. The double render is deliberate.
- **Self-contained.** Inline `<style>`, no external CSS / JS / fonts / CDN. Network-isolated; browsable via `file://`; shareable as a single attachment.

---

## Output structure

The artefact has a fixed top-to-bottom shape, populated into `framework/assets/analyses-inputs/template-task-analysis.html` via documented placeholder substitution:

0. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead: what this task hierarchy (HTA — hierarchical task analysis) is, what it found, and what the consultant should do with it. The **first** section, above the overview header. A faithful condensation of the content below — it introduces no fact, count, or citation not already present, and carries no `[SRC]` of its own. Methodology jargon (task, subtask, goal, plan/sequence) is glossed at first use; client domain terms are not glossed (the GLOSSARY methodology owns those). Per `framework/shared/output-readability.md`.
1. **Header banner** (`<header id="overview">`) — title, generation timestamp, manifest sha256 (first 12 chars), manifest row count consumed / skipped, target-mode (prototype / application, from the manifest's `target` field if present), run number. Includes a `<nav class="toc-trees">` with jump-links to per-goal sections (one link per top-level goal — almost always one).
2. **Goal summary** (`<section id="goal-summary">`) — for each top-level goal (typically one; rarely more — see §Multi-goal handling below): a short paragraph naming the goal (node `0`), its trigger event (when it starts), its preconditions (what must be true to begin), and the success outcome (what makes it complete). Every claim cites a manifest source.
3. **Visual tree** (`<section id="visual-tree">`) — nested `<ol>` / `<details>`. Each node renders: hierarchical id (`0`, `1`, `1.1`, …), label, `[SRC: <filename>]` chips (one per source), Plan-type badge for non-terminals (`SEQ` / `SEL` / `ITER` / `CONC` / `DISC`, colour-coded), `[leaf]` chip for terminals, `[AI-SUGGESTED]` chip and red left border for inferred nodes.
4. **Structured tree** (`<pre><code class="language-yaml">` inside `<section id="structured-tree">`) — machine-readable copy of the entire tree. Schema below.
5. **Plans table** (`<table>` inside `<section id="plans-table">`) — every non-terminal node's Plan: id, parent-label, plan-type pill, plan-text (Annett-style English), source citations, inferred-flag.
6. **Information requirements table** (`<table>` inside `<section id="information-table">`) — every terminal operation's data nouns: terminal id, label, direction (read / write), nouns (verbatim from inputs where possible), source citations.
7. **Gaps and inferred nodes** (`<section id="gaps">`) — list of every `inferred: true` node and every silent-Plan branch, with `blocking | non-blocking` classification (per §Inferred-Plan three-tier escalation below), the suggested consultant prompt the resolver would surface, and the source span where the gap was detected.
8. **Diagnostics** (collapsed `<details id="diagnostics">`) — counts summary, the 8 quality-gate results (PASS / FAIL), source roster (consumed + skipped tables), `[GAP-INFERRED]` and `[GAP-PLAN-SILENT]` registry, run history (append-only bullet list), and the trailing **Next steps** banner instructing the consultant how to feed this artefact back into `/requirements`.

Section order lives in the template, not in the analyser. The analyser emits the same placeholder blocks regardless; the template decides where they land.

### Structured-tree YAML schema (embedded in `<pre><code class="language-yaml">`)

```yaml
task_analysis:
  manifest_sha256: <hex>
  generated_at: <ISO-8601 UTC>
  run_count: <int ≥ 1>
  target: prototype | application | (not declared in manifest)
  goals:
    - id: "0"                      # super-ordinate goal node; one per top-level goal
      parent_id: null
      label: <short verb-phrase, user-side subject>
      is_operation: false
      trigger: <event that starts the goal, with [SRC: <filename>] in the value>
      preconditions: [<short list, each with [SRC: <filename>]>]
      completion: <success outcome, with [SRC: <filename>]>
      plan:
        type: sequence | selection | iteration | concurrent | discretionary
        expression: <Annett-style English sentence>
        branches: []               # populated for selection / iteration
        sources: ["[SRC: <filename>]", ...]   # ≥ 1 if not inferred
        inferred: false            # true → plan.sources may be empty
        confidence: high | medium | low
      information_required: []     # empty for non-terminals; required for terminals
      sources: ["[SRC: <filename>]", ...]   # ≥ 1 if not inferred
      inferred: false
      confidence: high | medium | low
      children: ["1", "2", "3", ...]
    - id: "1"
      parent_id: "0"
      label: <verb-phrase>
      is_operation: false           # if has children
      plan: {...}                   # required because non-terminal
      information_required: []
      sources: [...]
      inferred: false
      children: ["1.1", "1.2"]
    # ...
    - id: "1.1"
      parent_id: "1"
      label: <atomic verb-phrase, user-side>
      is_operation: true            # terminal — no plan, no children
      plan: null
      information_required:
        - noun: <data noun verbatim or paraphrased>
          direction: read | write
          sources: ["[SRC: <filename>]", ...]
      sources: ["[SRC: <filename>]", ...]    # ≥ 1 — terminals MUST cite a source (no inferred terminals)
      inferred: false                # must be false for terminals
      children: []
```

YAML invariants:
- `goals` is a flat array; hierarchy is encoded via `id` / `parent_id`.
- `is_operation: true` implies `plan: null` and `children: []` and `inferred: false`.
- `is_operation: false` implies a non-null `plan` and `len(children) ≥ 2` (a node with one child is a redundant level — collapse).
- Every node has at least one source citation OR `inferred: true`. Terminals must cite (`inferred: false`).
- `information_required` is empty for non-terminals and non-empty-or-explicitly-empty for terminals (an empty array is permitted but rare — surface in diagnostics if more than half of terminals have zero).

### Multi-goal handling

The expected and recommended shape is **one top-level goal per analysis**. If the inputs evidence ≥ 2 viable goal frames (e.g. the brief describes both "submit an expense claim" and "approve an expense claim" as independent top-level user goals, not one nested under the other), the analyser surfaces an `AskUserQuestion` at Round 1 with three options: `One — pick the highest-evidence frame`, `Both — render both as parallel top-level goals (Recommended if both are independently load-bearing)`, `Restate — let me name the goal frame myself`. Multi-goal artefacts render each goal in its own `<section>` with its own visual tree; the YAML carries multiple entries with `parent_id: null` and `id: "0"`, `id: "0b"`, etc.

---

## Workflow rounds (8 rounds + 4 operational steps = 12 workflow steps)

Each round produces a distinct, named in-memory output. The analyser does not write the artefact until Round 8 is complete and all 8 hard quality checks have passed (or the consultant chose Override).

### Round 1 — Root-goal identification

- For each row in `consumed_rows`, scan the content for **goal statements** — imperative verbs with a user as subject, nominalised goal phrases, or section headers naming a user-task ("Expense submission", "User onboards a new customer").
- Identify the top-level user goal — the verb phrase that names what the actor is trying to *accomplish* (not what the system does, not what UI is built). Format: short verb phrase, user-side subject, sentence-case. Example: *"Submit expense claim"*, *"Onboard a new customer"*, *"Resolve a billing dispute"*.
- **No invented goals.** The goal label must be traceable to ≥ 1 verbatim mention in the inputs (paraphrased label is fine; the *concept* must cite).
- **Multi-goal disambiguation.** If ≥ 2 candidate goal frames surface with comparable evidence weight, surface the `AskUserQuestion` per §Multi-goal handling.

Output: a `goal_frames` list (length 1 typically, ≥ 2 occasionally). Each frame carries the candidate label, the trigger event, the preconditions, and the success outcome — all with source citations.

### Round 2 — Level-1 sub-goal enumeration

For each goal frame, enumerate the immediate (level-1) sub-goals:

- Walk the inputs for sub-tasks named under the goal — section sub-headings, numbered lists, sentences describing intermediate accomplishments.
- Each level-1 sub-goal carries a short verb phrase label (user-side subject, no UI nouns at non-terminals), `[SRC: <filename>]` citations, and a confidence score (`high` / `medium` / `low`).
- **Cap rule:** 2–10 level-1 sub-goals per goal. Fewer than 2 means the goal is collapsing into a single sub-task (likely the level is redundant or the goal is itself a sub-goal); more than 10 means the goal should be split (surface the cap as a soft warning in diagnostics).

Output: per goal frame, a `level_1_subgoals` list with citations.

### Round 3 — Recursive decomposition (depth ≤ 5)

For each level-1 sub-goal, decompose recursively until the **stopping rule** is met:

- **Stopping rule:** an operation is terminal when its verb names one discrete user action that maps to a single UI action OR a single atomic data mutation. Examples of terminal operations: `submit form`, `enter amount`, `select category`, `click approve`, `attach receipt`. Examples of non-terminal sub-goals that need further decomposition: `populate the claim`, `validate the order`, `provide rejection reason and amended details`.
- **Depth cap:** ≤ 5 levels (root at level 0; terminals at level ≤ 5). If the inputs evidence deeper structure, surface in diagnostics as a `[GAP-DEPTH-CAP]` warning and either truncate at level 5 (terminals become coarser than ideal) or surface the over-depth branch to the consultant.
- **Sub-goals-per-parent:** 2–10. Same diagnostics as Round 2. A parent with 1 child is a redundant level — collapse it.
- **Inference allowance.** Sub-goals (not terminals) may be marked `inferred: true` when the inputs imply their existence (e.g. a Plan references a sub-goal whose decomposition is missing) but do not name them verbatim. Inferred sub-goals carry `sources: []` and `confidence: low|medium` and are surfaced in §Gaps. **Terminal operations are NEVER inferred** (Diaper & Stanton 2004 anti-confabulation rule — see §Anti-patterns).

Output: per goal frame, the full HTA tree with all nodes typed `is_operation: true|false` and citations attached.

### Round 4 — Plan attachment + inferred-Plan three-tier escalation

For every non-terminal node (every node with `is_operation: false`), assign a Plan from the source language using the extraction table below:

| Source language pattern | Maps to Plan type | Notes |
|---|---|---|
| Numbered lists; "first…, then…, finally…"; sequence markers ("do A, then B"); imperative chains | `sequence` | The default for ordered procedures. |
| Conditional clauses ("if X then Y"; "unless Z, do A"); branching ("for travel claims, …"); role-conditional ("approvers see…", "members can only…") | `selection` | Plan must name the guard variable in `plan.expression`. Multi-way selections name every guard / child. |
| "For each", "repeat until", "while X, …", "for every"; iteration markers; collection verbs ("process each item", "review every entry") | `iteration` | Plan must name the termination condition. |
| "Concurrently", "in parallel", "while also", "at the same time", "simultaneously" | `concurrent` | Surfaces session / state-locking needs downstream. |
| "Any order", "in any sequence", "as preferred", "either way" | `discretionary` | The least common case. Must be explicitly evidenced in the source — not a silent fallback. |

**Three-tier inferred-Plan escalation.** When the inputs do not name a coordination structure for a non-terminal branch, the analyser must NOT silently assume `sequence` (that is the most common silent-confabulation failure). Instead, apply the three-tier escalation:

1. **Tier 1 — Surface the gap.** If the silent branch is high-leverage (its Plan would gate downstream acceptance criteria), mark `plan.inferred: true` and emit a `[GAP-PLAN-SILENT]` entry in diagnostics with `blocking: true`. The resolver-style prompt: *"How are the children of `<parent-label>` coordinated? Options: sequence / selection / iteration / concurrent / discretionary."* This is the preferred branch.
2. **Tier 2 — Fall back to `discretionary` with explicit `plan.inferred: true`.** Plan expression: *"source silent — discretionary assumed (consultant should confirm)"*. Mark `blocking: false` in diagnostics. Use only when the silent branch is non-load-bearing (a deep low-leverage sub-tree).
3. **Tier 3 — Refuse to decompose further.** If the silent branch's coordination matters but the inputs cannot support any inference, collapse the branch's children back into the parent as a single terminal operation labelled with the parent's verb phrase (so the branch becomes opaque rather than confabulated). Mark in diagnostics.

**No `plan.type` may be present without one of: a source citation in `plan.sources`, OR `plan.inferred: true`.** This is gate 4 below.

### Round 5 — Information-requirements annotation (SGT layer)

For every terminal operation, annotate the data nouns the actor reads or writes:

- Walk the source spans around the operation's citation site. Identify nouns the operation manipulates: form fields, record attributes, entity properties, status values, attached artefacts.
- Each entry: `{noun, direction: read | write, sources}`. `read` means the operation consumes the noun's value; `write` means the operation produces or changes it. A single noun may appear with both directions if the operation reads-then-writes (e.g. `status: read, write` for an edit-then-confirm flow).
- Use verbatim nouns where the inputs name them ("receipt", "claim amount", "approval status"). Paraphrased nouns are allowed when the inputs use long phrases ("the supporting document the user uploads" → `receipt`).
- An empty array is permitted (some terminal operations genuinely touch no data — `cancel`, `back`), but if more than half of terminals have empty arrays, surface a soft warning in diagnostics — likely the analyser is missing data-noun signals in the sources.

Output: per terminal operation, `information_required` array populated.

### Round 6 — Gap classification (blocking vs non-blocking)

Walk the in-memory tree and classify every inferred node + every `[GAP-PLAN-SILENT]` entry:

- **`blocking`** — the node gates downstream acceptance criteria. Selection Plan with no source language to name the guard; iteration Plan with no termination condition; inferred sub-goal that breaks the bijection target (a level-1 sub-goal the goal mentions but the inputs never decompose). Resolver should surface these to the consultant before `/requirements` runs.
- **`non-blocking`** — the inference is plausible and low-leverage. Default-Plan inferences on deep low-leverage sub-trees; inferred sub-goals whose absence does not break the goal's bijection. Diagnostics flags but does not gate.

Each blocking gap allocates an `AI-NNN` identifier from the existing namespace (shared with `framework/shared/general-rules.md` and the `/requirements` drafter / resolver). The marker grammar is `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` — same as the rest of the framework, so the resolver can ingest gaps from this artefact uniformly without grammar changes.

Output: per inferred node, a `gap_classification` payload with `{ai_id, blocking, suggested_prompt, source_span}`.

### Round 7 — Self-validate (12-point checklist)

Run all 8 hard quality gates from §Quality gates below, plus four structural integrity checks:

- Numbering consistency: every child id is parent-id-prefixed; no orphan ids; no duplicate ids.
- Every non-terminal has either ≥ 2 children OR a single child that is `is_operation: true` and the consultant explicitly accepted the unary branch via Override (rare; flagged).
- Citation discipline: every `[SRC: <filename>]` payload appears in `consumed_rows[*].filename` exactly.
- Information-requirements discipline: every terminal has `information_required` (may be empty); non-terminals have `information_required: []`.

On any failure → §Failure handling.

### Round 8 — Render + write + verify

- Read `framework/assets/analyses-inputs/template-task-analysis.html` once.
- Build the substitution map (placeholders documented in the template's header comment + §Output structure above).
- HTML-escape every consultant-supplied string before injection (`<`, `>`, `&`, `"`, `'`). YAML inside `<pre><code>` is escaped as plain text within the block — do not double-escape inside YAML.
- Compute the SHA-256 of the in-memory composed HTML.
- `Write analyse-inputs/TASK-ANALYSIS/task-analysis.html`. Invoke `framework/skills/verify-artifact-write.md` with `expected_sha256` and `expected_min_bytes = 4096`. On `RF-04 trigger` → halt and fail handback.
- Hand back to the orchestrator with the Accept / Revise / Restart loop.

---

## Provenance markers

Every node, every Plan, every terminal operation, every information-requirement entry carries either source citations or an inference marker. Three marker shapes:

| Marker | Used in | Payload | Meaning |
|---|---|---|---|
| `[SRC: <filename>]` | YAML sources arrays, visual-tree chips, table source-citation columns, goal-summary paragraph | basename + extension, matching a manifest row's `filename` field | The node / plan / information requirement is anchored to this manifest source. |
| `[AI-SUGGESTED: AI-NNN \| blocking\|non-blocking]` | inferred non-terminal nodes and inferred Plans (only) | sequential AI-NNN from the shared namespace; classification per Round 6 | The node / Plan was inferred from context, not directly cited. Surface to consultant via resolver. Never used on terminal operations. |
| `[GAP-INFERRED]` and `[GAP-PLAN-SILENT]` | diagnostics section only (gaps registry) | none | Diagnostics-side aggregate marker for inference incidence per goal. Counts and lists tie back to the `[AI-SUGGESTED]` markers in the tree body. |

**No fourth marker.** **`[AI-SUGGESTED]` markers are forbidden on terminal operations** — terminals must always cite a source.

---

## Source-of-truth hierarchy

The analyser walks the manifest in this order:

1. **`Native-text` rows** → read `original_path` directly as text. The richest source for verb extraction.
2. **`Native-multimodal` rows** → read `original_path` (Claude vision surfaces image bytes). Transcribe visible text and structurally significant observations. Diagrams (flowcharts, wireframes) often carry coordination logic.
3. **`Supported-via-MCP` rows** → read `converted_sibling` (the `.converted.md` that the input-handler produced via markitdown). Do **not** re-invoke `markitdown-mcp` — the manifest's `converted_sibling` is the contract.
4. **`Unsupported` rows** → skipped; recorded in `Source roster > Skipped` with the manifest's `conversions_applied` reason.

The analyser **never** reads:

- Any path under `requirements/` other than `requirements/source-manifest.json` and the manifest-enumerated source files.
- Any path under `framework/state/`.
- Any path under `framework/shared/` (textual `RF-NN` / `GR-NN` references are links for the reader, not file loads).
- Other analyses' artefacts (`analyse-requirements/<OTHER-METHOD>/...`, `analyse-inputs/<OTHER-METHOD>/...`). Optionally re-reads the prior `analyse-inputs/TASK-ANALYSIS/task-analysis.html` for the additive merge.

---

## Quality gates (8 hard gates)

Run at Round 7 close, before render. Each check operates on the in-memory state.

1. **Citation completeness.** Every node, every Plan, every information-requirement entry carries either ≥ 1 `[SRC: <filename>]` matching a manifest row's `filename` exactly, OR `inferred: true` (non-terminals + Plans only — terminals must always cite).
2. **No inferred terminals.** Every node with `is_operation: true` has `inferred: false`. (Diaper & Stanton 2004 anti-confabulation rule — the load-bearing methodology gate.)
3. **No UI-noun labels at non-terminals.** No non-terminal node label starts with or consists of UI-action verbs (`click`, `tap`, `press`, `select option`, `hover`, `scroll`, `swipe`). These are reserved for terminals where they are genuinely the atomic act. Non-terminal labels must start with a user-side outcome verb (`submit`, `populate`, `validate`, `decide`, `provide`, `approve`).
4. **Every non-terminal carries a Plan with provenance.** Plan type ∈ {sequence, selection, iteration, concurrent, discretionary}; `plan.expression` is non-empty; either `plan.sources` has ≥ 1 citation OR `plan.inferred: true`. A Plan with neither is a fail.
5. **Decomposition discipline.** Depth ≤ 5 (root at level 0). Every non-terminal has ≥ 2 children unless a unary-branch Override is recorded. Sub-goals-per-parent ≤ 10 (soft warning if exceeded; hard fail if > 15).
6. **Selection-Plan and iteration-Plan completeness.** Every `selection` Plan names a guard variable in `plan.expression`. Every `iteration` Plan names a termination condition. Plans without these are silently incomplete — fail with a structured diagnostic naming the offending node.
7. **Minimum-decomposition rule.** Each goal must have ≥ 2 terminal operations across the whole tree. A single-leaf tree indicates either a trivial goal (in which case the inputs don't justify an HTA — surface as `Cannot produce HTA: inputs evidence a single atomic goal, not a decomposable task`) or a failed decomposition.
8. **Manifest fingerprint + source roster.** The artefact's embedded `<script type="application/json" id="task-analysis-meta">` block carries `manifest_sha256` equal to the Step 2 value; the diagnostics source-roster `Consumed` table enumerates every manifest row whose `tier != "Unsupported"` (filename, tier, sha256[:8], citation count); the `Skipped` table enumerates every `Unsupported` row.

### Failure handling (Revise / Override / Restart)

On any hard-gate failure: do **not** write the artefact. Surface `AskUserQuestion` with three options:

1. `Revise — exit so the consultant can enrich input/ and re-invoke /analyse-inputs (Recommended)`
2. `Override — proceed and write a known-defective artefact (Run-history bullet records every violation)`
3. `Restart — re-run from Round 1 with a fresh manifest pass`

On **Revise**: hand back to the orchestrator with a `failed-handback` state.
On **Override**: record each failing gate in the Run-history bullet for this run; proceed to render. Note: gate 2 (no inferred terminals) is `Override`-able in extremis but should almost never be — surfacing the issue and refusing to render is the right move.
On **Restart**: re-enter Round 1. Cap at three fail-Restart cycles; on the fourth, force the Revise path.

---

## Anti-patterns

All four are documented in the literature; each maps to a hard gate above.

1. **Over-decomposition.** Annett & Duncan (1967); Stanton (2006, p. 63). Without a stopping rule the analyst keeps subdividing indefinitely. In document-only settings the temptation is worse because the LLM has no observational friction. **Enforcement:** Stopping rule (atomic UI action / atomic data mutation) + depth cap = 5 + sub-goals-per-parent ≤ 10. Gates 5 and the diagnostics depth-cap warning.

2. **Device-task confusion (UI-noun labels at non-terminals).** Diaper (2004); Kirwan & Ainsworth, *A Guide to Task Analysis* (1992). Describing what the *system* does instead of what the *user* is trying to achieve. Symptom: non-terminal nodes labelled "click Submit button" instead of "submit claim for approval". **Enforcement:** Gate 3 — non-terminal labels must start with a user-side outcome verb; `click`, `tap`, `select option`, `hover`, `swipe`, `press`, `scroll` are banned at non-terminals and only permitted at terminals when they are genuinely the atomic act.

3. **Missing Plans.** Stanton (2006, p. 60) — Plans are *"the most important and most often neglected component of HTA"*. An HTA without Plans is a flat outline and provides almost none of the value claimed for the methodology. **Enforcement:** Gate 4 — every non-terminal must have a Plan with either source citations OR `plan.inferred: true`. Silent-Plan branches escalate through the three-tier process in §Round 4 — they do not silently default to `sequence`.

4. **Analyst confabulation (inferred terminals).** Diaper & Stanton (2004) discuss "analyst confabulation" in document-only studies. The LLM analogue is hallucinating plausible-sounding terminal operations the inputs do not name. **Enforcement:** Gate 2 — inferred terminals are forbidden. Inferred sub-goals and inferred Plans are permitted (with marker + resolver surfacing) because they are corrective inferences over structure; inferred terminals would corrupt the acceptance-criteria bijection downstream.

Two additional anti-patterns are framework-wide and apply here:

5. **Do not bundle external CDN / fonts / JS.** The artefact is self-contained — inline CSS, no `<script>` beyond the metadata block, no fonts, no external resources. (Frame-wide invariant; mirrors `journey-mapping`.)
6. **Do not auto-copy the artefact to `input/`.** The agent's write-isolation rule (CLAUDE.md §"Stand-alone constraints") forbids `/analyse-inputs` from writing outside `analyse-inputs/<METHOD>/*`. The trailing **Next steps** banner in the artefact instructs the consultant to copy manually; the analyser does not.

---

## Stop-condition

The analysis is complete when:

- Every goal frame has a populated tree with depth ≤ 5, every non-terminal has a Plan with provenance, every terminal has a source citation and `information_required` array.
- All 8 hard gates pass, or the consultant chose Override and the failures are recorded in the Run-history bullet.
- `analyse-inputs/TASK-ANALYSIS/task-analysis.html` has been written and `verify-artifact-write` returned `pass`.
- The consultant chose Accept in the handback loop.

---

## Re-run semantics

- The cursor lives in the artefact's `<script type="application/json" id="task-analysis-meta">` block — `manifest_sha256`, `run_count`, per-goal `terminal_count`. No state file under `framework/state/`.
- On re-run, the analyser compares the current manifest fingerprint to the prior cursor:
  - **No change** → pure additive widening; inferred-only sub-goals may be confirmed by consultant Revise to flip `inferred: false` with a new citation when the consultant adds material; other content is preserved verbatim.
  - **Change** → drift prompt: `append-only` (preserves prior tree verbatim; appends new sub-goals / terminals where new manifest rows justify them; flags conflicts), `re-extract` (re-runs Rounds 1–7 from scratch on the current manifest; node ids preserved where re-extraction produces equivalent labels), or `abort` (exit without writing).
- The artefact is monotonically growing across runs unless the consultant chose `re-extract` or manually edited the file.

---

## Downstream consumption (handled by `framework/skills/map-task-analysis-from-inputs-to-ui.md`)

The analyser's primary downstream consumer is the **`/requirements` drafter**, not a design-spec author. The mapping is:

- **YAML structured tree** → bijection target for `framework/skills/completeness-gap-pass.md`. Every terminal operation should map to ≥ 1 requirement in the merged `requirements/requirements.md`; every requirement should map to ≥ 1 terminal operation (or be flagged unattributed). The drafter consumes the tree as candidate-requirement scaffolding.
- **Plans (selection / iteration / concurrent)** → acceptance-criteria fodder. Selection Plans become *"Given X, When Y, Then Z"* branches in `§6` requirements. Iteration Plans become *"the user may repeat …"* rules with the termination condition as the loop invariant. Concurrent Plans surface as session / state-locking requirements in NFR or `§6` integration constraints.
- **`information_required` arrays** → `§7 Data entities` hints. The read/write nouns per terminal are precursors to data-model nodes; nouns appearing across ≥ 2 terminals are first-class entity candidates.
- **`[AI-SUGGESTED: AI-NNN | blocking]` markers** → resolver questions. The resolver pipeline ingests these uniformly via the existing `framework/shared/general-rules.md` grammar — no schema changes needed.
- **Visual-tree HTML section** → consultant-facing artefact for sign-off review before `/requirements` runs.

The `map-task-analysis-from-inputs-to-ui.md` skill is a stub at MVP — the canonical mapping list lives in this section.

---

## Next steps (rendered in the artefact's footer banner)

The trailing **Next steps** banner in the artefact instructs the consultant:

> *"To use this artefact as additional input for `/requirements`, copy this file into `input/` (e.g. `input/task-analysis.html`) and re-run `/requirements`. The input-handler will classify it as `Supported-via-MCP`, markitdown will convert it to `input/task-analysis.html.converted.md` (preserving the structured YAML block as fenced code), and the drafter will consume it via the refreshed manifest. The YAML structured tree becomes a bijection target for `/requirements`'s completeness gap pass; the Plans table seeds acceptance-criteria branches; the information-requirements table hints at `§7 Data entities`; any `[AI-SUGGESTED: AI-NNN | blocking]` gaps flow into the resolver as consultant questions."*

The analyser does **not** auto-copy. The consultant copies manually.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/task-analysis-inputs-analysis.md` — decompositional, literal, single-actor, source-grounded, gap-honest, additive, Plan-mandatory. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact is human-read (and re-ingested by `/requirements`), so the analyser also follows `framework/shared/output-readability.md`: it writes the "In plain terms" lead (what this task hierarchy / HTA is, what it found, what the consultant should do with it), glosses methodology jargon at first use in human-readable prose ("task", "subtask", "task hierarchy / HTA", "goal", "plan/sequence"), leaves client domain vocabulary unglossed (GLOSSARY territory), and keeps every `[SRC: <filename>]` marker. The plain-language layer is confined to the lead and first-use glosses; the visual tree, Plans table, Information requirements table, YAML block, and diagnostics keep their concrete, structured discipline.
