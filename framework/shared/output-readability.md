<!-- ROLE: shared (cross-pipeline prose policy). Referenced by every analysis/review character file's "Reader & plain language" voice block. Canonical definition of the human-audience readability standard — referenced by path, never restated. -->

# Output readability standard (analyses & reviews)

The artefacts produced by `/analyse-requirement`, `/analyse-inputs`, `/review-requirement`, and `/review-inputs` are **read by humans** — the consultant, and sometimes client stakeholders. They must be understandable without prior knowledge of the methodology or of this framework's internal vocabulary.

This standard is **additive**: it layers a comprehension surface on top of the existing artefact. It removes **no** structure, **no** citation, **no** rigour, and it does **not** relax any quality gate. It is referenced (not restated) by each analysis/review character file's *Reader & plain language* voice block. Where it appears to conflict with a character's existing voice rules, the reconciliation in §R below governs.

## Audience (load-bearing, asymmetric)

Both analysis and review artefacts are written for a human reader. Analyses are **additionally** read by a downstream consumer that differs by pipeline:

| Artefact | Human reader | Downstream consumer |
|---|---|---|
| `/analyse-inputs` outputs | yes | **`/requirements`** (re-dropped into the corpus / read by the drafter) |
| `/analyse-requirement` outputs | yes | **`/wireframe` `blueprint-architect`** — *optional*, via the per-analysis machine-readable sidecar (the `RF-09` fallback path) |
| `/review-requirement` outputs | yes | **none** — nothing downstream parses a review |
| `/review-inputs` outputs | yes | **none** |

In every downstream case the embedded machine-readable sidecar + retained `[SRC:]` markers carry the load; plain prose on top does not disturb them. **Reviews have no machine consumer**, so no part of a review needs to be preserved "for the machine".

## Rules

1. **Lead with plain English — the "In plain terms" block.** Every artefact opens with an `In plain terms` section as its **first** section, above the metric grid and the navigation/TOC. It is **2–5 sentences** answering, in order: *what this is · what it found · what to do with it*. It is a faithful condensation of content already established (and cited) in the body — it introduces **no new facts** and is **not itself a citation source**. It uses everyday language; method names may appear but are glossed per rule 2.

2. **Gloss jargon at first use.** The first time a **methodology** term (e.g. CTA, CCP, "defensibility score", "disposition", "Jaccard overlap", "inductive/deductive coding") or a **framework** term (e.g. surface, posture, realization, sidecar) appears in human-readable prose, append a 3–8 word plain gloss in parentheses. Examples:
   - "CTAs (the actions a user can take on this object)"
   - "defensibility score (0–6 — how well the requirement's existence is justified)"
   - "disposition (what to do about the finding: patch, defer, or reject)"
   - **Exemption — do NOT gloss client domain vocabulary.** Domain nouns/terms of the client's product (Order, SKU, Fund, SPV, "yellow sheet data") are **not** glossed here; defining them is the exclusive job of the GLOSSARY methodologies (`analyse-*/GLOSSARY/`). Leave them as-is.

3. **Readable generated labels.** Theme names, cluster names, and finding headings the agent coins are written as readable phrases, not verb-starved noun stacks. Where a compressed label is genuinely unavoidable, pair it with a one-line plain gloss.

4. **Keep all traceability — it reassures, it is not noise.** `[SRC: …]` stays in analyses; Location/ID + verbatim Evidence stays in reviews. **No demotion, no hiding, no removal.** The reader wants to see where each statement came from.

5. **No marketing, no chatbot warmth (unchanged universal constraint).** Clarity comes from plain words, glosses, and the summary — never from enthusiasm or padding. Severity language in reviews is preserved **verbatim**; the "In plain terms" block must not soften a Blocker/Major into reassurance.

6. **Density stays; machinery prose is handled by audience.** Structured cards/tables/heatmaps, the embedded machine-readable sidecar, and metric lines are unchanged.
   - **Analyses** — pipeline-machinery / re-ingestion prose (e.g. "this Mermaid source survives markitdown conversion…", "Use in /requirements", `mmdc` instructions) moves into a collapsed `<details>` footer titled **"For downstream use"**, out of the human reading path but retained because the downstream consumer needs it. The embedded sidecar is retained in place.
   - **Reviews** — pipeline-machinery / self-referential text is **removed** from the rendered page. Nothing downstream consumes a review, so there is no footer to preserve it for. Genuine reviewer content (verdict legend, diagnostics) stays, in its existing collapsed `<details>` where applicable.

## §R — Reconciliation with existing character voice rules

Existing character files mandate concrete, telegraphic discipline in the structured findings ("speak in counts/named objects/cited findings, not vibes"; "state structural reasons out loud"; "no narrative"). **Those rules are unchanged and continue to govern the structured sections** (object columns, finding articles, tables, diagnostics). This standard adds prose in exactly two places — the **"In plain terms"** block and the **first-use glosses** — and nowhere else. The two are complementary, not contradictory:

- Structured section → existing telegraphic rules apply, verbatim.
- "In plain terms" block + glosses → plain-language rules here apply.
- "No marketing / no warmth" applies to **both** — it is the shared floor.

A character's *Reader & plain language* block should state this scoping explicitly so the model does not over-apply prose into the structured body or soften findings.
