# Wireframe domain-default dimension profile

**Role:** asset (wireframe-private; cross-pipeline-reusable by a future `/prototype`).

**Purpose:** Provide the canonical default trade-off configuration the
`blueprint-architect` applies when the consultant gives intent only (the happy
path of the simplified `scope-selector` flow). Without a known-good default,
the architect would have to guess from scratch on every run; with it, the
architect produces a defensible `variants.json` deterministically and only
re-decides when the consultant explicitly overrides at scope-selector's
confirmation step.

**Domain locked.** Per `CLAUDE.md > Constraints > Target domain`, this project
targets **internal data-management productivity apps** (CRUD-heavy, mixed-persona
workforce tools). Every constant in this file is keyed to that domain. Do not
edit these defaults to suit a marketing or content-app run — fork the file
under a new pipeline-specific defaults asset instead.

**Inherits from:**
- `framework/assets/wireframes/tradeoff-dimensions-registry.md` (canonical
  dimension vocabulary + applicability rules + persona-position compatibility).
- `framework/shared/general-rules.md` (`GR-NN` deterministic defaults).

**Used by:**
- `framework/skills/scope-selector.md` — surfaces the default dimensions in its
  confirmation prompt so the consultant sees what the architect will do; the
  consultant's `Edit dimensions` affordance lets them override before the
  architect runs.
- `framework/agents/blueprint-architect.md` — reads this file in its variant
  composition step; applies the defaults unless `scope.json > chosen_dimensions`
  records a consultant override.
- `framework/assets/wireframes/divergence-heuristics.md` — references this file as
  the **Rule-D / Rule-W fallback**: when the scope's personas are uniform-goal-type
  (Rule D) or the goal evidence is too weak to anchor (Rule W), the heuristic
  recommends exactly the static profile defined here, and the architect applies it.

---

## Section 1 — Default diverging dimensions

> **Precedence note.** When `scope.json > divergence_profile` is present and in force
> (a goal/persona-driven recommendation the consultant confirmed via the
> scope-selector — see `framework/assets/wireframes/divergence-heuristics.md`), the
> architect uses **that** profile instead of these static defaults. This file is the
> **Rule-D / Rule-W fallback** the heuristic recommends when the personas are
> uniform-goal-type or the goal evidence is too weak to anchor. The static content
> below remains the canonical fallback — do not move or delete it.

The architect diverges variants on **exactly these two dimensions** by default:

| Rank | Dimension ID | Dimension name | Why default for this domain |
|---|---|---|---|
| 1 | D3 | density-focus | Every internal-productivity scope has a CRUD / table / data-list surface. `D3` always applies (per `tradeoff-dimensions-registry.md > Section 2`) whenever the scope contains ≥1 collection screen, which is true for ~all scopes in this domain. D3 produces the most visually-divergent variants (sparse master-detail vs dense 8-column table). |
| 2 | D1 | speed-accuracy | Internal productivity work is throughput-oriented. The "careful default vs power-user speed" axis is the single most consequential decision for daily operators in this domain. `D1` applies whenever the scope contains ≥1 input / capture screen, which is true for most scopes. |

**Why not the others** (recorded so future-you can revisit without re-deriving):

- `D2 power-simplicity` — applies only when `personas_available` spans both
  novice and expert traits. Many internal-tool scopes bind to a uniform persona
  (the team using the tool), so D2's applicability is contingent. The default
  profile must be applicability-safe, so D2 is reserved for the fallback chain.
- `D4 control-automation` — applies only when the scope has system-driven
  decisions (validation/routing/auto-fill). Common but not universal; in the
  fallback chain rather than the default.
- `D5 flexibility-consistency` — applies only when the scope spans multiple
  object types or flows. Many wireframe scopes are single-flow; in the
  fallback chain.
- `D6 memorability-discoverability` — inactive (pending upstream rename per
  `tradeoff-dimensions-registry.md > Section 1`).

---

## Section 2 — Default cardinality

**2 variants.** Two is the right number for a comparison view: stakeholders
see "this or that", not "this or this or this or that". The cardinality cap of
3 (per the architect's existing self-validation) remains in place; the
consultant raises cardinality via the scope-selector's `Edit dimensions`
affordance, never automatically.

---

## Section 3 — Default polar positions per variant

The architect emits these positions unless overridden. Both variants diverge
on `D3` and `D1`; all other dimensions sit at `0` (neutral) for audit-trail
completeness.

### Variant A — `CAREFUL-DEFAULT` (the conservative variant)

| Dimension | Position | Plain-English meaning |
|---|---|---|
| D3 density-focus | -1 | Spacious — whitespace-led, one section visible at a time |
| D1 speed-accuracy | -1 | Accuracy-leaning — more confirmation, careful pace |
| D2..D5 | 0 | Neutral |

Bound by default to occasional / first-time persona traits when both
persona types exist (see Section 4).

### Variant B — `POWER-DENSE` (the expert variant)

| Dimension | Position | Plain-English meaning |
|---|---|---|
| D3 density-focus | +2 | Dense — 8+ columns, inline-edit enabled, high information per viewport |
| D1 speed-accuracy | +1 | Speed-leaning — keyboard-first, fewer guardrails |
| D2..D5 | 0 | Neutral |

Bound by default to daily / high-volume persona traits when both
persona types exist (see Section 4).

**Polar-position rationale.** The two variants sit on opposite sides of both
default dimensions (`A: D3-1/D1-1`, `B: D3+2/D1+1`). This maximises visual
divergence on the variants-side-by-side landing — the consultant sees the
trade-off rendered, not just described. The positions also pass the
incoherent-pair check in `tradeoff-dimensions-registry.md > Section 4`
(neither `D1+2/D2-2` nor `D2-2/D3+2` is reached).

---

## Section 4 — Persona-binding rule

> **Precedence note.** When `scope.json > divergence_profile` is present and in force
> (see `framework/assets/wireframes/divergence-heuristics.md`), its
> `variant_bindings[]` supply the persona-binding directly and the architect uses
> them instead of the rules below. This section is the **Rule-D / Rule-W fallback**
> binding rule the heuristic recommends for uniform-goal-type or weak-evidence
> scopes; it remains the canonical fallback — do not move or delete it.

The architect bind variants to personas using these rules (in order; first
match wins).

1. **If `personas_available` contains a persona whose §3 description matches
   any of {`occasional`, `first-time`, `infrequent`, `new-user`} AND a persona
   whose §3 description matches any of {`daily`, `high-volume`, `power-user`,
   `expert`}**: bind `CAREFUL-DEFAULT` → the occasional persona, `POWER-DENSE`
   → the daily persona.
2. **Else if `personas_available` contains exactly one persona**: bind both
   variants to it.
3. **Else (mixed personas but no clear occasional/daily split)**: bind both
   variants to the first persona alphabetically. Surface a non-blocking note
   in the architect's handback summary so the consultant knows persona
   binding fell back.

The architect's existing persona-position compatibility check
(`tradeoff-dimensions-registry.md > Section 5`) runs after binding. If
either default variant's positions are *hard-rejected* for its bound persona
(e.g. occasional + `D3 ≥ +1` is a hard reject), the architect substitutes via
the fallback chain in Section 5 below.

---

## Section 5 — Fallback chain (when defaults don't apply)

The architect runs `tradeoff-dimensions-registry.md > Section 2` applicability
rules against the scope. If `D3` is inapplicable (scope has no collection
screen) OR `D1` is inapplicable (scope is read-only browsing only), substitute
in this order:

| Substitute order | Dimension | Substitutes when |
|---|---|---|
| 1 | D4 control-automation | `D1` is inapplicable AND scope has system-driven decisions |
| 2 | D2 power-simplicity | `D1` or `D3` is inapplicable AND `personas_available` contains both novice and expert traits |
| 3 | D5 flexibility-consistency | A primary default is inapplicable AND scope spans multiple object types |

After substitution, the architect re-derives polar positions for the new
dimension by reading `tradeoff-dimensions-registry.md > Section 3`'s per-pattern
effects and picking the most visually-divergent pair (typically `+2` and `-1`
or `+1` and `-2`). The substitution is recorded in the architect's handback
summary as a non-blocking note.

If after substitution fewer than two applicable dimensions remain, the
architect surfaces its existing conditional gate (per
`framework/agents/blueprint-architect/steps/step-07-handback.md`) and asks the
consultant whether to (a) accept a single-dimension comparison, (b) narrow
scope, or (c) cancel.

---

## Anti-patterns

- Do not edit Sections 1–3 to suit a one-off scope. The defaults are derived
  from the domain lock in `CLAUDE.md`; per-scope tuning happens at
  scope-selector's `Edit dimensions` affordance, not in this file.
- Do not add new dimensions to Section 1. The canonical vocabulary is
  governed by `tradeoff-dimensions-registry.md > Section 1`.
- Do not promote `D6 memorability-discoverability` into the default profile
  until the upstream rename in `tradeoff-dimensions-registry.md > Section 1`
  resolves.
- Do not change Variant A / Variant B `variant_id` slugs without updating
  `framework/agents/blueprint-architect.md` — the slugs are referenced by the
  architect when authoring `variants.json` from defaults.
- Do not loosen the persona-binding rule in Section 4 to skip the
  compatibility check at Section 5 of the registry. Hard rejects remain hard.
