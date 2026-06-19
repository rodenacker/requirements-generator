# step-sub-render-surface (per-surface sub-agent)

**Role:** the instruction set for ONE parallel sub-agent dispatched by `step-04`. It renders the **new shared components** for exactly one surface and — when the surface is a **standalone secondary** screen — **authors that surface's own standalone route page**. It is the unit that makes generation parallel + safe.

**Activation:** load `framework/assets/persona-llm.md` + `framework/assets/characters/prototype-generator.md` (same stance as the driver).

**Assignment (passed in the dispatch prompt):** `{ surface_id, surface_intent, realization, host?, owned_files, owned_route_file (its own `src/app/<name_slug>/<surface-kebab>/page.tsx`, or null when the driver owns the route), route_map (outbound link target route strings + breadcrumb trail — knowledge only), nav_context (shared per-prototype `layout.tsx` present, or self-wire back-link/breadcrumb), components_to_reuse, data_bindings (Property→fixture-field→store), role_visibility (§6.5 per-role visibility for this surface, or null), posture, dimension_positions, ux_baseline_subset }`.

## Hard rules (collision-safety)

- **Write ONLY the files in `owned_files`.** These are new shared components under `src/components/{atoms,molecules,organisms,templates,domain}/` — plus, for a standalone secondary surface, your **one** `owned_route_file` (`src/app/<name_slug>/<surface-kebab>/page.tsx`).
- **Never** write any route file other than your own `owned_route_file`: not the root `page.tsx`, not a per-prototype `layout.tsx`, not a folded-host route, not a wizard route. Never write the data layer (`types`/`fixtures`/`stores`/`seed`) or any file not in `owned_files`. The driver owns those. (When `owned_route_file` is null you write no route at all — the driver composes your surface in step-05.)
- **Never overwrite** an existing component — reuse it (it's in `components_to_reuse`).
- Read the existing shared library + the shadcn `ui/` primitives freely.

## Render contract

0. **Timing (self-measure only).** Capture an ISO start timestamp at activation (`(Get-Date).ToUniversalTime().ToString('o')`) and an end timestamp immediately before returning; report them as `started`/`ended` in the manifest. **Do not append to `framework/state/timing.ndjson` yourself** — concurrent writes from parallel sub-agents would corrupt it; the driver emits your `render-surface` span from these values after the wave joins (see `prototype-generator.md > Timing log`).
1. Compose each owned component from shared `ui/` primitives + existing shared components, themed by the fixed brand tokens (no new palette/type/radius — D1).
2. Apply the **posture + positions** to layout/density/disclosure/interaction only (e.g. dense table at D3+, inline-edit at D1+/P1, wizard step at P2, calm whitespace at P5). Realize the surface per its `realization`. For a **fold/wizard** surface (`owned_route_file` null) you produce only the component(s) the drawer/modal/expand/wizard-step needs — the driver wires them into the host/wizard route in step-05.
3. **Anti-fabrication:** every data-bound element binds to a Property in `data_bindings` (the blueprint closed set) and carries `data-prop="Entity.Field"` (or `F-NN:Param`). No invented fields. UI-only controls (search/sort/pagination/filters/save/cancel/density-toggle) are exempt and carry no `data-prop`. This applies to your components **and** to your route page (step 4).
4. **Author your own standalone route — only when `owned_route_file` is set.** Write that one `page.tsx`, composing your surface's components inside the shared chrome, and wire exactly what the driver wires for driver-owned routes (relocated here for your page):
   - store usage (`useXStore`) for data display + mutation (PI-02);
   - `activeRole` from the chrome store when `role_visibility` is non-null, varying visible components/actions per that rule (PI-05);
   - **`data-testid="primary-cta"` on the surface's primary action** (the verify-skill smoke contract — every route must expose it unless the surface genuinely has no primary action; do not omit it when one exists);
   - outbound navigation: `<Link href>` only to the **target route strings in `route_map`** (never guess a route) + this surface's breadcrumb. Rely on the shared per-prototype `layout.tsx` for sidebar/command-palette when `nav_context` says it exists — **do not author shared nav yourself**;
   - route metadata: set the route `<title>` to the prototype name;
   - re-assert anti-fabrication on the page (`data-prop` ∈ closed set), same as for components.
   The chrome already carries `data-testid="proto-chrome"` (from the app-level layout — do not re-stamp it).
5. **Baseline floor** (`ux_baseline_subset` from `ux-baseline-checklist.md`): render the three states (empty/loading/error) where the surface is a collection or async action; keyboard-operable + visible focus; name/role/value on controls; not-colour-alone for status; ≥24px targets. Self-check before writing.
6. **No per-write verify.** Your writes (components + your one route page) are all compile-covered — `tsc --noEmit` + the Playwright smoke gate (`step-06`) catch a truncated or malformed write as a localized error the bounded-retry loop diagnoses by file path. Do **not** run `verify-artifact-write.md` on them (the option-08 compile-covered exception — see `CLAUDE.md §2`). Self-check the render before returning instead.

## Return (route manifest)

`{ surface_id, files_written: [...], components_created: [...], components_reused: [...], props_bound: ["Entity.Field", ...], states_rendered: ["default","loading","empty","error", ...], baseline_ok: true, started: "<iso>", ended: "<iso>" }` — and, **when you authored a route**, also `{ route_written: "<owned_route_file>", primary_cta_present: true|false (false only if the surface has no primary action), outbound_links: ["<route_path>", ...] }`. Or `failed { surface_id, reason }` (e.g. a binding not in the closed set, an unrenderable realization, a `route_map` target you could not wire). The driver consumes the manifest in `step-05` (to skip re-authoring an already-written standalone route, or to compose a driver-owned one) and in `step-07` to self-validate.

## Anti-patterns

- Do not write outside `owned_files`; do not touch the data layer; do not write any route file other than your own `owned_route_file` (no root page, no `layout.tsx`, no folded-host or wizard route).
- Do not author shared intra-prototype nav (sidebar/command-palette/per-prototype layout) — inherit it from the driver-authored `layout.tsx`; only wire your own outbound `<Link>`s + breadcrumb.
- Do not guess a route string — wire `<Link href>` only to the targets given in `route_map`.
- Do not omit `data-testid="primary-cta"` when your surface has a primary action (the smoke gate fails the route without it).
- Do not invent data fields or fixtures; bind only to the closed set.
- Do not add a private/per-prototype theme or component folder (rules 15–16; D1).
- Do not skip the three states or the baseline self-check.
- Do not return success with a fabricated binding or an unwired `route_map` target — return `failed` so the driver can route to retry/`RF-12`.
