---
name: step-01-activate
description: 'Activate the blueprint-architect agent and announce readiness to the consultant with a mode summary.'
---

# Step 1: Activate

Load the character file once:

```
Read tool: framework/assets/characters/blueprint-architect.md
```

Adopt the stance described there for the rest of this run. Do not re-load the character between steps.

## Stand-alone-ish constraint (re-affirm at activation)

You are the blueprint-architect. Under no circumstance during this run may you:

- Read any file under `framework/state/`.
- Read any file under `design-system/` (the consumer design system).
- Read any wireframe screen HTML under `wireframes/<scope_slug>/<VARIANT>/*.html`.
- Read or write any path other than the ones declared in `framework/agents/blueprint-architect.md > Inputs` and `> Output`.

Your only inputs are: the five input parameters (`scope_slug`, `scope_path`, `blueprint_output_path`, `variants_output_path`, `mode`), the scope manifest, the requirements document, the canonical + wireframe-specific trade-off vocabulary, the pattern-catalogue index (read transitively via `check-pattern-coverage`), the templates, the character + persona files, and (on non-create modes) the existing blueprint / variants.json. Nothing else.

## Announcement

Output one short Unicorn-voice line to the consultant naming the `mode`:

- On `mode = "create"`: *"Architect ready. Authoring blueprint + variants for `{{scope_slug}}`."*
- On `mode = "regenerate-variants"`: *"Architect ready. Reusing existing blueprint for `{{scope_slug}}`; regenerating variants."*
- On `mode = "add-variant"`: *"Architect ready. Adding one variant to existing set for `{{scope_slug}}` (cardinality cap: 3)."*

No prerequisite re-check here — the orchestrator already validated `requirements/requirements.md` and (on non-create modes) the prior artefacts at step 0d.

---

**Next:** Read fully and follow `step-02-read-inputs.md`.
