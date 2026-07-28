<!-- ROLE: shared (cross-pipeline consultant affordance). Canonical definition of the auto-open-in-browser behaviour and its path allowlist — referenced by path, never restated. Implemented by framework/tools/open-artifact.cjs, wired as a PostToolUse hook in .claude/settings.json. -->

# Artefact preview (auto-open in the default browser)

**Purpose.** Canonical rule for opening a freshly-written HTML artefact in the consultant's default browser **at write time — before the accept gate**, so the artefact is already on screen when the gate appears. Reviewing a wireframe set, a design system, or an analysis no longer requires an alt-tab-and-navigate round trip on every gate; the consultant reads the artefact, then switches back and answers.

## Mechanism — harness-level, not a pipeline step

The behaviour is implemented by a **`PostToolUse` hook** (matcher `Write`) declared in `.claude/settings.json`, which runs `framework/tools/open-artifact.cjs`.

**No orchestrator, agent, or skill invokes it.** There is no skill to call and no `Tools`-section entry to add. It fires on the `Write` itself, which is why it needs no edit at any of the 43 write sites across the six pipelines. Do not add a call site for it, and do not look for one — a second, prompt-level invocation would double-open every artefact.

Because it is a hook it is not permission-gated, so it needs no `permissions.allow` entry and never prompts.

**Activation requires a Claude Code restart.** `.claude/settings.json` hooks are read at process start, so a session that was already running when this affordance was added (or when its allowlist is edited) will **not** fire it — the same session-start caching that makes `RF-01`/`RF-06`/`RF-10` tell the consultant to restart after an install. Verified behaviour: the hook command itself works when invoked directly, and only the harness registration is deferred. `/clear` is **not** sufficient; restart Claude Code.

## Path allowlist (canonical)

Repo-relative, forward-slashed. **Allowlist-only** — anything unmatched is skipped, so there is no deny list to keep in sync.

```
^analyse-requirements/[^/]+/[^/]+\.html$
^analyse-inputs/[^/]+/[^/]+\.html$
^review-requirements/[^/]+/[^/]+\.html$
^review-inputs/[^/]+/[^/]+\.html$
^design-system/design-system-(light|dark)\.html$
^wireframes/[^/]+/index\.html$
```

| Pipeline | Opens | Tabs per run |
|---|---|---|
| `/analyse-requirement` | the methodology artefact | 1 |
| `/analyse-inputs` | the methodology artefact | 1 |
| `/review-requirement` | the methodology artefact | 1 |
| `/review-inputs` | the methodology artefact | 1 |
| `/design-system` | each mode file in `{{files_to_write}}` | 1 or 2 — hue-source first |
| `/wireframe` | `index.html` only | 1 |

**Deliberate exclusions** — each is a decision, not an oversight:

- **`wireframes/<slug>/<variant>/screen-NN-*.html`** — three path segments, so the `wireframes/` pattern cannot match. `index.html` is the comparator's intended entry point (§1 scope details, §2 side-by-side screen-link columns, §3 variant cards, §4 trade-off matrix), and each screen link opens the real wireframe in a new tab on click. Opening the screens up front would be 10–25 tabs per run and would bypass the navigation the comparator exists to provide.
- **`design-system/.workspace/**`** — an extra segment; the transient styler workspace never matches.
- **`design-system/design-system.html`** — legacy unsuffixed artefact, no longer authored (existence-checked and deleted only). Left out rather than resurrected.
- **`prototypes/**`** — `/prototype` produces a Next.js app served by `npm run dev`, not a `file://` artefact. Previewing it needs a dev-server-and-navigate affordance, which is out of scope here.
- **`framework/**`, `template/**`, `input/**`** — templates and inputs are not run outputs.
- **Non-`.html` artefacts** (`*.sidecar.json`, `_drift.json`, `manifest.json`, `variant-position.json`, `scope.json`) and the markdown-artefact pipelines (`/requirements`, `/generate-prd`, `/export-application`, `/resolve-review`) — nothing to open in a browser.

The matcher is **`Write` only**, not `Edit`/`MultiEdit`. Every artefact-producing step in these pipelines writes in a single atomic `Write`; an `Edit` against an artefact is a hand-fix, not a pipeline product, and does not warrant a tab.

## Ordering relative to `verify-artifact-write`

The hook fires on the `Write`, therefore **before** `framework/skills/verify-artifact-write.md` runs. That skill is a read-back predicate, not a mutation, so the bytes opened are the bytes verified — the preview can never show content that differs from what the verify pass checked.

Two bounded consequences:

- A **truncated** write large enough to clear the 512-byte floor opens, and `RF-04` then halts the pipeline. The consultant sees a broken tab followed by the halt line. The tab is noise, never a source of wrong content.
- `verify-artifact-write`'s **silent re-`Write`** would otherwise open a second tab. Suppressed by the content-hash dedupe below.

## Idempotence

The helper records `{ "<relpath>": "<sha256>" }` in `<os-tmpdir>/reqgen-open-<session_id>.json` and skips a re-open when the hash is unchanged.

- Same session, identical bytes → **no** second tab (this is the silent-retry case).
- Same session, different bytes → **opens** (a `Revise` branch re-renders; the consultant needs to see the revision).
- New session → **opens**, even for byte-identical content.

State lives in the OS temp dir, **not** `framework/state/` — that tree is orchestrator/agent-owned with per-file ownership declared in orchestrator `Tools` sections, and a hook writing there would breach that ownership and pollute a tracked directory.

That temp write is **not** a pipeline write: it is made by the harness, not by an agent, and it lands outside the repo. It therefore does not touch any pipeline's stand-alone constraint (e.g. the styler's *"no write to any path outside `design-system/`"*) and needs no entry in the write-isolation exception list in `docs/maintenance.md`.

## Failure semantics — non-fatal, and no `RF-NN`

Every failure path exits 0. A missing file, an unreadable payload, an absent browser association, or a launch error is **silently skipped**; the pipeline proceeds untouched and the consultant opens the artefact manually, exactly as before this affordance existed.

**A failed preview is not a refusal and deliberately has no predicate in `framework/shared/refusal-registry.md`.** That registry's severities are `pause` (halt and offer a bounded choice set) and `hard` (halt and fail handback); a viewer that did not launch warrants neither, and minting an `RF-NN` would give a convenience affordance pipeline-halting semantics. The precedent for a component that surfaces no refusal at all is `framework/skills/render-visual-to-raster.md > Refusal handling`.

Consequently, **consultant-facing prose must never assert that a tab exists.** The correct phrasing names the path as a fallback:

> Opened in your browser — if it didn't open, open `<path>` via `file://`.

## Opt-out

Set `REQGEN_NO_AUTO_OPEN` to any value other than empty / `0` / `false`. The helper exits before doing any work. Set it in `.claude/settings.json > env` to disable the affordance for the workspace, or in the shell environment for one session.

## Platform

- **Windows** — `rundll32.exe url.dll,FileProtocolHandler <file-url>`. Chosen over `cmd /c start "" "<path>"`: no shell, so no quoting or metacharacter hazard, and the path is percent-encoded via `pathToFileURL`.
- **macOS** — `open <path>` · **Linux** — `xdg-open <path>`. Present but untested, consistent with the workspace's Windows/PowerShell-first posture (`framework/tools/setup-environment.ps1` is `#requires -Version 7.0`).

The hook command itself is `cmd /c`, so on a non-Windows host the hook does not fire at all and the pipelines behave exactly as they did before.

## Testing the allowlist

`framework/tools/open-artifact.cjs --dry-run <repo-relative-path> [...]` prints `OPEN <path>` or `SKIP <path> (<reason>)` per argument without touching disk or launching anything. Use this to verify pattern changes rather than triggering real runs.

## Referenced by

`CLAUDE.md` §1 (Constraints), `docs/maintenance.md` (Roles & write isolation; Where new system elements go), `docs/architecture.md`, `framework/dependency-graphs.md`. The allowlist and the failure semantics are defined **here only** (canonical-source rule); callers reference this file, they do not restate it.
