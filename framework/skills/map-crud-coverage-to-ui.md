# map-crud-coverage-to-ui.md

**Purpose:** Translate a `crud-coverage` analysis artefact into UI-inventory entries (candidate surfaces, actions, role-switcher seeds) for downstream design consumption. **Stub at MVP** — like the other analyses' map-skills, this is registry metadata read by a future design-spec-drafter, **not** invoked by `/analyse-requirement`. The canonical structured projection the architect actually consumes is the sidecar (`analyse-requirements/CRUD-COVERAGE/crud-coverage.sidecar.json`, roles `screen-inventory-entity-bijection` + `per-screen-cta-set`); this file documents the wider mapping for human design authors.

## Inputs

- `analyse-requirements/CRUD-COVERAGE/crud-matrix.html` — the coverage matrix artefact (or its sidecar for the structured subset).

## Mapping

### Operation → surface / action

| Delivered cell | Candidate surface / action |
|---|---|
| `C` create | a creation surface — a form (standalone screen, inline drawer, or wizard step) whose fields are the entity's `§7` shape; primary CTA `Add <Entity>` / `New <Entity>` / a flow-start step. |
| `R` read | a **list** surface (collection of instances) **and** a **detail** surface (one instance); for single-record entities, a read-only summary / review surface suffices. |
| `U` update | an **edit** affordance on the detail/review surface (inline edit, edit-from-review, or an edit form); back-navigation that preserves and amends counts as update. |
| `D` delete | a **destructive flow** — a remove/archive/discard action, modal-gated per the project's destructive-action convention (names the affected item, destructive-styled primary, focus defaults to Cancel). |

### Verdict → design signal

- **delivered** → the surface/action above is expected to exist; cross-check it against the blueprint's `LS-NN` logical-surface inventory. A no-Create entity → a missing form surface; a no-Delete entity → a missing destructive flow.
- **granted-not-delivered** → a surface the design **should expect** (the right is granted in `§6.5`) but the spec leaves unspecified — surface it to the consultant as a design unknown; do **not** fabricate the requirement.
- **forgotten** → not a surface; an `[AI-SUGGESTED]` resolver question to settle before building.
- **intentional** → no surface for the absent operation; record the documented exception so the design does not add an unwanted affordance.

### Role view → access UI

- The role × entity × operation grant grid → `PI-05` PrototypeChrome **role-switcher** entries (one per `§6.5` role) + per-surface permission tiers (which actions each role sees).
- A **Segregation-of-Duties** flag → a control/compliance finding for the auditor stakeholder; not a UI affordance.

## Note

No widening. Every surface/action this mapping proposes must trace to a `delivered` or `granted-not-delivered` cell, which in turn traces to a `§6.1`/`§5`/`§6.4`/`§6.5` source. The mapping never introduces an entity, operation, or property the matrix did not carry.
