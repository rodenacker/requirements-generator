# Prototype app shell & chrome spec (`app-shell-spec.md`)

**Role:** asset (prototype-private).

**Purpose:** Specify the **shared** application shell, the **prototype chrome** (review harness), the **landing page**, and the **prototype registry** module — all authored **once** by `prototype-app-scaffolder.md` (shell + chrome + empty landing/registry) and thereafter only the registry + landing are **regenerated additively** by `prototype-landing-updater.md`. The shell and chrome are static code shared by every prototype; they must never be regenerated per prototype.

**Consumed by:** `prototype-app-scaffolder.md` (authors at scaffold), `prototype-landing-updater.md` (regenerates registry + landing), `prototype-generator.md` (routes mount inside the shell). Honours PI-05 + PI-08 (`framework/shared/prototype-invariants.md`).

---

## File map

| File | Authored by | Regenerated? | Role |
|---|---|---|---|
| `src/app/layout.tsx` | scaffolder | never | RootLayout: html/body, imports `globals.css`, carries the colour-mode init script, seeds stores on mount, renders `<PrototypeChrome>` around `{children}`. |
| `src/components/atoms/ThemeToggle.tsx` | scaffolder | never | Colour-mode control. Authored **only** when `.scaffold.json` `colour_mode.strategy ∈ {toggle, custom}`. |
| `e2e/theme-modes.smoke.spec.ts` | scaffolder | never | Proves the colour-mode mechanism. Authored **only** when `colour_mode.sets == ["light","dark"]`. |
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
- **`<html lang="en" suppressHydrationWarning>` — required, not optional.** The init script below mutates `documentElement.className` before React hydrates; without `suppressHydrationWarning` React logs a hydration mismatch, and the smoke's zero-console-errors assertion turns that into a failing gate on **every** prototype.
- Carries the **colour-mode init script** — see below.

## Colour-mode mechanism

One mechanism for every strategy: **the `.dark` class on `<html>`**. `globals.css` already ships `@custom-variant dark (&:is(.dark *))`, and `theme.css`'s `.dark` block matches the element directly — so the class drives both the token values and every shadcn `dark:` utility. Nothing here changes `globals.css`.

The strategy comes from `prototypes/.scaffold.json` `colour_mode.strategy`, fixed at scaffold. Choose **one** of the following literal blocks — do not improvise a variant.

**`toggle` and `custom`** — a blocking inline `<script>` as the first child of `<head>`, via `dangerouslySetInnerHTML` (the template already renders `<head>` manually inside a `'use client'` layout, so this is well-formed). It must run before first paint; a `useEffect` would flash the wrong theme.

```
(function(){try{
  var p = localStorage.getItem('prototype-colour-mode') || 'system';
  var d = p === 'dark' || (p === 'system' && matchMedia('(prefers-color-scheme: dark)').matches);
  document.documentElement.classList.toggle('dark', d);
}catch(e){}})()
```

**`system`** — the same script without the stored preference, plus a live listener so a mid-session OS change is picked up:

```
(function(){try{
  var m = matchMedia('(prefers-color-scheme: dark)');
  var a = function(){ document.documentElement.classList.toggle('dark', m.matches) };
  a(); m.addEventListener('change', a);
}catch(e){}})()
```

**`none`** — **no script at all.** If the single token set is dark, put the class on the element literally: `<html lang="en" className="dark" suppressHydrationWarning>`. This is what keeps the shadcn `dark:` branches and `color-scheme` agreeing with a dark-only palette. If the single set is light, no class and no `className` prop.

The `try/catch` is deliberate: a browser with `localStorage` disabled must still render, just without the stored preference.

## `ThemeToggle` (`src/components/atoms/ThemeToggle.tsx`)

Authored **only** for `strategy ∈ {toggle, custom}`. No new dependency — `lucide-react` and the shadcn `Button` already ship.

- **Three states, cycling System → Light → Dark → System.** A two-state button initialised from the OS can never return to *following* the OS, which is the documented default.
- Reads/writes `localStorage['prototype-colour-mode']` (`'system' | 'light' | 'dark'`) and applies the resolved value with `documentElement.classList.toggle('dark', …)` — the same expression the init script uses, so there is exactly one way the class is ever set.
- While in `system`, subscribes to `matchMedia('(prefers-color-scheme: dark)')` `change` and re-applies; unsubscribes on unmount and when leaving `system`.
- Initial state comes from `localStorage` in a mount effect, **not** during render — the server-rendered markup must not depend on it.
- Icons: `Monitor` / `Sun` / `Moon` (lucide), inheriting `currentColor`. Never a literal colour class.
- Accessible: `aria-label` naming the *current* state and what the next click does (e.g. *"Colour mode: follows system. Switch to light."*); ≥24×24 CSS px target per `ux-baseline-checklist.md`; visible focus ring.
- **UI-only control.** No `data-src` / `data-prop` — same exemption class as search, sort, pagination and the density toggle (`shared-component-conventions.md`).
- Persistence here is deliberate, and deliberately unlike `proto-chrome-store.ts` (which is session-only): the mode must be readable **synchronously before paint**, which a Zustand store cannot do.

A `custom` note may adjust the default state, the placement, or 2- vs 3-state. It may not change the class mechanism, the storage key, or add a third palette.

## `e2e/theme-modes.smoke.spec.ts`

Authored **only** when `colour_mode.sets == ["light","dark"]`. Proves the *mechanism* once, against `/` (the landing). The per-prototype smoke proves the *components* — see `verify-prototype-build.md`.

- Drive the mode with `page.emulateMedia({ colorScheme })`, which exercises the real `matchMedia` path the init script uses. Do **not** inject the class directly — that would test the assertion, not the app.
- **Disable transitions before any colour assertion**: `page.addStyleTag({ content: '*,*::before,*::after{transition:none!important;animation:none!important}' })`. Several shadcn primitives transition `background-color`/`color`, and `getComputedStyle` mid-transition returns the *previous* mode's colour — measured on this template, a primary button reads the light pair for ~150ms after the class flips. Class assertions are unaffected; colour assertions are not.
- In each mode: assert `documentElement` has/lacks `.dark`, and that `getComputedStyle(body).backgroundColor` differs between the two and matches that mode's `--background` token.
- `strategy: toggle` — click the toggle through the full System → Light → Dark cycle asserting the class at each step; then `page.reload()` and assert the choice survived **and** that the class is already correct before `networkidle` (the no-FOUC check).
- `strategy: system` — assert no toggle is present and that `emulateMedia` alone flips the app live.
- Additive: never delete or weaken other specs.

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
- Renders `<ThemeToggle />` in its page header when `colour_mode.strategy ∈ {toggle, custom}`. This is the landing page of the prototypes app, so the control belongs here as app chrome — and it guarantees the mode stays reachable even for a prototype whose nav model needs no app-shell header of its own.
- Same-scope prototypes sit side-by-side so a reviewer can compare UX approaches (the purpose).
- Empty state (no prototypes yet): friendly message + "Run /prototype to generate one" (this is the scaffold-time initial content; satisfies `GR-08`).
- Regeneration is **additive**: never drops an existing entry; a per-prototype reset removes only that entry.

---

## Self-validation
- Shell + chrome authored once; not regenerated per prototype.
- `layout.tsx` carries `suppressHydrationWarning` on `<html>` and exactly one of the three literal init blocks (or none, for `strategy: none`); the class is never set from a `useEffect`.
- `ThemeToggle.tsx` exists iff `colour_mode.strategy ∈ {toggle, custom}`; `e2e/theme-modes.smoke.spec.ts` exists iff `colour_mode.sets == ["light","dark"]`. Neither appears in `PrototypeChrome`.
- For `strategy: none` with a dark single set, `<html>` carries a literal `className="dark"` and `theme.css`'s `:root` declares `color-scheme: dark`.
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
- **Do not render `ThemeToggle` in `PrototypeChrome`.** Cheaper — the chrome is on every route and needs no generator change — but wrong: PI-08 says the chrome carries nothing that "should be read as a feature of the product being specified", and a consultant answering *"a button in the UI"* is specifying product behaviour. The toggle belongs to the **application shell** (generator, `step-05-compose-route.md`) and the landing page, exactly like the brand logo above. Sitting it beside the role switcher and data-reset would tell reviewers the opposite of what was specified.
- Do not set the `.dark` class from anywhere but the init script and `ThemeToggle` — one expression, two call sites, no third path.
- Do not apply the colour mode in a `useEffect` in `layout.tsx`. It must be set before first paint, or every load flashes the wrong theme.
- Do not add `next-themes`. The mechanism above is ~50 lines and avoids a dependency in an environment where npm lifecycle scripts are constrained.
