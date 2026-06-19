# Setup: Browser for `/prototype` smoke tests

**Referenced by:** `RF-11 playwright_browsers_missing` in `framework/shared/refusal-registry.md`.

**Why:** The `/prototype` verify gate runs a small **Playwright smoke test** (route loads, no console errors, primary CTA clickable) to prove the generated prototype is genuinely clickable (rule 13). `@playwright/test` ships as a dev dependency of the prototype app, and the app's `playwright.config.ts` **auto-detects a Chromium-family browser at config-load time** rather than relying on a downloaded Chromium. On any machine with Google Chrome or Microsoft Edge installed (i.e. essentially every Windows/macOS dev machine), **no separate browser install is needed**.

## Normal case — nothing to install

`prototypes/playwright.config.ts` (copied verbatim from `template/playwright.config.ts`) resolves the browser in this priority order, synchronously, when the config loads:

1. `PLAYWRIGHT_CHROME_PATH` — an explicit executable path (machine-local override; never committed).
2. `PLAYWRIGHT_CHANNEL` — an explicit channel name (`chrome` | `msedge` | `chromium`).
3. **Auto-detect** — Google Chrome, then Microsoft Edge, probed at their standard per-OS install locations (`%PROGRAMFILES%`, `%PROGRAMFILES(X86)%`, `%LOCALAPPDATA%` on Windows; `/Applications` on macOS; `/usr/bin`, `/opt` on Linux).
4. **Bundled Chromium** — if no system browser is found, Playwright's downloaded Chromium (requires `npx playwright install chromium`).

So if Chrome **or** Edge is installed normally, the smoke test runs with zero setup. `RF-11` fires only when **none** of the four resolves to a launchable browser — the genuine "no browser at all" case.

## If `RF-11` fires (no Chrome, no Edge, no bundled Chromium)

Pick whichever fits the machine. Set any env var in the **same terminal that launches Claude Code** so the test process inherits it:

- **Point at a Chrome/Edge in a non-standard location** (auto-detect only probes standard paths):
  ```powershell
  $env:PLAYWRIGHT_CHROME_PATH = "C:\path\to\chrome.exe"
  ```
- **Force a specific channel** (e.g. you have Edge but auto-detect missed it):
  ```powershell
  $env:PLAYWRIGHT_CHANNEL = "msedge"
  ```
- **Download a browser** (only if no Chrome/Edge is present at all — e.g. a headless CI box):
  ```powershell
  cd prototypes
  npx playwright install chromium
  ```
  (If the run reports missing OS dependencies on Linux, also run `npx playwright install-deps`.)

## Verify

```powershell
cd prototypes
npx playwright test --list   # config parses, resolves a browser, lists the smoke projects
```

## Then

Re-invoke `/prototype`. Resumption picks up at the verify step for the prototype you were generating; the smoke test runs against the already-generated route.

## Alternative (no browser at all)

At the `RF-11` prompt you may instead choose **`skip-smoke-with-warning`**: the verify gate then runs `lint` + `tsc --noEmit` only. The prototype is accepted, but its runtime render/click is not proven by the harness — verify it manually with `cd prototypes && npm run dev`.
