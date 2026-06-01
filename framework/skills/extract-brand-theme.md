# extract-brand-theme.md

**Purpose:** Establish the **single, shared brand theme** for the `prototypes/` app by (re)writing `prototypes/src/styles/theme.css`'s `:root` token block. Brand source priority is a→b→c: (a) the `/design-system` output if present, else (b) consultant-supplied brand, else (c) the template's professional defaults (no-op). This runs **once** at scaffold; the resulting theme is uniform across every prototype (resolved decision D1). The mapping is best-effort and validated by the empty-app build smoke — any `theme.css` var the source does not cover keeps the template default, so the app always builds.

**Caller-agnostic; today's caller is `prototype-app-scaffolder.md`.** A future "re-theme all prototypes" action may reuse it.

## Inputs

- `app_dir` — repo-relative prototype app root. Required (`"prototypes/"`). Target file is `<app_dir>/src/styles/theme.css`.
- `design_system_path` — repo-relative path to `/design-system` output. Optional; default `"design-system/design-system.html"`.
- `consultant_brand` — optional object captured by the agent when source (a) is absent: `{ mode: "url" | "tokens", url?: <string>, tokens?: { <css-var>: <value> } }`. `null` if the consultant chose template defaults.

## Outputs

- `{ "source": "design-system" | "consultant-url" | "consultant-tokens" | "template-defaults", "theme_path": "<app_dir>/src/styles/theme.css", "token_sha256": "<sha of the rewritten :root block>" }` — returned to the agent, which records `source` + `token_sha256` in `.scaffold.json` (drift detection on later runs).
- `RF-04 trigger` if the write fails verification.

## Source resolution (priority order)

### (a) `/design-system` output — preferred
1. Glob `design_system_path`. If absent → fall through to (b).
2. Read the file; extract the `<script type="application/json" id="design-tokens">…</script>` block with one regex; `JSON.parse` it. Parse failure / missing block → fall through to (b) (record a one-line notice).
3. Map the parsed tokens into `theme.css` `:root` vars (table below). The `/design-system` `colours` keys are deliberately the same names as the template's semantic vars, so the colour mapping is direct.

**Mapping table (design-system token → theme.css `:root` var(s)):**

| design-system token | theme.css var(s) |
|---|---|
| `colours.primary.hex` | `--primary`, `--ring`, `--sidebar-primary`, `--sidebar-ring` |
| `colours.secondary.hex` | `--secondary` |
| `colours.accent.hex` | `--accent`, `--sidebar-accent` |
| `colours.background.hex` | `--background`, `--card`, `--popover` |
| `colours.surface.hex` | `--surface`, `--sidebar` |
| `colours.text.hex` | `--foreground`, `--text`, `--card-foreground`, `--popover-foreground`, `--sidebar-foreground` |
| `colours.text-muted.hex` | `--muted-foreground`, `--text-muted` |
| `colours.success.hex` | `--success` |
| `colours.warning.hex` | `--warning` |
| `colours.error.hex` | `--destructive`, `--error` |
| `colours.info.hex` | `--chart-3` (no dedicated `--info` var in the template) |
| `typography.font-sans` (or family entry) | `--font-sans` (in the `@theme` block) |
| `typography.font-mono` (or family entry) | `--font-mono` |

- **Derived vars:** `--primary-foreground`, `--secondary-foreground`, `--accent-foreground`, `--destructive-foreground` are set to a readable on-colour (near-white or near-black) chosen for ≥4.5:1 contrast against their base (use `colours.background`/`colours.text` as the light/dark anchors). `--border` and `--input` default to a low-contrast neutral derived from `text-muted` unless the source provides one.
- **`--radius`** and the `effects.*` shadows/transitions are **not** part of the colour contract; keep the template `--radius` default unless the consultant explicitly overrides (radius is brand, not posture — it stays uniform).
- Any `:root` var not covered by the source keeps its current (template) value. Never delete a var.
- Set `source = "design-system"`.

### (b) consultant-supplied brand
- If `consultant_brand.mode == "tokens"`: apply the provided `{ <css-var>: <value> }` pairs over the current `:root` (only known vars; ignore unknown keys). `source = "consultant-tokens"`.
- If `consultant_brand.mode == "url"`: the agent has already fetched/derived a token set from the URL (reusing the design-system extraction approach is out of scope for this skill — the agent supplies the resulting `tokens` map). Apply as above. `source = "consultant-url"`.

### (c) template defaults
- If neither (a) nor (b) yields tokens: leave `theme.css` as copied from the template (the professional neutral defaults). `source = "template-defaults"`. This is a valid, intentional outcome — a brandless but coherent prototype.

## Write + verify
1. Re-render the `:root` block (and `@theme` font vars if changed) in place, preserving the file's structure, comments, and every var name (overwrite values only; never drop a var). Keep the `@theme` mapping block intact.
2. Compute sha256 of the rewritten `:root` block; `Write` the file; call `framework/skills/verify-artifact-write.md`. On `RF-04 trigger`, surface and return.
3. Return `{ source, theme_path, token_sha256 }`.

## Self-validation
- The file still parses as valid CSS and retains every `:root` var the template shipped (none dropped).
- Mapped values are valid colour/length values; foreground vars meet ≥4.5:1 against their base where derived.
- `--radius` unchanged unless an explicit override was given.
- `source` accurately reflects which branch produced the values; `token_sha256` is over the final `:root` block.
- `verify-artifact-write` returned `pass`.

## Anti-patterns
- Do not vary the theme per prototype — there is exactly one shared brand (D1). This skill runs once at scaffold.
- Do not introduce posture/UX parameters here — brand is colour/type/radius only; layout/workflow divergence lives in the design spec, not the theme.
- Do not delete or rename `:root` vars (shadcn + the components depend on them). Overwrite values only; uncovered vars keep template defaults.
- Do not fail the run when source (a)/(b) are absent — fall through to template defaults (a valid outcome). Only a write-verify failure is fatal (`RF-04`).
