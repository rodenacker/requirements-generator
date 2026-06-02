<!-- ROLE: skill. STATUS: stub — author when downstream prioritisation-aware design consumption is built. -->

# map-mvp-slicing-to-ui.md

**Purpose:** Translate an MVP-slicing artefact (`analyse-requirements/MVP-SLICING/mvp-slicing.html`) into prioritisation signals for downstream design: the proposed MVP set (the `Must` cards) → a default in-scope feature set; the backbone activities → screen-sequencing hints; the release bands → a phased build order.

**Inputs:** `analyse-requirements/MVP-SLICING/mvp-slicing.html` (and its embedded `<script type="application/json" id="mvp-slice">` machine dump), `assets/taxonomy-screens.md`.

**Outputs:** Prioritisation signals for the design spec — a default MVP feature set and a release-phase ordering.

**Used by:** `framework/agents/design-spec-drafter/agent.md` (future); and, when scope-selector MVP-scope wiring is built, as the bridge that turns the `Must` set into a default `scope.json` filter.

**Used how:** Called when the MVP-slicing analysis is present. Combines with other map-*-to-ui skills via the accrue-all pattern.

> Content TBD. Today the MVP-slicing methodology is `upstream-only` per `framework/skills/select-supporting-analyses.md > Static method → architect_roles mapping` — the blueprint-architect records but does not consume it. This stub becomes load-bearing when the deferred scope-selector MVP-scope wiring is built (flip the `architect_roles` row to `feature-presence` and populate the `feature-presence` sidecar payload from the Must/Should/Could/Won't buckets the analyser already computes).
