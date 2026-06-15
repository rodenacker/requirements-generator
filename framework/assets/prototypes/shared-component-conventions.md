# Shared-component conventions (`shared-component-conventions.md`)

**Role:** asset (prototype-private).

**Purpose:** The contract that makes "many prototypes in one app, generated partly in parallel" safe and coherent. It governs (1) where components/stores/fixtures/types live and how they are named, (2) the **component-ownership / collision-avoidance protocol** that lets parallel per-surface sub-agents write into one shared tree without clobbering each other, (3) the **shared-not-private** rule (rules 15–16), (4) the **data-prop anti-fabrication** contract, (5) the store/fixture seeding contract, and (6) the **wireframe pattern → shared component correspondence** that lets the §7 component inventory be projected deterministically from a `primary_basis` wireframe variant (the wireframe fast path).

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
3. **Driver assigns each sub-agent a disjoint set of filenames it MAY create** — its uniquely-owned new components, **plus** (for a **standalone secondary** surface) its **own** standalone route page `src/app/<name-slug>/<surface-kebab>/page.tsx`, so standalone-route authoring joins the parallel wave. The assignment is explicit and non-overlapping. Standalone-vs-coupled is decided from the §5 realization enum (step-02): only a `standalone-screen` that is not the primary/root surface parallelizes its route; the primary/root page, folded-host routes (drawer/expand/modal — many-to-one), wizard routes, and any per-prototype `layout.tsx` stay **driver-owned**.
4. **Sub-agents only WRITE files in their assigned set**; they only READ the existing shared library. They never create a component outside their assignment, never write any route other than their own assigned standalone `page.tsx` (never the root page, a `layout.tsx`, a folded-host route, or a wizard route), never overwrite an existing file, and never edit `seed.ts`/`stores/index.ts`/`types/index.ts` (driver-owned).
5. **Reuse-first**: before the driver marks a component "new", it checks the shared library for an existing component that fits; existing names are reused, never duplicated. Component count grows monotonically across runs (rule 13 payoff: later prototypes write less).

If two surfaces genuinely need the same brand-new component, the driver authors it once before dispatch (slight serialisation) and both surfaces reuse it. This replaces the per-variant-directory isolation the wireframe pipeline gets for free.

The disjoint `owned_files` partition — not the number of concurrent sub-agents — is the collision-safety boundary; it holds at any wave size. Extending the partition to standalone route files stays **provably** disjoint: each standalone secondary surface contributes exactly one route path `<surface-kebab>/page.tsx`, unique by surface, and the only many-to-one route case (multiple folds → one host route) is driver-owned — so no two sub-agents can ever target one route. The driver dispatches all surfaces-with-`owned_files` in a single wave up to a ceiling of 8 (an operational ceiling for message size and resource manageability, not a safety limit); the harness queues calls beyond its own concurrency limit gracefully.

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

## 7. Wireframe pattern → shared component correspondence (the §7 fast path)

When a `/prototype` run designates a `primary_basis` wireframe variant, the variant's
`manifest.json` already names, per surface, a settled **realization** + **pattern picks**
(`primary_pattern`, `primary_pattern_variant`, `modifiers[]`, `secondary_patterns[]`,
drawn from `framework/assets/pattern-catalogue/`). `prototype-spec-drafter.md` projects
those picks into the §7 component inventory through the correspondence below, tagging each
row `[SRC: WF:<variant>]` (instead of re-deriving components from the blueprint + posture).
This keeps the prototype faithful to the wireframe the consultant chose and removes drafter
judgement from §7.

**Naming, not existence.** Each row names the **canonical shared component** (name + tier
per §1/§2) the pattern maps to. The component may or may not already be on disk — reuse-vs-new
remains the **generator driver's** call (§3, `step-04`): it reuses an existing component of
that name or authors a new one. The correspondence guarantees *naming stability* (the same
wireframe pattern always maps to the same component name), which is what makes reuse
compound across prototypes (rule 13 monotonic growth). The drafter records the *intent*
(`reuse`/`new`); the driver decides.

**Generic vs domain.** Rows name the **domain-neutral** generic (`RecordTable`, not
`InvoiceTable`) per §2. When a surface binds a specific entity, the driver may compose a
`domain/<Entity><Role>` wrapper over the generic — that is a driver concern, not a §7-projection
concern.

### 7.1 Realization → structural container (from the variant's `realization`, already §5)

| Realization | Structural component(s) | Notes |
|---|---|---|
| `standalone-screen` | route `page.tsx` composes the primary-pattern component inside the shared app shell (`templates/` shell when list+detail) | no overlay container; route page authored by the surface's sub-agent for a standalone **secondary**, by the driver for the **primary/root** (§3) |
| `inline-drawer` | `organisms/DetailDrawer` (wraps `ui/Sheet`); host surface uses `templates/ListDetailShell` | folded onto `host_surface`/`host_state` |
| `inline-expand` | disclosure **within** the host collection (e.g. `organisms/RecordTable` `expandable-row` variant) — a host modifier, **no new component** | folded onto host |
| `modal` | `organisms/RecordFormModal` (form payload) or `molecules/ConfirmDialog` (confirmation), each wrapping `ui/Dialog` | pick by `primary_pattern` |
| `wizard-split` | `organisms/Wizard` + `templates/WizardShell` (+ `atoms/StepperIndicator`) | multi-screen flow |

### 7.2 `primary_pattern` category → shared component

| Catalogue pattern | Tier | Shared component (name + tier) |
|---|---|---|
| `collections/table` | T1 | `organisms/RecordTable` (+ built-in sort headers; `molecules/Pagination` chrome) |
| `collections/master-detail-list` | T1 | `templates/ListDetailShell` + `organisms/RecordList` + detail composition |
| `collections/data-list` | T1 | `organisms/RecordList` |
| `collections/dashboard` | T1 | `organisms/Dashboard` composing `molecules/KpiTile` + cards |
| `collections/detail-page` | T1 | `templates/DetailShell` + `domain/<Entity>Detail` composition |
| `collections/card-grid` | T2 | `organisms/RecordCardGrid` |
| `collections/kpi-tile` | T2 | `molecules/KpiTile` |
| `collections/detail-panel` | T2 | `organisms/DetailPanel` (inline/side) |
| `forms/single-form` | T1 | `organisms/RecordForm` + `molecules/FormField` (→ `organisms/RecordFormModal` when realization is `modal`) |
| `forms/multi-step-wizard` | T1 | `organisms/Wizard` + `templates/WizardShell` |
| `forms/search-and-filter` | T1 | `molecules/SearchFilterBar` |
| `forms/inline-edit` | T2 | `organisms/RecordTable` `editable` variant (inline cell editors — no separate component) |
| `forms/bulk-edit` | T2 | `organisms/BulkActionBar` + selectable host collection |
| `forms/file-upload` | T3 | `organisms/FileUpload` |
| `surfaces/modal-confirmation` | T1 | `molecules/ConfirmDialog` |
| `surfaces/drawer-detail` | T1 | `organisms/DetailDrawer` |
| `surfaces/modal-form` | T2 | `organisms/RecordFormModal` |
| `surfaces/drawer-form` | T2 | `organisms/DrawerForm` |
| `surfaces/popover` | T2 | `molecules/Popover` (wraps `ui/Popover`) |
| `feedback/notification-toast` | T1 | `ui/` toast primitive (shipped) — invoked, not authored |
| `feedback/empty-state` | T1 | `molecules/EmptyState` |
| `feedback/notification-banner` | T2 | `atoms/NotificationBanner` |
| `feedback/confirmation-receipt` | T2 | `organisms/ConfirmationReceipt` |
| `navigation/tabs` | T1 | `ui/Tabs` (shipped primitive) |
| `navigation/pagination` | T1 | `molecules/Pagination` |
| `navigation/stepper-indicator` | T1 | `atoms/StepperIndicator` |
| `navigation/segmented-control` | T2 | `molecules/SegmentedControl` |
| `navigation/command-palette` | T2 | `organisms/CommandPalette` |
| `layouts/app-shell-with-sidebar` | T1 | `templates/AppShellSidebar` (usually the scaffold root layout — reuse) |
| `layouts/app-shell-with-topnav` | T1 | `templates/AppShellTopnav` |
| `layouts/centered-form` | T1 | `templates/CenteredFormShell` |
| `layouts/settings-shell` | T1 | `templates/SettingsShell` |
| `auth/login-form` | T3 | `organisms/LoginForm` |
| `auth/signup-form` | T3 | `organisms/SignupForm` |

**T3 / not-listed patterns.** A T3 catalogue pattern the variant settled but not tabled above
maps by analogy to an `organisms/<PascalCasePattern>` (or the nearest structural tier),
authored when the first surface requires it — the same "author when first needed" discipline
the catalogue uses for T3 stubs. Add a row here when that happens (living doc).

### 7.3 Variants, modifiers, secondary patterns

- **`primary_pattern_variant` + `modifiers[]`** (e.g. table `compact`/`selectable`/`editable`,
  `wf-table--compact`) → **props/variants of the same component**, never new components.
- **`secondary_patterns[]`** → **additional composed shared components** for that surface, each
  resolved through 7.2 (e.g. a table with `feedback/empty-state` + `forms/search-and-filter`
  → `organisms/RecordTable` + `molecules/EmptyState` + `molecules/SearchFilterBar`).
- **Conventions** the catalogue keeps out of band (`tooltip`, `breadcrumbs`, `loading-skeleton`,
  `inline-error`, `role-switcher`, etc.) are `ui/`/`atoms/` primitives or built-in states, and
  are **UI-only** (no `data-prop`) — they are not §7 inventory rows.

**Living doc.** Append rows as new pattern categories are settled by variants; never remove rows
(mirrors `pattern-bindings.md` discipline). Every row must name a tier that exists in §1 and a
pattern that exists in `framework/assets/pattern-catalogue/`.

---

## Self-validation
- No component definitions under `src/app/<name-slug>/**` (routes compose only).
- No private per-prototype component folders; every new component is in a shared tier.
- The driver's ownership map is disjoint (components **and** standalone route files); no two agents were assigned the same path; no standalone route collides with a driver-owned root/`layout.tsx`/host/wizard route; no existing file was overwritten.
- Every data-bound element binds to a blueprint closed-set Property (carries `data-prop`); no fabricated fields in components or fixtures.
- New stores registered in `stores/index.ts` + `seed.ts`; types in `types/index.ts`; all driver-authored before dispatch.
- The brand theme was not forked; no per-prototype palette/type scale was added.

## Anti-patterns
- Do not let a sub-agent create a component outside its assigned filename set, overwrite an existing component, edit the driver-owned data files, or write a route other than its own assigned standalone `page.tsx` (never the root page, a `layout.tsx`, a folded-host route, or a wizard route).
- Do not duplicate a component that already exists in the shared library — reuse it.
- Do not create private per-prototype components or themes (rules 15–16).
- Do not bind any element to a field absent from the blueprint closed set (fabrication).
- Do not add fixture fields beyond the closed set.
- Do not modify shadcn `ui/` primitives — wrap them in `atoms/` if behaviour must change.
