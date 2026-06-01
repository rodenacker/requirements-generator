# step-03-ensure-fixtures-stores

**Goal:** Author the cross-cutting data layer **before** any sub-agent dispatch, so parallel sub-agents see a consistent, complete data layer (driver-owned; collision-safety).

For each entity in the render plan (additively — never overwrite an existing entity's artefacts):

1. **Type** — add/extend the entity interface in `src/types/index.ts`. Fields = exactly the blueprint Property closed set for that entity (no fabricated fields).
2. **Fixture** — write `src/data/fixtures/<entity-kebab>.json` with a handful of realistic rows; every field is a closed-set Property (PI-02 fixtures; anti-fabrication extends to fixtures).
3. **Store** — write `src/stores/<entity-kebab>-store.ts`: a Zustand `persist` store (`createJSONStorage(localStorage)`, `skipHydration: true`) with `items`, `isLoaded`, CRUD actions, `seedFromFixtures()`, `reset()` — modelled on the template's former `_example-store` pattern. Mutations persist in-session only (PI-02).
4. **Register** — re-export the store from `src/stores/index.ts`; wire `seedAllStores()` (rehydrate + seed-if-empty) and `resetAllStores()` (reset+reseed) in `src/data/seed.ts` for the new store, additively (preserve other prototypes' registrations).
5. Verify each write via `framework/skills/verify-artifact-write.md`.

Also author here any **new shared component the ownership map assigned to the driver** (shared by ≥2 surfaces), so sub-agents can reuse it.

Proceed to `step-04-dispatch-surface-subagents.md`.
