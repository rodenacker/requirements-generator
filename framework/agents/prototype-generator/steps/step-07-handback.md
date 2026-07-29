# step-07-handback

**Goal:** Final self-validation + hand back to the orchestrator.

1. Run the driver self-validation (per `prototype-generator.md > Self-validation`):
   - every `LS-NN` realized (standalone route / folded-in-host / wizard steps); no surface missing;
   - every `data-prop` value ∈ the blueprint closed set (Grep the rendered routes/components vs the closed set); fixtures carry only closed-set fields — **zero fabrications**;
   - no component definitions under `src/app/<name_slug>/**`; no private per-prototype components; no existing shared component overwritten; new stores registered in `index.ts` + `seed.ts`;
   - **single-nav-table pass** — `src/data/nav/<name_slug>.ts` exists, the `src/data/nav/index.ts` barrel carries this `name_slug` **and** every earlier prototype's, every `NAV[].route` matches a route authored this run, every `roles` array is non-empty. Then Grep for a **second** derivation and for stray writes, in the same pass as the two greps above: a nav array literal / `navItemsForRole`-style helper / role→pages map outside `src/data/nav/`; any `user`/`auth`/`session` store; anything new under `src/lib/`; any unguarded persisted-store read (a `useXStore` read not gated on `isLoaded`). Any hit is a FAIL — four greps, one pass, per `shared-component-conventions.md §4/§6/§6a`;
   - `data-testid="proto-chrome"` (chrome) + `data-testid="primary-cta"` (primary action) present; multi-role surfaces read `activeRole` (PI-05);
   - **colour-mode toggle belt** — when `prototypes/.scaffold.json` has `colour_mode.strategy ∈ {toggle, custom}`, Grep `ThemeToggle` over the surface-wrapping components (this prototype's `src/app/<name_slug>/layout.tsx` if authored, plus every `src/components/templates/*` its routes compose) and require a hit in **every one of them** — not ≥1 across the set. A `≥1` predicate passes when one compliant shell sits beside four bare ones, which is precisely the shape a real run shipped; the obligation in `step-05-compose-route.md` rule 2 attaches to **each** component that wraps a surface's content, so the check must too. The only exemption remains a prototype composing no shell component at all (also rule 2). Run it alongside the closed-set `data-prop` grep above — same pass, two greps;
   - `ux-baseline-checklist.md` floor satisfied on every surface;
   - the verify gate returned `pass` / `pass-with-warning`.
2. Hand back to the orchestrator:
   - **`ok {name_slug, route, components_created[], components_reused[], smoke_skipped?}`** — the orchestrator advances to the landing update (Step F4).
   - **`failed {structured}`** — a self-validation miss that bounded retry could not clear, or an `RF-12` halt. The orchestrator does not update the landing; the broken route + spec remain on disk for inspection.
3. Do not present to the consultant or run an accept loop — the orchestrator owns the Step-G accept gate.
