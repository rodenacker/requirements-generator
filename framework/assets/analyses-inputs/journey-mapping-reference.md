<!-- ROLE: asset (analysis reference). Methodology definition for the journey-mapping input-analyser. Modelled on framework/assets/analyses-inputs/thematic-analysis-reference.md. Industry framing: Nielsen Norman Group "Journey Mapping 101" + James Kalbach "Mapping Experiences" (O'Reilly, 2nd ed., 2020) — current-state user-journey mapping adapted for software-requirements elicitation inputs. One persona per map; if N personas implied by the inputs, render N journey cards in one artefact. Every non-empty cell carries one `[SRC: <filename>]` or `[STANDARD-RULE: GR-NN]` marker. Inferred cells render the proxy quote inline + `[SRC: <filename>]` for transparency. Cells without a proxy stay empty rather than fabricate. -->

# Journey Mapping reference

> **Method:** Walk every consumable source enumerated in `requirements/source-manifest.json`. For each named actor surfaced in the inputs, build one current-state journey map of the as-is workflow described in the briefs / decks / interview notes / screenshots — phases (3–6), steps per phase (3–8, user-as-subject verb phrases), touchpoints, channels, thoughts (verbatim quotes only), emotions (proxy-derived, −2…+2 scale), pain points, backstage systems, opportunities, and moments of truth. Render the artefact as self-contained HTML at `analyse-inputs/JOURNEY-MAPPING/journey-mapping.html` with **diagrams-first ordering** — a compact overview, then one `<article class="diagram-block">` per persona (inline SVG emotion curve + CSS-grid swim-lane table) stacked in the `#diagrams` gallery, then narrative bridges + moments-of-truth in `#narratives`, then collapsed diagnostics. Every non-empty cell carries one `[SRC: <filename>]` or `[STANDARD-RULE: GR-NN]` marker naming a manifest row's `filename` field (basename + extension). Coverage gaps surface as `[GAP-NO-EVIDENCE]` notes inside the diagnostics block — **never** as fabricated cells. Across re-runs the artefact is **additive**: prior journey cards, swim-lane cell contents, bridges, and moments-of-truth are preserved; new manifest content extends them.

**Output file:** `analyse-inputs/JOURNEY-MAPPING/journey-mapping.html` — self-contained HTML (inline `<style>`, inline SVG, no external JS, no CDN, no remote font). Mirrors the precedent set by `analyse-requirements/USER-JOURNEYS/user-journeys-map.html`. Re-ingestible into `input/` for `/requirements` consumption: HTML classifies as `Markitdown-text` tier and converts cleanly to Markdown while preserving the inline `[SRC: <filename>]` markers (the audit trail end-to-end is the load-bearing reason for the marker discipline).

**Analyser agent:** `framework/agents/analyses-inputs/journey-mapping-analyser.md`

**Character:** `framework/assets/characters/journey-mapping-inputs-analysis.md`

**Template:** `framework/assets/analyses-inputs/template-journey-mapping.html`

---

## Industry framing — Nielsen Norman Group + Kalbach, adapted for requirements work

A journey map is a venerable UX-research / service-design artefact:

- **Nielsen Norman Group's "Journey Mapping 101"** is the industry de-facto baseline: *"A journey map is a visualization of the process that a person goes through in order to accomplish a goal."* The canonical components are an actor / persona, a scenario + expectations, journey phases (chronological stages), actions / mindsets / emotions, and opportunities. NN/G's hard rule: **one persona per map** — combining personas dilutes narrative and produces an "average user" that does not exist.
- **James Kalbach's *Mapping Experiences* (O'Reilly, 2020)** generalises journey maps into one species of "alignment diagram" — visuals that align an individual's experience with an organisation's value delivery. Kalbach distinguishes journey maps from experience maps, service blueprints, mental-model diagrams, and spatial maps along five dimensions: point of view, scope, focus, structure, and uses. Journey maps specifically take the **customer/user's point of view** of a **defined scenario**, organised **chronologically**, focused on **cognitive and emotional states**, emphasising **moments of truth**.
- **Variants in the literature:**
  - **Current-state** — the as-is experience. Diagnoses problems. Most rigorous when grounded in research.
  - **Future-state** — the to-be experience. Supports design innovation.
  - **Day-in-the-life** — broader than one scenario; the full activity ecosystem.
  - **Service blueprint** — extends a journey map below the line of visibility with frontstage / backstage / support processes. A different artefact, not a variant.

This analyser ships **current-state only**. Rationale:

- Input documents (briefs, decks) overwhelmingly describe **as-is pain** ("today, users have to manually re-key data across three systems"). That's current-state evidence.
- Future-state maps require design hypotheses that don't exist yet at the `/analyse-inputs` stage — that's what the requirements draft will produce. Doing future-state in `/analyse-inputs` would short-circuit the consultant's design judgement.
- Day-in-the-life over-reaches the evidence in briefs (briefs scope a feature, not a day).
- Service blueprint is a meaningfully different artefact; promote it to a separate methodology when needed. **Backstage** appears here as a single lane in the journey map, capturing the most-valuable backstage signal (integration hints) without the methodology drift.

### Why journey mapping for INPUTS is distinct from `/analyse-requirement`'s `USER-JOURNEYS`

The codebase already ships a `USER-JOURNEYS` analyser under `/analyse-requirement` that lenses the synthesised `requirements/requirements.md`. The two methodologies share column names but operate at different pipeline stages with different source material:

| Lens | Pipeline | Source material | Temporal pose | Downstream use |
|---|---|---|---|---|
| `USER-JOURNEYS` (requirements side) | `/analyse-requirement` | `requirements/requirements.md` (synthesised spec) | **Future-state** (current-of-the-spec — system to be built) | Verify the spec covers the right experience |
| `JOURNEY-MAPPING` (inputs side, this analyser) | `/analyse-inputs` | Raw `input/` (briefs, decks, interview notes) | **Current-state** (current-of-the-world — as-is workflow) | Inform the spec by providing a structured experience map of what exists today |

Same column shape, different source material at different pipeline stages, different downstream uses. Compare: `opportunity-solution-trees` exists on both sides too (reverse-discovery for requirements, forward-discovery for inputs).

### Why this analyser uses HTML, not Markdown + Mermaid

- **Stakeholder-presentable** as-is via `file://` — consultants and PMs can open it in a browser without a Mermaid runtime, the same way they open `analyse-requirements/USER-JOURNEYS/user-journeys-map.html`.
- **Higher diagram fidelity.** Inline SVG renders the true −2…+2 emotion scale with negative-territory gridlines (Mermaid's `journey` chart is locked to 1–5 integers); CSS-grid swim-lane tables give deterministic column-per-phase × row-per-lane layout with text wrapping, accessibility, and hover states (Mermaid `flowchart LR` with `subgraph` swim-lanes can look cramped or overflow with 5+ lanes).
- **No `mmdc` dependency at write-time** — diagrams are inline SVG and HTML, so no Mermaid validator call, no install-instruction halt, fewer failure modes.
- **Round-trip safe.** The drafter reads HTML through markitdown, which preserves text content (including inline `[SRC: <filename>]` markers) while collapsing visual fidelity — exactly the trade-off this pipeline wants (visuals for consultants, text for `/requirements`).

---

## Output structure

The artefact has a fixed top-to-bottom shape, optimised for **diagrams-first review**:

1. **Compact overview** (`<header id="overview">`). Title, one-line caption (persona / phase / step / pain / opportunity / moments-of-truth counts + run number + generated-at), and a thin inline `<nav class="toc-diagrams">` with jump-links targeting the per-persona diagram blocks. Designed to fit above the fold on a 1080p screen so the first diagram is visible without scrolling.
2. **Diagrams gallery** (`<main id="diagrams">`). One `<article class="diagram-block" id="diagram-{persona-slug}">` per persona, in discovery order. Per block:
   - `<header>` — persona name + scenario + trigger + outcome (with `[SRC: <filename>]` markers).
   - `<figure class="emotion-curve">` — inline `<svg viewBox="0 0 720 200" role="img" aria-label="…">` rendering gridlines, polyline, per-phase circles (`.point`), moment-of-truth circles (`.point.moment`), phase labels.
   - `<figure class="swimlane">` — CSS-grid `<table>` with seven lanes (rows) × N phases (columns):
     - `.lane-actions` — verb-phrase actions, user-as-subject.
     - `.lane-touchpoints` — screens, surfaces, physical artefacts.
     - `.lane-channels` — web / mobile / phone / email / in-person.
     - `.lane-thoughts` — verbatim quoted thoughts (`"…"`) only.
     - `.lane-pain` — explicit pain points.
     - `.lane-backstage` — backstage systems, integrations, manual processes.
     - `.lane-opportunities` — verb-led opportunity statements.
3. **Narrative details** (`<section id="narratives">`). One `<article class="narrative-block" id="narrative-{persona-slug}">` per persona, in discovery order. Per block:
   - `<section class="bridge">` — pain → opportunity bullet list (one bullet per pain point; every pain has ≥ 1 opportunity).
   - `<section class="moments">` — moments-of-truth bullet list with step references and reasons.
4. **Diagnostics** (`<details id="diagnostics" class="diagnostics-toggle">`). Collapsed by default. Inside: the 8 hard-gate result lines (PASS / FAIL), source roster (Consumed + Skipped tables), per-run history bullets (run number, ISO date, persona-count delta, phase-count delta, override notes), and any `[GAP-NO-EVIDENCE]` notes (cells the analyser left empty for lack of proxy).
5. **Embedded JSON metadata** (`<script type="application/json" id="journey-mapping-meta">`) at the top of `<body>`. Carries `manifest_sha256`, `generated_at`, `run_count`, `persona_count`, `phase_total`, `step_total`, `pain_count`, `opportunity_count`, `moments_of_truth`. Used by the next run's drift gate.

---

## Round 1 — Persona discovery

Walk every consumable manifest row in full and enumerate named actors / user roles. Sources are tier-driven:

- `Native-text` → `Read original_path` directly.
- `Native-multimodal` → `Read original_path`; Claude's vision surfaces image bytes; transcribe visible text and structurally significant observations.
- `Supported-via-MCP` → `Read converted_sibling` (the `.converted.md`).
- `Unsupported` → skipped; record in the Consumed/Skipped roster.

Each candidate persona carries:

```
{
  persona_id,            // UJ-PNN zero-padded
  name,                  // verbatim from inputs (no invented names)
  role_description,      // short paraphrase if available
  source_filenames: [<filename>],   // ≥ 1
  source_quote: verbatim ≤ 200 chars (the quote that names this actor)
}
```

**Hard rule (NN/G):** one persona per journey map. If the inputs imply N personas, plan N journey cards in this run. **No invented personas.** If the inputs mention only an unnamed "user", capture that as `{name: "User", role_description: "(unnamed in inputs)"}` and proceed — degrading gracefully is preferred over fabricating a persona name.

State per-source persona-discovery counts aloud:

> *"Round 1 (Persona discovery): identified 3 personas across 4 sources — `Customer Service Rep` (3 sources: brief.docx, interview-notes.md, slack-export.md), `Billing Admin` (2 sources: brief.docx, whiteboard-photo.png), `End Customer` (1 source: interview-notes.md). Will render 3 journey cards."*

---

## Round 2 — Scenario & phase decomposition

For each persona, identify the scenario(s) the inputs describe. A scenario is the named workflow the persona is trying to accomplish (*"resolve a billing dispute"*, *"onboard a new client"*, *"close out a quarter"*). Then decompose the scenario into **3–6 phases** spanning trigger → outcome.

Each phase carries:

```
{
  phase_id,              // UJ-PNN-Pn zero-padded
  label,                 // verb-phrase header, ≤ 6 words (e.g., "Triage", "Investigation", "Resolution")
  source_filenames: [<filename>],
  trigger_evidence: verbatim ≤ 200 chars (what kicks off this phase)
}
```

**Hard constraint:** 3 ≤ phases ≤ 6. Refuse to emit a journey card with fewer than 3 phases (collapses to a screen) or more than 6 (becomes a task list, not a journey). If the inputs justify more than 6, prefer to merge sub-phases under broader phase headers; if the inputs justify fewer than 3, surface the gap to the consultant rather than padding.

The typical six-phase shape (Trigger → Approach → Engage → Progress → Decide / commit → Outcome) is a suggestion, not a contract — anchor phase names to the input documents' own language where possible.

State the per-persona phase shape aloud.

---

## Round 3 — Step extraction

For each phase, list **3–8 user actions** (verb phrases, user-as-subject):

```
{
  step_id,               // UJ-PNN-Pn-Sm zero-padded
  text,                  // "Reads the open ticket", "Pulls up the account record"
  source_filenames: [<filename>],
  source_quote: verbatim ≤ 200 chars
}
```

**Anti-pattern guard:** Actions must have the **user** as the subject. *"User submits the order"* is correct. *"System receives the order"* is wrong (that's the system's POV, not the user's). NN/G is firm: the journey is the user's experience, not the system's processing.

**Bound check:** if the inputs justify fewer than 3 steps in a phase, the phase boundary may be wrong (merge with neighbour or split differently). If they justify more than 8, sub-phases are merging too aggressively (split the phase).

State the step shape per phase aloud.

---

## Round 4 — Touchpoints, channels, backstage

For each step, identify:

- **Touchpoint** — the screen / surface / physical artefact the user contacts (*"ticket UI"*, *"CRM customer page"*, *"phone"*).
- **Channel** — the medium category (web / mobile / phone / email / in-person / chat / paper).
- **Backstage system** — any system or process running out of sight that the step depends on (*"CRM API"*, *"manual handoff to billing team"*, *"nightly batch sync"*).

Each cell that has content carries `[SRC: <filename>]`. Cells with no proxy in the inputs stay empty (render as `—` in the swim-lane table); the analyser does not invent touchpoints or backstage systems.

This is the **inputs-leaning** round. Touchpoint and channel are usually well-evidenced in briefs (briefs describe systems by name). Backstage is medium-evidenced (integrations and handoffs are usually mentioned). The next round (thoughts / emotions) is the inference-heavy one.

---

## Round 5 — Thoughts, emotions, pain points

This is the **inference-aware** round. The analyser must respect the source-of-truth hierarchy.

### Thoughts

Verbatim quoted thoughts only. If a source says *"users tell us they're not sure which approval link to click"*, the thought is `"not sure which approval link to click"` with `[SRC: <filename>]`. If no source quotes a thought, the cell stays empty. **Do not invent thoughts from analyst world knowledge.**

### Emotions (proxy-derived)

Emotion scores are integers in [−2, +2]:

| Score | Label | Proxy in inputs |
|---|---|---|
| **+2** | Delighted / confident | Explicit positive quote: *"users love how fast this is"*, *"customers report being delighted"* |
| **+1** | Engaged / hopeful | Positive language without intensifier: *"helpful"*, *"useful"*, *"works well"* |
| **0** | Neutral | No emotional language; routine task with no friction signal |
| **−1** | Anxious / impatient | Friction proxy: *"takes 30 minutes today"*, *"users complain about"*, *"error-prone"*, *"confusing"* |
| **−2** | Frustrated / panicked | Strong negative: *"users hate"*, *"escalates to management"*, *"abandons the workflow"*, *"calls support every time"* |

The cell renders the emotion label + score + the proxy quote inline, e.g.:

```
−1 impatient (proxy: "takes 30 minutes today") [SRC: brief-v3.pdf]
```

This makes the inference path transparent: the consultant can audit the proxy and decide whether the score is defensible. **Stay-silent rule:** if there is no proxy in any consumed source for a step's emotion, leave the cell empty (`—`) and record `[GAP-NO-EVIDENCE]` in the diagnostics block. **Do not fabricate emotions.**

A flat emotion curve (every phase at 0) is suspicious — it usually means the analyser stopped inferring rather than the experience being actually monotonic. The 8 hard gates include a non-flat-curve check; if the curve is flat the analyser must either find more proxies in the inputs or surface the issue in diagnostics.

### Pain points

Explicit pain statements in the inputs, named verbatim or paraphrased: *"approval requests get lost in email"*, *"the account ID has to be re-keyed in three systems"*. Each pain point carries `[SRC: <filename>]` and is anchored to a specific step or phase boundary (the swim-lane table renders pain in the `.lane-pain` row aligned with the affected phase column).

Pain points are usually well-evidenced in briefs (briefs exist *because* of pain).

---

## Round 6 — Opportunities and moments of truth

### Opportunities

For every pain point, derive ≥ 1 opportunity. Opportunities are **verb-led** and **solution-agnostic**:

| Pain | Opportunity |
|---|---|
| *"account ID has to be re-keyed in three systems"* | *"Auto-fill the account ID across systems"* |
| *"approval requests get lost in email"* | *"Surface approval requests in a shared queue"* |
| *"users don't know which approver is on call"* | *"Show the active approver inline on every approval"* |

Opportunities **inherit** the parent pain's `[SRC: <filename>]` set. They are seeds for the `/requirements` drafter, not authored requirements.

**Hard rule:** every pain point has ≥ 1 opportunity. A pain without an opportunity is either (a) a pain the inputs name as out-of-scope (rare; surface the reason in diagnostics) or (b) a missing inference the analyser should make. The 8 hard gates include this check.

### Moments of truth

A phase is a **moment of truth** if any of:

- The emotion score drops by ≥ 2 between the previous phase and this one.
- The inputs use explicit stakes language (*"critical"*, *"high-stakes"*, *"audit-relevant"*, *"customer-facing"*).
- The phase is a hand-off across teams / systems where evidence shows friction.

Moments-of-truth carry `[SRC: <filename>]` for the stake-language quote if applicable, or are derived from the sentiment-drop with the previous-phase + current-phase scores recorded. Every journey card flags ≥ 1 moment of truth (a journey with zero moments is rare and is flagged in diagnostics as a structural anomaly).

---

## Emotion-curve SVG spec (analyser-rendered inline)

The analyser generates each persona's emotion curve deterministically via the same algorithm USER-JOURNEYS uses (adapt `render_emotion_svg(phases, scores, moments)` from `framework/agents/analyses/user-journeys-analyser.md`):

- `viewBox="0 0 720 200"` — fixed aspect ratio.
- Y-axis: −2 at y=180, 0 at y=100, +2 at y=20. Horizontal gridlines at y=20, 60, 100, 140, 180 (class `gridline`). Y-axis line at x=40 (class `axis`).
- X-axis: one tick per phase, evenly spaced over x=60…700. Phase labels (class `phase-label`) at y=195, centred over their tick. XML-escape phase strings.
- Polyline (class `curve`) connecting `(tick_x, score_to_y(score))` for each phase, in phase order.
- Per-phase data point — `<circle class="point">` radius 4. Moments-of-truth get `class="point moment"` for emphasis.
- Y-axis labels (class `axis-label`): "+2", "+1", "0", "−1", "−2" at x=32, right-aligned.
- `<svg>` carries `role="img"` and `aria-label="Emotion curve for {persona} — {scenario}"`. XML-escape persona / scenario.

The swim-lane table below the SVG is the screen-reader-accessible equivalent.

---

## Swim-lane table spec (analyser-rendered CSS Grid)

Per persona, one `<table>` inside a `<figure class="swimlane">`:

```html
<table>
  <thead>
    <tr>
      <th scope="col">Lane / Phase</th>
      <th scope="col">{phase-1}</th>
      ...
      <th scope="col">{phase-N}</th>
    </tr>
  </thead>
  <tbody>
    <tr class="lane-actions">
      <th scope="row">Actions</th>
      <td>… [SRC: …]</td>
      ...
    </tr>
    <tr class="lane-touchpoints"><th>Touchpoints</th>…</tr>
    <tr class="lane-channels"><th>Channels</th>…</tr>
    <tr class="lane-thoughts"><th>Thoughts</th>…</tr>
    <tr class="lane-pain"><th>Pain points</th>…</tr>
    <tr class="lane-backstage"><th>Backstage</th>…</tr>
    <tr class="lane-opportunities"><th>Opportunities</th>…</tr>
  </tbody>
</table>
```

- Seven lanes in fixed order. All seven `<tr>` are always rendered per persona; empty cells render as `<td>—</td>` (not omitted — the column / lane grid stays intact).
- Each `<td>` carries `[SRC: <filename>]` (or `[STANDARD-RULE: GR-NN]`) markers inline as plain text within the cell body. The markitdown round-trip preserves them.
- Multi-item cells render as `<ul>` with one `<li>` per item, each ending in its own `[SRC: …]` marker.
- HTML-escape `<`, `>`, `&`, `"`, `'` in every consultant-supplied string.

---

## Source-of-truth hierarchy

The analyser fills cells according to this hierarchy. The marker hierarchy is:

1. **Verbatim from a manifest-listed input file** → `[SRC: <filename>]` with the verbatim quote in the cell.
2. **Paraphrased from a named input file** → `[SRC: <filename>]` with the paraphrase.
3. **Anchored to a general rule** → `[STANDARD-RULE: GR-NN]` payload is the rule ID; used when a cell's content is determined by a `framework/shared/general-rules.md` clause (rare in journey mapping; expect mostly `[SRC]`).
4. **Inferred from a proxy quote in the inputs** → cell renders the proxy quote inline + `[SRC: <filename>]` (transparency: the inference path is visible).
5. **No proxy** → stay silent; render `—`; record `[GAP-NO-EVIDENCE]` in diagnostics.

**No `[AI-SUGGESTED]` markers anywhere in the artefact** — `[AI-SUGGESTED]` is reserved for the `/requirements` drafter; the inputs-side analyser discipline is strict-extraction with proxy-transparency for inferred cells.

The analyser reads exactly the files the manifest enumerates, plus the prior artefact (for additive merge) and its own four asset files. The manifest's `tier` field dictates the read path:

| Tier | Source location | Read mechanism |
|---|---|---|
| `Native-text` | `original_path` | `Read` directly as text |
| `Native-multimodal` | `original_path` | `Read` — Claude's vision surfaces image bytes; transcribe visible text and structure |
| `Supported-via-MCP` | `converted_sibling` | `Read` the `.converted.md` (markitdown's output, produced by input-handler) |
| `Unsupported` | — | Skipped; recorded in `Source roster > Skipped` |

The analyser **never** reads:

- Any path under `requirements/` other than `requirements/source-manifest.json` and its enumerated rows' `original_path` / `converted_sibling`.
- Any path under `framework/state/`.
- Any path under `framework/shared/` (textual references to `RF-NN` / `GR-NN` in this file and in the analyser are links for the reader, not file loads).
- Other analyses' artefacts (`analyse-requirements/<METHOD>/…`, `analyse-inputs/<OTHER-METHOD>/…`).
- Any pattern-catalogue or design-system file.

---

## Provenance markers

| Marker | Used in section | Payload | Meaning |
|---|---|---|---|
| `[SRC: <filename>]` | Diagram-block cells, narrative bullets | basename + extension matching a manifest row's `filename` field | The cited content is anchored to this manifest source; if a verbatim quote is in the cell, it is from this source |
| `[STANDARD-RULE: GR-NN]` | Diagram-block cells (rare) | rule ID from `framework/shared/general-rules.md` | The cited content is determined by a general rule |
| `[GAP-NO-EVIDENCE]` | Diagnostics section only | (none) | A cell was left empty because no proxy was found in any consumed source |

**No `[AI-SUGGESTED]` markers anywhere in the artefact.** This methodology is extraction-with-proxy-transparency; invented inferences are not permitted.

---

## Quality gates (8 hard gates)

Run at Round 6 close, before render. Each gate captures `{gate_id, status: pass | fail, flagged_items: [...]}`:

1. **One persona per journey card.** Every `<article class="diagram-block">` has exactly one named persona. No persona merging.
2. **Phase count 3 ≤ phases ≤ 6** per journey card.
3. **Step count 3 ≤ steps ≤ 8 per phase** in every journey card.
4. **Every step has an action verb** with the user as subject (no "System receives X" anti-pattern).
5. **Every pain point has ≥ 1 opportunity** addressing it (bridge rule).
6. **≥ 1 moment of truth per journey card.** A card with zero moments is structurally suspect (either the inputs name no high-stakes phases — flag in diagnostics — or the analyser stopped inferring).
7. **Emotion curve non-flat OR documented as monotonic-by-evidence.** A flat curve (variation < 1 across phases) only passes if every score traces to a proxy quote in the inputs (no inference-by-default-to-zero allowed). Otherwise fail.
8. **Citation completeness.** Every non-empty cell in the swim-lane tables, every bridge bullet, every moment-of-truth bullet carries `[SRC: <filename>]` or `[STANDARD-RULE: GR-NN]`; every marker payload matches a manifest row's `filename` field exactly (or a valid `GR-NN`). Empty cells render `—` with a corresponding `[GAP-NO-EVIDENCE]` entry in diagnostics.

### Failure handling (Revise / Override / Restart)

On any hard-gate failure: do **not** write the artefact. Surface `AskUserQuestion` with three options:

1. `Revise — exit so the consultant can enrich input/ and re-invoke /analyse-inputs (Recommended)`
2. `Override — proceed and write a known-defective artefact (Run-history bullet records every violation)`
3. `Restart — re-run from Round 1 with a fresh manifest pass`

On **Revise**: hand back to the orchestrator with `failed-handback`.
On **Override**: record each failing gate in the Run-history bullet for this run; proceed to render.
On **Restart**: re-enter Round 1. Cap at three fail-Restart cycles; on the fourth, force the Revise path.

---

## Stop-condition

The analysis is complete when:

- `journeys` is non-empty (at least one persona × scenario pair survived Round 1–6).
- All 8 hard gates pass, or the consultant chose Override and the failures are recorded in diagnostics.
- The HTML has been rendered, every `<svg>` validates structurally (well-formed XML, polyline points = phase count, every `<text>` XML-escaped), every swim-lane `<tr>` has the expected lane class and N `<td>` cells (matching phase count).
- `analyse-inputs/JOURNEY-MAPPING/journey-mapping.html` has been written and `verify-artifact-write` returned `pass`.
- The consultant chose Accept in the handback loop.

---

## Re-run semantics

- The cursor (`manifest_sha256`, `run_count`) lives in the artefact's `<script type="application/json" id="journey-mapping-meta">` block. No state file under `framework/state/`.
- On re-run, the analyser parses the prior artefact's embedded JSON metadata block, compares the current manifest fingerprint to the prior cursor's value:
  - **No change** → pure additive widening; only new content from new manifest rows extends prior journey cards (if their personas / scenarios match) or seeds new journey cards.
  - **Change** → surface a drift prompt via `AskUserQuestion`:
    - `Append new content — preserve every prior journey card verbatim; extend cells where new manifest rows justify new content; seed new cards for new personas (Recommended)`
    - `Re-extract everything — re-run Rounds 1–6 from scratch on the current manifest; journey card headings preserved where re-extraction produces equivalent personas`
    - `Abort — exit without writing`
- The artefact is monotonically growing across runs unless the consultant explicitly chose `Re-extract everything` or manually edited the file.

---

## Common pitfalls (anti-patterns)

The analyser's character file enforces these as voice / discipline rules. Listed here for the consultant audit:

1. **Confusing stages with steps.** Stages are 3–6 phase headers; steps are 3–8 actions per stage. Conflating produces either a 30-stage scroll or a 5-stage outline with no detail.
2. **Confusing steps with touchpoints.** A step is what the user *does* (verb); a touchpoint is *where* the doing happens. One step can hit multiple touchpoints.
3. **Inventing emotions not in the source.** A pleasant-sounding "delighted" with no proxy is fiction. Stay silent — render `—` and `[GAP-NO-EVIDENCE]`.
4. **Inventing thoughts not in the source.** Thoughts are quotable mental content; without a quote, leave empty.
5. **Conflating actor with persona with role.** One map = one named actor / persona instance. If inputs imply N personas, produce N journey cards.
6. **Documenting internal processes from the company's POV.** Every action's subject is the user. *"User submits form"* not *"System receives form"*.
7. **Skipping pain points to keep the map "positive".** A pain-free map is suspicious — briefs exist because pain exists.
8. **Skipping opportunities columns.** NN/G is explicit: opportunities are the most-valuable column.
9. **Too little detail** (5 stages, no steps, no pain) → diagram-not-tool. **Too much detail** (30 steps per stage) → spreadsheet nobody reads. Sweet spot: 3–6 phases × 3–8 steps.
10. **Treating the map as a deliverable instead of an analysis.** The map's value is the *opportunities it surfaces*.
11. **Merging multiple personas into one "average" map.** NN/G is unanimous: no merging.
12. **Using future-state language in a current-state map.** *"The user should be able to…"* belongs in requirements; *"The user struggles to…"* belongs in the journey map.
13. **Letting the emotion curve be flat.** A flat curve almost always means the analyser stopped inferring rather than the experience being actually monotonic. Gate 7 catches this.

---

## Downstream consumption (handled by `framework/skills/map-journey-mapping-from-inputs-to-ui.md`)

The analyser does not author requirements; the downstream mapping documents how this artefact's signals route into the requirements draft:

| Journey-map cell | Generates this seed for `/requirements` |
|---|---|
| **Phases** | `§5 Task flows` backbone (one task-flow outline per persona × scenario) |
| **Actions** | Functional requirements (`§6.2 Functional`) — the system must allow X |
| **Touchpoints** | Screen / view inventory (`§8 Source UI references`) + multi-platform requirements |
| **Channels** | Channel-coverage requirements (multi-platform / multi-channel sections of `§6.2`) |
| **Pain points** | Non-functional requirements (`§6.1 NFRs`) — performance / error-handling / discoverability / recoverability |
| **Opportunities** | User-story seeds (`§4 User goals & stories`) |
| **Backstage** | Integration requirements (`§6.5 Integrations`) — system-to-system contracts, data dependencies |
| **Thoughts** | Help / onboarding / confirmation / microcopy requirements (the system must answer the question the user is asking at this step) |
| **Sentiment curve** | Prioritisation signal — low-sentiment phases get higher requirements-drafting priority |
| **Moments of truth** | Reliability + observability requirements (P0 priority annotation; these touchpoints must not fail silently) |

When the consultant re-drops `journey-mapping.html` into `input/`, the drafter reads it as a `Markitdown-text`-tier source. The drafter's claim-citation traces *through* the journey map to the original brief filenames via the `[SRC: <filename>]` markers preserved through markitdown conversion. The audit trail is end-to-end.

`framework/skills/map-journey-mapping-from-inputs-to-ui.md` is a stub at MVP — the mapping is documented here for the analyser's character file and for future downstream design-spec authors.
