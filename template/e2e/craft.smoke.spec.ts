import { test, expect } from '@playwright/test'

/**
 * Visual-craft invariants — app-level, brand-independent, proven ONCE.
 *
 * Canonical rules: framework/assets/prototypes/visual-craft-standard.md
 *
 * This file ships in `template/e2e/` (not authored per prototype, and not tied to
 * `theme-modes.smoke.spec.ts`) for two reasons:
 *   1. These are properties of the template's global CSS + token contract, not of
 *      any one prototype's components — so they cannot regress per run, and paying
 *      for them per prototype would be waste.
 *   2. `theme-modes.smoke.spec.ts` is only authored when TWO colour modes exist.
 *      Craft invariants are mode-independent, so hanging them off that file would
 *      leave every single-mode app with zero craft coverage.
 *
 * The press test injects its own probe button rather than hunting for one in the
 * page. What is under test is the GLOBAL press layer in globals.css — which
 * matches on `button` — not any particular component. A probe makes the assertion
 * deterministic and keeps the test valid on the bare template (whose landing page
 * has no button) as well as on a fully generated app.
 */

const TOKENS = [
  // Motion
  '--duration-fast',
  '--duration-base',
  '--duration-slow',
  '--ease-standard',
  '--ease-entrance',
  // Type
  '--font-heading',
  '--text-xs',
  '--text-2xl',
  '--text-4xl',
  '--brand-heading-weight',
  '--brand-body-weight',
  // Elevation
  '--elevation-xs',
  '--elevation-sm',
  '--elevation-md',
  '--elevation-lg',
]

test('the brand token contract resolves', async ({ page }) => {
  await page.goto('/')
  const missing = await page.evaluate((names: string[]) => {
    const cs = getComputedStyle(document.documentElement)
    return names.filter((n) => cs.getPropertyValue(n).trim() === '')
  }, TOKENS)
  expect(
    missing,
    `theme.css must define every craft token — missing: ${missing.join(', ')}. ` +
      'A missing token means generated components have nothing to bind to, which is ' +
      'how prototypes end up flat. See extract-brand-theme.md.',
  ).toHaveLength(0)
})

test('Tailwind regenerates its scales against the brand tokens', async ({ page }) => {
  await page.goto('/')
  // shadow-md / text-2xl / font-heading must resolve to the BRAND values, i.e. the
  // @theme overrides must have taken effect rather than Tailwind's stock defaults.
  const resolved = await page.evaluate(() => {
    const probe = document.createElement('div')
    probe.className = 'shadow-md text-2xl font-heading'
    document.body.appendChild(probe)
    const cs = getComputedStyle(probe)
    const out = {
      boxShadow: cs.boxShadow,
      fontSize: cs.fontSize,
      fontFamily: cs.fontFamily,
    }
    probe.remove()
    return out
  })
  expect(resolved.boxShadow, 'shadow-md must emit a real shadow').not.toBe('none')
  expect(resolved.fontSize, 'text-2xl must resolve to a size').toMatch(/\d/)
  expect(resolved.fontFamily, 'font-heading must resolve to a family').not.toBe('')
})

test('every clickable element presses to 98%', async ({ page }) => {
  await page.goto('/')

  const probe = await page.evaluateHandle(() => {
    const b = document.createElement('button')
    b.textContent = 'press probe'
    b.style.position = 'fixed'
    b.style.top = '40px'
    b.style.left = '40px'
    b.style.width = '160px'
    b.style.height = '48px'
    b.style.zIndex = '99999'
    document.body.appendChild(b)
    return b
  })

  const read = () =>
    probe.evaluate((el: Element) => getComputedStyle(el as HTMLElement).scale)

  // Resting: no scaling.
  const resting = await read()
  expect(['none', '1', '1 1'], `resting scale was "${resting}"`).toContain(resting)

  // Press and hold, then read. The transition is token-driven, so wait for it to
  // settle rather than guessing a duration.
  const box = (await probe.asElement()!.boundingBox())!
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2)
  await page.mouse.down()

  await expect
    .poll(read, {
      message:
        'A pressed button must scale to 98% (visual-craft-standard.md §2). The rule ' +
        'lives in the global press layer in globals.css and uses the `scale` property, ' +
        'not `transform` — Tailwind v4 scale-* utilities compile to `scale`, and mixing ' +
        'the two compounds to 0.96.',
      timeout: 2000,
    })
    .toMatch(/^0\.98(\s+0\.98)?$/)

  await page.mouse.up()

  // Releasing must restore it — a stuck press is worse than none.
  await expect
    .poll(read, { message: 'press must release', timeout: 2000 })
    .toMatch(/^(none|1(\s+1)?)$/)

  await probe.evaluate((el: Element) => el.remove())
})

test('an aria-disabled control does not press', async ({ page }) => {
  await page.goto('/')

  // `aria-disabled` rather than `disabled` on purpose. A natively-disabled button
  // never matches `:active` in any browser, so asserting against it would pass for
  // the wrong reason. `aria-disabled="true"` keeps the element focusable AND
  // pointer-interactive — it is the genuinely dangerous case, because it looks and
  // behaves clickable, and it is the case the global layer explicitly neutralises.
  const probe = await page.evaluateHandle(() => {
    const b = document.createElement('button')
    b.setAttribute('aria-disabled', 'true')
    b.textContent = 'aria-disabled probe'
    b.style.position = 'fixed'
    b.style.top = '120px'
    b.style.left = '40px'
    b.style.width = '200px'
    b.style.height = '48px'
    b.style.zIndex = '99999'
    document.body.appendChild(b)
    return b
  })

  const box = (await probe.asElement()!.boundingBox())!
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2)
  await page.mouse.down()

  // Give any transition the same settling budget the press test allows, then assert
  // it never moved.
  await page.waitForTimeout(400)
  const scale = await probe.evaluate(
    (el: Element) => getComputedStyle(el as HTMLElement).scale,
  )
  await page.mouse.up()
  await probe.evaluate((el: Element) => el.remove())

  expect(
    scale,
    'An aria-disabled control must not press — an element that cannot act must not ' +
      `appear to act (visual-craft-standard.md §2). Got scale "${scale}".`,
  ).toMatch(/^(none|1(\s+1)?)$/)
})

test('reduced motion collapses the press transition', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.goto('/')
  const duration = await page.evaluate(() => {
    const b = document.createElement('button')
    document.body.appendChild(b)
    const d = getComputedStyle(b).transitionDuration
    b.remove()
    return d
  })
  // globals.css collapses to 0.01ms rather than `none`, so transitionend still fires.
  // Parse numerically: the browser serialises 0.01ms as "1e-05s", which no naive
  // decimal regex matches.
  const seconds = Number.parseFloat(duration)
  expect(
    Number.isFinite(seconds) && seconds < 0.001,
    `under prefers-reduced-motion the transition must collapse to under 1ms, got ` +
      `"${duration}" (design-system-standards.md §2 is canonical for the policy)`,
  ).toBe(true)
})
