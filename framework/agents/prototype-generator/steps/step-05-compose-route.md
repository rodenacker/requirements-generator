# step-05-compose-route

**Goal:** Assemble the route tree under `src/app/<name_slug>/**`, composing the shared components into each surface's realization. Driver-owned (route files); collision-free with sub-agents.

For the prototype's surfaces (using the component manifests from step-04 + reused components):

1. **Route structure per realization** (`framework/assets/wireframes/realization-strategies.md`):
   - `standalone-screen` → its own route file (`src/app/<name_slug>/<surface-kebab>/page.tsx`, or the primary surface as `src/app/<name_slug>/page.tsx`).
   - `inline-drawer` / `inline-expand` / `modal` → **no own route**; composed into the host surface's route as a drawer/expandable/overlay sub-tree (the fold's components rendered on the host page).
   - `wizard-split` → a route with N sub-steps (stepper + per-step component); one route, staged disclosure.
2. **Compose** each route by importing + arranging the surface's components (created or reused). Wire:
   - store usage (`useXStore`) for data display + mutation (PI-02);
   - `activeRole` from the chrome store on multi-role surfaces, varying visible components/actions per spec §6.5 RBAC (PI-05);
   - navigation per the spec's §6 navigation model (links, command-palette entry, breadcrumbs) within the shared chrome;
   - `data-testid="primary-cta"` on the surface's primary action (verify-skill smoke contract); the chrome already carries `data-testid="proto-chrome"`.
3. **Route metadata:** set the route's `<title>`/metadata to the prototype name. Compose under the shared `layout.tsx` (no per-prototype layout unless the realization needs a nested layout — that nested layout is still a route file, driver-owned).
4. Bind every data element with `data-prop="Entity.Field"` (closed set) — re-assert anti-fabrication at composition time.
5. Verify each route file via `framework/skills/verify-artifact-write.md`.

Proceed to `step-06-verify-build.md`.
