# verify-prototype-build.md

**Purpose:** The `/prototype` **verify gate** (orchestrator Step F3, invoked by `prototype-generator`). Runs, in order, `lint` → `tsc --noEmit` → a **Playwright smoke** against **every** route the prototype authored, and returns a structured verdict. The smoke is what makes "hi-fi clickable" (rule 13) a checked guarantee rather than a hope. On any failure the caller (the generator driver) does a bounded retry of the offending surface; exhaustion routes to `RF-12`.

> **Why no production build.** The gate deliberately omits `next build`. Prototypes are client-side only (PI-01..PI-08): fixture-backed, server simulated, demoed from `next dev`. The smoke's `webServer` auto-starts `npm run dev`, so a production bundle is never exercised, and `tsc --noEmit` already covers the type-error class. The failure modes `next build` uniquely catches (RSC serialization, `"use client"` boundaries, static generation, build-time tree-shaking) cannot occur under those invariants. If a future prototype ever ships a real server component, restore the `build` phase here (and in the `phase` enum below + the RF-11/RF-12 trigger lists).

**Caller-agnostic; today's caller is `prototype-generator.md` (step-06).**

## Inputs

- `app_dir` — `"prototypes/"`. Required.
- `name_slug` — the prototype's route segment. Required.
- `route` — `"/<name_slug>"`. Required. The prototype's **primary** route (the landing link, and the one the both-modes contrast sweep measures).
- `routes` — **every** route this prototype authored, `route` first. Optional; when absent or empty, defaults to `[route]`. The caller assembles it from the driver's `route_map` plus each sub-agent manifest's `route_written` (`prototype-generator/steps/step-06-verify-build.md`) — both already exist, so nothing new is computed. The default keeps every other caller, and the pre-`routes` behaviour, working unchanged.
- `attempt` — the verify attempt number (1 on first call; the generator's bounded-retry increments it on re-invocation). Optional, default `1`. Stamped onto the phase timing events so a clean run is distinguishable from an N-attempt one.
- **`colour_mode`** — read from `<app_dir>.scaffold.json` (not passed in). Two fields matter here: `colour_mode.sets` — when it holds **two** entries the smoke exercises both colour modes, otherwise that part is byte-identical to the single-mode behaviour; and `colour_mode.strategy` — when it is `toggle` or `custom` the per-route toggle assertions in step 1 are emitted, otherwise they are omitted (no `ThemeToggle.tsx` exists to find). A missing or malformed `colour_mode` is treated as single-mode with no toggle.

## Outputs

Exactly one of:
- **`pass`** — all three phases passed.
- **`pass-with-warning`** — `lint`+`tsc` passed and the smoke was **skipped** per the consultant's `RF-11 skip-smoke-with-warning` choice. Carries `{ smoke_skipped: true }`.
- **`RF-11 trigger`** — the smoke could not run because Playwright browsers are not installed. The orchestrator surfaces `RF-11` (`{install-and-retry, skip-smoke-with-warning, abort}`); `skip-smoke-with-warning` re-invokes this skill with smoke disabled → `pass-with-warning`.
- **structured-fail** — `{ "phase": "lint"|"typecheck"|"smoke", "summary": "<≤300-char error excerpt>" }`. The generator retries the offending surface (≤2); persistent failure → the generator/orchestrator surfaces `RF-12` (hard).

## Procedure

1. **Author the smoke spec (idempotent).** Ensure `<app_dir>e2e/<name_slug>.smoke.spec.ts` exists; (re)write it from this generic template (parametrised by `routes`) — **one `test()` per route**, so a failure names the route that broke:
    ```ts
    import { test, expect } from '@playwright/test'
    const ROUTES = ['<route>', '<route-2>', '<route-3>']  // = `routes`; `route` first
    for (const ROUTE of ROUTES) {
      test(`${ROUTE} renders, is clickable, no console errors`, async ({ page }) => {
        const errors: string[] = []
        page.on('console', m => { if (m.type() === 'error') errors.push(m.text()) })
        page.on('pageerror', e => errors.push(String(e)))
        const resp = await page.goto(ROUTE, { waitUntil: 'networkidle' })
        expect(resp?.status() ?? 200, 'route responds < 400').toBeLessThan(400)
        await expect(page.getByTestId('proto-chrome'), 'prototype chrome present (PI-05/PI-08)').toBeVisible()
        // The next two lines ONLY when colour_mode.strategy ∈ {toggle, custom} — omit entirely otherwise.
        await expect(page.locator('[data-slot="colour-mode-toggle"]').first(),
          'colour-mode toggle reachable in the application shell').toBeVisible()
        await expect(page.getByRole('button', { name: /colour mode/i }).first(),
          'colour-mode toggle carries its accessible name').toBeVisible()
        const cta = page.getByTestId('primary-cta')
        if (await cta.count()) { await expect(cta.first()).toBeEnabled(); await cta.first().click() }
        expect(errors, `no console/page errors on ${ROUTE}: ${errors.join(' | ')}`).toHaveLength(0)
      })
    }
    ```
   **Every authored route is visited — this is load-bearing, not thoroughness for its own sake.** Until 2026-07-29 the template hardcoded a single `const ROUTE = '<route>'`, so a prototype's secondary routes had **zero** runtime coverage: a real run shipped a hydration mismatch on a secondary page that the `no console/page errors` assertion above would have caught on the first visit, and a shell with no colour-mode toggle on three of five pages. Both were invisible to every gate. Do not collapse this back to one route, and do not sample a subset — the route list is small (one per standalone surface) and each visit is a page load, not a suite.

   The **two toggle assertions are deliberately paired**: `data-slot` alone passes with a missing or drifted `aria-label`, which is itself a requirement of the `ThemeToggle` contract (`framework/assets/prototypes/app-shell-spec.md`). Two assertions, two distinct failure messages. A prototype that composes **no** shell component on any route is the documented fallback in `step-05-compose-route.md` rule 2 — it is **not** an exemption here; it fails these assertions deliberately, because the reviewer then has no colour-mode control inside the app.
   **This file is the canonical owner of the prototype app's runtime test-hook vocabulary.** The hooks and their stampers:

   | Hook | Stamped on | Stamped by |
   |---|---|---|
   | `data-testid="proto-chrome"` | the `PrototypeChrome` root | `prototype-app-scaffolder.md` (once, per `app-shell-spec.md`) |
   | `data-testid="primary-cta"` | each route's primary action | `prototype-generator.md` (per route; omitted only where a surface has no primary action — the smoke then skips the click) |
   | `data-slot="colour-mode-toggle"` | the `ThemeToggle` `Button` | `prototype-app-scaffolder.md` (once, per `app-shell-spec.md`) |

   Every mention elsewhere — in `prototype-generator.md`'s Self-validation, the generator steps, `app-shell-spec.md` — is a **reference to this table**, not a second definition. Adding a hook means adding a row here first. Authoring the spec is additive — never delete other prototypes' smoke specs.

   **Division of labour with `e2e/theme-modes.smoke.spec.ts`** (scaffold-owned, authored once, never regenerated — see `app-shell-spec.md`). That file keeps the two things it can prove without knowing this prototype's routes: the colour-mode **mechanism** against `/`, and the static `theme.css` **token-pair contrast audit**. Its per-route toggle loop iterates `PROTOTYPES[].route` from the registry, and a registry entry carries exactly **one** `route` per prototype — so that loop is, structurally, primary-route-only and can never see a secondary route. The per-prototype spec above is therefore where per-route toggle coverage lives: it is the only place the full authored route list is known. Both assertions are kept; they are complements, not duplicates.
1b. **Append the both-modes test — only when `colour_mode.sets` has two entries.** Append a second `test()` to the same spec file. It reuses the already-loaded page: one `emulateMedia` call per mode, no extra browser launch and no extra navigation.

    **Scoped to the primary `route` only — a deliberate, disclosed bound.** Unlike step 1's per-route sweep, this test is not multiplied across `routes`: it is the expensive assertion (two full DOM sweeps plus a hover pass), and the components it measures are **shared** across every route of the app, so a hardcoded label colour fails on the primary route as readily as on a secondary one. If a future run finds a contrast defect that only a secondary route renders, widen this to `routes` then — but widen it knowingly, and say so, rather than discovering the bound by accident.

    Why per prototype, when the mechanism is app-level: the *mechanism* is proven once by `e2e/theme-modes.smoke.spec.ts` (scaffold-authored). The *components* are new code on every run, and a hardcoded label colour is the most likely colour-mode defect — on real dark palettes `text-white` on a status fill measures ~2.1:1. That cannot be caught once.

    ```ts
    test('renders legibly in both colour modes', async ({ page }) => {
      await page.goto(ROUTES[0], { waitUntil: 'networkidle' })  // the primary route — see the bound above
      // MANDATORY: kill transitions/animations before measuring — see the note below.
      await page.addStyleTag({ content:
        '*,*::before,*::after{transition:none!important;animation:none!important}' })
      for (const scheme of ['light', 'dark'] as const) {
        await page.emulateMedia({ colorScheme: scheme })
        const bad = await page.evaluate(() => { /* the sweep — see below */ })
        expect(bad, `contrast failures in ${scheme}: ${JSON.stringify(bad)}`).toHaveLength(0)
        // hover pass: for up to 10 interactive elements, hover then re-measure that element
      }
    })
    ```

    > **Transitions must be disabled before measuring — this is not optional.** The shadcn `Button` carries `transition-all`, and `Input`/`Select`/`Badge` carry `transition-[color,box-shadow]`. `getComputedStyle` during a running transition returns the **current interpolated value**, which immediately after a mode flip is still the *old* colour. Measured empirically on this template: right after adding `.dark`, a primary button still reported `rgb(0,73,193)`/`rgb(250,250,250)` — the light pair — and only after the transition settled did it report the correct `rgb(59,130,206)`/`rgb(10,10,10)`. A sweep that skips this does not merely flake: it silently measures the **light** colours while believing it is testing dark, so it passes a genuinely broken dark mode. The `addStyleTag` above makes every read instant and deterministic; it changes only timing, never the final computed value. Apply the same treatment after `hover()` — hover fills transition too.

    **The sweep**, bounded deliberately — it targets the failure class that bites, not WCAG conformance:
    - **Elements:** visible text inside `button, a, [role="button"], [data-slot="badge"], td, th, label, h1, h2, h3, h4`.
    - **Measure:** the element's computed `color` against its *effective* background — walk ancestors until a non-transparent `background-color`, compositing any alpha over what is behind it. Fail below **4.5:1**, or **3:1** for text ≥24px or ≥18.66px bold.
    - **Skip:** `opacity: 0`, `visibility: hidden`, `display: none`, zero-size, empty/whitespace text, and any element whose effective background involves a `background-image` or gradient. These are the honest false-positive corners; excluding them keeps the gate trustworthy.
    - **Hover:** for the first ≤10 interactive elements, `hover()` and re-measure **that element's own** text. This is the direct check for a label that passes at rest and fails on hover — on real palettes a primary button can read 4.97:1 at rest and 4.31:1 under `hover:bg-primary/90`.
    - **Icons:** every `svg` inside those elements must resolve its stroke/fill to `currentColor` or to the same computed `color` as its parent — never a divergent literal.
    - **Report:** each failure as `{ selector, color, background, ratio, state }` so the generator's retry can locate it.
2. **lint.** `npm run lint` in `app_dir`. Non-zero exit → return `structured-fail {phase:"lint"}` (excerpt the first error block).
3. **typecheck.** `npx tsc --noEmit` in `app_dir`. Non-zero → `structured-fail {phase:"typecheck"}`.
4. **smoke** (unless disabled by the caller for the `RF-11 skip` path). Run, in `app_dir` (the config's `webServer` auto-starts `npm run dev`):
    - single-mode: `npx playwright test e2e/<name_slug>.smoke.spec.ts --project=desktop-chrome` — **unchanged**.
    - two modes: `npx playwright test e2e/<name_slug>.smoke.spec.ts e2e/theme-modes.smoke.spec.ts --project=desktop-chrome`.
    - If the run aborts because **browsers are missing** (error matching `Executable doesn't exist` / `playwright install`) → return `RF-11 trigger` (do not treat as a test failure).
    - Test failure (assertion failed) → `structured-fail {phase:"smoke"}` with the failing assertion message.
    - Pass → continue.
5. **Return** `pass` (or `pass-with-warning` when the smoke was skipped).

## Timing log (sub-steps)

Wrap each phase that actually runs in a `substep_start`/`substep_end` pair appended to `framework/state/timing.ndjson` (`stage: "verify"`, `run_id` from the caller's context). This is the **canonical owner** of the verify substep vocabulary: `substep ∈ { lint, typecheck, smoke }` (add `build` here if the `build` phase is ever restored — see the "Why no production build" note). Stamp `attempt` (from Inputs) on **both** events, and `outcome: "pass"|"fail"` on the `substep_end`. The verify-phase durations are the system's **"real compute"** signal — what the timing reporter sums into the compute bucket.

- A phase that **fails and short-circuits** still emits its `substep_end` with `outcome:"fail"` (a known result, not a halt) and the later phases simply do not run (no orphan). The orphan-`substep_start`-is-halt-signal contract applies only to an *unexpected* abort mid-phase.
- Same append-only PowerShell `Add-Content` idiom, timestamp capture, and paired-adjacent batching as `framework/agents/requirements-drafter.md > Timing log (sub-steps)`. Observability only; never read or gate on it.

```powershell
$now = (Get-Date).ToUniversalTime().ToString('o')
@{t=$now; type='substep_start'; stage='verify'; substep='lint'; attempt=1; run_id='<run_id-from-context>'} | ConvertTo-Json -Compress | Add-Content -Path framework/state/timing.ndjson
# … run `npm run lint` …
@{t=(Get-Date).ToUniversalTime().ToString('o'); type='substep_end'; stage='verify'; substep='lint'; attempt=1; outcome='pass'; run_id='<run_id-from-context>'} | ConvertTo-Json -Compress | Add-Content -Path framework/state/timing.ndjson
```

## Self-validation
- Phases ran in order; the first failure short-circuits and is returned with its phase + a bounded excerpt.
- The smoke spec exists under `<app_dir>e2e/` and emits **one `test()` per entry in `routes`** (never a single collapsed test, never a subset); the primary `route` is `ROUTES[0]`; other prototypes' smoke specs were not touched.
- The per-route colour-mode toggle assertions were emitted **iff** `colour_mode.strategy ∈ {toggle, custom}` — both of them (`data-slot` **and** the `/colour mode/i` accessible name), on every route.
- The both-modes contrast test targets `ROUTES[0]` only, and that bound is stated in the spec file's own comment rather than left implicit.
- A missing-browser condition returns `RF-11 trigger`, never a `structured-fail {phase:"smoke"}` (the two are different recoveries).
- The `colour_mode.sets` branch was evaluated in exactly **one** place, and the single-mode path — spec content and Playwright command — is byte-identical to the pre-colour-mode behaviour. Single-mode runs pay nothing.
- When two modes are live: the both-modes test was appended (not replacing the base test), `e2e/theme-modes.smoke.spec.ts` was included in the run, and a contrast failure surfaced as `structured-fail {phase:"smoke"}` naming the selector and ratio.

## Anti-patterns
- **Do not collapse the per-route loop back to a single route, and do not sample a subset of `routes`.** That is the exact hole a real run shipped through: a hydration mismatch and three toggle-less shells, all on secondary routes, all invisible because only `/<name_slug>` was ever visited. If a route is genuinely unvisitable, say which and why in the returned summary — never drop it silently (`CLAUDE.md`: no silent caps).
- Do not conflate "Playwright browsers not installed" (`RF-11`, a setup pause) with "the smoke assertion failed" (`structured-fail`, a build defect).
- Do not silently skip the smoke — skipping only happens on the explicit `RF-11 skip-smoke-with-warning` path and yields `pass-with-warning`, recorded by the landing-updater.
- Do not delete or overwrite other prototypes' e2e specs; the smoke spec write is additive per `name_slug`.
- Do not "fix" a failing phase here — return the structured fail; remediation (regenerate the surface) is the generator's job, and exhaustion is `RF-12`.
- Do not run the both-modes test when only one token set exists. There is no second palette to exercise, and the sweep would just re-assert the light pass at double cost.
- Do not add a second Playwright *project* for dark. `emulateMedia` flips the mode in-page; a project re-runs the whole suite in a fresh browser to learn the same thing.
- Do not set the `.dark` class directly from the spec. Drive it through `emulateMedia` so the app's own init script does the work — injecting the class tests the assertion, not the application.
- **Do not measure colour without disabling transitions first.** A mid-transition read returns the previous mode's colour, so the sweep "passes" by measuring light values while nominally in dark. This is the one failure mode that makes the gate actively misleading rather than merely absent. Do not substitute a fixed `waitForTimeout` — durations are token-driven (`--transition-*`) and brand-dependent, so a hardcoded wait is a guess.
- Do not widen the sweep into a general accessibility audit. It is scoped to labels and icons on filled surfaces. If broader coverage is wanted later, add `@axe-core/playwright` deliberately — do not let this grow into it by accident.
- Do not weaken the sweep to make a prototype pass. A contrast miss consumes the generator's retry budget and can reach `RF-12`; that is intended — a prototype with invisible labels should not reach the landing page.
