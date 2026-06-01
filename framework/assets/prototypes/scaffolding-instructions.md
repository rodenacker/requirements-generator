# Prototype app scaffolding instructions (`scaffolding-instructions.md`)

**Role:** asset (prototype-private).

**Purpose:** The exact, deterministic recipe for turning the pristine `template/` Next.js app into the shared `prototypes/` app **once**. Consumed by `framework/skills/scaffold-prototype-app.md` (pure mechanics) and `framework/agents/prototype-app-scaffolder.md` (orchestrates copy + brand + shell + verify). After a successful scaffold, `prototypes/.scaffold.json` records it and **every later `/prototype` run skips scaffolding**.

**Design intent:** `prototypes/` is a one-time copy of `template/`. The copy is brand-neutral plumbing + a clean slate (shell, chrome, empty landing, no data). The first and subsequent prototype generations add routes, shared components, fixtures, stores, and types **additively**. This amortises the single expensive cost (copy + `npm install`) across all prototypes (rule 13).

---

## 1. Idempotency gate (check before doing anything)

The scaffold is **done** iff ALL hold:
- `prototypes/.scaffold.json` exists and parses;
- `prototypes/package.json` exists;
- `prototypes/node_modules/` exists and is non-empty.

If done → return `already-scaffolded` (no copy, no install, no writes). If partially present (e.g. `.scaffold.json` missing but `prototypes/` exists) → treat as a failed prior scaffold: surface `RF-13` (hard) so the consultant can remove `prototypes/` and retry clean. Never copy *over* a partial tree.

## 2. Copy set

Copy the entire `template/` tree into `prototypes/`, **excluding**:
- `node_modules/` (re-installed in step 5 — never copied or committed)
- `.next/` (build output)
- `.git/` (if present)
- the example scaffolding files: `src/stores/_example-store.ts`, `src/data/fixtures/_example-data.json`, and the `ExampleItem` interface in `src/types/index.ts`.

Everything else copies verbatim: `package.json`, `package-lock.json`, all configs (`next.config.ts`, `tsconfig.json`, `eslint.config.mjs`, `postcss.config.mjs`, `components.json`, `vitest.config.ts`, `vitest.setup.ts`, `playwright.config.ts`, `next-env.d.ts`), `public/`, `src/components/ui/**` (shadcn primitives), `src/components/{atoms,molecules,organisms,templates,domain}/.gitkeep`, `src/lib/utils.ts`, `src/styles/theme.css`, `src/app/globals.css`, `src/app/favicon.ico`, `src/components/ErrorBoundary.tsx`, `src/data/test-fixtures/.gitkeep`.

> Use a copy that honours the exclude list (e.g. robocopy/xcopy on Windows with `/XD node_modules .next .git` and `/XF _example-*`, or an equivalent file-by-file copy). The mechanics live in `scaffold-prototype-app.md`.

## 3. Clean-slate rewrites (so the empty app builds green)

Because the example store/data/type are excluded, three files that referenced them are rewritten to a clean, store-less baseline:

- `src/types/index.ts` → empty module with a top comment: `// Prototype types are added per-generation by prototype-generator (step-03). Shared across prototypes.`
- `src/stores/index.ts` → empty barrel: `export {}` + the same per-generation comment.
- `src/data/seed.ts` → no-op `seedAllStores()` and `resetAllStores()` whose bodies are comment-only stubs (`// stores registered here per-generation`), so they are import-safe before any store exists.

The first generation that creates a real store wires these three files additively (see `shared-component-conventions.md`).

## 4. Brand theme + shell + chrome + landing (authored once)

Before install, the scaffolder:
1. **Brand theme** — calls `framework/skills/extract-brand-theme.md` to (re)write `prototypes/src/styles/theme.css` from the brand source (a `/design-system` tokens → b consultant → c template defaults). Records `brand_source` + token-block sha.
2. **App shell + chrome + landing** — authors the files specified in `framework/assets/prototypes/app-shell-spec.md`: `src/app/layout.tsx` (RootLayout + store seeding + `<PrototypeChrome>`), the chrome organism + its store, `src/data/prototype-registry.ts` (initially empty), and `src/app/page.tsx` (landing, initially "no prototypes yet").
3. Verifies every authored file via `framework/skills/verify-artifact-write.md`.

## 5. Install (once)

Run `npm install` in `prototypes/` (uses the copied `package-lock.json` for a reproducible tree). Node/npm absent or wrong major → `RF-10`. Install failure → `RF-13`.

## 6. Build smoke (scaffold acceptance)

Run `npm run build` (or `tsc --noEmit` + `next build`) in `prototypes/`. The empty app (shell + chrome + empty landing, no routes, no stores) **must build green**. Failure → fix the clean-slate rewrites and retry once; second failure → `RF-13`.

## 7. Write `.scaffold.json`

```json
{
  "scaffolded_at": "<ISO-8601>",
  "template_copied_from": "template/",
  "brand_source": "design-system | consultant-url | consultant-tokens | template-defaults",
  "brand_token_sha256": "<sha of the theme.css token block at scaffold time>",
  "node_version": "<major.minor.patch captured at install>",
  "app_ok": true
}
```

Verify via `verify-artifact-write.md`. `brand_token_sha256` lets later runs detect `/design-system` drift (a non-blocking notice; never auto-re-themes mid-set — see `prototype-orch.md` Step F1).

---

## Self-validation
- `.scaffold.json` exists and `app_ok: true`; `prototypes/package.json` + non-empty `node_modules/` present.
- The exclude list was honoured: no `_example-*` files under `prototypes/`; no `node_modules`/`.next`/`.git` copied.
- The empty app builds green (step 6 passed).
- `theme.css` token block written from the recorded `brand_source`.
- Every authored file verified via `verify-artifact-write.md`.

## Anti-patterns
- Do not copy `node_modules/` (slow, non-portable, must stay gitignored). Always `npm install`.
- Do not scaffold over a partial `prototypes/` tree — surface `RF-13` instead.
- Do not re-scaffold on later runs — the idempotency gate (§1) must short-circuit.
- Do not author routes or stores here — scaffolding produces only plumbing + clean slate + shell/chrome/empty-landing. Routes/stores/components are the generator's job.
- Do not invent brand tokens here — brand comes from `extract-brand-theme.md` (source a→b→c).
