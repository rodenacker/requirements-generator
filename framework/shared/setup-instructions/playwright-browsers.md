# Setup: Playwright browsers (for `/prototype` smoke tests)

**Referenced by:** `RF-11 playwright_browsers_missing` in `framework/shared/refusal-registry.md`.

**Why:** The `/prototype` verify gate runs a small **Playwright smoke test** (route loads, no console errors, primary CTA clickable) to prove the generated prototype is genuinely clickable (rule 13). `@playwright/test` ships as a dev dependency of the prototype app, but Playwright needs its **browser binaries** installed once on the machine. This is separate from `npm install`.

## Install

From the prototype app directory:
```powershell
cd prototypes
npx playwright install chromium
```

(Installing just `chromium` is enough for the smoke test and is the fastest option. Drop the `chromium` argument to install all browsers.)

If the run reports missing OS dependencies, also run:
```powershell
npx playwright install-deps
```

## Verify

```powershell
cd prototypes
npx playwright --version
npx playwright install --dry-run   # lists installed browsers
```

## Then

Re-invoke `/prototype`. Resumption picks up at the verify step for the prototype you were generating; the smoke test runs against the already-generated route.

## Alternative (no install)

At the `RF-11` prompt you may instead choose **`skip-smoke-with-warning`**: the verify gate then runs `lint` + `tsc --noEmit` + `next build` only. The prototype is accepted, but its runtime render/click is not proven by the harness — verify it manually with `cd prototypes && npm run dev`.
