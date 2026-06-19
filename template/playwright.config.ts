import { defineConfig, devices } from '@playwright/test'

const port = Number(process.env.PLAYWRIGHT_PORT) || 3000

// Run the smoke test against a browser already installed on the machine instead of
// Playwright's downloaded Chromium — no `npx playwright install` needed, so a fresh
// checkout on any machine works without the (often-failing) browser download.
// Resolution order:
//   1. PLAYWRIGHT_CHROME_PATH — explicit executable for a non-standard install (machine-local; never committed).
//   2. PLAYWRIGHT_CHANNEL     — channel name; defaults to 'chrome'. Set 'msedge' on a Windows
//                               machine without Chrome (Edge is preinstalled on Windows 10/11).
// Playwright resolves a channel at launch against the standard install roots
// (%LOCALAPPDATA%, %PROGRAMFILES%, %PROGRAMFILES(X86)% on Windows; OS-standard paths elsewhere).
const browserExecutablePath = process.env.PLAYWRIGHT_CHROME_PATH || undefined
const browserChannel = browserExecutablePath ? undefined : process.env.PLAYWRIGHT_CHANNEL || 'chrome'

const browserUse = {
  ...devices['Desktop Chrome'],
  channel: browserChannel,
  ...(browserExecutablePath ? { launchOptions: { executablePath: browserExecutablePath } } : {}),
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
