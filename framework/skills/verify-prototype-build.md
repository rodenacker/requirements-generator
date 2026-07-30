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
- **`device_targets`** — `{ primary, breakpoints, touch }`, passed by the caller from the design-spec front-matter (resolved at `step-02` rule 1). Optional; absent behaves as `{ primary: "desktop", breakpoints: ["desktop"], touch: false }`, which is byte-identical to the pre-device behaviour. Maps onto Playwright projects declared in `template/playwright.config.ts`:

  | Breakpoint | Project | Viewport |
  |---|---|---|
  | `desktop` | `desktop-chrome` | 1280 × 800 |
  | `tablet` | `tablet-chrome` | 768 × 1024 |
  | `mobile` | `mobile-chrome` | 390 × 844, `hasTouch` |

  `primary` selects the project the **full** per-route sweep runs at; the remaining breakpoints get only the bounded layout-integrity test in step 1c. Named viewports and the per-target obligations are canonical in `framework/assets/prototypes/visual-craft-standard.md §11`.
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

   **Division of labour with the two app-level specs.** `e2e/craft.smoke.spec.ts` ships **with the template** (copied, never authored) and proves the visual-craft invariants that cannot vary per prototype: the craft tokens resolve on `:root`, Tailwind's `shadow-*`/`text-*`/`font-*` scales regenerate against brand values, a pressed control scales to 98%, an `aria-disabled` control does not, and `prefers-reduced-motion` collapses the transition. It is app-level and brand-independent, so it is proven **once** and costs a per-prototype run nothing — do not duplicate any of it into the per-prototype spec, and do not gate it on `colour_mode` (craft invariants are mode-independent, which is exactly why it does not live in the file below).

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
      await page.evaluate(INSTALL_SWEEP)   // the literal block below — author it verbatim
      for (const scheme of ['light', 'dark'] as const) {
        await page.emulateMedia({ colorScheme: scheme })
        const bad = await page.evaluate(() => (window as any).__protoSweep.measureAll('rest'))
        expect(bad, `contrast failures in ${scheme}: ${JSON.stringify(bad)}`).toHaveLength(0)
        // hover pass: for up to 10 interactive elements, hover then re-measure that element
        // via __protoSweep.measureOne(node, 'hover')
      }
      await page.emulateMedia({ colorScheme: null })
    })
    ```

    **`INSTALL_SWEEP` — author this block VERBATIM. Do not improvise the colour resolution.**
    Everything below the `resolve()`/`effectiveBg()` pair (the selector list, the thresholds, the icon check) is ordinary and may be adapted; **those two functions may not be**. They were re-derived from prose on every run until 2026-07-30, and the version one run produced could not read `oklab()` — which is what Tailwind v4 compiles **every** opacity modifier into (`bg-primary/90` → `color-mix(in oklab, …)`; `getComputedStyle` returns `oklab(0.773639 -0.0852014 -0.0883295 / 0.9)`). It treated the unparseable fill as *absent*, walked past it to an ancestor, and measured the label against a colour the element never had. Verified against Chromium, not assumed.

    ```ts
    const INSTALL_SWEEP = () => {
      interface RGBA { r: number; g: number; b: number; a: number }

      const canvas = document.createElement('canvas')
      canvas.width = 1
      canvas.height = 1
      const ctx = canvas.getContext('2d', { willReadFrequently: true })

      /**
       * oklab/oklch -> sRGB. FALLBACK ONLY — the canvas below converts natively in any
       * current Chromium. This exists because `playwright.config.ts` resolves whichever
       * system Chrome/Edge is installed (see its browser-resolution block), so the
       * browser's colour support is NOT pinned and a version too old for `oklch` is a
       * real deployment, not a hypothetical.
       */
      const oklabToRgb = (L: number, a: number, bb: number, alpha: number): RGBA => {
        // oklab -> LMS' -> linear LMS -> linear sRGB (Ottosson's inverse matrices).
        const l_ = L + 0.3963377774 * a + 0.2158037573 * bb
        const m_ = L - 0.1055613458 * a - 0.0638541728 * bb
        const s_ = L - 0.0894841775 * a - 1.291485548 * bb
        const l = l_ * l_ * l_, m = m_ * m_ * m_, s = s_ * s_ * s_
        const lr = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
        const lg = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
        const lb = -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s
        const enc = (v: number) => {
          const c = v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(Math.max(v, 0), 1 / 2.4) - 0.055
          return Math.min(255, Math.max(0, Math.round(c * 255)))
        }
        return { r: enc(lr), g: enc(lg), b: enc(lb), a: alpha }
      }

      /** Parse `oklab(L a b / A)` / `oklch(L C H / A)`. Hue units are REQUIRED, not optional:
       *  treating `rad`/`turn`/`grad` as degrees silently returns a wildly wrong colour
       *  (`oklch(0.7 0.15 4.36rad)` -> rgb(233,114,147) instead of rgb(75,163,247)). */
      const parseModern = (value: string): RGBA | null => {
        const m = /^ok(lab|lch)\(([^)]+)\)$/i.exec(value.trim())
        if (!m) return null
        const kind = m[1].toLowerCase()
        const [coords, alphaPart] = m[2].split('/')
        const n = coords.trim().split(/\s+/)
        if (n.length < 3) return null
        const num = (t: string, ref = 1) =>
          t.endsWith('%') ? (parseFloat(t) / 100) * ref : parseFloat(t)
        const L = num(n[0])
        let A: number, B: number
        if (kind === 'lab') {
          A = num(n[1], 0.4)
          B = num(n[2], 0.4)
        } else {
          const C = num(n[1], 0.4)
          const hRaw = n[2].trim()
          const v = parseFloat(hRaw)
          // `grad` MUST be tested before `rad` — "grad" ends with "rad", so the
          // looser test swallows it and reads 277.8grad as 277.8 radians.
          const deg = /grad$/i.test(hRaw) ? v * 0.9
            : /rad$/i.test(hRaw) ? (v * 180) / Math.PI
            : /turn$/i.test(hRaw) ? v * 360
            : v                                  // bare number or `deg`
          const h = (deg * Math.PI) / 180
          A = C * Math.cos(h)
          B = C * Math.sin(h)
        }
        const alpha = alphaPart === undefined || alphaPart.trim() === '' || alphaPart.trim() === 'none'
          ? 1 : num(alphaPart.trim())
        if ([L, A, B, alpha].some((v) => !Number.isFinite(v))) return null
        return oklabToRgb(L, A, B, alpha)
      }

      /**
       * Resolve any CSS colour to RGBA, or null if it cannot be measured.
       *
       * Order matters. The canvas is tried FIRST because it is the browser's own
       * converter: it handles oklab, oklch, lab, color(srgb …) and color(display-p3 …)
       * with correct gamut mapping, so it stays right for syntax this file has never
       * heard of. Read the PIXEL, never the `fillStyle` read-back string — Chrome echoes
       * `oklab(...)` straight back, which is exactly what defeats a string parser.
       *
       * A rejected assignment is a silent NO-OP, not a throw, so it is detected with two
       * sentinels: if the value is genuinely unassignable both probes survive. Two rather
       * than one so a candidate that IS the sentinel colour cannot false-trip.
       */
      const resolve = (value: string): RGBA | null => {
        if (!value || value === 'none' || value === 'transparent') return null
        if (ctx) {
          ctx.fillStyle = '#ff00ff'
          ctx.fillStyle = value
          let assigned = ctx.fillStyle !== '#ff00ff'
          if (!assigned) {
            ctx.fillStyle = '#00ffff'
            ctx.fillStyle = value
            assigned = ctx.fillStyle !== '#00ffff'
          }
          if (assigned) {
            try {
              ctx.clearRect(0, 0, 1, 1)
              ctx.fillRect(0, 0, 1, 1)
              const d = ctx.getImageData(0, 0, 1, 1).data
              return { r: d[0], g: d[1], b: d[2], a: d[3] / 255 }
            } catch { /* fall through to the converter */ }
          }
        }
        return parseModern(value)   // null here => the caller reports `unresolved`
      }

      const lum = ({ r, g, b }: RGBA) => {
        const f = (v: number) => {
          const s = v / 255
          return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4)
        }
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
      }
      const ratio = (x: RGBA, y: RGBA) => {
        const a = lum(x), b = lum(y)
        return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)
      }
      const over = (fg: RGBA, bg: RGBA): RGBA => ({
        r: fg.r * fg.a + bg.r * (1 - fg.a),
        g: fg.g * fg.a + bg.g * (1 - fg.a),
        b: fg.b * fg.a + bg.b * (1 - fg.a),
        a: 1,
      })

      /**
       * The element's effective background, compositing alpha over what sits behind it.
       *
       * A `backgroundColor` that is neither transparent nor resolvable is returned as
       * `unresolved`, NEVER skipped. Skipping deletes that layer from the composite and
       * yields a confident wrong ratio in BOTH directions: worse than reality over a dark
       * page (a false fail) and better than reality over a light one (a false pass — the
       * dangerous direction). Any future syntax then surfaces as "cannot measure" instead.
       */
      const effectiveBg = (
        el: Element,
      ): { colour?: RGBA; gradient?: boolean; unresolved?: string } => {
        const chain: RGBA[] = []
        let node: Element | null = el
        while (node) {
          const cs = getComputedStyle(node)
          if (cs.backgroundImage && cs.backgroundImage !== 'none') return { gradient: true }
          const raw = cs.backgroundColor
          const bg = resolve(raw)
          if (!bg && raw && raw !== 'none' && raw !== 'transparent' && !/^rgba?\(.*0\)$/.test(raw)) {
            return { unresolved: raw }
          }
          if (bg && bg.a > 0) {
            chain.push(bg)
            if (bg.a >= 1) break
          }
          node = node.parentElement
        }
        let base: RGBA = chain.length && chain[chain.length - 1].a >= 1
          ? (chain.pop() as RGBA)
          : { r: 255, g: 255, b: 255, a: 1 }
        for (let i = chain.length - 1; i >= 0; i -= 1) base = over(chain[i], base)
        return { colour: base }
      }
      // …then measureOne(el, state) / measureAll(state) per the bullets below, exposed as
      // window.__protoSweep. An `unresolved` background OR text colour is pushed as a
      // finding with `ratio: null` and a note naming the syntax — it FAILS the test.
    }
    ```

    > **Transitions must be disabled before measuring — this is not optional.** The shadcn `Button` carries `transition-all`, and `Input`/`Select`/`Badge` carry `transition-[color,box-shadow]`. `getComputedStyle` during a running transition returns the **current interpolated value**, which immediately after a mode flip is still the *old* colour. Measured empirically on this template: right after adding `.dark`, a primary button still reported `rgb(0,73,193)`/`rgb(250,250,250)` — the light pair — and only after the transition settled did it report the correct `rgb(59,130,206)`/`rgb(10,10,10)`. A sweep that skips this does not merely flake: it silently measures the **light** colours while believing it is testing dark, so it passes a genuinely broken dark mode. The `addStyleTag` above makes every read instant and deterministic; it changes only timing, never the final computed value. Apply the same treatment after `hover()` — hover fills transition too.

    **The sweep**, bounded deliberately — it targets the failure class that bites, not WCAG conformance:
    - **Elements:** visible text inside `button, a, [role="button"], [data-slot="badge"], td, th, label, h1, h2, h3, h4`.
    - **Measure:** the element's computed `color` against its *effective* background — walk ancestors until a non-transparent `background-color`, compositing any alpha over what is behind it. Fail below **4.5:1**, or **3:1** for text ≥24px or ≥18.66px bold.
    - **Skip:** `opacity: 0`, `visibility: hidden`, `display: none`, zero-size, empty/whitespace text, and any element whose effective background involves a `background-image` or gradient. These are the honest false-positive corners; excluding them keeps the gate trustworthy.
      **This list is closed. An unparseable colour is NOT a skip** — it is an `unresolved` finding that fails the test (see `effectiveBg` above). Adding "unresolvable → skip" here looks like tidying and is the exact bug this block was written to kill: it converts a colour the checker cannot read into a silent pass.
    - **Hover:** for the first ≤10 interactive elements, `hover()` and re-measure **that element's own** text. This is the direct check for a label that passes at rest and fails on hover — on real palettes a primary button can read 4.97:1 at rest and 4.31:1 under `hover:bg-primary/90`.
    - **Icons:** every `svg` inside those elements must resolve its stroke/fill to `currentColor` or to the same computed `color` as its parent — never a divergent literal.
    - **Report:** each failure as `{ selector, color, background, ratio, required, state }` so the generator's retry can locate it — plus, for an unmeasurable colour, `{ …, ratio: null, note: 'unresolved <background|text> colour — checker cannot parse this colour syntax' }` carrying the offending value in `background`/`color`. `ratio: null` is the marker that distinguishes a **checker limitation** from a **contrast miss**: regenerating a surface cannot fix it, so if every finding in a run carries it, the defect is in the sweep or the browser, not in the prototype.
1c. **Append the layout-integrity test — only when `device_targets.breakpoints` holds more than one entry.** Append a third `test()` to the same spec file, guarded so it runs only outside the primary project.

    **Scoped to the primary `route` only, and to non-primary projects only — a deliberate, disclosed bound**, for the same reason the both-modes test is bounded (step 1b): `routes × devices` would multiply the slowest phase, and the layout primitives being checked (the app shell, the table, the form grid) are **shared** across every route, so a missing breakpoint fails on the primary route as readily as on a secondary one. The added cost is **one page load per extra breakpoint**, not one per route per breakpoint. If a future run finds a responsive defect only a secondary route renders, widen this to `routes` then — but widen it knowingly and say so, rather than discovering the bound by accident.

    ```ts
    // Runs in tablet-chrome / mobile-chrome only; the primary project gets the full sweep above.
    test('layout holds at this viewport', async ({ page }, testInfo) => {
      test.skip(testInfo.project.name === '<primary-project>', 'primary viewport is covered by the full sweep')
      await page.goto(ROUTES[0], { waitUntil: 'networkidle' })
      // 1. No horizontal page scroll — the single most common responsive failure.
      const overflow = await page.evaluate(() => {
        const d = document.documentElement
        return { scrollWidth: d.scrollWidth, clientWidth: d.clientWidth }
      })
      expect(overflow.scrollWidth,
        `no horizontal page scroll (${overflow.scrollWidth} > ${overflow.clientWidth})`)
        .toBeLessThanOrEqual(overflow.clientWidth + 1)
      // 2. The chrome and the primary action survive the narrowing.
      await expect(page.getByTestId('proto-chrome')).toBeVisible()
      const cta = page.getByTestId('primary-cta')
      if (await cta.count()) await expect(cta.first()).toBeVisible()
      // 3. Touch-target floor — only when device_targets.touch is true.
      const small = await page.evaluate(() => {
        const sel = 'button, a, [role="button"], input, select, [role="tab"]'
        return [...document.querySelectorAll(sel)]
          .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 })
          .filter(el => { const r = el.getBoundingClientRect(); return r.width < 44 || r.height < 44 })
          .slice(0, 10)
          .map(el => ({ tag: el.tagName, text: (el.textContent ?? '').trim().slice(0, 30) }))
      })
      expect(small, `touch targets below 44x44: ${JSON.stringify(small)}`).toHaveLength(0)
    })
    ```

    Emit assertion 3 **only** when `device_targets.touch === true` (`design-system-standards.md §4`); on a non-touch target the 24×24 baseline already applies and is the `ux-baseline-checklist.md` floor's business, not this test's. Substitute the real project name for `<primary-project>`.

    **A horizontal-overflow failure is a real defect, not a flake.** The last real generated prototype authored zero breakpoints and put `overflow-x-auto` on a desktop table — exactly what `GR-18` forbids — and no gate saw it because `tablet-chrome` was declared in the config and never invoked.
2. **lint.** `npm run lint` in `app_dir`. Non-zero exit → return `structured-fail {phase:"lint"}` (excerpt the first error block).
3. **typecheck.** `npx tsc --noEmit` in `app_dir`. Non-zero → `structured-fail {phase:"typecheck"}`.
4. **smoke** (unless disabled by the caller for the `RF-11 skip` path). Run, in `app_dir` (the config's `webServer` auto-starts `npm run dev`). The **primary** project comes from `device_targets.primary`; extra `--project` flags are added, one per non-primary breakpoint, in the same invocation so the dev server starts once:
    - single-mode, desktop-only: `npx playwright test e2e/<name_slug>.smoke.spec.ts --project=desktop-chrome` — **unchanged**.
    - two modes, desktop-only: `npx playwright test e2e/<name_slug>.smoke.spec.ts e2e/theme-modes.smoke.spec.ts --project=desktop-chrome`.
    - with extra breakpoints, e.g. `breakpoints: ["mobile","tablet","desktop"]`, `primary: "desktop"`: append `--project=tablet-chrome --project=mobile-chrome`. The per-route sweep and the both-modes test are guarded to the primary project (steps 1/1b are written to run everywhere, so add the same `test.skip(testInfo.project.name !== '<primary-project>')` guard to both when more than one project runs); the layout-integrity test from 1c is guarded to the non-primary ones. Net effect: `routes` page loads at the primary viewport plus **one** page load per extra breakpoint.
    - `e2e/theme-modes.smoke.spec.ts` (scaffold-owned) is likewise primary-project-only — it proves an app-level mechanism and a static token audit, neither of which varies by viewport.
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
- **Device projects match `device_targets.breakpoints` exactly** — one `--project` per breakpoint, primary first; the layout-integrity test was appended **iff** more than one breakpoint is listed, is guarded to the non-primary projects, carries the touch-target assertion **iff** `touch === true`, and states its primary-route-only bound in its own comment. A desktop-only prototype pays nothing: one project, no third test, command byte-identical to the pre-device behaviour.
- A missing-browser condition returns `RF-11 trigger`, never a `structured-fail {phase:"smoke"}` (the two are different recoveries).
- The `colour_mode.sets` branch was evaluated in exactly **one** place, and the single-mode path — spec content and Playwright command — is byte-identical to the pre-colour-mode behaviour. Single-mode runs pay nothing.
- When two modes are live: the both-modes test was appended (not replacing the base test), `e2e/theme-modes.smoke.spec.ts` was included in the run, and a contrast failure surfaced as `structured-fail {phase:"smoke"}` naming the selector and ratio.
- **The `INSTALL_SWEEP` block was authored verbatim**: `resolve()` tries the canvas **first** and reads the pixel (never the `fillStyle` read-back string), detects a rejected assignment with the two-sentinel probe, falls back to `parseModern` (with `rad`/`turn`/`grad` hue units handled), and returns null only when both paths fail. `effectiveBg()` returns `unresolved` for a non-transparent colour it cannot resolve, and that finding fails the test. Confirm by reading the generated spec, not by assuming: this pair has been silently re-derived wrong before.

## Anti-patterns
- **Do not collapse the per-route loop back to a single route, and do not sample a subset of `routes`.** That is the exact hole a real run shipped through: a hydration mismatch and three toggle-less shells, all on secondary routes, all invisible because only `/<name_slug>` was ever visited. If a route is genuinely unvisitable, say which and why in the returned summary — never drop it silently (`CLAUDE.md`: no silent caps).
- Do not conflate "Playwright browsers not installed" (`RF-11`, a setup pause) with "the smoke assertion failed" (`structured-fail`, a build defect).
- Do not silently skip the smoke — skipping only happens on the explicit `RF-11 skip-smoke-with-warning` path and yields `pass-with-warning`, recorded by the landing-updater.
- Do not delete or overwrite other prototypes' e2e specs; the smoke spec write is additive per `name_slug`.
- Do not "fix" a failing phase here — return the structured fail; remediation (regenerate the surface) is the generator's job, and exhaustion is `RF-12`.
- Do not run the both-modes test when only one token set exists. There is no second palette to exercise, and the sweep would just re-assert the light pass at double cost.
- Do not add a second Playwright *project* for dark. `emulateMedia` flips the mode in-page; a project re-runs the whole suite in a fresh browser to learn the same thing. **This does not extend to viewports** — a viewport genuinely cannot be flipped in-page without re-running layout under a different browser metric, so device breakpoints *are* projects (`tablet-chrome`, `mobile-chrome`). The distinction: colour mode is a media-query the page can be asked to re-evaluate; a viewport is a property of the browser context. Keep the device projects bounded instead (step 1c: primary route only, non-primary projects only).
- **Do not run the full per-route sweep, or the both-modes contrast test, at every device project.** That turns a bounded addition into `routes × devices` and makes the slowest phase the dominant cost of a run. Guard them to the primary project; the extra breakpoints get only the layout-integrity test.
- **Do not skip the extra `--project` flags** when `device_targets.breakpoints` lists more than one entry. A declared-but-never-invoked project is exactly the state `tablet-chrome` sat in before this: present in the config, referenced by nothing, and providing zero coverage while looking like it provided some.
- Do not set the `.dark` class directly from the spec. Drive it through `emulateMedia` so the app's own init script does the work — injecting the class tests the assertion, not the application.
- **Do not measure colour without disabling transitions first.** A mid-transition read returns the previous mode's colour, so the sweep "passes" by measuring light values while nominally in dark. This is the one failure mode that makes the gate actively misleading rather than merely absent. Do not substitute a fixed `waitForTimeout` — durations are token-driven (`--duration-fast` / `--duration-base` / `--duration-slow`, plus `--default-transition-duration` which every bare `transition` utility resolves through) and brand-dependent, so a hardcoded wait is a guess.
- Do not widen the sweep into a general accessibility audit. It is scoped to labels and icons on filled surfaces. If broader coverage is wanted later, add `@axe-core/playwright` deliberately — do not let this grow into it by accident.
- Do not weaken the sweep to make a prototype pass. A contrast miss consumes the generator's retry budget and can reach `RF-12`; that is intended — a prototype with invisible labels should not reach the landing page.
- **Do not treat an unparseable colour as absent.** Dropping an unresolvable layer from the background composite is not a conservative default — it measures the label against an ancestor the element never sat on, which reads *worse* than reality over a dark page and *better* over a light one. The false-pass direction is the dangerous one, and it is silent. A colour the checker cannot read is an `unresolved` finding, never a skip and never a `null` swallowed by the caller.
- **Do not re-derive `resolve()`/`effectiveBg()` from the prose bullets.** Author the literal block. Every hand-rolled version so far has parsed only `rgb()`/`rgba()`/hex, which misses every Tailwind opacity modifier in the app — the states most likely to fail, and the ones `extract-brand-theme.md`'s worst-state rule exists for.
