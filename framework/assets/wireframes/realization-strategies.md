# Wireframe realization strategies

**Role:** asset (wireframe-private; cross-pipeline-reusable by a future `/prototype`).

**Purpose:** Define the closed enum of **realization strategies** — the ways a single
decomposition-agnostic **logical surface** (`LS-NN` in the blueprint) can be turned into
physical screen(s) in a variant. Realization is the **information-architecture divergence
axis**: two variants can render the same logical surface inventory yet differ in *how many
screens* exist and *where each surface lives* (its own screen, an inline drawer, a modal, a
multi-step wizard, or merged with a sibling).

This is the load-bearing translation between the blueprint's logical surfaces + each
variant's `surface_plan.realization` and the concrete physical screen files the
variant-generator writes.

**Baseline equivalence.** When every surface is realized `standalone-screen` (the default),
`LS-NN ≡ S-NN`, one physical screen per surface, and the pipeline behaves exactly as it did
before realization existed. This is the safety net: a run that takes only defaults is
byte-for-byte the pre-realization pipeline.

**Inherits from:**
- `framework/assets/pattern-catalogue/_index.md` — every realization maps to catalogue
  patterns that already exist (zero new pattern authoring).
- `framework/assets/wireframes/tradeoff-dimensions-registry.md` — Section 3.0 base-pattern
  ownership (the realization picks the *physical structure*; Section 3 picks the *pattern
  variant* within each physical screen).

**Used by:**
- `framework/agents/blueprint-architect/steps/step-03-author-blueprint.md` — derives each
  surface's `allowed_realizations` + `default_realization` (deterministic, from surface
  nature + relationships).
- `framework/agents/blueprint-architect/steps/step-05-compose-variants.md` — per variant,
  picks a realization from `allowed_realizations[LS]` ∩ the persona's
  `divergence_profile.realization_recommendation`, and derives `physical_screens[]`.
- `framework/agents/wireframe-variant-generator/steps/step-04-compose-screens.md` — renders
  each realization (standalone file, host-state drawer/modal, or wizard sub-screens).
- `framework/agents/wireframe-comparator.md` — surfaces the per-surface realization in the
  index's §4 "structure" row and aligns variants by logical surface.

---

## Section 1 — Realization closed enum

| Realization | Physical result | Catalogue pattern(s) | Notes |
|---|---|---|---|
| `standalone-screen` | exactly **1** own file (`screen-NN-slug.html`) | the surface's own primary pattern (`detail-page` / `table` / `single-form` / `dashboard` …) | the default; baseline equivalence |
| `inline-drawer` | **0** own files — rendered as a `host_state` sub-tree on the host surface's screen | `surfaces/drawer-detail` | detail/summary folded onto a list/parent; deep-link via `#ls-NN-drawer` (fast-follow) |
| `inline-expand` | **0** own files — rendered as an expandable region on the host screen | `collections/table` `expandable-row` / `collections/detail-panel` | row-level inline reveal on a host collection |
| `wizard-split` | **N** own files (`screen-NNa-slug.html`, `screen-NNb-…`) | `forms/multi-step-wizard` + `navigation/stepper-indicator` | one capture surface split into sequential sub-screens; one LS → many screens |
| `modal` | **0** own files — rendered as an overlay state on the host screen | `surfaces/modal-form` / `surfaces/modal-confirmation` | low-field capture or confirm/guard folded as an overlay on the host |
| `combined` *(fast-follow — not in first wave)* | **0** own files — merged into a sibling surface's single screen | `collections/master-detail-list` | the only realization that mutates a *sibling* surface; modelled on the detail LS as `realization: combined, merge_with: LS-list`; the list LS records `absorbs: LS-detail`. **Deferred** until single-surface realizations are proven. |

**First wave ships** `{ standalone-screen, inline-drawer, inline-expand, wizard-split, modal }`.
`combined` is authored in the enum for forward-compatibility but the architect must **not**
emit it until the fast-follow lands (its `allowed_realizations` derivation entry is marked
`*` in step-03 / the registry and is skipped in the first wave).

---

## Section 2 — `surface_plan` per-surface shape (consumed contract)

Each variant's `variants.json > surface_plan` is keyed by `LS-NN`. Per surface:

```json
"LS-03": {
  "realization": "inline-drawer",
  "host_surface": "LS-01",            // present iff realization folds onto a host
  "rendered_on": "S-01",              // host's physical screen_id (folds/modal only)
  "host_state": "drawer-detail-open", // the host screen state that renders this surface (folds/modal only)
  "physical_screens": [],             // standalone → 1 entry; wizard-split → N; folds/modal/combined → 0
  "covers_properties": ["FileLog.CurrentFileName","FileLog.RecordCount"],
  "primary_pattern": "surfaces/drawer-detail",
  "primary_pattern_variant": "default",
  "base_pattern_owner": "density-focus",
  "modifiers": [],
  "secondary_patterns": [],
  "states_rendered": ["default","loading"]
}
```

For `standalone-screen` and `wizard-split`, the pattern fields live on **each**
`physical_screens[]` element (so a wizard spreads `covers_properties` + pattern across its
sub-screens); for folds/modal the pattern fields sit on the surface entry and render into the
host's `host_state`. `physical_screens[]` element shape:

```json
{ "screen_id": "S-02a", "screen_file": "screen-02a-upload-pick.html",
  "sub_step": 1, "of": 3,
  "covers_properties": ["F-05:FileName","F-05:FileSettingId"],
  "primary_pattern": "forms/multi-step-wizard", "primary_pattern_variant": "default",
  "base_pattern_owner": "speed-accuracy", "modifiers": [],
  "secondary_patterns": ["navigation/stepper-indicator"],
  "states_rendered": ["default","error"] }
```

Cardinality of `physical_screens[]`: standalone → 1; wizard-split → N; `inline-drawer` /
`inline-expand` / `modal` / `combined` → 0.

---

## Section 3 — Anti-patterns

- Do not emit `combined` until the fast-follow lands. First wave is single-surface
  realizations only; `combined` is the sole realization that rewrites a sibling surface's
  screen and needs its own validation pass.
- Do not fold a surface onto a host whose own realization in the same variant produces **no**
  physical screen (no fold-of-fold). The host must resolve to a real `screen_id`.
- Do not introduce a realization value outside this enum. Adding one is a coordinated change
  across this file, `step-03`/`step-05`, the generator's `step-04`, and the comparator.
- Do not let a realization invent a pattern. Every realization maps to existing catalogue
  patterns (Section 1); an absent pattern is caught by the architect's author-time validation
  and routes to the step-07 conditional gate.
- Do not drop a folded surface's property coverage. A folded/modal surface still declares
  `covers_properties`; the generator stamps its `data-src`/`data-prop` on the drawer/modal
  sub-tree so the audit trail survives the fold.
