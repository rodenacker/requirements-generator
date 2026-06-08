<!-- ROLE: asset (analysis reference). Methodology definition for the glossary analyser, INPUT-ANALYSIS variant. Sibling — NOT a clone — of framework/assets/analyses/glossary-reference.md (which reads the synthesised requirements/requirements.md). This one reads the RAW consultant material enumerated in requirements/source-manifest.json. Industry framing: establishing a shared, agreed vocabulary (Evans 2003 Domain-Driven Design "ubiquitous language"; ISO 704 / ISO 1087 terminology principles; ISO/IEC/IEEE 24765 software-engineering vocabulary practice; Berry & Kamsties ambiguity work; Frantzi et al. 2000 term extraction). -->

# Glossary analysis reference (input-analysis variant)

> **Purpose — establish a common understanding, not just audit it.** Walk the raw consultant inputs enumerated in `requirements/source-manifest.json`, surface the significant terms, classify each as **domain-specific** (problem space) or **application-specific** (solution space), define each term **from the inputs** (cited `[SRC: <filename>]`), and **rate the shared-understanding maturity** of each term on a 0–4 scale. Then **drive convergence**: where the inputs leave a term undefined, weak, synonymous, or conflicting, the analyser PROPOSES the agreed understanding — a candidate definition, a refinement, or a canonical-term resolution — in a clearly-fenced, marked, blocking, anchored block the consultant confirms. The end state the method works toward is one agreed vocabulary downstream (`/requirements` and design) can use consistently: the project's **ubiquitous language**.

**Output file:** `analyse-inputs/GLOSSARY/glossary.html` — a self-contained, readability-optimised HTML document that reads as a lookup reference, carrying an embedded machine-readable JSON term model for re-ingestion. (The requirements-side sibling is also self-contained HTML; the two differ in source and primary axis, not format — see the comparison table below.)

**Analyser agent:** `framework/agents/analyses-inputs/glossary-analyser.md`

**Character:** `framework/assets/characters/glossary-inputs-analysis.md`

**Template:** `framework/assets/analyses-inputs/template-glossary.html`

---

## Industry framing — a glossary as the engine of shared understanding

A glossary is a venerable artefact of requirements work, and its purpose is alignment:

- **Domain-Driven Design (Evans 2003).** A project's *ubiquitous language* is the shared vocabulary between domain experts, business analysts, and engineers — used identically in conversation, requirements, and design. Establishing it is the central act of taming domain complexity. Terms are surfaced *from the domain*, but where the domain's usage is unsettled, the team must *converge* on one agreed meaning. **Bounded contexts** make legitimate cross-context differences explicit rather than letting people talk past each other.
- **ISO 704 / ISO 1087 (Terminology work — principles, methods, concepts and terms).** A well-formed definition states **essential characteristics** in a **genus + differentia** shape ("an X is a [genus] that [differentia]"), is **non-circular** (does not use the term or a synonym), is **affirmative** (says what a thing *is*, not only what it is not), is **appropriately scoped** (neither too broad nor too narrow), and uses **no figurative language**. This is the yardstick for rating definition maturity and for writing every proposed definition.
- **ISO/IEC/IEEE 24765 / IEEE 830 / ISO/IEC/IEEE 29148.** Requirements specifications carry a definitions/glossary section; vocabularies are built from authoritative sources and **cite** them; un-cited definitions are unsuitable for normative use.
- **Term extraction (Frantzi, Ananiadou & Mima 2000 — C-value/NC-value; TF-IDF).** Classical automatic term extraction ranks candidates by *termhood* (is it a domain-bearing concept?) and *unithood* (does the word sequence cohere as a unit?). These methods assume a large corpus. A consultant project has 5–30 heterogeneous documents — too few for reliable statistics. **The adaptation:** the LLM reader acts as the extractor, using termhood/unithood as *judgement signals*, and **every candidate term carries ≥1 source-tuple** (`filename` + verbatim snippet + use-count). The mandatory source-tuple is what replaces statistical confidence — a term with no `[SRC]` cannot exist in the glossary. Determinism comes from citations, not frequency thresholds.
- **Ambiguity vs vagueness (Berry & Kamsties).** *Ambiguity* = multiple distinct interpretations (homonymy, conflicting usage). *Vagueness* = unclear boundaries of meaning (qualitative adjectives without operationalisation: "user-friendly", "fast", "secure"). Both are requirements risks; the method surfaces vague general qualifiers as their own findings register.
- **Polysemy vs homonymy.** *Polysemy* (one term, related senses) → a single entry with a `notes` disambiguation. *Homonymy* (one spelling, unrelated senses) → separate entries, each flagged.

### How this differs from the requirements-side GLOSSARY

| Axis | requirements-side (`analyse-requirements/GLOSSARY/`) | inputs-side (this method) |
|---|---|---|
| Source | one synthesised `requirements/requirements.md` | many raw inputs via `source-manifest.json` |
| Citation | `§N.M` section refs | `[SRC: <filename>]` (manifest row `filename`) |
| Output | self-contained HTML + embedded JSON | self-contained HTML + embedded JSON |
| Primary axis | scope tiers (nouns→acronyms→verbs→fields) | **classification: domain vs application** |
| Rating | binary (defined / used-without-definition) | **0–4 shared-understanding maturity** |
| Inference | **forbidden** — extraction-only, no `[AI-SUGGESTED]` | **convergence engine** — proposals via the sanctioned, fenced, blocking `[AI-SUGGESTED]` channel |
| Goal | surface vocabulary + expose gaps | **establish** one agreed vocabulary |

The relaxation of the requirements-side's hard no-`[AI-SUGGESTED]` rule is deliberate and bounded: proposals are the *only* authoring-adjacent act, they are always fenced, marked, blocking, technique-named, and source-anchored, and on a `/requirements` round-trip they become mandatory resolver confirmations. This reuses the exact channel `task-analysis`, `user-goal-analysis`, and `business-context-definition` already use; it does not widen the framework-wide `[AI-SUGGESTED]` invariant.

This analyser **never** reads `framework/assets/glossary.md` (the cross-agent BA/UX vocabulary reference — a different artefact) nor the requirements-side `analyse-requirements/GLOSSARY/glossary.html`.

---

## Output structure (template-scaffolded; reads as a reference)

The artefact is laid out top-to-bottom (placeholders substituted into `template-glossary.html`):

0. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead explaining *what this glossary is*: the agreed vocabulary for the project's domain, how many terms are defined, how many are used-but-undefined (flagged for the consultant), and that the consultant should confirm or correct the proposed definitions. The **first** section, above the meta-grid. A faithful condensation of the glossary below — it introduces no term, count, or citation not already present, and carries no `[SRC]` of its own. **The lead explains what the glossary is; it does NOT re-define the domain terms** (they are the glossary's content). Methodology jargon is glossed at first use here (e.g. "used-but-undefined", "alias/synonym", "provenance", "definition source"); client domain terms are not glossed. Per `framework/shared/output-readability.md`.
1. **Overview** — title, subtitle, meta-grid (domain, generated timestamp, manifest fingerprint, source count + tier breakdown, total terms, domain/application split, maturity histogram L0–L4, settled/proposed/disputed tallies, proposal count, and the five open-item counts).
2. **TOC** — static top-level anchors.
3. **Canonical glossary — domain terms** — alphabetical term cards. **The primary content.**
4. **Canonical glossary — application terms** — alphabetical term cards.
5. **Open items (work toward agreement):** five registers — Needs definition (L0/L1) · To refine (L2) · To reconcile (synonym clusters) · To resolve (L4 conflicts) · Ambiguous general terms.
6. **Machine-readable model** — `{{BODY_JSON}}` inside `<pre><code class="language-json" id="glossary-body">`.
7. **Round-trip footer** — static; how `/requirements` adopts the agreed terms.
8. **Diagnostics** (collapsed) — gate results, classification split, proposal audit by kind/technique, discard log, source roster (Consumed + Skipped), run history.
9. **`glossary-meta` HTML comment** — emitted just before `</main>`: `<!-- glossary-meta: manifest_fingerprint=<sha>, run_count=N -->`.

---

## Per-entry schema

Each term carries:

```
{
  term,                       // canonical headword, verbatim or near-verbatim as it appears in the inputs
  part_of_speech,             // noun | noun-phrase | verb | adjective | acronym
  classification,             // "domain" | "application"
  bounded_context,            // null | <named context, e.g. "sales", "fulfilment"> — set only when a term legitimately differs by context
  definition,                 // null | { quote: <verbatim>, source_filename, pattern }   — extraction-grounded ONLY
  maturity_level,             // 0 | 1 | 2 | 3 | 4   (see scale)
  agreement,                  // "settled" | "proposed" | "disputed" | "undefined"  (derived — see below)
  canonical_term,             // "self" | <other term string>   — synonym-cluster convergence pointer
  aliases: [<term string>],   // present only on a canonical entry; the terms that fold into it
  ai_proposal: null | {       // present ONLY when the analyser proposes convergence (see Round 4)
    kind,                     // "definition" | "refinement" | "canonical-resolution"
    text,                     // the proposed ISO-704-shaped definition / reconciling definition / context-split
    ai_id,                    // AI-NNN zero-padded, stable across append-only runs
    blocking: true,           // ALWAYS true
    technique,                // one of the 6 closed-set techniques
    anchor: { snippet, source_filename }   // ≥1 — REQUIRED; an anchorless proposal is forbidden (G2)
  },
  synonyms: [<term string>],  // surface synonyms named in the inputs (distinct from alias-folding)
  acronym_expansion,          // null | <expansion string>  (for part_of_speech == acronym)
  related_terms: [<term string>],
  sources: [ { filename, context_snippet (verbatim ≤200 chars), use_count } ],   // ≥1 — the traceability guard (G1)
  conflicting_usages: [ { source_filename, quote } ],   // populated for maturity_level == 4
  notes                       // null | <disambiguation / polysemy note / boundary note>
}
```

**`agreement` is derived, not free-chosen:**
- `settled` — `maturity_level == 3`, OR a term whose `ai_proposal` the consultant confirmed in a prior run (the proposal is promoted to a cited/accepted `definition`).
- `proposed` — carries an unconfirmed `ai_proposal`.
- `disputed` — `maturity_level == 4` with no confirmed resolution yet.
- `undefined` — `maturity_level == 0` with no proposal emitted yet.

`canonical_term`/`aliases` capture synonym-cluster convergence: one entry is canonical (`canonical_term == "self"`); each alias entry sets `canonical_term` to the canonical headword and is folded into the canonical card in the rendered HTML (not given its own card), while still appearing in the JSON body.

---

## The 0–4 shared-understanding maturity scale

This is the rating the method assigns to every core-glossary term — how *settled/agreed* the term currently is in the source material — and it drives which convergence proposal (if any) the analyser emits.

| Level | Name | Criteria | Convergence action (Round 4) |
|---|---|---|---|
| **0** | **Undefined** | The term is used in ≥1 source but has **no definition anywhere** in the inputs. No shared understanding exists. | Propose a candidate **definition**. |
| **1** | **Implicit / Assumed** | Meaning is only inferable from usage context; never stated explicitly. | Propose a candidate **definition**. |
| **2** | **Partial / Contested** | An explicit definition exists but is **circular**, **incomplete**, **too broad/narrow**, uses undefined terms, or otherwise violates ISO 704 (missing genus or differentia). **Record the specific violation.** | Propose a **refinement**. |
| **3** | **Settled** | Clear, non-circular, ISO-704-compliant (genus + differentia), and **consistent** across all occurrences. Already shared. | None — leave as-is. This is the target state. |
| **4** | **Conflicting** | **Multiple incompatible definitions** across documents or contexts. | Propose a **canonical-resolution**: unify, or an explicit context-split. |

A term can legitimately hold more than one settled meaning **across distinct bounded contexts** — that is a context-split (Round 4), not a conflict; the entries carry `bounded_context` and `notes`.

---

## Source-of-truth hierarchy (per-tier ingest)

The analyser reads the manifest once, then each consumable source per its tier (identical to every other inputs-side analyser):

- `Native-text` / `Native-multimodal` → `Read row.original_path` (multimodal surfaces image bytes; transcribe visible text + structurally significant observations).
- `Supported-via-MCP` → `Read row.converted_sibling` (already converted by the input-handler; never re-invoke markitdown).
- `Unsupported` → skip; record `(filename, reason)` for the Skipped roster.

Raw inputs have **no `§N.M` section structure** — citations are `[SRC: <filename>]` against the manifest row's `filename`, optionally with a short locator phrase in prose.

---

## Round 1 — Candidate-term extraction (multi-source)

Walk every consumed source and harvest candidate terms. Each candidate carries ≥1 **source-tuple** `{ filename, context_snippet (verbatim ≤200 chars), use_count }`. Candidate sources, in priority order:

- **Recurring noun phrases** (capitalised or domain-salient) appearing across ≥1 source — the domain's nouns (entities, roles, statuses, artefacts).
- **Acronyms / abbreviations** — all-caps tokens length 2–6 (stoplist `THE AND FOR NOT MUST MAY SHALL MVP`); MixedCase acronyms (`KYC`, `AML`).
- **Domain action verbs** when they name a business operation (Approve, Reject, Submit, Reconcile, Settle, …).
- **Technical / system tokens** — API/endpoint/service/schema/field names, UI element names (these will classify as *application*).
- **Qualitative adjectives** — candidate ambiguity-risky general qualifiers for the D0 check.

LLM-as-extractor adaptation of C-value/NC-value + TF-IDF: prefer multi-word units that cohere (unithood) and concepts that are domain-bearing rather than general (termhood); use cross-document spread as a salience signal. **No statistical corpus is required or assumed** — the mandatory source-tuple is the rigour guarantee.

State per-candidate-class counts aloud.

## Round 2 — Classification (domain vs application; ambiguity lane; discard)

For each candidate, apply the **decision tree (first match wins)**:

- **D0 — Ambiguity-risky general qualifier?** A vague qualitative adjective whose boundaries of meaning are unclear (Berry & Kamsties): *user-friendly, fast, slow, secure, flexible, intuitive, scalable, robust, simple, efficient, seamless, reliable, modern, easy, performant, responsive, lightweight, powerful*, etc. → route to the **`ambiguous_general`** findings register (with `[SRC]` use-sites and the "needs an operationalised definition" note). **Not** a core-glossary entry.
- **D1 — Domain-specific (problem space)?** Vocabulary the business/domain experts use — entities, roles, statuses, business operations, domain artefacts. → `classification: domain`; set `bounded_context` only if the term legitimately differs by context.
- **D2 — Application-specific (solution space)?** Vocabulary about the system/implementation — UI elements, screens, technical components, API/data/field names, system states. → `classification: application`.
- **D3 — Pure general English, not ambiguity-risky?** (e.g. "information", "process", "user" used generically with no domain-specific meaning) → **discard**; record in the Diagnostics **discard log** with a one-line reason (so the consultant can audit what was dropped). Never pad the glossary with these.

State the classification split aloud (e.g. "Round 2: 14 domain, 9 application, 4 ambiguous-general routed to findings, 7 general discarded").

## Round 3 — Definition detection + maturity rating + conflict/synonym detection

**Definition detection** — for each core-glossary term, scan its source occurrences for an **explicit definition pattern** (only these qualify; earliest match by manifest-row order then in-file order wins):

| Pattern | Example |
|---|---|
| *"A {term} is …"* / *"An {term} is …"* | *"An Order is a documented request from a customer."* |
| *"The {term} is defined as …"* | *"The Customer is defined as a registered account holder."* |
| Definition-list shape (`{term}: {definition}`, `**{term}** — …`, list item with bold/code term + colon) | *"`SKU`: a stock-keeping unit identifier."* |
| Appositive (*"{term}, which is …"* / *"{term} (i.e., …)"* / *"{term}, i.e., …"*) | *"the Approval Token, i.e., the one-time signed value …"* |
| Any source's **structured definition-list / labelled glossary row** matching the term | a glossary slide or a "Definitions" table row |
| Any source's **data/attribute table row** whose name matches the term | a schema/field table |
| Any source's **role / entity entry** matching the term | an org-chart box or a persona card |

If a pattern matches, set `definition = { quote (verbatim), source_filename, pattern }`.

**Maturity rating** — assign `maturity_level` per the 0–4 scale. A term with no matched definition is L0 (Undefined) unless its meaning is clearly inferable from usage, in which case L1 (Implicit). A matched-but-weak definition is L2 (record the ISO-704 violation in `notes`). A clean, consistent, ISO-704-compliant definition is L3.

**Conflict detection (L4)** — if a term has **multiple incompatible definitions** across sources, set `maturity_level = 4`, populate `conflicting_usages` with each `{ source_filename, quote }`, and route it to the **`to_resolve`** register.

**Synonym detection** — group terms that name the **same referent** across the inputs (e.g. *customer* / *client* / *account holder*). For each cluster, route to the **`to_reconcile`** register. Distinguish **polysemy** (keep one entry + `notes`) from **homonymy** (separate entries, flagged in `notes`).

State the maturity histogram + conflict/synonym counts aloud.

## Round 4 — Convergence proposals (the engine)

This is the method's signature pass and its primary risk surface. For each case below, emit an `ai_proposal`. **Every proposal is `blocking: true`, carries exactly one closed-set `technique`, and carries ≥1 `anchor` `[SRC]`. A proposal with no anchor does not exist (G2). A proposal is never merged into the cited `definition` field (G3).**

| Trigger | `kind` | Allowed `technique` | What the proposal contains |
|---|---|---|---|
| Term at L0 / L1 | `definition` | `genus-differentia-synthesis` · `usage-context-abstraction` · `domain-analogue-mapping` | one ISO-704-shaped candidate definition |
| Term at L2 | `refinement` | `genus-differentia-synthesis` · `usage-context-abstraction` | an ISO-704-compliant rewrite of the weak definition |
| Synonym cluster (`to_reconcile`) | `canonical-resolution` | `synonym-merge` | a proposed `canonical_term`, the aliases that fold into it, and one reconciling definition |
| Conflict at L4 (`to_resolve`) | `canonical-resolution` | `conflict-unify` · `context-split` | either one reconciling definition (unify) OR explicit context-qualified terms with `bounded_context` (split) |

**Closed technique set:** `genus-differentia-synthesis | usage-context-abstraction | domain-analogue-mapping | synonym-merge | conflict-unify | context-split`.

**STOP rules.** (1) **No proposal on an L3 settled term** — it is already shared. (2) **Anchor floor** — every proposal ladders from a verbatim snippet that actually appears in a consumed source; never from world knowledge with no anchor. (3) **Single proposal per term/cluster** — do not emit competing proposals; pick the best and note alternatives in Diagnostics. (4) **Genus-differentia shape** — every proposed/refined definition states a genus and a differentia, is non-circular, affirmative, and free of figurative language (ISO 704).

State the proposal shape aloud (count by kind + technique).

## Round 5 — Assemble register + open-items + agreement facets

- Assemble the **canonical glossary**: domain terms then application terms, alphabetical; alias entries fold into their canonical entry's card (but remain in the JSON body).
- Build the five **open-item registers** (framed as work toward agreement): `needs_definition` (L0/L1), `to_refine` (L2), `to_reconcile` (synonym clusters), `to_resolve` (L4 conflicts), `ambiguous_general` (vague qualifiers from D0).
- Set each entry's `agreement` facet (derived per the schema rule).
- Close the collections. Validation (next step) emits gate results, never new entries.

---

## Prior-run merge (additive)

Identical philosophy to the requirements-side glossary. If a prior `glossary.html` exists and `drift_mode != "re-extract"`:
- Prior entries are preserved verbatim (keyed by term); **consultant-confirmed agreements** (a term whose proposal was accepted, now `settled`) are preserved as settled.
- New terms from new manifest rows are appended.
- A new candidate colliding with a prior term: prior wins.
- `re-extract` refreshes all bodies and re-mints `AI-NNN` from `AI-001`.

The artefact is monotonically growing across runs unless the consultant chooses re-extract or manually edits.

---

## Quality gates (hard gates)

Run after the collections close and before the write. Each captures `{ gate_id, status, flagged_items }`.

- **G1 — Provenance.** Every core-glossary term carries ≥1 `[SRC: <filename>]` source-tuple; every cited `definition` has a verbatim quote + a `source_filename` matching a `consumed_rows[*].filename`. Flag unsourced terms/definitions.
- **G2 — Anti-confabulation.** Every `ai_proposal` is `blocking: true`, carries exactly one closed-set `technique`, carries ≥1 anchor `[SRC]`, and matches its `kind`↔trigger (definition→L0/L1; refinement→L2; canonical-resolution→synonym cluster or L4). **No proposal on an L3 term.** No core definition authored from world knowledge outside this channel. Flag offenders + the missing element.
- **G3 — Field separation.** The cited `definition` and the `ai_proposal` are never presented as one; they render in distinct blocks (`.cited-definition` vs `.ai-proposal`). Flag any term that mixes them.
- **G4 — Classification.** Every core-glossary term has `classification ∈ {domain, application}` (exactly one); no discard-class term leaked into the core; every ambiguity-risky qualifier is in `ambiguous_general`, not the core. Flag mis-routed terms.
- **G5 — Maturity & agreement validity.** `maturity_level ∈ {0..4}`; L4 has non-empty `conflicting_usages`; L3 has a cited ISO-704-shaped definition; L0 has null `definition`; `agreement` derives consistently from level + confirmation state. Flag invalid rows.
- **G6 — Lexical presence.** Every core term and every findings term is lexically present in ≥1 consumed source (phantom-term / stale-inheritance guard). Flag phantoms.
- **G7 — Canonical convergence.** Every synonym cluster resolves to exactly one `canonical_term`; every alias points to a present canonical entry; no two canonical entries share a referent without an explicit context-split (`bounded_context` set on both). Flag offenders.
- **G8 — Additive-merge preservation.** On a non-`re-extract` re-run, every prior term, confirmed agreement, and resolution is present in the merged set. Flag dropped prior items.
- **G9 — Coverage.** Every `consumed_rows` entry contributes ≥1 candidate OR is marked `irrelevant-to-glossary` with a one-line reason. Flag silently-skipped sources.
- **G10 — Self-containment / round-trip.** Artefact begins `<!doctype html>`; no `<script>`, no external `href`/`src`, no Mermaid; exactly one `glossary-meta` comment; the `glossary-body` JSON parses and contains every term, every proposal (with full `ai_proposal`/anchor), and every register; no literal `{{...}}` remain. Flag violations.

### Failure handling

On any gate failure: do **not** write. Surface `AskUserQuestion` with:
1. `Revise — exit so the consultant can enrich input/ and re-invoke /analyse-inputs (Recommended)`
2. `Override — proceed and write a known-defective report (Run-history records every violation)`
3. `Restart — re-run from Round 1`

On Revise → `failed-handback`. On Override → record violations in the Run-history bullet; proceed. On Restart → re-enter Round 1; cap at three fail-Restart cycles, then force Revise.

---

## Anti-patterns

- **Do not author a definition outside the proposal channel.** A cited `definition` is a verbatim quote from a source. A proposed definition lives only in `ai_proposal`, fenced and marked. There is no third path. (G1, G2, G3.)
- **Do not emit an anchorless proposal.** Every proposal ladders from a verbatim snippet in a consumed source via a named technique. (G2.)
- **Do not propose on an L3 settled term.** It is already shared; a proposal there is noise. (G2.)
- **Do not pad the glossary with general vocabulary.** Discard non-risky general English (logged); route vague qualifiers to the ambiguity register. (G4.)
- **Do not collapse two referents into one canonical term without evidence,** and do not split a single concept into two canonical entries. Synonym/conflict resolution is a *proposal* the consultant confirms. (G7.)
- **Do not inflate a maturity level to dodge a finding.** A weak definition is L2 with the violation recorded; a contradiction is L4. Sparsity and conflict are signals, not defects.
- **Do not read `framework/assets/glossary.md` or `analyse-requirements/GLOSSARY/glossary.html`.** This method is input-grounded and stand-alone; loading either conflates artefacts.
- **Do not bundle external JS / CSS / Mermaid / fonts / CDN.** Self-contained HTML only; the embedded JSON lives in `<pre><code class="language-json">`, never a `<script>` (markitdown strips `<script>`).
- **Do not paste the artefact body into the conversation.** It is on disk; the consultant opens it in a browser.

---

## Stop-condition

Complete when: every core term carries a maturity rating and either a cited definition or a fenced proposal (or an honest `undefined` with a needs-definition register entry); every synonym cluster and conflict has a proposed resolution; all hard gates pass (or were Override'd); the artefact is written and `verify-artifact-write` returned `pass`; and the consultant chose Accept.

---

## Downstream consumption — establishing the canonical vocabulary in `/requirements`

When the consultant copies `glossary.html` into `input/` and re-invokes `/requirements`, the input-handler classifies it `Supported-via-MCP` (markitdown → `glossary.html.converted.md`, preserving the `glossary-body` JSON as a fenced code block and the `[SRC]` / `[AI-SUGGESTED]` markers as literal text). The drafter then:

- adopts every **settled** (L3 or consultant-confirmed) definition as the **canonical vocabulary** — `/requirements` uses these terms consistently and seeds `§2 Domain model` / `§7 Data entities` from them;
- treats every **`[AI-SUGGESTED: AI-NNN | blocking]`** proposal (definition, refinement, canonical-resolution) as a **mandatory resolver confirmation** — the consultant validates each proposed meaning, refinement, or canonical-term choice before it anchors a requirement;
- uses the `canonical_term`/`aliases` map to avoid drafting the same concept under multiple names.

`map_skill` is `null`: a glossary produces a vocabulary artefact, not a UI inventory; its consumer is `/requirements`, not a design-spec/wireframe author.

---

## References

- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software.* Addison-Wesley. (Ubiquitous language; bounded contexts.)
- ISO 704:2022, *Terminology work — Principles and methods*; ISO 1087:2019, *Terminology work — Vocabulary*. (Definition principles: genus-differentia, non-circularity, essential characteristics.)
- ISO/IEC/IEEE 24765:2017, *Systems and software engineering — Vocabulary*; IEEE 830-1998 §1.3; ISO/IEC/IEEE 29148. (Glossary section; cited definitions.)
- Frantzi, K., Ananiadou, S., & Mima, H. (2000). "Automatic Recognition of Multi-Word Terms: the C-value/NC-value Method." *Int. J. on Digital Libraries* 3(2), 115–130. (Termhood/unithood.)
- Berry, D. M., & Kamsties, E. (2004). "Ambiguity in Requirements Specification" / *Ambiguity Handbook*. (Ambiguity vs vagueness.)
- ISO 30042:2019, *TermBase eXchange (TBX)*. (Term-entry structure inspiration: status, synonyms, related terms.)

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/glossary-inputs-analysis.md` — literal, citation-bound, extraction-first, convergence-disciplined. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact is human-read (and re-ingested by `/requirements`), so the analyser also follows `framework/shared/output-readability.md` (restated in the character's *Reader & plain language* block, so no `framework/shared/` read is needed): it writes the "In plain terms" lead explaining *what the glossary is* — the agreed vocabulary for the project's domain, term/undefined counts, and what the consultant should do — glosses methodology jargon (used-but-undefined, alias/synonym, provenance, definition source) at first use in human-readable prose, leaves client domain vocabulary entirely unglossed (defining domain vocabulary is the glossary's whole job, so this rule is critical here), and keeps every `[SRC: <filename>]` marker. The plain-language layer is confined to the lead and first-use glosses; the term cards, open-item registers, JSON body, and diagnostics keep their concrete, telegraphic, citation-bound discipline.
