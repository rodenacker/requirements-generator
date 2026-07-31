# scaffold-prototype-app.md

**Purpose:** Deterministically materialise the shared `prototypes/` Next.js app from pristine `template/` — the **copy + clean-slate** mechanics only. This skill performs the idempotency gate, the file copy (honouring the exclude list), and the three clean-slate rewrites so the tree is ready for the calling agent to inject the brand theme + shell and then install. It does **not** author content (brand/shell/landing), run `npm install`, or write `.scaffold.json` — those are owned by `framework/agents/prototype-app-scaffolder.md`, which calls this skill first. The canonical recipe is `framework/assets/prototypes/scaffolding-instructions.md`; this skill implements its §1–§3.

**Caller-agnostic; today's only caller is `prototype-app-scaffolder.md`.**

## Inputs

- `template_dir` — repo-relative source. Required. The agent passes `"template/"`.
- `app_dir` — repo-relative destination. Required. The agent passes `"prototypes/"`.

## Outputs

Exactly one of:
- **`copied`** — `app_dir` did not previously exist as a valid scaffold (it was absent, or contained **only** the committed `.gitkeep` folder marker — the repo's never-run baseline); the tree was copied (exclude list honoured) and the three clean-slate files rewritten. The agent proceeds to brand + shell + install.
- **`already-scaffolded`** — the idempotency gate passed (`.scaffold.json` + `package.json` + non-empty `node_modules/` all present). No tree copy performed. The **primitive top-up** (step 1b) may have added missing `ui/` files; the return names them as `ui_primitives_added[]` (empty when none). The agent skips the rest of the scaffold step.
- **`needs-install`** — a **valid committed scaffold** is present (`.scaffold.json` parses + `package.json` exists) but `node_modules/` is empty/absent (a fresh clone / second machine / CI / cleared deps). No tree copy, no clean-slate, no re-author — the source is already on disk. The **primitive top-up** (step 1b) runs here too, with the same `ui_primitives_added[]` return. The agent runs `npm install` + build smoke against it and returns `scaffolded`.
- **`RF-13 trigger`** — a *partial* `app_dir` was found — real scaffold files (e.g. `src/`, `package.json`) present **without** a valid `.scaffold.json` (a failed prior scaffold). A `.gitkeep`-only tree is **not** partial (it is the never-run baseline → `copied`); a tree **with** a valid `.scaffold.json` is **not** partial either (→ `already-scaffolded`/`needs-install`). The skill does not copy over a genuine partial tree; it surfaces `RF-13` per `framework/shared/refusal-registry.md` so the consultant removes the partial tree (down to `.gitkeep`) and retries clean.

## Procedure

1. **Idempotency gate** (`scaffolding-instructions.md §1`). Glob/Test. When assessing whether `app_dir/` "exists," **ignore the `.gitkeep` folder marker** — the never-run baseline holds only `.gitkeep`, so a `.gitkeep`-only tree counts as *absent*. (`app_dir/` source is tracked in git; only `node_modules/` + `.next/` are ignored.) A **valid `.scaffold.json` is the discriminator** — its presence means a real scaffold, never a partial one:
   - If `app_dir/.scaffold.json` parses **and** `app_dir/package.json` exists:
     - `app_dir/node_modules/` non-empty → return `already-scaffolded`.
     - else (`node_modules/` empty/absent) → return `needs-install` (valid committed scaffold checked out without deps; no copy, no rewrite).
   - Else if `app_dir/` contains real entries (anything other than `.gitkeep`) → return `RF-13 trigger` (partial/failed prior scaffold: real files without a valid `.scaffold.json`; do not copy over it).
   - Else (`app_dir/` absent, or contains only `.gitkeep`) → proceed to copy.
1b. **Primitive top-up — additive, `ui/` only.** On the two no-copy paths (`already-scaffolded`, `needs-install`), and **before** returning:
   - Glob `template_dir/src/components/ui/*.tsx` and `app_dir/src/components/ui/*.tsx`; take the set difference by **basename**.
   - Copy **only** the files present in `template_dir` and absent from `app_dir`. **Never overwrite an existing primitive** — `ui/` is do-not-modify (`shared-component-conventions.md §1`), and a scaffolded app's copy is the one the generated components have been compiling against. A basename that exists in both is left untouched even if the bytes differ.
   - Return the copied basenames as `ui_primitives_added[]` and name them in the status line, so an addition is never silent.

   **Why this step exists.** The scaffold is process-once: on `already-scaffolded` the tree copy is skipped entirely, so a primitive added to `template/` after the first scaffold would **never** reach `prototypes/` — and a generated component importing it would fail `tsc`. That is not hypothetical: `ui/pagination.tsx` was added after `prototypes/` was already scaffolded, and `design-system-standards.md §1 > Tables` now requires it on every data table. The top-up is bounded (one Glob-diff plus N copies of files that by definition do not exist yet) and generalises to every future primitive.

   Scope is **exactly** `src/components/ui/*.tsx`. Do not extend it to `atoms/`, `molecules/`, `organisms/`, `templates/` or `domain/` (generated, accumulating, owned by the generator's partition), nor to config, styles or the data layer — a "top-up" that reached those would silently revert per-run work.
2. **Copy with exclude list** (`§2`). Copy the entire `template_dir` tree into `app_dir`, excluding directories `node_modules/`, `.next/`, `.git/` and files matching `_example-*` (i.e. `src/stores/_example-store.ts`, `src/data/fixtures/_example-data.json`). On Windows use `robocopy "<template_dir>" "<app_dir>" /E /XD node_modules .next .git /XF _example-*` (or an equivalent file-by-file copy). The copy **merges** into the existing `app_dir`, leaving the committed `.gitkeep` in place (`template_dir` has no `.gitkeep`, so nothing is overwritten). Treat a copy failure as fatal → return `RF-13 trigger`.
3. **Clean-slate rewrites** (`§3`) — so the store-less tree builds:
   - `app_dir/src/types/index.ts` → `// Prototype entity types are added per-generation by prototype-generator (step-03). Shared across prototypes.\nexport {}\n`
   - `app_dir/src/stores/index.ts` → the same comment + `export {}\n` (empty barrel).
   - `app_dir/src/data/seed.ts` → import-safe no-ops:
     ```ts
     // Stores are registered here per-generation by prototype-generator (step-03).
     export function seedAllStores(): void { /* no stores yet */ }
     export function resetAllStores(): void { /* no stores yet */ }
     ```
   Verify each rewrite via `framework/skills/verify-artifact-write.md`.
4. **Return** `copied`.

## Self-validation
- On `copied`: no `_example-*` files exist under `app_dir`; no `node_modules`/`.next`/`.git` were copied; the three clean-slate files exist and are import-safe; each was verified.
- On `already-scaffolded`: no writes were performed **other than** the step-1b `ui/` top-up, and every file it wrote was absent beforehand.
- On `needs-install`: no tree copy/rewrite performed; a valid `.scaffold.json` + `package.json` were present and `node_modules/` was empty/absent; the step-1b top-up obeyed the same absent-only rule.
- After step 1b (either path): `app_dir/src/components/ui/` contains every basename in `template_dir/src/components/ui/`; no pre-existing primitive changed size or mtime; `ui_primitives_added[]` names exactly the files written.
- On `RF-13 trigger`: no copy was performed over the partial tree.

## Anti-patterns
- Do not copy `node_modules/` — it is reinstalled by the agent (and is git-ignored).
- Do not run `npm install`, author brand/shell, or write `.scaffold.json` here — those are the agent's steps (after this skill returns `copied`).
- Do not copy over a partial `app_dir` (real scaffold files without a valid `.scaffold.json`) — return `RF-13` so the consultant retries clean. A `.gitkeep`-only `app_dir` is the never-run baseline, **not** partial — copy into it; a tree with a valid `.scaffold.json` but no `node_modules/` is **not** partial either — return `needs-install`, never `RF-13`.
- Do not exclude config files (`package-lock.json`, `next.config.ts`, `tsconfig.json`, `playwright.config.ts`, etc.) — the app needs them verbatim.
- **Do not let the step-1b top-up overwrite anything.** It is set-difference-by-basename, absent-only. Overwriting a primitive would silently change the API that already-generated components compile against, and `ui/` is do-not-modify by contract — a drifted primitive is a consultant-visible problem to raise, not one to fix by clobbering.
- **Do not widen the top-up beyond `src/components/ui/*.tsx`.** Every other component tier accumulates per run and is owned by the generator's `owned_files` partition; topping those up from `template/` would revert generated work.
