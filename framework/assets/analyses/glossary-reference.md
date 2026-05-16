<!-- ROLE: asset (analysis reference). Methodology definition for the glossary analyser. Modelled on framework/assets/analyses/five-whys-reference.md. Industry framing: domain-vocabulary extraction (Evans 2003 Domain-Driven Design "ubiquitous language"; ISO/IEC/IEEE 24765:2017 software-engineering vocabulary practice) — surface the terms a project actually uses and the definitions the source document gives them, not author a domain dictionary. -->

# Glossary analysis reference

> **Method:** Walk `requirements/requirements.md` extracting domain terms at a consultant-chosen **scope tier** (1 = nouns + roles + statuses → 2 += acronyms → 3 += action verbs → 4 += field names; each tier strictly extends the prior). For every surfaced term, locate every occurrence in the document, record the section references, and look for an **explicit definition** at one of those sites. If a definition is found, lift it verbatim into the artefact and cite the section ref. If no explicit definition is found, surface the term in a separate **"Used without explicit definition"** section with use-site citations only — the analyser never authors a gloss from world knowledge. Across re-runs the artefact is **additive**: prior entries are preserved; widening the scope tier appends new entries.

**Output file:** `analyses/GLOSSARY/glossary.md` — a self-contained markdown document. **No template scaffold:** Glossary is the second MVP analyser to exercise the registry's `template_asset: null` clause (pure markdown, no HTML / SVG / Mermaid). The first was `five-whys`.

**Analyser agent:** `framework/agents/analyses/glossary-analyser.md`

**Character:** `framework/assets/characters/glossary-analysis.md`.

---

## Industry framing — domain vocabulary as extraction artefact

A glossary is a venerable artefact of requirements work:

- **Domain-Driven Design (Evans 2003).** A project's "ubiquitous language" is the shared vocabulary between domain experts, business analysts, and engineers. Its terms are surfaced *from the domain*, not invented by the modeller — the glossary is a record of the language the domain already uses.
- **ISO/IEC/IEEE 24765 (Systems and software engineering — Vocabulary).** Domain-specific vocabularies are built from authoritative sources and cite those sources; un-cited definitions are unsuitable for normative use.
- **Common failure modes.** Authoring definitions from analyst world-knowledge that diverge from the project's actual usage; conflating different terms behind the same gloss; padding the glossary with generic English; silently inventing entries for terms the document never uses.

This analyser sits firmly in the extraction camp. The subject of every entry is a term that **appears in `requirements/requirements.md`**; the definition is either **lifted verbatim from the document** or marked as a **gap** (the term is used but never defined). No glossary entry is authored from world-knowledge.

### Why apply a glossary analyser in this workspace?

Consultants reading a freshly merged `requirements/requirements.md` repeatedly need a single page that lists the domain terms in scope and what each one means *as used in this document*. They currently have to skim the whole spec to build that picture in their head — slow, error-prone, and unaudited. The Glossary analyser delivers that page deterministically and traceably.

| Lens | Methodology | Question answered |
|---|---|---|
| Per-entity lifecycle | state-diagram | What states does this entity move through? |
| Per-scenario interaction | sequence-diagram | How do components talk to each other? |
| Multi-actor process flow | activity-diagram | Who does what, in what order? |
| Actor goals × main flows | use-cases | What does the user want to achieve? |
| Core objects × CTAs × CCPs | ooux | What things does the system manipulate? |
| Per-requirement justification | five-whys | Why does each requirement exist? |
| **Domain vocabulary × definitions** | **glossary** | **Which terms are in scope and what do they mean here?** |

### Why this analyser uses markdown, not HTML

Glossary is alphabetical, definitional text. There is no diagram component (no SVG, no Mermaid, no figure-pair structure). HTML scaffolding adds ceremony without value. The registry's `template_asset: null` clause exists precisely for this case — pure-markdown analyses compose the artefact as a string and write it directly, retaining the SHA-256 + min-bytes verify discipline that every analyser shares. This is the same rationale that put `five-whys` on markdown.

---

## Output structure

The artefact has a fixed top-to-bottom shape. No tier-1 / tier-2 split — every section header is always rendered (sections beyond the active scope tier read *"(populated when scope tier ≥ N)"*).

1. **Header.** Title, generation timestamp, requirements SHA-256, active scope tier.
2. **Glossary-meta** HTML comment carrying the additive-merge cursor (`last_scope_tier`, `last_input_sha256`, `run_count`).
3. **Summary.** Counts: terms defined, terms used without explicit definition, acronyms (if tier ≥ 2), action terms (if tier ≥ 3), field names (if tier ≥ 4), total entries.
4. **Defined terms.** Alphabetical. Each entry: term heading, verbatim definition lifted from `requirements.md`, citation (section ref + a use-count).
5. **Terms used without explicit definition.** Alphabetical. Each entry: term heading, use-count, citation list of use-sites.
6. **Acronyms and abbreviations** (populated when scope tier ≥ 2). Alphabetical. Each entry: abbreviation, expansion (if requirements expands it), or *"used without expansion"* flag with citations.
7. **Action terms** (populated when scope tier ≥ 3). Alphabetical. Each entry: action verb, surfaced object pattern (e.g., *"Approve {Order}"*), citation list.
8. **Field names** (populated when scope tier ≥ 4). Alphabetical. Each entry: field name (as it appears in requirements), the entity it belongs to (if requirements states it), citation list.
9. **Run history.** Append-only list of prior runs (one bullet per run, timestamped, with scope tier and entry-count delta).

---

## Scope tiers

The consultant picks a scope tier at every run. Tiers are **strictly cumulative** — tier `k` includes everything from tiers `1..k` plus the new category introduced at tier `k`.

| Tier | Adds | Examples |
|---|---|---|
| 1 (default for first run) | Domain nouns + actor roles + named status values | *Order*, *Customer*, *SKU*, *Admin*, *Operator*, *Pending*, *Confirmed*, *Rejected* |
| 2 | + acronyms and abbreviations | *KYC*, *AML*, *PO*, *SLA* |
| 3 | + action verbs / domain actions | *Approve*, *Reject*, *Submit*, *Cancel*, *Refund* |
| 4 | + field names | *order_total*, *customer_id*, *created_at* |

The tier scope is enforced as a hard quality gate (gate 5 in §"Quality checks"): a tier-1 entry must not be an action verb or a field name.

The default at first run is tier 1 (the narrowest, most disciplined scope). At every re-run the analyser **proposes `last_scope_tier + 1`** as the default and offers the consultant the broader tiers, "same tier (refresh new terms only)", or any tier they explicitly pick.

---

## Source-of-truth hierarchy

The analyser reads exactly one document — `requirements/requirements.md` — and reads it once. The whole document is in scope:

- `§1 Application context` — domain framing, business drivers, often the source of named statuses and roles.
- `§2 Domain model` — the canonical source of entity / domain-noun definitions.
- `§3 Target users` — actor roles.
- `§4 User goals & stories` — usage sites for nouns, roles, action verbs.
- `§5 Task flows` — usage sites for action verbs; gating-step terms.
- `§6 Requirements` — usage sites for everything; explicit definitions sometimes live in inline rationale phrases.
- `§7 Data entities` — the canonical source of field names and the entities they belong to.
- `§8 Prototype invariants` (`PI-NN`) and `§9 General rules` (`GR-NN`) if present — terms used in policy-level statements.

The analyser **never** reads any other file: not `framework/assets/glossary.md` (that is the cross-agent vocabulary reference, a different artefact), not `framework/state/`, not other analyses outputs, not pipeline-internal artefacts under `requirements/`.

---

## Round 1 — Candidate-term extraction (tokenisation pass)

Walk `requirements/requirements.md` collecting candidate term tokens at the active scope tier.

### Tier 1 candidate sources

- **Capitalised single-word and multi-word noun phrases** that appear ≥ 2 times — these are the domain's recurring nouns. Lowercase domain terms can survive if they appear in conventional positions (subject of a clause in `§2`, header of an attribute table in `§7`, named in `§3` as a role).
- **Role lists** in `§3 Target users` — every named actor / persona.
- **Named status values** appearing in `§6` quoted strings (e.g., *"the order status is `Pending`"*) and in `§5` decision-point branches (e.g., *"if `Approved` …"*).

### Tier 2 additions

- **All-caps tokens of length 2–6** that appear ≥ 1 time and are not common English (filter against a small stoplist: `THE`, `AND`, `FOR`, `NOT`, `MUST`, `MAY`, `SHALL`).
- **Camel/MixedCase tokens** that look like acronyms (`KYC`, `AML`, `POS`).

### Tier 3 additions

- **Modal-led verbs in `§5` step text and `§6` clauses** matching the pattern *"the {actor} {verb}s {object}"* — `verb` is the candidate, `{object}` is recorded for the surfaced "action shape" column.
- Domain-action verbs from a small allowlist when they appear in `§5` / `§6`: *Approve*, *Reject*, *Submit*, *Cancel*, *Confirm*, *Refund*, *Reverse*, *Reconcile*, *Settle*, *Issue*, *Void*, *Suspend*, *Activate*, *Deactivate*, *Assign*, *Unassign*.

### Tier 4 additions

- **snake_case and lowerCamelCase tokens** that appear in `§7 Data entities` attribute tables. The owning entity is the row's entity (from the table heading or row context).
- **snake_case and lowerCamelCase tokens** in `§6` clauses that are clearly field-name references (used as the object of *"the {field} value must …"*, *"set the {field} to …"*).

### Per-token record

Each candidate carries:

```
{
  term,                              // verbatim, as first encountered
  category ∈ {domain-noun, role, status, acronym, action, field},
  occurrences: [{section_ref, snippet}],   // every site
  use_count: int,
  explicit_definition: null | {
    location: section_ref,
    quote: verbatim string,
    pattern: enum (see below)
  },
  owning_entity: null | string       // populated for category == "field"
}
```

---

## Round 2 — Explicit-definition detection

For each candidate, scan its occurrence sites for an **explicit definition pattern**. The patterns (and only these patterns) qualify a snippet as an explicit definition:

| Pattern | Example | Captured definition |
|---|---|---|
| *"A {term} is …"* / *"An {term} is …"* | *"An Order is a documented request from a customer."* | the clause after *"is"* up to the next sentence boundary |
| *"The {term} is defined as …"* | *"The Customer is defined as a registered account holder."* | the clause after *"defined as"* |
| *"{term}:** {definition}"* (definition-list shape — markdown bold-term-followed-by-colon, or `term — definition`, or `term: definition` in a list) | *"`Order`: a documented request from a customer."* | the definition body up to the next list item or blank line |
| *"{term}, which is …"* / *"{term} (i.e., …)"* / *"{term}, i.e., …"* | *"the Approval Token, i.e., the one-time signed value …"* | the appositive clause |
| **§2 Domain-model entity row** for a category=`domain-noun` candidate matching an entity name | the §2 entity description | the entity's "purpose" / "description" cell verbatim |
| **§7 Data-entities attribute row** for a category=`field` candidate | the attribute's "description" cell | the cell verbatim |
| **§3 Target-users entry** for a category=`role` candidate | the role's "description" / "responsibilities" block | the block verbatim |

Only **one** explicit definition is captured per term. If multiple patterns match across multiple occurrences, the **earliest** match in the document wins (by section order, then by line order within the section). This is deterministic and auditable.

A term with `explicit_definition == null` after this round is classified **"used without explicit definition"** — and the analyser **never** synthesises a gloss for it.

---

## Round 3 — Prior-run merge (additive)

If a prior `analyses/GLOSSARY/glossary.md` exists, the analyser:

1. Parses the `<!-- glossary-meta: ... -->` header to read `last_scope_tier`, `last_input_sha256`, `run_count`.
2. Parses each entry's heading and citation list to recover the set of already-surfaced terms.
3. Computes the **merge result**:

   - **Term present in prior file AND in this run's candidate set:** the **prior entry wins** (preserves consultant approval). The new run does not re-extract the entry.
   - **Term present in prior file but NOT in this run's candidate set:** keep the prior entry verbatim. (Possible cause: `requirements.md` changed and the term was removed; the consultant can manually delete the entry if desired. The drift gate in the analyser surfaces this case.)
   - **Term in this run's candidate set but NOT in the prior file:** new entry. Added to the output.

The merge is a **set union with prior-wins resolution**. The artefact is therefore **monotonically growing across runs** unless the consultant manually edits it.

---

## Round 4 — Drift handling

The analyser computes the SHA-256 of `requirements/requirements.md` at run time and compares it to `last_input_sha256` from the prior run's meta header. Three cases:

- **No prior run** — first run. No drift check; treat all surfaced terms as new entries.
- **Hash equal** — `requirements.md` is unchanged. Pure additive widening; no drift prompt.
- **Hash different** — `requirements.md` has changed since the last run. Surface the drift prompt and let the consultant pick:
  - **Append new terms only (default)** — preserve every prior entry verbatim; add only new terms surfaced at the current scope tier.
  - **Re-extract everything** — refresh definitions for every entry from the current `requirements.md`; new definitions overwrite prior ones; the prior file is treated as a list of *which terms to include* but not as a source of definitions.
  - **Abort** — exit without writing. The consultant can manually reconcile.

---

## Round 5 — Render and verify

Compose the markdown in memory section by section per §"Output structure". Compute the SHA-256 of the composed string. `Write` to `analyses/GLOSSARY/glossary.md`. Invoke `framework/skills/verify-artifact-write.md` with the path, the SHA-256, and a `expected_min_bytes` of 512 (a minimum legal render — Header + Meta + Summary + Run-history — clears 512 bytes comfortably; a first-run tier-1 artefact with even one definition row clears 1 KB).

On verify-pass: advance to handback. On verify-fail-twice: halt per RF-04 (write-unverified).

---

## Provenance markers

Every defined-term entry carries exactly one of two provenance shapes:

| Shape | When | Markdown rendering |
|---|---|---|
| Section ref + verbatim quote | An explicit-definition pattern (Round 2) matched | `§N.M — "{verbatim definition}"` |
| Section ref + section name | Definition lifted from a structured table row (§2 entity row, §7 attribute row, §3 role entry) | `§N.M ({entity / attribute / role}) — "{verbatim description}"` |

Every "used without explicit definition" entry carries:

| Shape | Markdown rendering |
|---|---|
| Use-count + use-site refs | `Used {N} times — §{a}, §{b}, §{c}` (first three use-sites; truncate with *"…and N more"* if > 3) |

**No `[AI-SUGGESTED]` markers anywhere in the artefact.** Glossary entries are extraction, not inference; there is no analyser-authored content to mark. If a term's definition cannot be extracted, the term goes in the "used without explicit definition" section — it does not get an `[AI-SUGGESTED]` gloss.

This is the load-bearing invariant. It honours the framework-wide `feedback_ai_suggested_invariant` (never widen the marker into authoring territory) and the `feedback_analyses_are_extraction_not_authoring` rule (analysis copy uses extraction verbs, never authoring verbs).

---

## Quality checks (7 hard gates)

Run after Round 3 (merge) and before Round 5 (render). Each check operates on the in-memory merged entry set.

1. **Every defined-term entry carries a citation.** Citation shape: `§N.M` (section ref) followed by a verbatim quote of the source text. Zero-citation entries fail this check.
2. **No term appears in both "defined" and "used without explicit definition" sections.** Disjoint-section invariant.
3. **Every term in the output is lexically present in `requirements.md`.** Phantom-term check — scan the document for the term string (case-insensitive); any term not found fails.
4. **Every cited section ref resolves to a real section in `requirements.md`.** No invented references.
5. **Tiered scope is respected at the current run's tier.** Tier-1 entries must be `domain-noun`, `role`, or `status` — not `acronym`, `action`, or `field`. Tier-2 entries add `acronym`. Tier-3 add `action`. Tier-4 add `field`. A category outside the tier's allowed set fails the check.
6. **Additive merge preserved every prior entry.** Re-run mode: every term heading present in the prior file must also be present in the new file. (Exception: a term the consultant explicitly chose to refresh under the "re-extract everything" drift branch may have a different definition body, but the heading must still be present.)
7. **No `[AI-SUGGESTED]` marker appears anywhere in the artefact.** Lexical scan; any occurrence fails. (The marker is reserved by the framework's `[AI-SUGGESTED]` invariant; the glossary analyser must not emit it.)

### Failure handling

On any hard-check failure: do **not** write the artefact. Surface `AskUserQuestion` with three options:

1. `Revise — exit so the consultant can edit requirements/requirements.md and re-invoke /analyse-requirement (Recommended)`
2. `Override — proceed and write a known-incomplete artefact (the diagnostics block will record every violation)`
3. `Restart — re-run from Round 1 with a fresh extraction`

On **Revise**: hand back to the orchestrator with a `failed-handback` state.
On **Override**: record each failing check in the Run-history bullet for this run; proceed to render.
On **Restart**: re-enter Round 1. Cap at three fail-Restart cycles; on the fourth, force the Revise path.

---

## Stop-condition

The analysis is complete when:

- Every surfaced term has either a defined entry (with citation) or a "used without explicit definition" entry (with use-site citations).
- All 7 hard quality checks pass, or the consultant chose Override.
- `analyses/GLOSSARY/glossary.md` has been written and `verify-artifact-write` returned `pass`.
- The consultant chose Accept in the handback loop.

---

## Re-run semantics summary

- The cursor (`last_scope_tier`, `last_input_sha256`, `run_count`) lives in the artefact's HTML-comment header. No state file under `framework/state/`.
- The default at re-run is **widen by one tier** (`last_scope_tier + 1`); the consultant can pick the same tier (refresh new terms only) or any wider tier.
- The drift gate fires when `requirements.md` has changed since the last run; the default branch is **append new terms only**, preserving prior entries verbatim.
- The artefact is monotonically growing across runs unless the consultant explicitly chose the "re-extract everything" drift branch or manually edited the file between runs.

---

## Downstream consumption (handled by `framework/skills/map-glossary-to-ui.md`)

The analyser does not author UI primitives, so the downstream mapping is **signal-based**, not affordance-based:

- **Coverage of undefined terms** (count of "used without explicit definition" entries / total entries) → signal for `/requirements` enrichment. A high undefined-term count means the requirements document uses vocabulary it does not define — the consultant should add definitions to `§2 Domain model` (for entities) or `§3 Target users` (for roles).
- **Term-count by scope tier** → signal for design-spec consumers. A vocabulary-rich domain typically needs more form fields, more list columns, more disambiguation in screen titles; the count is a rough proxy for design-surface complexity.
- **Acronym density** (count of tier-2 entries / total entries) → signal for screen-readability review. High acronym density warns that the design system needs an in-app glossary affordance.

`framework/skills/map-glossary-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character file and for future downstream design-spec authors.
