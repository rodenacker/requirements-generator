<!--
role: asset
kind: template

Populate-top-to-bottom skeleton for the transient "Amendments (pending re-merge)"
section, written by framework/skills/apply-amendments-section.md (which reads this
file) on behalf of either of its two callers:

  - framework/agents/resolve-review-drafter.md at its Step 9b — ONLY on
    review-requirements-sourced runs, ONLY after the paired input/ resolutions
    document was written and verified, and ONLY with the consultant's per-run opt-in.
  - framework/agents/amend-requirements-drafter.md at its Step 9 — unconditionally
    (applying the section is that pipeline's purpose, so it has no opt-in ask),
    after the paired input/amendments-<date>.md document was written and verified.

Both callers pass fully-composed entries plus their own "### Run …" header form; the
skill owns placement, AMD-NN numbering, byte-isolation, the pairing assertion, and the
write-verify. Neither caller reads this file directly.

This file is the CANONICAL DEFINITION of:
  - the Amendments section's shape and heading text ("## Amendments (pending re-merge)")
  - the AMD-NN amendment-entry IDs
  - the two "### Run …" sub-block header forms (review-sourced and consultant-sourced)
  - the section's placement and lifecycle rules (restated for fail-closed resilience
    in framework/skills/apply-amendments-section.md and in each caller's Self-validation)

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
    disappears WITH the regeneration, correctly: the paired input/ document is
    ingested as corpus and the same content is folded into the body with proper
    [SRC: C-NNN] citations. No reconciliation machinery exists or is needed.
  - The pairing invariant is hard: every AMD entry's amendment prose must exist in
    the input/ document named in its Run sub-block header. A section-only fix is a
    contract violation — and, because the next re-merge deletes this section, it is
    silent data loss rather than a shortcut.

Population rules:
  - Replace every {{PLACEHOLDER}}; the finished section contains zero {{…}} tokens.
  - Alternatives inside a placeholder are written {{a | b}} — emit exactly one.
  - One "#### AMD-NN — …" block per accepted entry, in the paired input/ document's
    own order (finding order for review-sourced runs, AM-NN order for
    consultant-sourced runs). AMD-NN is zero-padded and per-section continuous
    across runs (a second Run sub-block continues where the first stopped).
  - Emit ONE "### Run …" header per run, choosing the form that matches the source
    (both are given below). The two forms differ only in what they name as the origin;
    the AMD blocks beneath them are identical in shape.
  - The AMD block carries NO "Impact:" line, even when the paired input/ document's
    entry has one. Impact flags (closed-set-change / scope-change /
    amends-amendment — canonical in
    framework/assets/amend-requirements/template-amendments.md) are a property of the
    durable record, not of this cache; carrying them here would put a second,
    divergent copy of a derived classification into the host document.
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

> Appended by `/resolve-review` or `/amend-requirements`. Entries in this section
> **supersede** the base text they name, everywhere in this document, until the next
> `/requirements` run folds their source documents into the body (this section then
> disappears with the regeneration — by design). Every entry is derived from a
> consultant-approved document under `input/` (named per run below); none of it is
> AI-invented content. Origin markers `[CONSULTANT-STATED]` /
> `[AI-INFERRED, CONSULTANT-CONFIRMED]`: canonical definitions in
> `framework/assets/resolve-review/template-resolutions.md`. Where an amendment
> adds, removes, or renames a §7 data-shape property or an F-NN parameter, the
> amended set is the authoritative closed set.

<!-- Run sub-block header — emit EXACTLY ONE of the two forms below per run, matching
     the source. Review-sourced (written for framework/agents/resolve-review-drafter.md): -->
### Run {{YYYY-MM-DD}} — from `input/{{resolutions-filename}}` (review: `{{review_path}}`)

<!-- Consultant-sourced (written for framework/agents/amend-requirements-drafter.md).
     There is no review to name; the origin is the consultant's own in-thread
     statements, recorded in the named input/ document: -->
### Run {{YYYY-MM-DD}} — from `input/{{amendments-filename}}` (source: consultant)

#### AMD-{{NN}} — {{one-line problem or change, from the paired input/ document}}

**Amends:** {{the base anchor — §N.N / F-NN / BR-NN / US-NN / Shape.Field / an earlier AMD-NN — plus a short verbatim quote of the superseded base text | (net-new — supersedes nothing in this document)}}

**Amendment** `[{{CONSULTANT-STATED | AI-INFERRED, CONSULTANT-CONFIRMED}}]`: {{the declarative prose — identical to the entry in the paired input/ document}}

<!-- Grounding line — emit ONLY when the paired input/ entry carries one (i.e.
     elicitation-with-options resolutions, or candidate-derived amendments); copy it
     verbatim from that entry. Omit the whole line otherwise. Copying it verbatim
     preserves the pairing invariant. -->
**Grounding:** {{[grounded: <anchor>] | [domain-default] | [assumption — confirm with client]}} — {{one-line implication — copied verbatim from the paired input/ entry}}

<!-- repeat the AMD block per accepted entry; repeat the "### Run …" sub-block per
     /resolve-review or /amend-requirements run that lands while this section is alive -->
