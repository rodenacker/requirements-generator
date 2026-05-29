---
role: asset
kind: registry
methodologies:
  # Planned methodologies for /analyse-inputs. Each methodology lands in its own
  # follow-up development, promoting `status: future` to `status: mvp` and filling in
  # the remaining seven fields. MVP methodologies so far:
  #   - `thematic-analysis` (Braun & Clarke 2006, six-phase reflexive thematic
  #     analysis with a deductive coverage check against a fixed 10-area concern
  #     frame; pure markdown + Mermaid theme-map).
  #   - `opportunity-solution-trees` (Teresa Torres 2016, four-layer discovery
  #     tree adapted for raw consultant inputs — forward discovery, vs the
  #     reverse-discovery sibling under /analyse-requirement; pure markdown +
  #     Mermaid graph TD; carries a `## Candidate requirements` bridge that
  #     `/requirements` consumes when the artefact is re-dropped into `input/`).
  #   - `journey-mapping` (NN/G Journey Mapping 101 + Kalbach 2020,
  #     current-state user-journey mapping adapted for raw consultant inputs
  #     — one persona per journey card, [SRC: <filename>] citations on every
  #     non-empty cell, emotion proxies rendered inline for transparency,
  #     self-contained HTML with diagrams-first ordering: compact overview,
  #     prominent #diagrams gallery with inline SVG emotion curves +
  #     CSS-grid swim-lane tables, then #narratives, then collapsed
  #     diagnostics; HTML survives markitdown round-trip for /requirements
  #     re-ingestion with end-to-end audit trail through preserved
  #     [SRC: <filename>] markers).
  #   - `task-analysis` (Hierarchical Task Analysis — Annett & Duncan 1967,
  #     Stanton 2006 — augmented with a Sub-Goal Template-derived
  #     per-terminal information layer (Ormerod & Shepherd 2004); adapted
  #     for raw consultant inputs as a single-actor, decomposition-first,
  #     document-only extraction; numbered goal/sub-goal/operation tree
  #     with mandatory Plans (sequence/selection/iteration/concurrent/
  #     discretionary) on every non-terminal; per-terminal data nouns
  #     (read/write directions); [SRC: <filename>] citations on every
  #     non-inferred node, [AI-SUGGESTED: AI-NNN | blocking|non-blocking]
  #     on inferred non-terminals + inferred Plans only — inferred
  #     terminals forbidden (Diaper & Stanton 2004 anti-confabulation
  #     rule); silent-Plan branches escalate through a three-tier process,
  #     never silently default to `sequence`; self-contained HTML with
  #     embedded <pre><code class="language-yaml"> structured tree that
  #     survives markitdown HTML→MD conversion as fenced code, making
  #     the artefact the primary structural-input-handoff to the
  #     /requirements drafter when copied into input/ for re-ingestion).
  #   - `jtbd` (Jobs-To-Be-Done — hybrid Christensen-Moesta canonical
  #     statement form `When <situation>, I want to <motivation>, so I
  #     can <outcome>` + four forces of progress (push/pull/anxiety/
  #     habit) + Ulwick importance × satisfaction = opportunity scoring
  #     `Opp = Imp + max(0, Imp - Sat)` with 1–5 scale; adapted for raw
  #     consultant inputs as a six-round JTBD-X process whose actors,
  #     situations, motivations, outcomes, and forces are anchored to
  #     manifest-row filenames via [SRC: <filename>] markers; outcomes
  #     without anchorable measures carry `(no-metric-in-inputs)`;
  #     unsignaled Importance/Satisfaction scores carry
  #     `consultant-assigned-no-signal`; forces with no input mention
  #     carry `not-named-in-inputs` (surfacing absence — most raw input
  #     sets name Push and Pull but rarely Anxiety and Habit); self-
  #     contained HTML job-card grid + 5×5 opportunity matrix; re-
  #     ingestible by /requirements via Native-text classification when
  #     copied into input/, with end-to-end audit trail preserved
  #     through dual-citation chain).
  #   - `ooux` (Sophia Prater's ORCA process — six rounds Discovery →
  #     Objects → Relationships → CTAs → Attributes → CCPs — adapted for
  #     raw consultant inputs as a multi-source, synonym-merge-load-bearing,
  #     document-only extraction; canonical object list emerges from raw
  #     prose, ERD diagrams, brief sections, interview notes, and whiteboard
  #     photos through Round 1 Discovery + Round 2 synonym merge; provenance
  #     markers `from-source-<filename>` / `synonym-merged-from-[<filenames>]`
  #     / `inferred-from-<filename>` on every object — never an unmarked
  #     object, never a fourth marker; every CTA, attribute, CCP, and
  #     relationship carries `[SRC: <filename>]` matching a manifest row's
  #     `filename` field exactly; the artefact ships three visual surfaces
  #     plus a machine-readable body block: Mermaid `erDiagram` (entities +
  #     relationships + cardinality + PK on primary CCP — the "MUST contain
  #     a diagram" deliverable; survives markitdown HTML→MD as a fenced code
  #     block), canonical OOUX sticky-note column-board (CTAs, header, CCPs,
  #     metadata, nested refs), relationship matrix table, and a
  #     `<pre><code class="language-json" id="ooux-object-map-body">` block
  #     carrying the full object model in JSON for `/requirements`
  #     re-ingestion via markitdown round-trip — the load-bearing
  #     machine-readable contract for the downstream drafter; eight hard
  #     quality gates: seven inherited from the requirements-side OOUX
  #     reference (every Object has ≥1 CTA; every CTA attaches to exactly
  #     one Object; every nested Relationship declares cardinality; every
  #     Object has ≥1 CCP; no orphan Attributes; provenance markers
  #     exhaustive; matrix + nested refs + Mermaid agree) plus Gate 8
  #     specific to the inputs side: every consumed manifest row contributes
  #     ≥1 candidate noun in Round 1 OR is marked `irrelevant-to-domain`
  #     in diagnostics with a one-line reason — surfacing silent skips the
  #     synthesised `requirements/requirements.md` would have hidden; the
  #     synonym-merge log in diagnostics is the most-interpretive surface
  #     and the audit trail consultants use to confirm or revise
  #     cross-source identity decisions; re-ingestible by `/requirements`
  #     when copied into `input/` with end-to-end audit trail preserved
  #     through the markitdown HTML→MD pathway).
  #   - `swim-lane-process-mapping` (Rummler-Brache Cross-Functional
  #     Process Mapping + Disconnect Analysis — Rummler & Brache 1990,
  #     *Improving Performance: How to Manage the White Space on the
  #     Organization Chart*; framed under BABOK 10.35 Process
  #     Modelling; adapted for raw consultant inputs as a multi-actor,
  #     handoff-shaped, document-only extraction; one or more discrete
  #     processes per artefact, each rendered as a Mermaid `flowchart
  #     TD` source block with one `subgraph` swim-lane per actor
  #     (kind: role / system / external-service); steps typed
  #     `start` / `end` / `process` / `decision` / `data-store` /
  #     `external-system`; every lane-to-lane handoff (the lane-
  #     crossing edges that are the methodology's first-class
  #     objects) classified in a global Disconnect Register via the
  #     conjunctive four-element cleanliness rubric — named source
  #     step AND trigger event AND receiving lane AND payload →
  #     `clean`; otherwise one of four non-`clean` categories
  #     (`ambiguous-trigger`, `missing-actor`, `unstated-exception`,
  #     `conflicting-source`) with the missing element specifically
  #     flagged and a suggested resolver question for the next
  #     consultant conversation — Rummler estimated 80% of process
  #     failures live in the "white space" between lanes, and the
  #     register is the methodology's analytical lens onto that
  #     white space; inferred lane assignments, routing steps, and
  #     handoff payloads carry [AI-SUGGESTED: AI-NNN |
  #     blocking|non-blocking] markers in the shared namespace;
  #     inferred disconnect trigger events forbidden — the
  #     description names the missing element, not the guess;
  #     self-contained HTML with embedded `<pre class="mermaid-source">`
  #     blocks (rendered visual is out-of-band via mmdc or
  #     mermaid.live; no inline Mermaid runtime, no CDN), an
  #     embedded `<pre><code class="language-yaml">` structured
  #     process model that survives markitdown HTML→MD conversion
  #     as a fenced code block (the load-bearing re-ingestion
  #     contract for the /requirements drafter), an Actor inventory
  #     table, the Disconnect Register table with five category
  #     pills, a Gaps section for inferred nodes, and a collapsed
  #     diagnostics block; re-ingestible by /requirements when
  #     copied into input/, with the Disconnect Register's
  #     `consultant_follow_up: yes` rows flowing into the resolver
  #     pipeline as AI-NNN questions in the existing grammar).
  #   - `user-goal-analysis` (User Goal Analysis — a pragmatic Goal-Oriented
  #     Requirements Engineering synthesis: Cooper's three goal types
  #     (life / end / experience) + the hard/soft goal split (Chung et al.
  #     NFR framework) + KAOS AND/OR goal refinement (van Lamsweerde) +
  #     means-end laddering (Gutman) & Five-Whys for inferring unstated
  #     goals + an i*-lite actor↔goal dependency map (Yu); adapted for raw
  #     consultant inputs as a six-pass document-only
  #     extraction-AND-bounded-inference process. Surfaces user goals both
  #     EXPLICITLY stated and INFERRED. Explicit goals carry [SRC: <filename>];
  #     inferred goals carry [AI-SUGGESTED: AI-NN | blocking|non-blocking]
  #     co-present with a named technique (laddering / five-whys /
  #     solution-reframe / obstacle-analysis / softgoal-from-quality-adjective)
  #     AND ≥1 source anchor — anchorless inference is forbidden (the
  #     load-bearing anti-confabulation gate G2, mirroring task-analysis's
  #     "inferred terminals forbidden"). Seven hard gates (provenance,
  #     anti-confabulation, solution-bias/anti-vacuity, classification,
  #     hierarchy integrity, criterion, coverage). Self-contained,
  #     dependency-free HTML (NO Mermaid / mmdc): goal register grouped by
  #     Cooper type, a CSS-only nested AND/OR refinement tree, an actor map,
  #     a conflicts table, and an embedded
  #     <pre><code class="language-json" id="user-goal-analysis-body"> block
  #     carrying the full goal model for /requirements re-ingestion via
  #     markitdown HTML→MD round-trip. Designed as a /requirements input:
  #     explicit goals seed §4 User goals & stories; inferred goals surface
  #     to the resolver as AI-NNN questions — blocking ones as mandatory
  #     confirmations — so the consultant validates every inference before it
  #     becomes a requirement. Distinct from JTBD (jobs, extraction-only),
  #     task-analysis (decomposes a GIVEN goal DOWN into operations), and
  #     opportunity-solution-trees (jumps to solutions).
  - { name: glossary, status: future }
  - { name: five-whys, status: future }
  - name: task-analysis
    status: mvp
    description: Hierarchical Task Analysis (HTA) of raw consultant inputs — decomposes user goals into a numbered sub-goal / operation tree with mandatory Plans (sequence / selection / iteration / concurrent / discretionary) on every non-terminal and per-terminal data-noun annotations (Sub-Goal Template information layer). Designed to be re-fed into /requirements as a secondary input — the embedded YAML structured tree becomes a bijection target for the drafter's completeness gap pass, Plans seed acceptance-criteria branches, and information-requirements hint at §7 Data entities.
    output_path: analyse-inputs/TASK-ANALYSIS/task-analysis.html
    reference_asset: framework/assets/analyses-inputs/task-analysis-reference.md
    template_asset: framework/assets/analyses-inputs/template-task-analysis.html
    map_skill: framework/skills/map-task-analysis-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/task-analysis-analyser.md
    character: framework/assets/characters/task-analysis-inputs-analysis.md
  - name: thematic-analysis
    status: mvp
    description: Surfaces the patterns the consultant's raw inputs already carry as codes, themes, and a theme-map — and bridges each theme to candidate requirements before /requirements drafts them.
    output_path: analyse-inputs/THEMATIC-ANALYSIS/thematic-analysis.md
    reference_asset: framework/assets/analyses-inputs/thematic-analysis-reference.md
    template_asset: null
    map_skill: framework/skills/map-thematic-analysis-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/thematic-analysis-analyser.md
    character: framework/assets/characters/thematic-analysis-inputs-analysis.md
  - name: opportunity-solution-trees
    status: mvp
    description: Maps raw inputs into an outcome → opportunities → solutions → assumption-test discovery tree (Torres 2016), with a bridge of candidate-requirement seeds /requirements can pick up when the artefact is re-dropped into input/.
    output_path: analyse-inputs/OPPORTUNITY-SOLUTION-TREES/opportunity-solution-tree.md
    reference_asset: framework/assets/analyses-inputs/opportunity-solution-trees-reference.md
    template_asset: null
    map_skill: framework/skills/map-opportunity-solution-trees-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/opportunity-solution-trees-analyser.md
    character: framework/assets/characters/opportunity-solution-trees-inputs-analysis.md
  - name: journey-mapping
    status: mvp
    description: Maps the as-is user workflow described in raw inputs into one journey card per persona — phases, steps, touchpoints, channels, thoughts, sentiment curve, pain points, backstage, opportunities, moments of truth — giving the /requirements drafter a concrete backbone for task flows, NFRs, integrations, user stories, and priorities.
    output_path: analyse-inputs/JOURNEY-MAPPING/journey-mapping.html
    reference_asset: framework/assets/analyses-inputs/journey-mapping-reference.md
    template_asset: framework/assets/analyses-inputs/template-journey-mapping.html
    map_skill: framework/skills/map-journey-mapping-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/journey-mapping-analyser.md
    character: framework/assets/characters/journey-mapping-inputs-analysis.md
  - name: jtbd
    status: mvp
    description: Surfaces the jobs, outcomes, and forces of progress (push / pull / anxiety / habit) that the consultant's raw inputs describe — hybrid Christensen-Moesta canonical statement form + Ulwick opportunity scoring — so the requirements that follow anchor to user motivation rather than features. Re-ingestible by /requirements when copied into input/ as a Native-text source.
    output_path: analyse-inputs/JTBD/jtbd-job-map.html
    reference_asset: framework/assets/analyses-inputs/jtbd-reference.md
    template_asset: framework/assets/analyses-inputs/template-jtbd.html
    map_skill: framework/skills/map-jtbd-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/jtbd-analyser.md
    character: framework/assets/characters/jtbd-inputs-analysis.md
  - name: ooux
    status: mvp
    description: Sophia Prater's ORCA process applied to raw consultant inputs — six rounds (Discovery → Objects → Relationships → CTAs → Attributes → CCPs) producing the canonical OOUX sticky-note column-board PLUS a Mermaid `erDiagram` of objects + relationships + cardinality PLUS an embedded `<pre><code class="language-json">` body block carrying the full machine-readable object model. Synonym merge across sources is the load-bearing Round 2 step (`Customer` vs `Client` vs `Account holder` — every collision logged with literal terms collapsed, source filenames, and merge heuristic). Provenance markers `from-source-<filename>` / `synonym-merged-from-[<filenames>]` / `inferred-from-<filename>` on every object — never unmarked. Eight hard quality gates: seven inherited from the requirements-side OOUX reference plus Gate 8 (every consumed manifest row contributes ≥1 candidate noun OR is marked `irrelevant-to-domain` with a reason — surfaces silent skips that the synthesised `requirements/requirements.md` would have hidden). Designed as a `/requirements` re-ingestion input — the embedded JSON body block and the Mermaid erDiagram both survive markitdown HTML→MD conversion as fenced code blocks, so the drafter consumes the full object model in one shot when the consultant copies the artefact into `input/` for a downstream `/requirements` run.
    output_path: analyse-inputs/OOUX/ooux-object-map.html
    reference_asset: framework/assets/analyses-inputs/ooux-reference.md
    template_asset: framework/assets/analyses-inputs/template-ooux.html
    map_skill: framework/skills/map-ooux-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/ooux-analyser.md
    character: framework/assets/characters/ooux-inputs-analysis.md
  - name: swim-lane-process-mapping
    status: mvp
    description: Maps every discrete cross-functional process the raw inputs describe into Rummler-Brache swim-lane flowcharts (Mermaid `flowchart TD` with one `subgraph` per actor lane) and surfaces a Disconnect Register classifying every lane-to-lane handoff — clean / ambiguous-trigger / missing-actor / unstated-exception / conflicting-source — exposing the "white-space" gaps Rummler attributed 80% of process failures to. Designed to be re-fed into /requirements as a secondary input — the embedded YAML structured model becomes a bijection target for the drafter's completeness gap pass (processes → §5 Task flows, handoffs → §6 integration constraints, decision branch guards → §6 acceptance-criteria branches, data-store and external-system steps → §7 data entities and §2 external-system aggregates), and every `consultant_follow_up: yes` disconnect flows into the resolver as an AI-NNN question.
    output_path: analyse-inputs/SWIM-LANE-PROCESS-MAPPING/swim-lane-process-mapping.html
    reference_asset: framework/assets/analyses-inputs/swim-lane-process-mapping-reference.md
    template_asset: framework/assets/analyses-inputs/template-swim-lane-process-mapping.html
    map_skill: framework/skills/map-swim-lane-process-mapping-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/swim-lane-process-mapping-analyser.md
    character: framework/assets/characters/swim-lane-process-mapping-inputs-analysis.md
  - name: affinity-mapping
    status: mvp
    description: Bottom-up affinity diagram (Kawakita 1967 KJ method; Beyer & Holtzblatt 1997 Contextual Design) applied to raw consultant inputs — atomic notes extracted per-claim from briefs / decks / interviews / screenshots, clustered by conceptual similarity through a sub-agent-isolated two-pass re-cluster (Pass-1 in main context; Pass-2 in a fresh sub-agent context that sees only the note list — the only realistic anti-anchoring mechanism for an autonomous LLM run; Jaccard-similarity drift detection on cluster memberships, no semantic-equivalence judgement required), labelled in insight-statement form (Beyer/Holtzblatt rule — labels after clustering, never before), grouped into 4–8 L3 super-themes; orphans preserved in an explicit parking-lot; cross-cluster tensions surfaced as a secondary diagram when present. Self-contained HTML with diagram-first ordering: compact overview, primary Mermaid `mindmap` near top (root → super-themes → L2 clusters only — full notes live in cluster cards below to preserve mindmap legibility at ≤34 nodes), conditional secondary Mermaid `flowchart TD` tension graph, cluster cards listing every note with `[SRC: <filename>]` citations and stable/drifted confidence chip with Jaccard value, orphans table, embedded `<pre><code class="language-json" id="affinity-map-body">` re-ingestion block carrying the full hierarchy, collapsed diagnostics with Pass-1/Pass-2 Jaccard drift log. Re-ingestible by /requirements via markitdown HTML→MD when copied into input/ — the JSON body block and mindmap source survive as fenced code blocks; super-theme insight statements feed §1 vision anchors, clusters feed §5 task-flow groupings and §3 acceptance-criteria threads, orphans feed §10 out-of-scope candidates, tensions feed §6 trade-off-aware acceptance-criteria branches.
    output_path: analyse-inputs/AFFINITY-MAPPING/affinity-map.html
    reference_asset: framework/assets/analyses-inputs/affinity-mapping-reference.md
    template_asset: framework/assets/analyses-inputs/template-affinity-mapping.html
    map_skill: framework/skills/map-affinity-mapping-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/affinity-mapping-analyser.md
    character: framework/assets/characters/affinity-mapping-inputs-analysis.md
  - name: user-goal-analysis
    status: mvp
    description: Surfaces the user goals the raw inputs carry — both explicitly stated AND inferred — as a readability-optimised HTML goal register. A pragmatic GORE synthesis (Cooper's life/end/experience goal types + hard/soft goals + KAOS AND/OR refinement + means-end laddering & Five-Whys for inference + an i*-lite actor↔goal map). Explicit goals carry [SRC: <filename>]; inferred goals carry [AI-SUGGESTED: AI-NN | blocking|non-blocking] co-present with a named technique (laddering / five-whys / solution-reframe / obstacle-analysis / softgoal-from-quality-adjective) AND ≥1 source anchor — anchorless inference is forbidden (anti-confabulation gate G2). Seven hard gates. Self-contained, dependency-free HTML (NO Mermaid): goal register grouped by Cooper type, a CSS-only nested AND/OR refinement tree, an actor map, a conflicts table, and an embedded <pre><code class="language-json" id="user-goal-analysis-body"> block carrying the full goal model. Designed to be re-fed into /requirements — explicit goals seed §4 User goals & stories; inferred goals surface to the resolver as AI-NNN questions (blocking ones as mandatory confirmations), so the consultant validates every inference before it becomes a requirement. Distinct from JTBD (jobs, extraction-only), task-analysis (decomposes a GIVEN goal DOWN into operations), and opportunity-solution-trees (jumps to solutions).
    output_path: analyse-inputs/USER-GOAL-ANALYSIS/user-goal-analysis.html
    reference_asset: framework/assets/analyses-inputs/user-goal-analysis-reference.md
    template_asset: framework/assets/analyses-inputs/template-user-goal-analysis.html
    map_skill: framework/skills/map-user-goal-analysis-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/user-goal-analysis-analyser.md
    character: framework/assets/characters/user-goal-analysis-inputs-analysis.md
---

# analyses-inputs/registry.md

**Purpose:** Methodology registry for `/analyse-inputs`. Sibling of `framework/assets/analyses/registry.md`. The frontmatter above is the **machine-readable** contract — `framework/skills/analysis-selector.md` filters `status == "mvp"` to present options to the consultant when invoked with `registry_path: "framework/assets/analyses-inputs/registry.md"`; `framework/orchestrators/analyse-inputs-orch.md` looks up `analyser_agent` for the chosen methodology and invokes it at step 3.

**Source material:** unlike `/analyse-requirement` (whose analysers read `requirements/requirements.md`), methodologies registered here operate over the raw consultant-dropped material in `input/`, enumerated via `requirements/source-manifest.json`. The shared `framework/agents/input-handler.md` builds the manifest on demand at the orchestrator's step 1.

**Used by:**

- `framework/skills/analysis-selector.md` — reads MVP-status rows; presents them via the numbered-list prompt.
- `framework/orchestrators/analyse-inputs-orch.md` — reads the chosen row's `analyser_agent` and `output_path` to drive invocation and the prior-artefact gate.
- `framework/agents/analyses-inputs/<method>-analyser.md` — each analyser reads its own `reference_asset`, `character`, and `template_asset` paths at activation. No analyser file exists on disk until its row has been promoted to `status: mvp`.

**Adding a new methodology (per-PR steps):**

1. Pick a planned row (e.g. `{ name: glossary, status: future }`) or append a new one.
2. Author the analyser agent at `framework/agents/analyses-inputs/<method>-analyser.md`. Each analyser:
    - Reads `requirements/source-manifest.json` once at Step 2 to enumerate sources.
    - For each manifest row where `tier != "Unsupported"`: Read the file at `original_path` (for `Native-text` and `Native-multimodal`) or `converted_sibling` (for `Supported-via-MCP`). For `Native-multimodal`, the Read tool surfaces image bytes as multimodal input automatically.
    - Skips manifest rows with `tier == "Unsupported"` and records the reason in the artefact's diagnostics block.
    - Cites source-of-fact in the artefact body using `[SRC: <filename>]` markers (filename payload, not the requirements pipeline's `C-NNN` sidecar IDs).
    - Records a source-roster section in the artefact listing every filename consumed and every skipped filename with reason.
    - Records a manifest-fingerprint field in the artefact (the manifest's sha256, or sha256 of its serialised bytes) so the artefact captures exactly which manifest version it analysed.
    - Self-validates: every manifest row with `tier != "Unsupported"` was Read or skipped-with-reason; the artefact reads no path under `requirements/` other than `requirements/source-manifest.json`; the artefact reads no path under `framework/state/` or `framework/shared/`.
3. Author the reference asset at `framework/assets/analyses-inputs/<method>-reference.md` (methodology rules and patterns).
4. Author the character file at `framework/assets/characters/<method>-inputs-analysis.md` (Unicorn stance during the analyser run).
5. (Optional) Author the template asset at `framework/assets/analyses-inputs/template-<method>.{html,md}`. Set `template_asset: null` for methodologies that emit pure Markdown without a scaffold (the `analyses/registry.md` precedent: `five-whys` and `glossary` both ship with `template_asset: null`).
6. (Optional) Author the map-skill at `framework/skills/map-<method>-from-inputs-to-ui.md` — or reuse `framework/skills/map-<method>-to-ui.md` if the mapping is source-agnostic.
7. Promote the registry row: flip `status: future` to `status: mvp` and populate all remaining fields (`description`, `output_path`, `reference_asset`, `template_asset`, `map_skill`, `analyser_agent`, `character`). `output_path` lives under `analyse-inputs/<METHOD>/` (uppercase methodology name) — e.g. `analyse-inputs/GLOSSARY/glossary.md`.
8. Add the analyser node to graph 5 in `framework/dependency-graphs.md`.
9. No orchestrator changes required — the selector skill picks the new MVP row up automatically.

**Field semantics:**

- `name` — kebab-case slug. Used as the subdirectory name under `analyse-inputs/` (uppercased to `analyse-inputs/<METHOD>/`) and as the path component in the analyser agent file. Methodology slugs are shared across registries (a row named `glossary` can exist in both `analyses/registry.md` and `analyses-inputs/registry.md`); the artefacts do not clobber because the output paths differ (`analyse-requirements/GLOSSARY/...` vs `analyse-inputs/GLOSSARY/...`).
- `status` — `mvp` (selectable now) or `future` (not yet built; this is the default state for every row on framework first-ship).
- `description` — one-line label surfaced in the selector's printed list. Required only when `status: mvp`.
- `output_path` — relative path of the artefact the analyser writes. Drives the prior-artefact gate in the orchestrator. **Must** live under `analyse-inputs/` for write-isolation. Required only when `status: mvp`.
- `reference_asset` — the methodology reference the analyser follows. Required only when `status: mvp`.
- `template_asset` — file scaffold the analyser populates (may be `null` for methodologies that emit pure Markdown).
- `map_skill` — translates the analysis output into UI inventory entries for downstream design consumption. May reuse the existing `framework/skills/map-<method>-to-ui.md` if source-agnostic, or be a sibling `map-<method>-from-inputs-to-ui.md` if the mapping diverges. Not invoked by `/analyse-inputs`.
- `analyser_agent` — the foreground agent invoked by the orchestrator. Required only when `status: mvp`.
- `character` — stance the Unicorn adopts while running the analyser. Required only when `status: mvp`.

**Empty-MVP behaviour:** when every row has `status: future` the selector returns `empty-registry` and the orchestrator surfaces a friendly "no input analyses available yet" message and exits cleanly. This was the expected steady state on framework first-ship; with `task-analysis`, `thematic-analysis`, `opportunity-solution-trees`, `journey-mapping`, `jtbd`, `ooux`, `swim-lane-process-mapping`, `affinity-mapping`, and `user-goal-analysis` now at `status: mvp`, the selector presents nine options to the consultant. If every MVP row is removed in the future, the empty-registry behaviour resumes — it is not an error.
