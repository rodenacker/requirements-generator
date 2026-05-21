<!-- ROLE: skill. STATUS: stub — author during phase-2 build-order. -->

# map-ooux-from-inputs-to-ui.md

**Purpose:** Translate an inputs-side OOUX object map (`analyse-inputs/OOUX/ooux-object-map.html`) into UI inventory entries: objects → screen-taxonomy elements + modifiers; CTAs → behaviour entries on appropriate atoms/molecules; relationships → navigation links between screens.

**Sibling:** `framework/skills/map-ooux-to-ui.md` — the requirements-side OOUX map-skill. Both are phase-2 stubs; either may be the canonical implementation when authored (the inputs-side variant has the advantage of richer provenance via filename citations and synonym-merge metadata; the requirements-side variant has the advantage of canonicalised §2.1 names).

**Inputs:** `analyse-inputs/OOUX/ooux-object-map.html` (specifically the embedded `<pre><code class="language-json" id="ooux-object-map-body">` block — survives markitdown round-trip and is the load-bearing machine-readable contract), `assets/taxonomy-screens.md`.

**Outputs:** UI inventory rows for the design spec.

**Used by:** `framework/agents/design-spec-drafter/agent.md`.

**Used how:** Called when the inputs-side OOUX analysis is present. Combines with other `map-*-from-inputs-to-ui` skills via the accrue-all pattern. Not invoked by `/analyse-inputs` — registry metadata only, per the convention established by `framework/skills/map-task-analysis-from-inputs-to-ui.md` and siblings.

> Content TBD per phase-2 build-order. The inputs-side variant differs from the requirements-side stub by reading the canonical-name + synonym-merged-from + provenance fields out of the embedded JSON block (rather than parsing the rendered HTML), so it preserves the full audit trail of which source named which object verbatim.
