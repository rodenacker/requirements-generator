<!-- ROLE: asset (analysis reference). Methodology definition for the data-model analyser. Modelled on framework/assets/analyses/user-journeys-reference.md. Industry framing: DAMA-DMBOK Data Modeling & Design — the Data Model is the deliverable (Logical level), an ERD is a *visualisation* of it in a chosen notation. -->

# Data Model analysis reference

> **Method:** Extract the **Logical Data Model** (entities, attributes, relationships, cardinalities, business rules, normalisation notes) from `requirements/requirements.md` once. The Data Model is always rendered as tabular sections. The consultant then picks **none, one, several, or all** of three ER-diagram notations (Crow's Foot, Chen, UML class diagram) to add as visual `<figure>` blocks. Same data, multiple views.

**Output file:** `analyse-requirements/DATA-MODEL/data-model.html` — a self-contained HTML artefact containing the Data Model (always) plus zero or more ERD visualisations (per consultant selection). No external CSS/JS dependencies; viewable by opening `file://` in a browser.

**Analyser agent:** `framework/agents/analyses/data-model-analyser.md`

**Character:** `framework/assets/characters/data-model-analysis.md`.

---

## Industry framing — Data Model vs ERD

Per DAMA-DMBOK and the traditional three-level data modelling stack:

| Level | What | When used | Stakeholders |
|---|---|---|---|
| **Conceptual** | Entities + high-level relationships. No attributes, no PKs. | Earliest scoping; whiteboard with business. | Business analysts. |
| **Logical** (this methodology) | Entities + attributes (conceptual types) + PK/FK + cardinalities + business rules + normalisation (3NF). Platform-agnostic. | Pre-UI, pre-database consultant deliverable. | Data architects, BAs, the consultant. |
| **Physical** | Tables + DBMS-specific types (`VARCHAR(255)`, `TIMESTAMPTZ`) + indexes + storage. | After database choice. | DBAs, database engineers. |

An **ERD (Entity-Relationship Diagram)** is a *visualisation* of any of these levels in a notation: Crow's Foot, Chen, or UML class diagram. The Data Model is the substance; the ERD is the view. This methodology produces a **Logical Data Model** + optional ERD views — the right level for a pre-UI / pre-DB consultant artefact.

---

## Output structure

The artefact has two tiers:

### Section 0 — In plain terms (first visual above the diagram)

A short human-readable lead block (`{{PLAIN_SUMMARY}}`): 2–5 plain-English sentences stating what this analysis is, what it found, and what the consultant should do with it. The ER diagram (entity-relationship diagram — a visual map of entities and their relationships) remains the first visual after this lead. The lead introduces no fact, count, or citation not already present in the body and carries no `[SRC: C-NNN]` of its own. Methodology jargon is glossed at first use: entity (a type of thing the system stores), attribute/field (a data property of an entity), relationship (a named link between two entities), cardinality (how many of one entity relate to how many of another), primary key (the unique identifier of an entity), foreign key (a reference to another entity's primary key). Client domain terms are not glossed — that is the GLOSSARY methodology's job.

### Tier 1 — Data Model (always rendered)

Five tabular sections, in this order:

1. **Entities table** — `id`, `display_name`, `persistence` (`persistent` / `value-object` / `policy`), `description`, `lifecycle_states` (if any), `provenance`.
2. **Attributes table** — `entity`, `attribute`, `conceptual_type` (one of `text` / `number` / `date` / `timestamp` / `boolean` / `enum` / `UUID` / `reference` / `binary`), `nullable`, `pk` (true/false), `fk` (target `entity.attribute` or empty), `notes`, `provenance`.
3. **Relationships table** — `from_entity`, `verb`, `to_entity`, `from_cardinality` (`min..max`), `to_cardinality` (`min..max`), `identifying` (true/false), `provenance`.
4. **Business rules table** — `id` (`BR-NN` zero-padded), `target` (entity id or relationship id), `rule`, `provenance`.
5. **Normalisation notes** — `<ul>` of items, each `{action, target, rationale, provenance}`. Targets 3NF.

Conceptual types only. Platform-agnostic. No DBMS-specific types under any circumstance.

### Tier 2 — ERD views (0..3, consultant-selected)

After the Data Model is extracted, the analyser surfaces a `multiSelect: true` prompt. The consultant picks any combination of:

- **Crow's Foot (Information Engineering)** — industry standard. Endpoint markers disambiguate optionality (`╫` exactly-one, `○` zero-or-one, `<<` zero-or-many, `<` one-or-many). Entity rectangles with attribute compartment.
- **Chen notation** — 1976 academic notation. Entity rectangles + diamond-shaped relationship boxes (verb inside the diamond) + cardinality labels (`1`, `N`, `M`) on the line segments. Attribute compartment omitted (Chen attributes are ovals — too noisy at scale; full attribute list lives in the Tier-1 table).
- **UML class diagram** — matches the existing `§2.4` Mermaid `classDiagram` style. Entity rectangles with title + attribute compartments + multiplicity labels (`1`, `0..*`, `1..*`). Verb label as a UML `«stereotype»`.

**Zero selections is valid** — produces a Data-Model-only output (Tier 1 only, no SVG blocks). DAMA-canonical tabular Data Models are a recognised deliverable form.

---

## Source-of-truth hierarchy

The analyser walks `requirements/requirements.md` in this order:

1. **`§2 Domain model`** — primary source.
    - `§2.1 Concepts` → entities (with persistence type from the concept's classification).
    - `§2.2 Relationships` → edges with cardinalities (verbatim where stated).
    - `§2.3 Aggregates & lifecycles` → attributes + lifecycle states + invariants (business rules).
    - `§2.4 Diagram` → cross-check (e.g. existing Mermaid `classDiagram` if present).
2. **`§4 User goals & stories`** + **`§5 Task flows`** — derived entities (nouns the user manipulates) and derived relationships (verbs that imply edges).
3. **`§6 Requirements`** — attribute constraints and business rules (compliance, validation, audit).
4. **`§7 Data entities`** (when present) — explicit data fields supplementing §2.

If `§2 Domain model` is absent or empty, the analyser degrades gracefully to §4/§5/§6/§7 derivation. Density of `ai-suggested` markers will be high; the soft warning surfaces this in diagnostics.

---

## Attribute granularity in the SVG

For notations with an attribute compartment (Crow's Foot, UML — Chen omits attributes), the SVG shows **key attributes only**: PK + 2–4 most-salient required attributes per entity. Full attribute list lives in the Tier-1 Attributes table — nothing is lost.

For N > 12 entities, all selected notations degrade to entity-name-only rectangles (no attribute compartment) and a layout warning is flagged in diagnostics.

---

## Provenance markers (3 — exhaustive)

Every entity, attribute, relationship, business rule, and normalisation note carries exactly one of:

| Marker | CSS class | When |
|---|---|---|
| `from-domain-model` | `.provenance-from-domain-model` | Content appears verbatim in `§2 Domain model` (any subsection). |
| `derived-from-§N` | `.provenance-derived` | Content was extracted from a named section but is not verbatim in §2. The source section is recorded in a `data-source="§N"` attribute on the element. |
| `ai-suggested` | `.provenance-ai-suggested` | Content was inferred (e.g., a proposed join entity for an M:N, a derived attribute type, a normalisation note). Prefixed with `[AI-SUGGESTED]` in the text content. |

No fourth marker. No item unmarked.

---

## Quality checks (10 hard gates)

All checks operate on the Data Model — they are **independent of which ERD views the consultant selects**. The Data Model must be valid regardless of presentation.

1. **Every entity has a name** — both kebab-case id (`file-log`) and a display name (`File Log`).
2. **Every entity has ≥ 1 attribute.**
3. **Every entity has exactly one PK marked.** Composite PK is allowed (multiple attributes flagged `pk: true` in a single entity); zero or multiple non-composite PKs fail.
4. **Every FK marker on an attribute resolves.** The target `entity.attribute` exists in the entity list, and the target attribute is marked `pk: true` on its entity.
5. **Every relationship's two endpoints exist in the entity list.** No dangling edges.
6. **Every relationship has explicit min/max cardinality on both sides.** `min ∈ {0, 1}`, `max ∈ {1, N}`. Out-of-range or missing values fail.
7. **Every relationship has a verb label** — not empty, not whitespace.
8. **Every M:N relationship either justifies staying M:N (a `notes` field explaining why no association entity is needed) or proposes a join entity** (flagged `ai-suggested` in the entities table and the normalisation notes).
9. **Every business rule names a target entity-id or relationship-id that exists** in this run's tables.
10. **Every entity, attribute, relationship, and business rule carries exactly one provenance marker.**

**Soft check (warning, not gate):**

- **AI-SUGGESTED density.** If > 50% of relationships are `ai-suggested`, emit a `density-warning` line in diagnostics and the handback summary. *"`§2 Domain model` is thin — most relationships were inferred. Enrich `§2` and re-run for higher-confidence cardinalities."* Does not block writing.

---

## Notation-selection sub-step

After all 10 hard checks pass (or the consultant chose Override at Step 8), the analyser surfaces a single `AskUserQuestion` with `multiSelect: true`:

- **Question:** *"The Data Model has been extracted and validated. Which ERD visualisations should be added to the output? Pick none, one, several, or all — the Data Model itself is always rendered."*
- **Header:** `ERD views`
- **Options:**
    1. `Crow's Foot — industry standard, optionality on each side`
    2. `Chen — original 1976 academic notation`
    3. `UML class diagram — matches §2.4 Mermaid style`

Empty selection is **valid**. Cancelling the prompt outright (closing the dialog rather than submitting an empty selection) hands control back to the accept/revise/restart loop, not to silent emission.

---

## Stop-condition

The analysis is complete when:

- Every entity declared in `§2.1` (or derived from §4/§5/§6/§7 when §2 is absent) has a row in the Entities table with at least one attribute and exactly one PK.
- Every relationship declared in `§2.2` (or derived from §5 verbs) has a row in the Relationships table with explicit min/max cardinalities on both sides and a verb label.
- Every aggregate invariant in `§2.3` and every constraint in `§6` is captured as a row in the Business rules table.
- All 10 hard quality checks pass, or the consultant chose Override.
- The consultant chose Accept in the Step 11 accept/revise/restart loop.

---

## Input-coverage asymmetry

`§2 Domain model` carries the entities, relationships, and cardinalities cleanly. The columns it does **not** typically carry:

- **Attribute conceptual types.** When `§2.3` lists an attribute without a type (e.g. "file name"), the analyser infers (`text`) and marks `ai-suggested`.
- **Optionality on each side of a relationship.** `§2.2` often states `[1:N]` without specifying whether the `1` side is `[1..1]` (mandatory) or `[0..1]` (optional). The analyser infers based on aggregate ownership in §2.3 and marks `ai-suggested` where ambiguous.
- **Business rules beyond simple invariants.** Compliance rules, validation logic, and conditional invariants in `§6` are derived (mark `derived-from-§6`).
- **Join entities for M:N.** Rarely declared in §2; almost always inferred. Always flagged `ai-suggested`.

Richer inputs → richer Data Model. Methodology degrades gracefully: with thin `§2`, the model is mostly inferred and flagged.

---

## Output shape (HTML schema)

The artefact is a single self-contained HTML file at `analyse-requirements/DATA-MODEL/data-model.html`. The analyser populates `framework/assets/analyses/template-data-model.html` via documented placeholder substitution. Every substituted value is HTML-escaped before injection (XML-escape inside `<svg><text>` nodes).

### Header placeholders

| Placeholder | Value |
|---|---|
| `{{TITLE}}` | *"Data Model — `<domain>`"* if `§1` declares a domain, else *"Data Model"*. |
| `{{DOMAIN}}` | Verbatim from `§1 Application context > Domain`, else *"(not declared in requirements.md)"*. |
| `{{GENERATED_AT}}` | ISO-8601 UTC, captured at render time. |
| `{{REQUIREMENTS_SHA256}}` | SHA-256 of `requirements/requirements.md` captured at Step 2. |
| `{{ENTITY_COUNT}}` | Number of rows in the Entities table. |
| `{{ATTRIBUTE_COUNT}}` | Number of rows in the Attributes table. |
| `{{RELATIONSHIP_COUNT}}` | Number of rows in the Relationships table. |
| `{{BUSINESS_RULE_COUNT}}` | Number of rows in the Business rules table. |
| `{{AI_SUGGESTED_COUNT}}` | Total items (entities + attributes + relationships + rules + normalisation notes) marked `ai-suggested`. |
| `{{NOTATIONS_SELECTED}}` | Comma-separated list of selected notations (`Crow's Foot, Chen, UML`), or *"none"* if the consultant selected zero. |

### Body placeholders

| Placeholder | Value |
|---|---|
| `{{DIAGNOSTICS_BLOCK}}` | Pre-rendered `<section class="diagnostics">` containing: counts summary line, per-marker provenance summary, the 10 check result lines (PASS/FAIL), the AI-SUGGESTED density-warning line (with `class="hidden"` if ≤ 50%), and (on Override runs) per-flagged-item lines. |
| `{{DATA_MODEL_BLOCK}}` | Pre-rendered `<section class="data-model">` containing the five tables in fixed order (Entities, Attributes, Relationships, Business rules, Normalisation notes). |
| `{{ERD_VIEWS_BLOCK}}` | Pre-rendered `<section class="erd-views">` containing zero-to-three `<figure class="erd-diagram erd-{notation}">` blocks. If the consultant selected zero notations, this placeholder is replaced with `<!-- no ERD views selected -->` and the section is absent (or rendered as a single `<p class="erd-views-empty">No ERD visualisations were selected. Data Model tables above are the deliverable.</p>`). |
| `{{MERMAID_BLOCK}}` | Pre-rendered `<details class="mermaid-source">` containing zero-to-two `<pre>` blocks: one `erDiagram` source if Crow's Foot was selected, one `classDiagram` source if UML was selected. Chen has no Mermaid equivalent. If neither Crow's Foot nor UML was selected, this placeholder renders as `<!-- no mermaid equivalents -->`. |

### SVG conventions

- `viewBox="0 0 1000 H"` where `H` is computed from the entity-grid height — typically 600–900.
- `role="img"` + `aria-label="<notation> ERD for <domain>"` on every `<svg>`.
- All `<text>` nodes XML-escape entity, attribute, and verb strings.
- **Shared entity-placement grid across notations** — `ceil(√N) × ceil(N/cols)` grid, degree-sorted (most-connected first, centred). When the consultant selects multiple notations, the same `(x, y)` coordinates are reused per entity so the visual arrangement is consistent across views.
- Crow's Foot endpoint markers, Chen diamonds, and UML multiplicity labels are emitted per-notation; the entity-box internals follow each notation's convention.
- The tabular Data Model section is the screen-reader-accessible equivalent of any SVG; the SVGs themselves are glance affordances.

### CSS class contract used by the analyser

The template scaffold owns CSS variables, layout, and typography. The analyser emits HTML using the following named classes:

- `.data-model` — outer container for Tier 1 tables.
- `.entities-table`, `.attributes-table`, `.relationships-table`, `.business-rules-table`, `.normalisation-notes` — one per section.
- `.erd-views` — outer container for Tier 2 figures.
- `.erd-diagram` — applied to every `<figure>`; one of `.erd-crows-foot`, `.erd-chen`, `.erd-uml` for the notation-specific styling.
- `.entity-box`, `.entity-name`, `.entity-attribute-list` — inside SVG.
- `.relationship-line`, `.relationship-verb`, `.cardinality-label` — inside SVG.
- `.crows-foot-endpoint`, `.chen-diamond`, `.uml-multiplicity` — notation-specific markers.
- `.provenance-from-domain-model`, `.provenance-derived`, `.provenance-ai-suggested` — exactly one per content row in any table.
- `.ai-suggested` — applied to any cell whose content carries the `[AI-SUGGESTED]` prefix. Renders italic + dim background.
- `.pk-marker`, `.fk-marker` — small inline pill badges in the attributes table.
- `.mermaid-source` — applied to the `<details>` wrapping the Mermaid `<pre>` blocks.
- `.rev-marker` — applied to any row flagged by a failed quality check on an Override run.

The analyser does **not** edit the template's CSS or layout — only the documented `{{placeholders}}` are substituted.

---

## Downstream consumption (handled by `framework/skills/map-data-model-to-ui.md`)

- **Entities** → screen taxonomy. Each `persistent` entity becomes a candidate list-screen + detail-screen pair.
- **Attributes** → form fields on the detail-screen. PK is read-only; nullable attributes are optional fields; enum attributes are dropdowns.
- **Relationships** → cross-screen navigation. A relationship `User → uploads → File` becomes a "Files uploaded by this user" link on the User detail screen and a "Uploaded by" link on the File detail screen.
- **Cardinalities** → list-vs-detail decisions. `1..N` from User to File → User has a list of Files. `0..1` from File to ApprovalRequest → File optionally surfaces an ApprovalRequest summary inline.
- **Business rules** → constraints + validation messages on screens.
- **Normalisation notes** → may surface as global decisions (e.g., "approvals are first-class entities, not edge attributes — give them a dedicated screen").

`framework/skills/map-data-model-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character file and for future downstream design-spec authors.

---

## Voice and stance — readability pointer

The artefact is read by a human (the consultant, sometimes a client stakeholder) **and** consumed downstream by `/wireframe`'s `blueprint-architect`. The human-readability standard is `framework/shared/output-readability.md`, restated operationally in the character (`framework/assets/characters/data-model-analysis.md > Reader & plain language`). The rules are additive and do not relax any quality gate or provenance discipline above:

- The "In plain terms" lead is a faithful condensation — it introduces no fact, count, or citation not present in the body, and carries no `[SRC: C-NNN]` of its own.
- Methodology jargon (entity, attribute/field, relationship, cardinality, primary key, foreign key, ER diagram) is glossed at first use in human-readable prose (the lead, the handback line). Client domain terms are not glossed — that is the GLOSSARY methodology's job.
- The plain-English layer is confined to the lead and first-use glosses. The ER diagram, tables, JSON body, and diagnostics keep their concrete, telegraphic discipline.
- Every `[SRC: C-NNN]` marker is kept verbatim — never demoted or dropped.
