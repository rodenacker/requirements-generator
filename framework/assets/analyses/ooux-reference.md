<!-- ROLE: asset (P2 analysis reference). Loaded by framework/agents/analyses/ooux-analyser.md at activation. -->

# analyses/ooux-reference.md

**Purpose:** Methodology reference for Object-Oriented UX analysis (Sophia Prater's ORCA process). The analyser follows this document literally and exhaustively.

**Used by:**

- `framework/agents/analyses/ooux-analyser.md` — drives the agent's six-round process plus the quality-check sweep.
- `framework/skills/map-ooux-to-ui.md` — uses the object-map structure to derive UI inventory entries (downstream consumer; stub).

**Output produced by the analyser:** `analyse-requirements/OOUX/ooux-object-map.html` — self-contained HTML object-map grid using `framework/assets/analyses/template-ooux.html` as scaffold.

---

## Upstream input contract

OOUX is a **UX-lens refinement** of the BA's domain model, never a parallel inventory. The analyser starts from `requirements/requirements.md > §2 Domain model > Concepts` as the canonical object list. Object names match `§2.1` concept names verbatim; OOUX adds CTAs, relationship-navigation intent, and grid attributes the domain model does not carry.

If §2 Domain model is absent or empty, the analyser falls back to extracting candidate object names from `§Task flows`, `§User stories`, or the document's running prose — flagging the synthesis path in the artefact's frontmatter so the consultant can see the object list was not anchored to a domain-model section.

---

## The ORCA process

Six rounds, executed in order. The analyser does not skip rounds and does not collapse rounds into a single pass — each round's output feeds the next, and round-by-round structure is what makes the methodology auditable.

### Round 1 — Discovery

Read `requirements/requirements.md` in full. Extract every candidate noun phrase that names a thing the consultant's users will interact with: business entities, content types, user-facing concepts. Include synonyms and near-duplicates at this stage; deduplication happens in Round 2.

**Sources, in priority order:**

1. `§2 Domain model > §2.1 Concepts` — canonical.
2. `§2 Domain model > §2.2 Relationships` — names referenced here that did not appear in §2.1.
3. `§Task flows`, `§User stories`, `§Personas` — supplementary noun phrases.
4. Running prose — last resort; flag in the artefact frontmatter when this path is used.

**Output of Round 1:** an unfiltered candidate list with provenance (which section each candidate came from).

### Round 2 — Objects

Refine the Round 1 candidates into a final object list:

- Merge synonyms and near-duplicates. Prefer the §2.1 concept name when one exists.
- Drop UI artefacts (buttons, screens, fields) — they belong to the design phase, not the object map.
- Drop verbs and processes (e.g. *"approval"* as an isolated noun — capture it as a CTA on the relevant object).
- Drop attributes (e.g. *"price"* is an attribute of *"product"*, not its own object).
- Retain anything the user thinks of as a noun in the system, even if it has no behaviour yet.

**Output of Round 2:** the final object list. Every object has a verbatim §2.1 name where possible; objects without a §2.1 anchor are flagged in the artefact with `derived-from: <section>`.

### Round 3 — Relationships

For every pair of objects, ask: *"Does an instance of A meaningfully relate to an instance of B?"* Record only relationships that the consultant's users will navigate or reason about. Skip relationships that only exist in implementation (e.g. *"`User` has an audit trail through `AuditLog`"* is not a user-facing relationship unless audit trails are part of the UX).

**Declare cardinality** for every relationship: `1:1`, `1:N`, `N:M`. A nested relationship (an object referenced inside another object's attribute set) must carry its cardinality explicitly — the relationship matrix and the nested reference must agree.

**Output of Round 3:** the relationship matrix. For each relationship, capture: source object, target object, cardinality, label (one short verb phrase — *"belongs to"*, *"contains"*, *"approves"*).

### Round 4 — Calls to Action (CTAs)

For every object, list the actions the user can take **on that object**. Phrase each CTA as a verb in imperative form (*"Create order"*, *"Cancel subscription"*, *"Reassign owner"*). Filter rules:

- Every CTA attaches to **exactly one** object — the object the action operates on. If a CTA seems to act on two objects, decompose it (a *"transfer"* CTA may decompose into *"send"* on the source object and *"receive"* on the target object).
- Every object has **at least one** CTA. An object with zero CTAs is a candidate for demotion to an attribute of another object (re-evaluate in Round 2 if this happens) or for the *display-only* annotation if the consultant confirms the object is truly read-only.
- CTAs from `§Task flows` and `§User stories` are authoritative — every flow/story step that names a user action must appear as a CTA on the appropriate object.

**Output of Round 4:** a CTA list per object.

### Round 5 — Attributes

For every object, list the attributes — the pieces of data the user reads about that object, in the order they matter on screen. Pull from:

- `§2 Domain model > §2.1 Concepts` attribute lists, when present.
- `§Reports`, `§Lists`, or any section that names what fields a user sees in a grid or detail view.
- `§Constraints` for validation-bearing attributes (required / format / range).

Attributes are display-oriented at this stage — not yet form-field-oriented. *"created_at"* is an attribute if users see it; *"id"* generally is not (unless the user's mental model includes a human-readable identifier like *"Order #"*).

**Output of Round 5:** an attribute list per object.

### Round 6 — Core Content Priorities (CCPs)

For every object, mark a small subset of attributes — typically 2 to 5 — as **Core Content Priorities**. CCPs are the attributes the user must see on every surface that shows this object: in a list row, in a card, in a search result snippet. They answer the question *"if all you can show is three pieces of data, which three?"*.

**Rules:**

- Every object has **at least one** CCP. An object with zero CCPs is a candidate for demotion to a side-data role (re-evaluate in Round 2 if this happens).
- CCPs are a subset of the Round 5 attribute list — never invented here.
- A CCP that consists of *"id"* alone is a smell. CCPs should include at least one human-meaningful attribute (a name, a title, a status).
- The order of CCPs matters: the first CCP is the primary identifier the user reads. Order CCPs by descending visual prominence.

**Output of Round 6:** for every object, the attribute list is partitioned into CCP-marked and non-CCP, with the CCP-marked attributes ordered.

---

## Output presentation

The artefact renders as the canonical OOUX **sticky-note column-board**: one column per object, stickies stacked vertically. Color contract follows the canonical Prater/OOUX vocabulary:

| Sticky kind        | Color               | What it carries                                                                |
|--------------------|---------------------|--------------------------------------------------------------------------------|
| CTA                | green               | Round 4 verbs (top of column)                                                  |
| Object header      | blue                | Object name + provenance dot                                                   |
| Core Content       | yellow              | Round 6 CCP-marked attributes, ordered by visual prominence                    |
| Metadata           | pink                | Round 5 attributes NOT marked CCP                                              |
| Nested object ref  | blue, dashed border | Round 3 relationships where `also_nested = true`, with cardinality chip        |

Pure (non-nested) relationships are recorded in the diagnostics block as a small relationship matrix; the column-board itself does not draw edge-lines between columns (canonical Prater templates omit them and rely on the nested stickies plus the matrix for audit).

---

## Quality checks (run after Round 6, before write)

Every check is a hard gate. If any check fails, the analyser does **not** write the artefact — it surfaces a structured error to the consultant and halts. (See `framework/agents/analyses/ooux-analyser.md > Step 8 — Validate` for the halt contract.)

1. **Every Object has ≥1 CTA.** Objects without CTAs are either incomplete or candidates for demotion. Flag the list.
2. **Every CTA attaches to exactly one Object.** Multi-object CTAs are a methodology violation. Flag the offending CTAs by name.
3. **Every nested Relationship declares cardinality.** A nested reference without an explicit `1:1` / `1:N` / `N:M` annotation breaks the relationship matrix. Flag the offending relationships by source-target pair.
4. **Every Object has ≥1 CCP attribute.** Without at least one CCP, the object has no defined snippet view. Flag the list.
5. **No orphan Attributes.** An attribute attached to an object that does not appear in the final object list is a data error. Flag the orphans.
6. **Object names match §2.1 concept names verbatim where §2 exists.** Spelling drift between the domain model and the OOUX map breaks downstream consumption. Flag mismatches.
7. **Relationship matrix and nested references agree.** If `Order` nests `Customer` with `N:1`, the matrix row `Order → Customer` must also say `N:1`. Flag mismatches.

---

## Anti-patterns

- **Treating screens as objects.** *"Dashboard"* is not an object. The objects that appear on a dashboard are. Screens belong to the design phase.
- **Treating buttons as CTAs.** A CTA is a user intent (*"Approve request"*). The button is the UI affordance. The map captures intent, not affordance.
- **Inventing objects not present in the requirements.** If a noun is not in `§2 Domain model > §2.1 Concepts` and not in `§Task flows` / `§User stories` / running prose, do not add it. Flag a gap and surface the missing concept to the consultant rather than inventing.
- **Collapsing rounds.** Do not write objects and CTAs in the same pass. The round-by-round structure is what makes the map reviewable — collapsing rounds hides reasoning.
- **Editorialising.** The analyser is a literal lens onto the requirements doc. It does not propose new product features; it surfaces structure the BA already documented.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/ooux-analysis.md` — analytical, thorough, literal. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.
