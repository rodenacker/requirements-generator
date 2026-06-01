# Framework Dependency Graphs

Nine transitive load/read/invoke trees, one per orchestrator. Source of truth for "what loads what". LLM-only doc (not loaded at runtime) — diagrams dropped in favour of filename-keyed adjacency lists.

## Notation

- `A → B, C` — A loads/reads/invokes B and C. The arrow target is the **filename** (node identity); dir prefixes shown only where they disambiguate (`characters/`, `steps/`, `reviews/`, …).
- `A ⇒ @macro` — A expands a shared subtree defined in *Shared conventions*.
- `[cond: …]` — conditional/runtime-predicated edge (was a dashed Mermaid edge).
- `[parallel …]` — dispatched as a parallel sub-agent (was a dashed-border node), not a foreground invocation.
- `(char)`/`(tmpl)` — optional type hint when the filename alone is ambiguous.
- Stats `N nodes / M edges / depth D` describe the original graph topology (unchanged; same edges, terser notation).

## Shared conventions (apply to every graph unless a per-graph note overrides)

- **No cycles** in any subtree.
- **Pipeline output artefacts are produced, not loaded** → never drawn as edges (e.g. `requirements/requirements.md`, `prd/prd.md`, manifests, draft sidecars). A pipeline's own read target (e.g. analysers/reviewers reading `requirements/requirements.md`) is implicit, not drawn.
- **No `pattern-catalogue/` "see also" pointers** drawn — except graph 8, where `pattern-catalogue/_index.md` is a real direct read.
- **Write isolation.** Each pipeline writes only its own output dir. Two documented cross-pipeline write exceptions, both inherited from shared agents: `input-handler.md` writes `requirements/source-manifest.json` + `input/*.converted.md` (create/refresh modes only); `blueprint-architect.md` writes `blueprints/<slug>/{scope.json, blueprint.md}`. Orchestrator step-0b preflight has read-only access to `requirements/`, `requirements/source-manifest.json`, `state/.progress.json`.
- **check-context-bloat.md** → `refusal-registry.md`, `state/.progress.json` (existence/byte check only; callers never write `.progress.json`). `artefact_dir` = `input/` for the two `*-inputs` pipelines, else `requirements/`.
- **verify-artifact-write.md** → `refusal-registry.md`, called from every agent's write step. Shared across all orchestrators (one file on disk).
- **Registry-driven orchs (graphs 3, 4, 5, 6).** `<selector> → registry.md` is the discovery edge; `orch → agent_*` edges are runtime invocation paths. Adding an MVP method = new registry row + asset fan-out + one `orch → agent` edge; **zero orchestrator edits**.

### `@input-handler-subtree` (graphs 1, 5, 6, 7 — one set of files on disk)

```
input-handler.md → check-manifest-freshness.md, classify-input-tier.md, preflight-mcp.md,
                   convert-input-file.md, build-source-manifest.md, verify-artifact-write.md,
                   refusal-registry.md, setup-instructions/markitdown.md
  classify-input-tier → convert-input-file
  preflight-mcp       → refusal-registry
  convert-input-file  → verify-artifact-write, refusal-registry
  build-source-manifest → verify-artifact-write
  verify-artifact-write → refusal-registry
```

Per-caller `progress_path`: requirements = `.progress.json`; generate-prd = `.prd-progress.json`; analyse-inputs / review-inputs = `null` (suppresses the agent's `RF-01 continue-later` write). `check-manifest-freshness` runs at step 0 (create / refresh / no-op / halt decision) whenever a manifest exists; the other five skills run at steps 3–6 on create/refresh only.

---

## 1. requirements-orch.md · 26 nodes / 40 edges / depth 4

```
orch → input-handler, requirements-drafter, requirements-resolver, requirements-merger,
       check-context-bloat, refusal-registry, state/.progress.json
input-handler ⇒ @input-handler-subtree (progress_path=.progress.json)
requirements-drafter → template-requirements.md, prototype-scope.md, general-rules.md,
       refusal-registry.md, verify-artifact-write, completeness-gap-pass.md, mermaid-validator.md
completeness-gap-pass → prototype-scope.md, general-rules.md, topics-requirements.md
requirements-resolver → characters/requirements-qa.md, run-qa-level1.md, run-qa-level2.md,
       flag-gaps-ambiguities.md, prototype-scope.md, general-rules.md
flag-gaps-ambiguities → prototype-scope.md, general-rules.md
requirements-merger → prototype-invariants.md
```

**Notes (unique):**
- drafter's `derive-architectural-implications` substep uses an **inline** capability catalogue declared in `requirements-drafter.md` → not a file edge. Rows emitted as `[AI-SUGGESTED: non-blocking]`, refined in resolver Phase 2.
- merger **retains** `[SRC: C-NNN]` tags in final `requirements.md`; `draft-claims.ndjson` stays authoritative for verbatim quotes (grounding re-verification).
- `template-requirements.md`'s `<!-- format: -->` / `<!-- guidance: -->` directives survive the merger strip (which only matches `[AI-SUGGESTED]`/`[STANDARD-RULE]`/`[OUT-OF-SCOPE]`/blocking-suffix/`AI-NNN`/`GR-NN`) — they are part of the published spec.
- `characters/requirements-qa.md` is a stub (no transitive deps).

---

## 2. design-system-orch.md · 30 nodes / 41 edges / depth 5

```
orch → design-system-styler, check-context-bloat, refusal-registry, state/.progress.json
design-system-styler → steps/step-01-activate … step-07-handback,
       characters/style-extraction.md, persona-llm.md
  step-01-activate → characters/style-extraction.md
  step-04-site-fetching → preflight-mcp, refusal-registry, setup-instructions/playwright.md,
       prompt-templates/site-fetching.md, prompt-templates/css-identification.md
  step-05-brand-extraction → prompt-templates/brand-extraction.md,
       data/insufficient-data-handling.md, data/color-extraction-rules.md, data/font-rules.md,
       data/typography-scale-rules.md, data/shadow-motion-rules.md
  step-05b-domain-inference → data/contrast-validation.md, prompt-templates/domain-inference.md
  step-06-artifact-generation → prompt-templates/artifact-generation.md, template-design-system.html,
       design-system-standards.html, data/component-catalogue.md, verify-artifact-write
prompt-templates/artifact-generation.md → template-design-system.html
preflight-mcp → refusal-registry
```

**Notes (unique):**
- Deepest tree (depth 5). `step-05b-domain-inference` derives an inferred token set per-run from the `{{domain}}` string (status colours + tokens left unset after step-05).
- `template-design-system.html` shared by `step-06` (operative loader) and `prompt-templates/artifact-generation.md` (which tells step-06 to read it).
- `data/component-catalogue.md` (step-06 only) owns the Components CSS + per-family `Live demo` / `States matrix` HTML; step-06 token-substitutes token refs into the template placeholders.
- `design-system-standards.html` names `template-design-spec.md` only in prose → not an edge. (`.md` sibling is the human-edit SoT; styler reads only the `.html`.)
- orch reads `requirements/` as the bloat proxy (step-0b); styler subtree itself reaches nothing in `requirements/`, `state/`, or the shared policy files.

---

## 3. review-requirement-orch.md · 32 nodes / 45 edges / depth 3

```
orch → review-selector, check-context-bloat, refusal-registry,
       + 5 reviewers: adversarial, first-principles, ten-ux-questions,
         ten-ba-questions, user-stories
review-selector → reviews/registry.md

Each reviewer → characters/<r>-review.md, reviews/<r>-reference.md,
                reviews/template-<r>.md, verify-artifact-write
deltas:
  adversarial      +adversarial-dimension-worker.md  [parallel ×8, read-only, step 3]
  first-principles +general-rules, prototype-invariants            [Q3/Q5 rescue, step 6]
  ten-ux-questions +general-rules, prototype-invariants, prototype-scope   [step-4 filter]
  ten-ba-questions +general-rules, prototype-invariants, prototype-scope,
                   +reviews/ten-ux-questions-reference.md  [one-way UX-drop filter, step 4]
  user-stories     +general-rules, prototype-invariants
```

**Notes (unique):**
- adversarial is the only sub-agent dispatch here (8 parallel read-only dimension workers, step 3); all others single-pass, no fan-out.
- Shared-policy reads are **filter sources only** — reviewers drop candidate questions already answered by an active `GR-NN`/`PI-NN` or out-of-scope per `prototype-scope.md`. (adversarial reads none — its task is defect-citation, not gap-filtering.)
- ba→ux-reference is **one-way** (ux never reads ba) — orthogonality enforced by a filter-time read, not a circular dep.
- first-principles / user-stories omit `prototype-scope.md` (their subjects are in-scope by construction); user-stories also omits the ux-reference (story-quality criteria are orthogonal to UX/BA framing) and applies no top-N cap.

---

## 4. analyse-requirement-orch.md · 22 nodes / 26 edges / depth 3

```
orch → analysis-selector, check-context-bloat, refusal-registry,
       + 12 analysers: ooux, jtbd, use-cases, data-model, user-journeys,
         sequence-diagram, state-diagram, activity-diagram, task-flows,
         five-whys, glossary, opportunity-solution-trees
analysis-selector → analyses/registry.md

task-flows-analyser → characters/task-flows-analysis.md, analyses/task-flows-reference.md,
       analyses/template-task-flows.html, verify-artifact-write, svg-overlap-check.md
data-model-analyser  → svg-overlap-check.md
state-diagram-analyser → svg-overlap-check.md
```

**Notes (unique):**
- Only task-flows' full 4-asset shape is drawn; the other 11 analysers fan out identically (reference + template + character + map-skill) — omitted for readability. `five-whys` + `glossary` carry `template_asset: null` (compose markdown directly).
- `svg-overlap-check.md` is called from the write step of the 3 SVG-heavy analysers (task-flows, data-model, state-diagram) only **after** `verify-artifact-write` passes and only when ≥1 inline SVG was emitted; writes `state/svg-overlap-<pipeline>.ndjson`.
- map-skills are **registry metadata** (for a future design-spec-drafter), not loaded by the analyser → no edge.

---

## 5. analyse-inputs-orch.md · 65 nodes / 81 edges / depth 4

```
orch → analysis-selector, check-context-bloat, input-handler, refusal-registry,
       + 11 analysers: thematic-analysis, opportunity-solution-trees, journey-mapping,
         task-analysis, jtbd, ooux, swim-lane-process-mapping, affinity-mapping,
         user-goal-analysis, business-context-definition, glossary
analysis-selector → analyses-inputs/registry.md
input-handler ⇒ @input-handler-subtree (progress_path=null)

Each analyser → analyses-inputs/<m>-reference.md, characters/<m>-inputs-analysis.md,
                verify-artifact-write
deltas:
  +template (analyses-inputs/template-<m>.html): journey-mapping, task-analysis, jtbd,
     ooux, swim-lane-process-mapping, affinity-mapping, user-goal-analysis,
     business-context-definition, glossary
  +mermaid-validator: thematic-analysis, opportunity-solution-trees, ooux,
     swim-lane-process-mapping, affinity-mapping
  +setup-instructions/mmdc.md: affinity-mapping only
  (thematic-analysis, opportunity-solution-trees carry NO template — pure markdown)
  (user-goal-analysis is intentionally dependency-free: HTML template, NO mermaid-validator,
     NO mmdc — its goal-refinement hierarchy renders as a CSS-only nested AND/OR tree)
  (business-context-definition is likewise dependency-free: HTML template, NO mermaid-validator,
     NO mmdc — its problem→need→goal causal-chain map renders as a CSS-only four-stage grid and
     its goal hierarchy as a CSS-only KAOS AND/OR tree)
  (glossary is likewise dependency-free: HTML template, NO mermaid-validator, NO mmdc — alphabetical
     term cards with classification/maturity/agreement badges + five open-item registers render in
     CSS only; it is the only analyses-inputs analyser using the [AI-SUGGESTED] channel as a
     convergence engine across L0/L1 (definition), L2 (refinement), synonym clusters, and L4
     conflicts (canonical-resolution), and the only one with map_skill: null)
```

**Notes (unique):**
- 11 MVP analysers; `five-whys` is `status: future` (file absent) → omitted; `glossary` is now `mvp`.
- input-handler create/refresh writes are the only writes outside `analyse-inputs/<METHOD>/`.
- map-skills are registry metadata → no edges (mirrors graph 4).
- **mermaid-validator behaviour:** on `not-installed`, thematic-analysis / opportunity-solution-trees / ooux / swim-lane halt; affinity-mapping surfaces `RF-07` with a 3-way `{install-and-retry, skip-with-warning, abort}` choice (degraded path). swim-lane / ooux / affinity-mapping implement drop-on-3-retry-failure (artefact still writes; block replaced with `[GAP-MERMAID-INVALID]`).
- affinity-mapping is the **only `mindmap`-emitting** analyser (+ conditional `flowchart TD` for tensions) → the only edge to `setup-instructions/mmdc.md`.
- affinity-mapping is the **only sub-agent-invoking** analyser: step-6 Round-3 `general-purpose` sub-agent receives the Round-1 notes JSON only (no Pass-1 labels) — documented "no sub-agents" exception (purely computational anti-anchoring KJ discipline; not drawn — one-shot tool call).
- Methodology rationale (KJ/ORCA/Rummler-Brache provenance, sibling comparisons, re-ingestibility) lives in each analyser + `*-reference.md`, not here.

---

## 6. review-inputs-orch.md · 33 nodes / 43 edges / depth 4

```
orch → analysis-selector, check-context-bloat, input-handler, refusal-registry,
       + 4 reviewers: adversarial, ambiguity, completeness, gap-analysis
analysis-selector → reviews-inputs/registry.md
input-handler ⇒ @input-handler-subtree (progress_path=null)

Each reviewer → characters/<r>-inputs-review.md, reviews-inputs/<r>-reference.md,
                verify-artifact-write
deltas:
  adversarial    +reviews-inputs/template-adversarial.html,
                 +adversarial-dimension-worker.md  [parallel ×6, NO tools, step 4]
  ambiguity      (none — pure markdown)
  completeness   +general-rules                          [step-15 disposition]
                 +prototype-scope  [cond: target=prototype, step 15]
  gap-analysis   +reviews-inputs/template-gap-analysis.html, +topics-requirements.md [step 3],
                 +general-rules                          [step 3]
                 +prototype-scope  [cond: target=prototype, step 3]
```

**Notes (unique):**
- `analysis-selector.md` shared with graphs 4 + 5; here it gets `list_label:"reviews"` + `verb_label:"review"`.
- adversarial fans out 6 parallel **tool-less** workers (parent inlines a frozen evidence bundle + quote indices, so workers need no disk access). adversarial + ambiguity are full-overwrite per run (no additive merge), unlike graph-5 analysers.
- `gap-analysis → topics-requirements.md` is the **only graph-6 edge** touching that file (otherwise read only by drafter + completeness-gap-pass in graph 1); the `Dimension` column is read verbatim. gap-analysis emits a drafter-ingestible `Candidate Requirement` column.
- completeness renders a 10×N coverage matrix; gap-analysis renders an HTML SVG heatmap. All four reviewers carry `map_skill: null`. `reviews-inputs/registry.md` has no remaining `future` rows.

---

## 7. generate-prd-orch.md · 23 nodes / 33 edges / depth 4

```
orch → input-handler, prd-drafter, prd-resolver, prd-merger,
       check-context-bloat, refusal-registry, state/.prd-progress.json
input-handler ⇒ @input-handler-subtree (progress_path=.prd-progress.json)
prd-drafter → template-prd.md, characters/prd-drafting.md, refusal-registry.md,
       verify-artifact-write, completeness-gap-pass-prd.md, grounding-verifier.md
completeness-gap-pass-prd → topics-prd.md
prd-resolver → characters/prd-resolving.md
prd-merger  → characters/prd-finalising.md
```

**Notes (unique):**
- `.prd-progress.json` is distinct from `.progress.json` so `/requirements` and `/generate-prd` can run concurrently without state collision; resolver sidecars likewise PRD-namespaced (`prd-resolver-*`).
- `source-manifest.json > target` is **informational only** (no decision branches; orch never invokes `set-build-target.md`). Pipeline is fully independent of `requirements/requirements.md` (never reads/writes it).
- Emits exactly **2 markers**: `[SRC: PC-NNN]`, `[AI-SUGGESTED: PAI-NNN]`. No `STANDARD-RULE`/`OUT-OF-SCOPE`/`REQ`. drafter's only shared edge is `refusal-registry.md` (RF-04) — **no** general-rules / prototype-scope. resolver has **no** shared-policy edges (unlike the requirements resolver).
- `completeness-gap-pass-prd.md` is a clone of `completeness-gap-pass.md` (smaller tree: no general-rules, no out-of-scope, no Tier C/D; Tier-A invariants B1–B10 are PRD-shaped). Cloned, not parameterised — bijection sets are pipeline-specific.
- merger retains `[SRC: PC-NNN]`; **never** appends a Prototype-invariants block (no edge to `prototype-invariants.md`).

---

## 8. wireframe-orch.md · 43 nodes / 64 edges / depth 4

```
orch → scope-selector, select-supporting-analyses, check-context-bloat,
       check-wireframe-set-freshness, blueprint-architect, wireframe-variant-generator,
       wireframe-comparator, refusal-registry

scope-selector → verify-artifact-write, wireframes/divergence-heuristics.md
  divergence-heuristics → wireframes/tradeoff-dimensions-registry.md,
                          wireframes/position-vocabulary.md
select-supporting-analyses → analyses/registry.md, analyses/sidecar-schema.md,
       verify-artifact-write, check-context-bloat,
       [writes per-scope] wireframes/<slug>/analyses-inputs.json

blueprint-architect → steps/step-01-activate … step-07-handback,
       characters/blueprint-architect.md, persona-llm.md
  step-01 → characters/blueprint-architect.md
  step-02 → analyses/sidecar-schema.md,
            [cond present] wireframes/<slug>/analyses-inputs.json,
            [cond sidecar branch] analyse-requirements/<M>/<name>.sidecar.json,
            [cond legacy ≤60KB, RF-09] analyse-requirements/<M>/*,
            [cond legacy only] analyse-requirements/TRADE-OFF-DIMENSIONS/trade-off-matrix.html
  step-03 → wireframes/realization-strategies.md
  step-04 → check-pattern-coverage, templates/template-blueprint.md, verify-artifact-write
  step-05 → trade-off-dimensions.md, wireframes/tradeoff-dimensions-registry.md,
            wireframes/pattern-bindings.md, wireframes/domain-defaults.md,
            wireframes/position-vocabulary.md, pattern-catalogue/_index.md,
            wireframes/realization-strategies.md,
            [cond deferred sidecar] analyse-requirements/<M>/<name>.sidecar.json,
            [cond deferred legacy] analyse-requirements/<M>/*
  step-06 → verify-artifact-write
check-pattern-coverage → pattern-catalogue/_index.md

wireframe-variant-generator → steps/step-01-activate … step-06-self-validate-and-handback,
       characters/wireframe-variant.md, persona-llm.md   [parallel sub-agent: 1 Agent call/variant, cap 4]
  step-01 → characters/wireframe-variant.md
  step-02 → templates/template-screen.html, wireframes/position-vocabulary.md, pattern-catalogue/_index.md
  step-03 → design-systems/wireframe-ds.html, verify-artifact-write
  step-04 → pattern-catalogue/_index.md, wireframes/position-vocabulary.md, verify-artifact-write
  step-05 → verify-artifact-write

wireframe-comparator → characters/wireframe-comparator.md, persona-llm.md,
       wireframes/template-set-index.html, wireframes/position-vocabulary.md, verify-artifact-write
```

**Notes (unique):**
- **Four-stage** (Scope → Design-Brief → Parallel Variant Generation → Comparison), not registry-driven. Variant cardinality default 2 / cap 3; configs are emergent (composed by architect from dimensions × goals × personas, not a closed archetype registry). variant-generator is the only parallel sub-agent; scope-selector / architect / comparator run foreground.
- **Cross-pipeline** (shared with a future `/prototype`): `blueprint-architect.md`, `scope-selector.md`, `check-pattern-coverage.md`. `check-wireframe-set-freshness.md` is wireframe-private. architect writes `blueprints/<slug>/{scope.json, blueprint.md}` — the documented cross-pipeline exception.
- **Sidecar-first protocol** (per `analyses/sidecar-schema.md`): `sidecar_present` → read sidecar (≤20 KB); else bounded full-Read of the prose `output_path` ≤60 KB (`RF-09`); drift halts under `RF-08`. Applies at step-02 and at step-05's deferred step-5-only selections.
- `analyses-inputs.json` read only when `analyses_inputs_path` is non-null and present. `select-supporting-analyses` **auto-proceeds (no prompt)** when zero MVP analyses resolve on disk → empty `selections[]` → `selected-none`. `trade-off-matrix.html` is legacy-fallback only (step-2.7, when `analyses_inputs_path` null/absent AND trade-off-dimensions not selected at Stage 1b).
- **Surface-model refactor:** per-screen pattern selection lives in the architect's `variants.json > surface_plan` (step-05 reads `pattern-catalogue/_index.md` + `realization-strategies.md`). The generator now **renders** `surface_plan` (no longer reads `tradeoff-dimensions-registry.md` / `pattern-bindings.md`); the comparator checks **render-vs-`surface_plan`** (no longer re-derives from the registry).
- **Logical-surface model:** blueprint is a decomposition-agnostic `LS-NN` inventory + `allowed`/`default` realizations (per `realization-strategies.md`). Each `surface_plan` picks a realization (standalone / inline-drawer / inline-expand / modal / wizard-split). All-standalone baseline ≡ legacy 1-screen-per-surface (`LS-NN ≡ S-NN`).
- **Goal-driven divergence:** scope-selector executes `divergence-heuristics.md` when orch passes `propose_divergence_axes: true` and persists `divergence_profile` into `scope.json`; the architect **consumes** that profile at step-05 (does **not** re-read the heuristic → no `architect → divergence-heuristics` edge).
- `pattern-catalogue/_index.md` is shared with the `/design-system` styler (which loads it transitively via `data/component-catalogue.md`); wireframe consumers read it directly. Per-pattern files under `pattern-catalogue/<category>/<pattern>.md` are read **selectively** (only picked patterns), not en masse.

---

## 9. prototype-orch.md · one-prototype-per-run; generates a real Next.js app

```
orch → scope-selector, select-prototype-inputs, check-context-bloat,
       blueprint-architect, prototype-spec-drafter, prototype-spec-resolver, prototype-spec-merger,
       prototype-app-scaffolder, prototype-generator, prototype-landing-updater,
       refusal-registry, state/.prototype-progress.json

scope-selector → verify-artifact-write   [propose_divergence_axes:false → NO divergence-heuristics edge]
select-prototype-inputs → analyses/registry.md, analyses-inputs/registry.md, analyses/sidecar-schema.md,
       wireframes/<slug>/variants.json, requirements/source-manifest.json,
       verify-artifact-write, check-context-bloat,
       [writes] prototypes/.specs/<name-slug>/supporting-inputs.json
blueprint-architect → (see graph 8; invoked with variants_output_path:null → blueprint-only, writes
       blueprints/<slug>/blueprint.md, NO variants.json)
prototype-spec-drafter → prototypes/template-design-spec.md,
       characters/prototype-spec-drafting.md, prototypes/design-philosophies.md,
       prototypes/ux-baseline-checklist.md, wireframes/position-vocabulary.md,
       wireframes/tradeoff-dimensions-registry.md, blueprints/<slug>/blueprint.md, verify-artifact-write
       [cond fast path] wireframes/<slug>/<variant>/{variant-position.json, manifest.json}
prototype-spec-resolver → characters/prototype-spec-resolving.md, flag-gaps-ambiguities.md,
       wireframes/tradeoff-dimensions-registry.md, verify-artifact-write
prototype-spec-merger → characters/prototype-spec-finalising.md, prototype-invariants.md
prototype-app-scaffolder → scaffold-prototype-app.md, extract-brand-theme.md,
       prototypes/scaffolding-instructions.md, prototypes/app-shell-spec.md, verify-artifact-write
       [cond brand source a] design-system/design-system.html
prototype-generator → steps/step-01-activate … step-07-handback, steps/step-sub-render-surface.md,
       characters/prototype-generator.md, persona-llm.md, prototypes/shared-component-conventions.md,
       prototypes/ux-baseline-checklist.md, blueprints/<slug>/blueprint.md,
       verify-prototype-build.md, verify-artifact-write
       [parallel sub-agent: 1 Agent call/surface, cap 4 → step-sub-render-surface]
  verify-prototype-build → refusal-registry (RF-11/RF-12)
prototype-landing-updater → wireframes/position-vocabulary.md, verify-artifact-write
```

**Notes (unique):**
- **One prototype per run**, accumulating in the shared `prototypes/` Next.js app (rule 1). `.prototype-progress.json` tracks the in-flight run; the durable completed set lives in `prototypes/.registry.json`. Distinct progress file → concurrent with other pipelines.
- **Cross-pipeline reuse:** `scope-selector` (`propose_divergence_axes:false`) + `blueprint-architect` (`variants_output_path:null`, blueprint-only). Write scope: `prototypes/**` + `framework/state/*` (+ the shared `blueprints/<slug>/{scope.json,blueprint.md}` exception via those two shared components). `prototypes/template-design-spec.md`, `design-philosophies.md`, `ux-baseline-checklist.md`, `scaffolding-instructions.md`, `app-shell-spec.md`, `shared-component-conventions.md` all live under `framework/assets/prototypes/`.
- **Divergence is UX only** (brand fixed/shared). The posture preset (`design-philosophies.md`) supplies D1–D5 starting positions (references `tradeoff-dimensions-registry.md` + `position-vocabulary.md`, never redefines; **D6 inactive → 0**). On the **wireframe-seeded fast path**, the drafter cites realizations from a selected variant's `surface_plan` (not `[AI-SUGGESTED]`), so the resolver often auto-completes.
- **Conditional scaffold:** `prototype-app-scaffolder` runs only on the first run (skipped when `prototypes/.scaffold.json` present). Brand source a→b→c via `extract-brand-theme.md`. `npm install` once (amortised — rule 13).
- **Parallel generation:** `prototype-generator` is the only parallel sub-agent dispatch (≤4 per-surface sub-agents, non-interactive). The driver owns cross-cutting writes (types/fixtures/stores/seed) + all route files; sub-agents own disjoint shared-component filenames (collision-safety per `shared-component-conventions.md §3`).
- **Verify gate:** `verify-prototype-build.md` runs lint + tsc + `next build` + Playwright smoke. New refusals `RF-10` (node missing), `RF-11` (playwright browsers), `RF-12` (build failed after retries), `RF-13` (scaffold failed). Invariants PI-01..PI-08 (PI-08 = chrome is a harness).
- **Anti-fabrication:** every `data-prop` binds to a blueprint per-surface Property closed set; fixtures carry only closed-set fields — mirrors the wireframe `data-prop` rule.
- **Per-prototype reset** deletes only the in-flight slug's `.specs/<slug>/` + `src/app/<slug>/` + its `.registry.json` entry + resolver sidecars; never other prototypes, the shared library, the scaffold, or the brand.
