<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order. -->

# map-business-context-definition-from-inputs-to-ui.md

**Purpose:** Translate an inputs-side Business Context Definition report (`analyse-inputs/BUSINESS-CONTEXT-DEFINITION/business-context-definition.html`) into design-spec signals for downstream consumption: Business Goals / Objectives → product-scope and success-metric anchors; the problem→need→goal causal chain → requirement-rationale traceability seeds; opportunity-driven needs → roadmap/phasing hints; the human-centered Problem Statement → primary design-challenge framing; surfaced tensions → trade-off-aware design decisions.

**Inputs:** `analyse-inputs/BUSINESS-CONTEXT-DEFINITION/business-context-definition.html` (specifically the embedded `<pre><code class="language-json" id="bcd-body">` block — survives markitdown round-trip and is the load-bearing machine-readable contract carrying every `business_problems`, `business_needs`, `business_goals`, `business_objectives`, `problem_statements`, `causal_links`, `tensions`, provenance, and `inference` field).

**Outputs:** design-scope anchors + success-metric seeds + requirement-rationale traceability rows for the design spec.

**Used by:** a future `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when the inputs-side Business Context Definition report is present. Combines with other `map-*-from-inputs-to-ui` skills via the accrue-all pattern. **Not invoked by `/analyse-inputs`** — registry metadata only, per the convention established by `framework/skills/map-user-goal-analysis-from-inputs-to-ui.md`, `framework/skills/map-task-analysis-from-inputs-to-ui.md`, `framework/skills/map-ooux-from-inputs-to-ui.md`, and siblings (graph 5: map-skills are registry metadata → no analyser edge).

> Content TBD per phase-2 build-order. The inputs-side variant reads the canonical business-context model out of the embedded JSON block (rather than parsing rendered HTML), so it preserves the full audit trail of which source named which motivation and which technique inferred each latent item. Distinct from `map-user-goal-analysis-from-inputs-to-ui.md` (which routes *actor* goals → primary-task weighting + NFR seeds): this skill routes *enterprise* motivation, so Goals/Objectives feed product-scope + success metrics, the causal chain feeds requirement rationale, and the Problem Statement feeds the headline design challenge. Inferred items (`provenance: "inferred"`) are routed only after the consultant has confirmed them on a `/requirements` round-trip — an unconfirmed inferred item is a candidate, not a design input.
