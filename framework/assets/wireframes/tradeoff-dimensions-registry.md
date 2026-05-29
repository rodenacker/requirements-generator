# Wireframe trade-off dimensions registry

**Role:** asset (wireframe-private).

**Purpose:** Project the canonical trade-off vocabulary at
`framework/assets/trade-off-dimensions.md` into the operational decisions a
wireframe-variant-generator has to make: *which catalogue pattern (and which
variant of it) does each dimension position translate to, per pattern category?*

This registry is the load-bearing translation layer between the architect's
abstract `variants.json > dimension_positions` (`-2..+2` per dimension) and the
variant-generator's concrete per-screen pattern picks. Without it, variants at
adjacent positions render visually-identical HTML and the comparator's matrix
becomes uninformative.

**Inherits from:** `framework/assets/trade-off-dimensions.md` (canonical vocabulary).
The canonical doc is currently a stub; this file references its six dimensions
*by name* and documents per-pattern-category effects. Once the canonical doc is
authored, no change is needed here as long as the dimension names remain stable.

**Known canonical-vocabulary issue (release-blocker for `/wireframe`):** the
canonical doc currently lists `Memorability↔Density` as the sixth axis, which
duplicates Density with `Density↔Focus`. The duplication is resolved upstream of
this file by the canonical-vocabulary owner (proposed: replace with
`Memorability↔Discoverability`). This registry references the **resolved** name
once it lands. Until then, the duplicated row is marked `STATUS: pending
upstream resolution` and consumers (variant-generator) must not emit positions
on the duplicated axis.

> ⚠ Prerequisite ownership: the three release-blockers listed in
> `plans/add-wireframe-generation-module.md > Prerequisites` are upstream of
> this registry. (1) Fill `trade-off-dimensions.md`. (2) Resolve the Density
> duplication. (3) This file's per-pattern-category mappings (covered below).
> The wireframe pipeline is unblocked for the third prerequisite as soon as
> *this* file exists; it is unblocked for the first two as soon as the
> canonical doc is authored and de-duplicated.

**Used by:**
- `framework/agents/blueprint-architect.md` — **sole consumer of Section 3**:
  dimension-applicability filter (§2), the base-pattern-owner / modifier-layering rule
  (§3.0), per-surface pattern-variant selection **at author time** (§3),
  variant-position coherence check (§4), persona-position compatibility check (§5).
  Pattern picks are authored into `variants.json > surface_plan` here — not re-derived
  downstream.
- `framework/assets/wireframes/divergence-heuristics.md` — reuses §2 goal-type
  applicability and §5 persona-trait positions (references, does not re-define them).

> The variant-generator and comparator **no longer read this registry.** Pattern
> selection moved into the architect (`surface_plan`); the generator renders the
> authored plan and the comparator checks render-vs-plan. This removes the prior
> double-interpretation (generator picked from §3, comparator re-derived from §3) that
> produced false-positive drift.

---

## Section 1 — Dimension catalogue (canonical names)

The six canonical dimensions (per `framework/assets/trade-off-dimensions.md`):

| ID | Dimension | Negative pole (-2) | Neutral (0) | Positive pole (+2) | Status |
|---|---|---|---|---|---|
| D1 | speed-accuracy | maximally accurate, slow careful | balanced | maximally fast, error-tolerant | active |
| D2 | power-simplicity | maximally simple, novice-first | balanced | maximally powerful, expert-first | active |
| D3 | density-focus | sparse focus, one-thing-at-a-time | balanced | dense, many-things-at-once | active |
| D4 | control-automation | full manual control | balanced | full automation, opinionated defaults | active |
| D5 | flexibility-consistency | bespoke per-context | balanced | rigidly consistent | active |
| D6 | memorability-discoverability | maximum memorability, terse | balanced | maximum discoverability, verbose | **pending upstream rename** (was: memorability-density) |

> Variant-generators are forbidden from emitting non-neutral positions on D6
> until upstream resolution lands. The architect's self-validation rejects
> any variant carrying `memorability-discoverability != 0` (or, transitively,
> the legacy `memorability-density` key) while the canonical doc still carries
> the duplicated axis name.

---

## Section 2 — Dimension applicability rules

Not every dimension applies to every scope. The architect uses these rules
during the design-brief stage to filter the dimension list it offers the
consultant for variant divergence.

| Dimension | Applies whenever scope's user-goal type ∈ … | Does not apply when … |
|---|---|---|
| D1 speed-accuracy | high-throughput input, batch processing, transactional data entry | scope is read-only browsing / dashboards only |
| D2 power-simplicity | mixed-persona scope (novice + expert in `personas_available`) | scope binds to a single uniform persona on the simplicity-spectrum |
| D3 density-focus | collection-heavy (≥1 table / data-list / dashboard screen) | scope is single-form / single-record only |
| D4 control-automation | scope has system-driven decisions (validation, suggestion, default-fill, approval routing) | scope is pure manual capture with no automation slot |
| D5 flexibility-consistency | scope spans multiple object types or multiple flows | single-flow, single-object scope |
| D6 memorability-discoverability | scope includes ≥1 navigational decision (menu, action surface, command palette) | scope is purely sequential (wizard-only) |

The architect surfaces only applicable dimensions in its consultant prompt;
inapplicable dimensions are still recorded in `variants.json` with
`position: 0` (neutral) for audit trail completeness.

---

## Section 3.0 — Base-pattern ownership & modifier layering

A screen has exactly **one** primary pattern. When more than one diverging dimension
has an effect on the same pattern-category (the common case — `density-focus` and
`speed-accuracy` both touch Collections), they cannot each name a base pattern for the
same screen. Per pattern-category, exactly **one** dimension is the **base-pattern owner**
(it selects `primary_pattern` + `primary_pattern_variant`); every other diverging
dimension layers as a **modifier** (it contributes `modifiers[]` + `secondary_patterns[]`
only, never a competing base pattern).

| Pattern-category | Base-pattern owner | Modifier dimensions express as |
|---|---|---|
| Collections (table / data-list / card-grid / master-detail) | **D3 density-focus** → base pattern + `wf-table--spacious` / `wf-table--compact` | D1 speed-accuracy → confirmation friction, bulk-select (`selectable`), keyboard shortcuts, inline-edit (`editable`); D4 control-automation → auto-defaults / suggestion; D5 flexibility-consistency → shell reuse |
| Forms | **D1 speed-accuracy** → archetype (`multi-step-wizard` ↔ `single-form` ↔ `inline-edit`); **D3 density-focus** → layout variant (`single-form.compact` / `single-form.two-column`) | D2 power-simplicity → help density; D4 control-automation → autofill |
| Navigation / surfaces | **D2 power-simplicity** | D1 speed-accuracy → keyboard-first; D6 (inactive) |

**Rule.** If a modifier dimension's Section-3 effect names a base pattern, re-express it
as a modifier on the owner's base. Forms is the only **two-owner** category — D1 picks the
archetype and D3 picks the layout variant; they decide *different* things and never
conflict (e.g. a `single-form` can simultaneously be `two-column` from D3 and
submit-on-Enter from D1+).

**Consumed at author time.** The blueprint-architect applies this rule once per variant per
surface when it authors `variants.json > surface_plan` (see
`framework/agents/blueprint-architect/steps/step-05-compose-variants.md > 5.3.6`). Every
pattern + variant it names must exist in `framework/assets/pattern-catalogue/` — an absent
pattern routes to the architect's step-07 conditional gate, never to silent drift.

---

## Section 3 — Per-pattern-category HTML effects

This section is the load-bearing translation: for each {dimension, pattern-category, position}
triple, it documents the concrete composition the **blueprint-architect** authors into
`surface_plan` at design time (per Section 3.0's base-owner rule). Each position cell names a
catalogue pattern *variant* (present in that pattern's `variants:` block) or a DS spacing
modifier (`wf-table--spacious` / `wf-table--compact`) — **never** a variant absent from the
catalogue.

Format: rows are `dimension → pattern-category → effect-per-position`.

### D1 speed-accuracy — Collections (modifier — density-focus owns the base)

D1 contributes **modifiers only** on Collections; the base pattern + density variant come
from D3 (Section 3.0). Express D1's position as composition adjustments layered on whatever
base D3 chose — never as a competing base pattern.

| Position | Modifier effect (layered on D3's base) |
|---|---|
| -2 | Explicit confirmation on every row action; no bulk-select; one deliberate action at a time. |
| -1 | Per-row confirm on destructive actions; bulk-select disabled by default. |
|  0 | Standard inline actions; confirm on destructive only. |
| +1 | Keyboard shortcuts for common actions; bulk-select on (`selectable` variant). |
| +2 | Inline-edit (`editable` variant) + `selectable`; auto-apply on focus-blur; minimal confirmation friction. |

### D1 speed-accuracy — Forms

| Position | Effect |
|---|---|
| -2 | `multi-step-wizard`; one decision per page; mandatory review step. |
| -1 | `single-form.scrollable-with-save-bar`; section groups; explicit save bar. |
|  0 | `single-form.default`; field-level validation on-blur. |
| +1 | `single-form.compact`; submit-on-Enter from any field. |
| +2 | `inline-edit`; commit-on-blur; no separate save action. |

### D2 power-simplicity — Forms

| Position | Effect |
|---|---|
| -2 | `multi-step-wizard`; one task per page; constant progress indicator; explicit "next" CTAs. |
| -1 | `single-form.default` with `help-aside` and verbose help text on every field. |
|  0 | `single-form.default`; help text on non-obvious fields only. |
| +1 | `single-form.compact`; keyboard-first; help text on-demand (popover). |
| +2 | `inline-edit` + keyboard shortcuts table; assumes prior knowledge; minimal copy. |

### D2 power-simplicity — Navigation

| Position | Effect |
|---|---|
| -2 | `tabs` or single primary action; no command-palette. |
| -1 | `tabs` + secondary nav surface (sidebar drill). |
|  0 | `tabs` + breadcrumbs. |
| +1 | `tabs` + `command-palette` + keyboard shortcuts. |
| +2 | `omnibar` or `command-palette` as primary entry; tabs collapsed. |

### D3 density-focus — Collections (base-pattern owner)

D3 owns the base pattern + density. All entries are catalogue-real; the density nuance at
±1 is a DS spacing modifier on the default `table`, not a (non-existent) `table.spacious` /
`table.comfortable` catalogue variant. Behavioral variants (`editable`, `selectable`) are
contributed by D1 (the modifier dimension), not here.

| Position | Base pattern + catalogue variant | DS spacing modifier |
|---|---|---|
| -2 | `collections/master-detail-list` `default` — single-record focus, one record per viewport. | — |
| -1 | `collections/table` `default` — roomy rows, whitespace-led. (For visual/browse-oriented collections, `collections/card-grid` `default` is the alternative base.) | `wf-table--spacious` |
|  0 | `collections/table` `default` — standard density. | — |
| +1 | `collections/table` `default` — 5+ visible columns, compact rows. | `wf-table--compact` |
| +2 | `collections/table` `default` — 8+ columns, high information density per viewport. | `wf-table--compact` |

### D3 density-focus — Forms

| Position | Effect |
|---|---|
| -2 | `single-form.default` with one section visible at a time (collapsed others). |
| -1 | `single-form.default`; one column. |
|  0 | `single-form.default`; one column with section groups. |
| +1 | `single-form.two-column`; paired fields side-by-side. |
| +2 | `single-form.compact` + `two-column`; dense field layout; help text suppressed. |

### D4 control-automation — Forms / Validation

| Position | Effect |
|---|---|
| -2 | No autofill; no suggestion; user types every value; validation on-submit only. |
| -1 | Autocomplete on text fields; user accepts/rejects per suggestion. |
|  0 | Standard defaults; field-level validation on-blur. |
| +1 | Smart-default-fill; suggestion preview; user can override. |
| +2 | Aggressive auto-defaults; one-click "fill from previous"; system-suggested confirmation paths. |

### D4 control-automation — Approval / decision surfaces

| Position | Effect |
|---|---|
| -2 | Multiple confirmation gates; type-and-confirm; explicit "reason" field on every decision. |
| -1 | Modal confirmation with required reason. |
|  0 | Modal confirmation, optional reason. |
| +1 | Inline confirm action; optional bulk-decide. |
| +2 | Auto-decide with override window; bulk-approve as default action. |

### D5 flexibility-consistency — Layouts

| Position | Effect |
|---|---|
| -2 | Each scope screen uses a different layout shell tuned to its task. |
| -1 | Two layout shells across the scope. |
|  0 | One primary shell, one secondary shell. |
| +1 | One shell across every screen; section-group reuse. |
| +2 | One shell across every screen; identical section composition; per-screen content variation only. |

### D6 memorability-discoverability — Navigation / Surfaces

| Position | Effect |
|---|---|
| -2 | Terse labels; icon-only chrome where safe (per `GR-17`); keyboard-first. |
| -1 | Short labels; icons paired with one-word labels in primary chrome. |
|  0 | Standard labels; icons paired with text in all chrome. |
| +1 | Verbose labels; explicit tooltips on every action; on-screen hint surfaces. |
| +2 | Verbose labels + always-visible help panels + onboarding tooltips on first visit. |

(Note: D6 mappings are reserved for activation once upstream rename lands.
Until then, variant-generators emit `memorability-discoverability: 0` and
ignore this section's D6 rows.)

---

## Section 4 — Known-incoherent dimension pairs

The architect's self-validation rejects any variant whose dimension positions
fall in these combinations (the configurations are structurally contradictory
and would produce uninhabited or chaotic UIs).

| Pair | Combination | Reason |
|---|---|---|
| D1 × D2 | speed-accuracy +2 AND power-simplicity -2 | Maximum speed + maximum simplicity = stripped wizard with no time to read each step. Wizard fights speed-+2's premise. |
| D2 × D3 | power-simplicity -2 AND density-focus +2 | Novice-first + dense-+2 = novice presented with 8-column table. Discoverability collapses. |
| D3 × D4 | density-focus +2 AND control-automation -2 | Dense view + manual-everything = every cell asks the user to confirm. Cognitive load explodes. |
| D4 × D2 | control-automation +2 AND power-simplicity -2 | Aggressive auto-fill + novice persona = system makes decisions the user doesn't know enough to override. |
| D1 × D4 | speed-accuracy -2 AND control-automation +2 | Maximum accuracy + maximum automation = the system decides while the user demands review. Contradictory. |

The architect surfaces a clear rejection message naming the pair and the
incompatibility; the consultant either adjusts the variant or accepts a
narrower position.

---

## Section 5 — Persona-position compatibility rules

The architect rejects any variant whose dimension positions are hostile to its
bound persona. The rules are deliberately conservative; soft conflicts surface
as warnings, hard conflicts block the variant.

Persona-trait → forbidden position-range (hard reject):

| Persona trait | Forbidden positions | Reason |
|---|---|---|
| occasional / first-time user | D2 power-simplicity ≥ +1 | Expert-first patterns produce worse outcomes for occasional users. |
| occasional / first-time user | D3 density-focus ≥ +1 | High density assumes acclimatised users. |
| occasional / first-time user | D6 memorability-discoverability ≤ -1 | Terse chrome relies on prior memorisation. |
| daily / high-volume user | D2 power-simplicity ≤ -1 | Novice-first patterns waste expert keystrokes. |
| daily / high-volume user | D3 density-focus ≤ -1 | Sparse layouts force more navigation for the same task volume. |
| audit / compliance role | D1 speed-accuracy ≥ +1 | Speed-+ favours throughput over completeness; auditor's goal is opposite. |
| audit / compliance role | D4 control-automation ≥ +1 | Audit demands the human signed off; automation erodes accountability. |

Persona-trait → soft-conflict-range (warn, do not reject):

| Persona trait | Soft-conflict positions | Reason |
|---|---|---|
| daily / high-volume user | D4 control-automation ≤ -1 | Manual-everything is fine for experts but increases per-task time; consultant may have made a deliberate choice. |
| occasional / first-time user | D1 speed-accuracy ≥ +1 | Speed bias may produce error-recovery friction for occasional users. |

Persona traits are extracted by the architect from `requirements.md > §3` per-persona descriptions (e.g. a §3 row labelled "Importer (daily, high-volume)" maps to `daily / high-volume user`).

---

## Anti-patterns

- Do not edit the canonical dimension names in Section 1 to bypass the upstream
  blocker on D6. Either the upstream doc lands a resolved name, or D6 stays
  inactive — there is no third option.
- Do not add new dimensions to Section 1. The canonical vocabulary is governed
  by `framework/assets/trade-off-dimensions.md`; this registry mirrors it.
- Do not loosen the incoherent-pair rules in Section 4 to allow a "creative"
  combination. The rules describe structural contradictions, not stylistic
  taste — easing them produces uninhabited variants.
- Do not loosen the persona-position rules in Section 5 to expand variant
  cardinality. The cardinality cap of 3 is a separate constraint; relaxing
  persona viability just to add a variant degrades the comparison's signal.
- Do not name a pattern or pattern variant in Section 3 / 3.0 that is absent from
  `framework/assets/pattern-catalogue/`. Section 3 is consumed by the
  blueprint-architect **at author time**: a named variant missing from the catalogue's
  `variants:` block is caught when the architect validates `surface_plan` and routes to
  its step-07 conditional gate — it is no longer silently rendered as a fallback that
  later flags as drift. The catalogue is the source of truth; keep this section
  catalogue-true at all times (this is why `table.spacious` / `table.comfortable` /
  `card-grid.spacious` were removed — they never existed in the catalogue). DS spacing
  modifiers (`wf-table--spacious` / `wf-table--compact`) are design-system classes, not
  catalogue variants — they live in `framework/assets/design-systems/wireframe-ds.html`.
