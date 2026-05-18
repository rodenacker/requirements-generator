---
role: asset
kind: registry
methodologies:
  # Methodologies for /review-inputs. Each methodology ships as a separate development,
  # promoting `status: future` to `status: mvp` and filling in the remaining eight fields.
  # The `adversarial` row is the first MVP — a BMAD-style seven-dimension critique of
  # the raw consultant input set, paralleling the eight-dimension /review-requirement
  # adversarial reviewer with dimensions tuned for input-set defects (stakeholder
  # coverage, workflow coverage, ambiguity, cross-source conflict, quantitative signal,
  # scope signal, sampling bias). Additional `status: future` rows below become
  # operational only when their reviewer / reference / character / template files are
  # authored and the row's status is flipped to `mvp`. If every MVP row were removed,
  # the selector returns `empty-registry` and the orchestrator surfaces a friendly
  # "no input reviews available yet" message and exits cleanly.
  #
  # Slug-collision note: methodology slugs are shared across registries (a row named
  # `completeness` could exist in both `reviews-inputs/registry.md` and
  # `reviews/registry.md`); the artefacts do not clobber because the output paths
  # differ (`review-inputs/COMPLETENESS/...` vs `review-requirements/COMPLETENESS/...`).
  - name: adversarial
    status: mvp
    description: Choose this to flush out defects in the raw consultant inputs (stakeholder gaps, ambiguity, cross-source conflicts, missing edge cases, sampling bias) before /requirements drafts from them.
    output_path: review-inputs/ADVERSARIAL/adversarial-review.md
    reference_asset: framework/assets/reviews-inputs/adversarial-reference.md
    template_asset: framework/assets/reviews-inputs/template-adversarial.md
    map_skill: null
    reviewer_agent: framework/agents/reviews-inputs/adversarial-reviewer.md
    character: framework/assets/characters/adversarial-inputs-review.md
  - { name: completeness-review, status: future }
  - name: ambiguity-review
    status: mvp
    description: Choose this to surface lexical, syntactic, referential, vague, subjective, weak-verb, and optionality ambiguities in the raw consultant inputs (Berry/Kamsties + Femmer taxonomy) — with ready-to-paste stakeholder elicitation questions per finding — before /requirements drafts from them.
    output_path: review-inputs/AMBIGUITY-REVIEW/ambiguity-review.md
    reference_asset: framework/assets/reviews-inputs/ambiguity-reference.md
    template_asset: null
    map_skill: null
    reviewer_agent: framework/agents/reviews-inputs/ambiguity-reviewer.md
    character: framework/assets/characters/ambiguity-inputs-review.md
---

# reviews-inputs/registry.md

**Purpose:** Methodology registry for `/review-inputs`. Sibling of `framework/assets/reviews/registry.md` (which drives `/review-requirement`) and of `framework/assets/analyses-inputs/registry.md` (which drives `/analyse-inputs`). The frontmatter above is the **machine-readable** contract — `framework/skills/analysis-selector.md` filters `status == "mvp"` to present options to the consultant when invoked with `registry_path: "framework/assets/reviews-inputs/registry.md"`; `framework/orchestrators/review-inputs-orch.md` looks up `reviewer_agent` for the chosen methodology and invokes it at step 3.

**Source material:** like `/analyse-inputs` (and unlike `/review-requirement`, whose reviewers read `requirements/requirements.md`), methodologies registered here operate over the raw consultant-dropped material in `input/`, enumerated via `requirements/source-manifest.json`. The shared `framework/agents/input-handler.md` builds the manifest on demand at the orchestrator's step 1.

**Pipeline cleavage:**

- `/analyse-inputs` *transforms* raw inputs into derived structural models (theme maps, opportunity-solution trees) that downstream design phases consume as positive contracts.
- `/review-inputs` *critiques* raw inputs themselves — flagging gaps, ambiguities, conflicts, completeness defects, stakeholder-coverage holes — producing punch-lists the consultant uses to chase missing material before drafting requirements.

Folding input-reviews into the analyses-inputs registry would muddy the consultant's choice list (the `/analyse-inputs` selector would show "Completeness Review" alongside "Thematic Analysis" as if they were peers, when they have opposite semantics). Two commands, two orchestrators, two registries — the same cardinality used by the `/analyse-requirement` / `/review-requirement` split.

**Used by:**

- `framework/skills/analysis-selector.md` — reads MVP-status rows; presents them via the numbered-list prompt. The skill is methodology-neutral and pipeline-neutral; `/review-inputs` is its third caller (after `/analyse-requirement` and `/analyse-inputs`). The caller passes `list_label: "reviews"` and `verb_label: "review"` so the printed prompt reads naturally for reviewing rather than analysing.
- `framework/orchestrators/review-inputs-orch.md` — reads the chosen row's `reviewer_agent` and `output_path` to drive invocation and the prior-artefact gate.
- `framework/agents/reviews-inputs/<method>-reviewer.md` — each reviewer reads its own `reference_asset`, `character`, and `template_asset` paths at activation. No reviewer file exists on disk until its row has been promoted to `status: mvp`.

**Adding a new methodology (per-PR steps):**

1. Pick a planned row (e.g. `{ name: completeness-review, status: future }`) or append a new one.
2. Author the reviewer agent at `framework/agents/reviews-inputs/<method>-reviewer.md`. Each reviewer:
    - Reads `requirements/source-manifest.json` once at its source-enumeration step.
    - For each manifest row where `tier != "Unsupported"`: Read the file at `original_path` (for `Native-text` and `Native-multimodal`) or `converted_sibling` (for `Supported-via-MCP`). For `Native-multimodal`, the Read tool surfaces image bytes as multimodal input automatically.
    - Skips manifest rows with `tier == "Unsupported"` and records the reason in the artefact's diagnostics block.
    - Cites source-of-fact in the artefact body using `[SRC: <filename>]` markers (filename payload, matching the `/analyse-inputs` convention; not the `/requirements` pipeline's `C-NNN` sidecar IDs).
    - Records a source-roster section in the artefact listing every filename consumed and every skipped filename with reason.
    - Records a manifest-fingerprint field in the artefact (the manifest's sha256, or sha256 of its serialised bytes) so the artefact captures exactly which manifest version it reviewed.
    - Self-validates: every manifest row with `tier != "Unsupported"` was Read or skipped-with-reason; the artefact reads no path under `requirements/` other than `requirements/source-manifest.json`; the artefact reads no path under `framework/state/` or `framework/shared/`.
3. Author the reference asset at `framework/assets/reviews-inputs/<method>-reference.md` (methodology rules and patterns).
4. Author the character file at `framework/assets/characters/<method>-inputs-review.md` (Unicorn stance during the reviewer run).
5. (Optional) Author the template asset at `framework/assets/reviews-inputs/template-<method>.{html,md}`. Set `template_asset: null` for methodologies that emit pure Markdown without a scaffold.
6. Promote the registry row: flip `status: future` to `status: mvp` and populate all remaining fields (`description`, `output_path`, `reference_asset`, `template_asset`, `map_skill`, `reviewer_agent`, `character`). `output_path` lives under `review-inputs/<METHOD>/` (uppercase methodology name) — e.g. `review-inputs/COMPLETENESS-REVIEW/completeness-review.md`.
7. Add the reviewer node to graph 6 in `framework/dependency-graphs.md`.
8. No orchestrator changes required — the selector skill picks the new MVP row up automatically.

**Field semantics:**

- `name` — kebab-case slug. Used as the subdirectory name under `review-inputs/` (uppercased to `review-inputs/<METHOD>/`) and as the path component in the reviewer agent file. Methodology slugs are shared across registries; the artefacts do not clobber because the output paths differ.
- `status` — `mvp` (selectable now) or `future` (not yet built; reviewer / reference / character / template files do not exist on disk).
- `description` — one-line label surfaced in the selector's printed list. Required only when `status: mvp`.
- `output_path` — relative path of the artefact the reviewer writes. Drives the prior-artefact gate in the orchestrator. **Must** live under `review-inputs/` for write-isolation. Required only when `status: mvp`.
- `reference_asset` — the methodology reference the reviewer follows. Required only when `status: mvp`.
- `template_asset` — file scaffold the reviewer populates (may be `null` for methodologies that emit pure Markdown).
- `map_skill` — present for parity with `analyses-inputs/registry.md`; **almost always `null`** for reviews because reviews don't translate into UI inventory. Mirrors the `reviews/registry.md` convention.
- `reviewer_agent` — the foreground agent invoked by the orchestrator. Required only when `status: mvp`.
- `character` — stance the Unicorn adopts while running the reviewer. Required only when `status: mvp`.

**Empty-MVP behaviour:** when every row has `status: future` the selector returns `empty-registry` and the orchestrator surfaces a friendly "no input reviews available yet" message and exits cleanly. With the `adversarial` row at `status: mvp`, the selector returns `selected` for that methodology when chosen. If every MVP row is later removed, the empty-registry behaviour resumes — it is not an error.
