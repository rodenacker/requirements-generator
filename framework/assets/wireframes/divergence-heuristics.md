# Wireframe divergence heuristics

**Role:** asset (wireframe-private; cross-pipeline-reusable by a future `/prototype`).

**Purpose:** Define the deterministic procedure that **extrapolates** how a scope's
wireframe variants should diverge — *which personas* each variant serves, *which
trade-off axis* separates them, and *which information-architecture realizations*
each persona's variant prefers — from the spec's own user goals (`requirements.md`
§4) and persona goal-types (`requirements.md` §3). This replaces a canned
density/speed default with a **recommended default the consultant confirms**: when
the scope's personas pursue materially different goal-types, the recommendation is
to bind each variant to a *different* persona on the axis that best separates them;
when the personas are uniform (or the evidence is too weak to anchor), the
recommendation falls back to the static density/speed default that has always
shipped. The heuristic runs **once**, in `framework/skills/scope-selector.md`, which
persists its output to `scope.json > divergence_profile`. The architect consumes
that profile verbatim and never re-derives it.

**Inherits from:**
- `framework/assets/wireframes/tradeoff-dimensions-registry.md` — §2 user-goal-type
  applicability vocabulary (`high-throughput input`, `batch processing`,
  `transactional data entry`, `read-only browsing`, `navigational`) and the
  dimension applicability rules; §5 persona-trait → forbidden/soft dimension
  positions (`daily / high-volume`, `audit / compliance`, `occasional / first-time`).
  This file **references** those vocabularies and rules; it does not re-define them.
- `requirements/requirements.md` §4 goals-catalogue columns (`Goal statement`,
  `Quality signals`, `Goal kind`, `Layout pref`, `UX-pattern pref`) and §3 persona
  blocks (`Role`, `Expertise`, `Stakes`, `Frequency`, `Driving forces — wants/fears`).
- `framework/assets/wireframes/realization-strategies.md` — the realization closed
  enum `{ standalone-screen, inline-drawer, inline-expand, wizard-split, modal }`
  (`combined` is fast-follow and never recommended here). §4 below maps persona
  goal-types onto preferred/avoided members of this enum.
- `framework/assets/wireframes/position-vocabulary.md` — the plain-English
  `(dimension, position)` labels the scope-selector surfaces in its confirmation
  prompt when it renders a Rule-P recommendation.

**Used by:**
- `framework/skills/scope-selector.md` — **executes** §1–§4 below (its new Step 3.5)
  to produce the in-memory `divergence_profile`, then surfaces it behind the Step-4
  confirmation gate and persists the confirmed result to `scope.json`.
- `framework/agents/blueprint-architect.md` — **references the fallback contract**
  only: its step-05 resolves the divergence profile by precedence
  `scope.json > dimension_override` → `scope.json > divergence_profile` →
  `framework/assets/wireframes/domain-defaults.md`. When `divergence_profile` is
  absent/null/`static-default`, the architect uses `domain-defaults.md` exactly as
  it does today — this file's Rule D / Rule W is what *recommends* that fallback.
  The architect maps each binding's abstract `pole` onto concrete dimension
  positions per the registry's §3; it does not consume §1–§4 of this file directly.

---

## Section 1 — Goal-type inference (per in-scope goal)

For each in-scope goal `G-NN` — the goals in `scope.sources.goals` **plus** any goal
reached by an in-scope task-flow or story (a task-flow / story names its goal via
`→ §4.1 G-NN`) — classify the goal into exactly one **goal-type** from the registry
§2 vocabulary: `high-throughput input`, `batch processing`, `transactional data
entry`, `read-only browsing`, or `navigational`.

The classification is **first-hit-wins** down the ordered rule list. **Every hit
cites the verbatim text that triggered it** (the cell value, the goal-statement
phrase, or the persona-wants phrase), so the recommendation is auditable and a
missing anchor cleanly degrades to Rule W (§3).

1. **Explicit preference cell.** If the goal's `UX-pattern pref` cell is non-empty,
   map its verbatim text to a goal-type (e.g. "bulk-edit table" → `batch
   processing`; "single-record form" → `transactional data entry`). Else if the
   `Layout pref` cell is non-empty, map it the same way. Cite the cell verbatim.
   *(In the worked spec both columns are `—` for every goal, so this rule never
   fires there and classification falls to rule 2.)*

2. **Goal-kind + goal-statement verbs.** Read the goal's `Goal kind` and the verbs
   in its `Goal statement`. Map first-matching verb-class:
   - import / upload / enter / capture / submit → `high-throughput input` (or
     `transactional data entry` when the goal-statement stresses one-record-at-a-time
     correctness over volume).
   - approve / reject / audit / decide / judgement / sign-off → `transactional data
     entry` **with an audit overlay** (the decision is per-record and accountability-
     bearing; the registry §5 `audit / compliance role` rules apply to the persona
     that pursues it).
   - view / visibility / locate / search / export / browse / review → `read-only
     browsing`.
   - filter / navigate / find-across / drill → `navigational`.
   Cite the matched verb(s) from the goal statement verbatim.

3. **Linked-persona wants (last resort).** If neither the preference cells nor the
   goal-statement verbs disambiguate, classify from the verbs in the linked persona's
   §3 "Driving forces — wants" line (the persona that owns the story/flow reaching
   this goal). Cite the wants-phrase verbatim. If even this yields no anchor, the
   goal contributes **no** evidence and the persona that owns only such goals is a
   weak-evidence persona (feeds Rule W in §3).

**Worked example (this spec's in-scope goals).**

| Goal | First-hit rule | Verbatim anchor | Goal-type |
|---|---|---|---|
| G-01 Successfully import transaction files | rule 2 (verb "import") | "Successfully import transaction files for downstream approval" | `high-throughput input` |
| G-02 Maintain control over which transactions are approved / rejected | rule 2 (verbs "approved", "rejected", "with reason") | "Maintain control over which transactions are approved and which are rejected with reason" | `transactional data entry` + audit overlay |
| G-03 Provide visibility into file processing status | rule 2 (verb "visibility") | "Provide visibility into file processing status and per-file outcomes" | `read-only browsing` |
| G-04 Export decided transactions | rule 2 (verb "export") | "Export decided transactions for downstream processing and reconciliation" | `read-only browsing` |
| G-05 Locate transactions and files quickly | rule 2 (verbs "locate", "filter/search" in quality signals) | "Locate specific transactions and files quickly across the working set" | `navigational` |

---

## Section 2 — Persona goal-type assignment

For each persona name in `scope.json > personas_available`, derive a tuple
`(frequency, expertise, role, dominant-goal-type)`.

- `frequency`, `expertise`, `role` are extracted using **the architect's existing
  trait-extraction vocabulary** — see `framework/agents/blueprint-architect/steps/step-02-read-inputs.md > 2.4`
  (`frequency ∈ {daily | weekly | occasional | first-time}`, `expertise ∈ {novice |
  intermediate | expert}`, `role ∈ {operator | reviewer | approver | auditor | viewer
  | admin}`). Do **not** re-define this vocabulary here; reuse it verbatim so the
  scope-selector and the architect read personas identically.
- `dominant-goal-type` is the goal-type (from §1) of the goals this persona owns
  (via §4.2 stories / §5 flows whose actor is this persona). When a persona owns
  goals of several goal-types, the **dominant** one is the goal-type covering the
  most owned goals; ties break toward the type that carries an audit overlay (audit
  accountability dominates throughput when both are present, per registry §5's
  hard-reject asymmetry for the `audit / compliance role`).

**Worked example (this spec's two personas).**

| Persona | frequency | expertise | role | Owned goals (goal-types) | Dominant goal-type |
|---|---|---|---|---|---|
| Importer | daily | operational (→ `intermediate`) | operator | G-01 (`high-throughput input`), G-03 / G-05 (browsing / navigational) | **`high-throughput input`** |
| Approver | daily | financially-literate (→ `expert`) | approver / auditor | G-02 (`transactional data entry` + audit), G-04 (`read-only browsing`), G-05 (navigational) | **`read-only browsing` + audit** |

Note that **both personas are `daily`** in this spec, so a *frequency*-only split
would not separate them. The separation comes from the **dominant goal-type** (the
Importer's throughput-input vs the Approver's read-and-judge-under-audit), which §3
turns into a binding recommendation, and §3 then picks the dimension axis that puts
those two goal-types at opposite, registry-§5-compatible poles.

---

## Section 3 — Divergence decision

Apply exactly one rule. Each produces the in-memory `divergence_profile` the
scope-selector persists.

### Rule P — persona divergence (the goal-driven recommendation)

**Fires when:** ≥ 2 personas in `personas_available` have **dominant goal-types that
differ across a registry-§2 axis class** (e.g. one persona is `high-throughput
input` and another is `read-only browsing` / `transactional data entry` + audit) AND
§1 produced ≥ 1 verbatim anchor for each of those goal-bearing personas.

**Recommendation:**
- Bind **each variant to a different persona** (`cardinality = #distinct
  goal-bearing personas`, hard cap 3 — if more than 3 personas qualify, keep the 3
  whose dominant goal-types are most polar-separable and record the drop in the
  binding rationale).
- Choose the **separating axis** as the single dimension that **maximises compatible
  polar distance** between the bound personas under registry §5: pick a dimension on
  which the two personas' goal-types push to *opposite poles* AND **neither pole
  hits a §5 hard-reject** for its persona. This deliberately avoids merely pinning the
  audit persona to neutral — choose an axis where the audit/browsing persona has a
  *negative* pole it can legitimately occupy, not just `0`.
  - Worked example: with Importer (`high-throughput input`, daily/expert-leaning) vs
    Approver (`read-only browsing` + audit, daily/expert), **`density-focus` (D3)**
    is the separating axis: Importer → `+` (dense, scan-and-act on a high-volume
    table — registry §5 permits `daily/high-volume` at high density) and Approver →
    `-1` (spacious / one-record-at-a-time review — compatible with an auditor who
    reads each record deliberately, and *not* a §5 hard-reject). `speed-accuracy`
    (D1) is a poor separating axis *here* because §5 hard-rejects `audit / compliance
    role` at `D1 ≥ +1`: the Approver could only sit at `0`/`-`, so D1 cannot put the
    two personas at genuinely opposite compatible poles. (When a future spec pairs a
    throughput operator against a *first-time* persona, D1 or D2 may instead be the
    best separating axis — the rule is "max compatible polar distance", not a fixed
    axis.)
- `evidence_strength: "strong"`, `source: "recommended-confirmed"` (set by the
  scope-selector once the consultant accepts).
- Populate `variant_bindings[]`: one per persona, each carrying `persona`,
  `persona_goal_type`, the abstract `pole` (`"power"` for the high-throughput /
  dense side, `"careful"` for the spacious / audit side, `"mixed"` only when a
  persona genuinely straddles), a one-line `rationale`, and an `evidence[]` array of
  the verbatim `§3 …` / `§4 …` anchors that justified the binding.
- Populate `realization_recommendation` per §4 below, keyed by each bound persona's
  dominant goal-type.

### Rule D — static default (uniform personas)

**Fires when:** Rule P does not fire because the personas' dominant goal-types do
**not** differ across a registry-§2 axis class (uniform-goal-type scope, or a single
persona).

**Recommendation:** today's static default — diverge on `density-focus` +
`speed-accuracy`, `cardinality = 2`, persona binding + polar positions per
`framework/assets/wireframes/domain-defaults.md` (Sections 1–4). `evidence_strength:
"strong"` (the uniformity itself is well-evidenced), `source: "static-default"`.
`variant_bindings[]` mirror the domain-defaults `CAREFUL-DEFAULT` / `POWER-DENSE`
split; `realization_recommendation` may be omitted (the architect uses each
surface's `default_realization`) or populated from §4 keyed by the uniform goal-type.

### Rule W — weak evidence (fail-safe to static)

**Fires when:** §1 could **not** cite ≥ 1 verbatim anchor for at least one
goal-bearing persona (e.g. the persona owns only goals that fell through all three
§1 rules with no anchor). Rule W also catches the case where the personas *look*
divergent but the divergence rests on un-anchored inference.

**Recommendation:** identical to Rule D's static default, but tagged
`evidence_strength: "weak"`, `source: "static-default"`. The weak tag is the signal
the scope-selector renders in its confirmation prompt ("static default — goal
evidence weak/uniform") so the consultant knows the recommendation is a fallback,
not a goal-extrapolated divergence. **Weak evidence MUST resolve to the static
default** — never emit a Rule-P persona-divergence on weak evidence.

---

## Section 4 — Realization recommendation

Map each bound persona's **dominant goal-type** onto preferred / avoided members of
the realization enum (`framework/assets/wireframes/realization-strategies.md` §1).
This populates `divergence_profile.realization_recommendation["<goal-type>"] = {
prefer: [...], avoid: [...] }`; the architect intersects it with each surface's
`allowed_realizations` when it picks a per-surface realization at step-05.

| Persona goal-type cluster | Prefer | Avoid | Why |
|---|---|---|---|
| `high-throughput input` / expert / daily | `inline-drawer`, `inline-expand`, `modal` | `wizard-split` | Consolidated, fewer page loads — a high-volume operator wants detail/edit in place, not a multi-screen detour. |
| `read-only browsing` + audit / occasional / first-time | `standalone-screen`, `wizard-split`, `modal` | `inline-expand` | Decomposed, one-thing-at-a-time — an auditor (or an occasional user) reviews each record on its own surface, with deliberate steps. |

Notes:
- `combined` is **never** recommended (fast-follow per realization-strategies.md §1;
  the architect must not emit it in the first wave regardless).
- `standalone-screen` is always implicitly allowed (the baseline); the `prefer` /
  `avoid` lists only *bias* the architect's pick within each surface's
  `allowed_realizations` — they never force a realization a surface does not allow.

---

## Section 5 — Reuse contract

- This file **defines no new dimension names.** Every separating axis named in §3 is
  a canonical dimension from `tradeoff-dimensions-registry.md > Section 1`
  (`density-focus`, `speed-accuracy`, `power-simplicity`, `control-automation`,
  `flexibility-consistency`; `memorability-discoverability` stays inactive).
- This file **defers concrete polar positions to the registry's §3.** §3 above emits
  an abstract `pole` (`"careful"` / `"power"` / `"mixed"`) per binding; the
  blueprint-architect maps `pole` → concrete `-2..+2` `dimension_positions` per
  `tradeoff-dimensions-registry.md > Section 3` and validates them against §4
  (incoherent pairs) and §5 (persona compatibility). The heuristic chooses *which
  axis and which side*; the architect chooses *how far along the axis*.
- The realization enum in §4 is exactly the closed enum from
  `realization-strategies.md` §1 — no realization name is invented here.

---

## Anti-patterns

- Do not define a new dimension name. Separating axes are canonical registry §1
  dimensions only; inventing an axis breaks the architect's `dimension_positions`
  contract.
- Do not emit a recommendation without verbatim evidence. Every goal-type
  classification (§1) and every Rule-P binding (§3) cites the verbatim cell /
  goal-statement / persona-wants text that triggered it. An un-anchored binding is a
  Rule-W weak-evidence case, not a strong recommendation.
- Do not emit a Rule-P persona-divergence on weak evidence. Weak evidence MUST fall
  back to Rule D's static default with `evidence_strength: "weak"`.
- Do not bind both variants to the same persona when Rule P fires. Rule P's premise
  is that distinct personas pursue distinct goal-types; collapsing them to one
  persona discards the very signal that fired the rule.
- Do not pick a separating axis that pins the audit / occasional persona to neutral
  when a compatible *opposite-pole* axis exists. The goal of "max compatible polar
  distance" is a genuinely divergent comparison, not a one-sided one.
- Do not pick a separating axis whose pole hits a §5 hard-reject for either bound
  persona (e.g. `speed-accuracy ≥ +1` for an `audit / compliance role`). Compatible
  polar distance is bounded by registry §5; a hard-reject pole is not "distance", it
  is an invalid variant.
- Do not surface the recommendation silently. The recommendation is always rendered
  behind the scope-selector's Step-4 confirmation gate; the consultant accepts,
  edits scope, edits dimensions (which supersedes the recommendation), or cancels.
  The heuristic never writes a divergence profile the consultant did not see.
- Do not re-run this heuristic in the architect. It executes once, in the
  scope-selector; the architect consumes `scope.json > divergence_profile` verbatim.
