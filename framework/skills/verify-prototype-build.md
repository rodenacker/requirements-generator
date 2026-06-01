# verify-prototype-build.md

**Purpose:** The `/prototype` **verify gate** (orchestrator Step F3, invoked by `prototype-generator`). Runs, in order, `lint` → `tsc --noEmit` → `next build` → a **Playwright smoke** against the generated route, and returns a structured verdict. The smoke is what makes "hi-fi clickable" (rule 13) a checked guarantee rather than a hope. On any failure the caller (the generator driver) does a bounded retry of the offending surface; exhaustion routes to `RF-12`.

**Caller-agnostic; today's caller is `prototype-generator.md` (step-06).**

## Inputs

- `app_dir` — `"prototypes/"`. Required.
- `name_slug` — the prototype's route segment. Required.
- `route` — `"/<name_slug>"`. Required.

## Outputs

Exactly one of:
- **`pass`** — all four phases passed.
- **`pass-with-warning`** — `lint`+`tsc`+`build` passed and the smoke was **skipped** per the consultant's `RF-11 skip-smoke-with-warning` choice. Carries `{ smoke_skipped: true }`.
- **`RF-11 trigger`** — the smoke could not run because Playwright browsers are not installed. The orchestrator surfaces `RF-11` (`{install-and-retry, skip-smoke-with-warning, abort}`); `skip-smoke-with-warning` re-invokes this skill with smoke disabled → `pass-with-warning`.
- **structured-fail** — `{ "phase": "lint"|"typecheck"|"build"|"smoke", "summary": "<≤300-char error excerpt>" }`. The generator retries the offending surface (≤2); persistent failure → the generator/orchestrator surfaces `RF-12` (hard).

## Procedure

1. **Author the smoke spec (idempotent).** Ensure `<app_dir>e2e/<name_slug>.smoke.spec.ts` exists; (re)write it from this generic template (parametrised by `route`):
    ```ts
    import { test, expect } from '@playwright/test'
    const ROUTE = '<route>'
    test('prototype route renders, is clickable, no console errors', async ({ page }) => {
      const errors: string[] = []
      page.on('console', m => { if (m.type() === 'error') errors.push(m.text()) })
      page.on('pageerror', e => errors.push(String(e)))
      const resp = await page.goto(ROUTE, { waitUntil: 'networkidle' })
      expect(resp?.status() ?? 200, 'route responds < 400').toBeLessThan(400)
      await expect(page.getByTestId('proto-chrome'), 'prototype chrome present (PI-05/PI-08)').toBeVisible()
      const cta = page.getByTestId('primary-cta')
      if (await cta.count()) { await expect(cta.first()).toBeEnabled(); await cta.first().click() }
      expect(errors, `no console/page errors: ${errors.join(' | ')}`).toHaveLength(0)
    })
    ```
   This relies on the generator's runtime contract: the shared chrome root carries `data-testid="proto-chrome"`, and each route's primary action carries `data-testid="primary-cta"` (omitted only on surfaces with no primary action; the smoke skips the click then). Authoring is additive — never delete other prototypes' smoke specs.
2. **lint.** `npm run lint` in `app_dir`. Non-zero exit → return `structured-fail {phase:"lint"}` (excerpt the first error block).
3. **typecheck.** `npx tsc --noEmit` in `app_dir`. Non-zero → `structured-fail {phase:"typecheck"}`.
4. **build.** `npm run build` in `app_dir`. Non-zero → `structured-fail {phase:"build"}`.
5. **smoke** (unless disabled by the caller for the `RF-11 skip` path). Run `npx playwright test e2e/<name_slug>.smoke.spec.ts --project=desktop-chrome` in `app_dir` (the config's `webServer` auto-starts `npm run dev`).
    - If the run aborts because **browsers are missing** (error matching `Executable doesn't exist` / `playwright install`) → return `RF-11 trigger` (do not treat as a test failure).
    - Test failure (assertion failed) → `structured-fail {phase:"smoke"}` with the failing assertion message.
    - Pass → continue.
6. **Return** `pass` (or `pass-with-warning` when the smoke was skipped).

## Self-validation
- Phases ran in order; the first failure short-circuits and is returned with its phase + a bounded excerpt.
- The smoke spec exists under `<app_dir>e2e/` and targets `<route>`; other prototypes' smoke specs were not touched.
- A missing-browser condition returns `RF-11 trigger`, never a `structured-fail {phase:"smoke"}` (the two are different recoveries).

## Anti-patterns
- Do not conflate "Playwright browsers not installed" (`RF-11`, a setup pause) with "the smoke assertion failed" (`structured-fail`, a build defect).
- Do not silently skip the smoke — skipping only happens on the explicit `RF-11 skip-smoke-with-warning` path and yields `pass-with-warning`, recorded by the landing-updater.
- Do not delete or overwrite other prototypes' e2e specs; the smoke spec write is additive per `name_slug`.
- Do not "fix" a failing build here — return the structured fail; remediation (regenerate the surface) is the generator's job, and exhaustion is `RF-12`.
