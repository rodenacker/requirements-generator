<!-- ROLE: asset (template). Populated by `framework/agents/design-system-styler.md` step-06. Final output written to `design-system/design-system.md`. Section order is contractual — do not reorder. -->

---
reference_url: "https://www.digiata.com/"
extraction_date: "2026-05-04"
extraction_status: "success"
domain: "internal financial services productivity tool"
domain_source: "free-text"
css_source_type: "browser-aggregate"
css_source_url: "https://www.digiata.com/"
---

# Design System: internal financial services productivity tool

> Tokens extracted from [https://www.digiata.com/](https://www.digiata.com/). Status colours and any unset tokens are filled from `framework/assets/domain-defaults/internal financial services productivity tool.md` (or per-run inference if free-text is free-text).
>
> Every token below carries a provenance marker — `extracted-from-url` if the value was found in the fetched CSS, `inferred-from-domain` if it came from the `internal financial services productivity tool` defaults. Review before consuming.

---

## Extraction Summary

Human-readable view with source context per token. The machine-readable Brand sections below contain the same values without context.

### Colours

| Token        | Hex       | Source Context              | Provenance              |
| ------------ | --------- | --------------------------- | ----------------------- |
| primary      | `#FF6B01`      | `--color-brand--primary` in :root      | extracted-from-url      |
| secondary    | `#FAB500`    | `--color-brand--secondary` in :root    | extracted-from-url    |
| accent       | `#FF8C3A`       | `--color-brand--primary-light` in :root       | extracted-from-url       |
| background   | `#090909`   | `--bg--primary` in :root (also body background-color)   | extracted-from-url   |
| surface      | `#181818`      | `--color-neutral--dark-grey` in :root      | extracted-from-url      |
| text         | `#FFF9EC`         | `--text--primary` in :root (also body color)         | extracted-from-url         |
| text-muted   | `#A8A8A8`   | `--text--secondary` in :root   | extracted-from-url   |
| success      | `#4ADE80`      | domain-inference (internal financial services productivity tool)      | inferred-from-domain      |
| warning      | `#F59E0B`      | domain-inference (internal financial services productivity tool)      | inferred-from-domain      |
| error        | `#EF4444`        | domain-inference (internal financial services productivity tool)        | inferred-from-domain        |
| info         | `#3B82F6`         | domain-inference (internal financial services productivity tool)         | inferred-from-domain         |

### Typography

| Token              | Value                          | Source Context              | Provenance              |
| ------------------ | ------------------------------ | --------------------------- | ----------------------- |
| heading-family     | Roobert, sans-serif           | `--h1--font-family` in :root | extracted-from-url |
| heading-weight     | 400           | h1 computed font-weight | extracted-from-url |
| body-family        | "Sequel Sans Book Disp", sans-serif              | `--font--primary-family` in :root    | extracted-from-url    |
| body-weight        | 400              | body computed font-weight    | extracted-from-url    |
| text-xs            | 0.75rem                  | `--meta-small--font-size` in :root        | extracted-from-url        |
| text-sm            | 0.875rem                  | `--meta--font-size` in :root        | extracted-from-url        |
| text-base          | 1rem                | `--paragraph--font-size` in :root      | extracted-from-url      |
| text-lg            | 1.125rem                  | `--paragraph-medium--font-size` in :root        | extracted-from-url        |
| text-xl            | 1.25rem                  | domain-inference (internal financial services productivity tool)        | inferred-from-domain        |
| text-2xl           | 1.5rem                 | `--paragraph-large--font-size` in :root       | extracted-from-url       |
| text-3xl           | 2rem                 | `--h3--font-size` in :root       | extracted-from-url       |
| text-4xl           | 3rem                 | `--h2--font-size` in :root       | extracted-from-url       |
| line-height-tight  | 1.2                 | `--h1--line-height` in :root       | extracted-from-url       |
| line-height-base   | 1.5                  | `--paragraph--line-height` in :root        | extracted-from-url        |
| line-height-loose  | 1.75                 | domain-inference (internal financial services productivity tool)       | inferred-from-domain       |

### Effects

| Token              | Value                                 | Source Context           | Provenance               |
| ------------------ | ------------------------------------- | ------------------------ | ------------------------ |
| shadow-sm          | 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(0, 0, 0, 0.1)                       | box-shadow declaration on form/card surfaces   | extracted-from-url     |
| shadow-md          | 4px 4px 0 0 #FF6B01                       | box-shadow declaration with `var(--color-brand--primary)`   | extracted-from-url     |
| shadow-lg          | 0 10px 15px -3px rgba(0, 0, 0, 0.45), 0 4px 6px -2px rgba(0, 0, 0, 0.3)                       | domain-inference (internal financial services productivity tool)   | inferred-from-domain     |
| transition-fast    | 100ms                        | transition shorthand `color 0.1s, box-shadow 0.1s`    | extracted-from-url      |
| transition-base    | 200ms                        | button computed transition-duration `0.2s`    | extracted-from-url      |
| transition-slow    | 300ms                        | transition shorthand `0.3s`    | extracted-from-url      |
| easing-standard    | cubic-bezier(0.23, 1, 0.32, 1)                 | transition shorthand `0.6s cubic-bezier(0.23, 1, 0.32, 1)`      | extracted-from-url        |

### Contrast Validation

WCAG AA validation for the four required text/background pairs (minimum 4.5:1 for normal body text). Auto-adjustment runs against the `text` and `text-muted` tokens until each pair passes; adjustments are listed below.

| Pair                            | Ratio                       | Status              |
| ------------------------------- | --------------------------- | ------------------- |
| text on background              | 19.0:1      | Pass      |
| text on surface                 | 17.1:1 | Pass |
| text-muted on background        | 8.4:1     | Pass     |
| text-muted on surface           | 7.5:1 | Pass |

Adjustments: none

---

## Brand Colours

| Token       | Value             |
| ----------- | ----------------- |
| primary     | #FF6B01      |
| secondary   | #FAB500    |
| accent      | #FF8C3A       |
| background  | #090909   |
| surface     | #181818      |
| text        | #FFF9EC         |
| text-muted  | #A8A8A8   |
| success     | #4ADE80      |
| warning     | #F59E0B      |
| error       | #EF4444        |
| info        | #3B82F6         |

## Brand Typography

### Families

| Role    | Family                    | Weight                    |
| ------- | ------------------------- | ------------------------- |
| Heading | Roobert, sans-serif      | 400      |
| Body    | "Sequel Sans Book Disp", sans-serif         | 400         |

### Sizes

| Token     | Value             |
| --------- | ----------------- |
| text-xs   | 0.75rem     |
| text-sm   | 0.875rem     |
| text-base | 1rem   |
| text-lg   | 1.125rem     |
| text-xl   | 1.25rem     |
| text-2xl  | 1.5rem    |
| text-3xl  | 2rem    |
| text-4xl  | 3rem    |

### Line Heights

| Token              | Value             |
| ------------------ | ----------------- |
| line-height-tight  | 1.2    |
| line-height-base   | 1.5     |
| line-height-loose  | 1.75    |

## Brand Effects

### Shadows

| Token     | Value                |
| --------- | -------------------- |
| shadow-sm | 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(0, 0, 0, 0.1)      |
| shadow-md | 4px 4px 0 0 #FF6B01      |
| shadow-lg | 0 10px 15px -3px rgba(0, 0, 0, 0.45), 0 4px 6px -2px rgba(0, 0, 0, 0.3)      |

### Motion

| Token             | Value                 |
| ----------------- | --------------------- |
| transition-fast   | 100ms        |
| transition-base   | 200ms        |
| transition-slow   | 300ms        |
| easing-standard   | cubic-bezier(0.23, 1, 0.32, 1) |
