# Setup: Browser for `/prototype` smoke tests

**Referenced by:** `RF-11 playwright_browsers_missing` in `framework/shared/refusal-registry.md`.

**Why:** The `/prototype` verify gate runs a small **Playwright smoke test** (route loads, no console errors, primary CTA clickable) to prove the generated prototype is genuinely clickable (rule 13). `@playwright/test` ships as a dev dependency of the prototype app, and the app's `playwright.config.ts` is configured to drive a **browser already installed on your machine** rather than a downloaded Chromium — so on most machines **no separate browser install is needed**.

## Normal case — nothing to install

`prototypes/playwright.config.ts` (copied verbatim from `template/playwright.config.ts`) sets `channel: 'chrome'`, which Playwright resolves at launch against the standard install locations (`%LOCALAPPDATA%`, `%PROGRAMFILES%`, `%PROGRAMFILES(X86)%` on Windows; OS-standard paths elsewhere). If Google Chrome is installed normally, the smoke test runs with zero setup.

## If `RF-11` fires (no browser found)

Pick whichever fits the machine — each avoids the (often-failing) browser download. Set the env var in the **same terminal that launches Claude Code** so the test process inherits it:

- **Use Edge instead of Chrome** (Edge is preinstalled on Windows 10/11):
  ```powershell
  $env:PLAYWRIGHT_CHANNEL = "msedge"
  ```
- **Chrome in a non-standard location** — point Playwright straight at the executable:
  ```powershell
  $env:PLAYWRIGHT_CHROME_PATH = "C:\path\to\chrome.exe"
  ```
- **Last resort — download a browser** (only if no Chrome/Edge is present at all):
  ```powershell
  cd prototypes
  npx playwright install chromium
  ```
  (If the run reports missing OS dependencies on Linux, also run `npx playwright install-deps`.)

## Verify

```powershell
cd prototypes
npx playwright test --list   # config parses; lists the smoke projects
```

## Then

Re-invoke `/prototype`. Resumption picks up at the verify step for the prototype you were generating; the smoke test runs against the already-generated route.

## Alternative (no browser at all)

At the `RF-11` prompt you may instead choose **`skip-smoke-with-warning`**: the verify gate then runs `lint` + `tsc --noEmit` only. The prototype is accepted, but its runtime render/click is not proven by the harness — verify it manually with `cd prototypes && npm run dev`.
