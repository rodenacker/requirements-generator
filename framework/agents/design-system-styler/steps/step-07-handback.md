---
name: step-07-handback
description: 'Present the artefact summary in the Unicorn voice, run the accept/revise/restart loop, clean up the workspace, and hand back to the orchestrator.'
# Variables referenced (inherited from agent):
# workspace_path: 'design-system/.workspace'
---

# Step 7: Hand Back

## A. Summary in Unicorn Voice

Output one short, concrete summary listing the written file(s), token counts, and provenance breakdown. No marketing language. No chatbot warmth.

Lead with the hue-source file (the grounded one), then the derived file if there is one.

**Single-file template:**

> "Wrote `design-system/design-system-{{mode}}.html` — `{{n_colors_extracted}}/11` colour tokens extracted, `{{n_typo_extracted}}/15` typography tokens extracted, `{{n_effects_extracted}}/7` effects tokens extracted; the rest filled from `{{domain}}` defaults. Contrast: `{{cv_pass_count_<mode>}}/4` pairs pass at WCAG AA (`{{cv_adjustment_count_<mode>}}` adjustments). Ready, or want changes?"

**Two-file template:**

> "Wrote two files. `design-system/design-system-{{hue_source_mode}}.html` — **primary**, the extracted palette: `{{n_colors_extracted}}/11` colour tokens extracted, `{{n_typo_extracted}}/15` typography, `{{n_effects_extracted}}/7` effects; the rest filled from `{{domain}}` defaults. Contrast `{{cv_pass_count_<hue>}}/4` (`{{cv_adjustment_count_<hue>}}` adjustments).
> `design-system/design-system-{{derived_mode}}.html` — derived from the same brand hues, not separately extracted; 11 colours + 3 shadows re-lit, typography and motion shared verbatim. Contrast `{{cv_pass_count_<derived>}}/4` (`{{cv_adjustment_count_<derived>}}` adjustments).
> Ready, or want changes?"

Variants — prepend whichever apply:

- If `{{extraction_status}} != "success"`: *"URL extraction did not run (`{{extraction_status}}`) — every token comes from the `{{domain}}` defaults."*
- If `{{reference_url}}` is null: *"No URL given — every token comes from the `{{domain}}` defaults."*
- If `{{extracted_scheme}} == "dark"`: *"The site shipped a **dark** palette, so dark is the hue source here and light is the derived mode."* — this inverts the common case and the consultant should not have to infer it from the filenames.
- If `{{files_to_write}}` contains a mode the consultant did **not** ask for (they chose one mode but the hue-source file was written too): *"You asked for `{{requested_mode}}` only; I also wrote the `{{hue_source_mode}}` file because that's the palette the URL actually shipped — it's kept as the grounded record and marked primary."*

Always name which file is primary when two were written. `{{primary_mode}}` is always `{{hue_source_mode}}`.

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
- **Revise** — accept the consultant's revision instructions in their next message. Revisions are **mode-scoped**; establish which mode a named token belongs to before applying it (ask if genuinely ambiguous). Apply the changes:
   - **Revising a hue-source token** — write the new value into the hue-source set, re-run that mode's contrast validation in its own direction, **and re-derive the affected counterpart token(s) in the derived set** (per `data/cross-mode-derivation-rules.md`), then re-run the derived mode's contrast validation. Re-deriving is what preserves the invariant that the two files describe the same brand; silently leaving the derived value stale would break it. If the consultant explicitly scopes the change to one mode ("only in light"), honour that and skip the re-derivation — but say that the two files now diverge.
   - **Revising a derived token** — override that value in the derived set only. Do **not** propagate backwards into the hue-source set: the hue source is the grounded record, and a consultant tweak to a derived value is a downstream correction, not new evidence about the brand.
   - For colour overrides: re-run contrast validation against the affected pairs in the relevant mode's direction.
   - For typography or effect overrides: write the new value into the corresponding in-memory structure. Note that the 19 shared tokens (typography + motion) are shared across modes — revising one changes **both** files.
   - For provenance: a revised value retains the marker that was on it before — the consultant's edit is treated as a downstream correction, not a re-source. (Per the locked decision, there is no `consultant-specified` marker in v1.) A revised derived token also keeps its `derived: …` source string.
   - Re-render **only the affected file(s)** by re-entering step-06's per-mode procedure for those modes, including per-file sha256 + `verify-artifact-write`. When a hue-source token changed and was re-derived, both files are affected.
   - Loop back to §A and present the updated summary.
- **Restart** — re-enter `step-02-inputs.md`. The previously-written `design-system-*.html` files are left in place; the next step-06 will overwrite them. Note that extraction runs again, so the scheme is re-detected and the step-05b §E mode question is re-asked — the mode choice is not sticky across a restart.

The accept/revise/restart loop continues until the consultant chooses Accept.

## C. Workspace Cleanup

After acceptance:

1. Delete `design-system/.workspace/` and its contents: `Bash rm -rf design-system/.workspace`.
2. If deletion fails, log a warning but do not halt — workspace cleanup is best-effort.

## D. Hand Back to Orchestrator

Output the final handback line:

> "Design system accepted. Handing back to the orchestrator."

The orchestrator's handback gate is satisfied when:

- **Every** mode in `{{files_to_write}}` has its `design-system/design-system-<mode>.html` on disk, each verified by `verify-artifact-write` with a `pass`. This always includes `{{hue_source_mode}}`.
- Exactly one written file carries `meta.primary: true`, and it is the `{{hue_source_mode}}` file.
- The consultant has chosen Accept.
- The workspace folder has been removed.

A partial pair — hue-source file verified but the requested derived file missing — does **not** satisfy the gate.

---

**STOP** — design-system-styler workflow complete.
