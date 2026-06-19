import { defineConfig, devices } from '@playwright/test'
import { existsSync } from 'node:fs'

const port = Number(process.env.PLAYWRIGHT_PORT) || 3000

// --- Browser resolution ------------------------------------------------------
// The smoke test only needs *a* Chromium-family browser. To keep a fresh checkout
// working on any machine without Playwright's (often-failing, proxy-sensitive)
// browser download, we resolve one at config-load time, in priority order:
//   1. PLAYWRIGHT_CHROME_PATH — explicit executable for a non-standard install
//      (machine-local; never committed).
//   2. PLAYWRIGHT_CHANNEL     — explicit channel name ('chrome' | 'msedge' | 'chromium').
//   3. Auto-detect a system browser: Google Chrome, then Microsoft Edge, at their
//      standard per-OS install locations.
//   4. Fall back to Playwright's bundled Chromium (needs `npx playwright install
//      chromium`).
// Only when NONE of these yields a launchable browser does the smoke fail — that is
// the genuine "no browser at all" case, surfaced as RF-11. Resolution is synchronous
// (fs.existsSync) because Playwright evaluates this config before launching and cannot
// retry a different channel at launch time.

type BrowserChoice = { channel?: string; executablePath?: string }

const CHROME_PATHS: Record<string, string[]> = {
  win32: [
    `${process.env.PROGRAMFILES ?? 'C:\\Program Files'}\\Google\\Chrome\\Application\\chrome.exe`,
    `${process.env['PROGRAMFILES(X86)'] ?? 'C:\\Program Files (x86)'}\\Google\\Chrome\\Application\\chrome.exe`,
    `${process.env.LOCALAPPDATA ?? ''}\\Google\\Chrome\\Application\\chrome.exe`,
  ],
  darwin: ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
  linux: ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/opt/google/chrome/chrome'],
}

const EDGE_PATHS: Record<string, string[]> = {
  win32: [
    `${process.env['PROGRAMFILES(X86)'] ?? 'C:\\Program Files (x86)'}\\Microsoft\\Edge\\Application\\msedge.exe`,
    `${process.env.PROGRAMFILES ?? 'C:\\Program Files'}\\Microsoft\\Edge\\Application\\msedge.exe`,
  ],
  darwin: ['/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'],
  linux: ['/usr/bin/microsoft-edge', '/usr/bin/microsoft-edge-stable', '/opt/microsoft/msedge/msedge'],
}

function firstExisting(paths: string[]): string | undefined {
  return paths.filter(Boolean).find((p) => existsSync(p))
}

function resolveBrowser(): BrowserChoice {
  const explicitPath = process.env.PLAYWRIGHT_CHROME_PATH
  if (explicitPath) return { executablePath: explicitPath }

  const explicitChannel = process.env.PLAYWRIGHT_CHANNEL
  if (explicitChannel) return { channel: explicitChannel }

  const platform = process.platform
  if (firstExisting(CHROME_PATHS[platform] ?? [])) return { channel: 'chrome' }
  if (firstExisting(EDGE_PATHS[platform] ?? [])) return { channel: 'msedge' }

  // No system browser found — fall back to Playwright's bundled Chromium.
  console.warn(
    "[playwright.config] No system Chrome/Edge found; using Playwright's bundled Chromium. " +
      'If the smoke test reports a missing executable, run `npx playwright install chromium`, ' +
      'or set PLAYWRIGHT_CHANNEL=msedge / PLAYWRIGHT_CHROME_PATH=<path-to-chrome.exe>.',
  )
  return {}
}

const browserChoice = resolveBrowser()

// Explicitly assign `channel` (even when undefined) so it overrides any channel the
// device descriptor carries: undefined channel + an executablePath launches that binary
// directly; undefined channel + no executablePath uses the bundled Chromium.
const browserUse = {
  ...devices['Desktop Chrome'],
  channel: browserChoice.channel,
  ...(browserChoice.executablePath
    ? { launchOptions: { executablePath: browserChoice.executablePath } }
    : {}),
}

export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: `http://localhost:${port}`,
    trace: 'retry-with-trace',
  },
  webServer: {
    command: process.platform === 'win32' ? `set PORT=${port}&& npm run dev` : `PORT=${port} npm run dev`,
    url: `http://localhost:${port}`,
    timeout: 120_000,
    reuseExistingServer: !process.env.CI,
  },
  projects: [
    {
      name: 'desktop-chrome',
      use: {
        ...browserUse,
        viewport: { width: 1280, height: 800 },
      },
    },
    {
      // Desktop Chrome at tablet viewport — tests responsive layout without mobile UA/touch emulation
      name: 'tablet-chrome',
      use: {
        ...browserUse,
        viewport: { width: 768, height: 1024 },
      },
    },
  ],
})
