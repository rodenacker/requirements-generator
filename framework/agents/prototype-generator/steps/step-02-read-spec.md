# step-02-read-spec

**Goal:** Build the render plan + the disjoint component-ownership map (the collision-safety contract).

1. From spec **§5** read each surface's realization (`standalone-screen` / `inline-drawer` / `inline-expand` / `modal` / `wizard-split`) + host/rendered-on for folds. From **§7** read the component inventory (per surface: components composed, reuse vs new, atomic tier). From **§8** read per-surface data binding (Property → fixture field → store).
2. **Reuse-scan** the existing `prototypes/src/components/**` library: for every "new" component in §7, check whether an existing shared component already fits; if so, downgrade it to **reuse** (the library grows monotonically — rule 13).
3. **Cross-cutting data needs:** collect the set of entities across §8 (each needs a type + fixture + store). These are driver-owned (step-03).
4. **Component-ownership map:** assign each genuinely-new shared component to exactly one owner:
   - a component used by exactly one surface → that surface's sub-agent owns its file;
   - a new component shared by ≥2 surfaces → the **driver** authors it in step-03 (before dispatch) so no two sub-agents race it.
   Produce, per surface, a disjoint `owned_files: [<relative component paths>]` list. Verify the union is collision-free (no path assigned twice; none collides with an existing file).
5. Record the plan in memory (surfaces, realizations, per-surface owned_files, data-layer entities, reuse list). No writes in this step.

Proceed to `step-03-ensure-fixtures-stores.md`.
