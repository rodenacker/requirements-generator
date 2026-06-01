# step-07-handback

**Goal:** Final self-validation + hand back to the orchestrator.

1. Run the driver self-validation (per `prototype-generator.md > Self-validation`):
   - every `LS-NN` realized (standalone route / folded-in-host / wizard steps); no surface missing;
   - every `data-prop` value ∈ the blueprint closed set (Grep the rendered routes/components vs the closed set); fixtures carry only closed-set fields — **zero fabrications**;
   - no component definitions under `src/app/<name_slug>/**`; no private per-prototype components; no existing shared component overwritten; new stores registered in `index.ts` + `seed.ts`;
   - `data-testid="proto-chrome"` (chrome) + `data-testid="primary-cta"` (primary action) present; multi-role surfaces read `activeRole` (PI-05);
   - `ux-baseline-checklist.md` floor satisfied on every surface;
   - the verify gate returned `pass` / `pass-with-warning`.
2. Hand back to the orchestrator:
   - **`ok {name_slug, route, components_created[], components_reused[], smoke_skipped?}`** — the orchestrator advances to the landing update (Step F4).
   - **`failed {structured}`** — a self-validation miss that bounded retry could not clear, or an `RF-12` halt. The orchestrator does not update the landing; the broken route + spec remain on disk for inspection.
3. Do not present to the consultant or run an accept loop — the orchestrator owns the Step-G accept gate.
