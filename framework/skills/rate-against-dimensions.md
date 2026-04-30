<!-- ROLE: skill. STATUS: stub — author during phase-1 build-order step 4. -->

# rate-against-dimensions.md

**Purpose:** Apply trade-off-dimension ratings (−2 … +2 per dimension) to a screen, view, or component using heuristics from `assets/trade-off-dimensions.md` and quality signals from `assets/taxonomy-goals.md`.

**Inputs:** the artifact being rated (screen / view / organism), `assets/trade-off-dimensions.md`, `assets/taxonomy-goals.md`, the screen's user goals + quality signals from `requirements.md`.

**Outputs:** rating per relevant dimension + rationale string for each.

**Used by:**
- `framework/agents/design-spec-drafter/agent.md` — populates per-screen trade-off rating tables.
- `framework/agents/design-qa/agent.md` — flags low-score alternatives.

**Used how:** Cascades Goal → Screen → View → Component with override at any level. Tier 1 dimensions always rated; Tier 2 when signalled; Tier 3 in specific situations.

> Content TBD per `plan/v7b-Brief.md > §trade-off-dimensions.md > Per-kind resolution`.
