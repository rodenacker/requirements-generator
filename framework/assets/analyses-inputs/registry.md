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
  - { name: glossary, status: future }
  - { name: jtbd, status: future }
  - { name: five-whys, status: future }
  - name: thematic-analysis
    status: mvp
    description: Surfaces the patterns the consultant's raw inputs already carry as codes, themes, and a theme-map — and bridges each theme to candidate requirements before /requirements drafts them.
    output_path: analyses/inputs/THEMATIC-ANALYSIS/thematic-analysis.md
    reference_asset: framework/assets/analyses-inputs/thematic-analysis-reference.md
    template_asset: null
    map_skill: framework/skills/map-thematic-analysis-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/thematic-analysis-analyser.md
    character: framework/assets/characters/thematic-analysis-inputs-analysis.md
  - name: opportunity-solution-trees
    status: mvp
    description: Maps raw inputs into an outcome → opportunities → solutions → assumption-test discovery tree (Torres 2016), with a bridge of candidate-requirement seeds /requirements can pick up when the artefact is re-dropped into input/.
    output_path: analyses/inputs/OPPORTUNITY-SOLUTION-TREES/opportunity-solution-tree.md
    reference_asset: framework/assets/analyses-inputs/opportunity-solution-trees-reference.md
    template_asset: null
    map_skill: framework/skills/map-opportunity-solution-trees-from-inputs-to-ui.md
    analyser_agent: framework/agents/analyses-inputs/opportunity-solution-trees-analyser.md
    character: framework/assets/characters/opportunity-solution-trees-inputs-analysis.md
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
7. Promote the registry row: flip `status: future` to `status: mvp` and populate all remaining fields (`description`, `output_path`, `reference_asset`, `template_asset`, `map_skill`, `analyser_agent`, `character`). `output_path` lives under `analyses/inputs/<METHOD>/` (uppercase methodology name) — e.g. `analyses/inputs/GLOSSARY/glossary.md`.
8. Add the analyser node to graph 5 in `framework/dependency-graphs.md`.
9. No orchestrator changes required — the selector skill picks the new MVP row up automatically.

**Field semantics:**

- `name` — kebab-case slug. Used as the subdirectory name under `analyses/inputs/` (uppercased to `analyses/inputs/<METHOD>/`) and as the path component in the analyser agent file. Methodology slugs are shared across registries (a row named `glossary` can exist in both `analyses/registry.md` and `analyses-inputs/registry.md`); the artefacts do not clobber because the output paths differ (`analyses/GLOSSARY/...` vs `analyses/inputs/GLOSSARY/...`).
- `status` — `mvp` (selectable now) or `future` (not yet built; this is the default state for every row on framework first-ship).
- `description` — one-line label surfaced in the selector's printed list. Required only when `status: mvp`.
- `output_path` — relative path of the artefact the analyser writes. Drives the prior-artefact gate in the orchestrator. **Must** live under `analyses/inputs/` for write-isolation. Required only when `status: mvp`.
- `reference_asset` — the methodology reference the analyser follows. Required only when `status: mvp`.
- `template_asset` — file scaffold the analyser populates (may be `null` for methodologies that emit pure Markdown).
- `map_skill` — translates the analysis output into UI inventory entries for downstream design consumption. May reuse the existing `framework/skills/map-<method>-to-ui.md` if source-agnostic, or be a sibling `map-<method>-from-inputs-to-ui.md` if the mapping diverges. Not invoked by `/analyse-inputs`.
- `analyser_agent` — the foreground agent invoked by the orchestrator. Required only when `status: mvp`.
- `character` — stance the Unicorn adopts while running the analyser. Required only when `status: mvp`.

**Forbidden name reservation:** the name `inputs` must not be used as a methodology slug in either this registry or `framework/assets/analyses/registry.md` — it would collide with this pipeline's output-directory scope (`analyses/inputs/`).

**Empty-MVP behaviour:** when every row has `status: future` the selector returns `empty-registry` and the orchestrator surfaces a friendly "no input analyses available yet" message and exits cleanly. This was the expected steady state on framework first-ship; with `thematic-analysis` and `opportunity-solution-trees` now at `status: mvp`, the selector presents two options to the consultant. If every MVP row is removed in the future, the empty-registry behaviour resumes — it is not an error.
