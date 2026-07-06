# step-02-read-spec

**Goal:** Build the render plan + the disjoint component-ownership map (the collision-safety contract).

1. From spec **§5** read each surface's realization (`standalone-screen` / `inline-drawer` / `inline-expand` / `modal` / `wizard-split`) + host/rendered-on for folds. From **§7** read the component inventory (per surface: components composed, reuse vs new, atomic tier). From **§8** read per-surface data binding (Property → fixture field → store). From **§3** read the Application character rows + copy-guidance sub-table into in-memory `app_character` (`null` on the `none recorded` fallback) — the copy-voice input for every surface's user-facing copy.
2. **Reuse-scan** the existing `prototypes/src/components/**` library: for every "new" component in §7, check whether an existing shared component already fits; if so, downgrade it to **reuse** (the library grows monotonically — rule 13).
3. **Cross-cutting data needs:** collect the set of entities across §8 (each needs a type + fixture + store). These are driver-owned (step-03).
4. **Route map + parallelizable classification** (decidable from the §5 realization — a closed enum, not a heuristic). Build `route_map`: per surface `{ route_path, realization, is_parallelizable }`:
   - `standalone-screen`, **non-primary** → `route_path = src/app/<name_slug>/<surface-kebab>/page.tsx`; `is_parallelizable = true` (its sub-agent authors this leaf route — see `step-sub-render-surface.md`).
   - the **primary/root** standalone surface → `route_path = src/app/<name_slug>/page.tsx`; `is_parallelizable = false` (the cross-surface hub; driver-owned in step-05).
   - `inline-drawer` / `inline-expand` / `modal` → **no own route** (rendered on the host's screen); `is_parallelizable = false` (driver composes onto the host route — many-to-one, the only collision risk, kept driver-owned).
   - `wizard-split` → N sub-step routes; `is_parallelizable = false` (driver-owned multi-step wiring).
5. **File-ownership map:** assign each genuinely-new shared component to exactly one owner:
   - a component used by exactly one surface → that surface's sub-agent owns its file;
   - a new component shared by ≥2 surfaces → the **driver** authors it in step-03 (before dispatch) so no two sub-agents race it.
   Then, for each `is_parallelizable` surface, **append its `route_map.route_path` to that surface's `owned_files`** — the sub-agent authors its own standalone leaf route alongside its components.
   Produce, per surface, a disjoint `owned_files: [<relative paths>]` list (uniquely-owned new components + the one standalone route where applicable). **Verify the union is collision-free** — no path assigned twice; no route path collides with the driver-owned root `page.tsx`, a per-prototype `layout.tsx`, or any folded-host route; none collides with an existing file. Route paths are unique by construction (one `<surface-kebab>/page.tsx` per surface), so the partition stays provably disjoint. A duplicate or collision is an `RF-04`-class self-validation FAIL — fix before dispatch.
6. Record the plan in memory (surfaces, realizations, `route_map`, per-surface owned_files, data-layer entities, reuse list). No writes in this step.

Proceed to `step-03-ensure-fixtures-stores.md`.
