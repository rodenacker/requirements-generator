<!-- ROLE: skill. STATUS: stub — populate during phase-2 build-order step when an OST-aware design-spec consumer ships. -->

# map-opportunity-solution-trees-to-ui.md

**Purpose:** Translate Opportunity Solution Tree structure into screen-prioritisation hints + per-screen Core Content Priority signals. The single root Outcome anchors the product's primary outcome KPI on the dashboard surface; unaddressed Opportunities (Opportunities with no Solution children in the tree) are *gap-screen candidates* — surfaces the design phase should weigh against scope cuts; multi-Solution Opportunities (Opportunities with ≥2 Solution children) drive *cluster-screen* candidates where the cluster of features ladders to one user need; orphan Solutions (Solutions under the sentinel `(none stated in requirements)` parent) flag scope items the design phase should re-verify with the consultant before committing screens for them.

**Inputs:** `analyse-requirements/OPPORTUNITY-SOLUTION-TREES/opportunity-solution-tree.html`, `framework/assets/taxonomy-screens.md`.

**Outputs:** screen-prioritisation hints (which Solutions become "core" vs "supporting" screens, anchored to their Opportunity parent's weight) + per-screen CCP signals (Solutions whose Opportunity is high-priority in the tree get higher Core Content Priority on the screens that surface them) for the design-spec drafter.

**Used by:** future `framework/agents/design-spec-drafter/agent.md` (or equivalent downstream design consumer) — invoked when an OST analysis is present alongside (or instead of) a JTBD analysis. Not invoked by `/analyse-requirement`.

**Used how:** The downstream consumer cross-references the tree's ladder structure with the screen taxonomy. The tree's flags (orphan-solution, unaddressed-in-requirements, weakly-anchored, vertical-only-branch, multi-parent-solution) become design-phase signals: orphans flag screens that need consultant re-verification; unaddressed Opportunities flag missing screens; multi-parent Solutions flag screens that may be over-loaded.

**Relationship to `map-jtbd-to-ui.md`:** OST and JTBD are complementary lenses. JTBD's `(importance, satisfaction) → opportunity` scoring drives per-job CCP weight; OST's ladder structure drives per-screen *justification* (why a screen exists — which Opportunity it serves — which Outcome that Opportunity ladders to). When both are present the design phase reconciles weights by taking JTBD's opportunity score as the primary signal and OST's laddering as the structural anchor.

> Content TBD per phase-2 build order; this stub exists because every registry row carries a `map_skill` path. The `/analyse-requirement` pipeline does not invoke this skill — downstream design-spec consumers do, once they exist.
