---
name: step-06-artifact-generation
description: 'Render the populated template, append the static standards appendix, write to design-system/design-system.md, then verify the write.'
# Variables referenced (inherited from agent):
# prompt_artifact_generation: 'framework/agents/design-system-styler/prompt-templates/artifact-generation.md'
# template_path: 'framework/assets/template-design-system.md'
# standards_path: 'framework/assets/design-system-standards.md'
# output_path: 'design-system/design-system.md'
---

# Step 6: Generate the Artefact

Read the artifact-generation prompt template:

```
Read tool: framework/agents/design-system-styler/prompt-templates/artifact-generation.md
```

**Inputs (in-memory after step-05b):**

- `{{extracted_colors}}` — 7 brand tokens (status colours always domain-filled)
- `{{status_colors}}` — 4 status tokens (always `inferred-from-domain`)
- `{{extracted_typography}}` — 15 typography tokens
- `{{extracted_effects}}` — 7 effect tokens
- `{{contrast_validation}}` — 4 pair ratios + adjustments line
- `{{extraction_status}}`, `{{extraction_date}}`, `{{domain}}`, `{{domain_source}}`, `{{reference_url}}`, `{{css_source_type}}`, `{{css_source_url}}`

## A. Source the Template

Read `framework/assets/template-design-system.md`. Use it as the structural base. Replace every `{{placeholder}}` with the corresponding in-memory value. Do not insert, remove, or reorder sections.

## B. Apply the Artifact-Generation Prompt

Apply the prompt template's instructions in order:

1. Section 3 — Frontmatter: write the YAML frontmatter with all eight provenance fields.
2. Section 4 — Attribution paragraph: pick the variant per `{{extraction_status}}` and `{{reference_url}}` state.
3. Section 5 — Provenance tagging: every token row gets `extracted-from-url` or `inferred-from-domain`.
4. Section 6 — Populate the Extraction Summary tables (Colours, Typography, Effects, Contrast Validation) and the machine-readable Brand sections.

The artefact is generated even when `{{extraction_status}}` ≠ `"success"`. The doc is always complete (every token filled from domain defaults if extraction was skipped); the frontmatter `extraction_status` field records *why* the URL path didn't yield extracted values.

## B-bis. Append the Static Standards Appendix

After the template is fully rendered (all placeholders replaced) and before the pre-write self-check, append the static standards file:

1. Read `framework/assets/design-system-standards.md`.
2. Concatenate its full contents to the rendered template string, separated by exactly one blank line. The standards file opens with its own `---` separator and an `## Design System Standards` heading, so it slots in cleanly after the `## Brand Effects > Motion` table.
3. **Do not modify the standards content.** No placeholder substitution, no rewording, no truncation. It is static reference material that ships verbatim with every output. If the file cannot be read, halt — do not write a partial artefact.

## C. Pre-Write Self-Check

Before calling `Write`:

- Render the full artefact (template body + appended standards) as one string in memory.
- Confirm: every `{{placeholder}}` has been replaced. No literal `{{...}}` substrings remain. (The standards appendix contains no placeholders.)
- Confirm: every Provenance cell in the Extraction Summary is non-empty and is one of `extracted-from-url` or `inferred-from-domain`. No third marker.
- Confirm: status-colour rows (success/warning/error/info) all carry `inferred-from-domain` regardless of the URL outcome.
- Confirm: the `## Brand Effects > Motion` table appears in its required position with `easing-standard` as its final row.
- Confirm: the document continues after the Motion table with the static `## Design System Standards` section sourced from `framework/assets/design-system-standards.md`. The document ends with the final line of that standards file.
- Compute `sha256` of the rendered byte string (template + standards). Store as `{{expected_sha256}}`.

## D. Write

1. Ensure the `design-system/` directory exists. If not, create it: `Bash mkdir -p design-system`.
2. Write the rendered string to `design-system/design-system.md` (single atomic Write call).
3. Store `{{artifact_path}} = "design-system/design-system.md"` and `{{artifact_written}} = true`.

## E. Verify the Write

Invoke `framework/skills/verify-artifact-write.md` with:

- `path = "design-system/design-system.md"`
- `expected_sha256 = {{expected_sha256}}`
- `expected_min_bytes = 2000` (a complete artefact runs well above this; truncation that drops a section will not)

If the skill returns `pass`, advance to step-07.

If the skill returns `RF-04 trigger`, halt per the refusal-registry surface — the agent does not write a `completed` event for itself, the orchestrator surfaces the refusal, and the consultant resolves the underlying filesystem issue before re-running.

---

**Next:** Read fully and follow `step-07-handback.md`.
