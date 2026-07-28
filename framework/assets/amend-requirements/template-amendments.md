<!--
role: asset
kind: template

Populate-top-to-bottom skeleton for the /amend-requirements amendments document,
written by framework/agents/amend-requirements-drafter.md (staged at
amend-requirements/amendments-draft.md, finalised as a NEW dated file under input/).

This file is the CANONICAL DEFINITION of:
  - the AM-NN amendment-entry IDs (document-local, always starting at AM-01)
  - the Amends line and its net-new sentinel
  - the Impact line and its closed flag vocabulary

It deliberately does NOT redefine the origin markers or the grounding tags — those are
canonical in framework/assets/resolve-review/template-resolutions.md and are spelled
verbatim here (canonical-source rule, docs/maintenance.md).

Why AM-NN and not AMD-NN:
  AMD-NN numbering lives in the host document's "## Amendments (pending re-merge)"
  section and is per-section continuous across runs — so it depends on what that
  section already holds and shifts meaning when the document is regenerated. AM-NN is
  document-local and stable forever: this file's third entry is AM-03 whatever the host
  document's numbering happens to be. The two ID spaces are independent by design; the
  pairing between them is asserted on amendment prose, not on IDs
  (framework/skills/apply-amendments-section.md > Self-validation).

Population rules:
  - Replace every {{PLACEHOLDER}}; the finished document contains zero {{…}} tokens.
  - Alternatives inside a placeholder are written {{a | b | c}} — emit exactly one.
  - One "### AM-NN — …" block per accepted amendment, in the order the consultant
    stated them. AM-NN is zero-padded and starts at AM-01 in every document.
  - Every block carries EXACTLY ONE origin marker, EXACTLY ONE Amends line, EXACTLY ONE
    Impact line, and EXACTLY ONE Supersedes line.
  - The "Grounding" line is emitted ONLY for amendments drafted through the
    elicitation-with-options flow (a vague ask the drafter turned into candidates);
    omit the whole line for amendments the consultant stated outright.
  - The dropped table lists every change the consultant raised and then abandoned or
    explicitly withdrew; changes never raised are not listed.
  - HTML comments in this skeleton ARE part of the output document — they brief
    downstream readers (the /requirements drafter and the consultant) and are emitted
    verbatim with placeholders resolved.

Marker legend (referenced, not redefined):
  [CONSULTANT-STATED] and [AI-INFERRED, CONSULTANT-CONFIRMED] — canonical definitions
  in framework/assets/resolve-review/template-resolutions.md > Marker legend. Grounding
  tags ([grounded: <anchor>] / [domain-default] / [assumption — confirm with client])
  are canonical in the same file. Spell all of them verbatim; never coin a variant.

Impact flag vocabulary (canonical here — closed set, computed by the drafter, never asked):
  closed-set-change: {{adds | removes | renames}} <Shape.Field | F-NN:ParamName>
      The amendment changes the closed property set the wireframe/prototype pipelines
      bind against (CLAUDE.md > Constraints > Wireframe pipeline never invents object
      properties). A removal can orphan existing data-prop bindings.
  scope-change: <one line>
      The amendment moves something across the §1.5 In / Out / Deferred boundary.
  amends-amendment: AMD-NN
      The base text this amendment supersedes is itself an entry in the host document's
      "## Amendments (pending re-merge)" section, not original body text.
  (none)
      No flag applies. Emitted as the literal "(none)".
-->
# Requirements Amendments — {{YYYY-MM-DD}}

<!-- Consultant-approved input document produced by /amend-requirements.
     Corpus material: the next source-manifest build ingests this file like any other
     input/ file (Native-text tier). Each amendment below states what the requirements
     document should assert, anchored to the base text it replaces. Where an amendment
     changes a fact stated elsewhere in the corpus, its Supersedes line is
     authoritative: treat the superseded statement as replaced, not contradicted.
     The paired "## Amendments (pending re-merge)" section in requirements.md is a
     transient cache of this file and disappears at the next /requirements re-merge —
     THIS file is the durable record. -->

## Provenance

| Field | Value |
|---|---|
| Source | consultant (in-thread, `/amend-requirements`) |
| Amendment date | {{YYYY-MM-DD}} |
| Requirements document | `requirements/requirements.md` |
| Requirements sha256 at amendment time | `{{DOC_SHA256}}` |
| Requirements `Status` at amendment time | {{final | draft | (unparseable)}} |
| Requirements `Last finalised at` | {{ISO-8601 | not stamped}} |
| Amendments already in the document | {{N}} entries across {{M}} runs | (none — first amendment run) |
| Amendments recorded here | {{AM-NN, AM-NN, …}} |
| Changes dropped | {{short label, short label, … | (none)}} |
| Impact flags | {{closed-set-change: {{k}}; scope-change: {{k}}; amends-amendment: {{k}} | (none)}} |

<!-- No "addendum applied" row: whether the paired requirements.md section write
     succeeded is decided after this document is finalised, and recording transient
     host-document state in a durable corpus file would mislead after the next
     re-merge removes that section. The pairing is recorded on the section side (its
     Run sub-block names this file). -->

**Origin markers:** `[CONSULTANT-STATED]` — the consultant supplied the amendment
content. `[AI-INFERRED, CONSULTANT-CONFIRMED]` — drafted by the drafter as a candidate
enrichment for a vague or underspecified change and explicitly selected by the
consultant for that one amendment. Canonical definitions:
`framework/assets/resolve-review/template-resolutions.md`. Every amendment below carries
exactly one. Amendments drafted as candidates also carry a **grounding tag** on their
Grounding line.

## Amendments

### AM-{{NN}} — {{one-line change}}

**Amends:** {{the base anchor — §N.N / F-NN / BR-NN / US-NN / Shape.Field / AMD-NN — followed by a short verbatim quote (≤5 lines) of the superseded base text | (net-new — supersedes nothing in the requirements document)}}

**Amendment** `[{{CONSULTANT-STATED | AI-INFERRED, CONSULTANT-CONFIRMED}}]`
{{declarative, corpus-quality amendment prose — a statement of fact, requirement, or scope decision; what the amended document should assert; never a Q&A transcript}}

<!-- Grounding line — emit ONLY for amendments drafted through the
     elicitation-with-options candidate flow; omit the whole line for amendments the
     consultant stated outright. -->
**Grounding:** {{[grounded: <§N.N / F-NN / BR-NN / AMD-NN>] | [domain-default] | [assumption — confirm with client]}} — {{one-line implication: what adopting this amendment commits the design/build to}}

**Impact:** {{closed-set-change: {{adds | removes | renames}} {{Shape.Field | F-NN:ParamName}} | scope-change: {{one line}} | amends-amendment: AMD-{{NN}} | (none)}}

**Supersedes:** {{This supersedes the statement in `requirements/requirements.md` regarding {{X}}. | This supersedes the statement in `<filename>` regarding {{X}}. | (supersedes nothing — net-new information)}}

---

<!-- repeat the block above per accepted amendment, separated by --- rules -->

## Changes raised but dropped

| Short label | Why dropped |
|---|---|
| {{short label}} | {{consultant's reason, or "withdrawn at the per-change ask (no reason given)"}} |

<!-- if nothing was dropped, replace the table with the single line:
     (none — every change raised was recorded) -->
