<!--
role: asset
kind: template

Populate-top-to-bottom skeleton for the transient "Amendments (pending re-merge)"
section that framework/agents/resolve-review-drafter.md inserts into
requirements/requirements.md at its Step 9b — ONLY on review-requirements-sourced
runs, ONLY after the paired input/ resolutions document was written and verified,
and ONLY with the consultant's per-run opt-in.

This file is the CANONICAL DEFINITION of:
  - the Amendments section's shape and heading text ("## Amendments (pending re-merge)")
  - the AMD-NN amendment-entry IDs
  - the section's placement and lifecycle rules (restated for fail-closed resilience
    in the drafter's Step 9b and Self-validation)

Placement rule:
  - Insert the whole section immediately BEFORE the "## Prototype invariants" heading
    when that appendix exists (the /export-application exporter strips PI-heading→EOF;
    anything after PI would be silently deleted at export). When no PI appendix exists
    (application-target docs), append at EOF.
  - If a "## Amendments (pending re-merge)" section already exists, do not insert a
    second section — append a new "### Run …" sub-block inside the existing section,
    continuing the AMD-NN numbering from the highest existing entry.
  - No other byte of the host document is ever touched. Insertion/extension only.

Lifecycle (self-cleaning — by design):
  - The next /requirements run overwrites requirements.md wholesale; this section
    disappears WITH the regeneration, correctly: the paired input/ resolutions
    document is ingested as corpus and the same content is folded into the body with
    proper [SRC: C-NNN] citations. No reconciliation machinery exists or is needed.
  - The pairing invariant is hard: every AMD entry's resolution prose must exist in
    the input/ resolutions document named in its Run sub-block header. An
    addendum-only fix is a contract violation.

Population rules:
  - Replace every {{PLACEHOLDER}}; the finished section contains zero {{…}} tokens.
  - Alternatives inside a placeholder are written {{a | b}} — emit exactly one.
  - One "#### AMD-NN — …" block per accepted resolution, in the resolutions
    document's finding order. AMD-NN is zero-padded and per-section continuous
    across runs (a second Run sub-block continues where the first stopped).
  - AMD IDs are deliberately NOT requirement-ID-shaped (F-NN / BR-NN / …): amendments
    must not mint per-run requirement IDs, and ID-walking reviewers must not
    enumerate them as base requirements.
  - Origin markers are the canonical /resolve-review pair — definitions in
    framework/assets/resolve-review/template-resolutions.md; spell them verbatim.
  - If the paired input/ resolution carries a "Grounding" line (elicitation-with-options
    resolutions), copy it verbatim onto the AMD block; omit it otherwise. This preserves
    the pairing invariant (addendum prose stays identical to the input/ resolution) — it
    does not breach it.
  - The preamble blockquote below IS part of the output — it instructs downstream
    LLM consumers (analysers, blueprint-architect, prototype agents, the exporter)
    how to apply the section. Emit it verbatim with placeholders resolved, once per
    section (not per Run sub-block).
-->
## Amendments (pending re-merge)

> Appended by `/resolve-review`. Entries in this section **supersede** the base text
> they name, everywhere in this document, until the next `/requirements` run folds
> their source resolutions into the body (this section then disappears with the
> regeneration — by design). Every entry is derived from a consultant-approved
> resolutions document under `input/` (named per run below); none of it is
> AI-invented content. Origin markers `[CONSULTANT-STATED]` /
> `[AI-INFERRED, CONSULTANT-CONFIRMED]`: canonical definitions in
> `framework/assets/resolve-review/template-resolutions.md`. Where an amendment
> adds, removes, or renames a §7 data-shape property or an F-NN parameter, the
> amended set is the authoritative closed set.

### Run {{YYYY-MM-DD}} — from `input/{{resolutions-filename}}` (review: `{{review_path}}`)

#### AMD-{{NN}} — {{one-line problem, from the resolutions document}}

**Amends:** {{the base anchor — §N.N / F-NN / BR-NN / US-NN / Shape.Field — plus a short verbatim quote of the superseded base text | (net-new — supersedes nothing in this document)}}

**Amendment** `[{{CONSULTANT-STATED | AI-INFERRED, CONSULTANT-CONFIRMED}}]`: {{the declarative resolution prose — identical to the resolution in the paired input/ document}}

<!-- Grounding line — emit ONLY when the paired input/ resolution carries one (i.e.
     elicitation-with-options resolutions); copy it verbatim from that resolution. Omit
     the whole line otherwise. Copying it verbatim preserves the pairing invariant. -->
**Grounding:** {{[grounded: <anchor>] | [domain-default] | [assumption — confirm with client]}} — {{one-line implication — copied verbatim from the paired input/ resolution}}

<!-- repeat the AMD block per accepted resolution; repeat the "### Run …" sub-block
     per /resolve-review run that lands while this section is alive -->
