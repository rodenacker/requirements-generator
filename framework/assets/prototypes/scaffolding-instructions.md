# Prototype app scaffolding instructions (`scaffolding-instructions.md`)

**Role:** asset (prototype-private).

**Purpose:** The exact, deterministic recipe for turning the pristine `template/` Next.js app into the shared `prototypes/` app **once**. Consumed by `framework/skills/scaffold-prototype-app.md` (pure mechanics) and `framework/agents/prototype-app-scaffolder.md` (orchestrates copy + brand + shell + verify). After a successful scaffold, `prototypes/.scaffold.json` records it and **every later `/prototype` run skips scaffolding**.

**Design intent:** `prototypes/` is a one-time copy of `template/`. The copy is brand-neutral plumbing + a clean slate (shell, chrome, empty landing, no data). The first and subsequent prototype generations add routes, shared components, fixtures, stores, and types **additively**. This amortises the single expensive cost (copy + `npm install`) across all prototypes (rule 13).

---

## 1. Idempotency gate (check before doing anything)

The scaffold is **fully done** iff ALL hold:
- `prototypes/.scaffold.json` exists and parses;
- `prototypes/package.json` exists;
- `prototypes/node_modules/` exists and is non-empty.

If fully done → return `already-scaffolded` (no copy, no install, no writes).

**A valid `prototypes/.scaffold.json` is the discriminator: its presence means the tree is a real scaffold, never a partial one.** Prototype source is **tracked in git** (only `prototypes/node_modules/` + `prototypes/.next/` are ignored). So a checkout that has not yet installed deps — a fresh clone, a second machine, CI, or after clearing `node_modules/` — presents a **valid scaffold that only needs install**: `.scaffold.json` parses **and** `package.json` exists, but `node_modules/` is empty/absent. This is **not** a failed scaffold → return `needs-install` (no copy, no re-author; the calling agent runs `npm install` + build smoke against the already-present source).

A `prototypes/` containing **nothing but `.gitkeep`** (the never-run baseline folder marker) counts as *absent* → proceed to copy (the copy merges into the dir and leaves `.gitkeep` in place).

If real scaffold files are present (e.g. `src/`, `package.json`) **without** a valid `prototypes/.scaffold.json` → treat as a failed prior scaffold: surface `RF-13` (hard) so the consultant can remove `prototypes/` (down to `.gitkeep`) and retry clean. Never copy *over* a partial tree — but a `.gitkeep`-only tree is **not** partial, and a tree with a valid `.scaffold.json` is `needs-install`/`already-scaffolded`, never `RF-13`.

## 2. Copy set

Copy the entire `template/` tree into `prototypes/`, **excluding**:
- `node_modules/` (re-installed in step 5 — never copied or committed)
- `.next/` (build output)
- `.git/` (if present)
- the example scaffolding files: `src/stores/_example-store.ts`, `src/data/fixtures/_example-data.json`, and the `ExampleItem` interface in `src/types/index.ts`.

Everything else copies verbatim: `package.json`, `package-lock.json`, all configs (`next.config.ts`, `tsconfig.json`, `eslint.config.mjs`, `postcss.config.mjs`, `components.json`, `vitest.config.ts`, `vitest.setup.ts`, `playwright.config.ts`, `next-env.d.ts`), `.gitignore`, `public/`, `src/components/ui/**` (shadcn primitives), `src/components/{atoms,molecules,organisms,templates,domain}/.gitkeep`, `src/lib/utils.ts`, `src/styles/theme.css`, `src/app/globals.css`, `src/app/favicon.ico`, `src/components/ErrorBoundary.tsx`, `src/data/test-fixtures/.gitkeep`, and `e2e/craft.smoke.spec.ts`.

Three of those carry the visual-craft contract and are load-bearing, not boilerplate:
- **`src/styles/theme.css`** — the `@theme` scales (type, weights, motion, elevation registration) that `extract-brand-theme.md` then overwrites with brand values.
- **`src/app/globals.css`** — the base layer (heading face, tabular numerals, token-bound scrollbars, selection), the **global press layer** that gives every clickable element its 98% press, the overlay fade + lift + blur-clear entrance, and the `prefers-reduced-motion` collapse. Copying this is what makes tactility structural rather than something eight parallel sub-agents each have to remember.
- **`e2e/craft.smoke.spec.ts`** — proves those invariants at runtime, once per app, brand-independently (`app-shell-spec.md > File map`).

**`playwright.config.ts`** declares three projects — `desktop-chrome` (1280×800), `tablet-chrome` (768×1024), `mobile-chrome` (390×844, `hasTouch`). `verify-prototype-build.md` selects among them from the prototype's `device_targets`. All three spread the same resolved browser choice, so none of them reintroduces the "no launchable browser" class the resolution logic exists to prevent.

> Use a copy that honours the exclude list (e.g. robocopy/xcopy on Windows with `/XD node_modules .next .git` and `/XF _example-*`, or an equivalent file-by-file copy). The mechanics live in `scaffold-prototype-app.md`.

## 3. Clean-slate rewrites (so the empty app builds green)

Because the example store/data/type are excluded, three files that referenced them are rewritten to a clean, store-less baseline:

- `src/types/index.ts` → empty module with a top comment: `// Prototype types are added per-generation by prototype-generator (step-03). Shared across prototypes.`
- `src/stores/index.ts` → empty barrel: `export {}` + the same per-generation comment.
- `src/data/seed.ts` → no-op `seedAllStores()` and `resetAllStores()` whose bodies are comment-only stubs (`// stores registered here per-generation`), so they are import-safe before any store exists.

The first generation that creates a real store wires these three files additively (see `shared-component-conventions.md`).

## 4. Brand theme + shell + chrome + landing (authored once)

Before install, the scaffolder:
1. **Brand theme + logo** — calls `framework/skills/extract-brand-theme.md` to (re)write `prototypes/src/styles/theme.css` from the brand source (a `/design-system` tokens → b consultant → c template defaults). The skill reads **every** present design-system mode file and writes a `:root` base block plus, when two genuine token sets exist and the strategy is not `none`, a `.dark` alternate block; it derives every on-colour per mode by measurement (see that skill's *Contrast & on-colours*). Records `brand_source`, the sha over both blocks, and `sets`/`base`/`contrast`. The same skill also captures the app's product **logo + favicon** when an ingested Stadium `design-signals` asset points at one: `prototypes/public/brand/logo.<ext>` (rendered in the application shell by the generator) and `prototypes/src/app/icon.<ext>` (Next.js file-convention favicon — coexists with the template's `favicon.ico`). Records `brand_logo` (or `null`).
2. **App shell + chrome + landing** — authors the files specified in `framework/assets/prototypes/app-shell-spec.md`: `src/app/layout.tsx` (RootLayout + colour-mode init script + store seeding + `<PrototypeChrome>`), the chrome organism + its store, `src/data/prototype-registry.ts` (initially empty), `src/data/nav/index.ts` (the nav barrel — `NavEntry` + an initially-empty `NAV_BY_PROTOTYPE`; the chrome imports it, so it must exist and typecheck on a zero-prototype app), and `src/app/page.tsx` (landing, initially "no prototypes yet").
3. **Colour-mode files (conditional)** — `src/components/atoms/ThemeToggle.tsx` when `colour_mode.strategy ∈ {toggle, custom}`; `e2e/theme-modes.smoke.spec.ts` when `colour_mode.sets == ["light","dark"]`. Both per `app-shell-spec.md`. Neither is authored otherwise, so a single-mode app carries no dead code.
4. Verifies every authored file via `framework/skills/verify-artifact-write.md`.

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
  "brand_token_sha256": "<sha over BOTH theme.css token blocks at scaffold time>",
  "brand_logo": { "logo_src": "/brand/logo.png", "favicon_file": "src/app/icon.png", "source_app": "<AppName>" },
  "brand_fonts": {
    "families": [
      { "role": "heading", "brand": "<family>", "loadable": "<family-or-null>",
        "param": "<google-family-param-or-null>",
        "status": "google-native | substituted | unverified" },
      { "role": "body", "...": "..." }
    ],
    "links": ["<one Google Fonts stylesheet href per distinct loadable family>"]
  },
  "theme_contract": 2,
  "colour_mode": {
    "strategy": "toggle | system | none | custom",
    "sets": ["light", "dark"],
    "base": "light | dark",
    "default": "system | light | dark",
    "note": "<verbatim consultant freetext — only when strategy == custom>",
    "contrast": { "checked": 0, "adjustments": "<fill nudges applied, or 'none'>" }
  },
  "node_version": "<major.minor.patch captured at install>",
  "app_ok": true
}
```

Verify via `verify-artifact-write.md`. `brand_token_sha256` lets later runs detect `/design-system` drift (a non-blocking notice; never auto-re-themes mid-set — see `prototype-orch.md` Step F1). `brand_logo` is `null` when no Stadium logo pointer was found; when non-null it records the captured logo/favicon so the generator can render the logo in each prototype's application shell.

`brand_fonts` records what `layout.tsx` actually asks the browser to download (`app-shell-spec.md > Brand webfont loading`), so a later run can tell which families were requested without re-parsing `theme.css` — and, crucially, **without re-deriving which name in a stack is fetchable.** On a `design-system` brand source it is `meta.brand_fonts` copied verbatim from the design-system artefact, where `/design-system` already resolved availability (`font-availability-rules.md`); a `substituted` entry means the brand's own typeface is licensed and not on Google Fonts, so `theme.css` names it first and `links` requests the stand-in behind it. On the other three brand sources `families` is derived from the named families in `theme.css` and every `status` is `google-native`.

`links` holds **one URL per family, never a combined `?family=A&family=B` request** — Google returns 200 and silently drops an unrecognised family, so a combined request cannot surface a missing brand font. It is `[]` only when no family's availability could be confirmed, which cannot happen on the `template-defaults` path since that names `Inter`.

**`theme_contract`** is the version of the token contract `theme.css` was written against:

| Value | Means |
|---|---|
| absent or `1` | **legacy, colour-only** — written before the type scale, motion tiers and elevation ladder were mapped. Components in that app have no brand elevation, duration or type step to bind to. |
| `2` | current — colour **plus** `--font-heading`, the 8-step `--text-*` scale with paired line-heights, `--duration-fast/base/slow`, `--ease-standard`, and the four `--elevation-*` per mode block. |

Like the brand and the colour mode, it is written once. A pre-contract-2 app is **not** silently re-themed on a later run (that would change every already-accepted prototype's appearance mid-set, violating D1); it produces a non-blocking **contract-drift** notice at `prototype-orch.md` Step F1, and adopting the new contract means resetting `prototypes/`.

`colour_mode` is the **locked** record of the Step-B(4b) decision, and the discriminator three downstream consumers read:

| Field | Read by | For |
|---|---|---|
| `strategy` | `step-05-compose-route.md` | whether the app shell renders `<ThemeToggle />` |
| `sets` | `verify-prototype-build.md` | whether the smoke exercises both modes |
| `sets` | `prototype-orch.md` Step F1 | the mode-drift notice |
| `theme_contract` | `prototype-orch.md` Step F1 | the contract-drift notice (absent/`< 2` ⇒ legacy colour-only theme) |
| `base`, `contrast` | handback + audit | which set is in `:root`, and any fill nudges applied |

Like the brand, it is written once and never re-authored on a later run. A design-system that later gains a second mode produces a non-blocking drift notice, not a re-theme — adopting it means resetting `prototypes/`.

---

## Self-validation
- `.scaffold.json` exists and `app_ok: true`; `prototypes/package.json` + non-empty `node_modules/` present.
- The exclude list was honoured: no `_example-*` files under `prototypes/`; no `node_modules`/`.next`/`.git` copied.
- The empty app builds green (step 6 passed).
- `theme.css` token block written from the recorded `brand_source`, carrying the **full** contract-2 token set (type scale, motion tiers, elevation ladder) — not colour alone.
- `layout.tsx` carries the brand webfont links; `.scaffold.json` records `brand_fonts` and `theme_contract: 2`.
- Every authored file verified via `verify-artifact-write.md`.

## Anti-patterns
- Do not copy `node_modules/` (slow, non-portable, must stay gitignored). Always `npm install`.
- Do not scaffold over a partial `prototypes/` tree (real files, no valid `.scaffold.json`) — surface `RF-13` instead. A `.gitkeep`-only tree is the never-run baseline, not partial — scaffold into it.
- Do not re-scaffold on later runs — the idempotency gate (§1) must short-circuit.
- Do not author routes or stores here — scaffolding produces only plumbing + clean slate + shell/chrome/empty-landing. Routes/stores/components are the generator's job.
- Do not invent brand tokens here — brand comes from `extract-brand-theme.md` (source a→b→c).
