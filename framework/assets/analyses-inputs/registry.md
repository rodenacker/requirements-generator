---
role: asset
kind: registry
methodologies:
  # Methodologies for /analyse-inputs. Each methodology lands in its own follow-up
  # development that authors its agent/reference/character/template and appends the row
  # with `status: mvp`. See `plans/` for the candidate roadmap. MVP methodologies so far:
  #   - `thematic-analysis` (Braun & Clarke 2006, six-phase reflexive thematic
  #     analysis with a deductive coverage check against a fixed 10-area concern
  #     frame; self-contained HTML with a pre-rendered inline-SVG theme-map in
  #     #diagrams + an adjacent collapsed Mermaid-source export <details> + an
  #     embedded <pre><code class="language-json" id="thematic-analysis-body">
  #     model that survives the markitdown HTML->MD round-trip for /requirements
  #     re-ingestion).
  #   - `opportunity-solution-trees` (Teresa Torres 2016, four-layer discovery
  #     tree adapted for raw consultant inputs — forward discovery, vs the
  #     reverse-discovery sibling under /analyse-requirement; self-contained HTML
  #     with a pre-rendered layered SVG tree diagram (one <svg class="tree-svg">,
  #     nodes + edges in one viewBox coordinate space) in #diagrams + an
  #     adjacent collapsed Mermaid graph TD export <details>; carries a
  #     Candidate-requirements bridge plus an embedded
  #     <pre><code class="language-json" id="opportunity-solution-tree-body">
  #     model that `/requirements` consumes when the artefact is re-dropped into
  #     `input/` via the markitdown HTML->MD round-trip).
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
  #     `filename` field exactly; the artefact ships two visual surfaces
  #     plus a machine-readable body block: the canonical OOUX sticky-note
  #     column-board (CTAs, header, CCPs, metadata, nested refs — the object
  #     map, the rendered "MUST contain a diagram" deliverable), relationship
  #     matrix table, and a
  #     `<pre><code class="language-json" id="ooux-object-map-body">` block
  #     carrying the full object model in JSON for `/requirements`
  #     re-ingestion via markitdown round-trip — the load-bearing
  #     machine-readable contract for the downstream drafter; eight hard
  #     quality gates: seven inherited from the requirements-side OOUX
  #     reference (every Object has ≥1 CTA; every CTA attaches to exactly
  #     one Object; every nested Relationship declares cardinality; every
  #     Object has ≥1 CCP; no orphan Attributes; provenance markers
  #     exhaustive; matrix + nested refs agree) plus Gate 8
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
  #     processes per artefact, each rendered as a pre-rendered
  #     inline-SVG swim-lane (one lane per actor) with the Mermaid
  #     `flowchart TD` source kept as a collapsed export adjunct
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
  #     self-contained HTML with a pre-rendered inline-SVG swim-lane
  #     per process (Mermaid `flowchart TD` source kept as a collapsed
  #     `<pre class="mermaid-source">` export adjunct; no Mermaid
  #     runtime, no CDN), an
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
  #   - `business-context-definition` (Business Context Definition — an
  #     enterprise-motivation synthesis: OMG Business Motivation Model Ends
  #     (Vision / Goal / Objective) + IIBA BABOK Business Need (problem OR
  #     opportunity; underlying-cause-vs-symptom) + Five-Whys root-cause
  #     analysis + Gause & Weinberg problem-as-gap + Design-Thinking POV /
  #     "How Might We" reframing + KAOS AND/OR goal refinement kept at the
  #     enterprise tier; adapted for raw consultant inputs as a six-pass
  #     document-only extraction-AND-bounded-inference process. Surfaces the
  #     enterprise motivation behind the request — the Business Problem(s),
  #     Business Need(s), Business Goal(s) / Objective(s), and a human-centered
  #     Problem Statement — both EXPLICITLY stated and INFERRED, linked in a
  #     problem→need→goal→problem-statement causal chain. The four mandated
  #     artefacts are the four labelled sections of one self-contained HTML
  #     report: Business Needs Assessment, Business Problem Statement (with
  #     Five-Whys root-cause ladders), Business Goals collection (BMM-tiered
  #     CSS-only AND/OR tree), and a solution-neutral Problem Statement (POV +
  #     HMW). Explicit items carry [SRC: <filename>]; inferred items carry
  #     [AI-SUGGESTED: AI-NN | blocking|non-blocking] co-present with a named
  #     technique (five-whys-root-cause / bmm-laddering / opportunity-reframe /
  #     abductive-best-explanation / swot-influencer-inference / pov-hmw-reframe)
  #     AND ≥1 source anchor — anchorless inference forbidden (anti-confabulation
  #     gate Q2). Seven hard gates (Q1 provenance, Q2 anti-confabulation,
  #     Q3 classification, Q4 causal-chain integrity, Q5 well-formedness,
  #     Q6 enterprise-scope, Q7 coverage). ENTERPRISE-ONLY: actor / end-user
  #     goals are user-goal-analysis's exclusive lane — encountered actor goals
  #     are routed to a `deferred-to-user-goal-analysis` boundary-audit log
  #     (decision-tree D0 + gate Q6), never classified as Business Goals, so a
  #     consultant can run both methods on one input/ and get two clean,
  #     non-overlapping registers. Self-contained, dependency-free HTML (NO
  #     Mermaid): a CSS-only four-stage causal-chain map (diagram-first),
  #     need/problem/goal/problem-statement cards, a BMM AND/OR goal tree, a
  #     tensions table, and an embedded
  #     <pre><code class="language-json" id="bcd-body"> block carrying the full
  #     business-context model for /requirements re-ingestion via markitdown
  #     HTML→MD round-trip. Designed to be re-fed into /requirements —
  #     explicit Goals / Objectives / Needs seed the strategic framing (why each
  #     requirement exists), the causal chain seeds requirement→goal→need→problem
  #     traceability, the Problem Statement seeds scope framing, and inferred
  #     items surface to the resolver as AI-NNN questions (blocking ones as
  #     mandatory confirmations). Distinct from user-goal-analysis (ACTOR goals,
  #     Cooper types), opportunity-solution-trees (jumps to solutions), and
  #     five-whys (a bare cause chain) — BCD owns the enterprise
  #     problem→need→goal→problem-statement account and stops at the requirement
  #     boundary.
  #   - `glossary` (Glossary — establishing ONE agreed vocabulary, the project's
  #     ubiquitous language, for the system's specification and design: Evans 2003
  #     DDD ubiquitous language + bounded contexts + ISO 704 / ISO 1087 definition
  #     principles (genus-differentia, non-circularity, essential characteristics)
  #     + Berry & Kamsties ambiguity-vs-vagueness + Frantzi et al. 2000
  #     termhood/unithood term extraction adapted for small heterogeneous corpora
  #     via an LLM-as-extractor with a MANDATORY source-tuple per candidate (the
  #     traceability guard that replaces statistical confidence). Surfaces the
  #     significant terms across the raw inputs, classifies each domain (problem
  #     space) vs application (solution space), defines each from the inputs
  #     (cited [SRC: <filename>]), and rates shared-understanding maturity 0-4
  #     (Undefined / Implicit / Partial / Settled / Conflicting). DRIVES
  #     CONVERGENCE — for an L0/L1 term it proposes a candidate definition, for an
  #     L2 term a refinement, for a synonym cluster a canonical term + reconciling
  #     definition, for an L4 conflict a unify-or-context-split resolution — each
  #     rendered in a fenced .ai-proposal block marked
  #     [AI-SUGGESTED: AI-NNN | blocking] with a named technique
  #     (genus-differentia-synthesis / usage-context-abstraction /
  #     domain-analogue-mapping / synonym-merge / conflict-unify / context-split)
  #     and >=1 source anchor — never anchorless, never on a Settled (L3) term,
  #     never merged into the cited definition. This deliberately relaxes the
  #     requirements-side GLOSSARY's hard no-[AI-SUGGESTED] rule, bounded to this
  #     sanctioned, blocking, confirm-before-canon channel (the same channel
  #     task-analysis / user-goal-analysis / business-context-definition use), so
  #     it does not widen the framework-wide invariant. Ten hard gates (G1
  #     provenance, G2 anti-confabulation, G3 field-separation, G4 classification,
  #     G5 maturity/agreement, G6 lexical-presence, G7 canonical-convergence, G8
  #     additive-merge, G9 coverage, G10 self-containment). Self-contained,
  #     dependency-free HTML (NO Mermaid): alphabetical term cards with
  #     classification / maturity / agreement badges, five open-item registers
  #     (needs-definition / to-refine / to-reconcile / to-resolve /
  #     ambiguous-general), and an embedded
  #     <pre><code class="language-json" id="glossary-body"> block carrying the
  #     full term model that survives a markitdown HTML→MD round-trip for
  #     /requirements re-ingestion. Designed as a /requirements input: settled
  #     definitions become the canonical vocabulary the drafter adopts; the
  #     blocking proposals surface to the resolver as AI-NNN mandatory
  #     confirmations the consultant agrees before they anchor requirements.
  #     map_skill: null — a glossary is a vocabulary artefact, not a UI inventory;
  #     its consumer is /requirements, not a design-spec/wireframe author.)
  - name: glossary
    status: mvp
    group: Vocabulary & objects
    description: Choose this when you want one agreed vocabulary for the system's spec and design — the significant terms across your raw inputs surfaced, classified as domain or application terms, defined from the inputs, and rated for how settled each shared understanding is. It produces an HTML glossary that reads as a lookup reference — per-term cards with a domain/application badge, a 0-4 maturity badge, the cited definition, and, where the inputs leave a term undefined, weak, synonymous, or conflicting, a fenced proposed definition or canonical resolution for you to confirm. Re-drop it into input/ so /requirements adopts the agreed terms as canonical vocabulary and the blocking proposals reach the resolver as questions you confirm before they anchor requirements.
    output_path: analyse-inputs/GLOSSARY/glossary.html
    reference_asset: framework/assets/analyses-inputs/glossary-reference.md
    template_asset: framework/assets/analyses-inputs/template-glossary.html
    map_skill: null
    analyser_agent: framework/agents/analyses-inputs/glossary-analyser.md
    character: framework/assets/characters/glossary-inputs-analysis.md
  - name: task-analysis
    status: mvp
    group: Process & tasks
    description: Choose this when the raw inputs describe how users accomplish goals step by step and you want that procedure decomposed before /requirements drafts from it. It produces an HTML hierarchical task analysis — a numbered sub-goal and operation tree with a plan on every non-terminal and the data each step reads or writes. Re-drop the artefact into input/ so the drafter uses its structured tree as a completeness target and seeds acceptance-criteria branches and data entities from it.
    output_path: analyse-inputs/TASK-ANALYSIS/task-analysis.html
    reference_asset: framework/assets/analyses-inputs/task-analysis-reference.md
    template_asset: framework/assets/analyses-inputs/template-task-analysis.html
    map_skill: framework/skills/map-task-analysis-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/task-analysis-analyser.md
    character: framework/assets/characters/task-analysis-inputs-analysis.md
  - name: thematic-analysis
    status: mvp
    group: Synthesis & themes
    description: Choose this when your raw inputs are unstructured — interviews, notes, decks — and you want the recurring patterns surfaced before drafting requirements. It produces a self-contained HTML report of the codes and themes the inputs carry, with a pre-rendered theme-map diagram, candidate requirements bridged from each theme, and an embedded machine-readable model. Re-drop it into input/ so /requirements drafts from the themes, or use it yourself to sanity-check coverage.
    output_path: analyse-inputs/THEMATIC-ANALYSIS/thematic-analysis.html
    reference_asset: framework/assets/analyses-inputs/thematic-analysis-reference.md
    template_asset: framework/assets/analyses-inputs/template-thematic-analysis.html
    map_skill: framework/skills/map-thematic-analysis-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/thematic-analysis-analyser.md
    character: framework/assets/characters/thematic-analysis-inputs-analysis.md
  - name: opportunity-solution-trees
    status: mvp
    group: Users, goals & value
    description: Choose this when the raw inputs name a desired outcome and you want the opportunities and solution options mapped before requirements lock in. It produces a self-contained HTML discovery tree of outcome → opportunities → solutions → assumption tests (Torres 2016), with a pre-rendered tree diagram, candidate-requirement seeds, and an embedded machine-readable model. Re-drop it into input/ so /requirements picks up the seeds, and use the assumption tests to decide what to validate first.
    output_path: analyse-inputs/OPPORTUNITY-SOLUTION-TREES/opportunity-solution-tree.html
    reference_asset: framework/assets/analyses-inputs/opportunity-solution-trees-reference.md
    template_asset: framework/assets/analyses-inputs/template-opportunity-solution-trees.html
    map_skill: framework/skills/map-opportunity-solution-trees-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/opportunity-solution-trees-analyser.md
    character: framework/assets/characters/opportunity-solution-trees-inputs-analysis.md
  - name: journey-mapping
    status: mvp
    group: Users, goals & value
    description: Choose this when the raw inputs describe an as-is workflow and you want it mapped per persona before drafting task flows and NFRs. It produces an HTML journey card per persona — phases, steps, touchpoints, channels, sentiment curve, pain points, and opportunities. Hand it to /requirements as a backbone for task flows, integrations, and user stories, and use the pain points to set priorities.
    output_path: analyse-inputs/JOURNEY-MAPPING/journey-mapping.html
    reference_asset: framework/assets/analyses-inputs/journey-mapping-reference.md
    template_asset: framework/assets/analyses-inputs/template-journey-mapping.html
    map_skill: framework/skills/map-journey-mapping-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/journey-mapping-analyser.md
    character: framework/assets/characters/journey-mapping-inputs-analysis.md
  - name: jtbd
    status: mvp
    group: Users, goals & value
    description: Choose this when you want the requirements anchored to user motivation, drawn from what the raw inputs say about why users act. It produces an HTML job map of the jobs, outcomes, and forces of progress (push / pull / anxiety / habit) the inputs describe, with opportunity scores (importance vs satisfaction — which jobs are most underserved). Re-drop it into input/ as a Native-text source so the requirements that follow target jobs and outcomes rather than features.
    output_path: analyse-inputs/JTBD/jtbd-job-map.html
    reference_asset: framework/assets/analyses-inputs/jtbd-reference.md
    template_asset: framework/assets/analyses-inputs/template-jtbd.html
    map_skill: framework/skills/map-jtbd-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/jtbd-analyser.md
    character: framework/assets/characters/jtbd-inputs-analysis.md
  - name: ooux
    status: mvp
    group: Vocabulary & objects
    description: Choose this when your raw inputs span many sources and you need one reconciled object model — merging synonyms like Customer, Client, and Account holder — before requirements. It produces an HTML object map combining a sticky-note column-board and an embedded machine-readable object model, with every object tagged by source. Re-drop it into input/ so /requirements ingests the full object model in one pass, and review the synonym-merge log to confirm the cross-source identity calls.
    output_path: analyse-inputs/OOUX/ooux-object-map.html
    reference_asset: framework/assets/analyses-inputs/ooux-reference.md
    template_asset: framework/assets/analyses-inputs/template-ooux.html
    map_skill: framework/skills/map-ooux-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/ooux-analyser.md
    character: framework/assets/characters/ooux-inputs-analysis.md
  - name: swim-lane-process-mapping
    status: mvp
    group: Process & tasks
    description: Choose this when the raw inputs describe a cross-functional process and you want the actor handoffs and their gaps surfaced before drafting. It produces an HTML set of Rummler-Brache swim-lane flowcharts plus a Disconnect Register classifying every lane-to-lane handoff as clean or defective (the "white-space" gaps Rummler attributed 80% of process failures to). Re-drop it into input/ so processes seed task flows and handoffs seed integration constraints, and chase the flagged handoff gaps with stakeholders.
    output_path: analyse-inputs/SWIM-LANE-PROCESS-MAPPING/swim-lane-process-mapping.html
    reference_asset: framework/assets/analyses-inputs/swim-lane-process-mapping-reference.md
    template_asset: framework/assets/analyses-inputs/template-swim-lane-process-mapping.html
    map_skill: framework/skills/map-swim-lane-process-mapping-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/swim-lane-process-mapping-analyser.md
    character: framework/assets/characters/swim-lane-process-mapping-inputs-analysis.md
  - name: affinity-mapping
    status: mvp
    group: Synthesis & themes
    description: Choose this when you have a large, messy pile of raw notes and want them clustered bottom-up into themes before imposing any structure. It produces an HTML affinity diagram — atomic notes grouped into labelled clusters and 4–8 super-themes, with orphans and cross-cluster tensions called out. Re-drop it into input/ so super-themes seed vision anchors and clusters seed task-flow groupings, and use the orphans as out-of-scope candidates.
    output_path: analyse-inputs/AFFINITY-MAPPING/affinity-map.html
    reference_asset: framework/assets/analyses-inputs/affinity-mapping-reference.md
    template_asset: framework/assets/analyses-inputs/template-affinity-mapping.html
    map_skill: framework/skills/map-affinity-mapping-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/affinity-mapping-analyser.md
    character: framework/assets/characters/affinity-mapping-inputs-analysis.md
  - name: user-goal-analysis
    status: mvp
    group: Users, goals & value
    description: Choose this when you want the actor and end-user goals behind the request made explicit — both the goals the inputs state and the ones they imply. It produces an HTML goal register grouped by goal type, with an AND/OR refinement tree, an actor map, and a conflicts table, and inferred goals flagged for confirmation. Re-drop it into input/ so explicit goals seed user stories and inferred goals reach the resolver as questions you confirm before they become requirements.
    output_path: analyse-inputs/USER-GOAL-ANALYSIS/user-goal-analysis.html
    reference_asset: framework/assets/analyses-inputs/user-goal-analysis-reference.md
    template_asset: framework/assets/analyses-inputs/template-user-goal-analysis.html
    map_skill: framework/skills/map-user-goal-analysis-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/user-goal-analysis-analyser.md
    character: framework/assets/characters/user-goal-analysis-inputs-analysis.md
  - name: business-context-definition
    status: mvp
    group: Business context
    description: Choose this when you need the enterprise motivation behind the request — the business problems, needs, and goals — rather than the individual actor goals user-goal-analysis covers. It produces an HTML report linking business problem → need → goal → problem-statement in one causal chain, with inferred items flagged for confirmation. Re-drop it into input/ so the chain seeds strategic framing and requirement traceability, and run user-goal-analysis alongside it for actor-level goals.
    output_path: analyse-inputs/BUSINESS-CONTEXT-DEFINITION/business-context-definition.html
    reference_asset: framework/assets/analyses-inputs/business-context-definition-reference.md
    template_asset: framework/assets/analyses-inputs/template-business-context-definition.html
    map_skill: framework/skills/map-business-context-definition-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/business-context-definition-analyser.md
    character: framework/assets/characters/business-context-definition-inputs-analysis.md
---

# analyses-inputs/registry.md

**Purpose:** Methodology registry for `/analyse-inputs`. Sibling of `framework/assets/analyses/registry.md`. The frontmatter above is the **machine-readable** contract — `framework/skills/analysis-selector.md` filters `status == "mvp"` to present options to the consultant when invoked with `registry_path: "framework/assets/analyses-inputs/registry.md"`; `framework/orchestrators/analyse-inputs-orch.md` looks up `analyser_agent` for the chosen methodology and invokes it at step 3.

**Source material:** unlike `/analyse-requirement` (whose analysers read `requirements/requirements.md`), methodologies registered here operate over the raw consultant-dropped material in `input/`, enumerated via `requirements/source-manifest.json`. The shared `framework/agents/input-handler.md` builds the manifest on demand at the orchestrator's step 1.

**Used by:**

- `framework/skills/analysis-selector.md` — reads MVP-status rows; presents them as a printed numbered list clustered by `group`, with `★ suggested next` / `✓ already run` marks derived from each row's `output_path` presence on disk.
- `framework/orchestrators/analyse-inputs-orch.md` — reads the chosen row's `analyser_agent` and `output_path` to drive invocation and the prior-artefact gate.
- `framework/agents/analyses-inputs/<method>-analyser.md` — each analyser reads its own `reference_asset`, `character`, and `template_asset` paths at activation. No analyser file exists on disk until its row has been promoted to `status: mvp`.

**Adding a new methodology (per-PR steps):**

1. Pick a candidate from `plans/` (see `plans/README.md` for the roadmap) and follow its build checklist, or author a brand-new methodology. The row is appended with `status: mvp` at step 7.
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
5. (Optional) Author the template asset at `framework/assets/analyses-inputs/template-<method>.html`. Set `template_asset: null` only for methodologies that emit pure Markdown without a scaffold. (As of the HTML migration, every MVP methodology populates an `.html` scaffold — no MVP row currently ships `template_asset: null`.)
6. (Optional) Author the map-skill at `framework/skills/map-<method>-from-inputs-to-ui.md` — or reuse `framework/skills/map-<method>-to-ui.md` if the mapping is source-agnostic.
7. Append the registry row with `status: mvp` and populate all remaining fields (`description`, `output_path`, `reference_asset`, `template_asset`, `map_skill`, `analyser_agent`, `character`, and the optional `group` — assign a lens group; omitting it drops the row into a trailing `Other` group). `output_path` lives under `analyse-inputs/<METHOD>/` (uppercase methodology name) — e.g. `analyse-inputs/GLOSSARY/glossary.html`.
8. Add the analyser node to graph 5 in `framework/dependency-graphs.md`.
9. No orchestrator changes required — the selector skill picks the new MVP row up automatically.

**Field semantics:**

- `name` — kebab-case slug. Used as the subdirectory name under `analyse-inputs/` (uppercased to `analyse-inputs/<METHOD>/`) and as the path component in the analyser agent file. Methodology slugs are shared across registries (a row named `glossary` can exist in both `analyses/registry.md` and `analyses-inputs/registry.md`); the artefacts do not clobber because the output paths differ (`analyse-requirements/GLOSSARY/...` vs `analyse-inputs/GLOSSARY/...`).
- `status` — currently always `mvp`. The selector filters to `status == mvp` defensively; planned, not-yet-built methodologies live in `plans/`, not as registry rows.
- `group` — optional lens-group label (e.g. `Users, goals & value`, `Process & tasks`). The selector clusters MVP rows by this value (groups in first-appearance order, registry order preserved within each group) and renders it as a header. Rows with no `group` fall into a trailing `Other` group. Consultant-facing — keep it short and human-readable.
- `description` — short consultant-facing blurb surfaced in the selector's printed list, written as three succinct sentences (why/when to choose it → what it produces → how to use the output). Required only when `status: mvp`.
- `output_path` — relative path of the artefact the analyser writes. Drives the prior-artefact gate in the orchestrator. **Must** live under `analyse-inputs/` for write-isolation. Required only when `status: mvp`.
- `reference_asset` — the methodology reference the analyser follows. Required only when `status: mvp`.
- `template_asset` — file scaffold the analyser populates (may be `null` for methodologies that emit pure Markdown).
- `map_skill` — translates the analysis output into UI inventory entries for downstream design consumption. May reuse the existing `framework/skills/map-<method>-to-ui.md` if source-agnostic, or be a sibling `map-<method>-from-inputs-to-ui.md` if the mapping diverges. Not invoked by `/analyse-inputs`.
- `analyser_agent` — the foreground agent invoked by the orchestrator. Required only when `status: mvp`.
- `character` — stance the Unicorn adopts while running the analyser. Required only when `status: mvp`.

**Empty-MVP behaviour:** when the registry has no `status: mvp` rows the selector returns `empty-registry` and the orchestrator surfaces a friendly "no input analyses available yet" message and exits cleanly. With `task-analysis`, `thematic-analysis`, `opportunity-solution-trees`, `journey-mapping`, `jtbd`, `ooux`, `swim-lane-process-mapping`, `affinity-mapping`, `user-goal-analysis`, `business-context-definition`, and `glossary` at `status: mvp`, the selector presents eleven options to the consultant. This is a defensive guard; were every MVP row removed it would resume — it is not an error.
