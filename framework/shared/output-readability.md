<!-- ROLE: shared (cross-pipeline prose policy). Referenced by every human-facing producer's "Reader & plain language" voice block. Canonical definition of the human-audience readability standard — referenced by path, never restated. -->

# Output readability standard (human-facing artefacts)

Every artefact in the **Scope** table below is read by the **consultant**. It must answer two questions directly, without the reader having to go and look something else up:

1. **What did you find?**
2. **What does that mean for me — what do I do now?**

This standard is **not additive**. Volume is itself a defect: an artefact the consultant cannot finish reading has failed, however complete it is. Applying this standard must leave a document **the same length or shorter**, with the single exception of rule 4's pointer quotations, which trade a few words on the page for a lookup the reader would otherwise have to perform. It removes **no** structure, **no** citation, **no** rigour, and it relaxes **no** quality gate. Format is out of scope — cards, tables, metric grids, TOCs, heatmaps and embedded sidecars are unchanged. **Phrasing** is what this standard governs.

It is referenced (not restated) by each producing agent's or character's *Reader & plain language* voice block. Where it appears to conflict with a character's existing voice rules, the reconciliation in §R below governs.

## Scope

**Binds** (human-facing):

| Artefact | Produced by |
|---|---|
| `generated-docs/requirements/requirements.md` | `/requirements` |
| `generated-docs/prd/prd.md` | `/generate-prd` |
| `generated-docs/analyse-inputs/**`, `generated-docs/analyse-requirements/**` | `/analyse-inputs`, `/analyse-requirement` |
| `generated-docs/review-inputs/**`, `generated-docs/review-requirements/**` | `/review-inputs`, `/review-requirement` |
| `documentation/<stem>-<date>.md` resolutions document | `/resolve-review` |
| `documentation/amendments-<date>.md` + the transient `## Amendments (pending re-merge)` section | `/amend-requirements` |
| `generated-docs/design-system/design-system-{light,dark}.html` | `/design-system` |
| `generated-docs/export-application/requirements-application.md`, `generated-docs/export-application/fold-report.md` | `/export-application` |
| `wireframes/<scope-slug>/**` | `/wireframe` |
| Every consultant-facing question, batch, and gate summary | all pipelines |

**Exempt** (LLM-only — no human reads them, so none of the rules below apply):

- `documentation/<App>.stadium-assets/**`
- `documentation/*.converted.md` visual-input descriptions
- `blueprints/<scope-slug>/{blueprint.md, scope.json}`
- `prototypes/.specs/<name-slug>/design-spec.md`
- every `.ndjson` sidecar (`draft-claims`, `resolver-answers`, `timing`, per-analysis machine sidecars, …)

**Dual-audience documents are bound in their entirety.** `requirements.md` and `prd.md` are read by both a human and a downstream agent and cannot be reliably partitioned by paragraph — so every rule, including rule 4's pointer quotation, applies throughout.

## Audience (load-bearing, asymmetric)

The human reader is the **consultant**, and only the consultant. Client stakeholders are not an audience for any artefact in this system — do not write for them, and do not gloss framework vocabulary on their behalf.

Analyses are **additionally** read by a downstream consumer that differs by pipeline:

| Artefact | Human reader | Downstream consumer |
|---|---|---|
| `/analyse-inputs` outputs | yes | **`/requirements`** (re-dropped into the corpus / read by the drafter) |
| `/analyse-requirement` outputs | yes | **`/wireframe` `blueprint-architect`** — *optional*, via the per-analysis machine-readable sidecar (the `RF-09` fallback path) |
| `/review-requirement` outputs | yes | **none** — nothing downstream parses a review |
| `/review-inputs` outputs | yes | **none** |
| `generated-docs/requirements/requirements.md` | yes | **`/wireframe`, `/prototype`, `/analyse-requirement`, `/review-requirement`, `/export-application`** |

In every downstream case the embedded machine-readable sidecar + retained `[SRC:]` markers carry the load; plain prose on top does not disturb them. **Reviews have no machine consumer**, so no part of a review needs to be preserved "for the machine".

## Rules

1. **Summary first — the "In plain terms" block.** Every artefact opens with an `In plain terms` section as its **first** section, above the metric grid and the navigation/TOC. It carries two short labelled groups, in order — **What we found** / **What it means for you** — **2–5 sentences total** across both. Default shape is bullets; a character file that calls for a single short lead paragraph satisfies this by keeping the two labelled halves in order (see §R). It is a faithful condensation of content already established (and cited) in the body — it introduces **no new facts** and is **not itself a citation source**. Where a command can change the document, the second group **names that command**.

2. **One idea per sentence; 30 words maximum.** A sentence over the cap is **split**, never compressed — precision is worth more than the cap. Where splitting would change the meaning, leave the sentence intact and let self-validation report it.

3. **Name the actor; use the active voice.** *"The Approver records a decision"*, not *"a decision is recorded"*. Where the actor is the system, say so.

4. **Every pointer carries a quotation of its referent.** A bare `→ §4.1 G-01` costs the reader a lookup. Write `→ §4.1 G-01 "Reach a decision on every uploaded record"` — **at most 8 words, drawn verbatim from the referent's own title or first clause**, in quotation marks. It is a **quotation, never a restatement**: this is what keeps the rule compatible with the canonical-source constraint (*"never paraphrase or redefine"*) — a quote is not a paraphrase. Applies to `→ §N.M` pointers and to bare ID cross-references (`F-06`, `BR-03`, `RPT-01`, `AI-004`, `C-027`) alike, wherever the ID appears in prose a human reads.

   **Exempt:**
   - a pointer whose own text already names its referent — `→ §2.1 Order`, `→ §5 Flow: Approve shipment`. It is already self-contained; a quotation would only repeat it.
   - the referent's *own* definition row — a row does not quote itself.
   - repeated pointers to the same referent inside one table cell.
   - `[SRC: C-NNN]` and `[SRC: <filename>]` provenance tags — they are traceability markers, not reading pointers, and rule 10 governs them.

   Inside a markdown table cell, a quotation containing `|` is truncated before the pipe rather than escaped; the 8-word cap usually settles this first.

5. **No hedges in a normative statement.** Closed list: *may · typically · optionally · generally · when useful*. A normative statement says what is or must be. (`should` is deliberately **not** on the list — it carries real normative weight in requirements prose.)

6. **Conclusion first, reasoning after.** The reader can stop at the first clause of any entry — finding, row, recommendation, answer — and still have the answer. Reasoning, caveats and provenance follow it, never precede it.

7. **Gloss methodology jargon at first use.** The first time a **methodology** term (CTA, CCP, "defensibility score", "disposition", "Jaccard overlap", "inductive/deductive coding") appears in human-readable prose, append a 3–8 word plain gloss in parentheses — e.g. *"CTAs (the actions a user can take on this object)"*.
   - **Do NOT gloss framework vocabulary.** *Surface*, *posture*, *realization*, *sidecar*, *blueprint*, *scope span* and their kin are the consultant's daily working vocabulary. Glossing them is noise the reader pays for.
   - **Do NOT gloss client domain vocabulary.** Domain nouns of the client's product (Order, SKU, Fund, SPV, "yellow sheet data") are defined exclusively by the GLOSSARY methodologies (`analyse-*/GLOSSARY/`). Leave them as-is.

8. **Dense explanatory prose becomes bullets.** A paragraph that stacks three or more clauses onto one subject is a list wearing prose clothing — split it. This is a phrasing change only; it never converts a table, card, or structured section into prose or vice-versa.

9. **Readable generated labels.** Theme names, cluster names, and finding headings the agent coins are written as readable phrases, not verb-starved noun stacks. Where a compressed label is genuinely unavoidable, pair it with a one-line plain gloss.

10. **Keep all traceability — it reassures, it is not noise.** `[SRC: …]` stays in analyses and in `requirements.md`; Location/ID + verbatim Evidence stays in reviews. **No demotion, no hiding, no removal.** The test is that a sentence must still read correctly **if the marker were deleted** — never that the marker is removed.

11. **No marketing, no chatbot warmth (unchanged universal constraint).** Clarity comes from plain words, glosses, and the summary — never from enthusiasm or padding. Severity language in reviews is preserved **verbatim**; the "In plain terms" block must not soften a Blocker/Major into reassurance.

12. **Machinery out of the primary reading path; density stays.** Structured cards/tables/heatmaps, the embedded machine-readable sidecar, and metric lines are unchanged.
    - **Documents with a downstream consumer** (analyses, `requirements.md`) — pipeline-machinery / re-ingestion prose (target-mode applicability, "this Mermaid source survives markitdown conversion…", "Use in /requirements") moves to a **"For downstream use"** section at the foot (a collapsed `<details>` footer in HTML artefacts), out of the human reading path but retained verbatim because the downstream consumer needs it. The embedded sidecar is retained in place.
    - **Reviews** — pipeline-machinery / self-referential text is **removed** from the rendered page. Nothing downstream consumes a review, so there is no footer to preserve it for. Genuine reviewer content (verdict legend, diagnostics) stays, in its existing collapsed `<details>` where applicable.

13. **A gate summary that announces an HTML artefact names its preview.** The artefact opens in the consultant's default browser at write time — *before* the gate — so the gate line must say so, and must name the path as a fallback rather than assert that a tab exists. The sentence is fixed and canonical in `framework/shared/artifact-preview.md`; use it **verbatim**, immediately before the gate's closing question. Do not coin a variant and do not promise a tab.

    This is not decoration. The affordance is **per-workspace** and **fails open** by design, so a gate that says nothing about the preview is what turns a workspace where it was never installed into months of silence — the consultant has no expectation to violate. A gate that names it gets the failure reported the same day.

    Applies to every producer whose artefact is on the `artifact-preview.md` allowlist. Producers of markdown artefacts (`/requirements`, `/generate-prd`, `/export-application`, `/resolve-review`, `/amend-requirements`) have nothing to preview and add nothing.

## Self-validation (soft — reported, never halting)

Add these four assertions to the producing agent's existing self-validation block. Readability has **no verdict function**: a hard gate on an undecidable predicate becomes either a rubber stamp or a false halt, so **no `RF-` predicate is defined here and none may be invented**. A failing assertion is reported in the handback summary and the artefact still ships.

1. No sentence in human-facing prose exceeds 30 words (rule 2) — **or** the over-cap sentences are listed, each with the reason splitting would change its meaning.
2. Every `→ §` pointer and ID cross-reference in human-facing prose carries a quotation of its referent (rule 4).
3. No hedge from the closed list appears in a normative statement (rule 5).
4. The opening summary answers *what we found* and *what it means for you*, and names the command that changes the document (rule 1).

## §R — Reconciliation with existing character voice rules

Existing character files mandate concrete, telegraphic discipline in the structured findings ("speak in counts/named objects/cited findings, not vibes"; "state structural reasons out loud"; "no narrative"). **Those rules are unchanged and continue to govern the structured sections** (object columns, finding articles, tables, diagnostics). This standard adds prose in exactly two places — the **"In plain terms"** block and the **first-use glosses** — and nowhere else. The two are complementary, not contradictory:

- Structured section → existing telegraphic rules apply, verbatim.
- "In plain terms" block + glosses → plain-language rules here apply.
- "No marketing / no warmth" applies to **both** — it is the shared floor.
- A character file specifying the lead as *"2–5 plain-English sentences"* or *"the one sanctioned narrative paragraph"* is **satisfied by rule 1 as written**: the two labelled groups are that lead's structure, not additional prose, and the 2–5-sentence cap is the same cap. No character file needs editing to comply.

A character's *Reader & plain language* block should state this scoping explicitly so the model does not over-apply prose into the structured body or soften findings.
