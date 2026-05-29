<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order. -->

# map-user-goal-analysis-from-inputs-to-ui.md

**Purpose:** Translate an inputs-side User Goal Analysis register (`analyse-inputs/USER-GOAL-ANALYSIS/user-goal-analysis.html`) into UI inventory signals for downstream design-spec consumption: end goals → primary-task weighting hints; soft goals → NFR / quality-attribute seeds; the goal-refinement hierarchy → information-architecture grouping hints; actor↔goal dependencies → role/permission seeds; surfaced conflicts → trade-off-aware design decisions.

**Inputs:** `analyse-inputs/USER-GOAL-ANALYSIS/user-goal-analysis.html` (specifically the embedded `<pre><code class="language-json" id="user-goal-analysis-body">` block — survives markitdown round-trip and is the load-bearing machine-readable contract carrying every goal's `cooper_type`, `hardness`, `provenance`, `inference`, `parent`/`refinement`, `actors`, and `criterion`).

**Outputs:** UI inventory rows + NFR seeds for the design spec.

**Used by:** a future `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when the inputs-side User Goal Analysis register is present. Combines with other `map-*-from-inputs-to-ui` skills via the accrue-all pattern. **Not invoked by `/analyse-inputs`** — registry metadata only, per the convention established by `framework/skills/map-task-analysis-from-inputs-to-ui.md`, `framework/skills/map-ooux-from-inputs-to-ui.md`, and siblings (graph 5: map-skills are registry metadata → no analyser edge).

> Content TBD per phase-2 build-order. The inputs-side variant reads the canonical goal model out of the embedded JSON block (rather than parsing rendered HTML), so it preserves the full audit trail of which source named which goal and which technique inferred each latent goal. Distinct from JTBD's `map-jtbd-from-inputs-to-ui.md` (which routes jobs/outcomes/forces): this skill routes *classified goals + hierarchy*, so end goals feed primary-task weighting, soft goals feed NFR seeds, and the AND/OR refinement feeds IA grouping. Inferred goals (`provenance: "inferred"`) are routed only after the consultant has confirmed them on a `/requirements` round-trip — an unconfirmed inferred goal is a candidate, not a design input.
