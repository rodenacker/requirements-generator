<!-- ROLE: asset (review reference). Loaded by framework/agents/reviews-inputs/gap-analysis-reviewer.md at activation. -->

# reviews-inputs/gap-analysis-reference.md

**Purpose:** Methodology reference for **Gap Analysis** (inputs-side) — a template-bijection delta of the **raw consultant input set** enumerated by `requirements/source-manifest.json` against the `/requirements` drafter's specific template (`framework/assets/topics-requirements.md`). The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews-inputs/gap-analysis-reviewer.md` — drives the agent's topic-walk, coverage classification, severity scoring, recommendation + candidate-requirement composition, cross-dimension consolidation, and quality-gate sweep.

**Output produced by the reviewer:** `review-inputs/GAP-ANALYSIS/gap-analysis.html` — a self-contained HTML artefact with an inline-SVG coverage heatmap, a gap matrix table, per-dimension narrative, an action list, an embedded structured JSON block (the `/requirements` re-ingestion carrier), and diagnostics.

**Sibling lenses under `/review-inputs`:**

- `framework/assets/reviews-inputs/completeness-reference.md` — sweeps a ten-dimension RE-canon completeness check (IEEE 29148 / IEEE 830 / Volere / BABOK / Wiegers / INCOSE / ISO 25010) and produces a markdown register with disposition flags (Needs-Clarification / Standard-Rule-Applies / Out-of-Scope) and per-source stakeholder elicitation questions. **Yardstick = the BA literature canon.**
- `framework/assets/reviews-inputs/adversarial-reference.md` — six-dimension BMAD-style critique of the corpus (voice authenticity, ambiguity, conflict, etc.). Clusters defects thematically.
- `framework/assets/reviews-inputs/ambiguity-reference.md` — seven-dimension Berry/Kamsties + Femmer linguistic-ambiguity taxonomy. **≥2-interpretations test** on every finding.

This reference's **yardstick = `framework/assets/topics-requirements.md`** — the project's own template. Where completeness-review asks *"is this input set complete by professional BA standards?"*, this lens asks *"is this input set complete by **this drafter's** template?"*. The two methodologies are independent and complementary; either, both, or neither may run on a given input set; the artefacts coexist and the lenses do not cross-read each other.

---

## 1. Industry framing

**Gap Analysis** has several converging lineages, all centred on the same core operation: a structured comparison between a desired state (To-Be) and an actual state (As-Is), with the delta logged as actionable gaps.

- **Strategic management** — McKinsey 7S framework (Peters & Waterman, 1980); SWOT-adjacent posture analysis.
- **Business analysis canon** — **BABOK v3 (IIBA, 2015)** §10.21 (Process Analysis) and §10.32 (Requirements Analysis Quality Characteristics) frame gap analysis as a discovery + validation activity; §6.4 (Requirements Life Cycle Management) and §10.36 (Solution Scope Definition) describe the gap → requirement hand-off.
- **Architecture canon** — **TOGAF 9.2 §23 "Gap Analysis"** publishes the canonical Gap Matrix (rows = capabilities, columns = As-Is / To-Be / Gap / Action) and is the most rigorous published taxonomy for software/architecture work; distinguishes "people, process, technology" gap classes.
- **Software requirements canon** — **ISO/IEC/IEEE 29148:2018** §5.2.5 (completeness as a stakeholder-requirement attribute) and §6.4.2.3 (the nine completeness checks for a system requirements specification); **IEEE 830-1998** §4.3.7 (completeness); **Wiegers & Beatty, *Software Requirements* 3rd ed.** Ch. 17 separates "missing requirements" (internal gaps) from "requirements that imply change to existing systems" (external gaps).
- **Quality model** — **ISO/IEC 25010:2011** quality attributes (Functional Suitability, Performance Efficiency, Compatibility, Usability, Reliability, Security, Maintainability, Portability) anchor the Non-functional dimension.
- **Fit-Gap (ERP variant)** — SAP Activate methodology and Salesforce Implementation Playbooks formalise gap analysis with a fixed As-Is (the packaged product's out-of-box capability) and a parametric To-Be (the client's requirements).

**How this lens specialises the canon.** When the source material is a brief / PRD / deck / spreadsheet *rather than* a live system, the As-Is is genuinely absent or thin. The textbook handling is two-fold:

- **Internal gaps** — what the inputs *fail to specify*. This is canonically called **requirements completeness analysis** or **specification gap analysis** (IEEE 830 §4.3.7; IEEE 29148 §5.2.5; Wiegers Ch. 17).
- **External gaps** — build/change deltas vs an As-Is reference. This is the classical Fit-Gap pattern but requires an As-Is which most greenfield projects lack.

**This reference scopes to internal gaps**, with the To-Be = `topics-requirements.md` (the project's template). The reviewer does **not** attempt to construct an As-Is from the inputs; the gap is purely "does the corpus supply enough content for the drafter to populate this template section without fabricating?".

**Distinguishing from related techniques:**

- **SWOT** — strategic posture (internal vs external, positive vs negative); not delta-focused. May feed gap-analysis but doesn't replace it.
- **Five-Whys / RCA** — explains *why* a gap exists; gap-analysis identifies *that* it exists and its size.
- **Feasibility analysis** — asks *can we close the gap?*; gap-analysis asks *what is the gap?*.

---

## 2. Operational definition

**To-Be:** `framework/assets/topics-requirements.md` — the project's canonical list of topics every `/requirements` artefact must cover, with per-topic emit predicates, Tier A/B/C/D completeness rules, and per-topic `Dimension` values (SPoT). 30+ topics spanning §0.1, §1, §1.5, …, §10.

**As-Is:** the raw consultant input set enumerated by `requirements/source-manifest.json` — every manifest row whose `tier != "Unsupported"` is read once via its `original_path` (Native tiers) or `converted_sibling` (Supported-via-MCP tier).

**The gap** = the per-topic delta. For every topic the reviewer walks the six-step decision tree in §4 below and assigns one of six coverage states. Two of those states (`Missing` and `Partial`) produce `GAP-NN` rows in the artefact; the other four (`Covered`, `Standard-rule`, `Out-of-scope`, `N/A`) appear in the coverage matrix and per-dimension narrative but carry no `GAP-NN`.

**Pipeline contribution.** Each `Missing` or `Partial` gap row ships with:

- A **Recommendation** (analyst prose) — the consultant's decision-question.
- A **Candidate Requirement** (shall-form, behavioural) — the drafter-ingestible candidate that would close the gap.
- A severity bucket (`MoSCoW`, derived from Impact × Confidence).

When the consultant copies the produced `gap-analysis.html` into `input/` and runs `/requirements`, the embedded structured JSON block is parsed by the drafter (via markitdown HTML→MD conversion). Candidate Requirements keyed by `topic_ref` give the drafter pre-formed candidates for exactly the topics that would otherwise hit the `completeness-gap-pass` skill's `[AI-SUGGESTED]` fabrication path. Gaps the consultant has already seen and (by not removing them) endorsed become drafter-cited requirements (`[SRC: gap-analysis.html]`) instead of drafter-fabricated `[AI-SUGGESTED]` ones. Resolver Q&A burden drops correspondingly.

---

## 3. Sibling-methodology relationship to `completeness-review`

These two `/review-inputs` methodologies are **complementary, not redundant.** They share the "what's absent" question but diverge on three load-bearing axes:

| Axis | `completeness-review` | `gap-analysis` (this lens) |
|---|---|---|
| **Yardstick** | BA-canon (IEEE 29148 / Volere / BABOK / Wiegers / INCOSE / ISO 25010), ten RE dimensions | This project's `framework/assets/topics-requirements.md`, 30+ template topics |
| **Implicit question** | *"Is this input set complete by professional BA standards?"* | *"Is this input set complete by **this drafter's** template?"* |
| **Catches gaps like** | "no first-hand Finance Manager voice", "no exclusion list", "vague NFR keyword with no threshold" | "no `§6.3 Validation rules` content", "no `§10 Volumes`", "no `§6.5 RBAC` matrix" |
| **Downstream verb** | *"go elicit"* (each finding ships with a stakeholder elicitation question) | *"ratify, edit, or reject this candidate"* (each gap ships with a shall-form Candidate Requirement) |
| **Disposition vocabulary** | Needs-Clarification / Standard-Rule-Applies / Out-of-Scope (markdown) | Covered / Partial / Missing / Standard-rule / Out-of-scope / N/A (HTML, six-state) |
| **Output** | Markdown register + markdown coverage matrix | HTML + inline-SVG coverage heatmap + HTML gap matrix |
| **Severity** | Blocker / Major / Minor + disposition flag | Impact × Confidence → MoSCoW (closed matrix) |

**Either, both, or neither may run on a given input set.** A consultant who wants a broad authority-grounded punch-list for client follow-up picks completeness-review; one who wants a visual drafter-aligned gap map with pre-drafted requirements picks gap-analysis. Many consultants will run both for thorough coverage.

The reviewer does **not** read completeness-review's artefact (or any other sibling reviewer's output) under any circumstances. Each lens is independently grounded in the manifest; cross-reading would conflate methodologies and produce correlated noise.

---

## 4. Six-state coverage vocabulary (closed set)

Every topic in `topics-requirements.md` resolves to exactly **one** of six coverage states. The reviewer walks the following decision tree (in order, stop at first match):

1. **`Stated-in-inputs?`** — at least one manifest-cited source supplies content satisfying the topic's Tier-A bijection rule (or, for topics without a Tier-A rule, a content-threshold appropriate to the topic's nature).
    - **All threshold sub-aspects covered** → mark `Covered`. Cite `[SRC: <filename>]` per evidence aspect.
    - **Some sub-aspects covered, others silent** → mark `Partial`. Cite covered aspects; the gap row's `problem` field names what is silent. **Produces a `GAP-NN` gap row.**
2. **`Deterministically resolvable via GR-NN?`** — `framework/shared/general-rules.md` carries a rule whose `Applies to:` predicate matches the topic content-wise. → mark `Standard-rule`. Cite the rule ID.
3. **`Out of scope per prototype-scope.md?`** — `framework/shared/prototype-scope.md` excludes the topic under `manifest.target == "prototype"`. → mark `Out-of-scope`. Cite the scope predicate. (When `manifest.target == "application"` or `null`, the prototype-scope filter is not applied; topics that would have been Out-of-scope under prototype default to one of the other states.)
4. **`Conditional emit predicate is false?`** — topic's `Emit predicate` in `topics-requirements.md` is conditional (e.g. §2.5 only when ≥1 aggregate has >2 lifecycle states) and the corpus does not satisfy the predicate. → mark `N/A`.
5. **Otherwise** → mark `Missing`. Evidence carries the sentinel `(no mention in consumed corpus)`. **Produces a `GAP-NN` gap row.**

**Closed-set discipline.** The six states map directly onto the drafter's downstream marker namespaces:

- `Covered` → drafter consumes the cited inputs at face value; no marker.
- `Partial` → drafter consumes what's cited; remaining sub-aspects route through the drafter's classification (drafter fills via `[AI-SUGGESTED]` or `[STANDARD-RULE]` per its own rubric). The gap-analysis artefact ships a Candidate Requirement the drafter may adopt.
- `Missing` → drafter fills via `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` per `completeness-gap-pass.md`. The gap-analysis artefact ships a Candidate Requirement the drafter may adopt with `[SRC: gap-analysis.html]` citation.
- `Standard-rule` → drafter renders `[STANDARD-RULE: GR-NN]`.
- `Out-of-scope` → drafter renders `[OUT-OF-SCOPE: domain-default]` (prototype) or fills silently (application).
- `N/A` → drafter does not emit the topic at all.

Surfacing `Standard-rule` / `Out-of-scope` / `N/A` states is the methodology's pipeline-contribution discipline. The reviewer **never silently drops** these states — they appear in the coverage matrix and per-dimension narrative as non-gap rows so the consultant sees how the drafter will resolve the topic downstream.

---

## 5. Eight-dimension taxonomy (SPoT-owned)

The dimension classification is **defined in** `framework/assets/topics-requirements.md` — the section-list table's `Dimension` column carries one value per topic, drawn from this closed eight-value taxonomy:

| Dimension | One-line definition |
|---|---|
| `Stakeholder` | Personas, roles, actor identities, RBAC scopes — *who* the system serves. |
| `Scope` | Context, in/out/deferred boundaries, assumptions, architectural implications, source UI references — *what frame* the system operates in. |
| `Domain` | Concepts, relationships, aggregates, lifecycles, state transitions, glossary — *what objects* the system manipulates. |
| `Functional` | Features, business rules, validation rules, UI feature needs, reporting — *what the system does*. |
| `Process` | Task flows, edge/empty/error states, notification points — *how work moves through* the system. |
| `Non-functional` | Session UX, FE performance budgets, accessibility, volumes — *how well* the system behaves. |
| `Compliance` | Compliance UI behaviour, audit-trail UI feature — *what regulatory / audit obligations* surface. |
| `Integration` | Consumed backend contracts — *what external systems* the system depends on. |
| `Data` | Data shapes consumed by the FE, derivations — *what the FE displays / consumes*. |

The reviewer reads the `Dimension` value from the topic's row in `topics-requirements.md` at runtime (Step 3) and uses it verbatim. **The reviewer never invents a dimension.** If a topic in `topics-requirements.md` carries no `Dimension` value (schema violation), the reviewer halts with a structured error — the fix is upstream in `topics-requirements.md`, not in the reviewer.

This SPoT design ensures that adding a new template topic (e.g. `§6.11 New section`) requires only one edit: filling the new row's `Dimension` cell. The gap-analysis reviewer auto-classifies gaps for the new topic on the next run; no edits to this reference, the agent, the template, or the character file.

---

## 6. Severity rubric (Impact × Confidence → MoSCoW)

Every `Missing` and `Partial` gap row carries three severity fields:

- `impact` — reviewer's judgement of "what breaks downstream if this gap is not addressed before drafting":
    - `Critical` — drafting cannot proceed without a Q&A round; drafter's `[AI-SUGGESTED]` fabrication would be load-bearing for downstream design.
    - `High` — drafting can proceed but a Q&A round is highly likely.
    - `Medium` — drafting proceeds; gap surfaces during merger or design.
    - `Low` — cosmetic, easily resolved at design time.
- `confidence` — reviewer's certainty that this is a real gap (vs silent-intent):
    - `Confirmed` — the topic carries a Tier A bijection rule in `topics-requirements.md` (the project's canon demands it; absence is genuine omission).
    - `Likely` — Tier B (soft references); the topic is expected but absence could plausibly be silent-intent.
    - `Speculative` — the reviewer is reading absence-of-evidence and the inputs may simply not have surfaced the topic yet.
- `moscow` — derived **deterministically** from Impact × Confidence per the closed matrix:

| Impact \ Confidence | Confirmed | Likely | Speculative |
|---|---|---|---|
| Critical | Must | Must | Should |
| High | Must | Should | Should |
| Medium | Should | Could | Could |
| Low | Could | Could | Won't |

**The Confidence-honesty rule.** `confidence == Confirmed` is gated on Tier A bijection rules (per `topics-requirements.md`'s Tier classification). A reviewer who marks a Tier-B miss as Confirmed to upgrade its MoSCoW bucket commits the canonical gap-analysis anti-pattern (gap-count inflation — BABOK §10.38). Gate 3 enforces.

**Why not Impact × Effort?** Effort scoring requires architectural context the reviewer hasn't seen (it's reading a brief, not designing a build). Low-confidence effort scores would degrade the artefact's authority. Confidence, in contrast, directly answers the canonical gap-analysis anti-pattern *"absence-of-evidence ≠ evidence-of-gap"* — named in BABOK §10.32 and operationalised here via the Tier A / B / C / D classification the project already maintains.

---

## 7. Recommendation vs Candidate Requirement contract

Every `Missing` and `Partial` gap row produces two action cells. Both must be populated (gate 5 enforces parity).

**Recommendation** — analyst voice, one sentence. Surfaces the consultant's decision-question. Examples:

- *"Define how Admin permissions are scoped for the Customer entity."*
- *"Capture the legacy invoicing API contract, or confirm there is no legacy system to integrate with."*
- *"Decide whether multi-tenant deployments are in V1 scope or deferred to phase 2."*

**Candidate Requirement** — shall-form, behavioural, ≥1 sentence. Drafter-ingestible. Capability-category vocabulary only (per `GR-20`); no UI-layout vocabulary (per `GR-21`); no architecture / vendor / stack specifics. Examples:

- *"The system shall expose an Admin-only configurable permission matrix for every entity covering read, create, update, delete, and archive operations."*
- *"The system shall consume the legacy invoicing API via a synchronous read contract and shall surface unavailability with a user-visible banner and disabled affected CTAs."*
- *"The system shall scope V1 access to single-tenant configurations."*

**Forbidden in Candidate Requirements (gate 4 enforces):**

- Architecture verbs: `build`, `implement with`, `use Kafka`, `deploy to AWS`, `use Postgres`. → Capability-category only.
- UI-layout vocabulary: `modal`, `dialog`, `inline red text`, `table`, `card grid`. → Behavioural only.
- Vendor or stack-specific names — generic capability vocabulary only.

**For `Won't` MoSCoW rows**, the Candidate Requirement may be the literal sentinel `(deferred — no candidate requirement issued)`. The Recommendation is still populated (typically *"Defer to phase 2 or accept as out-of-scope"*).

**Parity discipline.** A Candidate Requirement's behavioural outcome must logically resolve the Recommendation's decision-question. Both cells share the same gap row and the same `topic_ref` and `dimension`. Gate 5 enforces parity at validation time.

**Why split the column?** A single shall-form column reads as preemptive specification and creates friction in the consultant accept gate. A single prose column means the drafter has to rewrite every recommendation into shall-form on ingestion, losing the source-grounding chain. The split keeps both audiences served: first-read consultants get prose; drafter re-ingestion gets shall-form.

---

## 8. Eight-round workflow

The reviewer runs 12 steps total (4 operational + 8 rounds). The eight rounds are:

1. **Round 1 — Topic walk.** Read `topics-requirements.md` and, for every row, walk the §4 decision tree against the ingested corpus. Record `(topic_ref, dimension, coverage, evidence)` per topic. Dimension is read verbatim from the topic's `Dimension` cell — never invented.
2. **Round 2 — Severity.** For every `Missing` or `Partial` topic, score Impact × Confidence. Apply the matrix to derive MoSCoW. Enforce the Confidence-honesty rule (Confirmed only when topic carries Tier A bijection rule).
3. **Round 3 — Recommendation + Candidate Requirement.** Per gap row: write Recommendation (prose, analyst voice) + Candidate Requirement (shall-form, behavioural, no solutioning). Cite evidence on every Partial row.
4. **Round 4 — Coverage matrix.** Compute aggregate counts per top-level template section × coverage tier (heatmap data) and per-dimension × MoSCoW (executive summary).
5. **Round 5 — Cross-dimension consolidation.** Where a single corpus span produces multiple findings (e.g. silence on RBAC produces both a `§6.5 Stakeholder` gap and a `§3 Personas` gap), keep both findings but cross-reference them via `also_see: [GAP-NN]` cells. Same discipline `completeness-reviewer` Step 14 enforces.
6. **Round 6 — Self-validate.** Run the eight quality gates (§9 below). On failure, surface `AskUserQuestion` (Revise / Override / Restart).
7. **Round 7 — Render + write + verify.** Read template, build substitution map, HTML-escape every consultant-supplied string, compute SHA-256, write to `review-inputs/GAP-ANALYSIS/gap-analysis.html`, invoke `verify-artifact-write.md` (`expected_min_bytes = 6144`).
8. **Round 8 — Handback.** Unicorn-voice summary; sibling-methodology hint; Accept / Revise / Restart loop.

The four operational steps preceding the eight rounds are: (1) Activate, (2) Read manifest + per-tier ingest, (3) Read bijection target (`topics-requirements.md` + `general-rules.md` + `prototype-scope.md`), (4) Detect prior artefact (drift gate).

---

## 9. Quality gates (eight, all hard)

Every gate runs at Round 6 (Step 10 of the agent). On any gate failure, the reviewer surfaces a structured error via `AskUserQuestion` and does **not** write the artefact unless the consultant chooses Override.

1. **Bijection completeness.** Every topic in `topics-requirements.md` produces exactly one coverage row in the artefact (no topics omitted, no duplicates). The count of coverage rows equals the count of topics in the section-list table (modulo `N/A` topics, which appear in the coverage row set but not in the heatmap).
2. **Evidence requirement.** Every `Covered` and `Partial` row carries ≥1 `[SRC: <filename>]` citation, and every cited filename matches a manifest row's `filename` field. Every `Standard-rule` row cites a `GR-NN` that exists as a heading in `framework/shared/general-rules.md`. Every `Out-of-scope` row cites a `prototype-scope.md` predicate phrase. Every `Missing` row's Evidence is the literal sentinel `(no mention in consumed corpus)`.
3. **Confidence honesty.** No `Missing` or `Partial` gap row has `confidence == Confirmed` unless its `topic_ref` carries a Tier A bijection rule in `topics-requirements.md`. Tier B / C / D topics cap at `confidence ≤ Likely`. (When the Tier classification cannot be unambiguously determined from `topics-requirements.md`, the reviewer caps Confidence at Likely.)
4. **No solutioning leak.** Pre-write Grep guards (mirroring drafter's `GR-20` / `GR-21`) catch architecture verbs, vendor/stack names, and UI-layout vocabulary in any `candidate_requirement` cell. Behavioural / capability-category vocabulary only.
5. **Recommendation–CandidateRequirement parity.** Every gap row's `recommendation` and `candidate_requirement` cells are both populated (or the Candidate Requirement carries the literal sentinel `(deferred — no candidate requirement issued)` for `Won't` rows). The two cells share the same `topic_ref` and `dimension`.
6. **Dimension fidelity.** Every gap row's `dimension` value is one of the closed eight, sourced verbatim from the topic's `Dimension` cell in `topics-requirements.md`. The reviewer never invents a dimension.
7. **GAP-NN gap-free.** IDs are monotonic from `GAP-01` with no gaps and no duplicates. Re-numbered after the Revise loop if any gap row is struck or merged.
8. **Manifest + template fingerprints.** The embedded `gap-analysis-meta` JSON block carries non-empty `manifest_sha256` and `topics_requirements_sha256` values; both are recomputed at write time. No `[AI-SUGGESTED]` markers anywhere in the artefact body.

**On gate failure:** the reviewer surfaces *"Quality gates fired: `{list}`. How should this run proceed?"* with options `Revise / Override / Restart`. Override writes the artefact with every flagged item recorded in the diagnostics block (the consultant explicitly accepted the violations).

---

## 10. Output structure (`review-inputs/GAP-ANALYSIS/gap-analysis.html`)

Self-contained HTML5. No external CSS / JS / fonts / CDNs. Opens cleanly via `file://`; prints sensibly to PDF via the browser's native dialog.

**Section ordering (fixed):**

1. **Title + metadata block.** `<h1>Gap Analysis (inputs-side)</h1>` plus a metadata table listing `Generated-At` (ISO-8601 UTC), `Manifest fingerprint` (manifest SHA-256), `topics-requirements.md fingerprint` (template SHA-256), `Target` (the manifest's `target` field, or `null`), `Reviewer Identity` (fixed string), `Sources Consumed` (count), `Sources Skipped` (count).
2. **Executive summary.** Total gap rows; per-dimension counts; per-MoSCoW counts; per-coverage-state counts; verdict (one of `BLOCKED` / `NEEDS-DECISIONS` / `ACCEPTED-WITH-CANDIDATES` per the verdict rubric below).
3. **Verdict.** Exactly one of the three values, on its own line in bold, preceded by `Verdict:`.
4. **Coverage Heatmap (inline SVG).** 10 rows × 5 columns. Rows = top-level template sections (`§1 Context`, `§2 Domain`, `§3 Personas`, `§4 Goals & Stories`, `§5 Flows`, `§6 Functional+NFR+RBAC`, `§7 Data`, `§8 UI refs`, `§9 Glossary`, `§10 Volumes`). Columns = coverage tiers (`Covered`, `Partial`, `Missing`, `Standard-rule`, `Out-of-scope`). Cell value = topic count. Cell intensity = severity-weighted (Missing × Critical = darkest red; Covered = green). Fixed `viewBox="0 0 1080 640"`.
5. **Gap Matrix table** (HTML). Columns: `GAP-NN | §Topic | Dimension | Coverage | Impact | Confidence | MoSCoW | Recommendation | Candidate Requirement | Evidence | also_see`. Sticky header (CSS only — `position: sticky`), zebra rows, MoSCoW colour bands.
6. **Action list.** Filtered subset of the gap matrix where `moscow ∈ {Must, Should}`. Rendered as an ordered list, each item showing `GAP-NN | topic_ref | candidate_requirement`. The list the consultant copies for downstream consumption.
7. **Per-dimension narrative.** Eight sections, one per dimension that produced ≥1 gap row. Each section: dimension name + per-gap-row block (`GAP-NN`, coverage, MoSCoW, recommendation, candidate requirement, evidence). Dimensions with zero gap rows are omitted from this section (their coverage cells still appear in the heatmap).
8. **Source roster.** Two tables. **Consumed:** `filename | tier | sha256[:8] | covered-count | partial-count | missing-count`. **Skipped:** `filename | reason`, or the line *"(no sources skipped this run)"*.
9. **Structured JSON block** (`<script type="application/json" id="gap-analysis-meta">`). Schema in §11 below. This is the carrier the `/requirements` drafter parses when the artefact is re-ingested.
10. **Diagnostics** (collapsed by default — `<details>` element). Five subsections: Quality gates (all 8, PASS/FAIL with flagged items), Coverage map (per consumed filename counts), Override log, Run history (single line: *"Full overwrite per run; no carried-over findings."*), Schema-drift detection (manifest + topics-requirements.md SHA-256 vs prior artefact's values if available).

**Verdict rubric:**

- `BLOCKED` — at least one gap row carries `(coverage = Missing, moscow = Must, confidence = Confirmed)`. The drafter cannot proceed without addressing.
- `NEEDS-DECISIONS` — no Blocking gaps as defined above, but ≥1 gap row carries `moscow ∈ {Must, Should}`. The drafter can proceed but the consultant should ratify Candidate Requirements first.
- `ACCEPTED-WITH-CANDIDATES` — all gap rows are `Could` or `Won't`, **or** zero gap rows exist run-wide. The artefact ships clean; the drafter may proceed and any candidates serve as defensive coverage.

---

## 11. JSON schema (the `gap-analysis-meta` block)

Embedded as `<script type="application/json" id="gap-analysis-meta">` in the produced HTML. Survives markitdown HTML→MD conversion as a fenced ` ```json ` code block. Schema:

```json
{
  "schema_version": "1.0",
  "manifest_sha256": "<64-hex>",
  "topics_requirements_sha256": "<64-hex>",
  "generated_at": "<ISO-8601 UTC>",
  "target": "prototype | application | null",
  "verdict": "BLOCKED | NEEDS-DECISIONS | ACCEPTED-WITH-CANDIDATES",
  "coverage_summary": {
    "by_section": {
      "§1": {"Covered": 0, "Partial": 0, "Missing": 0, "Standard-rule": 0, "Out-of-scope": 0, "N/A": 0},
      "§2": {...},
      "...": "..."
    },
    "by_dimension": {
      "Stakeholder": {"Covered": 0, "Partial": 0, "Missing": 0, "Standard-rule": 0, "Out-of-scope": 0, "N/A": 0},
      "Scope": {...},
      "Domain": {...},
      "Functional": {...},
      "Process": {...},
      "Non-functional": {...},
      "Compliance": {...},
      "Integration": {...},
      "Data": {...}
    },
    "by_moscow": {"Must": 0, "Should": 0, "Could": 0, "Won't": 0}
  },
  "coverage_rows": [
    {
      "topic_ref": "§N.M",
      "topic_title": "<verbatim from topics-requirements.md>",
      "dimension": "<one of eight>",
      "coverage": "Covered | Partial | Missing | Standard-rule | Out-of-scope | N/A",
      "evidence": ["[SRC: <filename>]", "..."]  // OR ["GR-NN"] for Standard-rule, OR ["<scope predicate>"] for Out-of-scope, OR ["(no mention in consumed corpus)"] for Missing, OR [] for N/A
    }
    // ... one row per topic in topics-requirements.md
  ],
  "gaps": [
    {
      "id": "GAP-NN",
      "topic_ref": "§N.M",
      "dimension": "<one of eight>",
      "coverage": "Partial | Missing",
      "impact": "Critical | High | Medium | Low",
      "confidence": "Confirmed | Likely | Speculative",
      "moscow": "Must | Should | Could | Won't",
      "recommendation": "<analyst prose, one sentence>",
      "candidate_requirement": "The system shall... | (deferred — no candidate requirement issued)",
      "evidence": ["[SRC: <filename>]", "..."]  // OR ["(no mention in consumed corpus)"] for pure Missing
      ,
      "also_see": ["GAP-NN", "..."]
    }
    // ... one entry per gap row (Partial or Missing coverage only)
  ],
  "source_roster": {
    "consumed": [
      {"filename": "<basename>", "tier": "Native-text | Native-multimodal | Supported-via-MCP", "sha256_short": "<8-hex>"}
    ],
    "skipped": [
      {"filename": "<basename>", "reason": "<from manifest>"}
    ]
  },
  "quality_gates": [
    {"id": 1, "name": "Bijection completeness", "status": "PASS | FAIL", "flagged": []}
    // ... gates 2..8
  ]
}
```

**Schema-version discipline.** The `schema_version` field starts at `"1.0"`. Additive schema changes (new optional fields) keep `schema_version: "1.0"`. Breaking changes (field-rename, type-change, semantic-shift) bump to `"2.0"` and the drafter's ingestion logic must guard on the version.

**Drift detection.** When the consultant re-runs gap-analysis, the reviewer reads any prior artefact (Step 4 — Detect prior artefact) and parses its `manifest_sha256` and `topics_requirements_sha256`. If both match the current values, the reviewer reports "no drift detected; coverage state would be identical" and prompts the consultant to confirm Overwrite anyway. If either has changed, the reviewer reports which fingerprint drifted and proceeds with a fresh sweep.

---

## Used by

- `framework/agents/reviews-inputs/gap-analysis-reviewer.md` — workflow Steps 1–12.

## Anti-patterns

- Flagging a topic as `Missing` when it's actually `Standard-rule`-resolvable. The §4 decision tree is ordered: Standard-rule lookup precedes the Missing default.
- Inflating Confidence (Likely → Confirmed) to upgrade MoSCoW bucket. Gap-count inflation is the canonical gap-analysis anti-pattern (BABOK §10.38). Gate 3 enforces Tier-A gating on Confirmed.
- Double-counting cause-and-effect as separate gaps. A single root cause spanning multiple topics is consolidated at Round 5 via `also_see` cross-references — both gap rows remain, but their relationship is visible.
- Solutioning the Candidate Requirement column. Architecture verbs (`build`, `implement with`, `use Kafka`) are forbidden — capability-category and behavioural vocabulary only. Gate 4 enforces.
- UI-layout vocabulary in the Candidate Requirement. *"display in a modal"*, *"show errors inline"*, *"render as a table"* are layout. Behavioural / capability vocabulary only.
- Inventing a dimension. The reviewer reads from `topics-requirements.md`'s `Dimension` column verbatim. Halt and surface the schema violation if the column is missing for any topic.
- Reading sibling reviewer artefacts. The reviewer never reads `review-inputs/COMPLETENESS-REVIEW/*`, `review-inputs/ADVERSARIAL/*`, `review-inputs/AMBIGUITY-REVIEW/*`.
- Writing `[AI-SUGGESTED]` markers in the artefact. That namespace belongs to the drafter.
- Performing additive merge across runs. Full-overwrite per run; the orchestrator's prior-artefact gate has already taken the consultant's decision.
- Using line numbers in Evidence. Citation is `[SRC: <filename>]` only.
- Using the `Agent` / `Task` tool. Sequential single-threaded by design.
