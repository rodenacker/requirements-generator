---
role: asset
kind: registry
methodologies:
  # MVP — fully implemented and selectable via /review-requirement. Curated order + `group`
  # drive the selector's lens grouping + `★ suggested next` flag (see framework/skills/analysis-selector.md).
  - name: adversarial
    status: mvp
    group: Document integrity
    description: Choose this when you want the requirements stress-tested for defects so design starts from a patched document rather than inherited weaknesses. It produces a self-contained HTML critique flagging contradictions, gaps, ambiguities, and risky assumptions across the document, with each finding rated against the system's frontend purpose so backend-only concerns are still raised but never block a frontend spec. Work the flagged defects back into requirements.md before design or estimation begins.
    output_path: review-requirements/ADVERSARIAL/adversarial-review.html
    reference_asset: framework/assets/reviews/adversarial-reference.md
    template_asset: framework/assets/reviews/template-adversarial.html
    map_skill: null
    reviewer_agent: framework/agents/reviews/adversarial-reviewer.md
    character: framework/assets/characters/adversarial-review.md
  - name: first-principles
    status: mvp
    group: Document integrity
    description: Choose this when you suspect some requirements were carried over by habit and want each tested against its business rationale. It produces a self-contained HTML review judging whether each requirement is defensible from first principles, marking the weak ones. Cut or strengthen the flagged items before they reach design.
    output_path: review-requirements/FIRST-PRINCIPLES/first-principles-review.html
    reference_asset: framework/assets/reviews/first-principles-reference.md
    template_asset: framework/assets/reviews/template-first-principles.html
    map_skill: null
    reviewer_agent: framework/agents/reviews/first-principles-reviewer.md
    character: framework/assets/characters/first-principles-review.md
  - name: ten-ba-questions
    status: mvp
    group: Stakeholder & BA gaps
    description: Choose this before design or estimation when you want the most consequential business-analysis gaps named rather than a full critique. It produces a self-contained HTML list of the ten most pressing stakeholder questions the requirements leave unanswered. Take the ten questions to your stakeholders and fold the answers back into the document.
    output_path: review-requirements/TEN-BA-QUESTIONS/ten-ba-questions-review.html
    reference_asset: framework/assets/reviews/ten-ba-questions-reference.md
    template_asset: framework/assets/reviews/template-ten-ba-questions.html
    map_skill: null
    reviewer_agent: framework/agents/reviews/ten-ba-questions-reviewer.md
    character: framework/assets/characters/ten-ba-questions-review.md
  - name: ten-ux-questions
    status: mvp
    group: UX gaps
    description: Choose this before designing screens when you want the sharpest UX unknowns surfaced so you don't design against gaps. It produces a self-contained HTML list of the ten most pressing UX questions the requirements leave unanswered. Resolve the ten questions before wireframing, or carry them into design as explicit assumptions.
    output_path: review-requirements/TEN-UX-QUESTIONS/ten-ux-questions-review.html
    reference_asset: framework/assets/reviews/ten-ux-questions-reference.md
    template_asset: framework/assets/reviews/template-ten-ux-questions.html
    map_skill: null
    reviewer_agent: framework/agents/reviews/ten-ux-questions-reviewer.md
    character: framework/assets/characters/ten-ux-questions-review.md
  - name: user-stories
    status: mvp
    group: Backlog readiness
    description: Choose this when you need to know which user stories aren't ready for design or estimation before they enter the backlog. It produces a self-contained HTML review judging each story against readiness criteria and flagging the ones that fall short. Rework the flagged stories until they're ready, then admit them to the backlog.
    output_path: review-requirements/USER-STORIES/user-stories-review.html
    reference_asset: framework/assets/reviews/user-stories-reference.md
    template_asset: framework/assets/reviews/template-user-stories.html
    map_skill: null
    reviewer_agent: framework/agents/reviews/user-stories-reviewer.md
    character: framework/assets/characters/user-stories-review.md
  - name: requirements-quality
    status: mvp
    group: Document integrity
    description: Choose this before design or estimation when you want every requirement scored against the ISO/IEC/IEEE 29148 well-formedness standard (singular, unambiguous, verifiable, conforming, complete) with the four judgment characteristics fenced separately, rather than a freeform critique. It produces a self-contained HTML requirement-by-characteristic heatmap with a risk-tier distribution, a set-level consistency and redundancy register, and a fix list that rewrites the ambiguous and compound requirements into EARS form. Work the Red-tier requirements up to standard before they reach design, and read the per-characteristic tally to see which weakness dominates.
    output_path: review-requirements/REQUIREMENTS-QUALITY/requirements-quality.html
    reference_asset: framework/assets/reviews/requirements-quality-reference.md
    template_asset: framework/assets/reviews/template-requirements-quality.html
    map_skill: null
    reviewer_agent: framework/agents/reviews/requirements-quality-reviewer.md
    character: framework/assets/characters/requirements-quality-review.md
  - name: requirements-traceability
    status: mvp
    group: Document integrity
    description: Choose this before the requirements feed design or code-gen when you want to know which facts trace back to a real input source or an accepted AI-suggestion — and which trace to nothing. It produces a self-contained HTML audit that leads with the untraceable result (orphans, broken citations, and content the consultant dropped that leaked through), backed by a deterministic citation check and a requirement-by-trace-target heatmap. Resolve the flagged orphans and broken citations — supply the missing source, re-confirm the dropped value, or remove the claim — before the document is trusted downstream.
    output_path: review-requirements/REQUIREMENTS-TRACEABILITY/requirements-traceability.html
    reference_asset: framework/assets/reviews/requirements-traceability-reference.md
    template_asset: framework/assets/reviews/template-requirements-traceability.html
    map_skill: null
    reviewer_agent: framework/agents/reviews/requirements-traceability-reviewer.md
    character: framework/assets/characters/requirements-traceability-review.md
---

# reviews/registry.md

**Purpose:** Methodology registry for `/review-requirement`. The frontmatter above is the **machine-readable** contract — `framework/skills/analysis-selector.md` (invoked with `list_label: "reviews"`, `verb_label: "review"`) filters `status == "mvp"` to present options to the consultant, clustered by `group` with the next un-run review flagged `★ suggested next`; `framework/orchestrators/review-requirement-orch.md` looks up `reviewer_agent` for the chosen methodology and invokes it. (The former pipeline-private `review-selector.md` was retired — `/review-requirement` now shares the methodology-neutral `analysis-selector` with the other three selector pipelines.)

This registry is structurally identical to `framework/assets/analyses/registry.md` (which drives `/analyse-requirement`) so the two pipelines share the same registry-driven, open/closed extension contract. The semantic distinction is the *intent* of the output: `/analyse-requirement` produces derived structural models (object maps, job maps, use-case maps) that downstream design phases consume; `/review-requirement` produces critique reports flagging defects, gaps, ambiguities, and risks in `requirements/requirements.md` itself.

**Used by:**

- `framework/skills/analysis-selector.md` — reads MVP-status rows; presents them as a printed numbered list clustered by `group`, with `★ suggested next` / `✓ already run` marks. Invoked with `list_label: "reviews"`, `verb_label: "review"`.
- `framework/orchestrators/review-requirement-orch.md` — reads the chosen row's `reviewer_agent` and `output_path` to drive invocation and the prior-artefact gate.
- `framework/agents/reviews/<method>-reviewer.md` — each reviewer reads its own `reference_asset`, `character`, and `template_asset` paths at activation.

**Adding a new methodology:**

1. Pick a candidate from `plans/` (see `plans/README.md` for the roadmap) and follow its build checklist — its "Turning this into a plan" section mirrors these steps — or author a brand-new methodology not yet in `plans/`.
2. Append the row to the frontmatter with `status: mvp` and populate the fields: `name`, `status`, `description`, `output_path`, `reference_asset`, `template_asset` (may be `null`), `map_skill` (typically `null` for reviews — reviews don't feed UI inventory), `reviewer_agent`, `character`, and the optional `group` (assign a lens group; omitting it drops the row into a trailing `Other` group). Place the row at its best-practice position within its group so the selector's `★ suggested next` flag stays sensible.
3. Author the reviewer agent, the reference asset, the character file, and (if needed) the template asset.
4. No orchestrator changes required — the selector skill picks the new row up automatically.

**Field semantics:**

- `name` — kebab-case slug. Used as the basis for the subdirectory name under `review-requirements/` (uppercased, e.g. `adversarial` → `review-requirements/ADVERSARIAL/`) and as the path component in the reviewer agent file.
- `status` — currently always `mvp`. The selector filters to `status == mvp` defensively (discarding any row whose status is absent or non-`mvp`); planned, not-yet-built methodologies live in `plans/`, not as registry rows.
- `group` — optional lens-group label (e.g. `Document integrity`, `UX gaps`). The selector clusters MVP rows by this value (groups in first-appearance order, registry order preserved within each group) and renders it as a header. Rows with no `group` fall into a trailing `Other` group. Consultant-facing — keep it short and human-readable.
- `description` — short consultant-facing blurb surfaced in the selector's printed list, written as three succinct sentences (why/when to choose it → what it produces → how to use the output).
- `output_path` — relative path of the artefact the reviewer writes. Drives the prior-artefact gate in the orchestrator.
- `reference_asset` — the methodology reference the reviewer follows.
- `template_asset` — file scaffold the reviewer populates (may be `null` for methodologies that emit pure Markdown without placeholders).
- `map_skill` — present for parity with `analyses/registry.md`; almost always `null` for reviews because reviews don't translate into UI inventory.
- `reviewer_agent` — the foreground agent invoked by the orchestrator.
- `character` — stance the Unicorn adopts while running the reviewer.

## Why a separate registry from `analyses/registry.md`?

Reviews and analyses are categorically different outputs:

- An **analysis** *transforms* requirements into a derived structural model (objects, jobs, use cases) — its output is consumed by downstream design phases as a positive contract.
- A **review** *critiques* the requirements document for defects — its output is consumed by the consultant as a punch-list to fix the requirements doc itself.

Folding reviews into the analyses registry would:

- Muddy the consultant's choice list (the `/analyse-requirement` selector would show "Adversarial Review" alongside "OOUX" as if they were peers, when they have opposite semantics — one builds *from* the doc, the other critiques *the* doc).
- Complicate the stand-alone write invariant: analyses write to `analyse-requirements/<METHOD>/`; reviews must write to `review-requirements/<METHOD>/`. A single registry would need a per-row output-root field, replacing a clear two-pipeline split with a more brittle multiplexed one.
- Break the natural mapping `slash-command → orchestrator → registry`. Two commands, two orchestrators, two registries is the right cardinality.

The cost of duplication is one selector skill and one orchestrator — both clone the `/analyse-requirement` versions verbatim with path swaps. The benefit is clean semantic separation between *building from* and *critiquing of* the requirements doc.
