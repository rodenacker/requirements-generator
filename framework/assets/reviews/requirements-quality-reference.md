<!-- ROLE: asset (review reference). Loaded by framework/agents/reviews/requirements-quality-reviewer.md at activation. -->

# reviews/requirements-quality-reference.md

**Purpose:** Methodology reference for the **Requirements Quality** review of every ID-bearing requirement in `requirements/requirements.md`. The reviewer scores each requirement against the **nine ISO/IEC/IEEE 29148:2018 individual well-formedness characteristics**, runs the **five set-level characteristics** as a document-level pass, and — for the ambiguous and compound requirements — proposes **EARS-form rewrites**. The reviewer follows this document literally and exhaustively.

**Used by:**

- `framework/agents/reviews/requirements-quality-reviewer.md` — drives enumeration, per-requirement nine-characteristic scoring, the set-level pass, the GR/PI rescue, the fix-list/EARS construction, validate, render, and write workflow.

**Output produced by the reviewer:** `review-requirements/REQUIREMENTS-QUALITY/requirements-quality.html` — a self-contained HTML document structured as follows (section order fixed):

0. **In plain terms** — 2–5 plain-English sentences: what this review is, what it found (verdict + tier counts), and what the consultant should do next. A faithful condensation — no finding or count not in the punch-list below; severity preserved verbatim (a BLOCKED verdict is stated as plainly in the lead as in the findings). Jargon glossed at first use (verdict, risk tier, decidable characteristic, judgment band, EARS). The *one* sanctioned narrative paragraph; everything below is a punch-list.
1. **Executive summary** — verdict banner, per-characteristic failure tally, tier distribution, set-level tally, judgment-band tally.
2. **Scorecard heatmap** — the requirement × characteristic heatmap diagram (diagrams-first ordering).
3. **Per-requirement scorecard** — one row per ID-bearing requirement.
4. **Fix list (EARS rewrites)** — one card per Red/Yellow requirement.
5. **Set-level register** — the five 29148 set-level characteristics + GTWR redundancy extension.
6. **Judgement-fence note** — decidable/judgment split + ID-scope exclusion + FIRST-PRINCIPLES pointer.
7. **Diagnostics** — ten quality gates, rescue log, drift fingerprints, override log.

The scaffold for the artefact is `framework/assets/reviews/template-requirements-quality.html`.

---

## What "Requirements Quality Review" means

ISO/IEC/IEEE 29148:2018 (*Systems and software engineering — Life cycle processes — Requirements engineering*, superseding IEEE 830-1998) defines a **fixed rubric** for a well-formed requirement: nine characteristics each requirement should satisfy, and five characteristics the requirement *set* should satisfy. This review applies that rubric **mechanically and per-requirement**: every requirement gets the same nine checks, the same way, so the result is reproducible and auditable — the same document scored twice yields the same scorecard.

The lens's load-bearing honesty is the **decidability split**. Five of the nine characteristics are *mechanically decidable from the requirement text alone* (a closed dictionary, a clause count, a template-conformance grep, a measurable-anchor test); four genuinely require **domain or stakeholder knowledge** and cannot be decided from the document — the empirical literature reports only fair-to-moderate inter-rater agreement on them (Cohen's κ ≈ 0.45–0.75). The review **leads with the five decidable characteristics** (scored pass/fail with a citable rule ID + verbatim evidence) and **fences the four judgment characteristics** in a separate, lower-confidence band (`likely-pass | concern | not-doc-decidable` — never pass/fail). It never reports a single blended "conformance %"; the literature documents that as a vanity-metric / false-precision trap.

Where a requirement fails *Unambiguous* or *Singular*, the lens is **constructive**: it proposes an EARS-form rewrite (split the compound; replace the flagged term), under a strict anti-fabrication rule — a rewrite that would invent a value the document does not state is rendered as a placeholder flagged `confirm`, never a fabricated number.

### How this differs from the other `/review-requirement` lenses

| Lens | Stance | What gets surfaced | Instrument |
|---|---|---|---|
| **adversarial** | *"What is wrong with what's written?"* | Defects across the whole doc, found freeform. | Eight freeform defect lenses. |
| **first-principles** | *"Does each artefact need to exist given the stated business reality?"* | Weak justification chains; orphans; collective-coherence gaps. | Per-subject defensibility audit. |
| **ten-ba-questions / ten-ux-questions** | *"What's missing for a BA / designer?"* | Stakeholder / designer questions. | Top-ten gap list. |
| **user-stories** | *"Which §4.2 stories are not yet good stories?"* | Story-craft defects. | Six story-quality criteria. |
| **requirements-quality** | *"Is each requirement well-formed against ISO 29148?"* | Per-requirement well-formedness defects scored on a fixed nine-characteristic rubric + EARS rewrites. | **Fixed per-requirement conformance scorecard + risk tiers.** |

A doc can be **adversarially clean** and **first-principles defensible** and still be **quality-poor** — every requirement justified and contradiction-free, yet compound, ambiguous, or untestable in its wording. This lens is the only one that applies a *stable, reproducible, per-requirement rubric* and hands back repaired text. Its single overlap point is **Necessary** (≈ first-principles' Q1); the lens handles this by reducing Necessary to a thin doc-trace shadow that explicitly **defers the full business-defensibility audit to FIRST-PRINCIPLES** (see C1 below).

---

## Sources and defensibility

- **ISO/IEC/IEEE 29148:2018** — the nine individual + five set-level characteristics. The authoritative rubric this lens scores against. Supersedes IEEE 830-1998 (which had eight characteristics — correct, unambiguous, complete, consistent, ranked, verifiable, modifiable, traceable; 29148 added *necessary, appropriate, singular, feasible, conforming* and moved ranked/modifiable/traceable to process/metadata attributes).
- **INCOSE *Guide to Writing Requirements* (GTWR) v4, 2023** — the citable rule backbone beneath the decidable cells. ~40+ rules across the categories *Accuracy, Concision, Non-ambiguity, Singularity, Completeness, Realism* (plus Conditions / Uniqueness / Abstraction), each mapping onto a 29148 characteristic.
- **EARS — Easy Approach to Requirements Syntax** (Mavin, Wilkinson, Harwood, Novak, RE'09; "Big Ears", RE'10) — the rewrite grammar. Also the project's house syntax for §6.1/§6.2 acceptance criteria (GR-23), which makes *Conforming* and the rewrite target the project's own mandated grammar, not an imported one.
- **Femmer, Fernández, Wagner, Eder — "Requirements Smells"** (*Journal of Systems and Software*, 2017) — the lexically-detectable smell catalogue (vague adjectives/adverbs, vague verbs, comparatives/superlatives, loopholes, vague pronouns, implied-multiple) behind the *Unambiguous* and *Singular* decision procedures; their *Smella* tool demonstrated >85% detection precision on these smells.
- **NASA Automated Requirements Measurement (ARM)** — Wilson, Rosenberg, Hyatt — the imperatives / weak-phrases / options / continuances / directives quality indicators; ~90% precision on imperative/weak-phrase detection.
- **Berry, Kamsties & Krieger — *Ambiguity Handbook*** — the five-category linguistic ambiguity taxonomy (lexical / syntactic / semantic / pragmatic / vagueness) that frames the *Unambiguous* dictionary buckets.
- **QuARS** (Lami, Gnesi, Fabbrini et al.) and **Génova et al.** — corroborating tool evidence that atomicity, vagueness, and weak-phrase checks are automatable at ≈80–90% agreement with expert assessment.
- **Carson (INCOSE IS 2015)** — graded-quality assessment + the finding that *verifiability* is foundational: where a requirement has no measurable verification criterion, judgments of necessity, feasibility, and correctness reduce to opinion. This is the empirical basis for the decidability split.

The synthesis is this reference's contribution: take the 29148 rubric, bind each *decidable* characteristic to a lexical/syntactic detection procedure with a citable rule backbone (GTWR + Femmer + ARM), and **fence the judgment characteristics honestly** rather than fake a hard verdict on a κ≈0.5 judgment — leading with what a document-only reviewer can decide at 80–95% precision, and being explicit about what it cannot.

---

## Scope: what gets scored

The scorecard rows are the **ID-bearing, individually-addressable requirements**:

- **G-NN** — §4.1 Goals catalogue.
- **F-NN** — §6.1 Functional requirements.
- **BR-NN** — §6.2 Business rules.
- **UI-NN** — §6.4 UI feature needs.
- **RPT-NN** — §6.7 Reporting feature needs (if present).
- **NT-NN** — §6.8 Notification points (if present).

Use the document's own IDs. Each scorecard row record carries `{req_id, req_type, anchor, statement, ac_cell, priority, raw_position}`.

**Excluded from per-requirement scoring (assessed only in the set-level pass):**

- **§6.3 Validation rules** — already EARS-by-construction per GR-23 (the `Rule → Error message` pairing); no formal ID; field-centric rows. Applying *Conforming* to them is vacuous.
- **§6.5 Access control (RBAC)** — a roles × resources matrix; cells are permission tokens, not *shall*-statements.
- **§6.6 NFR** (Session UX, FE performance, Compliance UI, Accessibility) — bulleted, no formal ID.

Forcing nine cells onto a matrix cell or a bullet manufactures false precision. These sections are still read and assessed at the **set-level pass** (consistency, comprehensibility, validatability). The exclusion is disclosed in the artefact's `judgement-fence note` and recorded in diagnostics as `id_scope_excluded`. This mirrors the first-principles reviewer's "do not score §1/§3/§5" scope discipline.

Other sections (§1 context, §2 domain, §3 personas, §5 task flows, §7 data shapes) are **upstream context the reviewer reads but does not score** — they supply the trace targets for the *Necessary* doc-trace shadow and the set-level Complete/Comprehensible passes.

---

## The decidability split (the load-bearing design axis)

| Band | Characteristics | Verdict vocabulary | Confidence | Basis |
|---|---|---|---|---|
| **DECIDABLE** | C5 Singular · C3 Unambiguous · C9 Conforming · C7 Verifiable · C4 Complete-structural | `pass \| fail \| N/A` | high (≈80–95%) | mechanical: closed dictionary, clause count, GR-grep, measurable-anchor test, TBD/dangling-ref scan |
| **JUDGMENT** | C1 Necessary · C2 Appropriate · C8 Correct · C6 Feasible | `likely-pass \| concern \| not-doc-decidable` | moderate (κ≈0.45–0.75) | requires domain/stakeholder knowledge; fenced, never asserted as a hard fail |

The five decidable characteristics are the first column-group of the heatmap; the four judgment characteristics are a visually-separated second group rendered in a muted band. **Risk tiers and the per-characteristic fail tally are computed from the decidable band only** — a judgment `concern` never changes a requirement's tier and never enters the fail tally.

---

## The nine individual characteristics

Each procedure is applied to one requirement's `{statement, ac_cell, req_type, priority}`. A decidable `fail` MUST carry (a) a rule code from the closed list below, and (b) a **verbatim offending-phrase quote** that exists in the Step-2 quote index (anti-fabrication, gate-enforced). A judgment band MUST carry a doc-internal observation (an anchor or an internal contradiction), never a freelance opinion.

### C5 — Singular *(DECIDABLE)*

**ISO:** states a single capability/constraint, not multiple combined.

**Procedure.** Tokenise the statement. **FAIL** if it contains:

- a coordinating conjunction (`and`, `as well as`, `also`, `plus`, `; and`) joining ≥2 independent *shall*-able predicates (`RQ-SING-conjunction`); or
- an enumerated list of separable capabilities (`shall X, Y, and Z` where X/Y/Z are distinct capabilities) (`RQ-SING-enumeration`); or
- multiple distinct verbs each expressing a separate system response (`RQ-SING-multiverb`).

**Not a fail:** a conjunction inside one noun-phrase object (`name and address` = one field set), or inside an EARS precondition (≤3 preconditions per GR-23 is one trigger, not two requirements). When genuinely unclear whether a conjunction joins capabilities or noun-phrase parts, **FAIL as `RQ-SING-compound-suspect`** (conservative — a split proposal is cheap). **N/A** never.

**Backbone:** GTWR Singularity category; Femmer "implied multiple requirements" smell.

### C3 — Unambiguous *(DECIDABLE)*

**ISO:** can be interpreted in only one way.

**Procedure.** Scan the statement and AC against the **closed weak-phrase dictionary** below (verbatim, append-only — the agent does NOT freelance "this feels vague"; only listed terms fire, exactly as the GR-20 blocklist is a closed alternation). **FAIL** on ≥1 hit; cite the hit term + bucket + rule code.

- **Vague adjectives / adverbs** (`RQ-AMB-vague-term`): `fast, slow, quick, quickly, easy, easily, user-friendly, intuitive, intuitively, efficient, efficiently, flexible, robust, seamless, seamlessly, scalable, appropriate, appropriately, reasonable, reasonably, sufficient, adequate, adequately, acceptable, graceful, gracefully, simple, smooth, modern, recent, soon, timely, f?ast enough, several, some, many, few, most, minimal, optimal, state-of-the-art`.
- **Loophole / escape clauses** (`RQ-AMB-loophole`): `as appropriate, as needed, where appropriate, where feasible, where possible, if possible, if practical, if necessary, to the extent possible, normally, generally, typically, etc., and so on, including but not limited to, such as, may (as permission), might, could (as permission), support for, capable of, be able to`.
- **Comparatives / superlatives without a baseline** (`RQ-AMB-comparative`): `better, better than, faster than, as good as, best, worst, most important, highest, maximise, minimise, optimise, improved` — when no measurable baseline/threshold is given.
- **Unresolved referents** (`RQ-AMB-pronoun`): `it, this, that, these, those, they` used when the statement names ≥2 candidate antecedent nouns.

**Not a fail:** a flagged word inside a `[STANDARD-RULE: GR-NN]`-tagged value (the rule fixes the meaning), or a bounded quantifier whose scope the doc closes (`all required fields` where the required set is defined). **N/A** never.

**Backbone:** Femmer smells; NASA ARM weak-phrase indicators; Berry/Kamsties lexical & vagueness categories; GTWR Non-ambiguity.

### C9 — Conforming *(DECIDABLE)*

**ISO:** conforms to the approved style / template. **Target:** `framework/assets/topics-requirements.md` + `framework/assets/template-requirements.md` (the project's own house style).

**Procedure.** **FAIL** on any:

- **`RQ-CONF-stack`** — the statement or AC names a framework/library/runtime/database/vendor/product/version (run the **GR-20** blocklist alternation, case-insensitive). One hit = fail.
- **`RQ-CONF-layout`** — for UI-NN / RPT-NN / NT-NN rows, the cell uses UI-layout vocabulary (run the **GR-21** blocklist: `column|row|grid|sidebar|header|footer|sticky|fixed|top-right|…` and component-as-layout `Card|Modal|Drawer|Popover|Tabs|Wizard|…`). One hit = fail.
- **`RQ-CONF-ac-syntax`** — **GR-23**: an F-NN or BR-NN acceptance criterion that is NOT in EARS form (`The system shall …` / `When … the system shall …` / `While …` / `Where …` / `If … then the system shall …`); or a BR-NN statement not in `When {condition}, then {outcome}` form; or a UI-NN / story AC written in EARS (wrong notation — those keep observable-signal / Given-When-Then). 
- **`RQ-CONF-structure`** — a mandated column for the row type is missing (F-NN: Priority + Statement + AC + Source; BR-NN: Statement / Enforcement / AC / Source / Severity; UI-NN: Priority + behaviour + AC).

**N/A** for a column the active target-mode legitimately omits (e.g. an `application`-only field under `prototype`). **PASS** when all type-applicable house rules hold.

**Backbone:** the project's own GR-20 / GR-21 / GR-23 (which the drafter already enforces — this lens re-checks the merged doc); GTWR Conforming.

### C7 — Verifiable *(DECIDABLE — lexical slice only)*

**ISO:** realisation can be verified by analysis / demonstration / inspection / test; measurable.

**Procedure (lexical verifiability only).** **PASS** if the AC cell is populated AND contains a measurable anchor: a number + unit, a threshold/comparator (`≤ ≥ < > within N`), an enumerated closed set, a binary observable state, or a Given-When-Then with an observable result. **FAIL** (`RQ-VER-no-ac`) if the AC is absent or `TBD`; **FAIL** (`RQ-VER-unmeasurable`) if the AC contains only unmeasurable verbs (`handle`, `support`, `manage`, `process`, `work correctly`) with no observable signal. **N/A** never.

**Scope disclaimer (baked into the artefact):** this cell decides *lexical* verifiability — "is there a testable signal in the text?" — NOT "is this the right test?" or "can a test actually be written post-design?" The latter is the judgment characteristic *Correct* and a design-time concern.

**Backbone:** GTWR Realism/verifiability; NASA ARM measurability; Carson's "verifiability is foundational".

### C4 — Complete *(DECIDABLE — structural slice only)*

**ISO (individual):** needs no further amplification; no TBD.

**Procedure (structural slice).** **FAIL** if the statement or AC contains `TBD`, `TBC`, `???`, `[gap]`, an unresolved `[AI-SUGGESTED]` left in the merged doc, a trailing dangling `…`, a cross-reference to a non-existent ID (`→ §6.2 BR-99` where BR-99 is absent — `RQ-COMP-dangling-ref`), or an empty mandated cell (`RQ-COMP-empty-cell`); else **FAIL** as `RQ-COMP-tbd` for the placeholder cases. **PASS** otherwise. **N/A** never.

**Scope disclaimer:** *semantic* completeness ("is anything the stakeholder needs missing?") is NOT this cell — it is the set-level Complete pass + a judgment, and is deferred to TEN-BA-QUESTIONS for the full treatment.

**Backbone:** GTWR Completeness (no-TBD rule).

### C1 — Necessary *(JUDGMENT — fenced)*

**ISO:** essential; its omission leaves an unfulfilled need.

**Fenced procedure (doc-trace shadow only).** Observe whether the requirement traces to an upstream node *in the document*: a §4.1 goal (via rationale/`Goal:` annotation), a §4.2 story, a §6.2 BR, a §1.5 In-scope capability, or a `[STANDARD-RULE: GR-NN]` marker.

- Traces → `likely-pass` (confidence moderate), observation = the anchor.
- No trace AND not a GR-NN default → `concern: no upstream trace in document`.
- Necessity genuinely needs a stakeholder → `not-doc-decidable`.

**Never assert "this requirement is unnecessary."** The strongest claim is "no upstream trace is visible in the document." The band carries the pointer: *"for the full business-defensibility audit, run FIRST-PRINCIPLES."* (This is the deliberate overlap-management seam.)

### C2 — Appropriate *(JUDGMENT — fenced)*

**ISO:** right level of abstraction; implementation-free; not lower than needed.

**Fenced procedure.** `concern` on mechanism-over-outcome wording (the requirement prescribes *how* where *what* would do — `the system shall use a dropdown` vs `the system shall let the user select one status`). `likely-pass` when stated as an outcome. `not-doc-decidable` when level-appropriateness needs architecture context. (Note: hard stack/layout prescriptions already fire as a Conforming fail under GR-20/GR-21; Appropriate catches the *softer* mechanism-over-outcome signal that those greps miss.)

### C8 — Correct *(JUDGMENT — fenced)*

**ISO:** accurately represents the stakeholder need.

**Fenced procedure.** Default `not-doc-decidable` — correctness is a fact about the stakeholder's intent, not about the text. The agent may render `concern` **only** when the document *internally contradicts itself* about this requirement (the statement says one threshold, a linked BR says another), and even then it cross-references the set-level Consistent finding rather than asserting the requirement is "wrong."

### C6 — Feasible *(JUDGMENT — fenced)*

**ISO:** realisable within constraints (technology, cost, schedule, regulatory).

**Fenced procedure.** Default `not-doc-decidable` — feasibility is a function of the build team and stack, which a requirements doc (targeting a simulated prototype per PI-01..PI-08) does not fix. The band reads *"feasibility requires technical/architecture review — not assessable from the requirements text alone."* The agent may render `concern` **only** on a self-evident impossibility stated in the text (a requirement that contradicts a §1.5 Out-of-scope exclusion or an active PI invariant).

---

## The five set-level characteristics (document-level pass)

Run once over the whole requirement set after per-requirement scoring. Each emits 0..N findings `{characteristic, severity (blocking|major|minor), anchors[], evidence_per_anchor[], relation, consequence}`. Evidence discipline mirrors first-principles' CS findings: quotes ≤3 lines, verbatim from the quote index; `consequence` uses **observational verbs only** (`leaves, cannot, does not, contradicts, omits, lacks`), never prescriptive (`add, specify, define, require, must, should`) — gate-enforced.

1. **SL-Complete** — orphan-goal (a §4.1 goal with no implementing F-NN/UI-NN), a §3 persona with no §4.2 story, a §6.10 backend op with no §6.1 F-NN (A14 bijection), a dangling cross-ref. (Semantic completeness is fenced — deferred to TEN-BA-QUESTIONS.)
2. **SL-Consistent** — contradictory thresholds/outcomes on the same entity, conflicting RBAC-vs-BR gating, a term used two ways. Cite both anchors + both verbatim quotes. Default `major`; **`blocking` if the conflict is on a Must-priority pair**.
3. **SL-Feasible** — fenced; default `not-doc-decidable`; `concern` only on a collective internal impossibility (two Must requirements whose union violates a PI invariant).
4. **SL-Comprehensible** — a domain term used before its §2.1/§9 definition, an unexpanded acronym on first use, an ID reference that doesn't resolve. Severity minor/major.
5. **SL-Able-to-be-validated** — a tally (not a grade) of requirements carrying a measurable AC (rolls up the per-requirement Verifiable results) + presence of §4.1 quality signals.

**Plus the extension (NOT a sixth canonical characteristic):**

- **SR-EXT-redundancy** — near-duplicate requirements (two F-NN with overlapping statements + the same anchor target). **Explicitly labelled a GTWR-Concision extension folded under the set-level register — NOT a 29148 set-level characteristic.** (29148 mandates exactly five set-level characteristics; "not-redundant" / "bounded" are organisational extensions.)

---

## Scoring rubric (risk tiers — no vanity %)

**Per-requirement risk tier**, computed from DECIDABLE cells only:

- **RED** — ≥1 decidable FAIL on **Singular** OR **Unambiguous** OR **Verifiable**. (The testability/estimation killers: a compound, ambiguous, or untestable requirement is high-risk regardless of the rest.)
- **YELLOW** — no RED trigger, but ≥1 decidable FAIL on **Conforming** OR **Complete-structural**. (House-style / TBD defects: real, lower blast-radius.)
- **GREEN** — zero decidable FAILs. (Judgment `concern` bands may still be present; they are surfaced separately and never downgrade a GREEN.)

**Document-level summary** (the exec-summary renders all four; there is **no single blended conformance percentage**):

- **Per-characteristic failure tally** — one count per decidable characteristic (`Singular: N · Unambiguous: N · Conforming: N · Verifiable: N · Complete-struct: N`). The "which weakness dominates" signal.
- **Risk-tier distribution** — `Red: N · Yellow: N · Green: N (of M scored)`.
- **Set-level count** — `Complete: N · Consistent: N · Feasible: N · Comprehensible: N · Validatable: tally · redundancy(ext): N`.
- **Judgment band tally** (muted, separate) — `Necessary: N concern · Appropriate: N concern · Correct: N not-decidable · Feasible: N not-decidable`.

The score is **tied to the fix list, not a grade.** The artefact states: *"No aggregate conformance percentage is reported; track readiness by Red-tier count trending to zero."*

---

## Verdict mapping

Reuse the three cross-reviewer verdict strings. Derive deterministically from the decidable-tier distribution + set-level severities:

| Verdict | Trigger |
|---|---|
| **BLOCKED** | ≥1 `blocking` set-level finding (a Must-priority Consistency conflict, or an orphan-goal) **OR** ≥3 RED requirements **OR** a single RED on a Must-priority requirement's Singular/Verifiable. |
| **NEEDS-REVISION** | ≥1 RED requirement OR ≥1 set-level `major`, but no BLOCKED trigger. |
| **ACCEPTED-WITH-CONCERNS** | zero RED, zero set-level `major`/`blocking`. Yellow tiers and judgment concerns DO NOT block — they are triage signal. (The lens never returns an unconditional ACCEPTED — the fix list always merits a look.) |

The verdict is information, not a hard gate: the reviewer writes the artefact regardless and hands back via Accept/Revise/Restart.

---

## Fix list + EARS rewrite procedure

A proposed rewrite is generated **only** for:

- **Unambiguous FAIL** — replace the flagged weak-phrase with a measurable/definite form.
- **Singular FAIL** — split into N atomic EARS requirements, one per separable capability; preserve the ID with letter suffixes (`F-12` → `F-12a`, `F-12b`) so the 1→N mapping is visible.
- **Conforming FAIL where the only defect is non-EARS AC syntax** — re-cast the AC into the correct EARS pattern (the safest rewrite — pure notation, no meaning change).

No rewrite is proposed for Verifiable / Complete-structural fails (they need a value the agent must not invent), or for any judgment band.

**EARS patterns (the rewrite grammar):**

- **Ubiquitous** — `The <system> shall <response>.`
- **State-driven** — `While <state>, the <system> shall <response>.`
- **Event-driven** — `When <trigger>, the <system> shall <response>.`
- **Optional-feature** — `Where <feature is included>, the <system> shall <response>.`
- **Unwanted-behaviour** — `If <condition>, then the <system> shall <response>.`
- **Complex** — keyword composition of the above.

**Anti-fabrication rule (load-bearing).**

- A **pure structural transform** (splitting a compound; re-casting AC into EARS; replacing a vague pronoun with the explicit antecedent already present in the text) renders as a paste-ready `Original → Proposed (EARS)` block.
- A rewrite that **would change or add meaning** — chiefly replacing a vague quantifier with a number the document does not state (`shall respond quickly` → `shall respond within 2 seconds`) — MUST render as a **placeholder template** (`shall respond within ⟨threshold — confirm with stakeholder⟩`) flagged `meaning-change: confirm`. The agent **never** fabricates the value. This mirrors first-principles' "do not invent evidence / do not author replacement subjects."

**Surfacing.** A dedicated Fix List section, one card per Red/Yellow requirement: ID + anchor, failing characteristic(s) + rule codes, the offending verbatim quote, and the `Original → Proposed (EARS)` block (with a `confirm` chip where meaning-change). The rewrites also serialise into the embedded JSON block, re-ingestible by a future `/requirements` pass — **no auto-feed is built in this MVP** (consistent with all five existing reviewers, which produce punch-lists the consultant manually folds back). The handback summary line reports the rewrite count + the count needing confirmation.

---

## GR-NN / PI-NN rescue (filter — the late, scoped read)

Read `framework/shared/general-rules.md` and `framework/shared/prototype-invariants.md` **once, at this step only** (mirrors first-principles' Step 6). Two rescue rules over the JUDGMENT band:

1. **Necessary / Appropriate rescue (GR-NN).** A requirement that *looks* unnecessary or over-specified may implement a framework standard default — a confirmation gate (GR-04), a session-timeout value (GR-19), a pagination/sort/empty-state/loading behaviour (GR-08..GR-18). If it implements an active GR-NN, re-mark the Necessary band from `concern` to `likely-pass` with observation `[STANDARD-RULE: GR-NN] — {summary}`, and suppress an Appropriate "mechanism" concern that the rule itself mandates.
2. **Feasible rescue (PI-NN).** A requirement that looks infeasible because it names backend behaviour is rescued by PI-01..PI-08 (the prototype simulates it) — re-mark the Feasible band observation `[PROTOTYPE-INVARIANT: PI-NN] — {summary}`.

**NOT rescuable:** the five decidable fails (Singular, Unambiguous, Conforming, Verifiable, Complete-structural). A GR-NN cannot make a compound requirement singular or an ambiguous one precise — those are the requirement's own textual defects. (Mirrors first-principles' "Q1/Q2/Q4/Q6 not rescuable.") Record every rescue in diagnostics `{req_id, characteristic, rescue_source: GR-NN|PI-NN, summary}`.

---

## Quality gates (hard gates)

Run before writing. Each is `pass | fail` (gate 8 has a `warn` variant). On any hard-gate fail the reviewer does **not** write — it surfaces the failure via `AskUserQuestion {Revise | Override | Restart}` (max 3 restart loops, then force Revise).

1. **Schema** — every scorecard has nine cells; every decidable cell verdict ∈ {pass, fail, N/A}; every judgment cell band ∈ {likely-pass, concern, not-doc-decidable}.
2. **Enumeration** — `scored_count == enumerated_count` from Step 3.
3. **Evidence-quote-exists (anti-fabrication)** — every decidable `fail` evidence quote AND every set-level `evidence_per_anchor.quote` is a verbatim substring in the Step-2 quote index.
4. **Decidable-fail-has-rule-code** — every decidable `fail` carries a non-null rule code from the closed list in this reference.
5. **Judgment-cell-is-fenced** — every judgment cell is a band + confidence, never pass/fail; no judgment cell asserts a hard fail; Correct/Feasible default `not-doc-decidable` unless an internal-contradiction observation is cited.
6. **Tier consistency** — each `risk_tier` matches its decidable-cell verdicts per the scoring rule.
7. **Rewrite anti-fabrication** — every proposed rewrite is either a pure structural transform OR carries a placeholder + `meaning-change: confirm`; no rewrite asserts an invented numeric threshold.
8. **Set-level observational-verb** — every set-level `consequence` contains zero prescriptive verbs (lexical filter: `add|include|specify|define|require|mandate|must|should`). *(warn variant: a set-level layer is `not-applicable` because the doc lacks that section — e.g. no §6.7 RPT rows — documented in diagnostics.)*
9. **SHA match** — `REQUIREMENTS_SHA256` equals the Step-2 SHA-256.
10. **Verdict consistency** — recompute the verdict from the tier distribution + set-level severities; assert it equals the rendered value.

---

## Worked examples (the build-time decidability fixture)

A 14-requirement deliberately-flawed fixture (the lens's by-hand decidability pilot — there is no live `requirements/requirements.md` in this generator repo). Real ID shapes; a mix of clean controls and seeded defects. This is reference material, never a runtime input.

| ID | Pri | Statement (as written) | AC (as written) | Tier | Decidable failures (rule code) | Judgment |
|---|---|---|---|---|---|---|
| F-01 | Must | The system shall allow a user to create an invoice. | When the user submits the create-invoice form with all required fields valid, the system shall persist the invoice and show it in the invoice list. | GREEN | — | — |
| F-02 | Must | The system shall let the user create, edit, and delete invoices and export them to PDF. | The user can manage invoices. | RED | Singular `RQ-SING-enumeration`; Verifiable `RQ-VER-unmeasurable` ("manage"); Conforming `RQ-CONF-ac-syntax` (non-EARS AC) | — |
| F-03 | Should | The system shall respond quickly to user actions. | Response is fast. | RED | Unambiguous `RQ-AMB-vague-term` ("quickly","fast"); Verifiable `RQ-VER-unmeasurable`; Conforming `RQ-CONF-ac-syntax` | — |
| F-04 | Should | The system shall handle errors appropriately. | Errors are handled gracefully. | RED | Unambiguous `RQ-AMB-vague-term` ("appropriately","gracefully"); Verifiable `RQ-VER-unmeasurable` ("handle") | — |
| F-05 | Must | When the user submits the invoice form, the system shall validate the required fields. | When a required field is empty, the system shall display an inline error naming the field. | GREEN | — | — |
| F-06 | Should | The system shall use a modal dialog with a sticky header for confirmations. | When the user triggers a destructive action, the system shall display a confirmation dialog. | YELLOW | Conforming `RQ-CONF-layout` ("modal dialog","sticky header") | Appropriate → `concern` (mechanism); Necessary → `likely-pass` via `[STANDARD-RULE: GR-04]` |
| F-07 | Could | The system shall integrate with the Stripe payment API. | When a payment is submitted, the system shall record the result. | YELLOW | Conforming `RQ-CONF-stack` ("Stripe") | — |
| F-08 | Must | The system shall require explicit confirmation naming the invoice before deleting it. | When the user clicks Delete, the system shall require confirmation naming the invoice; on confirm, the system shall delete it. | GREEN | — | Necessary → `likely-pass` via `[STANDARD-RULE: GR-04]` (the confirmation step is the framework default, not gold-plating) |
| BR-01 | Must | When an invoice total exceeds 10000, then the invoice shall require manager approval before payment. | If an invoice total exceeds 10000 and lacks manager approval, then the system shall block payment and show "Manager approval required." | GREEN | — | — |
| BR-02 | Should | Invoices over 5000 are auto-approved. | Invoices above 5000 are approved automatically. | YELLOW | Conforming `RQ-CONF-ac-syntax` (not `When…then`, AC not EARS) | Correct → `concern` (cross-refs SL-Consistent vs BR-01) |
| UI-02 | Must | The user can filter the invoice list by status. | Given the user selects a status filter, the list shows only invoices in that status. | GREEN | — | — |
| UI-03 | Should | The user can manage invoices efficiently and intuitively. | The interface is intuitive. | RED | Unambiguous `RQ-AMB-vague-term` ("efficiently","intuitively"); Singular `RQ-SING-multiverb` ("manage"); Verifiable `RQ-VER-unmeasurable` | — |
| RPT-01 | Could | A monthly revenue report for finance. TBD. | *(none)* | RED | Verifiable `RQ-VER-no-ac`; Complete-structural `RQ-COMP-tbd` | — |
| NT-01 | Should | Notify relevant people when something important happens. | Notifications are sent when needed. | RED | Unambiguous `RQ-AMB-vague-term` ("relevant","important","when needed"); Verifiable `RQ-VER-unmeasurable` | — |

**Set-level:** SL-Consistent — **BR-01 vs BR-02**: an invoice over 10000 is both auto-approved (BR-02) and requires manager approval (BR-01) — a contradiction on the Invoice approval policy; `blocking` (Must-priority BR-01). SR-EXT-redundancy — none.

**Tally:** Singular 2 · Unambiguous 4 · Conforming 4 · Verifiable 6 · Complete-struct 1. Tiers: Red 6 · Yellow 3 · Green 5 (of 14). **Verdict: BLOCKED** (≥3 RED + a blocking set-level conflict).

**Fix-list examples:**

- F-02 (Singular) → split: `F-02a — The system shall let the user create an invoice.` · `F-02b — The system shall let the user edit an invoice.` · `F-02c — The system shall let the user delete an invoice.` · `F-02d — The system shall let the user export an invoice to PDF.` (pure structural transform; AC each re-cast to EARS).
- F-03 (Unambiguous) → `Original: "shall respond quickly" → Proposed: "When the user triggers an action, the system shall display a result within ⟨threshold — confirm with stakeholder⟩."` flagged `meaning-change: confirm` (no fabricated number).

This fixture proves the four acceptance criteria: ≥70% of the 70 decidable cells are confidently decidable (all five checks mechanical per row); ≥2 Singular/Unambiguous defects pinned to IDs (Singular×2, Unambiguous×4); judgment cells degrade gracefully (F-06/F-08 rescue, Correct/Feasible mostly `not-doc-decidable`, none change a tier); SL-Consistent catches BR-01/BR-02.

---

## Anti-patterns (binding on the reviewer)

- **Do not freelance ambiguity.** Only the closed weak-phrase dictionary fires Unambiguous. *"This feels vague"* without a dictionary hit is not a finding (reproducibility contract — mirrors the GR-20 closed blocklist).
- **Do not assert a hard verdict on a judgment characteristic.** Necessary/Appropriate/Correct/Feasible render as bands at moderate confidence, never pass/fail. Correct/Feasible default `not-doc-decidable`.
- **Do not fabricate a value in a rewrite.** A meaning-changing rewrite carries a `⟨…confirm⟩` placeholder, never an invented threshold (gate 7).
- **Do not rescue a decidable fail.** GR-NN/PI-NN rescue applies only to the judgment band; a compound/ambiguous/untestable requirement is the requirement's own defect.
- **Do not report a single blended conformance %.** Report the per-characteristic tally + tier distribution.
- **Do not score §6.3 / §6.5 / §6.6 as per-requirement rows.** They are set-level-only; disclose the exclusion.
- **Do not write `[SRC: …]` or `[AI-SUGGESTED: AI-NN]` markers in the artefact.** Per `feedback_no_inline_provenance`, the review artefact is clean of inline markers; provenance is the requirement ID / §-anchor. Rescued judgment cells use `[STANDARD-RULE: GR-NN]` / `[PROTOTYPE-INVARIANT: PI-NN]` as in-artefact evidence tags (the same convention first-principles uses).
- **Do not read draft sidecars / analyses / design-system / framework state.** Read `requirements/requirements.md` + this reference + the character + the template + the conforming-target files + (at the late filter step) general-rules + prototype-invariants. Nothing else.
- **Do not cross lanes.** A contradiction *between* requirements is a set-level Consistent finding, not nine separate cell fails. A "should this exist at all" judgment is the Necessary band's thin shadow + a pointer to FIRST-PRINCIPLES — do not run the full defensibility audit here.
- **Do not paste the artefact body into the conversation.** The file lands on disk; the consultant opens it.

## Voice and readability

This artefact is read by a human consultant (sometimes a client stakeholder) and by **no one else** — a review has no downstream machine consumer. The full readability standard is `framework/shared/output-readability.md` (additive — relaxes no gate, no severity, no quality check). The operative contract for this reviewer:

- The "In plain terms" lead is the **one** sanctioned narrative paragraph. It is plain, not warm. Everything below it is a punch-list of scored cells, evidence quotes, and fix-list cards.
- Jargon is glossed at first use in the lead: *verdict (the overall gate — BLOCKED / NEEDS-REVISION / ACCEPTED-WITH-CONCERNS)*, *risk tier (per-requirement severity — Red / Yellow / Green)*, *decidable characteristic*, *judgment band*, *EARS*. Client domain terms are never glossed.
- Severity is **never softened** in the lead: a BLOCKED verdict names it as BLOCKED; a Red tier is Red.
- Traceability (requirement ID / §-anchor / verbatim evidence) is preserved everywhere; no `[SRC:]` markers are added.

## Stance summary

Requirements Quality scores every ID-bearing requirement on the ISO 29148 nine-characteristic rubric, leading with the five characteristics a document-only reviewer can decide mechanically (Singular, Unambiguous, Conforming, Verifiable, Complete-structural) at 80–95% precision with a citable rule backbone, and fencing the four that need domain knowledge (Necessary, Appropriate, Correct, Feasible) as moderate-confidence bands rather than faking a verdict. It runs the five set-level characteristics as a document-level pass, computes risk tiers from the decidable band only, reports a per-characteristic tally rather than a vanity percentage, and hands back EARS-form rewrites for the ambiguous and compound requirements under a strict no-fabrication rule. A reviewer that freelances ambiguity, asserts a hard verdict on a judgment characteristic, fabricates a rewrite value, or reports one blended score has bent the methodology beyond its contract.
