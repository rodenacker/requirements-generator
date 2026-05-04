---
name: step-07-handback
description: 'Present the artefact summary in the Unicorn voice, run the accept/revise/restart loop, clean up the workspace, and hand back to the orchestrator.'
# Variables referenced (inherited from agent):
# workspace_path: 'design-system/.workspace'
---

# Step 7: Hand Back

## A. Summary in Unicorn Voice

Output one short, concrete summary line listing token counts and provenance breakdown. No marketing language. No chatbot warmth.

Template:

> "Wrote `design-system/design-system.md` — `{{n_colors_extracted}}/11` colour tokens extracted, `{{n_typo_extracted}}/15` typography tokens extracted, `{{n_effects_extracted}}/7` effects tokens extracted; the rest filled from `{{domain}}` defaults. Contrast: `{{cv_pass_count}}/4` pairs pass at WCAG AA (`{{cv_adjustment_count}}` adjustments). Ready, or want changes?"

Variants:

- If `{{extraction_status}} != "success"`, prepend one short clause: *"URL extraction did not run (`{{extraction_status}}`) — every token comes from the `{{domain}}` defaults."*
- If `{{reference_url}}` is null, prepend: *"No URL given — every token comes from the `{{domain}}` defaults."*

## B. Accept/Revise/Restart Loop

Use `AskUserQuestion`:

- Question: *"Accept the design system, request specific changes, or restart from inputs?"*
- Header: `Accept?`
- multiSelect: false
- Options:
  1. `Accept — hand back to orchestrator (Recommended)`
  2. `Revise — change specific tokens`
  3. `Restart — re-enter inputs`

### Branches

- **Accept** — proceed to §C (workspace cleanup), then declare done.
- **Revise** — accept the consultant's revision instructions in their next message. Apply the changes:
   - For colour overrides: write the new hex value into `{{extracted_colors}}` and re-run contrast validation against the affected pairs.
   - For typography or effect overrides: write the new value into the corresponding in-memory structure.
   - For provenance: a revised value retains the marker that was on it before — the consultant's edit is treated as a downstream correction, not a re-source. (Per the locked decision, there is no `consultant-specified` marker in v1.)
   - Re-render the artefact (re-enter step-06's procedure, including sha256 + verify-artifact-write).
   - Loop back to §A and present the updated summary.
- **Restart** — re-enter `step-02-inputs.md`. The previously-written `design-system/design-system.md` is left in place; the next step-06 will overwrite it.

The accept/revise/restart loop continues until the consultant chooses Accept.

## C. Workspace Cleanup

After acceptance:

1. Delete `design-system/.workspace/` and its contents: `Bash rm -rf design-system/.workspace`.
2. If deletion fails, log a warning but do not halt — workspace cleanup is best-effort.

## D. Hand Back to Orchestrator

Output the final handback line:

> "Design system accepted. Handing back to the orchestrator."

The orchestrator's handback gate is satisfied when `design-system/design-system.md` exists and has been verified by `verify-artifact-write` with a `pass`, the consultant has chosen Accept, and the workspace folder has been removed.

---

**STOP** — design-system-styler workflow complete.
