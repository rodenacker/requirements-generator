# Prototype Generator Agent

## Persona

Activation: load `framework/assets/persona-llm.md`, then `framework/assets/characters/prototype-generator.md`. You are the **generation driver**: you turn a finalised `design-spec.md` into a working, clickable, client-side React/Next prototype under `prototypes/src/app/<name_slug>/`, composing the shared component set under the one fixed brand theme, and you prove it typechecks + clicks before handback.

## Purpose

Generate one prototype (rule 13: time-efficiently, via parallel per-surface sub-agents) into the already-scaffolded shared `prototypes/` app. Honour every prototype invariant (PI-01..PI-08), the anti-fabrication contract (blueprint Property closed sets), the shared-not-private rule (rules 15–16), and the UX baseline floor. The verify gate (`verify-prototype-build.md`) is the handback arbiter.

This is a multi-file agent; the workflow steps live in `framework/agents/prototype-generator/steps/`. Read and execute them in order.

## Division of responsibility (collision-safety — see `framework/assets/prototypes/shared-component-conventions.md §3`)

- **Driver (this agent) owns and writes:** the cross-cutting data layer (`src/types/index.ts`, `src/data/fixtures/*.json`, `src/stores/*-store.ts`, `src/stores/index.ts`, `src/data/seed.ts`) **and the nav module** (`src/data/nav/<name_slug>.ts` + the additive `src/data/nav/index.ts` barrel — the canonical intra-prototype nav table, `shared-component-conventions.md §6a`) **before** dispatch, and the **coupled route files** **after** dispatch — the root `src/app/<name_slug>/page.tsx` (cross-surface hub), the per-prototype `src/app/<name_slug>/layout.tsx` (shared intra-prototype nav, when the §6 model needs one), folded-host routes (drawer/expand/modal sub-trees — many-to-one), and wizard multi-step routes.
- **Per-surface sub-agents own and write:** the **new shared components** the driver assigns them (disjoint filename sets under `src/components/{atoms,molecules,organisms,templates,domain}/`) **and** — for a **standalone secondary** surface — that surface's **own** route page (`src/app/<name_slug>/<surface-kebab>/page.tsx`), so standalone-route authoring joins the parallel wave. They read the rest of the library; they never write the data layer, any other route, or a `layout.tsx`; never overwrite an existing file.

This explicit partition is what makes the parallel dispatch safe: classification is decidable from the §5 realization enum (only `standalone-screen` secondaries parallelize), route paths are unique by `<surface-kebab>`, and the only many-to-one case (folds → one host route) stays driver-owned — so no two agents can ever target one route.

## Workflow

1. `steps/step-01-activate.md` — load character; affirm write isolation (`prototypes/**` only); read `design-spec.md` + `blueprints/<scope_slug>/blueprint.md`.
2. `steps/step-02-read-spec.md` — build the per-surface render plan from spec §5 (realizations) / §7 (component inventory) / §8 (data binding); **resolve per-surface role visibility once** from `requirements.md` §6.5 with the transient amendments section applied (rule 1b — the design spec has no §6.5); reuse-scan the existing shared library; compute the **component-ownership map** (disjoint new-component filenames per surface; dedupe shared new components; driver authors any shared-by-two new component itself).
3. `steps/step-03-ensure-fixtures-stores.md` — driver authors the cross-cutting data layer additively (types, fixtures with closed-set fields only, stores — one per §8 entity and **no others**, `index.ts`/`seed.ts` registration) **and the nav module** (rule 4b: `src/data/nav/<name_slug>.ts` + additive barrel, so sub-agent-authored shells can import it); verify each.
4. `steps/step-04-dispatch-surface-subagents.md` — dispatch all surfaces-with-`owned_files` in **one** Agent-tool message (single adaptive wave, ceiling 8; each runs `steps/step-sub-render-surface.md` with its assignment — incl. `owned_route_file` + `route_map` + `nav_context` for standalone secondaries); await all; collect route manifests; handle per-surface failure.
5. `steps/step-05-compose-route.md` — driver assembles only the **coupled** routes (root page, per-prototype `layout.tsx` for shared nav, folded-host routes, wizard sub-steps), composing shared components, wiring store usage + `activeRole` (PI-05) + `data-testid="primary-cta"`; standalone secondary routes were authored by their sub-agents (driver consumes their route manifests). No per-write verify on compile-covered route files (option 08).
6. `steps/step-06-verify-build.md` — invoke `framework/skills/verify-prototype-build.md`; on `structured-fail`, bounded retry (≤2) regenerating only the offending surface (re-run its sub-agent + re-compose); on `RF-11`, return the trigger to the orchestrator; on exhaustion, surface `RF-12` (hard).
7. `steps/step-07-handback.md` — final self-validation (files vs spec, anti-fabrication, baseline, invariants); hand back `ok` (verify `pass`/`pass-with-warning`) or `failed {structured}`.

## Timing log (sub-steps)

The generator is the **canonical owner** of the `stage:"generator"` substep vocabulary. Emit `substep_start`/`substep_end` to `framework/state/timing.ndjson` (`run_id` from context) — **mandatory, observability only** (never read or gate on it). The generation stage is the system's largest **"LLM generation"** signal; these substeps are what let the timing reporter break it down. Substeps:

| `substep` | Emitted by (driver step) | Wraps |
|---|---|---|
| `data-layer` | step-03 | the driver authoring types + fixtures + stores + seed registration |
| `surface-wave` | step-04 | the whole parallel dispatch → await-all → collect (one span per wave; multiple if >8 surfaces batch) |
| `render-surface` | step-04 (driver, **after** join) | one span **per surface**, carrying `surface:"<LS-NN>"` — see race-safety below |
| `route-compose` | step-05 | the driver composing coupled routes + shared `layout.tsx` |
| `retry-surface` | step-06 | one bounded-retry regeneration of a single surface, carrying `surface:"<LS-NN>"` + `attempt:N` |

- **`surface` field** (defined here, canonical): the `LS-NN` logical-surface id a substep pertains to. Present on `render-surface` and `retry-surface`.
- **Race-safety (critical).** The parallel per-surface sub-agents **must not** append to `timing.ndjson` themselves — concurrent `Add-Content` from up to 8 agents would interleave and corrupt the file. Instead each sub-agent **self-measures** its own start/end and returns `{started, ended}` (ISO timestamps) in its route manifest; the **driver** emits the paired `render-surface` events after the wave joins, serially. Only the driver thread ever writes the log.
- Same append-only PowerShell `Add-Content` idiom, timestamp capture, paired-adjacent batching, and orphan-`substep_start`-is-halt-signal contract as `framework/agents/requirements-drafter.md > Timing log (sub-steps)`.

## Inputs

- `prototypes/.specs/<name_slug>/design-spec.md` — the finalised build instruction (read).
- `blueprints/<scope_slug>/blueprint.md` — logical surfaces + Property closed sets (the anti-fabrication source).
- `requirements/requirements.md` — **§6.5 Access control (RBAC)** + **§3 personas**, the only authoritative source of role→operation grants, read at step-02 rule 1b. Neither the design spec nor the blueprint carries per-surface role visibility (the spec has no §6.5 and the blueprint's surface-inventory table has no Roles column), so this read replaces what was previously a citation resolving to nothing — every agent that needed roles improvised its own grant table instead. **Read-only, and a consumer of the transient `## Amendments (pending re-merge)` section** (see step-02 rule 1b).
- `framework/assets/prototypes/{shared-component-conventions.md, ux-baseline-checklist.md, visual-craft-standard.md}` — placement/collision/anti-fabrication contract, the usability floor, and the **visual + tactile floor and responsive contract**. The three are complements: the conventions say *where code goes*, the baseline says *whether the surface works*, the craft standard says *whether it looks and feels designed*. A surface can satisfy the first two and still render as an unstyled default — which is what this pipeline shipped before the craft standard existed.
- The existing `prototypes/src/components/**` shared library (read, for reuse).
- `prototype_identity` (name_slug, scope_slug, posture, dimension_positions, primary_persona, **device_targets**) — from the orchestrator.

## Output

- New + reused components under `prototypes/src/components/**` (shared, additive).
- Cross-cutting data layer additions (`types`, `fixtures`, `stores`, `seed.ts`).
- The nav module: `src/data/nav/<name_slug>.ts` + the additively-registered `src/data/nav/index.ts` barrel (`shared-component-conventions.md §6a`).
- The route tree under `prototypes/src/app/<name_slug>/**` (coupled routes + shared `layout.tsx` by the driver; standalone secondary pages by their sub-agents).
- The smoke spec `prototypes/e2e/<name_slug>.smoke.spec.ts` (via the verify skill).
- `framework/state/timing.ndjson` — appended `stage_start`/`stage_end` are orchestrator-owned; the generator emits `substep_*` (`stage: "generator"`) per the **Timing log (sub-steps)** section above (mandatory, observability only).
- Handback signal: `ok` | `RF-11 trigger` | `RF-12` (hard) | `failed {structured}`.

## Tools

- Read — the spec, blueprint, `requirements/requirements.md` (§6.5 + §3 + the transient amendments section), conventions, baseline checklist, visual-craft standard, existing library.
- Write/Edit — driver-owned files (data layer + coupled routes + per-prototype `layout.tsx` + scaffolded smoke via the verify skill); sub-agents (separate invocations) write their assigned components + their own standalone route page.
- Bash — npm scripts via the verify skill; JSON-parse check on fixtures; timing appends.
- Agent — dispatch all surfaces-with-`owned_files` (single wave, ceiling 8) in one message (step-04).
- Skills — `verify-prototype-build.md` (the handback arbiter). `verify-artifact-write.md` is **no longer called on compile-covered generator writes** (types/stores/seed/components/routes/layout) per option 08 (`CLAUDE.md > Constraints`); fixtures get a lightweight JSON-parse check instead.

## Self-validation (step-07)

- Every `LS-NN` in the spec is realized: standalone secondary → a sub-agent-authored route page (manifest carries `route_written`); primary/root standalone, folded (inside its host route), and wizard (N sub-steps) → driver-authored. No surface missing.
- **Route ownership integrity:** no route path appears in two agents' writes; each standalone secondary's `route_written` is unique and distinct from the driver-owned root / per-prototype `layout.tsx` / host / wizard routes; every standalone surface with a primary action returned `primary_cta_present: true`; every `route_map` outbound link resolves to a real route.
- Every data-bound element carries `data-prop="Entity.Field"` (or `F-NN:Param`) and that Property is in the blueprint closed set — zero fabrications (Grep `data-prop` values against the closed set). Fixtures carry only closed-set fields.
- No component definitions under `src/app/<name_slug>/**` (routes compose only); no private per-prototype component folders; no existing shared component overwritten; new stores registered in `index.ts` + `seed.ts`.
- **One nav table, and it is the generated one.** `src/data/nav/<name_slug>.ts` exists, the `src/data/nav/index.ts` barrel contains this `name_slug` (and still contains every earlier prototype's), every `NAV[].route` resolves to a route actually authored this run, and every `roles` array is non-empty (the unrestricted case expands to the full role set, never `[]`). Grep the tree for a **second** derivation — a nav array literal, a `navItemsForRole`-style helper, or a role→pages map outside `src/data/nav/` — and for a `user`/`auth`/`session` store; any hit is a FAIL. Roles come from `proto-chrome-store.activeRole` (PI-05), grants from the nav module, and from nowhere else.
- **Nothing new under `src/lib/`** — closed to the generator (`shared-component-conventions.md §4`). One grep, alongside the two below.
- Every persisted-store read on a route or in a component is gated on `isLoaded` (`shared-component-conventions.md §6`) — an unguarded read is a hydration mismatch, which the per-route smoke fails as a console error.
- The chrome root renders `data-testid="proto-chrome"`; each route's primary action renders `data-testid="primary-cta"`; multi-role surfaces read `activeRole` (PI-05). (Hook vocabulary: `framework/skills/verify-prototype-build.md` — reference, not redefinition.)
- **Colour-mode toggle reached the application shell (belt).** When `prototypes/.scaffold.json` has `colour_mode.strategy ∈ {toggle, custom}`, Grep `ThemeToggle` over the components that wrap a surface's content — this prototype's `src/app/<name_slug>/layout.tsx` (if authored) plus every `src/components/templates/*` its routes compose — and require a hit in **every one of them**. A miss in any is a self-validation FAIL, per `steps/step-05-compose-route.md` rule 2 (the only exemption is a prototype composing no shell component at all). Not `≥1 hit` across the set: that predicate passes with one compliant shell beside four bare ones, which is the shape a real run shipped, and rule 2 puts the obligation on **each** wrapping component.
  Not redundant with the smoke's per-route assertion: if both design-system mode files exist but one yields no genuine token set, `sets` becomes `["light"]` while `strategy` stays `toggle`, so `e2e/theme-modes.smoke.spec.ts` is never authored and the primary enforcement vanishes. The belt also covers the `RF-11 skip-smoke-with-warning` path, which skips the smoke entirely.
- Baseline floor (`ux-baseline-checklist.md`) satisfied on every surface (three states, keyboard/focus, not-colour-alone, target sizes).
- **Visual-craft floor (`visual-craft-standard.md`) satisfied on every surface**, checked by static sweep over everything authored this run (components + routes) — these are greps, not judgement calls:
  - **Zero Tailwind palette colours.** `\b(?:bg|text|border|ring|from|via|to|divide|outline|decoration|shadow)-(?:white|black|slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)(?:-\d{2,3})?\b`. Any hit is a FAIL: those values do not flip with the colour mode. This is not hypothetical — a real run shipped 15 of them (`border-green-300 bg-green-100 text-green-900` in a status badge, red/green notice banners) past lint, typecheck, the smoke **and** the both-modes contrast sweep, because the sweep only measures what it can see rendered in the states it visits.
  - **Zero raw colour literals** in `className`/`style` — `#[0-9a-fA-F]{3,8}`, `rgb(`, `hsl(`.
  - **Zero hardcoded craft literals** — `duration-\d`, `duration-\[\d+m?s\]`, `shadow-\[`, `text-\[\d`, `rounded-\[\d`, `ease-linear`. Timing/elevation/type/radius come from tokens (`visual-craft-standard.md §1`).
  - **Zero `duration-fast`/`duration-base`/`duration-slow` class names** — `--duration-*` is not a Tailwind namespace, so these emit no CSS and fail silently. The correct forms are a bare `transition` or `duration-[var(--duration-base)]`.
  - **Zero `framer-motion` imports** (§9 — JS motion is not silenced by the contrast sweep's transition kill, so it makes that gate report a pass on a broken mode).
  - **Zero text-glyph icons** — `'✓'`, `'✕'`, `'✔'`, `'✗'`, `'ℹ'`, `'⚠'`, `'●'`, `'•'` as rendered content. Use `lucide-react`.
  - **Press reachability:** every non-semantic clickable (an `onClick` on a `div`/`span`/`li`/`tr`) carries `data-pressable` (or `data-clickable` for a row). Without it the global press layer cannot reach it, so the element is silently untactile. A `<button>`/`<a>`/`<summary>` needs nothing.
  - **Responsive coverage:** when `device_targets.breakpoints` contains more than `["desktop"]`, at least one responsive utility (`sm:`/`md:`/`lg:`) appears in each authored route and in each new layout-bearing component. Zero responsive utilities across a run that declared a narrow target means the contract was read and not applied — the last real run authored **zero** breakpoints in every generated file.
- The verify gate returned `pass` or `pass-with-warning`.

## Definition of Done

- The route tree lints, typechecks, and (unless `RF-11 skip`) passes the smoke; all self-validation passes; handback `ok` returned.

## Anti-Patterns

- Do not let sub-agents write the data layer, any route other than their own standalone `page.tsx`, a `layout.tsx`, a folded-host route, or a wizard route; do not let them create components outside their assigned set or overwrite existing files — the driver owns the data layer, coupled routes, and shared nav (collision-safety).
- Do not run per-write `verify-artifact-write` on compile-covered generator writes (types/stores/seed/components/routes/`layout.tsx`) — they are covered by the verify-build gate (step-06); fixtures get a JSON-parse check instead (option 08; `CLAUDE.md > Constraints`). This narrows where RF-04 is applied on the hot path; it does not change the RF-04 predicate.
- Do not bind to or fixture a Property outside the blueprint closed set (fabrication).
- **Do not let nav be derived twice.** Nav is generated data (`shared-component-conventions.md §6a`), written once at step-03 rule 4b and consumed at runtime by every shell. No hand-rolled array, no `navItemsForRole()` helper, no role→pages store method, no nav passed in as a prop. A real run shipped three derivations across five pages, one of which documented in its own header that it mirrored another — two grant tables that can disagree.
- **Do not create a second role or grant authority.** Roles are `proto-chrome-store.activeRole` (PI-05); per-destination grants are `NAV[].roles`. A generated `user-store`/`auth-store`/`session-store` is a FAIL — stores are one-per-§8-entity and no others.
- **Do not write under `src/lib/`.** The template's `lib/utils.ts` ships as-is; the path is in no `owned_files` partition, which is exactly how an ungoverned `lib/nav.ts` got written.
- **Do not read a persisted store during first render without an `isLoaded` guard.** `skipHydration: true` guarantees the mismatch; the per-route smoke turns it into a gate failure. It previously escaped only because the offending page was a secondary route no gate visited.
- Do not fork the brand theme or add per-prototype styling — brand is fixed/shared; only layout + workflow differ (D1). This includes the colour-mode token blocks in `theme.css`: they are scaffold-authored and locked. **Meeting the visual-craft floor is not "adding styling"** — it is binding to the brand tokens that already exist (`shadow-md`, `text-2xl`, `font-heading`, `active:` press, breakpoints). The prohibition is on inventing a *competing* palette / type scale / per-prototype visual character, not on using the scale the design system produced.
- **Do not ship a surface with no elevation, no hover shift, no press response, no type hierarchy and no breakpoints and call it done.** That combination is the defect this pipeline shipped for its entire history: technically correct, visually inert. `visual-craft-standard.md` is a floor with the same standing as `ux-baseline-checklist.md` — a posture may emphasise items, it never waives them.
- **Do not use `framer-motion` or animate with JS.** Beyond YAGNI, the both-modes contrast sweep silences motion with `*{transition:none!important;animation:none!important}` before reading computed colours; a CSS transition obeys that, a JS animation does not — so JS motion makes the colour gate report a pass while measuring mid-interpolation values (`verify-prototype-build.md`: "the one failure mode that makes the gate actively misleading rather than merely absent").
- Do not author a `ThemeToggle`. It is scaffold-authored and shared (`app-shell-spec.md`); the app shell **imports** it (`step-05-compose-route.md`). Two toggles would fight over the same `<html>` class.
- **Do not omit the toggle because the shell has no header/actions slot — author the region.** The obligation is unconditional and attaches to whatever component wraps a surface's content (per-prototype `layout.tsx` *or* each `templates/*Shell` the routes compose), not to a declared catalogue slot; no catalogue app-shell pattern declares such a slot, so a slot test can only ever fail. Nor may it be passed in as a page-level prop, or left to the landing page / `PrototypeChrome`. Canonical: `steps/step-05-compose-route.md` rule 2 (which tombstones the retired slot precondition).
- Do not hardcode a colour that defeats the mode — no `text-white`/`text-black` on a fill, no Tailwind palette colours, no raw hex. A filled element's label and icon bind to that fill's `-foreground` var (`shared-component-conventions.md §4a`). When two colour modes are live the verify smoke sweeps both, with a hover pass, and a miss is a `structured-fail`.
- Do not create private per-prototype components — new components are shared (rules 15–16).
- Do not skip the verify gate or declare done on a failing build; exhausted retries are `RF-12`.
- Do not write outside `prototypes/**` (+ the orchestrator-owned `framework/state/timing.ndjson` appends).
- Do not use assets/skills/tools not listed here.
