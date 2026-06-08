<!-- ROLE: asset (P2 analysis reference). Loaded by framework/agents/analyses-inputs/ooux-analyser.md at activation. -->

# analyses-inputs/ooux-reference.md

**Purpose:** Methodology reference for Object-Oriented UX analysis (Sophia Prater's ORCA process) applied to **raw consultant inputs** enumerated via `requirements/source-manifest.json`. The analyser follows this document literally and exhaustively.

**Used by:**

- `framework/agents/analyses-inputs/ooux-analyser.md` — drives the agent's six-round process plus the eight-check quality sweep.
- `framework/skills/map-ooux-from-inputs-to-ui.md` — uses the object-map structure (specifically the embedded JSON body block) to derive UI inventory entries (downstream consumer; stub).

**Output produced by the analyser:** `analyse-inputs/OOUX/ooux-object-map.html` — self-contained HTML object-map artefact carrying:
- A colour-key legend bar directly under the TOC, above the column-board.
- The canonical OOUX sticky-note column-board (one column per object), under an `<h2>` heading — the object map, the rendered "MUST contain a diagram" deliverable.
- A relationship matrix (tabular fallback).
- An embedded `<pre><code class="language-json" id="ooux-object-map-body">` block carrying the full machine-readable object model (survives markitdown round-trip as fenced JSON; the load-bearing `/requirements` re-ingestion contract).
- A source-roster section (consumed + skipped manifest rows), placed below the object-map body.
- A small `<script type="application/json" id="ooux-object-map-meta">` block in `<head>` carrying counts and the manifest fingerprint (consumed by the drift-detection logic on subsequent runs; not relied on by `/requirements` since markitdown strips `<script>` blocks).
- A collapsed diagnostics block (synonym-merge log, 8 gate results, source roster).

**Sibling:** `framework/assets/analyses/ooux-reference.md` — the requirements-side OOUX reference. The six rounds are inherited verbatim with these adaptations: synonym-merge becomes load-bearing in Round 2, provenance markers reference filenames rather than `§2.1`/`§Task flows` sections, and an 8th quality gate is added (every consumed manifest row must contribute ≥ 1 candidate noun or be marked `irrelevant-to-domain` with a reason).

---

## Upstream input contract

OOUX on the inputs side is **an extraction lens onto raw consultant material**, not a refinement of an already-synthesised domain model. The analyser starts from `requirements/source-manifest.json` and reads every row whose `tier != "Unsupported"`:

- `Native-text` → read `row.original_path` as text.
- `Native-multimodal` → read `row.original_path` as image bytes (Claude's multimodal vision); transcribe visible text + structurally significant observations (object labels on diagrams, ERD entity names, screen artefact names that imply backing objects).
- `Supported-via-MCP` → read `row.converted_sibling` as text (markitdown-converted by the input-handler at orchestrator Step 1).
- `Unsupported` → skip; record `(filename, reason)` in the source roster's Skipped table.

There is no §2.1 anchor to fall back to. Object names are chosen from raw inputs through Round 1 (Discovery) and Round 2 (Objects + synonym merge). Every chosen name is verbatim from one or more sources; no name is normalised or invented.

If `requirements/source-manifest.json` is absent, the orchestrator's Step 1 input-handler invocation guarantees it is created before the analyser runs. If the manifest enumerates zero consumable rows, the analyser halts with an RF-03 analogue rather than producing an empty map.

---

## The ORCA process

Six rounds, executed in order. The analyser does not skip rounds and does not collapse rounds into a single pass — each round's output feeds the next, and round-by-round structure is what makes the methodology auditable on raw material with multiple sources.

### Round 1 — Discovery

For each row in `consumed_rows`, scan the content (text or transcribed visual notes) for candidate noun phrases that name things the consultant's users will interact with: business entities, content types, user-facing concepts.

**Sources** are equal-weight on the inputs side; no priority order. Walk every consumed row; collect every noun candidate found anywhere in the row's content.

A candidate is:

```
{
  name,                                    // verbatim noun phrase as it appears in the source
  source_filename,                         // exactly one filename per candidate; cross-source mentions produce
                                           // multiple candidate entries which Round 2 merges
  source_quote,                            // verbatim ≤ 200 chars containing the noun phrase
  source_excerpt_offset                    // optional: character offset within the source content
}
```

Include synonyms and near-duplicates at this stage; deduplication happens in Round 2. Include candidates that may turn out to be UI artefacts / verbs / attributes (Round 2 will reject them with reasons).

**Round 1 output:** an unfiltered candidate list with provenance (which `filename` each candidate came from). Aggregate count per filename — this is the input to Gate 8.

**No invented candidates.** If a noun is not in any consumed source, do not add it. Round 2's `inferred-from-<filename>` marker is reserved for nouns *implied* by surrounding context in a *named* source — never for nouns the analyser hallucinated.

### Round 2 — Objects (synonym merge is load-bearing)

Refine the Round 1 candidates into a canonical object list. This is the most interpretive step on the inputs side because raw consultant material commonly names the same object differently across sources.

**Merge rules:**

- **Cluster candidates that refer to the same business entity.** Use exact-string matches, case-insensitive matches, plural/singular pairs, abbreviation pairs (when both forms appear and one is the expansion of the other), and obvious paraphrases. **Do not cluster aggressively** — when a cluster is ambiguous (e.g. "Customer" vs "Account" might be the same or might be distinct), keep them separate and surface the question in the diagnostics' synonym-merge log as `unresolved-merge-candidate`.
- **Pick a canonical name per cluster.** Heuristic in order: (1) the verbatim form that appears across the most distinct source filenames; (2) on a tie, the longest verbatim form; (3) on a further tie, the alphabetically-first verbatim form. Never paraphrase the canonical name into a "tidier" form — it must be verbatim from one of the cluster members.
- **Log every merge in diagnostics.** The synonym-merge log records: every literal term collapsed, every source filename that contributed each term, the canonical name chosen, and the heuristic that picked it. The consultant uses this log to audit interpretive decisions.
- **Drop UI artefacts** (buttons, screens, dialog boxes, fields, menu items, modals, toasts) — they belong to the design phase, not the object map. Record the drop in diagnostics with the noun and reason.
- **Drop verbs and processes** (e.g. *"approval"* as an isolated noun — capture it as a CTA on the relevant object).
- **Drop attributes** (e.g. *"price"* is an attribute of *"product"*, not its own object).
- **Retain anything the user thinks of as a noun in the system,** even if it has no behaviour yet.

For every retained object, assign a **provenance marker**:

| Marker | When |
| --- | --- |
| `from-source-<filename>` | The canonical name appears verbatim in exactly one consumed manifest row. |
| `synonym-merged-from-[<filename>, <filename>, ...]` | The canonical name was chosen through a synonym merge across multiple consumed manifest rows. The filenames list every source that contributed a term to the merge. |
| `inferred-from-<filename>` | The canonical name does not appear verbatim in any source but was implied by surrounding context in a single named source. Used sparingly; objects with this marker are surfaced in the artefact's Gaps section. |

No fourth marker is allowed. No object is unmarked.

**Round 2 output:** the canonical object list with provenance markers. Plus the synonym-merge log (which lands in the diagnostics block at render time).

### Round 3 — Relationships

For every pair of objects, ask: *"Does an instance of A meaningfully relate to an instance of B per the inputs?"* Record only relationships that the consultant's users will navigate or reason about, **and** that at least one consumed source provides evidence for. Skip relationships that only exist in implementation (e.g. *"`User` has an audit trail through `AuditLog`"* is not a user-facing relationship unless audit trails are part of the UX).

**Declare cardinality** for every relationship: `1:1`, `1:N`, `N:M`. A nested relationship (an object referenced inside another object's attribute set) must carry its cardinality explicitly — the relationship matrix and the nested reference must agree.

Each relationship:

```
{
  source,                                  // canonical object name
  target,                                  // canonical object name
  label,                                   // one short verb phrase ("belongs to", "contains", "approves")
  cardinality,                             // 1:1 | 1:N | N:M
  also_nested,                             // true if the target is referenced inside source's attribute set; default false
  source_filenames: [<filename>],          // ≥ 1 if not inferred; aggregate across sources
  source_quote                             // verbatim ≤ 200 chars from a single representative source
}
```

**Round 3 output:** the relationship list with cardinality and source citations.

### Round 4 — Calls to Action (CTAs)

For every object, list the actions the user can take **on that object** as named or implied by the consumed sources. Phrase each CTA as a verb in imperative form (*"Create order"*, *"Cancel subscription"*, *"Reassign owner"*). Filter rules:

- Every CTA attaches to **exactly one** object — the object the action operates on. If a CTA seems to act on two objects, decompose it (a *"transfer"* CTA may decompose into *"send"* on the source object and *"receive"* on the target object).
- Every object has **at least one** CTA. An object with zero CTAs is a candidate for demotion to an attribute of another object (re-evaluate in Round 2 if this happens) or for the *display-only* annotation if the consumed sources confirm the object is truly read-only.
- CTAs from process-like content (workflow steps, task lists, user stories embedded in interview notes) are authoritative — every workflow step that names a user action on an object must appear as a CTA on that object.
- Each CTA cites its source: `[SRC: <filename>]` markers in the artefact body; the `source_filename` field in the embedded JSON.

**Round 4 output:** a CTA list per object with source citations.

### Round 5 — Attributes

For every object, list the attributes — the pieces of data the user reads about that object, in the order they matter on screen. Pull from:

- Explicit attribute lists in consumed sources (interview notes that enumerate "we track first name, last name, email, status"; brief sections that describe screens with field lists; ERD-like diagrams in `Native-multimodal` sources).
- Reports / lists / table descriptions that name fields the user sees.
- Constraints / validation language ("must be unique", "format YYYY-MM-DD") for validation-bearing attributes.

Attributes are display-oriented at this stage — not yet form-field-oriented. *"created_at"* is an attribute if users see it; *"id"* generally is not (unless the user's mental model includes a human-readable identifier like *"Order #"*).

Each attribute cites its source: `[SRC: <filename>]` markers in the artefact body.

**Round 5 output:** an attribute list per object with source citations.

### Round 6 — Core Content Priorities (CCPs)

For every object, mark a small subset of attributes — typically 2 to 5 — as **Core Content Priorities**. CCPs are the attributes the user must see on every surface that shows this object: in a list row, in a card, in a search result snippet. They answer the question *"if all you can show is three pieces of data, which three?"*.

**Rules:**

- Every object has **at least one** CCP. An object with zero CCPs is a candidate for demotion to a side-data role (re-evaluate in Round 2 if this happens).
- CCPs are a subset of the Round 5 attribute list — never invented here.
- A CCP that consists of *"id"* alone is a smell. CCPs should include at least one human-meaningful attribute (a name, a title, a status).
- The order of CCPs matters: the first CCP is the primary identifier the user reads. Order CCPs by descending visual prominence.

**Round 6 output:** for every object, the attribute list is partitioned into CCP-marked (ordered) and non-CCP.

`model` (the in-memory object + relationship + CTA + attribute + CCP + synonym-merge-log structure) is **closed** at the end of Round 6. The validate + render steps must not add objects, relationships, CTAs, attributes, or CCPs.

---

## Output presentation

The artefact's surfaces, in rendered (DOM) order — an "In plain terms" lead sits first, then the overview/meta-grid, then a colour-key legend bar directly under the TOC, above the column-board:

0. **In plain terms** (`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}`) — a 2–5 sentence plain-English lead: what this object map is, what it found, what the consultant should do with it. The **first** section, above the meta-grid. A faithful condensation of the map below — it introduces no object, count, or fact not already present, and carries no `[SRC]` of its own. Methodology jargon is glossed at first use here; client domain terms are not glossed (the GLOSSARY methodology owns those). Per `framework/shared/output-readability.md`.

1. **Sticky-note column-board** (`<section id="diagrams">` — an `<h2>` "Object column-board" heading followed by `<div class="object-board">`) — the canonical OOUX visual and the rendered **"MUST contain a diagram" deliverable**. One `<section class="object-column">` per object. Five sticky stacks per column in fixed order: CTAs (green) → Object header with provenance dot (blue) → Core Content / CCP (yellow) → Metadata / non-CCP (pink) → Nested references (blue, dashed border). Empty stacks render with `hidden`. The column-board does not survive markitdown round-trip layout-wise — its text content survives as enumerated list items, but the visual grid is lost. The embedded JSON block (item 3 below) is the primary structural carrier through round-trip; the column-board is supplementary for direct HTML viewing.

2. **Relationship matrix** (`<section id="tables">` with `<table class="rel-matrix">`) — tabular fallback. One row per recorded relationship. Source / label / target / cardinality / nested?. Mirrors the requirements-side template's §4. Survives markitdown round-trip as an MD table.

3. **Machine-readable body block** (`<section id="object-map-body">` with `<pre><code class="language-json" id="ooux-object-map-body">`) — the full machine-readable object model in JSON. See the JSON schema below. **This is the load-bearing markitdown-survival contract.** When the consultant copies the HTML into `input/` and reruns `/requirements`, this block converts to a fenced ```json code block in `.converted.md` and the drafter consumes the full model in one shot.

4. **Source roster** (`<section id="source-roster">`) — table of consumed manifest rows (`filename`, `tier`, `sha256[:8]`, `nouns_contributed`) and table of skipped rows (`filename`, `reason`). Sits below the object-map body — the audit trail establishing which sources fed the map, not the headline.

5. **Diagnostics** (`<details id="diagnostics">`) — collapsed by default. Synonym-merge log, 8 quality-gate results (PASS/FAIL), flagged items (Override-only), `irrelevant-to-domain` source rows (Gate 8 emissions).

Plus the `<head>` carries a small `<script type="application/json" id="ooux-object-map-meta">` block with counts + manifest fingerprint + run number. This block is consulted by the drift-detection logic on subsequent runs but is **stripped by markitdown** and so is not relied on by `/requirements`.

Colour contract for the column-board follows the canonical Prater/OOUX vocabulary:

| Sticky kind        | Color               | What it carries                                                                |
|--------------------|---------------------|--------------------------------------------------------------------------------|
| CTA                | green               | Round 4 verbs (top of column)                                                  |
| Object header      | blue                | Object name + provenance dot                                                   |
| Core Content       | yellow              | Round 6 CCP-marked attributes, ordered by visual prominence                    |
| Metadata           | pink                | Round 5 attributes NOT marked CCP                                              |
| Nested object ref  | blue, dashed border | Round 3 relationships where `also_nested = true`, with cardinality chip        |

---

## JSON body schema (the `<pre><code class="language-json" id="ooux-object-map-body">` block)

```json
{
  "schema_version": 1,
  "generated_at": "<ISO-8601 UTC>",
  "manifest_sha256": "<64-char hex>",
  "target": "prototype | application | (not declared)",
  "run_count": <int ≥ 1>,
  "source_roster": {
    "consumed": [
      { "filename": "<basename>",
        "tier": "Native-text | Native-multimodal | Supported-via-MCP",
        "sha256": "<first 8 chars>",
        "nouns_contributed": <int ≥ 0> }
    ],
    "skipped": [
      { "filename": "<basename>", "reason": "<one-line reason>" }
    ]
  },
  "objects": [
    {
      "name": "<canonical-name verbatim from a source>",
      "provenance": "from-source-<filename> | synonym-merged-from-[<filename>,...] | inferred-from-<filename>",
      "ctas": ["<verb phrase>", ...],
      "ccps": ["<attribute name>", ...],           // ordered; primary identifier first
      "attributes": ["<attribute name>", ...],     // full list including ccps and non-ccps
      "citations": ["<filename>", ...]             // every filename that contributed any field for this object
    }
  ],
  "relationships": [
    {
      "from": "<canonical object name>",
      "to": "<canonical object name>",
      "verb": "<short verb phrase>",
      "cardinality": "1:1 | 1:N | N:M",
      "also_nested": true | false,
      "citations": ["<filename>", ...]
    }
  ],
  "synonym_merges": [
    {
      "canonical": "<canonical name>",
      "merged_from": ["<literal term>", "<literal term>", ...],
      "source_filenames": ["<filename>", ...],
      "heuristic": "most-sources | longest | alphabetical | unresolved-merge-candidate"
    }
  ],
  "quality_gates": [
    { "id": "G1..G8", "result": "pass | fail", "note": "<flagged items if fail>" }
  ],
  "irrelevant_to_domain_rows": [
    { "filename": "<basename>", "reason": "<one-line reason>" }
  ]
}
```

The JSON is **the canonical machine-readable surface**. The rendered column-board and the relationship matrix are presentations of the same data. They must agree (Gate 7 checks this).

---

## Quality checks (run after Round 6, before write)

Every check is a hard gate. If any check fails, the analyser does **not** write the artefact — it surfaces a structured error to the consultant via `AskUserQuestion` Revise / Override / Restart, per `framework/agents/analyses-inputs/ooux-analyser.md > Step 9 — Validate`.

Gates 1–7 are inherited verbatim from the requirements-side OOUX reference. Gate 8 is specific to the inputs-side variant.

1. **Every Object has ≥ 1 CTA.** Objects without CTAs are either incomplete or candidates for demotion. Flag the list.
2. **Every CTA attaches to exactly one Object.** Multi-object CTAs are a methodology violation. Flag the offending CTAs by name.
3. **Every nested Relationship declares cardinality.** A nested reference without an explicit `1:1` / `1:N` / `N:M` annotation breaks the relationship matrix. Flag the offending relationships by source-target pair.
4. **Every Object has ≥ 1 CCP attribute.** Without at least one CCP, the object has no defined snippet view. Flag the list.
5. **No orphan Attributes.** An attribute attached to an object that does not appear in the final object list is a data error. Flag the orphans.
6. **Object provenance markers are exhaustive.** Every object has exactly one of `from-source-<filename>`, `synonym-merged-from-[<filenames>]`, or `inferred-from-<filename>`. No unmarked objects; no fourth marker. The filenames inside the markers must equal `consumed_rows[*].filename` exactly.
7. **Relationship matrix and nested references agree.** If `Order` nests `Customer` with `N:1`, the matrix row `Order → Customer` must also say `N:1`. Flag mismatches.
8. **Every consumed manifest row contributes ≥ 1 candidate noun OR is marked `irrelevant-to-domain` in diagnostics with a one-line reason.** Without this gate, the analyser could silently ingest a manifest row and produce nothing from it, leaving the consultant unable to tell whether the file was scanned thoroughly or skipped under the hood. The gate forces every silent skip to be explicit. The `irrelevant-to-domain_rows` list in the JSON body block is the machine-readable surface for the rows that triggered the explicit-skip path.

---

## Anti-patterns

- **Treating screens as objects.** *"Dashboard"* is not an object. The objects that appear on a dashboard are. Screens belong to the design phase. Even if a brief lists "screens we need", the analyser does not promote screen names to objects.
- **Treating buttons as CTAs.** A CTA is a user intent (*"Approve request"*). The button is the UI affordance. The map captures intent, not affordance.
- **Inventing objects not present in the inputs.** If a noun is not in any consumed source, do not add it. Round 2's `inferred-from-<filename>` marker is reserved for nouns *implied* by surrounding context in a *named* source — never for nouns the analyser hallucinated. Flag a gap and surface the missing concept to the consultant via the Step 9 Revise path.
- **Silently merging synonyms.** Every merge is logged. The synonym-merge log in diagnostics is the audit surface for the most interpretive step on the inputs side. A silent merge ("I knew they meant the same thing") hides reasoning and breaks reviewability.
- **Aggressively merging ambiguous candidates.** When two terms might or might not refer to the same entity, do not merge by default. Keep them separate; record the question as `unresolved-merge-candidate` in the diagnostics. The consultant resolves via the Step 11 Revise loop.
- **Normalising the canonical name.** The canonical name is verbatim from one of the cluster members, not a "tidier" form. "CRM" stays "CRM" unless the inputs themselves expand it.
- **Collapsing rounds.** Do not write objects and CTAs in the same pass. The round-by-round structure is what makes the map reviewable — collapsing rounds hides reasoning and breaks the quality-check sweep.
- **Editorialising.** The analyser is a literal lens onto the consumed inputs. It does not propose new product features; it surfaces structure the consultants already documented.
- **Silently skipping a manifest row.** Gate 8 catches this. Every consumed row either contributes ≥ 1 candidate noun in Round 1 or is recorded in `irrelevant_to_domain_rows` with a reason.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/ooux-inputs-analysis.md` — analytical, thorough, literal, synonym-honest. The reference here defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact is human-read (and re-ingested by `/requirements`), so the analyser also follows `framework/shared/output-readability.md`: it writes the "In plain terms" lead, glosses methodology jargon (object, CTA, CCP, synonym-merge, provenance) at first use in human-readable prose, leaves client domain vocabulary unglossed (GLOSSARY territory), and keeps every `[SRC: <filename>]` marker. The plain-language layer is confined to the lead and first-use glosses; the column-board, matrix, JSON body, and diagnostics keep their concrete, named-object discipline.
