<!-- ROLE: asset (P2 analysis reference). Loaded by framework/agents/analyses/opportunity-solution-trees-analyser.md at activation. -->

# analyses/opportunity-solution-trees-reference.md

**Purpose:** Methodology reference for **Opportunity Solution Trees** (Teresa Torres, *Continuous Discovery Habits*, 2021; canonical exposition at `producttalk.org/opportunity-solution-trees/`). Torres designed OST for **forward discovery** — building a tree top-down from a desired Outcome through customer-interview-sourced Opportunities to candidate Solutions to Assumption Tests. The analyser does the **reverse**: it reads an already-merged `requirements/requirements.md` and ladders **upward** from features (Solutions) to needs (Opportunities) to goals (Outcomes), plus a best-effort fourth layer of Assumption Tests where the doc names risks or open questions. The reversal framing is the load-bearing methodological choice — it lets the analyser respect the framework-wide *extraction-not-authoring* discipline, and it makes the artefact a **structural audit** of the PRD rather than a fabricated discovery output.

**Used by:**

- `framework/agents/analyses/opportunity-solution-trees-analyser.md` — drives the agent's six-round process plus the quality-gate sweep.
- `framework/skills/map-opportunity-solution-trees-to-ui.md` — uses the tree structure to derive primary-opportunity weighting + per-screen Core Content Priority signals (downstream consumer; stub).

**Output produced by the analyser:** `analyses/OPPORTUNITY-SOLUTION-TREES/opportunity-solution-tree.html` — self-contained HTML tree using `framework/assets/analyses/template-opportunity-solution-trees.html` as scaffold.

---

## The reversal framing (read this first)

Torres's original OST is **forward**: a product team starts with a single business or product Outcome, runs customer interviews to surface unmet Opportunities, brainstorms candidate Solutions for the most promising Opportunities, then designs Assumption Tests to falsify the riskiest assumptions before building. The tree is built top-down; it produces a *plan for discovery*.

A merged `requirements/requirements.md` is the **output** of that process — its Solutions (features, user stories, acceptance criteria) have already been chosen, and the Opportunities behind them have been compressed into "so that …" tails of user stories, persona pains, and domain prose. To respect [[feedback_analyses_are_extraction_not_authoring]], the analyser cannot run interviews and cannot synthesise needs from thin air. It can only **surface** what the document's structure already exposes.

Therefore the analyser runs the tree **upward**:

1. Start with the doc's stated business/product **Outcome** (`§Success metrics` / `§Goals` / `§Business goals`).
2. Walk the doc's user-perspective material — `§Personas.Pains`, `§User stories` *"so that …"* tails, `§Pains`, `§Domain` problem statements — and surface every **Opportunity** they encode.
3. Walk the doc's product-perspective material — `§User stories` *"I want …"* heads, `§Acceptance criteria` headings, `§Features` — and surface every **Solution** the doc commits to.
4. Walk `§Risks`, `§Assumptions`, `§Open questions` — usually sparse or absent in a PRD — and surface every explicitly-named **Assumption Test**.
5. **Ladder** Solutions to Opportunities by actor + need/pain semantic match; ladder Opportunities to the single root Outcome by metric / goal keyword overlap.

What this gives the consultant is **not** a discovery plan — it is a structural audit of the PRD:

- Orphan Solutions (features the doc commits to but whose underlying customer need is not stated) signal *under-justified scope*.
- Unaddressed Opportunities (pains the doc names but does not commit a Solution against) signal *gaps in scope*.
- Vertical-only branches (one Opportunity with one Solution and no siblings) signal *premature commitment* (Torres warns that vertical-only branches collapse the discovery space).
- Disguised-Solution Opportunities (an "opportunity" that only one Solution could possibly address) signal *solutions-pretending-to-be-needs*.
- Missing Assumption Tests are usually expected for a written PRD; the absence is information, not a defect.

The output's job is to show all five signals at a glance.

---

## Upstream input contract

The analyser anchors on the canonical requirements sections:

- `§Success metrics` / `§Goals` / `§Business goals` — canonical source of the **root Outcome**. Torres-aligned classification: a *business outcome* is a financial / commercial metric (revenue, churn, market share); a *product outcome* measures customer behaviour or sentiment in the product; a *traction metric* measures adoption of a single feature. Torres recommends a product outcome at the root.
- `§Personas` and `§Personas.Pains` — canonical source of customer-perspective **Opportunity** material. Each pain is a candidate Opportunity; each persona supplies the actor.
- `§User stories` — dual source: the *"so that …"* tail is a candidate **Opportunity** (the customer's reason for wanting the feature), the *"I want …"* head is a candidate **Solution** (the feature itself).
- `§Acceptance criteria` headings — supplementary source of **Solutions** (each criterion describes a behaviour the product must exhibit).
- `§Pains` / `§1 Domain` (problem statements only) — supplementary source of **Opportunities** where `§Personas.Pains` and `§User stories` *"so that …"* tails are sparse. Use only the problem-statement clauses, not the value-proposition or product-description prose.
- `§Risks`, `§Assumptions`, `§Open questions` — canonical and only source of **Assumption Tests**. Absent in most PRDs; the analyser surfaces the absence rather than fabricating tests.
- `§Features in scope` / `§Scope inclusions` — supplementary source of **Solutions** for features that are committed but not story-mapped.

If `§Success metrics` / `§Goals` / `§Business goals` is absent or empty, the analyser **halts**. There is no fallback that fabricates a root Outcome from prose — a tree with no root is not a tree, and inventing one would silently invalidate every ladder above it.

If `§Personas.Pains` and `§User stories` *"so that …"* tails are both sparse, the analyser falls back to `§Pains` and `§1 Domain` problem statements, flagging every fallback Opportunity with the `from-domain-prose` provenance marker.

---

## The four layers (root → leaves)

### Layer 1 — Outcome

**Definition (Torres):** *"Business outcomes measure the health of the business and are typically financial metrics like grow revenue, increase market share, or reduce churn. Product outcomes typically measure a customer behaviour in the product or a customer sentiment about the product."* Torres recommends a **product outcome** at the top.

**Canonical form:**

> *"`<metric or goal>`, measured by `<measurement>`, by `<horizon if stated>`."*

**Source priority:**

1. `§Success metrics` — explicit KPI; strongest source.
2. `§Goals` / `§Business goals` — explicit goal statement.
3. (No fallback.) Absence → hard halt.

**Multiplicity rules:**

- **Exactly one** root Outcome per tree. If `§Success metrics` names multiple, the analyser surfaces a `AskUserQuestion` asking the consultant to pick the single primary outcome (or to re-run the analyser once per outcome). The tree is a single-root structure by Torres's design; multi-root collapses every laddering rule.
- The single Outcome carries a classification (`business-outcome` | `product-outcome` | `traction-metric`) per Torres's vocabulary, surfaced in diagnostics.

### Layer 2 — Opportunity

**Definition (Torres, verbatim):** *"An unmet customer need, pain point, or desire."* Framed **from the customer's perspective**, not the company's. **Validity test (Torres):** *"Is there more than one way to address this opportunity?"* If only one Solution could possibly address it, it is a Solution disguised as an Opportunity.

**Canonical form:**

> *"`<actor>` needs / cannot / wants `<need or pain>` when `<situation>`."*

(`when <situation>` is optional but recommended; many requirements pains carry an implicit trigger.)

**Source priority:**

1. `§Personas.Pains` — explicit pain per persona; strongest source.
2. `§User stories` *"so that …"* tail — the customer's reason for the feature.
3. `§Pains` (top-level) — explicit pain not tied to a persona.
4. `§1 Domain` problem statements — only problem-statement clauses, not value-proposition or product-description prose.

**Provenance markers (one per Opportunity, mandatory):**

| Marker | Meaning |
| --- | --- |
| `from-persona-pains` | Lifted from a `§Personas.Pains` entry. |
| `from-user-story-tail` | Lifted from a `§User stories` *"so that …"* tail. |
| `from-pains` | Lifted from a top-level `§Pains` entry. |
| `from-domain-prose` | Derived from `§1 Domain` problem-statement prose. Only used when the first three sources are sparse. |

**Filter rules:**

- **Reject solution-leaked Opportunities.** Forbidden tokens in the *need / pain* clause (case-insensitive substring match): `dashboard`, `screen`, `page`, `button`, `dialog`, `modal`, `dropdown`, `field`, `widget`, `report`, `export`, plus any verb of *building / adding*: `add`, `build`, `implement`, `create`, `provide`. These name UI affordances or product actions, not customer needs. Rewrite to the underlying need or reject.
- **Reject company-perspective Opportunities.** Forbidden tokens in the *need / pain* clause: `we`, `our`, `the business`, `the company`, `the team`. Opportunities are framed from the customer's perspective, period. Rewrite from the actor's perspective or reject.
- **Reject feeling-only Opportunities.** A clause that names *only* a feeling (`frustrated`, `confused`, `worried`, `annoyed`) without a need / pain / desire is unactionable. Sharpen to the underlying need (`feels frustrated when X` → `cannot Y when X`).
- **Merge near-duplicates.** Two Opportunities with the same actor and near-identical need are merged; prefer the more specific wording.

### Layer 3 — Solution

**Definition (Torres, verbatim):** *"A product, a feature, a service, a workflow, a process, documentation, or anything else that we offer to customers to help address a known opportunity."*

**Canonical form:**

> *"`<verb> <object>`" or "`<feature name>`" (verbatim from §User stories / §Acceptance criteria / §Features)*

**Source priority:**

1. `§User stories` *"I want …"* head — strongest source; explicit user-facing solution.
2. `§Acceptance criteria` headings — each criterion implies a Solution behaviour.
3. `§Features in scope` / `§Scope inclusions` — committed features not story-mapped.

**Provenance markers (one per Solution, mandatory):**

| Marker | Meaning |
| --- | --- |
| `from-user-story-head` | Lifted from a `§User stories` *"I want …"* head. |
| `from-acceptance-criteria` | Lifted from an `§Acceptance criteria` heading. |
| `from-features-in-scope` | Lifted from a `§Features in scope` row. |

### Layer 4 — Assumption Test (best-effort)

**Definition (Torres):** an experiment that falsifies a riskiest assumption *before* the team commits to building. Torres groups assumptions into five categories:

| Category | What it tests |
| --- | --- |
| `desirability` | Why do we think customers want this and will use it as expected? |
| `viability` | Why is this good for the business (commercial / strategic / legal)? |
| `feasibility` | Why do we think we can build it (technical reach)? |
| `usability` | Why do we think customers will be able to use it without help? |
| `ethical` | Is there potential harm — to customers, third parties, society — in building it? |

**Source priority (only — no fallback):**

1. `§Risks` — each risk is a candidate Assumption Test for the Solution(s) it concerns.
2. `§Assumptions` — each named assumption is a candidate test.
3. `§Open questions` — each open question is a candidate test.

**Provenance markers (one per Assumption Test, mandatory):**

| Marker | Meaning |
| --- | --- |
| `from-risks` | Lifted from a `§Risks` entry. |
| `from-assumptions` | Lifted from a `§Assumptions` entry. |
| `from-open-questions` | Lifted from a `§Open questions` entry. |

**Absent-layer handling:** when none of `§Risks` / `§Assumptions` / `§Open questions` is present, the entire Layer 4 renders as a single placeholder block with the literal marker `no-assumption-tests-in-requirements` and a one-line explanation that this is expected for a written PRD. Diagnostics record the absence. **The analyser never invents Assumption Tests.** This is the same discipline as `jtbd-analyser`'s `no-metric-in-requirements` marker.

---

## Laddering rules

The four layers compose the tree by **parent edges**, not by free-form association.

### Outcome ← Opportunity

Every Opportunity links upward to **the single root Outcome**. The link is asserted by keyword overlap between the Opportunity's *need / pain* clause and the Outcome's *measurement* clause (e.g. Outcome `reduce time to onboard a new customer` ↔ Opportunity `new customer cannot complete signup in one sitting`). When no keyword overlap exists, the Opportunity carries the `no-clear-outcome-link` flag and renders on the tree but is highlighted in diagnostics as `weakly-anchored`.

### Opportunity ← Solution

Every Solution links upward to **exactly one** parent Opportunity by actor + need/pain semantic match:

- The Solution's actor (from the user story's *"As a `<actor>`"* preface) must match the Opportunity's actor.
- The Solution's behaviour (the *"I want …"* head) must address the Opportunity's *need / pain* clause.

**Multi-parent Solutions are flagged but permitted.** A feature genuinely serving two distinct customer needs is real — but it usually signals an *over-loaded feature* worth surfacing. The tree renders the Solution under its primary parent and lists the secondary parents in the diagnostics block.

**Orphan Solutions** (no Opportunity in the doc maps to them) are **never** fabricated a parent. They land in the diagnostics block under `orphan-solutions` and on the tree under a sentinel parent `Opportunity: (none stated in requirements)` — surfacing the gap.

### Solution ← Assumption Test

Every Assumption Test links to **one or more** Solutions whose assumptions it tests. The link is asserted by:

- Explicit cross-reference in the `§Risks` / `§Assumptions` / `§Open questions` entry (e.g. *"Risk: integration with legacy CRM may be slower than 5 s — risks user story US-12"*).
- Semantic match on the Solution's behaviour or the affected `§Acceptance criteria` heading.

When the cross-reference is implicit and the analyser cannot identify the Solution(s) the test concerns, the test attaches at the **Outcome level** (a global / cross-cutting assumption) with the `global-assumption` flag.

---

## Quality gates (run after Round 4, before write)

Every gate is a hard gate. If any gate fails, the analyser does **not** write the artefact — it surfaces a structured error to the consultant and halts via the agent's Step 8 Revise / Override / Restart loop.

1. **Exactly one root Outcome.** If `§Success metrics` / `§Goals` named one and only one outcome (or the consultant chose one via the multi-outcome `AskUserQuestion`), the gate passes. If the analyser arrived at Round 4 with zero or multiple unresolved roots, the gate fails.
2. **Customer-perspective Opportunities.** Every Opportunity's *need / pain* clause is free of forbidden company-perspective tokens (`we`, `our`, `the business`, `the company`, `the team`). Flag offending Opportunities by id + offending text.
3. **More-than-one-way-to-address.** Every Opportunity has **either** (a) ≥2 candidate Solutions in scope linking to it, **or** (b) an explicit `unaddressed-in-requirements` flag (meaning the doc names the pain but commits no Solution to it). A 1:1 Opportunity-Solution pairing with no siblings signals a disguised Solution; flag for consultant review.
4. **No vertical-only branches.** A branch where the root has one Opportunity, the Opportunity has one Solution, and the Solution has no siblings is a vertical-only branch (Torres anti-pattern). Warn rather than fail; render the branch but flag in diagnostics.
5. **Every Solution ladders to root.** Every Solution has a traceable Outcome ← Opportunity ← Solution chain. Solutions with no Opportunity parent in the doc land under the sentinel `(none stated in requirements)` parent (not a failure — surfaces the gap).
6. **Provenance complete.** Every Outcome, Opportunity, Solution, and Assumption Test on the tree carries its mandatory provenance marker. No node is unmarked.
7. **No solution-leak in Opportunities.** No Opportunity *need / pain* clause contains UI-affordance tokens (`dashboard`, `screen`, `page`, `button`, `dialog`, `modal`, `dropdown`, `field`, `widget`, `report`, `export`) or building verbs (`add`, `build`, `implement`, `create`, `provide`). Flag offending Opportunities.

---

## Output presentation

The artefact renders as a top-to-bottom tree with four bands. Color contract:

| Element | Color | What it carries |
| --- | --- | --- |
| Outcome card (Layer 1) | indigo | The single root Outcome + classification badge (`business` / `product` / `traction`). |
| Opportunity card (Layer 2) | amber | Actor + need/pain clause + provenance dot. |
| Solution card (Layer 3) | blue | Feature / story / criterion + provenance dot. |
| Assumption-Test card (Layer 4) | violet | Test description + Torres category badge (`desirability` / `viability` / `feasibility` / `usability` / `ethical`). |
| Connectors | grey | Inline SVG `<path>` lines connecting parents to children. |
| Sentinel parent `(none stated in requirements)` | red-bordered | Renders Solutions whose Opportunity is not in the doc. Visually loud — the gap is the finding. |
| `unaddressed-in-requirements` flag | red-bordered | Renders Opportunities the doc names but commits no Solution against. |
| `not-named-in-requirements` placeholder | muted-italic | Used only when Layer 4 is entirely absent. |
| Diagnostics block | bottom of page | Per-gate result, counts, orphan-solution list, weakly-anchored Opportunity list, vertical-only branch list, multi-parent Solution list. |

A top-of-page `<details class="how-to-read">` panel (collapsed by default) explains the reversal framing in plain language for consultants new to OST.

---

## Anti-patterns

- **Inventing an Outcome from prose.** If `§Success metrics` / `§Goals` / `§Business goals` is empty, the analyser halts. A fabricated root invalidates every ladder above it. Mirror of `user-journeys-analyser`'s no-invented-personas rule.
- **Inventing Opportunities from the analyser's own intuition.** Opportunities live in `§Personas.Pains` / `§User stories` tails / `§Pains` / `§1 Domain`. If the analyser cannot anchor a candidate Opportunity to one of those, it is not on the tree. The tree's value comes from anchoring; thinning the anchor breaks the audit.
- **Inventing Assumption Tests.** Layer 4 comes from `§Risks` / `§Assumptions` / `§Open questions` only. Absence is the answer when those sections are missing. The `no-assumption-tests-in-requirements` placeholder is honest; a guess at "things the team should test" is invented data.
- **Solutions disguised as Opportunities.** Gate 7 (UI-affordance keyword reject) plus Gate 3 (more-than-one-way-to-address) catch the obvious cases. The non-obvious case — an Opportunity that is technically customer-framed but maps 1:1 to a single Solution — is flagged for consultant review, not silently passed.
- **Fabricating parents for orphan Solutions.** A Solution with no Opportunity in the doc lands under `(none stated in requirements)`. The analyser **never** invents an Opportunity to make the tree "complete" — the gap is the finding.
- **Forward-discovery framing in the artefact's prose.** The Unicorn does not narrate the tree as if the team is about to run interviews. The artefact is a structural audit of an existing PRD; its purpose is to surface gaps, not to plan discovery.
- **Multi-root trees.** The tree has exactly one root Outcome. If `§Success metrics` names two, the analyser asks the consultant to pick one or to re-run; it does not render two roots.
- **Collapsing rounds.** Round 1 (Outcome) → Round 2 (Opportunities) → Round 3 (Solutions) → Round 4 (Assumption Tests, best-effort) → Round 5 (Laddering) → Round 6 (Quality gates). Each round's output is the next round's input; collapsing rounds hides reasoning and breaks the gate sweep.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/opportunity-solution-trees-analysis.md` — literal, structural, reversal-aware. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.
