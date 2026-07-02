# Prototype app shell & chrome spec (`app-shell-spec.md`)

**Role:** asset (prototype-private).

**Purpose:** Specify the **shared** application shell, the **prototype chrome** (review harness), the **landing page**, and the **prototype registry** module — all authored **once** by `prototype-app-scaffolder.md` (shell + chrome + empty landing/registry) and thereafter only the registry + landing are **regenerated additively** by `prototype-landing-updater.md`. The shell and chrome are static code shared by every prototype; they must never be regenerated per prototype.

**Consumed by:** `prototype-app-scaffolder.md` (authors at scaffold), `prototype-landing-updater.md` (regenerates registry + landing), `prototype-generator.md` (routes mount inside the shell). Honours PI-05 + PI-08 (`framework/shared/prototype-invariants.md`).

---

## File map

| File | Authored by | Regenerated? | Role |
|---|---|---|---|
| `src/app/layout.tsx` | scaffolder | never | RootLayout: html/body, imports `globals.css`, seeds stores on mount, renders `<PrototypeChrome>` around `{children}`. |
| `src/components/organisms/PrototypeChrome.tsx` | scaffolder | never | The review harness: inter-prototype nav, role switcher (PI-05), data-reset, current-prototype info. |
| `src/stores/proto-chrome-store.ts` | scaffolder | never | Zustand store for chrome state: `activeRole`, setters. Not persisted (session chrome state). |
| `src/data/prototype-registry.ts` | scaffolder (empty) | **yes** (landing-updater) | Typed array of all prototypes `{ name, slug, route, scope_slug, scope_label, posture_label, position_labels[], roles[] }`. Imported by landing + chrome. |
| `src/app/page.tsx` | scaffolder (empty) | **yes** (landing-updater) | Landing: lists prototypes grouped by `scope_slug`. |

`prototypes/.registry.json` (repo-root, non-routed) is the **orchestrator-canonical** record; the landing-updater keeps `src/data/prototype-registry.ts` in sync with it (the TS module is what the app imports; the JSON is what the orchestrator reads for resumability/collision detection). Both are regenerated together.

---

## `layout.tsx` (RootLayout)

- `'use client'`; imports `./globals.css`.
- On mount (`useEffect`) calls `seedAllStores()` from `@/data/seed` (idempotent; rehydrates persisted stores then seeds from fixtures if empty — same contract as the template's `seed.ts`).
- Wraps `{children}` in `<ErrorBoundary>` (template already ships `src/components/ErrorBoundary.tsx`) and `<PrototypeChrome>`.
- `<head>` title "Prototype" (generic; per-prototype `<title>` set by route metadata).

## `PrototypeChrome` (the review harness — PI-08)

A persistent bar/rail **outside** the app-under-design, visually marked as a prototype tool (not part of any requirement). Reads `usePathname()` to find the active prototype in `prototype-registry.ts`.

Contains:
1. **Inter-prototype nav** — a "Prototypes" link to `/` (landing) + a quick switcher (dropdown/command) listing all registry entries grouped by scope. Lets a reviewer jump between prototypes of the same scope to compare UX (the core purpose).
2. **Role switcher (PI-05)** — a select listing the active prototype's `roles[]` (from the registry); writes `activeRole` to `proto-chrome-store`. Every multi-role surface reads `activeRole` to vary visible components/actions per §6.5 RBAC. Hidden (or single, disabled) when the active prototype has one role.
3. **Data reset** — a button calling `resetAllStores()` (`@/data/seed`), re-seeding fixtures (PI-02). Confirmation per `GR-04`.
4. **Current-prototype info** — when on a prototype route, shows its `prototype_name`, `scope_label`, `posture_label`, and `position_labels[]` (plain-English from `position-vocabulary.md`) so a reviewer knows which design they're experiencing. On the landing route, shows nothing or a one-line app title.

Chrome styling uses the shared brand theme but is visually distinct (e.g. a slim top bar with a "PROTOTYPE" tag) so reviewers never mistake it for the app. It is **not** part of any requirement and carries no `data-prop`/`data-src` (PI-08).

## `proto-chrome-store.ts`

Zustand store (not persisted): `{ activeRole: string | null, setActiveRole(role) }`. Default `activeRole` = the active prototype's first role on route change.

## `prototype-registry.ts` (regenerated)

```ts
export interface PrototypeEntry {
  name: string          // consultant-given name
  slug: string          // name-slug (route segment)
  route: string         // "/<slug>"
  scope_slug: string
  scope_label: string   // human scope intent
  posture_label: string // e.g. "Analytical / Information-Dense"
  position_labels: string[] // plain-English D1–D5 labels from position-vocabulary.md
  roles: string[]       // §3 roles in scope (drives the role switcher)
}
export const PROTOTYPES: PrototypeEntry[] = [ /* regenerated additively per run */ ]
```

## `page.tsx` (landing — regenerated)

- Imports `PROTOTYPES` from `@/data/prototype-registry`.
- Groups entries by `scope_slug`; renders one section per scope (heading = `scope_label`).
- Each prototype → a card (shared `Card`) with: `name`, `posture_label`, `position_labels` as chips (shared `Badge`), `roles`, and a primary link/button to `route`.
- Same-scope prototypes sit side-by-side so a reviewer can compare UX approaches (the purpose).
- Empty state (no prototypes yet): friendly message + "Run /prototype to generate one" (this is the scaffold-time initial content; satisfies `GR-08`).
- Regeneration is **additive**: never drops an existing entry; a per-prototype reset removes only that entry.

---

## Self-validation
- Shell + chrome authored once; not regenerated per prototype.
- Chrome renders the active prototype's roles in the role switcher (PI-05) and a data-reset (PI-02); it is visually distinct and carries no requirement bindings (PI-08).
- `prototype-registry.ts` and `.registry.json` are kept in sync by the landing-updater; the app imports the TS module (never the root JSON across the src boundary).
- Landing groups by scope and renders same-scope prototypes together.
- The empty app (no entries) builds and renders the empty-state landing.

## Anti-patterns
- Do not regenerate the shell or chrome per prototype — only the registry module + landing page change between runs.
- Do not import `prototypes/.registry.json` from inside `src/` (cross-tree import). The app imports `src/data/prototype-registry.ts`.
- Do not let the chrome leak into the app-under-design's `data-prop`/`data-src` space — it is a harness (PI-08).
- Do not render the app's **brand logo** in `PrototypeChrome`. The captured brand logo (`public/brand/logo.*`, from `.scaffold.json` `brand_logo`) belongs to the **application shell** — the generator renders it in the per-prototype `src/app/<name_slug>/layout.tsx` brand slot (`step-05-compose-route.md`), not in this review harness. The chrome stays brand-marked-as-a-tool, never carrying the product's own logo.
- Do not have the landing-updater drop or reorder other prototypes' entries — regeneration is additive (a reset removes exactly one entry).
- Do not theme the chrome off-brand — it uses the shared tokens but is *visually marked* as a tool, not *styled differently per prototype*.
