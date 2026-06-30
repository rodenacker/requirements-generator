# stadium/theming-model.md — styling & theming reference

How a Stadium app expresses its visual identity, and the recipe for classifying that identity as **plain**, **themed (kit)**, or **extensively customized**. This feeds `/design-system` — but only via a **manual bridge** (see end).

## What carries styling in a Stadium app

1. **Theme** — the chosen stock theme name on the Application, one of the 11: `Cobalt, Dark, DarkRed, Default, Forest, Grey, Orange, PinkBlue, Purple, Scarlet, Teal`. This is a *signal*, not a stylesheet you read.
2. **Stock theme folders** — `ClientApp/src/assets/themes/<Name>/theme.scss`. **Ignore these.** They are MD5-identical boilerplate across apps (200+ SCSS variables, same in every app). Reading them yields zero app-specific signal; the only thing that matters is *which* theme name the app selected (point 1).
3. **App-level custom StyleSheet** — `Application.StyleSheet` (present iff `Application.IsStyleSheetEnabled`). An inline CSS blob the consultant authored in the Designer. Present in most apps but often minimal.
4. **Per-control style rules** — the design model's `StyleRule` table (key + CSS). The extractor keeps only the non-empty ones.
5. **Custom EmbeddedFiles CSS** — `wwwroot/Content/EmbeddedFiles/CSS/*.css`. **This is the discriminating signal.** It is module CSS and bespoke component CSS the app actually ships.

## Classification recipe (the extractor implements this)

Drive the classification off the **custom EmbeddedFiles CSS set** (`modules.embedded_css`), not the stock themes:

| Custom EmbeddedFiles CSS | Classification |
|---|---|
| empty / absent | **plain / standard** — stock theme, no custom CSS |
| exactly `theming-variables.css` | **built-in theming-kit** — uses [theming-kit](https://github.com/stadium-software/theming-kit); count the *uncommented* CSS custom properties (`grep -cE '^\s*--' theming-variables.css`) for the depth of theming |
| multiple / custom-named CSS | **extensively customized** — bespoke + module component CSS |

Worked examples from the corpus:
- *MemberAdmin* — no custom CSS → **plain / standard** (theme `Default`).
- *Financial Reports* — `collapsible-control-variables.css, page-loader-variables.css, page-loader.css, popup.css` → **extensively customized** (theme `DarkRed`, plus the `collapse-controls`/`page-loader`/`popups` modules).
- One app ships exactly `theming-variables.css` with 46 uncommented vars → **built-in theming-kit**.

## Related CSS modules

- **[theming-kit](https://github.com/stadium-software/theming-kit)** — a layer of CSS custom properties (`--…`) that lets an app re-skin the stock controls without touching the theme folders. Detected by `theming-variables.css`. CSS-only (no `global-scripts.js` entry).
- **[css-utilities](https://github.com/stadium-software/css-utilities)** — Tailwind-like atomic utility classes (spacing, flex, color helpers). CSS-only.

Both are also listed in `module-catalogue.md`; because they carry no JS comment URL, they appear in the styling classification, not in the `modules` (JS) detected list.

## Fonts

Apps bundle a consistent font set under `ClientApp/src/assets/fonts/` — typically Roboto (Light/Regular), Open Sans (regular/semibold), Font Awesome (`fa-*-400/900`), and Glyphicons. This is shared boilerplate; treat a *deviation* from it as the only font signal worth noting.

## The manual bridge to `/design-system`

`/design-system` (the brand-token styler) **cannot read `input/`** — it works from a URL → suggested domain → tokens. So the extracted styling facts reach it **manually**: the consultant reads the per-app `design-signals` asset (theme name, classification, custom CSS list, any extracted brand image under `embedded/`), forms an **informed domain** from it, and supplies that domain to the styler. There is no automatic feed. Everything in `design-signals` is Tier-B / advisory — it biases the design, it does not bind it.
