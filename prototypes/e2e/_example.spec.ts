import { test, expect } from '@playwright/test'

test.describe('Example E2E Test', () => {
  test('homepage loads successfully', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/prototype/i)
  })
})
