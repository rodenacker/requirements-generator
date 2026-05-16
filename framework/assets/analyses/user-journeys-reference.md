<!-- ROLE: asset (P2 analysis reference). v7a-derived seed (from .claude/skills/wds-3-scenarios/data/scenario-outline-template.md). Heavy rewrite applied: WDS scenario / 8-question dialog framing dropped; Mermaid trigger-map cross-references dropped; "shortest path" + sunshine-path concept retained as the journey's *primary* track but extended with the full journey-map column set; replaced flat-step list with the canonical journey-map columns (stage → touchpoint → action → thoughts → emotions → pain points → opportunities) per v7b-Brief.md > §analyses/user-journeys-reference.md. Output convention aligned with OOUX/JTBD/USE-CASES MVPs — self-contained HTML under `analyses/<METHOD>/`, not markdown. -->

# User-Journeys analysis reference

> **Method:** Per primary target-user persona, per top-level user goal, produce a temporal flow map showing where the user is, what they're doing, what they're thinking and feeling, and where the application could help most.

**Output file:** `analyses/USER-JOURNEYS/user-journeys-map.html` — a self-contained HTML artefact containing one journey card per (persona × top-level goal). Each card carries a tabular swimlane grid (phases × {actions, thoughts, emotions, touchpoints, pain-points, opportunities}) plus an inline-SVG emotion-curve visualisation. No external CSS/JS dependencies; viewable by opening `file://` in a browser.

**Analyser agent:** `framework/agents/analyses/user-journeys-analyser.md`

**Character:** `framework/assets/characters/user-journeys-analysis.md`.

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

A **moment of truth** is any row where the emotion drops by ≥1 from the previous row, or where stakes are stated as high in `requirements/requirements.md > §4 User goals & stories > context`. Moments of truth get extra design attention — the opportunities column for those rows feeds directly into design-spec §Global design decisions.

---

## Quality checks

- Every journey covers at least one full task from trigger to outcome (no truncation at "user lands on app").
- Every pain point has a suggested opportunity. A pain point without an opportunity is a finding the analyser surfaces back to the consultant, not a journey row.
- Every journey is anchored to one named target-user persona from `requirements/requirements.md > §3 Target users` and one top-level goal from `§4 User goals & stories` (or one task flow from `§5 Task flows`). No invented personas or goals.
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

The journey-map's *stages, touchpoints, actions* derive cleanly from `requirements/requirements.md > §5 Task flows` + `§8 Source UI references`.

The *thoughts, emotions, pain points, opportunities* columns are typically **not** present in client briefs or PRDs — they come from user research (interview transcripts, survey results, contextual inquiries). When such research isn't in `/input/`:

1. The analyser **infers** these columns from:
   - Domain knowledge (`requirements/requirements.md > §1 Application context` + `§2 Domain model`).
   - `§4 User goals & stories` (frequency / expertise / stakes as emotional proxies — high stakes → anxiety, rare event → confusion, high frequency → impatience with friction).
   - Existing-tool critique in `§8 Source UI references` (pain points reflect frustration with current tooling).
2. Each inferred cell is flagged `[AI-SUGGESTED]`.
3. The completeness report surfaces the inferred cells; consultant resolves via Q&A or via dropping research docs into `/input/` and re-running `/analyse-requirement`.

**Richer inputs → richer journey outputs.** The methodology degrades gracefully: with thin evidence, the journey is mostly inferred and flagged; with rich evidence (interviews, surveys), inferences shrink and confidence rises.

---

## Output shape (HTML schema)

The artefact is a single self-contained HTML file at `analyses/USER-JOURNEYS/user-journeys-map.html`. The analyser populates `framework/assets/analyses/template-user-journeys.html` via documented placeholder substitution. Every substituted value is HTML-escaped before injection (XML-escape inside `<svg><text>` nodes).

### Header placeholders

| Placeholder | Value |
|---|---|
| `{{TITLE}}` | *"User Journeys — `<domain>`"* if `§1` declares a domain, else *"User Journeys"*. |
| `{{DOMAIN}}` | Verbatim from `§1 Application context > Domain`, else *"(not declared in requirements.md)"*. |
| `{{GENERATED_AT}}` | ISO-8601 UTC, captured at render time. |
| `{{REQUIREMENTS_SHA256}}` | SHA-256 of `requirements/requirements.md` captured at Step 2. |
| `{{JOURNEY_COUNT}}` | Number of `<section class="journey-card">` blocks rendered. |
| `{{PERSONA_COUNT}}` | Distinct personas covered (each may anchor more than one journey). |
| `{{PHASE_COUNT}}` | Total phases across all journeys. |
| `{{ACTION_COUNT}}` | Total actions across all journeys. |
| `{{PAIN_POINT_COUNT}}` | Total pain points across all journeys. |
| `{{OPPORTUNITY_COUNT}}` | Total opportunities across all journeys. |
| `{{AI_SUGGESTED_COUNT}}` | Total cells marked `ai-suggested` — the key diagnostic affordance. |

### Body placeholders

| Placeholder | Value |
|---|---|
| `{{DIAGNOSTICS_BLOCK}}` | Pre-rendered `<section class="diagnostics">` containing: provenance summary (count per marker), 8 quality-check result lines (PASS/FAIL), per-journey AI-SUGGESTED density table, density-warning line if any journey exceeds 75%, and (on Override runs) per-flagged-item lines. |
| `{{JOURNEY_CARDS}}` | Pre-rendered `<section class="journey-card">` blocks. One card per journey, in discovery order. |

### Per-card schema

Each `<section class="journey-card" id="journey-<slug>" style="--phase-count: N">` contains, in order:

1. `<header class="journey-header">` — persona name + scenario title + trigger + outcome.
2. `<figure class="journey-flow">` — inline `<svg role="img" aria-label="Emotion curve for <persona> — <scenario>">` showing the emotion curve over phases (polyline + gridlines + phase tick labels; y-axis fixed at −2…+2).
3. `<table class="journey-swimlane">` — CSS-Grid table: column 0 is the lane label, columns 1…N are the phases. Five lanes in fixed order: `.lane-actions`, `.lane-thoughts`, `.lane-emotion`, `.lane-touchpoints`, `.lane-painpoints`. Every `<td>` carries exactly one provenance class (see §Provenance markers below). Rows at moments-of-truth get the `.moment-of-truth` row class.
4. `<footer class="journey-footer">` — opportunities and ownership lists.

### Provenance markers

Every rendered cell carries exactly one of:

| Marker | CSS class | When |
|---|---|---|
| `from-task-flow` | `.provenance-from-task-flow` | Cell content appears verbatim in `§5 Task flows`. |
| `from-user-story` | `.provenance-from-user-story` | Cell content appears verbatim in `§4 User goals & stories`. |
| `from-persona` | `.provenance-from-persona` | Cell content appears verbatim in `§3 Target users`. |
| `derived-from-<section>` | `.provenance-derived` | Cell content was extracted from a named section but is not verbatim. The source section is recorded in a `data-source` attribute on the cell. |
| `ai-suggested` | `.provenance-ai-suggested` | Cell content was inferred per the input-coverage asymmetry rules above. The cell text is prefixed with `[AI-SUGGESTED]` per the global invariant. |

No sixth marker is allowed. No cell is unmarked.

### CSS class contract used by the analyser

The template scaffold owns CSS variables, layout, and typography. The analyser emits HTML using the following named classes:

- `.journey-card`, `.journey-header`, `.journey-flow`, `.journey-swimlane`, `.journey-footer`.
- `.lane-actions`, `.lane-thoughts`, `.lane-emotion`, `.lane-touchpoints`, `.lane-painpoints`.
- `.ai-suggested` — applied to any cell flagged `[AI-SUGGESTED]`; renders italic + dim background so the affordance is visually obvious.
- `.moment-of-truth` — applied to any `<tr>` (or `<td>` in the emotion lane) at a moment-of-truth phase.
- `.provenance-*` — exactly one per cell, per the markers table.
- `.rev-marker` — applied to any cell flagged by a failed quality check on an Override run.

The analyser does **not** edit the template's CSS or layout — only the documented `{{placeholders}}` are substituted.

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
