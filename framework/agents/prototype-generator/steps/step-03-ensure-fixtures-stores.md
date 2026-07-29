# step-03-ensure-fixtures-stores

**Goal:** Author the cross-cutting data layer **before** any sub-agent dispatch, so parallel sub-agents see a consistent, complete data layer (driver-owned; collision-safety).

**Timing:** emit `substep_start` (`stage:"generator"`, `substep:"data-layer"`) before step 1 and `substep_end` after step 4b, per `prototype-generator.md > Timing log (sub-steps)`.

For each entity in the render plan (additively — never overwrite an existing entity's artefacts):

1. **Type** — add/extend the entity interface in `src/types/index.ts`. Fields = exactly the blueprint Property closed set for that entity (no fabricated fields).
2. **Fixture** — write `src/data/fixtures/<entity-kebab>.json` with a handful of realistic rows; every field is a closed-set Property (PI-02 fixtures; anti-fabrication extends to fixtures).
3. **Store** — write `src/stores/<entity-kebab>-store.ts`: a Zustand `persist` store (`createJSONStorage(localStorage)`, `skipHydration: true`) with `items`, `isLoaded`, CRUD actions, `seedFromFixtures()`, `reset()` — modelled on the template's former `_example-store` pattern. Mutations persist in-session only (PI-02). Consumers must gate reads on `isLoaded` (`shared-component-conventions.md §6`).
   **One store per §8 entity, and no others.** This is a closed set, not a floor: do **not** author a `user-store`, `auth-store`, `session-store`, or any store holding roles, grants, or session identity. Roles live in the scaffold-authored `proto-chrome-store.activeRole` (PI-05) and per-destination grants live in the nav module (step 4b). A real run wrote a `user-store.pagesForRole` that became a second grant table competing with a `lib/nav.ts` role map — the rule was previously silent on non-entity stores, which is how it got through.
4. **Register** — re-export the store from `src/stores/index.ts`; wire `seedAllStores()` (rehydrate + seed-if-empty) and `resetAllStores()` (reset+reseed) in `src/data/seed.ts` for the new store, additively (preserve other prototypes' registrations).

Then **once for the prototype** (not per entity):

4b. **Nav module (the canonical nav table).** Write `src/data/nav/<name_slug>.ts` and register it in the `src/data/nav/index.ts` barrel. Shape is canonical in `shared-component-conventions.md §6a` — do not restate or vary it.
   - One `NavEntry` per destination the prototype actually routes to: `route` + `surface_id` from step-02's `route_map` (folded surfaces contribute **no** entry — they render on their host; wizard sub-steps contribute the wizard's entry route, not each step), `label` from the design spec §5 surface intent, `roles` from step-02 rule 1b's `role_visibility`, **fully expanded** (never empty — the unrestricted case expands to the prototype's whole role set).
   - Order: the primary/root surface first, then §5 declaration order. Ordering and labelling are *how* — driver design authority per `CLAUDE.md §1`, not a spec-cited fact.
   - Barrel registration is **additive**, exactly like `src/stores/index.ts` and `src/data/seed.ts` in step 4: never drop or reorder another prototype's entry. The barrel itself is normally scaffold-authored (empty, with the `NavEntry` declaration — `prototype-app-scaffolder.md`); treat it as **create-if-absent** anyway, so an app scaffolded before that existed grows one on its next `/prototype` run rather than failing. No template change and no migration either way.
   - **This must happen here, before dispatch, not in step-05.** A `templates/*Shell` may be authored by a per-surface **sub-agent** (`step-sub-render-surface.md` rule 1b), and a sub-agent cannot write driver-owned files — so if the module does not exist before the wave, a shell that needs nav has nothing to import and hand-rolls an array instead. That is the exact failure a real run shipped.

5. **No per-write sha256 verify on compile-covered writes** (types, stores, `stores/index.ts`, `data/seed.ts`, `data/nav/*`, any driver-authored shared component) — they are covered by `tsc --noEmit` + the Playwright smoke gate (`step-06`), which the bounded-retry loop diagnoses by file path; do **not** run `verify-artifact-write.md` on them (the option-08 compile-covered exception — see `CLAUDE.md > Constraints`). **Fixtures** (`.json`) are compile-covered only indirectly (via import), so after writing each fixture do a lightweight **JSON-parse check** (parse the file; malformed → fix before dispatch) in place of the sha256 verify.

Also author here any **new shared component the ownership map assigned to the driver** (shared by ≥2 surfaces), so sub-agents can reuse it.

Proceed to `step-04-dispatch-surface-subagents.md`.
