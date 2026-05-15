---
role: asset
kind: registry
methodologies:
  # MVP — fully implemented and selectable via /review. Listed alphabetically; none privileged.
  - name: adversarial
    status: mvp
    description: Adversarial review of requirements.md (BMAD-style, strict mode — must find issues, eight review dimensions, Patch/Defer/Reject disposition)
    output_path: reviews/ADVERSARIAL/adversarial-review.md
    reference_asset: framework/assets/reviews/adversarial-reference.md
    template_asset: framework/assets/reviews/template-adversarial.md
    map_skill: null
    reviewer_agent: framework/agents/reviews/adversarial-reviewer.md
    character: framework/assets/characters/adversarial-review.md
  - name: ten-ux-questions
    status: mvp
    description: 10 UX Questions — the most pressing unanswered questions an experienced UX designer would ask after reading requirements.md (priority — blocking / major / minor; final 10 selected from a candidate pool of up to 50; eight UX gap categories)
    output_path: reviews/TEN-UX-QUESTIONS/ten-ux-questions-review.md
    reference_asset: framework/assets/reviews/ten-ux-questions-reference.md
    template_asset: framework/assets/reviews/template-ten-ux-questions.md
    map_skill: null
    reviewer_agent: framework/agents/reviews/ten-ux-questions-reviewer.md
    character: framework/assets/characters/ten-ux-questions-review.md
  # Future — stub-only; no reviewer agent on disk. Promote by flipping status, populating
  # the remaining fields, and authoring the reviewer + reference + character + template.
  - { name: stakeholder-review, status: future }
  - { name: compliance-review, status: future }
  - { name: mvp-scope-review, status: future }
  - { name: feasibility-review, status: future }
  - { name: accessibility-review, status: future }
  - { name: security-review, status: future }
  - { name: testability-review, status: future }
  - { name: data-model-review, status: future }
  - { name: rbac-review, status: future }
  - { name: premortem, status: future }
  - { name: six-thinking-hats, status: future }
  - { name: wiegers-inspection, status: future }
  - { name: invest-story-review, status: future }
---

# reviews/registry.md

**Purpose:** Methodology registry for `/review`. The frontmatter above is the **machine-readable** contract — `framework/skills/review-selector.md` filters `status == "mvp"` to present options to the consultant; `framework/orchestrators/review-orch.md` looks up `reviewer_agent` for the chosen methodology and invokes it.

This registry is structurally identical to `framework/assets/analyses/registry.md` (which drives `/analyse`) so the two pipelines share the same registry-driven, open/closed extension contract. The semantic distinction is the *intent* of the output: `/analyse` produces derived structural models (object maps, job maps, use-case maps) that downstream design phases consume; `/review` produces critique reports flagging defects, gaps, ambiguities, and risks in `requirements/requirements.md` itself.

**Used by:**

- `framework/skills/review-selector.md` — reads MVP-status rows; presents them via `AskUserQuestion`.
- `framework/orchestrators/review-orch.md` — reads the chosen row's `reviewer_agent` and `output_path` to drive invocation and the prior-artefact gate.
- `framework/agents/reviews/<method>-reviewer.md` — each reviewer reads its own `reference_asset`, `character`, and `template_asset` paths at activation.

**Adding a new methodology:**

1. Append a row to the frontmatter (or flip an existing `future` row to `mvp`).
2. Populate all eight fields: `name`, `status`, `description`, `output_path`, `reference_asset`, `template_asset` (may be `null`), `map_skill` (typically `null` for reviews — reviews don't feed UI inventory), `reviewer_agent`, `character`.
3. Author the reviewer agent, the reference asset, the character file, and (if needed) the template asset.
4. No orchestrator changes required — the selector skill picks the new row up automatically.

**Field semantics:**

- `name` — kebab-case slug. Used as the basis for the subdirectory name under `reviews/` (uppercased, e.g. `adversarial` → `reviews/ADVERSARIAL/`) and as the path component in the reviewer agent file.
- `status` — `mvp` (selectable now) or `future` (not yet built).
- `description` — one-line label surfaced in the `AskUserQuestion` choice list.
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

- Muddy the consultant's choice list (the `/analyse` selector would show "Adversarial Review" alongside "OOUX" as if they were peers, when they have opposite semantics — one builds *from* the doc, the other critiques *the* doc).
- Complicate the stand-alone write invariant: analyses write to `analyses/<METHOD>/`; reviews must write to `reviews/<METHOD>/`. A single registry would need a per-row output-root field, replacing a clear two-pipeline split with a more brittle multiplexed one.
- Break the natural mapping `slash-command → orchestrator → registry`. Two commands, two orchestrators, two registries is the right cardinality.

The cost of duplication is one selector skill and one orchestrator — both clone the `/analyse` versions verbatim with path swaps. The benefit is clean semantic separation between *building from* and *critiquing of* the requirements doc.
