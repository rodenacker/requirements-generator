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
| `e2e/craft.smoke.spec.ts` | **template (copied, not authored)** | never | Proves the visual-craft invariants: every craft token resolves, Tailwind's `shadow-*`/`text-*`/`font-*` scales regenerate against the brand values, a pressed control scales to 98%, an `aria-disabled` control does not, and `prefers-reduced-motion` collapses the transition. Ships in `template/e2e/` so **every** app gets it — deliberately *not* hung off `theme-modes.smoke.spec.ts`, which only exists when two colour modes do, and craft invariants are mode-independent. The scaffolder authors nothing here; it arrives with the copy. |
| `src/components/organisms/PrototypeChrome.tsx` | scaffolder | never | The review harness: inter-prototype nav, role switcher (PI-05), data-reset, current-prototype info. |
| `src/stores/proto-chrome-store.ts` | scaffolder | never | Zustand store for chrome state: `activeRole`, setters. Not persisted (session chrome state). |
| `src/data/prototype-registry.ts` | scaffolder (empty) | **yes** (landing-updater) | Typed array of all prototypes `{ name, slug, route, scope_slug, scope_label, posture_label, position_labels[], roles[] }`. Imported by landing + chrome. |
| `src/data/nav/index.ts` | scaffolder (empty) | **yes** (generator, additively per prototype) | The intra-prototype nav barrel: `NavEntry` + `NAV_BY_PROTOTYPE`. Shape canonical in `shared-component-conventions.md §6a`. Imported by the chrome (role-switcher disabled state) and by every application shell (nav items). Distinct from the registry — that is one row *per prototype*, this is the destination list *within* each. |
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
- Carries the **brand webfont links** — see below.

## Brand webfont loading

**Without this the brand typeface never loads.** `theme.css` sets `--font-sans: '<Family>', sans-serif`, but a font family declared in CSS is not a font *fetched* — with no `@font-face` and no stylesheet link the browser silently falls through to the generic terminal, so a prototype renders in `system-ui` while every token file says otherwise. `/design-system` spends a whole rules file (`design-system-styler/data/font-rules.md`, four enforcement points) choosing a licensable brand face; this is where that choice becomes visible.

Render these as the **first children of `<head>`**, before the colour-mode script:

```tsx
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap"
/>
```

- Build the `family=` segments from the **named** family of `--font-heading` and `--font-sans` in `theme.css` (the part before the generic terminal, URL-encoded with `+` for spaces). Emit **one** `family=` segment when the two resolve to the same face — the common case, since the design-system's two families are usually identical.
- Weights are always `400;500;600;700`. That covers `--brand-body-weight` and `--brand-heading-weight` for every value the design-system emits (`font-rules.md` constrains weights to two of these) plus the `font-medium`/`font-semibold` utilities the primitives use. Do not compute a narrower axis list — a missing weight is synthesised by the browser as a smeared faux-bold, which looks worse than the extra request.
- `display=swap` is required: text paints immediately in the fallback and reflows once, rather than blocking first paint on a network fetch the smoke gate is timing.
- Record the emitted href in `.scaffold.json` as `brand_fonts.href` (plus `brand_fonts.families`) so a later run can tell what was requested without re-parsing `theme.css`.
- When the brand source is `template-defaults`, this still runs — the template default names `Inter`, which is a real face worth loading.

**A `<link>`, not `next/font/google` — deliberate.** `next/font` resolves and self-hosts the face at **build** time, so a machine without network access turns a cosmetic concern into a hard scaffold failure (`RF-13`). A stylesheet link degrades gracefully: offline, or for a family that is not on Google Fonts, the request fails and rendering falls through to the generic terminal that `font-rules.md §4` guarantees every emitted stack carries (`'Manrope', sans-serif` — one named family, one generic). The prototype stays correct and buildable either way; it is only less pretty. Do not "upgrade" this to `next/font` — and note that this layout is `'use client'`, so it cannot export `metadata` and has no server-side font pipeline available to it anyway.

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
- Initial state is read from `localStorage` through **`useSyncExternalStore`** (with a `getServerSnapshot` returning `'system'`), **not** during render and **not** seeded into `useState` from a mount effect — the server-rendered markup must not depend on it. See the literal block below; the older mount-effect shape is a hard lint failure.
- **`data-slot="colour-mode-toggle"` on the `Button` — required.** This is the test hook the per-route presence assertion selects (`e2e/theme-modes.smoke.spec.ts`, below); the hook vocabulary itself is owned by `framework/skills/verify-prototype-build.md`. `data-slot` rather than a new `data-testid` because it is already the in-use convention (the shipped shadcn primitives stamp it on nine components, and the verify sweep already selects `[data-slot="badge"]`) and because it is immune to label drift. Passed as a prop it **replaces** the primitive's own `data-slot="button"` — harmless: nothing in the template, the sweep, or any CSS selects `[data-slot="button"]` (the sweep matches the `button` tag).
- Icons: `Monitor` / `Sun` / `Moon` (lucide), inheriting `currentColor`. Never a literal colour class.
- Accessible: `aria-label` naming the *current* state and what the next click does (e.g. *"Colour mode: follows your system setting. Switch to light."*). It **must** match `/colour mode/i` — the smoke asserts the accessible name additively, so a drifted or missing label fails loudly instead of silently. ≥24×24 CSS px target per `ux-baseline-checklist.md`; visible focus ring.
- **UI-only control.** No `data-src` / `data-prop` — same exemption class as search, sort, pagination and the density toggle (`shared-component-conventions.md`).
- Persistence here is deliberate, and deliberately unlike `proto-chrome-store.ts` (which is session-only): the mode must be readable **synchronously before paint**, which a Zustand store cannot do.

**Author this literal component** — as with the init blocks above, do not improvise a variant. `localStorage` is an *external* store, so it is read with `useSyncExternalStore`. The older *"initial state comes from `localStorage` in a mount effect"* shape is a **lint failure, not a style preference**: `eslint-plugin-react-hooks@7` (shipped transitively by `eslint-config-next@16`, verified 7.0.1 in `template/`) reports `react-hooks/set-state-in-effect` — *"Calling setState synchronously within an effect can trigger cascading renders"* — so `npm run lint` exits non-zero and `verify-prototype-build.md` returns `structured-fail {phase:"lint"}` on **every** fresh scaffold with `strategy ∈ {toggle, custom}`. The block below is lint-clean and typecheck-clean against `template/`.

```tsx
'use client'

import { useEffect, useSyncExternalStore } from 'react'
import { Monitor, Moon, Sun } from 'lucide-react'
import { Button } from '@/components/ui/button'

type Mode = 'system' | 'light' | 'dark'

const KEY = 'prototype-colour-mode'
const ORDER: Mode[] = ['system', 'light', 'dark']
const LABEL: Record<Mode, string> = {
  system: 'follows your system setting',
  light: 'light',
  dark: 'dark',
}

const listeners = new Set<() => void>()

function subscribe(onChange: () => void) {
  listeners.add(onChange)
  window.addEventListener('storage', onChange) // cross-tab
  return () => {
    listeners.delete(onChange)
    window.removeEventListener('storage', onChange)
  }
}

function getSnapshot(): Mode {
  try {
    const v = localStorage.getItem(KEY)
    return v === 'light' || v === 'dark' || v === 'system' ? v : 'system'
  } catch {
    return 'system'
  }
}

function getServerSnapshot(): Mode {
  return 'system'
}

function setMode(next: Mode) {
  try {
    localStorage.setItem(KEY, next)
  } catch {
    /* localStorage disabled — the click still applies for this session */
  }
  listeners.forEach((l) => l())
}

function isDark(mode: Mode) {
  return (
    mode === 'dark' ||
    (mode === 'system' && matchMedia('(prefers-color-scheme: dark)').matches)
  )
}

export default function ThemeToggle() {
  const mode = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot)

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark(mode))
  }, [mode])

  useEffect(() => {
    if (mode !== 'system') return
    const mq = matchMedia('(prefers-color-scheme: dark)')
    const apply = () => document.documentElement.classList.toggle('dark', mq.matches)
    mq.addEventListener('change', apply)
    return () => mq.removeEventListener('change', apply)
  }, [mode])

  const next = ORDER[(ORDER.indexOf(mode) + 1) % ORDER.length]
  const Icon = mode === 'light' ? Sun : mode === 'dark' ? Moon : Monitor

  return (
    <Button
      data-slot="colour-mode-toggle"
      variant="ghost"
      size="icon"
      aria-label={`Colour mode: ${LABEL[mode]}. Switch to ${LABEL[next]}.`}
      onClick={() => setMode(next)}
    >
      <Icon aria-hidden="true" />
    </Button>
  )
}
```

A `custom` note may adjust the default state, the placement, or 2- vs 3-state. It may not change the class mechanism, the storage key, the `data-slot` hook, or add a third palette.

**Where it is rendered.** The scaffolder renders it on the landing page only (`src/app/page.tsx`, below). Every **prototype route** gets it from the **application shell**, which the generator is unconditionally obliged to carry it in — `framework/agents/prototype-generator/steps/step-05-compose-route.md` rule 2 is canonical for that placement, and this file does not restate it.

## `e2e/theme-modes.smoke.spec.ts`

Authored **only** when `colour_mode.sets == ["light","dark"]`. Proves the *mechanism* once against `/` (the landing), **plus** two app-wide contracts that no other gate covers (below). The per-prototype smoke proves the *components* — see `verify-prototype-build.md`.

This file is authored once and **never regenerated**, so it must derive its coverage from the registry rather than from a fixed route list: `import { PROTOTYPES } from '@/data/prototype-registry'` (the tsconfig `@/*` path applies to `e2e/**`, which the `include` globs cover). Coverage then grows automatically with every future `/prototype` run at zero per-run cost. Skip the per-route loop cleanly when `PROTOTYPES` is empty (the scaffold-time state).

- Drive the mode with `page.emulateMedia({ colorScheme })`, which exercises the real `matchMedia` path the init script uses. Do **not** inject the class directly — that would test the assertion, not the app.
- **Disable transitions before any colour assertion**: `page.addStyleTag({ content: '*,*::before,*::after{transition:none!important;animation:none!important}' })`. Several shadcn primitives transition `background-color`/`color`, and `getComputedStyle` mid-transition returns the *previous* mode's colour — measured on this template, a primary button reads the light pair for ~150ms after the class flips. Class assertions are unaffected; colour assertions are not.
- In each mode: assert `documentElement` has/lacks `.dark`, and that `getComputedStyle(body).backgroundColor` differs between the two and matches that mode's `--background` token.
- `strategy: toggle` — click the toggle through the full System → Light → Dark cycle asserting the class at each step; then `page.reload()` and assert the choice survived **and** that the class is already correct before `networkidle` (the no-FOUC check).
- `strategy: system` — assert no toggle is present and that `emulateMedia` alone flips the app live.
- Additive: never delete or weaken other specs.

### (a) Per-route toggle presence — `strategy ∈ {toggle, custom}` only

The rule that the toggle lives in the **application shell** (`step-05-compose-route.md` rule 2) is enforced here, not by discipline. For **each** `PROTOTYPES[].route`, in its own `test()` so a failure names the route:

- navigate to the route, then `await expect(page.locator('[data-slot="colour-mode-toggle"]').first()).toBeVisible()`;
- **additively**, `await expect(page.getByRole('button', { name: /colour mode/i }).first()).toBeVisible()` — the `data-slot` hook alone would pass with a broken or missing `aria-label`, which is itself a requirement of the `ThemeToggle` section above. Two assertions, two distinct failure messages.

A prototype whose surfaces compose **no** shell component at all is the documented fallback in `step-05-compose-route.md`; it is **not** an exemption here — that prototype fails this test, which is the intended signal (the reviewer's colour-mode control is unreachable inside the app). Do not add a skip for it.

### (b) Static token-pair contrast audit — both blocks

The DOM sweep in `verify-prototype-build.md` only measures pairs some component happens to render. This audit checks the **tokens themselves**, so a wrong on-colour is caught even on a pair nothing renders yet. In one `test()`, with **no page navigation** (it is pure computation):

- read `src/styles/theme.css` with `node:fs` (`readFileSync`) at `path.resolve(process.cwd(), 'src/styles/theme.css')` — Playwright runs specs with `cwd` set to the project dir (verified: `cwd` reports `…/prototypes`). Do **not** use `new URL('…', import.meta.url)`: `import.meta` forces this spec to ESM output and the run then dies at config load with *"ReferenceError: require is not defined in ES module scope"*, before any test is collected (verified against `template/`);
- parse the `:root` and `.dark` blocks into `var → value` maps (hex values). A **block** that is absent is skipped silently — that is the legitimate single-mode case. An individual **var** that is absent is skipped *with a reported reason*, never silently;
- for each of these ten fill/on-colour pairs — the *Vars produced* rows of the *Contrast & on-colours* table in `framework/skills/extract-brand-theme.md`, restated here as an explicit list so the parser is unambiguous — compute the WCAG contrast ratio from sRGB relative luminance:

  `--primary`/`--primary-foreground`, `--secondary`/`--secondary-foreground`, `--destructive`/`--destructive-foreground`, `--error`/`--error-foreground`, `--success`/`--success-foreground`, `--warning`/`--warning-foreground`, `--info`/`--info-foreground`, `--sidebar-primary`/`--sidebar-primary-foreground`, `--accent`/`--accent-foreground`, `--sidebar-accent`/`--sidebar-accent-foreground`.

  Ten pairs per block — twenty checks when both blocks exist. Deliberately **not** included: `text`/`text_muted` against `background`/`surface`, which `/design-system` already gates (*What is not gated here*, same skill) — nor the `token/NN` opacity composites, which are the DOM sweep's job because they depend on what actually renders.
- assert **every** pair clears **4.5:1** in **both** blocks. Report each failure as `<block> <fill_var> <fill> × <fg_var> <fg> = <ratio>:1` so the number is in the failure message, and flag any pair below 3:1 as below even the large-text floor.
- Validated in both directions: the template's own `theme.css` passes all ten `:root` pairs, and a fixture carrying the run's five original `#FFFFFF` on-colours reports exactly those five — `--primary` at 3.98:1 (the same number this file already cites for that fill), `--warning` at 2.95:1, `.dark --secondary` at 1.23:1.

Why this exists: `extract-brand-theme.md` is already correct — it says *"Measure against the fill; never infer from the mode"* and calls an unclearable pair a FAIL. A real run nonetheless reported `contrast: { checked: 42, adjustments: "none" }` while five pairs failed (a light-mode `--warning-foreground: #FFFFFF` measured **2.94:1**, below even the 3:1 large-text floor). The skill needed no amendment; the *claim* needed to be checkable rather than exhortative. Skip a pair only when a var is genuinely absent from `theme.css`, and say which in the failure message — never silently.

## `PrototypeChrome` (the review harness — PI-08)

A persistent bar/rail **outside** the app-under-design, visually marked as a prototype tool (not part of any requirement). Reads `usePathname()` to find the active prototype in `prototype-registry.ts`.

**Its root element carries `data-testid="proto-chrome"` — required.** Every per-prototype smoke asserts it is visible (`framework/skills/verify-prototype-build.md`, the canonical owner of the runtime test-hook vocabulary — this is a reference, not a second definition). Omitting it does not degrade gracefully: it fails the verify gate on **every** prototype, consumes the generator's whole retry budget, and reaches `RF-12` — while the app itself looks fine in a browser, which makes it an expensive stamp to forget.

Contains:
1. **Inter-prototype nav** — a "Prototypes" link to `/` (landing) + a quick switcher (dropdown/command) listing all registry entries grouped by scope. Lets a reviewer jump between prototypes of the same scope to compare UX (the core purpose).
2. **Role switcher (PI-05)** — a select listing the active prototype's `roles[]` (from the registry); writes `activeRole` to `proto-chrome-store`. Every multi-role surface reads `activeRole` to vary visible components/actions per the requirements' §6.5 RBAC. Hidden (or single, disabled) when the active prototype has one role.
   - **Per-screen disabled state — required by PI-05, not optional polish.** PI-05 says *"roles to whom the active screen is not accessible per §6.5 RBAC are rendered in a **disabled** state"*. Resolve the current route in `NAV_BY_PROTOTYPE` (`import { NAV_BY_PROTOTYPE } from '@/data/nav'`; match the entry whose `route` equals `usePathname()`, else fall back to the prototype's primary entry) and render every role absent from that entry's `roles[]` as **disabled** — still listed, still visible, not selectable. **Disabled, never hidden:** a reviewer must be able to see that a role exists and is excluded here; silently dropping it is indistinguishable from the role not existing at all, which is the opposite of what PI-05 is for. The role *set* still comes from the registry (`roles[]`, i.e. §3 personas in scope); only the per-screen accessibility comes from the nav module.
   - Until 2026-07-29 this clause was unimplementable and unimplemented — the only role data the chrome could reach was the registry's flat per-prototype `roles[]`, with no per-screen dimension, so the spec stopped at hide-when-single-role. `shared-component-conventions.md §6a` supplies the missing table. **This file is authored once and never regenerated** (see the file map above), so this reaches **newly scaffolded apps only**; an existing `prototypes/` tree keeps the old chrome until it is re-scaffolded from scratch.
   - Falling back to the primary entry (rather than to "all roles enabled") matters for folded surfaces: a drawer/modal surface has no route of its own and renders on its host, so the host's entry is the correct authority for it.
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
  device_targets?: {    // OPTIONAL — absent on prototypes generated before the field existed
    primary: 'desktop' | 'tablet' | 'mobile'
    breakpoints: ('mobile' | 'tablet' | 'desktop')[]
    touch: boolean
  }
}
export const PROTOTYPES: PrototypeEntry[] = [ /* regenerated additively per run */ ]
```

## `page.tsx` (landing — regenerated)

- Imports `PROTOTYPES` from `@/data/prototype-registry`.
- Groups entries by `scope_slug`; renders one section per scope (heading = `scope_label`).
- Each prototype → a card (shared `Card`) with: `name`, `posture_label`, `position_labels` as chips (shared `Badge`), a **device badge** derived from `device_targets` when present (*Desktop only* / *Desktop + tablet* / *Responsive* / *Mobile first* — omitted entirely when the field is absent, never defaulted), `roles`, and a primary link/button to `route`. The device badge is what lets a reviewer comparing two same-scope prototypes see at a glance that one was built for a workstation and the other for a phone.
- **`device_targets` is optional in the interface on purpose.** The landing must typecheck against registry entries written before the field existed; a required field would break `tsc --noEmit` on any app carrying an older entry.
- Renders `<ThemeToggle />` in its page header when `colour_mode.strategy ∈ {toggle, custom}`. This is the landing page of the prototypes app, so the control belongs here as app chrome — and it guarantees the mode stays reachable even for a prototype whose nav model needs no app-shell header of its own.
- Same-scope prototypes sit side-by-side so a reviewer can compare UX approaches (the purpose).
- Empty state (no prototypes yet): friendly message + "Run /prototype to generate one" (this is the scaffold-time initial content; satisfies `GR-08`).
- Regeneration is **additive**: never drops an existing entry; a per-prototype reset removes only that entry.

---

## Self-validation
- Shell + chrome authored once; not regenerated per prototype.
- `layout.tsx` carries `suppressHydrationWarning` on `<html>` and exactly one of the three literal init blocks (or none, for `strategy: none`); the class is never set from a `useEffect`.
- `layout.tsx` carries the two `preconnect` links and one Google Fonts `stylesheet` link whose `family=` segments match the named families in `theme.css`'s `--font-heading` / `--font-sans`, at weights `400;500;600;700`, with `display=swap`; the href is recorded in `.scaffold.json` `brand_fonts`. No `next/font` import appears anywhere.
- `ThemeToggle.tsx` exists iff `colour_mode.strategy ∈ {toggle, custom}`; `e2e/theme-modes.smoke.spec.ts` exists iff `colour_mode.sets == ["light","dark"]`. Neither appears in `PrototypeChrome`.
- `ThemeToggle.tsx` was authored as the **literal block** above: `useSyncExternalStore` + `getServerSnapshot`, no `setState` inside any effect, `data-slot="colour-mode-toggle"` on the `Button`, and an `aria-label` matching `/colour mode/i`. `npm run lint` exits zero (the mount-effect shape does not — `react-hooks/set-state-in-effect`).
- `theme-modes.smoke.spec.ts` imports `PROTOTYPES` from `@/data/prototype-registry` and covers, beyond the `/` mechanism tests: (a) `[data-slot="colour-mode-toggle"]` visible **plus** the `/colour mode/i` accessible name on **every** `PROTOTYPES[].route` (for `strategy ∈ {toggle, custom}`), and (b) the static `theme.css` token-pair contrast audit over both blocks at 4.5:1. No route or pair is silently skipped.
- For `strategy: none` with a dark single set, `<html>` carries a literal `className="dark"` and `theme.css`'s `:root` declares `color-scheme: dark`.
- Chrome renders the active prototype's roles in the role switcher (PI-05) and a data-reset (PI-02); it is visually distinct and carries no requirement bindings (PI-08).
- The role switcher renders roles inaccessible on the **current screen** as **disabled** (not hidden), resolved from `NAV_BY_PROTOTYPE` — the full PI-05 clause, not just hide-when-single-role.
- `src/data/nav/index.ts` was authored with the `NavEntry` declaration and an **empty** `NAV_BY_PROTOTYPE`, and the zero-prototype app typechecks.
- **The chrome root carries `data-testid="proto-chrome"`.** Its absence fails every per-prototype smoke while leaving the app visually fine — check it explicitly rather than by eye.
- `prototype-registry.ts` and `.registry.json` are kept in sync by the landing-updater; the app imports the TS module (never the root JSON across the src boundary).
- Landing groups by scope and renders same-scope prototypes together.
- The empty app (no entries) builds and renders the empty-state landing.

## Anti-patterns
- Do not regenerate the shell or chrome per prototype — only the registry module + landing page change between runs.
- Do not import `prototypes/.registry.json` from inside `src/` (cross-tree import). The app imports `src/data/prototype-registry.ts`.
- Do not let the chrome leak into the app-under-design's `data-prop`/`data-src` space — it is a harness (PI-08).
- Do not render the app's **brand logo** in `PrototypeChrome`. The captured brand logo (`public/brand/logo.*`, from `.scaffold.json` `brand_logo`) belongs to the **application shell** — the generator renders it in whichever component wraps a surface's content, per-prototype `layout.tsx` or `templates/*Shell` (`step-05-compose-route.md` rule 2, canonical), not in this review harness. The chrome stays brand-marked-as-a-tool, never carrying the product's own logo.
- Do not have the landing-updater drop or reorder other prototypes' entries — regeneration is additive (a reset removes exactly one entry). The same applies to the generator and `src/data/nav/index.ts`.
- **Do not hide roles the current screen excludes — disable them.** PI-05 says disabled, and a hidden role is indistinguishable from a non-existent one, which defeats the point of a review harness.
- **Do not put intra-prototype routes in `prototype-registry.ts`, or per-prototype rows in `src/data/nav/`.** The registry is one row per prototype (the landing link), regenerated *after* the verify gate; the nav barrel is the destination list within a prototype, written *before* sub-agent dispatch. Merging them would put nav behind the gate that is supposed to check it (`shared-component-conventions.md §6a`).
- **Do not render nav in the chrome.** The chrome's nav is *inter*-prototype (jump between generated prototypes); the application's own nav belongs to the application shell (PI-08), exactly like the brand logo and the colour-mode toggle.
- Do not theme the chrome off-brand — it uses the shared tokens but is *visually marked* as a tool, not *styled differently per prototype*.
- **Do not render `ThemeToggle` in `PrototypeChrome`.** Cheaper — the chrome is on every route and needs no generator change — but wrong: PI-08 says the chrome carries nothing that "should be read as a feature of the product being specified", and a consultant answering *"a button in the UI"* is specifying product behaviour. The toggle belongs to the **application shell** (generator, `step-05-compose-route.md`) and the landing page, exactly like the brand logo above. Sitting it beside the role switcher and data-reset would tell reviewers the opposite of what was specified.
- Do not set the `.dark` class from anywhere but the init script and `ThemeToggle` — one expression, three call sites (the init script, the toggle's apply effect, and its `system` `matchMedia` handler), no fourth path.
- **Do not seed the toggle's initial mode into `useState` from a mount effect.** `localStorage` is an external store; read it with `useSyncExternalStore`. The mount-effect shape is not merely unfashionable — it is a `react-hooks/set-state-in-effect` error under `eslint-plugin-react-hooks@7`, so it fails `npm run lint` and hence the verify gate on every fresh scaffold with a toggle.
- **Do not omit `data-slot="colour-mode-toggle"` or drift the `aria-label` away from `/colour mode/i`.** Both are asserted per route by `theme-modes.smoke.spec.ts`; the label is a real accessibility requirement, not just a selector.
- **Do not omit `data-testid="proto-chrome"` from the chrome root.** It costs one attribute and its absence fails every prototype's verify gate.
- Do not narrow `theme-modes.smoke.spec.ts` to `/`. It is authored once and never regenerated, so route coverage must come from `PROTOTYPES` — a fixed route list freezes coverage at scaffold time, when no prototype exists yet.
- **Do not use `import.meta.url` in any e2e spec.** It forces ESM output for the spec and the whole Playwright run then fails at config load (*"require is not defined in ES module scope"*) with `No tests found` — a whole-suite outage, not a single failing test. Resolve files from `process.cwd()` instead.
- Do not give the token audit a browser or a `page.goto`. It is pure computation over `theme.css` and runs in milliseconds; navigating would only add flake.
- Do not apply the colour mode in a `useEffect` in `layout.tsx`. It must be set before first paint, or every load flashes the wrong theme.
- Do not add `next-themes`. The mechanism above is ~50 lines and avoids a dependency in an environment where npm lifecycle scripts are constrained.
- **Do not ship a layout with no font link.** A `--font-sans` that names a family nobody fetches is the quietest defect in the whole pipeline: every token file reads correctly, the build passes, the smoke passes, and the prototype renders in `system-ui`. Declaring a family is not loading it.
- **Do not replace the font `<link>` with `next/font/google`.** It moves the fetch to build time, so an offline machine fails the scaffold (`RF-13`) over a typeface. See the rationale in *Brand webfont loading*.
