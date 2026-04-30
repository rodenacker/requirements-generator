<!-- ROLE: asset (P2 analysis reference). v7a-derived seed (from .claude/skills/wds-3-scenarios/data/scenario-outline-template.md). Heavy rewrite applied: WDS scenario / 8-question dialog framing dropped; Mermaid trigger-map cross-references dropped; "shortest path" + sunshine-path concept retained as the journey's *primary* track but extended with the full journey-map column set; replaced flat-step list with the canonical journey-map columns (stage → touchpoint → action → thoughts → emotions → pain points → opportunities) per v7b-Brief.md > §analyses/user-journeys-reference.md. Finalise during phase-2 build-order step 9. -->

# User-Journeys analysis reference

> **Method:** Per primary target-user persona, per top-level user goal, produce a temporal flow map showing where the user is, what they're doing, what they're thinking and feeling, and where the application could help most.

**Output file:** `artifacts/requirements/analyses/user-journeys.md` — markdown table per journey + narrative summary.

**Analyser agent:** `framework/agents/analyses/user-journeys-analyser/agent.md`

**Character:** `framework/assets/characters/user-journeys-analysis.md` (TBD).

---

## Journey-map columns

Each journey is a table with these columns:

| Stage | Touchpoint | Action | Thoughts | Emotions | Pain points | Opportunities |
|---|---|---|---|---|---|---|
| {{phase of the journey}} | {{where the interaction happens — screen, channel, system, real-world}} | {{what the user does}} | {{what's going through their head}} | {{−2 … +2 emotional rating + label}} | {{friction, frustration, confusion}} | {{candidate design decisions to feed back into design-spec global decisions}} |

---

## Stages

Stages span trigger → outcome, end-to-end. Typical shape (project-specific):

1. **Trigger** — what brings the user to this goal.
2. **Approach** — pre-application context, mental preparation, prior tooling.
3. **Engage** — initial application interaction.
4. **Progress** — sustained use through the goal's primary task flow.
5. **Decide / commit** — the moment-of-truth action.
6. **Outcome** — confirmation, follow-through, downstream consequences.

Stages are not screens. Multiple stages can share a screen; one stage can span multiple screens. The journey describes the *user's experience over time*, not the application's structure.

---

## Emotion scale

`−2` (frustrated / panicked) → `−1` (anxious / uncertain) → `0` (neutral) → `+1` (engaged / hopeful) → `+2` (delighted / confident).

A **moment of truth** is any row where the emotion drops by ≥1 from the previous row, or where stakes are stated as high in `topics-requirements.md > §User goals > context`. Moments of truth get extra design attention — the opportunities column for those rows feeds directly into design-spec §Global design decisions.

---

## Quality checks

- Every journey covers at least one full task from trigger to outcome (no truncation at "user lands on app").
- Every pain point has a suggested opportunity. A pain point without an opportunity is a finding the analyser surfaces back to the consultant, not a journey row.
- Every journey is anchored to one named target-user persona from `requirements.md > §Target users` and one top-level goal from §User goals. No invented personas or goals.
- One journey per primary target-user persona × top-level goal. Cap at the highest-frequency or highest-stakes journeys for MVP — don't enumerate every permutation.

---

## Stop-condition

The analysis is complete when:

- Every primary target-user persona's highest-priority top-level goal has a journey.
- Every journey covers trigger → outcome with at least one moment-of-truth row identified.
- Every pain point has an opportunity.
- Coverage is documented at the top of the analysis file (which goals × personas got journeys; which were skipped and why).

---

## Input-coverage asymmetry (v7b note)

The journey-map's *stages, touchpoints, actions* derive cleanly from `topics-requirements.md > §Task flows` + `§Source UI references`.

The *thoughts, emotions, pain points, opportunities* columns are typically **not** present in client briefs or PRDs — they come from user research (interview transcripts, survey results, contextual inquiries). When such research isn't in `/input/`:

1. The analyser **infers** these columns from:
   - Domain knowledge (`requirements.md > §Domain`).
   - `§User goals > context` (frequency / expertise / stakes as emotional proxies — high stakes → anxiety, rare event → confusion, high frequency → impatience with friction).
   - Existing-tool critique in `§Source UI references` (pain points reflect frustration with current tooling).
2. Each inferred cell is flagged `[AI-SUGGESTED]`.
3. The completeness report surfaces the inferred cells; consultant resolves via Q&A or via dropping research docs into `/input/` and re-running `/analyse`.

**Richer inputs → richer journey outputs.** The methodology degrades gracefully: with thin evidence, the journey is mostly inferred and flagged; with rich evidence (interviews, surveys), inferences shrink and confidence rises.

---

## Output shape (markdown skeleton)

```markdown
# User Journeys

**Coverage:** {{N}} journeys across {{M}} target-user personas × top-level goals. Skipped: {{list with rationale}}.

---

## Journey 1: {{Persona}} — {{Top-level goal}}

**Trigger:** {{what kicks off the journey}}
**Outcome:** {{what success looks like at the end}}
**Moments of truth:** {{rows flagged below}}

| Stage | Touchpoint | Action | Thoughts | Emotions | Pain points | Opportunities |
|---|---|---|---|---|---|---|
| {{stage}} | {{touchpoint}} | {{action}} | {{thoughts}} | {{emotion + label}} | {{pain}} | {{opportunity}} |

**Narrative summary:** {{2–4 sentences describing the arc — where the user starts emotionally, where the moment of truth sits, where they end. Useful as a callout in the design spec's per-screen rationale where a screen sits at a moment-of-truth row.}}

---

<!-- repeat per journey -->
```

---

## Downstream consumption (handled by `skills/map-user-journeys-to-ui.md`)

- Journey stages → navigation model (which routes follow which, in what order).
- Touchpoints → screen list (every distinct touchpoint is a candidate `screen` or `view`).
- Pain points → constraints + states in the design spec (a pain point at a "loading" touchpoint becomes a Loading-state requirement on that screen).
- Opportunities → design-spec §Global design decisions (any opportunity that recurs across journeys becomes a global decision; one-off opportunities become per-screen decisions).
- Moments of truth → per-screen trade-off ratings biased toward Accuracy, Focus, Memorability.

---

## What v7b deliberately drops from v7a's scenario template

| v7a element | Why dropped in v7b |
|---|---|
| 8-question scenario dialog (Q1 Transaction → Q8 Shortest Path) | Replaced by analyser-agent activation that reads `requirements.md` directly. The questions become silent extraction by the analyser, not consultant prompts. |
| "Sunshine path" / shortest-path framing | Subsumed: the journey's "Action" column **is** the sunshine path; v7b doesn't separate "shortest" and "actual" — it documents the actual journey including pain points. Branches become separate journeys when stakes-relevant; otherwise they're rows with low-emotion ratings. |
| Trigger-map cross-references (Mermaid + persona-priority emojis) | v7b has no trigger-map deliverable; persona references are direct file paths into `requirements.md > §Target users`. |
| Per-step folder structure (`[NN].1-[page-slug]/`) | Belongs to the page-creation workflow, not the journey analysis. v7b's journey is structural, not artifact-producing. |
| Hope / Worry as separate one-line fields | Subsumed into the Thoughts + Emotions columns; redundant under journey-map structure. |
