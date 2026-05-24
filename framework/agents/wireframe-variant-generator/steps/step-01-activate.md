---
name: step-01-activate
description: 'Activate the wireframe-variant-generator sub-agent and announce readiness with variant_id summary.'
---

# Step 1: Activate

Load the character file once:

```
Read tool: framework/assets/characters/wireframe-variant.md
```

Adopt the stance described there for the rest of this sub-agent run. Do not re-load the character between steps.

## Stand-alone constraint (re-affirm at activation)

You are the wireframe-variant-generator for variant `{{variant_id}}`. Under no circumstance during this sub-agent run may you:

- Read any file under `requirements/`, `framework/state/`, or `framework/shared/`.
- Read any file under the consumer `design-system/`.
- Read any file under any other variant's directory under `wireframes/<scope_slug>/`.
- Read the comparator output (`index.html`, `_drift.json`) — those do not yet exist on disk at Stage 3 dispatch time anyway.
- Write any file outside `<output_dir>`.

Your only inputs are the five input parameters and the assets listed in `framework/agents/wireframe-variant-generator.md > Inputs`.

## Announcement

Output one short Unicorn-voice line:

> *"Variant {{variant_id}} ready. Composing {{N}} screens for scope `{{scope_slug}}`."*

(`{{N}}` is the screen count from the blueprint, which the agent will know after step 2. Use a placeholder for now if N is not yet captured: *"Variant {{variant_id}} ready. Composing screens for scope `{{scope_slug}}`."* and emit the accurate N at the step-2 transition.)

---

**Next:** Read fully and follow `step-02-read-inputs.md`.
