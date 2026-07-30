# extract-brand-theme.md

**Purpose:** Establish the **single, shared brand theme** for the `prototypes/` app by (re)writing `prototypes/src/styles/theme.css` — the `@theme` scales (type, weights, motion, elevation registration) plus the token blocks: the `:root` base set and, when a second genuine token set exists, a `.dark` alternate set. It carries the **whole** design-system token set, not just colour: the type scale, heading family, durations, easing and elevation ladder are what make a generated prototype look designed rather than default. Brand source priority is a→b→c: (a) the `/design-system` output if present, else (b) consultant-supplied brand, else (c) the template's professional defaults (no-op). This runs **once** at scaffold; the resulting theme is uniform across every prototype (resolved decision D1). The mapping is best-effort and validated by the empty-app build smoke — any `theme.css` var the source does not cover keeps the template default, so the app always builds.

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
- `brand_fonts` is included in the returned object as `{ "families": [...], "links": [...] }`, copied **verbatim** from the design-system's `meta.brand_fonts` (source (a) only). The agent records it in `.scaffold.json` as `brand_fonts`, and `framework/assets/prototypes/app-shell-spec.md > Brand webfont loading` emits `links` as-is. It is `null` when the design-system file predates the field or when the source is (b)/(c)/(d) — see *Brand webfont contract* below.
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
| `typography.body_family.value` | `--font-sans` (in the `@theme` block) — verbatim, including a two-name substituted stack |
| `typography.heading_family.value` | `--font-heading` (in the `@theme` block) — verbatim, including a two-name substituted stack |
| `meta.brand_fonts` | *not a CSS var* — returned to the agent for `.scaffold.json`; consumed by `app-shell-spec.md` to build the `<head>` font links |
| `typography.body_weight.value` | `--brand-body-weight` (in the `@theme` block) |
| `typography.heading_weight.value` | `--brand-heading-weight` (in the `@theme` block) |
| `typography.size_xs … size_4xl` (all 8) | `--text-xs … --text-4xl` (in the `@theme` block) |
| `typography.lh_tight` | `--text-xl--line-height` … `--text-4xl--line-height` (the display sizes) |
| `typography.lh_base` | `--text-xs--line-height` … `--text-lg--line-height` (the body sizes) |
| `typography.lh_loose` | *unmapped by design — see the line-height note* |
| `effects.transition_fast/base/slow` | `--duration-fast` / `--duration-base` / `--duration-slow` (in the `@theme` block) |
| `effects.easing_standard.value` | `--ease-standard` (in the `@theme` block) |
| `effects.shadow_sm/md/lg` | `--elevation-sm` / `--elevation-md` / `--elevation-lg` (**per token block** — see the elevation note) |
| *derived from* `effects.shadow_sm` | `--elevation-xs` — the same geometry at **half alpha** and y-offset `1px` (per block) |

- **Key names are the design-system's own:** `text_muted` with an **underscore**, `body_family`, `heading_family` — there is no `typography.font-sans` or `font-mono` key in the schema. `--font-mono` keeps the template default (the design-system emits no mono family).
- **A family value is copied verbatim, however many names it holds.** `heading_family.value` is normally `'<Family>', <generic>`, but a slot whose brand typeface is licensed and not on Google Fonts arrives as `'<Brand>', '<Loadable>', <generic>` (`'Gotham', 'Montserrat', sans-serif`) — the brand face first, its verified Google-Fonts stand-in behind it, per `framework/agents/design-system-styler/data/font-availability-rules.md` §6.1. Write it into `--font-heading` / `--font-sans` **unchanged**. Do not collapse it to one name, do not reorder it, and do not "clean up" what looks like a redundant fallback: the cascade is what performs the substitution, and a machine that has the licensed face installed renders the real brand font because the brand name is still first.

**Brand webfont contract.** `--font-heading` and `--font-sans` declare a family; they do not fetch one. The fetch is a `<link>` in `layout.tsx`, and **which name to request is not something this skill's consumers may re-derive** — a two-name stack has two candidates and only one of them is fetchable. So:

- **Source (a)** — return `meta.brand_fonts` verbatim. `links` is already built, deduped, and one-family-per-URL; `families[].status` says which slot is `google-native`, `substituted`, or `unverified` (an `unverified` slot is deliberately absent from `links` — its availability could not be confirmed, so nothing is requested for it).
- **Sources (b)/(c)/(d)** — return `brand_fonts: null`. There is no availability record to pass on, so `app-shell-spec.md` falls back to deriving one `family=` segment per named family from the stack, exactly as it did before this field existed. That path is also what a design-system file written before `meta.brand_fonts` existed takes, so older outputs keep working unchanged.
- **Never build the link URLs here.** This skill's job ends at reporting what the design-system decided; `app-shell-spec.md` owns the `<head>` markup.
- **Typography and motion tokens are mode-invariant** — the design-system copies all 15 typography tokens across modes verbatim, and durations/easing carry no colour — so they live in `@theme` only and are taken from the **base** set. Elevation is the one exception (below).
- **Weights do not use Tailwind's `--font-weight-*` namespace.** That namespace emits `font-<name>` utilities, exactly as the `--font-*` family namespace does, so a `--font-weight-heading` would collide with `--font-heading`. The two weights are therefore plain custom properties (`--brand-heading-weight`, `--brand-body-weight`), applied to `body` and `h1–h6` by the template's `globals.css` base layer. Do not "fix" this by moving them into `--font-weight-*`.
- **Line-height mapping is deliberately 2-of-3.** Tailwind pairs a line-height to each size via the real `--text-<size>--line-height` key, so the design-system's 3 line-heights are distributed by role: `lh_base` to the body sizes (`xs`–`lg`), `lh_tight` to the display sizes (`xl`–`4xl`). `lh_loose` has no size to own — it is a prose-block value with no Tailwind size pairing — so it is intentionally unmapped rather than forced onto a size where it would make headings airy. This is the one token in the contract that is knowingly dropped; it is recorded here so the drop is auditable rather than accidental.
- **`--duration-*` is not a Tailwind theme namespace** (verified against `tailwindcss` 4.2.1 — the theme ships `--default-transition-duration`, not a `--duration-*` family). So writing these vars does **not** generate `duration-fast` utilities. Two consequences, both already handled by the template: generated components reach an explicit tier through `duration-[var(--duration-base)]`, and the template additionally binds `--default-transition-duration: var(--duration-fast)` plus `--default-transition-timing-function: var(--ease-standard)`, which are real Tailwind keys — so every bare `transition` / `transition-colors` / `transition-all` already in the shadcn primitives picks up the brand tier with no per-utility change. Write the three `--duration-*` vars; do not attempt to emit `duration-*` utilities.
- **Easing: write `--ease-standard` only.** `--ease-in`, `--ease-out` and `--ease-in-out` are Tailwind defaults consumed by `tw-animate-css` and the shadcn primitives — **never overwrite them**. `--ease-entrance` (the overlay-entrance decelerate curve) is a craft constant owned by the template, not a brand signal; leave it untouched.
- **Elevation is the one mode-varying non-colour token, so it is written per block.** `cross-mode-derivation-rules.md §3.4` derives a dark set's shadows by keeping the light geometry and raising the black alpha ~1.5–2×, so each written set legitimately has its own values. Map each set's own `effects.shadow_*` into that set's block (`:root`, and `.dark` when two sets are written), exactly as the colours are mapped. The template's `@theme` already registers `--shadow-xs/sm/md/lg: var(--elevation-*)`, so `shadow-sm` / `shadow-md` / `shadow-lg` utilities regenerate against the brand ladder — do not write `--shadow-*` directly.
- **Overriding `--text-*` is intended to be retroactive.** Because `--text-*` is a real Tailwind namespace, remapping it means every existing `text-sm` / `text-2xl` in already-generated components follows the brand scale with no code change. Expect the first run after a scale change to shift which text crosses the contrast sweep's large-text threshold (≥24px, or ≥18.66px bold); that is the gate working, not a regression.
- **The accent note.** In shadcn, `--accent`/`--accent-foreground` is the **neutral hover/selected surface** pair — it backs `hover:bg-accent` on ghost and outline buttons and badge links, and `focus:bg-accent` on select items. It is *not* a brand accent slot. Putting the brand accent hue there turns every hover into a saturated brand fill and routinely fails contrast (a real extracted palette gives brand-text-on-accent at 1.46:1, and a bright accent gives white-on-accent at 1.74:1). So: `--accent` and `--sidebar-accent` are **derived per mode** as a neutral hover surface — that mode's `surface` shifted ~6–8% toward that mode's `text` — and `--accent-foreground` / `--sidebar-accent-foreground` are that mode's `text`. The brand accent hue lives on `--brand-accent` for deliberate use (callouts, highlights, chart series), never as an interaction surface.
- **`--radius`** is **not** mapped; keep the template default unless the consultant explicitly overrides (radius is brand, not posture — it stays uniform, and the design-system emits no radius token: `font-rules.md` records border-radius as out of v1 scope). `--radius` and the `@theme` font/type/motion vars are **mode-invariant**: they live only in `:root`/`@theme` and are taken from the **base** set. (Safe by construction — the design-system copies all 15 typography tokens across modes verbatim.) **Elevation is the exception** and is written per block — see the elevation note above.
  > **This bullet used to exclude `effects.*` entirely** ("the `effects.*` shadows/transitions are **not** part of the colour contract"). That was the single largest cause of flat, unpolished prototypes: `/design-system` extracted 3 shadows, 3 durations and an easing curve, rendered them for consultant review, and this skill then discarded all 7 — along with 11 of the 15 typography tokens — so a generated component had no elevation, duration, easing or type scale to bind to and *could not* be polished. The contract is no longer colour-only; it is the **whole token set the design-system emits**, minus `lh_loose` (noted above) and radius (no source token). Do not re-narrow it.
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

A label must clear its threshold against **every** fill state it will ever sit on, not just the resting one. The shipped `ui/` primitives use a fixed, enumerable set of fills; each opacity-modified value composites over **that mode's `background`** before measuring.

**The `Modes` column is normative, not annotation.** A state whose utility carries a `dark:` prefix never renders in a light set, and scoring it there produces a bogus failure — measured: the light template's `destructive/60` reports 3.01:1 for a fill that light mode never paints. Read `Modes` before scoring, and skip any state the set being written does not paint. This column is the canonical source for that applicability; the static token-pair audit in `framework/assets/prototypes/app-shell-spec.md` derives its state list from it rather than re-deciding.

| Fill state | Modes | Where |
|---|---|---|
| `primary` solid, `primary/90` | both | button default + hover; badge default + hover; `selection:bg-primary` |
| `secondary` solid, `secondary/80`, `secondary/90` | both | button secondary + hover; badge secondary + hover |
| `destructive` solid, `destructive/90` | both | button + badge destructive, and hover |
| `destructive/60` | **dark** | `dark:bg-destructive/60` — the dark resting fill on button + badge |
| `accent` solid | both | ghost/outline button hover, badge link hover, select item focus |
| `accent/50` | **dark** | `dark:hover:bg-accent/50` — ghost button hover |
| `input/30`, `input/50` | **dark** | `dark:bg-input/30` + `dark:hover:bg-input/50` — outline button, input, checkbox, select, tabs active |
| `muted/50` | both | table row hover + footer |
| `background` | **light** | tabs active — `data-[state=active]:bg-background` is unprefixed but `dark:` overrides it with `input/30`, so it only ever paints in a light set |

Every `Modes` value above was read off the shipped `ui/` primitives (`bg-input` → `button.tsx:28`, `checkbox.tsx:20`, `input.tsx:11`, `select.tsx:40`, `tabs.tsx:69`; `accent/50` → `button.tsx:32`; `muted/50` → `table.tsx:52,70`), not inferred from the state's name. Re-read them if a primitive changes.

Threshold **4.5:1** (3:1 only for text ≥24px, or ≥18.66px bold — do not apply it to icons or button labels).

### The procedure

1. For each fill token, build its state list from the table, **filtered by the `Modes` column to the set being written** — a `dark`-only state is not scored in a light set and vice versa. Composite every `token/NN` over that mode's `background`.
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
@theme {
  /* unchanged structure — Tailwind colour-var registration, radius scale,
   * --shadow-* → var(--elevation-*) registration, --ease-entrance.
   * MAPPED here from the base set (mode-invariant):
   *   --font-sans, --font-heading, --brand-body-weight, --brand-heading-weight
   *   --text-xs … --text-4xl  (+ their --text-*--line-height pairs)
   *   --duration-fast/base/slow, --ease-standard
   * NEVER touched here: --ease-in / --ease-out / --ease-in-out (Tailwind
   * defaults used by tw-animate-css + the primitives), --radius, --font-mono. */
}

/* Base token set — <mode> — source: <source> */
:root {
  color-scheme: <light|dark>;
  --radius: …;
  …every colour var…
  --elevation-xs: …;  /* derived from this set's shadow_sm at half alpha */
  --elevation-sm: …;  /* this set's effects.shadow_sm */
  --elevation-md: …;  /* this set's effects.shadow_md */
  --elevation-lg: …;  /* this set's effects.shadow_lg */
}

/* Alternate dark token set — written only when sets == ["light","dark"] */
.dark {
  color-scheme: dark;
  …the same var names, dark values (including this set's own --elevation-*)…
}
```

1. Re-render the `:root` block (and the `@theme` font / type-scale / motion vars) **in place**, preserving the file's structure, comments, and every var name (overwrite values only; never drop a var). Keep the `@theme` registration lines (`--color-*`, `--shadow-*`, radius scale) intact.
2. Add `color-scheme` as the first declaration of each block — `light` or `dark` to match that block's set. This is what makes native widgets (scrollbars, **date pickers**, `<select>` popups) render in the right mode; without it a dark theme shows light system chrome.
3. When `sets == ["light","dark"]`, write the `.dark` block immediately after `:root`, defining **exactly the same var names** with the dark set's values. When `sets` has one entry, ensure **no** `.dark` block is present (remove one left by a previous run). The `.dark` block is written or removed **as a whole** — the "never drop a var" rule applies within a block.
4. Compute sha256 over **both blocks as written** (concatenated in file order); `Write` the file; call `framework/skills/verify-artifact-write.md`. On `RF-04 trigger`, surface and return.
5. Return `{ source, theme_path, token_sha256, sets, base, contrast }`.

## Self-validation
- The file still parses as valid CSS and retains every `:root` var the template shipped (none dropped).
- Mapped values are valid colour/length values.
- **Block symmetry:** when a `.dark` block exists, its var-name set is **exactly** equal to `:root`'s — no var in one and not the other, **including all four `--elevation-*` vars**. Both blocks are non-empty and each declares `color-scheme`.
- **Non-colour tokens landed:** `--font-heading`, `--brand-heading-weight`, `--brand-body-weight`, all 8 `--text-*` (each with its `--text-*--line-height` pair), `--duration-fast/base/slow` and `--ease-standard` are present in `@theme` with values from the base set; all four `--elevation-*` are present in **every** written block. A design-system source that produced `effects.*` or `typography.size_*` and left any of these at the template default is a **mapping miss** — surface it, do not ship silently.
- **Tailwind defaults untouched:** `--ease-in`, `--ease-out`, `--ease-in-out`, `--ease-entrance`, `--font-mono` and `--radius` still hold their template values; no `--font-weight-*` var was written (it would collide with `--font-heading`); no `--shadow-*` var was written directly (they are registrations pointing at `--elevation-*`).
- **`.dark` presence matches `sets`:** present iff `sets == ["light","dark"]`. A single-mode run leaves no `.dark` block behind.
- **Contrast matrix:** for every written set, every fill token × every state in the *Contrast & on-colours* table clears its threshold with the chosen `-foreground`, or appears in the recorded `adjustments`. Report `contrast.checked` as the number of (token × state × mode) pairs evaluated. A pair that clears neither candidate nor a nudge is a **FAIL** — surface it, do not silently ship it.
- No `-foreground` var was chosen by mode rather than by measurement (spot-check: the chosen value is the higher-scoring candidate against that token's worst state).
- `--radius` unchanged unless an explicit override was given; `--radius` and the `@theme` font vars appear only once, not duplicated into `.dark`.
- `source` accurately reflects which branch produced the values; `token_sha256` is over both blocks as written.
- `verify-artifact-write` returned `pass` (theme write).
- Logo: when `brand_logo` is non-null, the file at `<app_dir>/public<brand_logo.logo_src>` and the favicon at `<app_dir>/<brand_logo.favicon_file>` both exist and are non-empty, and `logo_src` matches the copied path; when `null`, no brand image was written and the run still succeeded.

## Anti-patterns
- Do not vary the theme per prototype — there is exactly one shared brand (D1). This skill runs once at scaffold.
- Do not introduce posture/UX parameters here — brand is colour/type/motion/elevation/radius **plus the logo/favicon image**; layout/workflow divergence lives in the design spec, not here. The logo is a decorative brand asset, not a data element (no `data-src`/`data-prop`).
- **Do not re-narrow the contract to colour.** Every `effects.*` and `typography.*` token the design-system emits has a target in the mapping table (except `lh_loose`, whose drop is documented). Dropping them again reproduces the flat-prototype defect this mapping exists to fix: a component cannot bind to an elevation, duration or type step that was never written.
- **Do not overwrite `--ease-in` / `--ease-out` / `--ease-in-out`.** They are Tailwind defaults that `tw-animate-css` and the shadcn primitives already animate against; the brand curve goes on `--ease-standard`. Do not touch `--ease-entrance` either — it is the template's overlay-entrance craft constant.
- **Do not write weights into `--font-weight-*`.** That namespace emits `font-<name>` utilities and would collide with `--font-heading`. Use `--brand-heading-weight` / `--brand-body-weight`.
- **Do not write `--shadow-*` directly.** Those are `@theme` registrations pointing at `--elevation-*`; the values belong in the per-mode token blocks, because a dark set raises the shadow alpha.
- **Do not emit `duration-*` utility classes or assume they exist.** `--duration-*` is not a Tailwind namespace; the vars are consumed by raw CSS, by `duration-[var(--duration-base)]`, and via `--default-transition-duration`.
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
