# step-05-compose-route

**Goal:** Assemble the **driver-owned** routes under `src/app/<name_slug>/**` and the shared intra-prototype nav, composing shared components into each coupled surface's realization. Standalone secondary surfaces authored their own route in their sub-agent (step-04 / `step-sub-render-surface.md`); the driver only **consumes** their route manifests here. Collision-free with sub-agents (the disjoint `owned_files` partition, step-02).

**Timing:** emit `substep_start` (`stage:"generator"`, `substep:"route-compose"`) before step 1 and `substep_end` after step 6, per `prototype-generator.md > Timing log (sub-steps)`.

For the prototype's surfaces (using the manifests from step-04 + reused components + the `route_map` from step-02):

1. **Who owns which route** (`route_map`, step-02; realization enum in `framework/assets/wireframes/realization-strategies.md`):
   - `standalone-screen` **secondary** (`is_parallelizable`) → **already authored by its sub-agent** (its `route_written` is in the manifest). The driver does **not** re-author it; it only confirms the surface→route mapping holds (every parallelizable surface returned a `route_written`; none missing — else route to retry/`RF-12` via step-06).
   - `standalone-screen` **primary/root** → driver authors `src/app/<name_slug>/page.tsx` (the cross-surface hub).
   - `inline-drawer` / `inline-expand` / `modal` → driver composes the fold into the **host** surface's route as a drawer/expandable/overlay sub-tree (the fold's components, from the host's manifest, rendered on the host page). Many-to-one → driver-owned.
   - `wizard-split` → driver authors a route with N sub-steps (stepper + per-step component); one route, staged disclosure.
2. **Shared intra-prototype nav.** When the spec's §6 navigation model needs nav spanning multiple standalone surfaces (sidebar / command-palette enumerating routes), the driver authors **one** per-prototype `src/app/<name_slug>/layout.tsx` carrying it, so every leaf page (driver- or sub-agent-authored) inherits it via Next.js nested layout — **no sub-agent writes shared nav**. When the model needs no shared per-prototype nav, omit the layout (pages self-wire back-link/breadcrumb; this is the `nav_context` the dispatch passed each standalone sub-agent). The app-level `layout.tsx` (inter-prototype chrome + `data-testid="proto-chrome"`) is scaffold-authored and untouched.
   - **Brand logo (application shell).** When authoring this per-prototype `layout.tsx` app-shell and it has a brand/header slot (e.g. the `app-shell-with-topnav` / sidebar patterns' `brand` slot), render the shared brand logo there **iff one was captured at scaffold** — `prototypes/.scaffold.json` has `brand_logo != null` (equivalently `prototypes/public/brand/logo.*` exists): `<img src="<brand_logo.logo_src>" alt="<app name> logo" />` (the app title is acceptable alongside or as fallback text). This is **UI-only brand chrome** — no `data-src`/`data-prop` (same exemption as search/sort/pagination). It belongs to the **application shell**, never the scaffold-authored `PrototypeChrome` review harness (PI-08). When no per-prototype layout is authored (no shared nav) or no logo was captured, render no logo — brand-lock is application-shell-scoped and a missing logo is a valid neutral outcome.
3. **Compose** each **driver-owned** route by importing + arranging the surface's components (created or reused). Wire, exactly as the standalone sub-agents do for their own pages:
   - store usage (`useXStore`) for data display + mutation (PI-02);
   - `activeRole` from the chrome store on multi-role surfaces, varying visible components/actions per spec §6.5 RBAC (PI-05);
   - navigation per the spec's §6 model (links to `route_map` targets, command-palette entry, breadcrumbs) within the shared chrome;
   - `data-testid="primary-cta"` on the surface's primary action (verify-skill smoke contract); the chrome already carries `data-testid="proto-chrome"`.
4. **Route metadata:** set each driver-owned route's `<title>`/metadata to the prototype name.
5. Bind every data element on driver-owned routes with `data-prop="Entity.Field"` (closed set) — re-assert anti-fabrication at composition time.
6. **No per-write verify on routes.** Route files (and the per-prototype `layout.tsx`) are compile-covered — `tsc --noEmit` + the Playwright smoke gate (`step-06`) catch a bad write as a localized error the bounded-retry loop diagnoses by file path. Do **not** run `verify-artifact-write.md` on them (the option-08 compile-covered exception — see `CLAUDE.md > Constraints`).

Proceed to `step-06-verify-build.md`.
