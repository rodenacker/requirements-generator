<!-- ROLE: asset (analysis reference). Methodology definition for the faceted-classification analyser. Industry framing: S.R. Ranganathan facet analysis / colon classification (library science); Rosenfeld, Morville & Arango, Information Architecture: For the Web and Beyond, 4th ed. (O'Reilly, 2015) — the organization, labeling, and search systems treatment. The lens derives the orthogonal, independent attribute dimensions (facets) along which a data-management app's record collections can be sliced — status, type, owner, date-range — each with its value set and a backing data property, plus a facet-value-scoped controlled vocabulary. For a CRUD-heavy, list-dominated app this IS the filter / sort / search specification for list surfaces — the UI-only controls the wireframe anti-fabrication rule exempts but otherwise leaves under-designed. It is a transformation lens (it builds a derived navigation model from §7 data shapes + stated filter/sort needs), not a free-text critique. It never invents a facet, a value, or a backing property. -->

# Faceted Classification & Controlled Vocabulary analysis reference

> **Method:** For every list-bearing / collection surface in scope, derive the **facets** — the orthogonal, independent attribute dimensions along which a user slices the record set (status, type, owner, region, date-range) — each with its **value set**, its **kind**, and a **backing property** that resolves to a §7 data shape. Run the load-bearing analysis the structure makes mechanical: **orthogonality** (is each facet independent of the others, or is one predicting another?). Add a **facet-value-scoped controlled vocabulary** (preferred value label + variants + scope note) to normalise label drift. The facets become the filter-chip / facet-rail / sort-axis specification the list surfaces are designed against; non-orthogonal pairs and undefined value domains become resolver questions before wireframing.

**Output file:** `analyse-requirements/FACETED-CLASSIFICATION/facet-map.html` — a self-contained HTML artefact (no external CSS/JS, no `<script>`, no CDN, no Mermaid runtime; opens via `file://`). **Diagrams-first** section order: Overview → TOC → Diagrams (facet-coverage cards + orthogonality matrix) → Tables (controlled-vocabulary table + non-orthogonality register + filter/sort scaffolding note) → Machine-readable model → Diagnostics. The "diagrams" are CSS-only (facet cards + a matrix table) — no inline SVG, no `svg-overlap-check`.

**Re-ingestion:** the artefact embeds a `<pre><code class="language-json" id="faceted-classification-body">` model that survives the markitdown HTML→MD round-trip as a fenced ```json block. A consultant may re-drop the HTML into `input/`; `/requirements` then ingests the structured facet model, and every facet/value-set marked `[AI-SUGGESTED: AI-NNN | blocking]` reaches the resolver as a mandatory confirmation — which is the path by which this analysis hardens `§6.4` filter/sort UI requirements. This is the load-bearing downstream contract — distinct from the sidecar (below).

**Sidecar:** `analyse-requirements/FACETED-CLASSIFICATION/faceted-classification.sidecar.json` — per `framework/assets/analyses/sidecar-schema.md`. Exposes the **`upstream-only`** role (the blueprint-architect does not consume the facet model at MVP; the analysis is a requirements-improvement aid like `decision-tables`, `five-whys`, and `mvp-slicing`). Emitting it keeps `sidecar_present == true` so selecting this lens in `/wireframe` never trips the `RF-09` legacy-prose fallback. A future `per-surface-facets` architect role that feeds the wireframe filter/sort scaffolding directly is a deliberate, coordinated enhancement — **out of scope here** (see the sidecar section).

**Analyser agent:** `framework/agents/analyses/faceted-classification-analyser.md`

**Character:** `framework/assets/characters/faceted-classification-analysis.md`

---

## Industry framing — facet analysis & faceted classification

Faceted classification predates software: S.R. Ranganathan's facet analysis / colon classification (library science, 1933) replaced a single rigid hierarchy with several independent dimensions a thing could be classified along simultaneously. Its modern, digital form is codified in Rosenfeld, Morville & Arango, *Information Architecture: For the Web and Beyond* (4th ed., O'Reilly, 2015) — facets and controlled vocabularies are core constructs of the organization, labeling, navigation, and search systems that book treats. The analytical pay-off for a data-management app: a collection surface lives and dies on how users slice it, and a **faceted** navigation (independent dimensions combined freely) is the structure that lets a user reach any subset without a pre-baked hierarchy.

The defining property — and the only one this lens can verify doc-only — is **orthogonality**: facets are mutually exclusive *as dimensions* and collectively exhaustive over how the collection is sliced. Two facets are independent iff a record's value on one is uninformative about its value on the other. A facet set that fails this is one dimension wearing two hats and produces redundant filters.

This is a **transformation** lens (it builds a derived navigation model from the spec's own §7 data shapes and stated filter/sort needs), not a free-text critique. It never invents a facet, a value, or a backing property.

---

## The structured object — facets per collection

| Part | Meaning |
|---|---|
| **Collection / list surface** | A surface that renders a *set* of records (a Transactions list, a Files browse). Facets attach to collections, not to single-record detail/edit surfaces. |
| **Facet** | An orthogonal, independent attribute dimension a user slices the collection along (`transaction-status`, `assigned-approver`, `decision-date`). One facet, one dimension. |
| **Kind** | How the facet is sliced and rendered: `enum` (single-select), `multi-enum` (multi-select), `date-range`, `range` (numeric), `boolean`, `text-search`. |
| **Value set** | The controlled set of values a facet can take, drawn from the spec (`status` ∈ {Pending, Approved, Rejected}). For `range`/`date-range`, the bounds; for `text-search`, the searched fields. |
| **Backing property** | The §7 `Shape.Property` (or `F-NN:ParamName`) the facet filters on. The facet *control* is UI-only chrome (exempt from the wireframe `data-prop` closed set), but it must *cite* a backing property that exists in §7 — this is the anti-fabrication anchor. |
| **UI control** | The realisation: filter chips (enum), checkbox facet rail (multi-enum), date-range picker, range slider, toggle (boolean), search box (text-search). Sort-eligible facets also become sort axes. |

Each facet carries a stable **facet ID** (`<collection-slug>-<dimension-slug>`), its **source** (`§7 Shape.Property` / `F-NN` / `UI-NN` / `§6.4` / `§5 <flow>`), and a **derivation marker** (cited vs inferred).

---

## Where facets hide in a requirements document (extraction scan)

| Source | What it yields |
|---|---|
| `§7 Data shapes` | The candidate facet attributes — every **categorical** (enum/status/role/boolean/reference) or **rangeable** (date, numeric with stated bands) property is a facet candidate for the collections that render its entity. |
| `§6.4 UI feature needs` (UI-NN) | Stated filter / sort / search needs — *"user can filter by status"*, *"sortable by date"*, *"search files by name"*. A stated need is a **cited** facet. |
| `§5 Task flows` / `§4 Goals` | The collections themselves — goals/flows with verbs *browse / list / search / filter / find / locate* name the list surfaces facets attach to, and often the dimension a user locates *by*. |
| `§2.3 Aggregates & lifecycles` / `§9 Key terminology` | The **value domains** for status/enum facets (the set of lifecycle states; named categories). |
| `§6.5 Access control (RBAC)` | Role value sets, where an `owner`/`assignee`/`role` facet slices by actor. |

A facet named in a `§6.4` need but whose value domain is absent is still surfaced — with the missing part flagged (`needs-a-threshold` / `[AI-SUGGESTED]`), never guessed.

---

## Facet typing (decidability of orthogonality and completeness depends on this)

| Kind | Signal | Value-domain treatment |
|---|---|---|
| **enum** | a status set (`§2.3`/`§9`), a role set (`§6.5`), a single-choice category | value set is the named set; filter chips / dropdown |
| **multi-enum** | a category where a record can hold several values (tags, labels) | value set is the named set; checkbox facet rail |
| **boolean** | a flag property (`§7`) | {true, false}; toggle chip |
| **date-range** | a date/timestamp property (`§7`) | bounded by a stated min/max where given, else open-ended range; date-range picker |
| **range** (numeric) | a numeric property **with stated bands/thresholds** | the **stated** bands only; range control |
| **un-banded numeric / open-text** | a numeric/open-text property with **no** thresholds stated | **out-of-scope-for-faceting** as a range — flagged `needs-a-threshold`; **never** partition it or invent a boundary. (Open text may still be a `text-search` target — that is allowed, because search needs no value domain.) |

The single most important anti-fabrication rule lives here: an un-banded numeric is **not** silently split into bands to make a tidy range facet. It is flagged as a question for the consultant. (Lifted verbatim in spirit from the `decision-tables` un-banded rule.)

---

## The analyses

### Orthogonality (the load-bearing, derivable analysis)

For each collection, test **every pair** of its facets for independence. Two facets `A` and `B` are **orthogonal** iff knowing a record's value on `A` tells you nothing about its value on `B` (and vice versa). Build the orthogonality matrix (facets × facets, each cell `independent` / `dependent`). A **dependent** pair — `region` predicts `settlement-currency`; `type` predicts the available `status` set — is **not** two facets; it is one dimension expressed twice, producing redundant and confusing filters. Each dependent pair becomes a **non-orthogonality register** row:

- the pair, the **dependency direction** (which value predicts which), the source evidence, and a **collapse / re-derive recommendation** (keep the determining dimension; drop or derive the dependent one);
- `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` when the independence judgement rests on inference rather than stated data (blocking when the pair governs a stated `§4` findability goal); a clear-cut dependency from §7 cardinality is a `[STANDARD-RULE]`-style structural finding cited to §7, not an AI guess.

Orthogonality is **derivable** from the data model. **Which** facets users actually reach for is **not** derivable doc-only — see the standing caveat.

### Coverage (every collection has its slice dimensions)

Every list-bearing surface in scope is walked. A collection with **no** derivable facet (records carry no categorical/rangeable property worth slicing on) is flagged `no-slice-dimension` with a one-line reason — not padded with a manufactured facet. A collection with **only one** facet (or only a free-text search) triggers the soft thin-slice warning (below): the slicing is thin, which usually means `§7`/`§6.4` under-specify the record's attributes.

### Controlled vocabulary (facet-value-scoped, advisory)

For each facet whose values drift in label across the spec (Status vs State vs Stage; {Pending, In-Review, Submitted} used interchangeably for one state), record a controlled-vocabulary row: `preferred value label`, `variant/synonym labels`, `scope note`. This is **facet-value-scoped only** — it reconciles the values *within* a facet. All *entity/term* synonym work belongs to GLOSSARY and is **deferred**, never restated. When the GLOSSARY artefact is present on disk it MAY be seed-read for value labels; it is never required.

---

## Anti-fabrication discipline (load-bearing)

- **A backing property is cited, never invented.** Every facet binds to a §7 `Shape.Property` or an `F-NN:ParamName`. A facet whose backing field is not in §7 (and not an F-NN parameter) is **not added**. The facet control stays UI-only-exempt chrome, but the dimension it filters must be a real, stated property — this is what tightens today's freely-invented filter chrome into provenance-backed scaffolding.
- **A value domain is sourced, never guessed.** Value sets come from `§2.3`/`§9`/`§6.5`/`§7`. An un-banded numeric is flagged `needs-a-threshold`, never partitioned. A category value the spec does not name is not added.
- **An inferred facet is a flagged question.** A facet the spec implies but does not state (the records obviously want a date filter but no `§6.4` need says so) is `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` with a named inference technique and ≥ 1 source anchor — anchorless inference is forbidden.
- **A deterministic house rule is a standard rule, not an inference.** Where a `GR-NN` house rule supplies a behaviour (e.g. pagination always present per `GR-11`, all columns sortable per `GR-12`), mark `[STANDARD-RULE: GR-NN]` — the resolver skips it.
- **Never invent a collection.** Collections trace to `§5`/`§4` list/browse goals and `§7` entities; absent that, no collection is added.

---

## Lane boundary with sibling lenses (analytic — no required cross-read)

Faceted classification overlaps three existing lenses at the edges; draw the lanes by **deliverable**, so the methods don't restate each other:

- **vs `glossary` / GLOSSARY:** the glossary defines **terms and their meanings** (an alphabetical definitions list). Faceted classification defines **the orthogonal axes records are organised along** and how they become filter/sort UI. The seam is the controlled-vocabulary table — keep it **facet-value-scoped** (values within a facet); defer all entity/term synonym reconciliation to GLOSSARY. The analyser MAY `Glob`+`Read` `analyse-requirements/GLOSSARY/*` if present, purely as a value-label seed — exactly as `decision-tables` optionally reads STATE-DIAGRAM. It is **never required** and never a dependency.
- **vs `data-model`:** the data model is the **storage schema** (entities, attributes, cardinality, for persistence). Facets are the **query/navigation dimensions** (how the collection is sliced for retrieval). A storage attribute becomes a facet **only if** a user slices on it; many stored attributes are never facets, and a `date-range` facet spans a stored timestamp without *being* the schema.
- **vs `ooux`:** OOUX gives an object its own screen and CTAs ("Invoice gets a list screen"). Faceted classification gives the *collection of* that object its navigation axes ("the Invoice list is sliced by status × owner × date-range"). OOUX decides what gets a screen; this decides how its list is sliced.

---

## Output structure

### Diagrams (top of document) — CSS only

1. **Facet-coverage cards** — the value, front-loaded. One card per collection, each listing its facets as chips: facet name · kind · value-set preview · backing property · cited/inferred marker. The reader sees the slicing dimensions of every list surface at a glance, and which collections are thin or have no slice dimension.
2. **Orthogonality matrix** — per collection, a CSS table of facets × facets with each cell marked `independent` (✓) or `dependent` (✕ + the dependency direction). Non-orthogonal pairs are highlighted; this is the analytic surface that distinguishes a facet map from a list of attributes. A single-facet collection renders a one-cell note ("one dimension — orthogonality trivial").

### Tables (below the diagrams)

3. **Filter/sort scaffolding note** — per list-bearing surface, the design hand-off: which facets become **filter chips**, which become a **facet rail** (multi-enum), which become **sort axes**, and which fields the **search box** covers. The UI-control specification the wireframe `data-prop` rule leaves exempt-but-undesigned.
4. **Controlled-vocabulary table** — `preferred value label`, `variant/synonym labels`, `scope note`, `facet` — facet-value-scoped rows where label drift exists.
5. **Non-orthogonality register** — one row per dependent pair: `{collection, facet-pair, dependency-direction, evidence, recommendation, marker}`. Blocking rows carry `[AI-SUGGESTED]` + `.provenance-ai-suggested`.

### Machine-readable model + Diagnostics (bottom)

6. The non-collapsed `<pre><code class="language-json" id="faceted-classification-body">` model carrying `{ collections[], facets[], value_sets, orthogonality_matrix, non_orthogonal_pairs[], controlled_vocabulary[] }` for `/requirements` re-ingestion.
7. **Diagnostics** (collapsed): counts summary, the hard-check result lines (PASS/FAIL), the thin-slice / no-slice notes, the un-banded-flag notes, the **standing empirical-validation disclaimer**, and the honest-skip note when no collection was in scope.

---

## Quality checks (hard gates + soft)

All checks operate on the facet model; the model must be valid regardless of how many facets a collection has.

1. **Every facet has a kebab-case id, a display name, a kind, a value set (or an explicit `needs-a-threshold` / `text-search` exemption), and a backing property** — each traceable to a scanned section, OR carrying an `[AI-SUGGESTED]` marker + ≥ 1 anchor for an inferred facet.
2. **Every facet's backing property resolves to a §7 `Shape.Property` or an `F-NN:ParamName`** — no facet binds to a field absent from §7. (The anti-fabrication core: facets cite real properties; the control stays exempt chrome.)
3. **Every value set is sourced from the spec** (`§2.3`/`§9`/`§6.5`/`§7`); no invented value domain; every un-banded numeric is flagged `needs-a-threshold`, never partitioned.
4. **Orthogonality is checked for every facet pair within a collection; every dependent pair appears in the non-orthogonality register** — none silently shipped as two facets. (Orthogonality FAIL is the signature defect this lens exists to catch.)
5. **Every list-bearing surface in scope has ≥ 1 facet OR is flagged `no-slice-dimension` with a reason;** when no collection surface is in scope at all, the honest-skip near-empty artefact is produced (no manufactured facets).
6. **The controlled vocabulary is facet-value-scoped** — it carries only value-within-facet rows; no entity/term synonym reconciliation (deferred to GLOSSARY).
7. **Inferred facets/value-sets carry `[AI-SUGGESTED: AI-NNN | blocking|non-blocking]` + a named technique + ≥ 1 anchor;** no anchorless inference; no facet invents a §7 property.

**Soft check (warning, not gate): thin slice.** If a collection has **only one** facet, or only a free-text search and no structured facet, emit a `thin-slice-warning`: *"This collection is sliced on a single dimension — usually a signal that `§7`/`§6.4` under-specify the record's filterable attributes, not that the analysis is wrong."* Does not block writing.

On any hard-check failure (1–7): do **not** write the artefact; surface the failing checks + flagged items via `AskUserQuestion` with Revise / Override / Restart, per the analyser's Step 7 contract.

---

## Standing disclaimer (always rendered in the artefact)

**Facet design without empirical sort validation.** Orthogonality is *derivable* from the data model and is verified here. But *which* facets users actually reach for — the genuine usefulness and priority of each dimension — is normally validated by live card-sorting / tree-testing, which this doc-only analysis cannot run. Treat the facet set as a **hypothesis to test**, not a settled spec. A plausible-looking, perfectly-orthogonal facet map can still be wrong about how users slice the data.

---

## Five-round discipline

Each round produces a distinct in-memory output. The analyser does not write until Round 5 completes and all hard checks pass (or the consultant chose Override).

- **Round 1 — Collection & facet discovery.** Identify list-bearing surfaces/collections (`§5`/`§4` browse/list/search/filter goals; `§6.4` filter/sort needs). Scan `§7` for categorical/rangeable attributes and `§6.4` for stated filter/sort/search needs. List candidate facets per collection with source IDs. Honest-skip if no collection surface exists.
- **Round 2 — Facet typing & value-set modelling.** Per facet, assign a kind; pull the value domain from the spec; flag un-banded numerics.
- **Round 3 — Backing-property binding & vocabulary.** Bind each facet to its §7 `Shape.Property` / `F-NN`; mark cited vs inferred; build the facet-value-scoped controlled vocabulary. Optionally seed-read GLOSSARY if present.
- **Round 4 — Orthogonality analysis.** Test every facet pair within a collection; build the orthogonality matrix + non-orthogonality register; derive the per-facet UI control and the per-surface filter/sort scaffolding note.
- **Round 5 — Registers + validate.** Build the facet map, orthogonality matrix, controlled-vocabulary table, non-orthogonality register, filter/sort scaffolding note. Run the 7 hard checks + the soft thin-slice check. Compute the (minimal) `upstream-only` sidecar payload.

If a later round invalidates an earlier one (Round 4 reveals two facets are one dimension), loop back and revise — do not paper over it.

---

## Worked example (transaction-import / approval domain)

A Transactions list surface (from a `§5` "review transactions" flow / `§4` "locate transactions quickly" goal):

- `transaction-status` — **enum**, value set {Pending, Approved, Rejected} from `§2.3`, backing `Transaction.CurrentStatus` (§7), cited (`UI-07` "filter by status"). Filter chips; sort-eligible.
- `assigned-approver` — **enum**, value set = the Approver role set from `§6.5`, backing `Transaction.AssignedApprover` (§7), cited. Filter chips.
- `decision-date` — **date-range**, backing `Transaction.DecisionDate` (§7), cited (`UI-09` "sortable by date"). Date-range picker; sort-eligible.
- `amount` — candidate **range**, backing `Transaction.Amount` (§7), but `§7` names **no** thresholds → flagged `needs-a-threshold` (non-blocking); offered as a `text-search`/sort axis only until bands are named.

Orthogonality: `transaction-status` × `assigned-approver` × `decision-date` are mutually independent (status tells you nothing about approver or date). Suppose a candidate `settlement-region` and `settlement-currency` are both proposed — `§7` shows currency is determined by region → **non-orthogonal pair**, register row recommends collapsing to `settlement-region` (currency derivable). Filter/sort scaffolding: status + approver as filter chips, date as a date-range control, status & date as sort axes, name/reference as the search box's fields.

---

## Sidecar projection (downstream context-cost optimisation)

Per `framework/assets/analyses/sidecar-schema.md`, the analyser writes `analyse-requirements/FACETED-CLASSIFICATION/faceted-classification.sidecar.json` exposing exactly the **`upstream-only`** role (per `framework/skills/select-supporting-analyses.md > Static method → architect_roles mapping`):

```json
{ "architect_projection": { "upstream-only": { "notes": "Faceted classification is a requirements-improvement aid; the blueprint-architect does not consume the facet model at MVP. Re-ingestion into /requirements is via the embedded JSON body block, not this sidecar." } } }
```

Full envelope: `schema_version "1"`, `method "faceted-classification"`, `source_path`, `source_sha256` of the HTML at write time, `generated_at`, `truncated false`. Hard cap ≤ 20 KB (trivially met). **Do not invent role keys** — a dedicated `per-surface-facets` role (so the blueprint-architect consumes facets into per-collection-surface filter/sort scaffolding directly) is a deliberate future enhancement requiring a coordinated change across `select-supporting-analyses.md`, `sidecar-schema.md`, `step-02-read-inputs.md`, `step-03-author-blueprint.md`, and the downstream `surface_plan` co-edit set; it is **out of scope** here. (The full facet model is nonetheless emitted into the `#faceted-classification-body` block now, so that future enhancement is pure plumbing, not re-analysis.)

---

## Downstream consumption (handled by `framework/skills/map-faceted-classification-to-ui.md`)

- Each **enum facet** → filter chips (or a dropdown) on the owning collection surface.
- Each **multi-enum facet** → a checkbox **facet rail**.
- Each **date-range / range facet** → a range control (date-range picker / slider).
- Each **boolean facet** → a toggle chip.
- Each **text-search target** → the search box's covered fields.
- Each **sort-eligible facet** → a sort axis (column-sort or a sort control).
- Each **non-orthogonal pair** → a design decision to settle (collapse the redundant filter) before building.

`map-faceted-classification-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character and future design-spec authors. No widening: every control traces to a facet that traces to a §7 `Shape.Property` / `F-NN` / `§6.4` source. Facets scaffold the **UI-only controls the wireframe anti-fabrication rule exempts** (search/sort/filter chips); they do **not** introduce bindable `data-prop` properties.

---

## Stop-condition

The analysis is complete when every collection in scope has its facets derived (or is honestly flagged `no-slice-dimension`); every facet has a kind, a sourced value set (or an `[AI-SUGGESTED]` / `needs-a-threshold` flag), and a backing §7 `Shape.Property` / `F-NN`; every facet pair has been tested for orthogonality with every dependent pair in the non-orthogonality register; the controlled vocabulary is facet-value-scoped; the standing empirical-validation disclaimer is present; all 7 hard checks pass (or Override); and the consultant chose Accept in the handback loop.
