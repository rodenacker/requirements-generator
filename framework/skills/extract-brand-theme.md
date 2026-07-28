# extract-brand-theme.md

**Purpose:** Establish the **single, shared brand theme** for the `prototypes/` app by (re)writing `prototypes/src/styles/theme.css`'s token blocks — the `:root` base set and, when a second genuine token set exists, a `.dark` alternate set. Brand source priority is a→b→c: (a) the `/design-system` output if present, else (b) consultant-supplied brand, else (c) the template's professional defaults (no-op). This runs **once** at scaffold; the resulting theme is uniform across every prototype (resolved decision D1). The mapping is best-effort and validated by the empty-app build smoke — any `theme.css` var the source does not cover keeps the template default, so the app always builds.

It owns **on-colour derivation** (*Contrast & on-colours* below): the label/icon colour for every filled element, computed per mode against the actual fill in every interaction state the shipped primitives use. This is the load-bearing part of colour-mode support — a palette swap without it produces invisible labels.

It additionally performs a **logo + favicon capture** (see *Logo & favicon capture* below): when an ingested Stadium app's `design-signals` asset points at a product logo, that image is copied into the shared app as a static brand asset — the same once-at-scaffold, uniform-across-prototypes lifecycle as the theme tokens. This is the only brand asset outside `theme.css`; it is a decorative image, never a posture/UX parameter.

**Caller-agnostic; today's caller is `prototype-app-scaffolder.md`.** A future "re-theme all prototypes" action may reuse it.

## Inputs

- `app_dir` — repo-relative prototype app root. Required (`"prototypes/"`). Target file is `<app_dir>/src/styles/theme.css`.
- `design_system_dir` — repo-relative directory holding `/design-system` output. Optional; default `"design-system/"`. **All present mode files are read, not just the first.** Glob `design-system-light.html` and `design-system-dark.html` (plus the legacy unsuffixed `design-system.html`) and key each parsed token set by its own `meta.mode` — **never by filename**. `/design-system` may legitimately have produced only one mode, so a missing light file is not a missing design system. A legacy unsuffixed file carries no `meta.mode`; treat it as `light`.
- `design_system_path` — **deprecated**, accepted for compatibility. When passed explicitly it pins a single file, used as given with no glob and no sibling; the result is necessarily single-mode.
- `colour_mode` — the strategy object resolved by the orchestrator at Step B(4b): `{ strategy: "toggle"|"system"|"none"|"custom", default?: "system"|"light"|"dark", chosen_mode?: "light"|"dark", note?: <string> }`. `chosen_mode` is set only when `strategy == "none"` **and** two sets were available (the consultant picked one). Optional; absent behaves as `{ strategy: "none" }`.
- `consultant_brand` — optional object captured by the agent when source (a) is absent: `{ mode: "url" | "tokens", url?: <string>, tokens?: { <css-var>: <value> } }`. `null` if the consultant chose template defaults.
- `logo_search_glob` — optional; default `"input/*.stadium-assets/*.stadium.design-signals.md"`. Where to look for an ingested Stadium app's `design-signals` asset (which may carry a `logo:` front-matter pointer). Drives *Logo & favicon capture*.

## Outputs

- `{ "source": "design-system" | "consultant-url" | "consultant-tokens" | "template-defaults", "theme_path": "<app_dir>/src/styles/theme.css", "token_sha256": "<sha over BOTH token blocks as written>", "sets": ["light"] | ["dark"] | ["light","dark"], "base": "light" | "dark", "contrast": { "checked": <int>, "adjustments": "<record or 'none'>" }, "brand_logo": { "logo_src": "/brand/<file>", "favicon_file": "src/app/icon.<ext>", "source_app": "<AppName>" } | null }` — returned to the agent, which records these in `.scaffold.json` (drift detection + logo record on later runs). Paths in `brand_logo` are app-relative (`logo_src` is the web path under `public/`; `favicon_file` is relative to `<app_dir>`). `brand_logo` is `null` when no logo was found.
- `sets` names the token sets actually written. It is `["light","dark"]` **only** when two genuine sets were parsed **and** `colour_mode.strategy != "none"`. It is the value the orchestrator, the scaffolder, and `verify-prototype-build.md` branch on.
- `RF-04 trigger` if the theme write fails verification. (Logo/favicon copies are static-asset writes — existence/byte-checked, not `RF-04`-gated; a missing logo is a graceful no-op, never fatal.)

## Source resolution (priority order)

### (a) `/design-system` output — preferred
1. Glob `<design_system_dir>/design-system-light.html`, `<design_system_dir>/design-system-dark.html`, and the legacy `<design_system_dir>/design-system.html`. If none exist → fall through to (b).
2. For **each** file found: extract the `<script type="application/json" id="design-tokens">…</script>` block with one regex; `JSON.parse` it. Key the result by its own `meta.mode` (legacy unsuffixed → `light`). A file whose block is missing or unparseable is skipped with a one-line notice; if that leaves zero sets → fall through to (b).
3. **Choose the base set.** Base = the `light` set when one was parsed, else the `dark` set. (Two sets always include light, so base is light whenever both exist.)
4. **Decide how many sets to write:**
   - Two sets parsed **and** `colour_mode.strategy != "none"` → write `:root` from light and `.dark` from dark. `sets = ["light","dark"]`.
   - Two sets parsed **and** `colour_mode.strategy == "none"` → write only `:root`, from `colour_mode.chosen_mode`. `sets = [chosen_mode]`, `base = chosen_mode`.
   - One set parsed → write only `:root`, from that set. `sets = [<that mode>]`.
5. Map each written set's tokens into its block using the table below — **the same table for both blocks**, no per-mode mapping deltas. The `/design-system` `colours` keys are deliberately the same names as the template's semantic vars, so the colour mapping is direct.
6. Derive that set's on-colours and neutrals per *Contrast & on-colours* below, using **only that set's own tokens** as anchors.

**Never derive a missing mode here.** Cross-mode derivation is `/design-system`'s job (`cross-mode-derivation-rules.md`), where it is gated by a per-mode WCAG check. One set on disk means one set in `theme.css`, full stop.

**Mapping table (design-system token → theme.css `:root` var(s)):**

| design-system token | theme.css var(s) |
|---|---|
| `colours.primary.hex` | `--primary`, `--ring`, `--sidebar-primary`, `--sidebar-ring` |
| `colours.secondary.hex` | `--secondary` |
| `colours.accent.hex` | `--brand-accent` — **not** `--accent`; see the accent note below |
| `colours.background.hex` | `--background`, `--card`, `--popover` |
| `colours.surface.hex` | `--surface`, `--sidebar` |
| `colours.text.hex` | `--foreground`, `--text`, `--card-foreground`, `--popover-foreground`, `--sidebar-foreground` |
| `colours.text_muted.hex` | `--muted-foreground`, `--text-muted` |
| `colours.success.hex` | `--success` |
| `colours.warning.hex` | `--warning` |
| `colours.error.hex` | `--destructive`, `--error` |
| `colours.info.hex` | `--info`, `--chart-3` |
| `typography.body_family.value` | `--font-sans` (in the `@theme` block) |

- **Key names are the design-system's own:** `text_muted` with an **underscore**, and `body_family` — there is no `typography.font-sans` or `font-mono` key in the schema. `--font-mono` keeps the template default (the design-system emits no mono family). `typography.heading_family` is currently unmapped: the template has no `--font-heading` var, and the two families are usually identical anyway.
- **The accent note.** In shadcn, `--accent`/`--accent-foreground` is the **neutral hover/selected surface** pair — it backs `hover:bg-accent` on ghost and outline buttons and badge links, and `focus:bg-accent` on select items. It is *not* a brand accent slot. Putting the brand accent hue there turns every hover into a saturated brand fill and routinely fails contrast (a real extracted palette gives brand-text-on-accent at 1.46:1, and a bright accent gives white-on-accent at 1.74:1). So: `--accent` and `--sidebar-accent` are **derived per mode** as a neutral hover surface — that mode's `surface` shifted ~6–8% toward that mode's `text` — and `--accent-foreground` / `--sidebar-accent-foreground` are that mode's `text`. The brand accent hue lives on `--brand-accent` for deliberate use (callouts, highlights, chart series), never as an interaction surface.
- **`--radius`** and the `effects.*` shadows/transitions are **not** part of the colour contract; keep the template `--radius` default unless the consultant explicitly overrides (radius is brand, not posture — it stays uniform). `--radius` and the `@theme` font vars are **mode-invariant**: they live only in `:root`/`@theme` and are taken from the **base** set. (Safe by construction — the design-system copies all 15 typography tokens across modes verbatim.)
- Any var not covered by the source keeps its current (template) value. Never delete a var **within** a block. (The `.dark` block as a whole is written or omitted per step 4 — that is a block-level decision, not a var deletion.)
- Set `source = "design-system"`.

### (b) consultant-supplied brand — always single-mode
- If `consultant_brand.mode == "tokens"`: apply the provided `{ <css-var>: <value> }` pairs over the `:root` block (only known vars; ignore unknown keys). `source = "consultant-tokens"`.
- If `consultant_brand.mode == "url"`: the agent has already fetched/derived a token set from the URL (reusing the design-system extraction approach is out of scope for this skill — the agent supplies the resulting `tokens` map). Apply as above. `source = "consultant-url"`.
- A consultant brand is one token set, so `sets = ["light"]` (or `["dark"]` if the supplied set is dark by luminance) and **no `.dark` block is written**. Do not pair a consultant-supplied palette with any other dark set — a client-brand light palette beside a generic dark one is worse than no dark mode.
- On-colours are still derived per *Contrast & on-colours* — the single set gets the same treatment.

### (c) template defaults — always single-mode
- If neither (a) nor (b) yields tokens: leave the `:root` colour values as copied from the template (the professional neutral defaults). `source = "template-defaults"`, `sets = ["light"]`, no `.dark` block. This is a valid, intentional outcome — a brandless but coherent prototype.
- Still derive the status on-colours (`--success-foreground` etc.) against the template's own fills, so generated components have correct vars to bind to.

## Contrast & on-colours (per mode, measured)

Runs once **per written token set**, using only that set's own tokens. This is where a palette swap becomes a usable theme.

### The rule

**Measure against the fill; never infer from the mode.** For each filled token, compute the WCAG contrast ratio of near-white (`#FFFFFF`) and of near-black (`#0A0A0A`) against the fill, and take the higher scorer. Do **not** reason "light mode ⇒ white labels" or "dark mode ⇒ black labels" — both shorthands demonstrably fail on real extracted brands (a light-mode brand accent of `#00D6FF` scores 1.74:1 for white and 11.37:1 for black).

### The states to check

A label must clear its threshold against **every** fill state it will ever sit on, not just the resting one. The shipped `ui/` primitives use a fixed, enumerable set of fills; each opacity-modified value composites over **that mode's `background`** before measuring:

| Fill state | Where |
|---|---|
| `primary` solid, `primary/90` | button default + hover; badge default + hover; `selection:bg-primary` |
| `secondary` solid, `secondary/80`, `secondary/90` | button secondary + hover; badge secondary + hover |
| `destructive` solid, `destructive/90`, `destructive/60` | button + badge destructive, hover, and the dark resting fill |
| `accent` solid, `accent/50` | ghost/outline button hover, badge link hover, select item focus |
| `input/30`, `input/50` | outline button + input + select dark fill and hover; tabs active |
| `muted/50` | table row hover |
| `background` | tabs active (light) |

Threshold **4.5:1** (3:1 only for text ≥24px, or ≥18.66px bold — do not apply it to icons or button labels).

### The procedure

1. For each fill token, build its state list from the table. Composite every `token/NN` over that mode's `background`.
2. Score near-white and near-black against **every** state; each candidate's score is its **worst** state.
3. If the better candidate clears the threshold → that is the `-foreground` value. Done.
4. **If neither candidate clears it → nudge the fill.** Preserve hue and saturation; step the fill's lightness (toward the mode's `background` for a dark set, away from it for a light set) in 2% increments, re-scoring after each step, until the better candidate clears 4.5:1 across all states. Cap at 20 steps; if still failing, take the best achieved, and record it as a miss rather than looping. Apply the nudged value to the fill var **and** re-derive its states.
   This is the same operation `contrast-validation.md` already performs inside `/design-system`, applied at a boundary its four-pair gate deliberately does not cover. It is necessary, not optional: a real extracted dark palette produces a primary button where black scores 4.97 at rest but 4.31 on hover, and white scores 3.98 at rest — **neither label colour works**, so the fill itself must move.
5. Record every nudge as `<token>: <before> → <after> (<candidate> was <ratio> on <state>)`.

### Vars produced

| Var | Derivation |
|---|---|
| `--primary-foreground` | on-colour for `primary` |
| `--secondary-foreground` | on-colour for `secondary` |
| `--destructive-foreground`, `--error-foreground` | on-colour for `destructive` |
| `--success-foreground` | on-colour for `success` |
| `--warning-foreground` | on-colour for `warning` |
| `--info-foreground` | on-colour for `info` |
| `--accent-foreground`, `--sidebar-accent-foreground` | that mode's `text` (the accent surface is neutral by construction — see the accent note) |
| `--sidebar-primary-foreground` | same as `--primary-foreground` |
| `--muted` | that mode's `surface` |
| `--border`, `--input`, `--sidebar-border` | that mode's `text_muted` at low alpha composited over that mode's `background` — a visible but low-contrast neutral |

The status on-colours (`--success-foreground`, `--warning-foreground`, `--info-foreground`, `--error-foreground`) exist so a generated status badge has something correct to bind to. Without them a badge reaches for `text-white`, which scores 2.06–2.32 on real dark status fills.

### What is *not* gated here

`text` and `text_muted` against `background` and `surface` — `/design-system` already gates those four pairs per mode and adjusts them. Do not re-adjust them; re-checking and reporting is fine, changing them is not.

## Logo & favicon capture (Stadium brand chrome)

Independent of the token source above (a/b/c) — the logo has one source today: an ingested Stadium app's
`design-signals` asset. Runs after the token block is written.

1. Glob `logo_search_glob`. If none match → `brand_logo = null`; skip (a brandless-logo prototype is a valid outcome).
2. Read only the **YAML front-matter** of each match (sorted lexicographically for determinism). Take the first whose
   `logo:` value is non-null (not the literal `null`). Its `logo:` and `favicon:` values are `embedded/<file>` pointers
   relative to that asset's directory (`input/<AppName>.stadium-assets/`); resolve them to absolute source paths. Capture
   `source_app` from the front-matter `app:` field.
3. If the resolved `logo:` source file exists, copy it to `<app_dir>/public/brand/logo.<ext>` (preserve extension;
   `<ext>` from the source). Set `brand_logo.logo_src = "/brand/logo.<ext>"` (the web path the app shell renders).
4. Favicon: resolve the `favicon:` pointer (defaults to the logo). Copy it to `<app_dir>/src/app/icon.<ext>` using the
   source's real extension — Next.js App Router auto-serves `src/app/icon.{ico,png,jpg,jpeg,svg}` as the favicon, so no
   `layout.tsx` edit is needed (the client-component layout cannot export `metadata`). Set `brand_logo.favicon_file`.
5. These are static-asset copies: confirm each destination exists and is non-empty (a lightweight byte-check, per the
   `CLAUDE.md` compile-covered/asset exemption — **not** `verify-artifact-write.md`, not `RF-04`). A failed copy → treat
   as no logo (`brand_logo = null` for that asset) and continue; never fail the scaffold over brand chrome.

The logo is a **shared, brand-locked** asset (one per app, like the theme — D1). It is rendered as UI-only chrome in the
application shell by the generator (`step-05-compose-route.md`), never in the `PrototypeChrome` review harness (PI-08),
and carries no `data-src`/`data-prop`.

## Write + verify

Target shape of `theme.css`:

```css
@theme { /* unchanged structure — fonts, Tailwind var registration, radius scale */ }

/* Base token set — <mode> — source: <source> */
:root {
  color-scheme: <light|dark>;
  --radius: …;
  …every colour var…
}

/* Alternate dark token set — written only when sets == ["light","dark"] */
.dark {
  color-scheme: dark;
  …the same var names, dark values…
}
```

1. Re-render the `:root` block (and `@theme` font vars if changed) **in place**, preserving the file's structure, comments, and every var name (overwrite values only; never drop a var). Keep the `@theme` mapping block intact.
2. Add `color-scheme` as the first declaration of each block — `light` or `dark` to match that block's set. This is what makes native widgets (scrollbars, **date pickers**, `<select>` popups) render in the right mode; without it a dark theme shows light system chrome.
3. When `sets == ["light","dark"]`, write the `.dark` block immediately after `:root`, defining **exactly the same var names** with the dark set's values. When `sets` has one entry, ensure **no** `.dark` block is present (remove one left by a previous run). The `.dark` block is written or removed **as a whole** — the "never drop a var" rule applies within a block.
4. Compute sha256 over **both blocks as written** (concatenated in file order); `Write` the file; call `framework/skills/verify-artifact-write.md`. On `RF-04 trigger`, surface and return.
5. Return `{ source, theme_path, token_sha256, sets, base, contrast }`.

## Self-validation
- The file still parses as valid CSS and retains every `:root` var the template shipped (none dropped).
- Mapped values are valid colour/length values.
- **Block symmetry:** when a `.dark` block exists, its var-name set is **exactly** equal to `:root`'s — no var in one and not the other. Both blocks are non-empty and each declares `color-scheme`.
- **`.dark` presence matches `sets`:** present iff `sets == ["light","dark"]`. A single-mode run leaves no `.dark` block behind.
- **Contrast matrix:** for every written set, every fill token × every state in the *Contrast & on-colours* table clears its threshold with the chosen `-foreground`, or appears in the recorded `adjustments`. Report `contrast.checked` as the number of (token × state × mode) pairs evaluated. A pair that clears neither candidate nor a nudge is a **FAIL** — surface it, do not silently ship it.
- No `-foreground` var was chosen by mode rather than by measurement (spot-check: the chosen value is the higher-scoring candidate against that token's worst state).
- `--radius` unchanged unless an explicit override was given; `--radius` and the `@theme` font vars appear only once, not duplicated into `.dark`.
- `source` accurately reflects which branch produced the values; `token_sha256` is over both blocks as written.
- `verify-artifact-write` returned `pass` (theme write).
- Logo: when `brand_logo` is non-null, the file at `<app_dir>/public<brand_logo.logo_src>` and the favicon at `<app_dir>/<brand_logo.favicon_file>` both exist and are non-empty, and `logo_src` matches the copied path; when `null`, no brand image was written and the run still succeeded.

## Anti-patterns
- Do not vary the theme per prototype — there is exactly one shared brand (D1). This skill runs once at scaffold.
- Do not introduce posture/UX parameters here — brand is colour/type/radius **plus the logo/favicon image**; layout/workflow divergence lives in the design spec, not here. The logo is a decorative brand asset, not a data element (no `data-src`/`data-prop`).
- Do not delete or rename vars within a block (shadcn + the components depend on them). Overwrite values only; uncovered vars keep template defaults. Adding or removing the `.dark` block as a unit is not a var deletion.
- **Do not resolve the design system by filename precedence.** Read every present mode file and key it by its own `meta.mode`. The old first-existing-wins order (`-light` → `-dark` → legacy) meant a run with both files never opened the dark one, and themed a dark-hue-source brand from its *derived* palette. `meta.primary` is now irrelevant: both palettes are used, each in its own mode.
- **Do not derive a missing colour mode.** That belongs to `/design-system` (`cross-mode-derivation-rules.md`), where it is contrast-gated. One set on disk → one set here.
- **Do not choose an on-colour from the mode.** "Light mode ⇒ white on fills" and "dark mode ⇒ black on fills" both fail on real brands. Measure against the fill.
- **Do not check only the resting fill.** A label that passes at rest and fails on hover is the single most common colour-mode defect. Score every state in the table and take the worst.
- Do not put the brand accent hue on `--accent`. That var is shadcn's neutral hover/selected surface; the brand hue belongs on `--brand-accent`.
- Do not emit a `.dark` block from anything but a genuine second token set — not from a derived palette, not from a framework-shipped generic dark set, not paired with a consultant-supplied light brand.
- Do not fail the run when source (a)/(b) are absent — fall through to template defaults (a valid outcome). Only the theme write-verify failure is fatal (`RF-04`); a missing/uncopyable logo is a graceful `brand_logo = null`.
- Do not guess a logo. The logo comes only from a Stadium `design-signals` `logo:` pointer (recorded by the extractor). No pointer → no logo. Do not scan `embedded/` for arbitrary images here — identification is the extractor's job, done once.
- Do not render or reference the logo in the prototype chrome / review harness — it belongs to the application shell (PI-08). This skill only *captures* the file; the generator renders it.
