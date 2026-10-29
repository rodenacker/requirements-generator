# CORS-fallback fixture

Exercises `/design-system` step-04 §4.A.3, which no real reference site has triggered yet.

Run `node framework/tools/__fixtures__/cors-css/serve.cjs` (Ctrl+C to stop):

- `http://localhost:8701/` — the page. It links two stylesheets on the other origin, no `crossorigin`, so both are `corsBlocked` in §4.A.2's evaluate.
- `http://localhost:8702/brand.css` — `--fixture-brand: #12569A` plus a `prefers-color-scheme: dark` block with `--fixture-bg`, no CORS headers.
- `http://localhost:8702/old/brand.css` — `301` to `/brand.css` (the redirect case).

Expected after §4.A.3: one `cors-<k>.css` per distinct sheet, `rawCss` contains `--fixture-brand: #12569A` once, and `{{alt_scheme}}.customProperties` contains `--fixture-bg`.

## Tool behaviour verified 2026-10-29 (Playwright MCP)

- `browser_network_requests({ static: true, filter: "\\.css" })` lists the redirect as two lines: `/old/brand.css => [301]` and `/brand.css => [200]`, each with its own index.
- `browser_network_request({ index, part: "response-body", filename })` returns the CSS. `filename` resolves against the repo root and fails with `ENOENT` if the folder does not exist.
- The 301 line's `response-headers` carry `location: /brand.css`, relative to the href.
