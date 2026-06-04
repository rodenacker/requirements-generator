<!-- ROLE: asset (analysis reference). Methodology definition for the opportunity-solution-trees input-analyser. Modelled on framework/assets/analyses-inputs/thematic-analysis-reference.md (operational shape) and adapted from framework/assets/analyses/opportunity-solution-trees-reference.md (Torres methodology). Industry framing: Teresa Torres, "Continuous Discovery Habits" (2021); canonical exposition at producttalk.org/opportunity-solution-trees/. Adapted for forward-discovery against raw consultant inputs rather than reverse-discovery against a merged PRD. Inductive Rounds 1-5 extract the tree from inputs; Round 6 produces the candidate-requirements bridge that /requirements consumes when this artefact is re-dropped into input/. -->

# Opportunity Solution Tree (inputs-side) reference

> **Method:** Walk every consumable source enumerated in `requirements/source-manifest.json`, extract a single root **Outcome** (Round 1; multi-outcome candidates surface an interactive picker), inductively surface customer-perspective **Opportunities** (Round 2), inductively surface candidate **Solutions** (Round 3), best-effort extract **Assumption Tests** (Round 4), **ladder** the four layers into a tree (Round 5), then produce the report — including a **bridge** from each Opportunity to candidate-requirement seeds the `/requirements` drafter can pick up when the artefact is re-ingested (Round 6). Every node carries one or more `[SRC: <filename>]` markers naming a manifest row whose `filename` field equals the marker payload. Across re-runs the artefact is **additive**: prior tree nodes, ladder edges, and candidate-requirement lines are preserved; new manifest content extends them.

**Output file:** `analyse-inputs/OPPORTUNITY-SOLUTION-TREES/opportunity-solution-tree.html` — a self-contained HTML document rendered via `framework/assets/analyses-inputs/template-opportunity-solution-trees.html`. The tree is a **pre-rendered inline SVG** in a `#diagrams` section (reusing the requirements-side twin's `{{TREE}}` SVG approach), with an adjacent collapsed `<details class="mermaid-block">` block carrying the `graph TD` source as an export / re-ingestion adjunct (embedded as text, not validated by `mmdc`). A `language-json` `opportunity-solution-tree-body` block carries the tree model and the candidate-requirement seeds, so the artefact survives a markitdown HTML→Markdown conversion for re-ingestion by `/requirements`.

**Analyser agent:** `framework/agents/analyses-inputs/opportunity-solution-trees-analyser.md`

**Character:** `framework/assets/characters/opportunity-solution-trees-inputs-analysis.md`

---

## Industry framing — Torres (2016) adapted for raw inputs

The Opportunity Solution Tree is Teresa Torres's product-discovery artefact: a single business / product **Outcome** at the root, **Opportunities** (unmet customer needs, pain points, desires) branching beneath, candidate **Solutions** under each Opportunity, and **Assumption Tests** under each Solution. Torres's discipline (forward discovery):

- *"An opportunity is an unmet customer need, pain point, or desire."* — framed from the customer's perspective, never the company's.
- *"A solution is a product, a service, a feature, or anything else that we offer to customers to help address a known opportunity."* — implementation, never need.
- **Validity test for Opportunities:** *"Is there more than one way to address this opportunity?"* If only one Solution could possibly address it, it is a Solution disguised as an Opportunity.
- **Anti-pattern:** vertical-only branches (one Opportunity, one Solution, no siblings) signal premature commitment — the discovery space has been collapsed.

The sibling analyser at `framework/agents/analyses/opportunity-solution-trees-analyser.md` runs Torres's tree in **reverse** — it audits a merged `requirements/requirements.md` to surface gaps after the team has committed to features. This inputs-side analyser runs Torres's tree **forward** — closer to her original intent, but adapted for raw consultant material:

- Raw inputs legitimately carry **multiple stakeholder Outcomes** (the brief names one goal; the workshop notes another; the slide deck a third). The analyser surfaces an interactive picker on first run (consultant picks one as primary; others render in `## Candidate outcomes` with `[CANDIDATE-OUTCOME]` markers) rather than hard-halting.
- Raw inputs carry **contradictory pains**, **vague feelings**, **unnamed actors**, and **near-duplicate phrasings** of the same need across multiple sources. The analyser merges aggressively by actor + semantic head, keeps every source citation, and flags contradictions in diagnostics rather than inventing a reconciliation.
- Raw inputs almost never carry **explicit Assumption Tests**. The `(no assumption tests in inputs)` placeholder is the expected state; the analyser does not fabricate tests.
- Raw inputs carry **sparse Solutions**. Many consultant inputs describe pains but stop short of feature commitments. 1:1 Opportunity-Solution pairings and Opportunities with zero source-grounded Solutions are permitted; the latter get the `unaddressed-in-inputs` flag (informational, not a gate failure).

The artefact's load-bearing addition versus the reverse-discovery sibling is the **candidate-requirements bridge** (Round 6 sub-step A) — a per-Opportunity list of *"The system should `<verb> <object>` so that `<outcome>`"* lines, citing the parent Opportunity's `[SRC: <filename>]` set. The consultant re-drops the artefact into `input/` to feed `/requirements`; the drafter classifies it as `Native-text` and reads the bridge section as candidate-requirement seeds, the same way it reads `thematic-analysis`'s `Theme-to-requirement-candidates` section.

### Why apply OST to raw inputs?

| Lens | Methodology | Question answered | Operates on |
|---|---|---|---|
| Vocabulary × definitions | glossary (input variant) | Which terms appear in the raw material? | raw `input/` |
| Jobs × situations | jtbd (input variant) | What jobs are users trying to get done? | raw `input/` |
| Causal chain × root drivers | five-whys (input variant) | Why does this concern exist in the inputs? | raw `input/` |
| Cross-cutting patterns | thematic-analysis | What recurring patterns do the inputs carry? | raw `input/` |
| **Strategic ladder × discovery space** | **opportunity-solution-trees** | **Which Outcome do the inputs imply, and what Opportunities + candidate Solutions ladder to it?** | **raw `input/`** |

OST complements `thematic-analysis`: TA emphasises *what* themes recur across sources; OST emphasises *why* (the outcome the work serves) and *how* (the candidate solutions the inputs hint at). A consultant may run both and re-ingest both into `input/` for a richer `/requirements` run.

### Why HTML with embedded SVG tree + Mermaid source + JSON body

- **Self-contained, diagram-first.** The artefact is a single HTML file the consultant can open in a browser with the Opportunity Solution Tree at the top as a pre-rendered, self-contained layered SVG — one `<svg class="tree-svg">` in which the analyser places every node and every edge in a single `viewBox` coordinate space, so edges meet their nodes by construction at any node count. No Mermaid runtime, no external assets. This matches the framework's HTML-output, diagrams-first convention.
- **Re-ingestibility via embedded fenced blocks.** Re-ingestion is still load-bearing: the consultant re-drops the artefact into `input/` to feed `/requirements`. The embedded `language-json` `opportunity-solution-tree-body` block (tree model + candidate-requirement seeds) and the collapsed `mermaid-source` block survive a markitdown HTML→Markdown conversion, so the model round-trips cleanly and the drafter reads the candidate-requirement seeds without parsing presentational HTML. The "HTML cannot round-trip into `/requirements`" rationale that previously justified staying in markdown is therefore obsolete — the embedded JSON body block is what makes the HTML round-trip cleanly now.
- **Diagram as inline SVG.** The layered tree diagram is a pre-rendered, self-contained inline `<svg class="tree-svg">` (nodes + edges in one `viewBox` coordinate space); the `graph TD` source is kept in an adjacent collapsed `<details class="mermaid-block">` block as an export / re-ingestion adjunct, embedded as text and **not** validated by `mmdc` (the inline tree is the visible diagram — matching the other inline-SVG analyses; no `mmdc` dependency).

The requirements-side twin already produced HTML + SVG as a final audit deliverable; the inputs-side variant now produces the same self-contained HTML shape while keeping its load-bearing candidate-requirements bridge re-ingestible through the embedded body block.

---

## Output structure

The artefact has a fixed top-to-bottom shape:

1. **Header.** Title, generation timestamp, manifest fingerprint (sha256 of `requirements/source-manifest.json`), run count.
2. **ost-meta** HTML comment carrying the additive-merge cursor (`manifest_fingerprint`, `run_count`).
3. **Summary.** Counts: outcomes (primary + candidate), opportunities, solutions (with orphan count), assumption tests (or `absent` flag), candidate-requirements, orphan / unaddressed / weakly-anchored counts, sources consumed / skipped.
4. **Outcome.** Single block — the primary root.
5. **Candidate outcomes.** Zero or more blocks, each carrying a `[CANDIDATE-OUTCOME]` marker. Omitted entirely when only one outcome candidate emerged from Round 1.
6. **Opportunities.** One block per Opportunity, alphabetical by `<actor> — <need clause>`. Each block:
    - `### Op-NN — <actor> — <need clause>`
    - Canonical-form sentence: *"`<actor>` needs / cannot / wants `<need or pain>` when `<situation>`."*
    - Supporting extracts: bullet list of verbatim ≤ 200-char extracts, each ending in `[SRC: <filename>]`.
    - Provenance markers: `(provenance: from-inputs)` (the inputs-side analyser collapses the four reverse-discovery provenance buckets into a single marker because raw inputs do not carry the canonical PRD section structure).
    - Cross-source: `Cross-source: yes (N sources)` or `Cross-source: no (single source: <filename>)`.
    - Flags (if any): `[UNADDRESSED]` (no source-grounded Solution children), `[WEAKLY-ANCHORED]` (no keyword overlap with primary Outcome).
7. **Solutions.** Grouped by parent Opportunity (sub-heading `### Under Op-NN`); plus a final group `### [ORPHAN-SOLUTION] Under Op-?: (none stated in inputs)` collecting solutions with no source-grounded parent Opportunity. Each Solution:
    - Verbatim text (`<verb> <object>` or `<feature name>`).
    - Source extract + `[SRC: <filename>]`.
8. **Assumption Tests.** Grouped by parent Solution (sub-heading `### For S-NN`). When Layer 4 is entirely absent, render the single placeholder line: *"`(no assumption tests in inputs)` — raw consultant inputs rarely carry explicit risk / assumption / open-question phrasing; this layer is expected to be absent. Add risk / assumption material to `input/` and re-run to populate it."*
9. **Opportunity Solution Tree.** A `#diagrams` section with the tree as a pre-rendered inline SVG (per the diagram spec below), and the `graph TD` source kept in an adjacent collapsed `<details class="mermaid-source">` block.
10. **Candidate requirements (bridge to `/requirements`).** Heading `## Candidate requirements`. One sub-section per Opportunity (`### From Op-NN`); each sub-section a bullet list of *"The system should `<verb> <object>` so that `<outcome>`."* lines, each ending in `[SRC: <filename>]` inherited from the parent Opportunity. Opportunities flagged `[UNADDRESSED]` render a single bullet: *"`(no source-grounded solutions; recommend-elicit-solution)` — the inputs name this opportunity but commit no solution to it. Add elicitation material naming candidate solutions to `input/` and re-run, or accept as out-of-scope."*
11. **Coverage diagnostics.** Heading `## Coverage diagnostics`. Four sub-lists (each emits an italic *"(no entries this run)"* line when empty):
    - **Orphan solutions** — solutions under sentinel `Op-?`.
    - **Unaddressed opportunities** — opportunities with no source-grounded Solution children.
    - **Weakly-anchored opportunities** — opportunities with no keyword overlap with the primary Outcome's measurement clause.
    - **Contradictions** — pairs of opportunities whose need clauses lexically conflict (e.g., one says *"must be fast"*, another says *"must be deliberate"*). Flagged for consultant interview; never auto-reconciled.
12. **Source roster.** Heading `## Source roster`. Two tables:
    - **Consumed**: one row per manifest entry whose `tier != "Unsupported"` (`filename`, `tier`, `sha256[:8]`, `node-count` = outcomes + opportunities + solutions + assumption tests cited from this file).
    - **Skipped**: one row per manifest entry whose `tier == "Unsupported"` (`filename`, reason).
13. **Run history.** Append-only bullet list of prior runs (timestamp, opportunity-count delta, solution-count delta, candidate-requirement-count delta, Override notes if applicable).

---

## Round 1 — Outcome extraction

Walk every consumable source for outcome-like signals:

- **KPI / metric tables** ("reduce churn to 5%", "increase weekly active users by 40%", "achieve 95th-percentile latency < 300 ms").
- **Goal statements** ("we want to …", "the project will be successful when …", "our objective is to …", "this initiative aims to …").
- **Success-criteria slides / sections** (often in briefs and proposal decks).
- **Business-case framing** (revenue lift, cost reduction, retention, market expansion).

For each candidate Outcome, capture:

```
{
  outcome_id,
  text,                                       // canonical form: "<metric or goal>, measured by <measurement>, by <horizon if stated>"
  classification,                             // business-outcome | product-outcome | traction-metric (Torres taxonomy)
  source_filenames: [<filename>...],          // ≥ 1
  extract: verbatim ≤ 200 chars               // anchoring quote
}
```

**Classification (Torres):**

| Class | What it measures |
|---|---|
| `business-outcome` | Financial / commercial metric (revenue, churn, market share, CAC, LTV). |
| `product-outcome` | Customer behaviour or sentiment in the product (activation, retention, NPS, task-completion-rate). |
| `traction-metric` | Adoption of a single feature (signups for X, opens of Y). Torres recommends a product outcome at the root. |

**Multiplicity handling:**

- **One candidate** → set as the primary root Outcome; advance to Round 2.
- **≥ 2 candidates** → surface an `AskUserQuestion` listing every candidate with its classification and supporting `[SRC: <filename>]`. Consultant picks the primary. Non-primary candidates are preserved with `[CANDIDATE-OUTCOME]` markers in the `## Candidate outcomes` section and do **not** ladder Opportunities (the tree has one root).
- **Zero candidates** after best-effort → hard halt with the structured error: *"No outcome-like signal was extracted from the consumed inputs. Add a brief / proposal / goal statement to `input/` and re-invoke `/analyse-inputs`."* (analogous to RF-03).

---

## Round 2 — Opportunity extraction

Walk every consumable source for customer-perspective need / pain / desire clauses. Sources are not section-typed (raw inputs lack the canonical `§Personas.Pains` / `§User stories` structure of merged PRDs); instead, the analyser scans for **clause shapes**:

- *"`<actor>` needs / cannot / wants `<need or pain>` …"*
- *"`<actor>` struggles with / is blocked by / loses time when …"*
- *"`<actor>` has no way to …"*
- *"Users complain that …"*, *"Customers report …"* (third-person observational shapes).

For each candidate Opportunity, capture:

```
{
  opportunity_id,
  actor,                                      // canonical persona name; harmonise variants ("warehouse lead" ≡ "warehouse manager")
  need_clause,                                // canonical form: "needs / cannot / wants <need or pain> when <situation>"
  source_filenames: [<filename>...],          // ≥ 1
  extracts: [(filename, verbatim ≤ 200 chars)...],
  cross_source: bool
}
```

**Canonical form:** *"`<actor>` needs / cannot / wants `<need or pain>` when `<situation>`."* `when <situation>` is optional but encouraged when the source supplies a trigger.

**Filter rules** (same discipline as the reverse-discovery sibling; adapted to raw inputs):

- **Reject solution-leaked Opportunities.** Forbidden tokens in the *need / pain* clause (case-insensitive substring match): `dashboard`, `screen`, `page`, `button`, `dialog`, `modal`, `dropdown`, `field`, `widget`, `report`, `export`, plus building verbs: `add`, `build`, `implement`, `create`, `provide`. Rewrite to the underlying need or reject. (Enforced by **Gate 3**.)
- **Reject company-perspective Opportunities.** Forbidden tokens: `we`, `our`, `the business`, `the company`, `the team`. Rewrite from the actor's perspective or reject. (Enforced by **Gate 2**.)
- **Reject feeling-only Opportunities.** A clause naming only a feeling (`frustrated`, `confused`, `worried`, `annoyed`) without a need / pain / desire is unactionable. Sharpen to the underlying need or reject.
- **Merge near-duplicates aggressively.** Raw inputs carry many wording variants of the same pain across multiple sources. Merge two Opportunities when they share the same canonical actor and their need clauses share ≥ 60% semantic overlap (the same noun-phrase head and a near-identical verb). Keep all source citations; pick the more specific wording for the canonical `need_clause`.
- **Harmonise actor names.** Variants of the same role across inputs (`warehouse lead`, `warehouse manager`, `WH supervisor`) collapse to a single canonical actor. Surface the harmonisation in diagnostics so the consultant can audit.
- **Unnamed actors.** When a source mentions a pain without naming an actor (*"someone needs to reconcile billing"*), assign `actor: unnamed-actor` and flag for consultant attention. Do not invent an actor.

**Source-citation requirement:** every Opportunity carries ≥ 1 `[SRC: <filename>]` per source, with verbatim extract ≤ 200 chars per source. No Opportunity is on the tree without a source-grounded extract.

---

## Round 3 — Solution extraction

Walk every consumable source for feature mentions, system asks, capability requests. Sources include:

- Brief / proposal feature lists.
- Workshop notes ("the system should …", "we need a way to …").
- Slide deck feature slides.
- Interview transcripts ("can the tool let me …").
- Annotated mockups / wireframes (Native-multimodal sources surface this via vision).

For each candidate Solution, capture:

```
{
  solution_id,
  text,                                       // verbatim "<verb> <object>" or "<feature name>"; no rewriting
  actor_hint,                                 // optional; harvested from the surrounding context if any
  source_filenames: [<filename>...],          // ≥ 1
  extract: verbatim ≤ 200 chars
}
```

**Canonical form:** verbatim text — `<verb> <object>` or `<feature name>`. The analyser does **not** rewrite Solution labels; the consultant's wording is the audit trail.

**Sparsity is expected.** Many consultant inputs describe pains and stop short of feature commitments. A Round-3 result with zero Solutions is permitted; every Opportunity will then carry the `[UNADDRESSED]` flag and the bridge section will recommend elicitation (Gate 5).

**Multi-source merging:** when two source files reference the same feature with near-identical wording, merge into one Solution and keep all source citations.

---

## Round 4 — Assumption-Test extraction (best-effort)

Walk only for explicit risk / assumption / open-question phrasing:

- *"Risk: …"*, *"Open question: …"*, *"We're assuming that …"*, *"We need to validate that …"*, *"What if …"*, *"Concern: …"*.

For each candidate Assumption Test, capture:

```
{
  assumption_test_id,
  text,                                       // verbatim test description
  category,                                   // desirability | viability | feasibility | usability | ethical (Torres taxonomy; default desirability if no keyword match)
  source_filenames: [<filename>...],          // ≥ 1
  extract: verbatim ≤ 200 chars
}
```

**Torres categories (keyword heuristics):**

| Category | Keyword cues |
|---|---|
| `desirability` | want, use, value, prefer, choose, churn, retention, NPS, sentiment |
| `viability` | revenue, margin, cost, ROI, commercial, legal, regulatory, license, contract |
| `feasibility` | latency, throughput, scale, performance, integration, API, infrastructure, technical, capacity, third-party |
| `usability` | usable, understand, accessible, learn, complete, abandon, drop-off, friction |
| `ethical` | harm, privacy, bias, fairness, consent, vulnerable, surveillance, dignity |

**Absent layer.** When Round 4 produces zero candidates, set `layer_4_absent = true`. Section 8 of the artefact renders the placeholder line; the Mermaid diagram omits the Layer-4 band entirely; the summary reports `assumption tests: absent`. **This is expected.** The analyser does **not** fabricate tests.

---

## Round 5 — Laddering

The four layers compose the tree by **parent edges**, not free-form association.

### Outcome ← Opportunity

Every Opportunity links upward to the **primary** root Outcome. The link is asserted by keyword overlap between the Opportunity's *need / pain* clause and the Outcome's *measurement* clause. When no overlap exists, the Opportunity carries the `[WEAKLY-ANCHORED]` flag and renders on the tree but is highlighted in `## Coverage diagnostics > Weakly-anchored opportunities`. The Opportunity is **not** repaired by reassignment to a `[CANDIDATE-OUTCOME]` — the tree's primary outcome anchors every Opportunity or the Opportunity is weakly anchored, full stop.

### Opportunity ← Solution

Every Solution links upward to **at most one** parent Opportunity by actor + need / pain semantic match:

- The Solution's `actor_hint` (if any) must match the Opportunity's canonical actor.
- The Solution's verbatim behaviour must address the Opportunity's *need / pain* clause.

**Multi-parent Solutions.** A Solution genuinely addressing two distinct Opportunities renders under its primary parent (the one with the strongest semantic match) and lists the secondary parent(s) inline. Flagged for consultant attention but not gated.

**Orphan Solutions.** A Solution with no source-grounded parent Opportunity in the inputs **never** has one fabricated. It lands under the sentinel parent `Op-?: (none stated in inputs)` with the `[ORPHAN-SOLUTION]` marker, rendering red-bordered in the Mermaid diagram. The gap is the finding.

### Solution ← Assumption Test

Every Assumption Test links to **one or more** Solutions whose assumptions it tests. The link is asserted by:

- Explicit cross-reference in the source (*"Risk: the integration may be slower than 5 s — risks the bulk-reconciliation feature"*).
- Semantic match on the Solution's behaviour.

When the link is implicit and the analyser cannot identify the Solution(s) the test concerns, the test attaches at the **Outcome level** as a global / cross-cutting assumption with the `global-assumption` flag.

---

## Round 6 — Bridge + diagnostics

### Sub-step A — Bridge (load-bearing addition vs the requirements-side sibling)

For each Opportunity in the tree, derive one or more **candidate-requirement** lines:

```
{
  opportunity_id,
  candidate_requirement_id,
  line: "The system should <verb> <object> so that <outcome>.",
  source_filenames: [<filename>...]      // inherited from parent Opportunity
}
```

**Shape rules:**

- *"The system should `<verb> <object>` so that `<outcome>`."* — solution-agnostic language. Prefer outcome wording (*"so that approvers can act within their permission scope"*) over implementation wording (*"using OAuth scopes"*). These are seeds for `/requirements`, not authored requirements.
- One bullet per candidate-requirement line; each line ends in `[SRC: <filename>]` per source.
- Citations inherit from the parent Opportunity.

**Sourcing:**

- When Solutions exist for the Opportunity, derive the `<verb> <object>` from the matched Solutions' verbatim text.
- When the Opportunity is `[UNADDRESSED]`, emit a single bullet: *"`(no source-grounded solutions; recommend-elicit-solution)` — the inputs name this opportunity but commit no solution to it. Add elicitation material naming candidate solutions to `input/` and re-run, or accept as out-of-scope."* This bullet satisfies **Gate 5**.

**Mechanism downstream:**

- When the consultant drops this artefact into `input/`, the input-handler classifies it as `Native-text` and the `/requirements` drafter reads the `## Candidate requirements` section as candidate-requirement seeds.
- The drafter normalises voice, assigns `R-NN` IDs, and merges into `§6` of `requirements/requirements-draft.md`. The drafter's `[SRC: C-NNN]` claim-IDs coexist with this artefact's `[SRC: <filename>]` markers in the draft; the merger strips both at requirements-finalisation time, producing a clean `requirements/requirements.md`.

### Sub-step B — Coverage diagnostics

Walk the laddered tree and populate four diagnostics sub-lists for `## Coverage diagnostics`:

- **Orphan solutions** — every solution under sentinel `Op-?`.
- **Unaddressed opportunities** — every opportunity with `[UNADDRESSED]` flag.
- **Weakly-anchored opportunities** — every opportunity with `[WEAKLY-ANCHORED]` flag.
- **Contradictions** — pairs of opportunities whose need clauses lexically conflict (e.g., share an actor + noun-phrase head but carry opposing verbs / qualifiers). Surface every pair; never auto-reconcile.

The diagnostics block is the audit value of the artefact — the consultant reads it to identify what to elicit, validate, or de-scope before `/requirements` runs.

---

## Mermaid diagram spec

- **Graph type:** `graph TD` (top-down). Outcome at the top reads cleanly to leaves.
- **Node shapes by layer:**

  | Layer | Mermaid syntax | Visual shape |
  |---|---|---|
  | Outcome (primary) | `O([Outcome: <text>])` | stadium |
  | Candidate outcome | `Cn([Candidate Outcome: <text>])` + `class Cn candidate;` | stadium with dashed border |
  | Opportunity | `Op1[Op: <actor> — <need clause>]` | rectangle |
  | Sentinel `Op-?` | `OpX[Op-?: none stated in inputs]` + `class OpX orphan;` | rectangle, red-bordered |
  | Solution | `S1{{<verbatim text>}}` | hexagon |
  | Orphan Solution | `S1{{<verbatim text>}}` + `class S1 orphan;` | hexagon, red-bordered |
  | Assumption Test | `A1[(<test text>)]` | cylinder |

- **Edges:**
  - Root → Opportunity: `O --> Op1`.
  - Opportunity → Solution: `Op1 --> S1`.
  - Sentinel → Orphan Solution: `OpX -.-> S2` (dashed, signals the gap).
  - Solution → Assumption Test: `S1 --> A1`.
  - Outcome → global Assumption Test (when no Solution link is identifiable): `O --> A0`.

- **Mermaid `classDef` block (emitted once, near top of diagram):**

  ```
  classDef candidate stroke-dasharray:5 5,stroke:#6b7280;
  classDef orphan stroke:#dc2626,stroke-width:2px,stroke-dasharray:3 3;
  ```

- **Candidate Outcomes are not rendered in the Mermaid tree.** Only the primary Outcome anchors the tree; the candidate outcomes live in `## Candidate outcomes` as text blocks. This keeps the diagram unambiguous (one root, one ladder) and matches the confirmed multi-outcome design decision.

- **Label-escaping rules.** Wrap node labels in double quotes when the text contains any of `[`, `]`, `(`, `)`, `"`, `{`, `}`, `|`. Example: `Op1["Op: Finance Manager — needs to reconcile (cross-system) billing errors"]`.

- **Truncation rule.** Mermaid labels exceeding 80 chars truncate to 77 chars + `…`; the full verbatim text lives in the corresponding body section anyway. The Mermaid diagram is a visual index, not the authoritative content.

- **No Mermaid validation.** The layered tree diagram is a pre-rendered, self-contained inline SVG (nodes + edges in one `viewBox`); the `graph TD` source beneath it is embedded as an unvalidated export adjunct (no `mmdc` dependency). Keep the SVG and the Mermaid source in agreement — every node is a `<g class="node …">` in the SVG and a node in the source.

---

## Source-of-truth hierarchy

The analyser reads exactly the files the manifest enumerates, plus the prior artefact (for additive merge) and its own three asset files. The manifest's `tier` field dictates the read path:

| Tier | Source location | Read mechanism |
|---|---|---|
| `Native-text` | `original_path` | `Read` directly as text |
| `Native-multimodal` | `original_path` | `Read` — Claude's vision surfaces image bytes; transcribe visible text / annotations / mockup labels |
| `Supported-via-MCP` | `converted_sibling` | `Read` the `.converted.md` (markitdown's output, produced by input-handler) |
| `Unsupported` | — | Skipped; recorded in `Source roster > Skipped` |

The analyser **never** reads:

- Any path under `requirements/` other than `requirements/source-manifest.json`.
- Any path under `framework/state/`.
- Any path under `framework/shared/` (textual references to `RF-NN` / `GR-NN` are links for the reader, not file loads).
- Other analyses' artefacts (`analyse-requirements/<OTHER-METHOD>/...`, `analyse-inputs/<OTHER-METHOD>/...`) — including `analyse-inputs/THEMATIC-ANALYSIS/thematic-analysis.html`, even though both lenses operate on the same inputs.
- Any pattern-catalogue or design-system file.

---

## Provenance markers

| Marker | Used in section | Payload | Meaning |
|---|---|---|---|
| `[SRC: <filename>]` | every layer + Candidate outcomes + Candidate requirements | manifest row's `filename` (basename with extension) | The cited outcome / opportunity / solution / assumption test / candidate-requirement is anchored to this manifest source; its extract is verbatim from the row's content |
| `[CANDIDATE-OUTCOME]` | Candidate outcomes section only | (none) | Outcome candidate that was **not** picked as the primary root by the consultant on first run; preserved for audit, not laddered |
| `[ORPHAN-SOLUTION]` | Solutions section + Coverage diagnostics | (none) | Solution with no source-grounded parent Opportunity in the inputs; rendered under sentinel `Op-?` |
| `[UNADDRESSED]` | Opportunities section + Candidate requirements + Coverage diagnostics | (none) | Opportunity with no source-grounded Solution children; bridge entry is a `recommend-elicit-solution` advisory |
| `[WEAKLY-ANCHORED]` | Opportunities section + Coverage diagnostics | (none) | Opportunity with no keyword overlap with the primary Outcome's measurement clause |

**No `[AI-SUGGESTED]` anywhere in the artefact.** OST is extraction, not inference. Every outcome, opportunity, solution, assumption test, and candidate-requirement line traces to a `[SRC: <filename>]` marker; the four no-payload markers above all flag *absence* or *non-primary status*, never *inference*.

---

## Quality gates (6 hard gates)

Run at Round 6 close, before render. Each check operates on the in-memory state.

1. **Citation completeness.** Every outcome / candidate outcome / opportunity / solution / assumption test / candidate-requirement line carries at least one `[SRC: <filename>]` marker, and every marker payload matches a manifest row's `filename` field exactly. Mismatch fails.
2. **Customer-perspective Opportunities.** No Opportunity's *need / pain* clause contains forbidden company-perspective tokens (`we`, `our`, `the business`, `the company`, `the team` — case-insensitive substring match). Flag offending Opportunities by id + offending text.
3. **No solution-leak in Opportunities.** No Opportunity *need / pain* clause contains UI-affordance tokens (`dashboard`, `screen`, `page`, `button`, `dialog`, `modal`, `dropdown`, `field`, `widget`, `report`, `export`) or building verbs (`add`, `build`, `implement`, `create`, `provide`). Flag offending Opportunities.
4. **Diagram completeness.** Every primary Outcome / Opportunity / Solution / Assumption Test in the in-memory tree appears as a node (`<g class="node …">`) in **both** the pre-rendered layered SVG tree diagram **and** the `graph TD` Mermaid export source; neither has dangling references, and every SVG edge `<path>` connects two node centres present in the SVG. (The Mermaid source is an unvalidated export adjunct — no `mmdc`.)
5. **Bridge completeness.** Every Opportunity in the tree has at least one corresponding line under `## Candidate requirements` — either a *"The system should ___ so that ___"* candidate-requirement seed, or (for `[UNADDRESSED]` Opportunities) the `recommend-elicit-solution` advisory bullet. No Opportunity disappears silently from the bridge.
6. **Manifest fingerprint + source roster.** The artefact carries exactly one `<!-- ost-meta: ... -->` line; its `manifest_fingerprint` value equals the Round 1 sha256; the `Source roster > Consumed` table enumerates every manifest row whose `tier != "Unsupported"`; the `Source roster > Skipped` table enumerates every manifest row whose `tier == "Unsupported"`; together they account for every manifest row.

### Relaxations from the requirements-side sibling, defended

The reverse-discovery sibling at `framework/assets/analyses/opportunity-solution-trees-reference.md` ships **seven hard gates**. The inputs-side analyser drops or relaxes three of them:

- **Dropped: "Exactly one root Outcome" (sibling gate 1).** Raw consultant material legitimately carries multiple stakeholder outcomes (the brief names one goal; the workshop notes another; the slide deck a third). Hard-halting on multi-outcome would be hostile and would force the consultant to reconcile outcomes before any analysis is possible — that reconciliation is itself the consultant's job and is informed by this analyser's output. **Replaced by interactive consultant pick** on first run + `[CANDIDATE-OUTCOME]` markers for the non-primary candidates (preserved for audit but not laddered).
- **Relaxed: "More-than-one-way-to-address" (sibling gate 3).** Raw inputs often capture only one mentioned solution per pain — the consultant has not yet brainstormed alternatives, the material is pre-synthesis. A 1:1 Opportunity-Solution pairing is **permitted** at the inputs stage; an Opportunity with zero source-grounded Solutions is **permitted** and flagged `[UNADDRESSED]` (informational, not a gate failure). The sibling's discipline (forcing ≥ 2 Solutions or an `unaddressed-in-requirements` flag) belongs to the audit stage, not the discovery stage.
- **Dropped: "No vertical-only branches warn" (sibling gate 4).** Inputs-side trees are sparse by nature — most inputs name two or three pains and zero or one solutions. Warning on every shallow branch would drown the diagnostics block in noise that the consultant cannot act on at the input stage. Re-introduce this check at the requirements-side audit, not here.

The three relaxations are defended at the methodology level (here) so the discipline is documented at the right altitude rather than encoded in the agent file alone.

### Failure handling (Revise / Override / Restart)

On any hard-gate failure: do **not** write the artefact. Surface `AskUserQuestion` with three options:

1. `Revise — exit so the consultant can enrich input/ and re-invoke /analyse-inputs (Recommended)`
2. `Override — proceed and write a known-defective artefact (Run-history bullet records every violation)`
3. `Restart — re-run from Round 1 with a fresh manifest pass`

On **Revise**: hand back to the orchestrator with a `failed-handback` state.
On **Override**: record each failing gate in the Run-history bullet for this run; proceed to render.
On **Restart**: re-enter Round 1. Cap at three fail-Restart cycles; on the fourth, force the Revise path.

---

## Stop-condition

The analysis is complete when:

- A primary root Outcome exists (Round 1 produced ≥ 1 candidate, and the consultant picked one on multi-candidate runs).
- All 6 hard gates pass, or the consultant chose Override and the failures are recorded in Diagnostics.
- Every node is a `<g class="node …">` in the pre-rendered layered SVG tree diagram and a node in the `graph TD` Mermaid export source (embedded as unvalidated text).
- `analyse-inputs/OPPORTUNITY-SOLUTION-TREES/opportunity-solution-tree.html` has been written and `verify-artifact-write` returned `pass`.
- The consultant chose Accept in the handback loop.

---

## Re-run semantics

- The cursor (`manifest_fingerprint`, `run_count`) lives in the artefact's HTML-comment header. No state file under `framework/state/`.
- On re-run, the analyser compares the current manifest fingerprint to the prior cursor's value:
  - **No change** → pure additive widening; only new nodes from new manifest rows extend the prior tree (if they ladder under an existing Opportunity / Outcome) or seed new nodes.
  - **Change** → the analyser surfaces a drift prompt: `append-new-nodes-only` (default, preserves prior tree verbatim; appends new nodes that ladder under existing parents or seed new ones), `re-extract-everything` (re-runs Rounds 1–5 from scratch on the current manifest; ids preserved where re-laddering produces equivalent nodes), or `abort` (exit without writing).
- The artefact is monotonically growing across runs unless the consultant explicitly chose `re-extract-everything` or manually edited the file.
- The primary Outcome is preserved across runs unless `re-extract-everything` re-surfaces multiple candidates and the consultant explicitly re-picks.

---

## Downstream consumption (handled by `framework/skills/map-opportunity-solution-trees-from-inputs-to-ui.md`)

The analyser does not author UI primitives; the downstream mapping is **signal-based**, not affordance-based:

- **Outcome catalogue** → routed to product-strategy alignment signals for design-spec consumers. The primary Outcome anchors the design's value proposition; candidate Outcomes inform stakeholder-alignment conversations.
- **Opportunity catalogue** → routed to feature-cluster seeds (one cluster per Opportunity; cluster name seeded by canonical `<actor> — <need clause>`).
- **Candidate-requirement lines** → routed to acceptance-criteria seeds for the `/requirements` drafter (same channel as `thematic-analysis`'s bridge). This is the load-bearing downstream connection; the analyser is the **only** input-analyser besides `thematic-analysis` that produces a per-opportunity / per-theme bridge of candidate-requirement seeds.
- **Orphan solutions** → routed to consultant-interview prompts (*"the inputs name solution X but no source-grounded opportunity it addresses; what need does it serve?"*).
- **Unaddressed opportunities** → routed to consultant-interview prompts (*"opportunity Y has no solution in the inputs; should it be deferred, out-of-scope, or does it imply a missing feature?"*).
- **Weakly-anchored opportunities** → routed to consultant-interview prompts (*"opportunity Z doesn't keyword-match the outcome; is it relevant?"*).
- **Contradictions** → routed to consultant-interview prompts (*"opportunities A and B carry opposing need clauses; which represents the authoritative requirement, or do both need accommodating?"*).
- **Manifest fingerprint** → used by re-runs to detect drift between the analysis and the current manifest; not routed to design consumers.

`map-opportunity-solution-trees-from-inputs-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character file and for future downstream design-spec authors.
