# stadium/template-model.md — templates as master pages

A Stadium **Template** is a master-page layout. Every **Page** renders *inside* a template, which supplies the shared chrome around the page's own content. Modelling the template once — rather than re-describing the same nav bar and header on every page — keeps the surface inventory honest.

## The shape

- A Template has a `Name`, an `IsDefaultTemplate` flag, an optional **Load** event handler (runs when any page using the template opens), and its own **Control** tree.
- **Most apps have a single `DefaultTemplate`** that every page uses (observed in both sample apps — MemberAdmin and the 18-page Financial Reports both carry exactly one `DefaultTemplate`). Multi-template apps exist but are the exception.
- The template's control tree holds the **shared chrome**: app logo / branding, the **navigation menu** (the `Menu` control or a set of nav buttons), the header, the footer, and any global busy indicator / page-loader.

## `[PageUse(...)]` — the member-page list

In the deployed (generated) source, each template compiles to a controller class carrying a **`[PageUse("PageA","PageB",...)]`** attribute that enumerates the pages rendered through that template. This is the authoritative list of which pages share that shell — read it to bind pages to their chrome, rather than inferring membership.

## Why this matters for extraction & requirements

- **Extract the shell once.** The shared logo / nav / header / footer belong to the *app shell* (system §5 navigation + the `/wireframe` IA), not to each individual surface. Attributing them per-page would inflate every screen with duplicate chrome and obscure what is actually page-specific.
- **Navigation lives in the template + scripts.** The menu structure comes from the template's `Menu`/nav controls; the *edges* between pages come from `NavigateToPage` actions in scripts (see the `navigation` asset). Together they give the app's IA.
- **Page content is the delta.** Once the template is subtracted, what remains on a page (its forms, grids, detail panels) is the real per-surface requirement. The extractor's `surfaces` asset lists pages and templates separately for exactly this reason.
