<!-- ROLE: asset (analysis reference). Methodology definition for the crud-coverage analyser. Industry framing: information-engineering entity-function matrix (Martin & Finkelstein, c. 1981); BABOK v3 #39 Roles and Permissions Matrix; TMAP CRUD matrix. The lens crosses every data entity against the four lifecycle operations (Create / Read / Update / Delete) and asks, mechanically, whether each operation has a delivering function — surfacing the operation nobody wrote a use-case for as an empty cell rather than as silence. -->

# CRUD / Entity-Lifecycle Coverage analysis reference

> **Method:** Build a **per-entity coverage matrix** crossing every data entity in `requirements/requirements.md` against the four lifecycle operations (`C` create, `R` read, `U` update, `D` delete/archive). Each cell is given a **coverage verdict** — *delivered* (a function/flow/UI delivers it), *granted-not-delivered* (§6.5 RBAC grants the right but no function delivers it), *forgotten* (an expected operation with no delivery and no grant), or *intentional* (a deliberately-narrow lifecycle). The matrix doubles as a screen-and-action checklist against the blueprint; the holes become resolver questions before wireframing.

**Output file:** `analyse-requirements/CRUD-COVERAGE/crud-matrix.html` — a self-contained HTML artefact (no external CSS/JS; opens via `file://`). **Diagrams-first** section order: Overview → TOC → Diagrams (coverage heatmap + optional role view) → Tables (traceability matrix + lifecycle-hole register + plain matrix) → Diagnostics.

**Sidecar:** `analyse-requirements/CRUD-COVERAGE/crud-coverage.sidecar.json` — per `framework/assets/analyses/sidecar-schema.md`. Exposes the `screen-inventory-entity-bijection` and `per-screen-cta-set` roles.

**Analyser agent:** `framework/agents/analyses/crud-coverage-analyser.md`

**Character:** `framework/assets/characters/crud-coverage-analysis.md`

---

## Industry framing — the entity-function matrix

The CRUD matrix grew out of the entity/process clustering step of information engineering (James Martin & Clive Finkelstein, c. 1981): cross every entity against every function and record which functions create, read, update, or delete each entity. Two adjacent lineages converge on the same artefact:

- **TMAP CRUD matrix** (test management) — the matrix as a coverage/consistency check: every entity needs a create path, a read path, an update path, and a delete path across the function set, unless its lifecycle is intentionally narrower. https://www.tmap.net/wiki/crud/
- **BABOK v3 #39 — Roles and Permissions Matrix** — the *role × entity × operation* view: which role may perform which operation on which entity. This is the optional role view (below), not a separate method.

The coverage rule (the analytical lens): **every persistent entity needs ≥ 1 Create, ≥ 1 Read, ≥ 1 Update, and ≥ 1 Delete (or archive/retire) path across the function set — unless its lifecycle is *intentionally* narrower.** An absent operation is a candidate defect (a *forgotten* hole); an absent-and-intended operation is a documented exception (an *intentional* narrowness).

This is a **transformation** lens (it builds a derived coverage model from the spec's own entities and functions), not a free-text critique. It does not invent entities, functions, or operations.

---

## Operation vocabulary (aligned with §6.5)

Four operations, columns of the matrix, using the project's existing §6.5 *Access control* vocabulary:

| Op | Name | Delivered by (typical) |
|---|---|---|
| `C` | Create | a function/flow that brings a new instance into being (a creation form, a "start" step, an upload) |
| `R` | Read | a function/flow that displays the entity (a list, a detail view, a review summary, a confirmation screen) |
| `U` | Update | a function/flow that edits an existing instance (an edit affordance, a back-navigation that preserves and amends, a re-upload) |
| `D` | Delete | a function/flow that removes, archives, retires, discards, or clears an instance |

`§6.5` additionally uses `X` (execute/invoke) for *flow* rows (use-cases / task flows) and `—` for no access. CRUD-coverage rows on **data entities** (`§2.1`/`§2.3`/`§7`), so its four columns are `C/R/U/D`; `X` is not a column here. Where `§6.5` grants `D` on an entity, that maps to this matrix's `D` column.

---

## Intentional-narrowness rubric (forgotten vs intentional)

A missing operation is **intentional** (a documented exception, not a flagged hole) when the entity falls in one of these classes — otherwise it is **forgotten** (an `[AI-SUGGESTED]` resolver question):

| Class | Signal in requirements | Intentionally-absent operations |
|---|---|---|
| `derived` | `§2.1` persistence column reads *derived*; `§7.X Derivations` lists it | C, U, D — a derived value is computed (R only); never user-CRUD'd |
| `aggregate-member` | `§2.2` shows it is `included`/`required` by an aggregate root with cardinality `[1]`/`[1..*]`; `§2.3` lists it under *Member concepts* | D — deleted only by deleting/discarding the parent aggregate, never individually |
| `immutable-record` | `§2.3` key-invariant or `§9` defines it as append-only / write-once (audit log, issued invoice, confirmation) | U, D — create + read only |
| `reference/lookup` | admin-seeded enumeration (country list, bracket set) surfaced via a `§6.10` fixture, not user-authored | C — read-only to the user |

When an entity does not fit any class, the coverage rule applies in full and any missing operation is *forgotten*. The two-way classification is **load-bearing**: classifying a genuinely-narrow lifecycle as *forgotten* cries wolf; classifying a genuine gap as *intentional* hides the defect.

---

## Source-of-truth hierarchy

The analyser walks `requirements/requirements.md` in this order:

1. **Entities (matrix rows).** `§2.1 Concepts` + `§2.3 Aggregates & lifecycles` (aggregate roots + member concepts) + `§7 Data shapes`. Persistence kind (`persistent` / `derived`) from `§2.1`. Prior `analyse-requirements/{OOUX,DATA-MODEL}/*` outputs, **if present on disk**, seed and corroborate the entity list (they are an optional convenience, not a prerequisite — read them only if they exist).
2. **Granted operations.** `§6.5 Access control (RBAC)` — the authoritative *intent* declaration of which operations each role may perform on each entity, in `C/R/U/D/X/—` vocabulary. When present, this is the spine the matrix cross-checks delivery against. The orphaned-right gap (granted but never delivered) lives here.
3. **Delivered operations.** `§6.1 Functional` (F-NN), `§5 Task flows`, `§6.4 UI feature needs` (UI-NN), `§4 stories`. A function/flow/UI that creates, reads, updates, or deletes an entity fills that cell as *delivered* and cites the source ID.
4. **Narrowness signals.** `§2.2 Relationships` (aggregate membership), `§2.3` (member concepts, key invariants, lifecycle states), `§7.X Derivations`, `§9 Key terminology` — feed the intentional-narrowness rubric.
5. **Inference** — only for the *forgotten* classification of an uncovered cell (an expected operation with neither a grant nor a delivering function). Inferred holes carry the `[AI-SUGGESTED]` marker. The analyser never invents an entity, a function, or a *delivered* cell.

If `§6.5` is absent, the analyser builds the matrix from delivery alone (every cell is *delivered* or *forgotten* or *intentional*; the *granted-not-delivered* verdict cannot fire) and notes the absence in diagnostics.

---

## Coverage verdict taxonomy (4 — exhaustive)

Every (entity, operation) cell carries exactly one verdict:

| Verdict | CSS class | Meaning | Marker |
|---|---|---|---|
| `delivered` | `.cov-delivered` | ≥ 1 function/flow/UI in the requirements delivers this operation. Cites the source ID(s) (`F-NN` / `§5 <flow>` / `UI-NN` / `§6.5`). | provenance: `delivered` |
| `granted-not-delivered` | `.cov-granted` | `§6.5` grants the operation but **no** function/flow/UI delivers it — the orphaned-right gap. | provenance: `granted-not-delivered` (cites `§6.5`) |
| `forgotten` | `.cov-forgotten` | An expected operation (per the coverage rule, entity not in an intentional class) with no delivery and no grant. | `[AI-SUGGESTED: AI-NNN \| blocking\|non-blocking]` + `.provenance-ai-suggested` |
| `intentional` | `.cov-intentional` | A deliberately-narrow lifecycle per the rubric above. | documented exception (cites the rubric class + the §-anchor) |

Only `forgotten` cells carry `[AI-SUGGESTED]` — they are the genuinely-non-traceable inference (an operation the requirements neither deliver nor grant). This honours the framework-wide `[AI-SUGGESTED]` invariant. `granted-not-delivered` is **not** `[AI-SUGGESTED]` — it is fully traceable (the right is in `§6.5`); it is a cross-section consistency finding, and it is typically the highest-value hole the matrix surfaces.

---

## Output structure

### 0. In plain terms (first rendered section)

`<section id="plain-terms">` with `{{PLAIN_SUMMARY}}` — a 2–5 sentence plain-English lead: what this CRUD coverage matrix (the entity × operation table) is, what it found, and what the consultant should do with it (e.g. review the lifecycle-hole register, raise resolver questions before wireframing). The **first** section, above the overview meta-grid. A faithful condensation of the content below — it introduces no entity, count, or citation not already in the matrix, and carries no `[SRC]` of its own. Methodology jargon (CRUD, coverage matrix, operation gap, coverage verdict, entity) is glossed at first use here; client domain terms are not glossed (the GLOSSARY methodology owns those). Per `framework/shared/output-readability.md`.

### Diagrams (top of document)

1. **Coverage heatmap** — the centrepiece. Rows = entities (grouped persistent then derived); columns = `C` `R` `U` `D`. Each cell is colour-classed by verdict (delivered / granted-not-delivered / forgotten / intentional) and carries the delivering source IDs (or the hole marker) as text — colour is never the sole signal (a glyph + the verdict word accompany it). A forgotten or granted-not-delivered cell reads "hot".
2. **Role view (optional)** — rendered only when `§6.5` declares **more than one role**, or declares role-conditioned access. Reproduces the `§6.5` role × entity × operation grant grid, cross-checks granted-vs-delivered per role, and flags **Segregation-of-Duties** violations (a single role holding two operations the spec says must be separated — e.g. Create + an approve/`X` on a record it should not self-approve). When the spec is single-actor (one role in `§6.5`), the role view collapses to a one-line note: *"Single-actor spec — one role in §6.5; Segregation-of-Duties analysis is not applicable."* and is **not** rendered as a grid.

### Tables (below the diagrams)

3. **Entity × function traceability matrix** — rows = entities, columns = the delivering functions/flows (`F-NN`, `§5` flows, `UI-NN`), cells = the operation letters that function performs on that entity. This is the "show your work" backing for the heatmap.
4. **Lifecycle-hole register** — one row per `forgotten` or `granted-not-delivered` cell: `{entity, operation, verdict, classification, marker/exception, resolver-question-or-exception-reason}`. Forgotten rows carry `[AI-SUGGESTED]` + a stakeholder question; granted-not-delivered rows carry the `§6.5` citation + the design implication ("a surface for this operation is expected but unspecified").
5. **Plain entity × operation matrix** — the heatmap's data as a plain accessible table (verdict word per cell), for copy and for screen readers.

### Diagnostics (bottom, collapsed)

6. Counts summary, per-verdict tallies, the hard-check result lines (PASS/FAIL), the forgotten-density soft-warning line, and an embedded `<script type="application/json" id="crud-matrix">` block carrying the full `{entity, operation, verdict, sources, classification}` matrix for self-contained machine-readability.

---

## Quality checks (6 hard gates + 1 soft)

All checks operate on the matrix; the matrix must be valid regardless of whether the optional role view is rendered.

1. **Every entity has a kebab-case id, a display name, and a persistence kind** (`persistent` / `derived`), each sourced to `§2.1`/`§2.3`/`§7`.
2. **Every (entity, operation) cell carries exactly one verdict** (`delivered` / `granted-not-delivered` / `forgotten` / `intentional`) — no blank cells, no two verdicts.
3. **Every `delivered` cell cites ≥ 1 source ID** (`F-NN` / `§5 <flow>` / `UI-NN` / `§6.5`). A delivered cell with no citation is a fabrication.
4. **Every `forgotten` cell carries `[AI-SUGGESTED]` + a resolver question.** No silent hole; no fabricated outcome.
5. **Every `intentional` cell cites a rubric class + a §-anchor.** An intentional verdict with no documented reason is treated as a hard fail (it would hide a real gap).
6. **`§6.5` reconciliation (when `§6.5` present):** every entity row of `§6.5` appears in the matrix (no entity silently dropped), and every operation `§6.5` grants is classified `delivered` or `granted-not-delivered` — **never** `forgotten` (a granted operation is by definition not forgotten) and never `intentional` (a grant contradicts intentional narrowness).

**Soft check (warning, not gate):** **forgotten density.** `density = forgotten_cells / (total_cells − intentional_cells)`. If `density > 40%`, emit a `density-warning` line in diagnostics and the handback: *"Functional coverage is thin — many expected operations have no delivering function. This usually means `§6.1`/`§5` under-specify the lifecycle, not that the matrix is wrong."* Does not block writing.

On any hard-check failure (1–6): do **not** write the artefact; surface the failing checks + flagged items via `AskUserQuestion` with Revise / Override / Restart, per the analyser's Step 6 contract.

---

## Five-round discipline

Each round produces a distinct in-memory output. The analyser does not write until Round 5 completes and all hard checks pass (or the consultant chose Override).

- **Round 1 — Entity discovery.** Walk `§2.1`/`§2.3`/`§7` (+ prior OOUX/DATA-MODEL on disk if present) for entities. Record id, display name, persistence kind, aggregate membership. Cap at 16 entities; if exceeded, state the cap aloud and keep the persistent aggregate roots + their members first.
- **Round 2 — Delivery mapping.** Walk `§6.1`/`§5`/`§6.4`/`§4` for every function/flow/UI; for each, record which entities it creates/reads/updates/deletes (cite the source ID). Build the entity × function traceability matrix.
- **Round 3 — Grant mapping.** Parse `§6.5` (if present) into per-role per-entity granted operations. Record the role count.
- **Round 4 — Verdict assignment.** For each (entity, operation) cell, assign the verdict: `delivered` if Round 2 delivers it; else `granted-not-delivered` if Round 3 grants it; else `intentional` if the entity matches the narrowness rubric for that operation; else `forgotten`. Build the lifecycle-hole register.
- **Round 5 — Role view + validate.** If `§6.5` has > 1 role or role-conditioned access, build the role grid + SoD flags; else emit the single-actor note. Run the 6 hard checks + the soft density check. Build the cross-checks for the sidecar projections.

---

## Sidecar projection (downstream context-cost optimisation)

Per `framework/assets/analyses/sidecar-schema.md`, the analyser writes `analyse-requirements/CRUD-COVERAGE/crud-coverage.sidecar.json` exposing exactly two closed-enum roles (per `framework/skills/select-supporting-analyses.md > Static method → architect_roles mapping`):

- **`screen-inventory-entity-bijection`** — one entry per entity: `expected_screens` derived from its **delivered** (and granted-not-delivered) operations — `C → create-form`, `R → list` + `detail`, `U → edit-form`, `D → destructive-flow`. `source_anchor = "crud-coverage:<entity>"`; `rationale` ≤ 120 chars noting any holes. Forgotten-only entities still list their expected screens with the rationale flagging the gap (the architect cross-checks, never widens the feature set).
- **`per-screen-cta-set`** — one entry per delivered `C`/`U`/`D` cell: `screen_hint` = the owning entity's surface, `label` = a verb-phrase CTA (`C → "Add <Entity>"`, `U → "Edit"`, `D → "Discard"`/`"Delete"`), `source_anchor = "crud-coverage:<entity>.<op>"`.

Hard cap ≤ 20 KB; `source_sha256` of the HTML at write time; `truncated` flag per the schema. **Do not invent role keys.**

---

## Downstream consumption (handled by `framework/skills/map-crud-coverage-to-ui.md`)

- Each **delivered** cell → a candidate surface/action: `C →` creation form; `R →` list + detail surface; `U →` edit affordance; `D →` destructive flow (modal-gated per the project's destructive-action convention).
- Each **granted-not-delivered** cell → a surface the blueprint should expect but that the spec leaves unspecified — flagged, not fabricated.
- The **role view** → role-switcher entries (`PI-05`) + permission tiers; SoD flags → control/compliance findings for the auditor stakeholder.

`map-crud-coverage-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character and future design-spec authors.

---

## Stop-condition

The analysis is complete when every entity has a row with all four operation cells carrying exactly one verdict; every delivered cell cites a source; every forgotten cell carries `[AI-SUGGESTED]` + a question; every intentional cell cites a rubric class; the `§6.5` reconciliation check passes (when `§6.5` is present); all 6 hard checks pass (or Override); and the consultant chose Accept in the handback loop.

---

## Voice and stance

The analyser's stance is defined in `framework/assets/characters/crud-coverage-analysis.md` — mechanical, exhaustive, cross-section, provenance-honest. This reference defines **what** to do; the character file defines **how** the agent talks while doing it.

The artefact is human-read (and consumed downstream by `/wireframe`'s `blueprint-architect` via the sidecar), so the analyser also follows `framework/shared/output-readability.md`: it writes the "In plain terms" lead (`{{PLAIN_SUMMARY}}`), glosses methodology jargon — CRUD (Create / Read / Update / Delete operations), coverage matrix (entity × operation table), operation gap (a missing operation cell), coverage verdict (delivered / granted-not-delivered / forgotten / intentional), entity (a named data object the system stores or derives) — at first use in human-readable prose, leaves client domain vocabulary unglossed (GLOSSARY territory), and keeps every `[SRC: C-NNN]` marker. The plain-language layer is confined to the lead and first-use glosses; the matrix, tables, JSON, and diagnostics keep their concrete, named-entity discipline.
