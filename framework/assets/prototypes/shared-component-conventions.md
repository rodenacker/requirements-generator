# Shared-component conventions (`shared-component-conventions.md`)

**Role:** asset (prototype-private).

**Purpose:** The contract that makes "many prototypes in one app, generated partly in parallel" safe and coherent. It governs (1) where components/stores/fixtures/types live and how they are named, (2) the **component-ownership / collision-avoidance protocol** that lets parallel per-surface sub-agents write into one shared tree without clobbering each other, (3) the **shared-not-private** rule (rules 15–16), (4) the **data-prop anti-fabrication** contract, (5) the store/fixture seeding contract, (6) the **navigation data contract** (§6a — the canonical nav table every application shell reads), and (7) the **wireframe pattern → shared component correspondence** that lets the §7 component inventory be projected deterministically from a `primary_basis` wireframe variant (the wireframe fast path).

**Consumed by:** `prototype-generator.md` + `prototype-generator/steps/{step-02-read-spec, step-03-ensure-fixtures-stores, step-04-dispatch-surface-subagents, step-05-compose-route, step-sub-render-surface}.md`, and — for the §6a nav barrel it authors empty + the chrome that reads it — `prototype-app-scaffolder.md` / `app-shell-spec.md`. Referenced by `prototype-spec-drafter.md` (§7 component inventory) and `template-design-spec.md`.

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
- Nav: `src/data/nav/<name-slug>.ts` exporting `NAV`; barrel `src/data/nav/index.ts` exporting `NavEntry` + `NAV_BY_PROTOTYPE` (§6a).

## 3. Component-ownership / collision-avoidance protocol (load-bearing)

Parallel per-surface sub-agents write into one shared `src/components/**` tree. To prevent clobbering, lost writes, or duplicate definitions, the **generator driver** (`step-04`) — not the sub-agents — owns partitioning:

1. **Driver does all cross-cutting writes first** (`step-03`, before any dispatch): types, fixtures, stores, `seed.ts` registration, and the **nav module** (§6a). Sub-agents never touch these — but they *read* the nav module, which is exactly why it must be written before the wave: a sub-agent-authored shell that needs nav and finds nothing hand-rolls its own array instead.
2. **Driver computes a component-ownership map**: from the design spec §7 inventory, it lists every component each surface needs, marks **reuse** (already on disk) vs **new**, and **deduplicates new components across surfaces** (if two surfaces both need a new `ConfirmDialog`, the driver assigns it to exactly one surface — or authors it itself — and the other surface reuses it).
3. **Driver assigns each sub-agent a disjoint set of filenames it MAY create** — its uniquely-owned new components, **plus** (for a **standalone secondary** surface) its **own** standalone route page `src/app/<name-slug>/<surface-kebab>/page.tsx`, so standalone-route authoring joins the parallel wave. The assignment is explicit and non-overlapping. Standalone-vs-coupled is decided from the §5 realization enum (step-02): only a `standalone-screen` that is not the primary/root surface parallelizes its route; the primary/root page, folded-host routes (drawer/expand/modal — many-to-one), wizard routes, and any per-prototype `layout.tsx` stay **driver-owned**.
4. **Sub-agents only WRITE files in their assigned set**; they only READ the existing shared library. They never create a component outside their assignment, never write any route other than their own assigned standalone `page.tsx` (never the root page, a `layout.tsx`, a folded-host route, or a wizard route), never overwrite an existing file, and never edit `seed.ts`/`stores/index.ts`/`types/index.ts` (driver-owned).
5. **Reuse-first**: before the driver marks a component "new", it checks the shared library for an existing component that fits; existing names are reused, never duplicated. Component count grows monotonically across runs (rule 13 payoff: later prototypes write less).

If two surfaces genuinely need the same brand-new component, the driver authors it once before dispatch (slight serialisation) and both surfaces reuse it. This replaces the per-variant-directory isolation the wireframe pipeline gets for free.

The disjoint `owned_files` partition — not the number of concurrent sub-agents — is the collision-safety boundary; it holds at any wave size. Extending the partition to standalone route files stays **provably** disjoint: each standalone secondary surface contributes exactly one route path `<surface-kebab>/page.tsx`, unique by surface, and the only many-to-one route case (multiple folds → one host route) is driver-owned — so no two sub-agents can ever target one route. The driver dispatches all surfaces-with-`owned_files` in a single wave up to a ceiling of 8 (an operational ceiling for message size and resource manageability, not a safety limit); the harness queues calls beyond its own concurrency limit gracefully.

## 4. Shared-not-private rule (rules 15–16)

The **only** new artefacts a prototype may generate are **shared** components and **shared** styling contributions, placed in the shared locations above, plus the driver-owned data layer (§6) and nav module (§6a). A prototype **must not** create a private component folder under its route. Anything reusable a prototype needs becomes part of the shared library, available to every later prototype.

**`src/lib/` is closed to the generator.** The template ships `src/lib/utils.ts` (copied verbatim per `scaffolding-instructions.md`) and nothing else belongs there. Until 2026-07-29 this paragraph licensed *"shared scripts/util helpers … (or `src/lib/`)"* — but `src/lib/**` appears in **no** `owned_files` partition (§3), so a file written there had no owner, no collision-safety, and no gate. A real run used exactly that gap for a `lib/nav.ts` that became one of three competing nav derivations. Shared logic belongs in a shared component or, when it is data, in the driver-owned data layer; there is no third home.

Styling: prototypes do **not** add per-prototype themes. The brand theme (`src/styles/theme.css`) is fixed and shared. New *styling* contributions mean shared utility classes / component variants expressed through the existing token system — never a competing palette/type scale.

### 4a. Colour binding (what makes light/dark actually work)

The app may carry **two** token sets — a `:root` base block and a `.dark` alternate — switched by a `.dark` class on `<html>`. Only values that flow through the token vars change with the mode. Anything else is frozen at whatever it was written as, which in dark mode is how labels and icons go invisible.

- **Bind every colour through a semantic token.** Use `bg-primary`, `text-foreground`, `border-border`, `bg-muted`, `text-text-muted` and friends. **Never** a raw literal (`bg-[#fff]`, `style={{ color: '#333' }}`) and **never** a Tailwind palette colour (`bg-white`, `text-gray-900`, `bg-slate-100`, `text-black`). Those do not flip. §4's rule above forbids *adding a palette*; this forbids the one-off literal, which is the far more common way it happens.
- **A filled element takes its label and icon colour from that fill's `-foreground` var** — `bg-primary text-primary-foreground`, `bg-success text-success-foreground`, `bg-destructive text-destructive-foreground`. Never `text-white` / `text-black` on a fill: the correct choice inverts between modes and between brands, and it is computed per mode by `extract-brand-theme.md`. (On a real dark palette, `text-white` on the status fills measures 2.06–2.32:1 — invisible in practice.)
- **Icons inherit `currentColor`.** Do not give a `lucide` icon an explicit colour class unless it is a semantic token, and never one that diverges from its container's text colour.
- **Do not reach for `--brand-accent` as an interaction surface.** `--accent` / `--accent-foreground` is the neutral hover/selected pair that shadcn's `hover:bg-accent` uses; `--brand-accent` is the brand hue, for callouts, highlights and chart series.
- This is enforced, not just advised: when two modes are live, the verify smoke sweeps every visible label and icon in **both** modes, including a hover pass, and a contrast miss is a `structured-fail` (`verify-prototype-build.md`).

## 5. Data-prop anti-fabrication contract

Every data-bound element a prototype renders (table column, form field, detail row, status chip, card field) MUST bind to a **Property in the blueprint's per-surface closed set** (`blueprints/<scope-slug>/blueprint.md`, drawn from `requirements.md §7` data shapes + `F-NN` parameters). This mirrors the wireframe `data-prop` rule:

- The design spec §8 declares, per surface, the closed Property set → fixture field → store.
- A field with a "real-looking" name that is **not** in the blueprint closed set is a **fabrication** and a self-validation FAIL (RF-04-class — fix before handback).
- UI-only controls (search, sort, pagination, filter chips, save/cancel, density toggle, **the colour-mode `ThemeToggle`**, dropzones, the command palette) are exempt — they carry no `data-prop`.
- For readability + auditability, generated data-bound elements carry a `data-prop="Entity.Field"` (or `F-NN:Param`) attribute, exactly as wireframes do, so the contract is greppable in the rendered DOM.

## 6. Store / fixture / type seeding contract

- One Zustand store per entity (modelled on the template's former `_example-store`: `persist` + `createJSONStorage(localStorage)` + `skipHydration: true`, with `seedFromFixtures()` / `reset()` / CRUD actions). Mutations persist in-session only (PI-02).
- Fixture JSON fields = exactly the entity's Property closed set (anti-fabrication extends to fixtures — no invented fields).
- The driver registers each new store in `src/stores/index.ts` (barrel) and wires `seedAllStores()`/`resetAllStores()` in `src/data/seed.ts` additively (rehydrate + seed-if-empty for `seedAllStores`; reset+reseed for `resetAllStores`).
- Types: one interface per entity in `src/types/index.ts`.
- All of the above are **driver-owned** (`step-03`), authored before sub-agent dispatch, so parallel sub-agents see a consistent data layer.

**Reading a persisted store: gate on `isLoaded` (canonical rule).** Every entity store is created with `skipHydration: true`, which *guarantees* that first-render state differs from post-rehydration state — the store is empty on the server-rendered pass and populated after `seedAllStores()` runs. Any render path that reads store data must therefore branch on `isLoaded` (render the loading state until it is true) rather than reading `items` unconditionally during render. The `isLoaded` flag exists on every store for exactly this purpose; it is not optional bookkeeping.

Reading through it is not a style question. React logs the divergence as a hydration mismatch, which lands in the console — and the per-route smoke asserts **zero console errors on every authored route** (`framework/skills/verify-prototype-build.md`), so it is a gate failure. It reached production once precisely because the offending page was a *secondary* route that no gate visited; both halves of that (the unguarded read and the unvisited route) are now closed. The same reasoning applies to any other external store read during render — see `app-shell-spec.md`'s `ThemeToggle`, which reads `localStorage` through `useSyncExternalStore` with a `getServerSnapshot` for the same reason.

## 6a. Navigation data contract (the canonical nav table)

**This section is the canonical owner of the nav module's shape.** Every other file — `step-02`/`step-03`/`step-05`/`step-sub-render-surface`, `app-shell-spec.md` — references it and never redefines it (`docs/maintenance.md > Canonical-source rule`).

A prototype's intra-prototype navigation is **generated data**, not code any component derives. Two driver-owned files:

```ts
// src/data/nav/index.ts — the barrel. Authored EMPTY by prototype-app-scaffolder.md,
// then registered into additively by the generator driver, one entry per prototype.
export interface NavEntry {
  route: string      // "/<name-slug>" or "/<name-slug>/<surface-kebab>" — must be a real authored route
  label: string      // from the design spec §5 surface intent
  surface_id: string // "LS-NN" — traceability back to the blueprint surface
  roles: string[]    // roles for whom this destination is visible; see the expansion rule below
}
import { NAV as <camelSlug> } from './<name-slug>'
export const NAV_BY_PROTOTYPE: Record<string, NavEntry[]> = { '<name-slug>': <camelSlug>, /* … */ }

// src/data/nav/<name-slug>.ts — one per prototype, driver-authored at step-03 rule 4b
import type { NavEntry } from './index'
export const NAV: NavEntry[] = [ /* … */ ]
```

**`NavEntry` is declared in the barrel, not in a per-prototype file** — because `PrototypeChrome` imports the barrel at **scaffold** time, when no prototype exists yet. The barrel therefore ships empty (`NAV_BY_PROTOTYPE = {}`) exactly as `prototype-registry.ts` does, so `tsc --noEmit` passes on a freshly scaffolded app with zero prototypes. Declaring the type in a per-prototype file instead would make the barrel un-authorable until the first prototype existed.

**Why a barrel keyed by slug, rather than a per-prototype import.** Application shells are **shared** components (`templates/AppShellSidebar` and friends, §1/§7.2) reused by every later prototype, so a shell cannot import one prototype's nav — it must resolve nav at **runtime** from the route it is rendering: take the first path segment of `usePathname()` as the `name-slug` and look it up in `NAV_BY_PROTOTYPE`. This is the same resolution `PrototypeChrome` already performs against `prototype-registry.ts` (`app-shell-spec.md`).

**`roles` is always fully expanded — never empty, never a sentinel.** The driver expands the "unrestricted" case (step-02 rule 1b: surface binds no entity, or its entities appear in no §6.5 row) into the prototype's full role list at write time, and a single-role prototype gets that one role. Consumers then do one thing — `entry.roles.includes(activeRole)` — with no union type, no `'all'` sentinel, and no per-call-site special case to get wrong.

**This table is the only grant table.** Roles come from `proto-chrome-store.activeRole` (PI-05); which destinations a role may see comes from here. A generated `user-store` / `auth-store` / `session-store` holding roles or grants is a second authority and a self-validation FAIL (§Anti-patterns). Nav arrays hand-rolled inside a page or a shell are the same failure in a cheaper disguise.

**Not a duplicate of `prototype-registry.ts`.** The registry is **inter**-prototype: one row per prototype, carrying the single landing-page `route`, consumed by the landing page and the review chrome, regenerated by `prototype-landing-updater.md` *after* the verify gate. This module is **intra**-prototype: the destination list *within* one prototype, written *before* sub-agent dispatch so shells can import it and the gate can see it. Different scope, different owner, different timing — do not merge them, and do not put intra-prototype routes in the registry.

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
| `layouts/app-shell-with-sidebar` | T1 | `templates/AppShellSidebar` |
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
- Exactly one store per §8 entity and **no others** — no `user`/`auth`/`session` store carrying roles or grants.
- `src/data/nav/<name-slug>.ts` + the `src/data/nav/index.ts` barrel exist, were written before dispatch, and every `NAV[].route` resolves to a real authored route; every `roles` array is non-empty; no nav array or role-grant map exists anywhere else in the tree.
- Nothing new was written under `src/lib/`.
- The brand theme was not forked; no per-prototype palette/type scale was added.

## Anti-patterns
- Do not let a sub-agent create a component outside its assigned filename set, overwrite an existing component, edit the driver-owned data files, or write a route other than its own assigned standalone `page.tsx` (never the root page, a `layout.tsx`, a folded-host route, or a wizard route).
- Do not duplicate a component that already exists in the shared library — reuse it.
- Do not create private per-prototype components or themes (rules 15–16).
- Do not bind any element to a field absent from the blueprint closed set (fabrication).
- Do not add fixture fields beyond the closed set.
- Do not modify shadcn `ui/` primitives — wrap them in `atoms/` if behaviour must change.
- **Do not derive nav in a component, a page, or a helper module.** Nav is generated data (§6a). A hand-rolled nav array, a `navItemsForRole()` helper, or a role→pages map anywhere outside `src/data/nav/` is a second derivation — and a second derivation is the defect, whether or not it happens to agree today. A real run shipped three (`lib/nav.ts`, an inline array, and a store method), one of which documented in its own header that it mirrored another.
- **Do not create a second role or grant authority.** Roles come from `proto-chrome-store.activeRole`; grants come from `src/data/nav/`. A generated `user-store`/`auth-store`/`session-store` is a FAIL.
- **Do not read a persisted store during first render without an `isLoaded` guard** (§6) — `skipHydration: true` makes that a hydration mismatch, which the per-route smoke fails on.
- **Do not write anything under `src/lib/`** (§4). The template's `lib/utils.ts` ships as-is; the tree has no owner for anything else there.
