# step-04-dispatch-surface-subagents

**Goal:** Render each surface's new shared components in parallel, safely.

1. Group the render plan by surface. **Dispatch every surface that has `owned_files` in a single wave** — one Agent-tool message with N `Agent` calls — up to a ceiling of **8**. If >8 surfaces have owned components (rare; rule 13 shrinks this over runs), batch in waves of ≤8. The disjoint `owned_files` partition (verified collision-free in step-02), **not** the wave size, is the collision-safety boundary and holds at any N; the harness caps true concurrency at ~min(16, cpu-2) and queues the remainder gracefully. A surface whose components are all reuse (no `owned_files`) needs no sub-agent — the driver composes it directly in step-05.
2. Dispatch all sub-agents in a **single Agent-tool message** (one tool block, multiple `Agent` calls — like `wireframe-orch` Stage 3). Each sub-agent prompt:
   - names `framework/agents/prototype-generator/steps/step-sub-render-surface.md` as its instructions;
   - passes the surface assignment: `{ surface_id, surface_intent, realization, host (if folded), owned_files (the ONLY files it may write), components_to_reuse, data_bindings (Property→store), posture, dimension_positions, ux-baseline subset }`;
   - states the hard rule: **write only `owned_files`; read the rest of the library; never write the data layer or route files; never overwrite an existing file.**
3. Await all. Each returns a **component manifest**: `{ surface_id, files_written, components_created, components_reused, props_bound, states_rendered, baseline_ok }` (or `failed {surface_id, reason}`).
4. On a per-surface failure: retry that one sub-agent once; if it fails again, carry the `failed` forward — step-06's bounded-retry / `RF-12` path handles terminal failure (do not silently drop a surface).

Proceed to `step-05-compose-route.md` with the collected manifests.
