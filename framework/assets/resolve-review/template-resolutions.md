<!--
role: asset
kind: template

Populate-top-to-bottom skeleton for the /resolve-review resolutions document,
written by framework/agents/resolve-review-drafter.md (staged at
resolve-review/resolutions-draft.md, finalised as a NEW dated file under input/).

This file is the CANONICAL DEFINITION of:
  - the two origin markers: [CONSULTANT-STATED] and [AI-INFERRED, CONSULTANT-CONFIRMED]
  - the mandatory Supersedes line and its net-new sentinel

Population rules:
  - Replace every {{PLACEHOLDER}}; the finished document contains zero {{…}} tokens.
  - Alternatives inside a placeholder are written {{a | b | c}} — emit exactly one.
  - One "### {{ID}} — …" block per resolved finding, in finding-ID order.
  - Every resolution block carries EXACTLY ONE origin marker and EXACTLY ONE
    Supersedes line (a named-file supersession or the literal net-new sentinel).
  - The "Grounding" line is OPTIONAL: emit it (exactly one grounding tag + a one-line
    implication) ONLY for elicitation-with-options (gap-surfacing question) resolutions,
    and omit the whole line for every other resolution semantics.
  - The skipped table lists every finding the consultant selected-then-skipped or
    explicitly rejected at the per-finding ask; findings never selected at the
    multi-pick are not listed.
  - HTML comments in this skeleton ARE part of the output document — they brief
    downstream readers (the /requirements drafter and the consultant) and are
    emitted verbatim with placeholders resolved.

Marker legend (canonical):
  [CONSULTANT-STATED]
      The consultant supplied the resolution content (typed the answer, stated the
      intended meaning, edited the candidate text). Highest-confidence origin.
  [AI-INFERRED, CONSULTANT-CONFIRMED]
      The resolution was drafted by the resolver — either from the review finding's own
      actionable payload (recommendation, interpretation, candidate requirement) OR, for
      elicitation-with-options (gap-surfacing question) findings, from the resolver's own
      domain reasoning to close an elicited gap — and the consultant explicitly affirmed
      it: individually at the per-finding ask, or via the explicit "Accept all remaining
      as drafted" choice (confirmation-type flows only — elicitation-with-options is
      always confirmed per finding). Silence, a skipped answer, or approval of a different
      finding is never a valid path to this marker. Every resolution drafted from domain
      reasoning carries a grounding tag (see below) — the tag, not a new marker, carries
      the trust signal for how well-grounded the resolution is.
  Grounding tag (elicitation-with-options resolutions only)
      Exactly one of: "[grounded: <anchor>]" (the resolution stands on a cited §N.N /
      F-NN / BR-NN / existing AMD-NN of requirements.md), "[domain-default]" (an
      enterprise financial-transaction data-management convention — maker-checker,
      four-eyes, SLA cut-offs, reconciliation consumers, …), or "[assumption — confirm
      with client]". Carried on the optional "Grounding" line of the resolution block,
      together with a one-line implication. Present for every elicitation-with-options
      resolution (consultant-stated or AI-inferred); omitted for all other resolution
      semantics.
  Supersedes line
      "This supersedes the statement in `<filename>` regarding <X>." — emitted when
      the resolution changes or overrides a fact stated elsewhere in the input
      corpus, naming the file and the subject. When the resolution adds net-new
      information that contradicts nothing, emit the literal sentinel:
      "(supersedes nothing — net-new information)". One of the two forms is
      mandatory on every resolution.
-->
# Review Resolutions — {{METHOD_NAME}} ({{METHOD_DIR}})

<!-- Consultant-approved input document produced by /resolve-review.
     Corpus material: the next source-manifest build ingests this file like any
     other input/ file (Native-text tier). Finding IDs below are per-run labels
     from the source review and reset whenever that review is re-run — the
     verbatim finding quotes are the durable anchors. Where a resolution changes
     a fact stated elsewhere in the corpus, its Supersedes line is authoritative:
     treat the superseded statement as replaced, not contradicted. -->

## Provenance

| Field | Value |
|---|---|
| Source review | `{{REVIEW_PATH}}` |
| Source review sha256 | `{{REVIEW_SHA256}}` |
| Review's source fingerprint | {{`REVIEW_SOURCE_FINGERPRINT` | (not recorded in the review)}} |
| Fingerprint target ({{`requirements/source-manifest.json` | `requirements/requirements.md`}}) at resolution time | {{`CURRENT_FINGERPRINT` | (no manifest on disk)}} |
| Source drift | {{none | DRIFT — the review predates the current {{corpus | requirements document}} | (not compared — no manifest)}} |
| Methodology | `{{method_slug}}` |
| Resolution date | {{YYYY-MM-DD}} |
| Findings resolved | {{ID, ID, …}} |
| Findings skipped | {{ID, ID, … | (none)}} |

<!-- No addendum row: the Step-9b addendum outcome is decided after this document is
     finalised, and recording transient requirements.md state in a durable corpus file
     would mislead after the next re-merge removes the addendum. The pairing is recorded
     on the addendum side (its Run sub-block names this file). -->

**Origin markers:** `[CONSULTANT-STATED]` — the consultant supplied the resolution
content. `[AI-INFERRED, CONSULTANT-CONFIRMED]` — drafted by the resolver from the
review finding's own actionable payload, or (for gap-surfacing question findings) from
the resolver's domain reasoning, and explicitly confirmed by the consultant (per
finding, or — confirmation-type flows only — via an explicit "Accept all remaining as
drafted" choice). Every resolution below carries exactly one. Resolutions drafted to
close an elicited gap also carry a **grounding tag** on their Grounding line.

## Resolutions

### {{ID}} — {{one-line problem}}

**Finding (verbatim, from the review):**
> {{evidence quote — verbatim per the methodology's verbatim_anchor; multi-line quotes keep the > prefix per line}}

**Problem as stated by the review:** {{problem text, verbatim | (gap-analysis: coverage + impact × confidence, verbatim)}}

**Review's actionable payload:** {{Recommendation + Disposition | Elicitation question | Interpretations | Candidate Requirement + MoSCoW — copied verbatim}}

**Resolution** `[{{CONSULTANT-STATED | AI-INFERRED, CONSULTANT-CONFIRMED}}]`
{{declarative, corpus-quality resolution prose — a statement of fact, requirement, or scope decision; never a Q&A transcript}}

<!-- Grounding line — emit ONLY for elicitation-with-options (gap-surfacing question)
     resolutions; omit the whole line for every other resolution semantics. -->
**Grounding:** {{[grounded: <§N.N / F-NN / BR-NN / AMD-NN>] | [domain-default] | [assumption — confirm with client]}} — {{one-line implication: what adopting this resolution commits the design/build to}}

**Supersedes:** {{This supersedes the statement in `<filename>` regarding {{X}}. | (supersedes nothing — net-new information)}}

---

<!-- repeat the block above per resolved finding, separated by --- rules -->

## Findings considered but skipped

| ID | One-line problem | Skip reason |
|---|---|---|
| {{ID}} | {{one-line problem}} | {{consultant's reason, or "skipped at per-finding ask (no reason given)"}} |

<!-- if no findings were skipped, replace the table with the single line:
     (none — every selected finding was resolved) -->
