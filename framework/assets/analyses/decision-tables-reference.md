<!-- ROLE: asset (analysis reference). Methodology definition for the decision-tables analyser. Industry framing: OMG Decision Model and Notation (DMN) decision tables + hit policies; BABOK v3 #9 Business Rules Analysis + #17 Decision Modelling; Barbara von Halle, Business Rules Applied (2001); Vanthienen et al., Semantics and Analysis of DMN Decision Tables (arXiv 1603.07466). The lens extracts every conditional business rule scattered through the requirements prose, re-casts it into a DMN decision table (condition columns -> conclusion, with an explicit hit policy), and runs the two analyses decision-table theory makes mechanical: completeness (is every reachable combination of condition values assigned an outcome?) and consistency (do any two rules conflict?). It surfaces the unhandled combination and the contradictory rule a linear prose reader misses. -->

# Decision Tables / Business-Rules Catalogue (DMN) analysis reference

> **Method:** Find every **decision** in `requirements/requirements.md` — a point where the system reads some condition values and reaches a conclusion (a field becomes required, an action is enabled, a request is routed, an applicant qualifies) — and re-cast each as a **DMN decision table**: condition columns, a conclusion column, one rule per row, and an explicit **hit policy**. Then run the two analyses the tabular form makes mechanical: **completeness** (every reachable combination of the conditions' enumerable values is assigned an outcome) and **consistency** (no two rules assign conflicting outcomes to an overlapping input region). The tables become the form-validation, conditional-visibility, and action-enablement spec the screens enforce; the gaps and conflicts become resolver questions before wireframing.

**Output file:** `analyse-requirements/DECISION-TABLES/decision-tables.html` — a self-contained HTML artefact (no external CSS/JS, no `<script>`, no CDN, no Mermaid runtime; opens via `file://`). **Diagrams-first** section order: Overview → TOC → Diagrams (decision-health strip + Decision Requirements Diagram) → Tables (decision tables + completeness register + consistency register + business-rules catalogue) → Diagnostics.

**Re-ingestion:** the artefact embeds a `<pre><code class="language-json" id="decision-tables-body">` model that survives the markitdown HTML→MD round-trip as a fenced ```json block. A consultant may re-drop the HTML into `input/`; `/requirements` then ingests the structured rule model, and every completeness gap marked `[AI-SUGGESTED: AI-NNN | blocking]` reaches the resolver as a mandatory confirmation. This is the load-bearing downstream contract — distinct from the sidecar (below).

**Sidecar:** `analyse-requirements/DECISION-TABLES/decision-tables.sidecar.json` — per `framework/assets/analyses/sidecar-schema.md`. Exposes the **`upstream-only`** role (the blueprint-architect does not consume decision-table rules at MVP; the analysis is a requirements-improvement aid like `five-whys` and `mvp-slicing`). Emitting it keeps `sidecar_present == true` so selecting this lens in `/wireframe` never trips the `RF-09` legacy-prose fallback.

**Analyser agent:** `framework/agents/analyses/decision-tables-analyser.md`

**Character:** `framework/assets/characters/decision-tables-analysis.md`

---

## Industry framing — DMN decision tables

The decision table is older than software (Pollack, 1963; the lineage runs through structured analysis and CASE tooling), but its modern, analysable form is the OMG **Decision Model and Notation (DMN)** standard: a decision is a function from inputs to an output, expressed as a table whose rows are rules and whose **hit policy** declares how overlapping rules resolve. Two adjacent lineages converge here:

- **BABOK v3 #9 Business Rules Analysis** + **#17 Decision Modelling** — the BA practice of pulling operative rules out of policy prose and modelling the decisions they feed.
- **Barbara von Halle, *Business Rules Applied* (2001)** + the Business Rules Group "Business Rules Manifesto" — rules as a first-class, separately-managed asset, not buried in procedure.

The analytical pay-off (Vanthienen et al., *Semantics and Analysis of DMN Decision Tables*, arXiv 1603.07466): once the logic is tabular and the condition value-spaces are enumerable, **completeness** and **consistency** are mechanical checks over the cartesian product — the unhandled combination and the contradictory pair fall out of the structure rather than depending on a careful reader.

This is a **transformation** lens (it builds a derived rule model from the spec's own conditional prose), not a free-text critique. It never invents a decision, a condition value, or — above all — a missing outcome.

---

## The structured object — one decision table per decision

| Part | Meaning |
|---|---|
| **Decision** | A named point where the system reaches a conclusion from condition values. One table per decision. |
| **Inputs / conditions** | The variables the decision reads (e.g. `status`, `role`, `amount band`, a boolean flag). Each has a **value domain** drawn from the spec. |
| **Rules** | Rows. Each rule is a combination of condition entries (one per condition, or `-` for don't-care) → one conclusion. |
| **Hit policy** | How overlapping rules resolve (and whether overlap is even legal). One per table. See the catalogue below. |
| **Conclusion** | The outcome: a field/action state (`required` / `optional` / `enabled` / `disabled` / `visible` / `hidden`), a derived value, a routing target, or an eligibility verdict. |

Each rule carries a stable **rule ID** (`<decision-slug>-R<n>`), its **source** (`F-NN` / `UI-NN` / `§6.5` / `§5 <flow>` / `§7`), and a **derivation marker** (cited vs inferred).

---

## Hit-policy catalogue (single-hit only at MVP)

| Code | Name | Meaning | When to use |
|---|---|---|---|
| `U` | **Unique** | At most one rule may match any input; overlap is illegal. | **Default.** The cleanest policy and the one that makes completeness + consistency fully mechanical. Prefer it unless the spec states otherwise. |
| `A` | **Any** | Rules may overlap, but all overlapping rules must give the **same** conclusion. | When the spec lists redundant-but-agreeing rules. |
| `P` | **Priority** | Overlap allowed; the highest-priority matching rule wins (priority by declared output order). | When the spec states precedence between outcomes. |
| `F` | **First** | Overlap allowed; the first matching rule by row order wins. | When the spec states an explicit ordered "first match" evaluation. |

Multiple-hit / aggregation policies (`C` Collect, `C+`/`C<`/`C>`/`C#`, `R` Rule order, `O` Output order) are **out of MVP scope** — a decision that needs them is flagged for the consultant rather than modelled. The hit policy is **declared, never inferred silently**: if the spec doesn't state precedence, the table is `U` and any overlap is a consistency defect (not a silent `F`).

---

## Where decisions hide in a requirements document (extraction scan)

The analyser scans these sections for conditional language — *"when / if / unless / only … then …"*, *"is required when"*, *"is enabled for"*, *"is visible only if"*, *"qualifies if"*, *"otherwise"*, *"depending on"* — and lifts each into a candidate decision:

| Source | Decision kind |
|---|---|
| `§6.1 Functional` (F-NN) | validation rules, conditional requiredness, action enablement, derivation |
| `§6.4 UI feature needs` (UI-NN) | conditional visibility, enable/disable of controls |
| `§6.5 Access control (RBAC)` | role-conditioned access conclusions (who may do what, under which condition) |
| `§5 Task flows` | decision points / branch conditions within a flow |
| `§7 Data shapes` + `§7.X Derivations` | field-level constraints, computed/derived values |

A decision named in prose but whose conditions or outcomes are absent is still surfaced — with the missing part flagged (below), never guessed.

---

## Condition typing (decidability of completeness depends on this)

Completeness is only decidable over **enumerable** condition value-spaces. Each condition is typed:

| Type | Signal | Completeness treatment |
|---|---|---|
| **enumerable** | a status set (`§2.3`/`§9`), a role set (`§6.5`), a boolean flag, a named category | fully checkable over the cartesian product of its values |
| **named-band** | the spec states the thresholds/bands (e.g. *"< £1,000"* / *"≥ £1,000"*) | checkable against the **stated** bands only |
| **un-banded numeric / free-text** | a numeric or open-text condition with **no** thresholds stated in the spec | **out-of-scope-for-completeness** — flagged `needs-a-threshold`; **never** partition it or invent a boundary |

The single most important anti-fabrication rule lives here: an un-banded numeric is **not** silently split into bands to make a table look complete. It is flagged as a question for the consultant.

---

## The analyses

### Completeness (mechanical over enumerable domains)

For each decision, form the cartesian product of every enumerable / named-band condition's value domain. Every combination matched by **no** rule (after accounting for `-` don't-care entries and any explicit `otherwise` rule) is a **completeness gap**. Each genuine gap becomes a register row and a resolver question — *"What happens when `status = Rejected` and `role = Owner`?"* — marked:

- `[AI-SUGGESTED: AI-NNN | blocking]` when the missing combination is reachable and consequential (it blocks a stated `§4` goal / `§5` flow, or governs a destructive/irreversible action) — these reach the `/requirements` resolver as mandatory confirmations on re-ingestion;
- `[AI-SUGGESTED: AI-NNN | non-blocking]` for low-consequence gaps, and for any gap that exists only because a condition is un-bandable (the gap is "the band is undefined", not "the outcome is undefined").

A decision whose conditions are **all** un-bandable cannot have its completeness computed; say so explicitly rather than report "complete".

### Consistency (overlap + hit-policy violation)

Two rules **overlap** when their input regions intersect (a `-` don't-care widens a rule's region). For each overlapping pair:

- under `U`: any overlap is a **hit-policy violation** (two rules match the same input) — a defect, listed in the consistency register;
- under `A`: an overlap with **different** conclusions is a **conflict**; an overlap with the same conclusion is fine;
- under `P`/`F`: an overlap is legal (precedence resolves it) — but record it so the consultant can confirm the precedence is intended.

A **conflict** is always: two rules whose regions intersect and whose conclusions differ, under a policy that forbids it. Conflicts are cited to both source requirements (the contradiction is usually two requirements authored apart).

### Redundancy / subsumption (optional third register, low cost)

A rule is **subsumed** when its input region is a subset of another rule's region **and** they share the same conclusion — the subsumed rule is dead (it never decides anything the other doesn't). Two rules are **mergeable** when they differ in exactly one condition's value and share a conclusion (table contraction). These are advisory tidiness findings, never blocking.

---

## Anti-fabrication discipline (load-bearing)

- **A missing outcome is a question, never a guess.** A completeness gap is an `[AI-SUGGESTED]` resolver question; the conclusion cell is left empty/flagged, never filled with a plausible outcome.
- **A deterministic default is a standard rule, not an inference.** Where a house rule supplies the outcome, mark it `[STANDARD-RULE: GR-NN]` (e.g. `GR-04` for the confirmation gate on an irreversible action; `GR-05` for validation timing). The resolver skips these.
- **Every rule is cited.** A stated rule cites its source ID; an inferred rule carries its derivation marker **and** ≥ 1 source anchor — anchorless inference is forbidden.
- **Conditions are reduced to the spec's enumerable bands.** Never invent a numeric threshold or a category value the spec does not name.
- **Never invent a decision.** A decision must trace to conditional prose in the scanned sections; absent that, it is not added.

---

## Rule-explosion control (the #1 readability risk)

A table nobody can read is a failure even when complete. The reference enforces:

- **One table per decision.** Never one giant table. Scope each table to the conditions that actually affect **its** conclusion.
- **Collapse irrelevant conditions** with a `-` don't-care entry; do not include a condition that does not change the outcome.
- **Prefer an explicit `otherwise` / default row** where the spec states a catch-all, rather than enumerating the residual combinations.
- **Size cap.** A decision whose enumerable rule-space exceeds **64 combinations** (or whose conditions exceed **6**) is **decomposed into sub-decisions** (a sub-decision's conclusion becomes an input to the parent — the DRD dependency edge) or, if it cannot be cleanly decomposed, **flagged** in diagnostics as `oversized — completeness not enumerated` rather than rendered as a combinatorial wall.

---

## Lane boundary with STATE-DIAGRAM (analytic — no required cross-read)

Some conditional rules are really **entity status-transition guards**, which the STATE-DIAGRAM analysis owns (`framework/assets/analyses/state-diagram-reference.md` — the `guard` column on its transitions table). Draw the lane by **outcome**:

- If a rule's **conclusion is a status transition** (it moves an entity from one lifecycle state to another) → it belongs to STATE-DIAGRAM. **Exclude it**, and note `see STATE-DIAGRAM` in diagnostics.
- If a rule governs **validation / conditional requiredness / visibility / enablement / derivation / eligibility / routing** (the conclusion is a field or action state, a value, or a route — not a state change) → it belongs **here**.

The analyser MAY `Glob`+`Read` `analyse-requirements/STATE-DIAGRAM/state-diagram.html` if it exists, purely as a convenience seed to recognise which conditions are transition guards — exactly as `crud-coverage` optionally reads OOUX/DATA-MODEL. It is **never required**, never a dependency, and the lane rule is applied analytically whether or not the STATE-DIAGRAM artefact is present.

---

## Output structure

### 0. In plain terms (first rendered section)

`{{PLAIN_SUMMARY}}` — a 2–5 sentence plain-English lead placed above the overview meta-grid, per `framework/shared/output-readability.md`. It states what this decision-tables analysis is, what it found (summary of decisions, gaps, conflicts), and what the consultant should do with it (review blocking gaps, surface to `/requirements` resolver). It is a faithful condensation of the content below — it introduces no fact, count, or citation not already present, and carries no `[SRC: C-NNN]` of its own. Methodology jargon (decision table, condition, conclusion/action, rule, hit policy, completeness, gap, consistency, conflict) is glossed at first use; client domain terms are not glossed. Rendered as `<section id="plain-terms">`.

### Diagrams (top of document)

1. **Decision-health strip** — the value, front-loaded. One card per decision: rule count · completeness (`complete` / *n* gaps) · consistency (`consistent` / *n* conflicts) · hit policy. The reader sees the gaps and conflicts before the tables.
2. **Decision Requirements Diagram (DRD)** — the canonical DMN diagram, pre-rendered as inline `<svg>` (geometry baked at render time; no `<script>`). Decision nodes (rectangles) + Input-Data nodes (stadium/oval) + information-requirement edges (a sub-decision's conclusion feeding a parent decision; an input-data node feeding a decision). Edge provenance classes mirror five-whys (`prov-from-requirements` / `prov-from-section` / `prov-derived` / `prov-ai-suggested`). A collapsed `<details class="mermaid-source">` carries a `flowchart TD` export so the consultant can regenerate/edit the DRD. When there are no inter-decision dependencies, the DRD is a flat set of decision nodes with their input-data — still useful as an inventory.

### Tables (below the diagrams)

3. **Decision tables** — the centrepiece. One table per decision: condition columns, the conclusion column, one row per rule, a **hit-policy badge**, `-` don't-care cells, and an `otherwise` row where present. Each rule row shows its rule ID + source. Gap and conflict cells are glyph + word, never colour-only.
4. **Completeness register** — one row per gap: `{decision, missing-combination, classification, marker, resolver-question}`. Blocking rows carry `[AI-SUGGESTED]` + `.provenance-ai-suggested`.
5. **Consistency register** — one row per conflict / hit-policy violation: `{decision, rule-pair, overlap-region, conflicting-conclusions, both-source-citations}`.
6. **Business-rules catalogue** — every rule, flat, with rule ID, the decision it belongs to, its source, and cited-vs-inferred provenance — the "show your work" backing the tables.

### Diagnostics (bottom, collapsed)

7. Counts summary, the hard-check result lines (PASS/FAIL), the size-cap notes, the excluded-transition-guards note (lane boundary), and the embedded `<pre><code class="language-json" id="decision-tables-body">` model carrying `{ decisions[], inputs[], rules[], hit_policy, completeness_gaps[], conflicts[] }` for `/requirements` re-ingestion.

### Downstream-use footer (collapsed, after diagnostics)

8. `<details class="downstream-toggle">` — re-ingestion mechanics (how to copy the HTML into `input/`, what the markitdown round-trip preserves, how blocking gaps reach the `/requirements` resolver). Collapsed by default; machinery prose moved here so it does not interrupt the reader. The JSON/`<pre><code>` block remains in the non-collapsed `#body` section (markitdown-survival contract — cannot be collapsed).

---

## Quality checks (hard gates + soft)

All checks operate on the rule model; the model must be valid regardless of whether the DRD shows dependencies.

1. **Every decision has a kebab-case id, a display name, a hit policy, and ≥ 1 condition**, each traceable to a scanned section.
2. **Every rule has a stable id, ≥ 1 source citation OR a derivation marker + ≥ 1 anchor, and exactly one conclusion** (or an explicit flagged-empty conclusion for a gap row surfaced in-table). No uncited, anchorless, or two-conclusion rule.
3. **No completeness gap is filled with a fabricated outcome** — every gap is an `[AI-SUGGESTED]` register row; no conclusion cell is invented.
4. **Every condition is typed** (`enumerable` / `named-band` / `un-banded`); un-banded conditions are flagged, never silently partitioned; no invented threshold or category value.
5. **Consistency completeness:** under `U`/`A`, every overlapping-conflicting rule pair appears in the consistency register — none silently dropped.
6. **Lane boundary:** no rule whose conclusion is a status transition appears in any table (those are excluded with a `see STATE-DIAGRAM` note).
7. **Size cap respected:** no rendered table exceeds the 64-combination / 6-condition cap without being decomposed or flagged `oversized`.

**Soft check (warning, not gate): gap density.** `density = blocking_gaps / total_enumerable_combinations`. If `density > 40%`, emit a `density-warning`: *"Conditional coverage is thin — most reachable combinations have no stated rule. This usually means `§6.1`/`§6.4` under-specify the logic, not that the analysis is wrong."* Does not block writing.

On any hard-check failure (1–7): do **not** write the artefact; surface the failing checks + flagged items via `AskUserQuestion` with Revise / Override / Restart, per the analyser's Step 7 contract.

---

## Five-round discipline

Each round produces a distinct in-memory output. The analyser does not write until Round 5 completes and all hard checks pass (or the consultant chose Override).

- **Round 1 — Decision discovery.** Scan `§6.1`/`§6.4`/`§6.5`/`§5`/`§7` for conditional language; list candidate decisions, each with its source IDs. Apply the lane rule — drop decisions whose outcome is a status transition (note → STATE-DIAGRAM). Optionally seed-read the STATE-DIAGRAM artefact if present.
- **Round 2 — Condition modelling.** Per decision, name its input conditions; type each (`enumerable` / `named-band` / `un-banded`); pull each condition's value domain from the spec; flag un-bandable conditions.
- **Round 3 — Rule extraction.** Per decision, extract the stated rules (condition combo → conclusion); assign rule IDs, source citations, derivation markers; pick the hit policy (default `U`).
- **Round 4 — Completeness + consistency analysis.** Enumerate the cartesian product over enumerable/named-band domains; compute gaps, conflicts, hit-policy violations, and (optionally) redundancy/subsumption. Apply the size cap — decompose or flag oversized decisions.
- **Round 5 — Registers + validate.** Build the completeness register (blocking/non-blocking per the rule above), the consistency register, the business-rules catalogue. Run the 7 hard checks + the soft density check. Compute the (minimal) `upstream-only` sidecar payload.

If a later round invalidates an earlier one (Round 3 reveals a condition Round 2 missed), loop back and revise — do not paper over it.

---

## Sidecar projection (downstream context-cost optimisation)

Per `framework/assets/analyses/sidecar-schema.md`, the analyser writes `analyse-requirements/DECISION-TABLES/decision-tables.sidecar.json` exposing exactly the **`upstream-only`** role (per `framework/skills/select-supporting-analyses.md > Static method → architect_roles mapping`):

```json
{ "architect_projection": { "upstream-only": { "notes": "Decision-tables is a requirements-improvement aid; the blueprint-architect does not consume the rule model at MVP. Re-ingestion into /requirements is via the embedded JSON body block, not this sidecar." } } }
```

Full envelope: `schema_version "1"`, `method "decision-tables"`, `source_path`, `source_sha256` of the HTML at write time, `generated_at`, `truncated false`. Hard cap ≤ 20 KB (trivially met). **Do not invent role keys** — a dedicated `interaction-logic` / `form-behaviour-guards` role (so the architect consumes conditional-field rules directly) is a deliberate future enhancement requiring a coordinated change across `select-supporting-analyses.md`, `sidecar-schema.md`, and the architect's step files; it is **out of scope** here.

---

## Downstream consumption (handled by `framework/skills/map-decision-tables-to-ui.md`)

- Each **condition** → a form-validation guard / a conditional-visibility toggle / an action-enablement rule on the owning surface.
- Each **conclusion** → a field state (`required`/`optional`/`hidden`) or surface state the screen must realise.
- Each **completeness gap** → a flagged design unknown (not a surface) to settle before building.

`map-decision-tables-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character and future design-spec authors. No widening: every guard/state traces to a rule that traces to a `§6.1`/`§6.4`/`§6.5`/`§5`/`§7` source.

---

## Stop-condition

The analysis is complete when every decision has a table with a declared hit policy and ≥ 1 typed condition; every rule cites a source or carries a derivation marker + anchor; every completeness gap is an `[AI-SUGGESTED]` register row (blocking where consequential) with no fabricated outcome; every conflict appears in the consistency register; no status-transition rule was tabulated; the size cap holds; all 7 hard checks pass (or Override); and the consultant chose Accept in the handback loop.

---

## Voice and readability

The rendered artefact is read by a human (the consultant, sometimes a client stakeholder) **and** consumed downstream by `/wireframe`'s `blueprint-architect` (optionally, via the per-analysis machine-readable sidecar). The operative standard is `framework/shared/output-readability.md` — restated in the character's *Reader & plain language* block so the analyser never needs to load `framework/shared/` at runtime.

**What this means for the output:**

- **Lead first.** The `{{PLAIN_SUMMARY}}` "In plain terms" section (`<section id="plain-terms">`) is the first rendered section, before the overview meta-grid. It states in 2–5 plain sentences what the analysis is, what it found, and what the consultant should do with it.
- **Gloss methodology jargon at first use.** In the lead and any handback prose: "decision table (a grid of conditions → actions)", "condition (an input variable the table reads)", "action/conclusion (the outcome a rule assigns)", "rule (one row of the table)", "hit policy (how overlapping rules resolve)", "completeness (every reachable condition-value combination has an assigned outcome)", "gap (a reachable combination with no stated rule)", "consistency (no two rules conflict)", "conflict (two overlapping rules with differing conclusions)". Client domain terms are **never** glossed here — that is the GLOSSARY methodology's job.
- **Plain layer confined.** The lead and glosses are the only plain-English additions. The decision tables, registers, JSON block, and diagnostics keep their existing concrete, telegraphic discipline unchanged.
- **Keep every `[SRC: C-NNN]`.** Never demote or drop source citations. They reassure the reader and feed the downstream sidecar.
- **Machinery prose collapsed.** Re-ingestion instructions (how to copy into `input/`, what markitdown preserves, how blocking gaps reach the resolver) live in the `<details class="downstream-toggle">` footer. The `<pre><code class="language-json" id="decision-tables-body">` block stays in the non-collapsed `#body` section (required for round-trip survival).
