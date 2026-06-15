import { test, expect } from '@playwright/test'

const ROUTE = '/approval-queue-dense'

test('prototype route renders, is clickable, no console errors', async ({ page }) => {
  const errors: string[] = []
  page.on('console', (m) => {
    if (m.type() === 'error') errors.push(m.text())
  })
  page.on('pageerror', (e) => errors.push(String(e)))

  const resp = await page.goto(ROUTE, { waitUntil: 'networkidle' })
  expect(resp?.status() ?? 200, 'route responds < 400').toBeLessThan(400)

  await expect(page.getByTestId('proto-chrome'), 'prototype chrome present (PI-05/PI-08)').toBeVisible()

  const cta = page.getByTestId('primary-cta')
  if (await cta.count()) {
    await expect(cta.first()).toBeEnabled()
    await cta.first().click()
  }

  expect(errors, `no console/page errors: ${errors.join(' | ')}`).toHaveLength(0)
})
