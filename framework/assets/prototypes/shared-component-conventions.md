# Shared-component conventions (`shared-component-conventions.md`)

**Role:** asset (prototype-private).

**Purpose:** The contract that makes "many prototypes in one app, generated partly in parallel" safe and coherent. It governs (1) where components/stores/fixtures/types live and how they are named, (2) the **component-ownership / collision-avoidance protocol** that lets parallel per-surface sub-agents write into one shared tree without clobbering each other, (3) the **shared-not-private** rule (rules 15–16), (4) the **data-prop anti-fabrication** contract, and (5) the store/fixture seeding contract.

**Consumed by:** `prototype-generator.md` + `prototype-generator/steps/{step-03-ensure-fixtures-stores, step-04-dispatch-surface-subagents, step-05-compose-route, step-sub-render-surface}.md`. Referenced by `prototype-spec-drafter.md` (§7 component inventory) and `template-design-spec.md`.

---

## 1. Placement (atomic design, all shared)

The template ships `src/components/{ui,atoms,molecules,organisms,templates,domain}` (the `ui/` folder is shadcn primitives). All generated components are **shared** and live here — never under a prototype route folder.

| Tier | Holds | Example |
|---|---|---|
| `ui/` | shadcn primitives (shipped; do not modify) | `Button`, `Table`, `Dialog`, `Input`, `Badge`, `Select`, `Sheet`, `Tabs`, `Card` |
| `atoms/` | tiny single-purpose wrappers over `ui/` | `StatusBadge`, `FieldLabel` |
| `molecules/` | small compositions | `SearchFilterBar`, `ConfirmDialog`, `FormField` |
| `organisms/` | task components | `RecordTable`, `RecordFormModal`, `DetailDrawer`, `BulkActionBar`, `Wizard` |
| `templates/` | page-level layout shells | `ListDetailShell`, `WizardShell` |
| `domain/` | entity-specific compositions (named by the §7 entity) | `InvoiceTable`, `ImportQueueBoard` |

Routes (`src/app/<name-slug>/**`) contain **only** `page.tsx`/`layout.tsx` that **compose** shared components + bind data. No component definitions live under routes.

## 2. Naming

- Components: `PascalCase.tsx`, file name = export name. Generic task components are **domain-neutral** (`RecordTable`, not `InvoiceTable`) when reusable across entities; entity-specific compositions go in `domain/` named `<Entity><Role>.tsx`.
- Stores: `src/stores/<entity-kebab>-store.ts` exporting `use<Entity>Store`; re-exported from `src/stores/index.ts`.
- Fixtures: `src/data/fixtures/<entity-kebab>.json`.
- Types: `src/types/index.ts` (one interface per entity; shared).

## 3. Component-ownership / collision-avoidance protocol (load-bearing)

Parallel per-surface sub-agents write into one shared `src/components/**` tree. To prevent clobbering, lost writes, or duplicate definitions, the **generator driver** (`step-04`) — not the sub-agents — owns partitioning:

1. **Driver does all cross-cutting writes first** (`step-03`, before any dispatch): types, fixtures, stores, and `seed.ts` registration. Sub-agents never touch these.
2. **Driver computes a component-ownership map**: from the design spec §7 inventory, it lists every component each surface needs, marks **reuse** (already on disk) vs **new**, and **deduplicates new components across surfaces** (if two surfaces both need a new `ConfirmDialog`, the driver assigns it to exactly one surface — or authors it itself — and the other surface reuses it).
3. **Driver assigns each sub-agent a disjoint set of filenames it MAY create** (its surface's route segment + its uniquely-owned new components). The assignment is explicit and non-overlapping.
4. **Sub-agents only WRITE files in their assigned set**; they only READ the existing shared library. They never create a component outside their assignment, never overwrite an existing file, and never edit `seed.ts`/`stores/index.ts`/`types/index.ts` (driver-owned).
5. **Reuse-first**: before the driver marks a component "new", it checks the shared library for an existing component that fits; existing names are reused, never duplicated. Component count grows monotonically across runs (rule 13 payoff: later prototypes write less).

If two surfaces genuinely need the same brand-new component, the driver authors it once before dispatch (slight serialisation) and both surfaces reuse it. This replaces the per-variant-directory isolation the wireframe pipeline gets for free.

The disjoint `owned_files` partition — not the number of concurrent sub-agents — is the collision-safety boundary; it holds at any wave size. The driver dispatches all owned-component surfaces in a single wave up to a ceiling of 8 (an operational ceiling for message size and resource manageability, not a safety limit); the harness queues calls beyond its own concurrency limit gracefully.

## 4. Shared-not-private rule (rules 15–16)

The **only** new artefacts a prototype may generate are **shared** components, **shared** styling contributions, and **shared** scripts/util helpers — all placed in the shared locations above (or `src/lib/`). A prototype **must not** create a private component folder under its route. Anything reusable a prototype needs becomes part of the shared library, available to every later prototype.

Styling: prototypes do **not** add per-prototype themes. The brand theme (`src/styles/theme.css`) is fixed and shared. New *styling* contributions mean shared utility classes / component variants expressed through the existing token system — never a competing palette/type scale.

## 5. Data-prop anti-fabrication contract

Every data-bound element a prototype renders (table column, form field, detail row, status chip, card field) MUST bind to a **Property in the blueprint's per-surface closed set** (`blueprints/<scope-slug>/blueprint.md`, drawn from `requirements.md §7` data shapes + `F-NN` parameters). This mirrors the wireframe `data-prop` rule:

- The design spec §8 declares, per surface, the closed Property set → fixture field → store.
- A field with a "real-looking" name that is **not** in the blueprint closed set is a **fabrication** and a self-validation FAIL (RF-04-class — fix before handback).
- UI-only controls (search, sort, pagination, filter chips, save/cancel, density toggle, dropzones, the command palette) are exempt — they carry no `data-prop`.
- For readability + auditability, generated data-bound elements carry a `data-prop="Entity.Field"` (or `F-NN:Param`) attribute, exactly as wireframes do, so the contract is greppable in the rendered DOM.

## 6. Store / fixture / type seeding contract

- One Zustand store per entity (modelled on the template's former `_example-store`: `persist` + `createJSONStorage(localStorage)` + `skipHydration: true`, with `seedFromFixtures()` / `reset()` / CRUD actions). Mutations persist in-session only (PI-02).
- Fixture JSON fields = exactly the entity's Property closed set (anti-fabrication extends to fixtures — no invented fields).
- The driver registers each new store in `src/stores/index.ts` (barrel) and wires `seedAllStores()`/`resetAllStores()` in `src/data/seed.ts` additively (rehydrate + seed-if-empty for `seedAllStores`; reset+reseed for `resetAllStores`).
- Types: one interface per entity in `src/types/index.ts`.
- All of the above are **driver-owned** (`step-03`), authored before sub-agent dispatch, so parallel sub-agents see a consistent data layer.

---

## Self-validation
- No component definitions under `src/app/<name-slug>/**` (routes compose only).
- No private per-prototype component folders; every new component is in a shared tier.
- The driver's ownership map is disjoint; no two sub-agents were assigned the same filename; no existing file was overwritten.
- Every data-bound element binds to a blueprint closed-set Property (carries `data-prop`); no fabricated fields in components or fixtures.
- New stores registered in `stores/index.ts` + `seed.ts`; types in `types/index.ts`; all driver-authored before dispatch.
- The brand theme was not forked; no per-prototype palette/type scale was added.

## Anti-patterns
- Do not let a sub-agent create a component outside its assigned filename set, overwrite an existing component, or edit the driver-owned data files.
- Do not duplicate a component that already exists in the shared library — reuse it.
- Do not create private per-prototype components or themes (rules 15–16).
- Do not bind any element to a field absent from the blueprint closed set (fabrication).
- Do not add fixture fields beyond the closed set.
- Do not modify shadcn `ui/` primitives — wrap them in `atoms/` if behaviour must change.
