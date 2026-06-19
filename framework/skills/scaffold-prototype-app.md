# scaffold-prototype-app.md

**Purpose:** Deterministically materialise the shared `prototypes/` Next.js app from pristine `template/` — the **copy + clean-slate** mechanics only. This skill performs the idempotency gate, the file copy (honouring the exclude list), and the three clean-slate rewrites so the tree is ready for the calling agent to inject the brand theme + shell and then install. It does **not** author content (brand/shell/landing), run `npm install`, or write `.scaffold.json` — those are owned by `framework/agents/prototype-app-scaffolder.md`, which calls this skill first. The canonical recipe is `framework/assets/prototypes/scaffolding-instructions.md`; this skill implements its §1–§3.

**Caller-agnostic; today's only caller is `prototype-app-scaffolder.md`.**

## Inputs

- `template_dir` — repo-relative source. Required. The agent passes `"template/"`.
- `app_dir` — repo-relative destination. Required. The agent passes `"prototypes/"`.

## Outputs

Exactly one of:
- **`copied`** — `app_dir` did not previously exist as a valid scaffold (it was absent, or contained **only** the committed `.gitkeep` folder marker — the repo's never-run baseline); the tree was copied (exclude list honoured) and the three clean-slate files rewritten. The agent proceeds to brand + shell + install.
- **`already-scaffolded`** — the idempotency gate passed (`.scaffold.json` + `package.json` + non-empty `node_modules/` all present). No copy performed. The agent skips the entire scaffold step.
- **`RF-13 trigger`** — a *partial* `app_dir` was found — real scaffold files (e.g. `src/`, `package.json`) present **without** a valid `.scaffold.json` (a failed prior scaffold). A `.gitkeep`-only tree is **not** partial — it is the never-run baseline and returns `copied`, not this. The skill does not copy over a genuine partial tree; it surfaces `RF-13` per `framework/shared/refusal-registry.md` so the consultant removes the partial tree (down to `.gitkeep`) and retries clean.

## Procedure

1. **Idempotency gate** (`scaffolding-instructions.md §1`). Glob/Test. When assessing whether `app_dir/` "exists," **ignore the `.gitkeep` folder marker** — the repo commits `app_dir/` as a never-run baseline holding only `.gitkeep` (all generated content is git-ignored), so a `.gitkeep`-only tree counts as *absent*:
   - If `app_dir/.scaffold.json` parses **and** `app_dir/package.json` exists **and** `app_dir/node_modules/` is non-empty → return `already-scaffolded`.
   - Else if `app_dir/` contains real entries (anything other than `.gitkeep`) but the above is not fully satisfied → return `RF-13 trigger` (partial/failed prior scaffold; do not copy over it).
   - Else (`app_dir/` absent, or contains only `.gitkeep`) → proceed to copy.
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
- On `already-scaffolded`: no writes were performed.
- On `RF-13 trigger`: no copy was performed over the partial tree.

## Anti-patterns
- Do not copy `node_modules/` — it is reinstalled by the agent (and is git-ignored).
- Do not run `npm install`, author brand/shell, or write `.scaffold.json` here — those are the agent's steps (after this skill returns `copied`).
- Do not copy over a partial `app_dir` (real scaffold files without a valid `.scaffold.json`) — return `RF-13` so the consultant retries clean. A `.gitkeep`-only `app_dir` is the never-run baseline, **not** partial — copy into it.
- Do not exclude config files (`package-lock.json`, `next.config.ts`, `tsconfig.json`, `playwright.config.ts`, etc.) — the app needs them verbatim.
